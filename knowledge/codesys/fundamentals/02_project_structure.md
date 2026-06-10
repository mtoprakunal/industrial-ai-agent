---
KONU        : CODESYS Proje İç Yapısı
KATEGORİ    : codesys
ALT_KATEGORI: fundamentals
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_struct_project_creation.html"
    başlık: "CODESYS Online Help — Creating and Configuring a Project"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_f_task_configuration.html"
    başlık: "CODESYS Online Help — Task Configuration"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_struct_installing_libraries.html"
    başlık: "CODESYS Online Help — Library Manager"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_mapping_hardware_in_device_tree.html"
    başlık: "CODESYS Online Help — Mapping Hardware in Device Tree"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_runtime_architecture.md"
    ilişki: gerektirir
  - konu: "03_iec61131_languages.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/task-structure/01_task_types.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/libraries/01_standard_libraries.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "CODESYS runtime kavramı (01_runtime_architecture.md)"
  - "IEC 61131-3 POU kavramı (Program, Function Block, Function)"
  - "CODESYS Development System kurulumu"
ÇELİŞKİLER :
  - kaynak: "Farklı CODESYS versiyonları (V2 vs V3)"
    konu: "Proje yapısı V2 ile V3 arasında köklü biçimde farklıdır"
    çözüm: >
      Bu belge yalnızca CODESYS V3.x'i kapsar. V2 projelerinde Device tree yoktur,
      her şey tek bir Global Variable ve tek bir Task üzerinde düzenlenir.
      V2'den V3'e migration otomatik değildir; manuel dönüştürme gerektirir.
  - kaynak: "Üçüncü taraf CODESYS türevleri"
    konu: "WAGO e!COCKPIT, Beckhoff TwinCAT, Schneider Machine Expert farklı isimler kullanır"
    çözüm: >
      Kavramlar aynı olsa da menü yerleri ve isimlendirmeler farklı olabilir.
      Örneğin TwinCAT'te 'Application' yerine 'PLC Project', 'Device' yerine
      'Runtime' denir. Kavramsal yapı aynıdır.
---

## Özün Ne

CODESYS'te bir proje açtığınızda sol tarafta gördüğünüz panel —genellikle **Device Tree** (Devices görünümü) olarak adlandırılır— o projenin tüm anatomisini hiyerarşik biçimde gösterir. Her satır, her düğüm, bir amaca hizmet eder: biri donanım konfigürasyonunu, biri değişkenleri, biri çalışma zamanlamasını, biri kütüphaneleri yönetir. Bu hiyerarşiyi anlamadan CODESYS'te anlamlı bir iş yapmak mümkün değildir; neyi nereye yazacağınızı bilemezsiniz. Bu belge, o sol panelin tam anatomisini açıklar.

## Nasıl Çalışır

### Proje Dosyası

CODESYS projesi tek bir **`.project`** dosyasıdır (XML tabanlı). İçinde şunlar gömülü durumdadır: kaynak kodlar, konfigürasyon, kütüphane referansları, I/O eşleştirmeleri. Projeyi bir başkasıyla paylaşmak için ya bu dosyayı ya da daha taşınabilir olan **`.projectarchive`** formatını (bağımlı kütüphaneleri de içerir) kullanmak gerekir.

### Hiyerarşik Yapı (Tam Şema)

```
[Proje Dosyası] → MyMachine.project
│
├── POUs (Proje geneli paylaşılan POU'lar)
│   └── [Projeye özel global programlar — genellikle boş bırakılır]
│
└── Devices (Device Tree — sol panel)
    │
    └── [ROOT] MyDevice (Device Object)
        │   ← Hedef donanımı temsil eder
        │   ← Device Description (.devdesc) ile tanımlı
        │
        ├── PLC Logic
        │   │
        │   └── Application (Ana Uygulama)
        │       │   ← Çalışacak IEC uygulamasının kapsayıcısı
        │       │   ← Birden fazla Application eklenebilir (V3 özelliği)
        │       │
        │       ├── Library Manager
        │       │   └── Standard.library, Util.library, ...
        │       │
        │       ├── Task Configuration
        │       │   └── MainTask (Cyclic, 10ms, Prio:1)
        │       │       └── PLC_PRG (çağrılan programlar)
        │       │
        │       ├── PLC_PRG (varsayılan PROGRAM POU)
        │       │
        │       ├── GVL (Global Variable List)
        │       │   └── GVL_IO, GVL_Params, GVL_Alarms...
        │       │
        │       ├── DUT (Data Unit Types)
        │       │   └── STRUCT, ENUM, ALIAS tanımları
        │       │
        │       └── Visualizations (WebVisu / TargetVisu)
        │
        ├── [Fieldbus Cihazları]
        │   ├── EtherCAT_Master
        │   │   └── Drive_1 (Slave)
        │   │       └── I/O Mapping (Device inputs → GVL)
        │   │
        │   └── Modbus_TCP_Slave_1
        │
        └── [Diğer alt cihazlar]
```

