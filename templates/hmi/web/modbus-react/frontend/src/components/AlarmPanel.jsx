// Alarm paneli — ISA-18.2 onceliklendirme (CRITICAL/HIGH/MEDIUM/LOW).
// Gateway "ALARM" mesajlari ile aktif/normal durumlari iter; burada yalnizca
// AKTIF olanlar listelenir. (Bu sablon onaylama/acknowledge tutmaz; gercek
// projede ack durumu ve gecmis eklenir — bkz. architecture/03_alarm_management.)
import { useHMIStore } from "../store/hmiStore.js";

const PRIORITY_ORDER = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
const PRIORITY_ICON = { CRITICAL: "▲▲▲", HIGH: "▲▲", MEDIUM: "▲", LOW: "●" };

export function AlarmPanel() {
  const alarms = useHMIStore((s) => s.alarms);

  const active = Object.entries(alarms)
    .filter(([, a]) => a.active)
    .sort(
      ([, a], [, b]) =>
        (PRIORITY_ORDER[a.priority] ?? 9) - (PRIORITY_ORDER[b.priority] ?? 9)
    );

  if (active.length === 0) {
    return <div className="alarm-panel no-alarms">Aktif alarm yok</div>;
  }

  return (
    <div className="alarm-panel">
      <h3>Aktif Alarmlar ({active.length})</h3>
      <ul className="alarm-list">
        {active.map(([tag, a]) => (
          <li key={tag} className={`alarm-item priority-${a.priority?.toLowerCase()}`}>
            <span className="alarm-icon" aria-hidden="true">
              {PRIORITY_ICON[a.priority] || "●"}
            </span>
            <span className="alarm-text">{a.text || a.label || tag}</span>
            <span className="alarm-time">
              {new Date(a.timestamp).toLocaleTimeString("tr-TR")}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
