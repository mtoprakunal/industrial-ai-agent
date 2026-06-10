// ============================================================
// wsServer.js — Tarayıcıya açılan WebSocket sunucusu
// ------------------------------------------------------------
// Sorumluluklar:
//   - Bağlanan istemciye anında FULL_UPDATE (son değer önbelleği) gönder
//   - Tüm istemcilere TAG_UPDATE / BATCH_UPDATE / CONNECTION_STATUS yay
//   - WRITE_TAG isteklerini doğrula ve OpcuaManager.writeTag'e ilet, WRITE_ACK döndür
//   - ping/pong ile ölü (hayalet) bağlantıları temizle
//
// Tek serileştirme, çok gönderim: broadcast içinde JSON.stringify döngü dışında.
// ============================================================

import { WebSocketServer, WebSocket } from 'ws';
import { config } from './config.js';

export class HmiWsServer {
    constructor(opcua) {
        this.opcua = opcua;
        this.clients = new Map(); // id -> { ws, lastPong }
        this.counter = 0;

        // Son bilinen değer önbelleği (yeni istemciye anında snapshot için).
        // "push" mimarisini "pull-on-connect" ile birleştiren zorunlu nokta.
        this.tagCache = {}; // tag -> { value, quality, timestamp }

        // Batch penceresi: 100ms'de gelen tüm değişimleri tek mesajda topla
        this.pending = new Map(); // tag -> { value, quality, timestamp }
        this.batchTimer = null;

        this.wss = new WebSocketServer({
            port: config.wsPort,
            maxPayload: 1_000_000, // 1MB — HMI için 100MB varsayılanı gereksiz büyük
        });
        this._setup();
        this._startPing();

        // OPC-UA -> WebSocket köprüsü
        this.opcua.on('tagUpdate', (u) => this._onTagUpdate(u));
        this.opcua.on('statusChange', (s) =>
            this.broadcast({ type: 'CONNECTION_STATUS', status: s })
        );

        console.log(`[ws] listening on ws://0.0.0.0:${config.wsPort}`);
    }

    _setup() {
        this.wss.on('connection', (ws, req) => {
            const id = `c${++this.counter}`;
            this.clients.set(id, { ws, lastPong: Date.now() });
            const ip = req.socket.remoteAddress;
            console.log(`[ws] client ${id} connected (${ip}) total=${this.clients.size}`);

            // Yeni istemciye mevcut durumu gönder: önce snapshot, sonra delta akışı
            this._send(ws, {
                type: 'FULL_UPDATE',
                data: this.tagCache,
                status: this.opcua.getStatus(),
            });

            ws.on('message', (raw) => {
                let msg;
                try {
                    msg = JSON.parse(raw.toString());
                } catch {
                    console.warn(`[ws] invalid JSON from ${id}`);
                    return;
                }
                this._handleMessage(id, ws, msg);
            });

            ws.on('pong', () => {
                const c = this.clients.get(id);
                if (c) c.lastPong = Date.now();
            });

            ws.on('close', () => {
                this.clients.delete(id);
                console.log(`[ws] client ${id} disconnected total=${this.clients.size}`);
            });

            ws.on('error', (err) => {
                console.error(`[ws] client ${id} error: ${err.message}`);
                this.clients.delete(id);
            });
        });
    }

    async _handleMessage(id, ws, msg) {
        switch (msg.type) {
            case 'PONG':
                {
                    const c = this.clients.get(id);
                    if (c) c.lastPong = Date.now();
                }
                break;

            case 'REQUEST_FULL_UPDATE':
                // Sekme arka plandan döndüğünde frontend bunu ister
                this._send(ws, {
                    type: 'FULL_UPDATE',
                    data: this.tagCache,
                    status: this.opcua.getStatus(),
                });
                break;

            case 'WRITE_TAG':
                await this._handleWrite(id, ws, msg);
                break;

            default:
                console.warn(`[ws] unknown message type from ${id}: ${msg.type}`);
        }
    }

    async _handleWrite(id, ws, msg) {
        // Yazma kimlik doğrulaması (basit paylaşılan token).
        // Token tanımlıysa eşleşmeli; üretimde gerçek oturum/JWT ile değiştir.
        if (config.writeAuthToken && msg.authToken !== config.writeAuthToken) {
            this._send(ws, {
                type: 'WRITE_ACK',
                writeTag: msg.writeTag,
                success: false,
                error: 'unauthorized',
            });
            return;
        }

        const { writeTag, value } = msg;
        const result = await this.opcua.writeTag(writeTag, value);

        // Yazma audit log'u — kim, ne, sonuç
        console.log(`[write] ${id} ${writeTag}=${value} -> ${result.success ? 'OK' : 'FAIL'}`);

        this._send(ws, {
            type: 'WRITE_ACK',
            writeTag,
            success: result.success,
            error: result.error,
        });
    }

    _onTagUpdate(u) {
        // Önbelleği güncelle (yeni istemci snapshot'ı için)
        this.tagCache[u.tag] = { value: u.value, quality: u.quality, timestamp: u.timestamp };

        // Batch kuyruğa al — aynı tag tek pencerede birden çok değişirse son değer kalır
        this.pending.set(u.tag, { value: u.value, quality: u.quality, timestamp: u.timestamp });
        if (!this.batchTimer) {
            this.batchTimer = setTimeout(() => this._flush(), config.batchIntervalMs);
        }
    }

    _flush() {
        this.batchTimer = null;
        if (this.pending.size === 0) return;
        const updates = Object.fromEntries(this.pending);
        this.pending.clear();
        this.broadcast({ type: 'BATCH_UPDATE', updates });
    }

    // Tek serileştirme, tüm istemcilere gönderim + backpressure koruması
    broadcast(msg) {
        const data = JSON.stringify(msg);
        for (const [id, { ws }] of this.clients) {
            if (ws.readyState !== WebSocket.OPEN) continue;
            // Yavaş istemci tüm sistemi yavaşlatmasın
            if (ws.bufferedAmount > 1_000_000) {
                console.warn(`[ws] backpressure on ${id}, skipping`);
                continue;
            }
            ws.send(data);
        }
    }

    _send(ws, msg) {
        if (ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify(msg));
    }

    // Protokol-seviyesi ping/pong — fd-level canlılık + hayalet bağlantı temizliği
    _startPing() {
        this.pingTimer = setInterval(() => {
            const now = Date.now();
            for (const [id, c] of this.clients) {
                if (now - c.lastPong > 60000) {
                    console.log(`[ws] terminating stale client ${id}`);
                    c.ws.terminate();
                    this.clients.delete(id);
                } else if (c.ws.readyState === WebSocket.OPEN) {
                    c.ws.ping();
                }
            }
        }, 30000);
    }

    stop() {
        if (this.pingTimer) clearInterval(this.pingTimer);
        if (this.batchTimer) clearTimeout(this.batchTimer);
        this.wss.close();
    }
}
