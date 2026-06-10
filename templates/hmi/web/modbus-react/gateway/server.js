// ============================================================================
//  server.js — Modbus TCP -> WebSocket gateway
// ============================================================================
//
//  Tarayici dogrudan Modbus TCP (port 502, ham TCP soketi) konusamaz; yalnizca
//  HTTP/WebSocket acabilir. Bu yuzden bu Node.js gateway zorunludur:
//
//      Tarayici  --WebSocket-->  [server.js]  --Modbus TCP-->  PLC/slave
//
//  - PLC'yi periyodik okur (polling; Modbus'ta subscription yoktur).
//  - Yalnizca DEGISEN tag'leri WebSocket ile iter (delta yayini).
//  - Frontend'den gelen WRITE_COIL / WRITE_REGISTER isteklerini PLC'ye iletir.
//  - Baglanti kopunca otomatik yeniden baglanir.
//
//  Referans: knowledge/hmi/web-based/02_modbus_clients_js.md,
//            knowledge/hmi/web-based/05_realtime_websocket.md
// ============================================================================

import net from "node:net";
import { EventEmitter } from "node:events";
import { WebSocketServer, WebSocket } from "ws";
import Modbus from "jsmodbus";
import dotenv from "dotenv";

import {
  TAG_MAP,
  READ_BLOCKS,
  decodeAll,
  isAlarmActive,
} from "./register-map.js";

dotenv.config();

// --- Yapilandirma (.env) ---
const CFG = {
  host: process.env.MODBUS_HOST || "127.0.0.1",
  port: Number(process.env.MODBUS_PORT || 502),
  unitId: Number(process.env.MODBUS_UNIT_ID || 1),
  pollMs: Number(process.env.POLL_INTERVAL_MS || 500),
  timeoutMs: Number(process.env.MODBUS_TIMEOUT_MS || 2000),
  reconnectMs: Number(process.env.RECONNECT_MS || 5000),
  wsPort: Number(process.env.WS_PORT || 8080),
  writeToken: process.env.WRITE_TOKEN || "",
};

// Modbus exception kodu -> okunabilir mesaj (knowledge Hata 3)
const EXCEPTION_MESSAGES = {
  1: "Illegal Function (FC desteklenmiyor)",
  2: "Illegal Data Address (tanimsiz/bosluklu adres)",
  3: "Illegal Data Value (gecersiz deger / blok cok buyuk)",
  4: "Slave Device Failure",
  6: "Slave Device Busy",
};

// ============================================================================
//  ModbusManager — PLC baglantisi, polling, yazma, reconnect
// ============================================================================
class ModbusManager extends EventEmitter {
  constructor(cfg) {
    super();
    this.cfg = cfg;
    this.socket = null;
    this.client = null;
    this.status = "DISCONNECTED"; // DISCONNECTED | CONNECTING | CONNECTED | ERROR
    this.pollTimer = null;
    this.reconnectTimer = null;
    this.isPolling = false; // re-entrancy guard (knowledge Optimizasyon madde 5)
    this.lastValues = {}; // tag -> value (delta yayini icin)
    this.lastGoodPoll = 0; // stale tespiti icin (Modbus'ta quality yok)
  }

  connect() {
    if (this.status === "CONNECTING" || this.status === "CONNECTED") return;
    this._setStatus("CONNECTING");

    // jsmodbus her yeniden baglanmada YENI socket + YENI client ister (Not 6).
    this.socket = new net.Socket();
    this.client = new Modbus.client.TCP(this.socket, this.cfg.unitId, this.cfg.timeoutMs);

    // Cevapsiz istek tum donguyu kilitlemesin (Not 7).
    this.socket.setTimeout(this.cfg.timeoutMs);

    this.socket.on("connect", () => {
      console.log(`[modbus] baglandi -> ${this.cfg.host}:${this.cfg.port} (unit ${this.cfg.unitId})`);
      this._setStatus("CONNECTED");
      this._startPolling();
    });

    this.socket.on("timeout", () => {
      console.warn("[modbus] socket timeout");
      this.socket.destroy(new Error("socket timeout"));
    });

    this.socket.on("error", (err) => {
      console.error(`[modbus] socket error: ${err.message}`);
      this._setStatus("ERROR");
    });

    this.socket.on("close", () => {
      this._stopPolling();
      if (this.status !== "DISCONNECTED") {
        console.log("[modbus] baglanti kapandi, yeniden denenecek");
      }
      this._setStatus("DISCONNECTED");
      this._scheduleReconnect();
    });

    this.socket.connect({ host: this.cfg.host, port: this.cfg.port });
  }

