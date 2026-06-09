---
KONU        : iX Developer — Ekran Tasarımı
KATEGORİ    : hmi
ALT_KATEGORI: ix-developer
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://www.beijerelectronics.com/docs/iX-251-Reference/en/objects.html"
    başlık: "iX Developer 2.51 Reference — Objects"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-251-Reference/en/tags.html"
    başlık: "iX Developer 2.51 Reference — Tags"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-251-Reference/en/ribbon-tabs.html"
    başlık: "iX Developer 2.51 Reference — Ribbon Tabs"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-251-Reference/en/development-environment.html"
    başlık: "iX Developer 2.51 Reference — Development Environment"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-250-Reference/en/alarm-management.html"
    başlık: "iX Developer 2.50 Reference — Alarm Management"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-251-Reference/en/trend-viewer.html"
    başlık: "iX Developer 2.51 Reference — Trend Viewer"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX/3.0/User-Guide/en/objects.html"
    başlık: "iX Developer 3.0 User Guide — Objects"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-User/en/navigation-and-screen-jumps.html"
    başlık: "iX Developer User Guide — Navigation and Screen Jumps"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX/3.0/User-Guide/en/actions.html"
    başlık: "iX Developer 3.0 User Guide — Actions"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/ix-user/en/dynamics.html"
    başlık: "iX Developer User Guide — Dynamics"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX/3.1/User-Guide/en/screens.html"
    başlık: "iX Developer 3.1 User Guide — Screens"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-253-Reference/en/working-with-projects.html"
    başlık: "iX Developer 2.53 Reference — Working with Projects"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX/3.0/User-Guide/en/optimize-performance.html"
    başlık: "iX Developer 3.0 User Guide — Optimize Performance"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-250-Reference/en/tags.html"
    başlık: "iX Developer 2.50 Reference — Tags (Binding & Expressions)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/en/Products/software/ix-hmi-software/efficient-workflow/Template___screens"
    başlık: "Beijer Electronics — Template Screens Feature Overview"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/en/Products/software/ix-hmi-software/efficient-workflow/Alias"
    başlık: "Beijer Electronics — Alias Feature Overview"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/en/Products/software/ix-hmi-software"
    başlık: "iX2 HMI Software — Beijer Electronics Ürün Sayfası"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/en/Products/software/ix-hmi-software/Vimeo___video___page"
    başlık: "iX Developer 2 — Tutorial Video Listesi"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "knowledge/hmi/ix-developer/01_architecture.md"
    ilişki: gerektirir
  - konu: "knowledge/hmi/ix-developer/02_codesys_connection.md"
    ilişki: gerektirir
  - konu: "knowledge/hmi/ix-developer/04_scripting.md"
    ilişki: tamamlar
  - konu: "knowledge/hmi/architecture/01_hmi_patterns.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "iX Developer kurulumu ve temel proje oluşturma (01_architecture.md)"
  - "Controller bağlantısı ve tag yapısı (02_codesys_connection.md)"
  - "ISA-101 yüksek performanslı HMI ilkeleri (hmi/architecture/01_hmi_patterns.md)"
ÇELİŞKİLER :
  - kaynak: "iX Developer 2.xx (X2 serisi) vs iX Developer 3.xx (X3 serisi)"
    konu: >
      iX Developer 2.xx sürümleri X2 panel serisi için, 3.xx sürümleri X3 panel serisi
      içindir. İki sürüm arasında proje dosyası uyumsuzluğu vardır; bazı özellikler
      3.0'da başlangıçta eksikti (sonradan 3.1/3.2 ile eklendi). Bu belgede
      çoğunlukla 2.xx/2.5x referansları kullanılmıştır çünkü X2 serisi yaygın
      kullanımda olmaya devam etmektedir. 3.xx'e özgü farklılıklar ilgili yerlerde
      belirtilmiştir.
    çözüm: >
      Mevcut projenizin hedef paneline göre doğru sürümü kullanın.
      X2 serisi → iX Developer 2.5x; X3 serisi → iX Developer 3.x
  - kaynak: "Dinamikler ile Script çakışması"
    konu: >
      Bir nesnenin belirli bir özelliği için hem Dynamics sekmesinde dinamik ayar
      yapılmış hem de C# script ile aynı özellik değiştirilmeye çalışılırsa
      dinamik ayar devre dışı kalır; script öncelik kazanır.
    çözüm: >
      Her özellik için yalnızca bir yöntem kullanın: ya Dynamics sekmesi ya script.
      İkisi aynı anda aynı özelliğe uygulanamaz.
  - kaynak: "Alias kısıtlamaları"
    konu: >
      Alias kullanan ekranlar arka plan (background) veya ön plan (foreground)
      ekran olarak başka ekranlara atıfta bulunamaz. Ayrıca array tag, expression
      ve TrendViewer nesnesiyle Alias çalışmaz.
    çözüm: >
      Arka plan ekran gereken yerlerde Alias yerine doğrudan ekran kopyalama veya
      Component Library yeniden kullanımı tercih edin.
  - kaynak: "ISA-101'in iX Developer'da resmi desteği"
    konu: >
      Beijer Electronics resmi belgelerinde ISA-101 uyumluluğuna veya
      ISA-101 özelinde hazır renk şemalarına atıfta bulunulmamaktadır.
      iX Developer, ISA-101'i otomatik uygulayan bir "high performance HMI modu"
      sunmamaktadır.
    çözüm: >
      ISA-101 ilkeleri (gri nötr arka plan, kırmızının yalnızca alarm için
      kullanılması vb.) geliştiricinin bilinçli tasarım kararlarıyla uygulanmalıdır.
      iX Developer'daki Quick Styles ve Component Library bu ilkeleri tutarlı
      biçimde hayata geçirmeye yardımcı olur.
---

## Özün Ne

Beijer iX Developer, Beijer Electronics X2 (sürüm 2.xx) ve X3 (sürüm 3.xx) serisi operatör panelleri ile PC tabanlı uygulamalar için tasarlanan grafik HMI geliştirme ortamıdır. Ekran tasarımı, iX Developer projesinin görsel katmanını oluşturur: controller tag'lerine bağlı dinamik nesneler, navigasyon yapısı, alarm izleme, trend görüntüleme ve operatör etkileşimleri bu katmanda tanımlanır. Endüstriyel güvenilirlik ve ISA-101 yüksek performanslı HMI ilkeleri, iX Developer'da doğrudan uygulama katmanında tasarımcının sorumluluğundadır.

