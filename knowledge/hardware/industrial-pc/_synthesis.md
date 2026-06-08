---
KONU        : Endüstriyel PC — SoftPLC Platformuna Giden Yol (Sentez)
KATEGORİ    : hardware
ALT_KATEGORI: industrial-pc
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "knowledge/hardware/industrial-pc/01_codesys_runtime_setup.md"
    başlık: "CODESYS Runtime Kurulumu"
    güvenilirlik: deneyimsel
  - url: "knowledge/hardware/industrial-pc/02_network_config.md"
    başlık: "Endüstriyel PC Ağ Yapılandırması"
    güvenilirlik: deneyimsel
  - url: "knowledge/hardware/industrial-pc/03_performance_tuning.md"
    başlık: "Gerçek Zamanlı Performans Optimizasyonu"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/hardware/industrial-pc/01_codesys_runtime_setup.md"
    ilişki: detaylandırır
  - konu: "knowledge/hardware/industrial-pc/02_network_config.md"
    ilişki: detaylandırır
  - konu: "knowledge/hardware/industrial-pc/03_performance_tuning.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/fundamentals/_synthesis.md"
    ilişki: önkoşul
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: önkoşul
ÖNKOŞUL     :
  - "CODESYS Runtime mimarisinin temel kavramları (SoftPLC, Task, Scan Cycle) — bkz. knowledge/codesys/fundamentals/01_runtime_architecture.md"
  - "Linux sistem yönetiminin temelleri (systemctl, dpkg, GRUB, netplan, ip, sysctl)"
  - "BIOS/UEFI yapılandırma erişimi ve Ubuntu 22.04 LTS veya Debian 12 kurulu IPC"
ÇELİŞKİLER :
  - kaynak: "01_codesys_runtime_setup.md — iki çelişki"
    konu: >
      (a) Deploy Tool ile manuel dpkg arasında tercih;
      (b) CODESYSControl.cfg dosya yolu: /etc/CODESYSControl.cfg ile /etc/codesyscontrol/ altı
    çözüm: >
      (a) CODESYS v4.14+ Deploy Tool IDE üzerinden SSH kurulumu yönetir ve önerilen yoldur;
      headless/CI ortamlarında dpkg tercih edilebilir. Her iki yol resmi dokümantasyonda mevcuttur.
      (b) Paket kurulumu /etc/codesyscontrol/ altında oluşturur; gerçek yolu doğrulamak için
      kurulum sonrası `systemctl status codesyscontrol` çıktısına bakılmalı.
  - kaynak: "02_network_config.md — iki çelişki"
    konu: >
      (a) CmpBlkDrvUdp NIC kısıtlaması için itf.0.ipaddress/name (Toradex) ile MaxInterfaces=0 (Forge) arasındaki yöntem farkı;
      (b) CmpGwServer sözdizimi için resmi belge örneği bulunamadı
    çözüm: >
      (a) Her iki yol aynı [CmpBlkDrvUdp] bölümündedir; üretim öncesi test ortamında doğrulama önerilir.
      (b) Kurulum sonrası dosya incelenerek doğrulanmalı: grep -r "CmpGwServer" /etc/codesyscontrol/
  - kaynak: "03_performance_tuning.md — üç çelişki"
    konu: >
      (a) nohz_full, rcu_nocbs'yi otomatik tetikliyor mu?;
      (b) SL lisansla taskset affinity güvenilir mi?;
      (c) Hyperthreading kapatma zorunluluğu
    çözüm: >
      (a) Güncel kernel belgelerine göre nohz_full rcu_nocbs davranışını tetikler; ancak her ikisini açıkça yazmak zararsız ve güvenlidir.
      (b) CODESYS Forge raporları SL lisanslarda taskset'in geçici çalıştığını ancak runtime'ın core 0'a dönebildiğini gösterir; güvenilir pinleme için MC lisansı gerekir.
      (c) CODESYS Linux belgesi bunu zorunlu kılmaz; Forge ölçümleri (180→62µs) kayda değer katkıyı kanıtlar. Üretimde kapatılmalı.
---

## Özün Ne

Bu sentez, "Kutudan çıkmış bir endüstriyel PC'yi üretim ortamında çalışan, gerçek zamanlı, ağa bağlı, güvenli ve güvenilir bir SoftPLC platformuna nasıl dönüştürürüm?" sorusunun bütünsel yanıtıdır.

