<script setup>
// Ana uygulama — WebSocket'i mount'ta başlat, bileşenleri yerleştir.
// Composable'ı (useOpcUa) <script setup> üst seviyesinde çağır;
// async/timeout içinde DEĞİL (04 Not 7 — lifecycle hook scope).
import { onMounted, onBeforeUnmount } from 'vue';
import { storeToRefs } from 'pinia';
import { useHmiStore } from './store/hmi';
import { useOpcUa } from './composables/useOpcUa';
import ConnectionStatus from './components/ConnectionStatus.vue';
import AlarmPanel from './components/AlarmPanel.vue';
import ZoneCard from './components/ZoneCard.vue';
import CommandPanel from './components/CommandPanel.vue';

const store = useHmiStore();
const { wsStatus, hasCritical } = storeToRefs(store);
const { init, disconnect } = useOpcUa();

onMounted(() => init());        // bağlantıyı bileşen mount olunca aç (04 Hata 3)
onBeforeUnmount(() => disconnect());
</script>

<template>
    <!-- Üst bant: bağlantı koptuğunda veya kritik alarmda uyar -->
    <div v-if="wsStatus !== 'CONNECTED'" class="banner banner-conn">
        <span v-if="wsStatus === 'CONNECTING'">⏳ Gateway'e bağlanıyor...</span>
        <span v-else>⚠ Gateway bağlantısı yok — veriler güncel olmayabilir</span>
    </div>
    <div v-else-if="hasCritical" class="banner banner-crit">
        🔴 KRİTİK ALARM AKTİF
    </div>

    <div class="hmi">
        <header class="hmi-header">
            <h1>Konveyör Hattı — OPC-UA HMI</h1>
            <ConnectionStatus />
        </header>

        <main class="hmi-main">
            <section class="zones">
                <ZoneCard :zone="1" />
                <ZoneCard :zone="2" />
                <ZoneCard :zone="3" />
            </section>

            <aside class="side">
                <AlarmPanel />
                <CommandPanel />
            </aside>
        </main>
    </div>
</template>

<style scoped>
.banner { padding: 8px 16px; text-align: center; font-weight: bold; }
.banner-conn { background: #7a5b00; color: #fff; }
.banner-crit { background: #c0392b; color: #fff; animation: blink 0.8s infinite; }
@keyframes blink { 50% { opacity: 0.5; } }

.hmi { padding: 16px; max-width: 1100px; margin: 0 auto; }
.hmi-header {
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 12px; margin-bottom: 16px;
    border-bottom: 1px solid #333a44; padding-bottom: 12px;
}
.hmi-header h1 { font-size: 1.3rem; margin: 0; }
.hmi-main { display: grid; grid-template-columns: 1fr 360px; gap: 16px; }
.zones { display: flex; gap: 12px; flex-wrap: wrap; align-content: flex-start; }
.side { display: flex; flex-direction: column; gap: 16px; }
@media (max-width: 800px) { .hmi-main { grid-template-columns: 1fr; } }
</style>
