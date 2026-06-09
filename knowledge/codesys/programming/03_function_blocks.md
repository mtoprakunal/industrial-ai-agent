---
KONU        : İyi Bir Function Block Nasıl Yazılır
KATEGORİ    : codesys
ALT_KATEGORI: programming
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_obj_function_block.html"
    başlık: "CODESYS Online Help — Object: Function Block"
    güvenilirlik: resmi
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/function-block-vs-aoi-understanding-plc-programming-terminology"
    başlık: "Industrial Monitor Direct — Function Block vs AOI"
    güvenilirlik: topluluk
  - url: "https://www.plctalk.net/forums/threads/program-vs-function-block-vs-functions.127713/"
    başlık: "PLCtalk — Program vs Function Block vs Functions"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_pou_types.md"
    ilişki: gerektirir
  - konu: "02_gvl_design.md"
    ilişki: tamamlar
  - konu: "04_libraries.md"
    ilişki: tamamlar
  - konu: "05_error_handling.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "POU tipleri (01_pou_types.md)"
  - "ST dili temelleri (fundamentals/03_iec61131_languages.md)"
  - "CASE ile state machine kavramı"
ÇELİŞKİLER :
  - kaynak: "FB tasarım felsefeleri — monolitik vs atomik"
    konu: "Bir FB ne kadar büyük olmalı?"
    çözüm: >
      FB'yi tek bir sorumluluğa sahip tutmak (Single Responsibility) bakımı
      kolaylaştırır. Ancak çok küçük FB'ler (yalnızca 3-5 satır) gereksiz
      karmaşıklık yaratır. Pratik kural: Bir cihazın tüm yaşam döngüsü
      (init, run, fault, stop) tek FB'de; alt işlevler (ölçeklendirme,
      PID) ayrı, daha küçük FB veya Function'larda.
---

## Özün Ne

Function Block, CODESYS'in en güçlü yapı taşıdır. Doğru yazılmış bir FB; bir kez yazılır, onlarca projede kullanılır, test edilebilir, genişletilebilir ve başka geliştiriciler tarafından anlaşılabilir. Kötü yazılmış bir FB ise tam tersine: global değişkenlere sızdırır, kopyalanabilir değildir, test edilemez ve bakımı kaçınılmaz hale getirir. Bu belge, "iyi FB" ile "kötü FB" arasındaki farkı somut örneklerle ortaya koyar.

## Nasıl Çalışır

### FB Arayüz Tasarımı — Değişken Bölümleri

İyi bir FB, dış dünyayla yalnızca tanımlanmış arayüz değişkenleri üzerinden konuşur. Global değişkene doğrudan erişmez.

```iecst
FUNCTION_BLOCK FB_Motor
VAR_INPUT
    (* ── Komutlar (çağıran tarafından yazılır) ── *)
    xStartCmd     : BOOL;           (* Çalıştırma komutu *)
    xStopCmd      : BOOL;           (* Durdurma komutu *)
    xFaultReset   : BOOL;           (* Hata sıfırlama — yükselen kenar *)
    
    (* ── Konfigürasyon (tipik olarak sabittir) ── *)
    tStartDelay   : TIME := T#3S;   (* Çalışma onay gecikmesi *)
    tFaultDelay   : TIME := T#500MS;(* Geri bildirim yoksa fault gecikmesi *)
    bEnabled      : BOOL := TRUE;   (* FALSE → hiç çalışmaz *)
END_VAR

VAR_OUTPUT
    (* ── Çıkışlar (çağıran tarafından okunur) ── *)
    xRunOutput    : BOOL;           (* Motor çıkış komutu → I/O'ya bağlanır *)
    xReady        : BOOL;           (* İdle, hata yok, start bekliyor *)
    xRunning      : BOOL;           (* Onaylı çalışma durumu *)
    xFault        : BOOL;           (* Aktif hata bayrağı *)
    eState        : E_MotorState;   (* Mevcut durum — HMI/diagnostik için *)
    sLastFaultMsg : STRING(80);     (* Son hata mesajı — operatör bilgi *)
END_VAR

VAR_IN_OUT
    (* ── Paylaşılan referanslar (okunur + yazılır) ── *)
    stDiag : ST_MotorDiag;          (* Diagnostik struct — FB günceller *)
END_VAR

VAR
    (* ── Dahili durum değişkenleri (dışarıdan görünmez) ── *)
    tStartTimer      : TON;
    tFaultTimer      : TON;
    fbRTrig_Reset    : R_TRIG;      (* Fault reset yükselen kenar *)
    tRunningTime     : TIME;        (* Toplam çalışma süresi *)
    bLastStartCmd    : BOOL;        (* Edge detection için *)
END_VAR
```

