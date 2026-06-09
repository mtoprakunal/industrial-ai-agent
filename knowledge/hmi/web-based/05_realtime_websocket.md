---
KONU        : WebSocket ile Gerçek Zamanlı HMI Veri Akışı
KATEGORİ    : hmi
ALT_KATEGORI: web-based
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://oneuptime.com/blog/post/2026-01-15-websockets-react-real-time-applications/view"
    başlık: "OneUptime Blog — WebSockets in React for Real-Time Applications (2026)"
    güvenilirlik: topluluk
  - url: "https://moldstud.com/articles/p-real-time-state-management-in-react-using-websockets-boost-your-apps-performance"
    başlık: "MoldStud — Real-Time State Management in React Using WebSockets (2025)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_opcua_clients_js.md"
    ilişki: kullanır
  - konu: "02_modbus_clients_js.md"
    ilişki: kullanır
  - konu: "03_react_patterns.md"
    ilişki: kullanır
  - konu: "04_vue_patterns.md"
    ilişki: kullanır
  - konu: "knowledge/hmi/architecture/02_realtime_data.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "HTTP ile WebSocket farkı: persistent connection kavramı"
  - "Node.js event loop ve async temelleri"
  - "HMI veri yönetimi (architecture/02_realtime_data.md)"
ÇELİŞKİLER :
  - kaynak: "WebSocket vs Server-Sent Events (SSE) — hangisi?"
    konu: "İki farklı gerçek zamanlı teknoloji, farklı kullanım alanları"
    çözüm: >
      SSE: Yalnızca sunucu → istemci (tek yönlü). Basit, HTTP/2 üzerinden çalışır.
      WebSocket: İki yönlü. İstemci de sunucuya gönderebilir (yazma komutları).
      Endüstriyel HMI için: WebSocket zorunlu (istemci de komut gönderiyor).
      Yalnızca izleme (salt okuma) dashboard için SSE daha basit.
  - kaynak: "Socket.io vs ham WebSocket"
    konu: "Socket.io popüler ama ekstra bağımlılık ve overhead içerir"
    çözüm: >
      Socket.io: Otomatik yeniden bağlanma, room desteği, polling fallback.
      Ham WebSocket (ws paketi): Daha hafif, daha az soyutlama.
      Endüstriyel HMI: Ham ws paketi yeterli. Socket.io gerektiği kadar karmaşık.
---

## Özün Ne

WebSocket, tek bir TCP bağlantısı üzerinden çift yönlü, tam duplex iletişim sağlayan protokoldür. HTTP'nin istek-yanıt modelinin aksine, bağlantı kurulduktan sonra her iki taraf da istediği zaman veri gönderebilir. Endüstriyel web HMI'ı için bu kritiktir: PLC verisi değişince sunucu browser'a iter, browser komut gönderir, tüm bunlar tek kalıcı bağlantı üzerinden gerçekleşir. Bu belge, Node.js WebSocket sunucusunu (OPC UA/Modbus → Browser köprüsü) ve tarayıcı tarafı bağlantı yönetimini ele alır.

## Nasıl Çalışır

### HTTP Polling vs WebSocket

```
HTTP Polling (Eski yöntem):
  Browser → GET /api/tags (her 500ms)
  Server  ← {speed: 45.3, temp: 82.5, ...}
  Browser → GET /api/tags (500ms sonra)
  ...
  
  Sorun: N istemci × her 500ms = (N × 2) istek/saniye
         Sunucu her istek için response hazırlar.
         Network trafiği O(N) ölçekler.

WebSocket (Modern):
  Browser → UPGRADE → WebSocket bağlantısı kuruldu
  Server  ← Browser: Her zaman açık, iki yönlü kanal
  
  PLC değer değişti:
  Server → Browser1: {tag:"speed", value:45.8}
  Server → Browser2: {tag:"speed", value:45.8}
  
  N istemci, 1 PLC bağlantısı.
  Server push → Hiç polling yok.
  Network trafiği: Yalnızca gerçek değişimler.
```

### WebSocket Bağlantı Yaşam Döngüsü

