---
KONU        : Endüstriyel PC'de CODESYS Runtime Gerçek Zamanlı Performans Optimizasyonu
KATEGORİ    : hardware
ALT_KATEGORI: industrial-pc
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Control/_rtsl_performance_optimization_linux.html"
    başlık: "CODESYS Control — Performance Optimization (Linux) (Resmi Dokümantasyon)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Control/_rtsl_performance_optimization.html"
    başlık: "CODESYS Control — Optimization of Real-Time Performance (Resmi Dokümantasyon)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_task_configuration_jitter_definitions.html"
    başlık: "CODESYS — Definitions of Jitter and Latency (Resmi Dokümantasyon)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_obj_task_config_monitor.html"
    başlık: "CODESYS — Tab: Monitoring (Resmi Dokümantasyon)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_multi_core.html"
    başlık: "CODESYS — Multicore Support (Resmi Dokümantasyon)"
    güvenilirlik: resmi
  - url: "https://packages.debian.org/bookworm/kernel/linux-image-rt-amd64"
    başlık: "Debian Bookworm — linux-image-rt-amd64 Paket Detayları"
    güvenilirlik: resmi
  - url: "https://docs.kernel.org/admin-guide/cpu-isolation.html"
    başlık: "Linux Kernel — CPU Isolation Admin Guide"
    güvenilirlik: resmi
  - url: "https://wiki.linuxfoundation.org/realtime/preempt_rt_versions"
    başlık: "Linux Foundation Wiki — PREEMPT_RT Sürüm Listesi"
    güvenilirlik: resmi
  - url: "https://documentation.ubuntu.com/real-time/latest/how-to/measure-maximum-latency/"
    başlık: "Ubuntu Real-Time Docs — How to Measure Maximum Latency (Resmi)"
    güvenilirlik: resmi
  - url: "https://documentation.ubuntu.com/real-time/latest/how-to/tune-irq-affinity/"
    başlık: "Ubuntu Real-Time Docs — How to Tune IRQ Affinity (Resmi)"
    güvenilirlik: resmi
  - url: "https://docs.redhat.com/en/documentation/red_hat_enterprise_linux_for_real_time/9/html/optimizing_rhel_9_for_real_time_for_low_latency_operation/assembly_binding-interrupts-and-processes_optimizing-rhel9-for-real-time-for-low-latency-operation"
    başlık: "Red Hat — RHEL for Real Time 9 Tuning Guide: IRQ and Process Binding (Resmi)"
    güvenilirlik: resmi
  - url: "https://www.w3tutorials.net/blog/tickless-kernel-isolcpus-nohz-full-and-rcu-nocbs/"
    başlık: "w3tutorials — isolcpus, nohz_full ve rcu_nocbs ile Tickless Kernel"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Runtime/thread/dd3a2052c9/"
    başlık: "CODESYS Forge — Good improvement in Linux Real Time (jitter ölçüm verileri)"
    güvenilirlik: topluluk
  - url: "https://eci.intel.com/docs/3.3/components/codesys.html"
    başlık: "Intel ECI — CODESYS Software PLC Entegrasyonu ve Performans Ayarı"
    güvenilirlik: topluluk
  - url: "https://www.acontis.com/en/building-a-real-time-linux-kernel-in-ubuntu-preemptrt.html"
    başlık: "acontis — Building a Real-Time Linux Kernel in Ubuntu with PREEMPT_RT"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Runtime/thread/19f4bfbc4f/"
    başlık: "CODESYS Forge — CPU Core Affinity ve SL Lisans Kısıtı"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/hardware/industrial-pc/01_codesys_runtime_setup.md"
    ilişki: gerektirir
  - konu: "knowledge/hardware/industrial-pc/02_network_config.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/task-structure/02_cycle_time.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "CODESYS runtime kurulumu tamamlanmış olmalı — bkz. knowledge/hardware/industrial-pc/01_codesys_runtime_setup.md"
  - "CODESYS runtime mimarisi (Task, Scheduler, Scan Cycle) — bkz. knowledge/codesys/fundamentals/01_runtime_architecture.md"
  - "Linux sistem yönetimi: GRUB yapılandırması, systemd, sysctl, /proc /sys dosya sistemi"
  - "BIOS/UEFI yapılandırma erişimi fiziksel olarak mevcut olmalı"
ÇELİŞKİLER :
  - kaynak: "CODESYS Forge forum vs kernel.org belgeleri"
    konu: "nohz_full parametresi rcu_nocbs'yi otomatik etkinleştiriyor mu?"
    çözüm: >
      Güncel kernel belgelerine göre (docs.kernel.org) nohz_full belirtilen CPU'larda
      rcu_nocbs davranışını otomatik tetikler; ancak bazı forum kaynakları her ikisini
      ayrı ayrı belirtmeyi önerir. Güvenli yaklaşım: Her iki parametreyi de açıkça GRUB
      satırına yazmak. Bu çift belirtim gereksiz ama zararsızdır.
  - kaynak: "Intel ECI Dokümantasyonu vs CODESYS Forge Forum"
    konu: "CODESYSControl.cfg SetAffinityMask ile SL lisansta taskset affinity arasındaki fark"
    çözüm: >
      CODESYS Forge'da bildirilen deneyimler, SL (Single-Core) lisanslarda taskset ile
      affinity değişikliğinin görünürde çalıştığını ancak runtime'ın core 0'a dönebildiğini
      göstermektedir. CODESYS resmi belgesi de CPU pinlemenin Task Groups üzerinden
      MC (Multicore) lisansıyla yapılmasını önerir. SL lisanslı sistemlerde OS-düzeyi
      optimizasyon (isolcpus, IRQ yönlendirme) uygulanabilir; IEC görev pinlemesi için
      MC lisansı gereklidir.
  - kaynak: "CODESYS Linux Dokümantasyonu vs pratikte ölçümler"
    konu: "Hyperthreading kapatmanın etkisi"
    çözüm: >
      CODESYS Linux resmi belgesi hyperthreading kapatmayı zorunlu kılmaz; ancak
      CODESYS Forge'da paylaşılan gerçek ölçümler (180µs'den 62µs'ye iyileşme)
      SMT devre dışı bırakmanın kayda değer katkı sağladığını göstermektedir.
      Pratik öneri: üretim IPC'lerinde hyperthreading kapatılmalıdır.
---

## Özün Ne

Bir endüstriyel PC'ye CODESYS runtime kurulması, tek başına gerçek zamanlı performans garantisi vermez. Standart bir Linux çekirdeği üzerinde çalışan runtime, işletim sisteminin diğer görevleri tarafından kesilir ve bu kesintiler PLC döngü süresinde öngörülemeyen sapmalar (jitter) yaratır. Gerçek zamanlı performans optimizasyonu, bu sapmayı kabul edilebilir bir sınıra çekmek için donanım (BIOS), işletim sistemi çekirdeği ve runtime katmanlarında eşgüdümlü ayarlamalar yapılması sürecidir.

