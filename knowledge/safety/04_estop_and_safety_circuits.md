---
KONU        : Acil Durdurma ve Emniyet Devreleri
KATEGORİ    : safety
ALT_KATEGORI: safety-circuits
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://machinerysafety101.com/2010/09/27/emergency-stop-categories/"
    başlık: "Understanding Stop Categories for Machinery — Machinery Safety 101"
    güvenilirlik: topluluk
  - url: "https://www.se.com/eg/en/faqs/FA225420/"
    başlık: "Difference between Stop Category 0, 1 and 2 — Schneider Electric"
    güvenilirlik: topluluk
  - url: "https://www.iso.org/standard/45947.html"
    başlık: "ISO 13850 — Emergency stop function, principles for design (ISO resmi)"
    güvenilirlik: resmi
  - url: "https://en.wikipedia.org/wiki/ISO_13849"
    başlık: "ISO 13849 — Wikipedia (Kategori, çift kanal, reset)"
    güvenilirlik: topluluk
  - url: "https://www.iec.ch/standardsdev/our-development-process/"
    başlık: "IEC 60204-1 — Safety of machinery, electrical equipment (IEC resmi)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "knowledge/safety/_synthesis.md"
    ilişki: detaylandırır
  - konu: "knowledge/safety/01_sil_pl_standards.md"
    ilişki: gerektirir
  - konu: "knowledge/safety/02_safety_plc_and_io.md"
    ilişki: gerektirir
  - konu: "knowledge/safety/03_safe_motion.md"
    ilişki: tamamlar
  - konu: "agent/safety_principles.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "knowledge/safety/01_sil_pl_standards.md (Kategori, PL, çift kanal)"
  - "knowledge/safety/02_safety_plc_and_io.md (emniyet rölesi, F-DI/F-DO)"
ÇELİŞKİLER :
  - kaynak: "E-stop yazılımla sağlanabilir mi?"
    konu: "Acil durdurmanın yazılım veya donanım olması"
    çözüm: >
      HAYIR. E-stop DONANIMSALDIR. Buton kontağı doğrudan emniyet zincirini (röle/Safety
      PLC F-DI) keser; yazılım yalnızca durumu YANSITIR ve kontrollü duruşu yönetir.
      CPU donsa bile E-stop çalışmalı. (agent: estop_is_hardwired_not_software)
  - kaynak: "Stop Kategori 0 her zaman en güvenli mi?"
    konu: "Anında güç kesme (Kat. 0) vs kontrollü duruş (Kat. 1)"
    çözüm: >
      HAYIR — duruma bağlı. Kat. 0 gücü anında keser; yüksek atalet/dikey yükte motor
      savrulur veya yük düşer → daha tehlikeli olabilir. Kat. 1 önce kontrollü yavaşlatır
      sonra gücü keser. Tehlike analizine göre seçilir. E-stop için yalnızca Kat. 0 ve 1
      izinlidir; Kat. 2 (güç korunur) acil durdurma için KULLANILAMAZ.
  - kaynak: "Reset (manuel kurma) emniyet için zorunlu mu?"
    konu: "Otomatik vs manuel reset"
    çözüm: >
      Tehlikeli hareket varsa manuel reset ZORUNLUDUR. Emniyet koşulu düzelince sistem
      KENDILIĞINDEN çalışmaya başlamamalı; operatör bilinçli reset (ayrı buton) yapmalı.
      Otomatik yeniden başlama (auto-reset) yalnızca beklenmedik harekete yol açmayan
      düşük riskli durumlarda kabul edilir. Reset butonu emniyet bölgesini görmeli.
---

## Özün Ne

Acil durdurma (E-stop) ve emniyet devreleri, bir operatörün veya emniyet cihazının (ışık perdesi, kapı kilidi) tehlikeli hareketi durdurmasını sağlayan donanımsal zincirlerdir. Temel ilke `agent/safety_principles.md` ile birebir aynıdır: **E-stop donanımsaldır; yazılım yalnızca durumu yansıtır ve kontrollü duruşu yönetir** (`estop_is_hardwired_not_software`). E-stop butonunun kontağı, hiçbir yazılım katmanına bağlı olmadan, doğrudan emniyet zincirini keser — CPU donsa, firmware çökse bile çalışmalıdır.

