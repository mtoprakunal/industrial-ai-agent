---
KONU        : Paketleme Makineleri Otomasyonu (CODESYS)
KATEGORİ    : applications
ALT_KATEGORI: packaging
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://www.omac.org/packml"
    başlık: "PackML — OMAC Packaging Workgroup resmi sayfası"
    güvenilirlik: resmi
  - url: "https://en.wikipedia.org/wiki/PackML"
    başlık: "PackML — Wikipedia (ISA-TR88.00.02 özeti)"
    güvenilirlik: topluluk
  - url: "https://en.wikipedia.org/wiki/ISA-88"
    başlık: "ISA-88 Batch Control Standard — Wikipedia"
    güvenilirlik: topluluk
  - url: "https://www.isa.org/standards-and-publications/isa-standards/isa-88-standards"
    başlık: "ISA-88 Series of Standards — ISA resmi sayfası"
    güvenilirlik: resmi
  - url: "https://www.oee.com/"
    başlık: "OEE (Overall Equipment Effectiveness) — oee.com"
    güvenilirlik: topluluk
  - url: "https://evocon.com/articles/how-to-calculate-oee-formulas-examples/"
    başlık: "OEE Calculation: Formulas, Examples, and Insights — Evocon"
    güvenilirlik: topluluk
  - url: "https://plcprogramming.io/blog/packaging-machine-plc-programming-guide"
    başlık: "Packaging Machine PLC Programming Guide — PLCProgramming.io"
    güvenilirlik: topluluk
  - url: "https://content.helpme-codesys.com/en/CODESYS%20SFC/_sfc_start_page.html"
    başlık: "CODESYS SFC — Resmi Online Yardım"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_preserve_data_with_recipes.html"
    başlık: "Preserving Data with Recipes — CODESYS Online Help"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_preserve_data_with_persistent_variables.html"
    başlık: "Preserving Data with Persistent Variables — CODESYS Online Help"
    güvenilirlik: resmi
  - url: "https://store.codesys.com/media/n98_media_assets/files/Bundle-SoftMotion/0/CODESYS%20SoftMotion%20SL_en.pdf"
    başlık: "CODESYS SoftMotion Data Sheet — 3S-Smart Software Solutions"
    güvenilirlik: resmi
  - url: "https://www.sense-the-world.com/tech-hub/24546.html"
    başlık: "How to Wire Proximity Sensors for Packaging Machines"
    güvenilirlik: topluluk
  - url: "https://sgsystemsglobal.com/glossary/isa-88-phases-equipment-modules/"
    başlık: "ISA-88 Phases & Equipment Modules — SG Systems Global"
    güvenilirlik: topluluk
  - url: "knowledge/codesys/fundamentals/03_iec61131_languages.md"
    başlık: "CODESYS'te IEC 61131-3 Programlama Dilleri — FB_PackagingMachine SFC/CASE örneği"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/task-structure/_synthesis.md"
    başlık: "CODESYS Task Yapısı Sentezi — Basit Makine Şablonu A"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/_synthesis.md"
    başlık: "CODESYS Programlama Mimarisi Sentezi — FB, GVL, Hata Yönetimi"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "codesys/fundamentals/03_iec61131_languages"
    ilişki: gerektirir
  - konu: "codesys/task-structure/_synthesis"
    ilişki: gerektirir
  - konu: "codesys/programming/_synthesis"
    ilişki: gerektirir
  - konu: "applications/conveyor"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "IEC 61131-3 ST ve SFC dilleri (03_iec61131_languages.md)"
  - "CODESYS Task yapısı — Cyclic task, Freewheeling, öncelik yönetimi"
  - "Function Block tasarımı (CASE state machine, VAR_INPUT/OUTPUT)"
  - "TON, CTU, R_TRIG standard kütüphane blokları"
ÇELİŞKİLER :
  - kaynak: "CODESYS Recipe Manager resmi dokümantasyonu"
    konu: "Array of STRUCT içeren reçetelerin yüklenmesinde indeks kaybı sorunu bildirilmiştir"
    çözüm: >
      Array of STRUCT yerine sabit sayıda struct instance kullanın (ör. 20 adet
      ST_Recipe instance) ve dönüştürücü fonksiyon ile yükle/kaydet yapın.
      Alternatif: Reçete verisini PERSISTENT GVL'de Array olarak saklayın,
      Recipe Manager'ı yalnızca dosya export/import için kullanın.
  - kaynak: "PackML (ISA-TR88.00.02) ile CODESYS SFC state isimleri"
    konu: "PackML 17 standart durum tanımlar (Stopped, Idle, Running, Aborting vb.);
           CODESYS SFC step isimlendirmesi keyfidir ve PackML'e otomatik uymaz"
    çözüm: >
      Step isimlerini PackML durum adlarıyla eşleştirin (ör. Step_Idle, Step_Execute,
      Step_Aborting). Bu, SCADA/OPC UA entegrasyonunda durum okumayı standartlaştırır.
---

## Özün Ne

Paketleme makineleri, ürünleri besleme (feed), konumlama (positioning), kaplama/yapıştırma (sealing), atma (ejection) ve sayım (counting) adımlarından oluşan döngüsel bir sekansı yüksek hızda ve güvenilir biçimde tekrarlar. Bu sekans, IEC 61131-3 SFC (Sequential Function Chart) ile doğal olarak ifade edilir; her sekans adımı bir SFC Step, geçiş koşulları ise Transition olarak tanımlanır. CODESYS bu yapıyı online debug görünürlüğüyle destekler: hangi adımın aktif olduğu gerçek zamanlı olarak ekranda izlenebilir — bu özellik, saha sorunlarının teşhisini dramatik ölçüde hızlandırır. Paketleme otomasyon projelerinde SFC ana iskelet, ST ise adım içi detay mantığı için birlikte kullanılır.

## Nasıl Çalışır

### Tipik Paketleme Makinesi Sekansı

Tüm paketleme makineleri, makine türünden bağımsız olarak aynı temel döngüyü izler:

```
┌────────────────────────────────────────────────────────────────────────────┐
│              PAKETlEME MAKİNESİ TEMEL DÖNGÜSÜ                              │
├─────────────────┬──────────────────────────────────────────────────────────┤
│ Adım            │ Açıklama                                                  │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ 1. BESLEME      │ Ürün konveyörden makine bölgesine taşınır                │
│    (Feed)       │ Foto-sensör ürünü algılar → index hareketi tamamlanır    │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ 2. KONUMLAMA    │ Ürün sealing istasyonuna göre hizalanır                  │
│    (Positioning)│ Servo veya pnömatik konumlandırma; enkoder geri bildirimi │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ 3. SEALING      │ Isı veya yapıştırıcıyla ambalaj kapatılır                │
│    (Yapıştırma) │ Zamanlama KRİTİK: T_seal aşılırsa ürün yanar/bozulur    │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ 4. SOĞUTMA      │ (Opsiyonel, ısıl sealing sonrası) Kısa bekleme           │
│    (Cool)       │ Sealing elemanının ürüne yapışmaması için                 │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ 5. EJEKSİYON    │ Paketlenmiş ürün çıkış konveyörüne itilir                │
│    (Ejection)   │ Pnömatik silindir; pozisyon geri bildirimiyle doğrulanır │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ 6. SAYIM        │ Üretim sayacı artırılır; OEE verisi güncellenir           │
│    (Count)      │ Aktif reçete parametrelerine göre hedef kontrol edilir    │
└─────────────────┴──────────────────────────────────────────────────────────┘
```