Bu belgede dört ana katman ele alınır: (1) BIOS/UEFI düzeyinde C-state/SpeedStep/hyperthreading kapatma, (2) PREEMPT_RT çekirdek kurulumu ve CPU izolasyon parametreleri (`isolcpus`, `nohz_full`, `rcu_nocbs`), (3) IRQ yönlendirme ve CPU frekans yönetimi, (4) CODESYS runtime ve IEC görev düzeyinde affinity ile jitter ölçümü. Bu aşamaların tümü uygulanmadan yalnızca birinin yapılması kısmi iyileşme sağlar; en iyi sonuç için hepsi birlikte uygulanmalıdır.

Jitter ve CPU pinleme kavramlarının genel mimarisini anlamak için bkz. `knowledge/codesys/fundamentals/01_runtime_architecture.md` — bu belge orada özetlenen ilkelerin pratikte nasıl uygulandığını detaylandırır, tekrar etmez.

## Nasıl Çalışır

### Jitter Neden Oluşur

CODESYS resmi belgelerine göre **periyodik jitter (Jper)**, bir görevin gerçek döngü süresi (Tper) ile yapılandırılan hedef döngü süresi (T0) arasındaki farktır: `Jper = Tper − T0`. **Serbest bırakma jitter'ı (Jr)** ise maksimum gecikme ile minimum gecikme arasındaki farkı gösterir: `Jr = Lmax - Lmin`. Jr = 0 olması, görevin sabit bir ofsete sahip olduğu anlamına gelir ve en iyi deterministik durumdur.

Jitter'ın başlıca kaynakları:

| Kaynak | Açıklama | Çözüm Katmanı |
|--------|----------|---------------|
| Donanım kesintileri (IRQ) | Ağ, disk, USB, PCI cihazlar çekirdeği keser | IRQ yönlendirme |
| Çekirdek zamanlayıcı tikleri | HZ frekansında periyodik zamanlayıcı ateşlenir | nohz_full |
| RCU geri çağrıları | Bellek geri kazanımı CPU'yu kısa süreliğine bloke eder | rcu_nocbs |
| C-state geçişleri | CPU derin uyku → aktif geçişte yüzlerce µs kayıp | BIOS: C-state kapat |
| Frekans ölçeklendirme | SpeedStep/P-state değişimi gecikmeye neden olur | BIOS: SpeedStep kapat |
| Hyperthreading çekişmesi | İki mantıksal çekirdek fiziksel kaynakları paylaşır | BIOS: SMT kapat |
| OS görevlerinin CPU paylaşımı | Arka plan süreçler RT görevle aynı çekirdeği kullanır | isolcpus + taskset |

### PREEMPT_RT Çekirdeğinin Etkisi

Standart Linux çekirdeğinde, kernel kodu çalışırken (spinlock tutulurken) görevler önlenemez (preempt edilemez). PREEMPT_RT bu spinlock'ların büyük çoğunluğunu uyuyabilen rt-mutex'lerle değiştirir ve donanım kesme işleyicilerini yapılandırılabilir öncelikli çekirdek thread'lerine dönüştürür. rt-mutex'ler öncelik terslemesini önlemek için öncelik devralımı (priority inheritance) uygular. Sonuç olarak en kötü durum zamanlama gecikmesi milisaniyelerden onlarca mikrosaniyeye düşer.

Kernel 6.12'den itibaren PREEMPT_RT mainline Linux çekirdeğine birleştirilmiştir. Önceki kernel'larda yamanın ayrıca uygulanması gerekir. CODESYS resmi belgesi, Linux sistemlerde PREEMPT_RT çekirdeğinin kullanılmasını açıkça önerir.

### CPU İzolasyonu Mekanizması

`isolcpus`, `nohz_full` ve `rcu_nocbs` üç parametresi birlikte çalışarak izole bir çekirdek ortamı oluşturur:

- **`isolcpus`**: Belirtilen CPU'ları genel zamanlayıcı dengeleme algoritmasından ayırır. Bu CPU'lara yalnızca açıkça atanmış görevler çalışabilir.
- **`nohz_full`**: Belirtilen CPU'larda periyodik zamanlayıcı tiklerini devre dışı bırakır ("dynticks" modu). Bu, jitter'ın önemli bir kaynağını ortadan kaldırır.
- **`rcu_nocbs`**: Bellek geri kazanımı için kullanılan RCU geri çağrılarını izole edilmiş CPU'lardan "housekeeping" CPU'larına taşır. Güncel çekirdeklerde `nohz_full` bunu otomatik tetikler; ancak her ikisini açıkça belirtmek daha güvenlidir.

### CODESYS Runtime Öncelik Eşlemesi

CODESYS Linux belgelerine göre IEC görev öncelikleri, Linux SCHED_FIFO seviyeleri ile şu şekilde eşlenir:

```
IEC RT Önceliği (32–47)  →  Linux SCHED_FIFO  56–88
IEC Standart (48–63)      →  SCHED_OTHER
```

Dikkat: Çoğu sistem IRQ'su ve kernel worker'ı ~Linux öncelik 50 seviyesinde çalışır. IEC görevleri bunların üstünde kalmak için 56+ öncelik almalıdır; ancak ağ/depolama gibi kritik sistem servisleri tam bloke edilmemelidir.

### CODESYS Multicore Lisansı ve Affinity

CPU pinleme iki ayrı mekanizma üzerinden yapılır:

1. **CODESYSControl.cfg → `[SysProcess]` → `RealTimePriority`**: Runtime ana sürecinin önceliğini ayarlar.
2. **CODESYS Multicore (MC) Lisansı → Task Groups**: IEC görevlerini belirli çekirdeklere bağlar. Standart SL lisansında bu özellik mevcut değildir. CODESYS Forge forum deneyimleri, SL lisanslarda `taskset` ile affinity denemesinin görünürde çalıştığını ancak runtime'ın core 0'a dönebildiğini ortaya koymuştur.

## Pratikte Nasıl Kullanılır

### Adım 1: BIOS/UEFI Ayarları

Bu ayarlar sisteme fiziksel erişim gerektirir ve BIOS/UEFI menüsünde uygulanır. CODESYS Forge forum ölçümlerine göre bu ayarlar tek başına jitter değerlerini yarıya indirebilir.

| BIOS Ayarı | Hedef Değer | Neden |
|------------|-------------|-------|
| C-States | Devre dışı veya C1 max | Derin uyku → aktif geçiş yüzlerce µs gecikme yaratır |
| Intel SpeedStep / AMD Cool'n'Quiet | Devre dışı | Frekans değişiminden kaynaklanan öngörülemeyen jitter önlenir |
| Turbo Boost / Turbo Core | Devre dışı (önerilir) | Ani frekans artışları zamanlama tutarsızlığı yaratır |
| Hyperthreading / SMT | Devre dışı | Her fiziksel çekirdek tek thread'e tahsis edilir; kaynak çekişmesi önlenir |
| Power Management Profile | Maximum Performance | Tüm güç tasarrufu mekanizmaları devre dışı |