### Durum Makinesi ile FB İmplementasyonu

İyi bir FB, davranışını net bir durum makinesiyle modeller. Her durumda ne yapıldığı, hangi koşulda geçiş olduğu açıkça görülür.

```iecst
(* Durum tanımı — DUT dosyasında *)
TYPE E_MotorState :
(
    eIdle       := 0,   (* Bekliyor, hazır *)
    eStarting   := 1,   (* Başlama gecikmesi sürüyor *)
    eRunning    := 2,   (* Çalışıyor, onaylandı *)
    eStopping   := 3,   (* Durma komutu verildi *)
    eFault      := 4    (* Hata durumu *)
);
END_TYPE

(* FB implementasyonu *)
fbRTrig_Reset(CLK := xFaultReset);

CASE eState OF

    eIdle:
        xRunOutput  := FALSE;
        xReady      := bEnabled AND NOT xFault;
        xRunning    := FALSE;
        
        IF xStartCmd AND bEnabled AND NOT xFault THEN
            tStartTimer(IN := FALSE);   (* Timer'ı sıfırla *)
            eState := eStarting;
        END_IF

    eStarting:
        xRunOutput  := TRUE;            (* Çıkış ver *)
        xReady      := FALSE;
        tStartTimer(IN := TRUE, PT := tStartDelay);
        
        (* Geri bildirim zamanında gelmezse fault *)
        IF NOT xFeedback_External THEN  (* Eğer fiziksel FB bağlıysa *)
            tFaultTimer(IN := TRUE, PT := tFaultDelay);
            IF tFaultTimer.Q THEN
                sLastFaultMsg := 'Motor run feedback timeout';
                xFault := TRUE;
                eState := eFault;
            END_IF
        END_IF
        
        IF tStartTimer.Q THEN
            tStartTimer(IN := FALSE);
            tFaultTimer(IN := FALSE);
            eState := eRunning;
        END_IF
        
        IF xStopCmd OR NOT bEnabled THEN
            tStartTimer(IN := FALSE);
            eState := eIdle;
        END_IF

    eRunning:
        xRunOutput  := TRUE;
        xRunning    := TRUE;
        tRunningTime := tRunningTime + T#10MS;  (* Cycle time eklenir *)
        
        stDiag.tTotalRunTime := tRunningTime;   (* VAR_IN_OUT güncelle *)
        
        IF xStopCmd OR NOT bEnabled THEN
            eState := eStopping;
        END_IF

    eStopping:
        xRunOutput  := FALSE;
        xRunning    := FALSE;
        eState      := eIdle;   (* Basit durma — gecikme eklenebilir *)

    eFault:
        xRunOutput  := FALSE;
        xRunning    := FALSE;
        xFault      := TRUE;
        
        IF fbRTrig_Reset.Q THEN     (* Reset yükselen kenar *)
            xFault         := FALSE;
            sLastFaultMsg  := '';
            eState         := eIdle;
        END_IF

    ELSE:
        (* Bilinmeyen durum — güvenli duruma geç *)
        xRunOutput  := FALSE;
        eState      := eFault;
        sLastFaultMsg := 'Unknown state';
END_CASE

(* Çıkış özetleme *)
xReady := (eState = eIdle) AND bEnabled AND NOT xFault;
```

### FB Tasarım Prensipleri

**1. Single Responsibility (Tek Sorumluluk)**
```
✅ FB_Motor: Motor yaşam döngüsü yönetir (start, run, stop, fault)
✅ FB_PID: PID hesabı yapar
✅ FB_Alarm: Tek bir alarm yönetir

❌ FB_MotorWithPIDAndAlarm: Üç sorumluluğu bir arada — bakımı zor, test edilemez
```

