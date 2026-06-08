---
KONU        : Web Tabanlı HMI Geliştirme — Sentez
KATEGORİ    : hmi
ALT_KATEGORI: web-based
SEVİYE      : Orta–İleri
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "knowledge/hmi/web-based/01_opcua_clients_js.md"
    başlık: "JavaScript ile OPC UA İstemci Geliştirme"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/web-based/02_modbus_clients_js.md"
    başlık: "JavaScript ile Modbus TCP İstemci Geliştirme"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/web-based/03_react_patterns.md"
    başlık: "React ile Endüstriyel HMI Geliştirme"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/web-based/04_vue_patterns.md"
    başlık: "Vue.js ile Endüstriyel HMI Geliştirme"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/web-based/05_realtime_websocket.md"
    başlık: "WebSocket ile Gerçek Zamanlı HMI Veri Akışı"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_opcua_clients_js.md"
    ilişki: detaylandırır
  - konu: "02_modbus_clients_js.md"
    ilişki: detaylandırır
  - konu: "03_react_patterns.md"
    ilişki: detaylandırır
  - konu: "04_vue_patterns.md"
    ilişki: detaylandırır
  - konu: "05_realtime_websocket.md"
    ilişki: detaylandırır
  - konu: "knowledge/protocols/opc-ua/04_subscriptions.md"
    ilişki: gerektirir
  - konu: "knowledge/protocols/modbus-tcp/02_register_model.md"
    ilişki: gerektirir
  - konu: "knowledge/hmi/architecture/02_realtime_data.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Node.js ve async/await temelleri"
  - "OPC UA subscription kavramı (protocols/opc-ua/04_subscriptions.md)"
  - "Modbus TCP register modeli (protocols/modbus-tcp/02_register_model.md)"
  - "React veya Vue 3 Composition API temel kullanımı"
  - "HTTP ile WebSocket farkı: kalıcı bağlantı kavramı"
ÇELİŞKİLER :
  - kaynak: "Beş kaynak belgesi"
    konu: "Bu sentez belgesi yeni çelişki içermez; kaynak belgelere atıflar yapar."
    çözüm: "Her kaynak belgede protokol veya framework seçim çelişkileri ayrı ayrı ele alınmıştır."
---

## Özün Ne

Bu sentez, "Bir PLC'deki veriyi tarayıcıya nasıl gerçek zamanlı taşırım?" sorusunun tam yanıtıdır. Beş belge birbirinin halkasıdır: OPC UA ve Modbus istemcileri PLC'ye bağlanır; WebSocket sunucusu bu veriyi tarayıcıya iter; React veya Vue frontend veriyi görsel bileşenlere dönüştürür. Tüm bu halkalar birlikte kurulduğunda, klasik SCADA yazılımlarının yerini alabilecek, tarayıcıdan erişilebilen, sıfır kurulum gerektiren bir web HMI ortaya çıkar.

Temel kavramsal geçiş: "Polling değil, push." PLC'yi saniyede N kez sorgulamak yerine PLC verisi değişince sunucu tarayıcıya iter. Bu fark, hem ağ yükünü hem de PLC CPU yükünü dramatik biçimde azaltır; gözlemlenen oran 50 istemci × polling'e karşı tek OPC UA subscription + WebSocket broadcast.

## Nasıl Çalışır

### Tam Stack Zihin Haritası

