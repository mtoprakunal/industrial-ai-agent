---
KONU        : CODESYS GVL Tasarımı
KATEGORİ    : codesys
ALT_KATEGORI: programming
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_defining_global_variables.html"
    başlık: "CODESYS Online Help — Declaring Global Variables"
    güvenilirlik: resmi
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/codesys-local-vs-global-variables-scope-advantages"
    başlık: "Industrial Monitor Direct — Local vs Global Variables in CODESYS"
    güvenilirlik: topluluk
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/codesys-retain-persistent-variables-data-block-alternative"
    başlık: "Industrial Monitor Direct — Persistent Data Storage in CODESYS"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Engineering/thread/587bd07ae4/"
    başlık: "CODESYS Forge — Global Variables ve qualified_only tartışması"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_pou_types.md"
    ilişki: gerektirir
  - konu: "03_function_blocks.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/fundamentals/02_project_structure.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/task-structure/03_priority_management.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "CODESYS POU tipleri (01_pou_types.md)"
  - "VAR, VAR_GLOBAL, RETAIN, PERSISTENT anahtar kelimeleri"
ÇELİŞKİLER :
  - kaynak: "CODESYS V2.3 vs V3.5"
    konu: "V2'de GVL prefix gerekmiyordu (doğrudan isimle erişim); V3'te qualified_only varsayılan"
    çözüm: >
      V3'te GVL adı prefix olarak kullanılır: GVL_IO.xMotorRun.
      {attribute 'qualified_only'} pragma kaldırılırsa prefix olmadan erişmek
      mümkün olur; ancak aynı isimde farklı GVL'ler varsa çakışma hatası verir.
      Büyük projelerde prefix zorunlu tutmak (qualified_only) daha güvenlidir.
  - kaynak: "Bazı CODESYS türev platformları (WAGO, Beckhoff)"
    konu: "GVL isimlerinin ve erişim biçiminin platforma göre farklılık göstermesi"
    çözüm: >
      GVL mantığı standart; ancak bazı platformlar kendi convention'larını dayatabilir.
      Proje başında hedef platform convention'ı kontrol edilmelidir.
---

## Özün Ne

Global Variable List (GVL), tüm uygulama içinden erişilebilen değişkenlerin tanımlandığı dosyadır. GVL olmadan farklı POU'lar arasında veri paylaşımı mümkün değildir; ancak kötü tasarlanmış bir GVL, projeyi zamanla yönetilemez hale getirir. "Tek büyük GVL" anti-pattern'i — 500 değişkenin tek dosyaya yığılması — bakım süresini 3-5 katına çıkarır, race condition riskini artırır ve yeni geliştiriciyi projeye dahil etmeyi zorlaştırır. GVL tasarımı, kodun kalitesi kadar projenin uzun vadeli sağlığını belirler.

## Nasıl Çalışır

### GVL'nin Teknik Temeli

```iecst
(* GVL'nin içi — değişken bildirim biçimi *)
VAR_GLOBAL
    (* Standart global değişken — program süresi boyunca yaşar *)
    xMotorRun : BOOL;

    (* RETAIN — Güç kesilse de değeri korur (warm restart sonrası) *)
    dwProductionCount : DWORD;
    rLastSetpoint     : REAL;
    {attribute 'retain'}

    (* PERSISTENT — Download + güç kesilmesinde bile korunur *)
    {attribute 'persistent'}
    stMachineCalibration : ST_CalibrationData;
END_VAR
```

**Değişken Kalıcılık Seviyeleri:**

| Tür | Güç Kesilmesi | Program Download | Açıklama |
|---|---|---|---|
| Standart VAR_GLOBAL | Sıfırlanır | Sıfırlanır | Geçici çalışma verisi |
| RETAIN | Korunur | Sıfırlanır | Sayaçlar, zaman bilgisi |
| PERSISTENT | Korunur | Korunur | Kalibrasyon, parametre |

### qualified_only Attribute

