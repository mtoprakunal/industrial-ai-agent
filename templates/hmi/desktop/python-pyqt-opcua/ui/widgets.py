"""
ui/widgets.py — Yeniden kullanılabilir HMI widget'ları.

ISA-101 renk kuralları (knowledge/hmi/desktop/03_pyqt_patterns.md):
- Normal/durağan: gri
- Çalışıyor: yeşil
- Arıza/alarm: kırmızı
- Bayat (stale) veri: gri + italik
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

# ISA-101 durum stilleri (03_pyqt_patterns ALARM/STATUS_STYLES ile uyumlu)
_STATE_STYLES = {
    "IDLE": "background-color:#9E9E9E;color:#fff;",
    "STARTING": "background-color:#F9A825;color:#000;",
    "RUNNING": "background-color:#388E3C;color:#fff;",
    "STOPPING": "background-color:#F57F17;color:#fff;",
    "JAM": "background-color:#E65100;color:#fff;font-weight:bold;",
    "FAULT": "background-color:#B71C1C;color:#fff;font-weight:bold;",
    "STALE": "background-color:#9E9E9E;color:#fff;font-style:italic;",
}

_BASE = "border-radius:4px;padding:6px;"


class ZoneWidget(QFrame):
    """Tek bir konveyör bölgesi için durum + hız göstergesi."""

    def __init__(self, zone_no: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._zone_no = zone_no
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self._title = QLabel(f"Bölge {zone_no}")
        self._title.setStyleSheet("font-weight:bold;font-size:14px;")

        self._state = QLabel("—")
        self._state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._state.setMinimumHeight(36)
        self._state.setStyleSheet(_STATE_STYLES["IDLE"] + _BASE)

        self._speed = QLabel("Hız: —- m/min")
        self._auto = QLabel("Mod: —")

        layout = QVBoxLayout(self)
        layout.addWidget(self._title)
        layout.addWidget(self._state)
        layout.addWidget(self._speed)
        layout.addWidget(self._auto)

    def set_state(self, state_name: str) -> None:
        self._state.setText(state_name)
        self._state.setStyleSheet(_STATE_STYLES.get(state_name, _STATE_STYLES["IDLE"]) + _BASE)

    def set_speed(self, speed: float) -> None:
        self._speed.setText(f"Hız: {speed:.1f} m/min")

    def set_auto(self, is_auto: bool) -> None:
        self._auto.setText(f"Mod: {'OTO' if is_auto else 'MANUEL'}")

    def set_stale(self) -> None:
        self._state.setText("VERİ YOK")
        self._state.setStyleSheet(_STATE_STYLES["STALE"] + _BASE)


class StatusBanner(QWidget):
    """Üst bilgi şeridi: E-Stop, çalışma izni, genel alarm, bağlantı."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._estop = QLabel("E-STOP")
        self._permit = QLabel("İZİN")
        self._alarm = QLabel("ALARM")
        self._conn = QLabel("BAĞLANTI")

        for lbl in (self._estop, self._permit, self._alarm, self._conn):
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setMinimumHeight(32)
            lbl.setStyleSheet("background-color:#9E9E9E;color:#fff;" + _BASE)

        layout = QHBoxLayout(self)
        for lbl in (self._estop, self._permit, self._alarm, self._conn):
            layout.addWidget(lbl)

    def set_estop(self, active: bool) -> None:
        if active:
            self._estop.setText("E-STOP AKTİF")
            self._estop.setStyleSheet("background-color:#B71C1C;color:#fff;font-weight:bold;" + _BASE)
        else:
            self._estop.setText("E-STOP OK")
            self._estop.setStyleSheet("background-color:#388E3C;color:#fff;" + _BASE)

    def set_permit(self, ok: bool) -> None:
        self._permit.setText("İZİN VAR" if ok else "İZİN YOK")
        color = "#388E3C" if ok else "#E65100"
        self._permit.setStyleSheet(f"background-color:{color};color:#fff;" + _BASE)

    def set_any_alarm(self, active: bool) -> None:
        self._alarm.setText("ALARM" if active else "NORMAL")
        color = "#B71C1C" if active else "#388E3C"
        weight = "font-weight:bold;" if active else ""
        self._alarm.setStyleSheet(f"background-color:{color};color:#fff;{weight}" + _BASE)

    def set_connection(self, state: str) -> None:
        """state: 'CONNECTED' | 'STALE' | 'DISCONNECTED'."""
        text, color = {
            "CONNECTED": ("BAĞLI", "#388E3C"),
            "STALE": ("VERİ BAYAT", "#F9A825"),
            "DISCONNECTED": ("BAĞLI DEĞİL", "#B71C1C"),
        }.get(state, ("?", "#9E9E9E"))
        self._conn.setText(text)
        self._conn.setStyleSheet(f"background-color:{color};color:#fff;" + _BASE)
