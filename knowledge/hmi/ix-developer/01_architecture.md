---
KONU        : Beijer iX Developer Mimarisi
KATEGORİ    : hmi
ALT_KATEGORI: ix-developer
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://www.beijerelectronics.com/docs/iX-251-Reference/en/index-en.html"
    başlık: "iX Developer 2.51 Referans Kılavuzu"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-250-Reference/en/the-configuration-tool.html"
    başlık: "iX Developer 2.50 - The Configuration Tool"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-250-Reference/en/tags.html"
    başlık: "iX Developer 2.50 - Tags"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-250-Reference/en/controller.html"
    başlık: "iX Developer 2.50 - Controller"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX/3.0/User-Guide/en/controllers.html"
    başlık: "iX Developer 3.0 - Controllers"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX/3.0/User-Guide/en/projects.html"
    başlık: "iX Developer 3.0 - Projects"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX/3.0/User-Guide/en/servers.html"
    başlık: "iX Developer 3.0 - Servers (Web Server & OPC UA Server)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-250-Reference/en/audit-trail.html"
    başlık: "iX Developer 2.50 - Audit Trail"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-251-Reference/en/trend-viewer.html"
    başlık: "iX Developer 2.51 - Trend Viewer"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/ix-user/en/alarm-management.html"
    başlık: "iX Developer - Alarm Management"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/en/Products/software/ix-hmi-software"
    başlık: "iX2 HMI Software - Resmi Ürün Sayfası"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/en/Products/software/ix-hmi-software/for-advanced-users"
    başlık: "iX HMI Software - Advanced Users (C# scripting, .NET, OPC UA)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-Script/en/getting-started.html"
    başlık: "iX Developer Scripting - Getting Started"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.us/en-US/Products/software/iX3"
    başlık: "iX3 HMI Software - Ürün Sayfası"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/X2-X3/en/x2-to-x3---transition-guide-for-ix-developer.html"
    başlık: "X2 to X3 - Transition Guide for iX Developer"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "knowledge/hmi/ix-developer/02_codesys_connection.md"
    ilişki: tamamlar
  - konu: "knowledge/hmi/ix-developer/03_screen_design.md"
    ilişki: detaylandırır
  - konu: "knowledge/hmi/ix-developer/04_scripting.md"
    ilişki: detaylandırır
  - konu: "knowledge/hmi/architecture/01_hmi_patterns.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Genel HMI mimarisi kavramları (knowledge/hmi/architecture/_synthesis.md)"
  - "Tag ve controller kavramı: PLC ile HMI arasındaki veri bağlantısı"
  - "Temel .NET/C# bilgisi (gelişmiş özellikler için)"
ÇELİŞKİLER :
  - kaynak: "Resmi belgeler"
    konu: "iX Developer 2.xx ile iX Developer 3.xx (iX3) paralel olarak satılmaktadır. iX2 X2 serisi panellerle; iX3 yalnızca X3 serisi panellerle uyumludur. Bu belge öncelikle iX2/2.5x üzerinedir — iX3 farkları ayrıca belirtilmiştir."
    çözüm: "Proje başlarken hedef panel serisine göre doğru yazılım versiyonu seçilmeli."
  - kaynak: "Lisanslama ayrıntıları"
    konu: "Resmi online dokümanda iX Runtime için tag sınırı sayıları (örn. Temel lisans kaç tag?) açıkça yayımlanmamaktadır. Yalnızca 'USB dongle veya Softkey gerekli', 'iç taglar sınırsız', 'controller taglarda limit var' bilgileri yer almaktadır."
    çözüm: "Kesin tag limitleri için Beijer Electronics satış kanalı veya SmartStore ile iletişime geçilmeli."
  - kaynak: "iX2 vs iX3 .NET teknoloji temeli"
    konu: "iX2 WPF (Windows Presentation Foundation) tabanlı olduğu belgelenmiştir. iX3'ün iç teknoloji temeli (WPF mi, MAUI mi, başka bir çerçeve mi?) resmi online dokümanda açıkça belirtilmemektedir."
    çözüm: "iX3 için 'C# scripting + NuGet paketi' desteği doğrulanmıştır; altta yatan UI framework belirsizliği teknik bağlama göre değerlendirilebilir."
  - kaynak: "İX Developer'ın eski T-serisi paneller ile ilişkisi"
    konu: "iX T7A, iX T10A, iX T15C gibi eski T-serisi paneller resmi sitede 'Previous models' olarak listelenmiştir. iX Developer 2.xx ile uyumlu oldukları kabul edilmekle birlikte, belirli versiyon kısıtlamaları resmi online dokümanda net olarak belgelenmemiştir."
    çözüm: "T-serisi için versiyon uyumluluğu Beijer destek belgelerinden veya donanım dokümanından doğrulanmalı."
---

## Özün Ne

Beijer Electronics **iX Developer**, Beijer'in kendi HMI panel serileri (X2, X3) ve PC tabanlı uygulamalar için tasarlanmış entegre bir HMI geliştirme ve çalışma zamanı platformudur. Yazılım iki ana parçadan oluşur: proje tasarımının yapıldığı **iX Developer** (geliştirme ortamı) ve tasarlanan projenin hedef panelde veya PC'de çalıştırıldığı **iX Runtime** (çalışma zamanı motoru). Altta yatan teknoloji .NET ve WPF (Windows Presentation Foundation) tabanlıdır; bu sayede C# ile özel fonksiyon yazımı ve harici .NET assembly import desteği sunulmaktadır.

iX Developer'ın kritik özelliği **marka bağımsız sürücü modeli**dir: Siemens, Allen-Bradley, Mitsubishi, Schneider Electric dahil onlarca farklı PLC markasına sürücü desteği sağlanır; aynı proje birden fazla controller'a aynı anda bağlanabilir. Alarm yönetimi, trend/data logger, reçete yönetimi ve audit trail gibi endüstriyel HMI fonksiyonları ek yazılıma gerek kalmadan dahili olarak sağlanır.

