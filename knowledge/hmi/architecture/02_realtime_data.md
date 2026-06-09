---
KONU        : HMI'da Gerçek Zamanlı Veri Yönetimi
KATEGORİ    : hmi
ALT_KATEGORI: architecture
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://www.code-brew.com/hmi-software-development-guide/"
    başlık: "Code-Brew — HMI Software Development Guide for 2026"
    güvenilirlik: topluluk
  - url: "https://www.trout.software/blog/real-time-plc-data-streaming-opc-ua-modbus-and-modern-integration-patterns"
    başlık: "Trout Software — Real-Time PLC Data Streaming: OPC UA and Modbus Patterns"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_hmi_patterns.md"
    ilişki: gerektirir
  - konu: "03_alarm_management.md"
    ilişki: tamamlar
  - konu: "knowledge/protocols/opc-ua/04_subscriptions.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "HMI mimari kalıpları (01_hmi_patterns.md)"
  - "OPC UA subscription veya Modbus polling kavramı"
ÇELİŞKİLER :
  - kaynak: "Polling her şeyi çözer algısı"
    konu: "100ms polling yeterli gibi görünür ama gizli sorunlar yaratır"
    çözüm: >
      Polling, PLC ve ağ üzerinde sürekli yük oluşturur.
      100ms polling × 1000 tag = 10.000 okuma/saniye.
      OPC UA Subscription: Yalnızca değişen değerler gelir.
      Subscription ile network trafiği %70-90 azalabilir.
      Ancak Modbus TCP için subscription alternatif yoktur — polling zorunlu.
---

## Özün Ne

"Gerçek zamanlı" ifadesi HMI bağlamında yanıltıcı olabilir. PLC, fiziksel I/O'yu 10ms'de işlerken HMI ekranı 200ms'de yenileniyorsa bu kabul edilebilir bir tasarımdır — operatör 200ms farkı algılamaz. Ancak alarm durumu PLC'de aktif olduktan 5 saniye sonra HMI'da görünüyorsa bu ciddi bir sorundur. Veri yönetimi, hangi verinin ne kadar hızlı güncellenmesi gerektiğini doğru analiz etmekle başlar. Bu belge, polling ve event-driven mimarilerini, bağlantı kopma yönetimini, stale data tespitini ve gerçek projelerde yaşanan performans sorunlarını ele alır.

## Nasıl Çalışır

### Polling vs Event-Driven (Subscription)

```
Polling (Modbus TCP ile zorunlu, OPC UA ile seçimlik):

  HMI                 PLC
   │── "Değer ne?" ──►│
   │◄── "82.5°C" ─────│
   │    (100ms bekle)   │
   │── "Değer ne?" ──►│
   │◄── "82.5°C" ─────│
   │    (100ms bekle)   │
   ...
   
   Problem: Değer değişmese de sürekli sorgu.
   1000 tag × her 100ms = 10.000 mesaj/saniye (boşuna).

Event-Driven / Subscription (OPC UA):

  HMI                 PLC (OPC UA Server)
   │── Subscribe ────►│
   │◄── "82.5°C" ─────│  (ilk değer)
   │                   │
   │  (3 dakika sessiz, değer değişmedi)
   │                   │
   │◄── "83.1°C" ─────│  (değer değişti → bildirim)
   │◄── "83.4°C" ─────│  (değer değişti → bildirim)
   
   Avantaj: Yalnızca değişim iletilir.
   1000 tag'de çoğu sabit → Çok az mesaj.
```

### Veri Hızı Gereksinimleri Analizi

Her tag için güncelleme hızı analiz edilmeli:

```
Tag Tipi              Güncelleme Sıklığı    Yöntem
──────────────────────────────────────────────────────────────────────
Alarm durumu           <100ms               OPC UA Sub (hızlı) veya dedike poll
Motor çalışma biti     100-200ms            OPC UA Sub
Anlık ölçüm (hız)     200-500ms            OPC UA Sub / Polling
Sıcaklık, basınç      500ms-1s             OPC UA Sub / Polling
Sayaç, toplam üretim   1-5s                OPC UA Sub / Polling
Enerji tüketimi        5-60s               Slow polling / MQTT
Vardiya raporu         Dakika/vardiya       REST API, veritabanı
──────────────────────────────────────────────────────────────────────

Kural: Ekran yenileme hızı ≥ veri güncelleme hızı olmalı.
       Veri 100ms'de değişiyor ama ekran 500ms'de yenileniyorsa:
       → 4 değer değişimi kaçırılır.
       → Alarm gecikmesi: max 500ms (genellikle kabul edilebilir).
```

