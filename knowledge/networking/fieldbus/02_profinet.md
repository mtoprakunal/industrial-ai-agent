---
KONU        : PROFINET — Gerçek-Zaman Fieldbus (RT/IRT, GSDML, Conformance Classes)
KATEGORİ    : networking
ALT_KATEGORI: fieldbus
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.profibus.com/technology/profinet"
    başlık: "PROFIBUS & PROFINET International (PI) — PROFINET Technology"
    güvenilirlik: resmi
  - url: "https://www.profinet.com/community/faq"
    başlık: "PI North America — PROFINET FAQ"
    güvenilirlik: resmi
  - url: "https://rt-labs.com/profinet/profinet-basics/"
    başlık: "RT-Labs — PROFINET Basics (RT/IRT, IO Controller/Device, DCP)"
    güvenilirlik: topluluk
  - url: "https://scadaprotocols.com/profinet-conformance-classes-explained/"
    başlık: "SCADA Protocols — PROFINET Conformance Classes (CC-A/B/C/D)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "_synthesis.md"
    ilişki: detaylandırır
  - konu: "01_ethercat.md"
    ilişki: alternatif
  - konu: "knowledge/networking/01_topologies.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: alternatif
ÖNKOŞUL     :
  - "Ethernet temelleri: frame, VLAN önceliği (802.1Q), MAC, EtherType"
  - "TCP/IP ve UDP temelleri"
  - "Fieldbus üst sentezi (_synthesis.md) okunmuş olmalı"
ÇELİŞKİLER :
  - kaynak: "PROFINET vs PROFIBUS karışıklığı"
    konu: "PROFINET ve PROFIBUS farklı protokollerdir, aynı organizasyon (PI) yönetir"
    çözüm: >
      PROFIBUS: seri (RS-485) tabanlı klasik fieldbus. PROFINET: Ethernet tabanlı, modern.
      İkisi de PI (PROFIBUS & PROFINET International) tarafından yönetilir. PROFINET, PROFIBUS'ın
      Ethernet halefidir; proxy cihazlarla PROFIBUS segmentleri PROFINET'e bağlanabilir.
  - kaynak: "PROFINET RT 'standart Ethernet bozuyor mu?'"
    konu: "RT standart switch'lerle çalışır, IRT özel switch gerektirir"
    çözüm: >
      RT (CC-A/B): standart/yönetilen switch'ler yeterli; Layer 2 öncelikli frame (0x8892).
      IRT (CC-C): zaman-dilimli iletişim ve bant rezervasyonu için IRT-yetenekli switch/ASIC zorunlu.
      Çoğu uygulama RT ile yapılır; IRT yalnız mikrosaniye senkron motion için.
---

## Özün Ne

PROFINET (Process Field Network), PROFIBUS & PROFINET International (PI) tarafından yönetilen, IEC 61158/61784 standartlarına dahil Ethernet-tabanlı gerçek-zaman fieldbus'tır. Siemens ekosisteminin (S7 PLC, TIA Portal, SINAMICS, ET200) omurgasıdır ve PROFIBUS'ın Ethernet halefidir. Standart Ethernet altyapısı üzerinde üç iletişim sınıfı sunar: NRT (TCP/UDP, parametre/diagnostik), RT (Layer 2 öncelikli, fabrika otomasyonu) ve IRT (isochronous, mikrosaniye senkron motion).

PROFINET'in tasarım felsefesi "tek kablo üzerinde her şey"dir: aynı Ethernet hattında hem gerçek-zaman I/O (RT/IRT) hem de standart TCP/IP (web, parametre) birlikte koşar. EtherCAT gibi PROFINET de OPC UA/Modbus raporlama katmanının **altında**, gerçek-zaman kontrol katmanında çalışır.

## Nasıl Çalışır

### Üç İletişim Sınıfı

