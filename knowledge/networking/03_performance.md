---
KONU        : Endüstriyel Ağ Gecikme ve Güvenilirlik
KATEGORİ    : networking
ALT_KATEGORI: networking
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "https://us.profinet.com/profinet-rt-vs-irt/"
    başlık: "A Complete Comparison: PROFINET RT vs IRT — PI North America"
    güvenilirlik: resmi
  - url: "https://us.profinet.com/is-profinet-deterministic/"
    başlık: "Is PROFINET Deterministic? — PI North America"
    güvenilirlik: resmi
  - url: "https://us.profinet.com/profinet-irt-isochronous-real-time/"
    başlık: "PROFINET IRT — Isochronous Real Time — PI North America"
    güvenilirlik: resmi
  - url: "https://profinetuniversity.com/profinet-basics/isochronous-real-time-irt-communication/"
    başlık: "Isochronous Real-Time (IRT) Communication — PROFINET University"
    güvenilirlik: resmi
  - url: "https://www.ethercat.org/en/technology.html"
    başlık: "EtherCAT Technology — EtherCAT Technology Group (resmi)"
    güvenilirlik: resmi
  - url: "https://www.zigron.com/blog/tsn-fundamentals-802-1as-802-1qbv"
    başlık: "TSN Fundamentals: 802.1AS and 802.1Qbv — Zigron"
    güvenilirlik: topluluk
  - url: "https://maisvch.com/blog/tsn-time-sensitive-networking-industrial-automation/"
    başlık: "What Is TSN (Time-Sensitive Networking)? Industrial Automation Guide — MaisVCH"
    güvenilirlik: topluluk
  - url: "https://maplesystems.com/quality-of-service-qos-in-industrial-networks/"
    başlık: "QoS in Industrial Networks — Maple Systems"
    güvenilirlik: topluluk
  - url: "https://www.rtautomation.com/rtas-blog/frame-prioritization-within-ethernet-ip-and-profinet/"
    başlık: "Frame Prioritization Within EtherNet/IP and PROFINET — Real Time Automation"
    güvenilirlik: topluluk
  - url: "https://scadaprotocols.com/prp-vs-hsr-iec-62439-3/"
    başlık: "PRP vs HSR Explained: IEC 62439-3 Complete Guide — SCADA Protocols"
    güvenilirlik: topluluk
  - url: "https://icnavigator.com/technology/industrial-ethernet-tsn/ring-redundancy-mrp-hsr-prp/"
    başlık: "Ring Redundancy (MRP/HSR/PRP) for Industrial Ethernet — ICNavigator"
    güvenilirlik: topluluk
  - url: "https://maplesystems.com/storm-control-in-industrial-networks/"
    başlık: "Storm Control in Industrial Networks — Maple Systems"
    güvenilirlik: topluluk
  - url: "https://en.wikipedia.org/wiki/Parallel_Redundancy_Protocol"
    başlık: "Parallel Redundancy Protocol — Wikipedia"
    güvenilirlik: topluluk
  - url: "https://en.wikipedia.org/wiki/High-availability_Seamless_Redundancy"
    başlık: "High-availability Seamless Redundancy — Wikipedia"
    güvenilirlik: topluluk
  - url: "https://infosys.beckhoff.com/content/1033/ethercatsystem/2469118347.html"
    başlık: "EtherCAT Distributed Clocks — Beckhoff Automation"
    güvenilirlik: resmi
  - url: "https://community.cisco.com/t5/internet-of-things-knowledge-base/profinet-rt-packets-not-supported-on-cisco-vlan-based-switches/ta-p/4971229"
    başlık: "PROFINET RT Packets ve 802.1p Priority — Cisco Community"
    güvenilirlik: topluluk
  - url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11415645/"
    başlık: "Data Losses and Synchronization According to Delay in PLC-Based Systems — PMC/MDPI"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/networking/01_topologies.md"
    ilişki: gerektirir
  - konu: "knowledge/networking/02_security.md"
    ilişki: tamamlar
  - konu: "knowledge/hardware/industrial-pc/03_performance_tuning"
    ilişki: tamamlar
  - konu: "knowledge/codesys/task-structure/02_cycle_time"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "OSI modeli (Katman 1-3) ve Ethernet çerçeve yapısı"
  - "VLAN ve 802.1Q etiketleme temel bilgisi"
  - "knowledge/networking/01_topologies.md (MRP/PRP/HSR kavramları)"
  - "PLC döngü zamanı (scan time) kavramı"
ÇELİŞKİLER :
  - kaynak: "PROFINET University ve PI North America"
    konu: "PROFINET IRT minimum cycle time değeri"
    çözüm: >
      PI North America'nın resmi sayfası 250 µs'yi standart minimum değer
      olarak belirtirken, PROFINET v2.3 uzantılarıyla 31.25 µs'ye kadar
      inilebildiğini belirtmektedir. PROFINET University de aynı iki değeri
      doğrulamaktadır. 31.25 µs, yalnızca özel donanım ve Conformance Class C
      ile ulaşılabilen üst sınırdır; genel uygulama için 250 µs–1 ms referans
      alınmalıdır.
  - kaynak: "Çeşitli topluluk kaynakları vs IEC 62439-3"
    konu: "HSR/PRP'nin 'sıfır gecikmeli' olduğu iddiası"
    çözüm: >
      HSR ve PRP'nin 'sıfır kurtarma süresi' ifadesi, bir arıza durumunda
      çerçeve kaybı yaşanmaması anlamına gelir; yoksa ek gecikme (jitter)
      olmadığı anlamına gelmez. Çerçeve çoğaltma ve atma mekanizmaları, özellikle
      HSR halkasında yol asimetrisi nedeniyle jitter artışına yol açabilir.
      Bu nedenle sıfır kayıp ve sıfır jitter birbirinden farklı kavramlardır.
