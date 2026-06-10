---
KONU        : EtherNet/IP — Gerçek-Zaman Fieldbus (CIP, Implicit/Explicit Messaging, EDS)
KATEGORİ    : networking
ALT_KATEGORI: fieldbus
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.odva.org/technology-standards/key-technologies/ethernet-ip/"
    başlık: "ODVA — EtherNet/IP & Common Industrial Protocol (CIP)"
    güvenilirlik: resmi
  - url: "https://www.odva.org/wp-content/uploads/2020/05/PUB00213R0_EtherNetIP_Developers_Guide.pdf"
    başlık: "ODVA — EtherNet/IP Quick Start for Vendors Handbook (PUB00213)"
    güvenilirlik: resmi
  - url: "https://softwaretoolbox.com/resources/what-is-ethernetip"
    başlık: "Software Toolbox — What is EtherNet/IP (CIP, Explicit/Implicit)"
    güvenilirlik: topluluk
  - url: "https://www.motioncontroltips.com/what-are-explicit-and-implicit-messaging-in-ethernet-ip/"
    başlık: "Motion Control Tips — Explicit and Implicit Messaging in EtherNet/IP"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "_synthesis.md"
    ilişki: detaylandırır
  - konu: "01_ethercat.md"
    ilişki: alternatif
  - konu: "02_profinet.md"
    ilişki: alternatif
  - konu: "04_canopen.md"
    ilişki: tamamlar
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: alternatif
ÖNKOŞUL     :
  - "TCP/IP ve UDP temelleri (port, multicast)"
  - "Nesne yönelimli model kavramı (class/instance/attribute)"
  - "Fieldbus üst sentezi (_synthesis.md) okunmuş olmalı"
ÇELİŞKİLER :
  - kaynak: "EtherNet/IP'deki 'IP' internet protokolü mü?"
    konu: "EtherNet/IP'deki IP 'Industrial Protocol' anlamına gelir, Internet Protocol değil"
    çözüm: >
      EtherNet/IP = Ethernet Industrial Protocol. CIP'i (Common Industrial Protocol) standart
      Ethernet+TCP/UDP üzerinde taşır. Karışıklık yaygındır; ODVA terminolojisinde IP = Industrial Protocol.
  - kaynak: "EtherNet/IP gerçek-zaman mı? Standart Ethernet üzerinde nasıl?"
    konu: "EtherNet/IP determinizmi switch/ağ tasarımına ve CIP Sync'e bağlıdır"
    çözüm: >
      Implicit (I/O) mesajlaşma UDP üzerinde producer/consumer ile cyclic çalışır (RPI).
      Sıkı senkron motion için CIP Motion + CIP Sync (IEEE 1588 PTP) gerekir. Standart Ethernet
      üzerinde çalışır ama EtherCAT/PROFINET-IRT düzeyinde donanımsal determinizm için yönetilen
      switch ve PTP altyapısı gerekir.
---

## Özün Ne

EtherNet/IP (Ethernet Industrial Protocol), ODVA (Open DeviceNet Vendor Association) tarafından yönetilen, IEC 61158/61784 standartlarına dahil Ethernet-tabanlı gerçek-zaman fieldbus'tır. Rockwell Automation / Allen-Bradley ekosisteminin (ControlLogix, CompactLogix, Studio 5000, Kinetix) ağırlıklı protokolüdür. Temeli **CIP (Common Industrial Protocol)** adlı nesne-yönelimli uygulama katmanıdır: her cihaz, sınıf/örnek/özellik (class/instance/attribute) hiyerarşisinde CIP nesneleri olarak modellenir.

EtherNet/IP'nin ayırt edici özelliği, aynı CIP nesne modelini DeviceNet (CAN), ControlNet ve CompoNet ile paylaşmasıdır — yani bir cihazın modeli ağ türünden bağımsızdır ve bridge'lerle ağlar arası yönlendirilebilir. EtherNet/IP de OPC UA/Modbus raporlama katmanının **altında**, gerçek-zaman kontrol katmanında yer alır.

## Nasıl Çalışır

### CIP — Common Industrial Protocol (Nesne Modeli)

CIP, cihazı nesne-yönelimli modeller. Üç katman:

```
CLASS (Sınıf)        → Ortak özellikli nesne kategorisi (ID ile)
   örn: Identity (0x01), Assembly (0x04), Connection Manager (0x06)
   │
   ├─ INSTANCE (Örnek) → Sınıfın belirli bir örneği
   │     │
   │     └─ ATTRIBUTE (Özellik) → Tek veri öğesi
   │           erişim: Get_Attribute_Single (0x0E), Set_Attribute_Single (0x10) ...
   │
SERVICE (Servis)     → Nesneye uygulanan işlem (servis kodu ile)
```

Zorunlu nesneler:
- **Identity Object (0x01):** Üretici, ürün kodu, seri no, durum — cihaz kimliği.
- **Assembly Object (0x04):** I/O verisini gruplar; implicit bağlantının arayüzü.
- **Connection Manager (0x06):** Bağlantı kurulumu (Forward_Open / Forward_Close).

### Implicit vs Explicit Messaging

EtherNet/IP'nin iki temel iletişim biçimi vardır:

```
┌──────────────────────────────────────────────────────────────────┐
│ IMPLICIT (I/O) MESSAGING — gerçek-zaman                           │
│   Taşıma: UDP, port 2222                                          │
│   Model : Producer/Consumer (bir üretici → çok tüketici, multicast)│
│   Kurulum: Forward_Open ile bağlantı açılır                       │
│   İçerik: Assembly instance verisi (önceden tanımlı yapı)         │
│   Periyot: RPI (Requested Packet Interval), tipik 1-500ms         │
│   Kullanım: cyclic I/O, sürücü kontrolü, gerçek-zaman process data │
├──────────────────────────────────────────────────────────────────┤
│ EXPLICIT MESSAGING — istek/yanıt, gerçek-zaman değil               │
│   Taşıma: TCP, port 44818                                         │
│   Model : Request/Response (her mesaj adres+servis taşır)         │
│   İçerik: herhangi bir CIP nesnesi/özelliği (esnek)               │
│   Kullanım: konfigürasyon, parametre, diagnostik, SCADA polling   │
└──────────────────────────────────────────────────────────────────┘
```

Kritik fark: **implicit** verimlilik için "ne taşıdığını önceden bilir" (assembly yapısı sabit, her pakette adres yok) — gerçek-zaman içindir. **Explicit** her mesajda neyi istediğini açıkça söyler (esnek ama daha ağır) — konfig/diagnostik içindir. SCADA ve OPC sunucuları genelde explicit kullanır.

### Producer/Consumer Modeli

Geleneksel master/slave'in aksine, implicit mesajlaşma **producer/consumer** modelini kullanır: bir üretici (örn. bir I/O modülü) veriyi bir kez UDP multicast olarak yayınlar; birden çok tüketici (PLC, başka cihaz) aynı veriyi alabilir. Bu, aynı verinin birden çok cihaza verimli dağıtımını sağlar.

### Assembly Instances (Input / Output)

Assembly nesnesi (0x04), implicit bağlantıda taşınan veriyi yapılandırır. İki tür örnek:
- **Input assembly:** Cihazdan controller'a giden veri (cihazın "ürettiği").
- **Output assembly:** Controller'dan cihaza gelen veri (cihazın "tükettiği").
- **Configuration assembly:** Bağlantı kurulurken gönderilen konfig verisi.

Forward_Open sırasında bu assembly instance numaraları ve boyutları belirtilir; EDS dosyası hangi instance'ların kullanılacağını tanımlar.

### EDS Dosyaları

**EDS (Electronic Data Sheet)**, metin (INI benzeri) formatında cihaz tanım dosyasıdır. Cihazın CIP yeteneklerini tanımlar: desteklenen nesneler, assembly instance'ları ve boyutları, parametreler, bağlantı seçenekleri. Mühendislik aracı (Studio 5000, CODESYS) cihazı bu dosyayla tanır. CIP uygunluk sertifikasyonunda EDS dosyası ODVA tarafından doğrulanır/onaylanır.

### Adresleme ve CIP Sync

- **IP adresi:** EtherNet/IP cihazları standart IP kullanır (BOOTP/DHCP ya da statik). PROFINET'in device-name kimliğinin aksine, burada kimlik IP tabanlıdır.
- **CIP Sync:** IEEE 1588 PTP (Precision Time Protocol) tabanlı zaman senkronizasyonu. Sıkı senkron uygulamalar (CIP Motion) için kullanılır.
- **CIP Motion:** Senkron eksen kontrolü profili; CIP Sync üzerine kurulur.
- **CIP Safety:** Fonksiyonel güvenlik profili (STO vb.) — fieldbus üzeri güvenli telegramlar.

