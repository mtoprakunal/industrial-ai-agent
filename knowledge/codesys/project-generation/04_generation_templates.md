---
KONU        : CODESYS Otomatik Proje Üretimi — Şablon Sistemi
KATEGORİ    : codesys
ALT_KATEGORI: project-generation
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/codesys/project-generation/01_project_file_structure.md"
    başlık: "CODESYS Proje Dosyası İç Yapısı"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/project-generation/02_script_engine.md"
    başlık: "CODESYS Script Engine"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/project-generation/03_plcopen_xml.md"
    başlık: "PLCopen XML Formatı"
    güvenilirlik: deneyimsel
  - url: "https://github.com/tkucic/codesys_workflow_automation"
    başlık: "GitHub — CODESYS Workflow Automation"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_project_file_structure.md"
    ilişki: gerektirir
  - konu: "02_script_engine.md"
    ilişki: gerektirir
  - konu: "03_plcopen_xml.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Script Engine (02_script_engine.md)"
  - "PLCopen XML (03_plcopen_xml.md)"
  - "CODESYS proje yapısı (fundamentals/02_project_structure.md)"
  - "Python temel bilgisi (IronPython 2.7)"
ÇELİŞKİLER :
  - kaynak: "Şablon tabanlı üretim vs model tabanlı üretim"
    konu: "Ne kadar otomatik ne kadar manuel?"
    çözüm: >
      Tam otomatik üretim (sıfırdan proje) cihaz tree'yi de içerdiğinde
      çok karmaşık hale gelir ve kırılgan olur. En sağlam yaklaşım:
      Manuel hazırlanmış template .project (device tree, library, task iskelet) +
      otomatik GVL, POU, implementasyon üretimi. Bu hibrit yaklaşım
      esneklik ve güvenilirliği dengeler.
---

## Özün Ne

Bu belge, bir proje spesifikasyonundan (JSON, Excel, veritabanı) geçerli, derlenebilir bir CODESYS projesi üretmek için agent'ın izleyeceği adım sırasını ve şablon mantığını tanımlar. Önceki üç belge araçları anlattı (XML yapısı, Script Engine, PLCopen XML); bu belge onları bir araya getirerek somut bir üretim akışı oluşturur. Amaç: Bir I/O listesi ve makine tanımı verildiğinde, sıfırdan proje oluşturabilmek.

## Nasıl Çalışır

### Üretim Mimarisi — Genel Bakış

```
GİRDİ (Proje Spesifikasyonu)
  JSON / Excel / Veritabanı
        │
        ▼
┌───────────────────────────────────────────────────────────┐
│              GENERATOR (Python — Harici)                  │
│                                                           │
│  1. Spesifikasyonu oku ve doğrula                        │
│  2. Template .project'i kopyala                          │
│  3. PLCopen XML parçaları üret (POU, DUT, GVL)          │
│  4. CODESYS Script Engine'e geç                          │
└───────────────────────┬───────────────────────────────────┘
                        │ PLCopen XML dosyaları + config.json
                        ▼
┌───────────────────────────────────────────────────────────┐
│         CODESYS SCRIPT ENGINE (IronPython)                │
│                                                           │
│  5. Template projeyi aç                                  │
│  6. PLCopen XML parçalarını import et                    │
│  7. GVL'leri doldur                                      │
│  8. Task yapılandır                                      │
│  9. Library ekle                                         │
│  10. PLC_PRG orkestrasyonu yaz                          │
│  11. Derle, hataları raporla                             │
│  12. Kaydet                                              │
└───────────────────────┬───────────────────────────────────┘
                        │
                        ▼
ÇIKTI: Derlenebilir .project dosyası
```

### Spesifikasyon Formatı — JSON Şeması