### Veri Katmanı Tasarımı

Web HMI mimarisinde veri katmanı ayırımı:

```
Browser (React/Vue)
    │ WebSocket push
    ▼
Backend API (Node.js/Python)
    ├── OPC UA Client (subscription)    ─► CODESYS/PLC (OPC UA Server)
    ├── Modbus Client (polling thread)  ─► Legacy PLC
    └── MQTT Subscriber                 ─► MQTT Broker

Backend sorumluluğu:
  1. PLC bağlantısını yönet (reconnect dahil)
  2. Gelen değerleri normalize et (birim dönüşümü, ölçeklendirme)
  3. Değişen değerleri WebSocket ile browser'a ilet
  4. Bağlantı durumunu izle ve yayınla
  5. Alarm durumlarını tespit et ve ilet
```

### WebSocket ile Gerçek Zamanlı Veri (Web HMI)

```javascript
// Backend: OPC UA Subscription → WebSocket push
const { OPCUAClient } = require('node-opcua');
const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });
const clients = new Set();

wss.on('connection', (ws) => {
    clients.add(ws);
    
    // Yeni bağlanan istemciye mevcut durumu gönder
    ws.send(JSON.stringify({
        type: 'FULL_UPDATE',
        data: currentTagValues,
        connectionStatus: 'CONNECTED',
        timestamp: Date.now()
    }));
    
    ws.on('close', () => clients.delete(ws));
});

// OPC UA değer değişiminde tüm WebSocket istemcilerine gönder
function broadcastTagUpdate(tagName, value, quality, timestamp) {
    const msg = JSON.stringify({
        type: 'TAG_UPDATE',
        tag: tagName,
        value: value,
        quality: quality,     // 'GOOD' | 'BAD' | 'UNCERTAIN'
        timestamp: timestamp
    });
    
    for (const client of clients) {
        if (client.readyState === WebSocket.OPEN) {
            client.send(msg);
        }
    }
}
```

```javascript
// Frontend: WebSocket → State güncellemesi (React)
import { useState, useEffect, useCallback } from 'react';

function usePLCData() {
    const [tags, setTags] = useState({});
    const [connectionStatus, setConnectionStatus] = useState('CONNECTING');
    const [lastUpdate, setLastUpdate] = useState(null);
    
    useEffect(() => {
        let ws;
        let reconnectTimer;
        
        function connect() {
            ws = new WebSocket('ws://localhost:8080');
            
            ws.onopen = () => {
                setConnectionStatus('CONNECTED');
                clearTimeout(reconnectTimer);
            };
            
            ws.onmessage = (event) => {
                const msg = JSON.parse(event.data);
                
                if (msg.type === 'FULL_UPDATE') {
                    setTags(msg.data);
                    setConnectionStatus('CONNECTED');
                } else if (msg.type === 'TAG_UPDATE') {
                    setTags(prev => ({
                        ...prev,
                        [msg.tag]: {
                            value: msg.value,
                            quality: msg.quality,
                            timestamp: msg.timestamp
                        }
                    }));
                    setLastUpdate(msg.timestamp);
                } else if (msg.type === 'CONNECTION_STATUS') {
                    setConnectionStatus(msg.status);  // 'CONNECTED' | 'DISCONNECTED' | 'DEGRADED'
                }
            };
            
            ws.onclose = () => {
                setConnectionStatus('DISCONNECTED');
                // 3 saniye sonra yeniden bağlan
                reconnectTimer = setTimeout(connect, 3000);
            };
            
            ws.onerror = () => {
                setConnectionStatus('ERROR');
            };
        }
        
        connect();
        
        return () => {
            clearTimeout(reconnectTimer);
            if (ws) ws.close();
        };
    }, []);
    
    return { tags, connectionStatus, lastUpdate };
}
```

### Stale Data (Eski Veri) Yönetimi

