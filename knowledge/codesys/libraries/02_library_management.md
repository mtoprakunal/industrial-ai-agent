---
KONU        : Library Manager — Kütüphane Yönetimi, Sürümleme, Placeholder
KATEGORİ    : codesys
ALT_KATEGORI: libraries
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_obj_library_manager.html"
    başlık: "CODESYS Online Help — Object: Library Manager"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/LibDevSummary/placeholder.html"
    başlık: "CODESYS Online Help — Placeholder (Library Development Summary)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_update_library_placeholders.html"
    başlık: "CODESYS Online Help — Updating Library Placeholders"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_cmd_placeholder.html"
    başlık: "CODESYS Online Help — Command: Placeholders"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_standard_libraries.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/programming/04_libraries.md"
    ilişki: detaylandırır
  - konu: "_synthesis.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "Kütüphane kavramı ve FB'yi kütüphaneye dönüştürme (programming/04_libraries.md)"
  - "Standart kütüphaneler (01_standard_libraries.md)"
ÇELİŞKİLER :
  - kaynak: "Asterisk (*) referans vs placeholder referans"
    konu: "Hangisi tercih edilmeli?"
    çözüm: >
      Asterisk referansı 'her zaman kurulu en yeni sürüm'ü çözer ve yanlışlıkla
      yapılan kurulumlarla istemeden değişebilir. Placeholder referansı yalnızca
      bilinçli sürüm değişimiyle güncellenir. Üretim/dağıtım projelerinde
      placeholder veya sabit sürüm tercih edilmelidir.
  - kaynak: "Compiler profiles vs placeholder çözümleme"
    konu: "Library profiles SP17 itibarıyla deprecated"
    çözüm: >
      [DOĞRULANMADI — sürüm geçişi] CODESYS SP17 ve sonrasında derleyici-bağımlı
      library profile çözümlemesi kullanımdan kaldırılmıştır; placeholder
      çözümlemesi cihaz açıklaması ve library support package üzerinden yürür.
      Hedef sürümün dokümanını esas alın.
---

## Özün Ne

CODESYS projeleri yalıtık değildir: Standard, Util, IoStandard gibi sistem kütüphanelerine ve çoğu zaman şirkete özel kütüphanelere bağımlıdır. **Library Manager** bu bağımlılıkların tek yönetim noktasıdır; hangi kütüphanenin hangi sürümünün kullanıldığını, nasıl referanslandığını (sabit sürüm, asterisk, placeholder) ve hangi namespace ile erişildiğini buradan görür ve düzenlersiniz. Bu konunun bilinmesi şart, çünkü sürüm yönetimi sahada en çok zaman kaybettiren sessiz sorunlardan birinin kaynağıdır: bir bilgisayarda derlenen proje, başka bir bilgisayarda farklı kütüphane sürümü yüzünden derlenmez ya da farklı davranır. **Placeholder** mekanizması bu kaosu engellemek için tasarlanmıştır — bağımlılık hiyerarşisinin alt katmanını, üst katmanları bozmadan güncellemeyi mümkün kılar. Uzman, projeyi başka makinede/yıllar sonra aynı şekilde derlenecek biçimde kurmayı (tekrarlanabilir build) bu mekanizmalarla sağlar.

## Nasıl Çalışır

### Library Manager Nedir

Her uygulamanın (Application) altında bir **Library Manager** nesnesi vardır. Burada:
- Referanslanan tüm kütüphaneler, sürümleri ve **Effective version** (çözümlenmiş, gerçekte kullanılan sürüm) listelenir.
- Sistem kütüphaneleri üretici bilgisiyle (parantez içinde, ör. "System") gösterilir.
- Bir kütüphane başka kütüphanelere bağımlıysa, referanslanan (dependent) kütüphaneler otomatik dahil edilir; bunlar salt-okunurdur (yalnızca bağımsız/non-dependent kütüphanelerin özellikleri düzenlenebilir).
- İkonlar durum gösterir: imzalı (güvenilir/güvenilmeyen sertifika), kurcalanmış (tampered), lisanssız, eksik/opsiyonel, çözümlenememiş.

