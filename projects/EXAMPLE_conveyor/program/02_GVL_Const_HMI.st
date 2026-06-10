// ============================================================
// GVL_Const — Sabitler (sihirli sayi yok kurali)
// ============================================================
{attribute 'qualified_only'}
VAR_GLOBAL CONSTANT
    // Analog olcekleme (4-20mA, modul ham deger araligi varsayimi 0..32767)
    RAW_4MA      : INT  := 6553;     // 4mA  -> ham deger (~%20)
    RAW_20MA     : INT  := 32767;    // 20mA -> ham deger (tam skala)
    RAW_BREAK    : INT  := 3276;     // <2mA -> kablo kopmasi esigi (NAMUR NE107)
    SPEED_ENG_MIN: REAL := 0.0;      // m/min
    SPEED_ENG_MAX: REAL := 120.0;    // m/min

    // Hiz arizasi tespiti
    SPEED_MIN_RUN  : REAL := 5.0;          // Calisirken beklenen min hiz (m/min)
    T_SPEED_CHECK  : TIME := T#2S;         // Hiz kontrol gecikmesi

    // Zamanlamalar
    T_JAM_DEBOUNCE : TIME := T#200MS;      // Sikisma debounce (spec)
    T_START_RAMP   : TIME := T#500MS;      // Baslatma gecis suresi
    T_STOP_RAMP    : TIME := T#300MS;      // Durdurma gecis suresi
END_VAR

// ============================================================
// GVL_HMI — OPC-UA / HMI'a acilan degiskenler
// Bu degiskenler Symbol Configuration ile OPC-UA node olur.
// HMI yalniz OPC-UA uzerinden okur; kontrol mantigi HMI'da DEGIL.
// Komutlar (xCmd*) HMI'dan yazilir; geri kalan salt-okunur izlemedir.
// ============================================================
{attribute 'qualified_only'}
VAR_GLOBAL
    // Izleme (PLC -> HMI, salt okunur)
    aZoneState   : ARRAY[1..3] OF E_ZoneState;   // Bolge durumlari
    aZoneSpeed   : ARRAY[1..3] OF REAL;          // m/min
    aZoneRunning : ARRAY[1..3] OF BOOL;
    aZoneJam     : ARRAY[1..3] OF BOOL;
    aZoneSpdFlt  : ARRAY[1..3] OF BOOL;
    aZoneTacBrk  : ARRAY[1..3] OF BOOL;           // Takometre kablo kopmasi
    aZoneAuto    : ARRAY[1..3] OF BOOL;
    xEStopActive : BOOL;                          // A001
    xRunPermit   : BOOL;                          // PLT_PMT durumu
    xZone2Itlk   : BOOL;                          // A060 interlock blokaji
    xAnyAlarm    : BOOL;

    // Komut (HMI -> PLC) — yalniz OTO modda gecerli, manuelde butonlar onceliklidir
    axCmdAutoRun : ARRAY[1..3] OF BOOL;           // Oto mod calistirma istegi
    xCmdReset    : BOOL;                          // HMI'dan reset (PLT_RST ile OR'lanir)

    // Heartbeat — HMI baglanti kopmasini tespit eder (her saniye toggle)
    uHeartbeat   : UDINT;
END_VAR
