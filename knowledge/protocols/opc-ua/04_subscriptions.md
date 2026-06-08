---
KONU        : OPC-UA Subscription Mekanizması
KATEGORİ    : protocols
ALT_KATEGORI: opc-ua
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://reference.opcfoundation.org/Core/Part4/v104/docs/5.12.1/"
    başlık: "OPC Foundation — UA Part 4: Services — MonitoredItem Model"
    güvenilirlik: resmi
  - url: "https://documentation.unified-automation.com/uagateway/1.5.7/html/L2UaSubscription.html"
    başlık: "Unified Automation — OPC UA Subscription Concept"
    güvenilirlik: topluluk
  - url: "https://www.rtautomation.com/rtas-blog/data-exchange-in-opc-ua/"
    başlık: "RT Automation — Data Exchange in OPC UA"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_architecture.md"
    ilişki: gerektirir
  - konu: "02_address_space.md"
    ilişki: gerektirir
  - konu: "06_client_implementations.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "OPC UA mimarisi (01_architecture.md)"
  - "Node ve Variable kavramları (02_address_space.md)"
ÇELİŞKİLER :
  - kaynak: "Sampling interval = 0 anlamı"
    konu: "Sampling interval sıfır ayarlandığında 'mümkün olan en hızlı' anlamına gelir"
    çözüm: >
      Bazı sunucular sampling interval=0'ı 'server minimum' olarak yorumlar.
      Bu, sunucuya aşırı yük bindirebilir (özellikle her döngüde örnekleme).
      Üretimde sampling interval her zaman açıkça belirtilmeli.
      CODESYS için önerilen minimum: 100ms (PLC task cycle time'a bağlı).
  - kaynak: "Publishing interval ile sampling interval karıştırma"
    konu: "İki farklı kavram sık karıştırılır"
    çözüm: >
      Sampling interval: Sunucunun veri kaynağını ne sıklıkta kontrol ettiği.
      Publishing interval: Sunucunun istemciye bildirim gönderdiği aralık.
      Sampling ≤ Publishing olabilir (sunucu örnekler, biriktirir, bir arada gönderir).
      Veya Sampling = Publishing = her değişimde tek gönderim.
---

## Özün Ne

OPC UA Subscription, istemcinin bir değişkenin değiştiğinde haberdar edilmesini sağlayan mekanizmadır. Polling'e (her X saniyede bir "değer ne?" sormak) alternatidir ve daha verimlidir: Sunucu yalnızca değer değiştiğinde gönderir, istemci sürekli sormak zorunda kalmaz. Bu model, hem ağ trafiğini azaltır hem de CPU yükünü düşürür hem de gerçek değişimlerin anında yakalanmasını sağlar. Subscription tasarımı — hangi değişkenlerin hangi aralıkla izleneceği, queue boyutu, publishing interval — doğru yapılmazsa hem istemci hem sunucu tarafında ciddi sorunlara yol açar.

## Nasıl Çalışır

### Kavramsal Yapı: Subscription → MonitoredItem

```
Bir Session (bağlantı oturumu) birden fazla Subscription içerebilir.
Bir Subscription birden fazla MonitoredItem içerebilir.

Session
├── Subscription_1 (Publishing Interval: 100ms)
│   ├── MonitoredItem_1: Motor1.Speed (Sampling: 100ms)
│   ├── MonitoredItem_2: Motor1.Current (Sampling: 100ms)
│   └── MonitoredItem_3: Motor1.FaultStatus (Sampling: 50ms)
│
├── Subscription_2 (Publishing Interval: 1000ms)
│   ├── MonitoredItem_4: Temperature.Zone1 (Sampling: 500ms)
│   ├── MonitoredItem_5: Temperature.Zone2 (Sampling: 500ms)
│   └── MonitoredItem_6: ProductionCount (Sampling: 1000ms)
│
└── Subscription_3 (Publishing Interval: 5000ms)
    └── MonitoredItem_7: MachineStatus.TotalRuntime (Sampling: 5000ms)
```

### Sampling vs Publishing — Temel Fark

```
Sampling Interval = Sunucu veri kaynağını ne sıklıkta kontrol eder?
Publishing Interval = Sunucu istemciye bildirim paketini ne sıklıkla gönderir?

Örnek — Sampling 100ms, Publishing 1000ms:

0ms   100ms  200ms  300ms  400ms  500ms  600ms  700ms  800ms  900ms  1000ms
│      │      │      │      │      │      │      │      │      │      │
│ ←── Sampling: Sunucu 10 kez kontrol eder ──────────────────────────── →│
│   S1     S2     S3     S4     S5     S6     S7     S8     S9     S10  │
│   (değişmedi) (değişti!) (değişmedi) (...) (değişti!) (...)           │
│                                                                        │
│ ←── Publishing: Sunucu bir kez gönderir (tüm birikmiş değişimler) ───►│
│   → Notification: S3 değeri, S5 değeri  (queue'daki değişimler)       │

Sonuç:
  - Sunucu 10 kez kontrol etti → Yalnızca 2 değişim buldu → 1 paketle gönderdi
  - İstemci: Saniyede 1 paket aldı ama içinde 2 anlık değer var
  - Ağ kullanımı: 10 polling yerine 1 paket = %90 azalma
```

### Zaman Çizelgesi

```
Zaman →───────────────────────────────────────────────────────────────

Sampling:  ↕   ↕   ↕   ↕   ↕   ↕   ↕   ↕   ↕   ↕  (100ms)
           │   │   │   │   │   │   │   │   │   │
           ○   ○   ●   ○   ○   ●   ○   ○   ○   ○
           (○=değişmedi ●=değişti → queue'ya alındı)
                   │               │
                   Q1              Q2

Publishing:  ────────────────────────────────►  (1000ms)
                                           │
                              Notification [Q1, Q2] → İstemciye gider

KeepAlive: Eğer hiç değişim yoksa, sunucu boş KeepAlive paketi gönderir
           → İstemci "sunucu hâlâ hayatta" bilgisini alır
```

### MonitoredItem Parametreleri

**Sampling Interval:**
```
Sunucunun veri kaynağını kontrol sıklığı.
-1       : Publishing interval'i kullan (varsayılan)
 0       : Sunucu minimumu (dikkatli kullan)
 100     : 100ms (mümkün olan en hızlı pratik değer çoğu CODESYS için)
 1000    : 1 saniye

CODESYS'te minimum: Task cycle time'a bağlı (ör. 10ms task → 10ms minimum)
```

**Queue Size:**
```
Her MonitoredItem'ın kaç değişimi saklayabileceği.
1       : Yalnızca en son değer (oldest-overwrite)
          → Publishing interval'den hızlı sampling'de eski değerler kaybolur
N       : N değer sakla → Publishing'de hepsi gönderilir
          → Hiçbir değer kaçmaz ama bellek kullanımı artar
          
Pratik seçim:
  Hızlı sinyaller (alarm, event): Queue=1 (en son yeterli)
  Değişim geçmişi önemli: Queue=5-10 (hiçbirini kaçırma)
```

**Discard Policy:**
```
Queue dolduğunda ne yapılır?
  DiscardOldest : En eski değer atılır, yenisi eklenir
  DiscardNewest : Yeni değer reddedilir
  
Endüstride: DiscardOldest yaygın (en güncel değer korunur)
```

**Dead Band Filter:**
```
Yalnızca belirli bir değişim eşiğini aşan değerler raporlanır.
Gürültülü analog sinyallerde gereksiz bildirim azaltır.

Absolute : Değerin mutlak değişimi > threshold
Percent  : Değerin yüzdesel değişimi > threshold%

Örnek:
  Motor.Speed = 1450 rpm
  DeadBand = Absolute, 10 rpm
  → Speed 1440-1460 aralığında ise bildirim gönderilmez
  → Speed 1461 rpm'e çıkınca bildirim gönderilir
```

### KeepAlive ve Lifetime

```
MaxKeepAliveCount:
  Bildirim yokken kaç publishing interval'de bir KeepAlive gönderilsin?
  Örnek: MaxKeepAlive=10, Publishing=1000ms
  → Hiç değer değişmezse her 10 saniyede bir KeepAlive paketi
  → İstemci sunucunun hayatta olduğunu bilir

LifetimeCount:
  İstemci kaç publishing interval boyunca Publish Request göndermezse
  subscription iptal edilsin?
  Örnek: Lifetime=300, Publishing=1000ms
  → 300 saniye boyunca istemci yanıt vermezse subscription silinir
  
Pratik oranlar:
  LifetimeCount ≥ 3 × MaxKeepAliveCount (OPC UA spec gereği)
```

## Pratikte Nasıl Kullanılır

### Subscription Tasarım Prensipleri

```
Prensip 1: Farklı hızlar için ayrı subscription
  ❌ Yanlış: Tüm değişkenler tek subscription'da (Publishing: 100ms)
             → Yavaş değişen sıcaklık değerleri de 100ms'de gönderilir → gereksiz trafik
  
  ✅ Doğru:
     Subscription_Fast  (100ms): Hız, akım, alarm
     Subscription_Medium (1s)  : Sıcaklık, basınç, sayaç
     Subscription_Slow  (10s)  : Çalışma süresi, enerji tüketimi

Prensip 2: Sampling interval ≥ veri kaynağı döngüsü
  CODESYS'te Task_Control 10ms çalışıyorsa
  MonitoredItem sampling interval minimum 10ms olmalı
  10ms'den kısa ayarlamak boşuna sunucu yükü

Prensip 3: Queue size'ı gerçek ihtiyaca göre ayarla
  Alarm/event: Queue=1 yeterli (en son durum önemli)
  Veri kaydı (historian): Queue=50+ (hiçbir değer kaçmamalı)
  HMI display: Queue=1 (görüntülenecek tek değer)

Prensip 4: DeadBand filter analog sinyallerde kullan
  gürültülü sensörlerde deadband olmadan saniyede yüzlerce gereksiz bildirim
  → CPU + ağ yük
```

### HMI için Subscription Tasarımı

```
HMI (Human Machine Interface) gereksinimleri:
  Operatör görüntüsünün 100ms'den hızlı yenilenmesi fark edilmez.
  Alarm durumu anlık yakalanmalı.
  Sayaçlar 1s yeterli.

Önerilen yapı:
  Subscription_Alarms  (Publishing: 100ms, Sampling: 100ms, Queue: 1)
    → Motor1.FaultStatus
    → EmergencyStop.Active
    → TemperatureAlarm.Active
    
  Subscription_Status  (Publishing: 500ms, Sampling: 500ms, Queue: 1)
    → Motor1.Speed
    → Motor1.Current
    → Temperature.Zone1
    
  Subscription_Slow    (Publishing: 5000ms, Sampling: 5000ms, Queue: 1)
    → ProductionCount.Today
    → Runtime.TotalHours
    → Energy.TodayKWh
```

## Örnekler

### Örnek 1: Python asyncua ile Subscription

```python
import asyncio
from asyncua import Client, ua

class SubscriptionHandler:
    """Subscription bildirimlerini işleyen handler sınıfı."""
    
    def __init__(self):
        self.received_data = {}
    
    def datachange_notification(self, node, val, data):
        """Değer değişiminde çağrılır — hızlı olmalı, block etmemeli!"""
        node_id = str(node.nodeid)
        self.received_data[node_id] = {
            'value': val,
            'timestamp': data.monitored_item.Value.SourceTimestamp
        }
        print(f"DataChange: {node} = {val}")
    
    def status_change_notification(self, status):
        """Subscription durumu değişince çağrılır."""
        print(f"Subscription status: {status}")

async def create_subscription():
    async with Client("opc.tcp://192.168.1.100:4840") as client:
        
        handler = SubscriptionHandler()
        
        # Subscription oluştur
        subscription = await client.create_subscription(
            period=500,          # Publishing interval: 500ms
            handler=handler
        )
        
        # MonitoredItem ekle
        nodes_to_monitor = [
            "ns=4;s=|var|CODESYS Control.Application.GVL_IO.rMotorSpeed",
            "ns=4;s=|var|CODESYS Control.Application.GVL_IO.rTemperature",
            "ns=4;s=|var|CODESYS Control.Application.GVL_Alarms.xMotorFault",
        ]
        
        monitored_items = []
        for node_id in nodes_to_monitor:
            node = client.get_node(node_id)
            handle = await subscription.subscribe_data_change(
                node,
                queuesize=1    # HMI için en son değer yeterli
            )
            monitored_items.append(handle)
        
        print("Subscription active. Monitoring values...")
        
        # 30 saniye izle
        await asyncio.sleep(30)
        
        # Temizlik
        await subscription.unsubscribe(monitored_items)
        await subscription.delete()

asyncio.run(create_subscription())
```

### Örnek 2: Gelişmiş Subscription — DeadBand + Queue

```python
async def advanced_subscription():
    async with Client("opc.tcp://192.168.1.100:4840") as client:
        
        handler = SubscriptionHandler()
        subscription = await client.create_subscription(
            period=1000,    # 1s publishing interval
            handler=handler
        )
        
        # Gürültülü analog sensör — DeadBand filter ile
        temp_node = client.get_node("ns=4;s=Temperature.Zone1")
        
        # MonitoredItemCreateRequest ile gelişmiş ayarlar
        monitoring_params = ua.MonitoringParameters()
        monitoring_params.SamplingInterval = 500    # 500ms örnekleme
        monitoring_params.QueueSize = 5            # 5 değer sakla
        monitoring_params.DiscardOldest = True
        
        # DeadBand filtresi
        filter_obj = ua.DataChangeFilter()
        filter_obj.Trigger = ua.DataChangeTrigger.StatusValue  # Değer değişince
        filter_obj.DeadbandType = ua.DeadbandType.Absolute    # Mutlak fark
        filter_obj.DeadbandValue = 1.0                        # ±1.0°C değişim eşiği
        monitoring_params.Filter = ua.ExtensionObject.from_params(filter_obj)
        
        item_request = ua.MonitoredItemCreateRequest()
        item_request.ItemToMonitor = ua.ReadValueId()
        item_request.ItemToMonitor.NodeId = temp_node.nodeid
        item_request.ItemToMonitor.AttributeId = ua.AttributeIds.Value
        item_request.MonitoringMode = ua.MonitoringMode.Reporting
        item_request.RequestedParameters = monitoring_params
        
        result = await subscription.create_monitored_items([item_request])
        print(f"MonitoredItem created: {result[0].StatusCode}")
        
        await asyncio.sleep(60)
        await subscription.delete()

asyncio.run(advanced_subscription())
```

### Örnek 3: Alarm/Event Subscription

```python
async def event_subscription():
    """OPC UA Event subscription — alarm yakalama."""
    
    async with Client("opc.tcp://192.168.1.100:4840") as client:
        
        class EventHandler:
            def event_notification(self, event):
                print(f"EVENT: {event.EventId}")
                print(f"  Message: {event.Message}")
                print(f"  Severity: {event.Severity}")
                print(f"  Time: {event.Time}")
                print(f"  SourceName: {event.SourceName}")
        
        handler = EventHandler()
        subscription = await client.create_subscription(500, handler)
        
        # Server'ın event node'una abone ol
        server_node = client.get_node(ua.ObjectIds.Server)
        
        # Tüm BaseEventType olaylarını izle
        await subscription.subscribe_events(
            server_node,
            ua.ObjectIds.BaseEventType
        )
        
        print("Event subscription active. Waiting for alarms...")
        await asyncio.sleep(300)    # 5 dakika izle
        await subscription.delete()

asyncio.run(event_subscription())
```

## Sık Yapılan Hatalar

### Hata 1: Handler'da Ağır İşlem Yapmak

```python
# ❌ YANLIŞ — Handler'da database yazma, ağ çağrısı
class BadHandler:
    def datachange_notification(self, node, val, data):
        save_to_database(val)       # Bloklanabilir → Subscription bloke
        send_email_alert(val)       # Ağ işlemi → Bloklanabilir
        time.sleep(1)               # Kesinlikle YAPMA

# ✅ DOĞRU — Değeri queue'ya at, ayrı thread işlesin
import queue
class GoodHandler:
    def __init__(self):
        self.data_queue = queue.Queue(maxsize=1000)
    
    def datachange_notification(self, node, val, data):
        # Sadece queue'ya at — anında döner
        try:
            self.data_queue.put_nowait((str(node.nodeid), val))
        except queue.Full:
            pass  # Queue doldu → en eski at (veya log)
```

### Hata 2: Sampling Interval'ı Sıfır Bırakmak

```
Sampling interval = 0 → "Mümkün olan en hızlı"
CODESYS PLC'de bu = her scan döngüsü = 10ms

100 MonitoredItem × 10ms sampling = 10.000 örnekleme/saniye
Gereksiz sunucu yükü, gereksiz ağ trafiği.

Çözüm: Sampling interval'ı her zaman açıkça belirt.
         HMI: 500ms-1000ms yeterli
         Alarm: 100ms-200ms
         Historian: Gerçek ihtiyaca göre
```

### Hata 3: Subscription'ı Silmeden Bağlantıyı Kesmek

```python
# ❌ YANLIŞ — Subscription silinmeden disconnect
async def bad_client():
    client = Client("opc.tcp://...")
    await client.connect()
    sub = await client.create_subscription(500, handler)
    await sub.subscribe_data_change(some_node)
    # ... işlem ...
    await client.disconnect()  # Sub silinmedi → Sunucuda hayalet subscription

# ✅ DOĞRU — Context manager veya explicit cleanup
async def good_client():
    async with Client("opc.tcp://...") as client:
        sub = await client.create_subscription(500, handler)
        try:
            await sub.subscribe_data_change(some_node)
            await asyncio.sleep(60)
        finally:
            await sub.delete()  # Her zaman temizle
```

### Hata 4: Çok Fazla Subscription Oluşturmak

```
Bazı PLC sunucuları 10-20 eş zamanlı subscription sınırına sahip.
Her yeniden bağlantıda yeni subscription oluşturan client → Sunucu kapasitesini doldurur.

Çözüm:
  1. Mümkünse tek subscription içinde tüm MonitoredItem'ları topla.
  2. Bağlantı kesilirse önce eski subscription'ları temizle, sonra yeni kur.
  3. Subscription count'u monitor et.
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**Subscription Kullan:**
- Değişkeni sürekli izlemek istediğinde (HMI, dashboard, alarm)
- Ağ trafiğini minimize etmek istediğinde
- Değer ne zaman değişeceğini öngöremediğinde
- Anlık değişimleri yakalamak kritikse

**Read (Polling) Kullan:**
- Tek seferlik değer okumada (başlatma, raporlama)
- Belirli bir anda değere ihtiyaç duyulduğunda
- Subscription overhead istemediğinde (basit script)
- Çok nadir değişen değerler için

## Gerçek Proje Notları

**Not 1 — Handler'da Bloklanmanın Keşfi**  
SCADA bağlantısı bazen subscription bildirimleri almayı durduruyordu. Araştırma: Handler fonksiyonu içinde DB yazma işlemi zaman zaman 200ms sürüyordu; bu süre boyunca OPC UA subscription thread bloklandı. Queue mekanizmasına geçildi; handler anında döner, ayrı thread DB'ye yazar. Sorun çözüldü.

**Not 2 — Sıfır Sampling Interval ile Sunucu Çökmesi**  
Raspberry Pi üzerinde CODESYS, 200 MonitoredItem ile sampling=0 ayarıyla başlatıldı. CPU %95'e çıktı, OPC UA server yanıt vermez hale geldi. Sampling interval'lar 500ms'ye ayarlandı, CPU %15'e indi. Öğrenilen: Sıfır sampling, sınırlı donanımda ciddi risk.

**Not 3 — Alarm Queue Tasarımı**  
Üretim makinesinde alarm subscription queue=1 ile başlangıçta kuruldu. Hızlı alarm-reset-alarm döngüsünde bazı alarm geçişleri kaçırıldı. Queue=5'e çıkarıldı; alarm geçişleri eksiksiz yakalandı. Queue size, alarm sayacını etkiliyor: Hiçbir alarm geçişi kaçırılamayacaksa Queue büyük tutulmalı.

## İlgili Konular

```
knowledge/protocols/opc-ua/
├── 01_architecture.md           → Session ve Subscription ilişkisi
├── 02_address_space.md          → MonitoredItem'ın izlediği NodeId
├── 05_codesys_server_config.md  → Sunucu tarafı subscription parametreleri
└── 06_client_implementations.md → Node-RED, Python, .NET subscription örnekleri
```
