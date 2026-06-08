---
KONU        : Endüstriyel PC Ağ Yapılandırması (CODESYS Runtime için)
KATEGORİ    : hardware
ALT_KATEGORI: industrial-pc
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Control/_rtsl_start_page.html"
    başlık: "CODESYS Control — Start Page, Port Numaraları Tablosu (Resmi Dokümantasyon)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Control/_rtsl_extablish_connection_to_instance.html"
    başlık: "CODESYS Control — Establishing a Connection to an Instance (Resmi Dokümantasyon)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20PROFINET/_pnio_runtime_configuration_device.html"
    başlık: "CODESYS PROFINET — Configuring a PROFINET Device, SysSocket/SysEthernet (Resmi)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20PROFINET/_pnio_runtime_configuration_controller.html"
    başlık: "CODESYS PROFINET — Configuring a PROFINET Controller, Linux.ProtocolFilter (Resmi)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20PROFINET/_pnio_trouble_profinet_and_other_drivers.html"
    başlık: "CODESYS PROFINET — PROFINET and Other Drivers, Exclusive NIC Access (Resmi)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Communication/_comm_opcua_server_config.html"
    başlık: "CODESYS OPC UA Server Configuration Settings, NetworkAdapter parametresi (Resmi)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/Security/_sec_start_page.html"
    başlık: "CODESYS Security — Genel Güvenlik Önerileri, Ağ Ayrımı (Resmi)"
    güvenilirlik: resmi
  - url: "https://github.com/toradex/codesys/blob/master/CODESYSControl.cfg"
    başlık: "Toradex GitHub — CODESYSControl.cfg Referans Dosyası (Üretici Topluluk)"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Engineering/thread/4a26eddbf8/"
    başlık: "CODESYS Forge — Scan Network için kullanılan portlar (Forum)"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Runtime/thread/d123fc2610/"
    başlık: "CODESYS Forge — CmpBlkDrvUdp MaxInterfaces=0 ile UDP deactivation (Forum)"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Engineering/thread/327fc95392/"
    başlık: "CODESYS Forge — CODESYSControl_User.cfg ile OPC UA NetworkAdapter bağlama (Forum)"
    güvenilirlik: topluluk
  - url: "https://www2.parkcity.co.uk/blog/netplan-two-nics-different-ips"
    başlık: "Netplan: Two NICs, Different IPs On Ubuntu 22.04 (Blog)"
    güvenilirlik: topluluk
  - url: "https://oneuptime.com/blog/post/2026-03-02-multiple-interfaces-netplan-ubuntu/view"
    başlık: "How to Set Up Multiple Interfaces with Netplan on Ubuntu (Blog)"
    güvenilirlik: topluluk
  - url: "https://computingforgeeks.com/configure-static-ip-ubuntu-2604-netplan/"
    başlık: "Configure Static IP Ubuntu 26.04 with Netplan (Blog)"
    güvenilirlik: topluluk
  - url: "https://scadaprotocols.com/network-segmentation-iec-62443/"
    başlık: "Network Segmentation in Industrial Control Systems — IEC 62443 (Topluluk)"
    güvenilirlik: topluluk
  - url: "https://ics-cert.kaspersky.com/publications/reports/2019/09/18/security-research-codesys-runtime-a-plc-control-framework-part-1/"
    başlık: "Kaspersky ICS CERT — CODESYS Runtime Güvenlik Araştırması Bölüm 1 (Araştırma)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/hardware/industrial-pc/01_codesys_runtime_setup.md"
    ilişki: gerektirir
  - konu: "knowledge/hardware/industrial-pc/03_performance_tuning.md"
    ilişki: tamamlar
  - konu: "knowledge/networking/01_topologies.md"
    ilişki: tamamlar
  - konu: "knowledge/networking/02_security.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "CODESYS Runtime kurulumu tamamlanmış olmalı — bkz. knowledge/hardware/industrial-pc/01_codesys_runtime_setup.md"
  - "Linux ağ yönetiminin temelleri: ip addr, ip route, systemctl"
  - "Endüstriyel PC'ye Ubuntu 22.04 LTS veya Debian 12 kurulu olmalı"
  - "Hedef sistemde en az bir, tercihen iki fiziksel NIC bulunmalı"
