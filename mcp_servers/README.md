# MCP Sunucuları — Endüstriyel Otomasyon Araç Katmanı

Bu klasör, agent'ın endüstriyel sistemlerle **canlı** etkileşim kurmasını sağlayan
[Model Context Protocol (MCP)](https://modelcontextprotocol.io) sunucularını içerir.
Bilgi tabanı (`/knowledge/`) agent'a *ne bildiğini* verir; bu sunucular ise
*ne yapabileceğini* — gerçek PLC'lere bağlanma, register okuma, proje üretme.

> **Durum:** Tüm sunucular şu an **stub** seviyesindedir. MCP el sıkışması (handshake)
> çalışır, araçları listeler, ancak her araç çağrısı `[STUB] henüz implemente edilmedi`
> döndürür. İmplementasyon sonraki adımda doldurulacaktır.

## Sunucular

| Sunucu | Tip | Amaç |
|--------|-----|------|
| `exa` | url (uzak) | Web araştırması — `_index.json`'da yoksa kaynak bulma (repo kökü `.mcp.json`) |
| `opcua_mcp` | stdio | OPC-UA sunucularına bağlan: browse, read/write node, subscription |
| `modbus_mcp` | stdio | Modbus TCP slave/master: holding register / coil okuma-yazma |
| `codesys_mcp` | stdio | CODESYS proje üretimi, script engine, derleme, PLCopen XML |
| `inoproshop_mcp` | stdio | Inovance InoProShop: proje, EtherCAT, motion (AM600/AC800) |
| `ixdeveloper_mcp` | stdio | Beijer iX Developer: ekran üretimi, tag binding, export |

`exa` dışındakiler bu repodaki yerel Python süreçleridir; `exa` uzaktaki bir
HTTP MCP uç noktasıdır ve `EXA_API_KEY` ister.

## Kurulum

```bash
# Sanal ortam (önerilir)
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Bağımlılıklar
pip install -r mcp_servers/requirements.txt

# Ortam değişkenleri
cp .env.template .env
# .env dosyasını aç ve gerçek anahtarları yaz (EXA_API_KEY vb.)
```

## Konfigürasyon

Sunucular repo kökündeki **`.mcp.json`** dosyasında tanımlıdır. Claude Code bu
dosyayı otomatik okur. `${EXA_API_KEY}` gibi yer tutucular `.env`'den çözülür.

## Bir Sunucuyu Tek Başına Test Etme

Her sunucu stdio üzerinden konuşur; elle test için MCP Inspector kullan:

```bash
npx @modelcontextprotocol/inspector python3 mcp_servers/opcua_mcp/server.py
```

## Yeni Araç Ekleme

1. İlgili `server.py` içinde `list_tools()` listesine `Tool(...)` ekle.
2. `call_tool()` içinde araç adını ele al, stub yerine gerçek mantığı yaz.
3. Bağımlılık gerekiyorsa `requirements.txt`'e ekle.
4. Sunucunun kendi `README.md`'sini güncelle.

## Güvenlik Notu

- `.env` **asla** commit edilmez (`.gitignore`'da). Sadece `.env.template` izlenir.
- Modbus/OPC-UA bağlantıları üretim ağına dokunabilir — `rules.json`'daki
  `modbus_never_exposed_to_internet` ve `opcua_never_left_anonymous_in_production`
  kurallarına uy.
