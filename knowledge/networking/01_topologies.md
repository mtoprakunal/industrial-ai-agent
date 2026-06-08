---
KONU        : Endüstriyel Ağ Topolojileri
KATEGORİ    : networking
ALT_KATEGORI: networking
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "https://us.profinet.com/wp-content/uploads/2019/08/Topology.pdf"
    başlık: "PROFINET Topology Options — PI North America Resmi Belgesi"
    güvenilirlik: resmi
  - url: "https://copperhilltech.com/blog/industrial-ethernet-guide-network-topologies/"
    başlık: "Industrial Ethernet Guide: Network Topologies — Copperhill Technologies"
    güvenilirlik: topluluk
  - url: "https://scadaprotocols.com/media-redundancy-protocol-mrp-industrial-ethernet/"
    başlık: "MRP Media Redundancy Protocol — SCADA Protocols"
    güvenilirlik: topluluk
  - url: "https://www.perle.com/supportfiles/mrp.shtml"
    başlık: "Ring Protocol MRP (IEC 62439-2) — Perle Systems"
    güvenilirlik: topluluk
  - url: "https://en.wikipedia.org/wiki/Media_Redundancy_Protocol"
    başlık: "Media Redundancy Protocol — Wikipedia"
    güvenilirlik: topluluk
  - url: "https://aercoiot.com/redundancy-ring-protocols-for-industrial-networks/"
    başlık: "Ring Redundancy Protocols for Industrial Ethernet — AercoIoT"
    güvenilirlik: topluluk
  - url: "https://www.checkpoint.com/cyber-hub/network-security/what-is-industrial-control-systems-ics-security/purdue-model-for-ics-security/"
    başlık: "Purdue Model for ICS Security — Check Point Software"
    güvenilirlik: topluluk
  - url: "https://inductiveautomation.com/resources/article/the-purdue-model-and-ignition"
    başlık: "The Purdue Model and Ignition — Inductive Automation"
    güvenilirlik: topluluk
  - url: "https://connect981.com/faqs/what-is-the-isa-95-purdue-model"
    başlık: "What is the ISA-95 Purdue Model?"
    güvenilirlik: topluluk
  - url: "https://www.come-star.com/blog/redundant-ring-protocols/"
    başlık: "Key Industrial Redundant Ring Protocols — Come-Star"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/networking/02_security.md"
    ilişki: tamamlar
  - konu: "knowledge/networking/03_performance.md"
    ilişki: tamamlar
  - konu: "knowledge/standards/02_iec62443"
    ilişki: gerektirir
  - konu: "knowledge/protocols/profinet/"
    ilişki: kullanır
  - konu: "knowledge/protocols/ethercat/"
    ilişki: kullanır
  - konu: "knowledge/hardware/"
    ilişki: kullanır
ÖNKOŞUL     :
  - "OSI modeli (Katman 1-2 fiziksel/veri bağlantı) temel bilgisi"
  - "Switch, hub, router kavramları"
  - "IP adresleme ve VLAN kavramı"
ÇELİŞKİLER :
  - kaynak: "Çeşitli endüstriyel Ethernet kılavuzları"
    konu: "Halka topolojisinde MRP mi, RSTP mi?"
    çözüm: >
      RSTP (IEEE 802.1w) genel amaçlı IT ağları için tasarlanmıştır ve yeniden
      yapılandırma süresi 1-30 saniye arasında değişebilir. Endüstriyel ortamda
      bu süre watchdog tetiklemesine yol açar. IEC 62439-2 kapsamındaki MRP ise
      50 düğüme kadar < 200 ms, yapılandırmaya bağlı olarak < 10 ms'ye kadar
      iner. PROFINET ortamlarında MRP zorunlu tercih, EtherNet/IP ortamlarında
      DLR (ODVA, < 3 ms) önerilir.
  - kaynak: "PI North America vs çeşitli topluluk kaynakları"
    konu: "Ağaç (tree) topolojinin doğrusal ile karışması"
    çözüm: >
      Bazı kaynaklar 'ağaç' yerine 'daisy chain' veya 'line' terimini kullanır.
      PI North America belgesi (Topology.pdf) line, star, tree ve ring olarak
      dört temel kategori tanımlar. Bu belgede de aynı sınıflandırma benimsenir.
