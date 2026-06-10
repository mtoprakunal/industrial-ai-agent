---
KONU        : InoProShop EtherCAT Konfigürasyonu (Master / Slave / ESI / GL20 / Servo)
KATEGORİ    : inovance
ALT_KATEGORI: inoproshop
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.manualslib.com/manual/2433383/Inovance-Ethercat-Md800.html?page=41"
    başlık: "Inovance EtherCAT MD800 — InoProShop EtherCAT master/slave kurulumu (AM/AC serisi)"
    güvenilirlik: topluluk
  - url: "https://idea-tech.in/wp-content/uploads/2023/12/INOVANCE-SV660N-Startup-Procedure-ENGLISH-28-12-23.pdf"
    başlık: "Inovance — SV660N Startup Procedure (EtherCAT/InoProShop devreye alma)"
    güvenilirlik: resmi
  - url: "https://www.ethercat.org/en/products/6B9B3C89DDDE44C2ACFBE609E8C72C3B.htm"
    başlık: "EtherCAT Technology Group — SV660N (CiA402 sertifika kaydı)"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/products/plcs-hmis/gl20-i/o-modules"
    başlık: "Inovance — GL20 I/O Modules (EtherCAT slave coupler)"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/fileadmin/downloads/Brochures/EN/AM600_Br_EN_Singles_Web_V2.2.pdf"
    başlık: "Inovance — AM600 (EtherCAT master, 32 eksen) broşürü"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "04_hardware_configuration.md"
    ilişki: gerektirir
  - konu: "01_inoproshop_overview.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/networking/_synthesis.md"
    ilişki: tamamlar
  - konu: "devices/INOVANCE_SV660N/datasheet.json"
    ilişki: kullanır
  - konu: "devices/INOVANCE_IS620N/datasheet.json"
    ilişki: kullanır
  - konu: "devices/INOVANCE_GL20/datasheet.json"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Donanım ağacı / Device Tree kurulmuş olmalı (04_hardware_configuration.md)"
  - "InoProShop = CODESYS V3 gerçeği (01_inoproshop_overview.md)"
  - "CiA 402 servo profili ve PLCopen Motion (MC_*) temel kavramı"
ÇELİŞKİLER :
  - kaynak: "Yaygın varsayım: 'EtherCAT raporlama ağı gibi esnektir; gerçek-zaman gerektirmez'"
    konu: "EtherCAT gerçek-zaman fieldbus'tır; OPC UA/Modbus/MQTT raporlama katmanından AYRIDIR"
    çözüm: >
      knowledge/codesys/networking/_synthesis.md'deki 'hiçbiri gerçek-zaman değil'
      ilkesi networking protokolleri (OPC UA/Modbus/TCP/MQTT) içindir. EtherCAT bunun
      tam tersi: senkron motion'ın gerçek-zaman katmanıdır (DC ile mikrosaniye senkron).
      İki dünyayı karıştırmayın — servo senkronu EtherCAT/DC işidir, MES raporlaması
      OPC UA işidir.
---

## Özün Ne

EtherCAT konfigürasyonu, InoProShop projesinde **gerçek-zaman fieldbus'ı** kurmaktır:
AM600/AC800 kontrolörü **EtherCAT master** olarak çalışır, hattaki GL20 I/O coupler'ları
ve SV660N/IS620N servo sürücüleri **slave** olarak ona bağlanır. Bu işlemin üç ayağı
vardır: (1) slave'i tanıtan **ESI** (EtherCAT Slave Information, XML) dosyası, (2)
master altına slave ekleyip **PDO eşlemesi** yapmak, (3) **senkronizasyon modunu**
(FreeRun / SM-Sync / DC-Sync) ve gerekirse **Distributed Clocks**'u doğru ayarlamak.

InoProShop CODESYS V3 türevi olduğu için bu yığın **CODESYS EtherCAT master**'ının
birebir aynısıdır: aynı EtherCAT Master objesi, aynı ESI import diyaloğu, aynı
SoftMotion CiA402 Axis. Inovance farkı, kendi cihazlarının (SV660N, IS620N, GL20)
ESI'lerinin havuzda hazır gelmesidir.

Neden önemli: Senkron çok-eksenli motion'ın (CAM, interpolasyon) "kalbi" EtherCAT
DC senkronudur. DC yanlışsa eksenler titrer, takip hatası alır; FreeRun'da bırakılan
bir servo CSP modunda asla istenen senkronu tutturamaz.

