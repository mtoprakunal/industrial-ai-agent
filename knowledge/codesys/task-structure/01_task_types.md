---
KONU        : CODESYS Task Tipleri
KATEGORİ    : codesys
ALT_KATEGORI: task-structure
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_f_reference_task.html"
    başlık: "CODESYS Online Help — Task Configuration Reference"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_freewheeling_iec_task.html"
    başlık: "CODESYS Online Help — Freewheeling IEC Task"
    güvenilirlik: resmi
  - url: "https://forge.codesys.com/forge/talk/Runtime/thread/e8a4d63391/"
    başlık: "CODESYS Forge — Freewheeling vs Cyclic Task"
    güvenilirlik: topluluk
  - url: "https://www.plctalk.net/forums/threads/cyclic-task-vs-free-wheeling.137925/"
    başlık: "PLCtalk — Cyclic Task vs Freewheeling (Gerçek Proje Tartışması)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "02_cycle_time.md"
    ilişki: tamamlar
  - konu: "03_priority_management.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "CODESYS runtime ve scan cycle kavramı (fundamentals/01_runtime_architecture.md)"
  - "Task Configuration objesi nedir (fundamentals/02_project_structure.md)"
ÇELİŞKİLER :
  - kaynak: "CODESYS Forge topluluk tartışmaları"
    konu: "Freewheeling mi Cyclic mi — ana görev için hangisi tercih edilmeli?"
    çözüm: >
      Siemens kökenli mühendisler Freewheeling'e (OB1 mantığına) eğilirken,
      Rockwell kökenli mühendisler Cyclic'i tercih eder. PID, motion veya
      zamana bağlı herhangi bir hesaplama yapılıyorsa Cyclic zorunludur.
      Saf boolean kontrol mantığı için Freewheeling kabul edilebilir ancak
      Cyclic'in öngörülebilirlik avantajı çoğu projede onu üstün kılar.
  - kaynak: "CODESYS resmi dökümantasyon"
    konu: "Status vs Event tetikleme farkı sık karıştırılır"
    çözüm: >
      Status: Koşul TRUE olduğu sürece her scheduler döngüsünde task çalışır.
      Event: Yalnızca FALSE→TRUE geçişinde (yükselen kenar) bir kez tetiklenir.
      Yanlış tip seçimi, task'ın ya hiç çalışmamasına ya da sürekli çalışmasına neden olur.
---

## Özün Ne

CODESYS'te bir task'ın ne zaman ve nasıl tetikleneceği, "task tipi" ile belirlenir. Yanlış tip seçimi; bir task'ın hiç istenen sıklıkta çalışmamasına, CPU'yu gereksiz tüketmesine ya da PID gibi zamana bağlı hesaplamaların bozulmasına yol açar. CODESYS beş task tipi sunar: **Cyclic** (zamanlı), **Freewheeling** (mümkün olan en hızlı), **Event** (değişken kenarıyla tetiklenen), **Status** (koşul tabanlı) ve harici donanım interrupt'ına bağlı **External Event**. Her birinin doğru kullanım alanı vardır ve bunlar birbirinin yerine geçemez.

## Nasıl Çalışır

### Genel Tetiklenme Mekanizması

CODESYS scheduler'ı belirli bir çözünürlükte (`SchedulerInterval`, varsayılan 1ms) döngü yapar. Her döngüde hangi task'ın çalışması gerektiğini kontrol eder; çalışması gereken task varsa öncelik sıralamasına göre çalıştırır.

```
Scheduler (1ms döngü)
│
├── Task_Motion  (Cyclic, 1ms, Prio:0)   → Her döngüde çalışır
├── Task_Main    (Cyclic, 10ms, Prio:1)  → Her 10 döngüde bir çalışır
├── Task_Comm    (Freewheeling, Prio:10) → Boşta CPU varsa çalışır
└── Task_Alarm   (Event: xAlarmBit, Prio:2) → xAlarmBit yükselen kenarında çalışır
```

### Tip 1: Cyclic (Zamanlı)

Sabit bir zaman aralığıyla tekrar eden task. `Interval` parametresiyle belirlenir.

