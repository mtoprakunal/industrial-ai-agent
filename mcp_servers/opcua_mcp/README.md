# OPC-UA MCP Sunucusu

OPC-UA sunucularıyla canlı etkileşim için MCP araç katmanı. Agent'ın bir PLC'nin
adres uzayını gezmesini, node okuyup yazmasını ve subscription kurmasını sağlar.

> **Durum:** İMPLEMENTE EDİLDİ — `asyncua` (async) ile gerçek browse/read/write/subscribe.
> `asyncua` kurulu değilse araç çağrıları anlamlı bir kurulum hatası döndürür.

## Araçlar

| Araç | Açıklama |
|------|----------|
| `opcua_connect` | Endpoint'e bağlan (opsiyonel kullanıcı/parola); oturum kalıcı |
| `opcua_disconnect` | Aktif oturumu kapat |
| `opcua_browse` | Adres uzayını gez (boş node_id → Objects) |
| `opcua_read` | Bir/çok node değer + tip + status oku |
| `opcua_write` | Node'a değer yaz (data_type verilmezse mevcut tip kullanılır) |
| `opcua_subscribe` | Toplama penceresi boyunca data-change örnekleri biriktir |

## Bağlantı Modeli

`opcua_connect` ile kurulan oturum, stdio süreç ömrü boyunca modül düzeyinde
kalıcı tutulur — sonraki araçlar aynı oturumu kullanır. Tüm sonuçlar JSON olarak
döner; sunucu/ağ hataları `{"error": ...}` biçiminde gelir.

**Subscription uyarlaması:** MCP istek/yanıt modeline uygun olarak `opcua_subscribe`
bir subscription kurar, `duration_ms` (varsayılan 2000) penceresi boyunca
data-change bildirimlerini biriktirir ve topluca döndürür. İlk değer de örnek
olarak gelir. Sürekli akış (streaming) gerekiyorsa pencere tekrar tekrar çağrılır.

## Bağımlılık

`asyncua>=1.0.0` (bkz. `../requirements.txt`). Test edilen sürüm: asyncua 2.0.

## Güvenlik Notu (önemli)

- Bu sürüm yalnızca `security_policy: None` (güvenliksiz) ve opsiyonel
  kullanıcı/parola destekler. **Üretimde** PKI/sertifika tabanlı
  `Basic256Sha256` + `SignAndEncrypt` zorunludur ve anonim bağlantı bırakılmaz
  (`rules.json` → `opcua_never_left_anonymous_in_production`). Sertifika tabanlı
  güvenlik sonraki iterasyonda eklenecek.
- Yazma işlemlerinde **tek-yazar** ilkesine uy; NodeId'ler "frozen" kabul edilir.

## Test

```bash
# Fonksiyonel duman testi (kendi asyncua simülatör sunucusunu başlatır)
.venv\Scripts\python.exe mcp_servers\opcua_mcp\_smoke_test.py

# MCP stdio katmanı
npx @modelcontextprotocol/inspector python3 mcp_servers/opcua_mcp/server.py
```

`_smoke_test.py` connect → browse → read → write → subscribe → disconnect
zincirini doğrular (tüm değer kontrolleri geçer, exit 0).

## İlgili Bilgi Tabanı

- `/knowledge/protocols/opc-ua/` (Uzman seviye, 6 belge)
- `/knowledge/codesys/networking/01_opcua_server.md`