## Nasıl Çalışır

### EtherCAT Master + Slave + ESI üçlüsü

```
AM600 / AC800  =  EtherCAT MASTER
        │  (tek EtherCAT RJ45 hat; 100 Mbit/s tam dupleks, 100 m segment)
        ▼
 ┌─────────────┬──────────────┬──────────────┐
 │ GL20-RTU-ECT│  SV660N      │  IS620N      │   ← SLAVE'ler (hat/line topolojisi)
 │ (I/O coupler)│ (CiA402 servo)│ (CiA402 servo)│
 └─────────────┴──────────────┴──────────────┘
```

- **Master:** AM600 standart EtherCAT portuyla 32 eksene kadar (8 interpolasyon /
  16 CAM) sürer; EtherCAT üzerinden 125 slave istasyona kadar (datasheet). AC800 ise
  256 eksene kadar.
- **Slave:** Her slave kendini bir **ESI (XML)** ile tanıtır. ESI; PDO yapısını, SDO
  objelerini, DC yeteneklerini ve CoE (CANopen over EtherCAT) profilini tanımlar.
- **Process Data (PDO):** Her döngüde master, slave'lerin process data'sını okur/yazar.
  GL20 için bu I/O bit/word'leri; servo için CiA402 objeleri (Controlword 6040h,
  Statusword 6041h, Target position 607Ah ... — datasheet register_map).

### Senkronizasyon Modları

EtherCAT slave'inin process data'sını ne zaman uyguladığını belirler:

| Mod | Ne yapar | Tipik kullanım |
|---|---|---|
| **FreeRun** | Slave kendi iç saatiyle çalışır; master döngüsüyle senkron DEĞİL | Basit I/O, zaman-kritik olmayan |
| **SM-Sync (SM2/SM3 event)** | Slave, master'ın process data (SyncManager) olayında günceller | Orta hassasiyet I/O |
| **DC-Sync (Distributed Clocks)** | Tüm slave'ler ortak bir referans saate kilitlenir; eşzamanlı (jitter ~ns) | **Senkron motion (servo CSP/CSV/CST), CAM, interpolasyon** |

**Distributed Clocks (DC):** Hattaki ilk DC-yetenekli slave (genelde ilk servo) referans
saat olur; master ve diğer slave'ler buna senkronize edilir. SYNC0 (ve gerekirse SYNC1)
kesmeleri ile her slave process data'sını TAM aynı anda uygular. Çok-eksenli senkronun
fiziksel temeli budur.

### CiA 402 Servo Ekseni

SV660N / IS620N IEC 61800-7 (CiA 402) profilini EtherCAT CoE üzerinden uygular
(datasheet). InoProShop'ta servo slave eklendikten sonra üzerine bir **SoftMotion CiA402
Axis** objesi eklenir; PLCopen MC_* FB'leri (MC_Power, MC_MoveAbsolute, MC_MoveVelocity,
MC_Home...) bu eksen üzerinden çalışır. Desteklenen modlar (datasheet 6060h):
**CSP(8) / CSV(9) / CST(10) / PP(1) / PV(3) / PT(4) / HM(6)**. Senkron motion için
**CSP** (Cyclic Synchronous Position) + DC-Sync standarttır.

## Pratikte Nasıl Kullanılır

### 1. EtherCAT Master Ekle / Etkinleştir

- 04'teki Device Tree hazır olmalı. Network/donanım konfigürasyonunu aç, CPU'yu seç ve
  **EtherCAT Master** fonksiyonunu etkinleştir (AM600 master istasyonu). (Kaynak: MD800
  InoProShop kurulum adımları.)
- Master ayarlarında: kullanılacak ağ adaptörü (AM600 EtherCAT portu), **döngü süresi
  (cycle time)** — motion için tipik 1 ms ya da daha hızlı; GL20 minimum 125 µs destekler.

### 2. ESI Dosyasını İçe Aktar (slave tanımı)

- Inovance kendi cihazları (SV660N, IS620N, GL20) için ESI'leri havuzda sunar; eksikse
  resmi destek portalından ESI/XML indirilir (datasheet: download_url boş — portaldan
  temin edilmeli).
- **Tools → Device Repository → Install** ile ESI/XML'i yükle. Önemli kural (MD800
  kılavuzu): *"Başka sürümde bir konfigürasyon dosyası varsa, yenisini içe aktarmadan
  önce mevcut dosyayı SİL."* Aynı slave'in çakışan iki ESI sürümü en sinsi hatalardandır.

