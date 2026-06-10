---
KONU        : CODESYS Networking — Uzman Sentezi
KATEGORİ    : codesys
ALT_KATEGORI: networking
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/codesys/networking/01_opcua_server.md"
    başlık: "CODESYS OPC UA Sunucu Kurulumu (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/networking/02_modbus_slave.md"
    başlık: "CODESYS Modbus TCP Slave Kurulumu (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/networking/03_tcp_socket.md"
    başlık: "CODESYS SysSock ile TCP Socket Programlama (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/networking/04_mqtt_client.md"
    başlık: "CODESYS MQTT Client Kurulumu (Uzman)"
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
  - konu: "knowledge/codesys/programming/_synthesis.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Dört networking belgesinin Uzman bölümleri okunmuş olmalıdır."
  - "fundamentals/_synthesis (determinizm), task-structure/_synthesis (bloke-I/O), programming/_synthesis (GVL/tek-yazar) kavranmış olmalıdır."
  - "Saha entegrasyon ve devreye alma deneyimi varsayılır."
ÇELİŞKİLER :
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez belgesi yeni çelişki içermez; kaynak belgelere atıflar yapar."
---

## Özün Ne

"CODESYS dış dünyayla nasıl konuşur?" sorusunun dört yanıtı (OPC UA, Modbus, TCP, MQTT) ayrı protokoller gibi görünür; uzman gözüyle bunlar **üç eksende** konumlanan seçimlerdir ve **üç ortak ilkeyle** yönetilir.

**Üç eksen** (protokolü seçtiren):
1. **Zenginlik ↔ Basitlik** — OPC UA (zengin model/tip/method) ↔ Modbus (16-bit register) ↔ TCP (ham byte).
2. **Güvenlik** — OPC UA (AES+sertifika+auth) ↔ MQTT (TLS opsiyonel) ↔ Modbus/TCP (yok).
3. **Push ↔ Poll** — MQTT (proaktif push, broker) ↔ OPC UA (subscription) ↔ Modbus (master poll) ↔ TCP (custom).

**Üç ortak ilke** (hepsini yöneten):
1. **GVL temeli** — dördü de GVL değişkenleri üzerinden çalışır; her birinin erişim biçimi farklı (Symbol Cfg / I/O Mapping / ADR pointer / JSON CONCAT).
2. **Bloke-I/O ayrımı** — ağ çağrıları bloke edebilir (connect, broker bağlantısı); hepsi düşük öncelikli/Freewheeling task'ta kalmalı (task-structure/01).
3. **Raporlama ≠ kontrol** — hiçbiri gerçek zamanlı kontrol katmanı değildir; raporlama/komuta katmanıdır (fundamentals/01 determinizm felsefesi). Gerçek-zaman fieldbus'ın (EtherCAT/PROFINET) işi.

Uzmanlık: protokolü üç eksende doğru konumlamak ve üç ilkeyle sağlam kurmak.

## Nasıl Çalışır

### Dört Protokolün Konumu

```
                    ZENGİNLİK
                       ▲
            OPC UA ●   │  (tip, method, model, history, güvenlik)
                       │
            MQTT   ●   │  (topic/payload, pub-sub, LWT, QoS)
                       │
            Modbus ●   │  (register/coil, poll)
                       │
            TCP    ●   │  (ham byte akışı, framing kendin)
                       └──────────────────────────────► BASİTLİK/KURULUM HIZI

PUSH ◄────────────────────────────────────────────────────────► POLL
MQTT(broker push)   OPC UA(subscription)   TCP(custom)   Modbus(master poll)

GÜVENLİK: OPC UA(AES+sertifika) > MQTT(TLS ops.) >> Modbus/TCP(yok, ağ-seviyesi koru)
```

### Ortak Zemin: GVL + Task + Determinizm Sınırı