```
┌─────────────────────────────────────────────────────────────────────────┐
│              WEB TABANLI HMI — TAM STACK ZİHİN HARİTASI                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  PLC KATMANI                                                             │
│  ┌────────────────────────────┐  ┌───────────────────────────┐          │
│  │      CODESYS / IEC PLC     │  │  Modbus TCP PLC/Cihaz     │          │
│  │  opc.tcp://192.168.1.x:4840│  │  192.168.1.x:502          │          │
│  └──────────────┬─────────────┘  └─────────────┬─────────────┘          │
│                 │ OPC UA Subscription            │ Polling (500ms)       │
│                 ▼                               ▼                        │
│  BACKEND KATMANI — Node.js (TypeScript)                                  │
│  ┌──────────────────────────────────────────────────────────┐            │
│  │                                                          │            │
│  │  ┌───────────────────┐   ┌───────────────────────┐      │            │
│  │  │   OPCUAManager    │   │    ModbusManager       │      │            │
│  │  │  (node-opcua)     │   │    (jsmodbus)          │      │            │
│  │  │                   │   │                        │      │            │
│  │  │  • createSession  │   │  • net.Socket + TCP    │      │            │
│  │  │  • createSubscr.  │   │  • setInterval poll    │      │            │
│  │  │  • MonitoredItem  │   │  • Promise.all reads   │      │            │
│  │  │  • auto-reconnect │   │  • float32/uint32 dec  │      │            │
│  │  │  • ns=idx dynamic │   │  • auto-reconnect      │      │            │
│  │  └────────┬──────────┘   └──────────┬────────────┘      │            │
│  │           │ emit("tagUpdate")        │ emit("tagUpdate") │            │
│  │           └──────────────┬──────────┘                   │            │
│  │                          ▼                               │            │
│  │              ┌───────────────────────┐                  │            │
│  │              │  HMIWebSocketServer   │                  │            │
│  │              │  (ws paketi, port 8080│                  │            │
│  │              │                       │                  │            │
│  │              │  • broadcast()        │                  │            │
│  │              │  • FULL_UPDATE (ilk)  │                  │            │
│  │              │  • TAG_UPDATE (delta) │                  │            │
│  │              │  • WRITE_ACK          │                  │            │
│  │              │  • Ping/Pong 30s      │                  │            │
│  │              │  • BatchUpdateManager │                  │            │
│  │              └──────────┬────────────┘                  │            │
│  └─────────────────────────┼────────────────────────────────┘           │
│                            │ ws:// (WS) veya wss:// (WSS)               │
│                            ▼                                             │
│  FRONTEND KATMANI — Tarayıcı                                             │
│  ┌──────────────────────────────────────────────────────────┐            │
│  │                                                          │            │
│  │  useWebSocket hook / composable (Singleton bağlantı)     │            │
│  │       │ onmessage                                        │            │
│  │       ▼                                                  │            │
│  │  ┌─────────────────────────────────────────────────┐    │            │
│  │  │        State Yönetimi                           │    │            │
│  │  │  React: Zustand Store (useHMIStore)             │    │            │
│  │  │  Vue:   Pinia Store   (useHMIStore)             │    │            │
│  │  │         • tags: Record<string, TagValue>        │    │            │
│  │  │         • connectionStatus                      │    │            │
│  │  │         • activeAlarms                          │    │            │
│  │  └───────┬─────────────────────────────────────────┘    │            │
│  │          │ granüler selector                            │            │
│  │          ▼                                              │            │
│  │  ┌──────────────────────────────────────────────────┐   │            │
│  │  │  useTagValue('actual_speed') → AnalogGauge       │   │            │
│  │  │  useTagValue('motor_fault')  → StatusIndicator   │   │            │
│  │  │  useTagValue('temperature')  → TagDisplay        │   │            │
│  │  │  useConnectionStatus()       → ConnectionBanner  │   │            │
│  │  └──────────────────────────────────────────────────┘   │            │
│  │                                                          │            │
│  │  Yazma akışı:                                            │            │
│  │  SetpointControl → sendCommand("WRITE_REGISTER", …)      │            │
│  │  → wsInstance.send(JSON.stringify(msg))                  │            │
│  │  → Backend: validateToken → plcManager.writeTag()        │            │
│  │  → WRITE_ACK                                             │            │
│  └──────────────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────────┘
```

### "Veri Bir Değer Değişiminde Ne Olur?" Mental Model

