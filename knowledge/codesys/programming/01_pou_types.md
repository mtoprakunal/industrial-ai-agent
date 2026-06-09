---
KONU        : CODESYS POU Tipleri — Program, Function Block, Function
KATEGORİ    : codesys
ALT_KATEGORI: programming
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_obj_program.html"
    başlık: "CODESYS Online Help — Object: Program"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_obj_function_block.html"
    başlık: "CODESYS Online Help — Object: Function Block"
    güvenilirlik: resmi
  - url: "https://www.realpars.com/blog/codesys-pous"
    başlık: "RealPars — What Are the Different Types of POUs in CODESYS?"
    güvenilirlik: topluluk
  - url: "https://www.plctalk.net/forums/threads/program-vs-function-block-vs-functions.127713/"
    başlık: "PLCtalk — Program vs Function Block vs Functions (Tartışma)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "02_gvl_design.md"
    ilişki: tamamlar
  - konu: "03_function_blocks.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/fundamentals/02_project_structure.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "CODESYS proje yapısı (fundamentals/02_project_structure.md)"
  - "Temel IEC 61131-3 ST sözdizimi"
ÇELİŞKİLER :
  - kaynak: "IEC 61131-3 standardı vs CODESYS uygulaması"
    konu: "Standartta Function yalnızca tek dönüş değeri döndürür; CODESYS VAR_OUTPUT ile çoklu çıktıya izin verir"
    çözüm: >
      IEC standardında Function, imzasında tek bir dönüş değeri tanımlar.
      CODESYS'te ek olarak VAR_OUTPUT değişkenleri tanımlanabilir — bu teknik
      olarak çoklu çıktıya olanak verir. Taşınabilirlik ve okunabilirlik için
      çoklu çıktı gereken her durumda Function Block tercih edilmelidir.
  - kaynak: "CODESYS Forge topluluk"
    konu: "Program'ın birden fazla çağrılmasının yan etkileri"
    çözüm: >
      Bir Program farklı POU'lardan birden fazla çağrılabilir; her çağrıda
      değişiklikler kümülatif olarak birikir ve global etki yaratır.
      Bu durum beklenmedik yan etkilere neden olur. Program'ı yalnızca bir
      task'tan tek kez çağırmak mimari olarak doğrudur.
---

## Özün Ne

CODESYS'te her kod birimi üç POU tipinden biri olarak tanımlanır: **Program** (singleton, global durum), **Function Block** (çoklu instance, kendi belleği), **Function** (durumsuz, saf hesaplama). Bu ayrım rastgele değildir — her tipin bellek modeli, çağrılma biçimi ve yeniden kullanılabilirlik profili birbirinden farklıdır. Yanlış tip seçimi doğrudan bakım sorununa dönüşür: Program yapılan her şey kopyalanamaz, Function Block yapılması gereken her şey sonsuz global değişkene yol açar. Üç tipin farkını içselleştirmek CODESYS mimarisinin temelidir.

## Nasıl Çalışır

### Bellek Modeli Karşılaştırması

```
Tip           Bellek        Instance  Durum   Çağrılma
──────────────────────────────────────────────────────────────
PROGRAM       Statik, tek   Hayır     Evet    Task tarafından, bir kez
FUNCTION_BLOCK Dinamik, N   Evet      Evet    Başka POU'dan, N kez
FUNCTION       Yığın (stack) Hayır    Hayır   Başka POU'dan, N kez
```

### PROGRAM

**Tanım:** Singleton. Bellekte yalnızca bir kopyası vardır. Değişkenleri kalıcıdır — bir çağrıda yapılan değişiklik, bir sonraki çağrıya taşınır. Farklı POU'lardan çağrılabilir ancak tüm çağrılar aynı bellek alanını etkiler.

**Bellek Modeli:**
```
Proje Başlangıcı
│
└── PRG_ConveyorControl (PROGRAM — tek kopya, static RAM)
    ├── xRunning      : BOOL    ← Önceki çağrıdan korunur
    ├── dwCycleCount  : DWORD   ← Birikimli sayar
    └── tRunTimer     : TON     ← Timer state korunur
```

