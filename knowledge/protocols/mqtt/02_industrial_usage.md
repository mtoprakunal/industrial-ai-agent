---
KONU        : MQTT Endüstriyel Otomasyon Kullanımı
KATEGORİ    : protocols
ALT_KATEGORI: mqtt
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://www.hivemq.com/resources/iiot-protocols-opc-ua-mqtt-sparkplug-comparison/"
    başlık: "HiveMQ — OPC UA and MQTT Sparkplug Comparison"
    güvenilirlik: topluluk
  - url: "https://www.emqx.com/en/blog/a-comparison-of-iiot-protocols-mqtt-sparkplug-vs-opc-ua"
    başlık: "EMQ — IIoT Protocols: MQTT Sparkplug vs OPC-UA Comparison"
    güvenilirlik: topluluk
  - url: "https://www.manubes.com/mqtt-brokers-comparison/"
    başlık: "Manubes — Comparison of Industrial MQTT Brokers"
    güvenilirlik: topluluk
  - url: "https://teeptrak.com/en/unified-namespace-uns-mqtt-sparkplug-iiot-2027/"
    başlık: "TEEPTRAK — Unified Namespace for Manufacturing 2027"
    güvenilirlik: topluluk
  - url: "https://blanpa.github.io/blog/mqtt-vs-sparkplug-vs-nats-vs-opcua/"
    başlık: "Blanpa Blog — MQTT vs Sparkplug B vs OPC-UA"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_basics.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/networking/04_mqtt_client.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: tamamlar
  - konu: "knowledge/protocols/opc-ua/04_subscriptions.md"
    ilişki: karşılaştırır
ÖNKOŞUL     :
  - "MQTT temelleri (01_basics.md)"
  - "CODESYS MQTT client kurulumu (codesys/networking/04_mqtt_client.md)"
ÇELİŞKİLER :
  - kaynak: "Sparkplug B vs OPC UA PubSub — hangisi endüstriyel MQTT için?"
    konu: "İkisi de endüstriyel MQTT'ye anlam katar ama farklı yöntemlerle"
    çözüm: >
      OPC UA PubSub: OPC UA bilgi modelini MQTT transport üzerinde kullanır.
      Zengin semantik, sertifikalı güvenlik ama karmaşık.
      Sparkplug B: Daha basit Protobuf tabanlı payload, SCADA entegrasyonu güçlü,
      Inductive Automation/Ignition ile doğal uyum. Başlangıç için Sparkplug B daha kolay.
  - kaynak: "MQTT'yi OPC UA'nın tamamen yerine kullanmak"
    konu: "MQTT OPC UA'nın sahip olduğu bazı özelliklere sahip değil"
    çözüm: >
      MQTT: Pub/sub, hafif, broker tabanlı, bulut/IoT ideal.
      OPC UA eksikleri MQTT'de: Semantik veri modeli yok, metod çağrısı yok,
      browse/discovery yok, resmi güvenlik sertifikasyonu yok.
      Doğru mimari: OPC UA cihaz-SCADA katmanında, MQTT bulut katmanında.
      Ya da Sparkplug B her ikisinin güçlerini birleştirir.
---

## Özün Ne

MQTT endüstriyel otomasyonda giderek daha büyük bir rol oynamaktadır — özellikle fabrika verilerini bulut platformlarına, analitik motorlarına ve MES/ERP sistemlerine taşımak için. Ancak "endüstriyel MQTT" yalnızca broker kurup veri göndermekten fazlasıdır: Topic tasarımı, Sparkplug B standardı, güvenlik yapılandırması ve OPC UA ile uyumlu çalışma — bunların hepsi production kalitesinde bir sistem için gereklidir. Bu belge, MQTT'nin endüstriyel bağlamda nasıl kullanıldığını, hangi broker'ların hangi senaryolarda uygun olduğunu ve gerçek projedeki deneyimleri ele alır.

## Ne Zaman Kullanılır

### MQTT'nin Güçlü Olduğu Senaryolar

