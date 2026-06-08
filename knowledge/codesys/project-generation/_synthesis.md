---
KONU        : CODESYS Otomatik Proje Üretimi — Sentez
KATEGORİ    : codesys
ALT_KATEGORI: project-generation
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "knowledge/codesys/project-generation/01_project_file_structure.md"
    başlık: "CODESYS Proje Dosyası İç Yapısı"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/project-generation/02_script_engine.md"
    başlık: "CODESYS Script Engine"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/project-generation/03_plcopen_xml.md"
    başlık: "PLCopen XML (IEC 61131-10) Formatı"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/project-generation/04_generation_templates.md"
    başlık: "CODESYS Otomatik Proje Üretimi — Şablon Sistemi"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_project_file_structure.md"
    ilişki: detaylandırır
  - konu: "02_script_engine.md"
    ilişki: detaylandırır
  - konu: "03_plcopen_xml.md"
    ilişki: detaylandırır
  - konu: "04_generation_templates.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "CODESYS proje yapısı (fundamentals/02_project_structure.md)"
  - "IEC 61131-3 dilleri (fundamentals/03_iec61131_languages.md)"
  - "Python temel bilgisi (IronPython 2.7 ve CPython 3.x farkı dahil)"
  - "XML temel kavramları (element, attribute, namespace)"
ÇELİŞKİLER :
  - kaynak: "04_generation_templates.md — Hibrit yaklaşım"
    konu: "Tam otomatik üretim mi, hibrit şablon yaklaşımı mı?"
    çözüm: >
      Sıfırdan tam otomatik üretim (device tree dahil) kırılgandır.
      En sağlam yaklaşım: Elle hazırlanmış template .project (device tree, library,
      task iskeleti) + otomatik GVL, POU ve implementasyon üretimi kombinasyonu.
      Bu sentez bu hibrit yaklaşımı temel alır.
  - kaynak: "01_project_file_structure.md — File-Based Storage"
    konu: "Klasik .project tek XML mı, yeni file-based format mı?"
    çözüm: >
      File-based storage (2026 itibarıyla beta) her POU'yu ayrı dosyaya yazar; Git dostu.
      Klasik .project tek XML'dir ve hâlâ standarttır. Bu sentez klasik formatı temel alır.
---

## Özün Ne

Bu sentez, dört belgenin birlikte verdiği tek soruya yanıt verir: **Bir AI agent, bir JSON spesifikasyonundan nasıl geçerli, derlenebilir bir CODESYS projesi üretir?**

Her belge bu zincirin farklı bir halkasını tanımlar: `01_project_file_structure.md`, CODESYS `.project` dosyasının XML anatomisini açar. `02_script_engine.md`, bu anatomiye IronPython 2.7 ile dokunmanın resmi yolunu verir. `03_plcopen_xml.md`, kod içeriklerini CODESYS dışında üretip Script Engine'e teslim etmenin standart formatını tanımlar. `04_generation_templates.md`, bu üç aracı somut bir üretim akışına bağlar ve agent'ın izleyeceği karar ağacını çizer. Dört belge birlikte anlaşıldığında CODESYS, insan müdahalesi gerektirmeyen programatik bir çıktı haline gelir.

Bu klasör, agent'ın CODESYS projesi üretmesi için kritiktir: Buradaki bilgiyi özümsemeyen bir agent, "bir motor fb'si oluştur" komutunu karşılayacak araçlara sahip değildir.

## Nasıl Çalışır

### Dört Belgenin Bütünsel Bağlantısı

