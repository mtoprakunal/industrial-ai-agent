---
KONU        : CODESYS Temeller — Uzman Sentezi
KATEGORİ    : codesys
ALT_KATEGORI: fundamentals
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    başlık: "CODESYS Runtime Mimarisi (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/fundamentals/02_project_structure.md"
    başlık: "CODESYS Proje İç Yapısı (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/fundamentals/03_iec61131_languages.md"
    başlık: "IEC 61131-3 Programlama Dilleri (Uzman)"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_runtime_architecture.md"
    ilişki: detaylandırır
  - konu: "02_project_structure.md"
    ilişki: detaylandırır
  - konu: "03_iec61131_languages.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "Üç temel belgenin Uzman seviyesindeki tüm bölümleri okunmuş olmalıdır."
  - "Saha devreye alma (commissioning) ve hata ayıklama deneyimi varsayılır."
ÇELİŞKİLER :
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez belgesi yeni çelişki içermez; kaynak belgelere atıflar yapar."
---

## Özün Ne

Bu sentez iki katmanlıdır. Yeni başlayan için: üç belge birbirinin parçasıdır — Runtime zemini, Proje Yapısı iskeleti, Diller içeriği tanımlar. **Uzman için** ise asıl mesaj farklıdır: bu üç katman birbirinden bağımsız öğrenilen konular değil, **aynı tasarım felsefesinin** üç yüzüdür. CODESYS'in her kararı tek bir hedefe hizmet eder: **donanımdan bağımsız, deterministik, doğrulanabilir endüstriyel kontrol.** Runtime'da JIT'in olmaması, proje yapısında Online Change'in arayüz değişikliğini reddetmesi, dillerin tek bir AST'ye derlenmesi — üçü de bu felsefenin sonucudur. Uzmanlık, bu bağlantıyı görüp sahada karşılaşılan tuhaflıkları (jitter, retain kaybı, takılan SFC) bu felsefeden türetebilmektir.

## Nasıl Çalışır

### Üç Belgenin Birbirine Bağlantısı

```
┌────────────────────────────────────────────────────────────────────┐
│                    CODESYS TEMEL ZİHİN HARİTASI                    │
├─────────────────────────────────────────────────────────────────────┤
│  01_runtime_architecture.md                                          │
│  ┌──────────────────────────────────────────────┐                   │
│  │  RUNTIME (CODESYS Control)                   │                   │
│  │  • Component Manager + Execution Engine      │                   │
│  │  • Task Scheduler → Scan Cycle → I/O Image   │                   │
│  │  • pthread/SCHED_FIFO (Linux) | RTSS (Win)   │                   │
│  └──────────────────┬───────────────────────────┘                   │
│                     │ Runtime, projeyi çalıştırır                   │
│                     ▼                                                │
│  02_project_structure.md                                             │
│  ┌──────────────────────────────────────────────┐                   │
│  │  PROJE (Device Tree)                         │                   │
│  │  Device → PLC Logic → Application →          │                   │
│  │    Task Config | POU | GVL | DUT | Library   │                   │
│  │  GUID grafiği · sembolik I/O mapping         │                   │
│  └──────────────────┬───────────────────────────┘                   │
│                     │ POU'lar belirli bir dilde yazılır              │
│                     ▼                                                │
│  03_iec61131_languages.md                                            │
│  ┌──────────────────────────────────────────────┐                   │
│  │  DİLLER (IEC 61131-3 + CFC)                  │                   │
│  │  ST → algoritma/OOP · LD → interlock         │                   │
│  │  FBD → sinyal · SFC → sekans · IL → eski     │                   │
│  │  Hepsi → tek ortak AST → native kod          │                   │
│  └──────────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────┘
```

### Tasarım Felsefesi: Tek Bir İlke, Üç Yansıma

| Tasarım Kararı | Hangi Belge | Hizmet Ettiği İlke |
|---|---|---|
| JIT yok, deterministik execution engine | 01 | Her döngü aynı süre → determinizm |
| I/O image (çift tampon) | 01 | Scan içinde giriş tutarlılığı |
| Component Manager (200+ modül) | 01 | Donanım/lisans modülerliği |
| Online Change arayüz değişikliğini reddeder | 02 | Çalışan bellek görüntüsünü koru |
| Device Tree fiziksel topolojiyi yansıtır | 02 | Configuration-as-data, taşınabilirlik |
| Sembolik I/O mapping (`AT %` yerine) | 02 | Topoloji değişiminde sağlamlık |
| 5 dil → tek AST | 03 | Temsil çeşitliliği, semantik birliği |
| OOP yalnızca ST'de | 03 | Test edilebilir, yeniden kullanılabilir kod |

