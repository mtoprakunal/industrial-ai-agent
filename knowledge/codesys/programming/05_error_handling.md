---
KONU        : CODESYS'te Hata Yönetimi
KATEGORİ    : codesys
ALT_KATEGORI: programming
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://wiki.kontron.ch/kchcdsv3/codesys-exception-handling"
    başlık: "Kontron Wiki — CODESYS Exception Handling"
    güvenilirlik: topluluk
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_operator_try_catch_finally_endtry.html"
    başlık: "CODESYS Online Help — __TRY/__CATCH/__FINALLY/__ENDTRY"
    güvenilirlik: resmi
  - url: "https://stefanhenneken.net/2019/07/29/iec-61131-3-exception-handling-with-__try-__catch/"
    başlık: "Stefan Henneken — IEC 61131-3 Exception Handling with __TRY/__CATCH"
    güvenilirlik: topluluk
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_f_reference_task.html"
    başlık: "CODESYS Online Help — Task Watchdog Reference"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "02_gvl_design.md"
    ilişki: kullanır
  - konu: "03_function_blocks.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/task-structure/01_task_types.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Watchdog kavramı (task-structure/01_task_types.md)"
  - "GVL_Alarms tasarımı (02_gvl_design.md)"
  - "Function Block state machine (03_function_blocks.md)"
ÇELİŞKİLER :
  - kaynak: "CODESYS __TRY/__CATCH desteği"
    konu: "__TRY/__CATCH yalnızca 32-bit platformlarda desteklenir; 64-bit sistemlerde desteklenmez"
    çözüm: >
      Modern x64 endüstriyel PC'lerde __TRY/__CATCH çalışmaz.
      Bu kısıt CODESYS'in 64-bit runtime desteğiyle ilgili mimari bir sorundur.
      64-bit sistemlerde IEC kodunda savunmacı programlama (sınır kontrolleri,
      null pointer önleme) tercih edilmeli; kritik bölümler için __TRY yerine
      dizi erişim koruması ve pointer güvenlik kontrolleri kullanılmalıdır.
  - kaynak: "Watchdog davranışı — V2 vs V3"
    konu: "V2'de watchdog PLC'yi reboot ederken V3'te yalnızca uygulamayı durdurur"
    çözüm: >
      CODESYS V3'te watchdog tetiklenirse yalnızca ilgili Application ve
      child application'ları durur; runtime çalışmaya devam eder.
      Otomatik yeniden başlatma için ek kod (Application event handler veya
      harici watchdog hardware) gerektirir. Bu V2 alışkanlığından gelen
      mühendisler için sürpriz yaratabilir.
---

## Özün Ne

CODESYS'te Java veya Python'daki gibi genel bir `try/catch` mekanizması yoktur (ve 64-bit sistemlerde hiç yoktur). Bunun yerine hata yönetimi dört katmanlı bir yaklaşımla sağlanır: **Task Watchdog** (runtime koruyucusu), **FB içi savunmacı programlama** (logic katman koruması), **Diagnostik değişkenler** (durum raporlama), ve **Operatör bilgilendirme** (insan arayüzü). Bu dört katmanın biri bile eksik olduğunda, üretim ortamında saatlerce süren debuglar kaçınılmaz hale gelir.

## Nasıl Çalışır

### Katman 1: Task Watchdog — Runtime Koruması

Watchdog, task'ın belirlenen sürede tamamlanmasını garantiler. İki türü vardır:

**Normal Watchdog:**
```
Tetikleme koşulu: Exec Time > Watchdog Time

Yapılandırma:
  Task Configuration → MainTask → Configuration →
    Watchdog: ✓ Enabled
    Time: t#50ms          (Cycle Time'ın 3-5 katı önerilir)
    Sensitivity: 3        (3 ardışık ihlalde tetikle)
```

**Omitted Cycle Watchdog:**
```
Tetikleme koşulu: Task Time × Sensitivity içinde task hiç çalışmadı
(Yüksek öncelikli task CPU'yu tüketiyor, bu task hiç başlayamıyor)

Sensitivity: 3 → Interval × 3 = 30ms'de hiç çalışmazsa → tetiklenir
```

**Watchdog Tetiklenince Ne Olur?**
```
CODESYS V3 davranışı:
  1. Etkilenen Application durdurulur (Runtime değil, Application!)
  2. Fiziksel çıkışlar: Son değerlerinde kilitlenir (cihaz durur/çalışır kalabilir)
  3. CODESYS Log'a kayıt: "Watchdog exception in Task_Control"
  4. Runtime çalışmaya devam eder — diğer Application'lar etkilenmez
  5. Otomatik yeniden başlatma: Varsayılan olarak YOK — manuel müdahale gerekir
```

