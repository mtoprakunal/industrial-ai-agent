---
KONU        : CODESYS Forge ve CODESYS Store Örnek Projeleri
KATEGORİ    : examples
ALT_KATEGORI: open-source
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://forge.codesys.com/prj/"
    başlık: "CODESYS Forge — açık kaynak proje portalı (proje listesi)"
    güvenilirlik: resmi
  - url: "https://forge.codesys.com/prj/codesys-example/home/Home/"
    başlık: "CODESYS Forge — CODESYS Examples (resmi örnek projeler kümesi)"
    güvenilirlik: resmi
  - url: "https://store.codesys.com/en/oscat-basic.html"
    başlık: "CODESYS Store — ürün/örnek dağıtım sayfası örneği"
    güvenilirlik: resmi
  - url: "https://us.store.codesys.com/examples.html"
    başlık: "CODESYS Store — Free Examples, Snippets"
    güvenilirlik: resmi
  - url: "https://forge.codesys.com/lib/counit/home/Home/"
    başlık: "CODESYS Forge — co♻e unittest framework (CfUnit) topluluk projesi"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/codesys/programming/04_libraries.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/networking/01_opcua_server.md"
    ilişki: tamamlar
  - konu: "01_oscat_library.md"
    ilişki: tamamlar
  - konu: "03_github_iec61131_projects.md"
    ilişki: alternatif
ÖNKOŞUL     :
  - "CODESYS projesi açma, kütüphane ekleme (knowledge/codesys/programming/04_libraries.md)"
  - "Visualization/HMI ve Task kavramları (temel CODESYS bilgisi)"
ÇELİŞKİLER :
  - kaynak: "Kavram karışıklığı: 'CODESYS Store = CODESYS Forge'"
    konu: "Store ve Forge aynı şey değildir"
    çözüm: >
      Doğrulanmış olgu: CODESYS Store, CODESYS GmbH'nin işlettiği ticari pazar
      yeridir (ücretli ürünler + ÜCRETSİZ örnek/snippet'ler). CODESYS Forge ise
      açık kaynak topluluk portalıdır; buradaki tüm projeler CODESYS ile
      yapılmış ve herkese ÜCRETSİZ açık olmak zorundadır, ayrıca "CODESYS Talk"
      forumunu barındırır. Store ücretsiz örnekleri çoğunlukla Forge'a yönlendirir.
---

## Özün Ne

CODESYS ekosisteminde hazır, çalışan örnek projelere ve topluluk kütüphanelerine ulaşmanın iki
ana resmi kapısı vardır: **CODESYS Store** ve **CODESYS Forge**. Store, CODESYS GmbH'nin ticari
mağazasıdır — ücretli eklentilerin yanı sıra çok sayıda **ücretsiz örnek proje ve snippet**
barındırır; bir özelliği "denemek" için en hızlı yoldur. Forge ise **açık kaynak topluluk
portalıdır**: yüzlerce (yazım anında ~269) proje, kütüphane, sürücü ve örnek burada herkese
ücretsiz açık şekilde paylaşılır ve "CODESYS Talk" forumu da burada yer alır.

Neden önemli: Bir agent veya mühendis için bunlar "öğreten örnekler" hazinesidir. Bir HMI'ın
nasıl kurulduğunu, trend kaydının nasıl yapıldığını, MQTT/Sparkplug ile IIoT bağlantısının
nasıl gerçekleştiğini veya birim testin nasıl yazıldığını, teoriyle değil **gerçek, açılıp
incelenebilir proje arşivleriyle** gösterirler. Doğru örneği bulmak, sıfırdan yazmaktan kat kat
hızlıdır.

## Nasıl Çalışır

**CODESYS Store** (store.codesys.com / us.store.codesys.com):
- CODESYS GmbH tarafından işletilen resmi mağaza. Ürünler indirilebilir paketler halindedir.
- İçeriğin önemli bir kısmı **ücretsiz** örnek proje/snippet'tir; amaç desteklenen teknolojileri
  (motion, vizualizasyon, ağ, OPC UA vb.) kolayca denetmektir.
- OSCAT BASIC gibi topluluk kütüphaneleri de Store üzerinden ücretsiz dağıtılır.
- Store, en güncel sürümler ve daha fazla ücretsiz örnek için sıklıkla Forge'a yönlendirir.

**CODESYS Forge** (forge.codesys.com):
- Açık kaynak topluluk portalı. Kuralı net: burada listelenen her proje CODESYS ile yapılmış
  olmalı ve herkese ücretsiz açık olmalı.
- Projeler türlerine göre düzenlenir: **tools, libraries, drivers, standart/örnek projeler**.
- "CODESYS Talk" forumu (forum.codesys.com) mühendislik tartışmaları için buradadır.
- Resmi "CODESYS Examples" kümesi burada yaşar: HMI Example, Trend Example, Element Collections
  Examples, NetBaseServices (NBS) Example, Visu Demo Factory gibi.

Forge'daki dikkat çeken topluluk projeleri arasında: IEC 61131-3 birim test çatısı
(co♻e/CfUnit), MQTT/Sparkplug B IIoT entegrasyonu, JSON ayrıştırma kütüphanesi, dosya/XML
yönetimi, donanım-bağımsız debug logger ve SoftMotion sürücü örnekleri bulunur.

## Pratikte Nasıl Kullanılır

1. **Ne aradığını netleştir:** Bir teknoloji mi denemek istiyorsun (örn. OPC UA sunucu, trend,
   MQTT) yoksa hazır bir kütüphane mi (JSON, unittest, dosya işleme)?
2. **Önce Store'a bak (teknoloji denemesi için):** us.store.codesys.com/examples üzerinden
   ücretsiz örnekleri tara; ilgili `.project`/proje arşivini indir.
3. **Forge'a bak (kütüphane/topluluk projesi için):** forge.codesys.com/prj/ üzerinde tür
   (tools/libraries/drivers) ve anahtar kelimeyle ara. Proje sayfasında genellikle indirme,
   wiki/dokümantasyon ve forum bağlantısı vardır.
4. **Projeyi aç:** İndirilen arşivi CODESYS'te aç (sürüm uyumuna dikkat — örnek hangi CODESYS
   sürümünde yapıldıysa o sürümde sorunsuz açılır). Kütüphane bağımlılıkları varsa Library
   Repository'ye kur (bkz. 04_libraries.md).
