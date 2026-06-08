---
KONU        : Modbus TCP İstemci Implementasyonları
KATEGORİ    : protocols
ALT_KATEGORI: modbus-tcp
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://www.pymodbus.org/docs/tcp-client"
    başlık: "PyModbus Docs — TCP Client"
    güvenilirlik: topluluk
  - url: "https://www.pymodbus.org/docs/basic-concepts"
    başlık: "PyModbus Docs — Protocol Basics"
    güvenilirlik: topluluk
  - url: "https://controlbyte.tech/blog/python-modbus-plc-communication/"
    başlık: "ControlByte — Python Modbus PLC Communication (2026)"
    güvenilirlik: topluluk
  - url: "https://pymodbustcp.readthedocs.io/en/stable/examples/client_read_h_registers.html"
    başlık: "pyModbusTCP ReadTheDocs — Client Examples"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_protocol_basics.md"
    ilişki: gerektirir
  - konu: "02_register_model.md"
    ilişki: gerektirir
  - konu: "03_function_codes.md"
    ilişki: gerektirir
  - konu: "04_codesys_slave_config.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Modbus protokol temelleri (01_protocol_basics.md - 03_function_codes.md)"
  - "Python veya JavaScript temel programlama bilgisi"
ÇELİŞKİLER :
  - kaynak: "pymodbus vs pyModbusTCP — iki farklı Python kütüphanesi"
    konu: "İki kütüphane benzer isim, farklı API ve özellik seti"
    çözüm: >
      pymodbus (pip install pymodbus): Kapsamlı, RTU + TCP + ASCII, async destek.
        Büyük projeler, özellik zenginliği gerektiğinde.
      pyModbusTCP (pip install pyModbusTCP): Yalnızca Modbus TCP, çok basit API.
        Küçük scriptler, hız isteyen basit kullanımda.
      Bu belge pymodbus kullanır (daha yaygın). API farkı minimal.
---

## Özün Ne

Modbus TCP istemcisi yazmak, `connect → read/write → disconnect` döngüsünden ibarettir. Ancak production kalitesinde bir istemci: bağlantı koptuğunda kendini yeniler, hataları düzgün yakalar, float/string gibi karmaşık tipleri doğru ayrıştırır ve polling döngüsünü verimli yapılandırır. Bu belge Python (pymodbus) ve JavaScript (jsmodbus) için tam örnekler sunar; her ikisinde de başlangıçtan production-ready sınıfa kadar adım adım gidilir.

---

## Python — pymodbus

### Kurulum

```bash
pip install pymodbus

# Asenkron destek (asyncio):
pip install pymodbus[reqs]

# Seri port (RTU) desteği:
pip install pymodbus[serial]
```

### Temel Bağlantı

```python
from pymodbus.client import ModbusTcpClient

# Bağlantı kur
client = ModbusTcpClient(
    host='192.168.1.100',
    port=502,
    timeout=3,       # Saniye cinsinden socket timeout
    retries=3        # Hata sonrası yeniden deneme
)

connected = client.connect()
if not connected:
    print("Bağlantı başarısız!")
    exit(1)

# Okuma
result = client.read_holding_registers(address=0, count=10, slave=1)
if not result.isError():
    print(f"HR[0-9]: {result.registers}")

# Yazma
client.write_register(address=0, value=450, slave=1)

# Context manager ile (önerilir — otomatik disconnect)
with ModbusTcpClient('192.168.1.100', port=502, timeout=3) as client:
    result = client.read_holding_registers(0, 10, slave=1)
    print(result.registers)
```

### Tüm Register Tiplerine Erişim