**Watchdog Sonrası Çıkış Güvenliği:**

Fiziksel çıkışların son değerde kalması tehlikelidir. Güvenli tasarım:

```iecst
(* Güvenlik çıkışları: Watchdog sonrası "fail-safe" konumuna geçmeli *)
(* Bunu sağlamanın yolu: Güvenlik çıkışlarını ayrı, yüksek öncelikli
   Task_Safety'de yönetmek. Task_Safety watchdog'u Task_Control'den bağımsız. *)

(* Task_Safety (Prio:0, 1ms) içinde: *)
PRG_Safety():
    IF NOT GVL_State.xSystemOK THEN
        GVL_IO.xMotor1_Out := FALSE;   (* Motor durdur *)
        GVL_IO.xHeater_Out  := FALSE;  (* Isıtıcı kapat *)
        GVL_IO.xValve_Out   := FALSE;  (* Vanayı kapat *)
    END_IF
```

### Katman 2: `__TRY/__CATCH` — Çalışma Zamanı İstisnaları (32-bit Sistemler)

CODESYS'in `__TRY/__CATCH/__FINALLY/__ENDTRY` operatörleri, donanım seviyesinde oluşan istisnaları yakalamak için kullanılır:

```iecst
(* __TRY/__CATCH — YALNIZCA 32-BIT PLATFORMLARDA *)
VAR
    eExceptCode : ExceptionCode;
    pData       : POINTER TO DWORD;
    dwData      : DWORD;
END_VAR

__TRY
    (* Tehlikeli işlem: Null pointer erişimi *)
    pData := 0;              (* Null pointer *)
    dwData := pData^;        (* Bu satır normalde exception fırlatır *)

__CATCH(eExceptCode)
    (* Exception yakalandı — güvenli duruma geç *)
    GVL_Alarms.xRuntimeException := TRUE;
    GVL_Alarms.sLastExceptionMsg  := CONCAT('Runtime exception: ', 
                                            DWORD_TO_STRING(DWORD(eExceptCode)));
    (* Program devam eder — runtime durmaz *)

__FINALLY
    (* Exception olsun ya da olmasın çalışır — temizlik *)
    pData := 0;

__ENDTRY
```

**ExceptionCode Değerleri:**
```
RTSEXCPT_NOEXCEPTION      := 0           → İstisna yok
RTSEXCPT_WATCHDOG         := 16#10       → Watchdog tetiklendi
RTSEXCPT_IO_CONFIG_ERROR  := 16#12       → I/O yapılandırma hatası
RTSEXCPT_FIELDBUS_ERROR   := 16#14       → Fieldbus hatası
RTSEXCPT_CYCLE_TIME_EXCEED:= 16#16       → Döngü süresi aşıldı
RTSEXCPT_OUT_OF_MEMORY    := 16#1C       → Bellek yetersiz
RTSEXCPT_UNRESOLVED_EXTREFS := 16#18     → Çözülemeyen dış referans
```

**64-bit sistemlerde alternatif (pointer koruması):**

```iecst
(* 64-bit sistemlerde __TRY yerine savunmacı programlama *)
IF pData <> 0 THEN          (* Null kontrol *)
    dwData := pData^;       (* Güvenli erişim *)
ELSE
    GVL_Alarms.xNullPointerDetected := TRUE;
END_IF
```

### Katman 3: FB İçi Savunmacı Programlama

Her FB, kötü giriş verisini işleyebilmeli ve hata durumunu raporlayabilmelidir.