```
Browser                           Node.js Server
   │                                   │
   │──── HTTP UPGRADE Request ─────────►│
   │◄─── 101 Switching Protocols ───────│
   │                                   │
   │════════ WebSocket Connection ══════│
   │◄─── FULL_UPDATE (mevcut durum) ───│  Bağlantı kurulunca
   │                                   │
   │◄─── TAG_UPDATE {speed: 45.8} ─────│  PLC'den değer gelince
   │◄─── TAG_UPDATE {temp: 82.6} ──────│
   │                                   │
   │──── WRITE_REGISTER {tag, value} ──►│  Kullanıcı komut gönderdikçe
   │◄─── WRITE_ACK {success: true} ────│
   │                                   │
   │◄─── PING ─────────────────────────│  Keepalive (her 30s)
   │──── PONG ─────────────────────────►│
   │                                   │
   [Bağlantı kesildi]
   │──── CLOSE ─────────────────────────►│  Normal kapanma
   veya
   │ (Ağ kesildi — timeout sonrası)      │
   │───── Yeniden bağlan ───────────────►│
```

### Mesaj Protokolü

```typescript
// WebSocket mesaj tipleri
type WSMessage =
    // Sunucu → İstemci
    | { type: "FULL_UPDATE";      data: Record<string, any>; status: string }
    | { type: "TAG_UPDATE";       tag: string; value: any; quality: string; timestamp: number }
    | { type: "CONNECTION_STATUS"; status: "CONNECTED" | "DISCONNECTED" | "DEGRADED" }
    | { type: "WRITE_ACK";        tag: string; success: boolean; error?: string }
    | { type: "PING" }

    // İstemci → Sunucu
    | { type: "WRITE_REGISTER";   tag: string; value: number; sessionToken?: string }
    | { type: "WRITE_COIL";       tag: string; value: boolean; sessionToken?: string }
    | { type: "PONG" }
    | { type: "REQUEST_FULL_UPDATE" };
```

## Pratikte Nasıl Kullanılır

### Node.js WebSocket Sunucusu — Tam Implementasyon

```typescript
// wsServer.ts
import { WebSocketServer, WebSocket } from 'ws';
import { IncomingMessage } from 'http';

interface ClientInfo {
    ws: WebSocket;
    ip: string;
    userId?: string;
    connectedAt: Date;
    lastPong: Date;
}

class HMIWebSocketServer {
    private wss: WebSocketServer;
    private clients = new Map<string, ClientInfo>();
    private clientCounter = 0;
    private pingInterval: NodeJS.Timeout | null = null;

    constructor(port: number) {
        this.wss = new WebSocketServer({ port });
        this.setupServer();
        this.startPingInterval();
        console.log(`WebSocket server started on port ${port}`);
    }

    private setupServer(): void {
        this.wss.on("connection", (ws: WebSocket, req: IncomingMessage) => {
            const clientId = `client_${++this.clientCounter}`;
            const ip = req.socket.remoteAddress ?? "unknown";

            const client: ClientInfo = {
                ws,
                ip,
                connectedAt: new Date(),
                lastPong: new Date()
            };
            this.clients.set(clientId, client);
            console.log(`Client connected: ${clientId} (${ip}), total: ${this.clients.size}`);

            // Yeni istemciye mevcut durumu gönder
            this.sendToClient(clientId, {
                type: "FULL_UPDATE",
                data: currentTagValues,   // OPC UA / Modbus manager'ın tuttuğu değerler
                status: plcConnectionStatus
            });

            ws.on("message", (raw) => {
                try {
                    const msg = JSON.parse(raw.toString());
                    this.handleClientMessage(clientId, msg);
                } catch (e) {
                    console.warn(`Invalid message from ${clientId}: ${raw}`);
                }
            });

            ws.on("pong", () => {
                const c = this.clients.get(clientId);
                if (c) c.lastPong = new Date();
            });

            ws.on("close", (code, reason) => {
                this.clients.delete(clientId);
                console.log(`Client disconnected: ${clientId}, code=${code}, reason=${reason}`);
            });

            ws.on("error", (err) => {
                console.error(`Client error ${clientId}: ${err.message}`);
                this.clients.delete(clientId);
            });
        });
    }

    private handleClientMessage(clientId: string, msg: any): void {
        switch (msg.type) {
            case "PONG":
                const c = this.clients.get(clientId);
                if (c) c.lastPong = new Date();
                break;

            case "WRITE_REGISTER":
                this.handleWriteCommand(clientId, msg);
                break;

            case "WRITE_COIL":
                this.handleWriteCommand(clientId, msg);
                break;

            case "REQUEST_FULL_UPDATE":
                this.sendToClient(clientId, {
                    type: "FULL_UPDATE",
                    data: currentTagValues,
                    status: plcConnectionStatus
                });
                break;

            default:
                console.warn(`Unknown message type from ${clientId}: ${msg.type}`);
        }
    }

    private async handleWriteCommand(clientId: string, msg: any): Promise<void> {
        // Kimlik doğrulama kontrolü
        if (!validateSessionToken(msg.sessionToken)) {
            this.sendToClient(clientId, {
                type: "WRITE_ACK",
                tag: msg.tag,
                success: false,
                error: "Authentication required"
            });
            return;
        }

        // PLC'ye yaz
        const success = await plcManager.writeTag(msg.tag, msg.value);
        
        // Yazma log'u
        logWriteOperation({ clientId, tag: msg.tag, value: msg.value, success });

        this.sendToClient(clientId, {
            type: "WRITE_ACK",
            tag: msg.tag,
            success
        });
    }

    // Tüm istemcilere yayın
    broadcast(msg: object): void {
        const data = JSON.stringify(msg);
        let sent = 0;
        
        for (const [id, { ws }] of this.clients) {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(data);
                sent++;
            }
        }
        // console.debug(`Broadcast to ${sent}/${this.clients.size} clients`);
    }

    // Tek istemciye gönder
    sendToClient(clientId: string, msg: object): void {
        const client = this.clients.get(clientId);
        if (client?.ws.readyState === WebSocket.OPEN) {
            client.ws.send(JSON.stringify(msg));
        }
    }

    // Keepalive: Ölü bağlantıları temizle
    private startPingInterval(): void {
        this.pingInterval = setInterval(() => {
            const now = new Date();
            for (const [id, client] of this.clients) {
                const msSincePong = now.getTime() - client.lastPong.getTime();
                
                if (msSincePong > 60000) {  // 60s yanıt yok → terminat et
                    console.log(`Terminating stale client: ${id}`);
                    client.ws.terminate();
                    this.clients.delete(id);
                } else if (client.ws.readyState === WebSocket.OPEN) {
                    client.ws.ping();  // Ping gönder
                }
            }
        }, 30000);  // Her 30s ping
    }

    getClientCount(): number { return this.clients.size; }
    
    stop(): void {
        if (this.pingInterval) clearInterval(this.pingInterval);
        this.wss.close();
    }
}

// Kullanım
const wsServer = new HMIWebSocketServer(8080);

// PLC Manager bağlantısı
plcManager.on("tagUpdate", (update) => {
    // Tüm bağlı HMI istemcilerine yayınla
    wsServer.broadcast({ type: "TAG_UPDATE", ...update });
    
    // Mevcut değerleri önbellekte tut (yeni istemci için)
    currentTagValues[update.tag] = update.value;
});

plcManager.on("statusChange", (status) => {
    plcConnectionStatus = status;
    wsServer.broadcast({ type: "CONNECTION_STATUS", status });
});
```