CODESYS Windows RTE resmi belgesi bu ayarları açıkça listeler; Linux için de aynı prensipler geçerlidir.

### Adım 2: PREEMPT_RT Çekirdek Kurulumu

**Debian 12 (Bookworm) — Hazır Paket (En Hızlı Yol):**

```bash
# RT çekirdeği kur (Debian resmi deposunda linux-image-rt-amd64 6.1.x-rt mevcuttur)
sudo apt update
sudo apt install linux-image-rt-amd64

# GRUB güncelle ve yeniden başlat
sudo update-grub
sudo reboot
# GRUB menüsünde "Advanced options" → RT kernel'ı seç

# Doğrulama
uname -r
# Beklenen: 6.1.x-rt-amd64

grep CONFIG_PREEMPT_RT /boot/config-$(uname -r)
# Beklenen: CONFIG_PREEMPT_RT=y
```

**Ubuntu 22.04 LTS — Ubuntu Pro ile:**

```bash
# Ubuntu Pro ücretsiz kişisel hesap ile (5 makineye kadar ücretsiz)
sudo pro attach <TOKEN>
sudo pro enable realtime-kernel
sudo reboot

# Doğrulama
cat /proc/version | grep PREEMPT_RT
```

**Ubuntu / Debian — Kaynak Derleme (Özelleştirilmiş yapılandırma gerekiyorsa):**

```bash
# Bağımlılıkları yükle
sudo apt install -y build-essential libncurses-dev bison flex libssl-dev \
  libelf-dev bc dwarves zstd pahole

# Kernel + RT yamasını indir
# Mevcut sürümler: https://cdn.kernel.org/pub/linux/kernel/projects/rt/
wget https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/linux-5.15.96.tar.gz
wget https://mirrors.edge.kernel.org/pub/linux/kernel/projects/rt/5.15/patch-5.15.96-rt61.patch.xz

# Aç ve yamayı uygula
tar -xzf linux-5.15.96.tar.gz
xz -d patch-5.15.96-rt61.patch.xz
cd linux-5.15.96
patch -p1 < ../patch-5.15.96-rt61.patch

# Mevcut kernel konfigürasyonunu temel al; menuconfig'de
# "General Setup → Preemption Model → Fully Preemptible Kernel (Real-Time)" seç
cp /boot/config-$(uname -r) .config
make menuconfig

# Debian paketi olarak derle ve kur
make -j$(nproc) deb-pkg LOCALVERSION=-rt
sudo dpkg -i ../linux-image-*.deb ../linux-headers-*.deb
sudo update-grub
sudo reboot
```

### Adım 3: GRUB — CPU İzolasyonu ve C-State Parametreleri

```bash
sudo nano /etc/default/grub
```

**4 çekirdekli sistemde (core 0-1 OS, core 2-3 CODESYS) örnek yapılandırma:**

```
GRUB_CMDLINE_LINUX="quiet isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3 \
  processor.max_cstate=1 intel_idle.max_cstate=0 \
  acpi_irq_nobalance noirqbalance intel_pstate=disable"
```

| Parametre | Açıklama |
|-----------|----------|
| `isolcpus=2,3` | Core 2 ve 3'ü genel zamanlayıcıdan izole eder |
| `nohz_full=2,3` | Core 2 ve 3'te periyodik zamanlayıcı tikini durdurur |
| `rcu_nocbs=2,3` | RCU geri çağrılarını bu çekirdeklerden housekeeping CPU'larına taşır |
| `processor.max_cstate=1` | ACPI C-state'i maksimum C1 ile sınırlar (AMD ve Intel fallback) |
| `intel_idle.max_cstate=0` | Intel intel_idle sürücüsünü devre dışı bırakır; acpi_idle devralır |
| `acpi_irq_nobalance noirqbalance` | IRQ otomatik dengelemeyi önler; yönlendirme elle yapılır |
| `intel_pstate=disable` | Intel P-state sürücüsünü kapat; acpi_cpufreq devralır, performance governor daha tutarlı çalışır |

Değişikliği uygula:

```bash
sudo update-grub
sudo reboot

# Doğrulama
cat /sys/devices/system/cpu/isolated
# Çıktı: 2-3

cat /sys/devices/system/cpu/nohz_full
# Çıktı: 2-3
```

### Adım 4: IRQ Yönlendirme

irqbalance servisi devre dışı bırakıldıktan sonra tüm hareketli IRQ'ları housekeeping çekirdeklerine (core 0-1) yönlendir:

```bash
# irqbalance'ı kaldır
sudo systemctl disable irqbalance
sudo systemctl stop irqbalance

# Tüm IRQ'ları core 0 ve 1'e yönlendiren script
# 0x3 = binary 0011 = core 0 ve core 1
for irq in /proc/irq/*/smp_affinity; do
  echo 3 | sudo tee "$irq" > /dev/null 2>&1
done

# Belirli bir IRQ'nun affinity'sini kontrol et (örnek: IRQ 16)
cat /proc/irq/16/smp_affinity
# Beklenen: 00000003  (core 0 ve 1)

# smp_affinity_list okunabilir format için:
cat /proc/irq/16/smp_affinity_list
# Beklenen: 0-1
```

Bu yönlendirme reboot sonrası kaybolur. Kalıcı hale getirmek için systemd servisi veya `/etc/rc.local` kullanılabilir; ayrıca GRUB'daki `noirqbalance` ve `acpi_irq_nobalance` parametreleri boot anındaki atamayı kısmen korur.

### Adım 5: CPU Frekans Yöneticisi

```bash
# cpufrequtils yoksa yükle
sudo apt install cpufrequtils

# Tüm çekirdekleri "performance" moduna al
for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
  echo performance | sudo tee "$cpu"
done

# Doğrulama
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
# Beklenen: performance

# Kalıcı yapılandırma
echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils
sudo systemctl restart cpufrequtils
```

### Adım 6: Ek Sistem Optimizasyonları

```bash
# RT throttling'i devre dışı bırak
# Varsayılan 950000µs değeri RT thread'lerin saniyenin %95'ini kullanmasına izin verir;
# yüksek yükte bu kota dolunca RT görev sessizce askıya alınır
echo -1 | sudo tee /proc/sys/kernel/sched_rt_runtime_us

# Transparent hugepage'leri kapat (anlık bellek yeniden düzenlemesi jitter yaratır)
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled

# KSM (Kernel Samepage Merging) kapat
echo 0 | sudo tee /sys/kernel/mm/ksm/run

# NUMA dengelemeyi kapat (tek soketli sistemlerde zaten anlamsız)
echo 0 | sudo tee /proc/sys/kernel/numa_balancing

# Hyperthreading'i çalışma zamanında kontrol / kapatma
# (BIOS'tan yapılamamışsa geçici çözüm)
echo off | sudo tee /sys/devices/system/cpu/smt/control

# Kalıcı sysctl yapılandırması
cat <<'EOF' | sudo tee /etc/sysctl.d/99-realtime.conf
kernel.sched_rt_runtime_us = -1
vm.swappiness = 10
EOF
sudo sysctl --system
```

