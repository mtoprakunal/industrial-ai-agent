---
KONU        : InoProShop Proje Yapısı
KATEGORİ    : inovance
ALT_KATEGORI: inoproshop
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://idea-tech.in/wp-content/uploads/2020/04/INOVANCE-AM400AM600AC800-PLC-SOFTWARE-MANUAL-ENGLISH-20-4-20.pdf"
    başlık: "Inovance — AM400/AM600/AC800 Medium-Sized PLC Software (InoProShop) User Guide"
    güvenilirlik: resmi
  - url: "https://www.manualslib.com/manual/2433383/Inovance-Ethercat-Md800.html?page=41"
    başlık: "Inovance EtherCAT MD800 Starting Manual — InoProShop Project (AM/AC Series)"
    güvenilirlik: topluluk
  - url: "https://docs.planarmotor.com/tech-portal/inovance-inoproshop"
    başlık: "Planar Motor — Inovance InoProShop (proje oluşturma, Devices tree, Library Manager, EtherCAT)"
    güvenilirlik: topluluk
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_struct_project_creation.html"
    başlık: "CODESYS Online Help — Creating and Configuring a Project (.project, .projectarchive)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_mapping_hardware_in_device_tree.html"
    başlık: "CODESYS Online Help — Mapping Hardware in Device Tree"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/news/details/inovance-has-worked-with-codesys-since-2015-is-now-listed-on-the-codesys-website-173"
    başlık: "Inovance — CODESYS ile 2015'ten beri çalışıyor (resmi haber)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_inoproshop_overview.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/fundamentals/02_project_structure.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: gerektirir
  - konu: "03_iec61131_in_inoproshop.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/libraries/01_standard_libraries.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "InoProShop genel bakış ve InoProShop = CODESYS V3 türevi gerçeği (01_inoproshop_overview.md)"
  - "CODESYS V3 proje iç yapısı: Device tree, Application, Task, GVL, POU, Library Manager (knowledge/codesys/fundamentals/02_project_structure.md)"
  - "CODESYS runtime kavramı (knowledge/codesys/fundamentals/01_runtime_architecture.md)"
ÇELİŞKİLER :
  - kaynak: "Proje dosyası uzantısı — resmi InoProShop dokümanında metin olarak teyit edilemedi"
    konu: >
      InoProShop'un kaydettiği proje dosyasının uzantısı (CODESYS V3'teki gibi .project mı,
      yoksa Inovance'a özel bir uzantı mı) erişilebilen kaynaklarda açıkça yazılı değildir.
      Web kaynakları bunu CODESYS tabanından çıkarımla ".project" diye tahmin etmektedir.
    çözüm: >
      Bu belge uzantıyı TAHMİN ETMEZ. InoProShop CODESYS V3 türevi olduğundan büyük olasılıkla
      CODESYS V3 formatını (.project + taşınabilir .projectarchive) kullanır; ancak kesin uzantı
      Inovance InoProShop dokümanından / kurulu yazılımda File > Save As diyalogundan
      DOĞRULANMALIDIR. Belge boyunca uzantı "doğrulanmalı" olarak işaretlenmiştir.
  - kaynak: "AutoShop ile karışıklık"
    konu: "H5U/H3U/Easy projeleri InoProShop ile DEĞİL AutoShop ile açılır; proje yapısı tamamen farklıdır"
    çözüm: >
      Bu belge yalnızca InoProShop'un (AM400/AM600/AC800) CODESYS V3 tabanlı proje yapısını
      kapsar. AutoShop proje yapısı CODESYS değildir ve kapsam dışıdır.
---

## Özün Ne

InoProShop'ta bir proje açtığınızda gördüğünüz yapı **CODESYS V3 proje yapısının birebir
kendisidir**. Inovance, CODESYS Development System çekirdeğini kendi cihaz havuzu, motion
kütüphaneleri ve EtherCAT yığınıyla paketler; ama projenin iskeleti değişmez: sol panelde
bir **Device tree (Devices görünümü)**, altında **PLC Logic → Application**, onun içinde
**Library Manager**, **Task Configuration**, **PLC_PRG**, **GVL**, **DUT** ve görselleştirme
düğümleri yer alır. Bu yüzden CODESYS V3 proje yapısını bilen bir mühendis InoProShop projesini
ilk açtığında neredeyse hiçbir şeyi yeniden öğrenmez.

