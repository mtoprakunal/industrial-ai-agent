---
KONU        : InoProShop Genel Bakış
KATEGORİ    : inovance
ALT_KATEGORI: inoproshop
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.inovance.eu/news/details/inovance-has-worked-with-codesys-since-2015-is-now-listed-on-the-codesys-website-173"
    başlık: "Inovance — CODESYS ile 2015'ten beri çalışıyor (resmi haber)"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/products/motion-controllers-i/o-modules/am600-motion-controllers"
    başlık: "Inovance — AM400/AM600 Motion Controllers"
    güvenilirlik: resmi
  - url: "https://www.manualslib.com/manual/1812322/Inovance-Am600-Series.html?page=119"
    başlık: "Inovance AM600 Series Hardware Manual — Programming Environment (InoProShop, Win7/Win10)"
    güvenilirlik: topluluk
  - url: "https://idea-tech.in/wp-content/uploads/2020/04/INOVANCE-AM400AM600AC800-PLC-SOFTWARE-MANUAL-ENGLISH-20-4-20.pdf"
    başlık: "Inovance — AM400/AM600/AC800 Medium-Sized PLC Software (InoProShop) User Guide"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: gerektirir
  - konu: "02_project_structure.md"
    ilişki: detaylandırır
  - konu: "08_codesys_to_inoproshop.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "CODESYS V3 runtime ve geliştirme ortamı kavramı (knowledge/codesys/fundamentals/)"
  - "IEC 61131-3 temel kavramları (POU, Task, GVL)"
ÇELİŞKİLER :
  - kaynak: "Kullanıcı talebi: 'InoProShop H5U'yu programlar'"
    konu: "H5U/H3U/Easy serisi InoProShop ile DEĞİL, Inovance AutoShop ile programlanır"
    çözüm: >
      Doğrulanmış olgu: InoProShop yalnızca AM400 / AM600 / AC800 (orta-sınıf,
      CODESYS V3 tabanlı) kontrolörler içindir. H5U/H3U/Easy küçük PLC'leri
      Inovance'ın kendi AutoShop ortamını (CODESYS DEĞİL; LD/IL/SFC) kullanır.
      Bu belge tabanı InoProShop = CODESYS gerçeğine dayanır; H5U bilinçli olarak
      kapsam dışıdır (bkz. 04_hardware_configuration.md'deki uyarı).
---

## Özün Ne

InoProShop, Inovance'ın orta-sınıf PLC ve motion kontrolörlerini (AM400, AM600, AC800)
programlamak için kullandığı geliştirme ortamıdır. **Özü itibarıyla CODESYS V3'tür**:
Inovance 2015'ten beri CODESYS GmbH ile çalışır ve InoProShop, CODESYS Development
System çekirdeği üzerine inşa edilmiş, Inovance'a özel cihaz tanımları, motion
kütüphaneleri ve EtherCAT yığını eklenmiş bir türevdir. Bu yüzden CODESYS V3 bilen bir
mühendis InoProShop'ta neredeyse hiç öğrenme eğrisi yaşamaz — menüler, IEC 61131-3
dilleri, Device tree, Library Manager ve online debug mantığı birebir CODESYS'tir.

Neden önemli: Inovance otomasyon donanımı (özellikle AM600 motion + SV660/IS620 servo +
GL20 I/O EtherCAT ekosistemi) Avrupa ve Türkiye'de yaygınlaşıyor. Bu donanımı verimli
kullanmanın yolu InoProShop'tur ve CODESYS bilgisi doğrudan transfer olur.

## Nasıl Çalışır

InoProShop, CODESYS V3 mimarisini miras alır:

- **Geliştirme ortamı (IDE):** CODESYS Development System tabanlı. Aynı pencere düzeni,
  POU editörleri, derleyici ve online görünüm.
- **Runtime:** Hedef kontrolör (AM600 vb.) bir CODESYS Control runtime çalıştırır.
  Inovance bunu kendi firmware'ine gömer.
- **Cihaz açıklamaları:** Inovance kontrolörleri, servo sürücüleri ve I/O modülleri
  InoProShop'a Device Repository üzerinden (Inovance'a özel device description + EtherCAT
  ESI dosyaları) tanıtılır.