**2. Kapsülleme — Global'e Dokunma**
```iecst
(* ❌ KÖTÜ — FB global değişkene yazıyor *)
FUNCTION_BLOCK FB_Motor_Bad
    GVL_IO.xMotorOut := xRunOutput;     (* FB içinden global'e direkt yazma *)
    GVL_Alarms.xMotorFault := xFault;   (* Yan etki — test edilemez *)

(* ✅ İYİ — FB yalnızca kendi çıkışlarına yazar *)
FUNCTION_BLOCK FB_Motor_Good
    (* Yalnızca VAR_OUTPUT'a yazar *)
    xRunOutput := TRUE;
    xFault := FALSE;
    
(* Çağıran PRG_Control: *)
    fbMotor1(xStartCmd := GVL_HMI.xStart);
    GVL_IO.xMotorOut    := fbMotor1.xRunOutput;   (* PRG global'e yazar *)
    GVL_Alarms.xMotorFault := fbMotor1.xFault;    (* PRG global'e yazar *)
```

**3. Savunmacı Programlama**
```iecst
(* Giriş sınırları her döngüde kontrol edilmeli *)
IF tStartDelay < T#100MS THEN
    tStartDelay := T#100MS;    (* Alt limit koru *)
END_IF
IF tStartDelay > T#60S THEN
    tStartDelay := T#60S;      (* Üst limit koru *)
END_IF
```

**4. ELSE koşulu her CASE'de**
```iecst
CASE eState OF
    ...durum'lar...
    ELSE:
        eState := eFault;    (* Bilinmeyen durum → güvenli duruma *)
        xRunOutput := FALSE;
END_CASE
```

**5. Başlatma Değerleri**
```iecst
VAR_INPUT
    tStartDelay : TIME := T#3S;    (* Makul varsayılan — çağıran belirtmek zorunda değil *)
    bEnabled    : BOOL := TRUE;    (* Varsayılan aktif *)
    rMaxSpeed   : REAL := 100.0;
END_VAR
VAR
    eState : E_MotorState := eIdle;  (* İlk durum açık *)
END_VAR
```

## Pratikte Nasıl Kullanılır

### FB_Valve — Vana Kontrolü Örneği

```iecst
FUNCTION_BLOCK FB_Valve
VAR_INPUT
    xOpenCmd      : BOOL;       (* Açma komutu *)
    xCloseCmd     : BOOL;       (* Kapama komutu *)
    tOpenTimeout  : TIME := T#5S;
    tCloseTimeout : TIME := T#5S;
END_VAR
VAR_OUTPUT
    xOpenOutput   : BOOL;       (* Vana açma çıkışı *)
    xOpen         : BOOL;       (* Açık durumda onaylandı *)
    xClosed       : BOOL;       (* Kapalı durumda onaylandı *)
    xFault        : BOOL;
    eState        : E_ValveState;
END_VAR
VAR_INPUT
    (* Gerçek vana geri bildirimleri — bağlanmayabilir *)
    xOpenFB       : BOOL;       (* Açık limit switch *)
    xClosedFB     : BOOL;       (* Kapalı limit switch *)
END_VAR
VAR
    tTimeout      : TON;
END_VAR

CASE eState OF
    eValve_Closed:
        xOpenOutput := FALSE;
        xClosed := xClosedFB OR NOT xOpenFB;  (* FB yoksa pozisyon tahmini *)
        xOpen   := FALSE;
        IF xOpenCmd AND NOT xCloseCmd THEN
            tTimeout(IN := FALSE);
            eState := eValve_Opening;
        END_IF

    eValve_Opening:
        xOpenOutput := TRUE;
        tTimeout(IN := TRUE, PT := tOpenTimeout);
        IF xOpenFB THEN
            tTimeout(IN := FALSE);
            eState := eValve_Open;
        ELSIF tTimeout.Q THEN
            xFault := TRUE;
            eState := eValve_Fault;
        END_IF

    eValve_Open:
        xOpenOutput := TRUE;
        xOpen   := TRUE;
        xClosed := FALSE;
        IF xCloseCmd OR NOT xOpenCmd THEN
            eState := eValve_Closing;
        END_IF

    eValve_Closing:
        xOpenOutput := FALSE;
        tTimeout(IN := TRUE, PT := tCloseTimeout);
        IF xClosedFB THEN
            tTimeout(IN := FALSE);
            eState := eValve_Closed;
        ELSIF tTimeout.Q THEN
            xFault := TRUE;
            eState := eValve_Fault;
        END_IF

    eValve_Fault:
        xOpenOutput := FALSE;
        (* Fault reset harici olarak yönetilir *)
END_CASE
```

