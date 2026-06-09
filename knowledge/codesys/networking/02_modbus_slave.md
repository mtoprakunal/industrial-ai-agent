---
KONU        : CODESYS Modbus TCP Slave Kurulumu
KATEGORİ    : codesys
ALT_KATEGORI: networking
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Modbus/_mod_edt_slave_com_channel.html"
    başlık: "CODESYS Online Help — Modbus Server Channel Configuration"
    güvenilirlik: resmi
  - url: "https://www.plctalk.net/forums/threads/codesys-modbus-tcp-server.144313/"
    başlık: "PLCtalk — CODESYS Modbus TCP Server Tartışması"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Runtime/thread/607bfea988/"
    başlık: "CODESYS Forge — Modbus TCP Supported Functions"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Engineering/thread/63039dcd4f/"
    başlık: "CODESYS Forge — Modbus Register Read/Write Same Variable"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_opcua_server.md"
    ilişki: alternatif
  - konu: "knowledge/codesys/programming/02_gvl_design.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Modbus protokol temelleri: Function Code, Register adresleme"
  - "CODESYS Device Tree ve I/O Mapping (fundamentals/02_project_structure.md)"
  - "GVL tasarımı (programming/02_gvl_design.md)"
ÇELİŞKİLER :
  - kaynak: "Modbus adresleme konvansiyonu: 0-tabanlı vs 1-tabanlı"
    konu: "Bazı HMI/SCADA'lar register adresini 0'dan, bazıları 1'den başlatır"
    çözüm: >
      Modbus protokolü 0-tabanlı (0x0000) çalışır.
      Ancak pek çok HMI ve SCADA programlama aracı kullanıcıya
      1-tabanlı adres gösterir (register 1 = adres 0x0000).
      Bağlantı kurulurken istemci yazılımının konvansiyonu sorgulanmalı
      ve register haritası buna göre tasarlanmalı.
  - kaynak: "REAL değer Modbus üzerinden gönderme"
    konu: "Modbus yalnızca 16-bit integer taşır; REAL için özel dönüşüm gerekir"
    çözüm: >
      REAL (32-bit float) iki WORD register'a bölünerek gönderilir.
      Byte order (Big Endian / Little Endian / swap) istemci ve sunucu
      arasında eşleşmeli. Anlaşmak için önce test değeri gönderilip kontrol edilmeli.
---

## Özün Ne

Modbus TCP, endüstriyel otomasyonun en köklü ve en yaygın iletişim protokolüdür. OPC UA kadar zengin değildir ama kurulumu dakikalar alır, hemen hemen her HMI ve SCADA tarafından desteklenir ve düşük kaynaklı sistemlerde bile çalışır. CODESYS'te Modbus TCP Slave kurulumu; donanım değişkeni gibi Device Tree'ye eklenir, I/O Mapping ile GVL değişkenlerine bağlanır. Register haritası net tasarlanmadığında hata ayıklamak saatler alabilir; bu belge o tasarım sürecini adım adım ele alır.

## Nasıl Çalışır

### Modbus Veri Modeli

Modbus dört veri türü tanımlar:

```
Veri Türü          Erişim     Boyut  FC     Adres Aralığı
─────────────────────────────────────────────────────────────
Coil               Okuma+Yaz  1-bit  01,05,15  00001-09999
Discrete Input     Yalnız Oku 1-bit  02        10001-19999
Holding Register   Okuma+Yaz  16-bit 03,06,16  40001-49999
Input Register     Yalnız Oku 16-bit 04        30001-39999
```

**CODESYS Slave olarak işleyişi:**

```
Modbus Master (HMI / SCADA / Python script)
    │ FC03: Read Holding Registers (addr=0, count=10)
    ▼
CODESYS Modbus TCP Slave (port 502)
    │ I/O Mapping
    ▼
GVL_Modbus.aHoldingRegs[0..9]  ← Her register bir WORD değişkeni
```

### Function Code Referansı

| FC | İşlem | Veri Türü | Açıklama |
|---|---|---|---|
| 01 | Read Coils | Coil | Boolean okuma |
| 02 | Read Discrete Inputs | Discrete Input | Boolean okuma (salt) |
| 03 | Read Holding Registers | Holding Register | 16-bit okuma/yazma |
| 04 | Read Input Registers | Input Register | 16-bit salt okuma |
| 05 | Write Single Coil | Coil | Tek boolean yazma |
| 06 | Write Single Register | Holding Register | Tek 16-bit yazma |
| 15 | Write Multiple Coils | Coil | Çoklu boolean yazma |
| 16 | Write Multiple Registers | Holding Register | Çoklu 16-bit yazma |