Üç belge zorunlu bir silsiledir: **Runtime kurulumu (01)** ham donanımı IEC 61131-3 yürütücüsüne dönüştürür; **ağ yapılandırması (02)** fieldbus ve IT trafiğini fiziksel ve mantıksal olarak ayırarak güvenli iletişimi sağlar; **performans tuning (03)** OS ve donanım seviyesinde jitter kaynaklarını ortadan kaldırarak ölçülebilir gerçek zamanlı davranış garanti eder. Bu üç aşamanın tamamı uygulanmadan bir IPC "SoftPLC" değil, sadece Linux üzerinde çalışan bir yazılımdır.

## Nasıl Çalışır

### Zihin Haritası: Runtime Kurulumundan Üretime Hazır SoftPLC'ye

```
┌───────────────────────────────────────────────────────────────────────────┐
│           IPC → ÜRETİME HAZIR SOFTPLC  —  ZİHİN HARİTASI                │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  AŞAMA 1: RUNTIME KURULUMU                                                │
│  ┌────────────────────────────────────────────────────────────────┐       │
│  │  Ham IPC (Linux — Ubuntu 22.04 LTS veya Debian 12)            │       │
│  │    │                                                           │       │
│  │    ▼  dpkg -i codemeter-lite*.deb (önce CodeMeter-Lite!)       │       │
│  │    ▼  dpkg -i codesyscontrol_linux*.deb                        │       │
│  │    ▼  systemctl enable/start codesyscontrol                    │       │
│  │    ▼  /etc/codesyscontrol/CODESYSControl.cfg  ← temel ayarlar │       │
│  │    ▼  Lisans aktivasyonu (online veya offline .WibuCmRaC)      │       │
│  │    ▼  IDE → TCP 1217 üzerinden Gateway bağlantısı              │       │
│  │                                                                 │       │
│  │  Kritik dosya yolları:                                          │       │
│  │    /opt/codesys/bin/codesyscontrol.bin  ← binary               │       │
│  │    /etc/codesyscontrol/CODESYSControl.cfg  ← ana config        │       │
│  │    /var/opt/codesys/  ← lisans ve veri                         │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │  Runtime zemin hazır                        │
│                             ▼                                              │
│  AŞAMA 2: AĞ YAPILANDIRMASI                                               │
│  ┌────────────────────────────────────────────────────────────────┐       │
│  │  /etc/netplan/01-industrial.yaml  ← statik IP, çift NIC        │       │
│  │    │                                                            │       │
│  │    ├─► enp2s0: 192.168.1.x  (IT/Programlama/SCADA/OPC UA)      │       │
│  │    │     → varsayılan rota YALNIZCA burada                      │       │
│  │    │     → Gateway (TCP 1217) bu NIC'ten dinler                 │       │
│  │    │                                                            │       │
│  │    └─► enp3s0: 192.168.100.x  (Fieldbus/EtherCAT/PROFINET)     │       │
│  │          → varsayılan rota YOK; yalnızca yerel subnet           │       │
│  │          → SysEthernet özel erişim (PROFINET/EtherCAT)         │       │
│  │                                                                 │       │
│  │  CODESYSControl.cfg ağ bölümleri:                               │       │
│  │    [CmpBlkDrvUdp] MaxInterfaces=1, itf.0.ipaddress=...         │       │
│  │    [CmpOPCUAServer] NetworkAdapter=enp2s0                       │       │
│  │    [SysEthernet] Linux.ProtocolFilter=3, QDISC_BYPASS=1        │       │
│  │                                                                 │       │
│  │  UFW: 1217/tcp, 1740-1743/udp, 4840/tcp → yalnızca IT subnet   │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │  Ağ güvenli, trafikler izole                │
│                             ▼                                              │
│  AŞAMA 3: PERFORMANS TUNING                                               │
│  ┌────────────────────────────────────────────────────────────────┐       │
│  │  BIOS: C-state kapat, SpeedStep kapat, SMT(HT) kapat           │       │
│  │    │                                                            │       │
│  │    ▼  PREEMPT_RT kernel (apt install linux-image-rt-amd64)     │       │
│  │    ▼  GRUB: isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3           │       │
│  │    ▼        intel_idle.max_cstate=0 processor.max_cstate=1     │       │
│  │    ▼        noirqbalance acpi_irq_nobalance intel_pstate=disable│       │
│  │    ▼  IRQ yönlendirme: tüm IRQ'lar → core 0,1 (echo 3 > ...)  │       │
│  │    ▼  CPU frekans: performance governor (cpufrequtils)          │       │
│  │    ▼  sched_rt_runtime_us = -1 (RT throttling kapat)           │       │
│  │    ▼  CODESYSControl.cfg: RealTimePriority=79, Scheduler=200µs │       │
│  │    ▼  cyclictest ile ölçüm: Max < 100µs hedef                  │       │
│  │    ▼  CODESYS Task Monitor: Exec/Cycle < %70 doğrulama         │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                              │
│                             ▼                                              │
│  ÜRETİME HAZIR SOFTPLC PLATFORMU                                          │
│  ┌────────────────────────────────────────────────────────────────┐       │
│  │  • Deterministik scan cycle (tipik 1–10 ms)                    │       │
│  │  • Fieldbus trafiği IT'den fiziksel olarak izole               │       │
│  │  • IEC 62443 ağ bölge ayrımı uygulanmış                        │       │
│  │  • SCHED_FIFO önceliği 79, izole çekirdekler (core 2-3)        │       │
│  │  • Systemd boot: network-online.target sonrası otomatik başlar │       │
│  │  • Lisanslı (demo mod değil, üretim garantisi var)             │       │
│  └────────────────────────────────────────────────────────────────┘       │
└───────────────────────────────────────────────────────────────────────────┘
```

