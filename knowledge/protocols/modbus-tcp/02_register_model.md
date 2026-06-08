---
KONU        : Modbus Register Modeli ve Adresleme
KATEGORİ    : protocols
ALT_KATEGORI: modbus-tcp
SEVİYE      : Temel
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://modbussimulator.com/blog/modbus-register-types-explained"
    başlık: "ModbusSimulator — Modbus Register Types Explained (2026)"
    güvenilirlik: topluluk
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/understanding-modbus-data-objects-coils-registers-and-function-codes"
    başlık: "Industrial Monitor Direct — Modbus Data Objects Explained"
    güvenilirlik: topluluk
  - url: "https://www.csimn.com/CSI_pages/Modbus101.html"
    başlık: "Control Solutions — Modbus 101 Tutorial"
    güvenilirlik: topluluk
  - url: "https://control.com/forums/threads/modbus-registers.49685/"
    başlık: "Control.com Forum — Modbus Registers Discussion (Float, Endianness)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_protocol_basics.md"
    ilişki: gerektirir
  - konu: "03_function_codes.md"
    ilişki: tamamlar
  - konu: "04_codesys_slave_config.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Modbus protokol temelleri (01_protocol_basics.md)"
  - "Bit ve byte kavramları, big-endian/little-endian"
ÇELİŞKİLER :
  - kaynak: "0-tabanlı vs 1-tabanlı adresleme — en yaygın Modbus hatası"
    konu: "Belgede 40001 yazan register, protokolde adres 0 ile okunur"
    çözüm: >
      Üretici belgesi (register haritası): 1-tabanlı. 40001 = HR #1.
      Modbus protokol frame'i (wire): 0-tabanlı. Starting Address = 0x0000.
      pymodbus: 0-tabanlı kullanır. Belgede 40001 → kodda address=0.
      Modbus Poll/SCADA: Ayarlanabilir (konvansiyonu seç).
      Bu fark yanlış anlaşılırsa bir register kayması olur — veri var ama yanlış.
  - kaynak: "Float byte order — büyük endian ve kelime sıralama çeşitleri"
    konu: "IEEE 754 float 2 register = 4 byte ama sıralama çeşidi 4 farklı şekilde"
    çözüm: >
      En yaygın: Big-Endian (AB CD) — MSB önce. Çoğu modern cihaz.
      Mixed: CD AB veya BA DC — bazı eski cihazlar.
      Little-Endian: DC BA — nadir.
      Test: Bilinen değeri (ör. 1.0 = 0x3F800000) yaz, oku, byte sırasını doğrula.
---

## Özün Ne

Modbus veri modeli dört register tipinden oluşur: Coil, Discrete Input, Holding Register, Input Register. Bu dört tip, bit/word boyutu ve okuma/yazma erişimi bakımından birbirinden ayrılır. Register adresleme ise en çok karışıklığa neden olan konudur: Üretici belgesindeki "40001" numarası ile pymodbus'ta yazılan `address=0` aynı registerdır. Bu ayrımı içselleştirmeyen her mühendis er ya da geç "yanlış register okuyor" sorunuyla karşılaşır.

## Nasıl Çalışır

### 4 Register Tipi

```
┌─────────────────┬────────┬────────┬──────────┬──────────────────────────────┐
│ Tip             │ Boyut  │ Erişim │ FC       │ Kullanım                     │
├─────────────────┼────────┼────────┼──────────┼──────────────────────────────┤
│ Coil (0x)       │ 1 bit  │ R/W    │ 01,05,15 │ Dijital çıkış, röle komutu  │
│ Discrete Input  │ 1 bit  │ R      │ 02       │ Dijital giriş, buton, switch │
│ Holding Register│ 16 bit │ R/W    │ 03,06,16 │ Setpoint, parametre, komut   │
│ Input Register  │ 16 bit │ R      │ 04       │ Ölçüm değeri, sensör okuma   │
└─────────────────┴────────┴────────┴──────────┴──────────────────────────────┘
```

**Pratik gerçek:** Çoğu üretici tüm verisini Holding Register alanına (4x) yerleştirir ve yalnızca FC03 kullanır. Hem ölçümler hem parametreler Holding Register'dadır. Bu standardı "basitleştirir" ama Modbus veri modelinin semantiğini kaybettirir.

---

### Coil (0x — Bit Çıkış)

