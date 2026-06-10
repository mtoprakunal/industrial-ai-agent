// ============================================================
// ZonePanel.jsx — Tek konveyör bölgesi (zone) kartı
// ------------------------------------------------------------
// Gösterir: durum (E_ZoneState), hız (aZoneSpeed), çalışıyor biti (aZoneRunning)
// Komut: axCmdAutoRun[zone] (oto mod çalıştırma isteği) — buton.
// zone: 1 | 2 | 3
// ============================================================

import React from 'react';
import { useTagValue } from '../hooks/useTagValue.js';
import { zoneStateInfo } from '../tagMeta.js';
import { CommandButton } from './CommandButton.jsx';

export const ZonePanel = React.memo(function ZonePanel({ zone }) {
    const state = useTagValue(`aZoneState_${zone}`);
    const speed = useTagValue(`aZoneSpeed_${zone}`);
    const running = useTagValue(`aZoneRunning_${zone}`);

    const info = zoneStateInfo(state.value);
    const stale = state.isStale;

    return (
        <div className={`zone-panel zone-${info.cls} ${stale ? 'stale' : ''}`}>
            <div className="zone-head">
                <h3>Bölge {zone}</h3>
                <span className={`zone-badge badge-${info.cls}`}>
                    {stale ? '?' : info.label}
                </span>
            </div>

            <div className="zone-body">
                <div className="zone-metric">
                    <span className="zm-label">Hız</span>
                    <span className="zm-value">
                        {speed.value === null ? '--' : Number(speed.value).toFixed(1)}
                        <span className="zm-unit">m/dk</span>
                    </span>
                </div>
                <div className="zone-metric">
                    <span className="zm-label">Motor</span>
                    <span className="zm-value">
                        {running.value === null
                            ? '?'
                            : running.value
                              ? 'ÇALIŞIYOR'
                              : 'DURMUŞ'}
                    </span>
                </div>
            </div>

            <div className="zone-cmd">
                {/* axCmdAutoRun[zone] -> oto modda çalıştırma isteği (momentary BOOL) */}
                <CommandButton
                    writeTag={`cmdAutoRun_${zone}`}
                    label="Oto Çalıştır"
                    value={true}
                    momentary
                />
            </div>
        </div>
    );
});
