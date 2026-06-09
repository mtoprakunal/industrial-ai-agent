---
KONU        : CODESYS MQTT Client Kurulumu
KATEGORİ    : codesys
ALT_KATEGORI: networking
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/libs/MQTT%20Client%20SL/Current/index.html"
    başlık: "CODESYS Online Help — MQTT Client SL Library Documentation"
    güvenilirlik: resmi
  - url: "https://us.store.codesys.com/codesys-iiot-libraries-sl.html"
    başlık: "CODESYS Store — IIoT Libraries SL (MQTT Client SL dahil)"
    güvenilirlik: resmi
  - url: "https://github.com/rossmann-engineering/CoDeSys-MQTT-library"
    başlık: "GitHub — CoDeSys MQTT Library (Topluluk kütüphanesi)"
    güvenilirlik: topluluk
  - url: "https://github.com/stefandreyer/CODESYS-MQTT"
    başlık: "GitHub — CODESYS-MQTT (Topluluk kütüphanesi, tüm QoS)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_opcua_server.md"
    ilişki: tamamlar
  - konu: "03_tcp_socket.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/programming/02_gvl_design.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "MQTT temel kavramları: Broker, Topic, Publish, Subscribe, QoS"
  - "JSON veya başka serileştirme formatına aşinalık"
  - "CODESYS kütüphane sistemi (programming/04_libraries.md)"
ÇELİŞKİLER :
  - kaynak: "CODESYS IIoT Libraries SL (Resmi) vs Topluluk kütüphaneleri"
    konu: "Hangi MQTT kütüphanesi kullanılmalı?"
    çözüm: >
      Resmi: CODESYS IIoT Libraries SL (ücretli, CODESYS Store).
      Topluluk: rossmann-engineering veya stefandreyer GitHub kütüphaneleri (ücretsiz).
      Topluluk kütüphaneler yaygın kullanılır ve production projelerde çalışır.
      Ücretli sürüm TLS/SSL desteği ve resmi bakımla öne çıkar.
      Başlangıç için: stefandreyer kütüphanesi (tüm QoS, iyi dokümantasyon).
  - kaynak: "QoS 1 vs QoS 2 CODESYS gerçekleştirimleri"
    konu: "Bazı kütüphaneler QoS 2 (Exactly Once) tam desteklemiyor"
    çözüm: >
      Endüstriyel uygulamalar için QoS 1 (At Least Once) çoğunlukla yeterlidir.
      QoS 2 daha yüksek protokol yükü getirir ve tüm kütüphanelerde stabil değildir.
      Kritik mesaj teslimi için QoS 1 + uygulama katmanında tekrar mantığı tercih et.
---

## Özün Ne

MQTT, hafif ve event-driven bir mesajlaşma protokolüdür. PLC'yi MQTT client olarak yapılandırmak; makine verilerini bulut platformlarına (AWS IoT, Azure IoT Hub, Google Cloud IoT), SCADA sistemlerine veya enerji yönetim platformlarına gerçek zamanlı göndermek için giderek yaygınlaşan bir yaklaşımdır. OPC UA'ya kıyasla çok daha düşük bant genişliği tüketir; JSON tabanlı payload yapısıyla da modern IoT altyapılarıyla doğal uyum sağlar. CODESYS'te yerleşik MQTT desteği yoktur, ancak CODESYS Store'dan veya açık kaynak olarak kütüphane eklemek mümkündür.

## Nasıl Çalışır

### MQTT Mimarisi

```
PLC (MQTT Client — Publisher + Subscriber)
    │
    │ TCP/TLS (port 1883 şifresiz / 8883 TLS)
    ▼
MQTT Broker (Mosquitto / AWS IoT / Azure IoT Hub / HiveMQ)
    │
    ├──► SCADA (Subscriber — makine verisini izler)
    ├──► Bulut Platform (Subscriber — veri analitiği)
    └──► Mobil App (Publisher — komut gönderir → PLC Subscribe eder)
```

### Publish/Subscribe Modeli

```
PUBLISH (Yayınlama):
  PLC → Broker'a mesaj gönderir
  Topic: "factory/line1/machine3/temperature"
  Payload: "82.5"

SUBSCRIBE (Abone Olma):
  PLC, belirli topic'leri dinler
  Topic filter: "factory/line1/machine3/commands/#"
  # = çok seviyeli wildcard (tüm alt topicler)
  + = tek seviyeli wildcard
```

