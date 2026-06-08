---
KONU        : CODESYS OPC-UA Sunucu Detaylı Konfigürasyonu
KATEGORİ    : protocols
ALT_KATEGORI: opc-ua
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Communication/_cds_runtime_opc_ua_server.html"
    başlık: "CODESYS Online Help — OPC UA Server"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Communication/_comm_configuration_and_-commissioning_of_-the_opcua_server.html"
    başlık: "CODESYS Online Help — OPC UA Server Commissioning"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Communication/_comm_opcua_server_config.html"
    başlık: "CODESYS Online Help — OPC UA Server Configuration Settings"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_architecture.md"
    ilişki: gerektirir
  - konu: "03_security.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/networking/01_opcua_server.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "OPC UA mimarisi ve güvenlik (01_architecture.md, 03_security.md)"
  - "CODESYS proje yapısı (fundamentals/02_project_structure.md)"
  - "Runtime ve Linux/Windows yapılandırma (fundamentals/01_runtime_architecture.md)"
ÇELİŞKİLER :
  - kaynak: "Symbol Configuration vs Communication Manager + OPC UA Server nesnesi"
    konu: "Hangi yöntem ne zaman tercih edilmeli?"
    çözüm: >
      Symbol Configuration: Hızlı, minimal yapılandırma, tüm GVL değişkenlerini otomatik sunar.
      Yeterli çoğu SCADA/HMI entegrasyonu için.
      Communication Manager + OPC UA Server: Custom namespace, method desteği,
      gelişmiş information model, çok uygulama yönetimi gerektirdiğinde.
      Basit projeler için Symbol Configuration tercih et; karmaşık için Communication Manager.
---

## Özün Ne

Bu belge, CODESYS'teki OPC UA sunucu yapılandırmasını bütün parametreleriyle ele alır. `knowledge/codesys/networking/01_opcua_server.md` kurulumu anlatan giriş belgesidir; bu belge ise her parametrenin ne anlama geldiğini, performans üzerindeki etkisini ve gerçek projelerdeki doğru değerlerini açıklar. Endpoint URL yapısı, namespace organizasyonu, sertifika yönetimi, session limitleri ve Symbol Configuration detayları burada bulunur.

## Nasıl Çalışır

### CODESYS OPC UA Server — İki Entegrasyon Yöntemi

```
Yöntem 1: Yerleşik OPC UA Server (Symbol Configuration)
─────────────────────────────────────────────────────────
  Application → Add Object → Symbol Configuration
  
  Avantajlar:
    - Sıfır kod değişikliği
    - Tüm GVL değişkenleri otomatik dışa açılır
    - Yapılandırma kolay
  
  Sınırlamalar:
    - Custom namespace yok (CODESYS standart namespace)
    - Method desteği yok
    - Node hiyerarşisi CODESYS proje yapısını yansıtır
    - Tek application servisi
  
Yöntem 2: Communication Manager + OPC UA Server Nesnesi
─────────────────────────────────────────────────────────
  Application → Add Object → Communication Manager
  Communication Manager → Add Object → OPC UA Server
  
  Avantajlar:
    - Custom namespace ve node hiyerarşisi
    - Method desteği
    - Gelişmiş erişim kontrolü
    - Birden fazla application koordinasyonu
  
  Sınırlamalar:
    - Daha fazla yapılandırma
    - GVL değişkenleri manuel olarak publish edilmeli
```

### Endpoint URL Yapısı

```
opc.tcp://[host]:[port]/[path]

CODESYS varsayılan:
  opc.tcp://localhost:4840
  opc.tcp://192.168.1.100:4840

Tam endpoint URL (runtime adı dahil):
  opc.tcp://192.168.1.100:4840/CODESYS/Application/SimulationServer

CODESYS'te endpoint URL'si:
  Communication Settings → Endpoint URL
  veya CODESYSControl.cfg [CmpOPCUAServer] ServerPort

Port seçimi:
  4840 → Standart OPC UA portu (IANA kayıtlı)
  48400 → Alternatif (birden fazla server için)
  Güvenlik duvarı: Yalnızca seçilen port açılır
```

