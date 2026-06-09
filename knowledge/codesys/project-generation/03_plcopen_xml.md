---
KONU        : PLCopen XML (IEC 61131-10) Formatı
KATEGORİ    : codesys
ALT_KATEGORI: project-generation
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://www.plcopen.org/standards/logic/iec-61131-10/"
    başlık: "PLCopen — IEC 61131-10: PLC open XML Exchange Format"
    güvenilirlik: resmi
  - url: "https://standards.globalspec.com/std/13291341/61131-10"
    başlık: "GlobalSpec — IEC 61131-10 Standard Overview"
    güvenilirlik: resmi
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/codesys-pou-importexport-between-abb-and-schneider-brands"
    başlık: "Industrial Monitor Direct — PLCopen XML Cross-Brand Transfer"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Engineering/thread/fb39a2222a/"
    başlık: "CODESYS Forge — GVL'den PLCopen XML Parse Etme"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_project_file_structure.md"
    ilişki: tamamlar
  - konu: "02_script_engine.md"
    ilişki: kullanır
  - konu: "04_generation_templates.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "CODESYS proje yapısı (fundamentals/02_project_structure.md)"
  - "XML temel kavramları"
  - "IEC 61131-3 POU tipleri (programming/01_pou_types.md)"
ÇELİŞKİLER :
  - kaynak: "PLCopen XML v2.01 vs CODESYS native XML"
    konu: "PLCopen XML tüm CODESYS-özgü bilgileri taşımaz"
    çözüm: >
      PLCopen XML standart IEC 61131-3 içeriğini taşır: POU, DUT, GVL, Task, Config.
      Ancak CODESYS'e özgü bilgiler (device tree, EtherCAT slave konfigürasyonu,
      I/O mapping detayları, OPC UA sunucu ayarları) <addData> altında vendor-specific
      alanda saklanır. Import sırasında hedef platform bu kısımları görmezden gelebilir.
      Çapraz platform transferde hardware konfigürasyonu her zaman yeniden yapılmalıdır.
  - kaynak: "Farklı CODESYS versiyonları PLCopen export"
    konu: "V3.5 SP10 ile V3.5 SP21'in export ettiği PLCopen XML farklı olabilir"
    çözüm: >
      PLCopen XML şeması versiyonlanmıştır (v2.01 yaygın). CODESYS, CODESYS-özgü
      uzantılar için <addData> kullanır ve bu kısımlar versiyonlar arası uyumluluğu
      karmaşıklaştırır. Import öncesi hedef CODESYS versiyonu ile test et.
---

## Özün Ne

PLCopen XML, IEC 61131-3 proje içeriklerini farklı PLC programlama ortamları arasında taşınabilir kılan XML tabanlı standart bir formattır. IEC 61131-10 olarak standardize edilmiştir. CODESYS bu formatı hem dışa aktarım (export) hem içe aktarım (import) için destekler. Proje üretimi açısından PLCopen XML'in iki kritik kullanımı vardır: (1) harici araçlardan üretilen POU, DUT ve GVL kodunu CODESYS'e toplu import etmek; (2) mevcut projelerden kod parçalarını çıkarıp başka projelere veya platformlara aktarmak. Script Engine'e alternatif değil, tamamlayıcıdır: Script Engine proje nesne modelini yönetirken, PLCopen XML içeriği toplu taşır.

## Nasıl Çalışır

