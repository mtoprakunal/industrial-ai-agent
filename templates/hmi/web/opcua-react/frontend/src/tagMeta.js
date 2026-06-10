// ============================================================
// tagMeta.js — Tag metadata ve enum eşlemeleri
// ------------------------------------------------------------
// EXAMPLE_conveyor projesinin DUT/GVL tanımlarına dayanır.
// E_ZoneState (00_DUTs.st) -> okunabilir metin + ISA-101 durum sınıfı.
// ============================================================

// E_ZoneState enum (PLC: 00_DUTs.st)
export const ZONE_STATE = {
    0: { label: 'BEKLİYOR', cls: 'idle' },     // STATE_IDLE
    1: { label: 'BAŞLATILIYOR', cls: 'transition' }, // STATE_STARTING
    2: { label: 'ÇALIŞIYOR', cls: 'running' },  // STATE_RUNNING
    3: { label: 'DURDURULUYOR', cls: 'transition' }, // STATE_STOPPING
    4: { label: 'SIKIŞMA', cls: 'alarm' },      // STATE_JAMMED
    5: { label: 'HATA', cls: 'alarm' },         // STATE_FAULT
};

export function zoneStateInfo(value) {
    return ZONE_STATE[value] ?? { label: '?', cls: 'unknown' };
}

// Alarm tag'leri -> ISA-18.2 öncelik + açıklama (neden/eylem ile)
// state: tag değeri true ise alarm aktif kabul edilir.
export const ALARM_DEFS = [
    {
        tag: 'xEStopActive',
        label: 'Acil Durdurma (E-Stop) Aktif',
        priority: 'CRITICAL',
        note: 'Saha acil durdurma butonu basılı. Güvenli olduğunda kurtar ve reset gönder.',
    },
    {
        tag: 'aZoneJam_1',
        label: 'Bölge 1 Sıkışma',
        priority: 'HIGH',
        note: 'Konveyör bölge 1 ürün sıkışması. Hattı temizle, sonra reset.',
    },
    {
        tag: 'aZoneJam_2',
        label: 'Bölge 2 Sıkışma',
        priority: 'HIGH',
        note: 'Konveyör bölge 2 ürün sıkışması. Hattı temizle, sonra reset.',
    },
    {
        tag: 'aZoneJam_3',
        label: 'Bölge 3 Sıkışma',
        priority: 'HIGH',
        note: 'Konveyör bölge 3 ürün sıkışması. Hattı temizle, sonra reset.',
    },
    {
        tag: 'aZoneSpdFlt_1',
        label: 'Bölge 1 Hız Arızası',
        priority: 'HIGH',
        note: 'Beklenen hıza ulaşılamadı. Motor/takometre kablosunu kontrol et.',
    },
    {
        tag: 'aZoneSpdFlt_2',
        label: 'Bölge 2 Hız Arızası',
        priority: 'HIGH',
        note: 'Beklenen hıza ulaşılamadı. Motor/takometre kablosunu kontrol et.',
    },
    {
        tag: 'aZoneSpdFlt_3',
        label: 'Bölge 3 Hız Arızası',
        priority: 'HIGH',
        note: 'Beklenen hıza ulaşılamadı. Motor/takometre kablosunu kontrol et.',
    },
    {
        tag: 'xZone2Itlk',
        label: 'Bölge 2 Interlock Blokajı',
        priority: 'MEDIUM',
        note: 'A060 interlock aktif. Önceki bölge koşulu sağlanmadan bölge 2 çalışmaz.',
    },
];

export const PRIORITY_RANK = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