Bu belge, iX Developer **2.xx** (özellikle 2.50–2.51) sürümünü öncelikli olarak ele almakta; iX Developer **3.xx** (iX3) farkları ilgili bölümlerde ayrıca belirtilmektedir.

## Nasıl Çalışır

### Tasarım / Çalışma Zamanı Ayrımı

iX Developer iki ortam arasında net bir ayrım yapar:

```
┌──────────────────────────────────────────────────────────────────────┐
│  iX DEVELOPER (Geliştirme Ortamı) — Mühendis PC'si                  │
│                                                                        │
│  ┌─────────────────────┐    ┌──────────────────────────────────────┐  │
│  │  Tasarım Ortamı     │    │  Proje Klasörü                       │  │
│  │  - Ekran tasarımı   │    │  /MyProject/                         │  │
│  │  - Tag tanımlama    │    │    ├── Tasarım dosyaları (üst düzey) │  │
│  │  - Driver ekleme    │    │    ├── Temp/  (derleme geçici)       │  │
│  │  - Alarm/Reçete/    │    │    └── Output/ (Runtime dosyaları)   │  │
│  │    Trend yapılandır │    │                                      │  │
│  │  - C# script        │    │  Build → App (derlenmiş paket)       │  │
│  └─────────────────────┘    └──────────────────────────────────────┘  │
│                                        │                               │
│                          İndir / Transfer                              │
│                                        ▼                               │
├──────────────────────────────────────────────────────────────────────┤
│  iX RUNTIME (Çalışma Zamanı) — Hedef Panel veya PC                  │
│                                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │  Derlenmiş iX App çalışır                                       │  │
│  │  - Controller sürücüleri → PLC bağlantısı                       │  │
│  │  - Alarm motoru                                                  │  │
│  │  - Trend / Data Logger                                           │  │
│  │  - Reçete motoru                                                 │  │
│  │  - Audit Trail servisi                                           │  │
│  │  - Web Server (port 7001) + OPC UA Server                       │  │
│  │  - Lisans: USB dongle veya Softkey (PC için gerekli)            │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

- **iX Developer** Windows 10/11 çalışan mühendis PC'sinde kurulur. Tasarım dosyaları üst düzey proje klasöründe saklanır; derleme (Build/Rebuild) sırasında Temp ve Output klasörleri oluşturulur. Output klasöründeki runtime dosyaları hedef panele veya PC'ye aktarılır.
- **iX Runtime** hedef donanımda (HMI paneli veya PC) iX App'i çalıştırır. PC tabanlı çalışmada lisans (USB dongle veya Softkey) zorunludur. HMI panellerinde ayrı lisans gerekmez.

iX Developer 3'te terminoloji değişmiştir: "iX App" terimi kullanılır; proje "App" olarak derlenir ve target'a aktarılır. iX3'te OS3 (X3 serisi için özel işletim sistemi katmanı) watchdog, uzaktan erişim ve PIN yönetimini üstlenir.

### Tag / Controller / Driver Modeli

**Tag Modeli**

iX Developer'da PLC'ye (veya diğer cihazlara) bağlı ya da dahili tüm veri noktaları "tag" olarak modellenir.

| Tag Tipi | Açıklama |
|---|---|
| Controller tag | Harici controller'a sürücü veya OPC aracılığıyla bağlı tag. Çift yönlü okuma/yazma. |
| Internal tag | Controller bağlantısı olmayan yerel hesaplama/durum taşıma için kullanılan tag. Kalıcı (non-volatile) olarak işaretlenebilir. |
| System tag | Donanım metrikleri (CPU yükü, sıcaklık), iletişim durumu, tarih/saat gibi sistem değişkenlerini açığa çıkaran önceden tanımlı, salt okunur/yazılabilir taglar. Arayüzde mavi renk ile gösterilir. |
| Array tag | Aynı veri tipinden dizin numarasıyla adreslenebilen tag grubu. |

**Desteklenen veri tipleri:** BIT, BOOL, INT16, UINT16, INT32, UINT32, FLOAT, DOUBLE, DATETIME, STRING.

**Poll grupları:** Taglar 5 farklı polling aralığına atanabilir. Yüksek performanslı panellerde minimum 25 ms aralığa kadar inilebilir. Bu sayede kritik alarm bitleri hızlı, yavaş değişen ölçümler daha seyrek okunabilir.

**Ölçekleme (Scaling):** Yalnızca controller taglarına uygulanır.
- Okuma: `Panel değeri = Offset + (Gain × Register değeri)`
- Yazma: `Register değeri = (Panel değeri − Offset) / Gain`

**Veri Değişimi (Data Exchange):** Aynı veya farklı markalı birden fazla controller arasında gerçek zamanlı tag senkronizasyonu sağlar. Tag bazında veya tüm tag aralığı için yön (okuma/yazma/çift yönlü) ve tetikleyici (değer değişimi veya zaman bazlı) tanımlanabilir.

**Controller Modeli**

Her controller bir sürücüyle (veya OPC UA bağlantısıyla) eşleşir. Tek bir tag birden fazla controller'a eş zamanlı olarak bağlanabilir; böylece aynı proje farklı controller'larla çalışabilir. Birden fazla controller eş zamanlı aktif olduğunda, aynı tag iki farklı aktif controller'a bağlıysa iX App hangi controller'dan değer okunacağını belirleyemez — bu durum dikkat gerektirir.

**DEMO Controller:** Gerçek donanım olmadan geliştirme ve test imkânı sağlar. Önceden tanımlı digital taglar (M0–M99), analog taglar (D0–D99), counter taglar (C0–C4) ile birlikte gelir.

**Driver (Sürücü) Mimarisi**

İki tip sürücü mevcuttur:

| Sürücü Tipi | Kurulum | Boyut | Yeniden Başlatma |
|---|---|---|---|
| MPD sürücü | Yönetici yetkisi gerekli | ~3 MB | Gerekli |
| GEN2 sürücü | Kullanıcı modunda kurulabilir | ~250 kB | Gerekli değil |

**Generic Driver Engine** iX Developer ile otomatik olarak kurulur ve GEN2 sürücülerini yönetir; iX Developer'dan bağımsız güncellenebilir. Sürücüler internet veya yerel dosyadan güncellenebilir.

OPC UA bağlantısında iX Developer bir OPC UA **istemcisi** olarak çalışır. Bağlantı parametreleri: URL formatı `opc.tcp://`, anonim veya kullanıcı adı/şifre kimlik doğrulama, namespace URI, subscription ve sampling aralıkları.

