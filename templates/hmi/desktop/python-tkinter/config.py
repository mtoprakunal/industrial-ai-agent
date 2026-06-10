"""
config.py — OPC-UA bağlantı ve node konfigürasyonu (Tkinter HMI).

EXAMPLE_conveyor CODESYS PLC'sine doğrudan bağlanır. PyQt şablonuyla aynı
mantığı izler; bkz. ../python-pyqt-opcua/config.py açıklamaları.
"""

# --- Sunucu / endpoint ---
OPCUA_ENDPOINT = "opc.tcp://192.168.1.100:4840"
CODESYS_NS_URI = "http://www.3s-software.com/schemas/Codesys-V3"

RUNTIME_NAME = "CODESYS Control Win V3"
APPLICATION_NAME = "Application"
GVL_HMI = "GVL_HMI"

# --- Güvenlik ---
USE_SECURITY = False
OPCUA_USERNAME = None
OPCUA_PASSWORD = None

# --- Zamanlama ---
POLL_INTERVAL_S = 0.3          # Arka plan thread okuma periyodu (saniye)
UI_REFRESH_MS = 200            # Tkinter after() ile GUI yenileme periyodu (ms)
HEARTBEAT_TIMEOUT_MS = 3000    # uHeartbeat bu süre değişmezse "VERİ BAYAT"

ZONE_COUNT = 3


def _node(var_name: str) -> str:
    return f"|var|{RUNTIME_NAME}.{APPLICATION_NAME}.{GVL_HMI}.{var_name}"


# İzleme node'ları (PLC -> HMI, salt okunur)
READ_NODES = {
    "aZoneState": _node("aZoneState"),
    "aZoneSpeed": _node("aZoneSpeed"),
    "aZoneRunning": _node("aZoneRunning"),
    "aZoneJam": _node("aZoneJam"),
    "aZoneSpdFlt": _node("aZoneSpdFlt"),
    "aZoneTacBrk": _node("aZoneTacBrk"),
    "aZoneAuto": _node("aZoneAuto"),
    "xEStopActive": _node("xEStopActive"),
    "xRunPermit": _node("xRunPermit"),
    "xZone2Itlk": _node("xZone2Itlk"),
    "xAnyAlarm": _node("xAnyAlarm"),
    "uHeartbeat": _node("uHeartbeat"),
}

# Komut node'ları (HMI -> PLC)
WRITE_NODES = {
    "axCmdAutoRun": _node("axCmdAutoRun"),
    "xCmdReset": _node("xCmdReset"),
}

ZONE_STATE_NAMES = {
    0: "IDLE",
    1: "STARTING",
    2: "RUNNING",
    3: "STOPPING",
    4: "JAM",
    5: "FAULT",
}
