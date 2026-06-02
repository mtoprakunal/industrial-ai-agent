# Industrial Automation AI Agent

Endüstriyel otomasyon mühendisliği için geliştirilmiş, sürekli öğrenen ve gelişen bir AI agent sistemi.

## Bu Agent Ne Yapar?

- Proje gereksinimlerini anlayarak en uygun mimari ve protokol kararını verir
- CODESYS projelerini otomatik olarak üretir (task yapısı, GVL, fonksiyon blokları, ağ konfigürasyonu)
- HMI katmanını dil ve framework bağımsız olarak üretir (web veya masaüstü)
- Bilmediği konularda web araştırması yapar, öğrendiklerini bilgi tabanına ekler
- Birden fazla kaynaktan gelen bilgiyi sentezleyerek bütünleşik kararlar verir

## Sistem Mimarisi

```
industrial-ai-agent/
│
├── agent/              → Agent'ın kimliği, kuralları, davranış kılavuzları
│
├── knowledge/          → Canlı bilgi tabanı (sürekli büyür)
│   ├── protocols/      → OPC-UA, Modbus TCP, TCP Socket, MQTT
│   ├── codesys/        → CODESYS derin bilgisi
│   ├── hmi/            → HMI mimarisi ve teknolojileri
│   ├── hardware/       → Endüstriyel PC'ler ve cihazlar
│   ├── networking/     → Endüstriyel ağ mimarisi
│   ├── standards/      → IEC standartları
│   ├── applications/   → Uygulama bazlı bilgi
│   └── decisions/      → Gerçek karar örnekleri ve gerekçeleri
│
├── devices/            → Cihaz datasheet kütüphanesi
├── templates/          → CODESYS script, PLCopen XML, HMI şablonları
├── projects/           → Üretilmiş ve örnek projeler
├── scripts/            → Yardımcı araçlar
└── tests/              → Agent test senaryoları
```

## Bilgi Olgunluk Seviyeleri

Her bilgi alanı beş seviyede takip edilir:

| Seviye | Anlam |
|--------|-------|
| Stub | Başlık var, içerik henüz yok |
| Temel | Temel kavramlar mevcut |
| Orta | Pratik örnekler ve konfigürasyonlar eklendi |
| İleri | Derin bilgi, tuzaklar, edge case'ler |
| Uzman | Gerçek proje deneyimleri dahil |

## Bilgi Ekleme

Yeni bilgi eklemek için `knowledge/_template.md` şablonunu kullan.
Belgeyi ekledikten sonra `knowledge/_index.json` dosyasını güncelle.
