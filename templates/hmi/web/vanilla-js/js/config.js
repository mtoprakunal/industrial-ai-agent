// ============================================================
// config.js — HMI yapılandırması
// ------------------------------------------------------------
// WS URL, tag tanımları, alarm tanımları ve E_ZoneState enum
// eşlemesi burada toplanır. Tüm "sihirli sayı / sihirli string"
// tek yerde durur; yeni tag/alarm eklemek için sadece bu dosya
// düzenlenir, mantık dosyaları (ui.js/commands.js) değişmez.
//
// Kaynak değişkenler: EXAMPLE_conveyor / 02_GVL_Const_HMI.st
//   aZoneState[1..3], aZoneSpeed[1..3], xEStopActive,
//   axCmdAutoRun[1..3], xCmdReset, uHeartbeat ...
// ============================================================

// Global namespace — modül kullanmadan (script tag ile yüklenebilir)
// tüm yapılandırmayı tek nesnede toplar, global kirliliği önler.
window.HMI_CONFIG = (function () {
    'use strict';

    // ----------------------------------------------------------------
    // WebSocket adresi
    // ----------------------------------------------------------------
    // Gateway statik servis ediyorsa sayfa ile aynı host'tan bağlanırız.
    // Sabit IP gerekiyorsa WS_URL'i elle "ws://192.168.1.50:8080" yapın.
    // HTTPS sayfada otomatik wss:// (şifreli) seçilir.
    const proto = (location.protocol === 'https:') ? 'wss:' : 'ws:';
    const host = location.hostname || 'localhost';
    const WS_URL = `${proto}//${host}:8080`;

    // ----------------------------------------------------------------
    // Bağlantı / watchdog parametreleri (ms)
    // ----------------------------------------------------------------
    const RECONNECT_INITIAL_MS = 1000;   // İlk yeniden bağlanma gecikmesi
    const RECONNECT_MAX_MS = 30000;      // Exponential backoff tavanı
    const HEARTBEAT_TIMEOUT_MS = 4000;   // uHeartbeat bu süre artmazsa OFFLINE
    const STALE_TIMEOUT_MS = 5000;       // Tag bu süre güncellenmezse "eski" işaretle

    // ----------------------------------------------------------------
    // E_ZoneState enum eşlemesi (00_DUTs.st ile birebir)
    // Her durum için: etiket + renk sınıfı (css/style.css'teki state-* ile uyumlu)
    // ----------------------------------------------------------------
    const ZONE_STATE = {
        0: { label: 'BEKLİYOR',  cls: 'state-idle' },     // STATE_IDLE
        1: { label: 'BAŞLIYOR',  cls: 'state-starting' },  // STATE_STARTING
        2: { label: 'ÇALIŞIYOR', cls: 'state-running' },   // STATE_RUNNING
        3: { label: 'DURUYOR',   cls: 'state-stopping' },  // STATE_STOPPING
        4: { label: 'SIKIŞMA',   cls: 'state-jammed' },    // STATE_JAMMED
        5: { label: 'HATA',      cls: 'state-fault' }      // STATE_FAULT
    };

    function zoneStateInfo(value) {
        return ZONE_STATE[value] || { label: '???', cls: 'state-unknown' };
    }

    // ----------------------------------------------------------------
    // Tag tanımları
    // ------------------------------------------------------------
    // key   : gateway'in TAG_UPDATE / BATCH_UPDATE mesajında kullandığı tag adı
    // type  : 'enum' | 'number' | 'bool' — gösterim biçimini belirler
    // Diğer alanlar gösterime özeldir (label, unit, decimals, ...).
    // ----------------------------------------------------------------
    const TAGS = [
        // --- Bölge 1 ---
        { key: 'aZoneState.1', label: 'Bölge 1 Durum', type: 'enum',   group: 'zone1' },
        { key: 'aZoneSpeed.1', label: 'Bölge 1 Hız',   type: 'number', unit: 'm/dk', decimals: 1, group: 'zone1' },
        // --- Bölge 2 ---
        { key: 'aZoneState.2', label: 'Bölge 2 Durum', type: 'enum',   group: 'zone2' },
        { key: 'aZoneSpeed.2', label: 'Bölge 2 Hız',   type: 'number', unit: 'm/dk', decimals: 1, group: 'zone2' },
        // --- Bölge 3 ---
        { key: 'aZoneState.3', label: 'Bölge 3 Durum', type: 'enum',   group: 'zone3' },
        { key: 'aZoneSpeed.3', label: 'Bölge 3 Hız',   type: 'number', unit: 'm/dk', decimals: 1, group: 'zone3' },
        // --- Hat geneli ---
        { key: 'xEStopActive', label: 'Acil Stop',     type: 'bool', trueLabel: 'AKTİF', falseLabel: 'NORMAL', trueIsBad: true, group: 'line' },
        { key: 'xRunPermit',   label: 'Çalışma İzni',  type: 'bool', trueLabel: 'VAR',   falseLabel: 'YOK',    trueIsBad: false, group: 'line' },
        { key: 'xAnyAlarm',    label: 'Toplam Alarm',  type: 'bool', trueLabel: 'VAR',   falseLabel: 'YOK',    trueIsBad: true, group: 'line' }
    ];

    // ----------------------------------------------------------------
    // Alarm tanımları
    // ------------------------------------------------------------
    // Gateway iki yoldan alarm bildirebilir:
    //  (a) Doğrudan ALARM mesajı gönderir (gateway-contract.md), ya da
    //  (b) Sadece tag değeri gönderir; biz aşağıdaki "derive" kuralıyla
    //      bool/enum tag'lerden alarm üretiriz (basit panolar için yeterli).
    // Aşağıdaki tanımlar (b) yolu içindir; (a) gelirse olduğu gibi gösterilir.
    //
    // priority : 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' (ISA-18.2)
    // when     : (tags) => boolean  → true ise alarm aktif kabul edilir
    // ----------------------------------------------------------------
    const ALARM_RULES = [
        {
            id: 'A001_ESTOP',
            priority: 'CRITICAL',
            description: 'Acil Stop Aktif',
            cause: 'Acil stop butonuna basıldı veya güvenlik devresi açık.',
            action: 'Tehlikeyi giderin, butonu çevirip Reset basın.',
            when: (t) => t.get('xEStopActive') === true
        },
        {
            id: 'A_ZONE1_JAM',
            priority: 'HIGH',
            description: 'Bölge 1 Sıkışma',
            cause: 'Bölgede malzeme sıkıştı (STATE_JAMMED).',
            action: 'Sıkışmayı temizleyin, ardından Reset basın.',
            when: (t) => t.get('aZoneState.1') === 4
        },
        {
            id: 'A_ZONE2_JAM',
            priority: 'HIGH',
            description: 'Bölge 2 Sıkışma',
            cause: 'Bölgede malzeme sıkıştı (STATE_JAMMED).',
            action: 'Sıkışmayı temizleyin, ardından Reset basın.',
            when: (t) => t.get('aZoneState.2') === 4
        },
        {
            id: 'A_ZONE3_JAM',
            priority: 'HIGH',
            description: 'Bölge 3 Sıkışma',
            cause: 'Bölgede malzeme sıkıştı (STATE_JAMMED).',
            action: 'Sıkışmayı temizleyin, ardından Reset basın.',
            when: (t) => t.get('aZoneState.3') === 4
        },
        {
            id: 'A_ZONE1_FAULT',
            priority: 'HIGH',
            description: 'Bölge 1 Hata (Hız/Diğer)',
            cause: 'Hız arızası veya takometre kablo kopması (STATE_FAULT).',
            action: 'Tahrik panelini ve takometreyi kontrol edin, Reset basın.',
            when: (t) => t.get('aZoneState.1') === 5
        },
        {
            id: 'A_ZONE2_FAULT',
            priority: 'HIGH',
            description: 'Bölge 2 Hata (Hız/Diğer)',
            cause: 'Hız arızası veya takometre kablo kopması (STATE_FAULT).',
            action: 'Tahrik panelini ve takometreyi kontrol edin, Reset basın.',
            when: (t) => t.get('aZoneState.2') === 5
        },
        {
            id: 'A_ZONE3_FAULT',
            priority: 'HIGH',
            description: 'Bölge 3 Hata (Hız/Diğer)',
            cause: 'Hız arızası veya takometre kablo kopması (STATE_FAULT).',
            action: 'Tahrik panelini ve takometreyi kontrol edin, Reset basın.',
            when: (t) => t.get('aZoneState.3') === 5
        }
    ];

    // Öncelik → renk/sıralama meta verisi (ISA-18.2: kırmızı/turuncu/sarı/mavi)
    const PRIORITY = {
        CRITICAL: { rank: 0, cls: 'prio-critical', label: 'KRİTİK' },
        HIGH:     { rank: 1, cls: 'prio-high',     label: 'YÜKSEK' },
        MEDIUM:   { rank: 2, cls: 'prio-medium',   label: 'ORTA'   },
        LOW:      { rank: 3, cls: 'prio-low',      label: 'DÜŞÜK'  }
    };

    // ----------------------------------------------------------------
    // Komut (yazma) tanımları
    // ------------------------------------------------------------
    // Her buton bir client→server write mesajı üretir (commands.js).
    // wtype : gateway sözleşmesindeki yazma tipi
    //         'WRITE_COIL' (bool) | 'WRITE_REGISTER' (sayısal)
    // tag   : gateway'in çözeceği yazılabilir tag adı
    // value : sabit değer (ör. true). Pulse=true ise yaz→kısa süre sonra false.
    // ----------------------------------------------------------------
    const COMMANDS = [
        { id: 'cmd_auto_run_1', label: 'Bölge 1 Oto Çalıştır', wtype: 'WRITE_COIL', tag: 'axCmdAutoRun.1', value: true, kind: 'toggle' },
        { id: 'cmd_auto_run_2', label: 'Bölge 2 Oto Çalıştır', wtype: 'WRITE_COIL', tag: 'axCmdAutoRun.2', value: true, kind: 'toggle' },
        { id: 'cmd_auto_run_3', label: 'Bölge 3 Oto Çalıştır', wtype: 'WRITE_COIL', tag: 'axCmdAutoRun.3', value: true, kind: 'toggle' },
        { id: 'cmd_reset',      label: 'RESET',                 wtype: 'WRITE_COIL', tag: 'xCmdReset',     value: true, kind: 'pulse' }
    ];

    // Heartbeat tag adı — gateway bunu her toggle ettiğinde watchdog beslenir.
    const HEARTBEAT_TAG = 'uHeartbeat';

    return {
        WS_URL,
        RECONNECT_INITIAL_MS,
        RECONNECT_MAX_MS,
        HEARTBEAT_TIMEOUT_MS,
        STALE_TIMEOUT_MS,
        TAGS,
        ALARM_RULES,
        PRIORITY,
        COMMANDS,
        HEARTBEAT_TAG,
        zoneStateInfo
    };
})();
