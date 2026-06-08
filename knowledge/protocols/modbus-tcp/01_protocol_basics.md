---
KONU        : Modbus TCP Protokol Temelleri
KATEGORİ    : protocols
ALT_KATEGORI: modbus-tcp
SEVİYE      : Temel
SON_GÜNCELLEME: 2026-06-01
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
