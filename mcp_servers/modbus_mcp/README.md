# Modbus TCP MCP Sunucusu

Modbus TCP cihazlarıyla canlı etkileşim için MCP araç katmanı. Holding/input
register ve coil/discrete-input okuma-yazma.

> **Durum:** STUB — araçlar listelenir, çağrılar `[STUB]` döndürür.

## Araçlar

| Araç | FC | Açıklama |
|------|----|----------|
| `modbus_connect` | — | TCP cihaza bağlan (host/port/unit_id) |
| `modbus_read_holding_registers` | FC03 | Holding register oku |
| `modbus_read_coils` | FC01/02 | Coil / discrete input oku |
| `modbus_write_register` | FC06/16 | Register yaz (tek/çoklu) |
| `modbus_write_coil` | FC05/15 | Coil yaz (tek/çoklu) |

## Bağımlılık

`pymodbus>=3.0.0` (bkz. `../requirements.txt`).

## İmplementasyon Notları (sonraki adım)

- `pymodbus.client.AsyncModbusTcpClient` kullan.
- **Word-order / endianness** en sık hata kaynağı: 32-bit değerlerde byte/word
  sırasını cihaza göre yapılandır (`/knowledge/protocols/modbus-tcp/02_register_model.md`).
- Adresleme: protokol 0-tabanlı, dokümanlar sık sık 1-tabanlı (40001…) gösterir — çevir.
- Güvenlik: Modbus internete açılmaz (`rules.json` → `modbus_never_exposed_to_internet`).

## İlgili Bilgi Tabanı

- `/knowledge/protocols/modbus-tcp/` (Uzman seviye, 5 belge)
- `/knowledge/codesys/networking/02_modbus_slave.md`
