# Inovance SV660N — Kablolama ve Entegrasyon Notları

> Mühendislik özetidir. Bağlayıcı değerler için resmi Inovance SV660N donanım/haberleşme
> kılavuzuna ve cihaz etiketine bak. Bulunamayan değerler `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

SV660N, tek eksenli **EtherCAT** AC servo sürücüsüdür ("N" = network). Bir EtherCAT
master (PLC/motion controller, ör. CODESYS SoftMotion veya Inovance AM/AC serisi) bu
sürücüyü CiA 402 ekseni olarak sürer. Sürücü, motoru ve 23-bit enkoder geri beslemesini
kapatarak konum/hız/tork çevrimini gerçekler.

## Güç Bağlantısı

- Ana güç giriş sınıfı modele göre: **1AC 220 V**, **3AC 220 V** veya **3AC 380 V**.
  Sürücü etiketindeki giriş sınıfını motorla eşleştir.
- Kontrol/STO devresi için **24 VDC (±15%)** harici besleme gerekir.
- Giriş tarafına model akımına uygun sigorta/kontaktör; gerekiyorsa hat reaktörü/EMC filtresi.
- Yüksek atalet/sık frenleme uygulamasında **harici fren (regen) direnci** boyutlandır.

## Motor ve Enkoder Bağlantısı

- Motor güç kabloları (U/V/W) faz sırasına dikkat ederek bağlanır; PE (toprak) zorunlu.
- **Enkoder**: 23-bit seri (mutlak) enkoder kablosu sürücünün enkoder konnektörüne.
  Mutlak modda multi-turn pil (varsa motor/kablo seçeneğine göre) gerekebilir.
- Güç ve enkoder kablolarını ayrı kanallarda, ekranlı ve tek noktadan topraklı tut (EMI).

## Haberleşme (EtherCAT)

| Arayüz | İşlev |
|--------|-------|
| 2x RJ45 (IN / OUT) | EtherCAT hat (line) topolojisi — master'dan gelen IN, sonraki slave'e OUT |
| USB | Komisyon / diagnostik (InoDriverShop) |

- EtherCAT CoE + **CiA 402** profili; 7 çalışma modu (PP, PV, PT, HM, CSP, CSV, CST),
  ~125 µs çevrim süresi.
- IN/OUT yönüne dikkat; hat sonundaki slave'in OUT portu boş kalır.

## CODESYS SoftMotion / CiA 402 Ekseni Olarak Ekleme

1. CODESYS device tree'de **EtherCAT Master** ekle, ağ adaptörünü seç.
2. SV660N **ESI/XML** dosyasını CODESYS Device Repository'ye yükle (Inovance resmi
   destek portalından temin et — `datasheet.json`'da `download_url` boş).
3. Master altına SV660N slave'ini ekle; PDO eşlemesini seç (controlword/statusword,
   target/actual position vb.).
4. Slave üzerine sağ tık → **Add SoftMotion CiA 402 Axis** ile eksen objesi ekle.
5. PLCopen `MC_Power`, `MC_MoveAbsolute`, `MC_MoveVelocity` vb. FB'lerle ekseni sür.
6. Tipik mod CSP (cyclic synchronous position); döngü süresini master görev periyoduyla eşle.

## STO / Emniyet

- **STO (Safe Torque Off)**: çift kanallı, izole girişler **STO1/STO2**, konnektör **CN6**
  (sadece **-FS** emniyet modelinde). Besleme 24 VDC.
- Sürücü ile emniyet şalteri/röle arası **maks. 30 m** kablo.
- STO tetiklendiğinde motor torku güvenli şekilde kesilir (serbest yavaşlar) — bu bir
  **fren değildir**; mekanik tutma için ayrıca motor freni gerekebilir.
- Emniyet fonksiyonunu emniyet rölesi/PLC ile entegre et; SIL/PL kategorisini resmi
  emniyet kılavuzundan doğrula (datasheet.json'da boş bırakıldı).

## Fail-safe / Tuzaklar

- EtherCAT kopması → master watchdog ile eksen güvenli durdurma (quick stop) tetiklenmeli;
  fault tepkisini CiA 402 durum makinesinde yapılandır.
- Tek-yazar: eksen referanslarını yalnızca motion görevi yazsın.
- Mutlak enkoder pil/multi-turn referansını devreye alımda doğrula (homing gerekebilir).
- Pano içi dikey **arka plaka montaj**; IP20 → temiz/kuru pano içi şart.

## Doğrulanmamış / Boş Bırakılan

Depolama sıcaklığı, nem, ağırlık, tam fiziksel boyut, overload katsayısı, STO SIL/PL
kategorisi ve ESI indirme linki resmi Inovance kaynağından teyit edilmeli. Üreticiye özel
H-grubu Modbus parametre adresleri SV660N Communication Guide'dan alınmalı (uydurulmadı).