5. **İncele ve uyarla:** Örneğin Device/Task ağacını, GVL'lerini, FB'lerini incele; kendi
   projene yalnızca gereken pattern'i/POU'yu taşı. Telifli/lisanslı içerikte ilgili lisans
   koşuluna uy.

## Örnekler

Forge'daki resmi "CODESYS Examples" kümesinden öğretici projeler:

- **HMI Example (HMIDemo.project):** Bir CODESYS V3 kontrolörü ile bir HMI'ı birbirine bağlar;
  CODESYS HMI istemcisinin nasıl kurulduğunu gösterir.
- **Trend Example:** "Trend" görselleştirme elemanıyla değerlerin nasıl kaydedildiğini ve
  görselleştirildiğini gösterir.
- **Visu Demo Factory:** Bir paketleme sisteminin görselleştirmesini içeren proje arşivi;
  mevcut vizualizasyon elemanlarını sergiler — HMI tasarımı öğrenmek için zengin bir kaynak.
- **Element Collections Examples:** "Element Collections" kütüphanesinin kullanımını gösterir.
- **NetBaseServices (NBS) Example:** Soket/ağ tabanlı temel servislerin (NBS) nasıl kullanıldığını
  gösterir — kendi TCP/UDP iletişimini yazarken referans.

Topluluk (Forge libraries) örneklerinden:
- **co♻e / CfUnit:** IEC 61131-3 birim test çatısı — FB'leri test etmenin somut deseni.
- **Sparkplug™ MQTT edge:** CODESYS + MQTT ile IIoT veri yayını.
- **JSON parsing library:** Yapısal veri ayrıştırma.

