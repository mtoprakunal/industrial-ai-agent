---
KONU        : Güvenli Hareket (Safe Motion) — IEC 61800-5-2
KATEGORİ    : safety
ALT_KATEGORI: safe-motion
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.synapticon.com/en/motion-control-academy/sichere-stopp-funktionen-ss1-ss2-sos"
    başlık: "SS1, SS2 and SOS — Safe stop functions explained (Synapticon)"
    güvenilirlik: topluluk
  - url: "https://www.machinebuilding.net/safe-motion-standard-en-61800-5-2-more-than-safe-torque-off"
    başlık: "Safe motion standard EN 61800-5-2: more than Safe Torque Off"
    güvenilirlik: topluluk
  - url: "https://download.sew-eurodrive.com/download/html/30587239/en-EN/4014183898743621600907.html"
    başlık: "Safety sub-functions according to EN 61800-5-2 — SEW-EURODRIVE"
    güvenilirlik: topluluk
  - url: "https://www.manualslib.com/manual/2112228/Inovance-Sv660n-Series.html?page=419"
    başlık: "Inovance SV660N Advanced User's Manual — Safety Function: STO"
    güvenilirlik: resmi
  - url: "https://www.motioncontroltips.com/how-do-sto-inputs-affect-sil3-ple-conformity-for-ac-drives/"
    başlık: "How STO inputs affect SIL3/PLe conformity — Motion Control Tips"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/safety/_synthesis.md"
    ilişki: detaylandırır
  - konu: "knowledge/safety/01_sil_pl_standards.md"
    ilişki: gerektirir
  - konu: "knowledge/safety/02_safety_plc_and_io.md"
    ilişki: gerektirir
  - konu: "knowledge/safety/04_estop_and_safety_circuits.md"
    ilişki: tamamlar
  - konu: "knowledge/inovance/inoproshop/06_motion_control.md"
    ilişki: detaylandırır
  - konu: "agent/safety_principles.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "knowledge/inovance/inoproshop/06_motion_control.md (PLCopen MC_Stop, ErrorStop, eksen durumları)"
  - "knowledge/safety/02_safety_plc_and_io.md (F-DO, FSoE, çift kanal)"
ÇELİŞKİLER :
  - kaynak: "MC_Stop emniyetli duruş mudur?"
    konu: "PLCopen MC_Stop ile emniyet fonksiyonu STO/SS1 ilişkisi"
    çözüm: >
      HAYIR. MC_Stop YAZILIMSAL, kontrollü duruştur — emniyet DEĞİLDİR. CPU donar,
      sürücü haberleşmesi kopar veya kod hatalıysa MC_Stop motoru durdurmaz. Emniyetli
      duruş, sürücünün DONANIMSAL STO girişiyle (veya SS1) sağlanır. MC_Stop emniyet
      fonksiyonunun YERİNE GEÇMEZ; yalnızca normal işletme duruşudur. (agent ilkesi)
  - kaynak: "STO her durumda yeterli mi?"
    konu: "Dikey/asılı yük ve döner kütlede STO riski"
    çözüm: >
      HAYIR. STO motoru ANINDA enerjisiz bırakır (Stop Kat. 0) → motor serbest savrulur.
      Dikey eksende yük DÜŞER (yerçekimi); yüksek atalette mil savrulmaya devam eder.
      Bu durumlarda önce kontrollü duruş (SS1) sonra STO, ayrıca mekanik fren (SBC)
      gerekir. Emniyet fonksiyonu tehlikeye göre seçilir; "STO koyduk, tamam" yanılgıdır.
---

## Özün Ne

Güvenli hareket (safe motion), bir servo/sürücünün hareketini emniyetli biçimde sınırlayan veya durduran fonksiyonlar ailesidir; **IEC 61800-5-2** standardıyla tanımlanır (PDS-SR — güç tahrik sistemleri, emniyetle ilgili). En temel ve en yaygın fonksiyon **STO (Safe Torque Off)**'tur: motora giden tork üretimini donanımsal olarak keser, böylece motor güç üretemez. Standart ayrıca SS1, SS2, SOS, SLS, SDI gibi daha sofistike fonksiyonlar tanımlar.

Bu belgenin değişmez mesajı `agent/safety_principles.md` ile aynıdır: **Emniyetli duruş PLCopen `MC_Stop` ile sağlanmaz.** `MC_Stop` yazılımsal, kontrollü bir duruştur — emniyet değildir. Emniyet, sürücünün **donanımsal STO girişiyle** ve emniyet rölesi/Safety PLC ile kurulur. Bu belge, IEC 61800-5-2 fonksiyonlarını ve bunların `knowledge/inovance/inoproshop/06_motion_control.md` içinde geçen SV660N STO girişiyle nasıl bağlandığını anlatır.