```
Zaman: 0ms     10ms    20ms    30ms    40ms
       │        │       │       │       │
Task   █░░░░░░░░█░░░░░░░█░░░░░░░█░░░░░░░█
       └──run──┘└──idle─┘└──run─┘

█ = çalışıyor   ░ = bekliyor
```

**Temel özellikler:**
- Öngörülebilir zamanlama — PID, motion, zaman tabanlı hesaplamalar için zorunlu
- Yürütme süresi `Interval`'ı aşarsa watchdog tetiklenir
- CPU yük garantisi: Kod ne kadar hızlı çalışırsa çalışsın, bir sonraki döngüye kadar bekler
- Fazla CPU tüketmez; `Interval` ile kapasite yönetimi yapılır

**Ne zaman kullanılır:**
- Herhangi bir türev veya integral hesabı (PID, ramp)
- Motion task (EtherCAT sync cycle ile eşleştirilir)
- Güvenlik ve acil durum mantığı
- Pratikte neredeyse tüm kontrol task'ları

---

### Tip 2: Freewheeling (Serbest Döngü)

Cycle time tanımı yoktur. Bir önceki çalışma biter bitmez kısa bir sistem gecikmesinin ardından hemen yeniden çalışır. Klasik donanım PLC'deki tek scan döngüsüne (Siemens OB1) en yakın task tipidir.

```
Zaman: →→→→→→→→→→→→→→→→→→→→→→→→→→→
Task   ████░████░████░████░████░████
       └run┘ └─bekleme─┘└run┘

Bir önceki çalışma süresine orantılı kısa bekleme — düzensiz aralıklar
```

**Temel özellikler:**
- Cycle time garanti edilmez; kod ne kadar uzun sürer, o kadar uzar
- CPU'yu maksimum kullanır; başka düşük öncelikli task'lara nefes aldırmaz
- Bekleme süresi, son çalışma süresinin bir yüzdesidir (otomatik hesaplanır)
- Watchdog tanımlanabilir ancak cycle time referansı olmadığı için sadece maksimum süre sınırı koyar

**Ne zaman kullanılır:**
- Arka planda CPU boşaltma amaçlı iletişim task'ları
- Düşük öncelikli log ve diagnostik görevler
- EtherCAT veya fieldbus yoksa ve zamanlama gereksinimleri gevşekse
- Siemens OB1'den geçiş yapan ekipler için geçici adaptasyon

**Ne zaman kullanılmamalı:**
- PID veya herhangi bir zaman türevli hesaplama içeren mantık
- Fieldbus (EtherCAT, PROFINET, CANopen) ile senkronize çalışan task
- Gerçek zamanlılık garantisi gerektiren herhangi bir kontrol döngüsü

---

### Tip 3: Event (İç Olay — Değişken Kenarı)

Global bir BOOL değişkeninin **yükselen kenarında** (FALSE → TRUE geçişi) tetiklenir. Tetiklenmeden önceki tüm scan döngülerinde hiç çalışmaz.

```
xTriggerVar: 0 0 0 0 0 1 1 1 1 0 0 0 1 1 0
Task:                   █               █
                        └── tek çalışma ┘
```

**Temel özellikler:**
- Kenar tetiklemeli: Koşul sürekli TRUE olsa bile yalnızca geçiş anında çalışır
- Scheduler çözünürlüğü kritik: Scheduler 1ms döngü yapıyorsa 1ms'den kısa süreli pulslar kaçırılabilir
- Aşırı tetiklenme (6 event/ms üzeri bazı platformlarda) runtime'ı HALT durumuna geçirebilir
- Görece nadir ihtiyaç duyulur; çoğu senaryoda Cyclic task içinde kenar algılama daha güvenilirdir

**Ne zaman kullanılır:**
- Nadir ancak kritik olaylar: alarm tetikleme, reçete yükleme komutu
- Başka bir task'ın veya dış sistem tetikleyicisinin işaret verdiği eylemler
- Yüksek öncelikli kısa süreli işlemler (etiket yazma, log kaydı)

---

