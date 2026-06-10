---
KONU        : Beckhoff TwinCAT 3 Örnek Programları ve Uygulama Notları
KATEGORİ    : examples
ALT_KATEGORI: vendor-app-notes
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://github.com/Beckhoff"
    başlık: "Beckhoff resmi GitHub organizasyonu — TFxxxx_Samples depoları"
    güvenilirlik: resmi
  - url: "https://github.com/Beckhoff/TF6310_Samples"
    başlık: "Beckhoff/TF6310_Samples — TC3 TCP/IP örnekleri (PLC + C# + container)"
    güvenilirlik: resmi
  - url: "https://github.com/Beckhoff/TF7xxx_Samples"
    başlık: "Beckhoff/TF7xxx_Samples — TC3 Vision örnekleri"
    güvenilirlik: resmi
  - url: "https://infosys.beckhoff.com/content/1033/tc3_plc_intro/3259158539.html"
    başlık: "Beckhoff InfoSys — TwinCAT 3: Differences compared with TwinCAT 2"
    güvenilirlik: resmi
  - url: "https://infosys.beckhoff.com/content/1033/ethercatsystem/2469116427.html"
    başlık: "Beckhoff InfoSys — EtherCAT System Documentation (Sample programs)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_codesys_application_examples.md"
    ilişki: alternatif
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: gerektirir
  - konu: "knowledge/protocols"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "IEC 61131-3 temel kavramları (POU, FB, GVL, Task)"
  - "CODESYS V3 mantığı (TwinCAT 3 ile karşılaştırma için; knowledge/codesys/)"
  - "EtherCAT master/slave temel kavramı"
ÇELİŞKİLER :
  - kaynak: "Yaygın iddia: 'TwinCAT 3, CODESYS 3'tür / CODESYS runtime kullanır'"
    konu: "TwinCAT 2 ≈ CODESYS V2 idi; TwinCAT 3 Beckhoff'un kendi runtime/derleyicisidir"
    çözüm: >
      Doğrulanmış: TwinCAT 2.x büyük ölçüde CODESYS V2 tabanlıydı. TwinCAT 3 ise
      Visual Studio (XAE) içine taşındı ve Beckhoff kendi runtime/kernel uzantılarını
      kullanır; CODESYS V3 runtime'ı DEĞİLDİR (CODESYS runtime güvenlik açıkları
      TwinCAT 3'ü etkilememiştir). IEC 61131-3 dil ailesi ortaktır, runtime ve IDE
      farklıdır. [DOĞRULANMADI] "yalnızca dil yapısını ödünç aldı" iddiasının kesin
      kapsamı topluluk kaynaklıdır; Beckhoff resmi açıklaması esas alınmalıdır.
---

## Özün Ne

Beckhoff TwinCAT 3, IEC 61131-3 tabanlı ama **Beckhoff'a özel** bir otomasyon
platformudur: standart bir Windows endüstriyel PC'sini, gerçek-zamanlı çekirdek uzantıları
ile deterministik bir PLC + motion + IoT denetleyicisine dönüştürür. Geliştirme ortamı
(XAE) **Visual Studio** içine gömülüdür. TwinCAT örnek programları, ürün ailelerine
(TFxxxx fonksiyonları) göre düzenlenmiş, çoğunlukla **resmi GitHub depolarında** yayınlanan,
her klasörü ayrı bir mini-proje olan kaynaklı örneklerdir.

Neden önemli: TwinCAT ekosistemi CODESYS ile aynı IEC 61131-3 köküne dayanır; bu yüzden
CODESYS/InoProShop bilen biri ST/FB/Task mantığını taşıyabilir. Ancak runtime, IDE,
EtherCAT entegrasyonu ve haberleşme TF-kütüphaneleri Beckhoff'a özeldir — örnekler bu
farkları öğrenmenin en hızlı yoludur.

## Nasıl Çalışır

### Örneklerin dağıtım modeli

Beckhoff örnekleri başlıca iki kanaldan gelir:

1. **GitHub (github.com/Beckhoff):** Her TF (TwinCAT Function) ürünü için bir
   `TF...._Samples` deposu. Depo klonlanır veya ZIP indirilir; her örnek ayrı klasörde,
   InfoSys dokümanındaki sıraya göre yerleştirilir. Tipik içerik: bir TwinCAT projesi
   (PLC kodu) + (gerekiyorsa) bir C#/.NET istemci + (modern depolarda) container örnekleri.