```
1. PLC CODESYS'te GVL_IO.rActualSpeed değişti (45.2 → 45.8)

2. BACKEND — OPCUAManager:
   • MonitoredItem "changed" olayı ateşlendi (samplingInterval: 500ms)
   • emit("tagUpdate", { tag: "actual_speed", value: 45.8,
                         quality: "GOOD", timestamp: Date })

3. BACKEND — BatchUpdateManager (opsiyonel):
   • 100ms içindeki tüm değişimleri biriktir
   • flush() → tek BATCH_UPDATE mesajı

4. BACKEND — HMIWebSocketServer:
   • broadcast({ type: "TAG_UPDATE", tag: "actual_speed",
                  value: 45.8, quality: "GOOD", timestamp: … })
   • Tüm açık WebSocket istemcilerine gönder

5. BROWSER — WebSocket onmessage:
   • msg.type === "TAG_UPDATE" → store.updateTag(…)

6. BROWSER — State (Zustand/Pinia):
   • tags["actual_speed"] = { value: 45.8, quality: "GOOD", ts }
   • Yalnızca "actual_speed" tag'ini izleyen bileşenler render tetiklenir

7. BROWSER — AnalogGauge bileşeni:
   • useTagValue("actual_speed") → value = 45.8
   • Gauge fill %45.8 genişliğinde → DOM güncellendi
   • Kullanıcı 45.8 değerini görür
```

## Hızlı Referans Tabloları

### Tablo 1: Protokol ve JavaScript Client Kütüphaneleri

| Protokol | Kütüphane | npm Paketi | Mekanizma | Ne Zaman |
|---|---|---|---|---|
| OPC UA | node-opcua | `node-opcua` | Subscription (push) | CODESYS, Siemens, modern PLC |
| Modbus TCP | jsmodbus | `jsmodbus` | Polling (setInterval) | Legacy PLC, Modbus destekleyen her cihaz |
| Modbus TCP+RTU | modbus-serial | `modbus-serial` | Polling | RTU/seri de gerekiyorsa |

**Seçim kuralı**: OPC UA mümkünse tercih et; subscription sayesinde PLC'yi sorgulamak yerine PLC seni haberdar eder. Sadece Modbus destekleyen cihazlarda polling kaçınılmaz — polling hızını PLC belgesindeki max sorgu hızını aşmadan ayarla.

### Tablo 2: OPC UA İstemci Kritik Parametreler

| Parametre | Önerilen Değer | Açıklama |
|---|---|---|
| `requestedPublishingInterval` | 500ms | Sunucunun değişimleri göndereceği aralık |
| `samplingInterval` (alarm) | 100ms | Alarm/kritik tag daha sık örneklenir |
| `samplingInterval` (analog) | 500ms | Normal telemetri |
| `samplingInterval` (sayaç) | 5000ms | Yavaş değişen tag |
| `requestedSessionTimeout` | 3600000ms (1 saat) | WS backend session'ı için yeterli süre |
| Namespace index | `session.getNamespaceIndex(uri)` | Asla hardcode etme (`ns=4` olmayabilir) |
| Güvenlik (geliştirme) | `MessageSecurityMode.None` | Geliştirme kolaylığı |
| Güvenlik (üretim) | `SignAndEncrypt + Basic256Sha256` | `OPCUACertificateManager` ile |

### Tablo 3: Modbus TCP Polling Parametreleri

| Parametre | Önerilen Değer | Açıklama |
|---|---|---|
| Polling aralığı | 500ms–1000ms | PLC CPU yüküne göre ayarla |
| readHoldingRegisters max boyut | 125 register/istek | Modbus TCP spesifikasyon sınırı |
| Eş zamanlı istek | Dikkatli kullan | Bazı PLC'ler Promise.all'a yanıt karıştırır |
| 0-tabanlı adres | HR 40101 → index 100 | 40001 çıkarılır |
| Float32 decode | `Buffer.readFloatBE()` | Big-Endian: high word önce |
| Uint32 decode | `(regs[0] << 16) \| regs[1]` | 32-bit sayaç iki register'dan |

### Tablo 4: React vs Vue — HMI Bağlamında Karşılaştırma

