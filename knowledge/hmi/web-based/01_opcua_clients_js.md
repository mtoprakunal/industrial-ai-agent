---
KONU        : JavaScript ile OPC-UA İstemci Geliştirme
KATEGORİ    : hmi
ALT_KATEGORI: web-based
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://node-opcua.github.io/"
    başlık: "NodeOPCUA — Official Site and API Documentation"
    güvenilirlik: resmi
  - url: "https://github.com/node-opcua/node-opcua"
    başlık: "GitHub — node-opcua/node-opcua"
    güvenilirlik: resmi
  - url: "https://www.npmjs.com/package/node-opcua"
    başlık: "npm — node-opcua Package"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "05_realtime_websocket.md"
    ilişki: tamamlar
  - konu: "03_react_patterns.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/opc-ua/04_subscriptions.md"
    ilişki: gerektirir
  - konu: "knowledge/protocols/opc-ua/06_client_implementations.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "OPC UA subscription kavramı (protocols/opc-ua/04_subscriptions.md)"
  - "Node.js ve async/await temelleri"
  - "TypeScript temel bilgisi (opsiyonel ama önerilir)"
ÇELİŞKİLER :
  - kaynak: "node-opcua güvenli bağlantı ve sertifika yönetimi"
    konu: "İlk kurulumda sertifika yönetimi zaman alıcı"
    çözüm: >
      node-opcua, OPCUACertificateManager sınıfı ile sertifika yaşam döngüsünü
      otomatik yönetir. Geliştirme ortamında self-signed sertifika otomatik
      oluşturulur. Production'da: Kendi sertifikanı ver ya da let the library
      create and manage it. Kritik: Sunucu sertifikasını trusted store'a ekle.
      İlk bağlantıda "certificate not trusted" hatası normaldir —
      trust workflow bir kez yapılır, sonra otomatik.
---

## Özün Ne

Node.js üzerinde çalışan `node-opcua`, en kapsamlı ve yaygın kullanılan JavaScript/TypeScript OPC UA kütüphanesidir. Web tabanlı HMI arka planı (backend) olarak kullanıldığında PLC'ye bağlanır, değerleri okur, subscription kurar ve bu verileri WebSocket aracılığıyla tarayıcıya iletir. Production kalitesinde bir OPC UA istemcisi, yalnızca bağlantı ve okuma değil; otomatik yeniden bağlanma, subscription yeniden kurma, sertifika yönetimi ve bağlantı durumu izleme de gerektirir.

## Nasıl Çalışır

### Kurulum

```bash
npm install node-opcua
# TypeScript için tip tanımları dahil
npm install --save-dev @types/node-opcua  # opsiyonel — paket kendi tiplerini içerir

# Güvenli bağlantı için ek paket
npm install node-opcua-crypto
```

### OPC UA Bağlantı Katmanı — Temel Kavramlar

```
OPCUAClient → createSession → browseNodes → readValues → createSubscription
                              ↑
                     Session her zaman aktif kalmalı.
                     Session timeout'u aşılırsa yeniden oluşturulmalı.
```

### Basit Bağlantı ve Okuma

```typescript
import {
    OPCUAClient,
    MessageSecurityMode,
    SecurityPolicy,
    AttributeIds,
    ClientSession,
    ClientSubscription,
    TimestampsToReturn,
    MonitoringParametersOptions,
    ClientMonitoredItem
} from 'node-opcua';

const endpointUrl = "opc.tcp://192.168.1.100:4840";

async function basicRead() {
    const client = OPCUAClient.create({
        applicationName: "WebHMI",
        connectionStrategy: {
            initialDelay: 1000,
            maxRetry: 5
        },
        securityMode: MessageSecurityMode.None,
        securityPolicy: SecurityPolicy.None,
        endpointMustExist: false
    });

    await client.connect(endpointUrl);
    const session = await client.createSession();

    // Namespace index — URI'dan dinamik al (taşınabilir!)
    const nsUri = "http://www.3s-software.com/schemas/Codesys-V3";
    const nsIdx = await session.getNamespaceIndex(nsUri);

    // Tek değer oku
    const motorNode = session.getNode(
        `ns=${nsIdx};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun`
    );
    const dv = await motorNode.readAttribute(AttributeIds.Value);
    console.log(`Motor: ${dv.value.value}, status: ${dv.statusCode.toString()}`);

    // Toplu okuma — verimli
    const nodesToRead = [
        { nodeId: `ns=${nsIdx};s=|var|CODESYS Control.Application.GVL_IO.rTemperature`, attributeId: AttributeIds.Value },
        { nodeId: `ns=${nsIdx};s=|var|CODESYS Control.Application.GVL_IO.rSpeed`, attributeId: AttributeIds.Value }
    ];
    const results = await session.read(nodesToRead);
    console.log(`Temp: ${results[0].value.value}, Speed: ${results[1].value.value}`);

    await session.close();
    await client.disconnect();
}

basicRead().catch(console.error);
```

