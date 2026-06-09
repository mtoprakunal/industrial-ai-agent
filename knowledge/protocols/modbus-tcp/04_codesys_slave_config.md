---
KONU        : CODESYS Modbus TCP Slave Yapılandırması
KATEGORİ    : protocols
ALT_KATEGORI: modbus-tcp
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Modbus/_mod_edt_slave_com_channel.html"
    başlık: "CODESYS Online Help — Modbus Server Channel Configuration"
    güvenilirlik: resmi
  - url: "https://forge.codesys.com/forge/talk/Runtime/thread/607bfea988/"
    başlık: "CODESYS Forge — Modbus TCP Supported Functions"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Engineering/thread/63039dcd4f/"
    başlık: "CODESYS Forge — Modbus Register Read/Write Same Variable"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_protocol_basics.md"
    ilişki: gerektirir
  - konu: "02_register_model.md"
    ilişki: gerektirir
  - konu: "03_function_codes.md"
    ilişki: kullanır
  - konu: "knowledge/codesys/networking/02_modbus_slave.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "CODESYS Device Tree ve I/O Mapping (fundamentals/02_project_structure.md)"
  - "Modbus register modeli (02_register_model.md)"
  - "GVL tasarımı (programming/02_gvl_design.md)"
ÇELİŞKİLER :
  - kaynak: "Holding Register'a PLC kodu tarafından yazılabilir mi?"
    konu: "CODESYS Modbus Slave'de Holding Register, master tarafından yazılır; PLC kodu yazamaz"
    çözüm: >
      Modbus slave I/O mapping'de Holding Register → CODESYS değişkenine eşlenir.
      Master (HMI/SCADA) FC16 ile yazar → CODESYS değişkeni güncellenir.
      PLC kodu bu değişkeni okur, işler; ancak doğrudan üzerine yazamaz (override edilir).
      PLC'nin Holding Register'a yazması gerekiyorsa: Modbus Master olarak kendi kendine yaz
      (loopback) veya Input Register kullan (PLC yazar, master okur).
  - kaynak: "Birden fazla master aynı slave'e bağlanabilir mi?"
    konu: "Evet ama dikkatli olunmazsa register tutarsızlığı oluşur"
    çözüm: >
      Modbus TCP birden fazla eş zamanlı TCP bağlantısını destekler.
      Ancak her master aynı Holding Register'a yazabilir — son yazan kazanır.
      Tasarım: Her master'ın farklı register bloklarına yazma yetkisi olmalı.
      Ya da tek yazıcı (one-writer) prensibi uygulanmalı.
---

## Özün Ne

CODESYS'te Modbus TCP Slave kurmak, Device Tree'ye bir "donanım" eklemek gibi yapılır: Ethernet arayüzünün altına Modbus TCP Slave Device eklenir, register haritası ve I/O Mapping yapılandırılır, GVL değişkenlerine bağlanır. Bu belge, söz konusu yapılandırmanın her adımını, tüm parametre seçeneklerini ve gerçek projede karşılaşılan sorunları ele alır. `knowledge/codesys/networking/02_modbus_slave.md` belgesi giriş niteliğindedir; bu belge daha derin yapılandırma detaylarını kapsar.

## Nasıl Çalışır

### CODESYS Modbus TCP Slave Mimarisi

```
Ethernet Arayüzü (eth0, 192.168.1.100)
    │
    └── ModbusTCP_Slave_Device (port 502)
            │
            ├── Coil Area        : Coil[0..N]    ← FC01/05/15
            ├── Discrete Input   : DI[0..N]      ← FC02
            ├── Holding Register : HR[0..N]      ← FC03/06/16
            └── Input Register   : IR[0..N]      ← FC04
                    │
                    ├── I/O Mapping
                    │     Offset 0 → GVL_Modbus.wSpeedSetpoint
                    │     Offset 1 → GVL_Modbus.wTempSetpoint
                    │     ...
                    │
                    └── Bus Cycle Task: Task_Slow (100ms)
```

### Adım 1: ModbusTCP Slave Device Ekleme

```
Device Tree → Ethernet arayüzü (sağ tıkla) → Add Device

Arama: "Modbus" → "ModbusTCP_Slave_Device" (veya "Modbus TCP Slave")

Alternatif isimler platforma göre:
  Wago: "ModbusTCP_Slave"
  CODESYS Control: "ModbusTCP_Slave_Device"
  Raspberry Pi: "ModbusTCP_Slave"
```

### Adım 2: General Yapılandırması

```
ModbusTCP_Slave_Device (çift tık) → General sekmesi:

┌─────────────────────────────────────────────────────────┐
│  Genel Parametreler                                      │
├──────────────────────────────┬──────────────────────────┤
│ Port Number                  │ 502 (standart)           │
│ Unit ID                      │ 1 (master'ın kullanacağı)│
│ Coil Count                   │ 128                      │
│ Discrete Input Count         │ 64                       │
│ Holding Register Count       │ 200                      │
│ Input Register Count         │ 100                      │
│ Timeout (ms)                 │ 3000                     │
│ Allow Coil/DI Bit Area       │ ✓ (Discrete Bit Areas)   │
└──────────────────────────────┴──────────────────────────┘
```