---

## Özün Ne

Endüstriyel ağ performansı, bir PLC'nin veya hareket kontrolörünün sahadan aldığı veriyi ne kadar hızlı, ne kadar güvenilir ve ne kadar öngörülebilir biçimde alıp gönderdiğini tanımlar. Bu alanda iki temel boyut vardır: **gecikme bütçesi** (latency, jitter, determinizm) ve **güvenilirlik bütçesi** (redundancy, uptime, storm önleme).

Standart Ethernet, "en iyi çaba" (best-effort) modunda çalışır: çerçeveler iletilmeye çalışılır, ancak süre veya kaybsızlık garanti edilmez. Endüstriyel otomasyon bu modeli kabul edemez; bir servo sürücünün komut çerçevesini 100 µs ± 1 µs tutarlılığıyla almaması halinde eksen senkronizasyonu bozulur, üretim hatası veya mekanik hasar oluşur. Bu nedenle PROFINET IRT, EtherCAT, TSN ve QoS mekanizmaları standart Ethernet'in üzerine kesin zamanlama ve önceliklendirme garantileri eklemek için tasarlanmıştır.

Güvenilirlik boyutunda ise tek bir kablo kopmasının veya switch arızasının kabul edilemez olduğu ortamlar için MRP, PRP ve HSR protokolleri ayrı kurtarma/süreklilik stratejileri sunar. Bu belge, bu iki boyutu nicel değerler ve pratik konfigürasyon rehberiyle kapsamlı biçimde ele almaktadır.

## Nasıl Çalışır

### 1. Temel Kavramlar: Latency, Jitter, Determinizm

**Latency (Gecikme):** Bir çerçevenin gönderici uçtan alıcı uca ulaşma süresidir. Endüstriyel bağlamda "tek yönlü gecikme" (one-way latency) veya tam döngü gecikmesi (round-trip latency) olarak ölçülür. Gecikme; kablo yayılım gecikmesi, switch işleme gecikmesi (store-and-forward vs cut-through) ve yığın yazılımı gecikmesinin toplamıdır.

**Jitter:** Art arda gelen çerçeveler arasındaki gecikme farkının değişkenliğidir. PLC çevrim zamanının tutarlı olabilmesi için jitter'ın çevrim zamanının küçük bir kesri olması gerekir. Örneğin 1 ms çevrim zamanı için ±5 µs jitter kabul edilebilirken ±200 µs kabul edilemez.

**Determinizm:** Ağın her koşulda (yüksek trafik, yayın fırtınası, switch yükü) garanti edilmiş gecikme üst sınırına sahip olmasıdır. Standart Ethernet'te bu garanti yoktur; endüstriyel protokoller determinizmi donanım veya protokol mekanizmalarıyla sağlar.

**Bandwidth (Bant genişliği):** Birim zamanda aktarılabilen maksimum veri miktarıdır. Endüstriyel ağlarda 100 Mbps Fast Ethernet veya 1 Gbps Gigabit Ethernet yaygındır. Bant genişliği yeterli olsa bile determinizm sağlanmadan yüksek anlık trafik gecikmeye neden olabilir.

---

### 2. PROFINET RT ve IRT Zamanlama Sınıfları

PROFINET, aynı fiziksel ağ üzerinde üç iletişim kanalını eşzamanlı çalıştırır (PI North America resmi kaynakları):

| Sınıf | Tam Ad | Çevrim Süresi | Jitter | Kullanım |
|---|---|---|---|---|
| NRT | Non-Real-Time | Yüzlerce ms | Yüksek | TCP/IP, tanılama, web arayüzü |
| RT | Real-Time | 250 µs – 512 ms | ≤ 100 µs | Standart I/O, %95+ uygulama |
| IRT | Isochronous Real-Time | 31.25 µs – 250 µs | ≤ 1 µs | Servo, baskı makinesi, kesim hattı |

**PROFINET RT Mekanizması:**
RT çerçeveleri, TCP/IP katmanlarını atlayarak doğrudan Ethernet Katman 2 üzerinden iletilir. EtherType değeri `0x8892` olarak sabitlenmiştir. Bu sayede TCP/IP yığınının getirdiği ek gecikme ortadan kalkar. VLAN etiketi içinde `802.1p Priority Code Point (PCP) = 6` olarak işaretlenir; böylece switch'ler RT trafiğini diğer trafiğin önüne alır.

**PROFINET IRT Mekanizması:**
IRT, çevrim zamanını üç aşamaya böler:

```
|<────── IRT (Kırmızı) ──────>|<── RT (Turuncu) ──>|<── NRT (Yeşil) ──>|
     Sadece IRT verisi           Zaman-kritik RT      Serbest Ethernet
     (ayrılmış bant)              verisi               (TCP/IP, SNMP vb.)
```

- **Kırmızı faz:** Yalnızca IRT verisi için ayrılmış süre dilimi. Diğer tüm trafik engellenir. Örneğin toplam bant genişliğinin %25'i IRT'ye ayrılabilir; kalan %75 RT ve NRT için kullanılır.
- **Turuncu faz:** Zaman-kritik RT mesajları bu fazda iletilir.
- **Yeşil faz:** Standart Ethernet trafiği (TCP/IP, HTTP tanılama, SNMP) geçebilir. Minimum 125 µs uzunluğunda olmalıdır; bu nedenle 250 µs altındaki çevrim süreleri standart Ethernet çerçevesi boyutlarıyla doğrudan uyumsuz olup özel donanım gerektirir.