### Değer Yazma

```typescript
async function writeValues(session: ClientSession, nsIdx: number) {
    // Tek değer yaz
    const statusCode = await session.writeSingleNode(
        `ns=${nsIdx};s=|var|CODESYS Control.Application.GVL_Params.rSpeedSetpoint`,
        { dataType: "Double", value: 65.0 }
    );
    console.log(`Write status: ${statusCode.toString()}`);

    // Çoklu yazma
    const nodesToWrite = [
        {
            nodeId: `ns=${nsIdx};s=|var|CODESYS Control.Application.GVL_Params.rSpeedSP`,
            attributeId: AttributeIds.Value,
            value: { dataType: "Double", value: 65.0 }
        },
        {
            nodeId: `ns=${nsIdx};s=|var|CODESYS Control.Application.GVL_HMI.xStartCmd`,
            attributeId: AttributeIds.Value,
            value: { dataType: "Boolean", value: true }
        }
    ];
    const writeResults = await session.write(nodesToWrite);
    writeResults.forEach((sc, i) => console.log(`Write ${i}: ${sc.toString()}`));
}
```

### Subscription — Production-Ready Implementasyon

```typescript
async function setupSubscription(session: ClientSession, nsIdx: number, onData: Function) {
    // Subscription oluştur
    const subscription = await session.createSubscription2({
        requestedPublishingInterval: 500,        // 500ms publishing
        requestedMaxKeepAliveCount: 20,
        requestedLifetimeCount: 120,
        maxNotificationsPerPublish: 1000,
        publishingEnabled: true,
        priority: 128
    });

    subscription.on("started", () => console.log(`Subscription started: ${subscription.subscriptionId}`));
    subscription.on("terminated", () => console.log("Subscription terminated"));
    subscription.on("status_changed", (status) => console.log(`Subscription status: ${status}`));

    // MonitoredItem'ları ekle — farklı sampling hızlarıyla
    const alarmNodeId = `ns=${nsIdx};s=|var|CODESYS Control.Application.GVL_Alarms.xMotorFault`;
    const tempNodeId  = `ns=${nsIdx};s=|var|CODESYS Control.Application.GVL_IO.rTemperature`;
    const speedNodeId = `ns=${nsIdx};s=|var|CODESYS Control.Application.GVL_IO.rActualSpeed`;

    // Alarm — hızlı sampling
    const alarmItem = await subscription.monitor(
        { nodeId: alarmNodeId, attributeId: AttributeIds.Value },
        { samplingInterval: 100, discardOldest: true, queueSize: 10 },
        TimestampsToReturn.Source
    );
    alarmItem.on("changed", (dv) => {
        onData({ tag: "motor_fault", value: dv.value.value, quality: getQuality(dv), ts: dv.sourceTimestamp });
    });

    // Normal telemetri — 500ms sampling
    for (const [tag, nodeId] of [["temperature", tempNodeId], ["speed", speedNodeId]]) {
        const item = await subscription.monitor(
            { nodeId, attributeId: AttributeIds.Value },
            { samplingInterval: 500, discardOldest: true, queueSize: 5 },
            TimestampsToReturn.Source
        );
        item.on("changed", (dv) => {
            onData({ tag, value: dv.value.value, quality: getQuality(dv), ts: dv.sourceTimestamp });
        });
    }

    return subscription;
}

function getQuality(dataValue: any): "GOOD" | "BAD" | "UNCERTAIN" {
    if (dataValue.statusCode.isGood()) return "GOOD";
    if (dataValue.statusCode.isBad()) return "BAD";
    return "UNCERTAIN";
}
```

### Production-Ready OPC UA Manager

