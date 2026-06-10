---
KONU        : CODESYS Standart Kütüphaneleri (Standard, Util, IoStandard)
KATEGORİ    : codesys
ALT_KATEGORI: libraries
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/libs/Standard/Current/index.html"
    başlık: "CODESYS Online Help — Standard Library Documentation"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/libs/Util/Current/index.html"
    başlık: "CODESYS Online Help — Util Library Documentation"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/libs/Standard/Current/Trigger/R_TRIG.html"
    başlık: "CODESYS Online Help — R_TRIG (FB)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/libs/Util/Current/Mathematical-Functions/LIN_TRAFO.html"
    başlık: "CODESYS Online Help — LIN_TRAFO (FB)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/libs/Util/Current/Controller/PID.html"
    başlık: "CODESYS Online Help — PID (FB)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "02_library_management.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/programming/03_function_blocks.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/fundamentals/03_iec61131_languages.md"
    ilişki: gerektirir
  - konu: "_synthesis.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "FB instance modeli ve her-scan-çağrı kuralı (programming/03_function_blocks.md)"
  - "ST/FBD temelleri (fundamentals/03_iec61131_languages.md)"
ÇELİŞKİLER :
  - kaynak: "Eski IEC standardı vs CODESYS sürümleri"
    konu: "Standard library içindeki sayaç adı: CTUD mü ayrı CTU/CTD/CTUD mu?"
    çözüm: >
      Standard kütüphanesi CTU, CTD ve CTUD'yi içerir (yukarı, aşağı, yukarı/aşağı).
      Bazı eski dokümanlar yalnızca CTUD'den bahseder. Hedef sürümün
      Standard kütüphane dokümanını esas alın.
  - kaynak: "Platform üreticileri (Schneider, ABB, Beckhoff vb.)"
    konu: "Util library bazı platformlarda farklı isimle/parçalanmış gelebilir"
    çözüm: >
      [DOĞRULANMADI — platform bazında değişir] PID/CHARCURVE gibi bloklar bazı
      türevlerde ayrı kütüphanelere taşınmış olabilir. Üretici kütüphane
      listesini Library Manager'dan teyit edin.
---

## Özün Ne