### Mental Model: Neden Üç Aşamanın Hepsi Zorunlu?

Kutudan çıkan bir endüstriyel PC güçlü bir x86 bilgisayardır; ancak deterministik bir PLC değildir. Dönüşüm üç katmanda gerçekleşir ve her katman bir öncekinin üzerine inşa edilir:

> **Katman 1 — Yazılım katmanı (Runtime)**: CODESYS Control SL, Linux üzerinde IEC 61131-3 kodunu yürüten yazılım servisidir. Bu olmadan donanım anlamsızdır. Ancak yalnızca bu kurulduktan sonra ağ trafiği hâlâ tehlikelidir ve jitter kabul edilemez düzeydedir.

> **Katman 2 — İletişim katmanı (Ağ)**: EtherCAT veya PROFINET trafiği IT ağıyla aynı NIC'ten geçerse hem güvenlik açığı hem fieldbus zamanlama sorunu ortaya çıkar. Çift NIC + CODESYSControl.cfg ağ bölümleri + UFW bu katmanı tamamlar. Ayrıca IEC 62443 uyumluluk için zorunludur.

> **Katman 3 — Gerçek zamanlılık katmanı (Performans)**: Standart Linux kernel ile jitter 10 ms+ olabilir; 4 ms döngülü bir task bunu tutturamaz. PREEMPT_RT, isolcpus, IRQ yönlendirme ve BIOS ayarları bu katmanı oluşturur. CODESYS Forge ölçümlerine göre optimizasyon öncesi 180µs olan max gecikme, dört adım sonunda 18–22µs'ye düşebilmektedir.

## Hızlı Referans Tabloları

### A. Runtime Kurulum Komutları (Belge 01)

| Adım | Komut | Not |
|---|---|---|
| Bağımlılık | `sudo dpkg -i codemeter-lite_<V>_amd64.deb` | **Önce CodeMeter-Lite; sonra Control** |
| Runtime kurulumu | `sudo dpkg -i codesyscontrol_linux_<V>_amd64.deb` | — |
| Servis etkinleştir | `sudo systemctl enable codesyscontrol` | Boot otomatik |
| Servis başlat | `sudo systemctl start codesyscontrol` | — |
| Durum kontrol | `sudo systemctl status codesyscontrol` | "active (running)" beklenir |
| Canlı log | `sudo journalctl -u codesyscontrol -f` | — |
| Port doğrulama | `ss -tlnp \| grep 1217` | LISTEN görülmeli |
| Yeniden başlat | `sudo systemctl restart codesyscontrol` | cfg değişikliği sonrası |

### B. CODESYS Port Tablosu (Belge 02'den — resmi kaynak)

| Port | Protokol | Kullanım | Erişim |
|---|---|---|---|
| **1217** | TCP | Gateway: IDE ↔ Runtime | Yalnızca IT/Programlama subnet |
| **1740–1743** | UDP | Scan Network discovery | Yalnızca IT subnet |
| **11740–11743** | TCP | Direkt instance bağlantısı | Yalnızca IT subnet |
| **4840** | TCP | OPC UA sunucusu | Yalnızca SCADA subnet |
| **8080** | TCP | WebVisu (HTTP) | Dahili ağ |
| **443** | TCP | WebVisu (HTTPS) | Dahili ağ |
| **22** | TCP | SSH | Yalnızca IT subnet |

