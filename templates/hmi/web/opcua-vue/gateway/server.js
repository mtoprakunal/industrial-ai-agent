// ============================================================
// server.js — OPC-UA -> WebSocket Gateway
// ------------------------------------------------------------
// Mimari (knowledge/hmi/web-based/05_realtime_websocket.md):
//   Tarayıcı OPC-UA (opc.tcp ham TCP) konuşamaz. Bu gateway:
//     PLC tarafı : node-opcua ile subscription kurar, değerleri dinler.
//     Tarayıcı tarafı : ws ile WebSocket sunucusu açar, değerleri iter.
//     Yazma : tarayıcıdan gelen WRITE komutunu PLC'ye proxy'ler.
//
//   1 PLC bağlantısı -> N tarayıcı (broadcast). Tek subscription tüm
//   istemcileri besler (05 Not 1: %98 kaynak tasarrufu).
// ============================================================

import { EventEmitter } from 'node:events';
import { WebSocketServer, WebSocket } from 'ws';
import {
    OPCUAClient,
    MessageSecurityMode,
    SecurityPolicy,
    AttributeIds,
    TimestampsToReturn,
} from 'node-opcua';

import { config, TAGS, ALARM_DEFS } from './config.js';

// ============================================================
// 1) OPC-UA MANAGER — PLC bağlantısı, subscription, yazma, reconnect
// ============================================================
class OpcUaManager extends EventEmitter {
    constructor() {
        super();
        this.client = null;
        this.session = null;
        this.subscription = null;
        this.status = 'DISCONNECTED'; // DISCONNECTED | CONNECTING | CONNECTED | ERROR
        this.reconnectTimer = null;
        this.nsIdx = null;
        // Çözümlenmiş NodeId'ler: tagName -> "ns=4;s=..." (gerçek index ile)
        this.nodeIds = {};
    }

    setStatus(status) {
        if (this.status === status) return;
        this.status = status;
        this.emit('status', status);
    }

    // Tag yolundaki {ns} yer tutucusunu gerçek namespace index ile doldurur.
    resolveNodeIds() {
        this.nodeIds = {};
        for (const [tag, def] of Object.entries(TAGS)) {
            this.nodeIds[tag] = def.path.replace('{ns}', String(this.nsIdx));
        }
    }

    async connect() {
        if (this.status === 'CONNECTING' || this.status === 'CONNECTED') return;
        this.setStatus('CONNECTING');

        try {
            this.client = OPCUAClient.create({
                applicationName: 'OpcUaVueGateway',
                connectionStrategy: { initialDelay: 1000, maxRetry: 3, maxDelay: 10000 },
                securityMode: MessageSecurityMode[config.opcua.securityMode] ?? MessageSecurityMode.None,
                securityPolicy: SecurityPolicy[config.opcua.securityPolicy] ?? SecurityPolicy.None,
                endpointMustExist: false,
                // Session'ı uzun tut: idle WebSocket köprüsü timeout'a düşmesin (01 Not 3)
                requestedSessionTimeout: 3600000,
            });

            // Çalışma sırasında kopan bağlantı (NAT/firewall) — 01 Not 1
            this.client.on('connection_lost', () => {
                console.error('[OPC-UA] connection_lost');
                this.setStatus('DISCONNECTED');
                this.scheduleReconnect();
            });
            this.client.on('connection_reestablished', () =>
                console.log('[OPC-UA] connection_reestablished'),
            );

            await this.client.connect(config.opcua.endpoint);

            // Anonim mi, kullanıcı adı/şifre mi?
            const userIdentity = config.opcua.user
                ? { userName: config.opcua.user, password: config.opcua.pass }
                : undefined;
            this.session = await this.client.createSession(userIdentity);

            this.session.on('session_closed', () => {
                console.warn('[OPC-UA] session_closed');
                this.setStatus('DISCONNECTED');
                this.scheduleReconnect();
            });

            // Namespace index DİNAMİK al — hardcode etme (01 Hata 2 / Not 2)
            this.nsIdx = await this.session.getNamespaceIndex(config.opcua.namespaceUri);
            this.resolveNodeIds();
            console.log(`[OPC-UA] Bağlandı: ${config.opcua.endpoint} (ns=${this.nsIdx})`);

            await this.setupSubscription();
            this.setStatus('CONNECTED');
        } catch (err) {
            console.error(`[OPC-UA] connect hatası: ${err.message}`);
            this.setStatus('ERROR');
            this.scheduleReconnect();
        }
    }

