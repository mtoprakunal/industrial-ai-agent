#!/usr/bin/env python3
"""Modbus TCP MCP Sunucusu

Agent'ın Modbus TCP cihazlarıyla canlı etkileşim kurmasını sağlar:
holding/input register ve coil/discrete-input okuma-yazma.

Bağlantı modeli: `modbus_connect` ile kurulan bağlantı, stdio süreç ömrü
boyunca modül düzeyinde kalıcı tutulur; sonraki okuma/yazma araçları aynı
bağlantıyı kullanır. Kopma durumunda otomatik yeniden bağlanma denenir.

Çalıştırma:  python3 mcp_servers/modbus_mcp/server.py
Test:        npx @modelcontextprotocol/inspector python3 mcp_servers/modbus_mcp/server.py
Bağımlılık:  pymodbus>=3.0.0  (bkz. ../requirements.txt)
"""

import asyncio
import inspect
import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

try:
    from pymodbus.client import AsyncModbusTcpClient
except ImportError:  # pymodbus kurulu değilse araç çağrısında anlamlı hata ver
    AsyncModbusTcpClient = None

SERVER_NAME = "modbus-mcp"
server = Server(SERVER_NAME)

# Modül düzeyi bağlantı durumu — stdio süreç ömrü boyunca kalıcıdır.
_state: dict = {"client": None, "host": None, "port": None, "unit_id": 1}


# --------------------------------------------------------------------------- #
# Yardımcılar
# --------------------------------------------------------------------------- #
def _unit_kwarg(method) -> str:
    """Kurulu pymodbus sürümünün slave/device_id/unit'ten hangisini kabul
    ettiğini imzadan tespit eder (3.x sürümleri arasında değişir)."""
    try:
        params = inspect.signature(method).parameters
    except (ValueError, TypeError):
        return "slave"
    for name in ("slave", "device_id", "unit"):
        if name in params:
            return name
    return "slave"


async def _ensure_connected() -> "AsyncModbusTcpClient":
    """Aktif bir bağlantı döndürür; kopmuşsa yeniden bağlanmayı dener."""
    client = _state["client"]
    if client is None:
        raise RuntimeError("Bağlantı yok. Önce 'modbus_connect' aracını çağır.")
    if not getattr(client, "connected", False):
        await client.connect()
        if not getattr(client, "connected", False):
            raise RuntimeError(
                f"Bağlantı koptu ve yeniden kurulamadı: {_state['host']}:{_state['port']}"
            )
    return client


def _check(response) -> None:
    """Modbus yanıtını hata açısından kontrol eder, hatalıysa exception fırlatır."""
    if response is None:
        raise RuntimeError("Cihazdan yanıt alınamadı (None).")
    if hasattr(response, "isError") and response.isError():
        raise RuntimeError(f"Modbus exception yanıtı: {response}")


# --------------------------------------------------------------------------- #
# Araç implementasyonları
# --------------------------------------------------------------------------- #
async def _do_connect(args: dict) -> dict:
    if AsyncModbusTcpClient is None:
        raise RuntimeError(
            "pymodbus kurulu değil. Kurulum: "
            "pip install -r mcp_servers/requirements.txt"
        )
    host = args["host"]
    port = int(args.get("port", 502))
    unit_id = int(args.get("unit_id", 1))

    # Varsa eski bağlantıyı kapat.
    old = _state["client"]
    if old is not None:
        try:
            old.close()
        except Exception:
            pass

    client = AsyncModbusTcpClient(host, port=port)
    await client.connect()
    if not getattr(client, "connected", False):
        raise RuntimeError(f"Bağlanılamadı: {host}:{port}")

    _state.update(client=client, host=host, port=port, unit_id=unit_id)
    return {"connected": True, "host": host, "port": port, "unit_id": unit_id}


async def _do_disconnect(args: dict) -> dict:
    client = _state["client"]
    if client is None:
        return {"disconnected": True, "note": "Zaten bağlı değildi."}
    try:
        client.close()
    finally:
        host, port = _state["host"], _state["port"]
        _state.update(client=None, host=None, port=None)
    return {"disconnected": True, "host": host, "port": port}


async def _read_holding_registers(args: dict) -> dict:
    client = await _ensure_connected()
    address = int(args["address"])
    count = int(args["count"])
    kw = {_unit_kwarg(client.read_holding_registers): _state["unit_id"]}
    rr = await client.read_holding_registers(address, count=count, **kw)
    _check(rr)
    return {
        "function": "FC03 read_holding_registers",
        "address": address,
        "count": count,
        "registers": list(rr.registers),
    }


async def _read_coils(args: dict) -> dict:
    client = await _ensure_connected()
    address = int(args["address"])
    count = int(args["count"])
    input_type = args.get("input_type", "coil")

    if input_type == "discrete_input":
        method, fc = client.read_discrete_inputs, "FC02 read_discrete_inputs"
    else:
        method, fc = client.read_coils, "FC01 read_coils"

    kw = {_unit_kwarg(method): _state["unit_id"]}
    rr = await method(address, count=count, **kw)
    _check(rr)
    # rr.bits byte sınırına yuvarlanmış olabilir; istenen sayıya kırp.
    bits = [bool(b) for b in rr.bits][:count]
    return {"function": fc, "address": address, "count": count, "bits": bits}