```python
from pymodbus.client import ModbusTcpClient

SLAVE = 1

with ModbusTcpClient('192.168.1.100', port=502) as client:
    
    # FC01: Coil oku (boolean list)
    coils = client.read_coils(address=0, count=8, slave=SLAVE)
    if not coils.isError():
        for i, bit in enumerate(coils.bits[:8]):
            print(f"Coil[{i}]: {bit}")
    
    # FC02: Discrete Input oku
    di = client.read_discrete_inputs(address=0, count=4, slave=SLAVE)
    if not di.isError():
        print(f"DI: {di.bits[:4]}")
    
    # FC03: Holding Register oku
    hr = client.read_holding_registers(address=0, count=20, slave=SLAVE)
    if not hr.isError():
        print(f"HR[0]: {hr.registers[0]}")
        print(f"HR[0-19]: {hr.registers}")
    
    # FC04: Input Register oku
    ir = client.read_input_registers(address=0, count=10, slave=SLAVE)
    if not ir.isError():
        print(f"IR[0]: {ir.registers[0]}")
    
    # FC05: Tek Coil yaz
    client.write_coil(address=0, value=True, slave=SLAVE)
    client.write_coil(address=0, value=False, slave=SLAVE)
    
    # FC06: Tek Register yaz
    client.write_register(address=0, value=450, slave=SLAVE)
    
    # FC15: Çoklu Coil yaz
    client.write_coils(address=0, values=[True, False, True], slave=SLAVE)
    
    # FC16: Çoklu Register yaz
    client.write_registers(address=0, values=[450, 856, 3], slave=SLAVE)
```

### Float Okuma/Yazma

```python
import struct
from pymodbus.client import ModbusTcpClient

def read_float32(client, address, slave=1, byte_order='big'):
    """
    2 ardışık Holding Register'dan IEEE 754 float32 oku.
    byte_order: 'big' (AB CD), 'little' (DC BA),
                'big_swap' (CD AB), 'little_swap' (BA DC)
    """
    result = client.read_holding_registers(address, 2, slave=slave)
    if result.isError():
        raise ValueError(f"Float okuma hatası: {result}")
    
    r0, r1 = result.registers[0], result.registers[1]
    
    if byte_order == 'big':       # AB CD (en yaygın)
        raw = struct.pack('>HH', r0, r1)
        return struct.unpack('>f', raw)[0]
    elif byte_order == 'little':   # DC BA
        raw = struct.pack('<HH', r0, r1)
        return struct.unpack('<f', raw)[0]
    elif byte_order == 'big_swap': # CD AB
        raw = struct.pack('>HH', r1, r0)
        return struct.unpack('>f', raw)[0]
    elif byte_order == 'little_swap': # BA DC
        raw = struct.pack('<HH', r1, r0)
        return struct.unpack('<f', raw)[0]

def write_float32(client, address, value, slave=1, byte_order='big'):
    """IEEE 754 float32'yi 2 Holding Register'a yaz."""
    raw = struct.pack('>f', value)
    hw = struct.unpack('>H', raw[0:2])[0]
    lw = struct.unpack('>H', raw[2:4])[0]
    
    if byte_order == 'big':
        client.write_registers(address, [hw, lw], slave=slave)
    elif byte_order == 'big_swap':
        client.write_registers(address, [lw, hw], slave=slave)
    # diğer varyantlar benzer şekilde

# Kullanım
with ModbusTcpClient('192.168.1.100') as client:
    write_float32(client, address=20, value=85.5)
    temp = read_float32(client, address=20)
    print(f"Sıcaklık: {temp:.1f} °C")

def detect_byte_order(client, address, known_value, slave=1):
    """
    Bilinen bir değer yazarak byte order'ı otomatik tespit et.
    known_value: float (ör. 1.0 veya 100.0)
    """
    write_float32(client, address, known_value, byte_order='big')
    
    for order in ['big', 'little', 'big_swap', 'little_swap']:
        read_val = read_float32(client, address, byte_order=order)
        if abs(read_val - known_value) < 0.001:
            print(f"Byte order tespit edildi: {order}")
            return order
    
    raise ValueError("Byte order tespit edilemedi!")
```

### Hata Yönetimi

