---
KONU        : CODESYS Task Öncelik Yönetimi
KATEGORİ    : codesys
ALT_KATEGORI: task-structure
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_task_mapping_in_the_linux_system.html"
    başlık: "CODESYS Online Help — Mapping of Task Priorities on Linux"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Control/_rtsl_performance_optimization_linux.html"
    başlık: "CODESYS Control — Performance Optimization on Linux"
    güvenilirlik: resmi
  - url: "https://en.wikipedia.org/wiki/Priority_inversion"
    başlık: "Wikipedia — Priority Inversion"
    güvenilirlik: topluluk
  - url: "https://lapshinvr.com/articles/menedzher-zadach-codesys.html"
    başlık: "Task Manager CODESYS 3.5 — Cyclic/Priority Analizi"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/CODESYS-V2/thread/381978854b/"
    başlık: "CODESYS Forge — Task Configuration Tartışması"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_task_types.md"
    ilişki: gerektirir
  - konu: "02_cycle_time.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Task tipleri (01_task_types.md)"
  - "Cycle time kavramı (02_cycle_time.md)"
  - "Preemptive multitasking kavramı"
ÇELİŞKİLER :
  - kaynak: "CODESYS V2.3 vs V3.5 öncelik davranışı"
    konu: "V2'de substitutin, V3'te preemptive — farklı çalışma biçimleri"
    çözüm: >
      CODESYS V2.3'te yüksek öncelikli task tamamlanmadan diğeri başlamaz
      (cooperative/substituting). V3.5'te preemptive: yüksek öncelikli task,
      düşük öncelikli task'ı ORTASINDA keserek öne geçebilir. V2'den geçiş
      yapan projelerde bu fark beklenmedik davranışlara yol açabilir.
  - kaynak: "Linux scheduler etkileşimi"
    konu: "IEC task öncelikleri ile Linux thread öncelikleri arasındaki örtüşme"
    çözüm: >
      IEC Prio 0-3 → Linux SCHED_FIFO yüksek RT önceliği.
      IEC Prio 4-12 → Linux SCHED_FIFO orta RT önceliği.
      IEC Prio 13+ → Linux SCHED_OTHER (standart Linux scheduler).
      Standart network interrupt'ları Linux Prio 50'dedir (IEC Prio ~6 eşdeğeri).
      EtherCAT task'ı Prio ≤5 olmalı ki network interrupt'larının önüne geçsin.
---

## Özün Ne

CODESYS'te öncelik (priority), hangi task'ın CPU'yu önce kullanacağını belirler. 0 en yüksek, 31 en düşük önceliktir. Öncelik sistemi iyi yapılandırılmazsa yüksek öncelikli task düşük öncelikliyi aylarca çalıştırmayabilir (starvation), ya da iki task ortak veriyi aynı anda değiştirmeye çalışarak tutarsız durumlar yaratabilir (race condition). "Priority inversion" ise daha sinsi bir sorun: düşük öncelikli task, ortak kaynak tuttuğu için yüksek öncelikliyi bloke eder — teorik öncelik sırası pratikte tersine döner. Bu üç sorunu önlemek, sağlam bir task mimarisi kurmanın özüdür.

## Nasıl Çalışır

### Preemptive Scheduling — V3.5 Modeli

CODESYS V3.5, **preemptive** (kesici) çok görev modelini kullanır. Yüksek öncelikli bir task çalışmak istediğinde, o an çalışmakta olan düşük öncelikli task'ı **ortasında** keser ve CPU'yu devralır. Düşük öncelikli task, yüksek öncelikli tamamlanınca kaldığı yerden devam eder.

```
Zaman: →→→→→→→→→→→→→→→→→→→→→→→→→→→→→→
Prio 0 (1ms):  ██░░░░░░░░██░░░░░░░░██░░░
Prio 2 (10ms): ░░████░░░░░░████░░░░░░░░░
Prio 5 (50ms): ░░░░░░█████░░░░░░█████░░░

Prio 0 → Prio 2'yi keser
Prio 2 → Prio 5'i keser
Prio 5 → boşta CPU'yu kullanır
```

Bu modelin temel garantisi: **Daha yüksek öncelikli task her zaman daha düşük öncelikli task'tan önce çalışır.**

### Öncelik Sayısının Anlamı

```
IEC Öncelik: 0  1  2  3  4  5 ... 15 ... 31
              ↑                              ↑
          En yüksek                    En düşük
          (CPU'yu en çok alır)    (CPU ancak artan vakitte alır)
```

Sayı küçüldükçe öncelik artar. İki task aynı anda çalışmak istediğinde, numarası küçük olan kazanır.