**Uzman içgörüsü:** Sahada bir tuhaflık gördüğünüzde "hangi ilke ihlal edildi?" diye sorun. Jitter → determinizm katmanı (RT-preempt/affinity) eksik. Retain kaybı → bellek görüntüsü korunamadı. Takılan SFC → transition semantiği yanlış. Felsefe, hata tanısının pusulasıdır.

### "Yeni Başlayan" İçin Özet Mental Model

> **Runtime**: Bilgisayarı PLC'ye dönüştüren yazılım katmanı/servis. Donanımla konuşur, IEC kodunu deterministik çalıştırır.

> **Proje Yapısı**: Runtime'ın çalıştıracağı her şeyin GUID'li obje grafiği. Device → Application → Task/Library/POU/GVL/DUT.

> **Diller**: POU içini dolduran 5 IEC dili (+ CFC). Hepsi aynı derleyiciye iner; fark düşünce biçiminde ve okunabilirliktedir.

### Hızlı Referans Tabloları (Konsolide)

**A. Runtime Varyantı Seçimi (Belge 1)**

| Varyant | Platform | Gerçek Zamanlılık | Ne Zaman |
|---|---|---|---|
| Control Win SL | Windows | Soft-RT | Sadece geliştirme/test |
| Control RTE SL | Windows + RTSS | Hard-RT | Windows tabanlı üretim IPC |
| Control Linux SL | Linux (RT-preempt) | Soft/Hard-RT | **Üretim ortamı** |
| Virtual Control SL | Docker | Soft-RT | Bulut, sanal test |
| Control for Raspberry Pi | Linux/ARM | Soft-RT | Eğitim, prototip |

**B. POU Türü Seçimi (Belge 2)**

| Tür | Durum | Instance | Ne İçin |
|---|---|---|---|
| PROGRAM | Durumlu | Tekil | Orkestrasyon, task'a atanan kök |
| FUNCTION_BLOCK | Durumlu | Çoklu | Yeniden kullanılan mantık, kütüphane |
| FUNCTION | Durumsuz | Yok | Saf dönüşüm/hesap |

**C. Dil Seçimi (Belge 3)**

| Senaryo | Önerilen Dil |
|---|---|
| Algoritma, math, OOP, kütüphane | **ST** |
| Boolean interlock, acil durum, saha bakımı | **LD** |
| PID, analog sinyal akışı | **FBD** |
| 5+ adımlı sıralı döngü, batch | **SFC + ST** |
| Yeni proje | **IL kullanma** (deprecated) |

**D. Kritik Eşik Değerler ve Kurallar**

| Konu | Değer / Kural | Kaynak |
|---|---|---|
| Task yük güvenli sınırı | Exec/Cycle **< %70** | Belge 1 |
| Demo modu süresi | 2 saat → lisans şart | Belge 1 |
| `TIME` taşması | ~49.7 gün (32-bit ms) | Belge 1 |
| En kısa cycle time | 250µs–1ms (platform) | Belge 1 |
| Task priority aralığı | 0 (yüksek) – 31 (düşük) | Belge 2 |
| I/O notasyonu | `%I` / `%Q` / `%M` | Belge 2 |
| Kütüphane versiyonu | "newest" değil, **sabit** | Belge 2 |
| Retain layout | Sıra ASLA değişmez, **sona ekle** | Belge 2 |
| `REAL` karşılaştırma | `=` ASLA, tolerans bandı kullan | Belge 3 |
| Timer çağrısı | Her scan **koşulsuz** çağır | Belge 3 |
| ST performansı | C'ye göre ~3-5x yavaş | Belge 1, 3 |

**E. İsimlendirme Önekleri (Belge 2)**

```
x=BOOL  r=REAL  n=INT  w=WORD  dw=DWORD  s=STRING
t=TIME  a=ARRAY  st=STRUCT  e=ENUM  fb=FB instance
```

### Uzman Edge Case Konsolidasyonu (Üç Belgeden)

