---
KONU        : CODESYS Proje Dosyası İç Yapısı
KATEGORİ    : codesys
ALT_KATEGORI: project-generation
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_struct_project_creation.html"
    başlık: "CODESYS Online Help — Creating and Configuring a Project"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_device_tree_device_editor.html"
    başlık: "CODESYS Online Help — Device Tree and Device Editor"
    güvenilirlik: resmi
  - url: "https://store.codesys.com/media/n98_media_assets/files/w/h/whitepaper-codesys-file-based_storage-0900.pdf"
    başlık: "CODESYS Whitepaper — File-Based Storage 0.9.0.0"
    güvenilirlik: resmi
  - url: "https://github.com/tkucic/codesys_workflow_automation"
    başlık: "GitHub — CODESYS Workflow Automation (Scripting ile proje manipülasyonu)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "02_script_engine.md"
    ilişki: gerektirir
  - konu: "03_plcopen_xml.md"
    ilişki: tamamlar
  - konu: "04_generation_templates.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/fundamentals/02_project_structure.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "CODESYS proje yapısı (fundamentals/02_project_structure.md)"
  - "XML temel kavramları (element, attribute, namespace)"
  - "Proje üretimi neden gerekli — bağlam anlayışı"
ÇELİŞKİLER :
  - kaynak: "CODESYS File-Based Storage (Yeni Format, 0.9+)"
    konu: ".project tek XML vs file-based (klasör + dosya) format ayrımı"
    çözüm: >
      Klasik .project: Tüm proje tek XML dosyasında. Git diff'leri anlamsız.
      File-Based Storage (yeni, beta): Her POU, GVL, DUT ayrı dosyada; Git dostu.
      Bu belge klasik .project formatını ele alır. File-based format henüz production
      kullanımı için önerilmiyor (2026 itibarıyla beta). Klasik format hâlâ standarttır.
---

## Özün Ne

CODESYS `.project` dosyası, dışarıdan bakıldığında opaque bir binary gibi görünse de aslında UTF-8 kodlu sıkıştırılmış XML tabanlı bir formattır. İçini anlayan biri için proje üretimi, template manipülasyonu ve otomatik kod üretimi mümkün hale gelir. Script Engine ya da PLCopen XML ile etkileşimde bulunmak için de bu yapıyı kavramak gerekir: Script Engine API'si, proje nesne modelini (IScriptProject, IScriptApplication, IScriptPou...) manipüle ederken, arka planda tam olarak bu XML yapısını yazıp okumaktadır.

## Nasıl Çalışır

### Dosya Formatı

`.project` dosyası, CODESYS'in kendi XML şemasını kullanan XML belgesidir. Doğrudan metin editörüyle açıldığında okunabilir haldedir (şifreli değil). Ancak büyük projeler için IDE dışında manuel düzenleme önerilmez; XML tutarlılığını bozmak projeyi açılamaz hale getirebilir.

```bash
# .project dosyasını incele (küçük projeler için)
cat MyProject.project | head -100

# Daha büyük dosyalar için
xmllint --format MyProject.project | less
```

### Kök Yapı

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.3s-software.com/schemas/Codesys-V3">
    <ProjectInfo>
        <!-- Proje meta verisi -->
    </ProjectInfo>
    <Interfaces>
        <!-- Proje geneli POU'lar (POUs view) -->
    </Interfaces>
    <Implementations>
        <!-- Gizli uygulama detayları -->
    </Implementations>
    <DeviceDesc>
        <!-- Device tree kökü -->
    </DeviceDesc>
    <Dependencies>
        <!-- Proje bağımlılıkları -->
    </Dependencies>