```
┌─────────────────────────────────────────────────────────────────┐
│ NRT (Non-Real-Time)                                             │
│   Taşıma: standart TCP/UDP üzerinde IPv4                        │
│   Kullanım: parametreleme, konfig, diagnostik, web              │
│   Çevrim: ~100ms (zaman-kritik değil)                          │
├─────────────────────────────────────────────────────────────────┤
│ RT (Real-Time)                                                  │
│   Taşıma: Layer 2 (Ethernet), EtherType 0x8892, VLAN önceliği   │
│   IP/TCP YIĞINI ATLANIR → daha düşük gecikme                   │
│   Kullanım: standart fabrika otomasyonu I/O                     │
│   Çevrim: tipik 1-10ms                                          │
├─────────────────────────────────────────────────────────────────┤
│ IRT (Isochronous Real-Time)                                     │
│   Taşıma: 0x8892 + ZAMAN-DİLİMLİ (scheduled), bant rezervasyonu │
│   IRT-yetenekli switch/ASIC ZORUNLU                            │
│   Kullanım: senkron motion control, mikrosaniye eşzamanlılık    │
│   Çevrim: 31.25µs'e kadar; jitter <1µs                         │
└─────────────────────────────────────────────────────────────────┘
```

RT'nin anahtarı: gerçek-zaman frame'leri TCP/IP yığınını atlar ve doğrudan Layer 2'de VLAN öncelik etiketiyle (802.1Q) iletilir, böylece standart trafikten önce geçer. IRT ise bunun ötesine geçer: ağ bir senkron domain'e bölünür, her çevrimde gerçek-zaman trafiği için sabit zaman dilimi rezerve edilir; geri kalan dilim standart trafiğe kalır.

### Cihaz Rolleri

