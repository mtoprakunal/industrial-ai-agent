---
KONU        : Modbus TCP Protokol Temelleri
KATEGORİ    : protocols
ALT_KATEGORI: modbus-tcp
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://flowfuse.com/blog/2026/02/modbus-tcp-vs-modbus-rtu/"
    başlık: "FlowFuse — Modbus TCP vs Modbus RTU: Reliability, Latency, and Failure Modes"
    güvenilirlik: topluluk
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/modbus-tcpip-vs-modbus-rtu-key-differences-and-programming"
    başlık: "Industrial Monitor Direct — Modbus TCP/IP vs Modbus RTU"
    güvenilirlik: topluluk
  - url: "https://www.wevolver.com/article/modbus-rtu-vs-tcp"
    başlık: "Wevolver — Modbus RTU vs TCP: A Comprehensive Comparison"
    güvenilirlik: topluluk
  - url: "https://www.csimn.com/CSI_pages/Modbus101.html"
    başlık: "Control Solutions — Modbus Tutorial"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "02_register_model.md"
    ilişki: tamamlar
  - konu: "03_function_codes.md"
    ilişki: tamamlar
  - konu: "04_codesys_slave_config.md"
    ilişki: kullanır
  - konu: "knowledge/codesys/networking/02_modbus_slave.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Temel ağ kavramları (IP, TCP, port)"
  - "Master-slave iletişim modeli kavramı"
ÇELİŞKİLER :
  - kaynak: "Modbus TCP vs Modbus RTU over TCP — iki farklı şey"
    konu: "İkisi çoğunlukla birbirinin yerine kullanılıyor ama teknik olarak farklı"
    çözüm: >
      Modbus TCP: MBAP header kullanır, CRC yoktur. Gerçek Modbus TCP standardıdır.
      Modbus RTU over TCP: Ham RTU frame'i (CRC dahil) TCP üzerinden gönderir.
      Pek çok legacy cihaz RTU over TCP kullanır; standart Modbus TCP istemcileriyle
      uyumlu değildir. Cihaz belgesi her zaman hangi varyantın kullanıldığını kontrol edilmelidir.
  - kaynak: "Modbus TCP güvenliği — Modbus/TCP Security (port 802)"
    konu: "TLS destekli güvenli Modbus, 2018'den beri standart ama çok az kullanılıyor"
    çözüm: >
      Modbus Organization 2018'de TLS tabanlı güvenli Modbus spesifikasyonu yayımladı.
      Port 802 kullanır. Ancak 2026 itibarıyla çok az cihaz/araç destekler.
      Pratik güvenlik: Ağ segmentasyonu, VPN, güvenlik duvarı ile izolasyon.
---

## Özün Ne

Modbus, 1979'da Modicon tarafından geliştirilen ve bugün hâlâ dünyanın en yaygın endüstriyel iletişim protokolüdür. 47 yıllık yaşıyla milyonlarca kurulumda, binlerce farklı cihaz markasında çalışmaktadır. Modbus TCP, klasik seri Modbus (RTU/ASCII) protokolünün Ethernet/TCP-IP üzerine taşınmış versiyonudur. Güvenlik mekanizması, zengin veri tipi desteği veya otomatik keşif gibi modern özelliklerden yoksundur; ancak basitliği, evrensel uyumluluğu ve lisanssız açık yapısı onu vazgeçilmez kılmaktadır.

## Nasıl Çalışır

### Tarihsel Bağlam

```
1979: Modicon, PLC'leri birbirine bağlamak için Modbus protokolünü geliştirdi.
      RS-232 seri hat, master-slave modeli, basit register modeli.
      
1990'lar: Modbus RTU yaygınlaştı; RS-485 ile 1.2km'ye kadar, 247 cihaza kadar.

1999: Modbus TCP yayımlandı — aynı protokol, Ethernet/TCP-IP üzerine taşındı.

2004: Modbus Organization kuruldu, protokol tamamen açık ve ücretsiz hale geldi.

2018: Modbus/TCP Security (TLS) spesifikasyonu yayımlandı.

2026: Hâlâ dünyanın en yaygın endüstriyel protokolü.
      Sektörün "kilidi açık makas" atasözü bu protokol için geçerli.
```

### Master-Slave (Client-Server) Mimarisi

Modbus TCP'de her iletişim istemcinin (master) başlattığı bir istek-yanıt döngüsüdür. Sunucu (slave) hiçbir zaman kendiliğinden veri göndermez.