**IRT Senkronizasyon Protokolü (PTCP):**
PROFINET IRT, IEEE 1588v2 PTP (Precision Time Protocol) temelinde geliştirilen **PTCP (Precision Transparent Clock Protocol)** ile çalışır. PTCP; switch'lerdeki gecikmeleri ve kablo yayılım gecikmelerini nanosaniye hassasiyetiyle ölçerek tüm cihazları ortak bir saate senkronize eder. Sonuç: ağdaki tüm IRT cihazları arasında **≤ 1 µs** saat sapması.

**IRT Donanım Gereksinimleri:**
- Ağdaki tüm denetleyiciler, cihazlar ve switch'ler **PROFINET Conformance Class C** sertifikalı olmalıdır.
- Switch'ler **cut-through** (depolama olmadan iletim) modunda çalışmalıdır; store-and-forward switch'ler IRT için uygun değildir.
- Standart IT switch'leri IRT ağlarında kullanılamaz.

---

### 3. EtherCAT Zamanlama Mimarisi

EtherCAT, endüstriyel Ethernet protokolleri arasında en düşük jitter ve en kısa çevrim sürelerini sunan protokoldür (EtherCAT Technology Group resmi belgesi):

| Parametre | Değer |
|---|---|
| Minimum çevrim süresi | ≤ 100 µs (tipik uygulamalar için 125 µs – 1 ms) |
| Senkronizasyon jitteri | < 1 µs (dağıtık saat mekanizması ile) |
| Bant genişliği verimliliği | > %90 (full-duplex 100 Mbps üzerinde fiili veri oranı) |
| Maksimum düğüm sayısı | 65.535 cihaz/segment |
| Düğümler arası mesafe | 100 m (bakır 100BASE-TX), fiber ile sınırsız |
| Kablo kopması algılama | < 15 µs (tek bir iletişim çevrimi içinde) |

**EtherCAT'ın "Processing on the Fly" İlkesi:**
Standart Ethernet'te her cihaz çerçeveyi tamamen alır, işler, sonra gönderir (store-and-forward). EtherCAT'ta ise her slave, çerçeve hattı üzerinden geçerken kendi veri alanını okur ve yazar; çerçeve bitmeden iletilmeye devam eder. Bu mekanizma, büyük ağlarda bile gecikmenin birikmemesini sağlar.

**EtherCAT Dağıtık Saat (Distributed Clock) Mekanizması (Beckhoff):**
İlk slave referans saat kaynağı olarak seçilir. Master bir senkronizasyon çerçevesi gönderir; her slave çerçevenin geçiş zamanını kaydeder ve kendi yerel saatini buna göre düzeltir. Sonuç olarak tüm ağdaki saatler, ek donanım gerekmeksizin IEEE 1588 PTP ile eşdeğer < 1 µs hassasiyete ulaşır.

---

### 4. TSN — Time-Sensitive Networking (IEEE 802.1)

TSN, standart Ethernet altyapısı üzerinde deterministik iletişim garantisi sağlamak için IEEE 802.1 çalışma grubunun geliştirdiği bir standartlar bütünüdür. Endüstriyel otomasyon alanında PROFINET over TSN, OPC UA PubSub over TSN ve EtherNet/IP with CIP Sync over TSN bu altyapıyı kullanır.

#### TSN Alt Standartları

| Standart | İşlev | Temel Performans |
|---|---|---|
| **IEEE 802.1AS** (gPTP) | Ağ genelinde ortak zaman referansı | < 1 µs senkronizasyon hassasiyeti (TSN domain içinde) |
| **IEEE 802.1Qbv** | Zaman-farkında kuyruklama (Time-Aware Shaper, TAS) | < 1 ms gecikme garantisi (yapılandırmaya bağlı) |
| **IEEE 802.1Qbu / 802.3br** | Çerçeve önleme (Frame Preemption) | Alt-milisaniye çevrimler için yüksek öncelikli çerçeveler düşük öncelikli çerçeveleri kesebilir |
| **IEEE 802.1CB** | Çerçeve çoğaltma ve eleme (Frame Replication and Elimination) | Anlık yedeklilik geçişi (RSTP'nin 50 ms'ye karşın efektif olarak sıfır) |
| **IEEE 802.1Qci** | Giriş portunda per-akış filtreleme ve policing | Planlı trafiği kötü kaynaklı trafikten korur |
| **IEEE 802.1Qcc** | Bant genişliği rezervasyonu ve yol planlaması | Garantilenemeyen akışları kabul etmez |
| **IEC/IEEE 60802** | Endüstriyel otomasyon için TSN profili | PROFINET/EtherNet/IP entegrasyonu için standart konfigürasyon |

**IEEE 802.1Qbv — Kapı Kontrol Listesi (Gate Control List, GCL):**
Her switch portu üzerinde 8 öncelik kuyruğu bulunur. GCL, bu kuyruğların kapılarının ne zaman açık ne zaman kapalı olacağını belirleyen ve periyodik olarak tekrarlayan zaman çizelgesidir. Örneğin 1 ms çevrim içinde:

```
0 µs      250 µs      500 µs     1000 µs
|--- IRT ---|--- NRT/RT ---|--- RT ---|  (tekrar)
  (Kapı 7)   (Kapılar 0-5)  (Kapı 6)
```

**Koruma bandı (guard band):** Kapı kapanmadan hemen önce, mevcut düşük öncelikli çerçevenin iletilmesini engellemek için küçük bir zaman penceresi bırakılır. Koruma bandı eksik yapılandırılırsa yüksek ve düşük öncelikli çerçeveler çakışarak deterministik garanti bozulur.

