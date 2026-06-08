---
KONU        : MQTT Protokol — Sentez
KATEGORİ    : protocols
ALT_KATEGORI: mqtt
SEVİYE      : Temel-Orta
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "knowledge/protocols/mqtt/01_basics.md"
    başlık: "MQTT Protokol Temelleri"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/mqtt/02_industrial_usage.md"
    başlık: "MQTT Endüstriyel Otomasyon Kullanımı"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_basics.md"
    ilişki: detaylandırır
  - konu: "02_industrial_usage.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/networking/04_mqtt_client.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "Bu sentez, iki kaynak belgeyi okuduktan sonra okunmak üzere tasarlanmıştır."
  - "Temel ağ kavramları (TCP/IP, pub/sub modeli)"
ÇELİŞKİLER :
  - kaynak: "QoS 2 her zaman daha güvenli algısı"
    konu: "Daha yüksek QoS ≠ her zaman daha iyi — gerçek tradeoff var"
    çözüm: >
      QoS 2 tam garanti sağlar ama 4 yönlü el sıkışma gerektirir.
      200 sensör × 1 msg/sn × 4 paket = 800 paket/sn → broker CPU %60.
      Telemetri QoS 0, alarm QoS 1 yeterli. QoS 2 yalnızca sayaç/finansal.
  - kaynak: "MQTT = IoT, OPC UA = endüstri — birini seç algısı"
    konu: "İkisi rakip değil katmanlı mimari bileşenleridir"
    çözüm: >
      OPC UA: Cihaz-SCADA katmanı (bidirectional, semantik, metod çağrısı).
      MQTT: Veri toplama-bulut katmanı (push, çok alıcı, ölçeklenebilir).
      En sağlıklı mimari ikisini birlikte kullanır. OPC UA PubSub, MQTT'yi
      transport olarak kullanabilir.
  - kaynak: "Ham MQTT yeterli, Sparkplug B gereksiz karmaşıklık"
    konu: "Sparkplug B entegrasyon süresini dramatik düşürür"
    çözüm: >
      Ham MQTT: 2-3 gün (topic analiz, payload decode, birim belgele, tag konfigure).
      Sparkplug B: 2-3 saat (NBIRTH metadata otomatik, araçlar tag yapısını okur).
      Ölçek büyüyünce fark katlanır.
---

## Özün Ne

Bu sentez, "MQTT'yi temel pub/sub mekanizmasından endüstriyel IIoT'ye kadar bütünsel görmek isteyene ne anlatılmalı?" sorusuna yanıt verir. İki kaynak belge birbirinin devamıdır: `01_basics.md` MQTT'nin nasıl çalıştığını (broker, QoS, retain, LWT, topic) öğretir; `02_industrial_usage.md` bu mekanizmaların fabrika ortamında nasıl şekillendiğini (Sparkplug B, broker seçimi, OPC UA entegrasyonu, UNS mimarisi) gösterir. Bu ikisi bir arada anlaşıldığında MQTT'nin neden bu kadar yaygınlaştığı ve onu doğru kullananla yanlış kullananı ayıran kararlar netleşir.

## Nasıl Çalışır

### İki Belgenin Birbirine Bağlantısı — Zihin Haritası

