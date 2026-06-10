// ============================================================
// composables/useTagValue.js — Tek bir tag'in reaktif değeri
// ------------------------------------------------------------
// store.tags içinden anahtar-bazlı computed döner. Vue yalnızca
// O anahtar değişince ilgili computed'i tetikler (04 Optimizasyon md.2).
// value / quality / isStale / timestamp sağlar.
// ============================================================
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useHmiStore } from '../store/hmi';

export function useTagValue(tag, maxAgeMs = 5000) {
    const store = useHmiStore();
    // storeToRefs: state için reaktif referans (04 Not 6 / Hata 1)
    const { tags, wsStatus } = storeToRefs(store);

    const entry = computed(() => tags.value[tag]);

    const value = computed(() => {
        if (!entry.value || wsStatus.value === 'DISCONNECTED') return null;
        return entry.value.value;
    });

    const quality = computed(() => entry.value?.quality ?? 'BAD');
    const timestamp = computed(() => entry.value?.timestamp ?? null);

    // Eski veri tespiti: son güncelleme maxAge'i aştıysa veri "bayat"
    const isStale = computed(() => {
        if (!entry.value) return true;
        return Date.now() - entry.value.timestamp > maxAgeMs;
    });

    return { value, quality, timestamp, isStale };
}