```javascript
// Tag değeri için kalite ve yaşlılık kontrolü
function TagDisplay({ tagName, displayName, unit, maxAgeMs = 5000 }) {
    const { tags, connectionStatus } = usePLCData();
    const tag = tags[tagName];
    
    const isStale = tag
        ? (Date.now() - tag.timestamp) > maxAgeMs
        : false;
    const isBadQuality = tag?.quality === 'BAD';
    const isUncertain = tag?.quality === 'UNCERTAIN';
    
    // Bağlantı durumu veya veri kalitesi sorunları
    const hasIssue = connectionStatus !== 'CONNECTED' || isStale || isBadQuality;
    
    return (
        <div className={`tag-display ${hasIssue ? 'stale' : ''}`}>
            <span className="label">{displayName}</span>
            <span className={`value ${isBadQuality ? 'bad-quality' : ''}`}>
                {tag ? tag.value.toFixed(1) : '--.-'}
            </span>
            <span className="unit">{unit}</span>
            
            {/* Kalite ve eski veri göstergesi */}
            {isStale && (
                <span className="staleness-indicator" title="Veri güncellenmedi">
                    ⚠ {Math.round((Date.now() - tag.timestamp) / 1000)}s önce
                </span>
            )}
            {isBadQuality && (
                <span className="quality-badge bad">BAD</span>
            )}
        </div>
    );
}
```

```css
/* Stale data görsel gösterimi */
.tag-display.stale .value {
    color: #888888;        /* Grileştirilmiş değer */
    font-style: italic;    /* İtalik → "eski veri" işareti */
}

.tag-display .value.bad-quality {
    text-decoration: line-through; /* Üstü çizili → "geçersiz" */
    color: #cc4444;
}

.staleness-indicator {
    font-size: 0.7em;
    color: #cc8800;  /* Turuncu uyarı */
    margin-left: 4px;
}
```

### Bağlantı Kopma Yönetimi

```javascript
// Bağlantı durumu overlay bileşeni
function ConnectionOverlay({ status }) {
    if (status === 'CONNECTED') return null;
    
    const messages = {
        'DISCONNECTED': {
            severity: 'error',
            text: 'PLC Bağlantısı Kesildi',
            subtext: 'Son değerler gösteriliyor. Yeniden bağlanılıyor...',
            showBlinkingDot: true
        },
        'CONNECTING': {
            severity: 'warning',
            text: 'Bağlanıyor...',
            subtext: 'Lütfen bekleyin',
            showBlinkingDot: false
        },
        'DEGRADED': {
            severity: 'warning',
            text: 'Kısmi Bağlantı',
            subtext: 'Bazı veriler güncel olmayabilir',
            showBlinkingDot: true
        }
    };
    
    const info = messages[status] || messages['DISCONNECTED'];
    
    return (
        <div className={`connection-overlay ${info.severity}`}>
            <div className="overlay-banner">
                {info.showBlinkingDot && <span className="blink-dot" />}
                <strong>{info.text}</strong>
                <p>{info.subtext}</p>
            </div>
            {/* Ekranın geri kalanı görünür ama tüm yazma butonları devre dışı */}
        </div>
    );
}
```

**Bağlantı kopunca ne yapılmalı:**
```
✅ Yapılmalı:
  1. Bağlantı kopma anını kaydet
  2. Banner/overlay ile operatörü uyar (belirgin ama engelleyici değil)
  3. Son bilinen değerleri göster ama "eski" işareti ekle
  4. Yazma butonlarını devre dışı bırak (tehlikeli)
  5. Arka planda yeniden bağlanma döngüsü başlat
  6. Bağlantı yeniden kurulunca overlay kaldır + tam güncelleme al

✗ Yapılmamalı:
  1. Ekranı tamamen boş bırakmak
  2. Yazma butonlarını açık bırakmak (komut nereye gidecek?)
  3. "Yenile" diyerek kullanıcıya bırakmak (fabrika zemini bu değil)
  4. Bağlantı koptuğunu sessizce geçiştirmek
```

### Modbus Polling Döngüsü Tasarımı

