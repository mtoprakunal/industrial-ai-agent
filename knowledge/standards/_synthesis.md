---
KONU        : Endüstriyel Otomasyon Standartları — Sentez
KATEGORİ    : standards
ALT_KATEGORI: standards
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/standards/01_iec61131_3.md"
    başlık: "IEC 61131-3 — PLC Programlama Standardı"
    güvenilirlik: deneyimsel
  - url: "knowledge/standards/02_iec62443.md"
    başlık: "IEC 62443 — Endüstriyel Otomasyon Siber Güvenlik Standardı"
    güvenilirlik: deneyimsel
  - url: "knowledge/standards/03_namur_ne107.md"
    başlık: "NAMUR NE107 — Saha Cihazlarında Öz-İzleme ve Diagnostik"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/standards/01_iec61131_3.md"
    ilişki: detaylandırır
  - konu: "knowledge/standards/02_iec62443.md"
    ilişki: detaylandırır
  - konu: "knowledge/standards/03_namur_ne107.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/fundamentals/_synthesis.md"
    ilişki: tamamlar
  - konu: "knowledge/hmi/architecture/03_alarm_management.md"
    ilişki: tamamlar
  - konu: "knowledge/protocols/opc-ua/03_security.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "Bu sentez, üç standart belgesini okuduktan sonra okunmak üzere tasarlanmıştır."
  - "Temel PLC kavramı (IEC 61131-3'ün kapsamını anlamak için)"
  - "OT/IT ağ kavramları (IEC 62443 Zone/Conduit modelini kavramak için)"
  - "Proses endüstrisinde saha cihazı kavramı (NE107 için)"
ÇELİŞKİLER :
  - kaynak: "IEC 62443 Safety vs Security sınırı"
    konu: "IEC 62443 siber güvenliği kapsar; işlevsel güvenlik (SIL) IEC 61508/61511 kapsamındadır. NE107 ise ne güvenlik ne de siber güvenlik standardıdır — bir diagnostik tavsiyesidir. Üç standart birbiriyle örtüşür ama ikame etmez."
    çözüm: "Güvenlik SIL için IEC 61508/61511 önce gelir. Siber güvenlik IEC 62443 kapsamında ayrıca ele alınır. NE107, her iki alanda da cihaz sağlığı görünürlüğü sağlayan tamamlayıcıdır."
  - kaynak: "IEC 61131-3 OOP ile IEC 62443 FR1-FR3 entegrasyonu"
    konu: "IEC 61131-3 OOP özellikleri (Interface, erişim belirteçleri, kalıtım) IEC 62443 FR1-FR3 gereksinimlerine (kimlik doğrulama, kullanım kontrolü, sistem bütünlüğü) yazılım mimarisinde doğal katkı sağlar; ancak standartlar bu bağlantıyı doğrudan tanımlamaz."
    çözüm: "FR3 (Sistem Bütünlüğü) gereksinimini karşılamak için IEC 61131-3 iyi pratiklerinden (PRIVATE/PROTECTED erişim, Interface'e programlama, VAR_INPUT/OUTPUT disiplini) yararlanılabilir. Bu bilinçli bir tasarım kararıdır, standart zorunluluğu değildir."
---

## Özün Ne

Bu sentez, "Üç standart birlikte okunduğunda endüstriyel otomasyon sistemleri nasıl anlaşılır?" sorusuna yanıt verir. Üç belge farklı katmanlarda ama aynı sistemi çerçeveler:

**IEC 61131-3** — PLC'ye nasıl yazılır sorusunu yanıtlar: yazılım modeli, POU'lar, 5 dil, konfigurasyon/kaynak/görev hiyerarşisi.

**IEC 62443** — IACS nasıl korunur sorusunu yanıtlar: siber tehdit modellemesi, Zone/Conduit mimarisi, SL0-SL4 güvenlik seviyeleri, FR1-FR7 teknik gereksinimler.

**NAMUR NE107** — Saha cihazı nasıl izlenir sorusunu yanıtlar: F/C/S/M dört evrensel diagnostik sembolü, operatör-bakımcı bilgi katmanlama modeli.

Bir araya geldiklerinde: IEC 61131-3 sistemi programlar, IEC 62443 sistemi korur, NE107 sistemin sağlığını raporlar. Bu üçü olmadan endüstriyel otomasyon sistemi işlevsel ama kör ve savunmasız kalır.

### Birleştirici İlke — Standartlar Neden Vardır?

Bu üç belge yüzeyde farklı konular gibi görünse de (programlama / güvenlik / diagnostik) ortak bir derin iplikle bağlıdır: **standartlar, onlarca yıllık endüstriyel acının damıtılmış disiplinidir.** Her madde bir kaza, bir uyumsuzluk faciası, bir bakım kâbusu veya bir siber saldırının ardından yazıldı. Bu yüzden üçünün de gerçek dersi aynıdır:

> **Uyum (compliance) bir kutu işaretleme egzersizi değil, bir tasarım felsefesidir.**

