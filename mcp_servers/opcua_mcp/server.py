#!/usr/bin/env python3
"""OPC-UA MCP Sunucusu

Agent'ın OPC-UA sunucularıyla canlı etkileşim kurmasını sağlar:
adres uzayını gezme (browse), node okuma/yazma ve subscription.

Bağlantı modeli: `opcua_connect` ile kurulan oturum, stdio süreç ömrü boyunca
modül düzeyinde kalıcı tutulur; sonraki araçlar aynı oturumu kullanır.
Subscription istek/yanıt modeline uyarlanmıştır: bir toplama penceresi
(duration_ms) boyunca data-change örnekleri biriktirilip topluca döndürülür.

Çalıştırma:  python3 mcp_servers/opcua_mcp/server.py
Test:        npx @modelcontextprotocol/inspector python3 mcp_servers/opcua_mcp/server.py
Bağımlılık:  asyncua>=1.0.0  (bkz. ../requirements.txt)
"""

import asyncio
import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

try:
    from asyncua import Client, ua
except ImportError:  # asyncua kurulu değilse araç çağrısında anlamlı hata ver
    Client = None
    ua = None

SERVER_NAME = "opcua-mcp"
server = Server(SERVER_NAME)

# Modül düzeyi oturum durumu — stdio süreç ömrü boyunca kalıcıdır.
_state: dict = {"client": None, "endpoint": None}


# --------------------------------------------------------------------------- #
# Yardımcılar
# --------------------------------------------------------------------------- #
def _variant_types() -> dict:
    """data_type adı -> ua.VariantType eşlemesi."""
    return {
        "Boolean": ua.VariantType.Boolean,
        "SByte": ua.VariantType.SByte,
        "Byte": ua.VariantType.Byte,
        "Int16": ua.VariantType.Int16,
        "UInt16": ua.VariantType.UInt16,
        "Int32": ua.VariantType.Int32,
        "UInt32": ua.VariantType.UInt32,
        "Int64": ua.VariantType.Int64,
        "UInt64": ua.VariantType.UInt64,
        "Float": ua.VariantType.Float,
        "Double": ua.VariantType.Double,
        "String": ua.VariantType.String,
    }


def _coerce(value, vtype):
    """Python değerini hedef VariantType'a uygun tipe dönüştürür."""
    int_types = {
        ua.VariantType.SByte, ua.VariantType.Byte,
        ua.VariantType.Int16, ua.VariantType.UInt16,
        ua.VariantType.Int32, ua.VariantType.UInt32,
        ua.VariantType.Int64, ua.VariantType.UInt64,
    }
    if vtype in int_types:
        return int(value)
    if vtype in (ua.VariantType.Float, ua.VariantType.Double):
        return float(value)
    if vtype == ua.VariantType.Boolean:
        if isinstance(value, str):
            return value.strip().lower() in ("1", "true", "yes", "on", "evet")
        return bool(value)
    if vtype == ua.VariantType.String:
        return str(value)
    return value


def _jsonable(value):
    """OPC-UA değerini JSON-serileştirilebilir hale getirir."""
    if isinstance(value, (bool, int, float, str)) or value is None:
        return value
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return str(value)


async def _ensure_connected() -> "Client":
    """Aktif bir oturum döndürür; yoksa anlamlı hata fırlatır."""
    client = _state["client"]
    if client is None:
        raise RuntimeError("Oturum yok. Önce 'opcua_connect' aracını çağır.")
    return client


# --------------------------------------------------------------------------- #
# Araç implementasyonları
# --------------------------------------------------------------------------- #
async def _do_connect(args: dict) -> dict:
    if Client is None:
        raise RuntimeError(
            "asyncua kurulu değil. Kurulum: "
            "pip install -r mcp_servers/requirements.txt"
        )
    endpoint = args["endpoint"]
    username = args.get("username")
    password = args.get("password")
    security = args.get("security_policy")

    # Varsa eski oturumu kapat.
    old = _state["client"]
    if old is not None:
        try:
            await old.disconnect()
        except Exception:
            pass
        _state.update(client=None, endpoint=None)

    client = Client(url=endpoint)
    if username:
        client.set_user(username)
    if password:
        client.set_password(password)
    # security_policy "None"/boş ise güvenliksiz bağlanılır. Gerçek politika +
    # sertifika gerektiren senaryolar bu sürümde kapsam dışıdır (bkz. README).
    if security and security not in ("None", "none"):
        raise RuntimeError(
            f"security_policy='{security}' bu sürümde desteklenmiyor "
            "(sertifika/PKI gerektirir). Sadece 'None' destekleniyor."
        )

    await client.connect()
    _state.update(client=client, endpoint=endpoint)

    try:
        # ns=0;i=2259 = Server_ServerStatus_State
        state = int(await client.get_node("ns=0;i=2259").read_value())
    except Exception:
        state = None
    return {"connected": True, "endpoint": endpoint, "server_state": state}


async def _do_disconnect(args: dict) -> dict:
    client = _state["client"]
    if client is None:
        return {"disconnected": True, "note": "Zaten bağlı değildi."}
    endpoint = _state["endpoint"]
    try:
        await client.disconnect()
    finally:
        _state.update(client=None, endpoint=None)
    return {"disconnected": True, "endpoint": endpoint}