- **Motion:** AM600, PLCopen motion (MC_*) kütüphanesi ve EtherCAT master yığınıyla
  32 eksene kadar (8 eşzamanlı interpolasyon/CAM) kontrol sağlar.

Pratik fark CODESYS'in jenerik dağıtımına kıyasla "marka kilitli" bir dağıtım olmasıdır:
cihaz havuzu Inovance ürünleriyle önceden doludur, üçüncü taraf cihazlar ESI/GSDML ile
yine eklenebilir.

## Pratikte Nasıl Kullanılır

1. **Kurulum:** InoProShop'u Inovance resmi indirme sayfasından (`inovance.eu/downloads`)
   indir. Windows 7 / Windows 10 desteklenir. Kurulum CODESYS tabanlı IDE + Inovance
   cihaz havuzu + motion/EtherCAT bileşenlerini getirir.
2. **Lisanslama:** IDE genellikle ücretsizdir (CODESYS dağıtımlarında olduğu gibi).
   Ücretli olan, hedef runtime üzerindeki bazı opsiyonel işlev lisanslarıdır (örn. ek
   eksen, belirli kütüphaneler) — kesin lisans modeli sürüme ve ürüne göre değişir,
   Inovance ile teyit edilmelidir (bu belgede tahmin edilmedi).
3. **Proje aç:** Hedef cihazı (AM400/AM600/AC800) seç, Device tree oluştur, task ve
   POU'ları ekle (bkz. 02_project_structure.md).
4. **İndir & çalıştır:** Ethernet üzerinden kontrolöre bağlan, login ol, programı indir,
   online debug yap (bkz. 09_debugging.md).

## Örnekler

- **AM600 motion projesi:** EtherCAT master altında SV660N servolar + GL20 I/O; PLCopen
  MC_Power/MC_MoveAbsolute ile eksen kontrolü. (bkz. 05, 06)
- **AM400 kompakt kontrol:** Dahili 16 HSC DI / 8 HS DO + CAN + RS485 Modbus RTU ile
  hızlı makine kontrolü.
- **CODESYS'ten taşıma:** Mevcut bir CODESYS V3 mantığının (ST POU'ları, GVL) InoProShop'a
  aktarılması (bkz. 08).

## Sık Yapılan Hatalar

- **InoProShop ile AutoShop'u karıştırmak.** En yaygın hata. H5U/H3U/Easy projesini
  InoProShop'ta açmaya çalışmak çalışmaz — onlar AutoShop'a aittir. Önce hedef ürünü
  doğru ortamla eşle.
- **"CODESYS değil" sanmak.** InoProShop'u tamamen ayrı bir araç sanıp CODESYS bilgisini
  kullanmamak zaman kaybıdır; kavramların %95'i ortaktır.
- **Sürüm uyumu:** InoProShop sürümü ile kontrolör firmware'i uyumlu olmalı; uyumsuz
  sürüm indirme/derleme hatalarına yol açar.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih:** Donanım Inovance AM400/AM600/AC800 ise; özellikle Inovance EtherCAT servo +
  I/O ekosistemiyle motion uygulaması yapılıyorsa. Maliyet avantajı + CODESYS tanıdıklığı.
- **Etme:** Donanım H5U/H3U/Easy ise (AutoShop kullan). Çoklu marka, vendor-bağımsız bir
  CODESYS projesi gerekiyorsa jenerik CODESYS + ilgili device paketleri daha esnek olabilir.

## Gerçek Proje Notları

- CODESYS deneyimli ekipler InoProShop'a geçişte neredeyse eğitim gerektirmez; en büyük
  sürtünme cihaz havuzu/ESI yönetimi ve sürüm uyumudur.
- Bu belgedeki InoProShop-CODESYS eşlemesi güçlü kaynaklı bir olgudur; ancak proje-içi
  ince ayrıntılar (lisans kalemleri, sürüme özgü menü farkları) doğrudan Inovance
  dokümanından teyit edilmelidir. Olgunluk seviyesi "Orta" olarak işaretlenmiştir.

## İlgili Konular

- `02_project_structure.md` — InoProShop proje/dosya yapısı
- `08_codesys_to_inoproshop.md` — CODESYS'ten taşıma
- `knowledge/codesys/fundamentals/` — temel CODESYS bilgisi (taban)
