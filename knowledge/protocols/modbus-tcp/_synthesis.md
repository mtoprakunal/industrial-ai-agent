---
KONU        : Modbus TCP — Sentez
KATEGORİ    : protocols
ALT_KATEGORI: modbus-tcp
SEVİYE      : Temel–Orta
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "knowledge/protocols/modbus-tcp/01_protocol_basics.md"
    başlık: "Modbus TCP Protokol Temelleri"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/modbus-tcp/02_register_model.md"
    başlık: "Modbus Register Modeli ve Adresleme"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/modbus-tcp/03_function_codes.md"
    başlık: "Modbus Fonksiyon Kodları"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/modbus-tcp/04_codesys_slave_config.md"
    başlık: "CODESYS Modbus TCP Slave Yapılandırması"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/modbus-tcp/05_client_implementations.md"
    başlık: "Modbus TCP İstemci Implementasyonları"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_protocol_basics.md"
    ilişki: detaylandırır
  - konu: "02_register_model.md"
    ilişki: detaylandırır
  - konu: "03_function_codes.md"
    ilişki: detaylandırır
  - konu: "04_codesys_slave_config.md"
    ilişki: detaylandırır
  - konu: "05_client_implementations.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/fundamentals/_synthesis.md"
    ilişki: önkoşul
  - konu: "knowledge/codesys/networking/02_modbus_slave.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "CODESYS temelleri: Device Tree, GVL, Task yapısı (codesys/fundamentals/_synthesis.md)"
  - "Temel ağ kavramları: IP adresi, TCP portu, LAN/switch"
ÇELİŞKİLER :
  - kaynak: "Modbus TCP vs Modbus RTU over TCP"
    konu: "İkisi sıklıkla karıştırılır; bağlantı kurulur ama veri gelmez"
    çözüm: >
      Modbus TCP: MBAP header içerir, CRC yoktur — standart.
      RTU over TCP: Ham RTU frame (Slave Addr + CRC) TCP'ye sarılmış — MBAP yok.
      Wireshark ile ayırt edilir; pymodbus'ta Framer parametresi değiştirilerek çözülür.
  - kaynak: "0-tabanlı vs 1-tabanlı adresleme"
    konu: "Üretici belgesinde 40001 yazan register, protokolde adres 0'dır"
    çözüm: >
      Belge notasyonu: 40001–49999 (1-tabanlı).
      Protokol / pymodbus: address = belge_no - 40001 (0-tabanlı).
      Bu fark yanlış anlaşılırsa bir register kayması olur — hatalı veri okunur.
  - kaynak: "Holding Register'a PLC kodu yazabilir mi?"
    konu: "CODESYS slave'de Holding Register master tarafından yazılır; PLC kodu üzerine yazarsa master'ın komutu her scan'de silinir"
    çözüm: >
      Tek yön prensibi: HR → PLC (master yazar, PLC okur).
      Ters yön gerekiyorsa Input Register kullan (PLC yazar, master okur).
---

## Özün Ne

Modbus TCP, 1979'dan beri kullanılan ve bugün de dünyanın en yaygın endüstriyel iletişim protokolü olan Modbus'un Ethernet/TCP-IP üzerindeki versiyonudur. Güvenlik, otomatik keşif veya zengin veri tipleri gibi modern özellikleri yoktur; buna karşın basitliği, lisanssızlığı ve evrensel cihaz desteği onu vazgeçilmez kılar. Bu sentez, beş belgeyi tek bir bütün olarak bağlar: protokol çerçeve yapısından register modeline, function code'lardan CODESYS slave yapılandırmasına ve Python/JavaScript istemcilerine kadar tüm zinciri kavramsal olarak örgüler.

## Nasıl Çalışır

