---
KONU        : Konveyör Sistemleri Otomasyonu (CODESYS ile)
KATEGORİ    : applications
ALT_KATEGORI: conveyor
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/siemens-s7-conveyor-sorting-system-io-design-and-fault-handling"
    başlık: "PLC Conveyor Sorting: I/O Planning, Fault Detection & Alarms"
    güvenilirlik: topluluk
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/conveyor-belt-underspeed-detection-plc-programming-guide"
    başlık: "Conveyor Belt Underspeed Detection: PLC Logic & Configuration"
    güvenilirlik: topluluk
  - url: "https://amdmachines.com/blog/buffer-and-accumulation-conveyor-design/"
    başlık: "Buffer and Accumulation Conveyor Design — AMD Machines"
    güvenilirlik: topluluk
  - url: "https://www.cisco-eagle.com/category/3221/zero-pressure-accumulation-conveyor"
    başlık: "Zero Pressure Accumulation Conveyors — Cisco-Eagle"
    güvenilirlik: topluluk
  - url: "https://www.dynapar.com/knowledge/encoder-basics/encoder-how-to-guides/measure-conveyor-speed-with-encoders/"
    başlık: "How To Measure Conveyor Speed With Encoders — Dynapar"
    güvenilirlik: topluluk
  - url: "https://www.maplesystems.com/how-to-control-vfd-with-plc-and-hmi/"
    başlık: "How to Control a VFD with a PLC and HMI — Maple Systems"
    güvenilirlik: topluluk
  - url: "https://machinerysafety101.com/2010/09/27/emergency-stop-categories/"
    başlık: "Understanding Stop Categories for Machinery Stopping Functions"
    güvenilirlik: topluluk
  - url: "https://patents.google.com/patent/US6315104B1/en"
    başlık: "US6315104B1 — Accumulation Conveyor Control System (Patent)"
    güvenilirlik: resmi
  - url: "knowledge/codesys/fundamentals/02_project_structure.md"
    başlık: "CODESYS Proje İç Yapısı — FB_Motor, FB_Conveyor örnekleri"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/_synthesis.md"
    başlık: "CODESYS Programlama Mimarisi Sentezi — FB tasarımı, state machine"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/task-structure/_synthesis.md"
    başlık: "CODESYS Task Yapısı Sentezi — Konveyör için Şablon A"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "codesys/fundamentals/02_project_structure"
    ilişki: gerektirir
  - konu: "codesys/programming/03_function_blocks"
    ilişki: gerektirir
  - konu: "applications/motor-control"
    ilişki: tamamlar
  - konu: "codesys/task-structure/_synthesis"
    ilişki: kullanır
  - konu: "codesys/programming/_synthesis"
    ilişki: kullanır
ÖNKOŞUL     :
  - "CODESYS Function Block kavramı (codesys/programming/03_function_blocks.md)"
  - "State machine tasarımı — CASE eState deseni (codesys/programming/_synthesis.md)"
  - "IEC 61131-3 ST dili temelleri"
  - "VFD (sürücü) temel çalışma prensibi"
ÇELİŞKİLER :
  - kaynak: "Bazı VFD üreticileri (Siemens SINAMICS, ABB ACS880)"
    konu: "VFD hız referansı için analog 0–10 V, 4–20 mA ya da fieldbus (Modbus/PROFINET) kullanılabilir; seçim VFD modeline göre değişir"
    çözüm: >
      Bu belgede analog çıkış (0–10 V) ile Modbus RTU ikisi de örneklenmiştir.
      Projede kullanılan VFD'nin kılavuzuna başvurularak doğru yöntem seçilmelidir.
      Fieldbus erişimi varsa Modbus/EtherCAT tercih edilmeli; analog bağlantıda
      kablo uzunluğuna bağlı sinyal kaybı ve gürültü göz önünde bulundurulmalıdır.
  - kaynak: "IEC 60204-1 Durdurma Kategorileri"
    konu: "Konveyör E-stop için Kategori 0 (ani güç kesme) veya Kategori 1 (kontrollü yavaşlama sonrası kesme) uygulanabilir; hangisinin seçileceği risk değerlendirmesine bağlıdır"
    çözüm: >
      Yük kayması veya ürün devrilmesi riski varsa Kategori 1 (VFD rampiyle durdurma)
      tercih edilmeli. Kategori 0 seçildiğinde VFD bypass veya hardwired kontaktör
      zorunludur ve yazılım E-stop tek güvenlik katmanı olamaz.
---

## Özün Ne

Konveyör sistemleri, endüstriyel otomasyonun en yaygın uygulamalarından biridir: paketleme hatlarından maden bantlarına, otomotiv montaj hatlarından gıda işleme tesislerine kadar her yerde kullanılır. Görece basit görünen bu sistemler; sıkışma algılama, hız kontrolü, akümülasyon mantığı, çoklu zon senkronizasyonu ve güvenlik gereksinimleriyle birleşince karmaşık bir kontrol mühendisliği problemi haline gelir. Bu belge, CODESYS Structured Text (ST) ile bir konveyör sisteminin nasıl modelleneceğini, FB_Conveyor state machine mimarisini, tipik I/O sinyallerini, VFD entegrasyonunu ve güvenlik tasarımını açıklar. İç bilgi tabanındaki FB_Motor ve task tasarım şablonları temel alınmıştır; konveyöre özgü uygulamalar web araştırmasıyla desteklenmiştir.

