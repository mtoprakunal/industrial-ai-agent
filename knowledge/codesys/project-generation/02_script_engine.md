---
KONU        : CODESYS Script Engine
KATEGORİ    : codesys
ALT_KATEGORI: project-generation
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Scripting/_script_scripting_with_codesys.html"
    başlık: "CODESYS Online Help — Scripting with CODESYS"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Scripting/_cds_access_cds_func_in_python_scripts.html"
    başlık: "CODESYS Online Help — Using Scripts to Access CODESYS Functionalities"
    güvenilirlik: resmi
  - url: "https://forge.codesys.com/tol/scripting/home/Home/"
    başlık: "CODESYS Forge — Scripting Home (topluluk merkezi)"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/tol/scripting/snippets/3/"
    başlık: "CODESYS Forge — Snippet #3: Create a FB"
    güvenilirlik: topluluk
  - url: "https://github.com/tkucic/codesys_workflow_automation"
    başlık: "GitHub — CODESYS Workflow Automation"
    güvenilirlik: topluluk
  - url: "https://controlbyte.tech/blog/python-scripting-engine-for-codesys-claude-sonnet-programming-part-1/"
    başlık: "ControlByte.tech — Python Scripting Engine for CODESYS Part 1"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_project_file_structure.md"
    ilişki: gerektirir
  - konu: "04_generation_templates.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Python (IronPython 2.7) temel sözdizimi"
  - "CODESYS proje dosyası iç yapısı (01_project_file_structure.md)"
  - "CODESYS IDE'yi nasıl kullanacağını bilmek"
ÇELİŞKİLER :
  - kaynak: "IronPython 2.7 vs CPython 3.x"
    konu: "CODESYS Script Engine IronPython 2.7 kullanır; modern Python 3 sözdizimi çalışmaz"
    çözüm: >
      f-string (f"hello {name}"), walrus operatörü (:=), type hints gibi
      Python 3'e özgü özellikler Script Engine'de derleme hatası verir.
      CODESYS Forge'daki örnekler IronPython 2.7 sözdizimi kullanır.
      Format strings için .format() veya % kullan. print() yerine print ifadesi değil,
      print() fonksiyonu kullan (from __future__ import print_function ekle).
  - kaynak: "Script Engine çalışma modları"
    konu: "IDE içi script vs headless (--noUI) komut satırı script davranışı farklı"
    çözüm: >
      IDE içinde: projects.primary mevcut açık projeyi döndürür.
      Headless: projects.primary = None; önce projects.open() gerektirir.
      Her iki mod için çalışan scriptler try/except ile projects.primary
      None kontrolü yapmalıdır.
---

## Özün Ne

CODESYS Script Engine, IDE'nin IronPython 2.7 ile erişilebilen tam bir otomasyon katmanıdır. "Tüm manuel tıklamalarla yapılan her şey script ile yapılabilir" — bu CODESYS'in resmi vaadi. Proje oluşturma, POU ekleme, GVL doldurma, task yapılandırma, library ekleme, online bağlantı, download ve hatta compile — hepsi scriptlenebilir. Script Engine'i kavramak, CODESYS proje üretiminin kapısını açar: bir JSON veya Excel spesifikasyonundan sıfırdan çalışan bir PLC projesi oluşturmak mümkün hale gelir.

## Nasıl Çalışır

### Script Engine Mimarisi

```
Dış Kaynak (JSON / Excel / Veritabanı)
        │
        │ Proje Spesifikasyonu
        ▼
┌──────────────────────────────────────────────────────────┐
│                  Python Script (.py)                     │
│              (IronPython 2.7 sözdizimi)                  │
│                                                          │
│  from scriptengine import *   ← Otomatik import         │
│                                                          │
│  ┌──────────────────────────────────────────────┐       │
│  │         CODESYS Scripting API               │       │
│  │                                              │       │
│  │  projects  → Proje yönetimi                │       │
│  │  system    → IDE ve sistem işlemleri        │       │
│  │  online    → Runtime bağlantısı             │       │
│  │  ui        → Kullanıcı arayüzü              │       │
│  └──────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────┘
        │
        ▼
CODESYS .project dosyası (manipüle edilmiş)
```

