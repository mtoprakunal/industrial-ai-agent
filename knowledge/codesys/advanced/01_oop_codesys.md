---
KONU        : CODESYS V3 Nesne Yönelimli Programlama (OOP)
KATEGORİ    : codesys
ALT_KATEGORI: advanced
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_obj_interface.html"
    başlık: "CODESYS Online Help — Object: Interface"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_implementing_interface.html"
    başlık: "CODESYS Online Help — Implementation of an Interface"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_extending_function_block.html"
    başlık: "CODESYS Online Help — Extending a Function Block (EXTENDS, SUPER)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_obj_interface_property.html"
    başlık: "CODESYS Online Help — Object: Interface Property"
    güvenilirlik: resmi
  - url: "https://stefanhenneken.net/2010/10/04/methoden-eigenschaften-und-vererbung-mit-codesys-v3/"
    başlık: "Stefan Henneken — IEC 61131-3: Methoden, Eigenschaften und Vererbung"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/codesys/programming/03_function_blocks.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/programming/01_pou_types.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/fundamentals/03_iec61131_languages.md"
    ilişki: tamamlar
  - konu: "02_state_machines_sfc.md"
    ilişki: tamamlar
  - konu: "_synthesis.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "Function Block tasarımı ve instance modeli (programming/03_function_blocks.md)"
  - "POU tipleri ve bellek modeli (programming/01_pou_types.md)"
  - "ST dili ileri düzey aşinalık (fundamentals/03_iec61131_languages.md)"
ÇELİŞKİLER :
  - kaynak: "IEC 61131-3 2. baskı vs 3. baskı"
    konu: "OOP (METHOD, INTERFACE, EXTENDS) standardın 3. baskısıyla geldi; eski PLC kültürü OOP'a mesafeli"
    çözüm: >
      OOP, IEC 61131-3'ün 3. baskısında resmileşti ve CODESYS V3 bunu tam destekler.
      Ancak klasik FB + state machine yaklaşımı hâlâ çoğu otomasyon işi için yeterlidir.
      OOP'u "zorunlu" değil, "doğru yerde araç" olarak görün; bkz. Ne Zaman bölümü.
  - kaynak: "C++/Java OOP alışkanlıkları"
    konu: "CODESYS OOP'u masaüstü OOP gibi davranmaz: çöp toplayıcı yok, instance statiktir, online change kısıtları vardır"
    çözüm: >
      [DOĞRULANMADI — genel davranış; sürüm bazında ince farklar olabilir]
      CODESYS instance'ları derleme/indirme anında statik ayrılır; new/delete yoktur.
      Polimorfizm interface/pointer referansı üzerinden çalışır. Masaüstü OOP
      kalıplarını birebir taşımayın.
---

## Özün Ne

CODESYS V3, IEC 61131-3'ün 3. baskısıyla gelen nesne yönelimli programlamayı (OOP) tam destekler: INTERFACE, METHOD, PROPERTY, EXTENDS (kalıtım), IMPLEMENTS (arayüz uygulama), THIS^ ve SUPER^ işaretçileri. Bu yapıların tamamı yalnızca FUNCTION_BLOCK üzerinde çalışır — Program ve Function OOP'a katılmaz. OOP, klasik "FB + GVL + state machine" mimarisinin yerini almaz; onu **belirli problemlerde** (çok sayıda benzer ama farklı cihaz tipi, eklenti mimarisi, sürücü soyutlaması) tamamlar. Yanlış yerde kullanılan OOP, basit bir işi anlaşılması zor bir kalıtım ağacına çevirir; doğru yerde kullanılan OOP ise kod tekrarını yok eder ve genişletilebilir mimari kurar. Bu belgenin amacı, "ne zaman OOP, ne zaman klasik FB" sorusuna net cevap vermek ve OOP'un PLC'ye özgü tuzaklarını (online change, pointer, gövde vs metot) göstermektir.

## Nasıl Çalışır

### Beş Yapı Taşı

