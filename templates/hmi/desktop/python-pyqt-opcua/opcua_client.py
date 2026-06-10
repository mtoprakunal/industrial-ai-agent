"""
opcua_client.py — asyncua tabanlı OPC-UA istemci sarmalayıcısı.

Mimari (knowledge/hmi/desktop/01_opcua_clients_python.md + 03_pyqt_patterns.md):
- asyncua tamamen async'tir; qasync sayesinde Qt event loop'u ile AYNI thread'de
  (GUI thread) await edilir. Ayrı thread / run_coroutine_threadsafe gerekmez.
- Subscription handler (datachange_notification) asyncio loop thread'inde,
  yani burada GUI thread'inde çalışır. Handler HİÇBİR ZAMAN bloklamamalıdır:
  yalnızca thread-safe bir queue'ya yazar. GUI tarafı (QTimer) queue'yu 100ms'de
  bir boşaltıp coalesce ederek UI'yi günceller.
- Namespace index ASLA sabit yazılmaz; bağlantıda URI üzerinden alınır.
- async with / disconnect ile ghost session bırakılmaz (CODESYS MaxSessions).
"""

from __future__ import annotations

import logging
import queue
from datetime import datetime, timezone

from asyncua import Client, ua

import config

_logger = logging.getLogger("opcua_client")


class _SubHandler:
    """asyncua subscription callback'i — non-blocking, thread-safe queue'ya yazar.

    datachange_notification asyncio loop thread'inde senkron çağrılır.
    Hızlı olmalı: yalnızca put_nowait yapar (bkz. 01_opcua_clients_python Hata 3).
    """

    def __init__(self, data_queue: "queue.Queue[tuple[str, object]]") -> None:
        self._q = data_queue

    def datachange_notification(self, node, val, data) -> None:  # noqa: ANN001
        try:
            self._q.put_nowait((str(node.nodeid), val))
        except queue.Full:
            pass  # Kuyruk doluysa veriyi at, loop'u engelleme

    def status_change_notification(self, status) -> None:  # noqa: ANN001
        _logger.warning("Subscription durumu değişti: %s", status)


