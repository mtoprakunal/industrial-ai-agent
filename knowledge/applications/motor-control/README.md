---
KONU        : Motor Kontrol Sistemleri (CODESYS ile)
KATEGORİ    : applications
ALT_KATEGORI: motor-control
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/vfd-vs-soft-starter-vs-star-delta-motor-starting-comparison"
    başlık: "VFD vs Soft Starter vs Star-Delta: Motor Starting Methods – Industrial Monitor Direct"
    güvenilirlik: topluluk
  - url: "https://www.corgin.co.uk/blog/what-is-the-difference-between-direct-on-line-dol-star-delta-soft-start-and-variable-speed-drive-starting-modes"
    başlık: "DOL, Star-Delta, Soft Start ve VFD Başlatma Modları Farkı – Corgin"
    güvenilirlik: topluluk
  - url: "https://viox.com/types-of-motor-starters-selection-guide/"
    başlık: "5 Types of Motor Starters Explained: DOL, Star-Delta, Soft Starter & VFD | VIOX Guide"
    güvenilirlik: topluluk
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/danfoss-vfd-modbus-register-mapping-for-plc-integration"
    başlık: "Danfoss VFD Modbus Register Map: Addressing & Integration Guide – Industrial Monitor Direct"
    güvenilirlik: topluluk
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/abb-acs-355-modbus-register-mapping-for-idec-plc"
    başlık: "ABB ACS 355 Modbus Register Mapping for IDEC PLC – Industrial Monitor Direct"
    güvenilirlik: topluluk
  - url: "https://www.manualslib.com/manual/1248960/Abb-Acs355.html?page=312"
    başlık: "Modbus Mapping; Register Mapping — ABB ACS355 User Manual [Page 312] | ManualsLib"
    güvenilirlik: resmi
  - url: "https://www.manualslib.com/manual/1636864/Abb-Acs580.html?page=416"
    başlık: "Status Word — ABB ACS580 Firmware Manual [Page 416] | ManualsLib"
    güvenilirlik: resmi
  - url: "https://files.danfoss.com/download/Drives/MG33MO02.pdf"
    başlık: "Danfoss VLT AutomationDrive FC 301/302 Programming Guide (MG33MO02)"
    güvenilirlik: resmi
  - url: "https://plc247.com/danfoss-fc302-modbus-rtu-via-modbus-poll-tutorial/"
    başlık: "Danfoss FC302 Modbus RTU via Modbus Poll Tutorial – plc247.com"
    güvenilirlik: topluluk
  - url: "https://nfmconsulting.com/knowledge/motor-phase-loss-detection/"
    başlık: "Three-Phase Motor Phase Loss — Detection, Protection, and Recovery | NFM Consulting"
    güvenilirlik: topluluk
  - url: "https://electrical-engineering-portal.com/star-delta-motor-starter"
    başlık: "Star-delta motor starter explained in details | EEP"
    güvenilirlik: topluluk
  - url: "https://ladderlogicai.com/pages/blog/plc-for-motor-control-dol-star-delta-vfd-integration/"
    başlık: "PLC for motor control (DOL, Star-Delta, VFD integration) | AILogicHMI Blog"
    güvenilirlik: topluluk
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_obj_function_block.html"
    başlık: "CODESYS Online Help — Object: Function Block"
    güvenilirlik: resmi
  - url: "knowledge/codesys/fundamentals/02_project_structure.md"
    başlık: "CODESYS Proje İç Yapısı — FB_Motor state machine, GVL, DUT örnekleri"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/03_function_blocks.md"
    başlık: "İyi Bir Function Block Nasıl Yazılır — FB tasarım prensipleri"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/modbus-tcp/_synthesis.md"
    başlık: "Modbus TCP Sentezi — Register model, FC'ler, CODESYS slave yapılandırması"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "codesys/fundamentals/02_project_structure"
    ilişki: gerektirir
  - konu: "protocols/modbus-tcp/_synthesis"
    ilişki: kullanır
  - konu: "applications/conveyor"
    ilişki: tamamlar
  - konu: "codesys/programming/03_function_blocks"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "CODESYS proje yapısı: Device Tree, GVL, Task, DUT (codesys/fundamentals/02_project_structure.md)"
  - "Function Block kavramı ve state machine tasarımı (codesys/programming/03_function_blocks.md)"
  - "Modbus TCP protokolü ve register modeli (protocols/modbus-tcp/_synthesis.md)"
  - "IEC 61131-3 Structured Text temel sözdizimi"
  - "Üç fazlı asenkron motor çalışma prensipleri"
ÇELİŞKİLER :
  - kaynak: "VFD Modbus register haritaları üretici bağımlıdır"
    konu: "ABB ACS355, Danfoss FC302, Schneider Altivar register adresleri birbirinden farklıdır"
    çözüm: >
      Bu belgede verilen register haritaları gerçek üretici belgelerinden alınmıştır ve
      referans olarak kullanılabilir. Ancak her projeye başlamadan önce o VFD'nin özgün
      kullanım kılavuzundaki Modbus register haritası mutlaka doğrulanmalıdır. Özellikle
      ABB 'DCU' ve 'Standard Drive' profilleri arasında register adresleri değişmektedir.
  - kaynak: "Yıldız-Üçgen geçiş süresi tartışmalı"
    konu: "Bekleme süresi (yıldız sona erişimden delta başlangıcına kadar) 50–200 ms arasında değişen öneriler bulunmaktadır"
    çözüm: >
      Bekleme süresi, motor ve trafo empedansına bağlıdır; evrensel bir standart yoktur.
      IEC 60034-1 ve motor üreticisi verilerinden hareket edilmeli; pratik kural T#50MS'dir.
      Mekanik interlock ve ardışık kontaktör mantığıyla geçiş akımı sınırlanmalıdır.
  - kaynak: "Soft starter ile VFD arasındaki sınır"
    konu: "Bazı kaynaklarda 'soft starter = VFD lite' gibi hatalı bir eşitleme yapılıyor"
    çözüm: >
      Soft starter yalnızca başlatma/durdurma sırasında voltajı ayarlar; çalışma sırasında
      tam devre-kesici gibi davranır — hız kontrolü yoktur. VFD frekansı sürekli ayarlar;
      tam hız kontrolü, enerji tasarrufu ve Modbus haberleşmesi sağlar. Birbirinin yerine
      kullanılamaz.
---

## Özün Ne

Motor kontrol sistemleri, endüstriyel otomasyon projelerinin temel yapı taşıdır. Her üretim hattı, konveyör, pompa veya fan en az bir motoru içerir. Bu belge; DOL (direkt çevrimiçi), yıldız-üçgen, soft starter ve VFD başlatma yöntemlerini, PLC tarafındaki kontrol mantığını (start/stop/jog/yön/hız), geri bildirim ve koruma mekanizmalarını, VFD ile Modbus TCP/RTU haberleşmesini ve tüm bunları CODESYS Structured Text ile saran `FB_Motor` tasarımını kapsar. Gerçek üretici register haritaları ve doğrudan derlenebilecek ST kod örnekleri içerir.

---

## Nasıl Çalışır

### Motor Başlatma Yöntemleri — Karşılaştırma

Bir asenkron motoru devreye almanın dört temel yöntemi vardır. Her yöntem farklı akım sınırlama kabiliyeti, maliyet ve kontrol esnekliği sunar.

#### 1. DOL — Direkt Çevrimiçi (Direct-On-Line)

Motor tam gerilimle doğrudan şebekeye bağlanır. Motorun çalışma sargıları anlık olarak tam gerilim görür.

```
ŞEBEKE (L1/L2/L3) ──► KONTAKTÖR (Q1) ──► TERMIK AŞIRI YÜK RÖLESİ ──► MOTOR
```

- **Başlangıç akımı:** Nominal akımın 6–8 katı (I_start = 6–8 × I_FLC)
- **Başlangıç torku:** Yüksek (100–150% nominal tork)
- **Uygun motor gücü:** ≤ 5 kW (küçük motorlar) — şebeke kapasitesine göre değişir
- **Avantaj:** En basit, en ucuz devre; PLC çıkışı sadece tek bir kontaktörü sürer
- **Dezavantaj:** Şebekeye büyük akım darbesi; elektriksel ve mekanik stres
- **IEC referansı:** IEC 60034-1 Motor standardı, başlangıç akımı sınıflandırması için referans alınır

#### 2. Yıldız-Üçgen (Star-Delta / Y-Δ)

Motor önce yıldız (star) bağlantısıyla başlatılır; nominal hıza yaklaşınca üçgen (delta) bağlantısına geçilir. İki aşamalı kontaktör düzeni kullanılır: Ana kontaktör (Q1) + Yıldız (Q_Y) + Üçgen (Q_D).

```
Başlangıç: Q1 + Q_Y açık → Motor yıldız bağlı → U_faz = U_line / √3
Geçiş:     Q_Y kapatılır → 50–100 ms beklenir → Q_D açılır
Çalışma:   Q1 + Q_D açık → Motor üçgen bağlı → U_faz = U_line
```