| Yapı | Anahtar kelime | Ne işe yarar |
|---|---|---|
| Metot | `METHOD` | FB'ye, gövdeden ayrı, açıkça çağrılan işlev ekler (parametre + dönüş) |
| Özellik | `PROPERTY` | Get/Set erişimcileriyle kapsüllenmiş "alan" görünümü sağlar |
| Arayüz | `INTERFACE` | Yalnızca metot/özellik prototipleri içeren sözleşme (uygulama yok) |
| Kalıtım | `EXTENDS` | Türetilen FB, temel FB'nin tüm veri ve metotlarını devralır |
| Uygulama | `IMPLEMENTS` | FB'nin bir arayüzün tüm prototiplerini gerçeklemeyi taahhüt etmesi |

İki örtük işaretçi:
- `THIS^` — "şu anki instance'ın kendisi" (kendi alan/metotlarına erişim, gölgelenme çözme).
- `SUPER^` — türetilen FB içinden temel (base) FB'nin metot/değişkenlerine doğrudan erişim.

### METHOD — Gövdeden Ayrı Davranış

Klasik FB'de tüm mantık FB gövdesindedir (her çağrıda çalışır). METHOD ise yalnızca **açıkça çağrıldığında** çalışan, kendi `VAR_INPUT`/`VAR_OUTPUT`/`VAR` (yerel, stack'te, kalıcı değil) ve isteğe bağlı dönüş tipi olan bir işlevdir.

```iecst
METHOD SetSpeed : BOOL          (* BOOL döner: başarı/başarısızlık *)
VAR_INPUT
    rTargetSpeed : REAL;
END_VAR
    IF rTargetSpeed < 0.0 OR rTargetSpeed > rMaxSpeed THEN
        SetSpeed := FALSE;      (* Sınır dışı — reddet *)
        RETURN;
    END_IF
    rSetpoint := rTargetSpeed;  (* FB'nin kendi VAR'ı — kalıcı *)
    SetSpeed := TRUE;
```

> **Kritik kural (programming/03 Not 7):** Metodun kendi `VAR` bölümü **stack'tedir, kalıcı değildir** — her çağrıda sıfırlanır. Bu yüzden TON/CTU/R_TRIG gibi durumlu bloklar **asla** metot yerelinde tanımlanmaz; FB gövde-seviyesi `VAR`'da durur.

### PROPERTY — Get/Set ile Kapsülleme

PROPERTY, dışarıdan bir değişken gibi görünen ama altta Get ve/veya Set erişimci (accessor) metotları çalıştıran yapıdır. Resmî olarak bir özellik, `Get` ve/veya `Set` erişimcilerini bildirir; arayüzde bu erişimciler yalnızca prototip olarak yer alır, gövdesiz olur.

```iecst
(* PROPERTY rTemperature : REAL  altında: *)

(* Get erişimcisi *)
rTemperature := rInternalTemp;          (* okurken hesaplanmış değer dönebilir *)

(* Set erişimcisi *)
IF rTemperature >= rMinSet AND rTemperature <= rMaxSet THEN
    rInternalTemp := rTemperature;       (* yazarken sınır kontrolü *)
END_IF
```

Kullanan taraf `fbHeater.rTemperature := 80.0;` yazar; perde arkasında Set erişimcisi sınırı kontrol eder. Bu, "ham VAR_INPUT" yerine doğrulama içeren bir arayüz sunar.

### INTERFACE — Uygulamasız Sözleşme

Resmî tanım: bir arayüz, "metot ve özellik prototipleri kümesidir" — gövde içermez, değişken tanımlanamaz. CODESYS, arayüz tipindeki değişkenleri **her zaman referans (reference)** olarak ele alır. Bir FB, `IMPLEMENTS` ile bir veya birden fazla arayüzü uygular ve bu arayüzlerin tüm metot/özellik prototiplerini aynı isim ve parametrelerle gerçeklemek zorundadır.

```iecst
INTERFACE I_Drive
    (* Yalnızca prototipler — gövde yok *)
END_INTERFACE

METHOD Start : BOOL              (* I_Drive altında *)
METHOD Stop  : BOOL
PROPERTY rActualSpeed : REAL     (* Get *)
```

```iecst
FUNCTION_BLOCK FB_Servo IMPLEMENTS I_Drive
(* Start, Stop, rActualSpeed'in TAMAMINI gerçeklemek ZORUNLU *)
```