```json
{
    "project": {
        "name": "PackagingLine_Customer_XYZ",
        "version": "1.0.0",
        "author": "Acme Automation",
        "description": "3 konveyörlü paketleme hattı",
        "target_device": "CODESYS Control Linux ARM64 SL",
        "target_runtime_version": "3.5.21.0"
    },
    
    "libraries": [
        {"name": "Standard", "version": "3.5.17.0", "company": "System"},
        {"name": "Util",     "version": "3.5.17.0", "company": "System"},
        {"name": "CAA_File", "version": "3.5.17.0", "company": "CAA Technical Workgroup"}
    ],
    
    "tasks": [
        {"name": "Task_Safety",  "type": "Cyclic", "interval_ms": 5,   "priority": 0, "watchdog_ms": 25},
        {"name": "Task_Control", "type": "Cyclic", "interval_ms": 10,  "priority": 2, "watchdog_ms": 50},
        {"name": "Task_HMI",     "type": "Cyclic", "interval_ms": 100, "priority": 5, "watchdog_ms": 500},
        {"name": "Task_Background", "type": "Freewheeling", "priority": 15, "watchdog_ms": 5000}
    ],
    
    "motors": [
        {
            "name": "Conveyor1",
            "io_run_cmd":  "%Q0.0",
            "io_run_fb":   "%I0.0",
            "io_fault_fb": "%I0.1",
            "start_delay_ms": 3000,
            "task": "Task_Control"
        },
        {
            "name": "Conveyor2",
            "io_run_cmd":  "%Q0.1",
            "io_run_fb":   "%I0.2",
            "io_fault_fb": "%I0.3",
            "start_delay_ms": 2000,
            "task": "Task_Control"
        }
    ],
    
    "analog_inputs": [
        {
            "name": "Temperature_Zone1",
            "io_address": "%IW0",
            "raw_min": 0, "raw_max": 4095,
            "eng_min": 0.0, "eng_max": 100.0,
            "unit": "C",
            "alarm_high": 85.0,
            "alarm_low": 10.0
        }
    ],
    
    "communication": {
        "modbus_tcp_slave": {
            "enabled": true,
            "port": 502
        },
        "opcua_server": {
            "enabled": true,
            "port": 4840
        }
    },
    
    "recipes": {
        "enabled": true,
        "count": 5,
        "parameters": ["rSpeed_Pct", "rTemperature_Setpoint", "tDwellTime"]
    }
}
```

### Üretim Adımları — Detaylı

#### Adım 1: Spesifikasyon Doğrulama

```python
# generator.py — Harici Python 3 script (CODESYS dışında çalışır)

import json
import sys

def validate_spec(spec):
    """Spesifikasyon tutarlılık kontrolü."""
    errors = []
    
    # Zorunlu alanlar
    if not spec.get('project', {}).get('name'):
        errors.append("project.name boş")
    
    # Motor I/O adresi çakışması
    io_addresses = set()
    for motor in spec.get('motors', []):
        for addr_key in ['io_run_cmd', 'io_run_fb', 'io_fault_fb']:
            addr = motor.get(addr_key)
            if addr in io_addresses:
                errors.append("I/O adresi çakışması: {} - {}".format(motor['name'], addr))
            io_addresses.add(addr)
    
    # Task referansları
    task_names = {t['name'] for t in spec.get('tasks', [])}
    for motor in spec.get('motors', []):
        if motor.get('task') and motor['task'] not in task_names:
            errors.append("Motor {} geçersiz task: {}".format(motor['name'], motor['task']))
    
    if errors:
        for err in errors:
            print("ERROR: {}".format(err))
        sys.exit(1)
    
    print("Validation OK")
    return True
```

#### Adım 2: GVL Üretimi

```python
def generate_gvl_io_content(spec):
    """
    Spesifikasyondan GVL_IO içeriği üretir.
    Script Engine'e geçilecek string döndürür.
    """
    lines = [
        "{attribute 'qualified_only'}",
        "VAR_GLOBAL",
        "    (* ===== MOTOR I/O ===================================== *)"
    ]
    
    for motor in spec.get('motors', []):
        name = motor['name']
        lines.append("    (* {} *)".format(name))
        lines.append("    x{}_RunCmd   AT {} : BOOL;  (* Çalıştır komutu *)".format(
            name, motor['io_run_cmd']))
        lines.append("    x{}_RunFB    AT {} : BOOL;  (* Çalışma geri bildirimi *)".format(
            name, motor['io_run_fb']))
        lines.append("    x{}_FaultFB  AT {} : BOOL;  (* Arıza geri bildirimi *)".format(
            name, motor['io_fault_fb']))
        lines.append("")
    
    # Analog girişler
    if spec.get('analog_inputs'):
        lines.append("    (* ===== ANALOG GİRİŞLER ======================== *)")
        for i, ain in enumerate(spec['analog_inputs']):
            word_addr = "%IW{}".format(i * 2)
            lines.append("    w{}_Raw  AT {} : WORD;  (* {} ham ADC *)".format(
                ain['name'], word_addr, ain['unit']))
    
    lines.append("END_VAR")
    return "\n".join(lines)

def generate_gvl_params_content(spec):
    """GVL_Params içeriği — motor parametreleri."""
    lines = [
        "{attribute 'qualified_only'}",
        "VAR_GLOBAL"
    ]
    
    for motor in spec.get('motors', []):
        name = motor['name']
        delay_s = motor['start_delay_ms'] / 1000.0
        lines.append("    t{}_StartDelay : TIME := T#{:.1f}S;".format(name, delay_s))
    
    # Recipe parametreleri
    if spec.get('recipes', {}).get('enabled'):
        lines.append("")
        lines.append("    (* Reçete Parametreleri *)")
        for param in spec['recipes']['parameters']:
            lines.append("    {} : REAL := 0.0;".format(param))
    
    lines.append("END_VAR")
    return "\n".join(lines)

def generate_gvl_alarms_content(spec):
    """GVL_Alarms — motor ve sensör alarm bayrakları."""
    lines = [
        "{attribute 'qualified_only'}",
        "VAR_GLOBAL",
        "    xAnyActiveAlarm : BOOL;",
        ""
    ]
    
    for motor in spec.get('motors', []):
        lines.append("    xAlarm_{}_Fault : BOOL;".format(motor['name']))
    
    for ain in spec.get('analog_inputs', []):
        if ain.get('alarm_high'):
            lines.append("    xAlarm_{}_High  : BOOL;".format(ain['name']))
        if ain.get('alarm_low'):
            lines.append("    xAlarm_{}_Low   : BOOL;".format(ain['name']))
    
    lines.append("END_VAR")
    return "\n".join(lines)
```

