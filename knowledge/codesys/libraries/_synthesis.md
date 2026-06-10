---
KONU        : Kütüphane Stratejisi Sentezi — Kullan, Yaz, Sürümle
KATEGORİ    : codesys
ALT_KATEGORI: libraries
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "knowledge/codesys/libraries/01_standard_libraries.md"
    başlık: "CODESYS Standart Kütüphaneleri (İleri)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/libraries/02_library_management.md"
    başlık: "Library Manager — Sürümleme, Placeholder (İleri)"
    güvenilirlik: deneyimsel
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_obj_library_manager.html"
    başlık: "CODESYS Online Help — Object: Library Manager"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_standard_libraries.md"
    ilişki: detaylandırır
  - konu: "02_library_management.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/programming/04_libraries.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "Bu klasördeki iki belge (01_standard, 02_management) okunmuş olmalı."
  - "FB tasarımı ve kütüphane oluşturma (programming/03, programming/04)."
ÇELİŞKİLER :
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez yeni çelişki içermez; kaynak belgelere atıf yapar."
---

## Özün Ne

Kütüphane konusunun iki belgesi — hazır kütüphaneler (ne sunarlar) ve yönetim (nasıl sürümlenir) — tek bir uzman karar zincirinin iki halkasıdır: **"Kodu kim yazsın ve hangi sürüm sabit kalsın?"** Bu zincir üç soruyla yürür:

1. **Kullan mı, yaz mı?** — İhtiyacın olan zaten Standard/Util'de varsa, yeniden yazmak taşınabilirlik kazandırmaz; test edilmemiş risk ekler. Yoksa kendi FB/kütüphaneni yaz.
2. **Sarmala mı, doğrudan mı?** — Hazır blok işini görüyor ama arayüzü/projenin diline uymuyorsa, ince bir wrapper ile kendi sözleşmeni dayat; içeride hazır bloğu çağır.
3. **Nasıl sürümle?** — Hangi kararı verirsen ver, başka makinede/yıllar sonra **aynı şekilde derlenmeli**. Placeholder + namespace + belgelenmiş sürüm bunu garanti eder.

Uzmanlık, bu üç soruyu refleks haline getirmektir: önce kütüphaneye bak (yazma), gerekirse sarmala (arayüzü koru), her zaman sürümü sabitle (tekrarlanabilir build). Kütüphane sorunlarının çoğu teknik değil disiplin sorunudur — yanlış yerde yeniden yazılan blok, sabitlenmemiş sürüm, çakışan placeholder adı.

## Nasıl Çalışır

### İki Belgenin Zihin Haritası

```
01 STANDART KÜTÜPHANELER ── "Ne var, ne sunuyor?" (içerik ekseni)
   │  Standard: TON/TOF/CTU/R_TRIG/SR/RS   Util: LIN_TRAFO/CHARCURVE/PID/BLINK
   │  IoStandard: G/Ç yapı taşları
   │
   │  Neyi kullanacağına karar verdin → şimdi hangi sürüm, nasıl referans?
   ▼
02 YÖNETİM ─────────────── "Nasıl referans, hangi sürüm?" (kararlılık ekseni)
      Library Manager, namespace, sabit/asterisk/placeholder, repository, dağıtım
```

Birinci belge **içerik** (problemi çözen blok hangisi), ikinci belge **kararlılık** (o blok her ortamda aynı mı kalır) eksenidir. Çalışan bir kod için ikisi de gerekir: doğru bloğu seçmek + o bloğu sabit sürümle kilitlemek.

### Karar Akışı — Kullan / Sarmala / Yaz / Sürümle

```
İhtiyaç: bir işlev gerekiyor (timer, ölçekleme, PID, edge, ...)
│
├── Standard/Util'de var mı?
│    ├── Evet → arayüzü projeye uyuyor mu?
│    │          ├── Evet → DOĞRUDAN kullan (kendin yazma)
│    │          └── Hayır → WRAPPER FB ile sar (kendi arayüzün, içeride hazır blok)
│    └── Hayır → KENDİN yaz (FB) → tekrar kullanılacaksa KÜTÜPHANE yap
│
└── Her durumda: SÜRÜMLE
     placeholder adı (ayırt edici, değişmez) + namespace (qualified) + belgele
```

### Kütüphane Belirtilerinin İlkeye Haritası

| Belirti | İhlal | Düzeltme |
|---|---|---|
| Kendi yazdığın TON'da kayma | "Yaz" yerine "kullan" olmalıydı | Standard.TON'a dön |
| "Bende derleniyordu, sahada hayır" | Sürüm sabitlenmemiş | asterisk → placeholder/sabit |
| Placeholder adı çakıştı | Genel ad seçildi | Şirket öneki + amaç (değişmez!) |
| "Yanlış FB çağrılıyor" | Namespace zorunsuz | qualified-access aç |
| Hazır blok arayüzü her yere sızdı | Doğrudan kullanım, sarmalanmalıydı | Wrapper FB |
| PID absürt davranıyor | Cycle time uyumsuz | CYCLE = task periyodu |

## Pratikte Nasıl Kullanılır

### Uzman Refleks Sırası (Her Yeni İhtiyaçta)

1. **Önce kütüphaneye bak** — Standard/Util zaten sunuyor mu? (timer, sayaç, edge, scale, PID, blink, hysteresis...)
2. **Arayüz uyumunu kontrol et** — hazır blok projenin adlandırma/sözleşme diline uyuyor mu?
3. **Gerekirse sarmala** — uymuyorsa wrapper FB; uyuyorsa doğrudan çağır.
4. **Sürümü kilitle** — placeholder/sabit, namespace, sürüm belgesi.
5. **Tekrar kullanılacaksa kütüphaneleştir** — kendi FB'ni library project'e taşı, künye + placeholder ver.

