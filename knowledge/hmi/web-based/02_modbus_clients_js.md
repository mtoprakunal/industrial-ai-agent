---
KONU        : JavaScript ile Modbus TCP İstemci Geliştirme
KATEGORİ    : hmi
ALT_KATEGORI: web-based
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://github.com/Cloud-Automation/node-modbus"
    başlık: "GitHub — Cloud-Automation/node-modbus (jsmodbus)"
    güvenilirlik: topluluk
  - url: "https://www.npmjs.com/package/jsmodbus"
    başlık: "npm — jsmodbus Package"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_opcua_clients_js.md"
    ilişki: alternatif
  - konu: "05_realtime_websocket.md"
    ilişki: tamamlar
  - konu: "03_react_patterns.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/modbus-tcp/05_client_implementations.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "Modbus TCP register model (protocols/modbus-tcp/02_register_model.md)"
  - "Node.js ve async/await temelleri"
ÇELİŞKİLER :
  - kaynak: "jsmodbus vs modbus-serial — hangisi?"
    konu: "İki farklı Node.js Modbus kütüphanesi, farklı API tasarımı"
    çözüm: >
      jsmodbus: Yalnızca Modbus TCP, Promise tabanlı, daha temiz API.
      modbus-serial: TCP + RTU + ASCII + diğer, callback ve Promise karışık.
      Web HMI backend için: jsmodbus yeterli ve daha basit.
      RTU/seri port da gerekiyorsa: modbus-serial tercih et.
---

## Özün Ne

Web tabanlı bir HMI'ın Modbus TCP destekleyen PLC'lere bağlanması için Node.js backend'de bir Modbus istemcisi gerekir. Bu istemci, PLC register'larını belirli aralıklarla okur (polling), verileri normalize eder ve WebSocket aracılığıyla tarayıcıya iletir. Modbus TCP, OPC UA'nın aksine subscription mekanizmasına sahip değildir — polling kaçınılmazdır. Verimli polling tasarımı, bağlantı koptuğunda otomatik yeniden bağlanma ve hata toleransı bu belgenin temel konularıdır.

## Nasıl Çalışır

### Kurulum

```bash
npm install jsmodbus
# veya modbus-serial (TCP + RTU + diğer)
npm install modbus-serial
```

### jsmodbus ile Temel Bağlantı

```typescript
import net from 'net';
import Modbus from 'jsmodbus';

const socket = new net.Socket();
const client = new Modbus.client.TCP(socket, 1);  // Unit ID = 1

socket.connect({ host: '192.168.1.100', port: 502 });

socket.on('connect', async () => {
    console.log('Modbus bağlantısı kuruldu');

    // FC03: Holding Register oku
    const hrResult = await client.readHoldingRegisters(0, 10);
    const regs = hrResult.response.body.values;
    console.log(`HR[0-9]: ${regs}`);
    console.log(`Hız SP: ${regs[0] / 10.0} m/dk`);

    // FC04: Input Register oku
    const irResult = await client.readInputRegisters(0, 5);
    const ir = irResult.response.body.values;
    console.log(`Gerçek Hız: ${ir[0] / 10.0} m/dk`);
    console.log(`Sıcaklık: ${ir[1] / 10.0} °C`);

    // FC01: Coil oku
    const coilResult = await client.readCoils(0, 4);
    console.log(`Coils: ${coilResult.response.body.values}`);

    // FC05: Tek Coil yaz
    await client.writeSingleCoil(0, true);

    // FC06: Tek Register yaz (Hız SP = 45.0 → 450)
    await client.writeSingleRegister(0, 450);

    // FC16: Çoklu Register yaz
    await client.writeMultipleRegisters(0, [450, 856, 3]);
});

socket.on('error', (err) => console.error(`Socket error: ${err.message}`));
socket.on('close', () => console.log('Bağlantı kapandı'));
```

### Float32 Yardımcı Fonksiyonları

