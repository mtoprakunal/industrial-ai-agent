---
KONU        : Endüstriyel Ağ Güvenliği
KATEGORİ    : networking
ALT_KATEGORI: networking
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards"
    başlık: "ISA/IEC 62443 Series of Standards — ISA Resmi Sayfası"
    güvenilirlik: resmi
  - url: "https://instrunexus.com/iec-62443-zones-and-conduits-a-practical-approach-to-segmentation/"
    başlık: "IEC 62443 Zones and Conduits: A Practical Approach to Segmentation — InstruNexus"
    güvenilirlik: topluluk
  - url: "https://instrunexus.com/all-you-need-to-know-about-level-3-5-dmz-for-iccs-cybersecurity-with-iec-62443/"
    başlık: "All You Need to Know about Level 3.5 DMZ for ICCS Cybersecurity with IEC 62443 — InstruNexus"
    güvenilirlik: topluluk
  - url: "https://csrc.nist.gov/pubs/sp/800/82/r3/final"
    başlık: "NIST SP 800-82 Rev. 3 — Guide to Operational Technology (OT) Security — NIST CSRC"
    güvenilirlik: resmi
  - url: "https://www.cisa.gov/topics/industrial-control-systems"
    başlık: "Industrial Control Systems — CISA (Cybersecurity and Infrastructure Security Agency)"
    güvenilirlik: resmi
  - url: "https://iotworlds.com/iec-62443-zones-and-conduits-explained-with-a-practical-plant-example/"
    başlık: "IEC 62443 Zones and Conduits Explained with a Practical Plant Example — IoT Worlds"
    güvenilirlik: topluluk
  - url: "https://teeptrak.com/en/iec-62443-3-3-system-requirements-2026/"
    başlık: "IEC 62443-3-3 System Security Requirements (2026) — TEEPTRAK"
    güvenilirlik: topluluk
  - url: "https://www.dragos.com/blog/isa-iec-62443-concepts"
    başlık: "Understanding ISA/IEC 62443: A Guide for OT Security Teams — Dragos"
    güvenilirlik: topluluk
  - url: "https://www.sentinelone.com/cybersecurity-101/cybersecurity/what-is-the-purdue-model/"
    başlık: "What Is the Purdue Model? — SentinelOne"
    güvenilirlik: topluluk
  - url: "https://www.paloaltonetworks.com/cyberpedia/what-is-the-purdue-model-for-ics-security"
    başlık: "What Is the Purdue Model for ICS Security? — Palo Alto Networks"
    güvenilirlik: topluluk
  - url: "https://www.fortinet.com/resources/cyberglossary/purdue-model"
    başlık: "What Is the Purdue Model for ICS Security? — Fortinet"
    güvenilirlik: topluluk
  - url: "https://www.checkpoint.com/cyber-hub/network-security/what-is-industrial-control-systems-ics-security/purdue-model-for-ics-security/"
    başlık: "Purdue Model for ICS Security — Check Point Software"
    güvenilirlik: topluluk
  - url: "https://www.cisco.com/c/en/us/td/docs/Technology/industrial-automation-security-design-guide/m-segment-the-network-into-smaller-trust-zones.html"
    başlık: "Industrial Automation Security Design Guide 2.0 — Segment the Network into Smaller Trust Zones — Cisco"
    güvenilirlik: resmi
  - url: "https://www.garlandtechnology.com/blog/ot-segmentation-best-practices-for-a-more-secure-industrial-network"
    başlık: "OT Segmentation Best Practices For a More Secure Industrial Network — Garland Technology"
    güvenilirlik: topluluk
  - url: "https://www.sans.org/blog/introduction-to-ics-security-part-3"
    başlık: "Introduction to ICS Security Part 3 — SANS Institute"
    güvenilirlik: topluluk
  - url: "https://industrialcyber.co/nist/the-essential-guide-to-the-nist-sp-800-82-document/"
    başlık: "The Essential Guide to NIST SP 800-82 — Industrial Cyber"
    güvenilirlik: topluluk
  - url: "https://www.zscaler.com/zpedia/what-is-iec-62443"
    başlık: "What Is IEC 62443? Definition, Breakdown & Methodology — Zscaler"
    güvenilirlik: topluluk
  - url: "https://www.cybiant.com/knowledge/difference-in-cia-triad-security-in-information-technology-and-operational-technology/"
    başlık: "Difference in CIA Triad in IT and Operational Technology — Cybiant"
    güvenilirlik: topluluk
  - url: "https://www.forescout.com/blog/since-stuxnet-a-brief-history-of-critical-infrastructure-attacks/"
    başlık: "Since Stuxnet: A Brief History of Critical Infrastructure Attacks — Forescout"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/networking/01_topologies.md"
    ilişki: gerektirir
  - konu: "knowledge/networking/03_performance.md"
    ilişki: tamamlar
  - konu: "knowledge/standards/02_iec62443"
    ilişki: detaylandırır
  - konu: "knowledge/protocols/opc-ua/03_security"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Purdue/ISA-95 modeli ve katman numaralandırması (bkz. 01_topologies.md)"
  - "VLAN, Layer-3 switch, güvenlik duvarı (firewall) temel kavramları"
  - "IT/OT ayrımı: hangi cihazlar hangi katmanda bulunur"
ÇELİŞKİLER :
  - kaynak: "Çeşitli endüstriyel güvenlik kılavuzları"
    konu: "Purdue modeli geçerliliğini yitirdi mi?"
    çözüm: >
      Bazı kaynaklar (Zscaler, Palo Alto Networks) Purdue modelinin bulut/IoT
      entegrasyonlarında yetersiz kaldığını öne sürerek Zero Trust mimarisine
      geçişi savunur. CISA ve NIST SP 800-82 Rev.3 ise modeli hâlâ temel
      referans çerçeve olarak benimser. Pratik önerimiz: Purdue katmanları ve
      iDMZ'yi temel iskelet olarak koru; Zero Trust prensiplerini (kimlik
      doğrulama, mikro-segmentasyon, sürekli izleme) katman içindeki kontroller
      olarak uygula. İkisi karşıt değil, tamamlayıcıdır.
  - kaynak: "Çeşitli satıcı dokümanları"
    konu: "Güvenlik duvarı mı, veri diyotu mu?"
    çözüm: >
      Güvenlik duvarları çift yönlü denetimli geçişe izin verir; veri diyotları
      yalnızca tek yönlü (OT→IT) akışa izin verir ve donanım düzeyinde zorlama
      sağlar. Historian replikasyonu ve yüksek güvenlik gereksinimleri için veri
      diyotu tercih edilmeli; mühendislik erişimi ve yama dağıtımı gerektiren
      senaryolarda ise iki yönlü iletişime ihtiyaç duyulduğundan güvenlik
      duvarı zorunludur.