### CODESYS'te Slave Rolü

CODESYS Modbus TCP **Slave** (sunucu) rolündedir: HMI/SCADA'nın sorguladığı taraf PLC'dir. PLC aktif veri göndermez; istendiğinde yanıtlar.

```
Slave = Sunucu = Dinleyen
Master = İstemci = Sorgulayan

PLC (Slave, dinler, port 502)  ←── Sorgular ── HMI (Master)
PLC (Slave, yanıtlar)          ───── Yanıtlar → HMI (Master)
```

## Pratikte Nasıl Kullanılır

### Adım 1: Modbus TCP Slave Cihazını Ekle

```
Device Tree → Ethernet arayüzü (sağ tık) → Add Device →
    Modbus → ModbusTCP Slave Device
    
Alternatif isimler (platforma göre):
  Modbus TCP Slave
  ModbusTCP_Slave
  CODESYS Modbus TCP Server
```

### Adım 2: Genel Yapılandırma

```
ModbusTCP Slave Device (çift tık) → General sekmesi

Port Number       : 502          (standart Modbus TCP portu)
Coil Count        : 128          (Boolean değişken sayısı)
Discrete Input Count: 64
Holding Register Count: 200      (16-bit okuma/yazma register sayısı)
Input Register Count: 100        (16-bit salt okuma register sayısı)
```

### Adım 3: GVL Hazırla

Modbus üzerinden paylaşılacak değişkenler için özel GVL:

```iecst
{attribute 'qualified_only'}
VAR_GLOBAL
    (* ================================================ *)
    (* HOLDING REGISTERS (Master okur ve yazar)          *)
    (* ================================================ *)
    (* Blok 1: Setpoint ve parametreler (HR 0..9)        *)
    wSetpoint_Speed    : WORD;      (* HR 0: Hız setpoint × 10 (ör. 500 = 50.0 m/dk) *)
    wSetpoint_Temp     : WORD;      (* HR 1: Sıcaklık setpoint × 10 *)
    wRecipeID          : WORD;      (* HR 2: Aktif reçete numarası *)
    wReserved_HR3      : WORD;      (* HR 3: Rezerve — ileride kullanım *)
    wReserved_HR4      : WORD;      (* HR 4: Rezerve *)
    
    (* Blok 2: Komutlar (HR 10..19) *)
    wCommandRegister   : WORD;      (* HR 10: Bit maskeli komut register'ı *)
    wAlarmAckMask      : WORD;      (* HR 11: Alarm onay bit maskesi *)
    
    (* ================================================ *)
    (* INPUT REGISTERS (Master yalnızca okur)            *)
    (* ================================================ *)
    (* Blok 1: Proses değerleri (IR 0..9) *)
    wActual_Speed      : WORD;      (* IR 0: Gerçek hız × 10 *)
    wActual_Temp       : WORD;      (* IR 1: Gerçek sıcaklık × 10 *)
    wActual_Pressure   : WORD;      (* IR 2: Gerçek basınç × 100 *)
    wProductionCount_L : WORD;      (* IR 3: Üretim sayacı Low WORD *)
    wProductionCount_H : WORD;      (* IR 4: Üretim sayacı High WORD *)
    
    (* Blok 2: Durum (IR 10..19) *)
    wStatusRegister    : WORD;      (* IR 10: Bit maskeli durum *)
    wAlarmRegister     : WORD;      (* IR 11: Aktif alarmlar bit maskesi *)
    
    (* ================================================ *)
    (* COILS (Master okur ve yazar — tek bit)            *)
    (* ================================================ *)
    xCoil_StartCmd     : BOOL;      (* Coil 0: Başlatma komutu *)
    xCoil_StopCmd      : BOOL;      (* Coil 1: Durdurma komutu *)
    xCoil_Reset        : BOOL;      (* Coil 2: Reset komutu *)
    
    (* ================================================ *)
    (* DISCRETE INPUTS (Master yalnızca okur — tek bit)  *)
    (* ================================================ *)
    xDI_Running        : BOOL;      (* DI 0: Makine çalışıyor *)
    xDI_Fault          : BOOL;      (* DI 1: Arıza var *)
    xDI_AtSetpoint     : BOOL;      (* DI 2: Setpoint'te *)
    xDI_DoorOpen       : BOOL;      (* DI 3: Kapı açık *)
END_VAR
```