### FB Çağrısı — Doğru Biçim

```iecst
(* PRG_ProcessControl içinde *)
VAR
    fbMotor1   : FB_Motor;
    fbMotor2   : FB_Motor;
    fbValve1   : FB_Valve;
END_VAR

(* Tüm FB instance'ları her döngüde çağrılmalı *)
fbMotor1(
    xStartCmd   := GVL_HMI.xMotor1_Start,
    xStopCmd    := GVL_HMI.xMotor1_Stop OR GVL_Alarms.xEmgStop,
    xFaultReset := GVL_HMI.xMotor1_FaultReset,
    tStartDelay := GVL_Params.tMotor1_StartDelay
);

fbMotor2(
    xStartCmd   := GVL_HMI.xMotor2_Start AND fbMotor1.xRunning,  (* Motor1 çalışınca *)
    xStopCmd    := GVL_HMI.xMotor2_Stop
);

fbValve1(
    xOpenCmd   := fbMotor1.xRunning,
    xClosedFB  := GVL_IO.xValve1_ClosedFB,
    xOpenFB    := GVL_IO.xValve1_OpenFB
);

(* Çıkışları I/O'ya aktar *)
GVL_IO.xMotor1_Out := fbMotor1.xRunOutput;
GVL_IO.xMotor2_Out := fbMotor2.xRunOutput;
GVL_IO.xValve1_Out := fbValve1.xOpenOutput;

(* Alarm bayraklarını GVL_Alarms'a aktar *)
GVL_Alarms.xMotor1_Fault := fbMotor1.xFault;
GVL_Alarms.xValve1_Fault  := fbValve1.xFault;
```

## Örnekler

### Örnek 1: FB_PIDTemperature — Sıcaklık Kontrol FB'si

```iecst
FUNCTION_BLOCK FB_TemperatureController
VAR_INPUT
    rActual     : REAL;         (* °C cinsinden mevcut sıcaklık *)
    rSetpoint   : REAL;         (* Hedef sıcaklık *)
    bAutoMode   : BOOL := TRUE; (* FALSE → manuel mod *)
    rManOutput  : REAL;         (* Manuel modda çıkış *)
    tCycleTime  : TIME := T#10S;(* Task cycle time ile eşleşmeli *)
    
    (* PID parametreleri *)
    rKp         : REAL := 1.0;
    rTi         : REAL := 10.0; (* Saniye *)
    rTd         : REAL := 0.5;
    rOutMin     : REAL := 0.0;  (* % minimum çıkış *)
    rOutMax     : REAL := 100.0;(* % maksimum çıkış *)
END_VAR
VAR_OUTPUT
    rOutput     : REAL;         (* 0-100% ısıtıcı gücü *)
    bAtSetpoint : BOOL;         (* ±deadband içinde mi *)
    bSatHigh    : BOOL;         (* Çıkış maksimumda kilitli *)
    bSatLow     : BOOL;         (* Çıkış minimumda kilitli *)
END_VAR
VAR
    fbPID       : FB_PID;       (* Standard.library *)
    rDeadband   : REAL := 1.0;  (* ±°C *)
END_VAR

fbPID(
    fActualValue    := rActual,
    fSetpointValue  := rSetpoint,
    fManSyncValue   := rManOutput,
    bManualMode     := NOT bAutoMode,
    fKp             := rKp,
    fTn             := rTi,
    fTv             := rTd,
    fOutMinLimit    := rOutMin,
    fOutMaxLimit    := rOutMax,
    fCycleTime      := TIME_TO_REAL(tCycleTime) / 1000.0
);

rOutput     := fbPID.fOut;
bAtSetpoint := ABS(rActual - rSetpoint) <= rDeadband;
bSatHigh    := fbPID.bARWactive AND (rOutput >= rOutMax);
bSatLow     := fbPID.bARWactive AND (rOutput <= rOutMin);
```

