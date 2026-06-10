# Beijer X2 control 10 — Kablolama ve Entegrasyon Notları

> Bu notlar mühendislik özetidir. Bağlayıcı değerler için resmi Beijer Hardware &
> Installation dokümanına ve cihaz etiketine bak. Bulunamayan değerler
> `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

X2 control 10, **10.1 inç dokunmatik HMI** ile **entegre CODESYS yumuşak PLC**'yi birleştirir.
X2 control 7'nin büyük ve daha güçlü kardeşidir: **i.MX6 Quad** (dört çekirdek Cortex-A9
1.0 GHz), **2 GB RAM**. HMI iX Developer ile, kontrol mantığı BCS Tools (CODESYS 3.5) ile
yazılır — ayrı PLC gerekmez.

## Beslemeyi ve Portları Bağlama

- Besleme: **+24 V DC (18–32 V DC)**, tüketim ~21.6 W.
- **2x Ethernet** 10/100 Mbit (LAN A / LAN B, RJ45) — fieldbus ve IT ağı ayrımı için.
- Seri: **RS-232**, **RS-422/RS-485**, **RS-485** (üç COM).
- **2x USB Host 2.0**, **1x SD kart**.
- **2x Opto-MOS relay (SPST) çıkış** — küçük yerel dijital çıkış (ör. durum/alarm rölesi).
  (7 modelinden farklı olarak teknik veride CAN portu listelenmiyor.)

## CODESYS Entegrasyonu (bu cihaz CODESYS'i ÇALIŞTIRIR)

1. **BCS Tools** ile CODESYS 3.5 PLC projesi oluştur. 64 KB non-volatile değişken alanı var.
2. **EtherCAT master** standarttır; CODESYS EtherCAT/Modbus Ethernet/Modbus RTU/CANopen
   sürücüleri desteklenir.
3. Slave cihazları device tree'ye ekle (EtherCAT için ESI, Ethernet/IP için EDS, PROFINET
   için GSDML — ilgili cihazdan temin et).
4. **iX Developer** (2.40 SP5+) HMI projesi; iX, BCS Tools 3.62 PLC tag'lerini cihaz içi
   senkronizasyonla okur (ağ üzerinden değil).

## Fieldbus Köprüsü (harici cihazlara)

- EtherCAT master → sürücü/uzak I/O.
- Modbus TCP/RTU master → 3. parti cihaz/sayaç.
- PROFINET / Ethernet/IP → controller/device rolünde.

## Tuzaklar

- Opto-MOS çıkışları **küçük sinyal** içindir; doğrudan kontaktör/yük sürmek için harici röle
  kullan, akım/gerilim sınırına uy.
- EtherCAT master tek olmalı; DC senkronizasyon ve topoloji ayarlarını doğrula.
- Ekran **rezistif** — kapasitif çoklu dokunuş beklenmemeli.
- iX ↔ BCS Tools sürüm uyumu ve image versiyonu kritik.
- LAN A/B'yi aynı subnet'e koyma; OT/IT segmentasyonunu koru.

## Doğrulanmamış / Boş Bırakılan

İşletim sistemi versiyonu, yerel analog I/O (yok), izolasyon ve device description dosyası
(bağlanan cihaza göre) boş bırakıldı. CAN portu bu modelde teknik veride listelenmediği
için eklenmedi.