| Kriter | React | Vue 3 |
|---|---|---|
| State yönetimi | Zustand (önerilir) | Pinia (resmi, önerilir) |
| WebSocket hook | `useWebSocket` (hook) | `useWebSocket` (composable) |
| Tag hook | `useTagValue` (hook) | `useTagValue` (composable) |
| Reaktivite | Manuel (`React.memo`, `useMemo`, granüler selector) | Otomatik (Proxy tabanlı, ekstra optimizasyon az) |
| Render optimizasyonu çabası | Yüksek | Düşük |
| Öğrenme eğrisi | Dik | Daha kolay |
| CPU (200 tag, 50 güncelleme/s) | Granüler selector olmadan %60+ | Pinia + computed ile %18 |
| Şablon stili | JSX / TSX | SFC (`<template>`, `<script setup>`) |
| Büyük proje esnekliği | Yüksek | Orta-Yüksek |
| TypeScript entegrasyonu | Çok güçlü | Güçlü |
| Ekip hafif/hızlı prototip | Dezavantaj | Avantaj |
| **HMI için tercih** | Büyük/karmaşık | Orta ölçek, hızlı geliştirme |

### Tablo 5: WebSocket Mesaj Tipleri (Tam Protokol)

| Mesaj Tipi | Yön | Tetikleyen | İçerik |
|---|---|---|---|
| `FULL_UPDATE` | Sunucu → Tarayıcı | Yeni bağlantı kurulunca | Tüm tag değerleri + PLC bağlantı durumu |
| `TAG_UPDATE` | Sunucu → Tarayıcı | Tek tag değişiminde | tag, value, quality, timestamp |
| `BATCH_UPDATE` | Sunucu → Tarayıcı | 100ms batch (opsiyonel) | Tüm değişimler tek mesajda |
| `CONNECTION_STATUS` | Sunucu → Tarayıcı | PLC bağlantı değişiminde | status: CONNECTED/DISCONNECTED/DEGRADED |
| `WRITE_ACK` | Sunucu → Tarayıcı | Yazma komutu sonrası | tag, success, error? |
| `PING` | Sunucu → Tarayıcı | Her 30 saniye | Keepalive |
| `WRITE_REGISTER` | Tarayıcı → Sunucu | Operatör setpoint değiştirince | tag, value, sessionToken |
| `WRITE_COIL` | Tarayıcı → Sunucu | Operatör boolean komut | tag, value, sessionToken |
| `PONG` | Tarayıcı → Sunucu | PING'e yanıt | Keepalive |
| `REQUEST_FULL_UPDATE` | Tarayıcı → Sunucu | Manuel yenileme | — |

### Tablo 6: Gerçek Zamanlı Strateji Seçimi

| Senaryo | Strateji | Neden |
|---|---|---|
| Az tag (< 50), basit izleme | Ham TAG_UPDATE broadcast | Basitlik |
| Çok tag (> 50), çok istemci | BatchUpdateManager (100ms) | Mesaj/s azalır |
| Yalnızca izleme (salt okuma) | Server-Sent Events (SSE) alternatif | Daha basit, HTTP/2 üzerinden |
| Yazma komutu gerekiyor | WebSocket zorunlu | İki yönlü iletişim |
| Belirli tag grubunu izleme | İstemci abone filtresi | Gereksiz mesajları engeller |
| Üretim ortamı | WSS (WebSocket Secure over TLS) | Açık metin komut riski |

## Pratikte Nasıl Kullanılır

### "Sıfırdan Web HMI" Kontrol Listesi

**Adım 1 — Backend Kurulumu**

```
□ 1. Node.js + TypeScript projesi başlat
□ 2. npm install node-opcua ws express
   (veya: npm install jsmodbus ws express  ← Modbus için)
□ 3. OPCUAManager veya ModbusManager sınıfını kur
     → Otomatik yeniden bağlanma mutlaka olmalı
     → emit("tagUpdate") olayı → WebSocket'e aktarım
□ 4. HMIWebSocketServer kur (ws paketi, port 8080)
     → Yeni bağlantıya FULL_UPDATE gönder
     → PLC Manager → broadcast(TAG_UPDATE)
     → Ping/Pong keepalive: Her 30s, yanıt yok ise 60s'de terminate
□ 5. Yazma endpoint'leri: WRITE_REGISTER / WRITE_COIL
     → sessionToken doğrulama ZORUNLU
     → WRITE_ACK ile istemciye sonuç gönder
□ 6. Yazma log'u: Kim, ne zaman, hangi tag, hangi değer
```

