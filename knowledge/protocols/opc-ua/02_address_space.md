---
KONU        : OPC-UA Adres Uzayı Tasarımı
KATEGORİ    : protocols
ALT_KATEGORI: opc-ua
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://reference.opcfoundation.org/Core/Part3/v104/docs/4"
    başlık: "OPC Foundation — UA Part 3: Address Space Model"
    güvenilirlik: resmi
  - url: "https://reference.opcfoundation.org/DI/v102/docs/4.2.1/"
    başlık: "OPC Foundation — Information Modelling in OPC UA"
    güvenilirlik: resmi
  - url: "https://profanter.medium.com/opc-ua-address-space-explained-a6d7ee9f6a12"
    başlık: "Medium — OPC UA Address Space Explained (Stefan Profanter)"
    güvenilirlik: topluluk
  - url: "https://documentation.unified-automation.com/uasdkhp/1.0.0/html/_l2_ua_node_classes.html"
    başlık: "Unified Automation — OPC UA Node Classes"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_architecture.md"
    ilişki: gerektirir
  - konu: "03_security.md"
    ilişki: tamamlar
  - konu: "04_subscriptions.md"
    ilişki: kullanır
  - konu: "05_codesys_server_config.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "OPC UA temel mimarisi (01_architecture.md)"
  - "Nesne yönelimli programlama kavramları (sınıf, örnek, kalıtım)"
ÇELİŞKİLER :
  - kaynak: "Namespace index vs namespace URI kullanımı"
    konu: "Namespace index (ns=4) server'a göre değişir; URI sabit kalır"
    çözüm: >
      Hardcoded namespace index (ns=4;s=...) kullanmak kırılgandır.
      Aynı server farklı kurulumda farklı namespace index'i verebilir.
      Güvenli yaklaşım: Session başlangıcında namespace URI'dan
      get_namespace_index() ile index'i dinamik al, sonra kullan.
  - kaynak: "Flat vs hierarchical address space tasarımı"
    konu: "Tüm değişkenleri tek düz liste olarak sunmak kolaydır ama kötü pratiktir"
    çözüm: >
      Flat yapı: Kolay üretim, SCADA uyumlu ama keşfedilemez, anlamsız.
      Hierarchical yapı: Cihaz → Ünite → Ölçüm → Değer şeklinde gruplama.
      OPC UA'nın asıl gücü hiyerarşik, anlamlı bilgi modelidir.
      Flat yapı OPC Classic'i taklit eder — OPC UA'nın değerini düşürür.
---

## Özün Ne

OPC UA adres uzayı (Address Space), bir sunucunun istemcilere sunduğu tüm bilginin organize edildiği hiyerarşik yapıdır. Dosya sistemindeki klasörler gibi düşünülebilir; ancak çok daha zengindir: Yalnızca değerleri değil, tipleri, ilişkileri, metodları ve metadata'yı da barındırır. İyi tasarlanmış bir adres uzayı, istemcinin sunucuyu hiç bilmeden keşfedip anlayabilmesini sağlar. Kötü tasarlanmış bir adres uzayı ise OPC UA'yı pahalı bir Modbus'a dönüştürür.

## Nasıl Çalışır

### Adres Uzayı Temel Yapısı

Her OPC UA sunucusu, standart kök yapısıyla başlar:

```
Root (ns=0;i=84)
├── Objects (ns=0;i=85)      ← Uygulama nesneleri buraya girer
│   ├── Server               ← Sunucu kendisi hakkında bilgi
│   │   ├── ServerStatus
│   │   ├── Namespaces
│   │   └── ServerCapabilities
│   └── [Uygulama Nesneleri] ← Sizin tanımladıklarınız
│
├── Types (ns=0;i=86)        ← Tip tanımları
│   ├── DataTypes
│   ├── ReferenceTypes
│   ├── ObjectTypes
│   └── VariableTypes
│
└── Views (ns=0;i=87)        ← Özel görünümler (opsiyonel)
```

### 8 Node Sınıfı

OPC UA, 8 standart node sınıfı tanımlar. Bunların ötesinde yeni sınıf tanımlanamaz.