Sessiz, görünmez hataların ortak listesi — production öncesi kontrol için:

```
KATMAN      EDGE CASE                          BELİRTİ                  KORUMA
─────────────────────────────────────────────────────────────────────────────
Runtime     Cycle overrun < watchdog          Sessiz jitter birikimi   MaxCycleTime izle
Runtime     TIME 49.7 günde taşar             Uptime sayacı sıfırlanır LTIME/DWORD kullan
Runtime     RTC pili bitik → 1970             Bozuk zaman damgası      NTP boot'ta zorunlu
Proje       Retain sıra değişti               Sessiz veri bozulması    Sona ekle, sabit sıra
Proje       Online Change + pointer           Rastgele crash           ADR() her scan
Proje       AT %Q topoloji kayması            Yanlış çıkış aktif        Sembolik mapping
Diller      REAL eşitlik (=)                  Takılan transition       Tolerans bandı
Diller      Koşullu timer çağrısı             Donan/atlayan zaman       Koşulsuz çağrı
Diller      INT taşması (wrap)                Sessiz yanlış sayım       UDINT + sınır kontrol
Diller      AND kısa devre garantisi yok      Null deref crash          İç içe IF
```

## Pratikte Nasıl Kullanılır

### Production-Grade Devreye Alma Kontrol Listesi (Uzman)

Temel "ilk proje" listesinin ötesinde, **üretime geçiş** için:

```
RUNTIME / GERÇEK ZAMANLILIK (Belge 1)
□ RT-preempt kernel doğrulandı (uname → PREEMPT_RT)
□ BIOS: C-states / SpeedStep / Turbo / HT KAPALI
□ isolcpus + irqaffinity + nohz_full ayarlandı
□ Runtime SetAffinityMask izole çekirdeklere pinli
□ CPU governor = performance
□ MaxCycleTime/Jitter OPC UA ile SCADA'ya raporlanıyor
□ Lisans yüklü (demo modu DEĞİL)
□ Create Boot Application yapıldı + power-cycle ile doğrulandı

PROJE (Belge 2)
□ Kütüphane sürümleri sabitlendi (newest YOK)
□ Retain/Persistent ayrı listede, sıra dondurulmuş
□ I/O mapping sembolik (AT % yok), topoloji testi yapıldı
□ Device description sürümü takım genelinde sabit (.devpkg saklı)
□ Static Analysis temiz (warnings as errors)
□ Sembol konfigürasyonu sadece gerekli değişkenleri içeriyor

DİLLER / KOD (Belge 3)
□ REAL karşılaştırmalarda = yok, tolerans var
□ Timer/counter FB'leri koşulsuz çağrılıyor
□ Sıcak task'ta string/SFC yok
□ CFC execution order'lar kontrol edildi
□ POU dilleri bağlama uygun (interlock=LD, algoritma=ST)
```

### Performans Optimizasyon Sıralaması (Tüm Belgelerden)

Etki/çaba oranına göre uygulama sırası:

```
1. BIOS C-state kapatma          → en büyük jitter kaynağını yok eder (Belge 1)
2. CPU izolasyonu (isolcpus)     → OS gürültüsünü ayırır (Belge 1)
3. Veri yapısı (ARRAY+FOR)       → algoritmik kazanç, dilden bağımsız (Belge 3)
4. Pass-by-reference (büyük data)→ kopya maliyetini siler (Belge 2)
5. Loop-invariant hoisting       → sıcak döngü hesabını azaltır (Belge 3)
6. STRUCT alan sıralama          → bellek/cache verimi (Belge 2)
7. Task katmanlama (hız/orta/yavaş)→ scheduler dengesi (Belge 1,3)
```

### Üç Belgeyi Bağlayan Pratik Senaryo

**Görev**: Konveyör motoru başlatma butonundan 2sn sonra çalışsın, durdurma/acil-stop ile dursun.