---

## Özün Ne

Endüstriyel ağ topolojisi, bir otomasyonu oluşturan düğümlerin (PLC, HMI, sensör, switch) ve bağlantıların (kablo, optik fiber) birbirlerine göre nasıl düzenlendiğini tanımlar. Doğru topoloji seçimi; ağın arıza toleransını, gecikme bütçesini, bakım kolaylığını ve büyüme kapasitesini doğrudan belirler.

PI North America'nın resmi PROFINET belgesi, endüstriyel kablolu ağlar için dört temel topoloji kategorisi tanımlar: **doğrusal (line/bus), yıldız (star), halka (ring) ve ağaç (tree)**. Gerçek tesisler ise bu temel yapıların karışımından oluşan hibrit topolojiler kullanır. Yalnızca fiziksel yapı değil, **Purdue/ISA-95 modeli** gibi katmanlı mimari yaklaşımlar da bir "topoloji kararı"dır; zira hangi cihazların hangi katmanda yer alacağını ve katmanlar arası geçiş noktalarını (DMZ, güvenlik duvarı) belirler.

Endüstriyel ağ tasarımı IT ağ tasarımından kritik bir noktada ayrışır: Öncelik sırası **Kullanılabilirlik → Bütünlük → Gizlilik** (AIC) şeklindedir; IT'nin CIA üçgeninin tam tersidir. Bu yüzden topoloji kararları her zaman "arıza olduğunda ne olur?" sorusunu merkeze alır.

## Nasıl Çalışır

### Dört Temel Topoloji

#### 1. Doğrusal Topoloji (Line / Bus)

```
[PLC 1]──[Cihaz A]──[Cihaz B]──[Cihaz C]──[Cihaz D]
```

Her düğüm bir sonrakine kablo ile zincirleme bağlanır. PROFIBUS DP ve RS-485 tabanlı fieldbuslar bu topolojinin en yaygın temsilcisidir. RS-485 fiziksel katmanı, birden fazla cihazın aynı hatta bağlanmasını mümkün kılar; hat iki ucunda da sonlandırma direnci (termination resistor) zorunludur.

**Teknik özellikler:**
- Kablo maliyeti düşük — her cihaz için ayrı merkezi kablo çekilmez
- Tek bir kablo kopması veya tek bir arızalı cihaz hattın geri kalanını kesebilir (yüksek hassasiyet noktası)
- Industrial Ethernet'te "daisy chain" olarak da anılır; her cihazın iki Ethernet portu vardır (giriş + çıkış)
- EtherCAT bu yapıyı mantıksal olarak çok verimli kullanır: çerçeve düğümlerden geçerken her slave verisi çerçeve üzerinde okur/yazar ("processing on the fly")

#### 2. Yıldız Topoloji (Star)

```
        [PLC 1]
           |
[Cihaz A]──[SWITCH]──[Cihaz B]
           |
        [HMI]
```

Tüm düğümler merkezi bir switch'e (veya hub'a) bağlanır. Veriler switch üzerinden iletilir; düğümler birbirini doğrudan görmez. Modern endüstriyel Ethernet'in en yaygın fiziksel topolojisidir.

**Teknik özellikler:**
- Switch arızası tüm ağı keser — switch, tek arıza noktasıdır (Single Point of Failure)
- Yeni düğüm eklemek çok kolaydır; mevcut bağlantılar etkilenmez
- Sorun teşhisi basittir: her port bağımsız izlenebilir
- Yönetimli (managed) switch ile VLAN, QoS, port güvenliği, SNMP kolayca uygulanabilir
- Yedeklilik için switch çiftleme (dual homing) veya halka topolojiye geçiş gerekir

