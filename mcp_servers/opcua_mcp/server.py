#!/usr/bin/env python3
"""OPC-UA MCP Sunucusu — STUB

Agent'ın OPC-UA sunucularıyla canlı etkileşim kurmasını sağlar:
adres uzayını gezme (browse), node okuma/yazma ve subscription.

Durum: STUB. MCP el sıkışması ve araç listeleme çalışır; her araç çağrısı
"[STUB] henüz implemente edilmedi" döndürür. Gerçek mantık (asyncua ile)
sonraki adımda doldurulacaktır.

Çalıştırma:  python3 mcp_servers/opcua_mcp/server.py
Test:        npx @modelcontextprotocol/inspector python3 mcp_servers/opcua_mcp/server.py
"""

import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

SERVER_NAME = "opcua-mcp"
server = Server(SERVER_NAME)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Bu sunucunun sunduğu araçları bildirir."""
    return [
        Tool(
            name="opcua_connect",
            description="Bir OPC-UA sunucusuna bağlan (endpoint URL, opsiyonel güvenlik/kimlik).",
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
                        "description": "örn. None, Basic256Sha256",
                    },
                },
                "required": ["endpoint"],
            },
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
            description="Bir node'a değer yaz. (Üretimde tek-yazar kuralına dikkat.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_id": {"type": "string", "description": "Yazılacak NodeId"},
                    "value": {"description": "Yazılacak değer"},
                    "data_type": {
                        "type": "string",
                        "description": "örn. Boolean, Int16, Float, String",
                    },
                },
                "required": ["node_id", "value"],
            },
        ),
        Tool(
            name="opcua_subscribe",
            description="Bir node grubuna data-change subscription kur ve değişiklikleri izle.",
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
                        "description": "Yayın aralığı (ms), örn. 500",
                    },
                },
                "required": ["node_ids"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Araç çağrılarını ele alır. STUB: henüz gerçek mantık yok."""
    return [
        TextContent(
            type="text",
            text=(
                f"[STUB] '{name}' aracı henüz implemente edilmedi.\n"
                f"Alınan argümanlar: {arguments}\n"
                f"Sunucu: {SERVER_NAME}. Gerçek OPC-UA mantığı (asyncua) sonraki adımda eklenecek."
            ),
        )
    ]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