    async setupSubscription() {
        if (!this.session) return;

        // Tek subscription, katmanlı sampling (01 Optimizasyon md.2)
        this.subscription = await this.session.createSubscription2({
            requestedPublishingInterval: 500,
            requestedMaxKeepAliveCount: 20,
            requestedLifetimeCount: 120, // ~6:1 oran (01 Derin Teknik Detay)
            maxNotificationsPerPublish: 1000,
            publishingEnabled: true,
            priority: 128,
        });

        // Sunucu requested değerleri revize edebilir — gerçek değeri logla (01 Not 4)
        console.log(
            `[OPC-UA] Subscription id=${this.subscription.subscriptionId}, ` +
            `publishingInterval=${this.subscription.publishingInterval}ms`,
        );

        this.subscription.on('terminated', () => {
            console.warn('[OPC-UA] subscription terminated — yeniden bağlanılacak');
            this.setStatus('DISCONNECTED');
            this.scheduleReconnect();
        });

        // Her tag için monitoredItem ekle
        for (const [tag, def] of Object.entries(TAGS)) {
            const nodeId = this.nodeIds[tag];
            const item = await this.subscription.monitor(
                { nodeId, attributeId: AttributeIds.Value },
                { samplingInterval: def.sampling, discardOldest: true, queueSize: 10 },
                TimestampsToReturn.Source,
            );

            item.on('changed', (dataValue) => {
                this.emit('tag', {
                    tag,
                    value: dataValue.value?.value,
                    quality: qualityOf(dataValue),
                    timestamp: (dataValue.sourceTimestamp || new Date()).getTime(),
                });
            });
        }
        console.log(`[OPC-UA] ${Object.keys(TAGS).length} tag izleniyor`);
    }

    // Tarayıcıdan gelen yazma komutunu PLC'ye iletir.
    async writeTag(tag, value) {
        const def = TAGS[tag];
        if (!def) return { success: false, error: `Bilinmeyen tag: ${tag}` };
        if (def.dir !== 'rw') return { success: false, error: `Tag salt okunur: ${tag}` };
        if (!this.session || this.status !== 'CONNECTED') {
            return { success: false, error: 'PLC bağlı değil' };
        }

        try {
            // dataType açıkça verilir — Bad_TypeMismatch'i önler (01 Not 6)
            const statusCode = await this.session.write({
                nodeId: this.nodeIds[tag],
                attributeId: AttributeIds.Value,
                value: { value: { dataType: def.dataType, value } },
            });
            const success = statusCode.isGood();
            if (!success) console.error(`[OPC-UA] write ${tag} başarısız: ${statusCode.toString()}`);
            return { success, error: success ? undefined : statusCode.toString() };
        } catch (err) {
            return { success: false, error: err.message };
        }
    }

    scheduleReconnect() {
        if (this.reconnectTimer) return;
        console.log(`[OPC-UA] ${config.reconnectDelayMs}ms sonra yeniden bağlanılacak...`);
        this.reconnectTimer = setTimeout(async () => {
            this.reconnectTimer = null;
            await this.disconnect();
            await this.connect();
        }, config.reconnectDelayMs);
    }

