---
KONU        : İleri CODESYS Sentezi — OOP Ne Zaman, Durum Makinesi Nasıl Tasarlanır
KATEGORİ    : codesys
ALT_KATEGORI: advanced
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "knowledge/codesys/advanced/01_oop_codesys.md"
    başlık: "CODESYS V3 OOP (İleri)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/advanced/02_state_machines_sfc.md"
    başlık: "Durum Makineleri — SFC vs CASE (İleri)"
    güvenilirlik: deneyimsel
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_extending_function_block.html"
    başlık: "CODESYS Online Help — Extending a Function Block"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_oop_codesys.md"
    ilişki: detaylandırır
  - konu: "02_state_machines_sfc.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/programming/_synthesis.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "Bu klasördeki iki belge (01_oop, 02_state_machines) okunmuş olmalı."
  - "programming/_synthesis.md (kapsülleme + tek yönlü akış) kavranmış olmalı."
  - "Saha devreye alma ve bakım deneyimi varsayılır."
ÇELİŞKİLER :
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez yeni çelişki içermez; kaynak belgelere atıf yapar."
---

## Özün Ne

İleri CODESYS'in iki konusu — OOP ve durum makineleri — ayrı görünür ama tek bir uzman içgüdüsünün iki yüzüdür: **soyutlamayı problemin gerçek şekline oturtmak.** Yeni başlayan, eline aldığı her aracı her yere uygular: her şeyi OOP yapar ya da her sekansı SFC'ye sokar. Uzman tersini yapar — önce problemin doğasını okur, sonra en az soyutlamayla en açık çözümü seçer. Bu klasörün özü üç ilkede toplanır:

1. **Açıklık (explicitness) her şeyin üstündedir** — Durum açık (enum/step), geçiş açık (saf koşul), tanımsız durum açık (ELSE → güvenli). Hem CASE hem SFC bu disipline tabidir; OOP polimorfizmi bile "hangi davranış çalışacak" sorusunu örtük bırakmamalıdır.
2. **Soyutlama, tekrara karşı kazanılır — tekrar yoksa soyutlama borçtur** — OOP/arayüz yalnızca "aynı sözleşmenin iki+ farklı uygulaması" varsa değer üretir; tek uygulamaya kalıtım ağacı kurmak net kayıptır.
3. **PLC fiziği soyutlamanın altında durur** — Metot stack'tedir (kalıcı değil), timer her scan çağrılmalıdır, REAL eşitliği yoktur, online change pointer/instance düzenini bozabilir. Hiçbir OOP/SFC zarafeti bu gerçekleri askıya almaz.

Uzmanlık, bir tasarım kararını ("OOP mu klasik FB mi", "SFC mi CASE mi") bu üç ilkeye haritalayıp gereksiz soyutlamayı reddedebilmektir.

## Nasıl Çalışır

### İki Belgenin Zihin Haritası

```
01 OOP ───────────── "Farklı şeyleri tek sözleşmeyle yönet" (yapı/varyasyon ekseni)
   │  INTERFACE = sözleşme, EXTENDS = ortak+varyasyon, METHOD/PROPERTY = kapsülleme
   │
   │  Her cihazın İÇİNDEKİ davranış genellikle bir durum makinesidir
   ▼
02 DURUM MAKİNELERİ ─ "Zamanda adım adım ilerle" (davranış/zaman ekseni)
      SFC = görsel/paralel/online,  CASE = test/Git/koşullu/yeniden-kullanım
```

OOP **"ne" (yapı, tipler arası ilişki)** eksenidir; durum makinesi **"nasıl/ne zaman" (davranışın zaman içindeki akışı)** eksenidir. Gerçek bir cihaz FB'si ikisini birden taşır: bir arayüz uygular (OOP ekseni) ve içinde bir CASE state machine çalıştırır (davranış ekseni).

### Karar Ağacı — Hangi Aracı Ne Zaman