</project>
```

### Proje Hiyerarşisi — XML Nesnelere Eşleme

```
CODESYS IDE                          XML/Proje Modeli
──────────────────────────────────────────────────────────────
Project                       →  <project> kök elementi
├── POUs view                 →  <Interfaces> bölümü
│   ├── FB_SharedMotor        →  <pou name="FB_SharedMotor" ...>
│   └── Library Manager       →  <libraryManager> elementi
│
└── Devices view (Device Tree)→  <DeviceDesc> bölümü
    └── MyDevice (Root)       →  <device ...>
        ├── PLC Logic         →  <device type="...PLCLogic...">
        │   └── Application   →  <Device> (application type)
        │       ├── Library Manager → <libraryManager>
        │       ├── Task Config    → <Device type="...TaskConfig...">
        │       │   └── MainTask   →  <Task ...> elementi
        │       ├── PLC_PRG        →  <pou name="PLC_PRG" ...>
        │       ├── GVL_IO         →  <globalVarList name="GVL_IO">
        │       └── DUT_Motor      →  <dut name="DUT_Motor" ...>
        │
        └── EtherCAT_Master        →  <device type="EtherCAT...">
            └── Slave_1            →  <device type="EtherCATSlave...">
```

### POU XML Yapısı

```xml
<pou name="FB_Motor" pouType="functionBlock">
    <interface>
        <!-- Değişken bildirimleri -->
        <inputVars>
            <variable name="xStartCmd">
                <type><BOOL/></type>
            </variable>
            <variable name="tStartDelay">
                <type><TIME/></type>
                <initialValue><simpleValue value="T#3S"/></initialValue>
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
            <variable name="tStartTimer">
                <type><derived name="TON"/></type>
            </variable>
        </localVars>
    </interface>
    <body>
        <!-- Dil seçimine göre: ST için -->
        <ST>
            <xhtml xmlns="http://www.w3.org/1999/xhtml">
                CASE eState OF
                    eIdle:
                        (* ... kod ... *)
                END_CASE
            </xhtml>
        </ST>
        <!-- LD için: <LD> ... </LD> -->
        <!-- FBD için: <FBD> ... </FBD> -->
    </body>
</pou>
```

### GVL XML Yapısı

```xml
<globalVarList name="GVL_IO">
    <attributes>
        <!-- {attribute 'qualified_only'} gibi pragma'lar -->
        <attribute name="qualified_only"/>
    </attributes>
    <vars>
        <!-- VAR_GLOBAL bildirimi — tüm satırlar tek STRING olarak saklanır -->
        <!-- CODESYS kendi deklarasyon formatını korur -->
    </vars>
    <!-- Textual representation -->
    <textDecl>
        <xhtml xmlns="http://www.w3.org/1999/xhtml">
VAR_GLOBAL
    xMotorRun    AT %Q0.0 : BOOL;
    rTemperature AT %IW0  : REAL;
END_VAR
        </xhtml>
    </textDecl>
</globalVarList>
```

### Task Configuration XML Yapısı

```xml
<device name="Task Configuration" ...>
    <Task name="MainTask"
          interval="10000"
          priority="1"
          type="Cyclic"
          watchdogTime="50000"
          watchdogSensitivity="3">
        <!-- Task'a atanan programlar -->
        <POUcallList>
            <POUcall callType="Program">
                <calls>
                    <call typeGuid="..." typeName="PLC_PRG">
                        <inputAssignment>
                            <!-- Parametre atamaları -->
                        </inputAssignment>
                    </call>
                </calls>
            </POUcall>
        </POUcallList>
    </Task>
</device>
```

### Library Manager XML Yapısı

```xml
<libraryManager>
    <libraryReferences>
        <libraryReference
            defaultResolution="Standard, 3.5.17.0 (System)"
            namespace="*"
            version="3.5.17.0"
            company="System"
            title="Standard">
        </libraryReference>
        <libraryReference
            defaultResolution="Util, 3.5.17.0 (System)"
            namespace="Util"
            version="3.5.17.0"
            company="System"
            title="Util">
        </libraryReference>
    </libraryReferences>