```typescript
import { Buffer } from 'buffer';

/**
 * İki Modbus Holding Register'dan Big-Endian float32 oku.
 * registers[0] = High Word (AB), registers[1] = Low Word (CD)
 */
function registersToFloat32BE(registers: number[]): number {
    const buf = Buffer.allocUnsafe(4);
    buf.writeUInt16BE(registers[0], 0);
    buf.writeUInt16BE(registers[1], 2);
    return buf.readFloatBE(0);
}

/**
 * Float32'yi iki Big-Endian register'a dönüştür.
 */
function float32ToRegisters(value: number): [number, number] {
    const buf = Buffer.allocUnsafe(4);
    buf.writeFloatBE(value, 0);
    return [buf.readUInt16BE(0), buf.readUInt16BE(2)];
}

/**
 * 32-bit üretim sayacını iki register'dan oku.
 */
function registersToUint32(registers: number[]): number {
    return (registers[0] << 16) | registers[1];
}

// Kullanım:
const regs = hrResult.response.body.values;
const flowRate = registersToFloat32BE([regs[10], regs[11]]);
const prodCount = registersToUint32([regs[3], regs[4]]);
```

### Production-Ready Modbus Manager

```typescript
import net from 'net';
import Modbus from 'jsmodbus';
import { EventEmitter } from 'events';

// Register haritasını merkezi tanımla
interface TagDefinition {
    register: number;        // Register adresi (0-tabanlı)
    type: "HR" | "IR" | "COIL" | "DI";
    scale?: number;          // Bölünecek değer (ör: 10 → ×0.1)
    decode?: "uint32" | "float32_be" | "float32_swap"; // Özel decode
    unit?: string;
}

const TAG_MAP: Record<string, TagDefinition> = {
    speed_setpoint:     { register: 0,  type: "HR", scale: 10, unit: "m/dk" },
    temp_setpoint:      { register: 1,  type: "HR", scale: 10, unit: "°C" },
    recipe_id:          { register: 2,  type: "HR", unit: "" },
    command_register:   { register: 10, type: "HR", unit: "" },
    actual_speed:       { register: 0,  type: "IR", scale: 10, unit: "m/dk" },
    actual_temp:        { register: 1,  type: "IR", scale: 10, unit: "°C" },
    actual_pressure:    { register: 2,  type: "IR", scale: 100, unit: "bar" },
    status_register:    { register: 3,  type: "IR", unit: "" },
    production_count:   { register: 4,  type: "IR", decode: "uint32", unit: "adet" },
    flow_rate_sp:       { register: 10, type: "HR", decode: "float32_be", unit: "L/dk" },
    motor_run_cmd:      { register: 0,  type: "COIL" },
    motor_running:      { register: 0,  type: "DI" },
    motor_fault:        { register: 1,  type: "DI" },
};

type ConnectionStatus = "DISCONNECTED" | "CONNECTING" | "CONNECTED" | "ERROR";

class ModbusManager extends EventEmitter {
    private socket: net.Socket;
    private client: any;  // jsmodbus client
    private status: ConnectionStatus = "DISCONNECTED";
    private pollInterval: NodeJS.Timeout | null = null;
    private reconnectTimer: NodeJS.Timeout | null = null;
    private lastValues: Record<string, any> = {};

    constructor(
        private readonly host: string,
        private readonly port = 502,
        private readonly slaveId = 1,
        private readonly pollMs = 500,
        private readonly reconnectMs = 5000
    ) {
        super();
    }

    async connect(): Promise<void> {
        if (this.status === "CONNECTING") return;
        this.setStatus("CONNECTING");
        
        this.socket = new net.Socket();
        this.client = new Modbus.client.TCP(this.socket, this.slaveId);
        
        this.socket.connect({ host: this.host, port: this.port });
        
        this.socket.on("connect", () => {
            this.setStatus("CONNECTED");
            this.startPolling();
        });
        
        this.socket.on("error", (err) => {
            console.error(`Modbus socket error: ${err.message}`);
            this.setStatus("ERROR");
            this.stopPolling();
            this.scheduleReconnect();
        });
        
        this.socket.on("close", () => {
            console.log("Modbus connection closed");
            this.setStatus("DISCONNECTED");
            this.stopPolling();
            this.scheduleReconnect();
        });
    }

    private startPolling(): void {
        if (this.pollInterval) return;
        this.pollInterval = setInterval(() => this.poll(), this.pollMs);
    }

    private stopPolling(): void {
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
            this.pollInterval = null;
        }
    }

    private async poll(): Promise<void> {
        if (this.status !== "CONNECTED") return;
        
        try {
            // Toplu okuma — verimli (tek TCP round-trip)
            const [hrResult, irResult, coilResult, diResult] = await Promise.all([
                this.client.readHoldingRegisters(0, 20),
                this.client.readInputRegisters(0, 10),
                this.client.readCoils(0, 4),
                this.client.readDiscreteInputs(0, 4)
            ]);

            const hr = hrResult.response.body.values;
            const ir = irResult.response.body.values;
            const coils = coilResult.response.body.values;
            const dis = diResult.response.body.values;

            // Değerleri decode et
            const updates: Record<string, any> = {
                speed_setpoint:   hr[0] / 10.0,
                temp_setpoint:    hr[1] / 10.0,
                recipe_id:        hr[2],
                command_register: hr[10],
                flow_rate_sp:     registersToFloat32BE([hr[10], hr[11]]),
                actual_speed:     ir[0] / 10.0,
                actual_temp:      ir[1] / 10.0,
                actual_pressure:  ir[2] / 100.0,
                status_register:  ir[3],
                production_count: registersToUint32([ir[4], ir[5]]),
                motor_run_cmd:    coils[0],
                motor_running:    dis[0],
                motor_fault:      dis[1],
            };

            // Yalnızca değişen değerleri yayınla (CPU tasarrufu)
            for (const [tag, value] of Object.entries(updates)) {
                if (this.lastValues[tag] !== value) {
                    this.lastValues[tag] = value;
                    this.emit("tagUpdate", {
                        tag,
                        value,
                        quality: "GOOD",
                        timestamp: new Date()
                    });
                }
            }

        } catch (err: any) {
            console.error(`Poll error: ${err.message}`);
            if (err.message?.includes("connection")) {
                this.setStatus("DISCONNECTED");
                this.stopPolling();
                this.scheduleReconnect();
            }
        }
    }

    async writeRegister(tag: string, value: number): Promise<boolean> {
        if (this.status !== "CONNECTED") return false;
        
        const tagDef = TAG_MAP[tag];
        if (!tagDef || tagDef.type !== "HR") return false;
        
        try {
            let scaledValue = value;
            if (tagDef.scale) scaledValue = Math.round(value * tagDef.scale);
            
            if (tagDef.decode === "float32_be") {
                const [hw, lw] = float32ToRegisters(value);
                await this.client.writeMultipleRegisters(tagDef.register, [hw, lw]);
            } else {
                await this.client.writeSingleRegister(tagDef.register, scaledValue);
            }
            return true;
        } catch (err) {
            console.error(`Write error for ${tag}: ${err}`);
            return false;
        }
    }

    async writeCoil(tag: string, value: boolean): Promise<boolean> {
        if (this.status !== "CONNECTED") return false;
        const tagDef = TAG_MAP[tag];
        if (!tagDef || tagDef.type !== "COIL") return false;
        
        try {
            await this.client.writeSingleCoil(tagDef.register, value);
            return true;
        } catch (err) {
            return false;
        }
    }

    private scheduleReconnect(): void {
        if (this.reconnectTimer) return;
        this.reconnectTimer = setTimeout(async () => {
            this.reconnectTimer = null;
            if (this.socket) this.socket.destroy();
            await this.connect();
        }, this.reconnectMs);
    }

    private setStatus(status: ConnectionStatus): void {
        this.status = status;
        this.emit("statusChange", status);
    }

    getStatus(): ConnectionStatus { return this.status; }
    
    disconnect(): void {
        this.stopPolling();
        if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
        this.socket?.destroy();
        this.setStatus("DISCONNECTED");
    }
}
```