```
1. Çok alıcılı veri dağıtımı:
   Bir PLC'nin verisini aynı anda SCADA, bulut, mobil,
   analitik motoru ve energy manager'a göndermek.
   → MQTT pub/sub yapısı bunu doğal olarak çözer.
   → Her alıcı bağımsız abone olur; PLC'nin kodu değişmez.

2. Uzak ve düşük bant genişlikli bağlantılar:
   4G/LTE üzerinden fabrika verisi → Merkezî bulut.
   MQTT'nin minimum overhead'ı burada kritik.

3. Farklı üreticilerden cihazları tek noktada toplamak:
   PLC1 (CODESYS) + PLC2 (Siemens) + VFD + Enerji sayacı
   → Hepsi MQTT'ye yayınlar → Tek broker'dan tüm veri.

4. Bulut platformu entegrasyonu:
   AWS IoT Core, Azure IoT Hub, Google Cloud IoT
   → Tamamı MQTT destekler, doğal entegrasyon.

5. Unified Namespace (UNS) mimarisi:
   Tüm fabrika verisi tek MQTT broker'da toplanır.
   Her sistem istediğine abone olur → Noktadan-noktaya
   entegrasyon spaghetti ortadan kalkar.
```

### MQTT'nin ZAYIF Kaldığı Senaryolar

```
MQTT kullanma, OPC UA tercih et:
  ✗ PLC → SCADA doğrudan kontrol (set değer, metod çağır)
  ✗ Zengin semantik veri modeli gerektiğinde
  ✗ OPC UA sertifikalı güvenlik zorunlu olduğunda
  ✗ Gerçek zamanlı motion control komutları
  ✗ Companion specification uyumluluğu gerektiğinde

MQTT kullanma, Modbus TCP tercih et:
  ✗ Eski SCADA yalnızca Modbus biliyor
  ✗ Broker altyapısı yoksa / kurulamazsa
  ✗ Basit 2-cihaz bağlantısı (overkill olur)
```

---

## Broker Seçimi

### Mosquitto (Eclipse)

```
Tür: Açık kaynak, hafif
Lisans: EPL 2.0 / EDL 1.0 (ücretsiz)
Desteklenen MQTT: 3.1, 3.1.1, 5.0

Güçlü Yönler:
  ✓ Çok küçük kaynak tüketimi (Raspberry Pi'da çalışır)
  ✓ Kurulumu kolay (apt install mosquitto)
  ✓ Geniş topuluk ve dokümantasyon
  ✓ Geliştirme, test, küçük-orta ölçek için ideal
  ✓ TLS ve kullanıcı doğrulama desteği

Zayıf Yönler:
  ✗ Yatay ölçekleme yok (tek node)
  ✗ Kurumsal yönetim paneli yok
  ✗ Sparkplug B yerleşik desteği yok

Kullanım: Geliştirme, test ortamı, tek site pilot, fabrika kenarı

Kurulum:
  sudo apt install mosquitto mosquitto-clients
  # Konfigürasyon: /etc/mosquitto/mosquitto.conf

Temel konfigürasyon (/etc/mosquitto/conf.d/production.conf):
  listener 8883
  certfile /etc/mosquitto/certs/server.crt
  keyfile  /etc/mosquitto/certs/server.key
  cafile   /etc/mosquitto/certs/ca.crt
  require_certificate false
  allow_anonymous false
  password_file /etc/mosquitto/passwd
```

### HiveMQ

```
Tür: Kurumsal, kümeleme destekli
Lisans: Ticari (Community Edition ücretsiz ama sınırlı)
Desteklenen MQTT: 3.1, 3.1.1, 5.0

Güçlü Yönler:
  ✓ Yatay ölçekleme (cluster) — milyonlarca bağlantı
  ✓ Sparkplug B ve UNS desteği
  ✓ IEC 62443 uyumlu güvenlik
  ✓ Kapsamlı yönetim paneli ve REST API
  ✓ Extension/plugin framework
  ✓ Kubernetes hazır

Zayıf Yönler:
  ✗ Kurumsal lisans maliyeti
  ✗ Community Edition kısıtlı (25 bağlantı)

Kullanım: Büyük ölçekli üretim, otomotiv, sağlık, çok site
```

### EMQX