### C. Performans Parametreleri (Belge 03'ten — konsolide)

| Katman | Parametre | Değer | Açıklama |
|---|---|---|---|
| BIOS | C-States | Kapalı (C1 max) | Derin uyku gecikmesi önlenir |
| BIOS | SpeedStep/AMD Cool'n'Quiet | Kapalı | Frekans jitter önlenir |
| BIOS | Hyperthreading/SMT | Kapalı | Fiziksel çekirdek başına tek thread |
| GRUB | isolcpus | `2,3` (4-core örnek) | Zamanlayıcıdan izole |
| GRUB | nohz_full | `2,3` | Periyodik tikler durdurulur |
| GRUB | rcu_nocbs | `2,3` | RCU geri çağrıları taşınır |
| GRUB | intel_idle.max_cstate | `0` | intel_idle sürücüsü devre dışı |
| Kernel | sched_rt_runtime_us | `-1` | RT throttling kapatılır |
| CODESYSControl.cfg | RealTimePriority | `79` | SCHED_FIFO seviyesi |
| CODESYSControl.cfg | SchedulerInterval | `200` (µs) | 200µs ile başla; ölçüme göre ayarla |
| CODESYSControl.cfg | DisableCpuDmaLatency | `1` | DMA idle state geçişini önler |

### D. CODESYSControl.cfg — Üretim Şablonu (3 Belgenin Sentezi)

```ini
; ────────────────────────────────────────────────────────────────
; CODESYSControl.cfg — Üretim IPC Şablonu
; Kaynak: 01_codesys_runtime_setup.md + 02_network_config.md
;         + 03_performance_tuning.md
; ────────────────────────────────────────────────────────────────

[CmpGwServer]
Port=1217                          ; IDE bağlantı portu (Belge 01)

[SysSocket]
Adapter.0.Name=enp3s0              ; Fieldbus NIC (Belge 02 — PROFINET device)
Adapter.0.EnableSetIpAndMask=1     ; PROFINET DCP IP ataması

[SysEthernet]
Linux.ProtocolFilter=3             ; ETH_P_ALL — PROFINET/EtherCAT (Belge 02)
Linux.PACKET_QDISC_BYPASS=1        ; Fieldbus RT send jitter azaltır (Belge 02)

[CmpBlkDrvUdp]
MaxInterfaces=1                    ; Yalnızca IT NIC (Belge 02)
itf.0.ipaddress=192.168.1.100
itf.0.name=main
itf.0.networkmask=255.255.255.0

[CmpOPCUAServer]
NetworkAdapter=enp2s0              ; OPC UA → yalnızca IT NIC (Belge 02)
NetworkPort=4840

[SysCpuHandling]
Linux.DisableCpuDmaLatency=1       ; DMA gecikme önleme (Belge 01 + 03)

[SysProcess]
RealTimePriority=79                ; SCHED_FIFO (Belge 03)

[CmpSchedule]
SchedulerInterval=200              ; µs — ölçüme göre ayarla (Belge 03)
ProcessorLoad.Enable=1
ProcessorLoad.Maximum=200
ProcessorLoad.Interval=200

[CmpApp]
Bootproject.RetainMismatch.Init=1  ; Son uygulama boot'ta başlar (Belge 01)

[SysExcept]
Linux.DisableFpuUnderflowException=1
Linux.DisableFpuOverflowException=1
```

### E. Kritik Eşik Değerler

| Metrik | İyi | Dikkat | Kritik | Ölçüm |
|---|---|---|---|---|
| cyclictest Max Gecikme | ≤ 20µs | ≤ 100µs | > 100µs | `cyclictest --mlockall --affinity=3 --prio=99` |
| CODESYS Exec% | < %70 | %70–%80 | > %80 | Task Monitor → Max Cycle Time / Cycle Time |
| Jitter Max (Task Monitor) | ≤ 20µs | ≤ 100µs | > 100µs | IDE online mod → Task Config → Monitor |
| Demo mod | — | — | 2 saat sonra durur | `journalctl -u codesyscontrol \| grep demo` |

## Pratikte Nasıl Kullanılır

### Sıfırdan Üretime Kontrol Listesi

