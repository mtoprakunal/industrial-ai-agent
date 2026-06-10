---
KONU        : OSCAT Açık Kaynak PLC Kütüphanesi
KATEGORİ    : examples
ALT_KATEGORI: open-source
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "http://www.oscat.de/images/OSCATBasic/oscat_basic333_en.pdf"
    başlık: "OSCAT BASIC Library Documentation (English) — resmi proje dokümanı"
    güvenilirlik: resmi
  - url: "http://oscat.de/images/OSCATNetwork/oscat_netlib121_en.pdf"
    başlık: "OSCAT NETWORK Library Documentation (English)"
    güvenilirlik: resmi
  - url: "http://oscat.de/images/OSCATBuilding/oscat_building100_en.pdf"
    başlık: "OSCAT BUILDING Library Documentation (English)"
    güvenilirlik: resmi
  - url: "https://store.codesys.com/en/oscat-basic.html"
    başlık: "OSCAT BASIC — CODESYS Store (sürüm, sistem gereksinimi, lisans)"
    güvenilirlik: resmi
  - url: "https://github.com/stefandreyer/OSCAT-BASIC"
    başlık: "OSCAT BASIC — CODESYS V2.3'ten V3'e port (topluluk)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/codesys/programming/04_libraries.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/programming/03_function_blocks.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/networking/03_tcp_socket.md"
    ilişki: tamamlar
  - konu: "02_codesys_forge_store.md"
    ilişki: alternatif
ÖNKOŞUL     :
  - "CODESYS Library Manager ve kütüphane ekleme (knowledge/codesys/programming/04_libraries.md)"
  - "Function Block / Function kavramı (knowledge/codesys/programming/03_function_blocks.md)"
  - "IEC 61131-3 ST dili temelleri"
ÇELİŞKİLER :
  - kaynak: "Yaygın yanlış algı: 'OSCAT açık kaynak = MIT/GPL gibi OSI lisansı'"
    konu: "OSCAT'ın lisansı OSI onaylı bir açık kaynak lisansı değildir"
    çözüm: >
      Doğrulanmış olgu: OSCAT kendi özel (custom) lisansını kullanır — MIT veya GPL
      DEĞİL. Kullanım ücretsiz ve ticari kullanıma açık, kaynak kod değiştirilebilir,
      ancak yeniden dağıtım ÜCRETSİZ olmalı ve www.oscat.de'ye görünür atıf
      içermelidir. Donanıma gömülürse de OSCAT atfı zorunludur. Garanti yoktur.
      Yani "özgürce kullan ama sat-paketleyip-kapatma kuralları var" tipi bir lisans.
---

## Özün Ne

OSCAT (Open Source Community for Automation Technology), IEC 61131-3 standardına dayanan,
üretici-bağımsız (vendor-neutral) ücretsiz bir PLC kütüphanesi koleksiyonudur. Tek bir
satıcının özel fonksiyonlarına bağlı olmadığı için teorik olarak IEC 61131-3 uyumlu her
PLC'ye taşınabilir; pratikte en yaygın kullanımı CODESYS ve TwinCAT ortamlarındadır. Üç ana
kütüphaneden oluşur: **OSCAT BASIC** (genel amaçlı yardımcı fonksiyonlar), **OSCAT NETWORK**
(ağ/protokol blokları) ve **OSCAT BUILDING** (bina otomasyonu).

Neden önemli: OSCAT, "tekerleği yeniden icat etme" probleminin endüstriyel cevabıdır.
Bir mühendisin sıfırdan yazacağı string işleme, tarih/saat aritmetiği, sinyal filtreleme
veya FTP/SMTP istemcisi gibi yüzlerce hazır ve sahada denenmiş FB/fonksiyonu sunar. Aynı
zamanda **nasıl iyi kütüphane yazılır** sorusuna canlı bir referanstır: tutarlı isimlendirme,
saf fonksiyon (FUNCTION) ile durumlu FB ayrımı, kategorize edilmiş POU organizasyonu.

## Nasıl Çalışır

OSCAT, derlenmiş kapalı bir ürün değil, **kaynak kodu açık** IEC 61131-3 POU'larından oluşan
bir kütüphanedir. CODESYS'e `.library` / `.compiled-library` (veya eski V2.3 export) formatında
eklenir ve Library Manager üzerinden projeye dahil edilir (bkz. 04_libraries.md).

Üç kütüphanenin kapsamı:

- **OSCAT BASIC:** Tamamen donanım-bağımsız yardımcı fonksiyonlar. Başlıca kategoriler:
  - Buffer/array yönetimi (FIFO/LIFO, kaydırma, kopyalama)
  - Mühendislik fonksiyonları (ölçeklendirme, lineerizasyon, birim dönüşümleri)
  - Liste işleme
  - Mantık (bit işlemleri, kenar/darbe üreteçleri, çoklu seçiciler)
  - Matematik (istatistik, trigonometri yardımcıları, eğri/profil üreteçleri, basit kontrol/tuning yardımcıları)
  - String işleme (parçalama, birleştirme, arama, format)
  - Tarih/saat (takvim aritmetiği, gün/hafta/ay hesapları, güneş doğuş-batış gibi astronomik hesaplar)
- **OSCAT NETWORK:** Üst-katman ağ protokolü istemci/sunucu blokları. Belgelenen protokoller
  arasında **FTP, HTTP, SMTP (e-posta), SNTP (zaman senkronizasyonu) ve Telnet** bulunur.
  Bu bloklar alttaki TCP/UDP soket katmanını (platformun yığını) kullanır.
- **OSCAT BUILDING:** Bina otomasyonu (HVAC, aydınlatma, gölgeleme, takvim/zaman programları)
  için FB'ler; ısıtma eğrileri, konfor hesapları, astronomik saat tabanlı kontrol gibi.

Önemli mimari nokta: OSCAT donanım-bağımsızlığı hedefler, ama NETWORK kütüphanesi soket/yığın
gerektirdiğinden platformun ağ desteğine bağımlıdır — yani "%100 taşınabilir" iddiası
özellikle NETWORK için sınırlıdır. [DOĞRULANMADI: her protokol bloğunun her CODESYS hedefinde
sorunsuz çalıştığı — hedef firmware'in soket kütüphanesi desteğine bağlıdır.]

## Pratikte Nasıl Kullanılır

1. **Edin:** OSCAT BASIC en kolay yol CODESYS Store üzerinden ücretsiz indirilir
   (sürüm 3.3.5.0, Eylül 2024; CODESYS Development System ≥ 3.5.10.0 gerektirir).
   Resmi dağıtım ve dokümantasyon www.oscat.de adresindedir. BUILDING ve NETWORK de
   benzer şekilde Store/oscat.de üzerinden bulunur.
2. **Kur:** İndirilen paketi CODESYS'te **Tools → Library Repository → Install** ile
   repository'ye yükle.
3. **Projeye ekle:** Library Manager → **Add Library** → OSCAT'ı seç. Artık POU'lar
   namespace ile erişilebilir hale gelir.
4. **Kullan:** İhtiyacın olan FB/fonksiyonu çağır. Örneğin string parçalama veya bir
   ölçeklendirme fonksiyonu doğrudan kullanılabilir; durumlu bloklar (örn. zamanlayıcı
   tabanlı profil üreteçleri) her scan döngüsünde çağrılmalıdır (bkz. 03_function_blocks.md).
5. **Lisans atfını unutma:** Ürünü/donanımı dağıtırken OSCAT ve www.oscat.de atfını ekle.

Önemli kısıt: CODESYS Store'daki OSCAT BASIC paketi **32-bit platformları** destekler,
**64-bit kontrolörleri DESTEKLEMEZ**. 64-bit hedefte kullanım için topluluk port'ları veya
kaynaktan yeniden derleme gerekebilir. [DOĞRULANMADI: 64-bit destek durumunun sonraki
sürümlerde değişip değişmediği — resmi paket sayfasından teyit edilmeli.]

## Örnekler

- **String tabanlı reçete ayrıştırma:** Bir HMI'dan gelen ham string'i OSCAT BASIC'in
  string fonksiyonlarıyla parçalayıp sayısal parametrelere dönüştürmek — kendi parser'ını
  yazmaktan çok daha hızlı ve daha az hatalı.
- **Astronomik saat ile aydınlatma:** OSCAT BUILDING'in güneş doğuş/batış hesabıyla, sabit
  saat yerine coğrafi konuma göre dış aydınlatmayı tetiklemek.
- **PLC'den e-posta alarmı:** OSCAT NETWORK'ün SMTP bloğuyla, kritik bir alarmda
  doğrudan kontrolörden e-posta göndermek (harici gateway olmadan).
- **Zaman senkronizasyonu:** SNTP bloğuyla kontrolörün saatini bir NTP sunucusundan periyodik
  güncellemek.

(Bu belgede telifli OSCAT kaynak kodu birebir aktarılmamıştır; yalnızca hangi yeteneklerin
mevcut olduğu ve nasıl kullanıldığı özetlenmiştir.)

## Sık Yapılan Hatalar

- **Lisansı yanlış anlamak.** OSCAT'ı MIT/GPL gibi sanıp atıf koşulunu atlamak. Lisans
  ücretsiz ve ticari-dostu ama atıf (oscat.de referansı) ve "yeniden dağıtım ücretsiz olmalı"
  koşulları gerçektir.
- **64-bit kontrolörde Store paketini kullanmaya çalışmak.** Store'daki BASIC paketi 32-bit
  içindir; 64-bit hedeflerde derleme/yükleme sorunu çıkar.
- **NETWORK bloklarının her hedefte çalışacağını varsaymak.** Protokol blokları platformun
  soket/yığın desteğine bağlıdır; bazı hedeflerde lisanslı ağ bileşeni veya farklı yapılandırma
  gerekir.
- **Durumlu FB'leri koşullu çağırmak.** OSCAT'ın zamanlayıcı/profil içeren blokları da her IEC
  FB gibi her scan'de çağrılmalı; aksi halde iç zaman tabanı donar (bkz. 03_function_blocks.md
  "Her scan çağrı" kuralı).
