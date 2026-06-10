---
KONU        : Emniyet PLC Mimarisi ve Safety I/O
KATEGORİ    : safety
ALT_KATEGORI: safety-plc
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.ethercat.org/en/safety.html"
    başlık: "Safety over EtherCAT (FSoE) — EtherCAT Technology Group (resmi)"
    güvenilirlik: resmi
  - url: "https://www.profibus.com/technology/functional-safety-profisafe"
    başlık: "PROFIsafe — PROFIBUS & PROFINET International (resmi)"
    güvenilirlik: resmi
  - url: "https://www.hilscher.com/service-support/glossary/black-channel"
    başlık: "Black Channel principle — Hilscher Glossary"
    güvenilirlik: topluluk
  - url: "https://www.blog.beckhoffus.com/post/safety-over-ethercat"
    başlık: "Safety over EtherCAT: Just the Facts — Beckhoff"
    güvenilirlik: topluluk
  - url: "https://en.wikipedia.org/wiki/ISO_13849"
    başlık: "ISO 13849 — Wikipedia (Kategori, çift kanal mimarisi)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/safety/01_sil_pl_standards.md"
    ilişki: gerektirir
  - konu: "knowledge/safety/03_safe_motion.md"
    ilişki: tamamlar
  - konu: "knowledge/safety/04_estop_and_safety_circuits.md"
    ilişki: tamamlar
  - konu: "knowledge/networking/_synthesis.md"
    ilişki: kullanır
  - konu: "knowledge/inovance/inoproshop/05_ethercat_configuration.md"
    ilişki: kullanır
  - konu: "agent/safety_principles.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "knowledge/safety/01_sil_pl_standards.md (Kategori, çift kanal, DC kavramları)"
  - "EtherCAT/PROFINET fieldbus temel kavramları (knowledge/networking)"
ÇELİŞKİLER :
  - kaynak: "Safety fieldbus ayrı kablo mu ister?"
    konu: "Emniyet verisi standart fieldbus üzerinden geçebilir mi?"
    çözüm: >
      Geçebilir — bu 'black channel' (kara kanal) ilkesidir. Emniyet protokolü
      (FSoE/PROFIsafe/CIP Safety) standart ağın ÜSTÜNE bir güvenlik katmanı koyar;
      ağın kendisi emniyet analizine dahil edilmez. Yani EtherCAT/PROFINET kablosu
      hem standart hem emniyet verisini taşır; emniyet protokolü bozulmayı kendi
      tespit eder (CRC, sıra no, zaman aşımı). Ayrı emniyet kablosu ŞART DEĞİLDİR.
  - kaynak: "Safety PLC standart PLC'nin yerini alır mı?"
    konu: "Tek bir PLC hem emniyet hem standart mantığı çalıştırabilir mi?"
    çözüm: >
      Modern Safety PLC'ler her ikisini aynı kasada çalıştırır AMA mantık AYRIK tutulur:
      emniyet programı ayrı, sertifikalı bir ortamda; standart program normal ortamda.
      Standart kod emniyet kodunu çağıramaz/bozamaz. Emniyet, standart mantığa bağımlı
      OLAMAZ (agent ilkesi). Fiziksel olarak tek cihaz, mantıksal olarak iki ayrı dünya.
---

## Özün Ne

Emniyet PLC (Safety PLC / F-CPU), bir emniyet fonksiyonunun "karar ver" katmanını sertifikalı, hata-toleranslı bir donanımda gerçekleştiren kontrolördür. Standart bir PLC'den temel farkı: **içsel olarak yedekli (redundant) çalışır** — iki işlemci çekirdeği aynı mantığı yürütür, sonuçları karşılaştırır, uyuşmazlıkta sistemi güvenli hale (çıkışlar enerjisiz) sürer. Bu, `agent/rules.json` içindeki `all_outputs_deenergize_on_cpu_fault` ve `fail_safe_default_is_stop_not_run` kurallarının donanımsal karşılığıdır.

