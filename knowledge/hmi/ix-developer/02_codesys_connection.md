---
KONU        : Beijer iX Developer — CODESYS PLC Bağlantısı
KATEGORİ    : hmi
ALT_KATEGORI: ix-developer
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://www.beijerelectronics.com/docs/drivers/CODESYS-ARTI/Latest/iX/en/settings.html"
    başlık: "Beijer Electronics — CODESYS ARTI Driver Settings"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/drivers/CODESYS-ARTI/Latest/iX/en/addressing.html"
    başlık: "Beijer Electronics — CODESYS ARTI Driver Addressing"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/drivers/X2/CODESYS-Arti/Latest/iX/en/troubleshooting.html"
    başlık: "Beijer Electronics — CODESYS ARTI Troubleshooting"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/drivers/CODESYS-ARTI/Latest/iX/en/import-module.html"
    başlık: "Beijer Electronics — CODESYS ARTI Import Module"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-SP7HF-Reference/en/controller.html"
    başlık: "Beijer Electronics — iX Developer Controller Reference (OPC UA)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-250-Reference/en/controller.html"
    başlık: "Beijer Electronics — iX Developer 2.50 Controller Reference"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX/3.0/User-Guide/en/controllers.html"
    başlık: "Beijer Electronics — iX Developer 3.0 User Guide: Controllers"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX/3.0/User-Guide/en/servers.html"
    başlık: "Beijer Electronics — iX Developer 3.0 User Guide: Servers"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/drivers/driver-list/en/index-en.html"
    başlık: "Beijer Electronics — iX Developer 3 Driver List"
    güvenilirlik: resmi
  - url: "https://www.valin.com/resources/videos/how-setup-beijer-x2-pro-hmi-codesys-plc"
    başlık: "Valin — How to Setup a Beijer X2 Pro HMI with a CODESYS PLC"
    güvenilirlik: topluluk
  - url: "https://forum.plcnext-community.net/discussion/3849/axc2152-opc-ua-server-with-beijer-x2-hmi-panel"
    başlık: "PLCnext Community — OPC UA Server with Beijer X2 HMI Panel"
    güvenilirlik: topluluk
  - url: "https://revolutionpi.com/forum/viewtopic.php?t=3872"
    başlık: "Revolution Pi Forum — CODESYS OPC UA BadUserAccessDenied hatası"
    güvenilirlik: topluluk
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Communication/_cds_symbolconfiguration.html"
    başlık: "CODESYS Online Help — Symbol Configuration"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/Security/_sec_using_secure_opc_ua_server.html"
    başlık: "CODESYS Online Help — Securely Using OPC UA Server"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "knowledge/hmi/ix-developer/01_architecture.md"
    ilişki: gerektirir
  - konu: "knowledge/hmi/ix-developer/03_screen_design.md"
    ilişki: tamamlar
  - konu: "knowledge/protocols/opc-ua/05_codesys_server_config.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/networking/01_opcua_server.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "iX Developer kurulumu ve temel proje yapısı (01_architecture.md)"
  - "CODESYS projesi oluşturulmuş, PLC çalışıyor"
  - "CODESYS ARTI yöntemi için: CODESYS Symbol Configuration veya SDB dosyası mevcut"
  - "OPC UA yöntemi için: CODESYS OPC UA Server yapılandırılmış, port 4840 açık"
  - "Ağ bağlantısı doğrulanmış (HMI ↔ PLC ping çalışıyor)"
