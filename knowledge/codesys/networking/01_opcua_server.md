---
KONU        : CODESYS OPC UA Sunucu Kurulumu
KATEGORİ    : codesys
ALT_KATEGORI: networking
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Communication/_cds_runtime_opc_ua_server.html"
    başlık: "CODESYS Online Help — OPC UA Server"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/Security/_sec_using_secure_opc_ua_server.html"
    başlık: "CODESYS Online Help — Securely use OPC UA Server"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Communication/_comm_configuration_and_-commissioning_of_-the_opcua_server.html"
    başlık: "CODESYS Online Help — OPC UA Server Commissioning"
    güvenilirlik: resmi
  - url: "https://revolutionpi.com/en/tutorial/opc-ua-codesys-node-red"
    başlık: "Revolution Pi — OPC UA with CODESYS and Node-RED"
    güvenilirlik: topluluk
  - url: "https://www.salz-automation.com/en/blog/CODESYS_and_OPC_UA_Integration"
    başlık: "SALZ Automation — CODESYS and OPC UA Integration"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "02_modbus_slave.md"
    ilişki: alternatif
  - konu: "knowledge/codesys/programming/02_gvl_design.md"
    ilişki: gerektirir
  - konu: "knowledge/standards/opcua_overview.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "CODESYS proje yapısı ve GVL tasarımı (programming/02_gvl_design.md)"
  - "OPC UA temel kavramları: Node, Address Space, Subscription, Monitored Item"
  - "Runtime V3.5 SP17+ için kullanıcı yönetimi kavramı"
ÇELİŞKİLER :
  - kaynak: "CODESYS Runtime V3.5 SP17+"
    konu: "SP17'den itibaren anonymous erişim varsayılan olarak kapalı"
    çözüm: >
      SP17 ve sonrasında runtime'a erişmek için kullanıcı yönetimi zorunlu.
      OPC UA için anonymous erişim açıkça etkinleştirilmeli ya da sertifika
      tabanlı kimlik doğrulama yapılandırılmalı. Eski projeler SP17'ye
      geçince "bağlanamıyorum" şikayeti neredeyse her zaman budur.
  - kaynak: "Symbol Configuration vs Communication Manager"
    konu: "OPC UA sunucu kurmanın iki farklı yolu var — hangisi ne zaman?"
    çözüm: >
      Symbol Configuration (IEC Symbol): Hızlı, kod değişikliği gerektirmez.
      Communication Manager + OPC UA Server nesnesi: Gelişmiş yapılandırma,
      custom namespace, method çağrısı. Basit monitörleme için Symbol Configuration
      yeterli; karmaşık information model için Communication Manager kullan.
---

## Özün Ne

CODESYS OPC UA Server, PLC değişkenlerini endüstri standardı OPC UA protokolü üzerinden dışa açan yerleşik bir servistir. SCADA, MES, bulut platformları ve üçüncü taraf HMI'lar bu sayede PLC'ye bağlanabilir. CODESYS'in güçlü tarafı: Standart kurulumda OPC UA sunucu zaten dahilidir, harici bir sunucu uygulaması gerekmez. Doğru yapılandırılmış bir OPC UA sunucu; güvenli şifreli iletişim, kullanıcı kimlik doğrulama, subscription tabanlı değişim izleme ve yöntem çağrısını destekler.

## Nasıl Çalışır

### OPC UA Mimarisi — CODESYS Bağlamında

```
SCADA / MES / Bulut Platform / Node-RED / UaExpert
           │
           │ OPC UA (TCP, port 4840)
           │ Güvenlik: Sertifika + Kullanıcı Kimlik
           ▼
┌─────────────────────────────────────────────────┐
│           CODESYS OPC UA Server                 │
│                                                 │
│  Address Space                                  │
│  ├── Objects                                    │
│  │   └── DeviceSet                              │
│  │       └── [Controller Name]                 │
│  │           └── Application                   │
│  │               └── GVL_IO                    │
│  │                   ├── xMotorRun (Node)       │
│  │                   └── rTemperature (Node)    │
│  └── Types, Views...                            │
│                                                 │
│  Güvenlik Politikaları                          │
│  ├── None (test — üretimde kullanma)            │
│  ├── Basic256Sha256 (Signed)                    │
│  └── Basic256Sha256 (SignedAndEncrypted) ✓      │
└─────────────────────────────────────────────────┘
           │
           │ IEC Symbol Map
           ▼
┌──────────────────────┐
│   CODESYS Runtime    │
│   GVL_IO, GVL_Params │
│   POU değişkenleri   │
└──────────────────────┘
```

### OPC UA Kurulum Yöntemi: Symbol Configuration (Hızlı Yol)

