// Analog / int register gostergesi (input register, olcekli holding register).
// Deger + birim + min/max bar; alarm esikleri opsiyonel.
import React from "react";
import { useTagValue, useTagMeta } from "../hooks/useTagValue.js";

export const AnalogDisplay = React.memo(function AnalogDisplay({
  tag,
  min = 0,
  max = 100,
  alarmHigh,
  alarmLow,
  decimals = 1,
}) {
  const { value, isStale } = useTagValue(tag);
  const meta = useTagMeta(tag);
  const label = meta?.label || tag;
  const unit = meta?.unit || "";

  const hasValue = value !== null && value !== undefined && !isStale;
  const pct = hasValue
    ? Math.max(0, Math.min(100, ((value - min) / (max - min)) * 100))
    : 0;

  const isHigh = alarmHigh !== undefined && hasValue && value >= alarmHigh;
  const isLow = alarmLow !== undefined && hasValue && value <= alarmLow;
  const alarmClass = isHigh ? "alarm-high" : isLow ? "alarm-low" : "";

  return (
    <div className={`analog-display ${isStale ? "stale" : ""} ${alarmClass}`}>
      <div className="ad-label">{label}</div>
      <div className="ad-value">
        {hasValue ? value.toFixed(decimals) : "--.-"}
        <span className="ad-unit">{unit}</span>
      </div>
      <div className="ad-bar">
        <div className={`ad-fill ${alarmClass}`} style={{ width: `${pct}%` }} />
      </div>
      <div className="ad-range">
        <span>{min}</span>
        <span>
          {max} {unit}
        </span>
      </div>
    </div>
  );
});
