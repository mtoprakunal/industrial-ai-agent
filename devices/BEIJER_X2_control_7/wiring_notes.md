# Beijer X2 control 7 — Kablolama ve Entegrasyon Notları

> Bu notlar mühendislik özetidir. Bağlayıcı değerler için resmi Beijer Hardware &
> Installation dokümanına ve cihaz etiketine bak. Bulunamayan değerler
> `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

X2 control 7, **7 inç dokunmatik HMI** ile **entegre CODESYS yumuşak PLC**'yi tek kompakt
donanımda birleştirir. HMI tarafı **iX Developer** ile, kontrol mantığı **BCS Tools**
(CODESYS tabanlı, IEC 61131-3) ile programlanır. Yani bu cihaz hem operatör paneli hem de
makine PLC'sidir — ayrı bir PLC gerekmez.

Donanım: NXP i.MX6 DualLite tek çekirdek Cortex-A9 1.0 GHz, 1 GB RAM, 2 GB eMMC
(1.5 GB uygulama). 800×480 rezistif dokunmatik.

## Beslemeyi ve Portları Bağlama

- Besleme: **+24 V DC (18–32 V DC)**, tüketim ~14.4 W. Güç ucu cihaz arkasındadır.
- **2x Ethernet** 10/100 Mbit (LAN A / LAN B, RJ45). LAN A genelde makine fieldbus'ı
  (EtherCAT/PROFINET), LAN B fabrika/IT ağı için ayrılır.
- Seri: **COM1 RS-232**, **COM2 RS-422/RS-485**, **COM3 RS-485** — eski PLC/sürücü ya da
  Modbus RTU cihazları için.
- **1x CAN 2.0B** — CANopen master/uzak I/O için.
- **1x USB Host 2.0** (proje aktarımı, USB bellek), **1x SD kart**.

## CODESYS Entegrasyonu (bu cihaz CODESYS'i ÇALIŞTIRIR)

X2 control, harici bir CODESYS PLC'ye bağlanan değil, **kendisi CODESYS runtime
çalıştıran** bir cihazdır.

1. **BCS Tools** (CODESYS 3.5 tabanlı Beijer platformu) ile PLC projesi oluştur.
2. **EtherCAT master** standarttır: device tree'de EtherCAT master altına ESI tabanlı
   slave'leri (sürücü, uzak I/O) ekle.
3. Modbus TCP/RTU, PROFINET, Ethernet/IP, CANopen sürücüleri CODESYS device tree'sine
   eklenir (gerektiğinde GSDML/EDS dosyası ilgili cihazdan temin edilir).
4. **iX Developer** (2.40 SP5+) ile HMI projesi yapılır; iX, BCS Tools 3.62 ile üretilen
   PLC değişkenlerini doğrudan tag olarak okur — HMI↔PLC köprüsü cihaz içidir, ağ değil.

## Fieldbus Köprüsü (harici cihazlara)

- EtherCAT master → sürücü/servo/uzak I/O (ESI).
- Modbus TCP master/slave → 3. parti cihazlar.
- PROFINET / Ethernet/IP → ilgili controller veya device rolünde.

## Tuzaklar

- **EtherCAT master tek olmalı**: aynı segmentte ikinci master olmaz; topoloji ve dağıtık
  saat (DC) ayarlarını kontrol et.
- **Ekran rezistiftir** (kapasitif değil): eldivenle çalışır ama çok-dokunuş yoktur.
- **LAN A/B ayrımı**: OT/IT segmentasyonu için iki Ethernet'i karıştırma; aynı subnet'e iki
  arayüz koymak yönlendirme sorunları çıkarır.
- iX ve BCS Tools **sürüm uyumu** kritiktir (iX 2.50 projesi ↔ BCS Tools 3.62 gibi); uyumsuz
  image ile proje yüklenmez.
- 24 V besleme ve fieldbus topraklamasında ortak referans/EMI'ye dikkat.

## Doğrulanmamış / Boş Bırakılan

İşletim sistemi (gömülü Linux varyantı muhtemel ama versiyon resmi teknik veride
doğrulanmadı), yerel dijital/analog I/O (model bazında yok), izolasyon değerleri ve
device description (GSDML/EDS — bağlanan cihaza göre) boş bırakıldı.