```
┌────────────────────────────────────────────────────────────────────────┐
│                    MQTT BÜTÜNSEL ZİHİN HARİTASI                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  01_basics.md — TEMELLERİ ANLAMA                                        │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  PUB/SUB MODELİ                                                   │  │
│  │  Publisher (PLC/Sensör)                                           │  │
│  │       │ PUBLISH → factory/line1/temp = 82.5                       │  │
│  │       ▼                                                            │  │
│  │  ┌─────────────────────────────┐                                  │  │
│  │  │        MQTT BROKER          │  ← Merkezi mesaj yönlendirici    │  │
│  │  │  • Topic Routing            │                                  │  │
│  │  │  • Retained Messages        │  ← Yeni subscriber anında alır  │  │
│  │  │  • QoS Management          │  ← Teslimat garantisi            │  │
│  │  │  • Session (offline buffer) │                                  │  │
│  │  │  • Last Will (LWT)          │  ← Kopma otomatik bildirilir    │  │
│  │  └──────────────┬──────────────┘                                  │  │
│  │                 │ PUBLISH (subscribe edilmişse)                    │  │
│  │                 ▼                                                  │  │
│  │  Subscriber'lar: SCADA | Bulut | Dashboard | Analitik             │  │
│  │  → Alıcı sayısı artsa da Publisher kodu değişmez (gevşek bağ)    │  │
│  │                                                                   │  │
│  │  QoS 0 → Fire & forget (telemetri)                               │  │
│  │  QoS 1 → At least once (alarm, retain)                           │  │
│  │  QoS 2 → Exactly once (sayaç — nadiren gerekli)                  │  │
│  └────────────────────────────┬──────────────────────────────────────┘  │
│                               │ Temeller endüstriyel bağlama taşınır    │
│                               ▼                                          │
│  02_industrial_usage.md — ENDÜSTRİYEL KULLANIM                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  SPARKPLUG B — Ham MQTT'nin endüstriyel eksiklerini kapatır       │  │
│  │    NBIRTH: Tüm tag'ler + metadata (birim, tip, aralık) bir kez    │  │
│  │    NDATA:  Yalnızca değişenler (bant genişliği %70-90 azalır)     │  │
│  │    NDEATH: LWT — kopuş otomatik bildirilir                        │  │
│  │    Protobuf payload → JSON'dan %80 daha küçük                     │  │
│  │                                                                   │  │
│  │  KATMANLı MİMARİ (OPC UA + MQTT birlikte):                       │  │
│  │    PLC ←→ SCADA          [OPC UA: RW, güvenli, semantik]          │  │
│  │    PLC → MQTT Broker     [MQTT: Publish, yüksek hacim]            │  │
│  │    Broker → InfluxDB     [Subscriber: historian]                  │  │
│  │    Broker → Grafana      [Subscriber: dashboard]                  │  │
│  │    Broker → AWS / Azure  [Subscriber: bulut]                      │  │
│  │    Broker → MES / ERP    [Subscriber: kurumsal]                   │  │
│  │                                                                   │  │
│  │  UNS (Unified Namespace):                                         │  │
│  │    12 PLC × 3 hedef = 36 bağlantı  → MQTT ile: 12 + 3 = 15       │  │
│  │    Yeni analitik sistemi: Yalnızca 1 subscriber ekle              │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

### "Yeni Başlayan" İçin Özet Mental Model

MQTT'yi anlamanın en kısa yolu şu dört cümleye sığar:

> **Broker**: Postane gibi çalışır — gönderenin kime gittiğini bilmesine gerek yok, alanın kimden geldiğini bilmesine gerek yok.

> **Topic**: Posta kutusu adresi. Hiyerarşik yap: `enterprise/site/area/device/datapoint`. Wildcard (`+`, `#`) ile sonradan grupla.

> **QoS + Retain + LWT**: Üçlü güvenlik ağı. QoS teslimatı, retain geç bağlananı, LWT beklenmedik kopuşu çözer.

> **Sparkplug B**: Ham MQTT + standart topic + Protobuf payload + metadata. Endüstriyel entegrasyonu saatlerden günlere taşımayı önler.

## Hızlı Referans Tabloları

### A. QoS Seviyeleri — Seçim Rehberi

| QoS | Garanti | Mekanizma | Overhead | Endüstriyel Kullanım |
|---|---|---|---|---|
| 0 | Yok (at most once) | Tek yönlü PUBLISH | 1 paket | Telemetri akışı, sıcaklık, hız (kayıp tolere edilir) |
| 1 | En az bir kez (tekrar mümkün) | PUBLISH + PUBACK | 2 paket | Alarm bildirimi, reçete parametresi, retain mesajlar |
| 2 | Tam olarak bir kez | 4 yönlü el sıkışma | 4 paket | Üretim sayacı, finansal veri (çoğu senaryoda gereksiz) |