### Örnek 2: Kötü FB — Ne Olmamalı

```iecst
(* ❌ KÖTÜ FB — Tüm anti-pattern'lar bir arada *)
FUNCTION_BLOCK FB_Bad_Motor
VAR
    xRunning : BOOL;    (* Output değil VAR — dışarıdan okunamaz *)
END_VAR

(* Global değişkene doğrudan yazıyor *)
GVL_IO.xMotorOut := GVL_IO.xStartBtn AND NOT GVL_IO.xStopBtn;
GVL_Alarms.xMotorFault := NOT GVL_IO.xMotorFeedback AND GVL_IO.xMotorOut;

(* Sorunlar:
   1. VAR_INPUT yok — parametrize edilemiyor, kopyalanamaz
   2. VAR_OUTPUT yok — çıkış durumu sorgulanamiyor
   3. GVL'ye direkt yazıyor — yan etki, test edilemez
   4. State machine yok — durum belirsiz
   5. Hata mesajı yok — debug imkansız
   6. Eğer 5 motor olursa bu FB 5 kez aynı GVL'ye yazıyor — çakışma *)
```

## Sık Yapılan Hatalar

### Hata 1: FB'yi Her Döngüde Çağırmamak

```iecst
(* ❌ YANLIŞ — Koşullu çağrı *)
IF xEnableMotor THEN
    fbMotor1(xStartCmd := xStart);  (* xEnableMotor FALSE iken timer durur! *)
END_IF

(* ✅ DOĞRU — Her zaman çağır, enable'ı parametre olarak geç *)
fbMotor1(
    xStartCmd := xStart,
    bEnabled  := xEnableMotor   (* FB kendi içinde yönetir *)
);
```

TON, CTU gibi bloklar içeren her FB, her scan döngüsünde çağrılmalıdır. Koşullu çağrı, timer/sayaç değerlerinin donmasına neden olur.

### Hata 2: Çıkışı Çağrıdan Önce Okumak

```iecst
(* ❌ YANLIŞ — Önce çıkışı oku, sonra çağır *)
xMotorRunning := fbMotor1.xRunning;  (* Eski döngünün değeri! *)
fbMotor1(xStartCmd := xStart);

(* ✅ DOĞRU — Önce çağır, sonra çıkışı oku *)
fbMotor1(xStartCmd := xStart);
xMotorRunning := fbMotor1.xRunning;  (* Bu döngünün güncel değeri *)
```

### Hata 3: VAR_IN_OUT'a Sabit Geçirmek

```iecst
(* ❌ YANLIŞ — Sabit/literal VAR_IN_OUT'a geçirilemez *)
fbRecipe(stRecipe := stTempRecipe);  (* stTempRecipe'nin referansı geçer — OK *)
(* Ama: *)
fbRecipe(stRecipe := GVL_Recipes.aRecipeBank[nIdx]);  (* Array element — OK *)
(* Literal değer geçilemez — derleme hatası *)
```

### Hata 4: State Machine'de ELSE Kullanmamak

```iecst
(* ❌ YANLIŞ — ELSE yok *)
CASE eState OF
    eIdle: ...
    eRunning: ...
    eFault: ...
    (* Program hatası ile eState = 99 olursa ne olur? Tanımlanmamış! *)

(* ✅ DOĞRU *)
CASE eState OF
    eIdle: ...
    eRunning: ...
    eFault: ...
    ELSE:
        eState := eFault;   (* Bilinmeyen durum → güvenli duruma *)
        xRunOutput := FALSE;
END_CASE
```

### Hata 5: FB'nin Instance'ını Her Döngüde Yeniden Oluşturmak