2. **InfoSys (infosys.beckhoff.com):** Ürün dokümanı içindeki "Sample programs / Example
   programs" bölümleri; örneğin EtherCAT System dokümanı ve EL-terminal sayfaları örnek
   programlara ve indirme bağlantılarına yönlendirir.

### TwinCAT'in CODESYS'ten farkları (örnekleri okurken bilmek gereken)

- **IDE:** TwinCAT 3 = Visual Studio (XAE) eklentisi; CODESYS = bağımsız IDE. Menü/proje
  yapısı görsel olarak farklıdır.
- **Runtime:** TwinCAT 3 Beckhoff'un kendi gerçek-zamanlı çekirdeğidir; CODESYS V3 runtime
  değildir (bkz. ÇELİŞKİLER).
- **Adresleme/ADS:** Beckhoff'a özel **ADS** (Automation Device Specification) ara katmanı,
  PLC ↔ C#/.NET ↔ HMI haberleşmesinin temelidir. Örneklerin çoğu (ADS .NET, TCP/IP, OPC UA)
  ADS üzerinden konuşur — CODESYS'te doğrudan karşılığı yoktur.
- **HMI:** TwinCAT HMI (TE2000/TF2000) ayrı bir web tabanlı üründür; CODESYS Visualization'dan
  mimari olarak farklı (Beckhoff PLC ve görselleştirme ortamlarını ayırır).
- **C++/Matlab-Simulink:** TwinCAT 3, IEC 61131-3 yanında C++ modülleri ve Simulink kod
  üretimini de runtime'da çalıştırabilir (TC1300 C++ örnekleri) — CODESYS'te tipik değil.

## Pratikte Nasıl Kullanılır

1. **İlgili TF ürününü belirle:** Haberleşme (TCP/IP=TF6310, MQTT=TF6701, OPC UA=TF6100,
   S7=TF6620, FTP=TF6300), Vision=TF7xxx, Building Automation=TF8040, HMI=TF2000/TE2000,
   ADS .NET=TF6000.
2. **Depoyu al:** İlgili `Beckhoff/TF..._Samples` deposunu GitHub'dan klonla/ZIP indir.
   Her örnek alt klasördedir.
3. **Aç:** TwinCAT XAE (Visual Studio) ile projeyi aç; varsa C# istemcisini ayrı çöz.
4. **Çalıştır:** Yerel TwinCAT runtime'ında (XAR) aktive et; ADS üzerinden istemciyle
   haberleşmeyi izle. Vision/motion gibi donanım gerektiren örnekler için uygun donanım
   veya simülasyon gerekir.
5. **Pattern'i çıkar:** TF kütüphanesinin FB'lerinin (örn. IoT/MQTT publish-subscribe,
   TCP/IP socket FB'leri) çağrılma sırasını ve ADS arayüzünü öğren; kendi projene uyarla.

## Örnekler

Resmi `TF..._Samples` depolarının öğrettiği başlıca pattern'ler ("ne öğretir" düzeyinde,
kod kopyalanmadan; kaynak: github.com/Beckhoff depo listesi ve açıklamaları):

- **TF6310_Samples (TCP/IP):** PLC tarafı socket server/client + C# istemci + container
  örnekleri. Pattern: PLC'de TCP socket FB'leri ile bağlantı yönetimi ve istemci-sunucu
  haberleşmesi; modern dağıtım için container'lama.
- **TF6701_Samples (IoT MQTT) / TF6710 (IoT Functions) / TF6760 (HTTPS/REST):** PLC'den
  bulut/broker'a publish-subscribe ve REST çağrısı pattern'leri.
- **TF6100_Samples (OPC UA):** TwinCAT OPC UA server/client kurulumu, namespace ve node
  eşleme pattern'i.
- **TF6620_Samples (S7 Communication):** Siemens S7 PLC ile haberleşme — çoklu marka
  entegrasyon pattern'i.
- **TF7xxx_Samples (Vision):** Görüntü işleme zinciri; ayrıca C++ Vision örnekleri
  (Beckhoff-USA-Community/AAG_TcVision_CPP) gerçek-zamanlı görüntüyü PLC mantığına bağlamayı
  öğretir.
- **TF6000_ADS_DOTNET_V4/V5_Samples:** .NET uygulamasından ADS ile PLC değişkenlerine
  erişim — HMI/SCADA/üst sistem entegrasyonunun temel pattern'i.
