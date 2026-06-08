---
KONU        : CODESYS Temeller — Sentez
KATEGORİ    : codesys
ALT_KATEGORI: fundamentals
SEVİYE      : Temel
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    başlık: "CODESYS Runtime Mimarisi"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/fundamentals/02_project_structure.md"
    başlık: "CODESYS Proje İç Yapısı"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/fundamentals/03_iec61131_languages.md"
    başlık: "IEC 61131-3 Programlama Dilleri"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_runtime_architecture.md"
    ilişki: detaylandırır
  - konu: "02_project_structure.md"
    ilişki: detaylandırır
  - konu: "03_iec61131_languages.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "Bu sentez, üç temel belgeyi okuduktan sonra okunmak üzere tasarlanmıştır."
ÇELİŞKİLER :
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez belgesi yeni çelişki içermez; kaynak belgelere atıflar yapar."
---

## Özün Ne

Bu sentez, "CODESYS'e yeni başlayan biri üç temel belgeyi okuyunca ne anlamalı?" sorusuna yanıt verir. Üç belge birbirinin parçasıdır: Runtime, projenin çalıştığı zemini tanımlar; Proje Yapısı, o zemin üzerinde inşa edilen mimarinin iskeletini açıklar; Diller ise o iskeletin içini dolduran düşünce biçimlerini sunar. Bu üçü bir arada anlaşıldığında CODESYS'in neden bu şekilde tasarlandığı ve nasıl kullanılacağı netleşir.

## Nasıl Çalışır

### Üç Belgenin Birbirine Bağlantısı

```
┌────────────────────────────────────────────────────────────────────┐
│                    CODESYS TEMEL ZİHİN HARİTASI                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  01_runtime_architecture.md                                          │
│  ┌──────────────────────────────────────────────┐                   │
│  │           RUNTIME (CODESYS Control)          │                   │
│  │                                              │                   │
│  │  • Herhangi bir donanımı IEC kontrolcüye     │                   │
│  │    dönüştüren yazılım katmanı                │                   │
│  │  • Component Manager + Execution Engine      │                   │
│  │  • Task Scheduler → Scan Cycle → I/O Image   │                   │
│  │  • Windows / Linux / ARM / VxWorks           │                   │
│  └──────────────────┬───────────────────────────┘                   │
│                     │ Runtime, projeyi çalıştırır                   │
│                     ▼                                                │
│  02_project_structure.md                                             │
│  ┌──────────────────────────────────────────────┐                   │
│  │          PROJE (Device Tree)                 │                   │
│  │                                              │                   │
│  │  Device → Application → Library Manager     │                   │
│  │                       → Task Configuration  │                   │
│  │                       → POU'lar (Kod)        │                   │
│  │                       → GVL'ler (Değişken)   │                   │
│  │                       → DUT'lar (Tip)        │                   │
│  └──────────────────┬───────────────────────────┘                   │
│                     │ POU'lar belirli bir dilde yazılır              │
│                     ▼                                                │
│  03_iec61131_languages.md                                            │
│  ┌──────────────────────────────────────────────┐                   │
│  │          DİLLER (IEC 61131-3)                │                   │
│  │                                              │                   │
│  │  ST  → Algoritma, OOP, Math, Kütüphane      │                   │
│  │  LD  → Boolean, Interlock, Saha okunabilir  │                   │
│  │  FBD → Sinyal akışı, PID, Proses kontrol    │                   │
│  │  SFC → Sıralı döngü, Batch, State machine   │                   │
│  │  IL  → Deprecated — yeni projede kullanma   │                   │
│  └──────────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────┘
```

### "Yeni Başlayan" İçin Özet Mental Model

CODESYS'i anlamanın en kısa yolu şu üç cümleye sığar:

> **Runtime**: Bilgisayarı (veya gömülü cihazı) PLC'ye dönüştüren yazılım katmanı. Donanımla konuşur, IEC kodunu çalıştırır, gerçek zamanlılığı sağlar.

> **Proje Yapısı**: Runtime'ın çalıştıracağı her şeyin düzenlendiği hiyerarşi. Device altında Application, Application altında Task, Library, POU, GVL, DUT.

> **Diller**: POU'ların içini dolduran 5 IEC dili. ST en güçlü, LD en görsel, SFC en yapısal, FBD sinyal odaklı, IL artık eski.

### Hızlı Referans Tabloları (Üç Belgeden Konsolide)

