---
KONU        : EtherCAT — Gerçek-Zaman Fieldbus (Processing on the Fly, Distributed Clocks, ESM)
KATEGORİ    : networking
ALT_KATEGORI: fieldbus
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.ethercat.org/en/technology.html"
    başlık: "EtherCAT Technology Group (ETG) — EtherCAT Technology Overview"
    güvenilirlik: resmi
  - url: "https://www.ethercat.org/download/documents/ETG2200_V3i1i1_G_R_SlaveImplementationGuide.pdf"
    başlık: "ETG.2200 — EtherCAT SubDevice Implementation Guide V3.1.1"
    güvenilirlik: resmi
  - url: "https://infosys.beckhoff.com/content/1033/ethercatsystem/1036980875.html"
    başlık: "Beckhoff Infosys — EtherCAT State Machine"
    güvenilirlik: resmi
  - url: "https://infosys.beckhoff.com/content/1033/ethercatsystem/2469118347.html"
    başlık: "Beckhoff Infosys — EtherCAT Distributed Clocks"
    güvenilirlik: resmi
  - url: "https://en.wikipedia.org/wiki/EtherCAT"
    başlık: "EtherCAT — Wikipedia"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "_synthesis.md"
    ilişki: detaylandırır
  - konu: "04_canopen.md"
    ilişki: tamamlar
  - konu: "knowledge/inovance/inoproshop/05_ethercat_configuration.md"
    ilişki: kullanır
  - konu: "knowledge/inovance/inoproshop/06_motion_control.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: alternatif
ÖNKOŞUL     :
  - "Ethernet temelleri: frame, MAC, EtherType"
  - "Determinizm, jitter, çevrim süresi kavramları"
  - "Fieldbus üst sentezi (_synthesis.md) okunmuş olmalı"
ÇELİŞKİLER :
  - kaynak: "EtherCAT 'standart Ethernet mi?' tartışması"
    konu: "EtherCAT standart Ethernet frame kullanır ama standart switch ile çalışmaz"
    çözüm: >
      Fiziksel katman ve frame formatı standart Ethernet'tir (EtherType 0x88A4).
      Ancak slave'ler processing-on-the-fly yapan özel ESC (EtherCAT Slave Controller) ASIC'i
      kullanır ve topoloji genelde daisy-chain'dir; araya standart switch konmaz (gecikme/jitter bozar).
      "Standart Ethernet altyapısı üzerinde özel slave donanımı" doğru ifadedir.
  - kaynak: "Master için özel donanım gerekir mi?"
    konu: "EtherCAT master standart Ethernet NIC ile yazılımda çalışır"
    çözüm: >
      Master tarafı özel donanım GEREKTİRMEZ; standart NIC + yazılım yığını (CODESYS, TwinCAT,
      açık kaynak SOEM/IgH) yeterlidir. Özel ASIC yalnızca SLAVE tarafındadır (ESC).
---

## Özün Ne

EtherCAT (Ethernet for Control Automation Technology), Beckhoff tarafından geliştirilen ve EtherCAT Technology Group (ETG) tarafından yönetilen, IEC 61158/61784 standartlarına dahil bir gerçek-zaman fieldbus'tır. Temel yeniliği "processing on the fly" (uçarken işleme) prensibidir: tek bir Ethernet frame'i tüm slave cihazlardan zincir halinde geçer ve her slave kendi verisini frame hareket ederken donanımda okur/yazar. Bu sayede master tek frame ile yüzlerce cihazı tek çevrimde günceller ve %90'ın üzerinde Ethernet verimi sağlar.

EtherCAT'in asıl gücü senkron motion control'dür: Distributed Clocks (dağıtık saatler) ile tüm slave'ler genelde 100 nanosaniyenin altında bir toleransla senkronize çalışır. Bu nedenle CNC, robotik ve çok eksenli baskı gibi mikrosaniye senkronizasyon gerektiren uygulamalarda baskındır. EtherCAT, OPC UA/Modbus gibi raporlama protokollerinin **altında**, gerçek-zaman kontrol katmanında yer alır.