```python
# Backend Modbus polling — asyncio ile
import asyncio
from pymodbus.client import AsyncModbusTcpClient

class ModbusPoller:
    def __init__(self, host, port=502, slave_id=1):
        self.client = AsyncModbusTcpClient(host, port=port)
        self.slave_id = slave_id
        self.tag_values = {}
        self.connection_status = 'DISCONNECTED'
        self.callbacks = []
    
    def on_update(self, callback):
        self.callbacks.append(callback)
    
    async def _notify(self, tag, value, quality):
        for cb in self.callbacks:
            await cb(tag, value, quality, time.time())
    
    async def run(self):
        while True:
            if not self.client.connected:
                try:
                    await self.client.connect()
                    self.connection_status = 'CONNECTED'
                    await self._notify('_connection', True, 'GOOD')
                except Exception:
                    self.connection_status = 'DISCONNECTED'
                    await self._notify('_connection', False, 'BAD')
                    await asyncio.sleep(5)
                    continue
            
            try:
                # Toplu okuma — verimli
                result = await self.client.read_holding_registers(
                    address=0, count=20, slave=self.slave_id
                )
                
                if not result.isError():
                    regs = result.registers
                    
                    # Yalnızca değişen değerleri bildir (polling için önemli)
                    updates = {
                        'speed':       regs[0] / 10.0,
                        'temperature': regs[1] / 10.0,
                        'pressure':    regs[2] / 100.0,
                        'production':  (regs[10] << 16) | regs[11]
                    }
                    
                    for tag, value in updates.items():
                        if self.tag_values.get(tag) != value:
                            self.tag_values[tag] = value
                            await self._notify(tag, value, 'GOOD')
                else:
                    for tag in ['speed', 'temperature', 'pressure']:
                        await self._notify(tag, None, 'BAD')
                
            except Exception as e:
                self.connection_status = 'DISCONNECTED'
                await self._notify('_connection', False, 'BAD')
            
            await asyncio.sleep(0.1)  # 100ms polling
```

### OPC UA Subscription Tasarımı

```python
# OPC UA subscription — değişince bildir
from asyncua import Client

async def setup_subscription(plc_url, on_change_callback):
    """
    OPC UA subscription — polling'e göre çok daha verimli.
    Yalnızca değer değiştiğinde callback tetiklenir.
    """
    async with Client(plc_url) as client:
        handler = DataChangeHandler(on_change_callback)
        
        # Hızlı güncelleme gerektiren: 100ms subscription
        fast_sub = await client.create_subscription(100, handler)
        alarm_nodes = [
            client.get_node("ns=4;s=GVL_Alarms.xMotorFault"),
            client.get_node("ns=4;s=GVL_Alarms.xTempAlarm"),
        ]
        await fast_sub.subscribe_data_change(alarm_nodes)
        
        # Normal: 500ms subscription
        normal_sub = await client.create_subscription(500, handler)
        telemetry_nodes = [
            client.get_node("ns=4;s=GVL_IO.rActualSpeed"),
            client.get_node("ns=4;s=GVL_IO.rTemperature"),
        ]
        await normal_sub.subscribe_data_change(telemetry_nodes)
        
        # Yavaş: 5s subscription
        slow_sub = await client.create_subscription(5000, handler)
        counter_nodes = [
            client.get_node("ns=4;s=GVL_Diagnostics.dwProdCount"),
        ]
        await slow_sub.subscribe_data_change(counter_nodes)
        
        # Süresiz çalış
        await asyncio.sleep(float('inf'))

class DataChangeHandler:
    def __init__(self, callback):
        self.callback = callback
    
    def datachange_notification(self, node, val, data):
        quality = 'GOOD' if data.monitored_item.Value.StatusCode.is_good() else 'BAD'
        timestamp = data.monitored_item.Value.SourceTimestamp.timestamp()
        asyncio.create_task(self.callback(str(node.nodeid), val, quality, timestamp))
```

## Örnekler

### Örnek 1: Farklı Güncelleme Hızı Katmanları

```
Tag              Neden    Hız         Yöntem
──────────────────────────────────────────────────────
xEmergencyStop   Güvenlik  10-50ms   Dedike OPC UA sub, uyarı alarm
xMotorFault      Alarm     100ms     OPC UA sub fast
rActualSpeed     Operasyon 200ms     OPC UA sub normal
rTemperature     İzleme    500ms     OPC UA sub normal
dwProductionCount Raporlama 5s       OPC UA sub slow
nEnergyToday      Enerji   60s       Slow poll / MQTT
```

### Örnek 2: Bağlantı Kesintisinde Ekran Durumu

