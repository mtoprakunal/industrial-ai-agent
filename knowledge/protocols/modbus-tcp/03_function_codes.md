---
KONU        : Modbus Fonksiyon Kodları
KATEGORİ    : protocols
ALT_KATEGORI: modbus-tcp
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/modbus-function-codes-implementation-guide-for-device-developers"
    başlık: "Industrial Monitor Direct — Modbus Function Codes Implementation Guide"
    güvenilirlik: topluluk
  - url: "https://www.pymodbus.org/docs/basic-concepts"
    başlık: "PyModbus Docs — Modbus Protocol Basics"
    güvenilirlik: topluluk
  - url: "https://www.csimn.com/CSI_pages/Modbus101.html"
    başlık: "Control Solutions — Modbus 101"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_protocol_basics.md"
    ilişki: gerektirir
  - konu: "02_register_model.md"
    ilişki: gerektirir
  - konu: "05_client_implementations.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Modbus register modeli (02_register_model.md)"
ÇELİŞKİLER :
  - kaynak: "FC06 vs FC16 — tek register yazmada hangisi?"
    konu: "FC06 ve FC16 (count=1) aynı işi yapar ama bazı cihazlar yalnızca birini destekler"
    çözüm: >
      FC06: Tek register yazma için özel fonksiyon. Daha kısa frame.
      FC16: Çoklu register yazma. count=1 ile tek register de yazar.
      Her ikisi de standart. Cihaz belgesi hangisini desteklediğini belirtir.
      Emin değilsen FC16 kullan — daha evrensel.
---

## Özün Ne

Modbus'ta 8 temel fonksiyon kodu vardır ve bunların 6'sı neredeyse tüm projelerde kullanılır. Her kod belirli bir register tipine ve işleme karşılık gelir. FC01-04 okuma, FC05-06 tekli yazma, FC15-16 çoklu yazma. Hata durumunda sunucu, normal fonksiyon kodunun 0x80 OR'lanmış haliyle (exception response) yanıt verir. Bu belge her kodu pratik örnekler ve gerçek kullanım senaryolarıyla ele alır.

## Nasıl Çalışır

### Fonksiyon Kodu Özet Tablosu

```
FC   | Hex  | İşlem                    | Register Tipi     | Pymodbus Metodu
─────|------|--------------------------|-------------------|---------------------------------
01   | 0x01 | Read Coils               | Coil (0x)         | read_coils()
02   | 0x02 | Read Discrete Inputs     | Discrete (1x)     | read_discrete_inputs()
03   | 0x03 | Read Holding Registers   | Holding (4x)      | read_holding_registers()
04   | 0x04 | Read Input Registers     | Input (3x)        | read_input_registers()
05   | 0x05 | Write Single Coil        | Coil (0x)         | write_coil()
06   | 0x06 | Write Single Register    | Holding (4x)      | write_register()
15   | 0x0F | Write Multiple Coils     | Coil (0x)         | write_coils()
16   | 0x10 | Write Multiple Registers | Holding (4x)      | write_registers()
─────|------|--------------------------|-------------------|---------------------------------
08   | 0x08 | Diagnostics              | —                 | diagnostics_request()
22   | 0x16 | Mask Write Register      | Holding (4x)      | mask_write_register()
23   | 0x17 | Read/Write Multiple Regs | Holding (4x)      | readwrite_registers()
```

---

### FC01 — Read Coils (Coil Oku)

