---
KONU        : InoProShop'ta IEC 61131-3 ve CODESYS'ten Kod Taşıma
KATEGORİ    : inovance
ALT_KATEGORI: inoproshop
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.inovance.eu/news/details/inovance-has-worked-with-codesys-since-2015-is-now-listed-on-the-codesys-website-173"
    başlık: "Inovance — CODESYS ile 2015'ten beri çalışıyor (resmi haber)"
    güvenilirlik: resmi
  - url: "https://idea-tech.in/wp-content/uploads/2020/04/INOVANCE-AM400AM600AC800-PLC-SOFTWARE-MANUAL-ENGLISH-20-4-20.pdf"
    başlık: "Inovance — AM400/AM600/AC800 Medium-Sized PLC Software (InoProShop) User Guide (IEC 61131-3 / CODESYS dilleri)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_cmd_export_plcopenxml.html"
    başlık: "CODESYS Online Help — Command: Export PLCopenXML"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_project_export_import.html"
    başlık: "CODESYS Online Help — Exporting and Importing Projects (.export, PLCopenXML)"
    güvenilirlik: resmi
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/codesys-pou-importexport-between-abb-and-schneider-brands"
    başlık: "CODESYS POU Import/Export Between Brands via PLCopenXML — Industrial Monitor Direct"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/codesys/fundamentals/03_iec61131_languages.md"
    ilişki: gerektirir
  - konu: "02_project_structure.md"
    ilişki: gerektirir
  - konu: "01_inoproshop_overview.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/libraries/standard_libraries.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "IEC 61131-3 dilleri: ST, LD, FBD, SFC (ve IL/CFC) — CODESYS tabanı (knowledge/codesys/fundamentals/03_iec61131_languages.md)"
  - "InoProShop proje yapısı: Application, POU, Library Manager, Device Repository (02_project_structure.md)"
  - "InoProShop = CODESYS V3 türevi gerçeği (01_inoproshop_overview.md)"