### Tip 4: Status (Durum Tabanlı)

Bir BOOL değişkeninin değeri TRUE olduğu **her** scheduler döngüsünde çalışır. Event'ten farkı: kenar değil, seviye tetiklemesidir.

```
xCondition:  0 0 0 1 1 1 1 1 0 0 1 1 0 0
Task:                █ █ █ █ █       █ █
                     └─sürekli çalışır─┘
```

**Ne zaman kullanılır:**
- Belirli bir makine durumunda (ör. alarm aktifken) sürekli çalışması gereken ek kontrol mantığı
- Ana Cyclic task'ın yanında koşula bağlı yardımcı işlemler

**Dikkat:** Koşul sürekli TRUE kalırsa bu task scheduler her döngüsünde çalışmaya devam eder; yüksek CPU yüküne neden olabilir.

---

### Tip 5: External Event (Harici Kesme)

Donanım interrupt'ına (encoder Z-pulse, yüksek hız sayaç, harici sinyal) bağlı tetiklenme. Scheduler döngüsünü beklemeden donanım seviyesinde tetiklenir.

**Ne zaman kullanılır:**
- Mikrosaniye hassasiyeti gerektiren encoder referans izi algılama
- Donanım timer interrupt'ı ile senkronize hareket başlatma
- Çok sınırlı kullanım alanı — destekleyen platform ve donanım gerektirir

---

### Task Tipi Karar Şeması

```
Yeni bir task tanımlıyorum. Hangi tipi seçmeliyim?
│
├─► Sabit zaman aralığı gerekiyor mu?
│   ├── Evet → Cyclic
│   └── Hayır
│       │
│       ├─► Bir değişken değişince mi çalışmalı?
│       │   ├── Yükselen kenarda bir kez → Event
│       │   ├── Koşul TRUE olduğu sürece → Status
│       │   └── Donanım interrupt'ı → External Event
│       │
│       └─► Ne kadar hızlı olursa o kadar iyi mi?
│           ├── Evet, CPU boş kaldıkça çalışsın → Freewheeling
│           └── (Dikkat: PID/motion içeriyorsa → Cyclic'e dön)
```

## Pratikte Nasıl Kullanılır

### Task Tipi Yapılandırması (IDE)

```
Task Configuration → MainTask (çift tıkla) → Configuration sekmesi
    Type: Cyclic
    Interval: t#10ms
    Priority: 1
    Watchdog: ✓ Enabled
    Watchdog Time: t#50ms
    Sensitivity: 3
```

**Sensitivity nedir?** Watchdog tetiklenmesi için task'ın arka arkaya kaç döngü boyunca watchdog süresini aşması gerektiğidir. `Sensitivity = 3` ile tek seferlik spike watchdog'u tetiklemez; 3 ardışık ihlalde tetiklenir.

### Gerçek Projede Task Tipi Dağılımı

```
Makine Türü: Konveyörlü Paketleme Hattı
─────────────────────────────────────────────────────
Task_Safety      Cyclic  1ms  Prio:0  → E-stop, güvenlik izleme
Task_Motion      Cyclic  2ms  Prio:1  → SoftMotion, EtherCAT sync
Task_Control     Cyclic 10ms  Prio:2  → Konveyör, PID, sensör
Task_HMI         Cyclic 50ms  Prio:5  → HMI değişken güncelleme
Task_DataLog   Freewheel    Prio:15   → USB log yazma, diagnostik
Task_Recipe      Event  xLoadRecipe   → Reçete yükleme (nadir tetik)
```

## Örnekler

### Örnek 1: Cyclic Task ile PID — Neden Freewheeling Olmaz

```iecst
(* Task_Control: Cyclic, t#10ms *)
PROGRAM PRG_TemperatureControl
VAR
    fbPID      : FB_PID;
    tCycleTime : TIME := T#10MS;  (* Task cycle time ile eşleşmeli *)
END_VAR

fbPID(
    fActualValue   := GVL_IO.rTemperature,
    fSetpointValue := GVL_Params.rTempSetpoint,
    fCycleTime     := 0.010,   (* 10ms — Cyclic task ile aynı, sabit *)
    fKp            := 1.2,
    fTi            := 5.0,
    fTd            := 0.1
);

(* Eğer Freewheeling kullansaydık:
   fCycleTime değişken olurdu: bazen 8ms, bazen 15ms.
   PID integral birikimi hatalı hesaplanır → salınım → kararsızlık *)
```