### Üretim İçin Sürüm Disiplini

```
□ Üretimde asterisk yok → placeholder veya sabit sürüm
□ Şirket kütüphanesine ayırt edici, değişmez placeholder adı
□ Büyük projede qualified-access zorunlu (namespace)
□ Kütüphane sürümleri version kontrolünde / belgede
□ Sürüm yükseltmesi sonrası tam derleme + regresyon testi
□ Dağıtım formatı bilinçli seçildi (.library kaynak / .compiled-library kapalı)
```

## Örnekler

### Örnek: Kullan / Sarmala / Yaz Kararı

```
İhtiyaç A : 5sn açma gecikmesi.
  → Standard.TON var, arayüz basit → DOĞRUDAN kullan. (yazma)

İhtiyaç B : Ham ADC → °C ölçekleme, projenin her yerinde tek tip arayüz isteniyor.
  → Util.LIN_TRAFO var ama IN/IN_MIN/... arayüzü proje diline uymuyor.
  → FB_AnalogScale wrapper: kendi temiz arayüzün, içeride LIN_TRAFO çağrısı.

İhtiyaç C : Özel kaskad kontrol algoritması, Util.PID yetmiyor.
  → Kütüphanede yok → KENDİN yaz (FB) → 5+ projede kullanılacak → KÜTÜPHANE yap,
     placeholder + namespace ver.
```

### Örnek: Sürüm Belirtisini İlkeye İndirgemek

```
Belirti : "Devreye alma dizüstünde proje derlenmedi."
İlke    : Tekrarlanabilir build — sürüm sabitlenmeli.
Kök     : Şirket kütüphanesi asterisk (*) referanslı, makinelerde farklı sürüm.
Çözüm   : placeholder/sabit sürüm + sürümleri belgele. (02 Not 1)
```

## Sık Yapılan Hatalar

- **Önce yazmak, sonra "zaten varmış" demek:** Refleks ters; önce kütüphaneye bak. IEC standart bloğunu yeniden yazmak taşınabilirlik değil risk getirir (01 Not 1).
- **Sürümü sabitlememek:** "Bende çalışıyordu"nun bir numaralı sebebi (02 Not 1). Üretimde asterisk yasak.
- **Hazır bloğu sarmalamadan her yere sızdırmak:** Util'in arayüzü kod tabanına dağılırsa, ileride bloğu değiştirmek her çağrı noktasını kırar. Wrapper ile sözleşmeni koru.
- **Sürüm yükseltmesini "bedava" sanmak:** Placeholder bakımı kolaylaştırır ama arayüz uyumunu garanti etmez; yükseltme sonrası test şart (02 Not 3).
- **Namespace'i ihmal etmek:** Büyük projede çakışma kaçınılmaz; qualified-access baştan açılmalı (02 Not 4).

## Ne Zaman Tercih Edilmeli / Edilmemeli

Bu sentez teknoloji değil **strateji** sunar:

- **"Kullan" varsayılan olsun** — hazır blok varsa ve uyuyorsa, yazma.
- **"Sarmala" arayüz uyumsuzluğunda** — hazır işlevi koru, kendi sözleşmeni dayat.
- **"Yaz" yalnızca gerçekten yoksa** — ve tekrar kullanılacaksa kütüphaneleştir.
- **"Sürümle" her zaman** — istisna yok; her karar tekrarlanabilir build'e tabidir.

## Gerçek Proje Notları

**Not 1 — En Çok Zaman Kaybı Sürüm Disiplininden Geldi, Eksik Bloktan Değil**
Yıllar içinde "kütüphanede bu blok yok" sorunu nadiren takıldı; gerçek kayıplar sürüm yönetiminden çıktı: asterisk yüzünden farklı derlenen projeler, çakışan placeholder adları, belgelenmemiş bağımlılıklar. Kütüphane stratejisinin %80'i içerik değil kararlılık disiplinidir.

**Not 2 — Wrapper'ın Uzun Vadeli Kazancı**
Util.PID doğrudan 30 yerde çağrılan bir projede, daha iyi bir kontrol bloğuna geçiş gerektiğinde 30 çağrı noktası elle değişti. Sonraki projede tüm PID çağrıları `FB_Loop` wrapper'ı arkasındaydı; blok değişimi tek dosyada oldu. Ders: hazır bloğu sarmalamak başta fazladan iş gibi görünür, değişim geldiğinde katbekat geri öder.

**Not 3 — "Kullan" Refleksinin Eğitimle Yerleşmesi**
Yeni mühendisler ilk içgüdüyle her şeyi yazıyordu (kendi edge detector, kendi scale). Ekip kuralı oldu: "yeni FB yazmadan önce Standard ve Util'i tara". Kod tekrarı ve hata oranı belirgin düştü. Ders: "önce kütüphaneye bak" öğrenilen bir alışkanlıktır, doğuştan gelmez.

## İlgili Konular

```
knowledge/codesys/libraries/
├── 01_standard_libraries.md    → Standard/Util/IoStandard içeriği (ne sunar)
└── 02_library_management.md    → Sürümleme, placeholder, namespace, dağıtım

knowledge/codesys/programming/
├── 03_function_blocks.md       → İyi FB (wrapper/kendi blok temeli)
└── 04_libraries.md             → Kendi kütüphaneni oluşturma detayı

knowledge/codesys/advanced/
└── _synthesis.md               → Soyutlama disiplini (wrapper = arayüz soyutlaması)
```