```
Master (İstemci)                              Slave (Sunucu)
SCADA / HMI / Python Script                  PLC / Sensör / VFD
    │                                             │
    │──── TCP Connect (port 502) ────────────────►│
    │                                             │
    │──── Request: FC03, reg 0, count 10 ────────►│
    │◄─── Response: [100, 200, 300, ...] ─────────│
    │                                             │
    │──── Request: FC06, reg 5, value 500 ────────►│
    │◄─── Response: OK ───────────────────────────│
    │                                             │
    │──── TCP Disconnect ─────────────────────────►│
```

**Temel kurallar:**
- Yalnızca master istek başlatır
- Her istek için bir yanıt beklenir; sonraki istek yanıt gelmeden gönderilmez (senkron)
- Birden fazla master aynı slave'e bağlanabilir (Modbus TCP'de) ama her istek yine senkron

### Modbus RTU vs Modbus TCP — Temel Farklar

```
Özellik              Modbus RTU              Modbus TCP
─────────────────────────────────────────────────────────────────
Fiziksel katman      RS-232, RS-485, RS-422  Ethernet (Cat5/6, Fiber)
Transport            Seri hat (async)         TCP/IP (connection-oriented)
Hız                  9600-115200 bps          10/100/1000 Mbps
Mesafe               RS-485: ~1200m          100m/segment (switch ile sınırsız)
Cihaz adresi        Slave ID (1-247)         IP adresi + Unit ID
Hata kontrolü        CRC-16 (frame içinde)   TCP kendisi halleder (CRC yok)
Çerçeve sınırı       3.5 karakter sessizliği  MBAP header Length alanı
Bağlantı tipi        Connectionless (seri)   Connection-oriented (TCP)
Multi-master         Hayır (seri paylaşım)   Evet (birden fazla TCP bağlantısı)
Port                 —                        502 (standart)
```

### Modbus TCP Frame Yapısı

```
┌─────────────────────────────────────────────────────────┐
│                  MODBUS TCP FRAME                        │
├──────────┬──────────┬──────────┬──────────┬─────────────┤
│ Trans.ID │ Proto.ID │  Length  │ Unit ID  │  PDU        │
│ 2 byte   │ 2 byte   │ 2 byte   │ 1 byte   │ N byte      │
├──────────┴──────────┴──────────┴──────────┤             │
│     MBAP Header (7 byte toplam)           │             │
└───────────────────────────────────────────┴─────────────┘

MBAP = Modbus Application Protocol Header

Transaction ID: Her istek için artan numara (0x0001, 0x0002...)
                → Eşleşen yanıtı bulmak için kullanılır
                → Çoklu eş zamanlı istek için kritik

Protocol ID   : Her zaman 0x0000 (Modbus protokol için rezerve)

Length        : Unit ID + PDU'nun toplam byte uzunluğu

Unit ID       : Slave adresi (1-247, çoğunlukla 1 veya 255)
                → Gateway arkasındaki cihazları ayırt etmek için
                → Direkt TCP bağlantısında genellikle 1 veya 0xFF

PDU           : Asıl Modbus mesajı = Function Code + Data
```

**İstek frame örneği (FC03, 10 register oku):**
```
Hex: 00 01 00 00 00 06 01 03 00 00 00 0A

Parçalama:
  00 01 = Transaction ID: 1
  00 00 = Protocol ID: Modbus
  00 06 = Length: 6 byte (Unit ID + PDU)
  01    = Unit ID: 1 (slave adresi)
  03    = Function Code: Read Holding Registers
  00 00 = Starting Address: 0 (register 0)
  00 0A = Quantity: 10 (10 register oku)
```

**Yanıt frame örneği:**
```
Hex: 00 01 00 00 00 17 01 03 14 00 64 00 C8 ...

  00 01 = Transaction ID: 1 (eşleşiyor)
  00 00 = Protocol ID: Modbus
  00 17 = Length: 23 byte
  01    = Unit ID: 1
  03    = Function Code: Read Holding Registers
  14    = Byte Count: 20 (10 register × 2 byte)
  00 64 = Register 0: 100 (decimal)
  00 C8 = Register 1: 200 (decimal)
  ...
```

### Modbus RTU vs Modbus RTU over TCP

Dikkat: Bunlar Modbus TCP'den farklıdır.

