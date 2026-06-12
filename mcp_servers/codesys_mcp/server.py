#!/usr/bin/env python3
"""CODESYS MCP Sunucusu — STUB

Agent'ın CODESYS projeleri üretmesini ve script engine ile otomasyon
yapmasını sağlar: proje iskeleti, POU listeleme, PLCopen XML üretimi, derleme.

Durum: STUB. MCP el sıkışması ve araç listeleme çalışır; her araç çağrısı
"[STUB] henüz implemente edilmedi" döndürür. Gerçek mantık (CODESYS script
engine / PLCopen XML üreteci) sonraki adımda doldurulacaktır.

Çalıştırma:  python3 mcp_servers/codesys_mcp/server.py
Test:        npx @modelcontextprotocol/inspector python3 mcp_servers/codesys_mcp/server.py
"""

import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

SERVER_NAME = "codesys-mcp"
server = Server(SERVER_NAME)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Bu sunucunun sunduğu araçları bildirir."""
    return [
        Tool(
            name="codesys_generate_project",
            description="Bir spec'ten CODESYS proje iskeleti üret (task yapısı, GVL, FB hiyerarşisi).",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_path": {
                        "type": "string",
                        "description": "project_spec.json yolu, örn. projects/EXAMPLE_conveyor/project_spec.json",
                    },
                    "output_format": {
                        "type": "string",
                        "description": "st_source | plcopen_xml | script_engine",
                    },
                },
                "required": ["spec_path"],
            },
        ),
        Tool(
            name="codesys_list_pous",
            description="Bir proje/klasördeki POU'ları (Program, FB, Function) listele.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "description": "Proje veya program klasörü yolu"}
                },
                "required": ["project_path"],
            },
        ),
        Tool(
            name="codesys_generate_plcopen_xml",
            description="ST kaynağından veya spec'ten PLCopen XML üret (import edilebilir).",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_path": {"type": "string", "description": "ST kaynak dosyası veya klasörü"},
                    "output_path": {"type": "string", "description": "Üretilecek .xml yolu"},
                },
                "required": ["source_path"],
            },
        ),
        Tool(
            name="codesys_run_script",
            description="CODESYS script engine (IronPython) komutu çalıştır — proje otomasyonu.",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {"type": "string", "description": "Çalıştırılacak script engine komutu/dosyası"}
                },
                "required": ["script"],
            },
        ),
        Tool(
            name="codesys_compile_check",
            description="Üretilen kodu sözdizimi/derleme açısından doğrula (adres çakışması, tip hatası).",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "description": "Derlenecek proje yolu"}
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
                f"Sunucu: {SERVER_NAME}. Gerçek CODESYS üretim mantığı sonraki adımda eklenecek."
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