**Karşılaştırma: Standart Ethernet vs TSN**

| Parametre | Standart Ethernet | TSN (802.1Qbv) |
|---|---|---|
| Gecikme garantisi | Yok | Yapılandırılabilir (< 1 ms) |
| Jitter (yük altında) | 10–100 ms | < 1 µs (802.1AS ile) |
| Zaman senkronizasyonu | NTP (~1–10 ms) | IEEE 802.1AS (< 1 µs) |
| Protokol birlikteliği | Her protokol bağımsız ağ ister | IT ve OT trafiği aynı ağda |

---

### 5. QoS ve CoS: 802.1p ve DSCP

**QoS (Quality of Service)** genel bir terimdir; CoS (Class of Service) ise QoS'un Katman 2 Ethernet üzerindeki uygulamasına özgü ifadedir.

**IEEE 802.1p / CoS (Katman 2):**
VLAN etiketi (802.1Q) içindeki 3 bitlik **Priority Code Point (PCP)** alanı, 0–7 arasında 8 öncelik seviyesi tanımlar:

| PCP Değeri | Trafik Türü | Endüstriyel Karşılık |
|---|---|---|
| 7 | Network Control | STP, RSTP BPDU |
| 6 | Internetwork Control | **PROFINET RT/IRT siklik veri** |
| 5 | Critical Applications | Zaman kritik kontrol verisi |
| 4 | Video | HMI video akışı |
| 3 | Call Signaling | HMI iletişimi |
| 2 | Excellent Effort | SCADA sorgu-yanıt |
| 1 | Background | Yedek yazılım, yama |
| 0 | Best Effort (varsayılan) | Standart IT trafiği |

PROFINET RT/IRT çerçeveleri `PCP = 6` olarak işaretlenir (Cisco Community ve rtautomation.com). Bu, VLAN ID'sinden bağımsızdır; PROFINET genellikle VLAN ID = 0 (öncelik etiketi, VLAN segmentasyonu yok) ile `PCP = 6` kullanır.

**DSCP (Differentiated Services Code Point, Katman 3):**
IPv4/IPv6 başlığındaki 6 bitlik DSCP alanı, 64 farklı servis sınıfı tanımlar. EtherNet/IP, PROFINET'in aksine Katman 3 (UDP/IP üzerinden) çalıştığından DSCP kullanır; PROFINET ise doğrudan Katman 2 802.1p kullanır.

**Switch Kuyruğu Haritalama Örneği (Maple Systems):**

```
CoS 6–7  →  Kuyruk 4 (En yüksek öncelik — RT/IRT kontrol trafiği)
CoS 4–5  →  Kuyruk 3 (HMI trafiği)
CoS 2–3  →  Kuyruk 2 (SCADA sorgu/yanıt)
CoS 0–1  →  Kuyruk 1 (Arka plan — yedek, güncellemeler)
```

**Planlama Algoritmaları:**
- **Strict Priority (SP):** Her zaman en yüksek öncelikli kuyruğu öne alır. RT trafiği için uygundur; ancak düşük öncelikli trafik hiçbir zaman iletilemeyebilir (açlık/starvation riski).
- **Weighted Round Robin (WRR):** Kuyruklara ağırlıklı orantısal bant genişliği paylaşımı yapar; starvation riskini azaltır.
- Karma yaklaşım: Kuyruk 4 için SP, kuyruğa 1–3 için WRR.

---

### 6. Çevrim Zamanı ile Ağ Gecikmesi İlişkisi

PLC kontrol döngüsündeki toplam gecikme, birden fazla kaynaktan beslenir:

```
Toplam Gecikme = T_scan + T_network + T_fieldbus + T_actuator_response
```

- **T_scan:** PLC'nin bir program taraması tamamlaması için geçen süre (tipik: 1–20 ms)
- **T_network:** Ethernet ağındaki yayılım + switch gecikmesi (RT: < 1 ms, IRT: < 50 µs)
- **T_fieldbus:** Saha veri yolunun (EtherCAT, PROFIBUS) çevrim gecikmesi
- **T_actuator_response:** Aktüatörün komutu işleme süresi

**En kötü durum gecikmesi formülü:**
Bir giriş sinyalinin PLC çıkışına yansıması için en kötü durum: `2 × T_scan + T_network`. Bu, girişin tarama döngüsünün tam sonunda gelmiş olabileceğini (bir sonraki taramayı bekleme) ve çıkışın işlenmesinin de bir sonraki döngüyü beklediğini gösterir.

**Gerçek Zamanlılık Sınıfları (IEC 61784 temelli genel sınıflandırma):**

| Sınıf | Çevrim Süresi | Tipik Uygulama |
|---|---|---|
| RT Sınıf A | < 100 ms | Proses kontrolü, SCADA polling |
| RT Sınıf B | < 10 ms | Standart PLC I/O, PROFINET RT |
| RT Sınıf C | < 1 ms | Servo senkronizasyonu, PROFINET IRT, EtherCAT |

**Pratik Kural:** Ağ gecikmesi (T_network), PLC çevrim zamanının **%10'undan az** olmalıdır. 1 ms çevrim zamanında maksimum ağ gecikmesi 100 µs olmalıdır; bu PROFINET IRT veya EtherCAT gerektirir.

---

### 7. Yedeklilik: MRP, PRP, HSR Karşılaştırması

Bkz. `knowledge/networking/01_topologies.md` — protokol mimarileri orada kapsamlı biçimde ele alınmıştır. Aşağıda performans boyutu öne çıkarılmaktadır.

#### Yedeklilik Stratejileri Matrisi