### Device Objesi

Device, runtime'ın çalışacağı fiziksel veya sanal donanımı tanımlar. CODESYS'in **Device Repository**'sinden seçilen bir `.devdesc` (Device Description) dosyasıyla tanımlanır. Bu dosya:
- Desteklenen fieldbus arayüzleri
- CPU mimarisi
- Desteklenen CODESYS versiyonu
- I/O kapasitesi

bilgilerini içerir. 500'den fazla üreticinin cihaz tanımları CODESYS Device Directory'de mevcuttur.

**Communication Settings** bu objeye çift tıklanarak açılır ve runtime bağlantısı (IP adresi, port) buradan yapılandırılır.

### Application Objesi

Application, bir veya daha fazla task'ın çalıştırdığı IEC programlarının tüm koleksiyonudur. CODESYS V3'ün güçlü özelliği: tek bir Device üzerinde **birden fazla Application** çalışabilir. Her Application kendi:
- Library Manager'ına
- Task Configuration'ına
- GVL'lerine
- POU setine

sahiptir. Uygulamalar birbirinden bağımsız olarak start/stop/download edilebilir.

```
Device
├── Application_Production  ← Üretim kodu (stabil, değiştirilmez)
└── Application_Diagnostics ← Diagnostik araçlar (geliştirme devam ediyor)
```

### Library Manager

Kütüphaneler, tekrar kullanılabilir POU koleksiyonlarıdır. Library Manager bu kütüphaneleri projeye ekler ve yönetir. Yerleşim:

- **Application altındaki Library Manager**: O uygulamaya özgü kütüphaneler.
- **POUs view altındaki Library Manager**: Tüm uygulamalara ortak kütüphaneler.

```
Dahili kütüphane (*.library)      → Kaynak kod görünür, açık
Derlenmiş kütüphane (*.compiled-library-v3) → Kaynak kod gizli, IP korumalı
```

Versiyon yönetimi kritiktir: Kütüphane güncellemesi her projede otomatik olmaz; her proje hangi versiyonu kullandığını açıkça belirtir.

### Task Configuration

Bir task, IEC programlarının çalışma zamanlamasını belirleyen kronoloejk akış birimidir. Task Configuration objesi, bu task'ların listesini ve parametrelerini tutar.

**Task Türleri:**

| Tür | Açıklama | Kullanım |
|---|---|---|
| **Cyclic** | Sabit zaman aralığıyla çalışır | Ana kontrol döngüsü |
| **Freewheeling** | Mümkün olan en hızlı döngü, cycle time yok | Düşük öncelikli arka plan işleri |
| **Event (Internal)** | Bir değişkenin rising edge'iyle tetiklenir | Kesme benzeri davranış |
| **Event (External)** | Donanım interrupt'ıyla tetiklenir | Encoder, yüksek hız sayaç |
| **Status** | Koşul TRUE olduğu sürece çalışır | Belirli duruma bağlı işlem |

**Task Parametreleri:**
```
Priority : 0-31 (0 = en yüksek, 31 = en düşük)
Interval : t#10ms (Cyclic için)
Watchdog : Enabled, Time: t#50ms, Sensitivity: 3
```

### POU (Program Organization Unit)

POU, IEC 61131-3'ün temel kod birimidir. 3 türü vardır:

```
PROGRAM  → Durumlu, tekil instance, task tarafından doğrudan çağrılır
            Örnek: PLC_PRG, SafetyLogic, ProductionManager

FUNCTION_BLOCK → Durumlu, çok instance'lı, başka POU'lardan örneklenir
            Örnek: FB_Motor, FB_PIDController, FB_ConveyorBelt

FUNCTION → Durumsuz, giriş → çıkış, yan etkisiz olmalı
            Örnek: FC_ScaleValue, FC_ByteToWord, FC_IsInRange
```

Her POU şunları içerir:
- **VAR bölgesi**: Yerel değişkenler (sadece o POU içinde geçerli)
- **VAR_INPUT / VAR_OUTPUT / VAR_IN_OUT**: Arayüz değişkenleri
- **Implementation bölgesi**: ST, LD, FBD, SFC, IL kodu

### GVL (Global Variable List)

GVL, tüm application içinden erişilebilen değişkenlerin tanımlandığı yerdir. İsimlendirme kuralı proje genelinde tutarlı olmalıdır.

