---
KONU        : SIL, PL ve Kategori — IEC 61508 / IEC 62061 / ISO 13849
KATEGORİ    : safety
ALT_KATEGORI: standards
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://en.wikipedia.org/wiki/Safety_integrity_level"
    başlık: "Safety Integrity Level — Wikipedia (IEC 61508 PFD/PFH tabloları)"
    güvenilirlik: topluluk
  - url: "https://en.wikipedia.org/wiki/ISO_13849"
    başlık: "ISO 13849 — Wikipedia (PL, Kategori, MTTFd/DC/CCF)"
    güvenilirlik: topluluk
  - url: "https://www.sick.com/us/en/what-are-performance-levels/w/blog-safety-standard-performance-levels"
    başlık: "What are Performance Levels? — SICK (PL bantları)"
    güvenilirlik: topluluk
  - url: "https://www.iso.org/obp/ui/en/#!iso:std:73481:en"
    başlık: "ISO 13849-1:2023 — ISO resmi (PL, Kategori, Annex K)"
    güvenilirlik: resmi
  - url: "https://webstore.iec.ch/en/publication/5515"
    başlık: "IEC 61508 — IEC resmi (SIL, PFD/PFH tabloları)"
    güvenilirlik: resmi
  - url: "https://andersoncontrol.com/performance-level-vs-safety-integrity-level/"
    başlık: "Performance Level vs Safety Integrity Level — Anderson Controls (PL↔SIL)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/safety/_synthesis.md"
    ilişki: detaylandırır
  - konu: "knowledge/safety/02_safety_plc_and_io.md"
    ilişki: tamamlar
  - konu: "knowledge/safety/04_estop_and_safety_circuits.md"
    ilişki: tamamlar
  - konu: "agent/safety_principles.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "knowledge/safety/_synthesis.md (emniyet fonksiyonu, rastgele/sistematik hata)"
  - "Olasılık ve oran (rate) kavramlarına temel aşinalık"
ÇELİŞKİLER :
  - kaynak: "PL ve SIL aynı mı, birebir dönüşür mü?"
    konu: "ISO 13849 PL ile IEC 61508/62061 SIL arasındaki ilişki"
    çözüm: >
      Aynı fiziksel büyüklüğe (PFH) dayanırlar ama BİREBİR ÖZDEŞ DEĞİLDİR.
      Pratik karşılık: PL a → (SIL yok), PL b ve PL c → SIL 1, PL d → SIL 2,
      PL e → SIL 3. PL'de SIL 4 karşılığı yoktur (makine emniyeti SIL 4'e çıkmaz;
      SIL 4 proses/IEC 61511 alanıdır). Sınır değerlerde Annex K tablosu esas alınır.
  - kaynak: "IEC 62061 vs ISO 13849 — hangisini kullanmalı?"
    konu: "İki makine emniyeti standardının kapsam farkı"
    çözüm: >
      ISO 13849: her teknoloji (mekanik, hidrolik, pnömatik, elektronik) + basitleştirilmiş
      Kategori/PL yöntemi. IEC 62061: yalnızca E/E/PE (elektrik/elektronik/programlanabilir),
      karmaşık programlanabilir sistemler için daha derin. Karmaşık SRP/CS yoksa ISO 13849
      pratiktir; programlanabilir emniyet mantığı ağırlıktaysa IEC 62061 uygundur. 2021
      sonrası iki standart uyumlandırıldı (PL↔SIL karşılığı netleştirildi).
---

## Özün Ne

SIL ve PL, bir emniyet fonksiyonunun **ne kadar güvenilir** olduğunu sayısal olarak ifade eden ölçeklerdir. İkisi de aynı temel büyüklüğe dayanır: bir emniyet fonksiyonunun **saatte tehlikeli arıza olasılığı (PFH)** veya **talep başına tehlikeli arıza olasılığı (PFD)**. SIL (Safety Integrity Level) IEC 61508 ailesinden gelir ve 1–4 arası kademelenir; PL (Performance Level) ISO 13849-1'den gelir ve a–e arası kademelenir. Ayrıca ISO 13849, mimariyi tanımlamak için **Kategori (B, 1, 2, 3, 4)** kavramını kullanır.

