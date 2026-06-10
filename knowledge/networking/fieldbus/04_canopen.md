---
KONU        : CANopen — CAN-Tabanlı Fieldbus (CiA 301, NMT, PDO/SDO, Object Dictionary, CiA 402)
KATEGORİ    : networking
ALT_KATEGORI: fieldbus
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.can-cia.org/can-knowledge/canopen"
    başlık: "CAN in Automation (CiA) — CANopen"
    güvenilirlik: resmi
  - url: "https://www.can-cia.org/can-knowledge/canopen-profiles"
    başlık: "CAN in Automation (CiA) — CANopen Profiles (CiA 301, 402)"
    güvenilirlik: resmi
  - url: "https://www.kebamerica.com/blog/comprehensive-guide-to-the-cia-402-drive-profile/"
    başlık: "KEB — Comprehensive Guide to the CiA 402 Drive Profile"
    güvenilirlik: topluluk
  - url: "https://en.wikipedia.org/wiki/CANopen"
    başlık: "CANopen — Wikipedia"
    güvenilirlik: topluluk
  - url: "https://media.hms-networks.com/image/upload/v1701953901/Documents/Whitepapers/Ixxat_CANopen-Protocol-Whitepaper_EN.pdf"
    başlık: "HMS / Ixxat — Basics of CANopen and CANopen FD (Whitepaper)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "_synthesis.md"
    ilişki: detaylandırır
  - konu: "01_ethercat.md"
    ilişki: tamamlar
  - konu: "knowledge/inovance/inoproshop/06_motion_control.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: alternatif
ÖNKOŞUL     :
  - "CAN bus temelleri: arbitration, CAN ID, mesaj öncelik (düşük ID = yüksek öncelik)"
  - "Object dictionary / index-subindex kavramı"
  - "Fieldbus üst sentezi (_synthesis.md) okunmuş olmalı"
ÇELİŞKİLER :
  - kaynak: "CANopen 'yavaş/eski' algısı"
    konu: "CANopen ≤1 Mbit/s ile sınırlıdır ama hâlâ yaygındır"
    çözüm: >
      Klasik CAN ≤1 Mbit/s'tir; Ethernet-tabanlılara kıyasla düşük bant. Ancak düşük maliyet,
      kablo gürbüzlüğü, CiA 402 olgunluğu sayesinde mobil makine, sürücü, batarya, gömülü sistemde
      standarttır. CANopen FD (CAN FD üzerinde) bant genişliğini önemli ölçüde artırır.
  - kaynak: "CANopen mı EtherCAT mı (CoE)?"
    konu: "EtherCAT CoE, CANopen'ın Object Dictionary ve CiA 402 modelini kullanır"
    çözüm: >
      EtherCAT'in CoE (CANopen over EtherCAT) mailbox protokolü, CANopen'ın OD yapısını ve CiA 402
      sürücü profilini EtherCAT fiziksel katmanı üzerinde taşır. CANopen bilgisi EtherCAT motion'a
      doğrudan aktarılır; ikisi rakip değil, biri diğerinin uygulama modelini kullanır.
---

## Özün Ne

CANopen, CAN in Automation (CiA) tarafından yönetilen, CAN (Controller Area Network) veri yolu üzerine kurulu bir fieldbus standardıdır. Temel spesifikasyon **CiA 301**'dir ve uygulama katmanını, Object Dictionary'yi (nesne sözlüğü) ve tüm iletişim servislerini (NMT, SDO, PDO, SYNC, EMCY) tanımlar. CiA 402 sürücü profili IEC 61800-7-201/301 olarak da standartlaşmıştır.

CANopen'ın gücü düşük maliyet, kablo gürbüzlüğü ve olgun cihaz profilleridir. Klasik CAN ≤1 Mbit/s bant genişliğiyle sınırlıdır; bu nedenle Ethernet-tabanlı fieldbus'larla rakip değil, farklı bir maliyet/karmaşıklık noktasıdır: mobil makineler, tarım/inşaat araçları, batarya yönetimi, gömülü sistemler ve tek/birkaç servo sürücü senaryolarında baskındır. CANopen da OPC UA/Modbus raporlama katmanının **altında**, gerçek-zaman kontrol katmanında yer alır.