```python
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException, ConnectionException

EXCEPTION_CODES = {
    0x01: "Illegal Function Code",
    0x02: "Illegal Data Address",
    0x03: "Illegal Data Value",
    0x04: "Slave Device Failure",
    0x05: "Acknowledge",
    0x06: "Slave Device Busy",
    0x0A: "Gateway Path Unavailable",
    0x0B: "Gateway Target Failed to Respond",
}

def safe_read(client, address, count, reg_type='holding', slave=1):
    """Hata yönetimli register okuma."""
    try:
        if reg_type == 'holding':
            result = client.read_holding_registers(address, count, slave=slave)
        elif reg_type == 'input':
            result = client.read_input_registers(address, count, slave=slave)
        elif reg_type == 'coil':
            result = client.read_coils(address, count, slave=slave)
        elif reg_type == 'discrete':
            result = client.read_discrete_inputs(address, count, slave=slave)
        
        if result.isError():
            exc = getattr(result, 'exception_code', None)
            msg = EXCEPTION_CODES.get(exc, f"Unknown (0x{exc:02X})" if exc else "Unknown")
            raise ValueError(f"Modbus Exception {msg} @ addr={address}")
        
        return result
    
    except ConnectionException as e:
        raise ConnectionError(f"Bağlantı hatası: {e}") from e
    except ModbusException as e:
        raise RuntimeError(f"Modbus hatası: {e}") from e

# Kullanım
try:
    result = safe_read(client, 0, 10, 'holding')
    print(result.registers)
except ValueError as e:
    print(f"Register hatası: {e}")
    # 0x02 = adres yanlış → belgeyi kontrol et
except ConnectionError as e:
    print(f"Bağlantı koptu: {e}")
    # Reconnect döngüsüne gir
```

### Production-Ready İstemci Sınıfı