### PLCopen XML Şeması — Üst Düzey Yapı

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0201">

    <fileHeader companyName="Acme Automation"
                productName="CODESYS"
                productVersion="3.5.21.0"
                creationDateTime="2026-06-01T10:00:00"/>

    <contentHeader name="MyProject"
                   modificationDateTime="2026-06-01T10:00:00">
        <coordinateInfo>
            <fbd><scaling x="1" y="1"/></fbd>
            <ld><scaling x="1" y="1"/></ld>
            <sfc><scaling x="1" y="1"/></sfc>
        </coordinateInfo>
    </contentHeader>

    <types>
        <!-- DUT tanımları: STRUCT, ENUM, ALIAS -->
        <dataTypes>
            <dataType name="E_MotorState">...</dataType>
            <dataType name="ST_MotorDiag">...</dataType>
        </dataTypes>
    </types>

    <instances>
        <!-- Konfigürasyon: Resource ve Task tanımları -->
        <configurations>
            <configuration name="Application">
                <resource name="Resource">
                    <task name="MainTask" interval="T#10ms" priority="1">
                        <pouInstance typeName="PLC_PRG" name="PLC_PRG"/>
                    </task>
                    <!-- GVL'ler burada: globalVars -->
                    <globalVars name="GVL_IO">
                        <variable name="xMotorRun">
                            <type><BOOL/></type>
                        </variable>
                    </globalVars>
                </resource>
            </configuration>
        </configurations>
    </instances>

    <pous>
        <!-- POU'lar: Program, FB, Function -->
        <pou name="PLC_PRG" pouType="program">
            <interface>...</interface>
            <body><ST><![CDATA[ ...kod... ]]></ST></body>
        </pou>
        <pou name="FB_Motor" pouType="functionBlock">
            ...
        </pou>
    </pous>

    <addData>
        <!-- CODESYS'e özgü ek veri (vendor extension) -->
        <!-- Device tree, OPC UA, EtherCAT vb. -->
    </addData>

</project>
```

### POU XML Yapısı — Detay

```xml
<pou name="FB_Motor" pouType="functionBlock">
    <interface>
        <inputVars>
            <variable name="xStartCmd">
                <type><BOOL/></type>
                <documentation>
                    <xhtml xmlns="http://www.w3.org/1999/xhtml">
                        Çalıştırma komutu
                    </xhtml>
                </documentation>
            </variable>
            <variable name="tStartDelay">
                <type><TIME/></type>
                <initialValue>
                    <simpleValue value="T#3S"/>
                </initialValue>
            </variable>
        </inputVars>
        <outputVars>
            <variable name="xRunOutput">
                <type><BOOL/></type>
            </variable>
            <variable name="eState">
                <type><derived name="E_MotorState"/></type>
            </variable>
        </outputVars>
        <localVars>
            <variable name="tTimer">
                <type><derived name="TON"/></type>
            </variable>
        </localVars>
    </interface>
    <body>
        <!-- ST için: -->
        <ST><xhtml xmlns="http://www.w3.org/1999/xhtml">
<![CDATA[
CASE eState OF
    eIdle:
        xRunOutput := FALSE;
        IF xStartCmd THEN
            eState := eStarting;
        END_IF
    eRunning:
        xRunOutput := TRUE;
END_CASE
]]>
        </xhtml></ST>
    </body>
    <addData>
        <!-- CODESYS-özgü: Kod rengi, editör ayarları vb. -->
    </addData>
</pou>
```

### DUT XML Yapısı

```xml
<!-- ENUM -->
<dataType name="E_MotorState">
    <enumerated>
        <values>
            <value name="eIdle"><initialValue><simpleValue value="0"/></initialValue></value>
            <value name="eStarting"><initialValue><simpleValue value="1"/></initialValue></value>
            <value name="eRunning"><initialValue><simpleValue value="2"/></initialValue></value>
            <value name="eStopping"><initialValue><simpleValue value="3"/></initialValue></value>
            <value name="eFault"><initialValue><simpleValue value="4"/></initialValue></value>
        </values>
    </enumerated>
</dataType>

<!-- STRUCT -->
<dataType name="ST_MotorDiag">
    <structured>
        <variable name="tTotalRunTime"><type><TIME/></type></variable>
        <variable name="dwStartCount"><type><UDINT/></type></variable>
        <variable name="sFaultMsg"><type><string length="80"/></type></variable>
    </structured>
</dataType>
```

### Temel IEC Tipleri XML Gösterimi

```xml
<!-- Primitive tipler -->
<BOOL/>
<INT/>
<UINT/>
<DINT/>
<UDINT/>
<REAL/>
<LREAL/>
<TIME/>
<DATE/>
<STRING/>                          <!-- varsayılan uzunluk -->
<string length="80"/>              <!-- sabit uzunluk -->