```iecst
VAR_GLOBAL
    (* I/O Değişkenleri *)
    xConveyorRunFeedback   : BOOL;     (* Konveyör çalışma geri bildirimi *)
    xEmergencyStop         : BOOL;     (* Acil stop butonu *)
    rTemperatureSensor1    : REAL;     (* °C cinsinden sıcaklık *)
    
    (* Proses Parametreleri *)
    rTargetSpeed           : REAL := 50.0;  (* m/dk — varsayılan 50 *)
    tStartupDelay          : TIME := T#3S;
    
    (* Alarm Bayrakları *)
    xOverTempAlarm         : BOOL;
    xMotorFaultAlarm       : BOOL;
    
    (* Sayaçlar ve İstatistikler *)
    dwProductionCount      : DWORD;
    dwRejectedCount        : DWORD;
END_VAR
```

**GVL Erişimi**: Başka bir POU'dan `GVL_IO.xConveyorRunFeedback` şeklinde erişilir.

### DUT (Data Unit Type)

DUT, STRUCT, ENUM ve ALIAS tanımlarını barındırır:

```iecst
(* STRUCT örneği *)
TYPE ST_MotorData :
STRUCT
    xRunCommand    : BOOL;
    xRunFeedback   : BOOL;
    rCurrentSpeed  : REAL;
    rSetpoint      : REAL;
    eState         : E_MotorState;
    tRunningTime   : TIME;
END_STRUCT
END_TYPE

(* ENUM örneği *)
TYPE E_MotorState :
(
    eIdle      := 0,
    eStarting  := 1,
    eRunning   := 2,
    eStopping  := 3,
    eFault     := 4
);
END_TYPE
```

### I/O Mapping

I/O Mapping, fiziksel giriş/çıkış sinyallerini GVL değişkenleriyle bağlar. Fieldbus cihazının altında bulunur:

```
EtherCAT_Master → Drive_1 → I/O Mapping:
  %I 0.0 (Digital Input 1)    → GVL_IO.xConveyorRunFeedback
  %Q 0.0 (Digital Output 1)   → GVL_IO.xConveyorStart
  %IW 0  (Analog Input Word)  → GVL_IO.wSpeedFeedback
```

`%I`, `%Q`, `%M` notasyonu IEC 61131-3 standardından gelir:
- `%I` = Input (fiziksel giriş)
- `%Q` = Output (fiziksel çıkış)
- `%M` = Memory (iç bit)
- `%IW`, `%QW` = Word boyutlu giriş/çıkış

## Pratikte Nasıl Kullanılır

### Standart Proje Başlatma Adımları

**Adım 1: Yeni Proje Oluşturma**
```
File → New Project → Standard Project
    Device: CODESYS Control Win V3   (test için)
    PLC:    3S - Smart Software Solutions
    Programming language: Structured Text (ST)
```

Bu işlem otomatik olarak şunları oluşturur: Device, Application, Library Manager (Standard.library dahil), Task Configuration (MainTask), PLC_PRG.

**Adım 2: GVL Ekleme**
```
Application (sağ tık) → Add Object → Global Variable List
    İsim: GVL_IO   (I/O değişkenleri için)
    İsim: GVL_Params  (proses parametreleri için)
    İsim: GVL_Alarms  (alarm bayrakları için)
```

**Adım 3: DUT Ekleme**
```
Application (sağ tık) → Add Object → DUT
    İsim: ST_MotorData
    Tür: STRUCT
```

**Adım 4: Function Block Ekleme**
```
Application (sağ tık) → Add Object → POU
    İsim: FB_Motor
    Tür: Function Block
    Dil: Structured Text
```

**Adım 5: Task'a Program Atama**
```
Task Configuration → MainTask (çift tık) →
    Configuration Tab → Add Call →
    Program: FB_Motor_Instance (veya PLC_PRG)
```

**Adım 6: Library Ekleme**
```
Library Manager (çift tık) → Add Library (ikon) →
    Arama: "Util" → Util.library (3S – Smart Software Solutions) → OK
```

### Proje İsimlendirme Kuralları (Önerilen)

```
Önek  | Tür          | Örnek
------|--------------|----------------------------
x     | BOOL         | xMotorRunFeedback
r     | REAL         | rSetpointTemperature
n     | INT/UINT     | nProductCount
w     | WORD         | wAnalogInputRaw
dw    | DWORD        | dwSerialNumber
s     | STRING       | sRecipeName
t     | TIME         | tStartupDelay
dt    | DATE_AND_TIME| dtLastMaintenanceDate
a     | ARRAY        | aTemperatureHistory
st    | STRUCT       | stMotorData
e     | ENUM         | eSystemState
fb    | FUNCTION_BLOCK instance | fbPID_Temp
```

## Örnekler