| Protokol | Standart | Strateji | Kurtarma Süresi | Bant Genişliği Ek Yükü | Topoloji |
|---|---|---|---|---|---|
| **MRP** | IEC 62439-2 | Hızlı geçiş (ms) | < 10 ms (≤14 düğüm), < 200 ms (≤50 düğüm) | Minimal (yalnızca test çerçeveleri) | Halka |
| **PRP** | IEC 62439-3 | Sıfır kayıp (çift LAN) | **0 ms** (çerçeve kaybı yok) | **×2** (her çerçeve iki ağda da iletilir) | İkili paralel ağ |
| **HSR** | IEC 62439-3 | Sıfır kayıp (halka) | **0 ms** (çerçeve kaybı yok) | **×2** (halka boyunca iki yönde çoğaltma) | Halka |
| **DLR** | ODVA | Hızlı geçiş | < 3 ms | Minimal | Halka (EtherNet/IP) |
| **RSTP** | IEEE 802.1w | Yavaş geçiş | 1–5 saniye | Minimal | Herhangi |

**MRP Kurtarma Aşamaları (ICNavigator):**
1. **Algılama (Detection):** MRM, test çerçevelerinin kaybolduğunu tespit eder
2. **Kurtarma (Recovery):** Bloklu port açılır, MAC tabloları temizlenir
3. **Kararlılık (Stable Forwarding):** Yeni yol üzerinden trafik akışı doğrulanır

**PRP Mimarisi — Çift LAN (SCADA Protocols / Wikipedia):**
Her PRP düğümü (DAN — Doubly Attached Node) iki bağımsız ağa (LAN A ve LAN B) aynı çerçeveyi eşzamanlı gönderir. Alıcı, önce gelen çerçeveyi işler, ikincisini atar. LAN A veya LAN B'nin herhangi biri devre dışı kalsa bile hiç çerçeve kaybolmaz.

```
[DAN Gönderici] ──LAN A──> [DAN Alıcı] (ilkini al, ikinciyi at)
                ──LAN B──>
```

**HSR Mimarisi — Çift Yönlü Halka (Wikipedia / SCADA Protocols):**
Her HSR düğümü iki porta sahiptir; her gönderimde iki kopya, halkada ters yönlerde dolaşır. Alıcı kendi adresine gelen ilk kopyayı işler, ikincisini atar.

**Önemli Not — Sıfır Kayıp ≠ Sıfır Jitter:**
HSR ve PRP'de çerçeve çoğaltma ve atma mekanizması, özellikle halka yol asimetrisi durumunda jitter artışına yol açabilir. Sıfır kayıp garantisi, anlık gecikme değişkenliğinin (jitter) sıfır olduğu anlamına gelmez (ICNavigator teknik karşılaştırması).

---

### 8. Yayın Fırtınası (Broadcast Storm) Önleme

Broadcast storm, bir veya birden fazla cihazın aşırı miktarda yayın (broadcast) veya çoklu yayın (multicast) çerçevesi göndermesi sonucu ağın kullanılamaz hale gelmesidir. Endüstriyel ortamda bu durum PLC'lerin I/O güncellemelerini alamamasına, üretim durmasına ve güvenlik sistemlerinin devreye girmesine yol açar.

**Yaygın Nedenler (Maple Systems):**
- Arızalı veya yanlış yapılandırılmış cihazın aralıksız yayın göndermesi
- Unmanaged switch veya yanlış kablolama nedeniyle oluşan ağ döngüleri (loop)
- PROFINET ve EtherNet/IP gibi protokollerin keşif (discovery) çerçeveleri
- ARP ve BACnet protokollerinin inherent yayın kullanımı

**Önleme Mekanizmaları:**

**Storm Control (Yük Eşiği Denetimi):**
Switch her portun gelen yayın/multicast/bilinmeyen-unicast trafiğini sürekli izler. Trafik yapılandırılmış eşiği aşarsa switch aşan çerçeveleri düşürür, portu kapatır veya SNMP alarmı üretir. Endüstriyel ağlar için önerilen başlangıç eşiği: **%1–5 port bant genişliği** (Maple Systems). Baseline ölçümü yapıldıktan sonra eşik daraltılabilir.

**BPDU Guard:**
STP BPDU çerçevesi alan her erişim portunu hemen `err-disable` durumuna alır. Ağa yanlışlıkla bağlanan bir STP'li switch'in döngü oluşturmasını engeller.

**IGMP Snooping:**
Switch, multicast grup üyeliklerini öğrenerek multicast çerçeveleri yalnızca o gruba abone olan portlara iletir. PROFINET ve EtherNet/IP'nin multicast keşif trafiğini sadece ilgili cihazlara yönlendirerek ağ yükünü azaltır.

**MRP / STP Entegrasyonu:**
Storm control tek başına döngüleri çözmez; MRP veya RSTP ile birlikte kullanılmalıdır. Döngüyü oluşturan kök neden giderilmeden yalnızca storm control uygulamak geçici bir önlemdir.

## Pratikte Nasıl Kullanılır

### PROFINET RT/IRT Yapılandırma Adımları

1. **Uygulama gereksinimine karar ver:** Servo senkronizasyonu → IRT. Standart I/O → RT. Tanılama → NRT.
2. **Switch seç:** IRT için Conformance Class C onaylı, cut-through destekli switch zorunludur. Siemens SCALANCE X veya benzeri üretici onaylı cihazlar tercih edilir.
3. **STEP 7 / TIA Portal'da IRT aktif et:** "IO Controller" → "Communication" → "RT Class" = IRT seç. Sync domain tanımla.
4. **IRT bant genişliği payını ayarla:** Ağ yüküne göre %15–25 IRT ayrımı tipik başlangıç değeridir. Şebekedeki NRT trafiği yoğunsa yeşil faz en az 125 µs kalmalıdır.
5. **PTCP senkronizasyonunu doğrula:** STEP 7/TIA Portal'da "Isochronous Mode" etkin cihazlarda saat sapmasını izle; 1 µs altında tutulabiliyorsa yapılandırma doğrudur.

