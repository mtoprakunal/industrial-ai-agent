---
KONU        : MQTT Protokol Temelleri
KATEGORİ    : protocols
ALT_KATEGORI: mqtt
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://www.hivemq.com/mqtt/"
    başlık: "HiveMQ — MQTT Essentials 2026 Guide"
    güvenilirlik: topluluk
  - url: "https://www.hivemq.com/blog/mqtt-essentials-part-8-retained-messages/"
    başlık: "HiveMQ — MQTT Retained Messages Explained"
    güvenilirlik: topluluk
  - url: "https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt"
    başlık: "EMQ — Mastering MQTT: The Ultimate Beginner's Guide for 2026"
    güvenilirlik: topluluk
  - url: "https://justprotocols.com/protocols/mqtt"
    başlık: "JustProtocols — MQTT Protocol Explained: The Complete Guide"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "02_industrial_usage.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/networking/04_mqtt_client.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: karşılaştırır
  - konu: "knowledge/protocols/modbus-tcp/01_protocol_basics.md"
    ilişki: karşılaştırır
ÖNKOŞUL     :
  - "Temel ağ kavramları (TCP/IP, port)"
  - "İstemci-sunucu modeli kavramı"
ÇELİŞKİLER :
  - kaynak: "QoS 2 her zaman daha iyi algısı"
    konu: "Daha yüksek QoS her zaman daha iyi değil — tradeoff var"
    çözüm: >
      QoS 2 tam garanti sağlar ama 4 yönlü el sıkışma gerektirir:
      PUBLISH → PUBREC → PUBREL → PUBCOMP.
      Gecikme ve bandwidth tüketimi artar.
      Endüstriyel IoT'de: Akış verisi → QoS 0, Alarm → QoS 1 yeterli.
      QoS 2 yalnızca finansal/kritik tek-sefer mesajlar için gerçekten gerekli.
  - kaynak: "MQTT = IoT için, OPC UA = endüstri için algısı"
    konu: "İkisi rakip değil tamamlayıcıdır"
    çözüm: >
      MQTT: Hafif, pub/sub, broker tabanlı, bulut/IoT için ideal.
      OPC UA: Semantik zengin, güvenli, iki yönlü, PLC-SCADA için ideal.
      Doğru mimari: OPC UA cihaz katmanında, MQTT bulut katmanında.
      Hatta OPC UA PubSub spesifikasyonu MQTT'yi transport olarak kullanır.
---

## Özün Ne

MQTT (Message Queuing Telemetry Transport), 1999'da IBM tarafından düşük bant genişliğinde güvenilmez bağlantılar üzerinde sensör verisi taşımak için tasarlanmış hafif bir mesajlaşma protokolüdür. Bugün OASIS/ISO standardı (ISO/IEC 20922) haline gelmiş ve endüstriyel IoT'nin fiili iletişim standartlarından biri olmuştur. Modbus ve OPC UA'nın istek-yanıt modelinden farklı olarak MQTT **yayın/abone** (publish/subscribe) modeliyle çalışır: Veriyi üreten taraf broker'a yayınlar, ilgilenen her istemci broker'dan abone olarak alır. Bu yapı, bir ölçüm verisini aynı anda SCADA'ya, bulut platformuna, mobil uygulamaya ve analitik motoruna göndermek için idealdir.

## Nasıl Çalışır

### Publish/Subscribe Modeli

```
OPC UA / Modbus (İstek-Yanıt — Request/Response):
  İstemci → Sunucu: "Değer ne?"
  Sunucu → İstemci: "Değer 82.5°C"
  → İstemci her veri için aktif sorgulama yapmak zorunda.
  → Gönderici ve alıcı doğrudan bağlı.

MQTT (Yayın-Abone — Publish/Subscribe):
  PLC → Broker: "factory/line1/temperature = 82.5°C" (Publish)
  Broker → SCADA: 82.5°C  (Subscribe edilmişse)
  Broker → Bulut: 82.5°C  (Subscribe edilmişse)
  Broker → Dashboard: 82.5°C (Subscribe edilmişse)
  → Üretici (PLC) kimin aldığını bilmiyor.
  → Alıcılar üreticinin kim olduğunu bilmiyor.
  → Gevşek bağlantı (loose coupling) — asıl güç buradan gelir.
```

### Broker'ın Rolü

