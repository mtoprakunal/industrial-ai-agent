"""
main.py — EXAMPLE_conveyor için Tkinter + asyncua masaüstü HMI.

Mimari özeti:
- Yalnızca stdlib Tkinter (ek GUI bağımlılığı yok) + asyncua.
- OPC-UA IO ayrı daemon thread'inde (opcua_client.py, asyncua.sync + ThreadLoop).
- Tkinter `after(UI_REFRESH_MS)` döngüsü, worker'ın thread-safe snapshot'ını
  okuyup widget'ları günceller. GUI thread'inde HİÇBİR ağ IO yapılmaz.
- Heartbeat watchdog: uHeartbeat değişmezse "VERİ BAYAT" + komut butonları kilitli.

Çalıştırma:
    pip install -r requirements.txt
    python main.py
"""

from __future__ import annotations

import logging
import tkinter as tk
from datetime import datetime
from tkinter import ttk

import config
from opcua_client import OpcUaConveyorClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ISA-101 renkleri
COLOR_IDLE = "#9E9E9E"
COLOR_RUN = "#388E3C"
COLOR_WARN = "#F9A825"
COLOR_FAULT = "#B71C1C"
COLOR_STALE = "#9E9E9E"

_STATE_COLORS = {
    "IDLE": COLOR_IDLE,
    "STARTING": COLOR_WARN,
    "RUNNING": COLOR_RUN,
    "STOPPING": "#F57F17",
    "JAM": "#E65100",
    "FAULT": COLOR_FAULT,
}


class ZoneFrame(ttk.LabelFrame):
    """Tek bölge göstergesi."""

    def __init__(self, master, zone_no: int) -> None:
        super().__init__(master, text=f"Bölge {zone_no}")
        self._state = tk.Label(self, text="—", width=12, height=2,
                               bg=COLOR_IDLE, fg="white", font=("TkDefaultFont", 11, "bold"))
        self._state.pack(padx=6, pady=4, fill="x")
        self._speed = ttk.Label(self, text="Hız: —- m/min")
        self._speed.pack(padx=6)
        self._mode = ttk.Label(self, text="Mod: —")
        self._mode.pack(padx=6, pady=(0, 6))

    def set_state(self, name: str) -> None:
        self._state.config(text=name, bg=_STATE_COLORS.get(name, COLOR_IDLE))

    def set_speed(self, value: float) -> None:
        self._speed.config(text=f"Hız: {value:.1f} m/min")

    def set_mode(self, is_auto: bool) -> None:
        self._mode.config(text=f"Mod: {'OTO' if is_auto else 'MANUEL'}")

    def set_stale(self) -> None:
        self._state.config(text="VERİ YOK", bg=COLOR_STALE)


class HmiApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("EXAMPLE_conveyor — Tkinter OPC-UA HMI")
        self.geometry("820x620")

        self._client = OpcUaConveyorClient()
        self._auto_vars: list[tk.BooleanVar] = []

        self._build_ui()

        self._client.start()
        self.after(config.UI_REFRESH_MS, self._refresh)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # --- UI kurulum ---

    def _build_ui(self) -> None:
        # Durum şeridi
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=8, pady=6)
        self._lbl_conn = tk.Label(bar, text="BAĞLI DEĞİL", width=14, bg=COLOR_FAULT, fg="white")
        self._lbl_estop = tk.Label(bar, text="E-STOP", width=14, bg=COLOR_IDLE, fg="white")
        self._lbl_permit = tk.Label(bar, text="İZİN", width=14, bg=COLOR_IDLE, fg="white")
        self._lbl_alarm = tk.Label(bar, text="ALARM", width=14, bg=COLOR_IDLE, fg="white")
        for w in (self._lbl_conn, self._lbl_estop, self._lbl_permit, self._lbl_alarm):
            w.pack(side="left", padx=4)

        # Bölgeler
        zones = ttk.Frame(self)
        zones.pack(fill="x", padx=8, pady=6)
        self._zones: list[ZoneFrame] = []
        for z in range(1, config.ZONE_COUNT + 1):
            zf = ZoneFrame(zones, z)
            zf.pack(side="left", expand=True, fill="both", padx=4)
            self._zones.append(zf)

        # Komutlar
        cmds = ttk.LabelFrame(self, text="Komutlar")
        cmds.pack(fill="x", padx=8, pady=6)
        self._auto_checks: list[ttk.Checkbutton] = []
        for z in range(1, config.ZONE_COUNT + 1):
            var = tk.BooleanVar(value=False)
            self._auto_vars.append(var)
            chk = ttk.Checkbutton(
                cmds, text=f"Bölge {z} Oto Run", variable=var,
                command=lambda zn=z: self._on_auto_run(zn),
            )
            chk.pack(side="left", padx=8, pady=6)
            self._auto_checks.append(chk)
        self._btn_reset = ttk.Button(cmds, text="RESET", command=self._on_reset)
        self._btn_reset.pack(side="right", padx=8)

        # Alarm listesi
        alarm_box = ttk.LabelFrame(self, text="Alarmlar")
        alarm_box.pack(fill="both", expand=True, padx=8, pady=6)
        cols = ("zaman", "kod", "mesaj", "durum")
        self._tree = ttk.Treeview(alarm_box, columns=cols, show="headings", height=8)
        for c, w in zip(cols, (90, 80, 320, 90)):
            self._tree.heading(c, text=c.capitalize())
            self._tree.column(c, width=w)
        self._tree.pack(fill="both", expand=True, side="left")
        sb = ttk.Scrollbar(alarm_box, orient="vertical", command=self._tree.yview)
        sb.pack(side="right", fill="y")
        self._tree.configure(yscrollcommand=sb.set)

        # Onaylanmış (active=False) alarmlar için izleme
        self._acked: set[str] = set()

    def _set_commands_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for chk in self._auto_checks:
            chk.config(state=state)
        self._btn_reset.config(state=state)

    # --- Komut handler'ları (worker kuyruğuna iletir) ---

    def _on_auto_run(self, zone_no: int) -> None:
        value = self._auto_vars[zone_no - 1].get()
        self._client.command_auto_run(zone_no, value)

    def _on_reset(self) -> None:
        self._client.command_reset()

    # --- Periyodik GUI yenileme (after döngüsü) ---

    def _refresh(self) -> None:
        try:
            self._do_refresh()
        finally:
            self.after(config.UI_REFRESH_MS, self._refresh)

    def _do_refresh(self) -> None:
        if not self._client.connected:
            self._lbl_conn.config(text="BAĞLI DEĞİL", bg=COLOR_FAULT)
            self._set_commands_enabled(False)
            return

        if self._client.heartbeat_stale():
            self._lbl_conn.config(text="VERİ BAYAT", bg=COLOR_WARN)
            for zf in self._zones:
                zf.set_stale()
            self._set_commands_enabled(False)
            return

        self._lbl_conn.config(text="BAĞLI", bg=COLOR_RUN)
        self._set_commands_enabled(True)

        snap = self._client.get_snapshot()

        states = _as_list(snap.get("aZoneState"))
        speeds = _as_list(snap.get("aZoneSpeed"))
        autos = _as_list(snap.get("aZoneAuto"))
        for i, zf in enumerate(self._zones):
            if i < len(states):
                zf.set_state(config.ZONE_STATE_NAMES.get(int(states[i]), "?"))
            if i < len(speeds):
                zf.set_speed(float(speeds[i]))
            if i < len(autos):
                zf.set_mode(bool(autos[i]))

        estop = bool(snap.get("xEStopActive", False))
        self._lbl_estop.config(text="E-STOP AKTİF" if estop else "E-STOP OK",
                               bg=COLOR_FAULT if estop else COLOR_RUN)
        permit = bool(snap.get("xRunPermit", False))
        self._lbl_permit.config(text="İZİN VAR" if permit else "İZİN YOK",
                                bg=COLOR_RUN if permit else "#E65100")
        any_alarm = bool(snap.get("xAnyAlarm", False))
        self._lbl_alarm.config(text="ALARM" if any_alarm else "NORMAL",
                               bg=COLOR_FAULT if any_alarm else COLOR_RUN)

        self._refresh_alarms(snap)

    def _refresh_alarms(self, snap: dict) -> None:
        """PLC boolean bayraklarından aktif alarm listesi türetir."""
        rows: list[tuple[str, str, str, bool]] = []
        rows.append(("A001", "Acil Stop aktif", bool(snap.get("xEStopActive", False)), False))
        rows.append(("A060", "Bölge 2 interlock", bool(snap.get("xZone2Itlk", False)), False))
        for key, code, text in (
            ("aZoneJam", "JAM", "Sıkışma"),
            ("aZoneSpdFlt", "SPD", "Hız arızası"),
            ("aZoneTacBrk", "TAC", "Takometre kablo kopması"),
        ):
            flags = _as_list(snap.get(key))
            for i, active in enumerate(flags):
                rows.append((f"{code}-Z{i+1}", f"Bölge {i+1} {text}", bool(active), False))

        self._tree.delete(*self._tree.get_children())
        now = datetime.now().strftime("%H:%M:%S")
        for code, text, active, _ in rows:
            if not active:
                continue
            self._tree.insert("", "end", values=(now, code, text, "AKTİF"))

    def _on_close(self) -> None:
        self._client.stop()
        self.destroy()


def _as_list(value: object) -> list:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


if __name__ == "__main__":
    HmiApp().mainloop()