```iecst
(* ❌ YANLIŞ — FB'yi yerel değişken olarak bildirip döngüde her seferinde çağırmak
   gibi görünüyor ama aslında her PROGRAM çağrısında FB'nin durumu korunur.
   Asıl hata: FOR içinde temp FB kullanmak — her iterasyonda taze instance *)
FOR i := 1 TO 10 DO
    VAR tempFB : FB_Motor; END_VAR   (* Derleme zamanı hatası — ama mantık yanlış *)
END_FOR

(* ✅ DOĞRU — Array of FB *)
VAR
    afbMotor : ARRAY[1..10] OF FB_Motor;
END_VAR
FOR i := 1 TO 10 DO
    afbMotor[i](xStartCmd := aMotorStart[i]);
END_FOR
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**FB Yaz:**
- Bir cihaz veya işlem birimi, başlangıç → çalışma → duruş → hata yaşam döngüsüne sahipse
- Aynı mantık 2+ kez kullanılacaksa
- Test edilmesi ve bağımsız doğrulanması isteniyorsa
- Kütüphaneye alınacaksa

**FB Yazma:**
- Yalnızca bir kez kullanılacak ve kopyalanmayacaksa → PROGRAM
- Durum tutmaya gerek yoksa, saf hesaplamaysa → FUNCTION
- 3-5 satırlık mantık, paylaşım gerekmiyorsa → PROGRAM içinde yerel

## Gerçek Proje Notları

**Not 1 — FB_Motor'un 50 Farklı Projede Kullanılması**  
Bir kez yazılan `FB_Motor`, şu ana kadar 50'nin üzerinde projede kullanıldı. Her projede aynı arayüz, aynı durum makinesi — yalnızca `tStartDelay` ve `tFaultDelay` parametreleri değişiyor. Bakımı kolaylaştırmak, test zamanını kısaltmak, saha davranışını öngörülebilir kılmak açısından bu yaklaşım en büyük verimlilik artışını sağladı.

**Not 2 — Global'e Yazan FB'nin Açtığı Sorun**  
Eski bir projeden devralınan `FB_PressureControl` doğrudan `GVL_IO.xPumpOut`'a yazıyordu. Aynı projede iki basınç ünitesi eklenince FB iki kez çağrıldı — her iki instance da aynı `GVL_IO.xPumpOut`'a yazdı; son çağrı kazandı. Saatlerce süren debug sonrası FB tamamen yeniden yazıldı: çıkış değişkeni, atamayı çağıran `PRG_ProcessControl`'e bıraktı.

**Not 3 — Array of FB ile 30 Motor**  
Büyük bir üretim hattında 30 konveyör motorunu yönetmek için `ARRAY[1..30] OF FB_Motor` kullanıldı. FOR döngüsü ile tek satırda tüm motorlar çağrıldı. Bir motor parametresinin güncellenmesi tüm 30 motoru etkiledi — veya yalnızca bir `aMotorParams[i]` değiştirildi. Bağımsız programlama yerine bu yaklaşım, bakım süresini belirgin biçimde kısalttı.

**Not 4 — State Machine ELSE Olmayan Projenin Felaketi**  
Bir arıza sonrası program download edildi, RETAIN değişkenleri bozuldu, `eState` değeri `127` olarak kaldı. CASE yapısında `ELSE` yoktu; motor çıkışı belirsiz bir değerde kaldı — ne TRUE ne FALSE, tanımsız. Makine beklenmedik biçimde hareket etti. `ELSE → eFault` eklendikten sonra aynı senaryo güvenle sonuçlandı.

**Not 5 — Inheritance Zincirinde "Kaybolan" Method Çağrısı**  
Bir ekip `FB_Motor`'dan `FB_ServoMotor EXTENDS FB_Motor` türetti ve servo'da bir `Execute` metodu override etti. Ama base FB'nin gövdesindeki (FB body) kod hâlâ eski mantığı çalıştırıyordu — override beklenen yerde devreye girmedi. Neden: FB **gövdesi** (implementation) ile **metodları** ayrı çağrı yollarıdır; gövde kodu otomatik olarak türetilen sınıfın metodunu çağırmaz, açık `THIS^.Method()` veya sanal metot deseni gerekir. Ders: OOP'ta FB gövdesine mantık koymak yerine her şeyi metoda taşıyıp polimorfizmi açıkça kurun; "gövde + override" karışımı sessiz hata üretir.

**Not 6 — `REFERENCE TO` ve Atanmamış Referans Crash'i**  
Bir FB, `VAR_IN_OUT` yerine `REFERENCE TO ST_Data` aldı. Bir senaryoda çağıran referansı hiç atamadı (`__ISVALIDREF` kontrolü yoktu); FB atanmamış referansı dereference edince runtime exception (64-bit'te yakalanamaz) ile çöktü. Ders: `REFERENCE TO` kullanan FB, erişimden önce `__ISVALIDREF(refData)` ile geçerlilik kontrolü yapmalı. `VAR_IN_OUT` derleyici tarafından atama zorunluluğu getirir; `REFERENCE TO` getirmez — esneklik, sorumlulukla gelir.

**Not 7 — Method İçindeki Yerel Timer Tuzağı**  
Geliştirici bir TON'u FB metodunun `VAR` bölümünde tanımladı. Method her çağrıldığında timer sıfırlandı — Function'daki timer tuzağının (01_pou_types) FB-metot versiyonu. Method'un yerel `VAR`'ı, tıpkı Function gibi her çağrıda taze başlar; kalıcı durum FB'nin kendi `VAR` bölümünde olmalı, metodun değil. Ders: Durumlu bloklar (TON/CTU/R_TRIG) FB gövde-seviyesi `VAR`'da; method yerel değişkenleri stack'tedir, kalıcı değildir.

## Edge Case'ler ve Sistem Limitleri

### FB Çağrı Semantiği Edge Case'leri

```
Durum                                   Davranış
─────────────────────────────────────────────────────────────────
FB koşullu çağrılır (IF içinde)         İç timer/sayaç DONAR (çağrılmadığı scan)
Çıkış çağrıdan ÖNCE okunur              Bir önceki scan'in değeri (gecikme)
Aynı instance iki task'tan çağrılır     Tanımsız iç durum (bkz. task-structure/01)
VAR_IN_OUT'a literal geçirilir          Derleme hatası (literalin adresi yok)
Method yerel VAR'da TON                 Her çağrı sıfırlanır (durumsuz)
eState init değeri verilmemiş           0'dan başlar — ilk enum değeri olmalı
```

### State Machine'in "Geçiş Arası" Tutarsızlığı

Bir CASE state machine'de aynı scan içinde durum geçişi yapıldığında, geçişten sonraki kod **o scan çalışmaz** (CASE bir kez değerlendirilir). Bu kasıtlıdır (her scan bir adım) ama beklenmedik olabilir:

```iecst
CASE eState OF
    eStarting:
        eState := eRunning;   (* Bu scan eRunning kodu ÇALIŞMAZ *)
    eRunning:
        xRunOutput := TRUE;   (* Bir sonraki scan çalışır → 1 scan gecikme *)