## Nasıl Çalışır

### Konveyör Sistemi Bileşenleri

Tipik bir endüstriyel konveyör sistemi şu bileşenlerden oluşur:

```
┌──────────────────────────────────────────────────────────────────────┐
│                     KONVEYÖRSİSTEMİ ANATOMİSİ                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  SENSÖRLER (Girişler)           AKTÜATÖRLER (Çıkışlar)                │
│  ─────────────────              ────────────────────                  │
│  xStartBtn   → Başlatma         xMotorRun  → Motor / VFD Çalıştır    │
│  xStopBtn    → Durdurma         xMotorDir  → Yön (opsiyonel)          │
│  xEStop      → Acil Stop        wSpeedRef  → VFD Hız Referansı (AQ)  │
│  xPhotoSns   → Ürün varlığı     xBrakeDO   → Mekanik fren            │
│  xEncoder    → Hız geri bildirimi                                     │
│  xOverload   → Motor aşırı yük  GÖRSEL ÇIKIŞLAR                      │
│  xBeltFault  → Bant hatası      xRunLight  → Çalışma lambası         │
│  xFwdLimit   → İleri limit      xFaultLight → Hata lambası           │
│  xRevLimit   → Geri limit                                             │
│  xZone1Sns   → Zon 1 sensörü                                         │
│  xZoneNSns   → Zon N sensörü                                         │
└──────────────────────────────────────────────────────────────────────┘
```

### Kontrol Mantığı Katmanları

Bir konveyör sistemi kontrol mantığı 4 katmanda değerlendirilebilir:

| Katman | İçerik | Öncelik |
|--------|--------|---------|
| **Güvenlik** | E-stop, interlock, aşırı yük | En yüksek |
| **Sıra Kontrolü** | Start/stop sırası, başlangıç gecikmesi | Yüksek |
| **Proses Kontrolü** | Hız, akümülasyon, zon yönetimi | Normal |
| **Diagnostik** | Sıkışma algılama, hız izleme, alarmlar | Normal |

### State Machine Tasarımı

`FB_Conveyor` için önerilen state machine aşağıdaki durumları içerir:

```
       ┌──────────────────────────────────────────────────────────┐
       │                   FB_Conveyor STATE MACHINE               │
       └──────────────────────────────────────────────────────────┘

  [Güç Geldi]
       │
       ▼
  ┌─────────┐   xStartCmd & NOT xEStop &     ┌───────────┐
  │  eIdle  │──────── tümkosullar OK ────────►│ eStarting │
  └─────────┘                                 └─────┬─────┘
       ▲                                            │ tStartDelay.Q (ör. 3s)
       │                                            ▼
  ┌──────────┐  xStopCmd               ┌───────────────┐
  │eStopping │◄────────────────────────│   eRunning    │
  └──────────┘                         └───────┬───────┘
       │ Belt durdu                             │
       │                              Enkoder hızı düştü /
       ▼                              sensör çok uzun süre
  ┌─────────┐                         aktif kaldı
  │  eIdle  │                                  │
  └─────────┘                                  ▼
                                       ┌──────────────┐
  xEStop veya aşırı yük ──────────────►│    eFault    │
                                       └──────┬───────┘
                                              │ xFaultReset
                                              ▼
                                         ┌─────────┐
                                         │  eIdle  │
                                         └─────────┘
```

Daha kapsamlı bir uygulama için ek durumlar: `eJogForward`, `eJogReverse`, `eEmergencyStop`.

### Sıkışma (Jam) Algılama Prensibi

Sıkışma algılama, bir ürünün konveyörün belirli bir noktasında beklenen geçiş süresini aşması durumunda tetiklenir. Endüstri standardı yaklaşıma göre (industrialmonitordirect.com):

> "Normal operasyondaki ürünler arası geçiş süresini hesapla, buna %50 marj ekle."

```
xProductDetected TRUE olduktan tJamTimeout süresi geçerse
ve sensör hâlâ TRUE ise → Jam alarmı tetikle
```

Örnek: Minimum bant hızında ürün sensöründen geçiş süresi 1.3 saniyeyse, `tJamTimeout := T#2S` uygundur.

### Enkoder ile Hız İzleme

Dynapar'ın teknik rehberine göre (dynapar.com) üç enkoder montaj yöntemi kullanılır:

- **Motor mili (dolaylı)**: `v = (L × fp) / PPR` (L: tur başına mesafe, fp: darbe frekansı)
- **Rulo mili (dolaylı)**: `v = (π × D × fp) / PPR` (D: rulo çapı)
- **Ölçüm tekerleği (doğrudan)**: 1 ft çevreli tekerlek ile ft/dak doğrudan okunur

Düşük hız algılama için çift timer yöntemi (industrialmonitordirect.com):
- `TON_OnDelay` (1.0 s preset): Darbe gelmediğinde tetiklenir
- `TON_OffDelay` (2.0 s preset): Uzun hareketsizliği izler
- İkisi de `xUnderspeedFault` üretir

### Akümülasyon ve Sıfır Basınçlı Kontrol (ZPA)

