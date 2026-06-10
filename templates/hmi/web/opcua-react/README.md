# OPC-UA + React Web HMI Başlangıç Şablonu

PLC'ye OPC-UA ile bağlanan, verisini WebSocket üzerinden tarayıcıya yayan
ve tarayıcıdan gelen yazma komutlarını PLC'ye ileten tam çalışan bir
endüstriyel web HMI iskeleti.

Tarayıcı `opc.tcp://` ham TCP soketi açamaz (güvenlik sandbox'ı). Bu yüzden
arada bir **gateway** zorunludur: PLC tarafında OPC-UA, tarayıcı tarafında
WebSocket konuşur ve ikisini çevirir. Bu bir mimari kısıttır, tercih değil.

## Mimari

```
┌──────────────┐   opc.tcp (binary)   ┌──────────────────────┐   WebSocket (JSON)   ┌─────────────────┐
│   PLC        │◄────────────────────►│  GATEWAY (Node.js)   │◄────────────────────►│  TARAYICI       │
│  CODESYS     │                      │                      │                      │  (React/Vite)   │
│  OPC-UA      │   subscription /     │  node-opcua  (PLC)   │   TAG_UPDATE  ───►    │                 │
│  Server      │   monitored items    │  ws          (browser)│   BATCH_UPDATE ───►  │  useOpcUa hook  │
│              │                      │                      │   CONNECTION_STATUS  │  Zustand store  │
│  GVL_HMI     │   writeNode  ◄────   │  OpcuaManager        │   ◄─── WRITE_TAG     │  bileşenler     │
│  (tag'ler)   │                      │  HmiWsServer         │   WRITE_ACK   ───►    │                 │
└──────────────┘                      └──────────────────────┘                      └─────────────────┘
        ▲                                                                                     │
        │  PLC her saniye uHeartbeat artırır ── HMI bunu izleyerek "veri donmuş mu" anlar ───┘
```

- **Gateway** (`gateway/`): tek OPC-UA bağlantısı, N tarayıcı istemcisi.
  Subscription değişimlerini 100ms batch'lerle yayar, son-değer önbelleği tutar
  (yeni bağlanan istemci anında `FULL_UPDATE` snapshot alır), bağlantı kopunca
  otomatik yeniden bağlanır.
- **Frontend** (`frontend/`): singleton WebSocket (her bileşen kendi bağlantısını
  açmaz), Zustand granüler selector (yalnız değişen bileşen render olur),
  heartbeat tabanlı bağlantı göstergesi, alarm paneli ve yazma komutları.

## Klasör Yapısı

```
opcua-react/
├── README.md
├── gateway/                  # Node.js OPC-UA <-> WebSocket köprüsü
│   ├── package.json
│   ├── .env.example          # PLC endpoint, nodeId namespace, WS port, auth
│   ├── config.js             # TAG eşlemesi (MONITORED_TAGS / WRITABLE_TAGS)
│   ├── opcuaManager.js       # node-opcua: bağlantı, subscription, write, reconnect
│   ├── wsServer.js           # ws: broadcast, batch, FULL_UPDATE, WRITE_ACK, ping
│   └── server.js             # giriş noktası
└── frontend/                 # React (Vite) HMI
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── .env.example          # VITE_WS_URL, VITE_WRITE_AUTH_TOKEN
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── styles.css
        ├── tagMeta.js          # E_ZoneState enum + alarm tanımları
        ├── store/hmiStore.js   # Zustand store (düz tag haritası)
        ├── hooks/
        │   ├── useOpcUa.js     # singleton WebSocket bağlantı + writeTag
        │   └── useTagValue.js  # granüler tag selector + stale tespiti
        └── components/
            ├── ConnectionStatus.jsx  # heartbeat tabanlı durum
            ├── AlarmPanel.jsx        # aktif alarmlar (ISA-18.2 esinli)
            ├── ZonePanel.jsx         # bölge kartı (durum/hız/komut)
            ├── TagValue.jsx          # tek değer göstergesi
            └── CommandButton.jsx     # PLC'ye yazma komutu
```

## Kurulum

İki ayrı `npm install` gerekir (gateway ve frontend bağımsız paketlerdir):

```bash
# Gateway
cd gateway
npm install
cp .env.example .env        # değerleri düzenle (en az OPCUA_ENDPOINT)

# Frontend
cd ../frontend
npm install
cp .env.example .env        # gerekirse VITE_WS_URL düzenle
```

## Çalıştırma

İki terminal:

```bash
# Terminal 1 — Gateway (PLC'ye bağlanır, ws://0.0.0.0:8080 açar)
cd gateway
npm start            # veya: npm run dev  (dosya değişiminde otomatik yeniden başlat)

# Terminal 2 — Frontend (http://localhost:5173)
cd frontend
npm run dev
```

PLC olmadan denemek için herhangi bir OPC-UA test sunucusu kullanılabilir; tag
yolları eşleşmezse `Bad_NodeIdUnknown` loglanır ama gateway çökmez.

## Konfigürasyon

### PLC endpoint ve namespace (`gateway/.env`)

- `OPCUA_ENDPOINT` — örn. `opc.tcp://192.168.1.100:4840`
- `OPCUA_NAMESPACE_URI` — namespace **index** bundan dinamik çözülür.
  `ns=4` gibi hardcode etme; farklı CODESYS sürümleri farklı index atar.

### Tag eşlemesi (`gateway/config.js`)

Bu şablon **EXAMPLE_conveyor** projesinin `GVL_HMI` değişkenlerine göre örneklenmiştir:

| Frontend tag        | CODESYS değişkeni        | Yön            | Tip        |
|---------------------|--------------------------|----------------|------------|
| `aZoneState_1..3`   | `aZoneState[1..3]`       | oku (izleme)   | E_ZoneState|
| `aZoneSpeed_1..3`   | `aZoneSpeed[1..3]`       | oku (izleme)   | REAL m/dk  |
| `aZoneRunning_1..3` | `aZoneRunning[1..3]`     | oku (izleme)   | BOOL       |
| `aZoneJam_1..3`     | `aZoneJam[1..3]`         | oku (alarm)    | BOOL       |
| `aZoneSpdFlt_1..3`  | `aZoneSpdFlt[1..3]`      | oku (alarm)    | BOOL       |
| `xEStopActive`      | `xEStopActive`           | oku (alarm)    | BOOL       |
| `xRunPermit`        | `xRunPermit`             | oku            | BOOL       |
| `xZone2Itlk`        | `xZone2Itlk`             | oku (alarm)    | BOOL       |
| `xAnyAlarm`         | `xAnyAlarm`              | oku            | BOOL       |
| `uHeartbeat`        | `uHeartbeat`             | oku (canlılık) | UDINT      |
| `cmdAutoRun_1..3`   | `axCmdAutoRun[1..3]`     | **yaz** (komut)| BOOL       |
| `cmdReset`          | `xCmdReset`              | **yaz** (komut)| BOOL       |

Kendi projende:
1. `SYMBOL_PREFIX` değerini kendi runtime/GVL yoluna göre düzelt
   (UaExpert ile gerçek node yolunu doğrula).
2. `MONITORED_TAGS` listesine kendi izleme tag'lerini ekle, `sampling` (ve gerekirse
   analoglar için `deadband`) ver.