## Nasıl Çalışır

### Object Dictionary (Nesne Sözlüğü)

CANopen'ın kalbidir. Her cihazın tüm yapılandırılabilir/okunabilir verileri, 16-bit **index** ve 8-bit **subindex** ile adreslenen bir tabloda tutulur:

```
Index (16-bit) : Subindex (8-bit) → Değer
─────────────────────────────────────────────────────────
0x1000 : 00  → Device Type
0x1018 : 01  → Vendor ID (Identity)
0x6040 : 00  → Controlword (CiA 402 sürücü)
0x6041 : 00  → Statusword (CiA 402 sürücü)
0x6060 : 00  → Modes of Operation
0x607A : 00  → Target Position
...
Standart aralıklar:
  0x1000-0x1FFF → Communication profile (CiA 301)
  0x2000-0x5FFF → Manufacturer specific
  0x6000-0x9FFF → Device profile (örn. CiA 402 sürücü)
```

OD, cihazın "tüm bilgi modeli"dir; SDO ile tek tek erişilir, PDO ile gerçek-zaman eşlenir.

### NMT — Network Management (Durum Makinesi)

Bir node'un çalışma durumu NMT ile yönetilir. NMT master, node'lara durum geçiş komutları gönderir:

```
        ┌─────────────────┐
        │ Initialisation  │ Güç açılışı / reset → otomatik
        └────────┬────────┘
                 ▼ (otomatik)
        ┌─────────────────┐  SDO: ✓   PDO: ✗   Heartbeat: ✓
        │ Pre-Operational │  Yapılandırma durumu (OD'ye SDO ile yaz)
        └────────┬────────┘
                 ▼ NMT "Start Remote Node" (0x01)
        ┌─────────────────┐  SDO: ✓   PDO: ✓   (tam çalışma)
        │  Operational    │  PDO'lar akar; gerçek-zaman process data
        └────────┬────────┘
                 ▼ NMT "Stop" → Stopped (yalnız NMT/heartbeat)
        ┌─────────────────┐
        │    Stopped      │
        └─────────────────┘
```

Devreye almada en sık tuzak: node **Pre-Operational'da kalır**, NMT Start gönderilmediği için PDO akmaz — "veri gelmiyor" sanılır. Çözüm NMT Start komutudur (ya da master'ın otomatik start ayarı).

### PDO — Process Data Objects (Gerçek-Zaman)

PDO, gerçek-zaman process data taşıyan CANopen mesajıdır. Tek CAN frame'inde (≤8 byte) OD'den eşlenmiş değerleri taşır, adres/protokol overhead'i yoktur — bu yüzden hızlıdır:

- **TPDO (Transmit PDO):** Node'un gönderdiği veri (input).
- **RPDO (Receive PDO):** Node'un aldığı veri (output).
- **PDO mapping:** Hangi OD nesnelerinin PDO'ya konacağı OD'de yapılandırılır (örn. statusword + actual position bir TPDO'ya).
- **Transmission type:** PDO ne zaman gönderilir?
  - Event-driven (değişimde)
  - Cyclic synchronous (her SYNC mesajında)
  - Remote request

### SDO — Service Data Objects (Konfig/Acyclic)

SDO, OD'ye tek tek erişim sağlar (read/write). PDO'nun aksine teyitli (confirmed) ve adresli çalışır; her erişimde index+subindex belirtilir. Büyük veri için segmented/block transfer destekler. Kullanım: parametre yazma, konfigürasyon, nadir okuma. PDO sürekli akar, SDO tek seferlik işlemdir.

### SYNC, EMCY, Heartbeat

| Obje | İşlev |
|---|---|
| **SYNC** | Master'ın yayınladığı senkronizasyon mesajı; synchronous PDO'lar bununla tetiklenir (eşzamanlı örnekleme/aktüasyon). |
| **EMCY (Emergency)** | Node hata oluştuğunda yayınladığı acil durum mesajı; hata kodu taşır (teşhiste altın değerinde). |
| **Heartbeat** | Node periyodik "yaşıyorum + durumum" mesajı; node-guarding'in modern halefi, bağlantı izleme. |

### COB-ID ve Öncelik

CANopen mesajları CAN ID (COB-ID) ile adreslenir; CAN arbitration gereği **düşük ID = yüksek öncelik**. Varsayılan COB-ID'ler Node-ID'den türetilir (predefined connection set):
```
NMT          : 0x000 (en yüksek öncelik)
SYNC         : 0x080
EMCY         : 0x080 + Node-ID
TPDO1        : 0x180 + Node-ID
RPDO1        : 0x200 + Node-ID
SDO (tx/rx)  : 0x580 / 0x600 + Node-ID
Heartbeat    : 0x700 + Node-ID
```
Node-ID 1-127 aralığındadır; her node benzersiz olmalı (çakışma = bus hatası).

### CiA 402 — Sürücü ve Motion Control Profili

CiA 402 (IEC 61800-7-201/301), servo/inverter sürücüler için standart profildir. Bir **durum makinesi** ve **operation mode**'lar tanımlar:

```
Anahtar OD nesneleri:
  0x6040 Controlword   → sürücüyü sür (Enable, Switch On, Fault Reset bitleri)
  0x6041 Statusword    → sürücü durumu (Ready, Operation Enabled, Fault bitleri)
  0x6060 Modes of Op.  → mod seçimi
  0x6061 Modes Display → aktif mod

Operation modes:
  pp  Profile Position      → noktadan noktaya konum
  pv  Profile Velocity      → hız kontrolü
  tq  Torque                → tork kontrolü
  hm  Homing                → referans arama
  ip  Interpolated Position → senkron interpolasyon (SYNC ile)
  csp/csv/cst → cyclic synchronous position/velocity/torque (motion senkron)

Durum makinesi: Not Ready → Switch On Disabled → Ready to Switch On
                → Switched On → Operation Enabled (controlword ile ilerletilir)
```

CiA 402'nin değeri standartlık: farklı üreticilerin sürücüleri aynı controlword/statusword/mode mantığıyla yönetilir. **Bu profil EtherCAT CoE üzerinden de kullanılır** — yani CANopen sürücü bilgisi EtherCAT motion'a doğrudan aktarılır.

### EDS Dosyaları

**EDS (Electronic Data Sheet)**, CiA 306'da tanımlı metin formatında cihaz tanım dosyasıdır; cihazın iletişim davranışını ve Object Dictionary girişlerini tanımlar. Mühendislik aracı (CODESYS CANopen manager) cihazı bu dosyayla tanır; cihaza özel bir örnek (DCF, Device Configuration File) konfig sonrası üretilir.

## Pratikte Nasıl Kullanılır (CODESYS)

CODESYS CANopen master/slave manager'ı **yerleşiktir**. Tipik akış:

```
1. EDS kur: Device Repository → cihaz üreticisinin EDS dosyasını içe aktar.
2. CAN bus ekle: PLC'nin CAN portuna "CANbus" cihazı ekle, baud rate ayarla
   (tüm node'larda AYNI olmalı: 125k/250k/500k/1M).
3. CANopen Manager ekle: master rolü.
4. Node ekle: manager altına cihazları ekle (EDS'den), her birine benzersiz Node-ID (1-127).
5. PDO mapping: her node'un PDO'larını OD'den eşle (örn. RPDO=controlword+target,
   TPDO=statusword+actual position), transmission type seç (cyclic synchronous önerilir motion'da).
6. SYNC: senkron motion için SYNC üretimini etkinleştir, periyodu çevrim süresiyle eşle.
7. I/O mapping: PDO verilerini GVL değişkenlerine bağla.
8. Bus cycle task: manager'ı uygun çevrim süreli task'a bağla.
9. Sürücü için: SoftMotion CiA 402 ekseni ekle, MC_Power/MC_MoveAbsolute ile kontrol et.
```

## Örnekler

### Örnek 1 — CiA 402 Sürücü Etkinleştirme (Controlword Dizisi)
```
Sürücüyü "Operation Enabled"a getirme (Profile Position modu):
  1. 0x6060 = 1 (pp mode) yaz (SDO ya da konfig)
  2. 0x6040 = 0x0006 (Shutdown)        → Ready to Switch On
  3. 0x6040 = 0x0007 (Switch On)        → Switched On
  4. 0x6040 = 0x000F (Enable Operation) → Operation Enabled
  5. 0x607A = hedef pozisyon, 0x6040 bit4=1 (new setpoint) → hareket
  0x6041 statusword her adımda durumu teyit eder.

CODESYS SoftMotion bu diziyi MC_Power FB'si arkasında otomatik yürütür.
```

### Örnek 2 — "PDO Akmıyor" Teşhisi
```
Belirti : Node bağlı, SDO ile OD okunuyor ama TPDO/RPDO akmıyor.
Adım 1  : Node hangi NMT durumunda? → Pre-Operational'da.
Çözüm   : NMT Start (0x01) gönderildi mi? Manager otomatik-start kapalıysa el ile gönder.
          Operational'a geçince PDO'lar aktı.
Ders    : SDO Pre-Op'ta çalışır ama PDO yalnız Operational'da akar. PDO yoksa önce NMT durumuna bak.
```

## Sık Yapılan Hatalar

### Hata 1: Node'u Operational'a Getirmemek (PDO Akmaması)
SDO Pre-Operational'da çalışır, PDO yalnız Operational'da akar. NMT Start gönderilmezse "veri gelmiyor" sanılır. PDO yoksa ilk bakılacak şey NMT durumudur.

### Hata 2: Baud Rate / Node-ID Uyuşmazlığı
Tüm node'lar aynı baud rate'te olmalı; bir node farklıysa tüm bus bozulur (bus-off). İki node aynı Node-ID'yi alırsa COB-ID çakışır. Devreye almada her node'un baud ve benzersiz ID'si doğrulanmalı.

### Hata 3: Bus Yükünü (Bant Bütçesini) Hesaplamamak
Klasik CAN ≤1 Mbit/s'tir. Node × PDO × frekans kapasiteyi aşarsa PDO'lar gecikir, "rastgele" eksen titremesi/iletişim hatası görülür. Tasarımda bus yükü hesaplanmalı; aşılıyorsa SYNC periyodu büyütülür, PDO azaltılır ya da CANopen FD/Ethernet'e geçilir.

### Hata 4: Termination (Sonlandırma) Direnci Eksikliği
CAN bus iki ucunda 120Ω sonlandırma direnci gerektirir. Eksik/yanlış termination → yansımalar → rastgele hata, bus-off. Fiziksel kurulum kontrol edilmeli (toplam ~60Ω ölçülmeli).

### Hata 5: Senkron Motion'da SYNC'siz PDO Kullanmak
Çok eksenli senkron hareket için PDO'lar cyclic synchronous (SYNC ile tetiklenen) olmalı ve interpolated/cyclic synchronous mode kullanılmalı. Event-driven PDO ile eksenler senkron örneklenmez; titreme görülür.

### Hata 6: Yanlış EDS Sürümü
Firmware ile uyumsuz EDS → OD yapısı tutmaz, PDO mapping yanlış. Firmware ile eşleşen EDS kullan.

## Ne Zaman Tercih Edilmeli / Edilmemeli

```
✓ Düşük maliyet, gürbüz kablo gereken ortam (mobil makine, araç, batarya)
✓ Tek/birkaç servo sürücü, orta hız (1-10ms) yeterli
✓ Gömülü/embedded sistem, sınırlı kaynak
✓ CiA 402 olgun sürücü profili gerekiyorsa (standart sürücü kontrolü)
✓ CAN altyapısı zaten mevcut (otomotiv/off-highway kökenli sistemler)

✗ Yüksek bant genişliği gerekiyorsa (≤1 Mbit/s sınırı) → Ethernet-tabanlı veya CANopen FD
✗ Çok cihaz + mikrosaniye senkron motion (EtherCAT/PROFINET-IRT üstün)
✗ Çok sayıda hızlı I/O (Ethernet-tabanlı tek frame verimi yok)
✗ PLC → SCADA/MES raporlaması (OPC UA; CANopen kontrol katmanı)
```

## Gerçek Proje Notları

**Not 1 — "PDO akmıyor" = NMT Operational değil (neredeyse her zaman).** Saha refleksi kabloyu/EDS'yi suçlamaktır; oysa SDO çalışıyorsa fiziksel katman sağlamdır. PDO yoksa node Pre-Operational'da kalmıştır. NMT Start (ya da manager'da otomatik-start) ilk kontroldür.

**Not 2 — Bus yükü tasarımda hesaplanmazsa sahada doyar.** ≤1 Mbit/s acımasız bir sınırdır. 20 node'a 1ms'de büyük PDO yüklemek bus'ı doyurur; sonuç "rastgele" gibi görünen ama aslında bant doygunluğundan kaynaklanan eksen titremesi ve EMCY mesajlarıdır. SYNC periyodu, PDO sayısı ve boyutu baştan bütçelenmeli.

**Not 3 — Termination ve kablo CANopen'ın gizli zorluğudur.** Ethernet'in aksine CAN fiziksel katmanı hassastır: iki uçta 120Ω, doğru topoloji (yıldız değil hat), stub uzunluğu sınırı. Devreye almada "rastgele" hatalar genelde fiziksel: eksik termination, uzun stub, kötü topraklama. Multimetre ile ~60Ω ölçmek ilk teşhistir.

**Not 4 — CiA 402 EtherCAT'e köprüdür.** CANopen'da öğrenilen controlword/statusword/modes-of-operation mantığı EtherCAT CoE'de birebir aynıdır. Bir mühendis CANopen sürücü kontrolünü öğrendiyse, EtherCAT motion'a geçişi kolaydır; aynı OD nesnelerini farklı fiziksel katmanda kullanır.

**Not 5 — CANopen FD bant sıkışıklığını çözer.** Klasik CAN'in ≤1 Mbit/s ve 8-byte payload sınırı dar geldiğinde, CANopen FD (CAN FD üzerinde, 64-byte payload + daha yüksek veri hızı) seçenektir. Mevcut CANopen bilgisi korunur; fiziksel katman ve frame genişler. Yeni tasarımlarda bant ihtiyacı sınırdaysa değerlendirilmeli.

## İlgili Konular

```
knowledge/networking/fieldbus/
├── _synthesis.md     → Dört fieldbus karşılaştırması, raporlama≠kontrol
├── 01_ethercat.md    → CoE ile CiA 402'yi EtherCAT üzerinde kullanır (aynı OD)
├── 02_profinet.md    → Ethernet-tabanlı alternatif
└── 03_ethernet_ip.md → CIP ailesi DeviceNet (CAN) ile akraba

knowledge/inovance/inoproshop/
└── 06_motion_control.md → SoftMotion CiA 402 ekseni (CANopen/EtherCAT ortak profil)

Üst katman (raporlama):
knowledge/protocols/opc-ua/01_architecture.md → PLC↔SCADA (CANopen'ın üstü)

Standartlar: CiA 301 (communication), CiA 402 = IEC 61800-7-201/301 (drive),
             CiA 306 (EDS), CANopen FD
Araçlar: PCAN-View, Kvaser, CODESYS CANopen Manager, Wireshark (canopen dissector)
```