### QoS Seviyeleri

```
QoS 0 — At Most Once (En fazla bir kez)
  Gönderim garantisi yok. Ağ kesilirse mesaj kaybolur.
  Kullanım: Sürekli güncellenen sensör verileri (kaybolan 1 değer sorun değil)
  Avantaj: En düşük overhead — her mesaj tek bir paket

QoS 1 — At Least Once (En az bir kez)
  Mesaj en az bir kez iletilir. Duplikasyon mümkün.
  Broker'dan PUBACK alınana kadar yeniden gönderilir.
  Kullanım: Alarm bildirimleri, kritik proses değerleri
  Avantaj: Güvenilir teslimat + makul overhead

QoS 2 — Exactly Once (Tam olarak bir kez)
  Mesaj tam olarak bir kez iletilir. Duplikasyon yok.
  4 yönlü handshake: PUBLISH → PUBREC → PUBREL → PUBCOMP
  Kullanım: Finansal işlemler, hassas sayaçlar
  Dezavantaj: En yüksek overhead; bazı kütüphanelerde stabil değil
```

### Topic Tasarımı — Endüstriyel Standart

```
Endüstriyel MQTT topic şeması (SparkplugB'ye benzer):

factory/{site}/{area}/{line}/{device}/{data_type}/{variable}

Örnekler:
  factory/istanbul/imalat/line1/paketleme/telemetry/temperature
  factory/istanbul/imalat/line1/paketleme/telemetry/speed
  factory/istanbul/imalat/line1/paketleme/status/running
  factory/istanbul/imalat/line1/paketleme/alarms/motor_fault
  factory/istanbul/imalat/line1/paketleme/commands/setpoint_speed

Wildcard kullanımı:
  factory/istanbul/+/line1/#    → İstanbul'daki tüm alanların line1 verileri
  factory/#                     → Tüm fabrika verisi (dikkat: yüksek trafik)
```

## Pratikte Nasıl Kullanılır

### Adım 1: Kütüphane Kurulumu

**Seçenek A — Resmi CODESYS IIoT Libraries SL:**
```
CODESYS Store → "IIoT Libraries SL" satın al + indir
Tools → Library Repository → Install → *.package
Library Manager → Add Library → "MQTT Client SL"
```

**Seçenek B — Topluluk (stefandreyer — Önerilen Başlangıç):**
```
https://github.com/stefandreyer/CODESYS-MQTT → Release → İndir
Tools → Library Repository → Install → MQTT.library
Library Manager → Add Library → "MQTT"
```

**Seçenek C — Rossmann Engineering (Basit API):**
```
https://github.com/rossmann-engineering/CoDeSys-MQTT-library
Library Manager → Add Library → "MQTT_Client"
Namespace: MQTT_Client
```

### Adım 2: Broker Kurulumu (Test için Mosquitto)

```bash
# Linux'ta Mosquitto kurulumu
sudo apt install mosquitto mosquitto-clients

# Basit konfigürasyon — test için anonymous erişim
echo "listener 1883
allow_anonymous true" | sudo tee /etc/mosquitto/conf.d/local.conf

sudo systemctl restart mosquitto

# Test: Terminal 1 — Subscribe
mosquitto_sub -h 127.0.0.1 -t "factory/#" -v

# Test: Terminal 2 — Publish
mosquitto_pub -h 127.0.0.1 -t "factory/line1/temperature" -m "82.5"
```

### Adım 3: CODESYS'te MQTT Client (Rossmann Kütüphane Örneği)