</libraryManager>
```

### ProjectInfo XML

```xml
<ProjectInfo>
    <Title>MyMachineName</Title>
    <Version>1.2.0.0</Version>
    <Author>Engineer Name</Author>
    <Company>Acme Automation</Company>
    <Description>Paketleme Hattı PLC Projesi</Description>
    <Created>2026-01-15T10:30:00</Created>
    <LastModified>2026-06-01T14:22:00</LastModified>
    <CompilerVersion>3.5.21.0</CompilerVersion>
</ProjectInfo>
```

### Nesneler ve XML Etiket Eşleme Tablosu

| CODESYS Nesnesi | XML Etiket | Ana Attribute |
|---|---|---|
| PROGRAM | `<pou>` | `pouType="program"` |
| FUNCTION_BLOCK | `<pou>` | `pouType="functionBlock"` |
| FUNCTION | `<pou>` | `pouType="function"` |
| GVL | `<globalVarList>` | `name="GVL_IO"` |
| DUT (STRUCT) | `<dut>` | `type="Structure"` |
| DUT (ENUM) | `<dut>` | `type="Enum"` |
| Task | `<Task>` | `type="Cyclic"` |
| Device | `<device>` | `typeGuid="..."` |
| Library Manager | `<libraryManager>` | — |
| Application | özel `<device>` | application type |
| Folder | `<Folder>` | `name="MyFolder"` |

## Pratikte Nasıl Kullanılır

### .project Dosyasını İnceleme

```bash
# Tüm POU isimlerini listele
grep -o 'name="[^"]*" pouType' MyProject.project | sort

# Tüm GVL isimlerini bul
grep -o '<globalVarList name="[^"]*"' MyProject.project

# Task konfigürasyonunu bul
grep -A 10 '<Task name=' MyProject.project

# Library referanslarını listele
grep 'libraryReference' MyProject.project | grep 'title='

# Arama: Belirli bir değişken var mı?
grep 'xMotorRun' MyProject.project
```

### .project Dosyasını Python ile Ayrıştırma

```python
import xml.etree.ElementTree as ET

# BOM sorununu önlemek için
with open('MyProject.project', 'r', encoding='utf-8-sig') as f:
    content = f.read()

root = ET.fromstring(content)

# Namespace tanımı (CODESYS V3 şeması)
ns = {'codesys': 'http://www.3s-software.com/schemas/Codesys-V3'}

# Tüm POU'ları bul
pous = root.findall('.//pou', ns)
for pou in pous:
    name = pou.get('name')
    pou_type = pou.get('pouType')
    print(f"POU: {name} ({pou_type})")

# Tüm GVL'leri bul
gvls = root.findall('.//globalVarList', ns)
for gvl in gvls:
    print(f"GVL: {gvl.get('name')}")

# Library referanslarını bul
libs = root.findall('.//libraryReference', ns)
for lib in libs:
    title = lib.get('title')
    version = lib.get('version')
    print(f"Library: {title} v{version}")
```

### Programatik Proje Üretimi — Neden XML'e Dokunmak Gerekir?

Script Engine, proje manipülasyonunun birincil yoludur — doğrudan XML yazmak yerine API kullanılır. Ancak XML yapısını anlamak birkaç senaryoda kritiktir:

```
Senaryo 1: Script Engine erişimi olmayan ortam
  → .project dosyasını doğrudan oluştur veya manipüle et
  → Python xml.etree.ElementTree ile template'ten proje yaz

Senaryo 2: PLCopen XML oluşturma
  → PLCopen XML'in CODESYS proje XML'iyle örtüşen/ayrışan kısımları

Senaryo 3: Proje analizi
  → Projedeki tüm değişkenleri, POU'ları, bağımlılıkları raporla
  → Versiyon kontrolünde neyin değiştiğini anla

Senaryo 4: Şablon tabanlı proje üretimi
  → Template .project dosyası al, belirli bölümleri değiştir
  → Müşteriye özgü parametrelerle yeni proje üret