## Nasıl Çalışır

### Geliştirme Ortamı

iX Developer, şerit arayüzü (ribbon) tabanlı bir masaüstü IDE'dir. Temel bileşenler:

```
┌───────────────────────────────────────────────────────────────┐
│  Şerit Sekmeleri: Home | Project | System | Dynamics | Actions│
├───────────────────┬───────────────────────────────────────────┤
│  Project Explorer │         Tasarım Alanı (Desktop)           │
│  ─────────────    │   (Aktif ekran veya yapılandırma sayfası) │
│  Screens          │                                           │
│    Screen1        │   [Nesne sürükle & bırak]                 │
│    Screen2        │   [Boyutlandır, hizala]                   │
│  Functions        │   [Tag bağla]                             │
│  Data Loggers     │                                           │
│  Script Modules   ├───────────────────────────────────────────┤
│  Recipes          │  Özellik Izgarası (Property Grid)         │
└───────────────────┴───────────────────────────────────────────┘
```

Project Explorer beş ana grubu barındırır: **Screens**, **Functions**, **Data Loggers**, **Script Modules**, **Recipes**.

### Şerit Sekmeleri ve İşlevleri

Şerit sekmeleri bağlama duyarlıdır (context-sensitive): Bir nesne seçildiğinde ilgili sekmeler aktif olur.

| Sekme | İçerik |
|---|---|
| **Home** | Clipboard, Screen, Objects, Font, Format, Tag/Security, Name, Design Language |
| **Dynamics** | Layout (Move, Size), Color (Fill, Outline), General (Visible, Blink) |
| **General** | Nesneye özgü özellikler (ölçek, stil, gösterim formatı) |
| **Actions** | Tetikleyici-eylem çiftleri (Click → ShowScreen, Toggle, SetAnalog vb.) |
| **Project** | Build, Run, Simulate, Transfer (panele yükleme) |
| **System** | Tarih/saat, buzzer, arka ışık, OPC UA sunucusu, web sunucusu |

### Ekran Hiyerarşisi

```
iX Developer Projesi
│
├── Startup Screen  (ilk açılan, herhangi bir ekran atanabilir)
├── Normal Screens
│     ├── Background/Foreground Screen (ortak öğeler, navigasyon)
│     └── Popup Screens (modal/non-modal yüzer pencereler)
└── Template Screens (farklı projelerde yeniden kullanılabilir)
```

Ekranlar **Screen Groups** ile hiyerarşik olarak düzenlenebilir. Her ekranın üç kimliği vardır:
- **Screen Name**: iX Developer içindeki tanımlayıcı
- **Screen Title**: Çalışma zamanında popup başlığında görünür
- **Screen ID**: Sayısal kimlik; tag üzerinden programatik ekran geçişi için kullanılır

### Nesne Modeli

Her nesne şu temel özelliklere sahiptir:
- **Konum/Boyut**: Left, Top, Height, Width (piksel)
- **Tag Bağlantısı**: Home → Tag/Security grubu üzerinden atanır
- **Dinamikler**: Dynamics sekmesi ile tag değerine bağlı davranış
- **Eylemler**: Actions sekmesi ile kullanıcı etkileşimine karşılık
- **Güvenlik**: Security Group; hangi operatör grubunun nesneyi görebileceğini/kullanabileceğini belirler

## Pratikte Nasıl Kullanılır

### 1. Ekran Yönetimi ve Sayfa Yapısı

**Yeni ekran oluşturma:**
1. Home → Screen grubu → Add Screen
2. Ekran adı girin (harf ile başlayan alfanümerik)
3. Opsiyonel: Ekrandan sağ tıklayıp "Set as Startup Screen" seçeneği ile başlangıç ekranı atayın

**Arka plan ekranı (background screen):**
1. Ortak navigasyon barı, şirket logosu, alarm banner gibi tekrar eden öğeleri ayrı bir ekrana koyun
2. Bu ekranı arka plan olarak kullanmak isteyen ekranı açın
3. Home → Parent Screen → Background seçin
4. Arka planda yapılan değişiklikler bağlı tüm ekranlara otomatik yansır

**Popup ekran:**
- Herhangi bir ekranı popup olarak davranacak şekilde yapılandırabilirsiniz
- Show Screen action ile popup pozisyonu (X, Y koordinatları) ve boyutu belirlenir
- Modal popup: Alt ekranla etkileşimi engeller

### 2. Nesneler (Objects)

Nesneler Home → Objects grubundan ekrana sürüklenerek eklenir. İki ana kategori:

#### Gösterge Nesneleri (Read-Only)

| Nesne | Kullanım |
|---|---|
| **Analog Numeric** | Sayısal tag değerini gösterir. Format: tamsayı, ondalık, string, hex, binary. Sıfır doldurma ve karakter kısıtlaması yapılandırılabilir. |
| **Text Object** | Salt okunur metin; statik veya tag değerine bağlı dinamik içerik. |
| **Circular Meter** | Kırmızı/sarı/yeşil bölgeli kadran göstergesi. 0-360° açı aralığı yapılandırılabilir. İbre hareketi yumuşatma (smooth movement) desteği var. |
| **Linear Meter** | Yatay veya dikey çubuk göstergesi. Bölgeler ve ölçek yapılandırılabilir. |
| **Progress Bar** | Analog değeri ölçeksiz çubuk olarak gösterir. |
| **Multi Picture** | Tag değer aralığına göre farklı resim gösterir (motor çalışıyor/durmuş/arıza). |
| **Digital Clock** | Tarih, saat, gün bilgisi; özelleştirilebilir format. |

#### Giriş Nesneleri (Read/Write)

| Nesne | Kullanım |
|---|---|
| **Button** | Metin ve/veya resim gösterebilir. Actions sekmesiyle görevler atanır. Belirli bir tag değerini yazma, ekran geçişi, alarm onaylama vb. |
| **Slider** | Tag'e bağlı sayısal değeri ayarlar. Yatay/dikey yönelim, ölçek yapılandırması var. |
| **Touch Combo Box** | Açılır listeden metin seçimi; özelleştirilebilir öğe yüksekliği ve kaydırma hassasiyeti. |
| **Touch List Box** | Önceden tanımlı metin listesi; ayraç ve kaydırma seçenekleri. |
| **Roller Panel** | Belirli tag değerlerine karşılık gelen metinleri döngüsel kaydırma ile gösterir. |

