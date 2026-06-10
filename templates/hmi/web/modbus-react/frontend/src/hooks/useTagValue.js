// ============================================================================
//  useTagValue.js — Tek tag'i granuler secen hook
// ============================================================================
//  Her bilesen yalnizca kendi tag'ini secer; baska tag degisince render olmaz.
//  Primitif degerleri AYRI selector'larla seciyoruz (nesne dondurmek referans
//  esitligini bozar -> gizli re-render; Not 6).
// ============================================================================

import { useHMIStore } from "../store/hmiStore.js";
import { STALE_MS } from "../config.js";

export function useTagValue(tag) {
  const entry = useHMIStore((s) => s.tags[tag]);
  const connectionStatus = useHMIStore((s) => s.connectionStatus);

  if (!entry || connectionStatus === "DISCONNECTED") {
    return { value: null, isStale: true, timestamp: null };
  }

  const isStale = Date.now() - entry.timestamp > STALE_MS;
  return { value: entry.value, isStale, timestamp: entry.timestamp };
}

// Tag meta bilgisi (label, unit, min/max, writable...).
export function useTagMeta(tag) {
  return useHMIStore((s) => s.meta[tag]);
}