### modbus-serial ile Alternatif (RTU + TCP)

```typescript
import ModbusRTU from 'modbus-serial';

const client = new ModbusRTU();
await client.connectTCP("192.168.1.100", { port: 502 });
client.setID(1);  // Unit/Slave ID

// Holding Register oku
const hrData = await client.readHoldingRegisters(0, 10);
console.log(`HR[0]: ${hrData.data[0] / 10.0}`);

// Input Register oku
const irData = await client.readInputRegisters(0, 5);
console.log(`IR[0]: ${irData.data[0] / 10.0}`);

// Float32 oku (2 register)
const buf = Buffer.allocUnsafe(4);
buf.writeUInt16BE(hrData.data[10], 0);
buf.writeUInt16BE(hrData.data[11], 2);
console.log(`Float: ${buf.readFloatBE(0)}`);

// Yazma
await client.writeRegister(0, 450);        // FC06
await client.writeRegisters(0, [450, 856]); // FC16
await client.writeCoil(0, true);            // FC05
```

### WebSocket Entegrasyonu

```typescript
// server.ts — Modbus → WebSocket köprüsü
import express from 'express';
import { WebSocketServer } from 'ws';

const app = express();
const wss = new WebSocketServer({ port: 8080 });
const wsClients = new Set<any>();

const modbusManager = new ModbusManager('192.168.1.100', 502, 1, 500);

wss.on("connection", (ws) => {
    wsClients.add(ws);
    // Mevcut tüm değerleri yeni istemciye gönder
    ws.send(JSON.stringify({
        type: "FULL_UPDATE",
        data: modbusManager["lastValues"],
        status: modbusManager.getStatus()
    }));
    ws.on("close", () => wsClients.delete(ws));
    
    // Tarayıcıdan yazma komutları al
    ws.on("message", async (raw) => {
        const msg = JSON.parse(raw.toString());
        if (msg.type === "WRITE_REGISTER") {
            await modbusManager.writeRegister(msg.tag, msg.value);
        } else if (msg.type === "WRITE_COIL") {
            await modbusManager.writeCoil(msg.tag, msg.value);
        }
    });
});

function broadcast(data: object) {
    const msg = JSON.stringify(data);
    wsClients.forEach(ws => { if (ws.readyState === 1) ws.send(msg); });
}

modbusManager.on("tagUpdate", (u) => broadcast({ type: "TAG_UPDATE", ...u }));
modbusManager.on("statusChange", (s) => broadcast({ type: "CONNECTION_STATUS", status: s }));

app.listen(3001);
modbusManager.connect();
```

