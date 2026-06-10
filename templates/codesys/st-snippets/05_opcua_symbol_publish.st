// ============================================================
// OPC-UA Sembol Yayinlama Kaliplari
// Aciklama: PLC degiskenlerini OPC-UA'ya acmanin iki yolu:
//           (A) Symbol Configuration (UI'dan, kod gerekmez) - tavsiye edilen
//           (B) {attribute 'OPC.UA.DA' := '1'} pragma'lari ile kod icinde
//           Bu dosya pragma desenini, salt-okunur/yazilabilir ayrimini
//           ve HMI heartbeat (baglanti kopmasi tespiti) desenini gosterir.
// Altın kural: Kontrol mantigi HMI'da DEGIL PLC'de. HMI komut yazar,
//              PLC izin verirse uygular. Saldiri yuzeyini kucuk tut:
//              yalnizca gerekli degiskenleri ac.
// ============================================================

// ------------------------------------------------------------
// (A) Symbol Configuration yontemi (kod yok, ozet)
// ------------------------------------------------------------
// Application -> Add Object -> Symbol Configuration
//   [x] GVL_HMI_Read   -> Access Level: Read       (salt-okunur izleme)
//   [x] GVL_HMI_Cmd    -> Access Level: ReadWrite   (HMI komutlari)
// Build -> Download. NodeId formati:
//   ns=4;s=|var|<Runtime>.Application.GVL_HMI_Read.rSpeed
// NOT: Degisken adi = API sozlesmesi. Ad degisirse SCADA tag'i kopar.


// ============================================================
// GVL_HMI_Read - Salt-okunur izleme (PLC -> HMI)
// Pragma ile bu blok OPC-UA'ya read-only acilir.
// {attribute 'symbol' := 'read'} -> sembol seti erisimi read
// {attribute 'OPC.UA.DA' := '1'} -> node OPC-UA DA'da yayinlanir
// ============================================================
{attribute 'qualified_only'}
{attribute 'symbol' := 'read'}
VAR_GLOBAL
    {attribute 'OPC.UA.DA' := '1'}
    rSpeed        : REAL;           // m/min - olculen hiz (izleme)
    {attribute 'OPC.UA.DA' := '1'}
    rTemperature  : REAL;           // degC - sicaklik (izleme)
    {attribute 'OPC.UA.DA' := '1'}
    xRunning      : BOOL;           // Calisma durumu (izleme)
    {attribute 'OPC.UA.DA' := '1'}
    xAnyAlarm     : BOOL;           // Genel alarm ozeti (izleme)
    {attribute 'OPC.UA.DA' := '1'}
    nActiveAlarms : INT;            // Aktif alarm sayisi (izleme)
END_VAR


// ============================================================
// GVL_HMI_Cmd - Yazilabilir komutlar (HMI -> PLC)
// Bu degiskenler HMI'dan yazilir; PLC mantigi gecerliligini denetler.
// {attribute 'symbol' := 'readwrite'} -> okunur + yazilir
// ============================================================
{attribute 'qualified_only'}
{attribute 'symbol' := 'readwrite'}
VAR_GLOBAL
    {attribute 'OPC.UA.DA' := '1'}
    xCmdStart     : BOOL;           // HMI calistirma istegi (yalniz oto modda)
    {attribute 'OPC.UA.DA' := '1'}
    xCmdStop      : BOOL;           // HMI durdurma istegi
    {attribute 'OPC.UA.DA' := '1'}
    xCmdReset     : BOOL;           // HMI ariza sifirlama
    {attribute 'OPC.UA.DA' := '1'}
    rSetpoint     : REAL;           // HMI'dan setpoint (PLC kelepceler)
END_VAR


// ============================================================
// GVL_Heartbeat - HMI/SCADA baglanti gozlemi
// PLC her saniye uHbPlc'yi artirir; HMI bunu okuyup
// "PLC canli mi" anlar. HMI da uHbHmi'yi periyodik yazar;
// PLC bunu izleyip "HMI baglantisi kopdu mu" tespit eder.
// ============================================================
{attribute 'qualified_only'}
{attribute 'symbol' := 'readwrite'}
VAR_GLOBAL
    {attribute 'OPC.UA.DA' := '1'}
    uHbPlc        : UDINT;          // PLC -> HMI: PLC canlilik sayaci (read)
    {attribute 'OPC.UA.DA' := '1'}
    uHbHmi        : UDINT;          // HMI -> PLC: HMI canlilik sayaci (write)
    {attribute 'OPC.UA.DA' := '1'}
    xHmiConnected : BOOL;           // PLC tespiti: HMI baglantisi saglam mi
END_VAR


// ============================================================
// PRG_Heartbeat
// Aciklama: PLC heartbeat'i artirir ve HMI heartbeat'ini izler.
//           HMI uHbHmi'yi belirli surede degistirmezse baglanti
//           kopmus kabul edilir (xHmiConnected := FALSE).
//           Bu PROGRAM 100ms-1s araliginda bir task'ta cagrilmali.
// ============================================================
PROGRAM PRG_Heartbeat
VAR_INPUT
    tHmiTimeout   : TIME := T#5S;   // HMI bu surede degismezse kopuk say
    tPlcToggle    : TIME := T#1S;   // PLC heartbeat artirma periyodu
END_VAR
VAR
    tPlcTmr       : TON;
    tHmiTmr       : TON;
    uHbHmiPrev    : UDINT;
END_VAR

// --- PLC heartbeat: her tPlcToggle'da bir artir ---
tPlcTmr(IN := NOT tPlcTmr.Q, PT := tPlcToggle);
IF tPlcTmr.Q THEN
    GVL_Heartbeat.uHbPlc := GVL_Heartbeat.uHbPlc + 1;   // UDINT tasmasi normal (geri sarar)
END_IF

// --- HMI heartbeat izleme: degisiyor mu? ---
IF GVL_Heartbeat.uHbHmi <> uHbHmiPrev THEN
    // HMI heartbeat'i degisti -> baglanti canli, sayaci sifirla
    uHbHmiPrev := GVL_Heartbeat.uHbHmi;
    tHmiTmr(IN := FALSE);
    GVL_Heartbeat.xHmiConnected := TRUE;
ELSE
    // Degismedi -> zaman asimi say
    tHmiTmr(IN := TRUE, PT := tHmiTimeout);
    IF tHmiTmr.Q THEN
        GVL_Heartbeat.xHmiConnected := FALSE;   // HMI baglantisi koptu
    END_IF
END_IF

// Kullanim: baglanti kopunca HMI komutlarini yok say / guvenli duruma gec
// IF NOT GVL_Heartbeat.xHmiConnected THEN ... fail-safe ... END_IF
