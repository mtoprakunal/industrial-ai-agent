---
KONU        : NAMUR NE107 — Saha Cihazlarında Öz-İzleme ve Diagnostik
KATEGORİ    : standards
ALT_KATEGORI: standards
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://www.namur.net/en/publications/news-archive/ne-107-has-been-revised.html"
    başlık: "NE 107 has been revised — namur.net (resmi)"
    güvenilirlik: resmi
  - url: "https://www.namur.net/en/publications/news-archive/ne107-self-monitoring-and-diagnostics-of-field-devices-has-been-revised.html"
    başlık: "NE107 Self-monitoring and diagnostics of field devices has been revised — namur.net (resmi)"
    güvenilirlik: resmi
  - url: "https://www.dinmedia.de/en/technical-rule/namur-ne-107/394165451"
    başlık: "NAMUR NE 107:2025-07-15 — DIN Media (satın alınabilir belge kaydı)"
    güvenilirlik: resmi
  - url: "https://www.endress.com/en/support-overview/learning-center/namur-ne-107"
    başlık: "Why NAMUR NE 107 matters for device health — Endress+Hauser"
    güvenilirlik: topluluk
  - url: "https://instrumentationtools.com/namur-ne107-standard/"
    başlık: "NAMUR NE107 Standard — Inst Tools"
    güvenilirlik: topluluk
  - url: "https://www.chemengonline.com/eh-modern-instrumentation-simplifies-maintenance/"
    başlık: "Modern Instrumentation Simplifies Maintenance — Chemical Engineering / Endress+Hauser"
    güvenilirlik: topluluk
  - url: "https://www.automationworld.com/products/networks/article/13310449/operator-efficiency-achieved-with-harmonized-diagnostics-from-field-devices"
    başlık: "Operator Efficiency Achieved with Harmonized Diagnostics — Automation World"
    güvenilirlik: topluluk
  - url: "https://www.emersonautomationexperts.com/2013/asset-management/intelligent-field-device-diagnostic-alarm-management/"
    başlık: "Intelligent Field Device Diagnostic Alarm Management — Emerson Automation Experts"
    güvenilirlik: topluluk
  - url: "https://www.emersonautomationexperts.com/2013/asset-management/using-the-ff-912-diagnostics-specification-to-improve-daily-maintenance-routines/"
    başlık: "Using FF-912 Diagnostics Specification — Emerson Automation Experts"
    güvenilirlik: topluluk
  - url: "https://en.wikipedia.org/wiki/NAMUR"
    başlık: "NAMUR — Wikipedia"
    güvenilirlik: topluluk
  - url: "https://www.plantservices.com/home/article/11333980/industrial-networks-namur-ne-107-recommendations-come-to-the-united-states-diagnostic-data-served-where-operators-and-maintenance-techs-can-use-it-plant-services"
    başlık: "NAMUR NE107 Recommendations Come to the United States — Plant Services"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/standards/01_iec61131_3.md"
    ilişki: tamamlar
  - konu: "knowledge/standards/02_iec62443.md"
    ilişki: tamamlar
  - konu: "knowledge/hmi/architecture/03_alarm_management.md"
    ilişki: detaylandırır
  - konu: "knowledge/protocols/opc-ua/02_address_space.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "Proses endüstrisinde saha cihazı (sensör, aktüatör, transmitter) kavramı"
  - "DCS/SCADA/HMI altyapısına genel aşinalık"
  - "4-20 mA HART, PROFIBUS PA veya FOUNDATION fieldbus hakkında temel bilgi"
ÇELİŞKİLER :
  - kaynak: "NE107 belgesi ücretli; namur.net'ten satın alınır veya DIN Media üzerinden erişilir"
    konu: "Standart metninin tam içeriğine kamuya açık doğrudan erişim yok"
    çözüm: "Bu belgede yer alan teknik bilgiler namur.net resmi duyuruları, Endress+Hauser, Emerson ve Automation World gibi otoriter ikincil kaynaklara dayandırılmıştır. Doğrudan alıntı gereken bölümler kaynak notu ile işaretlenmiştir."
  - kaynak: "NE107 2017 baskısı vs 2025 baskısı"
    konu: "Mevcut geçerli baskı 2025-07-15 tarihlidir (32 sayfa, DIN Media); 2017-04-10 baskısı bir önceki resmi versiyondur. 2017→2025 değişiklik detayları kamuya açık kaynaklarda henüz ayrıntılı karşılaştırmalı biçimde yayınlanmamıştır."
    çözüm: "Yeni projeler için 2025 baskısını temel alın. namur.net resmi duyurusunda 2017 revizyonunun getirdiği dört ana değişiklik (genel hükümler, önceliklendirme tablosu, LED gösterimi, fabrika çıkış ayarları) yayınlanmıştır. 2025 değişiklikleri için NE107 belgesi satın alınmalıdır."
---

## Özün Ne

NAMUR NE107 "Self-Monitoring and Diagnosis of Field Devices" (Saha Cihazlarının Öz-İzlenmesi ve Diagnostiği), proses endüstrisinde tüm üreticilerin saha cihazlarından gelen diagnostik mesajları dört standart durum sinyaline — **Failure (F)**, **Function Check (C)**, **Out of Specification (S)** ve **Maintenance Required (M)** — indirgeyen uluslararası kullanıcı tavsiyesidir. Standart, NAMUR (Interessengemeinschaft Automatisierungstechnik der Prozessindustrie e.V.) tarafından yayınlanır; NAMUR, 1949'da Leverkusen, Almanya'da kurulan ve 160'tan fazla proses endüstrisi kullanıcısını temsil eden bağımsız bir kullanıcı derneğidir. NE107'nin temel amacı: bir operatörün cihaz üreticisinden veya çalışma prensibinden bağımsız olarak, herhangi bir akıllı saha cihazından sadece bu dört sembolle cihaz sağlığı hakkında anlık, evrensel düzeyde bilgi almasını sağlamak. Böylece operatör onlarca kriptik hata kodu yerine tek bir renk/sembol görür; bakım teknisyeni ise ilgili akıllı cihaz yönetim yazılımından ayrıntılı tanı bilgisine erişir.