#### 3. Halka Topoloji (Ring)

```
[PLC 1]──[Switch A]──[Switch B]──[Switch C]──[PLC 1]
                                              (geri döner)
```

Hat topolojisinin iki ucu birleştirilerek kapalı bir döngü oluşturulur. Normal çalışmada döngü engellemek için bir port bloklıdır; arıza durumunda blok kaldırılarak trafik alternatif yoldan devam eder.

**Teknik özellikler:**
- Tek bir kablo kopması veya switch arızası ağı durdurmaz — trafik ters yönden devam eder
- Yedeklilik protokolü kritik önem taşır: MRP, DLR, RSTP, HSR gibi protokoller devreye girer
- Halka boyutu arttıkça yeniden yapılandırma süresi protokole göre değişir
- Doğrusal yapıya göre biraz daha fazla kablo maliyeti gerekir (son düğümden başa dönüş)

#### 4. Ağaç Topoloji (Tree)

```
             [Omurga Switch]
            /               \
    [Switch A]           [Switch B]
    /        \            /       \
[PLC 1]  [PLC 2]     [PLC 3]   [HMI]
```

Hiyerarşik yapıdır; üst düzey düğümlerden alt dallara doğru uzanır. Geniş tesislerde omurga (backbone) switch'ler birden fazla saha switch'ini besler.

**Teknik özellikler:**
- Üst düzey switch arızası tüm alt dalları keser — hiyerarşik tek arıza noktaları oluşur
- Yönetim kolaylaşır: her dal kendi bütünlüğünde düşünülebilir
- Ağaç yapıyı halka ile birleştirerek "dairesel ağaç" (ring backbone + star branches) topolojisi gerçek projelerde en yaygın kullanılan hibrit yapıdır

---

### Halka Yedeklilik Protokolleri: MRP ve RSTP

#### MRP — Media Redundancy Protocol (IEC 62439-2)

MRP, yüksek kullanılabilirlikli endüstriyel otomasyon sistemleri için IEC 62439-2:2021 standardı kapsamında tanımlanmış halka yedeklilik protokolüdür.

**Mimari:**
- **Media Redundancy Manager (MRM)**: Halkayı izler, döngüyü önlemek için bir portunu bloklı tutar, test çerçeveleri (test frames) gönderir
- **Media Redundancy Client (MRC)**: Halkadaki diğer tüm cihazlar; test çerçevelerini ileterek halka bütünlüğünü destekler
- Arıza anında MRM bloklı portunu açar ve tüm switchlerin MAC tablolarını temizler; cihazlar yeni yolları öğrenir

**Kurtarma süreleri (Perle Systems teknik belgesi):**
- Yapılandırma seçeneğine bağlı olarak **< 10 ms, < 30 ms, < 200 ms veya < 500 ms**
- 50 düğüme kadar halkalarda tipik değer **< 200 ms**

**RSTP ile karşılaştırma (SCADA Protocols, AercoIoT):**

| Özellik | MRP (IEC 62439-2) | RSTP (IEEE 802.1w) |
|---|---|---|
| Tasarım amacı | Endüstriyel otomasyon | Genel IT Ethernet |
| Tipik kurtarma | < 200 ms | 1–3 saniye |
| En kötü durum | < 500 ms (yapılandırılabilir) | > 2 saniye, bazen 5+ saniye |
| Halka boyutu | 50 düğüme kadar optimize | Topoloji bağımlı |
| Determinizm | Yüksek (öngörülebilir) | Düşük (yeniden hesaplama) |
| PROFINET uyumu | Yerli destek | Uyumsuz (IRT için kullanılamaz) |

> RSTP 5 saniye algılama+onarım süresiyle endüstriyel watchdog sürelerini aşabilir. MRP bu sorunu çözmek için tasarlanmıştır. (Kaynak: SCADA Protocols)

**Diğer halka protokolleri (AercoIoT):**