```python
import time
import struct
import logging
import threading
from typing import Optional, List
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException, ModbusException

logger = logging.getLogger(__name__)

class ModbusManager:
    """
    Production kalitesi Modbus TCP istemcisi.
    - Otomatik yeniden bağlanma
    - Thread-safe okuma/yazma
    - Float/DWORD yardımcı metodları
    - Polling döngüsü desteği
    """
    
    def __init__(self, host: str, port: int = 502, slave: int = 1,
                 timeout: float = 3.0, reconnect_delay: float = 5.0):
        self.host = host
        self.port = port
        self.slave = slave
        self.timeout = timeout
        self.reconnect_delay = reconnect_delay
        
        self._client: Optional[ModbusTcpClient] = None
        self._lock = threading.Lock()
        self._connected = False
        self._running = False
        
    def connect(self) -> bool:
        """Bağlantı kur."""
        with self._lock:
            try:
                self._client = ModbusTcpClient(
                    self.host, port=self.port, timeout=self.timeout
                )
                if self._client.connect():
                    self._connected = True
                    logger.info(f"Bağlandı: {self.host}:{self.port}")
                    return True
                else:
                    logger.error(f"Bağlantı başarısız: {self.host}:{self.port}")
                    return False
            except Exception as e:
                logger.error(f"Bağlantı hatası: {e}")
                return False
    
    def disconnect(self):
        """Bağlantıyı kapat."""
        with self._lock:
            if self._client:
                self._client.close()
            self._connected = False
    
    def ensure_connected(self) -> bool:
        """Bağlantı yoksa yeniden bağlan."""
        if not self._connected:
            return self.connect()
        return True
    
    def read_registers(self, address: int, count: int) -> Optional[List[int]]:
        """Holding Register oku — hata durumunda None döner."""
        if not self.ensure_connected():
            return None
        
        with self._lock:
            try:
                result = self._client.read_holding_registers(
                    address, count, slave=self.slave
                )
                if result.isError():
                    logger.warning(f"HR okuma hatası @ {address}: {result}")
                    self._connected = False  # Reconnect tetikle
                    return None
                return result.registers
            except (ConnectionException, ModbusException) as e:
                logger.error(f"Okuma exception @ {address}: {e}")
                self._connected = False
                return None
    
    def write_register(self, address: int, value: int) -> bool:
        """Tek Holding Register yaz."""
        if not self.ensure_connected():
            return False
        
        with self._lock:
            try:
                result = self._client.write_register(
                    address, value, slave=self.slave
                )
                return not result.isError()
            except Exception as e:
                logger.error(f"Yazma hatası @ {address}: {e}")
                self._connected = False
                return False
    
    def write_registers(self, address: int, values: List[int]) -> bool:
        """Çoklu Holding Register yaz (FC16)."""
        if not self.ensure_connected():
            return False
        
        with self._lock:
            try:
                result = self._client.write_registers(
                    address, values, slave=self.slave
                )
                return not result.isError()
            except Exception as e:
                logger.error(f"Çoklu yazma hatası @ {address}: {e}")
                self._connected = False
                return False
    
    def read_float32(self, address: int) -> Optional[float]:
        """Big-Endian float32 oku (2 register)."""
        regs = self.read_registers(address, 2)
        if regs is None or len(regs) < 2:
            return None
        raw = struct.pack('>HH', regs[0], regs[1])
        return struct.unpack('>f', raw)[0]
    
    def write_float32(self, address: int, value: float) -> bool:
        """Big-Endian float32 yaz (2 register)."""
        raw = struct.pack('>f', value)
        hw = struct.unpack('>H', raw[0:2])[0]
        lw = struct.unpack('>H', raw[2:4])[0]
        return self.write_registers(address, [hw, lw])
    
    def read_uint32(self, address: int) -> Optional[int]:
        """32-bit unsigned integer oku (2 register, High-Low sırası)."""
        regs = self.read_registers(address, 2)
        if regs is None or len(regs) < 2:
            return None
        return (regs[0] << 16) | regs[1]
    
    def start_polling(self, interval: float, callback):
        """
        Arka planda periyodik polling döngüsü başlat.
        callback(data: dict) -> çağrılır
        """
        self._running = True
        
        def poll_loop():
            consecutive_failures = 0
            max_failures = 5
            
            while self._running:
                try:
                    # Veriyi toplu oku (tek istek — verimli)
                    hr = self.read_registers(0, 20)
                    ir = self.read_registers(0, 13)  # Input Register (FC04 için ayrı istemci gerekir)
                    
                    if hr is not None:
                        data = {
                            'speed_setpoint': hr[0] / 10.0,
                            'temp_setpoint':  hr[1] / 10.0,
                            'recipe_id':      hr[2],
                            'timestamp':      time.time()
                        }
                        callback(data)
                        consecutive_failures = 0
                    else:
                        consecutive_failures += 1
                        if consecutive_failures >= max_failures:
                            logger.error("Çok fazla ardışık hata — reconnect")
                            self.disconnect()
                            time.sleep(self.reconnect_delay)
                            consecutive_failures = 0
                
                except Exception as e:
                    logger.error(f"Polling exception: {e}")
                
                time.sleep(interval)
        
        self._poll_thread = threading.Thread(target=poll_loop, daemon=True)
        self._poll_thread.start()
    
    def stop(self):
        self._running = False
        self.disconnect()

# Kullanım örneği
def on_data(data: dict):
    print(f"[{time.strftime('%H:%M:%S')}] "
          f"Speed SP: {data['speed_setpoint']:.1f}, "
          f"Temp SP: {data['temp_setpoint']:.1f}")

plc = ModbusManager('192.168.1.100', slave=1, reconnect_delay=5.0)
plc.start_polling(interval=1.0, callback=on_data)

try:
    # Ana iş akışı
    plc.write_register(0, 450)        # Hız setpoint: 45.0
    plc.write_float32(20, 85.5)       # Float sıcaklık setpoint
    
    print("Çalışıyor. Ctrl+C ile dur.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    plc.stop()
    print("Durduruldu.")
```

### Otomatik Yeniden Bağlanma Döngüsü (Minimal)

```python
import time
from pymodbus.client import ModbusTcpClient

def run_with_reconnect(host, port=502, slave=1, poll_interval=1.0):
    """Bağlantı koptuğunda otomatik yeniden bağlanan polling döngüsü."""
    
    while True:
        print(f"Bağlanıyor: {host}:{port}...")
        
        try:
            with ModbusTcpClient(host, port=port, timeout=3) as client:
                print("Bağlandı.")
                
                while True:
                    result = client.read_holding_registers(0, 10, slave=slave)
                    
                    if result.isError():
                        print(f"Okuma hatası: {result}")
                        break  # Dış döngü yeniden bağlanır
                    
                    # Veriyi işle
                    regs = result.registers
                    speed = regs[0] / 10.0
                    temp  = regs[1] / 10.0
                    print(f"Hız: {speed} m/dk, Sıcaklık: {temp} °C")
                    
                    time.sleep(poll_interval)
        
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
        
        print(f"5 saniye sonra yeniden bağlanılacak...")
        time.sleep(5)

run_with_reconnect('192.168.1.100')
```