Kaynak: [namur.net resmi duyurusu](https://www.namur.net/en/publications/news-archive/ne107-self-monitoring-and-diagnostics-of-field-devices-has-been-revised.html), [Wikipedia NAMUR](https://en.wikipedia.org/wiki/NAMUR)

## Nasıl Çalışır

### NAMUR ve NE107 Kısaca Tarihçesi

| Tarih | Olay |
|-------|------|
| 1949 | NAMUR, Leverkusen'de kuruldu |
| İlk yayın (tarih kamuya açık değil) | NE107 ilk baskısı |
| 2006-06-12 | Önceki resmi baskı |
| **2017-04-10** | **Güncel pratik referans baskı**; dört önemli ekleme yapıldı |
| 2025-07-15 | En güncel baskı (32 sayfa, DIN Media'dan satın alınabilir) |

2017 revizyonunun getirdiği dört önemli değişiklik (namur.net resmi duyurusuna göre):
1. Genel hükümler güncellendi
2. Durum sinyali önceliklendirme tablosu eklendi
3. LED gösterimi için yöntemler tanımlandı
4. Cihazların fabrika çıkış (default) diagnostik yapılandırması standartlaştırıldı

Kaynak: [namur.net — NE 107 has been revised](https://www.namur.net/en/publications/news-archive/ne-107-has-been-revised.html)

### Dört Standart Durum Sinyali

NE107'nin özü, yüzlerce veya binlerce cihaza özgü hata kodunun dört standart kategoriye eşlenmesidir. Aşağıdaki tablo kaynakların çoğunluğunda tutarlı biçimde aktarılan resmi NE107 sınıflandırmasıdır:

| Sembol | Harf | Renk | İngilizce Adı | Türkçe Adı | Öncelik | Sinyal Geçerliliği | Açıklama |
|--------|------|------|---------------|------------|---------|---------------------|----------|
| ⬛ | **F** | **Kırmızı** | Failure | Arıza / Hata | 1 (En yüksek) | **Geçersiz** | Sensör, enstrüman veya aktüatörde arıza; ölçüm/kontrol sinyali güvenilmez |
| ⬛ | **C** | **Turuncu** | Function Check | Fonksiyon Kontrolü | 2 | **Geçici olarak geçersiz** | Cihaz test, kalibrasyon veya loop testi aşamasında; sinyal geçici olarak geçersiz (beklenen durum) |
| ⬛ | **S** | **Sarı** | Out of Specification | Spesifikasyon Dışı | 4 (En düşük) | **Belirsiz/şüpheli** | Cihaz izin verilen çalışma sınırları dışında; sinyal doğru olabilir ancak güvenilirliği azalmış |
| ⬛ | **M** | **Mavi** | Maintenance Required | Bakım Gerekli | 3 | **Geçerli** | Cihaz çalışıyor ancak yakın vadede bakım gerektiriyor; ölçüm şimdilik güvenilir |

Kaynak: [Endress+Hauser — Why NAMUR NE107 matters](https://www.endress.com/en/support-overview/learning-center/namur-ne-107), [Chemical Engineering / Endress+Hauser](https://www.chemengonline.com/eh-modern-instrumentation-simplifies-maintenance/), [Instrumentation Tools](https://instrumentationtools.com/namur-ne107-standard/)

**Not:** NE107 belgesi ücretli olduğundan renklerin tam resmi tanımına yalnızca otoriter ikincil kaynaklardan ulaşılabilmektedir. Yukarıdaki renk atamaları birden fazla üretici kaynak notuna ve sektör yayınına dayanmaktadır.

### Her Durum Sinyalinin Anlamı ve Örnekleri

**F — Failure (Kırmızı, Öncelik 1)**
Cihazda bir arıza oluşmuş ve ölçüm/kontrol sinyali artık güvenilir değildir. Operatörün hemen müdahalesi gerekir. DCS üzerinde bu sinyal en kritik uyarıyı tetikler.

Örnek durumlar:
- Sensör elektroniği arızası
- Bağlantı kesilmesi (kablonun kopması)
- Dahili referans ölçümünün başarısız olması
- Transmitter'ın kendi kendini teşhis ettiği donanım hatası

**C — Function Check (Turuncu, Öncelik 2)**
Cihaz kasıtlı olarak test, kalibrasyon veya bakım modundadır. Sinyal geçici olarak geçersizdir; bu beklenen ve planlı bir durumdur. Operatör paniklememelidir ancak o noktanın ölçümüne güvenmemelidir.

Örnek durumlar:
- Loop testi sırasında çıkışın zorlanması (forced output)
- Yerinde kalibrasyon
- Simulasyon modu

**S — Out of Specification (Sarı, Öncelik 4)**
Cihaz çalışıyor ancak belirtilen çalışma koşullarının (sıcaklık, basınç, ortam koşulları) dışına çıkılmış olabilir; ölçümün doğruluğu azalmış, güvenilirliği belirsizdir.

Örnek durumlar:
- Ortam sıcaklığının cihazın spesifikasyon aralığı dışına çıkması
- Besleme geriliminin tolerans sınırlarına yaklaşması
- pH sensöründe referans elektrodu bozulmaya başlaması

**M — Maintenance Required (Mavi, Öncelik 3)**
Cihaz şu anda doğru çalışıyor ve ölçüm geçerli, ancak aşınma, kirlenme veya ömür bitimine yaklaşma gibi nedenlerle kısa vadede planlı bakım yapılması önerilmektedir.

Örnek durumlar:
- pH sensörünün ömrüne yaklaşması (periyodik değiştirme gereği)
- Debimetre sensörüne tortu birikmesi
- Valf aktüatörünün sızdırmazlık elemanında yıpranma

Kaynak: [Endress+Hauser](https://www.endress.com/en/support-overview/learning-center/namur-ne-107), [Plant Services](https://www.plantservices.com/home/article/11333980/industrial-networks-namur-ne-107-recommendations-come-to-the-united-states-diagnostic-data-served-where-operators-and-maintenance-techs-can-use-it-plant-services)

### Durum Birleştirme (Aggregation) Kuralları

Bir saha cihazında aynı anda birden fazla diagnostik koşul aktif olabilir. NE107, bu durumda **en yüksek öncelikli sinyalin** ana durum olarak raporlanmasını tanımlar:

```
Öncelik hiyerarşisi (düşük sayı = yüksek öncelik):

1 → Failure (F)        ← Her zaman kazanır
2 → Function Check (C)
3 → Maintenance Required (M)
4 → Out of Specification (S)  ← En düşük, diğerleri tarafından ezilir
```

**Örnek:** Bir cihazda aynı anda hem "Out of Specification" (S, öncelik 4) hem de "Maintenance Required" (M, öncelik 3) koşulu aktifse, DCS'e yalnızca **M** (mavi) sinyali iletilir; S gizlenmez, ancak birleşik (aggregate) durum M olarak gösterilir.

Cihaz içinde dört diagnostik kategoride dört farklı önem derecesi olduğundan teorik olarak 4×4 = 16 eşleme kombinasyonu mevcuttur. Üretici, hangi dahili diagnostiğin hangi NE107 kategorisine gireceğini tanımlar; kullanıcı ise uygulamanın kritikliğine göre bu eşlemeyi yapılandırabilir.

Kaynak: [Plant Services](https://www.plantservices.com/home/article/11333980/industrial-networks-namur-ne-107-recommendations-come-to-the-united-states-diagnostic-data-served-where-operators-and-maintenance-techs-can-use-it-plant-services), [Automation World](https://www.automationworld.com/products/networks/article/13310449/operator-efficiency-achieved-with-harmonized-diagnostics-from-field-devices)

### İki Hedef Kitle Modeli

NE107'nin temel tasarım prensibi, diagnostik bilginin iki farklı role uygun biçimde sunulmasıdır:

```
Saha Cihazı
    │
    ├─ [Özet Durum Sinyali: F/C/S/M]──► DCS Operatör Konsolü
    │                                    (Operatör: "Hemen ne yapmalıyım?")
    │
    └─ [Ayrıntılı Diagnostik Veriler]──► IDM / AMS Yazılımı
                                         (Bakım Teknisyeni: "Neden? Nasıl düzeltirim?")
```

**Operatör perspektifi:** Proses güvenliğini yönetmek için yalnızca dört sinyalden birini görmesi yeterlidir. Ayrıntıya ihtiyacı yoktur; zaten cihazı onarmayacaktır. F sinyali alırsa proses güvenliğini korumak için gerekli aksiyonu alır.

**Bakım teknisyeni perspektifi:** IDM (Intelligent Device Management) veya AMS (Asset Management System) yazılımı üzerinden ayrıntılı diagnostik veriye, hata koduna ve önerilen eyleme erişir. Emerson'ın tanımına göre: "üç tıklamadan az adımda" sorunun kök nedenine ulaşmalıdır.

Kaynak: [Emerson Automation Experts — Intelligent Field Device Diagnostic Alarm Management](https://www.emersonautomationexperts.com/2013/asset-management/intelligent-field-device-diagnostic-alarm-management/), [Plant Services](https://www.plantservices.com/home/article/11333980/industrial-networks-namur-ne-107-recommendations-come-to-the-united-states-diagnostic-data-served-where-operators-and-maintenance-techs-can-use-it-plant-services)

### Fieldbus Protokollerinde NE107 Taşınması

NE107 durum sinyalleri farklı iletişim protokolleriyle taşınabilir:

| Protokol | Uygulama |
|----------|----------|
| **HART** (4-20 mA üzerinden) | En yaygın; ayrı bir "device status" byte ile iletilir |
| **Wireless HART** | HART ile aynı mantık; kablosuz altyapıyla |
| **PROFIBUS PA** | PA diagnostik profili NE107'yi uygular |
| **FOUNDATION fieldbus** | FF-912 spesifikasyonu NE107 önerilerini bünyesine almıştır |
| **EtherNet/IP** | ODVA CIP Process Diagnostics Object ile NE107 statüsü iletilir; aynı zamanda OPC UA'ya haritalanabilir |

**FF-912 nedir?** FOUNDATION fieldbus spesifikasyonunun diagnostik profilini tanımlayan bölümüdür. Fieldbus Foundation, NAMUR NE107 önerilerini FF-912 olarak standardize etmiştir. Emerson DeltaV gibi DCS sistemleri FF-912 host profilini destekleyerek NE107 uyumlu davranışı garanti eder.

Kaynak: [Automation World](https://www.automationworld.com/products/networks/article/13310449/operator-efficiency-achieved-with-harmonized-diagnostics-from-field-devices), [Emerson Automation Experts — FF-912](https://www.emersonautomationexperts.com/2013/asset-management/using-the-ff-912-diagnostics-specification-to-improve-daily-maintenance-routines/)

## Pratikte Nasıl Kullanılır

### Cihaz Seçimi ve Yapılandırma

**1. NE107 uyumlu cihaz temin edilmesi**

Satın alma aşamasında üreticiden NE107 uyumluluğu teyit edilmelidir. Büyük üreticiler (Endress+Hauser, Siemens SITRANS serisi, Emerson Rosemount, Yokogawa, Vega, Pepperl+Fuchs) HART, PROFIBUS PA ve FOUNDATION fieldbus cihazlarında NE107 diagnostik kategorilerini destekler.

**2. Diagnostik eşlemesinin yapılandırılması**

Her saha cihazının dahili diagnostik mesajları üretici tarafından dört NE107 kategorisinden birine önceden atanmıştır. Ancak bu eşleme uygulamanın kritikliğine göre FieldCare (Endress+Hauser), AMS Device Manager (Emerson), veya SIMATIC PDM (Siemens) gibi IDM yazılımları üzerinden değiştirilebilir.

Örnek düşünce süreci:
```
Uygulama: Reaktör besleme debisi (kritik güvenlik noktası)
Karar: "Sensör kirlenmesi" diagnostiği için üretici M (Maintenance) atamış.
Değerlendirme: Bu noktada S (Out of Specification) daha uygun olabilir.
Aksiyon: IDM yazılımından eşlemeyi S olarak değiştir; bakım önceliğini yükselt.
```

**3. DCS/HMI entegrasyonu**

DCS tarafında her saha cihazı için NE107 sinyalleri ayrı bir alarm/uyarı kanalı olarak yapılandırılır. Temel kuralar:
- **F sinyali → Operatör konsolüne yüksek öncelikli alarm** (proses güvenliğini etkileyebilir)
- **C sinyali → Operatöre bilgilendirici uyarı** (bakım planlı mı diye sor; planlıysa acknowledge et)
- **S sinyali → İkincil uyarı veya sadece bakım konsolüne** (uygulama kararı)
- **M sinyali → Yalnızca bakım konsolüne / AMS'e** (operatör için çoğunlukla anlamsız)

**4. Bakım iş akışına entegrasyon**

AMS / IDM yazılımı, NE107 sinyallerini önceliklendirilmiş bakım listesine dönüştürür. Günlük shift başında bakım teknisyeni IDM ekranını açar; F > C > M > S sırasıyla sıralanmış cihaz listesini görür ve kritik cihazlardan başlar.

Kaynak: [Emerson Automation Experts](https://www.emersonautomationexperts.com/2013/asset-management/using-the-ff-912-diagnostics-specification-to-improve-daily-maintenance-routines/), [Instrumentation Tools](https://instrumentationtools.com/namur-ne107-standard/)

### PA-DIM ve FDI ile İlişki

**PA-DIM (Process Automation Device Information Model)**

PA-DIM, FieldComm Group tarafından geliştirilen ve OPC UA Information Model olarak tanımlanan protokolden bağımsız bir cihaz bilgi modelidir. PA-DIM'in temel gereksinim kaynakları arasında doğrudan NE107 yer almaktadır:
- NAMUR NE107 (öz-izleme ve diagnostik)
- NAMUR Open Architecture (NOA) gereksinimleri
- IEC 61987 (semantik kimlikler)

PA-DIM içinde **Device Health** (Cihaz Sağlığı) parametresi, NE107'nin dört durum sinyalini OPC UA bilgi modeli içinde standart bir node olarak sunar. Bu sayede DCS, ERP veya bulut asset management platformları aynı OPC UA arayüzüyle herhangi bir üreticinin cihazından NE107 statüsünü okuyabilir.

**FDI (Field Device Integration)**

FDI, daha önce ayrı standartlar olarak var olan FDT/DTM ve EDDL teknolojilerini birleştiren IEC 62769 standardıdır. FDI sunucusu, cihazın EDD (Electronic Device Description) dosyasını kullanarak PA-DIM information modelini oluşturur:

```
Saha Cihazı (HART/PA/FF) ──► FDI Sunucusu ──► PA-DIM (OPC UA) ──► DCS/ERP/Cloud
                               [EDD kullanır]   [NE107 statüsü dahil]
```

FDT grubu da NE107 sembollerini kendi stil rehberine dahil etmiş; DTM arayüzlerinde F/C/S/M ikonları standart olarak kullanılmaktadır.

Kaynak: Web araması sonuçları: [FieldComm Group PA-DIM arama](https://www.fieldcommgroup.org/technologies/pa-dim), [Automation World](https://www.automationworld.com/products/networks/article/13310449/operator-efficiency-achieved-with-harmonized-diagnostics-from-field-devices)

**Not:** PA-DIM ve FDI ile NE107 entegrasyonunun tam teknik detayları için resmi kaynak PA-DIM White Paper (FieldComm Group) ve IEC 62769 (FDI) standardıdır; bu belgeler ücretli veya üyelik gerektiren kaynaklardır.

## Örnekler

### Örnek 1: Bir pH Transmitter'ın Yaşam Döngüsü Boyunca NE107 Durumları

```
Fabrika çıkışı → Kurulum → Normal çalışma → Yaşlanma → Arıza

Normal operasyon:
  Durum: GOOD (yeşil, NE107 sinyal yok — tüm iyi)
  Ölçüm: pH = 7.2 (geçerli)

3. ay — Elektrot yorulması başlıyor:
  NE107: M (Mavi — Maintenance Required)
  Mesaj: "Elektrot referans ömrü %20 kaldı"
  Aksiyon: Bakım planlaya ekle; ölçüm hâlâ geçerli

4. ay — Kalibrasyon yapılmadı, koşullar kötüleşti:
  NE107: S (Sarı — Out of Specification)
  Mesaj: "Referans jeli kuruma riski; ölçüm doğruluğu azaldı"
  Aksiyon: İvedi bakım; ölçüm şüpheli

4. ay, 15. gün — Elektrot tamamen devre dışı:
  NE107: F (Kırmızı — Failure)
  Mesaj: "Elektrot devre dışı; sinyal geçersiz"
  Aksiyon: Operatör prosesi güvenli moda al; bakım ekibini çağır

Kalibrasyon sırasında:
  NE107: C (Turuncu — Function Check)
  Mesaj: "Cihaz kalibrasyon modunda; çıkış simüle ediliyor"
  Aksiyon: Operatör bu ölçüme güvenme; bakım tamamlanana kadar bekle
```

### Örnek 2: DCS Operatör Ekranında NE107 Gösterimi

```
+----------------------------------+
| TT-101 REAKTÖR SICAKLIK          |
| Değer: 185.4 °C                  |
|                                   |
| [M] BAKIME HAZIRLA               |  ← Mavi kutu, M harfi
|                                   |
| Son güncelleme: 14:23:07          |
+----------------------------------+

Operatörün aksiyon listesi:
  1. Mevcut değer güvenilir → Proses normal devam ediyor
  2. Bakım birimine bildir → Planlı bakım programla
  3. Alarm acknowledge et → Alarm kuyruğundan kaldır
```

```
+----------------------------------+
| PT-205 BESLEME BASINCI           |
| Değer: --- (GEÇERSİZ)            |
|                                   |
| [F] ARIZA — ACİL                 |  ← Kırmızı kutu, F harfi
|                                   |
| Son güncelleme: 14:31:02          |
+----------------------------------+

Operatörün aksiyon listesi:
  1. Ölçüme GÜVENME → Proses güvenliğini kontrol et
  2. Yedek ölçüm noktasına geç
  3. Bakım çağır
  4. Gerekirse prosesi güvenli moda al
```

### Örnek 3: NE107 Eşleme Yapılandırması — Basitleştirilmiş Tablo

```
Dahili Diagnostik Mesajı          → NE107 Kategorisi (Fabrika)  → Kullanıcı Kararı
─────────────────────────────────────────────────────────────────────────────────
"Elektronik arıza"                → F (kırmızı)                  → Değiştirme
"Kalibrasyon modu aktif"          → C (turuncu)                  → Değiştirme
"Sensör kirlenme uyarısı"         → M (mavi)                     → S'ye yükseltilebilir
"Ortam sıcaklığı limiti aşıldı"   → S (sarı)                     → Değiştirme
"Ömür beklentisi %15 kaldı"       → M (mavi)                     → Değiştirme
"Referans jeli azaldı"            → M (mavi)                     → Kritik noktada S
"Güç kaynağı düşük gerilim"       → S (sarı)                     → F'ye yükseltilebilir
```

## Sık Yapılan Hatalar

### Hata 1: Tüm NE107 Sinyallerini Operatör Konsulüne Alarm Olarak Yönlendirmek

Alarm yönetimi perspektifinden bakıldığında NE107'nin **M** ve çoğu **S** sinyali operatörün proses kararlarını etkilemez. Bu sinyalleri operatör konsolüne alarm olarak yönlendirmek, ISA-18.2 / EEMUA 191 standartlarına aykırı alarm yükü oluşturur. Bakım sinyalleri sadece bakım yazılımına gitmelidir.

**Doğru yönlendirme:**
```
F → Operatör konsolu (kritik alarm)
C → Operatör konsolu (bilgilendirici, acknowledge edilebilir)
S → Uygulamaya göre değerlendir; genellikle bakım konsolu
M → Yalnızca bakım/AMS yazılımı
```

### Hata 2: Fabrika Çıkış Eşlemesini Gözden Geçirmemek

Üretici varsayılan NE107 eşlemeleri tasarım gereği muhafazakârdır veya jenerik uygulamalar için yapılmıştır. Her proses noktasının kritikliği farklıdır: bir atıksu tesisindeki pH ölçümü ile bir farmasötik reaktördeki pH ölçümü aynı NE107 konfigürasyonunu gerektirmez. Proje devreye alma (commissioning) aşamasında eşleme gözden geçirilmeli ve uyarlanmalıdır.

### Hata 3: Function Check Sinyalini Arıza Olarak Yorumlamak

**C (turuncu)** operatörün haberi olmadan bakım ekibinin cihazı test moduna aldığı durumlarda çok sık yanlış anlaşılır. Operatör C görüp panikleyebilir. Çözüm: C sinyali geldiğinde DCS'te otomatik olarak bakım iş emri sistemiyle çapraz kontrol yapılmalı; aktif bir bakım işi varsa bilgilendirici mesaj gösterilmelidir.

### Hata 4: NE107'yi Yalnızca FOUNDATION Fieldbus veya PROFIBUS PA'ya Özgü Saymak

NE107 bir tavsiye belgesidir; HART, Wireless HART, EtherNet/IP ve hatta 4-20 mA cihazlarda (harici diagnostik üzerinden) uygulanabilir. HART cihazlarında durum baytı NE107 kategorilerine eşlenebilir. Sadece digital fieldbus'a sahip tesislerde uygulanabilir olduğunu düşünmek yaygın bir yanılgıdır.

### Hata 5: Diagnostik Eşlemeyi Belgelememek

Hangi dahili diagnostiğin hangi NE107 kategorisine atandığı — özellikle fabrika varsayılanından sapılan noktalar — proje dokümantasyonuna girilmelidir. Cihaz değiştirildiğinde veya firmware güncellendiğinde eşleme sıfırlanabilir; dokümantasyon olmadan bu durum fark edilmez.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### NE107 Uyumu Her Zaman Tercih Edilmeli

Her akıllı saha cihazı alımında NE107 uyumluluğu minimum gereksinim olmalıdır. Modern proses endüstrisi DCS/SCADA sistemleri (Emerson DeltaV, Siemens PCS 7/PCS neo, Honeywell Experion, Yokogawa CENTUM VP, ABB System 800xA) NE107 uyumlu cihazları destekler. Üretici bağımsızlığı ve standart HMI gösterimi sağlayan tek evrensel diagnostik çerçevesidir.

### NE107 Özellikle Değerlidir

- **Karışık üretici ortamında:** Endress+Hauser sıcaklık sensörü, Siemens basınç transmitteri ve Emerson valf pozisyoneri aynı DCS'e bağlandığında, operatör hepsinden aynı dört sembolle bilgi alır
- **Büyük tesislerde:** Yüzlerce sensörden gelen binlerce hata kodu yerine dört kategori; alarm yönetimi ve bakım planlaması kökten basitleşir
- **Tahminsel bakım (predictive maintenance) altyapısında:** M ve S sinyallerinin zamansal trendi bakım ihtiyacını önceden öngörür
- **NOA / IIoT mimarilerinde:** PA-DIM üzerinden OPC UA ile taşınan NE107 sinyalleri bulut analytics platformlarına kolayca entegre edilir

### NE107 Sınırlı Kalır veya Dikkat Gerektirir

- **4-20 mA'ya kilitli eski (legacy) sistemlerde:** Standart analog sinyal ile NE107 durumu taşınamaz; HART overlay veya ayrı diagnostik bus gerekir
- **Çok basit on/off sensörlerde:** NE107 diagnostik altyapısı maliyeti faydayı aşabilir; basit NO/NC kontak cihazlarda genellikle uygulanmaz
- **SIL sertifikalı güvenlik işlevlerinde:** IEC 61508 güvenlik fonksiyonu için NE107 kendi başına yeterli değildir; SIL hesaplaması ayrı yapılmalıdır; NE107 tamamlayıcıdır

## Gerçek Proje Notları

**Not 1 — Devreye Alma Sırasında "NE107 Konfigürasyon Toplantısı" Yapın**
Kritik proses noktaları için hangi dahili diagnostiğin hangi NE107 kategorisine atanacağı — üretime geçmeden önce — proses mühendisi, enstrümantasyon mühendisi ve DCS mühendisinin katılımıyla birlikte gözden geçirilmelidir. Bu toplantı alarm rasyonalizasyonu (ISA-18.2) çalışmasının bir parçası olarak yapılabilir.

**Not 2 — F ve C Arasındaki Kritik Fark Sık Karıştırılır**
F: cihaz kendi kendini tespit ettiği gerçek bir arızayı raporluyor.
C: cihaz kasıtlı olarak test/bakım modunda, sinyal geçici olarak geçersiz.
İkisi de "sinyal geçersiz" demek olsa da operasyonel anlamları tamamen farklıdır. Alarm yönetim sistemi bu ayrımı net biçimde yapmalı; operatör eğitiminde özellikle vurgulanmalıdır.

**Not 3 — NE107'nin "Üretici Bağımsızlığı" Vaadi Pratikte Sınırlıdır**
Standart, üreticilerin *kendi dahili diagnostik mesajlarını* dört kategoriyle eşlemesini talep eder; ancak hangi dahili diagnostiğin hangi kategoriye gideceğini üretici belirler. İki farklı üreticinin "sensör kirlenmesi" durumunu F mı, S mi, M olarak mı sınıflandırdığı farklılaşabilir. Gerçek üretici bağımsızlığı için eşleme tablolarının proje bazında hizalanması gerekir.

**Not 4 — Pepperl+Fuchs ADM ile NE107 Ağ Seviyesinde Uygulanabilir**
Pepperl+Fuchs Advanced Diagnostic Module (ADM), FOUNDATION fieldbus H1 ve PROFIBUS PA ağ omurgasına ait fiziksel katman diagnostiklerini (kablo durumu, gürültü, voltaj sapmaları) NE107 formatında raporlar. Bu, cihaz değil ağ diagnostiğini de NE107 çatısı altına alır — büyük tesislerde bus seviyesinde sorunları cihaz sorunlarından ayırt etmek için değerlidir.

**Not 5 — IIoT / Bulut Entegrasyonunda PA-DIM Bağlantısı**
Endress+Hauser Netilion gibi bulut asset management platformları, sahadan PA-DIM + OPC UA üzerinden alınan NE107 sinyallerini trend grafiklere, tahminsel bakım analizine ve uzaktan izleme panolarına entegre eder. Bu mimari, NE107'yi fiziksel saha cihazı katmanından bulut analytics katmanına doğrudan çıkarır; OPC UA'nın rolü burada köprüdür.

Kaynak: [Automation World — Pepperl+Fuchs ADM](https://www.automationworld.com/products/networks/article/13310449/operator-efficiency-achieved-with-harmonized-diagnostics-from-field-devices)

**Not 6 — Firmware Güncellemesi NE107 Eşlemesini Sessizce Değiştirebilir**
Saha cihazının firmware'i güncellendiğinde üreticinin yeni sürümdeki dahili diagnostik→NE107 varsayılan eşlemesi önceki sürümden farklı olabilir. Sahada yaşanan tipik vaka: bir transmitter firmware güncellemesinden sonra daha önce M (Maintenance) raporladığı "sensör sürüklenmesi" durumunu S (Out of Spec) olarak raporlamaya başlar; DCS alarm rasyonalizasyonu buna göre ayarlanmadığı için operatör konsolu beklenmedik sarı alarmlarla dolar. Firmware güncellemesini bir "değişiklik yönetimi" (MoC) olayı olarak ele alın ve güncelleme sonrası NE107 eşleme tablosunu yeniden doğrulayın.

**Not 7 — "GOOD/Yeşil" NE107 Statüsü Değildir; Sinyal Yokluğudur**
Yaygın bir kavram hatası: dört sinyale "yeşil/GOOD" beşinci kategori olarak eklemek. NE107 yalnızca dört *anormal* durumu tanımlar; sağlıklı cihaz "sinyal yok" demektir. Bu ayrım önemlidir çünkü bir cihaz iletişimi tamamen kesilirse DCS "sinyal yok" görür ve bunu yanlışlıkla "GOOD" sayabilir — gerçekte bu bir F (Failure) durumudur. NE107 statüsünün taşındığı kanalın kendisinin (bus kopması, time-out) izlenmesi, statüsün "yokluğunu" arıza olarak yorumlamak için ayrıca gereklidir. Statüsün yokluğu ≠ sağlık.

**Not 8 — HART Cihazlarda NE107 Statüsü 4-20 mA Analog Sinyalden Bağımsızdır**
HART cihazlarda iki bağımsız kanal vardır: analog 4-20 mA birincil değer ve dijital HART katmanındaki cihaz durumu. Bir cihaz F (Failure) raporlarken 4-20 mA çıkışı NAMUR NE43'e göre arıza akımına (örn. <3.6 mA veya >21 mA) gidebilir veya gitmeyebilir — bu konfigürasyona bağlıdır. Sahada karışıklık yaratan nokta: NE107 dijital statüsü "F" derken DCS'in yalnızca analog değeri okuduğu (HART katmanını okumadığı) sistemlerde arıza fark edilmez. NE107'nin gerçekten işe yaraması için DCS/AMS'in HART dijital katmanını aktif okuması gerekir; salt 4-20 mA döngüsü NE107 statüsünü taşımaz. NE43 (arıza akımı) ve NE107 (diagnostik statü) birbirini tamamlar ama ikame etmez.

## Edge Case'ler ve Sistem Limitleri

NE107'nin "dört sembol" sadeliği, gerçek tesis ortamında çok sayıda gri alan barındırır. Aşağıdaki sınır durumları, basit dört-kategori modelinin nerede gerildiğini gösterir.

**Sınıflandırma belirsizlikleri**
- **Aynı fiziksel sebep, farklı kategori:** "Düşük besleme gerilimi" bir üreticide S (Out of Spec — sınır dışı çalışma), başka bir üreticide F (Failure — yakında durabilir) olarak sınıflandırılır. Standart sınıflandırma kuralını değil, *kategori tanımını* verir; eşleme kararı üreticinin yorumuna kalır. Çok-üreticili tesiste aynı arızanın farklı renkte görünmesi kaçınılmazdır.
- **Sınırda gezinen (flapping) statü:** Ortam sıcaklığı spesifikasyon sınırında dalgalanırsa cihaz S ↔ (sinyal yok) arasında saniyede defalarca geçiş yapabilir. Bu, DCS'te alarm flood ve gereksiz iş emri yaratır. NE107 histerezis/debounce tanımlamaz; bu, DCS/AMS tarafında çözülmesi gereken bir uygulama sorunudur.
- **Çoklu eşzamanlı koşulda bilgi kaybı:** Agregasyon kuralı en yüksek önceliği gösterir; F aktifken aynı anda var olan M tamamen gizlenir. Operatör arızayı giderince altında bekleyen M ortaya çıkar — "arıza bitti sandık, bir de baktık bakım gerekiyormuş" durumu. Operatör konsolu yalnızca agregat statüyü gösterirse alttaki koşullar görünmez kalır.

**Önceliklendirme tuzakları**
- **S'nin en düşük öncelikte olması yanıltıcı olabilir:** Öncelik sırası F>C>M>S'tir; ancak S (spesifikasyon dışı) bazı kritik ölçümlerde M'den (bakım gerekli) operasyonel olarak daha tehlikelidir — ölçüm *şu anda* şüphelidir. Standardın sabit önceliği uygulama kritikliğini bilmez; bu yüzden kritik noktalarda kullanıcı eşlemesi (M→S→F yükseltme) gerekir.
- **C (Function Check) güvenlik açığı yaratabilir:** C sırasında sinyal "geçici geçersiz" sayılır ve bazı kontrol stratejileri o ölçümü son geçerli değerde "donmuş" (frozen) tutar. Bir saldırgan veya hatalı bakım, cihazı uzun süre C modunda bırakırsa kontrol körleşir ama operatör "planlı bakım" sanır. C'nin süre sınırı ve eskalasyonu uygulamada tanımlanmalıdır.

**Altyapı ve taşıma sınırları**
- **Salt 4-20 mA (HART'sız) sistemler:** NE107 statüsü taşınamaz; yalnızca NE43 arıza akımı (analog out-of-range) mevcuttur. Bu sistemlerde NE107 fiilen uygulanamaz — ya HART overlay ya ayrı diagnostik bus gerekir.
- **Protokoller arası anlam kayması:** Aynı NE107 statüsü HART, PROFIBUS PA ve FF-912 üzerinden farklı kodlanır; çok-protokollü bir gateway üzerinden geçerken eşleme hataları (özellikle vendor-specific alt kodların kaybı) olabilir. Operatör F/C/S/M'yi görür ama altındaki ayrıntılı kod gateway'de düşmüş olabilir.
- **Eski cihaz / yeni DCS uyumsuzluğu:** NE107-öncesi (legacy) cihazlar dahili diagnostiği NE107 kategorilerine eşlemez; modern DCS bunları "statü bilinmiyor" olarak gösterir. Tesisin diagnostik olgunluğu en eski cihaz seviyesindedir.

## Optimizasyon

NE107'den maksimum değer almak, "dört sembolü göstermek" değil, doğru sinyali doğru kişiye doğru zamanda iletecek bir diagnostik mimarisi kurmaktır.

**Alarm yükü optimizasyonu (ISA-18.2 hizalaması)**
- **Sinyali role göre yönlendirin:** F → operatör (kritik), C → operatör (bilgilendirici), M → yalnızca AMS/bakım, S → uygulamaya göre. M ve gereksiz S sinyallerini operatör konsoluna alarm olarak göndermek EEMUA 191 alarm yükü hedeflerini (10 alarm/saat) ihlal eder; en sık görülen tasarım hatasıdır.
- **C için iş emriyle otomatik korelasyon:** C sinyali geldiğinde bakım iş emri sistemiyle (CMMS) otomatik çapraz kontrol yapın; aktif iş emri varsa operatöre "planlı bakım" notu gösterin, yoksa yetkisiz/beklenmedik test uyarısı verin.
- **S/M için trend tabanlı önceliklendirme:** Anlık sinyal yerine S/M sinyallerinin zaman serisini izleyin; sürekli artan M frekansı yaklaşan F'nin habercisidir ve tahminsel bakım tetikleyicisi olarak kullanılmalıdır.

**Eşleme yapılandırma optimizasyonu**
- **Kritiklik bazlı eşleme matrisi:** Her proses noktasının kritikliğine göre fabrika varsayılan eşlemesini gözden geçirin; kritik güvenlik noktalarında "sensör kirlenmesi" gibi M'leri S/F'ye yükseltin, düşük kritiklikli noktalarda gereksiz S'leri M'e düşürün.
- **Eşlemeyi tek kaynakta (single source of truth) tutun:** Proje genelinde NE107 eşleme tablosunu merkezi bir dokümanda tutun; cihaz/firmware değişiminde bu tabloya karşı doğrulama yapın (bkz. Gerçek Proje Notları 6).

**Mimari optimizasyonu**
- **PA-DIM + OPC UA ile üretici-bağımsız tek arayüz:** Çok-üreticili tesiste her cihazın NE107 statüsünü PA-DIM Device Health node'u üzerinden tek OPC UA arayüzüyle okumak, DCS-cihaz entegrasyon maliyetini düşürür ve bulut analitiğini standardize eder.
- **Bus seviyesi diagnostiği ayırın:** Pepperl+Fuchs ADM gibi fiziksel katman diagnostik modülleriyle "cihaz sorunu" ile "ağ/bus sorunu"nu NE107 çatısında ayırt edin — sahada arıza lokalizasyon süresini kısaltır.

## Derin Teknik Detay

**NE107 neden bir "standart" değil, bir "tavsiye" (Recommendation/NE)?**
NAMUR bir standardizasyon kuruluşu (IEC/ISO gibi) değil, proses endüstrisi *kullanıcılarının* derneğidir. NE107 "NAMUR Empfehlung" (NAMUR Tavsiyesi) olarak yayınlanır; yasal/sözleşmesel bağlayıcılığı yoktur ama pazar gücü vardır. Mantık şudur: kullanıcılar (BASF, Bayer, Shell gibi dev operatörler) toplu satın alma güçleriyle "NE107 uyumlu olmayan cihaz almayız" diyerek üreticileri fiilen zorlar. Bu, "yukarıdan standart dayatma" yerine "talep tarafından çekme" (demand-pull) modelidir — bir IEC standardından farklı bir yönetişim felsefesi.

**Dört kategori neden tam dört? Tasarımın bilişsel temeli**
NE107'nin kalbi bir *insan faktörü* (human factors) kararıdır. Operatör, kriz anında onlarca hata kodunu işleyemez; bilişsel yük (cognitive load) araştırmaları 4±1 kategorinin anlık ayırt edilebilir üst sınır olduğunu gösterir. Dört kategori iki bağımsız soruyu yanıtlar: "Sinyal güvenilir mi?" (F/C = hayır, M = evet, S = şüpheli) ve "Şimdi mi sonra mı müdahale?" (F/C = şimdi, M = sonra, S = değerlendir). Bu iki eksenli ayrım, dört kategorinin neden ne çok ne az olduğunun rasyonelidir.

**İki-hedef-kitle modelinin teorik önemi**
NE107'nin en derin tasarım kararı, *aynı veriyi iki soyutlama seviyesinde* sunmasıdır: operatöre özet (F/C/S/M), bakımcıya ayrıntı (IDM/AMS). Bu, yazılım mühendisliğindeki "bilgi gizleme" (information hiding) ve "ilgililerin ayrılması" (separation of concerns) ilkelerinin saha cihazına uygulanmasıdır. Operatörün arızayı *gidermesi* gerekmez, *yönetmesi* gerekir; bakımcının prosesi *yönetmesi* gerekmez, arızayı *gidermesi* gerekir. Tek bir veri kaynağı iki role iki farklı görünüm sunar — modern MVC mimarilerinin endüstriyel öncülü.

**Öncelik hiyerarşisinin (F>C>M>S) iç mantığı**
Sıralama keyfi değil, "yanlış pozitif maliyeti" ile "kaçırma maliyeti" dengesidir. F en üstte çünkü kaçırılan bir arıza fiziksel sonuç doğurur (kaçırma maliyeti en yüksek). S en altta çünkü "spesifikasyon dışı" çoğu zaman geçici ve telafi edilebilir (yanlış alarm maliyeti yüksek, kaçırma maliyeti düşük). C, F'nin hemen altındadır çünkü ikisi de "sinyal geçersiz" ortak sonucunu paylaşır — fark sadece niyet (kaza vs. plan). M, S'nin üstündedir çünkü M "kesin gelecek bakım" (deterministik), S "belki sorun" (olasılıksal) bilgisi taşır.

**Alternatif/ilişkili çerçevelerle konumlanma**
- **NAMUR NE43 (arıza akımı):** NE107'nin analog atası; 4-20 mA döngüsünde arıza akımı (<3.6 / >21 mA) tanımlar. NE43 "cihaz öldü mü?" sorusunu (ikili), NE107 "cihaz ne durumda?" sorusunu (dört kategori) yanıtlar. NE107 NE43'ün üzerine kuruludur, onu ikame etmez.
- **NAMUR NE131 / NOA (NAMUR Open Architecture):** NE107 diagnostik *anlamını* tanımlar; NOA bu veriyi kontrol sisteminden bağımsız ikinci bir "monitoring & optimization" kanalıyla buluta taşır. NE107, NOA'nın ana veri yüklerinden biridir.
- **VDI/VDE 2650 ve ISA-18.2:** Diagnostik mesajların *alarm* olarak nasıl yönetileceğini ISA-18.2 tanımlar; NE107 *neyin* raporlanacağını, ISA-18.2 *nasıl* alarmlanacağını söyler. İkisi dik (orthogonal) ve tamamlayıcıdır.
- **OPC UA DI / PA-DIM:** NE107'nin makine-okunur, üretici-bağımsız dijital temsili. NE107 insan-merkezli (renk/sembol) doğdu; PA-DIM onu makine-merkezli (OPC UA node) ekosisteme taşıyarak IIoT/bulut analitiğine açtı.

## İlgili Konular

```
knowledge/standards/
├── 01_iec61131_3.md         → PLC yazılım standardı; NE107 FB entegrasyonu için temel
├── 02_iec62443.md           → Endüstriyel siber güvenlik; saha cihazı güvenlik profilleri
└── _synthesis.md            → Üç standardın sentezi

knowledge/hmi/architecture/
└── 03_alarm_management.md   → ISA-18.2 alarm yönetimi; NE107 sinyallerinin alarm olarak
                               nasıl sınıflandırılacağının çerçevesi

knowledge/protocols/opc-ua/
└── 02_address_space.md      → OPC UA address space; PA-DIM'in NE107 sinyallerini
                               OPC UA node olarak nasıl modellediği

İlişkili harici standartlar (bu proje kapsamında belge yok):
  IEC 62769 (FDI)            → Field Device Integration; EDD tabanlı NE107 eşleme
  PA-DIM (FieldComm Group)   → OPC UA tabanlı cihaz bilgi modeli
  FF-912                     → FOUNDATION fieldbus diagnostik profili (NE107'nin FF uygulaması)
  ISA-18.2 / EEMUA 191       → Alarm yönetimi; NE107 sinyallerinin alarm kategorilerine atanması
```