```
┌──────────────────────────────────────────────────────────────────────────┐
│            CODESYS OTOMATİK PROJE ÜRETİMİ — ZİHİN HARİTASI             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  01_project_file_structure.md                                             │
│  ┌────────────────────────────────────────────────────────┐              │
│  │              .project DOSYASI (XML)                    │              │
│  │                                                        │              │
│  │  <project>                                             │              │
│  │    <ProjectInfo>  → Başlık, versiyon, yazar           │              │
│  │    <DeviceDesc>   → Device tree kökü                  │              │
│  │      <device>     → PLC Logic → Application          │              │
│  │        <pou>      → FB / PROGRAM / FUNCTION           │              │
│  │        <globalVarList> → GVL                          │              │
│  │        <dut>      → STRUCT / ENUM                     │              │
│  │        <Task>     → Cyclic, interval, priority        │              │
│  │        <libraryManager> → Kütüphane referansları      │              │
│  └────────────────────────────┬───────────────────────────┘              │
│                               │ Script Engine bu XML'i API üzerinden     │
│                               │ okur ve yazar                            │
│                               ▼                                           │
│  02_script_engine.md                                                      │
│  ┌────────────────────────────────────────────────────────┐              │
│  │          SCRIPT ENGINE (IronPython 2.7)                │              │
│  │                                                        │              │
│  │  projects.open()   → Projeyi aç                       │              │
│  │  app.create_pou()  → POU oluştur                      │              │
│  │  app.create_gvl()  → GVL oluştur                      │              │
│  │  app.create_dut()  → DUT oluştur                      │              │
│  │  fb.textual_declaration.replace() → Kod içeriği yaz   │              │
│  │  app.import_xml()  → PLCopen XML'i içe aktar          │              │
│  │  proj.compile()    → Derle                            │              │
│  │  projects.save()   → Kaydet                           │              │
│  │                                                        │              │
│  │  Çalıştırma modları:                                   │              │
│  │    IDE: Tools → Scripting → Run Script                │              │
│  │    Headless: CODESYS.exe --noUI --runscript=...       │              │
│  └────────────────────────────┬───────────────────────────┘              │
│                               │ Script Engine PLCopen XML'i import eder  │
│                               ▼                                           │
│  03_plcopen_xml.md                                                        │
│  ┌────────────────────────────────────────────────────────┐              │
│  │          PLCopen XML (IEC 61131-10)                    │              │
│  │                                                        │              │
│  │  <project xmlns="http://www.plcopen.org/xml/tc6_0201">│              │
│  │    <types>     → DUT (STRUCT, ENUM)                   │              │
│  │    <pous>      → POU (FB, PROGRAM, FUNCTION)          │              │
│  │    <instances> → GVL ve Task konfigürasyonu           │              │
│  │    <addData>   → CODESYS vendor uzantıları            │              │
│  │                                                        │              │
│  │  Harici Python 3 (CPython) ile PLCopen XML üretilebilir│             │
│  │  → Script Engine'e import_xml() ile verilir           │              │
│  └────────────────────────────┬───────────────────────────┘              │
│                               │ Şablon sistemi araçları bir araya getirir│
│                               ▼                                           │
│  04_generation_templates.md                                               │
│  ┌────────────────────────────────────────────────────────┐              │
│  │           ŞABLONLARla ÜRETİM AKIŞI                    │              │
│  │                                                        │              │
│  │  JSON Spec → validate() → generate_gvl_*()           │              │
│  │           → generate_fb_*() → PLCopen XML             │              │
│  │           → CODESYS headless → import + compile       │              │
│  │           → .project çıktısı                          │              │
│  │                                                        │              │
│  │  Karar ağacı:                                          │              │
│  │    Motor > 0? → FB_Motor + GVL_IO                     │              │
│  │    Analog > 0? → FB_AnalogSensor + GVL_IO             │              │
│  │    Recipe? → GVL_Recipes + FB_RecipeManager           │              │
│  │    Modbus? → GVL_Modbus + PRG_ModbusUpdate            │              │
│  └────────────────────────────────────────────────────────┘              │
└──────────────────────────────────────────────────────────────────────────┘
```

### "Agent İçin" Özet Mental Model

CODESYS proje üretimini anlamanın en kısa yolu dört cümleye sığar:

> **Dosya Yapısı**: `.project`, UTF-8 XML'dir. İçini XML olarak okuyabilirsin, ama yazmak için Script Engine kullan — yoksa formatı bozarsın.

> **Script Engine**: IronPython 2.7 ile çalışır. `app.create_pou()`, `fb.textual_declaration.replace()`, `app.import_xml()`, `proj.compile()` — temel dört API. f-string kullanma, `.format()` kullan.

> **PLCopen XML**: POU, DUT ve GVL içeriklerini CODESYS dışında (Python 3 ile) üret, Script Engine'e `import_xml()` ile ver. ST kodu kayıpsız taşınır; device tree ve I/O mapping taşınmaz.

> **Şablon Yaklaşımı**: Template `.project` device tree'yi taşır (elle hazırla). Script Engine GVL içeriklerini, FB'leri ve orkestrasyonu üretir. Üretim sırası kritik: DUT → GVL → FB → PROGRAM.

