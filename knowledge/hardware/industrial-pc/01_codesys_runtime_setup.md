---
KONU        : Endüstriyel PC'ye CODESYS Runtime Kurulumu
KATEGORİ    : hardware
ALT_KATEGORI: industrial-pc
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Control/_rtsl_install_runtime_on_controller.html"
    başlık: "CODESYS Control — Installing the Runtime on the Controller (Resmi Dokümantasyon)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Control/_rtsl_start_page.html"
    başlık: "CODESYS Control — Start Page (Resmi Dokümantasyon)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_installing_license.html"
    başlık: "CODESYS — Licensing of Products (Resmi Dokümantasyon)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Control/_rtsl_linux_installation_without_pm.html"
    başlık: "CODESYS — Installing SL Products without a Package Manager (Resmi Dokümantasyon)"
    güvenilirlik: resmi
  - url: "https://store.codesys.com/en/codesys-control-linux-sl-1.html"
    başlık: "CODESYS Store — CODESYS Control for Linux SL Ürün Sayfası"
    güvenilirlik: resmi
  - url: "https://store.codesys.com/en/codesys-control-win-sl-1.html"
    başlık: "CODESYS Store — CODESYS Control Win SL Ürün Sayfası"
    güvenilirlik: resmi
  - url: "https://store.codesys.com/en/howto_applicationbasedlicenses"
    başlık: "CODESYS Store — Application-Based Licenses Açıklaması"
    güvenilirlik: resmi
  - url: "https://github.com/tobias-carlbom/codesys-control-linux-sl"
    başlık: "GitHub — codesys-control-linux-sl Kurulum Rehberi (Topluluk)"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Runtime/thread/0a515ced3f/"
    başlık: "CODESYS Forge — Getting Started with CODESYS Control for Linux SL (Forum)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: gerektirir
  - konu: "knowledge/hardware/industrial-pc/02_network_config.md"
    ilişki: tamamlar
  - konu: "knowledge/hardware/industrial-pc/03_performance_tuning.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "CODESYS Runtime mimarisinin temel kavramları (SoftPLC, Task, Scan Cycle) — bkz. knowledge/codesys/fundamentals/01_runtime_architecture.md"
  - "Linux sistem yönetiminin temelleri (systemctl, dpkg, dosya izinleri)"
  - "Endüstriyel PC'ye Ubuntu 22.04 LTS veya Debian 12 kurulu olmalı"
ÇELİŞKİLER :
  - kaynak: "CODESYS Forge forum (topluluk) vs Resmi Dokümantasyon"
    konu: "Deploy Tool kullanımı ile manuel dpkg kurulumu arasındaki tercih"
    çözüm: >
      CODESYS v4.14+ ile gelen Deploy Tool, SSH üzerinden IDE'den doğrudan kurulumu yönetir
      ve önerilen yoldur. Ancak IDE erişimi olmayan headless ortamlarda veya otomasyon
      pipeline'larında dpkg ile manuel kurulum tercih edilebilir. Her iki yol da resmi
      dokümantasyonda yer almaktadır; proje koşuluna göre seçilmeli.
  - kaynak: "CODESYS Resmi Dokümantasyon"
    konu: "CODESYSControl.cfg dosya yolu: /etc/CODESYSControl.cfg vs /etc/codesyscontrol/CODESYSControl.cfg"
    çözüm: >
      Resmi dokümantasyon ve forum kaynakları iki farklı yol belirtiyor. Gerçek kurulumda
      paket /etc/codesyscontrol/ altında oluşturur; ancak servis binary'si /etc/CODESYSControl.cfg
      referansını da destekler. Kurulum sonrası `systemctl status codesyscontrol` çıktısında
      hangi yolun kullanıldığı görülür; her iki yol symlink ile uyumlu kılınabilir.
---

## Özün Ne

CODESYS Control, endüstriyel bir PC'yi IEC 61131-3 uyumlu SoftPLC'ye dönüştüren runtime yazılımıdır. Bir PC'nin "akıllı makine" değil, "kontrolcü" işlevi görmesi için gereken yazılım katmanıdır. Resmi terminolojide iki ana varyant öne çıkar: **CODESYS Control Linux SL** (Linux tabanlı, üretim tercihli) ve **CODESYS Control Win SL** (Windows tabanlı, geliştirme/test odaklı); üretim ortamında gerçek zamanlı performans için **CODESYS Control RTE SL** (Windows + yerleşik RT çekirdeği) üçüncü seçenektir.