```

## Örnekler

### Örnek 1: Minimal Proje XML Şablonu

Sıfırdan bir .project dosyası oluşturmak için minimum gerekli yapı:

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.3s-software.com/schemas/Codesys-V3">
  <ProjectInfo>
    <Title>GeneratedProject</Title>
    <Author>AutoGen</Author>
    <Version>1.0.0.0</Version>
  </ProjectInfo>
  <Interfaces/>
  <DeviceDesc>
    <!-- Device tree burada başlar -->
    <!-- Device typeGuid, cihaz tanımına göre değişir -->
  </DeviceDesc>
</project>
```

Pratikte sıfırdan XML oluşturmak yerine template .project üzerinde Script Engine kullanmak çok daha güvenlidir.

### Örnek 2: Script ile Proje Yapısını Analiz Etme

```python
# CODESYS Script Engine içinde (Tools → Scripting → Run Script)
# Projedeki tüm POU'ları, GVL'leri ve task'ları listele

proj = projects.primary

def explore_object(obj, indent=0):
    prefix = "  " * indent
    obj_type = type(obj).__name__
    name = getattr(obj, 'name', '?')
    print(f"{prefix}[{obj_type}] {name}")
    try:
        for child in obj.get_children(recursive=False):
            explore_object(child, indent + 1)
    except:
        pass

explore_object(proj)
# Çıktı:
# [IScriptProject] MyProject
#   [IScriptDevice] MyDevice
#     [IScriptDevice] PLC Logic
#       [IScriptApplication] Application
#         [IScriptTaskConfiguration] Task Configuration
#         [IScriptPou] PLC_PRG
#         [IScriptGvl] GVL_IO
```

### Örnek 3: Değişken Adlarını XML'den Çıkarma (Proje Dışı Araç)

```python
import xml.etree.ElementTree as ET
import re

def extract_variables_from_project(project_path):
    """
    .project dosyasından tüm GVL değişkenlerini çıkarır.
    Script Engine olmadan çalışır.
    """
    with open(project_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    root = ET.fromstring(content)
    ns = {'cs': 'http://www.3s-software.com/schemas/Codesys-V3'}
    
    variables = []
    
    # GVL'lerdeki textDecl'den değişkenleri ayrıştır
    for gvl in root.findall('.//globalVarList', ns):
        gvl_name = gvl.get('name', 'Unknown')
        text_decl = gvl.find('.//textDecl/xhtml:body', {'xhtml': 'http://www.w3.org/1999/xhtml'})
        if text_decl is None:
            # Farklı namespace formatı
            text_decl = gvl.find('.//textDecl')
        
        if text_decl is not None:
            decl_text = ''.join(text_decl.itertext())
            # Değişken isimlerini regex ile yakala
            var_matches = re.findall(r'(\w+)\s*(?:AT\s+%\w+\.\d+)?\s*:\s*(\w+)', decl_text)
            for var_name, var_type in var_matches:
                if var_name not in ('VAR_GLOBAL', 'END_VAR', 'RETAIN', 'PERSISTENT'):
                    variables.append({
                        'gvl': gvl_name,
                        'name': var_name,
                        'type': var_type
                    })
    
    return variables

# Kullanım
vars = extract_variables_from_project('MyProject.project')
for v in vars:
    print(f"{v['gvl']}.{v['name']} : {v['type']}")
```

## Sık Yapılan Hatalar

### Hata 1: .project Dosyasını Doğrudan Düzenlemek

```
❌ Yanlış: .project XML'ini text editor ile açıp değiştirmek
  Küçük bir hata (kapanmamış tag, hatalı encoding) projeyi açamaz hale getirir.
  CODESYS XML format değişikliklerini kontrol eder — tutarsızlık = açılmama.

✅ Doğru: Script Engine API kullan → Format bütünlüğü garanti altında.
  Son çare: .project'i backup al, küçük değişiklik yap, CODESYS'te aç.
```

### Hata 2: BOM (Byte Order Mark) Sorununu Görmezden Gelmek

