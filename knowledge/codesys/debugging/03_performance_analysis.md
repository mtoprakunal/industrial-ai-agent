---
KONU        : CODESYS Performans Analizi
KATEGORİ    : codesys
ALT_KATEGORI: debugging
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_monitoring_running_tasks.html"
    başlık: "CODESYS Online Help — Monitoring Tasks"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Control/_rtsl_performance_optimization_linux.html"
    başlık: "CODESYS Control — Performance Optimization on Linux"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Profiler/_prf_profiling_methods_overview.html"
    başlık: "CODESYS Online Help — Profiling Methods Overview"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Profiler/_prf_using_profiling_by_instrumentation.html"
    başlık: "CODESYS Online Help — Profiling by Code Instrumentation"
    güvenilirlik: resmi
  - url: "https://medium.com/@sean.gongz/how-to-get-current-task-actual-cycle-time-in-codesys-267384bcd3b7"
    başlık: "Medium — Getting Actual Cycle Time in CODESYS"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_common_errors.md"
    ilişki: tamamlar
  - konu: "02_debugging_tools.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/task-structure/02_cycle_time.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/task-structure/03_priority_management.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Task yapısı ve cycle time kavramı (task-structure/02_cycle_time.md)"
  - "Debug araçları (02_debugging_tools.md)"
  - "CODESYS online bağlantısı"
ÇELİŞKİLER :
  - kaynak: "CODESYS Profiler — ücretli araç"
    konu: "Profiler, Professional Developer Edition ile gelir; standart CODESYS'te yok"
    çözüm: >
      Profiler olmadan kod bloğu zamanlaması için TIME() fonksiyonu veya
      SysClock kütüphanesi kullanılabilir. Task Monitor ve Trace ile
      sorunun hangi POU'da olduğu büyük ölçüde daraltılabilir.
      Profiler, dar çevrime ihtiyaç duyulan motion ve yüksek hız sistemler için
      kritik; standart proses kontrol için Task Monitor çoğunlukla yeterli.
---

## Özün Ne

Bir CODESYS sistemi "çalışıyor" olması, doğru çalıştığı anlamına gelmez. CPU %85'te koşan, zaman zaman watchdog alarm veren, jitter'ı tutarsız seyreden bir sistem gelecek arızalarını sessizce biriktiriyor demektir. Performans analizi, bu birikimi görünür kılmak ve müdahale etmek için gereken araçları sunar. Task Monitor anlık fotoğrafı, Trace zaman içi değişimi, Profiler ise hangi kod bloğunun ne kadar zaman aldığını söyler. Bu üçü birlikte, performans sorununu kaynak koduna kadar indirir.

## Nasıl Çalışır

### Performans Metrikleri Tanımları

```
Cycle Time (Döngü Süresi):
  Task'ın başlaması ile bir sonraki başlaması arasındaki gerçek süre.
  Konfigürasyondaki Interval = ideal değer.
  Gerçek Cycle Time = ölçülen değer.

Exec Time (Yürütme Süresi):
  Task'ın INPUT oku → Kod çalıştır → OUTPUT yaz adımlarının toplam süresi.
  Exec Time < Cycle Time olmalı.

Jitter (Zamanlama Sapması):
  Gerçek cycle başlama anı ile ideal başlama anı arasındaki fark.
  Jitter_per = |T_gerçek - T_ideal|
  Küçük jitter = iyi RT performansı.

Latency (Gecikme):
  Scheduler'ın task'ı başlatmak için görevlendirmesi ile
  task'ın gerçekte başlaması arasındaki süre.
```

```
Zaman ekseninde:
                T_ideal   T_gerçek
                   │          │
Task başlama: ─────●──────────●──────
                   └──Latency─┘
                   │←──────────────→│
                       Jitter
                   
Cycle:        ─────◄──── Cycle Time ────►─────
                   ─────◄ Exec ►─── Idle ──────
```