### Linux'ta IEC Öncelik → Thread Öncelik Eşlemesi

```
IEC Priority | Linux Scheduling | Linux RT Priority | Açıklama
─────────────|──────────────────|───────────────────|──────────────────────────
0            | SCHED_FIFO       | 79                | Gerçek zamanlı, en yüksek
1            | SCHED_FIFO       | 78                |
2            | SCHED_FIFO       | 77                |
3            | SCHED_FIFO       | 76                |
4            | SCHED_FIFO       | 75                |
5            | SCHED_FIFO       | 74                |
...          | SCHED_FIFO       | ...               |
12           | SCHED_FIFO       | 67                | Linux network IRQ ~50'nin üstü
13           | SCHED_OTHER      | 0                 | ← Artık RT değil
14-31        | SCHED_OTHER      | 0                 | Standart Linux scheduler
```

**Kritik kural:** EtherCAT veya PROFINET gibi Ethernet tabanlı fieldbus task'ları, ağ sürücüsü interrupt'larından (Linux Prio ~50, IEC Prio ~6) **yüksek** öncelikte olmalıdır. Aksi halde fieldbus sync kaçırılır.

### Starvation (Açlık) Problemi

Yüksek öncelikli task çok sık çalışıyor ve CPU'nun büyük kısmını tüketiyorsa, düşük öncelikli task'lar hiç CPU alamaz — "aç" kalır.

```
Senaryo: Task_Safety (Prio:0, 1ms) her 1ms'de 0.9ms sürüyor.
  → CPU'nun %90'ı Prio:0'da.
  → Task_HMI (Prio:5, 50ms) her 50ms'de yalnızca 5ms CPU alabilir.
  → Task_Log (Freewheel, Prio:15) neredeyse hiç çalışamıyor.

Sonuç: HMI güncellenmesi çok yavaşlar, log hiç yazılmaz.

Çözüm: Task_Safety'nin exec time'ını düşür (kod optimizasyonu veya daha güçlü CPU).
        Ya da Task_Safety cycle time'ını artır (1ms yeterli mi, 2ms yetmez mi?).
```

### Race Condition (Yarış Durumu)

İki task aynı global değişkeni okuyor/yazıyorsa ve bir task diğerini ortasında kesebiliyorsa tutarsız veri oluşabilir.

```iecst
(* GVL'de *)
VAR_GLOBAL
    rSharedValue : REAL;
END_VAR

(* Task_Fast (Prio:0) — rSharedValue'yu güncelliyor *)
rSharedValue := SensorInput * 2.5 + Offset;
(* ← Bu satır ortasında Task_Slow başlarsa ne olur? *)

(* Task_Slow (Prio:5) — rSharedValue'yu kullanıyor *)
IF rSharedValue > Threshold THEN
    (* Yarım hesaplanmış değeri okuyor! *)
END_IF
```

REAL ve birden büyük boyutlu tip atamaları birden fazla instruction'a bölünebilir; preemption ortasında olursa yarım değer okunur.

**Çözüm yöntemleri:**

1. **Değişkeni yalnızca bir task'tan yaz, diğerinden oku** (en basit)
2. **Buffer yöntemi**: Her task kendi yerel kopyasıyla çalışır, paylaşım noktasını tek satırla günceller
3. **SysLibSem (Semaphore)**: CODESYS'in sunduğu mutex mekanizması — kritik bölgeyi kilitle
4. **CODESYS `__XADD` / `__XCHG` atomik fonksiyonları**: Atomik değişken güncellemesi

```iecst
(* Buffer yöntemi — en yaygın ve basit *)
(* Task_Fast: kendi yerel buffer'ını kullan *)
VAR
    rLocalValue : REAL;
END_VAR
rLocalValue := SensorInput * 2.5 + Offset;
rSharedValue := rLocalValue;  (* Tek satır atama — daha güvenli *)

(* Task_Slow: okuma sırasında preemption olsa bile
   en kötü ihtimalle bir önceki döngünün değerini okur — kabul edilebilir *)
```

### Priority Inversion (Öncelik Tersine Dönme)

En az anlaşılan ama en tehlikeli senaryo:

```
Aktörler:
  H = Yüksek öncelikli task (Prio:0)
  M = Orta öncelikli task   (Prio:5)
  L = Düşük öncelikli task  (Prio:15)
  R = Paylaşılan kaynak (mutex/semaphore)

1. L, R kaynağını kilitler ve işini yapmaya başlar.
2. H çalışmak ister, L'yi keser.
3. H, R kaynağına ihtiyaç duyar → R kilitli → bekler.
4. Beklerken M çalışmaya başlar (H bekliyor, M L'den yüksek öncelikli).
5. M, R'yi kullanmıyor ama L'yi önce bitirmesine izin vermiyor.
6. Sonuç: H (en yüksek), M (orta) tarafından DOLAYLI olarak bloke edilir.
   Öncelik sırası tersine döndü: L ve M, H'den önce çalışıyor.
```