```
Amaç    : Coil (0x) değerlerini oku — 1-bit, okuma+yazma capable
İstek   : [FC=01][Start Addr 2B][Count 2B]
Yanıt   : [FC=01][Byte Count 1B][Coil Data N byte]

Coil verisi: 8 coil = 1 byte. Coil 0 = bit 0 (LSB).

Örnek: 8 coil oku (address 0, count 8):
  Request:  01 01 00 00 00 08
  Response: 01 01 01 C5  (0xC5 = 11000101 binary)
  
  Bit analizi:
    Coil 0 = bit 0 = 1 (TRUE)
    Coil 1 = bit 1 = 0 (FALSE)
    Coil 2 = bit 2 = 1 (TRUE)
    Coil 3 = bit 3 = 0 (FALSE)
    Coil 4 = bit 4 = 0 (FALSE)
    Coil 5 = bit 5 = 0 (FALSE)
    Coil 6 = bit 6 = 1 (TRUE)
    Coil 7 = bit 7 = 1 (TRUE)
```

**Gerçek kullanım:** Motor çalışma durumunu birkaç bit olarak okumak. 16 motorun on/off durumu FC01 ile tek istekte okunabilir.

---

### FC02 — Read Discrete Inputs (Dijital Giriş Oku)

```
Amaç    : Discrete Input (1x) değerlerini oku — salt okunur 1-bit
İstek   : [FC=02][Start Addr 2B][Count 2B]
Yanıt   : [FC=02][Byte Count 1B][DI Data N byte]

FC01 ile aynı veri formatı ama farklı adres alanı.
```

**Gerçek kullanım:** Fiziksel buton, limit switch, kapı sensörü durumunu okumak. CODESYS slave'de Discrete Inputs genellikle GVL_IO'daki boolean giriş değişkenlerine bağlanır.

---

### FC03 — Read Holding Registers (Holding Register Oku)

**En sık kullanılan fonksiyon kodu. Projelerin %80+'ında yalnızca bu kullanılır.**

```
Amaç    : Holding Register (4x) değerlerini oku
İstek   : [FC=03][Start Addr 2B][Count 2B]
Yanıt   : [FC=03][Byte Count 1B][Register Data N×2 byte]

Her register 2 byte (16-bit). Big-endian.

Örnek: 4 register oku (address 0, count 4):
  Request:  03 03 00 00 00 04
  Response: 03 03 08 01 F4 00 64 07 D0 00 0A
  
  Byte Count = 8 (4 register × 2 byte)
  HR[0] = 0x01F4 = 500
  HR[1] = 0x0064 = 100
  HR[2] = 0x07D0 = 2000
  HR[3] = 0x000A = 10
```

**Maksimum count:** 125 register / istek (Modbus TCP spesifikasyonu sınırı).

**Gerçek kullanım:**
```python
# Tüm proses değerlerini tek istekte oku (verimli)
result = client.read_holding_registers(address=0, count=20, slave=1)

# Ayrıştır
speed_setpoint = result.registers[0] / 10.0      # HR[0]: ×10
temp_setpoint  = result.registers[1] / 10.0      # HR[1]: ×10
recipe_id      = result.registers[2]              # HR[2]: 1:1
command_word   = result.registers[3]              # HR[3]: bit mask
```

---

### FC04 — Read Input Registers (Input Register Oku)

```
Amaç    : Input Register (3x) değerlerini oku — salt okunur 16-bit
İstek   : [FC=04][Start Addr 2B][Count 2B]
Yanıt   : [FC=04][Byte Count 1B][Register Data N×2 byte]

FC03 ile aynı frame yapısı, farklı register alanı.
```

**Gerçek kullanım:** Analog sensör ölçümleri (sıcaklık, basınç, akım). Bazı cihazlar Input Register kullanmaz ve her şeyi Holding'e koyar — bu durumda FC04 döner exception.

---

### FC05 — Write Single Coil (Tek Coil Yaz)

```
Amaç    : Tek bir Coil'i TRUE veya FALSE yap
İstek   : [FC=05][Coil Addr 2B][Value 2B]

Value:
  0xFF00 = TRUE (ON)
  0x0000 = FALSE (OFF)
  Diğer değerler: Exception döner

Örnek: Coil 3'ü TRUE yap:
  Request:  05 05 00 03 FF 00
  Response: 05 05 00 03 FF 00  (echo — aynı frame)
```