**Temel Kural:** Program'ın task'tan **bir kez** çağrılması mimarinin gereğidir. Farklı task'lardan veya farklı POU'lardan aynı Program'ı çağırmak, korunan değişkenlerin hangi bağlamda değiştiğini belirsizleştirir.

```iecst
(* Task Configuration → MainTask → Çağrılanlar *)
(* ✅ Doğru kullanım: Task'tan bir kez *)
PRG_ConveyorControl();

(* ❌ Yanlış kullanım: Hem MainTask hem de SlowTask'tan çağırmak *)
(* Her iki task da aynı xRunning, dwCycleCount'u değiştirir — hangisi son yazarsa o kazanır *)
```

**Ne zaman kullanılır:**
- Bir makine biriminin (konveyör, fırın, dolum ünitesi) üst düzey orkestrasyon kodu
- Her döngüde çalışması gereken, kopyalanmayacak ana mantık
- Task'a doğrudan bağlı olan giriş noktası

---

### FUNCTION_BLOCK

**Tanım:** Blueprint + Instance modeli. Function Block tanımı bir şablondur; her kullanım yerinde ayrı bir `instance` oluşturulur. Her instance bağımsız belleğe sahiptir — TON timer'ın neden birden fazla kez tanımlanabileceği buradan gelir.

**Bellek Modeli:**
```
FB_Motor (şablon — kaynak kodda tek tanımlı)
│
├── fbMotor1 : FB_Motor  ← Bağımsız bellek, kendi xRunning, kendi tTimer
├── fbMotor2 : FB_Motor  ← Bağımsız bellek, kendi xRunning, kendi tTimer
└── fbMotor3 : FB_Motor  ← Bağımsız bellek, kendi xRunning, kendi tTimer

fbMotor1.xRunning = TRUE, fbMotor2.xRunning = FALSE — birbirinden bağımsız
```

**Değişken Bölümleri:**
```iecst
FUNCTION_BLOCK FB_Motor
VAR_INPUT       (* Çağıran tarafından verilir *)
    xStartCmd   : BOOL;
    xStopCmd    : BOOL;
    tStartDelay : TIME := T#3S;
END_VAR
VAR_OUTPUT      (* Çağıran tarafından okunur *)
    xRunOutput  : BOOL;
    xFaultOut   : BOOL;
    eState      : E_MotorState;
END_VAR
VAR_IN_OUT      (* Hem okunur hem yazılır — REFERANS gibi *)
    stDiag      : ST_MotorDiag;
END_VAR
VAR             (* Sadece bu instance'a özel, dışarıdan görünmez *)
    tDelayTimer : TON;
    dwRunCount  : DWORD;
END_VAR
```

**CODESYS'te OOP Desteği:** Function Block, CODESYS V3'te `EXTENDS` ve `IMPLEMENTS` anahtar kelimeleriyle OOP yapılarına katılabilir. Bu, ST ile Interface, Inheritance ve Polymorphism kullanımını mümkün kılar — yalnızca Function Block'ta, Program ve Function'da değil.

**Ne zaman kullanılır:**
- Aynı mantığın birden fazla instance'a ihtiyaç duyduğu her yer (motor, vana, sensör)
- Cihaz yaşam döngüsünü kapsüllemek (init → run → fault → stop)
- Kütüphaneye alınacak, projelerde tekrar kullanılacak bileşenler
- OOP mimarisi (interface, polymorphism) gereken tasarımlar

---

### FUNCTION

**Tanım:** Durumsuz. Her çağrıda başlar, hesaplar, biter — aralarında hiçbir şey kalmaz. Yığın (stack) üzerinde çalışır; çağrı sona erince tüm yerel değişkenler silinir.

