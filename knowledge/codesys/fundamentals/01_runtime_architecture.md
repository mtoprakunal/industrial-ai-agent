---
KONU        : CODESYS Runtime Mimarisi
KATEGORİ    : codesys
ALT_KATEGORI: fundamentals
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
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

**Not 6 — Retain Değişkenlerin Sessiz Kaybı (Persistence Tuzağı)**  
Bir fırınlama tesisinde günlük üretim sayaçları `VAR RETAIN` ile tanımlanmıştı. Online Change'ler sorunsuzdu, ancak bir gün **clean download** (tam yeniden indirme) yapıldığında tüm sayaçlar sıfırlandı. Neden: Retain bölgesi yalnızca online change ve power-cycle'da korunur; clean download retain'i de silebilir (varyanta göre). Daha kötüsü: Bir `RETAIN` değişkeninin **veri tipini veya sırasını** değiştirmek (ör. `INT` → `DINT`), retain bellek haritasını kaydırır ve **tüm retain değerleri çöpe döner** — derleyici uyarı vermez, değerler sessizce bozulur. Ders: Retain değişkenlerini ayrı bir GVL'de toplayın, sırasını ASLA değiştirmeyin, yeni değişkenleri **sona** ekleyin. Kritik veriler için retain yerine dosya/flash tabanlı kalıcılık (`CAA_File`, recipe management) tercih edin.

**Not 7 — Online Change'in Pointer Tuzağı**  
Bir paketleme makinesinde Online Change sonrası sistem rastgele crash etmeye başladı. Neden: Kodda `POINTER TO` ve `REFERENCE TO` ile tutulan adresler vardı. Online Change, bir FB'nin instance'ını bellekte **yeniden konumlandırdığında** (boyutu değişince) eski pointer'lar geçersiz (dangling) hale geldi. CODESYS bunu engelleyemez. Ders: Online Change yapılacak kod tabanında pointer'ları her scan'de yeniden hesaplayın (`ADR()`), asla scan'ler arası saklamayın. Güvenlik kritik sistemlerde Online Change yerine planlı duruş + clean download kullanın.