```
Adres aralığı (belge gösterimi): 00001 – 09999
Protokol adresi (wire): 0x0000 – 0x270F

Örnekler:
  Röle çıkışı → TRUE = enerjili
  Solenoid vana → TRUE = açık
  LED göstergesi → TRUE = yanar
  Motor start/stop komut biti

Önemli: Birden fazla coil okunurken sonuç byte'lara paketlenir.
  8 coil → 1 byte. Coil 0 = bit 0, Coil 7 = bit 7.
  Coil[3] = True → byte = 0b00001000 = 0x08
```

---

### Discrete Input (1x — Bit Giriş)

```
Adres aralığı (belge): 10001 – 19999
Protokol adresi: 0x0000 – 0x270F

Örnekler:
  Sınır switch durumu
  Kapı/kapak durumu (açık/kapalı)
  Arıza girişi (harici alarm)
  Buton durumu

Salt okunur: Master yalnızca FC02 ile okuyabilir, yazamaz.
```

---

### Holding Register (4x — 16-bit Okuma/Yazma)

```
Adres aralığı (belge): 40001 – 49999 (veya 400001 – 465535)
Protokol adresi: 0x0000 – 0xFFFF

16-bit unsigned integer (0 – 65535) varsayılan

Yaygın kullanımlar:
  Hız setpoint (0-10000 = 0.0-100.0%)
  Sıcaklık setpoint (×10 ölçekle: 856 = 85.6°C)
  Mod seçimi (0=Manuel, 1=Oto, 2=Arıza)
  Komut register (bit maskeli: bit0=Start, bit1=Stop)
  FLOAT değerler (2 ardışık register = 4 byte IEEE 754)
  STRING (N ardışık register, her register 2 ASCII karakter)
```

---

### Input Register (3x — 16-bit Salt Okunur)

```
Adres aralığı (belge): 30001 – 39999
Protokol adresi: 0x0000 – 0xFFFF

16-bit unsigned integer

Yaygın kullanımlar:
  Sıcaklık ölçümü
  Basınç ölçümü
  Akım ölçümü
  Sayaç değeri (low/high word çifti)

Not: Birçok cihaz bu ayrımı yapmaz;
     ölçümleri de Holding Register'da sunar.
```

---

### Adresleme — Karışıklığın Kaynağı

**En yaygın Modbus hatası:** Belgedeki adresi direkt koda yazmak.

```
Belge notasyonu (1-tabanlı, referans numarası):
  Holding Register 1 → "40001" veya "4x 0001"
  Holding Register 100 → "40100"
  Holding Register 1000 → "41000"

Protokol adresi (0-tabanlı, wire'da giden değer):
  Holding Register 1 → 0x0000 = 0
  Holding Register 100 → 0x0063 = 99
  Holding Register 1000 → 0x03E7 = 999

Dönüşüm:
  Protokol adresi = Belge numarası - 40001 (Holding Register için)
  Protokol adresi = Belge numarası - 1 (referans prefix hariç)

Örnekler:
  Belge: "40101" → pymodbus address = 100
  Belge: "40001" → pymodbus address = 0
  Belge: "41000" → pymodbus address = 999
  Belge: "30001" (Input Register 1) → FC04, address = 0
  Belge: "00001" (Coil 1) → FC01/FC05, address = 0
```

**SCADA ve araçlarda:**
```
Modbus Poll: "Display address" ayarını seç → 0-based veya 1-based
             1-based seçilirse "1" gir = protokol adres 0
Wonderware InTouch: tag adresini "40001" yaz → otomatik -1 yapılır
pymodbus: Her zaman 0-based kullanır
```

---

### Veri Tipi Kodlama

Modbus, yalnızca 16-bit unsigned integer taşır. Daha karmaşık tipler manuel kodlama gerektirir.

**UINT16 (varsayılan):**
```
Register 0 = 1234 → doğrudan 0x04D2
Range: 0 – 65535
```

**INT16 (işaretli 16-bit):**
```
-1234 → İki'nin tamamlayıcısı: 65535 - 1234 + 1 = 64302 → 0xFB2E
Okuma: 64302 > 32767 → int16 = 64302 - 65536 = -1234

Python:
import struct
raw = 64302
value = struct.unpack('>h', struct.pack('>H', raw))[0]  # -1234
```

**FLOAT32 (IEEE 754 — 2 Register):**
```
3.14159 = 0x40490FDB

Register 0 = 0x4049 (High Word)
Register 1 = 0x0FDB (Low Word)

Python okuma (Big-Endian, High-Low sırası):
regs = client.read_holding_registers(0, 2, slave=1).registers
import struct
value = struct.unpack('>f', struct.pack('>HH', regs[0], regs[1]))[0]
# → 3.14159

Python yazma:
packed = struct.pack('>f', 3.14159)
hw = struct.unpack('>H', packed[0:2])[0]  # High Word
lw = struct.unpack('>H', packed[2:4])[0]  # Low Word
client.write_registers(0, [hw, lw], slave=1)
```