```iecst
(* Savunmacı FB — Kötü giriş verisi koruması *)
FUNCTION_BLOCK FB_AnalogSensor
VAR_INPUT
    rRawADC    : REAL;          (* Ham ADC değeri *)
    rRawMin    : REAL := 0.0;
    rRawMax    : REAL := 4095.0;
    rEngMin    : REAL := 0.0;
    rEngMax    : REAL := 100.0;
    tTimeout   : TIME := T#5S;  (* Değer değişmezse timeout *)
END_VAR
VAR_OUTPUT
    rEngValue  : REAL;          (* Mühendislik birimi *)
    xValid     : BOOL;          (* Değer güvenilir mi *)
    xFault     : BOOL;          (* Arıza bayrağı *)
    eFaultCode : E_SensorFault; (* Hata kodu *)
    sFaultMsg  : STRING(80);
END_VAR
VAR
    rLastValue : REAL;
    tFrozenTimer : TON;        (* Değer donmuş mu? *)
END_VAR

(* Giriş aralık kontrolü *)
IF rRawMax <= rRawMin THEN
    xFault    := TRUE;
    eFaultCode := eSensorFault_ConfigError;
    sFaultMsg  := 'Config error: rRawMax <= rRawMin';
    xValid    := FALSE;
    RETURN;
END_IF

(* ADC değeri fiziksel sınır dışında mı? *)
IF rRawADC < rRawMin - 50.0 OR rRawADC > rRawMax + 50.0 THEN
    xFault    := TRUE;
    eFaultCode := eSensorFault_OutOfRange;
    sFaultMsg  := CONCAT('ADC out of range: ', REAL_TO_STRING(rRawADC));
    xValid    := FALSE;
    RETURN;
END_IF

(* Donmuş değer tespiti — sensör kopmuş mu? *)
tFrozenTimer(IN := (ABS(rRawADC - rLastValue) < 0.5), PT := tTimeout);
IF tFrozenTimer.Q THEN
    xFault    := TRUE;
    eFaultCode := eSensorFault_Frozen;
    sFaultMsg  := 'Sensor value frozen — check wiring';
    xValid    := FALSE;
    RETURN;
END_IF
rLastValue := rRawADC;

(* Ölçeklendirme *)
rEngValue := rEngMin + ((rRawADC - rRawMin) / (rRawMax - rRawMin)) * (rEngMax - rEngMin);
xValid    := TRUE;
xFault    := FALSE;
sFaultMsg  := '';
```

### Katman 4: Alarm Yönetimi — Operatör Bilgilendirme

Hata tespit edildiğinde yalnızca bayrak set etmek yeterli değildir. Operatöre ne olduğunu, nerede, ne zaman ve ne yapması gerektiğini söylemek gerekir.

```iecst
(* Alarm kaydı struct *)
TYPE ST_AlarmRecord :
STRUCT
    xActive      : BOOL;            (* Alarm hâlâ aktif mi *)
    xAcknowledged: BOOL;            (* Operatör onayladı mı *)
    dtTimestamp  : DATE_AND_TIME;   (* Ne zaman tetiklendi *)
    sMessage     : STRING(120);     (* Ne oldu *)
    sFaultSource : STRING(40);      (* Nereden — "FB_Motor1" *)
    eCategory    : E_AlarmCategory; (* Kritik/Uyarı/Bilgi *)
    eFaultCode   : DWORD;           (* Makine tarafından okunabilir kod *)
END_STRUCT
END_TYPE

(* Alarm yönetim FB'si *)
FUNCTION_BLOCK FB_AlarmManager
VAR_INPUT
    xTrigger     : BOOL;            (* Alarm tetikleme koşulu *)
    sMessage     : STRING(120);
    sFaultSource : STRING(40);
    eCategory    : E_AlarmCategory;
    eFaultCode   : DWORD;
    xAckCmd      : BOOL;            (* Operatör onay komutu *)
END_VAR
VAR_OUTPUT
    xActive       : BOOL;
    xUnAcknowledged: BOOL;
END_VAR
VAR_IN_OUT
    stRecord     : ST_AlarmRecord;  (* Güncellenecek alarm kaydı *)
END_VAR
VAR
    fbRTrig      : R_TRIG;
    fbAckRTrig   : R_TRIG;
END_VAR

fbRTrig(CLK := xTrigger);

(* Yeni alarm *)
IF fbRTrig.Q THEN
    stRecord.xActive       := TRUE;
    stRecord.xAcknowledged := FALSE;
    stRecord.dtTimestamp   := NOW();
    stRecord.sMessage      := sMessage;
    stRecord.sFaultSource  := sFaultSource;
    stRecord.eCategory     := eCategory;
    stRecord.eFaultCode    := eFaultCode;
END_IF

(* Alarm temizlendi — onaylanmış + koşul gitti *)
IF NOT xTrigger AND stRecord.xAcknowledged THEN
    stRecord.xActive := FALSE;
END_IF

(* Onay *)
fbAckRTrig(CLK := xAckCmd);
IF fbAckRTrig.Q AND stRecord.xActive THEN
    stRecord.xAcknowledged := TRUE;
END_IF

xActive        := stRecord.xActive;
xUnAcknowledged := stRecord.xActive AND NOT stRecord.xAcknowledged;
```

### Hata Kodu Stratejisi