### Adım 4: I/O Mapping

```
ModbusTCP Slave Device → I/O Mapping sekmesi

Holding Registers:
  Offset 0  ↔ GVL_Modbus.wSetpoint_Speed
  Offset 1  ↔ GVL_Modbus.wSetpoint_Temp
  Offset 2  ↔ GVL_Modbus.wRecipeID
  Offset 10 ↔ GVL_Modbus.wCommandRegister
  Offset 11 ↔ GVL_Modbus.wAlarmAckMask

Input Registers:
  Offset 0  ↔ GVL_Modbus.wActual_Speed
  Offset 1  ↔ GVL_Modbus.wActual_Temp
  Offset 10 ↔ GVL_Modbus.wStatusRegister
  Offset 11 ↔ GVL_Modbus.wAlarmRegister

Coils:
  Offset 0  ↔ GVL_Modbus.xCoil_StartCmd
  Offset 1  ↔ GVL_Modbus.xCoil_StopCmd

Discrete Inputs:
  Offset 0  ↔ GVL_Modbus.xDI_Running
  Offset 1  ↔ GVL_Modbus.xDI_Fault
```

### Adım 5: PLC Kodunda Register Güncelleme

Modbus register'ları, kontrol döngüsünün sonunda güncellenmeli:

```iecst
(* PRG_ModbusUpdate — Task_Slow içinde çağrılır (100ms, Prio:5) *)
PROGRAM PRG_ModbusUpdate

(* INPUT REGISTERS → Kontrol değerlerinden güncelle *)
(* REAL → WORD dönüşümü: ×10 ile tamsayıya çevir *)
GVL_Modbus.wActual_Speed   := REAL_TO_WORD(GVL_Diagnostics.rActualSpeed   * 10.0);
GVL_Modbus.wActual_Temp    := REAL_TO_WORD(GVL_Diagnostics.rActualTemp    * 10.0);
GVL_Modbus.wActual_Pressure:= REAL_TO_WORD(GVL_Diagnostics.rPressure_Bar  * 100.0);

(* DWORD → iki WORD olarak böl *)
GVL_Modbus.wProductionCount_L := WORD(GVL_Diagnostics.dwProductionCount AND 16#FFFF);
GVL_Modbus.wProductionCount_H := WORD(SHR(GVL_Diagnostics.dwProductionCount, 16));

(* Status register — bit maskeleme *)
GVL_Modbus.wStatusRegister := 0;
IF GVL_State.xRunning   THEN GVL_Modbus.wStatusRegister := GVL_Modbus.wStatusRegister OR 16#0001; END_IF
IF GVL_State.xAtSetpoint THEN GVL_Modbus.wStatusRegister := GVL_Modbus.wStatusRegister OR 16#0002; END_IF
IF GVL_State.xInSetup   THEN GVL_Modbus.wStatusRegister := GVL_Modbus.wStatusRegister OR 16#0004; END_IF

(* Alarm register *)
GVL_Modbus.wAlarmRegister := 0;
IF GVL_Alarms.xMotorFault      THEN GVL_Modbus.wAlarmRegister := GVL_Modbus.wAlarmRegister OR 16#0001; END_IF
IF GVL_Alarms.xTempOverRange   THEN GVL_Modbus.wAlarmRegister := GVL_Modbus.wAlarmRegister OR 16#0002; END_IF
IF GVL_Alarms.xPressureHigh    THEN GVL_Modbus.wAlarmRegister := GVL_Modbus.wAlarmRegister OR 16#0004; END_IF

(* Discrete Inputs *)
GVL_Modbus.xDI_Running    := GVL_State.xRunning;
GVL_Modbus.xDI_Fault      := GVL_Alarms.xAnyActiveAlarm;
GVL_Modbus.xDI_AtSetpoint := GVL_State.xAtSetpoint;

(* HOLDING REGISTERS → PLC parametrelerine aktar *)
(* Master'ın yazdığı setpoint değerlerini kontrol koduna ver *)
GVL_Params.rSpeedSetpoint := WORD_TO_REAL(GVL_Modbus.wSetpoint_Speed) / 10.0;
GVL_Params.rTempSetpoint  := WORD_TO_REAL(GVL_Modbus.wSetpoint_Temp)  / 10.0;

(* Command register — bit test et ve komut ver *)
IF (GVL_Modbus.wCommandRegister AND 16#0001) <> 0 THEN
    GVL_HMI.xStartCmd := TRUE;
    GVL_Modbus.wCommandRegister := GVL_Modbus.wCommandRegister AND NOT 16#0001;  (* Biti sıfırla *)
END_IF
```