ÇELİŞKİLER :
  - kaynak: "CODESYS Forge forum (topluluk) vs Toradex CODESYSControl.cfg referans dosyası"
    konu: "CmpBlkDrvUdp'yi belirli bir arayüze kısıtlamak için kullanılan parametreler"
    çözüm: >
      Toradex referans dosyasında itf.0.ipaddress ve itf.0.name parametreleri gösterilmektedir.
      Forge forumunda ise MaxInterfaces=0 ile tamamen devre dışı bırakma ya da MaxInterfaces=1 ile
      tek arayüze kısıtlama anlatılmaktadır. Her iki yol da aynı [CmpBlkDrvUdp] bölümündedir;
      üretim öncesi test ortamında doğrulanması önerilir.
  - kaynak: "CODESYS Resmi Dokümantasyon vs Topluluk Forumu"
    konu: "CmpGwServer bölümünün CODESYSControl.cfg içindeki tam sözdizimi"
    çözüm: >
      Resmi dokümantasyon gateway portunu 1217 olarak belirtir; ancak CODESYSControl.cfg için
      CmpGwServer sözdizimi örneği sunan resmi bir kaynak bulunamadı. Kurulum sonrası dosya
      incelenerek doğrulanmalıdır: grep -r "CmpGwServer" /etc/codesyscontrol/
---

## Özün Ne

Endüstriyel bir PC'de CODESYS runtime kurduktan sonraki kritik adım ağ yapılandırmasıdır. Bu yapılandırma iki temel amaca hizmet eder: (1) CODESYS IDE'nin runtime'a erişebilmesi için Gateway portunu (varsayılan: TCP 1217) doğru arayüzden yayınlamak ve (2) fieldbus trafiğini (EtherCAT, PROFINET vb.) IT ağından fiziksel veya mantıksal olarak izole etmek.

Yanlış yapılandırılmış bir ağ; runtime'a erişilememesine, fieldbus zamanlama sorunlarına (jitter artışı) ya da OT ağının IT tehditlerine açık kalmasına doğrudan yol açar. Üretim IPC'lerinde tipik olarak iki fiziksel NIC bulunur: biri SCADA/HMI/programlama ağına, diğeri fieldbus veya makine ağına bağlanır. Bu ayrımın doğru kurulması, IEC 62443 güvenlik standardının temel gereksinimidir.

## Nasıl Çalışır

### CODESYS Ağ İletişim Katmanları

CODESYS runtime, IDE ile iletişimi üç farklı protokol mekanizması üzerinden kurar:

```
CODESYS IDE (Geliştirme PC)
        │
        ├─ TCP 1217 ────────────► Gateway portu (standart bağlantı)
        ├─ UDP 1740-1743 ◄──────  Discovery / Scan Network
        └─ TCP 11740-11743 ◄────  Direkt runtime bağlantısı (port yönlendirme)

IPC Üzerinde Runtime:
   ├── enp2s0 (IT/Programlama ağı)  → 192.168.1.x — IDE, SCADA, OPC UA
   └── enp3s0 (Fieldbus/Makine ağı) → 192.168.100.x — EtherCAT, PROFINET
```

### Port Numaraları Tablosu

Aşağıdaki port bilgileri CODESYS resmi dokümantasyonundan alınmıştır (kaynak: `content.helpme-codesys.com/_rtsl_start_page.html`). Resmi dokümantasyon, bu portların "yapılandırma ile değiştirilebileceğini" belirtmektedir:

| Port | Protokol | Kullanım |
|---|---|---|
| **1217** | TCP | Gateway bağlantısı — IDE ↔ Runtime |
| **1740–1743** | UDP | Block driver tarama portları (Scan Network discovery) |
| **11740–11743** | TCP | TCP block driver portları (direkt instance bağlantısı) |
| **4840** | TCP | OPC UA sunucusu |
| **8080** | TCP | CODESYS Web sunucusu (WebVisu, HTTP) |
| **443** | TCP | CODESYS Web sunucusu (SSL/HTTPS) |
| **22** | TCP | SSH — Linux kurulum ve güncelleme |

Ağ tarama (Scan Network) için IDE, UDP 1740-1743 üzerinden broadcast gönderir. Direkt IP ile bağlanmak için TCP 11740 yeterlidir (kaynak: CODESYS Forge `4a26eddbf8`). Birden fazla runtime instance varsa sıradaki portlar kullanılır (11741, 11742 vb.).

### Fieldbus NIC Gereksinimleri — Özel Erişim Kuralı

CODESYS PROFINET ve EtherCAT sürücüleri, düşük seviyeli Ethernet bileşenine (SysEthernet) **özel erişim** gerektirir. Resmi PROFINET dokümantasyonuna göre (kaynak: `_pnio_trouble_profinet_and_other_drivers.html`):