**Gerçek kullanım:** Tek motor başlatma komutu. HMI "Start" butonuna basılınca.

---

### FC06 — Write Single Register (Tek Holding Register Yaz)

```
Amaç    : Tek bir Holding Register'a 16-bit değer yaz
İstek   : [FC=06][Register Addr 2B][Value 2B]
Yanıt   : [FC=06][Register Addr 2B][Value 2B]  (echo)

Örnek: HR[5]'e 1234 yaz:
  Request:  06 06 00 05 04 D2
  Response: 06 06 00 05 04 D2  (echo)
```

**Gerçek kullanım:** Setpoint güncelleme (tek değer). Hız setpoint, sıcaklık setpoint.

---

### FC15 — Write Multiple Coils (Çoklu Coil Yaz)

```
Amaç    : Birden fazla Coil'i tek istekte yaz
İstek   : [FC=0F][Start Addr 2B][Count 2B][Byte Count 1B][Coil Data N byte]
Yanıt   : [FC=0F][Start Addr 2B][Count 2B]

8 coil = 1 byte. Coil 0 = LSB.

Örnek: Coil 0-3'e [TRUE,FALSE,TRUE,FALSE] yaz:
  0b00000101 = 0x05
  Request: 0F 0F 00 00 00 04 01 05
```

**Gerçek kullanım:** Alarm reset için birden fazla bit aynı anda temizlemek. Birden fazla çıkış aynı anda aktive etmek.

---

### FC16 — Write Multiple Registers (Çoklu Register Yaz)

```
Amaç    : Birden fazla Holding Register'a tek istekte yaz
İstek   : [FC=10][Start Addr 2B][Count 2B][Byte Count 1B][Data N×2 byte]
Yanıt   : [FC=10][Start Addr 2B][Count 2B]

Maksimum: 123 register / istek

Örnek: HR[0-2]'e [100, 200, 300] yaz:
  Request: 10 10 00 00 00 03 06 00 64 00 C8 01 2C
  Response: 10 10 00 00 00 03
```

**Gerçek kullanım:** Float32 (2 register aynı anda), recipe yükleme (tüm parametreler tek istek), toplu parametre güncelleme.

---

### Hata (Exception) Yanıtları

```
Hata durumunda slave, normal FC yerine FC+0x80 ile yanıtlar:
  FC03 → 0x83 (hata yanıtı)
  FC06 → 0x86 (hata yanıtı)
  FC16 → 0x90 (hata yanıtı)

Hata yanıt frame:
  [FC+0x80][Exception Code]

Exception Code'lar:
  0x01 → Illegal Function     : Bu FC desteklenmiyor
  0x02 → Illegal Data Address : Register adresi geçersiz (aralık dışı)
  0x03 → Illegal Data Value   : Değer geçersiz (0xFF00/0x0000 dışı FC05 için)
  0x04 → Slave Device Failure : Cihaz içsel hata
  0x05 → Acknowledge          : İstek alındı, işleniyor (uzun işlemler)
  0x06 → Slave Device Busy    : Cihaz meşgul
  0x0A → Gateway Path Unavailable : Gateway yol bulunamadı
  0x0B → Gateway Target Device Failed to Respond : Hedef cihaz yanıt vermedi
```

**Hata tespiti (pymodbus):**

```python
result = client.read_holding_registers(0, 10, slave=1)

if result.isError():
    print(f"Hata: {result}")
    # ModbusIOException: exception response, exception code 0x02
    # → Register adresi aralık dışı — belge kontrol et
```

### Exception Code Tanı Rehberi