**AŞAMA 1 — Donanım Hazırlık**
```
□ BIOS: Secure Boot KAPALI (CODESYS Control SL imza sorunu)
□ BIOS: CPU C-States devre dışı (C1 max)
□ BIOS: Hyperthreading/SMT KAPALI
□ BIOS: SpeedStep/Turbo Boost KAPALI
□ BIOS: Power Management Profile → Maximum Performance
```

**AŞAMA 2 — İşletim Sistemi**
```
□ Ubuntu 22.04 LTS server (headless — GUI YOK) veya Debian 12 minimal
□ GUI yükleme: KESİNLİKLE KURMA — X11 RT olmayan thread'lerle CPU paylaşır
□ PREEMPT_RT kernel kur:
    Debian: sudo apt install linux-image-rt-amd64
    Ubuntu: sudo pro enable realtime-kernel  (Ubuntu Pro ücretsiz)
□ sudo update-grub && sudo reboot
□ uname -r çıktısında "-rt" ifadesi görülmeli
□ grep CONFIG_PREEMPT_RT /boot/config-$(uname -r) → CONFIG_PREEMPT_RT=y
□ Otomatik güncellemeleri kapat (unattended-upgrades)
```

**AŞAMA 3 — Runtime Kurulumu (Belge 01)**
```
□ sudo dpkg -i codemeter-lite_<V>_amd64.deb    ← ÖNCE CodeMeter-Lite
□ sudo systemctl start CodeMeter
□ sudo dpkg -i codesyscontrol_linux_<V>_amd64.deb
□ sudo systemctl enable codesyscontrol
□ /etc/codesyscontrol/CODESYSControl.cfg düzenle (şablon: Tablo D)
□ sudo systemctl start codesyscontrol
□ sudo journalctl -u codesyscontrol -f → hata yok mu?
□ ss -tlnp | grep 1217 → port dinleniyor mu?
□ IDE → License Manager → Lisansı aktive et (demo modda teslim ETME)
□ IDE → Communication Settings → Scan Network → IPC görünüyor mu?
□ Systemd boot sırası: network-online.target sonrası başlamalı
    /etc/systemd/system/codesyscontrol.service.d/override.conf:
    [Unit]
    After=network-online.target
    Wants=network-online.target
```

**AŞAMA 4 — Ağ Yapılandırması (Belge 02)**
```
□ ip link show → NIC isimlerini belirle (enp2s0, enp3s0 vb.)
□ /etc/netplan/01-industrial.yaml oluştur:
    enp2s0: IT/Programlama — statik IP, varsayılan rota BURADA
    enp3s0: Fieldbus — statik IP, varsayılan rota YOK
□ NIC'lere MAC adresine bağlı kalıcı isim ata (match.macaddress + set-name)
□ sudo chmod 600 /etc/netplan/01-industrial.yaml
□ sudo netplan try --timeout 60 (SSH'da güvenli uygulama)
□ CODESYSControl.cfg ağ bölümlerini yapılandır (Tablo D)
□ sudo systemctl restart codesyscontrol
□ ss -tlnp | grep 1217 → 192.168.1.x:1217 (0.0.0.0 DEĞİL)
□ UFW yapılandır: 1217/tcp, 1740-1743/udp, 4840/tcp → yalnızca IT subnet
□ Fieldbus subnet'inden 1217 ve 4840'a erişimi engelle
□ sudo ufw enable
```

**AŞAMA 5 — Performans Tuning (Belge 03)**
```
□ sudo nano /etc/default/grub → GRUB_CMDLINE_LINUX'a ekle:
    isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3
    processor.max_cstate=1 intel_idle.max_cstate=0
    acpi_irq_nobalance noirqbalance intel_pstate=disable
□ sudo update-grub && sudo reboot
□ cat /sys/devices/system/cpu/isolated → "2-3" görülmeli
□ sudo systemctl disable irqbalance && sudo systemctl stop irqbalance
□ IRQ yönlendirme: tüm IRQ'ları core 0,1'e (0x3)
    for irq in /proc/irq/*/smp_affinity; do echo 3 | sudo tee "$irq"; done
□ CPU frekans: performance governor
    for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
      echo performance | sudo tee "$cpu"; done
□ RT throttling kapat:
    echo -1 | sudo tee /proc/sys/kernel/sched_rt_runtime_us
    /etc/sysctl.d/99-realtime.conf: kernel.sched_rt_runtime_us = -1
□ Transparent hugepages kapat:
    echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
□ GUI varsa kaldır: sudo apt remove --purge xorg xserver-xorg
□ CODESYSControl.cfg: RealTimePriority=79, SchedulerInterval=200
□ sudo systemctl restart codesyscontrol
```