- PROFINET ve EtherCAT **aynı NIC üzerinde birlikte çalışamaz**
- PROFINET veya EtherCAT için kullanılan NIC, başka bir RT fieldbus çalıştıramaz
- Ancak Modbus/TCP, WebVisu ve CODESYS Communication gibi TCP/IP servisleri aynı NIC'i paylaşabilir
- Birden fazla NIC varsa her birine ayrı PROFINET veya EtherCAT sürücüsü atanabilir

Bu nedenle üretim IPC'lerinde ideal mimari şudur: **bir NIC yalnızca fieldbus'a ayrılır, diğer NIC IT trafiğine ayrılır.**

### OT/IT Ağ Ayrımı ve IEC 62443

IEC 62443 standardı, endüstriyel ağları "Güvenlik Bölgeleri" (Security Zones) ve aralarındaki "Conduit"ler (Kontrollü İletişim Kanalları) şeklinde tanımlar. Pratik uygulama mimarisi (kaynak: `scadaprotocols.com`):

```
[IT / Kurumsal]──[Firewall]──[DMZ]──[Firewall]──[OT / SCADA]──[Fieldbus Ağı]
  192.168.0.x                         192.168.1.x              192.168.100.x
  Ofis bilgisayarları    Historian,    IPC, SCADA server        EtherCAT, PROFINET
                         OPC UA proxy                           servo, I/O, sensör
```

DMZ katmanında historian sunucuları, OPC UA proxy ve uzak erişim sunucuları yer alır. Doğrudan IT→OT bağlantısına izin verilmez; tüm trafik kontrollü conduit üzerinden geçer.

CODESYS güvenlik sayfası (kaynak: `_sec_start_page.html`) şu üç ilkeyi temel güvenlik gereksinimi olarak listeler:
1. Ofis, üretim ve fieldbus ağlarının birbirinden ayrılması
2. Ağ sınırlarını koruyan firewall kullanımı
3. Ağlar arası iletişimde şifreli ve kimlik doğrulamalı protokol (VPN)

## Pratikte Nasıl Kullanılır

### 1. Adım: Mevcut Ağ Arayüzlerini Tanımlama

```bash
# Tüm ağ arayüzlerini listele
ip link show

# Örnek çıktı:
# 2: enp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
# 3: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500

# Ayrıntılı adres ve MAC bilgisi
ip addr show

# Sadece aktif arayüzler
ip -br link show up
```

Ubuntu/Debian'da modern NIC isimleri "Tahmin Edilebilir Ağ Arayüzü Adları" şemasını kullanır:
- `enp2s0` — PCI slot 2, port 0 (PCI konumuna dayalı)
- `eno1` — onboard NIC 1 (yerleşik karta dayalı)
- `eth0` — eski çekirdek adlandırması (bazı gömülü/ARM sistemlerde)

### 2. Adım: Netplan ile Statik IP — Tekli NIC

Ubuntu 22.04+ sistemlerde kalıcı ağ yapılandırması `/etc/netplan/` altındaki YAML dosyaları ile yapılır (kaynak: `computingforgeeks.com`):

```bash
# Mevcut netplan dosyasını bul
ls /etc/netplan/

# Yeni yapılandırma dosyası oluştur (sayısal önek sırayı belirler)
sudo nano /etc/netplan/01-industrial-network.yaml
```

Tek NIC ile temel statik IP yapılandırması:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp2s0:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

Netplan sözdizimi kritik notlar (kaynak: `computingforgeeks.com`):
- Girintileme için **yalnızca 2 boşluk** kullanılır; tab karakteri YAML parse hatasına neden olur
- IP adresleri CIDR gösterimiyle yazılır: `192.168.1.100/24`
- Ubuntu 22.04+ `gateway4:` ifadesi kullanımdan kaldırılmıştır; yerine `routes: - to: default` bloğu kullanılmalıdır
- Dosya izni: `sudo chmod 600 /etc/netplan/01-industrial-network.yaml`

```bash
# Yapılandırmayı sözdizimi hatası olmadan doğrula
sudo netplan generate

# Güvenli uygulama — 60 saniye içinde onaylanmazsa otomatik geri alır
sudo netplan try --timeout 60
# Enter'a basarak onayla

# Veya direkt uygula (dikkat: SSH bağlantısı kesilebilir)
sudo netplan apply

# Doğrulama komutları
ip -br a          # Arayüz durumu özeti
ip route show     # Yönlendirme tablosu
```

