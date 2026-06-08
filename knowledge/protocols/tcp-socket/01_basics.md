---
KONU        : TCP Socket Temelleri
KATEGORİ    : protocols
ALT_KATEGORI: tcp-socket
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://medium.com/@harshithgowdakt/deep-dive-into-tcp-sockets-how-data-travels-under-the-hood-7c16f6b2bf95"
    başlık: "Medium — Deep Dive into TCP Sockets: How Data Travels Under the Hood"
    güvenilirlik: topluluk
  - url: "https://www.codeproject.com/Articles/37496/TCP-IP-Protocol-Design-Message-Framing"
    başlık: "CodeProject — TCP/IP Protocol Design: Message Framing"
    güvenilirlik: topluluk
  - url: "https://blog.cloudflare.com/when-tcp-sockets-refuse-to-die/"
    başlık: "Cloudflare Blog — When TCP Sockets Refuse to Die"
    güvenilirlik: topluluk
  - url: "https://man7.org/linux/man-pages/man7/tcp.7.html"
    başlık: "Linux man7 — tcp(7) — Transmission Control Protocol"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "02_codesys_implementation.md"
    ilişki: detaylandırır
  - konu: "03_custom_protocol_design.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/networking/03_tcp_socket.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/modbus-tcp/01_protocol_basics.md"
    ilişki: alternatif
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: alternatif
ÖNKOŞUL     :
  - "OSI modeli ve TCP/IP temel kavramları"
  - "IP adresi, port, client-server mimarisi"
ÇELİŞKİLER :
  - kaynak: "TCP = güvenilir ama yavaş, UDP = hızlı ama güvenilmez algısı"
    konu: "Endüstriyel otomasyon için LAN içi TCP gecikme kaygısı genellikle abartılıdır"
    çözüm: >
      Fabrika LAN'ında TCP round-trip: <1ms. Bağlantı kurulumu (SYN-SYN/ACK-ACK):
      tek seferlik. Kalıcı bağlantı kurulduktan sonra overhead minimal.
      TCP'nin "yavaş" olduğu senaryo: Her mesaj için yeni bağlantı kuruluyorsa.
      Çözüm: Kalıcı bağlantı (persistent connection) — bir kez bağlan, sürekli kullan.
  - kaynak: "TCP ham stream = mesaj sınırı yok algısı"
    konu: "TCP bir byte stream'dir; gönderilen mesaj sınırları korunmaz"
    çözüm: >
      TCP, verinin hepsinin bütünlüklü ulaşmasını garanti eder ama hangi byte'ların
      tek pakette geleceğini garantilemez. Uygulama katmanında mesaj çerçeveleme
      (framing) zorunludur. Bu belgenin temel konusudur.
---

## Özün Ne

TCP Socket, uygulama katmanında herhangi bir protokol uygulamak için kullanılan en temel iletişim mekanizmasıdır. Modbus TCP, OPC UA, MQTT'nin tamamı TCP socket üzerine inşa edilmiştir. Peki OPC UA veya Modbus varken neden ham TCP socket tercih edilir? Cevap şudur: Karşı taraf bu protokollerden hiçbirini konuşmuyorsa. Barkod okuyucu, özel ölçüm cihazı, kamera sistemi, eski SCADA, vision sistemi — bunların çoğu kendi protokolüne sahiptir ve o protokol yalnızca ham TCP socket üzerinde çalışır. Bu belge, TCP socket'ın nasıl çalıştığını ve endüstriyel otomasyonda ne zaman, neden kullanıldığını ele alır.

## Nasıl Çalışır

### TCP Bağlantısı Kurulumu — Üçlü El Sıkışma

```
İstemci (Client)                         Sunucu (Server)
                                          [Dinlemede: port 9000]
    │                                            │
    │──── SYN (Seq=x) ─────────────────────────►│
    │     "Bağlanmak istiyorum"                  │
    │                                            │
    │◄─── SYN-ACK (Seq=y, Ack=x+1) ─────────────│
    │     "Kabul ediyorum, seninle senkronize oluyorum"
    │                                            │
    │──── ACK (Ack=y+1) ────────────────────────►│
    │     "Teşekkür, bağlantı kuruldu"           │
    │                                            │
    │           [BAĞLANTI KURULDU]               │
    │                                            │
    │══════ Veri akışı başlıyor ══════════════════│
    │──── DATA ────────────────────────────────► │
    │◄─── DATA ────────────────────────────────  │
    │                                            │
    [Bağlantı kapatma: FIN → FIN-ACK → ACK → FIN-ACK]
```

Üçlü el sıkışma yalnızca bir kez gerçekleşir. Bağlantı kurulduktan sonra her mesaj için tekrar gerekmez.

### TCP'nin Temel Özellikleri

