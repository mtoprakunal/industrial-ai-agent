---
KONU        : InoProShop Donanım Konfigürasyonu (AM600 / AC800 / I/O)
KATEGORİ    : inovance
ALT_KATEGORI: inoproshop
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.inovance.eu/products/motion-controllers-i/o-modules/am600-motion-controllers"
    başlık: "Inovance — AM400/AM600 Motion Controllers (ürün sayfası)"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/fileadmin/downloads/Brochures/EN/AM600_Br_EN_Singles_Web_V2.2.pdf"
    başlık: "Inovance — AM600 Motion Controller broşürü (Data code L6210221 V2.2)"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/fileadmin/downloads/AC_Drives_LV/AC800_Fl_EN_Singles_Web_V0.1__1_.pdf"
    başlık: "Inovance — AC800 Series IPC Motion Controller (flyer)"
    güvenilirlik: resmi
  - url: "https://www.manualslib.com/manual/2433383/Inovance-Ethercat-Md800.html?page=41"
    başlık: "Inovance EtherCAT MD800 — InoProShop proje oluşturma / ağ konfigürasyonu (AM/AC serisi)"
    güvenilirlik: topluluk
  - url: "https://www.inovance.eu/products/plcs-hmis/gl20-i/o-modules"
    başlık: "Inovance — GL20 I/O Modules (ürün sayfası)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_inoproshop_overview.md"
    ilişki: gerektirir
  - konu: "05_ethercat_configuration.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: gerektirir
  - konu: "devices/INOVANCE_AM600/datasheet.json"
    ilişki: kullanır
  - konu: "devices/INOVANCE_GL20/datasheet.json"
    ilişki: kullanır
ÖNKOŞUL     :
  - "InoProShop = CODESYS V3 gerçeği (01_inoproshop_overview.md)"
  - "CODESYS Device Tree / Device Repository kavramı (knowledge/codesys/fundamentals/)"
  - "IEC 61131-3 %I / %Q adresleme mantığı"
ÇELİŞKİLER :
  - kaynak: "Yaygın varsayım: 'H5U InoProShop'ta donanım olarak yapılandırılır'"
    konu: "H5U / H3U / Easy serisi InoProShop ile YAPILANDIRILMAZ — Inovance AutoShop kullanır"
    çözüm: >
      Doğrulanmış olgu: InoProShop (CODESYS V3 tabanlı) yalnızca AM400 / AM600 / AC800
      orta-sınıf kontrolörleri programlar ve donanım ağacını oluşturur. H5U/H3U/Easy
      küçük PLC'leri Inovance'ın AutoShop ortamına aittir (CODESYS DEĞİL). Bu belgedeki
      donanım konfigürasyonu yalnızca AM600/AC800 için geçerlidir; H5U için aşağıdaki
      UYARI bölümüne bakın ve AutoShop'a yönlendirin. GL20 I/O modülü ise hem H5U
      (AutoShop) hem AM600 (InoProShop) tarafından kullanılabilir — modülün kendisi
      ortamdan bağımsızdır, onu yapılandıran ortam farklıdır.
---

## Özün Ne

InoProShop'ta donanım konfigürasyonu, projenin **Device Tree'sini** (cihaz ağacını)
kurmaktır: hangi kontrolör (AM600/AC800), CPU yanına hangi lokal genişletme modülleri,
EtherCAT hattına hangi uzak I/O ve servo sürücüler gelecek — bunların tamamı
CODESYS V3 Device Tree mantığıyla tanımlanır. InoProShop CODESYS türevi olduğu için
bu işlem birebir CODESYS'tir: ağaca cihaz eklenir, modüller "plug device" olarak
takılır, I/O kanalları **%I / %Q** adreslerine eşlenir (I/O Mapping).

Neden önemli: Donanım ağacı yanlış kurulursa derleme geçse bile saha çalışmaz —
yanlış CPU sipariş kodu, eksik modül, ya da yanlış I/O eşlemesi devreye almada
en sık görülen kayıp zamandır. Ayrıca **doğru ürünü doğru ortamla eşlemek** (AM600 →
InoProShop, H5U → AutoShop) bu işin sıfırıncı adımıdır.

## ⚠️ ÖNEMLİ UYARI — H5U / H3U / Easy InoProShop'ta YAPILANDIRILMAZ

Bu, Inovance ekosisteminde en sık yapılan kategori hatasıdır ve burada bilinçli
olarak uydurulmamıştır:

- **InoProShop yalnızca AM400 / AM600 / AC800** orta-sınıf, CODESYS V3 tabanlı
  kontrolörlerin donanımını yapılandırır.
- **H5U / H3U / Easy serisi** küçük PLC'ler **Inovance AutoShop** ile yapılandırılır
  (CODESYS DEĞİL; kendi LD/SFC ortamı). Bu ürünleri InoProShop'ta donanım olarak
  ekleyemezsiniz; cihaz havuzunda CPU olarak görünmezler.
- Eğer eldeki kontrolör H5U ise: **bu belgeyi kullanmayın**, AutoShop dokümantasyonuna
  geçin. GL20 I/O ve SV660N/IS620N servo gibi *slave* cihazlar her iki ortamda da
  kullanılabilir, ancak bunları **yapılandıran master ortamı** ürüne göre değişir.

Bu çelişki frontmatter'daki ÇELİŞKİLER alanında ve 01_inoproshop_overview.md'de de
kayıtlıdır.

## Nasıl Çalışır

### Device Tree (CODESYS mirası)

InoProShop projesi bir kök **Device** (kontrolör) ile başlar. Altında katmanlı bir
ağaç oluşur:

```
Device (AM600-CPU1608TP)          ← kontrolör; CODESYS Control runtime burada
├── PLC Logic
│   └── Application (POU'lar, GVL, Task Configuration)
├── <Lokal genişletme bus'ı>      ← GL10 modülleri CPU yanına takılır
│   ├── GL10-xxxx (DI/DO/AI/AO)
│   └── ...
└── EtherCAT_Master               ← EtherCAT alanı (bkz. 05_ethercat_configuration.md)
    ├── GL20-RTU-ECT (bus coupler) → arkasına GL20 modülleri
    ├── SV660N (CiA402 servo)
    └── IS620N (CiA402 servo)
```

- **Lokal modüller** doğrudan CPU'nun arka bus'ına takılır (AM600 için GL10 ailesi;
  datasheet: CPU başına 16 lokal GL10 modülüne kadar).
- **Uzak / dağıtık I/O ve servo** EtherCAT master altına gelir (datasheet: EtherCAT
  üzerinden 125 slave istasyona kadar).

### Adresleme: %I / %Q (IEC 61131-3 / CODESYS mantığı)

Her dijital/analog kanal otomatik bir bellek adresi alır:

- `%I` = giriş image (Input): `%IX`, `%IB`, `%IW`, `%ID` (bit/byte/word/dword)
- `%Q` = çıkış image (Output): `%QX`, `%QB`, `%QW`, `%QD`
- `%M` = işaretçi/marker bellek

InoProShop bu adresleri otomatik atar; mühendis **I/O Mapping** sekmesinde her
kanalı anlamlı bir değişkene (tercihen bir GVL değişkenine) bağlar. Uzman pratiği:
ham `%IX0.0` adreslerini koda yazmak yerine `GVL_IO.bStartButton` gibi sembolik
isimlerle eşlemek — adres kayması (modül ekle/çıkar) kodu kırmaz.

## Pratikte Nasıl Kullanılır

### AM600 Donanım Konfigürasyonu (adım adım)

1. **Proje oluştur:** InoProShop'u başlat → New Project → hedef cihaz olarak doğru
   CPU'yu seç. Sipariş kodu kritik: örn. **AM600-CPU1608TP** (16 HSC giriş / 8 HS çıkış,
   TP = source/PNP) veya **TN** (sink/NPN). (datasheet: AM600 sipariş kodu TP 01440168 /
   TN 01440064.)
2. **CPU yerleşik I/O:** AM600 CPU'da 16 yüksek hızlı DI + 8 yüksek hızlı DO yerleşiktir;
   ayrıca 8 kanal A/B faz darbe sayacı (kanal başına ≤200 kHz) ve 4 grup 200 kHz
   pozisyonlama darbe çıkışı vardır (datasheet). Bunlar Device Tree'de CPU altında
   görünür ve %I/%Q'ya eşlenir.
3. **Lokal genişletme ekle:** Device Tree'de CPU'ya sağ tık → **Plug Device** → GL10
   modüllerini ekle (örn. GL10-4AD analog giriş, GL10-4DA analog çıkış). Modül sırası
   fiziksel donanım sırasıyla AYNI olmalıdır.
4. **Güç:** AM600 sistemi GL10-PS2 güç modülüyle beslenir (220 VAC → 24 VDC / 2 A);
   CPU girişi +24 VDC (datasheet). Güç bütçesi modül sayısıyla doğrulanmalı.