```
0x01 Illegal Function:
  → FC desteklenmiyor. Cihaz belgesi hangi FC'leri desteklediğini listeler.
  → FC04 dene, 0x01 geldi → Cihaz Input Register desteklemez; FC03 kullan.

0x02 Illegal Data Address:
  → Adres aralık dışı. Register haritasına bak.
  → Çok büyük count da bu hatayı verebilir (son register aralık dışına çıkıyor).

0x03 Illegal Data Value:
  → FC05'te 0xFF00/0x0000 dışında değer gönderildi.
  → FC16'da byte count ile register count tutarsızlığı.

0x04 Slave Device Failure:
  → Cihaz içsel arıza. Yeniden başlatma gerekebilir.

0x06 Slave Device Busy:
  → Cihaz işlemi tamamlayamıyor (firmware güncelleme gibi).
  → Birkaç saniye bekleyip tekrar dene.
```

## Pratikte Nasıl Kullanılır

### Hangi FC'yi Ne Zaman Kullanırsın?

```
Görev                              → FC  | Neden
─────────────────────────────────────────────────────────────────────
Motor çalışma durumu (bit)         → 01  | Coil okuma — çoklu bit verimli
Kapı/switch durumu                 → 02  | Discrete input
Tüm proses değerleri               → 03  | Holding — tek istekte çoklu
Sensör ölçümleri (salt okunur)     → 04  | Input register (destekleniyorsa)
Tek motor start/stop               → 05  | Tek coil yazma
Setpoint güncelleme (tek değer)    → 06  | Tek register yazma
Float32 setpoint (2 register)      → 16  | Çoklu register — atomik yaz
Tüm recipe parametreleri           → 16  | Birden fazla register aynı anda
Birden fazla coil sıfırla          → 15  | Çoklu coil yazma
```

### FC03 vs FC04 — Pratik Karar

```
Cihaz belgesi açıkça ayrım yapıyorsa:
  Ölçümler (30001-39999): FC04
  Parametreler (40001-49999): FC03

Cihaz belgesi tüm veriyi 4x'te listeliyorsa:
  → FC03 kullan, FC04 exception verir.

Emin değilsen: FC03 dene → çalışıyorsa tamam.
               FC03 exception → FC04 dene.
```

### Batch Read Stratejisi

```python
# ❌ YANLIŞ — Her değer için ayrı istek (çok yavaş)
speed  = client.read_holding_registers(0, 1, slave=1).registers[0]
temp   = client.read_holding_registers(1, 1, slave=1).registers[0]
recipe = client.read_holding_registers(2, 1, slave=1).registers[0]
# 3 round-trip = 3× gecikme

# ✅ DOĞRU — Tek istekte tüm değerler
regs = client.read_holding_registers(0, 10, slave=1).registers
speed  = regs[0] / 10.0
temp   = regs[1] / 10.0
recipe = regs[2]
# 1 round-trip = 1× gecikme
```

**Ne zaman ayrı istek kullanılır:**
- Farklı bölgeler birbirine bitişik değilse (0-5 ve 100-105)
- Birden fazla slave cihaz varsa
- Tek değer kritik ise (alarm kontrolü)

## Örnekler

### Örnek 1: Tüm Temel FC'lerin Kullanımı

```python
from pymodbus.client import ModbusTcpClient

with ModbusTcpClient('192.168.1.100', port=502, timeout=3) as client:
    slave = 1
    
    # FC01: 8 coil oku
    coils = client.read_coils(0, 8, slave=slave)
    print(f"Motor1: {coils.bits[0]}, Motor2: {coils.bits[1]}")
    
    # FC02: 4 discrete input oku
    di = client.read_discrete_inputs(0, 4, slave=slave)
    print(f"Door: {di.bits[0]}, EStop: {di.bits[1]}")
    
    # FC03: 10 holding register oku
    hr = client.read_holding_registers(0, 10, slave=slave)
    print(f"Speed SP: {hr.registers[0]/10.0}, Temp SP: {hr.registers[1]/10.0}")
    
    # FC04: 5 input register oku
    ir = client.read_input_registers(0, 5, slave=slave)
    print(f"Actual Speed: {ir.registers[0]/10.0}, Actual Temp: {ir.registers[1]/10.0}")
    
    # FC05: Coil 0 = True (Motor 1 Start)
    client.write_coil(0, True, slave=slave)
    print("Motor 1 start komutu gönderildi")
    
    # FC06: HR[0] = 450 (Hız setpoint = 45.0 m/dk)
    client.write_register(0, 450, slave=slave)
    print("Hız setpoint: 45.0")
    
    # FC15: Coil 0-3 = [True, False, True, False]
    client.write_coils(0, [True, False, True, False], slave=slave)
    print("Coil 0-3 güncellendi")
    
    # FC16: HR[0-1] = Float 85.5°C sıcaklık setpoint
    import struct
    raw = struct.pack('>f', 85.5)
    hw = struct.unpack('>H', raw[0:2])[0]
    lw = struct.unpack('>H', raw[2:4])[0]
    client.write_registers(10, [hw, lw], slave=slave)
    print("Sıcaklık setpoint: 85.5°C")
```

