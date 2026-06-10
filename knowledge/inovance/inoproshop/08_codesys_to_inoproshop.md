---
KONU        : CODESYS Projesini InoProShop'a Taşıma (Migrasyon)
KATEGORİ    : inovance
ALT_KATEGORI: inoproshop
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_project_transfer.html"
    başlık: "CODESYS Online Help — Transferring Projects (sabit kütüphane/derleyici sürümü, proje arşivi)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_opening_project_v23.html"
    başlık: "CODESYS Online Help — Opening a V2.3 Project (V2→V3 dönüşümü manuel)"
    güvenilirlik: resmi
  - url: "https://techdocs.wago.com/Software/eCOCKPIT/en-US/313344395.html"
    başlık: "WAGO e!COCKPIT — Importing CODESYS V2 and V3 Projects (bilinmeyen cihaz → uyumlu cihaz önerisi)"
    güvenilirlik: topluluk
  - url: "https://www.deif.com/blog/plc-codesys/be-independent-of-plc-vendors-with-codesys/"
    başlık: "DEIF — Be independent of PLC vendors with CODESYS (cihaz değiştirme mantığı)"
    güvenilirlik: topluluk
  - url: "https://idea-tech.in/wp-content/uploads/2020/04/INOVANCE-AM400AM600AC800-PLC-SOFTWARE-MANUAL-ENGLISH-20-4-20.pdf"
    başlık: "Inovance — AM400/AM600/AC800 PLC Software (InoProShop) User Guide"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_inoproshop_overview.md"
    ilişki: gerektirir
  - konu: "02_project_structure.md"
    ilişki: kullanır
  - konu: "09_debugging.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/fundamentals/02_project_structure.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "InoProShop = CODESYS V3 türevi olduğu kavranmış olmalı (01_inoproshop_overview.md)"
  - "CODESYS V3 Device tree, Library Manager, Application kavramları (knowledge/codesys/fundamentals/02_project_structure.md)"
  - "Hedef donanım AM400/AM600/AC800 olmalı (H5U/H3U/Easy DEĞİL — onlar AutoShop)"
ÇELİŞKİLER :
  - kaynak: "Kullanıcı beklentisi: 'CODESYS projem InoProShop'ta tek tıkla otomatik açılır'"
    konu: "Tam otomatik dönüşüm beklentisi gerçekçi değildir"
    çözüm: >
      IEC 61131-3 mantığı (POU/ST/GVL) yüksek oranda taşınır; ancak cihaz tanımı,
      vendor kütüphaneleri, EtherCAT slave eşlemesi ve motion FB'leri manuel yeniden
      kurulum gerektirir. "Otomatik" olan kod-içi mantıktır, donanım katmanı değil.
  - kaynak: "Sürüm uyumu (kaynak CODESYS sürümü vs InoProShop CODESYS çekirdek sürümü)"
    konu: "InoProShop'un dayandığı CODESYS çekirdek sürümü, kaynak projenin sürümünden eski/yeni olabilir"
    çözüm: >
      Sürümler arası proje açma CODESYS'te desteklenir fakat derleyici/kütüphane
      sürüm uyuşmazlığı uyarı/hata üretebilir. Kesin sürüm eşlemesi InoProShop
      kurulum sürümünden TEYİT EDİLMELİDİR (bu belgede tahmin edilmedi).
---

## Özün Ne

InoProShop bir CODESYS V3 türevi olduğundan, mevcut bir CODESYS V3 projesinin mantığı
(POU'lar, ST kodu, GVL'ler, standart IEC kütüphane çağrıları) InoProShop'a büyük
ölçüde **doğrudan** taşınır. Ancak bir CODESYS projesi yalnızca mantıktan ibaret
değildir: cihaz tanımı, EtherCAT slave eşlemesi, vendor'a özel kütüphaneler ve motion
fonksiyon blokları da projenin parçasıdır. Bu donanım/vendor katmanı **otomatik
taşınmaz**; hedef Inovance cihazına yeniden kurulması gerekir.

