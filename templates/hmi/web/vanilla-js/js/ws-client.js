// ============================================================
// ws-client.js — WebSocket istemcisi (bağlantı yönetimi)
// ------------------------------------------------------------
// Sorumluluklar:
//   1. Gateway'e bağlan, JSON mesajları parse et.
//   2. Otomatik yeniden bağlanma (exponential backoff + jitter).
//   3. İki katmanlı canlılık denetimi:
//      (a) close/error → yeniden bağlan.
//      (b) Heartbeat watchdog: uHeartbeat belirli süre artmazsa,
//          soket "açık" görünse bile durumu OFFLINE/DEGRADED yap
//          (gateway↔PLC kopması bu yolla yakalanır).
//   4. Tag değerlerini son-değer önbelleğinde (latest cache) tut.
//   5. Yazma (write) mesajı gönder (commands.js çağırır).
//
// Mimari not (grounding): Tarayıcı ham TCP açamaz; OPC-UA/Modbus'a
// doğrudan konuşamaz. Bu istemci yalnızca gateway ile WebSocket
// konuşur, gateway PLC tarafını çevirir.
// ============================================================

window.WSClient = (function () {
    'use strict';

    const CFG = window.HMI_CONFIG;

    // --- Bağlantı durumları (UI ile ortak sözlük) ---
    const STATUS = {
        CONNECTING: 'CONNECTING',
        CONNECTED: 'CONNECTED',     // Soket açık VE heartbeat taze
        DEGRADED: 'DEGRADED',       // Soket açık AMA heartbeat durmuş (gateway↔PLC?)
        OFFLINE: 'OFFLINE'          // Soket kapalı
    };

    let ws = null;
    let manualClose = false;
    let reconnectTimer = null;
    let reconnectDelay = CFG.RECONNECT_INITIAL_MS;
    let watchdogTimer = null;

    // Son-değer önbelleği: { tagKey: { value, quality, ts } }
    // ts = bu istemcinin değeri aldığı an (yaşlılık hesabı için tek saat).
    const tagCache = Object.create(null);

    // Heartbeat takibi
    let lastHeartbeatValue = null;
    let lastHeartbeatAt = 0;

    // Dış dünyaya bildirilen mevcut durum
    let currentStatus = STATUS.OFFLINE;

    // Dinleyiciler (ui.js bağlanır)
    const listeners = {
        status: [],   // (status) => void
        tags: [],     // (tagCache) => void   — her güncellemede
        alarms: []    // (alarmList) => void  — gateway ALARM gönderirse
    };

    function on(event, cb) {
        if (listeners[event]) listeners[event].push(cb);
    }

    function emit(event, payload) {
        (listeners[event] || []).forEach((cb) => {
            try { cb(payload); } catch (e) { console.error('listener error', e); }
        });
    }

    // ----------------------------------------------------------------
    // Durum değiştir + UI'a bildir (yalnızca gerçekten değişince)
    // ----------------------------------------------------------------
    function setStatus(next) {
        if (next === currentStatus) return;
        currentStatus = next;
        emit('status', next);
    }

    function getStatus() { return currentStatus; }
    function getTags() { return tagCache; }

    // ----------------------------------------------------------------
    // Bağlan
    // ----------------------------------------------------------------
    function connect() {
        if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
            return;
        }
        manualClose = false;
        setStatus(STATUS.CONNECTING);

        try {
            ws = new WebSocket(CFG.WS_URL);
        } catch (e) {
            console.error('WebSocket oluşturulamadı:', e);
            scheduleReconnect();
            return;
        }

        ws.onopen = () => {
            console.log('WebSocket bağlandı:', CFG.WS_URL);
            reconnectDelay = CFG.RECONNECT_INITIAL_MS;   // backoff sıfırla
            // Heartbeat'i taze say (ilk değer gelene kadar boşuna OFFLINE olmasın)
            lastHeartbeatAt = Date.now();
            lastHeartbeatValue = null;
            setStatus(STATUS.CONNECTED);
            startWatchdog();
            // Bağlantı kurulunca tüm mevcut durumu iste (latest cache snapshot)
            send({ type: 'REQUEST_FULL_UPDATE' });
        };

        ws.onmessage = (event) => {
            let msg;
            try {
                msg = JSON.parse(event.data);
            } catch (e) {
                console.warn('Geçersiz JSON:', String(event.data).slice(0, 120));
                return;
            }
            handleMessage(msg);
        };

        ws.onclose = (ev) => {
            stopWatchdog();
            ws = null;
            setStatus(STATUS.OFFLINE);
            // close code 1000 = temiz kapanış; manuel değilse yine de reconnect
            // (ağ kaynaklı 1006 vb. mutlaka yeniden bağlanmalı).
            if (!manualClose) {
                console.warn(`WebSocket kapandı (code=${ev.code}) → yeniden bağlanılıyor`);
                scheduleReconnect();
            }
        };

        ws.onerror = (ev) => {
            console.error('WebSocket hatası', ev);
            // onerror'u onclose izler; reconnect orada planlanır.
        };
    }

    // ----------------------------------------------------------------
    // Gelen mesajı işle
    // ----------------------------------------------------------------
    function handleMessage(msg) {
        switch (msg.type) {
            case 'FULL_UPDATE':
                // { type, data: { tagKey: value | {value,quality} }, status }
                if (msg.data && typeof msg.data === 'object') {
                    Object.keys(msg.data).forEach((key) => {
                        applyTag(key, msg.data[key]);
                    });
                }
                emit('tags', tagCache);
                break;

            case 'BATCH_UPDATE':
                // { type, updates: { tagKey: {value,quality,timestamp} } }
                if (msg.updates && typeof msg.updates === 'object') {
                    Object.keys(msg.updates).forEach((key) => {
                        applyTag(key, msg.updates[key]);
                    });
                }
                emit('tags', tagCache);
                break;

            case 'TAG_UPDATE':
                // { type, tag, value, quality?, timestamp? }
                applyTag(msg.tag, { value: msg.value, quality: msg.quality });
                emit('tags', tagCache);
                break;

            case 'ALARM':
                // Gateway doğrudan alarm listesi gönderirse (sözleşme b yolu).
                // { type, alarms: [ {id,priority,description,...,state} ] }
                if (Array.isArray(msg.alarms)) emit('alarms', msg.alarms);
                break;

            case 'WRITE_ACK':
                // { type, tag, success, error? }
                if (!msg.success) {
                    console.warn(`Yazma reddedildi: ${msg.tag} — ${msg.error || 'bilinmiyor'}`);
                }
                emit('writeAck', msg);
                break;

            case 'CONNECTION_STATUS':
                // Gateway↔PLC durumu. "CONNECTED" değilse DEGRADED göster.
                if (msg.status && msg.status !== 'CONNECTED') {
                    setStatus(STATUS.DEGRADED);
                } else if (ws && ws.readyState === WebSocket.OPEN) {
                    setStatus(STATUS.CONNECTED);
                }
                break;

            case 'PING':
                // Uygulama-seviyesi ping → pong dön (proxy ping'i yutarsa diye).
                send({ type: 'PONG' });
                break;

            default:
                // Bilinmeyen tip — sessizce yok say (ileri uyumluluk).
                break;
        }
    }

    // ----------------------------------------------------------------
    // Tek tag'i önbelleğe işle. raw, ham değer ya da {value,quality} olabilir.
    // ----------------------------------------------------------------
    function applyTag(key, raw) {
        if (key == null) return;
        let value, quality;
        if (raw !== null && typeof raw === 'object' && 'value' in raw) {
            value = raw.value;
            quality = raw.quality || 'GOOD';
        } else {
            value = raw;
            quality = 'GOOD';
        }
        tagCache[key] = { value: value, quality: quality, ts: Date.now() };

        // Heartbeat tag'i geldiyse watchdog'u besle.
        if (key === CFG.HEARTBEAT_TAG) {
            feedHeartbeat(value);
        }
    }

    // ----------------------------------------------------------------
    // Heartbeat watchdog
    // ------------------------------------------------------------
    // uHeartbeat PLC'de her saniye toggle/artar. Değer değiştikçe
    // lastHeartbeatAt güncellenir. Watchdog timer, değer belirli süre
    // değişmediyse DEGRADED'a düşürür (soket hâlâ açık olsa bile).
    // ----------------------------------------------------------------
    function feedHeartbeat(value) {
        if (value !== lastHeartbeatValue) {
            lastHeartbeatValue = value;
            lastHeartbeatAt = Date.now();
            // Soket açık + heartbeat taze → tekrar CONNECTED'a dön.
            if (ws && ws.readyState === WebSocket.OPEN && currentStatus === STATUS.DEGRADED) {
                setStatus(STATUS.CONNECTED);
            }
        }
    }

    function startWatchdog() {
        stopWatchdog();
        watchdogTimer = setInterval(() => {
            if (!ws || ws.readyState !== WebSocket.OPEN) return;
            const age = Date.now() - lastHeartbeatAt;
            if (age > CFG.HEARTBEAT_TIMEOUT_MS) {
                // Soket açık ama PLC'den canlılık yok → kısmi bağlantı.
                setStatus(STATUS.DEGRADED);
            }
        }, 1000);
    }

    function stopWatchdog() {
        if (watchdogTimer) { clearInterval(watchdogTimer); watchdogTimer = null; }
    }

    // ----------------------------------------------------------------
    // Exponential backoff + jitter ile yeniden bağlanma planla
    // ----------------------------------------------------------------
    function scheduleReconnect() {
        if (reconnectTimer || manualClose) return;
        // Thundering herd'i önlemek için 0-1000ms jitter ekle.
        const jitter = Math.floor(Math.random() * 1000);
        const delay = Math.min(reconnectDelay, CFG.RECONNECT_MAX_MS) + jitter;
        console.log(`Yeniden bağlanma ${delay} ms sonra`);
        reconnectTimer = setTimeout(() => {
            reconnectTimer = null;
            reconnectDelay = Math.min(reconnectDelay * 2, CFG.RECONNECT_MAX_MS);
            connect();
        }, delay);
    }

    // ----------------------------------------------------------------
    // Mesaj gönder (yalnızca soket açıksa). true = gönderildi.
    // ----------------------------------------------------------------
    function send(obj) {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(obj));
            return true;
        }
        return false;
    }

    // ----------------------------------------------------------------
    // Temiz kapanış (manuel / sayfa kapanırken)
    // ----------------------------------------------------------------
    function disconnect() {
        manualClose = true;
        if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = null; }
        stopWatchdog();
        if (ws) ws.close(1000, 'Client disconnect');
        ws = null;
        setStatus(STATUS.OFFLINE);
    }

    // Sayfa kapanırken eski soketi temiz bırak (hayalet bağlantı önleme).
    window.addEventListener('beforeunload', () => {
        if (ws && ws.readyState === WebSocket.OPEN) ws.close(1000, 'unload');
    });

    // Sekme tekrar görünür olunca tam güncelleme iste (arka planda timer kısılır).
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden && ws && ws.readyState === WebSocket.OPEN) {
            send({ type: 'REQUEST_FULL_UPDATE' });
        }
    });

    return {
        STATUS,
        connect,
        disconnect,
        send,
        on,
        getStatus,
        getTags
    };
})();