### PackML Durum Modeli ile İlişki

OMAC tarafından geliştirilen ve ISA-TR88.00.02 olarak standartlaştırılan **PackML**, paketleme makinesi yazılımı için 17 standart durum tanımlar. Bu durumlar CODESYS SFC adımlarıyla bire bir eşleştirilebilir:

```
PackML Ana Durumları            CODESYS SFC Step Karşılığı
─────────────────────────────────────────────────────────
Stopped  → Duraklatılmış, E-stop    Step_Stopped
Idle     → Başlatmaya hazır         Step_Idle
Running  → Ana üretim döngüsü       Step_Execute (alt SFC)
Held     → Geçici bekleme           Step_Held
Aborting → Acil durdurma            Step_Aborting (en hızlı)
Aborted  → Güvenli durdu            Step_Aborted
Complete → Parti tamamlandı         Step_Complete
```

PackML'in CODESYS implementasyonunda her PackML durumu bir SFC step, her komut (Start, Stop, Hold, Abort) ise bir SFC transition koşulu olarak yazılır. Bu yaklaşım OPC UA sunucusunun `PackML:State` etiketini standart biçimde raporlamasını sağlar. (Kaynak: OMAC PackML, ISA-TR88.00.02, 2008)

### ISA-88 Hiyerarşisi ile Paketleme Makinesi

ISA-88 fiziksel model hiyerarşisinde paketleme makinesi şöyle konumlanır:

```
Site
└── Area: Paketleme Hattı
    └── Process Cell: Paketleme Ünitesi
        ├── Unit: Sealing İstasyonu
        │   ├── Equipment Module: Sealing Çenesi (Jaw)
        │   │   └── Control Module: Isıtıcı + Sıcaklık Sensörü
        │   └── Equipment Module: Konumlama Silindiri
        ├── Unit: Besleme Konveyörü
        │   └── Control Module: Foto-sensör + Motor
        └── Unit: Ejeksiyon İstasyonu
            └── Control Module: Pnömatik Silindir + Pozisyon Sensörü
```

Bu hiyerarşi doğrudan CODESYS GVL yapısına yansıtılır: her Equipment Module için bir Function Block, her Control Module için ayrı I/O eşlemesi.

### Zamanlama Kritik Adımlar

Paketleme makinesinde iki adım zamanlama açısından kritiktir:

| Adım | Kritiklik | Neden | Sonuç |
|---|---|---|---|
| Sealing | ±50ms tolerans | Az ısı: ambalaj açılır; Fazla ısı: ürün bozulur | Reçeteden okunan T_seal değeri TON ile uygulanır |
| Ejeksiyon | ±20ms tolerans | Erken ejekt: ürün kayar; Geç ejekt: sonraki ürüne çarpışma | Pozisyon sensörü ile çift doğrulama |

---

## Pratikte Nasıl Kullanılır

### CODESYS Proje Mimarisi

Paketleme makinesi için önerilen CODESYS mimarisi:

```
Application
├── GVL_IO           → AT % fiziksel sinyal eşlemeleri
├── GVL_HMI          → Operatör komutları, ekran değerleri
├── GVL_Params       → Aktif reçete parametreleri
├── GVL_Alarms       → Alarm ve uyarı bayrakları
├── GVL_Recipes      → PERSISTENT: tüm reçete tablosu
├── GVL_Production   → RETAIN: üretim sayaçları, OEE verileri
│
├── DUTs
│   ├── E_PackState  → ENUM: makine durumları
│   ├── E_FaultCode  → ENUM: hata kodları
│   └── ST_Recipe    → STRUCT: reçete parametreleri
│
├── POUs
│   ├── FB_ConveyorFeed    → Besleme konveyörü kontrolü
│   ├── FB_SealingJaw      → Sealing çenesi + sıcaklık koruması
│   ├── FB_Ejector         → Ejeksiyon silindiri
│   ├── FB_ProductSensor   → Foto-sensör + filtre
│   ├── FB_RecipeManager   → Reçete yükleme/kaydetme
│   ├── FB_OEECalculator   → OEE hesaplama
│   └── FB_SafetyMonitor   → Kapı, E-stop izleme
│
├── PRG_MainSequence → SFC: ana paketleme döngüsü
├── PRG_Safety       → LD: güvenlik interlockları
└── PRG_HMI          → ST: HMI veri güncelleme
```

### Task Yapısı (Task Synthesis Şablon A — Basit Makine)

```
Task_Safety   Cyclic  5ms  Prio:0   E-stop, kapı kilidi, sealing ısı aşımı
Task_Control  Cyclic 10ms  Prio:2   Ana sekans, sensörler, aktüatörler
Task_Slow     Cyclic100ms  Prio:5   HMI güncelleme, OEE hesaplama
Task_Log      Freewheel   Prio:15  Üretim logu, dosya yazma
```

Sealing kritik adım için Task_Control'ün 10ms döngüsü yeterlidir: TON zamanlayıcı ±10ms hassasiyetle çalışır ve standart sealing süresi 500ms–2000ms aralığındadır.

### Ürün Algılama (Foto-sensör)

Foto-sensör (photoelectric sensor) ürün varlığını algılar. İki tip yayın yapılır:

**Doğrudan sinyal (ham I/O):**
```iecst
(* GVL_IO.xProductSensor_Raw → R_TRIG ile kenar algıla *)
rtProductDetect(CLK := GVL_IO.xProductSensor_Raw);
IF rtProductDetect.Q THEN
    (* Ürün algılandı, sayacı artır *)
    GVL_Production.dwDetectedCount := GVL_Production.dwDetectedCount + 1;
END_IF
```

**Filtrelenmiş FB:**
```iecst
FUNCTION_BLOCK FB_ProductSensor
VAR_INPUT
    xRaw        : BOOL;  (* Ham sensör sinyali *)
    tDebounce   : TIME := T#20MS;  (* Titreşim filtresi *)
END_VAR
VAR_OUTPUT
    xDetected   : BOOL;  (* Filtrelenmiş, kararlı çıkış *)
    xRisingEdge : BOOL;  (* Ürün geldi — tek pulse *)
END_VAR
VAR
    tFilter     : TON;
    rtEdge      : R_TRIG;
END_VAR

tFilter(IN := xRaw, PT := tDebounce);
xDetected   := tFilter.Q;
rtEdge(CLK  := xDetected);
xRisingEdge := rtEdge.Q;
```

### Reçete Yönetimi