Bu belge; bu runtime'ların fiziksel bir endüstriyel PC üzerine kurulmasını, sisteme servis olarak entegre edilmesini, lisanslanmasını ve IDE üzerinden ilk bağlantının kurulmasını adım adım ele alır. Kurulum, bir sonraki aşamaların (ağ yapılandırması, RT performans tuning) temelidir.

## Nasıl Çalışır

### Runtime Türleri ve Seçim Kriterleri

| Varyant | Platform | Gerçek Zamanlılık | Lisans | Tipik Kullanım |
|---|---|---|---|---|
| CODESYS Control **Linux SL** | Linux (x86/ARM) | Soft-RT (standart kernel) / Hard-RT (PREEMPT_RT) | Ücretli SL lisansı | Üretim IPC, embedded Linux |
| CODESYS Control **Win SL** | Windows x86/x64 | Soft-RT (Windows scheduler) | Ücretli SL lisansı | Geliştirme, test, non-critical |
| CODESYS Control **RTE SL** | Windows + RT Extension | Hard-RT (kendi RT çekirdeği, µs jitter) | Ayrı RTE lisansı | Yüksek performanslı Windows IPC |
| CODESYS Control **Virtual SL** | Container / Docker | Soft-RT | Ücretli SL lisansı | Bulut, sanal test |

CODESYS'in resmi dokümantasyonuna göre port tablosu şöyledir:
- **1217/TCP**: Gateway bağlantı portu (IDE ↔ Runtime)
- **1740–1743/UDP**: Block driver tarama portları
- **11740–11743/TCP**: TCP block driver portları
- **4840/TCP**: OPC UA sunucusu
- **8080/TCP**: Web sunucusu (WebVisu)
- **22/TCP**: SSH (Linux kurulum/güncelleme)

### Lisans Mimarisi

CODESYS lisanslama sistemi **CodeMeter** (WibuSystems) altyapısını kullanır. Lisans türleri:

```
Lisans Türleri:
├── Soft Container (CmSoftLicense)   → Donanım MAC adresine bağlı, yazılımsal
├── CmActLicense                     → Activation-based, çevrimiçi aktivasyon
└── Dongle (CmDongle, USB)           → Donanım bağımsız, taşınabilir
```

**Demo Modu**: Lisans yoksa runtime **2 saat** çalışır, ardından durur. Yeniden başlatılabilir, yani test için sınırsız kullanılabilir; üretimde kesinlikle lisans gerekir.

**Önemli**: Soft Container lisansı NIC'in MAC adresine bağlanır. Ağ kartı değişirse lisans geçersiz kalır. Kritik üretim sistemlerinde dongle tercih edilmeli.

### Kurulum Akışı

```
CODESYS IDE (Geliştirme PC)
        │
        │  1. Package Manager: "CODESYS Control for Linux SL" eklentisi yüklü?
        │  2. Deploy Tool (v4.14+) VEYA manuel dpkg
        │
        ▼
Endüstriyel PC (Hedef)
        │
        ├─ /opt/codesys/bin/codesyscontrol.bin    ← Runtime binary
        ├─ /etc/codesyscontrol/CODESYSControl.cfg  ← Ana konfigürasyon
        ├─ /etc/codesyscontrol/CODESYSControl_User.cfg ← Kullanıcı override
        └─ /var/opt/codesys/                       ← Lisans ve veri dizini
```

## Pratikte Nasıl Kullanılır

### Yöntem A: Deploy Tool ile Kurulum (Önerilen, v4.14+)

CODESYS IDE'de (geliştirme PC'de):

```
1. Tools → Package Manager →
   "CODESYS Control for Linux SL" paketini yükle → IDE'yi yeniden başlat

2. Tools → Deploy Control SL →
   SSH Adres : 192.168.1.100
   SSH Kullanıcı : root  (veya sudo yetkili kullanıcı)
   SSH Şifre : ***
   Ürün : "CODESYS Control for Linux SL" → İlgili versiyon seç
   → Install düğmesine bas
   → Runtime hedef PC'ye otomatik kurulur ve yeniden başlatılır
```

