---
KONU        : Endüstriyel Protokoller — Karşılaştırmalı Üst Sentez
KATEGORİ    : protocols
ALT_KATEGORI: protocols
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/protocols/opc-ua/_synthesis.md"
    başlık: "OPC UA Sentezi"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/modbus-tcp/_synthesis.md"
    başlık: "Modbus TCP Sentezi"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/tcp-socket/_synthesis.md"
    başlık: "TCP Socket Sentezi"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/mqtt/_synthesis.md"
    başlık: "MQTT Sentezi"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/protocols/opc-ua/_synthesis.md"
    ilişki: detaylandırır (OPC UA uçtan uca — mimari, güvenlik, subscription, CODESYS)
  - konu: "knowledge/protocols/modbus-tcp/_synthesis.md"
    ilişki: detaylandırır (Modbus TCP — register modeli, FC'ler, CODESYS slave, pymodbus)
  - konu: "knowledge/protocols/tcp-socket/_synthesis.md"
    ilişki: detaylandırır (Ham TCP — SysSock, framing, özel protokol tasarımı)
  - konu: "knowledge/protocols/mqtt/_synthesis.md"
    ilişki: detaylandırır (MQTT — pub/sub, Sparkplug B, UNS, broker seçimi)
  - konu: "knowledge/codesys/fundamentals/_synthesis.md"
    ilişki: önkoşul
ÖNKOŞUL     :
  - "Temel ağ kavramları: TCP/IP, port, LAN/WAN"
  - "Endüstriyel otomasyon katmanları: Fieldbus / SCADA / MES / Bulut"
ÇELİŞKİLER :
  - kaynak: "mqtt/_synthesis.md vs opc-ua/_synthesis.md — Rakip protokol algısı"
    konu: "MQTT ve OPC UA rakip değil, katmanlı mimari bileşenleridir"
    çözüm: >
      OPC UA: Cihaz-SCADA katmanı (bidirectional, semantik, metod çağrısı, güvenlik).
      MQTT: Veri toplama-bulut katmanı (pub/sub, çok alıcı, ölçeklenebilir).
      En olgun mimari ikisini birlikte kullanır; OPC UA PubSub, MQTT'yi transport olarak kullanabilir.
  - kaynak: "modbus-tcp/_synthesis.md — Güvenlik yokluğu"
    konu: "Modbus TCP protokol düzeyinde hiçbir güvenlik mekanizması sunmaz"
    çözüm: >
      Ağ mimarisi düzeyinde güvenlik sağlanır: VPN, güvenlik duvarı, ağ segmentasyonu.
      2024 FrostyGoop saldırısı: Port 502 internete açık → fiziksel hasar.
  - kaynak: "tcp-socket/_synthesis.md — connect() blocking istisnası"
    konu: "CODESYS'te SysSockConnect non-blocking moda alınan socket'ta bile her zaman blocking çalışır"
    çözüm: >
      connect() çağrısını Task_Control'e koyma; Freewheeling/Task_Background'da çalıştır.
      Task_Control'de connect() tüm PLC'yi dondurur, Watchdog tetikler, motorlar durur.
---

## Özün Ne

Bu üst sentez, "Elimde bir entegrasyon problemi var — hangi protokolü seçmeliyim ve neden?" sorusunu yanıtlar. Dört protokol alt sentezinin (OPC UA, Modbus TCP, Ham TCP Socket, MQTT) bağımsız olarak anlaşıldığı varsayılarak bu belgede yalnızca aralarındaki **karşılaştırma, seçim rehberi ve gerçek mimari kararlar** sunulur. Aynı sorunu farklı protokollerle çözmenin sonuçları gerçek proje deneyimine dayanır.

---

## Nasıl Çalışır

### Dört Protokolün Konumlandırma Haritası

```
OT (Operasyonel Teknoloji) içi ────────────── IT/Bulut katmanı ────►

  HAM TCP SOCKET          MODBUS TCP          OPC UA              MQTT
  ─────────────────────── ─────────────────── ─────────────────── ───────────────────
  Özel cihaz protokolü    Legacy alan otom.   PLC-SCADA-MES       Bulut / Multi-hedef
  Framing sende          Register tabanlı    Semantik bilgi mod. Pub/sub broker
  2 nokta                Request-Response    Request-Response    Push (Publisher'dan)
  En düşük overhead      +  subscriber       +  zengin tip       N:N fanout

        STRUCTURED (Şemalı veri) ──────────────────────────────────────────────────►

  En ham                 16-bit registerlar  NodeId + DataType   Topic + Payload
  Protokol tasarımcı     Tip yok (UINT16)    OOP veri modeli     JSON / Protobuf
  belirler               Float = 2 register  Struct, Enum, Array Sparkplug B ile şema


        REQUEST / RESPONSE ──────────────► PUB / SUB ──────────────────────────────►

  Ham TCP (tercihe göre) Modbus TCP          OPC UA Subscription MQTT
  her iki model olabilir  R/R zorunlu         R/R + Push model    Saf pub/sub
```

### Mental Model: 4 Protokolü Aklında Tutan Tek Çerçeve

```
  Soru 1: "Karşı taraf ne destekliyor?"
    → Modbus TCP : Legacy VFD, enerji sayacı, akıllı röle, eski SCADA → MODBUS TCP
    → OPC UA     : Modern PLC (Siemens, B&R, Beckhoff, CODESYS)       → OPC UA
    → MQTT       : IoT sensörü, AWS/Azure hedefi, cloud gateway        → MQTT
    → Hiçbiri    : Özel binary protokol, barkod okuyucu, robot kont.  → HAM TCP

  Soru 2: "Kaç alıcı var ve yön ne?"
    → 1 alıcı, bidirectional (setpoint yaz + ölçüm oku)               → MODBUS TCP veya OPC UA
    → 1 alıcı, SCADA kontrol + semantik model + güvenlik              → OPC UA
    → N alıcı (SCADA + historian + bulut + dashboard aynı anda)       → MQTT
    → 2 PLC arası özel köprü                                           → HAM TCP

  Soru 3: "Güvenlik kritik mi?"
    → Evet, IEC 62443 / NIS2 uyumluluk gerekli                        → OPC UA (SignAndEncrypt)
    → Evet ama sadece şifreleme yeterli                                → MQTT (TLS 8883)
    → Sadece ağ segmentasyonu                                          → MODBUS TCP
    → Kontrollü LAN ortamı, 2 cihaz                                   → HAM TCP

  Soru 4: "Veri ne kadar zengin?"
    → 16-bit integer/float, basit setpoint-ölçüm                      → MODBUS TCP
    → Semantik model, struct, metod çağrısı, otomatik keşif           → OPC UA
    → Büyük binary payload (görüntü, dalga şekli)                     → HAM TCP
    → JSON/Protobuf, değişken yapı, metadata                          → MQTT (Sparkplug B)
```

---

## Hızlı Referans Tabloları

### Tablo 1 — Senaryo → Protokol Seçim Rehberi (KRİTİK)

| Senaryo | Önerilen Protokol | Gerekçe |
|---|---|---|
| PLC → SCADA veri aktarımı (standart) | **OPC UA** | Semantik model, çok istemci, güvenlik |
| PLC → SCADA + MES + ERP zinciri | **OPC UA** | Companion Spec, metod çağrısı, hiyerarşi |
| Legacy VFD / enerji sayacı entegrasyonu | **Modbus TCP** | Cihaz zaten Modbus konuşuyor |
| Eski SCADA yalnızca Modbus biliyor | **Modbus TCP** | Başka seçenek yok |
| PLC → InfluxDB + Grafana + AWS aynı anda | **MQTT** | Pub/sub, N alıcı, broker fanout |
| Unified Namespace (UNS) mimarisi | **MQTT** | Merkezi veri havuzu, OPC UA ile katmanlı |
| Bulut platform entegrasyonu (AWS IoT, Azure IoT) | **MQTT** | Native cloud protokolü |
| Uzak izleme, 4G/LTE kısıtlı bant | **MQTT** | Minimum overhead, bağlantısız QoS |
| Barkod okuyucu / özel cihaz entegrasyonu | **Ham TCP** | Standart protokol desteklenmiyor |
| İki PLC arası özel düşük-gecikmeli veri köprüsü | **Ham TCP** | Overhead yok, protokol tasarım özgürlüğü |
| Üretici özel binary protokolü | **Ham TCP** | Tersine mühendislik + adaptasyon |
| OPC UA + çok alıcı ölçeklenebilir dağıtım | **OPC UA PubSub (MQTT transport)** | İki dünyanın birleşimi |
| Gerçek zamanlı motion control (< 1ms) | **EtherCAT / PROFINET** | Hiçbiri yetmez; fieldbus kullan |

---

### Tablo 2 — Protokol × Özellik Matrisi

| Özellik | OPC UA | Modbus TCP | Ham TCP Socket | MQTT |
|---|---|---|---|---|
| **Standart port** | 4840 | 502 | Serbest (10000–20000 önerilir) | 1883 (TLS: 8883) |
| **İletişim modeli** | İstemci-Sunucu + PubSub | Master-Slave (R/R) | Serbest (R/R veya push) | Pub/Sub (broker) |
| **Güvenlik** | Yerleşik (PKI, TLS, rol) | Yok (ağ katmanı) | Yok (uygulama katmanı ekle) | TLS opsiyonel |
| **Otomatik keşif** | Var (Browse, NodeId, Companion Spec) | Yok | Yok | Yok (Sparkplug B ile kısmi) |
| **Latency (LAN)** | Düşük (< 10ms) | Çok düşük (< 5ms) | En düşük (< 1ms) | Düşük (< 10ms) |
| **Standartlaşma** | IEC 62541, OPC Foundation | Modicon 1979, defacto standart | Yok (OS socket API) | OASIS MQTT 3.1.1 / 5.0 |
| **Veri tipi zenginliği** | Çok zengin (struct, enum, method) | Zayıf (16-bit, float=2 register) | Tasarıma bağlı | Orta (JSON/Protobuf) |
| **N istemci aynı anda** | Evet (session yönetimi) | Evet (ama polling karmaşıklaşır) | Evet (server ise) | Evet (broker fanout, doğal) |
| **Push bildirimi** | Evet (Subscription / MonitoredItem) | Hayır (polling zorunlu) | Evet (tasarıma bağlı) | Evet (broker push, doğal) |
| **Bağlantısız çalışma** | Hayır | Hayır | Hayır | Evet (QoS 1-2 + session) |
| **Uygulama karmaşıklığı** | Yüksek (PKI, namespace, session) | Düşük (register + FC) | Orta-Yüksek (framing, state machine) | Orta (broker, topic tasarımı) |
| **CODESYS desteği** | Yerleşik (Symbol Config) | Yerleşik (Slave Device) | SysSock kütüphanesi | CODESYS MQTT Client kütüphanesi |
| **Tipik kullanım katmanı** | OT: PLC ↔ SCADA/MES | OT: Alan cihazı ↔ PLC/SCADA | OT: Özel cihaz entegrasyonu | IT: SCADA ↔ Bulut / historian |

---

### Tablo 3 — Veri Tipi ve Karmaşıklık Karşılaştırması

| Veri İhtiyacı | OPC UA | Modbus TCP | Ham TCP | MQTT |
|---|---|---|---|---|
| Boolean (bit) | `Boolean` NodeId | Coil (1-bit) veya HR bit | 1 byte min | Payload string/byte |
| 16-bit tam sayı | `Int16` / `UInt16` | Holding Register doğrudan | 2 byte big-endian | JSON `"value": 42` |
| 32-bit float | `Float` (tek node) | 2 Holding Register, byte order dikkat | 4 byte big-endian | JSON `"value": 3.14` |
| String | `String` NodeId | N register (2 char/register) | N byte, delimiter veya length | Payload string |
| Struct / record | `ObjectType` + Variables | İmkânsız (birden fazla register) | Tasarıma bağlı | JSON object |
| Enum | `DataType Enum` | Bit maskesi / sayısal kod | Sayısal byte | String veya integer |
| Metadata (birim, aralık) | Address Space'te Property node | Yok, dış dökümantasyon | Yok, protokol tasarımı | Sparkplug B NBIRTH |
| Metod çağrısı | `Method` node (CallService) | Yok | Mesaj tipi olarak tasarla | Yok (topic tabanlı komut) |
| Değişim bildirimi | MonitoredItem / Subscription | Yok (polling) | Tasarıma bağlı (push) | Broker push (doğal) |

---

## Pratikte Nasıl Kullanılır

### Tipik Endüstriyel Mimari: Her Protokol Nerede?

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  BULUT / KURUMSAL KATMAN (ERP, AWS IoT, Azure, analitik)                 │
  │                                                                          │
  │           MQTT (TLS 8883, Sparkplug B veya JSON)                         │
  │           Subscriber: InfluxDB, Grafana, AWS IoT Core, MES               │
  └──────────────────────────────┬───────────────────────────────────────────┘
                                 │ MQTT Broker (HiveMQ / EMQX / Mosquitto)
                                 │ Tek merkezi veri havuzu
  ┌──────────────────────────────┴───────────────────────────────────────────┐
  │  SCADA / MES KATMANI (Ignition, Wonderware, Node-RED)                    │
  │                                                                          │
  │    OPC UA Client ────────────────────────────────────── MQTT Subscriber  │
  │    Bidirectional: setpoint yaz, alarm onayla            Historian'a yaz  │
  │    Semantik model, metod çağrısı, güvenlik              Sadece okuma     │
  └──────────────────────────────┬───────────────────────────────────────────┘
                                 │ opc.tcp://PLC-IP:4840
  ┌──────────────────────────────┴───────────────────────────────────────────┐
  │  PLC KATMANI (CODESYS, Siemens, B&R, Beckhoff)                           │
  │                                                                          │
  │  OPC UA Server ──── MQTT Publisher ──── Modbus TCP Slave ─── TCP Socket  │
  │  (Symbol Config)    (Task_Background)   (Slave Device)       (SysSock)   │
  │       │                   │                   │                  │       │
  │  SCADA'ya              Broker'a           Legacy SCADA'ya    Özel cihaza  │
  │  zengin veri           push yayın         register okuma     protokol    │
  └──────────┬──────────────────┬─────────────────┬─────────────────┬────────┘
             │                  │                 │                 │
  ┌──────────▼──────────────────▼─────────────────▼─────────────────▼────────┐
  │  ALAN CİHAZI KATMANI                                                     │
  │                                                                          │
  │  [EtherCAT I/O]  [Modbus RTU VFD]  [Modbus TCP Enerji Sayacı]  [TCP Cihaz]│
  │  Gerçek zamanlı  Legacy sürücü     Enerji izleme               Barkod     │
  │  fieldbus        FC63 RTU-TCP      FC03 HR oku                 okuyucu    │
  └──────────────────────────────────────────────────────────────────────────┘
```

### Gerçek Proje Mimarisi — OPC UA + MQTT Birlikte

```
  CODESYS PLC (192.168.1.100)
    │
    ├─ OPC UA Server (port 4840)
    │    Symbol Config → GVL_IO değişkenleri → NodeId'ler
    │    Güvenlik: Basic256Sha256 + SignAndEncrypt
    │    → SCADA (Ignition) ← OPC UA Client → setpoint yaz, alarm onayla
    │
    ├─ MQTT Publisher (Task_Background, 500ms)
    │    factory/istanbul/line1/motor1/speed   (QoS 0, retain=False)
    │    factory/istanbul/line1/motor1/alarm   (QoS 1, retain=False)
    │    factory/istanbul/line1/status/online  (QoS 1, retain=True, LWT="false")
    │    → Broker (EMQX) → InfluxDB, Grafana, AWS IoT Core
    │
    └─ Modbus TCP Slave (port 502, Unit ID=1)
         HR 0 = Hız setpoint   (SCADA/Legacy ister)
         IR 0 = Gerçek hız     (SCADA okur)
         → Legacy SCADA sistemi (Modbus TC istemcisi)
```

---

## Sık Yapılan Hatalar

### Hata 1: Yanlış Katmanda Yanlış Protokol

```
Senaryo: SCADA PLC'ye setpoint yazmak için MQTT kullanılıyor.
Sorun  : MQTT pub/sub'da komut yönü belirsiz; broker erişim kontrolü
         zayıfsa herhangi bir publisher setpoint değiştirebilir.
         Metod çağrısı yok; "yaz" ve "yazma başarıldı onayı" zinciri kurulamaz.
Çözüm  : SCADA ↔ PLC bidirectional kontrol için OPC UA. MQTT yalnızca
         "PLC'den çıkan veri" yönünde (publisher = PLC, subscriber = bulut/historian).
```

### Hata 2: Modbus TCP'yi "Güvenli Yeter" Diyerek İnternete Açmak

```
Senaryo: Port 502 NAT arkasında açık bırakıldı.
Referans: 2024 FrostyGoop saldırısı — Ukrayna'da ısıtma sistemi.
Etki   : Saldırgan Modbus komutları göndererek fiziksel hasar oluşturdu.
Kural  : Modbus TCP protokol düzeyinde sıfır güvenlik. Ağ katmanı zorunlu:
         VPN, güvenlik duvarı, VLAN segmentasyonu, port 502 internete hiçbir zaman.
```

### Hata 3: OPC UA'yı "Pahalı Modbus" Olarak Kullanmak

```
Senaryo: OPC UA kuruldu ama Address Space düz liste — 300 değişken aynı seviyede.
         NodeId'ler hardcode, namespace index hardcode (ns=4).
         Subscription yok; polling döngüsü ile sürekli read_value.
Etki   : OPC UA'nın tüm avantajları (keşfedilebilirlik, semantik, push) kullanılmıyor.
         Sistem karmaşık ama Modbus'tan daha zayıf.
Çözüm  : Hiyerarşik adres uzayı tasarımı (Device→Unit→Measurement→Value).
         get_namespace_index(URI) ile dinamik ns. Subscription kullan.
```

### Hata 4: Ham TCP'de Framing Yapmamak

```
Senaryo: CODESYS SysSockRecv() her çağrısında tam mesajın geldiği varsayılıyor.
Etki   : TCP stream davranışı — send(100 byte) recv() ile 30+70 byte gelebilir.
         Parser bozulur; hatalı komutlar işlenir, rastgele veri bozulması.
Kural  : Her ham TCP protokolünde akümülatör buffer + state machine parser zorunlu.
         SOH + LENGTH + CHECKSUM üçlüsü minimum çerçeve.
```

### Hata 5: MQTT Topic'i Başta Düz Tasarlamak

```
Senaryo: Pilot projede topic: "temp1", "speed_motor2" — düz, anlamsız.
Etki   : Fabrika büyüyünce wildcard imkânsız; subscriber'lar tek tek güncellendi.
         InfluxDB eski yapıda veri; Grafana bozuldu. 2 günlük migrasyon.
Kural  : ISA-95 tabanlı hiyerarşiyi başlangıçta kur.
         enterprise/site/area/line/cell/device/datapoint — bir daha değişmez.
```

### Hata 6: CODESYS'te connect() Task_Control'e Koymak

```
Senaryo: FB_TcpClient Task_Control (10ms, Prio:2) içinde çalışıyor.
         Hedef cihaz geçici olarak erişilemez.
Etki   : SysSockConnect her zaman BLOCKING — non-blocking moda alınsa bile.
         Task_Control 20 saniye dondu → Watchdog → tüm motorlar durdu.
         Gerçek üretim ortamında yaşandı.
Kural  : connect() çağrısı Task_Background (Freewheeling/Prio:10) içinde.
         Task_Control yalnızca GVL üzerinden xConnected flag'ini okur.
```

### Hata 7: Modbus TCP Adres Kayması (Off-by-One)

```
Senaryo: Belge "HR 40001 = Voltage Phase A" diyor. Kod address=40001 yazıyor.
Etki   : Exception 0x02 (Illegal Data Address). Veri hiç gelmiyor.
Kural  : address = belge_no - 40001 (0-tabanlı protokol vs 1-tabanlı belge notasyonu).
         pymodbus her zaman 0-tabanlı. SCADA araçlarının hangi konvansiyonu
         kullandığını kontrol et.
```

### Hata 8: MQTT'de LWT Olmadan Deploy

```
Senaryo: PLC beklenmedik kesildi. Dashboard 2 saat "Online" gösterdi.
Etki   : Operatör makineye gitti — kimse yok, alarm yok.
Kural  : Her MQTT bağlantısında LWT zorunlu:
         LWT Topic:   factory/.../status/online
         LWT Payload: "false"  QoS: 1  Retain: True
         Bağlanınca:  "true" yayınla (QoS 1, retain=True)
```

---

## Ne Zaman Hangisi

### OPC UA Seç

```
✓ PLC → SCADA / MES / ERP katmanı arası veri iletimi (standart senaryo)
✓ Birden fazla istemci aynı anda aynı veriye erişecek
✓ Güvenlik zorunlu: NIS2, IEC 62443, ISO 27001
✓ Semantik veri modeli gerekiyor (makinenin kendini tanımlaması)
✓ SCADA'nın setpoint yazması, alarm onaylaması gerekiyor (bidirectional kontrol)
✓ Method çağrısı gerekiyor (StartRecipe, Reset, Calibrate)
✓ Companion Specification uyumluluğu (robotik, CNC, ilaç)
✓ Platform bağımsız: Linux PLC → Windows SCADA → Python script

✗ Gerçek zamanlı motion control (EtherCAT/PROFINET kullan)
✗ Kaynak kısıtlı gömülü cihaz, çok basit 2-değer senaryosu (Modbus yeterli)
✗ N alıcıya veri dağıtımı ana ihtiyaçsa (MQTT daha doğal)
```

### Modbus TCP Seç

```
✓ Hedef cihaz Modbus destekliyor ve başka protokol yok
✓ Legacy entegrasyon: VFD, enerji sayacı, sensör, akıllı röle
✓ Eski SCADA yalnızca Modbus istemcisi biliyor
✓ Basit izleme: Birkaç değer periyodik okuma
✓ Hızlı prototip: Minimal kurulum, evrensel kütüphane
✓ Farklı marka cihazlar bir arada (evrensel uyumluluk)

✗ Güvenilir olay bildirimi / push gerekiyorsa (OPC UA Subscription veya MQTT)
✗ Zengin veri tipi semantiği (OPC UA)
✗ Birden fazla bağımsız alıcı (polling yönetimi karmaşıklaşır)
✗ TLS şifreleme zorunluysa (Modbus/TCP Security nadiren desteklenir)
```

### Ham TCP Socket Seç

```
✓ Karşı taraf Modbus TCP, OPC UA, MQTT'yi desteklemiyor
✓ Legacy / özel cihaz: Barkod okuyucu, eski SCADA, özel ölçüm cihazı, robot kontrolcü
✓ Üretici özel binary protokolü tanımlıyor
✓ Büyük binary veri: Görüntü, dalga şekli, blok transfer
✓ İki PLC arası özel düşük-gecikmeli köprü
✓ Mevcut legacy sistemin protokolüne adapte olmak zorundasın

✗ Karşı taraf standart protokol destekliyorsa (önce Modbus/OPC UA/MQTT dene)
✗ Güvenlik (SIL) gereksinimleri varsa (TLS + authenticated protokol gerekli)
✗ Birden fazla ekip üyesi geliştiriyorsa standart protokol tercih et
```

### MQTT Seç

```
✓ Bir verinin aynı anda N alıcıya gitmesi gerekiyor (pub/sub gücü)
✓ Bulut platform entegrasyonu: AWS IoT, Azure IoT Hub, Google Cloud IoT
✓ Unified Namespace (UNS) mimarisi kuruyorsun
✓ Analitik / zaman serisi pipeline: InfluxDB → Grafana
✓ Uzak/kısıtlı bant genişliği: 4G/LTE, düşük güç IoT
✓ Yeni alıcı eklendiğinde PLC kodunun değişmemesini istiyorsun
✓ Sparkplug B ile endüstriyel cihaz metadata standardı

✗ SCADA PLC'ye setpoint yazacak / alarm onaylayacak (OPC UA kullan)
✗ Zengin semantik model veya metod çağrısı gerekiyor (OPC UA)
✗ Broker altyapısı kurulamıyorsa ve 2 cihaz doğrudan iletişim kuracaksa (Modbus TCP)
✗ Gerçek zamanlı kontrol komutları (fieldbus kullan)
```

### Karar Ağacı

```
Entegre edilecek cihaz / senaryo:

    Standart protokol destekliyor mu?
        ├─ Modbus TCP → Modbus TCP (basit, evrensel)
        ├─ OPC UA     → OPC UA (zengin, güvenli)
        ├─ MQTT       → MQTT (push, çok alıcı)
        └─ Hiçbiri    → Ham TCP Socket
                          Cihazı tanı: nc <IP> <port>
                          Protokol ASCII mi, binary mi?

    SCADA ↔ PLC bidirectional kontrol?
        ├─ Evet → OPC UA (setpoint yaz, metod çağır)
        └─ Hayır (yalnızca veri topla) →
              Tek alıcı → OPC UA veya Modbus TCP
              Çok alıcı → MQTT

    Bulut / analitik entegrasyonu?
        ├─ Evet → MQTT (ikincil: OPC UA PubSub)
        └─ Hayır → OPC UA veya Modbus TCP

    Gerçek zamanlı kontrol (< 1ms)?
        → EtherCAT / PROFINET — bu 4 protokolden hiçbiri
```

---

## İlgili Konular

```
knowledge/protocols/
├── opc-ua/_synthesis.md          → OPC UA uçtan uca: mimari, güvenlik, subscription, CODESYS server, Python client
├── modbus-tcp/_synthesis.md      → Modbus TCP: register modeli, FC'ler, CODESYS slave, pymodbus, jsmodbus
├── tcp-socket/_synthesis.md      → Ham TCP: SysSock API, framing, özel protokol tasarımı, state machine
├── mqtt/_synthesis.md            → MQTT: pub/sub, QoS, LWT, Sparkplug B, UNS, broker seçimi
└── _synthesis.md (bu belge)      → Karşılaştırmalı üst sentez

Önkoşul:
knowledge/codesys/fundamentals/_synthesis.md → Device Tree, GVL, Task yapısı

CODESYS ağ implementasyonları:
knowledge/codesys/networking/
├── 01_opcua_server.md            → OPC UA server kurulum rehberi
├── 02_modbus_slave.md            → Modbus TCP slave yapılandırması
├── 03_tcp_socket.md              → SysSock özet implementasyon
└── 04_mqtt_client.md             → MQTT client kurulumu

Gerçek zamanlı fieldbus (bu 4 protokolün altındaki katman):
knowledge/networking/
└── ethercat/                     → < 1ms I/O, motion control

Araçlar:
  UaExpert         → OPC UA browser, NodeId keşif, subscription test
  Modbus Poll      → GUI Modbus master test
  MQTT Explorer    → GUI MQTT browser ve yayın testi
  netcat (nc)      → Ham TCP hızlı protokol keşfi
  Wireshark        → Her protokol trafik analizi (modbus, opc.ua, mqtt, tcp filtreleri)
  pymodbus         → pip install pymodbus (Python Modbus TCP)
  asyncua          → pip install asyncua[crypto] (Python OPC UA)
  paho-mqtt        → pip install paho-mqtt (Python MQTT)
  Python socket    → Ham TCP test client/server (stdlib)
```
