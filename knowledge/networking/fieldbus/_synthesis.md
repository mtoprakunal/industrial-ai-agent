---
KONU        : Gerçek-Zaman Fieldbus'lar — Karşılaştırmalı Üst Sentez (EtherCAT, PROFINET, EtherNet/IP, CANopen)
KATEGORİ    : networking
ALT_KATEGORI: fieldbus
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.ethercat.org/en/technology.html"
    başlık: "EtherCAT Technology Group — EtherCAT Technology Overview"
    güvenilirlik: resmi
  - url: "https://www.profibus.com/technology/profinet"
    başlık: "PROFIBUS & PROFINET International (PI) — PROFINET Technology"
    güvenilirlik: resmi
  - url: "https://www.odva.org/technology-standards/key-technologies/ethernet-ip/"
    başlık: "ODVA — EtherNet/IP & CIP Technology"
    güvenilirlik: resmi
  - url: "https://www.can-cia.org/can-knowledge/canopen"
    başlık: "CAN in Automation (CiA) — CANopen"
    güvenilirlik: resmi
  - url: "knowledge/protocols/_synthesis.md"
    başlık: "Endüstriyel Protokoller Üst Sentezi (OPC UA, Modbus, TCP, MQTT)"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_ethercat.md"
    ilişki: detaylandırır
  - konu: "02_profinet.md"
    ilişki: detaylandırır
  - konu: "03_ethernet_ip.md"
    ilişki: detaylandırır
  - konu: "04_canopen.md"
    ilişki: detaylandırır
  - konu: "knowledge/protocols/_synthesis.md"
    ilişki: tamamlar
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: alternatif
  - konu: "knowledge/networking/_synthesis.md"
    ilişki: gerektirir
  - konu: "knowledge/inovance/inoproshop/05_ethercat_configuration.md"
    ilişki: kullanır
  - konu: "knowledge/decisions/decision_framework"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Temel ağ kavramları: Ethernet, MAC/VLAN, TCP/IP, UDP"
  - "Endüstriyel katman modeli: fieldbus / SCADA / MES (Purdue/ISA-95)"
  - "Determinizm, jitter, çevrim süresi (cycle time) kavramları"
  - "raporlama ≠ kontrol ilkesi (knowledge/protocols/_synthesis.md)"
ÇELİŞKİLER :
  - kaynak: "Fieldbus vs OPC UA — hangisi 'daha iyi'?"
    konu: "Fieldbus ile OPC UA/Modbus aynı işi yapmaz; rakip değildirler"
    çözüm: >
      Fieldbus (EtherCAT/PROFINET/EtherNet/IP/CANopen) = gerçek-zaman KONTROL katmanı:
      deterministik, mikrosaniye-milisaniye çevrim, I/O ve motion senkronizasyonu.
      OPC UA/Modbus/MQTT = RAPORLAMA/komuta katmanı: SCADA/MES/bulut, deterministik değil.
      "raporlama ≠ kontrol": fieldbus PLC ile saha cihazı arasında, OPC UA PLC ile üst sistem arasında.
  - kaynak: "EtherCAT vs PROFINET 'hızlı/yavaş' tartışması"
    konu: "Çevrim süresi tek başına protokol üstünlüğü değildir"
    çözüm: >
      EtherCAT processing-on-the-fly ile <100µs DC senkronizasyon sağlar; PROFINET IRT ~31.25µs'e iner.
      Karar ekosistem (Beckhoff/CODESYS vs Siemens), topoloji, sertifikasyon ve cihaz mevcudiyetiyle verilir,
      ham hızla değil. Çoğu uygulamada her ikisi de fazlasıyla yeterli (1-4 ms tipik).
  - kaynak: "CANopen 'eski/yavaş' algısı"
    konu: "CANopen 1 Mbit/s CAN ile sınırlıdır ama hâlâ baskındır"
    çözüm: >
      CANopen bant genişliği düşüktür (max 1 Mbit/s klasik CAN) ama düşük maliyet, gürbüzlük ve
      CiA 402 olgunluğu sayesinde mobil makine, batarya, sürücü ve gömülü sistemlerde standarttır.
      Ethernet-tabanlılarla rakip değil; farklı bir maliyet/karmaşıklık noktasıdır. CANopen FD bant genişliğini açar.