### Namespace — İsim Çakışmasını Önleme

Her kütüphanenin içeriğine `<namespace>.<POU_adı>` ile erişilir. Namespace genellikle kütüphane adıyla aynıdır ama yerel olarak özelleştirilebilir. "qualified-access-only" özellikli kütüphaneler **namespace zorunluluğu** dayatır: `Util.LIN_TRAFO` yazmadan `LIN_TRAFO` çağıramazsınız. İki kütüphane aynı isimde FB içerirse namespace ayrımı çakışmayı çözer.

### Üç Referans Tipi

| Referans tipi | Davranış | Risk/Kullanım |
|---|---|---|
| **Sabit sürüm** (fixed) | Tam olarak belirtilen sürüm referanslanır | En öngörülebilir; manuel güncelleme gerekir |
| **Asterisk (*)** | "Kurulu en yeni sürüm" otomatik çözülür | Yanlışlıkla kurulan yeni sürümle **istemeden değişir** |
| **Placeholder** | Çözümlenebilir, isimli referans; yalnızca bilinçli değişir | Bağımlılık hiyerarşisi yönetimi için tasarlandı |

### Placeholder — Neden Var

Resmî gerekçe: Placeholder, "belirli bir kütüphane sürümüne yapılan bir referanstır" ve kütüphane hiyerarşisinin bakımını basitleştirir. Asterisk referansının aksine, placeholder **yalnızca belirli CODESYS bileşenlerinin yeni sürümlerine bilinçli geçişle** değişir — kazara kurulan yeni sürümle değişmez. Tutarlı placeholder kullanımı, bağımlılık hiyerarşisinin **alt katmanını** (güncelleme, hata düzeltmesi) **üst katmanları uyarlamak zorunda kalmadan** değiştirmeyi sağlar.

**Çözümleme sırası (resolution order):**
1. Uygulamaya bağlı (application-related) bağlanmamış placeholder'lar
2. Cihaz açıklamaları (device descriptions — runtime sürümüne bağlı)
3. Library support package'lar (paket sürümüne bağlı)
4. Library profile'lar (derleyici sürümüne bağlı — SP17 itibarıyla deprecated)

Uygulama bağlamı her zaman placeholder çözümlemesini geçersiz kılar (override eder).

**Kritik kısıt:** Placeholder **adı sonradan değiştirilemez**. Bu yüzden başkasının aynı adı seçme olasılığı düşük, ayırt edici bir ad seçmek şiddetle önerilir.

### Library Repository — Kurulum Kaynağı

**Library Repository** diyaloğu kütüphanelerin kurulması/kaldırılması ve konumlarının yapılandırılmasını sağlar. "Download Missing Libraries", eksik kütüphaneleri tanımlı sunuculardan tarayıp indirir. Bir projeyi açan makinede ilgili kütüphane kurulu değilse, çözümlenememiş (unresolved) görünür ve derleme başarısız olur.

### Kütüphane Oluşturma ve Dağıtma

Kendi kütüphanenizi geliştirmek (programming/04 detaylandırır) için:
1. Bir **library project** oluşturup POU'ları (FB, Function, INTERFACE) ekleyin.
2. **Project Information** (başlık, sürüm, şirket, namespace) doldurun — bunlar Library Manager'da görünür.
3. **Save Project as Compiled Library (.compiled-library)** ile derlenmiş/kapalı kaynak; **.library** ile kaynaklı dağıtım.
4. İmzalama (signing) ile güven/bütünlük sağlanır.
5. Repository'ye kurulunca diğer projeler "Add Library" ile referanslar.

> Dağıttığınız kütüphaneye bir **placeholder adı** ve namespace verin; tüketici projeler sürümü kazara değiştirmeden referanslasın.

## Pratikte Nasıl Kullanılır

### Kütüphane Ekleme

```
Library Manager (aç) → Add Library...
   → repository'den kütüphane seç (bağımlılıkları otomatik gelir)
   → Effective version sütununda çözümlenen sürümü doğrula
```

### Placeholder Çözümlemesini Düzenleme