```typescript
import { EventEmitter } from 'events';

type ConnectionStatus = "DISCONNECTED" | "CONNECTING" | "CONNECTED" | "ERROR";

interface TagUpdate {
    tag: string;
    value: any;
    quality: "GOOD" | "BAD" | "UNCERTAIN";
    timestamp: Date;
}

class OPCUAManager extends EventEmitter {
    private client: OPCUAClient | null = null;
    private session: ClientSession | null = null;
    private subscription: ClientSubscription | null = null;
    private status: ConnectionStatus = "DISCONNECTED";
    private reconnectTimer: NodeJS.Timeout | null = null;
    private nsIdx: number = 4;  // Dinamik alınacak
    
    constructor(
        private readonly endpointUrl: string,
        private readonly reconnectDelay = 5000
    ) {
        super();
    }

    async connect(): Promise<void> {
        if (this.status === "CONNECTING" || this.status === "CONNECTED") return;
        
        this.setStatus("CONNECTING");
        
        try {
            this.client = OPCUAClient.create({
                applicationName: "WebHMI_Backend",
                connectionStrategy: {
                    initialDelay: 1000,
                    maxRetry: 3,
                    maxDelay: 10000
                },
                securityMode: MessageSecurityMode.SignAndEncrypt,
                securityPolicy: SecurityPolicy.Basic256Sha256,
                endpointMustExist: false
            });

            // Bağlantı kopma olayını dinle
            this.client.on("connection_lost", () => {
                console.error("OPC UA connection lost");
                this.setStatus("DISCONNECTED");
                this.scheduleReconnect();
            });

            this.client.on("connection_reestablished", () => {
                console.log("OPC UA connection reestablished");
            });

            await this.client.connect(this.endpointUrl);

            this.session = await this.client.createSession({
                userName: process.env.OPC_UA_USER || "",
                password: process.env.OPC_UA_PASS || ""
            });

            // Session keepalive
            this.session.on("session_closed", () => {
                console.warn("Session closed unexpectedly");
                this.setStatus("DISCONNECTED");
                this.scheduleReconnect();
            });

            // Namespace index dinamik al
            const nsUri = "http://www.3s-software.com/schemas/Codesys-V3";
            this.nsIdx = await this.session.getNamespaceIndex(nsUri);
            
            await this.setupSubscription();
            
            this.setStatus("CONNECTED");
            console.log(`Connected to ${this.endpointUrl} (ns=${this.nsIdx})`);

        } catch (err) {
            console.error(`OPC UA connect error: ${err}`);
            this.setStatus("ERROR");
            this.scheduleReconnect();
        }
    }

    private async setupSubscription(): Promise<void> {
        if (!this.session) return;

        this.subscription = await this.session.createSubscription2({
            requestedPublishingInterval: 500,
            requestedMaxKeepAliveCount: 20,
            requestedLifetimeCount: 120,
            maxNotificationsPerPublish: 1000,
            publishingEnabled: true,
            priority: 128
        });

        this.subscription.on("terminated", () => {
            console.warn("Subscription terminated — will reconnect");
            this.setStatus("DISCONNECTED");
            this.scheduleReconnect();
        });

        // İzlenecek node'ları tanımla
        const tagsToMonitor = [
            { tag: "motor_fault",   nodeId: `ns=${this.nsIdx};s=|var|CODESYS Control.Application.GVL_Alarms.xMotorFault`,   sampling: 100 },
            { tag: "temperature",   nodeId: `ns=${this.nsIdx};s=|var|CODESYS Control.Application.GVL_IO.rTemperature`,       sampling: 500 },
            { tag: "actual_speed",  nodeId: `ns=${this.nsIdx};s=|var|CODESYS Control.Application.GVL_IO.rActualSpeed`,       sampling: 500 },
            { tag: "production_count", nodeId: `ns=${this.nsIdx};s=|var|CODESYS Control.Application.GVL_IO.dwProdCount`,    sampling: 5000 },
        ];

        for (const { tag, nodeId, sampling } of tagsToMonitor) {
            const item = await this.subscription.monitor(
                { nodeId, attributeId: AttributeIds.Value },
                { samplingInterval: sampling, discardOldest: true, queueSize: 10 },
                TimestampsToReturn.Source
            );
            item.on("changed", (dv) => {
                const update: TagUpdate = {
                    tag,
                    value: dv.value.value,
                    quality: getQuality(dv),
                    timestamp: dv.sourceTimestamp || new Date()
                };
                this.emit("tagUpdate", update);
            });
        }
    }

    async writeTag(tag: string, value: any): Promise<boolean> {
        if (!this.session || this.status !== "CONNECTED") {
            console.error("Cannot write: not connected");
            return false;
        }
        
        // Tag name'i NodeId'ye çevir (burada basitleştirilmiş map)
        const nodeId = this.getNodeId(tag);
        if (!nodeId) return false;

        const statusCode = await this.session.writeSingleNode(nodeId, { value });
        const success = statusCode.isGood();
        if (!success) console.error(`Write failed for ${tag}: ${statusCode.toString()}`);
        return success;
    }

    private getNodeId(tag: string): string | null {
        const TAG_MAP: Record<string, string> = {
            "speed_setpoint": `ns=${this.nsIdx};s=|var|CODESYS Control.Application.GVL_Params.rSpeedSP`,
            "start_cmd":      `ns=${this.nsIdx};s=|var|CODESYS Control.Application.GVL_HMI.xStartCmd`,
            "stop_cmd":       `ns=${this.nsIdx};s=|var|CODESYS Control.Application.GVL_HMI.xStopCmd`,
        };
        return TAG_MAP[tag] ?? null;
    }

    private scheduleReconnect(): void {
        if (this.reconnectTimer) return;
        console.log(`Reconnecting in ${this.reconnectDelay}ms...`);
        this.reconnectTimer = setTimeout(async () => {
            this.reconnectTimer = null;
            await this.disconnect();
            await this.connect();
        }, this.reconnectDelay);
    }

    private setStatus(status: ConnectionStatus): void {
        this.status = status;
        this.emit("statusChange", status);
    }

    async disconnect(): Promise<void> {
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
            this.reconnectTimer = null;
        }
        if (this.subscription) {
            await this.subscription.terminate();
            this.subscription = null;
        }
        if (this.session) {
            await this.session.close();
            this.session = null;
        }
        if (this.client) {
            await this.client.disconnect();
            this.client = null;
        }
        this.setStatus("DISCONNECTED");
    }

    getStatus(): ConnectionStatus { return this.status; }
}

// Kullanım:
const opcManager = new OPCUAManager("opc.tcp://192.168.1.100:4840");
opcManager.on("tagUpdate", (update: TagUpdate) => {
    // WebSocket broadcast — 05_realtime_websocket.md
    wsServer.broadcast(JSON.stringify({ type: "TAG_UPDATE", ...update }));
});
opcManager.on("statusChange", (status: ConnectionStatus) => {
    wsServer.broadcast(JSON.stringify({ type: "CONNECTION_STATUS", status }));
});
await opcManager.connect();
```