### Proje Yapısı

```
MyProject/                        ← Proje klasörü
├── [Tasarım Dosyaları]           ← Ekranlar, taglar, konfigürasyon
├── Temp/                         ← Derleme ara dosyaları (Build/Rebuild)
│   └── Output/                   ← Runtime'a gönderilecek dosyalar
│
iX Developer — Project Explorer:
├── Screens (Ekranlar)
│   ├── Foreground ekranlar
│   ├── Background ekranlar (şablon)
│   └── Templates (şablon ekranlar)
├── Functions (Fonksiyonlar)
│   ├── Alarm Server
│   ├── Security (Kullanıcı/Grup yönetimi)
│   ├── Tags
│   ├── Data Logger
│   ├── Trend Viewer
│   └── Recipe Manager
├── Controllers (Controller bağlantıları)
├── Script Modules (C# scriptler)
└── Configuration Pages
```

**Önemli kısıtlama:** Proje klasörü içindeki herhangi bir dosya yolu 260 karakteri geçerse Build, Rebuild, Run veya Simulate işlemi başarısız olur. Proje yerel sabit diskte saklanmalı; OneDrive, Google Drive gibi bulut senkronizasyon servisleri projede erişim hatalarına yol açabilir.

### Desteklenen Platformlar

**iX Developer 2.xx (iX2):**
- Hedef HMI paneller: **X2 serisi** (X2 base v2, X2 pro, X2 marine, X2 control, X2 extreme ve varyantları)
- Eski nesil **iX T-serisi** paneller (iX T7A, iX T7B, iX T10A, iX T15C vb.) — "Previous models" kategorisinde
- PC tabanlı uygulamalar: Windows 10/11 (IoT Enterprise 2019 LTSC dahil)
- Geliştirme PC: Windows 10 (22H2, 21H2, 20H2) veya Windows 11; 2 GHz+ işlemci, 2 GB RAM, DirectX 9.0+ grafik

**iX Developer 3.xx (iX3):**
- **Yalnızca X3 serisi** HMI paneller (X3 web varyantları hariç)
- OS3 işletim sistemi katmanı üzerinde çalışır
- iX2 projeleri iX3'e geçirilebilir; sıfırdan yeniden yazma gerekmez
- C# scripting + NuGet paketi desteği

**iX Runtime (PC tabanlı):**
- Windows 10/11 veya Windows 10 IoT Enterprise 2019 LTSC
- 1.3 GHz+ işlemci, 1 GB RAM, DirectX 9.0+ grafik
- Lisans zorunlu (aşağıya bakınız)

### Dahili Fonksiyonlar

**Alarm Yönetimi**

Alarm koşulları tag değerinin mantıksal değerlendirmesiyle tanımlanır. Alarmlar gruplara bölünebilir. Alarm göstergesi durumları:
- Yanıp sönen kırmızı → Aktif, onaylanmamış alarm var
- Yanıp sönen yeşil → Aktif onaylanmış alarm var veya aktif olmayan onaylanmamış alarm var
- Gösterge kaybolur → Tüm alarmlar onaylanmış ve pasif

Alarm nesnesi sütun düzenini, buton konumunu ve görüntüleme özelleştirmelerini destekler. "Ack All" butonu tüm alarmları onaylar.

**Trend Viewer ve Data Logger**

İki veri modu:
- **Gerçek zamanlı:** Tag değerleri RAM cache'den okunur; tarihsel saklama yapılmaz.
- **Tarihsel:** Data Logger aracılığıyla taglar proje veritabanına kaydedilir; Trend Viewer bu veriye erişir.

Eğri parametreleri (renk, kalınlık), zaman ekseni, değer ekseni (min/max) ve dinamik ölçekleme tag bağımlı olarak yapılandırılabilir.

**Reçete (Recipe) Yönetimi**

Reçeteler, bir grup tag değerini tek işlemle kaydetmek veya controller'a yüklemek için kullanılır. Tag Configuration sekmesinde reçeteye dahil edilecek taglar seçilir. Çalışma zamanında:
- **Save recipe:** Anlık tag değerleri HMI panelinde reçete olarak kaydedilir.
- **Load recipe:** Kaydedilmiş reçete değerleri controller'a indirilir.

Tasarım zamanında da runtime reçetelerinin import/export işlemi yapılabilir. Reçete kütüphaneleri farklı parametre setleri içerebilir.

**Audit Trail**

Operatör eylemlerini ve tag değişikliklerini izler. İki loglama stratejisi:
- **FDA Modu:** Hiçbir kayıt üzerine yazılmaz. Kapasite %80'e ulaşıldığında uyarı verilir; export yapılana kadar sistem yeni yazma işlemlerini engeller.
- **Dairesel tampon (Circular buffer):** Kapasite dolunca en eski kayıtlar sessizce üzerine yazılır.

Export: `.csv` formatında yapılır. Panel hedeflerinde USB, harici bellek kartı veya Proje Dosyaları klasörüne; PC hedeflerinde kullanıcı tanımlı yola export edilebilir. Virgül veya noktalı virgül ayırıcı seçilebilir.

**Güvenlik (Security)**