```
Tür: Yüksek performans, açık kaynak + kurumsal
Lisans: Apache 2.0 (Community), ticari (Enterprise)
Desteklenen MQTT: 3.1, 3.1.1, 5.0

Güçlü Yönler:
  ✓ 100 milyon+ eş zamanlı bağlantı (Erlang/OTP)
  ✓ Yerleşik kural motoru (SQL benzeri)
  ✓ Çoklu protokol: MQTT, WebSocket, CoAP, LwM2M
  ✓ Veri köprüsü: Kafka, InfluxDB, TimescaleDB entegrasyonu
  ✓ Community Edition kapsamlı

Zayıf Yönler:
  ✗ Erlang bilgisi gerektiren yönetim
  ✗ Kaynak tüketimi HiveMQ'dan yüksek

Kullanım: Büyük veri, IoT platformu, çok protokollü gateway
```

### Broker Seçim Özeti

```
Senaryo                              → Önerilen Broker
──────────────────────────────────────────────────────────
Geliştirme ve test                   → Mosquitto
Tek fabrika, <1000 cihaz             → Mosquitto veya EMQX Community
Çok fabrika, binlerce cihaz          → HiveMQ veya EMQX Enterprise
AWS ekosistemi                       → AWS IoT Core
Azure ekosistemi                     → Azure Event Grid MQTT
Sparkplug B + Ignition SCADA         → Cirrus Link Chariot
Yüksek performans + kural motoru     → EMQX
Kurumsal Avrupa / IEC 62443          → HiveMQ
```

---

## Sparkplug B

### Nedir?

Sparkplug B, MQTT'nin endüstriyel otomasyon için yetersiz kalan yönlerini tamamlayan bir spesifikasyondur. 2016'da Cirrus Link Solutions tarafından geliştirilmiş, şimdi Eclipse Foundation bünyesindedir.

MQTT'nin endüstriyel sorunları:
```
1. Topic özgürlüğü sorun → Herkes farklı topic yapısı kullanır
2. Payload standart yok → JSON, binary, string — herkes farklı
3. Cihaz durumu bilinmiyor → Online mi, offline mi?
4. İlk bağlantıda tüm değerler bilinmiyor
5. Tag metadata yok (birim, veri tipi, açıklama)
```

Sparkplug B çözümleri:
```
1. Standart topic hiyerarşisi:
   spBv1.0/{group_id}/{message_type}/{edge_node_id}/{device_id}
   
   message_type sabit değerler:
     NBIRTH: Edge node doğum mesajı (tüm tag'ler + metadata)
     NDEATH: Edge node ölüm mesajı (LWT)
     NDATA:  Edge node verisi (yalnızca değişenler)
     DBIRTH: Device doğum mesajı
     DDEATH: Device ölüm mesajı
     DDATA:  Device verisi
     NCMD:   Edge node'a komut
     DCMD:   Device'a komut

2. Protobuf payload → Kompakt binary (JSON'dan %80 daha küçük)
3. Report-by-exception → Yalnızca değişen değerler gönderilir
4. Birth/Death sertifikaları → Durum yönetimi
5. Tag metadata → Birim, veri tipi, engineering range
```

### Sparkplug B Mesaj Akışı

```
Edge Node (CODESYS + Sparkplug) ilk bağlantıda:

1. NBIRTH gönder (tüm tag'ler + metadata):
   Topic: spBv1.0/Paketleme/NBIRTH/Line1_PLC
   Payload (Protobuf):
     seq: 0
     timestamp: 1717200000000
     metrics: [
       {name: "ConveyorSpeed", datatype: FLOAT, value: 45.3, unit: "m/min"},
       {name: "Temperature",   datatype: FLOAT, value: 82.5, unit: "°C"},
       {name: "Running",       datatype: BOOL,  value: true}
     ]

2. NDATA yalnızca değişen değerler:
   Topic: spBv1.0/Paketleme/NDATA/Line1_PLC
   Payload:
     seq: 1
     metrics: [
       {name: "Temperature", value: 83.1}  ← Yalnızca bu değişti
     ]
   → Bant genişliği %70-90 azalma

3. Bağlantı kopunca broker NDEATH yayınlar (LWT):
   Topic: spBv1.0/Paketleme/NDEATH/Line1_PLC
   → SCADA: "Line1_PLC offline"
```

