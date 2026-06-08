---
KONU        : CODESYS Networking — Sentez
KATEGORİ    : codesys
ALT_KATEGORI: networking
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "knowledge/codesys/networking/01_opcua_server.md"
    başlık: "CODESYS OPC UA Sunucu Kurulumu"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/networking/02_modbus_slave.md"
    başlık: "CODESYS Modbus TCP Slave Kurulumu"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/networking/03_tcp_socket.md"
    başlık: "CODESYS SysSock ile TCP Socket Programlama"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/networking/04_mqtt_client.md"
    başlık: "CODESYS MQTT Client Kurulumu"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_opcua_server.md"
    ilişki: detaylandırır
  - konu: "02_modbus_slave.md"
    ilişki: detaylandırır
  - konu: "03_tcp_socket.md"
    ilişki: detaylandırır
  - konu: "04_mqtt_client.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "Bu sentez, dört networking belgesini okuduktan sonra okunmak üzere tasarlanmıştır."
  - "CODESYS proje yapısı ve GVL tasarımı (fundamentals/02_project_structure.md)"
ÇELİŞKİLER :
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez belgesi yeni çelişki içermez; kaynak belgelere atıflar yapar."
---

## Özün Ne

Bu sentez, "CODESYS kontrolcüsü dış dünyayla nasıl konuşur?" sorusuna tek bir bütünsel yanıt verir. Dört belge dört farklı dil konuşur: OPC UA endüstriyel SCADA/MES dünyasını, Modbus köklü ve evrensel HMI/SCADA gerçekliğini, TCP Socket özel protokol dünyasını ve MQTT bulut/IoT ekosistemini temsil eder. Her protokol bir seçenektir; doğru seçim senaryoya bağlıdır. Bu sentez, o seçimi kolaylaştırmak için dört protokolü bütünsel olarak bağlar ve karar tablosunu sunar.

## Nasıl Çalışır

### Dört Protokolün Zihin Haritası

```
┌──────────────────────────────────────────────────────────────────────────┐
│              CODESYS KONTROLCÜ — DIŞ DÜNYAYLA BAĞLANTI HARİTASI         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│                     ┌─────────────────────────┐                          │
│                     │    CODESYS Runtime       │                          │
│                     │    (PLC / SoftPLC)       │                          │
│                     │                          │                          │
│                     │  GVL_IO, GVL_Params,     │                          │
│                     │  GVL_Diagnostics,        │                          │
│                     │  GVL_Alarms              │                          │
│                     └──────────┬───────────────┘                          │
│                                │                                          │
│           ┌────────────────────┼────────────────────┐                    │
│           │                    │                    │                    │
│           ▼                    ▼                    ▼                    │
│   ┌───────────────┐   ┌────────────────┐   ┌───────────────┐            │
│   │  OPC UA       │   │  Modbus TCP    │   │  TCP Socket   │            │
│   │  SERVER       │   │  SLAVE         │   │  (SysSock)    │            │
│   │               │   │                │   │               │            │
│   │  Port: 4840   │   │  Port: 502     │   │  Port: Özel   │            │
│   │  Symbol Cfg   │   │  Device Tree   │   │  SysSockCreate│            │
│   │  Address Space│   │  I/O Mapping   │   │  State Machine│            │
│   │  Şifreli/Auth │   │  Register Harit│   │  Pointer/ADR  │            │
│   └──────┬────────┘   └───────┬────────┘   └───────┬───────┘            │
│          │                    │                    │                    │
│          ▼                    ▼                    ▼                    │
│   SCADA / MES / ERP    Eski SCADA / HMI    Barcode / Kamera             │
│   Bulut (OPC UA)       Evrensel araçlar    Legacy Sistem                │
│   Farklı üretici HMI   Python pymodbus     Özel Protokol                │
│                                                                           │
│           ┌──────────────────────────────────────────┐                   │
│           │               MQTT CLIENT                │                   │
│           │                                          │                   │
│           │  Port: 1883 (şifresiz) / 8883 (TLS)      │                   │
│           │  Broker → Mosquitto / AWS IoT / HiveMQ   │                   │
│           │  Topic: factory/{site}/{line}/{device}/... │                  │
│           │  Publish: Telemetri, Alarm                │                   │
│           │  Subscribe: Komutlar                      │                   │
│           └──────────────────┬───────────────────────┘                   │
│                              │                                            │
│                              ▼                                            │
│               Bulut (AWS / Azure / GCP)                                   │
│               Node-RED / Grafana / InfluxDB                               │
│               Mobil Dashboard                                             │
└──────────────────────────────────────────────────────────────────────────┘
```