### Beş Belgenin Zihin Haritası

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  MODBUS TCP — BÜTÜNSEL ZİHİN HARİTASI                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  01_protocol_basics.md                                                     │
│  ┌────────────────────────────────────────────────────────────┐           │
│  │              PROTOKOL TEMELLERI                             │           │
│  │                                                             │           │
│  │  • Master-Slave (Client-Server): Yalnızca master istek     │           │
│  │    başlatır; slave kendiliğinden veri göndermez            │           │
│  │  • Port 502, TCP bağlantısı, MBAP header (7 byte)         │           │
│  │  • Transaction ID → eşleşen yanıtı bulmak için            │           │
│  │  • Unit ID → Gateway arkasındaki cihaz ayrımı için         │           │
│  │  • Güvenlik YOK — ağ segmentasyonu zorunlu                │           │
│  └─────────────────────────────┬──────────────────────────────┘           │
│                                 │ Protokol, register modeli taşır          │
│                                 ▼                                           │
│  02_register_model.md                                                      │
│  ┌────────────────────────────────────────────────────────────┐           │
│  │              REGISTER MODELİ                                │           │
│  │                                                             │           │
│  │  4 tip:  Coil (1-bit RW)  │ Discrete Input (1-bit R)      │           │
│  │          Holding Reg (16-bit RW) │ Input Reg (16-bit R)   │           │
│  │                                                             │           │
│  │  Adresleme: Belge "40001" → protokol adres 0               │           │
│  │  Veri tipleri: UINT16, INT16, FLOAT32 (2 HR), UINT32,     │           │
│  │    STRING — tümü 16-bit registerlar üzerine kodlanır        │           │
│  └─────────────────────────────┬──────────────────────────────┘           │
│                                 │ Register tiplerine erişim FC ile olur     │
│                                 ▼                                           │
│  03_function_codes.md                                                      │
│  ┌────────────────────────────────────────────────────────────┐           │
│  │              FONKSİYON KODLARI                              │           │
│  │                                                             │           │
│  │  FC01 Coil oku    │ FC02 DI oku   │ FC03 HR oku (en sık)  │           │
│  │  FC04 IR oku      │ FC05 Coil yaz │ FC06 tek HR yaz        │           │
│  │  FC15 çok Coil yaz │ FC16 çok HR yaz (float, recipe)      │           │
│  │                                                             │           │
│  │  Hata: FC + 0x80 → Exception code (0x01-0x0B)             │           │
│  └─────────────────────────────┬──────────────────────────────┘           │
│                                 │ CODESYS slave bu FC'leri karşılar         │
│                                 ▼                                           │
│  04_codesys_slave_config.md                                                │
│  ┌────────────────────────────────────────────────────────────┐           │
│  │              CODESYS SLAVE YAPILANDIRMASI                   │           │
│  │                                                             │           │
│  │  Device Tree → Ethernet → ModbusTCP_Slave_Device ekle      │           │
│  │  General: port 502, Unit ID, register sayıları             │           │
│  │  GVL_Modbus: Tüm register değişkenleri tek GVL'de          │           │
│  │  I/O Mapping: Offset → GVL değişkeni eşleme               │           │
│  │  Bus Cycle Task: Task_Slow (100ms) — kontrol döngüsünü     │           │
│  │    yüklemez                                                 │           │
│  │  PRG_ModbusUpdate: PLC ↔ Modbus GVL veri aktarımı         │           │
│  └─────────────────────────────┬──────────────────────────────┘           │
│                                 │ Slave'e bağlanan istemci                  │
│                                 ▼                                           │
│  05_client_implementations.md                                              │
│  ┌────────────────────────────────────────────────────────────┐           │
│  │              İSTEMCİ UYGULAMALARI                           │           │
│  │                                                             │           │
│  │  Python: pymodbus — FC03/04/05/06/15/16 tam destek        │           │
│  │  JavaScript: jsmodbus — Promise tabanlı, Node.js           │           │
│  │  Float32 / UINT32 yardımcı fonksiyonlar                   │           │
│  │  Otomatik yeniden bağlanma + thread-safe lock              │           │
│  │  Polling döngüsü: Toplu okuma (batch) ile gecikme minimize │           │
│  └────────────────────────────────────────────────────────────┘           │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────┘
```

### Bütünsel Mental Model

Modbus TCP'yi anlamanın en kısa yolu şu dört cümleye sığar:

> **Protokol**: Master her şeyi sorar, slave hiç gönülsüz veri göndermez. Port 502, MBAP header, TCP güvenilirliği — 7-byte header içindeki Transaction ID her istek-yanıt çiftini eşleştirir.

> **Register Modeli**: Dört kutu vardır (Coil, DI, HR, IR). Her cihazda "asıl kutu" Holding Register'dır; çoğu üretici tüm veriyi oraya koyar. Belgedeki "40001" sayısı, kod/protokolde 0'dır — bu kayma tuzağını ezberle.

> **Function Code**: FC03 Read Holding Registers, projelerin %80+'ında tek başına yeter. Float setpoint için FC16 (iki register atomik yaz). Hata gelince FC + 0x80 yanıt döner; exception code 0x02 = adres yanlış, 0x01 = bu FC desteklenmiyor.

> **CODESYS Slave**: Device Tree'ye bir cihaz gibi eklenir. GVL_Modbus tüm register değişkenlerini barındırır. I/O Mapping offset'leri GVL'ye bağlar. PRG_ModbusUpdate her scan'de veri yönlerini (HR→PLC, PLC→IR) korur. Bus Cycle Task olarak Task_Slow seçilir.

### Frame Yapısı — Kısa Referans

```
MODBUS TCP FRAME (istek örneği — FC03, 10 register oku):