## Nasıl Çalışır

### IEC 61800-5-2 Emniyet Fonksiyonları — DOĞRULANMIŞ

| Fonksiyon | Adı | Ne yapar | Stop Kat. (IEC 60204-1) |
|-----------|-----|----------|--------------------------|
| **STO** | Safe Torque Off | Tork üretimini ANINDA keser; motor serbest savrulur (uncontrolled) | Kat. 0 |
| **SS1** | Safe Stop 1 | Önce kontrollü yavaşlatma, sonra STO devreye girer | Kat. 1 |
| **SS2** | Safe Stop 2 | Kontrollü duruş; sonra güç korunarak konum tutulur (→ SOS) | Kat. 2 |
| **SOS** | Safe Operating Stop | Motor enerjili kalır, duruş konumunu güvenle izler (savrulmaya izin vermez) | — |
| **SLS** | Safely Limited Speed | Bir/birkaç hız sınırını aşmayı engeller; aşılırsa STO/SS1 tetikler | — |
| **SDI** | Safe Direction | Belirlenen hareket yönüne uyumu izler; ihlalde SS1 tetikler | — |
| **SLA** | Safely Limited Acceleration | İvmeyi güvenli sınırda tutar | — |

Kaynak: [Synapticon — SS1/SS2/SOS](https://www.synapticon.com/en/motion-control-academy/sichere-stopp-funktionen-ss1-ss2-sos), [SEW-EURODRIVE — EN 61800-5-2 sub-functions](https://download.sew-eurodrive.com/download/html/30587239/en-EN/4014183898743621600907.html), [Machine Building — EN 61800-5-2](https://www.machinebuilding.net/safe-motion-standard-en-61800-5-2-more-than-safe-torque-off). Stop kategori eşleştirmesi için bkz. `04_estop_and_safety_circuits.md`.

### STO Nasıl Çalışır — Donanımsal Tork Kesme

```
Sürücünün GÜÇ KATMANI (PWM → IGBT → motor)
                    ▲
                    │ PWM sürme sinyalleri
          ┌─────────┴─────────┐
          │   STO devresi      │  ← İKİ bağımsız donanım yolu (çift kanal)
          │  STO1 ───┐         │
          │  STO2 ───┴── AND   │  Her iki sinyal AKTİF olmalı ki PWM geçsin
          └─────────┬─────────┘
                    │
          STO1 veya STO2 düşerse → PWM BLOKE → motor tork üretemez

Kritik: STO yazılımdan GEÇMEZ. Doğrudan donanım, PWM'yi fiziksel olarak engeller.
CPU donsa, firmware çökse bile STO çalışır → bu yüzden emniyetlidir (agent ilkesi).
```

### SV660N STO — DOĞRULANMIŞ

Inovance SV660N (EtherCAT servo sürücü) STO fonksiyonu:

- **Uyum:** IEC 61800-5-2:2016, **SIL 3 / PL e** kapasitesi.
- **Girişler:** İki yalıtılmış, çift kanallı giriş **STO1** ve **STO2** (+24 VDC besleme pini ile).
- **Mantık:** Her iki sinyal de aktif (yüksek) olmalı ki sürücü normal çalışsın. **Biri veya ikisi düşerse, PWM sinyalleri ~20 ms içinde bloke edilir** → motor tork üretemez.
- **SIL 3/PL e koşulu:** STO iki ayrı kanalla kontrol edilmeli; bir kanaldaki arıza diğerinin motoru durdurma yeteneğini etkilememeli (çift kanal + bağımsızlık).

Kaynak: [Inovance SV660N Advanced User's Manual — Safety Function: STO](https://www.manualslib.com/manual/2112228/Inovance-Sv660n-Series.html?page=419), [Motion Control Tips — STO SIL3/PLe](https://www.motioncontroltips.com/how-do-sto-inputs-affect-sil3-ple-conformity-for-ac-drives/). Bu, `knowledge/inovance/inoproshop/06_motion_control.md` içindeki "SV660N'de STO" notunun derinleştirilmiş halidir.

### MC_Stop ≠ STO — Kritik Ayrım

```
PLCopen MC_Stop (YAZILIM)              IEC 61800-5-2 STO (DONANIM)
──────────────────────────────────────────────────────────────────
Nerede çalışır  PLC + sürücü firmware    Sürücü güç katmanı (PWM gate)
CPU donarsa     ÇALIŞMAZ                  ÇALIŞIR (donanımsal)
Haberleşme      gerektirir (EtherCAT)     gerektirmez (donanım giriş)
Amaç            normal işletme duruşu     EMNIYET — tork kesme
Eksen durumu    Stopping → Standstill     ErrorStop (sonra MC_Reset)
Emniyet mi?     HAYIR                     EVET (SIL/PL kapasiteli)
```

Bu ayrım, eksen durum makinesiyle (bkz. `06_motion_control.md`) birleşir: STO tetiklenince eksen **ErrorStop**'a düşer; toparlanma için STO kalkar → `MC_Reset` → `MC_Power`. STO sonrası temiz toparlanma bu sırayı gerektirir.

## Pratikte Nasıl Kullanılır

### STO Bağlantısı (SV660N + Emniyet Rölesi/Safety PLC)

```
Emniyet kaynağı (E-stop / kapı / ışık perdesi)
        │ çift kanal
        ▼
Emniyet rölesi veya Safety PLC F-DO (çift kanal çıkış)
        │ STO1          │ STO2
        ▼               ▼
SV660N  STO1 girişi    STO2 girişi
        │
        └─► Her iki sinyal aktif → sürücü çalışır
            Biri düşer → PWM bloke (~20 ms) → motor enerjisiz (tork yok)

Standart CODESYS/InoProShop PLC:
  ✓ STO durumunu OKUR (sürücü diyagnostik objesinden), HMI'da gösterir
  ✓ STO sonrası kontrollü toparlanmayı yönetir (ErrorStop → Reset → Power)
  ✗ STO'yu TETİKLEMEZ — emniyet zinciri tetikler (agent ilkesi)
```

### FSoE Üzerinden STO (EtherCAT hattı)

SV660N STO, ayrı kablo yerine **FSoE** üzerinden de sürülebilir (bkz. `02_safety_plc_and_io.md`): Safety PLC, FSoE container ile STO komutunu EtherCAT hattı üzerinden gönderir; kara kanal (EtherCAT) taşır, FSoE katmanı korur. Tek EtherCAT zinciri hem motion PDO hem emniyet STO taşır.

### Fonksiyon Seçimi — Tehlikeye Göre

```
Yatay eksen, düşük atalet, savrulma zararsız     → STO (Kat. 0) yeterli
Yüksek hız/atalet, ani kesme tehlikeli            → SS1 (önce yavaşla, sonra STO)
Konum tutması gereken (robot kolu durunca)        → SS2 / SOS (konumu güvenle tut)
Kurulum/bakımda yavaş hareket gerekli (teach)     → SLS (güvenli sınırlı hız)
Tek yön güvenli, ters yön tehlikeli               → SDI (yön izleme)
Dikey/asılı yük (yerçekimi düşürür)               → SS1 + mekanik fren (SBC)
```

## Örnekler

### Örnek 1: Koruma Kapısı → SV660N STO (PL d hedefi)

```
Tehlike : Açık kapıda dönen mil → el sıkışması (S2, F2, P2 mertebesi)
Hedef   : PL d / SIL 2

Zincir:
  Kapı anahtarı (çift kanal, zorla açma) → Safety PLC F-DI
    → Safety PLC emniyet mantığı → F-DO çift kanal
    → SV660N STO1 + STO2 → PWM bloke → tork yok

Standart InoProShop: STO durumunu okur, HMI'da "Kapı açık — eksen emniyetli" gösterir,
kapı kapanınca operatör reset'iyle ErrorStop → MC_Reset → MC_Power sırasını yürütür.
```

### Örnek 2: Dikey Eksende STO Tuzağı

```
❌ Dikey kaldırma ekseninde yalnızca STO:
   STO tork keser → motor tutamaz → YÜK DÜŞER (yerçekimi). Tehlike artar!

✅ Doğru: SS1 (kontrollü yavaşlat) + mekanik fren (SBC ile güvenli devreye al).
   Fren kapanınca STO. Yük asla serbest düşmez.
```

### Örnek 3: SLS ile Teach Modu

```
Kurulumcu hücre içinde, kapı açık, yavaş hareketle eksen ayarlıyor (teach).
  SLS aktif → eksen hızı güvenli sınırın altında tutulur.
  Sınır aşılırsa → otomatik STO/SS1 → eksen durur.
Bu, "kapı açık ama kontrollü düşük hızla çalışma" gereksinimini emniyetli karşılar.
```

## Sık Yapılan Hatalar

### Hata 1: MC_Stop'u Emniyet Sanmak
En kritik hata. `MC_Stop` yazılımsal kontrollü duruştur; emniyet değildir. E-stop/kapı tehlikesi STO/SS1 ile (donanımsal) çözülür, `MC_Stop` ile değil. (agent ÇELİŞKİLER)

### Hata 2: Tek Kanallı STO ile SIL 3 Beklemek
STO'yu tek sinyalle sürmek SIL 3/PL e vermez. SV660N'de STO1 *ve* STO2 ayrı kanallardan, bağımsız sürülmeli.

### Hata 3: Dikey Yükte STO Yeterli Sanmak
STO motoru serbest bırakır; dikey/asılı yük düşer. SS1 + mekanik fren (SBC) gerekir.

### Hata 4: STO Sonrası Toparlanmayı Yanlış Yönetmek
STO tetiklenince eksen ErrorStop'a düşer. Doğrudan `MC_Power` denemek başarısız olur. Sıra: STO kalkar → `MC_Reset` → `MC_Power`. (bkz. `06_motion_control.md`)

### Hata 5: STO'yu Standart Koddan Tetiklemeye Çalışmak
STO'yu CODESYS programından sürmek emniyet ihlalidir (`safety_io_on_standard_modules_forbidden`). Tetikleme emniyet rölesi/Safety PLC/FSoE'nin işidir; standart kod yalnızca durumu okur.

### Hata 6: STO Tepki Süresini Doğrulamamak
SV660N STO ~20 ms'de PWM'yi bloke eder ama toplam emniyet tepki süresi (sensör + mantık + STO + mekanik) hedefe göre hesaplanmalı ve ölçülmeli (`estop_stop_time_must_be_verifiable`). Dönen kütlenin durma süresi ayrıca ölçülür.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **STO:** En yaygın; tork kesmenin yeterli olduğu, savrulmanın zararsız olduğu yatay/düşük atalet eksenler. Maliyet/karmaşıklık düşük.
- **SS1:** Yüksek hız/ataletli eksende ani kesme tehlikeliyse; önce yavaşlat sonra STO.
- **SS2/SOS:** Duruşta konumun korunması gerektiğinde (robot, asılı yük tutma).
- **SLS:** Kurulum/bakımda kapı açık düşük hızlı çalışma gerektiğinde.
- **SDI:** Tek yönün güvenli olduğu eksenlerde.
- **STO tek başına YETMEZ:** Dikey/asılı yük → SS1 + SBC (mekanik fren) şart.

## Gerçek Proje Notları

**Not 1 — "STO koyduk, emniyet tamam" en pahalı yanılgı.** Bir kaldırma ekseninde yalnızca STO kuruldu; testte E-stop'a basınca yük serbest düştü. STO tork keser, tutmaz. Çözüm SS1 + mekanik fren oldu. Emniyet fonksiyonu *tehlikeye göre* seçilir — STO varsayılan değil, yatay/düşük-atalet için doğru seçimdir.

**Not 2 — STO'yu FSoE ile sürmek kabloyu sadeleştirdi.** SV660N motion projesinde STO'yu ayrı kablo yerine FSoE üzerinden sürdük (bkz. `02`). Tek EtherCAT zinciri motion + emniyeti taşıdı; pano sadeleşti. SV660N'in hem standart PDO hem FSoE STO desteklemesi bunu mümkün kıldı.

**Not 3 — STO sonrası ErrorStop toparlanmasını baştan kodla.** İlk devreye almada, STO sonrası eksen ErrorStop'ta kaldı ve "neden hareket etmiyor" diye zaman harcandı. PLCopen state machine'inde ErrorStop → MC_Reset → MC_Power sırası baştan kodlanmalı; STO emniyet zincirinden, toparlanma standart koddan yürür (ayrımı koruyarak).

**Not 4 — Tepki süresini gerçekten ölç.** SV660N STO ~20 ms PWM bloke süresi veriyor ama bu emniyet zincirinin *bir parçası*. Toplam (sensör algılama + emniyet mantığı + STO + dönen kütlenin durması) gerçek ölçümle doğrulanmalı; spec'teki "X ms içinde dur" iddiası test edilebilir olmalı (`estop_stop_time_must_be_verifiable`).

**Not 5 — Standart limit ve yazılım limiti emniyet değildir.** `06_motion_control.md` da vurgulandığı gibi, yazılım pozisyon limitleri ve donanım limit anahtarları işlevseldir; acil durdurma STO + emniyet zinciriyle kurulur. İkisini karıştırmamak gerekir.

## İlgili Konular

```
knowledge/safety/
├── _synthesis.md                   → Emniyet fonksiyonu zinciri, STO örneği
├── 01_sil_pl_standards.md          → STO'nun SIL 3/PL e kapasitesi ne demek
├── 02_safety_plc_and_io.md         → STO'yu F-DO/FSoE ile sürme
└── 04_estop_and_safety_circuits.md → Stop kategori 0/1/2 ↔ STO/SS1/SS2 eşlemesi

knowledge/inovance/inoproshop/06_motion_control.md → SV660N, PLCopen, ErrorStop, MC_Stop
agent/safety_principles.md          → "E-stop donanımsal, MC_Stop emniyet değil" ilkesi
```