- **Sürüm/CODESYS uyumunu göz ardı etmek.** Çok eski V2.3 export'ları doğrudan V3'e taşımak
  derleme hataları üretebilir; V3 için hazır port (örn. stefandreyer/OSCAT-BASIC) kullanmak
  daha güvenli.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih:** Standart yardımcı işlevlere (string, tarih/saat, matematik, ölçeklendirme,
  basit ağ protokolleri) ihtiyaç varsa ve bunları sıfırdan yazmaya değmiyorsa. Vendor-bağımsız
  kalmak isteyen, birden çok marka CODESYS hedefinde aynı kodu kullanacak ekipler için ideal.
  Bina otomasyonu projelerinde OSCAT BUILDING ciddi zaman kazandırır.
- **Etmemeli:** Güvenlik-kritik (SIL) işlevler için — OSCAT garanti vermez, sertifikalı
  değildir; emniyet fonksiyonu sertifikalı kütüphane gerektirir. Ayrıca üreticinin kendi
  optimize/desteklenen kütüphanesi (örn. motion için PLCopen MC, vendor net hizmetleri)
  daha iyi destek/garanti sunduğunda onları tercih et. Sıkı bellek/performans bütçeli küçük
  PLC'lerde devasa kütüphaneyi tümüyle eklemek yerine yalnızca gerekli POU'ları almak gerekebilir.

## Gerçek Proje Notları

- OSCAT'ın en büyük değeri **kod okuma referansı** olmasıdır: kaynağı açık olduğu için bir FB'nin
  içine bakıp "iyi yazılmış bir IEC kütüphanesi nasıl organize edilir, nasıl isimlendirir,
  saf fonksiyonu durumlu bloktan nasıl ayırır" sorularına somut cevap bulunur. Yeni başlayan
  bir ekip için canlı bir ders kitabı gibidir.
- Destek tamamen **topluluk** temellidir (oscat.de forumu). Üretici destek hattı yoktur;
  bir blok beklenmedik davranınca kaynağı okuyup kendin teşhis etmen beklenir. Bu, kapalı
  ticari kütüphanelere kıyasla hem güç hem sorumluluktur.
- Pratikte ekipler genellikle tüm kütüphaneyi eklemek yerine, ihtiyaç duydukları az sayıda
  POU'yu kendi proje kütüphanelerine kopyalayıp (lisans koşullarına uyarak) bakım altına alır;
  böylece kontrolör belleği şişmez ve sürüm sabitlenir.
- Lisans atfı çoğu zaman unutulur — ürünleştirme aşamasında ekip içi bir kontrol listesine
  "OSCAT atfı eklendi mi?" maddesini koymak gerçek bir dağıtım sorununu önler.

## İlgili Konular

- `knowledge/codesys/programming/04_libraries.md` — CODESYS'te kütüphane ekleme/yönetme
- `knowledge/codesys/programming/03_function_blocks.md` — FB/fonksiyon kalitesi (OSCAT bir referans)
- `knowledge/codesys/networking/03_tcp_socket.md` — OSCAT NETWORK'ün dayandığı soket katmanı
- `02_codesys_forge_store.md` — OSCAT'ın dağıtıldığı CODESYS Store/Forge ekosistemi
- `03_github_iec61131_projects.md` — OSCAT'a alternatif/topluluk port'ları (GitHub)