---

## JavaScript / Node.js — jsmodbus

### Kurulum

```bash
npm install jsmodbus
# veya
npm install modbus-serial     # Alternatif, RTU + TCP
```

### Temel Bağlantı ve Okuma (jsmodbus)

```javascript
const net = require('net');
const Modbus = require('jsmodbus');

const HOST = '192.168.1.100';
const PORT = 502;
const SLAVE_ID = 1;

const socket = new net.Socket();
const client = new Modbus.client.TCP(socket, SLAVE_ID);

// Bağlantıyı kur
socket.connect({ host: HOST, port: PORT });

socket.on('connect', async () => {
    console.log('Bağlandı:', HOST);
    
    try {
        // FC03: Holding Register oku
        const hrResult = await client.readHoldingRegisters(0, 10);
        console.log('HR[0-9]:', hrResult.response.body.values);
        
        // Değerleri yorumla
        const speedSP = hrResult.response.body.values[0] / 10.0;
        const tempSP  = hrResult.response.body.values[1] / 10.0;
        console.log(`Hız SP: ${speedSP} m/dk, Sıcaklık SP: ${tempSP} °C`);
        
        // FC04: Input Register oku
        const irResult = await client.readInputRegisters(0, 5);
        console.log('IR[0-4]:', irResult.response.body.values);
        
        // FC01: Coil oku
        const coilResult = await client.readCoils(0, 8);
        console.log('Coils[0-7]:', coilResult.response.body.values);
        
        // FC05: Tek Coil yaz
        await client.writeSingleCoil(0, true);
        console.log('Coil 0 = TRUE');
        
        // FC06: Tek Register yaz
        await client.writeSingleRegister(0, 450);
        console.log('HR[0] = 450 yazıldı');
        
        // FC16: Çoklu Register yaz
        await client.writeMultipleRegisters(0, [450, 856, 3]);
        console.log('HR[0-2] yazıldı: [450, 856, 3]');
        
    } catch (err) {
        console.error('Modbus hatası:', err.message);
    }
    
    socket.destroy();
});

socket.on('error', (err) => {
    console.error('Socket hatası:', err.message);
});

socket.on('close', () => {
    console.log('Bağlantı kapandı.');
});
```

### Float32 Yardımcı Fonksiyonları (JS)

```javascript
/**
 * İki Modbus register'ından IEEE 754 float32 oku.
 * @param {number[]} registers - 2 elemanlı array [highWord, lowWord]
 * @param {string} byteOrder - 'big' (AB CD) | 'little' (DC BA) | 'big_swap' (CD AB)
 */
function registersToFloat32(registers, byteOrder = 'big') {
    const [r0, r1] = registers;
    const buf = Buffer.alloc(4);
    
    if (byteOrder === 'big') {
        buf.writeUInt16BE(r0, 0);
        buf.writeUInt16BE(r1, 2);
    } else if (byteOrder === 'little') {
        buf.writeUInt16LE(r1, 0);
        buf.writeUInt16LE(r0, 2);
    } else if (byteOrder === 'big_swap') {
        buf.writeUInt16BE(r1, 0);
        buf.writeUInt16BE(r0, 2);
    }
    
    return buf.readFloatBE(0);
}

/**
 * Float32 değerini iki Modbus register'ına çevir.
 */
function float32ToRegisters(value, byteOrder = 'big') {
    const buf = Buffer.alloc(4);
    buf.writeFloatBE(value, 0);
    
    const hw = buf.readUInt16BE(0);
    const lw = buf.readUInt16BE(2);
    
    if (byteOrder === 'big')      return [hw, lw];
    if (byteOrder === 'big_swap') return [lw, hw];
    // diğer varyantlar...
    return [hw, lw];
}

// Kullanım
socket.on('connect', async () => {
    // Float setpoint yaz (85.5°C)
    const regs = float32ToRegisters(85.5);
    await client.writeMultipleRegisters(20, regs);
    
    // Geri oku ve doğrula
    const result = await client.readHoldingRegisters(20, 2);
    const temp = registersToFloat32(result.response.body.values);
    console.log(`Sıcaklık: ${temp.toFixed(1)} °C`); // 85.5
});
```