```
Protokol    GVL Erişimi              Task Yerleşimi          Bloke Riski
──────────────────────────────────────────────────────────────────────────
OPC UA      Symbol Configuration     runtime (CmpOPCUAServer) düşük (sunucu ayrı)
Modbus      I/O Mapping (bus cycle)  bus cycle task (10-100ms) düşük (poll-yanıt)
TCP Socket  ADR() pointer + MEMCPY   Freewheeling (en düşük)  YÜKSEK (connect blocking)
MQTT        JSON CONCAT              Freewheeling/Slow         YÜKSEK (broker bağlantı)
```

**Uzman içgörüsü:** Bir networking sorununda önce ekseni belirle (yanlış protokol mü seçildi?), sonra ilkeyi kontrol et (GVL tek-yazar mı, task doğru mu, gerçek-zaman mı bekleniyor?). "SCADA değer geç görüyor" → çoğunlukla task cycle / sampling uyumsuzluğu, ağ değil.

### Mental Model: Tek Kontrolcü, Dört Ses

> **OPC UA**: SCADA/MES'e açılan zengin, güvenli, iki yönlü pencere. Symbol Cfg = kod yok. NodeId değişken yoluna bağlı (kırılgan API). Subscription = düşük CPU. Raporlama/komuta, kontrol değil.

> **Modbus TCP**: Evrensel arka kapı. Her HMI anlar. Register haritası + I/O Mapping. Güvenlik yok (ağ-seviyesi koru). 16-bit → REAL için ölçek/iki-register (word tearing dikkat). Poll-only (proaktif gönderemez).

> **TCP Socket**: En alt katman. Standart yetmeyince (barcode, kamera, legacy). Ham byte akışı → framing kendin. Blocking connect + state machine + handle yönetimi → en zor. Standart varsa kullanma.

> **MQTT**: IoT/bulut kanalı. Broker-aracılı pub/sub → decoupling. LWT/retained = broker durum hafızası. QoS = teslimat/overhead ödünleşimi. Kütüphane gerekir (sürüm-kilit). OPC UA ile yan yana çalışır.

## Hızlı Referans

### A. Protokol Karşılaştırması

| Kriter | OPC UA | Modbus TCP | TCP Socket | MQTT |
|---|---|---|---|---|
| Port | 4840 | 502 | özel | 1883 / 8883(TLS) |
| Güvenlik | AES+sertifika+auth | **yok** | uygulama | TLS (ops.) |
| Yön | çift + method | çift (register) | çift (custom) | pub+sub |
| Kurulum | orta | kolay | zor | orta |
| Veri modeli | çok zengin | düşük | sıfır (byte) | orta (topic) |
| Push/Poll | subscription | poll | custom | broker push |
| Çok tüketici | multi-session | multi-master | zor | broker halleder |
| Offline bildirim | yok | yok | yok | **LWT** |
| Gerçek-zaman | yok | yok | yok | yok |
| Kütüphane? | yerleşik | Device Tree | SysSock(yerleşik) | gerekir |

### B. Senaryo → Protokol

| Senaryo | Protokol | Gerekçe |
|---|---|---|
| SCADA/MES okuma + güvenlik | **OPC UA** | zengin, güvenli, subscription |
| Eski/evrensel HMI | **Modbus TCP** | hızlı, evrensel |
| HMI setpoint/durum | **Modbus TCP** | basit register |
| Barcode/kamera/legacy | **TCP Socket** | özel protokol |
| Bulut (AWS/Azure) | **MQTT** | hafif, TLS, cloud-native |
| Node-RED/Grafana | **MQTT** | JSON, native |
| Alarm → bulut | **MQTT QoS1 + idempotency** | guaranteed + dup koruma |
| SCADA + bulut birlikte | **OPC UA + MQTT** | çakışmaz, farklı güç |
| Çok sınırlı kaynak | **Modbus TCP** | en düşük yük |
| Güvenlik zorunlu | **OPC UA** SignAndEncrypt | AES-256 |

### C. Uzman Edge Case Konsolidasyonu