---

## Özün Ne

Endüstriyel ağ güvenliği; üretim, enerji, su, ulaştırma gibi kritik altyapılardaki OT (Operational Technology) sistemlerini siber tehditlere karşı koruyan disiplinlerin bütünüdür. IT güvenliğinin CIA öncelik sırası (Gizlilik → Bütünlük → Kullanılabilirlik) OT tarafında tersine döner: **AIC — Kullanılabilirlik önce gelir**, çünkü bir üretim hattının saniyeler içinde durması fiziksel hasar, güvenlik ihlali veya çevre felaketi anlamına gelebilir. Bu öncelik farkı, neredeyse her güvenlik tasarım kararını etkiler.

Konunun uluslararası standardı **ISA/IEC 62443** serisidir; ISA-99 komitesi tarafından geliştirilen ve IEC ile harmonize edilmiş bu seri, endüstriyel otomasyon ve kontrol sistemleri (IACS) için güvenlik bölgesi (zone) ve kanal (conduit) mimarisini, güvenlik seviyelerini (SL 1-4) ve yaşam döngüsü gereksinimlerini tanımlar. Buna paralel olarak **NIST SP 800-82 Rev.3** (Eylül 2023, "Guide to Operational Technology Security"), ABD federal kılavuzu olarak OT güvenliği için pratik karşı tedbirler sunar; CISA ise sektöre yönelik tavsiyeler ve olay müdahale rehberleri yayımlar.

Temel yapı taşı **Purdue/PERA modelinin** güvenlik gözlüğüyle okunmasıdır: her katmanın izin verilen trafiği tanımlanır, katmanlar arası sınırlar güvenlik duvarı ve iDMZ ile korunur, derinlemesine savunma (defense-in-depth) katmanları birbiri üzerine yığılır.

## Nasıl Çalışır

### OT ile IT Güvenliğinin Farkları

OT ve IT sistemleri farklı gereksinimler, yaşam döngüleri ve tehdit yüzeyine sahiptir. Bu farkları anlamadan tasarım yapılırsa IT güvenlik araçları OT ortamını bozar; OT-naif bir IT ekibi ise kritik sistemleri farkında olmadan açığa çıkarır.

| Özellik | OT Ağı | IT Ağı |
|---|---|---|
| Güvenlik önceliği | **AIC**: Kullanılabilirlik → Bütünlük → Gizlilik | **CIA**: Gizlilik → Bütünlük → Kullanılabilirlik |
| Kesinti toleransı | Milisaniye–saniye düzeyi | Dakika–saat düzeyi |
| Yama döngüsü | Yıllık veya daha seyrek (test zorunlu) | Aylık/haftalık standart |
| Cihaz ömrü | 15–25 yıl (1990'lardan kalan PLC'ler hâlâ yaygın) | 3–5 yıl |
| Protokoller | Modbus, PROFINET, DNP3, EtherNet/IP, OPC UA | TCP/IP, HTTP(S), LDAP, TLS |
| Güncelleme/yama | Üretici sertifikasyonu gerektiren, kontrollü | Standart yazılım dağıtım kanalları |
| Arızanın sonucu | Fiziksel hasar, can kaybı, çevre kirliliği | Veri kaybı, finansal/itibar hasarı |

Kaynak: Cybiant, SentinelOne, Dragos — OT/IT karşılaştırma analizleri

---

### Purdue Modelinin Güvenlik Mimarisi

Purdue Referans Mimarisi (PERA), 1992'de Purdue Üniversitesi tarafından geliştirilen ve ISA-99/IEC 62443 tarafından resmi güvenlik mimarisi olarak benimsenen katmanlı modeldir. Model, cihazları ve sistemleri 6 katmana ayırır ve her katmanlar arası sınırda trafik denetimi öngörür.

```
┌───────────────────────────────────────────────────────────────────────┐
│  SEVİYE 5: Dış Ağ / Bulut                                             │  ← IT Alanı
│  İnternet bağlantıları, bulut platformlar, dış servis sağlayıcılar    │
├───────────────────────────────────────────────────────────────────────┤
│  SEVİYE 4: Kurumsal Ağ (Enterprise)                                   │
│  ERP, CRM, e-posta, Active Directory, dosya sunucuları                │
╠═══════════════════════════════════════════════════════════════════════╡
│  SEVİYE 3.5: Endüstriyel DMZ (iDMZ) ← OT/IT Sınır Bölgesi           │
│  Güvenlik duvarı çifti, jump server, historian kopyası, proxy,        │
│  yama sunucusu, veri diyotu, antivirüs güncelleme sunucusu            │
╠═══════════════════════════════════════════════════════════════════════╡
│  SEVİYE 3: Üretim Yönetim Sistemleri (MES/MOM)                       │  ← OT Alanı
│  SCADA sunucuları, data historian (kaynak), MES, toplu iş yönetimi   │
├───────────────────────────────────────────────────────────────────────┤
│  SEVİYE 2: Denetim ve Kontrol                                         │
│  HMI, mühendislik istasyonları (EWS), DCS istemcisi, alarm yönetimi  │
├───────────────────────────────────────────────────────────────────────┤
│  SEVİYE 1: Temel Kontrol                                              │
│  PLC, RTU, güvenlik kontrolcüsü (SIS/SIL), IED                       │
├───────────────────────────────────────────────────────────────────────┤
│  SEVİYE 0: Fiziksel Süreç                                             │
│  Sensörler, aktüatörler, motorlar, valfler, pompalar, kodleyiciler    │
└───────────────────────────────────────────────────────────────────────┘
```