### Örnek 2: Exception Handling ile Sağlam Okuma

```python
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

def safe_read_holding(client, address, count, slave=1):
    """Güvenli holding register okuma — hata yönetimli."""
    try:
        result = client.read_holding_registers(address, count, slave=slave)
        
        if result.isError():
            exc_code = getattr(result, 'exception_code', 'unknown')
            error_map = {
                0x01: "Illegal Function (FC03 desteklenmiyor)",
                0x02: f"Illegal Data Address (adres {address} geçersiz)",
                0x03: "Illegal Data Value",
                0x04: "Slave Device Failure",
                0x06: "Slave Device Busy (tekrar dene)",
            }
            msg = error_map.get(exc_code, f"Exception 0x{exc_code:02X}")
            raise ValueError(f"Modbus exception: {msg}")
        
        return result.registers
    
    except ModbusException as e:
        raise ConnectionError(f"Modbus bağlantı hatası: {e}")

# Kullanım
try:
    regs = safe_read_holding(client, address=0, count=10)
    print(f"Değerler: {regs}")
except ValueError as e:
    print(f"Okuma hatası: {e}")
    # Exception code 0x02 → Adres düzeltilmesi gerekiyor
except ConnectionError as e:
    print(f"Bağlantı hatası: {e}")
    # Reconnect mantığı devreye girmeli
```

### Örnek 3: Gerçek Projede FC Kullanım Dağılımı

```
Bir paketleme hattı projesinde FC kullanım istatistiği (6 aylık log):

FC03 Read Holding Registers : %72 (ana polling döngüsü)
FC16 Write Multiple Regs    : %18 (recipe yükleme, float setpoint)
FC01 Read Coils             : %6  (motor durum okuma)
FC05 Write Single Coil      : %3  (start/stop komutları)
FC06 Write Single Register  : %1  (acil tek setpoint değişimi)

FC04, FC02, FC15 hiç kullanılmadı:
  FC04: Üretici tüm veriyi Holding'e koymuş
  FC02: Discrete input yok, coil kullanılıyor
  FC15: Tek coil komutu yeterli oldu
```

## Sık Yapılan Hatalar

### Hata 1: Exception'ı Hata Olarak Yanlış Yorumlamak

```
exception_code 0x02 geldi → "cihaz arızalı" düşüncesi.
Gerçek: Register adres aralık dışı. Adres 1 fazla yazılmış.

Doğru yaklaşım: Exception code'u oku → belgeyle karşılaştır.
0x02 = adres sorunu (belgeye bak)
0x04 = gerçek cihaz arızası
```

### Hata 2: FC05 için Yanlış Değer

```python
# ❌ YANLIŞ
client.write_coil(0, 1, slave=1)     # 1 değil! Exception: 0x03
client.write_coil(0, 255, slave=1)   # Exception: 0x03

# ✅ DOĞRU
client.write_coil(0, True, slave=1)  # pymodbus True = 0xFF00 gönderir
client.write_coil(0, False, slave=1) # pymodbus False = 0x0000 gönderir
```