### Production-Ready Node.js İstemcisi

```javascript
const net = require('net');
const Modbus = require('jsmodbus');
const EventEmitter = require('events');

class ModbusManager extends EventEmitter {
    /**
     * Otomatik reconnect destekli Modbus TCP istemcisi.
     */
    constructor(options = {}) {
        super();
        this.host = options.host || '192.168.1.100';
        this.port = options.port || 502;
        this.slaveId = options.slaveId || 1;
        this.reconnectDelay = options.reconnectDelay || 5000;
        this.pollInterval = options.pollInterval || 1000;
        
        this._socket = null;
        this._client = null;
        this._connected = false;
        this._running = false;
        this._pollTimer = null;
        this._reconnectTimer = null;
    }
    
    connect() {
        if (this._connected) return;
        
        this._socket = new net.Socket();
        this._client = new Modbus.client.TCP(this._socket, this.slaveId);
        
        this._socket.on('connect', () => {
            this._connected = true;
            console.log(`Bağlandı: ${this.host}:${this.port}`);
            this.emit('connected');
            
            if (this._running) {
                this._startPolling();
            }
        });
        
        this._socket.on('error', (err) => {
            console.error(`Socket hatası: ${err.message}`);
            this._connected = false;
            this.emit('error', err);
        });
        
        this._socket.on('close', () => {
            console.log('Bağlantı kapandı.');
            this._connected = false;
            this.emit('disconnected');
            
            if (this._running) {
                console.log(`${this.reconnectDelay}ms sonra yeniden bağlanılıyor...`);
                this._reconnectTimer = setTimeout(() => this.connect(), this.reconnectDelay);
            }
        });
        
        this._socket.connect({ host: this.host, port: this.port });
    }
    
    disconnect() {
        this._running = false;
        if (this._pollTimer) clearInterval(this._pollTimer);
        if (this._reconnectTimer) clearTimeout(this._reconnectTimer);
        if (this._socket) this._socket.destroy();
        this._connected = false;
    }
    
    async readHoldingRegisters(address, count) {
        if (!this._connected) throw new Error('Bağlı değil');
        const result = await this._client.readHoldingRegisters(address, count);
        return result.response.body.values;
    }
    
    async writeRegister(address, value) {
        if (!this._connected) throw new Error('Bağlı değil');
        await this._client.writeSingleRegister(address, value);
    }
    
    async writeRegisters(address, values) {
        if (!this._connected) throw new Error('Bağlı değil');
        await this._client.writeMultipleRegisters(address, values);
    }
    
    async readFloat32(address, byteOrder = 'big') {
        const regs = await this.readHoldingRegisters(address, 2);
        return registersToFloat32(regs, byteOrder);
    }
    
    async writeFloat32(address, value, byteOrder = 'big') {
        const regs = float32ToRegisters(value, byteOrder);
        await this.writeRegisters(address, regs);
    }
    
    startPolling(callback) {
        this._running = true;
        this._pollCallback = callback;
        if (this._connected) this._startPolling();
        this.connect();
    }
    
    _startPolling() {
        if (this._pollTimer) clearInterval(this._pollTimer);
        
        this._pollTimer = setInterval(async () => {
            if (!this._connected) return;
            
            try {
                const hr = await this.readHoldingRegisters(0, 20);
                const ir = await this.readHoldingRegisters(0, 10); // Slave Input Register için
                
                const data = {
                    speedSetpoint: hr[0] / 10.0,
                    tempSetpoint:  hr[1] / 10.0,
                    recipeId:      hr[2],
                    actualSpeed:   ir[0] / 10.0,
                    actualTemp:    ir[1] / 10.0,
                    timestamp:     Date.now()
                };
                
                if (this._pollCallback) this._pollCallback(data);
                this.emit('data', data);
                
            } catch (err) {
                console.error(`Polling hatası: ${err.message}`);
                this._connected = false;
                this._socket.destroy();  // Reconnect tetikler
            }
            
        }, this.pollInterval);
    }
}

// Kullanım
const plc = new ModbusManager({
    host: '192.168.1.100',
    slaveId: 1,
    reconnectDelay: 5000,
    pollInterval: 1000
});

plc.on('connected', async () => {
    // Başlangıç ayarları
    await plc.writeRegister(0, 450);       // Hız SP: 45.0
    await plc.writeFloat32(20, 85.5);      // Sıcaklık SP: 85.5°C
    console.log('Başlangıç ayarları yapıldı.');
});

plc.on('data', (data) => {
    console.log(
        `[${new Date().toISOString()}] ` +
        `Hız SP: ${data.speedSetpoint} m/dk, ` +
        `Sıcaklık SP: ${data.tempSetpoint} °C`
    );
});

plc.on('disconnected', () => {
    console.log('Bağlantı kesildi, yeniden bağlanılıyor...');
});

plc.startPolling();

// Graceful shutdown
process.on('SIGINT', () => {
    plc.disconnect();
    console.log('Durduruldu.');
    process.exit(0);
});
```

