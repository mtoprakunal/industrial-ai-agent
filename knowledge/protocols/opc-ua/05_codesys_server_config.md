---
KONU        : CODESYS OPC-UA Sunucu Detaylı Konfigürasyonu
KATEGORİ    : protocols
ALT_KATEGORI: opc-ua
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
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

**Not 4 — Symbol Set'in OnlineChange'te Sessizce Bozulması**  
Çalışan bir hatta OnlineChange ile yeni değişken eklendi ve Symbol Configuration "Build" edildi. Ama eklenen değişken Symbol Set'e dahil edilmediğinden bazı istemciler onu göremedi; bazıları gördü. Karışıklığın nedeni: OnlineChange adres uzayını yeniden üretir ve bu sırada NodeId'ler ve set üyelikleri değişebilir; bazı istemcilerin subscription'ları geçersiz NodeId'lere düştü ve sessizce `Bad` döndü. Ders: adres uzayını etkileyen Symbol Configuration değişiklikleri OnlineChange ile değil, planlı download + istemci yeniden bağlanmasıyla yapılmalı.

**Not 5 — `MinSamplingInterval=0` Bırakıldığı İçin DoS Benzeri Yük**  
CODESYSControl.cfg'de `MinSamplingInterval` ayarlanmamıştı (varsayılan 0). Üçüncü parti bir istemci yanlışlıkla sampling=0 ile 800 MonitoredItem açtı. Sunucu her PLC scan'inde tümünü örneklemeye çalıştı; OPC UA task exec time kontrol task'ını geciktirdi ve watchdog tetiklendi. Sunucu tarafında `MinSamplingInterval=100` kelepçesi konunca istemci ne isterse istesin minimum 100ms'ye sabitlendi. Ders: istemciye güvenme — sunucu tarafında sert kelepçe koy.

**Not 6 — Lisans Sınırlı Node Sayısı Sürprizi**  
Bazı CODESYS runtime lisansları (özellikle OEM/küçük PLC) OPC UA'da yayınlanabilen node sayısını veya eş zamanlı session'ı lisansla sınırlar. 1500 değişken işaretlendi ama runtime yalnızca ilk N tanesini yayınladı, gerisi sessizce eksik kaldı. PLC Shell log'unda lisans uyarısı vardı ama fark edilmedi. Ders: hedef runtime'ın OPC UA lisans sınırlarını (node/session) devreye almadan önce doğrula; "çalışıyor ama eksik" en sinsi hatadır.

## Edge Case'ler ve Sistem Limitleri

CODESYS OPC UA sunucusunun sınırları hem runtime kotalarından hem de adres uzayının runtime adına bağlı olmasından kaynaklanır:

| Edge Case | Neden | Belirti | Önlem |
|---|---|---|---|
| RuntimeName NodeId'de | String NodeId runtime adını içerir | Platform/isim değişince tüm tag bozulur | Custom namespace (Comm.Manager) |
| OnlineChange + Symbol | Adres uzayı yeniden üretilir | Subscription `Bad`'a düşer | Planlı download + reconnect |
| Lisans node/session limiti | OEM runtime kısıtı | Sessiz eksik yayın | Lisansı önceden doğrula |
| `MaxSessions=0` | "Sınırsız" = kaynak tükenmesi | Bellek/CPU spike, DoS | Daima sonlu limit |
| `MinSamplingInterval=0` | İstemci sunucuyu boğabilir | Watchdog/kontrol gecikmesi | ≥100ms kelepçe |
| Sertifika klasör yolu sürümle değişti | `/var/opt/.../pki` vs `/etc/codesys/pki` | Trust işe yaramaz | Doğru yolu logla/doğrula |
| Symbol Set ≠ kullanıcı eşlemesi | Set tanımlı ama role bağlanmamış | Yetkisiz veri görünür | Set'i erişim haklarına bağla |
| BOOL array / büyük struct | Encoding limiti / decode sorunu | `Bad` veya ham byte | Tip tanımı yükle, boyut sınırla |

Kritik sınır gerçekleri:
- **`MaxSessions=0` tehlikelidir.** "Sınırsız" pratikte gömülü cihazda bellek/CPU tükenmesine ve DoS'a açık kapı bırakır; her zaman sonlu, gerçek ihtiyaç + pay olan bir değer ver.
- **Sertifika klasör yolu runtime sürümüne göre değişir.** Eski kurulumlarda `/var/opt/codesys/PlcLogic/Application/pki`, yeni kurulumlarda `/etc/codesys/pki` olabilir; yanlış yola sertifika koymak "trusted'a aldım ama hâlâ reddediyor" hatasının klasik kaynağıdır.
- **Symbol Configuration yayınladığın her şeyi yayınlar.** "Tümünü işaretle" kolaylığı, kalibrasyon/reçete/seri-no gibi hassas veriyi de açar; bu bir bilgi sızıntısıdır.

## Optimizasyon

