// ============================================================
// store/hmi.js — Pinia store (Composition Store)
// ------------------------------------------------------------
// Tüm tag durumunu, bağlantı durumunu ve aktif alarmları tutar.
// WebSocket composable (useOpcUa) bu store'u günceller;
// bileşenler buradan reaktif okur (04_vue_patterns.md).
// ============================================================
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useHmiStore = defineStore('hmi', () => {
    // --- State ---
    // Bağlantı: gateway WebSocket durumu (tarayıcı <-> gateway)
    const wsStatus = ref('DISCONNECTED'); // DISCONNECTED | CONNECTING | CONNECTED | ERROR
    // PLC bağlantısı (gateway <-> PLC) — gateway CONNECTION_STATUS ile bildirir
    const plcStatus = ref('DISCONNECTED');
    // tag adı -> { value, quality, timestamp(ms) }
    const tags = ref({});
    // tag adı -> { priority, text, since(ms) }  (aktif alarmlar)
    const alarms = ref({});
    // Heartbeat takibi — son uHeartbeat değeri ve ne zaman değiştiği
    const lastHeartbeat = ref({ value: null, at: 0 });

    // --- Getters ---
    const isConnected = computed(() => wsStatus.value === 'CONNECTED');
    const isPlcConnected = computed(() => plcStatus.value === 'CONNECTED');

    // Aktif alarmları öncelik sırasına göre dizi olarak ver (ISA-18.2 sıralama)
    const PRIORITY_ORDER = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
    const activeAlarms = computed(() =>
        Object.entries(alarms.value)
            .map(([tag, a]) => ({ tag, ...a }))
            .sort((x, y) => PRIORITY_ORDER[x.priority] - PRIORITY_ORDER[y.priority] || x.since - y.since),
    );
    const alarmCount = computed(() => activeAlarms.value.length);
    const hasCritical = computed(() => activeAlarms.value.some((a) => a.priority === 'CRITICAL'));

    // Heartbeat canlı mı? PLC her saniye toggle eder; 3 sn değişmezse "donmuş".
    const heartbeatAlive = computed(() => {
        if (lastHeartbeat.value.at === 0) return false;
        return Date.now() - lastHeartbeat.value.at < 3000;
    });

    // --- Actions ---
    function setWsStatus(s) { wsStatus.value = s; }
    function setPlcStatus(s) { plcStatus.value = s; }

    function updateTag(tag, value, quality, timestamp) {
        // Vue 3 Proxy reaktivitesi yeni anahtarı da yakalar (04 Not 4)
        tags.value[tag] = { value, quality, timestamp };
        if (tag === 'heartbeat' && value !== lastHeartbeat.value.value) {
            lastHeartbeat.value = { value, at: Date.now() };
        }
    }

    // FULL_UPDATE / BATCH_UPDATE: birden çok tag'i tek seferde uygula
    function applyBatch(updates) {
        for (const [tag, d] of Object.entries(updates)) {
            updateTag(tag, d.value, d.quality, d.timestamp);
        }
    }

    function setAlarm(tag, priority, text, since) {
        alarms.value[tag] = { priority, text, since };
    }
    function clearAlarm(tag) {
        delete alarms.value[tag];
    }
    function setAlarms(list) {
        const next = {};
        for (const a of list) next[a.tag] = { priority: a.priority, text: a.text, since: a.since };
        alarms.value = next;
    }

    return {
        wsStatus, plcStatus, tags, alarms, lastHeartbeat,
        isConnected, isPlcConnected, activeAlarms, alarmCount, hasCritical, heartbeatAlive,
        setWsStatus, setPlcStatus, updateTag, applyBatch, setAlarm, clearAlarm, setAlarms,
    };
});