```
Normal durumda:
  Motor Hızı: [44.8 m/dk]  ← Siyah metin, güncel
  Sıcaklık:  [82.5 °C]     ← Siyah metin, güncel
  Durum:      [ÇALIŞIYOR]   ← Normal renk

Bağlantı kopunca (2 saniye sonra):
  ┌─────────────────────────────────────────────────┐
  │  ⚠ PLC BAĞLANTISI KESİLDİ — YENİDEN BAĞLANIYOR │
  └─────────────────────────────────────────────────┘
  Motor Hızı: [44.8 m/dk]  ← Gri metin, italik (son bilinen)
  Sıcaklık:  [82.5 °C]     ← Gri metin, italik (son bilinen)
  Durum:      [?]            ← Belirsiz
  
  [Başlat] [Durdur]   ← Tüm butonlar DEVRE DIŞI
```

### Örnek 3: Performans Sorunu Tespiti

```
Belirtiler: HMI yavaş, CPU %80+ backend
Araştırma:
  1. Backend logları: 10ms'de 500+ OPC UA okuma
  2. Sebepler: Her widget kendi OPC UA bağlantısı açmış
     50 widget × her biri 100ms poll = 5 saniyede 500 istek
  
Çözüm:
  a) Tek OPC UA client, paylaşımlı subscription
  b) Tek subscription handler → WebSocket broadcast
  c) Frontend: Yalnızca ekranda görünen widget'lar aktif
     (virtualization / intersection observer)
  
Sonuç: CPU %80 → %12
```

## Sık Yapılan Hatalar

### Hata 1: Her Widget Kendi Bağlantısını Açmak

```javascript
// ❌ YANLIŞ — Her bileşen kendi OPC UA/Modbus bağlantısını açar
function MotorWidget({ motorId }) {
    useEffect(() => {
        const client = new OPCUAClient(PLC_URL);  // Her widget için yeni bağlantı!
        client.connect().then(() => { ... });
    }, []);
}

// ✅ DOĞRU — Paylaşımlı singleton bağlantı
// Tek DataService (backend veya frontend store) tüm değerleri yönetir
function MotorWidget({ motorId }) {
    const speed = useTagValue(`motor.${motorId}.speed`);  // Store'dan okur
    const fault = useTagValue(`motor.${motorId}.fault`);
    // DataService bağlantıyı ve subscription'ı merkezi yönetir
}
```

### Hata 2: Throttle/Debounce Olmadan Hızlı Değer Güncellemesi

```javascript
// ❌ YANLIŞ — Her değer değişiminde React re-render tetikler
handler.datachange_notification = (node, val) => {
    setTagValue(node, val);  // Her 10ms'de render → UI takılıyor
};

// ✅ DOĞRU — Throttle ile sınırla
const throttledUpdate = throttle((updates) => {
    setTagValues(prev => ({ ...prev, ...updates }));
}, 100);  // En fazla 100ms'de bir render
```

### Hata 3: Bağlantı Kopmasını Sessizce Geçiştirmek

```javascript
// ❌ YANLIŞ — Hata yok sayılıyor
ws.onerror = () => {};
ws.onclose = () => {};

// ✅ DOĞRU — Kullanıcı bilgilendirilmeli
ws.onclose = () => {
    setConnectionStatus('DISCONNECTED');
    // Yazma butonlarını devre dışı bırak
    setWriteEnabled(false);
    // Yeniden bağlanma döngüsü başlat
    scheduleReconnect();
};
```

## Gerçek Proje Notları

**Not 1 — Polling Fırtınası**  
Bir HMI projesinde 200 tag, her biri 100ms polling. Backend 2000 Modbus isteği/saniye yapıyordu. PLC yanıt vermekte gecikmesi → timeout → bağlantı kopma döngüsü. Çözüm: Toplu okuma (200 tag → tek FC03 isteği, 100ms) + OPC UA'ya geçiş. Yük %95 azaldı.

**Not 2 — Stale Data'nın Operatör Kararını Etkilemesi**  
Bakım mühendisi HMI'a baktı, motor sıcaklığı 68°C görüyordu. Motoru incelemeye karar vermedi. Ama OPC UA bağlantısı 20 dakika önce kesilmişti — ekran eski veriyi gösteriyordu, gerçek sıcaklık 92°C'ye ulaşmıştı. Motor aşırı ısındı. Stale data overlay eklendi; artık bağlantı kopunca tüm değerler gri + uyarı görünüyor.