Hex: 00 01  00 00  00 06  01  03  00 00  00 0A
     │────│  │────│  │────│  │─│  │──│  │────│
     TxID    ProtoID Length  UID  FC   Addr   Count

TxID   (2B): Her istekte artan; yanıt eşleşmesi için
ProtoID(2B): Daima 0x0000
Length (2B): Unit ID + PDU'nun toplam byte sayısı
Unit ID(1B): Slave adresi (çoğunlukla 1)
FC     (1B): Fonksiyon kodu
Addr   (2B): Başlangıç register adresi (0-tabanlı)
Count  (2B): Kaç register okunacak

CRC YOK — TCP kendisi hata kontrolü sağlar.
```

## Hızlı Referans Tabloları

### A. Register Tipleri

| Tip | Boyut | Erişim | Belge Ref | Protokol Adres | Kullanım |
|---|---|---|---|---|---|
| Coil (0x) | 1 bit | R/W | 00001–09999 | 0x0000–0x270F | Dijital çıkış: röle, solenoid, LED |
| Discrete Input (1x) | 1 bit | R | 10001–19999 | 0x0000–0x270F | Dijital giriş: buton, switch, kapı |
| Holding Register (4x) | 16 bit | R/W | 40001–49999 | 0x0000–0xFFFF | Setpoint, parametre, komut, ölçüm (yaygın) |
| Input Register (3x) | 16 bit | R | 30001–39999 | 0x0000–0xFFFF | Sensör ölçümü, sayaç (salt okunur) |

**Pratik gerçek:** Çoğu cihaz, tüm veriyi Holding Register'a koyar ve yalnızca FC03 kullanır.

### B. Fonksiyon Kodu Listesi

| FC | Hex | İşlem | Register Tipi | pymodbus Metodu | Not |
|---|---|---|---|---|---|
| 01 | 0x01 | Read Coils | Coil | `read_coils()` | 8 coil = 1 byte, LSB = ilk coil |
| 02 | 0x02 | Read Discrete Inputs | Discrete | `read_discrete_inputs()` | FC01 ile aynı format |
| 03 | 0x03 | Read Holding Registers | Holding | `read_holding_registers()` | **En yaygın, maks 125 register** |
| 04 | 0x04 | Read Input Registers | Input | `read_input_registers()` | FC03 ile aynı format |
| 05 | 0x05 | Write Single Coil | Coil | `write_coil()` | Value: 0xFF00=TRUE, 0x0000=FALSE |
| 06 | 0x06 | Write Single Register | Holding | `write_register()` | Yanıt echo'dur |
| 15 | 0x0F | Write Multiple Coils | Coil | `write_coils()` | Çoklu bit aynı anda |
| 16 | 0x10 | Write Multiple Registers | Holding | `write_registers()` | Float32 ve recipe için şart; maks 123 register |

**Exception yanıtı:** Hata durumunda FC + 0x80 döner.

| Exception Code | Anlam | Çözüm |
|---|---|---|
| 0x01 | Illegal Function | Bu FC desteklenmiyor; belge kontrol et |
| 0x02 | Illegal Data Address | Adres aralık dışı; 0-tabanlı dönüşüm yap |
| 0x03 | Illegal Data Value | FC05'te 0xFF00/0x0000 dışı değer |
| 0x04 | Slave Device Failure | Cihaz içsel arıza |
| 0x06 | Slave Device Busy | Bekle ve tekrar dene |

### C. Adresleme Dönüşüm Şeması

```
BELGE NOTASYONU (1-tabanlı)  →  PROTOKOl ADRESİ (0-tabanlı)
──────────────────────────────────────────────────────────────
Holding Register:
  40001  →  address = 0
  40101  →  address = 100
  41000  →  address = 999
  Formül: address = belge_no - 40001