- **Başlangıç akımı:** DOL'un 1/3'ü (≈ 2–2.5 × I_FLC) — çünkü yıldızda gerilim √3 azalır
- **Başlangıç torku:** DOL'un 1/3'ü — dikkat: yük ağırsa motor yıldızda yeterince hızlanamaz
- **Geçiş sırasında:** Kısa süre (50–200 ms) devre açık kalır; bu geçiş akımı darbesine yol açar
- **Uygun motor gücü:** 7.5 kW – 100 kW arası orta güç uygulamaları
- **Kritik kural:** Q_Y ve Q_D arasında mekanik ve elektriksel kilitleme (interlock) zorunludur; ikisi aynı anda kapanırsa faz-faz kısa devre oluşur

#### 3. Soft Starter

Tiristörler (SCR) aracılığıyla başlangıçta şebeke gerilimi kademeli olarak artırılır, durdurma sırasında azaltılır. Çalışma sırasında tiristörler tam iletimde kalır — soft starter bir geçiş elemanıdır.

- **Başlangıç akımı:** Programlanabilir limit (tipik: 200–400% × I_FLC)
- **Hız kontrolü:** Yok — yalnızca başlatma ve durdurma sırasında gerilim ayarı yapar
- **Sıkça başlatma sınırı:** Tiristör ısısı nedeniyle saatte 6–10 start (üreticiye göre değişir)
- **PLC kontrolü:** Dijital start/stop komutu; bazı modeller seri iletişim (Modbus) destekler
- **Maliyet:** VFD'ye göre %40–60 daha ucuz; hız kontrolü gerekmediğinde tercih edilir

#### 4. VFD — Değişken Frekanslı Sürücü (Variable Frequency Drive)

İnverter teknolojisi kullanarak motor beslemesinin hem frekansını hem voltajını bağımsız olarak ayarlar. V/Hz oranı sabit tutularak motor manyetik akısı korunur.

```
ŞEBEKE ──► DOĞRULTUCU (Rectifier) ──► DC BUS ──► İNVERTER (IGBT) ──► MOTOR
           (AC→DC)                    (~540 V DC)  (DC→AC, değişken f)
```

- **Başlangıç akımı:** Nominal akıma yakın (1.0–1.5 × I_FLC)
- **Hız kontrolü:** 0–maksimum frekans arası sürekli ve hassas kontrol
- **Enerji tasarrufu:** Pompa ve fanlarda hız %20 azaltma → güç tüketimi %49 azalma (kübik ilişki)
- **Rampa:** Ayarlanabilir ivmelenme ve yavaşlama rampaları mekanik stresi önler
- **Haberleşme:** Modbus RTU/TCP, PROFINET, EtherNet/IP, CANopen üzerinden tam kontrol
- **Uygun:** Tüm güç aralıkları, hassas hız kontrolü, enerji optimizasyonu

#### Başlatma Yöntemi Seçim Matrisi

| Kriter | DOL | Yıldız-Üçgen | Soft Starter | VFD |
|---|---|---|---|---|
| Başlangıç akımı | 6–8× I_FLC | 2–2.5× I_FLC | 2–4× I_FLC | 1–1.5× I_FLC |
| Hız kontrolü | Yok | Yok | Yok | Tam |
| Maliyet (göreceli) | 1× | 2× | 3–4× | 5–8× |
| Tipik güç aralığı | ≤5 kW | 7.5–100 kW | 5–500 kW | Her güç |
| Enerji tasarrufu | Hayır | Hayır | Minimal | Büyük |
| Modbus haberleşme | Hayır | Hayır | Bazıları | Evet |
| PLC çıkış sayısı | 1 dijital | 3 dijital | 1–2 dijital | 1–2 dijital + seri |

---

### VFD Kontrol Mimarisi

VFD, PLC'den iki temel bilgi alır:

1. **Kontrol Kelimesi (Control Word):** Hangi işlemin yapılacağını belirten 16-bit register (çalış, dur, hata reset, yön...)
2. **Hız Referansı (Speed Reference):** 0–16384 arasında ölçeklenen değer (üreticiye göre değişir; bazıları 0–10000 veya Hz × 100 kullanır)

PLC ise iki temel bilgi okur:

1. **Durum Kelimesi (Status Word):** Drive'ın mevcut durumu (çalışıyor, hazır, hata, uyarı...)
2. **Gerçek Hız (Actual Speed):** Motor gerçek çalışma hızı veya frekansı

#### ABB ACS355 Modbus Register Haritası (Referans)

ABB ACS355 sürücüsünün varsayılan ABB Drives profili Modbus register haritası (resmi kullanım kılavuzundan; Modbus adresi 0-tabanlı):

| Modbus Adresi (0-tabanlı) | Belge Ref (1-tabanlı) | Veri | Yön | Açıklama |
|---|---|---|---|---|
| 0 | 40001 | Control Word | PLC → VFD | Kontrol komutu bitleri |
| 1 | 40002 | Speed Reference | PLC → VFD | 0–20000 = 0–%100 nominal |
| 2 | 40003 | Status Word | VFD → PLC | Sürücü durum bitleri |
| 3 | 40004 | Actual Speed | VFD → PLC | Gerçek hız (aynı ölçek) |
| 4 | 40005 | Motor Current | VFD → PLC | Mevcut akım (× 0.1 A) |
| 5 | 40006 | Motor Torque | VFD → PLC | Tork (%nominal) |
| 6 | 40007 | DC Bus Voltage | VFD → PLC | DC bara voltajı (V) |
| 7 | 40008 | Drive Temp | VFD → PLC | Sürücü sıcaklığı (°C) |