### Script Çalıştırma Yöntemleri

**Yöntem 1 — IDE Menüsü:**
```
Tools → Scripting → Run Script → .py dosyasını seç
```

**Yöntem 2 — Toolbar Butonu:**
```
Tools → Customize... → Commands → Scripting → "Run Script File"
Toolbar'a sürükle → Script dosya yolunu konfigüre et
```

**Yöntem 3 — Headless (Komut Satırı):**
```cmd
:: Windows
CODESYS.exe --profile="CODESYS V3.5 SP21" --noUI --runscript="C:\scripts\generate.py"

:: Argüman geçirme (V3.5 SP10+)
CODESYS.exe --noUI --runscript="generate.py" --scriptargs="config.json"
```

**Yöntem 4 — Script Commands (Toolbar Entegrasyonu):**
```
Script Commands klasörü: C:\ProgramData\CODESYS\Script Commands\
Klasöre .py dosyası + config.json + ikon koy → Tools menüsünde görünür
```

### Ana API Nesneleri

```python
# Implicit import — script başlarken otomatik:
# from scriptengine import *

# --- PROJELER ---
proj = projects.primary          # Açık projeyi al (IDE modunda)
proj = projects.open(r"C:\path\MyProject.project")  # Projeyi aç
projects.save()                  # Kaydet
projects.close()                 # Kapat

# Proje içinde nesne bul
found = proj.find("Application", recursive=True)
app = found[0]                   # İlk bulunan

# --- PROJE NESNELERİ OLUŞTURMA ---
# POU (Function Block, Program, Function)
fb = app.create_pou("FB_Motor")
prg = app.create_pou("PRG_Control", PouType.Program)
fc = app.create_pou("FC_Scale", PouType.Function)

# GVL
gvl = app.create_gvl("GVL_IO")

# DUT
dut = app.create_dut("ST_MotorData", DutType.Structure)
enum = app.create_dut("E_MotorState", DutType.Enum)

# Klasör
folder = app.create_folder("Motor_FBs")
fb_in_folder = folder.create_pou("FB_ConveyorMotor")

# --- TEXTUAL MANIPULATION ---
# Deklarasyon bloğunu tümüyle değiştir
fb.textual_declaration.replace("""
FUNCTION_BLOCK FB_Motor
VAR_INPUT
    xStartCmd : BOOL;
    xStopCmd  : BOOL;
END_VAR
VAR_OUTPUT
    xRunOutput : BOOL;
    xFault     : BOOL;
END_VAR
VAR
    tTimer : TON;
END_VAR
""")

# Implementasyon bloğunu değiştir
fb.textual_implementation.replace("""
IF xStartCmd AND NOT xFault THEN
    xRunOutput := TRUE;
END_IF
IF xStopCmd THEN
    xRunOutput := FALSE;
END_IF
""")

# Belirli satır ve sütuna içerik ekle (insert)
gvl.textual_declaration.insert(line=2, column=0, text="    xNewVariable : BOOL;\n")

# --- LIBRARY MANAGER ---
lib_manager = app.find("Library Manager", recursive=True)[0]
lib_manager.add_library("Util", "3.5.17.0", "System")

# --- BUILD ---
proj.compile()          # Derle
# proj.clean()          # Temizle

# --- ONLINE ---
# online.login(device, application)   # Bağlan ve yükle
# online.start(application)           # Çalıştır
```

### PouType ve DutType Enum'ları

```python
# PouType sabitleri
PouType.Program        # PROGRAM
PouType.FunctionBlock  # FUNCTION_BLOCK (varsayılan)
PouType.Function       # FUNCTION

# DutType sabitleri
DutType.Structure      # STRUCT (varsayılan)
DutType.Enum           # ENUM
DutType.Alias          # TYPE ... : baseTYPE
DutType.Union          # UNION
```

## Pratikte Nasıl Kullanılır