Arayüzler **çoklu kalıtımı** destekler (`INTERFACE I_C EXTENDS I_A, I_B`). Bir FB de aynı anda birden fazla arayüz uygulayabilir.

### EXTENDS — FB Kalıtımı

`FUNCTION_BLOCK FB_Derived EXTENDS FB_Base` ile türetilen FB, temel FB'nin tüm verilerini ve metotlarını devralır. Resmî kurallar:

- Türetilen instance, temel tip beklenen her yerde kullanılabilir (Liskov ikamesi).
- Metotlar aynı imzayla (isim + giriş + çıkış) override (ezilme) edilebilir.
- Türetilen FB, temel FB'deki değişkenle **aynı isimde değişken tanımlayamaz** (yalnızca `VAR_TEMP` istisnadır).
- **FB için çoklu kalıtım YASAKTIR** (yalnızca arayüzler çoklu kalıtım/uygulama yapabilir).
- `SUPER^` ile temel FB'nin metot/değişkenlerine erişilir.

```iecst
FUNCTION_BLOCK FB_ServoDrive EXTENDS FB_Drive

METHOD Start : BOOL              (* Base'deki Start'ı override eder *)
    SUPER^.Start();              (* Önce base davranışını çalıştır *)
    xServoEnabled := TRUE;       (* Sonra servo'ya özel ek davranış *)
    Start := TRUE;
```

### Abstract (Soyut) Kavramı

[DOĞRULANMADI — resmî EXTENDS sayfası soyut FB/metottan açıkça bahsetmez; davranış sürüm/derleyici sürümüne bağlı olabilir.] Pratikte:
- **INTERFACE zaten doğası gereği soyuttur** — gövde içermez, instance'ı oluşturulamaz, yalnızca uygulayan FB'de mantık vardır. PLC'de "abstract base class" ihtiyacının büyük kısmı arayüzle çözülür.
- Bazı CODESYS sürümleri `abstract` pragma/anahtar kelimeyle soyut metot/FB tanımına izin verir; ancak bunu kullanmadan önce hedef runtime sürümünde desteklendiğini doğrulayın. Taşınabilirlik için arayüz tercih edin.

## Pratikte Nasıl Kullanılır

### OOP Bir POU'ya Nasıl Eklenir

```
Application (sağ tık) → Add Object → Interface...   → I_Drive
I_Drive (sağ tık)     → Add Object → Method...      → Start, Stop
I_Drive (sağ tık)     → Add Object → Property...    → rActualSpeed

FB (sağ tık)          → Add Object → Method...      → metot ekle
FB declaration        → IMPLEMENTS / EXTENDS satırı elle yazılır
```

FB'ye metot eklerken CODESYS, temel bloktaki metotların bir listesini sunar; bunları kabul edip override için uyarlayabilirsiniz.

### Polimorfizm Deseni (En Değerli Kullanım)

Farklı cihaz tipleri aynı arayüzü uygular; üst katman onları tek tip olarak yönetir:

```iecst
VAR
    fbServo  : FB_ServoDrive;        (* IMPLEMENTS I_Drive *)
    fbVFD    : FB_FrequencyDrive;    (* IMPLEMENTS I_Drive *)
    aiDrives : ARRAY[1..2] OF I_Drive;
END_VAR

aiDrives[1] := fbServo;              (* arayüz referansı atanır *)
aiDrives[2] := fbVFD;

(* Üst katman tipi bilmeden çalıştırır — polimorfizm *)
FOR i := 1 TO 2 DO
    aiDrives[i].Start();             (* her cihaz kendi Start'ını çalıştırır *)
END_FOR
```

Üst katman `FB_ServoDrive` mi `FB_FrequencyDrive` mı olduğunu bilmez; arayüz sözleşmesine güvenir. Yeni bir sürücü tipi eklemek, üst katmanı değiştirmeden mümkün olur.

### Klasik FB ile OOP'un Birlikte Yaşaması

OOP her şeyi sarmalamaz. Pratik mimari:
- Ana state machine ve cihaz yaşam döngüsü → klasik FB gövdesi (CASE) — bkz. 02_state_machines_sfc.md.
- Cihaz tipleri arası ortak sözleşme → INTERFACE.
- Tip-özel davranış → IMPLEMENTS / EXTENDS + METHOD.
- Doğrulamalı erişim → PROPERTY.