| Protokol | Standart | Kurtarma | Kullanım Alanı |
|---|---|---|---|
| MRP | IEC 62439-2 | < 10–200 ms | PROFINET ağları |
| DLR (Device Level Ring) | ODVA | < 3 ms | EtherNet/IP (Allen-Bradley) |
| HSR (High-Speed Redundancy) | IEC 62439-3 | ~0 ms (paket çoğaltma) | Güç şebekeleri, kritik altyapı |
| PRP (Parallel Redundancy Protocol) | IEC 62439-3 | ~0 ms (çift bağımsız ağ) | Kritik altyapı |
| RSTP | IEEE 802.1w | 1–3 saniye | Genel IT (OT için önerilmez) |

---

### Purdue / ISA-95 Katmanlı Mimari Modeli

Purdue Referans Mimarisi (PERA), 1992 yılında Theodore J. Williams liderliğinde Purdue Üniversitesi'nin Bilgisayar Entegre Üretim Konsorsiyumu tarafından geliştirilmiştir. ISA-99 (bugünkü adıyla IEC 62443) bu modeli resmi güvenlik mimarisi olarak benimsemiştir.

Model, endüstriyel sistemleri **Seviye 0'dan Seviye 5'e** kadar altı hiyerarşik katmana ayırır:

```
┌─────────────────────────────────────────────────────┐
│  SEVİYE 5: Bulut / İş Planlaması                    │  ← IT Alanı
│  ERP, iş zekası, tedarik zinciri, bulut platformlar │
├─────────────────────────────────────────────────────┤
│  SEVİYE 4: Kurumsal Ağ (Enterprise)                 │
│  ERP sunucuları, e-posta, veritabanları, IT sistemi  │
├═════════════════════════════════════════════════════╡
│  SEVİYE 3.5: Endüstriyel DMZ (iDMZ)                 │  ← OT/IT Sınırı
│  Tarih sunucusu kopyası, OPC UA proxy, atlama kutusu │
│  (Jump box), yama sunucusu, güncellleme sunucusu     │
├─────────────────────────────────────────────────────┤
│  SEVİYE 3: Üretim Yönetim Sistemleri                │  ← OT Alanı
│  MES, SCADA, data historian, toplu iş yönetimi      │
├─────────────────────────────────────────────────────┤
│  SEVİYE 2: Denetim ve Kontrol                       │
│  HMI, mühendislik istasyonları, DCS, SCADA istemci  │
├─────────────────────────────────────────────────────┤
│  SEVİYE 1: Temel Kontrol                            │
│  PLC, RTU, güvenlik kontrolcüsü (SIS), IED          │
├─────────────────────────────────────────────────────┤
│  SEVİYE 0: Fiziksel Süreç                           │
│  Sensörler, aktüatörler, motorlar, valfler, pompalar │
└─────────────────────────────────────────────────────┘
```

**ISA-95 ve Purdue İlişkisi (Check Point, Inductive Automation):**
- ISA-95 (IEC 62264), kurumsal ve kontrol sistemleri entegrasyonu için uluslararası standarttır; Purdue modeli ile aynı seviye numaralandırmasını kullanır
- ISA-99 (şimdi IEC 62443), Purdue'yu güvenlik bölgeleri (security zones) ve tüp (conduit) mimarisi için temel referans olarak almıştır

#### OT/IT Ayrımı

**OT (Operational Technology)** ve **IT (Information Technology)** farklı öncelik yapılarına sahiptir:

| Özellik | OT Ağı | IT Ağı |
|---|---|---|
| Öncelik sırası | Kullanılabilirlik (A) → Bütünlük (I) → Gizlilik (C) | Gizlilik (C) → Bütünlük (I) → Kullanılabilirlik (A) |
| Gecikme toleransı | Mikro-saniyeden milisaniyeye | Birkaç saniyeye kadar |
| Güncelleme döngüsü | Yıllar (dondurulmuş sürüm) | Haftalık/aylık |
| Yama yönetimi | Test edilmeden uygulanamaz | Standart IT politikası |
| Protokoller | PROFINET, EtherCAT, Modbus, DNP3 | TCP/IP, HTTP(S), LDAP |
| Yaşam döngüsü | 15–25 yıl | 3–5 yıl |

