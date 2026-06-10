// Coil yazma kontrolu (FC05) — motor/lamba ac-kapa.
// Mevcut coil degerini gosterir; AC/KAPA butonlari ile gateway'e WRITE_COIL gonderir.
import { useHMIStore } from "../store/hmiStore.js";
import { useTagValue, useTagMeta } from "../hooks/useTagValue.js";
import { sendWrite } from "../hooks/useWebSocket.js";

export function CoilControl({ tag }) {
  const { value } = useTagValue(tag);
  const meta = useTagMeta(tag);
  const isConnected = useHMIStore((s) => s.connectionStatus === "CONNECTED");
  const ack = useHMIStore((s) => s.writeAcks[tag]);

  const label = meta?.label || tag;
  const disabled = !isConnected || !meta?.writable;

  const write = (v) => sendWrite("WRITE_COIL", tag, v);

  return (
    <div className="coil-control">
      <span className="cc-label">{label}</span>
      <span className={`cc-state ${value ? "on" : "off"}`}>
        {value === null ? "?" : value ? "ON" : "OFF"}
      </span>
      <div className="cc-buttons">
        <button
          className="cc-btn cc-on"
          disabled={disabled || value === true}
          onClick={() => write(true)}
        >
          AC
        </button>
        <button
          className="cc-btn cc-off"
          disabled={disabled || value === false}
          onClick={() => write(false)}
        >
          KAPA
        </button>
      </div>
      {ack && ack.success === false && (
        <span className="cc-error" title={ack.error}>
          ! {ack.error}
        </span>
      )}
    </div>
  );
}