### CIP Ailesi (Ağdan Bağımsız Model)

```
                    CIP (ortak nesne modeli)
        ┌──────────────┬──────────────┬──────────────┐
   EtherNet/IP      DeviceNet      ControlNet     CompoNet
   (Ethernet)       (CAN)          (koaks/fiber)  (seri)
   TCP/UDP          deterministik   deterministik  bit-strobe
```
Aynı cihaz nesne modeli tüm bu ağlarda geçerlidir; bridge node'larla ağlar arası CIP yönlendirmesi yapılabilir. Bu, DeviceNet'ten EtherNet/IP'ye geçişi kolaylaştırır.

## Pratikte Nasıl Kullanılır (CODESYS / Studio 5000)

CODESYS'te EtherNet/IP Scanner (master) ve Adapter (slave) eklentileriyle gelir. Tipik akış:

```
1. EDS kur: Device Repository → cihaz üreticisinin EDS dosyasını içe aktar.
2. Scanner ekle: Ethernet adaptörüne "EtherNet/IP Scanner" ekle.
3. Adapter ekle: scanner altına cihazı ekle (EDS'den), IP adresini ata.
4. Bağlantı (connection) tanımla: input/output assembly instance'larını seç,
   boyutlarını ve RPI'yi (örn. 10ms) ayarla.
5. I/O mapping: assembly verisini GVL değişkenlerine bağla.
6. (Senkron motion gerekiyorsa) CIP Sync / CIP Motion yapılandır.
7. Bus cycle task: scanner'ı uygun çevrim süreli task'a bağla.
```

Studio 5000 (Rockwell) tarafında: EDS import → Ethernet ağacına cihaz ekle → assembly/RPI tanımı → tag'ler otomatik üretilir.

## Örnekler

### Örnek 1 — Implicit ve Explicit Birlikte
```
PowerFlex VFD (EtherNet/IP):
  IMPLICIT (UDP 2222, RPI=20ms):
    Output assembly → controller yazar: hız setpoint, start/stop komut
    Input assembly  → controller okur: gerçek hız, akım, durum
  EXPLICIT (TCP 44818, gerektikçe):
    Set_Attribute → akselerasyon rampası parametresi (nadiren değişir)
    Get_Attribute → arıza geçmişi okuma (diagnostik)

Cyclic kontrol implicit ile; bir kerelik parametre/diagnostik explicit ile. Ayrı tutulur.
```

### Örnek 2 — RPI Seçimi
```
Senaryo: 30 I/O cihazı tek scanner'a bağlı.
Sorun  : Hepsine RPI=2ms verilince ağ/CPU doyar, paket kaybı.
Çözüm  : Kritik sürücülere RPI=10ms, yavaş sensörlere RPI=100ms.
Ders   : RPI cihaz başına ayarlanır; hepsine en hızlıyı vermek ağı boğar.
         RPI ihtiyaca göre kademelenmeli (bant bütçesi).
```

## Sık Yapılan Hatalar

### Hata 1: Implicit ve Explicit'i Karıştırmak
Cyclic kontrol verisini explicit (TCP polling) ile çekmeye çalışmak gerçek-zaman performansını öldürür; gereksiz overhead ve gecikme. Cyclic I/O daima implicit (UDP, assembly, RPI); konfig/diagnostik explicit.

### Hata 2: Tüm Cihazlara Aynı (Düşük) RPI Vermek
RPI cihaz başına ayarlanır. Hepsine en kısa RPI'yi vermek ağı ve scanner CPU'sunu boğar, paket kaybına yol açar. RPI ihtiyaca göre kademelenmeli.

### Hata 3: Yanlış Assembly Instance / Boyut
Forward_Open'da yanlış input/output assembly instance numarası ya da boyutu → bağlantı reddedilir (connection error) ya da veri kayar. EDS'deki doğru instance/boyutu kullan.

### Hata 4: Yanlış EDS Sürümü
Firmware ile uyumsuz EDS → assembly tanımı tutmaz, cihaz yapılandırılamaz. Firmware ile eşleşen EDS'yi kullan; ODVA onaylı sürüm tercih edilir.

