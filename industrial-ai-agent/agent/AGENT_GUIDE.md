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

```bash
python scripts/add_knowledge.py
```

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