**CODESYS'te öncelik tersine dönme riski:**
- `SysLibSem` (semaphore) ile korunan paylaşım noktaları
- Dış kütüphane çağrıları (C kütüphanesi, dosya sistemi)
- OPC UA server'ın paylaşılan veri erişimi

**Çözüm — Priority Inheritance:**
CODESYS'in kullandığı mutex implementasyonu priority inheritance desteği sunar; L kaynağı tutarken H bekliyorsa L'nin önceliği geçici olarak H'nin önceliğine yükseltilir. Ancak bu CODESYS'in kendi mutex mekanizmasına (`SysLibSem`) özgüdür; harici kaynak (dosya, ağ) tutulurken bekleme süresi minimize edilmelidir.

### Kaç Task Tanımlamak Mantıklı?

```
Çok az task (1-2):
  ✓ Basit, yönetimi kolay
  ✗ Her şey aynı cycle time → hız/verimlilik optimizasyonu yok
  ✗ Yavaş iş (log, komm.) hızlı işi etkiler

Çok fazla task (10+):
  ✓ Her görev kendi hızında çalışır
  ✗ Öncelik yönetimi karmaşıklaşır
  ✗ Context switch overhead artar
  ✗ Race condition riski artar

Pratik optimum: 3-6 task
```

**Kanıtlanmış 5 task mimarisi (çoğu makine için yeterli):**

| Task | Tip | Cycle | Öncelik | İçerik |
|---|---|---|---|---|
| Task_Safety | Cyclic | 1–5ms | 0 | E-stop, güvenlik izleme |
| Task_Fast | Cyclic | 1–2ms | 1 | Motion, EtherCAT (varsa) |
| Task_Control | Cyclic | 10ms | 2 | Ana kontrol mantığı, PID |
| Task_Slow | Cyclic | 50–100ms | 5 | HMI, yavaş sensörler |
| Task_Background | Freewheeling | — | 15 | Log, diagnostik, komm. |

## Pratikte Nasıl Kullanılır

### Öncelik Tasarım Adımları

**Adım 1: Kritiklik Sırasına Koy**
```
Ne olursa olsun çalışmalı → En yüksek öncelik (0-2)
Kontrol için gerekli      → Yüksek öncelik    (3-5)
İzleme ve HMI            → Orta öncelik      (6-10)
Arkaplan                 → Düşük öncelik     (11-15)
```

**Adım 2: Cycle Time ile Birlikte Değerlendir**
```
Öncelik ve cycle time birbirini etkiler:
  Eğer Task_A (Prio:0, 1ms) CPU'nun %90'ını alıyorsa
  Task_B (Prio:2, 10ms) teorik önceliği yüksek olsa da CPU kıtlığı yaşar.
  
  Kural: Düşük cycle time + yüksek öncelik kombinasyonu CPU'yu tüketir.
         Her task'ın exec/cycle oranı ≤ %70 olmalı.
```

**Adım 3: Paylaşılan Veriyi Haritalandır**
```
Task'lar arası paylaşılan GVL değişkenlerini listele:
  Kim yazar? → Tercihen tek task
  Kim okur?  → Birden fazla task okuyabilir (read-only güvenli)
  Her iki task da yazıyorsa → Mutex veya buffer mimarisi uygula
```

**Adım 4: Fieldbus Önceliğini Doğru Ayarla**
```
Linux'ta EtherCAT task:
  IEC Prio ≤ 5 olmalı (SCHED_FIFO, Linux RT ≥74)
  Ağ interrupt Linux Prio ~50 (IEC Prio ~6 eşdeğeri)
  Task fieldbus interrupt'tan yüksekte olmalı ki sync kaçırmaz.

Hatalı yapılandırma:
  EtherCAT task Prio:10 → Linux SCHED_FIFO 69
  Network IRQ Linux SCHED_FIFO 70 → IRQ task'ı geçer → sync kaçırılır
```

### Task Monitor ile Öncelik Doğrulama

Online modda Task Monitor, task'ların gerçek çalışma zamanlarını gösterir:

```
Task Configuration → Online → Monitor sekmesi

Sağlıklı öncelik sıralaması:
  Task_Safety (Prio:0, 1ms) : Jitter ±0.05ms  → ✓ Mükemmel
  Task_Motion (Prio:1, 2ms) : Jitter ±0.12ms  → ✓ İyi
  Task_Control(Prio:2,10ms) : Jitter ±0.40ms  → ✓ Normal
  Task_HMI    (Prio:5,50ms) : Jitter ±2.00ms  → ✓ Kabul edilebilir
  Task_Log    (Freewh p:15) : Düzensiz         → ✓ Beklenen

Starvation belirtisi:
  Task_HMI    (Prio:5,50ms) : Jitter ±15.0ms → ⚠ CPU kıtlığı var
```

## Örnekler

### Örnek 1: Tipik Makine Öncelik Hiyerarşisi

```iecst
(* Task Configuration — 5 task'lı standart mimari *)

(* Task 1: Güvenlik — her zaman en yüksek *)
Task_Safety:
    Type     : Cyclic
    Interval : t#5ms
    Priority : 0
    Watchdog : t#25ms, Sensitivity: 3
    Calls    : PRG_EmergencyStop, PRG_SafetyGates

(* Task 2: Ana kontrol *)
Task_Control:
    Type     : Cyclic
    Interval : t#10ms
    Priority : 2
    Watchdog : t#50ms, Sensitivity: 3
    Calls    : PRG_ConveyorControl, PRG_TemperatureCtrl, PRG_AlarmMgmt

(* Task 3: HMI güncelleme *)
Task_HMI:
    Type     : Cyclic
    Interval : t#100ms
    Priority : 5
    Watchdog : t#500ms, Sensitivity: 3
    Calls    : PRG_HMIUpdate, PRG_OPCUAWrite

(* Task 4: Arkaplan *)
Task_Background:
    Type     : Freewheeling
    Priority : 15
    Watchdog : t#5000ms, Sensitivity: 1
    Calls    : PRG_DataLogger, PRG_Diagnostics

(* Task 5: Reçete yükleme — olay tabanlı *)
Task_Recipe:
    Type     : Event (triggered by GVL_Cmds.xLoadRecipe)
    Priority : 3
    Calls    : PRG_LoadRecipe
```

### Örnek 2: Race Condition'ı Buffer ile Çözmek

```iecst
(* Senaryo: Task_Control (10ms) sıcaklık PID çıkışını hesaplıyor.
   Task_HMI (100ms) bu değeri OPC UA'ya yazıyor.
   Problem: Task_HMI okurken Task_Control yazabilir. *)

(* GVL_Control — Yalnızca Task_Control yazar *)
VAR_GLOBAL
    rPID_Output_Internal : REAL;   (* Task_Control'e özel *)
END_VAR

(* GVL_HMI — Task_Control yazdıktan sonra Task_HMI okur *)
VAR_GLOBAL
    rPID_Output_HMI : REAL;        (* Task_HMI'a özel, senkronize kopyası *)
END_VAR

(* Task_Control içinde (PRG_TemperatureCtrl'nin sonunda) *)
fbPID(...);
rPID_Output_Internal := fbPID.fOut;
GVL_HMI.rPID_Output_HMI := rPID_Output_Internal;  (* Tek satır atama — atomik *)

(* Task_HMI içinde *)
OPC_Write(value := GVL_HMI.rPID_Output_HMI);  (* Her zaman tutarlı değeri okur *)
```

### Örnek 3: Priority Inversion'ı Önlemek

```iecst
(* ❌ Riskli: Uzun süren işlemi Semaphore içinde yapmak *)
PROGRAM PRG_DataSharing_Bad
VAR
    hSem : RTS_IEC_HANDLE;
END_VAR

SysLibSemEnter(hSem);
    (* Uzun I/O işlemi burada — semaphore tutuluyor *)
    WriteToUSB(largeDataBuffer);    (* Bloke olabilir! *)
SysLibSemLeave(hSem);

(* ✅ Doğru: Kritik bölgeyi minimuma indir *)
PROGRAM PRG_DataSharing_Good
VAR
    hSem         : RTS_IEC_HANDLE;
    localSnapshot: ST_DataRecord;   (* Yerel kopya *)
END_VAR

(* Sadece kopyalama işlemi semaphore altında *)
SysLibSemEnter(hSem);
    localSnapshot := sharedData;    (* Hızlı kopya — µs mertebesinde *)
SysLibSemLeave(hSem);

(* Uzun işlem semaphore dışında *)
WriteToUSB(localSnapshot);          (* Artık semaphore tutulmuyor *)
```

### Örnek 4: Linux'ta Öncelik Doğrulama

CODESYS IDE → Device → PLC Shell:

```bash
> irq-list
IRQ  PRIORITY  DESCRIPTION
1    50        Network (eth0)
2    50        Network (eth1 — EtherCAT)
3    60        USB

> irq-set-prio 2 80
# EtherCAT network IRQ'sunu Linux Prio 80'e çek
# (IEC Task_EtherCAT Prio:0 → Linux 79'da, IRQ artık 80 → IRQ task'ı geçmez)
```