- **IEC 61131-3**, her üreticinin kendi diline kilitlediği 1980'ler pazarının acısından doğdu; dersi: *taşınabilirlik ve yapısal disiplin, kısa vadeli kolaylıktan değerlidir.*
- **IEC 62443**, Stuxnet sonrası OT'nin "hava boşluğu (air-gap) yeter" yanılgısının çöküşünden doğdu; dersi: *güvenlik, sonradan eklenen bir katman değil, mimarinin kendisidir (security-by-design).*
- **NAMUR NE107**, operatörün onlarca kriptik hata kodu altında ezildiği kontrol odasının acısından doğdu; dersi: *karmaşıklığı doğru kişiye doğru soyutlama seviyesinde sunmak, bilgiyi gizlemek kadar önemlidir.*

Üçü de "ne yapılacağını" değil, esas olarak "neden o şekilde düşünülmesi gerektiğini" kodlar. Bir mühendis standardı yalnızca uymak için okursa minimum yapar; *neden var olduğunu* anlarsa onu kendi tasarım sezgisine dönüştürür. Bu sentezin amacı, üç standardı bu ikinci seviyede — birbirini güçlendiren tek bir mühendislik disiplini olarak — görmektir.

## Nasıl Çalışır

### Üç Eksenin Birbirine Bağlantısı — Zihin Haritası

```
+--------------------------------------------------------------------------+
|          ENDUSTRiYEL OTOMASYON STANDARTLARI ZiHiN HARiTASI               |
+--------------------------------------------------------------------------+
|                                                                            |
|  IEC 61131-3 (01_iec61131_3.md)                                           |
|  +------------------------------------------------------+                |
|  |             PROGRAMLAMA EKSENi                       |                |
|  |                                                      |                |
|  |  CONFIGURATION -> RESOURCE -> TASK -> PROGRAM -> POU |                |
|  |                                                      |                |
|  |  FUNCTION    | Durumsuz | Saf hesap                  |                |
|  |  FUNC. BLOCK | Durumlu  | Cihaz mantigi, instance    |                |
|  |  PROGRAM     | Durumlu  | Orkestrasyon, tekil        |                |
|  |                                                      |                |
|  |  5 Dil: ST . LD . FBD . SFC . (IL deprecated)       |                |
|  |  OOP (3. baski): Interface, Inheritance, Methods     |                |
|  +-----------------------------+------------------------+                |
|                                |                                          |
|          FB'ler guvenli tasarlanir (FR3: Sistem Butunlugu <->)           |
|                                v                                          |
|  IEC 62443 (02_iec62443.md)                                               |
|  +------------------------------------------------------+                |
|  |             GUVENLiK EKSENi                          |                |
|  |                                                      |                |
|  |  Roller: Varlik Sahibi . Sistem Entegratoru . Tedarikci               |
|  |                                                      |                |
|  |  Zone (SL-T atamasi) <-> Conduit (protokol korumasi)|                |
|  |                                                      |                |
|  |  SL0  SL1    SL2        SL3           SL4            |                |
|  |  Yok  Kaza  Firsatci  IACS-bilgili  Ulus-devlet      |                |
|  |                                                      |                |
|  |  FR1(IAC) . FR2(UC) . FR3(SI) . FR4(DC)             |                |
|  |  FR5(RDF) . FR6(TRE) . FR7(RA)  -- 51 SR            |                |
|  +-----------------------------+------------------------+                |
|                                |                                          |
|    Cihaz guvenlik durumu gorunurlugu (FR6: Olaylara Yanit <-> NE107)     |
|                                v                                          |
|  NAMUR NE107 (03_namur_ne107.md)                                          |
|  +------------------------------------------------------+                |
|  |             DIAGNOSTiK EKSENi                        |                |
|  |                                                      |                |
|  |  F (Kirmizi, Oncelik 1) -> Ariza; sinyal GECERSIZ    |                |
|  |  C (Turuncu, Oncelik 2) -> Fonksiyon kontrolu; gecici|                |
|  |  M (Mavi,    Oncelik 3) -> Bakim gerekli; sinyal gec.|                |
|  |  S (Sari,    Oncelik 4) -> Spesifikasyon disi; supheli               |
|  |                                                      |                |
|  |  Operator -> 4 sembol (ozet)                         |                |
|  |  Bakimci  -> IDM/AMS ayrintili tani                  |                |
|  |  Protokol -> HART . PROFIBUS PA . FF-912 . OPC UA    |                |
|  +------------------------------------------------------+                |
+--------------------------------------------------------------------------+
```

### Mental Model — Tek Paragraf

Bir endüstriyel otomasyon sistemini bina olarak düşünün: IEC 61131-3 binanın yapı planı ve inşaat teknikleridir — hangi malzeme nereye, nasıl birleştirilir. IEC 62443 binanın güvenlik sistemidir — kapı kilitleri, kameralar, bölge geçiş kontrolleri, alarm sistemleri. NE107 ise binadaki her odanın üzerindeki durum lambası panelidir — kırmızı yanıyorsa o oda arızalı, mavi yanıyorsa bakım zamanı gelmiş. Bina işlevsel (61131-3 olmadan kod yok), güvenli (62443 olmadan savunmasız) ve görünür (NE107 olmadan kör) olmak zorundadır; üçü birlikte tam bir sistemi oluşturur.