### Adım 7: CODESYSControl.cfg Performans Ayarları

Dosya konumu: `/etc/codesyscontrol/CODESYSControl.cfg`

```ini
; CODESYS Control Linux SL — Performans Optimizasyon Konfigürasyonu
; Kaynak: CODESYS Resmi Dokümantasyonu + toradex/codesys GitHub referans CFG
;         + CODESYS Forge forum ölçüm verileri

[SysCpuHandling]
; CPU DMA gecikme optimizasyonu — v4.11.0.0'dan itibaren varsayılan 1
; DMA işlemleri sırasında CPU'nun idle state'e geçmesini önler
Linux.DisableCpuDmaLatency=1

[SysProcess]
; Runtime ana thread'inin Linux gerçek zamanlı önceliği (SCHED_FIFO)
; Değer aralığı: 1-99; çoğu sistem IRQ'su ~50 önceliğinde çalışır
; Önerilen: 79 (IRQ'ların üstünde, OS kritik servislerini tamamen bloke etmez)
RealTimePriority=79

[CmpSchedule]
; Zamanlayıcı çözünürlüğü (mikrosaniye)
; 1000µs = 1ms (varsayılan); daha düşük → daha az gecikme ama daha fazla CPU yükü
; Önerilen başlangıç: 200µs; cyclictest ve task monitör ölçümlerine göre ayarla
SchedulerInterval=200

; İşlemci yük izleme
ProcessorLoad.Enable=1
ProcessorLoad.Maximum=200
ProcessorLoad.Interval=200

; Atlanan döngü watchdog'u — üretimde AÇIK tutulmalı
; Yalnızca test/debug ortamında kapatılabilir:
; DisableOmittedCycleWatchdog=1

[CmpApp]
; Boot projesi davranışı: 1 = son uygulama her zaman başlatılır
Bootproject.RetainMismatch.Init=1

[SysExcept]
; FPU istisnaları — Linux standart davranışı için devre dışı
Linux.DisableFpuUnderflowException=1
Linux.DisableFpuOverflowException=1
```

Değişiklikten sonra runtime'ı yeniden başlat:

```bash
sudo systemctl restart codesyscontrol
```

### Adım 8: CODESYS Task İzolasyonu (MC Lisansı Gerektirir)

CODESYS Multicore (MC) lisansı mevcutsa IDE üzerinden Task Groups ile CPU çekirdeği ataması yapılır:

```
CODESYS IDE → Cihaz Ağacı → Uygulama → Task Configuration
    → Task Groups sekmesi
    → "Yeni Grup" ekle: "RT_Group"
    → CPU Core: 3  (GRUB'da isolcpus ile izole edilen çekirdeklerden biri)
    → Kritik görevleri (FastTask, SafetyTask) bu gruba ata
    → İletişim görevlerini (CommTask, SlowTask) ayrı grupta bırak (Core 2)
```

**Önerilen çekirdek dağılımı — 4 çekirdekli sistem:**

```
Core 0  →  İşletim sistemi, IRQ işleme, sistem servisleri
Core 1  →  İşletim sistemi yardımcı görevleri
Core 2  →  CODESYS runtime ana süreci (codesyscontrol binary)
Core 3  →  IEC görev yürütme (kritik RT görevler buraya bağlanır)
```

## Örnekler

### Örnek 1: Tam GRUB Satırı — 4 Çekirdekli Intel IPC

```
# /etc/default/grub
GRUB_CMDLINE_LINUX="quiet isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3 \
  processor.max_cstate=1 intel_idle.max_cstate=0 \
  acpi_irq_nobalance noirqbalance intel_pstate=disable"
```

AMD sistemlerde `intel_idle.max_cstate=0` ve `intel_pstate=disable` gereksizdir; yalnızca `processor.max_cstate=1 noirqbalance acpi_irq_nobalance` yeterlidir.

### Örnek 2: cyclictest ile Jitter Ölçümü

cyclictest, RT zamanlama gecikmelerini ölçen Linux'un standart aracıdır. `rt-tests` paketinde bulunur.

```bash
# rt-tests paketini yükle
sudo apt install rt-tests

# Temel gecikme testi — izole çekirdekte (core 3) çalıştır
sudo cyclictest \
  --mlockall \        # Belleği RAM'e kilitle (sayfa hatası jitter'ı önler)
  --threads=1 \       # Tek ölçüm thread'i
  --affinity=3 \      # Core 3'te çalıştır
  --prio=99 \         # Maksimum RT öncelik
  --interval=1000 \   # 1ms uyku aralığı
  --loops=100000      # 100.000 döngü (~100 saniye)

# Histogram çıktısı ile detaylı analiz
sudo cyclictest \
  --mlockall \
  --threads=1 \
  --affinity=3 \
  --prio=99 \
  --interval=1000 \
  --loops=1000000 \
  --histogram=1000 \  # 1000 çubuklu histogram (1µs çözünürlük)
  --histofall          # Tüm thread'lerin özet sütununu ekle

# Gerçekçi yük altında ölçüm — stress-ng ile
# Terminal 1: OS çekirdeklerine yük bindir
sudo taskset -c 0,1 stress-ng --cpu 2 --vm 2 --vm-bytes 512M --timeout 300s &

# Terminal 2: Aynı anda cyclictest çalıştır
sudo cyclictest --mlockall --threads=1 --affinity=3 --prio=99 \
  --interval=1000 --loops=300000
```

**cyclictest çıktısını okuma:**

```
T: 0 (12345) P:99 I:1000 C:100000 Min:    3 Act:   12 Avg:    9 Max:   47

T   = Thread numarası
P   = Öncelik
I   = Aralık (µs)
C   = Tamamlanan döngü sayısı
Min = Minimum gecikme (µs)   → düşük = iyi
Act = Son ölçüm (µs)
Avg = Ortalama gecikme (µs)
Max = Maksimum gecikme (µs)  → en kritik gösterge
```

**Gerçek sistem ölçümleri** (CODESYS Forge forum, çeşitli donanımlar):

| Donanım | Optimizasyon Öncesi | Optimizasyon Sonrası |
|---------|--------------------|--------------------|
| Intel i5 6. nesil | 180µs | 62µs |
| Intel J1900 | ~200µs | 22µs |
| Intel i7-8565U | ~150µs | 18µs |
| Intel i5-6440EQ | ~80µs | 10µs |
| Raspberry Pi 4 | ~200µs | 19–52µs |

**CODESYS jitter kabul eşikleri** (CODESYS SoftMotion belgesi):

- ≤ 20µs → Çok iyi
- ≤ 100µs → İyi
- > 100µs → İnceleme gerektirir; sistem seviyesi optimizasyona devam et

### Örnek 3: CODESYS IDE Task Monitor — Çevrimiçi İzleme

```
Cihaz Ağacı → Uygulama → Task Configuration → Monitor sekmesi (Online mod)
```