### Hata 3: Float32 İçin FC06 Kullanmak

```python
# ❌ YANLIŞ — FC06 tek register yazar (16-bit)
# Float 85.5 için 2 register (32-bit) gerekli
client.write_register(10, 85.5, slave=1)  # Hatalı veri

# ✅ DOĞRU — FC16 ile iki register atomik yaz
import struct
raw = struct.pack('>f', 85.5)
hw = struct.unpack('>H', raw[0:2])[0]
lw = struct.unpack('>H', raw[2:4])[0]
client.write_registers(10, [hw, lw], slave=1)
```

## Gerçek Proje Notları

**Not 1 — FC03 Yeterli**  
Çoğu projede FC03 + FC16 yeterli. Diğer FC'ler "gerekiyor gibi görünüyor" ama üretici zaten tüm veriyi Holding Register'a koymuş. Gereksiz karmaşıklık eklemek yerine önce FC03 dene.

**Not 2 — Batch Read'ın Hız Farkı**  
100ms polling döngüsünde 20 ayrı FC03 isteği (her register için) vs 1 FC03 (count=20): Round-trip latency 192.168.1.100 → 2ms. 20 × 2ms = 40ms overhead vs 1 × 2ms. Batch read ile döngü süresinin %39'unu kurtardık.

**Not 3 — FC05 Sonrası Echo Kontrolü**  
FC05 yanıtı istek frame'in echo'sudur. Eğer echo yanlışsa (farklı adres veya değer) — bu cihaz arızasını işaret edebilir. pymodbus bunu otomatik kontrol etmez; kritik sistemlerde yanıtın doğrulanması önerilir.

**Not 4 — 125 Sınırını Aşan Sessiz Hata**  
Bir cihazda 200 register'ı tek FC03 ile okuma denendi (`count=200`). Bir kütüphane Exception 0x03 döndürdü, bir diğeri sessizce yalnızca 125 register döndürüp gerisini eski tampondan doldurdu — bu en tehlikelisiydi çünkü hata gözükmedi, veri "vardı" ama son 75 register çöptü. >125 register gerektiğinde **kütüphaneye güvenme**, isteği elle 125'lik bloklara böl. pymodbus 3.x bunu otomatik bölmez, hata döndürür.

**Not 5 — Mask Write (FC22) ile Yarış Koşulunu Çözmek**  
Çoklu-master bir sistemde iki SCADA aynı komut word'üne farklı bitler yazıyordu. Her biri read-modify-write yapıyordu (FC03 oku → bit değiştir → FC16 yaz) ve aralarında diğerinin yazması araya giriyordu → bitler kayboluyordu. Çözüm: FC22 (Mask Write Register). Cihaz desteklediği için tek atomik istekte yalnızca hedef bit değiştirildi (`result = (current AND andMask) OR (orMask AND (NOT andMask))`), diğer bitlere dokunulmadı. FC22 az bilinir ama register-içi bit yarışlarının doğru çözümüdür.

**Not 6 — FC16 Geri-Okuması Echo Değildir**  
Bir mühendis FC16 yanıtının yazdığı değerleri echo'layacağını varsaydı (FC06 gibi). FC16 yanıtı yalnızca başlangıç adresi + register sayısını döndürür, **değerleri değil**. "Yazma başarılı mı?" doğrulaması için yanıttaki count'un istenen count'a eşitliği kontrol edilmeli; değer doğrulaması ayrı bir FC03 okuması gerektirir. Kritik setpoint yazmalarında write-then-read-back deseni uygulandı.

**Not 7 — Vendor Farkı: FC23 ile Tek İstekte Oku+Yaz**  
Yüksek-frekanslı bir kontrol döngüsünde her turda setpoint yazıp ölçüm okumak iki round-trip gerektiriyordu. Cihaz FC23 (Read/Write Multiple Registers) destekliyordu: Tek istekte hem yazma hem okuma yapılır, tur süresi yarıya indi. Ancak ikinci bir vendor'un cihazı FC23'e 0x01 (Illegal Function) döndürdü — FC23 standart ama yaygın desteklenmez. Önce yetenek testi yapıp, desteklenmiyorsa ayrı FC16+FC03'e düşen bir fallback yazıldı.

