---
KONU        : Vue.js ile Endüstriyel HMI Geliştirme
KATEGORİ    : hmi
ALT_KATEGORI: web-based
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://cloudinary.com/guides/vs/react-js-vs-vue-js"
    başlık: "Cloudinary — React JS vs Vue JS Practical Guide for 2025"
    güvenilirlik: topluluk
  - url: "https://tech-insider.org/react-vs-vue-2026/"
    başlık: "Tech-Insider — React vs Vue 2026: 7 Benchmarks"
    güvenilirlik: topluluk
  - url: "https://decode.agency/article/react-vs-vue/"
    başlık: "DECODE — React vs Vue: Which One to Choose in 2025?"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "03_react_patterns.md"
    ilişki: alternatif
  - konu: "05_realtime_websocket.md"
    ilişki: gerektirir
  - konu: "01_opcua_clients_js.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Vue 3 Composition API temelleri (ref, reactive, computed, watch)"
  - "WebSocket temelleri (05_realtime_websocket.md)"
  - "HMI gerçek zamanlı veri yönetimi (architecture/02_realtime_data.md)"
ÇELİŞKİLER :
  - kaynak: "Vue Options API vs Composition API — hangisi?"
    konu: "Vue 3'te iki farklı bileşen yazım stili var"
    çözüm: >
      Options API: Vue 2'ye yakın, daha tanıdık, daha az esneklik.
      Composition API: Daha güçlü, `<script setup>` ile daha az boilerplate,
      büyük projelerde daha sürdürülebilir. Yeni projeler için Composition API.
      Bu belge Composition API (script setup) kullanır.
---

## Özün Ne

Vue.js, şablon tabanlı syntax'ı, dahili reaktivite sistemi (Proxy tabanlı) ve resmi ekosistemi (Pinia state yönetimi, Vue Router) ile endüstriyel HMI geliştirme için çekici bir seçenektir. React'tan en belirgin fark: Vue'nun reaktivite sistemi DOM'u otomatik günceller, siz "ne değişti"yi değil "ne göstereceğini" tanımlarsınız. Pinia, Vuex'in yerini alan ve çok daha basit olan resmi state yönetim kütüphanesidir. Bu belge, Vue 3 Composition API ve Pinia ile endüstriyel HMI tasarımını ele alır.

## Nasıl Çalışır

### React vs Vue — HMI Bağlamında Karar

```
React Tercih Et:
  ✓ Ekip React biliyorsa
  ✓ Çok büyük/karmaşık uygulama (100K+ satır)
  ✓ React Native ile mobil da isteniyor
  ✓ Zengin ekosistem/kütüphane seçimi önemli
  ✓ TypeScript entegrasyonu çok kritikse

Vue Tercih Et:
  ✓ Ekip JavaScript bilgisi orta seviyedeyse (kolay öğrenme)
  ✓ Hızlı prototipleme gerekiyorsa
  ✓ Şablon bazlı yaklaşım tercih ediliyorsa
  ✓ Resmi entegre ekosistem (Pinia, Vue Router) isteniyor
  ✓ Orta ölçek proje: 5-15 geliştirici
  ✓ Vue'nun granüler reaktivitesi daha az render = daha az optimizasyon çabası

HMI için Vue'nun avantajı:
  Vue'nun Proxy tabanlı reaktivitesi, ref/reactive ile tanımlanan
  değişkenler değişince yalnızca ilgili DOM node'larını günceller.
  React'taki gibi useMemo/React.memo ile manuel optimizasyon daha az gerekir.
```

### Kurulum

```bash
npm create vue@latest hmi-frontend
# Seçenekler: TypeScript=Evet, Router=Evet, Pinia=Evet, Vitest=Evet
cd hmi-frontend
npm install
```

### Pinia ile Store

