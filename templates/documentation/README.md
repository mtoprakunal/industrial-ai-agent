# Dokümantasyon Şablonları

Her üretilen CODESYS projesi için standart dokümantasyon şablonları.
Yeni bir projede bu dosyaları proje klasörüne kopyalayıp `[doldurulacak]`
alanlarını doldurun.

## Şablonlar

| Dosya | Açıklama |
|-------|----------|
| `project_report_template.md` | Proje tasarım raporu — özet, gereksinim analizi, protokol seçim gerekçesi, IO/task/yazılım mimarisi, haberleşme, HMI, alarm, güvenlik, test ve referanslar. |
| `io_list_template.csv` | I/O sinyal listesi — `Tag,Adres,Tip,Yon,Task,Aciklama,Olcek_Not` sütunları, örnek satırlar ve sütun açıklamaları (ASCII). |
| `alarm_list_template.csv` | Alarm listesi — `Alarm_ID,Tag,Seviye,Sebep,Etki,Operator_Aksiyonu` sütunları, örnek satırlar (ASCII). |
| `network_diagram_template.md` | Ağ topolojisi — ASCII diyagram, VLAN/segment, IP plan, port/protokol tabloları ve IEC 62443 zone/conduit güvenlik notları. |

## Notlar
- CSV dosyalarında Türkçe karakter (ı, ş, ğ) kullanılmaz; örnek proje dosyalarıyla uyumlu olması için ASCII kullanılır.
- CSV başlıkları `projects/EXAMPLE_conveyor/` altındaki gerçek dosyalarla birebir aynıdır.