Input Register:
  30001  →  FC04, address = 0
  30010  →  FC04, address = 9
  Formül: address = belge_no - 30001

Coil:
  00001  →  FC01/05, address = 0
  Formül: address = belge_no - 1

Discrete Input:
  10001  →  FC02, address = 0
  Formül: address = belge_no - 10001

pymodbus her zaman 0-tabanlı kullanır.
SCADA/HMI araçları ayarlanabilir — hangi konvansiyonun seçildiğini kontrol et.
```

### D. Veri Tipi Kodlama Özeti

| Tip | Register Sayısı | Byte Order | Açıklama |
|---|---|---|---|
| UINT16 | 1 | — | Varsayılan, 0–65535 |
| INT16 | 1 | — | İki'nin tamamlayıcısı; >32767 → negatif |
| FLOAT32 | 2 | Big-Endian (AB CD) en yaygın | IEEE 754; byte order mutlaka test et |
| UINT32 | 2 | High-Low sırası | `(HR[0] << 16) | HR[1]` |
| STRING | N | Her register = 2 ASCII karakter | Yüksek byte önce |

**Float byte order varyantları:**

```
Varyant        | HR[0]   HR[1]  | Örnek: 3.14 = 0x4048F5C3
───────────────|───────────────|─────────────────────────────
Big-Endian     | 0x4048  0xF5C3 | ← En yaygın, modern cihazlar
Mixed-BE       | 0xF5C3  0x4048 | Bazı eski cihazlar (CD AB)
Little-Endian  | 0xC3F5  0x4840 | Nadir (DC BA)
Mixed-LE       | 0x48F5  0xC340 | (BA DC)

Test yöntemi: Bilinen değer yaz (örn. 1.0 = 0x3F800000),
              4 varyantı dene, eşleşeni bul.