ÇELİŞKİLER :
  - kaynak: "Resmi Beijer dokümantasyonu (driver-list, ARTI settings)"
    konu: "CODESYS ARTI sürüm numarası iX2 ve iX3 arasında farklı görünüyor (4.14/4.17/4.18)"
    çözüm: >
      iX Developer 3 driver listesi v4.18'i (Active) gösteriyor. CE6 (eski X2 Base v1, BoX2 Base v1)
      gerektiren projelerde v4.14 kullanılmalı. Yeni projelerde en güncel sürüm tercih edilmeli.
  - kaynak: "Resmi iX Developer dokümantasyonu (iX-251-Reference security-management)"
    konu: "iX Developer'ın kendi OPC UA sunucusunda şifreleme desteği yok; istemci olarak bağlanırken sunucu tarafındaki şifreleme durumu önemli"
    çözüm: >
      iX Developer OPC UA istemcisi, CODESYS OPC UA sunucusuna güvensiz (None) veya imzalı
      modda bağlanabilir. Şifreli mod için CODESYS tarafında Basic256SHA256 politikası açılır,
      ancak iX Developer OPC UA istemcisinin şifreleme kabiliyeti resmi dokümanda açıkça
      belirtilmemiş — test ortamında doğrulanması önerilir.
  - kaynak: "Resmi Beijer destek sayfası (cloudvpn.beijerelectronics.com) — HTTP 403"
    konu: "OPC-UA destek makalesi erişime kapalı; iX Developer OPC UA istemci güvenlik detayları tam doğrulanamadı"
    çözüm: >
      Erişilebilir kaynaklardan elde edilen bilgi (iX Developer Reference ve 3.0 User Guide)
      ile doğrulama yapıldı. Güvenlik politikası detayları için Beijer Electronics destek
      portalına doğrudan erişim veya resmi destek kanalı önerilir.
  - kaynak: "iX Developer OPC UA istemci — resmi dokümantasyon"
    konu: "OPC UA üzerinden dizi (array) tag desteği yok"
    çözüm: >
      Dizi değişkenler OPC UA controller'da desteklenmiyor. CODESYS ARTI driver ise
      1 boyutlu dizileri destekliyor. Dizi gereken durumlarda ARTI driver tercih edilmeli.
---

## Özün Ne

Beijer **iX Developer**, CODESYS tabanlı bir PLC'ye iki farklı yöntemle bağlanabilir: (1) **CODESYS ARTI driver** — CODESYS'in kendi ARTI (Automation Runtime Interface) protokolü üzerinden doğrudan ve yerel bağlantı; (2) **OPC UA client** — iX Developer'ı standart bir OPC UA istemcisi olarak kullanarak CODESYS'in OPC UA sunucusuna bağlanma. ARTI yöntemi Beijer-CODESYS ekosistemi için optimize edilmiş, sembol dosyası (XML/SDB) tabanlı bir entegrasyondur ve port 11740 kullanır. OPC UA yöntemi ise CODESYS dışı PLC'lerle de çalışan evrensel bir yaklaşımdır; CODESYS OPC UA Server'ın port 4840 üzerinden çalışmasını gerektirir. Her iki yöntem de tag import, adresleme ve canlı veri okuma/yazma işlemlerini destekler.

**iX Developer** (iX2 ve güncel iX3), Beijer Electronics'in HMI geliştirme ortamıdır. iX3, iX2 projelerini geriye dönük olarak destekler; iki platform arasında sürücü ve protokol uyumluluğu korunmaktadır.

## Nasıl Çalışır

### İki Bağlantı Yöntemi: ARTI vs OPC UA

```
┌───────────────────────────────────────────────────────────────┐
│               Beijer iX Developer (HMI)                        │
│                                                                 │
│  Tags → Controllers tab                                         │
│  ┌─────────────────────┐   ┌────────────────────────────────┐  │
│  │  CODESYS ARTI       │   │  OPC UA Client                 │  │
│  │  (driver v4.18)     │   │  (yerleşik — ekstra sürücü     │  │
│  │                     │   │   gerektirmez)                 │  │
│  │  Port: 11740        │   │  Port: 4840 (varsayılan)       │  │
│  │  Protokol: V3 TCP   │   │  URL: opc.tcp://[IP]:4840      │  │
│  │  Sembol: XML/SDB    │   │  Auth: Anonim / Kullanıcı adı  │  │
│  └────────┬────────────┘   └──────────────┬─────────────────┘  │
│           │                               │                     │
└───────────┼───────────────────────────────┼─────────────────────┘
            │                               │
            │ TCP/IP (LAN)                  │ TCP/IP (LAN)
            ▼                               ▼
┌───────────────────────────────────────────────────────────────┐
│               CODESYS Runtime (PLC)                            │
│                                                                 │
│  ARTI Servisi (port 11740)    OPC UA Sunucusu (port 4840)      │
│  ┌──────────────────────┐    ┌───────────────────────────────┐ │
│  │ Symbol Configuration │    │ Symbol Configuration          │ │
│  │ (XML dosyası         │    │ (Address Space: ns=4;s=|var|) │ │
│  │  PLC'ye indirilmiş)  │    │ AllowAnonymous=1 veya         │ │
│  │                      │    │ kullanıcı yönetimi            │ │
│  └──────────────────────┘    └───────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

### Yöntem 1: CODESYS ARTI Driver

ARTI (Automation Runtime Interface), CODESYS'in PLC ile HMI veya SCADA yazılımları arasındaki doğrudan iletişim protokolüdür. iX Developer, CODESYS ARTI sürücüsü (v4.18 — Active) ile bu protokolü kullanır.

**Temel özellikler:**
- Port: 11740 (CODESYS V3 varsayılanı)
- Protokol: V3 TCP/IP (yeni projeler) veya V2 TCP/IP (eski CODESYS V2 sistemleri)
- Kimlik doğrulama: Anonim (boş kullanıcı adı) veya kullanıcı adı + şifre
- Sembol erişimi: CODESYS'ten dışa aktarılan XML veya SDB dosyası üzerinden
- Dizi desteği: Tek boyutlu diziler dahil desteklenir
- 64-bit tipler: LWORD, LINT, LREAL desteklenmez

**Desteklenen veri tipleri:**
```
Desteklenen: BOOL, WORD, DWORD, INT, UINT, UDINT, DINT, STRING (maks 80 karakter),
             REAL, TIME, ve bunların 1 boyutlu dizileri,
             kullanıcı tanımlı tipler (içinde yalnızca desteklenen tipler varsa)