Bu belgenin kritik mesajı `agent/safety_principles.md` ile aynıdır: **Yüksek SIL/PL, yazılımdan değil, donanım mimarisinden gelir** — kanal sayısı (redundancy), diyagnostik kapsamı (DC), bileşen güvenilirliği (MTTFd) ve ortak nedenli arızaya (CCF) karşı önlemler. Bu belgedeki tüm sayısal eşikler resmi/birincil kaynaklarla doğrulanmıştır; doğrulanamayanlar [DOĞRULANMADI] ile işaretlenmiştir.

## Nasıl Çalışır

### Standart Ailesi — Kim Neyi Kapsar?

```
IEC 61508  → JENERIK TEMEL (tüm E/E/PE emniyet sistemleri). "Ana standart."
   ├── IEC 61511    → Proses endüstrisi (kimya, petrol, rafineri) — SIS, SIF
   ├── IEC 62061    → Makine emniyeti (elektrik/elektronik/programlanabilir kontrol)
   └── IEC 61800-5-2→ Güç tahrik sistemleri / sürücüler (STO, SS1...) → bkz. 03_safe_motion.md

ISO 13849-1 → MAKINE emniyeti (her teknoloji: mekanik+hidrolik+pnömatik+elektronik)
              Kategori + PL yöntemi. IEC 62061 ile uyumlandırılmıştır.
```

Sektör seçimi:
- **Proses tesisi** (tank, reaktör, yakıcı) → IEC 61511 (SIL diliyle).
- **Makine** (konveyör, pres, robot, paketleme) → ISO 13849 (PL) veya IEC 62061 (SIL).
- **Sürücü/servo** (SV660N gibi) → IEC 61800-5-2 (safe motion fonksiyonları), genelde ISO 13849/IEC 62061 sistemine bağlanır.

### Talep Modu: Low Demand vs High Demand/Continuous

SIL'in ölçü birimi, emniyet fonksiyonunun **ne sıklıkla çağrıldığına** bağlıdır:

```
LOW DEMAND (düşük talep)        → metrik: PFD (Probability of Failure on Demand)
  Fonksiyon yılda <1 kez çağrılır (ör. acil kapatma — nadiren olur)
  "İhtiyaç anında çalışmama olasılığı"

HIGH DEMAND / CONTINUOUS        → metrik: PFH (Probability of dangerous Failure per Hour)
  Fonksiyon sık veya sürekli aktif (ör. ışık perdesi, hız izleme)
  "Saat başına tehlikeli arıza olasılığı"   [birim: 1/saat]
```
Kaynak: [Wikipedia — Safety Integrity Level](https://en.wikipedia.org/wiki/Safety_integrity_level)

Makine emniyetinde fonksiyonlar genelde high-demand'dir (operatör sık sık kapı açar, ışık perdesini keser) → **PFH** kullanılır. PL de PFH tabanlıdır; bu yüzden PL ile high-demand SIL doğrudan karşılaştırılabilir.

### SIL Eşik Değerleri (IEC 61508) — DOĞRULANMIŞ

**Low Demand — PFD (talep başına ortalama tehlikeli arıza olasılığı):**

| SIL | PFD aralığı | Üs gösterimi |
|-----|-------------|--------------|
| SIL 1 | 0.1 – 0.01 | ≥10⁻² ... <10⁻¹ |
| SIL 2 | 0.01 – 0.001 | ≥10⁻³ ... <10⁻² |
| SIL 3 | 0.001 – 0.0001 | ≥10⁻⁴ ... <10⁻³ |
| SIL 4 | 0.0001 – 0.00001 | ≥10⁻⁵ ... <10⁻⁴ |

**High Demand / Continuous — PFH (saatte tehlikeli arıza olasılığı, 1/saat):**

| SIL | PFH aralığı | Üs gösterimi |
|-----|-------------|--------------|
| SIL 1 | 0.00001 – 0.000001 | ≥10⁻⁶ ... <10⁻⁵ |
| SIL 2 | 0.000001 – 0.0000001 | ≥10⁻⁷ ... <10⁻⁶ |
| SIL 3 | 0.0000001 – 0.00000001 | ≥10⁻⁸ ... <10⁻⁷ |
| SIL 4 | 0.00000001 – 0.000000001 | ≥10⁻⁹ ... <10⁻⁸ |

Kaynak: [Wikipedia — Safety Integrity Level (IEC 61508 Tablo 2 ve 3)](https://en.wikipedia.org/wiki/Safety_integrity_level). Not: Her SIL bir oran *aralığıdır*; tek bir değer değildir.

### PL Eşik Değerleri (ISO 13849-1, Annex K) — DOĞRULANMIŞ

PL yalnızca PFHd (saatte tehlikeli arıza olasılığı) ile ifade edilir:

| PL | PFHd aralığı (1/saat) |
|----|------------------------|
| **PL a** | ≥10⁻⁵ ... <10⁻⁴ |
| **PL b** | ≥3×10⁻⁶ ... <10⁻⁵ |
| **PL c** | ≥10⁻⁶ ... <3×10⁻⁶ |
| **PL d** | ≥10⁻⁷ ... <10⁻⁶ |
| **PL e** | ≥10⁻⁸ ... <10⁻⁷ |

Kaynak: [Wikipedia — ISO 13849](https://en.wikipedia.org/wiki/ISO_13849) (PL a <10⁻⁴, PL e ≥10⁻⁸ teyit), bant sınırları topluluk kaynaklarıyla (PL b 3×10⁻⁶ sınırı) tutarlı; kesin doğrulama için ISO 13849-1:2023 Annex K Tablo K.1. PL bantlarında ISO ±%5 tolerans tanır.

### PL ↔ SIL Karşılığı — DOĞRULANMIŞ (birebir değil!)

PL ve SIL aynı PFH eksenine oturduğu için karşılaştırılabilir, ama özdeş değildir:

| PL (ISO 13849) | SIL karşılığı (IEC 62061) | PFH bandı (yaklaşık) |
|----------------|----------------------------|-----------------------|
| PL a | (SIL yok) | 10⁻⁵ ... 10⁻⁴ |
| PL b | SIL 1 | 3×10⁻⁶ ... 10⁻⁵ |
| PL c | SIL 1 | 10⁻⁶ ... 3×10⁻⁶ |
| PL d | SIL 2 | 10⁻⁷ ... 10⁻⁶ |
| PL e | SIL 3 | 10⁻⁸ ... 10⁻⁷ |

Kaynak: [Anderson Controls — PL vs SIL](https://andersoncontrol.com/performance-level-vs-safety-integrity-level/) — "PL b ve PL c → SIL 1; PL d → SIL 2; PL e → SIL 3". Önemli: Makine emniyetinde **SIL 4 / PL üstü yoktur**; SIL 4 proses (IEC 61511) alanına özgüdür. Sınır değerlerde her zaman Annex K tablosu esas alınır, kabaca dönüşüm değil.

### Kategori (ISO 13849) — Mimari Sınıfları — DOĞRULANMIŞ

Kategori, emniyet zincirinin **donanım mimarisini** tanımlar. PL'yi belirleyen en büyük faktör budur:

| Kategori | Yapı | Arıza davranışı | Maks. PL |
|----------|------|------------------|----------|
| **B** | Tek kanal | Arıza fonksiyon kaybına yol açabilir | b |
| **1** | Tek kanal | Kanıtlanmış bileşen + kanıtlanmış güvenlik ilkesi | c |
| **2** | Tek kanal + periyodik test | Test arızayı bulur (ama test anları arası açık) | d |
| **3** | Çift kanal (redundant) | Tek arıza fonksiyon kaybına yol açmaz | e |
| **4** | Çift kanal + yüksek diyagnostik | Tek arıza yol açmaz + arıza birikmeden tespit | e |

Kaynak: [Wikipedia — ISO 13849 (Kategori tablosu)](https://en.wikipedia.org/wiki/ISO_13849).

Kritik gözlem: **PL d ve PL e için çift kanal (Kategori 3/4) pratik olarak zorunludur.** Tek kanallı bir devre (Kategori B/1) yüksek PL veremez — bu, agent ilkesi "emniyet redundant donanım zinciri ister"in sayısal kanıtıdır.

### MTTFd, DC, CCF: PL'yi Belirleyen Üç Parametre

ISO 13849'da bir kanalın PL'si üç girdiden hesaplanır:

```
MTTFd (Mean Time To dangerous Failure)  → bileşen güvenilirliği (yıl)
   Düşük: 3–10 yıl | Orta: 10–30 yıl | Yüksek: 30–100 yıl

DCavg (Diagnostic Coverage)             → diyagnostiğin yakaladığı arıza yüzdesi
   Yok: <60% | Düşük: 60–90% | Orta: 90–99% | Yüksek: ≥99%

CCF (Common Cause Failure)              → ortak nedenli arızaya karşı önlem
   Kategori 2/3/4 için min. 65 puan (Annex F kontrol listesi) zorunlu
```
Kaynak: [Wikipedia — ISO 13849](https://en.wikipedia.org/wiki/ISO_13849). Hesap mantığı: Kategori (mimari) + MTTFd (güvenilirlik) + DCavg (diyagnostik) birlikte, Annex K eğrisi üzerinden PL'yi verir. CCF, redundant kanalların *aynı anda aynı nedenle* bozulmasını engeller — çift kanalı anlamlı kılan şey budur.

## Pratikte Nasıl Kullanılır

### Risk Değerlendirme → Gerekli PL (PLr) Belirleme

ISO 13849, gerekli performans seviyesini (PLr — required PL) bir **risk grafiğiyle** belirler. Üç parametre:

```
S — Severity (Şiddet)          : S1 = hafif (geri dönüşlü) | S2 = ağır (geri dönüşsüz/ölüm)
F — Frequency/exposure (Maruz) : F1 = seyrek/kısa | F2 = sık/sürekli
P — Possibility of avoidance   : P1 = mümkün (yavaş, görülebilir) | P2 = neredeyse imkansız

Risk grafiği (ISO 13849-1 Şekil A.1 mantığı):
  S1-F1-P1 → PLr a
  S1...    → PLr b/c
  S2-F1-P1 → PLr c
  S2-F2-P2 → PLr e (en ağır)
```
Bu, `agent/rules.json` içindeki `risk_assessment_required: true` kuralının uygulanmasıdır. PLr belirlenmeden emniyet fonksiyonu tasarlanmaz.

### Doğrulama Koşulu

Tasarım geçerli sayılır ancak şu sağlanırsa:

```
Gerçekleşen PL  ≥  PLr (gerekli PL)
```
Gerçekleşen PL, mimarinin (Kategori) + MTTFd + DCavg + CCF hesabıyla bulunur. IFA SISTEMA gibi ücretsiz araçlar bu hesabı yapar.

### Tipik Hedefler (Sektör Pratiği)

```
Düşük risk (hafif sıkışma, yavaş hareket)      → PL b / PL c  (SIL 1)
Tipik makine ekseni, koruma kapısı              → PL d         (SIL 2)
Ağır risk (pres, robot hücresi, hızlı bıçak)    → PL e         (SIL 3)
Proses ESD / yakıcı yönetimi                    → SIL 2–3 (IEC 61511, SIL 4 nadir)
```

## Örnekler

### Örnek 1: Kapı İzleme Fonksiyonunun PL Hesabı (kavramsal)

```
Fonksiyon: "Koruma kapısı açılırsa eksen torku kesilir"
Risk      : S2 (el sıkışması, ağır) F2 (sık erişim) P2 (kaçınılamaz) → PLr e

Tasarım:
  Mimari : Kategori 3 (çift kanallı kapı anahtarı + çift kanallı STO)
  MTTFd  : Yüksek (sertifikalı emniyet anahtarı + sürücü STO)
  DCavg  : Yüksek (çapraz izleme, STO geri besleme)
  CCF    : ≥65 puan (ayrı kablolama, farklı teknoloji)
  → Gerçekleşen PL = e   ✓  (PL e ≥ PLr e sağlanır)
```

### Örnek 2: SIL Aralığının Anlamı (sayısal sezgi)

```
Bir high-demand emniyet fonksiyonu SIL 2 ister → PFH 10⁻⁷ ... 10⁻⁶ /saat olmalı.
Yani: saat başına tehlikeli arıza olasılığı 1 milyonda 1 ile 10 milyonda 1 arası.
Bir yıl ≈ 8760 saat → yılda kabaca 10⁻³ ... 10⁻² tehlikeli arıza beklentisi mertebesi.
Daha düşük arıza isteniyorsa (SIL 3) → çift kanal + yüksek diyagnostik şarttır.
```

### Örnek 3: Yanlış ve Doğru İfade

```
❌ "Bu emniyet rölesi SIL 3, demek ki sistemim SIL 3."
✅ "Bu röle SIL 3 KAPASITELİ (capability). Sistem SIL'i = sensör + röle + aktüatör
    zincirinin ortak PFH hesabı. En zayıf halka belirler."
```

## Sık Yapılan Hatalar

### Hata 1: PFD ile PFH'yi Karıştırmak
Low-demand (PFD, birimsiz olasılık) ile high-demand (PFH, 1/saat) farklı birimlerdir. Bir makinenin ışık perdesi (sürekli aktif) için PFD kullanmak kavramsal hatadır; high-demand → PFH.

### Hata 2: Tek Kanalla Yüksek PL Beklemek
Kategori B/1 (tek kanal) ile PL d/e elde edilemez. Yüksek PL çift kanal (Kategori 3/4) gerektirir. Yazılım eklemek bunu değiştirmez (agent ilkesi).

### Hata 3: PL↔SIL'i Birebir Dönüştürmek
"PL d = SIL 2 her zaman" demek sınır değerlerde hatalıdır. Karşılık yaklaşıktır; sınırda Annex K tablosu esas alınır. Bkz. ÇELİŞKİLER bölümü.

### Hata 4: CCF'yi Atlamak
Çift kanal kurup ortak nedenli arızayı (ikisi de aynı güç kaynağından, aynı kablo kanalından) gözardı etmek redundancy'yi anlamsız kılar. Kategori 3/4 için CCF ≥65 puan zorunludur.

### Hata 5: Sistematik Hatayı Sayısalla Karıştırmak
PFD/PFH yalnızca **rastgele donanım** arızasını ölçer. Yazılım/tasarım (sistematik) hataları bu sayılarla *azaltılamaz*; yalnızca geliştirme süreci disipliniyle (yaşam döngüsü, doğrulama) yönetilir. SIL'in iki ayağı vardır: sayısal (PFH) + sistematik kabiliyet (SC).

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **ISO 13849 (PL):** Makinelerde, karışık teknolojide (mekanik+pnömatik+elektronik), basitleştirilmiş yöntem yeterliyse. En yaygın makine emniyeti yolu.
- **IEC 62061 (SIL):** Karmaşık programlanabilir emniyet mantığı ağırlıktaysa, daha derin gerekçe gerektiğinde.
- **IEC 61511 (SIL):** Proses endüstrisinde (SIS — Safety Instrumented System).
- **IEC 61508:** Bileşen/cihaz üreticisi için temel referans; sürücü STO sertifikasyonu (IEC 61800-5-2 ile birlikte) buna dayanır.

## Gerçek Proje Notları

**Not 1 — PLr'yi müşteriyle birlikte belirle, varsayma.** `agent/rules.json`: `ask_before_assuming_safety_requirement`. Risk grafiği parametreleri (S/F/P) makineyi tanıyan kişiyle netleştirilmeli; mühendis tek başına "herhalde PL d" diyemez. Yanlış PLr, ya tehlikeli (düşük) ya da pahalı (yüksek) sistem üretir.

**Not 2 — Sertifikalı bileşen, hesabı kısaltır.** Emniyet anahtarı, röle ve sürücünün STO'su sertifikalıysa (üreticinin PFHd/MTTFd/PL değerleri belgeliyse), SISTEMA hesabı bu hazır değerleri kullanır. Sertifikasız bileşenle MTTFd'yi kendin türetmek hem zor hem tartışmalıdır.

**Not 3 — SISTEMA dosyasını proje teslimine ekle.** Almanya/AB denetimlerinde PL hesabının SISTEMA (.spj) dosyası ve risk değerlendirme raporu birlikte istenir. Bu, IEC 62443'teki "Zone/Conduit dokümantasyonu" disiplinine paraleldir — emniyet de belgelenmeden tamamlanmaz (`risk_assessment_required`).

**Not 4 — PL e'yi gerekmedikçe hedefleme.** Bir paketleme makinesinde tüm fonksiyonlara PL e dayatıldı; maliyet ve devreye alma süresi katlandı. Risk değerlendirmesi çoğu fonksiyon için PL c/d'nin yeterli olduğunu gösterdi. Emniyet seviyesi riskten gelir, "ne olur ne olmaz"dan değil.

## İlgili Konular

```
knowledge/safety/
├── _synthesis.md                   → Emniyet fonksiyonu, rastgele/sistematik hata
├── 02_safety_plc_and_io.md         → Mimariyi (Kategori) donanıma döken katman
├── 03_safe_motion.md               → IEC 61800-5-2 STO; sürücünün SIL/PL kapasitesi
└── 04_estop_and_safety_circuits.md → E-stop/ışık perdesi devre mimarisi (Kategori)

agent/safety_principles.md          → "Yüksek PL donanımdan gelir" ilkesi
```