### EtherCAT Çevrim Süresi Optimizasyonu

1. **Master döngü görevini real-time task'a al:** TwinCAT'ta `Task Priority = 0` ve `Cycle Time = 500 µs` (veya uygulama gerektirdiği değer).
2. **Distributed Clock etkinleştir:** Her slave için `DC Sync` aktif olmalı; referans slave olarak halkaya en yakın slave seçilmeli.
3. **Frame boyutunu minimize et:** PDO mapping'te yalnızca gerekli process data dahil edilmeli; gereksiz status byte'ları çıkarılmalı.
4. **EtherCAT kablo uzunluğunu hesapla:** 100 m/segment × propagation delay ≈ 0.5 µs; 100 köle × işlem gecikmesi ≈ 1–2 µs; toplam çerçeve dolaşım süresi çevrim zamanının altında kalmalıdır.

### QoS / CoS Yapılandırma Adımları

```
# Tipik managed switch QoS yapılandırma akışı (kavramsal)
1. VLAN oluştur veya mevcut VLAN'ı tanımla
2. PROFINET portlarında "trust CoS" etkin et
3. CoS 6-7 → Kuyruk 4 (Strict Priority)
4. CoS 4-5 → Kuyruk 3 (WRR ağırlık 40)
5. CoS 2-3 → Kuyruk 2 (WRR ağırlık 30)
6. CoS 0-1 → Kuyruk 1 (WRR ağırlık 30)
7. Storm control: broadcast = %2, multicast = %3
8. BPDU guard: tüm erişim portlarında etkin
9. IGMP snooping: PROFINET/EtherNet/IP multicast için etkin
```

### MRP Yapılandırması (PROFINET)

1. Halkadaki switch'lerden birini **MRM (Media Redundancy Manager)** ata; diğerleri otomatik MRC (Client) olur.
2. MRM yapılandırmasında kurtarma süresi hedefi seç: `< 200 ms` (50 düğüme kadar), `< 30 ms` (25 düğüme kadar), `< 10 ms` (14 düğüme kadar).
3. PROFINET denetleyicisinde (PLC) MRP domain adını ve ring port ayarlarını yapılandır.
4. Test: bir halkayı geçici olarak kes, PLC'nin I/O iletişiminin watchdog'u tetiklemeden devam ettiğini doğrula.

### PRP / HSR Seçim ve Yapılandırma

- **PRP tercih et:** Güç şebekeleri, altyapı kontrol sistemi, sıfır çerçeve kaybı zorunluysa ve iki bağımsız fiziksel ağ kurulabiliyorsa.
- **HSR tercih et:** Halka topoloji daha ucuzsa ve bay düzeyinde (process bus) dağıtık cihazlar varsa. Küçük–orta halka boyutu (16–32 düğüm önerilir).
- **RedBox kullan:** PRP ve HSR ağları arasında veya PRP/HSR ile standart Ethernet arasında bağlantı için RedBox (Redundancy Box) gereklidir.

## Örnekler

### Örnek 1: PROFINET IRT ile Çok Eksenli Servo Sistemi

```
Senaryo: 8 eksenli baskı makinesi, tüm eksenler senkron hareket etmeli
Gereksinim: Eksenler arası faz farkı < 5 µs

Çözüm:
  - PROFINET IRT, çevrim süresi = 500 µs, jitter = 1 µs
  - Tüm servo sürücüler Conformance Class C
  - Sync domain: PLC = sync master, tüm sürücüler sync slave
  - Switch: Siemens SCALANCE X208 (IRT onaylı, cut-through)
  - IRT bant genişliği: toplam %20 ayrıldı
  - NRT trafiği (tanılama HTTP): yeşil fazda ≥ 200 µs pencere
  
Sonuç: Eksenler arası gerçek ölçüm sapması < 2 µs
```

### Örnek 2: EtherCAT Robot Hücresi

```
Senaryo: 6 eksenli robot + konveyör senkronizasyonu, 32 slave
Gereksinim: Çevrim süresi ≤ 1 ms, jitter ≤ 1 µs

Hesaplama:
  - 32 slave × ~1 µs işlem gecikmesi = ~32 µs propagation
  - Çerçeve boyutu (32 slave PDO) ≈ 1200 byte
  - Aktarım süresi @100 Mbps: 1200 × 8 / 100.000.000 = 96 µs
  - Toplam döngü süresi ≈ 128 µs → 250 µs çevrim yeterli
  - Distributed Clock aktif, jitter < 0.5 µs ölçüldü

Sonuç: Seçilen 500 µs çevrim süresi %2 network kullanımı ile çalışıyor
```

### Örnek 3: QoS Yapılandırması ile Karma Trafik

```
Senaryo: Aynı ağda PROFINET RT + HMI + SCADA historian

Sorun olmadan önce:
  - Historian veritabanı yüklemesi sırasında 50 Mbps arka plan trafiği
  - PROFINET RT jitter 300 µs'e çıkıyor → PLC I/O zaman aşımı

Çözüm:
  - Switch'te CoS güven modunu etkinleştir
  - PROFINET RT portlarında PCP=6 etiketleme → Kuyruk 4 (SP)
  - Historian: DSCP marklandı, CoS 2 eşlendi → Kuyruk 2
  - Storm control: %3 broadcast eşiği
  
Sonuç: Historian yüklemesi sırasında PROFINET RT jitter < 50 µs'te kaldı
```