### Adım 1: Script Ortamını Hazırla

```python
# generate_project.py — Başlık şablonu
# encoding: utf-8
from __future__ import print_function  # IronPython 2.7 uyumu

import sys
import os

# Script Engine'den geçirilen argümanlar
# CODESYS.exe --runscript=generate.py --scriptargs="config.json"
config_path = None
if len(sys.argv) > 1:
    config_path = sys.argv[1]

# JSON konfigürasyon yükle
import json
if config_path and os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
else:
    # Varsayılan test konfigürasyonu
    config = {
        "project_name": "TestProject",
        "motors": ["Motor1", "Motor2"],
        "tasks": [
            {"name": "Task_Control", "interval": 10, "priority": 2}
        ]
    }

print("Config loaded: {}".format(config.get("project_name")))
```

### Adım 2: Proje Aç veya Oluştur

```python
# Template projeyi aç ve kopyala
import shutil

template_path = r"C:\Templates\BaseProject.project"
output_path = r"C:\Projects\{}.project".format(config["project_name"])

# Template'i kopyala
shutil.copy(template_path, output_path)

# Kopyalanan projeyi aç
proj = projects.open(output_path)
print("Project opened: {}".format(output_path))

# Application nesnesini bul
found = proj.find("Application", recursive=True)
if not found:
    raise Exception("Application not found in template!")
app = found[0]
```

### Adım 3: GVL Üretimi

```python
def generate_gvl_io(app, motor_list):
    """Motor listesinden GVL_IO üretir."""
    
    # Mevcut GVL_IO'yu bul veya oluştur
    found = app.find("GVL_IO", recursive=False)
    if found:
        gvl = found[0]
    else:
        gvl = app.create_gvl("GVL_IO")
    
    # Deklarasyon içeriği oluştur
    lines = [
        "{attribute 'qualified_only'}",
        "VAR_GLOBAL",
        "    (* === MOTOR I/O =================================== *)",
    ]
    
    for i, motor_name in enumerate(motor_list):
        offset = i
        lines.append("    (* {} *)".format(motor_name))
        lines.append("    x{}_RunFB    AT %I{}.0 : BOOL;   (* Çalışma geri bildirimi *)".format(motor_name, offset))
        lines.append("    x{}_FaultFB  AT %I{}.1 : BOOL;   (* Arıza geri bildirimi *)".format(motor_name, offset))
        lines.append("    x{}_RunCmd   AT %Q{}.0 : BOOL;   (* Çalıştırma komutu *)".format(motor_name, offset))
        lines.append("")
    
    lines.append("END_VAR")
    
    declaration = "\n".join(lines)
    gvl.textual_declaration.replace(declaration)
    print("GVL_IO generated with {} motors".format(len(motor_list)))

generate_gvl_io(app, config["motors"])
```

### Adım 4: Function Block Üretimi

