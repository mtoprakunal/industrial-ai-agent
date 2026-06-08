---
KONU        : OPC-UA Mimari Yapısı
KATEGORİ    : protocols
ALT_KATEGORI: opc-ua
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://opcfoundation.org/about/opc-technologies/opc-ua/"
    başlık: "OPC Foundation — OPC UA Overview"
    güvenilirlik: resmi
  - url: "https://integrationobjects.com/blog/what-is-opc-ua/"
    başlık: "Integration Objects — What is OPC UA? The Complete Guide"
    güvenilirlik: topluluk
  - url: "https://documentation.unified-automation.com/uasdkcpp/1.7.3/html/L2OpcUaFundamentalsOverview.html"
    başlık: "Unified Automation — OPC UA Fundamentals Overview"
    güvenilirlik: topluluk
  - url: "https://www.opc-router.com/what-is-opc-ua/"
    başlık: "OPC Router — What is OPC UA?"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "02_address_space.md"
    ilişki: detaylandırır
  - konu: "03_security.md"
    ilişki: detaylandırır
  - konu: "04_subscriptions.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/networking/01_opcua_server.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Temel ağ kavramları (TCP/IP, port, istemci-sunucu)"
  - "Endüstriyel otomasyon bağlamı (PLC, SCADA, MES kavramları)"
ÇELİŞKİLER :
  - kaynak: "OPC UA vs MQTT — hangisi daha iyi?"
    konu: "İkisi rakip değil tamamlayıcıdır; birbirinin yerine kullanılmamalı"
    çözüm: >
      OPC UA: Yapısal, semantik, güvenli, iki yönlü (okuma + yazma + method).
      MQTT: Hafif, pub/sub, broker tabanlı, IoT/bulut için ideal.
      Doğru mimari: OPC UA cihaz/PLC katmanında, MQTT bulut/broker katmanında.
      OPC UA PubSub, MQTT transport üzerinde de çalışır — iki dünya birleşiyor.
  - kaynak: "IEC 62541 vs OPC UA — aynı mı?"
    konu: "OPC UA ve IEC 62541 aynı standardın farklı adıdır"
    çözüm: >
      OPC UA, OPC Foundation tarafından yayımlanan ticari ad.
      IEC 62541, aynı standardın IEC tarafından kabul edilmiş uluslararası versiyonu.
      Teknik içerik özdeş. Resmi dökümanlarda her ikisi de referans gösterilebilir.
---

## Özün Ne

OPC UA (Open Platform Communications Unified Architecture), endüstriyel sistemlerin birbirleriyle güvenli, platform bağımsız ve anlam taşıyan şekilde iletişim kurmasını sağlayan bir standarttır. 2006'da OPC Foundation tarafından yayımlanmış, IEC 62541 olarak uluslararası standart statüsüne yükselmiştir. Önceki OPC Classic standartlarının (OPC DA, OPC HDA, OPC AE) Windows-bağımlı, COM/DCOM tabanlı mimarisinin yerini almak üzere tasarlanmıştır. Bugün, endüstriyel IoT mimarilerinin fiili standardı haline gelmiştir: PLC'den MES'e, MES'ten buluta kadar tüm katmanlarda kullanılır.

## Nasıl Çalışır

### OPC Classic vs OPC UA

```
OPC Classic (OPC DA, HDA, AE):                OPC UA:
─────────────────────────────────────────────────────────────
Teknoloji: COM/DCOM (Microsoft)                TCP/IP (standart)
Platform : Yalnızca Windows                    Platform bağımsız
Güvenlik : Windows güvenliği (NTLM, Kerberos)  Yerleşik şifreleme + sertifika
Port     : Dinamik DCOM portları (güvenlik duvarı sorunu)  Tek yapılandırılabilir port
Veri modeli: Ayrı spesifikasyonlar            Tek, birleşik model
Semantik: Yalnızca değer (tag + value)         Tam bilgi modeli (tip, anlam, ilişki)
Erişim   : LAN içi (DCOM kısıtı)              WAN, internet, DMZ
```

### Katmanlı Mimari

OPC UA, aşağıdan yukarıya dört ana katmandan oluşur:

```
┌──────────────────────────────────────────────────────────────┐
│                    UYGULAMA KATMANI                          │
│  Bilgi Modeli (Address Space, Node, Reference)               │
│  Servisler (Read, Write, Browse, Subscribe, Call Method)     │
│  Session Yönetimi                                            │
├──────────────────────────────────────────────────────────────┤
│                    GÜVENLİK KATMANI                          │
│  UA Secure Conversation (mesaj imzalama + şifreleme)         │
│  Sertifika yönetimi                                          │
│  Kullanıcı kimlik doğrulama                                  │
├──────────────────────────────────────────────────────────────┤
│                    KODLAMA KATMANI                           │
│  UA Binary (en yaygın, en hızlı)                             │
│  XML                                                         │
│  JSON (PubSub ve web uygulamaları için)                      │
├──────────────────────────────────────────────────────────────┤
│                    TRANSPORT KATMANI                         │
│  UA TCP (opc.tcp://, port 4840 varsayılan)  ← En yaygın     │
│  HTTPS (web servisleri için)                                 │
│  WebSocket (tarayıcı tabanlı istemciler için)                │
│  MQTT / AMQP (PubSub modu için)                             │
└──────────────────────────────────────────────────────────────┘
```

### İstemci-Sunucu Modeli

OPC UA'nın temel iletişim modeli istek-yanıt (request-response) tabanlıdır:

```
OPC UA Client                                    OPC UA Server
(SCADA, MES, Node-RED, Python script)            (CODESYS, Siemens, B&R)
    │                                                 │
    │──── TCP Bağlantısı (opc.tcp://IP:4840) ────────►│
    │                                                 │
    │──── CreateSession (oturum aç) ─────────────────►│
    │◄─── SessionId, AuthToken ───────────────────────│
    │                                                 │
    │──── ActivateSession (kimlik doğrula) ──────────►│
    │◄─── OK ─────────────────────────────────────────│
    │                                                 │
    │──── Browse (adres uzayını gez) ─────────────────►│
    │◄─── NodeList ───────────────────────────────────│
    │                                                 │
    │──── Read (değer oku) ──────────────────────────►│
    │◄─── DataValue (değer + zaman + kalite) ─────────│
    │                                                 │
    │──── Write (değer yaz) ─────────────────────────►│
    │◄─── OK / Hata ──────────────────────────────────│
    │                                                 │
    │──── CreateSubscription (abonelik kur) ─────────►│
    │◄─── SubscriptionId ─────────────────────────────│
    │──── CreateMonitoredItems (değişken izle) ───────►│
    │◄─── Bildirimler (değer değişince) ──────────────│
    │                                                 │
    │──── CloseSession ──────────────────────────────►│
    │──── TCP Bağlantıyı Kapat ──────────────────────►│
```

### Publish/Subscribe Modeli (OPC UA PubSub)

İstemci-sunucu dışında, OPC UA 2017'den itibaren PubSub modelini de destekler. Bu model, broker aracılığıyla çok-noktaya dağıtım için tasarlanmıştır:

```
OPC UA Publisher (PLC/Edge cihaz)
    │ Veri yayınlar (MQTT, AMQP, UDP üzerinden)
    ▼
MQTT Broker / Message Bus
    │ Abone olanlara iletir
    ├──► SCADA Subscriber
    ├──► MES Subscriber
    └──► Bulut Platform Subscriber

Fark (Client-Server vs PubSub):
  Client-Server: Bire bir, request-response, kalıcı bağlantı
  PubSub:        Birden çoğa, event-driven, bağlantısız, ölçeklenebilir
```

### OPC UA Servisleri

OPC UA, aşağıdaki standart servisleri tanımlar:

| Servis Grubu | İçerik |
|---|---|
| Discovery | Sunucu keşfi, endpoint listesi |
| Session | Oturum aç/kapat, kimlik doğrulama |
| Node Management | Node ekle/sil |
| View | Browse, adres uzayında gezinti |
| Query | Filtreli sorgulama |
| Attribute | Read, Write (tek veya toplu) |
| Method | Uzak metot çağrısı |
| MonitoredItem | Değişken/alarm izleme |
| Subscription | Abonelik yönetimi |
| History | Geçmiş veri okuma |
| Events | Alarm ve olay yönetimi |

### Endpoint URL Yapısı

