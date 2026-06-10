# Beijer X2 pro 15 — Kablolama ve Entegrasyon Notları

> Bu notlar mühendislik özetidir. Bağlayıcı değerler için resmi Beijer Hardware &
> Installation dokümanına ve cihaz etiketine bak. Bulunamayan değerler
> `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

X2 pro 15, **15.4 inç geniş ekran dokunmatik operatör panelidir** (saf HMI). **iX runtime**
ile gelir, **iX Developer** ile programlanır. X2 pro ailesinin en büyük ekranlısıdır;
çözünürlük **1280×800**. Dahili PLC mantığı (CODESYS) **ÇALIŞTIRMAZ** — veriyi haberleşme
sürücüleriyle PLC'den okur/yazar. Donanım: i.MX6 DualLite çift çekirdek Cortex-A9 1.0 GHz,
1 GB RAM, 1.5 GB eMMC.

## Beslemeyi ve Portları Bağlama

- Besleme: **+24 V DC (18–32 V DC)**, tüketim ~31.2 W (büyük ekran nedeniyle pro 10'dan
  yüksek). Güç beslemesini buna göre boyutlandır.
- **2x Ethernet** 10/100 Mbit (LAN A / LAN B, RJ45).
- Seri: **RS-232**, **RS-422/RS-485**, **RS-485**.
- **1x CAN 2.0B**, **2x USB Host 2.0**, **1x SD kart**.

## PLC'ye Bağlanış (köprü protokol)

X2 pro 15 kontrol yapmaz, **PLC'ye HMI olarak bağlanır**. iX Developer'da haberleşme
sürücüsü seçilir:

- **Modbus TCP / Modbus RTU** (yaygın, satıcı-bağımsız),
- **Ethernet/IP**, **PROFINET**,
- veya iX driver kütüphanesindeki üreticiye özel PLC sürücüsü.

Tag'ler PLC register/sembollerine eşlenir; panel görselleştirir, operatör girişlerini PLC'ye
yazar.

## CODESYS Entegrasyonu (DİKKAT: dolaylı)

- X2 pro 15 **CODESYS çalıştırmaz.** CODESYS PLC'ye (X2 control, BoX2 SC, 3. parti) **Modbus
  TCP** veya **OPC-UA istemci** olarak bağlanır.
- **OPC-UA sunucu** olarak yapılandırılıp üst SCADA'ya köprü olabilir.
- Dahili kontrol gerekiyorsa **X2 control 15** (CODESYS'li) seçilmelidir.

## Tuzaklar

- "control" ile "pro" farkı: **pro = sadece HMI.**
- Ekran **rezistif**; büyük yüzeyde kalibrasyon ve baskı kuvveti tutarlılığına dikkat.
- 31.2 W tüketim: pano güç beslemesi ve termal tasarımı buna göre yap.
- Çok sürücü/yüksek tarama hızı CPU yükünü artırır.
- LAN A/B aynı subnet'e konmamalı; OT/IT segmentasyonu korunmalı.

## Doğrulanmamış / Boş Bırakılan

İşletim sistemi versiyonu, izolasyon değerleri ve device description dosyası (sürücü/PLC'ye
göre) boş bırakıldı. Yerel proses I/O'su yoktur.