Kullanıcı ve grup tabanlı erişim kontrolü. Nesne düzeyinde güvenlik özellikleri tanımlanabilir.

**Web Server ve OPC UA Server**

| Sunucu | Protokol | Port | Kimlik Doğrulama | Notlar |
|---|---|---|---|---|
| Web Server | HTTPS | 7001 | Bearer token | REST API ile tag okuma/yazma; Swagger desteği; statik dosya sunumu |
| OPC UA Server | UA TCP Binary | Yapılandırılabilir | Kullanıcı adı/şifre | Maks. 20 eş zamanlı oturum; otomatik self-signed sertifika (20 yıl); array taglar desteklenmez |

Web Server JavaScript SDK ve RESTful API aracılığıyla harici sistemlerin HMI verilerine erişmesini sağlar.

### .NET / WPF Teknoloji Temeli

iX Developer (2.xx) WPF (Windows Presentation Foundation) tabanlı bir uygulamadır. Özelleşmiş fonksiyon tasarımı için:

- **C# scripting:** Betikler C# ile yazılır; derlenerek çalıştırılabilir dosyaya dönüştürülür (yorumlanmaz). Script modülleri yeniden kullanılabilir.
- **WPF User Control / WPF Custom Control:** Visual Studio'da WPF User Control Library projesi oluşturulur. WPF kontrolleri tag değerine dependency property aracılığıyla bağlanabilir. Windows Forms kontrolleri tag değerine bağlanamaz.
- **.NET Assembly import:** Harici `.dll` dosyaları `Project > Referenced Assemblies` üzerinden import edilir. Üçüncü parti assembly'ler `C:\Users\Public\Documents\Beijer Electronics AB\iX Developer\Thirdparty\` altında saklanır.
- **iX3 ek desteği:** NuGet paketi entegrasyonu. Active Directory kullanıcı yönetimi, çoklu oturum açma (SSO) ve çok faktörlü kimlik doğrulama (MFA).

### Lisanslama

| Senaryo | Lisans Gerekliliği |
|---|---|
| HMI paneli (X2, X3) | Lisans kısıtlaması yok; panel lisansı dahili |
| PC tabanlı iX Runtime | USB dongle veya Softkey (yazılım lisansı) zorunlu |
| İç taglar | Her iki senaryoda da sınırsız |
| Controller tagları (PC) | USB dongle tarafından belirlenen limitle sınırlı |
| iX Runtime deneme sürümü | 30 dakikada bir yeniden başlatma gerektirir |
| iX Developer deneme sürümü | 30 günlük ücretsiz deneme |

**Not:** Controller tag limiti sayıları resmi online dokümanda açıklanmamaktadır. Kesin değerler için Beijer Electronics satış kanalı veya SmartStore ile iletişime geçilmesi gereklidir (bkz. ÇELİŞKİLER).

## Pratikte Nasıl Kullanılır

### Yeni Proje Oluşturma (iX Developer 2.xx)

```
1. iX Developer'ı aç → File > New Project
2. Hedef seç: X2 panel modeli veya PC
   (Hedef seçimi ekran çözünürlüğünü ve mevcut özellikleri belirler)
3. Controller ekle: Tags > Controller Tab > Add
   - PLC tipi ve sürücüsü seçilir (MPD veya GEN2)
   - Sürücü internet veya yerel dosyadan yüklenir
   - İletişim parametreleri (IP, port, seri vb.) ayarlanır
4. Taglar tanımla: Tags sekmesi
   - Controller tag: Adres (ör. M0, D10), veri tipi, poll grubu
   - Internal tag: İlk değer, non-volatile seçeneği
   - Ölçekleme ve audit trail seçenekleri
5. Ekran tasarımı: Insert tab ile nesneler eklenir
   - Taglar nesnelerin özellik ızgarasından bağlanır
6. Alarm yapılandırması: Functions > Alarm Server
7. Data Logger: Functions > Data Logger → Trend Viewer bağlantısı
8. Reçete: Functions > Recipe Manager
9. Audit Trail: Insert tab → Audit Trail etkinleştirme
10. Build: Projeyi derle → Transfer: Panele indir veya PC'ye aktar
```

### iX Runtime PC Kurulumu

```
1. iX Runtime installer'ı çalıştır
2. USB dongle veya Softkey lisansı bağla/etkinleştir
3. Derlenmiş iX App'i (Output klasörü içeriği) çalışma dizinine kopyala
4. iX Runtime'ı başlat → Uygulama yüklenir ve çalışır
(Trial modunda her 30 dakikada manuel yeniden başlatma gerekir)
```

### Poll Grubu Yapılandırması — En İyi Pratikler

```
Tag Tipi               Poll Grubu   Aralık Önerisi
─────────────────────────────────────────────────
Alarm bitleri          Grup 1       25–100 ms
Motor durum bitleri    Grup 2       100–200 ms
Anlık ölçümler         Grup 3       200–500 ms
Sıcaklık, basınç       Grup 4       500 ms–1 s
Sayaçlar, toplamlar    Grup 5       1–5 s
```

### OPC UA Bağlantısı Yapılandırması

```
Tags > Controller Tab > Add Controller
  → Driver: OPC UA Client seçimi
  → URL: opc.tcp://<ip>:<port>
  → Kimlik doğrulama: Anonim veya kullanıcı adı/şifre
  → Namespace URI → kısa prefix eşleştirme
  → Subscription aralığı ve sampling aralığı ayarlama
  → Structured tags için: Project > Settings > Advanced > Enable
```

## Örnekler

### Basit Alarm Tanımı

```
Alarm Server → Add Alarm:
  Açıklama : "Motor 1 Aşırı Sıcaklık"
  Tag      : Motor1_Temperature
  Koşul    : GreaterThan
  Eşik     : 85.0
  Geçmiş   : Etkin (History logging açık)
  Onay gerekli: Evet (Require acknowledgement)
```