**Boyut hesaplama:**
```
Holding Register Count = Gerçek ihtiyaç × 1.5 (yedek pay)
Örnek: 80 register kullanılacak → 120 ayarla

Küçük sayı: Master gereksiz adres isterse → Exception 0x02
Büyük sayı: Hafıza tüketimi minimal, sorun yok
```

**Discrete Bit Areas seçeneği:**
```
✓ İşaretli: Coil ve Discrete Input alanları ayrı
✗ İşaretsiz: Holding Register alanının bit görünümü olarak coil/DI erişimi
             (Bazı eski HMI'lar bu modu gerektirir)
```

### Adım 3: GVL Hazırlama

Tüm Modbus değişkenlerini tek bir GVL'de topla:

```iecst
{attribute 'qualified_only'}
VAR_GLOBAL
    (* ============================================================= *)
    (* HOLDING REGISTERS — Master tarafından yazılır, PLC okur       *)
    (* ============================================================= *)
    (* Blok 1: Setpointler (HR 0-9) *)
    wSpeedSetpoint_x10  : WORD;  (* HR 0: Hız SP ×10 (450=45.0m/dk) *)
    wTempSetpoint_x10   : WORD;  (* HR 1: Sıcaklık SP ×10 *)
    wRecipeID           : WORD;  (* HR 2: Aktif reçete no *)
    wModeSelect         : WORD;  (* HR 3: 0=Manuel, 1=Oto, 2=Test *)
    wReserved_HR4       : WORD;  (* HR 4: Rezerve *)
    wReserved_HR5       : WORD;  (* HR 5: Rezerve *)
    
    (* Blok 2: Komut Register (HR 10) *)
    wCommandRegister    : WORD;  (* HR 10: Bit maskeli komut *)
                                 (*   Bit 0 = Start          *)
                                 (*   Bit 1 = Stop           *)
                                 (*   Bit 2 = Reset          *)
    
    (* Blok 3: Float setpointler (HR 20-21) — IEEE 754 Big-Endian *)
    wFlowRate_H         : WORD;  (* HR 20: Akış hız SP (High Word) *)
    wFlowRate_L         : WORD;  (* HR 21: Akış hız SP (Low Word) *)
    
    (* ============================================================= *)
    (* INPUT REGISTERS — PLC tarafından yazılır, Master okur         *)
    (* ============================================================= *)
    (* Blok 1: Proses ölçümleri (IR 0-9) *)
    wActualSpeed_x10    : WORD;  (* IR 0: Gerçek hız ×10 *)
    wActualTemp_x10     : WORD;  (* IR 1: Gerçek sıcaklık ×10 *)
    wActualPressure_x100: WORD;  (* IR 2: Gerçek basınç ×100 *)
    wStatusWord         : WORD;  (* IR 3: Durum bit maskesi *)
                                 (*   Bit 0 = Çalışıyor     *)
                                 (*   Bit 1 = Hata var       *)
                                 (*   Bit 2 = Setpoint'te   *)
    
    (* Blok 2: Sayaçlar (IR 10-11) *)
    wProdCount_H        : WORD;  (* IR 10: Üretim sayacı (High) *)
    wProdCount_L        : WORD;  (* IR 11: Üretim sayacı (Low) *)
    
    (* Blok 3: Alarm register (IR 12) *)
    wAlarmRegister      : WORD;  (* IR 12: Aktif alarm bit maskesi *)
    
    (* ============================================================= *)
    (* COILS — Master tarafından yazılır (boolean komutlar)           *)
    (* ============================================================= *)
    xCoil_StartCmd      : BOOL;  (* Coil 0: Motor başlat *)
    xCoil_StopCmd       : BOOL;  (* Coil 1: Motor durdur *)
    xCoil_ResetFault    : BOOL;  (* Coil 2: Arıza reset *)
    
    (* ============================================================= *)
    (* DISCRETE INPUTS — PLC tarafından yazılır, Master okur         *)
    (* ============================================================= *)
    xDI_Running         : BOOL;  (* DI 0: Makine çalışıyor *)
    xDI_Fault           : BOOL;  (* DI 1: Aktif arıza *)
    xDI_DoorOpen        : BOOL;  (* DI 2: Kapı açık *)
    xDI_AtSetpoint      : BOOL;  (* DI 3: Setpoint'te *)
END_VAR
```

### Adım 4: I/O Mapping