### Adım 6: Bağlantı Testi

```python
# Python pymodbus ile test
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('192.168.1.100', port=502)
client.connect()

# Holding Register 0'ı oku (hız setpoint)
result = client.read_holding_registers(address=0, count=10, slave=1)
print(f"HR[0] = {result.registers[0] / 10.0} m/dk")  # ×10 dönüşümü geri al

# Input Register 0'ı oku (gerçek hız)
result = client.read_input_registers(address=0, count=5, slave=1)
print(f"IR[0] = {result.registers[0] / 10.0} m/dk")

# HR 0'a yaz (yeni setpoint: 45.5 m/dk → 455)
client.write_register(address=0, value=455, slave=1)

# Coil 0'ı oku (start komutu)
result = client.read_coils(address=0, count=4, slave=1)
print(f"Start: {result.bits[0]}, Stop: {result.bits[1]}")

client.close()
```

## Örnekler

### Örnek 1: Register Haritası Dokümantasyonu

Her proje için Modbus register haritası bir belgede tutulmalıdır:

```
MODBUS TCP SLAVE REGISTER HARİTASI
Cihaz: Konveyörlü Paketleme Hattı PLC
IP: 192.168.1.100, Port: 502, Unit ID: 1

HOLDING REGISTERS (FC03 oku / FC06,16 yaz)
────────────────────────────────────────────────────────────────────────
HR Addr | Değişken         | Birim | Ölçek | Açıklama
────────────────────────────────────────────────────────────────────────
   0    | Hız Setpoint     | m/dk  | ×10   | 0-500 → 0.0-50.0 m/dk
   1    | Sıcaklık SP      | °C    | ×10   | 0-2500 → 0.0-250.0 °C
   2    | Reçete No        | -     | 1     | 0=Yok, 1-10=Reçete
   3..9 | Rezerve          | -     | -     | İleride kullanım
  10    | Komut Register   | -     | bit   | Bit 0=Start, 1=Stop, 2=Reset
  11    | Alarm Onay       | -     | bit   | Bit 0=Motor reset, 1=Temp reset

INPUT REGISTERS (FC04 oku — salt okunur)
────────────────────────────────────────────────────────────────────────
IR Addr | Değişken         | Birim | Ölçek | Açıklama
────────────────────────────────────────────────────────────────────────
   0    | Gerçek Hız       | m/dk  | ×10   | 0-500 → 0.0-50.0
   1    | Gerçek Sıcaklık  | °C    | ×10   | 0-3000 → 0.0-300.0
   2    | Gerçek Basınç    | bar   | ×100  | 0-1000 → 0.0-10.0
   3    | Sayaç (Low)      | adet  | 1     | DWORD'un düşük 16-bit
   4    | Sayaç (High)     | adet  | 1     | DWORD'un yüksek 16-bit
  10    | Durum Register   | -     | bit   | Bit 0=Running, 1=AtSP, 2=InSetup
  11    | Alarm Register   | -     | bit   | Bit 0=Motor, 1=Temp, 2=Pressure

COILS (FC01 oku / FC05,15 yaz)
────────────────────────────────────────────────────────────────────────
Coil Addr | Değişken    | Açıklama
────────────────────────────────────────────────────────────────────────
    0     | Start Cmd   | TRUE = Başlat komutu
    1     | Stop Cmd    | TRUE = Durdur komutu
    2     | Reset Cmd   | TRUE = Reset komutu (Rising edge)

DISCRETE INPUTS (FC02 oku — salt okunur)
────────────────────────────────────────────────────────────────────────
DI Addr | Değişken    | Açıklama
────────────────────────────────────────────────────────────────────────
   0    | Running     | Makine çalışıyor
   1    | Fault       | Aktif alarm var
   2    | AtSetpoint  | Setpoint'te
   3    | DoorOpen    | Kapı açık
```

### Örnek 2: REAL Değer — İki Register ile Gönderme