**Temel kural**: Seviyeler yalnızca komşu katmanlarla iletişim kurmalıdır. Seviye 4'ten doğrudan Seviye 2 veya altına erişim **yasaktır** — bu kural güvenlik duvarı kurallarıyla zorunlu kılınır (Kaynak: SentinelOne Purdue Model Kılavuzu, Palo Alto Networks).

---

### Endüstriyel DMZ (iDMZ) — Seviye 3.5

iDMZ, IT ve OT ağları arasında tampon bölge işlevi gören ve 2000'li yıllarda Purdue modeline eklenen kritik mimari bileşendir. Temel ilkesi şudur: **"Hiçbir trafik iDMZ'den doğrudan geçmez"** (Kaynak: InstruNexus, Level 3.5 DMZ rehberi).

#### Çift Güvenlik Duvarı Mimarisi

```
[Kurumsal Ağ L4]
       │
  [FW-1: IT güvenlik duvarı]   ← IT→iDMZ trafiğini denetler
       │
  [iDMZ — Seviye 3.5]
  ├── Jump / Bastion Server
  ├── Historian Mirror (salt okunur kopya)
  ├── OPC UA Proxy / Veri Aracısı
  ├── Yama Yönetim Sunucusu (WSUS, AV güncellemeleri)
  ├── Ters Proxy (Reverse Proxy)
  └── Veri Diyotu (tek yönlü optik köprü, yüksek güvenlik)
       │
  [FW-2: OT güvenlik duvarı]   ← iDMZ→OT trafiğini denetler
       │
[OT Ağı L3 ve altı]
```

**"Sonlandır ve başlat" (terminate-and-initiate) prensibi**: IT tarafından gelen oturumlar iDMZ sunucularında sonlandırılır; iDMZ'den OT'ye gidecek oturumlar ayrı ve yeni oturum olarak başlatılır. Bu yaklaşım, IT kaynaklı saldırıların doğrudan OT'ye ulaşmasını engeller ve her oturumun iDMZ'de denetlenmesine olanak tanır (Kaynak: InstruNexus; Cisco Industrial Automation Security Design Guide 2.0).

**VLAN ile iDMZ destekleme**: Cisco kılavuzu, iDMZ varlıkları için VLAN segmentasyonunun pratik olduğu yerlerde uygulanmasını önermektedir.

---

### IEC 62443 — Bölge (Zone) ve Kanal (Conduit) Mimarisi

ISA/IEC 62443, Purdue modelinin katı hiyerarşisine alternatif (ve tamamlayıcı) olarak esnek bir mantıksal segmentasyon modeli sunar.

#### Temel Kavramlar

**Güvenlik Bölgesi (Security Zone)**: Benzer güvenlik gereksinimleri, risk profili ve işlevsel özellikleri paylaşan varlıkların (cihaz, uygulama, ağ, insan) mantıksal veya fiziksel gruplaması. Bölge sınırları, saldırının yayılım alanını (blast radius) kısıtlar.

**Kanal (Conduit)**: İki veya daha fazla bölge arasındaki iletişim yollarının tamamı — yalnızca ağ bağlantısı değil, bu bağlantıyı denetleyen tüm teknik ve prosedürel kontroller. Güvenlik duvarı, VPN, IDS/IPS, veri diyotu, protokol aracısı bu kontrollerin teknolojik katmanlarıdır (Kaynak: IoT Worlds — IEC 62443 Zones and Conduits).

#### Kanal Tasarım Kriterleri (IEC 62443)

Bir kanal tasarlanırken şu beş boyut netleştirilmelidir (Kaynak: IoT Worlds):

| Boyut | Soru |
|---|---|
| **Kim iletişim kurar?** | Yalnızca yetkili sistemler; paylaşık hesap yasak |
| **Hangi protokoller?** | İşlevsel olarak zorunlu olanlar; diğerleri varsayılan olarak engelli |
| **Veri yönü?** | Tek yönlü (ör. historian replikasyonu) veya çift yönlü |
| **Kimlik doğrulama?** | Güçlü kimlik bilgileri, tercihen MFA ve PKI sertifikası |
| **İzleme/kayıt?** | Trafik denetimi, anomali tespiti, denetim izi |

#### Tipik Tesis Bölge Yapısı

| Bölge | İşlev | Hedef Güvenlik Seviyesi |
|---|---|---|
| Kurumsal IT | ERP, e-posta, dosya sunucuları | SL 2 |
| İDMZ / Bariyer | Proxy, jump server, historian kopyası | SL 2–3 |
| SCADA Sunucuları | Tesis geneli izleme ve kontrol | SL 3 |
| PLC Kontrol Hücresi | Doğrudan proses kontrolü | SL 3 |
| Alan Cihazları | Sensörler, aktüatörler | SL 2–3 |
| Uzak Erişim Bölgesi | Üçüncü taraf bakım, vendor erişimi | SL 2–3 |
| Güvenlik PLC'leri (SIS) | Güvenlik fonksiyonları (SIL 2/3) | SL 4 |

Kaynak: IoT Worlds — Pratik tesis örneği; InstruNexus — IEC 62443 segmentasyon rehberi

---

### IEC 62443 Güvenlik Seviyeleri (SL 1–4)

IEC 62443-3-3 (Sistem Güvenlik Gereksinimleri), her bölge için bir Hedef Güvenlik Seviyesi (SL-T) belirlenmesini zorunlu kılar. Üç SL türü tanımlanır (Kaynak: Dragos — ISA/IEC 62443 Concepts Rehberi):

- **SL-T (Target)**: Varlık sahibinin risk değerlendirmesiyle belirlediği istenen koruma düzeyi
- **SL-C (Capability)**: Sistemin ek tazmin edici tedbir olmaksızın sağlayabildiği doğal güvenlik kapasitesi
- **SL-A (Achieved)**: Uygulama sonrası ölçülen gerçek güvenlik seviyesi