### Symbol Configuration — Her Seçeneğin Anlamı

Symbol Configuration editörü açıldığında sol panelde tüm Application değişkenleri listesi gelir:

```
Symbol Configuration Editörü:
  [✓] GVL_IO.xMotorRun           Access: ReadWrite
  [✓] GVL_IO.rTemperature        Access: Read (Salt Okunur)
  [✓] GVL_Params.rSpeedSetpoint  Access: ReadWrite
  [ ] GVL_Internal.xDebugFlag    (İşaretlenmemiş → OPC UA'ya açılmaz)

Her değişken için ayarlar:
  Access Rights:
    Read            → Yalnızca okuma
    ReadWrite       → Okuma + yazma
    CurrentRead     → Canlı değer (subscribe edilebilir)
    
  Historizing:
    True → OPC UA History servisi ile geçmiş okunabilir
    (Gerçek history storage için ayrı historian gerekir)
```

**IEC Symbol Publishing ayarı:**
```
Symbol Configuration → Configuration sekmesi:
  ☑ Support OPC UA Information Model
  ☑ Support data access
  ☑ Support events
  
  Symbol Set Name: "ProductionData"  (opsiyonel — farklı kullanıcılara farklı set)
```

### Namespace Yönetimi

```
CODESYS OPC UA sunucusu namespace'leri:

ns=0: OPC UA Foundation standart namespace (Base, Server node'ları)
ns=1: OPC UA DI (Device Integration) — varsa
ns=2: CODESYS internal
ns=3: ...
ns=4: CODESYS uygulama namespace (değişkenler burada)

Namespace URI (her zaman sabit):
  "http://www.3s-software.com/schemas/Codesys-V3"

NodeId formatı (CODESYS):
  ns=4;s=|var|[RuntimeName].[ApplicationName].[GVLName].[VariableName]
  
  Örnek:
  ns=4;s=|var|CODESYS Control Linux ARM64 SL.Application.GVL_IO.xMotorRun
  ns=4;s=|var|CODESYS Control Win V3 x64.Application.GVL_Params.rSetpoint
  
  RuntimeName: runtime'ın adı (PLC Shell'de "version" komutu ile görülür)
  ApplicationName: CODESYS projesindeki Application nesnesinin adı
```

**Custom namespace (Communication Manager ile):**
```
Communication Manager → OPC UA Server → Configuration:
  Server Namespace URI: "http://acme-automation.com/myMachine"
  → Node'lar bu URI altında tanımlanır
  → İstemci: get_namespace_index("http://acme-automation.com/myMachine")
```

### CODESYSControl.cfg Tam Referans

```ini
[CmpOPCUAServer]
; ════════════════════════════════════════
; BAĞLANTI PARAMETRELERİ
; ════════════════════════════════════════

; OPC UA server TCP port
ServerPort=4840

; Endpoint path (boş = varsayılan)
; EndpointPath=CODESYS

; Maksimum eş zamanlı oturum (session) sayısı
; 0 = sınırsız (dikkat: kaynak tüketimi)
MaxSessions=20

; Maksimum MonitoredItem sayısı (tüm session toplamı)
MaxMonitoredItems=5000

; Maksimum Subscription sayısı (tüm session toplamı)  
MaxSubscriptions=500

; ════════════════════════════════════════
; GÜVENLİK PARAMETRELERİ
; ════════════════════════════════════════

; Anonymous erişim (0=kapalı, 1=açık)
; SP17+ varsayılan: 0
AllowAnonymous=0

; Minimum güvenlik modu
; 0=None kabul edilir, 1=en az Sign, 2=en az SignAndEncrypt
MinSecurityMode=2

; Sertifika iptal listesi (CRL) kontrolü
EnableCRLChecks=1

; ════════════════════════════════════════
; PERFORMANS PARAMETRELERİ
; ════════════════════════════════════════

; Session timeout (ms) - istemci bağlantı keserse timeout
SessionTimeout=30000

; Publish request zaman aşımı (ms)
PublishingTimeout=5000

; Minimum sampling interval (ms) - istemci daha hızlı isteyemez
MinSamplingInterval=100

; ════════════════════════════════════════
; LOGLAMA
; ════════════════════════════════════════

; OPC UA server log seviyesi
; 0=hiç, 1=hata, 2=uyarı, 3=bilgi, 4=debug
LogLevel=2
```

