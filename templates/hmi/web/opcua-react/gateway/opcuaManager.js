// ============================================================
// opcuaManager.js — node-opcua ile PLC OPC-UA istemcisi
// ------------------------------------------------------------
// Sorumluluklar:
//   - PLC'ye bağlan (connect + createSession)
//   - namespace index'i URI'dan DİNAMİK al (hardcode etme!)
//   - subscription + monitored item kur, değişimleri "tagUpdate" ile yay
//   - bağlantı kopmasını izle ve otomatik yeniden bağlan
//   - frontend'den gelen yazma isteklerini writeNode'a çevir
//   - "statusChange" olayı ile bağlantı durumunu yay
//
// Olaylar (EventEmitter):
//   "tagUpdate"    -> { tag, value, quality, timestamp }
//   "statusChange" -> "DISCONNECTED" | "CONNECTING" | "CONNECTED" | "ERROR"
// ============================================================

import { EventEmitter } from 'node:events';
import {
    OPCUAClient,
    MessageSecurityMode,
    SecurityPolicy,
    AttributeIds,
    TimestampsToReturn,
    DataChangeFilter,
    DataChangeTrigger,
    DeadbandType,
} from 'node-opcua';

import { config, MONITORED_TAGS, WRITABLE_TAGS } from './config.js';

// OPC-UA StatusCode -> sade kalite metni
function qualityOf(dataValue) {
    if (dataValue.statusCode.isGood()) return 'GOOD';
    if (dataValue.statusCode.isBad()) return 'BAD';
    return 'UNCERTAIN';
}

export class OpcuaManager extends EventEmitter {
    constructor() {
        super();
        this.client = null;
        this.session = null;
        this.subscription = null;
        this.status = 'DISCONNECTED';
        this.nsIdx = 4; // başlangıç tahmini; bağlanınca URI'dan güncellenir
        this.reconnectTimer = null;
    }

    // Sembol yolunu (config) gerçek nodeId string'ine çevir
    _nodeId(symbolPath) {
        return `ns=${this.nsIdx};s=${symbolPath}`;
    }

    _setStatus(status) {
        if (this.status === status) return;
        this.status = status;
        this.emit('statusChange', status);
    }

    getStatus() {
        return this.status;
    }

    async connect() {
        if (this.status === 'CONNECTING' || this.status === 'CONNECTED') return;
        this._setStatus('CONNECTING');

        try {
            this.client = OPCUAClient.create({
                applicationName: 'WebHMI_React_Gateway',
                applicationUri: 'urn:WebHMI:React:Gateway',
                connectionStrategy: { initialDelay: 1000, maxRetry: 3, maxDelay: 10000 },
                securityMode: MessageSecurityMode[config.opcua.securityMode] ?? MessageSecurityMode.None,
                securityPolicy: SecurityPolicy[config.opcua.securityPolicy] ?? SecurityPolicy.None,
                endpointMustExist: false,
            });

            // Çalışma sırasında bağlantı kopması (NAT/firewall idle drop dahil)
            this.client.on('connection_lost', () => {
                console.error('[opcua] connection_lost');
                this._setStatus('DISCONNECTED');
                this._scheduleReconnect();
            });
            this.client.on('connection_reestablished', () => {
                console.log('[opcua] connection_reestablished');
            });

            await this.client.connect(config.opcua.endpoint);

            this.session = await this.client.createSession({
                userName: config.opcua.user || undefined,
                password: config.opcua.pass || undefined,
                // CODESYS varsayılan session timeout düşük olabilir; uzun tut.
                requestedSessionTimeout: 3600000,
            });

            this.session.on('session_closed', () => {
                console.warn('[opcua] session_closed');
                this._setStatus('DISCONNECTED');
                this._scheduleReconnect();
            });

            // Namespace index'i URI'dan dinamik al — ns=4 hardcode etme!
            this.nsIdx = await this.session.getNamespaceIndex(config.opcua.namespaceUri);
            console.log(`[opcua] connected to ${config.opcua.endpoint} (ns=${this.nsIdx})`);

            await this._setupSubscription();
            this._setStatus('CONNECTED');
        } catch (err) {
            console.error(`[opcua] connect error: ${err?.message || err}`);
            this._setStatus('ERROR');
            this._scheduleReconnect();
        }
    }

