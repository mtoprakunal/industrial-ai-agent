// ============================================================
// CommandButton.jsx — PLC'ye yazma komutu butonu
// ------------------------------------------------------------
// useOpcUa.writeTag ile WRITE_TAG gönderir, WRITE_ACK bekler.
// Bağlantı kopuksa buton devre dışı (yanlış yere komut gitmesin).
// momentary=true: BOOL komutu önce value, kısa süre sonra false yazar
//   (push-button davranışı; PLC kenar tetiklemesini bekliyorsa uygun).
// ============================================================

import { useState } from 'react';
import { useHmiStore } from '../store/hmiStore.js';
import { useOpcUa } from '../hooks/useOpcUa.js';

export function CommandButton({ writeTag, label, value = true, momentary = false }) {
    const { writeTag: doWrite } = useOpcUa();
    const wsStatus = useHmiStore((s) => s.wsStatus);
    const plcStatus = useHmiStore((s) => s.plcStatus);

    const [pending, setPending] = useState(false);
    const [lastError, setLastError] = useState(null);

    const connected = wsStatus === 'CONNECTED' && plcStatus === 'CONNECTED';

    const handleClick = async () => {
        if (!connected || pending) return;
        setPending(true);
        setLastError(null);

        const res = await doWrite(writeTag, value);
        if (!res.success) {
            setLastError(res.error || 'yazma başarısız');
        } else if (momentary && typeof value === 'boolean') {
            // Push-button: kısa süre sonra sıfırla
            setTimeout(() => doWrite(writeTag, false), 300);
        }
        setPending(false);
    };

    return (
        <div className="cmd-button-wrap">
            <button
                className="cmd-button"
                onClick={handleClick}
                disabled={!connected || pending}
                title={!connected ? 'Bağlantı yok — komut gönderilemez' : ''}
            >
                {pending ? '...' : label}
            </button>
            {lastError && <span className="cmd-error">{lastError}</span>}
        </div>
    );
}