### Yöntem B: Manuel dpkg Kurulumu (Headless / CI ortamı)

Hedef Linux PC üzerinde (SSH veya doğrudan terminal):

```bash
# 1. Bağımlılıkları kontrol et / yükle
sudo apt-get update
sudo apt-get install -y libssl-dev

# 2. CodeMeter-Lite (lisans yöneticisi) bağımlılığını yükle
# Dosya, CODESYS IDE kurulumundan veya CODESYS Store'dan indirilir
sudo dpkg -i codemeter-lite_<Version>_amd64.deb
sudo systemctl start CodeMeter

# 3. CODESYS Control for Linux SL paketini yükle
sudo dpkg -i codesyscontrol_linux_<Version>_amd64.deb

# 4. Servis başlatma
sudo systemctl daemon-reload
sudo systemctl enable codesyscontrol
sudo systemctl start codesyscontrol

# 5. Servis durumu doğrulama
sudo systemctl status codesyscontrol
# Çıktıda: "Active: active (running)" görülmeli

# 6. Logları izle
sudo journalctl -u codesyscontrol -f
```

### CODESYSControl.cfg Temel Yapılandırması

Dosya konumu (kurulum sonrası): `/etc/codesyscontrol/CODESYSControl.cfg`

```ini
; CODESYS Control Linux SL — Temel Konfigürasyon
; (Kaynak: CODESYS Resmi Dokümantasyonu + toradex/codesys GitHub referans CFG)

[CmpGwServer]
; Gateway portu — IDE bu port üzerinden bağlanır
; Varsayılan: 1217
Port=1217

[SysSocket]
; Hangi ağ arayüzünden gateway sunulacak?
; Boş bırakılırsa tüm arayüzlerden dinler (güvenlik açığı!)
; Üretimde: sadece programlama NIC'ini belirt
; Adapter.0.Name=eth1

[SysProcess]
; Runtime ana thread'inin Linux gerçek zamanlı önceliği
; (PREEMPT_RT kernel ile anlamlıdır)
; RealTimePriority=79

[SysCpuHandling]
; CPU DMA gecikme yönetimi — v4.11.0.0'dan itibaren varsayılan olarak 1
; Gerçek zamanlılık için bu değer 1 olmalı
Linux.DisableCpuDmaLatency=1

[CmpSchedule]
; Görev zamanlayıcı çözünürlüğü (mikrosaniye)
; 1000 µs = 1 ms (varsayılan)
SchedulerInterval=1000

[CmpApp]
; Boot davranışı: 1 = son uygulama her zaman başlatılır
Bootproject.RetainMismatch.Init=1

[SysExcept]
; FPU istisnalarını devre dışı bırak (Linux standart davranış)
Linux.DisableFpuUnderflowException=1
Linux.DisableFpuOverflowException=1

[CmpLog]
; Log düzeyi: 4=Info, 6=Debug (üretimde 4 yeterli)
; Logger.0.Name=Sys
; Logger.0.Enable=1
; Logger.0.MaxEntries=10000
```

**Önemli**: Değişiklikler sonrası runtime'ı yeniden başlat:
```bash
sudo systemctl restart codesyscontrol
```

### Lisans Aktivasyonu