### C# Script ile Hesaplama (Script Modülü)

```csharp
// iX Developer Script Module — örnek
// Otomatik tetikleyici: Tag değeri değiştiğinde
using System;

public class MotorPowerCalc
{
    // Güç = Voltaj × Akım
    public static void Calculate()
    {
        double voltage = Globals.Tags.Motor1_Voltage.Value;
        double current = Globals.Tags.Motor1_Current.Value;
        Globals.Tags.Motor1_Power.Value = voltage * current;
    }
}
```

### Audit Trail — FDA Modu Yapılandırması

```
Insert Tab → Enable Audit Trail
  → Loglama stratejisi: FDA Mode
  → Log seçenekleri: Tag value changes, User actions
  → Açıklama: Audit Trail nesnelerine 255 karakter açıklama eklenebilir

Export:
  Actions → Database Export
    → Hedef: USB veya proje klasörü
    → Format: CSV (virgül veya noktalı virgül)
```

### WPF Custom Control Entegrasyonu

```csharp
// Visual Studio'da WPF User Control Library projesi
// DefaultProperty ile hangi property'nin tag'a bağlanacağı belirlenir
[DefaultProperty("Value")]
public partial class CustomGauge : UserControl
{
    public static readonly DependencyProperty ValueProperty =
        DependencyProperty.Register("Value", typeof(double),
            typeof(CustomGauge), new PropertyMetadata(0.0));

    public double Value
    {
        get => (double)GetValue(ValueProperty);
        set => SetValue(ValueProperty, value);
    }
}
// .dll → C:\Users\Public\Documents\Beijer Electronics AB\iX Developer\Thirdparty\
// iX Developer → Project > Referenced Assemblies → Import
```

## Sık Yapılan Hatalar

**1. Proje Klasörünü Bulut Senkronizasyona Kaydetmek**
OneDrive veya Google Drive ile senkronize edilen klasörlerde proje açma sırasında "Access Denied" hatası alınır. Çözüm: Proje mutlaka yerel sabit diskte saklanmalıdır.

**2. Dosya Yolu 260 Karakteri Aşıyor**
Proje klasörü içindeki herhangi bir dosya yolunun 260 karakteri aşması Build, Rebuild, Run ve Simulate işlemlerini başarısız kılar. Çözüm: Kısa proje adı seçilmeli, derin iç içe klasör yapısından kaçınılmalıdır.

**3. Aynı Tag Birden Fazla Aktif Controller'a Bağlamak**
Tek bir tag iki farklı aktif controller'a bağlandığında iX App hangi controller'dan okuma yapacağını belirleyemez; beklenmedik davranışa yol açabilir. Çözüm: Data Exchange özelliği bu senaryo için tasarlanmıştır; doğrudan çok controller bağlantısından kaçınılmalıdır.

**4. Windows Forms Kontrol ile Tag Bağlama Denemesi**
WPF'den farklı olarak Windows Forms kontrolleri tag değerine doğrudan bağlanamaz. Özel kontrol tasarımında WPF User Control Library seçilmelidir.

**5. MPD Sürücü Kurulumunda Yönetici Yetkisi Unutmak**
MPD sürücüleri yönetici yetkisi ve uygulama yeniden başlatması gerektirir. GEN2 sürücüleri ise kullanıcı modunda sorunsuz kurulur. Yeni projelerde GEN2 sürücüleri tercih edilmelidir.

**6. iX2 Projesini iX3 ile X2 Panele Aktarmaya Çalışmak**
iX Developer 3 yalnızca X3 serisi panellerle uyumludur; X2 serisi paneller için iX Developer 2.xx kullanılmalıdır. Versiyon uyuşmazlığı derleme veya transfer hatalarına yol açar.

**7. PC iX Runtime'ı Lisanssız Çalıştırmak**
Lisans olmadan iX Runtime her 30 dakikada bir yeniden başlatılması gerekir; kesintisiz endüstriyel kullanım mümkün değildir. Üretim ortamı için USB dongle veya Softkey lisansı edinilmelidir.

**8. Audit Trail için FDA Modu Yerine Circular Buffer Seçmek (Yönetmelik Uyumu Gereken Projelerde)**
FDA 21 CFR Part 11 kapsamındaki projelerde Circular Buffer kullanımı kayıtların üzerine yazılmasına izin verdiğinden yönetmelik ihlali oluşturur. FDA modunda veri %80 dolulukta uyarı verilir; export planı önceden tanımlanmalıdır.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### iX Developer Tercih Edilmeli

```
✓ Hedef donanım Beijer Electronics X2 veya X3 serisi panel
✓ Marka bağımsız PLC entegrasyonu (Siemens, AB, Mitsubishi vb.)
  ve tek geliştirme ortamı isteniyor
✓ Alarm, trend, reçete, audit trail gereksinimleri var;
  ek yazılım lisansından kaçınılmak isteniyor
✓ WPF/C# bilgisi ile özel kontrol veya hesaplama mantığı eklenecek
✓ Web tabanlı uzaktan erişim veya OPC UA veri paylaşımı gerekiyor
  (dahili sunucular kullanılacak)
✓ FDA 21 CFR Part 11 uyumlu audit trail gereksinimi var
```

### iX Developer Tercih Edilmemeli

```
✗ Hedef donanım Beijer Electronics dışı (Siemens TP serileri,
  Allen-Bradley PanelView, Weintek vb.) — o markaya özgü yazılım tercih edilmeli
✗ Büyük ölçekli SCADA (100+ ekran, historian, raporlama kritik)
  — Ignition, WinCC gibi platform tabanlı SCADA daha uygun
✗ Web tabanlı HMI tercih ediliyorsa (React/Vue + WebSocket)
  — iX Developer masaüstü geliştirme ortamı tabanlı, saf web değil
✗ Linux veya macOS geliştirme ortamı (iX Developer yalnızca Windows 10/11)
✗ Açık kaynak veya lisanssız çözüm gerektiğinde (PC runtime lisans zorunlu)
```