```
Aynı sözleşmenin 2+ farklı uygulaması var mı?
├── Hayır → klasik FB (OOP yok). Davranış sekans mı?
│            ├── 5+ adım / paralel / görsel-kritik → SFC (+ ST action)
│            └── az adım / test / Git / koşullu     → ST CASE
│
└── Evet  → OOP: INTERFACE + IMPLEMENTS (polimorfizm)
             Ortak gövde + küçük varyasyon mu? → + EXTENDS / SUPER^
             Her uygulamanın İÇ davranışı yine → CASE veya SFC (yukarıdaki dal)
```

### Üç İlkenin Saha Belirtilerine Haritası

| Saha belirtisi | İhlal edilen ilke | Düzeltme |
|---|---|---|
| Makine tanımsız durumda donuyor | Açıklık (ELSE yok) | Her CASE'e `ELSE → güvenli durum` |
| Override beklenen yerde çalışmıyor | Açıklık (gövde+override karışık) | Mantığı metoda taşı, gövde `THIS^.X()` |
| 5 seviye kalıtım, kimse okuyamıyor | Gereksiz soyutlama | Kalıtımı ≤2 seviyeye indir / arayüze çevir |
| Timer hiç bitmiyor | PLC fiziği (koşullu çağrı) | Durumlu blok her scan koşulsuz çağrılı |
| SFC adımında sonsuza takılı | PLC fiziği (REAL eşitlik) / deadlock | Eşik karşılaştırma + paralel dal timeout |
| Online change sonrası garip davranış | PLC fiziği (pointer/instance) | Kritik devreye alımda download |
| Tek motora interface ağacı | Gereksiz soyutlama | Klasik `FB_Motor` + CASE |

## Pratikte Nasıl Kullanılır

### Tasarım Akışı (Uzman Sırası)

1. **Problemi say:** Kaç farklı cihaz tipi? Kaç adım? Paralellik var mı? Kim bakacak?
2. **En az soyutlamayı seç:** Tek tip + az adım → FB + CASE. Birden çok tip → arayüz ekle. Çok adım/paralel/görsel → SFC katmanı ekle.
3. **Açıklığı zorla:** enum durumlar, ELSE dalı, saf transition, koşulsuz timer.
4. **PLC fiziğini doğrula:** metotta durumlu blok yok mu, REAL eşitlik yok mu, online change planı ne?
5. **Test/izlenebilirlik kararı:** Git+test kritik → CASE; saha görünürlük kritik → SFC; ikisi de → karışık katman.

### Tipik Karma Mimari

```
PRG_LineSequence        → SFC      (üst faz: Hazırlık→Üretim→Temizlik)
  └── her step action   → ST
FB_Drive (IMPLEMENTS I_Drive)      → OOP sözleşme
  ├── FB_Servo EXTENDS FB_Drive    → varyasyon
  └── FB_VFD   EXTENDS FB_Drive
       └── her FB içinde            → CASE state machine (cihaz yaşam döngüsü)
PROPERTY rSetpoint                 → doğrulamalı HMI erişimi
```

## Örnekler

### Örnek: Bir Belirtiyi İlkeye İndirgemek

```
Belirti : "Yeni tartım hücresi tedarikçisi eklediğimizde üst katmanı
           her seferinde değiştiriyoruz, 3 yerde kırılıyor."
İlke    : Soyutlama tekrara karşı kazanılır — burada GERÇEK tekrar/varyasyon var.
Çözüm   : I_WeighCell arayüzü; üst katman yalnızca arayüz referansı tutar;
           yeni tedarikçi = yeni FB, üst katman değişmez. (01_oop Not 1)
Karşıt  : Eğer tek tedarikçi olsaydı arayüz BORÇ olurdu — klasik FB yeterdi.
```

### Örnek: Hangi Durum Makinesi

```
Süreç A : 7 adımlı CIP, 2 paralel kol, operatör hangi adımı görmek istiyor.
        → SFC (+ ST action, her kola timeout). Görünürlük + paralellik kazanır.

Süreç B : 3 durumlu vana FB, kütüphaneye girecek, simülasyonda test edilecek.
        → ST CASE. Test + yeniden kullanım + az adım CASE'i seçtirir.
```

