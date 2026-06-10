"""
ui/alarm_panel.py — Alarm tablosu (ISA-18.2 esinli, sadeleştirilmiş).

Acknowledge != Resolved ayrımı (knowledge/hmi/architecture/03_alarm_management.md):
- AKTIF: koşul hâlâ var.
- KAPANDI: koşul ortadan kalktı ama operatör onaylamadıysa listede kalır.
- Operatör onaylayınca (Acknowledge) ve koşul da kapandıysa satır temizlenir.

Bu template'te alarmlar PLC'deki boolean alarm bayraklarından türetilir
(xEStopActive=A001, xZone2Itlk=A060, aZoneJam[i], aZoneSpdFlt[i], aZoneTacBrk[i]).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


@dataclass
class AlarmRecord:
    code: str          # ör. "A001", "JAM-Z2"
    text: str          # operatör mesajı
    active: bool        # koşul hâlâ var mı
    acknowledged: bool  # operatör gördü mü
    raised_at: datetime


class AlarmPanel(QWidget):
    """Aktif/onaylanmamış alarmları gösteren tablo + onay butonu."""

    _HEADERS = ["Zaman", "Kod", "Mesaj", "Durum", "Onay"]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._alarms: dict[str, AlarmRecord] = {}

        self._table = QTableWidget(0, len(self._HEADERS))
        self._table.setHorizontalHeaderLabels(self._HEADERS)
        self._table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self._btn_ack = QPushButton("Seçili Alarmı Onayla")
        self._btn_ack_all = QPushButton("Tümünü Onayla")
        self._btn_ack.clicked.connect(self._ack_selected)
        self._btn_ack_all.clicked.connect(self._ack_all)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self._btn_ack)
        btn_row.addWidget(self._btn_ack_all)

        layout = QVBoxLayout(self)
        layout.addWidget(self._table)
        layout.addLayout(btn_row)

    def set_condition(self, code: str, text: str, active: bool) -> None:
        """PLC alarm bayrağına göre alarm durumunu günceller.

        Yeni aktif alarm -> kayıt oluşturulur. Koşul kapanır ve onaylanmışsa
        kayıt silinir; onaylanmamışsa "KAPANDI" olarak listede kalır.
        """
        rec = self._alarms.get(code)
        if active:
            if rec is None:
                self._alarms[code] = AlarmRecord(
                    code=code, text=text, active=True,
                    acknowledged=False, raised_at=datetime.now(),
                )
            else:
                rec.active = True
        else:
            if rec is not None:
                rec.active = False
                if rec.acknowledged:
                    del self._alarms[code]
        self._refresh()

    def _ack_selected(self) -> None:
        row = self._table.currentRow()
        if row < 0:
            return
        code_item = self._table.item(row, 1)
        if code_item is None:
            return
        self._acknowledge(code_item.text())

    def _ack_all(self) -> None:
        for code in list(self._alarms.keys()):
            self._acknowledge(code)

    def _acknowledge(self, code: str) -> None:
        rec = self._alarms.get(code)
        if rec is None:
            return
        rec.acknowledged = True
        if not rec.active:  # Onaylandı + koşul kapalı -> temizle
            del self._alarms[code]
        self._refresh()

    def _refresh(self) -> None:
        rows = sorted(self._alarms.values(), key=lambda r: r.raised_at)
        self._table.setRowCount(len(rows))
        for i, rec in enumerate(rows):
            if rec.active:
                status = "AKTİF"
                color = QColor("#B71C1C")
            else:
                status = "KAPANDI"
                color = QColor("#F9A825")
            ack = "EVET" if rec.acknowledged else "—"
            values = [rec.raised_at.strftime("%H:%M:%S"), rec.code, rec.text, status, ack]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                if col == 3:
                    item.setBackground(color)
                    item.setForeground(QColor("#fff"))
                self._table.setItem(i, col, item)
        self._table.resizeColumnsToContents()
        self._table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