```
Broker = Merkezi mesaj dağıtım noktası

Publisher (PLC/Sensör)             Subscriber (SCADA/Dashboard/Bulut)
    │                                      ▲
    │ PUBLISH                              │ Subscribe edilmiş topic
    │ Topic: factory/temp                  │ mevcutsa mesajı ilet
    ▼                                      │
┌─────────────────────────────────────────────────────┐
│                   MQTT BROKER                        │
│                                                      │
│  Topic Routing                                       │
│  factory/temp → [SCADA, Cloud, Dashboard]           │
│                                                      │
│  Retained Messages: Son değeri sakla                │
│  QoS Management: Teslimat garantisi                 │
│  Session Management: Bağlantı kesilince sakla       │
│  Last Will: Beklenmedik kopma bildirimi             │
│  Authentication: TLS, kullanıcı adı/şifre          │
└─────────────────────────────────────────────────────┘

Popüler Broker'lar:
  Mosquitto  → Hafif, açık kaynak, Raspberry Pi'da bile çalışır
  HiveMQ     → Kurumsal, kümeleme, milyonlarca bağlantı
  EMQX       → Yüksek performans, 100M+ bağlantı, kural motoru
  AWS IoT Core → Yönetilen, AWS ekosistemi
  Azure Event Grid MQTT → Yönetilen, Azure ekosistemi
```

### Topic Yapısı

MQTT topic'leri hiyerarşik, eğik çizgiyle ayrılmış string'lerdir:

```
Sözdizimi: seviye1/seviye2/seviye3/...

Örnekler:
  factory/istanbul/line1/machine3/temperature
  home/livingroom/sensor/humidity
  vehicle/truck001/gps/latitude

Endüstriyel şema (ISA-95 tabanlı):
  enterprise/site/area/line/cell/device/datapoint

  acme/istanbul/imalat/line1/paketleme/motor1/speed
  acme/istanbul/imalat/line1/paketleme/motor1/current
  acme/istanbul/imalat/line1/paketleme/alarm/motor1_fault
  acme/istanbul/imalat/line1/paketleme/status/online
```

**Önemli kurallar:**
```
1. Topic büyük/küçük harfe duyarlıdır:
   Factory/temp ≠ factory/temp

2. / ile başlayan topic geçerli ama önerilmez:
   /factory/temp (boş ilk seviye)

3. $ ile başlayan topic'ler broker için rezerve:
   $SYS/broker/clients/connected (broker istatistikleri)

4. Boşluk kullanma (bazı broker'lar sorun çıkarır)
```

**Wildcard'lar (Yalnızca Subscribe'da):**
```
+ = Tek seviye wildcard
  factory/+/temperature → factory/line1/temperature ✓
                          factory/line2/temperature ✓
                          factory/line1/zone1/temperature ✗

# = Çok seviyeli wildcard (sona gelir)
  factory/line1/# → factory/line1/temperature ✓
                    factory/line1/motor1/speed ✓
                    factory/line1/alarm/fault ✓
  factory/#       → Tüm fabrika verisi (dikkat: yüksek trafik)
```

### QoS Seviyeleri

```
QoS 0 — At Most Once (En Fazla Bir Kez):
  Teslimat garantisi: Yok. Ağ kesilirse mesaj kaybolur.
  Mekanizma: Tek yönlü PUBLISH. Onay yok.
  Overhead: Minimum (tek paket)
  Kullanım: Sürekli güncellenen sensör verisi
             (kaybolan 1 sıcaklık değeri önemli değil)
  
  Publisher → PUBLISH → Broker → PUBLISH → Subscriber
  
QoS 1 — At Least Once (En Az Bir Kez):
  Teslimat garantisi: Mesaj en az bir kez ulaşır. Duplikasyon mümkün.
  Mekanizma: PUBLISH → PUBACK. PUBACK gelmezse yeniden gönder.
  Overhead: 2 mesaj (PUBLISH + PUBACK)
  Kullanım: Alarm bildirimleri, kritik proses değerleri
  
  Publisher → PUBLISH → Broker → PUBACK → Publisher
  Broker → PUBLISH → Subscriber → PUBACK → Broker

QoS 2 — Exactly Once (Tam Olarak Bir Kez):
  Teslimat garantisi: Mesaj tam olarak bir kez ulaşır.
  Mekanizma: 4 yönlü el sıkışma
  Overhead: 4 mesaj (PUBLISH+PUBREC+PUBREL+PUBCOMP)
  Kullanım: Finansal işlemler, hassas sayaçlar
             (çoğu endüstriyel senaryoda QoS 1 yeterli)
  
  Pub → PUBLISH → Bro → PUBREC → Pub → PUBREL → Bro → PUBCOMP → Pub
  Bro → PUBLISH → Sub → PUBREC → Bro → PUBREL → Sub → PUBCOMP → Bro
```

**QoS seçim rehberi:**

| Senaryo | QoS | Neden |
|---|---|---|
| Sıcaklık periyodik okuma (1/sn) | 0 | Kaybolan 1 değer sorun değil |
| Motor hız akış verisi | 0 | Sürekli gelecek, kayıp tolere edilir |
| Alarm aktif bildirimi | 1 | Alındığından emin olunmalı |
| Reçete parametresi | 1 | Kritik, duplikasyon tolere edilir |
| Makine online/offline durumu | 1 | Guaranteed delivery |
| Finansal sayaç | 2 | Duplikasyon kabul edilemez |

