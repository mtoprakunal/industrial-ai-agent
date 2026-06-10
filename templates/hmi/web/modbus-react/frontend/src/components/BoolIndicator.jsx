// Boolean (coil / discrete input) durum gostergesi — salt okunur.
// ISA-101: normal=gri, aktif=renkli; renk + sekil + metin birlikte (renk koru).
import React from "react";
import { useTagValue, useTagMeta } from "../hooks/useTagValue.js";

export const BoolIndicator = React.memo(function BoolIndicator({
  tag,
  onLabel = "AKTIF",
  offLabel = "PASIF",
}) {
  const { value, isStale } = useTagValue(tag);
  const meta = useTagMeta(tag);
  const label = meta?.label || tag;

  const state = isStale || value === null ? "unknown" : value ? "on" : "off";

  return (
    <div className={`bool-indicator state-${state}`}>
      <span className="bool-dot" aria-hidden="true" />
      <span className="bool-label">{label}</span>
      <span className="bool-text">
        {state === "unknown" ? "?" : value ? onLabel : offLabel}
      </span>
    </div>
  );
});
