---
KONU        : CODESYS Runtime Mimarisi
KATEGORİ    : codesys
ALT_KATEGORI: fundamentals
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://www.codesys.com/products/runtime/"
    başlık: "CODESYS Control Runtime System — Resmi Ürün Sayfası"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_f_reference_task.html"
    başlık: "CODESYS Online Help — Task Configuration Reference"
    güvenilirlik: resmi
  - url: "https://manualzz.com/doc/26032991/codesys-control-v3-manual"
    başlık: "CODESYS Control V3 Manual (Manualzz)"
    güvenilirlik: resmi
  - url: "https://eci.intel.com/docs/3.3/components/codesys.html"
    başlık: "Intel ECI — CODESYS Software PLC Entegrasyonu"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Runtime/"
    başlık: "CODESYS Forge Runtime Forum — Gerçek Proje Deneyimleri"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "02_project_structure.md"
    ilişki: tamamlar
  - konu: "03_iec61131_languages.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/tasks/task_types.md"
    ilişki: detaylandırır
  - konu: "knowledge/networking/fieldbus/ethercat.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Genel işletim sistemi kavramları (process, thread, scheduler)"
  - "Temel PLC mantığı ve scan cycle kavramı"
  - "Windows veya Linux kurulum deneyimi"
ÇELİŞKİLER :
  - kaynak: "Çeşitli forum kaynakları"
    konu: "Linux RT ile Windows RTE arasındaki gerçek zamanlılık performansı karşılaştırması"
    çözüm: >
      Linux RT-preempt çekirdeği ile yapılandırılmış sistemlerde CODESYS Control Linux SL,
      Windows RTE'ye kıyasla daha düşük jitter değerlerine ulaşabilmektedir; ancak bu,
      doğru CPU izolasyonu (isolcpus) ve IRQ yönetimi yapılandırmasını gerektirir.
      Windows RTE ise daha kolay kurulum ve bakım sunar; seçim projeye göre değişir.
  - kaynak: "CODESYS Resmi Dökümanlar"
    konu: "Runtime 'hardware-independent' iddiasının sınırları"
    çözüm: >
      IEC kodu gerçekten taşınabilirdir; ancak device description, fieldbus sürücüleri
      ve HAL (Hardware Abstraction Layer) uyarlamaları donanıma özgüdür. Tam bağımsızlık
      yalnızca application logic katmanında geçerlidir.
---

## Özün Ne

CODESYS Runtime (resmi adıyla *CODESYS Control*), herhangi bir akıllı cihazı IEC 61131-3 uyumlu endüstriyel kontrolcüye dönüştüren yerleşik yazılım katmanıdır. Temel fikir şudur: PLC mantığını donanımdan soyutla, taşınabilir yap. IEC 61131-3 ile yazılan uygulama kodu derlenip bir bytecode ara formatına çevrilir; bu bytecode doğrudan CPU mimarisine değil, runtime üzerinde çalışan bir sanal yürütme motoruna (execution engine) aktarılır. Bu sayede aynı `.project` dosyası Raspberry Pi üzerinde de, güçlü bir endüstriyel PC üzerinde de, ARM tabanlı gömülü bir kontrolcü üzerinde de çalışabilir; yalnızca hedef platforma uygun runtime kurulumu yeterlidir.

Milyonlarca endüstriyel uygulamada, 500'den fazla donanım üreticisinin 1000'i aşkın farklı cihaz türünde çalışan CODESYS runtime, günümüzde endüstriyel otomasyon yazılımının *de facto* standardı konumundadır. Beckhoff TwinCAT, WAGO e!COCKPIT, Bosch ctrlX ve ABB Automation Builder gibi büyük platformların tümü CODESYS runtime üzerine inşa edilmiştir.

## Nasıl Çalışır

### Mimari Katmanlar

CODESYS runtime mimarisi 4 ana katmandan oluşur:

```
┌─────────────────────────────────────────────────────────────┐
│                 IEC 61131-3 UYGULAMA KODU                   │
│         (ST / LD / FBD / SFC — kullanıcı yazar)            │
├─────────────────────────────────────────────────────────────┤
│              APPLICATION MANAGEMENT KATMANI                 │
│   IEC Task Manager  |  Scheduler  |  Debug/Monitor Engine   │
├─────────────────────────────────────────────────────────────┤
│               RUNTIME SYSTEM ÇEKİRDEĞİ                     │
│  Component Manager  |  Communication Stack  |  I/O Manager  │
│  Memory Manager     |  Execution Engine (bytecode VM)       │
├─────────────────────────────────────────────────────────────┤
│         PLATFORM ABSTRACTION LAYER (PAL / HAL)              │
│   OS Wrapper  |  File System  |  Network  |  Real-Time API   │
├─────────────────────────────────────────────────────────────┤
│               DONANIM / İŞLETİM SİSTEMİ                     │
│    Windows RTE  |  Linux RT  |  VxWorks  |  Bare Metal       │
└─────────────────────────────────────────────────────────────┘
```

### Component Manager

Runtime'ın bel kemiği **Component Manager**'dır. Tüm alt sistemler (scheduler, I/O, communication, application manager) birer *bileşen* olarak bu yöneticiye kayıt olur. Bu mimari sayesinde:

- Yeni bir fieldbus protokolü eklemek mevcut çekirdeği değiştirmez; yeni bir bileşen eklenir.
- Scheduler algoritması değiştirilebilir; yalnızca scheduler bileşeni yenilenir.
- Device üreticileri, özel HAL bileşenleri yazarak kendi donanımlarını runtime'a entegre eder.

### Scan Cycle ve Task Scheduler

Geleneksel bir donanım PLC'sinde scan cycle tek ve sabit bir döngüdür. CODESYS'te ise **çok görevli (multi-task)** bir model vardır:

```
Zaman ekseni →
│
│ Task_1 (Prio:1, 1ms)  ████░░░░████░░░░████░░░░████
│ Task_2 (Prio:2, 10ms) ░░░░████░░░░░░░░░░░░████░░░░
│ Task_Comm (Prio:15, freewheel) ░░░░░░░░████░░░░░░░░
│
│ ████ = çalışıyor  ░░░░ = bekliyor
```

Her task 3 aşamalı bir döngü izler:

1. **Input Phase**: Fiziksel giriş değerleri RAM'deki I/O image buffer'a kopyalanır.
2. **Execution Phase**: IEC bytecode yürütme motoru, task'ın çağırdığı tüm POU'ları sırayla işler.
3. **Output Phase**: Hesaplanan çıkış değerleri I/O image buffer'dan fiziksel çıkışlara yazılır.

Bu I/O image mekanizması kritiktir: Scan cycle boyunca giriş değerleri değişmez, çıkışlar da döngü bitene kadar fiziksel cihaza uygulanmaz. Bu belirlilik (determinizm) sağlar.

### IEC Task Manager ve Scheduler'ın Ayrılması

CODESYS V3'ün önemli bir tasarım kararı: IEC Task Manager ve Scheduler iki ayrı bileşendir. Task Manager, hangi POU'ların hangi task'ta çağrılacağını ve task parametrelerini (cycle time, priority, watchdog) yönetir. Scheduler ise bu task'ları işletim sisteminin zamanlayıcısıyla buluşturur. Bu ayrım sayesinde farklı platformlara özel scheduler stratejileri uygulanabilir.

### Watchdog Mekanizması

İki tür watchdog vardır:

- **Normal Watchdog**: Bir task'ın yürütme süresi tanımlanan `watchdog_time` değerini aşarsa tetiklenir. Örneğin 20ms'lik bir task'ın kodun bir döngüde 100ms tutması bu durumu tetikler.
- **Omitted Cycle Watchdog**: Bir task hiç başlamazsa (yüksek öncelikli başka bir task tarafından tamamen bloke edilirse) tetiklenir. Tetiklenme koşulu: `Time × Sensitivity` süresi içinde task bir kez bile execute edilmemişse.

### SoftPLC Varyantları

