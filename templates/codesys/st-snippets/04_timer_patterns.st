// ============================================================
// Timer Kalip Koleksiyonu (TON / TOF / TP)
// Aciklama: Endustride en sik kullanilan zamanlayici desenleri.
//           Tum TON/TOF/TP/BLINK bloklari HER SCAN cagrilmali;
//           kosullu cagri sayaci/zamani dondurur.
//           Sabitler VAR CONSTANT; sihirli sayi yok.
// Icindekiler:
//   1) FB_Debounce  - sinyal sicramasi temizleme (ornek: sikisma 200ms)
//   2) FB_OnDelay   - gecikmeli acma (delayed-on)
//   3) FB_Pulse     - tek atislik darbe (one-shot pulse)
//   4) FB_Blink     - lamba yanip sonme (blink/flash)
//   5) Retentive timer kalibi (akumulatif sure)
// ============================================================

// ============================================================
// FB_Debounce
// Aciklama: Gurultulu/sicrayan dijital girisi filtreler.
//           Giris stabil kalmadikca cikis degismez.
//           Ornek kullanim: sikisma sensoru 200ms debounce.
//           Hem yukselen hem dusen kenar icin ayri gecikme.
// ============================================================
FUNCTION_BLOCK FB_Debounce
VAR_INPUT
    xIn        : BOOL;              // Ham (gurultulu) giris
    tOnDelay   : TIME := T#200MS;   // Aktif kabul icin stabil kalma suresi
    tOffDelay  : TIME := T#200MS;   // Pasif kabul icin stabil kalma suresi
END_VAR
VAR_OUTPUT
    xOut       : BOOL;              // Filtrelenmis (debounce edilmis) cikis
    xRising    : BOOL;              // Cikista yukselen kenar (tek scan)
    xFalling   : BOOL;              // Cikista dusen kenar (tek scan)
END_VAR
VAR
    tOn        : TON;
    tOff       : TON;
    xOutPrev   : BOOL;
END_VAR

// Giris TRUE'da kalmissa onu kabul et
tOn(IN := xIn, PT := tOnDelay);
// Giris FALSE'ta kalmissa onu kabul et
tOff(IN := NOT xIn, PT := tOffDelay);

IF tOn.Q THEN
    xOut := TRUE;
ELSIF tOff.Q THEN
    xOut := FALSE;
END_IF

xRising  := xOut AND NOT xOutPrev;
xFalling := NOT xOut AND xOutPrev;
xOutPrev := xOut;


// ============================================================
// FB_OnDelay
// Aciklama: Giris TRUE olduktan tPreset sure sonra cikis TRUE.
//           Giris FALSE olunca cikis aninda FALSE (klasik TON).
//           Ornek: motor calistiktan 3s sonra "kararli" bayragi.
// ============================================================
FUNCTION_BLOCK FB_OnDelay
VAR_INPUT
    xIn        : BOOL;
    tPreset    : TIME := T#3S;      // Gecikme suresi
END_VAR
VAR_OUTPUT
    xOut       : BOOL;              // Gecikmeli cikis
    tElapsed   : TIME;              // Gecen sure (HMI gosterimi)
END_VAR
VAR
    tDelay     : TON;
END_VAR

tDelay(IN := xIn, PT := tPreset);
xOut     := tDelay.Q;
tElapsed := tDelay.ET;


// ============================================================
// FB_Pulse
// Aciklama: Yukselen kenarda sabit sureli tek darbe uretir (TP).
//           Giris ne kadar uzun TRUE kalirsa kalsin darbe suresi sabit.
//           Ornek: buton basisinda 500ms'lik sesli uyari/kornaya darbe.
// ============================================================
FUNCTION_BLOCK FB_Pulse
VAR_INPUT
    xTrig      : BOOL;              // Tetik (yukselen kenar)
    tWidth     : TIME := T#500MS;   // Darbe genisligi
END_VAR
VAR_OUTPUT
    xPulse     : BOOL;              // Darbe cikisi
END_VAR
VAR
    fbTP       : TP;
END_VAR

fbTP(IN := xTrig, PT := tWidth);
xPulse := fbTP.Q;


// ============================================================
// FB_Blink
// Aciklama: Cikisi simetrik/asimetrik yanip-sondurur (lamba flash).
//           xEnable TRUE iken tOn/tOff periyotlariyla titresir.
//           Ornek: aktif alarm lambasi yanip sonsun.
// ============================================================
FUNCTION_BLOCK FB_Blink
VAR_INPUT
    xEnable    : BOOL;              // Yanip sonmeyi etkinlestir
    tOnTime    : TIME := T#500MS;   // Yanik kalma suresi
    tOffTime   : TIME := T#500MS;   // Sonuk kalma suresi
END_VAR
VAR_OUTPUT
    xOut       : BOOL;              // Lamba cikisi
END_VAR
VAR
    tOnTmr     : TON;
    tOffTmr    : TON;
END_VAR

IF NOT xEnable THEN
    xOut := FALSE;
    tOnTmr(IN := FALSE);
    tOffTmr(IN := FALSE);
ELSE
    // Sonuk fazi bitince yak; yanik fazi bitince sondur
    tOffTmr(IN := NOT xOut, PT := tOffTime);
    IF tOffTmr.Q THEN
        xOut := TRUE;
    END_IF

    tOnTmr(IN := xOut, PT := tOnTime);
    IF tOnTmr.Q THEN
        xOut := FALSE;
    END_IF
END_IF


// ============================================================
// FB_RetentiveTimer
// Aciklama: Akumulatif (retentive) zamanlayici. TON'dan farki:
//           giris kesilince sayac SIFIRLANMAZ, durur ve kaldigi
//           yerden devam eder. xReset ile sifirlanir.
//           Ornek: motorun toplam calisma suresini olcmek.
// ============================================================
FUNCTION_BLOCK FB_RetentiveTimer
VAR_INPUT
    xIn        : BOOL;              // Sayma kosulu (TRUE iken biriktir)
    xReset     : BOOL;              // Akumlatoru sifirla
    tPreset    : TIME := T#0S;      // 0 = sinir yok; >0 ise Q icin esik
END_VAR
VAR_OUTPUT
    tAccum     : TIME;              // Birikmis sure
    xDone      : BOOL;              // tAccum >= tPreset (preset>0 ise)
END_VAR
VAR
    tSlice     : TON;               // Bir scan'lik dilim olcumu
    tCycle     : TIME := T#10MS;    // Task cycle time (gercege gore ayarla)
END_VAR

IF xReset THEN
    tAccum := T#0S;
    xDone  := FALSE;
END_IF

// Her scan, kosul aktifse cycle time kadar ekle
IF xIn THEN
    tAccum := tAccum + tCycle;
END_IF

IF tPreset > T#0S THEN
    xDone := tAccum >= tPreset;
END_IF
