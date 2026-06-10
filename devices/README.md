# Cihaz Kütüphanesi

Endüstriyel cihazların **kaynaklı özet kayıtları**. Telifli datasheet PDF'leri veya
cihaz tanım dosyaları (GSDML/ESI/EDS/GSD) burada **saklanmaz** — bunun yerine her cihaz
için mühendislik açısından önemli özellikler, resmi kaynak/indirme linkleri ve CODESYS
entegrasyon notları tutulur. Asıl XML/PDF dosyasını resmi linkten indirirsin.

## Yapı

Her cihaz kendi klasöründe:

```
devices/{URETICI}_{MODEL}/
├── datasheet.json     → yapılandırılmış teknik veri (agent/datasheet_schema.json'a uygun)
└── wiring_notes.md    → kablolama, devreye alma ve CODESYS entegrasyon notları
```

## Yeni Cihaz Ekleme

1. `devices/{URETICI}_{MODEL}/` klasörü oluştur.
2. `datasheet.json` yaz — `devices/_template.json`'u taban al, `agent/datasheet_schema.json`'a uy.
3. `wiring_notes.md` yaz.
4. Doğrula: `python scripts/validate_datasheet.py`.

## İlkeler

- **Gerçek değer kullan, tahmin etme.** Bulunamayan alanı `null` veya `""` bırak,
  `meta.completeness`'i `partial` yap.
- **Resmi kaynağı belirt.** Her cihazda en az bir `sources` girişi (tercihen `resmi`).
- **Telifli metni kopyalama.** Özellik değerleri (sayılar, protokoller) olgudur; datasheet
  metnini birebir aktarma, kendi sözlerinle özetle.

## Cihaz Tanım Dosyası Türleri

| Fieldbus | Dosya türü |
|----------|-----------|
| PROFINET | GSDML |
| EtherCAT | ESI |
| EtherNet/IP | EDS |
| PROFIBUS | GSD |
| Modbus TCP/RTU, OPC-UA | yok (register/adres haritasıyla entegre) |

## Kayıtlı Cihazlar

Güncel liste için `devices/_index.json`.