CODESYS sunucu tarafı optimizasyonu hem performans hem kararlılık içindir; kontrol döngüsünün OPC UA yükünden etkilenmemesi önceliklidir:

1. **OPC UA task'ını izole et (CPU pinning + öncelik).** `AffinityMask` ile OPC UA'yı kontrol task'larından ayrı çekirdeğe pin'le; OPC UA yükü asla kontrol jitter'ını etkilemesin. Çok çekirdekli cihazda en yüksek kararlılık kazancı budur.
2. **`MinSamplingInterval` kelepçesi koy (≥100ms).** İstemcinin sunucuyu boğmasını sunucu tarafında kesin engeller — istemci politikasına güvenme.
3. **Adres uzayını sadeleştir.** Yalnızca dışarı gereken değişkenleri işaretle. Daha az node = daha hızlı browse, daha az bellek, daha küçük saldırı yüzeyi, daha hızlı OnlineChange.
4. **Limitleri gerçeğe göre boyutlandır.** `MaxSessions`, `MaxSubscriptions`, `MaxMonitoredItems` = beklenen yük + makul pay. Çok yüksek limit kaynak israfı, çok düşük limit sessiz red.
5. **Custom namespace ile NodeId'yi runtime'dan bağımsızlaştır.** Communication Manager ile sabit namespace URI, runtime/platform değişiminde tag güncelleme maliyetini (Not 1'deki 2 günlük iş) sıfırlar.
6. **LogLevel'ı üretimde düşür.** `LogLevel=4 (debug)` kalırsa yoğun trafik altında loglama I/O'su ek yük yaratır; üretimde 1-2 yeterli.
7. **Toplu erişimi teşvik et.** İstemci tarafına toplu Read/Write ve tek subscription kullandırmak sunucu round-trip ve subscription tablosu yükünü azaltır.

## Derin Teknik Detay

**Symbol Configuration ile Communication Manager — neden iki mimari?** Symbol Configuration, IEC değişkenlerini (GVL üyelerini) doğrudan ve otomatik bir adres uzayına yansıtır; NodeId'ler `|var|RuntimeName.App.GVL.Var` formülüyle deterministik üretilir. Bu kolaylık bir bedelle gelir: adres uzayı CODESYS'in iç proje yapısına ve runtime adına *bağlıdır* — yani bilgi modeli aslında "ham değişken dökümü"dür, semantik tip sistemi içermez. Communication Manager + OPC UA Server nesnesi ise gerçek bir information model katmanı sunar: custom namespace, ObjectType, Method, kontrollü hiyerarşi. Bedeli manuel kurulum; getirisi runtime'dan bağımsız NodeId, companion specification uyumu ve method desteğidir. Doğru karar: basit SCADA/HMI için Symbol Configuration, müşteriye-açık/standart-uyumlu/method-gerektiren sistemler için Communication Manager.

**NodeId'nin runtime adına bağlanmasının kök nedeni.** Symbol Configuration NodeId'yi runtime adından türetir çünkü tek bir OPC UA sunucusu teorik olarak birden çok runtime/application barındırabilir ve bunları ayırt etmek gerekir. Ancak pratikte bu, runtime adı değişince (Windows→Linux taşıması, platform yükseltmesi) tüm string NodeId'leri kıran kırılganlık yaratır. Bu, "deterministik üretim" ile "stabilite" arasındaki bir takastır; custom namespace bu takası kullanıcı kontrolüne verir.

**MinSamplingInterval neden sunucu tarafında zorunlu kelepçe?** OPC UA'da sampling interval'i istemci ister ama sunucu revize edebilir. CODESYS'te OPC UA örnekleme, runtime task scheduler'ı içinde çalışır; çok düşük sampling, OPC UA task'ının CPU bütçesini tüketip kontrol task'larıyla yarışmasına yol açar. `MinSamplingInterval`, istemci ne isterse istesin sunucunun kabul edeceği tabandır — bu, kontrol determinizmini istemci davranışından koruyan bir güvenlik supabıdır. Bu yüzden CODESYS'te OPC UA "best effort" katmandır ve asla gerçek-zamanlı kontrol döngüsünün yerini almamalıdır.

**OnlineChange ve adres uzayı tutarlılığı.** CODESYS OnlineChange, çalışan PLC'yi durdurmadan kod günceller; ama Symbol Configuration'ı etkileyen değişiklikler adres uzayının yeniden üretilmesini gerektirebilir. Bu sırada NodeId'ler ve continuation point'ler geçersizleşebilir, açık subscription'lar kopuk NodeId'lere düşer. Bunun nedeni adres uzayının çalışma-zamanı türetilmiş olmasıdır: kod değişince türetilen yapı da değişir. Bu yüzden adres uzayını etkileyen değişiklikler OnlineChange ile değil, planlı bir bakım penceresinde download + istemci reconnect ile yapılmalıdır — aksi halde "bazı istemciler görüyor, bazıları görmüyor" türü tutarsızlıklar oluşur.

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