```python
def generate_motor_fb(app, motor_name):
    """Motor adına göre FB üretir."""
    
    fb_name = "FB_{}".format(motor_name)
    
    # Klasör oluştur (yoksa)
    found_folder = app.find("Motor_FBs", recursive=False)
    if found_folder:
        folder = found_folder[0]
    else:
        folder = app.create_folder("Motor_FBs")
    
    # FB oluştur
    fb = folder.create_pou(fb_name, PouType.FunctionBlock)
    
    # Deklarasyon
    declaration = """FUNCTION_BLOCK {fb_name}
VAR_INPUT
    xStartCmd   : BOOL;
    xStopCmd    : BOOL;
    xFaultReset : BOOL;
    tStartDelay : TIME := T#3S;
END_VAR
VAR_OUTPUT
    xRunOutput  : BOOL;
    xFault      : BOOL;
    eState      : E_MotorState;
    sFaultMsg   : STRING(80);
END_VAR
VAR
    tStartTimer : TON;
    fbResetEdge : R_TRIG;
END_VAR""".format(fb_name=fb_name)
    
    # Implementasyon (state machine şablonu)
    implementation = """fbResetEdge(CLK := xFaultReset);

CASE eState OF

    eIdle:
        xRunOutput := FALSE;
        IF xStartCmd AND NOT xFault THEN
            tStartTimer(IN := FALSE);
            eState := eStarting;
        END_IF

    eStarting:
        xRunOutput := TRUE;
        tStartTimer(IN := TRUE, PT := tStartDelay);
        IF tStartTimer.Q THEN
            tStartTimer(IN := FALSE);
            eState := eRunning;
        END_IF
        IF xStopCmd THEN
            tStartTimer(IN := FALSE);
            eState := eIdle;
        END_IF

    eRunning:
        xRunOutput := TRUE;
        IF xStopCmd THEN
            eState := eStopping;
        END_IF

    eStopping:
        xRunOutput := FALSE;
        eState := eIdle;

    eFault:
        xRunOutput := FALSE;
        IF fbResetEdge.Q THEN
            xFault := FALSE;
            sFaultMsg := '';
            eState := eIdle;
        END_IF

    ELSE:
        xRunOutput := FALSE;
        eState := eFault;
END_CASE"""
    
    fb.textual_declaration.replace(declaration)
    fb.textual_implementation.replace(implementation)
    
    print("FB created: {}".format(fb_name))
    return fb

for motor in config["motors"]:
    generate_motor_fb(app, motor)
```

### Adım 5: Task Yapılandırması

```python
def configure_tasks(app, task_config_list):
    """Task'ları yapılandırır."""
    
    task_config = app.find("Task Configuration", recursive=True)
    if not task_config:
        print("Warning: Task Configuration not found")
        return
    
    tc = task_config[0]
    
    for task_def in task_config_list:
        task_name = task_def["name"]
        interval_ms = task_def["interval"]   # millisecond
        priority = task_def["priority"]
        
        # Mevcut task bul veya yeni oluştur
        found_task = tc.find(task_name, recursive=False)
        if found_task:
            task = found_task[0]
        else:
            # Task oluşturma — API sınırlı, XML manipülasyon gerekebilir
            # Genellikle template'de task var, parametreler güncellenir
            task = tc.find("MainTask", recursive=False)
            if task:
                task = task[0]
        
        # Task parametrelerini güncelle (CODESYS V3.5 SP16+)
        if hasattr(task, 'set_interval'):
            task.set_interval(interval_ms * 1000)  # microsecond
        
        print("Task configured: {} ({}ms, Prio:{})".format(
            task_name, interval_ms, priority))

configure_tasks(app, config["tasks"])
```

### Adım 6: Kaydet ve Derle

```python
# Projeyi kaydet
projects.save()
print("Project saved.")

# Derleme dene
try:
    result = proj.compile()
    if result:
        print("Compilation SUCCESS")
    else:
        print("Compilation FAILED — check for errors")
except Exception as e:
    print("Compilation error: {}".format(str(e)))

# Kapat (headless mod için)
# projects.close()
```

## Örnekler

### Örnek 1: Headless Çalıştırma — Batch Script

```batch
@echo off
:: generate_all_machines.bat

SET CODESYS="C:\Program Files\CODESYS 3.5.21\CODESYS\Common\CODESYS.exe"
SET SCRIPT="C:\AutoGen\generate_machine.py"
SET CONFIGS_DIR="C:\AutoGen\configs"

FOR %%f IN ("%CONFIGS_DIR%\*.json") DO (
    echo Generating project for %%~nf ...
    %CODESYS% --profile="CODESYS V3.5 SP21" ^
               --noUI ^
               --runscript="%SCRIPT%" ^
               --scriptargs="%%f"
    echo Done: %%~nf
)
echo All projects generated.
```

### Örnek 2: DUT (STRUCT ve ENUM) Oluşturma