---

## Kütüphane Seçim Rehberi

```
                     pymodbus         pyModbusTCP      jsmodbus         modbus-serial
                     (Python)         (Python)         (Node.js)        (Node.js)
──────────────────────────────────────────────────────────────────────────────────
Lisans              │ BSD            │ MIT            │ MIT            │ MIT
RTU Desteği         │ ✓              │ ✗              │ ✓              │ ✓ (RS485)
TCP Desteği         │ ✓              │ ✓ (sadece)     │ ✓              │ ✓
Async (asyncio/async│ ✓              │ ✗              │ ✓ (Promise)    │ Callback
API Karmaşıklığı    │ Orta           │ Çok Basit      │ Orta           │ Kolay
Topluluk            │ Büyük          │ Küçük          │ Orta           │ Büyük
Güncelleme Sıklığı  │ Aktif          │ Aktif          │ Aktif          │ Aktif
──────────────────────────────────────────────────────────────────────────────────

pymodbus seç:
  ✓ TCP + RTU birlikte gerektiğinde
  ✓ Async Python uygulaması
  ✓ Kapsamlı hata yönetimi
  ✓ Endüstriyel otomasyon script pipeline'ı

pyModbusTCP seç:
  ✓ Yalnızca TCP, çok basit API
  ✓ Küçük monitoring scriptleri
  ✓ auto_open ile otomatik reconnect dahili

jsmodbus seç:
  ✓ Node.js tabanlı uygulama
  ✓ Web dashboard, Node-RED entegrasyonu
  ✓ Promise tabanlı modern JS

modbus-serial seç:
  ✓ Hem TCP hem RS485 serial
  ✓ Daha basit callback API tercih edildiğinde
```

## Sık Yapılan Hatalar

### Hata 1: Yanıtı Beklemeden Yeni İstek Göndermek

```python
# ❌ YANLIŞ — Thread-safe değil, race condition
import threading

def read_speed():
    return client.read_holding_registers(0, 1, slave=1)

def read_temp():
    return client.read_holding_registers(1, 1, slave=1)

t1 = threading.Thread(target=read_speed)
t2 = threading.Thread(target=read_temp)
t1.start(); t2.start()
# → İki thread aynı anda read_holding_registers çağırır → Bozuk yanıtlar

# ✅ DOĞRU — Tek istekte toplu oku VEYA lock ile koruma
result = client.read_holding_registers(0, 2, slave=1)  # Her ikisini tek seferde
speed = result.registers[0]
temp  = result.registers[1]
```

### Hata 2: Bağlantıyı Kapatmadan Yeniden Açmak