```

### E. CODESYS Slave Yapılandırma Özeti

| Adım | Eylem | Kritik Parametre |
|---|---|---|
| 1 | Device Tree → Ethernet → Add Device → ModbusTCP_Slave_Device | Platforma uygun cihaz seç |
| 2 | General: Port, Unit ID, register sayıları | HR Count = ihtiyaç × 1.5 (yedek pay) |
| 3 | GVL_Modbus oluştur | HR → WORD, Coil → BOOL, tam belgelenmiş |
| 4 | I/O Mapping: Offset → GVL değişkeni | Offset 0 = protokol adres 0 |
| 5 | Bus Cycle Task: Task_Slow (100ms) | Kontrol task'ını yüklemez |
| 6 | PRG_ModbusUpdate yaz | HR→PLC (okuma), PLC→IR (yazma) |

### F. Kütüphane Seçim Kartı

| Kütüphane | Dil | RTU? | Async? | Ne Zaman Seç |
|---|---|---|---|---|
| pymodbus | Python | Evet | Evet | Endüstriyel script, TCP + RTU, async pipeline |
| pyModbusTCP | Python | Hayır | Hayır | Küçük monitoring scripti, `auto_open` kolaylığı |
| jsmodbus | Node.js | Evet | Promise | Web dashboard, Node-RED entegrasyonu |
| modbus-serial | Node.js | Evet | Callback | Hem TCP hem RS485 serial |

## Pratikte Nasıl Kullanılır

### "İlk CODESYS Slave + Python Client" Kontrol Listesi

**CODESYS Slave Tarafı (Belgeler 4)**

```
□ 1. Device Tree → Ethernet arayüzü → Add Device → Modbus TCP Slave
□ 2. General: Port=502, Unit ID=1
       HR Count=200, IR Count=100, Coil Count=64, DI Count=32
□ 3. GVL_Modbus.st oluştur:
       HR değişkenleri: WORD (Master → PLC yönü)
       IR değişkenleri: WORD (PLC → Master yönü)
       Coil değişkenleri: BOOL (Master → PLC)
       DI değişkenleri: BOOL (PLC → Master)
□ 4. I/O Mapping → Her değişkeni doğru Offset'e bağla
       HR Offset 0 → GVL_Modbus.wSpeedSetpoint
       IR Offset 0 → GVL_Modbus.wActualSpeed
□ 5. Bus Cycle Task → Task_Slow seç
□ 6. PRG_ModbusUpdate oluştur, Task_Slow'a ekle:
       IR'ları PLC'den güncelle (GVL_Modbus.wActualSpeed := REAL_TO_WORD(rSpeed*10))
       HR'lardan PLC parametrelerini oku (rSpeedSP := WORD_TO_REAL(wSpeedSetpoint)/10.0)
□ 7. Build → Download → Online → Start
```

**Python İstemci Tarafı (Belge 5)**

```
□ 8. pip install pymodbus
□ 9. Temel bağlantı testi:
       nc -vz 192.168.1.100 502   # Port açık mı?
□ 10. İlk okuma:
       result = client.read_holding_registers(0, 10, slave=1)
       → result.isError() → False olmalı
□ 11. Veri doğrulama: CODESYS Watch Window değerleri ile karşılaştır
□ 12. Yazma testi: write_register(0, 450) → CODESYS'te GVL_Modbus.wSpeedSetpoint = 450
□ 13. Float testi: write_registers(20, [hw, lw]) → Float setpoint doğrula
```

### Beş Belgeyi Bağlayan Pratik Senaryo

**Görev**: CODESYS (Raspberry Pi, 192.168.1.100) üzerinde bir paketleme makinesi çalışıyor. Python izleme scripti hız ve sıcaklığı okuyor, SCADA hız setpointini yazıyor.

```
ADIM 1 — Protokol anlaşması (Belge 1)
  SCADA: Master (port 502 → 192.168.1.100)
  CODESYS: Slave (Unit ID = 1)
  Kural: SCADA istek gönderir, PLC yanıt verir.

ADIM 2 — Register haritası tasarımı (Belge 2)
  HR 0  (40001): Hız Setpoint    → SCADA yazar (FC16), PLC okur
  HR 1  (40002): Sıcaklık SP     → SCADA yazar (FC16), PLC okur
  IR 0  (30001): Gerçek Hız      → PLC yazar, SCADA okur (FC04)
  IR 1  (30002): Gerçek Sıcaklık → PLC yazar, SCADA okur (FC04)
  IR 3  (30004): Durum Word      → Bit 0=Çalışıyor, Bit 1=Hata

ADIM 3 — Hangi FC? (Belge 3)
  SCADA → Setpoint yaz: FC16 (iki register atomik)
  SCADA → Ölçüm oku  : FC04 (Input Register, salt okunur)
  Python → Durum oku : FC04, address=3