Akümülasyon konveyörlerinde ürünler birbirine temas etmeden birikmesi gerekir. Sıfır Basınç Akümülasyonu (Zero Pressure Accumulation — ZPA), konveyörü bağımsız kontrollü zonlara böler (amdmachines.com, cisco-eagle.com):

```
Zon Kontrolü (Cascade Logic):
  Her zon → bir sürücü + bir sensör
  Kural  : Aşağı yöndeki zon boşsa bu zon çalışır
           Aşağı yöndeki zon doluysa bu zon durur
  Sonuç  : Ürünler arası temas sıfır basınç altında birikmez
```

US Patent 6315104B1 (Accumulation Conveyor Control System), zon bazlı kaskat mantığı için referans patent olarak bilinir. Bu patent, her zonun bağımsız biçimde upstream sinyali üretmesini ve downstream zon durumuna göre sürücü kararı vermesini tanımlar.

### VFD Entegrasyon Yöntemleri

maplesystems.com rehberine göre üç katmanlı VFD kontrol mimarisi:

```
HMI (hız komutu) → [Modbus TCP/IP] → PLC → [Modbus RTU / 0-10V AQ] → VFD → Motor
```

| Yöntem | Avantaj | Dezavantaj |
|--------|---------|-----------|
| Analog çıkış (0–10V / 4–20mA) | Basit kablolama, evrensel | Gürültüye duyarlı, kablo uzunluğu sınırlı |
| Modbus RTU | Parametre okuma/yazma, teşhis | Baud rate ayarı, adres yönetimi |
| EtherCAT / PROFINET | Düşük gecikme, senkronize | Fieldbus donanım gerektirir |

Hız ramplama: VFD dahili rampa (ACC/DEC) kullanılmalı. Konveyörler için ACC = 5–20 s, DEC = benzer değer; ürün kaymalarını ve bant gerilimini önler.

### Güvenlik: Durdurma Kategorileri

IEC 60204-1'e göre durdurma kategorileri (machinerysafety101.com):

| Kategori | Tanım | Konveyör Uygulaması |
|---------|-------|-------------------|
| **Kategori 0** | Anında güç kesme (kontrolsüz) | Düz bantlar, hafif yük |
| **Kategori 1** | Kontrollü durdurma, ardından güç kesme | Eğimli bantlar, ağır yük, ürün kayması riski |
| **Kategori 2** | Kontrollü durdurma, güç devrede kalır | E-stop için **uygun değil** (IEC 60204-1) |

Kritik kural: **E-stop yalnızca yazılımda (PLC kodu) uygulanamaz.** Hardwired güvenlik rölesi veya güvenlik PLC'si (SIL 2 / PLd minimum) zorunludur.

## Pratikte Nasıl Kullanılır

### CODESYS Proje Yapısı — Konveyör için

`knowledge/codesys/task-structure/_synthesis.md` Şablon A (Basit Makine) konveyör uygulamaları için doğrudan uygulanabilir:

```
Task_Safety   Cyclic  5ms  Prio:0   E-stop, aşırı yük izleme
Task_Control  Cyclic 10ms  Prio:2   Konveyör state machine, zon kontrolü
Task_Slow     Cyclic100ms  Prio:5   HMI güncelleme, VFD Modbus
Task_Log      Freewheel    Prio:15  Diagnostik, üretim sayacı
```

Çoklu konveyörlü sistemlerde enkoder gerektiren yüksek çözünürlüklü hız izleme için ayrı bir Task_Fast (2–5 ms) eklenebilir.

### GVL Yapısı — Konveyör Projesi

```
GVL_IO         → Fiziksel sinyaller (AT % eşlemeli)
GVL_Params     → Hız setpoint, zamanlayıcı süreleri, zon sayısı
GVL_Alarms     → Jam, underspeed, overload, E-stop alarm bayrakları
GVL_HMI        → Operatör komutları ve ekran değerleri
GVL_Diagnostics→ Enkoder sayacı, üretim sayacı, çalışma süresi
```

### DUT Tanımları

```iecst
(* Konveyör Durum ENUM *)
TYPE E_ConveyorState :
(
    eIdle           := 0,
    eStarting       := 1,
    eRunning        := 2,
    eStopping       := 3,
    eEmergencyStop  := 4,
    eJammed         := 5,
    eUnderspeed     := 6,
    eFault          := 99
);
END_TYPE

(* Zon veri STRUCT *)
TYPE ST_ConveyorZone :
STRUCT
    xSensorOccupied   : BOOL;   (* Zon sensörü — ürün var *)
    xDriveEnable      : BOOL;   (* Zon sürücüsü çalışıyor *)
    xDownstreamClear  : BOOL;   (* Aşağı yön zon boş *)
    tJamTimer         : TON;    (* Sıkışma timer bloğu (VAR içinde) *)
    xJamFault         : BOOL;   (* Zon sıkışma alarmı *)
END_STRUCT
END_TYPE

(* Konveyör diagnostik STRUCT *)
TYPE ST_ConveyorDiag :
STRUCT
    dwProductCount    : DWORD;  (* Toplam ürün sayısı *)
    rActualSpeed_mpm  : REAL;   (* Gerçek hız — m/dak *)
    tRunningTime      : TIME;   (* Toplam çalışma süresi *)
    sFaultMsg         : STRING(80);
    eFaultCode        : DWORD;
END_STRUCT
END_TYPE
```

## Örnekler