### Retained Message (Saklanmış Mesaj)

Broker, her topic için son retained mesajı saklar. Yeni subscriber bağlandığında anında son değeri alır — veriyi yayınlayanın tekrar göndermesini beklemeksizin.

```
PLC → PUBLISH (retain=True): factory/line1/status = "Running"
Broker: Bu mesajı sakla.

3 saat sonra yeni bir Dashboard bağlandı:
Dashboard → SUBSCRIBE: factory/line1/status
Broker → Dashboard: "Running" (hemen, hiç beklemeden)

Retain olmadan:
Dashboard → SUBSCRIBE: factory/line1/status
Dashboard bekledi... bekledi... PLC bir sonraki güncellemeyi gönderene kadar.
```

**Retained kullanım senaryoları:**
```
Online/Offline durumu:
  Retain=True: factory/.../status/online = "true"
  Yeni subscriber anında "online" bilgisini alır.

Son ölçüm değeri:
  Retain=True: factory/.../temperature = "82.5"
  Dashboard açıldığında anında mevcut değeri gösterir.

Konfigürasyon/Metadata:
  Retain=True: factory/.../config/max_speed = "100.0"
  Yeni cihazlar konfigürasyonu anında alır.

Retain GEREKTİRMEYEN:
  Anlık olaylar (alarm tetiklendi — bir kez bildir)
  Event'ler (start komutu — tekrar gönderme)
```

### Last Will and Testament (LWT — Son Vasiyet)

İstemci beklenmedik şekilde bağlantısı kesildiğinde broker'ın otomatik olarak yayınlayacağı mesaj.

```
Bağlantı kurulurken LWT yapılandırması:
  Topic: factory/line1/status/online
  Payload: "false"
  QoS: 1
  Retain: True

Normal çalışma:
  PLC bağlanır → "true" yayınlar (retained) → Dashboard görür: "Online"

Beklenmedik kopma (güç kesilmesi, ağ hatası):
  PLC FIN göndermeden koptu.
  Broker: "Ah, LWT tetikle"
  Broker → factory/line1/status/online = "false" (retained)
  Dashboard görür: "Offline" ← Otomatik, PLC'nin kodu olmadan

Normal kapanma (FIN ile):
  PLC disconnect() çağırır → Broker LWT tetiklemez.
  (Genellikle normal kapanmada da "false" yayınlamak gerekir)
```

### MQTT Paket Yapısı — Minimum Overhead

```
MQTT Fixed Header: 2 byte (minimum!)
  Byte 1: Packet Type (4 bit) + Flags (4 bit)
  Byte 2: Remaining Length

CONNECT paketi: ~20-100 byte (bağlantı bilgileriyle)
PUBLISH paketi: 2 + topic_len + payload_len byte

Karşılaştırma (100 byte payload için):
  HTTP request:   ~300-600 byte (header + overhead)
  Modbus TCP:     ~17 byte (MBAP + PDU)
  MQTT PUBLISH:   ~15-30 byte (2-byte header + topic + payload)

MQTT'nin avantajı düşük bant genişliğinde ve mobil ağlarda belirgindir.
Fabrika LAN'ında fark küçük; 4G/LTE/internet üzerinden kritik.
```

### MQTT vs OPC UA vs Modbus — Karşılaştırma

```
Özellik          MQTT           OPC UA         Modbus TCP
─────────────────────────────────────────────────────────────────
Model            Pub/Sub        Client-Server  Client-Server
Broker           Gerekli        Yok            Yok
Veri modeli      Yok (raw)      Zengin/semantik Sadece register
Güvenlik         TLS opsiyonel  Yerleşik       Yok
Keşif            Yok            Var (browse)   Yok
İki yönlü       Evet (sub)     Evet           Evet (limited)
Ölçeklenebilir  Çok iyi        İyi            Sınırlı
Latency          Düşük          Düşük-Orta     Çok Düşük
Overhead         Minimum        Yüksek         Minimum
Standart         OASIS/ISO      IEC 62541      Modbus.org
Endüstri desteği Büyük büyüyor  Büyük          Evrensel (legacy)
─────────────────────────────────────────────────────────────────
İdeal senaryo   Bulut/IoT/Analitik  PLC-SCADA  Mevcut cihazlar
```

## Pratikte Nasıl Kullanılır

### Topic Tasarım Prensipleri