**AŞAMA 6 — Üretime Alım Doğrulama**
```
□ Baseline cyclictest (OS yükü altında, izole çekirdekte):
    sudo apt install rt-tests
    sudo cyclictest --mlockall --threads=1 --affinity=3 --prio=99
                    --interval=1000 --loops=1000000
    → Max gecikme ≤ 100µs hedef (< 20µs çok iyi, CODESYS SoftMotion belgesi)
□ Gerçek yük altında cyclictest:
    stress-ng --cpu 2 --vm 2 & cyclictest ...
□ IDE → gerçek IEC uygulaması yükle, Task Monitor izle
□ Task Monitor: Max Cycle Time < Cycle Time × 0.70 (Exec% < %70)
□ Güç kesme testi: IPC kapandıktan sonra boot + runtime otomatik başlamalı
□ Ağ kesinti testi: IT NIC çekildiğinde fieldbus programı devam etmeli
□ Lisans doğrulama: IDE → License Manager → geçerlilik tarihi kontrol
□ 24 saat kesintisiz cyclictest çalıştır; max jitter spike izle
```

## Sık Yapılan Hatalar

**1. CodeMeter-Lite Kurulmadan CODESYS Control Yüklemeye Çalışmak (Belge 01)**
`dpkg -i codesyscontrol*.deb` bağımlılık hatası verir. Önce `codemeter-lite*.deb` kurulmalı, sonra CODESYS Control.

**2. Demo Modda Teslim (Belge 01)**
Runtime lisans yoksa 2 saat sonra durur. Fabrikada üretim hattı çöker. Devreye alma kontrol listesine "Lisans doğrulama" adımı eklenmeli; IDE → License Manager → geçerlilik tarihi teyit edilmeli.

**3. Gateway'i Tüm Arayüzlerden Yayınlamak (Belge 01 + 02)**
`[SysSocket]` boş bırakılırsa gateway tüm NIC'lerden erişilebilir olur. Güvenlik açığı. `Adapter.0.Name=enp2s0` ile yalnızca IT NIC'ine kısıtlanmalı.

**4. CmpBlkDrvUdp'yi Tüm Arayüzlerde Açık Bırakmak (Belge 02)**
Varsayılan ayar UDP 1740-1743'ü tüm NIC'lerden yayar. Kaspersky ICS CERT (2019) araştırmasına göre bu, IP spoofing için saldırı yüzeyi oluşturur. `MaxInterfaces=1` ile IT NIC'ine kısıtla.

**5. İki NIC'e Aynı Anda İki Varsayılan Rota Tanımlamak (Belge 02)**
Fieldbus NIC'inde de `to: default` varsa dönüş trafiği yanlış arayüzden çıkar. Varsayılan rota yalnızca IT NIC'inde tanımlanmalı; fieldbus NIC'i subnet rotasını kernel otomatik yönlendirir.

**6. PROFINET ve EtherCAT'i Aynı NIC'te Çalıştırmaya Çalışmak (Belge 02)**
Her ikisi de SysEthernet'e özel erişim gerektirir; birlikte aynı NIC'te çalışamazlar. Her fieldbus protokolü için ayrı fiziksel NIC zorunludur.

**7. PREEMPT_RT Kernel Kurulmadan RT Performansı Beklemek (Belge 03)**
Standart kernel ile cyclictest max gecikme 10 ms+ olabilir. `uname -r` çıktısında "-rt" görünmüyorsa gerçek zamanlı çalışılmıyor demektir.

**8. isolcpus Ayarlanıp irqbalance Kapatılmamak (Belge 03)**
irqbalance periyodik olarak IRQ'ları izole çekirdeklere taşır ve jitter artar. `systemctl disable irqbalance` zorunludur.

**9. RT Throttling Aktifken Yüksek Yükte Görev Askıya Alınması (Belge 03)**
`sched_rt_runtime_us` varsayılan 950000 değeriyle RT thread saniyenin %95'ini kullanabilir; kota dolunca CODESYS görevi log'da hata göstermeden askıya alınır. `echo -1` ile kaldırılmalı.

**10. SL Lisansla taskset ile Affinity Denemesi (Belge 03)**
CODESYS Forge bildirimleri SL lisanslarda `taskset` atamasının geçici çalıştığını ancak runtime'ın core 0'a dönebildiğini gösterir. Güvenilir CPU pinleme için Multicore (MC) Lisansı gereklidir.