### Mental Model: Tek Kontrolcü, Dört Ses

CODESYS'in ağ protokollerini anlamanın en kısa yolu şu dört cümleye sığar:

> **OPC UA**: PLC'nin SCADA/MES dünyasına açtığı zengin, güvenli, iki yönlü penceredir. Yerleşik sunucu, sertifika + kullanıcı kimlik doğrulama, subscription modeli. Kod yazmak gerekmez — Symbol Configuration yeterlidir.

> **Modbus TCP**: PLC'nin evrensel dili konuştuğu arka kapıdır. Her HMI ve SCADA anlar. Sadece register haritası tasarlanır, I/O Mapping ile GVL değişkenlerine bağlanır. Şifreleme yoktur, ama kurmak dakikalar alır.

> **TCP Socket**: PLC'nin ham ağ soketi tuttuğu en alt katmandır. Standart protokolün yetmediği durumlarda — barcode okuyucu, kamera, legacy cihaz — SysSock API ile özel protokol yazılır. Karmaşıktır; blocking/non-blocking farkı, state machine zorunluluğu ve handle yönetimi dikkat gerektirir.

> **MQTT**: PLC'nin IoT/bulut dünyasına gönderdiği hafif, event-driven mesajlaşma kanalıdır. Broker üzerinden; SCADA'lar, cloud platformları, mobil uygulamalar PLC verisini alır. PLC hem yayıncı (publish) hem abone (subscribe) olur. OPC UA ile yan yana çalışabilir.

### Dört Protokolün Ortak Zemini: GVL

Dört protokolde de veri akışının merkezi GVL (Global Variable List) değişkenleridir. Fark; her protokolün bu değişkenlere farklı biçimde erişmesidir:

```
OPC UA    → Symbol Configuration: GVL değişkenlerini Node olarak Address Space'e açar
Modbus    → I/O Mapping:          GVL değişkenlerini Register ofsetlerine bağlar
TCP Socket→ ADR() pointer:        GVL değişkenlerini doğrudan byte buffer'a kopyalar
MQTT      → CONCAT ile JSON:      GVL değişkenlerini string payload içine gömer
```

## Hızlı Referans Tabloları

### A. Protokol Karşılaştırması: Ne Zaman Hangisi

| Kriter | OPC UA | Modbus TCP | TCP Socket | MQTT |
|---|---|---|---|---|
| Port | 4840 | 502 | Özel (ör. 8080) | 1883 / 8883 (TLS) |
| Güvenlik | Sertifika + Kullanıcı + AES-256 | **Yok** | Uygulama katmanına bağlı | TLS (ücretli lib veya IIoT SL) |
| Yön | Çift (okuma + yazma + method) | Çift (register okuma/yazma) | Çift (custom) | Çift (pub + sub) |
| Kurulum zorluğu | Orta | Kolay | Zor | Orta |
| Standart mı? | IEC 62541 | De-facto endüstri std | Hayır (özel) | OASIS MQTT 3.1.1 / 5.0 |
| Kaç bağlantı | Çok (multi-session) | Çok (multi-master) | Tek/Çok (FB karmaşıklığı) | Tüm subscriber'lar (broker üzerinden) |
| Veri modeli zenginliği | Çok yüksek (node, type, method) | Düşük (register/coil) | Sıfır (byte stream) | Orta (topic/payload) |
| CPU / RAM yükü | Yüksek | Düşük | Düşük | Düşük-Orta |
| Gerçek zamanlılık | Yok (soft RT) | Yok (polling) | Yok (TCP) | Yok (broker gecikmesi) |
| Tercih ortamı | Fabrika otomasyonu | Eski/evrensel sistemler | Özel cihaz entegrasyonu | Bulut / IoT / Analytics |

### B. Senaryo → Protokol Karar Tablosu

