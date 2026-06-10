// ============================================================
// Analog Olcekleme Kalip Koleksiyonu
// Aciklama: FB_AnalogScale (ham -> muhendislik) projede mevcuttur
//           (projects/EXAMPLE_conveyor/program/03_FB_AnalogScale.st).
//           Bu dosya 3 ek kalip sunar:
//             1) FB_AnalogScale KULLANIM ornegi (cagri bicimi)
//             2) FB_EngToRaw  - tersine olcekleme (rEng -> iRaw, 4-20mA cikis)
//             3) FB_EMAFilter - ustel hareketli ortalama (gurultu filtresi)
// Not: Tum sabitler VAR_INPUT veya VAR CONSTANT; sifira bolme korumalidir.
// ============================================================

// ------------------------------------------------------------
// 1) KULLANIM ORNEGI - FB_AnalogScale + filtre zinciri
// ------------------------------------------------------------
// (Bir PROGRAM icinde tipik baglanti)
//
// VAR
//     fbScale  : FB_AnalogScale;
//     fbFilter : FB_EMAFilter;
//     rSpeed   : REAL;
// END_VAR
//
// fbScale(
//     iRaw      := GVL_IO.iSpeedRaw,   // Modul ham deger
//     iRawMin   := GVL_Const.RAW_4MA,
//     iRawMax   := GVL_Const.RAW_20MA,
//     rEngMin   := GVL_Const.SPEED_ENG_MIN,
//     rEngMax   := GVL_Const.SPEED_ENG_MAX,
//     iRawBreak := GVL_Const.RAW_BREAK
// );
//
// fbFilter(rIn := fbScale.rEng, rAlpha := 0.2);  // Yumusatma
// rSpeed := fbFilter.rOut;
//
// GVL_HMI.aZoneSpeed[1] := rSpeed;               // PROGRAM global'e yazar
// GVL_HMI.aZoneTacBrk[1] := fbScale.xUnderRange; // Kablo kopmasi


// ============================================================
// FB_EngToRaw
// Aciklama: Muhendislik birimini ham analog cikisa cevirir.
//           4-20mA analog cikis modulune deger gondermek icin.
//           FB_AnalogScale'in tersidir. Kelepceleme yapar.
// ============================================================
FUNCTION_BLOCK FB_EngToRaw
VAR_INPUT
    rEng     : REAL;    // Yazilacak muhendislik degeri (ornek: %valf acikligi)
    rEngMin  : REAL;    // Muhendislik min (4mA karsiligi)
    rEngMax  : REAL;    // Muhendislik max (20mA karsiligi)
    iRawMin  : INT;     // 4mA karsiligi ham deger
    iRawMax  : INT;     // 20mA karsiligi ham deger
END_VAR
VAR_OUTPUT
    iRaw     : INT;     // Module yazilacak ham deger
END_VAR
VAR
    rEngSpan : REAL;
    rClamped : REAL;
    rRaw     : REAL;
END_VAR

// --- Sifira bolme korumasi ---
rEngSpan := rEngMax - rEngMin;
IF rEngSpan = 0.0 THEN
    iRaw := iRawMin;          // Hatali konfig -> guvenli min cikis
    RETURN;
END_IF

// --- Giris kelepceleme (muhendislik araliginda tut) ---
rClamped := rEng;
IF rClamped > rEngMax THEN
    rClamped := rEngMax;
ELSIF rClamped < rEngMin THEN
    rClamped := rEngMin;
END_IF

// --- Tersine lineer olcekleme ---
rRaw := INT_TO_REAL(iRawMin) +
        ((rClamped - rEngMin) / rEngSpan) * INT_TO_REAL(iRawMax - iRawMin);

iRaw := REAL_TO_INT(rRaw);


// ============================================================
// FB_EMAFilter
// Aciklama: Ustel Hareketli Ortalama (EMA) ile analog sinyal
//           filtreleme. y = alpha*x + (1-alpha)*y_onceki.
//           alpha buyukse hizli (az filtre), kucukse yavas (cok filtre).
//           Gurultulu 4-20mA sinyallerini yumusatmak icin.
// ============================================================
FUNCTION_BLOCK FB_EMAFilter
VAR_INPUT
    rIn      : REAL;            // Ham (gurultulu) giris
    rAlpha   : REAL := 0.2;     // Filtre katsayisi (0.0 < alpha <= 1.0)
END_VAR
VAR_OUTPUT
    rOut     : REAL;            // Filtrelenmis cikis
END_VAR
VAR
    xFirst   : BOOL := TRUE;    // Ilk cevrimde dogrudan yukle
    rAlphaLim: REAL;
END_VAR

// --- Alpha sinir koruma (gecersiz deger filtreyi bozar) ---
rAlphaLim := rAlpha;
IF rAlphaLim <= 0.0 THEN
    rAlphaLim := 0.01;          // Cok yavas ama kararli
ELSIF rAlphaLim > 1.0 THEN
    rAlphaLim := 1.0;           // Filtre yok (cikis = giris)
END_IF

// --- Ilk cevrim: sicrama olmasin diye giris ile baslat ---
IF xFirst THEN
    rOut   := rIn;
    xFirst := FALSE;
ELSE
    rOut := rAlphaLim * rIn + (1.0 - rAlphaLim) * rOut;
END_IF