**Güvenli sınırlar:**
```
Max Exec Time   < Cycle Time × 0.70   → ✓ Güvenli
Max Exec Time   < Cycle Time × 0.85   → ⚠ İzle
Max Exec Time   ≥ Cycle Time           → ✗ Watchdog riski
Max Jitter      < Cycle Time × 0.10   → ✓ Kabul edilebilir RT
Max Jitter      > Cycle Time × 0.20   → ⚠ RT kernel sorunlu olabilir
```

---

## Araç 1: Task Monitor

### Erişim ve Temel Kullanım

```
Online Login → Task Configuration (çift tık) → Monitor sekmesi

Görüntülenen kolonlar:
  Task Name         : Task adı
  Status            : Running / Stopped
  Cycle Count       : Toplam döngü sayısı (sıfırlanabilir)
  Last Cycle Time   : Son döngünün gerçek süresi (µs)
  Avg Cycle Time    : Ortalama döngü süresi (µs)
  Max Cycle Time    : Şimdiye kadarki en uzun döngü (µs) ← EN KRİTİK
  Min Cycle Time    : En kısa döngü (µs)
  Jitter (µs)       : Son ölçülen jitter değeri
  Min Jitter        : Minimum jitter
  Max Jitter        : Maksimum jitter ← Spike analizi için
```

### Task Monitor Okuma Stratejisi

```
Normal durum (Task_Control, 10ms):
  Last: 10.0ms | Avg: 10.1ms | Max: 11.2ms | Jitter: ±0.3ms ✓

Sorunlu durum — Tek spike:
  Last: 10.0ms | Avg: 10.2ms | Max: 45.7ms ← Spike!
  → Ara sıra uzun süren bir şey var
  → Trace ile yakala (02_debugging_tools.md)

Sorunlu durum — Sürekli yüksek:
  Last: 8.5ms | Avg: 8.7ms | Max: 9.1ms ← Cycle Time'a çok yakın!
  → Kod kapasiteyi aşıyor
  → Cycle time artır veya kodu böl

Sorunlu durum — Yüksek jitter:
  Max Jitter: ±3.5ms (10ms task için çok yüksek)
  → RT kernel sorunu veya CPU izolasyonu eksik
  → Linux: isolcpus, IRQ önceliği kontrol et
```

### Sıfırlama ve Uzun Süreli İzleme

```
Task Monitor → Sağ tıkla → "Reset"
→ Max değerleri sıfırla, izlemeyi yeniden başlat.

48 saat boyunca izleme:
  Vardiya başında Reset → 48 saat çalış → Max değerlere bak.
  Max Cycle Time hiç tehlikeli bölgeye girmedi mi?
  → Bu soruyu sormadan üretim onayı verilmemeli.
```

---

## Araç 2: PLC Shell ile Yük İzleme

```
Device → PLC Shell sekmesi

> plcload
PLC Load: 54%

> task list
Task_Safety   [  1ms Prio:0] Exec avg  0.18ms Max  0.31ms Jitter ±0.05ms
Task_Control  [ 10ms Prio:2] Exec avg  2.20ms Max  3.60ms Jitter ±0.30ms
Task_HMI      [100ms Prio:5] Exec avg  8.10ms Max 14.20ms Jitter ±1.50ms
Task_BG       [freewheel:15] Exec avg 12.00ms Max 620ms ← Dikkat
```

```
Analiz:
  Task_Safety:  2.20/10ms = %22 load   → Normal ✓
  Task_Control: 2.20/10ms = %22 load   → Normal ✓
  Task_HMI:     8.10/100ms = %8 load   → Normal ✓
  Task_BG:      Max 620ms ← Neden bu kadar uzun? → Araştır

Total ≈ %52 → Güvenli aralıkta ✓
```

---

## Araç 3: Kod İçi Zaman Ölçümü

Profiler olmadan hangi POU'nun ne kadar sürdüğünü ölçmek için `TIME()` veya `SysClock` kullanılabilir:

```iecst
(* Yöntem 1: TIME() ile basit ölçüm *)
PROGRAM PRG_TimeMeasure
VAR
    tStart    : TIME;
    tEnd      : TIME;
    tElapsed  : TIME;
    tMaxElapsed: TIME;
END_VAR

tStart := TIME();

(* Ölçülecek kod bloğu *)
PRG_HeavyCalculation();

tEnd := TIME();
tElapsed := tEnd - tStart;

IF tElapsed > tMaxElapsed THEN
    tMaxElapsed := tElapsed;
END_IF

(* Watch Window'da tMaxElapsed izle *)
```

```iecst
(* Yöntem 2: SysClock kütüphanesi ile mikrosaniye hassasiyeti *)
VAR
    dwStart   : DWORD;
    dwEnd     : DWORD;
    dwElapsed : DWORD;  (* mikrosaniye cinsinden *)
END_VAR

dwStart := SysTimeGetUs();
PRG_HeavyCalculation();
dwEnd   := SysTimeGetUs();
dwElapsed := dwEnd - dwStart;

(* Watch Window'da dwElapsed izle — µs cinsinden *)
```

### Hangi POU Ağır? — İkili Arama Yöntemi

Profiler olmadan performans sorununu bulmak için ikili arama:

```
1. Tüm task'ı ölç → Max Exec Time = 8ms (10ms cycle, %80 yük)
2. Task'ı ikiye böl:
   a) Yalnızca ilk yarı → Max Exec Time = 1ms
   b) Yalnızca ikinci yarı → Max Exec Time = 7ms ← Sorun burada
3. İkinci yarıyı ikiye böl:
   a) PRG_MotorControl → 0.5ms
   b) PRG_Communication → 6.5ms ← Sorun burada!
4. PRG_Communication'ı incele:
   → Socket recv bloklama 6ms sürüyor → Freewheeling task'a taşı.
```

Bu yöntem kaba ama hızlı. 4-5 adımda sorunlu POU bulunur.

---

## Araç 4: CODESYS Profiler (Professional Developer Edition)

Profiler, kod bloğu bazında exec time ölçümü yapar. İki modu vardır:

### Mod 1: Code Instrumentation (Her Döngü Kaydı)

```
Kurulum:
  Application → Add Object → Profiler
  Method: Instrumentation
  Task: Task_Control
  Recording mode: Record max cycle (en uzun döngüyü yakala)
  Buffer size: 10000
  
  POU Selection: Ölçmek istediğin POU'ları seç
  (Önce üst seviye POU'lar, sonra detay)

Online → Login → Start

Snapshot:
  Profiler editor → Online sekmesi → Refresh snapshot
  
  Görünüm:
  PRG_ConveyorControl    | Samples | Total Time | % of Task
  ├── FB_Motor1          |   1000  | 0.5ms      | 5%
  ├── FB_Motor2          |   1000  | 0.5ms      | 5%
  ├── FB_TemperatureCtrl |   1000  | 5.5ms      | 55% ← HOT SPOT!
  │   ├── FB_PID         |   1000  | 4.0ms      | 40%
  │   └── FB_Filter      |   1000  | 1.5ms      | 15%
  └── PRG_Communication  |   1000  | 1.5ms      | 15%
```

### Mod 2: Sampling (Ortalama Yük Profili)

```
Kurulum:
  Method: Sampling (multicore sistemler için)
  Task: Task_Control
  Sampling Interval: Cycle time değeri önerilir (10ms)
  
Uzun süre çalıştır (10+ dakika) → Snapshot al

Görünüm: Hangi POU istatistiksel olarak en fazla zaman alıyor
(Tek döngü spike değil, ortalama yük profili)
```

---

## Spike Analizi — Kök Neden Tespiti

Spike: Belirli döngülerde max cycle time'ın normalin 3-10 katına çıkması.

### Spike Kaynakları ve Tespiti