**Adım 2 — Frontend Kurulumu (React)**

```
□ 7. npm create vite@latest hmi-frontend -- --template react-ts
□ 8. npm install zustand
□ 9. hmiStore.ts oluştur (tags, connectionStatus, activeAlarms)
□ 10. useWebSocket hook → Singleton bağlantı → Store güncelle
□ 11. useTagValue hook → Tek tag seçici → React.memo bileşenler
□ 12. Bileşenler: TagDisplay, AnalogGauge, StatusIndicator, SetpointControl
□ 13. ConnectionBanner: Bağlantı kopunca ekranda uyarı
□ 14. Tüm yazma butonları: disabled={!isConnected}
```

**Adım 2 — Frontend Kurulumu (Vue)**

```
□ 7. npm create vue@latest hmi-frontend  (TypeScript+Pinia+Router seç)
□ 8. stores/hmiStore.ts → defineStore + Composition API
□ 9. composables/useWebSocket.ts → Singleton WS → store.updateTag()
□ 10. composables/useTagValue.ts → computed + storeToRefs
□ 11. Bileşenler: TagDisplay.vue, AnalogGauge.vue, SetpointControl.vue
□ 12. onMounted() içinde initWebSocket() → SSR/test güvenli
□ 13. v-if="connectionStatus !== 'CONNECTED'" → Bağlantı bandı
```

**Adım 3 — Test**

```
□ 15. wscat -c ws://localhost:8080  → Manuel WS bağlantı testi
□ 16. Bağlantı kopma simülasyonu → PLC kablosunu çek → Frontend banner görünmeli
□ 17. Yeniden bağlanma testi → Bağla → FULL_UPDATE geldi mi?
□ 18. Yazma testi → SetpointControl → WRITE_ACK success geldi mi?
□ 19. PLC değerde gerçek değişim → TagDisplay güncellendi mi?
□ 20. Üretim → Nginx + wss:// + HTTPS → Açık metin trafiği yok
```

### Beş Belgeyi Bağlayan Pratik Senaryo

**Görev**: Bir paketleme makinesinin hız setpointini web arayüzünden değiştir, gerçek hızı ve sıcaklığı anlık izle.

```
ADIM 1 — Backend: OPCUAManager (01_opcua_clients_js.md)
  const nsIdx = await session.getNamespaceIndex(
      "http://www.3s-software.com/schemas/Codesys-V3"
  );
  // MonitoredItem: GVL_IO.rActualSpeed, GVL_IO.rActualTemp (500ms sampling)
  item.on("changed", (dv) => opcManager.emit("tagUpdate", { tag, value, quality }));

ADIM 2 — Backend: WebSocket broadcast (05_realtime_websocket.md)
  opcManager.on("tagUpdate", (update) => {
      wsServer.broadcast({ type: "TAG_UPDATE", ...update });
      currentTagValues[update.tag] = update.value;
  });

ADIM 3 — Frontend: Store güncelle (03_react_patterns.md / 04_vue_patterns.md)
  // WebSocket onmessage:
  case "TAG_UPDATE":
      store.updateTag(msg.tag, msg.value, msg.quality, new Date(msg.timestamp));

ADIM 4 — Frontend: Bileşenler
  // React:
  <AnalogGauge tag="actual_speed" label="Gerçek Hız" unit="m/dk" min={0} max={100} />
  <SetpointControl tag="actual_speed" writeTag="speed_setpoint" label="Hız SP" ... />

  // Vue:
  <AnalogGauge tag="actual_speed" label="Gerçek Hız" unit="m/dk" :min="0" :max="100" />
  <SetpointControl tag="actual_speed" write-tag="speed_setpoint" label="Hız SP" ... />

ADIM 5 — Yazma akışı (01 + 05 birlikte)
  // Operatör "Uygula"ya bastı:
  sendCommand("WRITE_REGISTER", { tag: "speed_setpoint", value: 65.0 })
  
  // Backend aldı:
  if (!validateSessionToken(msg.sessionToken)) { → WRITE_ACK false }
  const success = await opcManager.writeTag("speed_setpoint", 65.0);
  → session.writeSingleNode(nodeId, { dataType: "Double", value: 65.0 })
  wsServer.sendToClient(clientId, { type: "WRITE_ACK", tag: "speed_setpoint", success });

  // PLC yeni setpointi işledi → GVL_IO.rActualSpeed yavaş yavaş 65'e yaklaştı
  // MonitoredItem değişimi algıladı → TAG_UPDATE yayını → AnalogGauge güncellendi
```