```
Prensip 1 — Hiyerarşik ve tutarlı:
  ❌ temp_line1, speed_motor2, alarm3  (düz, anlamsız)
  ✅ factory/line1/motor1/speed       (hiyerarşik, keşfedilebilir)

Prensip 2 — Genel → Özel sıralama:
  Doğru: enterprise/site/area/device/datapoint
  Yanlış: datapoint/device/area/site/enterprise

Prensip 3 — Wildcard için optimize:
  factory/+/alarm → Tüm hatlardaki alarmlara abone olmaya uygun
  factory/line1/# → Hat 1'in tüm verilerine abone olmaya uygun

Prensip 4 — Sabit yollar:
  Cihaz adı topic'te olmalı ama ID değil:
  ✅ factory/istanbul/line1/conveyor_motor/speed
  ❌ factory/istanbul/line1/device_1d3a7f/speed

Prensip 5 — Sensör vs komut ayrımı:
  factory/.../telemetry/temperature   → Sensör verisi
  factory/.../command/set_speed       → Komut
  factory/.../status/online           → Durum
```

### Mosquitto Kurulumu ve Test

```bash
# Linux kurulumu
sudo apt install mosquitto mosquitto-clients

# Test yapılandırması (~/.config/mosquitto/test.conf)
echo "listener 1883
allow_anonymous true" > /tmp/mosquitto.conf
mosquitto -c /tmp/mosquitto.conf -d

# Terminal 1 — Subscribe
mosquitto_sub -h localhost -t "factory/#" -v

# Terminal 2 — Publish (QoS 1, Retained)
mosquitto_pub -h localhost -t "factory/line1/temperature" \
              -m "82.5" -q 1 -r

# Terminal 1'de görünen:
# factory/line1/temperature 82.5

# Yeni subscriber bağlandığında retained değeri anında alır:
mosquitto_sub -h localhost -t "factory/line1/temperature" -v
# factory/line1/temperature 82.5  ← Anında (retained)
```

### Python (paho-mqtt) ile Temel Kullanım

```python
import paho.mqtt.client as mqtt
import json
import time

BROKER = 'localhost'
PORT = 1883
CLIENT_ID = 'PLC_Line1_Publisher'

# Last Will yapılandırması
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, CLIENT_ID)
client.will_set(
    topic='factory/line1/status/online',
    payload='false',
    qos=1,
    retain=True
)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Broker'a bağlandı")
        # Online durumu yayınla (retained)
        client.publish('factory/line1/status/online', 'true', qos=1, retain=True)
        # Abone ol
        client.subscribe('factory/line1/command/#', qos=1)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Komut alındı: {topic} = {payload}")
    
    if topic == 'factory/line1/command/set_speed':
        # Hız setpoint komutu
        speed = float(payload)
        print(f"Yeni hız setpoint: {speed} m/dk")

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

# Veri yayınlama döngüsü
try:
    while True:
        # Sensör verisi — QoS 0 (sürekli akış)
        payload = json.dumps({
            'temperature': 82.5,
            'speed': 45.3,
            'running': True,
            'timestamp': int(time.time())
        })
        client.publish('factory/line1/telemetry', payload, qos=0)
        
        # Alarm — QoS 1 (kritik)
        client.publish('factory/line1/alarm/motor_temp',
                       json.dumps({'active': False}), qos=1)
        
        time.sleep(5)

except KeyboardInterrupt:
    # Normal kapanma: offline yayınla
    client.publish('factory/line1/status/online', 'false', qos=1, retain=True)
    client.disconnect()
```

## Örnekler

### Örnek 1: LWT ile Online/Offline İzleme

```
Senaryo: Fabrikada 20 PLC. Hangilerinin online olduğunu bilmek istiyorum.

Her PLC LWT:
  Topic: factory/istanbul/line{N}/plc/status
  LWT Payload: "offline"
  LWT QoS: 1, LWT Retain: True
  
Bağlantı kurulunca PLC yayınlar:
  Topic: factory/istanbul/line{N}/plc/status
  Payload: "online"
  QoS: 1, Retain: True

Dashboard:
  Subscribe: factory/istanbul/+/plc/status
  → Tüm PLC'lerin anlık durumu (online/offline)
  → Yeni bağlanan dashboard anında mevcut durumu alır (retained)
```

### Örnek 2: Hiyerarşik Topic Tasarımı — Paketleme Fabrikası

```
factory/
├── istanbul/              (Site)
│   ├── metadata/          (Site metadata)
│   │   └── name = "İstanbul Fabrikası"  (retained)
│   └── imalat/            (Area)
│       ├── line1/         (Line)
│       │   ├── status/
│       │   │   ├── online = true       (retained)
│       │   │   └── production_active = true (retained)
│       │   ├── telemetry/             (5sn periyodik, QoS 0)
│       │   │   ├── speed              = 45.3
│       │   │   ├── temperature        = 82.5
│       │   │   └── production_count   = 15234
│       │   ├── alarm/                 (QoS 1, event)
│       │   │   ├── motor_fault        = {"active":false}
│       │   │   └── temp_high          = {"active":true,"value":92.1}
│       │   └── command/               (HMI → PLC, QoS 1)
│       │       ├── start              (Subscribe eden PLC)
│       │       ├── stop
│       │       └── set_speed          = 50.0
│       └── line2/         (Line)
│           └── ...
```