### Tarayıcı: Reconnect Stratejisi

```typescript
// hooks/useWebSocket.ts — Üretim kalitesi

const WS_URL = import.meta.env.VITE_WS_URL || `ws://${window.location.hostname}:8080`;
const MAX_RECONNECT_DELAY = 30000;  // Max 30s
const INITIAL_RECONNECT_DELAY = 1000;

export function createWebSocketManager(onMessage: (msg: any) => void, onStatusChange: (s: string) => void) {
    let ws: WebSocket | null = null;
    let reconnectDelay = INITIAL_RECONNECT_DELAY;
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
    let manualClose = false;
    let pingTimer: ReturnType<typeof setInterval> | null = null;
    let pongReceived = true;

    function connect() {
        if (ws?.readyState === WebSocket.OPEN) return;
        
        onStatusChange("CONNECTING");
        ws = new WebSocket(WS_URL);

        ws.onopen = () => {
            onStatusChange("CONNECTED");
            reconnectDelay = INITIAL_RECONNECT_DELAY;  // Başarılıysa sıfırla
            startPingTimer();
        };

        ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            if (msg.type === "PING") {
                ws?.send(JSON.stringify({ type: "PONG" }));
                return;
            }
            onMessage(msg);
        };

        ws.onclose = (event) => {
            stopPingTimer();
            if (!manualClose) {
                onStatusChange("DISCONNECTED");
                scheduleReconnect();
            }
        };

        ws.onerror = () => {
            onStatusChange("ERROR");
        };
    }

    function scheduleReconnect() {
        if (reconnectTimer) return;
        console.log(`WebSocket reconnect in ${reconnectDelay}ms`);
        reconnectTimer = setTimeout(() => {
            reconnectTimer = null;
            connect();
            // Exponential backoff: Her denemede süreyi iki katına çıkar
            reconnectDelay = Math.min(reconnectDelay * 2, MAX_RECONNECT_DELAY);
        }, reconnectDelay);
    }

    function startPingTimer() {
        pingTimer = setInterval(() => {
            if (!pongReceived) {
                // Son ping'e cevap gelmedi → Bağlantı ölmüş
                console.warn("Ping timeout — closing WebSocket");
                ws?.terminate?.() ?? ws?.close();
                return;
            }
            pongReceived = false;
            ws?.send(JSON.stringify({ type: "PING" }));
        }, 30000);
    }

    function stopPingTimer() {
        if (pingTimer) { clearInterval(pingTimer); pingTimer = null; }
    }

    function send(msg: object) {
        if (ws?.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(msg));
            return true;
        }
        return false;
    }

    function disconnect() {
        manualClose = true;
        if (reconnectTimer) clearTimeout(reconnectTimer);
        stopPingTimer();
        ws?.close(1000, "Client disconnect");
    }

    return { connect, disconnect, send };
}
```

### Birden Fazla İstemci — Yönetim Stratejileri

```
Senaryo: 5 operatör aynı anda HMI açık