Monitor sekmesinde görünen metrikler (CODESYS resmi belgesi):

| Sütun | Açıklama |
|-------|----------|
| Cycle Count | Toplam döngü sayısı (STOP modunda da artar) |
| IEC Cycle Count | Gerçek IEC kodu çalıştırılan döngü sayısı |
| Last Cycle Time | Son ölçülen döngü süresi (µs) |
| Avg Cycle Time | Tüm döngülerin ortalaması (µs) |
| Max Cycle Time | En uzun döngü süresi (µs) — kritik gösterge |
| Min Cycle Time | En kısa döngü süresi (µs) |
| Jitter Current | Anlık periyodik jitter Jper (µs) |
| Jitter Max | Oturumda kaydedilen en yüksek jitter (µs) |
| Core | Çalışan çekirdek numarası (-1 = tek çekirdek modu) |

Değerleri sıfırlamak için: sütun başlığına sağ tıkla → Reset.

**Not:** v3.5 SP11–SP15 arası sürümlerde jitter tepe-tepe (peak-peak) değer gösteriyordu; bu sürümlerdeki değerleri güncel sürümlerle karşılaştırırken dikkatli olunmalı.

### Örnek 4: Exec/Cycle Oranı ve %70 Kuralı

`Max Cycle Time` değerini yapılandırılan `Cycle Time` ile karşılaştırmak sistemin sağlığını gösterir:

```
Exec% = Max Cycle Time / Configured Cycle Time × 100
```

**Örnek:** 10ms döngülü bir görevde Max Cycle Time = 6.5ms ise Exec% = %65 → sağlıklı.

**Pratik rehber:**

| Exec% | Durum | Yapılması Gereken |
|-------|-------|-------------------|
| < %70 | Sağlıklı | Güvenli çalışıyor; ani yük artışlarına marjin var |
| %70–%80 | Dikkat | Döngü süresini artır veya kodu optimize et |
| > %80 | Kritik | Watchdog tetiklenme riski yüksek; acil müdahale |
| > %100 | Exception | Watchdog tetiklenmiş; görev durmuştur |

CODESYS resmi belgesi bu oranı sayısal olarak vermez; "Max Cycle Time hiçbir zaman yapılandırılan Cycle Time'a yaklaşmamalı" şeklinde ifade eder. %70 eşiği CODESYS topluluğunda yaygın kabul gören pratik bir kural olup `knowledge/codesys/fundamentals/01_runtime_architecture.md` belgesinde de (Örnek 3) referans gösterilmiştir.

## Sık Yapılan Hatalar

### Hata 1: isolcpus Ayarlanıp irqbalance Kapatılmamak

```
Senaryo: isolcpus=2,3 GRUB'a eklendi; ancak irqbalance servisi çalışmaya devam ediyor.
Sonuç  : irqbalance periyodik olarak IRQ'ları izole çekirdeklere taşıyor;
         jitter düzensiz artıyor ve sorun takibi güçleşiyor.

Çözüm:
sudo systemctl disable irqbalance
sudo systemctl stop irqbalance
```

Optimizasyon adımları sıralı ve eksiksiz uygulanmalıdır. Tek bir adım atlandığında tüm çabanın etkisi azalır.

### Hata 2: RT Throttling Aktifken Yüksek Yükte Görev Askıya Alınması

```
Senaryo: cyclictest düşük jitter gösteriyor; ancak gerçek IEC uygulaması
         yük altında zaman zaman donuyor. Logda herhangi bir hata yok.
Neden  : /proc/sys/kernel/sched_rt_runtime_us varsayılan değeri (950000),
         RT thread'lerin saniyenin %95'ini kullanmasına izin verir.
         Yoğun yükte kota dolunca Linux RT görevi SESSIZCE askıya alır.

Çözüm:
echo -1 | sudo tee /proc/sys/kernel/sched_rt_runtime_us
# Kalıcı: /etc/sysctl.d/99-realtime.conf içine kernel.sched_rt_runtime_us = -1 ekle
```

### Hata 3: C-State Devre Dışı Bırakmayı Yalnızca Yazılım ile Yapmak

```
Senaryo: GRUB'a processor.max_cstate=1 eklendi; BIOS'ta C-state hâlâ etkin.
Sonuç  : Kernel parametresi bazı C-state'leri kısıtlayabilir; ancak BIOS'un
         doğrudan donanım seviyesinde uyguladığı deep sleep state'ler devrede
         kalabilir. Jitter beklenenden yüksek seyreder.

Çözüm  : Her zaman hem BIOS hem kernel parametreleri birlikte yapılandırılmalı.
```

### Hata 4: Hyperthreading'i Açık Bırakmak

```
Senaryo: isolcpus=2,3 ile core 2 ve 3 izole edildi; BIOS'ta SMT etkin.
Sonuç  : Core 2 (fiziksel) ile Core 4 (sanal HT ikizi) aynı FPU/L1 önbelleğini
         paylaşır. OS core 4'ü kullanırken core 2'deki RT görev kaynaklardan
         dışlanır; öngörülemeyen jitter spike'ları oluşur.

Çözüm  : BIOS'ta SMT/Hyperthreading'i kapat. Sistem beklenen fiziksel çekirdek
         sayısını göstermeli (8 fiziksel çekirdekli CPU → 8 çekirdek, 16 değil).
```

### Hata 5: SL Lisansla taskset ile Affinity Denemeye Çalışmak

```
Senaryo: sudo taskset -pc 3 $(pgrep codesyscontrol) komutu çalıştırıldı.
         Affinity değeri değişti gibi görünüyor.
Sonuç  : CODESYS Forge forum bildirimine göre SL lisanslarda bu yöntem
         görünürde değişiklik yaratır ancak runtime periyodik olarak core 0'a
         dönebilir. Sonuç güvenilir değildir.

Çözüm  : CPU pinleme için CODESYS Multicore (MC) Lisansı gereklidir.
          MC lisansı Task Groups üzerinden resmi ve kalıcı core ataması sağlar.
```

### Hata 6: SchedulerInterval'ı Çok Düşük Ayarlamak

```ini
; Yanlış — çok düşük değer aşırı CPU yükü yaratır; sistem kararsızlaşabilir
[CmpSchedule]
SchedulerInterval=50   ; 50µs — gerekmedikçe bu kadar düşük gitme

; Doğru yaklaşım
[CmpSchedule]
SchedulerInterval=200  ; 200µs ile başla; ölçümlere göre ayarla
```

SchedulerInterval ile görev döngü süresi arasında denge kurulmalı. 10ms döngülü bir görev için 1000µs yeterlidir; 1ms döngülü görev için 200µs makuldür.

### Hata 7: Grafik Arayüz (GUI) Kaldırılmadan Üretim Ortamına Geçmek

```bash
# X11/masaüstü ortamı RT olmayan thread'lerle CPU paylaşır; jitter artar
dpkg -l | grep xorg

# Üretim IPC'sinde GUI kaldırılmalı
sudo apt remove --purge xorg xserver-xorg xfce4
sudo apt autoremove
```