## Gerçek Proje Notları

**Not 1 — Sürücü Seçimi Projeyi Etkiler**
GEN2 sürücüler MPD sürücülere göre daha küçük (250 kB vs 3 MB) ve kullanıcı modunda kurulabilir olmalarıyla pratik avantaj sağlar. Yeni kurulumda GEN2 sürücü mevcut olan PLC markası seçilmeli; müşteri sitesinde güncelleme gerektiğinde internet üzerinden ya da dosyadan anında yapılabileceği unutulmamalıdır.

**Not 2 — Poll Grubu Tasarımı Baştan Yapılmalı**
Tüm tagları aynı poll grubuna koymak düşük performanslı panellerde iletişim döngü süresini artırır ve gecikmeye yol açar. Alarm bitleri en hızlı gruba (25–100 ms), sayaçlar en yavaş gruba (1–5 s) atanmalı; 5 grup kapasitesi baştan planlanmalıdır.

**Not 3 — iX3'e Geçiş Öncesi Kırılma Noktaları**
iX3'e geçerken FTP ve VNC desteğinin kaldırıldığını, StatusBar/ToolBar/DataGrid kontrollerinin artık bulunmadığını ve SQLite kütüphanesinin değiştiğini (System.Data.SQLite → Microsoft.Data.Sqlite) göz önünde bulundurun. Mevcut iX2 projelerinde bu özellikleri kullanan kısımlar geçiş öncesi tespit edilmeli ve alternatifler planlanmalıdır.

**Not 4 — Audit Trail Kapasite Planlaması**
FDA modunda her operator aksiyonu ve tag değişimi loglanırsa büyük projelerde veritabanı doluluk hızı yüksek olabilir. Gerçekten takip edilmesi gereken taglar ve aksiyonlar seçici biçimde işaretlenmeli, otomatik export planı (tarih bazlı klasörleme, USB aktarım) devreye alınmalıdır.

**Not 5 — Web Server Güvenliği**
iX Developer 3.0 itibariyle Web Server yalnızca HTTPS üzerinden erişim sağlar. Eski iX2 projelerini iX3'e taşırken HTTP tabanlı entegrasyonlar HTTPS'e güncellenmeli, Bearer token kimlik doğrulama mekanizması gözden geçirilmelidir.

**Not 6 — Data Exchange ile Çoklu PLC Senaryosu**
Aynı hat üzerinde iki farklı markalı PLC (ör. Siemens S7 + Modbus cihaz) çalışıyorsa ve aralarında veri aktarımı gerekiyorsa iX Developer'ın Data Exchange özelliği bu işlevi HMI düzeyinde üstlenebilir. Bu PLC-to-PLC iletişim yerine HMI üzerinden köprü kurma anlamına gelir; kritiklik düzeyine ve gecikme toleransına göre tercih edilip edilmeyeceği değerlendirilmelidir.

**Not 7 — Build Output Klasörünün Temizlenmesi Versiyon Geçişlerinde Kritik**
iX Developer 2.5x'te bir projeyi büyük bir sürüm güncellemesinden sonra (ör. 2.50 → 2.53) ilk kez derlerken, eski `Temp/` ve `Output/` klasörlerinde kalan ara dosyalar transfer sonrası panelde "version mismatch" veya beyaz ekran hatasına yol açtı. `Rebuild All` (Build değil) yapmak ve gerektiğinde `Temp/` klasörünü manuel silmek sorunu çözdü. Pratik kural: ana sürüm yükseltmelerinden sonra ilk derleme her zaman temiz Rebuild olmalı; "incremental build" eski runtime DLL'lerini paketleyebilir.

**Not 8 — System Tag ile İletişim Kopması Tespiti Sahada Vazgeçilmez**
Sahada PLC-HMI hattı zaman zaman kopan bir tesiste, operatör "veriler donuyor ama alarm yok" şikayeti getirdi. Sorun: ekrandaki Analog Numeric nesneleri son okunan değeri gösteriyordu; bağlantı koptuğunda değer "donuyor" ama görsel bir uyarı yoktu. Çözüm: controller iletişim durumu system tag'i (communication status) bir banner nesnesine bağlandı ve kopma anında kırmızı uyarı gösterildi. iX, controller offline olduğunda tag değerini sıfırlamaz — son değeri tutar; bu davranış mutlaka system tag ile maskelenmelidir.

**Not 9 — PC Runtime'da Softkey vs USB Dongle Yedekleme Farkı**
Bir PC tabanlı iX Runtime kurulumunda Softkey lisansı kullanıldı; disk imajı yedeklenip yeni donanıma geri yüklendiğinde Softkey geçersiz hale geldi (donanım parmak izi değişti) ve runtime trial moduna düştü — her 30 dakikada yeniden başlama. USB dongle bu sorundan muaftır (taşınabilir). Üretim kritik PC runtime'larda USB dongle, sanallaştırılmış/yedeklenen ortamlarda ise Softkey'in donanım bağımlılığı önceden değerlendirilmelidir.

**Not 10 — 260 Karakter Limiti Sadece Build'i Değil Reçete/Trend Export'unu da Vurur**
Dosya yolu 260 karakter limiti yalnızca derleme aşamasında değil, runtime'da reçete export, audit trail CSV export ve trend log yazımında da tetiklenir. Derin klasör yapısına sahip bir USB hedefine export yapan bir projede, runtime sessizce export'u atladı (hata mesajı görünmedi, dosya oluşmadı). Hedef export yolları kısa tutulmalı; mümkünse USB kök dizinine yazılmalıdır.

## Edge Case'ler ve Sistem Limitleri

iX Developer mimarisi belirli sınırlarda öngörülebilir biçimde davranır; ancak bu sınırların aşılması çoğu zaman açık bir hata mesajı yerine sessiz performans düşüşü veya beklenmedik davranışla sonuçlanır. Aşağıdaki tablo saha deneyimi ve resmi notlarla doğrulanmış pratik limitleri özetler.