Seviye 3.5'teki **iDMZ**, iki dünya arasında kontrollü veri alışverişine izin verirken doğrudan erişimi engeller. Data Diode (tek yönlü ağ geçidi) gibi çözümler OT'den IT'ye veri akışını tek yönlü kılar; IT'den OT'ye komut akışına izin vermez.

---

### Hibrit Topolojiler

Gerçek endüstriyel tesislerde saf bir topoloji nadiren kullanılır. En yaygın kombinasyon:

```
[Omurga Halka — Fiber, 1 Gbps, MRP]
        |              |
[Alan Switch 1]  [Alan Switch 2]
  (Yıldız)          (Yıldız)
  /    \              /   \
[PLC1] [PLC2]    [PLC3] [HMI]
```

Bu kombinasyonla:
- **Omurga halka**: yedeklilik (MRP, < 200 ms kurtarma)
- **Alan switch yıldızları**: kolay cihaz ekleme, sade kablo yönetimi
- Ağaç yapı ile ölçeklenebilirlik korunur

## Pratikte Nasıl Kullanılır

### Adım 1: Fiziksel Ortamı Haritala

- Kaç PLC, HMI, sensör ağ geçidi, kamera ve switch bulunuyor?
- Kablo mesafeleri: 100 m sınırı (bakır 100BASE-TX) aşılıyor mu?
- Elektromanyetik gürültü (EMI) riski var mı? (kaynak, motor sürücüsü yakınlığı)
- 100 m üzeri veya yüksek EMI riski → fiber optik kablo (multimode OM3/OM4 veya singlemode)

### Adım 2: Yedeklilik Gereksinimini Belirle

- **Kesinti toleransı > 1 dakika**: Yıldız topoloji yeterli, switch yedekliliğine gerek yok
- **Kesinti toleransı < 1 dakika**: Halka topoloji + MRP zorunlu
- **Kesinti toleransı < 1 saniye / watchdog hassasiyeti**: MRP yapılandırmasını < 200 ms'ye ayarla
- **Sıfır kesinti (hareket kontrol, güvenlik sistemleri)**: HSR/PRP veya MRPD (PROFINET)

### Adım 3: Switch Tipini Seç

**Her zaman yönetimli (managed) switch kullan.** Yönetilmeyen (unmanaged) switch;
- MRP, RSTP, STP desteği sunmaz
- VLAN yapılandırmasına izin vermez
- QoS ve trafik önceliklendirme yapamaz
- SNMP ile izlenemez

PROFINET IRT için switch'in PTCP (Precision Transparent Clock Protocol) veya IEEE 1588 desteği zorunludur. Standart IT switchleri bunu desteklemez.

### Adım 4: Purdue Katmanlarını Ata

Her cihazı doğru Purdue seviyesine yerleştir. Seviyeler arası iletişim kurallarını tanımla:
- L1 ↔ L2: PROFINET/Modbus TCP (kontrol trafiği)
- L2 ↔ L3: OPC UA (veri toplama)
- L3 ↔ L4: DMZ üzerinden geçiş (her iki yönde protokol kırma)

### Adım 5: Kablo ve Düzeni Belgele

Network topoloji diyagramı, kablolamayla birlikte belgelenmeli ve güncel tutulmalıdır. Bir arıza anında diyagram olmadan sorun tespiti imkansız hale gelir.

## Örnekler

### Örnek 1: Küçük Üretim Hücresi — Yıldız

```
[PLC Siemens S7-1200]──────────────────┐
[Servo Sürücü 1]────────────────────── │
[Servo Sürücü 2]────────────────────── ├──[Yönetimli Switch, 8 port]──[HMI]
[Sensör Ağ Geçidi IO-Link Master]────── │
[Kamera]──────────────────────────────┘
```

