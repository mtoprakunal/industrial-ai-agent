#!/usr/bin/env python3
"""Modbus TCP MCP Sunucusu — STUB

Agent'ın Modbus TCP cihazlarıyla canlı etkileşim kurmasını sağlar:
holding/input register ve coil/discrete-input okuma-yazma.

Durum: STUB. MCP el sıkışması ve araç listeleme çalışır; her araç çağrısı
"[STUB] henüz implemente edilmedi" döndürür. Gerçek mantık (pymodbus ile)
sonraki adımda doldurulacaktır.

Çalıştırma:  python3 mcp_servers/modbus_mcp/server.py
Test:        npx @modelcontextprotocol/inspector python3 mcp_servers/modbus_mcp/server.py
"""

import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

SERVER_NAME = "modbus-mcp"
server = Server(SERVER_NAME)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Bu sunucunun sunduğu araçları bildirir."""
    return [
        Tool(
            name="modbus_connect",
            description="Bir Modbus TCP cihazına bağlan (host, port, unit/slave id).",
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
    """Araç çağrılarını ele alır. STUB: henüz gerçek mantık yok."""
    return [
        TextContent(
            type="text",
            text=(
                f"[STUB] '{name}' aracı henüz implemente edilmedi.\n"
                f"Alınan argümanlar: {arguments}\n"
                f"Sunucu: {SERVER_NAME}. Gerçek Modbus mantığı (pymodbus) sonraki adımda eklenecek."
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