## Nasıl Çalışır

### Processing on the Fly (Uçarken İşleme)

EtherCAT'in kalbi budur. Geleneksel fieldbus'ta master her cihaza ayrı bir telgraf gönderir ve yanıt bekler; bu hem yavaş hem de cihaz CPU'suna bağımlıdır. EtherCAT'te ise:

```
Master (standart NIC)
   │  Tek Ethernet frame gönderir (EtherType 0x88A4)
   ▼
[Slave 1] ──► [Slave 2] ──► [Slave 3] ──► ... ──► [Slave N]
   │            │             │                      │
   │ Frame geçerken her slave:                       │
   │  - kendine adreslenmiş veriyi OKUR (input)       │
   │  - kendi verisini frame'e YAZAR (output)         │
   │  hepsi DONANIMDA (ESC ASIC), nanosaniyeler içinde │
   ▼                                                  ▼
Son slave frame'i geri yansıtır ──────────────────────┘
   │  (fiziksel olarak hat sonundan döner)
   ▼
Master frame'i geri alır → tüm process image tek turda güncellendi
```

Slave'ler frame'i durdurup işlemez; frame akarken (birkaç nanosaniye gecikmeyle) içinden kendi verisini alır ve kendi verisini ekler. Bu işi yapan donanım **ESC (EtherCAT Slave Controller)** ASIC'idir; slave'in ana CPU'su process data alışverişine karışmaz. Bu, performansı uygulamadan bağımsız ve öngörülebilir kılar.

### Frame ve Adresleme

- Frame: Standart Ethernet, EtherType **0x88A4**. İçinde bir veya daha fazla EtherCAT **datagram** taşır; her datagram bir komut (read / write / read-write) içerir.
- **Logical addressing (FMMU):** **FMMU (Fieldbus Memory Management Unit)**, her slave'in mantıksal 4 GB adres uzayındaki kendi bölümünü fiziksel belleğine eşler. Master tek bir mantıksal adres bloğuna yazar; FMMU sayesinde her slave kendi kısmını otomatik alır.
- **SyncManager:** Cyclic (process data) ve acyclic (mailbox) iletişim kanallarını yönetir; veri tutarlılığını ve master-slave bellek koordinasyonunu sağlar.

### Distributed Clocks (Dağıtık Saatler)

Senkron motion'ın temelidir. Bir referans slave'in (genelde ilk DC-yetenekli slave) saati sistem zamanı kabul edilir; diğer tüm slave'ler ona senkronlanır:

```
1. Master broadcast gönderir → tüm slave'ler iç saatlerini aynı anda latch'ler.
2. Master latch'lenen değerleri okur → her slave'e olan propagasyon gecikmesini hesaplar.
3. Her slave'in saatine offset + delay compensation yazılır.
4. Çalışma boyunca sürekli ölçüm/düzeltme yapılır (drift kompanzasyonu).
→ Sonuç: tüm DC-slave'ler < 1µs (tipik <100ns) toleransla senkron.
```

DC senkronizasyonu, çevrim süresinden ayrı bir mekanizmadır. Hızlı çevrim verim sağlar; DC senkronizasyon **eşzamanlılık** sağlar — motion için ikincisi zorunludur.

### EtherCAT State Machine (ESM)

Bir slave'in çalışır hale gelmesi katı bir durum makinesi izler. Her durumda farklı iletişim türleri açıktır:

```
┌──────┐  Master sync manager 0/1'i (mailbox) kurar
│ INIT │  Hiçbir iletişim yok.
└──┬───┘
   ▼
┌────────┐  Mailbox iletişimi AÇIK (CoE/FoE/EoE...). Process data YOK.
│ PRE-OP │  Master: SM (kanal 2+), FMMU, PDO mapping'i yapılandırır.
└──┬─────┘  Geçişte slave mailbox'ın doğru kurulduğunu kontrol eder.
   ▼
┌─────────┐ Mailbox AÇIK + Process data: input'lar OKUNUR, output'lar GÜVENLİ.
│ SAFE-OP │ Output'lar watchdog kontrollü, varsayılan güvenli durumda.
└──┬──────┘ Geçişte slave SM ve DC ayarlarını doğrular.
   ▼
┌─────┐    Mailbox AÇIK + Process data TAM (input + output uygulanır).
│ OP  │    Master geçişten ÖNCE geçerli output verisi göndermiş olmalı.
└─────┘    Normal çalışma durumu.

(BOOTSTRAP: yalnızca INIT'ten erişilir; firmware güncellemesi için, sadece FoE açık.)
```

Devreye almada en sık tuzak: slave **SAFE-OP'ta takılır** ve OP'a geçemez. Neden çoğunlukla output watchdog (master geçerli output göndermiyor) ya da DC ayarı uyuşmazlığıdır. **AL Status Code** (Application Layer status) hata nedenini doğrudan söyler.

### Mailbox Protokolleri (Acyclic İletişim)

Process data dışında, slave'lerle parametre/dosya/diagnostik için mailbox kullanılır:

| Protokol | Açılımı | Kullanım |
|---|---|---|
| **CoE** | CAN application protocol over EtherCAT | Object Dictionary erişimi (CANopen OD'sini EtherCAT üzerinde kullanır); sürücü parametreleri, CiA 402 |
| **FoE** | File access over EtherCAT | Firmware/dosya transferi (Bootstrap state'te) |
| **EoE** | Ethernet over EtherCAT | Standart Ethernet (TCP/IP) tünelleme — web arayüzü, ping |
| **SoE** | Servo profile over EtherCAT | IEC 61800-7-204 servo sürücü profili |
| **AoE** | ADS over EtherCAT | Beckhoff Automation Device Specification yönlendirme |

**CoE özellikle önemli:** EtherCAT sürücüleri çoğunlukla CANopen'ın CiA 402 sürücü profilini ve Object Dictionary yapısını CoE üzerinden kullanır. Yani CANopen bilgisi EtherCAT motion'a doğrudan aktarılır.

### ESI Dosyaları

**ESI (EtherCAT SubDevice/Slave Information)**, XML formatında cihaz tanım dosyasıdır. İçinde: cihaz kimliği, PDO eşleme seçenekleri, desteklenen mailbox protokolleri, senkronizasyon yetenekleri (DC desteği) yer alır. Master mühendislik aracı (CODESYS, TwinCAT) cihazı bu dosyayla tanır ve yapılandırır. **Doğru sürüm kritiktir:** firmware ile ESI eşleşmezse PDO mapping tutmaz.

### Senkronizasyon Modları

| Mod | Açıklama | Kullanım |
|---|---|---|
| **Free Run** | Slave kendi iç saatiyle çalışır, master çevrimine senkron değil | Senkronizasyon gerektirmeyen I/O |
| **SM-Sync** | SyncManager olayı ile tetiklenir; master frame'ine senkron | Orta hassasiyet I/O |
| **DC-Sync** | Distributed Clocks SYNC0/SYNC1 sinyaliyle tetiklenir; <1µs | Motion control — zorunlu |

## Pratikte Nasıl Kullanılır (CODESYS)

CODESYS EtherCAT master'ı **yerleşiktir** (ek lisans motion için SoftMotion). Tipik akış:

```
1. ESI kur: Tools → Device Repository → cihaz üreticisinin ESI XML'ini ekle.
2. Master ekle: Device ağacında Ethernet adaptörüne "EtherCAT Master SoftMotion" ekle.
   - Kullanılacak NIC'i seç (PLC'nin EtherCAT portu).
3. Slave ekle: Master altına cihazları topoloji sırasına göre ekle
   (sıra = fiziksel kablo sırası; EtherCAT'te adres = sıra).
4. PDO mapping: Her slave'in Process Data sekmesinde input/output PDO'larını seç,
   I/O mapping ile GVL değişkenlerine bağla.
5. Distributed Clocks: Motion gerekiyorsa master DC ayarını aç, referans slave seç,
   her motion slave'inde DC-Sync modunu etkinleştir.
6. Bus cycle task: Master'ı HIZLI, yüksek öncelikli bir task'a bağla
   (örn. 250µs–1ms, EtherCAT_Task). Bu task fieldbus çevrimini belirler.
7. SoftMotion: Sürücüleri SM_Drive_GenericDSP402 (CiA 402 / CoE) ekseni olarak ekle,
   MC_Power / MC_MoveAbsolute vb. ile kontrol et.
```

Process data GVL değişkenlerine bağlandıktan sonra aynı GVL, OPC UA Symbol Configuration ile SCADA'ya açılır — kontrol (EtherCAT) ve raporlama (OPC UA) aynı veriyi farklı katmanlarda paylaşır.

## Örnekler

### Örnek 1 — Topoloji ve Adresleme
```
PLC EtherCAT Master (NIC)
  └─ Slave 1: Servo sürücü A   (auto-increment addr 0, station 1001)
  └─ Slave 2: Servo sürücü B   (auto-increment addr -1, station 1002)
  └─ Slave 3: EK1100 I/O coupler
       └─ EL1008 (8x DI)
       └─ EL2008 (8x DO)
       └─ EL3064 (4x AI)

EtherCAT'te adres = fiziksel sıra. Kabloyu farklı sıraya takarsan adresler kayar.
Hot-connect grupları dışında topoloji sırası tasarımla eşleşmeli.
```

### Örnek 2 — SafeOp Takılması Teşhisi
```
Belirti : 6 servonun 1'i OP'a geçmiyor, SAFE-OP'ta kalıyor.
Adım 1  : Master diagnostic → AL Status Code oku (örn. 0x001E "Invalid Output Config").
Adım 2  : O slave'in PDO mapping'i diğerlerinden farklı mı? ESI sürümü eşleşiyor mu?
Çözüm   : Yanlış ESI sürümü → doğru firmware ESI'si ile PDO yeniden eşlendi → OP.
Ders    : Tek slave'in farklı davranması → o slave'in tanım dosyası/firmware'i farklı.
```

## Sık Yapılan Hatalar

### Hata 1: Araya Standart Switch Koymak
EtherCAT daisy-chain (ya da hat/ağaç) topolojisi bekler; slave'ler frame'i fiziksel olarak iletir. Araya standart bir Ethernet switch koymak gecikme/jitter ekler ve processing-on-the-fly'ı bozar. Dallanma gerekiyorsa EtherCAT junction (EK1122 gibi) kullan.

### Hata 2: DC'yi Açmadan Senkron Motion Beklemek
Çevrim hızlı olsa bile DC-Sync açılmadan eksenler senkron olmaz; interpolasyonda titreme görülür. Motion'da DC-Sync ayrıca yapılandırılır.

### Hata 3: Yanlış ESI Sürümü
Firmware güncellenmiş cihazda eski ESI → PDO mapping tutmaz, cihaz SafeOp'ta takılır. Firmware ile eşleşen ESI'yi üreticiden al, Device Repository'deki eskiyi temizle.

### Hata 4: Master'ı Yavaş Task'a Bağlamak (CODESYS)
EtherCAT master'ın bus cycle task'ı 100ms'lik yavaş task ise, fieldbus çevrimi 100ms olur ve tüm gerçek-zaman avantajı kaybolur. Master ayrı, hızlı, yüksek öncelikli task'a bağlanmalı.

### Hata 5: Kablo Sırasını Değiştirip Adres Kaymasını Görmezden Gelmek
Auto-increment adresleme fiziksel sıraya bağlıdır. Devreye almadan sonra kablo sırası değişirse cihazlar yer değiştirir; explicit station alias (configured station address) kullanmak bu riski azaltır.

## Ne Zaman Tercih Edilmeli / Edilmemeli

```
✓ Çok eksenli senkron motion (EtherCAT'in en güçlü olduğu alan)
✓ Yüzlerce hızlı I/O noktası, <1ms çevrim
✓ Beckhoff/CODESYS ekosistemi, SoftMotion entegrasyonu
✓ <1µs senkronizasyon gerektiren uygulamalar (CNC, baskı, robotik)
✓ FSoE ile fonksiyonel güvenlik (STO/SS1) gerekiyorsa

✗ Tesis tamamen Siemens (PROFINET) ya da Rockwell (EtherNet/IP) ise — ekosistem sürtünmesi
✗ Mobil makine / batarya / düşük maliyet tek-sürücü senaryosu (CANopen daha uygun)
✗ PLC → SCADA/MES raporlaması (OPC UA kullan; EtherCAT kontrol katmanıdır)
```

## Gerçek Proje Notları

**Not 1 — EtherCAT'in verimi "boş slot" hissi yaratır.** Tek frame'de 100+ cihaz güncellendiğinden, ağ trafiği şaşırtıcı derecede düşük görünür. Yeni mühendisler "bu kadar az trafikle bu kadar cihaz nasıl?" diye sorar — cevap processing-on-the-fly'dır; her cihaz için ayrı paket yoktur.

**Not 2 — SafeOp takılması neredeyse her zaman config, kablo değil.** Saha refleksi kabloyu suçlamaktır; oysa SafeOp→OP geçişi mantıksal bir adımdır (master geçerli output göndermeli, DC/SM doğru olmalı). AL Status Code okunmadan kablo değiştirmek zaman kaybıdır.

**Not 3 — CoE = EtherCAT'te CANopen bilgisi.** EtherCAT sürücüsünü CoE üzerinden CiA 402 nesneleriyle (6040h controlword, 6041h statusword, 6060h modes of operation) yönetirsin. CANopen 04_canopen.md bilgisi doğrudan EtherCAT motion'a transfer olur; ikisi ayrı öğrenilmez.

**Not 4 — Hot-connect ve modüler makineler.** Takılıp çıkarılabilen istasyonlar (örn. araç-üstü değişen alet) için hot-connect grupları tanımlanır; aksi halde bir grup eksikken tüm bus OP olamaz. Modüler makine tasarımında bu baştan planlanmalı.

**Not 5 — Cable redundancy ucuz ama master desteği gerekir.** EtherCAT'te ring kapatılarak (son slave master'ın ikinci portuna) kablo kopması toleransı sağlanır; ancak bu master tarafında redundancy lisansı/desteği ister. Kritik hatlarda planlanır.

## İlgili Konular

```
knowledge/networking/fieldbus/
├── _synthesis.md     → Dört fieldbus karşılaştırması, raporlama≠kontrol
├── 04_canopen.md     → CiA 402 sürücü profili (EtherCAT CoE ile aynı OD)
├── 02_profinet.md    → Alternatif Ethernet fieldbus (Siemens)
└── 03_ethernet_ip.md → Alternatif Ethernet fieldbus (Rockwell)

knowledge/inovance/inoproshop/
├── 05_ethercat_configuration.md → InoProShop'ta EtherCAT pratik kurulum
└── 06_motion_control.md         → SoftMotion / eksen kontrolü

Üst katman (raporlama):
knowledge/protocols/opc-ua/01_architecture.md → PLC↔SCADA (EtherCAT'in üstü)

Standartlar: IEC 61158 / IEC 61784 (ETG yönetir), ETG.2200 (Slave Implementation Guide)
Araçlar: TwinCAT diagnostics, Wireshark (ecat dissector), CODESYS Device Repository
```