```iecst
(* IEEE 754 REAL → 2 WORD dönüşümü *)
TYPE UNION_RealToWord :
UNION
    rValue  : REAL;
    aWords  : ARRAY[0..1] OF WORD;
END_UNION
END_TYPE

VAR
    uConverter : UNION_RealToWord;
END_VAR

(* Dönüşüm *)
uConverter.rValue := GVL_Diagnostics.rFlowRate;  (* ör. 3.14159 *)
GVL_Modbus.wFlowRate_L := uConverter.aWords[0];  (* Low WORD → IR 20 *)
GVL_Modbus.wFlowRate_H := uConverter.aWords[1];  (* High WORD → IR 21 *)

(* İstemci tarafında: *)
(* High WORD << 16 | Low WORD → IEEE 754 → float = 3.14159 *)
(* Ancak Byte Order (Endian) istemci-sunucu arasında eşleşmeli! *)
```

### Örnek 3: Komut Register Okuma

```iecst
(* Komut register'ını her döngüde işle *)
PROGRAM PRG_CommandProcessor
VAR
    wPrevCommandReg : WORD;   (* Önceki değer — sadece değişince işle *)
    fbStartEdge     : R_TRIG;
    fbStopEdge      : R_TRIG;
END_VAR

(* Komut register değişti mi? *)
IF GVL_Modbus.wCommandRegister <> wPrevCommandReg THEN
    (* Bit 0: Start komutu *)
    IF (GVL_Modbus.wCommandRegister AND 16#0001) <> 0 THEN
        GVL_HMI.xStartCmd := TRUE;
    END_IF
    
    (* Bit 1: Stop komutu *)
    IF (GVL_Modbus.wCommandRegister AND 16#0002) <> 0 THEN
        GVL_HMI.xStopCmd := TRUE;
    END_IF
    
    (* Bit 2: Reset komutu *)
    IF (GVL_Modbus.wCommandRegister AND 16#0004) <> 0 THEN
        GVL_HMI.xFaultReset := TRUE;
    END_IF
    
    wPrevCommandReg := GVL_Modbus.wCommandRegister;
    
    (* İşlendikten sonra sıfırla *)
    GVL_Modbus.wCommandRegister := 0;
END_IF
```

## Sık Yapılan Hatalar

### Hata 1: Register Adresi 0-tabanlı mı 1-tabanlı mı?

```
SCADA programı: "HR 40001" olarak register yazılmış.
PLC tarafında: I/O Mapping Offset 0.

Sorun: SCADA "40001" derken 0-adresini mi yoksa 1-adresini mi kastediyor?
Modbus protokolü: 0-tabanlı (0x0000 = 40001 gösterimi)
SCADA genellikle: 40001 = Offset 0 gösterimi

Test: Tek bir bilinen değeri (ör. WORD = 1234) HR 0'a yaz → SCADA'da kontrol et.
Eğer 40001'de görünüyorsa → SCADA 40001 = Offset 0 kullanıyor.
```

### Hata 2: Slave ID (Unit ID) Yanlış

```
Semptom: Bağlantı kuruluyor ama veri gelmiyor.
Neden  : İstemci Unit ID 1 ile sorguluyor, PLC Unit ID 0 ile yanıtlıyor.
Çözüm  : ModbusTCP Slave Device → General → Unit ID ayarını kontrol et.
          İstemci (SCADA/HMI) ile aynı Unit ID kullanılmalı (genellikle 1).
```

### Hata 3: Holding Register'a Yazılan Değer Kayboldu

```
Neden  : Kontrol kodu her döngüde Modbus register'ını varsayılan değere yazıyor.
Örnek:
  Her döngüde: GVL_Modbus.wSetpoint_Speed := REAL_TO_WORD(rDefaultSpeed * 10);
  Master 455 yazar → Bir döngü sonra kod eski değere eziyor

Çözüm  : Holding Register → PLC parametresi akışı tek yönlü olmalı.
          PLC kontrol kodu Holding Register'ı asla ezmemeli.
          Holding Register'dan GVL_Params'a copy yapılır, ters değil.
```

### Hata 4: REAL → WORD Dönüşümünde Precision Kaybı