```
Library Manager → Placeholders (komut/diyalog)
   → her placeholder için çözümlenecek sürümü seç (mevcut/yeni)
   → sonuç Effective version'da görünür
```

### Tekrarlanabilir Build İçin Kontrol Listesi

```
□ Üretim projelerinde asterisk (*) yerine placeholder/sabit sürüm kullan
□ Şirket kütüphanelerine ayırt edici placeholder adı ver (sonradan değişmez!)
□ qualified-access (namespace zorunlu) ile isim çakışmasını engelle
□ Projeyle birlikte kullanılan kütüphane sürümlerini belgele/version kontrolüne koy
□ Başka makinede aç → unresolved kütüphane var mı kontrol et (Download Missing)
□ Devreye alma öncesi Effective version'ları gözden geçir
```

## Örnekler

### Örnek 1: Namespace ile Çakışma Çözme

```iecst
(* İki kütüphane de 'Scale' adlı FB içeriyor *)
VAR
    fbScaleA : LibVendorA.Scale;     (* namespace ile ayrım *)
    fbScaleB : LibVendorB.Scale;
END_VAR
```

### Örnek 2: Sürüm Çatışması Belirtisi

```
Library Manager görünümü (sorunlu):
  MyCompany_Drives   Version: *        Effective: 1.4.0.0   ← asterisk!
  └── MyCompany_Base  Version: 1.2.0.0  Effective: 1.3.0.0   ← beklenmedik

Sorun: asterisk yüzünden başka makinede kurulu en yeni sürüm çözüldü;
       proje farklı derlendi.
Çözüm: asterisk → placeholder veya sabit sürüm; Effective version sabitlendi.
```

### Örnek 3: Şirket Kütüphanesi Dağıtım Künyesi

```
Project Information (library project):
  Title       : MyCompany Motor Library
  Version     : 2.1.0.0
  Company     : MyCompany
  Namespace   : MC_Motor          ← qualified access ile çakışma yok
  Placeholder : MC_Motor          ← ayırt edici, değişmez ad
→ Save as Compiled Library → repository'ye kur → tüketici 'Add Library'
```

## Sık Yapılan Hatalar

### Hata 1: Üretimde Asterisk (*) Referans Bırakmak

Asterisk "kurulu en yeni"yi çözer; başka makinede/zamanda farklı sürüm çıkar, proje farklı derlenir veya derlenmez. Üretimde placeholder/sabit sürüm kullanın.

### Hata 2: Placeholder Adını Sonradan Değiştirmeye Çalışmak

Placeholder adı değiştirilemez. Genel/çakışan bir ad (ör. "Base", "Lib1") seçerseniz ileride başka kütüphaneyle çatışır ve düzeltmek zordur. Baştan ayırt edici ad verin.

### Hata 3: Kütüphane Sürümlerini Version Kontrolüne Koymamak

Proje dosyası Git'te ama hangi kütüphane sürümleriyle derlendiği kayıtlı değilse, başka makinede "unresolved/farklı sürüm" sorunu çıkar. Bağımlılık sürümlerini belgeleyin/sabitleyin.

### Hata 4: qualified-access Kütüphaneyi Namespace'siz Çağırmak

`LIN_TRAFO` (çıplak) yerine `Util.LIN_TRAFO` gerektiğini bilmeyince derleme hatası alınır. qualified-access-only kütüphanelerde namespace zorunludur.

### Hata 5: Kütüphaneyi Güncelleyip Kırıcı Değişikliği Görmemek