| Güvenlik Seviyesi | Karşı Koyduğu Tehdit | Tipik Bölge |
|---|---|---|
| **SL 1** | Rastlantısal ihlal, kasıtsız hata | Yardımcı sistemler |
| **SL 2** | Basit araçlarla kasıtlı saldırı (varsayılan imalat hedefi) | PLC hücreleri, SCADA |
| **SL 3** | IACS uzmanlığı gerektiren gelişmiş saldırı | Kritik üretim |
| **SL 4** | Devlet destekli, geniş kaynaklı saldırı | SIS, nükleer, kritik altyapı |

Kaynak: InstruNexus — Zone-Conduit segmentasyon rehberi; Teeptrak — IEC 62443-3-3 sistem gereksinimleri (2026)

---

### IEC 62443 Standart Serisi Yapısı

ISA Komitesi ISA-99 tarafından geliştirilen ve IEC ile ortak harmonize edilen bu seri dört ana gruptan oluşur (Kaynak: ISA.org — Resmi standart sayfası):

| Grup | Odak | Yayımlanan Bölümler |
|---|---|---|
| **Bölüm 1** | Genel Kavramlar ve Terimler | 1-1 (2007) — Terminoloji, kavramlar, modeller |
| **Bölüm 2** | Politika ve Prosedürler | 2-1 (2024) Güvenlik programı; 2-2 (2025) Koruma planı; 2-3 Yama yönetimi; 2-4 Servis sağlayıcı |
| **Bölüm 3** | Sistem Düzeyi | 3-2 (2020) Risk değerlendirmesi; 3-3 (2013) Sistem güvenlik gereksinimleri ve SL'ler |
| **Bölüm 4** | Bileşen ve Geliştirme | 4-1 (2018) Güvenli ürün geliştirme yaşam döngüsü; 4-2 (2018) IACS bileşen gereksinimleri |

**IEC 62443-3-3'ün 7 Temel Gereksinim (FR1–FR7)** (Kaynak: Teeptrak — IEC 62443-3-3 Rehberi):

| FR | Konu | SR Sayısı |
|---|---|---|
| FR1 | Kimlik Doğrulama ve Tanımlama Denetimi | 13 |
| FR2 | Kullanım Denetimi (Yetkilendirme / RBAC) | 12 |
| FR3 | Sistem Bütünlüğü | 9 |
| FR4 | Veri Gizliliği | 3 |
| FR5 | Kısıtlı Veri Akışı (Segmentasyon, Zone/Conduit) | 4 |
| FR6 | Olaylara Zamanında Müdahale (Loglama, SIEM) | 2 |
| FR7 | Kaynak Kullanılabilirliği (Yedek, DoS dayanıklılığı) | 8 |

Toplam: 51 temel Sistem Gereksinimi (SR), SL düzeyine bağlı olarak ~100–150 teknik kontrol (Kaynak: Teeptrak).

---

### Güvenlik Duvarı ve DPI (Derin Paket Denetimi)

Endüstriyel güvenlik duvarları, standart IT güvenlik duvarlarından farklı olarak OT protokollerini anlayan uygulama katmanı incelemesi yapar.

#### Güvenlik Duvarı Konumlandırma

Cisco Endüstriyel Otomasyon Güvenlik Tasarım Kılavuzu 2.0 üç kritik yerleştirme noktası tanımlar (Kaynak: Cisco Industrial Automation Security Design Guide):

1. **IT/OT Sınırı** (L4 ↔ iDMZ): Kurumsal ağdan OT'ye giren tüm trafiğin durum tabanlı paket incelemesinden (stateful packet inspection) geçirildiği ana sınır
2. **iDMZ/OT Sınırı** (iDMZ ↔ L3): İkinci güvenlik duvarı; iDMZ servislerinden OT içine geçişi denetler, DPI devreye girer
3. **Hücre/Alan Bölgesi** (L2/L1 arası): PLC hücrelerini birbirinden ayıran mikro-segmentasyon güvenlik duvarları

#### OT Protokolleri için DPI

Endüstriyel protokollere özgü DPI şu protokolleri anlayabilmeli ve kısıtlayabilmelidir:

- **Modbus/TCP**: Fonksiyon kodu düzeyinde kısıtlama (ör. yalnızca okuma izni, yazma bloklama)
- **DNP3**: Nesne türü ve yön denetimi (IEC 60870-5-104 de benzer)
- **S7Comm / S7+**: Siemens PLC iletişimi, yetkisiz komut engelleme
- **EtherNet/IP / CIP**: Allen-Bradley PLC hizmet kodu denetimi
- **OPC UA**: Oturum ve abonelik seviyesinde erişim denetimi (bkz. knowledge/protocols/opc-ua/03_security)

Fortinet FortiGuard OT Güvenlik Hizmeti, PLC/RTU/HMI'ları hedef alan tehditlere yönelik OT imza seti ile SCADA protokollerinde DPI gerçekleştirir ve yetkisiz komutları engeller (Kaynak: Fortinet — ICS and SCADA Risks and Solutions). Cisco Cyber Vision, switch/router üzerinde çalışan dağıtık DPI ile yalnızca meta veri toplar; bant genişliği etkisi minimumdur (Kaynak: Cisco Cyber Vision solution brief).

---

### VLAN ile Segmentasyon

VLAN'lar (IEEE 802.1Q), Layer-2 switch üzerinde aynı fiziksel altyapıyı paylaşan cihazları mantıksal olarak birbirinden ayırır; her VLAN bağımsız bir yayın alanı (broadcast domain) oluşturur.

#### OT'de VLAN Tasarım Prensipleri

NIST SP 800-82 Rev.3 ve Cisco kılavuzu şu prensipleri önermektedir:

```
VLAN 10 — Kurumsal IT (L4)
VLAN 20 — iDMZ Servisleri (L3.5)
VLAN 30 — SCADA / Historian (L3)
VLAN 40 — HMI / Mühendislik İstasyonu (L2)
VLAN 50 — PLC Hücresi A (L1, üretim hattı 1)
VLAN 51 — PLC Hücresi B (L1, üretim hattı 2)
VLAN 60 — Güvenlik PLC'leri / SIS (L1, izole)
VLAN 70 — Uzak Erişim Karantina (DMZ içinde)
```

