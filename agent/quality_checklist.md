# Kalite Kontrol Listesi — Proje Kabul Kriterleri

Her üretilen proje teslimden önce bu listeden geçer. Eksik kalan her madde ya tamamlanır ya da kullanıcıya **açıkça "yapılmadı" diye bildirilir.** Sessiz boşluk bırakmak başarısızlıktır; eksiği söylemek değildir.

---

## ⭐ Çekirdek Kabul Kriterleri

```
□ Tüm I/O'lar taglanmış
□ Adres çakışması yok
□ Task yapısı doğru (her mantık doğru cycle time'da)
□ Watchdog yapılandırılmış (açık)
□ Safety sinyalleri doğru task'ta (en yüksek öncelik, standart modülde değil)
□ Tüm FB'lerin açıklaması var
□ Alarm listesi tam
□ I/O listesi tam
□ Proje raporu yazılmış
□ HMI tüm kritik sinyalleri gösteriyor
□ Bağlantı kopması senaryosu düşünülmüş
```

Bu 11 madde geçmeden proje teslim edilmez.

---

## Detaylı Kontroller

### Bilgi & Dürüstlük
```
□ Her teknik iddianın kaynağı belli (bilgi tabanı belgesi / web kaynağı)
□ Tahmin yapılan yer varsa açıkça işaretlenmiş
□ Düşük olgunluk seviyeli konularda sınır belirtilmiş
□ Birden fazla kaynak sentezlenmiş (izole tek belge değil)
□ Çelişen kaynak varsa analiz edilmiş
```

### Karar Kalitesi
```
□ Her önemli karar KARAR / GEREKÇE / TAKAS üçlüsüyle sunulmuş
□ Alternatif yaklaşımlar belirtilmiş
□ Katı eşik yerine gereksinim-temelli akıl yürütme yapılmış
□ Çelişen gereksinimler kullanıcıya iletilmiş
□ Riskler önceden söylenmiş
```

### CODESYS / Kod
```
□ Task çevrim süreleri rules.json sınırları içinde
□ Her task exec time < cycle time
□ Toplam CPU yükü ≤ %70
□ Bloke I/O (connect/MQTT/dosya) kontrol task'ında DEĞİL, Freewheeling'de
□ İsimlendirme {Area}_{DeviceType}_{Number}_{Signal}, ≤24 karakter, boşluksuz
□ Sihirli sayı yok (sabit kullanılmış)
□ Pointer'lar her scan yeniden hesaplanıyor (saklanmıyor)
□ REAL bölmelerde NaN / sıfıra bölme kontrolü var
□ GVL ↔ io_list.csv ↔ ağ adres haritası birbiriyle tutarlı
□ Tek-yazar disiplini (her register/node/topic tek yazar)
```

### Emniyet (bkz. safety_principles.md)
```
□ Emniyet I/O standart modüllere bağlanmamış
□ CPU/watchdog arızasında tüm çıkışlar enerjisiz (fail-safe = stop)
□ E-Stop donanımsal, yazılım sadece durumu yansıtıyor
□ Watchdog açık (devre dışıysa gerekçe raporda)
□ Interlock'lar merkezi ve gerekçeli
□ Analog girişler aralık dışı (NAMUR NE107) için kontrol ediliyor
□ "Tek yazılım hatası birini yaralayabilir mi?" sorusu cevaplandı
```

### Protokol / Ağ
```
□ Protokol seçimi eksen analiziyle gerekçelendirilmiş
□ Modbus internete açık değil (port 502 izole)
□ OPC-UA üretimde anonim/None değil (güvenlik modu aktif)
□ MQTT'de LWT retained "false" yapılandırılmış
□ Sampling/poll periyodu task cycle ile uyumlu
```

### HMI
```
□ Köprü protokol üzerinden (mantık HMI'a gömülmemiş)
□ Kullanıcının tercih ettiği teknolojide üretilmiş
□ Tüm kritik sinyaller gösteriliyor
□ Bağlantı kopması senaryosu ele alınmış (heartbeat/connection flag)
□ Alarmlar onay (ack) mekanizmasıyla gösteriliyor
□ Kontrol aksiyonları için kullanıcı yetkilendirme var
```

### Çıktı Eksiksizliği
```
□ project_report.md (kararlar + riskler) üretildi
□ io_list.csv eksiksiz
□ alarm_list.csv (seviye, sebep, çözüm) eksiksiz
□ hardware_config/, program/, hmi/, docs/ mevcut
□ Risk değerlendirmesi yazıldı (varsayımlar işaretli)
```

### İletişim
```
□ Riskler ve öneriler açıkça listelendi
□ Üretilen yeni bilgi için "bilgi tabanına ekleyeyim mi?" soruldu
□ Eksik kalan maddeler gizlenmeden bildirildi
```

---

> **Son kontrol:** Bir madde "yapılamadı" ise bu bir başarısızlık değil — **gizlemek** başarısızlıktır. Eksiği söyle, gerekçesini ver, riski belirt.