```iecst
(* Global değişkenler — GVL_MQTT *)
VAR_GLOBAL
    fbMQTTClient    : MQTT_Client.FB_MQTTClient;
    fbMQTTPublish   : MQTT_Client.FB_MQTTPublish;
    fbMQTTSubscribe : MQTT_Client.FB_MQTTSubscribe;
    
    xMQTTConnected  : BOOL;
    sLastPayload    : STRING(256);
    sLastTopic      : STRING(128);
END_VAR

(* PRG_MQTTManager — Task_Background içinde *)
PROGRAM PRG_MQTTManager

(* Bağlantı yönetimi *)
GVL_MQTT.fbMQTTClient(
    Enable       := GVL_State.xSystemOK,
    sBrokerAddress := '192.168.1.10',
    nPort          := 1883,
    sClientID      := 'CODESYS_Line1_Paketleme',   (* Unique client ID *)
    sUsername      := 'plc_user',                   (* Boş bırakılabilir *)
    sPassword      := 'plc_password',
    nKeepAlive     := 60,                            (* Saniye *)
    
    (* Last Will & Testament — Bağlantı kopunca broker yayınlar *)
    sWillTopic     := 'factory/line1/paketleme/status/online',
    sWillPayload   := 'false',
    bWillRetain    := TRUE,
    nWillQoS       := 1
);

GVL_MQTT.xMQTTConnected := GVL_MQTT.fbMQTTClient.bConnected;
```

### Adım 4: Veri Yayınlama (Publish)

```iecst
(* PRG_MQTTPublish — Task_Slow içinde (100ms) *)
PROGRAM PRG_MQTTPublish
VAR
    sPayload    : STRING(256);
    tPublishTimer : TON;
    nPublishInterval : TIME := T#5S;    (* Her 5 saniyede yayınla *)
END_VAR

tPublishTimer(IN := GVL_MQTT.xMQTTConnected, PT := nPublishInterval);

IF tPublishTimer.Q THEN
    tPublishTimer(IN := FALSE);
    
    (* JSON payload oluştur *)
    sPayload := '{';
    sPayload := CONCAT(sPayload, '"temperature":');
    sPayload := CONCAT(sPayload, REAL_TO_STRING(GVL_Diagnostics.rTemperature));
    sPayload := CONCAT(sPayload, ',"speed":');
    sPayload := CONCAT(sPayload, REAL_TO_STRING(GVL_Diagnostics.rActualSpeed));
    sPayload := CONCAT(sPayload, ',"running":');
    IF GVL_State.xRunning THEN
        sPayload := CONCAT(sPayload, 'true');
    ELSE
        sPayload := CONCAT(sPayload, 'false');
    END_IF
    sPayload := CONCAT(sPayload, ',"production_count":');
    sPayload := CONCAT(sPayload, DWORD_TO_STRING(GVL_Diagnostics.dwProductionCount));
    sPayload := CONCAT(sPayload, '}');
    
    (* Telemetri yayınla *)
    GVL_MQTT.fbMQTTPublish(
        Enable      := TRUE,
        sTopic      := 'factory/istanbul/imalat/line1/paketleme/telemetry',
        sPayload    := sPayload,
        nQoS        := 1,          (* At Least Once *)
        bRetain     := FALSE,      (* Broker'da saklanmasın *)
        MQTT_Client := GVL_MQTT.fbMQTTClient
    );
    
    (* Online durumu yayınla (retained) *)
    GVL_MQTT.fbMQTTPublish(
        Enable      := TRUE,
        sTopic      := 'factory/istanbul/imalat/line1/paketleme/status/online',
        sPayload    := 'true',
        nQoS        := 1,
        bRetain     := TRUE,       (* Broker'da sakla — yeni subscriber anında görsün *)
        MQTT_Client := GVL_MQTT.fbMQTTClient
    );
END_IF

(* Alarm yayınlama — EVENT tabanlı, her değişimde *)
IF GVL_Alarms.xMotorFault AND NOT GVL_Alarms.xMotorFault_PrevState THEN
    GVL_MQTT.fbMQTTPublish(
        Enable   := TRUE,
        sTopic   := 'factory/istanbul/imalat/line1/paketleme/alarms/motor_fault',
        sPayload := '{"active":true,"timestamp":"' + DT_TO_STRING(NOW()) + '"}',
        nQoS     := 1,
        bRetain  := TRUE,
        MQTT_Client := GVL_MQTT.fbMQTTClient
    );
END_IF
GVL_Alarms.xMotorFault_PrevState := GVL_Alarms.xMotorFault;
```

### Adım 5: Komut Alma (Subscribe)