```
1. Güvenilir teslimat:
   Her segment ACK ile onaylanır. ACK gelmezse yeniden gönderilir.
   Uygulama katmanı kayıp veri için endişelenmez.

2. Sıralı teslimat:
   Paketler ağda farklı yollardan gelebilir ama TCP sırayla teslim eder.
   Segment numaraları (Sequence Number) bunu sağlar.

3. Akış kontrolü:
   Alıcı, göndereni yavaşlatabilir (Window Size mekanizması).
   Tampon dolduğunda gönderici bekler.

4. Stream yönelimli (kritik!):
   TCP bir byte stream'dir, paket tabanlı değil.
   send(100 byte) → recv() 50 byte + 50 byte olarak gelebilir.
   Mesaj sınırları korunmaz → Framing uygulamanın sorumluluğu.
```

### Kalıcı vs Kısa Bağlantı

```
Kısa Bağlantı (Short-lived connection):
  Her veri transferi için:
    SYN → SYN-ACK → ACK (3 paket: ~1-3ms LAN)
    Veri gönder
    FIN → FIN-ACK → ACK (3 paket)
  
  Kullanım: HTTP/1.0, nadir veri transferi
  Dezavantaj: Her seferinde bağlantı kurma maliyeti

Kalıcı Bağlantı (Persistent connection):
  Bir kez bağlan, sürekli kullan.
    SYN → SYN-ACK → ACK (bir kez)
    ─────────── Veri transferi ─────────────
    Mesaj 1 → Yanıt 1
    Mesaj 2 → Yanıt 2
    ...
    Mesaj N → Yanıt N
    FIN → ... (bağlantı kapatılırken)
  
  Kullanım: Veritabanı, OPC UA session, Modbus TCP (çoğu implementasyon)
  Avantaj: Düşük latency, bağlantı overhead'ı bir kez
```

**Endüstriyel otomasyondaki kural:** Periyodik veri alışverişi yapan her sistem kalıcı bağlantı kullanmalıdır. 100ms polling döngüsünde her seferinde bağlantı kurup kapatmak ciddi overhead oluşturur ve PLC gibi kaynak kısıtlı sistemlerde sorun yaratır.

### TCP Keep-Alive

TCP bağlantısı uzun süre veri olmadığında OS tarafından sonlandırılabilir. Keep-alive mekanizması bunu önler:

```
TCP Keep-Alive parametreleri (Linux):
  tcp_keepalive_time  : 7200s (2 saat, varsayılan)
  tcp_keepalive_intvl : 75s   (probe aralığı)
  tcp_keepalive_cnt   : 9     (probe sayısı, yanıt gelmezse)

Toplam ölü bağlantı tespiti:
  7200 + (75 × 9) = 7875 saniye ≈ 2.2 saat!

Endüstriyel uygulama için çok uzun.
Çözüm: SO_KEEPALIVE aç + parametreleri düşür
        veya uygulama katmanında heartbeat paketi gönder.
```

---

### OPC UA / Modbus Varken Neden Ham TCP?

```
OPC UA / Modbus tercih et:
  ✓ Karşı taraf bu protokolü destekliyorsa
  ✓ Standart istemci kütüphanesi mevcutsa
  ✓ Zengin veri modeli / güvenlik gerekiyorsa

Ham TCP Socket tercih et:
  ✗ Karşı taraf kendi protokolünü kullanıyorsa
  ✗ Legacy cihaz → hiçbir standart protokol yok
  ✗ Yüksek hız / düşük overhead kritikse (büyük binary veri)
  ✗ Özel framing / şifreleme / authentication tasarlanacaksa
  ✗ Cihaz yalnızca belirli bir custom protokol konuşuyor
```

### Endüstriyel TCP Socket Kullanım Senaryoları

| Cihaz / Sistem | Protokol | Neden Ham TCP |
|---|---|---|
| Barcode okuyucu | Özel ASCII | Standart protokol yok |
| Vision / kamera sistemi | Üretici özel | GIGE Vision değil, özel iletişim |
| Eski SCADA | Özel binary | 1990'lardan kalma format |
| Ölçüm cihazı | Özel telnet benzeri | Komut-yanıt ASCII |
| Yazıcı/etiket makinesi | ZPL, EPL veya özel | Özel dil |
| Robot kontrolcü | Üretici özel | TCP üzerinden robot komutları |
| Enerji analizörü | Özel binary | Yüksek örnekleme hızı |
| PLC↔PLC (aynı marka) | Üretici özel | FINS, MC, S7 protokolü |
| CNC | Özel ASCII | DNC protokolü |
| Endoscope/kamera | Özel | Görüntü transfer protokolü |

### TCP'nin Avantajları Ham Kullanımda