## Sık Yapılan Hatalar

### Hata 1: Tüm Task'lara Aynı Öncelik Vermek

```
❌ Yanlış:
  Task_Safety:  Priority 1
  Task_Control: Priority 1
  Task_HMI:     Priority 1
  
  Sorun: Aynı öncelikte task'lar sırayla (round-robin) çalışır.
         Güvenlik task'ı HMI task'ından önce gelmesi garanti edilemez.

✅ Doğru: Her task, gerçek önem sırasına göre farklı öncelik alır.
```

### Hata 2: Yüksek Öncelikli Task'a Yavaş İş Vermek

```
❌ Yanlış: Task_Safety (Prio:0, 5ms) içinde USB log yazma

  Neden  : USB yazma bloke olabilir → Task_Safety bloklıyor
           → Alt öncelikli task'lar da bloke → tüm sistem donuyor
  
✅ Doğru: Task_Safety sadece e-stop ve güvenlik kontakları.
          Byte başına max exec time hesaplanmış, watchdog buna göre.
```

### Hata 3: Öncelik Boşluğu Bırakmamak

```
❌ Yanlış: Prio 0, 1, 2, 3, 4, 5 kullanmak (bitişik)
  Sorun: Yeni task eklemek gerektiğinde aralara sıkıştırma yapılamaz.

✅ Doğru: Prio 0, 2, 5, 10, 15 (boşluklu)
  Yeni task eklenince: Prio 0 ile 2 arası → Prio 1 kullanılabilir.
```

### Hata 4: V2 Alışkanlığını V3'e Taşımak

```
V2.3'te substituting model:
  Aynı öncelikte task'lar biri bitince diğeri başlar.
  Düşük öncelikli task yüksek öncelikliyi kesmez.

V3.5'te preemptive model:
  Yüksek öncelikli task ORTASINDA kesebilir.
  V2'den copy-paste yapılmış global değişken paylaşımları
  V3'te race condition yaratabilir!

Kontrol: V2'den taşınan projelerde paylaşılan değişkenleri gözden geçir.
```

### Hata 5: Fieldbus Task Önceliğini Çok Düşük Ayarlamak