### Hata 5: Çok Fazla Multicast'i Yönetmemek
Producer/consumer multicast kullanır; büyük ağlarda IGMP snooping'siz switch'lerde multicast tüm portlara taşar ve ağı boğar. Yönetilen switch'lerde IGMP snooping etkinleştirilmeli.

## Ne Zaman Tercih Edilmeli / Edilmemeli

```
✓ Rockwell/Allen-Bradley ControlLogix/CompactLogix/Studio 5000 ekosistemi
✓ Mevcut DeviceNet/ControlNet'ten CIP modeli taşınması (aynı nesne modeli)
✓ Standart Ethernet altyapısı yeterli, producer/consumer çoklu tüketici
✓ CIP Safety ile fonksiyonel güvenlik, CIP Motion ile senkron eksen
✓ Kuzey Amerika ağırlıklı tesis/cihaz mevcudiyeti

✗ Tesis Siemens (PROFINET) ya da Beckhoff/CODESYS (EtherCAT) ağırlıklı ise
✗ En yüksek motion verimi/en düşük gecikme birincil (EtherCAT processing-on-the-fly üstün)
✗ Düşük maliyet mobil/gömülü tek sürücü (CANopen)
✗ PLC → SCADA/MES raporlaması (OPC UA; EtherNet/IP kontrol katmanı)
```

## Gerçek Proje Notları

**Not 1 — Implicit/explicit ayrımı EtherNet/IP'nin kalbidir.** Yeni mühendisler her şeyi explicit (kolay, esnek) ile yapmaya çalışır ve gerçek-zaman performansını kaybeder. Kural net: tekrarlayan cyclic veri implicit (assembly + RPI), bir kerelik/nadir işlem explicit. Bu ayrım yapılmazsa "EtherNet/IP yavaş" yanlış sonucuna varılır.

**Not 2 — RPI bant bütçesidir, "ne kadar hızlı olursa o kadar iyi" değil.** Her implicit bağlantı RPI'sinde ağda paket üretir. 50 cihaza 2ms RPI = saniyede 25.000 paket; scanner ve switch doyar. RPI cihazın gerçek ihtiyacına göre seçilir; çoğu sensör 50-100ms ile gayet iyidir.

**Not 3 — Multicast ve IGMP snooping unutulursa ağ boğulur.** Producer/consumer multicast kullanır; IGMP snooping'siz switch multicast'i tüm portlara yayar. Orta-büyük ağlarda yönetilen switch + IGMP snooping zorunlu; aksi halde "rastgele" paket kaybı ve bağlantı düşmeleri görülür.

**Not 4 — CIP modeli ağdan bağımsız; DeviceNet bilgisi taşınır.** Eski DeviceNet projesinden gelen mühendis, EtherNet/IP'de aynı CIP nesnelerini (Identity, Assembly) bulur. Geçiş, fiziksel katman değişimidir; uygulama modeli aynı kalır. Bu ODVA'nın stratejik avantajıdır.

**Not 5 — Senkron motion için CIP Sync/PTP altyapısı ayrı kurulur.** Standart implicit I/O senkron motion için yeterli determinizmi vermez; CIP Motion + CIP Sync (IEEE 1588 PTP) ve PTP-yetenekli switch gerekir. "EtherNet/IP ile motion yaparım" deyip PTP'yi atlamak titreyen eksenle sonuçlanır.

## İlgili Konular

```
knowledge/networking/fieldbus/
├── _synthesis.md     → Dört fieldbus karşılaştırması, raporlama≠kontrol
├── 01_ethercat.md    → Alternatif Ethernet fieldbus (Beckhoff/CODESYS)
├── 02_profinet.md    → Alternatif Ethernet fieldbus (Siemens)
└── 04_canopen.md     → CAN-tabanlı CIP akrabası DeviceNet ile karşılaştır

Üst katman (raporlama):
knowledge/protocols/opc-ua/01_architecture.md → PLC↔SCADA (EtherNet/IP'nin üstü)

Standartlar: IEC 61158 / IEC 61784 (ODVA yönetir), CIP spesifikasyonları (ODVA Vol.1-2)
CIP ailesi: DeviceNet, ControlNet, CompoNet (aynı nesne modeli)
Araçlar: Studio 5000, CODESYS EtherNet/IP eklentisi, Wireshark (enip, cip dissector)
```