### Örnek 2: Event Task ile Reçete Yükleme

```iecst
(* GVL_Commands içinde *)
VAR_GLOBAL
    xLoadRecipeCmd : BOOL;   (* HMI'dan event tetikleyici *)
END_VAR

(* Task_Recipe: Event triggered by GVL_Commands.xLoadRecipeCmd *)
PROGRAM PRG_LoadRecipe
VAR
    nRecipeID : INT;
END_VAR

(* Bu program yalnızca xLoadRecipeCmd FALSE→TRUE geçişinde çalışır *)
nRecipeID := GVL_HMI.nSelectedRecipe;
CASE nRecipeID OF
    1: (* Reçete 1 parametrelerini yükle *)
        GVL_Params.rTargetTemp  := 180.0;
        GVL_Params.rTargetSpeed := 45.0;
    2:
        GVL_Params.rTargetTemp  := 220.0;
        GVL_Params.rTargetSpeed := 30.0;
END_CASE

(* Komutu sıfırla — bir sonraki event için hazır *)
GVL_Commands.xLoadRecipeCmd := FALSE;
```

### Örnek 3: Freewheeling vs Cyclic — Zaman Farkını Görmek

```iecst
(* Freewheeling task içinde zaman ölçümü — değişken cycle time sorunu *)
PROGRAM PRG_MeasureCycleTime
VAR
    tLastCall  : TIME;
    tCurrent   : TIME;
    tMeasured  : TIME;   (* Her döngüde farklı değer! *)
END_VAR

tCurrent  := TIME();
tMeasured := tCurrent - tLastCall;
tLastCall := tCurrent;

(* Freewheeling'de tMeasured: 8ms, 12ms, 9ms, 15ms, 11ms... — tutarsız *)
(* Cyclic 10ms'de tMeasured: 10ms, 10ms, 10ms, 10ms... — kararlı     *)
```

### Örnek 4: Status Task ile Alarm Modu

```iecst
(* GVL_Status.xAlarmActive TRUE olduğu sürece bu task çalışır *)
(* Task_AlarmHandler: Status, triggered by GVL_Status.xAlarmActive *)

PROGRAM PRG_AlarmFlash
VAR
    tFlashTimer : TON;
    xFlashState : BOOL;
END_VAR

tFlashTimer(IN := NOT xFlashState, PT := T#500MS);
IF tFlashTimer.Q THEN
    tFlashTimer(IN := FALSE);
    xFlashState := NOT xFlashState;
END_IF

GVL_IO.xAlarmLight := xFlashState;
(* Alarm sona erdiğinde GVL_Status.xAlarmActive = FALSE → task duruyor *)
```

## Sık Yapılan Hatalar

### Hata 1: PID veya Ramp Hesabını Freewheeling Task'ta Yapmak

```
Semptom: Sıcaklık kontrolü salınım yapıyor, motor rampa düzgün çalışmıyor.
Neden  : Freewheeling cycle time değişken — integral birikiyor yanlış.
Çözüm  : PID ve ramp içeren her şey Cyclic task'ta olmalı.
```

### Hata 2: Event Task'ı Çok Sık Tetiklemek

```
Semptom: Runtime HALT durumuna geçiyor, log'da "ISR Count Exceeded".
Neden  : Event task saniyede 100+ kez tetikleniyor (ör. hızlı değişen sinyal).
Çözüm  : Yüksek frekanslı sinyaller için Event değil, Cyclic task + kenar
          algılama (R_TRIG bloğu) kullan.

(* Doğru yaklaşım *)
VAR
    fbRTrig : R_TRIG;
END_VAR
fbRTrig(CLK := xFastSignal);
IF fbRTrig.Q THEN
    (* Tetiklenme anında bir kez çalışır *)
END_IF
```