### 3. Slave Ekle (master altına)

- EtherCAT Master'a sağ tık → **Add Device** (veya cihaz listesinden ağaca sürükle) →
  ilgili slave'i seç (GL20-RTU-ECT / SV660N / IS620N).
- Fiziksel hat sırasıyla AYNI sırada ekle. Topoloji line (hat) olduğundan sıra önemlidir.

### 4. GL20 I/O Yapılandırması

- **GL20-RTU-ECT** coupler'ı slave olarak ekle. Arkasındaki modüller (GL20-1600END,
  GL20-0016ETN, GL20-4AD ...) coupler altında modül olarak görünür/eklenir.
- **PDO eşlemesi:** Her modülün giriş/çıkış process data'sı PDO'ya, oradan %I/%Q'ya
  düşer → I/O Mapping → GVL (bkz. 04).
- GL20 genelde **DC-Sync gerektirmez**; FreeRun ya da SM-Sync yeterlidir (saf I/O,
  motion senkronu yok). Yine de hat üzerinde servolarla DC referansı paylaşıyorsa
  master ayarına uyum gösterir.
- Not (datasheet): coupler arkası modüller EtherCAT **alias** erişimini desteklemez;
  alias master üzerinden yapılandırılır (1–65535).

### 5. SV660N / IS620N Servo Ekleme (CiA402)

1. Servo slave'i master altına ekle (ESI hazır).
2. Servoya sağ tık → **Add SoftMotion CiA402 Axis** (eksen objesi oluşur).
3. **Sync mode = DC-Sync (DC for synchronization)** seç; SYNC0 cycle = master cycle.
4. **Operation mode = CSP (8)** (senkron pozisyon) — CAM/interpolasyon için standart.
5. PDO eşlemesini doğrula: en az 6040h(Controlword), 6041h(Statusword), 607Ah(Target
   position), 6064h(Position actual) eşlenmeli. Tork/hız modu da kullanılacaksa 60FFh /
   6071h eklenir (datasheet register_map).
6. Eksen parametreleri (ölçek/scaling, yön, limitler) SoftMotion eksen ayarlarında.
7. PLCopen FB'leriyle sür: MC_Power → MC_Home → MC_MoveAbsolute vb.

### 6. Devreye Alma Doğrulaması

- Online'a geç → EtherCAT master durumunu kontrol et: tüm slave'ler **OP (Operational)**
  state'inde olmalı.
- Bus diagnostiği: kayıp frame, çalışma sayacı (working counter) hataları, DC senkron
  kayması.
- Servo: MC_Power ile enable, takip hatası (following error) ve DC jitter'ı izle.

## Örnekler

### Örnek — İki eksenli AM600 + GL20 EtherCAT yapısı

```
EtherCAT_Master  (cycle 1 ms, DC referans = ilk servo)
├── GL20-RTU-ECT            Sync: SM-Sync
│   ├── GL20-1600END   16 DI → %IX → GVL_IO.bIn[0..15]
│   └── GL20-0016ETN   16 DO → %QX → GVL_IO.bOut[0..15]
├── SV660N  → Axis_X   Sync: DC-Sync, Mode: CSP(8)
│   PDO: 6040h,6041h,607Ah,6064h
└── SV660N  → Axis_Y   Sync: DC-Sync, Mode: CSP(8)
```

### Örnek — Eksen sürme (PLCopen, ST — kavramsal)

```iecst
// Task_EtherCAT (yüksek öncelik, master cycle ile)
fbPowerX(Axis := Axis_X, Enable := TRUE, bRegulatorOn := TRUE, bDriveStart := TRUE);
IF fbPowerX.Status THEN
    fbMoveX(Axis := Axis_X, Execute := bGo, Position := 100.0,
            Velocity := 50.0, Acceleration := 200.0, Deceleration := 200.0);
END_IF
```

## Sık Yapılan Hatalar

- **Servoyu FreeRun'da bırakmak.** Senkron motion DC-Sync ister; FreeRun'da CSP ekseni
  titrer, takip hatası verir. Servo = DC-Sync, kural budur.
- **Çakışan ESI sürümleri.** Eski ESI silinmeden yenisini yüklemek → slave tanınmaz ya
  da yanlış PDO. Yenisini yüklemeden eskisini sil (MD800 kılavuzu).