### Sparkplug B vs Ham MQTT

```
Ham MQTT ile fabrika verisi:
  factory/line1/temperature = "82.5"  (text, birim bilgisi yok)
  factory/line1/speed = "45.3"        (text, aralık bilgisi yok)
  factory/line1/running = "true"      (text)
  → Yeni subscriber: "temperature ne birimi? 82.5 Celsius mi Fahrenheit mi?"

Sparkplug B ile:
  NBIRTH'de:
    {name: "Temperature", datatype: FLOAT, value: 82.5, unit: "°C",
     properties: {engLow: 0.0, engHigh: 150.0, alarm_high: 90.0}}
  → Yeni subscriber: Tüm metadata bilgisi BIRTH'ten geliyor
  → SCADA tag konfigürasyonu otomatik — elle girmeye gerek yok
```

---

## MQTT Güvenliği

### Transport Güvenliği (TLS)

```
Port 1883: Şifresiz MQTT (yalnızca izole geliştirme ağı)
Port 8883: TLS şifreli MQTT (production zorunlu)

TLS bileşenleri:
  CA Certificate: Güvenilen sertifika otoritesi
  Server Certificate: Broker sertifikası (CA tarafından imzalı)
  Server Private Key: Broker özel anahtarı
  (Client Certificate: Opsiyonel, mutual TLS için)

Mosquitto TLS yapılandırması:
  # /etc/mosquitto/conf.d/tls.conf
  listener 8883
  certfile /etc/mosquitto/certs/server.crt
  keyfile  /etc/mosquitto/certs/server.key
  cafile   /etc/mosquitto/certs/ca.crt
  require_certificate false  # Client sertifikası opsiyonel
  allow_anonymous false
  password_file /etc/mosquitto/passwd

# Kullanıcı oluşturma
mosquitto_passwd -c /etc/mosquitto/passwd plc_user
# (şifre girişi istenir)
```

### Python'da TLS Bağlantı

```python
import paho.mqtt.client as mqtt
import ssl

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, 'SecurePLCClient')

# TLS yapılandırması
client.tls_set(
    ca_certs='/path/to/ca.crt',
    certfile=None,               # Client cert (mutual TLS yoksa None)
    keyfile=None,
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

# Kullanıcı adı / şifre
client.username_pw_set('plc_user', 'secure_password')

# Bağlan (port 8883 = TLS)
client.connect('broker.factory.local', 8883, keepalive=60)
```

### ACL (Access Control List) — Konu Tabanlı Yetkilendirme

```
Mosquitto ACL dosyası (/etc/mosquitto/acl):

# plc_user: Yalnızca kendi line'ına yayın yapabilir
user plc_user_line1
topic write factory/istanbul/imalat/line1/#
topic read factory/istanbul/imalat/line1/command/#

# scada_user: Tüm fabrikayı okuyabilir, komut gönderebilir
user scada_user
topic read factory/#
topic write factory/+/+/+/command/#

# dashboard_user: Yalnızca okuyabilir
user dashboard_user
topic read factory/#
```

---

## OPC UA + MQTT Birlikte Kullanım

### Katmanlı Mimari

```
Endüstriyel IoT için yaygın "iyi" mimari:

Cihaz Katmanı (EtherCAT, PROFINET, IO-Link):
  PLC → Fiziksel I/O okuma/yazma

SCADA/Kontrol Katmanı:
  PLC ←→ SCADA (OPC UA: Bidirectional, secure, semantic)
    OPC UA güçlü: Metod çağrısı, node browse, kimlik doğrulama
    Örnek: SCADA setpoint yazar, alarm onaylar, recipe yükler

Veri Toplama / Analytics Katmanı:
  PLC/SCADA → MQTT Broker (Unidirectional push, high throughput)
    MQTT güçlü: Çok alıcıya dağıtım, bulut entegrasyonu, ölçekleme
    Örnek: InfluxDB, Grafana, AWS IoT, Azure Digital Twins

Enterprise / Bulut Katmanı:
  MQTT Broker → MES, ERP, AI/ML, Digital Twin

Diagram:
  EtherCAT/PROFINET          → PLC
  PLC ←→ SCADA              (OPC UA: RW, secure)
  PLC → MQTT Broker         (MQTT: Publish only, telemetry)
  MQTT Broker → InfluxDB    (Subscriber: historian)
  MQTT Broker → Dashboard   (Subscriber: Grafana)
  MQTT Broker → AWS IoT     (Subscriber: cloud)
  MQTT Broker → MES         (Subscriber: production data)
```