---

#### Object Node (Nesne)

Fiziksel veya mantıksal bir varlığı temsil eder. Bir sistemin, cihazın veya yazılım bileşeninin kabuğudur.

```
Motor1 (Object)
├── RunCommand  (Variable)   ← Çalıştırma komutu
├── RunFeedback (Variable)   ← Çalışma geri bildirimi
├── FaultStatus (Variable)   ← Arıza durumu
├── TotalRuntime (Variable)  ← Toplam çalışma süresi
└── Reset()     (Method)     ← Arıza sıfırlama metodu
```

---

#### Variable Node (Değişken)

Gerçek değer taşıyan node. OPC UA'da iki tür Variable vardır:

```
1. DataVariable: Ölçüm değeri, komut değeri gibi asıl veri.
   Örnek: Motor1.RunFeedback (BOOL)
          Motor1.Speed (FLOAT, rpm)

2. Property: Object'in özelliği/metadata'sı.
   Örnek: Motor1.Manufacturer ("Siemens")
          Motor1.SerialNumber ("SN-20240115-001")
          Motor1.MaxRPM (3000.0)
   
Fark: DataVariable alt değişkenlere sahip olabilir.
      Property yaprak node'dur, alt node alamaz.
```

Variable'ın kritik attribute'ları:

| Attribute | Açıklama | Örnek |
|---|---|---|
| NodeId | Benzersiz tanımlayıcı | `ns=4;s=Motor1.Speed` |
| BrowseName | Programatik isim | `"Speed"` |
| DisplayName | Görüntüleme ismi | `"Motor 1 Hız"` |
| DataType | Veri tipi | Double, Boolean, String... |
| Value | Güncel değer | `1450.5` |
| StatusCode | Değerin kalitesi | `Good`, `Bad`, `Uncertain` |
| SourceTimestamp | Verinin üretim zamanı | `2026-06-01T10:22:15Z` |
| ServerTimestamp | Sunucuya ulaşma zamanı | `2026-06-01T10:22:15.005Z` |
| AccessLevel | Okuma/yazma izni | `Read`, `ReadWrite` |
| Historizing | Geçmiş kaydediliyor mu | `True/False` |

---

#### Method Node (Metot)

Sunucuda çalıştırılabilecek bir fonksiyonu temsil eder. İstemci parametre gönderir, sunucu çalıştırır ve sonuç döner.

```
Reset() : No Input → StatusCode Output
StartRecipe(recipeId: Int32) : Int32 → Boolean, String
Calibrate(zeroOffset: Double, span: Double) : Double, Double → StatusCode
```

---

#### DataType Node (Veri Tipi)

Karmaşık yapıları (struct benzeri) tanımlar. OPC UA'da tüm tipler tip ağacında tanımlanır.

```
BaseDataType
├── Boolean
├── Number
│   ├── Integer (Int16, Int32, Int64...)
│   └── Float (Double, Float)
├── String
├── DateTime
├── Structure (kullanıcı tanımlı struct)
│   └── MotorStatus (özel struct)
│       ├── IsRunning : Boolean
│       ├── FaultCode : UInt32
│       └── CurrentSpeed : Double
└── Enumeration
    └── MotorState : {Idle=0, Starting=1, Running=2, Fault=3}
```

---

#### ObjectType, VariableType (Tip Tanımları)

Object'lerin ve Variable'ların şablonları. Sınıf gibi — örneklenebilir.

```
MotorType (ObjectType)
├── RunCommand  : VariableType (Boolean, ReadWrite)
├── RunFeedback : VariableType (Boolean, Read)
├── Speed       : VariableType (Double, Read, Unit: rpm)
└── Reset()     : MethodType

Motor1 : MotorType    ← Şablondan örnek
Motor2 : MotorType    ← Şablondan örnek
```

### Reference (İlişki)

Node'lar birbirine Reference (ilişki) ile bağlanır. Referans, yönlü bir bağlantıdır ve bir tip bilgisi taşır.

