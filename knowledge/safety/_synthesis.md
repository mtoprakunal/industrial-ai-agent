---
KONU        : Fonksiyonel Emniyet — Üst Sentez
KATEGORİ    : safety
ALT_KATEGORI: synthesis
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://en.wikipedia.org/wiki/Safety_integrity_level"
    başlık: "Safety Integrity Level — Wikipedia (IEC 61508 SIL/PFD/PFH tabloları)"
    güvenilirlik: topluluk
  - url: "https://en.wikipedia.org/wiki/ISO_13849"
    başlık: "ISO 13849 — Wikipedia (PL, Kategori, MTTFd/DC/CCF)"
    güvenilirlik: topluluk
  - url: "https://webstore.iec.ch/en/publication/5515"
    başlık: "IEC 61508 — Functional safety of E/E/PE safety-related systems (IEC resmi)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "knowledge/safety/01_sil_pl_standards.md"
    ilişki: detaylandırır
  - konu: "knowledge/safety/02_safety_plc_and_io.md"
    ilişki: detaylandırır
  - konu: "knowledge/safety/03_safe_motion.md"
    ilişki: detaylandırır
  - konu: "knowledge/safety/04_estop_and_safety_circuits.md"
    ilişki: detaylandırır
  - konu: "agent/safety_principles.md"
    ilişki: gerektirir
  - konu: "knowledge/standards/02_iec62443.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "PLC, sensör, aktüatör ve donanım/yazılım ayrımı temel kavramları"
  - "agent/safety_principles.md ilkelerinin okunmuş olması"
ÇELİŞKİLER :
  - kaynak: "Safety (emniyet) vs Security (siber güvenlik) — aynı şey mi?"
    konu: "Functional safety (IEC 61508 ailesi) ile cyber security (IEC 62443) farklı eksenlerdir"
    çözüm: >
      Safety: insanı/çevreyi makinenin fiziksel tehlikesinden korur (rastgele donanım
      arızası + sistematik hata). Security: sistemi kötü niyetli erişimden korur.
      Modern sistemlerde örtüşürler (güvenlik açığı bir emniyet fonksiyonunu devre dışı
      bırakabilir) ama birbirinin yerine geçmez. Bu belge ailesi SAFETY'ye odaklanır;
      security için knowledge/standards/02_iec62443.md.
  - kaynak: "Yazılım emniyeti garanti eder mi?"
    konu: "PLC kodunun emniyet fonksiyonunu üstlenip üstlenemeyeceği"
    çözüm: >
      HAYIR. Standart PLC yazılımı emniyeti GARANTİ ETMEZ; destekler. Garanti, sertifikalı
      donanımsal emniyet zincirinden (emniyet rölesi / Safety PLC + donanımsal STO) gelir.
      Bu, agent/rules.json safety.principle ile birebir aynı duruştur.
---

## Özün Ne

Fonksiyonel emniyet (functional safety), bir makinenin veya prosesin tehlikeli bir arıza durumunda **insanı ve çevreyi korumak** için tasarlanmış sistemlerin disiplinidir. Temel sorusu basittir: "Bir şey bozulduğunda sistem güvenli tarafa mı düşüyor?" Bu disiplin, IEC 61508 (jenerik temel standart) etrafında örgütlenmiş bir standartlar ailesiyle (makine için IEC 62061 + ISO 13849, proses için IEC 61511, sürücüler için IEC 61800-5-2) yönetilir.

