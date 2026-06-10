# Inovance MD500 — Kablolama ve Entegrasyon Notları

> Bu notlar mühendislik özetidir. Bağlayıcı değerler için resmi Inovance MD500 kullanıcı/donanım
> kılavuzuna ve cihaz üstündeki etikete bak. Bulunamayan değerler `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

MD500, yüksek performanslı genel amaçlı bir VFD'dir. V/f, sensörsüz vektör (SVC) ve kapalı
çevrim vektör (FVC) kontrol modlarını destekler. Şebekeden aldığı 3-fazlı gücü, motoru
değişken frekans/gerilimle sürmek için dönüştürür. Dahili RS-485 (Modbus RTU) ile PLC'ye bağlanır.

## Güç Kablolama (genel VFD)

- **Giriş (şebeke):** R / S / T (3AC 380–480 V veya 200–240 V model). Giriş tarafına uygun
  sigorta/şalter ve gerekiyorsa giriş reaktörü/EMC filtresi.
- **Motor (çıkış):** U / V / W → motor. Çıkış kablosu **ekranlı** olmalı; ekran her iki uçta
  topraklanır. Motor dönüş yönü U/V/W sırasıyla belirlenir.
- **DC bara / frenleme:** (+)/(−) DC bara ve frenleme direnci terminalleri (model aralığına göre;
  dahili frenleme ünitesi mevcut olabilir). Frenleme direnci ayrı bağlanır.
- **Topraklama:** PE terminali düşük empedanslı toprağa; motor PE'si sürücü PE'sine.
- ⚠️ Giriş ile çıkışı ASLA karıştırma — R/S/T'ye motor, U/V/W'ye şebeke bağlanırsa sürücü hasar görür.

## Kontrol Terminalleri

- Dijital girişler (DI), dijital/röle çıkışları (DO/RELAY), analog girişler (AI, 0–10 V / 0/4–20 mA),
  analog çıkış (AO). Terminal sayıları modele göre değişir → resmi kılavuzdan teyit et.
- Terminal komutu mı yoksa haberleşme komutu mu kullanılacağı parametreyle seçilir (komut kaynağı).
- Kontrol kablolarını güç kablolarından ayrı kanalda ve ekranlı tut.

## RS-485 / Modbus RTU

- Dahili RS-485 portu: A(+)/B(−) hattı. Çok düğümlü hatta hat sonu **120 Ω** sonlandırma.
- Parametrelerden ayarla: Modbus adresi, baud hızı, parite, komut/frekans kaynağı = haberleşme.
- Adres şeması: grup F/A parametreleri için adres = yüksek 8 bit grup + düşük 8 bit parametre SN
  (örn F0-16 → F010H).

## CODESYS Entegrasyonu (Modbus ile çalış/dur/frekans)

1. CODESYS device tree'de RS-485/seri arabirim altına **Modbus RTU (COM Port → Modbus Master/serial device)** ekle.
2. MD500'ü **Modbus slave** olarak ekle (slave adresi, baud, parite cihazla aynı olmalı).
3. Sürücüde komut/frekans kaynağını **haberleşme** yap.
4. Çalış/dur: **`0x2000`** komut register'ına yaz — `1`=ileri çalış, `2`=geri çalış, `5`=serbest duruş, `6`=yavaşlayarak dur, `7`=hata reset.
5. Frekans setpoint: **`0x1000`** register'ına yaz — ölçek `-10000…10000` = `-%100…%100` (göreli set değeri).
6. Durum oku: **`0x3000`** — `1`=ileri çalışıyor, `2`=geri çalışıyor, `3`=durmuş. Hata: **`0x8000`**.
7. Çıkış frekansı/bara gerilimi/akım gibi monitör değerleri Grup U register'larından okunur — kesin
   adresler resmi MD500 kullanıcı kılavuzu Ek B/C'den teyit edilmeli.

## Tek-Yazar Uyarısı

- Komut (`0x2000`) ve frekans (`0x1000`) register'larına **yalnızca tek bir PLC görevi** yazmalı.
  Aynı register'a birden fazla yazıcı = öngörülemez davranış. HMI'dan da yazılacaksa tek bir
  arabuluculuk katmanı (örn PLC) üzerinden yazılsın.

## Fail-Safe (haberleşme kopunca sürücü davranışı)

- Sürücüde **haberleşme zaman aşımı / iletişim kesinti** parametresini ayarla: zaman aşımında
  sürücü hata versin ve **güvenli şekilde dursun** (coast veya yavaşlayarak dur).
- Komut kaynağı sadece haberleşme ise, hat koptuğunda sürücü son komutu sürdürmesin; timeout ile
  durmaya geçsin. Acil durdurma her zaman **donanımsal** (terminal/STO) olmalı, sadece Modbus'a güvenme.
- Modbus RTU'da kimlik doğrulama yoktur; OT ağını segmente et.

## Doğrulanmamış / Boş Bırakılan

Çalışma sıcaklığı tam aralığı, IP sınıfı, fiziksel boyut/ağırlık, montaj tipi, kontrol terminali
sayıları ve Grup U monitör register adresleri resmi Inovance MD500 kaynağından teyit edilmeli.