ADIM 4 — CODESYS slave kur (Belge 4)
  Device Tree → Ethernet → ModbusTCP_Slave_Device
  GVL_Modbus: wSpeedSP(HR0), wTempSP(HR1), wActualSpeed(IR0), wActualTemp(IR1), wStatus(IR3)
  I/O Mapping: HR Offset 0 → wSpeedSP, IR Offset 0 → wActualSpeed ...
  PRG_ModbusUpdate (Task_Slow, 100ms):
    GVL_Modbus.wActualSpeed := REAL_TO_WORD(rSpeed * 10.0);
    GVL_Modbus.wStatus := 16#0001 IF xRunning ELSE 16#0000;
    rSpeedSP := WORD_TO_REAL(GVL_Modbus.wSpeedSP) / 10.0;

ADIM 5 — Python istemci yaz (Belge 5)
  from pymodbus.client import ModbusTcpClient
  import struct

  with ModbusTcpClient('192.168.1.100', port=502, timeout=3) as client:

      # Setpoint yaz (45.0 m/dk → ×10 = 450)
      client.write_registers(0, [450, 856], slave=1)  # FC16

      # Ölçüm oku (FC04)
      ir = client.read_input_registers(0, 4, slave=1)
      speed  = ir.registers[0] / 10.0   # IR 0
      temp   = ir.registers[1] / 10.0   # IR 1
      status = ir.registers[3]           # IR 3
      running = bool(status & 0x0001)

      print(f"Hız: {speed}, Sıcaklık: {temp}, Çalışıyor: {running}")