**VLAN'lar arası yönlendirme kuralları**:
- VLAN'lar arası trafik her zaman Layer-3 switch veya güvenlik duvarı üzerinden geçmelidir
- "Varsayılan olarak engelle, isteneni açık" (deny-all, permit-by-exception) politikası uygulanmalıdır
- VLAN hopping saldırılarına karşı trunk portlarında yalnızca gerekli VLAN'lara izin verilmelidir
- Yönetim erişimi için ayrı bir yönetim VLAN'ı tanımlanmalıdır

**Önemli uyarı**: VLAN tek başına güvenlik katmanı değil, segmentasyon kolaylaştırıcısıdır. Güvenlik duvarı kuralları olmadan VLAN segmentasyonu "yalnızca görünürde kalır" (Kaynak: 01_topologies.md — Proje Notu 3; Cisco tasarım kılavuzu).

---

### Defense-in-Depth (Derinlemesine Savunma)

CISA ICS-CERT Tavsiyesi, defense-in-depth'i "bir saldırının maliyetini artırırken tespit edilme olasılığını yükselten" çok katmanlı güvenlik yaklaşımı olarak tanımlar (Kaynak: CISA — Recommended Practice: Defense in Depth, 2016).

IEC 62443 de bu yaklaşımı beş temel prensip olarak ifade eder (Kaynak: Zscaler — IEC 62443 Rehberi):

1. **Tasarımda Güvenlik (Security by Design)**: Güvenlik; konseptten, devreye almaya, bakıma kadar tüm yaşam döngüsüne entegre edilir
2. **Derinlemesine Savunma**: Fiziksel, teknik ve prosedürel katmanlar iç içe çalışır; tek bir katmanın kırılması sistemin tümünü ele geçirmeye yetmez
3. **Risk Değerlendirmesi**: Tehditler ve açıklar sistematik biçimde belirlenir; her bölge için risk tabanlı SL-T atanır
4. **Sürekli İzleme**: Anomali ve tehdit sürekli tespit edilir; olaylara zamanında müdahale edilir (FR6)
5. **Paydaş İşbirliği**: Varlık sahibi, sistem entegratörü, ürün tedarikçisi ve düzenleyici aynı güvenlik çerçevesini paylaşır

Katman örnekleri:

```
[Fiziksel güvenlik] Kapı kilidi, kamera, server odası erişim kartı
       ↓
[Ağ segmentasyonu] VLAN, güvenlik duvarı, iDMZ, veri diyotu
       ↓
[Protokol denetimi] DPI, uygulama izin listesi, güvenlik duvarı kural seti
       ↓
[Kimlik ve erişim] MFA, RBAC, ayrıcalıklı erişim yönetimi (PAM)
       ↓
[Uç nokta koruması] Beyaz liste (application whitelisting), antivirüs, EDR
       ↓
[Yama yönetimi] Kontrollü yama testi ve dağıtımı (iDMZ üzerinden)
       ↓
[İzleme / SOC] OT-özgü IDS/IPS, SIEM, anomali tespiti
       ↓
[Yedekleme ve kurtarma] Belgelenmiş RTO/RPO, yedek PLC programları
```

---

### Güvenli Uzaktan Erişim

Uzaktan erişim, OT saldırı yüzeyinin en yaygın açığı olmaya devam etmektedir. Dragos 2024 OT güvenlik raporuna göre değerlendirilen OT ortamlarının **%65'inde** yanlış yapılandırılmış uzak erişim koşulları tespit edilmiştir; bunlar arasında hatalı yapılandırma, eski sistemler ve zayıf segmentasyon sayılabilir (Kaynak: SANS — Introduction to ICS Security Part 3).

#### Önerilen Mimari: İki Aşamalı Erişim

SANS ICS Security Part 3 belgesinde tarif edilen ve endüstri standardı haline gelen iki aşamalı model:

```
[Kullanıcı / Uzak Teknisyen]
        │
        ▼ Adım 1: MFA ile VPN
[VPN Sunucusu — iDMZ içinde]
        │
        ▼ Adım 2: RBAC ile Uzak Masaüstü
[Jump / Bastion Sunucu — iDMZ içinde]
        │
        ▼ Güvenlik duvarı politikası açılır (gerektiğinde)
[Hedef OT Sistemi — L2 veya L3]
```

**Kritik kontroller**:
- VPN bağlantısı için **MFA** zorunlu; paylaşık hesap asla kullanılmaz
- Jump server, **yalnızca görev için gerekli sistemlere** erişime izin verir (least privilege)
- Sürücü ve pano (clipboard) yönlendirmesi jump server'da devre dışıdır
- Her iki aşamada da oturum açma günlüğü tutulur, başarısız girişlerde hesap kilitlenir, hareketsizlikte oturum sonlandırılır
- Jump server "karantina" modunda bekler; güvenlik yöneticisi politikayı yalnızca bakım penceresi süresince açar

**Yaygın tehlikeli pratikler** (kaçınılmalı):
- Satıcı doğrudan modem/hotspot bağlantısı kurarak DMZ'yi atlatmak
- OT'ye doğrudan RDP açmak (jump server atlayarak)
- Tüm saha için tek paylaşık hesap kullanmak
- Bakım bitiminde geçici erişim kurallarını kaldırmayı unutmak

Kaynak: SANS — Introduction to ICS Security Part 3

---

### Yaygın Saldırı Yüzeyleri

OT sistemleri tarihsel olarak fiziksel yalıtım (air gap) ile korunurdu. IT/OT entegrasyonu bu yalıtımı büyük ölçüde ortadan kaldırdı; aynı zamanda IT'nin güvenlik açık havuzunu OT'ye taşıdı (Kaynak: Forescout — Since Stuxnet kritik altyapı saldırı tarihi).

**Başlıca saldırı yüzeyleri**:

| Saldırı Yüzeyi | Açıklama | Örnek |
|---|---|---|
| **Uzak Erişim Güvenlik Açıkları** | Zayıf VPN, paylaşık hesap, MFA yokluğu | Oldsmar su tesisi (2021) — TeamViewer kötü yapılandırması |
| **IT→OT Yanal Hareket** | IT ağından ele geçirilen makine OT'ye sızmak için kullanılır | NotPetya (2017) — Şirket ağından OT'ye yayıldı |
| **Mühendislik İstasyonu** | EWS/HMI; Windows tabanlı, PLC'ye doğrudan erişim | Stuxnet (2010) — USB ile dağıtım, Siemens Step7 saldırısı |
| **USB ve Taşınabilir Medya** | Ağdan yalıtılmış sistemlere giriş kapısı | Stuxnet, Triton/TRISIS başlangıç vektörü |
| **Tedarik Zinciri** | Yazılım güncellemesi veya cihaz içine yerleştirilen arka kapı | SolarWinds tarzı saldırılar |
| **Düz (Flat) OT Ağı** | Bölge yoksa bir PLC'nin ele geçirilmesi tüm fabrikayı açar | Fidye yazılımı (EKANS, Industroyer2) |
| **Yamansız Eski Sistemler** | 15–25 yıllık PLCler güncelleme almaz, güvenlik açıkları kalıcıdır | ICSPatch araştırmaları |
| **Tedarikçi/Bakımcı Erişimi** | Üçüncü tarafların sürekli aktif bağlantı bırakması | Yaygın denetim bulgularında ilk sıralarda |
| **Kablosuz Ağlar** | Endüstriyel Wi-Fi veya hücresel modem; yanlış yapılandırılmışsa OT'ye kapı | CISA CPG 2.0 — Kablosuz ağ tehditleri |
| **Historian / SCADA** | IT ile OT arasında köprü görevi gören bu sistemler saldırganlar için pivot noktasıdır | Havex (2014) — OPC sunucusu taraması |

**Öne çıkan tarihsel olaylar** (Kaynak: Forescout — Stuxnet tarihi; OPSWAT — ICS/OT ihlal analizi):
- **Stuxnet (2010)**: USB üzerinden Siemens S7 PLC'ye sızan ilk endüstriyel silah; İran Natanz'da santrifüjleri fiziksel olarak hasar verdi
- **Triton/TRISIS (2017)**: Suudi Arabistan petrokimya tesisinde güvenlik kontrolcüsüne (SIS) saldırdı; can kaybına neden olabilirdi
- **Colonial Pipeline (2021)**: DarkSide fidye yazılımı; operasyonel değil IT sistemleri hedef alındı, ancak iş sürekliliği kaybı nedeniyle boru hattı durduruldu
- **Industroyer2 (2022)**: Ukrayna elektrik şebekesine yönelik, IEC 60870-5-104 protokolünü doğrudan hedef alan kötü amaçlı yazılım

---

## Pratikte Nasıl Kullanılır

### Adım 1: Varlık Envanteri ve Risk Değerlendirmesi

Segmentasyon tasarımına başlamadan önce ne korunacağının bilinmesi gerekir. CISA "Foundations for OT Cybersecurity" rehberi ve NIST SP 800-82 Rev.3 envanteri zorunlu ön adım olarak tanımlar.

- Tüm OT varlıklarını (PLC, HMI, switch, mühendislik istasyonu, yazılım lisansı) belgele
- Her varlığın Purdue katmanını ve işlevsel grubunu belirle
- Kritiklik puanı ata: "Bu varlık ele geçirilirse ne olur?" (güvenlik, üretim, çevre)
- Yüksek kritiklik varlıkları en izolasyonlu bölgelere yerleştir

### Adım 2: Bölge (Zone) Tasarımı

IEC 62443 metodolojisi ile bölgeler altı adımda tasarlanır (Kaynak: InstruNexus — Zone-Conduit rehberi):

1. Kapsamlı varlık envanteri oluştur
2. Yüksek seviye risk değerlendirmesi yap
3. Varlıkları işlev, coğrafya ve güvenlik gereksinimlerine göre grupla
4. Kanal (conduit) tanımlarını "en az ayrıcalık" prensibiyle belirle
5. Detaylı risk analizi yap; her bölge için SL-T ata
6. Sürekli iyileştirme döngüsü kur

**Makro bölgelerle başla**, ardından kritik varlıklar çevresinde mikro-segmentasyon uygula. Önce yaşamsal sistemleri koru; tüm ağı aynı anda mükemmelleştirmeye çalışma.

### Adım 3: iDMZ ve Güvenlik Duvarı Kuralları

- Ağda doğrudan IT→OT erişimi var mı? Varsa, iDMZ yoksa bu birinci önceliği olmalıdır
- FW-1 (IT tarafı) kuralları: IT'den yalnızca iDMZ servislerine erişim; OT'ye doğrudan erişim yasak
- FW-2 (OT tarafı) kuralları: iDMZ'den yalnızca belirli protokollere, belirli kaynak-hedef çiftleriyle erişim
- Kural seti yönetimi: kural eklenmez, değiştirilir; tüm değişiklikler onay ve değişiklik yönetimi (change management) sürecine tabi

### Adım 4: Uzak Erişim Yapılandırması

- Mevcut tüm uzak erişim yollarını (VPN, RDP, TeamViewer, Citrix, modem) envanterle
- İzin verilenler dışında tümünü devre dışı bırak; güvenlik duvarında engelle
- Yetkili yol: VPN+MFA → Jump Server (iDMZ) → Hedef (OT, en az ayrıcalık)
- Üçüncü taraf erişimini zaman kısıtlı, izlenen, rol tabanlı yap

### Adım 5: İzleme ve Anomali Tespiti

- OT trafiğini izleyebilen IDS/IPS (Claroty, Dragos, Nozomi Networks, Cisco Cyber Vision) dağıt
- Temel trafik davranışı (baseline) oluştur; sapmaları uyarıya dönüştür
- Log yönetimi: PLC program değişiklikleri, mühendislik istasyonu girişleri, güvenlik duvarı redleri OT-SIEM'e gönder
- Yıllık veya altı aylık penetrasyon testi ve tatbikat (tabletop exercise)

### Adım 6: Yama ve Güvenlik Açığı Yönetimi

OT'de "yamayı hemen uygula" politikası doğrudan arızaya yol açabilir. Güvenli yaklaşım:

```
1. Yama yayımlandı (üretici bildirimi)
        ↓
2. Test ortamında (shadow PLC / lab) doğrula
        ↓
3. Planlı bakım penceresinde uygula
        ↓
4. Yama sunucusu iDMZ'den dağıtır (doğrudan internet erişimi yok)
        ↓
5. Değişiklik belgelenip onaylanır
```

Yama mümkün değilse tazmin edici kontroller uygula: segmentasyonu sıkılaştır, davranışsal izleme ekle, ilgili protokol trafiğini kısıtla.

---

## Örnekler

### Örnek 1: Kimya Tesisi — Bölge/Kanal Tasarımı

Bir kimya üretim tesisinin IEC 62443 uyumlu bölge haritası:

```
┌──────────────────┐       Kanal-1 (FW-1)        ┌──────────────────────┐
│  Kurumsal IT     │ ◄────────────────────────── │                       │
│  (SL 2, VLAN 10) │ ─────────────────────────► │    iDMZ (SL 3)        │
│  ERP, e-posta    │    Yalnızca HTTPS proxy,    │    VLAN 20            │
└──────────────────┘    historian sorgusu        │  Jump Server          │
                                                 │  Historian Mirror     │
                                                 │  Yama Sunucusu        │
                                                 └──────────┬───────────┘
                                                            │ Kanal-2 (FW-2)
                                              OPC UA → Yalnızca okuma
                                                            │
                              ┌─────────────────────────────▼──────────────┐
                              │  SCADA / Historian (L3, SL 3, VLAN 30)     │
                              │  Tepki verecek Batching sunucuları          │
                              └─────────────────────────────┬──────────────┘
                                                            │ Kanal-3 (FW-3)
                                              Modbus TCP → Yalnızca fonksiyon 3
                                                            │
                              ┌─────────────────────────────▼──────────────┐
                              │  PLC Hücresi / Reaktör (L1-L2, SL 3)       │
                              └────────────────────────────────────────────┘
                              │  Güvenlik PLC (SIS, SL 4, VLAN 60, izole)  │
                              └────────────────────────────────────────────┘
```

### Örnek 2: Güvenlik Duvarı Kural Örneği (Pseudocode)

```
# FW-2 (iDMZ → OT Sınırı)
# Varsayılan: TÜMÜNÜ ENGELLE

ALLOW src=historian_mirror dst=historian_kaynak proto=OPC_UA port=4840 dir=IN
ALLOW src=jump_server dst=hmi_01 proto=RDP port=3389 time=bakim_penceresi
ALLOW src=yama_sunucu dst=ews_01 proto=WSUS port=8530 dir=OUTBOUND
ALLOW src=ews_01 dst=plc_hucre_a proto=S7Comm port=102
DENY  src=ANY dst=plc_hucre_a  # PLC'ye doğrudan tüm diğer trafiği engelle
DENY  src=ANY dst=sis_zone     # Güvenlik PLC'ye her şey engelli
LOG   ALL DENIED
```

### Örnek 3: Uzak Bakım Penceresi Prosedürü

```
T-24 saat: Bakım talebi onaylanır; bakım kişisinin VPN hesabı aktifleştirilir
T-0:       Bakım kişisi VPN'e bağlanır (MFA)
            ↓
           Jump Server'a RDP ile bağlanır (OT kimlik bilgileri)
            ↓
           Jump Server'da sadece hedef PLC programlama yazılımı açılabilir
            ↓
           Oturum kaydedilir (session recording)
            ↓
T+bakım:   Bakım tamamlanır; bağlantı kesilir
T+1 saat:  Güvenlik yöneticisi VPN hesabını devre dışı bırakır ve kuralı kaldırır
T+24 saat: Oturum kaydı gözden geçirilir; değişiklik belgesi imzalanır
```

---

## Sık Yapılan Hatalar

### Hata 1: iDMZ Olmadan IT/OT Bağlantısı

```
❌ Yanlış: ERP sunucusu ──── doğrudan ──── SCADA / PLC
   Sonuç : Bir fidye yazılımı IT'den tüm OT'yi kapatabilir (bkz. NotPetya)
✅ Doğru : ERP → FW-1 → iDMZ → FW-2 → SCADA → PLC
```

### Hata 2: Jump Server Atlayarak Doğrudan OT'ye Bağlanmak

```
❌ Yanlış: VPN → doğrudan → PLC programlama portu (TCP 102)
   Sonuç : Kullanıcı bilgisayarı tehlikedeyse PLC doğrudan tehlikede
✅ Doğru : VPN → Jump Server (iDMZ) → PLC (kısıtlı politikayla)
```

### Hata 3: VLAN'ları Güvenlik Katmanı Saymak

```
❌ Yanlış: "VLAN'lar var, güvendeyiz"
   Sonuç : VLAN'lar arası güvenlik duvarı yoksa VLAN hoppping ile atlatılır
✅ Doğru : Her VLAN sınırında Layer-3 güvenlik duvarı; varsayılan kural = engelle
```

### Hata 4: OT'de Doğrudan İnternet Erişimi

```
❌ Yanlış: Mühendislik istasyonu hem PLC hem internete doğrudan bağlı
   Sonuç : Tehdit yüzeyi maksimuma çıkar; güvenlik açığı keşfi trivialleşir
✅ Doğru : EWS; yalnızca OT VLAN'ına bağlı; yama iDMZ'deki yama sunucusundan alır
```

### Hata 5: Tedarikçi Erişimini Kapatmayı Unutmak

```
❌ Yanlış: Bakım bitti, VPN tüneli "geçici" açık bırakıldı — aylar sonra hâlâ açık
   Sonuç : Tedarikçi ağı saldırıya uğrarsa fabrika OT'ye giriş kapısı açılır
✅ Doğru : Bakım penceresine bağlı zaman kısıtlı hesap; pencere bitince otomatik iptal
```

### Hata 6: Güvenlik Duvarı Kuralını Test Etmeden Uygulamak