```
Temel reference tipleri:
  HierarchicalReferences (hiyerarşik):
    HasComponent    : Object → alt object/variable/method
    HasProperty     : Object → property (metadata)
    Organizes       : Klasör → içerik
    HasSubtype      : Tip → alt tip
    
  NonHierarchicalReferences:
    HasTypeDefinition: Instance → Tip tanımı
    HasEncoding     : DataType → kodlama
    GeneratesEvent  : Nesne → oluşturduğu olay tipi
```

### NodeId Yapısı

Her node, adres uzayında benzersiz bir kimliğe (NodeId) sahiptir.

```
NodeId formatları:

Sayısal (Numeric):  ns=0;i=2253   (Standart OPC UA node'ları için)
String:             ns=4;s=|var|CODESYS.Application.GVL_IO.xMotorRun
GUID:               ns=1;g=550e8400-e29b-41d4-a716-446655440000
Opaque (binary):    ns=2;b=M/RbKs...  (nadir)

Bileşenler:
  ns = namespace index (0 = OPC UA standart, 1+ = uygulama tanımlı)
  i  = integer identifier
  s  = string identifier
  g  = GUID identifier
  b  = binary identifier
```

**Namespace:**
```
ns=0 : OPC UA Foundation tarafından tanımlı standart node'lar
ns=1 : Genellikle OPC UA DI (Device Integration) companion spec
ns=2 : Üçüncü parti companion spec veya uygulama
ns=3 : ...
ns=4 : CODESYS'in kendi namespace'i (tipik kurulum)

Namespace URI (sabit, taşınabilir):
  "http://www.3s-software.com/schemas/Codesys-V3"
  
Namespace Index (değişken, kuruluma göre):
  Session başlangıcında: nsIndex = client.get_namespace_index(uri)
```

## Pratikte Nasıl Kullanılır

### İyi Adres Uzayı Tasarımı

**Makine Ekipman Modeli (ISA-88 / ISA-95 uyumlu):**

```
Objects/
└── PackagingLine1 (Object, type: PackagingLineType)
    ├── ConveyorUnit (Object, type: ConveyorType)
    │   ├── Status (Object)
    │   │   ├── IsRunning  (Variable, Boolean)
    │   │   ├── FaultCode  (Variable, UInt32)
    │   │   └── FaultMsg   (Variable, String)
    │   ├── Control (Object)
    │   │   ├── StartCmd   (Variable, Boolean, ReadWrite)
    │   │   ├── StopCmd    (Variable, Boolean, ReadWrite)
    │   │   └── SpeedSP    (Variable, Double, ReadWrite, Unit:%)
    │   ├── Measurements (Object)
    │   │   ├── ActualSpeed (Variable, Double, Read, Unit:m/min)
    │   │   └── RunningTime (Variable, Duration, Read)
    │   └── Start()    (Method)
    │
    ├── TemperatureZone1 (Object, type: TemperatureControlType)
    │   ├── ActualTemp     (Variable, Double, Read, Unit:°C)
    │   ├── SetpointTemp   (Variable, Double, ReadWrite, Unit:°C)
    │   └── HeaterOutput   (Variable, Double, Read, Unit:%)
    │
    └── Alarms (Object)
        ├── ActiveAlarmCount (Variable, UInt32, Read)
        └── AcknowledgeAll() (Method)
```

**Kötü (Flat) Adres Uzayı — Kaçınılması Gereken:**

```
Objects/
└── Machine (Object)
    ├── xMotorRun     (Variable)   ← Hangi motor? Ne için?
    ├── rSetpoint     (Variable)   ← Neyin setpoint'i?
    ├── bAlarm1       (Variable)   ← Hangi alarm?
    ├── nCount        (Variable)   ← Ne sayıyor?
    └── ... (300 değişken aynı seviyede)
    
→ İstemci hiçbir şeyi anlayamaz, her şey hardcoded NodeId gerektirir.
```

### UaExpert ile Adres Uzayı Keşfi

```
1. UaExpert → Server → Add → opc.tcp://IP:4840
2. Server → Connect
3. Address Space sekmesi açılır:
   Objects → DeviceSet → [Controller] → Application → ...
4. İncelemek istediğin node'a çift tıkla
   → Attributes (NodeId, DisplayName, DataType, Value...) görürsün
5. Data Access View'e sürükle → Canlı değer izle
6. NodeId'yi not al: ns=4;s=|var|...
```