---

## Özün Ne

Bu üst sentez, "Gerçek-zaman kontrol için hangi fieldbus'ı seçmeliyim ve neden?" sorusunu yanıtlar. Dört protokolün (EtherCAT, PROFINET, EtherNet/IP, CANopen) tek tek anlaşıldığı varsayılarak burada yalnızca **karşılaştırma, seçim rehberi ve ortak ilkeler** sunulur.

Kritik konumlandırma: bu dört protokol, OPC UA/Modbus/MQTT'nin **altındaki** katmandır. OPC UA üst sentezinde tekrar edilen "raporlama ≠ kontrol" ilkesinin kontrol tarafı tam olarak burasıdır. SCADA bir setpoint yazar (OPC UA), PLC bunu alır ve servo sürücüye fieldbus üzerinden deterministik biçimde iletir (EtherCAT/PROFINET). İki katman birbirinin yerine kullanılamaz.

**Uzman mesajı:** Dört fieldbus rakip değil, **iki eksende** konumlanan ve **üç ortak ilkeyle** yönetilen araçlardır. Doğru fieldbus'ı seçmek çoğunlukla teknik üstünlük değil, **ekosistem ve cihaz mevcudiyeti** kararıdır.

---

## Birleştirici İlke: İki Eksen + Üç Ortak İlke