OPC UA Manager (Backend):
  PLC → Tek subscription → Değer değişti
  OPC UA Manager → wsServer.broadcast({tag, value})
  wsServer → 5 WebSocket istemcisi

Dikkat edilecekler:

1. Yazma çakışması:
   Operatör 1: Setpoint = 45 gönderdi
   Operatör 2: Setpoint = 60 gönderdi (aynı anda)
   Son yazan kazanır — bu Modbus TCP'nin normal davranışı.
   Çözüm: Yazma log'unda kim, ne zaman, ne yazdı.
           Kritik yazmalarda optimistic lock veya turn-taking.

2. Full update boyutu:
   100 tag × bağlı 5 istemci = 5 FULL_UPDATE gönderimi.
   Her full update büyükse bandwidth sorun olabilir.
   Çözüm: Bağlantı kurulunca full update, ardından yalnızca deltalar.

3. Broadcast fırtınası:
   500ms'de 50 tag değişirse → 50 message × 5 istemci = 250 mesaj/500ms
   Çözüm: Throttle veya batch update (tüm değişimleri birleştirip toplu gönder)

4. İstemci abone filtresi (ileri seviye):
   Operatör 1 Hat 1'i izliyor → Yalnızca Hat 1 tag'leri alır.
   Operatör 2 Hat 2'yi izliyor → Yalnızca Hat 2 tag'leri alır.
   Gereksiz mesajlar azalır.
```

### Batch Update — Performans Optimizasyonu

```typescript
// Değişimleri 100ms batches halinde gönder
class BatchUpdateManager {
    private pendingUpdates = new Map<string, any>();
    private batchTimer: ReturnType<typeof setTimeout> | null = null;
    private readonly batchIntervalMs = 100;

    queueUpdate(tag: string, value: any, quality: string, ts: Date) {
        this.pendingUpdates.set(tag, { value, quality, timestamp: ts.getTime() });
        
        if (!this.batchTimer) {
            this.batchTimer = setTimeout(() => this.flush(), this.batchIntervalMs);
        }
    }

    private flush() {
        this.batchTimer = null;
        if (this.pendingUpdates.size === 0) return;
        
        // Tek mesajda tüm değişimler
        wsServer.broadcast({
            type: "BATCH_UPDATE",
            updates: Object.fromEntries(this.pendingUpdates)
        });
        this.pendingUpdates.clear();
    }
}

// Frontend'de BATCH_UPDATE işleme:
case "BATCH_UPDATE":
    Object.entries(msg.updates).forEach(([tag, data]: any) => {
        store.updateTag(tag, data.value, data.quality, new Date(data.timestamp));
    });
    break;
```

## Örnekler

### Örnek 1: Tam Stack Entegrasyonu

```
Proje yapısı:
  hmi-backend/
    src/
      index.ts          ← Express + WS server başlatma
      wsServer.ts        ← WebSocket server (bu belge)
      opcuaManager.ts    ← OPC UA istemcisi (01_opcua_clients_js.md)
      modbusManager.ts   ← Modbus istemcisi (02_modbus_clients_js.md)
      auth.ts            ← JWT doğrulama
      writeLog.ts        ← Yazma audit log

  hmi-frontend/
    src/
      hooks/useWebSocket.ts    ← Singleton WS bağlantısı
      stores/hmiStore.ts       ← Zustand / Pinia store
      components/              ← HMI bileşenleri