```
Senaryo: EtherCAT task Prio:10 (Linux SCHED_FIFO 69)
         Network IRQ Linux 70 → IRQ task'tan yüksek!

Sonuç  : EtherCAT sync kaçırılıyor → drive'lar düzensiz hareket
Çözüm  : EtherCAT task Prio ≤ 5 olmalı (Linux SCHED_FIFO ≥74)
         IRQ önceliği de düşürülmeli: irq-set-prio <irq_no> 65
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Öncelik Aralıkları İçin Kullanım Kılavuzu

**Prio 0:** Yalnızca e-stop ve fiziksel güvenlik izleme. Başka hiçbir şey buraya girmemeli.

**Prio 1-3:** Motion control (EtherCAT, PROFINET RT sync). Fieldbus task'ları bu aralıkta olmalı.

**Prio 4-6:** Ana kontrol mantığı (PID, makine sekansı, alarm yönetimi).

**Prio 7-12:** İzleme, loglama altyapısı, yavaş sensör okuma.

**Prio 13-15:** HMI güncelleme, OPC UA write, ağ iletişimi (gerçek zamanlı garantisi gereksiz).

**Prio 16+:** Freewheeling task'lar, diagnostik, batch log yazma.

**Prio 0 ile 1 arasına task ekleme:** Mümkün değil — 0 ve 1 bitişik. Başlangıçtan Prio 0 ve 3 bırakmak, ara eklemeler için yer açar.

## Gerçek Proje Notları

**Not 1 — Starvation'ın Sinsi Belirtisi**  
Bir paketleme makinesinde OPC UA server bağlantısı günde 2-3 kez kopuyordu. CODESYS Monitor incelenince Task_HMI'ın jitter değeri ±20ms'ye çıktığı görüldü. Neden: Task_Control (Prio:2, 10ms) exec time'ı beklenenden uzundu, Task_HMI (Prio:5, 50ms) yeterince CPU alamıyordu. Task_Control'deki dosya yazma kodu Freewheeling task'a taşındı; Task_HMI jitter ±1.5ms'ye indi, OPC UA kopması durdu.

**Not 2 — Race Condition Üretim Ortamında**  
Bir dolum makinesinde, üretim sayaçlarının zaman zaman sıfırlandığı rapor edildi. Araştırma: Task_Control (10ms) ve Task_HMI (100ms) aynı `dwProductionCount` DWORD'unu farklı noktalardan yazıyordu. Preemption ortasında yarım değer okunuyordu. Çözüm: Yalnızca Task_Control yazar, Task_HMI yalnızca okur. DWORD ataması tek satıra indirildi.

**Not 3 — Öncelik Boşluğunun Değeri**  
İlk projede 0, 1, 2, 3, 4, 5 öncelikleri kullanıldı. 6 ay sonra müşteri EtherCAT eklendiğini söyledi. EtherCAT task Prio:0 olmalıydı, ama Prio:0 güvenlik task'ında kullanılıyordu. Tüm task öncelikleri yeniden numaralandırıldı — her task'a touch. İkinci projeden itibaren 0, 3, 6, 10, 15 şeması benimsendi.

**Not 4 — Priority Inversion'ı Defalarca Yaşayan Proje**  
Bir test sistemi projesinde SysLibSem ile korunan bir buffer'a Task_Fast (Prio:1) ve Task_IO (Prio:10) yazıyordu. Task_IO bazen büyük veri bloğunu semaphore altında yazıyordu. Task_Fast semaphore beklerken Task_Comm (Prio:5) önüne geçiyor, Task_IO'nun tamamlanmasını geciktiriyordu. Gerçek zamanlı test ölçümleri tutarsız sonuçlar vermeye başladı. Çözüm: Semaphore altındaki kritik bölge minimuma indirildi, sadece buffer pointer swap'ı korundu.

**Not 5 — "Prio 0 Her Şeye" Antikalibi**  
Deneyimsiz bir yapılandırmada tüm task'lar Prio:0'a ayarlanmıştı. Scheduler round-robin çalıştırdı, HMI task'ı güvenlik task'ıyla aynı öncelikte yarışıyordu. Sonuç: E-stop tepki süresi tutarsız, bazen 50ms buluyordu. Mimari sıfırdan tasarlandı; 5 farklı öncelik seviyesi tanımlandı.

**Not 6 — IEC Prio 0 ≠ Linux Prio 99 (RT Throttling Tuzağı)**  
Bir geliştirici "en yüksek öncelik" için Prio:0 verdi ve task'ın asla kesilmemesini bekledi. Ama task ara sıra mikro-gecikmeler yaşadı. Neden: IEC Prio:0 → Linux RT ~79, oysa Linux'un kendi RT throttling mekanizması (`/proc/sys/kernel/sched_rt_runtime_us`, varsayılan 950000/1000000) RT thread'lerin CPU'nun **%95'inden fazlasını** sürekli almasını engeller — kalan %5'i normal task'lara ayırır. Bir IEC task gerçekten %95+ CPU isterse, kernel onu periyodik olarak "throttle" eder. Ders: Hard-RT izolasyon için RT throttling'i bilinçli yönetin (izole çekirdekte kapatılabilir); "Prio:0 = mutlak hâkimiyet" yanlıştır, kernel araya girer.

**Not 7 — Aynı Öncelikte İki Task: Tanımsız Sıra**  
İki task aynı Prio:2'deydi; geliştirici A'nın hep B'den önce çalışacağını varsaydı (proje ağacındaki sıraya göre). Bir CODESYS sürüm güncellemesinden sonra sıra değişti, A'nın hazırladığı veriyi B önce okudu → bir scan gecikme. Ders: İki task arasında sıra bağımlılığı varsa **farklı öncelik** verin; aynı öncelikte sıra garanti değildir ve sürümler arası değişebilir. Sıra önemliyse onu kodla (tek task içinde sıralı çağrı) zorla.

**Not 8 — Multicore'da Önceliğin Anlamı Değişir**  
Tek çekirdekte Prio:0 task, Prio:5'i her zaman keser. Ama task'lar farklı çekirdeklere atandığında (V3.5 SP11+ `Core` parametresi) **ikisi de aynı anda** çalışır — preemption yok, çünkü farklı CPU'lardalar. Bir mühendis race condition'ı "Prio farkı korur" diye düşündü; multicore'da iki task gerçekten paralel çalışınca klasik shared-memory race patladı. Ders: Multicore'da öncelik, çekirdek-içi sıralama yapar; çekirdekler-arası koruma sağlamaz. Paralel çekirdeklerde atomik erişim / mutex zorunludur.

## Edge Case'ler ve Sistem Limitleri

### Atomiklik Sınırları (Race Condition'ın Kökü)

Hangi atamalar tek instruction'da (atomik) tamamlanır, hangileri bölünebilir?

```
Genelde atomik (hizalı, ≤ word boyutu):   BOOL, BYTE, WORD, INT, DINT, DWORD, REAL (32-bit)
GENELDE atomik DEĞİL (bölünebilir):        LREAL/LINT (64-bit, 32-bit platformda),
                                            STRING, ARRAY, STRUCT (çok-word),
                                            POINTER (64-bit platformda kısmen)