```
ADIM 1 — Runtime (Belge 1): Communication Settings → Gateway bağlan
ADIM 2 — Proje (Belge 2): GVL_IO + FB_Conveyor + PLC_PRG + MainTask(10ms)
ADIM 3 — Dil (Belge 3): FB_Conveyor içinde ST + CASE state machine

  FUNCTION_BLOCK FB_Conveyor
  VAR_INPUT  xStart, xStop, xEmgStop : BOOL; END_VAR
  VAR_OUTPUT xMotorOut : BOOL; END_VAR
  VAR  tDelay : TON;  eState : (eIdle, eWaiting, eRunning); END_VAR

  tDelay(IN := (eState = eWaiting), PT := T#2S);   (* koşulsuz çağrı! *)
  CASE eState OF
      eIdle:    IF xStart THEN eState := eWaiting; END_IF
      eWaiting: IF tDelay.Q THEN eState := eRunning; END_IF
      eRunning: xMotorOut := TRUE;
                IF xStop OR xEmgStop THEN
                    xMotorOut := FALSE; eState := eIdle;
                END_IF
  END_CASE

ADIM 4 — PLC_PRG'de çağır → GVL'den besle, çıkışı I/O'ya aktar
ADIM 5 — Build → Download → Create Boot App → power-cycle test
```

Dikkat: Bu uzman versiyonda timer **koşulsuz** çağrılır (`IN` ile kontrol) — Belge 3 Not 7'deki tuzaktan kaçınır.

## Örnekler

### Kavramsal Harita: Ne Nerede Duruyor?

```
Soru                                      Cevap (Kaynak Belge)
─────────────────────────────────────────────────────────────────
"Motor kodum nereye yazılır?"             Function Block (Belge 2)
"Scan cycle kaç ms olmalı?"               Task Config, %70 kuralı (1,2)
"Jitter neden 200µs spike yapıyor?"       BIOS C-states (Belge 1)
"Retain değerlerim neden sıfırlandı?"     Layout değişti (Belge 2)
"SFC neden o adımda takıldı?"             REAL eşitlik / transition (Belge 3)
"Online Change neden reddedildi?"         Arayüz/sıra değişti (Belge 2)
"Timer neden bazen donuyor?"              Koşullu çağrı (Belge 3)
"Çıkışlar neden yanlış kanala gitti?"     AT % adres kayması (Belge 2)
"Neden JIT yok, yavaş değil mi?"          Determinizm tasarımı (Belge 1)
"Git merge neden projeyi bozdu?"          GUID grafiği, XML (Belge 2)
```

### Öğrenme Yol Haritası (Uzmanlık Hattı)

```
TEMEL (0-1 ay)
└── 3 belgenin "Özün Ne / Nasıl Çalışır / Pratik" bölümleri
    Pratik: Win SL + Standard Project, motor FB, ST CASE

ORTA (1-3 ay)
└── "Sık Yapılan Hatalar" + "Gerçek Proje Notları"
    Pratik: çoklu task, SFC, GVL katmanlama, I/O mapping

UZMAN (3-12 ay) ← bu belgelerin yeni bölümleri
├── Edge Case'ler: sessiz hataları tanıma ve test etme
├── Optimizasyon: RT tuning, bellek düzeni, profiling
├── Derin Teknik Detay: tasarım kararlarının "neden"i
└── Pratik: production RT tuning, kütüphane mimarisi,
    OOP + interface, Online Change disiplini, static analysis
```

## Sık Yapılan Hatalar

### Başlangıç Hataları (5) — Temeller Önler

1. **Tüm kodu PLC_PRG'ye yazmak** (Belge 2) — FB mimarisi şart.
2. **Demo lisansla üretim** (Belge 1) — 2 saatte durur.
3. **Windows SoftPLC ile RT beklemek** (Belge 1) — RTE/Linux RT gerekir.
4. **Her değişkeni GVL'ye koymak** (Belge 2) — yerel veri POU'da.
5. **Algoritmayı LD'de yazmak** (Belge 3) — math/algoritma ST'de.

### Uzman Hataları (5) — Sahada Pahalıya Patlayan

1. **RT tuning'i atlamak** (Belge 1) — "kod doğru ama jitter var" → BIOS/isolcpus.
2. **Retain/Online Change disiplinsizliği** (Belge 2) — sessiz veri kaybı, dangling pointer.
3. **`AT %` doğrudan adresleme** (Belge 2) — topoloji değişince tehlikeli çıkış.
4. **REAL `=` ve koşullu timer** (Belge 3) — takılan sekans, donan zaman.
5. **Tek dile saplanmak** (Belge 3) — ne hep-LD ne hep-ST; bağlam belirler.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Bu Üç Belge Ne Zaman Yetmez?