```
PROTOKOL  EDGE CASE                       BELİRTİ                  KORUMA
──────────────────────────────────────────────────────────────────────────────
OPC UA    SP17+ anonymous kapalı          bağlanamıyor             auth veya AllowAnonymous=1
OPC UA    değişken adı = NodeId           ad değişince tag kaybı   isimleri "frozen" say
OPC UA    sembol patlaması                bootapp şişer + açık     sembol setini daralt
OPC UA    sampling < task cycle           kademeli değer            sampling ≥ task cycle
OPC UA    sertifika expire                toptan kopuş             süreyi izle + NTP
Modbus    0 vs 1 tabanlı adres            yanlış register          test değeriyle doğrula
Modbus    HR'ı PLC eziyor                 setpoint kaybolur        HR→GVL tek yön
Modbus    word tearing (DWORD)            Frankenstein değer       tek FC isteğinde oku
Modbus    coil kopunca son değer          fail-safe yok            uygulama watchdog
TCP       1 recv = 1 mesaj varsayımı      yarım/birleşik paket     framing + accumulator
TCP       connect blocking                task donar, watchdog     Freewheeling task
TCP       handle sızıntısı                fd dolar                 her hatada Close
TCP       half-open (kablo koptu)         ölü bağlantı canlı sanılır keepalive/heartbeat
MQTT      aynı Client ID                  bağlan-kop döngüsü       benzersiz ID
MQTT      QoS1 duplikasyon                çift alarm               idempotency (mesaj ID)
MQTT      retained komut                  zombi komut geri gelir   komut retained DEĞİL
MQTT      LWT yok                         dashboard offline diyemez LWT retained 'false'
```

### D. Ortak İlke Kontrolleri

```
GVL tek-yazar    → her register/node/topic'in tek yazarı (programming/02)
Task yerleşimi   → bloke-I/O (TCP connect, MQTT broker) Freewheeling/düşük öncelik
Bus cycle task   → Modbus image'i besleyen kod ile uyumlu task
Güvenlik baştan  → test "None"/anonymous/1883'te kalmasın; üretimden ÖNCE şifrele
Gerçek-zaman?    → hiçbiri kontrol için değil; fieldbus (EtherCAT) ayrı
```

## Pratikte Nasıl Kullanılır

### "Tek PLC, Dört Protokol" Mimarisi (Uzman)

```
Application
├── GVL_IO / GVL_Diagnostics / GVL_Params / GVL_Alarms   (çekirdek, tek-yazar)
├── GVL_Modbus  (WORD/BOOL register değişkenleri)
├── GVL_MQTT    (client FB + payload)
├── Symbol Configuration → OPC UA: yalnız GVL_HMI(yaz)+GVL_Diagnostics(oku), daraltılmış
└── Task Configuration
    ├── Task_Control     (10ms,  Prio:2)  → ana kontrol, GVL_Diagnostics günceller
    ├── Task_Slow        (100ms, Prio:5)  → PRG_ModbusUpdate (bus cycle), PRG_MQTTPublish (timer)
    └── Task_Background  (Freewheel)       → FB_TcpClient, PRG_MQTTManager (bloke-I/O burada)

OPC UA: runtime arka planda örnekler (CmpOPCUAServer); SCADA subscription
Modbus: bus cycle task = Task_Slow; word-tearing'e karşı çok-register tek istekte
TCP   : connect blocking → Freewheeling güvenli; framing + accumulator
MQTT  : Freewheeling bağlantı; QoS1+idempotency; LWT retained; publish timer'lı
```

### Devreye Alma Kontrol Listesi (Uzman)