<!-- Türetilmiş tipler -->
<derived name="TON"/>              <!-- Standart library tipi -->
<derived name="E_MotorState"/>     <!-- Kullanıcı tanımlı ENUM -->
<derived name="ST_MotorDiag"/>     <!-- Kullanıcı tanımlı STRUCT -->

<!-- Dizi -->
<array>
    <dimension lower="0" upper="9"/>
    <baseType><INT/></baseType>
</array>
```

### PLCopen XML Neyi Taşır, Neyi Taşımaz

```
TAŞINANLAR (platform bağımsız):
├── POU'lar — Program, Function Block, Function
│   ├── Değişken bildirimleri (VAR_INPUT, OUTPUT, LOCAL)
│   └── Uygulama kodu (ST, LD, FBD, SFC metinsel temsil)
├── DUT'lar — STRUCT, ENUM, ALIAS
├── GVL'ler — Global değişken listeleri
├── Task yapılandırması — İsim, interval, priority, POU çağrıları
└── Temel konfigürasyon bilgisi

TAŞINMAYANLAR (platform/vendor özgü):
├── Device tree (EtherCAT slave, Modbus konfigürasyonu)
├── I/O mapping (AT %I / %Q adresleri kaybolabilir)
├── Library Manager referansları (kütüphane bağımlılıkları)
├── OPC UA, MQTT, iletişim yapılandırmaları
├── Visualization (WebVisu, TargetVisu)
├── Symbol Configuration
└── CODESYS Runtime konfigürasyonu
```

## Pratikte Nasıl Kullanılır

### CODESYS'ten PLCopen XML Export

```
Yöntem 1 — IDE ile:
  Project → Export → PLCopen XML
    Seçenekler:
    [✓] Export POUs
    [✓] Export GVLs
    [✓] Export DUTs
    [✓] Export Task Configuration
    Dosya: MyProject_export.xml

Yöntem 2 — Script ile:
  proj = projects.primary
  proj.export_xml(r"C:\exports\MyProject_export.xml")
  
Yöntem 3 — Bireysel nesne export:
  found = proj.find("FB_Motor", recursive=True)
  fb = found[0]
  fb.export_xml(r"C:\exports\FB_Motor.xml")
```

### CODESYS'e PLCopen XML Import

```
Yöntem 1 — IDE ile:
  File → Import → PLCopen XML
    Dosyayı seç: MyExport.xml
    Import target: Application (altına eklenecek)
    
Yöntem 2 — Script ile:
  app = proj.find("Application", recursive=True)[0]
  app.import_xml(r"C:\exports\FB_Motor.xml")
  
Yöntem 3 — Proje import:
  projects.import_xml(r"C:\exports\WholeProject.xml")
```

### Python ile PLCopen XML Üretimi (Harici Araç)

```python
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def generate_plcopen_xml(pou_list, output_path):
    """
    Verilen POU listesinden PLCopen XML üretir.
    CODESYS Script Engine gerektirmez.
    """
    # Kök element
    root = Element('project')
    root.set('xmlns', 'http://www.plcopen.org/xml/tc6_0201')
    
    # File header
    fh = SubElement(root, 'fileHeader')
    fh.set('companyName', 'AutoGen')
    fh.set('productName', 'ProjectGenerator')
    fh.set('productVersion', '1.0.0')
    fh.set('creationDateTime', '2026-06-01T00:00:00')
    
    # Content header
    ch = SubElement(root, 'contentHeader')
    ch.set('name', 'GeneratedProject')
    
    # Types bölümü
    types_el = SubElement(root, 'types')
    dt_el = SubElement(types_el, 'dataTypes')
    
    # POUs bölümü
    pous_el = SubElement(root, 'pous')
    
    for pou_def in pou_list:
        pou_el = SubElement(pous_el, 'pou')
        pou_el.set('name', pou_def['name'])
        pou_el.set('pouType', pou_def.get('type', 'functionBlock'))
        
        # Interface
        interface_el = SubElement(pou_el, 'interface')
        
        if pou_def.get('inputs'):
            input_vars = SubElement(interface_el, 'inputVars')
            for var in pou_def['inputs']:
                var_el = SubElement(input_vars, 'variable')
                var_el.set('name', var['name'])
                type_el = SubElement(var_el, 'type')
                SubElement(type_el, var['type'])
        
        if pou_def.get('outputs'):
            output_vars = SubElement(interface_el, 'outputVars')
            for var in pou_def['outputs']:
                var_el = SubElement(output_vars, 'variable')
                var_el.set('name', var['name'])
                type_el = SubElement(var_el, 'type')
                SubElement(type_el, var['type'])
        
        # Body — ST kodu
        if pou_def.get('body_st'):
            body_el = SubElement(pou_el, 'body')
            st_el = SubElement(body_el, 'ST')
            xhtml_el = SubElement(st_el, 'xhtml')
            xhtml_el.set('xmlns', 'http://www.w3.org/1999/xhtml')
            xhtml_el.text = pou_def['body_st']
    
    # Güzel formatlı XML yaz
    xml_str = minidom.parseString(tostring(root)).toprettyxml(indent='  ')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print("PLCopen XML generated: {}".format(output_path))

