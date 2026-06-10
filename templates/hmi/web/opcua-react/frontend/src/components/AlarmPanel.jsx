// ============================================================
// AlarmPanel.jsx — Aktif alarm paneli (ISA-18.2 esinli)
// ------------------------------------------------------------
// ALARM_DEFS'teki her tag izlenir; değeri true ise alarm aktif.
// Öncelik sırasına göre dizilir (CRITICAL önce).
// Renk + ikon + metin birlikte (renk körü erişilebilirliği).
// NOT: Bu basit gösterim "aktif/normal"dir. Tam ISA-18.2 ack/shelve
//      yaşam döngüsü için ayrı bir alarm servisi gerekir (knowledge 03).
// ============================================================

import { useHmiStore } from '../store/hmiStore.js';
import { ALARM_DEFS, PRIORITY_RANK } from '../tagMeta.js';

const ICON = { CRITICAL: '🔴', HIGH: '🟠', MEDIUM: '🟡', LOW: '🔵' };

export function AlarmPanel() {
    // Tüm alarm tag değerlerini tek selector ile al.
    // Not: bu selector dizi döndürür; alarm sayısı azdır ve panel zaten
    // alarm değişiminde render olmalı, bu yüzden kabul edilebilir.
    const tags = useHmiStore((s) => s.tags);

    const active = ALARM_DEFS.filter((def) => tags[def.tag]?.value === true).sort(
        (a, b) => PRIORITY_RANK[a.priority] - PRIORITY_RANK[b.priority]
    );

    if (active.length === 0) {
        return <div className="alarm-panel ok">✓ Aktif Alarm Yok</div>;
    }

    return (
        <div className="alarm-panel">
            <h3>Aktif Alarmlar ({active.length})</h3>
            <ul className="alarm-list">
                {active.map((def) => (
                    <li key={def.tag} className={`alarm-item p-${def.priority.toLowerCase()}`}>
                        <span className="alarm-icon">{ICON[def.priority]}</span>
                        <div className="alarm-text">
                            <span className="alarm-label">
                                [{def.priority}] {def.label}
                            </span>
                            <span className="alarm-note">{def.note}</span>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}