```
ModbusTCP_Slave_Device → I/O Mapping sekmesi

Holding Registers:
┌────────┬────────────────────────────────┐
│ Offset │ Variable                        │
├────────┼────────────────────────────────┤
│   0    │ GVL_Modbus.wSpeedSetpoint_x10   │
│   1    │ GVL_Modbus.wTempSetpoint_x10    │
│   2    │ GVL_Modbus.wRecipeID            │
│   3    │ GVL_Modbus.wModeSelect          │
│   4    │ GVL_Modbus.wReserved_HR4        │
│   5    │ GVL_Modbus.wReserved_HR5        │
│  10    │ GVL_Modbus.wCommandRegister     │
│  20    │ GVL_Modbus.wFlowRate_H          │
│  21    │ GVL_Modbus.wFlowRate_L          │
└────────┴────────────────────────────────┘

Input Registers:
┌────────┬────────────────────────────────┐
│   0    │ GVL_Modbus.wActualSpeed_x10     │
│   1    │ GVL_Modbus.wActualTemp_x10      │
│   2    │ GVL_Modbus.wActualPressure_x100 │
│   3    │ GVL_Modbus.wStatusWord          │
│  10    │ GVL_Modbus.wProdCount_H         │
│  11    │ GVL_Modbus.wProdCount_L         │
│  12    │ GVL_Modbus.wAlarmRegister       │
└────────┴────────────────────────────────┘

Coils:
┌────────┬────────────────────────────────┐
│   0    │ GVL_Modbus.xCoil_StartCmd       │
│   1    │ GVL_Modbus.xCoil_StopCmd        │
│   2    │ GVL_Modbus.xCoil_ResetFault     │
└────────┴────────────────────────────────┘

Discrete Inputs:
┌────────┬────────────────────────────────┐
│   0    │ GVL_Modbus.xDI_Running          │
│   1    │ GVL_Modbus.xDI_Fault            │
│   2    │ GVL_Modbus.xDI_DoorOpen         │
│   3    │ GVL_Modbus.xDI_AtSetpoint       │
└────────┴────────────────────────────────┘
```

### Adım 5: Bus Cycle Task Ataması

```
I/O Mapping sekmesi → Bus Cycle Task: Task_Slow

Neden Task_Slow (100ms)?
  Modbus güncelleme her Task döngüsünde olur.
  Task_Control (10ms, Prio:2) → Modbus I/O güncelleme her 10ms = gereksiz yük.
  Task_Slow (100ms, Prio:5) → Modbus için yeterli, kontrol döngüsünü etkilemez.
  
  ⚠ Task_Slow yoksa en düşük öncelikli task'ı seç.
  ⚠ Freewheeling task da uygun ama timing garantisi yok.
```

### Adım 6: PLC Kodu — Register Güncelleme

Input Register (PLC → Master) ve Discrete Input değerlerini her döngüde güncelle:

```iecst
(* PRG_ModbusUpdate — Task_Slow içinde çağrılır *)
PROGRAM PRG_ModbusUpdate

(* ===== INPUT REGISTERS: PLC'den Master'a ===== *)

(* Hız: m/dk → ×10 integer *)
GVL_Modbus.wActualSpeed_x10 :=
    REAL_TO_WORD(GVL_Diagnostics.rActualSpeed * 10.0);

(* Sıcaklık *)
GVL_Modbus.wActualTemp_x10 :=
    REAL_TO_WORD(GVL_Diagnostics.rActualTemp * 10.0);

(* Basınç *)
GVL_Modbus.wActualPressure_x100 :=
    REAL_TO_WORD(GVL_Diagnostics.rPressure_Bar * 100.0);

(* Durum bit maskesi *)
GVL_Modbus.wStatusWord := 0;
IF GVL_State.xRunning    THEN GVL_Modbus.wStatusWord := GVL_Modbus.wStatusWord OR 16#0001; END_IF
IF GVL_Alarms.xAnyActive THEN GVL_Modbus.wStatusWord := GVL_Modbus.wStatusWord OR 16#0002; END_IF
IF GVL_State.xAtSetpoint THEN GVL_Modbus.wStatusWord := GVL_Modbus.wStatusWord OR 16#0004; END_IF

(* Üretim sayacı DWORD → 2 WORD *)
GVL_Modbus.wProdCount_H :=
    WORD(SHR(GVL_Diagnostics.dwProdCount, 16));
GVL_Modbus.wProdCount_L :=
    WORD(GVL_Diagnostics.dwProdCount AND 16#FFFF);

(* Alarm register — her alarm için bir bit *)
GVL_Modbus.wAlarmRegister := 0;
IF GVL_Alarms.xMotorFault    THEN GVL_Modbus.wAlarmRegister := GVL_Modbus.wAlarmRegister OR 16#0001; END_IF
IF GVL_Alarms.xTempOverRange THEN GVL_Modbus.wAlarmRegister := GVL_Modbus.wAlarmRegister OR 16#0002; END_IF
IF GVL_Alarms.xPressureHigh  THEN GVL_Modbus.wAlarmRegister := GVL_Modbus.wAlarmRegister OR 16#0004; END_IF

(* ===== DISCRETE INPUTS: PLC'den Master'a ===== *)
GVL_Modbus.xDI_Running    := GVL_State.xRunning;
GVL_Modbus.xDI_Fault      := GVL_Alarms.xAnyActive;
GVL_Modbus.xDI_DoorOpen   := GVL_IO.xDoorSensor;
GVL_Modbus.xDI_AtSetpoint := GVL_State.xAtSetpoint;

(* ===== HOLDING REGISTERS: Master'dan PLC'ye ===== *)
(* Master'ın yazdığı değerleri PLC parametrelerine aktar *)
(* NOT: Bu yön ASLA PLC → HR yazmamalı (master override eder) *)

GVL_Params.rSpeedSP :=
    WORD_TO_REAL(GVL_Modbus.wSpeedSetpoint_x10) / 10.0;
GVL_Params.rTempSP  :=
    WORD_TO_REAL(GVL_Modbus.wTempSetpoint_x10) / 10.0;
GVL_Params.nRecipeID :=
    WORD_TO_INT(GVL_Modbus.wRecipeID);

(* Float setpoint — iki register → IEEE 754 *)
VAR
    uConv : UNION
        rValue : REAL;
        aWords : ARRAY[0..1] OF WORD;
    END_UNION;
END_VAR

uConv.aWords[0] := GVL_Modbus.wFlowRate_H;  (* High Word *)
uConv.aWords[1] := GVL_Modbus.wFlowRate_L;  (* Low Word *)
GVL_Params.rFlowRateSP := uConv.rValue;

(* Komut register işleme *)
IF (GVL_Modbus.wCommandRegister AND 16#0001) <> 0 THEN
    GVL_HMI.xRemoteStart := TRUE;
    GVL_Modbus.wCommandRegister := GVL_Modbus.wCommandRegister AND (NOT 16#0001);
END_IF
IF (GVL_Modbus.wCommandRegister AND 16#0002) <> 0 THEN
    GVL_HMI.xRemoteStop := TRUE;
    GVL_Modbus.wCommandRegister := GVL_Modbus.wCommandRegister AND (NOT 16#0002);
END_IF

(* ===== COILS: Master'dan PLC'ye ===== *)
(* Coil değerleri, yükselen kenarla işle *)
IF GVL_Modbus.xCoil_StartCmd THEN
    GVL_HMI.xRemoteStart := TRUE;
    GVL_Modbus.xCoil_StartCmd := FALSE;  (* HMI'dan sonra temizle *)
END_IF
```