### Session ve Subscription Limitleri Hesaplama

```
Örnek: Bir SCADA + bir Python monitoring script + bir UaExpert debug

Gereken minimum:
  Sessions : 3 (her bağlantı = 1 session)
  
  Subscriptions per client:
    SCADA  : 3 subscription (hızlı/orta/yavaş)
    Python : 1 subscription
    UaExpert: 1 subscription
  MaxSubscriptions = 5
  
  MonitoredItems:
    SCADA  : 200 değişken (3 subscription'da dağılmış)
    Python : 50 değişken
    UaExpert: değişken (test amaçlı)
  MaxMonitoredItems = 500 (güvenlik payı)

CODESYSControl.cfg:
  MaxSessions=5
  MaxSubscriptions=20     (yedek pay ile)
  MaxMonitoredItems=1000  (yedek pay ile)
```

### Sertifika Klasör Yapısı (Linux)

```bash
# CODESYS OPC UA PKI klasörü (Linux)
/var/opt/codesys/PlcLogic/Application/pki/

# veya daha yeni kurulumlar:
/etc/codesys/pki/

# İçerik:
ls -la /var/opt/codesys/PlcLogic/Application/pki/
  own/      ← Sunucunun sertifika ve private key
  trusted/  ← Güvenilen istemci sertifikaları
  rejected/ ← Reddedilen (henüz güvenilmeyen) sertifikalar
  issuers/  ← Güvenilen CA sertifikaları

# İstemci sertifikasını güven listesine ekle
cp rejected/certs/[client_cert].der trusted/certs/
# Runtime restart gerekmez — otomatik algılar
```

### Performance Tuning

```
Yüksek frekanslı subscription yükü altında CODESYS OPC UA:

Problem: Çok sayıda istemci + hızlı subscription → CPU yükü artışı
Ölçüm: Task Monitor → OPC UA task'ının exec time'ı

Optimizasyon 1 — Sampling interval minimumunu artır:
  MinSamplingInterval=100   (100ms altı izin verilmez)
  → İstemcinin çok hızlı örnekleme yapmasını önler

Optimizasyon 2 — MonitoredItem limiti:
  MaxMonitoredItems=1000
  → 1000'den fazla değişken izlenirse yeni istemci reddedilir

Optimizasyon 3 — OPC UA task'ını ayrı CPU çekirdeğine pin:
  [CmpOPCUAServer]
  AffinityMask=0x4   ← Core 2 (binary: 0100)
  → OPC UA işlemleri kontrolü etkilemez

Optimizasyon 4 — Gereksiz değişkenleri Symbol Configuration'dan çıkar:
  Sadece gerçekten gerekli değişkenleri işaretle
  → Address space küçülür, browse hızlanır
```

## Pratikte Nasıl Kullanılır

### Adım 1: Runtime Bağlantı Doğrulama

```bash
# OPC UA server portuna bağlantı testi
telnet 192.168.1.100 4840

# veya netcat ile
nc -vz 192.168.1.100 4840

# Runtime log'dan OPC UA server başladı mı?
journalctl -u codesyscontrol | grep -i opcua
# [OPC UA Server] Listening on port 4840
```

### Adım 2: Symbol Configuration'ı Doğru Yapma

```
1. Application → Add Object → Symbol Configuration
2. Build → tüm değişkenler listede

3. Her değişken için erişim seviyesi:
   Kontrol çıkışları (xMotorRun): ReadWrite (SCADA yazabilir)
   Geri bildirimler (xMotorFB): Read (yalnızca okuma)
   Parametreler (rSetpoint): ReadWrite (operatör yazabilir)
   Dahili değişkenler (debug flags): İşaretleme (OPC UA'ya açma)

4. Symbol Set tanımla (opsiyonel):
   "ProductionData" → Üretim verileri (SCADA için)
   "MaintenanceData" → Teşhis verileri (bakım ekibi için)
   → Her set farklı kullanıcı grubuna açılabilir

5. Build → Download → Değişkenler OPC UA'da görünür
```