## Edge Case'ler ve Sistem Limitleri

```
FC      MAKS COUNT     SINIR KAYNAĞI              EDGE CASE
─────────────────────────────────────────────────────────────────────────────
FC01/02 2000 bit       Byte count 8-bit (250 byte) 2000 coil = 250 byte
FC03/04 125 register   Byte count 8-bit (255 byte) 125×2=250 byte
FC05    tek coil       —                           Value yalnız 0xFF00/0x0000
FC06    tek register   —                           Echo döner
FC15    1968 coil      Byte count 8-bit            246 byte coil verisi
FC16    123 register   Byte count 8-bit            123×2=246 byte
FC22    tek register   —                           AND/OR mask, atomik bit
FC23    125 oku/121 yaz iki ayrı byte count        Yaygın desteklenmez
```

**count=0 davranışı:** Spesifikasyon count ≥ 1 ister. count=0 gönderildiğinde cihazların bir kısmı Exception 0x03, bir kısmı boş yanıt, bir kısmı çöker. Asla 0 gönderme.

**Aralık sınırını taşan count:** `read_holding_registers(120, 10)` — son register 129. Cihazda yalnızca 125 register varsa, **başlangıç geçerli ama son geçersiz** olduğundan Exception 0x02 döner. Yani 0x02 her zaman "başlangıç adresi yanlış" demek değildir; `start + count - 1` taşması da olabilir.

**Exception vs timeout ayrımı:**
```
Exception 0x06 (Busy)      → Cihaz yanıt verdi, "meşgulüm" dedi → tekrar dene
Timeout (yanıt yok)        → Frame kayboldu veya cihaz dondu → reconnect düşün
Exception 0x0B (Gateway)   → Gateway'in arkasındaki cihaz yanıt vermedi
                             → Unit ID veya seri hat sorunu, gateway değil
```
0x06 ile timeout'u karıştırmak yanlış kurtarma stratejisine yol açar: 0x06'da cihaz canlıdır (bekle), timeout'ta bağlantı şüphelidir (yenile).

**Broadcast (Unit ID = 0) yazma:** Seri Modbus'ta yazma fonksiyonları (FC05/06/15/16) Unit ID=0 ile broadcast edilebilir ve **yanıt beklenmez**. Modbus TCP'de broadcast pratikte anlamsızdır (TCP point-to-point) ve çoğu cihaz yine yanıt verir; broadcast davranışına TCP üzerinde güvenilmemelidir.

## Optimizasyon

```
OPTİMİZASYON                       FC KARARI / KAZANÇ
─────────────────────────────────────────────────────────────────
Batch read                         Tek FC03(count=N) ≫ N×FC03(count=1)
Atomik çoklu yazma                  FC16 ile float/recipe tek istekte
Oku+yaz birleştirme                 FC23 destekleniyorsa 2 RTT → 1 RTT
Atomik bit set/clear                FC22 ile read-modify-write'tan kaçın
Coil bloğu okuma                    16 motor durumu tek FC01 (1 istek, 2 byte)
Yazma doğrulama maliyeti            Kritik değilse read-back yapma
```

**FC seçiminin latency etkisi:**
```
Senaryo: Setpoint yaz + ölçüm oku, her döngü, LAN 2ms RTT
  FC16 + FC03 ayrı     : 2 RTT = 4ms/döngü
  FC23 (oku+yaz)       : 1 RTT = 2ms/döngü → %50 kazanç
  500ms döngüde fark önemsiz, 10ms döngüde kritik.
```

