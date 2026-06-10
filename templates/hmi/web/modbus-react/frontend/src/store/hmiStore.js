// ============================================================================
//  hmiStore.js — Zustand global state
// ============================================================================
//  Endustriyel HMI'da kritik kural: granuler selector (her bilesen yalnizca
//  kendi tag'ini secsin) -> tek tag degisiminde tum agac render OLMAZ.
//  (knowledge/hmi/web-based/03_react_patterns.md Not 1, Optimizasyon madde 1)
// ============================================================================

import { create } from "zustand";

export const useHMIStore = create((set) => ({
  // --- Baglanti durumu ---
  connectionStatus: "DISCONNECTED", // DISCONNECTED | CONNECTING | CONNECTED | ERROR

  // --- Tag degerleri: { [tag]: { value, timestamp } } ---
  tags: {},

  // --- Tag meta bilgisi (gateway'den TAG_META ile gelir) ---
  meta: {},

  // --- Aktif alarmlar: { [tag]: { active, priority, text, label, timestamp } } ---
  alarms: {},

  // --- Son yazma sonuclari (ACK) — gecici UI geri bildirimi ---
  writeAcks: {}, // { [tag]: { success, error, at } }

  setConnectionStatus: (status) => set({ connectionStatus: status }),

  setMeta: (meta) => set({ meta }),

  // Tek tag guncelle (TAG_UPDATE). Sadece o anahtar degisir -> sig render.
  updateTag: (tag, value, timestamp) =>
    set((state) => ({
      tags: { ...state.tags, [tag]: { value, timestamp } },
    })),

  // Tum durumu yukle (FULL_UPDATE — baglanti aninda).
  setFullUpdate: (data) =>
    set(() => {
      const now = Date.now();
      const tags = {};
      for (const [tag, value] of Object.entries(data)) {
        tags[tag] = { value, timestamp: now };
      }
      return { tags };
    }),

  // Alarm durumu guncelle.
  setAlarm: (tag, payload) =>
    set((state) => ({
      alarms: { ...state.alarms, [tag]: payload },
    })),

  // Yazma onayi (ACK) kaydet.
  setWriteAck: (tag, success, error) =>
    set((state) => ({
      writeAcks: { ...state.writeAcks, [tag]: { success, error, at: Date.now() } },
    })),
}));