### Örnek 1: FB_Conveyor — Tam State Machine Implementasyonu

```iecst
FUNCTION_BLOCK FB_Conveyor
VAR_INPUT
    (* Komutlar *)
    xStartCmd       : BOOL;              (* HMI / sekans başlatma komutu *)
    xStopCmd        : BOOL;              (* Normal durdurma komutu *)
    xFaultReset     : BOOL;              (* Hata sıfırlama *)
    xEStop          : BOOL;              (* Acil stop — NC kontak, TRUE=güvenli *)

    (* Sensörler *)
    xMotorRunFB     : BOOL;              (* Motor çalışma geri bildirimi *)
    xOverloadFault  : BOOL;              (* Motor aşırı yük *)
    xProductSensor  : BOOL;             (* Ürün varlık sensörü *)
    wEncoderRaw     : WORD;             (* Enkoder ham değeri (HSCE) *)

    (* Parametreler *)
    tStartDelay     : TIME := T#3S;      (* Başlangıç gecikmesi *)
    tJamTimeout     : TIME := T#5S;      (* Sıkışma timeout süresi *)
    rMinSpeed_pct   : REAL := 20.0;     (* Minimum hız — % nominal *)
    rSpeedSetpoint_pct : REAL := 80.0;  (* Hız setpoint — % nominal *)
END_VAR

VAR_OUTPUT
    xMotorRunCmd    : BOOL;              (* Motora giden çalıştır komutu *)
    wSpeedRefOut    : WORD;             (* VFD analog/Modbus hız referansı 0–32767 *)
    xFaultOut       : BOOL;             (* Genel hata çıkışı *)
    eState          : E_ConveyorState;  (* Mevcut durum *)
    stDiag          : ST_ConveyorDiag; (* Diagnostik yapısı *)
END_VAR

VAR
    tStartTimer     : TON;              (* Başlangıç gecikmesi timer *)
    tJamTimer       : TON;              (* Sıkışma algılama timer *)
    tUnderspeedDly  : TON;             (* Düşük hız onay gecikmesi *)
    rActualSpeed    : REAL;            (* Hesaplanan gerçek hız % *)
    wEncoderPrev    : WORD;            (* Önceki enkoder değeri *)
    tSpeedCalcTimer : TON;             (* Hız hesaplama periyodu *)
END_VAR

(* ──────────────────────────────────────────────── *)
(*  E-STOP ÖNCELİKLİ KONTROL — her döngüde ilk    *)
(* ──────────────────────────────────────────────── *)
IF NOT xEStop OR xOverloadFault THEN
    xMotorRunCmd := FALSE;
    wSpeedRefOut := 0;
    IF eState <> eIdle AND eState <> eFault THEN
        eState := eEmergencyStop;
        stDiag.sFaultMsg := 'ACİL STOP veya AŞIRI YÜK — Manuel reset gerekli';
        stDiag.eFaultCode := 16#0001;
        xFaultOut := TRUE;
    END_IF
    RETURN;
END_IF

(* ──────────────────────────────────────────────── *)
(*  HIZ HESAPLAMA — tSpeedCalcTimer periyodunda    *)
(* ──────────────────────────────────────────────── *)
tSpeedCalcTimer(IN := TRUE, PT := T#500MS);
IF tSpeedCalcTimer.Q THEN
    tSpeedCalcTimer(IN := FALSE);
    (* Enkoder farkından hız tahmini — normalize 0..100% *)
    rActualSpeed := WORD_TO_REAL(wEncoderRaw - wEncoderPrev) / 327.67;
    wEncoderPrev := wEncoderRaw;
    stDiag.rActualSpeed_mpm := rActualSpeed;
END_IF

(* ──────────────────────────────────────────────── *)
(*  STATE MACHINE                                   *)
(* ──────────────────────────────────────────────── *)
CASE eState OF

    eIdle:
        xMotorRunCmd := FALSE;
        wSpeedRefOut := 0;
        tStartTimer(IN := FALSE);
        tJamTimer(IN := FALSE);
        IF xFaultOut AND xFaultReset THEN
            xFaultOut := FALSE;
            stDiag.sFaultMsg := '';
            stDiag.eFaultCode := 0;
        END_IF
        IF xStartCmd AND NOT xFaultOut THEN
            eState := eStarting;
        END_IF

    eStarting:
        (* Hız referansını kademeli artır — VFD rampa ek güvence *)
        wSpeedRefOut := REAL_TO_WORD(rSpeedSetpoint_pct * 327.67);
        xMotorRunCmd := TRUE;
        tStartTimer(IN := TRUE, PT := tStartDelay);
        IF tStartTimer.Q THEN
            tStartTimer(IN := FALSE);
            (* Geri bildirim kontrolü: motor start sonrası çalışıyor mu? *)
            IF NOT xMotorRunFB THEN
                xFaultOut := TRUE;
                stDiag.sFaultMsg := 'Motor çalışma geri bildirimi gelmedi (Kontaktör/kablo kontrol edin)';
                stDiag.eFaultCode := 16#0002;
                eState := eFault;
            ELSE
                eState := eRunning;
            END_IF
        END_IF

    eRunning:
        xMotorRunCmd := TRUE;
        wSpeedRefOut := REAL_TO_WORD(rSpeedSetpoint_pct * 327.67);
        stDiag.tRunningTime := stDiag.tRunningTime + T#10MS; (* Task_Control 10ms varsayım *)

        (* Normal durdurma *)
        IF xStopCmd THEN
            eState := eStopping;
        END_IF

        (* Sıkışma algılama: ürün sensörü tJamTimeout süresince aktif *)
        tJamTimer(IN := xProductSensor, PT := tJamTimeout);
        IF tJamTimer.Q THEN
            xFaultOut := TRUE;
            stDiag.sFaultMsg := 'SIKIŞMA: Ürün sensörü beklenen süreden fazla aktif';
            stDiag.eFaultCode := 16#0003;
            eState := eJammed;
        END_IF

        (* Düşük hız algılama — enkoder ile *)
        IF eState = eRunning THEN
            tUnderspeedDly(IN := (rActualSpeed < rMinSpeed_pct), PT := T#2S);
            IF tUnderspeedDly.Q THEN
                xFaultOut := TRUE;
                stDiag.sFaultMsg := 'DÜŞÜK HIZ: Enkoder geri bildirimi yetersiz — bant veya tahrik kontrol';
                stDiag.eFaultCode := 16#0004;
                eState := eUnderspeed;
            END_IF
        END_IF

    eStopping:
        (* Hız referansını düşür — VFD DEC parametresiyle yavaşlar *)
        wSpeedRefOut := 0;
        xMotorRunCmd := FALSE;
        IF NOT xMotorRunFB THEN
            eState := eIdle;
        END_IF

    eJammed, eUnderspeed, eFault, eEmergencyStop:
        xMotorRunCmd := FALSE;
        wSpeedRefOut := 0;
        IF xFaultReset AND NOT xOverloadFault AND xEStop THEN
            xFaultOut := FALSE;
            stDiag.sFaultMsg := '';
            stDiag.eFaultCode := 0;
            eState := eIdle;
        END_IF

    ELSE:
        (* Bilinmeyen durum — savunmacı programlama *)
        xMotorRunCmd := FALSE;
        wSpeedRefOut := 0;
        xFaultOut := TRUE;
        stDiag.sFaultMsg := 'BİLİNMEYEN DURUM — FB_Conveyor eState geçersiz';
        stDiag.eFaultCode := 16#FFFF;
        eState := eFault;

END_CASE

(* Ürün sayacı: sensörün yükselen kenarı *)
(* (R_TRIG kullanılmalı — burada sadelik için atlanmış) *)
```