**read-modify-write'tan kaçınma (FC22):**
Bir komut word'ünde tek bit değiştirmek normalde FC03(oku) + FC16(yaz) = 2 RTT + yarış riski. FC22 tek istekte (1 RTT, atomik) yapar. Cihaz FC22 destekliyorsa register-içi bit manipülasyonunda daima tercih edilmeli — hem hızlı hem yarış-güvenli.

**Yazma doğrulama bütçesi:**
Her FC06/FC16 sonrası read-back yapmak round-trip'i ikiye katlar. Kural: Emniyet-kritik komutlar (motor start, vana) read-back ile doğrulanır; sık güncellenen, kendiliğinden tekrar yazılan setpointler (hız trim) doğrulanmaz — bir sonraki döngü zaten düzeltir.

## Derin Teknik Detay

**Function code'un PDU'daki rolü:**
PDU = `[Function Code (1 byte)][Data (N byte)]`. FC, hem **hangi register alanına** (coil/DI/HR/IR) hem **hangi işleme** (oku/yaz/tek/çoklu) erişileceğini tek byte'ta kodlar. Bu, adres alanlarının protokolde ayrı olmayıp FC ile seçilmesinin nedenidir: Adres her zaman 0x0000'dan başlar, FC "hangi 0x0000" sorusunu yanıtlar. 8-bit FC alanı 0x80 (128) altındaki değerleri normal fonksiyon, üst biti set (≥0x80) olanları exception olarak ayırır — bu yüzden geçerli FC'ler 1–127 aralığındadır.

**Exception kodlamasının zarafeti:**
Hata yanıtında FC, orijinal FC ile **0x80 OR'lanır** (FC03 → 0x83). Tek bitlik bu işaret, istemcinin yanıtı parse etmeden önce "bu başarı mı hata mı" sorusunu PDU'nun ilk byte'ının en yüksek bitine bakarak anında cevaplamasını sağlar. Ardından gelen tek byte exception code'dur. Tüm hata mekanizması 2 byte'a sığar — yine radikal basitlik.

**8-bit byte count'un dayattığı sınır:**
FC03/04 yanıtı `[FC][Byte Count (1 byte)][Data]` yapısındadır. Byte Count 8-bit olduğundan en fazla 255 byte veri taşıyabilir → 127 register. Ancak spesifikasyon güvenli pay için **125** register'da sabitler (250 byte). FC16'da istek tarafında da byte count vardır ve frame yapısı gereği **123** register limiti gelir. Bu sınırların kökü MBAP Length (65535) değil, PDU içindeki tek-byte sayaçlardır — yani limit RTU'dan miras kalmıştır, TCP'nin getirdiği bir kısıt değildir.

**FC22 Mask Write mekanizması:**
FC22 iki maske alır: AND mask ve OR mask. Sonuç register şu formülle hesaplanır:
```
Result = (Current AND And_Mask) OR (Or_Mask AND (NOT And_Mask))
```
- Bir biti **set** etmek için: And_Mask'ta o bit 0, Or_Mask'ta 1.
- Bir biti **clear** etmek için: And_Mask'ta o bit 0, Or_Mask'ta 0.
- Bir biti **korumak** için: And_Mask'ta o bit 1, Or_Mask'ta 0.
Cihaz bu işlemi tek scan'de atomik yapar; araya başka master'ın yazması giremez. Bu, register-içi bayrak yönetiminde read-modify-write yarışının protokol-seviyesi çözümüdür ve neden FC16 + manuel bit hesabından üstün olduğunu açıklar.

## İlgili Konular

```
knowledge/protocols/modbus-tcp/
├── 01_protocol_basics.md        → Frame yapısı ve MBAP header
├── 02_register_model.md         → Register tipleri
├── 04_codesys_slave_config.md   → CODESYS'te FC yapılandırması
└── 05_client_implementations.md → pymodbus ile FC kullanımı

Araçlar:
  Modbus Poll   → Her FC'yi görsel olarak test etme
  pymodbus      → Python'da programatik test
  Wireshark     → Frame seviyesi analiz
```