**Kural**: Telemetri → 0, Alarm/Durum → 1, Sayaç/Finansal → 2. QoS 2'yi varsayılan yapma.

---

### B. Topic Tasarımı — Doğru / Yanlış

| Tasarım Kararı | Yanlış | Doğru |
|---|---|---|
| Hiyerarşi | `temp1`, `speed_motor2` | `factory/line1/motor1/speed` |
| Sıralama | `datapoint/device/area` | `enterprise/site/area/line/device/datapoint` |
| Wildcard uyumu | `line1_temp`, `line2_temp` | `factory/line1/temperature`, `factory/line2/temperature` → `factory/+/temperature` |
| Cihaz kimliği | `device_1d3a7f/speed` | `conveyor_motor/speed` (okunabilir isim) |
| Komut ayrımı | Hepsi aynı prefix | `telemetry/`, `command/`, `status/`, `alarm/` |
| Retain kullanımı | Her telemetri retain | Yalnızca durum ve config retain, akış verisi retain=False |

**ISA-95 tabanlı standart şema**: `enterprise/site/area/line/cell/device/datapoint`

---

### C. Sparkplug B / Endüstriyel Kullanım

| Konu | Ham MQTT | Sparkplug B |
|---|---|---|
| Topic yapısı | Serbest | `spBv1.0/{group}/{msg_type}/{edge_node}/{device}` (standart) |
| Payload | JSON, string, binary — herkeste farklı | Protobuf (kompakt, şemalı) |
| Metadata | Yok — payload'da tekrar et | NBIRTH'de bir kez: birim, tip, engineering range |
| Bant genişliği | Tüm değerler her seferinde | Report-by-exception: yalnızca değişenler (%70-90 azalma) |
| Cihaz durumu | Manuel LWT konfigure | NDEATH otomatik (standartta tanımlı) |
| Entegrasyon süresi | 2-3 gün (manuel analiz) | 2-3 saat (araçlar NBIRTH'i okur) |
| SCADA uyumu | Özel konfigürasyon | Ignition, HiveMQ Sparkplug Extension native desteği |

**Mesaj tipleri kısa özet**:
- `NBIRTH` / `DBIRTH` → Doğum: tüm tag + metadata
- `NDATA` / `DDATA` → Yalnızca değişenler
- `NDEATH` / `DDEATH` → Kopuş bildirimi (LWT)
- `NCMD` / `DCMD` → Komut (SCADA → Cihaz)

---

### D. Broker Seçimi Konsolide

| Senaryo | Önerilen Broker | Neden |
|---|---|---|
| Geliştirme ve test | Mosquitto | Kurulumu 1 dakika, kaynak yok denecek kadar az |
| Tek fabrika, < 1000 cihaz | Mosquitto veya EMQX Community | Yeterli kapasite, ücretsiz |
| Çok fabrika, binlerce cihaz | HiveMQ veya EMQX Enterprise | Cluster, HA, yönetim paneli |
| Sparkplug B + Ignition SCADA | Cirrus Link Chariot | Native Sparkplug desteği |
| AWS ekosistemi | AWS IoT Core | Yönetilen, sertifika tabanlı kimlik |
| Azure ekosistemi | Azure Event Grid MQTT | Yönetilen, Azure entegrasyonu |
| Yüksek hacim + kural motoru | EMQX | Erlang/OTP, 100M+ bağlantı, SQL kural motoru |
| Kurumsal Avrupa / IEC 62443 | HiveMQ | Güvenlik sertifikasyonu, uyumluluk |

**Kritik not**: Mosquitto tek node çalışır — broker SPOF olur. Üretim kritik sistemlerde HA cluster (HiveMQ veya EMQX) zorunlu.

---

### E. MQTT vs OPC UA vs Modbus — Ne Zaman Hangisi

| Karar | MQTT | OPC UA | Modbus TCP |
|---|---|---|---|
| Çok alıcıya veri dağıtımı | ✓ Ideal | Karmaşık | Hayır |
| Bulut / analitik entegrasyonu | ✓ Ideal | Ağır | Hayır |
| SCADA bidirectional kontrol | Kısmi | ✓ Ideal | Sınırlı |
| Semantik veri modeli | Yok | ✓ Zengin | Yok |
| Metod çağrısı | Yok | ✓ Var | Yok |
| Eski SCADA uyumluluğu | Düşük | Orta | ✓ Evrensel |
| Minimum overhead | ✓ | Hayır | ✓ |
| Güvenlik sertifikasyonu | TLS opsiyonel | ✓ Yerleşik | Yok |

**Doğru seçim**: OPC UA cihaz-SCADA katmanında, MQTT veri toplama-bulut katmanında. İkisi çelişmez, katmanlı çalışır.

## Pratikte Nasıl Kullanılır

### Katmanlı Endüstriyel Mimari — Kurulum Adımları

```
ADIM 1 — Topic Tasarımı (Başta Doğru Yap)
  ISA-95 hiyerarşisi:
  enterprise/site/area/line/cell/device/datapoint

  factory/
  ├── istanbul/imalat/line1/conveyor_motor/telemetry  (QoS 0, retain=False)
  ├── istanbul/imalat/line1/conveyor_motor/alarm/#    (QoS 1, retain=False)
  ├── istanbul/imalat/line1/status/online             (QoS 1, retain=True)
  └── istanbul/imalat/line1/command/#                 (QoS 1 — PLC subscribe)

ADIM 2 — LWT Konfigure Et (Her Zaman)
  Bağlanırken:
    LWT Topic:   factory/istanbul/line1/status/online
    LWT Payload: "false"
    LWT QoS: 1, LWT Retain: True
  Bağlanınca:
    PUBLISH: factory/.../status/online = "true" (QoS 1, retain=True)

ADIM 3 — QoS Ata
  Telemetri (sürekli):     QoS 0
  Alarm / komut / durum:   QoS 1
  Sayaç (exactly once):    QoS 2

ADIM 4 — Güvenlik Ekle
  Geliştirme: Port 1883, anonymous → Kabul edilebilir
  Production: Port 8883 (TLS), username/password, ACL → Zorunlu

ADIM 5 — Broker Seç (Ölçeğe Göre)
  Pilot / küçük: Mosquitto
  Orta-büyük:    EMQX Community
  Kurumsal HA:   HiveMQ veya EMQX Enterprise

ADIM 6 — UNS Mimarisi (Spaghetti'yi Çözer)
  Her PLC → Broker (bir bağlantı)
  Yeni alıcı (InfluxDB, Grafana, AWS, MES):
    Sadece yeni subscriber — PLC kodu değişmez
```

### CODESYS'te Hızlı MQTT Kurulum Kontrol Listesi

```
□ CODESYS MQTT Client kütüphanesi yüklü (04_mqtt_client.md'ye bak)
□ GVL_MQTT: Broker IP, port, kullanıcı adı, şifre
□ FB_MQTTClient: LWT konfigure (topic, payload "false", retain=True, QoS=1)
□ Bağlanınca: "true" yayınla (QoS 1, retain=True)
□ PRG_MQTTPublish: Periyodik (100ms veya 5sn) Task_Background'da çalış
□ Telemetri: QoS 0, retain=False
□ Alarm: QoS 1, retain=False
□ Broker bağlantısı: Port 8883 (TLS + kimlik doğrulama)
```

## Sık Yapılan Hatalar

**1. Topic'i Düz veya Anlamsız Tasarlamak**
`sensor1`, `temp_line2`, `alarm3` gibi düz isimler wildcard kullanımını imkânsız kılar. 3 ay sonra fabrika büyüyünce tüm subscriber'lar güncellenir, InfluxDB verileri eski yapıda kalır, Grafana bozulur. ISA-95 tabanlı hiyerarşiyi başlangıçta uygula.

**2. LWT'siz Deploy**
PLC beklenmedik kesildiğinde dashboard "Online" göstermeye devam eder. Operatör makineye gider, kimse yoktur. Her üretim sistemi LWT ile konuşlandırılmalı.

**3. Retain'i Telemetri Akışında Kullanmak**
Her telemetri mesajı retain=True olursa broker tüm son değerleri disk/bellekte saklar, yeniden başlatılınca hepsi yüklenir. Retain yalnızca durum (status, config) için. Sürekli akış verisi retain=False.

**4. Her Şeyi QoS 2 Yapmak**
200 sensör × 1 msg/sn × 4 paket = 800 paket/sn. Mosquitto CPU %60. QoS 0'a geçilince %8. QoS seviyesini iş gereksiniminden belirle, "daha güvenli olsun" mantığıyla değil.

**5. Broker'ı Güvensiz Açmak**
Port 1883 + anonymous = herkes bağlanabilir, komut gönderebilir. Production minimum: `allow_anonymous false`, `password_file`, TLS (8883), ACL.

**6. Payload'da Birim Bilgisi Yazmamak**
`factory/temperature = "82.5"` — Celsius mi Fahrenheit mi? Oran mı? Ham ADC mi? En azından JSON: `{"value": 82.5, "unit": "celsius"}`. En iyisi Sparkplug B: NBIRTH'de bir kez tanımla.

**7. Broker'ı SPOF Olarak Bırakmak**
Mosquitto tek node çalışır. Broker durdu, tüm MQTT durdu. Kritik üretim sistemlerinde HiveMQ veya EMQX cluster zorunlu.

## Ne Zaman ...

### MQTT Kullan

```
✓ Bir verinin aynı anda N alıcıya gitmesi gerekiyorsa (pub/sub gücü)
✓ Bulut platformu (AWS IoT, Azure IoT Hub) entegrasyonu varsa
✓ Farklı üreticilerden cihazları tek noktada toplamak istiyorsan
✓ Uzak veya düşük bant genişlikli bağlantı varsa (4G/LTE)
✓ Unified Namespace mimarisi kuruyorsan
✓ Analitik, zaman serisi veritabanı, Grafana pipeline'ı varsa
✓ Yeni alıcı eklenmesi PLC kodunu etkilemesini istemiyorsan
```

### MQTT Kullanma

```
✗ SCADA'nın PLC'ye setpoint yazması / alarm onaylaması gerekiyorsa → OPC UA
✗ Zengin semantik veri modeli veya metod çağrısı gerekiyorsa → OPC UA
✗ OPC UA sertifikalı güvenlik zorunluysa → OPC UA
✗ Gerçek zamanlı motion control komutları → Fieldbus (EtherCAT, PROFINET)
✗ Eski SCADA yalnızca Modbus biliyor → Modbus TCP
✗ Broker altyapısı kurulamıyorsa ve 2 cihaz doğrudan iletişim kuracaksa → Modbus TCP
```

### Sparkplug B Ekle

```
+ Birden fazla üretici/sistem NBIRTH metadata'yı otomatik okuyacaksa
+ Ignition SCADA veya HiveMQ Sparkplug Extension kullanıyorsan
+ Entegrasyon süresini dramatik kısaltmak istiyorsan
+ Bant genişliği kısıtlı ve report-by-exception gerekiyorsa
- Küçük pilot projede veya sadece test ediyorsan (ek karmaşıklık)
- Tüm alıcılar ham MQTT anlayan özel yazılımlarsa
```

## Gerçek Proje Notları

**Not 1 — Retained Mesaj Olmadan Boş Dashboard**
Bir fabrika dashboardu her sabah açılırken 30 saniye boş görünüyordu. PLC'ler retain=False ile yayınlıyordu. Dashboard subscribe olunca PLC'nin bir sonraki güncellemeyi göndermesini bekliyordu (ortalama 10 saniye). Retain=True eklenince dashboard açılır açılmaz tüm değerler mevcut. Grafana MQTT plugin ile doğrudan bağlantıda da aynı sorun yaşandı, aynı çözüm işe yaradı.

**Not 2 — LWT Olmadan 2 Saat "Phantom Online"**
Ağ ekipmanı güncelleme sırasında bir PLC beklenmedik biçimde kesildi. Dashboard 2 saat boyunca "Online" gösterdi. LWT yoktu. LWT eklendikten sonra kopuş 30 saniye içinde tespit edildi.

**Not 3 — QoS 2'nin Gerçek Maliyeti**
Pilot projede tüm mesajlar QoS 2: 200 sensör × 1/sn = 200 msg/sn × 4 paket = 800 paket/sn. Mosquitto CPU %60. QoS 0 (telemetri) + QoS 1 (alarmlar) geçişi: CPU %8. Kural pekişti: QoS seviyesi iş gereksiniminden belirlenir.

**Not 4 — Topic Değişikliğinin 2 Günlük Maliyeti**
Pilot projede topic yapısı `line1/temperature` şeklindeydi. Ölçek büyüyünce 3 fabrika eklendi. Topic `istanbul/line1/temperature` yapısına taşındı. InfluxDB eski veri yeni yapıyla eşleşmedi — analitik bozuldu. 2 günlük veri migrasyonu. Ders: ISA-95 tabanlı topic başlangıçta kuruldu, bir daha değişmedi.

**Not 5 — OPC UA + MQTT Birlikte Çalışmasının Değeri**
Bir projede SCADA ile OPC UA, analitik ile MQTT. İlk başta "çift entegrasyon — gereksiz?" diye soruldu. 3 ay sonra SCADA değişti: MQTT pipeline etkilenmedi. Sonra MQTT analitik platformu değişti: OPC UA SCADA bağlantısı etkilenmedi. Gevşek bağlantının gerçek değeri ancak değişim anında görüldü.

**Not 6 — Sparkplug B'nin Entegrasyon Süresine Etkisi**
Ham MQTT ile bir PLC entegrasyonu: Topic yapısını anla, payload formatını çöz, birimleri belgele, InfluxDB tag'lerini tanımla, Grafana konfigure et → 2-3 gün. Sparkplug B ile: NBIRTH mesajındaki metadata her şeyi anlatıyor, Ignition otomatik tag yapısı oluşturuyor → 2-3 saat. 10 PLC'de fark = yaklaşık 3 hafta.

## İlgili Konular

```
knowledge/protocols/mqtt/            ← Şu an buradasınız
├── 01_basics.md
├── 02_industrial_usage.md
└── _synthesis.md (bu belge)

Sonraki adım — CODESYS implementasyonu:
knowledge/codesys/networking/
└── 04_mqtt_client.md                → CODESYS'te MQTT client kurulumu

Sonraki adım — OPC UA ile birlikte kullanım:
knowledge/protocols/opc-ua/
├── 01_architecture.md               → OPC UA + MQTT katmanlı mimari
└── 04_subscriptions.md              → OPC UA PubSub vs MQTT karşılaştırması

Diğer protokoller:
knowledge/protocols/
├── modbus-tcp/                      → Eski sistemler, basit 2-cihaz
└── opc-ua/                          → Cihaz-SCADA katmanı

Araçlar:
  MQTT Explorer     → GUI MQTT browser ve test
  MQTTX             → Masaüstü ve CLI test istemcisi
  mosquitto_pub/sub → CLI hızlı test
  paho-mqtt         → Python kütüphanesi
  Node-RED          → Görsel MQTT akış entegrasyonu
  InfluxDB + Grafana → Zaman serisi + dashboard pipeline
  Sparkplug B spec  → https://www.eclipse.org/tahu/sparkplug/
```
