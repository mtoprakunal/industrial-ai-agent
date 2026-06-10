# Inovance MD810 — Kablolama ve Entegrasyon Notları

> Bu notlar mühendislik özetidir. Bağlayıcı değerler için resmi Inovance MD810 Standard Drive
> User Guide ve cihaz etiketine bak. Bulunamayan değerler `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

MD810, bir **çoklu sürücü (multidrive) sistemidir**: ortak bir **güç besleme ünitesi (PSU)**
ve onun ortak DC barasından beslenen **birden fazla sürücü ünitesinden** oluşur. Çok eksenli/çok
noktalı sürüş, sarıcı/açıcı ve enerji geri kazanımlı uygulamalar için kitap (book) tipi panel
yapısı sunar. IM ve PMSM motorları V/f, SVC ve FVC ile sürer. **STO SIL3** güvenlik fonksiyonu içerir.

## Güç Kablolama (çoklu sürücü mimarisi)

- **PSU giriş (şebeke):** R / S / T → güç besleme ünitesi (3AC 400 V). Giriş koruma + EMC.
- **Ortak DC bara:** PSU, (+)/(−) DC barayı oluşturur; sürücü üniteleri bu baradan beslenir.
  Bara bağlantı baraları/kabloları üretici talimatına göre torklanır. ⚠️ Polariteye dikkat.
- **Motor (her sürücü ünitesi çıkışı):** U / V / W → ilgili motor. Ekranlı motor kablosu, iki uçta topraklı.
- **Topraklama:** PSU ve tüm sürücü üniteleri ortak PE barasına; düşük empedanslı toprak.
- **STO:** STO terminallerini güvenlik devresine (acil stop / güvenlik rölesi / güvenlik PLC) bağla.

## Kontrol Terminalleri

- Her sürücü ünitesinde DI/DO/AI/AO terminalleri; sayılar modele göre değişir → resmi kılavuzdan teyit et.
- Komut/frekans kaynağı parametreyle seçilir.

## RS-485 / Modbus RTU

- Dahili RS-485: A(+)/B(−). Çok düğümlü hatta **120 Ω** sonlandırma. Opsiyonel fieldbus kartı
  (PROFINET/CANopen/PROFIBUS-DP/CANlink) yuvası mevcuttur.
- Adres şeması: grup F/A parametre adresi = yüksek 8 bit grup + düşük 8 bit parametre SN (F0-16 → F010H).

## CODESYS Entegrasyonu (Modbus ile çalış/dur/frekans)

1. CODESYS'te seri arabirim altına **Modbus RTU (Modbus Master/serial device)** ekle; her sürücü
   ünitesi ayrı Modbus slave adresine sahip olabilir.
2. Sürücüde komut/frekans kaynağını **haberleşme** yap.
3. Inovance MD ailesi ortak şemasında çalış/dur **`0x2000`** komut, frekans setpoint **`0x1000`**,
   durum **`0x3000`** register'larıyla yapılır.

> NOT: MD810 register/adres tablosu bu çalışmada resmi kaynaktan **doğrudan doğrulanamadı**;
> bu yüzden `datasheet.json`'da `register_map` bilinçli olarak **boş bırakıldı**. Kesin adresler
> ve komut/durum kodları için **resmi MD810 Standard Drive User Guide haberleşme bölümüne** bak.

## Tek-Yazar Uyarısı

- Her sürücü ünitesinin komut/frekans register'larına **yalnızca tek bir PLC görevi** yazsın.
  Çok eksenli sistemde her eksene tek yazıcı disiplini uygulanmalı; aksi halde öngörülemez davranış.

## Fail-Safe (haberleşme kopunca sürücü davranışı)

- **Haberleşme zaman aşımı** parametresini ayarla: timeout'ta sürücü hata verip güvenli dursun.
- Çoklu sürücü sisteminde ortak DC bara nedeniyle bir ünite hatası diğerlerini etkileyebilir;
  sistem seviyesi hata/kapama mantığını planla.
- Acil durdurma **donanımsal** olmalı: **STO (SIL3)** terminallerini güvenlik devresine bağla,
  sadece Modbus'a güvenme. Modbus RTU'da auth yok → OT ağını segmente et.

## Doğrulanmamış / Boş Bırakılan

Aşırı yük değeri, çalışma/depolama sıcaklığı, IP sınıfı, fiziksel boyut/ağırlık ve kesin Modbus
register haritası resmi Inovance MD810 kaynağından teyit edilmeli. register_map bilinçli boş bırakıldı.
