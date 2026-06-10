# Gateway ↔ HMI WebSocket Sözleşmesi

Bu belge, vanilla-js HMI'ın gateway'den **beklediği** ve gateway'e
**gönderdiği** WebSocket JSON mesaj formatını tanımlar. Gateway'i yazan
kişi bu sözleşmeye uymalıdır. Frontend hiçbir build adımı gerektirmez;
tek bağımlılığı bu sözleşmedir.

## Mimari

Tarayıcı ham TCP açamaz; OPC-UA (`opc.tcp://`) veya Modbus TCP (port 502)
ile **doğrudan** konuşamaz. Araya bir Node.js (veya başka) **gateway**
konur:

```
Tarayıcı  ──WebSocket(JSON)──►  Gateway  ──OPC-UA / Modbus──►  PLC
(bu HMI)                        (köprü)
```

Gateway, PLC tarafının (OPC-UA subscription ya da Modbus polling) hangi
protokol olduğundan **bağımsız** olarak aşağıdaki JSON formatını yayar.
HMI hangi protokolün kullanıldığını bilmez, bilmesi de gerekmez.

- Varsayılan WS adresi: `ws://<host>:8080` (HTTPS sayfada `wss://`).
  Adres `js/config.js` → `WS_URL` ile değiştirilebilir.

---

## 1. Tag Adlandırma

Tag adları, PLC değişken adlarıyla aynıdır (EXAMPLE_conveyor / GVL_HMI).
Dizi elemanları **nokta** ile gösterilir:

| HMI tag anahtarı   | PLC değişkeni            | Tip      |
|--------------------|--------------------------|----------|
| `aZoneState.1`     | `aZoneState[1]`          | enum INT |
| `aZoneState.2`     | `aZoneState[2]`          | enum INT |
| `aZoneState.3`     | `aZoneState[3]`          | enum INT |
| `aZoneSpeed.1`     | `aZoneSpeed[1]`          | REAL     |
| `aZoneSpeed.2`     | `aZoneSpeed[2]`          | REAL     |
| `aZoneSpeed.3`     | `aZoneSpeed[3]`          | REAL     |
| `xEStopActive`     | `xEStopActive`           | BOOL     |
| `xRunPermit`       | `xRunPermit`             | BOOL     |
| `xAnyAlarm`        | `xAnyAlarm`              | BOOL     |
| `uHeartbeat`       | `uHeartbeat`             | UDINT    |
| `axCmdAutoRun.1`   | `axCmdAutoRun[1]` (yaz)  | BOOL     |
| `axCmdAutoRun.2`   | `axCmdAutoRun[2]` (yaz)  | BOOL     |
| `axCmdAutoRun.3`   | `axCmdAutoRun[3]` (yaz)  | BOOL     |
| `xCmdReset`        | `xCmdReset` (yaz)        | BOOL     |

`E_ZoneState` enum eşlemesi (PLC `00_DUTs.st`):
`0=IDLE, 1=STARTING, 2=RUNNING, 3=STOPPING, 4=JAMMED, 5=FAULT`.

---

## 2. Sunucu → İstemci Mesajları (gateway yayınlar)

Tüm mesajlar JSON nesnesidir ve bir `type` alanı taşır.

### 2.1 FULL_UPDATE — bağlantı kurulunca tam durum
Yeni istemci bağlandığında veya `REQUEST_FULL_UPDATE` alınınca gönderilir.
`data` tüm bilinen tag'lerin son değerini içerir (latest-value cache).

```json
{
  "type": "FULL_UPDATE",
  "status": "CONNECTED",
  "data": {
    "aZoneState.1": 2,
    "aZoneSpeed.1": 44.8,
    "xEStopActive": false,
    "uHeartbeat": 1234
  }
}
```
`data` değerleri ham (yukarıdaki gibi) **veya** kaliteli olabilir:
```json
"aZoneSpeed.1": { "value": 44.8, "quality": "GOOD" }
```

### 2.2 TAG_UPDATE — tek tag değişimi
```json
{ "type": "TAG_UPDATE", "tag": "aZoneSpeed.1", "value": 45.2, "quality": "GOOD", "timestamp": 1718000000000 }
```
`quality`: `"GOOD" | "BAD" | "UNCERTAIN"` (opsiyonel, varsayılan GOOD).
`timestamp` opsiyoneldir; HMI yaşlılığı kendi saatiyle hesaplar.