```
Kaynak 1 — Dosya / Ağ İşlemi (En yaygın):
  Belirti: Max Exec Time sporadik olarak yüksek
  Kaynak: USB log yazma, socket recv, Modbus poll
  Tespit: Trace + kod zaman ölçümü → hangi PRG spike zamanında uzun?
  Çözüm: Bu işlemleri Freewheeling task'a taşı

Kaynak 2 — Büyük String / Dizi İşlemi:
  Belirti: Belirli koşulda spike (ör. alarm aktifken)
  Kaynak: STRING concatenation döngüsü, MEMCPY büyük buffer
  Tespit: Spike anındaki kod yolunu izle
  Çözüm: Kodu parçala, her döngüde küçük chunk işle

Kaynak 3 — Garbage Collection (nadir):
  Belirti: Düzenli aralıklarla (ör. her 60 saniyede) spike
  Kaynak: Dinamik bellek tahsis/serbest bırakma
  Çözüm: Dinamik bellek kullanımını azalt; CODESYS'te zaten az kullanılır

Kaynak 4 — OS Interrupt (Linux/Windows):
  Belirti: Spike zamanlaması rasgele, OS aktivitesiyle örtüşüyor
  Kaynak: OS güncelleme, ağ interrupt, USB
  Tespit: `cyclictest` ile OS jitter ölç
  Çözüm: RT kernel + CPU izolasyonu + IRQ affinity

Kaynak 5 — EtherCAT/Fieldbus Restart:
  Belirti: Fieldbus yeniden başladığında tek büyük spike
  Kaynak: Slave yeniden bağlanma handshake
  Çözüm: Beklenen davranış — tolerans ekle; watchdog sensitivity artır
```

### Trace ile Spike Yakalama

```iecst
(* Trace ile spike zamanında değişken değerlerini kaydet *)

(* Önce: Basit döngü sayacı ile spike zamanını tespit et *)
PROGRAM PRG_SpikeDetector
VAR
    dwCycleCount     : DWORD;
    dwSpikeCount     : DWORD;
    tLastCycle       : TIME;
    tCurrentCycle    : TIME;
    tCycleDelta      : TIME;
    tSpikeThreshold  : TIME := T#15MS;  (* 10ms task için 1.5× eşik *)
    xSpikeDetected   : BOOL;
END_VAR

dwCycleCount := dwCycleCount + 1;
tCurrentCycle := TIME();
tCycleDelta := tCurrentCycle - tLastCycle;
tLastCycle := tCurrentCycle;

xSpikeDetected := tCycleDelta > tSpikeThreshold;
IF xSpikeDetected THEN
    dwSpikeCount := dwSpikeCount + 1;
END_IF
```

```
Trace yapılandırması:
  Variables: xSpikeDetected, tCycleDelta,
             GVL_IO.rMotorCurrent, GVL_IO.rTemperature,
             dwSpikeCount
  Trigger: xSpikeDetected rising edge
  Pre-trigger: 200 döngü
  Post-trigger: 50 döngü
```

---

## Performans Optimizasyon Hiyerarşisi

Sorun tespit edildikten sonra çözüm sırası:

```
Adım 1 — Kod optimizasyonu (en az invazif):
  Bloke olan I/O → Freewheeling task'a taşı
  Büyük döngü → Parçala, her döngüde devam et
  String operasyonu → Minimize et
  Gereksiz hesaplama → Koşullu yap (her döngüde değil)

Adım 2 — Cycle time ayarı:
  Task cycle time artır (ör. 10ms → 20ms)
  → Daha az CPU pressure, daha az spike
  → Tepki süresi kabul edilebilir mi?

Adım 3 — Task bölme:
  Bir görevi birden fazla task'a böl
  Ağır: PRG_Communication → Ayrı slow task
  Hafif: PRG_Control → Hızlı task

Adım 4 — Donanım/OS optimizasyonu:
  Linux: RT-preempt çekirdek
  Linux: isolcpus, irqaffinity kernel parametreleri
  Linux: irq-set-prio ile IRQ öncelikleri
  Windows: RTE SL (RTSS kernel)
  Genel: Hyperthread'i BIOS'tan kapat
         Power saving modunu BIOS'tan kapat

Adım 5 — Donanım yükseltme:
  Daha güçlü CPU, daha hızlı RAM
  EtherCAT için dedicated NIC
```