```
GENEL
□ Protokol üç eksende doğru seçildi (zenginlik/güvenlik/push-poll)
□ Her protokol için ayrı GVL; her veri tek yazarlı
□ Bloke-I/O (TCP/MQTT) Freewheeling/düşük öncelik task'ta
□ Güvenlik üretimden önce açıldı (None/anonymous/1883 değil)

OPC UA
□ SP17+ kullanıcı yönetimi kuruldu · sembol seti daraltıldı (saldırı yüzeyi)
□ Dışa açılan isimler "frozen" · sertifika süresi + NTP izleniyor
□ Subscription sampling ≥ task cycle

MODBUS
□ Register haritası belgelendi + her iki tarafça onaylandı
□ Her register tek yazarlı (HR'ı PLC ezmiyor) · bus cycle task atandı
□ Çok-register değer tek FC isteğinde okunuyor (word tearing) · endian doğrulandı
□ Bağlantı watchdog'u (master poll etmiyorsa fail-safe)

TCP SOCKET
□ Framing + accumulator (1 recv ≠ 1 mesaj) · state machine
□ Freewheeling task · SO_REUSEADDR · her hatada SysSockClose
□ Keepalive/heartbeat (half-open tespiti) · TCP_NODELAY (gerekiyorsa)

MQTT
□ Benzersiz Client ID · LWT retained 'false' · publish timer'lı
□ QoS1 + idempotency (alarm) · komut topic'leri retained DEĞİL
□ Locale ',' → '.' · TLS (internet/bulut) · kütüphane sürümü sabit
```

### Belirti → Eksen/İlke → Kök Neden

```
Belirti                          Eksen/İlke        Kök Neden / Çözüm
─────────────────────────────────────────────────────────────────────
Yanlış protokol seçtim           Eksen             zenginlik/güvenlik/push tekrar değerlendir
SCADA değeri geç görüyor         İlke: task        sampling<cycle veya bus cycle yavaş
Connect/publish sistemi dondurdu İlke: bloke-I/O   Freewheeling task'a taşı
Setpoint kayboluyor              İlke: tek-yazar   HR/node'u PLC eziyor → tek yön
Gerçek-zaman bekledim, olmadı    İlke: determinizm hiçbiri RT değil → fieldbus
Ağdaki herkes PLC'ye erişti      Eksen: güvenlik   Modbus/None → OPC UA veya ağ izolasyonu
DWORD saçma değer                Modbus word tear  tek FC isteğinde oku
Yarım TCP mesajı                 TCP akış          framing + accumulator
MQTT çift alarm                  QoS1 dup          idempotency
Dashboard offline diyemiyor      MQTT LWT          LWT retained 'false'
```

## Sık Yapılan Hatalar

### En Kritik 7 (Dört Protokolden)

1. **OPC UA SP17 anonymous** — güncelleme sonrası toptan kopuş; auth önceden kur.
2. **OPC UA değişken adı değişimi** — NodeId kayar, SCADA tag kaybı; isimleri frozen say.
3. **Modbus register haritası yokluğu** — devreye almada uyuşmazlık; baştan belgele+onayla.
4. **Modbus HR ezme** — PLC setpoint'i eziyor; HR→GVL tek yön.
5. **TCP connect blocking** — ana task donar, watchdog; Freewheeling task.
6. **MQTT Client ID çakışması** — bağlan-kop döngüsü; benzersiz ID.
7. **MQTT LWT eksikliği** — offline tespit edilemez; LWT retained 'false'.

### Uzman Hataları (5) — Sahada İnce

1. **"1 recv = 1 mesaj"** (TCP) — yarım/birleşik paket; framing + accumulator.
2. **Word tearing** (Modbus) — çok-register değer yarım okunur; tek FC isteğinde.
3. **Retained komut** (MQTT) — zombi komut geri gelir; retained yalnız durum için.
4. **QoS1'i exactly-once sanmak** (MQTT) — duplikasyon; idempotency ekle.
5. **OPC UA sembol patlaması** — bootapp şişer + saldırı yüzeyi; sembol setini daralt.

## Ne Zaman Tercih Edilmeli / Edilmemeli

```
OPC UA mı Modbus mu?  → "Karşı taraf OPC UA destekliyor + güvenlik gerekli mi?"
                         Evet → OPC UA · Hayır/sınırlı kaynak → Modbus
TCP Socket?           → SADECE standart (Modbus/OPC UA/MQTT) yetmiyorsa (legacy/özel)
MQTT?                 → bulut/IoT/düşük-bant/event-driven; SCADA için DEĞİL (OPC UA)
İkisi birden?         → OPC UA(fabrika-içi SCADA) + MQTT(fabrika-dışı bulut) yaygın
```

Yetersiz kalınca: gerçek-zaman fieldbus → networking/ethercat · OPC UA model → standards/opcua_overview · güvenlik mimarisi → standards.