**11. Soft Container Lisansını NIC Değişiminden Korumamak (Belge 01)**
Soft Container lisansı MAC adresine bağlıdır; NIC değişimi lisansı geçersiz kılar. Kritik sistemlerde dongle lisansı kullanılmalı; her durumda `.WibuCmRaC` yedek dosyası güvenli konumda tutulmalı.

**12. Netplan Dosyasında Sekme (Tab) Kullanımı (Belge 02)**
YAML'da girinti için sekme kullanılırsa "Invalid YAML" hatası alınır. Yalnızca 2 boşluk kullanılmalı.

## Ne Zaman ...

### Ne Zaman Linux SL, Ne Zaman Windows SL/RTE?

| Durum | Tercih | Gerekçe (Kaynak) |
|---|---|---|
| Yeni proje, maliyet odaklı | Linux SL | İşletim sistemi lisansı yok; PREEMPT_RT ücretsiz (Belge 01) |
| EtherCAT / PROFINET kritik | Linux SL | PREEMPT_RT jitter Windows Win SL'den genellikle daha iyi (Belge 01) |
| ARM tabanlı IPC | Linux SL | Linux ARM desteği olgun; Windows ARM OT ekosistemi zayıf (Belge 01) |
| Mevcut Windows altyapısı | Windows Win SL | Ekip bilgisi, Active Directory entegrasyonu (Belge 01) |
| HMI aynı IPC'de | Windows Win SL | TwinCAT HMI, WinCC vb. Windows gerektirir (Belge 01) |
| Windows + µs-düzey jitter | Windows RTE SL | Win SL yetersiz kalıyorsa kendi RT çekirdeği (Belge 01) |
| Hızlı prototip | Win SL / Virtual SL | Geliştirici kendi PC'sinde anında test yapabilir (Belge 01) |
| SIL 2/3 güvenlik | **Hiçbiri** | Standart CODESYS SIL sertifikalı değil; CODESYS Safety veya sertifikalı donanım PLC |

### Ne Zaman Performans Tuning Zorunludur?

- **EtherCAT / PROFINET RT master**: 250µs veya daha düşük döngülü fieldbus için optimizasyonsuz güvenilir çalışmaz (Belge 03)
- **Servo/Motion kontrol**: 1–4ms döngü, ±0.1ms jitter toleransı (Belge 03)
- **Çok eksenli µs-senkronizasyon**: Her zaman zorunlu (Belge 03)
- **250ms veya daha uzun döngülü izleme**: Gereksiz karmaşıklık; atlana bilir (Belge 03)
- **Geliştirme/test PC'si**: BIOS erişimi kısıtlı; kısmi uygulama yeterli (Belge 03)

### Ne Zaman Çift NIC Zorunludur?

- Fieldbus (EtherCAT/PROFINET) + IT trafiği birlikte varsa: Her zaman (Belge 02)
- IEC 62443 uyumluluk gereksinimi: Fiziksel veya mantıksal ayrım zorunlu (Belge 02)
- Aynı IPC'de birden fazla fieldbus protokolü: Her biri için ayrı NIC şart (Belge 02)
- Yalnızca Modbus/TCP veya OPC UA (fieldbus yok): Tek NIC kabul edilebilir (Belge 02)

## Gerçek Proje Notları

**Not 1 — Sıralı Optimizasyon Veri Noktaları (Belge 03)**
10ms PROFINET döngülü dozaj pompası projesi. Adım adım cyclictest ölçümleri: BIOS C-state kapatma → 180µs'den 90µs'ye. PREEMPT_RT + isolcpus → 39µs. irqbalance kaldırma + IRQ yönlendirme → 22µs. SchedulerInterval=200 → 18µs. Son değer 10ms döngü için fazlasıyla yeterli; Task Monitor Max Cycle Time ≤ 3ms (%30 Exec%). Bu ölçümler optimizasyon sırasının önemini kanıtlar: hiçbir adım atlanmamalı.

**Not 2 — Interface İsminin Değişmesi Riski (Belge 02)**
Bir projede yeni NIC kartı eklenince arayüz ismi değişti (enp2s0 → enp3s0). `CODESYSControl.cfg`'deki `Adapter.0.Name` geçersiz kaldı ve fieldbus kesildi. Çözüm: netplan `match.macaddress + set-name` ile NIC'e kalıcı isim atamak. `CODESYSControl.cfg` sabit kalır, donanım değişimi ağ yapılandırmasını bozmaz.