Neden önemli: Inovance donanımını (AM600 + EtherCAT servo + GL20 I/O) verimli kullanmak,
neyin nereye yazılacağını bilmeyi gerektirir. Bu bilgi doğrudan CODESYS bilgi tabanından
(`knowledge/codesys/fundamentals/02_project_structure.md`) transfer olur; bu belge yalnızca
Inovance'a özgü farkları ve doğrulama noktalarını ekler.

## Nasıl Çalışır

### Proje / Çözüm Dosya Formatı

InoProShop, CODESYS V3 mimarisini miras aldığından **tek bir proje dosyası** mantığıyla
çalışır (CODESYS'teki `.project` gibi). CODESYS V3'te bu dosya XML/obje-grafiği hibrit bir
konteynerdir; içinde kaynak kodlar, cihaz konfigürasyonu, kütüphane referansları ve I/O
eşleştirmeleri gömülüdür. Taşınabilir paylaşım için CODESYS, bağımlılıkları da içeren bir
**arşiv** formatı (`.projectarchive`) sunar.

> **DOĞRULANMALI — dosya uzantısı:** InoProShop'un kaydettiği proje dosyasının kesin uzantısı,
> erişilebilen resmi Inovance dokümanında metin olarak teyit edilememiştir. CODESYS V3 türevi
> olması nedeniyle büyük olasılıkla CODESYS V3 formatını (`.project` ve taşınabilir
> `.projectarchive`) kullanır; ancak bu **tahmindir**. Kesin uzantı, kurulu InoProShop'ta
> `File > Save Project As` diyalogundaki dosya filtresinden veya Inovance InoProShop kullanım
> kılavuzundan doğrulanmalıdır. (Bkz. ÇELİŞKİLER.)

### CODESYS .project ile Benzerlikler ve Farklar

**Benzerlikler (neredeyse tamamı ortak):**

- Tek proje dosyası + ayrı taşınabilir arşiv mantığı.
- Dosyanın satır-bazlı Git merge'e uygun OLMAMASI: CODESYS proje dosyası GUID'ler, sıralı
  ID'ler ve gömülü blob'lar içerir; satır diff bozuk proje üretebilir (bkz. CODESYS belgesi
  Not 6). Aynı tuzak InoProShop için de geçerlidir.
- Kütüphane referanslarının dosyaya gömülmemesi; yalnızca (isim, sürüm, namespace) tutulması.
  Bu yüzden proje dosyası taşınınca kütüphaneler/ESI'ler eksik kalabilir.

**Farklar (Inovance'a özgü):**

- **Cihaz havuzu önceden dolu:** Yeni proje açarken hedef olarak Inovance kontrolörleri
  (örn. `AM600-CPU1608TP`, AM400, AC800) doğrudan listelenir; jenerik CODESYS dağıtımında bu
  cihazlar ayrıca yüklenir.
- **Inovance motion/EtherCAT bileşenleri** kurulumla birlikte gelir (PLCopen MC_* kütüphanesi,
  Inovance servo ESI'leri, GL20 I/O modülleri).
- Sürüm uyumu InoProShop sürümü ile kontrolör firmware'i arasında aranır (CODESYS'teki device
  description sürüm tuzağının Inovance karşılığı — bkz. CODESYS belgesi Not 7).

### Cihaz Ağacı (Device Tree) Yapısı

InoProShop'ta Devices görünümü, fiziksel donanım topolojisini birebir yansıtır — CODESYS ile
aynı hiyerarşi:

```
[Proje Dosyası]  ← uzantı DOĞRULANMALI (muhtemelen .project)
│
└── Device  (örn. AM600-CPU1608TP)        ← Inovance kontrolör, device description ile tanımlı
    │
    ├── PLC Logic
    │   └── Application
    │       ├── Library Manager           ← Inovance + standart CODESYS kütüphaneleri
    │       ├── Task Configuration
    │       │   └── MainTask  (EtherCAT bus cycle ile senkron olabilir)
    │       │       └── PLC_PRG
    │       ├── PLC_PRG  (varsayılan PROGRAM POU)
    │       ├── GVL  (Global Variable List)
    │       ├── DUT  (STRUCT / ENUM / ALIAS)
    │       └── Visualization (WebVisu / TargetVisu)
    │
    └── EtherCAT_Master                    ← Inovance kontrolörün dahili EtherCAT master'ı
        ├── SV660N_Drive_1 (Slave)         ← Inovance servo (ESI ile)
        │   └── I/O Mapping (PDO → GVL)
        └── GL20_IO_Coupler (Slave)        ← Inovance uzak I/O
            └── I/O Mapping
```

Network Configuration ekranından EtherCAT master etkinleştirilir, slave cihazlar (servo,
I/O) ECT/ESI dosyalarıyla içe aktarılıp ağaca sürüklenir. I/O adresleri (`%I`, `%Q`) bu
hiyerarşiden otomatik türetilir — bir slave'i ağaçta taşımak alt kanal adreslerini kaydırır
(CODESYS belgesi Not 8'deki tehlikeli tuzağın aynısı: doğrudan `AT %` adresleme yerine
sembolik I/O Mapping kullanın).

### Kütüphane Yönetimi (Library Manager + Inovance Cihaz Havuzu)

İki ayrı kavram vardır, karıştırılmamalıdır:

1. **Library Manager (kütüphaneler):** Application altındaki düğüm; tekrar kullanılabilir POU
   koleksiyonlarını (standart CODESYS kütüphaneleri + Inovance motion/iletişim kütüphaneleri)
   projeye ekler ve sürümlerini yönetir. Dahili kütüphane (`*.library`, kaynak açık) ve
   derlenmiş kütüphane (`*.compiled-library-v3`, IP korumalı) ayrımı CODESYS ile aynıdır.
   Sürüm sabitleme kuralı InoProShop'ta da geçerlidir: "newest" yerine sürüm sabitleyin.

2. **Device Repository (cihaz havuzu):** Tools menüsünden erişilen, kontrolör/servo/I/O
   *cihaz tanımlarının* (device description + EtherCAT ESI) tutulduğu havuz. InoProShop bu
   havuzu Inovance ürünleriyle önceden doldurur; üçüncü taraf cihazlar ESI/GSDML ile eklenir.
   Library Manager kod kütüphanesini, Device Repository ise donanım tanımını yönetir.

## Pratikte Nasıl Kullanılır

1. **Yeni proje:** `File > New Project > Standard Project`. Kategori Standard Project, hedef
   PLC olarak Inovance kontrolörü seç (örn. AM600-CPU1608TP), programlama dili seç (genelde
   Structured Text), projeye isim ver, OK. Bu işlem otomatik olarak Device, Application,
   Library Manager, Task Configuration (MainTask) ve PLC_PRG'yi oluşturur (CODESYS ile aynı).
2. **Cihaz ağacını kur:** Network Configuration'da EtherCAT Master'ı etkinleştir; servo/I/O
   slave'lerini ESI ile içe aktar ve ağaca ekle.
3. **POU/GVL/DUT ekle:** Application'a sağ tık > Add Object ile FB, GVL, DUT ekle (CODESYS ile
   birebir akış — bkz. `knowledge/codesys/fundamentals/02_project_structure.md`).
4. **I/O Mapping:** Her slave altındaki I/O Mapping ekranından fiziksel kanalları GVL
   değişkenlerine sembolik olarak bağla.
5. **Kütüphane ekle:** Library Manager > Add Library ile motion (MC_*) ve standart
   kütüphaneleri sürüm-sabit ekle.
6. **Kaydet / paylaş:** Projeyi kaydet; takıma taşırken bağımlılıkları içeren arşiv formatını
   tercih et (uzantı doğrulanmalı; CODESYS karşılığı `.projectarchive`).

## Örnekler

### Örnek 1 — AM600 motion projesinin ağaç iskeleti

```
MachineProject  (uzantı DOĞRULANMALI)
└── AM600-CPU1608TP
    └── PLC Logic
        └── Application
            ├── Library Manager
            │   ├── Standard.library
            │   ├── Util.library
            │   └── [Inovance Motion / MC_* kütüphanesi]
            ├── Task Configuration
            │   ├── EtherCAT_Task (bus cycle ile senkron, yüksek öncelik)
            │   │   └── PRG_Motion
            │   └── Task_Main (10ms)
            │       └── PRG_MachineLogic
            ├── PRG_Motion          (PROGRAM, ST)
            ├── PRG_MachineLogic    (PROGRAM, ST)
            ├── FB_AxisControl      (FUNCTION_BLOCK, ST — MC_* sarmalar)
            ├── GVL_IO / GVL_Params / GVL_Alarms
            └── DUT_AxisData (STRUCT)
        └── EtherCAT_Master
            ├── SV660N_Axis1 → I/O Mapping
            ├── SV660N_Axis2 → I/O Mapping
            └── GL20_DI16DO16 → I/O Mapping
```

### Örnek 2 — Library Manager vs Device Repository ayrımı

- "Eksenleri MC_MoveAbsolute ile sürmek istiyorum" → **Library Manager**'a motion kütüphanesini
  ekle (kod).
- "Yeni bir SV660N servoyu ağaca eklemek istiyorum ama listede yok" → **Device Repository**'ye
  servonun ESI dosyasını kur (donanım tanımı), sonra ağaca sürükle.

## Sık Yapılan Hatalar

- **Proje dosyasını Git'te satır-bazlı merge etmek.** CODESYS türevi proje dosyaları satır
  diff'e uygun değildir; bozuk proje üretir. Git'i yedek/geçmiş için kullanın, paralel çalışma
  için mantığı kütüphanelere bölün veya object-level export kullanın.
- **`AT %` doğrudan adresleme.** Slave eklenince tüm adresler kayar, yanlış kanallar sürülür
  (tehlikeli). Sembolik I/O Mapping kullanın.
- **Library Manager ile Device Repository'yi karıştırmak.** Kod kütüphanesi eksikse Library
  Manager'a, cihaz ağaca eklenemiyorsa Device Repository'ye (ESI) bakın.
- **Kütüphane/firmware sürüm uyumsuzluğu.** InoProShop sürümü, kütüphane sürümü ve kontrolör
  firmware'i uyumlu olmalı; "newest" kütüphane modu beklenmedik kırılmalara yol açar.
- **AutoShop projesini InoProShop'ta açmaya çalışmak.** H5U/H3U/Easy yapısı bu belgenin kapsamı
  dışındadır; tamamen farklı bir ortamdır.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Bu yapıyı kullan:** Donanım AM400/AM600/AC800 olduğunda. Proje yapısını kurarken CODESYS V3
  best-practice'lerini (kütüphane-merkezli mimari, katmanlı GVL, FB'lere kapsülleme, sürüm
  sabitleme) doğrudan uygula — hepsi InoProShop'ta geçerlidir.