### Örnek 1: Tam Bir Küçük Proje Yapısı

```
MyConveyorProject.project
│
└── Device (WAGO PFC200)
    └── PLC Logic
        └── Application
            ├── Library Manager
            │   ├── Standard.library           (temel tipler, bloklar)
            │   ├── Util.library               (FIFO, ring buffer)
            │   └── CAA_File.library           (dosya işlemleri)
            │
            ├── Task Configuration
            │   ├── Task_Safety    (Prio:0, Cyclic, 5ms)
            │   │   └── PRG_Safety
            │   ├── Task_Main      (Prio:1, Cyclic, 20ms)
            │   │   ├── PRG_ConveyorControl
            │   │   └── PRG_TemperatureControl
            │   └── Task_Comm      (Prio:10, Freewheel)
            │       └── PRG_OPCUAUpdate
            │
            ├── PRG_Safety         (PROGRAM, ST)
            ├── PRG_ConveyorControl(PROGRAM, ST)
            ├── PRG_TemperatureControl (PROGRAM, ST)
            ├── PRG_OPCUAUpdate    (PROGRAM, ST)
            │
            ├── FB_Motor           (FUNCTION_BLOCK, ST)
            ├── FB_PIDTemperature  (FUNCTION_BLOCK, ST)
            ├── FC_ScaleAnalog     (FUNCTION, ST)
            │
            ├── GVL_IO             (Global Variable List)
            ├── GVL_Params         (Global Variable List)
            ├── GVL_Alarms         (Global Variable List)
            │
            ├── DUT_MotorData      (STRUCT)
            ├── DUT_SystemState    (ENUM)
            │
            └── Visualization
                └── WebVisu_Main   (Web tabanlı HMI)
```

### Örnek 2: FB_Motor Basit Implementasyonu

```iecst
FUNCTION_BLOCK FB_Motor
VAR_INPUT
    xStartCommand  : BOOL;    (* Çalıştır komutu *)
    xStopCommand   : BOOL;    (* Durdur komutu *)
    xFaultReset    : BOOL;    (* Hata reset *)
    tStartupDelay  : TIME := T#3S;  (* Başlangıç gecikmesi *)
END_VAR
VAR_OUTPUT
    xRunOutput     : BOOL;    (* Motora giden çıkış *)
    xFaultOutput   : BOOL;    (* Hata bayrağı *)
    eState         : E_MotorState;  (* Güncel durum *)
END_VAR
VAR
    tStartTimer    : TON;     (* Başlangıç timer bloğu *)
    xRunFeedback   : BOOL;    (* I/O Mapping'den gelecek *)
END_VAR

(* State machine implementasyonu *)
CASE eState OF
    eIdle:
        xRunOutput := FALSE;
        IF xStartCommand AND NOT xFaultOutput THEN
            eState := eStarting;
        END_IF

    eStarting:
        tStartTimer(IN := TRUE, PT := tStartupDelay);
        xRunOutput := TRUE;
        IF tStartTimer.Q THEN
            tStartTimer(IN := FALSE);
            eState := eRunning;
        END_IF

    eRunning:
        xRunOutput := TRUE;
        IF xStopCommand THEN
            eState := eStopping;
        END_IF

    eStopping:
        xRunOutput := FALSE;
        eState := eIdle;

    eFault:
        xRunOutput := FALSE;
        IF xFaultReset THEN
            xFaultOutput := FALSE;
            eState := eIdle;
        END_IF
END_CASE
```

### Örnek 3: GVL ve DUT Kullanımı

```iecst
(* GVL_IO.gvl *)
VAR_GLOBAL
    (* Motor 1 I/O — EtherCAT mapping'den geliyor *)
    xMotor1_Run    AT %Q0.0 : BOOL;   (* Çalıştır çıkışı *)
    xMotor1_FB     AT %I0.0 : BOOL;   (* Geri bildirim girişi *)
    
    (* Motor 2 — FB instance aracılığıyla *)
    fbMotor2       : FB_Motor;
END_VAR

(* PRG_ConveyorControl.st içinde kullanım *)
PROGRAM PRG_ConveyorControl
VAR
    xStartBtn : BOOL;    (* HMI'dan gelir *)
END_VAR

(* FB instance çağrısı *)
GVL_IO.fbMotor2(
    xStartCommand := xStartBtn,
    xStopCommand  := GVL_IO.xEmergencyStop,
    tStartupDelay := GVL_Params.tMotor2StartDelay
);

(* Çıkışı I/O'ya aktar *)
GVL_IO.xMotor2_Run := GVL_IO.fbMotor2.xRunOutput;
```

## Sık Yapılan Hatalar

### Hata 1: Her Şeyi PLC_PRG İçine Koymak