### Örnek 4: PRP ile Kritik Altyapı Yedekliliği

```
Senaryo: Su arıtma tesisi SCADA sistemi, "sıfır kesinti" şartı

Topoloji:
  [SCADA Server (DAN)] ─── LAN A (fiber, ring A) ─── [RTU 1] [RTU 2]
                       ─── LAN B (bakır, ring B) ─── [RTU 1] [RTU 2]

Test:
  - LAN A switch'i güç dışı → çerçeve kaybı = 0
  - LAN B kablo çekildi → çerçeve kaybı = 0
  - Her iki arıza senaryosunda SCADA günlüğü kesinti kaydetmedi
```

## Sık Yapılan Hatalar

### Hata 1: RT Ağında Standart IT Switch Kullanmak

```
❌ Yanlış: PROFINET RT ağında yönetilmeyen veya IT tipi switch
   Sonuç : CoS/VLAN etiketleri yok sayılır, RT trafiği düşük öncelikli
           kuyruğa girer, I/O iletişimi aralıklı kesilir

✅ Doğru : Managed switch, "trust CoS" aktif, CoS 6 → yüksek öncelikli kuyruk
```

### Hata 2: IRT Ağında Yanlış Switch Türü

```
❌ Yanlış: IRT ağında store-and-forward modlu IT switch
   Sonuç : Store-and-forward gecikmesi IRT jitter bütçesini aşar (1 µs → 100+ µs)
           Senkronizasyon bozulur, servo hataları oluşur

✅ Doğru : PROFINET Conformance Class C onaylı, cut-through modlu switch
```

### Hata 3: Çevrim Süresini Ağ Gecikmesini Hesaplamadan Belirlemek

```
❌ Yanlış: "PLC görevim 500 µs çalışıyor, yeter" demek
   Sonuç : Ağ gecikmesi + fieldbus gecikmesi + aktüatör yanıtı = toplam > 500 µs
           Kontrol döngüsü kararsızlaşır

✅ Doğru : T_scan + T_network + T_fieldbus hesapla; en az %10 marj bırak
           Örnek: 500 µs çevrim → T_network maksimum 50 µs olmalı
```

### Hata 4: HSR Halkasını Gereğinden Büyük Kurmak

```
❌ Yanlış: 60 düğümlü tek HSR halkası
   Sonuç : Her çerçeve 60 düğümden geçerek çoğaltılır; yol asimetrisi artar,
           jitter bütçesi bozulur, bant genişliği tükenir

✅ Doğru : 16–32 düğüm per halka; büyük ağlarda RedBox ile halkaları birbirine bağla
```

### Hata 5: Storm Control Olmadan PROFINET Multicast Trafiği

```
❌ Yanlış: Arızalı bir IO cihazının aralıksız alarm multicast'i ağı doldurur
   Sonuç : Diğer PROFINET cihazlarının I/O güncellemeleri kaybolur

✅ Doğru : Her porta storm control (%1–5 eşik), IGMP snooping aktif,
           arızalı cihaz portunu izole etmek için SNMP trap yapılandır
```

### Hata 6: PRP'de Paylaşımlı Fiziksel Altyapı