| Alan | Pratik Limit / Eşik | Aşıldığında Davranış |
|---|---|---|
| Poll grubu sayısı | 5 (sabit) | 5'ten fazla farklı aralık gerekirse taglar uzlaşılan en yakın gruba sıkıştırılmalı |
| Minimum poll aralığı | ~25 ms (yüksek performanslı panel) | Düşük performanslı panellerde 25 ms istense bile fiili döngü süresi daha yüksek; iletişim doygunluğa ulaşır |
| OPC UA Server eş zamanlı oturum | 20 | 21. istemci bağlantısı reddedilir (BadTooManySessions benzeri) |
| Web Server portu | 7001 (HTTPS, iX3) | Port çakışması varsa Web Server sessizce başlamaz; tarayıcı erişimi kurulamaz |
| Dosya yolu uzunluğu | 260 karakter (Windows MAX_PATH) | Build/Rebuild/Run/Simulate ve runtime export başarısız |
| Aktif Data Logger | ~25 (öneri) | Daha fazlası iletişim ve disk I/O baskısı, panel donması |
| Ekran başına nesne | ~400 (öneri) | Ekran geçişi gecikmesi, render yavaşlaması |

**OPC UA Server ve array tag çelişkisi:** iX'in dahili OPC UA *Server*'ı array taglarını dışa açamaz. Bu, iX'i bir OPC UA *istemcisi* olarak kullanırken (CODESYS'e bağlanma — 02 numaralı belge) ayrı bir kısıttır: iX OPC UA istemcisi de array okuyamaz. Yani iX hem sunucu hem istemci tarafında array desteğinden yoksundur. Array gereken senaryoda ARTI driver veya array elemanlarının ayrı tag olarak modellenmesi gerekir.

**Internal tag persistency edge case:** Non-volatile işaretli internal taglar, kontrollü kapanışta (graceful shutdown) flash'a yazılır. Ani güç kesintisinde son birkaç saniyenin değişimi kaybolabilir — internal tag'ler bir UPS varsayımıyla "kalıcı" değildir, "düzenli kapanışta kalıcı"dır. Kritik üretim sayaçları PLC tarafında retain değişkende tutulmalı, HMI'da değil.

**System tag yazma sınırı:** System taglar çoğunlukla salt okunurdur; yazılabilir olanlara (ör. tarih/saat ayarı) bile runtime güvenlik bağlamında yazma engellenebilir. Bir system tag'e script ile yazma denemesi sessizce başarısız olabilir — dönüş değeri kontrol edilmeli.

**DEMO controller davranışı:** DEMO controller taglarına (M0–M99, D0–D99) yazılan değerler runtime'da gerçekten saklanmaz; analog taglar testere dişi / sinüs benzeri otomatik desenler üretir. Bu, ekran geliştirmede gerçek veri sanılıp yanlış ölçekleme yapılmasına yol açabilir; üretim öncesi DEMO controller mutlaka kaldırılmalıdır.

## Optimizasyon

iX Runtime performansının büyük kısmı iletişim katmanında (tag polling) ve render katmanında (ekran nesne sayısı) belirlenir. Aşağıdaki yaklaşımlar saha projelerinde ölçülebilir kazanım sağlar.

**1. Poll grubu segmentasyonu — en büyük kazanç kaynağı**
Tüm tagları tek poll grubuna koymak, en yavaş değişen tag'in (ör. 5 sn'lik bir sayaç) en hızlı tag'i (25 ms'lik alarm biti) yavaşlatmasına yol açmaz — fakat tüm taglar 25 ms'de okunursa iletişim kanalı gereksiz doygunluğa ulaşır. Doğru yaklaşım: kritik biti hızlı gruba, geri kalanı kademeli yavaş gruplara dağıtmak. Bir projede 800 tag'in tamamı 100 ms grupta iken döngü süresi 480 ms'ye çıkmıştı; %70 tag 1 sn gruba taşınınca kritik döngü 120 ms'ye indi.

**2. Ardışık adresleme ile telegram birleştirme**
Sürücüler ardışık PLC adreslerini (ör. M0.0–M11.7, D100–D150) tek bir okuma telegramında toplar. Dağınık adreslere yayılmış taglar her biri için ayrı telegram oluşturur. PLC tarafında HMI'ın okuduğu değişkenleri ardışık bir GVL bloğunda toplamak iletişim sayısını kat kat azaltır (bkz. 03 belgesi Not 5).

**3. Ekran nesne sayısı ve katmanlama**
Ekran başına nesneyi ~400 altında tutmak render süresini düşürür. Statik dekoratif öğeler (çerçeve, başlık) background ekrana taşınarak ön plan ekranın nesne yükü azaltılır. Görünmez ama tag'e bağlı nesneler bile poll yüküne katkıda bulunur — gizlenecek nesneler yerine ayrı ekran/popup tercih edilmelidir.

**4. Trend ve Data Logger örnekleme dengesi**
Trend Viewer eğri sayısı ve Data Logger örnekleme aralığı iletişimi doğrudan etkiler. 1 sn örneklemeli 10 eğrili bir trend, panelin iletişim bütçesinin önemli kısmını tüketebilir. Tarihsel analiz için 1–5 sn örnekleme yeterlidir; sub-saniye örnekleme yalnızca gerçek zamanlı kritik izlemede kullanılmalı.

**5. Driver güncelleme ve GEN2 tercihi**
GEN2 sürücüler kullanıcı modunda çalışır ve genellikle daha güncel iletişim yığınına sahiptir. Eski MPD sürücüden GEN2'ye geçiş, bazı PLC markalarında telegram optimizasyonu sayesinde ölçülebilir döngü iyileşmesi sağlar.

