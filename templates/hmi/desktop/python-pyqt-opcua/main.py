"""
main.py — EXAMPLE_conveyor için PyQt6 + asyncua masaüstü HMI.

Mimari özeti:
- qasync ile Qt event loop'u = asyncio event loop (TEK thread, GUI thread).
  asyncua çağrıları @asyncSlot ile GUI thread'inde await edilir.
- OPC-UA subscription verisi thread-safe queue'ya yazılır; bir QTimer (100ms)
  queue'yu boşaltıp coalesce ederek widget'ları günceller (boyama coalescing).
- Heartbeat watchdog: uHeartbeat değişmezse "VERİ BAYAT" gösterilir, yazma
  butonları devre dışı bırakılır (stale-data güvenlik kuralı).

Çalıştırma:
    pip install -r requirements.txt
    python main.py
"""

from __future__ import annotations

import asyncio
import logging
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from qasync import QEventLoop, asyncClose, asyncSlot

import config
from opcua_client import OpcUaConveyorClient
from ui.alarm_panel import AlarmPanel
from ui.widgets import StatusBanner, ZoneWidget

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("EXAMPLE_conveyor — PyQt6 OPC-UA HMI")
        self.resize(900, 650)

        self._client = OpcUaConveyorClient()
        # En son alınan değerlerin anlık görüntüsü (queue flush hedefi).
        self._snapshot: dict[str, object] = {}

        self._build_ui()

        # GUI güncelleme timer'ı — queue'yu boşalt + watchdog + UI yenile.
        self._ui_timer = QTimer(self)
        self._ui_timer.setInterval(config.UI_FLUSH_INTERVAL_MS)
        self._ui_timer.timeout.connect(self._flush_and_refresh)
        self._ui_timer.start()

    # --- UI kurulum ---

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        self._banner = StatusBanner()
        root.addWidget(self._banner)

        # Bölge göstergeleri
        zones_box = QGroupBox("Konveyör Bölgeleri")
        zones_layout = QHBoxLayout(zones_box)
        self._zones: list[ZoneWidget] = []
        for z in range(1, config.ZONE_COUNT + 1):
            w = ZoneWidget(z)
            self._zones.append(w)
            zones_layout.addWidget(w)
        root.addWidget(zones_box)

        # Komut butonları
        cmd_box = QGroupBox("Komutlar")
        cmd_layout = QGridLayout(cmd_box)
        self._auto_buttons: list[QPushButton] = []
        for z in range(1, config.ZONE_COUNT + 1):
            btn = QPushButton(f"Bölge {z} Oto Run")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, zn=z: self._on_auto_run(zn, checked))
            self._auto_buttons.append(btn)
            cmd_layout.addWidget(btn, 0, z - 1)

        self._btn_reset = QPushButton("RESET")
        self._btn_reset.clicked.connect(self._on_reset)
        cmd_layout.addWidget(self._btn_reset, 1, 0, 1, config.ZONE_COUNT)
        root.addWidget(cmd_box)

        # Alarm paneli
        alarm_box = QGroupBox("Alarmlar")
        alarm_layout = QVBoxLayout(alarm_box)
        self._alarms = AlarmPanel()
        alarm_layout.addWidget(self._alarms)
        root.addWidget(alarm_box)

        # Bağlan / kes
        conn_row = QHBoxLayout()
        self._btn_connect = QPushButton("Bağlan")
        self._btn_disconnect = QPushButton("Bağlantıyı Kes")
        self._btn_connect.clicked.connect(self._on_connect)
        self._btn_disconnect.clicked.connect(self._on_disconnect)
        conn_row.addWidget(self._btn_connect)
        conn_row.addWidget(self._btn_disconnect)
        root.addLayout(conn_row)

        self._set_commands_enabled(False)
        self._banner.set_connection("DISCONNECTED")

    def _set_commands_enabled(self, enabled: bool) -> None:
        for btn in self._auto_buttons:
            btn.setEnabled(enabled)
        self._btn_reset.setEnabled(enabled)

    # --- Bağlantı slot'ları (async) ---

    @asyncSlot()
    async def _on_connect(self) -> None:
        self._banner.set_connection("DISCONNECTED")
        self._btn_connect.setEnabled(False)
        try:
            await self._client.connect()
            self._banner.set_connection("CONNECTED")
            self._set_commands_enabled(True)
        except Exception as exc:  # noqa: BLE001
            logging.error("Bağlantı hatası: %s", exc)
            self._banner.set_connection("DISCONNECTED")
            self._btn_connect.setEnabled(True)

    @asyncSlot()
    async def _on_disconnect(self) -> None:
        await self._client.disconnect()
        self._set_commands_enabled(False)
        self._btn_connect.setEnabled(True)
        self._banner.set_connection("DISCONNECTED")

    @asyncSlot()
    async def _on_auto_run(self, zone_no: int, checked: bool) -> None:
        try:
            await self._client.write_auto_run(zone_no, checked)
        except Exception as exc:  # noqa: BLE001
            logging.error("axCmdAutoRun yazma hatası: %s", exc)

    @asyncSlot()
    async def _on_reset(self) -> None:
        try:
            await self._client.write_reset(True)
        except Exception as exc:  # noqa: BLE001
            logging.error("xCmdReset yazma hatası: %s", exc)

    # --- Periyodik GUI güncelleme ---

    def _flush_and_refresh(self) -> None:
        """Queue'yu boşalt (coalescing), watchdog'u kontrol et, UI'yi güncelle."""
        # 1) Subscription queue'sunu boşalt -> snapshot
        q = self._client.data_queue
        while not q.empty():
            try:
                node_id, value = q.get_nowait()
            except Exception:  # noqa: BLE001
                break
            name = self._client.resolve_name(node_id)
            if name is None:
                continue
            self._snapshot[name] = value
            if name == "uHeartbeat" and isinstance(value, int):
                self._client.update_heartbeat(value)

        if not self._client.connected:
            return

        # 2) Watchdog
        if self._client.heartbeat_stale():
            self._banner.set_connection("STALE")
            for w in self._zones:
                w.set_stale()
            self._set_commands_enabled(False)
            return

        self._banner.set_connection("CONNECTED")
        self._set_commands_enabled(True)

        # 3) Bölgeler — array değerleri liste olarak gelir (CODESYS ARRAY[1..3]).
        states = self._as_list(self._snapshot.get("aZoneState"))
        speeds = self._as_list(self._snapshot.get("aZoneSpeed"))
        autos = self._as_list(self._snapshot.get("aZoneAuto"))
        for i, w in enumerate(self._zones):
            if i < len(states):
                w.set_state(config.ZONE_STATE_NAMES.get(int(states[i]), "?"))
            if i < len(speeds):
                w.set_speed(float(speeds[i]))
            if i < len(autos):
                w.set_auto(bool(autos[i]))

        # 4) Banner durumları
        self._banner.set_estop(bool(self._snapshot.get("xEStopActive", False)))
        self._banner.set_permit(bool(self._snapshot.get("xRunPermit", False)))
        self._banner.set_any_alarm(bool(self._snapshot.get("xAnyAlarm", False)))

        # 5) Alarmlar — PLC boolean bayraklarından türet
        self._update_alarms()

    def _update_alarms(self) -> None:
        self._alarms.set_condition("A001", "Acil Stop aktif", bool(self._snapshot.get("xEStopActive", False)))
        self._alarms.set_condition("A060", "Bölge 2 interlock", bool(self._snapshot.get("xZone2Itlk", False)))
        for key, code, text in (
            ("aZoneJam", "JAM", "Sıkışma"),
            ("aZoneSpdFlt", "SPD", "Hız arızası"),
            ("aZoneTacBrk", "TAC", "Takometre kablo kopması"),
        ):
            flags = self._as_list(self._snapshot.get(key))
            for i, active in enumerate(flags):
                zn = i + 1
                self._alarms.set_condition(f"{code}-Z{zn}", f"Bölge {zn} {text}", bool(active))

    @staticmethod
    def _as_list(value: object) -> list:
        if value is None:
            return []
        if isinstance(value, (list, tuple)):
            return list(value)
        return [value]

    @asyncClose
    async def closeEvent(self, event) -> None:  # noqa: ANN001, N802
        await self._client.disconnect()


def main() -> None:
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    with loop:
        loop.run_until_complete(app_close_event.wait())


if __name__ == "__main__":
    main()