---

## Linux Özel: Sistem Seviyesi Performans

```bash
# RT kernel kontrolü (CODESYS PLC Shell veya SSH)
> rt-get kernelinfo
# veya bash'ta:
uname -r  # "rt" içeriyorsa RT kernel

# CPU izolasyonu — Kernel parametreleri
cat /proc/cmdline
# "isolcpus=2,3 nohz_full=2,3 irqaffinity=0,1" olmalı

# Mevcut IRQ-CPU eşlemesi
cat /proc/interrupts | head -20

# Network IRQ'yu tespit et (EtherCAT için)
cat /proc/net/dev  # eth0/eth1 hangi IRQ?

# IRQ önceliğini ayarla (PLC Shell'den)
> irq-list
> irq-set-prio 32 85  # EtherCAT NIC IRQ'sunu 85'e çek

# cyclictest — OS jitter ölçümü
cyclictest -t1 -p99 -n -i1000 -l100000
# Max latency 100µs altında olmalı RT kernel ile
```

---

## Pratik Performans Kontrol Listesi

Her proje devreye almadan önce:

```
□ 1. Task Monitor'u 48 saat izle
      Max Cycle Time < Cycle Time × 0.70?
      
□ 2. Toplam CPU yükünü hesapla
      Tüm task'ların (Exec/Cycle) toplamı < %70?
      
□ 3. Max Jitter kontrol
      Max Jitter < Cycle Time × 0.10?
      
□ 4. EtherCAT sync zamanlaması (varsa)
      Send Time / Recv Time < 10µs (x64) veya < 50µs (ARM)?
      
□ 5. Freewheeling task max exec time
      Aksi görünmüyor ama bloke oluyor mu? (Max değeri anormal yüksek?)
      
□ 6. 48 saat sonrası spike sayısı
      xSpikeDetected sayacı neredeyse sıfır mı?
```

## Örnekler

### Örnek 1: Tam Performans Analiz Raporu

```
PROJE: ConveyorControl v2.1
TARİH: 2026-06-01 (48 saatlik test)
PLATFORM: i7-8550U, Linux 5.15-rt, isolcpus=2,3

TASK MONİTÖR SONUÇLARI:
Task_Safety  [1ms,  Prio:0]: Avg 0.18ms | Max 0.31ms | Jitter ±0.04ms  ✓
Task_Control [10ms, Prio:2]: Avg 2.20ms | Max 3.60ms | Jitter ±0.30ms  ✓
Task_HMI     [100ms,Prio:5]: Avg 8.10ms | Max 14.2ms | Jitter ±1.50ms  ✓
Task_BG      [freewheel:15]: Avg 12.0ms | Max 620ms ← ARAŞTIR

CPU TOPLAM: ~52% ✓ Güvenli

SPIKE ANALİZİ:
  48 saat boyunca 3 spike gözlemlendi:
  Spike 1 (09:15): Fieldbus restart sonrası — beklenen ✓
  Spike 2 (18:42): Task_BG'de USB yazma gecikmesi → DÜZELT
  Spike 3 (23:11): OS ağ interrupt → IRQ öncelik ayarı gerekli

AKSİYON:
  1. Task_BG USB yazma → Ayrı timer ile kısıtla (max 100ms block)
  2. EtherCAT NIC IRQ önceliğini 85'e çek
  3. Yeniden 24 saat izle → Onay ver
```

### Örnek 2: Kod İçi Zaman Ölçümü ile Hot Spot Bulma