| Rol | Açıklama |
|---|---|
| **IO-Controller** | "Master" — tipik olarak PLC (Siemens S7). Cihazları yapılandırır, cyclic veriyi yönetir. |
| **IO-Device** | "Slave" — saha cihazı (I/O istasyonu, sürücü, sensör). Controller'a cyclic veri sağlar. |
| **IO-Supervisor** | Devreye alma/diagnostik istasyonu (mühendislik PC'si, HMI). |

### Application Relations (AR) ve Communication Relations (CR)

PROFINET'te bir IO-Controller ile IO-Device arasındaki ilişki bir **AR (Application Relation)** ile kurulur. AR içinde:
- **IO-CR (cyclic):** Gerçek-zaman process data alışverişi (RT/IRT).
- **Record Data CR / acyclic:** Parametre okuma/yazma, diagnostik.
- **Alarm CR:** Olay/alarm bildirimleri.

Cihaz çalışır hale gelmek için AR kurulumunu tamamlamalı; AR kurulamazsa (genelde isim/IP uyuşmazlığı) cyclic veri akmaz.

### DCP — İsim ve Adres Atama

PROFINET cihazları **device name** (cihaz adı) ile tanımlanır; IP adresi ikincildir. **DCP (Discovery and Configuration Protocol)** ile:
1. Controller, ağdaki cihazları MAC üzerinden keşfeder.
2. Her cihaza yapılandırılmış **device name** atanır (örn. "drive-axis1").
3. Controller bu isme göre IP atar ve AR kurar.

Devreye almada en sık sorun: cihaza yanlış/eksik isim atanması → controller cihazı bulamaz → AR kurulamaz. Cihaz değişiminde yeni cihaza eski ismin atanması gerekir (LLDP komşuluk bilgisiyle otomatik device replacement bunu kolaylaştırır).

### GSDML Dosyaları

**GSDML (General Station Description Markup Language)**, XML formatında cihaz tanım dosyasıdır. İçinde: cihaz kimliği, modül/submodül yapısı, I/O veri yapısı, desteklenen parametreler ve diagnostik yetenekleri yer alır. Mühendislik aracı (TIA Portal, CODESYS) cihazı bu dosyayla tanır. Önemli alanlar:
- **MinDeviceInterval:** Cihazın desteklediği en kısa çevrim süresi, 31.25µs'in katları cinsinden.
- Modül/submodül slot yapısı → process data eşlemesi buradan çıkar.

GSDML "en son 3 sürümden biri" temelli olmalıdır ve cihaz firmware'iyle eşleşmelidir.

### Conformance Classes (Uygunluk Sınıfları)

| Sınıf | Adı | Özellik | Tipik Kullanım |
|---|---|---|---|
| **CC-A** | RT | Temel PROFINET, standart switch, kablosuz dahil, >4ms tipik | En basit/ucuz, temel I/O |
| **CC-B** | RT | Yönetilen switch, LLDP topoloji, MRP ring redundancy | Standart fabrika otomasyonu (uygulamaların %90+'ı) |
| **CC-C** | IRT | Isochronous, 31.25µs'e kadar, IRT-yetenekli switch/ASIC zorunlu | Senkron motion control |
| **CC-D** | TSN | Time-Sensitive Networking tabanlı (yeni nesil) | Geleceğe dönük, TSN altyapısı |

CC-A/B = RT, CC-C = IRT olarak özetlenir. Çoğu proje CC-B'dir; IRT yalnız motion için gerekir.

### MRP — Ring Redundancy ve LLDP — Topoloji

- **MRP (Media Redundancy Protocol, IEC 62439-2):** Ring topolojide bir kablo koparsa hızlı yeniden yapılanma sağlar (tipik <200ms). CC-B'den itibaren yaygın.
- **LLDP (Link Layer Discovery Protocol):** Komşuluk bilgisini taşır; topoloji keşfi ve otomatik cihaz değişimi (yeni cihaza komşularından isim atama) için kullanılır.

## Pratikte Nasıl Kullanılır (CODESYS / TIA)

CODESYS tarafında PROFINET master (IO-Controller) ve device (IO-Device) eklenti paketleriyle gelir. Tipik akış:

```
1. GSDML kur: Device Repository → cihaz üreticisinin GSDML XML'ini ekle.
2. IO-Controller ekle: Ethernet adaptörüne "PROFINET IO Master" ekle, NIC ve IP ata.
3. IO-Device ekle: master altına cihazı ekle, GSDML'den modül/submodül slot'larını yerleştir.
4. Device name ata: cihaza yapılandırılmış ismi ver (DCP ile fiziksel cihaza yazılır).
5. Çevrim süresi: cihazın MinDeviceInterval'ına uygun update time seç (örn. 4ms CC-B).
6. I/O mapping: process data'yı GVL değişkenlerine bağla.
7. (IRT gerekiyorsa) senkron domain + IRT-yetenekli switch + isochronous mode yapılandır.
8. Bus cycle task: master'ı uygun çevrim süreli task'a bağla.
```

TIA Portal tarafında (Siemens) süreç benzerdir: GSD/GSDML import, cihaz adı atama (online erişim → "assign device name"), topology editor ile LLDP komşuluk, MRP ring tanımı.

## Örnekler

### Örnek 1 — RT vs IRT Kararı
```
Senaryo A: ET200 I/O istasyonu, 20ms'de okunması yeterli dijital sensörler.
  → RT (CC-A/B). Standart switch yeterli. IRT gereksiz maliyet.

Senaryo B: 6 SINAMICS sürücü, baskı silindirleri senkron dönmeli (<1µs jitter).
  → IRT (CC-C). Senkron domain + IRT switch + isochronous mode zorunlu.
```

### Örnek 2 — Device Name Sorunu Teşhisi
```
Belirti : Yeni takılan ET200 cihazı controller'a bağlanmıyor; AR kurulmuyor.
Adım 1  : Online erişim → cihazın device name'i boş mu / yanlış mı?
Adım 2  : DCP ile doğru ismi ata ("io-device-3").
Sonuç   : İsim eşleşti → controller AR kurdu → cyclic veri aktı.
Ders    : PROFINET'te kimlik = device name; IP ikincil. AR kurulmuyorsa önce isme bak.
```

## Sık Yapılan Hatalar

### Hata 1: Device Name Atamayı Unutmak / Yanlış Atamak
PROFINET cihazı isimle tanınır; isim boş/yanlışsa controller bulamaz, AR kurulamaz. Cihaz değişiminde yeni cihaza eski ismin atanması gerekir (otomatik device replacement LLDP ile kolaylaştırır).

### Hata 2: IRT Beklerken Standart Switch Kullanmak
IRT, zaman-dilimli iletişim için IRT-yetenekli switch/ASIC gerektirir. Standart switch'le IRT domain kurulamaz; senkronizasyon sağlanmaz. RT için standart switch yeterlidir, IRT için değil.

### Hata 3: Çevrim Süresini MinDeviceInterval'ın Altına Zorlamak
Cihazın GSDML'deki MinDeviceInterval'ından daha kısa çevrim istemek hata verir ya da cihaz devre dışı kalır. Önce GSDML'deki minimumu kontrol et.

### Hata 4: Yanlış GSDML Sürümü
Firmware ile uyumsuz GSDML → modül/submodül yapısı tutmaz, cihaz yapılandırılamaz. Firmware ile eşleşen, son 3 sürümden birini kullan.

### Hata 5: PROFINET'i PROFIBUS Sanmak
İkisi ayrı protokoldür (PROFINET=Ethernet, PROFIBUS=RS-485 seri). GSD (PROFIBUS) ile GSDML (PROFINET) dosyaları karıştırılmamalı. PROFIBUS segmentleri PROFINET'e proxy cihazla bağlanır.

## Ne Zaman Tercih Edilmeli / Edilmemeli

```
✓ Siemens S7 / TIA Portal ekosistemi (PROFINET'in doğal evi)
✓ PROFIBUS modernizasyonu, geniş Avrupa cihaz mevcudiyeti
✓ MRP ring redundancy gereken hatlar
✓ PROFIsafe ile fonksiyonel güvenlik
✓ Standart Ethernet altyapısı (RT) yeterliyse — maliyet avantajı

✗ Tesis Beckhoff/CODESYS (EtherCAT) ya da Rockwell (EtherNet/IP) ağırlıklı ise
✗ En yüksek motion verimi/en düşük gecikme birincil hedef (EtherCAT processing-on-the-fly üstün)
✗ Düşük maliyet mobil/gömülü tek sürücü (CANopen)
✗ PLC → SCADA/MES raporlaması (OPC UA; PROFINET kontrol katmanı)
```

## Gerçek Proje Notları

**Not 1 — Device name PROFINET'in kimlik anahtarıdır, IP değil.** Saha mühendisleri IP'ye odaklanır ama PROFINET cihazı isimle bulur. "AR kurulmuyor" sorununun çoğu eksik/yanlış device name'dir. Devreye almada her cihaza ismi atanmalı ve bu isim cihaz değişiminde korunmalı.

**Not 2 — Çoğu hat CC-B'dir; IRT'ye gereksiz para harcama.** IRT cazip görünür ama IRT-yetenekli switch'ler ve özel ASIC'ler maliyetlidir. Senkron motion yoksa RT (CC-B) %90 uygulamayı karşılar. IRT yalnız gerçek isochronous motion ihtiyacında gerekçelendirilir.

**Not 3 — MRP ring kapatması topolojiyi sabitler.** MRP ile kablo redundancy harika ama ring manager ve client rolleri doğru atanmalı; iki manager ya da yanlış konfig "ağ fırtınası" benzeri sorunlar üretir. Topology editor ile LLDP komşuluğu doğrulanmalı.

**Not 4 — Otomatik cihaz değişimi (device replacement) sahada altın değerinde.** LLDP komşuluk bilgisiyle, arızalı cihaz çıkarılıp yenisi takıldığında controller komşularından ismi otomatik atar — operatör mühendislik aracı açmadan cihaz değiştirir. Bu özellik baştan yapılandırılmalı (topology kaydı gerekir).

**Not 5 — TCP/IP ve RT aynı kabloda; bant planlaması önemli.** PROFINET'in gücü tek kabloda her şeyi taşımasıdır, ama ağır TCP trafiği (web, kamera, dosya) RT bant payını sıkıştırabilir. Yönetilen switch'lerde QoS/önceliklendirme ve gerekirse VLAN ayrımı planlanmalı.

## İlgili Konular

```
knowledge/networking/fieldbus/
├── _synthesis.md     → Dört fieldbus karşılaştırması, raporlama≠kontrol
├── 01_ethercat.md    → Alternatif Ethernet fieldbus (Beckhoff/CODESYS)
├── 03_ethernet_ip.md → Alternatif Ethernet fieldbus (Rockwell/CIP)
└── 04_canopen.md     → CAN-tabanlı alternatif

knowledge/networking/
└── 01_topologies.md  → MRP ring, RSTP, topoloji seçenekleri

Üst katman (raporlama):
knowledge/protocols/opc-ua/01_architecture.md → PLC↔SCADA (PROFINET'in üstü)

Standartlar: IEC 61158 / IEC 61784 (PI yönetir), MRP IEC 62439-2
Araçlar: TIA Portal, CODESYS PROFINET eklentisi, Wireshark (pn-dcp, pn-rt dissector)
```