**Not 3 — WebSocket Reconnect'te Tam Güncelleme**  
WebSocket yeniden bağlandıktan sonra yalnızca değişen değerleri göndermek yetmez. Bağlantı kopuk süresinde değişen ama sonradan eski değerine dönen değerler kaybolur. Çözüm: Reconnect'te her zaman FULL_UPDATE: tüm mevcut değerleri tek mesajda gönder. Ardından delta güncellemeler devam eder.

**Not 4 — Deadband Olmadan Analog Değer Subscription Fırtınası**  
OPC UA subscription'da analog bir basınç sensörü (gürültülü, ±0.05 bar titreşim) 100ms publish interval ile izleniyordu. Değer fiziksel olarak sabit olmasına rağmen sensör gürültüsü yüzünden her 100ms'de "değişti" bildirimi geliyordu — saniyede 10 bildirim, tek tag için. 200 analog tag → saniyede 2000 gereksiz bildirim, frontend re-render fırtınası. Çözüm: OPC UA MonitoringParameters içinde **DataChangeFilter + DeadbandType.Absolute** (ör. 0.1 bar) tanımlandı. Artık yalnızca 0.1 bar'dan fazla değişim bildiriliyor. Bildirim trafiği %95 düştü. Ders: Subscription "değişince gönderir" doğru ama "değişim" tanımını deadband ile sen belirlemezsen gürültü = değişim sayılır.

**Not 5 — SourceTimestamp vs ServerTimestamp Karışıklığı ve Yanlış Yaşlılık**  
Stale data tespiti `ServerTimestamp` üzerinden yapılıyordu. Bir OPC UA gateway (aggregating server) araya girdiğinde, gateway her değere kendi taze ServerTimestamp'ini basıyordu — alt PLC 30 saniyedir cevap vermese bile değer "taze" görünüyordu. Operatör stale veriyi canlı sandı. Çözüm: Yaşlılık ölçümü için **SourceTimestamp** (değerin kaynakta üretildiği an) kullanıldı; ayrıca StatusCode kalite biti (`Good_LocalOverride`, `Bad_NoCommunication`) izlendi. Ders: Zincirde gateway/aggregator varsa ServerTimestamp tazeliği gerçek tazeliği garantilemez — SourceTimestamp + StatusCode birlikte değerlendirilmeli.

**Not 6 — Queue Overflow ve Sessizce Atlanan Değerler**  
Bir devreye alma sırasında PLC'de hızlı değişen bir sayaç (her 20ms artıyor) 500ms publish interval ile subscribe edilmişti. Monitored item'ın `QueueSize`'ı varsayılan 1 idi. Sonuç: PLC 20ms'de değer üretiyor, kuyruk 1 değer tutuyor, 500ms'de bir okunuyor — aradaki ~24 değişim sessizce *overwrite* ediliyordu (DiscardOldest=true). Üretim sayacı atlamalı görünüyordu. Çözüm: Hızlı sayaçlar için ya `QueueSize` artırıldı (geçmiş değerleri toplu al) ya da PLC tarafında latch/biriktirme yapıldı. Ders: publish interval > değişim hızı ise QueueSize ayarı verinin kaybolup kaybolmayacağını belirler; varsayılan 1 çoğu zaman sessiz veri kaybı demektir.

## Edge Case'ler ve Sistem Limitleri

Gerçek zamanlı veri katmanı, "her şey yolundayken" çalışır; mühendislik kalitesi sınır koşullarda belli olur. Aşağıdaki tablo en kritik edge case'leri toplar.

| Edge Case | Tetikleyen Koşul | Belirti | Doğru Davranış |
|---|---|---|---|
| Stale data canlı görünür | Bağlantı kopuk, ekran son değeri tutuyor | Operatör eski veriyle karar alır | maxAge kontrolü (SourceTimestamp) → gri/italik + overlay |
| Gateway timestamp yanılgısı | Aggregating server taze ServerTimestamp basar | Yaşlılık tespiti devre dışı kalır | SourceTimestamp + StatusCode kullan |
| Subscription fırtınası | Gürültülü analog, deadband yok | Saniyede onlarca bildirim/tag, UI takılır | DataChangeFilter + AbsoluteDeadband |
| Sessiz veri kaybı | publish interval > değişim hızı, QueueSize=1 | Sayaç atlar, geçici tepe kaçar | QueueSize artır veya PLC'de latch |
| Reconnect delta kaybı | Kopuk sürede değişip dönen değer | İlk delta gelmez, değer eski kalır | Reconnect'te FULL_UPDATE |
| Saat kayması (clock skew) | PLC ve HMI saatleri senkron değil | Negatif "yaşlılık", trend zaman kayması | NTP/PTP senkron; yaşlılığı backend saatiyle hesapla |
| WebSocket backpressure | Frontend yavaş, mesaj birikir | Gecikme artar, bellek şişer | Sunucu-tarafı throttle + son-değer koalesleme |
| Modbus toplu okuma sınırı | Tek FC03 ile >125 register istemek | Exception response, okuma başarısız | Register bloklarını ≤125'e böl, ardışık adresle |