### 3. Adım: Netplan ile Statik IP — Çift NIC (Üretim Önerisi)

Çift NIC durumunda **yalnızca bir varsayılan rota** tanımlanmalıdır. İki NIC'te aynı anda varsayılan rota olursa, dönüş trafiği yanlış arayüzden çıkarak düşürülür (kaynak: `parkcity.co.uk`). Fieldbus NIC'i için varsayılan rota yerine yalnızca yerel subnet rotası tanımlanır:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:

    # NIC 1 — IT / Programlama / SCADA ağı
    # Gateway ve IDE bu NIC üzerinden bağlanır
    enp2s0:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      routes:
        - to: default          # Varsayılan rota YALNIZCA bu NIC'te
          via: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8]

    # NIC 2 — Fieldbus / Makine ağı
    # EtherCAT, PROFINET, Modbus/TCP aygıtları bu NIC üzerinden erişilir
    enp3s0:
      dhcp4: false
      addresses:
        - 192.168.100.1/24
      # Varsayılan rota YOK — yalnızca 192.168.100.0/24 subnet'ine otomatik yönlendirilir
```

Her iki NIC'ten gelen trafiğin doğru arayüzden yanıt vermesi gerekiyorsa policy-based routing uygulanır (kaynak: `oneuptime.com`):

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:

    enp2s0:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      routes:
        - to: default
          via: 192.168.1.1
          table: 100
        - to: 192.168.1.0/24
          via: 0.0.0.0
          table: 100
      routing-policy:
        - from: 192.168.1.100
          table: 100

    enp3s0:
      dhcp4: false
      addresses:
        - 192.168.100.1/24
      routes:
        - to: default
          via: 192.168.100.254
          table: 200
        - to: 192.168.100.0/24
          via: 0.0.0.0
          table: 200
      routing-policy:
        - from: 192.168.100.1
          table: 200
```

```bash
sudo chmod 600 /etc/netplan/01-industrial-network.yaml
sudo netplan apply

# Çift NIC doğrulama
ip route show table 100    # IT ağı rotaları
ip route show table 200    # Fieldbus ağı rotaları
ip -br a                   # Her iki NIC'in UP durumu
```

### 4. Adım: CODESYSControl.cfg Ağ Bölümleri

CODESYS runtime'ın hangi NIC'i kullandığı ve hangi portlarda dinlediği `CODESYSControl.cfg` (veya kullanıcı override için `CODESYSControl_User.cfg`) içindeki bölümlerle kontrol edilir. Dosya konumu: `/etc/codesyscontrol/CODESYSControl.cfg`

**SysEthernet Bölümü** — Fieldbus protokol filtresi (kaynak: `_pnio_runtime_configuration_controller.html`):

```ini
[SysEthernet]
; PROFINET veya EtherNet/IP kullanılıyorsa ETH_P_ALL (3) açılmalı
; EtherCAT varsayılan filtresi: 0x88A4
Linux.ProtocolFilter=3

; Fieldbus için QDISC bypass — PROFINET RT send jitter'ını azaltır
Linux.PACKET_QDISC_BYPASS=1
```

**SysSocket Bölümü** — PROFINET device için NIC ve IP yönetimi (kaynak: `_pnio_runtime_configuration_device.html`):

```ini
[SysSocket]
; PROFINET device için fieldbus NIC'ini belirt
Adapter.0.Name=enp3s0
; Runtime'ın IP/subnet ayarlamasına izin ver (PROFINET DCP için gerekli)
Adapter.0.EnableSetIpAndMask=1
```

**CmpBlkDrvUdp Bölümü** — UDP block driver arayüz kısıtlaması (kaynak: CODESYS Forge `d123fc2610`, Toradex `CODESYSControl.cfg`):

```ini
[CmpBlkDrvUdp]
; Yalnızca IT ağı NIC'ini dinle — tüm arayüzlerde açık kalmasın
MaxInterfaces=1
itf.0.ipaddress=192.168.1.100
itf.0.name=main
itf.0.networkmask=255.255.255.0

; Alternatif: UDP driver'ı tamamen devre dışı bırak (güvenli, izole ortam)
; MaxInterfaces=0
; (Bu durumda Scan Network çalışmaz; yalnızca direkt TCP 11740 ile bağlanılabilir)
```

