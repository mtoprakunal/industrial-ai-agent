// ============================================================
// Hata Yonetimi ve Watchdog Kaliplari
// Aciklama: Haberlesme/HMI watchdog (heartbeat timeout), task
//           watchdog kavrami, guvenli duruma gecis (fail-safe)
//           ve TRY benzeri hata yonetimi (CmpError/status kodu).
// Hata yonetimi felsefesi (knowledge/.../05_error_handling.md):
//   Savunmaci onleme + katmanli fail-safe. CODESYS'te genel
//   try/catch yoktur (64-bit'te __TRY hic yok). Onleme esastir.
// ============================================================

// ============================================================
// FB_CommWatchdog
// Aciklama: Bir haberlesme/HMI ortaginin heartbeat'ini izler.
//           Sayac belirli surede degismezse "kopuk" tespit eder.
//           Toparlanma: sayac yeniden degisirse otomatik temizlenir.
// Tek sorumluluk: heartbeat zaman asimi tespiti.
// ============================================================
FUNCTION_BLOCK FB_CommWatchdog
VAR_INPUT
    uHeartbeat  : UDINT;            // Karsi tarafin canlilik sayaci
    tTimeout    : TIME := T#3S;     // Bu surede degismezse kopuk say
    xEnable     : BOOL := TRUE;     // FALSE -> izleme yapma (saglikli kabul)
END_VAR
VAR_OUTPUT
    xConnected  : BOOL := TRUE;     // Baglanti saglam mi
    xTimeout    : BOOL;             // Zaman asimi olustu mu
    uFailCount  : UDINT;            // Toplam kopma sayisi (diagnostik)
END_VAR
VAR
    uHbPrev     : UDINT;
    tWdTmr      : TON;
    xWasConn    : BOOL := TRUE;
END_VAR

IF NOT xEnable THEN
    xConnected := TRUE;
    xTimeout   := FALSE;
    tWdTmr(IN := FALSE);
    uHbPrev    := uHeartbeat;
    RETURN;
END_IF

IF uHeartbeat <> uHbPrev THEN
    // Heartbeat ilerledi -> baglanti canli
    uHbPrev := uHeartbeat;
    tWdTmr(IN := FALSE);
    xConnected := TRUE;
    xTimeout   := FALSE;
ELSE
    // Degismedi -> zaman asimi say
    tWdTmr(IN := TRUE, PT := tTimeout);
    IF tWdTmr.Q THEN
        xConnected := FALSE;
        xTimeout   := TRUE;
    END_IF
END_IF

// Yeni kopma kenarini say (diagnostik)
IF xWasConn AND NOT xConnected THEN
    uFailCount := uFailCount + 1;
END_IF
xWasConn := xConnected;


// ============================================================
// FB_TryReadStatus - TRY benzeri durum-kodu hata yonetimi
// Aciklama: CODESYS'te genel try/catch yerine kutuphane FB'leri
//           bir status/error kodu doner (CmpError mantigi).
//           Bu sablon o kodu yorumlayip katmanli tepki uretir:
//           yeniden dene -> belirli sayidan sonra ariza.
// Not: 64-bit sistemde __TRY/__CATCH calismaz; savunmaci
//      durum-kodu denetimi tasinabilir ve guvenli yoldur.
// ============================================================
FUNCTION_BLOCK FB_TryReadStatus
VAR_INPUT
    xDone       : BOOL;             // Islem tamamlandi (kutuphane FB cikisi)
    xError      : BOOL;             // Islem hatali (kutuphane FB cikisi)
    wErrorId    : WORD;             // Hata kodu (kutuphane FB cikisi)
    nMaxRetries : INT := 3;         // Ariza ilan etmeden once deneme sayisi
    tRetryDelay : TIME := T#1S;     // Denemeler arasi bekleme
