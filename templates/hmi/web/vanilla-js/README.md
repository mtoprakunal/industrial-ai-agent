# Vanilla JS Web HMI (Framework Bağımsız)

Saf HTML / CSS / JavaScript ile yazılmış, **build adımı gerektirmeyen**
endüstriyel web HMI başlangıç şablonu. Tarayıcıda doğrudan açılır ya da
statik dosya olarak servis edilir. Bir Node.js (veya başka) **gateway**
WebSocket üzerinden gerçek zamanlı PLC verisi sağlar.

Örnek proje: `EXAMPLE_conveyor` (3 bölgeli konveyör hattı).

## Ne işe yarar

- Proses değerlerini canlı gösterir: bölge durumları (`aZoneState[1..3]`),
  hızlar (`aZoneSpeed[1..3]`), acil stop, çalışma izni, toplam alarm.
- Aktif alarmları ISA-18.2 önceliğiyle (kritik/yüksek/...) listeler ve
  onaylama (acknowledge) imkânı sunar.
- Komut butonları: bölge oto-çalıştır (`axCmdAutoRun`), `RESET`
  (`xCmdReset`) — WebSocket write mesajı gönderir.
- Bağlantı durumu LED'i + watchdog: WebSocket kopunca **ve** PLC
  canlılık sinyali (`uHeartbeat`) dururken (gateway↔PLC kopması)
  otomatik olarak offline/kısmi durum gösterir, yazma butonlarını kilitler.
- Otomatik yeniden bağlanma (exponential backoff + jitter).

## Neden framework yok

- **Basit panolar / tek ekran**: küçük bir hat panosunda React/Vue
  araç zinciri (npm, bundler, build) gereksiz ağırlık getirir.
- **Legacy / kısıtlı tarayıcılar**: fabrika zemininde eski tarayıcılı
  paneller, kiosk cihazları; transpile/polyfill derdi olmadan çalışır.
- **Sıfır bağımlılık, sıfır build**: dosyaları kopyala, aç, çalışır.
  Bakımı kolay, denetimi şeffaf — saf `ws://` trafiği `wscat` ile test edilir.
- Daha zengin ihtiyaçlar için kardeş şablonlar: `opcua-react/`,
  `opcua-vue/`, `modbus-react/` (bkz. `../README.md`).

## Nasıl servis edilir

Bu sayfanın çalışması için **gateway'in çalışıyor olması** gerekir
(WebSocket sunucusu, varsayılan `ws://<host>:8080`). Gateway'in yayması
gereken JSON formatı: [`gateway-contract.md`](./gateway-contract.md).

### Seçenek A — Python ile statik servis (en hızlı)
```bash
cd templates/hmi/web/vanilla-js
python3 -m http.server 8000
# Tarayıcı: http://localhost:8000
```

### Seçenek B — Gateway statik servis etsin (önerilen, tek origin)
Node.js gateway'i hem WebSocket sunabilir hem bu klasörü statik servis
edebilir (örn. Express `express.static('vanilla-js')`). Böylece HMI ve
WebSocket aynı host/origin'den gelir, CORS/karışık-içerik sorunu olmaz.

### Seçenek C — Dosyayı doğrudan aç (sadece geliştirme)
`index.html` çift tıklanabilir. Ancak `file://` altında bazı tarayıcı
kısıtları olabilir; gerçek test için A veya B tercih edin.

## Yapılandırma

Tüm ayarlar tek dosyada: [`js/config.js`](./js/config.js)
- `WS_URL` — gateway WebSocket adresi.
- `TAGS` — gösterilecek tag'ler (etiket, birim, tip).
- `ALARM_RULES` — gateway alarm göndermezse tag'lerden alarm türetme.
- `COMMANDS` — komut butonları (yazma tag'leri).
- Watchdog/backoff süreleri.

Yeni tag/alarm/komut eklemek için yalnızca `config.js` düzenlenir;
mantık dosyaları (`ws-client.js`, `ui.js`, `commands.js`) değişmez.

## Dosya yapısı

```
vanilla-js/
├── index.html            # Tek sayfa HMI iskeleti
├── css/
│   └── style.css         # Koyu endüstriyel tema, durum renkleri
├── js/
│   ├── config.js         # WS URL, tag/alarm/komut tanımları
│   ├── ws-client.js      # WebSocket: bağlan, parse, reconnect, watchdog
│   ├── ui.js             # DOM güncelleme: tag/alarm/LED render
│   └── commands.js       # Yazma komutları (write mesajı)
├── gateway-contract.md   # Gateway'in uyması gereken JSON sözleşmesi
└── README.md
```

## Test (gateway olmadan)

Hızlı bir sahte gateway ile UI'ı denemek için `ws` paketiyle küçük bir
Node script yazıp `gateway-contract.md`'deki `BATCH_UPDATE` mesajlarını
periyodik gönderebilirsiniz. `uHeartbeat`'i her saniye artırmayı unutmayın;
aksi halde HMI 4 sn içinde "KISMİ BAĞLANTI" gösterir (watchdog çalışıyor demektir).

## İlgili dokümanlar

- `knowledge/hmi/web-based/05_realtime_websocket.md` — WebSocket katmanı.
- `knowledge/hmi/web-based/01_opcua_clients_js.md` — node-opcua gateway.
- `knowledge/hmi/architecture/02_realtime_data.md` — stale data / reconnect.
- `knowledge/hmi/architecture/03_alarm_management.md` — ISA-18.2 alarm.
```