**Byte Order Varyantları:**

```
Varyant        | Byte sırası | Örnek (3.14 = 0x4048F5C3)
───────────────|─────────────|────────────────────────────
Big-Endian     | AB CD       | HR[0]=0x4048, HR[1]=0xF5C3 ← En yaygın
Mixed-BE       | CD AB       | HR[0]=0xF5C3, HR[1]=0x4048 ← Bazı cihazlar
Little-Endian  | DC BA       | HR[0]=0xC3F5, HR[1]=0x4840 ← Nadir
Mixed-LE       | BA DC       | HR[0]=0x48F5, HR[1]=0xC340

Test: Bilinen değer (ör. 1.0 = 0x3F800000) yaz → bit sırası:
  HR[0]=0x3F80, HR[1]=0x0000 → Big-Endian
  HR[0]=0x0000, HR[1]=0x3F80 → Mixed variant
```

**UINT32 / INT32 (32-bit tam sayı — 2 Register):**
```
1000000 = 0x000F4240

HR[0] = 0x000F (High Word)
HR[1] = 0x4240 (Low Word)

Python:
regs = client.read_holding_registers(0, 2, slave=1).registers
value = (regs[0] << 16) | regs[1]  # 1000000
```

**DWORD ürün sayacı (üretimde yaygın):**
```
Üretim sayacı = 1,500,000 adet

HR[0] = 1500000 >> 16  = 22 (0x0016) ← High word
HR[1] = 1500000 & 0xFFFF = 56320 (0xDC00) ← Low word

Okuma:
count = (hr[0] << 16) | hr[1]  # 1,500,000
```

**STRING (N register):**
```
Her register = 2 ASCII karakter (1 byte high, 1 byte low)

"PUMP1" (5 karakter) → 3 register (1 boşluk ile 6 karakter)
  HR[0] = ord('P') << 8 | ord('U') = 0x5055
  HR[1] = ord('M') << 8 | ord('P') = 0x4D50
  HR[2] = ord('1') << 8 | 0x00     = 0x3100

Python decode:
regs = [0x5055, 0x4D50, 0x3100]
s = ''.join(chr(r >> 8) + chr(r & 0xFF) for r in regs).rstrip('\x00')
# → "PUMP1"
```

## Pratikte Nasıl Kullanılır

### Register Haritası Tasarımı

İyi bir register haritası şunları sağlar:
- Tutarlı bloklar (IO aynı tip aynı alanda)
- Yeterli boşluk (ileride ekleme için)
- Belgelenmiş ölçek faktörleri
- Byte order notasyonu

```
ÖRNEK REGISTER HARİTASI — Paketleme Makinesi
═══════════════════════════════════════════════════════════════════
HOLDING REGISTERS — FC03 OKU / FC06,16 YAZ
───────────────────────────────────────────────────────────────────
HR Adr | Belge Ref | Değişken               | Tip    | Ölçek | RW
───────|────────---|────────────────────────|--------|-------|----
  0    |   40001   | Hız Setpoint           | UINT16 | ×10   | RW
  1    |   40002   | Sıcaklık Setpoint      | UINT16 | ×10   | RW
  2    |   40003   | Reçete No              | UINT16 | 1     | RW
  3    |   40004   | Komut Register         | UINT16 | bit   | RW
       |           |   Bit 0 = Start        |        |       |
       |           |   Bit 1 = Stop         |        |       |
       |           |   Bit 2 = Reset        |        |       |
  4-9  |   40005-10| Rezerve                | —      | —     | —
 10    |   40011   | Akış Hız SP (HIGH)     | UINT16 | —     | RW
 11    |   40012   | Akış Hız SP (LOW)      | UINT16 | —     | RW
       |           |   → FLOAT32 Big-Endian  |        |       |
───────────────────────────────────────────────────────────────────

INPUT REGISTERS — FC04 OKU (salt okunur)
───────────────────────────────────────────────────────────────────
IR Adr | Belge Ref | Değişken               | Tip    | Ölçek
───────|-----------|------------------------|--------|-------
  0    |   30001   | Gerçek Hız             | UINT16 | ×10
  1    |   30002   | Gerçek Sıcaklık        | UINT16 | ×10
  2    |   30003   | Gerçek Basınç          | UINT16 | ×100
  3    |   30004   | Durum Register         | UINT16 | bit
       |           |   Bit 0 = Çalışıyor    |        |
       |           |   Bit 1 = Hata var     |        |
       |           |   Bit 2 = Setpoint'te  |        |
  4    |   30005   | Üretim Sayacı (HIGH)   | UINT16 | —
  5    |   30006   | Üretim Sayacı (LOW)    | UINT16 | —
       |           |   → UINT32 Big-Endian  |        |
───────────────────────────────────────────────────────────────────

COILS — FC01 OKU / FC05,15 YAZ
───────────────────────────────────────────────────────────────────
Coil   | Belge Ref | Değişken
───────|-----------|-------------------------------
  0    |   00001   | Motor Start Komutu
  1    |   00002   | Motor Stop Komutu
  2    |   00003   | Reset Komutu

DISCRETE INPUTS — FC02 OKU (salt okunur)
───────────────────────────────────────────────────────────────────
DI     | Belge Ref | Değişken
───────|-----------|-------------------------------
  0    |   10001   | Makine Çalışıyor
  1    |   10002   | Hata Var
  2    |   10003   | Kapı Açık
═══════════════════════════════════════════════════════════════════
```