```iecst
(* ❌ Yanlış: Sadece integer kısmını al *)
GVL_Modbus.wTemp := REAL_TO_WORD(rTemperature);
(* 98.7°C → 98 WORD → İstemci 98 okur → Bilgi kaybı *)

(* ✅ Doğru: Ölçeklendirme ile precision koru *)
GVL_Modbus.wTemp := REAL_TO_WORD(rTemperature * 10.0);
(* 98.7°C → 987 WORD → İstemci 987/10 = 98.7 → Tam bilgi *)

(* Register haritasında ölçek belirt: IR 1 = Sıcaklık ×10 *)
```

### Hata 5: Bus Cycle Task Ayarlanmamış

```
Semptom: Modbus slave eklenmiş ama I/O Mapping güncellenmiyor.
Neden  : Slave device'ın bus cycle task'ı atanmamış.
Çözüm  : ModbusTCP Slave Device → I/O Mapping →
          Bus Cycle Task: Task_Slow (veya Task_Control)
          Bu task her çalıştığında Modbus register'ları güncellenir.
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**Modbus TCP Tercih Et:**
- Eski SCADA/HMI sistemi yalnızca Modbus destekliyor
- Hızlı entegrasyon, minimum yapılandırma
- Sınırlı veri noktası sayısı (< 200 register yeterli)
- Kaynak kısıtlı sistemler
- İstemci tarafında Modbus dışı destek yok

**Modbus TCP Tercih Etme:**
- Güvenlik gereksinimi var → OPC UA (şifreli iletişim)
- Zengin meta-data, tip bilgisi gerekiyor → OPC UA
- 1000+ değişken paylaşılacak → OPC UA daha verimli
- Dinamik veri modeli → OPC UA
- Gerçek zamanlı event-driven bildirim → OPC UA Subscription

## Gerçek Proje Notları

**Not 1 — 0 vs 1 Tabanlı Adres Felaketi**  
Bir HMI sistemi "HR 1" adresine yazıyor, PLC offset 0 bekliyor — veri kayboldu. HMI "HR 1" ile offset 0'ı kastediyor (1-tabanlı gösterim), PLC "offset 0" ile adres 40001'i kastediyor. Test değeri (WORD = 9999) konulup HMI'da kontrol edildi: HR 0'da görünüyordu. HMI'nın 1-tabanlı gösterimi kullandığı anlaşıldı; register haritası 1'den başlayacak şekilde yeniden belgelendi.

**Not 2 — Komut Bit'i Silinmediğinde Sürekli Start**  
HMI "Start" komutunu Coil 0'a TRUE yazdı. PLC Coil 0'ı Start komutu olarak işledi — motor çalıştı. Ama Coil 0 hâlâ TRUE'du. Her Modbus poll döngüsünde (100ms) PLC yeniden Start komutu alıyordu. Motor durdurulamıyordu. Çözüm: Start Coil → R_TRIG edge detection + HMI'nın yazdıktan 100ms sonra FALSE yazması. Daha sağlam çözüm: Command Register yaklaşımı (yazılır → işlenir → PLC sıfırlar).

**Not 3 — REAL İki Register Byte Order Sorunu**  
REAL değer iki WORD olarak gönderildi. Python istemci saçma değer okudu (ör. 3.14 yerine -5.2e10). Byte order (endian) uyuşmuyordu. PLC: `aWords[0]` = Low, `aWords[1]` = High. Python: `struct.unpack('>f', bytes)` büyük endian varsayıyordu. Çözüm: Python tarafında `struct.unpack('<f', ...)` küçük endian ile çözüldü.

**Not 4 — Register Haritası Olmadan Devreye Alma**  
Bir projede register haritası dokümante edilmeden PLC geliştiricisi ile SCADA entegratörü ayrı çalıştı. Devreye alma günü SCADA'nın register beklentisi ile PLC haritası uyuşmadı; 2 günlük düzeltme. Sonraki projelerde register haritası, proje başında tek sayfalık tablo olarak hazırlandı ve her iki tarafın onayına sunuldu.

**Not 5 — DWORD'un İki WORD'a Bölünmesinde Tutarsızlık (Word Tearing)**  
Üretim sayacı (DWORD) iki register'a `_L` ve `_H` olarak bölündü. SCADA bazen saçma değerler okudu: sayaç 65535→65536 geçişinde Low=0 ama High henüz güncellenmemişti — master, Low'u yeni High'ı eski okudu (ör. 0 yerine 4294901760). Neden: master iki register'ı iki ayrı FC03 ile okudu, arada PLC güncelledi. Çözüm: ikisini **tek FC03 isteğinde** (count=2) oku — Modbus tek istek içindeki register'ları atomik döndürür. Ya da bayrak/çift-okuma ile tutarlılık doğrula. Ders: çok-register değerlerde "word tearing" gerçek bir risktir.

**Not 6 — Bus Cycle Task ve REAL Ölçek Gecikmesi**  
Modbus slave'in bus cycle task'ı Task_Slow'a (100ms) atanmıştı, ama register'ları güncelleyen `PRG_ModbusUpdate` Task_Control'de (10ms) çalışıyordu. Sonuç: GVL değişkeni 10ms'de güncelleniyor ama Modbus image'i 100ms'de senkronize oluyordu — master bazen 90ms eski veri okudu. Ders: Modbus image güncellemesi (bus cycle task) ile register'ları besleyen kod aynı/uyumlu task'ta olmalı; bus cycle task seçimi veri tazeliğini belirler.

**Not 7 — Coil Polarite ve Fail-Safe Belirsizliği**  
Master "Stop" komutunu Coil'e FALSE yazarak verdi (aktif-düşük mantık), ama PLC TRUE=stop bekliyordu. Bağlantı koptuğunda coil son değerinde kaldı — ne master yeni komut verebildi ne de PLC güvenli duruma geçti. Ders: Komut coil'lerinde polariteyi netleştir (tercihen aktif-yüksek + edge), ve **bağlantı timeout** (master N saniyedir poll etmiyorsa) ile fail-safe'e geç. Modbus'ta bağlantı denetimi yoktur; uygulama katmanında watchdog gerekir.

## Edge Case'ler ve Sistem Limitleri

### Modbus Protokol Sınırları

```
Sınır                              Değer                    Not
─────────────────────────────────────────────────────────────────────
Tek istekte register (FC03/04)     125 register             Aşılırsa istek reddedilir
Tek istekte register yazma (FC16)  123 register
Tek istekte coil (FC01/02)         2000 coil
Register boyutu                    16-bit (0-65535)         32-bit için 2 register
Unit ID (TCP)                      genelde yok sayılır       ama bazı master zorunlu kılar
Eşzamanlı bağlantı                 cihaza bağlı (~birkaç)   aşılırsa yeni bağlantı red
Bağlantı denetimi                  YOK (protokol seviyesi)   uygulama watchdog şart
```

### Veri Bütünlüğü Edge Case'leri

```
Word tearing (çok-register değer)   → tek FC isteğinde oku (atomik) veya çift-okuma doğrula
Endian (REAL/DWORD byte sırası)     → big/little/word-swap; test değeriyle doğrula
Signed vs unsigned register         → -1 mi 65535 mi? master yorumuna bağlı, belgele
Coil bağlantı kopunca               → son değerde kalır; fail-safe otomatik değil
0 vs 1 tabanlı adres                → 40001=offset 0 mı 1 mi? test ile doğrula
```

### Güvenlik: Modbus'ta Hiçbir Şey Yok

Modbus TCP'de **kimlik doğrulama, şifreleme, yetkilendirme yoktur**. Ağa erişen herkes register okuyup yazabilir — start coil'ine TRUE yazıp makineyi başlatabilir. Bu protokolün doğasıdır, bir bug değil. Korunma tamamen ağ seviyesindedir: izole VLAN, firewall, sadece güvenilen master IP'lerine izin. Güvenlik gereken yerde Modbus değil OPC UA kullanılmalı (bkz. _synthesis karar tablosu).

## Optimizasyon

### Register Haritası Düzeni: Bloklama

Master genelde ardışık register'ları tek istekte okur. Haritayı **mantıksal bloklar** halinde ve **boşluksuz** düzenlemek, master'ın tek FC03 ile çok veri okumasını sağlar:

```
✅ İyi: Telemetri IR 0-9 ardışık → tek FC04(0,10) ile hepsi
❌ Kötü: Telemetri IR 0, 50, 120, 200'e dağınık → 4 ayrı istek

