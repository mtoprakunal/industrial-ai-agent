# Beijer BoX2 A12 — Kablolama ve Entegrasyon Notları

> Bu notlar mühendislik özetidir. Bağlayıcı değerler için resmi Beijer Hardware &
> Installation dokümanına ve cihaz etiketine bak. Bulunamayan değerler
> `datasheet.json`'da boş bırakıldı.
>
> **ÖNEMLİ:** "BoX2 A12" tam model adı Beijer'in güncel resmi ürün sayfalarında
> **doğrulanamadı**. 'A12' büyük olasılıkla bir donanım platformu / parça kodu ya da
> bölgesel/eski isimlendirmedir. Aşağıdaki bilgiler, cihaz tanımına en uygun doğrulanmış
> aile olan **BoX2 pro / BoX2 pro SC**'ye dayanır. Kesin değerleri sipariş kodu üzerinden
> resmi BoX2 dokümanından teyit et.

## Cihaz Ne İşe Yarar

BoX2, **ekransız (headless) endüstriyel box** cihazıdır: protokol dönüştürücü + IIoT/edge
gateway. **iX runtime** çalıştırır ve **iX Developer** ile yapılandırılır. Tipik BoX2 pro:
1 GHz çift çekirdek Cortex-A9, 1 GB RAM, 2 GB NAND flash, WEC2013 üstünde iX runtime.

İki temel kullanım:
1. **Gateway / HMI sunucu** (standart base/pro): farklı PLC/sürücü/protokolleri birbirine
   bağlar, veri tabanı/alarm/raporlama tutar, OPC-UA sunucu olarak üst sisteme veri verir.
2. **Edge controller** (yalnızca **SC = soft control** sürümleri): entegre **CODESYS**
   çalıştırır, BCS Tools ile programlanır, EtherCAT/Modbus/CANopen master olabilir.

## Beslemeyi ve Portları Bağlama

- Besleme: **+24 V DC (18–32 V DC)**.
- **2x Ethernet** 100 Mbit (LAN A / LAN B, RJ45) — bir taraf saha, diğer taraf IT/bulut.
- **3x seri port** (9-pin DSUB): RS-232 / RS-422 / RS-485 yazılımdan seçilir — Modbus RTU
  ve eski seri PLC'ler için.
- **1x USB Host 2.0**, **1x SD/microSD** kart.
- IP20/IP22 sınıfı (pano içi); **DIN ray** veya masaüstü/montaj plakası ile monte edilir.

## PLC'ye Bağlanış (köprü protokol)

- **Standart BoX2 (base/pro):** kontrol yapmaz. PLC'ye **Modbus TCP / Modbus RTU /
  Ethernet/IP / OPC-UA istemci** sürücüsüyle bağlanır; veriyi toplar, dönüştürür, üst
  sisteme **OPC-UA sunucu** ya da MQTT/bulut ile aktarır.
- Seri taraf (RS-485) Modbus RTU master/slave köprülemesi için kullanılır.

## CODESYS Entegrasyonu (DİKKAT: yalnızca SC sürümünde)

- **Standart BoX2 CODESYS ÇALIŞTIRMAZ** — sadece iX runtime. Harici CODESYS PLC'ye Modbus
  TCP / OPC-UA istemcisi olarak bağlanır.
- **BoX2 pro SC / extreme SC** sürümleri **entegre CODESYS Control 3.5** çalıştırır (BCS
  Tools ile programlanır), EtherCAT/Modbus/CANopen master olarak saha cihazlarını sürer.
- "A12" varyantının **SC olup olmadığı** resmi sipariş koduyla teyit edilmeli; SC değilse
  yerel kontrol için ayrı bir CODESYS denetleyici gerekir.

## Tuzaklar

- **SC / non-SC ayrımı kritiktir.** CODESYS bekleyip standart (non-SC) cihaz almak en sık
  hatadır — kontrol mantığı çalışmaz.
- Ekransız cihaz: tüm yapılandırma/teşhis ağ (iX, web) üzerinden yapılır; LAN A varsayılan
  IP'sini (genelde 192.168.x.x) ve LAN B DHCP davranışını başta doğrula.
- LAN A/B'yi aynı subnet'e koyma; OT/IT segmentasyonunu koru (gateway zaten bu sınırda durur).
- IP22 — pano dışı/tozlu ortamda extreme (IP66) sürümü gerekir.
- iX runtime ↔ image versiyonu ve (SC ise) BCS Tools/CODESYS sürüm uyumu kontrol edilmeli.

## Doğrulanmamış / Boş Bırakılan

"A12" model adının resmi karşılığı doğrulanamadı. Güç tüketimi, fiziksel boyut, ağırlık,
depolama sıcaklığı, nem ve izolasyon değerleri 'A12' varyantı için resmi dokümandan teyit
edilmeli — tahmin edilmedi, null bırakıldı. Ekran alanları (size/resolution/touch) cihaz
displaysiz olduğu için null. Device description dosyası (EtherCAT ESI / Ethernet/IP EDS —
yalnızca SC master modunda) bağlanan cihaza göre temin edilir.