## Örnekler

### Örnek 1: Arayüz + Polimorfizm — Çok Tipli Vana Yönetimi

```iecst
INTERFACE I_Valve
    (* prototipler *)
END_INTERFACE
METHOD Open  : BOOL              (* I_Valve *)
METHOD Close : BOOL
PROPERTY xIsOpen : BOOL          (* Get *)
```

```iecst
(* İki farklı vana donanımı, aynı sözleşme *)
FUNCTION_BLOCK FB_SolenoidValve IMPLEMENTS I_Valve
VAR_OUTPUT xCoilOut : BOOL; END_VAR
VAR xOpenState : BOOL; END_VAR

METHOD Open : BOOL
    xCoilOut := TRUE;
    xOpenState := TRUE;
    Open := TRUE;
(* Close, xIsOpen benzer şekilde gerçeklenir *)
```

```iecst
FUNCTION_BLOCK FB_MotorizedValve IMPLEMENTS I_Valve
VAR_OUTPUT xOpenCmd : BOOL; END_VAR
VAR fbActuator : FB_Actuator; xOpenState : BOOL; END_VAR

METHOD Open : BOOL
    fbActuator.Drive(eDir := eOpen);   (* motorlu — farklı iç mantık *)
    xOpenState := fbActuator.xAtOpenLimit;
    Open := xOpenState;
```

```iecst
(* Üst katman — tipten bağımsız *)
PROGRAM PRG_ValveManager
VAR
    fbSol  : FB_SolenoidValve;
    fbMot  : FB_MotorizedValve;
    aValves : ARRAY[1..2] OF I_Valve := [fbSol, fbMot];
    i : INT;
END_VAR
FOR i := 1 TO 2 DO
    IF GVL_HMI.axOpenCmd[i] THEN
        aValves[i].Open();           (* polimorfik çağrı *)
    END_IF
END_FOR
```

### Örnek 2: EXTENDS + SUPER^ — Temel Sürücü ve Servo Genişletmesi

```iecst
FUNCTION_BLOCK FB_Drive               (* temel: ortak start/stop *)
VAR_INPUT xEnable : BOOL; END_VAR
VAR_OUTPUT xRunOut : BOOL; END_VAR

METHOD Start : BOOL
    IF xEnable THEN
        xRunOut := TRUE;
        Start := TRUE;
    END_IF
```

```iecst
FUNCTION_BLOCK FB_ServoDrive EXTENDS FB_Drive
VAR_OUTPUT xServoEnable : BOOL; END_VAR

METHOD Start : BOOL                    (* override *)
    Start := SUPER^.Start();           (* base mantığı yeniden kullan *)
    IF Start THEN
        xServoEnable := TRUE;          (* servo'ya özel ek adım *)
    END_IF
```

### Örnek 3: PROPERTY ile Doğrulamalı Setpoint

```iecst
FUNCTION_BLOCK FB_Heater
VAR
    rSetInternal : REAL;
    rMinSet : REAL := 0.0;
    rMaxSet : REAL := 250.0;
END_VAR
```

```iecst
(* PROPERTY rSetpoint : REAL — Set erişimcisi *)
IF rSetpoint >= rMinSet AND rSetpoint <= rMaxSet THEN
    rSetInternal := rSetpoint;
ELSE
    (* sınır dışı yazma sessizce reddedilir — son geçerli değer korunur *)
    ;
END_IF
```

```iecst
(* PROPERTY rSetpoint : REAL — Get erişimcisi *)
rSetpoint := rSetInternal;
```

Kullanım: `fbHeater.rSetpoint := 300.0;` → Set erişimcisi reddeder; `rSetInternal` değişmez.

## Sık Yapılan Hatalar

### Hata 1: Metot Yerelinde Durumlu Blok

