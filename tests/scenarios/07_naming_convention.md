# Senaryo 07 — Tag İsimlendirme

## Girdi

> "Şu tag isimlerini kullanmak istiyorum: 'Motor 1 Run Command!', '2Nci Bölge Sıcaklık',
> 'sensor'. Bunlar uygun mu?"

## Bağlam

Önerilen isimler kuralları ihlal ediyor: boşluk, özel karakter, baştan rakam, belirsizlik.
Agent standart formata göre düzeltmeli.

## Beklenen Davranış

- Sorunları tek tek gösterir: boşluk yok, özel karakter (`!`) yok, baştan rakam yok,
  ≤24 karakter, anlamsız/belirsiz isim ("sensor") olmaz.
- `{Area}_{DeviceType}_{Number}_{Signal}` formatına dönüştürür, örneğin:
  - `ZN1_MTR_01_RunCmd`
  - `ZN2_TMP_01_PV`
  - belirsiz "sensor" için netleştirme sorar (hangi alan/cihaz/sinyal?).
- İsimlerin GVL / IO listesi / HMI / ağ konfigürasyonu arasında **tutarlı** olması
  gerektiğini vurgular.

## Geçme Kriteri

- 🔴 `{Area}_{DeviceType}_{Number}_{Signal}` formatını uyguladı.
- 🔴 Boşluk/özel karakter/baştan rakam ihlallerini düzeltti.
- ≤24 karakter sınırına değindi.
- Belirsiz "sensor" için netleştirme istedi (varsayım yapıp geçmedi).
- Katmanlar arası isim tutarlılığını vurguladı.

## Dayanak

- `agent/rules.json` → `naming` (format, max_length, no_spaces, no_leading_numbers,
  allowed_chars, consistent_across_gvl_iolist_hmi_network)