## Örnekler

### Örnek 1: Durum Register Bit Analizi

```typescript
// Bir değişim olduğunda status register bitlerini analiz et
modbusManager.on("tagUpdate", ({ tag, value }) => {
    if (tag === "status_register") {
        const status = {
            running:     !!(value & 0x0001),
            fault:       !!(value & 0x0002),
            at_setpoint: !!(value & 0x0004),
            in_setup:    !!(value & 0x0008),
        };
        console.log(`Status: Running=${status.running}, Fault=${status.fault}`);
        broadcast({ type: "TAG_UPDATE", tag: "status_register_decoded", value: status });
    }
});
```

### Örnek 2: Setpoint Güncelleme Akışı (Frontend → Modbus)

```javascript
// Frontend React bileşeninde:
function SpeedSetpoint() {
    const [value, setValue] = useState(45.0);
    const { ws } = useWebSocket();
    
    const handleApply = () => {
        ws.send(JSON.stringify({
            type: "WRITE_REGISTER",
            tag: "speed_setpoint",
            value: value  // Ölçekleme backend'de yapılır
        }));
    };
    
    return (
        <div>
            <input type="number" value={value} onChange={e => setValue(+e.target.value)} />
            <button onClick={handleApply}>Uygula</button>
        </div>
    );
}
```