CODESYS V3'te GVL'ler varsayılan olarak `{attribute 'qualified_only'}` ile gelir. Bu, değişkene `GVL_IO.xMotorRun` biçiminde prefix ile erişilmesi zorunluluğunu getirir.

```iecst
(* GVL_IO dosyasının başında *)
{attribute 'qualified_only'}
VAR_GLOBAL
    xMotorRun : BOOL;
END_VAR

(* ✅ Doğru erişim: *)
IF GVL_IO.xMotorRun THEN ...

(* ❌ Hatalı (qualified_only ile): *)
IF xMotorRun THEN ...  (* Derleme hatası *)
```

Prefix zorunluluğunun avantajı: Hangi değişkenin hangi GVL'den geldiği açıkça belli olur; isim çakışması riski ortadan kalkar.

---

### GVL Gruplama Stratejisi

Her GVL'nin tek, net bir sorumluluğu olmalıdır. Önerilen ayrım:

```
Application
├── GVL_IO           → Fiziksel I/O sinyalleri (AT %I, %Q eşlemeleri)
├── GVL_HMI          → HMI'a özel değişkenler (operatör komutları, ekran değerleri)
├── GVL_Params       → Proses parametreleri (operatör değiştirebilir)
├── GVL_Alarms       → Alarm ve uyarı bayrakları
├── GVL_Diagnostics  → Teşhis, sayaç, istatistik
├── GVL_Recipes      → Reçete verileri (RETAIN)
├── GVL_Config       → Makine konfigürasyonu (PERSISTENT)
└── GVL_Comm         → Haberleşme ara değişkenleri (OPC UA, Modbus)
```

Bu ayrım birkaç önemli faydayı beraberinde getirir:

**1. Erişim Kontrolü:** Saha personeli `GVL_Params`'ı değiştirebilir, `GVL_Config`'e dokunamaz.

**2. Race Condition Azaltma:** Her GVL'yi yalnızca belirli bir task yazar. `GVL_IO` → `Task_Control` yazar, `Task_HMI` yalnızca okur.

**3. Onboarding Kolaylığı:** Yeni geliştirici "Motor çıkışı nerede?" diye sormak yerine `GVL_IO` açar.

---

### Değişken İsimlendirme Kuralları

Tutarlı prefix sistemi, değişkenin tipini ve kapsamını kod okurken anında anlaşılır kılar.

**Tip Prefiksleri:**
```
Prefix | Tip           | Örnek
──────────────────────────────────────────────────
x      | BOOL          | xMotorRunFeedback
n      | INT / UINT    | nProductCount
w      | WORD          | wAnalogRawValue
dw     | DWORD         | dwTotalCycles
r      | REAL          | rTemperature_C
s      | STRING        | sRecipeName
t      | TIME          | tStartupDelay
dt     | DATE_AND_TIME | dtLastMaintenance
a      | ARRAY         | aTemperatureHistory
st     | STRUCT        | stMotorData
e      | ENUM          | eSystemState
i      | INT (eski)    | iCounter
b      | BOOL (eski)   | bRunning
```

