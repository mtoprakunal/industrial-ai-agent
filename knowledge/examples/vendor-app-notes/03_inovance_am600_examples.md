---
KONU        : Inovance AM600 / InoProShop Örnek Uygulamaları (Motion + EtherCAT)
KATEGORİ    : examples
ALT_KATEGORI: vendor-app-notes
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.inovance.eu/fileadmin/downloads/Brochures/EN/AM600_Br_EN_Singles_Web_V2.2.pdf"
    başlık: "Inovance — AM600 Motion Controller broşürü (32 eksen, PLCopen, IEC 61131-3/CODESYS)"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/downloads"
    başlık: "Inovance EU — Downloads (InoProShop yazılımı, kılavuzlar, ESI dosyaları)"
    güvenilirlik: resmi
  - url: "https://www.manualslib.com/manual/2433383/Inovance-Ethercat-Md800.html?page=41"
    başlık: "Inovance MD800 EtherCAT Starting Guide — InoProShop Project Examples (AM/AC serisi, EtherCAT slave ekleme)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20SoftMotion/_sm_example_single_axis_motion_control.html"
    başlık: "CODESYS SoftMotion — Single Axis Motion Control örneği (InoProShop tabanı)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "knowledge/inovance/inoproshop/01_inoproshop_overview.md"
    ilişki: gerektirir
  - konu: "knowledge/inovance/inoproshop/06_motion_control.md"
    ilişki: detaylandırır
  - konu: "knowledge/inovance/inoproshop/05_ethercat_servo.md"
    ilişki: gerektirir
  - konu: "01_codesys_application_examples.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "InoProShop = CODESYS V3 ilişkisi (knowledge/inovance/inoproshop/01)"
  - "PLCopen / SoftMotion MC_ FB pattern'leri (knowledge/inovance/inoproshop/06)"
  - "EtherCAT master/slave ve CiA 402 servo profili temel kavramı"
ÇELİŞKİLER :
  - kaynak: "Beklenti: 'Inovance'ın CODESYS Store benzeri merkezi bir örnek deposu var'"
    konu: "Inovance örnekleri tek bir resmi 'examples' portalında toplu değildir"
    çözüm: >
      Inovance örnek/uygulama notları dağınık gelir: Downloads sayfası (InoProShop, ESI,
      kılavuzlar), ürün/uygulama starting guide'ları (örn. MD800/MD500 EtherCAT guide içindeki
      "InoProShop Project Examples"), ve distribütör/uygulama notları. InoProShop = CODESYS
      olduğundan, jenerik CODESYS SoftMotion örnekleri (bkz. doc 01) çoğu motion pattern'i için
      doğrudan kullanılabilir; Inovance'a özel kısım cihaz havuzu, ESI ve servo parametreleridir.
---

## Özün Ne

Inovance AM600 örnek uygulamaları, **InoProShop (= CODESYS V3) üzerinde Inovance'a özel
donanımı** (AM600 CPU, SV660N/IS620N servo, GL10/GL20 EtherCAT I/O, MD500/MD800 AC sürücü)
çalıştırma reçeteleridir. Öğrettikleri şey iki katmanlıdır: (1) **CODESYS ortak katmanı** —
PLCopen MC_ FB'leri, task yapısı, visualization; (2) **Inovance'a özel katman** — EtherCAT
master altına Inovance slave'lerinin ESI ile eklenmesi, CiA 402 ekseninin servoya bağlanması,
servo parametre/ölçek ayarı.

Neden önemli: Inovance ekosistemi (AM600 + EtherCAT servo + I/O) Avrupa/Türkiye'de yaygınlaşıyor
ve maliyet avantajlıdır. CODESYS SoftMotion bilgisi doğrudan transfer olduğundan, asıl
öğrenilecek şey "Inovance donanımını InoProShop'ta nasıl doğru bağlarım" pattern'idir —
örnek starting guide'lar tam bunu gösterir.

## Nasıl Çalışır

### Örneklerin geldiği kanallar

Inovance, CODESYS Store gibi tek merkezi bir örnek portalına sahip değildir (bkz. ÇELİŞKİLER).
Örnek/uygulama bilgisi şu kanallardan derlenir:

1. **Inovance Downloads (inovance.eu/downloads):** InoProShop yazılımı, AM600 yazılım/donanım
   kılavuzları (programlama örnekleri içerir), servo/sürücü ESI (EtherCAT XML) dosyaları.