**Sayısal limitler ve eşikler:**
```
Modbus FC03/FC04 tek istek      : Max 125 register (16-bit) — protokol sınırı
Modbus FC16 tek yazma           : Max 123 register — protokol sınırı
OPC UA publish interval (pratik): 50ms taban (altı server'ı zorlar, fayda yok)
OPC UA monitored item / sub     : Server'a bağlı; binlerce mümkün ama
                                  PublishingInterval × ItemCount yükü dengele
WebSocket mesaj/saniye (browser): Throttle olmadan ~60+ render/s = jank;
                                  16ms (60fps) altında batch'le
İnsan algı eşiği                : ~100-200ms gecikme fark edilmez;
                                  >500ms "takılıyor" hissi başlar
```

## Optimizasyon

Veri katmanı optimizasyonu kaynağa en yakın yerde başlar: **PLC/server tarafında trafiği azalt**, sonra **ağda azalt**, en son **frontend'de render azalt**. Frontend'de throttle eklemek, kaynaktan gelen gereksiz trafiği geç çözer — önce kaynağı kes.

**Optimizasyon önceliği (kaynaktan görünüme):**
```
1. KAYNAK — Gereksiz veriyi hiç üretme/gönderme
   → OPC UA: DataChangeFilter (deadband) + uygun publish interval katmanı
   → Modbus: ardışık adres haritası, tek toplu okuma, değişim filtresi
   → "Değişmeyen değeri gönderme" — subscription'ın tüm amacı budur

2. AĞ — Aktarım maliyetini düşür
   → Birden çok delta'yı tek mesajda topla (coalesce) — N tag tek frame
   → Binary protokol (MessagePack/protobuf) JSON yerine yüksek hacimde
   → Reconnect'te tek FULL_UPDATE; sürekli tam snapshot gönderme

3. BACKEND — Tek paylaşımlı bağlantı
   → Singleton OPC UA/Modbus client; per-widget bağlantı YASAK
   → Katmanlı subscription: hızlı(100ms)/normal(500ms)/yavaş(5s)
   → Son-değer önbelleği (latest value cache) → yeni istemciye anında snapshot

4. FRONTEND — Render maliyetini düşür (en son)
   → Throttle/coalesce: 16ms penceresinde gelen tüm güncellemeleri batch'le
   → Görünmeyen widget subscription'ını askıya al (IntersectionObserver)
   → Trend canvas-tabanlı; immutable state için referans eşitliği koru
```

**Katmanlı publish interval — neden tek interval kullanılmaz:**
```
Tek 100ms subscription tüm tag'lere uygulanırsa:
  Enerji sayacı (60s'de değişir) bile 100ms'de yoklanır → boşa publish döngüsü.

Doğru: Değişim hızına göre üç subscription:
  fast_sub   (100ms)  → alarm bitleri, güvenlik
  normal_sub (500ms)  → ölçümler
  slow_sub   (5000ms) → sayaçlar, toplamlar
Server publish döngüsü sayısı ve ağ trafiği dramatik düşer.
```

## Derin Teknik Detay