### Birden Fazla Master Bağlantısı

```
CODESYS Modbus TCP Slave, birden fazla eş zamanlı TCP bağlantısını kabul eder.

Güvenli kullanım:
  Master A (SCADA): IR/DI okur, HR/Coil YAZMAZ (salt okuma)
  Master B (HMI): HR setpointleri yazar, IR/DI okur
  Master C (Python script): Yalnızca IR/DI okur (monitoring)

Riskli kullanım:
  Master A: HR[0]'a 450 yazar (hız = 45.0)
  Master B: HR[0]'a 300 yazar (hız = 30.0)
  → Son yazan kazanır → Tutarsız davranış

Çözüm: Her master'ın yazma yetkisi farklı register bloklarına sınırlandırılmalı.
        (CODESYS bunu protokol düzeyinde kısıtlamaz; uygulama düzeyinde tasarlanmalı.)
```

### Timeout ve Bağlantı Yönetimi

```
CODESYSControl.cfg — Modbus TCP parametreleri:

[CmpModbusTCP]
; Bağlantı timeout (ms)
SessionTimeout=5000

; Maksimum eş zamanlı bağlantı
MaxConnections=5

; Response timeout (ms)
ResponseTimeout=3000
```

```iecst
(* PLC kodu: Modbus bağlantı durumunu izle *)
(* ModbusTCP Slave cihaz diagnostics — platforma bağlı *)
PROGRAM PRG_ModbusHealth
VAR
    tLastActivityTimer : TON;
    xModbusConnected   : BOOL;
    tConnectionTimeout : TIME := T#10S;
END_VAR

(* Bağlantı durumu: Son Modbus aktivitesinden bu yana süre *)
tLastActivityTimer(
    IN := TRUE,
    PT := tConnectionTimeout
);

(* Eğer yeni veri geldiyse (HR güncellendi), timer sıfırla *)
IF GVL_Modbus.wSpeedSetpoint_x10 <> GVL_Modbus.wPrevSpeedSP THEN
    tLastActivityTimer(IN := FALSE);
    GVL_Modbus.wPrevSpeedSP := GVL_Modbus.wSpeedSetpoint_x10;
END_IF

xModbusConnected := NOT tLastActivityTimer.Q;

(* Bağlantı kopuksa: Güvenli moda geç *)
IF NOT xModbusConnected THEN
    GVL_Alarms.xModbusConnLost := TRUE;
    (* Güvenli fallback: Son bilinen değeri koru veya varsayılana dön *)
END_IF
```

## Örnekler

### Örnek 1: Çoklu Port ile İki Ayrı Modbus Slave

Bazı projelerde farklı HMI'lar farklı portlara bağlanmak ister:

```
Device Tree:
  Ethernet (eth0)
  ├── ModbusTCP_Slave_Main     (port 502) ← Üretim SCADA
  └── ModbusTCP_Slave_Debug    (port 5020) ← Bakım laptop

Her slave kendi I/O Mapping'ine sahip:
  Main: Operatör değişkenleri
  Debug: Tüm değişkenler + dahili diagnostikler
```