## Örnekler

### Örnek 1: Float Okuma ve Yazma — Tam Kod

```python
import struct
from pymodbus.client import ModbusTcpClient

def read_float32_be(client, address, slave=1):
    """Big-Endian (AB CD) float32 oku."""
    result = client.read_holding_registers(address, 2, slave=slave)
    if result.isError():
        raise Exception(f"Read error: {result}")
    regs = result.registers
    raw = struct.pack('>HH', regs[0], regs[1])
    return struct.unpack('>f', raw)[0]

def write_float32_be(client, address, value, slave=1):
    """Big-Endian (AB CD) float32 yaz."""
    raw = struct.pack('>f', value)
    hw = struct.unpack('>H', raw[0:2])[0]
    lw = struct.unpack('>H', raw[2:4])[0]
    return client.write_registers(address, [hw, lw], slave=slave)

with ModbusTcpClient('192.168.1.100', port=502) as client:
    # Sıcaklık setpoint'i yaz (HR 10-11 = float32)
    write_float32_be(client, address=10, value=85.5)
    
    # Geri oku ve doğrula
    temp = read_float32_be(client, address=10)
    print(f"Sıcaklık Setpoint: {temp:.1f} °C")  # 85.5 °C
```

### Örnek 2: Komut Register Bit Manipülasyonu

```python
def send_command(client, command_bits, slave=1, reg_address=3):
    """
    Bit maskeli komut register'ı.
    command_bits: dict {0: True/False, 1: True/False, ...}
    """
    # Mevcut değeri oku
    result = client.read_holding_registers(reg_address, 1, slave=slave)
    current = result.registers[0]
    
    # Bitleri güncelle
    new_value = current
    for bit_pos, state in command_bits.items():
        if state:
            new_value |= (1 << bit_pos)   # Bit set
        else:
            new_value &= ~(1 << bit_pos)  # Bit clear
    
    client.write_register(reg_address, new_value, slave=slave)
    return new_value

# Start komutu (bit 0 = 1)
send_command(client, {0: True, 1: False, 2: False})

# Stop komutu (bit 1 = 1)
send_command(client, {0: False, 1: True, 2: False})

# Reset (bit 2 = 1)
send_command(client, {2: True})
# Kısa gecikme sonrası sıfırla
import time; time.sleep(0.2)
send_command(client, {2: False})
```

### Örnek 3: Durum Register Bit Okuma

```python
def parse_status_register(value):
    """Durum register bitlerini çözümle."""
    return {
        'running':     bool(value & 0x0001),   # Bit 0
        'fault':       bool(value & 0x0002),   # Bit 1
        'at_setpoint': bool(value & 0x0004),   # Bit 2
        'in_setup':    bool(value & 0x0008),   # Bit 3
    }

result = client.read_input_registers(3, 1, slave=1)
status = parse_status_register(result.registers[0])

print(f"Çalışıyor: {status['running']}")
print(f"Hata: {status['fault']}")
print(f"Setpoint'te: {status['at_setpoint']}")
```

### Örnek 4: Adres Dönüşüm Fonksiyonu

