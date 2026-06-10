# OPC-UA + Vue 3 Web HMI Şablonu

Tarayıcı tabanlı endüstriyel HMI başlangıç projesi. PLC'ye **OPC-UA** ile bağlanır,
veriyi **WebSocket** üzerinden Vue 3 frontend'e iter, yazma komutlarını PLC'ye proxy'ler.

Örnek tag seti: `projects/EXAMPLE_conveyor` (3 bölgeli konveyör — `GVL_HMI`).

---

## Neden Gateway? (Mimari zorunluluk)

Tarayıcının JavaScript ortamı **ham TCP soketi açamaz** (güvenlik sandbox'ı) —
yalnızca HTTP(S), WebSocket ve WebRTC. OPC-UA ise `opc.tcp://` ham TCP gerektirir.
Bu yüzden tarayıcı OPC-UA'yı **doğrudan konuşamaz**; araya bir köprü (gateway) koymak
tercih değil, mimari bir zorunluluktur.

```
┌──────────────┐   OPC-UA          ┌──────────────────┐   WebSocket      ┌──────────────┐
│              │   (opc.tcp)       │  Node.js Gateway │   (ws/wss)       │  Vue 3 SPA   │
│  PLC / SoftPLC├──────────────────►│  node-opcua + ws ├──────────────────►│  (tarayıcı)  │
│  (CODESYS)   │◄──────────────────┤                  │◄─────────────────┤              │
└──────────────┘   write proxy      └──────────────────┘   WRITE komut     └──────────────┘
        1 OPC-UA subscription              1 köprü                  N tarayıcı (broadcast)
```

- **1 PLC bağlantısı → N tarayıcı**: tek OPC-UA subscription tüm istemcileri besler.
- Gateway: subscription, otomatik yeniden bağlanma, sertifika yönetimi, yazma proxy'si,
  heartbeat/ölü-bağlantı temizliği.
- Frontend: reaktif tag state (Pinia), gerçek zamanlı görüntüleme, alarm paneli, komut yazma,
  bağlantı durumu + heartbeat göstergesi.

---

## Dizin Yapısı

```
opcua-vue/
├── gateway/                  # Node.js OPC-UA <-> WebSocket köprüsü
│   ├── package.json          # node-opcua, ws, dotenv
│   ├── config.js             # .env okuma + TAG HARİTASI (GVL_HMI) + ALARM tanımları
│   ├── server.js             # OpcUaManager + WebSocket server + BatchManager
│   └── .env.example          # PLC endpoint, namespace URI, güvenlik, WS portu
│
├── frontend/                 # Vue 3 (Vite, Composition API, <script setup>)
│   ├── package.json          # vue, pinia, vite
│   ├── vite.config.js
│   ├── index.html
│   ├── .env.example          # VITE_WS_URL, VITE_WRITE_TOKEN
│   └── src/
│       ├── main.js
│       ├── styles.css
│       ├── App.vue
│       ├── store/hmi.js              # Pinia store: tags, alarms, bağlantı, heartbeat
│       ├── composables/
│       │   ├── useOpcUa.js           # WebSocket SINGLETON: reconnect, ping, writeTag
│       │   └── useTagValue.js        # tek tag'in reaktif değeri (value/quality/isStale)
│       └── components/
│           ├── ConnectionStatus.vue  # gateway/PLC durumu + heartbeat
│           ├── AlarmPanel.vue        # aktif alarmlar (ISA-18.2 öncelik sıralı)
│           ├── ZoneCard.vue          # bölge durumu/hız (gerçek zamanlı)
│           └── CommandPanel.vue      # axCmdAutoRun / xCmdReset yazma
└── README.md
```

---

## Örnek Tag'ler (EXAMPLE_conveyor / GVL_HMI)

| Frontend tag | OPC-UA değişken | Yön | Açıklama |
|---|---|---|---|
| `zone{1..3}_state` | `aZoneState[1..3]` | r | Bölge durumu (E_ZoneState 0..5) |
| `zone{1..3}_speed` | `aZoneSpeed[1..3]` | r | Hız (REAL, m/min) |
| `zone{1..3}_running` | `aZoneRunning[1..3]` | r | Çalışıyor bayrağı |
| `zone{1..3}_jam` | `aZoneJam[1..3]` | r | Sıkışma alarmı (HIGH) |
| `estop_active` | `xEStopActive` | r | Acil durdurma (CRITICAL) |
| `zone2_itlk` | `xZone2Itlk` | r | Bölge 2 interlock (HIGH) |
| `cmd_auto_run_z{1..3}` | `axCmdAutoRun[1..3]` | rw | Oto mod çalıştırma komutu |
| `cmd_reset` | `xCmdReset` | rw | HMI reset |
| `heartbeat` | `uHeartbeat` | r | Canlılık (her saniye toggle) |

NodeId formatı (CODESYS): `ns=<idx>;s=|var|CODESYS Control.Application.GVL_HMI.<değişken>`.
`<idx>` (namespace index) **çalışma zamanında** `OPCUA_NAMESPACE_URI`'den dinamik alınır —
asla hardcode edilmez (farklı runtime sürümleri farklı index atar).

---

## Kurulum & Çalıştırma

Önkoşul: Node.js 20+.

### 1) Gateway

```bash
cd gateway
npm install
cp .env.example .env
# .env içinde OPCUA_ENDPOINT, OPCUA_NAMESPACE_URI ve (varsa) kullanıcı bilgilerini düzenleyin
npm start          # veya: npm run dev  (dosya değişiminde otomatik yeniden başlat)
```

Gateway WebSocket'i `WS_PORT` (varsayılan 8080) üzerinde açar.

### 2) Frontend

```bash
cd frontend
npm install
cp .env.example .env      # VITE_WS_URL gateway adresini göstermeli
npm run dev               # http://localhost:5173
```

Üretim derlemesi: `npm run build` → `dist/` statik dosyaları (Nginx vb. ile sunulur).

### Test (PLC olmadan)

Gerçek PLC yokken `wscat` ile WebSocket'i test edebilirsiniz:

```bash
npx wscat -c ws://localhost:8080
# Gelen: FULL_UPDATE, BATCH_UPDATE, CONNECTION_STATUS, ALARM_ACTIVE/CLEAR
# Gönder: {"type":"WRITE","tag":"cmd_auto_run_z1","value":true,"token":"..."}
```

---

## Konfigürasyon

### Gateway (`gateway/.env`)
| Değişken | Açıklama |
|---|---|
| `OPCUA_ENDPOINT` | PLC OPC-UA adresi (`opc.tcp://ip:4840`) |
| `OPCUA_NAMESPACE_URI` | Namespace URI (index buradan dinamik alınır) |
| `OPCUA_USER` / `OPCUA_PASS` | Kimlik (boş = anonim) |
| `OPCUA_SECURITY_MODE` | `None` / `Sign` / `SignAndEncrypt` |
| `OPCUA_SECURITY_POLICY` | `None` / `Basic256Sha256` |
| `WS_PORT` | WebSocket portu (varsayılan 8080) |
| `WRITE_AUTH_TOKEN` | Yazma için paylaşılan sır (boş = doğrulama kapalı) |
| `BATCH_INTERVAL_MS` | Tag güncellemelerini birleştirme penceresi |

Tag/alarm tanımları `gateway/config.js` içindedir — kendi PLC değişkenlerinizi
`TAGS` ve `ALARM_DEFS` içine ekleyin. Yazılabilir tag'lerde `dataType` zorunludur
(`Bad_TypeMismatch` önlenir: CODESYS REAL→`Float`, LREAL→`Double`, BOOL→`Boolean`).

### Frontend (`frontend/.env`)
| Değişken | Açıklama |
|---|---|
| `VITE_WS_URL` | Gateway WebSocket adresi |
| `VITE_WRITE_TOKEN` | `WRITE_AUTH_TOKEN` ile eşleşen yazma token'ı |

---

## Mesaj Protokolü (WebSocket)

```
Gateway → Tarayıcı
  FULL_UPDATE        { data: {tag:{value,quality,timestamp}}, alarms: [...], status }
  BATCH_UPDATE       { updates: {tag:{value,quality,timestamp}} }
  CONNECTION_STATUS  { status }                     # gateway <-> PLC durumu
  ALARM_ACTIVE       { tag, priority, text, since }
  ALARM_CLEAR        { tag }

Tarayıcı → Gateway
  WRITE               { tag, value, token }
  WRITE_ACK (yanıt)   { tag, success, error? }
  REQUEST_FULL_UPDATE
  PONG
```

Dayanıklılık: gateway alarmları **anında** broadcast eder; telemetri `BatchManager`
ile `BATCH_INTERVAL_MS` penceresinde birleştirilir. Tarayıcı tarafı exponential
backoff + jitter ile yeniden bağlanır, sekme arka plandan dönünce `REQUEST_FULL_UPDATE`
gönderir.

---

## Güvenlik Notu

Bu bir **başlangıç şablonudur**; üretime almadan önce:

1. **WSS (TLS) zorunlu.** Şifresiz `ws://` üzerinde PLC komutları açık metindir.
   Nginx SSL termination + `wss://` kullanın. (Proxy arkasında
   `proxy_read_timeout 3600s` + `Upgrade`/`Connection` header'ları gerekir —
   aksi halde WebSocket 60s'de sessizce kopar.)
2. **OPC-UA güvenliği.** Üretimde `SignAndEncrypt` + `Basic256Sha256`.
   Sunucu sertifikasını trusted store'a ekleyin; `automaticallyAcceptUnknownCertificate`
   kapalı olmalı.
3. **Yazma yetkilendirmesi.** `WRITE_AUTH_TOKEN` basit bir paylaşılan sırdır —
   üretimde gerçek kimlik doğrulama (JWT/oturum) + kullanıcı bazlı yazma yetkisi +
   **yazma audit log'u** (kim, ne zaman, hangi tag'e ne yazdı) ekleyin.
4. **Yazma çakışması.** Çok operatörlü kullanımda "son yazan kazanır"; kritik
   yazmalarda turn-taking veya optimistic lock değerlendirin.
5. **Kontrol mantığı PLC'de kalmalı.** HMI yalnız izler ve komut *ister*;
   güvenlik interlock'ları (E-Stop, interlock) PLC'de uygulanır, tarayıcıda değil.