#### İzleme Nesneleri

| Nesne | Kullanım |
|---|---|
| **Trend Viewer** | Tag değerlerini zaman ekseninde gösterir; birden fazla eğri (pen/curve) desteği. |
| **Alarm Viewer** | Alarm öğelerini listeler; onaylama, temizleme, filtreleme düğmeleri yapılandırılabilir. |
| **Chart** | Dizi (array) tag değerlerini alan, çubuk, pasta, çizgi, radar formatında gösterir. |
| **Database Viewer** | Veritabanı içeriğini tablo olarak gösterir. |
| **Audit Trail Viewer** | Operatör değişikliklerini loglar ve gösterir. |

### 3. Tag Bağlama (Data Binding)

Tag bağlama, bir nesneyi controller veya internal tag'e bağlar:

```
Adımlar:
1. Nesneyi ekrana ekleyin
2. Nesneyi seçin
3. Home → Tag/Security grubu → Tag açılır listesi
4. Listeden controller tag, internal tag veya system tag seçin
5. İsteğe bağlı: Expression ekleyin (örn. değeri 0-100 aralığına normalize etmek için)
```

**Tag türleri:**

| Tür | Açıklama |
|---|---|
| **Controller Tag** | Harici denetleyiciye (PLC, sürücü) bağlı. Adres ataması gerekir. |
| **Internal Tag** | Proje içi; controller bağlantısı yok. Non-Volatile seçeneğiyle yeniden başlatmada korunabilir. |
| **System Tag** | Sistem değişkenleri: tarih/saat, bellek kullanımı, CPU yükü, iletişim durumu vb. |

**Ölçekleme (Scaling):**
Yalnızca controller tag'lere uygulanır.
```
Panel değeri = Offset + (Gain × Register değeri)
```

**Index Register:**
Birden fazla controller istasyonunu tek nesneyle göstermek için kullanılır.
```
I1:D10 sözdizimi:
  → Index 1 kaydının içeriği, okunacak controller adresini belirler
  → Aynı nesne, index değeri değiştirilerek farklı makine verilerini gösterebilir
```

**Expressions:**
Tek satırlık C# ifadeleri; tag değeri ekrana yansımadan önce dönüştürülür.
```csharp
// Varsayılan: değeri olduğu gibi göster
value

// Bit çıkartma örneği: 16 bit word'ün 3. biti
(value >> 3) & 1

// Dinamik offset örneği
value + offset_tag_value
```

### 4. Dinamik Özellikler (Dynamic Properties)

Dynamics sekmesi, nesne özelliklerini tag değerine bağlı olarak değiştirmek için kullanılır.

**Görünürlük (Visible):**
```
Dynamics → General grubu → Visible
→ Tag seçin
→ Tag değeri 0 olduğunda nesne görünmez olur
Öncelik sırası: Güvenlik > Görünürlük > Blink
```

**Renk Dinamiği (Fill / Outline Color):**
```
Dynamics → Color grubu → Fill
→ Tag seçin
→ "Add" ile tag değer aralıkları ekleyin
→ Her aralığa renk atayın (düz renk veya gradyan)
Örnek:
  0-40    → Gri  (normal durum — ISA-101 uyumlu)
  40-80   → Sarı (uyarı)
  80-100  → Kırmızı (alarm)
```

**Yanıp Sönme (Blink):**
```
Dynamics → General grubu → Blink
→ Etkinleştirme koşulu: tag değeri belli bir değere eşitken blink aktif
→ Frekans da tag üzerinden dinamik olarak kontrol edilebilir
Kural: Aktif-onaylanmamış alarm → blink açık; onaylandıktan sonra → sabit
```

**Hareket (Move) ve Boyut (Size):**
```
Dynamics → Layout grubu → Move
→ Tag seçin, başlangıç/bitiş değerleri ve karşılık gelen X/Y koordinatları tanımlayın
→ Nesne, tag değerine göre ekranda yer değiştirir

Dynamics → Layout grubu → Size
→ Genişlik ve yükseklik tag'lere bağlanır
→ Nesneler soldan sağa ve yukarıdan aşağıya doğru büyür/küçülür
```

**Dinamikler ve Script çakışması:**
Bir özellik için Dynamics sekmesinde dinamik yapılandırma varsa, aynı özelliği C# script'ten değiştirmek dinamik ayarı devre dışı bırakır. Her özellik için yalnızca bir yöntem kullanın.

### 5. Navigasyon

**Navigation Manager:**
```
Adımlar:
1. View → Navigation Manager
2. Mevcut ekranlar şematik olarak görünür
3. Bir ekrandan diğerine sürükleyerek bağlantı oluşturulur
4. Bağlantı noktasına otomatik olarak navigasyon butonu eklenir
```

**Ekran geçiş eylemleri (Actions sekmesi):**

| Eylem | Açıklama |
|---|---|
| **Show Screen** | Belirtilen ekranı açar. Popup ekranlar için konum (X,Y) belirlenebilir. |
| **Show Next / Previous Screen** | Sıradaki/önceki ekrana geçer. |
| **Show Start Screen** | Başlangıç ekranına döner. |
| **Close Screen** | Mevcut ekranı (özellikle popup) kapatır. |

**Üç tıklama kuralı (ISA-101):**
Tüm kritik ekranlara ≤ 3 tıklamayla ulaşılabilmeli. Navigation Manager kullanılırken bu kural proje başından itibaren gözetilmelidir. (Kaynak: ISA-101 hiyerarşi ilkeleri — bkz. `hmi/architecture/01_hmi_patterns.md`)

### 6. Alarm Viewer

Alarm sistemi iki katmandan oluşur: **Alarm Sunucusu (Alarm Server)** yapılandırması ve **Alarm Viewer** nesnesi.

**Alarm Sunucusu:**
```
Alarm durumları:
  Aktif        : Koşul sağlandı, onaylanmadı
  Pasif        : Normale döndü, onaylanmadı
  Onaylandı    : Koşul devam ediyor, onaylandı
  Normal       : Koşul sona erdi ve onaylandı

Alarm öğesi yapılandırması:
  → Tetikleyici: Tag değeri + karşılaştırma operatörü (>, <, =, yükselen kenar vb.)
  → Öncelik grubu (Group): Birden fazla grup desteklenir
  → Eylemler hiyerarşisi: Alarm öğesi → Grup → Sunucu (atlanmışsa üst seviye devreye girer)
  → Alarm göstergesi: Aktif alarm varken kırmızı yanıp söner; onaylanmışsa sabit renk
```