**OPC UA Sunucu NIC Bağlama** (kaynak: `_comm_opcua_server_config.html`):

```ini
[CmpOPCUAServer]
; OPC UA'yı yalnızca IT/SCADA NIC'ine bağla
; Varsayılan: "All available networkadapters are used"
NetworkAdapter=enp2s0
; Varsayılan port 4840; değiştirilecekse:
; NetworkPort=4840
```

Değişikliklerden sonra runtime yeniden başlatılmalıdır:

```bash
sudo systemctl restart codesyscontrol

# Gateway portunu dinlediğini doğrula
ss -tlnp | grep 1217
# Beklenen çıktı: LISTEN  0  128  192.168.1.100:1217
# (0.0.0.0:1217 değil — tüm arayüzlerde değil, yalnızca IT NIC'inden dinlemeli)

# UDP 1740 dinleme kontrolü
ss -ulnp | grep 1740
```

### 5. Adım: UFW Firewall Yapılandırması

CODESYS resmi dokümantasyonu, runtime portlarının internet üzerinden korumasız erişime **kesinlikle açılmaması** gerektiğini vurgular; internet erişimi zorunluysa VPN kullanılmalıdır (kaynak: `_rtsl_start_page.html`).

```bash
# UFW kurulumu
sudo apt-get install -y ufw

# Varsayılan politika: gelen trafiği engelle, gideni izin ver
sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH — yalnızca IT/programlama subnet'inden
sudo ufw allow from 192.168.1.0/24 to any port 22 proto tcp

# CODESYS Gateway (1217) — yalnızca programlama ağından
sudo ufw allow from 192.168.1.0/24 to any port 1217 proto tcp

# CODESYS UDP Block Driver (Scan Network) — yalnızca programlama ağından
sudo ufw allow from 192.168.1.0/24 to any port 1740:1743 proto udp

# CODESYS TCP Block Driver (direkt bağlantı) — yalnızca programlama ağından
sudo ufw allow from 192.168.1.0/24 to any port 11740:11743 proto tcp

# OPC UA — yalnızca SCADA/MES subnet'inden
sudo ufw allow from 192.168.1.0/24 to any port 4840 proto tcp

# WebVisu (HTTP) — yalnızca dahili ağdan
sudo ufw allow from 192.168.1.0/24 to any port 8080 proto tcp

# Fieldbus subnet'inden IT portlarına erişimi engelle
sudo ufw deny from 192.168.100.0/24 to any port 1217
sudo ufw deny from 192.168.100.0/24 to any port 4840

# UFW etkinleştir
sudo ufw enable

# Kuralları doğrula
sudo ufw status verbose
```

**PROFINET için özel not** (kaynak: `_pnio_firewall_packagefilter.html`): PROFINET RT, Ethertype `0x8892` kullanır; IP katmanında değil, Ethernet katmanında çalışır. UFW bu seviyeyi filtreleyemez. PROFINET trafiği doğrudan NIC'e ulaşır. Bu nedenle fieldbus NIC'inin IT ağından fiziksel olarak izole edilmesi en güvenilir yaklaşımdır.

## Örnekler

### Örnek 1: Üretim IPC'si — EtherCAT + SCADA Mimarisi

Senaryo: Bir makine hücresinde EtherCAT servo kontrolü ve SCADA erişimi gerektiren IPC.

```
IPC ağ planı:
  enp2s0: 192.168.1.100/24  → IT switch → SCADA server, IDE PC, OPC UA client
  enp3s0: 192.168.100.1/24  → Fieldbus switch → EtherCAT servo, I/O
```

`/etc/netplan/01-industrial.yaml`:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp2s0:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [192.168.1.1]
    enp3s0:
      dhcp4: false
      addresses:
        - 192.168.100.1/24
```

`/etc/codesyscontrol/CODESYSControl.cfg` (ek bölümler):

```ini
[SysEthernet]
Linux.ProtocolFilter=3
Linux.PACKET_QDISC_BYPASS=1

[CmpBlkDrvUdp]
MaxInterfaces=1
itf.0.ipaddress=192.168.1.100
itf.0.name=main
itf.0.networkmask=255.255.255.0

[CmpOPCUAServer]
NetworkAdapter=enp2s0
NetworkPort=4840
```

```bash
# Uygula
sudo chmod 600 /etc/netplan/01-industrial.yaml
sudo netplan apply
sudo systemctl restart codesyscontrol

