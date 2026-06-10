---
KONU        : GitHub'daki Açık Kaynak IEC 61131-3 / Structured Text Projeleri
KATEGORİ    : examples
ALT_KATEGORI: open-source
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://github.com/myutzy/awesome-structured-text"
    başlık: "awesome-structured-text — IEC 61131-3 ST kaynak listesi (topluluk küratörlü)"
    güvenilirlik: topluluk
  - url: "https://github.com/tcunit/TcUnit"
    başlık: "TcUnit — TwinCAT 3 birim test çatısı (MIT lisans, resmi proje deposu)"
    güvenilirlik: resmi
  - url: "https://tcunit.org/"
    başlık: "TcUnit resmi sitesi — CI/CD (TcUnit-Runner, Jenkins) entegrasyonu"
    güvenilirlik: resmi
  - url: "https://github.com/PLC-lang/rusty"
    başlık: "RuSTy — Rust/LLVM tabanlı ST derleyicisi (resmi depo, Dockerfile + cargo test)"
    güvenilirlik: resmi
  - url: "https://github.com/nucleron/matiec"
    başlık: "matiec — IEC 61131-3 → C açık kaynak derleyici"
    güvenilirlik: topluluk
  - url: "https://github.com/topics/iec-61131-3"
    başlık: "GitHub Topics: iec-61131-3 — proje keşfi"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/codesys/programming/04_libraries.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/programming/03_function_blocks.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/project-generation/03_plcopen_xml.md"
    ilişki: kullanır
  - konu: "02_codesys_forge_store.md"
    ilişki: alternatif
ÖNKOŞUL     :
  - "IEC 61131-3 dilleri ve ST temeli (knowledge/codesys/fundamentals/03_iec61131_languages.md)"
  - "FB tasarımı ve test edilebilirlik (knowledge/codesys/programming/03_function_blocks.md)"
  - "Git/sürüm kontrolü ve temel CI/CD kavramı"
ÇELİŞKİLER :
  - kaynak: "Beklenti: 'PLC kodu sürüm kontrolü/CI'ya uygun değildir'"
    konu: "IEC 61131-3 kodu metin-tabanlı (ST) ve PLCopen XML export ile Git + CI'ya uygundur"
    çözüm: >
      Doğrulanmış olgu: ST metin dosyası olarak Git'te diff/merge edilebilir;
      PLCopen XML ile proje export'lanıp versiyonlanabilir; TcUnit/CfUnit gibi
      çatılar Jenkins/Azure DevOps ile otomatik test çalıştırır. Yani modern
      yazılım mühendisliği (VCS, test, CI) PLC dünyasında uygulanabilir; mit
      sertifika/emniyet kısıtları ayrı bir konudur.
---

## Özün Ne

GitHub, endüstriyel otomasyon için yazılım-mühendisliği disiplininin (sürüm kontrolü, birim
test, CI/CD, kod analizi) PLC dünyasına taşındığı yerdir. Burada üç tür değerli içerik bulunur:
**(1) küratörlü listeler** (awesome-structured-text gibi — nereye bakılacağını gösterir),
**(2) araç/altyapı projeleri** (derleyiciler, test çatıları, linter'lar, OpenPLC gibi runtime'lar),
ve **(3) örnek kütüphane/uygulamalar** (TcOpen, OSCAT port'ları).

Neden önemli: Bir agent için buradaki asıl ders **kod organizasyonu, test ve CI**dir — yani
"hangi FB var" değil, "olgun bir PLC kod tabanı nasıl yapılandırılır, nasıl test edilir, değişiklik
nasıl güvenle yapılır" sorusunun cevabı. Bu, telifli kod kopyalamadan transfer edilebilen en
kalıcı bilgidir.

## Nasıl Çalışır

GitHub ekosistemini kategorilere ayırarak okumak en verimlisidir (awesome-structured-text bu
ayrımı yapar):

- **Geliştirme platformları:** CODESYS, TwinCAT, Beremiz, Siemens TIA Portal gibi IDE'ler
  (çoğu kapalı, ama Beremiz açık kaynaktır).
- **Runtime / Soft-PLC:** **OpenPLC** — tamamen ücretsiz, standart bir IEC 61131-3 soft-PLC;
  LD, IL, ST, FBD, SFC dillerinde programlama sağlar. Eğitim ve düşük maliyetli otomasyon için
  yaygın.
- **Derleyici / parser:** **matiec** (IEC 61131-3 → C), **RuSTy** (Rust + LLVM tabanlı modern ST
  derleyicisi), Tree-sitter ST grameri (editör/araç entegrasyonu için).
- **Statik analiz / linter:** **iec-checker** ve daha yeni "ST için deterministik semantik
  linter" projeleri (diff-tabanlı kontroller, FB-instance kuralları, PLCopen ve MISRA-C /
  IEC 61508-62443 eşlemeleri içerenler). Kod kalitesini ve emniyet kılavuzlarına uyumu otomatik
  denetler.