Bu belge ailesinin değişmez tezi — ki `agent/safety_principles.md` ve `agent/rules.json` içindeki `safety.principle` ile birebir aynıdır — şudur: **Emniyet, yazılım mantığına bağımlı olamaz.** Bir CODESYS programı, bir IF/THEN bloğu veya bir state machine emniyeti *destekler* ama *garanti etmez*. Garanti, sertifikalı donanımsal emniyet zincirinden gelir: emniyet rölesi, Safety PLC, donanımsal STO girişi, zorla yönlendirmeli (force-guided) kontaklar. Standart PLC bu sinyalleri *okuyabilir* (HMI'da durum göstermek için) ama emniyet fonksiyonunu *üstlenemez*.

## Nasıl Çalışır

### Emniyetin İki Düşmanı: Rastgele ve Sistematik Hatalar

Fonksiyonel emniyet iki farklı arıza türüyle savaşır:

```
RASTGELE DONANIM ARIZASI (Random Hardware Failure)
  Neden : Bileşen yaşlanması, fiziksel bozulma (kondansatör kuruması, röle yapışması)
  Doğa  : Olasılıksal — ne zaman olacağı tahmin edilemez, ama ORANI hesaplanabilir
  Ölçüm : PFD / PFH (aşağıda), MTTFd, FIT
  Savunma: Redundancy (çift kanal), diyagnostik, periyodik test

SİSTEMATİK HATA (Systematic Failure)
  Neden : Tasarım/spesifikasyon/yazılım hatası (yanlış kod, eksik gereksinim)
  Doğa  : Deterministik — aynı koşulda HER ZAMAN tekrarlanır
  Ölçüm : Sayısal değil; SÜREÇ kalitesiyle (yaşam döngüsü, V-model, doğrulama)
  Savunma: Geliştirme süreci disiplini, bağımsız doğrulama, kanıtlanmış bileşen
```

Önemli ders: **Yazılım hataları her zaman sistematiktir.** Bir kod hatasını "olasılıkla" azaltamazsınız; ya vardır ya yoktur. Bu yüzden emniyet, yazılımın doğruluğuna bel bağlayamaz — donanımsal, basit, kanıtlanmış bir zincire dayanır. Bu doğrudan agent ilkesidir.

### Emniyet Fonksiyonu (Safety Function) Kavramı

Emniyet, soyut bir "güvenli olma" değil, somut **emniyet fonksiyonlarının** toplamıdır. Bir emniyet fonksiyonu üç parçalı bir zincirdir:

```
ALGILA  →  KARAR VER  →  EYLEME GEÇ
(Sensor)   (Logic)       (Actuator)

Örnek: "Koruma kapısı açılırsa motor torku 100 ms içinde kesilir"
  Algıla   : Kapı anahtarı (güvenli, zorla açma kontaklı)
  Karar    : Emniyet rölesi / Safety PLC
  Eyleme   : Kontaktör açılır VEYA sürücü STO tetiklenir → motor enerjisiz
```

Bir emniyet fonksiyonunun bütünlüğü, zincirin **en zayıf halkası** kadardır. Sensörü SIL 3, mantığı SIL 3 ama aktüatörü SIL 1 ise, fonksiyon SIL 1'dir. Bu yüzden emniyet bir uçtan-uca (sensör→aktüatör) tasarım problemidir.

### SIL ve PL: Emniyetin "Ne Kadar Güvenilir" Ölçüsü

Bir emniyet fonksiyonunun ne kadar güvenilir olduğunu iki paralel ölçek tanımlar:

| Ölçek | Standart | Aralık | Bağlam |
|-------|----------|--------|--------|
| **SIL** (Safety Integrity Level) | IEC 61508 / 61511 / 62061 | 1 → 4 (4 en yüksek) | Jenerik, proses, makine elektronik |
| **PL** (Performance Level) | ISO 13849-1 | a → e (e en yüksek) | Makine emniyeti (mekanik + elektronik) |

Bu iki ölçek aynı fiziksel büyüklüğe — saatte tehlikeli arıza olasılığına (PFH) — dayanır; yalnızca etiketleri farklıdır. Detaylar ve eşik değerleri `01_sil_pl_standards.md` içindedir. Burada kritik üst-mesaj: **Yüksek SIL/PL ne kadar yazılım yazarsanız yazın elde edilmez; donanım mimarisinden (kanal sayısı, diyagnostik, bileşen kalitesi) gelir.**

### Risk Temelli Karar: Emniyet Fonksiyonu Ne Zaman Gerekir?

Emniyet bir lüks değil, risk değerlendirmesinin **çıktısıdır**. Akış:

```
1. Tehlike tanımla     → Makine ne ile zarar verebilir? (ezme, kesme, sıkışma, elektrik, sıcaklık)
2. Riski değerlendir   → Şiddet (S) × Maruz kalma (F) × Önleme olasılığı (P)
3. Gerekli seviye      → Risk grafiği → PLr (gerekli PL) veya SIL hedefi
4. Önlem tasarla       → PLr'yi karşılayan emniyet fonksiyonu (mimari + bileşen)
5. Doğrula             → Gerçekleşen PL ≥ PLr mi? (hesap + test)
```

Bu, `agent/rules.json` içindeki **teslim öncesi emniyet sorusunun** mühendislik karşılığıdır: *"Bu sistemde tek bir yazılım hatası birini yaralayabilir mi?"* — Cevap "evet" ise, o fonksiyon donanımsal emniyet zincirine taşınır ve risk değerlendirmesi (`risk_assessment_required: true`) belgeleninir.

## Pratikte Nasıl Kullanılır

### Bu Belge Ailesinin Haritası

```
knowledge/safety/
├── _synthesis.md                  → (bu belge) üst kavramlar, agent ilkeleriyle bağ
├── 01_sil_pl_standards.md         → SIL/PL/Kategori, PFD/PFH, risk değerlendirme
├── 02_safety_plc_and_io.md        → Safety PLC, çift kanal, F-modülleri, safety fieldbus
├── 03_safe_motion.md              → IEC 61800-5-2: STO/SS1/SS2/SLS/SOS/SDI, SV660N STO
└── 04_estop_and_safety_circuits.md→ E-stop, stop kategorileri, ışık perdesi, emniyet rölesi
```

### Karar Sırası (Bir Makine İçin)

1. **Risk değerlendir** → tehlike başına PLr/SIL hedefi belirle (`01`).
2. **Mimari seç** → hedef PLr'yi karşılayan Kategori ve kanal sayısı (`01`, `02`).
3. **Bileşen seç** → sertifikalı emniyet rölesi mi, Safety PLC mi (`02`).
4. **Hareket varsa** → sürücü STO + uygun safe motion fonksiyonu (`03`).
5. **Operatör arabirimi** → E-stop, ışık perdesi, kapı kilidi, reset mantığı (`04`).
6. **Doğrula ve belgele** → gerçekleşen PL ≥ PLr; risk değerlendirme raporu.

## Örnekler

### Örnek: Bir Hareket Fonksiyonunun Emniyet Zinciri (SV660N bağlamı)

```
Senaryo: EtherCAT hattında SV660N servo süren bir eksen; koruma kapısı korumalı.

Tehlike      : Açık kapıda dönen mil → el sıkışması/kesme (S yüksek)
Risk hedefi  : PL d / SIL 2 (tipik makine ekseni)
Emniyet fonk.: "Kapı açılırsa motor torku kesilir (STO)"

Zincir:
  Kapı anahtarı (zorla açma) → Emniyet rölesi / Safety PLC
       → SV660N STO1 + STO2 girişleri (çift kanal, donanımsal)
       → PWM bloke → motor enerjisiz (tork yok)

Standart CODESYS PLC'nin rolü:
  ✓ STO durumunu OKUR, HMI'da gösterir, kontrollü duruşu (MC_Stop) yönetir
  ✗ STO'yu TETİKLEMEZ — bu donanımsal emniyet zincirinin işi (agent ilkesi)
```

Bu örnek, dört belgenin nasıl birleştiğini gösterir: risk (`01`), Safety PLC/röle (`02`), STO (`03`), kapı/E-stop devresi (`04`).

## Sık Yapılan Hatalar

### Hata 1: "Kodda Kontrol Ederim" Yanılgısı
Bir CODESYS programına `IF KapiAcik THEN MotorKomut := FALSE` yazıp emniyeti sağladığını sanmak. Bu yalnızca **fonksiyonel** kontroldür; CPU donar, watchdog atlar veya değişken bozulursa motor durmaz. Emniyet, yazılımdan **bağımsız** donanımsal zincir gerektirir (`safety_io_on_standard_modules_forbidden`).

### Hata 2: SIL/PL'yi Bir Cihaz Etiketi Sanmak
"Bu sürücü SIL 3" demek, sürücünün STO fonksiyonunun SIL 3 *kapasitesi* (capability) olduğu anlamına gelir — sistemin SIL 3 olduğu değil. Sistem SIL'i, zincirin tamamının (sensör + mantık + aktüatör) ortak hesabıdır.

### Hata 3: Safety ile Security'yi Karıştırmak
IEC 62443 (siber güvenlik) bir emniyet standardı değildir; IEC 61508 ailesi (emniyet) bir güvenlik standardı değildir. Birbirini tamamlarlar ama biri diğerini karşılamaz.

### Hata 4: Fail-Safe Yönünü Yanlış Tasarlamak
Aktüatörü "sinyal gelince dur" diye tasarlamak yanlıştır; "sinyal kesilince dur" doğrudur. Güç/sinyal kaybı *güvenli yöne* düşmelidir (yay-geri valf, normalde-kapalı kontaktör). `agent/rules.json`: `fail_safe_default_is_stop_not_run`.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Emniyet Fonksiyonu Gerektiğinde (Zorunlu)
- Risk değerlendirmesi PLr ≥ a (yani herhangi bir kişisel yaralanma riski) çıkardığında.
- İnsan ile makinenin tehlikeli bölgesinin fiziksel olarak kesişebildiği her durumda.
- Yasal/normatif zorunluluk olduğunda (CE — Makine Direktifi 2006/42/EC).

### Aşırıya Kaçılmamalı
- Her sinyale SIL 3 hedeflemek maliyeti üstel artırır ve gereksizdir; risk neyse seviye odur.
- Emniyet fonksiyonu, **risk değerlendirmesinin çıktısı** olmalı — "ne olur ne olmaz" diye eklenen değil.

## Gerçek Proje Notları

**Not 1 — Emniyet, projenin ilk gününde başlar.** Risk değerlendirmesi tasarım sonuna bırakılırsa, emniyet zinciri sonradan "yamanır": ek kontaktör, ek kablo, mimari değişikliği. FEED/konsept aşamasında PLr belirlenirse mimari baştan doğru kurulur. Bu, IEC 62443'teki "greenfield Zone tasarımı" dersiyle aynıdır.

**Not 2 — En tehlikeli cümle: "Yazılımda hallederiz."** Bir müşteri, donanımsal E-stop maliyetinden kaçmak için "PLC kodu motoru durdursun yeter" dedi. Bu hem yasadışı (CE) hem ölümcül. Standart PLC durdurmayı *yönetebilir* ama *garanti edemez*. Emniyet rölesi + STO eklendi; maliyet farkı, tek bir kaza maliyetinin yanında ihmal edilebilirdi.

**Not 3 — STO her şeyi çözmez.** STO motoru enerjisiz bırakır (Stop Kategori 0) ama dikey eksende yük *düşebilir* (yerçekimi). Orada STO yerine kontrollü duruş (SS1) + mekanik fren (SBC) gerekir. Emniyet fonksiyonu seçimi tehlikeye göre yapılır; "STO koyduk, tamam" yanılgısı saha kazalarının kaynağıdır (bkz. `03_safe_motion.md`).

**Not 4 — Emniyet ve standart mantık ayrı yaşamalı.** Safety PLC ile standart PLC aynı kasada olabilir ama emniyet mantığı standart taskla *karışmaz*. Karıştığı projelerde, standart kodun bir değişikliği emniyet doğrulamasını geçersiz kıldı ve baştan validasyon gerekti. Ayrık tutmak hem güvenli hem ucuzdur (bkz. `02_safety_plc_and_io.md`).

## İlgili Konular

```
knowledge/safety/
├── 01_sil_pl_standards.md          → SIL/PL eşikleri, PFD/PFH, risk grafiği
├── 02_safety_plc_and_io.md         → Safety PLC mimarisi, safety fieldbus
├── 03_safe_motion.md               → IEC 61800-5-2, STO/SS1/SLS, SV660N
└── 04_estop_and_safety_circuits.md → E-stop, stop kategorileri, ışık perdesi

agent/
├── safety_principles.md            → Davranışsal emniyet ilkeleri (bu ailenin temeli)
└── rules.json (safety bölümü)      → İhlal edilemez kurallar

knowledge/standards/02_iec62443.md  → Siber güvenlik (safety ≠ security, tamamlar)
knowledge/inovance/inoproshop/06_motion_control.md → SV660N STO pratik notu
```