```python
def create_motor_duts(app):
    """Motor için gerekli DUT'ları oluşturur."""
    
    # ENUM oluştur
    state_enum = app.create_dut("E_MotorState", DutType.Enum)
    state_enum.textual_declaration.replace("""TYPE E_MotorState :
(
    eIdle      := 0,
    eStarting  := 1,
    eRunning   := 2,
    eStopping  := 3,
    eFault     := 4
);
END_TYPE""")
    
    # STRUCT oluştur
    motor_struct = app.create_dut("ST_MotorDiag", DutType.Structure)
    motor_struct.textual_declaration.replace("""TYPE ST_MotorDiag :
STRUCT
    tTotalRunTime  : TIME;
    dwStartCount   : DWORD;
    xLastFault     : BOOL;
    sFaultMessage  : STRING(80);
END_STRUCT
END_TYPE""")
    
    print("DUTs created: E_MotorState, ST_MotorDiag")

create_motor_duts(app)
```

### Örnek 3: Mevcut POU'yu Güncelleme

```python
def update_main_program(app, motor_list):
    """PLC_PRG'yi motor instance'larıyla doldurur."""
    
    found = app.find("PLC_PRG", recursive=True)
    if not found:
        print("PLC_PRG not found")
        return
    prg = found[0]
    
    # VAR bildirimi oluştur
    var_lines = ["VAR"]
    for motor in motor_list:
        var_lines.append("    fb{} : FB_{};".format(motor, motor))
    var_lines.append("END_VAR")
    
    # Implementation oluştur
    impl_lines = ["(* Motor FB çağrıları *)"]
    for motor in motor_list:
        impl_lines.append("fb{}(".format(motor))
        impl_lines.append("    xStartCmd   := GVL_HMI.x{}_Start,".format(motor))
        impl_lines.append("    xStopCmd    := GVL_HMI.x{}_Stop".format(motor))
        impl_lines.append(");")
        impl_lines.append("GVL_IO.x{}_RunCmd := fb{}.xRunOutput;".format(motor, motor))
        impl_lines.append("")
    
    declaration = "PROGRAM PLC_PRG\n" + "\n".join(var_lines)
    implementation = "\n".join(impl_lines)
    
    prg.textual_declaration.replace(declaration)
    prg.textual_implementation.replace(implementation)
    
    print("PLC_PRG updated with {} motors".format(len(motor_list)))

update_main_program(app, config["motors"])
```

### Örnek 4: PLCopen XML Import ile Şablon POU Ekleme

```python
def import_pou_from_xml(app, xml_file_path):
    """Hazır PLCopen XML dosyasından POU'yu projeye import et."""
    
    # import_xml: PLCopen XML formatından nesne import eder
    app.import_xml(xml_file_path)
    print("Imported from: {}".format(xml_file_path))

# Örnek: Hazır alarm yönetim FB'sini her projeye ekle
import_pou_from_xml(app, r"C:\Templates\FB_AlarmManager.xml")
```

## Sık Yapılan Hatalar

### Hata 1: IronPython 2.7 Sözdizimi Uyumsuzluğu

```python
# ❌ Python 3 özellikleri — ÇALIŞMAZ
name = "Motor"
print(f"Creating {name}")          # f-string: IronPython'da yok
result = [x for x in range(10) if (y := x * 2) > 5]  # walrus: yok

# ✅ IronPython 2.7 uyumlu
from __future__ import print_function
name = "Motor"
print("Creating {}".format(name))  # .format() çalışır
# veya: print("Creating %s" % name)
```

### Hata 2: projects.primary'nin None Olması

```python
# ❌ Yanlış — Headless modda çöker
proj = projects.primary
app = proj.find("Application", True)[0]  # AttributeError: None has no attribute 'find'

# ✅ Doğru — Kontrol + headless için open()
proj = projects.primary
if proj is None:
    # Headless mod veya proje açık değil
    proj = projects.open(r"C:\path\project.project")

if proj is None:
    raise Exception("Cannot open project!")
```

### Hata 3: find() Sonucunun Boş Olması

```python
# ❌ Hata — Sonuç boşsa IndexError
app = proj.find("Application", True)[0]

# ✅ Güvenli
results = proj.find("Application", recursive=True)
if not results:
    raise Exception("Application object not found in project!")
app = results[0]
```