**Online Aktivasyon (Geliştirme PC'nin interneti olması yeterli):**

```
CODESYS IDE (geliştirme PC'de):
  Tools → License Manager →
    Target: [Runtime'ın çalıştığı IPC seçilir]
    → "Activate License" → Aktivasyon kodu gir
    → IDE, lisans sunucusuna bağlanarak lisansı IPC'nin CodeMeter container'ına yükler
```

**Offline Aktivasyon (Air-gap ortamı):**

```
1. IDE'de: License Manager → "Create License Request File" → .WibuCmRaC oluştur
2. Bu dosyayı internete erişen bir PC'ye taşı
3. https://license.codesys.com adresine git → dosyayı yükle → .WibuCmRaU indir
4. .WibuCmRaU dosyasını IPC'ye taşı → IDE License Manager → "Apply License Update"
```

### İlk Bağlantı (IDE → Runtime)

```
CODESYS Development System IDE'de:
  1. Tools → Communication Settings
     → "Add Gateway" → TCP/IP → IP: 192.168.1.100, Port: 1217
  2. Gateway üzerinde "Scan Network" yap → IPC görünmeli
  3. Cihaza çift tıkla → "Connect"
  4. Login → uygulama yükle (Download) → Start
```

Gateway bağlantısı başarısız olursa:
```bash
# IPC üzerinde portun açık olduğunu doğrula
ss -tlnp | grep 1217
# Port kapalıysa runtime çalışmıyordur:
sudo systemctl status codesyscontrol
```

### Windows SL Kurulumu (Kısa Özet)

CODESYS Development System kurulumunda **Win SL kısıtlı sürümü otomatik yüklenir** (test için). Tam sürüm için:

```
1. CODESYS Store'dan CODESYS Control Win SL indirin ve kurulum sihirbazını çalıştırın
2. Kurulum sonrası sistem tepsisinde CODESYS sembolü görünür
3. Sağ tık → "PLC Configuration" → ağ arayüzü ve port yapılandırması
4. Service olarak otomatik başlar; Windows Services'ten "CODESYS Control Win SL" yönetilebilir
5. IDE'den localhost:1217 üzerinden bağlanılır
```

## Örnekler

### Örnek 1: Kurulum Sonrası Doğrulama Komutları

```bash
# Runtime çalışıyor mu?
sudo systemctl status codesyscontrol

# Beklenen çıktı:
# ● codesyscontrol.service - CODESYS Control for Linux SL
#    Active: active (running) since Mon 2026-06-08 10:30:00 UTC; 5min ago
#    Main PID: 1234 (codesyscontrol)

# Gateway portu dinleniyor mu?
ss -tlnp | grep 1217
# Beklenen çıktı: LISTEN  0  128  0.0.0.0:1217  0.0.0.0:*

# Runtime sürüm bilgisi (IDE'den bağlandıktan sonra PLC Shell):
# > version
# CODESYS Control for Linux SL V4.x.x.x
```

### Örnek 2: Systemd Servis Override — Ağ Hazır Olmadan Başlama Sorunu

Eğer runtime ağ arayüzleri hazır olmadan başlarsa gateway bind hatası verir. Çözüm:

```bash
sudo mkdir -p /etc/systemd/system/codesyscontrol.service.d/
sudo nano /etc/systemd/system/codesyscontrol.service.d/override.conf
```

İçerik:
```ini
[Unit]
After=network-online.target
Wants=network-online.target
```

Uygulamak:
```bash
sudo systemctl daemon-reload
sudo systemctl restart codesyscontrol
```

### Örnek 3: Demo Mod Tespiti ve Acil Yeniden Başlatma

```bash
# 2 saat sonra runtime durmuşsa log'da görülür:
sudo journalctl -u codesyscontrol --since "1 hour ago" | grep -i "demo\|license\|stop"

# Demo modda acil yeniden başlatma (lisans aktivasyonuna kadar geçici çözüm):
sudo systemctl restart codesyscontrol
```

### Örnek 4: Birden Fazla IPC'ye Aynı Konfigürasyonu Dağıtmak (Ansible Snippet)

```yaml
# ansible/roles/codesys_runtime/tasks/main.yml
- name: CODESYS Control deb paketini kopyala
  copy:
    src: codesyscontrol_linux_4.x_amd64.deb
    dest: /tmp/codesyscontrol.deb

- name: Runtime'ı yükle
  apt:
    deb: /tmp/codesyscontrol.deb

- name: CODESYSControl.cfg kopyala
  template:
    src: CODESYSControl.cfg.j2
    dest: /etc/codesyscontrol/CODESYSControl.cfg
    mode: '0644'

- name: Servisi etkinleştir ve başlat
  systemd:
    name: codesyscontrol
    enabled: true
    state: started
```

## Sık Yapılan Hatalar

### Hata 1: Codemeter-Lite Yüklenmeden Runtime Kurulumu

```
❌ Yanlış:
sudo dpkg -i codesyscontrol_linux_4.x_amd64.deb
# Hata: dependency "codemeter-lite" is not satisfied

✅ Doğru:
# Önce CodeMeter-Lite, sonra CODESYS Control:
sudo dpkg -i codemeter-lite_<Version>_amd64.deb
sudo dpkg -i codesyscontrol_linux_4.x_amd64.deb
```

### Hata 2: Lisansı Teslimatta Aktive Etmemek

```
Semptom: Fabrikada 2 saat sonra IPC durdu, üretim hattı çöktü.
Neden  : Demo modda teslim edilmiş.
Çözüm  : Devreye alma kontrol listesine "lisans doğrulama" adımı ekle.
          IDE → License Manager → Lisans geçerlilik tarihini kontrol et.
```

### Hata 3: Gateway'i Tüm Arayüzlerden Yayınlamak

```ini
; ❌ Yanlış — gateway tüm NIC'lerden erişilebilir
[SysSocket]
; Boş bırakılmış

; ✅ Doğru — gateway yalnızca programlama NIC'inden
[SysSocket]
Adapter.0.Name=eth1    ; SCADA/programlama arayüzü
```

### Hata 4: Runtime'ı Grafik Arayüzlü (GUI) OS'de Çalıştırmak

X11 ve masaüstü bileşenleri RT olmayan thread'lerle CPU paylaşır, jitter artar. Üretim IPC'lerinde mutlaka `server` kurulumu yapılmalı, GUI yüklenmemeli.

```bash
# GUI yüklü mü kontrol:
dpkg -l | grep xorg
# Eğer yüklüyse ve üretimdeyse kaldır:
sudo apt-get remove --purge xorg xserver-xorg
```

### Hata 5: Soft Container Lisansını Yedeklememek

Soft Container lisansı, CodeMeter tarafından v3.5 SP13+ sürümlerinde `.WibuCmRau` backup dosyası olarak otomatik oluşturulur. Bu dosya kaybolursa lisans yeniden aktive edilmesi gerekir. Her IPC için bu dosyayı güvenli bir lokasyona yedekle.

### Hata 6: MAC Adresine Bağlı Lisansla NIC Değişimi

```
Senaryo: Arızalanan NIC kartı değiştirildi → Runtime lisansı geçersiz oldu.
Çözüm  : Kritik sistemlerde dongle lisansı kullan (MAC'ten bağımsız).
          Dongle fiziksel USB üzerinde taşınır; kart değişimi lisansı etkilemez.
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Linux SL Tercih Edilmeli

- **Yeni proje, düşük maliyet**: İşletim sistemi lisans maliyeti yok; PREEMPT_RT ücretsiz.
- **EtherCAT / kritik fieldbus**: Linux PREEMPT_RT çekirdeği ile jitter tipik olarak Windows Win SL'den daha iyi.
- **Uzun ömürlü proje**: Ubuntu LTS / Debian long-term support ile 5+ yıl güvenli destek.
- **ARM tabanlı IPC**: Linux ARM desteği olgun; Windows ARM otomasyon ekosistemi zayıf.

### Win SL Tercih Edilmeli

- **Mevcut Windows altyapısı**: Ekip Windows biliyor, Active Directory entegrasyonu gerekiyor.
- **HMI aynı PC'de**: Beckhoff TwinCAT HMI, WinCC vb. Windows gerektiriyor.
- **Hızlı prototip**: Geliştirici kendi PC'sinde Win SL ile anında test yapabilir.

### RTE SL Tercih Edilmeli

- **Windows'ta hard-RT zorunlu**: Win SL'nin yetersiz kaldığı µs-düzey jitter gereksinimleri.
- **Büyük Windows ekosistemi + yüksek RT**: Fabrika Windows bilgisi var ama RT performance kritik.

### Hiçbiri Tercih Edilmemeli

- **SIL 2/3 fonksiyonel güvenlik** gerektiriyorsa: Standart CODESYS SIL sertifikalı değil; `CODESYS Safety` veya ayrı sertifikalı donanım PLC gerekir.
- **RAM < 256 MB, CPU < 500 MHz**: Runtime ayak izi küçük olmayan gömülü sistemlerde Raspberry Pi SL veya firmware PLC daha uygun.

## Gerçek Proje Notları

**Not 1 — Deploy Tool SSH Root Reddi**
Ubuntu 22.04 varsayılan olarak root SSH girişini engeller. Deploy Tool root ile bağlanmaya çalışırsa hata alır. Çözüm: `/etc/ssh/sshd_config` içinde `PermitRootLogin yes` yapılabilir (güvenlik riski), ya da sudo yetkili kullanıcı ile bağlanıp manuel kurulum tercih edilir.

**Not 2 — systemd Boot Sırası Tuzağı**
Runtime servis dosyası `After=network.target` ile ağı bekleyebilir; ancak `network.target` ağ arayüzlerinin UP olduğunu garanti etmez. `network-online.target` ile birlikte kullanmak gerekir (bkz. Örnek 2). Bu ayar yapılmadan bazı sistemlerde runtime boot'ta gateway'i bind edemiyor ve sessizce başarısız oluyor.

**Not 3 — v4.14 Deploy Tool Öncesi Eski Yöntem**
v4.14 öncesinde `Tools → Update Linux` menüsü kullanılırdı; bazı topluluк kaynakları hâlâ bu yöntemi anlatıyor. Yeni kurulumlarda Deploy Tool kullanılmalı. Eski `Update Linux` aracı deprecated (kullanımdan kaldırılmış) olabilir.

**Not 4 — Lisans Sunucusunun Çevrimdışı Olması**
Bir devreye alma anında CODESYS lisans sunucusu erişilemezdi. Acil çözüm: daha önce oluşturulan `.WibuCmRaC` istek dosyası ile offline aktivasyon tamamlandı. Bu nedenle her proje için offline aktivasyon prosedürü önceden hazır tutulmalı.

**Not 5 — Windows Update ve Win SL**
Win SL ile test ortamı kuran bir ekip, gece otomatik Windows Update tetiklenmesi ve servis yeniden başlaması nedeniyle test sürecini kaybetti. Üretimde veya uzun süreli test ortamlarında Windows Update otomatik güncelleme **mutlaka devre dışı** bırakılmalı.

**Not 6 — CodeMeter Servisi Boot Yarışı (Race Condition)**
Bir IPC'de runtime boot'ta sporadik olarak demo moduna düşüyordu; yeniden başlatınca lisans bulunuyordu. Kök neden: `codesyscontrol.service` ile `codemeter.service` aynı anda başlatılıyor, runtime CodeMeter container'ı henüz hazır olmadan lisansı sorguluyordu. CodeMeter ilk açılışta lisans dosyalarını okuyup CmContainer'ı RAM'e map ediyor; bu birkaç yüz ms sürüyor. Çözüm: override.conf içine `After=codemeter.service` + `Requires=codemeter.service` eklemek. `systemctl list-dependencies codesyscontrol` ile bağımlılık zincirini doğrula. Bu yarış özellikle SSD'li hızlı boot eden sistemlerde daha sık görülür çünkü servisler neredeyse eşzamanlı başlar.

**Not 7 — apt full-upgrade Runtime Binary'sini Değiştirmedi ama .cfg'yi Ezdi**
Bir bakım penceresinde `apt full-upgrade` çalıştırıldığında CODESYS deb paketi güncellendi; paketin postinst scripti `/etc/codesyscontrol/CODESYSControl.cfg` dosyasını **dağıtılan varsayılan ile değiştirdi** (dpkg conffile davranışı değil, manuel kopyalama yapıyor). Sonuç: tüm NIC/affinity/RT ayarları kayboldu, runtime tüm arayüzlerden gateway yayınlamaya başladı. Ders: özel ayarlar `CODESYSControl_User.cfg` (override dosyası) içinde tutulmalı — bu dosya paket güncellemesinde korunur. Ana `.cfg` dosyasını minimum tutup tüm site-özel ayarları User.cfg'ye taşı. Güncelleme öncesi her iki dosyayı da yedekle.

**Not 8 — Sürüm Farkı: v4.x ile v3.5 Servis Adı ve Binary Yolu**
Eski projelerde CODESYS Control V3 (`/opt/codesys/...`, servis `codesyscontrol`) ile yeni V4 SL (Deploy Tool ile gelen, bazı dağıtımlarda `codesyscontrol_*` instance bazlı servis isimleri) karıştırılıyor. V4 SL'de birden fazla runtime instance aynı IPC'de çalışabilir; her instance kendi config dizinine (`/var/opt/codesys/<instance>/`) sahiptir. Eski script'lerde sabit kodlanmış `/etc/codesyscontrol/CODESYSControl.cfg` yolu V4 multi-instance kurulumda yanlış instance'ı hedefleyebilir. Devreye almadan önce `systemctl status` ve `ps aux | grep codesys` ile gerçek binary yolu ve config dizini teyit edilmeli.

## Edge Case'ler ve Sistem Limitleri

CODESYS runtime kurulumu "çalışıyor / çalışmıyor" ikiliğinin ötesinde, sınır koşullarında öngörülemeyen davranışlar sergiler. Aşağıdaki tablo saha deneyiminde karşılaşılan limit ve edge case'leri özetler:

| Edge Case | Davranış | Limit / Eşik | Önlem |
|---|---|---|---|
| Demo mod expiry tam saat sınırında | Runtime 2 saatte tam durur; uygulama çıkışları **son değerde donar** (fail-safe değil) | 7200 s ± birkaç s | Demo modda asla fiziksel aktüatör bağlama |
| CodeMeter container bozulması | Lisans "geçersiz" değil "bulunamadı" olur; demo'ya düşer | `.WibuCmRaU` corrupt | `cmu --list-content` ile container bütünlüğü kontrol |
| Sistem saati geriye atlaması (NTP düzeltmesi) | CmActLicense süreli lisanslarda lisans erken bitebilir | Saat farkı > lisans toleransı | `timedatectl set-ntp` boot'ta, lisans aktivasyonundan önce |
| Disk doluluğu (`/var/opt/codesys` %100) | Boot project yazılamaz; runtime başlar ama uygulama yüklenemez | inode veya blok tükenmesi | `/var` ayrı partition + monitoring |
| Çok küçük RAM (< 512 MB) | Runtime başlar ama büyük uygulama RETAIN bölgesi alloc edemez | platform bağımlı | Hedef RAM ≥ 1 GB önerilir |
| 32-bit vs 64-bit deb karışımı | `dpkg` mimari uyumsuzluğunda sessizce yanlış paket | `dpkg --print-architecture` | Mimariyi kurulumdan önce doğrula |
| Saat dilimi / UTC karmaşası | Log timestamp'leri ve RTC tabanlı zamanlayıcılar kayar | yerel saat vs UTC | IPC'leri UTC'de tut, SCADA'da çevir |

**Lisans modeli sınırları:** Soft Container lisansı yalnızca *ilk* NIC'in (genelde en düşük PCI/bus numaralı) MAC adresine bağlanır. IPC'de birden fazla NIC varsa, BIOS/kernel'ın NIC enumerasyon sırası değiştiğinde (BIOS update, NIC ekleme) "ilk NIC" değişebilir ve lisans geçersiz olur. Bu, fiziksel olarak NIC değişmese bile yaşanabilen sinsi bir durumdur.

**Demo mod ve fonksiyonel güvenlik:** Demo modda çalışan runtime durduğunda çıkışlar fail-safe değildir; PROFIsafe/FSoE gibi güvenlik katmanları olmadan çıkışlar son değerde kalır. Bu, demo modda sahada fiziksel test yapmanın neden tehlikeli olduğunun teknik gerekçesidir.

## Optimizasyon

Kurulum aşamasında alınan kararlar, sonraki performans ve güvenlik aşamalarının tavanını belirler. Kurulumu "ilk seferde doğru" yapmanın optimizasyon stratejisi:

**1. Minimal OS yüzeyi (boot süresi ve jitter tavanı):**
```bash
# Headless server kurulumu; gereksiz servisleri kaldır
sudo systemctl disable --now snapd ModemManager bluetooth cups avahi-daemon
sudo apt-get purge -y snapd            # snap, periyodik refresh ile jitter kaynağı
# Boot süresini analiz et — runtime'ın ne kadar geç başladığını gör
systemd-analyze blame | head -20
systemd-analyze critical-chain codesyscontrol.service
```
snapd özellikle önemlidir: arka planda periyodik `snap refresh` mount/unmount işlemleri yapar ve bu I/O jitter'ı RT görevlere yansır.

**2. Config'i katmanlı yönet (bakım maliyeti):** Site-özel ayarları `CODESYSControl_User.cfg`'ye, varsayılanları ana `.cfg`'ye koy. Bu, paket güncellemelerinde ayar kaybını önler (bkz. Not 7) ve Ansible ile yalnızca tek dosyayı template'lemeyi sağlar.

**3. Boot project ön-derleme:** Büyük uygulamalarda runtime, boot project'i ilk başlatmada derler/yükler; bu boot süresini uzatır. `Bootproject.RetainMismatch.Init` ve önceden derlenmiş boot project ile soğuk başlatma hızlandırılır. Üretimde IPC güç kesintisi sonrası **runtime'ın ne kadar sürede çıkış verdiği** (recovery time) ölçülmeli ve proses gereksinimine göre optimize edilmeli.

**4. Lisans yedekleme otomasyonu:**
```bash
# CmContainer'ı periyodik yedekle (cron veya systemd timer)
cmu --export-license --file /backup/cm_$(hostname)_$(date +%F).WibuCmRaU --all
```
Bu yedek, NIC arızası/değişimi sonrası hızlı kurtarma sağlar; manuel re-aktivasyon (lisans sunucusu erişimi) gerektirmez.

## Derin Teknik Detay

**Neden CodeMeter ve neden MAC'e bağlama?** CODESYS lisanslama, Wibu-Systems CodeMeter altyapısını kullanır. Soft Container (CmActLicense), donanıma bağlanmak için bir "binding scheme" kullanır; varsayılan şema NIC MAC adresi, disk seri numarası ve CPU bilgisi gibi donanım parmak izlerinin bir kombinasyonudur. Bu tasarımın amacı, lisansın kopyalanıp başka makinede çalıştırılmasını (license piracy) engellemektir. Dezavantajı, donanım değişiminin lisansı kırmasıdır — bu yüzden kritik sistemlerde fiziksel CmDongle tercih edilir: dongle, parmak izini USB token'ın güvenli elemanında taşır, host donanımından bağımsızdır.

**Runtime'ın Linux'taki süreç modeli:** `codesyscontrol` binary'si tek bir Linux süreci içinde çok sayıda POSIX thread çalıştırır. IEC görevleri ayrı kernel thread'leri değil, runtime'ın kendi zamanlayıcısının (CmpSchedule) yönettiği thread'lerdir. Runtime ana thread'i SCHED_FIFO önceliğiyle çalışır (`[SysProcess] RealTimePriority`), ve CmpSchedule `SchedulerInterval` periyodunda IEC görevlerini tetikler. Bu mimari, runtime'ın OS scheduler'a değil kendi deterministik zamanlayıcısına dayanmasını sağlar — bu da neden PREEMPT_RT + SCHED_FIFO kombinasyonunun kritik olduğunu açıklar: runtime ana thread'i kesilirse tüm IEC görevleri gecikir.

**Neden gateway ayrı bir bileşen (CmpGwServer)?** CODESYS mimarisinde IDE doğrudan runtime'a değil, bir Gateway katmanına bağlanır (TCP 1217). Gateway, birden fazla runtime instance'a tek bir noktadan yönlendirme (routing) yapabilir ve runtime ile IDE arasında protokol soyutlaması sağlar. Bu, bir IDE'nin tek gateway üzerinden ağdaki birçok PLC'ye ulaşmasını mümkün kılar (block driver routing). Alternatif tasarım (IDE'nin doğrudan runtime'a bağlanması) basit olurdu ancak çok-cihazlı dağıtık keşif ve routing yeteneğini kaybederdi. Bu yüzden gateway, headless IPC'de bile runtime ile aynı süreçte gömülü olarak çalışır.

**Deb paketi vs Deploy Tool — altta ne farklı?** Deploy Tool, SSH üzerinden hedefe bağlanıp aslında aynı deb paketini transfer edip `dpkg` ile kuran bir orkestratördür; ek olarak hedefin mimarisini (x86/ARM) tespit edip doğru paketi seçer ve servis kurulumunu doğrular. Yani altta yatan mekanizma aynıdır; Deploy Tool sadece bu adımları IDE'den otomatize eder. Bu nedenle CI/headless ortamda manuel `dpkg` tamamen eşdeğer ve denetlenebilir bir yoldur.

## İlgili Konular

```
knowledge/hardware/industrial-pc/
├── 02_network_config.md            → Runtime kurulumu sonrası ağ yapılandırması
├── 03_performance_tuning.md        → RT kernel ve CPU optimizasyonu
└── _synthesis.md                   → Üç belgenin sentezi

knowledge/codesys/fundamentals/
├── 01_runtime_architecture.md      → CODESYS runtime iç mimarisi (önkoşul)
└── _synthesis.md                   → CODESYS temel kavramlar özeti

knowledge/codesys/tasks/
└── task_types.md                   → Cyclic, Event, Freewheeling task yapılandırması
```
