# Modbus TCP MCP Sunucusu

Modbus TCP cihazlarıyla canlı etkileşim için MCP araç katmanı. Holding/input
register ve coil/discrete-input okuma-yazma.

> **Durum:** İMPLEMENTE EDİLDİ — `pymodbus` (async) ile gerçek okuma/yazma.
> `pymodbus` kurulu değilse araç çağrıları anlamlı bir kurulum hatası döndürür.

## Araçlar

| Araç | FC | Açıklama |
|------|----|----------|
| `modbus_connect` | — | TCP cihaza bağlan (host/port/unit_id); bağlantı kalıcı tutulur |
| `modbus_disconnect` | — | Aktif bağlantıyı kapat |
| `modbus_read_holding_registers` | FC03 | Holding register oku |
| `modbus_read_coils` | FC01/02 | Coil / discrete input oku (`input_type`) |
| `modbus_write_register` | FC06/16 | Register yaz (tek=FC06, çoklu=FC16) |
| `modbus_write_coil` | FC05/15 | Coil yaz (tek=FC05, çoklu=FC15) |

## Bağlantı Modeli

`modbus_connect` ile kurulan bağlantı, stdio süreç ömrü boyunca modül düzeyinde
kalıcı tutulur — sonraki okuma/yazma araçları aynı bağlantıyı ve `unit_id`'yi
kullanır. Bağlantı kopmuşsa okuma/yazma öncesi otomatik yeniden bağlanma denenir.
Tüm sonuçlar JSON olarak döner; cihaz/ağ hataları `{"error": ...}` biçiminde gelir.

## Bağımlılık

`pymodbus>=3.0.0` (bkz. `../requirements.txt`).

> Not: pymodbus 3.x sürümleri arasında unit kimliği parametresi (`slave` /
> `device_id` / `unit`) değişebilir. Sunucu, yöntem imzasını inceleyerek doğru
> anahtarı otomatik seçer — sürüm sabitlemeye gerek yoktur.

## Bilinen Tuzaklar

- **Word-order / endianness** en sık hata kaynağı: 32-bit (REAL/DINT) değerler iki
  register'a yayılır; byte/word sırası cihaza göre değişir. Bu sunucu ham 16-bit
  register döndürür — birleştirme/ölçekleme çağıran tarafa aittir
  (`/knowledge/protocols/modbus-tcp/02_register_model.md`).
- **Adresleme:** protokol 0-tabanlı; dokümanlar sık sık 1-tabanlı (40001…) gösterir.
  Araçlara 0-tabanlı adres ver.
- **`read_coils` bit hizalama:** cihaz byte sınırına yuvarlayabilir; sunucu sonucu
  istenen `count`'a kırpar.
- **Güvenlik:** Modbus'ta kimlik doğrulama yoktur; internete açılmaz
  (`rules.json` → `modbus_never_exposed_to_internet`).

## Test

```bash
npx @modelcontextprotocol/inspector python3 mcp_servers/modbus_mcp/server.py
```

Gerçek cihaz yoksa bir Modbus TCP simülatörü (ör. `pymodbus` ile gelen
`pymodbus.server` veya ModbusPal/diagslave) `127.0.0.1:502` üzerinde çalıştırılabilir.

## İlgili Bilgi Tabanı

- `/knowledge/protocols/modbus-tcp/` (Uzman seviye, 5 belge)
- `/knowledge/codesys/networking/02_modbus_slave.md`