END_VAR
VAR_OUTPUT
    xOk         : BOOL;             // Basariyla tamamlandi
    xRetry      : BOOL;             // Yeniden deneme tetigi (tek scan)
    xFault      : BOOL;             // Kalici ariza (deneme tukendi)
    nRetryCount : INT;              // Yapilan deneme sayisi
    sFaultMsg   : STRING(80);
END_VAR
VAR
    fbErr       : R_TRIG;
    tRetryTmr   : TON;
END_VAR

xRetry := FALSE;
fbErr(CLK := xError);

IF xDone AND NOT xError THEN
    // --- Basari: temizle ---
    xOk         := TRUE;
    xFault      := FALSE;
    nRetryCount := 0;
    sFaultMsg   := '';
    tRetryTmr(IN := FALSE);

ELSIF fbErr.Q THEN
    // --- Yeni hata kenari: say ---
    xOk := FALSE;
    nRetryCount := nRetryCount + 1;

    IF nRetryCount >= nMaxRetries THEN
        // Deneme tukendi -> kalici ariza
        xFault    := TRUE;
        sFaultMsg := CONCAT('Islem basarisiz. Hata kodu: ', WORD_TO_STRING(wErrorId));
    ELSE
        // Yeniden denemek icin bekleme baslat
        tRetryTmr(IN := TRUE, PT := tRetryDelay);
    END_IF

ELSIF tRetryTmr.Q THEN
    // --- Bekleme bitti -> yeniden dene ---
    tRetryTmr(IN := FALSE);
    xRetry := TRUE;
END_IF


// ============================================================
// PRG_SafeState - Fail-safe (guvenli duruma gecis)
// Aciklama: Kritik hata/watchdog/baglanti kopmasi durumunda
//           tum tehlikeli ciktilari guvenli konuma getirir.
//           IDEAL: ayri, yuksek oncelikli Task_Safety'de calistir;
//           boylece Task_Control watchdog'undan bagimsiz korur.
// UYARI: CODESYS V3'te watchdog SADECE application'i durdurur;
//        fiziksel cikislar fieldbus fail-safe ayarina gore davranir
//        (otomatik 0 DEGIL). Slave fail-safe degerleri ayrica
//        konfigure edilmeli ve fiziksel test edilmelidir.
// ============================================================
PROGRAM PRG_SafeState
VAR_INPUT
    xSystemOk     : BOOL;           // Genel sistem saglikli mi
    xCommOk       : BOOL;           // Haberlesme saglikli mi
    xAnyCritical  : BOOL;           // Kritik alarm var mi
END_VAR
VAR
    xSafeStateNeeded : BOOL;
END_VAR

// --- Guvenli durum kosulu ---
xSafeStateNeeded := NOT xSystemOk OR NOT xCommOk OR xAnyCritical;

IF xSafeStateNeeded THEN
    // Tum tehlikeli ciktilari kapat (fail-safe)
    GVL_IO.xMotor1Out := FALSE;
    GVL_IO.xMotor2Out := FALSE;
    GVL_IO.xHeaterOut := FALSE;
    GVL_IO.xValveOut  := FALSE;     // NOT: vana fail-safe yonu prosese gore
END_IF


// ============================================================
// Task Watchdog yapilandirmasi (kavram - kod degil)
// ============================================================
// Task Configuration -> MainTask -> Configuration:
//   Watchdog        : Enabled
//   Time            : ~2-5 x beklenen Max Exec Time (ornek t#50ms)
//   Sensitivity     : 2-3 (tek spike'i tolere et, kalici sorunu yakala)
//
// Watchdog tetiklenince (V3):
//   1. Etkilenen Application durur (runtime devam eder)
//   2. Fiziksel cikislar -> fieldbus fail-safe ayarina gore
//   3. CODESYS Log'a kayit
//   4. Otomatik restart YOK - Application event handler gerekir
//
// Guvenlik: kritik cikislari ayri Task_Safety + donanim watchdog
//           rolesi ile koru. "STOP = guvenli" otomatik DEGILDIR.
