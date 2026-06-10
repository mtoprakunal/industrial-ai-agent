<script setup>
// Tek bir konveyör bölgesinin gerçek zamanlı görüntüsü:
// durum (E_ZoneState), hız (m/min), çalışıyor/sıkışma bayrakları.
// Veri useTagValue ile reaktif okunur.
import { computed } from 'vue';
import { useTagValue } from '../composables/useTagValue';

const props = defineProps({
    zone: { type: Number, required: true }, // 1..3
});

const { value: state, isStale } = useTagValue(`zone${props.zone}_state`);
const { value: speed } = useTagValue(`zone${props.zone}_speed`);
const { value: running } = useTagValue(`zone${props.zone}_running`);
const { value: jam } = useTagValue(`zone${props.zone}_jam`);

// E_ZoneState enum eşlemesi (00_DUTs.st)
const STATE_NAMES = {
    0: 'BOŞTA', 1: 'BAŞLATILIYOR', 2: 'ÇALIŞIYOR',
    3: 'DURDURULUYOR', 4: 'SIKIŞMA', 5: 'HATA',
};
const stateName = computed(() => STATE_NAMES[state.value] ?? '—');
const speedText = computed(() => (typeof speed.value === 'number' ? speed.value.toFixed(1) : '--.-'));
</script>

<template>
    <div
        class="zone-card"
        :class="{
            'is-stale': isStale,
            'st-running': state === 2,
            'st-jam': state === 4,
            'st-fault': state === 5,
        }"
    >
        <div class="zone-title">Bölge {{ zone }}</div>
        <div class="zone-state">{{ stateName }}</div>

        <div class="zone-speed">
            {{ speedText }} <span class="unit">m/dk</span>
        </div>

        <div class="zone-flags">
            <span class="flag" :class="{ on: running }">RUN</span>
            <span class="flag flag-jam" :class="{ on: jam }">JAM</span>
        </div>

        <div v-if="isStale" class="stale-tag" title="Eski veri — bağlantı/güncelleme sorunu">
            ⚠ ESKİ VERİ
        </div>
    </div>
</template>

<style scoped>
.zone-card {
    background: #232830;
    border: 2px solid #333a44;
    border-radius: 8px;
    padding: 14px;
    min-width: 150px;
    text-align: center;
    transition: border-color 0.2s;
}
.zone-title { font-size: 0.8rem; color: #9aa7b4; }
.zone-state { font-size: 1.1rem; font-weight: bold; margin: 4px 0; }
.zone-speed { font-size: 1.8rem; font-variant-numeric: tabular-nums; }
.unit { font-size: 0.8rem; color: #9aa7b4; }
.zone-flags { display: flex; gap: 6px; justify-content: center; margin-top: 8px; }
.flag {
    font-size: 0.7rem; padding: 2px 8px; border-radius: 3px;
    background: #2c333d; color: #6c7a89; border: 1px solid #3a414c;
}
.flag.on { background: #2ecc71; color: #06210f; border-color: #2ecc71; }
.flag-jam.on { background: #e74c3c; color: #fff; border-color: #e74c3c; }

.st-running { border-color: #2ecc71; }
.st-jam { border-color: #e74c3c; animation: pulse 1s infinite; }
.st-fault { border-color: #e67e22; }
.is-stale { opacity: 0.55; }
.stale-tag { margin-top: 6px; font-size: 0.72rem; color: #f1c40f; }
@keyframes pulse { 50% { box-shadow: 0 0 12px #e74c3c; } }
</style>