### Hata 3: Freewheeling Task'a Fieldbus Mantığı Koymak

```
Semptom: EtherCAT veya CANopen iletişimi düzensiz, frame kaçırıyor.
Neden  : Fieldbus sabit döngü gerektirir; Freewheeling bunu sağlayamaz.
Çözüm  : Fieldbus ile etkileşen tüm mantık mutlaka Cyclic task'ta olmalı.
          CODESYS resmi dökümantasyonu da bunu açıkça yasaklar.
```

### Hata 4: Status ile Event'i Karıştırmak

```iecst
(* Senaryo: Reçete yükleme komutu geldiğinde parametreleri bir kez güncelle *)

(* ❌ Yanlış — Status kullanmak *)
(* Task_Recipe: Status, triggered by xLoadCmd *)
(* xLoadCmd TRUE olduğu sürece her döngüde reçete tekrar tekrar yüklenir *)
(* Parametreler tutarsız hale gelebilir *)

(* ✅ Doğru — Event kullanmak *)
(* Task_Recipe: Event, triggered by xLoadCmd *)
(* Yalnızca FALSE→TRUE geçişinde bir kez çalışır *)
```

### Hata 5: Freewheeling'in "Daha Hızlı" Çalıştığını Sanmak

Yaygın yanılgı: "Freewheeling cycle time beklemediği için 10ms Cyclic'ten daha hızlı çalışır." Bu yalnızca kısmen doğrudur; gerçek tablo karmaşıktır.