  _startPolling() {
    if (this.pollTimer) return;
    this.pollTimer = setInterval(() => this._poll(), this.cfg.pollMs);
  }

  _stopPolling() {
    if (this.pollTimer) {
      clearInterval(this.pollTimer);
      this.pollTimer = null;
    }
  }

  async _poll() {
    // Onceki poll bitmeden yenisini baslatma (yavas cihaz / re-entrancy).
    if (this.isPolling || this.status !== "CONNECTED") return;
    this.isPolling = true;

    try {
      // Her adres uzayi icin TEK blok oku (bosluksuz; bkz. register-map READ_BLOCKS).
      // NOT: jsmodbus single-master; bazi legacy PLC'ler Promise.all'i karistirir
      //      (Not 1). Guvenli varsayilan: ardisik await.
      // valuesAsArray her zaman duz JS dizisi verir (registerlarda .values Buffer
      //   olabilir; valuesAsArray number[] garantiler). Dizi blok start'tan
      //   0-indeksli baslar; decodeAll (address - block.start) ile indeksler.
      const coils = READ_BLOCKS.COIL
        ? (await this.client.readCoils(READ_BLOCKS.COIL.start, READ_BLOCKS.COIL.count)).response.body.valuesAsArray
        : [];
      const discrete = READ_BLOCKS.DI
        ? (await this.client.readDiscreteInputs(READ_BLOCKS.DI.start, READ_BLOCKS.DI.count)).response.body.valuesAsArray
        : [];
      const input = READ_BLOCKS.IR
        ? Array.from((await this.client.readInputRegisters(READ_BLOCKS.IR.start, READ_BLOCKS.IR.count)).response.body.valuesAsArray)
        : [];
      const holding = READ_BLOCKS.HR
        ? Array.from((await this.client.readHoldingRegisters(READ_BLOCKS.HR.start, READ_BLOCKS.HR.count)).response.body.valuesAsArray)
        : [];

      const decoded = decodeAll({ coils, discrete, input, holding });

      this.lastGoodPoll = Date.now();

      // Delta yayini: yalnizca degisen tag'leri gonder (CPU + bandwidth tasarrufu).
      const ts = Date.now();
      for (const [tag, { value }] of Object.entries(decoded)) {
        if (this.lastValues[tag] !== value) {
          this.lastValues[tag] = value;
          this.emit("tagUpdate", { tag, value, timestamp: ts });
          this._evaluateAlarm(tag, value, ts);
        }
      }
    } catch (err) {
      this._handlePollError(err);
    } finally {
      this.isPolling = false;
    }
  }

  _evaluateAlarm(tag, value, ts) {
    const def = TAG_MAP[tag];
    if (!def?.alarm) return;
    const active = isAlarmActive(def, value);
    this.emit("alarm", {
      tag,
      active,
      priority: def.alarm.priority,
      text: def.alarm.text,
      label: def.label,
      timestamp: ts,
    });
  }

  _handlePollError(err) {
    if (err?.response?.body?.exceptionCode !== undefined) {
      const code = err.response.body.exceptionCode;
      console.error(`[modbus] Exception 0x${code.toString(16)}: ${EXCEPTION_MESSAGES[code] || "bilinmiyor"}`);
      // Exception protokol-seviyesi; baglanti hala canli olabilir, reconnect etme.
    } else {
      console.error(`[modbus] poll error: ${err.message}`);
      // Ag/baglanti hatasi -> socket'i kapat, close handler reconnect eder.
      this._setStatus("ERROR");
      this.socket?.destroy();
    }
  }