```iecst
(* PRG_TimingAnalysis — Task_Control içinde tüm PRG'leri ölç *)
PROGRAM PRG_TimingAnalysis
VAR
    dwT0, dwT1, dwT2, dwT3 : DWORD;  (* µs timestamp'ler *)
    dwMotorTime    : DWORD;  (* FB_Motor grubunun süresi *)
    dwTempTime     : DWORD;  (* Sıcaklık kontrolünün süresi *)
    dwCommTime     : DWORD;  (* Communication kodu süresi *)
    dwMaxMotorTime : DWORD;  (* En uzun Motor süresi *)
    dwMaxTempTime  : DWORD;
    dwMaxCommTime  : DWORD;
END_VAR

(* Motor FB'leri *)
dwT0 := SysTimeGetUs();
fbConveyor1(xStartCmd := GVL_HMI.xConv1_Start);
fbConveyor2(xStartCmd := GVL_HMI.xConv2_Start);
fbConveyor3(xStartCmd := GVL_HMI.xConv3_Start);
dwT1 := SysTimeGetUs();
dwMotorTime := dwT1 - dwT0;
IF dwMotorTime > dwMaxMotorTime THEN dwMaxMotorTime := dwMotorTime; END_IF

(* Sıcaklık kontrolü *)
dwT1 := SysTimeGetUs();
PRG_TemperatureControl();
dwT2 := SysTimeGetUs();
dwTempTime := dwT2 - dwT1;
IF dwTempTime > dwMaxTempTime THEN dwMaxTempTime := dwTempTime; END_IF

(* Communication *)
dwT2 := SysTimeGetUs();
PRG_ModbusUpdate();
PRG_OPCUAUpdate();
dwT3 := SysTimeGetUs();
dwCommTime := dwT3 - dwT2;
IF dwCommTime > dwMaxCommTime THEN dwMaxCommTime := dwCommTime; END_IF

(* Watch Window'da izle:
   dwMaxMotorTime → 350µs  (0.35ms)  ← Normal
   dwMaxTempTime  → 280µs  (0.28ms)  ← Normal
   dwMaxCommTime  → 6200µs (6.2ms)   ← HOT SPOT! *)
```

### Örnek 3: Linux cyclictest ile OS Jitter Doğrulama

```bash
# Hedef sistem bağlantısı (SSH)
ssh user@192.168.1.100

# RT kernel var mı?
uname -r
# Beklenen: 5.15.0-rt-generic (rt içersin)

# CPU izolasyonu aktif mi?
cat /proc/cmdline
# isolcpus=2,3 görünmeli

# CODESYS durdurulmuş halde cyclictest çalıştır
sudo systemctl stop codesyscontrol

# 60 saniye jitter testi — isolated CPU'da
sudo cyclictest -t1 -p99 -n -i1000 -l60000 -a2

# Sonuç örneği (RT kernel, CPU izolasyonu ile):
# T: 0 (99) P: 0 I:1000 C: 60000 Min:    5 Act:    7 Avg:    7 Max:   38
# Max 38µs → Mükemmel RT performansı ✓

# RT kernel yoksa tipik sonuç:
# Max: 3200µs → 3.2ms jitter → EtherCAT motion için kabul edilemez

# CODESYS yeniden başlat
sudo systemctl start codesyscontrol
```

## Sık Yapılan Hata Ayıklama Hataları

### Hata 1: Average Cycle Time'a Bakmak, Max'ı Görmezden Gelmek

```
Average: 10.1ms — her şey normal görünüyor.
Max: 45.7ms — kimse bakmamış.

Kural: Task Monitor'da tek önemli değer MAX CYCLE TIME'dır.
       Ortalama sizi yanıltır; gerçek sorunlar spike'larda gizlidir.
```

### Hata 2: Performans Testini Yalnızca Başlangıçta Yapmak

```
Devreye alma günü Task Monitor iyiydi.
3 ay sonra kod büyüdü, kütüphane güncellendi, watchdog alarmları başladı.

Kural: Performans analizi rutin bakımın parçası olmalı.
       Her büyük kod değişikliğinden sonra 24 saatlik izleme şart.
```

### Hata 3: Freewheeling Task'ın Max Değerini Görmezden Gelmek