# Kullanım
pou_definitions = [
    {
        'name': 'FB_SimpleMotor',
        'type': 'functionBlock',
        'inputs': [
            {'name': 'xStartCmd', 'type': 'BOOL'},
            {'name': 'xStopCmd', 'type': 'BOOL'}
        ],
        'outputs': [
            {'name': 'xRunOutput', 'type': 'BOOL'}
        ],
        'body_st': """IF xStartCmd AND NOT xStopCmd THEN
    xRunOutput := TRUE;
ELSE
    xRunOutput := FALSE;
END_IF"""
    }
]

generate_plcopen_xml(pou_definitions, 'generated_pous.xml')
```

### Çapraz Platform Transfer (ABB → CODESYS Örneği)

```
ABB Automation Builder → PLCopen XML export
        │
        │ FB_Motor.xml (PLCopen v2.01)
        ▼
CODESYS IDE → File → Import → FB_Motor.xml
        │
        │ Import sonrası kontrol listesi:
        ├── [✓] POU adı ve tipi korundu mu?
        ├── [✓] Değişken isimleri ve tipleri doğru?
        ├── [✓] ST kodu hatasız derleniyor mu?
        ├── [⚠] AT %I/%Q adresleri kayboldu → Yeniden eşle
        ├── [⚠] Kütüphane bağımlılıkları → Manuel ekle
        └── [✗] Device tree → Yeniden yapılandır
```

## Örnekler

### Örnek 1: Script ile Batch Export

```python
# CODESYS Script Engine içinde — tüm FB'leri ayrı dosyalara export et
import os

proj = projects.primary
app = proj.find("Application", recursive=True)[0]
export_dir = r"C:\exports\FBs"

if not os.path.exists(export_dir):
    os.makedirs(export_dir)

# Tüm Function Block'ları bul ve export et
pous = app.find("", recursive=True)  # Tüm nesneler
for pou in pous:
    if hasattr(pou, 'pou_type') and pou.pou_type == PouType.FunctionBlock:
        export_path = os.path.join(export_dir, "{}.xml".format(pou.name))
        pou.export_xml(export_path)
        print("Exported: {}".format(pou.name))

