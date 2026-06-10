// ============================================================
// ConnectionStatus.jsx — Bağlantı durumu göstergesi (heartbeat tabanlı)
// ------------------------------------------------------------
// İki katman izlenir:
//   1) wsStatus  : tarayıcı <-> gateway WebSocket
//   2) plcStatus : gateway <-> PLC (OPC-UA)  [CONNECTION_STATUS mesajı]
//   3) heartbeat : uHeartbeat tag'i HEARTBEAT_TIMEOUT içinde değişmiyorsa
//                  PLC verisi DONMUŞ kabul edilir (gateway "CONNECTED" dese bile).
// uHeartbeat PLC'de her saniye artar (GVL_HMI.uHeartbeat).
// ============================================================

import { useEffect, useRef, useState } from 'react';
import { useHmiStore } from '../store/hmiStore.js';

const HEARTBEAT_TIMEOUT_MS = 3000;

export function ConnectionStatus() {
    const wsStatus = useHmiStore((s) => s.wsStatus);
    const plcStatus = useHmiStore((s) => s.plcStatus);
    const heartbeat = useHmiStore((s) => s.tags['uHeartbeat']?.value);

    // Heartbeat'in son DEĞİŞTİĞİ anı izle (timestamp değil; değer değişimi)
    const lastBeatRef = useRef({ value: undefined, at: Date.now() });
    const [beatStale, setBeatStale] = useState(false);

    useEffect(() => {
        if (heartbeat !== lastBeatRef.current.value) {
            lastBeatRef.current = { value: heartbeat, at: Date.now() };
            setBeatStale(false);
        }
    }, [heartbeat]);

    // Periyodik kontrol: son beat'ten beri timeout geçti mi?
    useEffect(() => {
        const id = setInterval(() => {
            const age = Date.now() - lastBeatRef.current.at;
            setBeatStale(age > HEARTBEAT_TIMEOUT_MS);
        }, 1000);
        return () => clearInterval(id);
    }, []);

    // Genel durumu türet
    let state, text;
    if (wsStatus !== 'CONNECTED') {
        state = 'down';
        text = 'Gateway bağlantısı yok — yeniden bağlanılıyor...';
    } else if (plcStatus !== 'CONNECTED') {
        state = 'down';
        text = 'PLC (OPC-UA) bağlantısı kesildi';
    } else if (beatStale) {
        state = 'degraded';
        text = 'PLC heartbeat yok — veri donmuş olabilir';
    } else {
        state = 'ok';
        text = 'Bağlı — canlı';
    }

    return (
        <div className={`conn-status conn-${state}`}>
            <span className="conn-dot" />
            <span className="conn-text">{text}</span>
            <span className="conn-meta">
                WS:{wsStatus} · PLC:{plcStatus} · HB:{heartbeat ?? '--'}
            </span>
        </div>
    );
}