### CODESYS'te OPC UA + MQTT

```
Application yapısı:
  ├── OPC UA Server          → SCADA bağlantısı (ReadWrite, Secure)
  │   └── Symbol Configuration
  │       └── Exposed variables
  │
  └── MQTT Client            → Bulut/analitik (Publish only)
      ├── GVL_Modbus → GVL_MQTT eşleme
      └── PRG_MQTTPublish (100ms, Task_Background)
```

```iecst
(* PRG_MQTTPublish — Task_Background içinde *)
(* OPC UA ile eş zamanlı çalışır, çakışmaz *)
PROGRAM PRG_MQTTPublish
VAR
    fbMQTT      : MQTT_Client.FB_MQTTClient;
    fbPublish   : MQTT_Client.FB_MQTTPublish;
    sPayload    : STRING(512);
    tTimer      : TON;
END_VAR

fbMQTT(
    Enable           := TRUE,
    sBrokerAddress   := '192.168.1.10',
    nPort            := 8883,
    sClientID        := 'CODESYS_Line1',
    sUsername        := 'plc_user',
    sPassword        := 'secure_password',
    
    sWillTopic       := 'factory/istanbul/line1/status/online',
    sWillPayload     := 'false',
    bWillRetain      := TRUE,
    nWillQoS         := 1
);

tTimer(IN := fbMQTT.bConnected, PT := T#5S);
IF tTimer.Q THEN
    tTimer(IN := FALSE);
    
    (* JSON payload oluştur *)
    sPayload := '{"speed":';
    sPayload := CONCAT(sPayload, REAL_TO_STRING(GVL_Diagnostics.rActualSpeed));
    sPayload := CONCAT(sPayload, ',"temperature":');
    sPayload := CONCAT(sPayload, REAL_TO_STRING(GVL_Diagnostics.rActualTemp));
    sPayload := CONCAT(sPayload, ',"running":');
    sPayload := CONCAT(sPayload, SEL(GVL_State.xRunning, 'false', 'true'));
    sPayload := CONCAT(sPayload, '}');
    
    fbPublish(
        Enable      := TRUE,
        sTopic      := 'factory/istanbul/imalat/line1/paketleme/telemetry',
        sPayload    := sPayload,
        nQoS        := 0,         (* Telemetri: QoS 0 *)
        bRetain     := FALSE,
        MQTT_Client := fbMQTT
    );
END_IF

(* Online durumu *)
IF fbMQTT.bConnected THEN
    fbPublish(
        Enable      := TRUE,
        sTopic      := 'factory/istanbul/line1/status/online',
        sPayload    := 'true',
        nQoS        := 1,
        bRetain     := TRUE,      (* Retain: Durum bilgisi *)
        MQTT_Client := fbMQTT
    );
END_IF
```

---

## Gerçek Proje: Unified Namespace Uygulaması

### Senaryo

```
Fabrika: 3 üretim hattı, 12 PLC, 80 sensör, eski SCADA (Modbus TCP)
Hedef: Tüm veriyi InfluxDB'ye topla → Grafana dashboard → AWS'ye raporla

Mevcut sorun:
  Her sistem her sisteme point-to-point bağlı.
  12 PLC × 3 hedef = 36 bağlantı yapılandırması.
  Yeni analitik sistemi eklenince: 12 yeni bağlantı daha.
  
UNS ile çözüm:
  Her PLC → MQTT Broker (bir bağlantı)
  Broker → InfluxDB (bir subscriber)
  Broker → Grafana (bir subscriber)
  Broker → AWS    (bir subscriber)
  Yeni sistem eklenince: Yalnızca bir subscriber.
```

### Uygulanan Mimari

