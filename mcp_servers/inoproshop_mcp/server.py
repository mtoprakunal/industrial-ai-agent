#!/usr/bin/env python3
"""InoProShop (Inovance) MCP Sunucusu — STUB

Agent'ın Inovance InoProShop (CODESYS tabanlı) projeleri üretmesini sağlar:
proje iskeleti, donanım/EtherCAT konfigürasyonu, PLCopen motion.

Durum: STUB. MCP el sıkışması ve araç listeleme çalışır; her araç çağrısı
"[STUB] henüz implemente edilmedi" döndürür. Gerçek mantık sonraki adımda
doldurulacaktır.

Çalıştırma:  python3 mcp_servers/inoproshop_mcp/server.py
Test:        npx @modelcontextprotocol/inspector python3 mcp_servers/inoproshop_mcp/server.py
"""

import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

SERVER_NAME = "inoproshop-mcp"
server = Server(SERVER_NAME)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Bu sunucunun sunduğu araçları bildirir."""
    return [
        Tool(
            name="inoproshop_generate_project",
            description="Inovance PLC (AM600/AC800) için InoProShop proje iskeleti üret.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_path": {"type": "string", "description": "project_spec.json yolu"},
                    "plc_model": {
                        "type": "string",
                        "description": "Hedef PLC, örn. AM600, AC801, Easy521",
                    },
                },
                "required": ["spec_path"],
            },
        ),
        Tool(
            name="inoproshop_configure_hardware",
            description="Donanım ağacını yapılandır (CPU, I/O modülleri, genişleme).",
            inputSchema={
                "type": "object",
                "properties": {
                    "plc_model": {"type": "string", "description": "PLC modeli"},
                    "modules": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "I/O modül listesi (sıralı)",
                    },
                },
                "required": ["plc_model"],
            },
        ),
        Tool(
            name="inoproshop_configure_ethercat",
            description="EtherCAT master ve slave'leri yapılandır (servo/sürücü topolojisi).",
            inputSchema={
                "type": "object",
                "properties": {
                    "slaves": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "EtherCAT slave listesi, örn. SV660N, IS620N",
                    },
                    "cycle_time_us": {
                        "type": "integer",
                        "description": "DC senkron cycle time (µs), örn. 1000",
                    },
                },
                "required": ["slaves"],
            },
        ),
        Tool(
            name="inoproshop_configure_motion",
            description="PLCopen motion ekseni yapılandır (eksen tipi, ölçekleme, limitler).",
            inputSchema={
                "type": "object",
                "properties": {
                    "axis_name": {"type": "string", "description": "Eksen adı"},
                    "drive": {"type": "string", "description": "Sürücü, örn. SV660N"},
                    "units_per_rev": {"type": "number", "description": "Tur başına mühendislik birimi"},
                },
                "required": ["axis_name", "drive"],
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
                f"Sunucu: {SERVER_NAME}. Gerçek InoProShop üretim mantığı sonraki adımda eklenecek."
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
