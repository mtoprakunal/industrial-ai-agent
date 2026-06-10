---
KONU        : CODESYS Resmi Örnek Projeleri ve Uygulama Notları Ekosistemi
KATEGORİ    : examples
ALT_KATEGORI: vendor-app-notes
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Examples/_ex_sm_hmi.html"
    başlık: "CODESYS Online Help — Example: SoftMotion Robotics HMI (MotionHMI.project)"
    güvenilirlik: resmi
  - url: "https://store.codesys.com/en/examples.html"
    başlık: "CODESYS Store International — Free Examples, Snippets kategorisi"
    güvenilirlik: resmi
  - url: "https://forge.codesys.com/prj/codesys-example/"
    başlık: "CODESYS Forge — codesys-example proje grubu (EtherCAT, Modbus, HMI örnekleri)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Examples/_ex_visu_hmi.html"
    başlık: "CODESYS Online Help — Example: HMI (LibForHMIDemo, veri kaynağı bağlama)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: gerektirir
  - konu: "02_beckhoff_twincat_samples.md"
    ilişki: alternatif
  - konu: "03_inovance_am600_examples.md"
    ilişki: tamamlar
  - konu: "knowledge/inovance/inoproshop/06_motion_control.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "CODESYS V3 IDE ve runtime kavramı (knowledge/codesys/fundamentals/)"
  - "IEC 61131-3 temel kavramları (POU, GVL, FB, Task)"
ÇELİŞKİLER :
  - kaynak: "Topluluk algısı: 'Örnek paketleri yüklemek için lisans gerekir'"
    konu: "CODESYS Store'daki çoğu örnek/snippet ücretsizdir; lisans gereken kısım kullanılan opsiyonel runtime özelliğidir"
    çözüm: >
      Store'daki "Free Examples, Snippets" kategorisi ücretsiz indirilir. Ancak bir
      örnek SoftMotion, OPC UA Server gibi lisanslı bir runtime bileşeni kullanıyorsa,
      o bileşenin lisansı hedef cihazda ayrıca gerekir. Örnek projenin kendisi ücretsiz,
      kullandığı runtime özelliği ayrı değerlendirilir.
---

## Özün Ne

CODESYS, üreticiden bağımsız (vendor-neutral) IEC 61131-3 platformu olduğundan, resmi
örnek projeleri tek bir donanıma değil **pattern'lere** odaklanır: bir fonksiyon
bloğunun (FB) doğru çağrılma sırası, bir kütüphanenin tipik kullanımı, bir haberleşme
yığınının kurulumu. Bu yüzden CODESYS örnekleri, "kopyala-yapıştır kod" değil,
**"bir özelliği doğru kullanma reçetesi"** olarak okunmalıdır. Inovance InoProShop =
CODESYS V3 olduğundan (bkz. knowledge/inovance/inoproshop/01), bu örneklerin neredeyse
tamamı InoProShop'a doğrudan transfer olur.

Neden önemli: CODESYS ekosisteminde bir özelliği sıfırdan keşfetmek yerine, resmi örneği
inceleyip pattern'i öğrenmek devreye alma süresini ciddi kısaltır. Örnek projeler aynı
zamanda "bu özelliği hangi runtime/lisans gerektirir" sorusunun da fiili dokümantasyonudur.

## Nasıl Çalışır

CODESYS örnek ekosistemi üç resmi kanaldan beslenir:

1. **CODESYS Online Help (help.codesys.com / content.helpme-codesys.com):**
   "CODESYS Examples" bölümü, her büyük özellik için (SoftMotion, Visualization/HMI,
   Communication, CNC) açıklamalı örnek projeler barındırır. Örnek genellikle bir paket
   olarak yüklenir ve `C:\Users\<user>\CODESYS Examples\...` altına çıkar.
2. **CODESYS Store (store.codesys.com):** "Free Examples, Snippets" kategorisi ücretsiz
   örnek paketleri, ek kütüphaneler (örn. CAN Bus) ve snippet'ler sunar. Paket Package
   Manager ile IDE'ye kurulur.
3. **CODESYS Forge (forge.codesys.com):** Topluluk + resmi `codesys-example` proje grubu;
   kaynak kodlu, versiyonlu örnekler (EtherCAT IDN/SDO okuma-yazma, Modbus TCP/Serial
   server/client, HMI veri kaynağı bağlama vb.). Git benzeri sürüm geçmişiyle erişilir.

Örneklerin ortak yapısı: bir `.project` dosyası + gereken kütüphaneler + (varsa) bir
visualization. Açıldığında simülasyonda (donanımsız) çalışabilecek şekilde tasarlanır;
böylece donanım gelmeden pattern öğrenilebilir.

## Pratikte Nasıl Kullanılır

1. **Konuyu belirle:** Motion mu, haberleşme mi, HMI mı? Help'teki "CODESYS Examples"
   ağacından veya Store'dan ilgili paketi bul.
2. **Paketi kur:** Store paketini indir → **Tools > Package Manager > Install**. Örnek
   projeler kullanıcı klasörüne çıkar.
3. **Simülasyonda aç:** Projeyi aç, **Online > Simulation** ile donanımsız çalıştır;
   FB'lerin durum geçişlerini online izle.
4. **Pattern'i çıkar:** İlgilendiğin FB'nin nasıl çağrıldığına (her çevrim mi, kenar
   tetikli mi), hangi kütüphaneyi gerektirdiğine, hangi konfigürasyon nesnesine
   (Device tree düğümü) bağlandığına bak.