## Örnekler

### Örnek 1: Python ile Adres Uzayı Gezinti

```python
import asyncio
from asyncua import Client

async def browse_address_space():
    async with Client("opc.tcp://192.168.1.100:4840") as client:
        
        # Namespace index'i dinamik al (taşınabilir!)
        ns_uri = "http://www.3s-software.com/schemas/Codesys-V3"
        ns_idx = await client.get_namespace_index(ns_uri)
        print(f"Namespace index: {ns_idx}")
        
        # Objects klasöründen başla
        objects = client.nodes.objects
        
        # Alt node'ları listele
        children = await objects.get_children()
        for child in children:
            name = await child.read_browse_name()
            node_class = await child.read_node_class()
            print(f"  {name.Name} [{node_class}]")
        
        # Belirli bir node'u string NodeId ile bul
        node_id = f"ns={ns_idx};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun"
        motor_node = client.get_node(node_id)
        
        # Node attribute'larını oku
        value = await motor_node.read_value()
        data_type = await motor_node.read_data_type_as_variant_type()
        access_level = await motor_node.read_access_level()
        
        print(f"Motor Run: {value}")
        print(f"DataType: {data_type}")
        print(f"AccessLevel: {access_level}")

asyncio.run(browse_address_space())
```

### Örnek 2: Yapısal Tip (MotorStatus) Okuma

```python
# Sunucu MotorStatus struct yayınlıyorsa:
import asyncio
from asyncua import Client
from asyncua import ua

async def read_struct():
    async with Client("opc.tcp://192.168.1.100:4840") as client:
        
        motor_status_node = client.get_node("ns=4;s=Motor1.Status")
        
        # Struct değeri al
        value = await motor_status_node.read_value()
        
        # value bir ExtensionObject veya dictionary
        print(f"IsRunning: {value.IsRunning}")
        print(f"FaultCode: {value.FaultCode}")
        print(f"CurrentSpeed: {value.CurrentSpeed}")

asyncio.run(read_struct())
```

### Örnek 3: Method Çağrısı

```python
async def call_method():
    async with Client("opc.tcp://192.168.1.100:4840") as client:
        
        # Motor nesnesinin Reset metodunu çağır
        motor_object = client.get_node("ns=4;s=Machine.Motor1")
        
        # Metot çağrısı (input param: fault_code)
        result = await motor_object.call_method(
            "ns=4;s=Machine.Motor1.Reset",
            ua.Variant(42, ua.VariantType.UInt32)  # FaultCode parametresi
        )
        
        print(f"Reset result: {result}")

asyncio.run(call_method())
```

### Örnek 4: CODESYS'te Adres Uzayını Genişletme

CODESYS'te Symbol Configuration dışında, Communication Manager + OPC UA Server ile custom node eklenebilir:

```
Application → Communication Manager → OPC UA Server →
    Add Object: "PackagingLine1"
    Add Variable: "TotalProduction" (DWORD)
    Add Method: "ResetCounters"
    
→ Bu yaklaşım daha zengin bilgi modeli sağlar ama yapılandırması karmaşıktır.
→ Basit senaryolar için Symbol Configuration yeterli.
```

## Sık Yapılan Hatalar

### Hata 1: Namespace Index Hardcode Etmek

```python
# ❌ YANLIŞ — Farklı sunucuda ns=4 olmayabilir
node = client.get_node("ns=4;s=Motor1.Speed")

# ✅ DOĞRU — Dinamik al
ns = await client.get_namespace_index("http://www.3s-software.com/schemas/Codesys-V3")
node = client.get_node(f"ns={ns};s=Motor1.Speed")
```

### Hata 2: Property ile DataVariable Karıştırmak