## Sık Yapılan Hatalar

### Hata 1: Promise.all Yerine Sıralı Okuma

```typescript
// ❌ YANLIŞ — Sıralı okuma: 3 round-trip
const hr = await client.readHoldingRegisters(0, 20);
const ir = await client.readInputRegisters(0, 10);
const coils = await client.readCoils(0, 4);
// Toplam gecikme: 3 × latency

// ✅ DOĞRU — Paralel okuma: 1 round-trip (yaklaşık)
const [hr, ir, coils] = await Promise.all([
    client.readHoldingRegisters(0, 20),
    client.readInputRegisters(0, 10),
    client.readCoils(0, 4)
]);
// NOT: Modbus senkron protokol; server sıralı işler.
// Promise.all TCP overhead'ı azaltır ama sırayı garanti etmez.
// Bazı PLC'ler eş zamanlı isteği desteklemez — test et.
```

### Hata 2: 0-Tabanlı Adres Yanlışlığı

```typescript
// Belge: "HR 40101 = Hız Setpoint"
// ❌ YANLIŞ
await client.readHoldingRegisters(101, 1);  // 40102 okunur!

// ✅ DOĞRU: Belge referansından 40001 çıkar
// 40101 - 40001 = 100
await client.readHoldingRegisters(100, 1);
```

### Hata 3: Hata Nesnesini Yutmak

```typescript
// ❌ YANLIŞ
try {
    await client.readHoldingRegisters(0, 10);
} catch (e) {
    // Hiçbir şey
}

// ✅ DOĞRU — Modbus exception code'larını logla
try {
    await client.readHoldingRegisters(0, 10);
} catch (e: any) {
    if (e.err === "ModbusException") {
        const exCode = e.response?.body?.exceptionCode;
        console.error(`Modbus Exception 0x${exCode?.toString(16)}: ${EXCEPTION_MESSAGES[exCode]}`);
    } else {
        console.error(`Network error: ${e.message}`);
        this.scheduleReconnect();
    }
}
```

## Gerçek Proje Notları

**Not 1 — Promise.all'ın PLC Uyumsuzluğu**  
Bir legacy PLC'de `Promise.all` ile eş zamanlı istek gönderildi. PLC yanıtları karıştırdı — bazı istemciler yanlış veri aldı. Çözüm: Sıralı istek (bekleme eklendiğinde). Modbus protokolü single-master; PLC bazıları eş zamanlı isteği yönetemiyor.

**Not 2 — Polling Hızı ve PLC CPU Yükü**  
500ms polling × 4 okuma = ~8 Modbus isteği/saniye. Bir zayıf CPU'lu PLC'de bu yük CPU'yu %30'a çıkardı. Polling 1000ms'ye yükseltildi, PLC kurtuldu. Kural: PLC belgesi max sorgu hızını belirtiyorsa aşma.

**Not 3 — Toplu Okuma Boyutu Sınırı**  
`readHoldingRegisters(0, 200)` isteği Exception 0x03 döndürdü. Modbus TCP spesifikasyonu max 125 register/istek. İki ayrı okumaya bölündü: `readHoldingRegisters(0, 125)` + `readHoldingRegisters(125, 75)`.

**Not 4 — Word Swap (Byte Order) Cihaz Bağımlı**  
Bir akışmetre float32 değerini "ters" gönderdi: `registersToFloat32BE([regs[10], regs[11]])` saçma sayı verdi ama `[regs[11], regs[10]]` sırasıyla doğru çıktı. Modbus float kodlaması standart değildir; cihazlar AB-CD, CD-AB, BA-DC, DC-BA dört byte sırasından birini kullanır (big/little endian × word swap). Çözüm: TagDefinition'a `decode: "float32_be" | "float32_le" | "float32_swap"` eklendi, her cihaz için doğru sıra deneme-yanılma ile saptanıp sabitlendi. Tek bir global float decode varsaymak en sık hatadır.

