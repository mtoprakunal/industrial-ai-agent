// ============================================================================
//  useWebSocket.js — Singleton WebSocket baglantisi
// ============================================================================
//  TEK baglanti tum uygulama icin (her bilesen kendi WS'sini ACMAZ; Not 4,
//  Hata 2). Modul-seviyesi singleton + exponential backoff reconnect.
//  (knowledge/hmi/web-based/05_realtime_websocket.md)
// ============================================================================

import { useEffect } from "react";
import { useHMIStore } from "../store/hmiStore.js";
import { WS_URL, WRITE_TOKEN } from "../config.js";

const INITIAL_RECONNECT_DELAY = 1000;
const MAX_RECONNECT_DELAY = 30000;

// --- Modul-seviyesi singleton durumu ---
let ws = null;
let reconnectDelay = INITIAL_RECONNECT_DELAY;
let reconnectTimer = null;
let manualClose = false;

function connect() {
  if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) return;

  const store = useHMIStore.getState();
  store.setConnectionStatus("CONNECTING");

  ws = new WebSocket(WS_URL);

  ws.onopen = () => {
    reconnectDelay = INITIAL_RECONNECT_DELAY; // basarili -> backoff sifirla
    useHMIStore.getState().setConnectionStatus("CONNECTED");
  };

  ws.onmessage = (event) => {
    let msg;
    try {
      msg = JSON.parse(event.data);
    } catch {
      return;
    }
    const s = useHMIStore.getState();

    switch (msg.type) {
      case "FULL_UPDATE":
        s.setFullUpdate(msg.data);
        if (msg.status) s.setConnectionStatus(msg.status === "CONNECTED" ? "CONNECTED" : s.connectionStatus);
        break;
      case "TAG_META":
        s.setMeta(msg.meta);
        break;
      case "TAG_UPDATE":
        // timestamp WS uzerinden number (epoch ms) gelir; Date'e cevirme (Not 7).
        s.updateTag(msg.tag, msg.value, msg.timestamp);
        break;
      case "CONNECTION_STATUS":
        // Bu, PLC <-> gateway baglanti durumudur (WS degil).
        s.setConnectionStatus(msg.status);
        break;
      case "ALARM":
        s.setAlarm(msg.tag, {
          active: msg.active,
          priority: msg.priority,
          text: msg.text,
          label: msg.label,
          timestamp: msg.timestamp,
        });
        break;
      case "WRITE_ACK":
        s.setWriteAck(msg.tag, msg.success, msg.error);
        break;
      default:
        break;
    }
  };

  ws.onclose = () => {
    if (!manualClose) {
      useHMIStore.getState().setConnectionStatus("DISCONNECTED");
      scheduleReconnect();
    }
  };

  ws.onerror = () => {
    useHMIStore.getState().setConnectionStatus("ERROR");
    // onerror'u onclose izler; reconnect orada planlanir.
  };
}

function scheduleReconnect() {
  if (reconnectTimer) return;
  reconnectTimer = setTimeout(() => {
    reconnectTimer = null;
    connect();
    // Exponential backoff + jitter (thundering herd onleme).
    reconnectDelay = Math.min(reconnectDelay * 2, MAX_RECONNECT_DELAY) + Math.floor(Math.random() * 500);
  }, reconnectDelay);
}

// Yazma komutu gonder (coil veya register).
export function sendWrite(type, tag, value) {
  if (ws?.readyState !== WebSocket.OPEN) return false;
  ws.send(JSON.stringify({ type, tag, value, token: WRITE_TOKEN }));
  return true;
}

// Sekme arka plandan donunce tam guncelleme iste (timer throttle -> stale).
function requestFullUpdate() {
  if (ws?.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: "REQUEST_FULL_UPDATE" }));
  }
}

/**
 * App seviyesinde TEK kez cagrilir. Baglantiyi kurar ve yasam dongusunu yonetir.
 */
export function useWebSocket() {
  useEffect(() => {
    manualClose = false;
    connect();

    const onVisible = () => {
      if (document.visibilityState === "visible") requestFullUpdate();
    };
    document.addEventListener("visibilitychange", onVisible);

    return () => {
      document.removeEventListener("visibilitychange", onVisible);
      // NOT: singleton'i bilerek kapatmıyoruz; StrictMode cift-mount'ta
      //      baglantiyi kapatip yeniden acmamak icin (Not 4). Tek WS yasar.
    };
  }, []);
}
