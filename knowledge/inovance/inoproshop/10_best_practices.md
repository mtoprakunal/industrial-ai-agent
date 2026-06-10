---
KONU        : InoProShop En İyi Uygulamalar (Organizasyon, Performans, Güvenli Programlama)
KATEGORİ    : inovance
ALT_KATEGORI: inoproshop
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "agent/rules.json"
    başlık: "Agent Mühendislik Kuralları (timing, safety, naming, code_quality)"
    güvenilirlik: deneyimsel
  - url: "agent/quality_checklist.md"
    başlık: "Kalite Kontrol Listesi — Proje Kabul Kriterleri"
    güvenilirlik: deneyimsel
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_f_task_configuration.html"
    başlık: "CODESYS Online Help — Task Configuration (cycle/watchdog/priority)"
    güvenilirlik: resmi
  - url: "https://idea-tech.in/wp-content/uploads/2020/04/INOVANCE-AM400AM600AC800-PLC-SOFTWARE-MANUAL-ENGLISH-20-4-20.pdf"
    başlık: "Inovance — AM400/AM600/AC800 (InoProShop) User Guide"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_inoproshop_overview.md"
    ilişki: gerektirir
  - konu: "09_debugging.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/fundamentals/02_project_structure.md"
    ilişki: kullanır
  - konu: "knowledge/codesys/debugging/_synthesis.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "InoProShop = CODESYS V3 türevi; ilkeler CODESYS'e dayanır (01_inoproshop_overview.md)"
  - "Task/cycle/watchdog ve POU/GVL kavramları (knowledge/codesys/fundamentals/)"
  - "agent/rules.json mühendislik kurallarının kavranması"
ÇELİŞKİLER :
  - kaynak: "Kullanıcı eğilimi: 'emniyeti yazılımda interlock ile çözerim'"
    konu: "Emniyet yazılım mantığına bağlı OLMAMALIDIR"
    çözüm: >
      rules.json: emniyet garantisi donanımsal emniyet zincirinden gelir; yazılım
      destekler, garanti etmez. E-Stop donanımsal, fail-safe varsayılan = stop,
      CPU/watchdog arızasında tüm çıkışlar enerjisiz. InoProShop'ta safety, standart
      I/O modüllerine bağlanmaz.
  - kaynak: "Performans için watchdog'u kapatma eğilimi"
    konu: "Watchdog overrun'ı maskelemek için kapatılamaz"
    çözüm: >
      Watchdog daima açık; overrun varsa kök neden (bloke I/O, yük, döngü) çözülür.
      Kapatma yazılı gerekçe gerektirir ve emniyet ilkesine aykırıdır.
---

## Özün Ne

InoProShop bir CODESYS V3 türevi olduğundan, en iyi uygulamalar da CODESYS mühendislik
disiplininden ve bu agent'ın `rules.json` / `quality_checklist.md` kurallarından gelir.
Üç sütun vardır: **(1) proje organizasyonu ve isimlendirme**, **(2) performans/timing
disiplini**, **(3) güvenli programlama**. Bu üçü ayrı konular değil, tek bir
mühendislik tavrının yüzleridir: öngörülebilir, denetlenebilir, fail-safe bir sistem.

Temel ilke: **yazılım emniyeti destekler, garanti etmez.** Garanti donanımsal emniyet
zincirinden gelir; determinizm task disiplininden; bakım kolaylığı isimlendirme ve
tek-sorumluluk disiplininden gelir.

## Nasıl Çalışır

### 1) Proje Organizasyonu ve İsimlendirme

**İsimlendirme standardı (rules.json):**

```
Format : {Area}_{DeviceType}_{Number}_{Signal}
Örnek  : ZN1_MTR_01_RunCmd , TNK_LVL_02_PV
Kural  : ≤ 24 karakter · A-Z a-z 0-9 _ · boşluk yok ·
         başta rakam yok · reserved keyword yok
Tutarlılık: GVL ↔ io_list.csv ↔ HMI ↔ ağ adres haritası AYNI isim
```

**Proje yapısı:**
- POU'ları işleve göre klasörle (Motion / Process / Comm / Safety-monitoring / HMI).
- Global değişkenleri amaca göre GVL'lere böl (GVL_IO, GVL_Process, GVL_HMI); tek dev
  GVL'den kaçın.