### Örnek 3: QoS Karşılaştırması — Hangi Senaryo?

```python
# Sürekli sıcaklık ölçümü — QoS 0 (kayıp tolere edilir)
client.publish('factory/line1/temperature', '82.5', qos=0)

# Motor arıza bildirimi — QoS 1 (ulaşmalı, duplikasyon tolere edilir)
client.publish('factory/line1/alarm/motor_fault',
    json.dumps({'active': True, 'timestamp': time.time()}), qos=1)

# Fatura/üretim sayacı — QoS 2 (tam olarak bir kez, duplikasyon yok)
client.publish('factory/billing/production_batch',
    json.dumps({'count': 1500, 'batch_id': 'B20260601_001'}), qos=2)
```

## Sık Yapılan Hatalar

### Hata 1: Her Şeyi QoS 2 Yapmak

```
Sonuç: 4 yönlü handshake × 1000 mesaj/sn = ciddi overhead.
       Broker'ın işlemci yükü artar, gecikme artar.
Kural: QoS 0 sensör akışı için yeterli. QoS 1 alarm için.
       QoS 2 gerçekten "exactly once" gerektiğinde.
```

### Hata 2: Topic'i Çok Düz Tasarlamak

```
❌ sensor1, sensor2, alarm, status, temp1, speed2
→ Wildcard kullanılamaz, ölçeklenemiyor.

✅ factory/line1/motor1/speed, factory/line1/motor2/speed
→ factory/+/+/speed ile tüm motor hızları izlenebilir.
```

### Hata 3: LWT Olmadan Deploy

```
PLC beklenmedik kesildi.
Dashboard "Online" göstermeye devam ediyor (eski retained değer).
Operatör makineye gitti — kimse yok!

Kural: Her üretim sistemi LWT ile konuşlandırılmalı.
```

### Hata 4: Retain'i Her Mesajda Kullanmak

```
Her telemetri mesajı retain=True:
  Broker tüm son değerleri saklar (1000 sensör = 1000 retained mesaj)
  Broker yeniden başlatıldığında hepsi yüklenir.
  Performans kaybı.

Kural: Retain yalnızca "durum" bilgisi için (status, config, last value).
       Sürekli akış verisi için retain=False.
```

### Hata 5: Güvensiz Bağlantı ile Production

```
Port 1883 = şifresiz MQTT.
Fabrika ağında bile kimlik doğrulama yoksa:
  Herhangi bir ağ cihazı MQTT'ye bağlanıp komut gönderebilir.
  
Kural:
  Geliştirme: Port 1883, anonymous bağlantı → Tamam
  Production: Port 8883 (TLS), kullanıcı adı + şifre → Zorunlu
```

## Gerçek Proje Notları

**Not 1 — Retained Mesajın Kurtardığı Dashboard**  
Bir fabrika dashboardu her sabah açılırken 30 saniye boş görünüyordu. Nedenini anlayana kadar: Tüm PLC'ler retain=False ile yayınlıyordu. Dashboard subscribe olunca PLC'nin bir sonraki güncellemeyi göndermesini bekliyordu (ortalama 10 saniye). Retain=True eklenince dashboard açılır açılmaz tüm değerler mevcut.

**Not 2 — LWT ile Phantom Online Sorunu**  
Ağ ekipmanı güncelleme sırasında bir PLC bağlantısı beklenmedik biçimde kesildi. Dashboard 2 saat boyunca "Online" gösterdi. LWT yoktu. LWT eklendikten sonra kopuş 30 saniye içinde tespit edildi.

**Not 3 — QoS 2'nin Overhead'i**  
Bir pilot projede tüm mesajlar QoS 2 ile gönderildi. 200 sensör × 1/sn = 200 msg/sn × 4 paket = 800 paket/sn. Mosquitto CPU %60'a çıktı. QoS 0'a geçildi (telemetri) + QoS 1 (alarmlar). CPU %8'e indi. Gerçek proje etkisi.