```
Property: Sunucu tanımlı metadata, değişmez veya nadir değişir.
  Örnek: Motor.Manufacturer, Motor.MaxRPM
  → Subscribe etmek anlamsız — nadiren değişir.

DataVariable: Proses değişkeni, sık değişir.
  Örnek: Motor.Speed, Motor.Current
  → Subscribe et, izle.

Fark önemli: Client property'ye subscribe olmamalı;
             DataVariable'lar için subscription kurulmalı.
```

### Hata 3: Tüm Değişkenleri Tek Namespace'e Koymak

```
❌ Yanlış: Tüm node'lar ns=4'te, standart tip referansları karışık
✅ Doğru :
  ns=0 → OPC UA Foundation standart tipleri (BaseObjectType vb.)
  ns=1 → Companion spec tipleri (DI/Devices)
  ns=4 → Uygulama instance'ları (sizin makineniz)
```

### Hata 4: Büyük Binary Değerleri DataVariable Olarak Sunmak

OPC UA, küçük-orta büyüklükte process değerleri için optimize edilmiştir. Büyük binary veri (görüntü, log dosyası) için OPC UA File Transfer Service veya harici mekanizma kullanılmalıdır.

## Ne Zaman Tercih Edilmeli / Edilmemeli

**Zengin bilgi modeli kur:**
- Sistemin farklı ekiplerle paylaşılacağı (SCADA, MES, IT)
- Companion specification uyumluluk gerektiğinde
- Müşterinin OPC UA'yı "kendi başına keşfedebilmesini" istediğinde

**Basit flat yapı yeterli:**
- İç kullanım, tek istemci, tüm NodeID'ler hardcoded
- Prototip veya geçici entegrasyon
- OPC Classic'ten geçiş (uyumluluk önceliği)

## Gerçek Proje Notları

**Not 1 — Flat Yapının Bakım Maliyeti**  
İlk OPC UA projemizde 400 değişkeni düz bir Object altında sundu. 6 ay sonra yeni SCADA entegratörü projeye dahil oldu ve hangi tag'in ne anlama geldiğini anlamak için 2 gün harcadı. Hiyerarşik yapıya geçildi; sonraki entegrasyon 4 saatte tamamlandı.

**Not 2 — Companion Specification Sürprizi**  
B&R Automation üretici firmaya OPC UA DI (Device Integration) uyumlu PLC sattı. SCADA istemcisi DI standardını anlıyor ve otomatik keşfediyordu. Custom node haritalaması yazmak yerine standartta tanımlı Modules/DeviceName, Modules/SerialNumber gibi node'ları doğrudan kullandık. Entegrasyon süresi %70 azaldı.

**Not 3 — Method'ların Gücü**  
Reset, Calibrate, StartRecipe gibi operasyonlar artık OPC UA Method ile istemciden çağrılıyor. Eskiden ayrı Modbus register'ları ile "komut register" protokolü tasarlamak gerekiyordu. Method'larla çok daha temiz ve belgeli bir arayüz elde ettik.

**Not 4 — BrowseName vs DisplayName Karışıklığının Entegrasyon Bozması**  
Bir SCADA entegratörü tag'leri DisplayName ("Motor 1 Hız") ile path'leyince entegrasyon başka bir lokalizasyon kurulumunda bozuldu — DisplayName lokalize (LocalizedText) ve değişebilir; BrowseName ise QualifiedName (namespace + sabit string) ve API kontratının parçasıdır. Çözüm: BrowsePath/RelativePath daima BrowseName ile kurulur, DisplayName yalnızca operatöre gösterilir. Bu ayrımı netleştirdikten sonra "Türkçe HMI'da çalışıyor, İngilizce'de bozuluyor" sınıfı hatalar bitti.

**Not 5 — TranslateBrowsePathsToNodeIds ile NodeId Kırılganlığını Aşmak**  
String NodeId'leri (`ns=4;s=...`) tüm istemcilere gömmek runtime adı değişince yüzlerce tag'i bozuyordu. Çözüm: istemci başlangıçta bilinen BrowsePath'lerden (`/Objects/PackagingLine1/ConveyorUnit/Speed`) `TranslateBrowsePathsToNodeIds` servisiyle NodeId'leri runtime'da çözüp cache'ledi. Path semantik olarak sabit; NodeId fiziksel olarak değişse de path aynı kalıyor. Bu, NodeId kırılganlığına karşı en sağlam endüstriyel desen oldu.