- DUT (struct/enum) ile veri yapıla; sihirli sayı yerine sabit (constant) kullan.
- Her FB'nin **açıklaması** olmalı (rules.json: every_fb_must_have_description).
- Durum makinelerini açık **CASE** ile yaz (gizli IF zincirleri değil).

### 2) Performans / Timing Disiplini

**Task cycle hedefleri (rules.json):**

```
Sinyal türü            Max cycle   Task
─────────────────────────────────────────────────
Safety izleme          ≤ 1 ms      Safety (en yüksek öncelik)
Motion / sürücü        ≤ 2 ms      Task_Motion (EtherCAT senkron)
Hızlı interlock        ≤ 4 ms      Task_Fast
Analog / PID           ≤ 10 ms     Task_Control
Dijital sıralama       ≤ 20 ms     Task_Control
HMI / iletişim         ≤ 500 ms    Task_Comm / Background
Loglama / telemetri    ≤ 1000 ms   Task_Background / Freewheeling
```

**Kurallar:**
- Her task'ın **exec time < cycle time** olmalı; **Max** değere bak (ortalamaya değil).
- **Toplam CPU yükü ≤ %70** (manevra payı için).
- EtherCAT bus task önceliği ≤ 5.
- **Bloke I/O yalnız Freewheeling task'ta:** SysSockConnect, MQTT bağlantısı, dosya
  yazma, seri port, OPC-UA session açma. Bunlar kontrol/motion task'ında ASLA yer almaz.
- Hızlı sinyali yavaş task'a, yavaş sinyali hızlı task'a koyma (gecikme toleransı task'ı
  belirler).
- Watchdog overrun'ını **watchdog'u uzatarak/kapatarak çözme** — kök nedene in.

### 3) Güvenli Programlama

**İhlal edilemez emniyet ilkeleri (rules.json):**

```
□ Emniyet yazılım mantığına bağlı DEĞİL — garanti donanımsal zincirden gelir
□ E-Stop donanımsal; yazılım yalnız durumu yansıtır
□ Fail-safe varsayılan = STOP (run değil)
□ CPU/watchdog arızasında TÜM çıkışlar enerjisiz
□ Watchdog DAİMA açık (kapatma yazılı gerekçe ister)
□ Safety I/O standart modüllere bağlanmaz
□ Analog girişler aralık-dışı kontrolü (NAMUR NE107)
□ Interlock'lar merkezi ve gerekçeli (yorumlu)
```

**Kod kalitesi (rules.json code_quality):**
- Sihirli sayı yok → sabit kullan.
- Tek-sorumluluk: her FB tek iş yapar.
- Açık hata yönetimi (error_handling_explicit).
- Kontrol task'ında bloke çağrı yok.
- Pointer her scan yeniden hesaplanır, saklanmaz.
- REAL bölmelerde NaN / sıfıra-bölme kontrolü.
- RETAIN değişkenleri yalnız **sona** eklenir (layout bozulmasın); soğuk-başlatmada
  yaşaması gereken veri için PERSISTENT.

## Pratikte Nasıl Kullanılır

1. **Proje iskeletini kur:** İşlevsel POU klasörleri + amaç-bazlı GVL'ler + DUT'lar.
   İlk POU'dan önce isimlendirme standardını yaz, herkese uygula.
2. **Task yapısını planla:** Yukarıdaki cycle tablosuna göre task'ları oluştur; her
   sinyali doğru task'a ata. Watchdog'u her task'ta açık tut.
3. **Emniyeti donanıma yerleştir:** E-Stop, ışık perdesi, kapı kilidi donanımsal güvenlik
   rölesi/safety PLC zincirinde. InoProShop yalnız bu durumu **izler/yansıtır**, garanti
   etmez. Safety I/O'yu standart Inovance I/O modülüne bağlama.
4. **Kod yaz, disiplinle:** Açık CASE durum makineleri, sabitler, NaN/div-zero kontrolü,
   her FB'ye açıklama, tek-yazar disiplini (her register/node/topic tek yazar).
5. **Doğrula (quality_checklist.md):** Task Max < cycle, toplam CPU ≤ %70, force/breakpoint
   temizliği, watchdog açık, io_list/alarm_list tam, tüm I/O taglı.

## Örnekler

**İyi vs kötü isimlendirme:**

```
İYİ : ZN1_MTR_01_RunCmd   TNK_LVL_02_PV   CNV_VFD_03_SpdSP
KÖTÜ: motor1Calistir       seviye          hizAyari   (boşluksuz değil ama
       belirsiz, tutarsız, alan/tip/numara yok)
```

