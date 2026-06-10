---
KONU        : InoProShop Haberleşme (Modbus, OPC UA, CANopen, Socket, HMI)
KATEGORİ    : inovance
ALT_KATEGORI: inoproshop
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.inovance.eu/products/motion-controllers-i/o-modules/am600-motion-controllers"
    başlık: "Inovance — AM400/AM600 Motion Controllers (haberleşme arayüzleri)"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/fileadmin/downloads/Brochures/EN/AM600_Br_EN_Singles_Web_V2.2.pdf"
    başlık: "Inovance — AM600 Motion Controller Broşürü (EtherCAT, CAN, RS485, Ethernet)"
    güvenilirlik: resmi
  - url: "https://idea-tech.in/wp-content/uploads/2020/04/INOVANCE-AM400AM600AC800-PLC-SOFTWARE-MANUAL-ENGLISH-20-4-20.pdf"
    başlık: "Inovance — AM400/AM600/AC800 Medium-Sized PLC Software (InoProShop) User Guide"
    güvenilirlik: resmi
  - url: "https://www.manualslib.com/manual/1812322/Inovance-Am600-Series.html?page=85"
    başlık: "Inovance AM600 Hardware Manual — CANopen/CANlink Bus Connection"
    güvenilirlik: topluluk
  - url: "https://www.inovance.eu/products/plcs-hmis/it7000-hmi"
    başlık: "Inovance — IT7000 HMI (OPC UA, Modbus RTU/TCP, MQTT desteği)"
    güvenilirlik: resmi
  - url: "https://store.codesys.com/en/codesys-opc-ua-server-sl.html"
    başlık: "CODESYS Store — OPC UA Server SL (runtime eklenti/lisans)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Communication/_comm_opcua_server_config.html"
    başlık: "CODESYS — OPC UA Server Configuration (port 4840, ayarlar)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_inoproshop_overview.md"
    ilişki: gerektirir
  - konu: "knowledge/protocols/modbus-tcp/_synthesis.md"
    ilişki: detaylandırır
  - konu: "knowledge/protocols/opc-ua/_synthesis.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/networking/_synthesis.md"
    ilişki: kullanır
  - konu: "04_hardware_configuration.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "InoProShop = CODESYS V3 olgusu (01_inoproshop_overview.md)"
  - "CODESYS networking temelleri: GVL tek-yazar, bloke-I/O, Bus Cycle Task (knowledge/codesys/networking/_synthesis.md)"
  - "Modbus register modeli ve OPC UA adres uzayı kavramları (knowledge/protocols/)"
ÇELİŞKİLER :
  - kaynak: "Topluluk forumları: 'AM600'de OPC UA standart gelir' vs CODESYS Store: 'OPC UA Server SL ayrı lisans'"
    konu: "OPC UA sunucusunun belirli AM400/AM600 firmware'inde gömülü mü yoksa ayrı runtime lisansı mı gerektirdiği ürüne/sürüme göre değişir"
    çözüm: >
      DOĞRULANMADI — bu belgede tahmin edilmedi. CODESYS genel dağıtımında OPC UA
      Server SL ayrı bir runtime eklentisidir (store.codesys.com). Inovance bunu bazı
      AM serisi firmware'lerine gömebilir; kesin durum ürün + firmware + InoProShop
      sürümüne göre değişir. Devreye almadan önce hedef cihazda "Add Object → Symbol
      Configuration → Support OPC UA features" seçeneğinin görünüp görünmediği ve
      sunucunun gerçekten başladığı doğrudan Inovance dokümanı/cihaz üzerinde teyit
      edilmelidir. Aşağıda bu nokta açıkça işaretlenmiştir.
---

## Özün Ne

InoProShop CODESYS V3 olduğu için, AM400/AM600/AC800 kontrolörlerinin haberleşme
yapılandırması **büyük oranda jenerik CODESYS V3 ile birebir aynıdır**: Modbus TCP/RTU,
OPC UA server, CANopen master, ve ham TCP/UDP socket (SysSocket) için aynı Device Tree
mantığı, aynı kütüphaneler ve aynı GVL/Symbol Configuration akışı kullanılır. Yani
`knowledge/protocols/` ve `knowledge/codesys/networking/` altındaki bilgi doğrudan
transfer olur; InoProShop'a özgü olan tek şey, cihaz havuzunun Inovance ürünleriyle
(AM serisi kontrolör + IT7000 HMI + SV servo) önceden dolu gelmesidir.