CODESYS'in yerleşik OPC UA sunucusu IEC değişkenlerini Symbol Configuration nesnesi üzerinden dışa açar. Bu yöntemde kod yazmak gerekmez.

**Adım adım:**

```
1. Application → (Sağ tık) → Add Object → Symbol Configuration
   
2. Symbol Configuration editöründe değişkenleri işaretle:
   [✓] GVL_IO.xMotorRun        — OPC UA üzerinden okunabilir/yazılabilir
   [✓] GVL_IO.rTemperature     — OPC UA üzerinden okunabilir
   [✓] GVL_Params.rSetpoint    — OPC UA üzerinden okunabilir/yazılabilir
   
3. Her değişken için OPC UA özelliklerini ayarla:
   Access Level: Read | ReadWrite
   Historizing: (opsiyonel)

4. Build → Download → Start
```

Değişkenler şu NodeId formatında erişilebilir hale gelir:
```
ns=4;s=|var|CODESYS Control.Application.GVL_IO.xMotorRun
```

### OPC UA Sunucu Nesnesi (Gelişmiş Yol)

Daha fazla kontrol için Communication Manager nesnesi kullanılır:

```
Application → Add Object → Communication Manager
    → Communication Manager (Sağ tık) → Add Object → OPC UA Server

Yapılandırma:
  Port: 4840 (varsayılan)
  Maximum Sessions: 10
  Server URI: urn:MyCompany:MyMachine:CODESYS
  Publish/Subscribe Interval: 100ms (varsayılan)
```

### Güvenlik Politikaları

OPC UA üç güvenlik modu tanımlar:

```
Mode     | Şifreleme | İmza | Kullanım
─────────────────────────────────────────────────────────
None     | Yok       | Yok  | Yalnızca LAN test/geliştirme
Sign     | Yok       | Var  | Bütünlük koruması, şifresiz
Sign+Enc | AES-256   | Var  | ✓ Üretim — her zaman bu
```

CODESYS, güvenlik politikası olarak şunları destekler:
- `Basic256Sha256` — RSA imza + SHA-256
- `Aes128-Sha256-RsaOaep` — Daha modern, daha hızlı
- `Aes256-Sha256-RsaPss` — En yüksek güvenlik

### Sertifika Yönetimi

```
CODESYS IDE → View → Security Screen → Devices sekmesi
    → Controller seç
    → CmpOPCUAServer servisi
    → Create Certificate (ikon)
    
Parametreler:
  Organization: MyCompany
  Common Name: MyMachine OPC UA Server
  Country: TR
  City: Istanbul
  Valid Days: 3650 (10 yıl)
  
→ Oluştur → Runtime Yeniden Başlat
```

İstemci (UaExpert, Node-RED) ilk bağlantıda sertifikayı **trust** olarak işaretlemeli:

```
UaExpert → Server → Add → opc.tcp://192.168.1.100:4840
    Security Policy: Basic256Sha256
    Message Security Mode: SignAndEncrypt
    → OK → Sertifika uyarısı → Trust → Connect
```

### Kullanıcı Yönetimi (SP17+)

```
CODESYS IDE → Device → Edit Device → Access Rights sekmesi

Kullanıcı oluştur:
  Username: scada_user
  Password: Güçlü şifre
  Rights: View + Operator (okuma + seçili yazma)
  
Anonymous erişim (test için):
  Communication Settings → Security Settings → 
  Allow anonymous login: ✓ (yalnızca dahili ağ için)
```

### Address Space Tasarımı

Varsayılan address space tüm proje değişkenlerini tek bir ağaç altında sunar. Büyük projelerde düzeni korumak için Symbol Set'ler kullanılır:

```
Symbol Set: "ProductionData" → GVL_IO + GVL_Diagnostics
Symbol Set: "RecipeManagement" → GVL_Recipes + GVL_Params
Symbol Set: "AlarmSystem" → GVL_Alarms

Her Symbol Set farklı kullanıcı grubuna açılabilir:
  Operators → ProductionData: ReadWrite
  Viewers   → ProductionData: Read, RecipeManagement: Read
  SCADA     → Tüm setler: ReadWrite
```

## Pratikte Nasıl Kullanılır

### UaExpert ile Bağlantı Testi

```
1. UaExpert indir: https://www.unified-automation.com/products/development-tools/uaexpert.html
2. Server → Add
   Discovery URL: opc.tcp://192.168.1.100:4840
3. Security: Basic256Sha256 / SignAndEncrypt
4. Connect
5. Address Space sekmesinde değişkenleri göz at:
   Objects → DeviceSet → [Controller] → Application → GVL_IO → ...
6. Data Access View'e sürükle → Canlı değerleri izle
```