### Hata 4: textual_declaration.replace() Sözdizimi Hatası

```python
# ❌ Yanlış — ST sözdizimi hatası varsa sessizce başarısız olabilir
fb.textual_declaration.replace("FUNCTION_BLOCK FB_Test\nVAR_INPUT\nx : BOOL\nEND_VAR")
# "x : BOOL" → noktalı virgül eksik: "x : BOOL;" olmalı

# ✅ Doğru
# Textual declaration'ı önceden doğrula
# Compile() ile hata var mı kontrol et
declaration = """FUNCTION_BLOCK FB_Test
VAR_INPUT
    x : BOOL;
END_VAR
"""
fb.textual_declaration.replace(declaration)
proj.compile()  # Derleme hatası kontrolü
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**Script Engine Kullan:**
- Tekrarlayan proje oluşturma (10+ benzer makine projesi)
- I/O listesinden otomatik GVL üretimi
- CI/CD pipeline içinde otomatik derleme + test
- Template projeyi müşteriye özgü parametrelerle kişiselleştirme
- Kütüphane güncelleme yönetimi (tüm projelerde versiyon güncelle)

**Script Engine Kullanma:**
- Tek seferlik küçük değişiklikler → Manuel daha hızlı
- Karmaşık device tree yapılandırması → XML kırılgan, zor test edilir
- Gerçek zamanlı runtime operasyonları → Ayrı araçlar daha uygun

## Gerçek Proje Notları

**Not 1 — 50 Makine, 50 Proje, 1 Script**  
Bir OEM, 50 farklı müşteri için aynı temel makine mimarisini kullanıyordu. Farklılıklar: motor sayısı (2-8), sensör tipi, haberleşme protokolü. JSON konfigürasyon + Script Engine ile üretim süreci saatlerden dakikalara indi. Her müşteri için `generate.py config_customer_X.json` çağrısı tam bir proje üretiyor.

**Not 2 — PLC_PRG'yi Silip Yeniden Yazmak**  
Template projede PLC_PRG standart içerikle geliyordu. Script'te `textual_implementation.replace("")` ile boşaltılıp yeniden yazıldı. Bir süre sonra fark edildi: PLC_PRG'deki bazı yorumlar şablon gereksinimler için kritikti, sıfırlanınca kayboluyordu. Çözüm: PLC_PRG şablonu ayrı .st dosyasında saklandı ve `import_native()` ile projeye çekildi.

**Not 3 — Headless Modda CODESYS Lisansı**  
Headless modda Script Engine çalıştırırken CODESYS lisansı gerekir. Demo lisansla headless mümkün değil; IDE lisansı yeterliyken bazı operasyonlar için SL lisansı gerekiyor. CI sunucusunda lisans sorunu yaşandı — lisans dosyası CI makinesine kurularak çözüldü.

**Not 4 — find() ile Arama Performansı**  
Büyük projelerde `proj.find("MyFB", recursive=True)` çağrısı yavaş olabiliyor. Alternatif: Proje hiyerarşisini önceden haritalayıp cache'le. Veya her POU oluşturulduktan sonra referansı saklayarak tekrar arama yapmaktan kaçın.

## İlgili Konular

```
knowledge/codesys/project-generation/
├── 01_project_file_structure.md → Script'in manipüle ettiği XML yapısı
├── 03_plcopen_xml.md            → import_xml() ile PLCopen kullanımı
└── 04_generation_templates.md   → Script'in uyguladığı şablon sistemi

CODESYS Scripting Kaynakları:
  CODESYS Forge Scripting    → https://forge.codesys.com/tol/scripting/
  CODESYS Scripting API Ref  → CODESYS Help → CODESYS Scripting
  GitHub tkucic automation   → https://github.com/tkucic/codesys_workflow_automation

Script Editörü (Opsiyonel):
  CODESYS Scripting AddOn    → CODESYS Store (ücretli, IDE entegrasyon)
  VS Code + IronPython ext   → Ücretsiz alternatif
```