Farklı ürün boyutları için reçete yapısı:

```iecst
TYPE ST_Recipe :
STRUCT
    sName           : STRING(40);   (* Reçete adı: "BisBüyük_200g" *)
    tSealTime       : TIME;         (* Sealing süresi: T#800MS *)
    rSealTemp_C     : REAL;         (* Sealing sıcaklığı: 180.0 °C *)
    tEjectTime      : TIME;         (* Ejeksiyon süresi: T#300MS *)
    tFeedDelay      : TIME;         (* Besleme gecikmesi *)
    rConveyorSpeed  : REAL;         (* Konveyör hızı %: 65.0 *)
    nBatchTarget    : DWORD;        (* Parti hedef adedi: 1000 *)
END_STRUCT
END_TYPE

(* GVL_Recipes — PERSISTENT: download'a dayanır *)
VAR_GLOBAL PERSISTENT
    aRecipes        : ARRAY[1..20] OF ST_Recipe;
    nActiveRecipeIdx: INT := 1;
END_VAR
```

Reçete değişimi Event task ile tetiklenir — üretim sırasında aktif reçete değişmez:

```iecst
(* FB_RecipeManager içinde *)
FUNCTION_BLOCK FB_RecipeManager
VAR_INPUT
    xLoadCmd    : BOOL;   (* HMI'dan yükleme komutu *)
    nRecipeIdx  : INT;    (* Yüklenecek reçete indeksi *)
END_VAR
VAR
    rtLoad      : R_TRIG;
    xSeqBusy    : BOOL;
END_VAR

rtLoad(CLK := xLoadCmd);
IF rtLoad.Q AND NOT xSeqBusy THEN
    (* Sadece makine Idle durumdayken yükle *)
    IF GVL_HMI.eMachineState = eState_Idle THEN
        GVL_Params.stActiveRecipe := GVL_Recipes.aRecipes[nRecipeIdx];
        GVL_HMI.sActiveRecipeName := GVL_Params.stActiveRecipe.sName;
    END_IF
END_IF
```

---

## Örnekler

### Örnek 1: Tam SFC Yapısı — Paketleme Döngüsü (ST Transition + Aksiyon)

```
(* PRG_MainSequence — SFC diyagramı metin gösterimi *)
(* Adımlar ve geçişler SFC grafik editöründe çizilir;
   aksiyon ve transition kodları aşağıda ST olarak yazılır. *)

         ══════════════
           Step_Idle          ← Makine bekliyor, hazır
         ══════════════
               │
    [T_IdleToFeed: xStartCmd AND xProductReady AND NOT xSafetyFault]
               │
         ══════════════
           Step_Feed          ← Besleme konveyörü ürünü ilerletiyor
         ══════════════
               │
    [T_FeedToPosition: fbProductSensor.xRisingEdge AND fbConveyor.xAtPosition]
               │
         ══════════════
           Step_Position      ← Ürün sealing istasyonuna konumlanıyor
         ══════════════
               │
    [T_PositionToSeal: fbEjector.xHomeOK AND fbPositioner.xAtTarget]
               │
         ══════════════
           Step_Sealing       ← Isıl sealing uygulanıyor (KRİTİK)
         ══════════════
               │
    [T_SealToEject: fbSealingJaw.xSealComplete AND NOT fbSealingJaw.xFault]
               │
         ══════════════
           Step_Ejection      ← Paket çıkış konveyörüne itiliyor
         ══════════════
               │
    [T_EjectToCount: fbEjector.xEjectComplete]
               │
         ══════════════
           Step_Count         ← Sayaç artırılıyor, OEE güncelleniyor
         ══════════════
               │
    [T_CountToIdle: TRUE]      ← Koşulsuz: hemen bir sonraki döngüye
               │
    (Step_Idle'a döner — döngü)
```

### Örnek 2: Sealing Adımı SFC Aksiyonu (ST)

```iecst
(* Step_Sealing — ACTION: During (adım aktifken her döngüde çalışır) *)
ACTION Step_Sealing_During:

(* Sealing çenesi FB'yi çağır *)
fbSealingJaw(
    xCloseCmd       := TRUE,
    rTempSetpoint_C := GVL_Params.stActiveRecipe.rSealTemp_C,
    tSealDuration   := GVL_Params.stActiveRecipe.tSealTime,
    xTempOK         := GVL_IO.xSealTempOK
);

(* Isı aşımı koruması — güvenlik katmanı *)
IF GVL_IO.rSealTemp_C > (GVL_Params.stActiveRecipe.rSealTemp_C + 20.0) THEN
    GVL_Alarms.xSealOverTemp := TRUE;
END_IF

END_ACTION

(* Step_Sealing — ACTION: Exit (adım terk edilirken bir kez çalışır) *)
ACTION Step_Sealing_Exit:
    fbSealingJaw(xCloseCmd := FALSE);
    GVL_Alarms.xSealOverTemp := FALSE;
END_ACTION
```

### Örnek 3: Sealing FB — Zamanlama Kritik Uygulama

```iecst
FUNCTION_BLOCK FB_SealingJaw
VAR_INPUT
    xCloseCmd       : BOOL;
    rTempSetpoint_C : REAL;
    tSealDuration   : TIME;
    xTempOK         : BOOL;  (* Isı hedefine ulaştı *)
END_VAR
VAR_OUTPUT
    xSealComplete   : BOOL;
    xFault          : BOOL;
    eFaultCode      : DWORD;
    sFaultMsg       : STRING(80);
    eState          : E_SealState;
END_VAR
VAR
    tSealTimer      : TON;
    tTempTimeout    : TON;
END_VAR

CASE eState OF

    eSeal_Idle:
        xSealComplete := FALSE;
        xFault        := FALSE;
        IF xCloseCmd THEN
            eState := eSeal_Heating;
        END_IF

    eSeal_Heating:
        (* Isının hedefe ulaşması için max 10s bekle *)
        tTempTimeout(IN := TRUE, PT := T#10S);
        IF xTempOK THEN
            tTempTimeout(IN := FALSE);
            eState := eSeal_Pressing;
        ELSIF tTempTimeout.Q THEN
            tTempTimeout(IN := FALSE);
            eFaultCode := 16#0101;
            sFaultMsg  := 'Sealing: Hedef sicakliga 10s icinde ulaslamadi';
            xFault     := TRUE;
            eState     := eSeal_Fault;
        END_IF

    eSeal_Pressing:
        (* Belirlenen süre boyunca çene kapalı ve ısı aktif *)
        tSealTimer(IN := TRUE, PT := tSealDuration);
        IF tSealTimer.Q THEN
            tSealTimer(IN := FALSE);
            xSealComplete := TRUE;
            eState        := eSeal_Opening;
        END_IF
        (* Isı aşımı kontrol *)
        IF NOT xTempOK AND NOT GVL_IO.xSealHeaterOn THEN
            eFaultCode := 16#0102;
            sFaultMsg  := 'Sealing: Pres sirasinda isi kaybi';
            xFault     := TRUE;
            eState     := eSeal_Fault;
        END_IF

    eSeal_Opening:
        (* Çene açılma hareketi *)
        IF NOT xCloseCmd THEN
            xSealComplete := FALSE;
            eState        := eSeal_Idle;
        END_IF

    eSeal_Fault:
        xSealComplete := FALSE;
        (* Sadece hata reset komutuyla çıkılabilir *)
        IF GVL_HMI.xFaultReset THEN
            xFault     := FALSE;
            eFaultCode := 0;
            sFaultMsg  := '';
            eState     := eSeal_Idle;
        END_IF

    ELSE:
        (* Bilinmeyen durum — savunmacı programlama *)
        xSealComplete := FALSE;
        xFault        := TRUE;
        eFaultCode    := 16#00FF;
        sFaultMsg     := 'Sealing FB: Bilinmeyen durum';
        eState        := eSeal_Fault;

END_CASE
```

