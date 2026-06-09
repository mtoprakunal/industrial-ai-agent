---
KONU        : Endüstriyel Otomasyon Mimari Tasarım Kararları
KATEGORİ    : decisions
ALT_KATEGORI: architecture
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    başlık: "CODESYS Runtime Mimarisi — SoftPLC Varyantları ve Donanım Bağımsızlığı"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/_synthesis.md"
    başlık: "CODESYS Domain Üst Sentezi"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/task-structure/_synthesis.md"
    başlık: "CODESYS Task Yapısı Sentezi"
    güvenilirlik: deneyimsel
  - url: "knowledge/networking/_synthesis.md"
    başlık: "Endüstriyel Ağ Sentezi — Topoloji, Güvenlik, Performans"
    güvenilirlik: deneyimsel
  - url: "knowledge/hardware/industrial-pc/_synthesis.md"
    başlık: "Endüstriyel PC — SoftPLC Platformuna Giden Yol (Sentez)"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/_synthesis.md"
    başlık: "HMI Domain Üst Sentezi"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/task-structure/_synthesis.md"
    ilişki: gerektirir
  - konu: "knowledge/networking/_synthesis.md"
    ilişki: gerektirir
  - konu: "knowledge/decisions/protocol-selection"
    ilişki: tamamlar
  - konu: "knowledge/decisions/hmi-technology"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "CODESYS Runtime mimarisi: SoftPLC kavramı, varyantlar, scan cycle (01_runtime_architecture.md)"
  - "Task yapısı temelleri: Cyclic/Freewheeling/Event, öncelik, cycle time (task-structure/_synthesis.md)"
  - "Purdue/ISA-95 ağ katmanları, VLAN, segmentasyon (networking/_synthesis.md)"
  - "Endüstriyel PC kurulum ve performans tuning (hardware/industrial-pc/_synthesis.md)"
  - "HMI teknoloji manzarası: Web HMI, SCADA Platform, Panel HMI (hmi/_synthesis.md)"
ÇELİŞKİLER :
  - kaynak: "hardware/industrial-pc/_synthesis.md — Linux SL vs Windows RTE"
    konu: "Linux RT ile Windows RTE arasındaki jitter performansı karşılaştırması"
    çözüm: >
      Linux PREEMPT_RT + doğru optimizasyon genellikle daha düşük jitter üretir;
      ancak bu, CPU izolasyonu, IRQ yönetimi ve BIOS yapılandırmasının eksiksiz
      uygulanmasını gerektirir. Windows RTE daha kolay kurulum ve bakım sunar;
      ekip Windows bilgisi ve mevcut altyapı gözetilerek seçim yapılmalıdır.
  - kaynak: "codesys/fundamentals/01_runtime_architecture.md — donanım bağımsızlığı iddiası"
    konu: "Runtime 'hardware-independent' iddiasının gerçek kapsamı"
    çözüm: >
      IEC 61131-3 uygulama mantığı gerçekten taşınabilirdir; ancak device description
      dosyaları, fieldbus sürücüleri ve HAL katmanı donanıma özgüdür. Tam bağımsızlık
      yalnızca application logic katmanında geçerlidir — bunu bilen mimar, donanım
      değişikliğinin ne kadar iş gerektireceğini önceden kestirebilir.
  - kaynak: "networking/_synthesis.md — Purdue'nun güncelliği"
    konu: "Purdue modelinin modern IT/OT konverjans ortamında geçerliliği"
    çözüm: >
      Purdue fiziksel ağ topolojisi olarak uygulanmasa da kavramsal katman modeli
      olarak IEC 62443 Zone-Conduit mimarisinde hâlâ temel referanstır. Modern
      tesislerde fiziksel Purdue yerine VLAN + FW ile mantıksal Purdue uygulanır;
      ancak "komşu olmayan katmanlar doğrudan iletişim kuramaz" kuralı değişmez.
  - kaynak: "hmi/_synthesis.md — polling her şeyi çözer algısı"
    konu: "OPC UA subscription vs polling: performans ve tasarım etkisi"
    çözüm: >
      OPC UA subscription standart seçimdir; polling yalnızca OPC UA sunucusu
      olmayan legacy Modbus cihazlarında kaçınılmazdır. Polling seçimi HMI
      backend yükünü ve gecikme davranışını doğrudan etkiler.
---

## Özün Ne

Bir endüstriyel otomasyon sistemi mimarlanırken verilen her karar sonraki kararları kısıtlar. Hangi PLC platformunun seçildiği task mimarisini, task mimarisi ağ topolojisini, ağ topolojisi HMI erişim modelini doğrudan etkiler. Bu belge, bu kararları birbirinden yalıtılmış teknik tercihler olarak değil, birbiriyle bağlantılı mimari seçimler olarak ele alır.

Belgede sekiz kritik karar alanı tanımlanmıştır: SoftPLC platform seçimi, Application mimarisi (tek/çok), task yapısı tasarımı, merkezi vs dağıtık kontrol, IPC seçimi, ağ topolojisi ve segmentasyonu, HMI yaklaşımı ile edge vs bulut dağılımı. Her karar alanı için kriterler, trade-off'lar ve somut senaryo-karar örnekleri sunulmaktadır.

**Bu belgeyi okuyun eğer:** Yeni bir otomasyon projesi mimarlamaya başlıyorsanız, mevcut sistemin neden belirli kararlar içerdiğini anlamak istiyorsanız veya benzer projeler için tekrar kullanılabilir bir karar şablonu arıyorsanız.

---

## Nasıl Çalışır

### Karar Akış Haritası: Hangi Karar Hangisini Belirler

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              ENDÜSTRİYEL OTOMASYON MİMARİ KARAR AKIŞI                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ① SoftPLC vs Donanım PLC                                                    │
│  ┌────────────────────────────────────────────────────────────────────┐      │
│  │  Win SL (geliştirme) │ Linux SL (üretim) │ RTE SL (Windows RT)    │      │
│  │  vs. Siemens/Beckhoff/Allen-Bradley donanım PLC                   │      │
│  └─────────────────────────────┬──────────────────────────────────────┘      │
│                                │ Platform seçimi                             │
│                                ▼                                             │
│  ② Application Mimarisi                                                      │
│  ┌────────────────────────────────────────────────────────────────────┐      │
│  │  Tek Application (basit) │ Çok Application (modüler)               │      │
│  │  Runtime üzerinde kaç bağımsız uygulama?                           │      │
│  └─────────────────────────────┬──────────────────────────────────────┘      │
│                                │ Uygulama sınırları                          │
│                                ▼                                             │
│  ③ Task Mimarisi                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐      │
│  │  Kaç task? Hangi tipte? Cycle time? Öncelik hiyerarşisi?           │      │
│  │  Safety(0) → Motion(1) → Control(2) → HMI(5) → Arkaplan(15)      │      │
│  └─────────────────────────────┬──────────────────────────────────────┘      │
│                                │ Zamanlama gereksinimleri                    │
│                                ▼                                             │
│  ④ Merkezi vs Dağıtık Kontrol                                                │
│  ┌────────────────────────────────────────────────────────────────────┐      │
│  │  Tek IPC/PLC vs Birden fazla kontrolcü + koordinasyon              │      │
│  └─────────────────────────────┬──────────────────────────────────────┘      │
│                                │ Fiziksel dağılım                            │
│                                ▼                                             │
│  ⑤ IPC Seçimi                                                                │
│  ┌────────────────────────────────────────────────────────────────────┐      │
│  │  Donanım spec (CPU, RAM, NIC sayısı), form faktör, işletim sistemi │      │
│  └─────────────────────────────┬──────────────────────────────────────┘      │
│                                │ Fiziksel platform                           │
│                                ▼                                             │
│  ⑥ Ağ Topolojisi ve Segmentasyon                                             │
│  ┌────────────────────────────────────────────────────────────────────┐      │
│  │  Purdue katmanları (L0–L5), VLAN, iDMZ, fieldbus seçimi           │      │
│  │  Yıldız / Halka+MRP / PRP-HSR / Hibrit                            │      │
│  └─────────────────────────────┬──────────────────────────────────────┘      │
│                                │ Bağlantı mimarisi                           │
│                                ▼                                             │
│  ⑦ HMI Yaklaşımı                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐      │
│  │  Web HMI │ SCADA Platform (Ignition/WinCC) │ CODESYS WebVisu       │      │
│  │  Panel HMI │ Masaüstü SCADA                                        │      │
│  └─────────────────────────────┬──────────────────────────────────────┘      │
│                                │ İzleme katmanı                              │
│                                ▼                                             │
│  ⑧ Edge vs Bulut                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐      │
│  │  Yerel işleme / edge analitik / historian vs bulut entegrasyonu    │      │
│  └────────────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sekiz Kararın Birbirine Bağımlılığı

Kararlar bağımsız alınamaz. Örneğin:

- EtherCAT fieldbus seçilirse (⑥), task cycle time en az 2ms olmalıdır (③), bu da CPU çekirdeğine ve IPC spec'ine (⑤) doğrudan kısıt getirir.
- Çok Application mimarisi seçilirse (②), her Application kendi task yapısına ve lifecycle'ına sahip olabilir; bu hem tasarım esnekliği hem de hata izolasyonu sağlar.
- Web HMI seçilirse (⑦), OPC UA sunucusu açık olmalı, ağ segmentasyonunda HMI VLAN'ı ile OPC UA port 4840 erişimi planlanmış olmalıdır (⑥).

---