  /** Tek coil yaz (FC05). */
  async writeCoil(tag, value) {
    const def = TAG_MAP[tag];
    if (!def || def.type !== "COIL" || !def.writable) {
      return { ok: false, error: `Yazilamaz coil tag: ${tag}` };
    }
    if (this.status !== "CONNECTED") return { ok: false, error: "PLC bagli degil" };
    try {
      await this.client.writeSingleCoil(def.address, !!value);
      return { ok: true };
    } catch (err) {
      return { ok: false, error: err.message };
    }
  }

  /** Tek holding register yaz (FC06). Olcekleme burada yapilir. */
  async writeRegister(tag, value) {
    const def = TAG_MAP[tag];
    if (!def || def.type !== "HR" || !def.writable) {
      return { ok: false, error: `Yazilamaz register tag: ${tag}` };
    }
    if (this.status !== "CONNECTED") return { ok: false, error: "PLC bagli degil" };

    // Aralik kontrolu (sunucu tarafi dogrulama).
    if (def.min !== undefined && value < def.min) return { ok: false, error: `Min ${def.min}` };
    if (def.max !== undefined && value > def.max) return { ok: false, error: `Max ${def.max}` };

    const scaled = def.scale ? Math.round(value * def.scale) : Math.round(value);
    try {
      await this.client.writeSingleRegister(def.address, scaled);
      return { ok: true };
    } catch (err) {
      return { ok: false, error: err.message };
    }
  }

  /** Coklu register yaz (FC16) — ardisik HR tag dizisi icin. */
  async writeMultipleRegisters(startAddress, values) {
    if (this.status !== "CONNECTED") return { ok: false, error: "PLC bagli degil" };
    try {
      await this.client.writeMultipleRegisters(startAddress, values);
      return { ok: true };
    } catch (err) {
      return { ok: false, error: err.message };
    }
  }

  _scheduleReconnect() {
    if (this.reconnectTimer) return;
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      // Eski socket'in listener'larini temizle (sizinti / MaxListeners; Not 6).
      if (this.socket) {
        this.socket.removeAllListeners();
        this.socket.destroy();
        this.socket = null;
      }
      this.connect();
    }, this.cfg.reconnectMs);
  }

  _setStatus(status) {
    if (this.status === status) return;
    this.status = status;
    this.emit("statusChange", status);
  }

  getSnapshot() {
    return {
      status: this.status,
      values: this.lastValues,
      lastGoodPoll: this.lastGoodPoll,
    };
  }
}

// ============================================================================
//  WebSocket sunucu — gateway <-> tarayici
// ============================================================================
class HMIWebSocketServer {
  constructor(port, modbus) {
    this.modbus = modbus;
    this.clients = new Set();
    this.wss = new WebSocketServer({ port, maxPayload: 1_000_000 }); // 1MB (HMI icin yeterli)
    this._setup();
    this._startHeartbeat();
    console.log(`[ws] WebSocket sunucu calisiyor: ws://localhost:${port}`);
  }

  _setup() {
    this.wss.on("connection", (ws, req) => {
      ws.isAlive = true;
      this.clients.add(ws);
      const ip = req.socket.remoteAddress;
      console.log(`[ws] istemci baglandi (${ip}), toplam: ${this.clients.size}`);

      // Yeni istemciye mevcut tum durumu gonder.
      const snap = this.modbus.getSnapshot();
      ws.send(JSON.stringify({ type: "FULL_UPDATE", data: snap.values, status: snap.status }));
      ws.send(JSON.stringify({ type: "TAG_META", meta: this._buildMeta() }));

      ws.on("pong", () => { ws.isAlive = true; });

      ws.on("message", (raw) => this._onMessage(ws, raw));

      ws.on("close", () => {
        this.clients.delete(ws);
        console.log(`[ws] istemci ayrildi, kalan: ${this.clients.size}`);
      });

      ws.on("error", (err) => {
        console.error(`[ws] istemci hatasi: ${err.message}`);
        this.clients.delete(ws);
      });
    });
  }