CODESYS, neredeyse her projede ihtiyaç duyulan temel yapı taşlarını hazır kütüphaneler olarak sunar; bunların başında **Standard** (zamanlayıcı, sayaç, kenar algılama, bistabil), **Util** (ölçekleme, karakteristik eğri, PID, sinyal üreteçleri, bit/BCD/Gray dönüşümleri, istatistik) ve **IoStandard** (G/Ç konfigürasyon yapı taşları) gelir. Bu kütüphaneleri bilmenin değeri çift yönlüdür: bir yandan tekerleği yeniden icat etmekten (kendi TON'unu yazmak) kurtarır, diğer yandan bu bloklar IEC 61131-3'te standartlaştığı için her CODESYS tabanlı platformda aynı davranışı sergiler — yani taşınabilir ve öngörülebilirdir. Uzman, bu kütüphanelerin **ne sunduğunu** ezbere bilir; böylece "bunu kendim mi yazsam" sorusuna çoğu zaman "hayır, zaten var" yanıtını verir ve hazır bloğun ince davranışlarını (TON'un çağrı-güdümlü zamanı, PID'in cycle time bağımlılığı) tuzağa düşmeden kullanır.

## Nasıl Çalışır

### Standard Kütüphanesi — IEC Temel Blokları

IEC 61131-3'ün standart fonksiyon bloklarını içerir; FBD/LD/ST hepsinde kullanılır.

**Zamanlayıcılar (Timer)**
| Blok | İşlev |
|---|---|
| TON | Açma gecikmesi: IN TRUE olduktan PT süre sonra Q TRUE |
| TOF | Kapama gecikmesi: IN FALSE olduktan PT süre sonra Q FALSE |
| TP | Darbe (pulse): IN tetiklenince Q, PT süre boyunca TRUE |

**Sayaçlar (Counter)**
| Blok | İşlev |
|---|---|
| CTU | Yukarı sayıcı: CU yükselen kenarda CV artar, CV>=PV iken Q TRUE |
| CTD | Aşağı sayıcı: CD kenarında CV azalır, CV<=0 iken Q TRUE |
| CTUD | Yukarı/aşağı sayıcı: hem CU hem CD, RESET/LOAD ile |

**Kenar Algılama (Trigger)**
| Blok | İşlev |
|---|---|
| R_TRIG | Yükselen kenar: CLK FALSE→TRUE geçişinde Q tek scan TRUE |
| F_TRIG | Düşen kenar: CLK TRUE→FALSE geçişinde Q tek scan TRUE |

**Bistabil (Latch)**
| Blok | İşlev |
|---|---|
| SR | Set-baskın latch: SET1 baskındır (SET ve RESET birlikteyse Q1 TRUE) |
| RS | Reset-baskın latch: RESET1 baskındır |

**Diğer**
| Blok | İşlev |
|---|---|
| RTC | Gerçek zaman saati: çalışınca güncel tarih/saat döndürür |

Ayrıca CONCAT, LEFT, RIGHT, MID, LEN, FIND, INSERT, DELETE, REPLACE gibi **string** fonksiyonları da standart kapsamında sunulur.

> **Davranış notu:** TON/CTU/R_TRIG gibi bloklar zamanlarını/sayımlarını **çağrıldıkları anda** günceller — iç zaman tabanları yoktur (programming/03 Not 7). Her scan koşulsuz çağrılmaları gerekir; koşullu çağrı `.ET`/`.CV`'yi dondurur.

### Util Kütüphanesi — Pratik Mühendislik Blokları

Standard'ın üstüne sık ihtiyaç duyulan mühendislik fonksiyonlarını ekler:

**Analog / Ölçekleme**
- **LIN_TRAFO** — Doğrusal dönüşüm (ölçekleme): bir aralıktaki değeri başka aralığa lineer eşler (ör. ham ADC → mühendislik birimi).
- **CHARCURVE** — Karakteristik eğri: parçalı doğrusal yaklaşımla giriş verisini tanımlı bir eğriye göre dönüştürür (doğrusal olmayan sensör lineerizasyonu).
- **RAMP_INT / RAMP_REAL** — Çıkışı tanımlı eğimle rampalar (ani sıçramayı yumuşatır).

**Kontrol (Controller)**
- **PID** — Oransal-integral-türevsel kontrolör.
- **PID_FIXCYCLE** — Sabit çevrim süresine göre çalışan PID varyantı.
- **PD** — Oransal-türevsel kontrolör.

**Sinyal (Signals)**
- **BLINK** — Tanımlı açık/kapalı sürelerle yanıp sönen sinyal üretir.
- **GEN** — Fonksiyon üreteci (sinüs, üçgen, kare vb. dalga formları).
- **FREQ_MEASURE** — Sinyal frekansı ölçer.

**Matematiksel**
- **DERIVATIVE / INTEGRAL** — Türev (değişim hızı) ve integral (birikim).
- **STATISTICS_INT / STATISTICS_REAL, VARIANCE** — İstatistiksel hesaplar.

**Bit / BCD / Gray / Kodlama**
- Bit işleme: GETBIT, PUTBIT, SETBIT, EXTRACT, PACK, UNPACK, SWITCHBIT.
- BCD ↔ tamsayı, Gray ↔ ikili dönüşümleri.
- HEX/ASCII ve Base64 kodlama fonksiyonları.

**Analog İzleme (Analog Monitors)**
- **HYSTERESIS** — Histerezisli eşik geçiş algılama (gürültüye karşı kararlı).
- **LIMITALARM** — Değer tanımlı sınırları aşınca alarm üretir.

> **PID uyarısı:** Util.PID'in doğru çalışması cycle time bilgisine bağlıdır; FB her scan çağrılmalı ve çevrim süresi parametresi gerçek task periyoduyla eşleşmelidir (yanlış cycle time → yanlış I/D davranışı). Daha deterministik davranış için `PID_FIXCYCLE` tercih edilebilir.

### IoStandard Kütüphanesi — G/Ç Konfigürasyon Yapı Taşları

IoStandard, G/Ç (I/O) yapılandırması ve cihaz tanımıyla ilgili standart tip/yapı bloklarını sağlar (ör. modül parametre/diagnostik yapıları). [DOĞRULANMADI — kapsam sürüm/cihaz açıklamalarına göre değişir; çoğu projede otomatik olarak referans edilir, kullanıcı doğrudan az çağırır.] Uygulama mühendisi bu kütüphaneyi genellikle dolaylı kullanır; Library Manager'da G/Ç eşlemesi için arka planda referanslanır.

## Pratikte Nasıl Kullanılır

### Kütüphane Bloğu Çağırma

Standard/Util çoğu cihaz projesinde otomatik referanslanır. Bir bloğu kullanmak için instance bildirip her scan çağırın:

```iecst
VAR
    tDelay   : TON;             (* Standard *)
    fbScale  : LIN_TRAFO;       (* Util *)
    fbBlink  : BLINK;           (* Util *)
END_VAR

tDelay(IN := xStart, PT := T#5S);
xDelayed := tDelay.Q;
```

Kütüphane qualified-access ister ya da isim çakışması varsa namespace ile çağırın: `Util.LIN_TRAFO`, `Standard.TON` (bkz. 02_library_management.md namespace).

## Örnekler

### Örnek 1: LIN_TRAFO ile Analog Ölçekleme

```iecst
(* Ham 4-20mA → 0..250°C lineer dönüşüm *)
VAR
    fbScale : LIN_TRAFO;
    rTempC  : REAL;
END_VAR

fbScale(
    IN     := rRawCurrent,     (* ölçülen mA *)
    IN_MIN := 4.0,
    IN_MAX := 20.0,
    OUT_MIN:= 0.0,
    OUT_MAX:= 250.0
);
rTempC := fbScale.OUT;
```

> Not: Saf, durumsuz lineer ölçekleme için kendi `FC_ScaleAnalog` Function'ınız da uygundur (programming/01). LIN_TRAFO hazır ve okunaklıdır; ekip tercihine göre seçin.

### Örnek 2: R_TRIG ile Tek-Atımlık Buton

```iecst
VAR
    fbResetEdge : R_TRIG;
END_VAR

fbResetEdge(CLK := GVL_HMI.xResetButton);
IF fbResetEdge.Q THEN          (* yalnızca basış anında bir scan *)
    GVL_Alarms.xFaultLatch := FALSE;
END_IF
```

### Örnek 3: BLINK ile Durum Lambası + HYSTERESIS ile Kararlı Eşik

```iecst
VAR
    fbWarnLamp : BLINK;
    fbLevelHys : HYSTERESIS;
END_VAR

(* Uyarı lambası 500ms aç / 500ms kapa *)
fbWarnLamp(ENABLE := xWarning, TIMELOW := T#500MS, TIMEHIGH := T#500MS);
GVL_IO.xWarnLamp := fbWarnLamp.OUT;

(* Histerezisli seviye eşiği — gürültüde titremesin *)
fbLevelHys(IN := rLevel, HIGH := 80.0, LOW := 75.0);
(* IN 80'i geçince TRUE, 75'in altına inene dek TRUE kalır *)
```

### Örnek 4: Util.PID ile Sıcaklık Kontrolü

```iecst
VAR
    fbPID : PID;
END_VAR

fbPID(
    ACTUAL    := rTempActual,
    SET_POINT := rTempSetpoint,
    KP        := 2.0,
    TN        := 120.0,           (* integral süresi, s *)
    TV        := 10.0,            (* türev süresi, s *)
    Y_MANUAL  := 0.0,
    Y_OFFSET  := 0.0,
    Y_MIN     := 0.0,
    Y_MAX     := 100.0,
    MANUAL    := FALSE,
    RESET     := FALSE,
    CYCLE     := T#1S             (* task periyoduyla eşleşmeli *)
);
GVL_IO.rHeaterPower := fbPID.Y;
```

> [DOĞRULANMADI — Util.PID giriş adları sürümler arasında küçük farklılık gösterebilir; hedef sürümün PID dokümanından parametre adlarını teyit edin.]

## Sık Yapılan Hatalar

### Hata 1: Timer/Sayaç/Trigger'ı Koşullu Çağırmak

```iecst
(* ❌ IF içinde çağrı → .ET/.CV donar *)
IF xMode THEN tDelay(IN := xStart, PT := T#5S); END_IF
(* ✅ koşulsuz çağır, IN ile kontrol et *)
tDelay(IN := xStart AND xMode, PT := T#5S);
```

### Hata 2: PID Cycle Time'ı Yanlış Vermek

PID'e gerçek task periyodundan farklı CYCLE vermek, I ve D terimlerini yanlış ölçeklendirir → kararsız ya da çok yavaş kontrol. CYCLE = task periyodu olmalı; sabit ve güvenli istiyorsanız `PID_FIXCYCLE`.

### Hata 3: Hazır Blok Varken Kendi Versiyonunu Yazmak

Kendi TON/edge/scaling bloğunuzu yazmak, test edilmemiş, taşınamayan kod üretir. Standard/Util blokları IEC standardıdır ve her platformda aynı davranır; önce kütüphaneye bakın.

### Hata 4: R_TRIG'i Her Scan Çağırmamak

R_TRIG kenarı "iki ardışık çağrı arasındaki" değişimle algılar. Atlanan scan'lerde kenar kaçabilir veya gecikebilir. Her scan çağırın.

### Hata 5: Aynı Trigger Instance'ını Birden Çok Sinyale Kullanmak

```iecst
(* ❌ tek R_TRIG'i iki ayrı CLK ile çağırmak — iç durumu paylaşır, hatalı *)
(* ✅ her sinyale ayrı instance *)
fbEdgeA(CLK := xA);
fbEdgeB(CLK := xB);
```

### Hata 6: REAL Ölçekleme Sonucunu Eşitlikle Kontrol Etmek

LIN_TRAFO/CHARCURVE REAL döndürür; `= ` ile karşılaştırma float hatası yüzünden tutmaz (advanced/02 Hata 4). Eşik/tolerans kullanın.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Standard/Util Kütüphanesini Kullanın

- Zamanlama, sayma, kenar algılama, latch → her zaman Standard (kendin yazma).
- Lineer ölçekleme, karakteristik eğri, rampa → Util.LIN_TRAFO/CHARCURVE/RAMP.
- Basit PID kontrolü → Util.PID / PID_FIXCYCLE (gelişmiş kontrol gerekene dek yeterli).
- Yanıp sönen sinyal, dalga üreteci, frekans ölçümü → Util.BLINK/GEN/FREQ_MEASURE.
- Bit/BCD/Gray dönüşümleri, histerezis, limit alarm → Util.

### Kendi Bloğunuzu Yazın / Başka Kütüphane Kullanın

- Util.PID gelişmiş özellik (anti-windup ayrıntısı, gain scheduling, kaskad) yetersizse → özel kontrol FB'si veya üreticinin gelişmiş kontrol kütüphanesi.
- Util bloğunun arayüzü projeye uymuyorsa → ince bir sarmalayıcı (wrapper) FB ile kendi arayüzünüzü dayatın, içeride Util'i çağırın.
- Çok özel/donanıma-bağlı G/Ç davranışı → IoStandard yerine üretici kütüphanesi.

## Gerçek Proje Notları

**Not 1 — "Kendi TON'umuzu Yazdık" Felaketi**
Bir ekip taşınabilirlik kaygısıyla kendi `FB_Timer`'ını yazdı; sistem saatine bağlı ince bir hata vardı, bazı task periyotlarında 1 scan kayıyordu. Aylarca fark edilmedi. Standard.TON'a dönülünce sorun yok oldu. Ders: IEC standart bloklarını yeniden yazmak, taşınabilirlik kazandırmaz; aksine test edilmemiş risk ekler.

**Not 2 — PID Cycle Time Uyumsuzluğu**
Util.PID 10ms task'ta çalışıyordu ama CYCLE parametresine `T#1S` verilmişti (kopyala-yapıştır artığı). Kontrol absürt yavaştı; saatlerce "PID bozuk" diye arandı. CYCLE task periyoduna eşitlenince düzeldi. Ders: PID cycle time hatası sessizdir ve davranışı tamamen bozar; her PID devreye almasında ilk kontrol budur.

**Not 3 — CHARCURVE ile Doğrusal Olmayan Sensör**
Bir NTC sıcaklık sensörü doğrusal değildi; LIN_TRAFO yanlış sonuç verdi. CHARCURVE'e sensörün gerçek eğri noktaları girilince doğru lineerizasyon sağlandı. Ders: sensör doğrusal değilse LIN_TRAFO değil CHARCURVE; ikisini karıştırmak sessiz ölçüm hatası verir.

**Not 4 — HYSTERESIS ile Titreme Çözümü**
Bir seviye anahtarı tam eşikte gürültüden ötürü pompayı saniyede onlarca kez aç-kapa yapıyordu (röle aşınması). `HYSTERESIS` (HIGH/LOW bandı) eklenince çevirme durdu. Ders: eşik geçişlerinde ham karşılaştırma yerine histerezis kullanın; Util zaten sunuyor.

**Not 5 — R_TRIG Paylaşımı Hatası**
Bir geliştirici tek R_TRIG instance'ını bir döngü içinde farklı sinyaller için çağırdı; kenar algılamaları birbirine karıştı. Her sinyale ayrı instance (veya `ARRAY OF R_TRIG`) ile çözüldü. Ders: trigger/timer durumu instance'a özeldir; paylaşmak iç durumu bozar (programming/01 instance modeli).

## İlgili Konular

```
knowledge/codesys/libraries/
├── _synthesis.md               → Kütüphane stratejisi sentezi (kullan vs yaz vs sarmala)
└── 02_library_management.md    → Bu kütüphaneleri yönetme: sürüm, placeholder

knowledge/codesys/programming/
├── 03_function_blocks.md       → FB instance, her-scan-çağrı (TON/R_TRIG kuralı)
└── 01_pou_types.md             → Function vs FB (kendi ölçekleme Function'ı)

knowledge/codesys/fundamentals/
└── 03_iec61131_languages.md    → Bu blokların FBD/LD/ST'de kullanımı

knowledge/codesys/advanced/
└── 02_state_machines_sfc.md    → Timer'ları state machine içinde doğru çağırma
```