print("Export complete. {} FBs exported.".format(len([p for p in pous if hasattr(p, 'pou_type')])))
```

### Örnek 2: PLCopen XML'de GVL Üretimi

```python
def gvl_to_plcopen_xml(gvl_name, variables, output_path):
    """
    GVL tanımından PLCopen XML üretir.
    variables: [{'name': 'xMotorRun', 'type': 'BOOL', 'at': '%Q0.0'}, ...]
    """
    root = ET.Element('project')
    root.set('xmlns', 'http://www.plcopen.org/xml/tc6_0201')
    
    instances = ET.SubElement(root, 'instances')
    configs = ET.SubElement(instances, 'configurations')
    config = ET.SubElement(configs, 'configuration')
    config.set('name', 'DefaultConfig')
    resource = ET.SubElement(config, 'resource')
    resource.set('name', 'DefaultResource')
    
    global_vars = ET.SubElement(resource, 'globalVars')
    global_vars.set('name', gvl_name)
    
    for var in variables:
        var_el = ET.SubElement(global_vars, 'variable')
        var_el.set('name', var['name'])
        
        if var.get('at'):
            var_el.set('address', var['at'])  # AT adresi
        
        type_el = ET.SubElement(var_el, 'type')
        type_name = var['type']
        if type_name in ('BOOL', 'INT', 'UINT', 'REAL', 'TIME', 'DWORD'):
            ET.SubElement(type_el, type_name)
        else:
            derived = ET.SubElement(type_el, 'derived')
            derived.set('name', type_name)
    
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

# Kullanım
gvl_to_plcopen_xml(
    gvl_name="GVL_IO",
    variables=[
        {'name': 'xMotorRun', 'type': 'BOOL', 'at': '%Q0.0'},
        {'name': 'xMotorFB', 'type': 'BOOL', 'at': '%I0.0'},
        {'name': 'rTemperature', 'type': 'REAL', 'at': ''}
    ],
    output_path='GVL_IO.xml'
)
```

## Sık Yapılan Hatalar

### Hata 1: AT Adreslerinin Import Sonrası Kaybolması

```
Senaryo: PLCopen XML'de "xMotorRun AT %Q0.0 : BOOL" tanımlı.
         CODESYS import edince AT adresi düşüyor.
         
Neden  : AT adresleme, I/O Mapping'e bağlıdır ve Device tree olmadan anlamsızdır.
         PLCopen XML'de adres <variable address="%Q0.0"> ile geçirilir ama
         hedef platformda I/O mapping yeniden yapılmalıdır.

Çözüm  : Import sonrası I/O Mapping'i manuel olarak bağla.
          Veya Script Engine'den sonra programatik olarak eşle.
```

### Hata 2: BOM Karakteri ile XML Parse Hatası

```python
# PLCopen XML CODESYS tarafından BOM ile yazılır
# Python'da okurken:

# ❌ Yanlış
import xml.etree.ElementTree as ET
tree = ET.parse('export.xml')  # BOM → ParseError

# ✅ Doğru
import io
with io.open('export.xml', 'r') as f:
    f.seek(3)  # BOM'u atla
    tree = ET.parse(f)

# Veya daha güvenli:
with open('export.xml', 'r', encoding='utf-8-sig') as f:
    content = f.read()
root = ET.fromstring(content)
```

### Hata 3: Kütüphane Bağımlılıklarının Kaybolması

```
Senaryo: FB_Motor TON ve R_TRIG kullanıyor (Standard.library).
         PLCopen XML export edildiğinde Library Manager bilgisi dahil değil.
         Import sonrası Standard.library otomatik ekleniyor ama
         Util.library, CAA_File gibi ek kütüphaneler kaybolabiliyor.

Çözüm  : Import sonrası Library Manager kontrol edilmeli.
          Eksik kütüphaneler Manuel olarak eklenmeli.
          Veya Script Engine ile import + library ekleme birlikte yapılmalı.
```

### Hata 4: LD/FBD/SFC İçeriğinin Eksik Transfer Edilmesi

```
LD (Ladder Diagram) ve FBD (Function Block Diagram):
  PLCopen XML grafik temsili destekler ama koordinatlar kaybolabilir.
  Import edilen LD bloğu düz, okunaksız olabilir.

SFC (Sequential Function Chart):
  Adım ve geçiş yapısı transfer edilir.
  Ancak SFC aksiyon bloklarının kodu platforma göre yorumlanabilir.

ST (Structured Text):
  Kayıpsız transfer. Text-based format platform bağımsız.

Öneri: Taşınabilirlik kritikse tüm POU'ları ST'de yaz.
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**PLCopen XML Kullan:**
- CODESYS ile farklı PLC markası arasında POU transfer (ABB → CODESYS, Schneider → CODESYS)
- Script Engine olmadan harici araçta POU üretimi
- POU kütüphanesini düz metin/XML formatında saklamak
- CI/CD'de script değişikliklerini PLCopen XML olarak version control'de izlemek
- Müşteriye kaynak kodu vermek zorunda olduğunuzda (açık, standarttır)

