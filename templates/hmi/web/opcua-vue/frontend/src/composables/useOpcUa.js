// ============================================================
// composables/useOpcUa.js — WebSocket köprü istemcisi (SINGLETON)
// ------------------------------------------------------------
// Tarayıcı OPC-UA konuşamaz; gateway ile WebSocket üzerinden konuşur.
// Singleton: tüm bileşenler TEK bağlantıyı paylaşır (05 Hata 4).
// Otomatik yeniden bağlanma (exponential backoff + jitter),
// uygulama-seviyesi PING/PONG, yazma proxy'si içerir.
// ============================================================
import { useHmiStore } from '../store/hmi';

const WS_URL = import.meta.env.VITE_WS_URL || `ws://${window.location.hostname}:8080`;
const WRITE_TOKEN = import.meta.env.VITE_WRITE_TOKEN || '';
const INITIAL_DELAY = 1000;
const MAX_DELAY = 30000;

// Modül seviyesi durum — singleton garantisi
let ws = null;
let reconnectDelay = INITIAL_DELAY;
let reconnectTimer = null;
let manualClose = false;
let store = null;

function connect() {
    if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) return;

    store.setWsStatus('CONNECTING');
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
        store.setWsStatus('CONNECTED');
        reconnectDelay = INITIAL_DELAY; // başarılı bağlantıda backoff sıfırla
    };

    ws.onmessage = (event) => {
        let msg;
        try { msg = JSON.parse(event.data); } catch { return; }
        handleMessage(msg);
    };

    ws.onclose = (e) => {
        store.setWsStatus('DISCONNECTED');
        // 1000 = temiz kapanış; sadece ağ kaynaklı kopmalarda yeniden bağlan (05)
        if (!manualClose && e.code !== 1000) scheduleReconnect();
    };

    ws.onerror = () => store.setWsStatus('ERROR');
}

function handleMessage(msg) {
    switch (msg.type) {
        case 'FULL_UPDATE':
            store.applyBatch(msg.data || {});
            store.setAlarms(msg.alarms || []);
            if (msg.status) store.setPlcStatus(msg.status);
            break;

        case 'BATCH_UPDATE':
            store.applyBatch(msg.updates || {});
            break;

        case 'CONNECTION_STATUS': // gateway <-> PLC durumu
            store.setPlcStatus(msg.status);
            break;

        case 'ALARM_ACTIVE':
            store.setAlarm(msg.tag, msg.priority, msg.text, msg.since);
            break;

        case 'ALARM_CLEAR':
            store.clearAlarm(msg.tag);
            break;

        case 'PING': // gateway protokol ping'i ws katmanında, bu uygulama-seviyesi yedeği
            send({ type: 'PONG' });
            break;
    }
}

function scheduleReconnect() {
    if (reconnectTimer) return;
    // Jitter: thundering herd önle (05 Optimizasyon md.7)
    const delay = reconnectDelay + Math.floor(Math.random() * 1000);
    reconnectTimer = setTimeout(() => {
        reconnectTimer = null;
        connect();
        reconnectDelay = Math.min(reconnectDelay * 2, MAX_DELAY);
    }, delay);
}

function send(msg) {
    if (ws?.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(msg));
        return true;
    }
    return false;
}

// Tag yazma — gateway WRITE komutuna çevrilir
function writeTag(tag, value) {
    return send({ type: 'WRITE', tag, value, token: WRITE_TOKEN });
}

// Sekme arka plandan dönünce tam durum iste (05 visibilitychange)
function onVisibility() {
    if (document.visibilityState === 'visible' && ws?.readyState === WebSocket.OPEN) {
        send({ type: 'REQUEST_FULL_UPDATE' });
    }
}

export function useOpcUa() {
    // store'u ilk çağrıda bağla (Pinia aktif olmalı)
    if (!store) store = useHmiStore();

    function init() {
        manualClose = false;
        connect();
        document.addEventListener('visibilitychange', onVisibility);
        // F5/sekme kapanışında temiz kapanış (05 Not 8)
        window.addEventListener('beforeunload', () => ws?.close(1000));
    }

    function disconnect() {
        manualClose = true;
        if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = null; }
        document.removeEventListener('visibilitychange', onVisibility);
        ws?.close(1000, 'Client disconnect');
    }

    return { init, disconnect, writeTag };
}