```

**Edge case:** 32-bit ARM'da `LREAL` ataması iki 32-bit yazmaya bölünür; preemption ortada olursa okuyan task yarısı eski yarısı yeni bir "Frankenstein" değer görür. 64-bit platformda aynı `LREAL` atomik olabilir. Yani race güvenliği **platform word boyutuna** bağlıdır — kod taşınınca sessizce bozulabilir. Çok-word veriler için daima buffer/mutex deseni.

### Priority Inheritance'ın Sınırları

CODESYS `SysSem`/`SysLibSem` mutex'i priority inheritance sunar — ama yalnızca **CODESYS mutex'i** için. Şunlar inheritance kapsamı dışındadır ve sınırsız öncelik tersine dönmesi yaratabilir:

```
- Harici C kütüphanesi içindeki kilitler
- Dosya sistemi / OS çağrıları (open, write, flush)
- OPC UA stack'in iç kilitleri
- Ağ soketi blocking çağrıları
```

Bunları yüksek öncelikli task'tan **asla** doğrudan çağırmayın; düşük öncelikli bir task'ın tutabileceği bir OS kaynağında bekleyen yüksek öncelikli task, inheritance olmadan süresiz bloke olabilir.

### Watchdog ve Öncelik Etkileşimi (Omitted Cycle)

Düşük öncelikli bir task, yüksek öncelikli task'lar CPU'yu sürekli tüketirse **hiç çalışamaz** → "omitted cycle watchdog" tetiklenir (`fundamentals/01`). Yani starvation, sadece "yavaş çalışma" değil, watchdog STOP'a kadar gidebilir. Düşük öncelikli kritik-olmayan task'ların watchdog'unu, starvation'ı tolere edecek kadar geniş (veya kapalı) tutmak gerekebilir — aksi halde sağlıklı bir starvation, sistemi gereksiz yere durdurur.

### Linux SCHED_OTHER Sınırı (IEC Prio ≥13)

IEC Prio 13+ → Linux SCHED_OTHER (RT değil). Bu task'lar OS'in normal CFS scheduler'ında, **tüm sistem servisleriyle** (apt, log rotation, ssh) yarışır. Prio:15 bir log task'ı, ağır bir OS işlemi sırasında saniyelerce CPU alamayabilir. RT garantisi yalnızca IEC Prio ≤12'ye kadardır; bunu aşan hiçbir task'a zamanlama güveni duyulmamalıdır.

## Optimizasyon

### Öncelik + Cycle Time + Çekirdek: Üç Boyutlu Yerleşim

Modern multicore IPC'de optimizasyon, sadece öncelik değil çekirdek yerleşimidir:

```
Çekirdek 0-1: OS + IRQ + IEC Prio ≥13 (SCHED_OTHER) task'lar
Çekirdek 2  : Task_Fast/Motion (Prio 0-1) — izole, RT, tek başına
Çekirdek 3  : Task_Control (Prio 2) + EtherCAT — izole, RT

→ isolcpus=2,3 + her RT task'a Core ataması
→ Kritik motion task'ı, başka hiçbir şeyin koşmadığı bir çekirdekte
  → jitter dramatik düşer
