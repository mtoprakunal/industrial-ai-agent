"""
config.py — OPC-UA bağlantı ve node konfigürasyonu.

Bu masaüstü HMI, EXAMPLE_conveyor projesindeki CODESYS PLC'ye DOĞRUDAN
(gateway olmadan) bağlanır. Tag'ler GVL_HMI içindeki Symbol Configuration
ile OPC-UA node olarak açılmıştır.

ÖNEMLI:
- Namespace index (ns=) ASLA sabit yazılmaz; bağlantı sonrası URI'den alınır
  (bkz. opcua_client.py -> get_namespace_index). Burada yalnızca NodeId'nin
  ns'siz "identifier" (string) kısmını tutarız.
- CODESYS Runtime adı kuruluma göre değişir (Win V3, SL, vb.). Aşağıdaki
  RUNTIME_NAME değerini UaExpert ile sunucudan doğrulayın.
"""

# --- Sunucu / endpoint ---
# CODESYS OPC-UA Server varsayılan port: 4840
OPCUA_ENDPOINT = "opc.tcp://192.168.1.100:4840"

# CODESYS namespace URI'si — bağlantıda bu URI üzerinden index alınır.
# Controller modeline göre değişebilir; UaExpert ile NamespaceArray'i kontrol edin.
CODESYS_NS_URI = "http://www.3s-software.com/schemas/Codesys-V3"

# CODESYS NodeId yolundaki Runtime + Application adı.
# Format: |var|<RuntimeAdı>.<ApplicationAdı>.<GVL>.<DeğişkenAdı>
RUNTIME_NAME = "CODESYS Control Win V3"
APPLICATION_NAME = "Application"
GVL_HMI = "GVL_HMI"

# --- Güvenlik ---
# Geliştirme: anonymous + güvenliksiz kanal. Üretim: True + sertifika/kullanıcı.
USE_SECURITY = False
OPCUA_USERNAME: str | None = None  # örn. "opc_operator"
OPCUA_PASSWORD: str | None = None

# --- Subscription / watchdog ---
PUBLISHING_INTERVAL_MS = 500       # Sunucudan bildirim periyodu
SAMPLING_INTERVAL_MS = 200         # Sunucu örnekleme periyodu
HEARTBEAT_TIMEOUT_MS = 3000        # uHeartbeat bu süre değişmezse bağlantı "bayat"
UI_FLUSH_INTERVAL_MS = 100         # GUI güncelleme (coalescing) periyodu

# Bölge sayısı (EXAMPLE_conveyor: 3 bölge)
ZONE_COUNT = 3


def _node(var_name: str) -> str:
    """GVL_HMI içindeki bir değişken için ns'siz NodeId identifier'ı üretir.

    Dönen string, opcua_client içinde 'ns={ns};s=' ön eki ile birleştirilir.
    """
    return f"|var|{RUNTIME_NAME}.{APPLICATION_NAME}.{GVL_HMI}.{var_name}"


# --- İzlenen (PLC -> HMI, salt okunur) node identifier'ları ---
# CODESYS ARRAY[1..3] OPC-UA tarafında genelde tek bir array node olarak açılır;
# array'in tamamı tek okuma ile gelir ve [1..3] elemanlarına indekslenir.
READ_NODES = {
    "aZoneState": _node("aZoneState"),     # ARRAY[1..3] OF E_ZoneState (INT)
    "aZoneSpeed": _node("aZoneSpeed"),     # ARRAY[1..3] OF REAL (m/min)
    "aZoneRunning": _node("aZoneRunning"),  # ARRAY[1..3] OF BOOL
    "aZoneJam": _node("aZoneJam"),         # ARRAY[1..3] OF BOOL
    "aZoneSpdFlt": _node("aZoneSpdFlt"),   # ARRAY[1..3] OF BOOL
    "aZoneTacBrk": _node("aZoneTacBrk"),   # ARRAY[1..3] OF BOOL (takometre kablo kopması)
    "aZoneAuto": _node("aZoneAuto"),       # ARRAY[1..3] OF BOOL
    "xEStopActive": _node("xEStopActive"),  # BOOL — A001 acil stop
    "xRunPermit": _node("xRunPermit"),     # BOOL — PLT_PMT çalışma izni
    "xZone2Itlk": _node("xZone2Itlk"),     # BOOL — A060 interlock
    "xAnyAlarm": _node("xAnyAlarm"),       # BOOL — herhangi bir alarm
    "uHeartbeat": _node("uHeartbeat"),     # UDINT — her saniye toggle (watchdog)
}

# --- Komut (HMI -> PLC) node identifier'ları ---
WRITE_NODES = {
    "axCmdAutoRun": _node("axCmdAutoRun"),  # ARRAY[1..3] OF BOOL — oto mod çalıştırma
    "xCmdReset": _node("xCmdReset"),        # BOOL — reset (PLT_RST ile OR'lanır)
}


# --- E_ZoneState enum eşlemesi (PLC tarafındaki sıralamaya göre) ---
# EXAMPLE_conveyor E_ZoneState; gerçek sıralamayı PLC enum tanımından doğrulayın.
ZONE_STATE_NAMES = {
    0: "IDLE",
    1: "STARTING",
    2: "RUNNING",
    3: "STOPPING",
    4: "JAM",
    5: "FAULT",
}