```

Bu senaryo beş belgenin kesişim noktasıdır: Protokol frame'i MBAP üzerinden taşınır, register haritası yönleri belirler, FC03/04/16 veriyi aktarır, CODESYS slave GVL'yi doldurur, Python istemci tüketir.

## Sık Yapılan Hatalar

**1. Adres kayması (off-by-one) — "40101 yazdım, 40102 okunuyor"**
Belgedeki 40001 referans numarası protokol adres 0'dır. pymodbus her zaman 0-tabanlıdır. `address = belge_no - 40001` formülünü ezberle; sözlükle de yönet.

**2. RTU over TCP ile Modbus TCP karıştırma — "bağlantı kuruldu, veri yok"**
Wireshark'ta MBAP header varsa Modbus TCP, yoksa (Slave Addr + CRC yapısı) RTU over TCP. pymodbus'ta `Modbus RTU Framer over TCP` seçeneğine geç.

**3. Float byte order varsayımı — "anlamsız büyük sayı geliyor"**
"IEEE 754 float" yazan belge byte sırasını garanti etmez. Bilinen değer (1.0 = 0x3F800000) yaz, dört varyantı dene, eşleşeni bul. Asla varsayma.

**4. Holding Register'ı PLC kodu ile ezmek — "setpoint yazıyorum, anında eski değere dönüyor"**
PRG_ModbusUpdate'te HR değişkenine PLC kodu yazıyorsa master'ın yazdığı her scan'de silinir. Tek yön: HR yalnızca master tarafından yazılır, PLC okur. Ters yön için Input Register kullan.

**5. Bus Cycle Task atanmamış — "slave eklendi, değerler güncellenmiyor"**
I/O Mapping → Bus Cycle Task dropdown boş bırakılırsa I/O güncelleme gerçekleşmez. Task_Slow seç.

**6. Her register için ayrı istek — "polling döngüsü çok yavaş"**
20 ayrı FC03 (her biri 2ms round-trip) = 40ms overhead. Tek FC03, count=20 = 2ms. Batch okuma zorunlu; aynı bölgedeki registerları tek istekte oku.

**7. FC06 ile float yazmak — "setpoint yanlış"**
Float32 için iki register aynı anda yazılmalı; FC06 yalnızca bir register yazar. FC16 (`write_registers`) kullan ve iki word'ü birlikte gönder.

**8. isError() kontrolü atlamak — "AttributeError: 'ExceptionResponse' has no 'registers'"**
pymodbus exception durumunda Python exception fırlatmaz; isError() True döner. Her okuma sonrasında `if result.isError(): ...` kontrolü şarttır.

**9. Port 502'yi internete açmak — "FrostyGoop tarzı saldırı"**
2024 Ukrayna olayı: Port 502 doğrudan internete açık → fiziksel hasar. Modbus güvenliği protokol düzeyinde değil, ağ mimarisi düzeyinde sağlanır: VPN, güvenlik duvarı, ağ segmentasyonu.

**10. Reconnect delay çok kısa — "PLC yeniden başlıyorken script onu bunaltıyor"**
100ms delay ile saniyede 10 bağlantı denemesi PLC'yi zorlar. Minimum 5 saniye reconnect gecikmesi kullan.

## Ne Zaman ...

### Ne Zaman Modbus TCP Kullanılır?

```
✓ Cihaz Modbus destekliyor ve başka seçenek yok
✓ Legacy entegrasyon: VFD, enerji sayacı, sensör, akıllı röle
✓ Basit izleme: Birkaç değer periyodik okuma
✓ Hızlı prototip: Standart kütüphane, minimal kurulum
✓ Çok sayıda farklı marka cihaz bir arada (evrensel uyumluluk)
```

### Ne Zaman Modbus TCP Yeterli Değildir?

```
✗ Güvenilir olay bildirimi gerekiyorsa → OPC UA Subscription veya MQTT
✗ Zengin veri tipi semantiği gerekiyorsa → OPC UA Information Model
✗ < 10ms gerçek zamanlı kontrol döngüsü → EtherCAT / PROFINET
✗ TLS şifreleme zorunluysa → Modbus/TCP Security (port 802, az cihaz destekler)
✗ Büyük, değişken veri miktarı (binlerce tag) → OPC UA daha verimli
```

### FC Seçim Kılavuzu

```
Görev                                   →  FC   Neden
──────────────────────────────────────────────────────────────────────
Motor on/off durumu (bit)               →  01   Çok coil tek istekte
Kapı, switch, sensör durumu             →  02   Discrete input
Tüm proses değerleri (ana polling)      →  03   Holding, maks 125 reg
Sensör ölçümleri (salt okunur)          →  04   Input register
Tek motor start/stop (acil komut)       →  05   Tek coil yazma
Tek setpoint güncelleme                 →  06   Tek register yazma
Float32 setpoint (2 register atomik)    →  16   Atomik — FC06 yetmez
Recipe yükleme (çok parametre)          →  16   Tek istekte tümü
Alarm / durum bitleri tek yaz           →  15   Çoklu coil
```

## Gerçek Proje Notları

**Not 1 — "0 mı, 1 mi?" Vakası — Kayıp 2 Saat**
Enerji sayacı entegrasyonunda register haritası "HR 40001 = Voltage Phase A" diyordu. Hem PLC mühendisi hem Python scripti `address=40001` yazdı. Wireshark analizi: Protokolde adres 40001 (0x9C6B) — aralık dışı → Exception 0x02. Doğrusu `address=0`. Çözüm: Register haritasına iki sütun eklendi; biri belge referansı (40001), biri protokol adresi (0).

**Not 2 — RTU over TCP Tuzağı — "Bağlantı var, veri yok"**
Standart pymodbus Modbus TCP ile enerji sayacına bağlandık; bağlantı kuruldu, okuma sürekli exception. Wireshark: İstek frame'inde MBAP yok, Slave Addr + CRC var — cihaz RTU over TCP kullanıyor. Üretici belgesi bunu belirtmiyordu. `ModbusRtuFramer over TCP` seçeneğine geçince anında çalıştı.

**Not 3 — Float Byte Order Discovery**
Frekans konvertörü: "32-bit float, IEEE 754", byte order yok. Test: setpoint=10.0 yazdık. Geri okunan: HR[0]=0x0000, HR[1]=0x4120. Big-Endian 10.0 = 0x41200000 olduğundan HR[0] Low word, HR[1] High word → Mixed-LE varyantı. Struct kodu buna göre güncellendi.

**Not 4 — Komut Register Sıfırlanmama Problemi**
HMI "Start" için komut register bit 0'ı 1 yaptı. Motor başladı ama PRG_ModbusUpdate biti sıfırlamıyordu; her döngüde "Start" komutu tekrarlanıyordu. Motor durdurulamaz hale geldi. Düzeltme:
```iecst
IF (GVL_Modbus.wCommandRegister AND 16#0001) <> 0 THEN
    GVL_HMI.xRemoteStart := TRUE;
    GVL_Modbus.wCommandRegister := GVL_Modbus.wCommandRegister AND (NOT 16#0001);
END_IF
```

**Not 5 — Polling Döngüsü Tasarımı — 25 Saniyeden 8 Saniyeye**
Bir SCADA sisteminde 50 Modbus slave, tek master, her cihaz 10 register, 50ms timeout. 50 cihaz × 500ms = 25 saniye tam tur. Kritik değerler 25 saniye gecikmeli güncelleniyordu. Çözüm: Kritik cihazlar her turda, diğerleri her üç turda bir sorgulandı. Tur süresi 8 saniyeye indi.

**Not 6 — Task Seçiminin CPU Etkisi**
Modbus slave Bus Cycle Task'ı yanlışlıkla Task_Control (10ms, Prio:2) seçildi. Task Monitor: Task_Control exec time %30 arttı. Task_Slow (100ms) olarak değiştirilince normale döndü. Kural: Modbus I/O güncelleme kontrol döngüsünden ayrı, yavaş bir task'ta çalışmalı.

**Not 7 — Thread Lock'un Önemi**
Monitoring scriptinde her sensör için ayrı thread, hepsi aynı `client` nesnesini kullanıyordu. Rastgele "invalid response" hataları geliyordu. Threading.Lock eklendikten sonra tüm hatalar kalktı. pymodbus istemci nesneleri thread-safe değildir.

## İlgili Konular

```
knowledge/protocols/modbus-tcp/          ← Şu an buradasınız
├── 01_protocol_basics.md               MBAP header, RTU vs TCP, güvenlik
├── 02_register_model.md                4 register tipi, adresleme, float/string kodlama
├── 03_function_codes.md                FC01-FC16, exception codes, batch read
├── 04_codesys_slave_config.md          Device Tree, GVL, I/O Mapping, PRG_ModbusUpdate
├── 05_client_implementations.md        pymodbus, jsmodbus, ModbusManager sınıfı
└── _synthesis.md (bu belge)

CODESYS Entegrasyonu:
knowledge/codesys/networking/
└── 02_modbus_slave.md                  CODESYS Modbus slave giriş belgesi

Önkoşul:
knowledge/codesys/fundamentals/
└── _synthesis.md                       Device Tree, GVL, Task yapısı

Sonraki Adım — Daha İleri Protokoller:
knowledge/protocols/
├── opc-ua/                             Zengin semantik model, subscription, güvenlik
└── ethernet-ip/                        Rockwell/Allen-Bradley ekosistemi

Ağ Altyapısı:
knowledge/networking/
└── ethercat/                           < 1ms gerçek zamanlı fieldbus

Test Araçları:
  Modbus Poll       → GUI Modbus master, her FC görsel test
  Modbus Slave      → GUI simülatör (gerçek PLC olmadan test)
  pymodbus          → pip install pymodbus
  pyModbusTCP       → pip install pyModbusTCP (auto_open kolaylığı)
  jsmodbus          → npm install jsmodbus
  Wireshark         → Filtre: modbus veya tcp.port == 502
  QModMaster        → Açık kaynak GUI Modbus test aracı
```