### Node-RED ile OPC UA Bağlantısı

```javascript
// Node-RED OPC UA okuma konfigürasyonu
{
  "endpoint": "opc.tcp://192.168.1.100:4840",
  "action": "READ",
  "nodeId": "ns=4;s=|var|CODESYS Control.Application.GVL_IO.rTemperature"
}
```

### Python ile OPC UA Okuma

```python
from opcua import Client
import time

client = Client("opc.tcp://192.168.1.100:4840")
client.set_user("scada_user")
client.set_password("password")
client.connect()

node = client.get_node("ns=4;s=|var|CODESYS Control.Application.GVL_IO.rTemperature")
value = node.get_value()
print(f"Sıcaklık: {value} °C")

client.disconnect()
```

### CODESYSControl.cfg ile OPC UA Yapılandırma

Linux sistemlerde `/etc/CODESYSControl.cfg` veya `/etc/codesyscontrol/CODESYSControl.cfg`:

```ini
[CmpOPCUAServer]
; OPC UA sunucu port (varsayılan 4840)
ServerPort=4840

; Maksimum eş zamanlı oturum
MaxSessions=20

; Güvenlik modu (0=None, 1=Sign, 2=Sign+Encrypt)
; Üretimde 2 olmalı
SecurityMode=2

; Anonymous erişim (0=kapalı, 1=açık)
; SP17+ varsayılan: 0
AllowAnonymous=0
```

## Örnekler

### Örnek 1: Subscription ile Değişken İzleme

OPC UA'nın güçlü özelliği: İstemci, değişkeni her sorgulamak yerine "değişince bana bildir" diyebilir.

```
UaExpert → Data Access View → Değişkeni sürükle
    Sampling Interval: 100ms
    Queue Size: 1
    Discard Oldest: ✓
    
→ Değer değiştikçe otomatik güncelleme
→ CPU tüketimi: Polling'den çok daha düşük
```

### Örnek 2: NodeId Formatları

```
Sayısal NodeId:   ns=2;i=1001
String NodeId:    ns=4;s=|var|CODESYS Control.Application.GVL_IO.xMotorRun
GUID NodeId:      ns=1;g=550e8400-e29b-41d4-a716-446655440000

CODESYS Symbol Configuration varsayılanı:
  ns=4;s=|var|[RuntimeName].[ApplicationName].[GVL].[VariableName]
  
Örnek:
  ns=4;s=|var|CODESYS Control for Linux ARM64 SL.Application.GVL_IO.rTemperature
```

### Örnek 3: OPC UA Method Çağrısı (Gelişmiş)

Communication Manager + OPC UA Server kullanıldığında PLC metotları uzaktan çağrılabilir:

```iecst
(* FB_RecipeLoader içinde — Method tanımı *)
METHOD LoadRecipe : BOOL
VAR_INPUT
    nRecipeID : INT;
END_VAR

(* OPC UA Client'tan çağrı — UaExpert üzerinden *)
(* Objects → Application → FB_RecipeLoader instance → LoadRecipe → Call *)
(* nRecipeID = 3 parametresiyle → Method çağrısı PLC'de çalışır *)
```

## Sık Yapılan Hatalar

### Hata 1: SP17+ Sonrası "Bağlanamıyorum"

```
Semptom: Runtime güncellendi, OPC UA client bağlanamıyor.
Neden  : SP17+ varsayılan olarak anonymous erişimi kapattı.
Çözüm  :
  1. Kullanıcı yönetiminden OPC UA kullanıcısı oluştur
  2. İstemcide kullanıcı adı + şifre gir
  veya
  3. Test için: CODESYSControl.cfg → AllowAnonymous=1
  (Üretimde anonymous kapalı tutulmalı)
```

### Hata 2: Sertifika Güvenilmez — Bağlantı Reddedildi

```
Semptom: İstemci bağlanmaya çalışıyor ama sertifika hatası alıyor.
Neden  : İstemci, sunucunun sertifikasını henüz güvenilir olarak işaretlemedi.
Çözüm  : İlk bağlantıda UaExpert sertifika uyarısı gösterir → Trust/Accept → Tekrar bağlan.
          Programatik bağlantıda: Sertifikayı istemcinin trusted store'una kopyala.
```

### Hata 3: Değişken Address Space'de Görünmüyor

```
Semptom: UaExpert'te beklenen değişkenler yok.
Neden  :
  a) Symbol Configuration'da işaretlenmemiş
  b) Build + Download yapılmamış
  c) Symbol Configuration nesnesi Application altında değil
Çözüm  : Symbol Configuration'da ilgili değişkeni işaretle → Build → Download → Tekrar bağlan
```