**Alarm Viewer nesnesi — yapılandırma:**
```
General sekmesi → Sütun seçimi (Zaman, Açıklama, Durum, Grup vb.)
General sekmesi → Butonlar: Acknowledge Selected, Acknowledge All, Clear, Filter
Maksimum satır: 200 (performans önerisi)
```

**ISA-101 uyumlu alarm renk şeması:**
```
Aktif-Onaylanmamış  : Kırmızı + blink (en yüksek dikkat talebi)
Aktif-Onaylandı     : Kırmızı sabit
Pasif-Onaylanmamış  : Sarı/turuncu + blink (bilgi, müdahale bekleniyor)
Normal              : Gri/beyaz (satır listeden çıkarılabilir veya soluk gösterilir)
```

### 7. Trend Viewer

**Trend Viewer yapılandırması:**
```
Adımlar:
1. Home → Objects → Trend Viewer'ı ekrana sürükle
2. Nesneyi seçince General sekmesi aktif olur
3. General → Edit Curves → Yeni eğri ekle
4. Her eğri için:
   → Ad (legend'da görünür)
   → Kaynak: Tag (gerçek zamanlı, RAM'den) veya Log Item (Data Logger'dan, tarihsel)
   → Expression (opsiyonel)
   → Renk ve çizgi kalınlığı
   → Min/Max değer için tag (dinamik Y ekseni)
```

**Zaman ekseni ve tarihsel mod:**
```
Time Span: Görüntülenen süre aralığı (örn. son 10 dakika)
         Tag'e bağlanabilir → operatör çalışma zamanında değiştirebilir
Tarihsel mod: Data Logger log item gerektirir
            Zaman ekseni başlangıç/bitiş tarih-saat gösterir
            Time Span tag değiştirilince sistem Data Logger'dan eski veriyi çeker
            → Çok eğrili ve uzun zaman aralıklı grafiklerde gecikme yaşanabilir
```

**Performans uyarısı:**
Çok sayıda eğri ve kısa örnekleme aralığı iletişim performansını olumsuz etkiler. Ekran başına trend viewer eğrisi sayısını minimumda tutun.

### 8. Şablonlar ve Yeniden Kullanım

#### Arka Plan Ekranı (Background Screen)
Ortak navigasyon barı, şirket logosu, alarm özet bölümü gibi tüm ekranlarda tekrar eden öğeler için kullanılır.
```
Avantajı: Arka plan ekranda yapılan değişiklik bağlı tüm ekranlara anında yansır.
Kısıtı : Alias kullanan ekranlar background/foreground olarak kullanılamaz.
```

#### Alias — Ekran Düzeyinde Parametre
Alias, bir ekranı farklı tag kümesiyle tekrar kullanmayı sağlar. "Bir ekranın özelliği olarak düşünülmeli; bir tag'in yerini tutan yer tutucu."
```
Kullanım senaryosu:
  Motor_Detail adlı tek bir ekran tasarlayın.
  Motor1 için: Alias = Motor1_Speed, Motor1_Current, Motor1_Fault
  Motor2 için: Alias = Motor2_Speed, Motor2_Current, Motor2_Fault
  Aynı ekran farklı instance olarak her motor için gösterilir.

Alias kısıtları:
  ✗ Array tag ile çalışmaz
  ✗ Expression ile birlikte kullanılamaz
  ✗ TrendViewer nesnesiyle uyumsuz
  ✗ Background/Foreground ekran olarak kullanılamaz
```

#### Component Library — Nesne Yeniden Kullanımı
Component Library, projenin ve gelecekteki projelerin genelinde kullanılabilecek yeniden kullanılabilir nesne gruplarını saklar.
```
Nasıl eklenir:
  Ekranda bir nesne veya nesne grubu seçin
  Kopyalayıp Component Library penceresine yapıştırın
  Script kodları da bileşen olarak sürüklenip eklenebilir

Kategoriler: Önceden tanımlı nesneler, gruplar, medya dosyaları
Export/Import: Projeler arası taşıma desteklenir
```

#### Ekran Şablonları (Screen Templates)
Kaydedilen ekran, mevcut projede ve gelecekteki projelerde şablon olarak kullanılabilir.
```
Fayda: Kurumsal görsel kimlik tutarlılığı
       Bireysel arka plan ekranları yerine merkezi şablonlarla bakım kolaylığı
Destekleyen özellikler: Alias, Reusables, Cross Reference, Import/Export
```

### 9. Çoklu Çözünürlük Desteği

```
PC hedefleri için çözünürlük seçimi:
  Desteklenen değerler: 1920×1080, 1280×800, 800×600, 640×480
  Proje oluşturulurken seçilir; sonradan Project → Settings'ten değiştirilebilir.
  Çözünürlük değiştirildiğinde iX Developer grafikleri otomatik olarak yeniden boyutlandırır.

Panel hedefleri için:
  Proje sihirbazında (wizard) hedef panel seçilir.
  Panel'in teknik verilerinde çözünürlük görüntülenir.
  Çoğu panel için döndürülmüş görünüm (rotated view) desteği mevcuttur.
  X2 base v2: 5", 7", 10" seçenekleri — widescreen (geniş ekran) format

Öneri:
  Projenin başında hedef panel belirlenmeli ve tüm ekranlar bu çözünürlüğe göre tasarlanmalıdır.
  Panel değiştirilmesi gerekirse otomatik yeniden boyutlandırma yardımcı olur ama özel konumlandırmalar gözden geçirilmelidir.
```

### 10. ISA-101 Yüksek Performanslı HMI İlkelerinin iX'te Uygulanması

ISA-101 ilkeleri iX Developer'da otomatik uygulanmaz; geliştiricinin tasarım kararlarıyla hayata geçirilir. (Bkz. `hmi/architecture/01_hmi_patterns.md` — ISA-101 detayları burada tekrarlanmamıştır.)

**Renk paleti — iX Developer uygulaması:**
```
Normal durum nesneleri:
  → Quick Styles'tan açık gri dolgu seçin
  → Motor çalışıyor: Açık gri arka plan, beyaz metin "RUNNING"
  → Motor durmuş: Koyu gri arka plan, beyaz metin "STOPPED"

Dynamics → Fill:
  → Kırmızıyı YALNIZCA alarm/arıza koşuluna bağlayın
  → Sarıyı uyarı koşuluna bağlayın
  → Normal durum: gri (renksiz)

Alarm Viewer:
  → Aktif-onaylanmamış: kırmızı + blink
  → Onaylandı: kırmızı sabit
  → Pasif-onaylanmamış: sarı
```

