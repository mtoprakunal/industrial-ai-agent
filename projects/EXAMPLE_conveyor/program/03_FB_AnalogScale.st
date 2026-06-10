// ============================================================
// FB_AnalogScale
// Aciklama: 4-20mA ham analog degeri muhendislik birimine
//           cevirir. Kablo kopmasi (under-range, NAMUR NE107)
//           ve over-range tespiti yapar. Tek sorumluluk: olcekleme.
// ============================================================
FUNCTION_BLOCK FB_AnalogScale
VAR_INPUT
    iRaw     : INT;    // Modulden gelen ham deger
    iRawMin  : INT;    // 4mA karsiligi ham deger
    iRawMax  : INT;    // 20mA karsiligi ham deger
    rEngMin  : REAL;   // Muhendislik min
    rEngMax  : REAL;   // Muhendislik max
    iRawBreak: INT;    // Altinda kablo kopmasi sayilan esik
END_VAR
VAR_OUTPUT
    rEng       : REAL;   // Olceklenmis deger
    xUnderRange: BOOL;   // Kablo kopmasi / 4mA alti
    xOverRange : BOOL;   // 20mA ustu
END_VAR
VAR
    rSpan : REAL;
END_VAR

// --- Kablo kopmasi kontrolu (once) ---
xUnderRange := (iRaw < iRawBreak);

IF xUnderRange THEN
    rEng := rEngMin;        // Guvenli varsayilan: min deger
    xOverRange := FALSE;
    RETURN;
END_IF

// --- Sifira bolme korumasi ---
rSpan := INT_TO_REAL(iRawMax - iRawMin);
IF rSpan <= 0.0 THEN
    rEng := rEngMin;        // Hatali konfig - guvenli deger
    RETURN;
END_IF

// --- Lineer olcekleme ---
rEng := rEngMin + (INT_TO_REAL(iRaw - iRawMin) / rSpan) * (rEngMax - rEngMin);

// --- Kelepceleme (clamp) ---
xOverRange := (rEng > rEngMax);
IF rEng > rEngMax THEN
    rEng := rEngMax;
ELSIF rEng < rEngMin THEN
    rEng := rEngMin;
END_IF