```
Yetersiz Kaldığı Durum              Bakılacak Sonraki Konu
─────────────────────────────────────────────────────────
Motion control entegrasyonu         → knowledge/codesys/softmotion/
EtherCAT slave konfigürasyonu       → knowledge/networking/ethercat/
OPC UA server / sembol yönetimi     → knowledge/protocols/opc-ua/
WebVisu HMI tasarımı                → knowledge/hmi/webvisu/
Güvenlik (SIL) gereksinimleri       → knowledge/standards/safety_plc/
Ekip git workflow / CODESYS Git     → knowledge/codesys/pro_developer/
Profiling, trace, performans tuning → knowledge/codesys/advanced/profiling/
OOP, interface, kalıtım derinliği   → knowledge/codesys/advanced/oop_codesys/
```

## Gerçek Proje Notları

**Sentez Notu 1 — Felsefeyi Bir Kez Anla, Yüz Hatayı Çöz**  
Uzmanlığın eşiği: CODESYS'in her tuhaflığını tek tek ezberlemek yerine, "determinizm + bellek görüntüsü koruma + donanım soyutlama" üçlüsünden türetebilmek. Jitter, retain kaybı, reddedilen Online Change, takılan SFC — hepsi bu felsefenin kenar durumlarıdır. Felsefe pusula, edge case'ler harita.

**Sentez Notu 2 — "Kod Doğru Ama Çalışmıyor" = Çoğunlukla Katman Sorunu**  
Saha deneyimi: uzman seviyede sorunların büyük kısmı IEC kodunda değil, **alt katmanlardadır** — RT tuning (Belge 1), proje konfigürasyonu (Belge 2), dil semantiği inceliği (Belge 3). Kodu defalarca okumak yerine katmanı sorgulayın: "Bu bir scheduler mı, mapping mi, yoksa floating-point mi sorunu?"

**Sentez Notu 3 — Determinizm Bir Bütündür, Zinciri En Zayıf Halka Belirler**  
Mükemmel ST kodu + RT-preempt kernel + izole CPU, ama BIOS'ta C-state açıksa → jitter. Mükemmel mapping ama `AT %` kullanılmışsa → topoloji riski. Determinizm uçtan uca bir özelliktir; tek bir katmanın ihmali tüm zinciri bozar.

**Sentez Notu 4 — Online Change Hem Nimet Hem Tuzak**  
CODESYS'in en güçlü özelliği (çalışan makineyi durdurmadan güncelleme) aynı zamanda en sinsi hata kaynağıdır (dangling pointer, retain layout). Uzman kuralı: Online Change'i günlük geliştirmede kullan, ama **kritik devreye almada planlı duruş + clean download + boot app + power-cycle testi** yap. Hangisinin ne zaman güvenli olduğunu bilmek, Belge 2'deki "kabul/ret" listesini bilmektir.

**Sentez Notu 5 — Dil Çeşitliliği Bir Araç Kutusudur, İdeoloji Değil**  
"Hep ST" ya da "hep LD" kampları yanlış sorar. Doğru soru: "Bu POU'yu kim okuyacak ve ne yapıyor?" Saha teknisyeni bakacak interlock → LD. Yeniden kullanılacak test edilebilir mantık → ST + OOP. 8 adımlı batch sekansı → SFC + ST. Hepsi aynı AST'ye derlendiği için (Belge 3, Derin Teknik Detay) performans cezası yok; seçim tamamen okunabilirlik ve bakım içindir.

## İlgili Konular

```
knowledge/codesys/fundamentals/      ← Şu an buradasınız (Uzman seviye)
├── 01_runtime_architecture.md   (Uzman)
├── 02_project_structure.md      (Uzman)
├── 03_iec61131_languages.md     (Uzman)
└── _synthesis.md (bu belge)

Sonraki adım — İleri/Uzman Derinleşme:
knowledge/codesys/
├── tasks/            (task_types, task_priority_design)
├── libraries/        (standard_library, util_library)
├── best_practices/   (naming_conventions, fb_design_patterns)
├── advanced/         (oop_codesys, unit_testing, profiling)
├── softmotion/
└── visualization/

knowledge/protocols/  (opc-ua, modbus)
knowledge/networking/ (ethercat)
knowledge/standards/  (safety_plc, isa88_batch)
```