Neden önemli: Bir AM600 sahada genellikle aynı anda birden çok kanaldan konuşur —
EtherCAT ile servo (gerçek zaman), Modbus TCP/RTU ile eski cihaz ve HMI, OPC UA ile
SCADA/MES, CANopen ile sürücü/IO. Bu kanalların hangisinin **kontrol**, hangisinin
**raporlama/komuta** katmanı olduğunu doğru ayırmak, sağlam bir makine ile sürekli
"değer geç geliyor / takılıyor" şikâyeti üreten bir makine arasındaki farktır.

> **Temel ilke (knowledge/codesys/networking/_synthesis.md ile uyumlu):** Bu belgedeki
> hiçbir protokol (Modbus, OPC UA, socket, CANopen SDO) gerçek zamanlı kontrol katmanı
> değildir. Servo/motion senkronizasyonu EtherCAT'in (CANopen ise PDO + senkron) işidir.
> Modbus/OPC UA/socket = raporlama ve komuta.

## Nasıl Çalışır

### AM400/AM600 Haberleşme Arayüzleri (donanım tabanı)

Yazılım yapılandırması donanım arayüzüne dayanır. Resmi kaynaklara göre:

| Arayüz | AM400 | AM600 | Tipik Kullanım |
|---|---|---|---|
| Ethernet (LAN) | Var | Var | Modbus TCP, OPC UA, Socket, programlama/indirme |
| RS485 | 1 port | 2 port | Modbus RTU master/slave |
| CAN | 1 port (CANopen/CANlink, ≤1 Mbit/s) | 1 port (CANopen/CANlink, ≤1 Mbit/s) | CANopen master, sürücü/IO |
| EtherCAT | — | Var (motion master) | Gerçek zamanlı servo/IO (bu belgenin kapsamı dışı) |

> Not: AM600 LAN portu Modbus TCP ve socket talimatlarını destekler; ayrıca PROFINET
> slave (gateway olarak) gibi ek roller ürün/firmware'e göre olabilir. EtherCAT motion
> ayrı bir konudur (bkz. 05/06 belgeleri) ve burada haberleşme = saha/üst-katman
> raporlama olarak ele alınır.

### Ortak Zemin: Hepsi GVL Üzerinden

CODESYS'teki gibi InoProShop'ta da dört kanalın tamamı GVL değişkenleri üzerinden çalışır;
yalnızca erişim biçimi farklıdır:

```
Kanal        GVL Erişim Biçimi              Task Yerleşimi              Bloke Riski
──────────────────────────────────────────────────────────────────────────────────
Modbus TCP   I/O Mapping (Slave) / FB       Bus Cycle Task (yavaş)       düşük (poll-yanıt)
 / RTU        (Master, IoDrvModbus)         veya Freewheeling (master)
OPC UA       Symbol Configuration           runtime (CmpOPCUAServer)     düşük (sunucu ayrı)
CANopen      I/O Mapping (PDO) + FB (SDO)   Bus Cycle Task               düşük (PDO) / orta (SDO)
Socket TCP/UDP ADR()+MEMCPY (SysSocket)     Freewheeling (en düşük)      YÜKSEK (connect bloke)
```

İki ilke her kanalda geçerlidir (knowledge/codesys ile uyumlu):
1. **GVL tek-yazar:** Her register/node/topic'in tek bir yazarı olmalı. Master'ın yazdığı
   bir Holding Register'a PLC kodu da yazarsa komut her scan'de silinir.
2. **Bloke-I/O ayrımı:** Bloke edebilen çağrılar (socket connect, master bağlantısı) en
   düşük öncelikli / Freewheeling task'ta kalmalı; ana kontrol task'ını (örn. EtherCAT
   senkron task) asla bekletmemeli.

## Pratikte Nasıl Kullanılır