```typescript
// stores/hmiStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

type ConnectionStatus = "DISCONNECTED" | "CONNECTING" | "CONNECTED" | "ERROR";
type Quality = "GOOD" | "BAD" | "UNCERTAIN";

interface TagValue {
    value: any;
    quality: Quality;
    timestamp: Date;
}

// Composition Store syntax (Pinia önerileni)
export const useHMIStore = defineStore('hmi', () => {
    // State
    const connectionStatus = ref<ConnectionStatus>("DISCONNECTED");
    const tags = ref<Record<string, TagValue>>({});
    const activeAlarms = ref<string[]>([]);

    // Getters (computed)
    const isConnected = computed(() => connectionStatus.value === "CONNECTED");
    const alarmCount = computed(() => activeAlarms.value.length);
    const criticalAlarms = computed(() =>
        activeAlarms.value.filter(t => CRITICAL_TAGS.includes(t))
    );

    // Actions
    function setConnectionStatus(status: ConnectionStatus) {
        connectionStatus.value = status;
    }

    function updateTag(tag: string, value: any, quality: Quality, ts: Date) {
        // Vue reaktivitesi: Set ile mevcut objeyi güncellemek güvenli
        tags.value[tag] = { value, quality, timestamp: ts };
    }

    function setFullUpdate(data: Record<string, any>) {
        const now = new Date();
        const newTags: Record<string, TagValue> = {};
        for (const [tag, value] of Object.entries(data)) {
            newTags[tag] = { value, quality: "GOOD", timestamp: now };
        }
        tags.value = newTags;
    }

    function addAlarm(tag: string) {
        if (!activeAlarms.value.includes(tag)) {
            activeAlarms.value.push(tag);
        }
    }

    function removeAlarm(tag: string) {
        const idx = activeAlarms.value.indexOf(tag);
        if (idx > -1) activeAlarms.value.splice(idx, 1);
    }

    return {
        // State
        connectionStatus, tags, activeAlarms,
        // Getters
        isConnected, alarmCount, criticalAlarms,
        // Actions
        setConnectionStatus, updateTag, setFullUpdate, addAlarm, removeAlarm
    };
});

const CRITICAL_TAGS = ["motor_fault", "emergency_stop", "fire_alarm"];
```

### WebSocket Composable — Singleton

```typescript
// composables/useWebSocket.ts
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useHMIStore } from '../stores/hmiStore';

let wsInstance: WebSocket | null = null;
let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

export function useWebSocket() {
    const store = useHMIStore();

    function initWebSocket() {
        if (wsInstance?.readyState === WebSocket.OPEN) return;
        
        store.setConnectionStatus("CONNECTING");
        wsInstance = new WebSocket(import.meta.env.VITE_WS_URL || "ws://localhost:8080");

        wsInstance.onopen = () => {
            store.setConnectionStatus("CONNECTED");
            if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = null; }
        };

        wsInstance.onmessage = (event: MessageEvent) => {
            const msg = JSON.parse(event.data);
            switch (msg.type) {
                case "TAG_UPDATE":
                    store.updateTag(msg.tag, msg.value, msg.quality || "GOOD", new Date(msg.timestamp));
                    // Alarm takibi
                    if (typeof msg.value === "boolean") {
                        msg.value ? store.addAlarm(msg.tag) : store.removeAlarm(msg.tag);
                    }
                    break;
                case "FULL_UPDATE":
                    store.setFullUpdate(msg.data);
                    break;
                case "CONNECTION_STATUS":
                    store.setConnectionStatus(msg.status);
                    break;
            }
        };

        wsInstance.onclose = () => {
            store.setConnectionStatus("DISCONNECTED");
            scheduleReconnect();
        };
        wsInstance.onerror = () => store.setConnectionStatus("ERROR");
    }

    function scheduleReconnect() {
        if (reconnectTimer) return;
        reconnectTimer = setTimeout(() => {
            reconnectTimer = null;
            initWebSocket();
        }, 3000);
    }

    function send(msg: object) {
        if (wsInstance?.readyState === WebSocket.OPEN) {
            wsInstance.send(JSON.stringify(msg));
        }
    }

    return { initWebSocket, send };
}
```

### Tag Değeri Composable

```typescript
// composables/useTagValue.ts
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useHMIStore } from '../stores/hmiStore';

export function useTagValue<T = any>(tag: string, maxAgeMs = 5000) {
    const store = useHMIStore();
    // storeToRefs ile reaktif referans al
    const { tags, connectionStatus } = storeToRefs(store);

    const tagData = computed(() => tags.value[tag]);
    
    const value = computed<T | null>(() => {
        if (!tagData.value || connectionStatus.value === "DISCONNECTED") return null;
        return tagData.value.value as T;
    });

    const quality = computed(() => tagData.value?.quality ?? "BAD");

    const isStale = computed(() => {
        if (!tagData.value) return true;
        return (Date.now() - tagData.value.timestamp.getTime()) > maxAgeMs;
    });

    const timestamp = computed(() => tagData.value?.timestamp ?? null);

    return { value, quality, isStale, timestamp };
}
```