**Not 5 — Boşluklu Register Aralığında Exception**  
Register haritası 0-19 ve 100-105 kullanıyordu, arası boştu. `readHoldingRegisters(0, 106)` Exception 0x02 (Illegal Data Address) döndürdü çünkü 20-99 arası PLC'de tanımsızdı. Tek büyük okuma yerine iki ayrı blok okuma yapıldı (`0,20` + `100,6`). Modbus okuması sürekli bir adres bloğu gerektirir; deliklerin üzerinden geçemez.

**Not 6 — jsmodbus Socket Yeniden Kullanım Tuzağı**  
`socket.destroy()` sonrası aynı `net.Socket` nesnesi `connect()` ile yeniden kullanılmaya çalışıldı; "socket already destroyed" hatası alındı. jsmodbus'ta her yeniden bağlanmada **yeni** `net.Socket` ve **yeni** `Modbus.client.TCP` oluşturmak gerekir. Reconnect mantığında eski socket'in tüm listener'ları `removeAllListeners()` ile temizlenmeli, yoksa "MaxListenersExceededWarning" ve sızıntı oluşur.

**Not 7 — modbus-serial setTimeout Varsayılanı Çok Uzun**  
`modbus-serial` varsayılan timeout'u yoktu (sonsuz beklerdi); ağ kopunca poll fonksiyonu hiç dönmedi, poll interval'leri üst üste yığıldı. Çözüm: `client.setTimeout(2000)`. jsmodbus'ta ise timeout `Modbus.client.TCP(socket, unitId, timeout)` parametresi veya socket-level `setTimeout` ile verilir. Timeout olmadan tek bir cevapsız istek tüm polling döngüsünü kilitler.

## Edge Case'ler ve Sistem Limitleri

Modbus TCP, OPC UA'nın aksine **durumsuz, subscription'sız ve tip bilgisiz** bir protokoldür; sınırların çoğu bu sadelikten doğar.

| Edge Case | Tetikleyen | Belirti | Çözüm / Limit |
|---|---|---|---|
| Max 125 HR/istek | Tek okumada >125 register | Exception 0x03 | Blokları böl (Not 3) |
| Max 2000 coil/istek | Tek okumada >2000 coil (FC01/02) | Exception 0x03 | Blokları böl |
| Illegal Data Address | Boşluklu/tanımsız register (Not 5) | Exception 0x02 | Yalnızca tanımlı bloğu oku |
| Illegal Function | Cihaz FC desteklemiyor | Exception 0x01 | Cihaz tablosundan desteklenen FC'yi kullan |
| Slave Device Busy | Cihaz meşgul | Exception 0x06 | Backoff + yeniden dene |
| Word/byte order | float/int32 yanlış decode (Not 4) | Saçma sayı | Doğru endian/swap modu seç |
| TCP head-of-line | Tek socket, sıralı yanıt | Yavaş istek tümünü bekletir | İstek timeout (Not 7) |
| Eşzamanlı istek karışması | `Promise.all` legacy PLC'de | Yanlış veri eşleşmesi | Sıralı istek (Not 1) |
| Transaction ID taşması | >65535 işlem | Wrap-around (genelde sorunsuz) | Kütüphane yönetir; nadiren çakışma |
| Unit ID yanlış | Gateway arkası RTU cihaz | Timeout / boş yanıt | Doğru `setID()` / slaveId |
| Signed/unsigned | INT16 değer >32767 | Negatif görünür | `value > 32767 ? value - 65536 : value` |