## Hızlı Referans Tabloları

### A. Script Engine Temel API

| İşlem | API Çağrısı | Not |
|---|---|---|
| Proje aç | `projects.open(path)` | Headless mod için zorunlu |
| Nesne bul | `proj.find("isim", recursive=True)` | Liste döndürür, `[0]` al |
| FB oluştur | `app.create_pou("FB_Ad", PouType.FunctionBlock)` | Varsayılan FunctionBlock |
| PROGRAM oluştur | `app.create_pou("PRG_Ad", PouType.Program)` | — |
| FUNCTION oluştur | `app.create_pou("FC_Ad", PouType.Function)` | — |
| GVL oluştur | `app.create_gvl("GVL_IO")` | — |
| ENUM oluştur | `app.create_dut("E_Ad", DutType.Enum)` | — |
| STRUCT oluştur | `app.create_dut("ST_Ad", DutType.Structure)` | — |
| Klasör oluştur | `app.create_folder("Klasor")` | FB'leri içine al |
| Deklarasyon yaz | `fb.textual_declaration.replace(metin)` | Tam blok değiştir |
| İmplementasyon yaz | `fb.textual_implementation.replace(metin)` | Tam blok değiştir |
| PLCopen import | `app.import_xml(xml_path)` | DUT/FB/GVL import |
| Library ekle | `lib_mgr.add_library(isim, versiyon, firma)` | — |
| Derle | `proj.compile()` | True/False döner |
| Kaydet | `projects.save()` | — |
| Kapat | `projects.close()` | Headless için |

### B. PLCopen XML Yapı Taşları

| CODESYS Nesnesi | PLCopen XML Elementi | Konum |
|---|---|---|
| FUNCTION_BLOCK | `<pou pouType="functionBlock">` | `<pous>` altında |
| PROGRAM | `<pou pouType="program">` | `<pous>` altında |
| FUNCTION | `<pou pouType="function">` | `<pous>` altında |
| STRUCT | `<dataType>` + `<structured>` | `<types><dataTypes>` altında |
| ENUM | `<dataType>` + `<enumerated>` | `<types><dataTypes>` altında |
| GVL | `<globalVars name="...">` | `<instances><configurations><resource>` altında |
| Task | `<task name="..." interval="T#10ms" priority="1">` | Resource altında |
| ST kodu | `<body><ST><xhtml>...</xhtml></ST></body>` | `<pou>` içinde |

### C. IEC Tip XML Gösterimi (PLCopen XML)

| IEC Tipi | XML Gösterimi |
|---|---|
| BOOL | `<BOOL/>` |
| INT / UINT / DINT | `<INT/>` / `<UINT/>` / `<DINT/>` |
| REAL / LREAL | `<REAL/>` / `<LREAL/>` |
| TIME | `<TIME/>` |
| STRING(80) | `<string length="80"/>` |
| WORD / DWORD | `<WORD/>` / `<DWORD/>` |
| Kullanıcı tipi (ENUM/STRUCT) | `<derived name="E_MotorState"/>` |
| Dizi (0..9 INT) | `<array><dimension lower="0" upper="9"/><baseType><INT/></baseType></array>` |

### D. .project XML Nesneleri

| CODESYS Nesnesi | XML Etiketi | Önemli Attribute |
|---|---|---|
| PROGRAM | `<pou>` | `pouType="program"` |
| FUNCTION_BLOCK | `<pou>` | `pouType="functionBlock"` |
| FUNCTION | `<pou>` | `pouType="function"` |
| GVL | `<globalVarList>` | `name="GVL_IO"` |
| STRUCT | `<dut>` | `type="Structure"` |
| ENUM | `<dut>` | `type="Enum"` |
| Task | `<Task>` | `interval`, `priority`, `type="Cyclic"` |
| Device | `<device>` | `typeGuid="..."` (platforma özgü) |
| Library Manager | `<libraryManager>` | — |
| Klasör | `<Folder>` | `name="..."` |

### E. PLCopen XML — Taşınanlar ve Taşınmayanlar