Bu yüzden migrasyonu iki katmana ayırmak doğrudur: **(1) taşınabilir mantık katmanı**
(neredeyse sorunsuz) ve **(2) yeniden inşa edilen donanım/vendor katmanı** (manuel
emek). "Tek tıkla dönüşüm" beklentisi, ikinci katmanı göz ardı ettiği için yanlış olur.

> NOT: Bu belge CODESYS'in resmi proje-transfer/V2-açma davranışına ve genel
> vendor-cihaz-değiştirme mantığına dayanır. InoProShop'a **özgü** menü adımları ve
> sürüm eşlemeleri, InoProShop kurulu sürümünden teyit edilmelidir; aşağıda
> doğrulanmamış adımlar `[DOĞRULANMADI]` ile işaretlenmiştir.

## Nasıl Çalışır

### İki Katman Modeli

```
CODESYS V3 Projesi                    InoProShop (CODESYS V3 türevi)
─────────────────────                 ──────────────────────────────
KATMAN 1 — MANTIK (taşınabilir)
  POU (PRG/FB/FUN), ST/LD/SFC/FBD  ──► neredeyse birebir taşınır
  GVL, DUT (struct/enum), tipler   ──► birebir taşınır
  Standart IEC kütüphane çağrıları ──► aynı (Standard, Util, ...)
  Task konfigürasyonu (mantık)     ──► taşınır, atama gözden geçirilir

KATMAN 2 — DONANIM/VENDOR (yeniden inşa)
  Device tree kök cihaz            ──► Inovance AM400/AM600/AC800 ile DEĞİŞİR
  EtherCAT master + slave'ler      ──► Inovance ESI ile yeniden eklenir/eşlenir
  Vendor kütüphaneleri             ──► Inovance muadilleriyle değiştirilir
  Motion FB'leri (eksen referansı) ──► Inovance eksen/ESI'ye yeniden bağlanır
  I/O eşlemesi (%I/%Q)             ──► yeni cihaz adres haritasına göre yeniden
```

### Neden Mantık Taşınır, Donanım Taşınmaz?

IEC 61131-3 kod gövdesi vendor-bağımsızdır: bir ST POU'sundaki `IF`, `CASE`, aritmetik
ve standart FB çağrıları platformdan bağımsızdır. Buna karşılık cihaz tanımı projeye
**device description** (ve EtherCAT için **ESI**) dosyalarıyla bağlanır; bu dosyalar
vendor'a özeldir. CODESYS'te bir projeyi farklı bir cihaza taşımak demek, kök cihazı
yeni device description'a güncellemek demektir — ve resmi davranışa göre **hedef cihaz
mevcut tüm application'ları desteklemiyorsa application'lar düşürülebilir / uyarı
verilir** (kaynak: WAGO/CODESYS import davranışı). Inovance cihaz havuzu InoProShop'a
önceden gömülüdür, dolayısıyla Inovance cihazını seçmek kolaydır; zor olan I/O ve slave
eşlemesinin yeni adres haritasına yeniden oturtulmasıdır.

### Sürüm Uyumu

CODESYS, proje arşivinin yalnızca **sabit (fix) sürümlü kütüphaneler** ve sabit
derleyici/görselleştirme sürümüyle güvenilir biçimde taşındığını belirtir. Migrasyon
öncesi kaynak projede kütüphane sürümlerini sabitlemek, hedefte "library not found /
version mismatch" hatalarını azaltır (bkz. knowledge/codesys/debugging/01_common_errors.md).

## Pratikte Nasıl Kullanılır

Aşağıdaki akış, **CODESYS V3 → InoProShop** taşımanın gerçekçi adımlarıdır. Genel
CODESYS davranışı doğrulanmıştır; InoProShop'a özgü menü etiketleri `[DOĞRULANMADI]`.