    async disconnect() {
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
            this.reconnectTimer = null;
        }
        try { if (this.subscription) await this.subscription.terminate(); } catch { /* yok say */ }
        try { if (this.session) await this.session.close(); } catch { /* yok say */ }
        try { if (this.client) await this.client.disconnect(); } catch { /* yok say */ }
        this.subscription = null;
        this.session = null;
        this.client = null;
        this.setStatus('DISCONNECTED');
    }
}

function qualityOf(dataValue) {
    if (dataValue.statusCode.isGood()) return 'GOOD';
    if (dataValue.statusCode.isBad()) return 'BAD';
    return 'UNCERTAIN';
}

// ============================================================
// 2) WEBSOCKET SUNUCUSU — broadcast, write proxy, heartbeat
// ============================================================
class HmiWebSocketServer {
    constructor(port, opc) {
        this.opc = opc;
        this.clients = new Map(); // clientId -> { ws, lastPong }
        this.counter = 0;
        // Son bilinen tüm tag değerleri — yeni bağlanan istemciye gönderilir (05)
        this.cache = {};
        // Aktif alarmlar: tag -> { priority, text, since }
        this.alarms = {};

        this.wss = new WebSocketServer({ port });
        this.setup();
        this.startPing();
        console.log(`[WS] WebSocket sunucusu :${port} dinleniyor`);
    }

    setup() {
        this.wss.on('connection', (ws, req) => {
            const id = `c${++this.counter}`;
            this.clients.set(id, { ws, lastPong: Date.now() });
            console.log(`[WS] Bağlandı ${id} (${req.socket.remoteAddress}), toplam: ${this.clients.size}`);

            // Yeni istemciye mevcut tam durumu gönder
            this.sendTo(id, {
                type: 'FULL_UPDATE',
                data: this.cache,
                alarms: Object.entries(this.alarms).map(([tag, a]) => ({ tag, ...a })),
                status: this.opc.status,
            });

            ws.on('message', (raw) => {
                let msg;
                try { msg = JSON.parse(raw.toString()); }
                catch { return console.warn(`[WS] Geçersiz JSON: ${id}`); } // 05 Hata 2
                this.handle(id, msg);
            });
            ws.on('pong', () => {
                const c = this.clients.get(id);
                if (c) c.lastPong = Date.now();
            });
            ws.on('close', () => {
                this.clients.delete(id);
                console.log(`[WS] Ayrıldı ${id}, kalan: ${this.clients.size}`);
            });
            ws.on('error', (e) => {
                console.error(`[WS] Hata ${id}: ${e.message}`);
                this.clients.delete(id);
            });
        });
    }

    async handle(id, msg) {
        switch (msg.type) {
            case 'PONG':
                { const c = this.clients.get(id); if (c) c.lastPong = Date.now(); }
                break;

            case 'REQUEST_FULL_UPDATE':
                this.sendTo(id, {
                    type: 'FULL_UPDATE',
                    data: this.cache,
                    alarms: Object.entries(this.alarms).map(([tag, a]) => ({ tag, ...a })),
                    status: this.opc.status,
                });
                break;

            case 'WRITE': {
                // Yazma kimlik doğrulaması (05 Hata 3). Token boşsa geliştirme modu.
                if (config.ws.writeAuthToken && msg.token !== config.ws.writeAuthToken) {
                    this.sendTo(id, { type: 'WRITE_ACK', tag: msg.tag, success: false, error: 'Yetkisiz' });
                    return;
                }
                const result = await this.opc.writeTag(msg.tag, msg.value);
                console.log(`[WRITE] ${id} -> ${msg.tag}=${msg.value} : ${result.success ? 'OK' : result.error}`);
                this.sendTo(id, { type: 'WRITE_ACK', tag: msg.tag, ...result });
                break;
            }

            default:
                console.warn(`[WS] Bilinmeyen mesaj tipi: ${msg.type}`);
        }
    }

    // Bir tag değiştiğinde: cache güncelle + alarm değerlendir
    onTag(update) {
        this.cache[update.tag] = {
            value: update.value,
            quality: update.quality,
            timestamp: update.timestamp,
        };
        this.evaluateAlarm(update);
    }