**Not 6 — Struct (ExtensionObject) Okumada DataTypeDefinition Eksikliği**  
Bir CODESYS struct'ı (MotorStatus) okurken eski bir istemci alanları çözemedi, ham byte aldı. Neden: istemci sunucudan tip tanımını (DataTypeDefinition / BSD/binary type description) almamıştı; struct'lar self-contained değildir, decode için tip şeması gerekir. asyncua'da `load_data_type_definitions()` çağrılınca alanlar isimleriyle geldi. Custom struct kullanan her projede tip yükleme adımı zorunlu kontrol listesine girdi.

## Edge Case'ler ve Sistem Limitleri

Adres uzayının sınırları çoğunlukla "node sayısı" değil, "node'ların nasıl çözüldüğü ve serileştirildiği" ile ilgilidir:

| Edge Case | Davranış | Risk | Önlem |
|---|---|---|---|
| Namespace index ≠ NodeId sabitliği | Index kuruluma/restart sırasına göre değişebilir | Hardcoded `ns=4` bozulur | URI'dan dinamik çöz |
| NamespaceArray sırası | ns=0 sabit, geri kalan sunucu yüklemesine bağlı | İndeks kayması | NamespaceArray oku, eşle |
| Symbol explosion | Binlerce node = devasa adres uzayı | Browse yavaş + saldırı yüzeyi | Yalnızca gerekli node'u yayınla |
| Döngüsel referans (cyclic) | Browse sonsuz döngüye girebilir | İstemci asılır | Derinlik limiti + ziyaret seti |
| ExtensionObject (struct) | Decode için DataTypeDefinition şart | Ham byte / `Bad` | Tip tanımı yükle |
| String NodeId byte limiti | Çok uzun string NodeId reddedilir | `BadNodeIdInvalid` | NodeId'leri kısa tut |
| Modelling rule (Mandatory/Optional) | Instance'da Optional üyeler eksik olabilir | Beklenen node yok | Tip yerine instance browse et |
| AccessLevel vs UserAccessLevel | İlki tipsel, ikincisi kullanıcıya özel | Yazma "izin yok" döner | UserAccessLevel kontrol et |

Kritik sınır davranışları:
- **NodeId stabilitesi = API kontratı.** Bir NodeId yayımlandıktan sonra değiştirmek, REST API'de endpoint'i sessizce değiştirmek gibidir. String NodeId'ler CODESYS'te runtime adına bağlıdır; bu yüzden ya custom namespace kullanılır ya da BrowsePath ile çözülür.
- **Property yaprak olmak zorunda.** Property'ye alt node bağlamak spec ihlalidir; bazı istemciler bunu tolere etmez. Hiyerarşi taşıyacak metadata DataVariable olmalıdır.
- **Symbol explosion bir güvenlik konusudur.** Her açılan node hem keşif yüzeyi hem potansiyel yazma hedefidir; gereksiz iç değişkenleri yayınlamak bilgi sızıntısı ve saldırı yüzeyi yaratır.

## Optimizasyon

Adres uzayı optimizasyonu iki cephededir: tasarım-zamanı (model boyutu) ve çalışma-zamanı (erişim deseni). Öncelik sırası:

1. **NodeId'yi BrowsePath ile bir kez çöz, sonra cache'le.** Her döngüde browse/translate yapmak ağır servis çağrısıdır. Başlangıçta çöz, `Node` nesnesini ve çözülmüş NodeId'yi sakla; sonraki tüm Read/Write doğrudan NodeId ile gider.
2. **Toplu Read/Write.** Tek servis çağrısında onlarca node oku; round-trip maliyeti node sayısından bağımsız hale gelir.
3. **Adres uzayını küçük tut.** Yalnızca gerçekten dışarıya gereken node'ları yayınla. Daha küçük adres uzayı = daha hızlı browse, daha az bellek, daha küçük saldırı yüzeyi. "Her ihtimale karşı her şeyi aç" anti-deseni hem performans hem güvenlik borcudur.
4. **Tip tanımlarını (ObjectType) kullan.** Instance'ları tipten türetmek, istemcinin tek seferde tipi öğrenip tüm instance'lara uygulamasını sağlar; tekrarlı browse'u azaltır ve modeli kompaktlaştırır.
5. **Derin hiyerarşi yerine dengeli hiyerarşi.** 10 seviye derin ağaç browse'u yavaşlatır; 3-4 seviye + anlamlı gruplama hem okunur hem hızlıdır.
6. **DataType cache'leme.** Struct okurken DataTypeDefinition'ı bir kez yükle; her okumada tip şeması sorgulamak gereksizdir.