### Örnek 4: OEE Hesaplama FB

OEE = Kullanılabilirlik × Performans × Kalite formülüne göre (Kaynak: [oee.com](https://www.oee.com/)):

```iecst
FUNCTION_BLOCK FB_OEECalculator
VAR_INPUT
    tPlannedTime    : TIME;   (* Planlanan üretim süresi *)
    tDowntime       : TIME;   (* Arıza + setup toplam kayıp *)
    dwActualParts   : DWORD;  (* Gerçekte üretilen parça *)
    dwGoodParts     : DWORD;  (* İyi parça (kalite geçer) *)
    rIdealCycleTime : REAL;   (* Saniye/parça — reçeteden *)
END_VAR
VAR_OUTPUT
    rAvailability   : REAL;   (* 0.0 – 1.0 *)
    rPerformance    : REAL;
    rQuality        : REAL;
    rOEE            : REAL;
    rOEE_Pct        : REAL;   (* % formatında *)
END_VAR
VAR
    rOperatingTime_S : REAL;
    rPlannedTime_S   : REAL;
    rTheoreticalParts: REAL;
END_VAR

(* TIME → REAL saniye dönüşümü *)
rPlannedTime_S   := TIME_TO_REAL(tPlannedTime)  / 1000.0;
rOperatingTime_S := rPlannedTime_S - (TIME_TO_REAL(tDowntime) / 1000.0);

(* Kullanılabilirlik: Fiili çalışma / Planlanan süre *)
IF rPlannedTime_S > 0.0 THEN
    rAvailability := rOperatingTime_S / rPlannedTime_S;
ELSE
    rAvailability := 0.0;
END_IF

(* Performans: Gerçek üretim / Teorik maksimum üretim *)
IF rIdealCycleTime > 0.0 AND rOperatingTime_S > 0.0 THEN
    rTheoreticalParts := rOperatingTime_S / rIdealCycleTime;
    rPerformance := DWORD_TO_REAL(dwActualParts) / rTheoreticalParts;
ELSE
    rPerformance := 0.0;
END_IF

(* Kalite: İyi parça / Toplam üretim *)
IF dwActualParts > 0 THEN
    rQuality := DWORD_TO_REAL(dwGoodParts) / DWORD_TO_REAL(dwActualParts);
ELSE
    rQuality := 0.0;
END_IF

(* OEE: Üç faktörün çarpımı *)
rOEE     := rAvailability * rPerformance * rQuality;
rOEE_Pct := rOEE * 100.0;
```

### Örnek 5: ST ile Tam CASE State Machine — FB_PackagingMachine

İç bilgi tabanından alınan ve genişletilen FB_PackagingMachine (kaynak: `knowledge/codesys/fundamentals/03_iec61131_languages.md`, Örnek 3):

```iecst
TYPE E_PackStep : (
    ePack_Idle       := 0,
    ePack_Feed       := 1,
    ePack_Position   := 2,
    ePack_Sealing    := 3,
    ePack_Ejecting   := 4,
    ePack_Counting   := 5,
    ePack_Fault      := 99
) END_TYPE

FUNCTION_BLOCK FB_PackagingMachine
VAR_INPUT
    xStartCmd    : BOOL;
    xStopCmd     : BOOL;
    xFaultReset  : BOOL;
    xItemDetect  : BOOL;   (* Foto-sensör: ürün konveyörde *)
    xAtPosition  : BOOL;   (* Pozisyonlama tamamlandı *)
    xSealComplete: BOOL;   (* Sealing FB'den onay *)
    xSealFault   : BOOL;   (* Sealing FB hatası *)
    stRecipe     : ST_Recipe;  (* Aktif reçete *)
END_VAR
VAR_OUTPUT
    xConveyorRun : BOOL;
    xSealerCmd   : BOOL;   (* Sealing çenesi kapat *)
    xEjectorCmd  : BOOL;
    eCurrentStep : E_PackStep;
    xFault       : BOOL;
    sFaultMsg    : STRING(80);
    dwPackCount  : DWORD;
    xCycleDone   : BOOL;   (* Her başarılı döngüde 1 pulse *)
END_VAR
VAR
    tEjectTimer  : TON;
    tFeedTimeout : TON;
    rtCycleDone  : R_TRIG;
END_VAR

xCycleDone := FALSE;

CASE eCurrentStep OF

    ePack_Idle:
        xConveyorRun := FALSE;
        xSealerCmd   := FALSE;
        xEjectorCmd  := FALSE;
        IF xStartCmd AND NOT xFault THEN
            eCurrentStep := ePack_Feed;
        END_IF

    ePack_Feed:
        xConveyorRun := TRUE;
        (* Ürün algılama timeout koruması: max 30s *)
        tFeedTimeout(IN := TRUE, PT := T#30S);
        IF xItemDetect THEN
            tFeedTimeout(IN := FALSE);
            xConveyorRun := FALSE;
            eCurrentStep := ePack_Position;
        ELSIF tFeedTimeout.Q THEN
            tFeedTimeout(IN := FALSE);
            xConveyorRun := FALSE;
            xFault       := TRUE;
            sFaultMsg    := 'Feed timeout: 30s icinde urun algılanamadi';
            eCurrentStep := ePack_Fault;
        END_IF
        IF xStopCmd THEN
            tFeedTimeout(IN := FALSE);
            xConveyorRun := FALSE;
            eCurrentStep := ePack_Idle;
        END_IF

    ePack_Position:
        (* Konumlandırma mekanizması hareket ediyor *)
        (* xAtPosition: encoder/limit switch onayı *)
        IF xAtPosition THEN
            eCurrentStep := ePack_Sealing;
        END_IF

    ePack_Sealing:
        xSealerCmd := TRUE;
        IF xSealComplete THEN
            xSealerCmd   := FALSE;
            eCurrentStep := ePack_Ejecting;
        ELSIF xSealFault THEN
            xSealerCmd   := FALSE;
            xFault       := TRUE;
            sFaultMsg    := 'Sealing hatasi - FB_SealingJaw raportu';
            eCurrentStep := ePack_Fault;
        END_IF
        IF xStopCmd THEN
            xSealerCmd   := FALSE;
            eCurrentStep := ePack_Idle;
        END_IF

    ePack_Ejecting:
        xEjectorCmd := TRUE;
        tEjectTimer(IN := TRUE, PT := stRecipe.tEjectTime);
        IF tEjectTimer.Q THEN
            tEjectTimer(IN := FALSE);
            xEjectorCmd  := FALSE;
            eCurrentStep := ePack_Counting;
        END_IF

    ePack_Counting:
        dwPackCount  := dwPackCount + 1;
        xCycleDone   := TRUE;  (* OEE hesaplama ve HMI için pulse *)
        (* Parti hedefine ulaşıldı mı? *)
        IF dwPackCount >= stRecipe.nBatchTarget THEN
            eCurrentStep := ePack_Idle;
        ELSE
            eCurrentStep := ePack_Feed;  (* Sonraki döngü *)
        END_IF

    ePack_Fault:
        xConveyorRun := FALSE;
        xSealerCmd   := FALSE;
        xEjectorCmd  := FALSE;
        IF xFaultReset THEN
            xFault       := FALSE;
            sFaultMsg    := '';
            eCurrentStep := ePack_Idle;
        END_IF

    ELSE:
        (* Bilinmeyen durum — savunmacı programlama *)
        xConveyorRun := FALSE;
        xSealerCmd   := FALSE;
        xEjectorCmd  := FALSE;
        xFault       := TRUE;
        sFaultMsg    := 'PackagingMachine: Bilinmeyen step durumu';
        eCurrentStep := ePack_Fault;

END_CASE
```

### Örnek 6: Güvenlik Katmanı (PRG_Safety — LD Mantığı ST ile)

```iecst
(* PRG_Safety — Task_Safety, Cyclic 5ms, Prio:0 *)
(* Tüm güvenlik sinyallerini her döngüde bağımsız kontrol eder *)
PROGRAM PRG_Safety
VAR
    rtDoorOpen   : R_TRIG;
    tEStopDelay  : TON;
END_VAR

(* E-stop: anlık kapatma — gecikme YOK *)
IF GVL_IO.xEmergencyStop THEN
    GVL_IO.xConveyorOut  := FALSE;
    GVL_IO.xSealerOut    := FALSE;
    GVL_IO.xEjectorOut   := FALSE;
    GVL_Alarms.xEStopActive := TRUE;
END_IF

(* Güvenlik kapısı: kapı açılırsa makineyi durdur *)
rtDoorOpen(CLK := NOT GVL_IO.xSafetyDoor_Closed);
IF rtDoorOpen.Q THEN
    GVL_Alarms.xDoorOpenAlarm := TRUE;
END_IF
IF GVL_Alarms.xDoorOpenAlarm THEN
    GVL_IO.xConveyorOut := FALSE;
    GVL_IO.xSealerOut   := FALSE;
    (* Ejektör: kapı açılınca da çalışmaya devam edebilir
       SADECE bakım modu aktifse ve hız düşükse *)
    IF NOT GVL_HMI.xMaintenanceMode THEN
        GVL_IO.xEjectorOut := FALSE;
    END_IF
END_IF

(* Sealing aşırı ısı: anlık sealer kapatma *)
IF GVL_IO.rSealTemp_C > GVL_Params.rSealTemp_MaxLimit_C THEN
    GVL_IO.xSealerOut           := FALSE;
    GVL_Alarms.xSealOverTemp    := TRUE;
END_IF

(* Kritik alarm bütünleşik bayrağı *)
GVL_Alarms.xAnyCriticalAlarm :=
    GVL_Alarms.xEStopActive       OR
    GVL_Alarms.xDoorOpenAlarm     OR
    GVL_Alarms.xSealOverTemp;
```

### Örnek 7: Servo/Motion Girişi — MC_MoveAbsolute ile Konumlama

CODESYS SoftMotion PLCopen Motion Control Function Block'ları kullanılır. (Kaynak: CODESYS SoftMotion Data Sheet)

```iecst
(* FB_ServoPositioner — MC_MoveAbsolute ile sealing pozisyonuna git *)
FUNCTION_BLOCK FB_ServoPositioner
VAR_INPUT
    xMoveCmd        : BOOL;
    rTargetPos_mm   : REAL;
    rVelocity       : REAL := 100.0;  (* mm/s *)
    rAcceleration   : REAL := 500.0;
END_VAR
VAR_OUTPUT
    xAtTarget       : BOOL;
    xFault          : BOOL;
    rActualPos_mm   : REAL;
END_VAR
VAR
    mcPower         : MC_Power;
    mcMoveAbs       : MC_MoveAbsolute;
    mcReadActPos    : MC_ReadActualPosition;
    fbAxis          : AXIS_REF;     (* Fiziksel eksen referansı *)
    rtMoveCmd       : R_TRIG;
END_VAR

(* Eksen güç *)
mcPower(
    Axis    := fbAxis,
    Enable  := GVL_IO.xAxisEnable,
    bRegulatorOn := TRUE
);

(* Mevcut pozisyonu oku *)
mcReadActPos(
    Axis    := fbAxis,
    Enable  := TRUE
);
rActualPos_mm := mcReadActPos.Position;

(* Komut gelince hedefe git *)
rtMoveCmd(CLK := xMoveCmd);
IF rtMoveCmd.Q THEN
    mcMoveAbs(
        Axis         := fbAxis,
        Execute      := TRUE,
        Position     := rTargetPos_mm,
        Velocity     := rVelocity,
        Acceleration := rAcceleration,
        Deceleration := rAcceleration
    );
END_IF

xAtTarget := mcMoveAbs.Done;
xFault    := mcMoveAbs.Error OR mcPower.Error;
```

---

## Sık Yapılan Hatalar

### Hata 1: Sealing Süresini Sabit Koymak

```iecst
(* ❌ Yanlış: Sealing süresi kod içinde sabit *)
tSealTimer(IN := xSealStart, PT := T#800MS);

(* ✅ Doğru: Aktif reçeteden oku *)
tSealTimer(IN := xSealStart, PT := GVL_Params.stActiveRecipe.tSealTime);
```

Farklı ürün boyutları farklı sealing süresi gerektirir. Sabit değer, ürün değişiminde kod değişikliği anlamına gelir; bu hem tehlikeli hem de gereksiz.

### Hata 2: Güvenlik Mantığını Ana Sekansa Gömmek

```
❌ Yanlış: E-stop kontrolünü PRG_MainSequence'in CASE içine yazmak
   → Task_Control'ün watchdog hatası durumunda E-stop çalışmaz
   → Ana döngü meşgul iken E-stop gecikmeli tepki verir

✅ Doğru: PRG_Safety, ayrı Task_Safety (Prio:0, 5ms) içinde
   → Runtime'dan bağımsız, deterministik tepki
   → Ana mantık hatalı olsa da güvenlik katmanı çalışır
```

### Hata 3: Reçete Yüklemesini Üretim Sırasında Yapmak

Aktif sealing döngüsü sırasında reçete parametreleri değiştirilirse `tSealTime` değeri aniden değişir ve ürün yanabilir veya ambalaj kapanmaz. Kural:

```iecst
(* Reçete yükleme: YALNIZCA Idle durumda *)
IF xLoadCmd AND (eCurrentStep = ePack_Idle) THEN
    GVL_Params.stActiveRecipe := GVL_Recipes.aRecipes[nIdx];
END_IF
```

### Hata 4: Foto-Sensör Sinyalini Filtrelemeden Kullanmak

Yüksek hızlı konveyörde titreşim, ambalaj kenarından yansıma veya yüzey parlaklığı sahte tetiklemeler üretir. 20ms debounce filtresi bu durumu ortadan kaldırır.

```iecst
(* ❌ Ham sinyal: sahte tetikleme riski *)
IF GVL_IO.xProductSensor_Raw THEN
    eCurrentStep := ePack_Position;
END_IF

(* ✅ TON filtreli: 20ms kararlı olunca geçer *)
tDebounce(IN := GVL_IO.xProductSensor_Raw, PT := T#20MS);
IF tDebounce.Q THEN
    eCurrentStep := ePack_Position;
END_IF
```

### Hata 5: OEE Verilerini RETAIN Olmayan Değişkende Tutmak

Güç kesilmesi veya soğuk başlangıçta üretim sayaçları sıfırlanır; vardiya OEE hesabı bozulur.

```iecst
(* ✅ Doğru: RETAIN ile güç kesintisine dayanıklı *)
VAR_GLOBAL RETAIN
    dwTotalPackCount    : DWORD;
    dwGoodPackCount     : DWORD;
    tTotalDowntime      : TIME;
    dtLastShiftStart    : DATE_AND_TIME;
END_VAR
```

### Hata 6: Servo Eksenini Hata Sonrası Resetlemeden Çalıştırmak

MC_MoveAbsolute bir `Error` verdiğinde eksen hatalı konumda kalır. Hata reset edilmeden tekrar `Execute := TRUE` verilirse eksen beklenmedik harekete geçer.

```iecst
(* Hata reset iş akışı *)
IF mcMoveAbs.Error AND xFaultReset THEN
    mcReset(Axis := fbAxis, Execute := TRUE);
END_IF
```

### Hata 7: SFC Transition'ında Çıkış Atama Yapmak

```iecst
(* ❌ Yanlış: Transition içinde aksiyon — derlenir ama davranış tanımsız *)
T_FeedToSeal:
    GVL_IO.xConveyorOut := FALSE;  (* BU YANLIŞ *)
    xItemDetect AND xAtPosition;

(* ✅ Doğru: Transition sadece boolean koşul; çıkış ataması Step_Feed Exit aksiyonunda *)
T_FeedToSeal: xItemDetect AND xAtPosition;
```

---

## Ne Zaman Tercih Edilmeli / Edilmemeli

### SFC Tercih Edin — Paketleme Sekansı İçin

- 5+ adımlı, açık sıralı döngü varsa
- Saha ekibinin online debug sırasında hangi adımda olduğunu görmesi gerekiyorsa
- ISA-88 / PackML uyumu isteniyorsa
- Paralel sealing ve besleme dalları varsa (SFC OR/AND dallanması)

### CASE State Machine (ST) Tercih Edin

- 3-4 adımlı basit döngü (SFC gereksiz ağır)
- FB içine gömülü durum makinesi (örn. FB_SealingJaw kendi state machine'ini ST ile yönetir)
- Kütüphaneye alınacak, taşınabilir kod

### Servo/Motion Ekleyin

- 0.1mm altı konumlama hassasiyeti gerekiyorsa
- Ürün boyutuna göre stroke değişiyorsa (reçete bağımlı)
- Çoklu eksen senkronizasyonu gerekliyse (sealing çenesi + film sürme)

### Basit Pnömatik Yeterli Olduğunda Servo Eklemeyin

- Konum sabit (iki nokta: geri + ileri)
- Hız değişimi gerekmiyorsa
- Maliyet kısıtı varsa — limit switch + TON kombinasyonu yeterlidir

---

## Gerçek Proje Notları

**Not 1 — Sealing Süresi Toleransı Pratikte Nasıl Belirlenir**  
Sealing süresi, ürün ve ambalaj malzemesine bağlı olarak üretici spesifikasyonundan okunur (genellikle ±%10 tolerans). İlk devreye almada 5 adet prototip paket üretilip sealing kalitesi fiziksel olarak test edilir; süre ürün yanıyor → kısa, ambalaj açılıyor → uzun şeklinde iterate edilir. Bu test değeri aktif reçeteye kaydedilir ve onaylanmadan değiştirilemez hale getirilir (HMI seviye koruması).

**Not 2 — SFC Online Görünürlüğünün Değeri**  
Gerçek proje: Sealing hattında intermittent durdurma sorunu. CODESYS SFC online modda `Step_Sealing`'in aktif kaldığı görüldü — sealing FB'nin `xSealComplete` çıkışı hiç gelmiyordu. Sorun: sıcaklık sensörü kablo kopukluğu nedeniyle `xTempOK` FALSE kalıyordu, `eSeal_Heating` durumu beklemeye devam ediyordu. SFC görünümü olmadan bu arıza saatler alırdı; 20 dakikada çözüldü.

**Not 3 — Reçete Yönetiminde Array of STRUCT Tuzağı**  
CODESYS Recipe Manager, STRUCT dizileri yüklerken zaman zaman bazı indeksleri atlar (bilinen forum sorunu — kaynak: forge.codesys.com). Üretim projesinde reçete tablosu `ARRAY[1..20] OF ST_Recipe` olarak PERSISTENT GVL'de tutuldu; Recipe Manager yalnızca dosya export/import için kullanıldı. Aktif reçete geçişi tamamen kod içinde yönetildi. Bu yaklaşım hem güvenilir hem de HMI ile kolayca entegre edilebilir.

**Not 4 — OEE Hesabında "Planlanan Süre" Tanımı**  
OEE hesabında en sık yapılan hata: planlanan sürenin yanlış hesaplanması. Mola süreleri, planlı bakım, setup süreleri "planlanan" süreden çıkarılmalı mı? Standart (oee.com) bunları "Planned Downtime" olarak planlanan süreden dışlar. CODESYS'teki FB_OEECalculator'da `tPlannedTime` parametresi HMI'dan operatör tarafından girilen "vardiya süresinden planlı duruşlar düşüldükten sonra kalan" değer olarak tanımlanmalıdır. Aksi hâlde OEE değeri sistematik olarak düşük hesaplanır.

**Not 5 — PackML Durum İsimlerini SCADA'ya Yansıtmak**  
OPC UA üzerinden SCADA'ya bağlanan sistemlerde `eCurrentStep` enum değeri `GVL_HMI.nMachineState` olarak INT'e çevrilerek yayınlanır. Ancak PackML standart state numaralarını (Stopped=2, Idle=4, Running=6 vb.) kullanır. SFC step adlarını PackML ile eşleştirip doğru INT değerini GVL_HMI'ya yazmak SCADA entegrasyonunu standartlaştırır. Bu 15 satırlık bir ST programıdır ama aylarca sürebilecek SCADA entegrasyon sorunlarını önler.

**Not 6 — Foto-Sensör Seçimi: Tür Farkı**  
Gıda paketlemede ışıngeçişli (through-beam) sensörler diffüz sensörlere göre daha az sahte tetikleme üretir; ancak karşılıklı montaj gerektirir. Şeffaf ambalaj malzemeleri diffüz sensörü yanıltabilir — bu durumda polarize retroreflektif veya kapasitif sensör tercih edilir. PLC kodu fark etmez ama sensör seçimi sistem güvenilirliğini doğrudan etkiler.

**Not 7 — Reçete Değişiminin "Yumuşak" Olmaması: İlk Döngü Sürprizi**  
Reçete yalnızca `ePack_Idle`'da yükleniyordu (doğru), ancak `stRecipe` FB'ye VAR_INPUT olarak her cycle kopyalanıyordu. Operatör Idle anında reçeteyi değiştirdi; aynı cycle'da makine `ePack_Feed`'e geçti ama besleme gecikmesi eski reçeteden, sealing süresi yeni reçeteden okundu — karışık parametre. İlk paket yanlış mühürlendi. Çözüm: reçete bir bütün olarak `Idle→Feed` geçişinde tek bir lokal kopyaya alındı (`stRunningRecipe := stRecipe`), döngü boyunca bu lokal kopya kullanıldı. Ders: bir parti boyunca parametreler "donmuş" olmalı; canlı GVL referansı değil, döngü başında alınan snapshot kullanılmalı (RETAIN/PERSISTENT snapshot deseni).

**Not 8 — SFC Time-Limit (Step Watchdog) ile Sessiz Takılmaların Yakalanması**  
Bir hatta `Step_Position` bazen sonsuza kadar aktif kalıyordu (servo enkoder kablosu intermittent). Operatör makinenin "çalışıyor ama hiçbir şey yapmıyor" olduğunu fark etmiyordu çünkü hata bayrağı yoktu. Çözüm: CODESYS SFC'nin step time-monitoring özelliği (`Step.t` zaman değişkeni veya SFCError bayrağı) kullanıldı — her step için maksimum süre tanımlandı, aşılırsa `SFCError` TRUE oldu ve sistem `Step_Aborting`'e zorlandı. Ders: her bekleme adımının bir timeout'u olmalı; "transition koşulu hiç gelmezse" senaryosu daima tasarlanmalı (FB_PackagingMachine'deki `tFeedTimeout` bunun ST karşılığıdır).

**Not 9 — OEE Performans Faktörünün 1.0'ı Aşması**  
FB_OEECalculator sahada `rPerformance = 1.07` (>%100) raporladı; SCADA "imkansız" diye alarm verdi. Neden: `rIdealCycleTime` reçeteye konservatif (gerçekten yavaş) girilmişti, makine bundan hızlı çalıştı. Matematiksel olarak doğru ama OEE tanımına aykırı. Çözüm: `rPerformance := MIN(rPerformance, 1.0)` ile kapandı ve ideal cycle time, gözlenen en hızlı kararlı cycle'a göre yeniden kalibre edildi. Ders: OEE faktörleri 0.0–1.0 aralığında clamp edilmeli; >1.0 değer her zaman bir veri/parametre hatasının işaretidir.

---

## Edge Case'ler ve Sistem Limitleri

### Sınır Koşulları Tablosu

| Senaryo | Davranış | Doğru Tasarım |
|---------|----------|---------------|
| Transition koşulu hiç gelmez | Step sonsuza aktif, sessiz takılma | Her adıma timeout (tFeedTimeout / SFC step time-limit) |
| Reçete Idle'da değişti, aynı cycle Feed | Karışık parametre, ilk paket bozuk | Döngü başında stRunningRecipe snapshot |
| `rIdealCycleTime` çok konservatif | rPerformance > 1.0 (imkansız OEE) | MIN(faktör, 1.0) clamp |
| Foto-sensör chatter (şeffaf ambalaj) | Sahte ürün tespiti, sayaç şişer | 20 ms TON debounce + sensör türü seçimi |
| Sealing ısıya 10 s'de ulaşmaz | eSeal_Heating'de fault (DOĞRU) | tTempTimeout zorunlu — ısıtıcı/sensör arızası yakalanır |
| `nBatchTarget = 0` | Sayaç ilk cycle'da hedefi geçer, hemen Idle | nBatchTarget > 0 validasyonu reçete yüklemede |
| Servo MC error sonrası tekrar Execute | Eksen beklenmedik hareket | MC_Reset zorunlu, sonra Execute |
| Güç kesintisi parti ortasında | RETAIN yoksa sayaç sıfırlanır | dwPackCount RETAIN; aktif step PERSISTENT değil |

### Sayısal ve Zamanlama Limitleri

```
TON çözünürlüğü = task cycle (10 ms task → ±10 ms hata)
  Sealing 500–2000 ms : ±10 ms = %0.5–2 → kabul edilebilir
  Ejeksiyon ±20 ms tolerans : 10 ms task sınırda → 5 ms task gerekebilir
  ❌ Çok kritik zamanlama (<5 ms) → donanım çıkış karşılaştırma / HSC kullan

Reçete dizisi : ARRAY[1..20] OF ST_Recipe
  PERSISTENT alan boyutu sınırlı (cihaz NVRAM kapasitesi)
  ST_Recipe büyürse (STRING(40) + REAL'ler) toplam PERSISTENT taşabilir
  ✅ Reçete sayısı × struct boyutu < cihaz persistent limiti

OEE faktörleri : her biri 0.0..1.0
  rOEE = A × P × Q → teorik max 1.0
  >1.0 görülürse parametre hatası (her zaman)
```

### Hata Senaryosu — Sealing Sırasında Stop

Operatör `ePack_Sealing` aktifken Stop'a bastı. Kod `xSealerCmd := FALSE; eState := ePack_Idle` yapar. Ancak ısıl sealing çenesi ürüne **temas halinde** ve sıcak; aniden Idle'a dönmek çeneyi açık bırakırsa ürün yanmaya devam eder. Bu yüzden FB_SealingJaw kendi state machine'inde `eSeal_Opening` adımına sahiptir — stop, çenenin kontrollü açılmasını tetiklemeli, anlık kesme değil. Güvenlik katmanı (PRG_Safety, Task_Safety 5 ms) ise sealer'ı **anlık** keser; ikisi farklı amaçlar için ayrılmıştır: normal stop kontrollü, güvenlik stop'u anlıktır (IEC 60204-1 Kategori 1 vs 0 ayrımının paketleme karşılığı).

## Optimizasyon

### SFC vs Büyük CASE — Hangi Durumda Hangisi Hızlı?

SFC çalışma zamanı her cycle yalnızca **aktif** step'in aksiyonunu ve çıkış transition'larını değerlendirir; pasif step'ler taranmaz. Büyük CASE'de ise her cycle CASE değişkeni tek seferde dallanır (jump table) — ikisi de O(1)'e yakındır. Asıl fark teşhiste: SFC online görünürlüğü saha teşhisini hızlandırır (Not 2), ama derin iç-içe FB durum mantığı için CASE daha taşınabilir. Kural: ana sekans SFC (görünürlük), FB-içi alt durum CASE (kütüphane/taşınabilirlik).

```
Optimizasyon kuralı (kaynak: codesys/task-structure/_synthesis.md):
  Task_Safety  5 ms  Prio:0  → sadece BOOL interlock (E-stop, kapı, ısı)
  Task_Control 10 ms Prio:2  → SFC ana sekans + FB çağrıları
  Task_Slow    100ms Prio:5  → OEE (REAL bölme/çarpma), HMI
  Task_Log     FW    Prio:15 → dosya yazma (bloklanabilir I/O)
```

### OEE Hesabını Olay-Tetiklemeli Yapma

OEE her cycle hesaplanmaz; yalnızca `xCycleDone` pulse'ında (her tamamlanan pakette) veya vardiya sonunda güncellenir. Her 10 ms'de REAL bölme yapmak boşa FPU yükü demektir. `FB_OEECalculator` 100 ms Task_Slow'da veya event task'ta koşmalı.

| İşlem | Frekans | Task |
|-------|---------|------|
| Sealing/ejeksiyon TON | Her cycle | Task_Control 10 ms |
| OEE REAL hesabı | Pakette bir / 1 s | Task_Slow / event |
| Üretim logu dosya yazma | Vardiya / dolunca | Task_Log Freewheel |
| Reçete dosya I/O | Operatör komutu | Event task (asla cyclic'te) |

### Foto-Sensör Debounce'unu Ürün Hızına Uyarlama

Sabit 20 ms debounce, yüksek hızlı hatta (ürünler 30 ms arayla) iki ürünü tek ürün sayabilir veya geçiş penceresini kaçırabilir. Debounce süresi `< minimum ürün-arası süre` olmalı. Optimizasyon: debounce'u reçeteden (hat hızına bağlı) parametrele; çok hızlı hatlarda yazılım debounce yerine sensörün donanım filtresi (response time ayarı) kullanılmalı — yazılım her zaman cycle çözünürlüğüyle sınırlıdır.

## Derin Teknik Detay

### SFC Step Belleği ve "Initial Step" Mantığı

CODESYS SFC, her step için bir aktiflik bayrağı (`Step.x`) ve bir aktiflik süresi (`Step.t`) tutar. Bu, IEC 61131-3'ün SFC'yi bir token akış modeli olarak tanımlamasından gelir: token (etkinlik) initial step'te başlar, transition koşulu TRUE olunca bir sonraki step'e **geçer** ve önceki step'in token'ı silinir. Bu yüzden iki step'in aynı anda aktif olması (paralel dal hariç) bir hatadır ve SFC runtime bunu yakalar. Büyük CASE state machine'de bu garanti yoktur — programcı `eState`'i yanlışlıkla iki yere atayabilir. SFC'nin değeri tam da bu yapısal token garantisidir: "makine her an tam olarak bir durumdadır" kuralı dilin kendisi tarafından zorlanır. PackML'in 17 durumu bu yüzden SFC'ye doğal oturur — her PackML durumu tam bir token konumudur.

### Neden Sealing Süresi Reçeteden, Kodda Sabit Değil?

Sealing termodinamiği malzeme bağımlıdır: ısıl yapışma (heat seal) süresi, film kalınlığı, çene sıcaklığı ve basıncın bir fonksiyonudur (Arrhenius-tipi difüzyon). Aynı makine 50µm PE film ile 120µm laminat arasında geçtiğinde optimal süre 2–3 kat değişir. Süreyi koda gömmek, ürün değişiminde **kod değişikliği + yeniden derleme + indirme** demektir — bu hem üretim kaybı hem de validasyon riski (gıda/ilaçta her kod değişikliği yeniden doğrulama gerektirir). Reçeteyi PERSISTENT GVL'de tutmak, parametreyi koddan ayırarak ürün geçişini bir HMI seçimine indirger. Bu, "veri ile kodun ayrılması" ilkesinin paketlemedeki en somut örneğidir ve doğrudan GVL/RETAIN/PERSISTENT katman ayrımıyla bağlanır.

### RETAIN vs PERSISTENT — Paketlemede Net Ayrım

| Veri | Tip | Neden |
|------|-----|-------|
| Üretim sayacı (dwPackCount) | RETAIN | Güç kesintisinde korunmalı; download'da sıfırlanabilir (yeni vardiya) |
| OEE birikimleri | RETAIN | Vardiya boyunca güç kesintisine dayanıklı |
| Reçete tablosu (aRecipes) | PERSISTENT | Program güncellemesinde bile korunmalı |
| Kalibrasyon ofsetleri | PERSISTENT | Donanım sabiti; koddan tamamen bağımsız |
| Aktif step (eCurrentStep) | Hiçbiri | Güç gelince makine GÜVENLİ başlamalı (Idle), kaldığı yerden DEĞİL |

Kritik tasarım kararı son satırdadır: aktif step'i RETAIN yapmak tehlikelidir. Güç kesilip geldiğinde makine `ePack_Sealing`'den devam ederse, çene konumu/ürün durumu belirsizken sealer çalışır. Güvenli ilke: makine durumu **uçucu** olmalı, güç gelince daima bilinen güvenli durumdan (Idle) başlamalı. Bu, RETAIN'in "her şeyi sakla" diye düşünülmemesi gerektiğinin kanıtıdır — saklananın güç sonrası anlamı sorgulanmalıdır.

## İlgili Konular

```
knowledge/codesys/fundamentals/
└── 03_iec61131_languages.md  → SFC ve CASE state machine, FB_PackagingMachine örneği

knowledge/codesys/task-structure/
└── _synthesis.md             → Şablon A: basit makine task mimarisi

knowledge/codesys/programming/
└── _synthesis.md             → FB tasarımı, GVL yapısı, hata yönetimi

knowledge/applications/
├── conveyor/README.md        → Besleme konveyörü implementasyonu
├── motor-control/README.md   → Motor FB tasarım prensipleri
└── tank-level/README.md      → Analog sensör ve PID döngüsü

(Planlanan — henüz belge yok)
knowledge/standards/
├── isa88_batch.md            → ISA-88 tam implementasyon rehberi
└── packml.md                 → PackML durum modeli CODESYS şablonu

knowledge/codesys/advanced/
└── softmotion_basics.md      → MC_MoveAbsolute, MC_Power, AXIS_REF
```