```python
# ❌ YANLIŞ — Eski bağlantı kapatılmadan yenisi açılıyor
for i in range(100):
    client = ModbusTcpClient('192.168.1.100')
    client.connect()
    client.read_holding_registers(0, 1, slave=1)
    # client.close() YOK → Her döngü yeni bağlantı açık kalıyor
    # PLC MaxConnections dolunca yeni bağlantı reddedilir

# ✅ DOĞRU
with ModbusTcpClient('192.168.1.100') as client:
    for i in range(100):
        client.read_holding_registers(0, 1, slave=1)
        time.sleep(1)
# Context manager çıkışında otomatik close
```

### Hata 3: isError() Kontrolü Atlamak

```python
# ❌ YANLIŞ — Exception olmasa da Modbus error olabilir
result = client.read_holding_registers(0, 10, slave=1)
print(result.registers[0])  # AttributeError: 'ExceptionResponse' has no 'registers'

# ✅ DOĞRU
result = client.read_holding_registers(0, 10, slave=1)
if result.isError():
    print(f"Hata: {result}")
else:
    print(result.registers[0])
```

### Hata 4: Timeout'u Çok Kısa Ayarlamak

```python
# ❌ Timeout çok kısa: Yüklü ağda yanıt gecikmesi olabilir
client = ModbusTcpClient('192.168.1.100', timeout=0.1)

# Önerilen değerler:
# LAN içi (ms mertebesinde): timeout=1 (1 saniye)
# WAN/VPN (değişken gecikme): timeout=5
# Yüksek yük altındaki slave: timeout=3-5
```

## Gerçek Proje Notları

**Not 1 — Thread Lock'un Önemi**  
Bir monitoring scriptinde her sensör için ayrı thread oluşturulmuş, hepsi aynı `client` nesnesini kullanıyordu. Rastgele "invalid response" hataları geliyordu. Lock mekanizması eklendikten sonra tüm hatalar kalktı. Modbus istemci nesneleri thread-safe değildir.

**Not 2 — Otomatik Reconnect Gecikmesinin Doğru Seçimi**  
Bir üretim monitorunda reconnect delay = 100ms ayarlanmıştı. PLC kısa bir reboot yaptığında script saniyede 10 kez bağlantı denemesi yapıp PLC'yi bunalttı. PLC tekrar online olmakta güçlük çekti. Delay 5 saniyeye yükseltildi: Hem script hem PLC rahatladı.

**Not 3 — Float Byte Order'ı Test Etmeden Varsaymak**  
Cihaz belgesi "IEEE 754 float" yazıyordu. Kod Big-Endian varsaydı. Okunan değer: `-1.234e18` (anlamsız). Test: `known_value=1.0` yazıldı, 4 varyant denendi, `big_swap` tuttu. Ders: Float byte order asla varsayılmamalı, mutlaka test edilmeli.

**Not 4 — pyModbusTCP'nin auto_open Kolaylığı**  
Basit monitoring projelerinde pyModbusTCP'nin `auto_open=True` parametresi hayat kurtardı. Bağlantı düştüğünde otomatik yeniden açıyor:
```python
c = ModbusClient(host='192.168.1.100', auto_open=True, auto_close=True)
while True:
    regs = c.read_holding_registers(0, 10)
    if regs:
        print(regs)
    time.sleep(1)
# Bağlantı kopsa da otomatik açıyor — reconnect kodu gerekmez.
```

## İlgili Konular

```
knowledge/protocols/modbus-tcp/
├── 01_protocol_basics.md        → Protokol ve MBAP header
├── 02_register_model.md         → Register tipleri ve float kodlama
├── 03_function_codes.md         → FC03/04/16 referansı
└── 04_codesys_slave_config.md   → Bağlanılan CODESYS slave yapısı

Kütüphane kaynakları:
  pymodbus         → https://pymodbus.org
  pyModbusTCP      → https://pymodbustcp.readthedocs.io
  jsmodbus         → https://github.com/Cloud-Automation/node-modbus
  modbus-serial    → https://github.com/yaacov/node-modbus-serial

Test araçları:
  Modbus Slave    → Gerçek PLC olmadan test sunucu simülatörü
  Modbus Poll     → GUI master test aracı
  Wireshark       → Frame seviyesi analiz
```