**Bellek Modeli:**
```
FC_ScaleValue çağrıldığında:
  Stack: rRaw, rMin, rMax, rScaled ← push
  Hesaplama yapılır
  Sonuç dönderilir
  Stack: temizlenir  ← pop
  
Bir sonraki çağrıda önceki değerlerin hiçbiri yok.
```

**Temel Kısıt:** Dahili TON, CTU gibi durum saklayan bloklar kullanılamaz — her çağrıda sıfırlanır.

```iecst
(* ✅ Function için ideal kullanım — saf dönüşüm *)
FUNCTION FC_ScaleAnalog : REAL
VAR_INPUT
    rRaw    : REAL;    (* Ham ADC değeri, ör. 0..4095 *)
    rRawMin : REAL;    (* ADC minimum, ör. 0 *)
    rRawMax : REAL;    (* ADC maksimum, ör. 4095 *)
    rEngMin : REAL;    (* Mühendislik birimi minimum, ör. 0.0 °C *)
    rEngMax : REAL;    (* Mühendislik birimi maksimum, ör. 100.0 °C *)
END_VAR

FC_ScaleAnalog := rEngMin + ((rRaw - rRawMin) / (rRawMax - rRawMin)) * (rEngMax - rEngMin);

(* Çağrı: rTemperature := FC_ScaleAnalog(rRaw:=GVL_IO.wTempADC, rRawMin:=0, rRawMax:=4095, rEngMin:=0.0, rEngMax:=100.0); *)
```

**Ne zaman kullanılır:**
- Birim dönüşümü (°C → °F, bar → PSI, ADC → mühendislik birimi)
- Bit manipülasyonu (WORD → BYTE dizi, bitfield okuma)
- Matematiksel hesaplamalar (limit kontrolü, interpolasyon, ölçeklendirme)
- Herhangi bir "giriş ver, çıkış al" biçimindeki saf hesaplama