**Not 4 — Aynı Client ID ile İki İstemcinin "Ping-Pong" Döngüsü**  
Bir hatta yedeklilik için iki CODESYS PLC aynı `sClientID := 'Line1_PLC'` ile broker'a bağlandı. MQTT spesifikasyonu aynı Client ID'nin tek bağlantıya sahip olmasını şart koşar: ikinci istemci bağlanınca broker birincinin oturumunu **DISCONNECT** ile düşürdü. Birinci istemci `loop_start` yeniden bağlanma mantığıyla anında geri bağlandı → ikincisini düşürdü. İki istemci saniyede onlarca kez birbirini atan bir döngüye girdi; broker logları `client already connected, kicking old client` ile doldu, telemetri kayboldu. Çözüm: Her fiziksel cihaza globally-unique Client ID (örn. seri numarası eklenmiş `Line1_PLC_SN8842`). Ders: Client ID benzersizliği "öneri" değil, MQTT'nin sessiz ama ölümcül bir kuralıdır.

**Not 5 — Retained Komut "Zombi"si Makineyi Beklenmedik Başlattı**  
HMI, `factory/line1/command/start` topic'ine `retain=True` ile START komutu gönderiyordu (geliştiricinin "komut kaybolmasın" iyi niyetiyle). Broker bu mesajı sakladı. Hafta sonu PLC bakım için resetlenip yeniden bağlandığında, `command/#` topic'ine subscribe olur olmaz broker saklanmış START'ı anında teslim etti — kimse HMI'a dokunmadan konveyör çalıştı. Komut topic'leri **asla** retained olmamalı; komut bir olaydır (event), durum (state) değil. Retain yalnızca state için. Eski zombi mesajı temizlemek: `mosquitto_pub -t "factory/line1/command/start" -r -n` (boş retained mesaj retained'i siler).

**Not 6 — JSON Payload'daki Ondalık Ayraç (Locale) Tuzağı**  
CODESYS'te `REAL_TO_STRING` çağrısı runtime'ın locale ayarına göre `82,5` (virgül) üretebiliyordu. Bu değer `{"temperature":82,5}` olarak yayınlandı; subscriber tarafı (Node-RED `JSON.parse`) bunu ya hata verdi ya da `82` + ayrı bir `5` alanı olarak yorumladı — sessizce yanlış veri. İnternet üzerinden farklı locale'li sunuculara giden veride saatlerce fark edilmedi. Çözüm: Sayısal payload'ları her zaman nokta ondalık ayraçla, locale-bağımsız formatla üret (manuel string formatlama veya `LREAL_TO_STRING` yerine sabit format fonksiyonu). JSON sayıları daima C-locale'dir; broker payload'ı denetlemez — bu tamamen uygulama sorumluluğudur.

## Edge Case'ler ve Sistem Limitleri

MQTT'nin "basit" görünümü, sınır koşullarında çok sayıda sessiz tuzak barındırır. Aşağıdaki durumlar saha sistemlerinde gerçekten karşılaşılanlardır.

```
1. Keepalive ve Half-Open (Yarı Açık) Bağlantı Tespiti
   ──────────────────────────────────────────────────
   TCP, kabloyu çekince FIN göndermez — broker bağlantının koptuğunu
   anlamaz. MQTT keepalive bu yüzden var:
     • İstemci keepalive süresinde mesaj göndermezse PINGREQ yollar.
     • Broker 1.5 × keepalive boyunca hiçbir paket almazsa bağlantıyı
       ölü kabul eder → LWT tetiklenir.
   TUZAK: keepalive=60 → kopuş tespiti 90 saniyeye kadar gecikebilir.
   Hızlı LWT isteniyorsa keepalive düşürülür (örn. 10-20 sn), ama bu
   her istemciden düzenli PINGREQ → broker yükü artar.
   Mobil/4G ağda NAT timeout keepalive'dan kısaysa bağlantı sessizce ölür.

2. Client ID Çakışması (bkz. Not 4)
   ──────────────────────────────────
   Aynı Client ID = tek oturum. İkinci bağlanan birinciyi düşürür.
   Otomatik üretilen rastgele Client ID'ler (clean session) ise
   her yeniden bağlanmada offline mesaj kuyruğunu KAYBETTİRİR.

3. QoS 1 Duplikasyon (En Az Bir Kez ≠ Tam Bir Kez)
   ───────────────────────────────────────────────
   PUBACK ağda kaybolursa istemci aynı mesajı DUP flag'iyle tekrar yollar.
   Subscriber aynı alarmı 2 kez görür. "Üretim sayacı +1" gibi
   biriktiren işlemler ÇİFT sayar. Çözüm: payload'a idempotency anahtarı
   (batch_id, sequence) koy; subscriber daha önce gördüğü ID'yi yok say.

4. Retained Mesaj + Wildcard Subscribe = Açılışta Patlama
   ──────────────────────────────────────────────────────
   1000 sensör retained değer tutuyorsa, yeni bir `factory/#` aboneliği
   açılış anında 1000 mesajı tek seferde alır. Bağlantı/parse darboğazı.