#### Adım 3: POU Üretimi

```python
def generate_fb_motor_declaration(motor_name):
    """Motor FB deklarasyon bloğu üretir."""
    return """FUNCTION_BLOCK FB_{name}
VAR_INPUT
    xStartCmd   : BOOL;
    xStopCmd    : BOOL;
    xFaultReset : BOOL;
    tStartDelay : TIME := T#3S;
    xFeedback   : BOOL;
END_VAR
VAR_OUTPUT
    xRunOutput  : BOOL;
    xFault      : BOOL;
    eState      : E_MotorState;
    sFaultMsg   : STRING(80);
END_VAR
VAR
    tStartTimer : TON;
    tFaultTimer : TON;
    fbResetEdge : R_TRIG;
END_VAR""".format(name=motor_name)

def generate_fb_motor_implementation(motor_name):
    """Motor FB implementasyon bloğu üretir."""
    return """fbResetEdge(CLK := xFaultReset);

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
        
        (* Geri bildirim timeout kontrolü *)
        tFaultTimer(IN := NOT xFeedback AND xRunOutput, PT := T#3S);
        IF tFaultTimer.Q THEN
            tFaultTimer(IN := FALSE);
            xFault    := TRUE;
            sFaultMsg := '{name}: Feedback timeout';
            eState    := eFault;
        END_IF
        
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
            xFault    := FALSE;
            sFaultMsg := '';
            eState    := eIdle;
        END_IF

    ELSE:
        xRunOutput := FALSE;
        eState := eFault;
        sFaultMsg := '{name}: Unknown state';
END_CASE""".format(name=motor_name)

def generate_prg_control_content(spec):
    """PRG_ConveyorControl implementasyonu üretir."""
    motors = spec.get('motors', [])
    
    # VAR bildirimi
    var_lines = ["VAR"]
    for m in motors:
        var_lines.append("    fb{} : FB_{};".format(m['name'], m['name']))
    var_lines.append("END_VAR")
    
    # Implementasyon
    impl_lines = ["(* Motor FB Çağrıları — Auto-generated *)"]
    for m in motors:
        impl_lines.append("")
        impl_lines.append("fb{}(".format(m['name']))
        impl_lines.append("    xStartCmd   := GVL_HMI.x{}_Start,".format(m['name']))
        impl_lines.append("    xStopCmd    := GVL_HMI.x{}_Stop OR GVL_Alarms.xAnyActiveAlarm,".format(m['name']))
        impl_lines.append("    xFaultReset := GVL_HMI.x{}_FaultReset,".format(m['name']))
        impl_lines.append("    tStartDelay := GVL_Params.t{}_StartDelay,".format(m['name']))
        impl_lines.append("    xFeedback   := GVL_IO.x{}_RunFB".format(m['name']))
        impl_lines.append(");")
        impl_lines.append("GVL_IO.x{}_RunCmd      := fb{}.xRunOutput;".format(m['name'], m['name']))
        impl_lines.append("GVL_Alarms.xAlarm_{}_Fault := fb{}.xFault;".format(m['name'], m['name']))
    
    impl_lines.append("")
    impl_lines.append("(* Alarm özeti *)")
    alarm_conditions = ["GVL_Alarms.xAlarm_{}_Fault".format(m['name']) for m in motors]
    impl_lines.append("GVL_Alarms.xAnyActiveAlarm := {};".format(
        "\n    OR ".join(alarm_conditions) if alarm_conditions else "FALSE"))
    
    declaration = "PROGRAM PRG_ConveyorControl\n" + "\n".join(var_lines)
    implementation = "\n".join(impl_lines)
    return declaration, implementation
```