class OpcUaConveyorClient:
    """EXAMPLE_conveyor CODESYS PLC'sine doğrudan bağlanan OPC-UA istemcisi."""

    def __init__(self) -> None:
        self._client: Client | None = None
        self._ns: int | None = None
        self._subscription = None
        self._handles: list = []
        # Subscription verisi GUI'ye buradan akar (thread-safe).
        self.data_queue: "queue.Queue[tuple[str, object]]" = queue.Queue(maxsize=10_000)
        # NodeId (ns'li) -> mantıksal isim çözümü için ters harita.
        self._nodeid_to_name: dict[str, str] = {}
        # Son heartbeat değeri + zamanı (watchdog).
        self.last_heartbeat: int | None = None
        self.last_heartbeat_ts: datetime | None = None

    @property
    def connected(self) -> bool:
        return self._client is not None and self._ns is not None

    async def connect(self) -> None:
        """Sunucuya bağlan, namespace index'i al, subscription kur."""
        client = Client(url=config.OPCUA_ENDPOINT, timeout=10)

        if config.USE_SECURITY:
            # Üretim: SignAndEncrypt + Basic256Sha256. Sertifikalar önceden
            # üretilmeli (bkz. README güvenlik notu).
            from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

            await client.set_security(
                SecurityPolicyBasic256Sha256,
                certificate="client_cert.der",
                private_key="client_key.pem",
                server_certificate="server_cert.der",
            )
            if config.OPCUA_USERNAME:
                client.set_user(config.OPCUA_USERNAME)
                client.set_password(config.OPCUA_PASSWORD or "")

        # auto_reconnect: transport düşünce secure channel + session yeniden açılır.
        await client.connect()
        self._client = client

        # Namespace index — URI'den dinamik al, ASLA sabit yazma.
        self._ns = await client.get_namespace_index(config.CODESYS_NS_URI)
        _logger.info("Bağlandı: %s (ns=%s)", config.OPCUA_ENDPOINT, self._ns)

        await self._start_subscription()

    def _full_nodeid(self, identifier: str) -> str:
        return f"ns={self._ns};s={identifier}"

    async def _start_subscription(self) -> None:
        """Tüm izleme node'larını tek subscription altında izlemeye al."""
        handler = _SubHandler(self.data_queue)
        self._subscription = await self._client.create_subscription(
            period=config.PUBLISHING_INTERVAL_MS,
            handler=handler,
        )

        nodes = []
        for name, identifier in config.READ_NODES.items():
            node = self._client.get_node(self._full_nodeid(identifier))
            nodes.append(node)
            self._nodeid_to_name[str(node.nodeid)] = name

        self._handles = await self._subscription.subscribe_data_change(nodes)
        _logger.info("Subscription aktif — %d node izleniyor.", len(nodes))

    def resolve_name(self, node_id_str: str) -> str | None:
        """Subscription'tan gelen NodeId string'ini mantıksal isme çevirir."""
        return self._nodeid_to_name.get(node_id_str)

    def update_heartbeat(self, value: int) -> None:
        """uHeartbeat değişiminde çağrılır — watchdog zaman damgasını günceller."""
        self.last_heartbeat = value
        self.last_heartbeat_ts = datetime.now(timezone.utc)

    def heartbeat_stale(self) -> bool:
        """Heartbeat son HEARTBEAT_TIMEOUT_MS içinde güncellenmediyse True."""
        if self.last_heartbeat_ts is None:
            return True
        age_ms = (datetime.now(timezone.utc) - self.last_heartbeat_ts).total_seconds() * 1000
        return age_ms > config.HEARTBEAT_TIMEOUT_MS

    # --- Komut yazma (HMI -> PLC) ---

    async def write_auto_run(self, zone_index: int, value: bool) -> None:
        """axCmdAutoRun[zone_index] yaz. zone_index 1..ZONE_COUNT (CODESYS 1-tabanlı).

        CODESYS array elemanı OPC-UA'da ayrı node ise '[i]' ile erişilir; tek array
        node ise tüm dizi okunup yazılır. Burada eleman-node yaklaşımını kullanıyoruz
        (CODESYS Symbol Configuration'da array elemanları ayrı yayınlanır).
        """
        if not self.connected:
            return
        identifier = config.WRITE_NODES["axCmdAutoRun"]
        # OPC-UA array elemanı node ID'si: ...axCmdAutoRun[1]
        node = self._client.get_node(self._full_nodeid(f"{identifier}[{zone_index}]"))
        await node.write_value(ua.DataValue(ua.Variant(bool(value), ua.VariantType.Boolean)))
        _logger.info("axCmdAutoRun[%d] <- %s", zone_index, value)

    async def write_reset(self, value: bool = True) -> None:
        """xCmdReset yaz (PLT_RST ile OR'lanır)."""
        if not self.connected:
            return
        node = self._client.get_node(self._full_nodeid(config.WRITE_NODES["xCmdReset"]))
        await node.write_value(ua.DataValue(ua.Variant(bool(value), ua.VariantType.Boolean)))
        _logger.info("xCmdReset <- %s", value)

    async def disconnect(self) -> None:
        """Subscription'ı temizle ve session'ı kapat (ghost session bırakma)."""
        try:
            if self._subscription is not None:
                if self._handles:
                    await self._subscription.unsubscribe(self._handles)
                await self._subscription.delete()
        except Exception as exc:  # noqa: BLE001
            _logger.warning("Subscription temizleme hatası: %s", exc)
        finally:
            self._subscription = None
            self._handles = []

        if self._client is not None:
            try:
                await self._client.disconnect()
            finally:
                self._client = None
                self._ns = None
        _logger.info("Bağlantı kesildi.")