Alt katman kütüphanesini güncellemek (placeholder'la bile), bir FB imzası değiştiyse üst kodu kırabilir. Sürüm yükseltmesinden sonra **tam yeniden derleme + test** yapın; placeholder bakımı kolaylaştırır ama uyumluluğu garanti etmez.

### Hata 6: Compiled Library ile Kaynak Beklemek

`.compiled-library` kaynak içermez (kapalı); içine bakmak/düzenlemek isteyen tüketici hayal kırıklığına uğrar. Kaynak paylaşımı gerekiyorsa `.library` dağıtın.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Placeholder Kullanın

- Şirkete özel kütüphane dağıtıyorsanız (tüketici sürümü kazara değiştirmesin).
- Çok katmanlı kütüphane bağımlılığı varsa (alt katmanı üst katmanı bozmadan güncellemek için).
- Tekrarlanabilir build ve uzun ömürlü bakım kritikse.

### Sabit Sürüm Kullanın

- Validasyon/sertifikasyon gerektiren projelerde (tam sürüm dondurulmalı).
- Davranışın bit-bit aynı kalması zorunluysa.

### Asterisk (*) — Dikkatli Kullanın / Kaçının

- Yalnızca hızlı prototip/deneme; üretimde kaçının.
- "Her zaman en yeni" istemiyorsanız asla.

### Namespace (qualified access) Zorunlu Kılın

- Birden çok kütüphane kullanan büyük projelerde isim çakışmasını baştan engellemek için.

## Gerçek Proje Notları

**Not 1 — "Benim Makinemde Derleniyordu" Klasiği**
Bir proje geliştiricinin makinesinde sorunsuzdu; devreye alma dizüstünde derlenmedi. Sebep: şirket kütüphanesi asterisk (*) ile referanslıydı, iki makinede farklı sürüm kuruluydu. Placeholder + sabit sürüme geçilip kütüphane sürümleri belgelenince sorun bitti. Ders: asterisk referans, "bende çalışıyordu" hatasının bir numaralı sessiz kaynağıdır.

**Not 2 — Değiştirilemeyen Placeholder Adı**
İlk şirket kütüphanesine placeholder adı "Base" verildi. İki yıl sonra başka bir tedarikçi kütüphanesi de "Base" placeholder kullanınca çakışma çıktı; placeholder adı değiştirilemediği için kütüphaneyi yeni adla yeniden yayınlamak ve tüm tüketici projeleri güncellemek gerekti. Ders: placeholder adını şirket öneki + amaçla ayırt edici seçin (`MC_MotorBase`), asla genel kelime kullanmayın.

**Not 3 — Sürüm Yükseltmesi Sonrası Kırılan FB İmzası**
Alt katman kütüphanesi "küçük bir bugfix" için yükseltildi; bir FB'nin VAR_INPUT'una yeni alan eklenmişti. Üst kodda o FB'yi pozisyonel çağıran yerler kırıldı, fark online change sonrası sahada çıktı. Ders: kütüphane sürüm yükseltmesi placeholder'la kolay görünür ama arayüz uyumluluğunu garanti etmez; yükseltme sonrası tam derleme + regresyon testi şart.

**Not 4 — qualified-access'in Kurtardığı Büyük Proje**
20+ kütüphaneli bir entegrasyon projesinde iki kütüphane aynı isimde yardımcı FB içeriyordu. qualified-access-only baştan zorunlu kılındığı için her çağrı namespace'liydi; çakışma hiç yaşanmadı. Namespace zorunlu olmayan başka bir projede aynı durum saatlerce "yanlış FB çağrılıyor" hatasına yol açmıştı. Ders: büyük projelerde namespace zorunluluğunu baştan açın.

**Not 5 — Compiled vs Source Dağıtım Kararı**
Bir kütüphane müşteriye `.compiled-library` olarak verildi (IP koruması). Müşteri bir davranışı uyarlamak isteyince kaynağa erişemedi; her değişiklik için bize döndü. Sonraki müşteride iş modeline göre `.library` (kaynaklı) tercih edildi. Ders: dağıtım formatı teknik değil iş kararıdır — IP koruması mı, müşteri özgürlüğü mü; baştan netleştirin.

## İlgili Konular

```
knowledge/codesys/libraries/
├── _synthesis.md               → Kütüphane stratejisi sentezi (kullan/yaz/sürümle)
└── 01_standard_libraries.md    → Yönetilen kütüphaneler: Standard, Util, IoStandard

knowledge/codesys/programming/
└── 04_libraries.md             → Kendi kütüphaneni oluşturma (FB → library) detayı

knowledge/codesys/fundamentals/
└── 02_project_structure.md     → Library Manager'ın proje içindeki yeri
```