**PLCopen XML Kullanma, Script Engine Tercih Et:**
- CODESYS'e özgü konfigürasyon (device tree, I/O mapping, OPC UA)
- Library Manager yönetimi
- Bütünsel proje oluşturma (sadece POU değil tüm yapı)
- CODESYS içinde kalacak iş akışları — Script daha hızlı ve daha güvenilir

**Script + PLCopen XML Birlikte Kullan:**
- Harici araç PLCopen XML üretir → CODESYS Script Engine import eder + konfigürasyon yapar
- Bu kombinasyon en güçlü ve en esnek yaklaşım

## Gerçek Proje Notları

**Not 1 — Siemens TIA → CODESYS Transfer**  
Eski bir Siemens S7 projesini CODESYS'e taşımak için PLCopen XML yolu denendi. TIA Portal, PLCopen export desteklemez. Alternatif: S7 STL kodunu manuel ST'ye dönüştürdük. PLCopen XML ile doğrudan transfer mümkün değildi; CODESYS Script Engine ile yeni proje oluşturulup ST kodu içe aktarıldı.

**Not 2 — Çapraz Marka Transfer Başarısı**  
ABB Automation Builder'da yazılmış `FB_Motor` bloğu PLCopen XML ile CODESYS'e başarıyla aktarıldı. ST kodu %95 çalıştı. Kayıplar: AT adresleri (yeniden eşlendi), kütüphane versiyonu (Standard eklendi). Toplam düzeltme süresi: 30 dakika. El ile yazılmış olsaydı 4 saat alırdı.

**Not 3 — Harici Araçtan Toplu POU Üretimi**  
Bir proje üretim aracı, veritabanından her ürün hattı için POU listesi üretip PLCopen XML olarak kaydediyordu. CODESYS Script Engine bu XML'i import edip task ve library yapılandırmasını tamamlıyordu. PLCopen XML + Script Engine kombinasyonu, tüm çözümün temeliydı.

**Not 4 — BOM Tuzağının Üretim Ortamında Keşfedilmesi**  
CI pipeline'ında PLCopen XML otomatik işleniyordu. Python XML parser sürekli hata veriyordu. Lokal testte çalışıyordu çünkü editör BOM'suz dosya kaydediyordu; CODESYS'in export ettiği dosya BOM içeriyordu. `encoding='utf-8-sig'` ile düzeltildi.

**Not 5 — CDATA İçindeki ST Kodunda `<` `>` `&` Kaçışı**  
Üretilen bir FB'de `IF a < b AND c > d THEN` koşulu vardı; XML üretici bunu CDATA'ya sarmadan element text'i olarak yazınca `<` ve `>` XML tag başlangıcı sanıldı, dosya bozuldu. PLCopen XML, ST gövdesini CDATA bloğu (`<![CDATA[...]]>`) içinde taşır — tam da bu yüzden: ST kodu `<`, `>`, `&` içerebilir ve bunlar XML'de özel karakterlerdir. Ders: ST gövdesini daima CDATA'ya sar veya XML lib'in otomatik kaçışına güven; string concat ile XML kurma (01 ile aynı uyarı). CDATA içinde de `]]>` dizisi kaçırılmalı (nadir ama gerçek).

**Not 6 — addData Kaybı: "Export-Import Round-Trip" Yanılgısı**  
Bir ekip "PLCopen XML export edip import edersem proje aynı kalır" varsaydı; export-import sonrası I/O mapping, OPC UA ayarları ve EtherCAT konfigürasyonu kayboldu. Bu bilgiler `<addData>` (vendor-specific) altında ya hiç export edilmez ya da hedef tarafından yok sayılır. PLCopen XML **lossy**'dir — IEC içeriğini taşır, CODESYS-özgü her şeyi değil (03 "taşınmayanlar"). Ders: PLCopen XML'i "tam proje yedeği" sanma; POU/DUT/GVL taşıma aracıdır. Tam yedek için `.projectarchive`.