```
❌ Yanlış:
PROGRAM PLC_PRG
VAR
    (* 300 değişken tanımı *)
    (* Motor 1, Motor 2, Konveyör, Isı, Alarm... hepsi burada *)
END_VAR
(* 2000 satır karışık kod *)

✅ Doğru:
    PLC_PRG sadece orkestratör rolü üstlenir.
    FB_Motor, FB_Conveyor, FB_TemperatureCtrl gibi FB'ler iş mantığını taşır.
    PLC_PRG bunları sadece çağırır ve GVL üzerinden koordine eder.
```

### Hata 2: GVL'yi Tek Bir Dosyaya Yığmak

500+ değişkenli tek bir GVL, yönetilemez hale gelir. İyi yaklaşım:

```
GVL_IO         → Sadece fiziksel I/O değişkenleri
GVL_Params     → Operatörün değiştirebileceği proses parametreleri
GVL_Alarms     → Alarm ve uyarı bayrakları
GVL_Diagnostics→ Teşhis ve sayaçlar
GVL_Recipes    → Reçete verileri
```

### Hata 3: VAR yerine VAR_GLOBAL Kullanmak

Her değişkeni global yapmak **en yaygın başlangıç hatasıdır**. Global değişkenler tüm projenin ortak belleğidir; rastgele yazılabilir, hata ayıklaması güçleşir.

```
❌ Yanlış: Timer ve sayaç değişkenlerini GVL'ye koymak
✅ Doğru : Timer ve sayaçlar FB veya PROGRAM'ın kendi VAR bölümünde olmalı
           GVL yalnızca paylaşılması gereken değerler için kullanılmalı
```

### Hata 4: Library Manager Versiyon Karmaşası

```
❌ Yanlış: Library'yi "Use newest version" olarak eklemek
           → Kütüphane güncellendiğinde proje davranışı beklenmedik şekilde değişebilir

✅ Doğru : Belirli bir versiyon sabitleyin: "Standard, 3.5.17.0"
           Sürüm değişikliği kontrollü yapılmalı; gerileme testi yapılmalı
```

### Hata 5: Task'ı Boş Bırakmak ve PLC_PRG'yi Direkt Çalıştırmak

```
❌ Yanlış: Task Configuration'da hiç program atanmamış
           PLC_PRG otomatik çalışıyor sanılıyor (V2 alışkanlığı)

✅ Doğru : Her PROGRAM, bir Task'a atanmalıdır.
           Task Configuration → Task → Add Call → Program seç
```

### Hata 6: Device Description Olmadan Donanım Bağlamak

Gerçek donanım için doğru device description kurulu olmalıdır. Aksi halde I/O Mapping ekranı görünmez, fieldbus yapılandırması yapılamaz.