```
Modbus TCP:
  [MBAP Header (7 byte)][Function Code][Data]
  → CRC YOK → Standart Modbus TCP istemcileri kullanır

Modbus RTU over TCP:
  [Slave Addr][Function Code][Data][CRC-16]
  → Ham RTU frame'i TCP paketine sarılmış
  → MBAP header YOK → Özel gateway/cihazlar için
  → Standart Modbus TCP istemcileriyle UYUMLU DEĞİL
  
Neden önemli: Bazı eski cihazlar ve gatewayler RTU over TCP kullanır.
               Bağlantı kuruluyor ama veri gelmiyor/yanlış geliyorsa
               önce hangi varyantın kullanıldığı kontrol edilmeli.
```

### Neden Hâlâ Bu Kadar Yaygın?

```
1. Açık ve ücretsiz: Lisans yok, royalty yok, standart belgeler web'de
2. Basit: Öğrenmesi kolay, uygulaması kolay
3. Evrensel: PLC, VFD, sensör, enerji sayacı — hemen her şey Modbus destekliyor
4. Olgun: 47 yıllık uygulama deneyimi, kararlı
5. Tek port: Güvenlik duvarı yapılandırması kolay (yalnızca 502)
6. Polling modeli: Deterministik, zaman bütçelenebilir
```

### Modbus TCP Sınırlamaları

```
1. Güvenlik YOK:
   - Kimlik doğrulama yok
   - Şifreleme yok
   - Herhangi bir istemci bağlanıp okuyabilir/yazabilir
   - FrostyGoop malware (2024): Port 502 açık Ukrayna enerji sistemi → fiziksel hasar
   → Çözüm: Ağ segmentasyonu, VPN, güvenlik duvarı

2. Veri tipi kısıtı:
   - Yalnızca 16-bit integer register
   - Float, string, array için özel kodlama gerekli
   - OPC UA'nın zengin semantik modelinin hiçbir eşdeğeri yok

3. Keşif mekanizması yok:
   - Register adresi belgelerden öğrenilmeli
   - Hangi register ne anlama geliyor standart değil — üretici belirliyor

4. Single master (seri Modbus'ta):
   - RTU: Tek master, sıralı sorgulama
   - TCP: Çoklu TCP bağlantısı ama yine de senkron

5. Hız/verimlilik:
   - Her sorgu için bir round-trip (istek + bekleme + yanıt)
   - OPC UA subscription, MQTT pub/sub gibi push modeli yok
   - 500ms döngüyle 100 register = belirgin ağ yükü
```

## Pratikte Nasıl Kullanılır

### Port ve Bağlantı

```bash
# Port 502 açık mı test et
telnet 192.168.1.100 502
# veya
nc -vz 192.168.1.100 502

# Wireshark ile Modbus TCP trafiğini filtrele
# Wireshark filtresi: modbus
# veya: tcp.port == 502
```

### Unit ID (Slave Address) Mantığı

```
Doğrudan bağlantıda:
  PLC IP: 192.168.1.100, Unit ID: 1
  → Çoğu PLC Unit ID = 1 kullanır
  → Bazı cihazlar 0 veya 255 de kabul eder

Gateway arkasında:
  Gateway IP: 192.168.1.1, port: 502
  Arkasındaki RS-485 cihazlar:
    Unit ID = 1 → Slave #1 (Modbus RTU address 1)
    Unit ID = 5 → Slave #5 (Modbus RTU address 5)
  → Gateway, Unit ID'ye göre doğru RS-485 cihaza yönlendirir

Sorun giderme: Bağlantı kuruluyor ama yanıt yok
  → Unit ID yanlış. Üretici belgesi kontrol edilmeli.
  → 1, 2, 247, 255 sırasıyla denenebilir.
```

### Wireshark ile Modbus TCP Analizi

```
Wireshark filter: modbus
→ Her istek-yanıt çifti görünür
→ MBAP header, Transaction ID, Function Code, Data ayrıştırılmış

Önemli görünümler:
  Modbus/TCP → Query → Function Code
  Modbus/TCP → Response → Data
  Modbus/TCP → Response → Exception (hata durumunda)
```

## Örnekler

### Örnek 1: MBAP Header Manuel Analizi