**Kapsam / Kaynak Prefiksleri (GVL prefix'e ek):**
```
GVL_IO.x    → Fiziksel I/O (AT % eşlemeli)
GVL_HMI.x   → HMI'dan gelen komutlar
GVL_Params.r → Ayarlanabilir parametre
GVL_Alarms.x → Alarm bayrağı
```

**Yön / Birim Postfiksleri:**
```
...Cmd      → Komut (yazılır)
...Feedback → Geri bildirim (okunur)
...Setpoint → Hedef değer
..._C       → Celsius
..._Bar     → Bar cinsinden basınç
..._Pct     → Yüzde
```

**Tam örnek:**
```
GVL_IO.xConveyor1_RunFeedback   → Konveyör 1 çalışma geri bildirimi (BOOL, fiziksel giriş)
GVL_HMI.xConveyor1_StartCmd     → Operatörden başlatma komutu (BOOL, HMI yazıyor)
GVL_Params.rConveyor1_Speed_Pct → Hedef hız (REAL, yüzde, ayarlanabilir)
GVL_Alarms.xConveyor1_Fault     → Konveyör 1 arıza alarmı (BOOL)
```

## Pratikte Nasıl Kullanılır

### GVL_IO — I/O Eşleme Dosyası

```iecst
{attribute 'qualified_only'}
VAR_GLOBAL
    (* ======================== *)
    (* DİJİTAL GİRİŞLER        *)
    (* ======================== *)
    (* Konveyör 1 *)
    xConv1_RunFB    AT %I0.0 : BOOL; (* EtherCAT Slave 1, Ch.0 — Motor geri bildirim *)
    xConv1_FaultFB  AT %I0.1 : BOOL; (* EtherCAT Slave 1, Ch.1 — Motor arıza *)
    
    (* Güvenlik *)
    xEmergencyStop  AT %I1.0 : BOOL; (* Safety relay — E-stop zinciri *)
    xDoor1_Open     AT %I1.1 : BOOL; (* Kapı 1 güvenlik switch *)
    
    (* ======================== *)
    (* DİJİTAL ÇIKIŞLAR         *)
    (* ======================== *)
    xConv1_RunCmd   AT %Q0.0 : BOOL; (* EtherCAT Slave 1, Ch.0 — Motor çalıştır *)
    xAlarmLight     AT %Q1.0 : BOOL; (* Alarm lambası *)
    
    (* ======================== *)
    (* ANALOG GİRİŞLER          *)
    (* ======================== *)
    wTemp1_ADC      AT %IW0  : WORD; (* 0-4095 → 0-100°C *)
    wPressure1_ADC  AT %IW2  : WORD; (* 0-4095 → 0-10 bar *)
    
    (* ======================== *)
    (* ANALOG ÇIKIŞLAR          *)
    (* ======================== *)
    wConv1_Speed_AO AT %QW0  : WORD; (* 0-4095 → 0-50 Hz *)
END_VAR
```

### GVL_Params — Operatör Parametreleri

```iecst
{attribute 'qualified_only'}
VAR_GLOBAL
    (* Konveyör Parametreleri *)
    rConv1_MaxSpeed_Pct : REAL := 80.0;    (* % — varsayılan %80 *)
    rConv1_RampUp_s     : REAL := 5.0;     (* Saniye *)
    rConv1_RampDown_s   : REAL := 3.0;
    
    (* Sıcaklık Kontrol *)
    rTemp1_Setpoint_C   : REAL := 75.0;    (* °C *)
    rTemp1_Deadband_C   : REAL := 2.0;     (* ±°C *)
    rTemp1_MaxAlarm_C   : REAL := 90.0;    (* Alarm sınırı *)
    
    (* Üretim Hedefi *)
    dwDailyTarget       : DWORD := 5000;   (* Adet/gün *)
    tShiftDuration      : TIME := T#8H;
END_VAR
```

### GVL_Alarms — Alarm Yönetimi

```iecst
{attribute 'qualified_only'}
VAR_GLOBAL
    (* Aktif alarm bayrakları *)
    xAlarm_EmergencyStop    : BOOL;
    xAlarm_Conv1_Fault      : BOOL;
    xAlarm_Temp1_OverRange  : BOOL;
    xAlarm_Pressure_High    : BOOL;
    
    (* Uyarı bayrakları (alarm değil, izleme) *)
    xWarn_Conv1_SlowSpeed   : BOOL;
    xWarn_Temp1_NearLimit   : BOOL;
    
    (* Alarm özeti *)
    xAnyActiveAlarm         : BOOL;
    xAnyActiveWarning       : BOOL;
    dwActiveAlarmCount      : DWORD;
    
    (* Alarm geçmişi — son 10 alarm *)
    aAlarmHistory : ARRAY[1..10] OF ST_AlarmRecord;
    nAlarmHistoryIdx : INT := 1;
END_VAR
```

### GVL_Config — Kalıcı Makine Konfigürasyonu

```iecst
{attribute 'qualified_only'}
VAR_GLOBAL PERSISTENT
    (* Makine kimliği *)
    sMachineSerial    : STRING(20) := 'UNKN-0000';
    sMachineName      : STRING(40) := 'Default Machine';
    
    (* Kalibrasyon — Sahadaki ayarlar — download'dan korunur *)
    rTemp1_CalOffset  : REAL := 0.0;
    rTemp1_CalGain    : REAL := 1.0;
    
    (* Üretim istatistikleri *)
    dwTotalLifetimeCycles : DWORD;
    dtLastMaintenance     : DATE_AND_TIME;
END_VAR
```

## Örnekler

### Örnek 1: Kötü GVL vs İyi GVL Karşılaştırması

```iecst
(* ❌ KÖTÜ — Tek büyük GVL, her şey bir arada *)
VAR_GLOBAL
    xMotorRun        : BOOL;
    rSetpoint        : REAL;
    dwCount          : DWORD;
    xAlarm1          : BOOL;
    sRecipeName      : STRING;
    rCalibOffset     : REAL;
    xHMI_StartBtn    : BOOL;
    wADC_Raw         : WORD;
    (* ... 300 değişken daha ... *)
END_VAR
(* Sorular: rSetpoint kim yazar? xAlarm1'i kim tetikler? dwCount RETAIN mı? *)

(* ✅ İYİ — Her GVL'nin tek sorumluluğu var *)
(* GVL_IO: Fiziksel I/O eşlemeleri *)
(* GVL_Params: Operatör değiştirebilir proses parametreleri *)
(* GVL_Alarms: Yalnızca alarm bayrakları — Task_Control yazar, HMI okur *)
(* GVL_Config: PERSISTENT — download'a rağmen korunan kalibrasyon verileri *)
```

### Örnek 2: GVL_Recipes ile RETAIN Kullanımı

```iecst
{attribute 'qualified_only'}
VAR_GLOBAL RETAIN
    (* RETAIN: Güç kesilse de reçete kaybolmaz *)
    stActiveRecipe    : ST_Recipe;
    nActiveRecipeID   : INT := 0;
    bRecipeLoaded     : BOOL := FALSE;
    
    (* Reçete bankası — 10 reçete *)
    aRecipeBank : ARRAY[1..10] OF ST_Recipe;
END_VAR
(* Dikkat: RETAIN değişkenler download'da sıfırlanır. *)
(* Yeni program yüklenirken operatöre "Reçete kaydedildi mi?" uyarısı şarttır. *)
```

### Örnek 3: GVL Erişim Hiyerarşisi

```
Hangi POU hangi GVL'ye yazar / okur?

            GVL_IO  GVL_HMI  GVL_Params  GVL_Alarms  GVL_Config
Task_Control  YAZ     OKU      OKU         YAZ         OKU
Task_Safety   OKU     —        OKU         YAZ         —
Task_HMI      OKU     YAZ      YAZ*        OKU         OKU

* Task_HMI, GVL_Params'a operatör arayüzü üzerinden yazar.
  Ancak kritik parametrelerin şifre korumalı ekrandan yazılması önerilir.
```

## Sık Yapılan Hatalar

### Hata 1: Her Değişkeni Global Yapmak

```
Anti-pattern: "Lazım olur" diye her değişkeni GVL'ye koymak.

Sorun: FB_Motor içindeki timer ve durum değişkenleri GVL'de ne işi yapıyor?
       Race condition riski, gereksiz bellek tüketimi, proje karmaşası.

Kural: Bir değişken yalnızca birden fazla POU tarafından erişilmesi gerekiyorsa
       global olmalıdır. Aksi halde yerel (VAR) kalmalıdır.
```

### Hata 2: GVL_IO'ya Business Logic Değişkeni Koymak

```iecst
(* ❌ YANLIŞ *)
VAR_GLOBAL  (* GVL_IO içinde *)
    xMotorRun_FB AT %I0.0 : BOOL;   (* Fiziksel giriş — doğru *)
    xMotorIsRunning : BOOL;         (* Hesaplanmış durum — yanlış yer! *)
END_VAR

(* ✅ DOĞRU *)
(* GVL_IO: Yalnızca AT %I/%Q eşlemeli fiziksel sinyaller *)
(* xMotorIsRunning → FB_Motor'un VAR_OUTPUT ya da GVL_Diagnostics içinde *)
```

### Hata 3: RETAIN ile PERSISTENT'ı Karıştırmak

```
RETAIN    → Güç kesilmesine dayanır. Download'da SİFİRLANIR.
PERSISTENT → Her ikisine de dayanır.

Tuzak: Kalibrasyon datasını RETAIN ile tutmak.
       Yeni program download edildiğinde kalibrasyon sıfırlanır → saha felaketi.
Çözüm: Kalibrasyon ve makine kimliği → PERSISTENT
        Üretim sayaçları, shift verileri → RETAIN
        Çalışma süresi geçici verileri → Standart VAR_GLOBAL
```

### Hata 4: İsimlendirme Tutarsızlığı

```
❌ Karmaşık isimlendirme bir projedeki gerçek örnekler:
  Motor_Run_Feedback
  MotorRunFB
  xMtr_Running
  Run_Motor1
  bConveyor_is_running

✅ Tutarlı convention:
  xMotor1_RunFeedback
  xMotor2_RunFeedback
  xConveyor1_RunFeedback
  (prefix + nesne + özellik + yön — her zaman aynı biçim)
```

### Hata 5: qualified_only'yi Kaldırmak

```
Kısa vadeli rahatlık: GVL_IO.xMotorRun yerine sadece xMotorRun yazmak.
Uzun vadeli sorun: İki GVL'de aynı isim olursa derleyici hangi GVL'den
                   alacağını bilemez — belirsiz hata mesajları.

qualified_only'yi korumak: GVL adı, değişkenin nereden geldiğini
her okuyuşta açık eder. Büyük projelerde vazgeçilmez.
```

### Hata 6: Task'lar Arası GVL Yazma Çakışması

```iecst
(* ❌ YANLIŞ — iki farklı task aynı GVL değişkenine yazıyor *)
(* Task_Control: *)   GVL_Alarms.xMotorFault := fbMotor.xFaultOut;
(* Task_HMI: *)       GVL_Alarms.xMotorFault := FALSE;  (* Reset komutu *)

(* Sorun: Task preemption'da race condition. *)
(* ✅ DOĞRU: Task_Control yazar, Task_HMI sadece reset komutunu ayrı GVL'ye yazar *)
(* Task_Control: GVL_Alarms'a yazar *)
(* Task_HMI: GVL_HMI.xMotorFaultReset_Cmd := TRUE; (komut) *)
(* Task_Control: GVL_HMI.xMotorFaultReset_Cmd okur ve GVL_Alarms'ı günceller *)
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### GVL Ayrımı Kararları

**Ayrı GVL oluştur:**
- 30+ değişken bir kategoriye ait olmaya başladığında
- Farklı güvenlik/erişim seviyeleri ayrımı gerektiğinde
- RETAIN veya PERSISTENT ihtiyacı diğer değişkenlerden farklıysa
- Farklı task'ların farklı GVL'lere yazma hiyerarşisi tanımlanacaksa

**Tek GVL'de bırak:**
- 5'ten az değişken, net kategori yok
- Prototip veya çok küçük projeler

## Gerçek Proje Notları

**Not 1 — "Tek GVL Prensibi" Yıkıldığında**  
600 satırlık tek bir GVL'li proje devraldık. `xRun`, `xStop`, `xAlarm` gibi isimler. Hangi motorun, hangi ünitenin, hangisi komut hangi geri bildirim — hepsi belirsiz. 3 günlük analiz sonunda 6 GVL'ye bölündü. Bakım süresi %60 kısaldı.

**Not 2 — PERSISTENT'ın Değeri Sahadaki Bir Felakette**  
Kalibrasyon dataları RETAIN'de saklanıyordu. Bir bug fix için program download edildi — ve kalibrasyon sıfırlandı. Dolum makinesi 2 saat yanlış miktarda doldurdu, üretim partisi iptal edildi. Ders: Saha kalibrasyon verisi = PERSISTENT, tartışmasız.

**Not 3 — qualified_only Kaldırmanın Bedeli**  
Bir projede geliştirici konforu için `{attribute 'qualified_only'}` kaldırıldı. 6 ay sonra üçüncü taraf kütüphane entegre edildi. Kütüphanede de `xEnable` ve `xReady` vardı; projedeki `xEnable` ile çakıştı. 4 saat debug — `qualified_only` geri eklendi ve tüm kodda prefix güncellemesi yapıldı. Bir dahaki seferinde baştan konuldu.

**Not 4 — GVL_HMI'ın Koruyucu Rolü**  
Bir projede HMI doğrudan `GVL_Params`'a yazıyordu. Operatör yanlışlıkla bir değeri sıfırladı; makine beklenmedik biçimde çalıştı. Sonraki versiyonda `GVL_HMI` ara katmanı eklendi: HMI → `GVL_HMI.rNewSetpoint`, Task_Control → değer doğrulama → geçerliyse `GVL_Params.rSetpoint` güncellendi. Operatör hatalarına karşı bir güvenlik katmanı kazanıldı.

**Not 5 — PERSISTENT Listesi Sıra Değişince Sessiz Bozulma**  
Bir makinede `PERSISTENT` kalibrasyon değerleri zamanla "kaymış" değerler gösterdi — biri diğerinin değerini okudu. Neden: PERSISTENT değişkenler `PersistentVars` listesinde **bildirim sırasına göre** bir bellek imajına serileştirilir. Birisi listenin ortasına yeni bir değişken ekleyince, ekleme noktasından sonraki tüm değişkenlerin offset'i kaydı; eski persistent imaj yeni layout'a yanlış eşlendi. Ders: PERSISTENT/RETAIN listelerine **yalnızca sona** ekle, ortadan asla; tip değiştirme (REAL→LREAL) de offset kaydırır. Bu, fundamentals/02'deki retain layout kuralının GVL'ye yansımasıdır.

**Not 6 — `AT %` ile GVL'nin Topolojiye Kilitlenmesi**  
GVL_IO içinde `xMotor1_Run AT %Q0.0` gibi doğrudan adresler vardı. Bir fieldbus slave eklenince tüm `%Q` adresleri kaydı, GVL'deki sembolik isimler artık yanlış fiziksel kanallara bağlandı — makine yanlış valfleri açtı. Ders: GVL'de `AT %` doğrudan adres yerine **device tree I/O Mapping** üzerinden sembolik eşleme yapın. `AT %` yalnızca topolojisi asla değişmeyecek sistemlerde; değişebilen her yerde mapping ekranı (bkz. fundamentals/02 Not 8).

**Not 7 — GVL'nin OPC UA'ya Aşırı Açılması**  
Tüm GVL'ler Symbol Configuration'da işaretlenip OPC UA'ya açılmıştı. Sonuç: 8000+ sembol, devasa bootapp, yavaş sembolik erişim ve güvenlik açığı (iç durum değişkenleri dışarıdan yazılabilir). Ders: Yalnızca dışarı açılması gereken değişkenleri (GVL_HMI okunabilir, GVL_Params yazılabilir) sembol setine alın; GVL_State/GVL_Diag iç kalmalı. GVL katmanlaması burada erişim kontrolünün temeli olur.

## Edge Case'ler ve Sistem Limitleri

### RETAIN / PERSISTENT'ın Sessiz Sınırları

```
Durum                               Sonuç
─────────────────────────────────────────────────────────────────
Retain bölge boyutu aşıldı          Download reddedilir veya sessiz kesilir
Liste ortasına değişken eklendi     Offset kayar → tüm sonraki değerler bozulur
Tip değişti (INT→DINT, REAL→LREAL)  Offset kayar → değerler çöp olur
PERSISTENT bir FB instance içinde   Bazı sürümde derlenir AMA kaydedilmez
RETAIN pointer/referans             Adres saklamak anlamsız (reboot'ta geçersiz)
Clean download                      RETAIN da silinebilir (sadece power-cycle korur)
```

**Kritik:** PERSISTENT değişkenler `Add Object → Persistent Variables` listesinde toplanmalı. Rastgele bir POU'da `VAR PERSISTENT` yazmak bazı sürümlerde sessizce kaydedilmez — veri kaybı uyarısız gelir.

### qualified_only ve Namespace Çakışması

```
qualified_only KAPALI + iki GVL'de aynı isim → "ambiguous" derleme hatası
qualified_only KAPALI + kütüphanede aynı isim → çakışma (6 ay sonra patlar)
qualified_only AÇIK → her erişimde GVL prefix zorunlu, çakışma imkânsız
```

Edge case: Kendi GVL'niz `qualified_only` olsa bile, prefix'siz erişime izin veren eski bir kütüphane aynı ismi taşırsa, kütüphane tarafında belirsizlik oluşabilir. Çözüm: kütüphanelere namespace ver, GVL'lerde qualified_only'yi koru.

### Çoklu Task Erişiminde Atomiklik

GVL bir bellek bölgesidir; iki task aynı değişkene erişebilir. Atomiklik word boyutuna bağlıdır (bkz. task-structure/03):

```
GVL'de güvenli paylaşım (tek-yazar/tek-okur, ≤word): BOOL, INT, DINT, REAL(32-bit)
GVL'de TEHLİKELİ (çok-word, bölünebilir): LREAL, STRING, STRUCT, ARRAY
→ Çok-word paylaşım için double-buffer veya mutex; "GVL'ye koydum, paylaşılır" yetmez
```

## Optimizasyon

### Bellek Düzeni: GVL Struct'larının Hizalanması

GVL'deki struct/değişken sıralaması bellek dolgusunu (padding) etkiler:

```iecst
(* ❌ Karışık sıra — padding israfı *)
VAR_GLOBAL
    x1 : BOOL;    (* 1 byte + 3 padding *)
    r1 : REAL;    (* 4 byte *)
    x2 : BOOL;    (* 1 byte + 3 padding *)
    r2 : REAL;
END_VAR

(* ✅ Büyükten küçüğe — padding minimum *)
VAR_GLOBAL
    r1 : REAL;    (* 4 byte *)
    r2 : REAL;    (* 4 byte *)
    x1 : BOOL;    (* 1 byte *)
    x2 : BOOL;    (* 1 byte *)
END_VAR
```

Bu özellikle PERSISTENT/RETAIN bölgesinde kritik: küçük retain bütçesini padding ile israf etmek, sığmayan veri demektir.

### BOOL Paketleme ve Fieldbus Bant Genişliği

100 ayrı `BOOL` global yerine bir `DWORD` + bit erişimi (`GVL.dwFlags.0`), hem belleği hem de fieldbus/OPC UA üzerinden taşınan veriyi yoğunlaştırır — özellikle Modbus gibi register-tabanlı protokollerde 16 BOOL = 1 register tasarrufu.

### Symbol Configuration'ı Daraltma

OPC UA / sembolik erişim için üretilen sembol seti, hem bootapp boyutunu hem indirme süresini hem de runtime sembolik erişim hızını etkiler. Yalnızca gerçekten dışarı açılan GVL'leri (GVL_HMI, GVL_Params, seçili GVL_Diag) sembol setine dahil edin — GVL_State/iç değişkenler hariç tutulmalı.

## Derin Teknik Detay

### GVL Neden Var? — POU Kapsülleme ile Global Durum Gerilimi

İyi mimari "global durumdan kaçın" der; ama bir PLC fiziksel dünyada paylaşılan durumdur (I/O herkesindir). GVL bu gerilimin çözümüdür: global durumu **yapısallaştırır** ve sahiplik kuralı dayatır. Tek büyük GVL anti-pattern'i, global durumun yapısızlaşmasıdır — her POU her şeye dokunabilir, yani kapsülleme tamamen çöker. GVL katmanlaması (IO/HMI/Params/Alarms/Config), global durumu "sahipli alt-alanlara" böler; her alanın tek yazarı vardır. Bu, paylaşımlı belleği nesne-benzeri bir disipline sokmanın PLC yoludur.

### Kalıcılık Mekanizmasının İç Çalışması

```
Standart VAR_GLOBAL → çalışma belleği (RAM), her başlangıçta init değeri
RETAIN              → ayrı "retain segment" (RAM + power-fail koruması: NVRAM/flush)
PERSISTENT          → retain segment + bootproject ile birlikte saklanır
```

RETAIN bölgesi neden download'da silinir ama power-cycle'da korunur? Çünkü retain, **kod-bağımsız bir bellek imajıdır**: power-cycle kodu değiştirmez, layout aynı kalır, imaj geçerli. Download ise yeni bir layout getirebilir; runtime eski imajın yeni koda uyduğunu garanti edemez, bu yüzden temkinli davranıp sıfırlar. PERSISTENT, layout'u bootproject ile birlikte sakladığı için download'a da dayanır. Bu, "neden RETAIN download'da gider ama PERSISTENT gitmez" sorusunun mekanik cevabıdır — ve neden ikisinde de **sıra değiştirmek ölümcül** olduğunun (layout = offset eşlemesi) kökü.

### qualified_only: Derleyici Sembol Çözümleme Politikası

`qualified_only` bir derleyici sembol-arama (name resolution) politikasıdır. Kapalıyken derleyici, niteliksiz bir isim için tüm GVL'leri ve kütüphaneleri tarar; iki eşleşme bulursa belirsizlik (ambiguity) hatası verir. Açıkken arama uzayı tek bir GVL'ye daraltılır (prefix ile). V2'de bu yoktu (düz isim alanı); V3 büyük projeler ve kütüphane ekosistemi için bunu varsayılan yaptı. Anti-pattern (qualified_only kaldırmak), kısa vadeli yazım kolaylığı için derleyicinin çakışma korumasını kapatmaktır — 6 ay sonra üçüncü taraf kütüphane geldiğinde patlar (Not 3).

### GVL ve Task Race'i: Aynı Madalyonun İki Yüzü

GVL tasarımı (bu belge) ve task öncelik/race yönetimi (task-structure/03) ayrılmaz: GVL paylaşımın **nerede** olduğunu, task modeli paylaşımın **ne zaman tehlikeli** olduğunu tanımlar. "Her GVL'ye tek task yazar" kuralı, aslında preemptive scheduler'da race condition'ı önlemenin GVL-katmanındaki ifadesidir. GVL'yi tasarlarken her zaman "bu değişkeni hangi task yazıyor, hangisi okuyor?" matrisini çıkarmak, ikisini birleştiren uzman pratiğidir.

## İlgili Konular

```
knowledge/codesys/programming/
├── 01_pou_types.md          → GVL'ye erişen POU tipleri
├── 03_function_blocks.md    → FB içinde GVL erişim pratikleri
└── 05_error_handling.md     → GVL_Alarms tasarımı detayları

knowledge/codesys/task-structure/
└── 03_priority_management.md → GVL'ye çoklu task erişiminde race condition

knowledge/codesys/fundamentals/
└── 02_project_structure.md  → GVL'nin proje hiyerarşisindeki yeri
```
