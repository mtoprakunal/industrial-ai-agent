---
KONU        : CODESYS Programlama Mimarisi — Sentez
KATEGORİ    : codesys
ALT_KATEGORI: programming
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "knowledge/codesys/programming/01_pou_types.md"
    başlık: "CODESYS POU Tipleri — Program, Function Block, Function"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/02_gvl_design.md"
    başlık: "CODESYS GVL Tasarımı"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/03_function_blocks.md"
    başlık: "İyi Bir Function Block Nasıl Yazılır"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/04_libraries.md"
    başlık: "CODESYS Kütüphane Sistemi"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/05_error_handling.md"
    başlık: "CODESYS'te Hata Yönetimi"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_pou_types.md"
    ilişki: detaylandırır
  - konu: "02_gvl_design.md"
    ilişki: detaylandırır
  - konu: "03_function_blocks.md"
    ilişki: detaylandırır
  - konu: "04_libraries.md"
    ilişki: detaylandırır
  - konu: "05_error_handling.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "CODESYS temeller sentezi (fundamentals/_synthesis.md)"
  - "IEC 61131-3 ST dili temelleri"
  - "Task ve project structure kavramları"
ÇELİŞKİLER :
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez belgesi yeni çelişki içermez; kaynak belgelere atıflar yapar."
---

## Özün Ne

Bu sentez, beş programlama belgesini okuyunca edinilmesi gereken bütünsel mimari anlayışı özetler: CODESYS'te iyi bir proje, birbirini tamamlayan beş kararın ürünüdür. Hangi POU tipi, nasıl bir GVL yapısı, nasıl tasarlanmış Function Block'lar, kütüphane yönetimi ve hata stratejisi — bu beş karar birlikte doğru alındığında proje bakımı kolaylaşır, hata analizi hızlanır ve aynı kod onlarca projede yeniden kullanılabilir hale gelir. Tek bir karar yanlış alındığında — örneğin her şeyi PROGRAM'a yazmak ya da tüm değişkenleri tek GVL'ye koymak — tüm mimar çökme noktasına ilerler.

## Nasıl Çalışır

### Beş Belgenin Zihin Haritası

```
┌────────────────────────────────────────────────────────────────────────────┐
│              CODESYS PROGRAMLAMA MİMARİSİ — ZİHİN HARİTASI                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  01_pou_types.md                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  POU TİPLERİ — Kodun temel yapı taşları                             │    │
│  │                                                                       │    │
│  │  PROGRAM ──────── Singleton, task orkestratörü (PRG_Control)         │    │
│  │  FUNCTION_BLOCK── Çoklu instance, cihaz yaşam döngüsü (FB_Motor)    │    │
│  │  FUNCTION ──────── Durumsuz, saf hesaplama (FC_ScaleAnalog)          │    │
│  └──────────────────────────┬────────────────────────────────────────────┘  │
│                              │ POU'lar veri için GVL'ye başvurur            │
│                              ▼                                               │
│  02_gvl_design.md                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  GVL TASARIMI — POU'lar arası veri akışının omurgası                │    │
│  │                                                                       │    │
│  │  GVL_IO       ← Fiziksel I/O sinyalleri (AT %I/%Q)                  │    │
│  │  GVL_HMI      ← Operatör komutları (HMI yazar)                      │    │
│  │  GVL_Params   ← Proses parametreleri (ayarlanabilir)                 │    │
│  │  GVL_Alarms   ← Alarm ve uyarı bayrakları                            │    │
│  │  GVL_Config   ← PERSISTENT kalibrasyon verisi                        │    │
│  └──────────────────────────┬────────────────────────────────────────────┘  │
│                              │ FB'ler GVL'yi okur, çıkışlarını PROGRAM      │
│                              │ aracılığıyla GVL'ye yazar                    │
│                              ▼                                               │
│  03_function_blocks.md                                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  FUNCTION BLOCK TASARIMI — Cihaz mantığının kapsüllenmesi           │    │
│  │                                                                       │    │
│  │  VAR_INPUT  → Komutlar + konfigürasyon                               │    │
│  │  VAR_OUTPUT → Durum + hata raporlama                                  │    │
│  │  VAR_IN_OUT → Büyük struct referansı (kopyasız)                      │    │
│  │  CASE eState → State machine: Idle→Starting→Running→Fault            │    │
│  │  ELSE: → Bilinmeyen durum → eFault (savunmacı programlama)           │    │
│  └──────────────────────────┬────────────────────────────────────────────┘  │
│                              │ Olgun FB'ler kütüphaneye alınır              │
│                              ▼                                               │
│  04_libraries.md                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  KÜTÜPHANE SİSTEMİ — Tekrar kullanımın altyapısı                    │    │
│  │                                                                       │    │
│  │  Standard.lib → TON, CTU, R_TRIG, SR (her projede)                  │    │
│  │  Util.lib     → FIFO, string, istatistik                             │    │
│  │  CAA_File     → Dosya sistemi / log                                   │    │
│  │  MyMachineLib → Kendi FB'lerin (sabit versiyon!)                     │    │
│  └──────────────────────────┬────────────────────────────────────────────┘  │
│                              │ FB'ler hata durumunu raporlar;               │
│                              │ proje alarm mimarisini besler                │
│                              ▼                                               │
│  05_error_handling.md                                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  HATA YÖNETİMİ — Dört katmanlı güvenlik ağı                         │    │
│  │                                                                       │    │
│  │  Katman 1: Task Watchdog (runtime koruması)                          │    │
│  │  Katman 2: __TRY/__CATCH (yalnızca 32-bit, pointer güvenliği)        │    │
│  │  Katman 3: FB içi savunmacı programlama (giriş doğrulama)            │    │
│  │  Katman 4: Alarm yönetimi + operatör bilgilendirme                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────────┘
```