```
Katman 1: Cihaz
  PLC1-12 (CODESYS) → MQTT Publish (Mosquitto, 192.168.100.10:8883)
  Eski SCADA → Node-RED → MQTT (Modbus → MQTT köprüsü)
  Enerji sayaçları → MQTT Gateway → Broker

Katman 2: Broker (EMQX Community)
  Topic namespace: factory/istanbul/imalat/{line}/{machine}/{datapoint}
  TLS + Kullanıcı doğrulama
  Kural motoru: Alarm gelince webhook tetikle

Katman 3: Alıcılar
  InfluxDB: factory/# subscribe → Zaman serisi veritabanı
  Grafana: InfluxDB'den okur → Dashboard
  Node-RED: factory/+/+/alarm/# subscribe → Email/SMS
  AWS IoT Core: factory/# forward → Makine öğrenmesi modeli

Sonuç:
  Yeni analitik sistemi: Sadece yeni subscriber ekle.
  PLC kodu değişmiyor.
  SCADA değişmiyor.
  Entegrasyon spaghetti ortadan kalktı.
```

---

## Pratik Örnekler

### Örnek 1: Node-RED ile MQTT Akışı

```javascript
// Node-RED: CODESYS MQTT → InfluxDB → Grafana pipeline

// MQTT In Node (subscribe)
topic: "factory/istanbul/imalat/line1/paketleme/telemetry"
broker: "mqtt://user:pass@broker:8883"

// Function Node: JSON parse + InfluxDB formatı
msg.payload = JSON.parse(msg.payload);
msg.measurement = "line1_telemetry";
msg.fields = {
    speed: msg.payload.speed,
    temperature: msg.payload.temperature
};
msg.tags = {
    line: "line1",
    site: "istanbul"
};
return msg;

// InfluxDB Out Node → Grafana okur
```

### Örnek 2: AWS IoT Core Entegrasyonu

```bash
# AWS IoT Core'a bağlanmak için endpoint:
# xxxxxx.iot.eu-west-1.amazonaws.com:8883

# Her cihaz bir "Thing" — sertifika tabanlı kimlik
# CODESYS konfigürasyonu:
sBrokerAddress := 'xxxxxx.iot.eu-west-1.amazonaws.com'
nPort          := 8883
# Sertifika dosyaları:
sCACertFile    := '/home/codesys/certs/AmazonRootCA1.pem'
sCertFile      := '/home/codesys/certs/device.cert.pem'
sPrivKeyFile   := '/home/codesys/certs/private.key'
```

### Örnek 3: Grafana Dashboard için Topic Tasarımı

```
Grafana, MQTT plugin veya InfluxDB üzerinden veri okur.
Topic tasarımı Grafana sorgu kolaylığını doğrudan etkiler.

İyi tasarım:
  factory/{site}/{area}/{line}/{machine}/telemetry
  → Grafana variable: $site, $line, $machine
  → Tek dashboard tüm fabrikaları kapsar

Kötü tasarım:
  data1, temp_sensor, machine3_speed
  → Her makine için ayrı dashboard gerekir
```

---

## Sık Yapılan Hatalar

### Hata 1: Broker'ı Ağa Açmak

```
Mosquitto 1883 portunu herkese açık bırakmak → Kimse kimlik doğrulaması yapmıyor.
Herhangi bir cihaz bağlanıp komut gönderebilir.

Minimum güvenlik:
  1. allow_anonymous false
  2. password_file tanımla
  3. TLS zorunlu (8883)
  4. ACL ile topic yetkilendirmesi
```

### Hata 2: Topic Yapısını Sonradan Değiştirmek

```
Başlangıçta: sensor1/temp
3 ay sonra: factory/line1/temp (daha iyi ama)
  → Tüm subscriber'ların güncellenmesi gerekir.
  → InfluxDB'deki eski veri farklı yapıda.
  → Grafana dashboard'ları bozulur.

Kural: Topic tasarımını baştan doğru yap.
       ISA-95 hiyerarşisi: enterprise/site/area/line/cell/device/datapoint
```

### Hata 3: Broker'ı SPOF (Single Point of Failure) Yapmak