  // TAG_MAP'in frontend'in ihtiyac duydugu meta'sini cikar (fonksiyonlar haric).
  _buildMeta() {
    const meta = {};
    for (const [tag, def] of Object.entries(TAG_MAP)) {
      meta[tag] = {
        type: def.type,
        kind: def.kind,
        writable: !!def.writable,
        label: def.label,
        unit: def.unit,
        min: def.min,
        max: def.max,
        step: def.step,
        hasAlarm: !!def.alarm,
        alarmPriority: def.alarm?.priority,
      };
    }
    return meta;
  }

  async _onMessage(ws, raw) {
    let msg;
    try {
      msg = JSON.parse(raw.toString());
    } catch {
      console.warn("[ws] gecersiz JSON");
      return;
    }

    switch (msg.type) {
      case "PONG":
        ws.isAlive = true;
        break;

      case "REQUEST_FULL_UPDATE": {
        const snap = this.modbus.getSnapshot();
        ws.send(JSON.stringify({ type: "FULL_UPDATE", data: snap.values, status: snap.status }));
        break;
      }

      case "WRITE_COIL":
      case "WRITE_REGISTER":
        await this._handleWrite(ws, msg);
        break;

      default:
        console.warn(`[ws] bilinmeyen mesaj tipi: ${msg.type}`);
    }
  }

  async _handleWrite(ws, msg) {
    // Modbus'ta auth yoktur; basit token guard (yalnizca izole agda guvenilir).
    if (CFG.writeToken && msg.token !== CFG.writeToken) {
      ws.send(JSON.stringify({ type: "WRITE_ACK", tag: msg.tag, success: false, error: "Yetkisiz" }));
      return;
    }

    const result =
      msg.type === "WRITE_COIL"
        ? await this.modbus.writeCoil(msg.tag, msg.value)
        : await this.modbus.writeRegister(msg.tag, msg.value);

    // Yazma audit log'u (kim ne yazdi — gercek projede dosya/DB'ye).
    console.log(`[write] ${msg.type} ${msg.tag}=${msg.value} -> ${result.ok ? "OK" : "FAIL: " + result.error}`);

    ws.send(JSON.stringify({ type: "WRITE_ACK", tag: msg.tag, success: result.ok, error: result.error }));
  }

  broadcast(obj) {
    const data = JSON.stringify(obj); // tek serilestirme, cok gonderim (Not 7)
    for (const ws of this.clients) {
      if (ws.readyState !== WebSocket.OPEN) continue;
      // Backpressure: yavas istemci tum sunucuyu yavaslatmasin (Not 5).
      if (ws.bufferedAmount > 1_000_000) continue;
      ws.send(data);
    }
  }

  _startHeartbeat() {
    setInterval(() => {
      for (const ws of this.clients) {
        if (!ws.isAlive) {
          ws.terminate();
          this.clients.delete(ws);
          continue;
        }
        ws.isAlive = false;
        ws.ping();
      }
    }, 30000);
  }
}

// ============================================================================
//  Baslat
// ============================================================================
const modbus = new ModbusManager(CFG);
const wsServer = new HMIWebSocketServer(CFG.wsPort, modbus);

modbus.on("tagUpdate", (u) => wsServer.broadcast({ type: "TAG_UPDATE", ...u }));
modbus.on("statusChange", (status) => wsServer.broadcast({ type: "CONNECTION_STATUS", status }));
modbus.on("alarm", (a) => wsServer.broadcast({ type: "ALARM", ...a }));

modbus.connect();

// Temiz kapanis.
process.on("SIGINT", () => {
  console.log("\n[gateway] kapatiliyor...");
  modbus._stopPolling();
  modbus.socket?.destroy();
  wsServer.wss.close();
  process.exit(0);
});