## Sık Yapılan Hatalar

### Hata 1: Namespace Index'i Hardcode Etmek (OPC UA)

```typescript
// ❌ YANLIŞ — Farklı runtime versiyonunda ns=4 olmayabilir (ns=3 veya ns=5 gelebilir)
const nodeId = "ns=4;s=|var|CODESYS.App.GVL.xMotorRun";

// ✅ DOĞRU — Her session başlangıcında URI'dan dinamik al
const nsIdx = await session.getNamespaceIndex(
    "http://www.3s-software.com/schemas/Codesys-V3"
);
const nodeId = `ns=${nsIdx};s=|var|CODESYS.App.GVL.xMotorRun`;
```

### Hata 2: Modbus'ta 0-Tabanlı Adres Yanlışlığı

```typescript
// Belge: "HR 40101 = Hız Setpoint"
// ❌ YANLIŞ → 40102 okunur
await client.readHoldingRegisters(101, 1);

// ✅ DOĞRU: 40101 - 40001 = 100
await client.readHoldingRegisters(100, 1);
```

### Hata 3: Tüm Store'u Tek Selectorla Almak (React)

```typescript
// ❌ YANLIŞ — Herhangi bir tag değişince 200 bileşen yeniden render olur
const { tags } = useHMIStore();

// ✅ DOĞRU — Yalnızca bu tag değişince render tetiklenir
const speed = useHMIStore((s) => s.tags["actual_speed"]?.value);
```

### Hata 4: storeToRefs Kullanmamak (Vue)

```typescript
// ❌ YANLIŞ — Reaktivite kaybolur, değer asla güncellenmez
const { tags } = useHMIStore();

// ✅ DOĞRU — Reaktif referans
const { tags } = storeToRefs(useHMIStore());
const speed = computed(() => tags.value["actual_speed"]?.value);
```

### Hata 5: Her Bileşende Ayrı WebSocket Açmak

```typescript
// ❌ YANLIŞ — 50 bileşen = 50 WS bağlantısı → Sunucu ve tarayıcı çöker
useEffect(() => {
    const ws = new WebSocket("ws://...");  // Her bileşende yeni
}, []);

// ✅ DOĞRU — App kök seviyesinde Singleton hook
// → Store'u günceller → Tüm bileşenler store'dan okur
```

### Hata 6: Yazma Komutunu Kimlik Doğrulamadan Çalıştırmak

```typescript
// ❌ YANLIŞ — Herhangi biri WebSocket'e bağlanıp PLC'ye yazar
if (msg.type === "WRITE_REGISTER") {
    plcManager.writeTag(msg.tag, msg.value);  // Güvensiz
}

// ✅ DOĞRU
if (!validateSessionToken(msg.sessionToken)) {
    ws.send(JSON.stringify({ type: "WRITE_ACK", success: false, error: "Unauthorized" }));
    return;
}
```

### Hata 7: Bağlantı Kopunca Butonları Aktif Bırakmak

```typescript
// ❌ YANLIŞ — Kullanıcı komut gönderdi ama WebSocket kapalı → Sessizce kaybolur
<button onClick={handleStart}>Başlat</button>

// ✅ DOĞRU
const isConnected = useHMIStore((s) => s.connectionStatus === "CONNECTED");
<button onClick={handleStart} disabled={!isConnected}>Başlat</button>
```

### Hata 8: Ölü WebSocket Bağlantılarını Temizlememek (Backend)

```
Sorun: Switch güç kesildi → Sunucu bağlantıların hâlâ açık olduğunu sanıyor.
       broadcast() hep başarısız, log dolup taşıyor.
       Kaynak sızıntısı: Her yeni bağlantı map'e ekleniyor, hiçbiri silinmiyor.

Çözüm: Her 30s ping() gönder.
        60s içinde pong yoksa: ws.terminate() + clients.delete(clientId)
```