| Senaryo | Önerilen Protokol | Gerekçe |
|---|---|---|
| SCADA sistemi PLC verisi okuyor | **OPC UA** | Güvenli, zengin veri modeli, subscription |
| MES üretim takibi yapıyor | **OPC UA** | Metadata, tip bilgisi, method çağrısı |
| Eski SCADA yalnızca Modbus biliyor | **Modbus TCP** | Hızlı entegrasyon, evrensel destek |
| HMI setpoint yazıyor / durum okuyor | **Modbus TCP** | Basit register haritası yeterli |
| Barcode okuyucu TCP server çalıştırıyor | **TCP Socket** | Özel protokol, SysSock client |
| Kamera sistemi özel mesaj gönderiyor | **TCP Socket** | Framing + özel parse gerekiyor |
| Bulut platformuna (AWS/Azure) veri gönderme | **MQTT** | Hafif, TLS, cloud-native |
| Node-RED / Grafana dashboard | **MQTT** | Native entegrasyon, JSON payload |
| Alarm bildirimi buluta | **MQTT QoS 1** | Guaranteed delivery, event-driven |
| PLC'den hem SCADA hem bulut | **OPC UA + MQTT** | İkisi çakışmaz; farklı güçler |
| Çok sınırlı CPU/RAM | **Modbus TCP** | En düşük protokol yükü |
| Güvenlik zorunlu, şifre zorunlu | **OPC UA** (SignAndEncrypt) | AES-256, sertifika, kullanıcı yönetimi |
| 4G/LTE üzerinden bağlantı | **MQTT** | Düşük bant genişliği tüketimi |

### C. Teknik Özellikler Özeti

| Özellik | OPC UA | Modbus TCP | TCP Socket | MQTT |
|---|---|---|---|---|
| Ek kütüphane gerekir mi? | Hayır (yerleşik) | Hayır (Device Tree) | SysSock (yerleşik) | Evet (IIoT SL veya topluluk) |
| Kod yazmak gerekir mi? | Hayır (Symbol Cfg) | Hayır (I/O Mapping + PRG) | Evet (FB + state machine) | Evet (FB çağrısı + JSON) |
| Değişken tipi kısıtı | Yok | 16-bit WORD / 1-bit BOOL | Yok (byte dizisi) | Yok (string payload) |
| REAL değer gönderme | Doğrudan (Float node) | İki WORD + ölçeklendirme | Doğrudan (IEEE 754) | String + locale dikkat |
| Çok istemci | Evet (MaxSessions=10+) | Evet (paralel master) | Zor (multi-client FB) | Evet (broker halleder) |
| Tarihsel veri (history) | Evet (Historizing) | Hayır | Hayır | Hayır (InfluxDB ile dış) |
| PLC offline bildirimi | Yok | Yok | Yok | Evet (Last Will & Testament) |

### D. Hata Noktaları Özeti (Dört Belgeden Konsolide)