**6. OPC UA subscription vs polling**
OPC UA istemcisi olarak çalışırken, mantıksal olarak değişim bazlı subscription, sürekli polling'den daha verimlidir: sunucu yalnızca değişen değerleri yayınlar. Publishing interval'ı sampling interval'a göre doğru ayarlamak (publishing ≥ sampling) sunucuda kuyruk birikmesini önler.

## Derin Teknik Detay

**Tasarım/runtime ayrımının nedeni — neden derlenmiş paket?**
iX, projeyi yorumlanan bir XML/script ağacı olarak çalıştırmaz; Build aşamasında C# scriptleri gerçek .NET assembly'lerine derler ve ekran tanımlarını runtime'ın doğrudan yükleyebileceği bir pakete dönüştürür. Bunun nedeni performans ve belirlenebilirliktir: yorumlanan bir motor, gömülü panelin sınırlı CPU'sunda her tag değerlendirmesinde ayrıştırma maliyeti doğururdu. Derlenmiş model, scriptlerin runtime'da JIT/AOT maliyeti olmadan native hızda çalışmasını sağlar — bunun bedeli, her değişikliğin yeniden derleme ve transfer gerektirmesidir (canlı düzenleme yoktur). Bu, web tabanlı HMI'ların (anında yenilenen tarayıcı) aksine bir mühendislik tercihidir.

**Tag motorunun iç çalışması — neden poll grupları?**
iX tag motoru, her controller için bir iletişim iş parçacığı (driver thread) çalıştırır. Bu thread, atanan poll gruplarını sırayla döngüye sokar; her grubun aralığı dolduğunda o gruptaki taglar için okuma telegramı oluşturur. Tek bir global okuma aralığı yerine 5 grup sunulmasının nedeni, endüstriyel verinin doğal olarak heterojen frekanslı olmasıdır: bir acil durdurma biti ile bir günlük üretim toplamı aynı hızda okunmamalıdır. Grup modeli, geliştiriciye iletişim bütçesini elle dağıtma kontrolü verir — alternatif olan "her tag'in kendi aralığı" modeli (bazı SCADA'larda) daha esnek ama scheduler maliyeti yüksek ve gömülü panelde verimsizdir.

**Driver mimarisi — MPD vs GEN2 ve neden iki tip var?**
MPD (eski model) sürücüler iX Developer'ın kendi kurulum sürecine sıkı bağlıdır, yönetici yetkisi ve yeniden başlatma gerektirir çünkü sistem seviyesinde kaydedilir. GEN2 (Generic Driver Engine 2) ise iX'ten bağımsız, kullanıcı modunda yüklenip güncellenebilen modüler bir mimaridir. Bu ayrımın amacı, sürücü güncellemelerini iX Developer ana sürümünden ayrıştırmaktır: yeni bir PLC firmware'i çıktığında müşteri, tüm iX Developer'ı güncellemeden yalnızca ilgili GEN2 sürücüyü güncelleyebilir. Bu, uzun ömürlü endüstriyel kurulumlarda (10+ yıl) bakım maliyetini ciddi azaltır.

**WPF temeli neden Windows Forms değil?**
iX2'nin WPF (vektör tabanlı, GPU hızlandırmalı, dependency property modeli) üzerine kurulmasının nedeni, HMI'ların ölçeklenebilir grafik ve veri-bağlama (data binding) gereksinimidir. Dependency property sistemi, bir tag değerinin doğrudan bir görsel özelliğe (renk, konum) bağlanmasını çerçeve düzeyinde mümkün kılar — bu yüzden WPF User Control'ler tag'e bağlanabilirken, eski data-binding modeli olmayan Windows Forms kontrolleri bağlanamaz. iX3'ün .NET 8'e geçişi (scripting tarafında) NuGet ekosistemine ve modern dil özelliklerine erişim sağlarken, gömülü grafik katmanının soyutlanmasını korur.

**OPC UA Server'ın self-signed sertifikası — neden 20 yıl?**
iX OPC UA Server, ilk başlatmada otomatik bir self-signed sertifika üretir ve geçerlilik süresini 20 yıl olarak ayarlar. Bunun nedeni endüstriyel cihazların saha ömrüdür: bir CA altyapısı olmayan izole tesiste, kısa ömürlü bir sertifikanın yenilenmesi operatör müdahalesi gerektirir ve süresi dolduğunda iletişim sessizce kopabilir. 20 yıl, pratik olarak cihaz ömrünü kapsar. Bu tercih güvenlik (kısa rotasyon) ile saha güvenilirliği (kesintisiz çalışma) arasında bilinçli bir dengedir — yüksek güvenlik gereken ortamlarda harici CA imzalı sertifika ile değiştirilmelidir.

## İlgili Konular

```
knowledge/hmi/ix-developer/
├── 01_architecture.md       ← Şu an buradasınız
├── 02_codesys_connection.md → iX Developer + CODESYS entegrasyonu
├── 03_screen_design.md      → Ekran tasarımı, ISA-101 uygulaması
└── 04_scripting.md          → C# scripting, WPF kontrolleri, .NET assembly

Genel HMI mimarisi:
knowledge/hmi/architecture/
├── 01_hmi_patterns.md       → ISA-101 mimari çerçeve, ekran hiyerarşisi
├── 02_realtime_data.md      → OPC UA subscription, Modbus polling
├── 03_alarm_management.md   → ISA-18.2, alarm state machine
└── _synthesis.md            → Dört katmanın birleşik zihin haritası

Protokol katmanı (iX Developer OPC UA istemci kullanımıyla ilgili):
knowledge/protocols/opc-ua/  → OPC UA sunucu mimarisi ve subscription detayları

Standartlar:
  FDA 21 CFR Part 11  → Audit Trail FDA modu uyumluluğu
  ISA-101.01-2015     → HMI ekran tasarım standartları
  ISA-18.2-2016       → Alarm yönetimi yaşam döngüsü
```