Desteklenmeyen: BYTE, SINT, USINT, LWORD, LINT, LREAL
```

**Adresleme sözdizimi:**
```
CODESYS V3 (iX Developer'da):
  [Uygulama adı].[POU adı].[Değişken adı]
  Örnek: Application.PLC_PRG.xMotorRun
         Application.GVL_IO.rTemperature

CODESYS V2 (eski sistemler):
  [POU adı].[Değişken adı]          → yerel değişkenler
  .[Değişken adı]                   → global değişkenler
  Örnek: PLC_PRG.LocalVar
         .GlobVar

Bit erişimi (tamsayı değişkenler için):
  [POU adı].[Değişken adı].[Bit numarası]
  Örnek: Application.PLC_PRG.nStatus.3
  Not: Bit yazma işlemi okuma-sonra-yazma gerektirir; dikkatli kullanılmalı.

Çoklu istasyon (birden fazla PLC):
  [İstasyon numarası]:[Değişken yolu]
  Örnek: 05:Application.GVL_IO.xMotorRun   → İstasyon 5
         I2:Application.GVL_IO.xMotorRun   → Index register 2 ile istasyon
```

### Yöntem 2: OPC UA Client

iX Developer, herhangi bir OPC UA sunucusuna (CODESYS dahil) bağlanabilen bir OPC UA istemcisine sahiptir. Ekstra sürücü kurulumu gerekmez; yalnızca "OPC UA Server" controller türü seçilir.

**Temel özellikler:**
- Transport: Yalnızca UA TCP Binary desteklenir (URL: `opc.tcp://...`)
- Kimlik doğrulama: Anonim veya kullanıcı adı + şifre
- Dizi desteği: Desteklenmez
- NodeId tipleri: Numeric ve String desteklenir; Guid ve Opaque atlanır

**CODESYS OPC UA'da tag adresleme:**
```
Browsing yöntemi (önerilen):
  Tags → Ekle → "Add Tags from OPC Server" →
  Browse OPC Server diyaloğu → Tag seç → OK
  (Namespace URI'ları otomatik yapılandırılır)

BrowseName yöntemi (manuel):
  [Namespace URI öneki]:[BrowseName]
  Örnek: NS4:xMotorRun

NodeId yöntemi (direkt):
  *[Namespace URI öneki]:[IdentifierType]:[Identifier]
  Örnek: *NS4:String:|var|CODESYS Control Linux ARM64 SL.Application.GVL_IO.xMotorRun
         *NS4:Numeric:12345

CODESYS varsayılan namespace (atıf: protocols/opc-ua/05_codesys_server_config.md):
  ns=4; URI: "http://www.3s-software.com/schemas/Codesys-V3"
  NodeId formatı: ns=4;s=|var|[RuntimeAdı].[UygulamaAdı].[GVLAdı].[DeğişkenAdı]
```

**Subscription ve örnekleme ayarları:**
```
Maksimum subscription sayısı (controller ayarında yapılandırılır)
Örnekleme aralığı (Sampling interval): istemci tarafında ayarlanır
Yayın aralığı (Publishing interval) < Örnekleme aralığı ise sunucuda kuyruk oluşur
```

### X2 Control: Aynı Cihazda HMI + CODESYS

Beijer X2 control serisi (X2 control 4/7/10/12/15), aynı donanım üzerinde hem iX Developer HMI hem de CODESYS runtime çalıştırır. Bu durumda:

```
İki driver mimarisi kullanılır:
  Driver 1: iX HMI ↔ CODESYS (SoftControl Direct Access driver)
            → Dahili iletişim; aynı işlemci üzerinde
  Driver 2: CODESYS ↔ Uzak I/O (EtherCAT / Modbus TCP)
            → LAN A: EtherCAT için önerilir
            → LAN B: Modbus TCP için önerilir
```

## Pratikte Nasıl Kullanılır

### Yöntem 1: CODESYS ARTI Driver ile Bağlantı

**PLC tarafında hazırlık (CODESYS):**

```
1. Proje ağacında Application → Add Object → Symbol Configuration
2. Symbol Configuration editöründe HMI'ın görmesi gereken değişkenleri işaretle
   (GVL_IO, GVL_Params, PLC_PRG içindeki değişkenler)
3. Her değişken için erişim hakkı: Read veya ReadWrite
4. Build → Generate Code
   → Proje dizininde XML dosyası oluşur:
     [proje_adı].[cihaz_adı].[uygulama_adı].xml

5. Alternatif (V3): Download → "Download Symbol File" seçeneği
   Target Settings → General → "Download Symbol File" ✓
   → Sembol bilgisi PLC'ye indirilir; iX Developer bağlantı sırasında otomatik yükler

6. Güvenlik duvarı: TCP port 11740 açık olmalı
```

**iX Developer tarafında yapılandırma:**

```
Adım 1 — Controller ekle:
  Tags (sekme) → Controllers (alt sekme) → Add (düğme)
  → Controller türü: "CODESYS ARTI" → OK

Adım 2 — Bağlantı parametrelerini gir:
  IP Address  : [PLC IP adresi, örn. 192.168.1.100]
  Port        : 11740
  Protocol    : V3 TCP/IP    (CODESYS 3.x için)
               V2 TCP/IP    (eski CODESYS 2.x için)
  Username    : [boş bırak = anonim, veya CODESYS kullanıcı adı]
  Password    : [boş bırak = anonim, veya CODESYS şifresi]

Adım 3 — Sembol dosyasını içe aktar:
  Tags → Import (düğme) → CODESYS XML dosyasına göz at → Aç
  → Semboller listede görünür
  → İstasyon ataması: "Import to station(s)" → 1 (varsayılan)

  Alternatif — Bağlantı sırasında otomatik yükleme:
  Settings → "Load symbols when connecting" ✓
  → PLC'ye indirilmiş sembol dosyası bağlantı anında yüklenir

Adım 4 — Tag oluştur:
  Tags → Add → yeni tag
  Address alanına CODESYS V3 sözdizimini gir:
    Application.GVL_IO.xMotorRun      → BOOL, ReadWrite
    Application.GVL_IO.rTemperature   → REAL, Read
  VEYA Import ile tüm semboller toplu içe aktarılır

Adım 5 — Bağlantıyı doğrula:
  Transfer (Simüle Et / Panele indir)
  → Canlı değerlerin HMI üzerinde güncellendiğini gözlemle
```

**Önemli ayarlar:**

| Ayar | Varsayılan | Açıklama |
|------|-----------|----------|
| Update Rate | 200 ms | Düşürdükçe CPU yükü artar |
| Timeout | 2000 ms | Gateway kullanımında artırılabilir |
| Retries | 3 | Hata öncesi deneme sayısı |
| Offline Retry | 5 sn | Kopuk istasyonu yeniden denemek için bekleme |
| Byte Order | Intel | CODESYS varsayılanıyla uyumlu |

### Yöntem 2: OPC UA Client ile Bağlantı

**PLC tarafında hazırlık (CODESYS OPC UA Server):**

```
1. Application → Add Object → Symbol Configuration
   → Dışa açılacak değişkenleri işaretle, erişim hakları ata
   → Build → Download

2. CODESYS OPC UA Server yapılandırması
   (Detay: protocols/opc-ua/05_codesys_server_config.md)
   Endpoint: opc.tcp://[PLC_IP]:4840
   Güvenlik: AllowAnonymous=1  (hızlı test için)
             veya kullanıcı yönetimi kur

3. Güvenlik duvarı: TCP port 4840 açık olmalı
```

**iX Developer tarafında yapılandırma:**

```
Adım 1 — OPC UA Controller ekle:
  Tags → Controllers → Add
  → Controller türü: "OPC UA Server" → OK
  → URL gir: opc.tcp://192.168.1.100:4840
  → OK

Adım 2 — Kimlik doğrulama (isteğe bağlı):
  Settings → Authentication:
    Anonim giriş  : Username ve Password boş bırak
    Kullanıcı adı : CODESYS kullanıcı adı ve şifre gir
    Non-secure connections: Eski sunucular (v2.40 SP4 ve öncesi) için; dikkatli kullan

Adım 3 — Namespace yapılandırması:
  Settings → Namespace:
    CODESYS namespace URI ekle:
      URI   : http://www.3s-software.com/schemas/Codesys-V3
      Önek  : NS4   (veya tercih edilen kısaltma)
  NOT: Browse yöntemi kullanılırsa namespace'ler otomatik ayarlanır

Adım 4 — Tag ekle:
  Seçenek A — Browse (önerilen):
    Tags → Add → "Add Tags from OPC Server [Controller1]..."
    → Browse OPC Server diyaloğu açılır
    → Objects / DeviceSet / [Runtime] / Application / GVL_IO / xMotorRun
    → İstenen tag'leri seç → OK
    (Namespace'ler otomatik yapılandırılır)

  Seçenek B — BrowseName yöntemi:
    Tag Address alanına: NS4:xMotorRun
    (NS4 = http://www.3s-software.com/schemas/Codesys-V3 namespace öneki)

  Seçenek C — NodeId yöntemi (tam adres):
    Tag Address alanına:
      *NS4:String:|var|CODESYS Control Linux ARM64 SL.Application.GVL_IO.xMotorRun

Adım 5 — Namespace senkronizasyonu:
  Controllers sekmesinde OPC UA controller seç → OK
  → "Sync Namespace" butonu ile tag bağlantısını doğrula
  → Tag listesinde değerlerin güncellendiğini kontrol et
```

### Bağlantı Testi

```
Ağ düzeyi test:
  ping [PLC_IP]              → Temel bağlantı
  telnet [PLC_IP] 11740      → ARTI port erişimi
  telnet [PLC_IP] 4840       → OPC UA port erişimi

iX Developer düzeyinde test:
  1. Transfer → Simulate (panele yüklemeden simüle et)
  2. Tags ekranında tag değerlerinin güncellenip güncellenmediğini gözlemle
  3. Değer "---" veya sabit 0 ise bağlantı problemi var demektir

Bağımsız OPC UA testi (UaExpert ile):
  1. UaExpert → Sunucuya bağlan: opc.tcp://[PLC_IP]:4840
  2. Address Space'i gez → değişkenlerin göründüğünü doğrula
  3. UaExpert bağlanıyor ama iX bağlanamıyorsa → iX ayarlarında sorun
  4. İkisi de bağlanamıyorsa → CODESYS OPC UA Server yapılandırmasında sorun
```

## Örnekler

### Örnek 1: Standart ARTI Bağlantısı (Uzak CODESYS PLC)

```
Senaryo: Ayrı bir donanım üzerinde CODESYS V3 çalışıyor, iX Panel network üzerinden bağlanıyor.

CODESYS tarafı:
  Runtime: 192.168.1.100
  Uygulama: Application
  GVL_IO:
    xMotorRun    : BOOL   := FALSE;
    xMotorFB     : BOOL;
    rTemperature : REAL;
  GVL_Params:
    rSpeedSP     : REAL   := 50.0;

  Symbol Configuration:
    [✓] Application.GVL_IO.xMotorRun    → ReadWrite
    [✓] Application.GVL_IO.xMotorFB     → Read
    [✓] Application.GVL_IO.rTemperature → Read
    [✓] Application.GVL_Params.rSpeedSP → ReadWrite
  Build → XML dosyasını USB/ağ paylaşımına kopyala

iX Developer tarafı:
  Controller: CODESYS ARTI
  IP: 192.168.1.100  Port: 11740  Protocol: V3 TCP/IP
  Import → XML dosyasını seç → tüm semboller içe aktarılır

  Tag eşlemeleri (otomatik oluşur):
    HMI_MotorStart    → Application.GVL_IO.xMotorRun    (BOOL)
    HMI_MotorFeedback → Application.GVL_IO.xMotorFB     (BOOL)
    HMI_Temperature   → Application.GVL_IO.rTemperature (REAL)
    HMI_SpeedSetpoint → Application.GVL_Params.rSpeedSP (REAL)
```

### Örnek 2: OPC UA Bağlantısı (CODESYS OPC UA Server)

```
Senaryo: CODESYS OPC UA Server aktif, iX Developer OPC UA istemcisi olarak bağlanıyor.

CODESYS konfigürasyonu (özet):
  CODESYSControl.cfg:
    [CmpOPCUAServer]
    ServerPort=4840
    AllowAnonymous=1   (test için)

  Endpoint: opc.tcp://192.168.1.100:4840

iX Developer:
  Controller türü: OPC UA Server
  URL: opc.tcp://192.168.1.100:4840
  Auth: Anonim

  Browse yöntemi:
    Objects → DeviceSet → CODESYS Control Linux ARM64 SL
    → Application → GVL_IO → xMotorRun seç → OK
    Tag address otomatik: NS4:xMotorRun
    (veya tam NodeId: *NS4:String:|var|CODESYS Control Linux ARM64 SL.Application.GVL_IO.xMotorRun)
```

### Örnek 3: X2 Control (Entegre Cihaz)

```
Senaryo: X2 control 12 — aynı cihazda iX HMI + CODESYS runtime.

iX Developer konfigürasyonu:
  Driver 1 — HMI ↔ PLC (dahili):
    Controller: CODESYS ARTI (SoftControl Direct Access driver)
    IP: 127.0.0.1 (localhost) veya cihazın kendi IP'si
    Port: 11740
    Protocol: V3 TCP/IP

  Driver 2 — PLC ↔ Uzak I/O:
    EtherCAT: LAN A portu üzerinden
    Modbus TCP: LAN B portu üzerinden

  Not: CODESYS çalıştığı port üretici ve runtime versiyonuna göre
       11100–11999 aralığında değişebilir; cihaz dokümantasyonundan doğrula.
```

### Örnek 4: Çoklu İstasyon (Birden Fazla CODESYS PLC)

```
Senaryo: Bir iX Panel iki ayrı CODESYS PLC'ye bağlanıyor.

Controllers sekmesi:
  İstasyon 1: IP 192.168.1.100, Port 11740 (Ana makine)
  İstasyon 2: IP 192.168.1.101, Port 11740 (Yardımcı makine)

Tag adresleme:
  Ana makine:  Application.GVL_IO.xMotorRun       (varsayılan istasyon)
  Yardımcı:    02:Application.GVL_IO.xMotorRun     (istasyon 2 öneki)

İstasyon devre dışı bırakma (bakım):
  1:ACTIVE = 0  → İstasyon 1 devre dışı (HMI uyarı verir, diğer istasyon çalışır)
  1:ACTIVE = 1  → İstasyon 1 aktif
```

## Sık Yapılan Hatalar

### Hata 1: Symbol Configuration İndirilmedi — "No Symbol File"

```
Belirti : iX Developer → "No symbol file" veya "Loading Symbols failed"
Neden   : CODESYS Symbol Configuration var ama PLC'ye indirilmedi,
           veya iX bağlantısı kurulmadan önce PLC programı çalışmıyor.

Çözüm:
  CODESYS'te:
    Build → Generate Code  (XML dosyası oluşur)
    Online → Login → Download → Run

  iX Developer Settings'te:
    "Download Symbol File" (Target Settings → General) ✓ işaretliyse
    iX bağlandığında otomatik yükler.
    Değilse: XML dosyasını manuel import et.

  Kontrol: PLC programı çalışıyor olmalı (Online → Run modunda).
```

### Hata 2: CODESYS V3 Adresleme Hatası — "Invalid Variable"

```
Belirti : Tag değeri "---" veya bağlantı kurulmuş ama veri gelmiyor.
Neden   : CODESYS V3'te uygulama adı unutulmuş.

Yanlış : PLC_PRG.xMotorRun          (V2 sözdizimi)
Doğru  : Application.PLC_PRG.xMotorRun  (V3 sözdizimi)

Not: Uygulama adı "Application" değil farklıysa (örn. "MyApp"):
     MyApp.PLC_PRG.xMotorRun

CODESYS'te uygulama adını bulmak:
  Device Tree → Application nesnesinin adına sağ tıkla → Properties → Name
```

### Hata 3: OPC UA Bağlantısı — "BadUserAccessDenied" veya Sertifika Hatası

```
Belirti : iX Developer OPC UA controller bağlanamıyor; CODESYS logunda
           "BadUserAccessDenied" veya sertifika red mesajı.

Neden A — Anonim erişim kapalı:
  CODESYSControl.cfg'de AllowAnonymous=0
  Çözüm: AllowAnonymous=1 yap (test için) VEYA kullanıcı adı/şifre gir.

Neden B — Sertifika güven listesinde değil:
  iX Developer sertifikası CODESYS'in rejected/ klasöründe:
    /var/opt/codesys/PlcLogic/Application/pki/rejected/
  Çözüm: Sertifikayı trusted/ klasörüne taşı:
    cp rejected/certs/[ix_cert].der trusted/certs/

Neden C — CODESYS SP17+ kullanıcı yönetimi:
  CODESYS V3.5 SP17+ ile AllowAnonymous varsayılan değeri 0 oldu.
  (Detay: protocols/opc-ua/05_codesys_server_config.md)
  Çözüm: CODESYS kullanıcı yönetimi kur ve iX'e kullanıcı adı/şifre gir.

Hızlı test:
  UaExpert ile aynı sunucuya bağlan.
  UaExpert bağlanıyorsa sorun iX ayarlarındadır.
  İkisi de bağlanamıyorsa CODESYS sunucu yapılandırmasını kontrol et.
```

### Hata 4: Port Engellendi — PLC Ping Alıyor Ama Bağlantı Yok

```
Belirti : Ping çalışıyor ama ARTI (11740) veya OPC UA (4840) bağlantısı kurulamıyor.
Neden   : Güvenlik duvarı veya işletim sistemi portları engelliyor.

Test:
  Windows: telnet [PLC_IP] 11740
  Linux  : nc -vz [PLC_IP] 11740

Çözüm:
  PLC tarafında güvenlik duvarı kuralı ekle (iptables veya Windows Firewall):
    Port 11740 TCP → iX Panel IP'sinden erişime izin ver
    Port 4840  TCP → OPC UA kullanıyorsa

  iX Developer tarafında antivirus/güvenlik duvarı da kontrol et.
```

### Hata 5: Veri Tipi Uyumsuzluğu — "Datatype Mismatch"

```
Belirti : Tag bağlı görünüyor ama değer mantıksız veya hata mesajı var.
Neden   : CODESYS'teki veri tipi ile iX Developer'da tanımlanan tip uyuşmuyor.
          Veya CODESYS'te BYTE/SINT/LREAL kullanıldı — ARTI bunları desteklemiyor.

Çözüm:
  1. Import modülünü kullan — otomatik tip eşlemesi yapar.
  2. CODESYS'te BYTE → USINT, SINT → INT, LREAL → REAL'e dönüştür.
  3. Tag'i sil ve yeniden import et (CODESYS'te tip değişikliği olduysa).
```

### Hata 6: OPC UA'da Dizi Tag Desteklenmiyor

```
Belirti : CODESYS'teki dizi değişken OPC UA controller'da görünmüyor veya hata veriyor.
Neden   : iX Developer OPC UA controller dizileri desteklemiyor.

Çözüm A: CODESYS ARTI driver'a geç (1 boyutlu diziler desteklenir).
Çözüm B: Dizi elemanlarını ayrı ayrı değişken olarak CODESYS'te tanımla.
          Örn: xAlarms[0] → xAlarm_0, xAlarms[1] → xAlarm_1 gibi.
```

### Hata 7: Sürücü Güncellemesi Sonrası Kimlik Bilgileri Sorunu

```
Belirti : CODESYS ARTI v4.15'ten sonraki sürüme güncellendi, bağlantı kesildi.
Neden   : Sürücü güncellemesi mevcut şifreleme formatını değiştiriyor.

Çözüm: Tags → Controllers → Settings →
       User ve Password alanlarını manuel güncelle (silinip yeniden gir).
       Resmi not: "When upgrading from version 4.15 to a later version,
       you must manually update the User and Password in the driver settings."
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### CODESYS ARTI Driver — Ne Zaman?

```
Tercih et:
  ✓ Karşı taraf CODESYS V2 veya V3 runtime (SoftPLC, sertifikalı donanım)
  ✓ Dizi değişkenlere ihtiyaç var
  ✓ 64-bit olmayan tüm standart tipler kullanılıyor
  ✓ Basit ve hızlı kurulum önceliği
  ✓ X2 control entegre cihazlarda (SoftControl Direct Access)
  ✓ OPC UA server yapılandırması istenmiyor

Tercih etme:
  ✗ CODESYS dışı PLC (Siemens, Allen-Bradley, vb.) → OPC UA veya ilgili driver
  ✗ OPC UA standardıyla interoperabilite şart → OPC UA seç
  ✗ 64-bit veri tipleri (LREAL, LINT, LWORD) gerekiyor → OPC UA veya tip değişikliği
```

### OPC UA Client — Ne Zaman?

```
Tercih et:
  ✓ Vendor-bağımsız standart protokol gerekiyor
  ✓ CODESYS dışı OPC UA sunucusuna da bağlanma ihtimali var
  ✓ CODESYS OPC UA Server zaten kurulu ve kullanılıyor
  ✓ Gelişmiş güvenlik (kullanıcı yönetimi + sertifika) gerekiyor
  ✓ SCADA ve HMI aynı OPC UA altyapısını paylaşıyor

Tercih etme:
  ✗ Dizi değişkenler gerekiyor → ARTI driver seç
  ✗ Basit, hızlı CODESYS bağlantısı → ARTI daha az konfigürasyon
  ✗ OPC UA Server yapılandırmak istemiyorsun → ARTI yeterli
```

## Gerçek Proje Notları

**Not 1 — XML Dosyasının Yolu Uzun Olmamalı**
CODESYS proje dizini çok derinse (uzun klasör yolu) iX Developer'a import sırasında tag isimleri kesilebilir. CODESYS, tag adı uzunluğunu `[proje dosyasına giden yol] + [tag adı]` toplamına göre hesaplar. Cihaz adını kısa tut; proje dizinini mümkün olduğunca üst seviyede tut. Bu sorunla karşılaşıldığında cihaz adının kısaltılması çözüm oldu.

**Not 2 — OPC UA ile ARTI Birlikte Kullanım**
OPC UA Server aktifken (port 4840) ARTI da aynı anda çalışır (port 11740). İki protokol çakışmaz. Aynı PLC'ye hem OPC UA (SCADA için) hem ARTI (HMI için) kullanılabilir. Önerilen kural: HMI → ARTI (hızlı, basit), SCADA/MES → OPC UA (zengin veri modeli, subscription).

**Not 3 — "Import Only What You Need" Kuralı**
Symbol Configuration'daki tüm değişkenleri iX Developer'a import etmek sorun yaratabilir (çok sayıda tag, uzun yükleme süresi). Resmi Beijer dokümantasyonu açıkça "import only the tags that will be used" diyor. Pratik kural: Her ekran için gerekli tag'leri ayrı bir listede belirle, toplu import yerine seçici import yap.

**Not 4 — CODESYS SP17+ Geçişinde OPC UA Kimlik Sorunu**
CODESYS V3.5 SP17 ile anonim erişim varsayılan olarak kapatıldı. Daha önceki sürümde çalışan OPC UA bağlantısı SP17'ye geçişte aniden koptu. CODESYS tarafında kullanıcı yönetimi kurulana kadar `AllowAnonymous=1` ile geçici çözüm yapıldı, ardından kalıcı kullanıcı yönetimi devreye alındı. Bu detay için bkz: `protocols/opc-ua/05_codesys_server_config.md`.

**Not 5 — OPC UA NodeId Runtime Adına Bağımlı**
OPC UA üzerinden bağlanıldığında CODESYS runtime adı NodeId'nin bir parçasıdır:
`ns=4;s=|var|CODESYS Control Linux ARM64 SL.Application.GVL_IO.xMotorRun`
Runtime değişirse (ör. Windows → Linux ARM64 geçişi) tüm tag adresleri değişir.
ARTI driver bu sorundan muaf — değişken adlarını runtime adından bağımsız kullanır.
OPC UA'da kalıcı çözüm: Communication Manager ile custom namespace (runtime adından bağımsız NodeId). Bkz: `protocols/opc-ua/05_codesys_server_config.md`.

**Not 6 — Bağlantı Testi için UaExpert Zorunlu**
OPC UA bağlantısı sorunlarında iX Developer'dan önce UaExpert ile doğrulama yapmak saatler kazandırır. UaExpert bağlanabiliyorsa sorun iX ayarlarındadır; bağlanamıyorsa CODESYS OPC UA Server'da bir sorun var demektir. Bu ayrımı yapmadan saatlerce iX ayarlarıyla vakit geçirildiği oldu.

## İlgili Konular

```
knowledge/hmi/ix-developer/
├── 01_architecture.md          → iX Developer genel mimari ve panel türleri
└── 03_screen_design.md         → Bağlanan tag'lerin ekranda kullanımı

knowledge/protocols/opc-ua/
└── 05_codesys_server_config.md → CODESYS OPC UA Server detaylı konfigürasyonu
                                   (endpoint URL, AllowAnonymous, sertifika, SP17+)

knowledge/codesys/networking/
└── 01_opcua_server.md          → CODESYS OPC UA Server hızlı kurulum rehberi
```