**Ekran hiyerarşisi — iX uygulaması:**
```
Level 1 (Genel Bakış): 1 ekran
  → Tesis/hat özeti, KPI, aktif alarm sayısı
  → Minimum nesne sayısı, en basit içerik
  → Background screen: şirket logosu + navigasyon barı

Level 2 (Alan/Hat): Her hat/bölüm için 1-3 ekran
  → Ekipman listesi, kritik değerler
  → Trend Viewer: son 1 saat trendi

Level 3 (Detay): Her ekipman için 1 ekran (Alias kullanın)
  → Tüm ölçümler, setpoint kontrolleri, komut butonları
  → Alarm Viewer: yalnızca o ekipmanın alarmaları

Level 4 (Destek): Bakım/kalibrasyon ekranları
  → Tarihsel trend (Data Logger bağlı)
  → Tanı bilgileri
```

**Yazma doğrulaması — iX uygulaması:**
```
Kritik butonlar için iki adımlı onay:
1. Butona Actions sekmesinden script çağrısı ekleyin
2. Script'te onay popup ekranı gösterin (Show Screen — modal popup)
3. Popup'taki "Evet" butonu asıl eylemi gerçekleştirir
4. Popup'taki "İptal" butonu Close Screen ile kapatılır

iX Developer'da yerleşik onay dialog yok → C# script veya popup ekranla uygulanır.
(Bkz. 04_scripting.md)
```

**Animasyon minimizasyonu — iX uygulaması:**
```
İSA-101'e göre:
  ✗ Kaçınılacaklar: Dönen grafikler, akan sıvı animasyonları, sürekli renk değişimi
  ✓ Kabul edilenler: Alarm durumunda blink (onaylanana kadar), seviye çubuklarının
                     anlık güncellenmesi (animasyon değil gerçek veri)

iX Developer'da blink:
  → Dynamics → Blink → Tag değerine bağla
  → Yalnızca aktif-onaylanmamış alarm için etkinleştir
  → Onaylanma sonrası blink kaynağı olan alarm tag'i 0'a döner → blink durur
```

## Örnekler

### Örnek 1: Motor Detay Ekranı (Alias Kullanımı)

```
Senaryo: 8 adet aynı tip motor, her biri için ayrı detay ekranı gerekiyor.

Çözüm: Alias ile tek ekran, 8 instance.

1. "Motor_Detail" ekranı oluşturun
2. Aliases tanımlayın:
   - spd_actual  (gerçek hız)
   - spd_setpt   (hız setpoint)
   - current     (akım)
   - temp        (sıcaklık)
   - run_cmd     (çalıştır komutu)
   - stop_cmd    (durdur komutu)
   - fault_bit   (arıza biti)

3. Ekranda nesneleri bu alias'lara bağlayın:
   - Analog Numeric → spd_actual
   - Slider → spd_setpt
   - Analog Numeric → current
   - Linear Meter → temp (0-120°C, 90°C üzeri kırmızı bölge)
   - Button "Başlat" → run_cmd tag'ine 1 yaz (SetTag action)
   - Button "Durdur" → stop_cmd tag'ine 1 yaz
   - Multi Picture → fault_bit (0=gri, 1=kırmızı "ARIZA")

4. Show Screen action'da her motor için farklı alias mapping yapın:
   Motor1: spd_actual=M1.Speed, spd_setpt=M1.Setpoint, ...
   Motor2: spd_actual=M2.Speed, spd_setpt=M2.Setpoint, ...
```

### Örnek 2: ISA-101 Uyumlu Renk Dinamiği

```
Senaryo: Kazan sıcaklığı göstergesi. Normal: 80-120°C, Uyarı: >120°C, Alarm: >140°C

Circular Meter nesnesi:
  General → Min: 0, Max: 180
  General → Regions (bölgeler):
    0-80°C    → Koyu gri (soğuk, normal değil ama tehlikeli değil)
    80-120°C  → Açık gri (normal çalışma — ISA-101: nötr)
    120-140°C → Sarı     (uyarı)
    140-180°C → Kırmızı  (alarm)

Analog Numeric (sıcaklık sayısı):
  Tag: Kazan.Sicaklik
  Dynamics → Fill:
    0-120    → Gri arka plan
    120-140  → Sarı arka plan
    140-180  → Kırmızı arka plan
  Dynamics → Blink:
    Tag: Alarm_Kazan_Sicaklik (alarm sistemi tarafından set edilir)
    → Alarm aktif ve onaylanmamışken yanıp söner
```

### Örnek 3: Navigasyon Yapısı (Navigation Manager)

```
Ana ekranlar hiyerarşisi:
  Overview (Startup Screen)
    ├── Line1_Area
    │     ├── Motor_Detail [Alias: Line1_Motor1]
    │     ├── Motor_Detail [Alias: Line1_Motor2]
    │     └── Conveyor_Detail
    ├── Line2_Area
    │     └── (benzer yapı)
    ├── Alarms (Alarm Viewer)
    └── Reports

Background Screen: NavBar
  → Logo, "Ana Sayfa" butonu, alarm özet banner
  → TÜM ekranlara arka plan olarak atanır (Alias kullananlar hariç)
  → Alarm banner: Alarm Viewer mini-versiyon veya sistem tag ile aktif alarm sayısı

Navigasyon kuralı kontrolü:
  Overview → Line1_Area → Motor_Detail = 2 tıklama ✓ (hedef ≤3)
  Overview → Alarms = 1 tıklama ✓
```

### Örnek 4: Trend Viewer Yapılandırması

```
Ekran: Motor1 Detay → Trend sekmesi

Trend Viewer nesnesi:
  General → Edit Curves:
    Eğri 1: Ad="Hız", Tag=M1.Speed,   Renk=Mavi,   Min=0, Max=150
    Eğri 2: Ad="Akım", Tag=M1.Current, Renk=Turuncu, Min=0, Max=30
    Eğri 3: Ad="Sıcaklık", Log Item=DataLogger1.M1Temp, Renk=Kırmızı

  Zaman ekseni: Time Span Tag = TrendTimeSpan (operator seçiyor: 10dk/1sa/8sa)

  Butonlar (Actions):
    [Gerçek Zamanlı] → TrendTimeSpan = 600 (10 dakika)
    [Son 1 Saat]     → TrendTimeSpan = 3600
    [Son 8 Saat]     → TrendTimeSpan = 28800 (Data Logger gerektirir)
```