```iecst
(* PRG_MQTTSubscribe — Task_Background içinde *)
PROGRAM PRG_MQTTSubscribe
VAR
    xSubscribed : BOOL;
END_VAR

(* Subscribe yalnızca bir kez yapılır (bağlantı kurulunca) *)
IF GVL_MQTT.xMQTTConnected AND NOT xSubscribed THEN
    GVL_MQTT.fbMQTTSubscribe(
        Enable      := TRUE,
        sTopicFilter:= 'factory/istanbul/imalat/line1/paketleme/commands/#',
        nQoS        := 1,
        MQTT_Client := GVL_MQTT.fbMQTTClient
    );
    xSubscribed := TRUE;
END_IF

IF NOT GVL_MQTT.xMQTTConnected THEN
    xSubscribed := FALSE;  (* Bağlantı kesilince tekrar subscribe edilecek *)
END_IF

(* Gelen mesajları işle *)
IF GVL_MQTT.fbMQTTClient.bNewMessageReceived THEN
    GVL_MQTT.sLastTopic   := GVL_MQTT.fbMQTTClient.sTopicReceived;
    GVL_MQTT.sLastPayload := GVL_MQTT.fbMQTTClient.sPayloadReceived;
    
    (* Topic'e göre işle *)
    IF GVL_MQTT.sLastTopic = 'factory/istanbul/imalat/line1/paketleme/commands/setpoint_speed' THEN
        GVL_Params.rSpeedSetpoint := STRING_TO_REAL(GVL_MQTT.sLastPayload);
    
    ELSIF GVL_MQTT.sLastTopic = 'factory/istanbul/imalat/line1/paketleme/commands/start' THEN
        IF GVL_MQTT.sLastPayload = 'true' THEN
            GVL_HMI.xRemoteStartCmd := TRUE;
        END_IF
    
    ELSIF GVL_MQTT.sLastTopic = 'factory/istanbul/imalat/line1/paketleme/commands/recipe' THEN
        GVL_Params.nRemoteRecipeRequest := STRING_TO_INT(GVL_MQTT.sLastPayload);
    END_IF
END_IF
```

## Örnekler

### Örnek 1: Retained Mesaj Kullanımı

```iecst
(* Retained = TRUE: Broker bu mesajın son değerini saklar. *)
(* Yeni bir subscriber bağlandığında hemen bu değeri alır. *)
(* Makinenin mevcut durumunu "duyurmak" için ideal: *)

(* Online/offline durumu — Last Will ile bütünleşik *)
(* Bağlantı kurulunca: 'true' yayınla (retained) *)
(* Bağlantı kopunca: Broker Last Will'i yayınlar → 'false' (retained) *)

(* Başka subscriber bağlandığında doğrudan güncel online durumunu alır *)
(* "Bu PLC online mı?" sorusu için broker'a sorgu yetmez — retained kontrol et *)
```

### Örnek 2: SparkplugB Benzeri Topic Yapısı

```
SparkplugB formatı — Endüstride standartlaşan topic şeması:
  spBv1.0/{group_id}/NBIRTH/{edge_node_id}      → Node doğum bildirimi
  spBv1.0/{group_id}/DDATA/{edge_node_id}/{device_id}  → Cihaz verisi

Basitleştirilmiş endüstriyel şema (SparkplugB gerektirmeksizin):
  {factory}/{site}/{area}/{line}/{device}/birth      → İlk bağlantı metadata
  {factory}/{site}/{area}/{line}/{device}/data       → Periyodik telemetri
  {factory}/{site}/{area}/{line}/{device}/alarm      → Anlık alarm
  {factory}/{site}/{area}/{line}/{device}/cmd        → Komutlar (subscribe)
  {factory}/{site}/{area}/{line}/{device}/status     → Online/offline (retained)
```

### Örnek 3: Node-RED ile MQTT Bridge

```javascript
// Node-RED: PLC MQTT → Dashboard görselleştirme
// MQTT In node konfigürasyonu:
{
  "broker": "192.168.1.10:1883",
  "topic": "factory/istanbul/imalat/line1/paketleme/telemetry",
  "qos": 1
}

// Function node: JSON parse + dashboard'a aktar
msg.payload = JSON.parse(msg.payload);
msg.temperature = msg.payload.temperature;
msg.speed = msg.payload.speed;
return msg;

// Gauge node: msg.temperature → 0-100°C göstergesi
```

### Örnek 4: AWS IoT Core Entegrasyonu