**İki eksen** (fieldbus'ı SEÇTİREN — "hangisi?"):
1. **Taşıyıcı katman** — Ethernet-tabanlı (EtherCAT, PROFINET, EtherNet/IP) ↔ CAN-tabanlı (CANopen). Ethernet = yüksek bant + düşük çevrim; CAN = düşük maliyet + gürbüzlük + sınırlı bant (≤1 Mbit/s).
2. **Ekosistem** — EtherCAT (Beckhoff/CODESYS dünyası), PROFINET (Siemens dünyası), EtherNet/IP (Rockwell/Allen-Bradley dünyası), CANopen (sürücü/mobil makine/gömülü). Saha çoğunlukla PLC markası seçer, fieldbus onu izler.

**Üç ortak ilke** (fieldbus'ı KURAN — "nasıl sağlam?"):
1. **Cihaz açıklama dosyası kutsaldır** — Her fieldbus bir XML/metin tanım dosyası kullanır (EtherCAT ESI, PROFINET GSDML, EtherNet/IP EDS, CANopen EDS/CiA306). Sürüm uyumsuzluğu, yanlış dosya ya da eksik dosya devreye almanın #1 sorunudur.
2. **State machine / başlatma sırası** — Hepsinde cihazın çalışır hale gelmesi bir durum makinesi izler (EtherCAT INIT→OP, CANopen NMT, PROFINET AR kurulumu, EtherNet/IP Forward_Open). Cihaz OP/Operational değilse veri akmaz; hata teşhisi durum makinesinde başlar.
3. **Senkronizasyon ≠ sadece hız** — Çevrim süresi (cycle time) ile senkronizasyon (jitter/eşzamanlılık) farklı şeylerdir. Motion control için DC/IRT/isochronous senkronizasyon gerekir; yalnız hızlı çevrim yetmez. Determinizm bu katmanın varlık nedenidir.

| Eksen / İlke | EtherCAT | PROFINET | EtherNet/IP | CANopen |
|---|---|---|---|---|
| Taşıyıcı | Ethernet (processing on the fly) | Ethernet (Layer 2 RT/IRT) | Ethernet (CIP/UDP/TCP) | CAN (≤1 Mbit/s) |
| Ekosistem | Beckhoff/CODESYS | Siemens | Rockwell/AB | Sürücü/mobil/gömülü |
| Tanım dosyası | ESI (XML) | GSDML (XML) | EDS (metin) | EDS/CiA306 (metin) |
| State machine | ESM: INIT→PreOp→SafeOp→OP | AR/CR kurulum | Forward_Open / CIP conn. | NMT: Init→PreOp→Op |
| Senkronizasyon | Distributed Clocks (<1µs) | IRT (isochronous) | CIP Sync / CIP Motion | SYNC objesi |
| Tipik çevrim | 50µs–1ms | RT ~1-10ms / IRT ~31µs | ~1-500ms RPI | 1-10ms |
| Standart | IEC 61158/61784 (ETG) | IEC 61158/61784 (PI) | IEC 61158/61784 (ODVA) | IEC 61800-7 / CiA 301,402 |

**Uzman içgörüsü:** Bir fieldbus sorununda önce ekseni belirle (yanlış protokol mü — Siemens hattına EtherCAT mı zorluyorsun?), sonra ihlal edilen ortak ilkeyi kontrol et (yanlış/eski tanım dosyası mı, cihaz OP değil mi, senkronizasyon mu kurulmamış?). "Eksen sayacı atlıyor / motion senkron değil" → çoğunlukla senkronizasyon modu (DC/IRT) yapılandırılmamıştır, ham hız değil.

---

## Nasıl Çalışır

### Dört Fieldbus'ın Konumlandırma Haritası

```
  CAN-tabanlı ◄──────────────────────────────────► Ethernet-tabanlı
  ───────────────────────────────────────────────────────────────────
  CANopen              EtherNet/IP        PROFINET           EtherCAT
  (CiA 301/402)        (CIP/ODVA)         (PI)               (ETG)
  ≤1 Mbit/s            standart switch    standart/IRT       özel ASIC slave
  Düşük maliyet        Rockwell dünyası   Siemens dünyası    Beckhoff/CODESYS
  Sürücü, batarya      I/O, sürücü        I/O, motion        Motion, hızlı I/O
  SYNC objesi          producer/consumer  RT/IRT             processing on the fly
  EDS/CiA306           EDS                GSDML              ESI

      DETERMİNİZM / SENKRONİZASYON ───────────────────────────────►
  SYNC objesi          CIP Sync           IRT isochronous    DC < 1µs jitter
```

### Mental Model: Üç Ethernet Yaklaşımı + Bir CAN

```
> EtherCAT: "Tek tren tüm istasyonlardan geçer." Bir Ethernet frame'i tüm
  slave'lerden zincir halinde geçer; her slave kendi verisini frame hareket
  ederken okur/yazar (processing on the fly). Master tek frame ile yüzlerce
  cihazı tek çevrimde günceller. Distributed Clocks ile <1µs senkron. En verimli.

> PROFINET: "Standart Ethernet üzerinde öncelikli trafik." RT için Layer 2'de
  VLAN öncelikli frame (EtherType 0x8892); IRT için zaman-dilimli (scheduled)
  bant rezervasyonu ve özel switch'ler. TCP/IP de aynı kablo üzerinde koşar
  (parametre/diagnostik). Siemens ekosisteminin omurgası.

> EtherNet/IP: "Standart TCP/UDP üzerinde nesne modeli (CIP)." Her cihaz CIP
  nesnesi; implicit (I/O, UDP 2222, producer/consumer) gerçek-zaman, explicit
  (TCP 44818) konfig/diagnostik. DeviceNet/ControlNet ile aynı CIP modeli.
  Rockwell/Allen-Bradley dünyası.

> CANopen: "Düşük maliyetli, gürbüz CAN üzerinde olgun sürücü profili." Object
  Dictionary + PDO (gerçek-zaman) / SDO (konfig) + NMT (durum) + CiA 402 sürücü
  profili. Bant düşük ama ucuz, dayanıklı, her yerde. Mobil makine, batarya, servo.
```

---

## Hızlı Referans Tabloları

### Tablo 1 — Senaryo → Fieldbus Seçim Rehberi (KRİTİK)

| Senaryo | Önerilen | Gerekçe |
|---|---|---|
| Çok eksenli senkron motion (CNC, robot, baskı) | **EtherCAT** | Distributed Clocks <1µs, processing on the fly, CODESYS SoftMotion |
| Yüksek sayıda hızlı dijital I/O, kısa çevrim | **EtherCAT** | Tek frame'de yüzlerce nokta, en yüksek verim |
| Siemens S7 PLC tabanlı hat | **PROFINET** | Aynı ekosistem, TIA Portal, GSDML hazır |
| Mevcut PROFIBUS hattını Ethernet'e taşıma | **PROFINET** | PI geçiş yolu, proxy cihazlar |
| Rockwell/Allen-Bradley ControlLogix tabanlı hat | **EtherNet/IP** | Studio 5000, CIP ekosistemi |
| Mevcut DeviceNet/ControlNet modernizasyonu | **EtherNet/IP** | Aynı CIP nesne modeli, EDS taşınır |
| Mobil makine, tarım/inşaat aracı, batarya yönetimi | **CANopen** | Gürbüz, ucuz, kablo dayanıklı, CiA profilleri |
| Tek/birkaç servo sürücü, düşük maliyet | **CANopen (CiA 402)** | Olgun sürücü profili, basit donanım |
| Karışık marka cihaz + güvenlik gerektiren motion | **EtherCAT (FSoE)** veya **PROFINET (PROFIsafe)** | Fieldbus üzeri güvenlik profili |
| PLC → SCADA/MES veri aktarımı | **OPC UA (fieldbus DEĞİL)** | Raporlama katmanı; bkz. protocols/_synthesis |
| PLC → bulut | **MQTT (fieldbus DEĞİL)** | Raporlama; fieldbus saha kontrol katmanı |

### Tablo 2 — Protokol × Özellik Matrisi

| Özellik | EtherCAT | PROFINET | EtherNet/IP | CANopen |
|---|---|---|---|---|
| Standart organizasyon | ETG | PI (PROFIBUS&PROFINET Int.) | ODVA | CiA |
| IEC standardı | 61158/61784 | 61158/61784 | 61158/61784 | 61800-7-201/301 |
| Fiziksel katman | Ethernet 100 Mbit/s | Ethernet 100M/1G | Ethernet 100M/1G | CAN ≤1 Mbit/s |
| İletişim modeli | Master/Slave, tek frame | IO Controller/Device | Producer/Consumer (CIP) | Master/Slave + producer (PDO) |
| Gerçek-zaman taşıma | Processing on the fly | RT (L2 0x8892) / IRT | Implicit UDP 2222 | PDO (CAN ID önceliği) |
| Konfig/diagnostik taşıma | Mailbox (CoE/FoE/EoE) | TCP/UDP (NRT) | Explicit TCP 44818 | SDO |
| Senkronizasyon | Distributed Clocks | IRT isochronous | CIP Sync/Motion | SYNC objesi |
| Tipik çevrim süresi | 50µs–1ms | 1-10ms (RT), 31µs (IRT) | 1-500ms (RPI) | 1-10ms |
| Tanım dosyası | ESI (XML) | GSDML (XML) | EDS (metin) | EDS (CiA306, metin) |
| Cihaz durum makinesi | ESM (INIT→OP) | AR/CR | CIP connection | NMT |
| Güvenlik profili | FSoE (Safety over EtherCAT) | PROFIsafe | CIP Safety | (yok; CANopen Safety nadiren) |
| CODESYS desteği | Yerleşik master + SoftMotion | Master/Device (eklenti) | Scanner/Adapter (eklenti) | Master/Slave manager (yerleşik) |
| Tipik kablo | Standart Ethernet (CAT5e+) | Standart/yönetilen switch'li | Standart switch'li | İki telli twisted pair (CAN_H/L) |

### Tablo 3 — Senkronizasyon Mekanizması Karşılaştırması

| Mekanizma | EtherCAT | PROFINET | EtherNet/IP | CANopen |
|---|---|---|---|---|
| Saat dağıtımı | Distributed Clocks (referans slave saati) | IRT zaman dilimleme + senkron domain | CIP Sync (IEEE 1588 PTP) | SYNC mesajı (master üretir) |
| Tipik jitter | < 1µs (genelde <100ns) | < 1µs (IRT) | PTP'ye bağlı (~µs) | SYNC periyoduna bağlı (~ms) |
| Sync modları | Free Run, SM-Sync, DC-Sync | RT (senkronsuz çevrim), IRT (isochronous) | RPI tabanlı, CIP Motion için PTP | async / SYNC-driven PDO |
| Motion için | DC-Sync zorunlu | IRT (CC-C) zorunlu | CIP Motion + CIP Sync | SYNC + interpolated position mode |

---

## Pratikte Nasıl Kullanılır

### Tipik Mimari: Fieldbus Nerede, Raporlama Nerede?

```
  ┌────────────────────────────────────────────────────────────────┐
  │  MES / BULUT                                                    │
  │      ▲  OPC UA / MQTT  (RAPORLAMA — deterministik DEĞİL)        │
  ├──────┴──────────────────────────────────────────────────────────┤
  │  SCADA / HMI                                                    │
  │      ▲  OPC UA / Modbus TCP  (RAPORLAMA + komuta)               │
  ├──────┴──────────────────────────────────────────────────────────┤
  │  PLC  (CODESYS / Siemens / Rockwell)                            │
  │      │  ◄── Burada katman değişir: raporlama yukarı, kontrol aşağı │
  │      ▼  FIELDBUS  (KONTROL — deterministik, < 1ms)              │
  │   ┌──────────┬──────────┬──────────────┬──────────┐            │
  │   EtherCAT   PROFINET   EtherNet/IP    CANopen                 │
  ├───┴──────────┴──────────┴──────────────┴──────────┴────────────┤
  │  SAHA CİHAZLARI                                                 │
  │   Servo sürücü · I/O modülü · VFD · sensör · valf adası · enkoder│
  └────────────────────────────────────────────────────────────────┘
```

### Devreye Alma Ortak Akışı (Dört Fieldbus İçin)

```
1. Tanım dosyasını al ve içe aktar
   EtherCAT → ESI (.xml)  ·  PROFINET → GSDML  ·  EtherNet/IP → EDS  ·  CANopen → EDS
   DOĞRU SÜRÜM önemli: cihaz firmware'i ile dosya eşleşmeli.
2. Cihazı topolojiye/ağa ekle, adres/isim ata
   EtherCAT → otomatik (sıra=adres)  ·  PROFINET → DCP ile isim+IP  ·
   EtherNet/IP → IP (BOOTP/DHCP/statik)  ·  CANopen → Node-ID (1-127) + baud
3. Process data (PDO / I/O) eşlemesini yap
   EtherCAT → PDO mapping (ESI)  ·  PROFINET → modül/submodül slot  ·
   EtherNet/IP → assembly instance (input/output)  ·  CANopen → PDO mapping (OD)
4. Senkronizasyon modunu seç
   Motion gerekiyorsa: EtherCAT DC-Sync · PROFINET IRT · EtherNet/IP CIP Motion · CANopen SYNC
5. State machine'i OP/Operational'a getir, teşhis et
   Veri akmıyorsa cihaz hangi state'te takıldı? (en sık SafeOp/PreOp'ta kalma)
```

### CODESYS Tarafı (Ortak Notlar)

CODESYS dört fieldbus için de master/slave yapılandırma sağlar (EtherCAT yerleşik + SoftMotion, PROFINET/EtherNet/IP eklenti, CANopen yerleşik manager). Ortak CODESYS gerçekleri:
- Fieldbus master'ı bir **bus cycle task**'a bağlanır; bu task'ın çevrim süresi fieldbus çevrim süresini belirler. Yanlış task ataması en sık yapılandırma hatasıdır.
- Tanım dosyaları (ESI/GSDML/EDS) **Device Repository**'ye kurulur; eksikse cihaz ağaca eklenemez.
- I/O mapping ile process data GVL değişkenlerine bağlanır — buradan sonrası "raporlama" katmanına (OPC UA Symbol Config vb.) aynı GVL üzerinden açılır.

---

## Örnekler

### Örnek 1 — Aynı Hattın Dört Farklı Fieldbus Tasarımı

```
Senaryo: 6 eksenli pick-and-place hücresi (6 servo + 32 DI/DO + 1 görüntü tetiği)

EtherCAT çözümü (Beckhoff/CODESYS):
  PLC → EtherCAT master → 6 servo (DC-Sync) + EK1100 I/O coupler
  Tek frame tüm cihazları 250µs'de günceller; senkron interpolasyon mükemmel.

PROFINET çözümü (Siemens):
  S7-1500 IO Controller → 6 SINAMICS sürücü (IRT) + ET200 I/O
  IRT domain kurulur; isochronous mode ile eksenler senkron.

EtherNet/IP çözümü (Rockwell):
  ControlLogix → Kinetix sürücüler (CIP Motion + CIP Sync) + Point I/O
  Producer/consumer; RPI ayarlanır; CIP Motion ekseni senkronlar.

CANopen çözümü (maliyet odaklı):
  PLC CANopen master → 6 CiA 402 sürücü + I/O node
  SYNC + interpolated position mode; bant nedeniyle çevrim ~2-4ms,
  yüksek hız senkron motion için sınırda — bu senaryoda EtherCAT/PROFINET üstün.
```

### Örnek 2 — "raporlama ≠ kontrol" İki Katmanı Birlikte

```
CODESYS PLC:
  AŞAĞI (kontrol):  EtherCAT master → servo + I/O   (250µs, DC-Sync, deterministik)
  YUKARI (rapor):   OPC UA Server (4840) → SCADA     (subscription, deterministik DEĞİL)
                    MQTT Publisher → bulut historian  (500ms, fire-and-forget)

SCADA "Start" basar → OPC UA Write → GVL_HMI.xStart
  → PLC mantığı → EtherCAT process data → servo hareketi (deterministik)
SCADA gerçek pozisyonu izler → OPC UA Subscription ← GVL.rActualPos ← EtherCAT input

Setpoint yolu OPC UA (raporlama), hareketin kendisi EtherCAT (kontrol). Karışmaz.
```

---

## Sık Yapılan Hatalar

### Hata 1: Fieldbus'tan Raporlama Katmanı İşi Beklemek (veya tersi)
```
Senaryo: "EtherCAT'i SCADA'ya doğrudan bağlayayım" veya "MQTT ile servo senkronlasın".
Sorun  : Fieldbus saha-PLC kontrol katmanı; SCADA/bulut bağlantısı PLC üzerinden
         OPC UA/MQTT ile yapılır. Tersi de yanlış: MQTT/Modbus deterministik değil,
         motion senkronizasyonu yapamaz.
Kural  : raporlama ≠ kontrol. Fieldbus aşağı, OPC UA/MQTT yukarı. Karışmaz.
```

### Hata 2: Yanlış / Eski Tanım Dosyası (ESI/GSDML/EDS)
```
Senaryo: Cihaz firmware güncellendi ama eski ESI/GSDML/EDS kullanıldı.
Etki   : PDO/assembly eşlemesi tutmaz; cihaz tanınmaz ya da yanlış veri okunur.
Kural  : Tanım dosyası firmware sürümüyle eşleşmeli. Üreticinin resmi sitesinden,
         doğru sürümü al. Device Repository'de eski sürümleri temizle.
```

### Hata 3: Cihazı OP/Operational'a Getirmemek
```
Senaryo: EtherCAT slave SafeOp'ta takıldı; PROFINET device AR kuramadı;
         CANopen node PreOp'ta kaldı; veri akmıyor sanılıyor "ağ bozuk".
Kural  : Önce state machine'e bak. EtherCAT: AL Status Code neden OP'a geçmiyor?
         CANopen: NMT Start gönderildi mi? Veri yokluğu = state sorunu, kablo değil.
```

### Hata 4: Senkronizasyonu Hızla Karıştırmak
```
Senaryo: Çevrim 250µs'e indirildi ama eksenler hâlâ senkron değil; jitter var.
Etki   : Hızlı çevrim ≠ senkron. Motion için DC-Sync (EtherCAT) / IRT (PROFINET) /
         CIP Sync (EtherNet/IP) / SYNC (CANopen) AYRICA yapılandırılmalı.
Kural  : Motion control'da senkronizasyon modu açıkça kurulur; sadece çevrim hızı yetmez.
```

### Hata 5: Fieldbus Master'ı Yanlış Task'a Bağlamak (CODESYS)
```
Senaryo: EtherCAT master'ın bus cycle task'ı 100ms'lik yavaş task'a bağlandı.
Etki   : Fieldbus çevrimi 100ms'e çıktı; tüm "gerçek-zaman" avantajı kayboldu.
Kural  : Master'ı hızlı, yüksek öncelikli, jitter'sız bir bus cycle task'a bağla.
```

### Hata 6: CANopen'dan Ethernet Bant Genişliği Beklemek
```
Senaryo: 20 CANopen node'a 1ms'de büyük PDO trafiği yüklendi.
Etki   : CAN bus ≤1 Mbit/s doyar; PDO'lar gecikir, çevrim kayar, eksen titrer.
Kural  : CANopen bütçesini hesapla (node × PDO × periyot ≤ bus kapasitesi).
         Yüksek bant gerekiyorsa Ethernet-tabanlı (EtherCAT/PROFINET) seç, ya da CANopen FD.
```

---

## Ne Zaman Tercih Edilmeli / Edilmemeli

```
EtherCAT seç:
  ✓ Çok eksenli senkron motion (en güçlü olduğu alan), <1ms çevrim, yüzlerce I/O
  ✓ Beckhoff/CODESYS ekosistemi; SoftMotion ile entegrasyon
  ✓ Distributed Clocks ile <1µs senkron gerekiyor
  ✗ Mevcut hat tamamen Siemens/Rockwell ise (ekosistem sürtünmesi)

PROFINET seç:
  ✓ Siemens S7 / TIA Portal ekosistemi
  ✓ PROFIBUS modernizasyonu, geniş cihaz mevcudiyeti
  ✓ PROFIsafe ile güvenlik, MRP ile ring redundancy
  ✗ En düşük maliyet veya en yüksek motion verimi birincil hedefse

EtherNet/IP seç:
  ✓ Rockwell/Allen-Bradley ControlLogix / Studio 5000 ekosistemi
  ✓ Mevcut DeviceNet/ControlNet'ten CIP taşınması
  ✓ Standart Ethernet altyapısı yeterli, CIP Safety ile güvenlik
  ✗ Siemens/Beckhoff ağırlıklı tesis ise

CANopen seç:
  ✓ Düşük maliyet, gürbüz kablo, mobil/gömülü/batarya/tek sürücü
  ✓ CiA 402 olgun sürücü profili; basit donanım
  ✓ Sınırlı sayıda cihaz, orta hız (1-10ms) yeterli
  ✗ Yüksek bant, çok cihaz, mikrosaniye senkron motion (Ethernet-tabanlı seç)

Hiçbiri (yanlış katman):
  ✗ PLC → SCADA/MES/bulut: OPC UA / Modbus / MQTT kullan (raporlama, fieldbus değil)
```

---

## Gerçek Proje Notları

**Not 1 — Fieldbus kararı çoğunlukla PLC markası kararıdır.** Sahada "EtherCAT mi PROFINET mi daha iyi" tartışması teknik değil ekosistem tartışmasıdır. Müşteri S7 kullanıyorsa PROFINET, ControlLogix kullanıyorsa EtherNet/IP, CODESYS/Beckhoff ise EtherCAT pratik olarak verilmiş karardır. Teknik üstünlük farkı çoğu uygulamada ölçülemeyecek kadar küçüktür; ekosistem sürtünmesi (mühendislik aracı, cihaz desteği, yedek parça) çok daha pahalıdır.

**Not 2 — Tanım dosyası sürüm uyumsuzluğu devreye almayı en çok geciktiren tek şey.** ESI/GSDML/EDS dosyasının cihaz firmware'iyle eşleşmemesi, saatlerce "cihaz neden tanınmıyor" aramasına yol açar. Devreye almadan önce her cihazın firmware sürümünü not et, üreticiden tam eşleşen dosyayı indir, eski sürümleri repository'den temizle.

**Not 3 — "Veri akmıyor" sorununun %80'i state machine'de çözülür.** EtherCAT slave SafeOp'ta takılır (genelde output watchdog ya da DC ayarı), CANopen node Start NMT almamıştır, PROFINET device AR kuramamıştır (isim/IP uyuşmazlığı). Kablo/donanım suçlamadan önce cihazın hangi state'te olduğuna ve neden ilerlemediğine bak. EtherCAT'te AL Status Code, CANopen'da EMCY mesajı doğrudan nedeni söyler.

**Not 4 — Senkronizasyon ile çevrim hızını karıştırmak motion projelerini batırır.** Bir baskı makinesinde eksenler "hızlı ama senkron değil" titriyordu; çevrim 250µs idi ama DC-Sync açılmamıştı. DC etkinleştirilince <1µs senkron sağlandı ve titreme bitti. Çevrim hızı verimi belirler; senkronizasyon eşzamanlılığı belirler — ikisi ayrı ayarlardır.

**Not 5 — CANopen bant bütçesi hesaplanmadan tasarlanırsa sahada doyar.** Klasik CAN ≤1 Mbit/s'tir; node sayısı × PDO boyutu × frekans kapasiteyi aşarsa PDO'lar gecikir ve "rastgele" eksen titremesi/iletişim hatası görülür. Tasarım aşamasında bus yükü hesaplanmalı; aşılıyorsa SYNC periyodu büyütülür, PDO sayısı azaltılır ya da Ethernet-tabanlı protokole/CANopen FD'ye geçilir.

**Not 6 — Güvenlik fieldbus üzerinde ayrı profildir, ağ izolasyonu değil.** Motion güvenliği (STO, SS1) için fieldbus üstü güvenlik profili kullanılır: EtherCAT'te FSoE, PROFINET'te PROFIsafe, EtherNet/IP'de CIP Safety. Bunlar "black channel" prensibiyle normal fieldbus üzerinden güvenli telegramlar taşır. Modbus/OPC UA'daki "ağ izolasyonu ile güvenlik" yaklaşımından farklıdır; burada fonksiyonel güvenlik (SIL/PL) söz konusudur.

## İlgili Konular

```
knowledge/networking/fieldbus/
├── 01_ethercat.md      → EtherCAT: processing on the fly, DC, ESM, CoE/FoE, sync, CODESYS master
├── 02_profinet.md      → PROFINET: RT/IRT, GSDML, IO controller/device, conformance classes
├── 03_ethernet_ip.md   → EtherNet/IP: CIP, implicit/explicit, EDS, assembly, producer/consumer
├── 04_canopen.md       → CANopen: CiA 301, NMT, PDO/SDO, OD, EDS, CiA 402 sürücü profili
└── _synthesis.md (bu belge)

Üst katman (RAPORLAMA — fieldbus değil):
knowledge/protocols/_synthesis.md        → OPC UA, Modbus, TCP, MQTT karşılaştırması
knowledge/protocols/opc-ua/01_architecture.md → PLC↔SCADA raporlama katmanı

Bağlı:
knowledge/networking/_synthesis.md       → topoloji, güvenlik, performans
knowledge/inovance/inoproshop/05_ethercat_configuration.md → InoProShop EtherCAT pratiği
knowledge/decisions/decision_framework   → raporlama ≠ kontrol karar çerçevesi

Araçlar:
  TwinCAT / EtherCAT diagnostics  → ESM state, AL Status Code
  Wireshark (EtherCAT, PN-DCP, ENIP, CANopen dissector) → trafik analizi
  CANopen: PCAN-View, kvaser     → CAN bus izleme, NMT/PDO/SDO
  CODESYS Device Repository      → ESI/GSDML/EDS yönetimi
```
