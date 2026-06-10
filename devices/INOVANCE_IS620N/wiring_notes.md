# Inovance IS620N — Kablolama ve Entegrasyon Notları

> Mühendislik özetidir. Bağlayıcı değerler için resmi Inovance IS620N kullanım/haberleşme
> kılavuzuna ve cihaz etiketine bak. Bulunamayan değerler `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

IS620N, IS620 servo ailesinin **EtherCAT** ("N" = network) üyesi tek eksenli AC servo
sürücüsüdür. Bir EtherCAT master (PLC/motion controller, ör. Inovance AM600 veya CODESYS
SoftMotion) bu sürücüyü **CiA 402** ekseni olarak sürer. Motoru ve 23-bit mutlak enkoder
geri beslemesini kapatarak konum/hız/tork çevrimini gerçekler.

## Güç Bağlantısı

- Ana güç giriş sınıfı modele göre: **1AC 220 V**, **3AC 220 V** veya **3AC 380 V**.
  Sürücü etiketindeki giriş sınıfını motorla eşleştir.
- Kontrol/STO devresi için **24 VDC** harici besleme.
- Model akımına uygun sigorta/kontaktör; gerekiyorsa hat reaktörü/EMC filtresi.
- Frenleme enerjisi için gerektiğinde harici regen direnci boyutlandır.

## Motor ve Enkoder Bağlantısı

- Motor güç kabloları (U/V/W) faz sırasıyla; PE (toprak) zorunlu.
- **Enkoder**: 23-bit mutlak (multi-turn) seri enkoder kablosu sürücünün enkoder
  konnektörüne. Multi-turn pozisyon koruması için pil (motor/kablo seçeneğine göre) gerekebilir.
- Güç ve enkoder kablolarını ayrı, ekranlı, tek noktadan topraklı tut (EMI).

## Haberleşme (EtherCAT)

| Arayüz | İşlev |
|--------|-------|
| 2x RJ45 (IN / OUT) | EtherCAT hat (line) topolojisi |
| USB / komisyon | InoServoShop ile ince ayar/diagnostik |

- EtherCAT CoE + **CiA 402** profili; PP/PV/PT/HM/CSP/CSV/CST modları.
- Broşüre göre ESI/XML kütüphanesi sayesinde sürücü kontrolör tarafından otomatik tanınır.

## CODESYS SoftMotion / CiA 402 Ekseni Olarak Ekleme

1. CODESYS device tree'de **EtherCAT Master** ekle, ağ adaptörünü seç.
2. IS620N **ESI/XML** dosyasını Device Repository'ye yükle (Inovance resmi destek
   portalından temin et — `datasheet.json`'da `download_url` boş).
3. Master altına IS620N slave'ini ekle; PDO eşlemesini yapılandır.
4. Slave üzerine sağ tık → **Add SoftMotion CiA 402 Axis**.
5. PLCopen `MC_Power`, `MC_MoveAbsolute`, `MC_MoveVelocity` FB'leriyle ekseni sür.
6. Tipik CSP modu; çevrim süresini master görev periyoduyla eşle.

## STO / Emniyet

- IS620N model bazlı **STO (Safe Torque Off)** emniyet fonksiyonu içerir (çift kanallı
  emniyet girişi). STO tetiklendiğinde motor torku güvenli kesilir — bu **fren değildir**;
  mekanik tutma için motor freni gerekebilir.
- Terminal/konnektör adı, kablo uzunluğu ve SIL/PL kategorisi resmi IS620N emniyet
  kılavuzundan doğrulanmalı (datasheet.json'da boş bırakıldı).

## Fail-safe / Tuzaklar

- EtherCAT kopmasında master watchdog ile eksen güvenli durdurma (quick stop); CiA 402
  fault tepkisini yapılandır.
- Tek-yazar: eksen referanslarını yalnızca motion görevi yazsın.
- Devreye alımda mutlak enkoder referansını/homing'i doğrula.
- Pano içi dikey **arka plaka montaj**; temiz/kuru ortam.

## Doğrulanmamış / Boş Bırakılan

Çalışma/depolama sıcaklığı, nem, IP sınıfı, ağırlık, tam fiziksel boyut, overload katsayısı,
STO terminal adı ve SIL/PL kategorisi ile ESI indirme linki resmi Inovance kaynağından
teyit edilmeli. Üreticiye özel parametre adresleri IS620N haberleşme kılavuzundan alınmalı
(uydurulmadı).