## Sık Yapılan Hatalar

### Hata 1: Alias Ekranını Background Olarak Kullanmaya Çalışmak

```
Hata:
  Motor_Detail ekranı Alias kullanıyor.
  Bu ekranı NavigationBar ekranının arka planı olarak atamaya çalışıyorsunuz.
  iX Developer buna izin vermez.

Çözüm:
  Alias kullanan ekranlar background/foreground olamaz.
  Ortak öğeleri (navigasyon barı) ayrı bir ekrana koyun,
  bu ekranı tüm Alias'sız ekranlara background olarak atayın.
  Alias ekranlara ortak öğeleri Component Library'den kopyalayın.
```

### Hata 2: Dynamics ve Script Çakışması

```
Hata:
  Fill Color dinamiği yapılandırılmış bir nesnenin arka plan rengini
  script ile değiştirmeye çalışıyorsunuz.
  Script çalışıyor gibi görünüyor ama dinamik ayar artık çalışmıyor.

Çözüm:
  İki yöntem aynı anda aynı özelliğe uygulanamaz.
  Ya tamamen Dynamics sekmesini kullanın (önerilen, basit durumlarda)
  ya da tamamen script kullanın (karmaşık koşullar için).
  Değiştirmek için Dynamics → Clear Dynamics yapın, sonra script'e geçin.
```

### Hata 3: Trend Viewer'ı Tarihsel Veri Olmadan Kullanmak

```
Hata:
  Time Span'ı 8 saate çekiyorsunuz ama Data Logger yapılandırmadınız.
  Trend Viewer yalnızca RAM'deki anlık önbelleği gösterebilir.
  8 saatlik veri yok.

Çözüm:
  Tarihsel trend için Data Logger → Log Item oluşturun.
  Trend Viewer eğrisini Log Item'a bağlayın (doğrudan Tag değil).
  Data Logger örnekleme aralığını ve saklama süresini ayarlayın.
  Maksimum 25 aktif Data Logger önerilir.
```

### Hata 4: Alarm Viewer Satır Sayısını Aşmak

```
Hata:
  1000 alarm öğesi yapılandırıldı.
  Alarm Viewer yüklenmesi çok yavaş; ekran geçişleri donuyor.

Çözüm:
  Alarm Viewer maksimum satır sayısını 200'de tutun.
  Alarm öğesi sayısını 500'ün altında tutmaya çalışın.
  Alarm grupları ile filtreleyin: Her detay ekranında yalnızca
  ilgili ekipmanın alarmlarını gösteren filtreli Alarm Viewer kullanın.
```

### Hata 5: Ekran Başına 400'den Fazla Nesne

```
Hata:
  Ana ekrana 600 nesne eklenmiş.
  Ekran geçişleri yavaş, panel yanıt vermiyor.

Çözüm:
  Ekran başına 400 nesneden az tutun (resmi öneri).
  ISA-101 ekran hiyerarşisini uygulayın: Tek ekranda tüm bilgiyi
  göstermeye çalışmak hem performans hem operatör etkinliği açısından yanlış.
  Level 3 detay ekranlarına bölün.
```

### Hata 6: Kırmızıyı Renk Kodlaması Olarak Kullanmak (ISA-101 ihlali)

