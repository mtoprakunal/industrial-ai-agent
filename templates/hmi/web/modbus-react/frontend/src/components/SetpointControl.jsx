// Holding register yazma kontrolu (FC06) — setpoint girisi.
// Yerel input state'i kullanir (WS degerini input'a baglamaz; aksi halde
// operator yazarken deger ziplar — Not 7 / kontrollu input tuzagi).
import { useState } from "react";
import { useHMIStore } from "../store/hmiStore.js";
import { useTagValue, useTagMeta } from "../hooks/useTagValue.js";
import { sendWrite } from "../hooks/useWebSocket.js";

export function SetpointControl({ tag }) {
  const { value: current } = useTagValue(tag);
  const meta = useTagMeta(tag);
  const isConnected = useHMIStore((s) => s.connectionStatus === "CONNECTED");
  const ack = useHMIStore((s) => s.writeAcks[tag]);

  const [input, setInput] = useState("");

  const label = meta?.label || tag;
  const unit = meta?.unit || "";
  const min = meta?.min ?? 0;
  const max = meta?.max ?? 100;
  const step = meta?.step ?? 1;
  const disabled = !isConnected || !meta?.writable;

  const handleApply = () => {
    const v = parseFloat(input);
    if (Number.isNaN(v) || v < min || v > max) {
      alert(`Deger ${min}-${max} ${unit} araliginda olmali`);
      return;
    }
    // Olcekleme gateway'de yapilir; ham muhendislik degeri gonderiyoruz.
    sendWrite("WRITE_REGISTER", tag, v);
    setInput("");
  };

  return (
    <div className="setpoint-control">
      <label className="sp-label">{label}</label>
      <div className="sp-current">
        Mevcut: {current !== null ? Number(current).toFixed(1) : "--"} {unit}
      </div>
      <div className="sp-row">
        <input
          type="number"
          className="sp-input"
          min={min}
          max={max}
          step={step}
          value={input}
          placeholder={current !== null ? Number(current).toFixed(1) : "--"}
          onChange={(e) => setInput(e.target.value)}
          disabled={disabled}
        />
        <span className="sp-unit">{unit}</span>
        <button
          className="sp-apply"
          onClick={handleApply}
          disabled={disabled || input === ""}
        >
          Uygula
        </button>
      </div>
      {ack && ack.success === false && (
        <span className="sp-error">Yazma hatasi: {ack.error}</span>
      )}
    </div>
  );
}
