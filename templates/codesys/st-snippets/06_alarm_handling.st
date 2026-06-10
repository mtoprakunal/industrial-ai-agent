// ============================================================
// Alarm Yonetimi Kaliplari
// Aciklama: Alarm latch (gelme/gitme/kabul), seviye siniflandirma,
//           zaman damgasi ve aktif alarm sayaci icerir.
//           Tek alarm noktasi -> FB_Alarm; toplu yonetim -> PRG_AlarmManager.
// Onemli: Analog tetikli alarmlara histerezis + debounce ekleyin
//         (alarm chattering / sel baskini onleme).
// ============================================================

// ------------------------------------------------------------
// Alarm seviyesi (DUT dosyasinda tanimlanir)
// ------------------------------------------------------------
// TYPE E_AlarmLevel :
// (
//     eLevel_None     := 0,
//     eLevel_Dusuk    := 1,   // Bilgi - makine durmaz
//     eLevel_Orta     := 2,   // Uyari - dikkat
//     eLevel_Yuksek   := 3,   // Onemli - mudahale gerek
//     eLevel_Kritik   := 4    // Makine durmali
// );
// END_TYPE


// ============================================================
// FB_Alarm
// Aciklama: Tek bir alarm noktasini yonetir. Latch davranisli:
//           tetik gelince aktif olur, kosul gitse bile operator
//           kabul edene (Ack) kadar kayitli kalir.
//           Yasam dongusu: Gelme -> (Ack) -> Gitme -> Temizlenme.
// Tek sorumluluk: bir alarmin durum makinesi.
// ============================================================
FUNCTION_BLOCK FB_Alarm
VAR_INPUT
    xTrigger    : BOOL;             // Alarm kosulu (TRUE = aktif olmali)
    xAckCmd     : BOOL;             // Operator kabul komutu (yukselen kenar)
    eLevel      : E_AlarmLevel := eLevel_Orta;  // Alarm seviyesi
    sMessage    : STRING(80) := '';             // Operator mesaji
END_VAR
VAR_OUTPUT
    xActive     : BOOL;             // Alarm halen aktif (kosul var)
    xLatched    : BOOL;             // Kayitli (aktif veya kabul bekliyor)
    xUnacked    : BOOL;             // Aktif ama kabul edilmedi (yanip sonme icin)
    dtOnset     : DATE_AND_TIME;    // Geldigi an (zaman damgasi)
    dtClear     : DATE_AND_TIME;    // Gittigi an (zaman damgasi)
END_VAR
VAR
    fbOn        : R_TRIG;           // Tetik yukselen kenar (gelme)
    fbOff       : F_TRIG;           // Tetik dusen kenar (gitme)
    fbAck       : R_TRIG;           // Kabul yukselen kenar
    xAcked      : BOOL;             // Kabul edildi mi
END_VAR

fbOn(CLK := xTrigger);
fbOff(CLK := xTrigger);
fbAck(CLK := xAckCmd);

// --- GELME: yeni alarm ---
IF fbOn.Q THEN
    xLatched := TRUE;
    xAcked   := FALSE;
    dtOnset  := NOW();              // NOT: RTC pili bitikse zaman damgasi bozulur
END_IF

// --- GITME: kosul ortadan kalkti ---
IF fbOff.Q THEN
    dtClear := NOW();
END_IF

// --- KABUL: operator onayladi ---
IF fbAck.Q AND xLatched THEN
    xAcked := TRUE;
END_IF

// --- TEMIZLENME: kosul gitti VE kabul edildi ---
IF NOT xTrigger AND xAcked THEN
    xLatched := FALSE;
END_IF

// --- Cikis ozetleri ---
xActive  := xTrigger;
xUnacked := xLatched AND NOT xAcked;


