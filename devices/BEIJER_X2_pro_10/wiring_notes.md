# Beijer X2 pro 10 — Kablolama ve Entegrasyon Notları

> Bu notlar mühendislik özetidir. Bağlayıcı değerler için resmi Beijer Hardware &
> Installation dokümanına ve cihaz etiketine bak. Bulunamayan değerler
> `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

X2 pro 10, **10.1 inç dokunmatik operatör panelidir** (saf HMI). **iX runtime** ile gelir,
**iX Developer** ile programlanır. X2 control'den farkı: **dahili PLC mantığı (CODESYS)
ÇALIŞTIRMAZ.** Donanımı X2 control 10'a benzer (i.MX6 DualLite çift çekirdek Cortex-A9
1.0 GHz, 1 GB RAM, 1.5 GB eMMC) ama kontrol motoru yoktur — veriyi haberleşme sürücüleriyle
bir PLC'den okur/yazar.

## Beslemeyi ve Portları Bağlama

- Besleme: **+24 V DC (18–32 V DC)**, tüketim ~21.6 W.
- **2x Ethernet** 10/100 Mbit (LAN A / LAN B, RJ45).
- Seri: **COM1 RS-232 (RTS/CTS)**, **COM2 RS-422/RS-485**, **COM3 RS-485**.
- **1x CAN 2.0B**, **2x USB Host 2.0**, **1x SD kart**.

## PLC'ye Bağlanış (köprü protokol)

X2 pro kontrol yapmaz, **PLC'ye HMI olarak bağlanır**. iX Developer'da bir veya birden çok
**haberleşme sürücüsü (driver)** seçilir:

- **Modbus TCP / Modbus RTU** (en yaygın, satıcı-bağımsız),
- **Ethernet/IP**, **PROFINET**,
- ya da iX driver kütüphanesindeki üreticiye özel PLC sürücüsü (Siemens, Mitsubishi,
  Rockwell vb.).

iX tag'leri PLC register/sembollerine eşlenir; panel bu tag'leri okuyup gösterir, operatör
girişlerini PLC'ye yazar.

## CODESYS Entegrasyonu (DİKKAT: dolaylı)

- X2 pro **CODESYS çalıştırmaz.** Bir CODESYS PLC'ye (X2 control, BoX2 SC veya 3. parti
  CODESYS denetleyici) bağlanmak için panelde **Modbus TCP** veya **OPC-UA istemci** sürücüsü
  kullan; PLC tarafında karşılık gelen sunucu/slave açık olmalı.
- Panel ayrıca **OPC-UA sunucu** olarak yapılandırılıp üst SCADA'ya köprü olabilir.
- Dahili kontrol mantığı gerekiyorsa **X2 control 10** (CODESYS'li) modeline geç.

## Tuzaklar

- "control" ile "pro"yu karıştırma: **pro = sadece HMI**, control = HMI+PLC. Sipariş/seçimde
  bu fark kritiktir.
- Ekran **rezistif** (~1 milyon dokunma ömrü); kapasitif çoklu dokunuş yok.
- Çok sayıda sürücü/yüksek tarama hızı CPU yükünü artırır; tag yenileme periyotlarını ölçeklendir.
- LAN A/B'yi aynı subnet'e koyma; OT/IT ayrımını koru.

## Doğrulanmamış / Boş Bırakılan

İşletim sistemi versiyonu, izolasyon değerleri ve device description dosyası (sürücü/PLC'ye
göre) boş bırakıldı. Yerel proses I/O'su yoktur.