| Varyant | Platform | Gerçek Zamanlılık | Kullanım |
|---|---|---|---|
| CODESYS Control Win SL | Windows | Soft-RT (Windows scheduler) | Test, geliştirme, non-critical |
| CODESYS Control RTE SL | Windows + RTSS | Hard-RT | Yüksek performanslı Windows tabanlı IPC |
| CODESYS Control Linux SL | Linux (soft/RT-preempt) | Soft/Hard-RT | Üretim ortamı, embedded Linux |
| CODESYS Virtual Control SL | Container (Docker) | Soft-RT | Bulut, sanal test ortamları |
| CODESYS Control for Raspberry Pi | Linux/ARM | Soft-RT | Eğitim, prototipleme |

### Derleme Süreci

```
Kaynak Kod (ST/LD/FBD)
        │
        ▼
┌─────────────────────┐
│  CODESYS IDE        │
│  (Development Sys.) │
│  Derleyici          │
└──────────┬──────────┘
           │  Bytecode + Debug Bilgisi
           ▼
┌─────────────────────┐     Download (TCP/IP, USB, Serial)
│  .app dosyası       │ ──────────────────────────────────►  Runtime
│  (IEC bytecode)     │                                      (Hedef Cihaz)
└─────────────────────┘
```

Derleme sonucu oluşan `.app` dosyası platformdan bağımsızdır. Runtime bu bytecode'u kendi execution engine'i aracılığıyla işler; **JIT derleme kullanılmaz**, bu determinizmi artırır ancak saf native kod'a göre biraz daha yavaştır.

## Pratikte Nasıl Kullanılır

### 1. Runtime Kurulumu (Linux Örneği)

```bash
# CODESYS Store'dan indirilen .deb paketi ile kurulum
sudo dpkg -i codesys-control-linux-sl_4.x.x.x_amd64.deb

# Servis olarak başlatma
sudo systemctl start codesyscontrol
sudo systemctl enable codesyscontrol

# Servis durumu kontrolü
sudo systemctl status codesyscontrol
# Active: active (running) olmalı

# Log takibi
sudo journalctl -u codesyscontrol -f
```

### 2. Runtime Bağlantısı (IDE Üzerinden)

```
CODESYS IDE → Tools → Communication Settings
    ├── Gateway URL: 192.168.1.100:1217
    ├── Device Scan
    └── Bağlan (Connect)
```

`1217` portunu güvenlik duvarında açmak gerekir. Runtime'a bağlandıktan sonra IDE üzerinden:
- Online → Login (uygulama yükleme/bağlanma)
- Online → Start (uygulamayı çalıştırma)
- Online → Debug Mode (breakpoint, değişken izleme)

### 3. Runtime Konfigürasyon Dosyası

Linux'ta `/etc/CODESYSControl.cfg` veya `/etc/codesyscontrol/CODESYSControl.cfg` konumunda bulunur:

```ini
[CmpSchedule]
; Görev öncelik haritalaması
SchedulerInterval=1000          ; µs cinsinden, 1ms

[SysProcess]
; Runtime'ın çalışacağı işlemci çekirdeği (CPU pinning)
; Performans kritik sistemlerde tek çekirdeğe sabitleme
; SetAffinityMask=0x2         ; Sadece core 1 kullan (binary: 0010)

[CmpApp]
; Uygulama başlangıç davranışı
; 0: son durumu koru, 1: herzaman başlat
StartupMode=1
```

### 4. Lisanslama

Runtime demo modunda 2 saat çalışır, sonra durur. Üretim için lisans gereklidir:

```
Uygulama tabanlı lisans türleri:
├── Standard SL     → Temel kontrol, OPC UA server dahil
├── EtherCAT SL     → EtherCAT master ekler
├── SoftMotion SL   → Motion control ekler
└── WebVisu SL      → Web tabanlı HMI ekler
```

## Örnekler

### Örnek 1: Runtime Task Yapılandırması (Runtime Tarafı)

```
# /etc/codesyscontrol/CODESYSControl.cfg içinde
# RT-preempt kernel ile Linux'ta task öncelik düzeni:

[SysProcess]
RealTimePriority=79        ; Runtime ana thread önceliği (max: 99)

[CmpSchedule]
SchedulerInterval=1000     ; 1ms scheduler resolution
```