**Not 7 — Şema Sürümü Uyumsuzluğu (tc6_0201 vs daha yeni)**  
Bir araç PLCopen XML'i eski şema (`tc6_0200`) ile üretti; yeni CODESYS sürümü import'ta uyarı verip bazı alanları atladı. PLCopen XML şeması versiyonludur (v2.01 = `tc6_0201` yaygın); CODESYS sürümleri arası export farklılaşabilir, `<addData>` uzantıları uyumu karmaşıklaştırır. Ders: üretici ve hedef CODESYS arasında şema sürümünü hizala; import öncesi `xmllint --schema tc6.xsd` ile doğrula; hedef sürümle test et.

## Edge Case'ler ve Format Sınırları

### Taşıma Kayıpları (Lossy Transfer)

```
İçerik                          PLCopen XML'de        Sonuç
─────────────────────────────────────────────────────────────────
ST kodu                         tam (CDATA)           kayıpsız ✓
Değişken bildirimi + init       tam                   kayıpsız ✓
DUT (STRUCT/ENUM)               tam                   kayıpsız ✓
LD/FBD grafik                   temsil var, koordinat kayabilir  düz/okunaksız olabilir
SFC                             adım/geçiş var         aksiyon kodu yoruma açık
AT %I/%Q adresi                 address attr ile geçer  hedefte I/O mapping yeniden
Library referansı               YOK                   manuel ekle
Device tree / EtherCAT          <addData> veya YOK     kaybolur, yeniden yapılandır
OPC UA / Symbol Config          YOK                   kaybolur
```

### XML Karakter ve Encoding Edge Case'leri

```
ST'de < > &        → CDATA içinde taşınmalı (Not 5)
CDATA'da ]]>       → bölünüp kaçırılmalı (]]]]><![CDATA[>)
BOM (UTF-8-BOM)    → encoding='utf-8-sig' (Not 4)
Türkçe/unicode     → UTF-8 tutarlı; CODESYS unicode destekler ama tool zinciri test et
Şema sürümü        → tc6_0201 (v2.01) yaygın; uyumsuzluk sessiz alan atlar (Not 7)
```

### Grafik Diller ve Taşınabilirlik

ST kayıpsız taşınır (metinsel); LD/FBD koordinat kaybeder (düz görünür); SFC adım yapısı taşınır ama aksiyon kodu platforma göre yorumlanır. **Taşınabilirlik kritikse tüm POU'ları ST'de yaz** (fundamentals/03 ST tekel konumuyla aynı sonuç) — üretim açısından da ST en güvenli format.

## Optimizasyon

### Üretimde XML Lib Kullan, String Concat Değil

```
- ET.SubElement ile yapı kur → otomatik kaçış, geçerli XML garantisi
- ST gövdesi → CDATA (manuel <,>,& kaçışıyla uğraşma)
- minidom.toprettyxml veya lxml ile okunabilir çıktı (debug/diff için)
- yazarken xml_declaration=True + encoding='utf-8'
```

String concat ile XML kurmak (Not 5, 01 Not 2) en yaygın bozulma kaynağıdır; her zaman XML kütüphanesi.

### Batch Export ve Git-Dostu Saklama

```
- Her POU'yu ayrı PLCopen XML'e export → Git'te anlamlı diff (klasik .project'in yapamadığı)
- Üretim girdilerini (FB şablonları) PLCopen XML olarak version control'de tut
- Release'lerde tam proje yerine POU-bazlı XML diff → ne değişti net görülür
```

### Import + Script Engine Kombinasyonu

```
PLCopen XML (içerik) → app.import_xml() → Script Engine (library+config tamamla)
→ en hızlı ve en güvenilir üretim: içerik dışarıda üretilir, bağlam içeride kurulur
```

## Derin Teknik Detay

### Neden Lossy? — Standart İçerik vs Vendor Uzantı Ayrımı

