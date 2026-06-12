# InoProShop (Inovance) MCP Sunucusu

Inovance InoProShop (CODESYS tabanlı) proje üretimi için MCP araç katmanı.
Proje iskeleti, donanım/EtherCAT konfigürasyonu ve PLCopen motion.

> **Durum:** STUB — araçlar listelenir, çağrılar `[STUB]` döndürür.

## Araçlar

| Araç | Açıklama |
|------|----------|
| `inoproshop_generate_project` | AM600/AC800 proje iskeleti |
| `inoproshop_configure_hardware` | CPU + I/O modül ağacı |
| `inoproshop_configure_ethercat` | EtherCAT master/slave topolojisi |
| `inoproshop_configure_motion` | PLCopen eksen yapılandırma |

## İmplementasyon Notları (sonraki adım)

- InoProShop, CODESYS tabanlıdır — `codesys_mcp` ile birçok kavram paylaşılır;
  farklar donanım katalogu, EtherCAT XML'leri ve motion kütüphanelerindedir.
- Desteklenen sürücüler `/devices/` altında: SV660N, IS620N, MD500/MD810 vb.
- EtherCAT cycle time `rules.json` motion timing hedefleriyle uyumlu olmalı (≤2ms).

## İlgili Bilgi Tabanı

- `/knowledge/inovance/inoproshop/` (Orta seviye, 10 belge)
- `/knowledge/examples/vendor-app-notes/03_inovance_am600_examples.md`
- `/devices/INOVANCE_*`