### Örnek 2: CODESYS Development System ile Runtime Sürümü Doğrulama

IDE'den bağlantı kurulduktan sonra `Device → PLC Shell` sekmesinde:

```
> version
CODESYS Control for Linux ARM64 SL V4.10.0.0
Runtime: 3.5.21.0
```

### Örnek 3: Task Yük İzleme (Online Mode)

```
Task Configuration → (Online görünüm) →
MainTask: Cycle Time: 10ms | Exec Time: 2.3ms | Jitter: ±0.1ms
FastTask: Cycle Time: 1ms  | Exec Time: 0.8ms | Jitter: ±0.2ms
CommTask: Freewheel        | Exec Time: 15ms  | -
```

Exec Time / Cycle Time oranı %80'i geçtiğinde sistem kararsız hale gelmeye başlar. Güvenli üst sınır **%70**'tir.

## Sık Yapılan Hatalar

### Hata 1: Tüm Kodu Tek Task'a Yığmak

```
❌ Yanlış: MainTask (20ms) → PLC_PRG (tüm mantık 5000 satır)

✅ Doğru:
  FastTask  (1ms)  → Safety, Emergency Stop
  MainTask  (10ms) → Process Logic
  SlowTask  (100ms)→ Communication, Diagnostics
```

### Hata 2: Windows'ta SoftPLC ile Üretim Ortamı Kurmak

CODESYS Control **Win SL** (standart Windows), gerçek zamanlı değildir. Windows'un kendi task scheduler'ı IEC task'larını istediği zaman keser. Üretim için ya **CODESYS Control RTE SL** (Real-Time extension ile) ya da Linux RT-preempt kullanılmalıdır.

```
Semptom: Task'ın max cycle time değeri ani spike'lar gösteriyor
         (10ms olması gereken task bazen 50-100ms alıyor)
Neden  : Windows güncelleme, antivirus, GPU sürücüsü CPU'yu kesintiye uğratıyor
Çözüm  : RTE SL + RTSS kernel veya Linux RT geçişi
```

### Hata 3: Watchdog'u Devre Dışı Bırakmak

```
❌ Yanlış: Watchdog kapalı — "geliştirme aşamasındayım, açmam"
✅ Doğru : Geliştirmede dahi watchdog aktif olmalı (değeri geniş tutulabilir)
```

Watchdog olmadan, yanlış bir WHILE döngüsü tüm runtime'ı dondurabilir; fiziksel çıkışlar son değerlerinde kilitlenir.

### Hata 4: IEC Bytecode ve Native Kod Farkını Anlamamak

CODESYS JIT derlemesi yapmaz. Bu şu anlama gelir:
- **Avantaj**: Deterministik davranış, her döngü aynı sürede tamamlanır.
- **Dezavantaj**: Hesaplama yoğun algoritmalarda (FFT, karmaşık matris işlemi) native kod'a göre 3-10x yavaş olabilir. Bu tür işlemler için C kütüphanesi entegrasyonu (External Library) değerlendirilmelidir.

### Hata 5: CPU Pinning Yapmadan RT Performansı Beklemek

Linux sistemlerde runtime ve IEC task'ları, işletim sisteminin diğer thread'leriyle aynı CPU çekirdeğini paylaşırsa jitter artar. Doğru yaklaşım:

```bash
# Kernel boot parametrelerine eklenir (GRUB)
GRUB_CMDLINE_LINUX="isolcpus=1,3 irqaffinity=0,2 nohz_full=1,3"

# Runtime konfigürasyonunda core sabitleme
[SysProcess]
SetAffinityMask=0xA   # Binary: 1010 → Core 1 ve Core 3
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Tercih Edilmeli

- **Donanım bağımsızlığı gerektiğinde**: Aynı PLC programının farklı donanımlarda çalışması isteniyorsa (ör. bir proje hem WAGO PFC hem Raspberry Pi hem de endüstriyel PC'de çalışacak).
- **Hızlı prototipleme**: CODESYS Control Win SL ile birkaç dakikada çalışan bir SoftPLC kurulabilir.
- **Büyük ekosistemin gücünden yararlanmak**: 500+ üreticinin device description'larına, hazır fieldbus sürücülerine ve kütüphanelerine erişim.
- **Maliyet optimizasyonu**: Özel ASIC tabanlı PLC yerine standart endüstriyel PC + SoftPLC lisansı çok daha düşük maliyetli olabilir.

### Tercih Edilmemeli

- **Mikro-saniye düzeyinde (<100µs) determinizm gerektiğinde**: Gerçek servo kontrol ve yüksek hız motion uygulamalarında FPGA tabanlı veya özel ASIC PLC'ler (ör. Beckhoff C6000 serisi ile EtherCAT) daha güvenilir performans verir. CODESYS ile µs seviyesine ulaşmak mümkün ama çok fazla sistem optimizasyonu gerektirir.
- **Çok kısıtlı gömülü sistemler**: RAM < 32MB, işlemci < 100MHz olan sistemlerde runtime ayak izi büyük olabilir.
- **Yüksek güvenlik gerektiren (SIL 3/4) sistemler**: Standart CODESYS, SIL 3+ için sertifikalı değildir; bunun için CODESYS Safety (ayrı ürün) veya dedicated safety PLC gerekir.

## Gerçek Proje Notları

**Not 1 — CPU İzolasyonu Olmadan Jitter Cehennemi**  
Bir su arıtma tesisinde 10ms döngülü dozaj kontrol projesi. Raspberry Pi üzerinde standart Raspbian ile başlandı; task monitörde max cycle time zaman zaman 300ms'e çıkıyordu. Çözüm: RT-preempt çekirdek + `isolcpus=3` + runtime affinity mask = Core 3. Sonuç: max jitter 39µs'ye düştü, proje production'a geçti.

**Not 2 — Windows Update Felaketi**  
Bir makine üreticisi, CODESYS Control Win SL ile test makinesi hazırladı. Bir gece Windows Update tetiklendi, runtime yeniden başladı ve makine hattı çöktü. Ders: Üretim makinelerinde Windows Update otomatik güncellemeleri devre dışı bırakılmalı ve CODESYS Control **RTE SL** kullanılmalıdır.

**Not 3 — Demo Modu Tuzağı**  
Müşteri tesisinde devreye alma günü, runtime 2 saatte bir duruyordu. Neden: Lisans yüklenmemişti, demo modundaydı. Kontrol listesine "lisans doğrulama" adımı eklendi.

**Not 4 — Birden Fazla Application**  
CODESYS V3'ün çok önemli özelliği: Tek runtime üzerinde **birden fazla Application** çalışabilir. Bir projede üretim mantığı (Application_Main) ve test/diagnostik mantığı (Application_Diag) ayrı uygulamalar olarak deploy edildi. Ana uygulama güncellenmeden test uygulaması serbest bırakılabildi.

**Not 5 — Execution Engine Performans Beklentisi**  
Deneyimsel veri: CODESYS ST ile yazılmış kompakt döngü kodu, C ile yazılmış eşdeğere göre yaklaşık 3-5x daha yavaş çalışır. Bu, 10ms scan cycle için genellikle sorun değildir; ancak görüntü işleme, FFT veya büyük veri sıralama yapıyorsanız harici C kütüphanesi (External Library) kullanmak şart olur.

## İlgili Konular

```
knowledge/codesys/fundamentals/
├── 02_project_structure.md      → Runtime'ın çalıştırdığı proje dosyalarının yapısı
├── 03_iec61131_languages.md     → Runtime'ın yürüttüğü dillerin detayları
└── _synthesis.md                → Üç belgenin özet sentezi

knowledge/codesys/tasks/
├── task_types.md                → Cyclic, Event, Freewheeling task detayları
└── task_priorities_linux.md     → Linux sistemlerde öncelik haritalaması

knowledge/hardware/
└── softplc_vs_hardware_plc.md   → SoftPLC ile donanım PLC karşılaştırması

knowledge/standards/
└── iec61131_overview.md         → IEC 61131-3 standardının tam tanımı
```
