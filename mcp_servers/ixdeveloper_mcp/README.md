# iX Developer (Beijer) MCP Sunucusu

Beijer iX Developer HMI projeleri üretimi için MCP araç katmanı. Ekran üretimi,
CODESYS/OPC-UA tag binding, alarm yapılandırma ve proje export.

> **Durum:** STUB — araçlar listelenir, çağrılar `[STUB]` döndürür.

## Araçlar

| Araç | Açıklama |
|------|----------|
| `ix_generate_screen` | HMI ekranı üret (kritik sinyaller + alarm) |
| `ix_bind_tags` | HMI tag → controller (CODESYS/OPC-UA/Modbus) |
| `ix_configure_alarms` | `alarm_list.csv`'den ack'li/seviyeli alarmlar |
| `ix_export_project` | Panele yüklenebilir export |

## İmplementasyon Notları (sonraki adım)

- iX Developer C# scripting destekler — ileri mantık için kullanılabilir
  (`/knowledge/hmi/ix-developer/04_scripting.md`).
- Köprü her zaman protokoldür; HMI'ya PLC mantığı gömülmez
  (`rules.json` → `hmi_design.logic_never_embedded_in_hmi`).
- Tüm kritik sinyaller, bağlantı-kopması senaryosu ve ack'li alarmlar zorunlu.
- Hedef paneller `/devices/BEIJER_*` altında (X2 control/pro, BoX2).

## İlgili Bilgi Tabanı

- `/knowledge/hmi/ix-developer/` (Uzman seviye, 4 belge)
- `/knowledge/hmi/architecture/03_alarms.md`
- `/devices/BEIJER_*`