5. **Kendi projene uyarla:** Telifli kodu kopyalamak yerine pattern'i kendi yapına göre
   yeniden yaz (değişken adları, ölçek, task ataması senin projene göre).

## Örnekler

Resmi örneklerin öğrettiği başlıca pattern'ler (kod kopyalanmadan, "ne öğretir" düzeyinde):

- **SoftMotion Robotics HMI (`MotionHMI.project`):** Bir eksen grubunu (axis group) çevrimdışı
  yapılandırmayı, desteklenen kinematik modellerinden birini seçmeyi öğretir; 6 eksene kadar
  destekler. Bir **Depictor** nesnesiyle robotun 3B hareketini görselleştirir. Manuel jog +
  programlı hareket gösterir. Eşlik eden örnek, **OPC UA Robot Companion Specification**
  uygulamasını sergiler (kaynak: CODESYS Help — SoftMotion Robotics HMI).
- **HMI Example (`LibForHMIDemo`):** Bir kütüphane içindeki parametre arayüzlü
  visualization'ı bir veri kaynağına (CODESYS V3 controller, data source) **nasıl
  bağlayacağını** öğretir — yani HMI ile PLC mantığını ayırma pattern'i (kaynak: CODESYS
  Help — Example: HMI).
- **Modbus Example (Forge `modbus`):** `ModbusFB` derlenmiş kütüphanesiyle standart Modbus
  TCP/Serial server ve client kurmayı; ayrıca >16 bit "wide register" gibi standart-dışı
  uzantıları öğretir. Üç uygulamalı (`ModbusFB_examples.project`): FB'lere genel bakış,
  serial server, serial client (kaynak: Forge — Modbus).
- **EtherCAT Example (Forge `ethercat-example`):** Servo sürücüde EtherCAT üzerinden
  **IDN okuma-yazma**, **CoE (CAN over EtherCAT) SDO** okuma-yazma ve **FoE (File over
  EtherCAT)** ile firmware indirme pattern'lerini öğretir (kaynak: Forge — EtherCAT Example).

## Sık Yapılan Hatalar

- **Örnek kodu körü körüne kopyalamak.** Örnekler pattern öğretmek için sadeleştirilmiştir;
  hata işleme, emniyet, ölçek sıklıkla minimaldir. Üretime taşırken bunları sen eklemelisin.
- **Sürüm/kütüphane uyuşmazlığı.** Örnek belirli bir CODESYS sürümü + kütüphane versiyonuyla
  hazırlanmıştır; farklı sürümde açınca eksik kütüphane veya derleme hatası çıkar. Library
  Manager'da eksikleri tamamla.
- **Lisanslı runtime özelliğini gözden kaçırmak.** SoftMotion/OPC UA Server gibi örnekler
  hedef cihazda lisanslı bir runtime bileşeni gerektirir; simülasyonda çalışan örnek gerçek
  donanımda lisanssız çalışmayabilir.
- **Simülasyon ≠ gerçek donanım sanmak.** Simülasyonda zamanlama/jitter idealdir; gerçek
  EtherCAT/motion davranışı donanımda farklıdır.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih:** Yeni bir CODESYS özelliğini (motion, OPC UA, Modbus, HMI veri bağlama) ilk kez
  kullanırken; resmi örnek doğru pattern'i ve gereken kütüphaneyi hızla gösterir.
- **Etme / dikkat:** Örneği üretim kodu sanıp emniyet/hata işleme eklemeden sahaya almak.
  Ayrıca üreticiye özel (Beckhoff/Inovance) ince ayarlar için jenerik CODESYS örneği yeterli
  olmayabilir; o zaman üreticinin kendi örneklerine bak (bkz. doc 02, 03).

## Gerçek Proje Notları

- **Pattern transfer edilebilir, konfigürasyon değil.** Bir CODESYS SoftMotion örneğindeki
  `MC_*` FB kullanım sırası InoProShop'ta birebir çalışır; fakat eksen ölçeği, EtherCAT
  eşlemesi ve task ataması projeye/donanıma özeldir (bkz. inovance/inoproshop/06).
- **OPC UA Companion Spec örnekleri standartlaşmayı öğretir.** Robotics HMI örneğindeki
  OPC UA Robot Companion uygulaması, makine-istemci entegrasyonunda "kendi protokolünü
  uydurma, companion spec'e uy" mesajını verir — saha entegrasyonunda değerli bir alışkanlık.
- **Forge sürüm geçmişi okunmalı.** Forge örneklerinin r2/r3 gibi revizyonları vardır;
  en güncel revizyonu al, eski revizyondaki bilinen sorunları commit notlarından kontrol et.
- **[DOĞRULANMADI]** Her örnek paketinin tam içerik listesi sürümle değişir; bu belgedeki
  örnek seti temsilidir, kesin güncel liste için Store/Help/Forge'dan teyit edilmelidir.

## İlgili Konular

- `02_beckhoff_twincat_samples.md` — Beckhoff'un kendi örnek ekosistemi (TwinCAT farkı)
- `03_inovance_am600_examples.md` — Inovance AM600/InoProShop örnekleri (CODESYS tabanı)
- `knowledge/inovance/inoproshop/06_motion_control.md` — SoftMotion/PLCopen MC_ FB pattern'leri
- `knowledge/codesys/fundamentals/` — runtime, task, kütüphane temeli