```python
# Wireshark veya TCP dump'tan yakalanan ham Modbus TCP frame
frame = bytes.fromhex('00010000000601030000000A')

transaction_id = int.from_bytes(frame[0:2], 'big')   # 1
protocol_id    = int.from_bytes(frame[2:4], 'big')   # 0 (Modbus)
length         = int.from_bytes(frame[4:6], 'big')   # 6
unit_id        = frame[6]                             # 1
function_code  = frame[7]                             # 3 (Read Holding Registers)
start_addr     = int.from_bytes(frame[8:10], 'big')  # 0
quantity       = int.from_bytes(frame[10:12], 'big') # 10

print(f"TxID={transaction_id}, FC={function_code}, Addr={start_addr}, Count={quantity}")
# TxID=1, FC=3, Addr=0, Count=10
```

### Örnek 2: Güvenli Modbus TCP Ağ Mimarisi

```
İnternete açık kurumsal ağ
    │
    │ Güvenlik duvarı — port 502 KAPALI
    │
Demilitarized Zone (DMZ)
    │
    │ Güvenlik duvarı — yalnızca belirli IP adresleri
    │
OT (Operasyonel Teknoloji) Ağı
    ├── SCADA Server (192.168.10.10) → Tek yetkili Master
    ├── PLC-1 (192.168.10.100:502) ← Slave, yalnızca SCADA'dan
    ├── PLC-2 (192.168.10.101:502) ← Slave, yalnızca SCADA'dan
    └── VFD-1 (192.168.10.150:502) ← Slave, yalnızca SCADA'dan

Kural: Port 502, yalnızca yetkili SCADA IP'sinden gelen bağlantılara açık.
       Güvenlik duvarı kuralı: SRC=192.168.10.10, DST=any, PORT=502 → ALLOW
       Diğer her şey → DENY
```

## Sık Yapılan Hatalar

### Hata 1: RTU over TCP ile Modbus TCP Karıştırma

```
Semptom: Bağlantı kuruluyor, istek gönderiliyor ama yanıt yok veya exception.
Neden  : Cihaz RTU over TCP kullanıyor, istemci standart Modbus TCP gönderiyor.

Teşhis: Wireshark → İstek frame'ine bak:
  7+ byte MBAP header varsa → Modbus TCP
  Slave address + FC + CRC yapısı varsa → RTU over TCP

Çözüm: İstemci yazılımının RTU over TCP modunu etkinleştir.
        pymodbus: ModbusTcpClient yerine ModbusRtuFramer kullan.
```

### Hata 2: Port 502'yi Doğrudan İnternete Açmak

```
FrostyGoop malware (2024 Ukrayna olayı): port 502 açık = fiziksel saldırı.
Shodan taramasında açık port 502 bulunan endüstriyel cihaz: binlerce.

Kural: Port 502 asla doğrudan internete açılmamalı.
       VPN veya güvenlik duvarı ile korumalı ağ içi erişim.
```

### Hata 3: Unit ID = 0 veya 255 Yanılgısı

```
Bazı cihazlar Unit ID'yi tamamen yok sayar (broadcast, her ID'yi kabul eder).
Bazıları yalnızca belirli bir ID'ye yanıt verir.

Kural: Üretici belgesinden Unit ID kontrol et.
       Deneme: 1, 0, 255 sırasıyla dene.
```

## Gerçek Proje Notları

**Not 1 — FrostyGoop'tan Öğrenilenler**  
2024'te Ukrayna'daki enerji altyapısına Modbus TCP üzerinden saldırı yapıldı. Fiziksel donanım üzerinde doğrudan komut gönderildi. Ağ güvenliği: Sıfır. Sonuç: 600 apartman bloğunda ısıtma sistemi çöktü. Modbus güvenliği protokol düzeyinde değil, ağ mimarisi düzeyinde sağlanmalıdır.

**Not 2 — RTU over TCP Tuzağı**  
Bir enerji sayacı projemizde standart pymodbus Modbus TCP istemcisiyle bağlandık; bağlantı kuruldu ama okuma sürekli hata veriyordu. Wireshark analizi: Cihaz RTU over TCP kullanıyordu. Üretici belgesi bunu açıkça yazmıyordu. pymodbus'ta `Modbus RTU Framer over TCP` kullanımına geçince anında çalıştı.

**Not 3 — Polling Döngüsünün Tasarımı**  
Bir SCADA sisteminde 50 Modbus slave'i tek master'dan sorgulanıyordu. Her cihaz için 10 register, 50ms timeout = 500ms/cihaz × 50 cihaz = 25 saniye tam tur. Bazı kritik değerlerin güncellenmesi 25 saniye sürebiliyordu. Çözüm: Kritik cihazlar önce, az değişen cihazlar seyrek sorgulandı. Döngü 8 saniyeye indi.