| Protokol | En Kritik Hata | Çözüm |
|---|---|---|
| OPC UA | SP17+ anonymous erişim kapandı | CODESYSControl.cfg → AllowAnonymous=1 veya kullanıcı yönetimi |
| OPC UA | Değişken adı değişince tüm SCADA bağlantısı kesilebilir | Dışa açılan değişken isimlerini "frozen" kabul et |
| Modbus | 0-tabanlı vs 1-tabanlı adres | Test değeriyle doğrula, register haritasında belirt |
| Modbus | Holding Register'a yazılan değer PLC kodunca eziliyor | HR → GVL akışı tek yönlü; PLC asla HR'ı ezmemeli |
| TCP Socket | SysSockConnect blocking — task donuyor | Client FB'yi Freewheeling/düşük öncelikli task'a taşı |
| TCP Socket | Socket handle sızdırma | Her hata dalında SysSockClose çağır |
| TCP Socket | SysSockRecv = 0 ve -1 aynı ele alınırsa | 0 = bağlantı kapandı, -1 = veri yok (non-blocking normal) |
| MQTT | Aynı Client ID → sürekli bağlantı kopmasi | Her PLC instance benzersiz Client ID |
| MQTT | Her scan döngüsünde publish → broker flood | Timer ile sınırla (ör. T#5S) |
| MQTT | Last Will eksikliği → dashboard offline gösteremiyor | LWT: topic=status/online, payload='false', retain=TRUE |

## Pratikte Nasıl Kullanılır

### "Tek PLC, Dört Protokol" Mimarisi

Gerçek bir üretim hattında dört protokolün tamamı aynı anda etkin olabilir. Aşağıdaki örnek bu mimarinin nasıl inşa edildiğini gösterir:

```
Application
├── GVL_IO          ← Fiziksel I/O adresleri (%I, %Q)
├── GVL_Diagnostics ← Hesaplanmış proses değerleri
├── GVL_Params      ← Setpoint ve parametreler
├── GVL_Alarms      ← Aktif alarmlar
├── GVL_Modbus      ← Modbus register değişkenleri (WORD, BOOL)
├── GVL_MQTT        ← MQTT client FB ve payload değişkenleri
│
├── Symbol Configuration    ← OPC UA: GVL_IO + GVL_Diagnostics dışa açık
│
├── Task Configuration
│   ├── Task_Control  (10ms, Prio:2)  → PLC_PRG (ana kontrol)
│   ├── Task_Slow    (100ms, Prio:5)  → PRG_ModbusUpdate, PRG_MQTTPublish
│   └── Task_Background (Freewheeling) → PRG_TcpClient, PRG_MQTTManager
│
└── Device Tree
    └── Ethernet
        └── ModbusTCP Slave Device  ← Port 502
            I/O Mapping → GVL_Modbus.*
```

**Çalışma mantığı:**

```
Task_Control (10ms):
  → PLC ana mantığı çalışır
  → GVL_Diagnostics, GVL_Alarms güncellenir

Task_Slow (100ms):
  → PRG_ModbusUpdate: GVL_Diagnostics → GVL_Modbus (dönüşüm + maskeleme)
  → PRG_MQTTPublish : Timer dolunca JSON payload → MQTT broker

Task_Background (Freewheeling):
  → PRG_MQTTManager: MQTT bağlantı yönetimi + subscribe
  → FB_TcpClient   : Barcode okuyucuya bağlantı (blocking connect burada güvenli)

OPC UA (Arka planda — runtime tarafından):
  → Symbol Configuration değişkenleri her task cycle'ında otomatik güncellenir
  → SCADA subscription ile dilediği değişkeni izler
```

### Proje Başlangıç Kontrol Listesi

```
□ 1. Hangi protokol(ler) gerekiyor? → Senaryo/karar tablosuna bak
□ 2. OPC UA gerekiyorsa:
     → Runtime SP17+ mı? → Kullanıcı yönetimi kur
     → Symbol Configuration ekle, değişkenleri işaretle
     → Build + Download → UaExpert ile test
□ 3. Modbus gerekiyorsa:
     → Register haritasını belgele (SCADA ekibiyle onaylat)
     → ModbusTCP Slave Device ekle → I/O Mapping
     → GVL_Modbus tasarla → PRG_ModbusUpdate yaz
     → pymodbus ile test
□ 4. TCP Socket gerekiyorsa:
     → Karşı tarafın protokolünü belgele (framing, terminatör)
     → FB_TcpClient veya FB_TcpServer yaz (state machine)
     → Freewheeling task'a taşı
     → SO_REUSEADDR eklendi mi? netcat ile test
□ 5. MQTT gerekiyorsa:
     → Kütüphane seç (Resmi IIoT SL / stefandreyer / rossmann)
     → Broker kur (Mosquitto test için)
     → Topic şeması belgele
     → Client ID benzersiz mi? LWT yapılandırıldı mı?
     → MQTT Explorer ile topic'leri izle
□ 6. Task atamaları yapıldı mı?
     → Modbus: Bus Cycle Task atandı mı?
     → TCP Client: Freewheeling task'ta mı?
     → MQTT Publish: Timer var mı (her döngüde değil)?
```

## Sık Yapılan Hatalar

### En Kritik 7 Hata (Dört Protokolden Özet)

**1. OPC UA — SP17 Geçişinde Üretim Durması**
Runtime güncellendi, anonymous erişim kapandı, tüm SCADA bağlantısı kesildi. Ders: Runtime güncellemesi öncesi release notes okunmalı; kullanıcı yönetimi önceden kurulmalı.

**2. OPC UA — Değişken Adı Değişikliği**
`GVL_IO.xMotorRun` → `xMotor1_Run` yapıldığında NodeId değişti, SCADA 200 tag kaybetti. Ders: OPC UA'ya açılan değişken adları "frozen" sayılmalı; yeniden adlandırma SCADA güncellemesiyle eş zamanlı yapılmalı.

**3. Modbus — Register Haritası Olmadan Devreye Alma**
PLC ekibi ile SCADA ekibi ayrı çalıştı, devreye alma günü register beklentileri uyuşmadı. 2 günlük kayıp. Ders: Register haritası proje başında tek sayfalık tablo olarak hazırlanmalı, her iki tarafın onayına sunulmalı.

**4. Modbus — Holding Register Ezme**
Kontrol kodu her döngüde HR'ı varsayılan değere yazdı; SCADA'nın yazdığı setpoint bir döngü sonra kayboldu. Ders: HR → GVL_Params akışı tek yönlü olmalı; PLC kodu HR'ı asla ezmemeli.

**5. TCP Socket — SysSockConnect Task'ı Dondurdu**
Yüksek öncelikli task (10ms, Prio:2) içinde SysSockConnect çağrıldı. Hedef IP erişilemezdi; OS 75 saniye bekledi, watchdog tüm sistemi durdurdu. Ders: TCP client mutlaka Freewheeling veya düşük öncelikli task içinde çalışmalı.

**6. MQTT — Client ID Çakışması**
İki hat aynı Client ID kullandı; bağlantı her 30 saniyede koptu. Ders: Client ID proje genelinde benzersiz olmalı — ör. `PLC_ + MakinAdi + SerialNo`.

**7. MQTT — Last Will Eksikliği**
PLC ağ bağlantısı kesildiğinde Grafana dashboard "Online: true" göstermeye devam etti. Ders: Her MQTT client bağlantısında LWT yapılandırılmalı; retained mesaj + 'false' payload standardı olmalı.

## Ne Zaman ...

### Ne Zaman OPC UA, Ne Zaman Modbus?

OPC UA ve Modbus TCP en sık karıştırılan çift. Karar vermek için bir soru yeterlidir: **"Karşı taraf OPC UA destekliyor mu?"**

```
Destekliyorsa → OPC UA seç: Daha güvenli, daha zengin, subscription modeli
Desteklemiyorsa → Modbus TCP: Evrensel, hızlı, karmaşıksız

Ek karar faktörleri:
  Güvenlik zorunlu mu?          → OPC UA (Modbus'ta şifreleme yok)
  1000+ değişken mi?            → OPC UA (Modbus register haritası yönetilmez hale gelir)
  Hızlı entegrasyon mü?         → Modbus (kurulum ve test saatler alır, OPC UA günler)
  Metadata/type bilgisi gerekli? → OPC UA
  Eski sistem, sınırlı kaynak?  → Modbus
```

### Ne Zaman TCP Socket?

```
Sadece şu durumlarda TCP Socket'e başvur:
  ✓ Karşı taraf Modbus, OPC UA veya MQTT değil
  ✓ Özel framing ve parse gerekiyor
  ✓ Donanım üreticisi "TCP string protokolü" sunuyor
  ✗ Standart protokol seçeneği var → Kullan! (TCP socket bakımı ağır)
  ✗ Multi-client server lazım → OPC UA çok daha kolay
```

### Ne Zaman MQTT?

```
MQTT ideal seçimdir:
  ✓ Bulut platformuna veri akışı (AWS IoT, Azure IoT Hub)
  ✓ Grafana / InfluxDB / Node-RED entegrasyonu
  ✓ Düşük bant genişliği (4G/LTE bağlantısı)
  ✓ Event-driven alarm bildirimi
  ✓ Çok sayıda subscriber (broker ölçeklenir)

MQTT tercih etme:
  ✗ Karşı taraf SCADA → OPC UA veya Modbus yeterli
  ✗ Ağ güvenilmez ve QoS 1 yetmiyorsa → Uygulama katmanı retry mekanizması gerekir
  ✗ Gerçek zamanlı kontrol sinyali → MQTT gecikme garantisi vermez
```

### Ne Zaman İkisini Birden Kullan?

```
OPC UA + MQTT kombinasyonu giderek yaygınlaşıyor:
  OPC UA → Fabrika içi SCADA iletişimi (güvenli, iki yönlü, zengin)
  MQTT   → Fabrika dışı bulut veri akışı (hafif, IoT-native)

İki protokol çakışmaz; farklı task'larda, farklı GVL'leri kullanır.
```

## Gerçek Proje Notları

**Sentez Notu 1 — "Hangi Protokolü Seçeyim?" Anksiyetesi**
Yeni projelerde en çok zaman harcanan karar bu. Pratik öneri: Karşı sistemin ne desteklediğinden başla. SCADA Modbus biliyor mu? Modbus kur — OPC UA için haftalarca plan yapma. Bulut bağlantısı lazım mı? MQTT ekle. Her protokol bağımsız çalışır; birini seçmek diğerini kapsamaz.

**Sentez Notu 2 — Task Mimarisi Networking'in Çatısı**
Dört protokolde de task ataması kritik. Genel kural:
- Ana kontrol kodu → Task_Control (10ms, Prio:2)
- Modbus update + MQTT publish → Task_Slow (100ms, Prio:5)
- TCP client, MQTT connection manager → Task_Background (Freewheeling)

Bu ayrım yapılmazsa blocking çağrılar (SysSockConnect) veya aşırı protokol yükü (MQTT her 10ms) ana kontrolü bozar.

**Sentez Notu 3 — GVL Tasarımı Networking'in Temeli**
Tüm protokoller GVL değişkenleri üzerinden çalışır. `GVL_Modbus`, `GVL_MQTT` gibi protokol özelinde GVL'ler oluşturmak karışıklığı önler. OPC UA için dışa açılacak değişkenler "frozen" sayılmalı — isim değişikliği tüm SCADA bağlantılarını bozabilir.

**Sentez Notu 4 — Güvenlik Sonradan Değil Baştan**
OPC UA'da güvenlik politikası "None" ile test yapılıp unutulursa, ağ taraması yapan araçlar PLC'ye erişebilir (gerçek olay). MQTT'da TLS olmadan internet üzerinden gönderilen veri açık metin. Proje başlangıcında şifreleme modunu belirle; test bittikten sonra kapamak yerine üretimden önce aç.

**Sentez Notu 5 — Dört Protokolün Endüstride Gerçek Ağırlıkları**
Deneyimde gözlemlenen dağılım:
- OPC UA: Büyük/orta fabrikalar, SCADA/MES entegrasyonu, yeni projeler
- Modbus TCP: Her ölçekten fabrika, özellikle eski SCADA altyapısı olan yerler
- TCP Socket: Özel cihaz entegrasyonu (barcode, kamera, ölçüm) — sınırlı ama zorunlu
- MQTT: IoT projeleri, bulut entegrasyonu, yeni nesil Endüstri 4.0 uygulamaları

Gerçek dünyada tek protokolden çok kombinasyon hakimdir: OPC UA + Modbus legacy destek için, OPC UA + MQTT bulut için.

## İlgili Konular

```
knowledge/codesys/networking/      ← Şu an buradasınız
├── 01_opcua_server.md             ← OPC UA detay: Symbol Cfg, sertifika, SP17+
├── 02_modbus_slave.md             ← Modbus detay: Register haritası, FC, I/O Mapping
├── 03_tcp_socket.md               ← TCP Socket: SysSock API, state machine, blocking
├── 04_mqtt_client.md              ← MQTT: Kütüphane seçimi, topic tasarımı, LWT
└── _synthesis.md (bu belge)

Ön koşullar:
knowledge/codesys/fundamentals/
├── 02_project_structure.md        ← Device Tree, GVL, Task yapısı
└── _synthesis.md                  ← Runtime, proje, diller

Bağlı konular:
knowledge/codesys/programming/
├── 02_gvl_design.md               ← Networking GVL tasarımı
└── 03_function_blocks.md          ← TCP Socket FB tasarımı

knowledge/standards/
└── opcua_overview.md              ← OPC UA Information Model, NodeId

Araçlar (tüm protokoller için):
  UaExpert      → OPC UA test ve debug
  Modbus Poll   → Modbus Master test aracı
  pymodbus      → Python Modbus test scripting
  Wireshark     → TCP / Modbus / OPC UA paket analizi
  MQTT Explorer → MQTT topic görselleştirme
  Mosquitto     → Yerel MQTT broker
  netcat (nc)   → Hızlı TCP socket test
  Node-RED      → MQTT + OPC UA + Modbus bridge ve dashboard
```