### Güvenli Bağlantı (SignAndEncrypt)

```typescript
import { OPCUACertificateManager } from 'node-opcua';
import path from 'path';

async function createSecureClient() {
    // Sertifika yöneticisi — sertifikaları saklar ve yönetir
    const certManager = new OPCUACertificateManager({
        rootFolder: path.join(process.cwd(), "pki"),
        automaticallyAcceptUnknownCertificate: false,  // Üretimde false!
    });
    await certManager.initialize();

    const client = OPCUAClient.create({
        applicationName: "WebHMI_Secure",
        applicationUri: "urn:WebHMI:Client",
        securityMode: MessageSecurityMode.SignAndEncrypt,
        securityPolicy: SecurityPolicy.Basic256Sha256,
        certificateFile: path.join(process.cwd(), "pki/own/certs/client_cert.pem"),
        privateKeyFile: path.join(process.cwd(), "pki/own/private/private_key.pem"),
        serverCertificate: Buffer.from(
            // Sunucu sertifikasını trusted store'dan yükle
            require('fs').readFileSync(path.join(process.cwd(), "pki/trusted/certs/server.pem"))
        ),
        certificateManager: certManager,
        endpointMustExist: false
    });

    return client;
}
```

### Adres Uzayı Gezinme

```typescript
async function browseAddressSpace(session: ClientSession, nsIdx: number) {
    // Tüm uygulama node'larını listele
    const appNode = session.getNode(`ns=${nsIdx};s=|var|CODESYS Control.Application`);

    const browseResult = await session.browse({
        nodeId: appNode.nodeId,
        referenceTypeId: "HierarchicalReferences",
        includeSubtypes: true,
        browseDirection: "Forward",
        resultMask: 63
    });

    browseResult.references?.forEach(ref => {
        console.log(`  ${ref.browseName.name} [${ref.nodeClass}] ${ref.nodeId}`);
    });
}
```