Üretim IPC'lerinde server/headless kurulum kullanılmalı; GUI yüklenmemeli.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Bu Optimizasyonlar Gereklidir

- **EtherCAT / PROFINET RT**: 250µs veya daha düşük döngülü fieldbus master bu optimizasyonlar olmadan güvenilir çalışmaz.
- **Servo/Motion kontrol**: Konum geri besleme döngüleri 1–4ms gibi kısa döngülere ihtiyaç duyar; jitter toleransı ±0.1ms mertebesindedir.
- **Yüksek frekanslı PID döngüleri**: Kimya, ilaç, gıda gibi hassas dozaj sistemleri.
- **Çok eksenli senkronizasyon**: Birden fazla eksen veya cihazın µs hassasiyetinde eşitlenmesi.

### Bu Optimizasyonlar Gereksizdir

- **250ms veya daha uzun döngülü izleme uygulamaları**: Sıcaklık, basınç trend izleme gibi yavaş süreçlerde jitter optimizasyonu gereksiz karmaşıklık yaratır.
- **Geliştirme ve test PC'leri**: Masaüstü/laptop ortamında BIOS erişimi genellikle kısıtlıdır; bu optimizasyonların bir kısmı uygulanamaz.
- **Zaten donanım PLC kullanan sistemler**: Kanıtlanmış bir donanım PLC çözümü varsa SoftPLC'ye geçiş ve optimizasyon maliyeti gereksizdir.

### Dikkatli Olunması Gereken Durumlar

- **Güç kısıtlı ortamlar**: C-state devre dışı + performance governor ciddi güç artışına (ve ısıya) neden olur; termal tasarım buna göre yapılmalı.
- **VM / konteyner üzeri deploy**: Hypervisor katmanı RT optimizasyonlarının etkisini sınırlandırır; doğrudan donanım (bare-metal) üzerinde çalışmak tercih edilmeli.

## Gerçek Proje Notları

**Not 1 — Sıralı Optimizasyon Çalışması (Su Arıtma Tesisi)**
10ms PROFINET döngülü bir dozaj pompası kontrolü projesi. Adımlar sırayla uygulandı ve her adım sonrası cyclictest ile ölçüldü: (1) BIOS C-state kapatma → 180µs'den 90µs'ye. (2) PREEMPT_RT çekirdek + isolcpus → 39µs. (3) irqbalance kaldırma + IRQ yönlendirme → 22µs. (4) SchedulerInterval=200 → 18µs. Son değer 10ms döngü için son derece yeterli; CODESYS task monitör Max Cycle Time ≤ 3ms (%30 Exec%).

**Not 2 — Debian RT Paketi Boot Sorunu**
`apt install linux-image-rt-amd64` kurulumu sorunsuz tamamlandı; ancak GRUB menüsünde RT kernel görünmedi. Neden: Kurulum sonrası `update-grub` çalıştırılmamıştı. Teşhis: `grep menuentry /boot/grub/grub.cfg` çıktısında RT kernel yoktu. Çözüm: `sudo update-grub` + reboot. Ders: RT kernel kurulumundan sonra her zaman `update-grub` çalıştır ve GRUB menüsünde doğru kernel seçildiğini teyit et.

**Not 3 — RT Throttling Sessiz Kilidi (Motion Uygulaması)**
Bir motion uygulamasında IEC görevleri belirli bir yük eşiğinde 5–10ms askıya alınıyordu; CODESYS log'da hiçbir hata göstermiyordu. `journalctl` da sessizdi. `perf sched` ile inceleme yapınca RT kota doluluğu tespit edildi. `echo -1 > /proc/sys/kernel/sched_rt_runtime_us` ile düzeltildi. Bu ayar `/etc/sysctl.d/` altında kalıcı hale getirilmeli ve devreye alma kontrol listesine eklenmeli.

**Not 4 — Multicore Lisansının Önemi**
Bir proje SL lisansla 4 çekirdekli sistemde başlatıldı; taskset ile affinity denenince core ataması çalışır gibi göründü ancak periyodik jitter spike'ları devam etti. CODESYS MC deneme lisansı ile Task Groups ataması yapılınca RT görev Core 3'e gerçekten kilitlendi ve spike'lar tamamen ortadan kalktı. Yüksek performans kritik projelerde MC lisansı başlangıçtan itibaren bütçeye dahil edilmeli.

**Not 5 — EtherCAT ve IRQ Affinity Çatışması**
EtherCAT fieldbus kullanan bir sistemde, EtherCAT NIC IRQ'su yanlışlıkla izole bir çekirdeğe (core 3) yönlendirilmişti. Sonuç: EtherCAT sync kayıpları. Düzeltme: EtherCAT NIC IRQ'su housekeeping çekirdeğine bırakılmalı; ancak EtherCAT görev thread'i izole çekirdeğe pinlenmeli. IRQ ile thread iki farklı kavramdır; ayrı ayrı yapılandırılmalıdır.

**Not 6 — SchedulerInterval Ayarı Iterasyonu**
Bir projede varsayılan 1000µs SchedulerInterval ile başlandı; 2ms döngülü görev Exec% %85 gösteriyordu. SchedulerInterval 200µs'ye indirilince Exec% %60'a düştü ve kararlılık iyileşti. Ancak aynı değişiklik farklı bir düşük güçlü ARM sistemde (Cortex-A53) CPU yükünü %95'e çıkardı. SchedulerInterval sisteme özgüdür; her platformda ayrı ayrı optimize edilmeli.