async def _browse(args: dict) -> dict:
    client = await _ensure_connected()
    node_id = args.get("node_id")
    parent = client.get_node(node_id) if node_id else client.nodes.objects

    children = await parent.get_children()
    items = []
    for child in children:
        try:
            bn = await child.read_browse_name()
            nclass = await child.read_node_class()
            items.append(
                {
                    "node_id": child.nodeid.to_string(),
                    "browse_name": bn.Name,
                    "node_class": nclass.name,
                }
            )
        except Exception as exc:
            items.append({"node_id": child.nodeid.to_string(), "error": str(exc)})

    return {
        "parent": parent.nodeid.to_string(),
        "count": len(items),
        "children": items,
    }


async def _read(args: dict) -> dict:
    client = await _ensure_connected()
    node_ids = args["node_ids"]
    results = []
    for nid in node_ids:
        node = client.get_node(nid)
        try:
            dv = await node.read_data_value()
            results.append(
                {
                    "node_id": nid,
                    "value": _jsonable(dv.Value.Value),
                    "type": dv.Value.VariantType.name,
                    "status": "Good" if dv.StatusCode.is_good() else str(dv.StatusCode),
                }
            )
        except Exception as exc:
            results.append({"node_id": nid, "error": str(exc)})
    return {"count": len(results), "values": results}


async def _write(args: dict) -> dict:
    client = await _ensure_connected()
    node = client.get_node(args["node_id"])
    data_type = args.get("data_type")

    if data_type:
        vtype = _variant_types().get(data_type)
        if vtype is None:
            raise RuntimeError(f"Bilinmeyen data_type: {data_type}")
    else:
        # Mevcut değerin tipini oku, aynı tiple yaz.
        current = await node.read_data_value()
        vtype = current.Value.VariantType

    value = _coerce(args["value"], vtype)
    await node.write_value(ua.DataValue(ua.Variant(value, vtype)))
    return {
        "node_id": args["node_id"],
        "written": _jsonable(value),
        "type": vtype.name,
    }


async def _subscribe(args: dict) -> dict:
    client = await _ensure_connected()
    node_ids = args["node_ids"]
    interval = int(args.get("interval_ms", 500))
    duration = int(args.get("duration_ms", 2000))

    collected: list = []

    class _Handler:
        def datachange_notification(self, node, val, data):
            collected.append(
                {"node_id": node.nodeid.to_string(), "value": _jsonable(val)}
            )

    sub = await client.create_subscription(interval, _Handler())
    handles = []
    try:
        for nid in node_ids:
            handles.append(await sub.subscribe_data_change(client.get_node(nid)))
        await asyncio.sleep(duration / 1000)
    finally:
        try:
            await sub.delete()
        except Exception:
            pass

    return {
        "interval_ms": interval,
        "duration_ms": duration,
        "sample_count": len(collected),
        "samples": collected,
    }


# Araç adı -> implementasyon
_HANDLERS = {
    "opcua_connect": _do_connect,
    "opcua_disconnect": _do_disconnect,
    "opcua_browse": _browse,
    "opcua_read": _read,
    "opcua_write": _write,
    "opcua_subscribe": _subscribe,
}


# --------------------------------------------------------------------------- #
# MCP arayüzü
# --------------------------------------------------------------------------- #
@server.list_tools()
async def list_tools() -> list[Tool]:
    """Bu sunucunun sunduğu araçları bildirir."""
    return [
        Tool(
            name="opcua_connect",
            description="Bir OPC-UA sunucusuna bağlan (endpoint URL, opsiyonel kimlik). "
            "Oturum sonraki çağrılar için kalıcı tutulur.",
            inputSchema={
                "type": "object",
                "properties": {
                    "endpoint": {
                        "type": "string",
                        "description": "OPC-UA endpoint, örn. opc.tcp://192.168.1.10:4840",
                    },
                    "username": {"type": "string", "description": "Kullanıcı adı (opsiyonel)"},
                    "password": {"type": "string", "description": "Parola (opsiyonel)"},
                    "security_policy": {
                        "type": "string",
                        "description": "Şimdilik sadece 'None'. PKI/sertifika kapsam dışı.",
                    },
                },
                "required": ["endpoint"],
            },
        ),
        Tool(
            name="opcua_disconnect",
            description="Aktif OPC-UA oturumunu kapat.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="opcua_browse",
            description="Bir node altındaki adres uzayını gez (browse).",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_id": {
                        "type": "string",
                        "description": "Başlangıç node, örn. ns=2;s=Machine. Boşsa Objects.",
                    }
                },
            },
        ),
        Tool(
            name="opcua_read",
            description="Bir veya birden fazla node'un değerini oku.",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Okunacak NodeId listesi",
                    }
                },
                "required": ["node_ids"],
            },
        ),
        Tool(
            name="opcua_write",
            description="Bir node'a değer yaz. data_type verilmezse mevcut tip kullanılır. "
            "(Üretimde tek-yazar kuralına dikkat.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_id": {"type": "string", "description": "Yazılacak NodeId"},
                    "value": {"description": "Yazılacak değer"},
                    "data_type": {
                        "type": "string",
                        "description": "örn. Boolean, Int16, Int32, Float, Double, String",
                    },
                },
                "required": ["node_id", "value"],
            },
        ),
        Tool(
            name="opcua_subscribe",
            description="Bir node grubuna data-change subscription kur, bir toplama "
            "penceresi boyunca değişiklikleri biriktirip döndür.",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "İzlenecek NodeId listesi",
                    },
                    "interval_ms": {
                        "type": "integer",
                        "description": "Yayın aralığı (ms), varsayılan 500",
                    },
                    "duration_ms": {
                        "type": "integer",
                        "description": "Toplama penceresi (ms), varsayılan 2000",
                    },
                },
                "required": ["node_ids"],
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
        except Exception as exc:  # sunucu/ağ hataları araç sonucu olarak döner
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