## Derin Teknik Detay

**NodeId neden bu kadar merkezi?** OPC UA'da her şey — node, tip, referans hedefi — bir NodeId ile adreslenir. NodeId, namespace index + identifier (numeric/string/guid/opaque) çiftidir. Numeric NodeId'ler en kompakt ve hızlı çözülenidir (sabit standart node'lar için ideal: `i=2253`); string NodeId'ler insan-okunur ama daha büyük ve genelde uygulama tarafından üretilir (CODESYS `s=|var|...`); GUID'ler global benzersizlik ister (cihazlar arası taşınabilir kimlik için). Bu çeşitlilik bilinçlidir: standart altyapı numeric ile sıkıştırılır, uygulama esnekliği string/guid ile sağlanır. Numeric NodeId çözümü sunucuda genelde hash/dizi araması iken string çözümü string karşılaştırması gerektirir — bu yüzden çok-erişilen node'lar için numeric tercih edilir.

**Referanslar neden çift-yönlü tutulur?** Her Reference hem kaynağında (forward) hem hedefinde (inverse) saklanır: `Motor1 --HasComponent--> Speed` aynı zamanda `Speed --ComponentOf--> Motor1` olarak gezilebilir. Bu, adres uzayını gerçek bir graf yapar; istemci yukarı, aşağı veya yana gezebilir. Maliyeti bellek (her ilişki iki yerde), getirisi keşfedilebilirlik. ReferenceType'ların kendisi de adres uzayında node olarak tanımlıdır (ns=0 altında HierarchicalReferences ağacı), yani ilişki türleri de self-describing'dir.

**HasTypeDefinition: instance ile tip arasındaki köprü.** Her Object/Variable instance'ı bir `HasTypeDefinition` referansıyla tipine (ObjectType/VariableType) bağlanır. İstemci bu referansı izleyerek "bu bir MotorType örneği" bilgisini alır ve tipte tanımlı tüm üye yapısını önceden bilir. Bu, nesne-yönelimli kalıtımın adres uzayı karşılığıdır ve companion specification'ların temelidir: bir robot, OPC 40010'daki standart tipe `HasTypeDefinition` ile bağlandığında, o spec'i bilen her istemci robotu otomatik anlar.

**Modelling rules: tip neden instance'ı tam belirlemez?** ObjectType üyeleri `Mandatory` veya `Optional` modelling rule taşır. Bu yüzden tipte görünen bir üye, belirli bir instance'da olmayabilir. Tip-tabanlı kod yazmanın tuzağı budur: kod tipe göre yazılır ama gerçekte instance browse edilmeli. Bu esneklik, aynı tipin farklı donanım varyantlarında (opsiyonel sensörlü/sensörsüz) kullanılabilmesini sağlar — alternatifi her varyant için ayrı tip tanımlamak olurdu.

## İlgili Konular

```
knowledge/protocols/opc-ua/
├── 01_architecture.md           → OPC UA genel mimari
├── 03_security.md               → Node erişim hakları ve güvenlik
├── 04_subscriptions.md          → Variable subscription
├── 05_codesys_server_config.md  → CODESYS'te adres uzayı yapılandırma
└── 06_client_implementations.md → Browse ve read örnekleri

Araçlar:
  UaExpert     → Adres uzayı görsel gezgini
  UA Modeler   → Grafik bilgi modeli tasarım aracı
  OPC UA Nodeset Viewer → nodeset XML dosyasını görüntüle
```