(Telifli proje kodu burada birebir aktarılmamıştır; yalnızca her örneğin ne öğrettiği
özetlenmiştir.)

## Sık Yapılan Hatalar

- **Store ile Forge'u karıştırmak.** Store = ticari mağaza (+ ücretsiz örnekler); Forge = açık
  kaynak topluluk portalı. Ücretsiz/güncel sürümler genelde Forge'dadır.
- **Sürüm uyumsuzluğu.** Örnek proje, yapıldığı CODESYS sürümünden eski bir IDE'de açılmaz veya
  uyarı verir; yanlış sürümde açıp "bozuk" sanmak yaygın hata.
- **Eksik kütüphane bağımlılığı.** Örnek bir kütüphaneye dayanıyorsa, o kütüphane repository'de
  yoksa proje derlenmez. Forum/wiki'deki bağımlılık listesini kontrol et (bu, forumlarda en sık
  bildirilen "örnekteki kütüphaneler" sorunudur).
- **Lisansı kontrol etmeden ticari ürüne kopyalamak.** Forge projeleri ücretsiz açık olmak
  zorundadır ama her birinin kendi lisansı olabilir (MIT, OSCAT-tipi vb.); kullanmadan önce
  proje lisansını oku.
- **Örneği olduğu gibi sahaya almak.** Örnekler öğretmek için yazılır; üretim seviyesinde hata
  yönetimi, emniyet, ölçeklenebilirlik genelde basitleştirilmiştir.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih:** Yeni bir teknolojiyi (OPC UA, trend, MQTT, HMI) hızla öğrenmek/denemek; bir
  pattern'in resmi/topluluk referans uygulamasını görmek; hazır bir yardımcı kütüphaneyi (JSON,
  unittest, file handling) projeye katmak için. Sıfırdan yazmadan önce ilk durak olmalı.
- **Etmemeli:** Sertifikalı emniyet (SIL) işlevi için — örnekler garanti/sertifika içermez.
  Üretici destekli, SLA gerektiren kritik altyapıda topluluk projesi yerine vendor/SL ürünü
  tercih edilmeli. Ayrıca bir örnek uzun süredir bakımsızsa (eski sürüm, kapalı forum
  başlığı) ona bağımlı kalmak risklidir.

## Gerçek Proje Notları

- En verimli kullanım: örneği **çalıştırıp davranışı gözlemlemek**, sonra yalnızca ihtiyaç
  duyduğun deseni/POU'yu kendi projene taşımaktır — tüm örnek mimarisini kopyalamak yerine.
  Visu Demo Factory gibi projeler "hangi vizualizasyon elemanı ne işe yarar" sorusunu en hızlı
  cevaplayan kaynaktır.
- Forge'un asıl gücü forumla (CODESYS Talk) birleşmesidir: bir örnek çalışmazsa çoğu zaman aynı
  forum başlığında çözümü bulunur. Örnek + forum başlığını birlikte okumak izole proje arşivinden
  daha öğreticidir.
- Ekiplerin tekrar eden hatası, örnek projedeki **basitleştirilmiş hata yönetimini** üretime
  taşımaktır. Örneği bir "iskelet/öğretici" olarak görüp savunmacı programlama, emniyet ve
  diagnostik katmanını kendin eklemelisin (bkz. error_handling, function_blocks ELSE/fail-safe).
- Sürüm sabitleme önemli: bir örneği temel alıp ürünleştiriyorsan, kullandığın CODESYS sürümünü
  ve indirdiğin proje/kütüphane sürümünü kaydet; Forge/Store'da içerik güncellenince eski davranış
  kaybolabilir.

## İlgili Konular

- `01_oscat_library.md` — Store/Forge üzerinden dağıtılan en yaygın topluluk kütüphanesi
- `03_github_iec61131_projects.md` — Forge dışı (GitHub) açık kaynak ekosistem ve test/CI dersleri
- `knowledge/codesys/programming/04_libraries.md` — örnek projelerin kütüphane bağımlılıkları
- `knowledge/codesys/networking/01_opcua_server.md` — Store/Forge'daki OPC UA örnekleriyle ilişki