```
Tools → Device Repository → Install → [*.devdesc veya *.devpkg dosyası]
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Proje Yapısı Kararları

**Birden Fazla Application Kullanın:**
- Üretim ve test kodu birbirinden bağımsız deploy edilecekse
- Bir uygulama firmware güncellemesiyle değişirken diğeri çalışmaya devam edecekse
- Güvenlik (safety) uygulaması ile süreç uygulaması fiziksel olarak ayrı tutulacaksa

**Tekli Application Yeterlidir:**
- Küçük ve orta ölçekli makineler için (tek konveyör, tek proses ünitesi)
- Tüm mantığın senkronize çalışması gerektiğinde
- Basitlik öncelikliyse

**Function Block Kullanın:**
- Aynı mantık birden fazla yerde kullanılacaksa (FB_Motor yerine 5 farklı motor)
- Bir cihazın tüm yaşam döngüsü (init, run, fault, stop) kapsüllenmek isteniyorsa
- Kütüphane haline getirilecek, başka projelerde kullanılacak kod

**Function Kullanın:**
- Saf dönüşüm işlemleri (birim dönüşümü, bit manipülasyonu, ölçeklendirme)
- Yan etkisi olmayan, giriş → çıkış tarzı hesaplamalar

## Gerçek Proje Notları

**Not 1 — PLC_PRG Tuzağı**  
İlk CODESYS projesinde tüm motor kontrol, sıcaklık kontrolü ve iletişim kodu tek bir PLC_PRG'ye yazıldı. 3 ay sonra müşteri yeni bir motor eklenmesini istedi. Kodun neye bağlı olduğunu çözmek 2 gün sürdü. Function Block mimarisine geçiş toplam 1 haftayı aldı. Ders: Başlangıçta doğru yapı kurmak sonradan katlanarak kazandırır.

**Not 2 — Versiyon Kilitleme Ödülü**  
Bir projede `Util.library` "newest" modda eklenmiş. 6 ay sonra kütüphane güncellenmiş ve FIFO blok arayüzü değişmiş. Derleme aniden hata vermeye başladı. 2 saat debugdan sonra neden bulundu. O günden beri tüm projelerde kütüphane versiyonları sabitlendi.

**Not 3 — I/O Mapping Gözden Kaçan Ayrıntı**  
EtherCAT konfigürasyonunda slave cihazın I/O mapping'i yanlış değişkene bağlandı (xMotor1_FB yerine xMotor2_FB'ye). Program derlendi, çalıştı, ama motor geri bildirimi hiç gelmiyor gibiydi. 4 saatlik debugdan sonra I/O mapping ekranı tekrar kontrol edildi. Ders: I/O mapping ekranını her yeni donanım eklenmesinde sistematik biçimde gözden geçirin.

**Not 4 — Çok Application'ın Gücü**  
Bir paketleme makinesi projesinde:
- `Application_PLC`: Asıl makine mantığı (stable)
- `Application_DataLogger`: Veri kayıt ve iletişim modülü

DataLogger uygulaması geliştirilirken makine çalışmaya devam etti. Güncelleme için makineyi durdurmak gerekmedi. Bu mimarinin değeri, müşteri tesisinde ilk kez gösterildiğinde son derece etkili oldu.

**Not 5 — DUT'lerin Değeri**  
İlk başta struct kullanmaktan kaçınıldı, her motor için ayrı ayrı 10 global değişken tanımlandı (Motor1_Run, Motor1_FB, Motor1_Speed... Motor5_Run...). 5 motor için 50 değişken. Sonra STRUCT tanımlanarak tek bir `ARRAY [1..5] OF ST_MotorData` ile yönetilir hale getirildi. Kod %40 kısaldı, okunabilirlik 3 katına çıktı.

**Not 6 — `.project` İkili Birleştirme (Merge) Cehennemi**  
İki mühendis aynı `.project` dosyasında paralel çalıştı, Git ile birleştirmeye çalıştı. `.project` XML tabanlı olsa da içinde GUID'ler, sıralı ID'ler ve gömülü binary blob'lar vardır; satır-bazlı Git merge **bozuk proje** üretti, dosya açılmadı. Ders: CODESYS projelerinde Git'i "yedek ve geçmiş" için kullanın, ama gerçek işbirliği için **CODESYS Git** entegrasyonu (V3.5 SP17+) ya da object-level export (`.export`/PLCopenXML) + ortak kütüphane mimarisi kullanın. Ekip aynı uygulamada paralel çalışacaksa, mantığı ayrı **kütüphanelere** bölün; her mühendis kendi kütüphanesini sürümler.

**Not 7 — Device Description Sürüm Tuzağı**  
Proje bir mühendisin makinesinde açılıyordu, diğerinde "device not found, repository missing" hatası verdi. Neden: `.devdesc` belirli bir **sürümle** projeye bağlanır; diğer mühendiste o sürüm yüklü değildi (sadece daha yenisi vardı). CODESYS otomatik upgrade yapmaz, eşleşme arar. Ders: Device description paketlerini (`.devpkg`) proje deposunda saklayın ve takım genelinde sürüm sabitleyin. `.projectarchive` kullanırken "Device descriptions" kutusunu işaretleyin — arşive gömülür.

**Not 8 — GVL'de `AT %` Doğrudan Adresleme ile Donanım Değişimi**  
I/O değişkenleri GVL'de `xMotor1_Run AT %Q0.0 : BOOL;` ile sabit adreslere bağlanmıştı. Fieldbus topolojisi değişince (bir slave eklenince) tüm `%Q` adresleri kaydı, yüzlerce çıkış yanlış kanala gitti — makine tehlikeli biçimde yanlış valfleri açtı. Ders: `AT %` doğrudan adreslemeden kaçının; **I/O Mapping ekranı** üzerinden sembolik eşleme yapın. Mapping, slave eklense bile sembolik bağı korur. Doğrudan adres yalnızca topolojisi asla değişmeyecek sabit sistemlerde kullanılmalı.

**Not 9 — Library Namespace Çakışması**  
İki farklı kütüphane aynı isimde bir FB (`FB_Timer`) içeriyordu; derleyici "ambiguous" hatası verdi. Ders: Kütüphaneleri **namespace** ile ekleyin (Library Manager → Properties → Namespace) ve kodda nitelikli erişin: `MyLib.FB_Timer`. Kendi kütüphanelerinizde namespace tanımlamak, ileride çakışmayı baştan engeller.

## Edge Case'ler ve Sistem Limitleri

### Object GUID ve Kopyalama Tuzakları

CODESYS'te her obje (POU, GVL, DUT) bir **GUID** taşır. Bu görünmez ama kritik etkileri vardır:

- Bir POU'yu kopyala-yapıştır yaptığınızda yeni GUID üretilir; ama bazı referanslar (visualization, task call) eski GUID'e bağlı kalabilir → "object not found" tarzı hayalet hatalar.
- İki projeyi birleştirirken aynı GUID'e sahip iki farklı obje varsa, IDE birini sessizce gölgeleyebilir.
- Çözüm: Obje taşımak için kopyala-yapıştır yerine **export/import** (`.export`) kullanın; referans bütünlüğü daha iyi korunur.

### Application ve Task Limitleri

| Sınır | Pratik Değer | Not |
|---|---|---|
| Device başına Application | Cihaza bağlı (genelde 1, bazıları çoklu destekler) | Çoklu app, runtime lisansı/varyantına bağlı |
| Application başına Task | ~16-32 | Belge 01'deki scheduler limiti ile örtüşür |
| GVL boyutu | Pratikte sorun yok, derleme süresi etkilenir | 10.000+ değişken IDE'yi yavaşlatır |
| Nested STRUCT derinliği | Çok derin (~pratik sınır yok) | Ama bellek hizalama dolgu (padding) büyür |
| ARRAY boyutu | Bellekle sınırlı | `ARRAY [0..1000000]` bootapp boyutunu şişirir |

### Persistent vs Retain — İnce Ayrım

İki farklı kalıcılık mekanizması karıştırılır:

```
VAR RETAIN          → power-fail'de korunur, online change'de korunur,
                       RESET (warm) ile korunur, RESET COLD ile silinir