# Doğrulama
ss -tlnp | grep -E "1217|4840|8080"
ip route show
ip -br a
```

### Örnek 2: ip Komutuyla Geçici IP Atama (Test/Hızlı Erişim)

Netplan kalıcı yapılandırmasına alternatif olarak, test amacıyla geçici IP:

```bash
# Geçici statik IP ekle (yeniden başlatmada silinir)
sudo ip addr add 192.168.1.100/24 dev enp2s0

# Varsayılan rota ekle
sudo ip route add default via 192.168.1.1 dev enp2s0

# Mevcut bir IP adresini sil
sudo ip addr del 192.168.1.200/24 dev enp2s0

# Arayüzü aktif et
sudo ip link set enp2s0 up
sudo ip link set enp3s0 up

# Doğrulama
ip addr show enp2s0
ip route show
```

### Örnek 3: UFW Kurallarının Doğrulanması

```bash
# Tüm kuralları numaralı listele
sudo ufw status numbered

# Örnek çıktı:
#      To                         Action      From
#      --                         ------      ----
# [ 1] 22/tcp                     ALLOW IN    192.168.1.0/24
# [ 2] 1217/tcp                   ALLOW IN    192.168.1.0/24
# [ 3] 1740:1743/udp              ALLOW IN    192.168.1.0/24
# [ 4] 11740:11743/tcp            ALLOW IN    192.168.1.0/24
# [ 5] 4840/tcp                   ALLOW IN    192.168.1.0/24
# [ 6] 8080/tcp                   ALLOW IN    192.168.1.0/24
# [ 7] 1217/tcp                   DENY IN     192.168.100.0/24

# Port dinleme durumu (CODESYS portları)
ss -tlunp | grep -E "1217|1740|1741|1742|1743|11740|4840|8080"

# Belirli bir kuralı sil
sudo ufw delete 7
```

### Örnek 4: NIC İsmini MAC Adresine Bağlama (Kalıcı İsimlendirme)

NIC kartı değiştiğinde arayüz adı değişebilir; bu durum `CODESYSControl.cfg` ayarlarını bozar. Çözüm: `match` bloğu ile MAC adresine sabit isim atama:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:

    it-nic:
      match:
        macaddress: "aa:bb:cc:11:22:33"
      set-name: eth-it
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      routes:
        - to: default
          via: 192.168.1.1

    fieldbus-nic:
      match:
        macaddress: "aa:bb:cc:44:55:66"
      set-name: eth-fieldbus
      dhcp4: false
      addresses:
        - 192.168.100.1/24
```

`CODESYSControl.cfg`'de artık sabit isimler kullanılabilir:

```ini
[SysSocket]
Adapter.0.Name=eth-fieldbus
Adapter.0.EnableSetIpAndMask=1

[CmpOPCUAServer]
NetworkAdapter=eth-it
```

## Sık Yapılan Hatalar

### Hata 1: DHCP Açık Kalmış — Runtime Her Yeniden Başlamada IP Değişiyor

```
Semptom: IDE bazen bağlanıyor, bazen bağlanamıyor; sabahları SCADA offline.
Neden  : dhcp4: true bırakılmış; router farklı IP atıyor.
Çözüm  :
  grep -i dhcp /etc/netplan/*.yaml
  # dhcp4: true görünüyorsa → false olarak değiştir
  sudo netplan apply
```

### Hata 2: İki NIC'e Aynı Anda İki Varsayılan Rota Tanımlamak

```
Semptom: Fieldbus NIC'inden gelen paketlere yanıt yanlış arayüzden çıkıyor; bağlantı kopuyor.
Neden  : Her iki NIC'te de "routes: - to: default" tanımlı.
Çözüm  : Yalnızca IT/programlama NIC'inde varsayılan rota tanımla.
         Fieldbus NIC'inde sadece yerel subnet rotası yeterli — kernel otomatik yönlendirir.
         (Kaynak: parkcity.co.uk — tek default route ilkesi)
```

### Hata 3: CmpBlkDrvUdp Tüm Arayüzlerde Dinliyor

```ini
; ❌ Yanlış — varsayılan: tüm NIC'lerden UDP 1740-1743 açık
[CmpBlkDrvUdp]
; (boş — güvenlik açığı!)

; ✅ Doğru — yalnızca IT NIC'i
[CmpBlkDrvUdp]
MaxInterfaces=1
itf.0.ipaddress=192.168.1.100
itf.0.name=main
itf.0.networkmask=255.255.255.0
```