Aşağıdaki tablolar üç temel belgenin "tek bakışta" özetidir; ezbere bakılacak başvuru kartı niteliğindedir.

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
| PROGRAM | Durumlu | Tekil | Orkestrasyon (PLC_PRG), task'a atanan kök |
| FUNCTION_BLOCK | Durumlu | Çoklu | Yeniden kullanılan mantık (FB_Motor), kütüphane |
| FUNCTION | Durumsuz | Yok | Saf dönüşüm/hesap (ölçekleme, bit işlem) |

**C. Dil Seçimi (Belge 3)**

| Senaryo | Önerilen Dil |
|---|---|
| Algoritma, math, OOP, kütüphane | **ST** |
| Boolean interlock, acil durum, saha bakımı | **LD** |
| PID, analog sinyal akışı, proses kontrol | **FBD** |
| 5+ adımlı sıralı döngü, batch (ISA S88) | **SFC + ST** |
| Yeni proje | **IL kullanma** (deprecated) |

**D. Kritik Eşik Değerler ve Kurallar**

| Konu | Değer / Kural | Kaynak |
|---|---|---|
| Task yük güvenli sınırı | Exec Time / Cycle Time **< %70** | Belge 1 |
| Demo modu süresi | 2 saat sonra durur → lisans şart | Belge 1 |
| Task priority aralığı | 0 (en yüksek) – 31 (en düşük) | Belge 2 |
| I/O notasyonu | `%I` giriş, `%Q` çıkış, `%M` memory | Belge 2 |
| Kütüphane versiyonu | "newest" değil, **sabit versiyon** | Belge 2 |
| ST performansı | C'ye göre ~3-5x yavaş (ağır hesap → External Library) | Belge 1, 3 |

**E. İsimlendirme Önekleri (Belge 2)**

```
x=BOOL  r=REAL  n=INT  w=WORD  dw=DWORD  s=STRING
t=TIME  a=ARRAY  st=STRUCT  e=ENUM  fb=FB instance
```

## Pratikte Nasıl Kullanılır

### "İlk Proje" Kontrol Listesi

Aşağıdaki adımları sırayla tamamlayan biri, CODESYS'te temel bir çalışan proje kurabilir:

**Runtime Tarafı (Belge 1)**

```
□ 1. CODESYS Development System indir ve kur (ücretsiz)
□ 2. CODESYS Control Win V3 veya Control for Raspberry Pi indir
□ 3. Runtime'ı başlat (Windows'ta uygulama, Linux'ta systemctl)
□ 4. Demo modu: 2 saat sonra duruyor — geliştirme için yeterli
□ 5. IDE → Tools → Communication Settings → Gateway bağlantısı
```

**Proje Tarafı (Belge 2)**

```
□ 6. File → New Project → Standard Project
□ 7. Device: Kullandığın platforma uygun seç (veya Win V3 başlangıç için)
□ 8. Application altında GVL_IO ekle: giriş/çıkış değişkenlerini tanımla
□ 9. FB_Motor veya FB_Valve gibi function block'lar oluştur
□ 10. Task Configuration → MainTask → FB'leri çağır
□ 11. Build → Download → Start
```

**Dil Tarafı (Belge 3)**

```
□ 12. PLC_PRG içine basit ST kodu yaz: IF, CASE, FOR
□ 13. TON (Timer) kullanımını öğren — en temel yapı taşı
□ 14. CASE ile basit state machine yaz
□ 15. Bir Function Block yaz, PLC_PRG'den çağır
□ 16. İkinci bir POU'yu LD'de dene — farkı hisset
```

### Üç Belgeyi Bağlayan Pratik Senaryo

**Görev**: Bir konveyör bandı motoru, başlatma butonuna basıldıktan 2 saniye sonra çalışsın, durdurma butonuyla ya da acil stop ile durabilsin.