- **TF2000_Server_Samples / TE2000_Client_Samples:** TwinCAT HMI sunucu eklentileri ve
  istemci örnekleri; web tabanlı HMI pattern'i.
- **EtherCAT (InfoSys + EL örnekleri):** EtherCAT System dokümanı ve EL-terminal örnek
  programları, master konfigürasyonu, PDO eşleme ve terminal (EL2202/EL5021 vb.) kullanımını
  öğretir.

## Sık Yapılan Hatalar

- **"TwinCAT = CODESYS 3" varsaymak.** Dil ailesi ortak olsa da runtime/IDE/ADS farklıdır;
  CODESYS alışkanlıklarını (özellikle haberleşme ve HMI) birebir uygulamaya çalışmak
  yanıltır (bkz. ÇELİŞKİLER).
- **ADS'i atlamak.** Beckhoff örneklerinin çoğu ADS üzerinden konuşur; ADS yönlendirmesini
  (AmsNetId, route) kurmadan C# istemcisi PLC'ye bağlanmaz.
- **Lisans/aktivasyon.** TF örnekleri ilgili TwinCAT Function lisansını gerektirir; geliştirme
  için 7-günlük trial aktivasyonu kullanılabilir, ama her yeniden başlatmada yenilenmesi
  gerekir. [DOĞRULANMADI] kesin lisans/trial koşulları sürüme göre değişir, Beckhoff'tan teyit.
- **GitHub örneği = üretim kodu sanmak.** Örnekler pattern içindir; hata işleme/emniyet
  eksiktir.
- **Sürüm uyumu (TC build):** Örnek belirli bir TwinCAT 3 build/library sürümüyle hazırlanır;
  farklı build'de açınca dönüştürme/uyarı çıkabilir.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih:** Donanım Beckhoff (IPC/EtherCAT EL terminalleri/EtherCAT servo) ise; PC-tabanlı
  yüksek performanslı kontrol, görüntü işleme, IoT/bulut entegrasyonu veya C++/Simulink
  modülü gerekiyorsa. ADS ile zengin üst-sistem entegrasyonu güçlü yandır.
- **Etme / dikkat:** Marka-bağımsız bir CODESYS projesi taşınabilirliği önceliğinse veya ekip
  yalnızca CODESYS/InoProShop biliyorsa, TwinCAT'in öğrenme eğrisi (genelde CODESYS'ten daha
  dik) ve ADS/Visual Studio farkları maliyet yaratır. TwinCAT kodu doğrudan CODESYS/InoProShop'a
  taşınmaz (runtime farkı).

## Gerçek Proje Notları

- **CODESYS bilgisi yarı yarıya transfer olur.** ST/FB/Task/durum makinesi mantığı (örn.
  PLCopen MC_ FB sırası) kavramsal olarak aynıdır; fakat haberleşme (ADS vs OPC UA/Modbus
  FB'leri), HMI ve cihaz konfigürasyonu yeniden öğrenilir.
- **Örnekleri "tek klasör = tek ders" olarak okuyun.** GitHub depolarının klasör düzeni
  InfoSys doküman sırasını izler; bir TF özelliğini öğrenirken InfoSys sayfasını + ilgili
  klasörü birlikte okumak en verimli yoldur.
- **ADS köprüsü en değerli pattern.** Üst sistem (MES/SCADA/.NET servis) entegrasyonunda
  TF6000 ADS .NET örnekleri, "PLC değişkenine güvenli ve performanslı erişim" pattern'ini
  öğretir; bu, CODESYS dünyasında genelde OPC UA ile çözülen sorunun Beckhoff'a özgü, daha
  düşük gecikmeli yoludur.
- **TwinCAT 2 → 3 ayrımı kritik:** Eski bir Beckhoff projesi TwinCAT 2 (CODESYS V2 tabanlı)
  ise, TwinCAT 3 örnekleri doğrudan uymaz; migrasyon ayrı bir iştir. Proje devralırken önce
  TwinCAT sürümünü tespit edin.

## İlgili Konular

- `01_codesys_application_examples.md` — jenerik CODESYS örnek pattern'leri (karşılaştırma)
- `03_inovance_am600_examples.md` — Inovance/InoProShop (CODESYS tabanlı) örnekler
- `knowledge/protocols` — OPC UA, Modbus, EtherCAT, S7 haberleşme temelleri
- `knowledge/codesys/fundamentals/01_runtime_architecture.md` — runtime/IDE karşılaştırma tabanı