### Adım 3: Address Space Doğrulama (UaExpert)

```
UaExpert → Sunucuya bağlan → Address Space gezin:

Objects/
└── DeviceSet/
    └── CODESYS Control Linux ARM64 SL/
        └── Application/
            ├── GVL_IO/
            │   ├── xMotorRun   [Boolean, ReadWrite] ✓
            │   └── rTemperature [Double, Read] ✓
            └── GVL_Params/
                └── rSetpoint   [Double, ReadWrite] ✓

Kontrol listesi:
□ Beklenen tüm değişkenler görünüyor mu?
□ DataType doğru mu? (Boolean, Int16, Double...)
□ Access level doğru mu? (Read vs ReadWrite)
□ NodeId not alındı mı? (SCADA entegrasyonu için)
```

### Adım 4: SCADA Entegrasyonu İçin NodeID Listesi

```bash
# Python script ile tüm OPC UA node'larını otomatik listele
# Bu, SCADA konfigürasyonu için hazır tag listesi üretir

python3 list_opcua_nodes.py > opcua_tags.csv
```

```python
# list_opcua_nodes.py
import asyncio
from asyncua import Client

async def list_all_nodes(parent, depth=0, results=None):
    if results is None:
        results = []
    
    children = await parent.get_children()
    for child in children:
        browse_name = await child.read_browse_name()
        node_class = await child.read_node_class()
        
        if str(node_class) == "NodeClass.Variable":
            try:
                data_type = await child.read_data_type_as_variant_type()
                access = await child.read_access_level()
                results.append({
                    'NodeId': str(child.nodeid),
                    'Name': browse_name.Name,
                    'DataType': str(data_type),
                    'Access': str(access)
                })
            except:
                pass
        
        if depth < 5:  # Derinlik sınırı
            await list_all_nodes(child, depth+1, results)
    
    return results

async def main():
    async with Client("opc.tcp://192.168.1.100:4840") as client:
        objects = client.nodes.objects
        nodes = await list_all_nodes(objects)
        
        print("NodeId,Name,DataType,AccessLevel")
        for node in nodes:
            print(f"{node['NodeId']},{node['Name']},{node['DataType']},{node['Access']}")

asyncio.run(main())
```

## Örnekler

### Örnek 1: Çoklu Application ile OPC UA

```
Tek runtime, iki Application:
  Application_Production  → Üretim mantığı
  Application_Diagnostics → Teşhis araçları

Her Application kendi Symbol Configuration'ına sahip:
  Production  → GVL_IO, GVL_Params, GVL_Alarms → OPC UA'ya açık
  Diagnostics → GVL_Debug, GVL_Performance → Yalnızca bakım ekibine

OPC UA Server'da her Application ayrı namespace branch'i oluşturur:
  Objects/DeviceSet/[Runtime]/Application_Production/...
  Objects/DeviceSet/[Runtime]/Application_Diagnostics/...
```

### Örnek 2: OPC UA Method Tanımlama (Communication Manager ile)

```
Communication Manager → OPC UA Server → Add Method:

Method: "StartRecipe"
  Input  arguments: recipeId (Int32)
  Output arguments: success (Boolean), message (String)

IEC kodu:
  Application → PRG_OPCUAMethods → implement edilir
  
  (* OPC UA methodunun IEC tarafı *)
  PROGRAM PRG_OPCUAMethods
  VAR
      nRecipeRequest : INT;
      sMethodResult  : STRING;
  END_VAR
  
  IF nRecipeRequest > 0 THEN
      (* Reçete yükleme mantığı *)
      GVL_Params.nActiveRecipe := nRecipeRequest;
      sMethodResult := 'Recipe loaded successfully';
      nRecipeRequest := 0;
  END_IF
```

### Örnek 3: Yüksek Frekanslı Subscription için CODESYS Optimizasyonu