**İyi task ataması:**

```
Task_Safety  (1 ms, öncelik en yüksek)  → safety durum izleme
Task_Motion  (2 ms, EtherCAT senkron)   → MC_* eksen kontrol
Task_Control (10 ms)                    → PID, analog ölçekleme, sıralama
Task_Comm    (500 ms)                   → Modbus slave, OPC-UA, HMI güncelleme
Task_BG      (Freewheeling)             → MQTT publish, dosya log (bloke I/O burada)
```

**Sihirli sayı yerine sabit:**

```
// KÖTÜ:  IF tank_temp > 85.0 THEN ...
// İYİ:
VAR CONSTANT
    TNK_TMP_MAX_C : REAL := 85.0;  // tank üst sıcaklık eşiği (proses limiti)
END_VAR
IF TNK_TMP_01_PV > TNK_TMP_MAX_C THEN ...
```

## Sık Yapılan Hatalar

- **Emniyeti yazılıma yüklemek.** "E-Stop'u kod okur, çıkışı keser" yeterli değildir;
  emniyet donanımsal zincirden gelir, yazılım sadece yansıtır.
- **Watchdog'u kapatmak/uzatmak.** Overrun belirtisini silmek; kök neden (bloke I/O/yük)
  durur.
- **Bloke I/O'yu kontrol task'ında çalıştırmak.** MQTT/socket/dosya kontrol döngüsünü
  dondurur → watchdog. Freewheeling'e taşı.
- **Ortalama cycle'a güvenmek.** Determinizm en-kötü-durumdur; Max'a bak.
- **Tutarsız isimlendirme.** GVL'de bir, HMI'da başka isim → bakımda kaos. Tek standart,
  her katmanda aynı.
- **Tek dev GVL + tek dev PRG.** Bakımı imkânsızlaştırır; işleve böl, tek-sorumluluk FB.
- **RETAIN'i ortaya eklemek.** Bellek layout'unu kaydırır, eski değerler bozulur; sona ekle.
- **Sihirli sayılar.** Eşikleri koda gömmek; ayarlanamaz, izlenemez. Sabit kullan.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Bu disiplin her projede uygulanır.** İstisna yok; rules.json'daki `never` kuralları
  mutlaktır.
- **Watchdog kapatma yalnız** yazılı gerekçe + risk değerlendirmesiyle ve emniyet
  zinciri etkilenmiyorsa düşünülür — pratikte neredeyse hiç.
- **Esneklik isimlendirmede değil, mimaride.** İsim standardı katı; mimari (kaç task,
  hangi protokol) gereksinim-temelli akıl yürütmeyle seçilir, katı eşikle değil.

## Gerçek Proje Notları

- En çok teknik borç **isimlendirme tutarsızlığından** ve **tek dev GVL'den** doğar;
  proje başında 1 saatlik standart, aylarca bakım süresi kazandırır.
- Watchdog'u kapatma isteği neredeyse her zaman **gizli bir bloke-I/O** ya da **aşırı
  yük** işaretidir; kapatmak yerine Task Monitor Max ile kök nedeni bulmak doğru reflekstir.
- Inovance EtherCAT motion projelerinde en sık ihlal, motion task'ın yanlışlıkla bloke
  bir iletişim çağrısı içermesidir; bunu Freewheeling'e taşımak çoğu jitter/overrun
  sorununu çözer.
- "Tek yazılım hatası birini yaralayabilir mi?" sorusu teslim öncesi mutlaka cevaplanır;
  cevap "evet" ise o fonksiyon donanımsal emniyet zincirine taşınır — InoProShop kodunda
  bırakılmaz.
- "Orta" olgunluk: ilkeler güçlü (rules.json + CODESYS resmi); Inovance'a özgü tek fark
  cihaz/I/O isimleri ve modül yerleşimidir, mühendislik disiplini aynıdır.

## İlgili Konular

- `01_inoproshop_overview.md` — InoProShop = CODESYS V3 (taban)
- `09_debugging.md` — watchdog/EtherCAT/performans teşhisi
- `08_codesys_to_inoproshop.md` — taşımada task/isimlendirme gözden geçirme
- `knowledge/codesys/fundamentals/02_project_structure.md` — POU/GVL/Task/Library yapısı
- `agent/rules.json`, `agent/quality_checklist.md` — bağlayıcı mühendislik kuralları