**Not 4 — Transaction ID Sıfır Gönderen İstemci**  
Bir gateway arkasındaki cihaz tüm yanıtlarda Transaction ID = 0 döndürüyordu. Tek istek/tek yanıt senaryosunda sorun yoktu. Ancak iki Modbus isteğini pipeline (yanıt beklemeden) gönderen bir kütüphane kullanıldığında, gelen yanıtlar birbirine karıştı: TxID hep 0 olduğu için hangi yanıtın hangi isteğe ait olduğu ayırt edilemedi. Çözüm: İstemciyi strict-synchronous moda aldık (her zaman yanıt bekle, sonra gönder). TxID'ye güvenmek yerine sıralı senkron iletişim her zaman güvenli taraftır.

**Not 5 — Nagle Algoritması ve Gecikme Tuzağı**  
Bir Linux gateway üzerinde çalışan Python istemcisinde her Modbus istek-yanıtı ~40ms sürüyordu, oysa ağ ping'i <1ms idi. Sorun TCP Nagle algoritması + delayed ACK etkileşimiydi: Küçük Modbus PDU'ları (12 byte istek) tampona alınıp geç gönderiliyordu. `socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)` ile Nagle kapatıldı; round-trip 40ms'den 2ms'ye düştü. Modbus gibi küçük-paket-yoğun protokollerde TCP_NODELAY neredeyse her zaman doğru tercihtir.

**Not 6 — Yarı Açık Bağlantı (Half-Open Socket) Sessiz Donması**  
Bir PLC'nin güç kaynağı dalgalanıp TCP bağlantısı düzgün kapanmadan koptuğunda (FIN/RST yok), SCADA istemcisi bağlantıyı hâlâ "açık" sanıyordu. İstekler gönderiliyor ama TCP retransmit timeout'u (default ~60-120s) dolana kadar hata dönmüyordu — veriler 2 dakika boyunca dondu. Çözüm: Uygulama seviyesinde watchdog (3sn yanıt gelmezse bağlantıyı zorla kapat + reconnect) ve `SO_KEEPALIVE` ile agresif keepalive (5sn). OS'in TCP timeout'una asla güvenme.

**Not 7 — Vendor Farkı: Eş Zamanlı Bağlantı Limiti**  
Üç farklı slave cihazda MaxConnections davranışı tamamen farklıydı: Bir Wago kontrolcü 8 eş zamanlı bağlantıyı kabul edip 9.'yu reddetti (TCP RST); bir enerji sayacı yalnızca 1 bağlantıya izin verip yeni bağlantı gelince en eskiyi sessizce düşürdü; ucuz bir Çin gateway'i sınırsız bağlantı kabul edip 4. bağlantıdan sonra tüm yanıt sürelerini 10× yavaşlattı. Birden fazla master/istemci tasarlarken slave'in bağlantı limiti mutlaka belgeden veya testle doğrulanmalıdır.

## Edge Case'ler ve Sistem Limitleri

Modbus TCP'nin görünen basitliği, sınır koşullarında beklenmedik davranışları gizler. Aşağıdakiler saha pratiğinde tekrar tekrar görülen limitlerdir.

```
LİMİT / EDGE CASE                  DEĞER / DAVRANIŞ              SONUÇ
─────────────────────────────────────────────────────────────────────────────
MBAP Length alanı (16-bit)         maks 65535 byte PDU          Pratikte FC sınırı
                                                                 önce dolar
Transaction ID (16-bit)            0x0000–0xFFFF, wrap-around   65536 sonra başa
                                                                 döner; uzun
                                                                 oturumda çakışma
Protocol ID                        her zaman 0x0000             ≠0 gelirse frame
                                                                 reddedilmeli
Unit ID                            0–255 (0xFF rezerve/broadcast)Gateway dışında
                                                                 anlamı belirsiz
TCP segment fragmentasyonu         1 MBAP frame ≠ 1 TCP paketi  Birden çok recv()
                                                                 gerekebilir
Tek TCP paketinde 2 frame          mümkün (TCP stream)          Length'e göre
                                                                 parçalamak şart
Port 502 standart                  bazı cihazlar 1502/5020      Doğrula
Keepalive/idle timeout             vendor-spesifik (5–60s)      Sessiz disconnect
```