Kaspersky ICS CERT araştırmasına göre (2019), CmpBlkDrvUdp'nin tüm arayüzlerden erişilebilir kalması saldırı yüzeyini artırır ve IP spoofing saldırısı için zemin oluşturur.

### Hata 4: PROFINET ve EtherCAT'i Aynı NIC'te Çalıştırmaya Çalışmak

```
Semptom: Fieldbus cihazları keşfedilemiyor, ya da zaman zaman bağlantı kopuyor.
Neden  : PROFINET ve EtherCAT aynı NIC'in SysEthernet bileşenine özel erişim ister.
Çözüm  : Her fieldbus protocol için ayrı fiziksel NIC kullan.
         (Kaynak: CODESYS Resmi — _pnio_trouble_profinet_and_other_drivers.html)
```

### Hata 5: Korumasız Sistemde Tüm Portlar Dış Ağa Açık

```bash
# Güvenlik açığı kontrolü:
ss -tlunp | grep -E "1217|1740|4840"
# 0.0.0.0:1217 çıkıyorsa → tüm arayüzlerden erişilebilir; tehlikeli

# Acil düzeltme:
sudo ufw enable
sudo ufw default deny incoming
# Ardından yalnızca gerekli IP bloklarına izin ver
```

### Hata 6: Netplan Dosyasında Sekme (Tab) Kullanımı

```
Semptom: sudo netplan apply → "Invalid YAML" veya "mapping values are not allowed here"
Neden  : YAML dosyasında girinti için sekme kullanıldı.
Çözüm  :
  cat -A /etc/netplan/01-industrial.yaml | grep "^I"
  # ^I görünüyorsa sekme var → düzelt, 2 boşlukla değiştir
```

### Hata 7: OPC UA Sunucusu Tüm NIC'lerde Açık

```ini
; ❌ Yanlış — varsayılan: tüm adaptörler kullanılır (log: "All available networkadapters are used")
[CmpOPCUAServer]
; (boş)

; ✅ Doğru — yalnızca IT NIC'i
[CmpOPCUAServer]
NetworkAdapter=enp2s0
```

### Hata 8: Systemd Servisi Ağ Hazır Olmadan Başlıyor — Gateway Bind Hatası

```bash
# /etc/systemd/system/codesyscontrol.service.d/override.conf oluştur
sudo mkdir -p /etc/systemd/system/codesyscontrol.service.d/
sudo nano /etc/systemd/system/codesyscontrol.service.d/override.conf
```

```ini
[Unit]
After=network-online.target
Wants=network-online.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart codesyscontrol
```

`network.target` arayüzlerin UP olduğunu garanti etmez; `network-online.target` gereklidir.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Çift NIC Mimarisi Tercih Edilmeli

- **Üretim ortamı**: Fieldbus trafiğinin IT trafiğiyle çakışması kabul edilemez gecikmelere yol açabilir.
- **IEC 62443 uyumluluk gereksinimi**: Standart, OT ve IT ağlarının fiziksel veya mantıksal ayrımını zorunlu kılar.
- **EtherCAT veya PROFINET kullanan IPC**: Her ikisi de SysEthernet'e özel erişim gerektirir; paylaşımlı NIC sorun yaratabilir.
- **Çoklu fieldbus protokol**: Aynı IPC'de EtherCAT + PROFINET birlikte çalışacaksa her biri için ayrı NIC şarttır.

### Tekli NIC Kabul Edilebilir

- **Geliştirme/test ortamı**: Fieldbus yoksa ve yalnızca Modbus/TCP veya OPC UA kullanılıyorsa tek NIC yeterlidir.
- **Raspberry Pi / düşük maliyetli gömülü**: Fiziksel NIC seçeneği sınırlı; USB-Ethernet adaptörle geçici çözüm yapılabilir.
- **Yalnızca IT protokolleri**: WebVisu, OPC UA, Modbus/TCP, TCP üzerinden çalışan her şey tek NIC ile çalışabilir.

### Tercih Edilmemeli

- **Fieldbus NIC'ini IT ağına yönlendirmek veya köprülemek**: Fieldbus cihazları IT ağına maruz kalır; hem güvenlik riski hem gerçek zamanlılık kaybı yaşanır.
- **Fieldbus NIC'i için DHCP**: IP adresi değişimi fieldbus haberleşmesini keser.
- **1217 portunu doğrudan internete açmak**: CODESYS resmi dokümantasyonu bunu açıkça yasaklar; uzaktan erişim zorunluysa VPN kullanılmalıdır.
- **Yalnızca VLAN ile OT/IT ayrımı, firewall olmadan**: VLAN mantıksal ayrım sağlar fakat CODESYS gerçek zamanlı fieldbus için yeterli izolasyon garantisi vermez; fiziksel NIC ayrımı tercih edilmelidir.

