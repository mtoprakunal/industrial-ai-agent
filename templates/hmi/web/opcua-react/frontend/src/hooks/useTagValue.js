// ============================================================
// useTagValue.js — Tek tag'i granüler seçen hook
// ------------------------------------------------------------
// Zustand'dan yalnızca ilgili tag'i seçer -> başka tag değişince render olmaz.
// Stale (eski veri) tespiti: son timestamp maxAge'i aşarsa isStale=true.
// PLC bağlantısı kopuksa değer "şüpheli" sayılır.
// ============================================================

import { useHmiStore } from '../store/hmiStore.js';

const DEFAULT_MAX_AGE = 5000; // ms

export function useTagValue(tag, maxAge = DEFAULT_MAX_AGE) {
    // Primitif/alan-bazlı atomik selector'lar — yeni nesne döndürmemek için ayrı ayrı
    const entry = useHmiStore((s) => s.tags[tag]);
    const plcStatus = useHmiStore((s) => s.plcStatus);
    const wsStatus = useHmiStore((s) => s.wsStatus);

    if (!entry || wsStatus !== 'CONNECTED') {
        return { value: null, quality: 'BAD', isStale: true, timestamp: null };
    }

    const isStale =
        plcStatus !== 'CONNECTED' || Date.now() - entry.timestamp > maxAge;

    return {
        value: entry.value,
        quality: entry.quality,
        isStale,
        timestamp: entry.timestamp,
    };
}