**Not 7 — SMI (System Management Interrupt): Tüm Tuning'i Yenen Görünmez Düşman**
Tüm optimizasyonlar uygulanmış bir IPC'de cyclictest ortalama 12µs gösterirken, saatte birkaç kez 250µs+ spike'lar çıkıyordu. Bu spike'lar isolcpus/nohz_full ile açıklanamıyordu çünkü hiçbir Linux thread'i o çekirdekte çalışmıyordu. Kök neden: BIOS firmware'inin tetiklediği SMI — CPU'yu SMM (System Management Mode) moduna alan, OS'in göremediği ve maskeleyemediği en yüksek öncelikli kesme. SMI sırasında *tüm* çekirdekler donar; OS bunun farkında bile olmaz. Teşhis:
```bash
# hwlatdetect ile SMI/firmware kaynaklı donmaları ölç
sudo hwlatdetect --duration=120 --threshold=15
# SMI sayacını izle (Intel)
sudo turbostat --quiet --show SMI --interval 5
```
Çözüm sınırlıdır: BIOS'ta "USB Legacy Support", "ACPI thermal/fan SMI", "Hardware monitoring" gibi SMI üreten özellikleri kapatmak. Bazı tüketici anakartlarda SMI tamamen kapatılamaz — bu yüzden RT için *firmware'i RT-aware* endüstriyel anakart (BIOS'ta SMI minimizasyonu garantili) seçimi donanım aşamasında kritiktir. Ders: yazılım tuning'in bir tavanı var; tavanı firmware belirler.

**Not 8 — mlockall Yapılmayan Runtime'da Page Fault Jitter'ı**
cyclictest `--mlockall` ile mükemmel sonuç verirken gerçek CODESYS uygulaması ilk dakikalarda sporadik spike'lar gösterdi, sonra düzeldi. Neden: uygulama belleği henüz fiziksel RAM'e map edilmemişti; ilk erişimde major page fault oluşuyordu. CODESYS runtime kendi belleğini kilitler ancak büyük dinamik bellek (CAA Memory blokları, büyük diziler) ilk dokunuşta fault üretebilir. Önlem: `vm.swappiness=10` yetmez, üretimde swap'ı tamamen kapat (`swapoff -a`) — RT sistemde swap-in gecikmesi onlarca milisaniye olabilir. Ayrıca büyük bufferları başlatma (INIT) aşamasında bir kez "dokunarak" RAM'e zorla.

**Not 9 — Kernel 6.12 PREEMPT_RT Mainline ile -rt Paketi Davranış Farkı**
Kernel 6.12'de PREEMPT_RT mainline'a girdikten sonra bir ekip eski Debian `linux-image-rt-amd64` (6.1-rt) reflekslerini yeni kernel'e uyguladı ve `CONFIG_PREEMPT_RT=y` doğrulaması beklenenden farklı çıktı: 6.12+ kernel'de preemption modeli boot-time seçilebilir hale geldi (`preempt=full` cmdline). Doğrulama artık `uname -r`'da "-rt" aramaktan ibaret değil:
```bash
# 6.12+ için runtime preemption modunu kontrol et
cat /sys/kernel/debug/sched/preempt   # veya dmesg | grep -i preempt
journalctl -k | grep -i "rt:"
```
Eski belge/forum kaynakları hâlâ ayrı "-rt" kernel paketi varsayar; dağıtıma ve kernel sürümüne göre doğrulama yöntemi değişir. Üretimde kullanılan tam kernel sürümünü ve gerçek preemption modunu belgele.

**Not 10 — Turbo Boost Kapatınca Throughput Düştü, Jitter İyileşti — Trade-off**
Yoğun matematik (çok eksenli kinematik) içeren bir uygulamada Turbo Boost BIOS'ta kapatıldıktan sonra jitter iyileşti ama Max Cycle Time **arttı** çünkü CPU artık tek çekirdekte turbo frekansa çıkamıyordu ve ağır hesaplama base clock'ta daha uzun sürüyordu. Sonuç: Exec% %60'tan %78'e çıktı. Çözüm: turbo'yu açık bırakıp bunun yerine tüm çekirdekleri sabit yüksek frekansa kilitlemek (`intel_pstate=disable` + performance governor + min=max frekans). Jitter, frekansın *değişmesinden* kaynaklanır; yüksek sabit frekans hem düşük jitter hem yüksek throughput verir. Turbo'yu kapatmak körü körüne uygulanmamalı; hesaplama-yoğun uygulamalarda sabit-yüksek-frekans daha iyidir.

## Edge Case'ler ve Sistem Limitleri

RT tuning, sistemin doğrusal davranmadığı sınır bölgelerinde sürprizler barındırır. Aşağıdaki tablo, "her şeyi doğru yaptım ama hâlâ spike var" sınıfı sorunların altındaki edge case'leri özetler:

| Edge Case | Davranış | Mekanizma / Limit | Önlem / Teşhis |
|---|---|---|---|
| SMI / SMM girişi | Tüm çekirdekler donar, OS göremez | Firmware, NMI-üstü | `hwlatdetect`, `turbostat --show SMI` |
| Page fault (mlock yok) | İlk erişimde major fault spike | swap-in, demand paging | `mlockall`, `swapoff -a` |
| RT throttling kotası | Görev sessizce askıya alınır | `sched_rt_runtime_us=950000` | `-1` yap; `perf sched` |
| Cache thrashing (L2/L3 paylaşımı) | İzole çekirdekte bile jitter | shared LLC, başka core'un workload'u | CAT (Cache Allocation Technology) varsa partition |
| nohz_full housekeeping kotası | 1 saniyede 1 tick yine de gelir | dyntick tam sıfırlanmaz | kabul et; jitter bütçesine dahil |
| Thermal throttling | Frekans aniden düşer, jitter patlar | TjMax aşımı | termal tasarım; `turbostat` sıcaklık izle |
| C-state exit latency | C6'dan dönüş yüzlerce µs | `cpuidle` exit_latency | `processor.max_cstate=1` + BIOS |
| IRQ storm (arızalı cihaz) | Housekeeping core %100, dolaylı jitter | bozuk NIC/USB cihaz | `/proc/interrupts` artış izle |
| Çok az çekirdek (2-core) | isolcpus housekeeping'i boğar | 1 core OS'e yetmez | min 4 core RT izolasyonu için |
| MC lisans yok + multi-task | Görevler core 0'a toplanır | SL tek-core pinning kısıtı | MC lisansı |

**isolcpus'un kendi limiti:** `isolcpus` çekirdeği *zamanlayıcı dengelemeden* izole eder ama kernel'in bazı global işlemleri (TLB shootdown, IPI — Inter-Processor Interrupt, `on_each_cpu()` çağrıları) yine de izole çekirdekleri keser. Örneğin başka bir çekirdekte yapılan bir bellek unmap işlemi, izole çekirdeğe TLB shootdown IPI gönderir. Bu, izolasyonun *mutlak değil* olduğunun teknik gerçeğidir; `nohz_full` ile birlikte minimize edilir ama sıfırlanamaz.

**Determinizm tavanı:** Yazılım tuning ile ulaşılabilecek en iyi worst-case jitter, donanım/firmware tarafından belirlenir (SMI, cache mimarisi, bellek latency). Tüketici donanımında ~50-100µs taban varken, RT-aware endüstriyel donanımda <10µs mümkündür. Bu yüzden donanım seçimi tuning'den önce gelir.

## Optimizasyon

RT optimizasyonunun en kritik ilkesi **sıralamadır**: katmanlar belirli bir bağımlılık sırasına göre uygulanmalı, çünkü alttaki katman atlanırsa üsttekinin etkisi maskelenir veya ölçülemez. Determinizm zinciri aşağıdan yukarı kurulur:

**Uzman optimizasyon sıralaması (her adımdan sonra ölç, sonra ilerle):**

```
1. DONANIM/BIOS    → C-state kapat, SpeedStep kapat, SMI minimize, frekans sabitle
   (ölç: hwlatdetect — firmware tavanını öğren; bu senin teorik limitin)
        │
2. PREEMPT_RT      → RT kernel kur, preemption modunu doğrula
   (ölç: boş sistemde cyclictest — kernel tabanı)
        │
3. isolcpus/nohz   → RT çekirdekleri izole et, tickleri durdur
   (ölç: cyclictest izole çekirdekte — izolasyon kazancı)
        │
4. IRQ affinity    → irqbalance kapat, IRQ'ları housekeeping'e topla
   (ölç: yük altında cyclictest — IRQ jitter kalktı mı)
        │
5. RT throttling   → sched_rt_runtime_us=-1, swap kapat, hugepage kapat
   (ölç: uzun süreli yük testi — sessiz askıya alma var mı)
        │
6. CODESYS task    → RealTimePriority, MC lisans + Task Group pinning
   (ölç: Task Monitor Exec% + Jitter Max — uygulama seviyesi)
```

**Neden bu sıra?** Her adım bir önceki katmanın gürültüsünü ortadan kaldırdığı için, ölçüm ancak alttaki katman temizlendikten sonra anlamlıdır. Örneğin IRQ affinity'yi (4) RT kernel (2) olmadan ayarlarsan, kernel preemption gürültüsü IRQ kazancını gizler ve "IRQ ayarı işe yaramadı" yanlış sonucuna varırsın. Adım atlamadan ilerlemek, regresyonun hangi katmandan geldiğini de izole eder.

**Latency bütçesi yaklaşımı (uzman pratiği):** Toplam jitter bütçesini katmanlara böl ve her birini ayrı ölç:
```
Toplam worst-case bütçe (örn. 50µs) =
    SMI/firmware tavanı (hwlatdetect)          ~5-10µs
  + kernel preemption (boş cyclictest)         ~5-15µs
  + IRQ + IPI (yük altında cyclictest)         ~10-20µs
  + uygulama scheduling (CODESYS Jitter Max)   ~5-10µs
```
Hangi katman bütçeyi aşıyorsa oraya odaklan; her yeri körlemesine optimize etme.

**CPU partitioning ileri tekniği:** Çok çekirdekli sistemde `isolcpus` yerine cgroup v2 `cpuset` controller ile dinamik partition daha esnektir; ayrıca Intel RDT/CAT destekli CPU'larda Last-Level Cache'i RT çekirdek için ayırmak (cache partitioning) shared-LLC thrashing jitter'ını azaltır — bu, tüm çekirdek ve thread doğru pinlenmiş ama hâlâ açıklanamayan jitter olan ileri senaryolarda son çaredir.

## Derin Teknik Detay

**PREEMPT_RT içsel mekanizması — neden spinlock dönüşümü?** Standart Linux'ta `spinlock_t`, tutulduğu sürece preemption'ı kapatır (kritik bölge boyunca o çekirdekte hiçbir görev araya giremez). Bir yüksek öncelikli RT görev, düşük öncelikli bir görevin tuttuğu spinlock yüzünden çekirdek kodunda *milisaniyelerce* bekleyebilir — bu unbounded latency, gerçek zamanlılığın baş düşmanıdır. PREEMPT_RT, çoğu `spinlock_t`'i uyuyabilen `rt_mutex`'e dönüştürür: kilit tutulurken preemption açık kalır, yüksek öncelikli görev araya girebilir. Bedeli, kilidin uykuya dalma/uyanma maliyeti (context switch) ve priority inheritance defteri tutma yüküdür — bu yüzden PREEMPT_RT *ortalama* throughput'u düşürür ama *worst-case* latency'yi dramatik iyileştirir. RT'de önemli olan ortalama değil, en kötü durumdur.

**Priority inheritance — öncelik terslemesi çözümü:** Klasik öncelik terslemesi: düşük öncelikli L görevi bir mutex tutarken, orta öncelikli M görevi L'yi preempt eder, bu sırada yüksek öncelikli H görevi mutex'i bekler — H, M tarafından dolaylı olarak bloke edilmiştir. `rt_mutex`'in priority inheritance'ı: H mutex'i beklemeye başladığında L'nin önceliği geçici olarak H'ye yükseltilir, böylece M, L'yi preempt edemez ve L mutex'i hızla bırakır. Bu mekanizma, CODESYS runtime thread'leri ile kernel thread'leri arasındaki kilit etkileşimlerinde determinizmi korur.

**nohz_full'ün gerçek davranışı:** "Tickless" yanıltıcıdır — nohz_full çekirdekte tek bir runnable görev varken periyodik timer tick'ini kapatır, ama saniyede *bir* tick yine de gelir (RCU ve scheduler bookkeeping için zorunlu minimum). İki veya daha fazla runnable görev olduğunda tick geri döner (scheduler bunları ayırmak için tick'e ihtiyaç duyar). Bu yüzden izole çekirdekte **tam olarak bir** RT thread çalışması kritiktir; ikinci bir runnable görev nohz_full'ü etkisiz kılar. İşte bu, "bir RT görev = bir izole çekirdek" kuralının altındaki mekanizmadır.

**SCHED_FIFO vs SCHED_RR vs SCHED_DEADLINE — neden FIFO?** CODESYS SCHED_FIFO kullanır: aynı öncelikteki görevler arasında zaman dilimleme (time-slicing) yapmaz, görev ya gönüllü bırakana ya da daha yüksek öncelikli görev gelene kadar çalışır. SCHED_RR ise aynı öncelikte round-robin yapar (gereksiz context switch jitter'ı). SCHED_DEADLINE (EDF tabanlı) teorik olarak en iyisidir ama CODESYS'in sabit-periyotlu zamanlayıcı modeline FIFO daha doğrudan eşlenir — runtime kendi CmpSchedule'ı ile periyodu yönetir, kernel'den sadece "kesintisiz çalışma hakkı" ister. Bu yüzden FIFO seçilmiştir.

**IRQ thread'leştirme (threaded IRQs):** PREEMPT_RT'de donanım kesme işleyicileri (top-half) minimal tutulur ve asıl iş, önceliklendirilebilir bir kernel thread'e (`irq/N-devname`) taşınır. Bu, bir IRQ işleyicisinin RT görevden daha düşük önceliğe ayarlanmasını mümkün kılar — standart kernel'de imkansızdır çünkü IRQ her zaman görevi keser. Pratik sonuç: kritik olmayan bir cihazın IRQ thread'inin önceliğini RT görevinin altına çekebilirsin (`chrt -f -p <prio> $(pgrep -f irq/24)`), böylece o IRQ RT görevi bekletmez. Bu, IRQ affinity'den (hangi çekirdek) farklı ve onu tamamlayan bir kontrol eksenidir (hangi öncelik).

## İlgili Konular

```
knowledge/hardware/industrial-pc/
├── 01_codesys_runtime_setup.md      → Runtime kurulumu (bu belgenin önkoşulu)
├── 02_network_config.md             → EtherCAT / PROFINET NIC yapılandırması
└── _synthesis.md                    → Üç belgenin sentezi

knowledge/codesys/fundamentals/
├── 01_runtime_architecture.md       → Jitter/CPU pinning genel mimarisi
│                                      (Bu belgeyle tutarlı; tekrar etmez)
└── _synthesis.md                    → CODESYS temel kavramlar özeti

knowledge/codesys/task-structure/
└── 02_cycle_time.md                 → Task cycle time ayarı ve watchdog yapılandırması
```