ÇELİŞKİLER :
  - kaynak: "'CODESYS projesi InoProShop'ta doğrudan açılır' beklentisi"
    konu: >
      InoProShop ile jenerik CODESYS aynı V3 çekirdeğini paylaşsa da, bir projenin sorunsuz
      açılması sürüm uyumuna ve özellikle VENDOR'a özgü kütüphane/cihaz tanımlarına bağlıdır.
    çözüm: >
      IEC mantığı (ST/LD/FBD/SFC POU'ları, GVL, DUT) yüksek oranda uyumludur. Asıl uyumsuzluk
      kaynağı: cihaza özel FB'ler, vendor kütüphaneleri, fieldbus/ESI tanımları ve doğrudan
      adresleme. Tam proje taşıma yerine POU/obje düzeyinde taşıma (PLCopenXML / .export) ve
      hedef cihaza yeniden bağlama önerilir.
  - kaynak: "PLCopenXML 'her şeyi taşır' yanılgısı"
    konu: "PLCopenXML CODESYS'te kütüphaneleri ve cihaz konfigürasyonunu TAŞIMAZ; %100 uyum garanti değildir"
    çözüm: >
      PLCopenXML yalnızca POU/GVL/DUT gibi kod öğelerini taşır; kütüphane bağımlılıkları ve
      Device tree/I/O Mapping hedefte yeniden kurulmalıdır.
---

## Özün Ne

InoProShop, IEC 61131-3 dillerini **CODESYS V3 ile birebir aynı editörler ve aynı semantikle**
sunar: ST (Structured Text), LD (Ladder), FBD (Function Block Diagram), SFC (Sequential
Function Chart), ayrıca IL (deprecated) ve CODESYS'e özgü CFC. Bir POU oluştururken dil seçilir,
diller bir projede serbestçe karıştırılır — tıpkı CODESYS'te olduğu gibi. Bu yüzden dil bilgisi
ve dil-seçim rehberi doğrudan CODESYS bilgi tabanından
(`knowledge/codesys/fundamentals/03_iec61131_languages.md`) transfer olur.

İkinci konu: **CODESYS'ten InoProShop'a kod taşıma.** Aynı V3 çekirdeği sayesinde saf IEC
mantığı büyük oranda uyumludur; ancak vendor kütüphaneleri, cihaza özel FB'ler ve fieldbus
tanımları taşımada en kritik sürtünme noktalarıdır. Bu belge neyin taşındığını, neyin
taşınmadığını ve nelere dikkat edileceğini netleştirir.

## Nasıl Çalışır

### IEC 61131-3 Dilleri InoProShop'ta

InoProShop, CODESYS Development System çekirdeğini kullandığından dil davranışları aynıdır.
Özet karşılaştırma için CODESYS belgesindeki tam matris geçerlidir; burada InoProShop bağlamı:

| Dil | InoProShop'ta Durum | Tipik Inovance Kullanımı |
|---|---|---|
| **ST** | Tam destek; OOP (METHOD/INTERFACE/EXTENDS) yalnızca ST'de | Motion mantığı (MC_* sarmalama), algoritma, iletişim |
| **LD** | Tam destek | Saha okunabilir interlock, basit DI/DO devreleri |
| **FBD** | Tam destek | Analog/PID sinyal akışı görselleştirme |
| **SFC** | Tam destek | Makine döngüsü/sekans; adımların online izlenmesi |
| **IL** | Destekli ama deprecated | Yeni projede kullanılmamalı; ST'ye dönüştürülmeli |
| **CFC** | Destekli (CODESYS'e özgü, IEC dışı) | Serbest yerleşim/geri besleme; taşınabilirliği düşük |

Dil seçimi POU oluşturulurken `Add Object > POU > Implementation language` ile yapılır
(CODESYS ile aynı akış). Kritik kurallar da aynen geçerlidir:

- **Function** türü POU **SFC** olamaz (durumsuz fonksiyon, adım/geçiş yapısına uymaz).
- POU dili oluşturulduktan sonra menüden doğrudan değiştirilemez; yeniden yazım gerekir →
  dil seçimini baştan doğru yap.
- Kararsızsan **ST ile başla**: tüm yapı taşlarını destekler, OOP için tek seçenektir,
  Git diff/merge ve birim teste en uygun dildir.

Tüm dil-özel tuzaklar (REAL eşitlik karşılaştırması, timer'ı koşulsuz çağırma, çoklu coil,
SFC transition'da yan etki, CFC execution order, kısa devre garanti olmaması) InoProShop'ta
da **aynen** geçerlidir — bunlar CODESYS derleyici semantiğinden gelir, vendor'dan değil
(detay: `knowledge/codesys/fundamentals/03_iec61131_languages.md` Gerçek Proje Notları).

### Inovance'a Özgü Tek Fark: Kütüphane ve FB Havuzu

Dil semantiği aynı olsa da InoProShop ile gelen **kütüphane ve cihaz FB havuzu** Inovance'a
özeldir: PLCopen motion (MC_Power, MC_MoveAbsolute, MC_MoveVelocity, CAM/Gear FB'leri),
Inovance servo (SV660/IS620) ve GL20 I/O için cihaza özel FB'ler, Inovance iletişim
kütüphaneleri. Saf IEC mantığı taşınabilir; ama bu vendor FB'lerine yapılan çağrılar yalnızca
karşılık gelen kütüphane hedef ortamda varsa derlenir.

## Pratikte Nasıl Kullanılır — CODESYS'ten InoProShop'a Kod Taşıma

### Taşıma Yöntemleri

1. **Obje düzeyinde export/import (önerilen):** Kaynak CODESYS projesinde taşınacak POU/GVL/DUT'ları
   `.export` (CODESYS native, referans bütünlüğü daha iyi korunur) veya **PLCopenXML** ile dışa
   aktar; InoProShop'ta hedef Application'a import et. Vendor-bağımsız, temiz IEC mantığı için
   en güvenli yol.
2. **Tam proje taşıma:** Aynı V3 çekirdeği nedeniyle mümkün olabilir; ancak sürüm uyumuna ve
   vendor kütüphane/cihaz tanımlarının InoProShop'ta bulunmasına bağlıdır. Riskli; her zaman
   sorunsuz açılacağı garanti edilemez (bkz. ÇELİŞKİLER).
3. **Kütüphane yeniden bağlama:** İş mantığı dahili kütüphanelerde (`.library`) ise, kütüphaneyi
   InoProShop'a kurup projeden sürüm-sabit referansla kullan.

### Uyumlu Yapılar (sorunsuz taşınır)

- ST/LD/FBD/SFC ile yazılmış saf IEC mantığı (IF/CASE/FOR, state machine, boolean interlock).
- GVL, DUT (STRUCT/ENUM/ALIAS), kullanıcı tanımlı FB ve FC'ler (vendor FB çağırmıyorsa).
- Standart CODESYS kütüphane çağrıları (TON/TOF/CTU, Util FIFO vb.) — InoProShop bu standart
  kütüphaneleri içerir.
- OOP yapıları (INTERFACE, METHOD, PROPERTY) — ST tabanlı, çekirdek özelliği.

### Olası Uyumsuzluklar (dikkat / yeniden kurulum gerekir)

- **Vendor'a özel kütüphaneler:** Kaynak proje Beckhoff/WAGO/Schneider/Siemens'e özgü
  kütüphane FB'leri çağırıyorsa, InoProShop'ta bu kütüphaneler yoktur → derleme hatası. Inovance
  eşdeğeriyle (örn. motion için MC_* / Inovance FB) değiştirilmeli.
- **Cihaza özel FB'ler:** Hedef donanımın native FB'leri (örn. başka bir markanın eksen/IO FB'i)
  Inovance donanımında karşılığı olmadan çalışmaz; Inovance servo/I/O FB'leriyle yeniden yazılır.
- **Fieldbus / Device tree / I/O Mapping:** Bunlar PLCopenXML ile **taşınmaz**. Device tree
  InoProShop'ta yeniden kurulur (Inovance kontrolör + ESI ile servo/I/O), I/O Mapping yeniden
  yapılır. Doğrudan `AT %` adreslemeleri sembolik mapping'e taşınmalı (topoloji farkı adres kaydırır).
- **CFC POU'ları:** IEC dışı; PLCopenXML ile temiz taşınmaz. Taşınabilirlik gerekiyorsa FBD/ST.
- **Sürüm / firmware farkları:** Kaynak ve hedef V3 sürümleri ile InoProShop↔firmware uyumu
  derleme/indirme davranışını etkiler.
- **PLCopenXML'in kapsam sınırı:** Yalnızca kod öğelerini taşır; kütüphane bağımlılıkları ve
  cihaz konfigürasyonu hedefte yeniden kurulmalıdır. %100 uyum garanti değildir.

### Dikkat Edilecekler (taşıma checklist'i)

1. Taşınacak POU'ların **vendor FB bağımlılığını** önce tara; vendor çağrılarını işaretle.
2. Saf IEC mantığını `.export`/PLCopenXML ile aktar.
3. InoProShop'ta gerekli **kütüphaneleri** Library Manager'a sürüm-sabit ekle.
4. **Device tree + EtherCAT + I/O Mapping**'i hedefte yeniden kur (taşınmaz).
5. **Doğrudan adresleri** sembolik mapping'e dönüştür.
6. Vendor/cihaz FB çağrılarını **Inovance eşdeğerleriyle** değiştir.
7. Derle, statik analiz uyarılarını incele, **simülasyon + saha testi** yap (özellikle motion).

## Örnekler

### Örnek 1 — Taşınabilir IEC mantığı (sorunsuz)

```iecst
(* Vendor-bağımsız state machine — CODESYS'ten InoProShop'a olduğu gibi taşınır *)
FUNCTION_BLOCK FB_Conveyor
VAR_INPUT
    xStart : BOOL; xStop : BOOL;
END_VAR
VAR_OUTPUT
    xRun : BOOL; eState : E_ConvState;
END_VAR
VAR
    tDelay : TON;   (* standart kütüphane — her iki ortamda var *)
END_VAR

CASE eState OF
    eIdle:    IF xStart THEN eState := eRunning; END_IF
    eRunning: xRun := TRUE; IF xStop THEN eState := eIdle; END_IF
END_CASE
```

### Örnek 2 — Vendor FB değişimi gerektiren mantık

```iecst
(* Kaynak (başka marka): markaya özel eksen FB'i — InoProShop'ta YOK *)
fbAxis( Enable := TRUE, Position := 100.0 );   (* derlenmez: kütüphane eksik *)

(* InoProShop hedefi: Inovance PLCopen MC_* ile yeniden yaz *)
mcPower(  Axis := Axis1, Enable := TRUE );
mcMoveAbs(Axis := Axis1, Execute := xGo, Position := 100.0, Velocity := 200.0 );
```

## Sık Yapılan Hatalar

- **"CODESYS projesi olduğu gibi açılır" sanmak.** Saf mantık taşınır; vendor kütüphaneleri,
  cihaz FB'leri ve Device tree/I/O Mapping taşınmaz veya yeniden kurulmalıdır.
- **PLCopenXML'in kütüphane/cihaz taşıdığını sanmak.** Taşımaz; yalnızca POU/GVL/DUT.
- **Doğrudan `AT %` adreslerini taşıyıp test etmemek.** Hedef topoloji farklıdır, adres kayar,
  yanlış kanallar sürülür (tehlikeli) — sembolik mapping kullan.
- **Motion FB'lerini test etmeden devreye almak.** Vendor FB → MC_* dönüşümünü mutlaka
  simülasyon ve kontrollü saha testiyle doğrula.
- **CFC POU'larının temiz taşınmasını beklemek.** Taşınabilirlik için FBD/ST tercih et.
- **IL kodunu olduğu gibi taşımak.** Deprecated; CODESYS/InoProShop otomatik ST dönüştürücüsüyle
  çevir, gözden geçir, test et.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Taşımayı tercih et:** Mevcut CODESYS iş mantığı (algoritma, sekans, FB kütüphaneleri)
  vendor-bağımsızsa ve donanım Inovance'a geçiyorsa. Obje-düzeyi export ile temiz aktarım yap.
- **Yeniden yazmayı tercih et:** Mantık ağırlıklı olarak başka markanın cihaz/motion FB'lerine
  bağlıysa; bu durumda taşımak yerine Inovance MC_* / cihaz FB'leriyle yeniden kurmak daha
  temizdir.
- **Tam proje taşımadan kaçın:** Sürüm/vendor bağımlılığı belirsizse; obje-düzeyi taşıma + hedefte
  Device tree yeniden kurulum daha öngörülebilirdir.

## Gerçek Proje Notları

- En sık yaşanan sürpriz: kod "derlenmiyor" sanılır, oysa sorun **eksik vendor kütüphanesi** veya
  **yeniden kurulmamış Device tree/I/O Mapping**tir — IEC mantığının kendisi sağlamdır.
- **Motion taşıması en kritik kısımdır.** Eksen FB'leri marka-özeldir; MC_* eşlemesi mekanik
  limitler, ölçek ve emniyet açısından her zaman simülasyon + denetimli saha testi gerektirir.
- Taşınabilirliği baştan tasarlamak öder: iş mantığını **vendor-bağımsız FB/kütüphanelere**
  ayır, donanıma dokunan ince katmanı (motion/I/O) izole et. Böylece CODESYS↔InoProShop geçişi
  yalnızca ince katmanı yeniden bağlamaya indirgenir.
- Olgunluk "Orta": dil semantiği güçlü kaynaklı bir olgudur; ancak sürüme/InoProShop dağıtımına
  özgü kütüphane adları ve menü farkları kurulu yazılımdan/Inovance dokümanından teyit edilmelidir.

## İlgili Konular

- `knowledge/codesys/fundamentals/03_iec61131_languages.md` — IEC dillerinin tam derinlemesine
  rehberi (dil matrisi, dil-özel tuzaklar, dil seçim rehberi) — bu belgenin tabanı
- `02_project_structure.md` — Device tree, Library Manager, Device Repository (taşımada yeniden
  kurulan yapılar)
- `01_inoproshop_overview.md` — InoProShop = CODESYS V3 türevi (taşımanın neden mümkün olduğu)
- `knowledge/codesys/libraries/standard_libraries.md` — her iki ortamda ortak standart kütüphaneler