    // BOOL alarm tag'lerini ALARM_DEFS'e göre aktif/temiz olarak işle.
    evaluateAlarm(update) {
        const def = ALARM_DEFS[update.tag];
        if (!def) return;
        const active = update.value === true;

        if (active && !this.alarms[update.tag]) {
            this.alarms[update.tag] = { priority: def.priority, text: def.text, since: update.timestamp };
            this.broadcast({ type: 'ALARM_ACTIVE', tag: update.tag, ...this.alarms[update.tag] });
        } else if (!active && this.alarms[update.tag]) {
            delete this.alarms[update.tag];
            this.broadcast({ type: 'ALARM_CLEAR', tag: update.tag });
        }
    }

    broadcast(msg) {
        const data = JSON.stringify(msg); // tek serileştirme, çok gönderim (05 Not 7)
        for (const { ws } of this.clients.values()) {
            // Backpressure: yavaş istemci tüm sistemi yavaşlatmasın (05 Not 5)
            if (ws.readyState === WebSocket.OPEN && ws.bufferedAmount < 1_000_000) {
                ws.send(data);
            }
        }
    }

    sendTo(id, msg) {
        const c = this.clients.get(id);
        if (c?.ws.readyState === WebSocket.OPEN) c.ws.send(JSON.stringify(msg));
    }

    // Protokol-seviyesi ping + ölü bağlantı temizliği (05 Not 2/8)
    startPing() {
        this.pingTimer = setInterval(() => {
            const now = Date.now();
            for (const [id, c] of this.clients) {
                if (now - c.lastPong > 60000) {
                    console.log(`[WS] Ölü bağlantı sonlandırılıyor: ${id}`);
                    c.ws.terminate();
                    this.clients.delete(id);
                } else if (c.ws.readyState === WebSocket.OPEN) {
                    c.ws.ping();
                }
            }
        }, 30000);
    }

    stop() {
        clearInterval(this.pingTimer);
        this.wss.close();
    }
}

// ============================================================
// 3) BATCH MANAGER — tag güncellemelerini birleştir (05 BatchUpdateManager)
// ============================================================
class BatchManager {
    constructor(wsServer, intervalMs) {
        this.wsServer = wsServer;
        this.intervalMs = intervalMs;
        this.pending = new Map();
        this.timer = null;
    }

    queue(update) {
        // Aynı tag aynı pencerede birkaç kez değişse de yalnız son değer gider
        this.pending.set(update.tag, update);
        if (!this.timer) this.timer = setTimeout(() => this.flush(), this.intervalMs);
    }

    flush() {
        this.timer = null;
        if (this.pending.size === 0) return;
        const updates = {};
        for (const [tag, u] of this.pending) {
            updates[tag] = { value: u.value, quality: u.quality, timestamp: u.timestamp };
        }
        this.pending.clear();
        this.wsServer.broadcast({ type: 'BATCH_UPDATE', updates });
    }
}

// ============================================================
// 4) BAŞLATMA — bileşenleri birbirine bağla
// ============================================================
const opc = new OpcUaManager();
const wsServer = new HmiWebSocketServer(config.ws.port, opc);
const batch = new BatchManager(wsServer, config.batchIntervalMs);

opc.on('tag', (update) => {
    wsServer.onTag(update);      // cache + alarm değerlendirme (alarm anında broadcast)
    batch.queue(update);          // telemetri batch'lenerek iletilir
});

opc.on('status', (status) => {
    console.log(`[OPC-UA] durum -> ${status}`);
    wsServer.broadcast({ type: 'CONNECTION_STATUS', status });
});

opc.connect();

// Temiz kapanış — subscription + session + client + ws (01 Hata 3)
async function shutdown() {
    console.log('\n[GW] Kapatılıyor...');
    wsServer.stop();
    await opc.disconnect();
    process.exit(0);
}
process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