#### Adım 4: Script Engine Entegrasyonu

```python
# codesys_generator_script.py — Script Engine içinde çalışır (IronPython 2.7)
# encoding: utf-8
from __future__ import print_function
import json
import os
import sys

# Konfigürasyonu oku
config_path = sys.argv[1] if len(sys.argv) > 1 else r"C:\AutoGen\config.json"
with open(config_path, 'r') as f:
    spec = json.load(f)

template_path = r"C:\Templates\BaseProject.project"
output_path = r"C:\Projects\{}.project".format(spec['project']['name'])

# Template'i aç
import shutil
shutil.copy(template_path, output_path)
proj = projects.open(output_path)

app_results = proj.find("Application", recursive=True)
if not app_results:
    raise Exception("Application not found!")
app = app_results[0]

# --- GVL'LERİ DOLDUR ---
def update_or_create_gvl(app, gvl_name, content):
    found = app.find(gvl_name, recursive=False)
    if found:
        gvl = found[0]
    else:
        gvl = app.create_gvl(gvl_name)
    gvl.textual_declaration.replace(content)
    print("GVL updated: {}".format(gvl_name))

# GVL içeriklerini spec'ten üret
# (generate_gvl_io_content vb. PLCopen XML veya string olarak geliyor)
gvl_io_content = spec.get('_generated', {}).get('gvl_io', '')
if gvl_io_content:
    update_or_create_gvl(app, "GVL_IO", gvl_io_content)

gvl_params_content = spec.get('_generated', {}).get('gvl_params', '')
if gvl_params_content:
    update_or_create_gvl(app, "GVL_Params", gvl_params_content)

gvl_alarms_content = spec.get('_generated', {}).get('gvl_alarms', '')
if gvl_alarms_content:
    update_or_create_gvl(app, "GVL_Alarms", gvl_alarms_content)

# --- POU'LARI IMPORT ET (PLCopen XML'den) ---
pou_xml_dir = spec.get('_generated', {}).get('pou_xml_dir', '')
if pou_xml_dir and os.path.exists(pou_xml_dir):
    for xml_file in os.listdir(pou_xml_dir):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(pou_xml_dir, xml_file)
            app.import_xml(xml_path)
            print("Imported: {}".format(xml_file))

# --- PRG_CONTROL'Ü GÜNCELLE ---
prg_results = app.find("PRG_ConveyorControl", recursive=True)
if prg_results:
    prg = prg_results[0]
    prg_decl = spec.get('_generated', {}).get('prg_declaration', '')
    prg_impl = spec.get('_generated', {}).get('prg_implementation', '')
    if prg_decl:
        prg.textual_declaration.replace(prg_decl)
    if prg_impl:
        prg.textual_implementation.replace(prg_impl)
    print("PRG_ConveyorControl updated")

# --- LIBRARY EKLE ---
lib_mgr_results = app.find("Library Manager", recursive=True)
if lib_mgr_results:
    lib_mgr = lib_mgr_results[0]
    for lib in spec.get('libraries', []):
        lib_mgr.add_library(lib['name'], lib['version'], lib['company'])
        print("Library added: {} {}".format(lib['name'], lib['version']))

# --- KAYDET VE DERLE ---
projects.save()
print("Project saved: {}".format(output_path))

result = proj.compile()
if result:
    print("COMPILATION SUCCESS: {}".format(spec['project']['name']))
else:
    print("COMPILATION FAILED — check errors!")

projects.close()
```

### Tam Üretim Akışı

```
generate.py (Python 3, harici)        generate_script.py (IronPython, CODESYS)
─────────────────────────────────────────────────────────────────────────────
1. spec.json oku
2. validate_spec(spec)
3. generate_gvl_io_content(spec)
4. generate_gvl_params_content(spec)
5. generate_gvl_alarms_content(spec)
6. generate_fb_motor_declaration(...)    →  PLCopen XML yaz
7. generate_fb_motor_implementation(...) →  PLCopen XML yaz
8. generate_prg_control_content(spec)
9. Üretilenleri spec['_generated']'a ekle
10. config_with_generated.json yaz
11. CODESYS'i headless başlat              12. config_with_generated.json oku
                                           13. Template .project aç
                                           14. GVL'leri doldur
                                           15. PLCopen XML'leri import et
                                           16. PRG güncelle
                                           17. Library ekle
                                           18. Derle + kaydet
```