### Temel HMI Bileşenleri (SFC)

```vue
<!-- components/TagDisplay.vue -->
<script setup lang="ts">
import { computed } from 'vue';
import { useTagValue } from '../composables/useTagValue';

const props = defineProps<{
    tag: string;
    label: string;
    unit?: string;
    decimals?: number;
    maxAge?: number;
}>();

const { value, quality, isStale } = useTagValue<number>(props.tag, props.maxAge ?? 5000);

const formattedValue = computed(() =>
    value.value !== null ? value.value.toFixed(props.decimals ?? 1) : "--.-"
);
</script>

<template>
    <div
        class="tag-display"
        :class="{
            'stale': isStale,
            'quality-bad': quality === 'BAD',
            'quality-uncertain': quality === 'UNCERTAIN'
        }"
    >
        <span class="label">{{ label }}</span>
        <span class="value">
            {{ formattedValue }}
            <span class="unit">{{ unit }}</span>
        </span>
        <span v-if="isStale" class="stale-indicator" title="Eski veri">⚠</span>
    </div>
</template>

<style scoped>
.stale .value { color: #888; font-style: italic; }
.quality-bad .value { text-decoration: line-through; color: #cc4444; }
</style>
```

```vue
<!-- components/AnalogGauge.vue -->
<script setup lang="ts">
import { computed } from 'vue';
import { useTagValue } from '../composables/useTagValue';

const props = defineProps<{
    tag: string;
    label: string;
    unit: string;
    min: number;
    max: number;
    alarmHigh?: number;
    alarmLow?: number;
    decimals?: number;
}>();

const { value, quality, isStale } = useTagValue<number>(props.tag);

const pct = computed(() => {
    if (value.value === null) return 0;
    return Math.max(0, Math.min(100, ((value.value - props.min) / (props.max - props.min)) * 100));
});

const isHighAlarm = computed(() => props.alarmHigh !== undefined && value.value !== null && value.value >= props.alarmHigh);
const isLowAlarm  = computed(() => props.alarmLow  !== undefined && value.value !== null && value.value <= props.alarmLow);
const hasAlarm = computed(() => isHighAlarm.value || isLowAlarm.value);
</script>

<template>
    <div class="analog-gauge" :class="{ 'has-alarm': hasAlarm, 'stale': isStale }">
        <div class="gauge-label">{{ label }}</div>
        <div class="gauge-value">
            {{ value !== null ? value.toFixed(decimals ?? 1) : '--.-' }}
            <span class="unit">{{ unit }}</span>
        </div>
        <div class="gauge-bar">
            <div
                class="gauge-fill"
                :class="{ 'alarm-high': isHighAlarm, 'alarm-low': isLowAlarm }"
                :style="{ width: `${pct}%` }"
            />
        </div>
        <div class="gauge-range">
            <span>{{ min }}</span>
            <span>{{ max }} {{ unit }}</span>
        </div>
    </div>
</template>
```

```vue
<!-- components/SetpointControl.vue -->
<script setup lang="ts">
import { ref, computed } from 'vue';
import { useTagValue } from '../composables/useTagValue';
import { useWebSocket } from '../composables/useWebSocket';
import { useHMIStore } from '../stores/hmiStore';

const props = defineProps<{
    tag: string;
    writeTag: string;
    label: string;
    unit: string;
    min: number;
    max: number;
    step?: number;
}>();

const store = useHMIStore();
const { value: currentValue } = useTagValue<number>(props.tag);
const { send } = useWebSocket();
const inputValue = ref('');
const pending = ref(false);

const isConnected = computed(() => store.isConnected);
const isValid = computed(() => {
    const n = parseFloat(inputValue.value);
    return !isNaN(n) && n >= props.min && n <= props.max;
});

function handleApply() {
    if (!isValid.value) return;
    const newVal = parseFloat(inputValue.value);
    pending.value = true;
    send({ type: "WRITE_REGISTER", tag: props.writeTag, value: newVal });
    inputValue.value = '';
    setTimeout(() => { pending.value = false; }, 1000);
}
</script>

<template>
    <div class="setpoint-control">
        <label>{{ label }}</label>
        <div class="current-value">Mevcut: {{ currentValue?.toFixed(1) ?? "--.-" }} {{ unit }}</div>
        <div class="input-row">
            <input
                v-model="inputValue"
                type="number"
                :min="min"
                :max="max"
                :step="step ?? 1"
                :disabled="!isConnected || pending"
                :placeholder="String(currentValue?.toFixed(1) ?? '--')"
            />
            <span>{{ unit }}</span>
            <button
                @click="handleApply"
                :disabled="!isConnected || pending || !isValid"
            >
                {{ pending ? '...' : 'Uygula' }}
            </button>
        </div>
        <div v-if="inputValue && !isValid" class="validation-error">
            Değer {{ min }}-{{ max }} aralığında olmalı
        </div>
    </div>
</template>
```

