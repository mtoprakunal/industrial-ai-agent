<script setup>
// Aktif alarm paneli (ISA-18.2). Öncelik sırasına göre sıralı.
// Renk + ikon + metin (renk körü erişilebilirliği, 03 Örnek 3).
// Not: bu şablon alarm "aktif/temiz" gösterir; tam ISA-18.2 akışında
// ayrıca acknowledge (onay) durumu eklenir (03 acknowledge mantığı).
import { storeToRefs } from 'pinia';
import { useHmiStore } from '../store/hmi';

const store = useHmiStore();
const { activeAlarms } = storeToRefs(store);

const ICONS = { CRITICAL: '▲▲▲', HIGH: '▲▲', MEDIUM: '▲', LOW: '●' };
const LABELS = { CRITICAL: 'KRİTİK', HIGH: 'YÜKSEK', MEDIUM: 'ORTA', LOW: 'DÜŞÜK' };

function elapsed(since) {
    const s = Math.floor((Date.now() - since) / 1000);
    const m = Math.floor(s / 60);
    return `${String(m).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
}
</script>

<template>
    <section class="alarm-panel">
        <h3>Aktif Alarmlar ({{ activeAlarms.length }})</h3>

        <div v-if="activeAlarms.length === 0" class="no-alarms">
            Aktif alarm yok
        </div>

        <ul v-else class="alarm-list">
            <li
                v-for="a in activeAlarms"
                :key="a.tag"
                class="alarm-row"
                :class="`p-${a.priority.toLowerCase()}`"
            >
                <span class="icon">{{ ICONS[a.priority] }}</span>
                <span class="prio">{{ LABELS[a.priority] }}</span>
                <span class="text">{{ a.text }}</span>
                <span class="time">{{ elapsed(a.since) }}</span>
            </li>
        </ul>
    </section>
</template>

<style scoped>
.alarm-panel { background: #1e2228; border-radius: 6px; padding: 12px; }
.alarm-panel h3 { margin: 0 0 8px; font-size: 1rem; }
.no-alarms { color: #6c7a89; font-style: italic; padding: 8px 0; }
.alarm-list { list-style: none; margin: 0; padding: 0; }
.alarm-row {
    display: grid;
    grid-template-columns: 48px 70px 1fr 60px;
    align-items: center;
    gap: 8px;
    padding: 6px 8px;
    border-left: 4px solid #888;
    margin-bottom: 4px;
    border-radius: 3px;
    font-size: 0.9rem;
}
.icon { font-size: 0.7rem; letter-spacing: -2px; }
.prio { font-weight: bold; font-size: 0.75rem; }
.time { font-variant-numeric: tabular-nums; color: #aab; }

/* Renk + şekil + (kritikte) yanıp sönme — yalnız renge güvenme */
.p-critical { border-left-color: #e74c3c; background: #3a1f1f; animation: flash 1s infinite; }
.p-high { border-left-color: #e67e22; background: #332617; }
.p-medium { border-left-color: #f1c40f; background: #332f17; }
.p-low { border-left-color: #3498db; background: #1a2733; }
@keyframes flash { 50% { background: #5a2424; } }
</style>
