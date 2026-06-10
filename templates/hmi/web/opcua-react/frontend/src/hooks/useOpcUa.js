// ============================================================
// useOpcUa.js — Gateway'e singleton WebSocket bağlantısı
// ------------------------------------------------------------
// Tüm bileşenler aynı bağlantıyı paylaşır (her bileşen kendi WS açmaz!).
// Sorumluluklar:
//   - bağlan / otomatik yeniden bağlan (exponential backoff + jitter)
//   - gelen mesajları Zustand store'a yaz (TAG_UPDATE/BATCH/FULL/STATUS)
//   - uygulama-seviyesi PING'e PONG dön
//   - sekme arka plandan dönünce REQUEST_FULL_UPDATE iste (stale önleme)
//   - writeTag(): WRITE_TAG komutu gönder, WRITE_ACK'i Promise ile çöz
// ============================================================

import { useEffect, useRef, useCallback } from 'react';
import { useHmiStore } from '../store/hmiStore.js';

const WS_URL =
    import.meta.env.VITE_WS_URL || `ws://${window.location.hostname}:8080`;
const WRITE_AUTH_TOKEN = import.meta.env.VITE_WRITE_AUTH_TOKEN || '';

const INITIAL_RECONNECT_DELAY = 1000;
const MAX_RECONNECT_DELAY = 30000;

// --- Modül-seviyesi singleton durum ---
let ws = null;
let reconnectTimer = null;
let reconnectDelay = INITIAL_RECONNECT_DELAY;
let manualClose = false;
let refCount = 0;

// Bekleyen yazma istekleri: writeTag -> {resolve, timer}
const pendingWrites = new Map();

function storeApi() {
    return useHmiStore.getState();
}

function connect() {
    if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
        return;
    }
    manualClose = false;
    storeApi().setWsStatus('CONNECTING');
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
        reconnectDelay = INITIAL_RECONNECT_DELAY; // başarılı -> backoff sıfırla
        storeApi().setWsStatus('CONNECTED');
    };

    ws.onmessage = (event) => {
        let msg;
        try {
            msg = JSON.parse(event.data);
        } catch {
            return;
        }
        handleMessage(msg);
    };

    ws.onclose = (event) => {
        // Bekleyen yazmaları reddet
        for (const [, p] of pendingWrites) {
            clearTimeout(p.timer);
            p.resolve({ success: false, error: 'connection closed' });
        }
        pendingWrites.clear();

        if (!manualClose) {
            storeApi().setWsStatus('DISCONNECTED');
            // 1000 = temiz kapanış -> reconnect etme; diğerleri (1006 vb.) -> reconnect
            if (event.code !== 1000) scheduleReconnect();
        }
    };

    ws.onerror = () => {
        storeApi().setWsStatus('ERROR');
    };
}

function handleMessage(msg) {
    const s = storeApi();
    switch (msg.type) {
        case 'PING':
            send({ type: 'PONG' });
            break;
        case 'FULL_UPDATE':
            s.applyFullUpdate(msg.data || {});
            if (msg.status) s.setPlcStatus(msg.status);
            break;
        case 'BATCH_UPDATE':
            s.applyBatch(msg.updates || {});
            break;
        case 'TAG_UPDATE':
            s.updateTag(msg.tag, msg.value, msg.quality, msg.timestamp);
            break;
        case 'CONNECTION_STATUS':
            s.setPlcStatus(msg.status);
            break;
        case 'WRITE_ACK': {
            const p = pendingWrites.get(msg.writeTag);
            if (p) {
                clearTimeout(p.timer);
                pendingWrites.delete(msg.writeTag);
                p.resolve({ success: msg.success, error: msg.error });
            }
            break;
        }
        default:
            break;
    }
}

function scheduleReconnect() {
    if (reconnectTimer) return;
    // jitter -> thundering herd önleme (sunucu çökünce hepsi aynı anda dönmesin)
    const jitter = Math.floor(Math.random() * 1000);
    const delay = reconnectDelay + jitter;
    reconnectTimer = setTimeout(() => {
        reconnectTimer = null;
        connect();
        reconnectDelay = Math.min(reconnectDelay * 2, MAX_RECONNECT_DELAY);
    }, delay);
}

function send(obj) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(obj));
        return true;
    }
    return false;
}

// Yazma komutu — WRITE_ACK gelene kadar bekler (Promise). Timeout 5s.
function writeTag(writeTagName, value) {
    return new Promise((resolve) => {
        const ok = send({
            type: 'WRITE_TAG',
            writeTag: writeTagName,
            value,
            authToken: WRITE_AUTH_TOKEN || undefined,
        });
        if (!ok) {
            resolve({ success: false, error: 'not connected' });
            return;
        }
        // Aynı tag için eski bekleyeni temizle (son istek geçerli)
        const prev = pendingWrites.get(writeTagName);
        if (prev) clearTimeout(prev.timer);

        const timer = setTimeout(() => {
            pendingWrites.delete(writeTagName);
            resolve({ success: false, error: 'timeout' });
        }, 5000);
        pendingWrites.set(writeTagName, { resolve, timer });
    });
}

// ------------------------------------------------------------
// React hook — App seviyesinde bir kez kullanılır.
// Birden çok bileşen çağırsa bile refCount ile tek bağlantı korunur.
// ------------------------------------------------------------
export function useOpcUa() {
    const mounted = useRef(false);

    useEffect(() => {
        mounted.current = true;
        refCount += 1;
        connect();

        // Sekme tekrar görünür olunca tam güncelleme iste (donmuş veri önleme)
        const onVisible = () => {
            if (document.visibilityState === 'visible') {
                send({ type: 'REQUEST_FULL_UPDATE' });
            }
        };
        document.addEventListener('visibilitychange', onVisible);

        // Sayfa kapanırken temiz kapat (hayalet bağlantı önleme)
        const onUnload = () => {
            manualClose = true;
            ws?.close(1000, 'page unload');
        };
        window.addEventListener('beforeunload', onUnload);

        return () => {
            mounted.current = false;
            refCount -= 1;
            document.removeEventListener('visibilitychange', onVisible);
            window.removeEventListener('beforeunload', onUnload);
            // Son tüketici de gidince bağlantıyı kapat
            if (refCount <= 0) {
                manualClose = true;
                if (reconnectTimer) {
                    clearTimeout(reconnectTimer);
                    reconnectTimer = null;
                }
                ws?.close(1000, 'no consumers');
            }
        };
    }, []);

    const sendWrite = useCallback((tagName, value) => writeTag(tagName, value), []);

    return { writeTag: sendWrite };
}
