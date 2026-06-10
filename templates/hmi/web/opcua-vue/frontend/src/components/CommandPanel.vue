<script setup>
// Komut paneli — HMI'dan PLC'ye yazma (axCmdAutoRun, xCmdReset).
// GVL_HMI yorumuna göre: komutlar yalnız OTO modda geçerlidir,
// kontrol mantığı PLC'dedir; HMI sadece istek gönderir.
import { ref, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useHmiStore } from '../store/hmi';
import { useOpcUa } from '../composables/useOpcUa';
import { useTagValue } from '../composables/useTagValue';

const store = useHmiStore();
const { isConnected, isPlcConnected } = storeToRefs(store);
const { writeTag } = useOpcUa();

// Yazma yalnız gateway + PLC bağlıyken mümkün
const canWrite = computed(() => isConnected.value && isPlcConnected.value);

// Her bölge için oto-çalıştırma komutunun mevcut değerini oku (geri besleme)
const zones = [1, 2, 3].map((z) => ({
    zone: z,
    cmd: useTagValue(`cmd_auto_run_z${z}`),
}));

const pending = ref({}); // tag -> bool (yazma onayı bekleniyor)

function setAutoRun(zone, value) {
    const tag = `cmd_auto_run_z${zone}`;
    pending.value[tag] = true;
    writeTag(tag, value);
    // Basit görsel geri besleme; gerçek onay WRITE_ACK ile gelir (ileride genişletilebilir)
    setTimeout(() => { pending.value[tag] = false; }, 800);
}

function sendReset() {
    pending.value.cmd_reset = true;
    writeTag('cmd_reset', true);
    // Reset tek atımlık komut; PLT_RST ile OR'lanır, PLC kendi sıfırlar.
    setTimeout(() => {
        writeTag('cmd_reset', false);
        pending.value.cmd_reset = false;
    }, 500);
}
</script>

<template>
    <section class="command-panel">
        <h3>Komutlar (Oto Mod)</h3>

        <div v-if="!canWrite" class="warn">
            ⚠ Yazma devre dışı — gateway/PLC bağlı değil
        </div>

        <div class="cmd-grid">
            <div v-for="z in zones" :key="z.zone" class="cmd-zone">
                <span class="cmd-label">Bölge {{ z.zone }} Oto Çalıştır</span>
                <div class="btn-row">
                    <button
                        class="btn btn-on"
                        :class="{ active: z.cmd.value.value === true }"
                        :disabled="!canWrite || pending[`cmd_auto_run_z${z.zone}`]"
                        @click="setAutoRun(z.zone, true)"
                    >
                        BAŞLAT
                    </button>
                    <button
                        class="btn btn-off"
                        :class="{ active: z.cmd.value.value === false }"
                        :disabled="!canWrite || pending[`cmd_auto_run_z${z.zone}`]"
                        @click="setAutoRun(z.zone, false)"
                    >
                        DURDUR
                    </button>
                </div>
            </div>
        </div>

        <button class="btn btn-reset" :disabled="!canWrite || pending.cmd_reset" @click="sendReset">
            RESET (Alarm/Sıkışma)
        </button>
    </section>
</template>

<style scoped>
.command-panel { background: #1e2228; border-radius: 6px; padding: 12px; }
.command-panel h3 { margin: 0 0 8px; font-size: 1rem; }
.warn { color: #f1c40f; font-size: 0.85rem; margin-bottom: 8px; }
.cmd-grid { display: flex; flex-direction: column; gap: 8px; }
.cmd-zone { display: flex; justify-content: space-between; align-items: center; }
.cmd-label { font-size: 0.85rem; }
.btn-row { display: flex; gap: 6px; }
.btn {
    border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer;
    font-weight: bold; font-size: 0.8rem; color: #fff; background: #3a414c;
}
.btn:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-on.active { background: #2ecc71; color: #06210f; }
.btn-off.active { background: #e74c3c; }
.btn-reset { margin-top: 12px; width: 100%; background: #e67e22; }
</style>