### 2.3 BATCH_UPDATE — birden çok tag tek mesajda (önerilir)
Performans için 100 ms'lik pencerede değişimleri topla.
```json
{
  "type": "BATCH_UPDATE",
  "updates": {
    "aZoneSpeed.1": { "value": 45.2, "quality": "GOOD" },
    "aZoneState.2": { "value": 4,    "quality": "GOOD" }
  }
}
```

### 2.4 CONNECTION_STATUS — gateway↔PLC durumu
PLC bağlantısı koparsa gönderilir; HMI bunu "KISMİ BAĞLANTI" (DEGRADED)
olarak gösterir (WebSocket açık olsa bile).
```json
{ "type": "CONNECTION_STATUS", "status": "DISCONNECTED" }
```
`status`: `"CONNECTED" | "DISCONNECTED" | "DEGRADED"`.

### 2.5 ALARM — (opsiyonel) sunucu-tarafı alarm listesi
Gateway alarm durumunu kendisi yönetiyorsa tam aktif listeyi gönderir.
**Bu mesaj gelirse**, HMI tag'lerden alarm türetmeyi bırakır ve bu listeyi
kullanır.
```json
{
  "type": "ALARM",
  "alarms": [
    {
      "id": "A001_ESTOP",
      "priority": "CRITICAL",
      "description": "Acil Stop Aktif",
      "cause": "Güvenlik devresi açık.",
      "action": "Tehlikeyi giderip Reset basın.",
      "state": "ACTIVE_UNACK",
      "activeSince": 1718000000000
    }
  ]
}
```
`priority`: `"CRITICAL" | "HIGH" | "MEDIUM" | "LOW"`.
`state`: `"ACTIVE_UNACK" | "ACTIVE_ACK"` (RTN/NORMAL listeden düşer).

> ALARM mesajı **göndermezseniz** HMI, `xEStopActive` ve `aZoneState`
> (JAMMED/FAULT) tag'lerinden basit alarmlar türetir (bkz. `js/config.js`
> → `ALARM_RULES`). Basit panolar için bu yeterlidir.

### 2.6 WRITE_ACK — yazma onayı
```json
{ "type": "WRITE_ACK", "tag": "axCmdAutoRun.1", "success": true }
{ "type": "WRITE_ACK", "tag": "xCmdReset", "success": false, "error": "not connected" }
```

### 2.7 PING — (opsiyonel) uygulama-seviyesi canlılık
HMI buna otomatik `{"type":"PONG"}` ile yanıt verir.

---

## 3. İstemci → Sunucu Mesajları (HMI gönderir)

### 3.1 REQUEST_FULL_UPDATE
Bağlantı kurulunca ve sekme tekrar görünür olunca gönderilir.
Gateway buna `FULL_UPDATE` ile yanıt vermelidir.
```json
{ "type": "REQUEST_FULL_UPDATE" }
```

### 3.2 WRITE_COIL — bool yazma
```json
{ "type": "WRITE_COIL", "tag": "axCmdAutoRun.1", "value": true }
```

### 3.3 WRITE_REGISTER — sayısal yazma (setpoint vb.)
```json
{ "type": "WRITE_REGISTER", "tag": "rSpeedSetpoint", "value": 65.0 }
```

> RESET gibi tek atımlık (`pulse`) komutlarda HMI önce `value:true`,
> ~400 ms sonra `value:false` yazar. Gateway/PLC tek-atım mantığını
> normal kabul etmelidir.

### 3.4 ACK_ALARM — alarm onayla
```json
{ "type": "ACK_ALARM", "alarmId": "A001_ESTOP" }
```

### 3.5 PONG
HMI, `PING` aldığında otomatik gönderir.

---

## 4. Gateway Sorumlulukları (özet)

1. **Latest-value cache** tut → yeni istemciye anında `FULL_UPDATE`.
2. PLC'den gelen değişimleri 100 ms pencerede `BATCH_UPDATE`'e topla.
3. `uHeartbeat`'i her saniye olduğu gibi ilet (HMI watchdog'u besler).
4. PLC bağlantısı koparsa `CONNECTION_STATUS: DISCONNECTED` yayınla.
5. Yazma mesajlarını **yetki** kontrolünden geçir (üretimde `sessionToken`),
   ardından PLC'ye yaz ve `WRITE_ACK` dön.
6. Ölü WebSocket'leri ping/pong + timeout ile temizle.
7. Üretimde `wss://` (TLS) kullan — şifresiz PLC komutu taşıma.

> Node.js gateway implementasyon örnekleri için bkz.
> `knowledge/hmi/web-based/05_realtime_websocket.md` (WebSocket sunucusu) ve
> `knowledge/hmi/web-based/01_opcua_clients_js.md` (node-opcua köprüsü).