```
TAŞINANLAR (platform bağımsız):
  POU içerikleri (ST, LD, FBD, SFC temsil)
  Değişken bildirimleri (isim, tip, başlangıç değeri)
  DUT (STRUCT, ENUM, ALIAS)
  GVL değişken listeleri
  Task yapılandırması (isim, interval, priority)

TAŞINMAYANLAR (platform/vendor özgü):
  Device tree (EtherCAT slave, Modbus konfigürasyonu)
  I/O mapping (AT %I / %Q adresleri)
  Library Manager referansları
  OPC UA / MQTT / Visualization konfigürasyonu
  Symbol Configuration
  CODESYS Runtime konfigürasyonu
```

### F. Kritik Kurallar ve Eşik Değerler

| Kural | Değer / Açıklama | Kaynak |
|---|---|---|
| Script Engine Python versiyonu | IronPython 2.7 — f-string yok, `.format()` kullan | Belge 2 |
| Headless başlatma | `CODESYS.exe --noUI --runscript=... --scriptargs=...` | Belge 2 |
| Headless'ta `projects.primary` | None olabilir — `projects.open()` gerekli | Belge 2 |
| POU üretim sırası | DUT → GVL → FB → PROGRAM | Belge 4 |
| BOM sorunu | `.project` ve PLCopen XML UTF-8-BOM olabilir — `encoding='utf-8-sig'` kullan | Belge 1, 3 |
| typeGuid | Platforma ve CODESYS versiyonuna göre değişir — hardcode etme | Belge 1 |
| Device tree | Template'de hazır olmalı — Script Engine ile oluşturma zordur | Belge 4 |
| Derleme kontrolü | `proj.compile()` → True/False — başarısızsa projeyi kaydetme | Belge 4 |

## Pratikte Nasıl Kullanılır

### "İlk Otomatik Üretim" Kontrol Listesi

Aşağıdaki adımlar, bir spesifikasyondan derlenebilir CODESYS projesi üretmenin minimum çalışan akışıdır.