5. Topic ve Payload Boyut Limitleri
   ─────────────────────────────────
   Topic max 65535 byte (pratikte kısa tut). Payload teorik max 256 MB
   ama broker'lar varsayılan limit koyar (Mosquitto message_size_limit).
   "Tek mesajda 50 MB dosya" göndermek MQTT'nin kullanım amacı değildir.

6. Wildcard'ın Subscribe-Only Oluşu
   ─────────────────────────────────
   PUBLISH'te `+` veya `#` KULLANILAMAZ. `factory/+/temp` topic'ine
   publish denemesi protokol hatasıdır — bazı istemciler sessizce yutar.

7. $SYS ve Rezerve Topic'ler
   ─────────────────────────
   `factory/#` aboneliği $SYS topic'lerini KAPSAMAZ (broker bilinçli
   ayırır). Broker istatistiği için açıkça `$SYS/#` subscribe gerekir.

8. Saat Senkronizasyonu Yok
   ────────────────────────
   MQTT'nin payload'a timestamp koyma zorunluluğu yoktur. Broker mesaja
   zaman damgası eklemez (MQTT 5.0 dışında, o da opsiyonel). Veri sırası
   ve gecikme analizini uygulama kendi timestamp'iyle çözmek zorunda.
```

## Optimizasyon

Endüstriyel MQTT'de optimizasyon, "broker'a daha güçlü donanım vermek"ten önce mesaj tasarımı ve QoS disiplini ile yapılır. Uzman önceliği aşağıdaki sıradadır:

```
ÖNCELİK 1 — QoS'u iş gereksinimine göre düşür (en büyük kazanç)
  Telemetri akışı QoS 0. Her QoS 1→0 düşüşü mesaj başına PUBACK'i,
  her QoS 2→1 düşüşü 4 paketi 2'ye indirir. 200 msg/sn sistemde
  QoS 2→0 geçişi broker CPU'sunu %60 → %8 düşürdü (gerçek ölçüm).

ÖNCELİK 2 — Report-by-exception (yalnızca değişeni yayınla)
  Sensör değeri değişmediyse yayınlama. 1 sn periyot yerine
  "deadband: ±0.2°C değişince yayınla" → trafik %70-90 düşebilir.
  Sparkplug B bunu standart hale getirir (NDATA yalnızca değişen).

ÖNCELİK 3 — Payload'ı küçült
  Verbose JSON: {"temperature":82.5,"timestamp":1717200000} ~40 byte
  Anahtar kısalt / binary (Protobuf, Sparkplug B) → %80'e varan azalma.
  Fabrika LAN'ında önemsiz; 4G/uydu/internet üzerinden faturayı belirler.

ÖNCELİK 4 — Topic kardinalitesini ve retained sayısını sınırla
  Her retained mesaj broker'ın bellekte ve diskte tuttuğu kalıcı yüktür.
  Yalnızca state retain et. Telemetri retain=False.

ÖNCELİK 5 — Keepalive'ı senaryoya göre ayarla
  Stabil LAN: keepalive 60-120 sn (PINGREQ yükü düşük).
  Hızlı kopuş tespiti gereken kritik sistem: 10-20 sn (LWT hızlı tetiklenir),
  ama broker'a düzenli ping yükü gelir — denge kur.

ÖNCELİK 6 — Bağlantı sayısını ve clean-session politikasını yönet
  Binlerce kısa ömürlü bağlantı yerine kalıcı (persistent) bağlantı kullan.
  Offline mesaj gereken cihazlarda clean_session=False + sabit Client ID;
  gereksiz yere persistent session tutmak broker belleğini şişirir.

ÖNCELİK 7 — Broker yatay ölçekleme (en son çare)
  Yukarıdakiler tükendiğinde cluster (EMQX/HiveMQ). Donanım atmadan
  önce mesaj tasarımını düzeltmek neredeyse her zaman daha ucuzdur.

Genel kural: Önce "ne kadar az mesaj, ne kadar küçük, ne kadar düşük QoS"
gönderebileceğini sor; broker'ı güçlendirmek son adımdır.
```

## Derin Teknik Detay

MQTT'nin tasarım kararlarını anlamak, onu doğru kullanmanın anahtarıdır. Protokol 1999'da SCADA için petrol boru hattı telemetrisi (uydu, çok düşük bant genişliği, sık kopan hat) üzerine tasarlandı — bu köken, tüm tasarımı açıklar.

```
1. Neden Broker-Aracılı Pub/Sub? (Decoupling)
   ────────────────────────────────────────────
   İstek-yanıt (Modbus/OPC UA) modelinde gönderen ve alan birbirini
   bilmek ZORUNDA: IP, port, hazır olma durumu. MQTT broker'ı araya
   koyarak üç boyutta ayrıştırma (decoupling) sağlar:
     • Uzay (space): Publisher subscriber'ın adresini bilmez.
     • Zaman (time): Subscriber offline'ken yayınlanan mesaj (session
       + QoS 1) sonra teslim edilebilir.
     • Senkronizasyon: Publisher yayınlayıp işine devam eder, yanıt
       beklemez (fire-and-forget). İstek-yanıttaki blokaj yoktur.
   Bedeli: Broker bir SPOF ve ekstra atlamadır (latency + altyapı).