### Örnek 2: Sadece Holding Register Kullanan Tasarım (Basitleştirilmiş)

Birçok HMI, 4 register tipini desteklemez veya belgesi karmaşık olur. Basit çözüm:

```
Tüm değişkenler Holding Register'da:

HR 0-9   : PLC → HMI (ölçümler) — HMI FC03 ile okur, yazamaz
HR 10-19 : HMI → PLC (komutlar/setpointler) — HMI FC16 ile yazar
HR 20-29 : Durum bilgisi — HMI FC03 ile okur

Dezavantaj: Standart dışı. Ölçüm değerlerine HMI yazabilir.
Avantaj: Tek FC03 ve FC16 ile her şey çalışır. Basit HMI entegrasyonu.
```

### Örnek 3: Modbus Slave Test — Python ile

CODESYS slave yapılandırması tamamlandıktan sonra Python ile test:

```python
from pymodbus.client import ModbusTcpClient
import struct

PLC_IP = '192.168.1.100'
SLAVE_ID = 1

with ModbusTcpClient(PLC_IP, port=502, timeout=3) as client:
    
    print("=== HOLDING REGISTERS (HR) Okuma ===")
    hr = client.read_holding_registers(0, 11, slave=SLAVE_ID)
    if not hr.isError():
        print(f"HR[0] Hız SP    : {hr.registers[0] / 10.0} m/dk")
        print(f"HR[1] Sıcaklık SP: {hr.registers[1] / 10.0} °C")
        print(f"HR[2] Reçete No : {hr.registers[2]}")
        print(f"HR[10] Komut     : {hr.registers[10]:#06x}")
    
    print("\n=== INPUT REGISTERS (IR) Okuma ===")
    ir = client.read_input_registers(0, 13, slave=SLAVE_ID)
    if not ir.isError():
        print(f"IR[0] Gerçek Hız   : {ir.registers[0] / 10.0} m/dk")
        print(f"IR[1] Gerçek Sıcaklık: {ir.registers[1] / 10.0} °C")
        status = ir.registers[3]
        print(f"IR[3] Durum Word   : 0x{status:04x}")
        print(f"  Çalışıyor  : {bool(status & 0x0001)}")
        print(f"  Hata Var   : {bool(status & 0x0002)}")
        prod = (ir.registers[10] << 16) | ir.registers[11]
        print(f"Üretim Sayacı: {prod} adet")
    
    print("\n=== COILS Okuma ===")
    coils = client.read_coils(0, 3, slave=SLAVE_ID)
    if not coils.isError():
        print(f"Coil 0 Start Cmd : {coils.bits[0]}")
        print(f"Coil 1 Stop Cmd  : {coils.bits[1]}")
        print(f"Coil 2 Reset Cmd : {coils.bits[2]}")
    
    print("\n=== DISCRETE INPUTS Okuma ===")
    di = client.read_discrete_inputs(0, 4, slave=SLAVE_ID)
    if not di.isError():
        print(f"DI 0 Running   : {di.bits[0]}")
        print(f"DI 1 Fault     : {di.bits[1]}")
        print(f"DI 2 Door Open : {di.bits[2]}")
    
    print("\n=== YAZMA TESTLERİ ===")
    # Setpoint yaz
    client.write_register(0, 450, slave=SLAVE_ID)  # 45.0 m/dk
    print("HR[0] = 450 yazıldı (45.0 m/dk)")
    
    # Start komutu
    client.write_coil(0, True, slave=SLAVE_ID)
    print("Coil 0 = True (Start)")
    
    import time; time.sleep(0.2)
    client.write_coil(0, False, slave=SLAVE_ID)
    print("Coil 0 = False (Start temizlendi)")
```

## Sık Yapılan Hatalar

### Hata 1: Bus Cycle Task Ayarlanmamış

```
Semptom: Slave device eklendi, I/O Mapping yapıldı ama değerler güncellemiyor.
Neden  : Bus Cycle Task atanmamış → I/O güncelleme gerçekleşmiyor.

Çözüm  : I/O Mapping → Bus Cycle Task dropdown → Task_Slow seç
```

### Hata 2: Input Register'ı PLC Kodu Yazmıyor

```
Semptom: Master FC04 ile Input Register okuyor ama hep 0 geliyor.
Neden  : PRG_ModbusUpdate çalışmıyor veya değişken adı yanlış eşlenmiş.

Kontrol:
  1. PRG_ModbusUpdate hangi task'ta? Task_Slow çalışıyor mu?
  2. I/O Mapping'de doğru değişken bağlı mı?
  3. Watch Window'da GVL_Modbus.wActualSpeed_x10 değeri doğru mu?
```

### Hata 3: Holding Register'ı PLC Kodu Eziyor

