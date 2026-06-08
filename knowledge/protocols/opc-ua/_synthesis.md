---
KONU        : OPC UA — Sentez
KATEGORİ    : protocols
ALT_KATEGORI: opc-ua
SEVİYE      : Orta-İleri
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "knowledge/protocols/opc-ua/01_architecture.md"
    başlık: "OPC UA Mimari Yapısı"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/opc-ua/02_address_space.md"
    başlık: "OPC UA Adres Uzayı Tasarımı"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/opc-ua/03_security.md"
    başlık: "OPC UA Güvenlik Modeli"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/opc-ua/04_subscriptions.md"
    başlık: "OPC UA Subscription Mekanizması"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/opc-ua/05_codesys_server_config.md"
    başlık: "CODESYS OPC UA Sunucu Detaylı Konfigürasyonu"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/opc-ua/06_client_implementations.md"
    başlık: "OPC UA İstemci Implementasyonları"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/codesys/fundamentals/_synthesis.md"
    ilişki: gerektirir (CODESYS proje yapısı ve runtime temelleri)
  - konu: "knowledge/codesys/networking/01_opcua_server.md"
    ilişki: tamamlar
  - konu: "knowledge/protocols/modbus/"
    ilişki: karşılaştırma
ÖNKOŞUL     :
  - "Temel ağ kavramları: TCP/IP, port, istemci-sunucu modeli"
  - "CODESYS proje yapısı (fundamentals/02_project_structure.md)"
  - "Temel PKI/sertifika kavramları faydalı ama zorunlu değil"
ÇELİŞKİLER :
  - kaynak: "05_codesys_server_config.md vs 02_address_space.md — Namespace index"
    konu: "NodeId'de ns=4 hardcode etmek kırılgan; runtime değişiminde tüm tag'ler bozulur"
    çözüm: >
      Her zaman get_namespace_index(URI) ile dinamik al. CODESYS URI sabittir:
      "http://www.3s-software.com/schemas/Codesys-V3". Index kuruluma göre değişir.
  - kaynak: "03_security.md — SP17 yükseltme riski"
    konu: "CODESYS SP17+ sonrası anonymous erişim varsayılan kapalı; mevcut istemciler kesilir"
    çözüm: >
      Runtime yükseltmeden önce release notes oku. SP17 geçişinde tüm OPC UA
      istemcilerinin kullanıcı kimlik doğrulaması desteklemesi gerekir.
  - kaynak: "04_subscriptions.md — Sampling interval sıfır"
    konu: "Sampling=0 'mümkün olan en hızlı' anlamına gelir; sınırlı donanımda CPU'yu eritir"
    çözüm: >
      Sampling interval her zaman açıkça belirt. CODESYS için pratik minimum 100ms.
      MinSamplingInterval=100 ile CODESYSControl.cfg'de sunucu tarafında da sınırla.
---

## Özün Ne

Bu sentez, "OPC UA'yı teoriden CODESYS server kurulumuna ve Python/JS client kullanımına kadar bir bütün olarak nasıl anlarım?" sorusuna yanıt verir. Altı belge bir zincir oluşturur: Mimari (nedir, neden), Adres Uzayı (veri nasıl temsil edilir), Güvenlik (kimler erişebilir, nasıl şifrelenir), Subscription (değişimler nasıl iletilir), CODESYS Server Config (sunucu nasıl kurulur), Client Implementasyonları (Python/JS/.NET ile nasıl bağlanılır). Bu zincir anlaşılmadan parçaları doğru uygulamak mümkün değildir; anlaşılınca endüstriyel entegrasyonların büyük çoğunluğu çözümlenir.

## Nasıl Çalışır