Bu belge; **IEC 60204-1 stop kategorilerini (0/1/2)**, ışık perdesi/kapı kilidi gibi emniyet cihazlarını, emniyet rölesinin çalışmasını, iki-el kumandasını, reset (kurma) mantığını ve tüm bunların **ISO 13849 Kategori/PL** ile (bkz. `01_sil_pl_standards.md`) nasıl ilişkilendiğini anlatır. E-stop ayrıca ISO 13850 (acil durdurma tasarım ilkeleri) ile yönetilir.

## Nasıl Çalışır

### Stop Kategorileri (IEC 60204-1) — DOĞRULANMIŞ

| Kategori | Tanım | Güç davranışı | E-stop'ta izinli mi? |
|----------|-------|----------------|----------------------|
| **Kategori 0** | Aktüatörlere gücün ANINDA kesilmesiyle durdurma (kontrolsüz/uncontrolled stop) | Güç hemen kesilir | EVET |
| **Kategori 1** | Kontrollü duruş; durmak için güç verilir, duruş tamamlanınca güç kesilir | Önce var, sonra kesilir | EVET |
| **Kategori 2** | Kontrollü duruş; güç aktüatörde KALIR | Güç korunur | HAYIR (yalnız normal duruş) |

Kaynak: [Schneider Electric — Stop Categories](https://www.se.com/eg/en/faqs/FA225420/), [Machinery Safety 101 — Stop Categories](https://machinerysafety101.com/2010/09/27/emergency-stop-categories/). ISO 13850 ve IEC 60204-1: **acil durdurma yalnızca Kategori 0 veya 1 olabilir**; Kategori 2 (güç korunur) E-stop için kullanılamaz, yalnızca normal işletme duruşudur.

### Stop Kategorisi ↔ Safe Motion Eşlemesi

IEC 60204-1 stop kategorileri, IEC 61800-5-2 safe motion fonksiyonlarıyla (bkz. `03_safe_motion.md`) doğrudan örtüşür:

```
Stop Kategori 0  ↔  STO  (Safe Torque Off — anında tork kes, savrul)
Stop Kategori 1  ↔  SS1  (önce kontrollü yavaşla, sonra STO)
Stop Kategori 2  ↔  SS2/SOS (kontrollü dur, güç koru, konum tut)  ← E-stop'ta KULLANILMAZ
```
Seçim tehlikeye göredir: yüksek atalet/dikey yük → Kat. 1 (SS1), zararsız savrulma → Kat. 0 (STO).

### Emniyet Rölesi Nasıl Çalışır

Emniyet rölesi, basit emniyet fonksiyonlarının sertifikalı, programsız "karar ver" katmanıdır:

```
E-stop (NC, çift kanal)        Reset butonu
   │ K1      │ K2                  │
   ▼         ▼                     ▼
┌──────────────────────────────────────────┐
│           EMNIYET RÖLESİ                   │
│  • İki kanalı çapraz izler (cross-monitor) │
│  • Zorla yönlendirmeli (force-guided)      │
│    iç kontaklar → kontak yapışmasını görür │
│  • Reset için manuel kurma bekler           │
└─────────────────┬──────────────────────────┘
                  │ enerjili = çıkış kapalı (NO kontak açık)
                  ▼
        Kontaktör / sürücü STO (çift kanal)

Çalışma:
  E-stop basılı → röle düşer → çıkış açılır → güç/STO kesilir → makine durur
  E-stop kalkar → röle KENDİLİĞİNDEN kurulmaz → reset gerekir (manuel)
```

Kritik özellik **zorla yönlendirmeli (force-guided) kontaklar**: bir çıkış kontağı yapışırsa, mekanik olarak bağlı izleme kontağı bunu ele verir ve röle yeniden kurulmaz. Bu, Kategori 3/4 için gereken "arıza tespiti"ni (bkz. `01_sil_pl_standards.md` DC) sağlar.

### Işık Perdesi (Light Curtain)

```
Verici ───── ışık demetleri ───── Alıcı     (AOPD — Active Opto-electronic Protective Device)
              │                               IEC 61496 standardı
   Bir demet kesilince (el/kol girer) → emniyet çıkışı (OSSD) düşer
              │
              ▼
   Emniyet rölesi / Safety PLC → durdurma (STO/SS1)

Önemli kavramlar:
  • OSSD (Output Signal Switching Device): perdenin çift kanallı emniyet çıkışı
  • Çözünürlük: parmak (14mm) / el (30mm) / vücut (gövde algılama)
  • Güvenlik mesafesi: durma süresi × yaklaşma hızı + cisim çözünürlüğü payı
  • Muting: izinli durumda (ör. palet geçişi) perdeyi geçici, denetimli devre dışı bırakma
```
Güvenlik mesafesi yanlış hesaplanırsa, el tehlikeye perde tetiklemeden önce ulaşır → mesafe kritik.

### İki-El Kumandası (Two-Hand Control)

```
Operatörün iki elini de tehlike bölgesinden uzak tutar:
  Buton A ──┐
  Buton B ──┴── İKİSİ de, ~0.5 s içinde, EŞ ZAMANLI basılmalı
              │
   Tek buton / geç basış / köprüleme → hareket başlamaz
   Buton bırakılınca → hareket durur (Kat. 0 veya 1)

IEC 60204-1 / ISO 13851. Tek elle veya bağlayarak (zip-tie) kandırmaya karşı
eş zamanlılık ve sürekli basılı tutma şartı korur.
```

### Reset (Kurma) Mantığı — Beklenmedik Yeniden Başlamayı Önleme

```
Emniyet koşulu düzeldi (E-stop kalktı, kapı kapandı, perde temizlendi)
        │
        ▼
   Sistem KENDİLİĞİNDEN çalışmaz   ← kritik!
        │
   Operatör RESET butonuna basar (ayrı, bilinçli eylem)
        │
   Reset butonu emniyet bölgesini GÖRMELİ (operatör kimsenin içeride
   olmadığını görerek reset yapar)
        │
        ▼
   Sistem çalışmaya hazır (ama hareket ayrı START ile başlar)
```
`agent/rules.json`: emniyet düzelince "çalışmaya devam et" değil, "güvenli/durdur" varsayılan kalır (`fail_safe_default_is_stop_not_run`). Reset ayrı, bilinçli operatör eylemidir.

### Devre Mimarisi ↔ Kategori İlişkisi

```
Tek kanal E-stop + standart DI                → Kategori B (PL b max) — EMNIYET DEĞİL
Tek kanal + kanıtlanmış bileşen               → Kategori 1 (PL c max)
Çift kanal E-stop + emniyet rölesi (izlemeli) → Kategori 3 (PL e'ye kadar)
Çift kanal + çapraz izleme + yüksek diyagnostik→ Kategori 4 (PL e)
```
Hedef PL (PLr) belirler hangi mimari gerekir (bkz. `01_sil_pl_standards.md`). PL d/e için çift kanal + izleme şarttır.

## Pratikte Nasıl Kullanılır

### E-stop Devresi Kurulumu (Kategori 3, PL d/e)

1. **Çift kanallı E-stop butonu** seç (iki bağımsız NC kontak, zorla açma — direct opening).
2. Her kanalı **ayrı kablodan** emniyet rölesi/Safety PLC F-DI'sine bağla (CCF için ayrı yol).
3. Röle/Safety PLC **çapraz izleme** yapsın; kanal uyuşmazlığında güvenli hal.
4. Çıkışı **çift kanallı** olarak kontaktöre veya sürücü STO'suna sür (bkz. `03`).
5. **Manuel reset** ekle; reset butonu emniyet bölgesini görür konumda.
6. **Tepki süresini ölç** ve doğrula (`estop_stop_time_must_be_verifiable`).
7. **Standart PLC** yalnızca durumu okur, HMI'da gösterir; E-stop'u tetiklemez.

### NC (Normally Closed) ve Fail-Safe Kablolama

```
E-stop kontağı NC (normalde kapalı) kullanılır:
  Normal     → kontak kapalı → akım akar → röle enerjili → makine çalışabilir
  Basılı     → kontak açılır → akım kesilir → röle düşer → makine durur
  Kablo KOPARSA → akım kesilir → makine durur  ← FAIL-SAFE!

NO (normalde açık) kullanılsaydı, kablo kopması fark edilmez ve E-stop çalışmazdı.
Bu, agent ilkesi "sinyal kaybı = güvenli yön"un kablolama karşılığıdır.
```

## Örnekler

### Örnek 1: Robot Hücresi (PL e)

```
Tehlike: Robot kolu, yüksek hız → ağır yaralanma (S2, F2, P2) → PLr e

Emniyet cihazları:
  • Çevre: kapı kilitli (interlock) + ışık perdesi (giriş noktası)
  • E-stop: hücre köşelerinde + operatör panelinde (çift kanal)
  • Hepsi → Safety PLC → robot/servo STO (çift kanal, FSoE)

Reset: Hücre dışında, içeriyi gören konumda; operatör kimsenin olmadığını
       görerek reset yapar. Sistem otomatik başlamaz.
```

### Örnek 2: Stop Kategorisi Seçimi

```
Yatay konveyör (düşük atalet):      E-stop → Kat. 0 (STO) → anında dur, zararsız
Büyük santrifüj (yüksek atalet):    E-stop → Kat. 1 (SS1) → kontrollü yavaşla, sonra STO
                                    (Kat. 0 olsaydı dakikalarca savrulurdu — daha tehlikeli)
```

### Örnek 3: Yanlış Devre (agent ihlali)

```
❌ E-stop → tek kanal → standart DI → CODESYS "IF estop THEN motor:=FALSE"
   + emniyet kalkınca kod otomatik START veriyor
   İhlal: estop_is_hardwired_not_software + fail_safe_default_is_stop_not_run

✅ E-stop → çift kanal → emniyet rölesi (izlemeli) → kontaktör/STO (çift kanal)
   + manuel reset, otomatik başlama yok; standart PLC yalnızca durumu okur
```

## Sık Yapılan Hatalar

### Hata 1: E-stop'u Yazılıma Bağlamak
E-stop'u standart DI'dan okuyup yazılımda işlemek emniyet değildir. Buton kontağı doğrudan emniyet zincirini keser (`estop_is_hardwired_not_software`).

### Hata 2: NO Kontak Kullanmak
E-stop NC olmalı; kablo kopması güvenli yöne (durma) düşmeli. NO kontak fail-safe değildir.

### Hata 3: Otomatik Yeniden Başlama
Emniyet düzelince makineyi kendiliğinden başlatmak. Tehlikeli hareket varsa manuel reset zorunlu; reset bölgeyi görmeli (`fail_safe_default_is_stop_not_run`).

### Hata 4: E-stop için Kategori 2 Kullanmak
Kategori 2 (güç korunur) acil durdurmada kullanılamaz; yalnızca Kat. 0/1 izinli. Kat. 2 normal işletme duruşudur.

### Hata 5: Işık Perdesi Güvenlik Mesafesini Yanlış Hesaplamak
Mesafe = durma süresi × yaklaşma hızı + çözünürlük payı. Yanlış hesap → el, perde tetiklemeden tehlikeye ulaşır.

### Hata 6: Tek Kanal + Standart Modülle Yüksek PL Beklemek
PL d/e çift kanal + çapraz izleme ister (Kategori 3/4). Tek kanal Kategori B/1'de kalır (PL b/c max).

### Hata 7: Reset Butonunu Bölgeyi Görmeyen Yere Koymak
Operatör içeriyi görmeden reset yaparsa, bölgedeki kişi için tehlike doğar. Reset noktası tehlike bölgesini görmeli.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Stop Kat. 0 (STO):** Düşük atalet, savrulma zararsız, anında kesme güvenli.
- **Stop Kat. 1 (SS1):** Yüksek atalet/dikey yük; ani kesme tehlikeli → önce kontrollü yavaşla.
- **Işık perdesi:** Sık erişilen, fiziksel kapı uygun olmayan giriş noktaları (yükleme/boşaltma).
- **Kapı kilidi (interlock):** Bölgeye giriş seyrek, fiziksel bariyer mümkün.
- **İki-el kumanda:** Tek operatörün ellerini tehlikeden uzak tutması gereken pres/kesme işleri.
- **Manuel reset:** Tehlikeli hareketin olduğu her durumda zorunlu; auto-reset yalnız düşük risk.

## Gerçek Proje Notları

**Not 1 — NC + zorla açma (direct opening) pazarlık konusu değil.** Bir projede ucuz E-stop butonu (NO kontak, mekanik zorla açma yok) kullanılmak istendi. Reddedildi: kablo kopması fark edilmezdi ve kontak yapışması durdurmayı engellerdi. Sertifikalı, zorla açma kontaklı buton emniyet zincirinin temelidir; ucuzluk burada riske dönüşür.

**Not 2 — Reset, START'tan ayrı tutulmalı.** Bir hatta reset ve start aynı butona bağlanmıştı; emniyet düzelince makine aniden hareket etti. Reset (emniyeti yeniden kur) ile start (hareketi başlat) ayrı eylemler olmalı; reset makineyi *çalışmaya hazır* yapar, *çalıştırmaz*. Bu ayrım beklenmedik hareketi önler.

**Not 3 — Tepki süresini ölçmeden "güvenli" deme.** Spec "500 ms içinde dur" diyordu ama gerçekte dönen kütle 1.2 s'de durdu. Işık perdesi güvenlik mesafesi bu gerçek süreye göre yeniden hesaplandı. `estop_stop_time_must_be_verifiable` — iddia değil, ölçüm. Dönen/atıl kütlede durma süresi her zaman test edilir.

**Not 4 — Muting'i denetimli kur.** Bir paketleme hattında ışık perdesi muting'i (palet geçerken geçici devre dışı) yanlış kuruldu; perde sürekli mute kaldı ve koruma kalktı. Muting yalnızca tanımlı, denetimli koşulda (muting sensörleri + zaman penceresi) aktif olmalı; aksi halde "kapalı perde" tehlikesi doğar.

**Not 5 — Emniyet rölesi basit projede Safety PLC'den iyidir.** Tek E-stop + tek kapılı küçük bir makinede Safety PLC dayatmak gereksiz karmaşıklık getirdi. Sabit mantıklı emniyet rölesi (çapraz izlemeli, force-guided) aynı PL'yi daha ucuz ve daha hızlı doğrulanır şekilde sağladı (bkz. `02_safety_plc_and_io.md`).

**Not 6 — Standart PLC durumu okur, kararı vermez.** HMI'da "E-stop basılı", "Kapı açık", "Perde kesildi" göstermek değerli diyagnostiktir ve standart CODESYS bunu yapar. Ama durdurma kararı emniyet zincirinden gelir. Bu ayrım net tutulmazsa, denetim "emniyet yazılıma bağımlı" diye reddeder (`safety_io_on_standard_modules_forbidden`).

## İlgili Konular

```
knowledge/safety/
├── _synthesis.md                   → "E-stop donanımsal" üst ilkesi
├── 01_sil_pl_standards.md          → Kategori 3/4 = çift kanal devre mimarisi
├── 02_safety_plc_and_io.md         → Emniyet rölesi, F-DI/F-DO, FSoE
└── 03_safe_motion.md               → Stop Kat. 0/1/2 ↔ STO/SS1/SS2 eşlemesi

agent/safety_principles.md          → "Acil durdurma zinciri" (madde 5), fail-safe
agent/rules.json (safety)           → estop_is_hardwired_not_software, fail_safe_default_is_stop
```