### Örnek 2: ZPA (Sıfır Basınç Akümülasyon) Zon Kontrolü

```iecst
(* PRG_ZoneControl — N adet akümülasyon zonu için kaskat mantığı *)
PROGRAM PRG_ZoneControl
VAR
    aZones      : ARRAY[1..8] OF ST_ConveyorZone;
    i           : INT;
END_VAR

(* Aşağı yönden yukarı yöne kaskat: N..1 *)
FOR i := 8 DOWNTO 1 DO

    (* Aşağı yön zon clear mi? *)
    IF i = 8 THEN
        (* Son zon: çıkış sensörü veya downstream onayı *)
        aZones[i].xDownstreamClear := GVL_IO.xExitClear;
    ELSE
        (* Bir sonraki zonun boş olması = bu zonun downstream'i clear *)
        aZones[i].xDownstreamClear := NOT aZones[i+1].xSensorOccupied;
    END_IF

    (* Sıkışma timer *)
    aZones[i].tJamTimer(
        IN := aZones[i].xSensorOccupied AND NOT aZones[i].xDownstreamClear,
        PT := GVL_Params.tZoneJamTimeout
    );
    IF aZones[i].tJamTimer.Q THEN
        aZones[i].xJamFault := TRUE;
        GVL_Alarms.xZoneJamAlarm := TRUE;
    END_IF

    (* Zon sürücü kararı *)
    aZones[i].xDriveEnable :=
        aZones[i].xSensorOccupied         (* Ürün bu zonda *)
        AND aZones[i].xDownstreamClear     (* Aşağı yön boş *)
        AND NOT aZones[i].xJamFault        (* Sıkışma yok *)
        AND NOT GVL_Alarms.xAnyCriticalAlarm; (* Genel alarm yok *)

    (* Çıkışı I/O'ya yaz *)
    GVL_IO.aZoneDriveOut[i] := aZones[i].xDriveEnable;

END_FOR
```

### Örnek 3: VFD Hız Referansı — Analog ve Modbus Karşılaştırması

**Analog Çıkış (0–10V → 0–50 Hz):**
```iecst
(* wSpeedRefAO: PLC analog çıkış registeri, 0..32767 → 0..10V *)
(* VFD: 0V = 0 Hz, 10V = 50 Hz (max frekans) *)
wSpeedRefAO := REAL_TO_WORD(rSpeedSetpoint_pct / 100.0 * 32767.0);
GVL_IO.wVFD1_SpeedRef AT %QW0 := wSpeedRefAO;
```

**Modbus RTU ile VFD Kontrolü (örn. Yaskawa GA500):**
```iecst
(* Modbus yazma: Register 0x0001 = hız referansı (0..10000 = 0..100%) *)
(* Register 0x0002 = run/stop komutu (1=run, 0=stop)                  *)
(* PLC Modbus Master kütüphanesi üzerinden — gerçek adresler VFD kılavuzuna göre *)
GVL_Comm.wVFD1_FreqRef  := REAL_TO_WORD(rSpeedSetpoint_pct * 100.0);
GVL_Comm.xVFD1_RunCmd   := xMotorRunCmd;
(* ModbusMaster FB bu değerleri periyodik olarak VFD'ye yazar *)
```