```
Broker durdu → Tüm MQTT iletişim durdu.
Production'da: Broker yüksek erişilebilirlik (HA) ile çalışmalı.
  HiveMQ: Cluster desteği
  EMQX: Cluster desteği
  Mosquitto: Tek node → Kritik sistemler için uygun değil

Geçici çözüm: Broker persist session + QoS 1 ile
  bağlantı koptuğunda kuyrukta mesaj birikiyor,
  broker geri gelince teslim ediliyor.
```

### Hata 4: Payload'da Birim Bilgisi Yazmamak

```
factory/temperature = "82.5"
→ Celsius mi Fahrenheit mi? Oran mı? Ham ADC mi?

Daha iyi:
factory/temperature = {"value": 82.5, "unit": "celsius", "timestamp": 1717200000}

En iyisi (Sparkplug B): Metadata BIRTH'de tanımlı, her DATA mesajında tekrar etmeye gerek yok.
```

## Gerçek Proje Notları

**Not 1 — Retained Mesajın Grafana'yı Kurtarması**  
Grafana dashboardu her yeniden açıldığında 10-15 saniye boş görünüyordu. Veri kaynağı MQTT'ydi (InfluxDB değil, doğrudan MQTT plugin). CODESYS retain=False ile yayınlıyordu. Dashboard açılınca son değeri görmek için PLC'nin bir sonraki güncellemeyi göndermesini bekliyordu. Retain=True eklenince dashboard açılışında anında mevcut değer göründü.

**Not 2 — Topic Değişikliğinin Maliyeti**  
Pilot projede topic yapısı `line1/temperature` şeklindeydi. Ölçek genişleyince 3 fabrika eklendi. Topic'ler `istanbul/line1/temperature`, `ankara/line1/temperature` yapısına taşındı. InfluxDB'deki tüm eski veri yeni yapıyla eşleşmiyordu — analitik bozuldu. 2 günlük veri migrasyonu. Ders: ISA-95 tabanlı topic yapısı başlangıçtan itibaren uygulandı, bir daha değişmedi.

**Not 3 — OPC UA + MQTT Birlikte Çalışması**  
Bir projede SCADA ile OPC UA, analitik platform ile MQTT kullanıldı. İlk başta "çift entegrasyon — karmaşık değil mi?" diye soruldu. 3 ay sonra SCADA değişti. MQTT pipeline hiç etkilenmedi. MQTT analitik platformu değişti. OPC UA SCADA bağlantısı etkilenmedi. Gevşek bağlantının gerçek değeri o an anlaşıldı.

**Not 4 — Sparkplug B'nin Entegrasyon Süresine Etkisi**  
Ham MQTT ile bir PLC entegrasyonu: Topic yapısını anla, payload formatını çöz, birimleri belgele, InfluxDB tag'lerini tanımla, Grafana dashboard'u konfigure et → 2-3 gün.

Sparkplug B ile: NBIRTH mesajındaki metadata her şeyi anlatıyor. Otomasyon araçları (Ignition, HiveMQ Sparkplug Extension) bunu okuyup otomatik tag yapısı oluşturuyor → 2-3 saat.

## İlgili Konular

```
knowledge/protocols/mqtt/
└── 01_basics.md                 → MQTT temel kavramları

knowledge/codesys/networking/
└── 04_mqtt_client.md            → CODESYS MQTT implementasyonu

knowledge/protocols/opc-ua/
├── 01_architecture.md           → OPC UA + MQTT birlikte kullanım mimarisi
└── 04_subscriptions.md          → OPC UA PubSub vs MQTT karşılaştırması

Araçlar ve kaynaklar:
  Eclipse Mosquitto  → https://mosquitto.org (geliştirme broker)
  HiveMQ Community   → https://www.hivemq.com (kurumsal)
  EMQX               → https://www.emqx.io (yüksek performans)
  MQTT Explorer      → Görsel MQTT browser ve test aracı
  Node-RED           → MQTT akış tabanlı entegrasyon
  InfluxDB + Grafana → Zaman serisi + dashboard
  paho-mqtt          → Python MQTT kütüphanesi
  Sparkplug B spec   → https://www.eclipse.org/tahu/sparkplug/
```