### Hata 9: WSS Olmadan Üretime Almak

```
Sorun: ws:// (şifresiz) → Ağ dinleyicisi tüm PLC komutlarını görebilir.
       IT güvenlik denetiminde bulunur, acil düzeltme gerektirir.

Çözüm: Nginx + SSL sertifikası → wss:// (WebSocket Secure over TLS)
        Frontend bağlantı dizesi: wss://hmi.fabrika.local:8443
```

## Ne Zaman ...

### Ne Zaman OPC UA Seç, Ne Zaman Modbus?

```
OPC UA Seç:
  ✓ PLC CODESYS, Siemens TIA, Beckhoff TwinCAT gibi modern platform
  ✓ Subscription mekanizması istiyorsun (polling değil)
  ✓ Veri kalitesi (GOOD/BAD/UNCERTAIN) önemli
  ✓ Güvenli bağlantı (sertifika, SignAndEncrypt) gerekiyor
  ✓ Veri modeli karmaşık (struct, array, method call)

Modbus Seç:
  ✓ Legacy PLC veya Modbus destekleyen I/O cihazı
  ✓ OPC UA server yok / lisans sorunu var
  ✓ Register haritası belgelenmiş ve sabit
  ✓ Basit int/float veri, struct gerekmez
  ✓ jsmodbus yeterli; RTU de gerekiyorsa modbus-serial
```

### Ne Zaman React, Ne Zaman Vue?

```
React Seç:
  ✓ Ekip React biliyor
  ✓ Çok büyük uygulama (100K+ satır, 20+ geliştirici)
  ✓ TypeScript entegrasyonu çok kritik
  ✓ Mobil (React Native) de planlanıyor
  ✓ Zengin üçüncü parti kütüphane seçimi önemli

Vue Seç:
  ✓ Ekip JavaScript biliyor ama frontend framework'e yeni
  ✓ Hızlı prototipleme ve daha az boilerplate isteniyoe
  ✓ Orta ölçek (5–15 geliştirici, 5K–50K satır)
  ✓ Granüler reaktivite → React.memo/useMemo optimizasyon çabası azalsın
  ✓ Resmi entegre ekosistem (Pinia + Vue Router) yeterli
```

### Ne Zaman Batch Update Ekle?

```
Ekle:
  ✓ 50'den fazla tag aynı 500ms dilimde değişiyor
  ✓ 10'dan fazla eş zamanlı WebSocket istemcisi
  ✓ Sunucu CPU yükü yüksek, network trafiği yüksek

Ekleme:
  ✗ Az tag, az istemci → Karmaşıklık değmez
  ✗ Bazı tag'ler gecikme toleranssız (kritik alarm) → O tag'ler için anlık gönder
```

### Ne Zaman Doğrudan WebSocket, Ne Zaman SSE?

```
WebSocket:
  ✓ Operatör yazma komutu gönderiyor (setpoint, coil)
  ✓ İki yönlü iletişim zorunlu
  → Endüstriyel HMI'ın neredeyse tamamı bu kategoride

SSE (Server-Sent Events):
  ✓ Sadece izleme (salt okuma) dashboard
  ✓ HTTP/2 altyapısı var, basitlik isteniyor
  ✗ Yazma komutu yoksa veya REST API ile ayrı ele alınıyorsa
```

## Gerçek Proje Notları

**Not 1 — 50 Teknisyen, 1 OPC UA Bağlantısı**
50 teknisyen aynı anda web HMI kullandı. OPC UA Manager tek subscription tuttu, 50 WebSocket istemcisine broadcast etti. PLC'ye tek bağlantı. Polling modelinde 50 OPC UA session açık olacaktı — WebSocket + broadcast ile %98 kaynak tasarrufu.

**Not 2 — Ping/Pong ile Hayalet Bağlantı Tespiti**
Fabrika ağ switchi güç kesildi; WebSocket bağlantıları sunucu tarafında 5 dakika "açık" göründü. 30s ping / 60s pong timeout + terminate eklendikten sonra hayalet bağlantılar 35 saniyede temizlendi.

