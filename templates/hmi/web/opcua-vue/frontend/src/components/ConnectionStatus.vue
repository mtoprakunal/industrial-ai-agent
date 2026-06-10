<script setup>
// Bağlantı durumu göstergesi: WebSocket (tarayıcı<->gateway),
// PLC (gateway<->PLC) ve heartbeat canlılığı.
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useHmiStore } from '../store/hmi';

const store = useHmiStore();
const { wsStatus, plcStatus, heartbeatAlive, lastHeartbeat } = storeToRefs(store);

const wsLabel = computed(() => ({
    CONNECTED: 'Bağlı', CONNECTING: 'Bağlanıyor...', DISCONNECTED: 'Kesildi', ERROR: 'Hata',
}[wsStatus.value]));

const plcLabel = computed(() => ({
    CONNECTED: 'Bağlı', CONNECTING: 'Bağlanıyor...', DISCONNECTED: 'Kesildi', ERROR: 'Hata',
}[plcStatus.value]));
</script>

<template>
    <div class="conn-status">
        <span class="dot" :class="`s-${wsStatus.toLowerCase()}`" />
        <span class="lbl">Gateway: {{ wsLabel }}</span>

        <span class="dot" :class="`s-${plcStatus.toLowerCase()}`" />
        <span class="lbl">PLC: {{ plcLabel }}</span>

        <!-- Heartbeat: PLC her saniye uHeartbeat'i artırır; donmuşsa kopuk -->
        <span class="dot" :class="heartbeatAlive ? 's-connected' : 's-disconnected'" />
        <span class="lbl">
            Heartbeat: {{ heartbeatAlive ? 'Canlı' : 'Donmuş' }}
            <small v-if="lastHeartbeat.value !== null">({{ lastHeartbeat.value }})</small>
        </span>
    </div>
</template>

<style scoped>
.conn-status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.85rem;
    flex-wrap: wrap;
}
.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #888;
    display: inline-block;
}
.s-connected { background: #2ecc71; }
.s-connecting { background: #f1c40f; animation: blink 1s infinite; }
.s-disconnected { background: #e74c3c; }
.s-error { background: #c0392b; }
.lbl { margin-right: 12px; }
@keyframes blink { 50% { opacity: 0.3; } }
</style>