## Pratikte Nasıl Kullanılır

Bu bölüm her karar alanını ayrı ayrı ele alır: kriter tablosu, trade-off açıklaması ve somut senaryo-karar örnekleri.

---

### Karar 1 — SoftPLC Platform Seçimi

#### Karar Kriterleri Tablosu

| Kriter | CODESYS Win SL | CODESYS Linux SL | CODESYS RTE SL | Donanım PLC |
|---|---|---|---|---|
| **Gerçek zamanlılık** | Soft-RT (Windows scheduler) | Hard-RT (PREEMPT_RT ile) | Hard-RT (RTSS kernel) | Hard-RT (ASIC) |
| **Tipik jitter** | 1–50ms (spike'lı) | 18–100µs (optimize edilmiş) | < 100µs | < 1µs (ASIC) |
| **Geliştirme hızı** | Çok hızlı (kendi PC) | Orta (Linux kurulumu gerekir) | Orta | Yavaş (donanım bağımlı) |
| **Lisans maliyeti** | Düşük | Düşük (OS lisansı yok) | Orta (Windows + RTSS) | Yüksek |
| **Fieldbus desteği** | EtherCAT/PROFINET sınırlı | Full (PROFINET, EtherCAT) | Full | Üretici bağımlı |
| **SIL desteği** | Hayır | Hayır | Hayır | Bazıları (IEC 61508) |
| **Donanım bağımsızlığı** | Orta (Windows + x86) | Yüksek (ARM, x86, MIPS) | Düşük (Windows x86) | Yok |
| **Bakım zorluğu** | Düşük (BT bilgisi yeter) | Orta (Linux bilgisi gerekir) | Düşük-Orta | Düşük (OEM destek) |

**Kaynak:** `knowledge/codesys/fundamentals/01_runtime_architecture.md` — SoftPLC Varyantları tablosu; `knowledge/hardware/industrial-pc/_synthesis.md` — Ne Zaman Linux SL, Ne Zaman Windows SL/RTE tablosu.

#### Trade-Off Analizi

**SoftPLC'nin avantajı** donanım bağımsızlığıdır: IEC 61131-3 uygulama mantığı değişmeden farklı donanıma taşınabilir. Maliyet ve esneklik kazancı önemlidir. Dezavantajı, gerçek zamanlılık performansının OS ve donanım optimizasyonuna bağlı olmasıdır — optimize edilmemiş bir Linux SL kurulumu, bazen 10ms+ jitter üretir.

**Donanım PLC'nin avantajı** deterministik davranıştır: ASIC tabanlı tasarım, yazılım OS kesintilerinden bağımsız olarak mikrosaniye seviyesinde zaman tutarlılığı sağlar. Dezavantajı esneklik kaybı ve maliyettir.

Kritik ayrım (kaynak: `01_runtime_architecture.md` — Sık Yapılan Hatalar):

> CODESYS Control Win SL gerçek zamanlı değildir. Windows güncelleme, antivirus veya GPU sürücüsü CPU'yu istediği zaman keser. Semptom: 10ms döngü zaman zaman 50–100ms alır. Üretim için Linux PREEMPT_RT veya Windows RTE SL zorunludur.

#### Senaryo → Karar Örnekleri

**Senaryo 1A — Hızlı Prototip ve Geliştirme:**
Müşteri sunumu için çalışan demo hazırlamak gerekiyor. Cycle time < 50ms, EtherCAT yok.
- **Karar:** CODESYS Control Win SL
- **Gerekçe:** Geliştirici kendi PC'sinde birkaç dakikada çalışır. Gerçek zamanlı performans bu aşamada kriter değil.

**Senaryo 1B — Üretim Ortamı, Standart Makine:**
Konveyör + dolum sistemi. 10ms scan cycle, PROFINET, ARM tabanlı IPC.
- **Karar:** CODESYS Control Linux SL + PREEMPT_RT kernel
- **Gerekçe:** Linux OS lisansı yok, ARM desteği olgun, PREEMPT_RT + isolcpus ile jitter < 40µs elde edilebilir (bkz. `hardware/industrial-pc/_synthesis.md` — Proje Notu 1: 10ms döngü, jitter 18µs hedef).

**Senaryo 1C — Motion Kontrol, Windows Ekip:**
Servo kontrollü paketleme makinesi. Mühendislik ekibi Windows uzmanı, Active Directory entegrasyonu isteniyor, Beckhoff X86 IPC kullanılacak.
- **Karar:** CODESYS Control RTE SL (Windows + RTSS)
- **Gerekçe:** Ekip Windows biliyor, AD entegrasyonu Windows gerektirir, RTSS kernel Windows üzerinde hard-RT sağlar.

**Senaryo 1D — SIL 2 Gerektiren Güvenlik Sistemi:**
Pres makinesi, operatör güvenliği, SIL 2 gereksinimi.
- **Karar:** Sertifikalı donanım güvenlik PLC'si (örn. Pilz PNOZmulti, Phoenix Contact PSR)
- **Gerekçe:** Standart CODESYS SIL sertifikalı değildir. CODESYS Safety ayrı üründür. SIL 2/3 için sertifikalı dedicated safety PLC şarttır (bkz. `01_runtime_architecture.md` — Ne Zaman Tercih Edilmemeli).

---

### Karar 2 — Application Mimarisi (Tek vs Çoklu)

#### Karar Kriterleri Tablosu

| Kriter | Tek Application | Çok Application |
|---|---|---|
| **Karmaşıklık** | Düşük — tek deploy, tek proje | Yüksek — bağımsız lifecycle'lar |
| **Hata izolasyonu** | Düşük — bir bug tüm runtime'ı etkiler | Yüksek — her app bağımsız restart edilebilir |
| **Güncelleme esnekliği** | Düşük — tüm uygulama durdurulur | Yüksek — ana uygulama çalışırken diagnostik app güncellenebilir |
| **Kaynak paylaşımı** | Kolay — ortak GVL doğal | Zor — applicationlar arası iletişim mekanizması gerekir |
| **Bakım** | Kolay anlaşılır | Bağımlılık yönetimi gerekir |
| **Uygun kullanım** | Tek makine, tek sorumluluk | Üretim + diagnostik ayrımı; aşamalı devreye alma |

**Kaynak:** `knowledge/codesys/fundamentals/01_runtime_architecture.md` — Gerçek Proje Notu 4: "CODESYS V3'ün çok önemli özelliği: Tek runtime üzerinde birden fazla Application çalışabilir."

#### Trade-Off Analizi

Çok Application mimarisinin temel değeri **bağımsız yaşam döngüsüdür:** Üretim mantığı Application_Main, diagnostik ve test mantığı Application_Diag olarak deploy edilirse, Application_Diag güncellenirken Application_Main hiç durmaz. Bu, üretim hattı durmadan yazılım güncellemesine olanak tanır.

Dezavantaj: Applicationlar arasında veri paylaşımı GVL ile doğal değildir; gerçek zamanlı segmentler arasında paylaşım mekanizması (Modbus, OPC UA veya shared memory) tasarlanmalıdır.

#### Senaryo → Karar Örnekleri

**Senaryo 2A — Basit Makine Kontrolü:**
Tek konveyör, tek operatör istasyonu, offline güncellemeler kabul edilebilir.
- **Karar:** Tek Application
- **Gerekçe:** İlave karmaşıklık değmez. Güncellemeler için planlı bakım penceresi yeterli.

**Senaryo 2B — Sürekli Üretim Hattı + Uzaktan Diagnostik:**
7/24 çalışan üretim hattı. Üretimi durdurmadan diagnostik yazılımı güncellenecek, test senaryoları eklenecek.
- **Karar:** Çok Application (Application_Production + Application_Diagnostics)
- **Gerekçe:** Üretim uygulaması güncellenmeden diagnostik uygulaması serbest bırakılabilir. Gerçek proje deneyimine dayanmaktadır (bkz. `01_runtime_architecture.md` — Proje Notu 4).

---

### Karar 3 — Task Mimarisi

#### Karar Kriterleri: Task Sayısı ve Tipleri

**Adım 1: Uygulamanın bileşenlerini listele.**
**Adım 2: Her bileşen için zamanlama gereksinimini belirle.**
**Adım 3: Benzer zamanlamayı grupla — farklı zamanlamayı ayır.**
**Adım 4: Her gruba tip ve öncelik ata.**
**Adım 5: CPU yük toplamı %70 altında mı kontrol et.**

**Kaynak:** `knowledge/codesys/task-structure/_synthesis.md` — Tasarım Süreci: 5 Adım.

#### Hazır Şablon Tablosu: Proje Türüne Göre Başlangıç Mimarileri

| Şablon | Task | Tip | Cycle | Öncelik | Sorumluluk |
|---|---|---|---|---|---|
| **A — Basit Makine** | Task_Safety | Cyclic | 5ms | 0 | E-stop, güvenlik kontakları |
| | Task_Control | Cyclic | 10ms | 2 | Ana mantık, sensör, aktüatör |
| | Task_Slow | Cyclic | 100ms | 5 | HMI, OPC UA |
| | Task_Log | Freewheeling | — | 15 | Diagnostik, log |
| **B — Motion Dahil** | Task_Safety | Cyclic | 2ms | 0 | E-stop (EtherCAT sync) |
| | Task_Motion | Cyclic | 2ms | 1 | EtherCAT sync, SoftMotion |
| | Task_Control | Cyclic | 10ms | 2 | Koordinasyon, PID, recipe |
| | Task_HMI | Cyclic | 50ms | 5 | HMI, OPC UA |
| | Task_Log | Freewheeling | — | 15 | Log, diagnostik |
| **C — Proses Kontrol** | Task_Safety | Cyclic | 5ms | 0 | Güvenlik |
| | Task_FastPID | Cyclic | 10ms | 1 | Hızlı döngü PID (basınç, akış) |
| | Task_SlowPID | Cyclic | 100ms | 2 | Yavaş döngü PID (sıcaklık, seviye) |
| | Task_Sequence | Cyclic | 20ms | 3 | Sekans, recipe |
| | Task_HMI | Cyclic | 200ms | 5 | HMI |
| | Task_Log | Freewheeling | — | 15 | Log |

**Kaynak:** `knowledge/codesys/task-structure/_synthesis.md` — Hazır Şablon: Proje Türüne Göre Başlangıç Mimarileri.

#### Kritik Task Tasarım Kuralları

| Kural | Açıklama | Kaynak |
|---|---|---|
| **Güvenlik = Prio:0** | E-stop ve güvenlik izleme her zaman en yüksek öncelik | task-structure/_synthesis.md |
| **PID mutlaka Cyclic'te** | Freewheeling cycle time tutarsız; PID integral/türev hatalı hesaplanır | task-structure/_synthesis.md |
| **Fieldbus cycle time = Task cycle time** | EtherCAT 2ms ise Task da 2ms; uyumsuzluk drive titremeye yol açar | task-structure/_synthesis.md |
| **Dosya/ağ işlemi = Freewheeling** | Blocking çağrılar Cyclic task'ı dondurur | task-structure/_synthesis.md |
| **CPU yükü < %70** | Exec Time / Cycle Time oranı. %80 üzeri watchdog riski | 01_runtime_architecture.md |
| **Event task = yalnızca nadir olay** | Yüksek frekanslı sinyaller için Event task HALT'a yol açar; R_TRIG + Cyclic kullan | task-structure/_synthesis.md |

#### Senaryo → Karar Örnekleri

**Senaryo 3A — 4 Nozullu Şişe Dolum Makinesi:**
Konveyör (Modbus RTU), 4 solenoid vana, 4 kütüphane ölçer, operator paneli, recipe, USB log.

| Bileşen | Zamanlama Gereksinimi | Task Kararı |
|---|---|---|
| E-stop, kapı kilidi | < 10ms | Task_Safety: Cyclic 5ms Prio:0 |
| Solenoid vana, ölçer okuma | 10ms hassasiyet | Task_Control: Cyclic 10ms Prio:2 |
| Panel ışıkları | 50ms yeterli | Task_HMI: Cyclic 50ms Prio:5 |
| Reçete yükleme | Anlık, nadir | Task_Recipe: Event Prio:3 |
| USB log | 5 saniye yeterli | Task_Log: Freewheeling Prio:15 |

- **Tahmini CPU yük:** %21 (orta sınıf ARM) — güvenli margin.
- **Kaynak:** `task-structure/_synthesis.md` — Örnek 1: Şişe Dolum Makinesi.

**Senaryo 3B — EtherCAT Servo Eklenince Task Mimarisi Değişimi:**
Başlangıçta Modbus TCP tabanlı proje, sonradan servo eklendiğinde:
- **Eski:** Task_Control: Cyclic 10ms Prio:2 (tüm mantık)
- **Yeni:** Task_Motion ekle: Cyclic 2ms Prio:1 (EtherCAT sync); Task_Safety 10ms → 2ms'e taşı.
- **Öğrenim:** Başlangıçtan "fieldbus eklenirse ne olur?" sorusu sorulmalı (bkz. `task-structure/_synthesis.md` — Sentez Notu 3).

---

### Karar 4 — Merkezi vs Dağıtık Kontrol

#### Karar Kriterleri Tablosu

| Kriter | Merkezi Kontrol | Dağıtık Kontrol |
|---|---|---|
| **Fiziksel yayılım** | Küçük/tek alan | Büyük tesis, uzak alan grupları |
| **Bağlantı sürekliliği** | Kritik değil | Ağ kesintisine dayanıklılık gerekli |
| **Koordinasyon karmaşıklığı** | Düşük — tek kontrol mantığı | Yüksek — koordinasyon protokolü gerekir |
| **Yedeklilik** | IPC yedeklemesi zor | Her alan bağımsız çalışabilir |
| **Bakım** | Tek nokta, kolay | Birden fazla IPC yönetimi |
| **Gecikme hassasiyeti** | Düşük — fiziksel ağ hızlı | Yüksek — WAN gecikmesi kontrolü etkiler |
| **Ölçek** | Sınırlı (tek IPC kapasitesi) | Sınırsız — yeni alan = yeni IPC |

#### Trade-Off Analizi

Merkezi kontrol **basit** ve **anlaşılırdır** ancak tek arıza noktasıdır. IPC arızası veya ağ kesintisi tüm sistemi etkiler. Küçük tek alan tesisleri için genellikle doğru seçimdir.

Dağıtık kontrol her alanın kendi PLC/IPC'siyle **özerk çalışmasını** sağlar. Üst sistemden bağlantı kesilse bile alan operasyonuna devam eder. Büyük tesisler, birden fazla fabrika alanı veya WAN üzerinden bağlı süreçler için tercih edilir.

Ağ segmentasyonu (bkz. Karar 6) dağıtık mimarilerde daha kritik hale gelir: Her alan kendi VLAN/güvenlik zonasıyla izole edilmeli, koordinasyon trafiği ayrı bir VLAN üzerinden yönetilmelidir.

#### Senaryo → Karar Örnekleri

**Senaryo 4A — Tek Fabrika Hattı, 20 Sensör:**
Küçük ölçek, tek bina, sürekli ağ bağlantısı, tek operatör istasyonu.
- **Karar:** Merkezi — tek IPC + CODESYS SoftPLC
- **Gerekçe:** Karmaşıklık eklememek. Tek IPC yönetimi kolay, yedeklilik için ağ altyapısı (MRP) yeterli.

**Senaryo 4B — Çok Sahada Üretim (3 Fabrika):**
3 ayrı fabrikada üretim, merkezi MES, WAN üzerinden izleme. Her fabrika kendi proses döngüsünü bağımsız yönetiyor.
- **Karar:** Dağıtık — her fabrikada bağımsız IPC/PLC; merkezi historian ve SCADA.
- **Gerekçe:** WAN kesintisi lokal üretimi durdurmaz. Her fabrika kendi güvenlik zonasında çalışır. Merkezi koordinasyon OPC UA / MQTT üzerinden.

---

### Karar 5 — IPC Seçimi

#### Karar Kriterleri Tablosu

| Kriter | Raspberry Pi / SBC | Endüstriyel PC (x86) | Endüstriyel PC (ARM) | Vendor IPC (Beckhoff, WAGO) |
|---|---|---|---|---|
| **Maliyet** | < 100 USD | 500–3000 USD | 300–1500 USD | 800–5000+ USD |
| **Performans** | Orta (jitter: 39µs iyi optimize edilmiş) | Yüksek (< 20µs) | Orta-Yüksek | Çok yüksek (donanım optimize) |
| **Dayanıklılık** | Düşük (tüketici sınıfı) | Yüksek (geniş sıcaklık, vibrasyon) | Yüksek | Çok yüksek (IEC 61131 sertifika) |
| **Enerji tüketimi** | 5–15W | 30–100W | 10–30W | 10–50W |
| **Uzun vadeli temin** | Belirsiz | Orta (BOM değişimi) | Orta | Yüksek (10+ yıl garanti) |
| **Destek/garanti** | Yok | BT kanalı | Orta | OEM destek sözleşmesi |
| **EtherCAT/PROFINET** | Sınırlı | Tam (çift NIC) | Tam (bazıları) | Tam (dahili) |
| **Güvenlik sertifikası** | Yok | CE/UL | CE/UL | CE/UL/cULus |

**Kaynak:** `knowledge/hardware/industrial-pc/_synthesis.md` — Ne Zaman Linux SL, Ne Zaman Windows SL/RTE tablosu; `01_runtime_architecture.md` — Ne Zaman Tercih Edilmeli/Edilmemeli.

#### Donanım Ön Koşulları (SoftPLC için)

- **RAM:** En az 512MB, önerilen 2GB+ (runtime + uygulama + OS)
- **CPU:** En az 4 çekirdek (2 çekirdek izole + 2 çekirdek housekeeping — bkz. isolcpus)
- **NIC:** En az 2 adet (fieldbus trafiği IT trafiğinden fiziksel olarak ayrı)
- **Depolama:** SSD/eMMC (endüstriyel sınıf, geniş sıcaklık aralığı)
- **BIOS:** C-State kapatma, SpeedStep kapatma, SMT/HT kapatma desteği

**Kaynak:** `hardware/industrial-pc/_synthesis.md` — Hızlı Referans: Performans Parametreleri tablosu.

#### Senaryo → Karar Örnekleri

**Senaryo 5A — Eğitim / Prototipleme:**
Laboratuvar ortamı, maliyet kısıtlı, <50ms cycle time, EtherCAT yok.
- **Karar:** Raspberry Pi 4B + CODESYS Control for Raspberry Pi
- **Gerekçe:** Maliyet baskın kriter. Üretim performansı gerekmez. RT-preempt ile kabul edilebilir jitter (bkz. `01_runtime_architecture.md` — Proje Notu 1: 39µs).

**Senaryo 5B — Üretim Makinesi, EtherCAT, 7/24:**
Konveyör + servo, EtherCAT 2ms, 7 yıl operasyon beklentisi, DIN ray montaj.
- **Karar:** Endüstriyel PC (x86 veya ARM, fanless, geniş sıcaklık, çift NIC, SSD)
- **Gerekçe:** Uzun vadeli temin, endüstriyel dayanıklılık, çift NIC zorunluluğu (fieldbus + IT ayrımı), cyclictest < 20µs hedefi.

**Senaryo 5C — HMI + PLC Aynı Cihaz:**
Operatör paneli + kontrol mantığı aynı fiziksel cihazda (all-in-one panel PC).
- **Karar:** Windows RTE SL veya Windows Win SL (HMI aynı cihazda Windows gerektirir)
- **Gerekçe:** TwinCAT HMI, WinCC, Ignition (yerel) Windows gerektirir. `hardware/industrial-pc/_synthesis.md` — Ne Zaman tablosu: "HMI aynı IPC'de → Windows Win SL".

---

### Karar 6 — Ağ Topolojisi ve Segmentasyon

#### Topoloji Seçim Tablosu

| Topoloji | Ne Zaman | Avantaj | Dezavantaj |
|---|---|---|---|
| **Yıldız** | < 15 cihaz, kesinti toleransı yüksek | Kolay bakım, bağımsız port izolasyonu | Switch = tek arıza noktası |
| **Halka + MRP** | 15–50 cihaz, < 1 dk kesinti toleransı | Kablo kopmasına dayanıklı, < 200ms kurtarma | Düğüm sınırı: 50 |
| **PRP (ikili paralel)** | Sıfır çerçeve kaybı, SIS, kritik altyapı | ~0ms kayıp | 2× kablo, 2× switch maliyeti |
| **Hibrit (halka omurga + yıldız dal)** | Gerçek fabrika ortamı | Yedeklilik + ölçek + yönetim kolaylığı | Karmaşık konfigürasyon |

**Kaynak:** `knowledge/networking/_synthesis.md` — Topoloji Seçimi tablosu.

#### Purdue Segmentasyon Tablosu

| Katman | İçerik | VLAN | Hedef SL | Geçiş |
|---|---|---|---|---|
| **L5 Bulut** | ERP dışı, bulut | VLAN 10 | SL 2 | İnternet FW |
| **L4 Kurumsal IT** | ERP, e-posta, AD | VLAN 10 | SL 2 | FW-1 |
| **L3.5 iDMZ** | Jump server, historian kopyası | VLAN 20 | SL 2-3 | FW-2 |
| **L3 MES/SCADA** | Historian, SCADA sunucusu | VLAN 30 | SL 3 | FW-3 |
| **L2 Denetim** | HMI, mühendislik istasyonu | VLAN 40 | SL 3 | FW |
| **L1 Temel Kontrol** | PLC, RTU | VLAN 50 | SL 3 | — |
| **L0 Fiziksel** | Sensör, aktüatör | — | SL 2-3 | — |
| **SIS (izole)** | Güvenlik PLC'leri | VLAN 60 | SL 4 | Fiziksel izolasyon |

**Temel kural:** Komşu olmayan katmanlar arasında doğrudan iletişim yasaktır. L4 → L1 erişimi: FW-1 → iDMZ → FW-2 → FW-3 üzerinden geçmelidir.

**Kaynak:** `knowledge/networking/_synthesis.md` — Purdue Katmanları ve Segmentasyon tablosu; Gerçek Proje Notu 5 (iDMZ olmadan fidye yazılımı yayılımı).

#### Fieldbus Seçim Tablosu

| Senaryo | Fieldbus | Zamanlama |
|---|---|---|
| Standart I/O, basınç/sıcaklık | PROFINET RT | 250µs–10ms, ≤ 100µs jitter |
| Servo senkronizasyonu, çok eksen | PROFINET IRT | < 500µs, ≤ 1µs jitter |
| Robotik, koordineli hareket, < 100µs | EtherCAT | < 100µs, < 1µs jitter |
| Legacy, basit I/O | Modbus TCP | 50ms–1s (RT garantisi yok) |
| IT+OT aynı ağ, yeni tesis | TSN | < 1ms, determinizm |

**Kaynak:** `knowledge/networking/_synthesis.md` — Ne Zaman PROFINET RT, Ne Zaman IRT veya EtherCAT tablosu.

#### Senaryo → Karar Örnekleri

**Senaryo 6A — 20 Eksenli Baskı Makinesi:**
20 servo sürücü, PLC, 2 HMI, historian. Üretim kesintisi 1 dakika kabul edilemez.

- **Topoloji kararı:** Omurga halka MRP (2 core switch, fiber, < 200ms kurtarma); makine hücresi yıldız; servo zincirleri PROFINET IRT.
- **Segmentasyon kararı:** PLC hücresi VLAN 50 (SL 3); HMI VLAN 40 (SL 3); SCADA VLAN 30 (SL 3); iDMZ VLAN 20 (historian kopyası + yama).
- **Performans kararı:** PROFINET IRT 500µs, ≤ 1µs jitter. CoS 6 → Kuyruk 4 (Strict Priority). Switch: Conformance Class C, cut-through.
- **Kaynak:** `networking/_synthesis.md` — 20 Eksenli Baskı Makinesi Pratik Senaryo.

**Senaryo 6B — Küçük Makine Hücresi, IT Bağlantısı Yok:**
5 cihaz, tek PLC, Modbus TCP, üretim ağından izole.
- **Topoloji:** Yıldız (5 port managed switch)
- **Segmentasyon:** IT ağından fiziksel izolasyon; OPC UA portu (4840) yalnızca dahili subnet.
- **Fieldbus:** Modbus TCP (legacy sensörler)

---

### Karar 7 — HMI Yaklaşımı

#### HMI Teknoloji Seçim Tablosu

| Yaklaşım | Ne Zaman Seç | Avantaj | Dezavantaj |
|---|---|---|---|
| **Web HMI** (React/Vue + WebSocket) | Platform bağımsızlık, Git/CI-CD, özel UX, sıfır lisans | Her tarayıcıdan erişim, modern UX, versiyon kontrolü | Alarm/historian kendin yazarsın; WSS güvenlik altyapısı gerekir |
| **SCADA Platform** (Ignition, WinCC) | 100+ ekran, historian kritik, hızlı geliştirme | Alarm/historian dahili; tag bağlama hızlı | Yüksek lisans maliyeti, vendor bağımlılığı |
| **CODESYS WebVisu / TargetVisu** | CODESYS projesi, küçük panel, PLC ile aynı ortam | Sıfır ayrı backend, doğrudan değişken bağlama | Sınırlı UI esnekliği, büyük projede performans sınırı |
| **Panel HMI** (Siemens KTP, Weintek) | Makine başında sabit dokunmatik ekran | Dayanıklı, entegrasyon basit | Web erişimi yok, yazılım esnekliği kısıtlı |

**Kaynak:** `knowledge/hmi/_synthesis.md` — Tablo 1: HMI Teknoloji Seçimi.

#### HMI Protokol Seçimi

```
OPC UA subscription seç (standart tercih):
  ✓ Modern PLC (CODESYS, Siemens TIA, Beckhoff)
  ✓ Push modeli — polling yükü yok
  ✓ Veri kalitesi (GOOD/BAD/UNCERTAIN) önemli
  ✓ Güvenli bağlantı (sertifika tabanlı)

Modbus polling seç (yalnızca legacy):
  ✓ OPC UA sunucusu olmayan cihaz
  ✓ Basit int/float veri, struct gerekmez
  Zorunlu: Toplu okuma (max 125 register/istek) + değişim filtresi
```

**Kaynak:** `knowledge/hmi/_synthesis.md` — Ne Zaman OPC UA, Ne Zaman Modbus.

#### Kritik HMI Tasarım Kuralları (ISA-101 / ISA-18.2)

| Kural | Açıklama |
|---|---|
| Normal = nötr/gri | Renk yalnızca anomali için. Yeşil/kırmızı normal durumda alarm kör kılığı yaratır. |
| ≤ 3 tıklama | Dashboard'dan herhangi bir kritik kontrole maksimum 3 tıklama. |
| < 10 alarm / 10 dk | ISA-18.2 operatör başına alarm sınırı. Fazlası alarm körlüğüdür. |
| Acknowledge ≠ çözüldü | Alarm onayı "gördüm" demektir; koşul aktifse listede kalır. |
| Yetkilendirme iki katmanlı | Frontend UI gizleme + backend sessionToken doğrulaması; ikisi birlikte. |
| wss:// üretimde zorunlu | ws:// açık metin komut riski; Nginx SSL termination baştan planlanmalı. |

**Kaynak:** `knowledge/hmi/_synthesis.md` — Sık Yapılan Hatalar; Tablo 4: ISA-18.2 Alarm Öncelik Özeti.

#### Senaryo → Karar Örnekleri

**Senaryo 7A — Orta Ölçek Üretim, Git Tabanlı Geliştirme:**
20 tag, 5 ekran, 3 operatör, platform bağımsız erişim isteniyor.
- **Karar:** Web HMI (Vue 3 + Pinia, Node.js backend, OPC UA subscription)
- **Gerekçe:** Sıfır lisans, tarayıcıdan erişim, Git ile versiyon kontrolü. 20 tag için Vue 3 Pinia ekstra optimizasyon gerektirmez (200 tag / 50 güncelleme/s → CPU %18).

**Senaryo 7B — Büyük Tesis, 300 Ekran, Historian Kritik:**
Petrokimya tesisi, 300+ operatör ekranı, 5 yıllık üretim verisi arşivi, bakım SLA zorunlu.
- **Karar:** SCADA Platform (Ignition veya WinCC)
- **Gerekçe:** Dahili historian, alarm yönetimi, raporlama. Sıfırdan yazmak fizibil değil. Vendor SLA sözleşmesi kabul edilebilir.

**Senaryo 7C — Makine Başı Dokunmatik Panel:**
Tek makine, operatör makine başında çalışıyor, web erişimi gerekmez, CODESYS projesi.
- **Karar:** CODESYS TargetVisu (panel HMI)
- **Gerekçe:** Ayrı backend yok, doğrudan değişken bağlama, PLC ile aynı ortam. Küçük kapsam için WebVisu/TargetVisu fazlasıyla yeterli.

---

### Karar 8 — Edge vs Bulut

#### Karar Kriterleri Tablosu

| Kriter | Yerel / Edge | Hibrit | Tam Bulut |
|---|---|---|---|
| **Ağ bağımlılığı** | Hiç yok | Kısmi (bulut opsiyonel) | Tam bağımlı |
| **Gecikme hassasiyeti** | Düşük ms seviyesinde kritik kontrol | Kontrol yerel, analitik bulut | Yalnızca izleme/analitik |
| **Veri gizliliği** | Tam kontrol | Seçilen veriler buluta gider | Veri provayere gider |
| **Ölçeklenebilirlik** | IPC kapasitesiyle sınırlı | Bulut analitik ile esnek | Sınırsız |
| **Maliyet** | Başlangıç donanım | Karma | Düşük donanım, yüksek abonelik |
| **Bant genişliği** | Kritik değil | Seçici veri aktarımı | Yüksek bant genişliği gerekir |
| **Güvenlik** | OT ağı fiziksel izole | iDMZ üzerinden seçici | OT→internet açık bağlantı riski |

#### Trade-Off Analizi

Gerçek zamanlı kontrol (ms düzeyinde karar) **her zaman yerelde** olmalıdır: Bulut gecikmesi deterministik değildir, internet kesintisi kontrolü durduramaz. Bu kural tartışmasızdır.

Bulutun değeri **analitik ve izleme** katmanında ortaya çıkar: Çoklu tesis karşılaştırması, uzun dönem trend analizi, makine öğrenmesi tabanlı bakım tahmini. Bu işlevler gecikme toleranslıdır ve bulut ölçeğinden faydalanır.

Güvenlik kritik uyarı: OT ağından buluta doğrudan bağlantı, iDMZ olmadan kurulursa tüm Purdue segmentasyon modeli anlamsız hale gelir. MQTT veya OPC UA PubSub ile seçici veri aktarımı, daima iDMZ üzerinden yapılmalıdır (bkz. `networking/_synthesis.md` — Proje Notu 5: fidye yazılımı yayılımı).

#### Senaryo → Karar Örnekleri

**Senaryo 8A — Tek Makine, İnternet Bağlantısı Yok:**
Fabrika OT ağı internete açık değil, müşteri veri çıkmaz politikası.
- **Karar:** Tam yerel/edge — historian, alarm, raporlama yerel IPC veya yerel server.
- **Gerekçe:** Bağlantı kısıtı ve veri gizliliği. Uzaktan izleme VPN üzerinden yalnızca iDMZ jump server ile.

**Senaryo 8B — Çok Tesisli Firma, Merkezi Bakım İzleme:**
5 fabrika, her birinde bağımsız PLC. Merkezi bakım ekibi tüm tesisleri uzaktan izleyecek; bakım tahmini yapılacak.
- **Karar:** Hibrit — kontrol yerel, analitik MQTT/OPC UA PubSub → iDMZ → bulut.
- **Gerekçe:** Kontrol gecikme bağımsız çalışır. Seçilen KPI verileri (OEE, alarm sayısı, trend) buluta aktar. iDMZ güvenlik sınırını korur.

---

## Örnekler

Bu bölüm, yukarıdaki sekiz kararı bir araya getirerek somut proje senaryoları üretir.

### Örnek Senaryo A — Küçük Ölçekli Makine (Konveyör + Dolum)

**Gereksinimler:**
- 1 konveyör (frekans inverter, Modbus RTU)
- 4 solenoid vana
- 4 kütüphane ölçer (analog giriş)
- Operatör paneli (dokunmatik, 7 inç)
- 7/24 üretim, bütçe kısıtlı

**Mimari Kararlar:**

| Karar | Seçim | Gerekçe |
|---|---|---|
| PLC Platformu | CODESYS Linux SL (ARM IPC) | Maliyet, Linux ARM desteği olgun, <10ms cycle için jitter yeterli |
| Application | Tek Application | Proje küçük, ek karmaşıklık gereksiz |
| Task Mimarisi | Şablon A (4 task) | Safety 5ms/Prio:0, Control 10ms/Prio:2, HMI 50ms/Prio:5, Log FW/Prio:15 |
| Kontrol Mimarisi | Merkezi (tek IPC) | Tek alan, küçük ölçek |
| IPC | Fanless ARM IPC, çift NIC, eMMC | 7/24 dayanıklılık, maliyet dengesi |
| Ağ | Yıldız (5 port managed switch), IT izole | Küçük tesis, 5 cihaz |
| HMI | CODESYS TargetVisu (panel HMI) | CODESYS projesi, makine başı panel, ayrı backend gereksiz |
| Edge/Bulut | Tam yerel | İnternet bağlantısı yok, historian gereksiz |

---

### Örnek Senaryo B — Orta Ölçekli Motion Sistemi (EtherCAT Servo)

**Gereksinimler:**
- 6 EtherCAT servo ekseni
- 2ms senkronizasyon
- OPC UA SCADA bağlantısı
- Web HMI (3 operatör, farklı PC'lerden)
- 3 yıl operasyon garantisi

**Mimari Kararlar:**

| Karar | Seçim | Gerekçe |
|---|---|---|
| PLC Platformu | CODESYS Linux SL + PREEMPT_RT | EtherCAT 2ms, hard-RT gerekiyor; Linux SL + isolcpus ile <20µs jitter |
| Application | Tek Application + diagnostik app | Servo mantığı kritik, diagnostik ayrı app ile bağımsız güncellenebilir |
| Task Mimarisi | Şablon B (5 task) | Safety 2ms/Prio:0, Motion 2ms/Prio:1, Control 10ms/Prio:2, HMI 50ms/Prio:5, Log FW |
| Kontrol | Merkezi | 6 eksen tek IPC'de toplanabilir |
| IPC | x86 quad-core, çift NIC, SSD, PREEMPT_RT | Multicore izolasyon, EtherCAT + IT ayrımı, cyclictest <20µs |
| Ağ | Yıldız hücresi + MRP omurga | 15 cihaz, < 1 dk kesinti toleransı |
| HMI | Web HMI (Vue 3 + OPC UA backend) | 3 operatör farklı PC'den, Git ile versiyon kontrolü |
| Edge/Bulut | Yerel historian + seçici MQTT bulut | Trend verisi buluta, kontrol yerel |

**Kritik uyarı:** EtherCAT NIC IRQ'su yanlışlıkla izole çekirdeğe yönlendirilmemeli. EtherCAT NIC IRQ → housekeeping çekirdek (core 0-1); EtherCAT görev thread → izole çekirdek (core 2-3). Bu iki kavram karıştırıldığında sync kayıpları yaşanır (bkz. `hardware/industrial-pc/_synthesis.md` — Proje Notu 7).

---

### Örnek Senaryo C — Büyük Ölçek Proses Kontrol (Çok Alan)

**Gereksinimler:**
- 3 bağımsız proses hattı
- Çoklu PID döngüsü (sıcaklık, basınç, akış)
- SIL 2 güvenlik gereksinimi (bir hat)
- Merkezi SCADA + historian
- IT ağından izolasyon

**Mimari Kararlar:**

| Karar | Seçim | Gerekçe |
|---|---|---|
| PLC Platformu | 2× CODESYS Linux SL + 1× Sertifikalı Safety PLC | SIL 2 hattı için standart CODESYS yetersiz; safety PLC zorunlu |
| Application | Her hat için bağımsız Application | Hat 1 arızası diğerlerini etkilemez |
| Task Mimarisi | Şablon C (6 task) | FastPID 10ms, SlowPID 100ms, Sequence 20ms, HMI 200ms |
| Kontrol | Dağıtık (3 bağımsız IPC) | Her hat özerk çalışabilmeli |
| IPC | Endüstriyel x86, geniş sıcaklık, çift NIC | Proses ortamı dayanıklılık, 10 yıl temin garantisi |
| Ağ | Hibrit omurga MRP + yıldız dallar + VLAN segmentasyon | Büyük tesis, yedeklilik, IEC 62443 SL 3 hedefi |
| HMI | SCADA Platform (Ignition) | 100+ ekran, historian kritik, bakım SLA gerekli |
| Edge/Bulut | Yerel historian + iDMZ üzerinden merkezi izleme | Tesis politikası: veri yerel kalacak; üst yönetim izlemesi VPN |

---

## Sık Yapılan Hatalar

### Mimari Karar Hatalarının Sınıflandırması

**1. Geliştirme ortamını üretim ortamı zannetmek**

CODESYS Control Win SL üzerinde geliştirme yapılır, her şey çalışır. Gerçek donanımda (ARM, Linux RT) zamanlama, IRQ öncelikleri ve jitter farklı davranır. Windows Update bir gece sistemi yeniden başlatır ve makine hattı çöker.

Kural: Win SL yalnızca geliştirme ve test için. Üretim: Linux SL (PREEMPT_RT) veya Windows RTE SL.
**Kaynak:** `01_runtime_architecture.md` — Gerçek Proje Notu 2.

---

**2. Task mimarisini proje ortasında değiştirmek**

Tüm mantığı tek task'a koymak başlangıçta kolaydır. EtherCAT eklenmesi, yeni sensör grubu veya fieldbus değişikliği task mimarisini baştan yeniden tasarlamayı gerektirir. Devreye alma sırasında yapılan task değişikliği en az 2 gün ve beklenmedik üretim duruşu riski demektir.

Kural: Task mimarisi proje başında kağıt üzerinde tasarlanmalı; "fieldbus eklenirse ne olur?" sorusu baştan sorulmalıdır.
**Kaynak:** `task-structure/_synthesis.md` — Sentez Notu 2 ve 3.

---

**3. iDMZ olmadan IT/OT bağlantısı kurmak**

ERP sisteminden doğrudan PLC'ye erişim fidye yazılımı vektörüdür. Bkz. NotPetya sonrası vakalar. Bir üretim tesisinde muhasebe bilgisayarından yayılan fidye yazılımı SCADA'ya, oradan PLC'lere ulaştı; tesis 18 saat durdu.

Kural: ERP → FW-1 → iDMZ → FW-2 → SCADA → PLC. İki FW'nin maliyeti bir saatlik üretim kaybının çok altındadır.
**Kaynak:** `networking/_synthesis.md` — Gerçek Proje Notu 5.

---

**4. VLAN'ı tek başına güvenlik katmanı saymak**

"VLAN var, güvendeyiz" yanılgısı. Layer-3 güvenlik duvarı olmadan VLAN hopping ile atlatılır. Gerçek vaka: VLAN var görünüyordu, unmanaged switch kullanıldığı için güvenlik mimarisi görünmez biçimde geçersizdi.

Kural: Her VLAN sınırında Layer-3 güvenlik duvarı + varsayılan kural = engelle.
**Kaynak:** `networking/_synthesis.md` — Gerçek Proje Notu 1; Sık Yapılan Hatalar 4.

---

**5. SIL gereksinimini gözden kaçırmak**

Proje başında "güvenlik sistemi de var" denilip standart CODESYS SoftPLC ile SIL 2/3 hedeflenmesi. Standart CODESYS SIL sertifikalı değildir. Bu keşif proje ortasında yapılırsa mimari baştan yeniden tasarlanmalıdır.

Kural: Güvenlik gereksinimi (SIL) ilk toplantıda netleştirilmeli. SIL 1+: ayrı değerlendirme, SIL 2/3: sertifikalı safety PLC şart.
**Kaynak:** `01_runtime_architecture.md` — Ne Zaman Tercih Edilmemeli; `hardware/industrial-pc/_synthesis.md` — Ne Zaman tablosu.

---

**6. CPU pinleme yapmadan RT performansı beklemek**

Linux sistemde CODESYS kuruldu, cyclictest çalıştırıldı, max jitter 300ms. Runtime ve diğer OS thread'leri aynı çekirdeği paylaşıyor. isolcpus + IRQ yönlendirme + irqbalance kapatma yapılmadan gerçek zamanlı performans yoktur.

Kural: PREEMPT_RT tek başına yetmez. isolcpus, IRQ yönlendirme, irqbalance disable ve BIOS C-state kapatma birlikte uygulanmalıdır.
**Kaynak:** `01_runtime_architecture.md` — Gerçek Proje Notu 1; `hardware/industrial-pc/_synthesis.md` — Sık Yapılan Hatalar 7 ve 8.

---

**7. HMI'da bağlantı kopma senaryosunu planlamama**

Operatör ekranı 20 dakika önce bağlantısını kaybetmiş, eski değerleri göstermeye devam etmiş. Motor gerçekte 92°C'ye ulaşmıştı, ekran 68°C gösteriyordu. Motor hasar gördü.

Kural: Bağlantı kopunca görünür overlay (kırmızı banner + stale data gri/italik) + tüm yazma butonları disabled. Reconnect'te FULL_UPDATE zorunludur.
**Kaynak:** `hmi/_synthesis.md` — Sık Yapılan Hatalar 7 ve 8.

---

**8. Demo modda teslim**

Runtime lisans yüklenmeden devreye alındı. Fabrikada 2 saat sonra runtime durdu, üretim hattı çöktü.

Kural: Devreye alma kontrol listesinde "Lisans doğrulama" adımı zorunlu. IDE → License Manager → geçerlilik tarihi teyit edilmeli. Offline aktivasyon için .WibuCmRaC yedek dosyası önceden hazırlanmalı.
**Kaynak:** `hardware/industrial-pc/_synthesis.md` — Sık Yapılan Hatalar 2; `01_runtime_architecture.md` — Gerçek Proje Notu 3.

---

## Ne Zaman Tercih Edilmeli / Edilmemeli

Bu bölüm, sıkça sorulan "hangi durumda ne seç?" sorularını toplu olarak yanıtlar.

### SoftPLC Ne Zaman, Donanım PLC Ne Zaman?

| Tercih Et | Tercih Etme |
|---|---|
| Donanım bağımsızlığı gerekiyorsa | Mikrosaniye (<100µs) ASIC determinizm şartsa |
| Hızlı prototipleme (Win SL) | SIL 2/3 güvenlik sertifikasyonu gerekiyorsa |
| Büyük ekosistemin kütüphaneleri (500+ üretici) | RAM < 32MB, CPU < 100MHz (küçük gömülü) |
| Maliyet optimizasyonu gerekiyorsa | Uzun vadeli satıcı desteği tek belirleyici faktörse |
| Aynı kod birden fazla donanımda çalışacaksa | — |

### Linux SL Ne Zaman, Windows RTE Ne Zaman?

| Linux SL Seç | Windows RTE SL Seç |
|---|---|
| Yeni proje, maliyet odaklı (OS lisansı yok) | Mevcut Windows altyapısı, Active Directory |
| EtherCAT / PROFINET kritik (daha iyi jitter) | HMI aynı IPC'de (WinCC, TwinCAT HMI) |
| ARM tabanlı IPC | Ekip Windows biliyor, Linux eğitimi maliyetli |
| Uzun vadeli OS destek (Ubuntu LTS 5 yıl) | Windows + µs-düzey jitter kritikse |

### Ne Zaman Çok Application?

```
Çok Application seç:
  ✓ Üretimi durdurmadan diagnostik yazılımı güncellenecekse
  ✓ Farklı ekipler farklı uygulama modüllerini bağımsız yönetiyorsa
  ✓ Aşamalı devreye alma (önce ana uygulama, sonra ek modül) planlanıyorsa

Tek Application yeterli:
  ✓ Küçük proje, tek sorumluluk
  ✓ Güncellemeler için planlı bakım penceresi kabul edilebiliyorsa
  ✓ Applicationlar arası veri paylaşımı karmaşıklığından kaçınılmak isteniyorsa
```

---

## Gerçek Proje Notları

**Not 1 — Task Mimarisi Başında Tasarlanmazsa Devreye Alma Felaketi**

Bir makine projesinde tüm mantık tek 10ms task'ta yazıldı. EtherCAT servo eklenmesi gerekince task mimarisi devreye alma sırasında yeniden tasarlandı; POU'lar taşındı, watchdog ayarları değişti, öncelikler yeniden sıralandı. 2 gün ek iş, müşteri tesisinde 1 gün gecikme. Ders: "Başlangıçtan 10 dakika, devreye almada 2 gün" kuralı. Fieldbus gelecek mi? Baştan sor.

**Not 2 — IPC Ağ Arayüzü Değişince Fieldbus Kesildi**

Bir projede yeni NIC kartı eklenince arayüz ismi değişti (enp2s0 → enp3s0). CODESYSControl.cfg'deki Adapter.0.Name geçersiz kaldı ve fieldbus kesildi. Çözüm: netplan `match.macaddress + set-name` ile NIC'e kalıcı isim atamak. Ders: Donanım değişiminin yazılım yapılandırmasını bozmaması için MAC tabanlı arayüz isimlendirme şart.

**Not 3 — RT Throttling Sessiz Kilidi**

Bir motion uygulamasında IEC görevleri yük eşiğinde 5–10ms askıya alınıyordu; CODESYS log ve journalctl sessizdi. Sorun ancak `perf sched` incelemesinde tespit edildi: RT kota doluydu (`sched_rt_runtime_us` varsayılan 950000). `echo -1 > /proc/sys/kernel/sched_rt_runtime_us` ile düzeltildi. Ders: Sessiz askı, watchdog'dan daha tehlikelidir; devreye alma kontrol listesine RT throttling kontrolü eklenmeli.

**Not 4 — MRP Kurtarma Süresi, Watchdog ve Switch Firmware Üçlüsü**

Bir otomobil fabrikasında 32 düğümlü MRP halkasında watchdog zaman aşımları yaşandı. Belgede < 200ms garantisi vardı; ancak karışık üretici switch ortamında kurtarma süresi 350ms'e çıkıyordu. PLC watchdog 300ms ayarlıydı. Çözüm: Tüm halka switch'leri aynı üreticinin onaylı cihazlarına döndürüldü, watchdog 500ms'e ayarlandı. Ders: MRP kurtarma süresi, watchdog süresi ve switch firmware uyumluluğu birlikte planlanmalıdır.

**Not 5 — EtherCAT NIC IRQ Yanlış Çekirdeğe Yönlendi**

EtherCAT NIC IRQ'su yanlışlıkla izole çekirdeğe (core 3) yönlendirilince EtherCAT sync kayıpları yaşandı. Sorun: EtherCAT NIC IRQ'su housekeeping çekirdeğine (core 0-1) bırakılmalı; EtherCAT görev thread'i ise izole çekirdeğe (core 2-3) pinlenmeli. IRQ yönlendirme ve thread pinleme iki farklı kavramdır — karıştırılması kaynağı anlaşılmaz sync kayıplarına yol açar.

**Not 6 — Web HMI Bağlantı Kopma Senaryosu Geç Eklendi**

Bir projenin web HMI'ı bağlantı kopma durumunu ele almıyordu: OPC UA bağlantısı kesilince ekran eski değerleri göstermeye devam etti. Üretimde keşfedildi. Yazma butonları çalışmaya devam ediyordu; bir operatör bağlantı kopukken komut gönderdi. Çözüm: Reconnect FULL_UPDATE, kırmızı CONNECTION_STATUS banner, yazma butonları `disabled={!isConnected}`. Ders: Bağlantı kopma senaryosu ilk sprintten itibaren tasarlanmalı.

**Not 7 — SL Lisansla CPU Pinlemenin Sınırları**

4 çekirdekli sistemde SL lisansla taskset ile affinity denenince görünürde çalıştı; ancak periyodik jitter spike'ları devam etti. Multicore (MC) lisansıyla Task Groups ataması yapılınca RT görevi Core 3'e gerçekten kilitlendi, spike'lar tamamen ortadan kalktı. Ders: Performans kritik projelerde MC lisansı başlangıçtan itibaren bütçeye dahil edilmeli.

**Not 8 — Merkezi Mimariden Dağıtığa Geçişte Saat Senkronizasyonu Unutuldu**

Tek IPC'li merkezi bir tesise sonradan ikinci bir kontrolcü eklendi (dağıtık mimariye geçiş, Karar 4). İki IPC'nin sistem saatleri 4 saniye kaymıştı; historian'da iki hattan gelen olaylar yanlış sıralanıyor, alarm korelasyonu anlamsız hale geliyordu. NTP yapılandırılmamıştı çünkü tek IPC döneminde gerek yoktu. Çözüm: iDMZ'de bir PTP/NTP master kuruldu, tüm kontrolcüler ve SCADA aynı kaynağa senkronlandı. Ders: Dağıtık mimariye geçiş kararı (Karar 4) verildiği anda zaman senkronizasyonu mimarinin parçasıdır — sonradan eklenince geçmiş veri korelasyonu kurtarılamaz.

**Not 9 — Edge'den Buluta MQTT Köprüsü iDMZ'i Baypas Etti**

Hibrit edge/bulut kararı (Karar 8) verilen bir projede, devreye alma telaşıyla MQTT publisher doğrudan L1 kontrol VLAN'ından (VLAN 50) internete açıldı. Purdue segmentasyonu (Karar 6) kağıt üzerinde doğruydu ama tek bir outbound bağlantı tüm modeli delmişti. Bir güvenlik denetiminde "kontrol katmanından internete doğrudan oturum" bulgusu çıktı. Çözüm: MQTT publisher iDMZ'deki (VLAN 20) bir edge gateway'e taşındı; L1 yalnızca iDMZ ile OPC UA üzerinden konuşur, buluta çıkış iDMZ'den olur. Ders: Buluta giden tek bir bağlantı bile Purdue katmanlarına saygı göstermek zorundadır; "sadece outbound" mazereti segmentasyonu geçersiz kılmaz.

**Not 10 — Tek Application'da Online Change'in Gizli Maliyeti**

Tek Application mimarisi (Karar 2) seçilen 7/24 bir hatta küçük bir mantık düzeltmesi Online Change ile yapıldı. Online Change retain değişkenleri korur ama büyük bir POU'nun yeniden derlenmesi sırasında scan cycle bir kez uzadı ve motion task watchdog'a yakın bir tepe gördü. Çok Application olsaydı yalnızca ilgili app yeniden yüklenecek, motion application hiç etkilenmeyecekti. Ders: Tek Application + Online Change kombinasyonunda her değişiklik tüm runtime'ın derleme ve bellek yeniden düzenlemesini tetikler; kritik motion içeren hatlarda Çok Application ile mantığı izole etmek bu riski ortadan kaldırır.

---

## Edge Case'ler ve Sistem Limitleri

Mimari kararlar, sistem normal çalışırken değil sınır koşullarda test edildiğinde gerçek değerini gösterir. Aşağıdaki sınırlar karar verirken önceden bilinmeli — çünkü bunların çoğu devreye almadan önce görünmez.

### Platform ve Runtime Limitleri (Karar 1, 2, 3)

| Limit | Tipik Değer / Eşik | Karar Etkisi |
|---|---|---|
| **CPU yük tavanı** | %70 sürekli, %80 üzeri watchdog riski | Task mimarisi (③) tasarlanırken Exec/Cycle oranı margin'le hesaplanmalı |
| **Win SL jitter spike** | 50–100ms (Windows Update, AV, GPU sürücüsü) | Üretim için Win SL eler; geliştirme dışı kullanım yasak |
| **OPC UA MaxSessions** | Varsayılan 10 (CODESYS) | Web HMI tek backend bağlantısı kullanmalı; çoklu masaüstü istemci limiti aşar |
| **Çok Application sayısı** | Donanım/RAM bağımlı; pratikte 2–4 anlamlı | Her app ayrı task grupları ve bellek izolasyonu ister |
| **Retain bellek boyutu** | Hedef bağımlı (genelde KB seviyesi) | Online Change'te retain alanı taşarsa veriler sıfırlanır |
| **Event task frekansı** | Yüksek frekanslı olayda HALT riski | Nadir olaylar dışında R_TRIG + Cyclic kullan |

### Ağ ve Topoloji Sınır Koşulları (Karar 6)

- **MRP düğüm limiti:** 50 düğüm; aşılırsa kurtarma süresi garantisi (< 200ms) bozulur. Karışık üretici switch ortamında pratik kurtarma 350ms'e çıkabilir (bkz. Not 4) — watchdog buna göre ayarlanmalı.
- **PROFINET RT/IRT eş zamanlama sınırı:** Fieldbus cycle = task cycle olmalı; uyumsuzluk drive titremesine yol açar. EtherCAT 2ms ise IPC bu cycle'ı %70 margin'le karşılayabilmelidir.
- **VLAN ≠ güvenlik:** Layer-3 FW olmadan VLAN hopping ile aşılır. "VLAN var" güvenlik sınırı sayılmaz.
- **WAN gecikmesi:** Dağıtık kontrolde (Karar 4) koordinasyon trafiği WAN üzerindeyse deterministik değildir; gerçek zamanlı karar asla WAN'a bağlı olmamalı.

### Hata Senaryoları ve Davranış

```
SENARYO                          → SİSTEM DAVRANIŞI / KARAR ETKİSİ
─────────────────────────────────────────────────────────────────
Runtime lisansı süresi dolar     → 2 saat sonra runtime durur (demo mod), hat çöker
                                   → Devreye almada lisans doğrulama zorunlu adım
RT kota dolar (sched_rt_runtime) → IEC görevleri sessizce askıya alınır, log sessiz
                                   → Watchdog'dan tehlikeli; perf sched ile izlenmeli
EtherCAT NIC IRQ izole çekirdekte → Sync kaybı; IRQ housekeeping, thread izole çekirdek
İDMZ'siz IT/OT bağlantısı çöker  → Fidye yazılımı L4'ten L1'e yayılır (NotPetya örüntüsü)
HMI bağlantısı kopar             → Stale veri gösterimi; overlay + yazma disable zorunlu
Dağıtık kontrolcü saati kayar    → Historian olay sıralaması bozulur (bkz. Not 8)
```

**Kritik sınır kuralı:** Bir mimari karar, en kötü durum senaryosunda (worst case) hâlâ güvenli mi? Gerçek zamanlı kontrol her zaman yerelde olmalı (Karar 8), güvenlik her zaman Prio:0 ve mümkünse ayrı sertifikalı PLC'de olmalı (Karar 1), IT/OT geçişi her zaman iki FW + iDMZ üzerinden olmalı (Karar 6). Bu üç kural "edge case" değil, tasarımın değişmez aksiyomudur.

---

## Optimizasyon

Bu bir karar-rehberi belgesi olduğundan "optimizasyon" iki düzeyde anlam taşır: (1) karar **sürecinin** optimizasyonu — doğru kararı en az geri dönüşle vermek; (2) seçilen mimarinin maliyet/risk dengesini optimize etmek.

### Karar Sürecini Optimize Etmek

- **Kararları bağımlılık sırasına göre dondur.** Karar akış haritası (①→⑧) bir sıralama değil, bir bağımlılık grafiğidir. SoftPLC platformu (①) ve SIL gereksinimi en erken dondurulmalı çünkü bunlar geri alınması en pahalı kararlardır. HMI teknolojisi (⑦) en geç dondurulabilir — protokol katmanı (OPC UA subscription) sabitse HMI değiştirilebilir.
- **Geri dönüşü pahalı kararları öne al.** Maliyet sıralaması (en pahalıdan ucuza): SIL/safety mimarisi → fieldbus seçimi → task mimarisi → IPC donanımı → ağ topolojisi → HMI teknolojisi → edge/bulut bölüşümü. Erken yanlış SIL kararı tüm mimariyi yeniden yazdırır; geç HMI değişikliği yalnızca sunum katmanını etkiler.
- **"Fieldbus eklenirse ne olur?" sorusunu 0. günde sor.** Task mimarisini (③) baştan EtherCAT'e hazır tasarlamak 10 dakika; devreye almada yeniden tasarlamak 2 gün (Not 1). Bu, sürecin en yüksek ROI'li optimizasyonudur.

### Maliyet / Risk Trade-Off Matrisi

| Karar Eksenı | Düşük Maliyet Yönü | Düşük Risk Yönü | Optimizasyon İlkesi |
|---|---|---|---|
| Platform (①) | Linux SL (OS lisansı yok) | Donanım PLC / RTE SL | RT kritikliği ve ekip yetkinliğine göre dengele |
| Application (②) | Tek Application | Çok Application (izolasyon) | 7/24 + canlı güncelleme varsa Çok Application'ın bedeli değer |
| Kontrol (④) | Merkezi (tek IPC) | Dağıtık (özerk) | Fiziksel yayılım + WAN varsa dağıtık zorunlu |
| Topoloji (⑥) | Yıldız | PRP / Hibrit MRP | Kabul edilebilir kesinti süresi belirleyici |
| HMI (⑦) | Web HMI / WebVisu | SCADA (dahili historian) | Ekran sayısı + historian kritikliği eşiği |
| Edge/Bulut (⑧) | Tam bulut (düşük donanım) | Tam edge (bağımsız) | Gerçek zamanlı kontrol asla buluta bağlanmaz |

### En İyi Uygulama: Karar Kaydını Belgele

Her mimari karar için **gerekçe + reddedilen alternatif + geri dönüş maliyeti** üçlüsü yazılmalı (ADR — Architecture Decision Record yaklaşımı). Altı ay sonra projeye katılan mühendis "neden Linux SL değil de RTE SL?" sorusunu kararın kendisinden değil, kayıttan öğrenmeli. Belgelenmemiş karar, geri dönüşü en pahalı borçtur. CPU yük hedefi %70 ile sınırlandığında zaten %30 büyüme payı bırakılmış olur — bu, sonradan task ekleme maliyetini optimize eden tek en güçlü tek parametredir.

---

## Derin Teknik Detay

Bu bölüm, kararlardaki trade-off'ların **neden** var olduğunu mekanizma düzeyinde açıklar. Karar tablosu "ne seç" der; bu bölüm "neden böyle davranır" der.

### SoftPLC vs Donanım PLC: Determinizmin Gerçek Kaynağı

Donanım PLC'nin mikrosaniye determinizmi yazılımdan değil, **ayrık zamanlama donanımından** gelir: ASIC veya FPGA scan cycle'ı bir donanım sayacına bağlar, OS yoktur, kesme önceliği fiziksel olarak sabittir. SoftPLC'de ise scan cycle bir OS thread'idir ve determinizm tamamen **scheduler garantisine** bağlıdır. Linux PREEMPT_RT, çekirdek içindeki kesintisiz (non-preemptible) bölgeleri parçalayarak yüksek öncelikli RT thread'in herhangi bir anda CPU'yu kapabilmesini sağlar — ama bu yalnızca o thread izole bir çekirdekte (`isolcpus`) ve IRQ'lar başka çekirdeğe yönlendirilmişse işe yarar. İşte "donanım bağımsızlığı"nın gizli sınırı budur: IEC 61131-3 mantığı taşınabilir, ama determinizm garantisi donanım + OS + yapılandırma üçlüsünün eseridir ve taşınmaz.

### Tek vs Çok Application: Bellek ve Lifecycle İzolasyonu

CODESYS V3'te her Application kendi **bağımsız bellek alanına, kendi task setine ve kendi indirme/çalıştırma (download/boot) yaşam döngüsüne** sahiptir. Tek Application'da tüm POU'lar tek bir derleme ünitesidir; Online Change tüm sembol tablosunu ve bellek düzenini yeniden hesaplar (bkz. Not 10). Çok Application'da `Application_Diag` yeniden indirilirken `Application_Main`'in bellek alanına ve task'larına dokunulmaz — bu yüzden motion durmaz. Bedeli: GVL artık paylaşılan bellek değildir; applicationlar arası veri için açık bir kanal (shared memory, OPC UA, network variables) tasarlanmalıdır. Yani izolasyon "bedava" değildir; iletişim maliyetiyle satın alınır.

### OPC UA Subscription vs Modbus Polling: Push'un İç Mekanizması

Bu, HMI (⑦) ve protokol kararlarını birbirine bağlayan en kritik mekanizmadır. Modbus polling'de istemci her cycle'da tüm register bloğunu okur — PLC, verinin değişip değişmediğini bilmez, her istek tam round-trip maliyeti taşır. OPC UA subscription'da ise sunucu tarafında her MonitoredItem için bir **sampling interval** ve bir **deadband** tanımlıdır: sunucu değeri kendi içinde örnekler, yalnızca deadband'i aşan değişimi bir NotificationMessage'a koyar ve publishing interval'da gönderir. Yani ağ trafiği veri değişim hızıyla orantılıdır, polling frekansıyla değil. 200 tag'in saniyede yalnızca 5'i değişiyorsa, polling 200 değer/cycle taşır, subscription 5 değer taşır. CPU ve bant farkı buradan doğar — ve bu yüzden "polling her şeyi çözer" algısı yanlıştır (Çelişki kaydı).

### Purdue Segmentasyonu: Neden Komşu-Olmayan Katman Yasağı?

Purdue'nun "komşu olmayan katmanlar doğrudan konuşamaz" kuralı estetik değil, **saldırı yüzeyini matematiksel olarak küçültme** ilkesidir. L4'ten L1'e doğrudan yol varsa, L4'teki herhangi bir kompromize uç (ör. faturalama PC'si) L1 PLC'sine tek hop uzaklıktadır. Her zorunlu ara katman (iDMZ + iki FW) saldırganın yanal hareket için aşması gereken bir güvenlik sınırı ekler; iDMZ'deki jump server ve historian kopyası, gerçek kontrol katmanına asla doğrudan oturum açılmamasını sağlar. NotPetya örüntüsünde (Sık Yapılan Hatalar 3) tam olarak bu ara katmanların yokluğu, ofis ağındaki bir bulaşmanın SCADA ve PLC'ye yayılmasını sağladı. Modern tesislerde fiziksel Purdue yerine VLAN + L3 FW ile mantıksal Purdue uygulanır — ama yasağın kendisi değişmez (Çelişki kaydı).

### Edge vs Bulut: Determinizm Neden Yerelde Kalmak Zorunda?

Gerçek zamanlı kontrolün yerelde kalması bir tercih değil, **gecikme dağılımının doğası** gereğidir. Yerel fieldbus gecikmesi dar ve öngörülebilir bir dağılıma sahiptir (ör. EtherCAT < 100µs, jitter < 1µs). İnternet gecikmesi ise uzun kuyruklu (long-tail) bir dağılımdır: ortalama 30ms olabilir ama %99,9 persentil 2 saniye olabilir ve garanti edilemez. Kontrol döngüsü en kötü durum gecikmesine göre tasarlanmak zorundadır; long-tail dağılımda "en kötü durum" sınırsızdır. Bu yüzden bulut yalnızca gecikme-toleranslı katmanda (analitik, trend, ML tabanlı bakım tahmini) değer üretir — orada ortalama gecikme yeterlidir, worst-case önemsizdir. Aynı ayrım protokol seçiminde de geçerlidir: MQTT 4G üzerinde QoS + session ile bağlantısız çalışabildiği için telemetride kazanır, ama hiçbir zaman kontrol döngüsünü taşımaz.

---

## İlgili Konular

```
knowledge/decisions/
├── architecture/README.md         ← Şu an buradasınız (bu belge)
├── protocol-selection/            → OPC UA vs Modbus vs MQTT karar kaydı
└── hmi-technology/                → HMI teknoloji seçimi karar kaydı

Temel kaynak belgeler:
knowledge/codesys/
├── fundamentals/01_runtime_architecture.md  → SoftPLC varyantları, donanım bağımsızlığı
├── fundamentals/_synthesis.md              → CODESYS domain üst sentezi
└── task-structure/_synthesis.md            → Task tipleri, cycle time, öncelik şablonları

knowledge/hardware/
└── industrial-pc/_synthesis.md    → IPC seçimi, runtime kurulumu, performans tuning

knowledge/networking/
└── _synthesis.md                  → Purdue, topoloji, güvenlik, fieldbus seçimi

knowledge/hmi/
└── _synthesis.md                  → HMI teknoloji seçimi, ISA-101, ISA-18.2

Standartlar:
  IEC 61131-3     → PLC programlama dili standardı
  IEC 62443       → OT siber güvenlik — Zone/Conduit, SL seviyeleri
  IEC 61508       → Fonksiyonel güvenlik — SIL seviyeleri
  ISA-95          → Purdue ağ katmanı modeli
  ISA-101         → HMI tasarım standardı
  ISA-18.2        → Alarm yönetimi yaşam döngüsü
```