Safety I/O ise emniyet sinyallerini (E-stop, ışık perdesi, kapı kilidi) okuyan/süren özel, sertifikalı modüllerdir (F-modülleri). Kritik kural — agent ilkesiyle birebir: **emniyet I/O asla standart modüllere bağlanmaz** (`safety_io_on_standard_modules_forbidden`). Bu belge, emniyet mantığını ve I/O'sunu standart kontrolden mimari olarak nasıl ayırdığımızı ve emniyet verisinin fieldbus üzerinden (FSoE/PROFIsafe/CIP Safety) nasıl güvenle taşındığını anlatır.

## Nasıl Çalışır

### Standart PLC vs Safety PLC

```
                  STANDART PLC              SAFETY PLC (F-CPU)
──────────────────────────────────────────────────────────────────────
İşlemci         Tek çekirdek               Çift çekirdek (1oo2 / 2oo2)
Karşılaştırma   Yok                         Her tarama sonuçları karşılaştırır
Arıza davranışı Tanımsız/devam edebilir     Uyuşmazlık → güvenli hal (çıkış kapalı)
Watchdog        Var (kapatılabilir)         Var, kapatılamaz, emniyet kritik
Diyagnostik     Opsiyonel                   Sürekli, yerleşik (DC yüksek)
Sertifika       Yok                         TÜV — SIL 2/3, PL d/e
Programlama     Tüm IEC 61131-3 serbest      Kısıtlı, sertifikalı emniyet blokları
```

Safety PLC'nin özü **1oo2 / 2oo2** gibi mimarilerdir: iki bağımsız hesap yolu aynı sonucu üretmeli; üretmezse sistem güvenli tarafa düşer. Bu, ISO 13849 Kategori 3/4'ün (tek arıza fonksiyon kaybına yol açmaz) cihaz içi gerçekleştirimidir (bkz. `01_sil_pl_standards.md`).

### Çift Kanal (Dual Channel) İlkesi

Emniyet zincirinin tamamı — sensörden aktüatöre — çift kanallı kurulur:

```
        KANAL A                              KANAL B
   ┌──────────────┐                    ┌──────────────┐
   │ E-stop NC 1  │                    │ E-stop NC 2  │   ← iki ayrı kontak
   └──────┬───────┘                    └──────┬───────┘
          │                                   │
   ┌──────▼───────┐   çapraz izleme    ┌──────▼───────┐
   │ F-DI kanal A │ ◄───(cross-check)──► │ F-DI kanal B │   ← Safety I/O
   └──────┬───────┘                    └──────┬───────┘
          │                                   │
        ┌─▼───────────────────────────────────▼─┐
        │       Safety PLC (1oo2 değerlendirme)  │
        └─────────────────┬──────────────────────┘
                          │
              ┌───────────▼───────────┐
              │ F-DO → kontaktör/STO  │   ← çift kanallı kapatma
              └───────────────────────┘

Tek bir kanalın arızası (kontak yapışması, kablo kopması, modül arızası)
fonksiyonu kaybettirmez → diğer kanal hâlâ güvenli hale sürer.
Çapraz izleme (cross-monitoring) iki kanalın tutarsızlığını tespit eder.
```

Bu mimari, `agent/safety_principles.md` "Emniyet ≠ Standart Kontrol" maddesinin uygulanmasıdır.

### Black Channel (Kara Kanal) İlkesi — Safety Fieldbus

Emniyet verisini standart bir endüstriyel ağ üzerinden taşımanın anahtarı **black channel** ilkesidir:

```
┌─────────────────────────────────────────────────────────────────┐
│ EMNIYET KATMANI (FSoE / PROFIsafe / CIP Safety)                  │
│  • CRC (veri bütünlüğü)                                          │
│  • Sıra numarası (kayıp/tekrar/sıra bozulması tespiti)           │
│  • Zaman damgası / watchdog (gecikme/kayıp tespiti)              │
│  • Kimlik (yanlış alıcı tespiti)                                 │
│  → Bu katman, taşıyıcının BOZMASINI kendi tespit eder            │
├─────────────────────────────────────────────────────────────────┤
│ "KARA KANAL" = standart fieldbus (EtherCAT / PROFINET / Ethernet)│
│  • Emniyet analizine DAHIL EDİLMEZ                               │
│  • Switch, kablo, standart cihazlar burada                      │
│  • Hata yapabilir — emniyet katmanı yakalar                     │
└─────────────────────────────────────────────────────────────────┘
```
Kaynak: [Hilscher — Black Channel](https://www.hilscher.com/service-support/glossary/black-channel), [EtherCAT Technology Group — Safety](https://www.ethercat.org/en/safety.html).

Sonuç: Emniyet verisi standart EtherCAT/PROFINET kablosu üzerinden, standart trafikle aynı hatta taşınır; **ayrı emniyet kablosu gerekmez**. Taşıyıcı (kara kanal) bir biti bozarsa, sıralamayı karıştırırsa veya paketi geciktirirse, emniyet protokolü bunu CRC + sıra no + watchdog ile tespit eder ve sistemi güvenli hale (timeout → stop) sürer.

### Üç Ana Safety Fieldbus Protokolü

| Protokol | Taşıyıcı (kara kanal) | Standardizasyon | Tipik SIL | Yöntem |
|----------|------------------------|-----------------|-----------|--------|
| **FSoE** (Safety over EtherCAT / FailSafe over EtherCAT) | EtherCAT | ETG, IEC 61784-3 | SIL 3'e kadar | Emniyet "container" standart EtherCAT process data içinde gömülü |
| **PROFIsafe** | PROFIBUS / PROFINET | PI, IEC 61784-3 | SIL 3'e kadar | Ayrı emniyet telgrafı |
| **CIP Safety** | EtherNet/IP (DeviceNet) | ODVA, IEC 61784-3 | SIL 3'e kadar | Producer/consumer modeli üzerinde emniyet katmanı |

Kaynak: [EtherCAT TG](https://www.ethercat.org/en/safety.html) (FSoE SIL 3, standart+emniyet aynı hatta), [PROFIBUS PI](https://www.profibus.com/technology/functional-safety-profisafe), [Copperhill — Industrial Safety Protocols](https://copperhilltech.com/blog/industrial-ethernet-guide-industrial-safety-protocols/).

Ortak nokta: Üçü de **IEC 61784-3** (fieldbus emniyet iletişim profilleri) çatısına ve black channel ilkesine dayanır. Seçim genelde ekosisteme bağlıdır: EtherCAT hattı → FSoE (SV660N gibi EtherCAT servolar için doğal); Siemens/PROFINET → PROFIsafe; Rockwell/EtherNet-IP → CIP Safety.

### Emniyet ile Standart Mantığın Ayrımı

```
TEK KASA, İKİ AYRI DÜNYA:

  ┌─────────────────────────────────────────────┐
  │            Safety PLC donanımı                │
  │  ┌────────────────┐   ┌────────────────────┐ │
  │  │ EMNIYET ortamı │   │ STANDART ortamı     │ │
  │  │ (sertifikalı)  │   │ (normal IEC 61131-3)│ │
  │  │ • E-stop mant. │   │ • Proses mantığı    │ │
  │  │ • Kapı izleme  │   │ • PID, sıralama     │ │
  │  │ • STO tetik    │   │ • HMI/OPC-UA        │ │
  │  └───────┬────────┘   └─────────┬──────────┘ │
  │          │  tek yön: durum okuma  │            │
  │          └──────────►─────────────┘            │
  └─────────────────────────────────────────────┘

Kural: Standart program emniyet durumunu OKUYABİLİR (HMI göstermek için);
       emniyet kararını DEĞİŞTİREMEZ. Emniyet, standart koda BAĞIMLI OLAMAZ.
```
Bu, agent ÇELİŞKİLER çözümünün ve `safety_io_on_standard_modules_forbidden` kuralının mimari uygulamasıdır.

## Pratikte Nasıl Kullanılır

### Adım Adım (EtherCAT + FSoE örneği, InoProShop/CODESYS bağlamı)

1. **Emniyet kontrolörünü seç:** Safety PLC veya emniyet rölesi (basit fonksiyon için röle yeter, bkz. `04`).
2. **F-modüllerini EtherCAT'e ekle:** F-DI (E-stop, ışık perdesi girişleri), F-DO (kontaktör), sürücü STO bağlantısı.
3. **FSoE bağlantısını yapılandır:** Her emniyet cihazına benzersiz FSoE adresi (FSoE Slave Address) ata — yanlış adres = yanlış alıcı tespiti devreye girer.
4. **Emniyet programını yaz:** Sertifikalı emniyet FB'leri (E-stop, kapı izleme, ışık perdesi muting) ile; standart taskla *karıştırma*.
5. **Watchdog/timeout ayarla:** FSoE watchdog süresi, kara kanal gecikmesine dayanacak ama emniyet tepki süresini aşmayacak şekilde.
6. **Doğrula:** Her kanalı tek tek arızalandır (kablo çek, kontak köprüle) → sistem güvenli hale düşmeli. STO tepki süresini ölç (`estop_stop_time_must_be_verifiable`).

### FSoE Adresleme — Kritik Detay

```
Her FSoE slave benzersiz bir FSoE Slave Address (FSA) taşır.
İki cihaza aynı adres verilirse → emniyet katmanı "yanlış alıcı" tespit eder → güvenli hal.
Bu, kablolama hatasına karşı yerleşik korumadır; standart EtherCAT'te böyle bir koruma yoktur.
```

## Örnekler

### Örnek 1: Standart ve Emniyet Verisinin Aynı EtherCAT Hattında Taşınması

```
EtherCAT hattı (tek kablo zinciri):
  PLC ── SV660N (servo, standart PDO: hız/konum) ── SV660N STO (FSoE, emniyet) ──
       ── F-DI modülü (E-stop, FSoE) ── F-DO modülü (kontaktör, FSoE) ── ...

  Standart trafik (motion PDO) ve emniyet trafiği (FSoE container) AYNI hatta.
  Kara kanal (EtherCAT) ikisini de taşır; FSoE katmanı emniyet verisini korur.
  → Ek emniyet kablosu yok; ağ topolojisi tek (bkz. knowledge/networking).
```

### Örnek 2: Emniyet Rölesi vs Safety PLC Kararı

```
Basit hücre (1 E-stop + 1 kapı + 1 ışık perdesi):
  → Emniyet RÖLESİ yeterli. Programlanabilir değil, sabit mantık, ucuz, hızlı validasyon.

Karmaşık hat (çok bölge, muting, kademeli durdurma, çok eksen STO):
  → Safety PLC + FSoE. Esnek, ölçeklenebilir, ama validasyon ve maliyet daha yüksek.
```

### Örnek 3: Yanlış Mimari (agent ihlali)

```
❌ E-stop butonu → standart DI modülü → CODESYS programı "IF estop THEN stop"
   Sorun: CPU donarsa, watchdog atlanırsa, değişken bozulursa motor DURMAZ.
   Bu, safety_io_on_standard_modules_forbidden ihlalidir.

✅ E-stop → F-DI (çift kanal) → Safety PLC/röle → F-DO/STO (çift kanal, donanımsal)
   Standart CODESYS yalnızca durumu OKUR ve HMI'da gösterir.
```

## Sık Yapılan Hatalar

### Hata 1: Emniyet I/O'yu Standart Modüle Bağlamak
En sık ve en tehlikeli hata. E-stop'u standart DI'ya bağlayıp yazılımda işlemek emniyet sağlamaz (`safety_io_on_standard_modules_forbidden`). Emniyet sinyalleri F-modüllerine gider.

### Hata 2: Black Channel'ı Emniyet Analizine Katmak
EtherCAT switch'inin/kablosunun SIL'ini sorgulamak gereksizdir — kara kanal emniyet analizine dahil değildir. Emniyet, FSoE/PROFIsafe katmanından gelir. (Tersi de hata: "ağ standart, demek emniyet yok" — emniyet katmanı bağımsız çalışır.)

### Hata 3: FSoE Watchdog'u Çok Uzun Ayarlamak
Watchdog süresi emniyet tepki süresini belirler. Çok uzun = tehlike geç algılanır; çok kısa = gürültüde yanlış tetik. Tepki süresi bütçesi (sensör + iletişim + mantık + aktüatör) hedefe göre hesaplanmalı ve test edilmeli.

### Hata 4: Emniyet ve Standart Mantığı Karıştırmak
Standart kodun emniyet değişkenini yazması/etkilemesi. Bir değişiklik tüm emniyet validasyonunu geçersiz kılar. İki dünya ayrık tutulur.

### Hata 5: FSoE Adresini Tekrar Kullanmak
İki cihaza aynı FSoE adresi vermek; sistem güvenli hale düşer ve "neden durdu" diye saatler harcanır. Her emniyet slave benzersiz adres alır.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Emniyet rölesi:** Az sayıda sabit fonksiyon, küçük makine, hızlı/ucuz validasyon. Programlanabilirlik gerekmiyorsa ilk tercih.
- **Safety PLC + safety fieldbus:** Çok bölge, çok eksen, muting/kademeli durdurma, esneklik ve ölçeklenebilirlik gerektiğinde.
- **FSoE:** EtherCAT ekosistemi (Beckhoff, Inovance SV660N gibi servolar) — doğal seçim.
- **PROFIsafe:** Siemens/PROFINET ağırlıklı tesis.
- **CIP Safety:** Rockwell/EtherNet-IP ekosistemi.

## Gerçek Proje Notları

**Not 1 — Emniyet rölesini küçümseme.** Basit bir hücrede Safety PLC dayatmak gereksiz karmaşıklık ve uzun validasyon getirir. Sabit mantıklı emniyet rölesi çoğu küçük makineyi karşılar; validasyonu "kablola, test et, mühürle" kadar basittir. Programlanabilirlik gerçekten gerekene kadar röle tercih edilir.

**Not 2 — FSoE, EtherCAT hattını tek kablo tutar.** Bir SV660N motion projesinde, emniyet için ayrı kablo çekmek yerine STO'yu FSoE üzerinden sürdük. Tek EtherCAT zinciri hem motion PDO hem emniyet container taşıdı. Kablolama ve pano alanı belirgin azaldı; black channel ilkesi sayesinde switch/kablo emniyet hesabına girmedi.

**Not 3 — "Aynı kasa, ayrı dünya"yı dokümante et.** Safety PLC'de emniyet ve standart programın ayrık olduğunu proje raporunda açıkça yazmak, hem denetimi hem ileride bakım yapacak ekibi korur. Standart koddan emniyet değişkenine erişim olmadığını gösteren bir mimari diyagram, validasyonu hızlandırır.

**Not 4 — STO geri beslemesini izle, ama tetikleme.** Standart CODESYS, sürücünün STO durumunu (aktif/pasif) OPC-UA/HMI'da gösterebilir — bu faydalı diyagnostiktir. Ama STO'yu *tetiklemek* emniyet katmanının (F-DO veya FSoE STO) işidir, standart kodun değil. Bu ayrımı karıştıran bir projede, STO standart koddan tetiklenmeye çalışıldı ve validasyon reddedildi.

**Not 5 — Watchdog asla sessizce kapatılmaz.** `agent/rules.json`: `watchdog_always_enabled`, `watchdog_disable_requires_written_justification`. Bir overrun'ı "watchdog'u kapatarak" çözmek emniyet ihlalidir; çözüm task yapısını düzeltmektir, watchdog'u susturmak değil.

## İlgili Konular

```
knowledge/safety/
├── 01_sil_pl_standards.md          → Kategori 3/4 = çift kanal = bu mimari
├── 03_safe_motion.md               → Sürücü STO'sunun F-DO/FSoE ile sürülmesi
└── 04_estop_and_safety_circuits.md → E-stop/ışık perdesi devresi, emniyet rölesi

knowledge/networking/_synthesis.md  → Fieldbus topolojisi (kara kanal taşıyıcı)
knowledge/inovance/inoproshop/05_ethercat_configuration.md → EtherCAT + SV660N kurulum
agent/safety_principles.md          → "Emniyet ≠ standart kontrol", I/O ayrımı
```