### Örnek 4: Çoklu Konveyör Senkronizasyonu — Master/Slave Hız Eşleştirme

```iecst
(* PRG_ConveyorSync — Konveyör 1 (master) hızına Konveyör 2 (slave) eşitlenir *)
(* Master enkoder hızı referans alınır; slave hız referansı ona göre ayarlanır *)
PROGRAM PRG_ConveyorSync
VAR
    rMasterSpeed_pct  : REAL;   (* Master konveyör gerçek hızı % *)
    rSlaveSetpoint_pct: REAL;   (* Slave konveyör hız setpoint *)
    rGearRatio        : REAL := 1.0;   (* Varsayılan 1:1 senkronizasyon *)
    rMaxDeviation_pct : REAL := 5.0;  (* Maksimum izin verilen sapma *)
    rDeviation        : REAL;
END_VAR

(* Master hız oku *)
rMasterSpeed_pct := GVL_Diagnostics.rConv1_ActualSpeed_pct;

(* Slave setpoint: master hızı × dişli oranı *)
rSlaveSetpoint_pct := rMasterSpeed_pct * rGearRatio;

(* Sınır kontrolü *)
rSlaveSetpoint_pct := LIMIT(0.0, rSlaveSetpoint_pct, 100.0);

(* Sapma izleme *)
rDeviation := ABS(GVL_Diagnostics.rConv2_ActualSpeed_pct - rSlaveSetpoint_pct);
IF rDeviation > rMaxDeviation_pct AND GVL_IO.fbConv2.eState = eRunning THEN
    GVL_Alarms.xSyncDeviationAlarm := TRUE;
END_IF

(* Slave konveyöre setpoint yaz *)
GVL_IO.fbConv2.rSpeedSetpoint_pct := rSlaveSetpoint_pct;
```

### Örnek 5: PRG_Safety — Konveyör Güvenlik Mantığı

```iecst
(* PRG_Safety — Task_Safety (Prio:0, Cyclic 5ms) içinde çalışır          *)
(* Bu PROGRAM hardwired güvenlik rölesine ek yazılım güvenlik katmanıdır  *)
(* IEC 60204-1: E-stop yazılımda TEK katman OLAMAZ                        *)
PROGRAM PRG_Safety
VAR
END_VAR

(* ─────────────────────────────────────────────────── *)
(*  CRITICAL ALARM — tüm çıkışları kapat               *)
(* ─────────────────────────────────────────────────── *)
GVL_Alarms.xAnyCriticalAlarm :=
    NOT GVL_IO.xEStop_HW     (* E-stop fiziksel kontak — NC: FALSE = aktif *)
    OR GVL_IO.xOverload_Conv1
    OR GVL_IO.xOverload_Conv2
    OR GVL_Alarms.xZoneJamAlarm
    OR GVL_Alarms.xConv1_Fault
    OR GVL_Alarms.xConv2_Fault;

IF GVL_Alarms.xAnyCriticalAlarm THEN
    (* Tüm konveyör çıkışlarını kapat — motorları override et *)
    GVL_IO.xConv1_MotorRun := FALSE;
    GVL_IO.xConv2_MotorRun := FALSE;
    GVL_IO.wConv1_SpeedRef  := 0;
    GVL_IO.wConv2_SpeedRef  := 0;
    GVL_IO.xFaultLight      := TRUE;
END_IF
```

### Örnek 6: SFC ile Konveyör Başlatma Sıralaması

Çoklu konveyörde sıralı başlatma (SFC — Sequential Function Chart) ile tanımlanabilir. Aşağıdaki SFC mantığı ST pseudo-kodunda ifade edilmiştir:

```iecst
(* SFC adımları ST eşdeğeri — PRG_ConveyorStartupSequence *)
(* Step 0: Tüm konveyörler durdurulmuş, sistem hazır bekleniyor   *)
(* Step 1: Konveyör 3 (son) başlatılır — downstream önce çalışmalı *)
(* Step 2: T#2S gecikme                                             *)
(* Step 3: Konveyör 2 başlatılır                                    *)
(* Step 4: T#2S gecikme                                             *)
(* Step 5: Konveyör 1 (ilk) başlatılır                              *)
(* Step 6: Tüm sistem çalışır durumda                               *)

CASE nStartupStep OF
    0:
        IF xSystemStartCmd AND NOT GVL_Alarms.xAnyCriticalAlarm THEN
            nStartupStep := 1;
        END_IF

    1:  (* Conv3 başlat *)
        GVL_IO.fbConv3.xStartCmd := TRUE;
        IF GVL_IO.fbConv3.eState = eRunning THEN
            tStepTimer(IN := TRUE, PT := T#2S);
            IF tStepTimer.Q THEN tStepTimer(IN:=FALSE); nStartupStep := 2; END_IF
        END_IF

    2:  (* Conv2 başlat *)
        GVL_IO.fbConv2.xStartCmd := TRUE;
        IF GVL_IO.fbConv2.eState = eRunning THEN
            tStepTimer(IN := TRUE, PT := T#2S);
            IF tStepTimer.Q THEN tStepTimer(IN:=FALSE); nStartupStep := 3; END_IF
        END_IF

    3:  (* Conv1 başlat *)
        GVL_IO.fbConv1.xStartCmd := TRUE;
        IF GVL_IO.fbConv1.eState = eRunning THEN
            nStartupStep := 0; (* Başlatma tamamlandı, normal operasyon *)
        END_IF

    ELSE:
        nStartupStep := 0;

END_CASE
```