```
ADIM 1 — Runtime bağlantısı (Belge 1)
  IDE → Communication Settings → 192.168.1.100 → Bağlan

ADIM 2 — Proje yapısı kur (Belge 2)
  Application
  ├── GVL_IO          ← xStartBtn, xStopBtn, xEmgStop, xMotorOut tanımla
  ├── FB_Conveyor     ← Motor mantığı burada
  ├── PLC_PRG         ← FB'yi burada çağır
  └── Task Configuration → MainTask (10ms, Cyclic) → PLC_PRG

ADIM 3 — Dil seç ve yaz (Belge 3)
  FB_Conveyor içinde ST dili:

  FUNCTION_BLOCK FB_Conveyor
  VAR_INPUT
      xStart   : BOOL;
      xStop    : BOOL;
      xEmgStop : BOOL;
  END_VAR
  VAR_OUTPUT
      xMotorOut : BOOL;
  END_VAR
  VAR
      tDelay : TON;
      eState : (eIdle, eWaiting, eRunning);
  END_VAR

  CASE eState OF
      eIdle:
          IF xStart THEN eState := eWaiting; END_IF
      eWaiting:
          tDelay(IN := TRUE, PT := T#2S);
          IF tDelay.Q THEN
              tDelay(IN := FALSE);
              eState := eRunning;
          END_IF
      eRunning:
          xMotorOut := TRUE;
          IF xStop OR xEmgStop THEN
              xMotorOut := FALSE;
              eState := eIdle;
          END_IF
  END_CASE

ADIM 4 — PLC_PRG'de çağır
  fbConveyor(
      xStart   := GVL_IO.xStartBtn,
      xStop    := GVL_IO.xStopBtn,
      xEmgStop := GVL_IO.xEmgStop
  );
  GVL_IO.xMotorOut := fbConveyor.xMotorOut;

ADIM 5 — Build → Download → Start → Test
```

Bu senaryo üç belgenin kesişim noktasıdır: Runtime bağlantı, proje yapısı mimarisi ve ST dili bir arada çalışır.

## Örnekler

### Kavramsal Harita: Ne Nerede Duruyor?

```
Soru                                      Cevap (Kaynak Belge)
─────────────────────────────────────────────────────────────────
"Motor kodum nereye yazılır?"             Function Block (Belge 2)
"Scan cycle kaç ms olmalı?"               Task Config (Belge 1, 2)
"Değişkeni diğer POU'dan nasıl okurum?"   GVL (Belge 2)
"Sıralı makine döngüsü nasıl yazılır?"    SFC veya ST CASE (Belge 3)
"Runtime Linux'ta nasıl kurulur?"         systemctl (Belge 1)
"Kütüphane nasıl eklenir?"                Library Manager (Belge 2)
"TON bloğu nasıl kullanılır?"             ST veya LD'de (Belge 3)
"Birden fazla motor aynı FB'yi kullanabilir mi?" FB instance (Belge 2, 3)
"Watchdog nedir ve neden önemli?"         Runtime güvenliği (Belge 1)
"LD mi ST mi yazmalıyım?"                 Bağlama göre (Belge 3)
```

### Öğrenme Yol Haritası

```
BAŞLANGIÇ (0-2 hafta)
├── 01_runtime_architecture.md → CODESYS ne, SoftPLC ne
├── 02_project_structure.md   → Device Tree'yi tanı
└── Pratik: Control Win + Standard Project kur, motor FB yaz

TEMEL (2-4 hafta)
├── 03_iec61131_languages.md  → ST ve LD'yi dene
├── Pratik: TON, TOF, CTU öğren
├── Pratik: GVL ve DUT kullan
└── Pratik: Function Block yaz, test et

ORTA (1-2 ay)
├── Task yapılandırması → çoklu task, öncelik
├── SFC ile sıralı döngü yaz
├── Library Manager, hazır kütüphane kullan
└── I/O mapping ile gerçek veya sanal donanım bağla

İLERİ (2-6 ay)
├── OOP: Interface, Inheritance, Polymorphism (ST)
├── Harici kütüphane yaz (compiled-library)
├── EtherCAT / OPC UA entegrasyonu
└── Unit test, static analysis, versiyon kontrol (Git)
```

## Sık Yapılan Hatalar

### Başlangıçta En Çok Yapılan 5 Hata

Bu hataların tamamı üç temel belge okunduğunda önlenebilir:

**1. Tüm kodu PLC_PRG'ye yazmak** (Belge 2)  
Her makine elemanı için Function Block oluşturulmalıdır. PLC_PRG sadece orkestratördür.

**2. Demo lisansla üretim ortamı kurmak** (Belge 1)  
Runtime 2 saatte durur. Üretim ortamı mutlaka lisanslanmalıdır.

**3. Windows SoftPLC ile gerçek zamanlılık beklemek** (Belge 1)  
CODESYS Control Win SL gerçek zamanlı değildir. Üretim için RTE veya Linux RT gerekir.

**4. Her değişkeni GVL'ye koymak** (Belge 2)  
Yerel değişkenler POU'nun kendi VAR bölümünde olmalı. GVL yalnızca paylaşılan veriler içindir.