VAR PERSISTENT      → RETAIN'in tüm özellikleri + RESET ORIGIN'e kadar
                       korunur (kod indirmeden bile hayatta kalır)
```

**Edge case:** `PERSISTENT` değişkenler `PersistentVars` adında özel bir liste objesinde toplanmalıdır; rastgele bir POU içinde `VAR PERSISTENT` tanımlamak bazı sürümlerde derlenir ama **kaydedilmez** (sessiz veri kaybı). Daima `Add Object → Persistent Variables` listesi kullanın.

### Boş Task / Çağrılmayan POU

- Task Configuration'a atanmamış bir PROGRAM **hiç çalışmaz** ama derlenir ve bootapp'a dahil edilir (ölü kod). Statik analiz bunu "unused" olarak işaretler.
- Bir Task'a atanmış ama içi boş bir program, scheduler'da yer tutar ve cycle overhead yaratır — gereksiz task'lar performans kaçağıdır.

## Optimizasyon

### Proje Mimarisini Yeniden Kullanılabilirlik İçin Tasarlama

- **Kütüphane-merkezli mimari:** Tekrar eden mantığı (motor, valf, PID, iletişim) projeye gömmek yerine **dahili kütüphaneye** (`.library`) çıkarın. Her proje kütüphaneyi sürüm-sabit referansla kullanır. Avantaj: Bir bug fix tüm projelere tek noktadan yayılır; IP korumalı (`.compiled-library`) dağıtım mümkün olur.
- **Interface tabanlı bağımlılık:** FB'leri somut tiplere değil, `INTERFACE`'lere bağlayın (ör. `I_Motor`). Bu, test için mock instance enjekte etmeyi ve farklı donanımları aynı arayüzle değiştirmeyi sağlar.
- **GVL'yi katmanla:** `GVL_IO` (donanım sınırı), `GVL_Params` (operatör), `GVL_State` (iç durum), `GVL_Diag` (telemetri). Bu ayrım, OPC UA ile dışarı açılacak değişken setini netleştirir ve erişim kontrolünü kolaylaştırır.

### Derleme ve IDE Performansı

- **Büyük projelerde derleme süresi:** Çok sayıda visualization, derleme süresini lineer artırır. Geliştirme sırasında kullanılmayan visualization'ları ayrı bir application'a taşıyın veya "exclude from build" kullanın.
- **`__VARINFO` ve sembol dosyaları:** OPC UA / sembolik erişim için üretilen sembol konfigürasyonu (Symbol Configuration) gereğinden fazla değişken içeriyorsa hem bootapp şişer hem indirme yavaşlar. Yalnızca dışa açılacak değişkenleri seçin.

### Bellek Düzeni Optimizasyonu

- **STRUCT alan sıralaması:** Alanları **boyuta göre büyükten küçüğe** sıralamak (LREAL/DINT önce, BOOL sonra) hizalama dolgusunu (padding) azaltır. Karışık sıralanmış bir struct, `pack_mode` olmadan %30'a varan bellek israfı yaratabilir.
- **BOOL paketleme:** 100 ayrı `BOOL` yerine bir `WORD`/`DWORD` + bit erişimi (`wFlags.0`) hem bellek hem fieldbus bant genişliği tasarrufu sağlar — özellikle Modbus gibi register-tabanlı protokollerde.

## Derin Teknik Detay

### `.project` Dosyasının Anatomisi

`.project` aslında bir **SQLite-benzeri yapılandırılmış konteyner** değil, sıkıştırılmış/XML hibrit bir formattır (sürüme göre değişir). İçinde:

- Her obje ayrı bir "POU object" olarak GUID ile saklanır.
- Derleme çıktısı (compile cache) ayrı tutulur — bu yüzden `Clean` sonrası dosya küçülür.
- Kütüphane referansları **gerçek kütüphaneyi içermez**, yalnızca (isim, sürüm, namespace) referansını tutar. Bu yüzden `.project` taşınınca kütüphaneler eksik olabilir; `.projectarchive` ise bağımlılıkları paketler.

Bu tasarım, "neden Git merge çalışmıyor" sorusunun cevabıdır: dosya satır-bazlı diff için değil, IDE'nin obje grafiğini serileştirmesi için tasarlanmıştır.

### Device Tree Neden Hiyerarşik? — Donanım Soyutlamasının Yansıması

Device Tree, fiziksel donanım topolojisini birebir yansıtır: `Device → Bus Master → Slave → Module → Channel`. Bu kasıtlıdır:

- I/O adresleri (`%I`, `%Q`) bu hiyerarşiden **otomatik türetilir**. Bir slave'i ağaçta yukarı/aşağı taşımak, altındaki tüm kanalların adreslerini yeniden hesaplatır (Not 8'deki tuzağın kökü).
- Fieldbus tarama (scan) sonucu doğrudan bu ağaca yazılır; gerçek donanımı "öğrenip" ağaca ekler.
- Her düğüm kendi konfigürasyon parametrelerini (PDO mapping, COE startup) taşır — donanım davranışı kod değil, ağaç konfigürasyonuyla belirlenir. Bu, "configuration as data" felsefesidir: aynı kod, farklı ağaç konfigürasyonuyla farklı donanımlarda çalışır.

### PLC Logic Katmanı Neden Var?

`Device → PLC Logic → Application` zincirindeki **PLC Logic** ara düğümü gereksiz görünür ama bir amacı vardır: Bir cihaz birden fazla **çalıştırma bağlamı** (execution context) barındırabilir — ör. ana CPU + bir koprosör + bir safety controller. Her biri ayrı bir "PLC Logic" düğümü olur. Tek CPU'lu cihazlarda tek PLC Logic görürsünüz, ama mimari çoklu işlemcili karmaşık cihazları (ör. CPU + entegre motion kontrolcü) aynı ağaçta temsil edebilmek için bu katmanı korur.

### Online Change'in Proje Yapısıyla İlişkisi

Online Change'in neden bazı değişiklikleri kabul edip bazılarını reddettiği, proje yapısının bellek düzeniyle ilgilidir:

- **Kabul edilen:** Mevcut bir FB'nin implementasyonunu değiştirmek, yeni POU eklemek, yerel değişken eklemek (sona).
- **Reddedilen / clean download gerektiren:** Bir FB'nin **arayüzünü** (VAR_INPUT/OUTPUT) değiştirmek, GVL'de değişken **sırasını** değiştirmek, task konfigürasyonunu değiştirmek, retain layout'unu bozmak.

Neden? Online Change, çalışan instance'ların **bellek görüntüsünü** korumaya çalışır. Arayüz/sıralama değişikliği bellek haritasını kaydırır; çalışan veriyi taşıyamaz. Bu yüzden "yeni değişkeni sona ekle" kuralı altın değerindedir — sona ekleme bellek haritasının başını bozmaz.

## İlgili Konular

```
knowledge/codesys/fundamentals/
├── 01_runtime_architecture.md  → Bu yapıyı çalıştıran runtime'ın detayı
├── 03_iec61131_languages.md    → POU'ların içinde hangi dil kullanılır
└── _synthesis.md               → Üç belgenin özet sentezi

knowledge/codesys/tasks/
├── task_types.md               → Task türlerinin derinlemesine analizi
└── task_priority_design.md     → Öncelik mimarisi tasarım rehberi

knowledge/codesys/libraries/
├── standard_library.md         → TON, TOF, CTU, RS bloklarının kullanımı
└── util_library.md             → FIFO, ring buffer, format string

knowledge/codesys/best_practices/
└── naming_conventions.md       → Değişken isimlendirme standartları

knowledge/standards/
└── iec61131_pou_types.md       → IEC standardındaki POU tanımları
```