END_CASE
```

Hızlı geçişler için ya `WHILE`/tekrar değerlendirme (dikkatli!) ya da geçiş tasarımını 1-scan gecikmeyi kabul edecek şekilde yapın.

### Output Persistensi

FB output'ları (`VAR_OUTPUT`) instance belleğinde kalıcıdır — FB bir durumda output'u set edip başka durumda sıfırlamayı unutursa, output "yapışık" kalır. Her state'in tüm ilgili output'ları açıkça yönetmesi (veya CASE öncesi varsayılan atama) gerekir.

## Optimizasyon

### Büyük Veri için Referans, Kopya Değil

```iecst
(* ❌ 200 byte recipe her çağrı kopyalanır *)
VAR_INPUT stRecipe : ST_Recipe; END_VAR

(* ✅ Referans — kopya yok, CPU tasarrufu (gerçek projede ~%3 yük düşüşü) *)
VAR_IN_OUT stRecipe : ST_Recipe; END_VAR
```

### Method vs Gövde: Çağrı Sıklığına Göre

- **FB gövdesi (implementation):** Her FB çağrısında çalışır — ana state machine buraya.
- **Method:** Yalnızca açıkça çağrılınca çalışır — opsiyonel/seyrek işlemler (Init, Reset, GetDiag) metoda taşınırsa, her scan değil yalnızca gerektiğinde maliyet doğar.

Sıcak döngüde her scan çağrılan FB'de, seyrek mantığı metoda ayırmak ana gövdeyi yalın ve hızlı tutar.

### Array of FB + FOR: Toplu İşleme

```iecst
VAR afbMotor : ARRAY[1..30] OF FB_Motor; END_VAR
FOR i := 1 TO 30 DO
    afbMotor[i](xStartCmd := aStart[i], bEnabled := aEnable[i]);
    GVL_IO.aMotorOut[i] := afbMotor[i].xRunOutput;
