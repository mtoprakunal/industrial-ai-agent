# Bilgi Tabanını Kullanma Kılavuzu

## Bir Soru Geldiğinde Takip Et

```
Soru geldi
    │
    ▼
/knowledge/ içinde ara
    │
    ├── Belge var + Uzman/İleri seviye → Doğrudan kullan
    │
    ├── Belge var + Temel/Orta seviye → Kullan ama sınırı belirt
    │
    ├── Stub var → "Bu konuda belge hazırlanıyor" de, web'de araştır
    │
    └── Hiç yok → Web araştırması yap, bulduğunu sun ve eklemeyi öner
```

## Birden Fazla Belge Varsa

Aynı konuda birden fazla belge varsa hepsini oku. Çelişen bilgi ara. Sentez belgesi (`_synthesis.md`) varsa önce onu oku — zaten birleştirilmiş en doğru bilgiyi içerir.

## Bağlantılı Konuları Takip Et

Her belgedeki `BAĞLANTILAR` alanını kontrol et. İlgili belgeleri de oku. Gerçek anlayış izole bilgiden değil bağlantılardan gelir.

## Kaynak Ekleme Akışı

Araştırma yaptın ve değerli bilgi buldun:
1. Kaynağın güvenilirliğini değerlendir
2. `_template.md` formatında yeni belge oluştur
3. `_index.json` içinde seviyeyi güncelle
4. `_graph.json` içine bağlantıları ekle
5. Varsa `_synthesis.md` belgesini güncelle

## Bilmediğini Söyle

"Bu konuda henüz bilgi tabanımda yeterli belge yok" demek yanlış değil.
Tahminde bulunmak yanlış.