```iecst
(* AWS IoT Core — TLS zorunlu, port 8883 *)
(* CODESYS IIoT Libraries SL (ücretli) TLS destekler *)

GVL_MQTT.fbMQTTClient(
    Enable         := TRUE,
    sBrokerAddress := 'xxxxxxxxxx.iot.eu-west-1.amazonaws.com',
    nPort          := 8883,         (* TLS port *)
    sClientID      := 'PLC_Line1_Paketleme',
    
    (* TLS sertifika dosya yolları — PLC dosya sisteminde *)
    sCACertFile    := '/home/codesys/certs/AmazonRootCA1.pem',
    sCertFile      := '/home/codesys/certs/device.pem.crt',
    sPrivKeyFile   := '/home/codesys/certs/private.pem.key'
);

(* Topic formatı AWS IoT için: *)
(* Publish: dt/myFactory/line1/paketleme/telemetry *)
(* Subscribe: cmd/myFactory/line1/paketleme/# *)
```

## Sık Yapılan Hatalar

### Hata 1: Client ID Çakışması

```
Semptom: MQTT bağlantısı sürekli kuruluyor-kopuyor.
Neden  : Aynı Client ID'yi kullanan iki istemci var.
         Broker biri bağlandığında diğerini atar; eski client yeniden bağlanmaya çalışır.
Çözüm  : Her PLC instance'ı benzersiz Client ID kullanmalı.
          Örnek: 'PLC_' + sMachineName + '_' + sSerialNumber
```

### Hata 2: Yanlış QoS ile Kritik Veri Gönderme

```
❌ Alarm verisini QoS 0 ile göndermek:
   Ağ anlık kesilirse alarm mesajı kaybolur.
   SCADA alarm görmeden makine hatalı durumda devam eder.

✅ Alarm verisi: QoS 1 (At Least Once) ile gönder.
   Duplikasyon olursa timestamp ile filtrele.
```

### Hata 3: Periyodik Publish Yerine Her Döngüde Publish

```iecst
(* ❌ YANLIŞ — Her 10ms'de publish *)
(* Task_Control (10ms) içinde: *)
fbMQTTPublish(Enable := TRUE, sPayload := REAL_TO_STRING(rTemp));
(* 10ms = 100 msg/sn — broker ve ağ aşırı yüklenebilir *)

(* ✅ DOĞRU — Timer ile sınırla *)
(* Task_Background içinde 5s interval: *)
tPublishTimer(IN := xConnected, PT := T#5S);
IF tPublishTimer.Q THEN
    tPublishTimer(IN := FALSE);
    fbMQTTPublish(Enable := TRUE, ...);
END_IF
```

### Hata 4: Last Will Olmadan Online Durumu

```
Last Will & Testament olmadan PLC bağlantısı kesilirse:
  Broker herhangi bir mesaj yayınlamaz.
  SCADA/Dashboard "PLC offline" diyemez.
  
Last Will yapılandırması:
  Topic:   factory/.../status/online
  Payload: 'false'
  Retain:  TRUE
  QoS:     1
  
Bağlantı kurulunca PLC 'true' yayınlar (retained).
Bağlantı kopunca broker 'false' yayınlar (Last Will, retained).
```

### Hata 5: String Payload'da Locale Bağımlı Ondalık Ayırıcı