Tasarım kuralı: **Başlatma downstream'den upstream'e (son konveyörden ilk konveyöre), durdurma upstream'den downstream'e yapılır.** Bu, ürün birikimini ve bant üstünde yığılmayı önler.

## Sık Yapılan Hatalar

### Hata 1: E-stop'u Yalnızca PLC Koduna Bırakmak

```
❌ Yanlış:
    IF NOT xEStop THEN
        xMotorRunCmd := FALSE;   (* Yazılım tek güvenlik katmanı *)
    END_IF

✅ Doğru:
    Hardwired güvenlik rölesi (Pilz PNOZ, Siemens SIRIUS 3SK) E-stop devresini
    kontaktöre doğrudan bağlar. PLC kodu ikinci, yazılımsal katmandır.
    IEC 60204-1 ve ISO 13849 bu ikili yaklaşımı zorunlu kılar.
```

### Hata 2: Başlatmayı Upstream'den Downstream'e Yapmak

Doğru sıra: **son konveyör önce çalışır.** Upstream konveyör önce başlarsa ürünler duran downstream konveyörün üstüne birikir, sıkışma veya devrilme olur.

### Hata 3: Jam Timeout'u Sabit ve Kısa Tutmak

```
❌ Yanlış: tJamTimeout := T#1S  → Yavaş ürünleri hatalı alarm üretir
✅ Doğru : Normal geçiş süresi ölçülür, %50 marj eklenir.
           Hız değişkeninden otomatik hesap: tJamTimeout = rBeltLength / rMinSpeed * 1.5
```

### Hata 4: Hız Referansını VFD'ye Doğrudan Yazmak (Rampa Bypass)

```
❌ Yanlış:
    (* Her döngüde anında yeni setpoint — fiziksel rampa yok *)
    wSpeedRefAO := REAL_TO_WORD(rNewSpeed * 327.67);

✅ Doğru:
    VFD ACC/DEC parametreleri aktif bırakılmalı (5–20 s).
    PLC'den anlık setpoint sıçraması yapılırsa VFD kendi rampalama parametresini
    zaten uygular — ancak bu parametreler konfigüre edilmemişse mekanik darbe oluşur.
```

### Hata 5: ZPA Zonlarında Tek Sensör Güvenmesi

Her zon için yalnızca bir varlık sensörü kullanıldığında, sensör arızası veya kirlenme tam zon bypass'ına yol açar. En az iki bağımsız algılama (örneğin fotosel + mekanik limit) veya sensör diagnostiği (fiber optik öğretici çıkış) önerilir.

### Hata 6: FB_Conveyor'u Koşullu Çağırmak

```iecst
(* YANLIŞ: IF bloğu içinde çağrı — iç timer ve state machine donar *)
IF xConveyorEnabled THEN
    fbConv1(xStartCmd := xStart, ...);
END_IF

(* DOĞRU: Her döngüde çağır, enable mantığını FB'ye ilet *)
fbConv1(
    xStartCmd := xStart AND xConveyorEnabled,
    xStopCmd  := xStop OR NOT xConveyorEnabled,
    ...
);
```

`knowledge/codesys/programming/_synthesis.md` Hata 9'da bu kural açıkça belgelenmiştir.

### Hata 7: Enkoder Hız Hesabında Bölme Sıfır Koruması Yapmamak

industrialmonitordirect.com raporuna göre: puls aralığı hesaplamalarında **"karşılaştırma T4:4.ACC > 0 ZORUNLUDUR; aksi halde bölme sıfır hatasına girer."** CODESYS'te bu şu şekilde uygulanır:

```iecst
IF tSpeedCalcTimer.ET > T#0MS THEN
    rActualSpeed := REAL_TO_REAL(nPulseDelta) / TIME_TO_REAL(tSpeedCalcTimer.ET) * rCalibFactor;
ELSE
    rActualSpeed := 0.0;
END_IF
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### FB_Conveyor State Machine Ne Zaman Kullanılır?

**Uygun:**
- Başlatma gecikmesi gerektiren her konveyör (motor termik koruması, mekanik inersia)
- Sıkışma algılama zorunlu hatlar (gıda, ilaç, paketleme)
- Hız kontrolü gerektiren VFD entegrasyonu
- Çoklu konveyör senkronizasyonu olan sistemler
- Güvenlik sertifikasyonu (CE, OSHA) gereken makineler

**Gereksiz veya aşırı mühendislik:**
- Tek başına çalışan, sabit hızlı, kısa bantlar (ör. test tezgahı taşıyıcısı) → Basit ON/OFF mantığı yeterlidir
- Prototip veya tek parça üretim kurulumları

### ZPA Zon Kontrolü Ne Zaman Kullanılır?

**Zorunlu:**
- Kırılgan ürünler (cam, elektronik PCB, seramik)
- Farklı hızlarda aşağı yön ile yukarı yön arasında tampon gereksiniminde
- Ürün sırasının korunması gereken süreçler

**Basit kademeli akümülasyon yeterli (ZPA gerekmez):**
- Dayanıklı metal parçalar, ağır sandıklar
- Düşük hızlı (< 0.2 m/s) kısa hatlar

### VFD Ne Zaman Kullanılır?

- Hız değişkenliği gereksinimi varsa (reçeteye bağlı hız, yük bazlı hız)
- Enerji verimliliği öncelikli (DOL motorun 3–5 katı enerji tasarrufu mümkün)
- Soft-start/soft-stop mekanik avantajı isteniyorsa (bant gerilimi azalır, ömür uzar)

**DOL (Direct On-Line) yeterli:**
- Kısa bantlar, düşük enerji (<7.5 kW), sabit hız
- Sık start/stop gerektirmeyen statik konveyörler

## Gerçek Proje Notları

**Not 1 — "Downstream Önce" Kuralının Maliyeti**  
Bir paketleme hattında konveyörler upstream → downstream sırasıyla başlatılmıştı. İlk gün devreye almada ürünler duran shrink wrap konveyörünün üstüne birikti ve 40 dakika durma oldu. Doğru başlatma sırası (downstream ilk) uygulanınca sorun tamamen ortadan kalktı. Bu kural belgede "SFC Sıralı Başlatma" örneğinde yerini almaktadır.

**Not 2 — Jam Timeout Kalibrasyonu**  
Bir gıda üretim hattında tJamTimeout T#3S sabit bırakıldı. Hat, belirli ürün boyutlarında kasıtlı yavaşladığında yanlış jam alarmı üretmeye başladı. Hat hızı değişkenden hesaplanan dinamik timeout (L/v × 1.5) ile kalibre edilince yanlış alarm frekansı %95 düştü. Kural: timeout'u operasyon parametresinden türet, kodda sabit bırakma.

**Not 3 — VFD Modbus İletişim Gecikmesi**  
Bir konveyör hattında VFD Modbus RTU üzerinden kontrol ediliyordu ve Task_Control 10 ms'de çalışıyordu. Modbus yanıt gecikmesi 25–40 ms arasında değiştiğinden, FB içindeki hız geri bildirimi her döngüde taze değildi. Çözüm: Modbus okuma/yazma Task_Slow (100 ms) içine alındı, kritik motor kontrol çıkışları ise analog çıkışla beslendi. Hiçbir zaman Modbus üzerinden acil stop komutuna güvenme — hardwired devre zorunlu.

**Not 4 — ZPA Sensör Kirlenme Problemi**  
Bir toz ortamında çalışan ZPA konveyöründe fotosel sensörler kirlenince sürekli "zon dolu" okuyup tüm hat durdu. Çözüm: her sensöre "sensör diagnostik" çıkışı izlendi (bazı optik sensörler sinyal kalitesi çıkışı verir). Ek olarak yıkama döngüsünde sensörlerin "temiz ortamda" ölçümü baseline olarak alınıp sapma izlendi.

**Not 5 — Enkoder Slip Probleminin Fark Edilmemesi**  
Bant üzerindeki enkoder ölçüm tekerleği zamanla slip yapmaya başladı (tekerlek yüzeyi yıprandı). Hız hesabı nominal değerin %15 altında göstermeye başladı; yazılım bunu underspeed olarak yorumladı. Gerçek bant hızı normaldi. Çözüm: enkoderi motor miline taşıma ve periyodik kalibrasyon prosedürü ekleme.

**Not 6 — Güvenlik Rölesinin PLC E-Stop'undan Bağımsız Olması**  
Bir kullanıcı "PLC kodu zaten E-stop mantığı uyguluyor, safety relay neden gerekli?" diye sordu. Cevap: PLC watchdog hatası, CPU arızası veya program hatası durumunda yazılım E-stop çalışmaz. Safety relay donanım katmanıdır ve PLC çökmesinden bağımsız olarak motor kontaktörünü keser. ISO 13849 PLd için bu ikili yapı zorunludur.

## İlgili Konular

```
knowledge/applications/conveyor/
└── README.md (bu belge)

Önkoşul — CODESYS temeller:
knowledge/codesys/fundamentals/
├── 02_project_structure.md  → FB_Motor, FB_Conveyor örnekleri, GVL/DUT yapısı
└── _synthesis.md

Önkoşul — Programlama mimarisi:
knowledge/codesys/programming/
├── 03_function_blocks.md    → İyi FB tasarımı, state machine, ELSE koruması
└── _synthesis.md            → Beş belgenin bütünsel özeti

Önkoşul — Task tasarımı:
knowledge/codesys/task-structure/
└── _synthesis.md            → Şablon A (Basit Makine), konveyör için uygun

İlgili uygulamalar:
knowledge/applications/
└── motor-control/           → FB_Motor tasarımı, VFD kontrolü detayı

Protokol entegrasyonu:
knowledge/protocols/
└── modbus/                  → VFD Modbus RTU/TCP entegrasyon detayı

Güvenlik standartları:
knowledge/standards/
└── safety_plc.md            → ISO 13849, IEC 62061, SIL/PLd gereksinimleri
```