END_FOR
```

30 instance tek döngüde; instance pointer'ı cache'lenir, çağrı overhead'i minimuma iner.

## Derin Teknik Detay

### FB Instance = Veri + Davranış Pointer'ı

Bir FB instance, perde arkasında bir **veri bloğu** (VAR_INPUT/OUTPUT/VAR alanları ardışık bellekte) + ortak bir **kod gövdesi**dir. `fbMotor1(...)` çağrısı aslında "bu instance'ın veri bloğunun adresini ortak FB koduna geçir"dir. Bu yüzden:
- N instance, N veri bloğu + 1 kod kopyası (bellek verimli).
- Instance'ın adresi `ADR(fbMotor1)` ile alınabilir, `POINTER TO FB_Motor` ile gezilebilir.
- OOP'ta `THIS^` tam olarak "şu anki instance'ın veri bloğu pointer'ı"dır.

Bu model, C++'taki "nesne = veri + vtable pointer" modelinin PLC karşılığıdır; CODESYS OOP bunun üzerine inşa edilir.

### Encapsulation Neden Determinizmle İlgili

"FB global'e yazmasın, sadece output'a yazsın" kuralı estetik değil; **veri akış yönünü tek yönlü** kılar (fundamentals/_synthesis akış modeli). FB global'e yazarsa:
- İki instance aynı global'i ezer (race, son-yazar-kazanır).
- FB'nin çıktısı artık arayüzünden okunamaz (test edilemez).
- Veri akışı çok yönlü olur, izlenemez.

Output-only yazım, FB'yi saf bir "girişten çıkışa dönüşüm + iç durum" kutusu yapar — çağıran PROGRAM tek "yazar" olarak global'leri yönetir. Bu, GVL "tek-yazar" kuralının (02_gvl_design) FB seviyesindeki ikizidir.

### ELSE'in Savunma Felsefesi: Tanımsız Durum = Tehlikeli Durum

`CASE ... ELSE: eState := eFault` neden hayati? Çünkü `eState` bir bellek hücresidir; RETAIN bozulması, online change, pointer hatası veya enum'a olmayan değer ataması onu tanımsız bir sayıya (`127`) sürükleyebilir. ELSE'siz bir CASE, tanımsız durumda **hiçbir dalı çalıştırmaz** → output'lar son değerlerinde donar → makine "ne TRUE ne FALSE" belirsizliğinde hareket eder. ELSE, "bilmediğim her durumda güvenli duruma kaç" diyen savunma hattıdır — fail-safe tasarımın CASE seviyesindeki ifadesi. Bu, fundamentals'taki determinizm felsefesinin ("her yol öngörülebilir olmalı") kod-seviyesi uygulamasıdır.

### Her Scan Çağrı Zorunluluğunun Kökü

TON/CTU/R_TRIG gibi bloklar **kendi `.ET`/`.CV`'lerini çağrıldıkları anda günceller** — iç zaman tabanları yoktur, çağrı sıklığına göre ilerlerler (bkz. task-structure/01 Not 5). Koşullu çağrı, bu blokların zamanını dondurur. Bu yüzden FB'lerin `bEnabled` gibi bir girişle "her scan çağrıl, davranışı parametreyle kontrol et" deseni temeldir: çağrının kendisi zaman tabanını besler, mantık girişle yönetilir. "Her scan koşulsuz çağır" kuralı, IEC zamanlayıcı bloklarının çağrı-güdümlü doğasının doğrudan sonucudur.

## İlgili Konular

```
knowledge/codesys/programming/
├── 01_pou_types.md          → FB, Program, Function farkı
├── 02_gvl_design.md         → FB'nin GVL ile etkileşimi
├── 04_libraries.md          → FB'yi kütüphaneye dönüştürmek
└── 05_error_handling.md     → FB içinde hata yönetimi deseni

knowledge/codesys/advanced/
├── oop_codesys.md           → FB ile Interface ve Inheritance
└── unit_testing_codesys.md  → FB'yi test etmek

knowledge/codesys/fundamentals/
└── 03_iec61131_languages.md → FB içinde ST, SFC, LD kullanımı
```
