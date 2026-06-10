# Agent Kullanım Kılavuzu

## Proje Üretimi

1. `/projects/{proje_adi}/project_spec.json` oluştur
2. Agent'a şunu söyle:
   > "Bu spec için eksiksiz bir CODESYS projesi üret."
3. Agent bilgi tabanını okur, gerekirse araştırır, projeyi üretir.

## Bilgi Tabanı Durumunu Görme

```bash
python scripts/knowledge_status.py
```

## Yeni Bilgi Ekleme

İnteraktif:

```bash
python scripts/add_knowledge.py
```

Non-interaktif (scriptlenebilir):

```bash
python scripts/add_knowledge.py \
    --konu "OPC-UA Alarmları" --kategori protocols --alt opc-ua \
    --dosya 07_alarms.md --seviye Temel
```

Belgeyi oluşturur **ve `_index.json`'u otomatik günceller** (konu eklenir,
`last_updated` bugüne çekilir). `_graph.json` bağlantıları ilişki yorumu
gerektirdiği için elle eklenir — script bunu hatırlatır.

> Not: `_index.json` her eklemede `json` ile yeniden yazılır (2 boşluk girinti,
> Türkçe karakterler korunur). İlk çalıştırmada dosya tek seferlik biçim
> normalizasyonundan geçebilir; içerik aynı kalır.

## Testler

```bash
python tests/run_tests.py        # bilgi tabanı + kural bütünlük testleri
```

Yeni bilgi eklediğinde çalıştır — `_index.json` ile disk uyumsuzluğunu yakalar.
Agent davranış senaryoları için bkz. `tests/scenarios/`.

## Agent'a Soru Sorma

Herhangi bir otomasyon sorusunu sor:
- "CODESYS'te OPC-UA sunucusu nasıl kurulur?"
- "Bu proje için OPC-UA mı yoksa Modbus TCP mi daha uygun?"
- "Bu ST kodunda neden watchdog hatası alıyorum?"
- "3 bölgeli konveyör için task yapısı nasıl olmalı?"

## Bilgi Tabanına Katkı

Her öğrenilen şeyi ekle. Agent araştırma yaptıktan sonra
"Bunu bilgi tabanına ekleyeyim mi?" diye soracak.
"Evet" dersen `/knowledge/` altına ilgili formatta kaydeder.