2. **Ürün/Application Starting Guide'lar:** Örn. "MD800/MD500 EtherCAT Starting Guide" içindeki
   **"InoProShop Project Examples"** bölümü, AM/AC serisi denetleyiciyle bir EtherCAT AC
   sürücüyü adım adım bağlamayı gösterir.
3. **Jenerik CODESYS SoftMotion örnekleri:** InoProShop = CODESYS olduğundan, CODESYS Help/Store/Forge
   motion örnekleri (bkz. doc 01) Inovance ekseni üzerinde aynı pattern'le çalışır.

### Tipik AM600 örnek mimarisi

- **AM600 CPU** EtherCAT master rolünde; broşüre göre **32 eksene kadar** PTP, PLCopen
  kütüphanesiyle lineer/dairesel interpolasyon ve elektronik CAM (8 eksene kadar eşzamanlı),
  ayrıca robot kinematiği desteği (kaynak: AM600 broşürü).
- **EtherCAT hattı:** SV660N/IS620N servo (CiA 402) + GL10/GL20 RTU-ECT uzak I/O + opsiyonel
  MD500/MD800 AC sürücü.
- **Programlama:** IEC 61131-3 (ST/FBD/LD) + PLCopen MC_ FB'leri; visualization InoProShop
  içinde (CODESYS Visualization).

## Pratikte Nasıl Kullanılır

Starting guide örneklerinin öğrettiği tipik akış (kaynak: MD800/MD500 EtherCAT guide
"InoProShop Project Examples" + InoProShop=CODESYS motion akışı):

1. **Proje oluştur:** InoProShop'u başlat, hedef CPU'yu seç (örn. AM600-CPU1608TP) ve proje aç.
2. **EtherCAT Master ekle:** Network configuration'ı aç, CPU'yu seç, **EtherCAT Master**'ı etkinleştir.
3. **ESI import et:** Servo/sürücünün EtherCAT konfigürasyon dosyasını (ESI/XML) Device
   Repository'ye ekle (örn. MD500/SV660N ESI; Inovance destek portalından temin edilir).
4. **Slave ekle:** Cihaz listesinden sürücü/servo slave'ini master altına sürükle-bırak.
5. **CiA 402 Axis ekle (motion için):** Servo slave altına **SoftMotion CiA 402 Axis** ekle;
   InoProShop bir `AXIS_REF_SM3` üretir (bkz. inoproshop/06).
6. **Ölçek/parametre:** Eksen birim/devir + dişli oranını gir (SV660N 23-bit enkoder), servo
   parametrelerini ayarla.
7. **PLCopen mantığı yaz:** `MC_Power → MC_Home → MC_MoveAbsolute/MC_MoveVelocity → MC_Stop/MC_Reset`
   durum makinesi (bkz. inoproshop/06 örnek kodu — kendi yazımımız).
8. **İndir & devreye al:** Ethernet ile bağlan, login, indir, online debug; task monitor ile
   EtherCAT çevrim aşımını izle.

## Örnekler

"Ne öğretir" düzeyinde, Inovance örneklerinin tipik içeriği (telifli proje kopyalanmadan):

- **Tek eksen EtherCAT servo (SV660N/IS620N) pozisyonlama:** EtherCAT master + CiA 402 axis +
  PLCopen MC_ FB durum makinesi. Öğrettiği pattern: ESI ekleme → eksen bağlama → ölçek → güvenli
  güç-referans-hareket sırası (detaylı örnek kod: inoproshop/06).
- **MD500/MD800 AC sürücü EtherCAT'e bağlama (starting guide):** AM/AC serisi CPU altında AC
  sürücüyü slave olarak ekleme; öğrettiği şey saf motion değil, **sürücü-PLC EtherCAT
  entegrasyonu** ve PDO eşleme akışıdır (kaynak: MD800 EtherCAT Starting Guide, InoProShop
  Project Examples).
- **GL10/GL20 RTU-ECT uzak I/O:** EtherCAT üzerinden uzak DI/DO/AI/AO modülleri (her RTU-ECT
  ~16 DI/DO veya ~8 AI/AO); öğrettiği pattern: dağıtık I/O'yu master altına ekleyip değişkenlere
  eşleme.
- **Çok eksen interpolasyon / CAM:** PLCopen interpolasyon + CAM tablosu (8 eksene kadar
  eşzamanlı); jenerik CODESYS SoftMotion CAM/robotik örnekleri (doc 01) buraya transfer olur.

## Sık Yapılan Hatalar