### Altı Belgenin Zihin Haritası

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     OPC UA ZİHİN HARİTASI                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  01_architecture.md — NEDEN ve NE                                        │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  OPC UA = Platform bağımsız + Güvenli + Anlamlı endüstri protokolü│  │
│  │  • IEC 62541 (OPC Foundation standardı)                           │  │
│  │  • OPC Classic (COM/DCOM, yalnızca Windows) → OPC UA              │  │
│  │  • Transport: opc.tcp://IP:4840 (tek port, güvenlik duvarı dostu) │  │
│  │  • Servisler: Read, Write, Browse, Subscribe, Call Method          │  │
│  │  • PubSub modu: MQTT broker üzerinden çok-noktaya                 │  │
│  └──────────────────────────────┬────────────────────────────────────┘  │
│                                 │ Veriler nerede tutulur?               │
│                                 ▼                                        │
│  02_address_space.md — VERİ MODELİ                                       │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Address Space = Sunucunun hiyerarşik bilgi modeli                 │  │
│  │  • 8 Node sınıfı: Object, Variable, Method, DataType...            │  │
│  │  • NodeId: ns=4;s=|var|Runtime.Application.GVL_IO.xMotorRun       │  │
│  │  • Namespace: ns=0 (OPC UA std), ns=4 (CODESYS uygulama)          │  │
│  │  • İyi tasarım: Hiyerarşik (Device→Unit→Measurement→Value)        │  │
│  │  • Kötü tasarım: Flat (300 değişken aynı seviyede)                 │  │
│  └──────────────────────────────┬────────────────────────────────────┘  │
│                                 │ Bağlantı nasıl korunur?              │
│                                 ▼                                        │
│  03_security.md — GÜVENLİK                                               │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  3 katman: Mesaj → Uygulama → Kullanıcı                           │  │
│  │  • SecurityMode: None | Sign | SignAndEncrypt (üretim: daima 3.)   │  │
│  │  • SecurityPolicy: Basic256Sha256 / Aes256-Sha256-RsaPss           │  │
│  │  • PKI: rejected/ → trusted/certs/ (ilk bağlantı ritüeli)         │  │
│  │  • CODESYS SP17+: anonymous varsayılan kapalı                      │  │
│  └──────────────────────────────┬────────────────────────────────────┘  │
│                                 │ Değişimler nasıl iletilir?           │
│                                 ▼                                        │
│  04_subscriptions.md — VERİ AKIŞI                                        │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Subscription > MonitoredItem (polling'e karşı push modeli)        │  │
│  │  • Sampling Interval: Sunucu veri kaynağını ne sıklıkta kontrol   │  │
│  │  • Publishing Interval: Sunucu istemciye ne sıklıkta bildirir     │  │
│  │  • Queue Size: Kaç değişim biriktirilir                            │  │
│  │  • DeadBand Filter: Gürültülü analog sinyali filtrele             │  │
│  │  • KeepAlive: Bildirim yoksa sunucu "hâlâ buradayım" der          │  │
│  └──────────────────────────────┬────────────────────────────────────┘  │
│                                 │ CODESYS'te nasıl kurulur?            │
│                                 ▼                                        │
│  05_codesys_server_config.md — SUNUCU KURULUMU                           │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  2 yöntem: Symbol Configuration (hızlı) vs Comm.Manager (zengin)  │  │
│  │  • Symbol Config: GVL değişkenleri → OPC UA'ya aç, access belirle │  │
│  │  • NodeId formatı: ns=4;s=|var|[RuntimeName].[App].[GVL].[Var]   │  │
│  │  • CODESYSControl.cfg: MaxSessions, MinSamplingInterval, güvenlik │  │
│  │  • PKI klasörü: /var/opt/codesys/PlcLogic/Application/pki/        │  │
│  └──────────────────────────────┬────────────────────────────────────┘  │
│                                 │ Client nasıl bağlanır?               │
│                                 ▼                                        │
│  06_client_implementations.md — İSTEMCİ KODLARI                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Python asyncua / Node.js node-opcua / .NET OPC Foundation SDK    │  │
│  │  • get_namespace_index(URI) → dinamik ns al                        │  │
│  │  • read_value / write_value / create_subscription                  │  │
│  │  • Güvenli: set_security(Basic256Sha256) + kullanıcı kimliği       │  │
│  │  • Handler: queue + ayrı thread (block etmemeli!)                  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Bütünsel Mental Model: Bir Değişkenin Yolculuğu

```
PLC Döngüsü (10ms)
    │
    │ CODESYS Task_Control çalışır
    │ GVL_IO.rMotorSpeed = 1452.3 (REAL)
    │
    ▼
CODESYS OPC UA Server (05_codesys_server_config.md)
    │ Symbol Configuration: rMotorSpeed → ReadOnly → OPC UA'ya açık
    │ NodeId: ns=4;s=|var|CODESYS Control Linux ARM64 SL.Application.GVL_IO.rMotorSpeed
    │ Address Space'teki yeri: Objects/DeviceSet/[Runtime]/Application/GVL_IO/rMotorSpeed
    │
    ▼ (04_subscriptions.md)
Subscription Mekanizması
    │ MonitoredItem: Sampling=100ms, Queue=1, DeadBand=5rpm
    │ Sunucu 100ms'de bir kontrol eder
    │ Değer 5rpm'den fazla değiştiyse queue'ya alır
    │ Publishing Interval=500ms: Her 500ms'de birikenleri pakete koyar
    │
    ▼ (03_security.md)
Güvenlik Katmanı
    │ SecurityPolicy: Basic256Sha256
    │ MessageSecurityMode: SignAndEncrypt
    │ İstemci sertifikası: trusted/certs/ listesinde
    │ Kullanıcı: opc_scada rolü (Engineer)
    │ Mesaj şifrelenir → TCP'ye teslim
    │
    ▼ opc.tcp://192.168.1.100:4840
Ağ (TCP, port 4840)
    │
    ▼ (06_client_implementations.md)
Python asyncua Client
    │ handler.datachange_notification() çağrılır
    │ val = 1452.3, timestamp = 2026-06-08T10:22:15Z
    │ queue.put_nowait({node, val, timestamp})
    │ Ayrı asyncio task InfluxDB/DB'ye yazar
    │
    ▼
Dashboard / SCADA / MES
```

### Katmanlı Mimari: OPC UA'nın Endüstriyel Rolü

```
ERP / Bulut (SAP, Azure IoT)
    ▲
    │  REST / MQTT
    │
MES (Üretim Yönetimi)
    ▲
    │  OPC UA (Client → SCADA OPC UA Server)
    │
SCADA / Historian (Wonderware, Ignition, Node-RED)
    ▲
    │  OPC UA Client → opc.tcp://PLC-IP:4840
    │
OPC UA Server — CODESYS (veya Siemens, B&R, Beckhoff)
    │  Symbol Configuration → GVL değişkenleri dışa açılmış
    │  Güvenlik: Basic256Sha256 + SignAndEncrypt
    │  Adres Uzayı: Objects/DeviceSet/.../Application/GVL_IO/...
    ▲
    │  EtherCAT / PROFINET / Modbus RTU (gerçek zamanlı alan verisi)
    │
PLC / DCS / I/O Modülleri
    ▲
    │  Kablo / Fieldbus
    │
Sensör / Aktüatör
```

## Hızlı Referans Tabloları

### A. Security Policy ve Mode Matrisi

| SecurityPolicy | İmzalama | Şifreleme | Durum | Ne Zaman |
|---|---|---|---|---|
| `None` | — | — | Kaçın | Yalnızca izole geliştirme LAN |
| `Basic128Rsa15` | RSA-SHA1 | AES-128 | Eskimiş | Kullanma |
| `Basic256` | RSA-SHA1 | AES-256 | Eskimiş | Kullanma |
| `Basic256Sha256` | RSA-SHA256 | AES-256 | Güvenli | Üretim standardı |
| `Aes128-Sha256-RsaOaep` | RSA-SHA256 | AES-128 | Modern, hızlı | Kaynak kısıtlı PLC |
| `Aes256-Sha256-RsaPss` | RSA-PSS-SHA256 | AES-256 | En güçlü | Yüksek güvenlik gereksinimi |

| MessageSecurityMode | İmzalama | Şifreleme | Üretimde |
|---|---|---|---|
| `None` | ✗ | ✗ | Asla |
| `Sign` | ✓ | ✗ | Yalnızca bütünlük gerekiyorsa |
| `SignAndEncrypt` | ✓ | ✓ | Her zaman bu |

### B. Node Sınıfları

| Sınıf | Ne Temsil Eder | Örnekler | Alt Node |
|---|---|---|---|
| Object | Fiziksel/mantıksal varlık | Motor1, ConveyorUnit | Var |
| Variable (DataVariable) | Proses değeri | Speed, Temperature, xRun | Var |
| Variable (Property) | Metadata/özellik | Manufacturer, SerialNumber | Yok |
| Method | Çağrılabilir fonksiyon | Reset(), StartRecipe() | — |
| ObjectType | Object şablonu (sınıf) | MotorType, ConveyorType | — |
| VariableType | Variable şablonu | — | — |
| DataType | Veri tipi tanımı | MotorStatus (struct), MotorState (enum) | — |
| ReferenceType | İlişki türü | HasComponent, HasProperty | — |

### C. Subscription Parametreleri

| Parametre | Açıklama | HMI | Alarm | Historian |
|---|---|---|---|---|
| Publishing Interval | İstemciye bildirim gönderme sıklığı | 500ms | 100ms | 1000ms |
| Sampling Interval | Veri kaynağını kontrol sıklığı | 500ms | 100ms | 500ms |
| Queue Size | Biriktirilecek değer sayısı | 1 | 5–10 | 50+ |
| DiscardOldest | Queue dolunca en eskiyi at | True | True | False |
| DeadBand (Absolute) | Değişim eşiği (analog filtre) | — | — | Sinyal gürültüsüne göre |
| MaxKeepAliveCount | Bildirim yoksa kaçta bir KeepAlive | 10 | 5 | 20 |
| LifetimeCount | İstemci yanıt vermezse subscription iptal | 100 | 30 | 300 |

### D. CODESYS Server → Client Mimari Konsolide

| Konu | CODESYS Sunucu Tarafı | Client Tarafı |
|---|---|---|
| Değişken açma | Symbol Configuration → değişkeni işaretle | NodeId: `ns=4;s=\|var\|...` |
| Namespace | `http://www.3s-software.com/schemas/Codesys-V3` | `get_namespace_index(URI)` |
| Güvenlik | `[CmpOPCUAServer] MinSecurityMode=2` | `set_security(Basic256Sha256)` |
| Sertifika güveni | `rejected/` → `trusted/certs/` | Sunucu sertifikasını trust |
| Session limit | `MaxSessions=20` | Context manager ile kapat |
| Subscription limit | `MaxSubscriptions=500` | `subscription.delete()` çağır |
| Sampling hızı | `MinSamplingInterval=100` | `SamplingInterval=100+` belirt |
| Port | `ServerPort=4840` | `opc.tcp://IP:4840` |
| Erişim hakları | Symbol Config → Read / ReadWrite | Yazma için WriteValue, doğru kullanıcı rol |

### E. Kütüphane Seçim Tablosu

| Kriter | Python asyncua | Node.js node-opcua | .NET OPC Fnd SDK |
|---|---|---|---|
| API kolaylığı | En kolay | Orta | Karmaşık |
| Güvenlik (TLS) | Var | Var | Tam |
| Async desteği | Tam (async/await) | Tam | Var |
| Performans | Orta | Yüksek | En yüksek |
| OPC Foundation sertifikasyon | Hayır | Hayır | Evet |
| En iyi kullanım | Script, IoT, data analiz | Web HMI, Node-RED | Enterprise, WinForms |

## Pratikte Nasıl Kullanılır

### CODESYS OPC UA Kurulum Kontrol Listesi

```
SUNUCU TARAF (CODESYS IDE + Runtime)

□ 1. Runtime OPC UA lisansı kontrol (CODESYSControl.cfg → [CmpOPCUAServer])
□ 2. Application → Add Object → Symbol Configuration
□ 3. Her değişkene erişim seviyesi ata:
     - Kontrol çıkışları (xStartCmd): ReadWrite
     - Geri bildirimler (xMotorFB): Read
     - Dahili/debug değişkenler: İşaretleme (açma)
□ 4. Build → Download → (Online Start)
□ 5. UaExpert ile doğrula:
     - opc.tcp://IP:4840 → Bağlan
     - Objects/DeviceSet/ altında değişkenler görünüyor mu?
     - NodeId'leri not al

GÜVENLİK KURULUMU (SP17+ için zorunlu)

□ 6. CODESYS IDE → View → Security Screen → CmpOPCUAServer
□ 7. Create Certificate → Org/CN/Validity(10 yıl)/KeySize(2048+) → OK
□ 8. CODESYSControl.cfg'yi yapılandır:
     [CmpOPCUAServer]
     AllowAnonymous=0
     MinSecurityMode=2   ← SignAndEncrypt zorunlu
     MaxSessions=20
     MinSamplingInterval=100
□ 9. Runtime restart: sudo systemctl restart codesyscontrol
□ 10. İstemci sertifikasını trusted/certs/'e kopyala (ilk bağlantıdan sonra)

CLIENT TARAF (Python asyncua örneği)

□ 11. pip install asyncua[crypto]
□ 12. Namespace URI'dan index al (hardcode etme!)
□ 13. Context manager kullan: async with Client(...) as client
□ 14. Subscription için ayrı handler + queue kullan
□ 15. Reconnect mekanizması ekle (üretimde zorunlu)
```

### Gerçek Entegrasyon Senaryosu

**Görev**: CODESYS PLC'deki motor hızı ve alarm durumu, Python script ile 500ms'de bir izlensin; değer değişince InfluxDB'ye yazılsın.

```
ADIM 1 — CODESYS Symbol Configuration (Belge 5)
  GVL_IO.rMotorSpeed   → ReadOnly  → OPC UA'ya aç
  GVL_Alarms.xAnyAlarm → ReadOnly  → OPC UA'ya aç
  Build → Download

ADIM 2 — Güvenlik (Belge 3)
  Security Screen → Sertifika oluştur
  AllowAnonymous=0, MinSecurityMode=2
  
ADIM 3 — Python Client (Belge 6)
  ns = await client.get_namespace_index("http://www.3s-software.com/schemas/Codesys-V3")
  # NodeId'yi CODESYS runtime adından oluştur
  speed_node = client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rMotorSpeed")
  alarm_node = client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_Alarms.xAnyAlarm")

ADIM 4 — Subscription Tasarımı (Belge 4)
  subscription = await client.create_subscription(period=500, handler=handler)
  # Motor hızı: DeadBand 5 rpm (gürültü filtresi)
  # Alarm: Queue=5 (hiçbir geçiş kaçmasın)

ADIM 5 — Handler → InfluxDB
  class DataHandler:
      def datachange_notification(self, node, val, data):
          self.queue.put_nowait(...)   # Hızlı dön!
  # Ayrı asyncio task: queue'dan oku → InfluxDB yaz

ADIM 6 — Reconnect (Üretim zorunluluğu)
  while True:
      try:
          async with Client(...) as client:
              # subscription kur, izle
      except Exception:
          await asyncio.sleep(5)   # Yeniden bağlan
```

## Sık Yapılan Hatalar

### Hata 1: None Security Mode Üretime Taşımak

```
Senaryo: Test için None mode kuruldu → Kolaylık sağladı → Proje üretime geçti.
Etki   : Tüm OPC UA trafiği düz metin. Motor komutları ağda okunabilir/değiştirilebilir.
Önlem  : Üretim dağıtım kontrol listesinde "MinSecurityMode=2" zorunlu madde.
Düzelt : AllowAnonymous=0, MinSecurityMode=2 → runtime restart → istemcileri güncelle.
```

### Hata 2: Namespace Index Hardcode Etmek

```python
# Yanlış — ns=4 başka kurulumda farklı olabilir:
node = client.get_node("ns=4;s=|var|CODESYS Control.Application.GVL_IO.xMotorRun")

# Doğru — her bağlantıda URI'dan al, bir kez cache'le:
ns = await client.get_namespace_index("http://www.3s-software.com/schemas/Codesys-V3")
node = client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun")
```

### Hata 3: Subscription Handler'da Ağır İşlem

```python
# Yanlış — handler içinde database/ağ çağrısı subscription'ı bloklar:
def datachange_notification(self, node, val, data):
    database.write(val)   # 200ms sürebilir → OPC UA thread bloke!

# Doğru — queue'ya at, ayrı thread işlesin:
def datachange_notification(self, node, val, data):
    self.queue.put_nowait((node, val))   # Anında döner
```

### Hata 4: Flat Adres Uzayı Tasarımı

```
Yanlış: Objects/Machine/ altında 300 değişken düz liste
  → SCADA entegratörü hangi tag'in ne olduğunu anlayamaz
  → Her şey hardcoded NodeId gerektirir
  → OPC UA'yı pahalı Modbus'a dönüştürür

Doğru: Objects/PackagingLine1/ConveyorUnit/Status/IsRunning
  → Müşteri UaExpert ile sistemi kendi başına keşfeder
  → SCADA entegrasyonu kısa sürer
```

### Hata 5: Symbol Configuration Build Sonrası Download Unutmak

```
Değişken eklendi → Symbol Configuration'da işaretlendi → Build yapıldı.
Ama Download yapılmadı.
Sonuç: OPC UA'da eski adres uzayı görünür, yeni değişkenler yok.
Kural: Symbol Configuration her değişikliği Build + Download gerektirir.
```

### Hata 6: SP17 Yükseltmesinde Tüm Bağlantıların Kesilmesi

```
Runtime SP17'ye yükseltildi → Anonymous kapatıldı → SCADA bağlanamıyor.
Acil geçici çözüm: AllowAnonymous=1
Kalıcı çözüm: Tüm istemcilere kullanıcı adı/şifre yapılandır.
Önlem: Runtime güncellemesinden önce release notes oku; OPC UA değişikliklerini listele.
```

### Hata 7: Subscription Silinmeden Bağlantı Kesmek

```python
# Yanlış — sunucuda hayalet subscription birikir, MaxSubscriptions dolar:
await client.disconnect()   # subscription silinmedi

# Doğru:
try:
    await subscription.unsubscribe(handles)
    await subscription.delete()
finally:
    await client.disconnect()
```

## Ne Zaman ...

### OPC UA Ne Zaman Doğru Seçimdir?

```
OPC UA seç:
  ✓ PLC → SCADA, MES, ERP katmanları arası veri iletimi
  ✓ Platform bağımsız (Linux PLC → Windows SCADA → Python script)
  ✓ Güvenlik gereksinimi var (NIS2, ISO 27001 uyumluluk)
  ✓ Semantik veri modeli gerekiyor (makinenin kendini tanımlaması)
  ✓ Birden fazla istemci aynı anda aynı veriye erişecek
  ✓ Method çağrısı gerekiyor (StartRecipe, Reset, Calibrate)
  ✓ Companion Specification uyumluluğu (robotik, CNC, ilaç)

OPC UA seçme:
  ✗ Gerçek zamanlı motion control (EtherCAT/PROFINET kullan)
  ✗ Yüksek hız I/O (alt 1ms döngü — EtherCAT/CANopen kullan)
  ✗ Çok kısıtlı gömülü cihaz (Modbus RTU daha az kaynak tüketir)
  ✗ Yalnızca bir istemci, basit veri, hızlı prototip (MQTT veya Modbus TCP yeterli)
```

### Symbol Configuration Ne Zaman Yeterlidir?

```
Symbol Configuration yeterli:
  ✓ GVL değişkenleri OPC UA'ya açılacak (standart senaryo)
  ✓ Tek application, standart namespace
  ✓ SCADA/HMI entegrasyonu (okuma + yazma komutları)
  ✓ Hızlı kurulum önceliği

Communication Manager + OPC UA Server gerekli:
  ✓ Custom namespace URI (müşteri özel)
  ✓ Method tanımı (StartRecipe, Reset)
  ✓ Companion Specification uyumu
  ✓ Birden fazla application'ın koordinasyonu
  ✓ Zengin bilgi modeli (ObjectType, hiyerarşi)
```

### Sampling Interval Ne Seçilmeli?

```
Sinyal Türü               Sampling    Publishing   Queue
──────────────────────────────────────────────────────────
Acil stop, alarm          100ms       100ms        5–10
Motor durumu (bool)       100ms       500ms        1
Hız, akım (hızlı analog) 100ms       500ms        1–5
Sıcaklık, basınç          500ms       1000ms       1
Sayaç, enerji             1000ms      5000ms       1
Toplam çalışma süresi     5000ms      10000ms      1
```

## Gerçek Proje Notları

**Not 1 — NodeId Değişikliğinin SCADA Felaketi**
Runtime Windows'tan Linux ARM64'e taşındı. "CODESYS Control Win V3 x64" → "CODESYS Control Linux ARM64 SL" runtime adı değişti; 500 SCADA tag'inin tamamı güncellenmesi gerekti — 2 günlük acı iş. Sonraki projelerden itibaren Communication Manager ile custom namespace URI kullanılıyor. Runtime değişse bile NodeId'ler sabit kalıyor.

**Not 2 — SP17 Güncellemesi Sonrası Üretim Durması**
Bir Cuma akşamı runtime güncellemesi yapıldı. SP17 ile anonymous erişim kapandı. SCADA sistemi bağlantısı kesildi; üretim izleme gitti. Acil geçici çözüm AllowAnonymous=1; sonraki iki haftada tüm istemciler kullanıcı kimliğine geçirildi. Bu deneyimden sonra kural: Runtime güncellemesi = release notes okunması + test ortamında uygulama + mesai saatinde geçiş.

**Not 3 — Sertifika Trusted Sorunuyla Geçen 4 Saat**
İlk OPC UA projesinde istemci bağlanamıyordu; hata: "BadSecurityChecksFailed" — anlamsız bir mesaj. Asıl sorun: Sunucunun rejected/ klasöründe biriken istemci sertifikaları. trusted/certs/'e taşınınca anında bağlandı. Bugün kurulum sırasında Trust yapılandırması ilk adım olarak kontrol listesinde.

**Not 4 — Handler'da Bloklanmanın Bulunması**
SCADA bağlantısı zaman zaman subscription bildirimlerini almayı durduruyordu — değerler donuyordu. Araştırma: Handler içinde database yazma zaman zaman 200ms sürüyordu. Bu süre boyunca asyncua subscription thread bloklanıyordu. Queue + ayrı asyncio task'a geçildi; handler nanosaniyede dönüyor, database yazmayı task halediyor. Sorun tamamen çözüldü.

**Not 5 — Sıfır Sampling ile Raspberry Pi Çökmesi**
Raspberry Pi üzerinde CODESYS, 200 MonitoredItem ile sampling=0 (mümkün olan en hızlı) kuruldu. CPU %95'e çıktı, OPC UA server yanıt vermez oldu. MinSamplingInterval=500 ile CODESYSControl.cfg'de kısıtlandı; client sampling 500ms'ye ayarlandı; CPU %12'ye indi. Öğrenilen: Sampling interval her zaman açıkça belirt, sıfır bırakma.

**Not 6 — Companion Specification ile Entegrasyon Süresi %70 Kısaldı**
Robot OEM'i OPC 40010 (Robotics Companion Spec) uyumlu server sundu; SCADA istemcisi aynı spec'i destekliyordu. Custom tag eşlemesi yazmak yerine standartta tanımlı node'lar direkt kullanıldı. Entegrasyon 2 günden 4 saate indi. Companion spec uyumluluğu şimdi satın alma şartnamesinde standart madde.

**Not 7 — PubSub ile 50 PLC Yönetimi**
50 PLC'nin her birini ayrı OPC UA client/server olarak yönetmek operasyonel yük oluşturuyordu. OPC UA PubSub (MQTT transport) eklendikten sonra tüm PLC'ler broker'a yayınladı, SCADA tek noktadan abone oldu. 50 farklı bağlantı yönetimi yerine 1 broker bağlantısı — bakım süresi %80 azaldı.

## İlgili Konular

```
knowledge/protocols/opc-ua/               ← Şu an buradasınız
├── 01_architecture.md                    → Mimari ve protokol karşılaştırmaları
├── 02_address_space.md                   → Node sınıfları ve tasarım desenleri
├── 03_security.md                        → PKI, sertifika, roller detayı
├── 04_subscriptions.md                   → Subscription/MonitoredItem derinlemesine
├── 05_codesys_server_config.md           → CODESYS yapılandırma tüm parametreler
├── 06_client_implementations.md          → Python/JS/.NET kod örnekleri
└── _synthesis.md (bu belge)

Önkoşul (okunmadan gelindiyse):
knowledge/codesys/fundamentals/
├── 01_runtime_architecture.md            → CODESYS runtime nedir
├── 02_project_structure.md              → GVL, Application, Task yapısı
└── _synthesis.md

CODESYS OPC UA hızlı kurulum:
knowledge/codesys/networking/
└── 01_opcua_server.md                    → Adım adım kurulum rehberi

Tamamlayıcı protokoller:
knowledge/protocols/
└── modbus/                               → Legacy entegrasyon, basit senaryolar

Ağ altyapısı:
knowledge/networking/
└── ethercat/                             → Gerçek zamanlı alan ağı (OPC UA'nın altı)

Araçlar:
  UaExpert    → Ücretsiz OPC UA client/browser — ilk adres uzayı keşfi için şart
  UA Modeler  → Grafik bilgi modeli tasarım aracı (custom ObjectType için)
  Wireshark   → OPC UA trafik analizi (private key ile şifreli trafiği çöz)
  asyncua     → pip install asyncua[crypto] — Python OPC UA istemcisi
  node-opcua  → npm install node-opcua — Node.js OPC UA istemcisi
```