```
❌ Yanlış: Yeni FW-2 kural seti üretimde aktifleştirildi; historian trafiği kesildi
   Sonuç : Üretim verisi kayboldu; operatörler kör kaldı
✅ Doğru : Kural değişiklikleri önce test ortamında, ardından planlı bakım penceresinde
```

### Hata 7: Düz (Flat) OT Ağı Bırakmak

```
❌ Yanlış: Tüm PLC, HMI, SCADA aynı subnet üzerinde, güvenlik duvarı yok
   Sonuç : Bir cihazın ele geçirilmesi tüm ağa yayılır; saldırı patlaması sınırsız
✅ Doğru : Her işlevsel grup kendi VLAN/bölgesinde; aralarında güvenlik duvarı
```

---

## Ne Zaman Tercih Edilmeli / Edilmemeli

### iDMZ (Seviye 3.5) Her Zaman Uygulanmalıdır

**Uygula:**
- IT ve OT ağları arasında herhangi bir veri alışverişi varsa (historian, yama, uzak erişim)
- Dış satıcı veya bakım teknisyeni uzaktan bağlanıyorsa
- ERP/MES entegrasyonu varsa

**Maliyet/karmaşıklık gerekçesiyle atlanmamalıdır.** İDMZ olmadan IT/OT entegrasyonu, Purdue modeli tasarımını bütünüyle geçersiz kılar.

---

### Veri Diyotu — Ne Zaman Tercih Edilmeli

**Tercih et:**
- Yalnızca OT→IT veri akışı yeterliyse (historian replikasyonu)
- Kritik altyapı: enerji üretimi, nükleer, su arıtma (SL 4 bölgeler)
- IT→OT komut akışına hiç izin verilmeyecekse (en yüksek güvenlik)

**Tercih etme:**
- Çift yönlü iletişim gerekiyorsa (mühendislik erişimi, yama dağıtımı)
- Bütçe ve operasyonel karmaşıklık kritikse; bu durumda güvenlik duvarı + sıkı kural seti

---

### IEC 62443 SL Hedeflemesi

**SL 1**: Düşük kritiklik yardımcı sistemler, izole ortamlar
**SL 2**: Genel imalat ortamı (varsayılan başlangıç hedefi)
**SL 3**: Kritik üretim, enerji, kimya tesisleri
**SL 4**: Güvenlik sistemleri (SIS), nükleer, savunma altyapısı

---

## Gerçek Proje Notları

**Not 1 — "Güvenlik Duvarı Var, Güvendeyiz" Yanılgısı**
Bir gıda üretim tesisinde iDMZ kuruluydu; ancak FW-2 kuralları "hepsine izin ver" şeklinde yapılandırılmıştı çünkü proje baskısı altında test yapılamazdı. iDMZ fiziksel olarak vardı, işlevsel olarak yoktu. Ders: Güvenlik duvarı kural seti, cihaz varlığından çok daha önemlidir. Kurulum bitmeden kural seti penetrasyon testiyle doğrulanmalıdır.

**Not 2 — Satıcı Modemi Tuzağı**
Bir otomotiv parçası fabrikasında beş ayrı PLC üreticisi bakım amacıyla modem kurmuştu. Bunlar ağ haritalarında yoktu. Güvenlik denetimi sırasında keşfedildi; üçü aktif bağlantı kabul ediyordu. Ders: Ağa bağlanan her cihaz envanterlenmelidir; periyodik ağ taraması (Nmap, Nozomi gibi pasif araçlar) görünmeyen girişleri tespit eder.

**Not 3 — OT'de Windows İşletim Sistemi Yama Gecikmesi**
Seviye 2'deki HMI'larda Windows 7/Server 2008 sıkça görülür — çünkü HMI yazılım üreticisi yeni OS versiyonunu desteklememektedir. Bu sistemler EternalBlue (MS17-010) gibi eski açıklıklara karşı savunmasızdır. Tazmin edici kontrol: bu HMI'ları ayrı VLAN'a al, sadece izin verilen protokol/port kombinasyonlarına izin ver, davranış izleme ekle.

**Not 4 — Uzak Erişim Sonrası "Temizlik Unutma"**
Bakım pencereleri için açılan VPN tünelleri bakım bitiminde kapatılmazsa kalıcı saldırı kapısına dönüşür. Bu nedenle bakım hesaplarının süresi, maksimum bakım penceresi uzunluğuna (genellikle 4–8 saat) sınırlandırılmalıdır; süresi dolan hesap otomatik devre dışı kalır.

**Not 5 — iDMZ Historian Kopyası Yanlış Anlaşılması**
iDMZ'deki historian kopyası "salt okunur" ve "gecikmiş" veri içerir — bu kasıtlıdır. IT tarafı gerçek zamanlı kontrole ihtiyaç duymamalıdır; bunu iDMZ geçişinin engellemesi gereken tam olarak bu taleptir. Bu mimariyle tartışmaya giren IT ekiplerine: gereksinim "gerçek zamanlı kontrol" ise sorun mimari değil, güvenlik politikasıdır.

**Not 6 — IEC 62443 SL 2 ile Orta Ölçek Tesis İçin Süre ve Maliyet**
Teeptrak analizi bir orta ölçek imalat tesisinde SL 2 uyumluluğu için 12–18 ay ve 500.000–1.500.000 € yatırım öngörür. Bu rakam çoğu sigorta poliçesinin talep ettiği tazminat limitinin çok altındadır. Güvenlik yatırımı bir maliyet değil, iş sürekliliği sigortasıdır.

---

## İlgili Konular

```
knowledge/networking/
├── 01_topologies.md     → Purdue model topoloji temeli, VLAN kavramı (ÖNKOŞUL)
├── 03_performance.md    → Güvenlik kontrollerinin gecikme/bant genişliği etkisi
└── _synthesis.md        → Topoloji + güvenlik + performans sentezi

knowledge/standards/
└── 02_iec62443          → IEC 62443 standart serisi tüm detaylar (bu belge özet)

knowledge/protocols/
└── opc-ua/03_security   → OPC UA güvenliği: şifreleme, kimlik doğrulama, RBAC

knowledge/applications/
└── historian/           → Historian replikasyonu iDMZ üzerinden; güvenli veri akışı
```