```
Semptom: Master setpoint yazıyor (FC16) ama PLC hep eski değere dönüyor.
Neden  : PLC kodu GVL_Modbus.wSpeedSetpoint_x10'u sürekli override ediyor.
         Örnek: wSpeedSetpoint_x10 := REAL_TO_WORD(GVL_Params.rSpeedSP * 10);
         Bu yanlış yön! Master → HR → PLC olmalı, PLC → HR → Master değil.

Çözüm  : PRG_ModbusUpdate'te HR değişkenlerine PLC kodu asla yazmamalı.
          HR'dan PLC parametresine okuma yapılmalı:
          GVL_Params.rSpeedSP := WORD_TO_REAL(GVL_Modbus.wSpeedSetpoint_x10) / 10.0;
```

### Hata 4: Scaling Kayması

```
Semptom: HMI'da 85.0 setpoint yazıyor, PLC 0.85 veya 850 okuyor.
Neden  : Ölçek faktörü (×10) ya yazarken ya okurken uygulanıyor.

Kontrol:
  HMI belgesi: "register × 10 = gerçek değer"
  Yazma: HMI 85.0 → 850 yazar → HR[1] = 850
  PLC okuma: 850 / 10.0 = 85.0 ✓
  
  Hata örneği: HMI 85.0 yazar (scale yapmadı) → HR[1] = 85
  PLC okuma: 85 / 10.0 = 8.5 ✗ (yanlış ölçek)

Çözüm: Register haritasını HMI yazılımcısına açıkça belgelendirip ver.
        Her değişken için: birim, ölçek, veri tipi.
```

### Hata 5: Aynı Değişkene Birden Fazla Master Yazıyor

```
Semptom: Setpoint değerleri sürekli değişiyor; beklenmedik davranış.
Neden  : İki master aynı HR'a yazıyor. Son yazan kazanır.

Çözüm  : Register haritasını bölümle. Her master farklı HR bloğu kullanmalı.
          Veya tek yazıcı (one-writer) prensibi: Yalnızca bir master yazar.
```

## Gerçek Proje Notları

**Not 1 — Task Seçiminin CPU Üzerindeki Etkisi**  
Bir projede Modbus slave Bus Cycle Task'ı yanlışlıkla Task_Control (10ms, Prio:2) olarak ayarlanmıştı. Task Monitor'da Task_Control exec time %30 artış gösterdi. Nedeni: Her 10ms'de Modbus I/O güncellemesi + kontrol kodu. Task_Slow (100ms) olarak değiştirildi, Task_Control exec time normale döndü.

**Not 2 — "HR Neden Hep 0?" Vakası**  
Yeni kurulan bir sistemde master tüm HR'ları 0 okuyordu. PRG_ModbusUpdate'i yazan mühendis `wSpeedSetpoint_x10 := 450;` gibi sabit değer atamış (test için) ve kodu kaldırmayı unutmuştu. Her döngüde HR[0] = 450 olarak üzerine yazılıyordu. Master 1000 yazdı → 100ms içinde 450'ye döndü. 30 dakikalık debug: tek satır kod.

**Not 3 — Komut Register Sıfırlanmama Problemi**  
HMI "Start" için komut register bit 0'ı 1 yaptı. PLC bunu işledi ve motoru başlattı. Ama komut register 1 kalmaya devam etti — PLC her döngüde "Start" komutu alıyor gibiydi. Motor durdurulamazdı. Çözüm: PLC komutu işledikten sonra bit'i sıfırlamalı:
```
GVL_Modbus.wCommandRegister := GVL_Modbus.wCommandRegister AND (NOT 16#0001);
```

**Not 4 — Adresleme Karışıklığı ile Kayıp Bir Gün**  
HMI belgesi "HR 40011 = Akış Hızı" yazıyordu. HMI yazılımcısı register adresine 40011 girdi, pymodbus testi `address=40011` kullandı. İki taraf da yanlıştı: Doğrusu `address=10`. Gün boyunca her iki taraf "bizim yazılımımız doğru, karşı taraf hatalı" dedi. Wireshark ile frame analizi: Request `address=40011 (0x9C6B)` — aralık dışı → Exception 0x02. Belge standardizasyonu: Register haritasında hem 1-tabanlı belge referansı hem 0-tabanlı protokol adresi gösterildi.

**Not 5 — Bus Cycle Task Jitter'ı ve "Geç Gelen" Veri**  
Modbus slave I/O güncellemesi Bus Cycle Task'a bağlıdır. Task_Slow (100ms) seçilen bir projede, master 50ms'de bir sorgulasa bile PLC değerleri ancak 100ms'de bir tazeleniyordu — master ardışık iki okumada aynı değeri görüyordu. Üstelik Task_Slow başka ağır kodla yüklenince jitter 100ms'den 180ms'ye çıktı. Master tarafındaki polling periyodu, slave'in Bus Cycle Task periyodundan **kısa** olmamalı; aksi halde aynı snapshot tekrar tekrar okunur (gereksiz trafik). Master polling = Bus Cycle Task periyodu (veya biraz uzun) ayarlandı.