// ============================================================
// FB_AnalogAlarm
// Aciklama: Analog deger esik asimi alarmi. HISTEREZIS (set != reset)
//           ve DEBOUNCE (TON) ile chattering onler.
//           Ornek: sicaklik > 80 -> alarm; < 78 -> temizle.
// ============================================================
FUNCTION_BLOCK FB_AnalogAlarm
VAR_INPUT
    rValue      : REAL;             // Izlenen deger
    rSetLimit   : REAL := 80.0;     // Alarm tetik esigi
    rResetLimit : REAL := 78.0;     // Alarm cikis esigi (histerezis bandi)
    tDebounce   : TIME := T#500MS;  // Esik asimi stabil kalma suresi
    bHighAlarm  : BOOL := TRUE;     // TRUE=yuksek alarm, FALSE=dusuk alarm
END_VAR
VAR_OUTPUT
    xAlarm      : BOOL;             // Debounce'li alarm cikisi
END_VAR
VAR
    xRaw        : BOOL;             // Histerezisli ham alarm
    tDeb        : TON;
END_VAR

// --- Histerezis (Schmitt-trigger): yon'e gore esikler ---
IF bHighAlarm THEN
    IF rValue >= rSetLimit THEN
        xRaw := TRUE;
    ELSIF rValue <= rResetLimit THEN
        xRaw := FALSE;
    END_IF
ELSE
    // Dusuk alarm: deger esik altina dusunce tetik
    IF rValue <= rSetLimit THEN
        xRaw := TRUE;
    ELSIF rValue >= rResetLimit THEN
        xRaw := FALSE;
    END_IF
END_IF

// --- Debounce: kisa sicramalari yut ---
tDeb(IN := xRaw, PT := tDebounce);
xAlarm := tDeb.Q;


// ============================================================
// PRG_AlarmManager
// Aciklama: Birden cok FB_Alarm instance'ini yonetir, aktif
//           alarm sayisini ve seviye ozetlerini hesaplar.
//           Tum alarm degerlendirmesi orta hizli (10-50ms) task'ta.
// ============================================================
PROGRAM PRG_AlarmManager
VAR
    afbAlarm      : ARRAY[1..16] OF FB_Alarm;   // 16 alarm noktasi
    nActiveCount  : INT;                        // Aktif alarm sayisi
    nUnackedCount : INT;                        // Kabul edilmemis sayisi
    xAnyCritical  : BOOL;                       // Kritik alarm var mi
    xAnyAlarm     : BOOL;                       // Herhangi alarm var mi
    i             : INT;
END_VAR

// --- Ornek: 1 ve 2 numarali alarmlari besle (digerleri benzer) ---
afbAlarm[1](
    xTrigger := GVL_IO.xEStop,
    xAckCmd  := GVL_HMI_Cmd.xCmdReset,
    eLevel   := eLevel_Kritik,
    sMessage := 'Acil stop basili. Reset icin kurtarip onaylayin.'
);
afbAlarm[2](
    xTrigger := GVL_IO.xMotor1Fault,
    xAckCmd  := GVL_HMI_Cmd.xCmdReset,
    eLevel   := eLevel_Yuksek,
    sMessage := 'Motor 1 ariza. Kontaktor K1 kontrol edin.'
);

// --- Ozet sayaclari sifirla, sonra dongude topla ---
nActiveCount  := 0;
nUnackedCount := 0;
xAnyCritical  := FALSE;

FOR i := 1 TO 16 DO
    IF afbAlarm[i].xActive THEN
        nActiveCount := nActiveCount + 1;
        IF afbAlarm[i].eLevel = eLevel_Kritik THEN
            xAnyCritical := TRUE;
        END_IF
    END_IF
    IF afbAlarm[i].xUnacked THEN
        nUnackedCount := nUnackedCount + 1;
    END_IF
END_FOR

xAnyAlarm := nActiveCount > 0;

// --- Global izleme degiskenlerine aktar (PROGRAM yazar) ---
GVL_HMI_Read.nActiveAlarms := nActiveCount;
GVL_HMI_Read.xAnyAlarm     := xAnyAlarm;
