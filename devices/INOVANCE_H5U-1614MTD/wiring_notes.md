# Inovance H5U-1614MTD — Kablolama ve Entegrasyon Notları

> Mühendislik özeti. Bağlayıcı değerler için resmi Inovance H5U broşürü/User Guide'a
> ve cihaz etiketine bak. Bulunamayan değerler `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

H5U-1614MTD, Inovance'ın yüksek performanslı **kompakt EtherCAT master PLC**'sidir.
16 dijital giriş / 14 dijital çıkış yerleşiktir; EtherCAT üzerinden **32 senkron eksene**
kadar PLCopen uyumlu hareket kontrolü yapar. Mantık + hareket aynı cihazdadır
(merkezi denetleyici). Inovance **AutoShop** ile programlanır (LD/SFC + FB/FC).

## Portlar ve Yerleşik I/O

| Arayüz | İşlev |
|--------|-------|
| EtherCAT (RJ45) | Master; maks. 72 slave (I/O + eksenler). 100 m segment. |
| Ethernet (RJ45) | Modbus TCP, socket programlama |
| RS485 | Modbus RTU master/slave + serbest protokol |
| CAN | CANopen (yalnız eksen kontrolü) ve CANlink master/slave |
| USB / SD | Program yükleme/indirme, firmware (SD ile) |

- **16 DI**: sink (NPN) / source (PNP); 4 x 200 kHz yüksek hızlı giriş dahil (2'si enkoder).
- **14 DO**: sink (NPN); 8 x 200 kHz yüksek hızlı çıkış dahil (4 eksen darbe çıkışı).
- Güç: **+24 VDC**.
- Yerel genişletme: 16 GL10 (AM600 serisi) modülü; uzak I/O için GR10 modülleri EtherCAT slave.

## Fieldbus Rolü

- **EtherCAT: MASTER.** Inovance servoları (SV660N), AC sürücüler (MD500-ECAT) ve
  GL20/GR10 uzak I/O coupler'ları slave olarak sürer.
- CANopen master olarak da sürücü kontrolü yapabilir (yalnız eksen).
- RS485/Modbus TCP üzerinden HMI (IT7000) ve üst sistemlerle veri paylaşır.

## CODESYS Entegrasyonu (DOLAYLI — H5U CODESYS değildir)

H5U **CODESYS DEĞİL**, Inovance **AutoShop** ile programlanır. Doğrudan CODESYS
runtime'ı yoktur. CODESYS tabanlı bir sistemle birlikte çalışmak gerekiyorsa:

**Yol A — Modbus TCP / RTU (en taşınabilir):**
1. H5U'yu Modbus TCP server veya RTU slave olarak yapılandır (AutoShop'ta).
2. CODESYS master tarafında Modbus TCP/RTU master ile H5U register'larını oku/yaz.
3. Paylaşılacak değişkenleri H5U soft-element/register alanına eşle.

**Yol B — EtherCAT/CANopen ağ seviyesi:**
- H5U kendi EtherCAT master ağını sürer; bu ağ ayrı tutulur. CODESYS master ile
  aynı EtherCAT segmentinde iki master OLAMAZ — segmentleri ayır, üst seviyede
  Ethernet (Modbus TCP) ile köprüle.

## Tuzaklar

- **Tek master kuralı:** Bir EtherCAT segmentinde tek master olur. H5U master iken
  başka bir CODESYS master aynı hatta bağlanamaz.
- CANopen yalnız **eksen kontrolü** için; genel CANopen I/O için CANlink'i değerlendir.
- Yüksek hızlı I/O kanalları (200 kHz) sabit pinlerde; darbe ekseni atarken normal
  DO olarak kullanma çakışmasına dikkat et.
- 24 VDC besleme ve sink/source DI kablolaması (NPN/PNP) ortak ucu doğru bağla.
- EtherCAT kablo segmenti 100 m'yi aşmasın.

## Doğrulanmamış / Boş Bırakılan

Çalışma/depolama sıcaklığı, nem, IP sınıfı, ağırlık, güç tüketimi ve izolasyon resmi
kaynaktan teyit edilmeli. EtherCAT ESI dosyası Inovance destek/AutoShop kurulumundan
temin edilir (`download_url` boş).