```python
def modbus_ref_to_address(ref: str) -> tuple[str, int]:
    """
    Modbus referans notasyonunu (40001 gibi) tip ve protokol adresine dönüştür.
    
    '40001' → ('holding', 0)
    '30010' → ('input', 9)
    '00001' → ('coil', 0)
    '10001' → ('discrete', 0)
    """
    ref_int = int(ref)
    
    if 40001 <= ref_int <= 49999:
        return ('holding', ref_int - 40001)
    elif 30001 <= ref_int <= 39999:
        return ('input', ref_int - 30001)
    elif 1 <= ref_int <= 9999:
        return ('coil', ref_int - 1)
    elif 10001 <= ref_int <= 19999:
        return ('discrete', ref_int - 10001)
    else:
        raise ValueError(f"Geçersiz Modbus referansı: {ref}")

# Test
print(modbus_ref_to_address('40001'))  # ('holding', 0)
print(modbus_ref_to_address('40101'))  # ('holding', 100)
print(modbus_ref_to_address('30001'))  # ('input', 0)
```

## Sık Yapılan Hatalar

### Hata 1: Adres Kayması (Off-by-One)

```
Belge: "Temperature at register 40101"
Kod  : client.read_holding_registers(101, 1, slave=1)  # ❌ YANLIŞ → 40102 okunur

Doğru:
  40101 → protocol address = 40101 - 40001 = 100
  client.read_holding_registers(100, 1, slave=1)  # ✓
```

### Hata 2: Float Byte Order Varsayımı

```
Cihaz belgesi "32-bit float, 2 registers" yazıyor.
Byte order belirtilmemiş.
Kod Big-Endian varsayıyor → Anlamsız değer geliyor (ör. 3.14 yerine -1.234e18).

Çözüm: 
  1. Bilinen bir değeri (ör. setpoint=100.0) yaz.
  2. 4 byte'ı hex olarak oku.
  3. 100.0 = 0x42C80000 → hangi sırayla geldiğine bak.
  4. struct.pack ile tüm 4 varyantı dene.
```

### Hata 3: Scaling Faktörünü Kaçırmak

```
Belge: "Temperature: ×10 resolution"
Okunan değer: 856
Yorum: 856°C ← YANLIŞ

Doğru: 856 / 10 = 85.6°C

Register haritasında ölçek her zaman belirtilmeli.
Kod:  temp_c = registers[0] / 10.0
```

### Hata 4: Üretim Sayacını Tek Register'da Okumak

```
Üretim sayacı büyük olduğunda 65535'i aşar → overflow.
Register haritasında DWORD (2 register) olarak tanımlanmış ama
kod yalnızca 1 register okuyor.

Sonuç: Sayaç 65535'e ulaşınca sıfırlanmış görünüyor.

Çözüm:
count = (regs[0] << 16) | regs[1]  # 32-bit birleştirme
```

## Gerçek Proje Notları

**Not 1 — 0-Tabanlı Adres Felaketi**  
Bir enerji sayacı entegrasyonunda register haritası "HR 40001 = Voltage Phase A" diyordu. Kod `address=40001` yazıldı. Okunan veri: tamamen yanlış. Sorun: pymodbus 0-tabanlı, `address=40001` = protokol adres 40001 = register 40002! Doğru: `address=0`. 2 saatlik debug, 1 satır değişiklik.

**Not 2 — Float Byte Order Discovery**  
Bir frekans konvertörü belgesi "32-bit float, IEEE 754" yazıyordu, byte order yoktu. Test: setpoint=10.0 yazdık. Geri okunan 2 register: 0x0000, 0x4120. Big-Endian 10.0 = 0x41200000. Yani: HR[0]=0x0000 (Low), HR[1]=0x4120 (High) → Mixed-LE varyantı. Struct kodu buna göre ayarlandı.

**Not 3 — Tüm Veriyi Holding Register'a Koyan Cihazlar**  
Çoğu Çin üretimi cihaz Input Register kullanmıyor; hem ölçümleri hem parametreleri Holding Register'a (4x) koyuyor. Belge "HR 40001-40100" ve FC03 kullan diyor. Bu Modbus standardını çiğniyor ama pratikte çok yaygın. CODESYS'te slave tasarlarken bu baskıyı bilmek faydalı.

## İlgili Konular

```
knowledge/protocols/modbus-tcp/
├── 01_protocol_basics.md        → MBAP header ve frame yapısı
├── 03_function_codes.md         → Register tiplerini kullanan FC'ler
├── 04_codesys_slave_config.md   → CODESYS'te register eşleme
└── 05_client_implementations.md → Python'da register okuma/yazma

Araçlar:
  ModbusSimulator → Register haritası test aracı
  Modbus Poll     → GUI master — register değerlerini görsel izle
  struct paketi   → Python'da byte/float dönüşümü için
```