**Hazırlık (IDE'de Elle — Bir Kez)**

```
□ 1. Hedef platforma uygun device tree içeren BaseProject.project hazırla
□ 2. Library Manager: Standard + Util kütüphanelerini ekle
□ 3. Task Configuration: MainTask (Cyclic, 10ms, Priority 2) oluştur
□ 4. Application altında boş GVL'ler oluştur (GVL_IO, GVL_Params, GVL_Alarms)
□ 5. PLC_PRG var — içeriği boş
□ 6. Template'i kaydet: C:\Templates\BaseProject.project
```

**Harici Üretim (Python 3 — Her Proje İçin)**

```
□ 7. spec.json oluştur: proje adı, motor listesi, task tanımları
□ 8. validate_spec(spec) — I/O adresi çakışması, task referansı kontrol
□ 9. generate_gvl_io_content(spec) → GVL_IO deklarasyon metni üret
□ 10. generate_fb_motor_declaration(motor_name) → FB deklarasyon metni
□ 11. generate_fb_motor_implementation(motor_name) → FB implementasyon metni
□ 12. PLCopen XML üret: DUT + FB'leri pous_xml/ klasörüne yaz
□ 13. generate_prg_control_content(spec) → Orkestrasyon kodu üret
□ 14. Üretilenleri spec['_generated']'a ekle, config_final.json yaz
```

**Script Engine (IronPython 2.7 — CODESYS headless)**

```
□ 15. Template'i output_path'e kopyala (shutil.copy)
□ 16. projects.open(output_path)
□ 17. app = proj.find("Application", recursive=True)[0]
□ 18. GVL içeriklerini textual_declaration.replace() ile güncelle
□ 19. pous_xml/ klasöründeki her .xml için app.import_xml(xml_path)
□ 20. PRG'yi güncelle: declaration + implementation
□ 21. Library ekle: lib_mgr.add_library("Util", "3.5.17.0", "System")
□ 22. projects.save()
□ 23. result = proj.compile() — False ise hata fırlat
□ 24. projects.close()
```

### Agent İçin Üretim Karar Ağacı

```
Spesifikasyon analizi:
│
├─► Motor sayısı > 0?
│   ├── Evet → E_MotorState ENUM üret (DUT)
│   │         FB_<ad> üret (her motor için)
│   │         GVL_IO: x<ad>_RunCmd, x<ad>_RunFB, x<ad>_FaultFB
│   │         GVL_Params: t<ad>_StartDelay
│   │         GVL_Alarms: xAlarm_<ad>_Fault
│   └── Hayır → Motor bölümü atla
│
├─► Analog giriş > 0?
│   ├── Evet → FB_AnalogSensor üret, GVL_IO: w<ad>_Raw (WORD)
│   └── Hayır → Atla
│
├─► Recipe etkin?
│   ├── Evet → GVL_Recipes (RETAIN), FB_RecipeManager üret
│   └── Hayır → Atla
│
├─► Modbus TCP slave?
│   ├── Evet → GVL_Modbus, PRG_ModbusUpdate → Task_Background'a ata
│   └── Hayır → Atla
│
└─► OPC UA?
    ├── Evet → Symbol Configuration (manuel adım gerekir)
    └── Hayır → Atla

Task atama kuralları:
  Safety mantığı    → Task_Safety  (Priority 0, 5ms)
  Motor / kontrol   → Task_Control (Priority 2, 10ms)
  HMI / OPC UA      → Task_HMI    (Priority 5, 100ms)
  Modbus / log      → Task_Background (Priority 15, Freewheeling)
```

### Üç Belgeyi Bağlayan Tam Üretim Senaryosu

**Görev**: İki konveyör motorlu paketleme hattı projesi oluştur.

```
ADIM 1 — Spec hazırla (JSON)
  {
    "project": {"name": "PackagingLine"},
    "motors": [
      {"name": "Conveyor1", "io_run_cmd": "%Q0.0", "io_run_fb": "%I0.0",
       "io_fault_fb": "%I0.1", "start_delay_ms": 3000, "task": "Task_Control"},
      {"name": "Conveyor2", "io_run_cmd": "%Q0.1", "io_run_fb": "%I0.2",
       "io_fault_fb": "%I0.3", "start_delay_ms": 2000, "task": "Task_Control"}
    ],
    "tasks": [{"name": "Task_Control", "interval_ms": 10, "priority": 2}],
    "libraries": [
      {"name": "Standard", "version": "3.5.17.0", "company": "System"},
      {"name": "Util",     "version": "3.5.17.0", "company": "System"}
    ]
  }

ADIM 2 — Harici Python 3 ile üret
  python3 generate.py spec.json --output-dir /tmp/gen/

  Üretilen PLCopen XML (/tmp/gen/pous/):
    E_MotorState.xml   ← ENUM DUT
    ST_MotorDiag.xml   ← STRUCT DUT
    FB_Conveyor1.xml   ← Function Block
    FB_Conveyor2.xml   ← Function Block

  Üretilen GVL içerikleri (spec içine gömülü string):
    GVL_IO      → xConveyor1_RunCmd AT %Q0.0 : BOOL; ...
    GVL_Params  → tConveyor1_StartDelay : TIME := T#3.0S; ...
    GVL_Alarms  → xAlarm_Conveyor1_Fault : BOOL; ...

  Üretilen PRG_ConveyorControl:
    VAR: fbConveyor1 : FB_Conveyor1; fbConveyor2 : FB_Conveyor2;
    IMPL: fbConveyor1(xStartCmd := GVL_HMI.xConveyor1_Start, ...);
          GVL_IO.xConveyor1_RunCmd := fbConveyor1.xRunOutput;
          ...
          GVL_Alarms.xAnyActiveAlarm := GVL_Alarms.xAlarm_Conveyor1_Fault
                                     OR GVL_Alarms.xAlarm_Conveyor2_Fault;

ADIM 3 — Script Engine ile CODESYS (IronPython 2.7)
  CODESYS.exe --noUI --runscript=/tmp/gen/codesys_script.py \
              --scriptargs=/tmp/gen/spec_final.json

  Script içinde:
    shutil.copy("BaseProject.project", "PackagingLine.project")
    proj = projects.open("PackagingLine.project")
    app = proj.find("Application", recursive=True)[0]
    gvl_io.textual_declaration.replace(spec['_generated']['gvl_io'])
    app.import_xml("/tmp/gen/pous/E_MotorState.xml")
    app.import_xml("/tmp/gen/pous/FB_Conveyor1.xml")
    ...
    lib_mgr.add_library("Util", "3.5.17.0", "System")
    projects.save()
    result = proj.compile()  # → True
    projects.close()

ADIM 4 — Sonuç
  PackagingLine.project → derlenebilir, indirilebilir
```

## Sık Yapılan Hatalar

**1. IronPython 2.7'de Python 3 sözdizimi kullanmak** (Belge 2)
f-string (`f"..."`) ve walrus operatörü (`:=`) Script Engine'de çalışmaz. Her zaman `.format()` kullan, dosyanın başına `from __future__ import print_function` ekle.

**2. `projects.primary`'yi None kontrolü yapmadan kullanmak** (Belge 2)
Headless modda `projects.primary` her zaman None'dır. `projects.open(path)` ile projeyi açmadan hiçbir işlem yapılamaz.

**3. POU üretim sırasını gözetmemek** (Belge 4)
POU'lar birbirine bağımlıdır: FB_Motor, E_MotorState ENUM'unu kullanır. ENUM DUT, FB'den önce import edilmezse derleme hatası çıkar. Zorunlu sıra: DUT → GVL → FB → PROGRAM.

**4. Template'de device tree olmadan başlamak** (Belge 4)
Script Engine ile device tree oluşturmak karmaşık ve kırılgandır (typeGuid platforma göre değişir). Template .project her zaman device tree ve boş Application içermelidir.

**5. BOM karakterini görmezden gelmek** (Belge 1, 3)
CODESYS'in ürettiği `.project` ve PLCopen XML dosyaları UTF-8-BOM içerebilir. Python'da her zaman `encoding='utf-8-sig'` kullan, yoksa XML parser patlayacaktır.

**6. Derleme hatasını sessizce geçmek** (Belge 4)
`proj.compile()` False döndürdüğünde projeyi kaydetme; hata mesajlarını oku, sorunlu bölümü tespit et, yeniden üret ve tekrar dene. Ortalama 2–3 iterasyonda başarılı derleme elde edilir.

**7. typeGuid'i kodda sabit yazmak** (Belge 1)
Farklı CODESYS versiyonlarında aynı cihazın typeGuid'i değişebilir. Device referanslarını Script Engine'in `system.get_all_devices()` ile dinamik olarak al.

**8. PLCopen XML ile tüm konfigürasyonu taşımaya çalışmak** (Belge 3)
PLCopen XML yalnızca POU içeriklerini, DUT'ları ve GVL'leri taşır. Device tree, I/O mapping, kütüphane referansları ve OPC UA konfigürasyonu taşınmaz — bunlar her zaman Script Engine veya elle yapılmalıdır.

## Ne Zaman ...

### Otomatik Üretim Ne Zaman Değerlidir?

```
Güçlü tercih:
  ✓ 5+ benzer makine, farklı parametreli proje (OEM senaryosu)
  ✓ I/O listesi sık değişiyor, projenin de güncellenmesi gerekiyor
  ✓ CI/CD pipeline içinde otomatik derleme ve test
  ✓ Farklı müşteri konfigürasyonları (motor sayısı, sensör tipi)

Zayıf tercih — manuel daha iyi:
  ✗ Tek proje, tek müşteri, nadir değişiklik
  ✗ Karmaşık PID tuning veya motion path (şablona girmez)
  ✗ Güvenlik (SIL) projeleri — otomatik üretim doğrulama zorlaştırır
```

### Hangi Araç Ne Zaman?

```
Senaryo                                     Araç
──────────────────────────────────────────────────────────────────
POU, GVL, DUT oluştur/güncelle              Script Engine
Device tree konfigürasyonu                  Template .project (elle)
POU içeriklerini CODESYS dışında üret       PLCopen XML + Python 3
Mevcut projeyi analiz et / raporla          .project XML + Python ET
Çapraz platform POU transfer (ABB→CODESYS)  PLCopen XML import
Proje içeriğini Git'te takip et             PLCopen XML export
Script'i tekrarlayan CI sürecinde çalıştır  Headless (--noUI)
Library listesini yönet                     Script Engine
```

### Hibrit Yaklaşım — Neyi Otomatik, Neyi Manuel Yaz?

```
Otomatik üret:                   Manuel hazırla (Template'de sabit tut):
─────────────────────────         ─────────────────────────────────────
GVL içerikleri                    Device tree (EtherCAT, Modbus HW)
Standart FB'ler (Motor, Sensör)   Task yapısı ve isimleri
I/O adres atamaları               Kütüphane listesi
PRG orkestrasyonu                 PID tuning değerleri
Alarm özeti mantığı               Motion path parametreleri
Temel task atamaları              Güvenlik mantığı detayı
Library versiyonları              Müşteriye özgü iş mantığı
```

## Gerçek Proje Notları

**Sentez Notu 1 — Dört Belge Arasındaki Zihinsel Geçiş**
Yeni başlayanların en sık sorusu: "PLCopen XML mi kullansam, yoksa doğrudan Script Engine mi?" Yanıt: İkisi rakip değil, ortaktır. PLCopen XML içerikleri dışarıda (Python 3 ile) üretir; Script Engine bu içerikleri projeye yerleştirir ve konfigürasyonu tamamlar. En güçlü yaklaşım her zaman ikisinin kombinasyonudur.

**Sentez Notu 2 — Agent'ın Bu Klasördeki Bilgiyi Kullanma Şekli**
Bir agent "3 motorlu konveyör hattı için CODESYS projesi oluştur" komutunu aldığında şu akışı izlemeli:
1. Spec JSON üret (motor isimleri, I/O adresleri, task tanımları)
2. DUT XML'lerini PLCopen formatında yaz (E_MotorState, ST_MotorDiag)
3. Her motor için FB XML'i PLCopen formatında yaz
4. GVL içerik metinlerini üret
5. PRG orkestrasyon metnini üret
6. Script Engine'e tüm bunları pas et (headless veya IDE)
7. Derleme başarısızsa iterasyona devam et

**Sentez Notu 3 — "40 Hata" Dersi (İlk Üretim)**
İlk otomatik üretim denemesinde 40 derleme hatası çıktı — hepsi aynı neden: "E_MotorState tipi bulunamadı." DUT'lar FB'lerden önce import edilmemişti. Bağımlılık sırası gözetildiğinde sıfır hatayla derleme sağlandı. Bu sırayı hiç unutma: DUT → GVL → FB → PROGRAM.

**Sentez Notu 4 — Template'in Değeri**
Template `.project` ne kadar sağlamsa, script o kadar basit olur. Template'de her şey hazırsa (device tree, library, task iskeleti, boş GVL'ler), script sadece içerik üretir — mimari oluşturmaz. Template değişince tüm üretimler etkilenir: bu tek nokta güncellemesi hem avantaj hem sorumluluktur.