5. **EtherCAT alanı:** Uzak I/O ve servo için EtherCAT master ekle → bkz.
   05_ethercat_configuration.md.
6. **I/O Mapping:** Her modülün kanallarını GVL değişkenlerine bağla.
7. **İndir & doğrula:** Online'a geç, gerçek donanım topolojisinin ağaçla eşleştiğini
   doğrula (modül eksik/fazla uyarıları).

### AC800 Donanım Konfigürasyonu

AC800, AM600'den farklı olarak bir **IPC (endüstriyel PC) tabanlı** motion
kontrolördür ve yine InoProShop / CODESYS ile programlanır:

- **Platform:** Intel işlemci (modele göre **Core i5 ~2.3 GHz** veya **Celeron
  ~1.6 GHz**); işletim sistemi **LinuxRT** (gerçek-zaman Linux), CODESYS Control
  runtime üzerinde. (Kaynak: AC800 flyer + click2electro spesifikasyon özeti — resmi
  flyer'dan teyit edilmesi önerilir.)
- **Eksen:** EtherCAT bus tabanlı motion ile **256 eksene kadar** (AM600'ün 32
  ekseninin çok üzerinde). PLCopen + CAM + CNC + Robot bileşenleri.
- **EtherCAT portları (model bazlı, ⚠️ teyit edilmeli):**
  - **AC801** → tek EtherCAT master
  - **AC802 / AC810** → çift EtherCAT master (ayrı ağlar veya yedeklilik/redundancy)
  (Kaynak: click2electro özeti; kesin model/port eşlemesi resmi AC800 donanım
  kılavuzundan doğrulanmalıdır — bu belgede tahmin edilmemiştir.)
- **Haberleşme:** EtherCAT, EtherNet/IP, OPC UA, Modbus TCP, Modbus RTU
  master/slave (RS485 + RS232).
- **Konfigürasyon akışı:** AM600 ile aynı CODESYS Device Tree mantığı. Fark, AC800'ün
  lokal arka-bus genişletme modülü yerine **tüm I/O ve eksenleri EtherCAT üzerinden**
  alması (IPC olduğu için yerel modül bus'ı yoktur; I/O dağıtık GL20/GR10 üzerinden gelir).

### GL20 Dağıtık I/O Donanım Yerleşimi

GL20 hem AM600 hem AC800 ile kullanılabilir (ayrıca H5U/Easy ile AutoShop tarafında):

- **EtherCAT bus coupler:** GL20-RTU-ECT (datasheet sipariş kodu 1440286). Arkasına
  **16 genişletme modülüne kadar** DI/DO/AI/AO/sıcaklık modülü eklenir.
- **Modül örnekleri (datasheet):** GL20-1600END (16 DI), GL20-0016ETN (16 DO transistör),
  GL20-0008ER (8 DO röle), GL20-4AD (4 AI 16-bit), GL20-4DA (4 AO 16-bit), GL20-4PT
  (RTD), GL20-4TC (termokupl), GL20-0808ETN / GL20-3232ETN-M (kombo).
- **Yerleşim seçeneği:** GL20 modülleri ya bir coupler arkasına (EtherCAT slave olarak,
  uzak) ya da doğrudan AM600 CPU yanına (lokal) eklenebilir (datasheet). Donanım ağacında
  hangisi seçildiyse fiziksel kurulum ona uymalıdır.
- I/O verisi PDO eşlemesiyle gelir → I/O Mapping → GVL → kod (bkz. 05).

## Örnekler

### Örnek 1 — AM600 motion hücresi donanım ağacı

```
Device (AM600-CPU1608TP)
├── PLC Logic / Application
│   ├── GVL_IO            ← tüm fiziksel I/O sembolleri
│   ├── GVL_Axis          ← eksen referansları
│   └── Task_EtherCAT (Prio yüksek), Task_Logic (10 ms)
├── <CPU yerleşik> 16 DI / 8 DO  → GVL_IO.* (%IX, %QX)
├── GL10-4AD (lokal)      → GVL_IO.rAnalogIn[0..3] (%IW)
└── EtherCAT_Master
    ├── GL20-RTU-ECT
    │   ├── GL20-1600END  → GVL_IO.bRemoteIn[0..15] (%IX)
    │   └── GL20-0016ETN  → GVL_IO.bRemoteOut[0..15] (%QX)
    ├── SV660N  → SoftMotion CiA402 Axis (Axis_X)
    └── SV660N  → SoftMotion CiA402 Axis (Axis_Y)
```

### Örnek 2 — I/O Mapping satırı (kavramsal)

```
Channel        Address   Type   Mapping (Variable)
Input Bit 0    %IX0.0    BOOL   GVL_IO.bEStop
Input Bit 1    %IX0.1    BOOL   GVL_IO.bStartPB
Output Bit 0   %QX0.0    BOOL   GVL_IO.bLampGreen
AI Channel 0   %IW2      INT    GVL_IO.iPressureRaw
```

## Sık Yapılan Hatalar

- **H5U'yu InoProShop'ta açmaya çalışmak.** En büyük kategori hatası — yukarıdaki
  UYARI bölümüne bakın; AutoShop kullanın.
- **Yanlış CPU sipariş kodu (TP vs TN).** TP = source/PNP çıkış, TN = sink/NPN. Yanlış
  seçim sahada çıkışların hiç çalışmamasına yol açar; kod doğru görünse bile.
- **Device Tree modül sırası ≠ fiziksel sıra.** Lokal GL10 / coupler arkası GL20
  modülleri fiziksel takılı sırayla AYNI olmalı; yoksa I/O kanalları kayar.
- **Ham %IX adresini koda gömmek.** Modül ekleyince adres kayar, kod sessizce yanlış
  kanalı okur. Daima GVL sembolüne eşle.
- **Güç bütçesini atlamak.** Modül sayısı arttıkça 24 VDC besleme bütçesi aşılabilir;
  güç modülü kapasitesi (GL10-PS2: 2 A) kontrol edilmeli.
- **AC800'ü AM600 gibi lokal modüllü sanmak.** AC800 IPC'dir; I/O EtherCAT'tan gelir,
  arka-bus lokal modül yoktur.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **AM600:** ≤32 eksen, modüler PLC + lokal I/O + EtherCAT motion gereken klasik makine
  otomasyonu. CPU yerleşik HSC/darbe çıkışı sayesinde hızlı I/O işleri için ideal.
- **AC800:** Yüksek eksen sayısı (256'ya kadar), CNC/robot, yüksek hesaplama yükü ya da
  çift EtherCAT ağı/redundancy gereken IPC-sınıfı uygulamalar. Daha pahalı, daha güçlü.
- **InoProShop kullanma:** Donanım H5U/H3U/Easy ise → AutoShop. Çoklu-marka vendor-bağımsız
  proje gerekiyorsa jenerik CODESYS daha esnek olabilir (bkz. 01).

## Gerçek Proje Notları

- **Doğru ürün-ortam eşlemesi sıfırıncı adımdır.** Sahaya gidip H5U'yu InoProShop'ta
  açmaya çalışan ekip yarım gün kaybeder. Teklif/BOM aşamasında kontrolör serisi
  netleşmeli; AM/AC → InoProShop, H5U/Easy → AutoShop.
- **TP/TN seçimi devreye almada gizli hatadır.** Donanım ağacında TP seçip sahada TN
  takılı olduğunda derleme geçer, online bağlanır, ama çıkışlar PNP/NPN uyumsuzluğundan
  beklenen şekilde sürmez. Sipariş kodunu fiziksel etikete karşı doğrulayın.
- **AC800 spesifik sayıları (port sayısı, cycle time) modele çok bağlı.** Bu belgede
  i5/Celeron, LinuxRT, 256 eksen ve AC801/802/810 EtherCAT port farkı topluluk/flyer
  kaynaklıdır; kesin sayıları proje öncesi resmi AC800 donanım kılavuzundan teyit edin.
- **GL20 yerel mi uzak mı?** Kabin tasarımına göre karar verin: coupler arkası = uzak
  hat (kablo tasarrufu, EtherCAT gecikmesi); CPU yanı = lokal (en düşük gecikme).
  Ağaçtaki seçim fiziksel kuruluma birebir uymalı.

## İlgili Konular

- `05_ethercat_configuration.md` — EtherCAT master/slave, ESI, sync mode, DC
- `01_inoproshop_overview.md` — InoProShop = CODESYS V3 (taban)
- `knowledge/codesys/fundamentals/` — Device Tree, %I/%Q, runtime mimarisi
- `devices/INOVANCE_AM600/datasheet.json` — AM600 CPU/I/O/sipariş kodu gerçekleri
- `devices/INOVANCE_GL20/datasheet.json` — GL20 modül listesi ve coupler gerçekleri