5 cihaz, merkezi switch, yıldız topoloji. Kesinti toleransı 5 dakika → yedeklilik gerekmez.

### Örnek 2: Orta Fabrika — Halka Omurga + Yıldız Dallar

```
[Core Switch A]══════[Core Switch B]    (MRP Halka, Fiber, 1 Gbps)
      |                     |
[Alan Switch 1]       [Alan Switch 2]  (Her biri yıldız, bakır 100 Mbps)
  /    \    \            /     \
[PLC1][PLC2][HMI1]  [PLC3]   [HMI2]
```

MRP: Core Switch A = MRM (Media Redundancy Manager), Core Switch B = MRC. Kablo kopmasında < 150 ms kurtarma.

### Örnek 3: PROFIBUS DP Doğrusal Topoloji (Saha Seviyesi)

```
[PLC Master]──┬──[Slave 1 (RF430 sensör)]
              ├──[Slave 2 (G120 sürücü)]
              ├──[Slave 3 (ET 200S I/O modülü)]
              └──[Slave N]
(Her iki uçta 220 Ω sonlandırma direnci)
```

RS-485 fiziksel katmanı, 12 Mbps'te 100 m kablo uzunluğu sınırı; daha uzun mesafe için repeater gerekir.

## Sık Yapılan Hatalar

### Hata 1: Yönetilmeyen Switch ile Endüstriyel Ağ Kurmak

```
❌ Yanlış: Maliyeti düşürmek için unmanaged switch kullanmak
✅ Doğru : Her pozisyonda managed switch — IRT için PROFINET onaylı switch
```

Unmanaged switch; MRP, VLAN, QoS, SNMP, port yansıtma (mirroring) desteklemez. Sorun oluştuğunda teşhis bile mümkün değildir.

### Hata 2: RSTP'yi MRP Yerine Kullanmak

```
❌ Yanlış: Halka topolojide RSTP aktif, MRP yokken
   Sonuç : Kablo koptuğunda 1-5 saniye kesinti → PLC watchdog tetiklenir,
           üretim durur, güvenlik sistemi devreye girebilir
✅ Doğru : PROFINET ortamında MRP; EtherNet/IP ortamında DLR; kritik
           altyapıda HSR/PRP
```

### Hata 3: Purdue Katmanlarını Atlamak (L3.5 DMZ'siz Geçiş)

```
❌ Yanlış: IT ERP sunucusu → doğrudan → PLC (L1 cihazı)
   Sonuç : Bir fidye yazılımı ERP'den tüm fabrikayı kapatabilir
✅ Doğru : ERP (L4) → DMZ (L3.5) → Historian → OPC UA → SCADA (L3) →
           güvenlik duvarı → PLC (L1)
```

### Hata 4: Halka Boyutunu Aşmak

50'den fazla cihazı tek MRP halkasına bağlamak kurtarma süresini uzatır ve hata ayıklamayı zorlaştırır. Büyük tesislerde birbirine bağlı birden fazla halka (interconnected rings) kullanılmalıdır.

### Hata 5: Topoloji Belgelemesini Güncel Tutmamak

Cihaz eklendiğinde veya kablo değiştirildiğinde topoloji diyagramı güncellenmezse arıza sırasında yanlış karar alınır. Tüm değişiklikler belgelenmelidir.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Yıldız Topoloji

**Tercih et:**
- Küçük hücre uygulamaları (< 15 cihaz)
- Kesinti toleransı yüksek, basit ortamlar
- Hızlı kurulum ve kolay bakım öncelikliyse

**Tercih etme:**
- Yüksek yedeklilik gereksinimleri varsa
- Merkezi switch arızasının kabul edilemez olduğu üretim hatları

### Doğrusal (Line / Daisy Chain) Topoloji

**Tercih et:**
- Saha seviyesi (L0-L1) fieldbus uygulamaları (PROFIBUS, IO-Link)
- EtherCAT zincirleri (mantıksal halka, fiziksel doğrusal)
- Uzun, dar makine hücreleri (konveyör, hat)

