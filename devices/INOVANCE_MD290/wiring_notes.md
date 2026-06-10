# Inovance MD290 — Kablolama ve Entegrasyon Notları

> Bu notlar mühendislik özetidir. Bağlayıcı değerler için resmi Inovance MD290 kullanıcı/donanım
> kılavuzuna ve cihaz üstündeki etikete bak. Bulunamayan değerler `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

MD290, genel amaçlı **açık çevrim** kompakt bir VFD'dir. V/f kontrol (kayma kompanzasyonlu),
otomatik tork boost ve dahili DC reaktör içerir. Pompa/fan/konveyör gibi değişken-tork
uygulamaları için ekonomik bir sürücüdür. Dahili RS-485 (Modbus RTU) ile PLC'ye bağlanır.

## Güç Kablolama (genel VFD)

- **Giriş (şebeke):** R / S / T (3AC 380–480 V veya 200–240 V model). Uygun sigorta/şalter,
  gerekiyorsa EMC filtresi.
- **Motor (çıkış):** U / V / W → motor. Ekranlı motor kablosu; ekran iki uçta topraklı.
- **Frenleme:** DC bara / frenleme direnci terminalleri model aralığına göre mevcut.
- **Topraklama:** PE terminali düşük empedanslı toprağa.
- ⚠️ Giriş (R/S/T) ile çıkışı (U/V/W) karıştırma — yanlış bağlantı sürücüyü tahrip eder.

## Kontrol Terminalleri

- DI, DO/RELAY, AI (0–10 V / 0/4–20 mA), AO; sayılar modele göre değişir → resmi kılavuzdan teyit et.
- Komut ve frekans kaynağı parametreyle seçilir (terminal / panel / haberleşme).
- Kontrol kablolarını güç kablolarından ayrı ve ekranlı tut.

## RS-485 / Modbus RTU

- Dahili RS-485: A(+)/B(−). Çok düğümlü hatta **120 Ω** sonlandırma.
- Opsiyonel **izole RS-485 kartı (MD38TX1)** gürültülü ortamlarda tercih edilebilir.
- Parametrelerden: Modbus adresi, baud, parite, komut/frekans kaynağı = haberleşme (F0-28 protokol seçimi).
- Adres şeması: grup F/A parametre adresi = yüksek 8 bit grup + düşük 8 bit parametre SN (F0-16 → F010H).

## CODESYS Entegrasyonu (Modbus ile çalış/dur/frekans)

1. CODESYS'te seri arabirim altına **Modbus RTU (Modbus Master/serial device)** ekle.
2. MD290'ı **Modbus slave** olarak ekle (adres/baud/parite cihazla aynı).
3. Sürücüde komut/frekans kaynağını **haberleşme** yap.
4. Çalış/dur: **`0x2000`** komut register'ı — `1`=ileri çalış, `2`=geri çalış, `5`=serbest duruş, `6`=yavaşlayarak dur, `7`=hata reset.
5. Frekans setpoint: **`0x1000`** — ölçek `-10000…10000` = `-%100…%100`.
6. Durum oku: **`0x3000`** — `1`=ileri, `2`=geri, `3`=durmuş.

> NOT: Yukarıdaki register adresleri Inovance MD ailesinin ortak şemasıdır (MD500 ile aynı yapı).
> MD290'ın non-parameter adres tablosu kullanıma almadan önce **resmi MD290 Advanced User's Manual
> haberleşme bölümünden** teyit edilmelidir.

## Tek-Yazar Uyarısı

- Komut (`0x2000`) ve frekans (`0x1000`) register'larına **yalnızca tek bir PLC görevi** yazsın.
  Birden fazla yazıcı → öngörülemez davranış. HMI yazacaksa PLC üzerinden arabuluculukla yazsın.

## Fail-Safe (haberleşme kopunca sürücü davranışı)

- **Haberleşme zaman aşımı** parametresini ayarla: timeout'ta sürücü hata verip **güvenli dursun**.
- Komut yalnızca haberleşme ise hat koptuğunda son komut sürdürülmesin; timeout ile durmaya geçsin.
- Acil durdurma **donanımsal** olmalı; sadece Modbus'a güvenme. Modbus RTU'da auth yok → OT ağını segmente et.

## Doğrulanmamış / Boş Bırakılan

Çalışma sıcaklığı tam aralığı (ürün sayfasında -10…+40 °C, 40 °C üstü derating), fiziksel boyut/ağırlık,
montaj tipi, kontrol terminali sayıları ve kesin Modbus monitör adresleri resmi MD290 kaynağından
teyit edilmeli. Register şeması doğrudan MD290 kılavuzundan doğrulanmamıştır.