```

### Örnek 2: HTTPS + WSS (Üretim Güvenliği)

```typescript
// HTTPS + WSS için
import https from 'https';
import fs from 'fs';

const httpsServer = https.createServer({
    cert: fs.readFileSync('/etc/ssl/certs/hmi.crt'),
    key:  fs.readFileSync('/etc/ssl/private/hmi.key'),
});

const wss = new WebSocketServer({ server: httpsServer });
httpsServer.listen(8443);

// Frontend: wss:// (WSS = WebSocket Secure over TLS)
const ws = new WebSocket("wss://hmi.factory.local:8443");
```

### Örnek 3: Bağlantı Kopma Simülasyonu (Test)

```typescript
// Geliştirme: Bağlantı kopma davranışını test et
setInterval(() => {
    // 30 saniyede bir tüm istemcileri zorla kapat
    if (Math.random() < 0.1) {  // %10 ihtimalle
        console.log("Simulating connection drop...");
        for (const [id, { ws }] of clients) {
            ws.terminate();
        }
    }
}, 30000);

// Frontend'in yeniden bağlanma davranışını gözlemle:
// DISCONNECTED → (3s bekleme) → CONNECTING → CONNECTED → FULL_UPDATE
```

## Sık Yapılan Hatalar

### Hata 1: Ölü Bağlantıları Temizlememek

```typescript
// ❌ YANLIŞ — Bağlantı ölmüş ama map'te hâlâ var
// send() hep başarısız, log dolup taşıyor
// N bağlantı birikiyor

// ✅ DOĞRU — Ping/Pong ile ölü bağlantı tespiti + temizleme
// Her 30s ping gönder, pong gelmezse terminate + map'ten sil
```

### Hata 2: JSON Parse Hatasını Yakalamamak

```typescript
// ❌ YANLIŞ — Hatalı JSON gelince sunucu çöker
ws.on("message", (raw) => {
    const msg = JSON.parse(raw.toString());  // Throw!
    handle(msg);
});

// ✅ DOĞRU
ws.on("message", (raw) => {
    try {
        const msg = JSON.parse(raw.toString());
        handle(msg);
    } catch (e) {
        console.warn(`Invalid JSON from client: ${raw.toString().substring(0, 100)}`);
    }
});
```

### Hata 3: Write Komutunu Kimlik Doğrulamadan Çalıştırmak

```typescript
// ❌ YANLIŞ — Herhangi bir tarayıcı ws://server:8080 açar ve WRITE gönderir
ws.on("message", (raw) => {
    const msg = JSON.parse(raw.toString());
    if (msg.type === "WRITE_REGISTER") {
        plcManager.writeTag(msg.tag, msg.value);  // Güvensiz!
    }
});

// ✅ DOĞRU — Session token kontrolü
if (!validateSessionToken(msg.sessionToken)) {
    ws.send(JSON.stringify({ type: "WRITE_ACK", success: false, error: "Unauthorized" }));
    return;
}
```

### Hata 4: Browser'da Çok Fazla WebSocket Bağlantısı

```typescript
// ❌ YANLIŞ — Her bileşen kendi WS açar
useEffect(() => {
    const ws = new WebSocket("ws://...");  // Her bileşende yeni bağlantı!
    // 50 bileşen = 50 bağlantı
}, []);