```
opc.tcp://[host]:[port]/[path]

Örnekler:
  opc.tcp://192.168.1.100:4840                 ← Tipik CODESYS
  opc.tcp://plc-machine.local:4840/OPCUA/SimulationServer
  opc.tcp://192.168.1.100:4840/UA/Server

Not:
  4840 = OPC UA'nın IANA kayıtlı standart portu
  4843 = OPC UA over HTTPS portu
  Güvenlik duvarında yalnızca bu port açılır (OPC Classic'in aksine)
```

### OPC UA ve Rakip Protokoller

```
Protokol     | Semantik | Güvenlik | Standart | Yön     | Bağlantı | Kullanım
─────────────────────────────────────────────────────────────────────────────
OPC UA       | ✓ Zengin  | ✓ Yerleşik | IEC 62541 | 2 yönlü | Session  | Endüstriyel
Modbus TCP   | ✗ Düz     | ✗ Yok    | Modicon   | 2 yönlü | Basit    | Legacy, basit
MQTT         | ✗ Düz     | TLS opt  | OASIS     | Pub/Sub | Broker   | IoT, bulut
REST/HTTP    | Uygulama  | TLS      | HTTP      | İstek   | Stateless| Web enteg.
EtherCAT     | ✗ Düz     | ✗ Yok    | IEC 61158 | 2 yönlü | RT       | Motion, I/O
PROFINET     | Orta     | Orta     | IEC 61158 | 2 yönlü | RT       | Siemens ekosist.

OPC UA'nın Güçlü Yönleri:
  ✓ Platform bağımsız (Linux, Windows, ARM, cloud)
  ✓ Yerleşik güvenlik (şifreleme + sertifika + kullanıcı kimlik)
  ✓ Zengin semantik veri modeli (anlam taşıyan tip sistemi)
  ✓ Hem istemci-sunucu hem pub/sub
  ✓ Standart (IEC 62541 + OPC Foundation uyumluluk sertifikasyonu)
  ✓ Tek port (güvenlik duvarı dostu)
  ✓ Companion specifications: robotik, CNC, ilaç, gıda için hazır modeller

OPC UA'nın Zayıf Yönleri:
  ✗ Karmaşıklık: Uygulama ve yapılandırma öğrenme eğrisi
  ✗ Overhead: Modbus TCP'ye kıyasla daha büyük mesajlar
  ✗ Gerçek zamanlılık değil: EtherCAT/PROFINET gibi deterministik değil
  ✗ Kaynak tüketimi: Gömülü/kısıtlı cihazlarda ağır olabilir
```

## Pratikte Nasıl Kullanılır

### Tipik Endüstriyel Mimari

```
ERP / Bulut
    ▲
    │ OPC UA / REST
    │
MES (Üretim Yönetimi)
    ▲
    │ OPC UA
    │
SCADA / Historian
    ▲
    │ OPC UA
    │
OPC UA Server (CODESYS, Siemens, B&R, Beckhoff...)
    ▲
    │ EtherCAT / PROFINET / Modbus RTU
    │
PLC / DCS
    ▲
    │ Kablo
    │
Sensör / Aktüatör
```

### Endpoint Discovery

```python
# Python asyncua ile sunucu keşfi
import asyncio
from asyncua import Client

async def discover():
    # Gateway/discovery server'dan sunucu listesi al
    client = Client("opc.tcp://192.168.1.100:4840")
    servers = await client.connect_and_find_servers()
    for server in servers:
        print(server.ApplicationName, server.DiscoveryUrls)

asyncio.run(discover())
```

### Endpoint Listesi Alma

```python
# Sunucunun desteklediği security policy'leri listele
client = Client("opc.tcp://192.168.1.100:4840")
endpoints = await client.connect_and_get_server_endpoints()
for ep in endpoints:
    print(ep.EndpointUrl)
    print(ep.SecurityMode)       # None / Sign / SignAndEncrypt
    print(ep.SecurityPolicyUri)  # Basic256Sha256 vb.
```

## Örnekler

### Örnek 1: OPC UA'nın Endüstriyel Rolü

