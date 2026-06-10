// ============================================================
// FB_MotorStartStop
// Aciklama: Tek bir motorun start/stop mantigini yonetir.
//           Start butonu (NO), Stop butonu (NC tel-emniyetli),
//           interlock girisi, calisma geri beslemesi ve
//           kilitlenen (latch) ariza + reset icerir.
//           Tek sorumluluk: motor calistir/durdur mantigi.
//           Cikis I/O'ya YALNIZCA cagiran PROGRAM tarafindan baglanir.
// Not: Set/Reset cakismasinda STOP/ariza her zaman ONCELIKLIDIR
//      (reset dominant durdurma -> guvenli taraf).
// ============================================================
FUNCTION_BLOCK FB_MotorStartStop
VAR_INPUT
    // --- Komutlar ---
    xStartBtn   : BOOL;             // Start butonu (NO) - yukselen kenarda calistir
    xStopBtn    : BOOL;             // Stop butonu (NC) - TRUE = stop basili DEGIL
                                    //   yani kablo koparsa/buton basilirsa FALSE -> durdur
    xInterlock  : BOOL := TRUE;     // Calismaya izin (TRUE = izin var)
    xFaultReset : BOOL;             // Ariza sifirlama - yukselen kenar

    // --- Geri besleme ---
    xRunFeedback: BOOL;             // Kontaktor/yardimci kontak geri beslemesi

    // --- Konfigurasyon (sihirli sayi yok) ---
    tFbTimeout  : TIME := T#2S;     // Geri besleme gelmezse ariza gecikmesi
    bUseFeedback: BOOL := TRUE;     // FALSE -> geri besleme denetimi yapma
END_VAR
VAR_OUTPUT
    xRunOutput  : BOOL;             // Motor calistirma cikisi -> I/O'ya baglanir
    xRunning    : BOOL;             // Onaylanmis calisma durumu
    xReady      : BOOL;             // Bos, ariza yok, start bekliyor
    xFault      : BOOL;             // Kilitli ariza bayragi
    sFaultMsg   : STRING(80);       // Operatore bilgi mesaji
END_VAR
VAR
    fbStart     : R_TRIG;           // Start butonu yukselen kenar
    fbReset     : R_TRIG;           // Reset yukselen kenar
    tFbTimer    : TON;              // Geri besleme zaman asimi
    xCmdRun     : BOOL;             // Dahili calistirma istegi (latch)
END_VAR

// --- Kenar tespitleri (her scan cagrilmali) ---
fbStart(CLK := xStartBtn);
fbReset(CLK := xFaultReset);

// --- Ariza sifirlama (yalnizca kosul gitmisse) ---
IF fbReset.Q AND NOT (xRunFeedback AND NOT xRunOutput) THEN
    xFault    := FALSE;
    sFaultMsg := '';
END_IF

// --- Calistirma istegi: SET (start kenari) ---
IF fbStart.Q AND xInterlock AND NOT xFault THEN
    xCmdRun := TRUE;
END_IF

// --- Durdurma kosullari: RESET DOMINANT (guvenli taraf) ---
// Stop butonu NC: xStopBtn = FALSE -> durdur. Interlock kaybi -> durdur.
IF NOT xStopBtn OR NOT xInterlock OR xFault THEN
    xCmdRun := FALSE;
END_IF

// --- Fiziksel cikis ---
xRunOutput := xCmdRun AND NOT xFault;

// --- Geri besleme denetimi (kontaktor cekti mi?) ---
IF bUseFeedback THEN
    // Komut var ama geri besleme yok -> zaman asimi say
    tFbTimer(IN := (xRunOutput AND NOT xRunFeedback), PT := tFbTimeout);
    IF tFbTimer.Q THEN
        xFault    := TRUE;
        sFaultMsg := 'Motor calisma geri beslemesi yok. Kontaktor ve kabloyu kontrol edin.';
    END_IF

    // Komut yokken geri besleme varsa -> yapisik kontaktor (tehlikeli)
    IF NOT xRunOutput AND xRunFeedback THEN
        xFault    := TRUE;
        sFaultMsg := 'Beklenmeyen geri besleme. Kontaktor yapismis olabilir.';
    END_IF

    xRunning := xRunOutput AND xRunFeedback;
ELSE
    // Geri besleme yoksa cikis = calisma kabul edilir
    tFbTimer(IN := FALSE);
    xRunning := xRunOutput;
END_IF

// --- Hazir durumu ozeti ---
xReady := NOT xRunOutput AND NOT xFault AND xInterlock AND xStopBtn;