```iecst
(* Bit maskeleme ile hata kodları — tek DWORD'da birden fazla hata *)
TYPE E_FaultBits :
(
    eFault_None             := 0,
    eFault_MotorTimeout     := 16#00000001,   (* Bit 0 *)
    eFault_TempOverRange    := 16#00000002,   (* Bit 1 *)
    eFault_SensorFrozen     := 16#00000004,   (* Bit 2 *)
    eFault_CommTimeout      := 16#00000008,   (* Bit 3 *)
    eFault_ConfigError      := 16#00010000    (* Bit 16 — konfigürasyon *)
);
END_TYPE

(* Kullanım *)
dwFaultRegister := dwFaultRegister OR DWORD(eFault_MotorTimeout);  (* Set bit *)
dwFaultRegister := dwFaultRegister AND NOT DWORD(eFault_MotorTimeout);  (* Clear bit *)
IF (dwFaultRegister AND DWORD(eFault_TempOverRange)) <> 0 THEN   (* Test bit *)
    (* Sıcaklık alarmı aktif *)
END_IF
```

## Pratikte Nasıl Kullanılır

### Adım 1: Proje İçin Alarm Mimarisi Kur

```
GVL_Alarms (alarm bayrakları + kayıtlar)
    xAnyActiveAlarm        → Genel alarm özeti
    xAnyCriticalAlarm      → Makinenin durması gereken alarmlar
    xAnyWarning            → Uyarılar (makine durmuyor)
    aAlarmLog[1..50]       → ARRAY OF ST_AlarmRecord (geçmiş)
    nAlarmLogHead          → FIFO head pointer

FB_AlarmManager (her alarm noktası için bir instance)
    fbAlarm_EmgStop
    fbAlarm_Motor1_Fault
    fbAlarm_TempOverRange
    ...
```

### Adım 2: Her FB'ye Hata Çıkışı Ekle

```iecst
(* Standart FB hata arayüzü *)
VAR_OUTPUT
    xFault      : BOOL;         (* Hata var mı *)
    eFaultCode  : DWORD;        (* Hata kodu *)
    sFaultMsg   : STRING(80);   (* İnsan okunabilir mesaj *)
END_VAR
```

### Adım 3: Alarm Mesajını İnsan Okunabilir Yap

```iecst
(* ❌ KÖTÜ alarm mesajı *)
sFaultMsg := 'Error 4';   (* Sahadaki operatör ne yapacak? *)

(* ✅ İYİ alarm mesajı *)
sFaultMsg := 'Motor 1: Run feedback timeout after 3s. Check motor contactor K1.';
(* Ne: Timeout *)
(* Nerede: Motor 1 *)
(* Ne kadar süre sonra: 3s *)
(* Muhtemel neden: Kontaktör *)
(* Ne yapmalı: K1'i kontrol et *)
```

### Adım 4: Güvenli Durum Tasarla

```iecst
(* Kritik alarm → güvenli durum *)
PRG_Safety içinde:

(* Her döngüde kontrol *)
IF GVL_Alarms.xAnyCriticalAlarm THEN
    (* Tüm motorları durdur *)
    FOR i := 1 TO 8 DO
        GVL_IO.aMotorOut[i] := FALSE;
    END_FOR
    (* Tüm ısıtıcıları kapat *)
    GVL_IO.xHeater1_Out := FALSE;
    GVL_IO.xHeater2_Out := FALSE;
    (* Güvenlik vanasını kapat *)
    GVL_IO.xSafetyValve := FALSE;
END_IF
```

## Örnekler

### Örnek 1: Fieldbus Hata Tespiti

```iecst
(* EtherCAT bağlantı durumu izleme *)
PROGRAM PRG_FieldbusMonitor
VAR
    nEtherCATState : INT;
    tEtherCATFault : TON;
END_VAR

(* EtherCAT Master state okuma — CODESYS EtherCAT kütüphanesi *)
nEtherCATState := EC_Master.GetState();

(* Operational değil ise (8 = Operational) *)
IF nEtherCATState <> 8 THEN
    tEtherCATFault(IN := TRUE, PT := T#2S);  (* 2 saniye tolerans *)
    IF tEtherCATFault.Q THEN
        GVL_Alarms.xFieldbus_EtherCAT_Fault := TRUE;
        GVL_Alarms.sLastFieldbusFaultMsg := 
            CONCAT('EtherCAT not operational. State: ', INT_TO_STRING(nEtherCATState));
    END_IF
ELSE
    tEtherCATFault(IN := FALSE);
    GVL_Alarms.xFieldbus_EtherCAT_Fault := FALSE;
END_IF
```

### Örnek 2: Program Çöküşünden Sonra Otomatik Yeniden Başlatma