1. **Kaynak projeyi hazırla (CODESYS tarafı).**
   - Tüm kütüphaneleri **sabit sürüme** çek (Library Manager → her kütüphane → fix version).
   - Derleyici sürümünü ve görselleştirme profilini sabitle (Project Settings).
   - Hangi kütüphanelerin **standart IEC** (taşınır) hangilerinin **vendor'a özel**
     (değişecek) olduğunu listele. Bu liste migrasyonun yol haritasıdır.
   - Temiz derleme al, sıfır hata/uyarı ile başla.

2. **Mantığı dışa aktar (en güvenli yol: PLCopen XML / export).**
   - POU/GVL/DUT'ları PLCopen XML veya CODESYS export (`.export`) olarak dışa aktarmak,
     vendor-bağımsız mantığı temiz biçimde taşımanın en risksiz yoludur.
   - Alternatif: tüm projeyi InoProShop'ta açıp kök cihazı güncellemek `[DOĞRULANMADI]`
     — InoProShop sürümünün, kaynak proje formatını açıp açamadığı teyit edilmelidir.

3. **InoProShop'ta hedef projeyi kur.**
   - Yeni proje → hedef cihazı seç: **AM400 / AM600 / AC800**.
   - Dışa aktarılan POU/GVL/DUT'ları içe aktar (import).