```
Senaryo: Otomotiv fabrikası üretim hattı

Katman 1 (Cihaz): 12 CODESYS PLC → her birinde OPC UA Server
Katman 2 (SCADA): Wonderware → her PLC'ye OPC UA Client
Katman 3 (MES)  : SAP ME → SCADA'nın OPC UA serverına bağlanır
Katman 4 (Bulut): Azure IoT Hub → MES'ten MQTT üzerinden veri alır

OPC UA'nın rolü: Katman 1 ile Katman 2 arası + Katman 2 ile Katman 3 arası.
MQTT'nin rolü: Katman 3 ile Katman 4 arası.
```

### Örnek 2: OPC UA Mesaj Boyutu

```
Basit bir REAL değer okuma (Read servisi):
  OPC UA Binary: ~200-400 byte
  Modbus TCP: ~12 byte

Ancak OPC UA Subscription ile sürekli değer değişimi:
  İlk bağlantı: ~600 byte (handshake)
  Sonraki bildirimler: ~50-100 byte/değişken
  → Subscription'da verimi Modbus polling'e yaklaşır
```

## Sık Yapılan Hatalar

### Hata 1: OPC UA'yı Her Şey İçin Kullanmaya Çalışmak

OPC UA, gerçek zamanlı motion control veya yüksek hız I/O için tasarlanmamıştır. Bu katmanlar için EtherCAT, PROFINET veya CANopen kullanılmalı; OPC UA bunların üstündeki izleme/kontrol katmanında yer almalıdır.

### Hata 2: Güvenliği "Sonra Hallederiz" Ertelemek

OPC UA güvenlik altyapısı başlangıçta yapılandırılmazsa, proje büyüdükçe retroaktif güvenlik eklenmesi çok zorlaşır. Sertifika altyapısı ve kullanıcı yönetimi projenin ilk gününde kurulmalıdır.

### Hata 3: OPC Classic'i OPC UA ile Doğrudan Değiştirmeye Çalışmak

OPC Classic → OPC UA geçişi doğrudan 1:1 değildir. OPC Classic tag tabanlı; OPC UA nesne tabanlıdır. Doğru geçiş: Adres uzayını yeniden tasarla, mevcut sisteme OPC UA wrapper/bridge ekle (OPC Foundation'ın ücretsiz OPC UA Wrapper aracı bu işi yapar).

## Gerçek Proje Notları

**Not 1 — OPC UA'nın Güvenlik Duvarı Arkasından Çalışması**  
OPC Classic projelerinde, farklı ağ segmentlerinde SCADA bağlantısı için IT ekibinin DCOM portlarını açması saatler alırdı ve güvenli değildi. OPC UA'ya geçince: `4840` portunu aç, sertifika güven, bitti. IT ekibinin direnci OPC UA sertifikaları ve tek port gereksinimiyle büyük ölçüde azaldı.

**Not 2 — Companion Specification'ın Değeri**  
Bir robot entegrasyonunda, robot OEM'i OPC 40010 (Robotics Companion Spec) uyumlu server sundu. SCADA tarafında da aynı spec'i destekleyen client kullanıldı. Custom tag eşlemesi yapmak yerine standartta tanımlı node'ları direkt kullandık — entegrasyon süresi 2 günden 4 saate indi.

**Not 3 — PubSub ile Ölçekleme**  
50 PLC'nin her birini ayrı OPC UA client/server olarak yönetmek karmaşıktı. OPC UA PubSub (MQTT transport) eklendikten sonra tüm PLC'ler broker'a yayınladı, SCADA tek noktadan abone oldu. 50 farklı bağlantı yerine 1 broker bağlantısı — operasyonel yük dramatik şekilde azaldı.

## İlgili Konular

```
knowledge/protocols/opc-ua/
├── 02_address_space.md          → Bilgi modeli ve node yapısı
├── 03_security.md               → Güvenlik katmanı detayları
├── 04_subscriptions.md          → Abonelik mekanizması
├── 05_codesys_server_config.md  → CODESYS tarafı yapılandırma
└── 06_client_implementations.md → Python, JS, .NET istemcileri

knowledge/codesys/networking/
└── 01_opcua_server.md           → CODESYS OPC UA pratik kurulum

Araçlar:
  UaExpert    → Ücretsiz OPC UA client/browser (Unified Automation)
  Prosys OPC  → Alternatif test istemcisi
  YAAK        → Yet Another OPC UA Kit (açık kaynak)
```