- **InoProShop yerine AutoShop aramak.** AM600/AM400/AC800 örnekleri InoProShop'tadır; H5U/H3U/Easy
  örnekleri AutoShop'a aittir (CODESYS DEĞİL). Hedef ürünü doğru ortamla eşle (bkz. inoproshop/01).
- **ESI/sürüm uyuşmazlığı.** Yanlış veya eski ESI ile slave eklenince eksen/PDO eşlemesi tutmaz;
  InoProShop sürümü ↔ CPU firmware ↔ ESI sürümü uyumlu olmalı.
- **Ölçeği doğrulamadan üretime almak.** 23-bit enkoder + dişli oranı yanlışsa eksen yanlış mesafe
  gider; ilk işte "1 birim git" komutunu fiziksel ölçümle teyit et (bkz. inoproshop/06).
- **Motion'ı yavaş task'a koymak.** HMI/Modbus ile aynı yavaş task jitter yaratır; ayrı hızlı/senkron
  motion task kullan.
- **E-stop'u yazılıma emanet etmek.** MC_Stop güvenlik değildir; e-stop donanımsal STO + emniyet
  rölesi ile kurulur (SV660N'de CN6/STO; bkz. inoproshop/06 emniyet notu).
- **Starting guide'ı tam örnek sanmak.** Guide'lar genelde temel bağlantı adımlarını gösterir
  (örn. sayfa 41'de slave ekleme); CiA 402 axis, ölçek, PLCopen mantığı sonraki bölümlerde veya
  ayrı kılavuzlardadır. [DOĞRULANMADI] her guide'ın tam kapsamı sürüme göre değişir.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih:** Donanım Inovance AM600/AM400/AC800 + EtherCAT servo/I/O ise; maliyet avantajı +
  CODESYS tanıdıklığı birleşir. CODESYS SoftMotion bilen ekip için hızlı devreye alma.
- **Etme / dikkat:** H5U/H3U/Easy ise (AutoShop). Marka-bağımsız taşınabilirlik kritikse jenerik
  CODESYS + uygun device paketleri daha esnek olabilir. Çok özel/yüksek-uç motion veya zengin
  C++/Simulink entegrasyonu gerekiyorsa Beckhoff TwinCAT (doc 02) değerlendirilebilir.

## Gerçek Proje Notları

- **Asıl değer "Inovance'a özel bağlama" katmanında.** PLCopen mantığı CODESYS örneklerinden
  hazır gelir; Inovance örneklerinden öğrenilecek kritik şey ESI yönetimi, CiA 402 eşleme ve
  servo parametre/ölçek ayarıdır. Bu yüzden bir starting guide + jenerik CODESYS SoftMotion
  örneğini birlikte kullanmak en verimli kombinasyondur.
- **ESI dosyaları üretici portalından gelir.** Datasheet'lerde `download_url` boştur; ESI/firmware
  Inovance destek/distribütör kanalından temin edilir. Devreye almadan önce doğru ESI'yi edinin.
- **Mutlak multi-turn enkoder homing'i basitleştirir.** SV660N/IS620N pil yedekli mutlak enkoderdir;
  çoğu uygulamada bir kez homing yeter (bkz. inoproshop/06). Örnekleri uyarlarken "her açılışta
  homing" varsayımını gözden geçirin.
- **Broşür eksen/çevrim değerleri tavandır.** 32/16/8 eksen ve çevrim süreleri ideal koşul içindir;
  gerçek projede task monitor ile EtherCAT çevrim aşımını ölçün, gerekirse eksen yükünü/çevrimi
  yeniden boyutlandırın (bkz. inoproshop/06).
- **Dikey/yerçekimi yükü:** STO devreye girince eksen torksuz kalır; düşmeyi önlemek için servo
  motor freni şarttır — örnek projeler bunu çoğu zaman göstermez, sahada eklenmelidir.

## İlgili Konular

- `knowledge/inovance/inoproshop/01_inoproshop_overview.md` — InoProShop = CODESYS V3 tabanı
- `knowledge/inovance/inoproshop/06_motion_control.md` — PLCopen/SoftMotion MC_ FB örnek kodu, emniyet
- `knowledge/inovance/inoproshop/05_ethercat_servo.md` — EtherCAT master, CiA 402, ESI yönetimi
- `01_codesys_application_examples.md` — transfer edilebilir jenerik CODESYS motion örnekleri
- `02_beckhoff_twincat_samples.md` — alternatif ekosistem (TwinCAT) karşılaştırması