### Standartlar Arası Kesişim Noktaları

**IEC 61131-3 x IEC 62443 kesişimi:**
- FR3 (Sistem Bütünlüğü): PLC yazılım yapısında yetkisiz kod değişikliğini önlemek; IEC 61131-3'ün PRIVATE/PROTECTED erişim belirteçleri ve Interface'e programlama disiplini buna katkı sağlar.
- FR1 (Kimlik Doğrulama): PLC erişim kontrolü; IEC 61131-3 yazılım modeli, farklı görev ve POU'ların bağımsız yürütülmesini sağlayarak "en az ayrıcalık" (FR2) uygulamasına zemin hazırlar.
- 62443-4-1 güvenli geliştirme yaşam döngüsü, IEC 61131-3 ile yazılan PLC yazılımına da uygulanır; ML2+ süreç olgunluğu PLC kodu için de geçerlidir.

**IEC 62443 x NE107 kesişimi:**
- FR6 (Olaylara Zamanında Yanıt): NE107'nin F sinyali, bir siber güvenlik olayı olmasa da ölçüm bütünlüğünü doğrudan etkiler; FR6 kapsamındaki güvenlik olay izleme ile NE107 cihaz sağlığı izleme birbirini tamamlar.
- FR7 (Kaynak Erişilebilirliği): NE107 M sinyali planlı bakımı öne çekmek için kullanılırsa, cihaz arızası kaynaklı sistem duruşu (DoS riski) azalır — FR7 "erişilebilirlik" hedefine dolaylı katkı.
- IEC 62443 Zone tasarımında, NE107 uyumlu saha cihazlarının bulunduğu Zone'lar için diagnostic data akışı (HART, PA-DIM/OPC UA) Conduit güvenlik gereksinimlerine tabi tutulmalıdır.

**IEC 61131-3 x NE107 kesişimi:**
- NE107 durum sinyallerini PLC'de işlemek için FUNCTION_BLOCK yapısı kullanılır; F/C/S/M durumu için ENUMERATION ve STRUCT tipli değişkenler IEC 61131-3'ün veri tipi modeliyle doğal uyum içindedir.
- IEC 61131-3'ün görev (TASK) mimarisinde diagnostik işleme ayrı bir görevde (örn. CommTask, 100ms) yapılarak kontrol döngüsü (10ms) etkilenmez.
- PA-DIM/OPC UA üzerinden gelen NE107 verisi, IEC 61131-3 Function Block'larından OPC UA client kütüphanesiyle okunabilir; üreticiden bağımsız diagnostik entegrasyonu sağlanır.

## Hızlı Referans Tabloları

### A. Üç Standardın Karşılaştırmalı Özeti