**Sentez Notu 5 — CI/CD'de Lisans Tuzağı**
Headless modda Script Engine çalıştırırken CI sunucusunda CODESYS lisansı gerekir. Demo lisansla headless mümkün değildir. CI makinesine lisans dosyası kurularak çözülür; geliştirme aşamasında bunu geç keşfetmek zaman kaybettirir — CI ortamında erken test yapılmalıdır.

**Sentez Notu 6 — Spesifikasyonu Projeyle Birlikte Sakla**
Üretilen her `.project` dosyasıyla birlikte kullanılan `spec.json` version control'e alınmalıdır. "Bu proje neden bu şekilde üretildi?" sorusu bir yıl sonra kaçınılmaz olarak gelir — cevap spec.json'dadır.

## İlgili Konular

```
knowledge/codesys/project-generation/   ← Şu an buradasınız
├── 01_project_file_structure.md  → .project XML anatomisi, Python ile parse
├── 02_script_engine.md           → IronPython API, headless çalıştırma
├── 03_plcopen_xml.md             → POU/DUT/GVL XML formatı, üretim/import
├── 04_generation_templates.md    → Tam üretim akışı, JSON spec şeması
└── _synthesis.md (bu belge)

Önkoşul:
knowledge/codesys/fundamentals/
├── 02_project_structure.md       → IDE'deki görsel yapı — bu belgelerin karşı tarafı
└── 03_iec61131_languages.md      → Üretilen POU içeriklerinde kullanılan diller

Sonraki adım — Üretilen İçeriklerin Detayı:
knowledge/codesys/programming/
├── 01_pou_types.md               → Üretilecek FB, PRG, FC tasarımı
├── 02_gvl_design.md              → GVL organizasyon şeması
└── 03_function_blocks.md         → Şablon FB içerikleri

knowledge/codesys/task-structure/
└── _synthesis.md                 → Task yapısı tasarım kuralları

Araçlar:
  Python xml.etree.ElementTree    → .project ve PLCopen XML parse/üretim
  xmllint / xmlstarlet            → XML doğrulama ve formatlama
  openpyxl                        → Excel'den I/O listesi okuma
  CODESYS Forge Scripting         → https://forge.codesys.com/tol/scripting/
  GitHub tkucic automation        → https://github.com/tkucic/codesys_workflow_automation
```
