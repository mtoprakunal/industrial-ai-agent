# PENKO SGM820 — Kablolama ve Entegrasyon Notları

> Bu notlar mühendislik özetidir. Bağlayıcı değerler için resmi PENKO dokümanına
> ve cihaz üstündeki etikete bak. Bulunamayan değerler `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

SGM820, SGM800 serisinin **Ethernet** üyesidir. Bir load cell (yük hücresi) köprüsünün
analog mV/V sinyalini yüksek hızda dijitalleştirir ve ağırlık değerini fabrika ağına
**Modbus TCP / Ethernet/IP** üzerinden sunar. Kontrol mantığı PLC'dedir; SGM820 ölçüm ve
sinyal işleme katmanıdır.

## Load Cell Bağlantısı

- Maksimum **8 load cell** (350 Ω) paralel sürülebilir.
- 4-telli veya 6-telli (sense) bağlantı; uzun kablo veya hassas tartımda **6-telli** tercih
  edilir (kablo direnci kompanzasyonu).
- Örnekleme hızı **1600/s'e kadar**; gösterge yenileme 1–50 Hz arası ayarlanır.
- Giriş duyarlılığı tek-kutuplu veya çift-kutuplu mV/V olarak yapılandırılır.
- Kalibrasyon: PENKO **G-Cal** otomatik kalibrasyon ya da bilinen ağırlıkla manuel.

## Haberleşme

| Arayüz | Protokol |
|--------|----------|
| Ethernet (RJ45) | Modbus TCP, Ethernet/IP, Omron FINS |
| USB | Konfigürasyon (PI Configuration / web) |

- Konfigürasyon: USB, ön panel veya gömülü web sunucusu (seçili modeller).
- Parametrelere (PDI ağacı) erişim PENKO'nun **PDI protokolü** ile yapılır; bu protokol
  Modbus TCP üzerinden tünellenebilir (bkz. resmi "PDI over Modbus" dokümanı).

## CODESYS Entegrasyonu

**Yol A — Modbus TCP (en taşınabilir):**
1. CODESYS device tree'de Ethernet adaptörü altına **Modbus TCP Master** ekle.
2. SGM820'yi **Modbus TCP Slave** olarak ekle (IP + port 502).
3. Ağırlık/diagnostik register'larını oku; setpoint/komut register'larına yaz.
4. Register/PDI indeksleri **resmi PENKO PDI/Modbus dokümanından** alınır — bu dosyada
   tahmini adres verilmedi.

**Yol B — Ethernet/IP:**
1. SGM820 için **EDS** dosyasını PENKO'dan indir (datasheet.json'da `download_url` boş —
   resmi destek/şop üzerinden temin et).
2. CODESYS Ethernet/IP Scanner altına adapter olarak ekle, EDS'ten assembly'leri eşle.

## Tartım Uygulamasında Tuzaklar

- **Ağırlık verisi best-effort raporlamadır**, deterministik kontrol değil. Hızlı dozaj
  kesme mantığı için setpoint çıkışlarını (4 programlanabilir setpoint) veya cihaz-içi
  hızlı karşılaştırmayı kullan; ağ gecikmesine güvenme.
- Filtre/yenileme hızı ile gürültü-tepki dengesi: yüksek hız = daha gürültülü okuma.
- Tek-yazar disiplini: setpoint/komut register'larını yalnızca tek PLC görevi yazsın.
- Mekanik: load cell topraklaması ve EMI; ağ tarafında OT segmentasyonu (Modbus'ta auth yok).

## Doğrulanmamış / Boş Bırakılan

Güç beslemesi, güç tüketimi, çalışma sıcaklığı, IP sınıfı, fiziksel boyut, gösterge
çözünürlüğü ve register adres haritası resmi kaynaktan teyit edilmeli.