## Gerçek Proje Notları

**Sentez Notu 1 — Üç Eksen Seçer, Üç İlke Kurar**  
Protokol seçimi (eksen) ile sağlam kurulum (ilke) ayrı işlerdir. Yanlış eksen = baştan yanlış protokol (Modbus'a güvenlik bekleme); ihlal edilen ilke = doğru protokol kötü kurulum (TCP'yi ana task'ta çalıştırma). Uzman önce ekseni doğru seçer, sonra üç ilkeyle (GVL/task/determinizm) sağlamlaştırır.

**Sentez Notu 2 — Hepsi GVL Üzerinde, Hepsi Bloke Edebilir**  
Dört protokolün ortak iki gerçeği: (1) veri GVL'den akar — protokol-özel GVL'ler (GVL_Modbus, GVL_MQTT) + tek-yazar kuralı karışıklığı önler (programming/02); (2) ağ çağrıları bloke edebilir — TCP connect ve MQTT broker bağlantısı Freewheeling task'ta olmalı (task-structure/01). Bu iki ilke ihlal edilince protokol "çalışıyor görünür ama saha sorunu üretir".

**Sentez Notu 3 — Hiçbiri Gerçek Zamanlı Değil**  
OPC UA, Modbus, TCP, MQTT — dördü de raporlama/komuta katmanıdır, kontrol değil (fundamentals/01: kontrol determinizmi ≠ raporlama). "MQTT ile motor senkronize edeyim" veya "Modbus ile servo kontrol" yanlıştır; gerçek-zaman senkron iş fieldbus'ın (EtherCAT/PROFINET) işidir. Bu sınırı bilmek, ağ protokolünden olmayacak bir performans beklememeyi sağlar.

**Sentez Notu 4 — Güvenlik Baştan, Test Sonrası Değil**  
En tehlikeli desen: "None"/anonymous/port 1883 ile test → unutma → üretim. Modbus'ta hiç güvenlik yok (ağ izolasyonu şart), OPC UA'da None bırakmak PLC'yi açık eder, MQTT'de 1883 açık metin. Güvenlik modu proje başında kararlaştırılmalı; test bittiğinde "kapatmak" yerine üretimden önce "açmak" disiplini kurulmalı (gerçek olay: ağ taraması PLC'ye erişti).

**Sentez Notu 5 — Endüstride Kombinasyon Hakim**  
Tek protokol nadirdir. OPC UA + Modbus (legacy SCADA desteği), OPC UA + MQTT (fabrika-içi kontrol + fabrika-dışı bulut) en yaygın çiftler. Her protokol kendi ekseninde en güçlü olduğu işi yapar; çakışmazlar çünkü farklı task'larda, farklı GVL'lerde, farklı tüketicilere hizmet ederler. Uzman, "tek doğru protokol" aramaz; her veri akışına ekseninde en uygun olanı atar.

## İlgili Konular

```
knowledge/codesys/networking/      ← Şu an buradasınız (Uzman seviye)
├── 01_opcua_server.md       (Uzman)
├── 02_modbus_slave.md       (Uzman)
├── 03_tcp_socket.md         (Uzman)
├── 04_mqtt_client.md        (Uzman)
└── _synthesis.md (bu belge)

Önkoşul:
knowledge/codesys/fundamentals/   → determinizm sınırı, GVL, Device Tree
knowledge/codesys/task-structure/ → bloke-I/O task yerleşimi, watchdog
knowledge/codesys/programming/    → GVL tek-yazar, FB state machine, kütüphane sürüm

Bağlı / sonraki:
knowledge/networking/ethercat/    → gerçek-zaman fieldbus (raporlama değil kontrol)
knowledge/protocols/opc-ua/01_architecture.md → OPC UA Information Model, NodeId
knowledge/codesys/debugging/      → Wireshark, protokol analizi

Araçlar:
  UaExpert · Modbus Poll · pymodbus · Wireshark · MQTT Explorer · Mosquitto · netcat · Node-RED
```
