// ============================================================
// TagValue.jsx — Tek analog/sayısal tag göstergesi
// ------------------------------------------------------------
// React.memo: tag değeri değişmedikçe yeniden render olmaz.
// Stale veride gri + uyarı; null değerde "--".
// ============================================================

import React from 'react';
import { useTagValue } from '../hooks/useTagValue.js';

export const TagValue = React.memo(function TagValue({
    tag,
    label,
    unit = '',
    decimals = 1,
}) {
    const { value, quality, isStale } = useTagValue(tag);

    const display =
        value === null || value === undefined
            ? '--'
            : typeof value === 'number'
              ? value.toFixed(decimals)
              : String(value);

    return (
        <div className={`tag-value ${isStale ? 'stale' : ''} q-${quality.toLowerCase()}`}>
            <span className="tv-label">{label}</span>
            <span className="tv-number">
                {display}
                {unit && <span className="tv-unit">{unit}</span>}
            </span>
            {isStale && (
                <span className="tv-stale" title="Eski / şüpheli veri">
                    eski
                </span>
            )}
        </div>
    );
});