```
Hata:
  "Motor çalışıyor" durumu için yeşil, "durmuş" için kırmızı renk kullanılıyor.
  Bir alarm geldiğinde operatör gerçek alarmdaki kırmızıyı fark etmiyor.

Çözüm (ISA-101):
  Motor çalışıyor → Açık gri dolgu, "RUNNING" metni
  Motor durmuş    → Koyu gri dolgu, "STOPPED" metni
  Kırmızı renk YALNIZCA alarm/arıza koşuluna ayrılmıştır.
  iX Developer Dynamics → Fill: 0=koyu gri, 1=açık gri; alarm tag'i=kırmızı
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**iX Developer ekran tasarımı güçlü yönleri:**
- Fiziksel Beijer X2/X3 panel projelerinde — doğal seçim, doğrudan donanım entegrasyonu
- Sürükle-bırak hızlı geliştirme: Prototipten üretime kısa sürede
- Alias ile faceplate/makine şablonları: Aynı ekranı onlarca instance için yeniden kullan
- Yerleşik alarm, trend, recipe, audit trail — ek araç gerektirmez
- Tek satıcı (vendor) ekosistemine kilitli olmak sorun değilse

**iX Developer tercih edilmemeli:**
- Web tabanlı, tarayıcı erişimli HMI gerekiyorsa (iX Developer web server sınırlıdır)
- Platform bağımsızlığı kritikse (React/Vue tabanlı web HMI daha uygun)
- Git ile versiyon kontrolü birincil gereksinim ise (iX Developer dosyaları binary tabanlı)
- Büyük, çok kullanıcılı SCADA uygulamaları (Ignition veya WinCC daha uygun ölçek)

## Gerçek Proje Notları

**Not 1 — Background Ekran Değişikliğinin Yayılması**
Bir projede tüm 45 ekrana aynı navigasyon barı eklenmişti — her biri ayrı kopyalanmış. "Geri" butonunun konumu değişince 45 ekranda tek tek düzeltme yapıldı. Sonraki projede Background Screen kullanıldı; navigasyon barındaki herhangi bir değişiklik tek noktadan tüm ekranlara yayıldı. Bu pratiği hayata geçirmenin maliyeti yaklaşık 30 dakika, kazandırdığı süre 3+ saat.

**Not 2 — Alias Kısıtının Görünmeyen Maliyeti**
15 aynı tip pompa için Alias'lı tek ekran tasarlandı. Her şey güzeldi — ta ki arka plan ekran istenene kadar. Alias ekranlar background alamıyor. Çözüm: her pompa için ayrı ekran kopyalamak. Baştan bilinse, ortak öğeler Component Library'den inject edilirdi; background screen yerine.

**Not 3 — Data Logger Olmadan Uzun Süreli Trend**
Bir operatör "son 4 saatin hız trendini görmek istiyorum" dedi. Trend Viewer Log Item yerine direkt Tag'e bağlıydı — yalnızca RAM önbelleği tutuyordu (birkaç dakika). Data Logger yoktu. Sonraki gün Data Logger kuruldu, 30 günlük saklama ayarlandı. Tarihsel trend görmek için 30 gün beklendi. Ders: Trend Viewer + Data Logger kurulumu proje başında yapılmalıdır.

**Not 4 — Index Register ile Makine Seçici**
Bir paketten oluşan 20 aynı makine vardı. Her makine için ayrı ekran yerine:
- "Machine_Detail" ekranı: Index Register kullanıyor
- Bir buton grubunda makine 1-20 seçimi
- Seçilen numar Index Register'a yazılıyor
- Tüm Analog Numeric ve göstergeler Index Register üzerinden ilgili adresi okuyor
Sonuç: 20 ekran yerine 1 ekran, bakım 20 kat daha kolay. Bu yaklaşım Alias'tan farklıdır: array olmayan tag adresleme için uygundur.

**Not 5 — Performans İçin Tag Sıralama**
Controller'da M0.0 ile M11.7 arasındaki bit'ler art arda kullanılıyordu. iX Developer tek telegram ile tümünü okuyabildi. Farklı adreslere dağılmış bit'ler kullanıldığında her biri için ayrı okuma paketi oluştu; iletişim %300 arttı. Tag'leri ardışık adreslerde tanımlamak büyük performans farkı yaratır.

**Not 6 — Multi Picture Nesnesi ve Görsel Bellek Tüketimi**
Bir projede her makine durumu için yüksek çözünürlüklü PNG'ler kullanan 30+ Multi Picture nesnesi vardı. Ekran açılışı belirgin gecikti çünkü her görsel ekran yüklenirken belleğe alınıyordu. Çözüm: durum göstergeleri için vektör tabanlı basit şekiller + renk dinamiği kullanıldı; sadece gerçekten gerekli yerlerde raster görsel bırakıldı. Gömülü panelde görsel bellek sınırlıdır; büyük PNG/JPEG'ler hem yükleme hem RAM açısından pahalıdır. Görselleri hedef boyutta önceden ölçeklemek (runtime'da değil) gerekir.

**Not 7 — Modal Popup'ın Arka Plan Pollingi Durdurmadığı Yanılgısı**
Modal bir popup açıldığında operatör etkileşimi arka ekranda engellenir; ancak arka ekrandaki nesnelerin tag polling'i durmaz — değerler arka planda güncellenmeye devam eder. Bir ekipte "popup açıkken iletişim yükü düşer" varsayımıyla çok sayıda tag'i ana ekranda bırakıp popup'larla maskeleme yapıldı; iletişim yükü hiç düşmedi. Polling yükünü gerçekten azaltmak için tag'ler ayrı ekranlara taşınmalı, modal popup ile gizlenmemelidir.

**Not 8 — Çözünürlük Değişiminde Font ve Konum Kayması**
PC hedefli bir proje 1280×800'den 1920×1080'e taşındığında iX otomatik yeniden boyutlandırma yaptı ama font boyutları orantısız büyüdü ve bazı sabit-konumlu Analog Numeric nesneleri komşu nesnelerle çakıştı. Otomatik ölçekleme bir başlangıç noktasıdır, son değil: çözünürlük değişiminden sonra her ekran görsel olarak gözden geçirilmeli, özellikle metin taşması ve hizalama kontrol edilmelidir. Mümkünse hedef çözünürlük baştan kesinleştirilmelidir.

## Edge Case'ler ve Sistem Limitleri

Ekran tasarımı katmanında limitler çoğunlukla render performansı ve nesne davranışıyla ilgilidir; aşağıdaki tablo pratik eşikleri özetler.

| Alan | Pratik Limit / Eşik | Aşıldığında / Sınır Davranışı |
|---|---|---|
| Ekran başına nesne | ~400 (öneri) | Ekran geçiş gecikmesi, render donması |
| Alarm Viewer satır | ~200 (öneri) | Yükleme yavaşlığı, ekran geçişi takılması |
| Toplam alarm öğesi | ~500 (pratik) | Alarm motoru değerlendirme gecikmesi |
| Aktif Data Logger | ~25 (öneri) | İletişim + disk I/O baskısı |
| Trend Viewer eğri | Mümkün olduğunca az | Kısa örneklemeli çok eğri → iletişim doygunluğu |
| PC çözünürlük seçenekleri | 1920×1080 / 1280×800 / 800×600 / 640×480 | Diğer değerler doğrudan seçilemez |

**Alias edge case'leri:** Alias kullanan ekran background/foreground olamaz, array tag/expression/TrendViewer ile birlikte çalışmaz. Bu kısıtlar tasarım zamanında engellenir ama Component Library'den inject edilen öğelerde fark edilmeyebilir — alias'lı bir ekrana TrendViewer eklemek sessiz başarısızlık yerine bağlanmamış bir eğriyle sonuçlanır.

**Dynamics ve Script aynı özellikte:** Bir özelliğe hem Dynamics hem script uygulanırsa script kazanır, Dynamics sessizce devre dışı kalır — hata mesajı yoktur. Bu, "Dynamics neden çalışmıyor" hatasının en yaygın gizli nedenidir. Özellik başına tek mekanizma kuralı zorunludur.

**Index Register sınırı:** Index Register ile aynı nesne farklı istasyon/adres gösterebilir, ancak index değeri her değiştiğinde ilgili tüm nesneler yeni adresi yeniden okur — index hızlı değişirse (ör. her saniye makine değiştirme) iletişimde ani yük dalgaları oluşur. Index değişimi operatör tetiklemeli olmalı, otomatik döngü değil.

**Görünmez nesne hâlâ poll eder:** Visible dinamiği ile gizlenmiş bir nesne ekrandadır ve bağlı tag'i poll edilmeye devam eder. Performans için "gizlemek" yeterli değildir; yük azaltmak için nesne tamamen ayrı bir ekrana/popup'a taşınmalıdır.

**Expression tek satır sınırı:** Tag expression'ları tek satırlık C# ifadeleridir; çok adımlı mantık (if/else blokları, döngü) içermez. Karmaşık dönüşüm gerekiyorsa script modülüne veya bir ara internal tag'e geçilmelidir.

## Optimizasyon

**1. Background ekran ile statik yükü ayırma**
Tüm ekranlarda tekrar eden statik öğeleri (logo, çerçeve, navigasyon barı) background ekrana taşımak, ön plan ekranların nesne sayısını ve dolayısıyla render süresini düşürür. Ayrıca tek noktadan bakım sağlar — bir projede 45 ekrana kopyalanmış navigasyon barı yerine tek background ekran 3+ saat tasarruf sağladı (bkz. Not 1).

**2. Alias ile şablon ekran çoğaltma**
Aynı tip ekipmanın N adedi için ayrı ayrı ekran çizmek yerine tek bir Alias'lı şablon ekran kullanmak, hem geliştirme hem bakım maliyetini N kat azaltır. Tek bir değişiklik tüm instance'lara yansır. Sınırı: alias background olamaz; ortak öğeler Component Library ile inject edilmelidir.

**3. Index Register ile makine seçici deseni**
Onlarca benzer makine için Alias'a alternatif olarak Index Register kullanmak (operatör makine no seçer → tek ekran ilgili adresleri okur) ekran sayısını 1'e indirir. Array olmayan ardışık adresli veride çok etkilidir (bkz. Not 4).

**4. Ekranların tag yükünü poll grubuyla hizalama**
Bir ekranda gösterilen tag'lerin poll grubu seçimi ekran tepkiselliğini doğrudan etkiler. Detay ekranındaki kritik göstergeler hızlı gruba, arka plandaki özet sayaçlar yavaş gruba atanmalı (poll grubu detayı: 01 belgesi Optimizasyon).

**5. Trend/Data Logger yükünü ekran bazında sınırlama**
Her ekrana çok eğrili trend koymak yerine, tarihsel analizi ayrı bir "Trend" ekranında toplamak ve detay ekranlarında yalnızca son birkaç dakikalık gerçek zamanlı küçük trend göstermek iletişim bütçesini korur.

**6. Görsel varlık optimizasyonu**
Raster görseller (PNG/JPEG) hedef boyutunda önceden ölçeklenmeli; runtime ölçeklemesi hem CPU hem bellek tüketir. Durum göstergeleri için raster yerine renk dinamikli vektör şekiller tercih edilmeli (bkz. Not 6).

## Derin Teknik Detay

**Nesne modeli neden dependency property tabanlı?**
iX2'nin WPF temeli, her nesne özelliğini (Fill, Visible, Left, Top) bir dependency property olarak modeller. Bu, bir tag değerinin doğrudan bir görsel özelliğe bağlanmasını (binding) çerçeve düzeyinde mümkün kılar: tag değiştiğinde WPF'in property değişim bildirim mekanizması nesneyi otomatik yeniden çizer. Dynamics sekmesi aslında bu binding altyapısının görsel bir editörüdür. Bu yüzden bir özellik aynı anda hem binding (Dynamics) hem imperatif script ataması alamaz — WPF'te bir dependency property'nin tek bir "değer kaynağı önceliği" vardır ve imperatif atama (script) binding'i geçersiz kılar. "Dynamics neden çalışmadı" hatasının altında yatan mekanizma budur.

**Background/foreground ekran kompozisyonu — neden Alias dışlanır?**
Background ekran, ön plan ekranla aynı görsel ağaca (visual tree) birleştirilerek render edilir. Alias ise ekrana parametre geçmek için ekran açılışında bir tag-çözümleme bağlamı (context) kurar. Bir ekran hem background olarak başka bir ekrana gömülecek hem de kendi alias bağlamını koruyacaksa, hangi alias bağlamının geçerli olduğu belirsizleşir — aynı background ekranı farklı alias'larla birden çok ön plan ekran kullanabilir. iX bu belirsizliği tasarım kuralıyla (alias ekran background olamaz) baştan engeller. Bu, çalışma zamanı belirsizliği yerine tasarım zamanı kısıtı tercih eden bir mühendislik kararıdır.

**Trend Viewer'ın iki veri yolu — RAM cache vs Data Logger**
Trend Viewer doğrudan bir tag'e bağlandığında, değerleri sınırlı bir RAM ring buffer'dan okur (yalnızca birkaç dakikalık geçmiş). Data Logger'a (Log Item) bağlandığında ise veriyi proje veritabanından (SQLite tabanlı) çeker. Bu ikilik, gömülü panelde belleğin pahalı, diskin yavaş olmasından kaynaklanır: her tag'i sürekli diske loglamak I/O baskısı yaratır, bu yüzden gerçek zamanlı izleme RAM'den, tarihsel analiz diskten yapılır. "Son 4 saati gör" isteğinin Data Logger olmadan çalışmamasının nedeni budur (bkz. Not 3) — RAM buffer o derinliği tutmaz.

**Telegram birleştirme — sürücü neden ardışık adresi sever?**
Endüstriyel sürücüler PLC'den veri okurken her tag için ayrı istek yerine adres aralığını tek bir blok okuma telegramında toplar (block read / optimized read). Ardışık adresli (ör. M0–M11) taglar tek telegrama sığar; dağınık adresler her biri ayrı telegram gerektirir. Bunun nedeni protokol seviyesinde her telegram için sabit bir overhead (header, round-trip gecikmesi) olmasıdır — 10 tag'i tek telegramda okumak, 10 ayrı telegramdan kat kat ucuzdur. Bu yüzden PLC tarafında HMI değişkenlerini ardışık bir bellek bloğunda toplamak (bkz. Not 5) protokol seviyesinde optimizasyondur, sadece kozmetik düzen değil.

## İlgili Konular

```
knowledge/hmi/ix-developer/
├── 01_architecture.md       → iX Developer proje mimarisi, versiyon farkları
├── 02_codesys_connection.md → Controller bağlantısı, tag oluşturma
└── 04_scripting.md          → C# scripting, onay dialog'ları, özel dinamikler

knowledge/hmi/architecture/
└── 01_hmi_patterns.md       → ISA-101 standartları, HMI tasarım kalıpları (temel kaynak)

Resmi belgeler:
  iX Developer 2.51 Reference Manual
    → https://www.beijerelectronics.com/docs/iX-251-Reference/en/index-en.html
  iX Developer 3.0 User Guide (MAEN433A)
    → https://www.beijerelectronics.com/docs/iX/PDF/iX_Developer_3_0_MAEN433A.pdf
  iX Developer 3.2 User Guide (MAEN433C)
    → https://www.beijerelectronics.com/docs/iX/PDF/iX_Developer_3_2_MAEN433C.pdf
  iX Developer 2 Tutorial Videoları
    → https://www.beijerelectronics.com/en/Products/software/ix-hmi-software/Vimeo___video___page
```
