# modbus-react — Web Tabanlı HMI Başlangıç Şablonu (React + Modbus TCP)

Modbus TCP konuşan bir PLC/slave'i web tarayıcısından izlemek ve kontrol etmek
için tam çalışan bir başlangıç projesi. `EXAMPLE_conveyor` (3 bölgeli konveyör)
io_list mantığını örnek register haritası olarak kullanır.

---

## Mimari — Neden Gateway Zorunlu?

**Tarayıcı doğrudan Modbus TCP konuşamaz.** Modbus TCP ham TCP soketi (port 502)
gerektirir; tarayıcının JavaScript ortamı yalnızca HTTP(S), WebSocket ve WebRTC
açabilir (güvenlik sandbox'ı), rastgele TCP soketi açamaz. Bu yüzden aralarına
bir **Node.js gateway** koymak mimari bir zorunluluktur:

```
┌──────────────┐   WebSocket    ┌─────────────────┐   Modbus TCP    ┌─────────┐
│  React HMI   │ ◄────────────► │  Gateway        │ ◄─────────────► │  PLC /  │
│ (tarayıcı)   │   ws:// :8080  │  (Node.js)      │   tcp:// :502   │  slave  │
└──────────────┘                └─────────────────┘                 └─────────┘
   - WS hook                       - jsmodbus master                  - coil
   - Zustand store                 - periyodik polling                - discrete in
   - granüler render               - delta yayını (sadece değişen)     - input reg
   - coil/register yazma           - write proxy (FC05/06/16)          - holding reg
                                   - otomatik reconnect
```

**Veri akışı:**
1. Gateway PLC'ye Modbus TCP master olarak bağlanır.
2. Register/coil bloklarını periyodik okur (Modbus'ta subscription yoktur — polling kaçınılmazdır).
3. Yalnızca **değişen** tag'leri WebSocket ile tüm tarayıcılara iter (delta yayını).
4. Tarayıcıdan gelen yazma komutlarını (`WRITE_COIL`/`WRITE_REGISTER`) PLC'ye iletir.
5. Bağlantı kopunca otomatik yeniden bağlanır; tarayıcı da WS'i exponential backoff ile yeniden kurar.

---

## Modbus Adres Modeli

Modbus'ta **4 ayrı adres uzayı** vardır (hepsi 0-tabanlı). io_list.csv'deki
PLC I/O yönü bu uzaylara şöyle eşlenir:

| Bölge            | Function Code | Yön        | Tip    | io_list karşılığı            |
|------------------|---------------|------------|--------|------------------------------|
| **Coil**         | FC01 oku / FC05 yaz | Oku+Yaz | bool | **DO** (`%QX`) — motor, lamba, korna |
| **Discrete Input** | FC02 oku    | Salt oku | bool   | **DI** (`%IX`) — buton, sensör, seçici |
| **Input Register** | FC04 oku    | Salt oku | 16-bit | **AI** (`%IW`) — takometre, ölçüm |
| **Holding Register** | FC03 oku / FC06,FC16 yaz | Oku+Yaz | 16-bit | Setpoint, komut, reçete |

> **Önemli (0-tabanlı adres):** Dokümanlardaki "40101" gibi 4xxxx referansları
> 1-tabanlıdır. Kodda `40101 - 40001 = 100` → `readHoldingRegisters(100, 1)`.
>
> **Sürekli blok kuralı:** Modbus okuması bitişik bir adres bloğu okur, deliklerin
> üzerinden geçemez (boşlukta Exception 0x02). İlgili tag'leri adres uzayında yan
> yana yerleştirin.
>
> **16-bit gerçeği:** Her register ham 16-bit'tir. float32/int32 = 2 register; word
> ve byte sırası (endian/swap) **cihaza özeldir, standart değildir**. Bu şablon
> takometreyi tek register + 4-20mA ölçek olarak çözer; float gereken cihazlarda
> `register-map.js`'e bir `decode` fonksiyonu ekleyin (knowledge Not 4).

---

## Proje Yapısı

```
modbus-react/
├── README.md
├── gateway/                  # Node.js Modbus -> WebSocket köprüsü
│   ├── package.json          #   jsmodbus + ws + dotenv (ESM)
│   ├── server.js             #   ModbusManager (polling/reconnect) + WS sunucu
│   ├── register-map.js       #   TAG_MAP: coil/discrete/input/holding tanımları
│   ├── .env.example          #   PLC IP, port, poll hızı, WS portu, yazma token'ı
│   └── .gitignore
└── frontend/                 # React (Vite) HMI
    ├── package.json          #   react + react-dom + zustand
    ├── vite.config.js
    ├── index.html
    ├── .env.example          #   VITE_WS_URL, VITE_WRITE_TOKEN
    ├── .gitignore
    └── src/
        ├── main.jsx
        ├── App.jsx           #   3 bölgeli konveyör ekranı
        ├── config.js         #   WS adresi, stale eşiği
        ├── styles.css        #   ISA-101 esinli koyu tema
        ├── store/
        │   └── hmiStore.js   #   Zustand: tags, meta, alarms, connection
        ├── hooks/
        │   ├── useWebSocket.js   # Singleton WS + reconnect + sendWrite
        │   └── useTagValue.js    # Granüler tag selector + stale tespiti
        └── components/
            ├── ConnectionBanner.jsx
            ├── BoolIndicator.jsx     # coil/discrete bool gösterimi
            ├── AnalogDisplay.jsx     # input/holding register + bar + alarm
            ├── CoilControl.jsx       # FC05 yazma (AÇ/KAPA)
            ├── SetpointControl.jsx   # FC06 yazma (setpoint girişi)
            └── AlarmPanel.jsx        # ISA-18.2 öncelikli aktif alarm listesi
```

---

## Kurulum ve Çalıştırma

**Gereksinim:** Node.js 20+

### 1. Gateway

```bash
cd gateway
npm install
cp .env.example .env        # MODBUS_HOST'u PLC IP'nizle güncelleyin
npm start                   # veya: npm run dev  (--watch ile otomatik yeniden başlatma)
```

Gateway varsayılan olarak `ws://localhost:8080` üzerinde WebSocket sunar ve
`.env`'deki `MODBUS_HOST:MODBUS_PORT` adresindeki PLC'ye bağlanır.

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env        # gerekirse VITE_WS_URL'i ayarlayın
npm run dev                 # Vite dev sunucu -> http://localhost:5173
```

Üretim derlemesi: `npm run build` (çıktı `dist/`), `npm run preview` ile önizleme.

### Gerçek PLC olmadan test

`jsmodbus`'un kendi `Modbus.server.TCP` sınıfı ile sahte bir slave yazıp
gateway'i ona (`MODBUS_PORT=1502`) yönlendirebilirsiniz. Bu şablon bu yöntemle
uçtan uca (FULL_UPDATE → delta → alarm → write-ack) test edilmiştir.

---

## Register Haritası Nasıl Uyarlanır

Tek değiştirmeniz gereken dosya: **`gateway/register-map.js`**.

`TAG_MAP` içindeki her tag bir kayıttır:

```js
zn1_motor_run: { type: "COIL", address: 0, writable: true, kind: "bool",
                 label: "Bölge 1 Motor", plcTag: "ZN1_MTR_01_Run" },

zn1_speed:     { type: "IR", address: 0, kind: "analog", unit: "m/dk",
                 decode: (raw) => scale4_20mA(raw, 0, 120),
                 label: "Bölge 1 Hız", plcTag: "ZN1_TAC_01_Speed" },

zn1_speed_sp:  { type: "HR", address: 0, writable: true, kind: "analog",
                 scale: 10, unit: "m/dk", min: 0, max: 120, step: 0.5,
                 label: "Bölge 1 Hız Setpoint" },

zn1_jam:       { type: "DI", address: 3, kind: "bool", label: "Bölge 1 Sıkışma",
                 alarm: { priority: "HIGH", text: "Bölge 1 sıkışma algılandı" } },
```

Alan açıklamaları:

| Alan        | Anlamı |
|-------------|--------|
| `type`      | `COIL` / `DI` / `IR` / `HR` (adres uzayı) |
| `address`   | İlgili uzayda 0-tabanlı adres |
| `writable`  | `true` → frontend yazabilir (yalnızca COIL ve HR) |
| `kind`      | `bool` / `int` / `analog` (frontend gösterim ipucu) |
| `scale`     | HR/IR için lineer bölme: ham `/ scale`. Yazarken `× scale` |
| `decode`    | `(raw) => number` özel çözücü (scale yerine; örn. 4-20mA, float32) |
| `unit/min/max/step` | Meta: gösterim ve setpoint giriş doğrulaması |
| `alarm`     | `{ priority, text }` → DI/COIL alarm üretir |
| `invertAlarm` | `true` → değer FALSE iken alarm aktif (NC sağlıklı sinyal, örn. acil durdurma) |

**Okuma blokları otomatiktir:** `READ_BLOCKS`, `TAG_MAP`'teki min..max adresten
her uzay için tek bitişik blok çıkarır. Adres uzayınızda büyük boşluklar varsa
`register-map.js`'de blokları elle bölün (yoksa Exception 0x02 alırsınız).

Frontend `TAG_META` mesajıyla bu meta'yı otomatik alır; çoğu durumda
frontend'de bir şey değiştirmenize gerek kalmaz — sadece `App.jsx`'te hangi
tag'lerin hangi bileşende gösterileceğini düzenlersiniz.

---

## WebSocket Mesaj Protokolü

**Gateway → Tarayıcı:**
- `FULL_UPDATE` — bağlantıda mevcut tüm tag değerleri + PLC durumu
- `TAG_META` — tag meta sözlüğü (label, unit, writable, alarm...)
- `TAG_UPDATE` — tek tag değişimi `{ tag, value, timestamp }` (delta)
- `CONNECTION_STATUS` — PLC↔gateway durumu (`CONNECTED`/`DISCONNECTED`/...)
- `ALARM` — `{ tag, active, priority, text, label, timestamp }`
- `WRITE_ACK` — `{ tag, success, error? }`

**Tarayıcı → Gateway:**
- `WRITE_COIL` — `{ tag, value: bool, token }` (FC05)
- `WRITE_REGISTER` — `{ tag, value: number, token }` (FC06; ölçekleme gateway'de)
- `REQUEST_FULL_UPDATE` — tam durum iste (sekme arka plandan dönünce)
- `PONG` — heartbeat yanıtı

---

## Güvenlik Notu (ÖNEMLİ)

**Modbus'ta kimlik doğrulama yoktur.** Protokol şifresiz ve kimlik denetimsizdir:
port 502'ye ulaşan herkes register okuyabilir ve **yazabilir**. Bu yüzden:

1. **Gateway'i ve PLC'yi izole bir endüstriyel ağda (OT VLAN) tutun.** PLC asla
   doğrudan internete veya kurumsal IT ağına açılmamalıdır. Gateway, OT ağı ile
   HMI istemcileri arasındaki tek köprü olmalıdır (firewall/DMZ).
2. **WebSocket katmanında yazma yetkisi:** `WRITE_TOKEN` (.env) ayarlandığında
   frontend her yazma isteğinde aynı token'ı göndermek zorundadır. Bu basit bir
   guard'dır — **gerçek kimlik doğrulama yerine geçmez.** Üretimde JWT/oturum
   tabanlı auth + rol bazlı yetki (operatör/mühendis) + yazma audit log'u ekleyin.
3. **Üretimde `wss://` (TLS) kullanın.** `ws://` şifresizdir; tüm PLC komutları
   açık metin geçer. Nginx SSL termination veya gateway'de HTTPS sunucu.
4. **Sunucu tarafı doğrulama:** Yazma değerleri gateway'de `min/max` ile
   doğrulanır; istemciye güvenmeyin.
5. **Yazma audit:** Gateway her yazmayı loglar (`[write] ...`). Gerçek projede
   kim/ne zaman/ne yazdı bilgisini kalıcı (dosya/DB) tutun.

---

## İlgili Knowledge Belgeleri

- `knowledge/hmi/web-based/02_modbus_clients_js.md` — jsmodbus master, polling, reconnect
- `knowledge/hmi/web-based/03_react_patterns.md` — Zustand granüler selector, React.memo
- `knowledge/hmi/web-based/05_realtime_websocket.md` — WS köprü, heartbeat, backpressure
- `knowledge/hmi/architecture/03_alarm_management.md` — ISA-18.2 alarm yaşam döngüsü
- `knowledge/protocols/modbus-tcp/` — register modeli ve function code referansı