- **Etme:** Donanım H5U/H3U/Easy ise (AutoShop, farklı proje yapısı). Tek bir CODESYS projesini
  birden fazla markaya birebir taşımak gerekiyorsa, vendor-kilitli InoProShop dağıtımı yerine
  jenerik CODESYS + ilgili device paketleri düşünülmelidir (taşıma için bkz. belge 03).

## Gerçek Proje Notları

- CODESYS deneyimli ekiplerde proje yapısı sürtünmesiz benimsenir; en büyük iki sürtünme
  noktası **ESI/device repository sürüm yönetimi** ve **InoProShop ↔ firmware sürüm uyumudur**
  — tıpkı CODESYS'teki device description sürüm tuzağı gibi.
- EtherCAT görevini (motion) ayrı, yüksek öncelikli ve bus cycle ile senkron bir task'a koymak;
  makine mantığını ayrı bir cyclic task'a almak yaygın ve sağlam bir desendir.
- **Dosya uzantısı bu belgede bilinçli olarak doğrulanmamış bırakılmıştır.** Olgunluk seviyesi
  "Orta"dır; uzantı ve sürüme özgü menü farkları kurulu InoProShop'tan veya resmi Inovance
  dokümanından teyit edilmelidir.

## İlgili Konular

- `01_inoproshop_overview.md` — InoProShop genel bakış (InoProShop = CODESYS V3 türevi)
- `03_iec61131_in_inoproshop.md` — IEC 61131-3 dilleri ve CODESYS'ten kod taşıma
- `knowledge/codesys/fundamentals/02_project_structure.md` — taban CODESYS proje yapısı
  (Device tree, Application, Task, GVL, DUT, Library Manager, GUID/merge tuzakları)
- `knowledge/codesys/fundamentals/01_runtime_architecture.md` — bu yapıyı çalıştıran runtime