### 1) Modbus TCP — Server (Slave) ve Client (Master)

CODESYS Modbus mantığıyla birebir aynıdır (bkz. `knowledge/protocols/modbus-tcp/04_codesys_slave_config.md`).

**Slave (Server) — AM kontrolör SCADA/HMI'a register açar:**
1. Device Tree → Ethernet arayüzü → Add Device → **Modbus TCP Slave Device**.
2. General: Port=502, Unit ID, register sayıları (HR/IR/Coil/DI). Holding sayısını
   ihtiyacın ~1.5 katı seç (yedek pay).
3. `GVL_Modbus` oluştur (HR→WORD, Coil→BOOL ...), I/O Mapping ile offset'leri bağla.
   Offset 0 = protokol adres 0 (belgedeki 40001 = adres 0).
4. **Bus Cycle Task** ata (Task_Slow, ~100 ms). Atanmazsa I/O görüntüsü güncellenmez —
   en sık yapılan hata.
5. `PRG_ModbusUpdate` ile yön disiplinini koru: master yazar→PLC okur (HR); PLC yazar→
   master okur (IR). Aynı register'ı iki taraf yazmasın.

**Master (Client) — AM kontrolör başka cihazları (VFD, sayaç) okur:**
1. Device Tree → Ethernet → Add Device → **Modbus TCP Master** → altına **Modbus TCP Slave**
   (uzaktaki cihaz) ekle.
2. Slave altında **Modbus Channel** tanımla: FC (Read Holding Registers=FC03 vb.), başlangıç
   adresi, uzunluk, trigger (Cyclic / Rising edge).