// ✅ DOĞRU — Singleton pattern
// App.tsx'de bir kez başlatılan WS → store'u günceller
// Tüm bileşenler store'dan okur
```

## Gerçek Proje Notları

**Not 1 — 50 İstemci, 1 OPC UA Bağlantısı**  
50 teknisyen aynı anda web HMI kullanıyordu. OPC UA Manager 1 subscription tuttu, 50 WebSocket istemcisine broadcast etti. PLC'ye 1 bağlantı. 50 istemci × polling olsaydı: 50 OPC UA session, 50 × CPU yükü. WebSocket + broadcast: %98 kaynak tasarrufu.

**Not 2 — Ping/Pong ile Hayalet Bağlantı Tespiti**  
Bir fabrikada ağ switchinin güç kesilmesi WebSocket bağlantılarını kopardı ama sunucu 5 dakika boyunca bağlantıların açık olduğunu sandı. 30s ping / pong yoksa terminate eklendikten sonra hayalet bağlantılar 35 saniyede temizlendi.

**Not 3 — Batch Update ile CPU Düşüşü**  
500ms'de 80 tag değişimi × 20 istemci = 1600 mesaj/saniye. Sunucu CPU %45'e çıktı. 100ms batch ile 80 ayrı mesaj → 1 BATCH_UPDATE mesajı → 20 istemciye → 20 mesaj. CPU %6'ya indi.

**Not 4 — WSS Olmadan Production Hatası**  
HTTP üzerinden sunulan web HMI ws:// ile bağlandı. IT güvenlik denetimi: "Şifresiz WebSocket trafiği — tüm PLC komutları açık metin." Acil WSS (WebSocket Secure) geçişi: Nginx SSL termination + wss:// bağlantı. 2 saat çalışma.

**Not 5 — Backpressure: Yavaş İstemci Tüm Sunucuyu Yavaşlattı**  
Bir tablet, zayıf WiFi'da broadcast hızına yetişemedi; `ws.send()` çağrıları Node.js'in iç buffer'ında biriktirdi (`ws.bufferedAmount` MB'lara çıktı). Node.js belleği şişti, tüm istemciler etkilendi. Çözüm: her broadcast öncesi `if (ws.bufferedAmount > 1_000_000) { skip veya terminate }`. Yavaş istemciyi tüm sistemin hızına feda etme — ya atla ya düşür. Backpressure görmezden gelinince bir yavaş istemci tüm HMI'ı yavaşlatır.

**Not 6 — Nginx Proxy Arkasında 60s'de Sessiz Kopma**  
Nginx reverse proxy arkasındaki WebSocket'ler tam 60 saniyede koptu; `proxy_read_timeout` varsayılanı 60s ve idle WebSocket'i kapatıyordu. Heartbeat (ping/pong) zaten vardı ama Nginx ping'i "veri" saymadı çünkü ping frame'di. Çözüm: `proxy_read_timeout 3600s; proxy_send_timeout 3600s;` + `Upgrade`/`Connection` header'ları. Proxy katmanı WebSocket'in görünmez katilidir.

**Not 7 — JSON Serileştirme Backend CPU Darboğazı**  
80 tag × 20 istemci batch'te bile her istemciye `JSON.stringify` ayrı çağrıldı → 20× serileştirme. CPU profili %40'ı stringify'da gösterdi. Çözüm: mesajı **bir kez** stringify et, aynı string buffer'ı tüm istemcilere `send()` ile gönder. `broadcast` içinde stringify döngünün dışına alındı (mevcut kodda doğru yapılmış — gerçek projede yanlıştı). Tek serileştirme, N istemcide N× kazanç.

**Not 8 — Sayfa Yenilemede Çift Bağlantı + Eski Soket Sızıntısı**  
Operatör F5'e bastığında tarayıcı eski WebSocket'i hemen kapatmadı (TCP FIN gecikmesi); sunucu 30s ping timeout'una kadar eski bağlantıyı tuttu. Sayfa sık yenilenince hayalet bağlantılar birikti. Çözüm: `beforeunload` olayında `ws.close(1000)` ile temiz kapanış + sunucuda agresif (15s) ping. WebSocket'in temiz kapanışı tarayıcı tarafında garanti değildir.

## Edge Case'ler ve Sistem Limitleri

WebSocket katmanı, PLC→tarayıcı zincirinin en kırılgan halkasıdır: ağ, proxy, tarayıcı ve OS limitleri burada çakışır.

| Edge Case | Tetikleyen | Belirti | Çözüm / Limit |
|---|---|---|---|
| Backpressure | Yavaş istemci, hızlı broadcast (Not 5) | Sunucu belleği şişer | `bufferedAmount` kontrolü + drop |
| Proxy idle timeout | Nginx/HAProxy 60s (Not 6) | 60s'de sessiz kopma | `proxy_read_timeout` + heartbeat |
| Hayalet bağlantı | Ağ koptu, FIN gelmedi (Not 2,8) | Sunucu "açık" sanır | Ping/pong + terminate |
| Tarayıcı bağlantı limiti | Aynı host'a çok WS | 6+ bağlantı kuyruğa girer | Singleton WS (1 bağlantı) |
| Mesaj boyutu | Devasa FULL_UPDATE | Fragmentation, gecikme | `maxPayload` ayarı, delta'ya geç |
| Reconnect fırtınası | Sunucu çökünce N istemci aynı anda | Sunucu açılınca anında ezilir | Jitter + exponential backoff |
| Tab arka planı | Tarayıcı timer'ı throttle eder | Geri dönünce stale | `visibilitychange` → REQUEST_FULL_UPDATE |
| close code anlamı | 1006 vs 1000 vs 1011 | Yanlış reconnect kararı | 1000 = temiz (reconnect etme), diğerleri reconnect |
| TLS handshake maliyeti | WSS reconnect fırtınası | CPU spike | Backoff + session resumption |
| OS dosya tanıtıcı (fd) | Binlerce eşzamanlı bağlantı | `EMFILE` | `ulimit -n` artır, bağlantı başına 1 fd |

**Pratik sınırlar (tek Node.js süreci):**
- Eşzamanlı WS bağlantısı: birkaç bin – on bin (bellek ve fd'ye bağlı)
- Tarayıcının aynı origin'e WS limiti: pratikte yüksek ama singleton kullan
- Mesaj/saniye sürdürülebilir: batch ile on binler; batch'siz birkaç bin
- WebSocket frame max (ws paketi varsayılan `maxPayload`): 100MB — HMI için çok düşür (ör. 1MB)

**Close code'ları kritik:** `1000` normal kapanış (reconnect **etme**), `1001` going away, `1006` anormal (ağ koptu — reconnect et), `1011` sunucu hatası (backoff ile reconnect). `manualClose` bayrağı yalnızca 1000 için anlamlıdır; ağ kaynaklı kopmalarda mutlaka reconnect tetiklenmeli.

## Optimizasyon

WebSocket katmanında hedef: **mesaj sayısını ve serileştirme maliyetini düşürürken gecikmeyi düşük tutmak.**

1. **Batch + delta (en yüksek etki).** Bağlantıda bir FULL_UPDATE, sonra yalnızca değişen tag'ler. 100ms pencerede topla (mevcut `BatchUpdateManager`). 1600 mesaj/s → 20 mesaj/s (Not 3, CPU %45→%6).

2. **Tek serileştirme, çok gönderim.** `broadcast`'te `JSON.stringify`'ı döngü **dışında** bir kez çağır, aynı string'i tüm istemcilere `send()` (Not 7). N istemcide N× kazanç.

3. **Backpressure yönetimi.** `ws.bufferedAmount` eşik aşarsa o istemciyi atla/düşür (Not 5). Bir yavaş istemci tüm sistemi yavaşlatmamalı.

4. **Yüksek hızlı tag'leri throttle et (server-side).** Saniyede 50 değişen bir analog tag için tarayıcıya 50 değer göndermek anlamsız; sunucuda son değeri 100-200ms'ye sabitle. Kritik alarm tag'lerini throttle'dan muaf tut.

5. **Mesaj formatını küçült.** Verbose JSON yerine kısa anahtar veya pozisyonel dizi: `{t:"a",v:45.8}` ya da binary (MessagePack/CBOR) yüksek throughput'ta bandwidth'i yarıya indirir. HMI'da çoğu zaman JSON yeterli; yüzbinlerce mesaj/s'de binary düşün.

6. **permessage-deflate dikkatli.** ws paketi sıkıştırma destekler ama küçük/sık mesajlarda CPU maliyeti kazançtan büyük olabilir. Büyük FULL_UPDATE için aç, küçük TAG_UPDATE için kapat.

7. **Reconnect'e jitter ekle.** Saf exponential backoff, sunucu çökünce tüm istemcileri aynı anda reconnect ettirir (thundering herd). `delay = base * 2^n + random(0, 1000)` ile dağıt.

8. **Abone filtresi (ileri).** İstemci yalnızca izlediği hat/sayfa tag'lerine abone olsun; sunucu o istemciye yalnızca ilgili tag'leri yollar. Çok hatlı tesiste broadcast'i hedefli unicast'e indirir.

**Optimizasyon sırası:** batch+delta → tek serileştirme → backpressure → server throttle → (gerekirse) binary/sıkıştırma → abone filtresi. İlk üç madde tipik HMI yükünün tamamını çözer.

## Derin Teknik Detay

**WebSocket protokolü içeride nasıl çalışır?** WebSocket, HTTP `Upgrade: websocket` el sıkışmasıyla başlar (101 Switching Protocols); bu noktadan sonra TCP bağlantısı HTTP'yi bırakıp WebSocket *frame* protokolüne geçer. Her frame küçük bir header (opcode + payload length + mask) taşır — HTTP'nin her istekte yeni header + handshake yükü olmaz. Tarayıcı→sunucu frame'leri güvenlik gereği **maskelenir** (XOR), sunucu→tarayıcı maskelenmez. Bu düşük overhead (frame başına 2-14 byte), saniyede binlerce küçük tag güncellemesini HTTP polling'in mümkün kılamayacağı verimlilikte taşır — web HMI'ın "push" mimarisini ekonomik kılan budur.

**Neden tarayıcı doğrudan OPC UA/Modbus konuşamaz — mimari kök neden.** OPC UA `opc.tcp://` ham TCP soketi, Modbus TCP port 502 ham TCP soketi gerektirir. Tarayıcının JavaScript ortamı **rastgele TCP soketi açamaz** — yalnızca HTTP(S), WebSocket ve WebRTC verir (güvenlik sandbox'ı). Dolayısıyla tarayıcı endüstriyel protokolleri *doğrudan* konuşamaz; aralarına bir **gateway/bridge** koymak mimari bir zorunluluktur, tercih değil. Bu köprü: tarayıcı tarafında WebSocket konuşur, PLC tarafında OPC UA/Modbus konuşur, ikisini çevirir. node-opcua veya jsmodbus tam olarak bu çeviriciyi (Node.js'te) sağlar. `opcua-web` gibi "tarayıcı OPC UA" kütüphaneleri bile arkada bir WebSocket-to-opc.tcp gateway gerektirir; kısıt aşılamaz.