## Örnekler

### Örnek 1: Express + OPCUAManager Entegrasyonu

```typescript
// server.ts — Express API + OPC UA arka planı
import express from 'express';
import { WebSocketServer } from 'ws';

const app = express();
const wss = new WebSocketServer({ port: 8080 });

const opcManager = new OPCUAManager("opc.tcp://192.168.1.100:4840");

// WebSocket istemci kümesi
const wsClients = new Set<WebSocket>();
wss.on("connection", (ws) => {
    wsClients.add(ws);
    // Yeni bağlanan istemciye mevcut durumu gönder
    ws.send(JSON.stringify({ type: "CONNECTION_STATUS", status: opcManager.getStatus() }));
    ws.on("close", () => wsClients.delete(ws));
});

function broadcast(msg: object) {
    const data = JSON.stringify(msg);
    wsClients.forEach(ws => { if (ws.readyState === 1) ws.send(data); });
}

// OPC UA → WebSocket bağlantısı
opcManager.on("tagUpdate", (u) => broadcast({ type: "TAG_UPDATE", ...u }));
opcManager.on("statusChange", (s) => broadcast({ type: "CONNECTION_STATUS", status: s }));

// REST API: Yazma endpoint'leri
app.post("/api/write/:tag", express.json(), async (req, res) => {
    const { value } = req.body;
    const success = await opcManager.writeTag(req.params.tag, value);
    res.json({ success });
});

app.listen(3001);
opcManager.connect();
```

### Örnek 2: Node okuma kalitesi kontrolü

```typescript
// OPC UA Status Code'larını anlamlandır
function describeDataValue(dv: any) {
    const quality = dv.statusCode.isGood() ? "GOOD"
                  : dv.statusCode.isBad() ? "BAD"
                  : "UNCERTAIN";
    
    if (quality === "BAD") {
        console.warn(`Bad quality for node: ${dv.statusCode.toString()}`);
        // Olası nedenler:
        // Bad_NodeIdUnknown: NodeId bulunamadı — namespace veya path yanlış
        // Bad_NotReadable: Okuma yetkisi yok
        // Bad_OutOfService: Cihaz bakımda
    }
    
    return {
        value: quality === "GOOD" ? dv.value.value : null,
        quality,
        sourceTimestamp: dv.sourceTimestamp,
        serverTimestamp: dv.serverTimestamp
    };
}
```

## Sık Yapılan Hatalar

### Hata 1: Session'ı Kontrol Etmeden Yazma

```typescript
// ❌ YANLIŞ — Session null olabilir
await session.writeSingleNode(nodeId, value);

// ✅ DOĞRU
if (!session || opcManager.getStatus() !== "CONNECTED") {
    throw new Error("OPC UA not connected");
}
await session.writeSingleNode(nodeId, value);
```

### Hata 2: Namespace Index'i Hardcode Etmek

```typescript
// ❌ YANLIŞ — Farklı sunucu/versiyonda ns=4 olmayabilir
const nodeId = "ns=4;s=|var|CODESYS.App.GVL.xMotorRun";

// ✅ DOĞRU — Session başlangıcında URI'dan dinamik al
const nsIdx = await session.getNamespaceIndex("http://www.3s-software.com/...");
const nodeId = `ns=${nsIdx};s=|var|CODESYS.App.GVL.xMotorRun`;
```

### Hata 3: Subscription Sonlandırmayı Unutmak

```typescript
// Uygulama kapanırken temizlik
process.on("SIGINT", async () => {
    await opcManager.disconnect();  // Subscription + Session + Client hepsini kapatır
    process.exit(0);
});
```

### Hata 4: Çok Fazla MonitoredItem Tek Subscription'da

```
Sorun: 500 MonitoredItem tek subscription'da → Sunucu limiti aşılabilir.
Çözüm: Birden fazla subscription (hızlı/orta/yavaş katmanlar).
        Veya sunucunun MaxMonitoredItems konfigürasyonunu artır.
```

## Gerçek Proje Notları