**Modbus'ta veri kalitesi (quality) yoktur.** OPC UA'daki GOOD/BAD/UNCERTAIN karşılığı yoktur; başarılı okuma "GOOD" varsayılır. Bağlantı kopukken son okunan değer "stale" olur ama protokol bunu söylemez — stale tespiti tamamen backend'in sorumluluğudur (son başarılı poll zaman damgası).

**Pratik sınırlar:**
- Register/istek: HR/IR 125, Coil/DI 2000
- Aynı anda açık bağlantı/cihaz: çoğu PLC 1–4 (gateway arkası daha az)
- Pratik poll hızı: 100ms–1000ms (cihaz CPU'suna bağlı, Not 2)
- Round-trip latency: LAN'da 2–10ms, gateway/seri arkası 50–200ms

## Optimizasyon

Modbus'ta optimizasyonun tek hedefi vardır: **round-trip (istek-yanıt) sayısını ve PLC CPU yükünü minimize etmek.**

1. **Bitişik register'ları tek istekte oku.** En önemli kural. 20 ayrı `readHoldingRegisters(n, 1)` yerine `readHoldingRegisters(0, 20)`. Round-trip latency genelde gerçek transfer süresinden büyüktür; tek istek 20 kat daha hızlıdır.

2. **Register haritasını okuma için optimize tasarla.** İlişkili tag'leri register adres uzayında **yan yana** yerleştir ki tek blok okuma kapsasın. Boşluklar (Not 5) ya ekstra okuma ya da gereksiz veri transferi demektir.

3. **Delta yayını yap (sadece değişeni gönder).** Mevcut implementasyon `lastValues` ile bunu yapıyor — okunan tüm bloğu değil, yalnızca değişen tag'i WebSocket'e gönder. Modbus polling tüm bloğu okur ama tarayıcıya sadece değişim gitmeli.

4. **Poll hızını tag sınıfına göre ayır (multi-rate polling).** Her şeyi 200ms'de okumak yerine: kritik durum register'ı 200ms, analog değerler 500ms, üretim sayacı/reçete 5000ms. Bunu farklı interval'li ayrı poll döngüleriyle yap.

   ```typescript
   // Çok hızlı: alarm/durum bitleri
   setInterval(() => this.pollFast(), 200);
   // Orta: analog ölçümler
   setInterval(() => this.pollMedium(), 500);
   // Yavaş: sayaç, reçete, diagnostik
   setInterval(() => this.pollSlow(), 5000);
   ```

5. **Poll çakışmasını önle (re-entrancy guard).** Yavaş bir cihazda poll, interval'den uzun sürerse `setInterval` poll'ları üst üste tetikler. Bir `isPolling` bayrağı ile önceki poll bitmeden yenisini başlatma:

   ```typescript
   private isPolling = false;
   private async poll() {
       if (this.isPolling || this.status !== "CONNECTED") return;
       this.isPolling = true;
       try { /* okumalar */ } finally { this.isPolling = false; }
   }
   ```

6. **Timeout'u agresif ayarla.** Tek cevapsız istek tüm döngüyü kilitler (Not 7). 2 saniye timeout + reconnect, sonsuz beklemeden iyidir.

7. **Eşzamanlı istekten kaçın, ardışık zincirle.** `Promise.all` cazip ama Modbus single-master'dır (Not 1). Tek socket üzerinde ardışık `await` daha güvenlidir; latency'yi gerçek azaltan, paralellik değil, blok birleştirmedir (madde 1).

## Derin Teknik Detay

**Modbus neden subscription'a sahip değil, neden polling zorunlu?** Modbus, 1979'da Modicon PLC'leri için seri hat (RS-485) üzerinde tasarlandı. Saf master-slave (client-server) bir protokoldür: slave (PLC) **asla** kendiliğinden konuşamaz, yalnızca master'ın isteğine yanıt verir. Bu, çok-drop seri hatta çakışmayı (collision) önlemek için zorunluydu — tek master hattı yönetir. Modbus TCP, bu seri protokolü TCP'ye sardı (MBAP header eklendi) ama master-slave semantiğini korudu. Sonuç: TCP çift yönlü olsa da Modbus mantığı tek yönlü kalır; "değer değişti, beni haberdar et" diye bir mekanizma protokolde **yoktur**. Bu yüzden web HMI'da değişimi yakalamanın tek yolu periyodik okumadır (polling).

**MBAP header ve Transaction ID.** Modbus TCP her isteğe 7 byte'lık MBAP (Modbus Application Protocol) header ekler: Transaction ID (2), Protocol ID (2, hep 0), Length (2), Unit ID (1). Transaction ID, asenkron ortamda yanıtı isteğe eşlemek içindir — jsmodbus bunu otomatik artırır. Not 1'deki "yanıt karışması" sorunu, bazı basit PLC'lerin Transaction ID'yi yok sayıp gelen sırayla yanıt vermesinden kaynaklanır; bu durumda `Promise.all` ile gönderilen istekler yanlış eşlenir. Standart uyumlu cihazlarda Transaction ID eşleme bunu çözer, ama sahada uyumsuz cihaz çoktur — bu yüzden ardışık istek güvenli varsayılandır.

**Register tipsizliği ve "16-bit word" gerçeği.** Modbus'ta her register ham 16-bit'tir; float, int32, string gibi kavramlar protokolde yoktur. 32-bit float = 2 register, ama bu iki register'ın hangi sırayla birleşeceği (word order) ve byte'ların sırası (byte order) **cihaz üreticisinin** kararıdır, standart değildir. `Buffer.writeUInt16BE` + `readFloatBE` zinciri AB-CD sırasını varsayar; cihaz CD-AB kullanıyorsa register sırasını, BA-DC kullanıyorsa byte'ları swap'lemek gerekir (Not 4). Bu, Modbus'ın en çok zaman kaybettiren tuzağıdır ve tamamen "spesifikasyon dışı" bir alandır.

**Neden tarayıcı doğrudan Modbus konuşamaz?** Modbus TCP ham TCP soketi (port 502) gerektirir; tarayıcı yalnızca HTTP/WebSocket açabilir, rastgele TCP soketi açamaz (güvenlik kısıtı). Bu yüzden mimari kaçınılmaz: tarayıcı → WebSocket → Node.js bridge (jsmodbus/modbus-serial) → Modbus TCP → PLC. jsmodbus/modbus-serial **yalnızca Node.js'te** çalışır (`net` modülü gerektirir); `bundle` edip tarayıcıya koymaya çalışmak (webpack polyfill ile) anlamsızdır — tarayıcının TCP yeteneği yoktur. Bu mimari kısıt OPC UA ile aynıdır ve web HMI'da gateway/bridge katmanını zorunlu kılan temel sebeptir.

**jsmodbus vs modbus-serial iç tasarım farkı:** jsmodbus saf TCP/Promise odaklı, `net.Socket`'i dışarıdan alır (dependency injection) — bu yüzden socket yönetimi senin sorumluluğundadır (Not 6). modbus-serial socket'i içeride yönetir, RTU/ASCII/seri port + TCP destekler, ama API'si callback/Promise karışımıdır. Seri (RS-485) gateway arkası cihaz varsa modbus-serial; saf TCP ve temiz Promise akışı isteniyorsa jsmodbus.

## İlgili Konular

```
knowledge/hmi/web-based/
├── 01_opcua_clients_js.md       → OPC UA alternatifi (daha zengin özellik)
├── 03_react_patterns.md         → Frontend Modbus veri tüketimi
└── 05_realtime_websocket.md     → Modbus → WebSocket → Tarayıcı

knowledge/protocols/modbus-tcp/
├── 02_register_model.md         → Register adres ve ölçekleme
└── 03_function_codes.md         → FC01/03/04/05/06/16 referansı
```