**Ne zaman kullanılmamalıdır:**
- Timer, sayaç, durum makinesi içeren mantık → Function Block
- Birden fazla çağrıda kümülatif değer biriktirme → Function Block
- Sisteme yan etki (GVL'ye yazma) gerektiren işlem → dikkat, durumsuz kalınmalı

---

### Üç Tipin Karar Tablosu

```
Soru                                   Cevap
────────────────────────────────────────────────────────────────
Birden fazla kopyaya ihtiyaç var mı?   Evet → Function Block
                                        Hayır ↓
Durum/hafıza tutuluyor mu?             Evet → Program veya Function Block
                                        Hayır → Function
Task tarafından doğrudan çağrılacak mı? Evet → Program
                                        Hayır → Function Block veya Function
OOP gerekiyor mu?                      Evet → Function Block
Saf hesaplama mı?                      Evet → Function
```

## Pratikte Nasıl Kullanılır

### Tip Seçim Kontrol Listesi

```
Yeni POU oluştururken:
□ 5 farklı motoru kontrol edecek miyim? → Function Block
□ Bu POU'dan sadece bir tane olacak mı ve task'tan mı çağrılacak? → Program
□ Giriş al, hesapla, çıkış ver — başka bir şey yok mu? → Function
□ Timer veya sayaç kullanıyor muyum? → Asla Function değil, Function Block
□ Birden fazla yerden çağrılacak mı? → Kopyalanabilir mi? → Function Block veya Function
```

### Tipik Bir Projedeki Dağılım

```
Konveyörlü paketleme hattı (örnek)

PROGRAM (3 adet — task başına bir):
  PRG_Safety           Task_Safety'den çağrılır
  PRG_ConveyorControl  Task_Control'den çağrılır
  PRG_HMIUpdate        Task_HMI'dan çağrılır

FUNCTION_BLOCK (çoklu instance):
  FB_Motor             ← 4 farklı motor için 4 instance
  FB_Valve             ← 6 farklı vana için 6 instance
  FB_TemperatureCtrl   ← 2 ısıtıcı için 2 instance
  FB_Alarm             ← 20 farklı alarm için 20 instance

FUNCTION (saf hesaplama):
  FC_ScaleAnalog       ← 8 analog giriş için tekrar tekrar çağrılır
  FC_CelsiusToFahr     ← HMI'da gösterim için
  FC_IsInRange         ← Limit kontrolü her yerde kullanılır
  FC_ByteToWord        ← Modbus veri dönüşümü
```

## Örnekler

### Örnek 1: Aynı Mantık 3 Tipte — Farkları Görmek

**Görev:** Motor çalışıyor mu kontrolü + çalışma süresi sayacı

```iecst
(* === PROGRAM versiyonu === *)
(* Tek motor için, task'tan çağrılır, kopyalanamaz *)
PROGRAM PRG_MotorMonitor
VAR
    tRunTimer  : TON;
    tTotalRun  : TIME;
END_VAR
tRunTimer(IN := GVL_IO.xMotorFeedback, PT := T#24H);
IF GVL_IO.xMotorFeedback THEN
    tTotalRun := tTotalRun + T#10MS; (* Task cycle time ekleniyor *)
END_IF
(* Sorun: 4 motor olursa 4 PRG_MotorMonitor1,2,3,4 yazmak gerekir! *)

(* === FUNCTION BLOCK versiyonu === *)
(* Çoklu instance: fbMotor1, fbMotor2, fbMotor3... *)
FUNCTION_BLOCK FB_MotorMonitor
VAR_INPUT
    xFeedback  : BOOL;
    tCycleTime : TIME;
END_VAR
VAR_OUTPUT
    xRunning   : BOOL;
    tTotalRun  : TIME;
END_VAR
VAR
    tTimer     : TON;
END_VAR
xRunning := xFeedback;
tTimer(IN := xFeedback, PT := T#24H);
IF xFeedback THEN
    tTotalRun := tTotalRun + tCycleTime;
END_IF
(* 4 motor: fbMotor1(xFeedback:=...), fbMotor2(xFeedback:=...) *)
(* Her biri kendi tTotalRun'ını bağımsız sayar *)

(* === FUNCTION versiyonu — mümkün ama YANLIŞ seçim === *)
(* Durum tutamaz, tTotalRun her çağrıda sıfırlanır *)
FUNCTION FC_MotorRunning : BOOL
VAR_INPUT
    xFeedback : BOOL;
END_VAR
FC_MotorRunning := xFeedback;
(* tTotalRun sayamaz — durumsuz! Function yanlış seçim. *)
```

### Örnek 2: VAR_IN_OUT Kullanımı

```iecst
(* VAR_IN_OUT: struct geçirme — hem okur hem yazar, kopya oluşturmaz *)
FUNCTION_BLOCK FB_RecipeApply
VAR_IN_OUT
    stRecipe : ST_Recipe;   (* Referans olarak geçirilir, kopyalanmaz *)
END_VAR
VAR_INPUT
    xApply : BOOL;
END_VAR

IF xApply THEN
    stRecipe.bApplied := TRUE;
    stRecipe.dtApplyTime := NOW();
END_IF

(* Çağrı: fbRecipeApply(stRecipe := GVL_Recipes.stCurrentRecipe, xApply := ...); *)
(* GVL_Recipes.stCurrentRecipe.bApplied doğrudan güncellenir *)
```

### Örnek 3: Function ile Saf Hesaplama

```iecst
FUNCTION FC_IsInDeadband : BOOL
VAR_INPUT
    rActual    : REAL;
    rSetpoint  : REAL;
    rDeadband  : REAL;
END_VAR

FC_IsInDeadband := ABS(rActual - rSetpoint) <= rDeadband;

(* Her yerde kullanılır:
   IF FC_IsInDeadband(rActual:=rTemp, rSetpoint:=rTarget, rDeadband:=0.5) THEN
       xAtSetpoint := TRUE;
   END_IF *)
```

## Sık Yapılan Hatalar

### Hata 1: Her Şeyi Program Yapmak

```
Senaryo: 8 motorlu hatta her motor için ayrı PROGRAM.
  PRG_Motor1, PRG_Motor2 ... PRG_Motor8

Sorun: 8 özdeş programın bakımı: bir değişiklik 8 yerde tekrarlanır.
Çözüm: Tek FB_Motor tanımı, 8 instance:
  fbMotor1..8 : FB_Motor  ← 8 satır tanım, bir değişiklik her yerde
```

### Hata 2: Function'a Timer veya Sayaç Koymak

```iecst
(* ❌ YANLIŞ — Function'da TON kullanmak *)
FUNCTION FC_DelayedOutput : BOOL
VAR
    tDelay : TON;    (* Her çağrıda sıfırlanır! Timer hiç bitmez. *)
END_VAR
tDelay(IN := TRUE, PT := T#3S);
FC_DelayedOutput := tDelay.Q;
(* Bu kod asla TRUE döndürmez — tDelay her çağrıda yeniden başlar *)

(* ✅ DOĞRU — Function Block kullan *)
FUNCTION_BLOCK FB_DelayedOutput
VAR_INPUT
    xIn    : BOOL;
    tDelay : TIME;
END_VAR
VAR_OUTPUT
    xOut   : BOOL;
END_VAR
VAR
    tTimer : TON;   (* Instance'a özgü, korunur *)
END_VAR
tTimer(IN := xIn, PT := tDelay);
xOut := tTimer.Q;
```

### Hata 3: Program'ı Birden Fazla Yerden Çağırmak

```iecst
(* ❌ YANLIŞ *)
(* Task_Control içinde: *)    PRG_Alarm();
(* Task_HMI içinde de: *)     PRG_Alarm();   (* Aynı belleği iki task değiştiriyor! *)

(* ✅ DOĞRU *)
(* Task_Control: *)   PRG_Alarm();           (* Tek çağrı noktası *)
(* Task_HMI: *)       GVL_Alarms.xAlarmActive (* GVL üzerinden okur, PRG çağırmaz *)
```

### Hata 4: VAR_OUTPUT Değişkenini Çağıran Taraftan Yazmak

```iecst
(* ❌ YANLIŞ — Output'u dışarıdan zorla yazmak *)
fbMotor1.xRunOutput := TRUE;   (* Derlenir ama yanlış! *)
(* FB'nin iç mantığı bir sonraki scan'de bunu ezebilir *)

(* ✅ DOĞRU — Yalnızca Input değişkenlerini dışarıdan yönet *)
fbMotor1(xStartCmd := GVL_IO.xStartBtn, xStopCmd := GVL_IO.xStopBtn);
GVL_IO.xMotorOut := fbMotor1.xRunOutput;  (* Output'u oku, yazma *)
```

### Hata 5: Function'da Global Değişkene Yazmak

```iecst
(* ❌ YANLIŞ — Function'da yan etki *)
FUNCTION FC_CheckAndLog : BOOL
VAR_INPUT
    rValue : REAL;
END_VAR
IF rValue > 100.0 THEN
    GVL_Alarms.xOverRange := TRUE;   (* Yan etki! Function durumsuz olmalı *)
    FC_CheckAndLog := TRUE;
END_IF

(* ✅ DOĞRU — Yan etki yoksa Function, yoksa Function Block *)
FUNCTION FC_IsOverRange : BOOL
VAR_INPUT
    rValue    : REAL;
    rMaxValue : REAL;
END_VAR
FC_IsOverRange := rValue > rMaxValue;
(* Çağıran: GVL_Alarms.xOverRange := FC_IsOverRange(rValue:=rSensor, rMaxValue:=100.0); *)
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

| POU Tipi | Tercih Et | Tercih Etme |
|---|---|---|
| **PROGRAM** | Tek instance yeterli, task orkestratörü | Kopyalanabilir her şey |
| **FUNCTION_BLOCK** | Cihaz kontrolü, durum yönetimi, kütüphane | Saf hesaplama, durum gerekmez |
| **FUNCTION** | Dönüşüm, ölçeklendirme, bit işleme | Timer/sayaç içeren her şey |

## Gerçek Proje Notları

**Not 1 — Program'dan Function Block'a Geçiş Maliyeti**  
İlk büyük projede tüm konveyör mantığı `PRG_Conveyor` içindeydi. Müşteri 3 ay sonra hatta 4 yeni konveyör ekledi. `PRG_Conveyor1..5` oluşturmak, kodu kopyalamak, değişkenleri ayarlamak 3 gün sürdü. Bir hata düzeltmesi 5 dosyayı aynı anda düzenlemek anlamına geliyordu. Sonraki projede `FB_Conveyor` yazıldı; 5 instance 5 satır.

**Not 2 — Function'daki Timer Tuzağı**  
Yeni başlayan bir mühendis, `FC_PulseGenerator` adıyla Function içinde TON kullandı. Kod derlendi, çalıştı — ama puls çıkışı hiç gelmiyordu. 2 saat debug sonrası sorun fark edildi: TON her çağrıda sıfırlanıyordu. Function Block'a dönüştürüldü, problem çözüldü. Bu deneyim ekip içi bir "anti-pattern" listesine girdi.

**Not 3 — VAR_IN_OUT ile Büyük Struct Geçirme**  
Reçete yönetiminde `ST_Recipe` struct'ı 200 byte'tı. Her scan'de `VAR_INPUT` olarak kopyalanması gereksiz yük yaratıyordu. `VAR_IN_OUT` kullanımına geçilince CPU yükü %3 düştü — küçük ama ölçülebilir bir fark.

**Not 4 — Function'ın Okunabilirlik Gücü**  
`rTemperature := (GVL_IO.wTempADC / 4095.0) * 100.0 - 273.15` gibi satırlar proje boyunca 20 yerde tekrar ediyordu. `FC_ADCToTemperature` fonksiyonu yazıldıktan sonra aynı mantık tek satıra indi ve kalibrasyon katsayısı değiştiğinde yalnızca tek yer güncellendi.

**Not 5 — Function'ın "Gizli Durumu": VAR_STAT Tuzağı**  
Bir geliştirici, "Function durumsuzdur" kuralını bildiği halde `VAR_STAT` (static) ile bir sayaç tuttu — ve işe yaradı. Sorun şuydu: `VAR_STAT` Function'da tek bir global örnek paylaşır; Function 5 farklı yerden çağrılınca beşi de aynı sayacı artırdı. Görünürde "durumlu Function" elde edildi ama bu durum tüm çağrı noktalarınca paylaşılan tek bir bellek oldu. Ders: `VAR_STAT` Function'da çalışır ama instance-başına değil, **POU-başına tekildir** — gerçek per-instance durum gerekiyorsa hâlâ FB şart. `VAR_STAT` yalnızca tüm çağrılarda paylaşılması istenen sayaç/önbellek için doğrudur.

**Not 6 — `THIS^` ve Method'ların Program/Function'da Olmaması**  
Bir ekip, PROGRAM içinde METHOD tanımlamaya çalıştı (OOP alışkanlığıyla) — derleyici reddetti. METHOD, PROPERTY, `THIS^`, `SUPER^` yalnızca FUNCTION_BLOCK'a aittir. PROGRAM tek instance olduğu için method'a ihtiyaç duymaz; Function durumsuz olduğu için `THIS^` anlamsızdır. Ders: OOP gerektiren her şey FB'dir; "program da bir nesne olsun" beklentisi CODESYS'in nesne modeline aykırıdır.

**Not 7 — Function Çağrı Maliyeti (Sıcak Döngüde)**  
Analog ölçekleme `FC_Scale` 1ms task'ta 200 kanal için döngüde çağrılıyordu. Her çağrı bir stack frame kurar/yıkar; 200 çağrı/scan ölçülebilir overhead yarattı. Inline'lanabilir basit ifadeler için `{attribute 'inline'}` pragması veya doğrudan satır içi hesap, fonksiyon çağrı yükünü ortadan kaldırdı. Ders: Function soyutlaması bedavadır sanılır; sıcak döngüde çağrı sıklığı yüksekse inline değerlendirin.

## Edge Case'ler ve Sistem Limitleri

### Üç Tipin Bellek ve Yaşam Döngüsü Sınırları

```
Durum                                   PROGRAM    FUNCTION_BLOCK   FUNCTION
─────────────────────────────────────────────────────────────────────────
Statik bellek (her zaman ayrılı)        ✓          ✓ (instance)     ✗ (stack)
Reentrant (özyineleme/çoklu task)       ✗          dikkat           ✓ (stack-safe)
Recursion (kendini çağırma)             ✗          ✗ (instance state)✓ ama dikkat
VAR_STAT (POU-tekil kalıcı)             ✓          ✓                ✓ (paylaşımlı!)
Method/Property/THIS^                   ✗          ✓                ✗
RETAIN değişken                         ✓          ✓                ✗
```

### Function'da Recursion ve Stack

Function özyinelemeli (recursive) çağrılabilir — ama PLC'de stack sınırlıdır. Derin recursion (ör. ağaç gezme) **stack overflow → runtime crash** üretir; üstelik exception 64-bit'te yakalanamaz (bkz. 05_error_handling). Deterministik PLC kodunda recursion yerine açık stack/iteratif çözüm tercih edilir.

### Function Block Instance'ının "Sıfırlanması" Sorunu

Bir FB instance'ını çalışma anında "fabrika ayarına" döndürmenin standart bir yolu yoktur — `VAR` alanları yalnızca download/reset'te init değerine döner. Çalışırken reset gerekiyorsa FB'ye açık bir `xReset` girişi + iç init metodu yazılmalıdır. "Instance'ı yeniden oluşturmak" mümkün değildir; instance statik olarak ayrılmıştır.

### VAR_OUTPUT'a Dışarıdan Yazma — Derlenir Ama Tehlikeli

CODESYS, `fbMotor.xRunOutput := TRUE` gibi output'a dışarıdan yazmaya izin verir (derleme hatası vermez). Ama FB bir sonraki çağrıda bunu ezer. Bu "yarı-yazılabilir output" davranışı, sessiz mantık hatalarının kaynağıdır. Kural: output'lar salt-okunur muamelesi görmeli.

## Optimizasyon

### Tip Seçiminin Performans Profili

```
PROGRAM        → çağrı maliyeti yok (task doğrudan çalıştırır)
FUNCTION_BLOCK → instance pointer geçişi (çok ucuz) + gövde
FUNCTION       → stack frame kurulum/yıkım (her çağrıda)
```

Sıcak döngüde binlerce kez çağrılan saf hesap için **Function çağrısını inline'lamak** (`{attribute 'inline'}`) veya FB metoduna çevirmek (instance pointer cache'lenir) ölçülebilir kazanç sağlar.

### Pass-by-Reference ile Kopya Eliminasyonu

`VAR_INPUT` değere göre kopyalar; büyük struct/array'de bu her çağrı maliyetidir.

```iecst
(* ❌ 500 byte struct her çağrı kopyalanır *)
FUNCTION_BLOCK FB_Process VAR_INPUT stData : ST_Big; END_VAR

(* ✅ Referans — kopya yok *)
FUNCTION_BLOCK FB_Process VAR_IN_OUT stData : ST_Big; END_VAR
(* veya salt-okunur referans için: VAR_INPUT pData : POINTER TO ST_Big; *)
```

`VAR_IN_OUT` IEC'de referanstır; salt-okuma niyetinde bile kopya maliyetini siler. CODESYS V3.5 SP15+ ayrıca `VAR_INPUT {attribute 'by_reference'}` veya `REFERENCE TO` ile salt-okunur referans sağlar.

### Array of FB + FOR: Tekrarı Sıfıra İndirme

30 motor için 30 ayrı instance + 30 çağrı satırı yerine `ARRAY[1..30] OF FB_Motor` + tek `FOR` döngüsü; hem kod hacmini hem de bakım yüzeyini düşürür. Parametreler paralel bir `ARRAY OF ST_MotorParams`'tan beslenir.

## Derin Teknik Detay

### Neden Üç Ayrı Tip? — Bellek Modelinin Dayattığı Ayrım

Üç POU tipi keyfi bir API tercihi değil, üç farklı **bellek yaşam döngüsünün** doğrudan yansımasıdır:

```
FUNCTION       → otomatik (stack) ömür: çağrıda doğar, dönüşte ölür
FUNCTION_BLOCK → statik, instance-başına: download'da ayrılır, kalıcı
PROGRAM        → statik, tekil: instance kavramı yok, global singleton
```

Bu, C dilindeki yerel değişken (stack) / global static / dosya-statik ayrımıyla aynı temel ayrımdır. IEC bunu PLC'ye uyarlamıştır: Function = saf hesap (stack güvenli, reentrant), FB = durum makinesi (kalıcı instance state), PROGRAM = uygulamanın kök düğümü. "Hangi tipi seçeyim?" sorusunun gerçek cevabı her zaman "verimin yaşam döngüsü nedir?"dir.

### PROGRAM Aslında Bir Singleton FB'dir

Derleyici seviyesinde PROGRAM, instance'ı tek ve global olan özel bir FB gibi davranır — kendi statik bellek bloğuna sahiptir, task tarafından "çağrılır" (`PRG_X()`). Fark semantiktir: PROGRAM'ın instance'ı oluşturulamaz/kopyalanamaz, doğrudan adıyla erişilir. Bu yüzden PROGRAM'ı iki task'tan çağırmak (Not / Hata 3) tek paylaşılan belleği iki zaman tabanında bozar — tıpkı bir FB instance'ını iki task'tan çağırmak gibi (bkz. task-structure/01).

### Function'ın "Saf Olması" Determinizmle İlişkili

Function'ın yan etkisiz (saf) olması yalnızca bir stil tercihi değil; reentrancy ve test edilebilirlik garantisidir. Yan etkisiz bir Function:
- Aynı girişe her zaman aynı çıkışı verir → birim testi trivial.
- Stack'te çalıştığı için aynı anda farklı task'lardan reentrant çağrılabilir → race yok.
- Derleyici tarafından inline/optimize edilebilir (sabit katlama).

GVL'ye yazan bir Function bu üç garantiyi de kırar — bu yüzden "Function'da yan etki yapma" kuralı, kozmetik değil mimari bir sözleşmedir (bkz. fundamentals/_synthesis determinizm felsefesi).

### VAR_IN_OUT'un Pointer Gerçeği

`VAR_IN_OUT`, perde arkasında bir pointer (adres) geçişidir — bu yüzden literal/sabit geçirilemez (sabitin adresi yoktur). Bu mekanizma:
- Büyük veriyi kopyalamadan paylaşır (performans).
- Çağıranın orijinal değişkenini doğrudan değiştirir (yan etki — bilinçli olmalı).
- Online Change ile etkileşir: referans gösterilen değişken yeniden konumlanırsa pointer güncellenir, ama scan'ler arası saklanan ham `ADR()` sonuçları dangling olabilir (bkz. fundamentals/02 Online Change pointer tuzağı).

## İlgili Konular

```
knowledge/codesys/programming/
├── 02_gvl_design.md         → POU'lar arasındaki veri akışı
├── 03_function_blocks.md    → FB tasarım prensipleri derinlemesine
├── 04_libraries.md          → FB'leri kütüphaneye dönüştürmek
└── 05_error_handling.md     → FB içinde hata yönetimi

knowledge/codesys/fundamentals/
├── 02_project_structure.md  → POU'ların proje içindeki yeri
└── 03_iec61131_languages.md → Her POU tipinde hangi dil kullanılır

knowledge/codesys/advanced/
└── oop_codesys.md           → FB ile Interface, Inheritance, Polymorphism
```