3. Channel'ları GVL'ye I/O Mapping ile bağla. Float için iki register'ı tek FC16/FC03 ile
   birlikte oku/yaz (word tearing'e karşı) ve endian'ı bilinen değerle test et.

### 2) Modbus RTU — RS485 (Master/Slave)

AM400'de 1, AM600'de 2 RS485 portu vardır; dahili Modbus RTU master/slave protokolü destekler.

1. Device Tree → ilgili **COM Port / Serial** cihazını ekle → **Modbus_COM** (port: COM1/COM2,
   baud, parity, stop bits — iki uçta da aynı olmalı).
2. **Master:** Modbus_COM → Modbus_Master → Modbus_Slave → Modbus_Channel (TCP master ile
   aynı channel mantığı). **Slave:** Modbus Serial Device ekle, Unit ID + register.
3. Wiring: A/B (D+/D-) doğru, hat sonu ~120 Ω terminasyon, uzun hatta blendaj + ortak GND.
   "Veri yok / çöp" şikâyetlerinin çoğu baud/parity uyuşmazlığı veya terminasyon eksikliğidir.

### 3) OPC UA Server

CODESYS OPC UA server akışıyla aynıdır (bkz. `knowledge/protocols/opc-ua/05_codesys_server_config.md`).

> **LİSANS/SÜRÜM UYARISI (DOĞRULANMADI):** Jenerik CODESYS'te OPC UA Server **ayrı bir
> runtime eklentisidir** (CODESYS OPC UA Server SL). Inovance bunu bazı AM serisi
> firmware'lerinde gömülü sunabilir; bu **ürün + firmware + InoProShop sürümüne göre
> değişir** ve burada tahmin edilmemiştir. Devreye almadan önce hedef cihazda OPC UA
> seçeneğinin etkin olduğunu ve sunucunun gerçekten başladığını teyit et. Lisans yoksa
> Symbol Configuration görünse bile sunucu yayın yapmayabilir.

1. Application → Add Object → **Symbol Configuration** → "**Support OPC UA features**" işaretle.
2. Yayınlanacak değişkenleri seç ve erişim ata: komutlar (xStartCmd) ReadWrite, geri
   bildirimler (xMotorFB) Read. Yalnızca gerekeni aç (sembol patlaması = bootapp şişer +
   saldırı yüzeyi).
3. **Build → Download** (sadece Build yetmez; yeni semboller indirilmeden adres uzayında
   görünmez).
4. Varsayılan port **4840** (`opc.tcp://<PLC-IP>:4840`). UaExpert ile bağlanıp
   Objects/DeviceSet altında sembolleri doğrula, NodeId'leri not al.
5. **Güvenlik:** SP17+ runtime'larda anonim erişim varsayılan kapalıdır; sertifika + kullanıcı
   kimliği gerekir. Üretimde MessageSecurityMode = SignAndEncrypt, Basic256Sha256.
6. **NodeId kırılganlığı:** Namespace index'i istemcide hardcode etme; URI'dan dinamik al.
   CODESYS URI'si: `http://www.3s-software.com/schemas/Codesys-V3`.

### 4) CANopen (Master + EDS)

AM400/AM600'ün CAN portu CANopen/CANlink destekler (≤1 Mbit/s). CANopen master akışı CODESYS ile aynıdır.

1. EDS/DCF dosyasını al (cihaz üreticisinden) → Device Repository'ye **Install** et.
2. Device Tree → CAN arayüzü ekle → **CANbus** (baud rate seç; 1 Mbit/s ≤ ~25 m hat) →
   altına **CANopen_Manager** (master) ekle.
3. CANopen_Manager altına EDS'ten gelen **slave node**'ları ekle, her birine benzersiz
   **Node-ID** ver.
4. Her slave için **PDO Mapping** (devirsel proses verisi → I/O Mapping ile GVL'ye) ve
   gerekirse **SDO** (başlangıç parametreleri / async erişim). Heartbeat / Node Guarding
   ile node izleme aç.
5. PDO = gerçek zamanlıya yakın devirsel veri (Bus Cycle Task'ta); SDO = bloke edebilen
   async erişim, kontrol döngüsünde değil. CANlink, Inovance'ın kendi CAN protokolüdür —
   CANopen ile karıştırma; üçüncü taraf cihaz CANopen kullanır.

### 5) Socket Haberleşmesi (ham TCP/UDP — SysSocket)

Standart protokoller (Modbus/OPC UA) yetmediğinde (barkod okuyucu, kamera, legacy/özel
protokol) son çare. CODESYS SysSocket / Net Base Services kütüphaneleriyle aynıdır
(bkz. `knowledge/codesys/networking/03_tcp_socket.md`).

1. Library Manager → **CAA Net Base Services** (veya SysSocket) ekle.
2. Bir FB içinde socket aç (SysSockCreate), bağlan/dinle, gönder/al, **her hata yolunda
   SysSockClose** (handle/fd sızıntısı en yaygın tuzak).
3. **Freewheeling task'ta çalıştır** — connect bloke edebilir, ana kontrol task'ını dondurur.
4. **Framing kendin yapılır:** 1 recv = 1 mesaj değildir. Uzunluk-başlıklı veya
   ayraç-tabanlı bir accumulator (tampon) kur; yarım/birleşik paketleri çöz.
5. Half-open bağlantıyı (kablo koptu) yakalamak için uygulama-seviyesi heartbeat/keepalive.

### 6) HMI Bağlantısı — IT7000 ↔ AM400/AM600

Inovance IT7000 serisi HMI, **InoTouchPad** ile programlanır ve OPC UA, Modbus RTU/TCP,
MQTT köprü protokollerini destekler. PLC ile bağlantı bu köprü protokollerinden biri üzerinden kurulur.

**Köprü protokol seçimi:**
- **Modbus TCP (en yaygın, en basit):** AM kontrolörde Modbus TCP **Slave** kur (yukarıdaki
  adım 1). IT7000'i InoTouchPad'de Modbus TCP master/istemci olarak yapılandır, PLC IP +
  port 502 + register haritası gir. HMI register okur/yazar.
- **OPC UA (zengin/güvenli, lisans gerekebilir):** AM'de OPC UA server (adım 3), IT7000
  OPC UA client. NodeId tabanlı; lisans uyarısı geçerli.
- **Modbus RTU (RS485):** Panodan kablo çekmeden seri bağlantı gerekiyorsa; AM RS485
  portunu kullan.

> **İlke — HMI'a mantık gömülmez:** IT7000 yalnızca bir **görüntüleme/komut** katmanıdır.
> Kilitlemeler, emniyet mantığı, sıralama, hesaplama PLC'de (AM kontrolör) kalmalı. HMI'ın
> görevi PLC'deki GVL değişkenlerini göstermek ve operatör komutlarını PLC'ye iletmektir.
> Mantık HMI'a kayarsa: (a) HMI çevrimdışıyken makine güvenliğini kaybeder, (b) iki ayrı
> ortamda (InoProShop + InoTouchPad) çift bakım doğar, (c) "tek doğruluk kaynağı" PLC olma
> ilkesi bozulur. HMI'daki etiketler daima PLC GVL'sindeki bir değişkenle eşlenmelidir.

## Örnekler

**Senaryo:** AM600 bir paketleme makinesi kontrol ediyor. IT7000 HMI hız setpoint'i ve
durum gösteriyor; üst katmanda SCADA OPC UA ile izliyor; bir eski enerji sayacı RS485
Modbus RTU üzerinden okunuyor; EtherCAT servoları sürüyor.

```
AM600
├── EtherCAT Master ............ SV660N servolar (GERÇEK ZAMAN — kontrol)
├── Modbus TCP Slave (port 502)
│     GVL_Modbus: wSpeedSP(HR0)←HMI yazar, wActualSpeed(IR0)→HMI okur, wStatus(IR3)
│     Bus Cycle Task: Task_Slow (100 ms)
├── Modbus RTU Master (RS485-1)
│     Channel: FC04, enerji sayacından V/I/kWh oku (Freewheeling/yavaş)
├── OPC UA Server (port 4840)  [LİSANS DOĞRULA]
│     Symbol Config: GVL_Diagnostics(Read) + GVL_HMI(ReadWrite) — daraltılmış
│     SCADA subscription (SignAndEncrypt)
└── Task Configuration
      Task_EtherCAT (senkron)  → motion (bloke-I/O YASAK)
      Task_Slow (100 ms)       → PRG_ModbusUpdate (slave bus cycle)
      Task_Background (Freewheel) → Modbus RTU master, varsa socket FB

IT7000 (InoTouchPad)
└── Modbus TCP istemci → AM600:502
      Hız etiketi  → HR0 (wSpeedSP)
      Durum lambası → IR3 bit0 (çalışıyor)
      MANTIK YOK — sadece görüntüleme/komut
```

ST tarafında yön disiplini (Modbus slave, Task_Slow):
```iecst
// PLC → master yönü (IR salt okunur, master için)
GVL_Modbus.wActualSpeed := REAL_TO_WORD(rSpeed * 10.0);
IF xRunning THEN GVL_Modbus.wStatus := GVL_Modbus.wStatus OR 16#0001;
ELSE             GVL_Modbus.wStatus := GVL_Modbus.wStatus AND NOT 16#0001;
END_IF
// master → PLC yönü (HR'ı SADECE master yazar; burada yalnız okunur)
rSpeedSP := WORD_TO_REAL(GVL_Modbus.wSpeedSP) / 10.0;
```

## Sık Yapılan Hatalar

- **Modbus Slave'e Bus Cycle Task atamamak:** Cihaz eklenir, değerler güncellenmez.
  I/O Mapping → Bus Cycle Task = Task_Slow.
- **Holding Register'ı PLC kodu ile ezmek:** Master setpoint yazar, PLC her scan'de
  üzerine yazar → komut "kaybolur". Tek-yön kuralı: HR yalnız master, geri besleme IR.
- **OPC UA'da Build yapıp Download unutmak:** Yeni semboller adres uzayında görünmez.
- **OPC UA lisansını varsaymak:** Symbol Configuration görünür ama sunucu yayın yapmaz.
  Hedef AM cihazında OPC UA eklentisinin etkin olduğunu teyit et (DOĞRULANMADI maddesi).
- **Socket connect'i ana task'ta çağırmak:** Bloke edince EtherCAT/kontrol task'ı kaçırır,
  watchdog atar. Freewheeling task'a taşı.
- **"1 recv = 1 mesaj" varsaymak (socket):** Yarım/birleşik paket → bozuk veri. Accumulator
  + framing şart.
- **CANopen ile CANlink'i karıştırmak:** CANlink Inovance'a özel; üçüncü taraf CANopen
  cihaz CANopen Manager altında EDS ile eklenir. Yanlış protokol = node hiç görünmez.
- **RS485 baud/parity/terminasyon:** İki uçta ayar aynı olmalı; hat sonu 120 Ω. En sık
  "seri veri gelmiyor" nedeni.
- **HMI'a mantık gömmek:** IT7000'de kilit/sıralama yazmak → çift bakım + güvenlik riski.
  Mantık PLC'de kalır.

## Ne Zaman Tercih Edilmeli / Edilmemeli

```
İhtiyaç                                   → Kanal           Gerekçe
─────────────────────────────────────────────────────────────────────────────
IT7000 HMI bağlantısı (basit, hızlı)      → Modbus TCP      evrensel, register, kolay
SCADA/MES + güvenlik + zengin model       → OPC UA          subscription, AES, semantik
Eski cihaz / VFD / sayaç (RS485)          → Modbus RTU      dahili, evrensel
Sürücü/IO node (üçüncü taraf, CAN)        → CANopen         EDS, PDO/SDO
Barkod/kamera/özel protokol               → Socket (SysSock) standart yetmiyorsa son çare
Servo senkronizasyon / motion             → EtherCAT        gerçek zaman (bu belge değil)

Kaçın:
✗ OPC UA/Modbus ile motion senkronize etmek → EtherCAT/CANopen PDO kullan
✗ Standart varken socket yazmak             → bakım yükü, framing riski
✗ HMI'a kontrol mantığı koymak              → PLC tek doğruluk kaynağı
```

## Gerçek Proje Notları

- **InoProShop ≈ CODESYS olduğu için bilgi transferi tamdır:** Bu belgedeki her adımın
  ayrıntısı `knowledge/protocols/` ve `knowledge/codesys/networking/` belgelerinde daha
  derindir. InoProShop'a özgü olan tek pratik fark, Inovance cihazlarının (AM kontrolör,
  IT7000) havuzda hazır gelmesidir; üçüncü taraf cihaz yine EDS/GSDML/ESI ile eklenir.
- **OPC UA lisansı sahada sürpriz çıkarır:** Topluluk forumlarında "geliyor/gelmiyor"
  çelişkisi vardır (bkz. frontmatter ÇELİŞKİLER). Teklif/şartname aşamasında OPC UA
  gereksinimi varsa, hedef AM modeli ve firmware'i için OPC UA Server desteğini Inovance
  ile yazılı teyit et — sahada "sunucu başlamıyor" ile uğraşmaktan iyidir.
- **HMI köprüsü için Modbus TCP çoğu projede yeterlidir:** IT7000 OPC UA da destekler, ama
  HMI↔PLC gibi tek-tüketicili, fabrika-içi, basit bir bağ için Modbus TCP daha az kurulum
  ve daha az lisans riski getirir. OPC UA'yı SCADA/MES katmanına sakla.
- **Tek kontrolör, çok kanal disiplini:** Sahadaki "değer geç görünüyor / takılıyor"
  şikâyetlerinin çoğu ağ değil **task** kaynaklıdır: Modbus Bus Cycle Task'ı çok yavaş,
  OPC UA sampling < task cycle, ya da bloke-I/O yanlış task'ta. Önce task yerleşimini
  kontrol et.

## İlgili Konular

- `01_inoproshop_overview.md` — InoProShop = CODESYS V3 tabanı (önkoşul)
- `04_hardware_configuration.md` — AM400/AM600 donanım arayüzleri, cihaz havuzu
- `knowledge/protocols/modbus-tcp/_synthesis.md` — Modbus TCP derinlemesine (register, FC, slave)
- `knowledge/protocols/opc-ua/_synthesis.md` — OPC UA mimari, güvenlik, subscription, sunucu
- `knowledge/codesys/networking/_synthesis.md` — dört protokolün eksen/ilke sentezi (Modbus, OPC UA, socket, MQTT)
- `knowledge/codesys/networking/03_tcp_socket.md` — SysSock TCP/UDP, framing, Freewheeling
