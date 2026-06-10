"""
opcua_client.py — asyncua.sync tabanlı OPC-UA istemci (Tkinter için).

Tkinter'ın kendi event döngüsü vardır ve asyncio ile doğrudan birleşmez.
Bu yüzden knowledge dokümanındaki (01_opcua_clients_python §9) **asyncua.sync +
ayrı thread** desenini kullanırız:

- OPC-UA okuma/yazma ayrı bir daemon thread içinde `ThreadLoop` ile yürür
  (asyncua.sync altta tek bir asyncio loop döndürür; ThreadLoop zorunludur).
- Worker thread periyodik olarak (POLL_INTERVAL_S) tüm node'ları TEK Read
  servisiyle (read_values) okur — N round-trip yerine 1.
- Sonuçlar thread-safe bir dict + Lock ile saklanır; Tkinter tarafı after()
  ile bu snapshot'ı okuyup GUI'yi günceller (GUI thread'inde IO YAPILMAZ).
- Komutlar (write) thread-safe bir komut kuyruğuna konur; worker thread işler.

Bu desen polling tabanlıdır (subscription değil); Tkinter "hafif/bağımsız"
hedefine uygundur ve asyncio bilgisi gerektirmez.
"""

from __future__ import annotations

import logging
import queue
import threading
import time
from datetime import datetime, timezone

from asyncua.sync import Client, ThreadLoop
from asyncua import ua

import config

_logger = logging.getLogger("opcua_client")


class OpcUaConveyorClient:
    """Arka plan thread'inde çalışan senkron OPC-UA istemcisi."""

    def __init__(self) -> None:
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

        self._lock = threading.Lock()
        self._snapshot: dict[str, object] = {}
        self._connected = False
        self._error: str | None = None

        self._last_heartbeat: int | None = None
        self._last_heartbeat_ts: datetime | None = None

        # Yazma komutları: ("auto", zone, value) | ("reset", None, value)
        self._cmd_queue: "queue.Queue[tuple[str, int | None, bool]]" = queue.Queue()

    # --- Yaşam döngüsü ---

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)

    # --- GUI tarafına açık (thread-safe) erişim ---

    def get_snapshot(self) -> dict[str, object]:
        with self._lock:
            return dict(self._snapshot)

    @property
    def connected(self) -> bool:
        with self._lock:
            return self._connected

    @property
    def error(self) -> str | None:
        with self._lock:
            return self._error

    def heartbeat_stale(self) -> bool:
        with self._lock:
            ts = self._last_heartbeat_ts
        if ts is None:
            return True
        age_ms = (datetime.now(timezone.utc) - ts).total_seconds() * 1000
        return age_ms > config.HEARTBEAT_TIMEOUT_MS

    def command_auto_run(self, zone_no: int, value: bool) -> None:
        self._cmd_queue.put(("auto", zone_no, value))

    def command_reset(self) -> None:
        self._cmd_queue.put(("reset", None, True))

    # --- Arka plan thread ---

    def _run(self) -> None:
        """Bağlan, kopunca yeniden dene (dış döngü reconnect pattern'i)."""
        while not self._stop.is_set():
            try:
                self._session_loop()
            except Exception as exc:  # noqa: BLE001
                _logger.error("OPC-UA hatası: %s — 5 sn sonra yeniden denenecek", exc)
                with self._lock:
                    self._connected = False
                    self._error = str(exc)
                self._stop.wait(5.0)

    def _session_loop(self) -> None:
        with ThreadLoop() as tloop:
            client = Client(url=config.OPCUA_ENDPOINT, tloop=tloop, timeout=10)
            if config.USE_SECURITY:
                from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

                client.set_security(
                    SecurityPolicyBasic256Sha256,
                    certificate="client_cert.der",
                    private_key="client_key.pem",
                    server_certificate="server_cert.der",
                )
                if config.OPCUA_USERNAME:
                    client.set_user(config.OPCUA_USERNAME)
                    client.set_password(config.OPCUA_PASSWORD or "")

            with client:
                ns = client.get_namespace_index(config.CODESYS_NS_URI)
                _logger.info("Bağlandı: %s (ns=%s)", config.OPCUA_ENDPOINT, ns)

                read_names = list(config.READ_NODES.keys())
                read_nodes = [
                    client.get_node(f"ns={ns};s={config.READ_NODES[n]}")
                    for n in read_names
                ]

                with self._lock:
                    self._connected = True
                    self._error = None

                while not self._stop.is_set():
                    # 1) Bekleyen komutları yaz
                    self._drain_commands(client, ns)

                    # 2) Toplu okuma (tek Read servisi)
                    values = client.read_values(read_nodes)
                    snap = dict(zip(read_names, values))

                    with self._lock:
                        self._snapshot = snap
                        hb = snap.get("uHeartbeat")
                        if isinstance(hb, int) and hb != self._last_heartbeat:
                            self._last_heartbeat = hb
                            self._last_heartbeat_ts = datetime.now(timezone.utc)

                    time.sleep(config.POLL_INTERVAL_S)

    def _drain_commands(self, client: Client, ns: int) -> None:
        while True:
            try:
                kind, zone, value = self._cmd_queue.get_nowait()
            except queue.Empty:
                return
            try:
                if kind == "auto" and zone is not None:
                    identifier = config.WRITE_NODES["axCmdAutoRun"]
                    node = client.get_node(f"ns={ns};s={identifier}[{zone}]")
                    node.write_value(ua.DataValue(ua.Variant(bool(value), ua.VariantType.Boolean)))
                    _logger.info("axCmdAutoRun[%d] <- %s", zone, value)
                elif kind == "reset":
                    node = client.get_node(f"ns={ns};s={config.WRITE_NODES['xCmdReset']}")
                    node.write_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))
                    _logger.info("xCmdReset <- True")
            except Exception as exc:  # noqa: BLE001
                _logger.error("Komut yazma hatası (%s): %s", kind, exc)