```
❌ Yanlış: LAN A ve LAN B aynı fiziksel kablonet veya güç kaynağı paylaşıyor
   Sonuç : Güç kesintisi veya kablo hasarı her iki LAN'ı aynı anda çökertir
           PRP garantisi anlamsız hale gelir

✅ Doğru : LAN A ve LAN B'nin fiziksel yolları, güç kaynakları ve
           raftaki konumları tamamen bağımsız olmalı
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### PROFINET RT

**Tercih et:**
- Standart I/O güncellemeleri: sensör/aktüatör, sıcaklık, basınç
- 250 µs – 10 ms çevrim süresi yeterliyse
- Ağdaki switch'ler yalnızca managed ve CoS destekliyorsa

**Tercih etme:**
- Servo senkronizasyonu, çok eksenli koordineli hareket
- Jitter bütçesi < 5 µs olan uygulamalar

### PROFINET IRT

**Tercih et:**
- Servo, baskı makinesi, CNC, kesme/paketleme hatları
- Çevrim süresi < 500 µs, jitter < 1 µs gereken durumlar
- Koordineli çok eksen senkronizasyonu

**Tercih etme:**
- Standart I/O (maliyet ve karmaşıklık haklı kılmaz)
- Ağda Conformance Class C dışı switch varsa (seçenek yok, değiştirmek zorunlu)

### EtherCAT

**Tercih et:**
- En yüksek performans gerektiren motion control
- Mikro-saniye çevrim süreleri ve < 1 µs jitter
- Çok sayıda senkron servo ekseni (robotik, koordineli hareket)
- Bant genişliği verimliliğinin kritik olduğu durumlar

**Tercih etme:**
- Büyük ölçekli SCADA/HMI entegrasyonu (EtherCAT bu amaç için tasarlanmamıştır)
- EtherNet/IP veya PROFINET ekosisteminde çalışılıyorsa (protokol uyumsuzluğu)

### TSN

**Tercih et:**
- IT ve OT trafiğini aynı fiziksel ağda taşımak istiyorsan
- OPC UA PubSub ile deterministik bağlantı gerekiyorsa
- Yeni tesis tasarımı, geleceğe yönelik altyapı
- PROFINET over TSN veya EtherNet/IP over TSN yapılandırılıyorsa

**Tercih etme:**
- Mevcut PROFINET IRT veya EtherCAT ağı iyi çalışıyorsa (geçiş maliyeti yüksek)
- Switch ekipmanları TSN desteklemiyorsa (802.1Qbv uyumlu switch gerekli)

### PRP

**Tercih et:**
- Sıfır çerçeve kaybı zorunluysa (güç şebekesi, altyapı, emniyet)
- İki bağımsız fiziksel ağ kurulabiliyorsa
- Station bus (substation level) uygulamaları

**Tercih etme:**
- Bant genişliği kısıtlıysa (×2 ek yük önemli olabilir)
- Tek fiziksel ağ altyapısı varsa (HSR daha uygun)

### HSR

**Tercih et:**
- Sıfır çerçeve kaybı + halka topoloji tercih ediliyorsa
- Bay/process bus düzeyi küçük–orta halka uygulamaları (≤ 32 düğüm)
- Güç şebekeleri ve endüstriyel altyapı

**Tercih etme:**
- Büyük halkalarda (> 32 düğüm); bant genişliği ve jitter sorunları başlar
- Standart I/O veya PROFINET RT ortamları (MRP + DLR yeterli ve daha düşük maliyetli)

## Gerçek Proje Notları

**Not 1 — IRT Ağında Switch Firmware Versiyonu Kritik**
Bir paketleme makinesinde PROFINET IRT kurulumu yapıldı. Tüm switch'ler Conformance Class C onaylı alınmıştı; ancak jitter değerleri 1–2 µs yerine 8–12 µs çıkıyordu. Sorun: switch'lerin firmware'i cut-through modunu desteklemiyordu ve store-and-forward çalışıyordu. Üretici güncel firmware'e geçilmesini önerdi ve sorun çözüldü. **Ders: Conformance Class C sertifikası, yüklü firmware versiyonuna da bağlıdır. Kurulum öncesi firmware doğrulanmalıdır.**

**Not 2 — Karma Trafik Ortamında QoS Gözden Kaçırılıyor**
Bir tesiste PROFINET RT ve SCADA historian trafiği aynı switch'ten geçiyordu. Normal çalışmada sorun yoktu; ancak aylık veri aktarım günlerinde (historian tam yedek) PLC I/O zaman aşımları yaşandı. İncelemede switch'te QoS'un hiç yapılandırılmadığı ve PROFINET RT çerçevelerinin historian trafiğiyle aynı kuyrukta bekletildiği anlaşıldı. CoS yapılandırması eklendikten sonra sorun tamamen ortadan kalktı. **Ders: QoS sadece "karışık trafik ortamlarında" değil, ileride karışacak olasılığı olan her ortamda baştan yapılandırılmalıdır.**

**Not 3 — Broadcast Storm'un Kaynağı Arızalı IO Cihazı**
Bir otomotiv montaj hattında tüm PROFINET cihazları periyodik olarak çevrimdışı kalıyordu (1–2 dakika). Wireshark analizi, belirli bir IO-Link gateway'in 50.000 paket/saniye broadcast gönderdiğini gösterdi. Cihazın dahili yazılımı bir kenar durumda kilitlenip broadcast döngüsüne girmişti. Storm control yapılandırılmamış olduğundan tüm ağ trafiği bunaldı. **Ders: Storm control, fabrikanın "normal" çalışmasında görünmez; ancak bir cihaz arızalandığında anında devreye girmesi gerekir. Her porta %2–5 eşik ile yapılandırılmalıdır.**

**Not 4 — PRP'de "Bağımsız" Ağın Gerçekte Paylaşımlı Olması**
Bir su arıtma tesisinde PRP kurulumu yapıldı. Kağıt üzerinde LAN A ve LAN B bağımsızdı; ancak her ikisinin de aynı UPS grubuna bağlı olduğu görüldü. UPS arızasında her iki LAN aynı anda çöktü ve PRP'nin tüm güvencesi anlamsız kaldı. **Ders: PRP yedekliliği yalnızca ağ katmanında değil, güç, fiziksel konum ve uplink düzeylerinde de sağlanmalıdır.**

**Not 5 — TSN Geçişinde Yapılandırma Karmaşıklığı**
Pilot TSN projesinde standart Ethernet switch'lerinin yerini 802.1Qbv destekli TSN switch'leri alacaktı. GCL (Gate Control List) yapılandırması, sistemdeki tüm akışların bant genişliği profillerinin önceden bilinmesini gerektiriyordu. Planlama aşamasında gözden kaçan bir HMI video akışı, IRT penceresi ile çakışarak kritik bir servo ekseninde 5 ms gecikmeye neden oldu. **Ders: TSN'de GCL planlaması, ağdaki her veri akışının karakterize edilmesini (bant genişliği, periyot, öncelik) gerektirir. 802.1Qcc ile otomatik planlama bu karmaşıklığı azaltır.**

## İlgili Konular

```
knowledge/networking/
├── 01_topologies.md           → MRP/PRP/HSR topoloji ve mimari detayları
├── 02_security.md             → VLAN segmentasyonu, DMZ ve OT güvenliği
└── _synthesis.md              → Topoloji + güvenlik + performans entegre bakışı

knowledge/hardware/
└── industrial-pc/
    └── 03_performance_tuning  → Real-time OS, CPU interrupt latency, PREEMPT_RT

knowledge/codesys/
└── task-structure/
    └── 02_cycle_time          → PLC görev yapısı, scan time hesabı, watchdog

knowledge/protocols/
├── profinet/                  → PROFINET IO mimarisi, GSD dosyaları, tanılama
└── ethercat/                  → EoE, CoE, FoE, SoE EtherCAT protokol katmanları
```