**Tercih etme:**
- Yedeklilik gerektiren uygulamalar (tek kopma, tümü keser)
- Gelecekte büyüme beklenen ağlar

### Halka + MRP

**Tercih et:**
- Orta ve büyük ölçekli üretim tesisleri
- PROFINET ortamları
- Kesinti toleransı < 1 dakika olan hatlar

**Tercih etme:**
- Küçük hücreler (maliyeti haklı kılmaz)
- EtherCAT saf doğrusal zincirleri (EtherCAT kendi yedeklilik mekanizmasına sahiptir)

### Ağaç Topoloji

**Tercih et:**
- Çok katlı fabrika binaları, geniş tesisler
- Omurga halka + alan yıldızları hibridine alt yapı

**Tercih etme:**
- Üst katman switch'e bağımlılık kabul edilemediğinde (çift uplink ile destekle)

## Gerçek Proje Notları

**Not 1 — MRP Kurtarma Süresi Tahminlerinde Dikkat**
Bir otomobil parçası fabrikasında 32 düğümlü MRP halkası kuruldu. Belgelerde < 200 ms garanti ediliyordu; ancak switch'lerin MRP desteği eski firmware ile % 12 daha uzun kurtarma süresi veriyordu. Çözüm: tüm halka switch'leri üretici tarafından MRP için doğrulanmış firmware ile güncellendi. Sonuç: 143 ms ortalama kurtarma. Ders: MRP kurtarma süresi garanti edilmek isteniyorsa tüm switch'ler aynı üreticinin onaylı cihazları olmalıdır; karışık üretici ortamında uyumluluk testleri zorunludur.

**Not 2 — "Switch Azaltma" Baskısı**
Maliyet kısıtlaması nedeniyle bir tesiste ağaç topoloji oluşturuldu; birden fazla PLC, tek alan switch'ine bağlandı ve bu switch de doğrudan merkezi switch'e bağlandı. Alan switch'i arızasında o hücredeki üretim tamamen durdu. Sonraki tasarımda her kritik alan switch'i için çift uplink eklendi. Maliyet farkı, bir saatlik üretim kaybının çok altındaydı.

**Not 3 — Purdue Modeli "Sanal" Uygulaması**
Bazı tesislerde fiziksel topoloji basit (yıldız), ancak Purdue katmanları VLAN ile sanal olarak uygulanmaktadır. Bu geçerli bir yaklaşımdır; ancak VLAN'lar arası yönlendirmenin bir Layer-3 switch veya güvenlik duvarı üzerinden yapılması zorunludur; aksi hâlde segmentasyon yalnızca görünüşte kalır.

**Not 4 — EtherCAT Topoloji Esnekliği**
EtherCAT teknik olarak doğrusal, yıldız, ağaç ve halka kombinasyonlarını destekler (Wikipedia / ethercat.org). Bu esneklik EtherCAT'ın güçlü yönlerinden biridir; ancak çoğu saha uygulamasında tercih edilen yapı mantıksal halkaya göre çalışan fiziksel doğrusal dizilimdir.

## İlgili Konular

```
knowledge/networking/
├── 02_security.md           → Purdue model güvenlik detayları, VLAN, DMZ
├── 03_performance.md        → MRP kurtarma süresi gecikme bütçesi ilişkisi
└── _synthesis.md            → Topoloji + güvenlik + performans sentezi

knowledge/protocols/
├── profinet/                → MRP, PTCP, RT/IRT topoloji gereksinimleri
├── ethercat/                → Doğrusal topoloji ve dağıtık saat
└── modbus/                  → Bus topoloji ve doğrusal PROFIBUS mimarisi

knowledge/standards/
├── 02_iec62443              → Purdue model güvenlik bölge mimarisi
└── iec61784/                → Fieldbus ve RT Ethernet topoloji sınıfları

knowledge/hardware/
└── switches/                → Managed vs unmanaged, MRP desteği, PROFINET onayı
```