| Boyut | IEC 61131-3 | IEC 62443 | NAMUR NE107 |
|-------|-------------|-----------|-------------|
| **Yayıncı** | IEC TC65 | IEC TC65 WG10 + ISA99 | NAMUR (kullanıcı derneği) |
| **Baskı (aktif)** | 3. Baskı (2013), 4. Baskı (2025) | Çok parçalı seri (en son: 2-1 Ed.2 — 2024) | 2025-07-15 |
| **Tür** | Uluslararası standart | Uluslararası standart ailesi | Kullanıcı tavsiyesi |
| **Kapsam** | PLC yazılım mimarisi ve dilleri | IACS siber güvenliği | Saha cihazı diagnostik standardizasyonu |
| **Hedef Kitle** | PLC yazılım geliştiricisi | Varlık sahibi / SI / Ürün tedarikçisi | Proses operatörü / Bakım teknisyeni |
| **Temel Çıktı** | 5 dil + POU modeli + konfig. hiyerarşisi | Zone/Conduit + SL0-SL4 + FR1-FR7 | F/C/S/M 4 sembol |
| **Sertifikasyon** | PLCopen (BL/CL/RL) | ISASecure (CSA/SSA/SDLA/ACSSA) | Yok (tavsiye belgesi) |
| **Doğduğu acı** | Üretici dil kilitlenmesi (1980'ler) | Stuxnet / OT air-gap yanılgısı | Operatör hata-kodu yükü |
| **Uzman dersi** | Yapısal disiplin > kolaylık | Security-by-design, sonradan değil | Doğru soyutlama doğru role |
| **"Uyum" tuzağı** | "IEC uyumlu" ≠ taşınabilir | "%80 SR" ≠ SL (vektör gerekir) | "4 sembol" ≠ doğru yönlendirme |

---

### A2. Birleştirici Bakış — Üç Standart, Tek Disiplin

| Soru | IEC 61131-3 yanıtı | IEC 62443 yanıtı | NE107 yanıtı | Ortak ilke |
|------|--------------------|--------------------|--------------|------------|
| Soyutlama nasıl yönetilir? | POU/Interface ile bilgi gizleme | Zone/Conduit ile sınır soyutlama | İki-hedef-kitle (özet/ayrıntı) | Karmaşıklığı sınırla, doğru katmanda göster |
| Determinizm neden önemli? | Cyclic scan, WCET garantisi | SL tehdit-aktörü ile sabitlenir | Sabit öncelik (F>C>M>S) | Öngörülebilirlik, "ortalama"dan değerli |
| Sorumluluk kimde? | Geliştirici disiplini | Paylaşılan (sahip/SI/tedarikçi) | Üretici eşler, kullanıcı uyarlar | Tek aktör değil, zincir |
| En zayıf halka? | Üreticiye özgü uzantı sızıntısı | En zayıf FR tüm SL'yi çeker | En eski cihaz tüm olgunluğu çeker | Sistem en zayıf bileşeni kadar iyidir |

---

### B. IEC 62443 Güvenlik Seviyeleri (SL0-SL4)

| Seviye | Tehdit Aktörü | Tipik Teknik Önlem | Hedef Senaryo |
|--------|--------------|-------------------|---------------|
| **SL 0** | Yok | Hiçbir siber güvenlik gereksinimi yok | — |
| **SL 1** | İçeriden kaza, dikkatsizlik | Temel kimlik doğrulama, oturum yönetimi | Düşük kritiklik, izole ofis otomasyon |
| **SL 2** | Fırsatçı dış saldırgan (genel IT bilgisi) | Güçlü parola, ağ segmentasyonu, yamalar | Tipik üretim tesisi (çoğu Zone) |
| **SL 3** | IACS-bilgili hedefli saldırgan | MFA, şifreli iletişim, IDS, izleme | Kritik altyapı (su, enerji, gıda/ilaç) |
| **SL 4** | Ulus devlet düzeyi aktör | Fiziksel yalıtım, HSM, kapsamlı denetim | Nükleer, savunma, ulusal kritik altyapı |

**Üç SL boyutu (karıştırılmamalı):** SL-T (hedef, risk analizinden) — SL-C (bileşen kapasitesi) — SL-A (gerçekleşen, ölçülen). Sağlıklı sistemde: SL-A >= SL-T ve SL-C >= SL-T.

---

### C. IEC 62443 Temel Gereksinimler (FR1-FR7)

| FR | Kısa Ad | Türkçe Adı | SR Sayısı | NE107 / 61131-3 Bağlantısı |
|----|---------|------------|-----------|----------------------------|
| **FR 1** | IAC | Kimlik Belirleme ve Kimlik Doğrulama Kontrolü | 13 | 61131-3 erişim belirteçleri (PRIVATE/PUBLIC) |
| **FR 2** | UC | Kullanım Kontrolü | 12 | 61131-3 VAR_INPUT/OUTPUT disiplini |
| **FR 3** | SI | Sistem Bütünlüğü | 9 | 61131-3 OOP ile yazılım bütünlüğü; NE107 F sinyali |
| **FR 4** | DC | Veri Gizliliği | 3 | OPC UA Sign&Encrypt (NE107 veri taşıma güvenliği) |
| **FR 5** | RDF | Kısıtlı Veri Akışı | 4 | Zone/Conduit; NE107 diagnostic akışı Conduit kapsamında |
| **FR 6** | TRE | Olaylara Zamanında Yanıt | 2 | NE107 F/C sinyalleri olay tetikleyicisi olabilir |
| **FR 7** | RA | Kaynak Erişilebilirliği | 8 | NE107 M sinyali planlı bakımla arızayı önler |

---

### D. NAMUR NE107 — Dört Durum Sinyali Özeti

| Sembol | Renk | Öncelik | Sinyal Geçerliliği | Ne Anlama Gelir | Operatör Aksiyonu |
|--------|------|---------|--------------------|-----------------|--------------------|
| **F** | Kırmızı | 1 (En yüksek) | Geçersiz | Cihaz arızalı; ölçüme güvenme | Hemen müdahale; yedek ölçüme geç |
| **C** | Turuncu | 2 | Geçici geçersiz | Test/kalibrasyon modunda; planlı durum | Bakımı acknowledge et; bekle |
| **M** | Mavi | 3 | Geçerli | Çalışıyor ama yakın bakım gerekli | Bakım planla; acil değil |
| **S** | Sarı | 4 (En düşük) | Belirsiz/şüpheli | Spesifikasyon dışı çalışma; doğruluk azalmış | Değerlendirme yap; bakım öner |

**Agregasyon kuralı:** Birden fazla sinyal aktifse en yüksek öncelikli (düşük sayı) kazanır. F varsa F raporlanır; S diğerleri tarafından ezilir.

**Doğru DCS yönlendirmesi:**
- F → Operatör konsolu (kritik alarm)
- C → Operatör konsolu (bilgilendirici, acknowledge edilebilir)
- S → Uygulamaya göre; genellikle bakım konsolu
- M → Yalnızca bakım/AMS yazılımı

---

### E. IEC 62443 Olgunluk Seviyeleri (ML1-ML4)

| ML | Ad | Tanım |
|----|----|-------|
| **ML 1** | Initial | Belgesi yok, reaktif, bireye bağımlı, tekrarlanamaz |
| **ML 2** | Managed | Yazılı prosedür var, eğitimli personel, tekrarlanabilir |
| **ML 3** | Defined | Kuruluş genelinde standartlaştırılmış, kanıtlı belgeler mevcut |
| **ML 4** | Improving | Metriklerle izleniyor, sürekli iyileştirme döngüsü işliyor |

**Kritik not:** ML süreç olgunluğunu ölçer; SL-C teknik güvenlik kapasitesini ölçer. İkisi bağımsız eksendir.

---

### F. ISASecure Sertifikasyon Programı

| Sertifikat | Kısaltma | Temel Standart | Kimin İçin | Ne Belgeler |
|------------|----------|----------------|------------|-------------|
| Component Security Assurance | **CSA** | IEC 62443-4-2 | Ürün tedarikçisi | Bileşenin SL-C kapasitesi |
| IIoT Component Security Assurance | **ICSA** | IEC 62443-4-2 | IIoT üreticisi | IIoT cihaz güvenliği |
| System Security Assurance | **SSA** | IEC 62443-3-3 | Sistem entegratörü | Entegre sistemin SL-A |
| Security Dev. Lifecycle Assurance | **SDLA** | IEC 62443-4-1 | Ürün tedarikçisi | Geliştirme sürecinin ML olgunluğu |
| ACS Security Assurance | **ACSSA** | 2-1, 2-4, 3-2, 3-3 | Varlık sahibi | IACS operasyonel güvenlik programı |

---

### G. IEC 61131-3 POU Türleri ve Kullanım Rehberi

| POU Türü | İç Durum | Instance | Kullanım | Kaçının |
|----------|----------|----------|---------|---------|
| FUNCTION | Yok | Yok | Saf hesap, birim dönüşüm, ölçekleme | Durum saklamak |
| FUNCTION_BLOCK | Var | Çoklu (fbMotor1, fbMotor2...) | Yeniden kullanılan cihaz mantığı | Tek kopyada kalmak |
| PROGRAM | Var | Tekil | Orkestrasyon, TASK'a atanan kök POU | Her mantığı buraya yazmak |

---

### H. NE107 Protokol Desteği

| Protokol | NE107 Taşıma Yöntemi |
|----------|----------------------|
| **HART** (4-20 mA üzeri) | Device status byte → NE107 kategorisi |
| **Wireless HART** | HART ile aynı mantık, kablosuz |
| **PROFIBUS PA** | PA diagnostik profili NE107 uygular |
| **FOUNDATION fieldbus** | FF-912 spesifikasyonu (NE107 önerilerini standardize eder) |
| **EtherNet/IP** | ODVA CIP Process Diagnostics Object |
| **OPC UA (PA-DIM)** | Device Health node → standart NE107 statüsü |

## Pratikte Nasıl Kullanılır

### Üç Standardı Entegre Kullanan Proje Yaklaşımı

**Tasarım aşamasında (Greenfield):**
1. IEC 62443-3-2 ile Zone/Conduit mimarisini çiz ve SL-T'yi ata.
2. IEC 61131-3 yazılım mimarisini (CONFIGURATION/RESOURCE/TASK) Zone sınırlarına göre yapılandır; güvenlik kritik görevleri en yüksek öncelikli TASK'ta çalıştır.
3. Saha cihazı listesini derlerken NE107 uyumluluğunu seçim kriteri olarak ekle.
4. NE107 diagnostik kanallarının (HART/PA-DIM) Zone/Conduit içinden geçtiğini doğrula ve Conduit politikasına ekle.

**Geliştirme aşamasında:**
1. PLC yazılımını IEC 61131-3 iyi pratikleriyle (FB tabanlı, Interface'e programlama, VAR_INPUT/OUTPUT disiplini) geliştir — bu 62443 FR1-FR3 gereksinimlerine yazılım tarafında zemin hazırlar.
2. Her saha cihazı için NE107 eşleme tablosunu proje dokümanına ekle; fabrika çıkış eşlemelerini kritiklik bazında güncelle.
3. 62443-4-1 ML2+ hedefiyle güvenli geliştirme yaşam döngüsü uygula (güvenlik gereksinim analizi, güvenlik testi, güvenlik açığı yönetimi).

**Devreye alma ve işletme aşamasında:**
1. NE107 sinyallerini DCS/SCADA alarm yönetimiyle hizala: F kritik alarm; C bilgilendirici; M yalnızca AMS; S uygulamaya göre.
2. IEC 62443-2-1 uyarınca IACS Güvenlik Programını (politika, yama yönetimi, olay yanıt planı) aktif tut.
3. NE107 M ve S sinyallerinin zamansal trendini 62443 FR7 (erişilebilirlik) hedefiyle ilişkilendirerek tahminsel bakım planlaması yap.

### Rol Bazlı Uygulama — Kim Hangi Standarda Odaklanır?

```
Rol                             Birincil Standart        Tamamlayici Standart
----------------------------------------------------------------------
PLC Yazilim Gelistirici         IEC 61131-3              IEC 62443 (FR3, 4-1)
Sistem Entegratorü              IEC 62443 (3-2, 3-3)     IEC 61131-3, NE107
Varlik Sahibi / Operator        IEC 62443 (2-1, 3-2)     NE107 (F/C/S/M)
Bakim Teknisyeni                NAMUR NE107              IEC 61131-3 (FB anlayisi)
Urun Tedarikçisi (PLC/sensor)   IEC 62443 (4-1, 4-2)     IEC 61131-3, NE107
Proses Muhendisi                NAMUR NE107              IEC 62443 Zone (cihaz yeri)
```

## Sık Yapılan Hatalar

### Hata 1: Üç Standardı Bağımsız Silolar Olarak Ele Almak

```
Yanlis: "Biz sadece PLC yazilimcisiyiz; IEC 62443 SI ekibinin isi,
         NE107 ise enstru mantasyon muhendisinin meselesi."

Dogru : IEC 61131-3 ile yazilan PLC kodu dogrudan IEC 62443 FR3
        (Sistem Butunlugu) ve FR2 (Kullanim Kontrolü) gereksinimlerini
        etkiler. NE107 F sinyali, 62443 FR6 kapsaminda guvenlik olay
        yonetimiyle entegre calisabilir. Yazilim mimarisi, guvenlik
        tasarimi ve diagnostik entegrasyonu birlikte planlanmalidir.
```

### Hata 2: NE107 M Sinyalini Görmezden Gelmek

```
Yanlis: M sinyali operatör konsolüne alarm olarak yönlendirilmemis
        veya tamamen filtrelenmis; "Zaten bakim ekibinin meselesi."

Dogru : M sinyalini yalnizca AMS/IDM yazilimina yonlendirmek dogru
        olmakla birlikte, M sinyallerinin zamansal trendi 62443 FR7
        (erisebilirlik) ve genel OEE izlemesiyle iliskilendirilmelidir.
        Gormezden gelinen M sinyalleri ilerleyen asamada F (arizaya)
        donusur.
```

### Hata 3: IEC 61131-3 Yazılım Modelini IEC 62443'ten Bağımsız Tasarlamak

```
Yanlis: CONFIGURATION/RESOURCE/TASK hiyerarsisi yalnizca performans
        kaygiyla kurgulanmis; guvenlik Zone'lariyla iliskilendirilmemis.

Dogru : Guvenlik sistemleri (SIL/ESD) kendi ayri TASK'inda (en yuksek
        oncelik), kontrol Zone'u PLC'leri ayri TASK'ta, iletisim/loglama
        ayri TASK'ta calismalidur. Bu hem IEC 61131-3'ün gorev hiyerarsi
        pratigi hem de 62443 Zone mantigiyla uyumludur.
```

### Hata 4: ML ile SL'yi Karıştırmak

```
Yanlis: "Tedarikçimiz SDLA ML 3 sertifikali; SL 3 urun sunuyor demektir."

Dogru : ML (1-4) gelistirme sürecinin olgunlugunu olcer; SL-C urunun
        teknik guvenlik kapasitesini olcer. Iki eksen bagimsizdir.
        Tedarikci seciminde hem SDLA (ML) hem CSA (SL-C) belgelerini
        ayri ayri talep edin.
```

### Hata 5: NE107 Function Check'i Arıza Alarmı Olarak Yapılandırmak

```
Yanlis: C (turuncu) sinyali DCS'te F (kirmizi) ile ayni alarm onceliğinde;
        operator kalibrasyon sirasinda gereksiz panik yasiyor.

Dogru : C sinyali planli ve kasitli bir durumdur; sinyal gecici olarak
        gecersiz olsa da bu bir ariza degildir. DCS'te aktif bakim is
        emriyle capraz kontrol yapilmali; C görüldugunde "bakim
        planlanmis mi?" sorusu otomatik yanitlamalidir.
```

### Hata 6: IEC 61131-3 Global Değişken Anti-Pattern'i ile 62443 FR2 Çelişkisi

```
Yanlis: Her FB dogrudan VAR_GLOBAL yazan kod; hangi modulun neyi
        degistirdigi izlenemiyor — FR2 (en az ayricalik) pratikte yok.

Dogru : Veri akisi VAR_INPUT/VAR_OUTPUT uzerinden; Global degiskenler
        yalnizca paylaşilan I/O esleme icin. Bu hem IEC 61131-3 iyi
        pratigi hem de 62443 FR2 yazilim esdeğeridir.
```

### Hata 7: Brownfield Sistemlerde NE107 ve 62443 Uyumunu Abartmak

```
Yanlis: Mevcut eski (legacy) HART cihazlari veya 4-20 mA analog
        cihazlar icin tam NE107 ve SL 2+ uyumu tek seferde talep etmek.

Dogru : IEC 62443, eski sistemler icin "telafi edici kontroller
        (compensating controls)" mekanizmasini acikca tanimlar.
        NE107'nin analog sistemlerde uygulamasi sinirlidir; HART
        overlay veya ag seviyesinde ADM gibi cozumler gecis doneminde
        alternatif sunar.
```

## Ne Zaman ...

### Ne Zaman IEC 62443 SL-T'yi Yüksek Tutmalı?

- Güvenlik (ESD/SIL) sistemleri: SL 3-4 başlangıç noktası.
- Kritik altyapı (su, enerji, ilaç/gıda): SL 3 kontrol Zone'ları.
- AB NIS2 kapsamındaki operatörler (Ekim 2024+): SL 2 minimum; kritik Zone'lar SL 3.
- Uzaktan erişim gerektiren sistemler: SL 3+; MFA zorunlu.

### Ne Zaman NE107 Eşlemesini Fabrika Ayarından Değiştirmeli?

- Reaktör besleme, güvenlik kritik ölçüm noktaları: Üretici M atadığı "sensör kirlenmesi" diagnostiğini S veya F'ye yükselt.
- Düşük kritiklik noktaları: Gereksiz alarm yükünü önlemek için S'yi M'e düşür veya yalnızca AMS'e yönlendir.
- Farklı üreticilerin aynı tipteki diagnostiklerini tutarlı hizalamak: Çapraz üretici NE107 konfigürasyon toplantısı devreye alma öncesinde yapılmalı.

### Ne Zaman IEC 61131-3 OOP Uzantılarını Kullanmalı?

- Farklı saha cihazlarını ortak bir arayüzle yönetirken (I_FieldDevice Interface + NE107 durum metodları).
- 62443 güvenli geliştirme yaşam döngüsü (4-1) kapsamında kütüphane geliştirirken; Interface'e programlama test edilebilirliği artırır.
- Büyük tesis, çok mühendis: OOP kalıtım ve encapsulation bakım maliyetini düşürür.

### Ne Zaman Tek Başına Yetmez?

- IEC 61131-3 tek başına: Yazılım güvenli kodlanır ama sistem güvenliği (siber tehdit) ele alınmamıştır — 62443 gerekli.
- IEC 62443 tek başına: Siber güvenlik mimarisi kurulmuş ama saha cihazı sağlığı kör noktadır — NE107 tamamlar; cihaz bazlı F sinyali FR6 gözetimini güçlendirir.
- NE107 tek başına: Diagnostik görünürlük vardır ama ne güvenli yazılım ne de siber güvenlik mimarisi garanti altındadır.
- Üçü birlikte ama işlevsel güvenlik göz ardı: IEC 61508/61511 (SIL) siber güvenlikle tamamlayıcıdır ama onun yerine geçmez.

## Gerçek Proje Notları

**Sentez Notu 1 — Zone Tasarımı ile Task Mimarisi Birlikte Planlanmalı**
IEC 62443-3-2 Zone/Conduit mimarisi ve IEC 61131-3 CONFIGURATION/RESOURCE/TASK hiyerarşisi aynı FEED toplantısında birlikte planlanmadığında sonradan maliyetli yeniden yapılandırmalar gerekir. Güvenlik Zone'u sınırları, yazılımın hangi Task'ta hangi öncelikte çalışacağını doğrudan belirlemeli; güvenlik sistemleri (ESD) her zaman en yüksek öncelikli TASK'ta yer almalıdır.

**Sentez Notu 2 — NE107 Konfigürasyon Toplantısı, 62443 Risk Değerlendirmesiyle Eş Zamanlı Yapılmalı**
IEC 62443-3-2 risk değerlendirmesi sırasında Zone'lara atanan SL-T değerleri, o Zone'daki saha cihazları için NE107 eşleme kritikliğini doğrudan etkiler. SL-T 3 atanan bir Zone'daki kritik ölçüm noktasının NE107 eşlemesi daha katı tutulmalı (M'den S veya F'ye yükseltme eşiği düşürülmeli). Bu iki sürecin bağımsız yürütülmesi tutarsızlıklara yol açar.

**Sentez Notu 3 — "IEC 62443 Uyumlu PLC Yazılımı" Vaadi Boşluk Yaratır**
Bazı proje spesifikasyonlarında "62443 SL 2 uyumlu PLC yazılımı" ifadesi geçer. Bu muğlak bir gereksinimdir çünkü 62443-4-2 bileşen güvenliği ürün tedarikçisine yönelik teknik gereksinimler içerir; uygulama yazılımı geliştirme süreci ise 62443-4-1 SDLA kapsamındadır. "PLC yazılımı SL 2 uyumlu" demek için en azından: güvenli geliştirme sürecinin ML2+ olması, yazılımın FR1-FR3 gereksinimlerini karşıladığının test edilmiş olması ve TASK mimarisinin Zone sınırlarıyla hizalanması gerekir.

**Sentez Notu 4 — NE107 F Sinyali Bir 62443 Olay Göstergesi Olabilir**
Anormal biçimde artan F sinyali frekansı (normalden sapma) bir siber güvenlik olayının belirtisi olabilir: kötü niyetli firmware değişikliği, konfigürasyon sabotajı veya fiziksel müdahale sonucu cihaz tanı mekanizmasının bozulması. 62443 FR6 (Olaylara Zamanında Yanıt) kapsamındaki SIEM/SOC entegrasyonunda NE107 F sinyallerinin zaman serisi analizi, anormali tespiti için ek bir veri kaynağı olarak kullanılabilir.

**Sentez Notu 5 — Üç Standardın Dokümantasyon Hiyerarşisi**
Bir endüstriyel otomasyon projesinde üç standardın gerektirdiği belgeler şu katmanlarda toplanır:

```
Proje Güvenlik Programi (62443-2-1)
├── Zone/Conduit Mimarisi ve SL-T Tablosu (62443-3-2)
├── FR1-FR7 Uyum Matrisi (62443-3-3)
├── PLC Yazilim Mimarisi Belgesi (IEC 61131-3 Task/POU yapisi)
│   └── FUNCTION BLOCK kutuphane dokumantasyonu
├── NE107 Esleme Tablosu (cihaz bazli, fabrika/proje konfigurasyonu)
│   └── Kritik nokta sapma gereklileri
└── Sertifikasyon Kanitlari (ISASecure CSA/SDLA, PLCopen CL/RL)
```

Bu belge hiyerarşisi proje başında kurulmadığında devreye alma sonrasında tamamlanmak zorunda kalınır — ki bu hem zaman kaybı hem de denetim riski demektir.

**Sentez Notu 6 — Üç Standardın Ortak Açık Sözü: "En Zayıf Halka"**
Uzman bir gözle bakıldığında üç standart da aynı sistemik gerçeği farklı dillerde söyler. IEC 61131-3'te tek bir üreticiye-özgü pointer kullanımı tüm kod tabanının taşınabilirliğini bozar. IEC 62443'te yedi FR'den en zayıfı tüm Zone'un SL'sini belirler (vektörün minimumu). NE107'de tesisteki en eski, eşleme yapmayan cihaz tüm diagnostik olgunluğun tavanını çizer. Bu örtüşme tesadüf değildir: üçü de "güvenlik/kalite/taşınabilirlik, ortalamayla değil en kötü bileşenle ölçülür" ilkesini paylaşır. Pratik sonuç — proje değerlendirmesinde "ortalama uyum yüzdesi" yanıltıcıdır; her zaman zincirin en zayıf halkasını arayın.

**Sentez Notu 7 — PA-DIM, Üç Standardın Kesişim Noktasıdır**
PA-DIM (FieldComm Group) OPC UA Information Model, NAMUR NE107'yi doğrudan kaynak olarak tanımlar ve NE107 statüsünü standart bir OPC UA node olarak sunar. IEC 62443 FR5 (Kısıtlı Veri Akışı) kapsamında PA-DIM trafiği Conduit politikasına tabidir. IEC 61131-3 yazılımı ise OPC UA client kütüphanesiyle PA-DIM node'larını Function Block girişi olarak okuyabilir. Bu üçünün kesişim noktasını bilinçli tasarlayan sistemler, üretici bağımsız diagnostik ve güvenli veri akışını aynı anda elde eder.

## İlgili Konular

```
knowledge/standards/                    <- Su an buradasiniz
├── 01_iec61131_3.md                   -> PLC yazilim standardi — tam detay
├── 02_iec62443.md                     -> Endustriyel siber guvenlik — tam detay
├── 03_namur_ne107.md                  -> Saha cihazi diagnostigi — tam detay
└── _synthesis.md (bu belge)

Yazilim tarafi:
knowledge/codesys/fundamentals/
└── _synthesis.md                      -> CODESYS temel sentezi; 61131-3'un
                                          runtime+proje+dil entegrasyonu

Guvenlik tarafi:
knowledge/networking/
└── 02_security.md                     -> OT ag guvenligi; Zone/Conduit ag uygulamasi

knowledge/protocols/opc-ua/
└── 03_security.md                     -> OPC UA guvenlik profilleri; FR1-FR4 karsilama

Diagnostik ve HMI tarafi:
knowledge/hmi/architecture/
└── 03_alarm_management.md             -> ISA-18.2 alarm yonetimi; NE107 sinyallerinin
                                          alarm kategorilerine atanmasi

knowledge/protocols/opc-ua/
└── 02_address_space.md               -> OPC UA address space; PA-DIM/NE107 entegrasyonu

Iliskili harici standartlar (bu proje kapsaminda belge yok):
  IEC 61508/61511                     -> Fonksiyonel guvenlik (SIL) — 62443'u tamamlar
  IEC 62769 (FDI)                     -> Field Device Integration; EDD tabanli NE107 esleme
  PA-DIM (FieldComm Group)            -> OPC UA tabanli cihaz bilgi modeli
  FF-912                              -> FOUNDATION fieldbus diagnostik profili
  ISA-18.2 / EEMUA 191               -> Alarm yonetimi standardi
  ISO 27001                           -> IT guvenlik yonetim sistemi; 62443 ile tamamlayici
  NIS2 Direktifi (AB)                 -> 62443'u teknik uyum yolu olarak kabul eder
```