### Hata 4: OPC UA Subscription Gecikme Sorunları

```
Semptom: İstemcide değerler çok geç geliyor veya hiç gelmiyor.
Neden  : Task_Comm cycle time çok yavaş veya OPC UA update interval yanlış.
Çözüm  :
  a) OPC UA güncellemesini yapan task'ın cycle time'ını kontrol et
  b) Subscription publishing interval'ı ≥ task cycle time olarak ayarla
  c) Monitored item sampling interval = task cycle time
```

### Hata 5: REAL (FLOAT) Değer Hatalı Okunuyor

```
Neden  : REAL CODESYS'te IEEE 754 32-bit float. Bazı istemciler yanlış yorumlar.
Çözüm  : OPC UA üzerinden REAL'i Float olarak sun. Eğer istemci okuması yanlışsa,
          ölçeklendirme: REAL'i 1000 ile çarp → DWORD olarak sun → İstemci bölsün.
          Modern OPC UA istemciler Float'ı doğru yorumlar — sorun eskimiş istemcilerde.
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**OPC UA Tercih Et:**
- SCADA, MES, ERP ile entegrasyon
- Farklı üretici HMI'ları bağlama
- Bulut platformları (AWS IoT, Azure IoT Hub)
- Güvenlik gereksinimi yüksek sistemler (şifreli iletişim)
- Metadata ve type bilgisiyle zengin veri modeli

**OPC UA Tercih Etme:**
- Basit 2-makine iletişimi → Modbus TCP yeterli, OPC UA gereksiz overhead
- Çok sınırlı CPU/RAM kaynağı → OPC UA bellek ve işlemci yoğun
- Gerçek zamanlı kritik veri → EtherCAT/PROFINET; OPC UA real-time değildir
- Siemens TIA Portal tabanlı karşı taraf → OPC UA veya Profinet, gereksinimlere göre

## Gerçek Proje Notları

**Not 1 — SP17 Geçişinde Üretim Durması**  
Bir fabrikada CODESYS runtime SP17'ye güncellendi. Ertesi gün tüm SCADA'lar PLC'ye bağlanamadı — anonymous erişim kapanmıştı. SCADA yazılımı kullanıcı adı/şifre desteklemiyordu. Acil çözüm: `AllowAnonymous=1` yapıldı. Kalıcı çözüm: SCADA güncellenerek OPC UA kimlik doğrulama desteği eklendi. Ders: Runtime güncellemesi öncesi release notes okunmalı.

**Not 2 — NodeId Değişikliği ve SCADA Çöküşü**  
OPC UA Node'larının stringID'si değişken adına bağlıdır: `GVL_IO.xMotorRun`. Değişken ismi değiştirildiğinde (ör. `xMotorRun` → `xMotor1_Run`) NodeId değişti, SCADA tüm bağlantıları kaybetti. 200 tag'in güncellenmesi yarım gün sürdü. Ders: Dışa açılan değişkenlerin isimleri "frozen" kabul edilmeli; yeniden adlandırma yapılacaksa SCADA eş zamanlı güncellenmeli.

**Not 3 — Subscription vs Polling CPU Farkı**  
Bir SCADA sistemi 500 değişkeni 100ms'de polling yapıyordu; CPU yükü %15'ti. Subscription tabanlı yapıya geçildi (değişince bildir, 100ms sampling). CPU yükü %3'e indi, ağ trafiği %80 azaldı. OPC UA'nın subscription modeli bu nedenle endüstride tercih edilir.

**Not 4 — Güvenlik Politikası "None" ile Üretim**  
Bir makine üreticisi test esnasında "None" güvenlik politikasıyla bıraktı. Fabrikada ağ taraması yapan bir güvenlik aracı PLC'ye erişim sağladı. Kötü niyetli değildi ama alarm verdi. Tüm makineler SignAndEncrypt'e alındı. Ders: Test bittiğinde güvenlik politikası şifreli olarak güncellenmeli.

## İlgili Konular

```
knowledge/codesys/networking/
├── 02_modbus_slave.md        → OPC UA alternatifi; daha basit ama daha az güvenli
├── 03_tcp_socket.md          → Özel protokol için ham TCP
└── 04_mqtt_client.md         → Bulut/IoT için yayınlama

knowledge/codesys/programming/
└── 02_gvl_design.md          → OPC UA'ya açılacak değişkenlerin organizasyonu

knowledge/standards/
└── opcua_overview.md         → OPC UA Information Model, NodeId, Address Space

Araçlar:
  UaExpert   → https://www.unified-automation.com — test ve debug için
  Prosys OPC → https://prosysopc.com — alternatif istemci
  Node-RED   → node-red-contrib-opcua nodesi
```