async def _write_register(args: dict) -> dict:
    client = await _ensure_connected()
    address = int(args["address"])
    values = [int(v) for v in args["values"]]
    if not values:
        raise RuntimeError("'values' boş olamaz.")

    if len(values) == 1:
        method, fc = client.write_register, "FC06 write_register"
        kw = {_unit_kwarg(method): _state["unit_id"]}
        rr = await method(address, values[0], **kw)
    else:
        method, fc = client.write_registers, "FC16 write_registers"
        kw = {_unit_kwarg(method): _state["unit_id"]}
        rr = await method(address, values, **kw)
    _check(rr)
    return {"function": fc, "address": address, "written": values}


async def _write_coil(args: dict) -> dict:
    client = await _ensure_connected()
    address = int(args["address"])
    values = [bool(v) for v in args["values"]]
    if not values:
        raise RuntimeError("'values' boş olamaz.")

    if len(values) == 1:
        method, fc = client.write_coil, "FC05 write_coil"
        kw = {_unit_kwarg(method): _state["unit_id"]}
        rr = await method(address, values[0], **kw)
    else:
        method, fc = client.write_coils, "FC15 write_coils"
        kw = {_unit_kwarg(method): _state["unit_id"]}
        rr = await method(address, values, **kw)
    _check(rr)
    return {"function": fc, "address": address, "written": values}


# Araç adı -> (implementasyon, gerekli argümanlar)
_HANDLERS = {
    "modbus_connect": _do_connect,
    "modbus_disconnect": _do_disconnect,
    "modbus_read_holding_registers": _read_holding_registers,
    "modbus_read_coils": _read_coils,
    "modbus_write_register": _write_register,
    "modbus_write_coil": _write_coil,
}


# --------------------------------------------------------------------------- #
# MCP arayüzü
# --------------------------------------------------------------------------- #
@server.list_tools()
async def list_tools() -> list[Tool]:
    """Bu sunucunun sunduğu araçları bildirir."""
    return [
        Tool(
            name="modbus_connect",
            description="Bir Modbus TCP cihazına bağlan (host, port, unit/slave id). "
            "Bağlantı sonraki çağrılar için kalıcı tutulur.",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {"type": "string", "description": "IP veya hostname, örn. 192.168.1.20"},
                    "port": {"type": "integer", "description": "TCP port (varsayılan 502)"},
                    "unit_id": {"type": "integer", "description": "Unit/Slave ID (varsayılan 1)"},
                },
                "required": ["host"],
            },
        ),
        Tool(
            name="modbus_disconnect",
            description="Aktif Modbus TCP bağlantısını kapat.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="modbus_read_holding_registers",
            description="Holding register oku (FC03). word-order/endianness tuzaklarına dikkat.",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "integer", "description": "Başlangıç register adresi (0-tabanlı)"},
                    "count": {"type": "integer", "description": "Okunacak register sayısı"},
                },
                "required": ["address", "count"],
            },
        ),
        Tool(
            name="modbus_read_coils",
            description="Coil oku (FC01) veya discrete input (FC02).",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "integer", "description": "Başlangıç adresi (0-tabanlı)"},
                    "count": {"type": "integer", "description": "Okunacak bit sayısı"},
                    "input_type": {
                        "type": "string",
                        "description": "coil (FC01) veya discrete_input (FC02)",
                    },
                },
                "required": ["address", "count"],
            },
        ),
        Tool(
            name="modbus_write_register",
            description="Tek holding register yaz (FC06) veya çoklu (FC16).",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "integer", "description": "Yazılacak register adresi"},
                    "values": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "16-bit değer(ler). Tek eleman FC06, çoklu FC16.",
                    },
                },
                "required": ["address", "values"],
            },
        ),
        Tool(
            name="modbus_write_coil",
            description="Tek coil yaz (FC05) veya çoklu coil (FC15).",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "integer", "description": "Yazılacak coil adresi"},
                    "values": {
                        "type": "array",
                        "items": {"type": "boolean"},
                        "description": "Bool değer(ler). Tek eleman FC05, çoklu FC15.",
                    },
                },
                "required": ["address", "values"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Araç çağrılarını ilgili implementasyona yönlendirir."""
    arguments = arguments or {}
    handler = _HANDLERS.get(name)
    if handler is None:
        result = {"error": f"Bilinmeyen araç: {name}"}
    else:
        try:
            result = await handler(arguments)
        except Exception as exc:  # cihaz/ağ hataları araç sonucu olarak döner
            result = {"error": str(exc), "tool": name}

    text = json.dumps(result, ensure_ascii=False, indent=2)
    return [TextContent(type="text", text=text)]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