Boşluk bırakma (rezerve) iyi; ama ilgili veriyi aynı blokta tut.
```

### REAL Ölçekleme vs İki Register

```
Düşük precision yeterli (±0.1)  → REAL×10 → tek WORD (ör. 98.7→987). Basit, atomik, az bant.
Tam precision gerekli           → IEEE754 iki WORD (UNION). Endian dikkat + word tearing riski.
```

Çoğu endüstriyel değer (sıcaklık, hız, basınç) için ölçeklenmiş tek WORD hem daha verimli hem word-tearing'den bağışıktır.

### Bus Cycle Task Seçimi

Modbus image, atanan **bus cycle task** her çalıştığında senkronize olur. Veri tazeliği bu task'ın cycle'ıdır. Çok hızlı task (1ms) gereksiz CPU yer; çok yavaş task (1s) eski veri sunar. Tipik: register besleyen kod ile aynı task (10-100ms). Bus cycle task atanmazsa I/O mapping hiç güncellenmez (Hata 5).

## Derin Teknik Detay

### Neden Slave = Sunucu, Master = İstemci?

Modbus terminolojisi kafa karıştırır: PLC genelde "üstün" gibi düşünülür ama Modbus'ta **Slave**'dir (pasif, yanıtlayan). Çünkü Modbus master-poll mimarisidir: master sorar, slave yanıtlar; slave kendiliğinden veri gönderemez. Bu, 1979'un seri hat (RS-485) dünyasından gelir — tek master, çok slave, master sırayla yoklar (polling). TCP'ye taşındığında isimler korundu ama "master=client, slave=server" eşlemesi eklendi. PLC'nin "yanıtlayan" rolde olması, kendi durumunu proaktif bildiremeyeceği anlamına gelir — bu yüzden MQTT (push) bulut için, Modbus (poll) SCADA için tercih edilir.

### Word Tearing: Atomiklik Probleminin Modbus Yüzü

DWORD/REAL'in iki register'a bölünmesindeki tutarsızlık (Not 5), task-structure/03 ve programming/02'deki **atomiklik** probleminin protokol seviyesindeki tezahürüdür. PLC içinde 32-bit değer atomik olsa bile, Modbus master onu iki ayrı 16-bit okuma ile alırsa arada güncelleme yarım değer üretir. Çözüm aynı felsefedir: değeri tek atomik işlemde oku (tek FC isteği) veya çift-tampon/doğrulama. Modbus'ın 16-bit register doğası, 32-bit dünyada bu tearing'i kaçınılmaz kılar.

### Holding Register Çift Yönlülüğü ve Tek-Yazar Kuralı

Holding Register hem master hem PLC tarafından yazılabilir — bu, programming/02'deki "tek-yazar" kuralını ihlal etme tuzağıdır (Hata 3). Bir HR'ı master setpoint için yazıyorsa, PLC kodu onu **asla ezmemeli** (yalnızca okur, GVL_Params'a kopyalar). Tersine, PLC'nin yazdığı bir telemetri register'ına master yazmamalı. Her register için tek yazar tanımlamak — tıpkı GVL'de olduğu gibi — Modbus haritasının sağlığının temelidir. Register haritası belgesinde her register'ın yönü (R/W sahibi) açıkça yazılmalı.

### Modbus'ın Kalıcılığı: Neden Hâlâ Her Yerde?

Modbus 1979'dan beri yaşıyor çünkü **radikal basit**: 4 veri tipi, ~8 function code, durumsuz istek-yanıt. Bu basitlik, en zayıf cihazda bile (8-bit mikrodenetleyici) çalışmasını sağlar ve 45 yıllık geriye uyumluluk verir. OPC UA'nın zenginliği (tip, güvenlik, model) aynı zamanda karmaşıklık ve kaynak maliyetidir. Modbus'ın "eksiklikleri" (güvenlik yok, 16-bit, poll-only) aslında basitliğinin bedelidir — ve bu basitlik onu evrensel kılan şeydir. Uzman, Modbus'ı "ilkel" diye küçümsemez; doğru yerde (basit, güvenilir, evrensel veri paylaşımı) en verimli araçtır.

## İlgili Konular

```
knowledge/codesys/networking/
├── 01_opcua_server.md        → Daha güvenli, daha zengin alternatif
├── 03_tcp_socket.md          → Özel protokol gerektiğinde
└── 04_mqtt_client.md         → IoT/bulut entegrasyonu

knowledge/codesys/programming/
└── 02_gvl_design.md          → GVL_Modbus tasarımı

Araçlar:
  Modbus Poll  → Masaüstü Modbus Master test aracı
  pymodbus     → Python ile test scripting
  QModMaster   → Açık kaynak GUI Modbus test aracı
  Wireshark    → Modbus TCP paket analizi
```