4. **Vendor/donanım katmanını yeniden inşa et.**
   - Device tree'de EtherCAT master ekle, Inovance servo/I/O slave'lerini **ESI** ile ekle.
   - Standart-olmayan kütüphaneleri Inovance muadilleriyle değiştir (motion için
     Inovance'ın PLCopen MC_* kütüphanesi).
   - Motion FB'lerindeki eksen referanslarını (AXIS_REF) yeni Inovance eksenlerine bağla.
   - I/O eşlemesini (%I/%Q) yeni cihazın adres haritasına göre yeniden yap; eski AT
     adreslerine güvenme.

5. **Task atamasını rules.json'a göre gözden geçir.**
   - Motion ≤2 ms, hızlı interlock ≤4 ms, PID ≤10 ms, HMI/iletişim ≤500 ms
     (bkz. agent/rules.json). EtherCAT bus task önceliği ≤5.
   - Bloke I/O (Modbus/dosya/socket) yalnız Freewheeling task'ta kalmalı.

6. **Derle → indir → online doğrula.**
   - Watchdog açık olduğunu doğrula (asla migrasyon kolaylığı için kapatma).
   - Online izleme + Trace ile mantığı, EtherCAT diag ile bus'ı doğrula (bkz. 09).
   - Create Boot Application + power-cycle testi yap.

## Örnekler

**Senaryo: Jenerik CODESYS V3 AM600-benzeri motion projesini InoProShop'a taşıma**

```
Taşınan (Katman 1):
  PRG_Main (ST)            → import, değişmeden çalışır
  FB_AxisJog, FB_Recipe    → import, değişmeden çalışır
  GVL_Process, DUT_Recipe  → import, değişmeden çalışır
  Standard.library çağrıları (TON, R_TRIG, ...) → aynı

Yeniden inşa edilen (Katman 2):
  Kök cihaz: jenerik CODESYS Control → AM600
  EtherCAT slave: 3× SV660N servo  → Inovance ESI ile yeniden eklendi
  Motion lib: jenerik SM3_* / vendor MC → Inovance MC_* muadili
  AXIS_REF bağları: eski eksen → yeni Inovance ekseni (manuel)
  I/O: %QX0.0.. → yeni GL20 modül adres haritası (manuel)
```

**Tipik hata mesajları ve kökü:**

| Mesaj | Katman | Kök neden | Çözüm |
|---|---|---|---|
| "Library not found" | Vendor lib | jenerik/eski sürüm lib | Inovance muadili + sabit sürüm |
| "Device unknown / replace?" | Cihaz | kök cihaz Inovance değil | AM4xx/6xx/AC800 ile değiştir |
| "%QX address conflict" | I/O eşleme | eski AT adresleri taşındı | yeni adres haritasına yeniden eşle |
| Eksen FB'si HATA verir | Motion | AXIS_REF kopuk | ekseni yeniden bağla, ESI doğrula |
| "version mismatch" | Sürüm | derleyici/lib sürümü | sabit sürüm + InoProShop sürümünü teyit et |

## Sık Yapılan Hatalar

- **Tam otomatik dönüşüm beklemek.** Mantık taşınır; donanım/vendor katmanı manueldir.
  Proje süresini buna göre planla.
- **Yanlış hedef ortam.** Proje aslında küçük PLC içinse (H5U/H3U/Easy), hedef InoProShop
  DEĞİL AutoShop'tur. Önce donanımı doğrula (bkz. 01_inoproshop_overview.md).
- **Eski AT/%adreslerine güvenmek.** Yeni cihazın bellek/adres haritası farklıdır; I/O
  eşlemesini yeniden yapmadan indirmek sessiz yanlış-bağlantı üretir.
- **Kütüphane sürümlerini sabitlememek.** Dalgalı (float) sürümler hedefte "not found /
  mismatch" üretir; migrasyon öncesi fix version şart.
- **Watchdog'u kapatıp "önce çalışsın" demek.** rules.json'a aykırı; watchdog daima açık.
- **Motion FB'lerini taşıyıp eksen referansını unutmak.** Kod görünüşte taşınır ama
  AXIS_REF kopuk olduğundan çalışmaz; her ekseni yeni cihaza yeniden bağla.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tam proje arşivini açıp cihaz güncellemeyi dene:** Kaynak ve InoProShop CODESYS
  çekirdek sürümleri yakınsa ve donanım büyük ölçüde Inovance'a çevrilecekse — hızlı
  başlangıç. Ancak sürüm farkı belirsizse riskli `[DOĞRULANMADI]`.
- **Sadece mantığı export/import et (PLCopen XML):** Sürümler uzaksa, donanım baştan
  kurulacaksa veya kaynak proje çok-vendor karışıksa — en temiz, en öngörülebilir yol.
  Önerilen varsayılan budur.
- **Sıfırdan yaz:** Kaynak proje küçük/dağınıksa, taşıma emeği yeniden yazımdan fazlaysa.

## Gerçek Proje Notları

- Migrasyonda zamanın çoğu koda değil, **EtherCAT slave eşlemesi ve I/O yeniden
  haritalamasına** gider. Kaynak projede iyi belgelenmiş bir io_list.csv varsa bu süre
  belirgin düşer — taşımadan önce io_list'i çıkar.
- "Mantık çalışıyor ama eksen oynamıyor" en sık görülen migrasyon sonrası belirtidir;
  neredeyse her zaman kopuk AXIS_REF veya eksik ESI/motion lisansından kaynaklanır,
  kod hatasından değil.
- Sürüm eşlemesi en büyük belirsizliktir: InoProShop'un dayandığı CODESYS çekirdek
  sürümü resmi olarak her zaman ilan edilmez. Migrasyondan önce küçük bir pilot POU ile
  açma/derleme testi yapmak, tüm projeyi taşımadan önce sürüm riskini ölçer.
- Bu belge "Orta" olgunlukta: genel CODESYS davranışı güçlü kaynaklı, InoProShop'a özgü
  adımlar teyide muhtaç. `[DOĞRULANMADI]` etiketli adımları sahada doğrulayın.

## İlgili Konular

- `01_inoproshop_overview.md` — InoProShop = CODESYS V3 türevi (taban)
- `02_project_structure.md` — InoProShop proje/Device tree yapısı
- `09_debugging.md` — taşıma sonrası online doğrulama, EtherCAT diag
- `knowledge/codesys/fundamentals/02_project_structure.md` — CODESYS Device tree/Library Manager
- `knowledge/codesys/debugging/01_common_errors.md` — library/version/address hataları