**Not 1 — connection_lost Olayı ile Sessiz Bağlantı Kopması**  
OPC UA bağlantısı NAT timeout'u nedeniyle sessizce koptu. `connection_lost` olayı ateşlendi ama subscription events gelmeye devam etti (stale data). Çözüm: `connection_lost` olayında hem status'u DISCONNECTED yap hem de WebSocket istemcilerine bildir. Subscription'ı yeniden kur — session kapatılıp yeniden açılmalı.

**Not 2 — Namespace Index Sürprizi**  
Farklı CODESYS runtime versiyonları farklı namespace index atayabilir. Hardcoded `ns=4` bazı PLC'lerde `ns=3` veya `ns=5` olarak geldi. `session.getNamespaceIndex(uri)` çağrısı zorunlu hale getirildi.

**Not 3 — Session Timeout'unu Doğru Ayarlamak**  
CODESYS varsayılan session timeout 30 saniye. WebSocket aracılığıyla bağlanan bir HMI'ın arka planı bu timeout'tan etkilenebilir. `requestedSessionTimeout: 3600000` (1 saat) ile session bakımı için yeterli süre tanındı.

**Not 4 — RevisedPublishingInterval ≠ Requested**  
`requestedPublishingInterval: 500` ile subscription kuruldu ama sunucu `revisedPublishingInterval: 1000` döndürdü; sunucunun min PublishingInterval limiti 1000ms idi. Frontend "veri geç geliyor" diye şikayet etti. Çözüm: subscription kurulduktan sonra `subscription.publishingInterval` (revised değer) loglanmaya başlandı. Sunucunun revize ettiği değerler (publishingInterval, maxKeepAliveCount, lifetimeCount) requested değerden farklı olabilir — her zaman revised değeri esas al.

**Not 5 — Bağlantı Yeniden Kurulunca MonitoredItem'lar Kayboldu**  
node-opcua `connection_reestablished` olayında session otomatik yeniden kuruluyordu ama bazı CODESYS sürümlerinde sunucu eski subscription'ı düşürdü; `item.on("changed")` bir daha hiç ateşlenmedi (sessiz başarısızlık). Çözüm: `subscription.on("terminated")` ve `keepalive` sayacı izlendi; belirli süre keepalive gelmezse subscription manuel `recreateSubscriptionAndMonitoredItem()` ile yeniden kuruldu. node-opcua 2.x'te `subscription.recreateSubscriptionAndMonitoredItem()` mevcut; eski sürümlerde manuel re-monitor gerekiyordu.

**Not 6 — DataType Mismatch ile Sessiz Write Reddi**  
`writeSingleNode(nodeId, { dataType: "Double", value: 65 })` çağrısı `Bad_TypeMismatch` döndürdü çünkü PLC değişkeni `REAL` (Float, 32-bit) idi, Double değil. node-opcua otomatik dönüşüm yapmaz. Çözüm: yazma öncesi node'un `DataType` attribute'u bir kez okunup cache'lendi (`Float` → `dataType: "Float"`). LREAL ise Double, REAL ise Float kullan — karıştırma `Bad_TypeMismatch` üretir.

**Not 7 — Çok Hızlı samplingInterval ile Sunucu Reddi**  
Bir tag için `samplingInterval: 10` (10ms) istendi; sunucu `revisedSamplingInterval: 250` döndürdü (sunucunun donanım okuma çevrimi 250ms). 10ms beklentisiyle yazılan throttle mantığı boşa çıktı. Kural: samplingInterval, PLC'nin fiziksel I/O okuma çevriminden (task interval) daha hızlı olamaz; revised değeri kontrol et, donanımın altına inme.

## Edge Case'ler ve Sistem Limitleri

Web HMI backend'i olarak node-opcua kullanırken karşılaşılan sınırlar genelde **sunucu (PLC) tarafı limitlerinden** kaynaklanır; istemci kütüphanesi nadiren darboğazdır.