**OPC UA subscription'ın iç mekaniği — neden polling'den üstün:**
Subscription "push" gibi görünse de aslında istemci-yönlü bir mekanizmadır. İstemci `Subscription` oluşturur, içine `MonitoredItem`'lar ekler. Server her bir monitored item'ı **SamplingInterval** ile örnekler (değeri okur), değişim filtresinden (deadband) geçenleri o item'ın **kuyruğuna** (QueueSize) koyar. Ayrı bir **PublishingInterval** zamanlayıcısı, biriken değişiklikleri bir `NotificationMessage`'a paketleyip istemcinin önceden gönderdiği `PublishRequest`'lere yanıt olarak iletir.
```
Değer → [SamplingInterval örnekler] → [DataChangeFilter/deadband] →
        [MonitoredItem Queue (QueueSize)] → [PublishingInterval paketler] →
        [NotificationMessage → istemci]
```
Kritik içgörü: **SamplingInterval ≠ PublishingInterval**. Server değeri hızlı örnekleyip (ör. 50ms) yavaş yayınlayabilir (ör. 1s); bu durumda 1 saniyede 20 örnek kuyruğa girer, QueueSize yeterliyse hepsi tek mesajda gelir (sıkıştırılmış geçmiş). Polling'de bu mümkün değildir: her okuma bir tur-zaman (round-trip) ister, kaçan değer kaçmıştır. Ayrıca subscription bir **KeepAlive** mekanizmasına sahiptir: değişim olmasa bile periyodik "hâlâ buradayım" mesajı gönderir — istemci bunu görmezse bağlantıyı kopuk sayar. Polling'de "sessizlik" hem "değişmedi" hem "öldü" anlamına gelebilir; ayırt edilemez.

**Quality (StatusCode) neden değerin kendisi kadar önemli:**
OPC UA'da her değer bir üçlüdür: `(Value, StatusCode, Timestamp)`. StatusCode 32-bitlik bir alandır; üst bitler Good/Uncertain/Bad sınıfını, alt bitler nedeni taşır (`Bad_NoCommunication`, `Uncertain_LastUsableValue`, `Good_LocalOverride` vb.). Bir değer `82.5` olabilir ama StatusCode `Bad_NoCommunication` ise o `82.5` anlamsızdır — bağlantı kopmadan önceki son değerdir. Sadece `Value`'yu gösterip StatusCode'u yok saymak, Not 2'deki motor aşırı ısınma vakasının tam nedenidir. Modbus'ta bu kavram protokol seviyesinde **yoktur**; kalite ancak "okuma başarılı oldu mu / timeout mu" şeklinde dolaylı türetilir. Bu, OPC UA'nın legacy üstündeki en büyük somut güvenlik avantajıdır.

**Backend "latest value cache" deseni neden zorunlu:**
```
İstemci bağlandığında ekranın TÜM değerlere ihtiyacı var, ama subscription
yalnızca BUNDAN SONRAKİ değişimleri gönderir. Cache olmadan:
  Bağlanan istemci, bir tag değişene kadar onu "--.-" görür (saatlerce olabilir).

Latest value cache (backend'de tutulan son değer haritası):
  Yeni istemci bağlanır → cache'ten anında FULL_UPDATE snapshot alır →
  ardından delta akışına geçer. Bu, "push" mimarisinin "pull-on-connect"
  ile birleştiği zorunlu noktadır.
```

**Saat senkronizasyonu ve trend bütünlüğü:**
Trend grafikleri ve yaşlılık hesapları zaman damgasına dayanır. PLC saati ile HMI/backend saati arasında kayma (clock skew) varsa: (1) yaşlılık negatif çıkabilir (gelecekten gelen timestamp → "0 saniye önce" görünür ama aslında bayat); (2) farklı kaynaklardan trend'ler hizalanmaz. Endüstriyel ortamda çözüm NTP (≈ms doğruluk) veya kritik motion/SoE senaryolarda PTP/IEEE-1588 (≈µs). Pratik kural: **yaşlılık hesabını tek bir saatle (backend) yap** — `age = backend_now − SourceTimestamp` yerine, mümkünse backend değeri aldığı andaki kendi saatini referans al; böylece PLC-backend skew yaşlılığı bozmaz.

## İlgili Konular

```
knowledge/hmi/architecture/
├── 01_hmi_patterns.md           → HMI genel mimarisi
├── 03_alarm_management.md       → Alarm verisi özel güncelleme gereksinimleri
└── 04_user_auth.md              → Yazma yetkisi bağlantı durumuna bağlı

knowledge/protocols/opc-ua/
├── 04_subscriptions.md          → OPC UA subscription detayları
└── 06_client_implementations.md → asyncua / node-opcua örnekleri

knowledge/protocols/modbus-tcp/
└── 05_client_implementations.md → pymodbus polling örnekleri
```