```

Bu, tek çekirdekte preemption ile çözülen sıralamayı, fiziksel ayrıştırmayla çözer — en yüksek determinizm seviyesi.

### Kritik Bölgeyi Küçültme (Lock-Free'e Yaklaşma)

```iecst
(* En iyi: lock'suz tek-yazar/tek-okur — atomik word ile *)
(* Yazar task: tek DWORD/REAL atama → atomik, lock gerekmez *)
GVL.rLatest := fbCalc.fResult;

(* Çok-word veri gerekiyorsa: double-buffer + atomik index swap *)
aBuffer[nWriteIdx] := stBigRecord;   (* aktif olmayan buffer'a yaz *)
GVL.nActiveIdx := nWriteIdx;          (* tek WORD swap — atomik yayınla *)
nWriteIdx := 1 - nWriteIdx;
(* Okur task GVL.nActiveIdx'i okuyup o buffer'ı okur — hiç lock yok *)
```

Double-buffer (ping-pong), mutex'in priority inversion riskini tamamen ortadan kaldırır — yüksek performanslı task-arası paylaşımın altın standardıdır.

### IRQ Önceliklerini Ayarlama

EtherCAT/PROFINET kullanan sistemlerde ağ IRQ'sunun önceliği, fieldbus task'ı ile uyumlanmalıdır. Doğru sıralama: **IEC fieldbus task > ağ IRQ > diğer IRQ'lar**. PLC Shell `irq-set-prio` ile veya Linux `chrt`/`tuned` ile IRQ thread öncelikleri ayarlanır. Yanlış IRQ önceliği, mükemmel task tasarımını bile sync kaybıyla bozar.

## Derin Teknik Detay

### Neden Preemptive? V2 Cooperative'den Geçiş

CODESYS V2 cooperative (substituting) idi: aynı öncelikteki task biri bitmeden diğeri başlamaz, düşük öncelikli yüksek önceliği kesemezdi — basit ama bir uzun task tüm sistemi geciktirebilirdi. V3 preemptive'e geçti çünkü:

- **Determinizm garantisi:** Yüksek öncelikli (güvenlik, motion) task'ın, düşük öncelikli bir task'ın uzun exec'i yüzünden gecikmemesi gerekir. Preemption, "kritik olan her zaman önce" garantisini sağlar.
- **Modern donanım:** Preemption, hızlı bağlam değiştirme (context switch) gerektirir; V3 döneminin işlemcileri bunu ucuza yapar.
- **Bedeli:** Race condition yüzeyi açılır (V2'de iki task birbirini kesemediği için çoğu paylaşım otomatik güvenliydi). Bu yüzden V2'den taşınan kodda gizli race'ler ortaya çıkar (Not 4'teki tuzak). Preemption, güç ve sorumluluğu birlikte getirir.

### IEC Önceliğinin Linux RT Priority'ye Eşlenmesi — Neden 79 Tavan?

IEC Prio:0 → Linux RT 79'dur, 99 değil. Bu kasıtlıdır: Linux'ta RT priority 99'a yakın değerler, kernel'in kendi kritik thread'leri (migration, watchdog, RCU) tarafından kullanılır. CODESYS task'ı 99'a çıksaydı, kernel'in hayati thread'lerini aç bırakıp sistemi kararsızlaştırabilirdi. 79 tavanı, IEC task'larına geniş bir RT bandı (67-79) verirken kernel'in nefes alanını korur. Bu, "CODESYS neden 99 vermiyor" sorusunun cevabıdır — daha yüksek her zaman daha iyi değildir; OS ile birlikte yaşamak gerekir.

### Priority Inversion'ın Klasik Örneği: Mars Pathfinder

Priority inversion teorik bir endişe değildir — 1997 Mars Pathfinder görevinde aynı desen (yüksek öncelikli görev, düşük önceliklinin tuttuğu mutex'te beklerken orta öncelikli görevler araya girdi) sürekli sistem reset'lerine yol açtı; çözüm uzaktan priority inheritance'ı açmak oldu. CODESYS'te `SysSem`'in inheritance desteği bu dersin yansımasıdır. Endüstriyel bir makinede aynı desen, motion task'ının bir log task'ının tuttuğu kaynakta beklerken HMI task'ı tarafından dolaylı bloke edilmesi olarak görünür — sonuç, motion'da öngörülemeyen gecikmedir.

### Scheduler'ın Karar Anı (fundamentals/01 ile bağ)

Öncelik kararı, `fundamentals/01`'deki scheduler'ın her tick'te verdiği "şimdi kim çalışmalı" kararının çekirdeğidir. Preemptive modelde bu karar **her interrupt'ta** (yalnızca task bitiminde değil) yeniden verilir: yüksek öncelikli bir task hazır olur olmaz, scheduler çalışan düşük öncelikliyi anında askıya alır. Bu "anında" müdahale, Linux'ta RT-preempt kernel'in sağladığı şeydir — standart kernel'de scheduler ancak belirli noktalarda araya girebilir, bu da öncelik garantisini zayıflatır. Yani "öncelik doğru çalışsın" istiyorsanız, alttaki kernel'in preemption yeteneği (RT-preempt) önceliğin kendisi kadar önemlidir.

## İlgili Konular

```
knowledge/codesys/task-structure/
├── 01_task_types.md          → Task tipleri (Cyclic, Event, Freewheeling)
├── 02_cycle_time.md          → Cycle time ve CPU yük ilişkisi
└── _synthesis.md             → Task mimarisi tasarım kılavuzu

knowledge/codesys/fundamentals/
└── 01_runtime_architecture.md → Scheduler mekanizması, IEC Task Manager

knowledge/codesys/advanced/
├── multicore_tasks.md        → Çok çekirdekli sistemlerde affinity
└── shared_memory_patterns.md → Task'lar arası güvenli veri paylaşımı

knowledge/networking/
└── ethercat/task_sync.md     → EtherCAT sync ve task öncelik etkileşimi
```