**Not 6 — Watchdog'un Olmayışı: PLC Çalışıyor, SCADA Öldü, Motor Döndü**  
Bir kurulumda SCADA komut register'ı üzerinden motor başlattı. SCADA bilgisayarı çöktü; TCP bağlantısı koptu ama CODESYS slave'in son yazdığı register değerleri (Start=1) hafızada kaldı. PLC kodu "son komutu" uygulamaya devam etti, motor durmadı. Modbus slave kendiliğinden "bağlantı koptu → güvenli değer" yapmaz. Çözüm: PRG_ModbusHealth ile master aktivitesini izleyen bir watchdog; X saniye yazma gelmezse komut registerlarını güvenli duruma (Stop) zorlamak. Emniyet-kritik komutlar asla "kalıcı register değeri"ne bırakılmamalı.

**Not 7 — REAL Mapping: %QW Çiftinde Word Sırası Sürprizi**  
CODESYS'te bir REAL değişkeni doğrudan iki ardışık Holding Register offset'ine mapledik (uConv UNION ile). Master Big-Endian okudu ama değer ters geldi. Sebep: CODESYS'in çalıştığı hedef (ARM, little-endian Raspberry Pi) REAL'i bellekte little-endian word sırasıyla tutuyordu; aynı proje x86 yerine ARM'de farklı word sırası verdi. Çözüm: REAL'i iki WORD'e bölerken platform-bağımsız açık dönüşüm (SHR/AND ile manuel) kullanmak, UNION'a güvenmemek. CODESYS Modbus mapping'inde 32-bit değerlerde hedef CPU endian'ı mutlaka test edilmeli.

**Not 8 — Holding Register Sayısını Az Tutmanın Bedeli**  
Hafıza tasarrufu için HR Count = 50 ayarlandı (tam ihtiyaç). Sonradan 8 register'lık yeni bir özellik eklenince master `address=52` istedi → Exception 0x02. SCADA tarafında "cihaz arızalı" alarmı çıktı, saatlerce yanlış yerde arandı. Slave register sayısı her zaman ihtiyacın ~1.5 katı ayarlanmalı; CODESYS'te register hafızası ucuzdur, sonradan büyütmek download + duruş gerektirir.

## Edge Case'ler ve Sistem Limitleri

```
EDGE CASE                          CODESYS DAVRANIŞI               SONUÇ
─────────────────────────────────────────────────────────────────────────────
Register Count yetersiz            Aralık dışı isteğe Exception   0x02 döner
                                   0x02                            (cihaz arızası değil)
Bus Cycle Task atanmamış           I/O image güncellenmez          Değerler donar
Bus Cycle Task çok hızlı           CPU yükü + kontrol jitter'ı     Task_Control yavaşlar
MaxConnections aşımı               Yeni TCP bağlantısı reddedilir  RST veya sessiz drop
Bağlantı koptu                     Son register değerleri kalır    Watchdog şart
Aynı HR'a PLC + master yazar       Master'ın yazdığı her scan ezilir HR tek-yön olmalı
REAL/DWORD word sırası             Hedef CPU endian'ına bağlı      Platformda test et
Çoklu master aynı register         Son yazan kazanır               Blok bölümle
Download sırasında bağlantı        TCP koparılır, master timeout   Beklenen davranış
```

**Bus Cycle Task — I/O image senkronizasyonu:**
CODESYS'te Modbus slave register'ları, atanan Bus Cycle Task'ın **başında** GVL'den okunur ve **sonunda** GVL'ye yazılır (I/O image güncelleme). Yani master'ın yazdığı bir HR değeri, PLC koduna ancak bir sonraki task döngüsünde görünür; PLC'nin yazdığı bir IR değeri, master'a ancak task döngüsü tamamlandıktan sonra ulaşır. Bu, master polling'i task periyodundan hızlı yapıldığında neden "bayat snapshot" okunduğunu açıklar.

**Atomiklik garantisi — task içi:**
Bir 32-bit değerin iki register'ı **aynı Bus Cycle Task scan'inde** GVL'ye yazılırsa, I/O image güncellemesi tek seferde olduğundan o iki register tutarlı bir snapshot oluşturur. Word tearing riski, PLC değeri **scan'ler arasında** parça parça güncellediğinde doğar. Bu yüzden 32-bit değerleri tek atama bloğunda yazmak (shadow değişken deseni) CODESYS slave'de word tearing'i kaynağında çözer.

**MaxConnections aşımı:**
`CODESYSControl.cfg` içindeki `MaxConnections` aşıldığında runtime davranışı platforma göre değişir: Bazıları yeni bağlantıya TCP RST gönderir (istemci anında "connection refused" alır), bazıları bağlantıyı kabul edip ilk istekte düşürür. Çok sayıda istemci (her biri kendi bağlantısını açan) varsa bu limit hızla dolar; tek bir gateway/aggregator istemci tasarımı tercih edilmeli.

## Optimizasyon

```
OPTİMİZASYON                       KAZANÇ / GEREKÇE
─────────────────────────────────────────────────────────────────
Doğru Bus Cycle Task (Task_Slow)   Kontrol döngüsü jitter'ını korur
Register'ları bitişik maple         Master tek FC03 ile tüm bloğu okur
Tek-yön veri akışı (HR↔IR ayrımı)  Ezme/race önlenir, mantık netleşir
PRG_ModbusUpdate'i hafif tut        Task_Slow exec time düşük kalır
Değişmeyen IR'ları her scan         Gereksiz; ama maliyet düşük —
güncellemeyebilirsin                netlik için güncellemek tercih edilir
32-bit değerde shadow deseni        Word tearing'i kaynağında çözer
```