- **Test çatıları:** **TcUnit** (TwinCAT 3, xUnit tipi, MIT lisans), **CfUnit / co♻e** (vanilla
  CODESYS için TcUnit forku, MIT), platform-bağımsız **UniTest**. Tümü IEC 61131-3 veri tiplerini
  (ANY dahil) doğrulayan assert metotları sunar.
- **DevOps / paket yönetimi:** GitHub Actions iş akışları ve TwinCAT için paket yöneticileri;
  PLC kodunu CI hattına bağlamayı sağlar.
- **Kütüphane/framework:** OSCAT (port'lar), **TcOpen** (TwinCAT için uygulama çatısı) gibi.

Çalışma prensibi yazılım dünyasıyla aynıdır: ST metin dosyaları Git'te tutulur, PLCopen XML ile
proje export edilip versiyonlanır (bkz. 03_plcopen_xml.md), her commit'te CI test çatısını
çalıştırır.

## Pratikte Nasıl Kullanılır

1. **Keşif için listeden başla:** awesome-structured-text deposunu tara — kategorilere göre
   projeleri görüp ihtiyacına uyanı seç. GitHub Topics (`iec-61131-3`, `structured-text`) ile
   güncel/aktif projeleri filtrele (son güncelleme tarihine bak).
2. **Test çatısı kur:** TwinCAT kullanıyorsan TcUnit, CODESYS kullanıyorsan CfUnit/co♻e
   kütüphanesini projene ekle. FB'lerin için test POU'ları yaz (assert metotlarıyla).
3. **CI'ya bağla:** TcUnit-Runner ile testleri Jenkins / Azure DevOps gibi bir hatta koş; her
   sürüm kontrolü değişikliğinde testler otomatik çalışıp istatistik toplar.
4. **Linter ekle:** ST kodunu iec-checker / semantik linter ile commit öncesi denetle; stil ve
   emniyet kuralı ihlallerini erken yakala.
5. **Lisans ve aktiflik kontrolü:** Kullanmadan önce projenin lisansını (MIT, GPL, OSCAT-tipi,
   ticari) ve bakım durumunu (son commit, açık issue/PR) değerlendir.

## Örnekler

- **TcUnit ile regresyon koruması:** Bir `FB_Motor` için test POU'su; start/stop/fault geçişlerini
  assert eder. Kod değiştikçe CI testi kırılırsa regresyon anında görülür — sahada değil ofiste.
- **RuSTy ile platform-bağımsız derleme:** ST kodunu LLVM üzerinden derleyip CI içinde
  (Dockerfile + `cargo build`/`cargo test`) doğrulamak; vendor IDE'sine bağımlı olmadan derleme
  kontrolü.
- **OpenPLC ile düşük maliyetli/eğitim PLC:** Raspberry Pi gibi donanımda IEC 61131-3 programı
  koşturmak; gerçek lisanslı PLC olmadan kavram doğrulama (PoC).
- **awesome-structured-text ile araç seçimi:** Bir ekibin "ST için VSCode eklentisi, formatter
  (STweep), linter ve test çatısı" yığınını bu listeden seçip standartlaştırması.

(Bu projelerin kaynak kodu burada birebir aktarılmamıştır; yalnızca ne işe yaradıkları ve hangi
yazılım-mühendisliği dersini verdikleri özetlenmiştir.)

## Sık Yapılan Hatalar

- **Bakımsız/terk edilmiş projeye bağımlı olmak.** GitHub'da çok sayıda proje vardır ama bir
  kısmı yıllardır güncellenmez. Son commit tarihine, açık PR/issue sayısına ve lisansa bakmadan
  ürüne katmak risklidir.
- **Lisans uyumunu atlamak.** TcUnit/CfUnit MIT (esnek) iken bir başka proje GPL olabilir;
  GPL bir kütüphaneyi kapalı ticari ürüne katmak lisans ihlali doğurabilir. Lisans her zaman
  okunmalı.
- **"PLC kodu CI'ya gelmez" varsayımı.** ST metin-tabanlıdır; Git diff/merge, PLCopen XML export
  ve TcUnit-Runner ile CI tamamen mümkündür. Bu varsayım modern pratikten gerilik yaratır.
- **Test çatısını kurup test yazmamak.** Çatıyı eklemek değer üretmez; asıl iş FB davranışını
  assert eden testleri yazmak ve CI'da koşturmaktır.
- **Derleyici/runtime'ı sertifikalı sanmak.** OpenPLC, matiec, RuSTy araştırma/eğitim/genel amaçlı
  araçlardır; emniyet (SIL) veya sertifikalı üretim için tasarlanmamışlardır.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih:** Kod kalitesini ve sürdürülebilirliği artırmak isteyen her ciddi PLC ekibi için
  test çatısı (TcUnit/CfUnit) + linter + CI yığını neredeyse zorunlu kazançtır. Eğitim, PoC,
  vendor-bağımsız derleme doğrulaması için OpenPLC/RuSTy/matiec uygundur. Araç seçiminde
  awesome-structured-text iyi bir başlangıç haritasıdır.
- **Etmemeli:** Sertifikalı emniyet işlevi, garanti/SLA gerektiren kritik altyapı veya üretici
  destek zorunluluğu olan projelerde topluluk araçlarına bel bağlamak. Bu durumlarda vendor'ın
  sertifikalı IDE/runtime/SL ürünleri esastır; topluluk araçları yardımcı (yan) katman olarak
  kalmalıdır.

## Gerçek Proje Notları

- **En kalıcı ders araç değil, disiplindir.** TcUnit'in xUnit deseni, ekibe "her FB test
  edilebilir bir birimdir" düşüncesini kazandırır — bu, function_blocks.md'deki "FB tek
  sorumluluk + kapsülleme + output-only" kurallarının doğal sonucudur. Test edilebilir FB
  yazmak ile test çatısı kurmak aynı madalyonun iki yüzüdür.
- **CI'nın gerçek getirisi sahada görülür:** regresyon testleri ofiste kırıldığında, aynı hata
  makinede beklenmedik harekete dönüşmez. Bir kez kurulan CI hattı, "online change sonrası bir
  şey bozuldu mu?" endişesini ölçülebilir bir güvene dönüştürür.
- **PLCopen XML + Git kombinasyonu** kod incelemesini (code review) mümkün kılar: ST POU'ları
  metin diff'i olarak okunur; ikili `.project` dosyasının aksine değişiklik anlaşılır. Ekiplerin
  en büyük kazancı budur (bkz. 03_plcopen_xml.md).
- **Lisans hijyeni** uzun vadede en sık görmezden gelinen risktir. Bir ekip MIT sandığı bir
  kütüphanenin GPL olduğunu ürün sevkiyatından sonra fark ederse pahalı bir yeniden-yazım
  gerekebilir. Kullanılan her açık kaynak bileşenin lisansını proje başında bir listeye işlemek
  gerçek bir koruma sağlar.
- **Linter'ların emniyet-standardı eşlemeleri** (MISRA-C, IEC 61508/62443) tam sertifika yerine
  geçmez ama kod incelemesini hızlandırır ve denetime hazırlık katmanı sağlar — sertifikasyon
  sürecine girmeden önce kodu "temizlemek" için değerlidir.

## İlgili Konular

- `02_codesys_forge_store.md` — CODESYS-içi (Forge) açık kaynak alternatifi; co♻e/CfUnit orada da var
- `01_oscat_library.md` — GitHub'da V3 port'ları bulunan açık kaynak kütüphane örneği
- `knowledge/codesys/programming/03_function_blocks.md` — test edilebilir FB tasarımı (test çatısının ön koşulu)
- `knowledge/codesys/project-generation/03_plcopen_xml.md` — Git/CI'yı mümkün kılan metin export
- `knowledge/codesys/programming/04_libraries.md` — GitHub kütüphanelerini projeye dahil etme