```
Task_BG Max: 620ms → "Freewheeling task, sorun değil."

Yanlış düşünce. Freewheeling task'ın 620ms sürmesi:
  a) USB yazma bloke oluyor → Dosya sistemi sorunu
  b) Ağ socket timeout → Bağlantı kesilmiş
  c) FOR döngüsü büyük veri → Kod sorunu
  
620ms bloke Freewheeling task diğer düşük öncelikli işlemleri etkiler.
Kök neden araştırılmalı — "freewheeling" geçer not değil.
```

### Hata 4: RT Kernel Olmadan Motion Control Denemek

```
Senaryo: Raspberry Pi + standart Linux + EtherCAT servo.
         Jitter ±3ms (cyclictest sonucu).
         Servo sallanıyor, pozisyon hatası büyük.

Kural: EtherCAT servo motion için RT-preempt çekirdek zorunludur.
       ARM platformlarda bile RT çekirdek + CPU izolasyonu ile
       jitter 100µs altına indirilebilir.
```

## Gerçek Proje Notları

**Not 1 — Kod İçi Zaman Ölçümüyle 6ms Spike Bulma**  
Bir paketleme hattında Task_Control sporadik 10ms spike veriyordu. Profiler yoktu. Kod içi SysTimeGetUs() ölçümü konuldu, 6 bölge ölçüldü. 2 saatlik izleme sonrası `PRG_ModbusUpdate` içindeki `SysSockRecv` çağrısının bölgeyi tuttuğu görüldü — socket zaman zaman 6ms bekliyordu. Socket non-blocking moda alındı, Modbus kodu Freewheeling task'a taşındı. Spike ortadan kalktı.

**Not 2 — cyclictest ile Çözülemeyen Jitter**  
Bir ARM endüstriyel PLC'de EtherCAT motion kontrolü çalışıyordu ama servo sallanıyordu. cyclictest Max: 450µs. RT kernel kuruluydu ama isolcpus ayarlanmamıştı. CODESYS ve OS diğer servisleri aynı CPU çekirdeğini paylaşıyordu. `/boot/cmdline.txt`'e `isolcpus=3 irqaffinity=0,1,2 nohz_full=3` eklendi. Yeniden test: Max 42µs. Servo sallanması durdu.

**Not 3 — 48 Saatlik Test Olmadan Üretim Felaketi**  
Bir fabrika hattında PLC devreye alındı, 2 saatlik test güzeldi. Üretime geçildi. Gece 3'te watchdog alarmı. Araştırma: Gece gelen ağ yayın trafiği (broadcast storm) EtherCAT NIC'in IRQ'sunu boğdu, EtherCAT task senkronizasyonu kayboldu. Gündüz test saatlerinde bu trafik yoktu. 48 saatlik test gece vardiyasını kapsasaydı fark edilirdi. IRQ önceliği düzeltildi.

**Not 4 — Task Monitor'u Monitöre Koyma**  
Bir tesiste büyük ekran monitörler gözetleme için kullanılıyordu. Task Monitor'u HMI üzerinden PLC Shell `task list` çıktısıyla periyodik olarak tazeleyip gösterdik. Bakım ekibi Max Cycle Time grafikleriyle erken uyarı alır hale geldi. İlk spike görüldüğünde mühendis uyarıldı ve müdahale edildi — watchdog alarmı olmadı.

## İlgili Konular

```
knowledge/codesys/debugging/
├── 01_common_errors.md          → Watchdog hatası triage
└── 02_debugging_tools.md        → Trace ile spike yakalama

knowledge/codesys/task-structure/
├── 02_cycle_time.md             → Exec/Cycle time teorisi
└── 03_priority_management.md    → Linux IRQ öncelik tablosu

knowledge/codesys/fundamentals/
└── 01_runtime_architecture.md   → CPU izolasyonu (isolcpus)

Araçlar:
  cyclictest   → Linux RT jitter ölçümü
  CODESYS Profiler → Professional Developer Edition (ücretli)
  PLC Shell    → plcload, task list, irq-list, irq-set-prio
```