**5. "LD'yi herkes anlar" yanılgısıyla tüm algoritmayı LD'de yazmak** (Belge 3)  
LD basit interlock için güçlüdür. Matematiksel işlem ve algoritma için ST çok daha uygun ve okunabilirdir.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Bu Üç Belge Ne Zaman Yetmez?

Bu temeller şu konular için referans noktası değildir (daha ileri belgeler gerektirir):

```
Yetersiz Kaldığı Durum              Bakılacak Sonraki Konu
─────────────────────────────────────────────────────────
Motion control entegrasyonu         → knowledge/codesys/softmotion/
EtherCAT slave konfigürasyonu       → knowledge/networking/ethercat/
OPC UA server yapılandırması        → knowledge/protocols/opc-ua/
WebVisu HMI tasarımı                → knowledge/hmi/webvisu/
Güvenlik (SIL) gereksinimleri       → knowledge/standards/safety_plc/
Büyük ekip, git workflow            → knowledge/codesys/pro_developer/
Performans optimizasyonu            → knowledge/codesys/advanced/profiling/
```

## Gerçek Proje Notları

**Sentez Notu 1 — Üç Belge Arasındaki Zihinsel Geçiş**  
Deneyimde görülmüş en sık karışıklık: Yeni başlayanlar "runtime" ile "proje" arasındaki sınırı bulanık görüyor. Basit bir ayrım yardımcı olur: Runtime, siz olmadan da çalışır — bir servistir. Proje, sizin yazdığınız ve runtime'a yüklediğiniz içeriktir. Runtime sunucu, proje yazılım gibi düşünülebilir.

**Sentez Notu 2 — "Doğru Dil" Anksiyetesi**  
"Hangi dili kullanayım?" sorusu yeni başlayanları felç eder. Pratik önerim: **ST ile başlayın**. ST, tüm IEC yapılarını destekler, OOP için tek seçenektir, test edilebilir ve git-dostu koddur. LD ve SFC'yi seçici biçimde, güçlü oldukları yerde kullanın. Dil karışımından korkmayın; bir proje içinde farklı diller bir arada çalışır.

**Sentez Notu 3 — "SoftPLC = Gerçek PLC" Yanılgısı**  
CODESYS Control Win SL ile geliştirme yaparken her şey mükemmel çalışıyor. Üretim ortamında aynı proje gerçek donanıma geçince zamanlama sorunları, jitter, lisans sorunları ortaya çıkabiliyor. Üretim hedef platformunda erken test yapın; son dakika sürprizlerini önler.

**Sentez Notu 4 — Temel Belgelerin Değeri**  
Bu üç belge okunmadan onlarca saatlik "neden çalışmıyor" debugu yaşandığını gözlemledik. Runtime neden durdu? → Watchdog (Belge 1). Task neden çalışmıyor? → Task'a program atanmamış (Belge 2). Neden değişken başka POU'dan görünmüyor? → GVL'ye alınmamış (Belge 2). SFC transition neden geçmiyor? → Transition kodu yanlış (Belge 3). Temeller sağlamsa üst yapı hızla kurulur.

**Sentez Notu 5 — Bu Bilgi Tabanının Kullanım Önerisi**  
Bu üç belge + sentez, bir yeni ekip üyesinin ilk 2 haftasını yapılandırmak için tasarlandı. Önerilen akış:
1. Sentezi oku (bu belge) → Genel harita anlaşıldı
2. `01_runtime_architecture.md` → Runtime ne olduğu kavrandı
3. `02_project_structure.md` → Proje açık, sol panel anlaşıldı
4. `03_iec61131_languages.md` → İlk kod yazıldı, diller denendi
5. Senaryoyu uygula (bu belgede) → Motor FB örneği çalıştırıldı

## İlgili Konular

```
knowledge/codesys/fundamentals/      ← Şu an buradasınız
├── 01_runtime_architecture.md
├── 02_project_structure.md
├── 03_iec61131_languages.md
└── _synthesis.md (bu belge)

Sonraki adım — Orta Seviye:
knowledge/codesys/
├── tasks/
│   ├── task_types.md
│   └── task_priority_design.md
├── libraries/
│   ├── standard_library.md
│   └── util_library.md
└── best_practices/
    ├── naming_conventions.md
    └── fb_design_patterns.md

Sonraki adım — İleri Seviye:
knowledge/codesys/
├── advanced/
│   ├── oop_codesys.md
│   └── unit_testing.md
├── softmotion/
└── visualization/

knowledge/protocols/
├── opc-ua/
└── modbus/

knowledge/networking/
└── ethercat/
```