**Not 8 — Multicore'da "Daha Fazla Çekirdek = Daha Hızlı" Yanılgısı**  
8 çekirdekli bir IPC'ye geçen bir müşteri, tek bir 1ms task'ın daha hızlı olmasını bekledi — olmadı. Tek bir IEC task tek bir çekirdekte çalışır; CODESYS task'ları otomatik olarak çekirdekler arası dağıtmaz. Çoklu çekirdeğin faydası, **farklı task'ları farklı çekirdeklere** atamakla (V3.5 SP11+ `Core` parametresi) veya runtime'ı OS'ten izole etmekle gelir. Ders: Tek bir ağır döngüyü hızlandırmak için kodu paralelleştirmek (birden fazla task'a bölmek) gerekir; donanım tek başına çözmez.

**Not 9 — Bootapp ile Çalışan Kod Arasındaki Sürüm Uyuşmazlığı**  
Saha cihazı her power-cycle'da eski bir uygulamayla açılıyordu, oysa IDE'den yeni kod indirilmişti. Neden: İndirme yapıldı ama **"Create Boot Application"** çağrılmadı; runtime, RAM'deki yeni kodu çalıştırıyordu ama flash'taki `bootapp` hâlâ eskiydi. Power-cycle sonrası flash'tan eski uygulama yüklendi. Ders: Devreye almada her zaman `Online → Create Boot Application` yapın ve power-cycle testi ile doğrulayın.

## Edge Case'ler ve Sistem Limitleri

### Watchdog Tetiklenmesinin Gizli Davranışları

Watchdog tetiklendiğinde varsayılan davranış uygulamanın **STOP** durumuna geçmesidir; ancak detaylar incedir:

- **Tek task watchdog ≠ tüm sistem durması:** Çok task'lı bir uygulamada bir task'ın watchdog'u tetiklenirse **tüm uygulama** durur (her task değil). Yani diagnostic task'ınız da durur — alarmı dışarı raporlayamayabilirsiniz. Kritik alarm bildirimini watchdog'tan bağımsız bir mekanizmaya (ör. ayrı bir cihaz, hardware heartbeat) bağlayın.
- **Watchdog Sensitivity yanlış anlaşılır:** `Sensitivity = 1` her aşımda tetiklenir demek değildir. Watchdog koşulu `(cycle_time × sensitivity)` üzerinden hesaplanır; `Sensitivity` arttıkça tolerans artar. Tek seferlik bir spike'ı tolere etmek isterseniz sensitivity'yi artırın, ama bu gerçek bir takılmayı da geç yakalar.
- **Çıkışların durumu:** Watchdog STOP'ta çıkışlar **fieldbus master'ın fail-safe ayarına** göre davranır — CODESYS otomatik olarak 0'lamaz. EtherCAT'te SafeOp'a düşer, slave'in kendi fail-safe değerleri devreye girer. Bunu test etmeden "watchdog çıkışları kapatır" varsaymak tehlikelidir.

### Scan Cycle Aşımı (Cycle Overrun) — İki Farklı Senaryo

```
Senaryo A: Exec Time > Cycle Time, ama < Watchdog Time
  → Task bir sonraki interval'i KAÇIRIR (jitter birikir)
  → Sistem çalışmaya devam eder ama deterministik DEĞİLDİR
  → Sessiz tehlike: monitör dışında belirti yok

Senaryo B: Exec Time > Watchdog Time
  → Watchdog tetiklenir, uygulama STOP
  → Gürültülü ama güvenli
```

Senaryo A en tehlikelisidir çünkü görünmez. `MaxCycleTime` ve `AverageCycleTime` değerlerini sürekli izleyin; üretimde bu değerleri OPC UA ile SCADA'ya raporlayın.

### Sistem Limitleri (Pratik Tavanlar)

| Kaynak | Pratik Limit | Aşıldığında |
|---|---|---|
| Task sayısı | ~16-32 (varyanta göre) | Scheduler overhead'i ezici olur |
| En kısa cycle time | 250µs–1ms (platform) | Jitter cycle time'ı geçer, anlamsızlaşır |
| Online değişken izleme | ~1000-5000 değişken | Monitoring trafiği task'ı yavaşlatır |
| String uzunluğu | Varsayılan 80, max 255 byte | `STRING(255)` üstü için WSTRING |
| POU çağrı derinliği | Stack boyutuna bağlı (~genelde derin değil) | Stack overflow → runtime crash |
| Retain bellek | Cihaza özgü (ör. 32KB-256KB) | Sessizce taşar veya download reddedilir |

### Zaman ve Tarih Edge Case'leri

- **TIME taşması:** `TIME` tipi 32-bit milisaniyedir, ~**49.7 gün**te taşar (`T#49D17H...`). Uptime sayacı olarak `TIME` kullanan bir sistem 49 günde sıfırlanıp alarm üretti. Uzun süreler için `LTIME` (64-bit) veya `DWORD` saniye sayacı kullanın.
- **SysTimeGetMs() taşması:** Benzer şekilde 32-bit ms sayaçları periyodik taşar; iki zaman damgası arasındaki farkı `t2 - t1` ile alırken unsigned aritmetik taşmayı doğru ele alır, ama mutlak karşılaştırma (`t2 > t1`) taşma anında yanlış sonuç verir.
- **RTC senkronizasyonu:** Runtime başlarken RTC pili bitikse sistem 1970'e döner; zaman damgalı loglar bozulur. NTP/SNTP senkronizasyonunu boot'ta zorunlu kılın.

## Optimizasyon

### Jitter'ı Minimize Etme (Production-Grade Linux RT Reçetesi)

Sıralı olarak uygulanması gereken katmanlar (her biri ek kazanç verir):

```bash
# 1. RT-preempt kernel (PREEMPT_RT yaması veya hazır RT kernel)
uname -a   # ... PREEMPT_RT ... görünmeli

# 2. CPU izolasyonu — GRUB
GRUB_CMDLINE_LINUX="isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3 irqaffinity=0,1"

# 3. IRQ'ları izole çekirdeklerden uzak tut (irqaffinity yukarıda)
#    + tüm taşınabilir IRQ'ları core 0-1'e pinle

# 4. Runtime affinity — CODESYSControl.cfg
[SysProcess]
SetAffinityMask=0xC          # core 2,3 (binary 1100)
RealTimePriority=80          # OS RT öncelik (50-90 arası, 99'a yaklaşmayın)

# 5. CPU frekans yönetimini sabitle (governor)
cpupower frequency-set -g performance   # ondemand jitter yaratır

# 6. BIOS: C-states, SpeedStep, Turbo Boost, Hyperthreading KAPALI
#    (uyku durumundan çıkış latency'si jitter'ın en büyük kaynağıdır)
```

Tek tek etki sıralaması (deneyimsel): C-states kapatma > isolcpus > RT-preempt > affinity > governor. Birçok "açıklanamayan 200µs spike", BIOS'ta açık C-state'lerden kaynaklanır.

### Bellek ve Erişim Optimizasyonu

- **I/O image üzerinden çalış, fieldbus'tan doğrudan okuma:** Doğrudan slave register okumak (acyclic SDO) scan cycle'ı bloke eder. Cyclic process data (PDO) → I/O image → kod akışını koru.
- **Struct hizalama (alignment):** `{attribute 'pack_mode' := '1'}` pragmasıyla sıkıştırılmış struct'lar bellek tasarrufu sağlar ama **hizasız erişim** bazı ARM platformlarında ciddi yavaşlama (hatta exception) yaratır. Protokol paketleri için pack kullanın, hesaplama struct'ları için kullanmayın.
- **Pass-by-reference:** Büyük struct/array'leri `VAR_INPUT` ile değere göre geçmek her çağrıda kopya yaratır. `VAR_IN_OUT` (referans) veya `POINTER TO` kullanın — 10KB'lık bir struct'ı 1ms task'ta her döngü kopyalamak ölçülebilir CPU yer.
- **CONSTANT ve VAR_GLOBAL CONSTANT:** Sabitleri `CONSTANT` işaretlemek derleyiciye optimizasyon (sabit katlama) izni verir ve yanlışlıkla yazmayı engeller.

### Derleyici ve Build Optimizasyonu

- **Compiler warnings as errors:** `Project Settings → Compile options → Treat all warnings as errors` — production kodu uyarısız olmalı.
- **Build → Clean all** unutulduğunda eski derleme artıkları beklenmedik davranışa yol açar; CI/CD'de daima temiz build.
- **Static Analysis (CODESYS Static Analysis SL):** Yarışan değişken erişimi, kullanılmayan değişken, ölü kod, naming ihlali otomatik yakalanır — production kod tabanlarında zorunlu sayılmalı.

## Derin Teknik Detay

### Neden JIT Yok? Bytecode VM Tasarım Kararı

CODESYS'in execution engine'i JIT (Just-In-Time) derleme yapmaz; bytecode'u yorumlar (V3'te aslında platforma göre **derlenmiş native kod** üretir, ancak çalışma anında JIT optimizasyonu yapmaz). Bu kasıtlı bir karardır:

- **Determinizm > tepe performans:** JIT, "ısınma" sürecinde aynı kodu farklı sürelerde çalıştırır (önce yorumla, sonra derle, sonra yeniden optimize et). Bir PLC için **her döngünün aynı sürede** çalışması, ortalama hızdan çok daha kritiktir. JIT'in değişken latency'si gerçek zamanlılığı bozar.
- **Doğrulanabilirlik:** Sabit, öngörülebilir kod yolu, fonksiyonel güvenlik (functional safety) sertifikasyonunu kolaylaştırır. JIT'in çalışma anında ürettiği kodu sertifikalandırmak neredeyse imkânsızdır.
- **Bellek öngörülebilirliği:** JIT, kod cache'i için dinamik bellek ayırır — bu da deterministik olmayan GC/allocation davranışı demektir.

V2 ile V3 farkı: V2 saf bytecode yorumlayıcısıydı (daha yavaş, daha taşınabilir). V3, hedef platforma derlenmiş native makine kodu üretir (`.app` içinde platform-spesifik kod) — bu yüzden V3'te `.app` platforma bağımlıdır, ama `.project` taşınabilirdir. "Bytecode VM" zihinsel modeli V2 için tam doğru, V3 için yaklaşık doğrudur.

### I/O Image'ın Çift Tamponlama Mantığı