```ini
# CODESYSControl.cfg — Yüksek frekanslı OPC UA için
[CmpOPCUAServer]
ServerPort=4840
MaxSessions=5
MaxSubscriptions=20
MaxMonitoredItems=500

# OPC UA'ya özel CPU çekirdeği (CPU pinning)
# Core 3'te çalışır (binary: 1000)
AffinityMask=0x8

# Minimum sampling 100ms — daha hızlı isteği reddet
MinSamplingInterval=100

# Session timeout 60 saniye
SessionTimeout=60000

[SysProcess]
# CODESYS runtime çekirdeği: Core 0 ve Core 1
# OPC UA çekirdeği: Core 3 (yukarıda)
SetAffinityMask=0x3   # binary: 0011 = Core 0 ve 1
```

## Sık Yapılan Hatalar

### Hata 1: Symbol Configuration Build Sonrası Download Unutmak

```
Symbol Configuration değişti → Build edildi → Download yapılmadı.
OPC UA'da eski değişkenler görünüyor, yeniler yok.

Kural: Symbol Configuration değişikliği her zaman:
  Build → Download → (Online Start)
```

### Hata 2: NodeID'yi Runtime Adından Bağımsız Düşünmek

```
NodeId: ns=4;s=|var|CODESYS Control Win V3 x64.Application.GVL_IO.xMotorRun

"CODESYS Control Win V3 x64" → Runtime adı.
Runtime değiştirilirse (Win → Linux ARM64) NodeId değişir!
Tüm SCADA tag'leri güncellenmesi gerekir.

Çözüm: Runtime adını belgele ve değiştirmemeye çalış.
         Veya Communication Manager ile custom namespace kullan —
         bu durumda NodeId runtime adından bağımsız.
```

### Hata 3: MaxSessions Sınırını Aşmak

```
Semptom: Yeni istemci bağlanamıyor, mevcut bağlantılar çalışıyor.
Neden  : MaxSessions doldu.
Teşhis : PLC Shell → log → "MaxSessions exceeded" mesajı

Acil: MaxSessions değerini artır, runtime'ı yeniden başlat.
Kalıcı: İstemci sayısını belirle + yedek pay + MaxSessions ayarla.
```

## Gerçek Proje Notları

**Not 1 — NodeID Değişikliğinin SCADA Felaketi**  
Runtime Windows'tan Linux'a taşındı. Runtime adı değişti: "CODESYS Control Win V3 x64" → "CODESYS Control Linux ARM64 SL". 500 SCADA tag'inin tamamı güncellenmesi gerekti — 2 günlük iş. Sonraki projeden itibaren Communication Manager ile custom namespace kullanıldı; runtime değişiminden bağımsız NodeID'ler kullanılıyor.

**Not 2 — MaxMonitoredItems Limitinin Keşfi**  
Bir SCADA sistemi 2000 MonitoredItem açmaya çalışıyordu. MaxMonitoredItems=1000 ile ilk 1000 alındı, sonraki 1000 hata döndü. SCADA'nın neden bazı tag'lerin değerini alamadığı 2 saat anlaşılamadı. CODESYSControl.cfg'de MaxMonitoredItems=3000'e yükseltildi, sorun çözüldü.

**Not 3 — Symbol Configuration ile Hassas Veri Açığı**  
Bir projede "tüm değişkenleri işaretle" seçeneği kullanıldı. GVL_Config içindeki makine seri numarası, kalibrasyon katsayıları ve üretim reçeteleri de OPC UA'ya açıldı. Güvenlik denetiminde "aşırı açıklama" olarak işaretlendi. Sonraki versiyonda yalnızca gerekli değişkenler işaretlendi.

## İlgili Konular

```
knowledge/protocols/opc-ua/
├── 01_architecture.md           → OPC UA genel mimari ve endpoint
├── 02_address_space.md          → Namespace ve NodeID detayları
├── 03_security.md               → Sertifika ve güvenlik yapılandırma
├── 04_subscriptions.md          → Subscription parametre optimizasyonu
└── 06_client_implementations.md → İstemci tarafında NodeID kullanımı

knowledge/codesys/networking/
└── 01_opcua_server.md           → CODESYS OPC UA hızlı kurulum rehberi
```