## Örnekler

### Örnek 1: Tam Çalışan Üretim Çağrısı

```bash
# 1. Spesifikasyonu hazırla
cat spec.json

# 2. Harici generator çalıştır (Python 3)
python3 generate.py spec.json --output-dir /tmp/gen

# 3. CODESYS headless olarak projeyi oluştur
CODESYS.exe \
    --profile="CODESYS V3.5 SP21" \
    --noUI \
    --runscript="/tmp/gen/codesys_script.py" \
    --scriptargs="/tmp/gen/spec_with_generated.json"

# 4. Sonuç
ls /output/projects/PackagingLine_Customer_XYZ.project
```

### Örnek 2: I/O Listesinden GVL Üretimi

I/O listesi Excel'den geliyorsa:

```python
# io_list.xlsx → spec.json dönüşümü (Python 3, harici)
import openpyxl
import json

wb = openpyxl.load_workbook('io_list.xlsx')
ws = wb['IO_Map']

motors = []
analog_inputs = []

for row in ws.iter_rows(min_row=2, values_only=True):
    io_type, name, address, description = row[:4]
    
    if io_type == 'MOTOR':
        # Motor satırları: name=Conveyor1, address_block başlar
        motors.append({
            'name': name,
            'io_run_cmd': address,
            'io_run_fb': next_addr(address, 8),   # Örnek offset
            'io_fault_fb': next_addr(address, 9),
            'start_delay_ms': 3000,
            'task': 'Task_Control'
        })

spec = {
    'project': {'name': 'GeneratedProject'},
    'motors': motors,
    'analog_inputs': analog_inputs
}

with open('spec.json', 'w') as f:
    json.dump(spec, f, indent=2)
```

### Örnek 3: Agent İçin Üretim Kararları

Bir agent CODESYS projesi üretirken şu karar ağacını izlemeli:

```
Adım 1: Spesifikasyon Analizi
│
├─► Motor sayısı > 0?
│   ├── Evet → FB_Motor üret (her motor için), GVL_IO motor alanları ekle
│   └── Hayır → Motor bölümü atla
│
├─► Analog giriş sayısı > 0?
│   ├── Evet → FB_AnalogSensor üret (her sensör için), GVL_IO analog alanları ekle
│   └── Hayır → Analog bölümü atla
│
├─► Recipe enabled?
│   ├── Evet → GVL_Recipes (RETAIN), FB_RecipeManager üret
│   └── Hayır → Atla
│
├─► Modbus TCP slave enabled?
│   ├── Evet → GVL_Modbus üret, PRG_ModbusUpdate üret, Task_Slow'a ekle
│   └── Hayır → Atla
│
└─► OPC UA enabled?
    ├── Evet → Symbol Configuration oluştur, değişkenleri işaretle
    └── Hayır → Atla

Adım 2: Task Atama Kuralları
  Safety mantığı       → Task_Safety (en yüksek Prio)
  Motor/PID/kontrol    → Task_Control
  HMI/OPC UA          → Task_HMI
  Modbus/log          → Task_Background
  
Adım 3: Derleme Kontrolü
  IF compile() == FAIL:
    Hata mesajlarını yakala
    Yanlış üretilen bölümü bul
    Düzelt ve tekrar dene
```

## Sık Yapılan Hatalar

### Hata 1: Template Projede Device Tree Olmadan Başlamak

```
Senaryo: Script sıfırdan proje oluşturmaya çalışıyor.
         Device tree yoksa Application nesnesi yok.
         Application yoksa hiçbir şey eklenemiyor.

Çözüm  : Template .project her zaman şunları içermelidir:
          - Device (hedef platforma uygun)
          - PLC Logic node
          - Application (Library Manager + Task Configuration dahil)
          - Boş GVL'ler (isimler sabit, içerik üretilecek)
          
Template ne kadar hazırsa, script o kadar basit olur.
```

### Hata 2: I/O Adres Çakışması Kontrolü Atlamak

```python
# Üretim öncesi mutlaka kontrol:
io_addresses = set()
for motor in motors:
    for addr in [motor['io_run_cmd'], motor['io_run_fb'], motor['io_fault_fb']]:
        if addr and addr in io_addresses:
            raise ValueError("Duplicate I/O address: {} in {}".format(addr, motor['name']))
        if addr:
            io_addresses.add(addr)
```