```
1. Tam kontrol:
   Paket yapısı, timing, akış kontrolü — her şeyi tasarlarsın.

2. Yüksek performans:
   Modbus overhead'ı yok, OPC UA handshake yok.
   Raw binary → minimum byte.

3. Platform bağımsız:
   Her OS, her dil, her cihaz TCP destekler.

4. Esneklik:
   Gerçek zamanlı push bildirimi, binary büyük veri, sıkıştırma — hepsi mümkün.

5. Mevcut altyapı:
   Factory LAN zaten Ethernet/TCP. Ek donanım yok.
```

### TCP'nin Riskleri Ham Kullanımda

```
1. Güvenlik sıfır (varsayılan):
   Kimlik doğrulama yok, şifreleme yok.
   TLS/SSL eklenmezse veri açık metin.

2. Framing sorumluluğu:
   TCP stream = mesaj sınırı yok.
   Yanlış framing → veri karışması, protocol desynch.

3. Bağlantı kopması tespiti:
   TCP bağlantı kesildiğini söylemeyebilir (silent disconnect).
   Uygulama katmanında heartbeat / timeout gerekli.

4. Test ve debug zorluğu:
   Modbus Poll veya UaExpert gibi hazır araç yok.
   Wireshark + custom parser gerekebilir.

5. Dokümantasyon yükü:
   Register haritası yok. Her şey dokümante edilmeli.
```

## Pratikte Nasıl Kullanılır

### Bağlantı Mimarileri

**Senaryo 1: PLC Client, Cihaz Server (En Yaygın)**
```
PLC (TCP Client) ─────────────────► Barcode Okuyucu (TCP Server)
                    bağlantı kur
                    komut gönder
                    yanıt al
```

**Senaryo 2: PLC Server, SCADA Client**
```
PLC (TCP Server) ◄────────────────── SCADA (TCP Client)
                     port dinle, bağlantı kabul et
                     SCADA'nın sorgularına yanıt ver
```

**Senaryo 3: PLC ↔ PLC (peer-to-peer)**
```
PLC-1 (Server) ←─────────────────── PLC-2 (Client)
                  veya her ikisi de client olup farklı portlarda server
```

### Bağlantı Durumu Makinesi

TCP socket programlama her zaman bir durum makinesi (state machine) olarak düşünülmeli:

```
DISCONNECTED
    │ [xEnable = TRUE]
    ▼
CONNECTING
    │ [connect() başarılı]     [Timeout]
    ▼                              │
CONNECTED ──────────────────► DISCONNECTED
    │ [Veri gönder/al]           (yeniden deneme)
    │ [Bağlantı koptu (recv=0 veya hata)]
    ▼
DISCONNECTED (otomatik yeniden bağlanma)
```

### Port Seçimi

```
Endüstriyel TCP için port seçim rehberi:

< 1024 : Sistem portları — kullanma (root yetkisi gerekir)
1024-49151: Kayıtlı portlar
  502  : Modbus TCP (kullanma — çakışır)
  4840 : OPC UA (kullanma — çakışır)
  1883 : MQTT (kullanma — çakışır)
49152-65535: Dinamik/özel portlar — güvenli kullan

Önerilen aralık:
  10000-20000: Özel uygulama portları
  Örnek: 10502 (Modbus değil ama yakın, hatırlaması kolay)
  Örnek: 19000, 19001, 19002 (Farklı cihazlar için)
```

### TCP Keep-Alive Ayarı (Linux/Python)

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Keep-alive aktif
sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

# Boşta 60 saniye sonra probe başlat (varsayılan 2 saat değil)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)

# 10 saniyede bir probe gönder
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)

# 5 probe yanıtsız kalırsa bağlantıyı kes
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

