// ============================================================
// ui.js — DOM güncelleme katmanı
// ------------------------------------------------------------
// Sorumluluklar:
//   1. Bağlantı durumu LED'i + banner.
//   2. Tag değerlerini bas (sayı/enum/bool), eski (stale) veya
//      kötü kaliteli veriyi görsel olarak işaretle.
//   3. Alarm listesini render et (gateway ALARM göndermezse
//      tag'lerden türet — config.ALARM_RULES).
//   4. Bağlantı OFFLINE/DEGRADED iken yazma butonlarını kilitle.
//
// Saf DOM; framework yok. WSClient olaylarına abone olur.
// ============================================================

window.UI = (function () {
    'use strict';

    const CFG = window.HMI_CONFIG;
    const WS = window.WSClient;

    // DOM önbelleği (sık erişilen düğümler)
    const el = {};

    // Türetilmiş alarmların ack durumunu istemci tarafında tutarız
    // (gateway ack yönetmiyorsa basit panolar için yeterli).
    // { alarmId: { ackedAt, ack } }
    const ackState = Object.create(null);

    // Gateway doğrudan alarm gönderdiyse onu kullan; yoksa tag'lerden türet.
    let gatewayAlarms = null;

    function init() {
        el.led = document.getElementById('conn-led');
        el.connText = document.getElementById('conn-text');
        el.banner = document.getElementById('conn-banner');
        el.tagGrid = document.getElementById('tag-grid');
        el.alarmList = document.getElementById('alarm-list');
        el.alarmCount = document.getElementById('alarm-count');
        el.cmdPanel = document.getElementById('command-panel');

        buildTagCards();
        buildCommandButtons();

        // WSClient olaylarına abone ol
        WS.on('status', renderConnection);
        WS.on('tags', renderTags);
        WS.on('tags', renderAlarmsFromTags);
        WS.on('alarms', (list) => { gatewayAlarms = list; renderAlarms(list); });

        renderConnection(WS.getStatus());

        // Stale (eski veri) görselini canlı tut: bağlantı dursa da
        // saniyede bir yeniden boya, "X sn önce" sayacı ilerlesin.
        setInterval(() => renderTags(WS.getTags()), 1000);
    }

    // ----------------------------------------------------------------
    // Bağlantı durumu LED + banner + buton kilidi
    // ----------------------------------------------------------------
    function renderConnection(status) {
        const map = {
            CONNECTED:  { cls: 'led-green',  text: 'BAĞLI',          banner: null },
            CONNECTING: { cls: 'led-amber',  text: 'BAĞLANIYOR…',    banner: 'Gateway’e bağlanılıyor…' },
            DEGRADED:   { cls: 'led-amber',  text: 'KISMİ BAĞLANTI', banner: 'PLC canlılık sinyali yok — değerler güncel olmayabilir.' },
            OFFLINE:    { cls: 'led-red',    text: 'BAĞLANTI YOK',   banner: 'Gateway bağlantısı kesildi. Son değerler gösteriliyor — yeniden bağlanılıyor…' }
        };
        const s = map[status] || map.OFFLINE;

        if (el.led) el.led.className = 'led ' + s.cls + (status === 'OFFLINE' ? ' blink' : '');
        if (el.connText) el.connText.textContent = s.text;

        if (el.banner) {
            if (s.banner) {
                el.banner.textContent = s.banner;
                el.banner.classList.add('visible');
                el.banner.classList.toggle('banner-error', status === 'OFFLINE');
            } else {
                el.banner.classList.remove('visible', 'banner-error');
            }
        }

        // Güvenlik: bağlantı tam değilse yazma yasak (komut nereye gidecek?).
        const writeEnabled = (status === 'CONNECTED');
        document.querySelectorAll('.cmd-btn').forEach((b) => { b.disabled = !writeEnabled; });
    }

    // ----------------------------------------------------------------
    // Tag kartlarını bir kez kur (config.TAGS sırasıyla)
    // ----------------------------------------------------------------
    function buildTagCards() {
        if (!el.tagGrid) return;
        el.tagGrid.innerHTML = '';
        CFG.TAGS.forEach((tag) => {
            const card = document.createElement('div');
            card.className = 'tag-card';
            card.id = 'tag-' + cssId(tag.key);

            const label = document.createElement('div');
            label.className = 'tag-label';
            label.textContent = tag.label;

            const valueRow = document.createElement('div');
            valueRow.className = 'tag-value-row';

            const value = document.createElement('span');
            value.className = 'tag-value';
            value.textContent = '--';

            const unit = document.createElement('span');
            unit.className = 'tag-unit';
            unit.textContent = tag.unit || '';

            valueRow.appendChild(value);
            valueRow.appendChild(unit);

            const meta = document.createElement('div');
            meta.className = 'tag-meta';

            card.appendChild(label);
            card.appendChild(valueRow);
            card.appendChild(meta);
            el.tagGrid.appendChild(card);
        });
    }

    // ----------------------------------------------------------------
    // Tag değerlerini güncelle
    // ----------------------------------------------------------------
    function renderTags(tags) {
        if (!tags) return;
        const now = Date.now();

        CFG.TAGS.forEach((tag) => {
            const card = document.getElementById('tag-' + cssId(tag.key));
            if (!card) return;
            const valEl = card.querySelector('.tag-value');
            const metaEl = card.querySelector('.tag-meta');

            const entry = tags[tag.key];
            // Veri hiç gelmedi
            if (!entry) {
                valEl.textContent = '--';
                card.className = 'tag-card no-data';
                metaEl.textContent = 'veri yok';
                return;
            }

            const stale = (now - entry.ts) > CFG.STALE_TIMEOUT_MS;
            const badQuality = entry.quality === 'BAD';

            // Görünüm sınıflarını temizleyip yeniden uygula
            card.className = 'tag-card';

            // Değeri tipe göre biçimle
            let stateCls = '';
            if (tag.type === 'enum') {
                const info = CFG.zoneStateInfo(entry.value);
                valEl.textContent = info.label;
                stateCls = info.cls;
            } else if (tag.type === 'bool') {
                const on = entry.value === true || entry.value === 1;
                valEl.textContent = on ? tag.trueLabel : tag.falseLabel;
                // trueIsBad: true değer "kötü" durum mu (ör. EStop aktif)?
                const isBad = tag.trueIsBad ? on : !on;
                stateCls = isBad ? 'state-fault' : 'state-running';
            } else { // number
                const v = Number(entry.value);
                valEl.textContent = Number.isFinite(v)
                    ? v.toFixed(tag.decimals != null ? tag.decimals : 1)
                    : '--';
            }

            if (stateCls) card.classList.add(stateCls);
            if (badQuality) card.classList.add('bad-quality');
            if (stale) card.classList.add('stale');

            // Meta satırı: kalite / yaşlılık
            if (badQuality) {
                metaEl.textContent = 'KALİTE: BAD';
            } else if (stale) {
                metaEl.textContent = Math.round((now - entry.ts) / 1000) + ' sn önce';
            } else {
                metaEl.textContent = '';
            }
        });
    }

    // ----------------------------------------------------------------
    // Alarmları tag'lerden türet (gateway doğrudan göndermiyorsa)
    // ----------------------------------------------------------------
    function renderAlarmsFromTags(tags) {
        if (gatewayAlarms) return; // gateway alarm gönderiyorsa türetme yapma

        // Basit tag erişimi için yardımcı
        const accessor = {
            get: (key) => {
                const e = tags[key];
                return e ? e.value : undefined;
            }
        };

        const active = [];
        CFG.ALARM_RULES.forEach((rule) => {
            let isActive = false;
            try { isActive = !!rule.when(accessor); } catch (e) { /* tag yoksa pas */ }
            if (isActive) {
                const a = ackState[rule.id] || {};
                active.push({
                    id: rule.id,
                    priority: rule.priority,
                    description: rule.description,
                    cause: rule.cause,
                    action: rule.action,
                    // ack edilmiş ama koşul hâlâ aktif → ACTIVE_ACK
                    state: a.ack ? 'ACTIVE_ACK' : 'ACTIVE_UNACK',
                    activeSince: a.firstSeen || Date.now()
                });
                if (!a.firstSeen) {
                    ackState[rule.id] = Object.assign({}, a, { firstSeen: Date.now() });
                }
            } else {
                // Koşul düştü → ack durumunu sıfırla (RTN → NORMAL)
                delete ackState[rule.id];
            }
        });

        renderAlarms(active);
    }

    // ----------------------------------------------------------------
    // Alarm listesini DOM'a bas (öncelik sırasına göre)
    // ----------------------------------------------------------------
    function renderAlarms(list) {
        if (!el.alarmList) return;

        // Öncelik (rank) sonra başlangıç zamanına göre sırala
        const sorted = (list || []).slice().sort((a, b) => {
            const ra = (CFG.PRIORITY[a.priority] || { rank: 9 }).rank;
            const rb = (CFG.PRIORITY[b.priority] || { rank: 9 }).rank;
            if (ra !== rb) return ra - rb;
            return (a.activeSince || 0) - (b.activeSince || 0);
        });

        if (el.alarmCount) el.alarmCount.textContent = sorted.length;

        el.alarmList.innerHTML = '';

        if (sorted.length === 0) {
            const empty = document.createElement('div');
            empty.className = 'alarm-empty';
            empty.textContent = 'Aktif alarm yok';
            el.alarmList.appendChild(empty);
            return;
        }

        sorted.forEach((a) => {
            const prio = CFG.PRIORITY[a.priority] || CFG.PRIORITY.LOW;
            const unack = a.state === 'ACTIVE_UNACK';

            const row = document.createElement('div');
            row.className = 'alarm-row ' + prio.cls + (unack ? ' unack' : ' acked');

            // Öncelik rozeti (renk + metin + şekil → renk körü erişilebilirliği)
            const badge = document.createElement('span');
            badge.className = 'alarm-prio';
            badge.textContent = (unack ? '! ' : '✓ ') + prio.label;

            const body = document.createElement('div');
            body.className = 'alarm-body';

            const desc = document.createElement('div');
            desc.className = 'alarm-desc';
            desc.textContent = a.description;

            const detail = document.createElement('div');
            detail.className = 'alarm-detail';
            const parts = [];
            if (a.cause) parts.push('Neden: ' + a.cause);
            if (a.action) parts.push('Eylem: ' + a.action);
            detail.textContent = parts.join('  ');

            body.appendChild(desc);
            if (parts.length) body.appendChild(detail);

            row.appendChild(badge);
            row.appendChild(body);

            // Onayla butonu (yalnızca onaylanmamış alarmda)
            if (unack) {
                const ackBtn = document.createElement('button');
                ackBtn.className = 'alarm-ack-btn';
                ackBtn.textContent = 'Onayla';
                ackBtn.addEventListener('click', () => acknowledge(a.id));
                row.appendChild(ackBtn);
            }

            el.alarmList.appendChild(row);
        });
    }

    // Alarmı onayla. Türetilmiş alarmda istemci tarafı; gateway alarmında
    // sunucuya da bildir (sözleşme: ACK_ALARM).
    function acknowledge(alarmId) {
        const prev = ackState[alarmId] || {};
        ackState[alarmId] = Object.assign({}, prev, { ack: true, ackedAt: Date.now() });
        WS.send({ type: 'ACK_ALARM', alarmId: alarmId });

        if (gatewayAlarms) {
            // Gateway alarmlarında lokal görünümü hemen güncelle.
            gatewayAlarms = gatewayAlarms.map((a) =>
                a.id === alarmId ? Object.assign({}, a, { state: 'ACTIVE_ACK' }) : a
            );
            renderAlarms(gatewayAlarms);
        } else {
            renderAlarmsFromTags(WS.getTags());
        }
    }

    // ----------------------------------------------------------------
    // Komut butonlarını kur (config.COMMANDS) — commands.js'e devreder
    // ----------------------------------------------------------------
    function buildCommandButtons() {
        if (!el.cmdPanel) return;
        el.cmdPanel.innerHTML = '';
        CFG.COMMANDS.forEach((cmd) => {
            const btn = document.createElement('button');
            btn.className = 'cmd-btn' + (cmd.id === 'cmd_reset' ? ' cmd-reset' : '');
            btn.id = cmd.id;
            btn.textContent = cmd.label;
            btn.disabled = true; // bağlantı kurulana kadar kilitli
            btn.addEventListener('click', () => window.Commands.execute(cmd, btn));
            el.cmdPanel.appendChild(btn);
        });
    }

    // CSS id güvenli hale getir (nokta vb. → tire)
    function cssId(key) {
        return String(key).replace(/[^a-zA-Z0-9_-]/g, '-');
    }

    return { init };
})();