**Not 3 — Batch Update ile CPU Düşüşü**
500ms'de 80 tag değişimi × 20 istemci = saniyede 1600 ayrı mesaj; sunucu CPU %45. 100ms BatchUpdateManager ile 80 mesaj → 1 BATCH_UPDATE × 20 istemci → 20 mesaj/500ms. CPU %6'ya indi.

**Not 4 — Vue Reaktivitesi "Ücretsiz" Performans**
Aynı uygulamayı React.memo / useMemo olmadan React'ta yazdı → CPU %60. Vue Pinia + computed ile (ekstra optimizasyon olmadan) → CPU %18. Küçük-orta projede Vue'nun Proxy tabanlı granüler reaktivitesi ekstra emek gerektirmeden kazanıyor.

**Not 5 — React.memo'nun Nesne Prop Tuzağı**
`<AnalogGauge config={{ min: 0, max: 100 }} />` şeklinde nesne prop geçildi. Her render'da yeni nesne referansı oluştu; `React.memo` eşleşme bulamadı ve her render tetiklendi. Çözüm: Konfigürasyonu bileşen dışında sabit tanımla ya da `useMemo` ile sar.

**Not 6 — Namespace Index Sürprizi (OPC UA)**
CODESYS runtime versiyonu değiştiğinde hardcoded `ns=4` ifadesi başka bir PLC'de `ns=3` olarak geldi. `session.getNamespaceIndex(uri)` dinamik çağrısı her projede zorunlu hale getirildi.

**Not 7 — Modbus Promise.all PLC Uyumsuzluğu**
Bir legacy PLC'de `Promise.all` ile eş zamanlı dört Modbus isteği gönderildi; PLC yanıtları karıştırdı, bazı istemciler yanlış veri aldı. Çözüm: Sıralı istek. Modbus single-master protokol; eş zamanlı isteği desteklemeyen PLC'ler var. Test ortamında mutlaka doğrula.

**Not 8 — WSS Olmadan IT Denetimi**
HTTP üzerinden sunulan web HMI, `ws://` (şifresiz) WebSocket kullandı. IT güvenlik denetimi: "Tüm PLC komutları açık metin." Acil geçiş: Nginx SSL termination + `wss://` bağlantı. 2 saat çalışma süresi. Üretim ortamı planlamasında WSS baştan dahil edilmeli.

## İlgili Konular

```
knowledge/hmi/web-based/          ← Şu an buradasınız
├── 01_opcua_clients_js.md        → OPC UA backend detayları (node-opcua)
├── 02_modbus_clients_js.md       → Modbus TCP backend detayları (jsmodbus)
├── 03_react_patterns.md          → React + Zustand HMI desenleri
├── 04_vue_patterns.md            → Vue 3 + Pinia HMI desenleri
├── 05_realtime_websocket.md      → WebSocket sunucu/istemci tam implementasyon
└── _synthesis.md                 → Bu belge

Ön gereksinimler (Protokol katmanı):
knowledge/protocols/
├── opc-ua/
│   ├── 04_subscriptions.md      → MonitoredItem parametre teorisi
│   └── 06_client_implementations.md
└── modbus-tcp/
    ├── 02_register_model.md     → Register adresleme ve ölçekleme
    └── 03_function_codes.md     → FC01/03/04/05/06/16 referansı

Üst mimari:
knowledge/hmi/architecture/
├── 01_hmi_patterns.md           → ISA-101 tasarım prensipleri
├── 02_realtime_data.md          → Stale data ve bağlantı yönetimi
└── 03_alarm_management.md       → Alarm sistemi tasarımı

PLC tarafı:
knowledge/codesys/
└── fundamentals/_synthesis.md   → CODESYS Runtime + Proje + Diller sentezi

Araçlar:
  wscat       → WebSocket CLI test: wscat -c ws://localhost:8080
  Postman     → WebSocket test (v10+)
  Wireshark   → WebSocket trafik analizi
  Vue DevTools → Pinia state + reaktivite debug
  Redux DevTools → Zustand state debug (zustand-devtools ile)
```