# Toplam: 60 + (10 × 5) = 110 saniye ölü bağlantı tespiti
```

## Örnekler

### Örnek 1: Basit TCP Echo — Kavram Kanıtı

```python
# Sunucu (Terminal 1)
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 9000))
    server.listen(1)
    print("Dinliyor: 9000")
    
    conn, addr = server.accept()
    print(f"Bağlandı: {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:      # Bağlantı kapandı (recv = 0 = EOF)
                break
            conn.sendall(data)  # Echo: geri gönder

# İstemci (Terminal 2)
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(('127.0.0.1', 9000))
    client.sendall(b'Hello PLC!')
    response = client.recv(1024)
    print(f"Yanıt: {response}")  # b'Hello PLC!'
```

### Örnek 2: Barcode Okuyucu Entegrasyonu Senaryosu

```
Cihaz: Datalogic Matrix 300N barcode okuyucu
Protokol: Özel ASCII, TCP Server, port 5005
Format: Her okuma: "!READ <barcode_data>\r\n" string

PLC davranışı:
1. Okuyucuya TCP bağlan (port 5005)
2. Bağlantı kalıcı tut
3. recv() ile gelen her satırı oku
4. "!READ " başlıyorsa barcode verisini çıkar
5. Bağlantı kopunca yeniden bağlan
```

### Örnek 3: OPC UA vs TCP Socket Karar Ağacı

```
Entegre edilecek cihaz var →
    │
    Cihaz Modbus TCP destekliyor?
    ├── Evet → Modbus TCP kullan (02_modbus_slave.md)
    │
    Cihaz OPC UA destekliyor?
    ├── Evet → OPC UA kullan (01_opcua_server.md)
    │
    Cihaz MQTT destekliyor?
    ├── Evet → MQTT kullan (04_mqtt_client.md)
    │
    Cihaz özel TCP protokolü kullanıyor?
    ├── Evet → Ham TCP Socket (bu belge + 03_custom_protocol_design.md)
    │
    Cihaz RS-232/RS-485 seri port kullanıyor?
    └── Evet → SysSock değil, CODESYS SysCom (seri haberleşme) kullan
```

## Sık Yapılan Hatalar

### Hata 1: Her Mesaj İçin Yeni Bağlantı Açmak

```python
# ❌ YANLIŞ — Her 100ms'de connect/disconnect
while True:
    sock = socket.socket(...)
    sock.connect(('cihaz_ip', port))
    sock.sendall(komut)
    yanit = sock.recv(1024)
    sock.close()
    time.sleep(0.1)
# Sorun: SYN-SYN/ACK-ACK her döngüde → cihaz üzerinde bağlantı kuyruğu dolar

# ✅ DOĞRU — Kalıcı bağlantı
sock = socket.socket(...)
sock.connect(('cihaz_ip', port))
while True:
    sock.sendall(komut)
    yanit = sock.recv(1024)
    time.sleep(0.1)
```

### Hata 2: recv() = 0'ı Hata Zannetmek

```python
# ❌ YANLIŞ
data = sock.recv(1024)
if len(data) == 0:
    print("Hata: veri yok")  # Aslında bağlantı düzgün kapandı

# ✅ DOĞRU
data = sock.recv(1024)
if len(data) == 0:
    print("Bağlantı karşı tarafça kapatıldı — yeniden bağlan")
    # Bu normal bir EOF durumu, hata değil
```

### Hata 3: Blocking recv() Tüm Task'ı Dondurmak

CODESYS'te blocking recv() task'ı dondurur. Bu konunun detayı `02_codesys_implementation.md`'de ele alınmıştır. Özet: Non-blocking mode + timeout kullan.

## Gerçek Proje Notları

**Not 1 — Barcode Okuyucu Protokol Keşfi**  
Yeni bir barcode okuyucu entegre edilecekti. Üretici belgesi "TCP server, port 4001" diyordu. Protokol detayı yoktu. Adım 1: Netcat ile bağlandık (`nc IP 4001`). Okuyucu bir şey taradığında terminale string geldi: `<barcode_value>\r\n`. Protokol bu kadar. PLC kodu: Connect → recv loop → `\r\n`'e kadar buffer → barcode string.

**Not 2 — SCADA Köprü Tasarımı**  
Eski bir SCADA sistemi Modbus veya OPC UA desteklemiyordu. Kendi özel binary protokolüne sahipti. Çözüm: CODESYS'te TCP Server açıldı, SCADA bu servera bağlandı, komutları özel protokolde aldı ve yanıtladı. SCADA değiştirilmedi — yalnızca "özel protokol" konuşulan istemci ona göre tasarlandı.

**Not 3 — Keep-Alive'ın Önemi**  
Bir gece mesai olmayan fabrikada, sabah SCADA PLC'ye bağlanamıyordu. Araştırma: Gece boyunca veri gönderilmemiş, NAT gateway 30 dakika sonra session'ı kapsamış. TCP'nin "phantom bağlantı" durumu: PLC tarafında bağlantı "connected" görünüyor ama NAT'ı geçemiyordu. Çözüm: SO_KEEPALIVE ile her 60 saniyede probe. Session artık geceleri de canlı kalıyor.

## İlgili Konular

```
knowledge/protocols/tcp-socket/
├── 02_codesys_implementation.md → SysSock ile CODESYS implementasyonu
└── 03_custom_protocol_design.md → Özel protokol tasarımı

knowledge/codesys/networking/
└── 03_tcp_socket.md             → CODESYS SysSock detaylı rehber

knowledge/protocols/
├── modbus-tcp/01_protocol_basics.md → TCP üzerine kurulu Modbus
└── opc-ua/01_architecture.md        → TCP üzerine kurulu OPC UA

Araçlar:
  Netcat (nc)   → Hızlı TCP test istemcisi/sunucusu
  Wireshark     → TCP stream analizi
  socat         → Gelişmiş socket aracı
  Python socket → Test script yazımı
```