| Edge Case | Tetikleyen | Belirti | Çözüm / Limit |
|---|---|---|---|
| MaxMonitoredItems aşımı | Tek subscription'a yüzlerce item | `monitor()` `Bad_TooManyMonitoredItems` | Sunucu config'i artır veya çok subscription'a böl (hızlı/orta/yavaş) |
| MaxSubscriptions aşımı | Her tag'e ayrı subscription | `createSubscription2` reddedilir | Tag'leri sampling hızına göre 2-3 subscription'da grupla |
| RevisedPublishingInterval | Sunucu min limiti | Veri beklenenden yavaş | Revised değeri esas al (Not 4) |
| Session timeout | Düşük `requestedSessionTimeout` + idle | `Bad_SessionIdInvalid` | 1 saat veya keepalive ile canlı tut |
| SecureChannel timeout | NAT/firewall idle drop | Sessiz kopma, stale data | `connection_lost` dinle + keepalive (Not 1) |
| Bad_TypeMismatch | REAL vs LREAL, Int vs UInt | Write sessizce reddedilir | DataType'ı oku ve cache'le (Not 6) |
| maxNotificationsPerPublish | Tek publish'te çok değişim | Notifikasyonlar parçalanır, gecikme | Değeri yükselt; veya değişim hızını azalt |
| BrowseNext / continuationPoint | Büyük adres uzayı browse | İlk browse kısmi sonuç döner | `continuationPoint` ile `browseNext` döngüsü kur |
| Array/struct değer | ExtensionObject decode | `dv.value.value` ham buffer | DataTypeManager ile decode; bilinmeyen tip için `readNamespaceArray` |
| Deadband filtresi yok | Analog tag sürekli minik değişim | Gereksiz `changed` event sağanağı | `DataChangeFilter` + `deadbandValue` ile mutlak/yüzde deadband |