## Sık Yapılan Hatalar

- **Araç-merkezli düşünmek:** "OOP öğrendim, her şey OOP olsun" / "SFC güzel, her sekans SFC". Problem-merkezli düşünün; araç sonra gelir.
- **Açıklığı zarafete feda etmek:** Kısa, "akıllı" ama durum/geçişi örtük bırakan kod. Açık ve uzun, örtük ve kısaya yeğdir.
- **PLC fiziğini soyutlamanın arkasında unutmak:** Metot/sınıf zarafeti, "timer her scan çağrılmalı" gerçeğini değiştirmez.
- **Soyutlama derinliğini ölçmemek:** Kalıtım >2 seviye, SFC iç içe paralel dal — okunabilirlik çöker.

## Ne Zaman Tercih Edilmeli / Edilmemeli

Bu bir sentez belgesidir; teknoloji seçimi değil **karar disiplini** sunar:

- **OOP'a "evet" deyin** yalnızca çoğul-uygulama/genişletilebilirlik gerçek bir ihtiyaçsa.
- **SFC'ye "evet" deyin** görsel izlenebilirlik, paralellik veya 5+ adım değer üretiyorsa.
- **CASE'i varsayılan yapın** — test, Git, yeniden kullanım ve basitlik çoğu işi kapsar.
- **Hiçbirine "her zaman" demeyin** — her proje problemini yeniden okuyun.

## Gerçek Proje Notları

**Not 1 — En Pahalı Hatalar Soyutlama Hatalarıydı, Sözdizimi Değil**
Yıllar içinde en çok zaman kaybettiren sorunlar yanlış `IF` değil; yanlış soyutlama seçimleriydi: tek tipe kurulan kalıtım ağacı, basit işe sokulan SFC, gövde+override melezi. Sözdizimi hatası derleyicide yakalanır; soyutlama hatası sahada, aylar sonra ortaya çıkar.

**Not 2 — "CASE ile Başla, Gerekirse Yükselt" Kuralının Değeri**
Ekip kuralı haline gelen pratik: her yeni sekans önce ST CASE yazılır. Gerçekten görsellik/paralellik gerekirse SFC iskeletine sarmalanır. Tersini hiç yapmadık (SFC'den temiz CASE çıkarmak zordu). Düşük soyutlamadan yükseğe çıkmak, yüksekten inmekten kolaydır.

**Not 3 — Arayüz, Kalıtımdan Daha Sık Doğru Cevaptır**
OOP'un saha değerinin büyük kısmı `EXTENDS`'ten değil `INTERFACE`'ten geldi. Polimorfik sözleşme (çok tipli sürücü/vana/sensör) tekrar tekrar kazandırdı; derin kalıtım çoğu zaman sadeleştirilince daha iyi oldu. Kararsızsanız kalıtım yerine arayüz + kompozisyon deneyin.

**Not 4 — Açıklık Disiplini Hem CASE Hem SFC'de Aynı**
ELSE dalı (CASE) ile adım timeout/`SFCError` (SFC) aynı felsefenin iki yüzü: "tanımsız/takılı durumda güvenli tarafa kaç". Bu disiplini uygulayan iki yaklaşım da güvenliydi; uygulamayan ikisi de sahada makineyi belirsiz duruma soktu. Araç değil, disiplin güvenliği belirledi.

## İlgili Konular

```
knowledge/codesys/advanced/
├── 01_oop_codesys.md           → OOP detayları (interface/method/extends/property)
└── 02_state_machines_sfc.md    → SFC vs CASE detayları, action qualifier

knowledge/codesys/programming/
├── _synthesis.md               → Kapsülleme + tek yönlü akış (bu sentezin temeli)
├── 03_function_blocks.md       → FB gövde/metot, ELSE felsefesi
└── 01_pou_types.md             → Instance modeli, METHOD neden sadece FB'de

knowledge/codesys/fundamentals/
├── 03_iec61131_languages.md    → Dil seçimi (SFC/ST), OOP neden ST'de
└── _synthesis.md               → Determinizm felsefesi (üst sentez)
```