2. Neden LWT + Retained = Broker'ın "Durum Hafızası"
   ──────────────────────────────────────────────────
   MQTT istemcileri durumsuz (stateless) olabilir; durumu broker tutar.
   • Retained: "Bu topic'in SON değeri nedir?" sorusunu broker yanıtlar —
     yayıncı gitmiş olsa bile. Broker bir nevi son-değer veritabanıdır.
   • LWT: Broker, istemcinin ölümünü onun adına ilan eder. İstemci
     "öleceğini" peşinen broker'a söyler; öldüğünde broker konuşur.
   İkisi birlikte: Broker, bağlı olmayan cihazların güncel durumunu
   bile yeni gelenlere anlatabilen merkezi bir state machine olur.
   Bu, OPC UA'nın "sunucuya sor, sunucu ayakta olmalı" modelinin tersidir.

3. Neden Üç QoS Seviyesi? (Teslimat / Overhead Takası)
   ────────────────────────────────────────────────────
   Güvenilirlik bedavadır sanılır; değildir. Her garanti seviyesi
   ek round-trip ve broker state demektir:
     QoS 0: 0 ek paket, 0 broker state → kayıp mümkün.
     QoS 1: +1 PUBACK, gönderen mesajı ack gelene dek saklar → duplikasyon.
     QoS 2: +3 paket, hem gönderen hem broker state machine tutar (PUBREC/
            PUBREL/PUBCOMP) → tam-bir-kez, ama en yavaş ve en pahalı.
   Tasarımcılar "tek bir güvenilirlik" dayatmak yerine seçimi uygulamaya
   bıraktı: telemetride kayıp önemsizken sayaçta felakettir.

4. Neden TCP Üzerinde 2 Byte'lık Sabit Başlık?
   ─────────────────────────────────────────────
   Uydu/2G hattında her byte para ve enerjidir. Sabit başlık 2 byte;
   Remaining Length alanı değişken uzunluklu kodlama (variable-length
   integer) kullanır — küçük mesajlar 1 byte uzunluk alanıyla geçer.
   HTTP'nin onlarca satırlık metin başlığına karşı bu, pille çalışan
   sahada cihazın aylarca dayanmasını sağlayan tasarımdır.
   Port 1883 (düz) / 8883 (TLS) ayrımı IANA'da rezervedir; TLS handshake
   ek byte getirir ama transport şifrelemesi başka türlü sağlanamaz
   (MQTT'nin kendi içinde uygulama katmanı şifrelemesi yoktur).

5. MQTT vs Alternatifler — Neden "Gerçek Zamanlı Değil"
   ─────────────────────────────────────────────────────
   MQTT TCP üzerinde çalışır; TCP retransmission ve broker kuyruğu
   deterministik gecikme vermez. Motion control'ün µs-ms determinizmi
   MQTT'de YOKTUR — bu yüzden saha kontrolünde EtherCAT/PROFINET kalır.
   MQTT'nin yeri: "event-driven, hafif, çok-alıcılı, bulut-yerel telemetri".
   • vs AMQP: AMQP daha zengin kuyruk/routing semantiği ama çok daha ağır.
   • vs HTTP/REST: REST istek-yanıt + polling; MQTT push + kalıcı bağlantı,
     binlerce cihazda çok daha verimli.
   • vs OPC UA: OPC UA semantik + güvenlik + browse; MQTT bunların hiçbirini
     vermez, bunun yerine sadeliği ve ölçeklenebilirliği verir.
   Doğru zihinsel model: MQTT bir "taşıma borusu"dur; anlamı (Sparkplug B)
   ve güvenliği (TLS) protokolün üstüne katman olarak eklersin.
```

## İlgili Konular

```
knowledge/protocols/mqtt/
└── 02_industrial_usage.md       → CODESYS, Sparkplug B, broker seçimi

knowledge/codesys/networking/
└── 04_mqtt_client.md            → CODESYS'te MQTT client kurulumu

knowledge/protocols/opc-ua/
└── 01_architecture.md           → MQTT ile karşılaştırma ve birlikte kullanım

Araçlar:
  MQTT Explorer   → GUI MQTT browser ve test aracı
  mosquitto_pub   → CLI publish
  mosquitto_sub   → CLI subscribe
  paho-mqtt       → Python kütüphanesi
  MQTTX           → Masaüstü ve CLI MQTT test istemcisi
```