### Ana Uygulama

```vue
<!-- App.vue -->
<script setup lang="ts">
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useHMIStore } from './stores/hmiStore';
import { useWebSocket } from './composables/useWebSocket';
import TagDisplay from './components/TagDisplay.vue';
import AnalogGauge from './components/AnalogGauge.vue';
import SetpointControl from './components/SetpointControl.vue';

const store = useHMIStore();
const { connectionStatus, alarmCount } = storeToRefs(store);
const { initWebSocket } = useWebSocket();

onMounted(() => {
    initWebSocket();  // WebSocket bağlantısını başlat
});
</script>

<template>
    <!-- Bağlantı durumu bandı -->
    <div v-if="connectionStatus !== 'CONNECTED'" :class="`connection-banner status-${connectionStatus.toLowerCase()}`">
        <span v-if="connectionStatus === 'DISCONNECTED'">⚠ PLC bağlantısı kesildi</span>
        <span v-else-if="connectionStatus === 'CONNECTING'">⏳ Bağlanıyor...</span>
        <span v-else>❌ Bağlantı hatası</span>
    </div>

    <div class="hmi-app">
        <header class="hmi-header">
            <h1>Hat 1 — Paketleme</h1>
            <div class="alarm-count" :class="{ 'has-alarms': alarmCount > 0 }">
                Alarmlar: {{ alarmCount }}
            </div>
        </header>

        <main>
            <!-- Ölçümler -->
            <section class="measurements">
                <AnalogGauge
                    tag="actual_speed" label="Gerçek Hız" unit="m/dk"
                    :min="0" :max="100" :alarm-high="90"
                />
                <AnalogGauge
                    tag="actual_temp" label="Sıcaklık" unit="°C"
                    :min="0" :max="150" :alarm-high="90" :alarm-low="10"
                />
                <TagDisplay tag="production_count" label="Üretim" :decimals="0" />
            </section>

            <!-- Kontroller -->
            <section class="controls">
                <SetpointControl
                    tag="actual_speed" write-tag="speed_setpoint"
                    label="Hız Setpoint" unit="m/dk"
                    :min="0" :max="100" :step="0.5"
                />
            </section>
        </main>
    </div>
</template>
```

### Vue DevTools ile Debug

```
Vue DevTools tarayıcı eklentisi ile:
  - Pinia store'un anlık durumunu izle
  - Her bileşenin hangi state'e bağlı olduğunu gör
  - Bileşen ağacında reaktivite akışını takip et
  - Time-travel: Geçmiş state'lere geri dön

Chrome/Firefox eklentisi: "Vue.js devtools"
```

## Örnekler

### Örnek 1: watch ile Tag Değişimini İzleme

```typescript
// Belirli bir tag değişiminde yan etki
import { watch } from 'vue';
import { useTagValue } from '../composables/useTagValue';

const { value: motorFault } = useTagValue<boolean>('motor_fault');

// Motor arızası aktif olduğunda ses çal
watch(motorFault, (newVal, oldVal) => {
    if (newVal === true && oldVal === false) {
        playAlarmSound();
        showNotification("Motor Arızası", { severity: "CRITICAL" });
    }
});
```

### Örnek 2: v-model ile İki Yönlü Bağlama (Form)

```vue
<!-- Reçete parametresi formu -->
<script setup lang="ts">
import { reactive } from 'vue';
const params = reactive({ speed: 45.0, temp: 85.0, recipeId: 1 });

function applyRecipe() {
    send({ type: "WRITE_REGISTERS", params });
}
</script>

<template>
    <form @submit.prevent="applyRecipe">
        <label>Hız: <input v-model.number="params.speed" type="number" /></label>
        <label>Sıcaklık: <input v-model.number="params.temp" type="number" /></label>
        <button type="submit" :disabled="!isConnected">Reçete Yükle</button>
    </form>
</template>
```

