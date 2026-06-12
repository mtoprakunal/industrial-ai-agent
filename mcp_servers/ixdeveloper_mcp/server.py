#!/usr/bin/env python3
"""iX Developer (Beijer) MCP Sunucusu — STUB

Agent'ın Beijer iX Developer HMI projeleri üretmesini sağlar:
ekran üretimi, CODESYS tag binding, proje export.

Durum: STUB. MCP el sıkışması ve araç listeleme çalışır; her araç çağrısı
"[STUB] henüz implemente edilmedi" döndürür. Gerçek mantık sonraki adımda
doldurulacaktır.

Çalıştırma:  python3 mcp_servers/ixdeveloper_mcp/server.py
Test:        npx @modelcontextprotocol/inspector python3 mcp_servers/ixdeveloper_mcp/server.py
"""

import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

SERVER_NAME = "ixdeveloper-mcp"
server = Server(SERVER_NAME)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Bu sunucunun sunduğu araçları bildirir."""
    return [
        Tool(
            name="ix_generate_screen",
            description="Bir HMI ekranı üret (layout, nesneler, kritik sinyaller + alarm alanı).",
            inputSchema={
                "type": "object",
                "properties": {
                    "screen_name": {"type": "string", "description": "Ekran adı, örn. Overview"},
                    "signals": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Ekranda gösterilecek tag/sinyal listesi",
                    },
                    "target_panel": {
                        "type": "string",
                        "description": "Hedef panel, örn. X2 control 7, X2 pro 15, BoX2 A12",
                    },
                },
                "required": ["screen_name"],
            },
        ),
        Tool(
            name="ix_bind_tags",
            description="HMI tag'lerini CODESYS/OPC-UA controller tag'lerine bağla.",
            inputSchema={
                "type": "object",
                "properties": {
                    "controller": {
                        "type": "string",
                        "description": "Bağlanılacak controller, örn. CODESYS OPC-UA, Modbus TCP",
                    },
                    "tag_map": {
                        "type": "object",
                        "description": "HMI tag -> controller adres/node eşlemesi",
                    },
                },
                "required": ["controller"],
            },
        ),
        Tool(
            name="ix_configure_alarms",
            description="Alarm listesi yapılandır (ack'li, seviyeli) — alarm_list.csv'den.",
            inputSchema={
                "type": "object",
                "properties": {
                    "alarm_csv_path": {"type": "string", "description": "alarm_list.csv yolu"}
                },
                "required": ["alarm_csv_path"],
            },
        ),
        Tool(
            name="ix_export_project",
            description="iX Developer projesini paketle/export et (panele yüklenebilir).",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "description": "iX proje yolu"},
                    "output_path": {"type": "string", "description": "Export hedefi"},
                },
                "required": ["project_path"],
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
                f"Sunucu: {SERVER_NAME}. Gerçek iX Developer üretim mantığı sonraki adımda eklenecek."
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