**Not 3 — RT Throttling Sessiz Kilidi (Belge 03)**
Bir motion uygulamasında IEC görevleri yük eşiğinde 5–10ms askıya alınıyordu; CODESYS log ve `journalctl` sessizdi. `perf sched` incelemesinde RT kota doluluğu tespit edildi. `echo -1 > /proc/sys/kernel/sched_rt_runtime_us` ile düzeltildi. Bu ayar devreye alma kontrol listesine eklenmeli.

**Not 4 — Deploy Tool SSH Root Reddi (Belge 01)**
Ubuntu 22.04 varsayılan olarak root SSH girişini engeller. Deploy Tool root ile bağlanmaya çalışırsa hata alır. Ya `PermitRootLogin yes` ayarlanır (güvenlik riski) ya da sudo yetkili kullanıcıyla manuel dpkg kurulumu tercih edilir.

**Not 5 — Lisans Sunucusu Çevrimdışıyken Devreye Alma (Belge 01)**
Bir devreye alma anında CODESYS lisans sunucusu erişilemezdi. Önceden hazırlanan `.WibuCmRaC` istek dosyasıyla offline aktivasyon tamamlandı. Her proje için offline aktivasyon prosedürü önceden hazır tutulmalı.

**Not 6 — CmpBlkDrvUdp Kapatıldığında IDE Scan Network Çalışmaz (Belge 02)**
`MaxInterfaces=0` ile UDP block driver kapatılırsa CODESYS IDE "Scan Network" ile IPC'yi otomatik bulamaz. Yalnızca direkt TCP (IP:11740) çalışır. Güvenli izole ortamlarda tercih edilebilir; tüm geliştiricilerin manuel IP:port girişini bilmesi gerekir.

**Not 7 — EtherCAT NIC IRQ'su İzole Çekirdeğe Yönlendirilmemelidir (Belge 03)**
EtherCAT NIC IRQ'su yanlışlıkla izole çekirdeğe (core 3) yönlendirilince EtherCAT sync kayıpları yaşandı. Düzeltme: EtherCAT NIC IRQ'su housekeeping çekirdeğine (core 0-1) bırakılmalı; EtherCAT görev thread'i ise izole çekirdeğe pinlenmeli. IRQ yönlendirme ile thread pinleme iki ayrı kavramdır.

**Not 8 — Multicore Lisansının Önemi (Belge 03)**
SL lisanslı 4-çekirdekli sistemde `taskset` ile affinity denenince görünürde çalıştı ancak periyodik jitter spike'ları devam etti. MC deneme lisansıyla Task Groups ataması yapılınca RT görev Core 3'e gerçekten kilitlendi, spike'lar tamamen ortadan kalktı. Performans kritik projelerde MC lisansı başlangıçtan itibaren bütçeye dahil edilmeli.

## İlgili Konular

```
knowledge/hardware/industrial-pc/      ← Şu an buradasınız
├── 01_codesys_runtime_setup.md        → Runtime kurulumu detayları
├── 02_network_config.md               → Ağ yapılandırması detayları
├── 03_performance_tuning.md           → Performans tuning detayları
└── _synthesis.md (bu belge)

Önkoşul:
knowledge/codesys/fundamentals/
├── 01_runtime_architecture.md         → CODESYS runtime iç mimarisi, jitter/CPU genel model
└── _synthesis.md                      → CODESYS temel kavramlar özeti

Sonraki adım — Protokoller:
knowledge/protocols/
├── ethercat/                          → EtherCAT master yapılandırması
├── opc-ua/                            → OPC UA server kurulumu ve güvenliği
└── modbus/                            → Modbus TCP/RTU yapılandırması

Sonraki adım — Ağ:
knowledge/networking/
├── 01_topologies.md                   → Yıldız, ring, hat topoloji seçimi
└── 02_security.md                     → IEC 62443, OT/IT güvenlik mimarisi

Sonraki adım — CODESYS İleri:
knowledge/codesys/
├── task-structure/02_cycle_time.md    → Task cycle time ve watchdog yapılandırması
└── softmotion/                        → Servo motion control

Güvenlik ve Standartlar:
knowledge/standards/
├── safety_plc/                        → SIL, IEC 61508
└── cybersecurity/                     → IEC 62443, endüstriyel ağ güvenliği
```