**TCP stream sınırı — en sık atlanan edge case:**
Modbus TCP, mesaj-tabanlı değil **byte-stream** üzerine kuruludur. Tek bir `recv()` çağrısı yarım bir MBAP frame, tam bir frame veya **birden fazla** frame içerebilir. Doğru istemci, MBAP Length alanını okuyup tam olarak `7 + (Length - 1)` byte toplanana kadar okumaya devam etmelidir. Naif "tek recv = tek yanıt" varsayımı yüksek trafikte (ardışık hızlı istek) sessizce bozulur.

```python
# ❌ Naif okuma — fragmentasyonda kırılır
data = sock.recv(1024)   # Yarım frame veya 2 frame gelebilir

# ✅ Length-aware okuma
header = recv_exact(sock, 6)          # MBAP'ın ilk 6 byte'ı
length = int.from_bytes(header[4:6], 'big')
rest   = recv_exact(sock, length)     # Unit ID + PDU
frame  = header + rest
```

**Length alanı ile gerçek FC limiti:**
MBAP Length 16-bit olduğundan teorik PDU 65535 byte. Ancak FC03/04 yanıtında byte count alanı 8-bit (maks 255 byte = 127 register), bu yüzden register başına 2 byte ile **okuma limiti 125 register**, yazma (FC16) **123 register**'da sabitlenir. Yani gerçek darboğaz MBAP değil, PDU içindeki byte-count alanlarıdır.

**Unit ID = 0 belirsizliği:**
Spesifikasyon Unit ID 0'ı "doğrudan bağlı cihaz" olarak tanımlar, 0xFF'i ise "Unit ID kullanılmıyor" anlamında önerir. Pratikte cihazların yarısı 0'ı broadcast sanır, diğer yarısı yok sayar. Doğrudan TCP bağlantılarında daima cihazın belgesindeki değeri kullan; tahmin etme.

## Optimizasyon

Modbus TCP'de performans, neredeyse tamamen **round-trip sayısını azaltmak** ve **TCP davranışını ayarlamak** ile ilgilidir. Bant genişliği nadiren darboğazdır; gecikme (latency) ve istek sayısı darboğazdır.

```
OPTİMİZASYON ÖNCELİĞİ (en yüksek kazanç → en düşük)
─────────────────────────────────────────────────────────────────
1. Batch read           : Bitişik registerları tek FC03 ile oku
                          20 ayrı istek (40ms) → 1 istek (2ms)
2. TCP_NODELAY          : Nagle'ı kapat → küçük PDU gecikmesini sıfırla
                          40ms → 2ms round-trip (en dramatik tekil kazanç)
3. Persistent connection: Her döngüde connect/disconnect YAPMA
                          TCP 3-way handshake (1 RTT) her seferinde israf
4. Polling frekansı     : Değişmeyen veriyi sık sorgulama
                          Setpoint 5sn, ölçüm 200ms gibi katmanla
5. Register haritası    : Sık okunanları bitişik yerleştir
                          Tek bloğu tek istekte oku
6. Eş zamanlı bağlantı  : Bağımsız cihazları paralel oku
                          (tek slave'e değil, farklı IP'lere)
```

**Batch read'in matematiği:**
LAN içinde tipik round-trip latency 1–3ms'dir; PDU iletim süresi (~12 byte @ 100Mbps) nanosaniye mertebesinde, ihmal edilebilir. Yani 20 değeri okumanın maliyeti, **20 × latency** veya **1 × latency** arasında seçimdir. Modbus'ta verimlilik = "kaç istek attın", "kaç byte gönderdin" değil.

**Connection pooling vs tek bağlantı:**
Tek slave için tek persistent bağlantı en iyisidir (Modbus zaten senkron). Birden fazla **farklı** slave için her birine ayrı kalıcı bağlantı + paralel I/O (thread/async) toplam tur süresini cihaz sayısına bölmez ama belirgin azaltır. Aynı slave'e paralel bağlantı genelde kazanç sağlamaz — slave istekleri yine seri işler.

**Polling katmanlama örneği:**
```
Katman A (200ms) : Kritik proses değerleri (hız, sıcaklık, durum word)
Katman B (1s)    : İkincil ölçümler (basınç, akış, sayaçlar)
Katman C (5s)    : Setpoint geri okuma, diagnostik, firmware versiyonu
→ Toplam ağ yükü, hepsini 200ms'de okumaya göre ~%70 azalır.
```