### Örnek 3: Trend Grafiği (recharts ile)

```vue
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useTagValue } from '../composables/useTagValue';

const props = defineProps<{ tag: string; label: string; maxPoints?: number }>();

const { value } = useTagValue<number>(props.tag);
const history = ref<{ time: string; value: number }[]>([]);

// Her değer değişiminde geçmişe ekle
watch(value, (newVal) => {
    if (newVal === null) return;
    history.value.push({
        time: new Date().toLocaleTimeString(),
        value: newVal
    });
    if (history.value.length > (props.maxPoints ?? 60)) {
        history.value.shift();
    }
});
</script>

<template>
    <div class="trend-chart">
        <h4>{{ label }} Trend</h4>
        <!-- recharts veya chart.js kullanılabilir -->
        <LineChart :data="history" :x-key="'time'" :y-key="'value'" />
    </div>
</template>
```

## Sık Yapılan Hatalar

### Hata 1: ref vs reactive Karışıklığı

```typescript
// ❌ Reaktivite kaybolur — primitive değeri destructure etme!
const { tags } = useHMIStore();  // Non-reactive kopya!
const speed = tags["actual_speed"];  // Asla güncellenmez

// ✅ storeToRefs ile reaktif referans al
const { tags } = storeToRefs(useHMIStore());  // Reaktif!
const speed = computed(() => tags.value["actual_speed"]?.value);
```

### Hata 2: v-model ile Store'u Doğrudan Bağlamak

```vue
<!-- ❌ YANLIŞ — Store state'ini doğrudan değiştirme -->
<input v-model="store.tags['speed_setpoint'].value" />

<!-- ✅ DOĞRU — Yerel ref + action ile -->
<script setup>
const localValue = ref('');
const handleInput = () => store.writeTagCommand('speed_setpoint', localValue.value);
</script>
<input v-model="localValue" @change="handleInput" />
```

### Hata 3: onMounted Yerine Direkt Dosya Scope'unda WS Başlatmak

```typescript
// ❌ YANLIŞ — SSR veya test ortamında sorun
const ws = new WebSocket("ws://...");  // Dosya yüklenince hemen bağlanır

// ✅ DOĞRU
onMounted(() => {
    const { initWebSocket } = useWebSocket();
    initWebSocket();  // Bileşen DOM'a mount olunca başlat
});
```

## Gerçek Proje Notları

**Not 1 — Vue'nun Reaktivitesinin "Ücretsiz" Performansı**  
React'ta aynı uygulamayı React.memo/useMemo olmadan yazınca CPU %60 çıktı. Vue'da reactive + Pinia ile aynı mantığı yazınca (ekstra optimizasyon olmadan) CPU %18. Vue'nun granüler reaktivitesi küçük ve orta ölçek projelerde "ücretsiz" performans sağlar.

**Not 2 — Options API'den Composition API'ye Geçiş**  
Vue 2 Options API bilen bir operatör ekibi önce Options API seçti. 200 satır sonra kod karmaşıklaşmaya başladı (mixins, computed çakışmaları). `<script setup>` Composition API'ye geçince kod %30 kısaldı, okunabilirlik arttı. Yeni Vue projeleri için başlangıçtan Composition API önerilir.

**Not 3 — Pinia ile Time-Travel Debugging**  
Bir anomali: Belirli bir işlemden sonra setpoint değeri rastgele sıfırlanıyordu. Pinia DevTools'un state geçmişine bakılınca sorun bulundu: Bağlantı yeniden kurulduğunda `setFullUpdate` çağrısı tüm tag'leri eski değerlere getiriyordu. `setFullUpdate` yalnızca değer varsa güncellemeye çevrildi.

## İlgili Konular

```
knowledge/hmi/web-based/
├── 03_react_patterns.md         → React.js alternatifi
└── 05_realtime_websocket.md     → WebSocket backend entegrasyonu

knowledge/hmi/architecture/
├── 01_hmi_patterns.md           → ISA-101 tasarım prensipleri
└── 02_realtime_data.md          → Gerçek zamanlı veri yönetimi

Araçlar:
  Vue DevTools    → Reaktivite ve Pinia debug
  Pinia           → https://pinia.vuejs.org
  Vite            → Vue 3 build aracı
  Vitest          → Vue 3 birim testleri
```