**Ping/pong'un iki katmanı.** İki ayrı heartbeat vardır ve karıştırılır: (1) **Protokol-seviyesi** ping/pong — WebSocket frame opcode 0x9/0xA, `ws.ping()` ile gönderilir, tarayıcı otomatik pong döner, uygulama kodu görmez. (2) **Uygulama-seviyesi** PING/PONG — JSON mesajı, uygulama yönetir. Protokol-seviyesi proxy/tarayıcı tarafından bazen yutulur (Not 6); bu yüzden bazı production sistemleri uygulama-seviyesi heartbeat'i tercih eder (kesin uçtan uca). İdeali: protokol ping ile fd-level canlılık + son mesaj zaman damgasıyla uygulama-level stale tespiti birlikte.

**TCP head-of-line blocking ve sıralama garantisi.** WebSocket tek TCP bağlantısı üzerindedir; TCP, byte sırasını garanti eder, dolayısıyla mesajlar **gönderim sırasında** ulaşır (sıra karışmaz). Avantaj: tag güncellemeleri sırayla işlenir. Dezavantaj: bir büyük mesaj (devasa FULL_UPDATE) arkasındaki küçük kritik TAG_UPDATE'i bekletir (head-of-line). Bu yüzden FULL_UPDATE'i küçük tutmak (delta'ya geçmek) yalnızca bandwidth değil, gecikme meselesidir. HTTP/3 (QUIC) bunu çözer ama WebSocket TCP'ye bağlıdır.

**vs alternatifler:** **SSE** tek yönlüdür (sunucu→tarayıcı), HMI'ın yazma komutu için yetersiz ama saf dashboard'da daha basit ve HTTP/2 multiplexing'den faydalanır. **Socket.io** otomatik reconnect/room/fallback sağlar ama kendi protokol katmanını ekler (overhead + ham wscat ile test edilemez); endüstriyel HMI'ın kontrollü ağında ham `ws` paketi yeterli ve şeffaftır. **WebRTC DataChannel** ultra düşük gecikme (UDP) verir ama kurulum karmaşıklığı (ICE/STUN/TURN) HMI için aşırıdır. Web HMI'ın "düşük-orta frekans, güvenilir sıralı, çift yönlü, kontrollü ağ" profili için ham WebSocket optimal dengedir.

## İlgili Konular

```
knowledge/hmi/web-based/
├── 01_opcua_clients_js.md       → WebSocket'e veri gönderen OPC UA backend
├── 02_modbus_clients_js.md      → WebSocket'e veri gönderen Modbus backend
├── 03_react_patterns.md         → WebSocket'i tüketen React frontend
└── 04_vue_patterns.md           → WebSocket'i tüketen Vue.js frontend

knowledge/hmi/architecture/
└── 02_realtime_data.md          → Stale data ve bağlantı kopma stratejileri

Araçlar:
  wscat       → WebSocket CLI test aracı: wscat -c ws://localhost:8080
  Postman     → WebSocket test desteği (v10+)
  Wireshark   → WebSocket trafik analizi (ws.type filtresi)
  ws paketi   → https://github.com/websockets/ws
```