```iecst
(* ❌ YANLIŞ — metot VAR'ı kalıcı değil, timer her çağrı sıfırlanır *)
METHOD Run : BOOL
VAR tDelay : TON; END_VAR        (* stack'te — sıfırlanır *)
    tDelay(IN := TRUE, PT := T#3S);
    Run := tDelay.Q;             (* asla TRUE olmaz *)

(* ✅ DOĞRU — timer FB gövde-seviyesi VAR'da *)
(* FB VAR: tDelay : TON; *)
METHOD Run : BOOL
    tDelay(IN := TRUE, PT := T#3S);
    Run := tDelay.Q;
```

### Hata 2: FB Gövdesinin Override'ı Çağırdığını Sanmak

```iecst
(* FB gövdesindeki kod, türetilen sınıfın metodunu OTOMATİK çağırmaz.
   Polimorfizm gövdeden değil, metot çağrılarından gelir.
   (programming/03 Not 5) *)

(* ❌ YANLIŞ varsayım: base FB gövdesinde mantık + türetilende override
   beklemek → base gövde hâlâ eski mantığı çalıştırır. *)

(* ✅ DOĞRU: mantığı metoda taşı, gövdeyi yalnızca THIS^.Method() çağrısına indir *)
THIS^.Execute();   (* türetilen FB'de Execute override edilmişse o çalışır *)
```

### Hata 3: Atanmamış Arayüz Referansını Çağırmak

```iecst
(* ❌ YANLIŞ — arayüz referansı NULL iken metot çağrısı → crash *)
VAR iDrive : I_Drive; END_VAR
iDrive.Start();                  (* iDrive hiç atanmadıysa runtime exception *)

(* ✅ DOĞRU — geçerlilik kontrolü *)
IF iDrive <> 0 THEN              (* arayüz ref'i 0/NULL ile karşılaştırılır *)
    iDrive.Start();
END_IF
```

### Hata 4: OOP'u Basit İşe Zorlamak

Tek bir motor tipi, tek bir state machine için INTERFACE + EXTENDS + polimorfizm kurmak — gereksiz karmaşıklık. Klasik `FB_Motor` (CASE state machine) yeterken kalıtım ağacı kurmak, kodu okunamaz hale getirir.

### Hata 5: Çoklu FB Kalıtımı Denemek

```iecst
(* ❌ Derleme hatası — FB çoklu kalıtım yapamaz *)
FUNCTION_BLOCK FB_X EXTENDS FB_A, FB_B

(* ✅ Çoklu davranış gerekiyorsa: tek EXTENDS + çoklu IMPLEMENTS *)
FUNCTION_BLOCK FB_X EXTENDS FB_A IMPLEMENTS I_B, I_C
```

### Hata 6: Online Change ile Arayüz/Pointer Tutarsızlığı

Online change sırasında bir FB'nin yapısı (eklenen/çıkarılan değişken, değişen metot imzası) bellek düzenini değiştirebilir. Önceden saklanmış ham `ADR()`/`POINTER TO` değerleri ve bazı durumlarda arayüz referansları geçersizleşebilir (dangling). [DOĞRULANMADI — kesin davranış sürüme bağlı.] Güven gereken yerde online change yerine **download** ile devreye alın.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### OOP Tercih Edin

- **Çok sayıda benzer ama farklı cihaz tipi** ortak bir sözleşmeyle yönetilecekse (sürücü, vana, sensör aileleri) → INTERFACE + polimorfizm.
- **Eklenti/genişletilebilir mimari**: yeni tip eklendiğinde üst katman değişmemeli → arayüz.
- **Sürücü/HAL soyutlaması**: aynı üst mantık, farklı donanım altyapısı → arayüz.
- **Ortak temel + küçük varyasyonlar**: temel FB + EXTENDS ile birkaç metot override.
- **Doğrulamalı/hesaplanmış erişim**: ham VAR yerine PROPERTY.
- **Kütüphane geliştirme**: kararlı bir arayüz, dahili uygulamayı kullanıcıdan gizler.

### Klasik FB Tercih Edin (OOP Kullanmayın)

- Tek cihaz tipi, tek state machine → `FB_X` + CASE yeterli.
- Saha ekibi OOP bilmiyor ve kodu bakacak olan onlar → okunabilirlik kalıtımdan önemli.
- Basit I/O eşleme, interlock → OOP gereksiz soyutlama.
- Performans-kritik sıcak döngü → metot/sanal çağrı küçük ama ölçülebilir ek yük getirir.