Kaynak: [ABB ACS355 User Manual — Modbus Mapping, Page 312](https://www.manualslib.com/manual/1248960/Abb-Acs355.html?page=312)

**ABB ACS355 Control Word bit haritası (ABB Drives Profili):**

| Bit | Değer | Anlamı |
|---|---|---|
| 0 | 0x0001 | ON (1=açık, 0=kapalı) |
| 1 | 0x0002 | OFF2 — Serbest duruş |
| 2 | 0x0004 | OFF3 — Hızlı fren |
| 3 | 0x0008 | INHIBIT_OPERATION |
| 4 | 0x0010 | RAMP_OUTPUT_ZERO |
| 5 | 0x0020 | RAMP_HOLD |
| 6 | 0x0040 | RAMP_IN_ZERO |
| 7 | 0x0080 | RESET (yükselen kenar — hata reset) |
| 10 | 0x0400 | REMOTE_CMD (uzak komut aktif) |
| 11 | 0x0800 | EXT_CTRL_LOC (kontrol lokasyonu) |

**Tipik komut değerleri (ABB ACS355):**

| Durum | Hex Değer | Ondalık | Açıklama |
|---|---|---|---|
| Hazır (Enabled) | 0x047E | 1150 | ON + tüm OFF bitleri aktif, REMOTE |
| Çalıştır | 0x047F | 1151 | ON + OPERATION + REMOTE |
| Durdur | 0x047E | 1150 | Bit 0 sıfırlanır |
| Hata Reset | 0x04FF | 1279 | Bit 7 (RESET) = 1; sonra normal cmd |

#### Danfoss FC302 Modbus Register Haritası (Referans)

Danfoss FC 301/302 sürücüsünün FC profili (Danfoss FC Control Profile):

| Modbus Adresi (0-tabanlı) | Belge Ref | Veri | Yön | Açıklama |
|---|---|---|---|---|
| 49999 | 50000 | Control Word | PLC → VFD | FC Profil kontrol bitleri |
| 49998 | 49999 | Speed Reference | PLC → VFD | 0–16384 = 0–max frekans |
| 50000 | 50001 | Status Word | VFD → PLC | FC Profil durum bitleri |
| 50001 | 50002 | Actual Output Freq | VFD → PLC | Hz × 10 (örn. 500 = 50.0 Hz) |

**Danfoss FC Control Word tipik komutlar:**

| Durum | Hex | Açıklama |
|---|---|---|
| Çalıştır | 0x047F | Run komutu + normal rampa + hız referansı etkin |
| Durdur (serbest) | 0x047E | Bit 0 sıfır = coast stop |
| Hızlı Dur | 0x047B | Quick stop komutu |
| DC Fren | 0x0473 | DC brake komutu |

Kaynak: [Danfoss FC 301/302 Programming Guide MG33MO02](https://files.danfoss.com/download/Drives/MG33MO02.pdf), [Danfoss FC302 Modbus RTU Tutorial](https://plc247.com/danfoss-fc302-modbus-rtu-via-modbus-poll-tutorial/)

---

### Motor Koruma Mekanizmaları

#### Termik Aşırı Yük Koruması

Klasik uygulama: Termik röle (overload relay), motor sargılarında aşırı ısınmayı simüle etmek için bimetal şeritler kullanır ve motor akımı sürekli olarak ayar değerinin üstünde kalırsa kontaktörü açar. PLC tarafına normalde-kapalı (NC) dijital giriş olarak bağlanır.

VFD uygulamalarında: VFD kendi motorunu dahili modelle korur; ek termik röle gerekmeyebilir — ancak standartlar fiziksel koruma önerir.

#### Faz Kaybı Koruması (Phase Loss Detection)

Üç fazlı bir motor tek fazla çalışmaya devam ederse kalan iki fazda akım 1.73× artar, sargılar dakikalar içinde hasar görür. Faz kaybı iki yöntemle tespit edilir:

1. **Faz izleme rölesi (Phase Monitoring Relay):** Donanım düzeyinde; üç fazı sürekli izler, 10–100 ms içinde kontaktörü açar
2. **CT tabanlı PLC koruması:** Her fazda akım trafosu (CT), analog giriş — PLC kodu %10 dengesizlikte uyarı, %25 dengesizlikte trip üretir

#### Motor Termal Modeli (PLC İçinde)

VFD veya modern koruma röleleri matematiksel bir termal model hesaplar:

```
θ(t) = θ_amb + (θ_max - θ_amb) × [1 - exp(-t/τ)]

Burada:
  θ(t)    : t anındaki tahmini sargı sıcaklığı
  θ_amb   : Ortam sıcaklığı
  θ_max   : I²R ile belirlenen maksimum denge sıcaklığı
  τ       : Termal zaman sabiti (tipik: 5–30 dakika motor boyutuna göre)
```

PLC tarafında basit bir termal biriktirme sayacı kullanılabilir (bkz. Örnekler bölümü).

---

## Pratikte Nasıl Kullanılır

### DOL Motor Kontrolü — CODESYS Kurulumu

DOL için minimum PLC çıkışı: 1 dijital çıkış (kontaktör bobini)

```
CODESYS Proje Yapısı (DOL):
    GVL_IO:
        xMotor1_StartCmd  AT %Q0.0 : BOOL;  (* Kontaktör bobini *)
        xMotor1_FB        AT %I0.0 : BOOL;  (* Geri bildirim — NC aux contact *)
        xMotor1_OL_Trip   AT %I0.1 : BOOL;  (* Termik röle NC girişi *)
    
    DUT:
        E_MotorState : ENUM (eIdle, eStarting, eRunning, eStopping, eFault)
    
    FB_MotorDOL:
        VAR_INPUT: xStartCmd, xStopCmd, xFaultReset, xRunFeedback, xOverload
        VAR_OUTPUT: xRunOutput, xRunning, xFault, eState
```

### Yıldız-Üçgen Motor Kontrolü — CODESYS Kurulumu

Yıldız-üçgen için 3 dijital çıkış: Q_Main (ana), Q_Star (yıldız), Q_Delta (üçgen)

```
CODESYS Proje Yapısı (Yıldız-Üçgen):
    GVL_IO:
        xMotor_MainCtctr  AT %Q0.0 : BOOL;  (* Ana kontaktör Q1 *)
        xMotor_StarCtctr  AT %Q0.1 : BOOL;  (* Yıldız kontaktörü Q_Y *)
        xMotor_DeltaCtctr AT %Q0.2 : BOOL;  (* Üçgen kontaktörü Q_D *)
        xMotor_FB         AT %I0.0 : BOOL;  (* Motor geri bildirimi *)
        xMotor_OL_Trip    AT %I0.1 : BOOL;  (* Termik röle *)
    
    FB_MotorStarDelta:
        Durum: eIdle → eStarStart → eStarRunning → eTransition → eDeltaRunning → eStopping
        tStarTimer : TON;        (* Yıldız süresi — tipik 5–10 saniye *)
        tTransTimer: TON;        (* Geçiş boşluk süresi — tipik 50–100 ms *)
```

**Kritik güvenlik kuralı:** Q_Star ve Q_Delta aynı anda açık olamaz. CODESYS kodunda hem yazılım hem de donanım interlok şarttır:

```iecst
(* Yazılım interlok — her döngüde *)
IF xMotor_DeltaCtctr THEN
    xMotor_StarCtctr := FALSE;   (* Zorla sıfırla *)
END_IF
```

### VFD Kontrolü — Modbus TCP Yapılandırması

VFD'nin Modbus TCP destekli versiyonları için (ABB ACS580, Danfoss FC302 MCA120 opsiyon kartı vb.):

```
CODESYS Proje Yapısı (VFD Modbus TCP):
    GVL_Modbus_VFD1:
        (* Master olarak CODESYS, VFD slave *)
        wControlWord     : WORD;      (* PLC → VFD: HR 0 *)
        wSpeedReference  : WORD;      (* PLC → VFD: HR 1 (0–20000) *)
        wStatusWord      : WORD;      (* VFD → PLC: HR 2 okunur *)
        wActualSpeed     : WORD;      (* VFD → PLC: HR 3 okunur *)
        wMotorCurrent    : WORD;      (* VFD → PLC: HR 4 — ×0.1 A *)
    
    FB_VFD_ModbusTCP:
        Modbus TCP Master FB → her 100 ms'de FC03 ile durum oku, FC16 ile komut yaz
```

**Modbus TCP Master olarak CODESYS:** CODESYS Modbus TCP kütüphanesi kullanılır. Device Tree'ye `Modbus_TCP_Master` eklenir; her slave (VFD) ayrı bir cihaz objesi olarak tanımlanır.

---

## Örnekler

### Örnek 1: FB_MotorDOL — Tam DOL Motor Kontrol Function Block

```iecst
(* DUT dosyasında — E_MotorState zaten 02_project_structure.md'de tanımlı *)
TYPE E_MotorState :
(
    eIdle      := 0,
    eStarting  := 1,
    eRunning   := 2,
    eStopping  := 3,
    eFault     := 4
);
END_TYPE

(* Diagnostik struct *)
TYPE ST_MotorDiag :
STRUCT
    tTotalRunTime   : TIME;      (* Toplam çalışma süresi *)
    nStartCount     : DINT;      (* Toplam start sayısı *)
    tLastFaultTime  : TIME;      (* Son hata zamanı *)
    rLastCurrent    : REAL;      (* Son ölçülen akım A *)
END_STRUCT
END_TYPE

(* FB_MotorDOL — DOL motor kontrolü için tam Function Block *)
FUNCTION_BLOCK FB_MotorDOL
VAR_INPUT
    xStartCmd       : BOOL;              (* Start komutu — HMI veya sekans *)
    xStopCmd        : BOOL;              (* Stop komutu *)
    xFaultReset     : BOOL;              (* Hata sıfırlama — yükselen kenar *)
    xRunFeedback    : BOOL;              (* Motor geri bildirimi — aux contact *)
    xOverload       : BOOL;              (* Termik röle trip — NC = TRUE normal *)
    xEmergencyStop  : BOOL := TRUE;      (* Acil stop — NC = TRUE normal *)
    tStartTimeout   : TIME := T#5S;      (* Geri bildirim bekleme süresi *)
    bEnabled        : BOOL := TRUE;      (* FALSE → FB hiç çalışmaz *)
END_VAR
VAR_OUTPUT
    xRunOutput      : BOOL;              (* Kontaktör bobini çıkışı *)
    xRunning        : BOOL;              (* Onaylı çalışma *)
    xReady          : BOOL;              (* Başlatmaya hazır *)
    xFault          : BOOL;              (* Aktif hata bayrağı *)
    eState          : E_MotorState;      (* Mevcut durum *)
    sLastFaultMsg   : STRING(80);        (* Son hata mesajı *)
END_VAR
VAR_IN_OUT
    stDiag          : ST_MotorDiag;      (* Diagnostik — FB günceller *)
END_VAR
VAR
    tStartTimer     : TON;               (* Geri bildirim bekleme zamanlayıcı *)
    tRunTimer       : TON;               (* Çalışma süresi sayacı *)
    fbRTrig_Reset   : R_TRIG;           (* Reset yükselen kenar *)
    fbRTrig_Start   : R_TRIG;           (* Start yükselen kenar — sayaç için *)
    bLastState      : BOOL;
END_VAR

(* ─── Kenar tespiti ─── *)
fbRTrig_Reset(CLK := xFaultReset);
fbRTrig_Start(CLK := xStartCmd);

(* ─── Giriş sınır kontrolü ─── *)
IF tStartTimeout < T#1S  THEN tStartTimeout := T#1S;  END_IF
IF tStartTimeout > T#60S THEN tStartTimeout := T#60S; END_IF

(* ─── Acil stop ve aşırı yük — her durumda aktif ─── *)
IF NOT xEmergencyStop OR NOT xOverload THEN
    IF eState = eRunning OR eState = eStarting THEN
        xFault := TRUE;
        IF NOT xEmergencyStop THEN
            sLastFaultMsg := 'Emergency stop active';
        ELSE
            sLastFaultMsg := 'Overload trip detected';
        END_IF
        stDiag.tLastFaultTime := stDiag.tTotalRunTime;
        eState := eFault;
    END_IF
END_IF

(* ─── Durum makinesi ─── *)
CASE eState OF

    eIdle:
        xRunOutput  := FALSE;
        xRunning    := FALSE;
        xReady      := bEnabled AND NOT xFault AND xEmergencyStop AND xOverload;

        IF xStartCmd AND bEnabled AND NOT xFault
           AND xEmergencyStop AND xOverload THEN
            tStartTimer(IN := FALSE);   (* Timer sıfırla *)
            stDiag.nStartCount := stDiag.nStartCount + 1;
            eState := eStarting;
        END_IF

    eStarting:
        xRunOutput  := TRUE;
        xReady      := FALSE;
        tStartTimer(IN := TRUE, PT := tStartTimeout);

        (* Geri bildirim gelirse hemen çalışma durumuna geç *)
        IF xRunFeedback THEN
            tStartTimer(IN := FALSE);
            eState := eRunning;

        (* Geri bildirim zamanında gelmezse hata *)
        ELSIF tStartTimer.Q THEN
            tStartTimer(IN := FALSE);
            xFault := TRUE;
            xRunOutput := FALSE;
            sLastFaultMsg := 'Run feedback timeout at start';
            stDiag.tLastFaultTime := stDiag.tTotalRunTime;
            eState := eFault;

        (* Durdurma komutu başlangıç sırasında gelirse *)
        ELSIF xStopCmd OR NOT bEnabled THEN
            tStartTimer(IN := FALSE);
            xRunOutput := FALSE;
            eState := eIdle;
        END_IF

    eRunning:
        xRunOutput  := TRUE;
        xRunning    := TRUE;

        (* Çalışma süresi takibi *)
        tRunTimer(IN := TRUE, PT := T#24H);
        IF tRunTimer.Q THEN
            stDiag.tTotalRunTime := stDiag.tTotalRunTime + T#24H;
            tRunTimer(IN := FALSE);
        END_IF
        stDiag.tTotalRunTime := stDiag.tTotalRunTime
                                 + TIME_TO_TIME(T#10MS);  (* Cycle eklenir *)

        (* Geri bildirim kesilirse hata *)
        IF NOT xRunFeedback THEN
            xFault := TRUE;
            sLastFaultMsg := 'Run feedback lost during operation';
            stDiag.tLastFaultTime := stDiag.tTotalRunTime;
            eState := eFault;

        (* Stop komutu *)
        ELSIF xStopCmd OR NOT bEnabled THEN
            eState := eStopping;
        END_IF

    eStopping:
        xRunOutput  := FALSE;
        xRunning    := FALSE;
        (* Dönüş geri bildirimi sıfırlanana kadar bekle — opsiyonel *)
        IF NOT xRunFeedback THEN
            eState := eIdle;
        END_IF

    eFault:
        xRunOutput  := FALSE;
        xRunning    := FALSE;
        xFault      := TRUE;

        IF fbRTrig_Reset.Q AND xEmergencyStop AND xOverload THEN
            xFault        := FALSE;
            sLastFaultMsg := '';
            eState        := eIdle;
        END_IF

    ELSE:
        (* Bilinmeyen durum — güvenli duruma geç *)
        xRunOutput  := FALSE;
        xFault      := TRUE;
        sLastFaultMsg := 'Unknown state — safe stop';
        eState      := eFault;

END_CASE

(* ─── Çıkış özetleme ─── *)
xReady := (eState = eIdle) AND bEnabled AND NOT xFault
           AND xEmergencyStop AND xOverload;
```

---

### Örnek 2: FB_MotorStarDelta — Yıldız-Üçgen Kontrolü

```iecst
TYPE E_StarDeltaState :
(
    eSD_Idle        := 0,
    eSD_StarStart   := 1,     (* Yıldız: Q_Main + Q_Star açık *)
    eSD_StarRun     := 2,     (* Yıldız çalışma süresi doluyor *)
    eSD_Transition  := 3,     (* Her iki kontaktör kapalı — boşluk *)
    eSD_DeltaRun    := 4,     (* Üçgen: Q_Main + Q_Delta açık *)
    eSD_Stopping    := 5,
    eSD_Fault       := 6
);
END_TYPE

FUNCTION_BLOCK FB_MotorStarDelta
VAR_INPUT
    xStartCmd       : BOOL;
    xStopCmd        : BOOL;
    xFaultReset     : BOOL;
    xRunFeedback    : BOOL;
    xOverload       : BOOL := TRUE;    (* NC — TRUE = normal *)
    tStarTime       : TIME := T#8S;    (* Yıldız aşaması süresi *)
    tTransTime      : TIME := T#80MS;  (* Y→Δ geçiş boşluk süresi *)
    tFBTimeout      : TIME := T#5S;    (* Geri bildirim bekleme *)
    bEnabled        : BOOL := TRUE;
END_VAR
VAR_OUTPUT
    xMainOutput     : BOOL;   (* Q1 — Ana kontaktör *)
    xStarOutput     : BOOL;   (* Q_Y — Yıldız kontaktörü *)
    xDeltaOutput    : BOOL;   (* Q_D — Üçgen kontaktörü *)
    xRunning        : BOOL;
    xFault          : BOOL;
    eState          : E_StarDeltaState;
    sLastFaultMsg   : STRING(80);
END_VAR
VAR
    tStarTimer      : TON;
    tTransTimer     : TON;
    tFBTimer        : TON;
    fbRTrig_Reset   : R_TRIG;
END_VAR

fbRTrig_Reset(CLK := xFaultReset);

(* ─── Yazılım interlok — güvenlik için her döngüde ─── *)
(* Delta açıksa Star kesinlikle kapalı olmalı *)
IF xDeltaOutput AND xStarOutput THEN
    xStarOutput := FALSE;   (* Zorla sıfırla — kısa devre önleme *)
    xFault := TRUE;
    sLastFaultMsg := 'Star-Delta interlock violation!';
    eState := eSD_Fault;
END_IF

CASE eState OF

    eSD_Idle:
        xMainOutput  := FALSE;
        xStarOutput  := FALSE;
        xDeltaOutput := FALSE;
        xRunning     := FALSE;

        IF xStartCmd AND bEnabled AND NOT xFault AND xOverload THEN
            tStarTimer(IN := FALSE);
            tFBTimer(IN := FALSE);
            eState := eSD_StarStart;
        END_IF

    eSD_StarStart:
        xMainOutput  := TRUE;
        xStarOutput  := TRUE;
        xDeltaOutput := FALSE;

        (* Geri bildirim gelene kadar bekle *)
        tFBTimer(IN := TRUE, PT := tFBTimeout);
        IF xRunFeedback THEN
            tFBTimer(IN := FALSE);
            eState := eSD_StarRun;
        ELSIF tFBTimer.Q THEN
            tFBTimer(IN := FALSE);
            xFault := TRUE;
            xMainOutput := FALSE;
            xStarOutput := FALSE;
            sLastFaultMsg := 'No run feedback at star start';
            eState := eSD_Fault;
        END_IF

    eSD_StarRun:
        xMainOutput  := TRUE;
        xStarOutput  := TRUE;
        xDeltaOutput := FALSE;

        tStarTimer(IN := TRUE, PT := tStarTime);
        IF tStarTimer.Q THEN
            tStarTimer(IN := FALSE);
            (* Yıldız kontaktörünü kapat *)
            xStarOutput := FALSE;
            tTransTimer(IN := FALSE);
            eState := eSD_Transition;
        END_IF

        IF xStopCmd THEN
            tStarTimer(IN := FALSE);
            eState := eSD_Stopping;
        END_IF

    eSD_Transition:
        xMainOutput  := TRUE;
        xStarOutput  := FALSE;   (* Yıldız kapalı *)
        xDeltaOutput := FALSE;   (* Delta henüz açık değil *)

        (* Her iki kontaktör kapalı — mekanik geçiş süresi *)
        tTransTimer(IN := TRUE, PT := tTransTime);
        IF tTransTimer.Q THEN
            tTransTimer(IN := FALSE);
            xDeltaOutput := TRUE;  (* Delta aç *)
            eState := eSD_DeltaRun;
        END_IF

    eSD_DeltaRun:
        xMainOutput  := TRUE;
        xStarOutput  := FALSE;
        xDeltaOutput := TRUE;
        xRunning     := TRUE;

        (* Geri bildirim kaybı *)
        IF NOT xRunFeedback THEN
            xFault := TRUE;
            sLastFaultMsg := 'Feedback lost in delta run';
            eState := eSD_Fault;
        ELSIF xStopCmd OR NOT bEnabled THEN
            eState := eSD_Stopping;
        ELSIF NOT xOverload THEN
            xFault := TRUE;
            sLastFaultMsg := 'Overload trip in delta run';
            eState := eSD_Fault;
        END_IF

    eSD_Stopping:
        xMainOutput  := FALSE;
        xStarOutput  := FALSE;
        xDeltaOutput := FALSE;
        xRunning     := FALSE;
        IF NOT xRunFeedback THEN
            eState := eSD_Idle;
        END_IF

    eSD_Fault:
        xMainOutput  := FALSE;
        xStarOutput  := FALSE;
        xDeltaOutput := FALSE;
        xRunning     := FALSE;
        xFault       := TRUE;

        IF fbRTrig_Reset.Q AND xOverload THEN
            xFault        := FALSE;
            sLastFaultMsg := '';
            eState        := eSD_Idle;
        END_IF

    ELSE:
        xMainOutput  := FALSE;
        xStarOutput  := FALSE;
        xDeltaOutput := FALSE;
        xFault       := TRUE;
        sLastFaultMsg := 'Unknown SD state';
        eState       := eSD_Fault;

END_CASE
```

---

### Örnek 3: FB_VFD_Modbus — VFD Modbus Haberleşmesi (ABB ACS355 / Danfoss FC302)

```iecst
(*
 * FB_VFD_Modbus — VFD'yi Modbus TCP/RTU üzerinden kontrol eder
 * ABB ACS355 ve Danfoss FC302 için uyarlanmıştır.
 * Modbus Master FB'si CODESYS Modbus TCP kütüphanesinden sağlanır.
 * Burada kontrol kelimesi ve hız referansı mantığı gösterilmektedir.
 *)

TYPE E_VFD_State :
(
    eVFD_Idle        := 0,
    eVFD_Enabling    := 1,
    eVFD_Running     := 2,
    eVFD_Stopping    := 3,
    eVFD_Fault       := 4,
    eVFD_CommError   := 5
);
END_TYPE

FUNCTION_BLOCK FB_VFD_Modbus
VAR_INPUT
    xStartCmd       : BOOL;                  (* Çalıştır komutu *)
    xStopCmd        : BOOL;                  (* Durdur komutu *)
    xFaultReset     : BOOL;                  (* VFD hata reset — yükselen kenar *)
    rSpeedRef_RPM   : REAL;                  (* Hız referansı (RPM veya %) *)
    rSpeedMax_RPM   : REAL := 1500.0;        (* Maksimum motor hızı *)
    bEnabled        : BOOL := TRUE;
    bCommOK         : BOOL;                  (* Modbus haberleşme OK bayrağı *)
    (* VFD'den okunan ham Modbus register değerleri *)
    wStatusWord_In  : WORD;                  (* VFD status word — HR 2 *)
    wActualSpeed_In : WORD;                  (* Gerçek hız — HR 3 *)
    wCurrent_In     : WORD;                  (* Akım × 0.1 A — HR 4 *)
END_VAR
VAR_OUTPUT
    (* VFD'ye yazılacak ham Modbus register değerleri *)
    wControlWord_Out: WORD;                  (* Kontrol kelimesi → HR 0 *)
    wSpeedRef_Out   : WORD;                  (* Hız referansı → HR 1 (0–20000) *)
    (* İşlenmiş çıkışlar *)
    xRunning        : BOOL;
    xFault_VFD      : BOOL;                  (* VFD dahili hatası *)
    xCommFault      : BOOL;                  (* Haberleşme hatası *)
    rActualSpeed_RPM: REAL;                  (* Gerçek hız RPM *)
    rMotorCurrent_A : REAL;                  (* Motor akımı A *)
    eState          : E_VFD_State;
    sLastFaultMsg   : STRING(80);
END_VAR
VAR
    fbRTrig_Reset   : R_TRIG;
    fbRTrig_Start   : R_TRIG;
    tCommWatchdog   : TON;                   (* Haberleşme kesintisi izleyici *)
    wLastStatus     : WORD;
    (* ABB ACS355 kontrol kelimesi sabitleri *)
    CW_ENABLE       : WORD := 16#047E;       (* Enabled — hazır *)
    CW_RUN          : WORD := 16#047F;       (* Çalıştır *)
    CW_RESET        : WORD := 16#04FF;       (* Hata reset *)
    CW_STOP         : WORD := 16#047E;       (* Durdur *)
    (* ABB ACS355 status word bit maskeleri *)
    SW_READY        : WORD := 16#0001;       (* Bit 0 — Ready *)
    SW_ENABLED      : WORD := 16#0002;       (* Bit 1 — Enabled *)
    SW_RUNNING      : WORD := 16#0004;       (* Bit 2 — Running *)
    SW_FAULT        : WORD := 16#0008;       (* Bit 3 — Fault *)
    SW_ATSETPOINT   : WORD := 16#0100;       (* Bit 8 — At setpoint *)
END_VAR

fbRTrig_Reset(CLK := xFaultReset);
fbRTrig_Start(CLK := xStartCmd);

(* ─── Haberleşme watchdog ─── *)
tCommWatchdog(IN := NOT bCommOK, PT := T#3S);
IF tCommWatchdog.Q THEN
    xCommFault := TRUE;
    IF eState <> eVFD_CommError THEN
        sLastFaultMsg := 'Modbus communication lost';
        eState := eVFD_CommError;
    END_IF
ELSE
    xCommFault := FALSE;
END_IF

(* ─── Hız referansı ölçekleme: RPM → 0..20000 ─── *)
(* ABB ACS355: 20000 = %100 nominal hız *)
IF rSpeedMax_RPM > 0.0 THEN
    wSpeedRef_Out := REAL_TO_WORD(
        LIMIT(0.0, (rSpeedRef_RPM / rSpeedMax_RPM) * 20000.0, 20000.0)
    );
ELSE
    wSpeedRef_Out := 0;
END_IF

(* ─── Gerçek hız okuma ─── *)
rActualSpeed_RPM := (WORD_TO_REAL(wActualSpeed_In) / 20000.0) * rSpeedMax_RPM;
rMotorCurrent_A  := WORD_TO_REAL(wCurrent_In) * 0.1;  (* × 0.1 A *)

(* ─── Status word bit analizi ─── *)
xRunning   := (wStatusWord_In AND SW_RUNNING) <> 0;
xFault_VFD := (wStatusWord_In AND SW_FAULT)   <> 0;

(* ─── Durum makinesi ─── *)
CASE eState OF

    eVFD_Idle:
        wControlWord_Out := CW_ENABLE;  (* Drive enable — hazır konumda bekle *)

        IF xStartCmd AND bEnabled AND NOT xFault_VFD AND bCommOK THEN
            eState := eVFD_Enabling;
        END_IF

    eVFD_Enabling:
        wControlWord_Out := CW_RUN;    (* Çalıştır komutu gönder *)

        IF xRunning THEN
            eState := eVFD_Running;
        ELSIF xFault_VFD THEN
            xFault_VFD := TRUE;
            sLastFaultMsg := 'VFD fault at start';
            eState := eVFD_Fault;
        ELSIF xStopCmd OR NOT bEnabled THEN
            eState := eVFD_Stopping;
        END_IF

    eVFD_Running:
        wControlWord_Out := CW_RUN;    (* Çalışma komutu sürekli *)

        IF NOT xRunning AND (wStatusWord_In AND SW_FAULT) <> 0 THEN
            xFault_VFD := TRUE;
            sLastFaultMsg := 'VFD fault during run';
            eState := eVFD_Fault;
        ELSIF xStopCmd OR NOT bEnabled THEN
            eState := eVFD_Stopping;
        END_IF

    eVFD_Stopping:
        wControlWord_Out := CW_STOP;   (* Durdur komutu *)
        wSpeedRef_Out    := 0;

        IF NOT xRunning THEN
            eState := eVFD_Idle;
        END_IF

    eVFD_Fault:
        wControlWord_Out := CW_ENABLE;  (* Güvenli seviye *)

        IF fbRTrig_Reset.Q THEN
            (* Reset pulse: önce reset komutu, sonra enable *)
            wControlWord_Out := CW_RESET;
            xFault_VFD  := FALSE;
            sLastFaultMsg := '';
            eState := eVFD_Idle;
        END_IF

    eVFD_CommError:
        wControlWord_Out := CW_STOP;    (* Haberleşme yoksa dur *)
        wSpeedRef_Out    := 0;

        IF bCommOK THEN
            xCommFault := FALSE;
            eState := eVFD_Idle;
        END_IF

    ELSE:
        wControlWord_Out := CW_STOP;
        wSpeedRef_Out    := 0;
        sLastFaultMsg := 'Unknown VFD state';
        eState := eVFD_Fault;

END_CASE
```

---

### Örnek 4: FB_VFD_Modbus Kullanımı (PRG_MotorControl)

```iecst
(*
 * PRG_MotorControl — Motor kontrol programı
 * FB_VFD_Modbus instance'larını yönetir ve I/O ile bağlar
 *)
PROGRAM PRG_MotorControl
VAR
    fbVFD1          : FB_VFD_Modbus;
    fbVFD2          : FB_VFD_Modbus;
    fbMotorDOL1     : FB_MotorDOL;
END_VAR

(* ─── VFD 1 çağrısı — Konveyör ana sürücü ─── *)
fbVFD1(
    xStartCmd        := GVL_HMI.xConveyor1_Start,
    xStopCmd         := GVL_HMI.xConveyor1_Stop OR GVL_Alarms.xEmgStop,
    xFaultReset      := GVL_HMI.xConveyor1_FaultReset,
    rSpeedRef_RPM    := GVL_Params.rConveyor1_SpeedRef,
    rSpeedMax_RPM    := GVL_Params.rConveyor1_SpeedMax,
    bEnabled         := NOT GVL_Alarms.xSafetyFault,
    bCommOK          := GVL_Modbus.xVFD1_CommOK,
    wStatusWord_In   := GVL_Modbus.wVFD1_StatusWord,
    wActualSpeed_In  := GVL_Modbus.wVFD1_ActualSpeed,
    wCurrent_In      := GVL_Modbus.wVFD1_Current
);

(* Çıkışları Modbus GVL'ye aktar *)
GVL_Modbus.wVFD1_ControlWord  := fbVFD1.wControlWord_Out;
GVL_Modbus.wVFD1_SpeedRef     := fbVFD1.wSpeedRef_Out;

(* Alarm bayraklarını GVL_Alarms'a aktar *)
GVL_Alarms.xConveyor1_Fault   := fbVFD1.xFault_VFD OR fbVFD1.xCommFault;

(* Diagnostik HMI'ya aktar *)
GVL_HMI.rConveyor1_Speed      := fbVFD1.rActualSpeed_RPM;
GVL_HMI.rConveyor1_Current    := fbVFD1.rMotorCurrent_A;
GVL_HMI.eConveyor1_State      := fbVFD1.eState;

(* ─── DOL Motor 1 çağrısı — Yardımcı fan motoru ─── *)
fbMotorDOL1(
    xStartCmd       := GVL_HMI.xFan1_Start,
    xStopCmd        := GVL_HMI.xFan1_Stop,
    xFaultReset     := GVL_HMI.xFan1_FaultReset,
    xRunFeedback    := GVL_IO.xFan1_RunFB,
    xOverload       := GVL_IO.xFan1_OL,
    xEmergencyStop  := GVL_IO.xEmgStop_NC
);
GVL_IO.xFan1_Contactor     := fbMotorDOL1.xRunOutput;
GVL_Alarms.xFan1_Fault     := fbMotorDOL1.xFault;
```

---

### Örnek 5: FB_ThermalProtection — Yazılım Termal Modeli

```iecst
(*
 * FB_ThermalProtection — Basit termal biriktirme modeli
 * Motor akım bilgisi VFD veya CT analogundan gelir.
 * Resmi standart: IEC 60255-149 (termal aşırı yük koruma karakteristiği)
 * NOT: Bu yalnızca ek izleme içindir; birincil koruma donanımsal röle olmalıdır.
 *)
FUNCTION_BLOCK FB_ThermalProtection
VAR_INPUT
    rActualCurrent  : REAL;       (* Motor akımı — A cinsinden *)
    rRatedCurrent   : REAL;       (* Motor nominal akımı — A *)
    rThermalLimit   : REAL := 100.0;  (* % termal limit (100 = tam) *)
    rCoolRate       : REAL := 0.02;   (* Soğuma hızı (her döngüde %) *)
    bMotorRunning   : BOOL;
    tCycleTime      : TIME := T#10MS; (* Task cycle süresi *)
END_VAR
VAR_OUTPUT
    rThermalImage   : REAL;       (* Birikmiş termal yük — % *)
    xThermalWarning : BOOL;       (* %80 üstü — uyarı *)
    xThermalTrip    : BOOL;       (* Limit aşıldı — trip *)
END_VAR
VAR
    rCurrentRatio   : REAL;
    rCycleSec       : REAL;
END_VAR

rCycleSec := TIME_TO_REAL(tCycleTime) / 1000.0;  (* ms → saniye *)

(* Motor akım oranı: (I/I_rated)² *)
IF rRatedCurrent > 0.0 THEN
    rCurrentRatio := (rActualCurrent / rRatedCurrent);
    rCurrentRatio := rCurrentRatio * rCurrentRatio;  (* I²R etkisi *)
ELSE
    rCurrentRatio := 0.0;
END_IF

(* Termal imaj güncelleme *)
IF bMotorRunning THEN
    (* Isınma: akım oranına göre artış *)
    rThermalImage := rThermalImage + (rCurrentRatio * rCycleSec * 0.5);
ELSE
    (* Soğuma: motor durursa termal imaj azalır *)
    rThermalImage := rThermalImage - (rCoolRate * rCycleSec);
END_IF

(* Sınır kontrol *)
rThermalImage   := LIMIT(0.0, rThermalImage, 150.0);  (* Max 150% *)
xThermalWarning := rThermalImage >= (rThermalLimit * 0.8);   (* %80 uyarı *)
xThermalTrip    := rThermalImage >= rThermalLimit;            (* %100 trip *)
```

---

### Örnek 6: Jog (İmpuls Çalıştırma) ve Yön Kontrolü

```iecst
(*
 * VFD'de jog ve yön kontrolü — FB_VFD_Modbus'a ek olarak
 * Jog: Basılı tutulduğu sürece düşük hızda çalışır
 * Yön: İleri / geri seçimi
 *)
FUNCTION_BLOCK FB_VFD_JogDirection
VAR_INPUT
    xJogForward     : BOOL;      (* Jog ileri — basılı tut *)
    xJogReverse     : BOOL;      (* Jog geri — basılı tut *)
    xForwardSelect  : BOOL;      (* İleri yön seçimi *)
    rJogSpeed_RPM   : REAL := 100.0;  (* Jog hızı *)
    rNormalSpeed_RPM: REAL;      (* Normal çalışma hızı *)
    rSpeedMax_RPM   : REAL := 1500.0;
END_VAR
VAR_OUTPUT
    rSpeedRef_Out   : REAL;      (* FB_VFD_Modbus.rSpeedRef_RPM'e bağlanır *)
    xReverseCmd     : BOOL;      (* VFD yön komutu — control word bit 11 *)
END_VAR

(* Yön seçimi — jog sırasında da geçerli *)
xReverseCmd := NOT xForwardSelect;

(* Jog ileri aktifse: pozitif düşük hız *)
IF xJogForward AND NOT xJogReverse THEN
    rSpeedRef_Out := rJogSpeed_RPM;
    xReverseCmd   := FALSE;  (* Jog ileri = pozitif yön *)

(* Jog geri aktifse: negatif yön, düşük hız *)
ELSIF xJogReverse AND NOT xJogForward THEN
    rSpeedRef_Out := rJogSpeed_RPM;
    xReverseCmd   := TRUE;   (* Jog geri = negatif yön *)

(* Normal çalışma *)
ELSE
    rSpeedRef_Out := rNormalSpeed_RPM;
END_IF
```

---

## Sık Yapılan Hatalar

### Hata 1: Yıldız ve Üçgen Kontaktörlerini Aynı Anda Açmak

```
Senaryo: Yazılımda interlock yok. Kısa bir program hatası nedeniyle
         Q_Star ve Q_Delta aynı anda aktif oldu → faz-faz kısa devre.

Sonuç: Kontaktör kıvılcımla yandı, motor sargıları hasar gördü.

Çözüm:
  1. Yazılım interlok (her döngüde çalışır — yukarıdaki örnek)
  2. Donanım interlok (kontaktörlerin mekanik bağlantısı)
  3. CODESYS'te güvenlik görevine (Safety Task) taşınan interlock mantığı
```

### Hata 2: VFD Control Word'ü Sürekli Sıfırlamamak

```iecst
(* ❌ YANLIŞ — Reset komutu sürekli gönderiliyor *)
IF xFaultReset THEN
    wControlWord := CW_RESET;   (* Her scan'de reset — VFD reset döngüsüne giriyor *)
END_IF

(* ✅ DOĞRU — Yükselen kenar ile reset *)
fbRTrig_Reset(CLK := xFaultReset);
IF fbRTrig_Reset.Q THEN
    wControlWord := CW_RESET;   (* Yalnızca bir kez *)
    (* Sonraki döngüde normal CW_ENABLE gönderilir *)
END_IF
```

### Hata 3: Modbus Register Adresini 1 Tabanlı Kullanmak

```
Üretici belgesi: "Control Word: Register 40001"
Hatalı kod: write_register(address=40001, ...)
Sonuç: Exception 0x02 — Illegal Data Address

Doğrusu: address = 40001 - 40001 = 0
→ write_register(address=0, ...)

CODESYS Modbus Master yapılandırmasında "Starting Address" alanına
protokol adresi (0-tabanlı) girilmelidir.
```

### Hata 4: Geri Bildirim Olmadan Motor Çalışıyor Saymak

```
Senaryo: Kontaktör çıkış verildi, geri bildirim aux contact bağlanmadı.
         xRunFeedback sürekli FALSE → FB eState = eStarting'te takılı.

Çözüm:
  tStartTimeout sonunda eFault'a geçmeli ve operatörü uyarmalı.
  Geri bildirim bağlantısı her montajda doğrulanmalı.
  Test prosedürü: Kontaktörü elle kapat, xRunFeedback TRUE oldu mu kontrol et.
```

### Hata 5: VFD Hız Referansı Ölçekleme Hatası

```
Senaryo: Danfoss FC302 hız referansı 0–16384 iken ABB ACS355 için
         0–20000 kullanıldı. Motor yanlış hızda çalıştı.

Çözüm: Her VFD için üretici kılavuzundaki ölçek faktörü doğrulanmalı.
Danfoss FC302: 0–16384 = 0–%100 (MG33MO02 belgesine göre)
ABB ACS355:   0–20000 = 0–%100 (ACS355 kullanım kılavuzuna göre)
```

### Hata 6: Yıldız Süresini Yanlış Ayarlamak

```
Çok kısa yıldız süresi (tStarTime < motor hızlanma süresi):
  Motor yıldızda yeterince hızlanamaz → üçgene geçişte yüksek akım darbesi
  Sonuç: Termik röle trip, motor ve kontaktör stresi

Çok uzun yıldız süresi:
  Motor yıldızda aşırı ısınır (yıldız konfigürasyonu sürekli çalışma için tasarlanmamış)

Doğru ayar yöntemi:
  1. Motor no-load (boş) hızlanma süresini ölç
  2. Tam yük altında test et
  3. Motor yıldızda nominal hıza ulaştıktan sonra 1–2 saniye ekle
  Pratik başlangıç: tStarTime := T#8S; — sonra ölçüme göre ayarla
```

### Hata 7: Modbus TCP Master Task Seçimi

```
❌ YANLIŞ: VFD Modbus okuma/yazma işlemini kontrol döngüsüyle aynı task'ta yapmak
   → Modbus gecikmeleri kontrol döngüsünü bozar

✅ DOĞRU: Modbus iletişimini ayrı bir task'ta (Task_Comm, 100ms) yönet
          Kontrol döngüsü (Task_Main, 10ms) yalnızca GVL değerlerini okusun
          PRG_CommManager ayrı bir task'ta çalışsın
```

---

## Ne Zaman Tercih Edilmeli / Edilmemeli

### DOL Ne Zaman?

```
✓ Motor gücü ≤ 5 kW (veya şebeke kapasitesine göre daha büyük)
✓ Başlatma frekansı düşük (saatte birkaç kez)
✓ Hız kontrolü gerekmiyor
✓ Bütçe kısıtlı, basit çözüm yeterli
✓ Fan, pompa, kompresör gibi direkt bağlı yük

✗ Büyük motorlar (şebeke gerilim düşüşü sorun çıkarır)
✗ Yumuşak başlatma gereksinimi olan mekanik yükler
✗ Sık start/stop gereken süreçler
```

### Yıldız-Üçgen Ne Zaman?

```
✓ 7.5 kW – 100 kW arası motor gücü
✓ Hız kontrolü yok, yalnızca başlatma akımını azaltmak isteniyor
✓ Üçgen bağlantılı (Δ) IEC motoru kullanılıyor (önemli: Y bağlantılı motora uygulanamaz!)
✓ Düşük yük altında başlatma (boş konveyör, boş pompa)

✗ Yıldız bağlantılı (Y) motor — uygulanamaz
✗ Hız kontrolü gerekiyor → VFD kullan
✗ Çok sık start/stop — kontaktör ömrü kısalır
✗ Yük yıldızda yeterli ivme sağlanmıyorsa
```

### Soft Starter Ne Zaman?

```
✓ Hız kontrolü gerekmez, yalnızca yumuşak başlatma / durdurma
✓ Pompa uygulamaları: Su darbesi (water hammer) önleme
✓ VFD'ye göre %40–60 maliyet tasarrufu önemliyse
✓ Panel boyutu kısıtlıysa (soft starter VFD'den kompakt)

✗ Hız kontrolü gerekiyor → VFD
✗ Sürekli düşük hızda çalışma → VFD (soft starter bypass konumunda)
✗ Enerji tasarrufu hedefi → VFD
```

### VFD Ne Zaman?

```
✓ Hız kontrolü zorunlu (proses gerektiriyor)
✓ Enerji tasarrufu hedefi (pompa/fan: hız %20↓ → güç %49↓)
✓ Hassas rampa kontrolü (ivmelenme/yavaşlama)
✓ Modbus/PROFINET entegrasyonu gerekiyor
✓ Çift yönlü çalışma (ileri/geri)
✓ Jog fonksiyonu

✗ Basit sabit hızlı uygulama → DOL veya soft starter (VFD gereksiz maliyet)
✗ Harmonik kirliliğine karşı hassas şebekeler (VFD harmonik üretir; filtre gerekebilir)
```

---

## Gerçek Proje Notları

**Not 1 — Yıldız-Üçgen Geçişinde Süpriz Akım Darbesi**
Bir un değirmeni konveyör motorunda (22 kW) yıldız-üçgen geçiş süresi 80 ms olarak ayarlanmıştı. Devre analizörü, geçiş sırasında kısa bir akım darbesi ölçüyordu — motor artık hızlanmış olduğu için üçgene geçişte gerilim farkı büyüktü. Termik röle her üçten birinde trip yapıyordu. Çözüm: Geçiş süresi 150 ms'ye çıkarıldı, mekanik interlock kontrol edildi. Sorun ortadan kalktı. Ders: Geçiş süresi sadece "açık devre kalma süresi" değil, motorun o anki hızını da etkiler.

**Not 2 — ABB ACS355 Register 0 ile 1 Karışıklığı**
Yeni mühendis ABB belgesindeki "Register 1 = Control Word" notasyonunu 1-tabanlı zannetti ve Modbus adres 1 kullandı. Gerçekte ABB belgesi 1-tabanlı notasyon kullanıyor, protokol adresi 0'dır. Sürücü anlamsız şekilde davranıyordu. Wireshark trace açıldı; adres 1'e yazıldığını görmek, doğru adresi bulmak 2 saat aldı. Çözüm: Register haritasına hem "belge notasyonu" hem "protokol adresi" sütunları eklendi.

**Not 3 — VFD Modbus Haberleşmesi ile Kontrol Döngüsü Çakışması**
Bir paketleme makinesinde VFD Modbus TCP iletişimi 10 ms'lik kontrol döngüsüyle aynı task'ta çalışıyordu. VFD TCP zaman aşımı (timeout) dönemlerinde kontrol döngüsü gecikiyordu ve konveyör hızı düzensizleşiyordu. Çözüm: Modbus iletişimi 100 ms'lik ayrı bir task'a taşındı. Kontrol döngüsü yalnızca GVL değişkenlerini okur/yazar; VFD haberleşmesi bağımsız çalışır. Bu tasarım deseni sonraki tüm projelerde standart haline geldi.

**Not 4 — Hız Referansı Ölçeği Yanlış — Parametre Değişti**
Danfoss FC302 üzerinde hız referansı 0–16384 olarak kodlanmıştı. Sürücü yazılım güncellemesi sonrası aynı referans değerleri yanlış hız üretiyor oldu. Belge incelendi: firmware güncellemeyle ölçek 0–20000'e geçmişti (ABB DC profili ile uyum için opsiyon). Ders: VFD firmware güncellemelerinden önce register haritası değişiklikleri kontrol edilmeli; ölçekleme sabitleri magic number olarak kodlanmamalı, parametreden okunmalı veya konfigurasyon dosyasında tutulmalı.

**Not 5 — Termal Koruma Yazılımı Donanımı Geçemez**
Bir proje yöneticisi "PLC termal modeli varken donanımsal overload relay'e gerek yok" dedi ve maliyet kesintisi için röleler çıkarıldı. Altı ay sonra sargı sensörü arızalandı, PLC termal modeli güncellenmedi (gerçek akım yerine 0 A okuyordu). Motor aşırı ısındı ve yandı. Ders: Yazılım termal modeli ek izleme içindir. IEC 60364-4-43 ve makine güvenlik standartları (EN 60204-1) fiziksel motor koruma elemanını zorunlu kılar.

**Not 6 — jog Fonksiyonu Rampa Süresini Etkiliyor**
VFD'de normal rampa süresi 5 saniyeydi; jog modu için ayrı bir rampa parametresi (P1.05 Jog Acceleration Time) 0.5 saniyeye ayarlıydı. Operatör jog modunda motoru konumlandırmaya çalışırken ani hız değişimi mekanik yatakları zorladı. Çözüm: Jog hız referansı düşürüldü (100 RPM) ve jog rampa süresi 2 saniyeye artırıldı. Jog modu için ayrı parametre grubu VFD kılavuzunda mutlaka incelenmeli.

**Not 7 — Modbus Comm-Loss'ta VFD Çalışmaya Devam Etti**
Bir pompa istasyonunda RS-485 hattı gevşek bir terminalden koptu; PLC `bCommOK` FALSE oldu ve FB_VFD_Modbus `eVFD_CommError`'a geçip `CW_STOP` göndermeyi denedi — ama yazacak hat yoktu. VFD ise kendi haberleşme watchdog'u (parametre P8-04 fieldbus timeout) "fault" yerine "son referansı koru" olarak yapılandırıldığından motor en son hızda çalışmaya devam etti. Ders: comm-loss güvenliği iki taraflıdır. PLC'nin stop göndermesi yeterli değil; VFD'nin kendi fieldbus timeout parametresi mutlaka "fault stop" veya "ramp to stop" olarak ayarlanmalı. Yazılım watchdog (tCommWatchdog) yalnızca PLC tarafını korur.

**Not 8 — Status Word Bit Maskesi Profil Bağımlı Çıktı**
FB_VFD_Modbus'taki `SW_RUNNING := 16#0004` (Bit 2) ABB Drives profili içindi. Müşteri sürücüyü "DCU Profile" (Drive Control Unit) ile devreye almıştı; aynı bit farklı anlam taşıyordu, "running" gerçekte Bit 1'deydi. xRunning hiç TRUE olmadı, FB `eVFD_Enabling`'de takıldı, start timeout fault'u verdi. Ders: Control/Status Word bit haritası yalnızca register adresine değil, seçili **drive profiline** de bağlıdır (ABB'de ABB Drives vs DCU vs Standard). Bit maskeleri sabit (CW_/SW_ literal) olarak FB'ye gömülmemeli, en azından profil seçimine göre parametrelenmeli.

**Not 9 — VFD Rampada Dururken Start Komutu — "Reverse Jerk"**
Operatör DEC rampasıyla (8 s) yavaşlayan bir fanı, tam durmadan tekrar başlattı. FB henüz `eVFD_Running`'e dönmemişti ama VFD hâlâ pozitif frekansta dönüyordu; yeni start + farklı yön seçimi VFD'nin DC bus'ında ani tork tersine dönmesine (reverse jerk) ve aşırı gerilim (overvoltage) trip'ine yol açtı. Çözüm: FB'ye "tam duruş onayı" eklendi — yön değişimi veya yeniden start yalnızca `wActualSpeed_In < eşik` iken kabul edilir. Büyük ataletli yüklerde VFD'nin DC bus chopper/fren direnci de gözden geçirilmeli.

---

## Edge Case'ler ve Sistem Limitleri

### Sınır Koşulları Tablosu

| Senaryo | Davranış | Doğru Tasarım |
|---------|----------|---------------|
| Modbus comm-loss | PLC stop gönderir ama hat yok → motor son refte | VFD fieldbus timeout = fault/ramp stop |
| Yanlış drive profili (ABB DCU vs Drives) | Status Word bit maskesi yanlış → xRunning hep FALSE | Bit maskelerini profile göre parametrele |
| Hız ref ölçek karışıklığı (16384 vs 20000) | Motor yanlış hızda | Ölçek sabitini magic number yapma, parametreden oku |
| Y-Δ geçişi motor hızlanmadan | Δ'ya geçişte yüksek akım darbesi, termik trip | tStarTime ölçüme dayalı; geçiş 50–200 ms |
| Q_Star + Q_Delta eşzamanlı | Faz-faz kısa devre | Yazılım + donanım interlock (çift) |
| VFD reset CW her cycle | VFD reset döngüsünde kalır | R_TRIG ile tek-pulse reset |
| Tam durmadan reverse start | DC bus overvoltage trip, mekanik jerk | Yön/start için v < eşik onayı |
| Termik model akım=0 okuyor | Yazılım koruma kör; motor yanar | Donanım overload relay zorunlu |

### Sayısal Limitler ve Ölçekleme

```
ABB ACS355  : 20000 = %100 nominal hız
Danfoss FC302: 16384 = %100 (firmware'e göre 20000 olabilir!)
  ❌ rSpeedRef/rSpeedMax * 20000 → Danfoss'ta %122 fazla hız
  ✅ Ölçek faktörü GVL_Params'tan, üretici+firmware doğrulanmış

REAL_TO_WORD(>65535) : WORD overflow → düşük anlamsız değer
  ✅ LIMIT(0.0, x, 20000.0) çağrıdan önce zorunlu

Motor akımı register : ×0.1 A (üretici bağımlı; bazıları ×0.01)
  → ölçek faktörü yanlışsa termal model 10× hatalı

Soft starter start limiti : tiristör ısısı → saatte 6–10 start
  ✅ PLC'de start sayacı + soğuma timer ile sınırla
```

### Hata Senaryosu — Geri Bildirim ve Acil Stop Çakışması

FB_MotorDOL'da E-stop/overload kontrolü CASE'den **önce** her cycle çalışır ve `eState := eFault` set eder. Ancak `xRunFeedback` aux-contact gecikmesi (kontaktör fiziksel açılma süresi ~20–50 ms) nedeniyle, durduktan sonra `eStopping` durumunda geri bildirimin sıfırlanmasını beklerken kontaktör bounce'u false "feedback lost" üretebilir. Çözüm: feedback kaybı kararına da kısa bir onay gecikmesi (TON ~100 ms) eklenmeli — anlık spike değil, kalıcı koşul fault üretmeli. Bu, fail-safe ile gürültü reddi arasındaki dengeyi gösterir: güvenlik kararı hızlı olmalı (E-stop, RETURN ile) ama teşhis kararı gürültüye dayanıklı olmalı (debounce).

## Optimizasyon

### Modbus Trafiğini Ayrı Task'a İzole Etme

En kritik performans deseni (Hata 7, Not 3): Modbus okuma/yazma **asla** kontrol döngüsüyle aynı task'ta olmamalı. Modbus FB'leri I/O için bloklanır (TCP timeout 100+ ms, RTU char timeout); bu gecikme 10 ms kontrol döngüsünün watchdog'unu tetikleyebilir.

```
Task mimarisi (kaynak: codesys/task-structure/_synthesis.md):
  Task_Main 10 ms  Prio:2  → FB state machine, sadece GVL oku/yaz
  Task_Comm 100 ms Prio:5  → PRG_CommManager, Modbus FC03/FC16
  İki task arası köprü     → GVL_Modbus (single-writer: comm task yazar)
```

GVL_Modbus single-writer prensibi burada kritiktir: Status Word/Actual Speed'i **yalnızca** comm task yazar, kontrol task'ı yalnızca okur. Tersi olursa iki task aynı WORD'e yazıp veri yarışı (race) oluşturur.

### Write-on-Change ile Bus Yükünü Azaltma

| Strateji | Bus yükü | Risk |
|----------|----------|------|
| Her cycle full write | Yüksek | Düşük gecikme, hat doygunluğu |
| Write-on-change | Düşük | Comm-loss watchdog tetiklenmeyebilir |
| Change + periyodik refresh (1 s) | Orta | En dengeli — önerilen |

Çok sürücülü RS-485 hattında poll turu süresi = Σ(her slave yanıt süresi). Write-on-change ile gereksiz yazmalar elenince tur kısalır, her VFD'nin status tazeliği artar. Ancak run/stop komutu periyodik refresh edilmeli (Not 7 — comm-loss güvenliği).

### Termal Modeli FPU-Verimli Tutma

FB_ThermalProtection her cycle `(I/I_rated)²` hesaplar (REAL çarpma). Çok motorlu panoda (20+ motor) bu yük birikir. Optimizasyon: termal model 10 ms yerine 100 ms task'ta koşar — termal zaman sabiti (τ) dakikalar mertebesinde olduğundan 100 ms çözünürlük fazlasıyla yeterlidir. Bu, "pahalı işlemi yavaş task'a topla" kuralının motor korumadaki uygulamasıdır.

## Derin Teknik Detay

### Neden Control Word / Status Word? Doğrudan Bit I/O Değil mi?

VFD'ler durumu tek bir 16-bit register'da kodlar çünkü Modbus/fieldbus üzerinde her register transferi protokol overhead'i taşır (RTU'da CRC, adres, fonksiyon kodu). 16 ayrı coil yerine tek holding register okumak, tek bir FC03 ile tüm durumu atomik olarak alır — bu **atomiklik** kritiktir: "running" ve "fault" bitlerini ayrı transferlerde okusaydık, ikisi arasında VFD durumu değişebilir ve tutarsız anlık görüntü (torn read) oluşurdu. Tek register = tek tutarlı snapshot. PLC tarafında bit maskeleme (`AND SW_RUNNING`) bu yüzden register okunduktan sonra yapılır, hat üzerinde değil. Bu tasarım, GVL'de tek WORD'ün single-writer kuralıyla korunmasının neden doğal olduğunu da açıklar: register zaten atomik bir bütündür.

### V/Hz vs Vektör Kontrol — PLC Programcısı Neden Bilmeli?

VFD motor frekansını ayarlarken iki temel kontrol modu vardır ve bu, PLC'nin gördüğü davranışı değiştirir:

| Mod | Prensip | Düşük hızda tork | PLC etkisi |
|-----|---------|------------------|------------|
| **Skaler (V/Hz)** | Voltaj/frekans oranı sabit | Zayıf (<5 Hz) | Hız ref basit; konveyör start'ta tork yetersiz olabilir |
| **Vektör (sensorless)** | Akı + tork ayrı kontrol | Güçlü | Tam yük start mümkün; ama parametre tuning gerekir |
| **Closed-loop (encoder)** | Enkoder geri besleme | Mükemmel | PLC pozisyon/hız senkronizasyonu yapabilir |

PLC'den gelen hız referansı aynı olsa bile, V/Hz modunda düşük hızda yüklü konveyör hiç hareket etmeyebilir (motor "stall"). FB_MotorDOL'un start timeout fault'u bu durumda tetiklenir ve programcı "kod hatası" sanır — gerçekte VFD kontrol modu yanlıştır. Bu yüzden FB tasarımı VFD parametrelerinden bağımsız değildir; ikisi birlikte devreye alınır.

### IEC 61131-3 FB Instance Belleği ve VFD State Machine

FB_VFD_Modbus'un `eState` değişkeni, FB instance'ının statik belleğinde durur (her instance ayrı VFD = ayrı bellek). Bu, OOP'deki nesne durumuna benzer ama kritik fark: CODESYS'te FB çağrı sırası, kullanıcının kod yazma sırasıyla belirlenir ve cycle başına **bir kez** çalışması garanti edilir (koşullu çağrı dışında). VFD state machine'in `eVFD_Enabling → eVFD_Running` geçişi bu yüzden her cycle "running bit geldi mi?" diye yoklayabilir — durum cycle'lar arası korunur. Eğer FB her cycle çağrılmazsa (Hata: koşullu çağrı), `tCommWatchdog` saymayı durdurur ve comm-loss algılaması saatlerce gecikebilir. Determinizmin güvenlikle birleştiği nokta budur: watchdog'un güvenilirliği, FB'nin deterministik (koşulsuz, her cycle) çağrılmasına bağlıdır.

---

## İlgili Konular

```
knowledge/codesys/fundamentals/
└── 02_project_structure.md     → FB_Motor state machine, GVL, DUT tanımları

knowledge/codesys/programming/
└── 03_function_blocks.md       → FB tasarım prensipleri, state machine, interlock

knowledge/protocols/modbus-tcp/
└── _synthesis.md               → Modbus TCP register modeli, FC03/16, CODESYS slave

knowledge/applications/
└── conveyor/                   → Motor kontrol + konveyör sekans mantığı birlikte

knowledge/hardware/
└── vfd/                        → Sürücü seçimi, montaj, EMC filtreleme

knowledge/standards/
└── iec60034/                   → Motor standardları, verimlilik sınıfları (IE1-IE4)
└── iec60204-1/                 → Makine elektrik donanımı — motor koruma zorunlulukları
```