```iecst
(* ❌ YANLIŞ — Locale'e göre ',' veya '.' kullanabilir *)
sPayload := REAL_TO_STRING(82.5);  
(* Alman locale'de → "82,5" → JSON parse hatası *)

(* ✅ DOĞRU — Format kontrolü *)
sTemp := REAL_TO_STRING(rTemperature);
(* ',' karakterini '.' ile değiştir *)
sTemp := REPLACE(sTemp, ',', '.', 1, 0);  (* Util kütüphanesi REPLACE fonksiyonu *)
sPayload := CONCAT('{"temp":', sTemp);
sPayload := CONCAT(sPayload, '}');
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**MQTT Tercih Et:**
- Bulut platformu entegrasyonu (AWS, Azure, GCP)
- Düşük bant genişliği ortamı (4G/LTE üzerinden makine verisi)
- Çok sayıda IoT cihazını merkezi broker üzerinden koordine etme
- Event-driven bildirim (değer değişince hemen gönder)
- Mobile dashboard, web uygulaması entegrasyonu
- Node-RED, Grafana, InfluxDB gibi modern araçlarla kolay entegrasyon

**MQTT Tercih Etme:**
- Güvenilir ağ yoksa ve QoS 0 yeterliyse → Verimli ama kayıp riski var
- Gerçek zamanlı kontrol sinyali → MQTT gecikme garantisi vermiyor
- OPC UA destekleyen SCADA → OPC UA daha zengin veri modeli sunar
- Modbus TCP destekleyen eski SCADA → Modbus daha basit entegrasyon

## Gerçek Proje Notları

**Not 1 — Client ID Çakışmasının Bulunması**  
Bir projede iki hat aynı Client ID ile broker'a bağlanıyordu (`PLC_Paketleme`). Bağlantı her 30 saniyede kopuyordu. Wireshark'ta DISCONNECT paketi görüldü — broker aynı ID'yi görünce eski bağlantıyı attı. Client ID benzersiz yapılınca sorun çözüldü.

**Not 2 — Locale ve Ondalık Sorun**  
Alman dili ayarlı bir sistemde `REAL_TO_STRING(98.7)` → `"98,7"` döndürdü. Node-RED JSON parse hatası aldı. `REPLACE()` ile `,` → `.` değiştirilince sorun çözüldü. Tüm MQTT payload'larında sayısal değerler için bu dönüşüm standart hale getirildi.

**Not 3 — Last Will ile Dashboard Güvenilirliği**  
PLC ağ bağlantısı kesildiğinde dashboard "PLC Online: true" göstermeye devam ediyordu. Last Will yapılandırılmamıştı. LWT eklendikten sonra bağlantı kopunca Grafana dashboard'u 30 saniye içinde "Offline" göstermeye başladı.

**Not 4 — MQTT ile OPC UA Birlikte**  
Bir projede OPC UA (SCADA → PLC kontrolü) ve MQTT (PLC → Bulut veri analizi) birlikte kullanıldı. OPC UA güvenli, iki yönlü SCADA iletişimi için; MQTT sadece gönderi (publish only) bulut veri akışı için. İki protokol çakışmadı; her biri kendi gücünde kullanıldı. Bu kombinasyon endüstride giderek yaygınlaşıyor.

**Not 5 — Broker Erişilemezken Bloke Eden Publish ve Mesaj Birikimi**  
Broker bakıma alındığında, MQTT publish FB'si bağlantı kurmaya çalışırken Task_Slow'da gecikmeler yarattı; ayrıca offline süre boyunca üretilen telemetri "birikti" ve broker dönünce 5 dakikalık eski veri sel gibi gönderildi (yanıltıcı grafikler). Ders: MQTT mantığını **Freewheeling/düşük öncelikli task**'a koy (TCP gibi bloke edebilir); offline'da telemetri biriktirme — ya en son değeri tut (retained mantığı) ya da timestamp'li gönder. Broker erişilebilirliğini bir bağlantı-durumu bayrağıyla izle, publish'i ona bağla.

**Not 6 — QoS 1 Duplikasyonu ve Idempotency**  
Alarm mesajları QoS 1 (at-least-once) ile gönderildi; ağ tıkanınca PUBACK gecikti, FB yeniden gönderdi — broker aynı alarmı iki kez aldı, SCADA çift alarm kaydı oluşturdu. Ders: QoS 1 **duplikasyon** üretebilir; alıcı tarafı **idempotent** olmalı (her mesaja benzersiz ID/timestamp koy, alıcı tekrarı filtrele). "Tam olarak bir kez" için QoS 2 vardır ama overhead yüksek ve bazı kütüphanelerde stabil değil — pratikte QoS 1 + idempotency tercih edilir.

**Not 7 — Retained Mesaj "Hayalet Değer" Tuzağı**  
Bir setpoint komutu `commands/setpoint` topic'ine retained gönderildi. Aylar sonra yeni bir PLC aynı topic'e subscribe olunca broker'daki **eski retained komutu** anında teslim etti — makine beklenmedik bir setpoint'e atladı. Ders: Komut (command) topic'lerini ASLA retained gönderme (retained yalnızca durum/state için anlamlı: "son bilinen değer"). Komutlar anlıktır; retained komut "zombi komut" olarak geri gelir. Retained = durum bildirimi (online, son setpoint okuması), retained ≠ komut.

## Edge Case'ler ve Sistem Limitleri

### MQTT Davranış Edge Case'leri

```
Edge Case                          Sonuç                     Koruma
─────────────────────────────────────────────────────────────────────
Aynı Client ID iki istemci         Sürekli bağlan-kop        benzersiz Client ID
QoS 1 PUBACK gecikmesi             Duplikasyon               idempotency (mesaj ID)
Retained komut topic'i             Zombi komut geri gelir    komut retained DEĞİL
Broker offline + biriken telemetri Sel + eski veri           offline biriktirme yok
Kablo koptu, keepalive yok         Geç offline tespiti       keepalive/LWT
JSON locale (98,5 vs 98.5)         Parse hatası              REPLACE ',' → '.'
Topic'te boşluk/Türkçe karakter    Bazı broker reddeder      ASCII + tire/slash
Payload çok büyük                  Broker max packet sınırı  parçala veya küçült
```

### MQTT'in Garanti Etmedikleri

```
- Gerçek zamanlı teslimat: broker gecikmesi + ağ + QoS handshake değişken
- Sıralama: farklı topic'ler arası sıra garantisi yok (aynı topic+QoS1 içinde var)
- Bağlantı sürekliliği: keepalive aşımı → broker bağlantıyı düşürür
- Mesaj kalıcılığı: QoS 0 kaybolabilir; retained yalnızca SON mesajı tutar (geçmiş yok)
```

### Güvenlik Sınırları

```
Port 1883 (şifresiz)   → açık metin; internet üzerinden ASLA
Port 8883 (TLS)        → sertifika gerekir; ücretli IIoT SL veya TLS-destekli lib
anonymous broker        → ağdaki herkes publish/subscribe edebilir
ACL (topic yetkisi)     → broker tarafında; PLC değil broker zorlar
```

## Optimizasyon

### Bant Genişliği: MQTT'in Asıl Gücü

```
- Yalnızca DEĞİŞENİ yayınla (report-by-exception), her döngü değil → ağ ↓
- Telemetriyi grupla: 10 ayrı topic yerine tek JSON payload → daha az overhead
- QoS 0 sürekli sensör verisi için (kayıp 1 değer önemsiz), QoS 1 alarm için
- Retained ile durum: yeni subscriber broker'dan son değeri alır, PLC tekrar yayınlamaz
- Publish'i timer ile sınırla (Hata 3): 4G/LTE'de her saniye publish veri planını yer
```

### Task ve Bağlantı Yönetimi

MQTT FB'leri (özellikle bağlantı kurma) bloke edebilir — TCP gibi **Freewheeling/düşük öncelik** task'ta. Publish'i Task_Slow'da timer ile sınırla; bağlantı yönetimi + subscribe Task_Background'da. Ana kontrol task'ına MQTT koyma.

### Payload Formatı

```
JSON: okunabilir, evrensel, ama verbose (büyük) + parse maliyeti
SparkplugB (protobuf): kompakt, tipli, ama kütüphane + karmaşıklık
→ Düşük bant/çok cihaz → SparkplugB; basit/az cihaz → JSON
Locale tuzağı: REAL_TO_STRING ',' üretebilir → her sayısalda REPLACE ',' '.'
```

## Derin Teknik Detay

### Pub/Sub Neden Poll'dan Farklı? — Broker Aracılığı

Modbus/OPC UA client-server (PLC ↔ tüketici doğrudan), MQTT ise **broker-aracılı** pub/sub'tır: PLC broker'a yayınlar, broker ilgilenen tüm subscriber'lara dağıtır. Bu mimari decoupling sağlar:
- PLC, kim dinlediğini bilmez (1 veya 1000 subscriber, fark etmez — broker dağıtır).
- Subscriber, PLC online mı bilmez (broker retained/LWT ile durumu tutar).
- Yeni tüketici eklemek PLC'yi değiştirmez (broker'a subscribe olur).

Bu, "tek PLC → çok tüketici" senaryosunda Modbus/OPC UA'nın çoklu-bağlantı yükünü broker'a devreder. Bedeli: broker bir SPOF (tek hata noktası) ve ek gecikme katmanıdır. PLC'nin proaktif veri gönderebilmesi (Modbus'ın yapamadığı, Modbus derin-teknik-detay) MQTT'i bulut/telemetri için doğal kılar.

### Retained ve LWT: Broker'ın Durum Hafızası

MQTT'in iki "durum" mekanizması, broker'ı sadece mesaj dağıtıcı değil, **durum hafızası** yapar:
- **Retained:** Broker, bir topic'in son retained mesajını saklar; yeni subscriber bağlanınca anında alır. "Son bilinen durum" semantiği — online bayrağı, son setpoint okuması için ideal. Komut için DEĞİL (Not 7: zombi komut).
- **LWT (Last Will & Testament):** İstemci bağlanırken broker'a "ben aniden kopalarsam şu mesajı yayınla" der. Broker keepalive aşımını/kopuşu tespit edince LWT'yi yayınlar — PLC kendi offline'ını bildiremez (kopmuştur!), broker onun adına bildirir. Retained LWT = "online: false" → dashboard güvenilir offline tespiti (Not 3).

İkisi birlikte, bağlantısız (disconnected) bir PLC'nin durumunu bile sisteme yansıtır — Modbus/OPC UA'da olmayan bir yetenek.

### QoS: Teslimat Garantisi ile Overhead Ödünleşimi

```
QoS 0: PUBLISH (tek paket, fire-and-forget) → kayıp mümkün, en hızlı
QoS 1: PUBLISH → PUBACK (yeniden-gönderim PUBACK gelene dek) → duplikasyon mümkün
QoS 2: PUBLISH→PUBREC→PUBREL→PUBCOMP (4-yön) → tam-bir-kez, en yavaş
```

QoS, dağıtık sistemlerdeki klasik "at-most-once / at-least-once / exactly-once" teslimat semantiğidir. Exactly-once (QoS 2) teorik olarak ideal ama 4-yönlü handshake hem yavaş hem kütüphane-kırılgan; pratik endüstri çözümü **QoS 1 + uygulama-katmanı idempotency** (her mesaja benzersiz ID, alıcı tekrarı eler). Bu, "tam-bir-kez işleme"yi protokol yerine uygulamada çözer — dağıtık sistemlerde yaygın, sağlam bir desendir. QoS seçimi = "kayıp mı, duplikasyon mu, yoksa overhead mı kabul edilebilir?" sorusudur.

### MQTT Neden Yerleşik Değil? — Kütüphane Ekosistemi

CODESYS, Modbus/OPC UA'yı yerleşik sunar ama MQTT'i sunmaz (kütüphane gerekir). Çünkü MQTT, endüstriyel otomasyonun çekirdeğinden çok IoT/IT dünyasından gelir; CODESYS onu sonradan kütüphane (IIoT SL / topluluk) olarak ekledi. Bu, programming/04'teki kütüphane-sürüm-kilidi disiplinini gerektirir: hangi MQTT kütüphanesi (resmi TLS'li mi, topluluk mu), hangi sürüm, hangi QoS desteği — proje başında sabitlenmeli. TLS gereken (internet/bulut) projelerde ücretsiz topluluk kütüphaneleri yetersiz kalabilir; resmi IIoT SL'in TLS'i bu yüzden önemlidir.

## İlgili Konular

```
knowledge/codesys/networking/
├── 01_opcua_server.md        → Çift yönlü, güvenli SCADA iletişimi
├── 02_modbus_slave.md        → Basit, evrensel HMI iletişimi
└── 03_tcp_socket.md          → Özel protokol, MQTT kütüphanesi tabanı

knowledge/codesys/programming/
└── 02_gvl_design.md          → MQTT'ya gönderilecek değişkenlerin organizasyonu

Araçlar ve kaynaklar:
  Mosquitto          → https://mosquitto.org — yerel broker (ücretsiz)
  MQTT Explorer      → Görsel MQTT istemci, topic analizi
  Node-RED           → MQTT entegrasyonlu akış tabanlı programlama
  InfluxDB + Grafana → Zaman serisi veritabanı + dashboard
  AWS IoT Core       → Yönetilen bulut MQTT broker
  HiveMQ             → Kurumsal MQTT broker

Kütüphaneler:
  CODESYS IIoT Libraries SL → CODESYS Store (ücretli, resmi, TLS dahil)
  rossmann-engineering       → GitHub (ücretsiz, basit API)
  stefandreyer/CODESYS-MQTT  → GitHub (ücretsiz, tüm QoS, iyi dokümantasyon)
```