## Gerçek Proje Notları

**Not 1 — PROFINET DCP ve Statik IP Çatışması**
PROFINET protokolü, ağ cihazlarını DCP (Discovery and Configuration Protocol) ile keşfeder ve zaman zaman cihazın IP adresini değiştirebilir. `SysSocket` bölümünde `Adapter.0.EnableSetIpAndMask=1` etkinleştirilmişse, PROFINET controller bir cihazın IP'sini değiştirebilir. Fieldbus NIC'inin IP adresi PROFINET DCP tarafından üzerine yazılmasın diye bu parametre yalnızca PROFINET device rolündeki NIC için etkinleştirilmeli; IT NIC'inde devre dışı bırakılmalıdır.

**Not 2 — netplan try ile Uzak Sunucuda Güvenli Uygulama**
SSH ile bağlı bir IPC'de `sudo netplan apply` yapmak risklidir; yanlış yapılandırma SSH bağlantısını koparır ve cihaza fiziksel erişim gerektirir. `sudo netplan try --timeout 60` değişikliği uygular ve 60 saniye içinde onaylanmazsa otomatik geri alır. Üretim IPC'lerinde bu komut standart prosedür olmalıdır.

**Not 3 — Interface İsminin Değişmesi Riski**
Bir projede yeni NIC kartı eklendiğinde arayüz ismi değişti (enp2s0 → enp3s0); bu durum `CODESYSControl.cfg`'deki `Adapter.0.Name` parametresini geçersiz kıldı ve fieldbus kesildi. Çözüm: netplan'ın `match.macaddress` + `set-name` özelliğiyle NIC'e kalıcı isim atamak. Bu şekilde `CODESYSControl.cfg` sabit kalır ve donanım değişimi ağ yapılandırmasını bozmaz.

**Not 4 — CmpBlkDrvUdp Kapatıldığında IDE Scan Network Çalışmaz**
`MaxInterfaces=0` ile UDP block driver tamamen kapatılırsa, CODESYS IDE "Scan Network" ile bu IPC'yi otomatik keşfedemez. Yalnızca direkt TCP bağlantısı (IP:11740) çalışır. Güvenli, izole ortamlarda bu tercih edilebilir; ancak tüm geliştiricilerin manuel IP:port girişini bilmesi gerekir (kaynak: CODESYS Forge `d123fc2610`).

**Not 5 — UFW ve Docker Çakışması**
Bazı projelerde Docker yüklü IPC'lerde UFW kuralları Docker tarafından bypass edildi. UFW, `iptables` üzerinden çalışır; Docker kendi `iptables` zincirlerini yönetir ve UFW'yi atlayabilir. OT güvenliği açısından Docker kullanan IPC'lerde router/switch seviyesinde VLAN veya fiziksel ağ ayrımı ek güvenlik katmanı olarak uygulanmalıdır.

**Not 6 — Fieldbus NIC'inde Linux Ağ Yığınını Kapatmak**
EtherCAT kullanılan projelerde fieldbus NIC'inde Linux'un kendi TCP/IP yığınını tamamen kapatmak mümkündür. Bu yaklaşım, fieldbus NIC'ine doğrudan CODESYS sürücüsünün erişmesini sağlar ve maksimum gerçek zamanlı performans sunar. Ancak bu durumda o NIC'e SSH veya başka bir IP servisi ile erişilemez; NIC yalnızca CODESYS sürücüsüne aittir. Uygulama: arayüzü `ip link set enp3s0 down` ile kapatıp CODESYS sürücüsüne bırakmak.

## İlgili Konular

```
knowledge/hardware/industrial-pc/
├── 01_codesys_runtime_setup.md     → Runtime kurulumu (önkoşul)
└── 03_performance_tuning.md        → RT kernel, CPU izolasyonu, NIC interrupt affinity

knowledge/networking/
├── 01_topologies.md                → Yıldız, ring, hat topoloji seçimi
└── 02_security.md                  → IEC 62443, OT/IT güvenlik mimarisi detayları

knowledge/codesys/fundamentals/
└── 01_runtime_architecture.md      → CODESYS runtime iç mimarisi
```
