// ============================================================
// hmiStore.js — Zustand global durum deposu
// ------------------------------------------------------------
// Granüler selector için düz (flat) tag haritası tutulur:
//   tags: { [tag]: { value, quality, timestamp } }
// Her bileşen yalnızca kendi tag'ini seçer -> diğer tag değişince render olmaz.
// (bkz. knowledge 03_react_patterns — "granüler selector en yüksek etki")
// ============================================================

import { create } from 'zustand';

export const useHmiStore = create((set) => ({
    // Gateway <-> tarayıcı WebSocket bağlantı durumu
    wsStatus: 'CONNECTING', // CONNECTING | CONNECTED | DISCONNECTED | ERROR
    setWsStatus: (s) => set({ wsStatus: s }),

    // Gateway <-> PLC (OPC-UA) bağlantı durumu (CONNECTION_STATUS mesajı)
    plcStatus: 'DISCONNECTED',
    setPlcStatus: (s) => set({ plcStatus: s }),

    // Tag değerleri (düz harita)
    tags: {},

    // Tek tag güncelle (TAG_UPDATE)
    updateTag: (tag, value, quality, timestamp) =>
        set((state) => ({
            tags: { ...state.tags, [tag]: { value, quality, timestamp } },
        })),

    // Toplu güncelle (BATCH_UPDATE) — tek render ile birden çok tag
    applyBatch: (updates) =>
        set((state) => ({ tags: { ...state.tags, ...updates } })),

    // Tam snapshot (FULL_UPDATE) — bağlanınca / sekme dönüşünde
    applyFullUpdate: (data) => set({ tags: { ...data } }),
}));