**Pratik sayısal sınırlar (CODESYS Control SoftPLC tipik):**
- Eşzamanlı session: genelde 5–10 (config'e bağlı)
- Subscription/session: ~10
- MonitoredItem/server: birkaç bin (donanıma göre)
- Min publishing interval: 50–1000ms (runtime ayarı)
- Min sampling interval: PLC task interval'i (ör. 10–250ms)

Önemli: bu limitler **PLC sunucusunun** limitleridir, node-opcua'nın değil. Yeni bir PLC'ye bağlanırken `GetEndpoints` ve sunucu diagnostics node'ları (`Server.ServerCapabilities`) üzerinden bu değerler okunmalı, varsayım yapılmamalıdır.

## Optimizasyon

Endüstriyel web HMI backend'inde optimizasyon önceliği **PLC'ye binen yükü azaltmak**tır; Node.js CPU'su nadiren darboğazdır.

1. **Subscription kullan, polling değil.** OPC UA'nın en büyük kazancı budur: değer değişince sunucu sana iter. `session.read()` döngüsü kurmak, OPC UA'yı Modbus gibi kullanmaktır — anti-pattern.

2. **samplingInterval'i tag sınıfına göre katmanla.** Hepsini 100ms yapmak sunucuyu boğar. Alarm 100ms, analog 500ms, sayaç/yavaş 5000ms. Düşük öncelikli tag'leri ayrı, düşük öncelikli subscription'a koy.

3. **Deadband uygula (analog değerler için).** Gürültülü bir sıcaklık sensörü 500ms'de ±0.1°C oynuyorsa her örnekte `changed` ateşler. `DataChangeFilter` ile `deadbandType: Absolute, deadbandValue: 0.5` → yalnızca anlamlı değişim WebSocket'e gider.

   ```typescript
   import { DataChangeFilter, DataChangeTrigger, DeadbandType } from 'node-opcua';
   const item = await subscription.monitor(
       { nodeId, attributeId: AttributeIds.Value },
       {
           samplingInterval: 500, queueSize: 5, discardOldest: true,
           filter: new DataChangeFilter({
               trigger: DataChangeTrigger.StatusValue,
               deadbandType: DeadbandType.Absolute,
               deadbandValue: 0.5
           })
       },
       TimestampsToReturn.Source
   );
   ```

4. **queueSize'ı doğru ayarla.** `queueSize: 1` hızlı değişen tag'lerde ara değerleri düşürür (yalnızca son değer önemliyse iyi). Trend/audit için `queueSize: 10+` + `discardOldest: true`.

5. **maxNotificationsPerPublish + publishingInterval dengesi.** Çok tag varsa publishingInterval'i düşürmek yerine maxNotificationsPerPublish'i yükselt — daha az ama daha dolu publish mesajı, daha az TCP overhead.

6. **NodeId'leri önceden resolve et.** Her okumada string NodeId parse edilir. Sık erişilen node'lar için `session.getNode()` ile `ClientNode` cache'le; tekrar parse maliyeti ortadan kalkar.

7. **Backend'de delta filtreleme + WebSocket batch.** OPC UA zaten delta gönderir ama bunu WebSocket'e iletmeden önce `BatchUpdateManager` ile 100ms'lik pencerede topla (bkz. `05_realtime_websocket.md`). Tek tag'in 100ms'de 3 kez değişmesi → tarayıcıya 1 değer.

## Derin Teknik Detay

**Subscription/MonitoredItem mimarisi neden böyle tasarlandı?** OPC UA'nın push modeli aslında saf push değildir; içeride sunucu tarafında **sampling** + istemci tarafından tetiklenen **publish** mekanizması vardır. Sunucu, MonitoredItem'ı `samplingInterval` ile yoklar (donanımdan okur), değişimleri bir **Notification kuyruğuna** (queueSize) biriktirir. İstemci ise arka planda sürekli `Publish` request gönderir; sunucu bu request'lere biriken notifikasyonlarla yanıt verir. node-opcua bu Publish döngüsünü senin yerine yönetir — `subscription.monitor()` çağrısı bu makinenin sadece görünen yüzüdür.

Bu tasarımın nedeni **firewall/NAT dostu olmak**: sunucu istemciye kendiliğinden bağlantı açamaz (klasik push'un sorunu). Bunun yerine istemci açık tuttuğu kanaldan periyodik Publish gönderir, sunucu "ters yönde" yanıtla veri iter. Yani gerçekte istemci-başlatmalı bir "long-poll" üzerine kurulu pseudo-push'tur. Bu yüzden `maxKeepAliveCount` kritik: değişim yoksa bile sunucu, `publishingInterval × maxKeepAliveCount` süresinde bir boş KeepAlive yanıtı yollar; gelmezse istemci bağlantının öldüğünü anlar.

**`lifetimeCount` neden `maxKeepAliveCount`'tan çok büyük olmalı?** Sunucu, `publishingInterval × lifetimeCount` boyunca istemciden hiç Publish request almazsa subscription'ı düşürür. node-opcua varsayılan olarak `lifetimeCount ≥ 3 × maxKeepAliveCount` ister; aksi halde subscription, istemci yavaşladığında erken ölür. Bu yüzden `requestedLifetimeCount: 120, requestedMaxKeepAliveCount: 20` gibi 6:1 oran güvenlidir.

**node-opcua'nın yeniden bağlanma katmanı.** `connectionStrategy` (initialDelay/maxRetry/maxDelay) yalnızca **ilk bağlantı** için geçerlidir. Çalışma sırasında kopan bağlantı için kütüphane otomatik olarak SecureChannel'ı yeniden kurmaya çalışır, başarılı olursa session ve subscription'ları **transfer etmeyi** dener (`transferSubscriptions` servisi). Sunucu bu servisi desteklemiyorsa (bazı CODESYS sürümleri desteklemez) subscription'lar kaybolur — Not 5'in kök nedeni budur. Bu yüzden production'da `connection_reestablished` sonrası subscription sağlığını doğrulamak şarttır.

**vs alternatifler:** node-opcua saf JS/TS implementasyondur (native binding yok), bu yüzden taşınabilir ama yüksek throughput'ta (>50k notification/s) Python `asyncua` veya .NET stack'inden yavaştır. Web HMI senaryosunda (yüzlerce tag, saniyede onlarca değişim) bu fark görünmez; avantajı aynı dilde (TS) backend + frontend tip paylaşımıdır. Alternatif `opcua-web` gibi tarayıcı-içi WebSocket-OPC UA köprüleri vardır ama bunlar yine bir gateway gerektirir — tarayıcı opc.tcp TCP soketi açamaz, bu mimari kısıt değişmez.

## İlgili Konular

```
knowledge/hmi/web-based/
├── 02_modbus_clients_js.md      → Modbus TCP JavaScript istemcisi
├── 03_react_patterns.md         → Frontend OPC UA veri tüketimi
└── 05_realtime_websocket.md     → OPC UA → WebSocket → Tarayıcı akışı

knowledge/protocols/opc-ua/
├── 04_subscriptions.md          → Subscription parametre teorisi
└── 06_client_implementations.md → Python ve .NET örnekleri
```