PLCopen XML (IEC 61131-10) bir **değişim (exchange) standardıdır**; amacı farklı üreticilerin ortak IEC 61131-3 içeriğini paylaşmasıdır. Standart yalnızca IEC'nin tanımladığını taşıyabilir: POU, DUT, GVL, Task. Device tree, I/O mapping, OPC UA — bunlar IEC standardının dışında, **üreticiye özgü**dür ve `<addData>` (vendor extension) alanına düşer. Bir hedef platform diğerinin `<addData>`'sını anlamak zorunda değildir → yok sayar (Not 6). Bu lossy'lik bir kusur değil, tasarım: standart "ortak payda"yı taşır, "üretici-özel"i taşımaz. Bu yüzden PLCopen XML çapraz-marka POU transferinde (ABB→CODESYS) güçlü, tam-proje-yedeğinde zayıftır — `.projectarchive` (native, tam) onun tersidir.

### CDATA: ST'nin XML'e Gömülmesi

ST kodu `<`, `>`, `&`, `:=` gibi XML'de özel/sorunlu karakterler içerir. İki çözüm vardır: entity kaçışı (`&lt;`) veya CDATA bloğu. PLCopen XML CDATA'yı tercih eder çünkü ST gövdesi büyük ve kaçış-yoğundur; her `<`'i `&lt;` yapmak okunaksız ve hataya açıktır. CDATA "buradaki her şey ham metin, parse etme" der — ST kodu olduğu gibi gömülür. Tek istisna `]]>` dizisidir (CDATA sonlandırıcı); ST'de nadirdir ama üretici bunu bölmelidir. Bu, fundamentals/03'teki "ST text-tabanlı" özelliğinin XML serileştirmesindeki yansımasıdır: metinsel dil, CDATA ile temiz gömülür; grafik diller (koordinat, bağlantı) yapısal XML gerektirir ve taşıması zordur.

### Üç Format Üçgeni: Native / PLCopen / Script Engine

```
Native .project (01)  → IDE tam durum, GUID grafiği, taşınamaz, elle yazılamaz
PLCopen XML (03)      → taşınabilir IEC içeriği, lossy, dışarıda üretilebilir
Script Engine (02)    → native'i obje-API ile yazan, IDE-tutarlı köprü
```

Üretim akışı üçünü birleştirir: PLCopen ile içeriği **taşınabilir** üret (Script Engine'siz, çapraz-platform), Script Engine ile native projeye **tutarlı** yerleştir (import_xml + config). Bu üçgen, project-generation klasörünün özüdür: her format bir amaca hizmet eder, hibrit kullanım (04) en güçlüsüdür.

### import_xml: Birleştirme (Merge) Semantiği

`app.import_xml()` bir PLCopen XML'i mevcut projeye **birleştirir** — yeni objeler ekler, çakışan isimlerde davranış (üzerine yaz / atla / yeniden adlandır) CODESYS sürümüne ve ayara bağlıdır. Bu, üretimde idempotency için kritiktir (02 Not 6): aynı XML iki kez import edilirse çakışma olabilir. Ayrıca import edilen POU'nun bağımlılıkları (kullandığı DUT/library) hedefte yoksa, import başarılı görünür ama compile başarısız olur (DUT→FB sırası, 04 "40 hata"). Bu yüzden import sırası (DUT önce) ve sonrasında compile doğrulaması, PLCopen-tabanlı üretimin vazgeçilmez disiplinidir.

## İlgili Konular

```
knowledge/codesys/project-generation/
├── 01_project_file_structure.md → CODESYS native XML vs PLCopen XML
├── 02_script_engine.md          → import_xml() API kullanımı
└── 04_generation_templates.md   → Şablondan PLCopen XML üretimi

knowledge/codesys/fundamentals/
└── 03_iec61131_languages.md     → PLCopen XML'de taşınan dil içerikleri

Araçlar:
  PLCopen XML schema          → https://www.plcopen.org/pages/tc6_xml/
  xmllint --schema tc6.xsd    → PLCopen XML doğrulama
  Python xml.etree.ElementTree → PLCopen XML üretme/ayrıştırma
```
