# OPC-UA MCP Sunucusu

OPC-UA sunucularıyla canlı etkileşim için MCP araç katmanı. Agent'ın bir PLC'nin
adres uzayını gezmesini, node okuyup yazmasını ve subscription kurmasını sağlar.

> **Durum:** STUB — araçlar listelenir, çağrılar `[STUB]` döndürür.

## Araçlar

| Araç | Açıklama |
|------|----------|
| `opcua_connect` | Endpoint'e bağlan (güvenlik/kimlik opsiyonel) |
| `opcua_browse` | Adres uzayını gez |
| `opcua_read` | Node değer(ler)i oku |
| `opcua_write` | Node'a değer yaz |
| `opcua_subscribe` | Data-change subscription |

## Bağımlılık

`asyncua>=1.0.0` (bkz. `../requirements.txt`).

## İmplementasyon Notları (sonraki adım)

- `asyncua.Client` ile bağlantı; oturum havuzu tek bağlantıda tutulmalı.
- Güvenlik: üretimde anonim bağlantı yok (`rules.json` → `opcua_never_left_anonymous_in_production`).
- NodeId'ler "frozen" kabul edilir — yazma işlemlerinde tek-yazar ilkesini koru.

## İlgili Bilgi Tabanı

- `/knowledge/protocols/opc-ua/` (Uzman seviye, 6 belge)
- `/knowledge/codesys/networking/01_opcua_server.md`