```python
# ❌ Yanlış — BOM sorununa yol açar
with open('project.project', 'r') as f:
    ET.parse(f)  # BOM karakteri XML parser'ı bozar

# ✅ Doğru
with open('project.project', 'r', encoding='utf-8-sig') as f:
    content = f.read()
root = ET.fromstring(content)
```

### Hata 3: typeGuid Olmadan Device Eklemek

Device ekleme, cihazın typeGuid'ini gerektirir. Bu GUID, cihaz description dosyasına göre değişir ve proje dışından bilinmesi güçtür. Bu nedenle proje üretiminde device ekleme Script Engine üzerinden yapılmalıdır.

```python
# ✅ Doğru — Script Engine ile device guid'ini dinamik bul
devices = system.get_all_devices()
win_device = [d for d in devices if 'Control Win' in d.name][0]
proj.add_device(win_device.guid)
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**XML yapısını doğrudan kullan:**
- Proje analizi ve raporlama araçları (CI/CD pipeline içinde)
- Script Engine erişimi olmayan harici araçlarda
- Değişken, POU, bağımlılık listesi çıkarma
- .project'i template olarak kopyalayıp belirli bölümleri değiştirme

**XML'e dokunma, Script Engine kullan:**
- POU oluşturma, silme, değiştirme
- GVL değişken ekleme
- Task yapılandırması
- Library ekleme
- Herhangi bir "yazma" operasyonu

## Gerçek Proje Notları

**Not 1 — Büyük Proje, Tek XML**  
500+ POU içeren büyük bir proje 25MB'ı aşan tek bir .project dosyasına dönüşüyordu. Git diff ile "ne değişti" sorusunun cevabını bulmak neredeyse imkansızdı. File-based storage geçişi tartışıldı ama henüz beta. Geçici çözüm: Her release'te PLCopen XML export alınıp diff yapıldı.

**Not 2 — XML Bozan Özel Karakter**  
Bir geliştirici, ST koduna yorum olarak `<` ve `>` karakterleri yazdı. CODESYS bunları `&lt;` ve `&gt;` olarak kaçırdı — doğru. Ancak başka bir araçla XML manipüle edildiğinde bu kaçış karakterleri bozuldu ve proje açılmaz hale geldi. Ders: XML'i her zaman proper XML kütüphanesiyle işle, string replace kullanma.

**Not 3 — typeGuid Sürpriz Değişiklikleri**  
Farklı CODESYS versiyonlarında aynı cihazın typeGuid'i değişebilir. Bir araç v3.5.17 ile üretilen GUID'i v3.5.21'de kullanamazdı. Çözüm: typeGuid'leri araçta hardcode etme; Script Engine'in device repository'sinden dinamik al.

**Not 4 — Object GUID Kopya-Yapıştır ile "Hayalet Referans"**  
Bir template projeden POU kopyalanıp yapıştırıldı; çalıştı ama Task'taki POU çağrısı ve bir visualization eski POU'ya bağlı kaldı. Neden: her CODESYS objesi bir **GUID** taşır (fundamentals/02); kopyala-yapıştır yeni GUID üretir ama eski GUID'e bağlı referanslar (task POUcall `typeGuid`, visualization) güncellenmez → "object not found" hayalet hataları. Ders: obje taşımak için kopyala-yapıştır yerine **export/import** (PLCopen XML) kullan; üretimde POU çağrılarını isimle değil, oluşturulan objenin referansıyla bağla.

**Not 5 — Git Merge'in `.project`'i Bozması**  
İki mühendis aynı `.project`'te paralel çalıştı, Git ile birleştirdi — dosya açılmadı. `.project` XML olsa da GUID'ler, sıralı ID'ler ve gömülü blob'lar içerir; satır-bazlı merge bunları bozar (fundamentals/02 Not 6). Ders: `.project`'i Git'te "yedek+geçmiş" için tut, gerçek işbirliği için PLCopen XML object-export veya CODESYS Git entegrasyonu kullan; üretim araçları `.project`'i tek-yazar olarak üretmeli, paralel düzenlememeli.

**Not 6 — File-Based Storage Geçişinin Erken Denenmesi**  
Git-dostu olsun diye bir ekip file-based storage formatına (beta) geçti; her POU ayrı dosya oldu, diff'ler okunabilirdi. Ama bazı kütüphaneler ve eski araçlar bu formatı tanımadı, CI pipeline'ı kırıldı. Ders: 2026 itibarıyla file-based storage hâlâ beta; production üretim araçları klasik tek-XML `.project`'i hedeflemeli. File-based'i yalnızca formatı tam destekleyen kontrollü ortamda dene.

## Edge Case'ler ve Format Sınırları

### XML Bütünlüğü Tuzakları

```
Tuzak                              Sonuç                     Koruma
─────────────────────────────────────────────────────────────────────
Kapanmamış tag / hatalı encoding   proje açılmaz             proper XML lib, string-replace yok
BOM (UTF-8-BOM)                    parser patlar             encoding='utf-8-sig'
ST içinde < > karakterleri         &lt; &gt; kaçış bozulması  XML lib kullan, manuel kaçış yok
GUID çakışması (iki obje aynı GUID) biri sessizce gölgelenir   export/import, kopya değil
typeGuid versiyon farkı            device tanınmaz            dinamik repository'den al
Sıralı ID tutarsızlığı             referans kopar            Script Engine ile yaz, elle değil
```

### Manuel XML Düzenlemenin Sınırı

`.project`'i elle düzenlemek neredeyse her zaman yanlıştır çünkü:
- Obje GUID'leri, task POUcall `typeGuid`'leri, sıralı ID'ler arası tutarlılık elle korunamaz.
- Compile cache ve checksum'lar XML içinde gömülüdür; tutarsızlık projeyi açılamaz yapar.
- **Tek güvenli "okuma" senaryosu:** analiz/raporlama (grep, Python ET ile parse). **Yazma:** daima Script Engine.

### File-Based vs Klasik Format Edge Case'leri

```
Klasik (.project):  tek XML · Git merge bozar · tüm araçlar destekler · standart
File-based (beta):  klasör+dosya · Git-dostu diff · bazı araç/lib desteklemez · 2026 beta
```

Üretim aracı hangi formatı hedefleyeceğini bilmeli; ikisinin XML şeması ve obje serileştirmesi farklıdır.

## Optimizasyon

### Analiz/Raporlama için XML Doğrudan Okuma

Yazma için Script Engine zorunlu olsa da, **okuma** (analiz, raporlama, CI doğrulama) için doğrudan XML parse hızlı ve Script Engine'siz çalışır:

```python
# CI'da Script Engine/lisans gerektirmeden proje analizi
with open('proj.project', encoding='utf-8-sig') as f:   # BOM güvenli
    root = ET.fromstring(f.read())
