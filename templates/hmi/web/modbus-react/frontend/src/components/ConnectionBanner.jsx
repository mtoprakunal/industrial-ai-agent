// Baglanti durumu banner'i — PLC <-> gateway baglantisi koptugunda gorunur.
import { useHMIStore } from "../store/hmiStore.js";

export function ConnectionBanner() {
  const status = useHMIStore((s) => s.connectionStatus);
  if (status === "CONNECTED") return null;

  const messages = {
    DISCONNECTED: "PLC/gateway baglantisi kesildi — yeniden baglaniliyor...",
    CONNECTING: "Gateway'e baglaniliyor...",
    ERROR: "Baglanti hatasi — gateway calisiyor mu?",
  };

  return (
    <div className={`conn-banner status-${status.toLowerCase()}`}>
      {messages[status] || status}
    </div>
  );
}