### Karar Kuralı

> "Aynı arayüzü uygulayan **iki veya daha fazla** farklı uygulamam var mı?" Cevap hayırsa, polimorfizme gerek yok; klasik FB seçin. Cevap evetse, OOP gerçek değerini gösterir.

## Gerçek Proje Notları

**Not 1 — Arayüzün Eklenti Mimarisini Kurtarması**
Bir paketleme hattında üç farklı tartım hücresi tedarikçisi vardı (her biri farklı haberleşme). `I_WeighCell` arayüzü tanımlandı; her tedarikçi için ayrı FB onu uyguladı. Üst katman (`FB_WeighManager`) yalnızca `I_WeighCell` referansları tuttu. Dördüncü tedarikçi eklendiğinde üst katmanda tek satır değişmedi — yalnızca yeni bir FB yazıldı. OOP'un bu projede getirdiği değer, kalıtımdan değil **soyutlamadan** geldi.

**Not 2 — Gereksiz Kalıtım Ağacının Bedeli**
Başka bir projede genç bir ekip her şeyi OOP yaptı: `FB_Base` → `FB_Device` → `FB_Motor` → `FB_PumpMotor` → `FB_DosingPumpMotor`, beş seviye. Bir hata ayıklarken davranışın hangi seviyede tanımlandığını bulmak yarım gün sürdü (gövde mi, hangi override mı). Sonraki revizyonda iki seviyeye indirildi. Ders: kalıtım derinliği arttıkça okunabilirlik düşer; 2 seviye pratik üst sınırdır.

**Not 3 — Gövde + Override Karışımının Sessiz Hatası**
Bir `FB_Drive` gövdesinde state machine vardı; `FB_Servo EXTENDS FB_Drive` bir metodu override etti ama base gövde hâlâ eski yolu çalıştırıyordu (programming/03 Not 5). Override beklenen yerde devreye girmedi. Çözüm: tüm mantık `Execute()` metoduna taşındı, gövde yalnızca `THIS^.Execute()` çağırdı; böylece türetilen FB'nin override'ı polimorfik olarak çalıştı. Ders: OOP kullanacaksan **mantığı gövdeden metoda taşı**; "gövde + override" melezi tuzaktır.

**Not 4 — Online Change Sonrası Bozulan Arayüz Dizisi**
Bir sistemde `ARRAY OF I_Drive` çalışma anında dolduruluyordu. Online change ile bir FB'ye değişken eklendi; bazı arayüz referansları beklenmedik davrandı, bir sürücü yanlış metodu çalıştırır gibi göründü. Sorun bir soğuk reset (download) ile çözüldü. Ders: arayüz referansı tutan diziler/pointer'lar online change'e hassastır; kritik devreye almada download tercih edin. [DOĞRULANMADI — kök neden sürüm-spesifik.]

**Not 5 — PROPERTY ile HMI Doğrulaması**
Operatör HMI'dan setpoint giriyordu. Eskiden ham `VAR_INPUT rSet` vardı ve operatör 9999 yazınca sistem absürt değere gidiyordu. `PROPERTY rSetpoint` (Set erişimcisinde sınır kontrolü) eklenince geçersiz değerler kaynağında reddedildi; her çağrı noktasında ayrı kontrol gereği ortadan kalktı. Tek doğrulama noktası, dağıtık kontrolden daha güvenilir oldu.

## İlgili Konular

```
knowledge/codesys/advanced/
├── _synthesis.md               → OOP ne zaman / durum makinesi tasarımı sentezi
└── 02_state_machines_sfc.md    → Klasik state machine (OOP'un alternatifi/tamamlayıcısı)

knowledge/codesys/programming/
├── 01_pou_types.md             → FB instance modeli, METHOD/THIS^ neden sadece FB'de
├── 03_function_blocks.md       → FB tasarımı, gövde vs metot (Not 5, 7)
└── _synthesis.md               → Kapsülleme ve veri akışı ilkeleri

knowledge/codesys/fundamentals/
└── 03_iec61131_languages.md    → OOP'un neden yalnızca ST'de tanımlandığı
```