### Bütünsel Mental Model — Bir CODESYS Projesi Nasıl Nefes Alır?

CODESYS programlama mimarisini anlamanın en kısa yolu şu akışa bakmaktır:

> **Fiziksel dünya → GVL_IO** (AT % eşlemeli sinyaller)  
> **GVL_IO → FB_Motor/FB_Valve** (Function Block'lar fiziksel sinyali okur)  
> **FB_Motor → PROGRAM** (PROGRAM, FB'yi çağırır ve çıkışları GVL'ye yazar)  
> **PROGRAM → GVL_IO** (çıkış komutları fiziksel dünyaya döner)  
> **Herhangi bir adımda hata → GVL_Alarms** (alarm mimarisi tüm katmanları izler)  
> **Olgun FB'ler → Kütüphane** (bir sonraki projede sıfırdan başlanmaz)

Bu akış tek yönlüdür ve her adımın sorumluluğu nettir. Karışıklık, bu akışın dışına çıkıldığında başlar: FB'nin GVL'ye doğrudan yazması, PROGRAM'ın birden fazla yerden çağrılması, GVL_IO'ya iş mantığı değişkeni eklenmesi — her biri bu temiz akışı kırar.

## Hızlı Referans Tabloları

### A. POU Türü Seçim Tablosu (Belge 1)

| Soru | Cevap | POU Türü |
|---|---|---|
| Birden fazla kopyaya ihtiyaç var mı? | Evet | **FUNCTION_BLOCK** |
| Task tarafından doğrudan çağrılacak mı? | Evet, tek kopya | **PROGRAM** |
| Durum/hafıza tutuluyor mu? | Hayır | **FUNCTION** |
| Timer veya sayaç kullanıyor mu? | Evet | **FUNCTION_BLOCK** |
| OOP, interface, inheritance gerekiyor mu? | Evet | **FUNCTION_BLOCK** |
| Saf dönüşüm / hesaplama | Evet | **FUNCTION** |

Pratik dağılım — orta büyüklükte bir projede:
```
PROGRAM        → 3-5 adet (task başına bir, orkestrasyon)
FUNCTION_BLOCK → 10-50 adet, çoklu instance (cihaz başına bir tip)
FUNCTION       → 5-20 adet (ölçekleme, dönüşüm, limit kontrol)
```

### B. GVL Tasarım Kuralları (Belge 2)

| GVL Adı | İçerik | Kim Yazar | Kalıcılık |
|---|---|---|---|
| GVL_IO | AT % eşlemeli fiziksel sinyaller | Task_Control | Standart |
| GVL_HMI | HMI komutları, ekran değerleri | Task_HMI | Standart |
| GVL_Params | Proses parametreleri | Task_HMI (operatör) | Standart / RETAIN |
| GVL_Alarms | Alarm ve uyarı bayrakları | Task_Control, Task_Safety | Standart |
| GVL_Recipes | Reçete verileri | Task_HMI | **RETAIN** |
| GVL_Config | Makine kimliği, kalibrasyon | Mühendis (sadece) | **PERSISTENT** |
| GVL_Comm | Haberleşme ara değişkenleri | Task_Comm | Standart |

**Altın kural:** Bir değişken birden fazla POU tarafından paylaşılmıyorsa GVL'ye koyma. Bir GVL'ye yalnızca tek bir task yazar; diğerleri okur.

### C. Function Block Tasarım Desenleri (Belge 3)

| Desen | Ne Zaman | Nasıl |
|---|---|---|
| Standart cihaz FB'si | Motor, vana, sensör | VAR_INPUT + VAR_OUTPUT + CASE eState |
| Savunmacı giriş doğrulama | Tüm FB'lerde | RETURN ile erken çıkış, hata kodu set et |
| VAR_IN_OUT struct geçirme | Büyük struct (>50 byte) | Kopyalama yerine referans — CPU tasarrufu |
| Array of FB | Aynı cihazdan N adet | ARRAY[1..N] OF FB_Motor + FOR döngüsü |
| State machine ELSE | Her CASE içinde | ELSE: eState := eFault — bilinmeyen durum koruması |

**FB arayüz standardı** — her FB'de olması gereken minimum çıkışlar:
```
xFault      : BOOL      ← Hata var mı
eFaultCode  : DWORD     ← Makine okunabilir hata kodu
sFaultMsg   : STRING(80)← İnsan okunabilir mesaj
eState      : E_...State← Mevcut durum (HMI/diagnostik)
```

### D. Kütüphane Seçim ve Versiyon Kuralları (Belge 4)

| Kütüphane | İçerik | Her Projede? |
|---|---|---|
| Standard.library | TON, CTU, R_TRIG, SR, SEL, LIMIT | **Evet, otomatik** |
| Util.library | FIFO, string fonksiyonları, istatistik | Gerektiğinde |
| CAA_File | Dosya okuma/yazma | Log gereken projelerde |
| CAA_SerialCom | RS-232/485 seri port | Seri haberleşme |
| OSCAT Basic | Açık kaynak endüstriyel bloklar | PID, filtre alternatifi |
| MyMachineLib | Kendi geliştirdiğin FB'ler | 3+ projede aynı FB kullanılıyorsa |

**Versiyon kural:** Üretim projesinde `*` (newest) asla kullanma. Her kütüphane sabit versiyonla kilitlenmeli: `Standard, 3.5.17.0`.

### E. Hata Yönetimi Stratejileri (Belge 5)

| Katman | Mekanizma | Platform | Zorunlu mu? |
|---|---|---|---|
| Runtime koruması | Task Watchdog (Cycle × 3-5) | Tüm | **Her task'ta zorunlu** |
| İstisna yakalama | `__TRY/__CATCH` | Yalnızca 32-bit | Pointer işlemlerinde |
| Pointer koruması | `IF pData <> 0 THEN` | Tüm (özellikle 64-bit) | 64-bit'te zorunlu |
| FB içi doğrulama | Giriş sınır kontrolü, RETURN | Tüm | Her FB'de |
| Operatör bildirimi | FB_AlarmManager + ST_AlarmRecord | Tüm | Her üretim projesinde |
| Güvenli durum | Ayrı Task_Safety (Prio:0) | Tüm | Kritik çıkışlar için |

**Watchdog ayarı:** `Watchdog Time = Cycle Time × 3..5`. Sensitivity: 3 ardışık ihlalde tetikle.

### F. İsimlendirme Özeti (Belgeler 1-2)

```
Tip Prefiksleri:
  x=BOOL   n=INT/UINT   w=WORD   dw=DWORD   r=REAL
  s=STRING  t=TIME   dt=DATE_AND_TIME   a=ARRAY   st=STRUCT   e=ENUM

GVL Kaynak Prefiksleri (qualified_only zorunlu):
  GVL_IO.x    → Fiziksel I/O
  GVL_HMI.x   → HMI komutu
  GVL_Params.r → Proses parametresi
  GVL_Alarms.x → Alarm bayrağı

Yön Postfiksleri:
  ...Cmd      → Komut (yazılır)
  ...Feedback → Geri bildirim (okunur)
  ...Setpoint → Hedef değer
  ..._C / ..._Bar / ..._Pct → Birim
```

## Pratikte Nasıl Kullanılır

### Yeni Bir Makine Projesi İçin Kontrol Listesi

```
PROJE BAŞLANGIÇ MİMARİ KARARLARI
─────────────────────────────────────────────────────────
□ 1. Kaç farklı cihaz türü var? → Her cihaz türü için bir FB
□ 2. GVL ayrımını yap: IO, HMI, Params, Alarms, Config, Comm
□ 3. Hangi task'lar var? → Task başına bir PROGRAM
□ 4. RETAIN neler? → Üretim sayaçları, reçete aktif verisi
□ 5. PERSISTENT neler? → Kalibrasyon, makine kimliği, lifetime sayaç
□ 6. Watchdog her task'ta AÇIK — cycle × 3, sensitivity 3
□ 7. qualified_only her GVL'de AÇIK

KODLAMA AKIŞI
─────────────────────────────────────────────────────────
□ 8.  DUT: Enum (E_MotorState) + Struct (ST_MotorDiag, ST_AlarmRecord) tanımla
□ 9.  FB_Motor, FB_Valve, FB_AnalogSensor yaz (state machine, hata çıkışları)
□ 10. GVL_IO — AT % eşlemeleri (fiziksel sinyaller)
□ 11. GVL_HMI, GVL_Params, GVL_Alarms tanımla
□ 12. PRG_Control: FB'leri çağır → çıkışları GVL_IO'ya yaz → alarmları GVL_Alarms'a aktar
□ 13. PRG_Safety: xAnyCriticalAlarm → tüm kritik çıkışları kapat
□ 14. FB_AlarmManager instance'larını PRG_Control içinde çağır
□ 15. Build → Download → Test

KÜTÜPHANELEŞTİRME KARAR NOKTASI
─────────────────────────────────────────────────────────
□ 16. Bu FB 3+ projede kullanılacak mı? → Library projesi oluştur
□ 17. Kütüphane versiyonu sabitle, Project Archive ile dağıt
```

### Beş Belgeyi Bağlayan Pratik Senaryo

**Görev:** 2 konveyör motoru + 1 ısıtıcı + sıcaklık sensörü olan bir proses hattı.

```
ADIM 1 — POU Türü Kararı (Belge 1)
  FB_Motor         ← 2 instance (fbMotor1, fbMotor2)
  FB_TemperatureCtrl ← 1 instance, PID içerir
  FB_AnalogSensor  ← 1 instance (sıcaklık sensörü)
  FC_ScaleAnalog   ← Saf dönüşüm fonksiyonu
  PRG_ProcessControl ← Task_Control tarafından çağrılır (tek kopya)
  PRG_Safety       ← Task_Safety tarafından (Prio:0, 1ms)

ADIM 2 — GVL Yapısı (Belge 2)
  GVL_IO
    xConv1_RunFB    AT %I0.0 : BOOL;   (* Motor 1 geri bildirim *)
    xConv2_RunFB    AT %I0.1 : BOOL;
    wTemp_ADC       AT %IW0  : WORD;   (* Sıcaklık ADC *)
    xConv1_Out      AT %Q0.0 : BOOL;
    xConv2_Out      AT %Q0.1 : BOOL;
    xHeater_Out     AT %Q0.2 : BOOL;
  GVL_Params
    rTemp_Setpoint_C   : REAL := 75.0;
    rConv_MaxSpeed_Pct : REAL := 80.0;
  GVL_Alarms
    xAlarm_Conv1_Fault : BOOL;
    xAlarm_Temp_High   : BOOL;
    xAnyCriticalAlarm  : BOOL;
  GVL_Config PERSISTENT
    rTemp_CalOffset : REAL := 0.0;   (* Kalibrasyon — download'a dayanır *)

ADIM 3 — Function Block Tasarımı (Belge 3)
  FB_Motor:
    VAR_INPUT: xStartCmd, xStopCmd, xFaultReset, tStartDelay
    VAR_OUTPUT: xRunOutput, xFault, eState, sFaultMsg
    CASE eState: eIdle → eStarting → eRunning → eStopping / eFault
    ELSE: eState := eFault; xRunOutput := FALSE;

ADIM 4 — Kütüphane Kullanımı (Belge 4)
  Standard.library: TON (tStartTimer), R_TRIG (fault reset), CTU (üretim sayacı)
  MyMachineLib 1.2.0.0: FB_Motor, FB_AnalogSensor (sabit versiyon!)

ADIM 5 — Hata Yönetimi (Belge 5)
  Task_Control watchdog: 30ms cycle × 3 = 90ms, sensitivity 3
  Task_Safety  watchdog: 1ms cycle × 5 = 5ms, sensitivity 3

  PRG_ProcessControl içinde:
    fbMotor1(xStartCmd := GVL_HMI.xConv1_Start, ...);
    GVL_IO.xConv1_Out      := fbMotor1.xRunOutput;
    GVL_Alarms.xAlarm_Conv1_Fault := fbMotor1.xFault;

  PRG_Safety içinde:
    IF GVL_Alarms.xAnyCriticalAlarm THEN
        GVL_IO.xConv1_Out  := FALSE;
        GVL_IO.xConv2_Out  := FALSE;
        GVL_IO.xHeater_Out := FALSE;
    END_IF

  GVL_Alarms.xAnyCriticalAlarm :=
      GVL_Alarms.xAlarm_Conv1_Fault OR
      GVL_Alarms.xAlarm_Temp_High;
```

## Sık Yapılan Hatalar

### Hata 1: Her Şeyi PROGRAM'a Yazmak (Belge 1)

4 motor için `PRG_Motor1..4` oluşturmak. Bir hata düzeltmesi 4 dosyayı aynı anda değiştirmek demektir. Çözüm: Tek `FB_Motor` tanımı, 4 instance — bir değişiklik her yere yansır.

### Hata 2: Tek Büyük GVL Anti-Pattern'i (Belge 2)

500 değişkeni tek GVL'ye yığmak. "xRun kim yazar? rSetpoint RETAIN mı? xAlarm nereden geliyor?" soruları yanıtsız kalır. Çözüm: Her GVL'nin tek, net sorumluluğu — GVL_IO yalnızca fiziksel sinyal, GVL_Alarms yalnızca alarm.

### Hata 3: Function'a Timer Koymak (Belge 1)

`FC_DelayedOutput` içinde `TON` kullanmak. Timer her çağrıda sıfırlanır, çıkış asla gelmez. Durum tutan her yapı → Function Block.

### Hata 4: FB'nin Global'e Doğrudan Yazması (Belge 3)

FB içinden `GVL_IO.xMotorOut := TRUE` yazmak. 5 instance aynı değişkeni ezer. Çözüm: FB yalnızca `VAR_OUTPUT`'a yazar; atamayı çağıran PROGRAM yapar.

### Hata 5: Watchdog Kapalı Üretim Projesi (Belge 5)

Geliştirme kolaylığı için watchdog kapalı bırakılırsa bir sonsuz döngü runtime'ı dondurur, motorlar son komutlarında kilitlenir. Her task'ta watchdog zorunludur.

### Hata 6: Kalibrasyon Datasını RETAIN ile Saklamak (Belge 2)

RETAIN verisi program download'unda sıfırlanır. Kalibrasyon RETAIN'e konursa yeni firmware yüklendiğinde saha kalibrasyonu kaybolur. Kural: kalibrasyon = PERSISTENT, üretim sayacı = RETAIN.

### Hata 7: "Use Newest Version" Kütüphanesi (Belge 4)

Kütüphane versiyonu `*` bırakılırsa üçüncü taraf güncelleme beklenmedik davranış değişikliği getirir. Üretim projelerinde her kütüphane sabit versiyon ile kilitlenmeli.

### Hata 8: State Machine'de ELSE Kullanmamak (Belge 3)

RETAIN bozulursa `eState` tanımlanmamış değer alabilir. ELSE yoksa çıkış belirsiz — makine beklenmedik biçimde hareket eder. Her CASE: `ELSE: eState := eFault; xRunOutput := FALSE;`

### Hata 9: FB'yi Koşullu Çağırmak (Belge 3)

```iecst
(* YANLIŞ: *)
IF xEnable THEN fbMotor1(xStartCmd := ...); END_IF
(* xEnable = FALSE iken TON/CTU içindeki timerlar ve sayaçlar donar. *)

(* DOĞRU: *)
fbMotor1(xStartCmd := ..., bEnabled := xEnable);
```

### Hata 10: Çıkışı Çağrıdan Önce Okumak (Belge 3)

Önce `xRunning := fbMotor1.xRunning` okunursa önceki döngünün değeri alınır. Doğru sıra: önce çağır (`fbMotor1(...)`), sonra çıkışı oku.

## Ne Zaman ...

### Ne Zaman Kütüphane Oluşturulur?

Aynı FB 3 veya daha fazla projede kullanılıyorsa. Farklı müşterilere dağıtılacaksa. IP koruma gerekliyse → compiled-library. Küçük prototip ya da tek projeye özgüyse kütüphane gerekmez, proje içinde bırakılabilir.

### Ne Zaman PROGRAM Yerine FUNCTION_BLOCK Yazılır?

Kod birden fazla kopyalanacaksa her zaman FUNCTION_BLOCK. Cihazın (motor, vana, sensör) yaşam döngüsü yönetiliyorsa her zaman FUNCTION_BLOCK. Task'tan doğrudan çağrılan ve kopyalanmayacak orkestrasyon kodu → PROGRAM.

### Ne Zaman `__TRY/__CATCH` Kullanılır?

Yalnızca 32-bit platformda, pointer manipülasyonu veya external kütüphane çağrısı içeren kodda. 64-bit x64 sistemlerde `__TRY/__CATCH` desteklenmez — savunmacı programlama (null kontrolü, index sınır kontrolü) zorunludur.

### Ne Zaman PERSISTENT Kullanılır?

Veri hem güç kesilmesine hem de program download'una karşı korunmalıysa. Kalibrasyon, makine serial numarası, ömür boyu üretim sayacı, son bakım tarihi — bunların tamamı PERSISTENT. Yalnızca güç kesilmesine karşı korunması yeterli veriler (shift sayacı, aktif reçete) → RETAIN.

### Ne Zaman Ayrı Task_Safety Oluşturulur?

Kritik çıkışlar (motor, ısıtıcı, vana) başka bir task'ın watchdog hatasından etkilenmemeli ise her zaman. Task_Safety en yüksek öncelikte (Prio:0), en kısa döngü süresiyle (1ms), bağımsız watchdog ile çalışır ve yalnızca güvenli duruma geçiş mantığını yürütür.

## Gerçek Proje Notları

**Not 1 — Beş Belgenin Birikimli Değeri**  
Her belge tek başına değerlidir; ancak beşi birlikte uygulandığında etki çok daha büyük olur. PROGRAM → FB ayrımı kopyalamayı ortadan kaldırır, GVL ayrımı race condition'ı önler, FB tasarım prensipleri test edilebilirliği sağlar, kütüphane sistemi projeye taşır, hata yönetimi sahada 8 saatlik debug oturumunu tek saate indirir. Birini ihmal etmek zincirin en zayıf halkasını oluşturur.

**Not 2 — FB_Motor'un 50 Projede Yolculuğu**  
İyi tasarlanmış bir `FB_Motor` — temiz arayüz, state machine, hata çıkışları — bir kez yazılır ve onlarca projede parametresiyle uyarlanır. `tStartDelay := T#2S` ile birinde, `tStartDelay := T#5S` ile diğerinde. Arayüz aynı, davranış öngörülebilir, test kümesi paylaşılıyor. Kötü tasarlanmış bir FB ise her projede kopyalanır, her kopyada bir fark oluşur, yıllar içinde 20 farklı "FB_Motor" versiyonu ortaya çıkar — hangisinin doğru olduğu kimse tarafından bilinmez.

**Not 3 — GVL Kategorisizliğinin Maliyeti**  
600 satırlık tek bir GVL'de `xRun`, `xStop`, `xAlarm` gibi belirsiz isimler: Hangi motorun, hangi ünitenin? Komut mu geri bildirim mi? RETAIN mi değil mi? 3 gün analiz, 6 GVL'ye bölme, %60 bakım süresi azalması. Proje başında yapılan 2 saatlik GVL tasarımı, ilerleyen aylarda haftalar kurtarır.

**Not 4 — Kalibrasyon Kaybının Üretim Maliyeti**  
RETAIN'de saklanan kalibrasyon verisi, bug fix download'unda sıfırlandı. Dolum makinesi 2 saat yanlış miktarda doldurdu, üretim partisi iptal edildi. PERSISTENT eklenmesi 5 dakikalık bir değişiklikti — erteleme maliyeti üretim partisine mal oldu.

**Not 5 — 64-bit Platformun __TRY/__CATCH Tuzağı**  
Müşteri x64 IPC istedi. `__TRY/__CATCH` kullanan tüm bölümler derlendi ama çalışmadı — 64-bit CODESYS runtime bu özelliği desteklemez. Kodu yeniden yazmak: her pointer erişiminde null kontrolü, her dizi erişiminde index sınır kontrolü. Daha fazla satır, ama platforma taşınabilir ve gerçekten güvenli.

**Not 6 — Alarm Mesajı Kalitesinin Saha Etkisi**  
"Motor arızası" mesajıyla 8 saat süren arıza araştırması yaşandı. "Motor 1 çalışma geri bildirimi 50ms içinde gelmedi — Kontaktör K1 veya kablo J14'ü kontrol edin" mesajıyla aynı arıza 45 dakikada çözüldü. İyi alarm mesajı yazmak zaman alan bir disiplindir; saha maliyetini doğrudan etkiler.

## İlgili Konular

```
knowledge/codesys/programming/      ← Şu an buradasınız
├── 01_pou_types.md
├── 02_gvl_design.md
├── 03_function_blocks.md
├── 04_libraries.md
├── 05_error_handling.md
└── _synthesis.md (bu belge)

Önkoşul — Temel Seviye:
knowledge/codesys/fundamentals/
├── 01_runtime_architecture.md
├── 02_project_structure.md
├── 03_iec61131_languages.md
└── _synthesis.md

Sonraki adım — Task Yapılandırması:
knowledge/codesys/task-structure/
├── 01_task_types.md
├── 02_cycle_time_design.md
└── 03_priority_management.md

Sonraki adım — İleri Seviye:
knowledge/codesys/advanced/
├── oop_codesys.md           → FB ile Interface, Inheritance, Polymorphism
├── unit_testing_codesys.md  → FB'yi test etmek
├── compiled_library_guide.md → IP koruma, compiled-library oluşturma
└── application_events.md    → excpt_watchdog sistem olayı işleyici

Protokol / Haberleşme:
knowledge/protocols/
├── opc-ua/
└── modbus/

knowledge/networking/
└── ethercat/

Standartlar:
knowledge/standards/
└── safety_plc.md            → SIL gereksinimi, güvenlik mimarisi
```