- **Eksik PDO eşlemesi.** Controlword/Statusword eşlenmezse servo CiA402 durum makinesi
  asla "Operation Enabled"a geçmez; MC_Power Error verir.
- **Topoloji sırası ≠ fiziksel sıra.** Ağaçtaki slave sırası fiziksel hat sırasıyla
  eşleşmezse working counter / state hataları çıkar.
- **DC referansını yanlış slave'e vermek.** Referans saat DC-yetenekli ve hatta uygun
  konumda olmalı; tipik olarak ilk servo. I/O coupler'ı referans yapmak kararsızlık
  doğurabilir.
- **Cycle time çok agresif.** 250 µs altına inip hattaki slave sayısı/işlem yükünü
  hesaba katmamak frame kaçırmaya yol açar. GL20 min 125 µs destekler ama tüm hat
  bütçesi doğrulanmalı.
- **EtherCAT'i raporlama ağıyla karıştırmak.** EtherCAT gerçek-zaman kontroldür; MES/SCADA
  için OPC UA/Modbus ayrı katmandır (bkz. ÇELİŞKİLER ve networking/_synthesis).

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **DC-Sync + CSP:** Çok-eksenli senkron, CAM, elektronik dişli, interpolasyon — yani
  AM600/AC800'ün asıl varlık nedeni. Daima bu.
- **SM-Sync / FreeRun:** Saf I/O (GL20), senkron olmayan tekil eksen, ya da zamanlama
  kritik olmayan okuma/yazma. Gereksiz DC yükünden kaçınır.
- **EtherCAT kullanma / başka katman:** Fabrika üstü raporlama, SCADA, bulut →
  EtherCAT değil, OPC UA / MQTT (knowledge/codesys/networking/). Marka-bağımsız basit
  uzak I/O için PROFINET (GL20-RTU-PN varyantı) bir alternatif olabilir.

## Gerçek Proje Notları

- **DC senkron, motion projesinin "sessiz" kalbidir.** Eksenler "çalışıyor ama hafif
  titriyor / takip hatası alıyor" şikayetinin en sık kök nedeni yanlış/eksik DC-Sync'tir.
  Devreye almada her servonun gerçekten DC-Sync'te ve aynı SYNC0 cycle'da olduğunu
  online doğrulayın.
- **ESI sürüm hijyeni.** Sahada en çok zaman kaybettiren ikinci konu çakışan ESI'ler.
  Bir slave modeli için tek ve doğru sürümü havuzda tutun; firmware ile ESI sürümünü
  eşleştirin. Yeni sürüm yüklerken eskisini mutlaka silin.
- **CiA402 durum makinesi.** Servo enable olmuyorsa neredeyse her zaman Controlword/
  Statusword PDO eşlemesi ya da durum makinesi geçişi (Switch on disabled → Ready to
  switch on → Switched on → Operation enabled) sorunudur; ağ değil. 6041h Statusword'ü
  online izleyin.
- **SV660N vs IS620N.** İkisi de EtherCAT CiA402 servo; SV660N daha yeni (4.5 kHz akım
  çevrimi, 3 kHz hız bandı), IS620N bir önceki nesil (>4 kHz akım, 1.2 kHz hız bandı).
  InoProShop konfigürasyon akışı ikisinde de aynıdır; sadece doğru ESI seçilmeli.
- **AM600 32 eksen / AC800 256 eksen sınırı.** Proje eksen sayısı AM600'ü zorluyorsa
  (özellikle çok interpolasyon/CAM ekseni) AC800'e geçiş donanım kararıdır; EtherCAT
  konfigürasyon mantığı değişmez (bkz. 04).

## İlgili Konular

- `04_hardware_configuration.md` — Device Tree, master ekleme, %I/%Q, GL20 yerleşimi
- `01_inoproshop_overview.md` — InoProShop = CODESYS V3 (taban)
- `knowledge/codesys/networking/_synthesis.md` — raporlama protokolleri (EtherCAT'ten ayrı katman)
- `devices/INOVANCE_SV660N/datasheet.json` — CiA402 obje haritası, modlar
- `devices/INOVANCE_IS620N/datasheet.json` — CiA402 obje haritası, modlar
- `devices/INOVANCE_GL20/datasheet.json` — EtherCAT slave coupler, PDO/modül gerçekleri