```
Senaryo: Cyclic 10ms + Freewheeling aynı projede.
Gerçek : Cyclic task her 10ms'de kesinlikle çalışır.
         Freewheeling ise yalnızca Cyclic'in bıraktığı boşlukta çalışır.
         Eğer Cyclic CPU'nun %80'ini kullanıyorsa Freewheeling çok az çalışır.
         "Daha hızlı" değil, "boşta kalan zamanda" çalışır.
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

| Task Tipi | Tercih Et | Tercih Etme |
|---|---|---|
| **Cyclic** | PID, motion, fieldbus, güvenlik, her kritik kontrol | Gereksiz yere kısa interval (< gereksinimden) |
| **Freewheeling** | Log, diagnostik, düşük öncelikli arka plan | PID, motion, fieldbus, zaman hassas her şey |
| **Event** | Nadir tetiklenen komutlar (reçete, alarm reset) | Yüksek frekanslı sinyaller |
| **Status** | Belirli durumda sürekli çalışması gereken yardımcı mantık | Sürekli TRUE kalacak koşullar (CPU dolu olur) |
| **External Event** | Encoder Z-pulse, donanım kesme | Yazılım seviyesinde çözülmesi mümkün her şey |

## Gerçek Proje Notları

**Not 1 — Freewheeling'in PID'i Bozduğu Proje**  
Bir fırın sıcaklık kontrol projesinde ana task Freewheeling olarak yapılandırılmıştı. Fırın soğukken cycle time 8ms, fırın ısındıkça ve diğer sensörler devreye girdikçe cycle time 25ms'ye çıkıyordu. PID integral terimi bu değişken Δt ile yanlış hesaplandı; hedef sıcaklıkta ±15°C salınım oluştu. Task Cyclic 20ms'e değiştirildi, PID parametreleri sabit Δt=0.020 için yeniden ayarlandı; salınım ±1°C'ye indi.

**Not 2 — Event Task'ın Çok Tetiklenmesi**  
Bir konveyör hattında hız encoder sinyali Event task'a bağlanmıştı. Encoder 1000 pulse/devir üretiyordu; 300 RPM'de bu saniyede 5000 event demekti. Runtime "ISR Count Exceeded" hatasıyla HALT durumuna geçti. Çözüm: Encoder sayımı yüksek hızlı Cyclic task (1ms) içinde R_TRIG ile yapıldı, Event task tamamen kaldırıldı.

**Not 3 — Siemens'ten Gelenin Freewheeling Alışkanlığı**  
Siemens S7 kökenli bir mühendis, CODESYS projesinde tek bir Freewheeling task kullandı. Basit boolean kontrol için sorunsuz çalıştı. Sonra projeye EtherCAT eklenince drive'lar tutarsız hareket etti — Freewheeling'in belirsiz cycle time'ı EtherCAT sync sinyalini bozuyordu. Yeniden yapılandırma: EtherCAT task Cyclic 1ms, kontrol mantığı Cyclic 10ms, eski Freewheeling task'ı kaldırıldı.

**Not 4 — "Tek Task Her Şeyi Yapar" Yaklaşımı**  
Küçük projeler için tek Cyclic task yeterlidir. Ancak proje büyüyünce sorunlar başlar: Cycle time uzar, watchdog tetiklenir, kommunikasyon ve log görevleri kontrol döngüsünü etkiler. Başlangıçta en az iki task tasarlamak (hızlı kontrol + yavaş iletişim) ilerleyen aşamalarda büyük kolaylık sağlar.

**Not 5 — Event Task'ın "Kaybolan" Tetiklemeleri (Coalescing)**  
Bir alarm sisteminde Event task, alarm bitini her değişimde bir kez çalıştırması beklenerek tasarlandı. Ancak yoğun anlarda, scheduler interval'i (1ms) içinde bit hem TRUE hem FALSE olunca **kenar hiç görülmedi** — task tetiklenmedi. Event tetikleme, donanım interrupt'ı değildir; scheduler'ın bir sonraki taramasında bit'i örnekleyerek kenar arar. İki tarama arasındaki tüm geçişler "birleşir" (coalesce) ve tek bir net değişiklik gibi görünür. Ders: Event task yalnızca scheduler interval'inden **yavaş** değişen sinyaller için güvenilirdir. Hızlı/kısa pulslar için latch (set/reset bit) + Cyclic task kullanın.

**Not 6 — Freewheeling Task'ın Watchdog'u Yanıltıcı Olabilir**  
Bir log task'ı Freewheeling + watchdog 5s ile çalışıyordu. USB takılınca task 8 saniye bloke oldu ama watchdog'un beklenenden geç tetiklendiği görüldü. Neden: Freewheeling'de cycle time referansı olmadığı için watchdog yalnızca **mutlak maksimum süre** sınırı koyar; periyodik kontrol mantığı Cyclic'teki kadar keskin değildir. Üstelik tek bir task'ın watchdog'u tüm uygulamayı durdurur — log task'ı, çalışan üretim hattını durdurdu. Ders: Bloke olabilen I/O'yu Freewheeling'e koyarken bile, asıl koruma watchdog değil; non-blocking (state-machine tabanlı, parça parça) I/O tasarımıdır.

**Not 7 — External Event ile ISR İçinde IEC Kod Tuzağı**  
Yüksek hız sayaç kartı External Event task'ı tetikliyordu; geliştirici bu task'a 2ms süren bir hesap koydu. Donanım kesmesi 200µs'de bir geliyordu — task kendi tetiklenme aralığından uzun sürünce kesmeler birikip sistem kilitlendi. External Event task'ları kesme bağlamında (veya ona çok yakın öncelikte) çalışır; **mümkün olan en kısa, en deterministik kod** içermelidir (sadece sayaç oku/sakla). Ağır işlem ayrı bir Cyclic task'a devredilmelidir. Ders: External Event = "kısa kapt, hızlı çık".

## Edge Case'ler ve Sistem Limitleri

### Event Task Tetikleme Sınırları

```
Sınır                              Davranış / Limit
─────────────────────────────────────────────────────────────
Tetik aralığı < scheduler interval Kenar coalescing — geçişler kaybolur
Aşırı tetik (>~6 event/ms platforma) Runtime EXCEPTION/HALT ("ISR count")
Tetik bit'i task içinde resetlenmez Bir sonraki kenar için bit FALSE'a dönmeli
İki Event task aynı bit'e bağlı    Tetik sırası öncelik ile belirlenir
```

### Cyclic Task'ta "Interval'i Kaçırma" Davranışı

Bir Cyclic task'ın exec time'ı interval'i geçer ama watchdog'a varmazsa ne olur? CODESYS bir sonraki sürümlere/ayara göre iki strateji izleyebilir:

```
Strateji 1 (yaygın): Kaçırılan interval ATLANIR
  10ms task 13ms sürdü → 20ms'de bir sonraki çalışma (10ms'lik tetik kaybedildi)
  → Etkin frekans yarıya düşer, ama sistem stabil kalır