### Hata 3: Derleme Hatası Sessizce Geçmek

```python
# ❌ Yanlış — Hata sessizce geçiyor
proj.compile()

# ✅ Doğru — Hata raporla
result = proj.compile()
if not result:
    print("COMPILATION FAILED!")
    # Hata listesini al (API'ye bağlı)
    # Başarısız projeyi kaydetme
    raise Exception("Generated project does not compile!")
```

### Hata 4: Üretilen Kodu Test Etmemek

```
Üretilen proje derleniyor ≠ Doğru çalışıyor.

Minimum test:
  1. Tüm POU'lar compile edilebiliyor mu?
  2. Task'a atanan tüm programlar var mı?
  3. GVL'de kullanılan tüm tipler tanımlı mı?
  4. Kütüphane referansları çözümlenebiliyor mu?
  
İdeal: Simülasyon modunda çalıştırıp temel I/O test edin.
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Otomatik Üretim Hangi Durumda Değerli?

**Güçlü tercih:**
- 5+ aynı kategoride farklı parametreli proje (OEM senaryosu)
- I/O listesi değişince projenin de değişmesi gerekiyor
- Farklı müşteri konfigürasyonları (motor sayısı, sensör tipi)
- CI/CD pipeline içinde otomatik doğrulama

**Zayıf tercih / manuel daha iyi:**
- Tek proje, tek müşteri, nadir değişiklik
- Karmaşık kontrol mantığı (PID tuning, motion path) — şablon yazılamaz
- Güvenlik (SIL) projeleri — otomatik üretim doğrulama zorlaştırır

### Hibrit Yaklaşım (Önerilen)

```
Otomatik üret:              Manuel yaz:
─────────────────           ─────────────────
GVL içerikleri              Device tree
Standart FB'ler             EtherCAT konfigürasyonu
I/O adres atamaları         Motion path parametreleri
Task atama listesi          PID tuning değerleri
PRG orkestrasyonu           Güvenlik mantığı detayı
Library listesi             Müşteriye özgü iş mantığı
```

## Gerçek Proje Notları

**Not 1 — İlk Üretimde 40 Hata**  
İlk otomatik üretim denemesinde 40 derleme hatası çıktı. Hepsi benzer: "E_MotorState tipi bulunamadı." DUT'ları POU'lardan önce üretmek gerekiyordu — bağımlılık sırası kritik. POU sırasını şöyle düzeltildi: DUT → GVL → FB → PROGRAM.

**Not 2 — Template'de Sabit Kalan Şeyler**  
Template'de sabit tutulan şey: Task yapısı, library isimleri, boş GVL isimleri. Değişen şey: İçerikler. Bu ayrım, template'i kırılgan olmaktan çıkardı. Template değişince tüm üretimler etkileniyor — iyisi: tek noktadan güncelleme.

**Not 3 — Agent Üretiminde Doğrulama Döngüsü**  
Agent bir proje ürettiğinde ve derleme başarısız olduğunda: hata mesajını oku → hangi POU/GVL'de sorun var anla → o bölümü yeniden üret → tekrar derle. Bu döngü, üretim kalitesini kademeli olarak artırır. Ortalama 2-3 iterasyonda başarılı derleme.

**Not 4 — Spesifikasyon Versiyonlama**  
Her üretilen proje, üretimde kullanılan spec.json'ı da içermeli. Bir yıl sonra "bu proje nasıl üretildi?" sorusunun cevabı o dosyada. spec.json'ı .project ile birlikte version control'e al.

**Not 5 — "Derlendi" ≠ "Doğru Çalışıyor"**  
Bir üretilen proje sıfır hatayla derlendi, müşteriye gönderildi; sahada motor geri bildirimi hiç işlenmiyordu. Neden: GVL_IO'da `xConveyor1_RunFB` üretilmişti ama PRG'de FB'ye `xFeedback := GVL_IO.xConveyor1_RunFB` bağlanmamıştı (template orkestrasyon şablonunda eksik). Derleme bunu yakalamaz — sözdizimi doğru, mantık eksik. Ders: üretim doğrulaması derlemede bitmez; simülasyonda temel I/O akışı + "her FB girişi bağlı mı?" statik kontrolü gerekir. Üretilen kodun **anlamsal** doğruluğu ayrı bir test katmanıdır.

**Not 6 — Template Sürüm Sürüklenmesi (Drift)**  
Üç ayrı OEM ekibi aynı template'ten başladı ama her biri kendi kopyasını ufak ufak değiştirdi; bir yıl sonra dört farklı "BaseProject.project" vardı, hangisinin doğru olduğu bilinmiyordu (programming/03'teki "20 farklı FB_Motor" probleminin template versiyonu). Ders: template'i tek bir version-controlled kaynaktan yönet; üretim aracı template'i sabit bir sürümle referanslasın. Template = kütüphane gibi sürüm-kilitli olmalı.

**Not 7 — Idempotent Olmayan Üretimin Kirli Çıktısı**  
Bir üretim scripti hata sonrası yeniden çalıştırıldı; "obje zaten var" hataları + yarım GVL'ler birikti, çıktı kullanılamaz hale geldi (02 Not 6'nın üretim-akışı versiyonu). Ders: üretim her zaman temiz template kopyasından başlamalı (shutil.copy) VEYA tam idempotent olmalı (get-or-create + replace). "Mevcut projenin üzerine ekle" deseni kirli durumlar biriktirir; her üretim turu deterministik ve tekrarlanabilir olmalı.

## Edge Case'ler ve Üretim Sınırları

### Bağımlılık Sırası ve Çözümleme

```
Sıra ihlali                       Sonuç                     Doğru sıra
─────────────────────────────────────────────────────────────────────
FB önce, DUT sonra import          "tip bulunamadı" (40 hata) DUT → GVL → FB → PROGRAM
Library eklenmeden FB import        TON/R_TRIG çözülemez      önce Standard/Util ekle
GVL eklenmeden PRG import           "GVL_IO bulunamadı"        GVL'ler önce
PRG, var olmayan FB'yi çağırır      compile hatası            FB'ler PRG'den önce
Symbol Config OPC UA için manuel    OPC UA değişken yok        script + manuel adım
```

### Anlamsal (Semantic) Hatalar — Derlemenin Yakalamadıkları

```
- Bağlanmamış FB girişi (xFeedback boş) → derlenir, çalışmaz (Not 5)
- Yanlış I/O adresi (doğru sözdizimi, yanlış kanal) → derlenir, yanlış davranır
- Eksik alarm özeti (xAnyActiveAlarm hep FALSE) → derlenir, güvenlik açığı
- Task'a atanmamış PROGRAM → derlenir, hiç çalışmaz (fundamentals/02)
- Yanlış ölçek (×10 unutuldu) → derlenir, değer 10× hatalı
```

Bu hatalar üretim şablonunun **mantık** doğruluğuna bağlıdır; derleme yalnızca sözdizimini doğrular. Üretim aracının kendi semantic-check katmanı olmalı.

### Hibrit Sınırı: Neyi Üretemezsin

```
Üretilemez (template'te elle / Script Engine ile manuel):
  Device tree + typeGuid (platform-bağlı, 01)
  EtherCAT slave PDO mapping + CoE startup
  Motion path / cam tabloları
  PID tuning değerleri (saha ayarı)
  Güvenlik (SIL) mantığı (doğrulama gerektirir)
  Symbol Configuration (kısmen manuel)
```

## Optimizasyon

### Template'i İnce Tut, İçeriği Üret

```
Template'te SABİT (elle, sürüm-kilitli):
  device tree · library listesi · task iskeleti · boş GVL isimleri · boş PLC_PRG

Script'in ÜRETTİĞİ:
  GVL içerikleri · FB'ler · DUT'lar · PRG orkestrasyonu · I/O adresleri · alarm özeti
```

Template ne kadar hazırsa script o kadar basit ve sağlam (Not 2). Ama template ne kadar çok içerirse drift riski o kadar artar (Not 6) — denge: mimari sabit, içerik üretilen.

### Üretim Sırası ve Tek-Geçiş

```
1. Template kopyala (temiz başlangıç, idempotency)
2. DUT'lar (ENUM/STRUCT) — bağımlılık kökü
3. Library'ler — FB'lerin ihtiyacı
4. GVL'ler — POU'ların eriştiği
5. FB'ler (import_xml veya create+replace)
6. PROGRAM orkestrasyonu
7. Task atamaları
8. compile() → False ise dur, raporla (sakla-ma)
```

Bu sıra "40 hata" dersinin (Not 1) sistematik halidir; her adım bir öncekinin ürettiğine dayanır.

### Doğrulama Katmanları

```
1. Spec doğrulama (üretimden ÖNCE): I/O çakışması, task referansı, zorunlu alan
2. Compile (üretimden SONRA): sözdizimi
3. Semantic check: her FB girişi bağlı mı, her PROGRAM task'ta mı, alarm özeti dolu mu
4. Simülasyon (ideal): temel I/O akışı çalışıyor mu
```

Tek başına compile yetmez (Not 5); dört katman birlikte üretim güvenilirliğini sağlar.

## Derin Teknik Detay

### Neden Hibrit? — Üretilebilirlik Sınırının Konumu

Tam-otomatik üretim (device tree dahil sıfırdan) neden kırılgan? Çünkü üretilebilirlik, **bilginin kaynağına** bağlıdır:
- **Spec'ten türetilebilen** (motor sayısı→FB, I/O listesi→GVL) → otomatik üret.
- **Platforma/repository'ye bağlı** (typeGuid, device tree, EtherCAT ESI) → çalışma anında çözülür, spec'te yok → template'te elle.
- **Mühendislik kararı gerektiren** (PID tuning, motion path, SIL mantığı) → insan bilgisi, üretilemez.

Hibrit yaklaşım bu üç kategoriyi ayırır: otomatik olanı script üretir, platform-bağlıyı template taşır, mühendislik-kararını insan yazar. "Ne kadar otomatik?" sorusunun cevabı "spec'ten deterministik türetilebilen kadar"dır. Bu sınır, project-generation'ın temel mühendislik kararıdır.

### Spec → Proje: Model-Tabanlı Üretimin PLC Karşılığı

Bu akış (JSON spec → kod) aslında yazılım dünyasındaki **model-driven development**'in (MDD) PLC uygulamasıdır: yüksek-seviye model (spec) → kod üreteci → çalıştırılabilir artefakt. Avantajı: tek model değişikliği (motor ekle) tutarlı şekilde tüm projeye yansır (GVL+FB+PRG+alarm) — elle yapılsa 5 yerde değişiklik, biri unutulur. Bu, programming/01'deki "FB ile kopyalama yok" prensibinin bir üst katmanı: FB tekil mantığı, üreteç tekil mimariyi yeniden kullanılabilir kılar. OEM senaryosunda (50 makine, 1 script) değer buradan gelir.

### Derleme: Sözdizimi Doğrular, Mantık Doğrulamaz

`proj.compile()` bir IEC derleyicisidir — sözdizimi ve tip uyumunu kontrol eder, davranışı değil (Not 5). Bu, tüm derleyicilerin doğasıdır: "x : BOOL := 5" tip hatası verir (yakalanır), ama "yanlış FB girişine bağlama" sözdizimsel olarak geçerlidir (yakalanmaz). Üretilen kodda anlamsal hatalar (eksik bağlantı, yanlış adres, eksik alarm) ancak semantic-check (statik analiz: "her output bağlandı mı?") veya simülasyon ile yakalanır. Bu yüzden üretim doğrulaması derlemede bitmez; CODESYS Static Analysis (fundamentals/01) veya özel kontrol katmanı, üretilen kodun mantık bütünlüğünü doğrular. "Derlendi = teslim edilebilir" en pahalı üretim yanılgısıdır.

### Idempotency: Üretim Güvenilirliğinin Temeli

Üretim akışının idempotent olması (aynı spec → aynı sonuç, kaç kez çalışırsa) iki şeyi sağlar: kısmi-hata sonrası güvenli yeniden-çalıştırma (02 Not 6) ve deterministik çıktı (Not 7). İki strateji: (1) her turda temiz template kopyasından başla — basit, garantili; (2) get-or-create + replace ile mevcut üzerine yaz — karmaşık ama hızlı. Üretim araçları (1)'i tercih etmeli: temiz başlangıç, yarım-durum birikimini imkânsız kılar. Bu, fonksiyonel programlamadaki "saf fonksiyon" (aynı girdi→aynı çıktı, yan etki yok) prensibinin üretim-akışına uygulanışıdır — ve programming/01'deki Function'ın saflık garantisiyle aynı felsefe.

## İlgili Konular

```
knowledge/codesys/project-generation/
├── 01_project_file_structure.md → Üretilen projenin iç yapısı
├── 02_script_engine.md          → Script Engine API referansı
└── 03_plcopen_xml.md            → POU'ları PLCopen XML ile taşıma

knowledge/codesys/programming/
├── 01_pou_types.md              → Üretilecek POU tipleri
├── 02_gvl_design.md             → GVL organizasyon şeması
└── 03_function_blocks.md        → Şablonlanacak FB içerikleri

knowledge/codesys/task-structure/
└── _synthesis.md                → Task yapısı tasarım kuralları
```