## Derin Teknik Detay

**Neden MBAP header var ve CRC yok?**
Seri Modbus RTU, byte-stream üzerinde frame sınırını "3.5 karakter sessizliği" ile belirler ve CRC-16 ile bütünlüğü korur — çünkü RS-485 fiziksel katmanı gürültülüdür ve mesaj sınırı yoktur. TCP ise zaten **sıralı, hatasız, akış-tabanlı** bir transport sağlar: Checksum (TCP), sıralama (sequence number) ve retransmit TCP katmanında halledilir. Dolayısıyla Modbus TCP tasarımcıları CRC'yi attı (gereksiz, TCP zaten doğruluyor) ve frame sınırını belirtmek için 7-byte MBAP header'daki **Length** alanını ekledi. MBAP, RTU'nun timing-tabanlı framing'ini açık bir byte-sayımıyla değiştirir.

**Transaction ID neden var — RTU'da yokken?**
Seri Modbus katı half-duplex senkrondur: Master bir istek atar, yanıtı bekler, başka istek atamaz. Dolayısıyla istek-yanıt eşleşmesi triviyaldir. TCP ise multiplexing'e izin verir — bir master birden fazla isteği yanıt beklemeden pipeline'layabilir. Transaction ID, gelen yanıtı doğru isteğe eşlemek için bu pipeline senaryosunu mümkün kılar. Ancak pratikte çoğu istemci yine senkron çalışır ve TxID'yi sadece bir sıra numarası olarak kullanır (Not 4'teki TxID=0 cihazı bu yüzden çoğu durumda sorun çıkarmaz).

**vs alternatifler — neden Modbus TCP "yetersiz ama yenilmez":**
```
                Modbus TCP        OPC UA              EtherNet/IP
──────────────────────────────────────────────────────────────────────
Veri modeli     16-bit register   Zengin nesne tipi   CIP nesne modeli
Keşif           Yok (belge şart)  Browse/Address Space EDS dosyası
Güvenlik        Yok               X.509, şifreleme    CIP Security
Push/event      Yok (poll-only)   Subscription        I/O connection
Öğrenme eğrisi  Saatler           Haftalar            Günler
Cihaz desteği   ~Evrensel         Artıyor             Rockwell ağırlıklı
```
Modbus TCP'nin kalıcılığının kökü: Veri modeli o kadar ilkel ki (16-bit kelimeler + 8 fonksiyon) **herhangi** bir mikrodenetleyici onu birkaç yüz satırla implemente edebilir. OPC UA bir gömülü stack için megabaytlarca kod ve sertifika altyapısı ister. "Yeterince iyi ve her yerde çalışıyor" özelliği, teknik üstünlükten daha güçlü bir ağ etkisi yaratır.

**Stateless tasarımın bedeli:**
Modbus sunucusu istemci durumu tutmaz — her istek bağımsızdır. Bu, sunucu implementasyonunu basitleştirir (oturum yönetimi yok) ama iki maliyet getirir: (1) Olay bildirimi imkânsız — istemci değişikliği ancak tekrar sorgulayarak öğrenir; (2) 32-bit değerlerin iki 16-bit register'a bölünmesi atomik değildir → "word tearing" (bkz. 02_register_model.md). Sunucu, bir 32-bit değeri tam yazmadan istemci yarısını okursa tutarsız değer alır. Bu, basitliğin doğrudan bedelidir ve protokol seviyesinde çözümü yoktur; uygulama seviyesinde (handshake biti, çift okuma) yönetilir.

## İlgili Konular

```
knowledge/protocols/modbus-tcp/
├── 02_register_model.md         → Register tipleri ve adresleme
├── 03_function_codes.md         → Function code referansı
├── 04_codesys_slave_config.md   → CODESYS slave yapılandırması
└── 05_client_implementations.md → Python ve JavaScript istemcileri

knowledge/codesys/networking/
└── 02_modbus_slave.md           → CODESYS Modbus slave kurulum rehberi

Araçlar:
  Modbus Poll  → GUI Modbus master test aracı
  Modbus Slave → GUI Modbus slave simülatörü
  pymodbus     → Python kütüphanesi
  Wireshark    → Protokol analizi (modbus filtresi)
  QModMaster   → Açık kaynak GUI Modbus test aracı
```