```iecst
(* Application restart — Watchdog sonrası otomatik kurtarma *)
(* NOT: Bu kısım runtime seviyesinde System Event ile yapılır *)

(* CODESYS IDE → Application → Properties → System Events *)
(* excpt_watchdog → PRG_WatchdogHandler'ı çağır *)

PROGRAM PRG_WatchdogHandler
    (* Bu program yalnızca watchdog exception oluştuğunda çalışır *)
    GVL_Alarms.xWatchdogTriggered := TRUE;
    GVL_Alarms.dtWatchdogTime     := NOW();
    
    (* Güvenli duruma geç — fiziksel çıkışları kapat *)
    GVL_IO.xMotor1_Out := FALSE;
    GVL_IO.xHeater_Out  := FALSE;
    
    (* Log'a yaz *)
    (* ... *)
    
    (* 5 saniye sonra restart için timer → başka task içinde *)
```

### Örnek 3: Modbus Haberleşme Hata Yönetimi

```iecst
FUNCTION_BLOCK FB_ModbusDevice
VAR_INPUT
    xEnable     : BOOL;
END_VAR
VAR_OUTPUT
    xConnected  : BOOL;
    xFault      : BOOL;
    sFaultMsg   : STRING(80);
    nFailCount  : INT;
END_VAR
VAR
    fbModbusTCP : ModbusTCP_Client;  (* Kütüphane FB'si *)
    tRetryTimer : TON;
    tTimeoutTimer: TON;
    nMaxRetries : INT := 5;
END_VAR

fbModbusTCP(Enable := xEnable, ...);

CASE fbModbusTCP.eState OF
    
    eModbus_Connected:
        xConnected := TRUE;
        xFault     := FALSE;
        nFailCount := 0;
        tTimeoutTimer(IN := FALSE);
    
    eModbus_Error:
        xConnected := FALSE;
        nFailCount := nFailCount + 1;
        sFaultMsg  := CONCAT('Modbus error #', INT_TO_STRING(nFailCount));
        sFaultMsg  := CONCAT(sFaultMsg, ': ');
        sFaultMsg  := CONCAT(sFaultMsg, fbModbusTCP.sErrorText);
        
        IF nFailCount >= nMaxRetries THEN
            xFault := TRUE;
            sFaultMsg := CONCAT('Modbus device unreachable after ', 
                                INT_TO_STRING(nMaxRetries));
            sFaultMsg := CONCAT(sFaultMsg, ' retries.');
        ELSE
            (* Yeniden dene *)
            tRetryTimer(IN := TRUE, PT := T#5S);
            IF tRetryTimer.Q THEN
                tRetryTimer(IN := FALSE);
                fbModbusTCP.xReconnect := TRUE;
            END_IF
        END_IF
    
    ELSE:
        (* Bağlanıyor — normal *)
END_CASE
```

## Sık Yapılan Hatalar

### Hata 1: Hata Yönetimi Olmayan FB

```iecst
(* ❌ YANLIŞ — Hata durumu düşünülmemiş *)
FUNCTION_BLOCK FB_Valve_Basic
VAR_INPUT
    xOpenCmd : BOOL;
END_VAR
VAR_OUTPUT
    xOpenOutput : BOOL;
END_VAR
xOpenOutput := xOpenCmd;
(* Soru: Vana açılmazsa ne olur? Timeout? Geri bildirim yok? *)
(* Operatör nasıl anlar? Makine neden durdu? *)
```

### Hata 2: Watchdog Olmadan Üretim Projesi

```
Watchdog kapalı → Kod içindeki sonsuz döngü → Runtime donuyor →
Tüm çıkışlar son değerinde kilitli → Motor çalışıyor, durmadan.

Kural: Her task'ta watchdog AÇIK olmalıdır.
       Geliştirme aşamasında bile — erken uyarı mekanizması.
```

### Hata 3: Alarm Mesajının Yalnızca Operatöre Göre Yazılması

```
❌ Yanlış: "Motor arızası"
   Teknisyen bunu gördüğünde ne yapacak? Nereyi kontrol edecek?

✅ Doğru: "Motor 1 çalışma geri bildirimi yok (3sn sonra). Kontaktör K1 ve kablo J14'ü kontrol edin."
   Kim sorumluysa, tam olarak nereye bakması gerektiğini biliyor.
```

### Hata 4: Alarm Onaylanmadan Makineyi Yeniden Başlatmak

```iecst
(* ❌ YANLIŞ — Alarm hâlâ aktifken restart *)
IF xStartCmd THEN
    PRG_Startup();  (* Alarm koşulu devam ediyor olabilir *)
END_IF

(* ✅ DOĞRU — Önce alarm temizlenmeli *)
IF xStartCmd AND NOT GVL_Alarms.xAnyActiveAlarm THEN
    PRG_Startup();
END_IF

(* Veya: Alarm "onaylandı" ancak aktif → Makine restart'a izin verme *)
IF xStartCmd AND NOT GVL_Alarms.xAnyCriticalAlarm THEN
    PRG_Startup();  (* Uyarılar devam edebilir; kritikler hayır *)
END_IF
```

