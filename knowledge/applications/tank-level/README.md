---
KONU        : Tank Seviye Kontrolü (CODESYS ile)
KATEGORİ    : applications
ALT_KATEGORI: tank-level
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/libs/Util/Current/Controller/PID.html"
    başlık: "CODESYS Util Library — PID Function Block Resmi Belgesi"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/libs/Util/Current/Controller/PID_FIXCYCLE.html"
    başlık: "CODESYS Util Library — PID_FIXCYCLE Function Block"
    güvenilirlik: resmi
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/plc-water-level-control-sensor-selection-and-wiring-guide"
    başlık: "PLC Water Level Control: Sensor Selection and Wiring Guide — Industrial Monitor Direct"
    güvenilirlik: topluluk
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/pump-leadlag-control-programming-for-plc-systems"
    başlık: "How to Program Lead/Lag Pump Control in PLC — Industrial Monitor Direct"
    güvenilirlik: topluluk
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/plc-pump-rotation-logic-lead-lag-lag-lag-implementation"
    başlık: "PLC Pump Rotation: Lead-Lag-Lag-Lag & Standby Logic Setup — Industrial Monitor Direct"
    güvenilirlik: topluluk
  - url: "https://instrumentationtools.com/plc-basics-manual-control-closed-loop/"
    başlık: "PLC Basics — Manual Control, Closed Loop, ON-OFF with Hysteresis — Instrumentation Tools"
    güvenilirlik: topluluk
  - url: "https://instrumentationtools.com/plc-programming-using-level-switches/"
    başlık: "PLC Programming using Level Switches — Instrumentation Tools"
    güvenilirlik: topluluk
  - url: "https://iconprocon.com/blog_post/radar-vs-ultrasonic-level-sensors-which-is-best-for-your-tank/"
    başlık: "Radar vs. Ultrasonic Level Sensors: Which is Best for Your Tank? — Icon Procon"
    güvenilirlik: topluluk
  - url: "https://iconprocon.com/blog-post/understanding-four-types-of-liquid-level-sensors-hydrostatic-radar-ultrasonic-and-float/"
    başlık: "Understanding Four Types of Liquid Level Sensors — Icon Procon"
    güvenilirlik: topluluk
  - url: "https://ladderlogicai.com/pages/blog/design-a-tank-filling-system-with-level-sensors-pump-control-and-overflow-protection/"
    başlık: "Design a Tank Filling System with Level Sensors, Pump Control and Overflow Protection — AILogicHMI"
    güvenilirlik: topluluk
  - url: "https://automationforum.co/plc-program-for-motor-starter-with-low-level-switch-interlock/"
    başlık: "PLC Program for Motor Starter with Low-Level Switch Interlock — Automation Forum"
    güvenilirlik: topluluk
  - url: "https://corsosystems.com/posts/program-lead-lag-pumping-in-ignition"
    başlık: "How to Program Lead/Lag Pumping — Corso Systems"
    güvenilirlik: topluluk
  - url: "https://instrunexus.com/isa-5-1-instrumentation-symbols-and-identifications-detailed-analysis/"
    başlık: "ISA 5.1 Instrumentation Symbols and Identifications — InstruNexus"
    güvenilirlik: topluluk
  - url: "knowledge/codesys/fundamentals/03_iec61131_languages.md"
    başlık: "CODESYS IEC 61131-3 Dilleri — İç Bilgi Tabanı"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/_synthesis.md"
    başlık: "CODESYS Programlama Mimarisi Sentezi — İç Bilgi Tabanı"
    güvenilirlik: deneyimsel
  - url: "knowledge/standards/03_namur_ne107.md"
    başlık: "NAMUR NE107 Sensör Diagnostiği — İç Bilgi Tabanı"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/codesys/fundamentals/03_iec61131_languages.md"
    ilişki: gerektirir
  - konu: "knowledge/applications/motor-control"
    ilişki: tamamlar
  - konu: "knowledge/standards/03_namur_ne107.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "IEC 61131-3 ST (Structured Text) dili temel sözdizimi"
  - "CODESYS Function Block (FB) ve Function (FC) kavramları"
  - "Analog I/O: 4-20 mA sinyal standardı, ADC çözünürlüğü (0-27648 / 0-32767 / 0-65535)"
  - "PID kontrolör teorisi (Kp, Ti, Td kavramları)"
  - "Pompa ve vana kontrol temelleri"
ÇELİŞKİLER :
  - kaynak: "Üretici veri belgeleri vs pratikte ADC tam ölçek"
    konu: "4-20 mA → ADC dönüşüm tam ölçek değeri PLC/I/O modülüne göre farklıdır: Siemens S7 0-27648, bazı modüller 0-32767, bazıları 0-65535 kullanır. Ölçekleme formülü tam ölçeğe göre ayarlanmalıdır."
    çözüm: >
      Her I/O modülünün teknik veri sayfasını kontrol edin. Bu belgede 0-27648 (Siemens S7
      standardı) ve 0-32767 örnekleri verilmiştir. CODESYS kendi analog modülünüzün
      raw değerini neredeyse her zaman WORD (0-65535) veya INT (0-32767) olarak sunar;
      hangi üreticinin hangi tam ölçeği kullandığı GVL_IO yorum satırında belgelenmelidir.
  - kaynak: "PID için 'seviye kontrolü = hızlı kontrol' yanılgısı"
    konu: "Tank seviyesi genellikle yavaş bir proses değişkenidir (büyük hacim, düşük akış oranı). PID_FIXCYCLE yerine standart PID yeterlıdir ve cycle time hesabı basitleşir. Ancak küçük hacimli veya yüksek akışlı tanklarda hız önemli olabilir."
    çözüm: "Tank hacmi ve maksimum akış hızına göre PID mi PID_FIXCYCLE mi seçileceğine karar verilmelidir. Kural: doldurma/boşaltma süresi < 30 saniye ise PID_FIXCYCLE; aksi halde standart PID."
  - kaynak: "Tek transmitter ile hem kontrol hem alarm"
    konu: "Bir seviye transmitteri hem PID girdisi hem alarm kaynağı olarak kullanıldığında transmitter arızası hem kontrolü hem alarmı devre dışı bırakır. ISA 5.1 ve IEC 61511 ayrı enstrüman önerir."
    çözüm: "Kritik uygulamalarda seviye kontrolü için ayrı transmitter, LL/HH alarm ve interlock için ayrı bağımsız switch veya transmitter kullanılmalıdır (1oo2 veya 2oo3 oylama)."
---

## Özün Ne

Tank seviye kontrolü, proses endüstrisinin en yaygın otomasyon görevlerinden biridir: su arıtma, kimyasal depolama, gıda üretimi, petrokimya ve HVAC sistemlerinde tank içindeki sıvı seviyesinin ölçülmesi ve belirlenen sınırlar arasında tutulması işlemidir. Seviye ölçümü analog (4-20 mA transmitter: basınç farkı, ultrasonik, radar) veya dijital (şamandıra switch, kapasitif switch) sensörlerle yapılabilir; kontrol stratejisi uygulamanın dinamiğine göre basit histerezis (on/off) veya sürekli PID olarak seçilir. Kuru çalışma koruması ve taşma önleme interlockları, pompa ve tesisin korunması açısından zorunludur. CODESYS ile tank seviye uygulamaları, Util kütüphanesindeki standart `PID` Function Block'u ve iyi tasarlanmış `FB_LevelControl`, `FC_ScaleAnalog` gibi Function Block/Function yapıları üzerinden hem temiz hem test edilebilir biçimde gerçeklenebilir.

## Nasıl Çalışır

### Seviye Ölçüm Teknolojileri

#### 1. Analog Transmitter — 4-20 mA

Proses endüstrisinde en yaygın tercih. Çeşitleri:

