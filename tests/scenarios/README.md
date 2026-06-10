# Agent Davranış Senaryoları

Bu klasör, agent'ın **niteliksel** kalitesini değerlendirmek için tasarlanmış senaryolardır.
`tests/integrity/` otomatik testleri *bilgi tabanının yapısını* doğrular; buradaki
senaryolar ise *agent'ın akıl yürütmesini* doğrular.

## Nasıl Kullanılır

1. Senaryodaki **Girdi**'yi agent'a aynen ver (agent `agent/system_prompt.md` kimliğiyle
   ve `/knowledge/` erişimiyle çalışıyor olmalı).
2. Agent'ın cevabını **Geçme Kriteri** maddeleriyle karşılaştır.
3. Her madde için ✅ / ❌ işaretle. Eşik: kritik (🔴) maddelerin **tamamı** + toplamın
   en az %80'i tutmalı.

> Bu senaryolar otomatik koşmaz — `run_tests.py` bunları çalıştırmaz. Bir LLM-judge ile
> otomatikleştirilebilirler (her senaryonun Geçme Kriteri rubric olarak hazırdır), ama
> tasarım gereği insan/değerlendirici gözüyle okunmak içindirler.

## Senaryo Formatı

Her senaryo şu bölümleri içerir:

- **Girdi** — agent'a verilen prompt (aynen).
- **Bağlam** — senaryonun neyi test ettiği.
- **Beklenen Davranış** — agent'ın sergilemesi gereken akıl yürütme.
- **Geçme Kriteri** — işaretlenebilir rubric (🔴 = kritik, ihlal = başarısız).
- **Dayanak** — hangi kural/belge bu davranışı zorunlu kılıyor.

## Senaryo Listesi

| # | Senaryo | Test edilen çekirdek yetenek |
|---|---------|------------------------------|
| 01 | Protokol seçimi (çok istemci) | Eksen analizi + KARAR/GEREKÇE/TAKAS |
| 02 | Kontrol task'ında bloke I/O | Watchdog tuzağı, task ayrımı |
| 03 | E-Stop yazılımda mı? | Emniyet donanımsaldır (ihlal edilemez) |
| 04 | Task ataması | Gecikme toleransı → cycle time eşlemesi |
| 05 | HMI teknoloji çelişkisi | Tercihe saygı vs gereksinim çelişkisi |
| 06 | Bilinmeyen konu | Dürüstlük — uydurmama, araştırma teklifi |
| 07 | Tag isimlendirme | {Area}_{Type}_{Num}_{Signal}, ≤24 |
| 08 | Watchdog hata ayıklama | Sistematik teşhis, watchdog'u kapatmama |