I/O image mekanizması neden var? Determinizm için **giriş tutarlılığı (input consistency)** gerekir: Bir scan içinde aynı girişi iki kez okuyan iki POU **aynı değeri** görmelidir. Eğer doğrudan donanımdan okunsaydı, ilk okuma ile ikinci okuma arasında fiziksel değer değişebilir, mantık tutarsızlaşırdı.

```
Input Phase  : donanım → input image (tek seferlik snapshot)
Execution    : tüm POU'lar SADECE image'i okur/yazar (kararlı görünüm)
Output Phase : output image → donanım (tek seferlik commit)
```

Bu, veritabanlarındaki **transaction isolation**'a benzer: scan cycle bir "atomik işlem"dir. Alternatif (doğrudan I/O) daha düşük latency verir ama yarış koşulları (race condition) ve tutarsızlık üretir. Yüksek hızlı uygulamalarda kasıtlı olarak image'i bypass eden "direct I/O access" özelliği vardır, ama bu determinizmi feda eder.

### Scheduler ile OS Scheduler'ın Buluşması

CODESYS Scheduler kendi başına thread yaratmaz; OS'in zamanlama primitive'lerini kullanır:

- **Linux:** Her IEC task bir `pthread`'dir, `SCHED_FIFO` politikasıyla ve `RealTimePriority` değeriyle çalışır. Cycle time, bir yüksek çözünürlüklü timer (`timerfd`/`clock_nanosleep`) ile sağlanır. RT-preempt kernel, bu thread'lerin OS kernel thread'lerini (softirq, kworker) bile önceleyebilmesini sağlar — sıradan kernel'de bu mümkün değildir.
- **Windows RTE:** RTSS (Real-Time Subsystem), Windows HAL'in altına girerek bir timer interrupt'ını ele geçirir; IEC task'ları Windows'un göremediği bir bağlamda çalışır. Bu yüzden Windows Update bile RTE task'ını kesemez — ama Win SL'i keser (Win SL sadece normal bir Windows thread'idir).

Bu mimari, "neden Win SL gerçek zamanlı değil ama Linux SL olabilir" sorusunun cevabıdır: fark runtime'da değil, **runtime'ın OS scheduler'a nasıl bağlandığındadır**.

### Component Manager: Neden Mikroservis-Benzeri Mimari?

Component Manager, runtime'ı 200+ ayrık bileşene (`CmpXXX`) böler. Bu, monolitik bir PLC firmware'ine göre radikal bir karardır:

- **Donanım üreticisi entegrasyonu:** WAGO, sadece kendi I/O sürücüsü bileşenini yazar; CODESYS çekirdeğine dokunmaz. 500+ üretici aynı çekirdeği paylaşır.
- **Lisans granülerliği:** EtherCAT master, SoftMotion gibi yetenekler ayrı bileşenlerdir; lisans bileşen seviyesinde aktifleşir. Bu yüzden "Standard SL + EtherCAT SL" gibi katmanlı lisanslama mümkün.
- **Bellek ayak izi:** Kullanılmayan bileşenler yüklenmez. 32MB RAM'li bir cihaz, OPC UA ve WebVisu bileşenlerini hiç yüklemeyerek sığabilir.
- **Bedeli:** Bileşenler arası çağrı (component interface, `CAL`) doğrudan fonksiyon çağrısından biraz daha pahalıdır; ancak bu maliyet, scan cycle başına bir kez ödenir, döngü içinde değil.

Bu, Linux kernel'in modül sistemine (loadable kernel modules) kavramsal olarak benzer: çekirdek sabit, yetenekler takılıp çıkarılabilir.

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