| Teknoloji | Çalışma Prensibi | Tipik Uygulama | Avantaj | Kısıt |
|---|---|---|---|---|
| **Hidrostatik basınç** | Tank tabanındaki sıvı sütunu basıncı (ρgh) | Su depoları, kimyasal tank | Düşük maliyet, hareketli parça yok | Yoğunluk değişiminden etkilenir |
| **Ultrasonik** | Ses dalgası gidiş-dönüş süresi (TOF) | Atıksu, basit su tankları | Temazsız, bakım az | Köpük, buhar veya sıcak gaz yüzey yansımayı bozabilir |
| **Radar (80 GHz)** | Mikrodalgaların TOF ölçümü | Kimyasal, petrokimya, köpüklü sıvılar | Buhara, köpüğe, yoğunluğa duyarsız | Maliyet daha yüksek |
| **Diferansiyel basınç (DP)** | Alt ve üst basınç farkı | Kapalı basınçlı kaplar | Kapalı kaplarda çalışır | İki bağlantı noktası gerekir |

Kaynaklar: [Icon Procon — Radar vs Ultrasonic](https://iconprocon.com/blog_post/radar-vs-ultrasonic-level-sensors-which-is-best-for-your-tank/), [Icon Procon — 4 Tip Seviye Sensörü](https://iconprocon.com/blog-post/understanding-four-types-of-liquid-level-sensors-hydrostatic-radar-ultrasonic-and-float/)

4-20 mA çıkışlı transmitter, PLC'nin analog giriş modülüne bağlanır. ADC ham değeri (raw counts) mühendislik birimine (örn. cm, % doluluğu) ölçeklendirilmelidir.

#### 2. Dijital Şamandıra Switch (Float Switch)

Noktasal seviye bilgisi verir (seviye X'in altında/üstünde). Sürekli değil; yalnızca belirli eşik bilgisi. Düşük maliyet, yüksek güvenilirlik. Normalde kapalı (NC) veya normalde açık (NO) kontak. Tipik kullanım: LL (Low-Low) ve HH (High-High) interlock switchleri olarak, ayrı bir güvenlik katmanı.

Kaynak: [Industrial Monitor Direct — Sensor Selection](https://industrialmonitordirect.com/blogs/knowledgebase/plc-water-level-control-sensor-selection-and-wiring-guide)

#### 3. Kapasitif / Konduktivite Switch

Belirli bir seviyede elektriksel özellik değişimi ile tetiklenir. Kimyasal uyumlu tipleri mevcuttur. Şamandıra gibi nokta bilgisi verir.

### 4-20 mA Ölçekleme Matematiği

Transmitter: 4 mA = minimum seviye (örn. 0 cm), 20 mA = maksimum seviye (örn. 300 cm).  
ADC çözünürlüğü ve 4 mA ofseti hesaba katılmalıdır:

```
ADC_4mA   = 4/20 × ADC_MaxRaw  =  (örn. 6554 @ 0-32767 full scale)
ADC_20mA  = ADC_MaxRaw         =  (örn. 32767)

Seviye_cm = (ADC_Ham - ADC_4mA) / (ADC_20mA - ADC_4mA) × (Maks_cm - Min_cm) + Min_cm
```

Kablo kopması / transmitter arızası (< 4 mA veya > 20 mA) ayrıca tespit edilmelidir.

### Kontrol Stratejileri

#### Strateji 1: On/Off Histerezis Kontrolü

En basit yöntem. Pompa veya vana iki eşik arasında açılır/kapanır. Histerezis bandı olmadan eşik değer etrafında sürekli anahtarlama (chatter) oluşur.

```
Dolum tankı örneği (pompa boşaltıyor):
  Seviye < Alt_Eşik → Pompa DURDUR
  Seviye > Üst_Eşik → Pompa ÇALIŞTIR
  Alt_Eşik < Seviye < Üst_Eşik → Son komut devam eder (histerezis)
```

Avantaj: Basit, PID ayarı gerektirmez, donanım değişimlerine karşı dayanıklı.  
Kısıt: Pompa sık açılıp kapandığında mekanik yıpranma artar. Histerezis bandı bunu azaltır.

#### Strateji 2: PID ile Sürekli Kontrol

Sürekli analog çıkış: pompa VFD hızı veya kontrol vanası pozisyonu. Seviye hatası minimize edilir. Büyük hacimli tanklarda, akış oranının önemli olduğu uygulamalarda (kimyasal dozajlama, basınçlı kaplar) tercih edilir.

CODESYS Util kütüphanesindeki `PID` FB'si kullanılır:

```
Y = KP × (e + 1/TN × ∫e dt + TV × δe/δt) + Y_OFFSET
```

Parametreler:
- `KP` : Oransal kazanç
- `TN` : İntegral süresi (saniye)
- `TV` : Türev süresi (saniye)
- `Y_MIN / Y_MAX` : Çıkış sınırı (anti-windup)
- `Y_OFFSET` : Çıkış ofseti
- `MANUAL` / `RESET` : Manuel mod ve sıfırlama

Kaynak: [CODESYS Util Library — PID FB](https://content.helpme-codesys.com/en/libs/Util/Current/Controller/PID.html)

#### Strateji 3: Pompa/Vana Kombine Kontrol

Gerçek uygulamalarda PID çıkışı hem pompa hızını (VFD üzerinden) hem de besleme vanasını kontrol edebilir. Ayrıca yüksek ve düşük seviyelerde histerezis ile çalışma sınırları korunur. İki katmanlı kontrol:

1. PID → Normal seviye kontrolü
2. Histerezis eşikleri → Emniyet sınırları (PID'i override eder)

### Alarm ve Interlock Mimarisi (ISA 5.1)

ISA 5.1 seviye alarm notasyonu (önem sırasıyla):

| Etiket | Açıklama | Tipik Aksiyon |
|---|---|---|
| **LAHH** (Level Alarm High High) | Kritik yüksek seviye | Pompa durdur + giriş vanası kapat (interlock) |
| **LAH** (Level Alarm High) | Yüksek seviye uyarısı | Operatör uyarısı |
| **LAL** (Level Alarm Low) | Düşük seviye uyarısı | Operatör uyarısı |
| **LALL** (Level Alarm Low Low) | Kritik düşük seviye | Çıkış pompasını durdur (kuru çalışma koruması) |

Kaynak: [ISA 5.1 — InstruNexus](https://instrunexus.com/isa-5-1-instrumentation-symbols-and-identifications-detailed-analysis/)

**Kritik tasarım kuralı:** Kontrol transmitteri ile LAHH/LALL güvenlik switchleri birbirinden bağımsız olmalıdır. Tek transmitter hem kontrole hem güvenliğe bağlanırsa transmitter arızasında güvenlik katmanı da devre dışı kalır. (IEC 61511 prensibi — bkz. ÇELİŞKİLER bölümü)

### Kuru Çalışma Koruması

Pompa, sıvı olmadan çalışırsa:
- Mekanik sızdırmazlık elemanı aşırı ısınarak hasar görür
- Salmastra ve yatak erken aşınır
- Motor aşırı yüklenebilir

Koruma mekanizmaları:
1. **LALL switch** → Pompa otomatik durur, tekrar çalışma kilitlenir
2. **Çalışma geri bildirimi + akım izleme** → Pompa çalışıyor ancak yük yok ise dry-run şüphesi
3. **Minimum çalışma süresi kilidi** → Pompa durduktan sonra en az X saniye bekletilerek kısa süreli tekrar çalışma engellenir

Kaynak: [Automation Forum — Low Level Interlock](https://automationforum.co/plc-program-for-motor-starter-with-low-level-switch-interlock/)

### Taşma Önleme (Overflow Prevention)

1. **LAHH** switch → Giriş pompasını / besleme vanasını durdur
2. Bağımsız seviyeden bağımsız LAHH hard-wired interlock (PLC yazılımından bağımsız, doğrudan kontaktör bobinine)
3. Tankın fiziksel taşma çıkışı (son güvenlik: mekanik overflow)

Kaynak: [AILogicHMI — Tank Filling System](https://ladderlogicai.com/pages/blog/design-a-tank-filling-system-with-level-sensors-pump-control-and-overflow-protection/)

### Çoklu Pompa Rotasyonu (Lead-Lag)

Aynı görevi yapan birden fazla pompa olduğunda (lead = baş pompa, lag = yedek), pompa rotasyonu çalışma saatlerini eşitler ve erken yıpranmayı önler.

**Lead-Lag-Standby:** İki aktif pompa + bir standby. Talebe göre ikinci pompa devreye girer; standby yalnızca arıza durumunda çalışır.

**Lead-Lag-Lag:** Her üç pompa eşit çalışma süresiyle rotasyona girer.

Rotasyon tetikleyicileri:
- Sabit zaman aralığı (örn. her 8 saatte bir)
- Çalışma saati eşitliği (en az çalışan pompa lead seçilir)
- Arıza durumunda otomatik geçiş

**Önemli uyarı:** Eşit rotasyonun riski, tüm pompaların aynı anda ömür sonuna ulaşmasıdır. Kritik uygulamalarda bir pompa biraz daha az çalıştırılarak staggered life-end sağlanır.

Kaynak: [Industrial Monitor Direct — Lead-Lag Setup](https://industrialmonitordirect.com/blogs/knowledgebase/pump-leadlag-control-programming-for-plc-systems), [Corso Systems — Lead-Lag Logic](https://corsosystems.com/posts/program-lead-lag-pumping-in-ignition)

## Pratikte Nasıl Kullanılır

### CODESYS'te Proje Yapısı

```
Application
├── GVL_IO          → AT % eşlemeli fiziksel I/O (ham ADC, dijital switchler, pompa çıkışları)
├── GVL_HMI         → Operatör komutları (setpoint, mod seçimi, reset)
├── GVL_Params      → Proses parametreleri (histerezis bandı, alarm eşikleri, PID kazanç)
├── GVL_Alarms      → Alarm ve interlock bayrakları
├── DUT/
│   ├── E_TankMode  → ENUM: eManual, eOnOff, ePID, eFault
│   └── ST_LevelDiag → STRUCT: seviye değeri, alarm durumu, pompa sayaçları
├── FC_ScaleAnalog  → FUNCTION: ham ADC → mühendislik birimi dönüşümü
├── FB_LevelControl → FUNCTION_BLOCK: histerezis + PID kontrol mantığı
├── FB_PumpManager  → FUNCTION_BLOCK: lead-lag rotasyon, kuru çalışma koruması
└── PRG_TankControl → PROGRAM: tüm FB'leri çağırır, alarm üretir
```

### Adım Adım Uygulama

1. **Donanım haritası:** Hangi AI kanalı transmittere bağlı? Raw değer aralığı nedir? Şamandıralar hangi DI kanalında?
2. **GVL_IO tanımla:** `wLevelRaw AT %IW0 : WORD;` vs `xLevelHH AT %I0.0 : BOOL;`
3. **FC_ScaleAnalog yaz:** Ham → mühendislik birimi (cm veya %)
4. **Alarm eşiklerini GVL_Params'a koy:** `rLevelHH_cm`, `rLevelH_cm`, `rLevelL_cm`, `rLevelLL_cm`
5. **FB_LevelControl içinde histerezis veya PID mantığı yaz**
6. **FB_PumpManager içinde lead-lag ve kuru çalışma koruması yaz**
7. **PRG_TankControl içinde hepsini bağla, alarm bayraklarını GVL_Alarms'a aktar**
8. **PRG_Safety (ayrı task, yüksek öncelik):** LAHH veya LALL → tüm çıkışları güvenli konuma al

## Örnekler

### Örnek 1: FC_ScaleAnalog — 4-20 mA Ham ADC → cm Dönüşümü

```iecst
(* FC_ScaleAnalog: 4-20 mA analogunu mühendislik birimine çevirir.
   Bu örnek 0-32767 tam ölçekli bir I/O modülü için yazılmıştır.
   4 mA ≈ 6554 count, 20 mA ≈ 32767 count (0-32767 full scale)
   Kaynak prensibi: Industrial Monitor Direct analog scaling guide *)
FUNCTION FC_ScaleAnalog : REAL
VAR_INPUT
    nRawValue   : INT;     (* ADC ham değeri (0..32767) *)
    rRaw_4mA    : REAL;    (* 4 mA karşılığı raw (örn. 6554.0) *)
    rRaw_20mA   : REAL;    (* 20 mA karşılığı raw (örn. 32767.0) *)
    rEU_Min     : REAL;    (* Mühendislik birimi minimum (örn. 0.0 cm) *)
    rEU_Max     : REAL;    (* Mühendislik birimi maksimum (örn. 300.0 cm) *)
    rEU_FaultLo : REAL;    (* Kablo kopması durumunda döndürülecek değer *)
    rEU_FaultHi : REAL;    (* Transmitter taşması durumunda döndürülecek değer *)
    xFault      : BOOL;    (* Arıza çıkışı — dışarıya bildirim *)
END_VAR
VAR
    rRaw    : REAL;
    rSpan   : REAL;
END_VAR

rRaw  := INT_TO_REAL(nRawValue);
rSpan := rRaw_20mA - rRaw_4mA;

(* Kablo kopması: < 4 mA düşerse raw < rRaw_4mA eşiğinin altına iner *)
IF rRaw < (rRaw_4mA - 164.0) THEN          (* ~0.5 mA alt tolerans *)
    FC_ScaleAnalog := rEU_FaultLo;
    xFault         := TRUE;
    RETURN;
END_IF

(* Transmitter taşması: > 20 mA üzerine çıkarsa *)
IF rRaw > (rRaw_20mA + 164.0) THEN         (* ~0.5 mA üst tolerans *)
    FC_ScaleAnalog := rEU_FaultHi;
    xFault         := TRUE;
    RETURN;
END_IF

xFault := FALSE;

(* Lineer ölçekleme *)
IF rSpan <> 0.0 THEN
    FC_ScaleAnalog := (rRaw - rRaw_4mA) / rSpan * (rEU_Max - rEU_Min) + rEU_Min;
ELSE
    FC_ScaleAnalog := rEU_Min;  (* sıfır bölme koruma *)
END_IF

(* Sınır uygula: hesaplama hatalarına karşı *)
FC_ScaleAnalog := LIMIT(rEU_Min, FC_ScaleAnalog, rEU_Max);
```

---

### Örnek 2: FB_LevelHysteresis — On/Off Histerezis Pompa Kontrolü

```iecst
(* FB_LevelHysteresis: Seviye kontrol — histerezis tabanlı pompa açma/kapama.
   Dolum modu: Seviye düşünce pompa aç, seviye yükselince kapat.
   Kaynak prensibi: Instrumentation Tools — ON-OFF with Hysteresis *)
FUNCTION_BLOCK FB_LevelHysteresis
VAR_INPUT
    rLevelActual  : REAL;   (* Anlık seviye (cm veya %) *)
    rSetpointHigh : REAL;   (* Seviye bu değeri geçince pompa kapat (dolu) *)
    rSetpointLow  : REAL;   (* Seviye bu değerin altına düşünce pompa aç (boş) *)
    xEnable       : BOOL;   (* FALSE ise pompa zorla kapalı *)
    xFaultActive  : BOOL;   (* Harici arıza: pompayı durdur *)
END_VAR
VAR_OUTPUT
    xPumpRun      : BOOL;   (* TRUE = pompa çalışır *)
    eState        : E_HystState; (* İzleme için durum bilgisi *)
END_VAR
VAR
    (* Histerezis durumunu korumak için latch *)
    xAboveHigh    : BOOL;
    xBelowLow     : BOOL;
END_VAR

(* Arıza veya devre dışı durumunda güvenli konuma geç *)
IF NOT xEnable OR xFaultActive THEN
    xPumpRun := FALSE;
    eState   := eHyst_Disabled;
    RETURN;
END_IF

(* Histerezis mantığı: son durumu koru, yalnızca eşik geçilince değiştir *)
xAboveHigh := rLevelActual >= rSetpointHigh;
xBelowLow  := rLevelActual <= rSetpointLow;

IF xAboveHigh THEN
    xPumpRun := FALSE;   (* Tank dolu: pompa durdur *)
    eState   := eHyst_PumpOff_HighReached;
ELSIF xBelowLow THEN
    xPumpRun := TRUE;    (* Tank boş: pompa çalıştır *)
    eState   := eHyst_PumpOn_LowReached;
(* ELSE: histerezis bandında → son durum korunur (xPumpRun değişmez) *)
ELSE
    IF xPumpRun THEN
        eState := eHyst_PumpOn_InBand;
    ELSE
        eState := eHyst_PumpOff_InBand;
    END_IF
END_IF
```

---

### Örnek 3: FB_LevelPID — PID ile Sürekli Seviye Kontrolü

```iecst
(* FB_LevelPID: Tank seviyesini PID ile sürekli kontrol eder.
   Çıkış: 0.0-100.0 % → VFD hızı veya kontrol vanası açısı.
   CODESYS Util kütüphanesindeki PID FB'si kullanılır.
   Kaynak: CODESYS Online Help — PID (FB) - Controller
   https://content.helpme-codesys.com/en/libs/Util/Current/Controller/PID.html *)
FUNCTION_BLOCK FB_LevelPID
VAR_INPUT
    rLevelActual  : REAL;    (* Anlık seviye (cm veya %) *)
    rLevelSetpoint: REAL;    (* Hedef seviye *)
    rKP           : REAL;    (* Oransal kazanç *)
    rTN           : REAL;    (* İntegral süresi (saniye) — 0.0 = integral kapalı *)
    rTV           : REAL;    (* Türev süresi (saniye) — 0.0 = türev kapalı *)
    rOutputMin    : REAL;    (* Çıkış alt sınırı (örn. 0.0) *)
    rOutputMax    : REAL;    (* Çıkış üst sınırı (örn. 100.0) *)
    xManualMode   : BOOL;    (* TRUE = manuel mod — PID hesabı durur *)
    rManualOutput : REAL;    (* Manuel modda çıkış değeri *)
    xReset        : BOOL;    (* TRUE = integral sıfırla + çıkışı Y_OFFSET'e çek *)
    xEnable       : BOOL;    (* FALSE = çıkış 0 olarak set edilir *)
    xFault        : BOOL;    (* Harici arıza — PID durdurulur *)
END_VAR
VAR_OUTPUT
    rOutput       : REAL;    (* Kontrol çıkışı 0.0-100.0 % *)
    xOverflow     : BOOL;    (* PID iç taşma — CODESYS PID FB OVERFLOW çıkışı *)
    eState        : E_PIDState;
END_VAR
VAR
    fbPID         : PID;     (* CODESYS Util kütüphanesi — Standard, 3.5.21.0 *)
END_VAR

(* Arıza veya devre dışı *)
IF NOT xEnable OR xFault THEN
    rOutput  := 0.0;
    eState   := ePID_Disabled;
    fbPID(RESET := TRUE);    (* İntegral sıfırla — bumpless transfer için *)
    RETURN;
END_IF

(* PID FB çağrısı *)
fbPID(
    ACTUAL    := rLevelActual,
    SET_POINT := rLevelSetpoint,
    KP        := rKP,
    TN        := rTN,
    TV        := rTV,
    Y_OFFSET  := rOutputMin,
    Y_MIN     := rOutputMin,
    Y_MAX     := rOutputMax,
    MANUAL    := xManualMode,
    RESET     := xReset
);

(* Manuel modda operatörün değerini çıkışa bas *)
IF xManualMode THEN
    rOutput := LIMIT(rOutputMin, rManualOutput, rOutputMax);
    eState  := ePID_Manual;
ELSE
    rOutput   := fbPID.Y;
    xOverflow := fbPID.OVERFLOW;
    eState    := ePID_Auto;
END_IF
```

---

### Örnek 4: FB_PumpManager — Lead-Lag Rotasyon ve Kuru Çalışma Koruması

```iecst
(* FB_PumpManager: 2 pompa için lead-lag rotasyon + kuru çalışma koruması.
   Pompa rotasyonu çalışma saatlerine göre yapılır.
   Kaynak: Industrial Monitor Direct — Lead-Lag Programming Guide
   https://industrialmonitordirect.com/blogs/knowledgebase/pump-leadlag-control-programming-for-plc-systems *)
FUNCTION_BLOCK FB_PumpManager
VAR_INPUT
    xRunRequest     : BOOL;    (* PID veya histerezis FB'den: pompa çalışsın mı? *)
    xPump1Feedback  : BOOL;    (* Pompa 1 çalışma geri bildirimi (kontaktör FB) *)
    xPump2Feedback  : BOOL;    (* Pompa 2 çalışma geri bildirimi *)
    xLevelLL        : BOOL;    (* TRUE = seviye kritik düşük (LALL) — kuru çalışma tehlikesi *)
    xFaultReset     : BOOL;    (* Operatörden hata resetleme *)
    tRotationPeriod : TIME;    (* Pompa rotasyon aralığı (örn. T#8H) *)
    tFeedbackTimeout: TIME;    (* Çalışma geri bildirimi için max bekleme süresi (örn. T#5S) *)
END_VAR
VAR_OUTPUT
    xPump1Out       : BOOL;    (* Pompa 1 çıkış komutu *)
    xPump2Out       : BOOL;    (* Pompa 2 komutu *)
    xFault          : BOOL;    (* Genel hata bayrağı *)
    sFaultMsg       : STRING(80);
    nLeadPump       : INT;     (* 1 veya 2: hangi pompa lead *)
    rPump1Hours     : REAL;    (* Pompa 1 toplam çalışma saati *)
    rPump2Hours     : REAL;    (* Pompa 2 çalışma saati *)
END_VAR
VAR
    tRotTimer       : TON;     (* Rotasyon zamanlayıcısı *)
    tFB1_Timeout    : TON;     (* Pompa 1 geri bildirim zaman aşımı *)
    tFB2_Timeout    : TON;     (* Pompa 2 geri bildirim zaman aşımı *)
    tPump1Run       : TON;     (* Çalışma saati birikimi için 1 saatlik timer *)
    tPump2Run       : TON;     (* Aynısı pompa 2 için *)
    xPump1Fault     : BOOL;
    xPump2Fault     : BOOL;
    xDryRunProtect  : BOOL;
END_VAR

(* ---- Kuru Çalışma Koruması ---- *)
xDryRunProtect := xLevelLL;
IF xDryRunProtect THEN
    xPump1Out := FALSE;
    xPump2Out := FALSE;
    xFault    := TRUE;
    sFaultMsg := 'LALL aktif: kuru calisma korumasi - her iki pompa durduruldu';
    RETURN;
END_IF

(* ---- Geri Bildirim Zaman Aşımı İzleme ---- *)
tFB1_Timeout(IN := xPump1Out AND NOT xPump1Feedback, PT := tFeedbackTimeout);
tFB2_Timeout(IN := xPump2Out AND NOT xPump2Feedback, PT := tFeedbackTimeout);

IF tFB1_Timeout.Q THEN
    xPump1Fault := TRUE;
    xFault      := TRUE;
    sFaultMsg   := 'Pompa 1: calisma geri bildirimi gelmedi - kontaktor veya kablo kontrol';
END_IF
IF tFB2_Timeout.Q THEN
    xPump2Fault := TRUE;
    xFault      := TRUE;
    sFaultMsg   := 'Pompa 2: calisma geri bildirimi gelmedi - kontaktor veya kablo kontrol';
END_IF

(* ---- Hata Resetleme ---- *)
IF xFaultReset THEN
    xPump1Fault := FALSE;
    xPump2Fault := FALSE;
    xFault      := FALSE;
    sFaultMsg   := '';
END_IF

(* ---- Rotasyon Zamanlayıcısı ---- *)
tRotTimer(IN := TRUE, PT := tRotationPeriod);
IF tRotTimer.Q THEN
    tRotTimer(IN := FALSE);  (* Yeniden başlat *)
    (* Çalışma saati karşılaştırmasına göre lead seç *)
    IF rPump1Hours <= rPump2Hours THEN
        nLeadPump := 1;
    ELSE
        nLeadPump := 2;
    END_IF
END_IF

(* ---- Çalışma Saati Birikimi (1 saatlik adımlar) ---- *)
tPump1Run(IN := xPump1Feedback, PT := T#1H);
tPump2Run(IN := xPump2Feedback, PT := T#1H);
IF tPump1Run.Q THEN tPump1Run(IN := FALSE); rPump1Hours := rPump1Hours + 1.0; END_IF
IF tPump2Run.Q THEN tPump2Run(IN := FALSE); rPump2Hours := rPump2Hours + 1.0; END_IF

(* ---- Pompa Çıkışı Atama ---- *)
IF NOT xFault THEN
    CASE nLeadPump OF
        1:
            xPump1Out := xRunRequest AND NOT xPump1Fault;
            xPump2Out := FALSE;  (* Lag: beklemede *)
        2:
            xPump2Out := xRunRequest AND NOT xPump2Fault;
            xPump1Out := FALSE;
        ELSE:
            nLeadPump := 1;  (* Bilinmeyen durum — güvenli varsayılan *)
    END_CASE
ELSE
    xPump1Out := FALSE;
    xPump2Out := FALSE;
END_IF
```

---

### Örnek 5: PRG_TankControl — Ana Orkestrasyon Programı

```iecst
(* PRG_TankControl: Tüm seviye kontrol mantığını bir araya getirir.
   Task: Task_Control (örn. 100ms döngü). *)
PROGRAM PRG_TankControl
VAR
    (* Ölçekleme *)
    rLevelCm         : REAL;     (* Ölçeklenmiş seviye (cm) *)
    xLevelSensorFault: BOOL;     (* Transmitter kablo kopması/taşma *)

    (* Kontrol FB'leri *)
    fbHysteresis     : FB_LevelHysteresis;
    fbPIDCtrl        : FB_LevelPID;
    fbPumpMgr        : FB_PumpManager;

    (* Mod *)
    xUsePID          : BOOL;     (* TRUE=PID modu, FALSE=histerezis modu *)
END_VAR

(* ---- 1. Ölçekleme ---- *)
rLevelCm := FC_ScaleAnalog(
    nRawValue    := GVL_IO.wLevelRaw,
    rRaw_4mA     := 6554.0,
    rRaw_20mA    := 32767.0,
    rEU_Min      := 0.0,
    rEU_Max      := GVL_Params.rTankHeight_cm,
    rEU_FaultLo  := -1.0,
    rEU_FaultHi  := GVL_Params.rTankHeight_cm + 10.0,
    xFault       => xLevelSensorFault
);

(* Sensör arızasını alarm olarak aktar *)
GVL_Alarms.xAlarm_SensorFault := xLevelSensorFault;

(* ---- 2. Histerezis Kontrol ---- *)
fbHysteresis(
    rLevelActual  := rLevelCm,
    rSetpointHigh := GVL_Params.rHyst_High_cm,
    rSetpointLow  := GVL_Params.rHyst_Low_cm,
    xEnable       := NOT xUsePID AND NOT xLevelSensorFault,
    xFaultActive  := GVL_Alarms.xAnyHardInterlock
);

(* ---- 3. PID Kontrol ---- *)
fbPIDCtrl(
    rLevelActual   := rLevelCm,
    rLevelSetpoint := GVL_HMI.rLevelSetpoint_cm,
    rKP            := GVL_Params.rPID_Kp,
    rTN            := GVL_Params.rPID_Tn,
    rTV            := GVL_Params.rPID_Tv,
    rOutputMin     := 0.0,
    rOutputMax     := 100.0,
    xManualMode    := GVL_HMI.xPID_ManualMode,
    rManualOutput  := GVL_HMI.rPID_ManualOutput,
    xReset         := GVL_HMI.xPID_Reset,
    xEnable        := xUsePID AND NOT xLevelSensorFault,
    xFault         := GVL_Alarms.xAnyHardInterlock
);

(* PID çıkışı → VFD frekans setpoint (0-100% → analog çıkış) *)
IF xUsePID THEN
    GVL_IO.rVFD_SpeedPct := fbPIDCtrl.rOutput;
ELSE
    GVL_IO.rVFD_SpeedPct := 0.0;
END_IF

(* ---- 4. Pompa Yönetimi ---- *)
fbPumpMgr(
    xRunRequest     := fbHysteresis.xPumpRun OR (xUsePID AND fbPIDCtrl.rOutput > 2.0),
    xPump1Feedback  := GVL_IO.xPump1_RunFB,
    xPump2Feedback  := GVL_IO.xPump2_RunFB,
    xLevelLL        := GVL_IO.xLevelLL_Switch OR (rLevelCm < GVL_Params.rLevelLL_cm),
    xFaultReset     := GVL_HMI.xPumpFaultReset,
    tRotationPeriod := GVL_Params.tPumpRotation,
    tFeedbackTimeout:= T#5S
);

GVL_IO.xPump1_Out := fbPumpMgr.xPump1Out;
GVL_IO.xPump2_Out := fbPumpMgr.xPump2Out;

(* ---- 5. Alarm Üretimi ---- *)
(* Seviye alarmları — histerezis ile chatter önleme eklenebilir *)
GVL_Alarms.xAlarm_LevelHH := rLevelCm >= GVL_Params.rLevelHH_cm;
GVL_Alarms.xAlarm_LevelH  := rLevelCm >= GVL_Params.rLevelH_cm
                              AND NOT GVL_Alarms.xAlarm_LevelHH;
GVL_Alarms.xAlarm_LevelL  := rLevelCm <= GVL_Params.rLevelL_cm
                              AND NOT GVL_Alarms.xAlarm_LevelLL;
GVL_Alarms.xAlarm_LevelLL := rLevelCm <= GVL_Params.rLevelLL_cm;
GVL_Alarms.xAlarm_PumpFault := fbPumpMgr.xFault;

(* Hard interlock: LAHH veya LALL → tüm pompaları durdur (PRG_Safety'de de tekrarlanır) *)
GVL_Alarms.xAnyHardInterlock :=
    GVL_Alarms.xAlarm_LevelHH OR
    GVL_Alarms.xAlarm_LevelLL OR
    GVL_IO.xEmergencyStop;
```

---

### Örnek 6: PRG_Safety — Bağımsız Güvenlik Görevi

```iecst
(* PRG_Safety: Yüksek öncelikli, bağımsız güvenlik görevi.
   Task_Safety: Prio:0, 10ms döngü, bağımsız watchdog.
   PRG_TankControl'den bağımsız olarak LAHH/LALL interlockunu uygular. *)
PROGRAM PRG_Safety
VAR
END_VAR

(* LAHH: Tank taşıyor — tüm giriş pompalarını kapat *)
IF GVL_IO.xLevelHH_Switch OR GVL_Alarms.xAlarm_LevelHH THEN
    GVL_IO.xPump1_Out := FALSE;
    GVL_IO.xPump2_Out := FALSE;
    GVL_IO.xInletValve_Out := FALSE;
END_IF

(* LALL: Tank boş — kuru çalışma koruması *)
IF GVL_IO.xLevelLL_Switch OR GVL_Alarms.xAlarm_LevelLL THEN
    GVL_IO.xPump1_Out := FALSE;
    GVL_IO.xPump2_Out := FALSE;
END_IF

(* Acil durum durdurma *)
IF GVL_IO.xEmergencyStop THEN
    GVL_IO.xPump1_Out     := FALSE;
    GVL_IO.xPump2_Out     := FALSE;
    GVL_IO.xInletValve_Out := FALSE;
END_IF
```

---

### Örnek 7: GVL_Params — Parametre Bloğu

```iecst
(* GVL_Params: Tank seviye kontrolü proses parametreleri.
   RETAIN: güç kesilmesinde korunur. PERSISTENT DEĞİL (program download sıfırlar). *)
VAR_GLOBAL RETAIN
    (* Tank boyutu *)
    rTankHeight_cm   : REAL := 300.0;   (* Tank toplam yüksekliği cm *)

    (* Alarm eşikleri *)
    rLevelHH_cm      : REAL := 280.0;   (* LAHH — taşma interlok *)
    rLevelH_cm       : REAL := 260.0;   (* LAH — yüksek uyarı *)
    rLevelL_cm       : REAL := 40.0;    (* LAL — düşük uyarı *)
    rLevelLL_cm      : REAL := 20.0;    (* LALL — kuru çalışma koruma interlok *)

    (* Histerezis bandı (on/off mod) *)
    rHyst_High_cm    : REAL := 240.0;   (* Bu seviye geçilince pompa dur *)
    rHyst_Low_cm     : REAL := 80.0;    (* Bu seviyenin altına düşünce pompa çalış *)

    (* PID parametreleri *)
    rPID_Kp          : REAL := 1.5;
    rPID_Tn          : REAL := 60.0;    (* saniye — seviye yavaş proses *)
    rPID_Tv          : REAL := 0.0;     (* türev kapalı — seviye için genellikle *)

    (* Pompa rotasyon süresi *)
    tPumpRotation    : TIME := T#8H;
END_VAR
```

## Sık Yapılan Hatalar

### Hata 1: Histerezis Bandı Olmadan On/Off Kontrol

```
Durum: rSetpointHigh = rSetpointLow = 150.0 cm (tek eşik)
Sonuç: Seviye 149.9 → pompa açık, 150.1 → pompa kapalı → sürekli açma-kapama
       Pompa motoru kısa sürede aşırı ısınır ve arızalanır
Çözüm: rSetpointHigh ve rSetpointLow arasında en az 10-20 cm band bırakın
```

### Hata 2: Kablo Kopmasını Kontrol Etmemek

Transmitter 4-20 mA çıkış verir. Kablo kopunca ADC 0 okur (0 mA). Ölçekleme fonksiyonu bunu "seviye 0 cm" olarak yorumlar → LALL aktif → pompa durur veya kuru çalışma alarmı verir. Gerçekte ise arıza sinyali olabilir. Çözüm: `FC_ScaleAnalog` gibi bir fonksiyon içinde `< 4 mA` (raw < eşik) durumu için `xFault` bayrağı üretin ve alarm yönetimine gönderin. NE107 F durumu ile eşleştirilebilir.

### Hata 3: PID İçin Yanlış Ti (Integral Süresi) Seçimi

Seviye kontrolü yavaş bir prosestir. Ti çok küçük seçilirse (örn. Ti=5 saniye) integral birikmesi hızlanır, aşım (overshoot) büyür, pompa salınımlı çalışır. Başlangıç değeri: Ti = 3-5 × dolum/boşaltma süresi (dakika cinsinden). Test et, ayarla. Türev genellikle seviye kontrolünde gerekmez (TV=0).

### Hata 4: Kontrol Transmitteri ile Güvenlik Switchini Aynı Yapmak

Tek transmitter hem PID girişi hem LAHH/LALL interlockuna bağlandığında, transmitter arızalanırsa hem kontrol hem güvenlik katmanı aynı anda devre dışı kalır. Kritik tanklarda bağımsız float switch veya ayrı bir transmitter kullanın. Kaynak: [Interlock/Alarm sequence — Eng-Tips forum tartışması](https://www.eng-tips.com/viewthread.cfm?qid=204210)

### Hata 5: Pompa Rotasyonu = Her Zaman Eşit Çalışma Saati Hedefi

Eşit rotasyon her pompanın aynı anda ömür sonuna ulaşmasına neden olabilir. Gerçek proje notu: 4 vidali pompa 5 yıl eşit rotasyondan sonra hepsi 5 hafta içinde arızalandı. Çözüm: Bir pompayı hafifçe daha az çalıştırmak (örn. Pompa 3 standby) veya periyodik farklı rotasyon intervalları uygulamak. Kaynak: [Industrial Monitor Direct — Lead-Lag](https://industrialmonitordirect.com/blogs/knowledgebase/pump-leadlag-control-programming-for-plc-systems)

### Hata 6: FB'yi Koşullu Çağırmak — Timer'ların Dondurulması

```iecst
(* YANLIŞ: *)
IF xEnable THEN
    fbPumpMgr(xRunRequest := ..., ...);
END_IF
(* xEnable = FALSE iken iç TON/Timer'lar donup kalır;
   rotasyon zamanlayıcısı beklenmedik değerde kalır. *)

(* DOĞRU: *)
fbPumpMgr(
    xRunRequest := xEnable AND rLevelCtrl_Request,
    ...
);
(* Her döngüde çağrılır; xRunRequest FALSE olduğunda FB kendi iç mantığıyla durur. *)
```

### Hata 7: LAHH/LALL Eşiklerini PID Setpointine Çok Yakın Koymak

```
rLevelSetpoint = 200 cm, rLevelHH_cm = 205 cm
PID Kp yüksekse seviye 205'i kısa sürede geçer → LAHH aktif → pompa durur → tekrar düşer → döngü
```
Çözüm: Kontrol setpointi ile alarm eşikleri arasında en az %10-15 boşluk bırakın.

### Hata 8: Sensör Diagnostiğini İhmal Etmek

Transmitter kirlenme, sürüklenme (drift) veya kablo bozulması gibi yavaş gelişen arızalarda 4-20 mA sinyali yanlış değer üretmeye devam eder — hata kodu üretmeden. NAMUR NE107 kapsamında: bu durum **S (Out of Specification)** veya **M (Maintenance Required)** kategorisine girer. PLC tarafında; ölçüm zaman içinde beklenmedik sapma gösteriyorsa (kalibrasyon sapması algoritması veya çift transmitter karşılaştırması) alarm üretilmelidir. Kaynak: [NAMUR NE107 iç belge](knowledge/standards/03_namur_ne107.md)

## Ne Zaman Tercih Edilmeli / Edilmemeli

### On/Off Histerezis Tercih Edin

- Tank hacmi büyük, akış oranı düşük → seviye değişimi yavaş
- Pompa frekans kontrolü (VFD) yok; sabit devirli pompa
- Basit su tankı, sump pit, yağmur suyu toplama havuzu
- Bakım ekibi PID ayarlamak istemiyor / bilmiyor
- Sık pompa açma/kapama sorun değil (büyük bant genişliği)

### PID Tercih Edin

- Küçük hacimli tank + yüksek akış → seviye değişimi hızlı
- VFD mevcut — sürekli pompa hızı ayarı mümkün
- Kimyasal dozajlama, basınçlı kap, karıştırıcılı reaktör gibi seviyenin sabit tutulması kritik
- Taşma ve kuru çalışma riski yüksek (dar güvenli çalışma penceresi)

### Lead-Lag Her Zaman Tercih Edin (2+ pompa)

- Tek pompa arızasında sistemin durmaması gerekiyorsa
- Pompalar aynı görevi yapıyorsa — yıpranmayı eşitlemek için

### Lead-Lag Dikkatli Uygulayın

- Standby pompayı rotasyona katmak: standby her zaman hazır olmalı. Eşit rotasyon yerine standby sadece arızada devreye girmeli.
- Eşit çalışma saati hedefi: ömür döngüsü senaryosunu mutlaka değerlendirin.

## Gerçek Proje Notları

**Not 1 — Büyük Tank, Yavaş Proses: İntegral Birikmesi Problemi**  
Bir arıtma tesisinde 5000 litre'lik bir tank için PID kurulmuştu. Ti=10 saniye ile tuning yapıldı. Tank büyük olduğu için hata uzun süre sıfırlanmıyordu; integral birikti, pompa tam hızda çalıştı ve LAHH aktif oldu. Ti=120 saniyeye çıkarılıp Y_MAX pompa kapasitesinin %80'ine indirilince aşım tamamen ortadan kalktı. Ders: Büyük hacim = büyük Ti; çıkış sınırı anti-windup yetersiz kalabilir.

**Not 2 — Float Switch Bounce (Titreşim) Problemi**  
Mekanik şamandıra switchler titreşim veya köpük nedeniyle çok hızlı açılıp kapanabilir. Bu durumda LALL alarmı defalarca tetiklenip resetlenir. Çözüm: LALL switch girişine 2-5 saniye gecikme (TON ile debounce) eklenmeli; kalıcı koşul gerçek alarm şartıdır, anlık spike değil.

**Not 3 — Pompa Geri Bildirim Alarmı: En Değerli Alarm**  
"Pompa arızası" mesajı yerine "Pompa 1 çalışma geri bildirimi 5 saniye içinde gelmedi — kontaktör K1 veya güç kablosunu kontrol edin" mesajı, saha ekibinin arıza bulma süresini saatlerden dakikalara indirir. `sFaultMsg` çıkışına yatırım yapmak karşılığını kat kat verir. (Bkz. iç belge: `knowledge/codesys/programming/_synthesis.md`, Not 6)

**Not 4 — PID Tuning: Seviye Kontrolü İçin Başlangıç Noktaları**  
Seviye prosesi genellikle entegratör davranışı gösterir (akış girer, seviye yükselir — doğal integrasyon). Bu nedenle:
- Kp küçük başlat (0.5-2.0 arası)
- Ti orta-büyük (30-120 saniye)
- Td sıfır (türev genellikle gerekmez, gürültüyü büyütür)
- Anti-windup: Y_MIN/Y_MAX mutlaka ayarla — pompa fiziksel sınırlarını geçemesin

**Not 5 — Çift Ölçüm Karşılaştırması ile Sensör Doğruluğu**  
Kritik bir kimyasal tankta iki ayrı seviye transmitteri kullanılıyorsa, değerlerin farkı belirli bir eşiği (örn. 5 cm) geçtiğinde "sensör uyuşmazlığı" alarmı üretilmesi, yavaş gelişen sensör sürüklenmesini erken tespit eder. Bu, NE107 S kategorisine karşılık gelir: sinyal mevcut ama doğruluğu şüpheli.

**Not 6 — RETAIN vs PERSISTENT için Alarm Eşikleri**  
Alarm eşiklerini RETAIN'e koymak yeterlidir — operatör ayarları güç kesilmesinde korunmalı, ama program yeniden yüklendiğinde üretim mühendisinin yeni eşikleri uygulamaya almasına izin verilmeli. Kalibrasyon ofsetleri (sensör kalibrasyonu, ölçü dönüştürme sabitleri) ise PERSISTENT olmalı. (Bkz. iç belge: `knowledge/codesys/programming/_synthesis.md`, Not 4)

**Not 7 — Lead Pompa Rotasyonu Çalışırken Tetiklendi**  
FB_PumpManager'da rotasyon timer'ı her 8 saatte `nLeadPump`'ı değiştiriyordu — pompa **çalışırken** dahil. Bir gece rotasyon, lead pompa tam basınçta çalışırken tetiklendi; lead Pompa 1'den Pompa 2'ye anlık geçiş yapıldı, Pompa 1 durdu, Pompa 2 soğuk başladı ve hatta su darbesi (water hammer) oluştu, çek valf gürültüyle kapandı. Çözüm: rotasyon kararı yalnızca `xRunRequest = FALSE` (pompa boştayken) uygulandı; rotasyon zamanı geldiğinde "bekleyen rotasyon" bayrağı set edildi, bir sonraki doğal duruşta gerçekleşti. Ders: durum değişimi (lead seçimi) ile aktüatör durumu (pompa çalışıyor) çakışmamalı; geçiş daima güvenli ana ertelenmelidir.

**Not 8 — PID Manuel→Otomatik Geçişinde Bump (Sıçrama)**  
Operatör pompayı manuel %60'ta çalıştırıyordu; otomatik moda geçti ve PID çıkışı bir anda %12'ye düştü (integral terimi manuel modda birikmemişti). Pompa hızı aniden düştü, seviye dalgalandı. Çözüm: CODESYS PID FB'sinin MANUAL girişi bumpless transfer için tasarlanmıştır — manuel moddayken FB'yi RESET veya MANUAL=TRUE ile çağırıp Y'yi manuel değere senkronlamak gerekir; FB_LevelPID'de manuel moddan çıkarken integral terimi mevcut çıkışa göre ön-yüklenmeli (bumpless). Ders: mod geçişlerinde çıkış sürekliliği (continuity) korunmalı; PID iç durumu manuel modu "izlemeli" (tracking).

**Not 9 — Hidrostatik Transmitter Yoğunluk Sapması**  
Bir kimyasal tankta hidrostatik (basınç) transmitter kullanılıyordu; sıvı yoğunluğu sıcaklıkla %4 değişti. Basınç = ρgh olduğundan, yoğunluk düşünce aynı seviye daha düşük basınç → PLC "seviye düştü" okudu, oysa hacim aynıydı. PID gereksiz yere pompayı çalıştırıp tankı taşırdı. Çözüm: kritik tank radar transmitter'a (yoğunluktan bağımsız) geçirildi; alternatifte sıcaklık kompanzasyonu eklenebilirdi. Ders: ölçüm teknolojisinin fiziksel varsayımı (hidrostatik = sabit yoğunluk) proses gerçeğiyle uyuşmalıdır — kod kusursuz olsa da yanlış sensör yanlış kontrol verir.

## Edge Case'ler ve Sistem Limitleri

### Sınır Koşulları Tablosu

| Senaryo | Davranış | Doğru Tasarım |
|---------|----------|---------------|
| 4–20 mA kablo kopması (0 mA) | Ham raw=0 → "seviye 0 cm" → false LALL | FC_ScaleAnalog'da <4 mA → xFault, NE107 F |
| Transmitter >20 mA (kısa devre) | Raw>tam ölçek → seviye taşmış görünür | >20.5 mA → xFault, fail değer |
| Hidrostatik yoğunluk değişimi | Aynı hacim, farklı basınç → yanlış seviye | Radar/DP veya sıcaklık kompanzasyonu |
| Rotasyon pompa çalışırken | Anlık lead geçişi → water hammer | Rotasyon yalnızca xRunRequest=FALSE'da |
| Manuel→Auto geçiş | PID çıkışı sıçrar (integral boş) | Bumpless: integral ön-yükleme/tracking |
| Setpoint LAHH'a çok yakın | PID overshoot → LAHH → durdur → döngü | Setpoint–alarm arası %10–15 boşluk |
| Histerezis bandı = 0 | Eşik çevresinde chatter, motor yanar | rHigh – rLow ≥ 10–20 cm |
| Float switch bounce/köpük | LALL defalarca tetiklenir | TON 2–5 s debounce (kalıcı koşul) |
| Tek transmitter kontrol+güvenlik | Arızada ikisi de devre dışı | Bağımsız LL/HH switch (IEC 61511) |

### Sayısal ve Ölçekleme Limitleri

```
ADC tam ölçek üretici bağımlı:
  Siemens S7 : 0–27648    Bazıları : 0–32767    Bazıları : 0–65535
  ❌ Yanlış tam ölçek → tüm seviye lineer hatalı (ölçek faktörü kayar)
  ✅ rRaw_4mA / rRaw_20mA GVL_IO yorumunda belgelenir

4 mA ofset (live zero) :
  0 mA ≠ 0 seviye; 4 mA = min seviye
  ❌ Ofset atlanırsa min seviyede %20 sabit hata
  ✅ Seviye = (raw – raw_4mA)/(raw_20mA – raw_4mA) × span + min

PID yavaş proses (entegratör):
  Ti çok küçük (<dolum süresi) → integral windup, overshoot
  ✅ Ti ≈ 3–5 × dolum/boşaltma süresi; Y_MIN/Y_MAX anti-windup zorunlu

Sıfır bölme noktaları:
  rSpan = raw_20mA – raw_4mA   → 0 ise ölçekleme patlar
  rRatedCurrent, rIdealCycle   → tüm bölmelerde > 0 kontrolü
```

### Hata Senaryosu — Sensör Arızası Tüm Kontrol Katmanını Çökertir

Tek bir transmitter hem PID girişi, hem histerezis, hem LAHH/LALL yazılım alarmına bağlıysa; transmitter sürüklenir (drift) ve yanlış-düşük okursa: PID pompayı tam hızda çalıştırır, histerezis "boş" der, LALL "kuru" alarmı verir — hepsi aynı yanlış veriyle. Bu, ortak-neden arızasıdır (common-cause failure). IEC 61511 çözümü: güvenlik fonksiyonu (LAHH/LALL interlock) **fiziksel olarak bağımsız** bir float/switch'ten gelmeli. PRG_Safety bu bağımsız switch'i (`xLevelHH_Switch`, `xLevelLL_Switch`) okur, hesaplanan `rLevelCm`'i değil. Yazılım katman ayrımı (Task_Safety bağımsız task) yetmez; sinyal kaynağı da bağımsız olmalıdır.

## Optimizasyon

### Analog Filtreleme ve Ölçeklemeyi Tek Yerde Toplama

`FC_ScaleAnalog` her PID/histerezis çağrısında tekrar çağrılırsa aynı ham değer birden çok kez ölçeklenir (REAL bölme tekrarı). Optimizasyon: ölçekleme PRG_TankControl başında bir kez yapılır, sonuç `rLevelCm` GVL'ye yazılır, tüm FB'ler bunu okur. Bu GVL single-writer prensibidir: seviye değerinin tek bir yazıcısı (ölçekleme adımı) olur, FB'ler salt okur — hem tutarlılık hem CPU tasarrufu.

```
Optimizasyon kuralı (kaynak: codesys/task-structure/_synthesis.md):
  Seviye yavaş proses → Task_Slow 100 ms PID için fazlasıyla yeterli
  PID_FIXCYCLE yerine standart PID: cycle time'ı FB hesaplar, jitter toleranslı
  Hızlı (>5 ms) seviye kontrolü neredeyse hiç gerekmez
```

| İşlem | Frekans | Task |
|-------|---------|------|
| LAHH/LALL interlock (BOOL) | 10 ms | Task_Safety Prio:0 |
| Ölçekleme + PID (REAL) | 100 ms | Task_Control Prio:2 |
| Lead-lag rotasyon, çalışma saati | 100 ms / 1 s | Task_Slow |
| Trend log, OPC UA yayını | 1 s | Task_Log Freewheel |

### Hareketli Ortalama ile Ölçüm Gürültüsünü Bastırma

Ultrasonik/radar yüzey dalgalanmasında ham seviye gürültülüdür; PID türev terimi bu gürültüyü büyütür (bu yüzden seviyede TV=0). Optimizasyon: 5–10 örnekli hareketli ortalama (moving average) veya birinci dereceden IIR filtre, PID girişini yumuşatır. Ancak filtre gecikmesi (lag) faz kaybı getirir; yavaş seviye prosesinde bu kabul edilebilir ama hızlı tankta filtre süresi proses zaman sabitinden çok küçük tutulmalı.

### Alarm Değerlendirmesinde Histerezis ile Chatter'ı Önleme

`rLevelCm >= rLevelHH_cm` çıplak karşılaştırması, seviye eşik etrafında gürültüyle salınırken alarmı defalarca set/reset eder (alarm flooding). PID çıkış chatter'ıyla aynı sorun. Çözüm: alarm set ve reset için ayrı eşik (deadband) — örn. LAHH 280 cm'de set, 275 cm'de reset. Bu, on/off pompa histerezisinin alarm tarafındaki karşılığıdır ve SCADA alarm günlüğünü temiz tutar.

## Derin Teknik Detay

### CODESYS PID FB İçinde Anti-Windup Nasıl Çalışır?

Integral windup, çıkış doygunluğa (Y_MAX) ulaştığında integral teriminin birikmeye devam etmesidir: pompa zaten %100'de ama PID hâlâ "daha fazla" diye integrali şişirir; seviye düşmeye başladığında bu birikmiş integralin boşalması gecikme ve büyük overshoot yaratır. CODESYS Util PID FB'si, Y çıkışı Y_MIN/Y_MAX'a clamp edildiğinde integral toplamını da sınırlandırarak (back-calculation / clamping) bunu önler. Bu yüzden Y_MIN/Y_MAX'ı yalnızca aktüatör sınırı için değil, anti-windup için de doğru ayarlamak şarttır (Not 1, Not 4). Seviye gibi entegratör proseslerinde windup en sık görülen tuning hatasıdır çünkü hata uzun süre tek yönlü kalır — integral hızla doygunluğa gider.

### Neden Seviye "Entegratör Proses"tir ve Bu Tuning'i Nasıl Değiştirir?

Çoğu proses (sıcaklık, basınç) self-regulating'dir: girdi sabitse çıktı bir dengeye oturur. Seviye farklıdır: sabit giriş akışında seviye **durmadan yükselir** (∫ akış dt = hacim). Bu, transfer fonksiyonunda bir saf integratör (1/s) demektir. Pratik sonuç: seviye prosesi zaten bir integratör içerdiğinden, PID'in integral terimi (1/Ti) çoğu zaman gereksiz hatta zararlıdır — saf P (oransal) kontrol çoğu seviye döngüsünü dengeler. Bu yüzden Not 4'te "Kp küçük, Ti büyük (yavaş), Td=0" önerilir; klasik self-regulating proses tuning'i (agresif PI) seviyede salınım yaratır. Kontrol teorisinin pratiğe yansıması: prosesin doğasını (entegratör mü, self-regulating mi) bilmeden PID ayarlanamaz.

### 4–20 mA "Live Zero" Tasarımının Dahiyane Yanı

Neden 0–20 mA değil de 4–20 mA? Çünkü 4 mA alt sınır (live zero), "sıfır sinyal" ile "sıfır seviye"yi ayırır. 0 mA = kablo kopması/güç kaybı; 4 mA = gerçek minimum seviye. Bu sayede transmitter arızası (akım 4 mA'nın altına düşer) ile geçerli minimum ölçüm (tam 4 mA) yazılımda **ayırt edilebilir** — FC_ScaleAnalog'daki `< rRaw_4mA - tolerans` kontrolü tam da bunu yapar ve NE107 F (failure) durumuna eşler. 0–20 mA standardında bu mümkün olmazdı: 0 mA hem "boş tank" hem "kopuk kablo" anlamına gelirdi, fail-safe teşhis imkansızlaşırdı. Live zero, akım döngüsünün kendi içinde bir teşhis kanalı taşımasını sağlayan minimalist bir mühendislik kararıdır — fail-safe felsefesinin elektriksel düzeydeki en zarif örneklerinden biridir.

## İlgili Konular

```
knowledge/codesys/fundamentals/
└── 03_iec61131_languages.md   → ST dili, PID FB, analog ölçekleme örnekleri

knowledge/codesys/programming/
└── _synthesis.md              → FB tasarımı, GVL mimarisi, hata yönetimi

knowledge/standards/
└── 03_namur_ne107.md          → Sensör diagnostiği: F/C/S/M sinyalleri
                                  Transmitter kablo kopması → NE107 F
                                  Sensör sürüklenmesi → NE107 S/M

knowledge/applications/
└── motor-control/             → Pompa motoru FB tasarımı (tamamlayıcı)

Harici referanslar:
  CODESYS Util Library — PID FB:
    https://content.helpme-codesys.com/en/libs/Util/Current/Controller/PID.html
  CODESYS Util Library — PID_FIXCYCLE FB:
    https://content.helpme-codesys.com/en/libs/Util/Current/Controller/PID_FIXCYCLE.html
  ISA 5.1 — Enstrüman sembol ve etiketleme standardı
  IEC 61511 — Fonksiyonel güvenlik, SIL, bağımsız güvenlik enstrümanı gereksinimi
```