Strateji 2: Tetik BİRİKİR (catch-up)
  Kaçırılan döngüler kuyruğa girer → task ardışık çalışmaya çalışır
  → "ölüm sarmalı" riski: her döngü öncekinin gecikmesini büyütür
```

Pratikte birinci strateji baskındır, ama bunu **varsaymak** yerine Task Monitor'da `Cycle Count` ve gerçek frekansı doğrulayın.

### Status Task'ın Gizli CPU Açlığı

Status task, koşul TRUE kaldıkça **her scheduler döngüsünde** çalışır — yani 1ms scheduler'da TRUE bir koşul, etkin olarak 1ms Cyclic task'a dönüşür. Alarm modunda "geçici" sandığınız Status task, alarm saatlerce sürerse CPU'yu 1ms task gibi tüketir. Status task'ı pratikte nadiren doğru seçimdir; çoğu durumda Cyclic task + `IF xCondition` daha öngörülebilirdir.

### Task'lar Arası Ortak FB Instance Tuzağı

Aynı FB instance'ını (özellikle timer) **iki farklı task'tan** çağırmak tanımsız davranıştır: instance'ın iç durumu iki farklı zaman tabanında güncellenir, `.ET` anlamsızlaşır. Her timer/sayaç instance'ı tek bir task'a ait olmalıdır.

## Optimizasyon

### Task Tipi Seçiminin CPU Bütçesine Etkisi

```
Tip            CPU Profili                    Ne Zaman Tasarruf
──────────────────────────────────────────────────────────────────
Cyclic         Sabit, hesaplanabilir          Doğru interval ile minimum
Freewheeling   Kalan CPU'yu DOLDURUR (%100)   Düşük öncelikte → görünmez
Event          Sadece tetikte → çok ucuz      Nadir olaylar için ideal
Status         TRUE süresince Cyclic gibi      Kısa süreli koşullarda OK
External Event Kesme overhead'i + bağlam       Sadece µs gereksiniminde
```

**Anahtar içgörü:** Freewheeling task düşük öncelikte "ücretsiz" görünür çünkü kalan CPU'yu kullanır — ama yüksek öncelikte konursa CPU'yu tamamen yutar ve alt task'ları aç bırakır. Freewheeling = **daima en düşük öncelik**.

### Nadir İş için Event > Polling

Saniyede bir kez olan bir olayı 10ms Cyclic task içinde poll'lamak, saniyede 100 boş kontrol demektir. Event task aynı işi sıfır boş kontrolle yapar. Nadir, asenkron olaylarda (reçete yükleme, mod değişimi, manuel komut) Event task hem CPU hem de okunabilirlik kazandırır — yeter ki tetik sinyali scheduler interval'inden yavaş değişsin (Not 5).

### Sub-Sampling: Task Sayısını Azaltma Tekniği

Çok sayıda farklı hızda iş varsa, her biri için ayrı task açmak yerine tek Cyclic task içinde sayaç tabanlı alt-örnekleme yapın:

```iecst
(* Task_Control: Cyclic 10ms — birden çok hızı tek task'ta yönet *)
nDiv := nDiv + 1;
(* Her 10ms: hızlı mantık *)
FastLogic();
(* Her 100ms (10×10ms): orta mantık *)
IF (nDiv MOD 10) = 0 THEN MediumLogic(); END_IF
(* Her 1s (100×10ms): yavaş mantık *)
IF (nDiv MOD 100) = 0 THEN SlowLogic(); END_IF
```

Bu, context-switch overhead'ini ve race condition yüzeyini azaltır — 8 task yerine 2-3 task. Bedeli: tüm alt-mantık aynı öncelikte çalışır.

## Derin Teknik Detay

### Tetikleme Modellerinin Altyapısı

Beş task tipi aslında scheduler'ın tek bir karar döngüsünün farklı tetik kaynaklarıdır:

```
Scheduler her interval'de sorar: "Bu task şimdi çalışmalı mı?"
  Cyclic        → (now - last_run) >= interval ?
  Freewheeling  → önceki çalışma bitti + kısa bekleme doldu ?
  Event         → izlenen bit'te FALSE→TRUE kenarı var mı ? (yazılım polling)
  Status        → izlenen bit TRUE mu ? (seviye polling)
  External Event→ donanım IRQ bayrağı set mi ? (interrupt-driven)
```

Kritik fark: **Event ve Status yazılımsal polling'dir** (scheduler bit'i her interval örnekler), **External Event donanımsaldır** (IRQ doğrudan tetikler). Bu yüzden Event task scheduler interval'inden hızlı sinyalleri kaçırır (Not 5), External Event ise kaçırmaz ama kesme overhead'i taşır. "Event" ve "External Event" isim benzerliğine rağmen tamamen farklı mekanizmalardır.

### Freewheeling'in "Bekleme" Hesabı Neden Var?

Freewheeling saf "bittiği an yeniden başla" olsaydı, CPU'yu %100 kilitler ve hiçbir alt task çalışamazdı. CODESYS, freewheeling task'a bilinçli bir kısa bekleme (önceki exec süresinin bir oranı) ekler. Bu, alt öncelikli task'lara ve OS'e "nefes alma" penceresi açar. Yani freewheeling tam olarak "serbest" değildir; sistemi kilitlememek için kasıtlı throttle içerir. Bu tasarım, "freewheeling tüm CPU'yu alır" ezberinin neden tam doğru olmadığını açıklar — alt task'lar yine de az da olsa çalışır.

### Neden PID İçin Cyclic Zorunlu? — Matematik

PID'in integral ve türev terimleri Δt (örnekleme periyodu) içerir:

```
I_term += Ki × error × Δt
D_term  = Kd × (error - error_prev) / Δt
```

Freewheeling'de Δt her döngüde değişir (8ms, 15ms, 9ms...). Eğer kod sabit bir `fCycleTime` parametresi kullanırsa (gerçek Δt'den sapan), integral birikimi ve türev tahmini sistematik olarak hatalı olur → salınım. Eğer kod gerçek ölçülen Δt'yi kullanırsa, gürültülü/değişken Δt türev terimini patlatır. İki durumda da kontrol bozulur. Cyclic'in sabit Δt'si bu matematiği geçerli kılan tek koşuldur. Bu, "Freewheeling PID'i bozar" kuralının altındaki gerçek sebeptir — alışkanlık değil, matematik.

### Event Task ve Determinizm Felsefesi (fundamentals/01 ile bağ)

`fundamentals/01_runtime_architecture.md`'deki "determinizm" felsefesi burada da geçerlidir: Event ve External Event task'lar **asenkron**tır — yani ne zaman çalışacakları önceden bilinemez. Bu, deterministik tasarımla gerilim içindedir. CODESYS bu yüzden çoğu kontrol mantığını Cyclic'te tutmayı teşvik eder ve Event'i nadir, izole olaylarla sınırlar. Asenkron tetikleme güçlüdür ama "her döngü öngörülebilir" garantisini zayıflatır; uzman, bu ödünleşimi bilerek Event'i seçer.

## İlgili Konular

```
knowledge/codesys/task-structure/
├── 02_cycle_time.md         → Cyclic task için doğru interval nasıl seçilir
├── 03_priority_management.md→ Task öncelikleri nasıl sıralanır
└── _synthesis.md            → Task mimarisi tasarım kılavuzu

knowledge/codesys/fundamentals/
├── 01_runtime_architecture.md → Scheduler ve scan cycle mekanizması
└── 02_project_structure.md    → Task Configuration nesnesi

knowledge/codesys/advanced/
└── multicore_tasks.md         → Çok çekirdekli sistemlerde task affinity
```
