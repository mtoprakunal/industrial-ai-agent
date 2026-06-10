// ============================================================
// FB_SimplePID
// Aciklama: Elle yazilmis konum-tipi (positional) PID kontrolor.
//           Anti-windup (integral clamp), manuel/oto bumpless
//           gecis ve cikis kelepceleme icerir.
//           Tek sorumluluk: PID hesabi (olcekleme/IO ayri FB'de).
// Not: CODESYS standart kutuphanesinde FB_PID hazir vardir;
//      bu FB egitim/tasinabilirlik icin saydam bir alternatiftir.
//      Her scan cagrilmali (TON yok ama integral durum tutar).
// Birim: rKp birimsiz; rTi/rTd SANIYE cinsinden; tCycle PID periyodu.
// ============================================================
FUNCTION_BLOCK FB_SimplePID
VAR_INPUT
    rActual    : REAL;              // Olcum (process value)
    rSetpoint  : REAL;              // Hedef deger

    // --- Mod ---
    bAuto      : BOOL := TRUE;      // FALSE -> manuel mod
    rManOut    : REAL;              // Manuel modda cikis degeri

    // --- PID parametreleri (sihirli sayi yok) ---
    rKp        : REAL := 1.0;       // Oransal kazanc
    rTi        : REAL := 10.0;      // Integral zamani [s] (0 = I kapali)
    rTd        : REAL := 0.0;       // Turev zamani [s]   (0 = D kapali)
    tCycle     : TIME := T#100MS;   // PID cevrim suresi (task cycle ile esit)

    // --- Cikis sinirlari ---
    rOutMin    : REAL := 0.0;       // Min cikis (ornek: %0)
    rOutMax    : REAL := 100.0;     // Max cikis (ornek: %100)
END_VAR
VAR_OUTPUT
    rOut       : REAL;              // PID cikisi (kelepcelenmis)
    bSatHigh   : BOOL;              // Cikis ust limitte (doygunluk)
    bSatLow    : BOOL;              // Cikis alt limitte (doygunluk)
    rError     : REAL;              // Anlik hata (SP - PV)
END_VAR
VAR
    rIntegral  : REAL;              // Integral birikim
    rPrevError : REAL;              // Onceki hata (turev icin)
    rDt        : REAL;              // Cevrim suresi [s]
    rP         : REAL;
    rI         : REAL;
    rD         : REAL;
    rRaw       : REAL;              // Kelepcelemeden onceki cikis
    bFirstScan : BOOL := TRUE;
END_VAR

// --- Cevrim suresi [s] (sifira bolme korumasi) ---
rDt := TIME_TO_REAL(tCycle) / 1000.0;
IF rDt <= 0.0 THEN
    rDt := 0.1;                     // Guvenli varsayilan 100ms
END_IF

// --- Limit tutarlilik korumasi ---
IF rOutMax <= rOutMin THEN
    rOutMax := rOutMin + 1.0;       // Hatali konfig -> en az 1 birim aralik
END_IF

rError := rSetpoint - rActual;

IF bAuto THEN
    // ---------- OTO MOD ----------
    // P terimi
    rP := rKp * rError;

    // I terimi (rTi=0 -> integral kapali)
    IF rTi > 0.0 THEN
        rIntegral := rIntegral + (rKp / rTi) * rError * rDt;
    ELSE
        rIntegral := 0.0;
    END_IF
    rI := rIntegral;

    // D terimi (turev; ilk scan'de atlama olmasin)
    IF (rTd > 0.0) AND NOT bFirstScan THEN
        rD := rKp * rTd * (rError - rPrevError) / rDt;
    ELSE
        rD := 0.0;
    END_IF

    rRaw := rP + rI + rD;

    // --- Cikis kelepceleme + ANTI-WINDUP ---
    // Cikis doygunlukta ise integrali geri sar (sinirda dondur).
    IF rRaw > rOutMax THEN
        rOut     := rOutMax;
        bSatHigh := TRUE;
        bSatLow  := FALSE;
        // Anti-windup: fazla biriken integrali geri al
        rIntegral := rIntegral - (rRaw - rOutMax);
    ELSIF rRaw < rOutMin THEN
        rOut     := rOutMin;
        bSatHigh := FALSE;
        bSatLow  := TRUE;
        rIntegral := rIntegral - (rRaw - rOutMin);
    ELSE
        rOut     := rRaw;
        bSatHigh := FALSE;
        bSatLow  := FALSE;
    END_IF

ELSE
    // ---------- MANUEL MOD ----------
    // Manuel cikisi kelepcele
    IF rManOut > rOutMax THEN
        rOut := rOutMax;
    ELSIF rManOut < rOutMin THEN
        rOut := rOutMin;
    ELSE
        rOut := rManOut;
    END_IF
    bSatHigh := FALSE;
    bSatLow  := FALSE;

    // BUMPLESS TRANSFER hazirligi:
    // Manueldeyken integrali mevcut cikisa esitle ki OTO'ya
    // gecince cikis sicramasin (P ve D anlik hesaplanir).
    rIntegral := rOut - rKp * rError;
END_IF

rPrevError := rError;
bFirstScan := FALSE;

// ------------------------------------------------------------
// CODESYS STANDART FB_PID KULLANIMI (alternatif)
// ------------------------------------------------------------
// VAR fbPID : FB_PID; END_VAR  // Standard.library / Util.library
//
// fbPID(
//     fActualValue   := rActual,
//     fSetpointValue := rSetpoint,
//     fKp            := 1.0,
//     fTn            := 10.0,                       // Integral zamani [s]
//     fTv            := 0.5,                        // Turev zamani [s]
//     fOutMinLimit   := 0.0,
//     fOutMaxLimit   := 100.0,
//     bManMode       := NOT bAuto,
//     fManValue      := rManOut,
//     fCycleTime     := TIME_TO_REAL(T#100MS) / 1000.0  // [s]
// );
// rOut := fbPID.fOut;