**Task periyodu seçimi — kontrol vs Modbus:**
Modbus I/O güncellemesi gerçek zamanlı kontrol döngüsünün (Task_Control, 10ms) içinde **olmamalıdır**. Modbus güncellemesini ayrı, daha yavaş bir task'a (Task_Slow, 100ms) koymak iki kazanç sağlar: (1) Kontrol döngüsü jitter'ı korunur — Modbus I/O, kontrol scan'ine yük bindirmez; (2) Master tipik olarak 100ms–1s periyodla sorgular, daha hızlı I/O güncellemesi zaten boşa gider. Modbus güncelleme periyodu, master'ın en hızlı polling periyoduna eşit veya biraz altında tutulmalıdır.

**Register düzeni master verimliliğini belirler:**
CODESYS I/O Mapping'de offset'leri **mantıksal olarak değil, master'ın okuma deseni**ne göre düzenle. Master her döngüde HR 0–20'yi okuyorsa, sık okunan tüm değerler 0–20 aralığında bitişik olmalı; rezerv ve nadir kullanılan registerlar bloğun sonuna. Böylece master tek `read_holding_registers(0, 21)` ile tüm canlı veriyi alır — slave tarafındaki düzen, master tarafındaki round-trip sayısını doğrudan belirler.

**PRG_ModbusUpdate hafifliği:**
Bu PRG her Bus Cycle Task scan'inde çalışır. İçine ağır hesap (PID, filtre, döngü) koymak Task_Slow exec time'ını şişirir ve I/O güncellemesini geciktirir. Sadece veri kopyalama/ölçekleme/bit-maskeleme yapmalı; iş mantığı kendi task'ında kalmalı.

## Derin Teknik Detay

**CODESYS Modbus slave neden "I/O cihazı" gibi modellenir?**
CODESYS, Modbus slave register'larını Device Tree'de bir fieldbus I/O modülü gibi sunar çünkü altta yatan mekanizma gerçekten I/O image güncellemesidir. EtherCAT/PROFINET I/O modülleriyle **aynı** Bus Cycle Task mekanizmasını kullanır: Task başında girişler (master'ın yazdığı HR/Coil) GVL'ye kopyalanır, task sonunda çıkışlar (PLC'nin yazdığı IR/DI) register'lara yazılır. Bu birleşik model, Modbus register'larının neden doğrudan PLC değişkenlerine maplenip senkron tutulduğunu açıklar — Modbus, CODESYS'in genel fieldbus soyutlamasına oturtulmuştur.

**Veri yönü neden donanımla zorlanmaz, konvansiyonla yönetilir:**
Modbus protokolü Holding Register'ı R/W tanımlar — hem master yazabilir hem (teorik olarak) okunabilir. CODESYS bunu donanımsal olarak tek-yön yapmaz; mapping'de HR hücresi hem master'dan yazılabilir hem PLC kodundan değiştirilebilir. "HR = master yazar, PLC okur; IR = PLC yazar, master okur" kuralı bir **konvansiyondur**, protokol veya runtime zorlamaz. Bu yüzden "PLC HR'ı eziyor" hatası bu kadar yaygındır: Hiçbir mekanizma yanlış yönü engellemez, yalnızca disiplin engeller.

**Bağlantısız (stateless) slave'in emniyet boşluğu:**
Modbus slave, master'ın "hâlâ orada mı" olduğunu protokol seviyesinde bilmez. TCP bağlantısı koptuğunda runtime bunu algılayabilir ama register değerlerini **otomatik temizlemez** — son yazılan komut hafızada kalır. Bu, stateless poll-response tasarımının doğrudan sonucudur: Sunucu istemci durumu tutmadığı için "istemci gitti, komutu geri al" diye bir kavram yoktur. Emniyet, uygulama katmanında (watchdog timer + güvenli-durum fallback) inşa edilmek zorundadır. OPC UA'nın session/subscription keepalive mekanizmasının çözdüğü problem tam olarak budur; Modbus'ta bedeli manuel watchdog kodudur.

## İlgili Konular

```
knowledge/protocols/modbus-tcp/
├── 01_protocol_basics.md        → MBAP ve master-slave mantığı
├── 02_register_model.md         → Register tipleri ve ölçek faktörleri
├── 03_function_codes.md         → FC03/16 gibi kullanılan kodlar
└── 05_client_implementations.md → Slave'e bağlanan Python/JS istemcileri

knowledge/codesys/networking/
└── 02_modbus_slave.md           → CODESYS Modbus slave giriş belgesi

Araçlar:
  Modbus Poll  → CODESYS slave'i test etmek için GUI master
  pymodbus     → Python ile otomatik test
  Wireshark    → Paket düzeyinde analiz
```