3. `WRITABLE_TAGS` içinde her komut için doğru `dataType` ver: CODESYS `REAL` → `"Float"`,
   `LREAL` → `"Double"`, `BOOL` → `"Boolean"`. Yanlış tip `Bad_TypeMismatch` ile
   sessiz yazma reddine yol açar.

### Heartbeat

PLC `uHeartbeat`'i her saniye artırır. Frontend `ConnectionStatus` bu değerin
değişimini izler: gateway "CONNECTED" dese bile heartbeat 3 sn ilerlemiyorsa
ekran **DEGRADED (veri donmuş)** uyarısı verir. Bu, gateway-PLC arası sessiz
kopmayı (NAT/firewall idle drop) yakalar.

## Güvenlik Notları

- **Gateway internal ağda kalmalı.** PLC'ye yazma yetkisine sahip bu süreç
  internete açılmamalıdır. Tarayıcı yalnız gateway'in WebSocket'ine bağlanır,
  PLC'ye asla doğrudan erişmez.
- **OPC-UA güvenlik politikası.** Geliştirmede `None` kabul edilebilir; üretimde
  `OPCUA_SECURITY_MODE=SignAndEncrypt` + `OPCUA_SECURITY_POLICY=Basic256Sha256`
  kullan ve sunucu sertifikasını trusted store'a ekle.
- **WSS (TLS).** Üretimde WebSocket'i şifrele (`wss://`): tüm PLC komutları aksi
  halde açık metin gider. Tipik desen: Nginx SSL termination + `wss://`
  (Nginx'te `proxy_read_timeout 3600s` + `Upgrade/Connection` header'ları gerekir,
  yoksa idle WebSocket 60 sn'de sessizce kopar).
- **Yazma kimlik doğrulaması.** Bu şablon basit paylaşılan token (`WRITE_AUTH_TOKEN`)
  içerir; üretimde gerçek oturum/JWT + rol bazlı yetki ile değiştir. Token boşsa
  yazma doğrulaması kapalıdır — yalnız geliştirme için.
- **Yazma denetim kaydı (audit).** Gateway her yazmayı loglar (kim/ne/sonuç).
  Üretimde kalıcı bir audit log'a yaz.
- **Bağlantı kopunca yazma kilidi.** Frontend, WebSocket veya PLC bağlantısı
  kopukken tüm komut butonlarını devre dışı bırakır (komut nereye gideceği belirsiz
  bir duruma gitmesin).

## Sürüm Notları

- Node.js ≥ 20 (gateway ESM kullanır).
- `node-opcua` ^2.155, `ws` ^8.18, React 18, Vite 6, Zustand 5.