### Hata 5: Çıkış Yönetimini Yalnızca FB'ye Bırakmak

```
CODESYS Application durduğunda fiziksel çıkışlar son değerde kalır.
Motor çalışıyorsa → watchdog → application durur → motor çalışmaya devam eder!

Çözüm:
1. Güvenlik çıkışları ayrı, bağımsız Task_Safety'de yönetilir.
2. Task_Safety watchdog'u daha kısa (1ms), bağımsız izleme.
3. Harici hardware watchdog relay: Runtime yanıt vermezse çıkışları keser.
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Hangi Hata Yönetim Mekanizması Nerede Kullanılır?

| Mekanizma | Kullanım Durumu | Platform |
|---|---|---|
| Task Watchdog | Her task'ta, zorunlu | Tüm platformlar |
| __TRY/__CATCH | Pointer işlemleri, external lib çağrıları | Yalnızca 32-bit |
| FB içi savunmacı kod | Her FB, giriş doğrulama | Tüm platformlar |
| Alarm manager FB | Operatör bildirimi | Tüm platformlar |
| Hardware watchdog relay | Kritik güvenlik çıkışları | Fiziksel I/O |
| Separate safety task | Fail-safe çıkış yönetimi | Tüm platformlar |

## Gerçek Proje Notları

**Not 1 — Hata Mesajı Olmayan Makinenin 8 Saatlik Kaybı**  
Bir paketleme hattında motor geri bildirimi gelmiyordu. Makine durmuş, ekran "Motor fault" yazıyor — başka bilgi yok. Saha ekibi tüm motoru söktü, test etti, yerine taktı — sorun değil. Kablo test edildi — normal. 8 saat sonra PLC programındaki timeout değerinin 500ms yerine 50ms ayarlandığı fark edildi; yeni motor thermo switch'i 500ms içinde kapandığından timeout oluyordu. İyi mesaj: "Motor 1 feedback timeout 50ms içinde — thermo veya contactor gecikmesi olabilir" saatte çözülürdü.

**Not 2 — Watchdog Kapalı Makinenin Acı Deneyimi**  
Geliştirme kolaylığı için watchdog kapalı bırakıldı ve proje üretime gitti. 3 gün sonra bir while döngüsündeki koşul hiçbir zaman FALSE olmadı (sensör bağlı değildi). Runtime dondu, tüm motorlar son komutlarında kaldı, iki motor aşırı ısındı. Watchdog her task'ta etkin olsaydı runtime 50ms içinde durur, motorlar kapanırdı.

**Not 3 — 64-bit Tuzağı**  
Müşteri x64 endüstriyel PC istedi. `__TRY/__CATCH` kullanan tüm kod bölümleri derlendi ama çalışmadı — 64-bit CODESYS runtime bu özelliği desteklemiyor. Kod yeniden yazıldı: Her pointer erişiminden önce null kontrolü, her dizi erişiminden önce index sınır kontrolü. Daha fazla satır ama taşınabilir ve güvenli.

**Not 4 — Alarm Kodu Stratejisinin Değeri**  
32-bit hata kodu (bit maskeleme) kullanılan bir projede operatör paneli tek bir DWORD değerini OPC UA üzerinden SCADA'ya gönderiyordu. SCADA tarafında her bit ayrı bir alarm satırına eşlendi; birden fazla eş zamanlı hata tek kayıt olarak saklandı. 6 ay sonra makine bakımında bu log, bakım süresini yarıya indiren ayrıntılı arıza geçmişi sağladı.

**Not 5 — Çıkışların "Son Değerde Kilitlenmesi" mi, Fail-Safe mi?**  
Bir ekip "watchdog tetiklenince çıkışlar kapanır" varsaydı; gerçekte CODESYS application durunca çıkışlar **fieldbus master'ın fail-safe ayarına** göre davranır — otomatik 0 değil. EtherCAT SafeOp'a düşer, slave'in kendi fail-safe değerleri devreye girer; bu yapılandırılmamışsa çıkışlar son değerde kalabilir. Motor çalışır durumda kilitlendi. Ders: Watchdog/STOP sonrası çıkış davranışı **fieldbus slave fail-safe konfigürasyonunda** ayarlanır (SDO/CoE startup, fail-safe data) ve mutlaka fiziksel test edilmeli — "STOP = güvenli" otomatik değildir (fundamentals/01 ile aynı uyarı).

**Not 6 — Alarm "Chattering" (Titreme) Sel Baskını**  
Bir basınç alarmı eşik değerinin tam etrafında salınan bir sensör yüzünden saniyede onlarca kez set/reset oldu; alarm log'u 10 dakikada doldu, gerçek alarmlar kayboldu. Neden: Histerezis (deadband) yoktu. Ders: Her analog-tetikli alarma **histerezis** (set eşiği ≠ reset eşiği) ve **minimum süre** (`TON` ile debounce) ekleyin. Alarm chattering, SCADA/log sistemini boğan en yaygın saha sorunudur.

**Not 7 — Exception Handler İçinde Yapılamayanlar**  
`excpt_watchdog` system event handler'ında geliştirici karmaşık kurtarma mantığı + dosya yazma koydu. Handler exception bağlamında çalışır; bloke eden/uzun işlemler veya yeni exception fırlatan kod sistemi tamamen kilitledi. Ders: Exception/system-event handler **minimum, non-blocking** olmalı — bayrak set et, güvenli çıkışları kapat, zaman damgası al; gerçek kurtarma ayrı bir task'ta. Handler içinde dosya/ağ/yeni-exception riskli kod yasak.

## Edge Case'ler ve Sistem Limitleri

### Hata Mekanizmalarının Platform/Sürüm Sınırları

```
Mekanizma            Sınır
─────────────────────────────────────────────────────────────────
__TRY/__CATCH        Yalnızca 32-bit; 64-bit'te derlenir ama çalışmaz
Watchdog             Application'ı durdurur, runtime'ı DEĞİL (V3); V2 reboot ederdi
Watchdog → çıkış     Fieldbus fail-safe'e bağlı, otomatik 0 değil (Not 5)
NOW()/RTC            Pil bitikse 1970; zaman damgalı alarm bozulur
STRING alarm mesajı  Varsayılan 80 byte; uzun mesaj sessiz kesilir (truncate)
Alarm log array      Sabit boyut; FIFO taşması en eski kaydı ezer (kayıp)
Exception in handler Sistemi tamamen kilitleyebilir (Not 7)
```

### `__TRY/__CATCH`'in Yakalayamadıkları

32-bit'te bile `__TRY/__CATCH` her şeyi yakalamaz:
- **Watchdog timeout** yakalanmaz (zaten task'ı durduran mekanizma).
- **Stack overflow** (derin recursion) genelde yakalanamaz — sistem çöker.
- **Bölünme** (DIV by zero) bazı platformlarda exception, bazılarında sessiz sonuç (INF/NaN REAL'de).

### Sayısal Edge Case'ler (Sessiz Hatalar)

```
Tamsayı /0          → Exception (32-bit yakalanabilir) veya runtime crash
REAL /0             → +INF/-INF/NaN (exception YOK, sessiz yayılır)
NaN karşılaştırma   → tüm karşılaştırmalar FALSE (NaN = NaN bile FALSE)
INT taşması         → wrap (sessiz), alarm sayacında yanlış değer
```

NaN bir kez oluşunca tüm aritmetiğe yayılır ve `>`/`<`/`=` hep FALSE döner — bir PID çıkışı NaN olursa hiçbir limit kontrolü yakalamaz. `__FINITE()`/açık kontrol gerekir.

## Optimizasyon

### Alarm Sisteminin Performans Maliyeti

```
Pahalı (sıcak task'ta kaçın):
  - Her scan STRING CONCAT ile mesaj kurma → string işlemi yavaş
  - Her alarm için ayrı FB instance + NOW() çağrısı

Optimizasyon:
  - Mesaj string'lerini SABIT tut (CONCAT yerine önceden tanımlı)
  - Alarm değerlendirmesini orta task'ta (10-50ms) yap, 1ms'de değil
  - Sadece DURUM DEĞİŞİMİNDE (R_TRIG) mesaj kur, her scan değil
  - Hata kodunu DWORD bit-mask ile taşı (string değil) → SCADA'da çöz
```

### Savunmacı Kontrolün Maliyeti vs Değeri

Her FB'de giriş doğrulama (range check, null check) küçük bir CPU maliyeti getirir ama saatlerce debug'ı önler. Optimizasyon: ucuz kontrolleri (range, null) her scan yap; pahalı kontrolleri (frozen detection timer'lı) yalnızca gerekli FB'lerde. Savunma kodu "her ihtimale karşı" değil, "bilinen başarısızlık modlarına karşı" olmalı.

### Hata Kodu: String yerine Bit-Mask

İnsan-okunabilir string mesajı runtime'da taşımak yerine, makine-okunabilir DWORD bit-mask taşıyın; string'e çevirmeyi HMI/SCADA katmanında yapın (Not 4). Bu hem bant genişliği (1 DWORD vs 80+ byte string) hem CPU (string CONCAT yok) tasarrufu sağlar ve birden fazla eş zamanlı hatayı tek değerde kodlar.

## Derin Teknik Detay

### Neden Genel try/catch Yok? — Determinizm ve Sertifikasyon

CODESYS'te Java/Python tarzı genel exception handling yokluğu (ve 64-bit'te `__TRY` desteğinin olmaması) tesadüf değil:
- **Determinizm:** Exception unwinding (stack çözme) öngörülemeyen sürede çalışır; bir PLC'nin her scan'i sabit sürmeli (fundamentals/01). Exception tabanlı kontrol akışı bu garantiyi kırar.
- **Fail-safe felsefesi:** PLC dünyasında "hatayı yakala ve devam et" yerine "hatayı önle, oluşursa güvenli duruma kaç" hakimdir. Savunmacı programlama (önleme) + watchdog (son çare durma), exception-ve-devam modelinden daha güvenlidir.
- **Sertifikasyon:** Fonksiyonel güvenlik (SIL), öngörülebilir kod yolları ister; exception'ların dinamik sıçraması doğrulamayı zorlaştırır.

Bu yüzden CODESYS hata stratejisi "exception yakalama" değil, "savunmacı önleme + katmanlı fail-safe"dir — bu, fundamentals'taki determinizm felsefesinin hata-yönetimi yüzüdür.

### Watchdog Neden Application'ı Durdurur, Runtime'ı Değil (V3)?

V2'de watchdog tüm PLC'yi reboot ederdi; V3'te yalnızca etkilenen Application durur, runtime ve diğer application'lar çalışmaya devam eder. Bu, fundamentals/01'deki Component Manager / çoklu-application mimarisinin doğrudan sonucu: runtime bir servistir, application'lar onun üzerinde çalışan bağımsız birimler. Bir application'ın watchdog'u, diğerini (ör. diagnostic application) etkilememeli. Bedeli: çıkışların otomatik güvenli hale gelmemesi (Not 5) — bu yüzden kritik çıkışlar ayrı Task_Safety + fieldbus fail-safe ile korunmalı. "Runtime ayakta ama application durdu" durumu, V2'den gelen mühendisler için en büyük sürprizdir.

### Dört Katmanın Neden Ayrı Olduğu

Hata yönetiminin dört katmanı (watchdog / savunmacı kod / __TRY / alarm) farklı **başarısızlık ölçeklerini** ele alır:

```
Katman               Yakaladığı Başarısızlık Ölçeği
─────────────────────────────────────────────────────
Savunmacı kod (FB)   Mantık-seviyesi: kötü giriş, range dışı, sensör arızası
__TRY/__CATCH        Bellek-seviyesi: null deref, geçersiz erişim (32-bit)
Watchdog             Zaman-seviyesi: sonsuz döngü, takılma, starvation
Alarm + Safety task  Sistem-seviyesi: operatör bildirimi, güvenli duruma geçiş
```

Tek bir mekanizma tüm ölçekleri kapsayamaz: savunmacı kod sonsuz döngüyü yakalamaz (watchdog yakalar); watchdog kötü sensör değerini bilmez (savunmacı kod bilir). Katmanlar dik (orthogonal) olduğu için biri eksik olunca o ölçekteki başarısızlık tamamen korumasız kalır — "8 saatlik debug" hikâyelerinin çoğu eksik bir katmandır.

### Alarm Histerezisi ve Debounce: Sinyal İşleme Kökü

Alarm chattering (Not 6), aslında bir sinyal-işleme problemidir: gürültülü bir sinyalin eşik etrafında salınması. Çözüm kontrol mühendisliğinden gelir — **histerezis** (Schmitt-trigger: set ve reset için farklı eşik) + **debounce** (minimum süre filtresi). Bu, bir alarmın "fiziksel olay" ile "ölçüm gürültüsü" arasında ayrım yapmasını sağlar. Aynı prensip task-structure/02'deki Nyquist/örnekleme tartışmasıyla akrabadır: sinyalin gerçek dinamiği ile gürültüsünü ayırmak, hem kontrolün hem alarmın doğruluğunun temelidir.

## İlgili Konular

```
knowledge/codesys/programming/
├── 02_gvl_design.md         → GVL_Alarms yapısı
├── 03_function_blocks.md    → FB içinde hata state machine
└── 04_libraries.md          → CAA_File ile hata logu dosyaya yazma

knowledge/codesys/task-structure/
├── 01_task_types.md          → Watchdog tipi ve yapılandırması
└── 03_priority_management.md → Safety task — bağımsız watchdog

knowledge/codesys/advanced/
└── application_events.md    → excpt_watchdog sistem olayı işleyici

knowledge/standards/
└── safety_plc.md            → SIL gereksinimi olan sistemlerde hata yönetimi
```