    async _setupSubscription() {
        // 6:1 lifetime/keepalive oranı güvenli (bkz. knowledge 01_opcua_clients_js)
        this.subscription = await this.session.createSubscription2({
            requestedPublishingInterval: 250,
            requestedMaxKeepAliveCount: 20,
            requestedLifetimeCount: 120,
            maxNotificationsPerPublish: 1000,
            publishingEnabled: true,
            priority: 128,
        });

        this.subscription.on('terminated', () => {
            console.warn('[opcua] subscription terminated — reconnect');
            this._setStatus('DISCONNECTED');
            this._scheduleReconnect();
        });

        for (const { tag, symbolPath, sampling, deadband } of MONITORED_TAGS) {
            const monitoringParams = {
                samplingInterval: sampling,
                discardOldest: true,
                queueSize: 10,
            };
            // Analog tag'lerde deadband — gürültü = değişim sayılmasın
            if (deadband) {
                monitoringParams.filter = new DataChangeFilter({
                    trigger: DataChangeTrigger.StatusValue,
                    deadbandType: DeadbandType.Absolute,
                    deadbandValue: deadband,
                });
            }

            const item = await this.subscription.monitor(
                { nodeId: this._nodeId(symbolPath), attributeId: AttributeIds.Value },
                monitoringParams,
                TimestampsToReturn.Both
            );

            item.on('changed', (dv) => {
                this.emit('tagUpdate', {
                    tag,
                    value: dv.value?.value ?? null,
                    quality: qualityOf(dv),
                    // WebSocket üzerinden Date taşınmaz -> epoch ms gönder
                    timestamp: (dv.sourceTimestamp || dv.serverTimestamp || new Date()).getTime(),
                });
            });
        }

        console.log(`[opcua] subscription ready (${MONITORED_TAGS.length} monitored items)`);
    }

    // Frontend'den gelen yazma isteğini OPC-UA writeNode'a çevir.
    // writeTag: WRITABLE_TAGS anahtarı. Döner: { success, error? }
    async writeTag(writeTag, value) {
        if (!this.session || this.status !== 'CONNECTED') {
            return { success: false, error: 'OPC-UA not connected' };
        }
        const def = WRITABLE_TAGS[writeTag];
        if (!def) {
            return { success: false, error: `unknown writeTag: ${writeTag}` };
        }

        try {
            // dataType config'te sabit — TypeMismatch'ten kaçınmak için doğru ver.
            const statusCode = await this.session.write({
                nodeId: this._nodeId(def.symbolPath),
                attributeId: AttributeIds.Value,
                value: { value: { dataType: def.dataType, value } },
            });

            if (statusCode.isGood()) {
                console.log(`[opcua] write OK ${writeTag} = ${value}`);
                return { success: true };
            }
            const error = statusCode.toString();
            console.error(`[opcua] write FAIL ${writeTag}: ${error}`);
            return { success: false, error };
        } catch (err) {
            const error = err?.message || String(err);
            console.error(`[opcua] write exception ${writeTag}: ${error}`);
            return { success: false, error };
        }
    }

    _scheduleReconnect() {
        if (this.reconnectTimer) return;
        console.log(`[opcua] reconnect in ${config.reconnectDelayMs}ms`);
        this.reconnectTimer = setTimeout(async () => {
            this.reconnectTimer = null;
            await this._teardown();
            await this.connect();
        }, config.reconnectDelayMs);
    }

    // Subscription + session + client'ı sırayla kapat (sızıntı önleme)
    async _teardown() {
        try {
            if (this.subscription) {
                await this.subscription.terminate();
            }
        } catch { /* yoksay */ }
        this.subscription = null;

        try {
            if (this.session) await this.session.close();
        } catch { /* yoksay */ }
        this.session = null;

        try {
            if (this.client) await this.client.disconnect();
        } catch { /* yoksay */ }
        this.client = null;
    }

    async disconnect() {
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
            this.reconnectTimer = null;
        }
        await this._teardown();
        this._setStatus('DISCONNECTED');
    }
}