# POU sayısı, GVL listesi, library sürümleri, kullanılmayan değişken raporu
```

Bu, CODESYS lisansı tüketmeden (Not: headless Script Engine lisans ister, programming/02) hızlı statik analiz sağlar.

### Büyük Proje ve Format Seçimi

```
- 500+ POU → tek .project 25MB+ olur; diff anlamsız (Not 1)
- Geçici çözüm: her release'te PLCopen XML export + diff
- Compile cache şişer; "Clean" sonrası .project küçülür (gereksiz cache atılır)
- Üretimde: template'i minimal tut, içeriği script üretsin (bootapp/dosya küçük kalır)
```

### Referans Bütünlüğü için Export/Import

Kopya-yapıştır GUID hayalet referansları (Not 4) yaratır; **export/import** referans bütünlüğünü daha iyi korur. Üretim akışında objeleri PLCopen XML ile import etmek, kopyalamaktan daha güvenlidir.

## Derin Teknik Detay

### `.project` Neden Tek XML? — IDE'nin Obje Grafiği Serileştirmesi

`.project`, insan-diff'i için değil, **IDE'nin bellekteki obje grafiğini serileştirmek** için tasarlanmıştır (fundamentals/02 derin detay). Her obje (POU, GVL, DUT, Task) bir GUID ile düğüm, referanslar (task→POU, FB→DUT) ise GUID-bağlantılı kenarlardır. XML bu grafiği düzleştirir; satır sırası anlamlı değildir, GUID bağlantıları anlamlıdır. Bu yüzden:
- Git satır-merge'i grafiği bozar (kenarlar kopar) → açılmaz.
- Elle düzenleme GUID tutarlılığını bozar → açılmaz.
- Script Engine grafiği obje-seviyesinde manipüle eder (API), serileştirmeyi IDE'ye bırakır → güvenli.

Bu, "neden XML ama elle düzenlenemez" çelişkisinin çözümüdür: format XML'dir ama semantik bir obje grafiğidir, metin değil.

### Script Engine ile XML'in İlişkisi: API = Obje Grafiği, XML = Serileştirme

Script Engine'in `IScriptPou`, `IScriptGvl` gibi nesneleri, tam olarak `.project` XML'indeki `<pou>`, `<globalVarList>` düğümlerine karşılık gelir (belgedeki eşleme tablosu). `app.create_pou()` bir XML `<pou>` düğümü + GUID üretir; `textual_declaration.replace()` o düğümün `<interface>`/`<body>` içeriğini yazar. Yani Script Engine, XML'i doğrudan yazmak yerine obje grafiğini manipüle eder ve IDE serileştirmeyi tutarlı yapar. XML yapısını bilmek, Script Engine'in "ne yaptığını" anlamak için gereklidir — ama yazma her zaman API üzerinden olmalıdır (Not 2, Hata 1).

### typeGuid: Device Description'a Bağlı Kimlik

Bir `<device typeGuid="...">`'in GUID'i, kurulu device description'dan (`.devdesc`) gelir (fundamentals/02). Bu GUID device+sürüm kombinasyonuna özgüdür; CODESYS sürümü veya device paketi değişince değişebilir (Not 3). Bu yüzden üretim aracı typeGuid'i hardcode edemez — çalışma anında `system.get_all_devices()` ile repository'den çözmelidir. Bu, device tree'nin neden template'te elle hazırlanması gerektiğinin (04 hibrit yaklaşım) teknik kökü: device ekleme, kurulu repository'ye ve doğru GUID'e bağlıdır, sıfırdan XML ile güvenilir yapılamaz.

### PLCopen XML vs Native XML: İki Serileştirmenin Amacı

`.project` native XML CODESYS'in **tam** durumunu (GUID grafiği, device tree, cache) saklar — taşınabilir değil, IDE-özgü. PLCopen XML ise IEC 61131-3 içeriğinin **taşınabilir** alt kümesini saklar (POU/DUT/GVL, device tree değil — bkz. 03). Bu ikilik kasıtlıdır: native format IDE'nin iç çalışması için, PLCopen değişim (exchange) için. Üretim akışı ikisini birleştirir: içeriği PLCopen ile dışarıda üret (taşınabilir, Script Engine'siz), native projeye Script Engine ile yerleştir (IDE-tutarlı). "Hangi XML?" sorusunun cevabı her zaman "üretiyorsan PLCopen, yerleştiriyorsan native (Script Engine üzerinden)"dir.

## İlgili Konular

```
knowledge/codesys/project-generation/
├── 02_script_engine.md       → XML yapısını API üzerinden manipüle etmek
├── 03_plcopen_xml.md         → PLCopen XML: taşınabilir alternatif format
└── 04_generation_templates.md→ Şablon tabanlı proje üretimi

knowledge/codesys/fundamentals/
└── 02_project_structure.md   → IDE'deki görsel yapı — bu belgenin karşı tarafı

Araçlar:
  xmllint         → XML doğrulama ve formatlama
  xmlstarlet      → XML sorgu ve dönüşüm
  Python ET       → xml.etree.ElementTree — standart kütüphane
  lxml            → Daha hızlı XML parser, XPath desteği
```
