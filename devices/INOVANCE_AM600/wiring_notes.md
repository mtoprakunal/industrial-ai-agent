# Inovance AM600 — Kablolama ve Entegrasyon Notları

> Mühendislik özeti. Bağlayıcı değerler için resmi Inovance AM600 broşürü ve cihaz
> etiketine bak. Bulunamayan değerler `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

AM600, **yerleşik PLC işlevli merkezi hareket kontrolörüdür** (modüler). EtherCAT
master olarak 32 eksene kadar pozisyonlama, 8 eksene kadar enterpolasyon, 16 eksene
kadar CAM yapar. CPU + güç modülü (GL10-PS2) + 16'ya kadar genişletme modülünden
oluşur. **Inovance'ın CODESYS tabanlı InoProShop** ortamıyla programlanır (IEC 61131-3).

## Sistem Yapısı

```
GL10-PS2 (220VAC→24VDC)  +  AM600 CPU  +  16'ya kadar GL10 yerel modül
                                |
                          EtherCAT bus → GR10 uzak modüller / GL10-RTU-ECTA coupler / SV660N servolar
```

## Portlar ve Yerleşik I/O (AM600-CPU1608TP/TN)

| Arayüz | İşlev |
|--------|-------|
| EtherCAT (RJ45) | Master; 125 slave istasyona kadar. CiA 402 (CSP/CSV/CST/HM/PP/PV/PT). |
| Ethernet (RJ45) | Modbus TCP master/slave, EtherNet/IP scanner/adapter, OPC UA server |
| 2x RS485 | Modbus RTU master/slave |
| CAN | CANopen master, CANlink master/slave |
| USB / SD | Programlama / saklama |

- **16 yüksek hızlı giriş / 8 yüksek hızlı çıkış** (TP=source/PNP, TN=sink/NPN).
- 8 kanal A/B faz sayacı (200 kHz), 4 grup 200 kHz pozisyonlama darbe çıkışı.
- Güç: CPU **+24 VDC**; GL10-PS2 güç modülü 220 VAC giriş → 24 VDC/2 A.
- **TP tipi** harici FCN bağlantı kablosu (X210-5-X.X) ve T024-K klemens bloğu ister;
  **TN tipi** çıkarılabilir yaylı klemensle gelir.

## Fieldbus Rolü

- **EtherCAT: MASTER.** SV660N servoları, GR10/GL20 uzak I/O ve üçüncü taraf CiA 402
  cihazlarını sürer.
- CANopen **master**, CANlink master/slave, Modbus RTU/TCP master/slave.
- OPC UA **server**, EtherNet/IP **scanner/adapter**.

## CODESYS Entegrasyonu (DOĞRUDAN — InoProShop CODESYS tabanlıdır)

AM600, Inovance'ın diğer PLC'lerinden farklı olarak **CODESYS tabanlı InoProShop**
ile programlanır. Inovance 2015'ten beri CODESYS GmbH ile çalışır.

1. **InoProShop**'ta proje aç; dili seç (ST/LD/SFC/CFC).
2. Network Configuration'da EtherCAT master'ı yapılandır; SV660N ve GL20/GR10
   slave'lerini ESI ile ekle (drag&drop), PDO eşle.
3. **PLCopen Motion** kütüphanesi ile eksenleri programla (MC_MoveAbsolute,
   MC_CamTableSelect, MC_CamIn vb.); CAM tablosunu grafik editörle oluştur.
4. Üst sisteme OPC UA server / Modbus TCP ile bağlan.

> Not: InoProShop CODESYS tabanlıdır ama Inovance'a özel dağıtımdır; standart CODESYS
> IDE'siyle birebir aynı değildir. Inovance cihaz açıklama dosyaları (ESI) InoProShop
> kurulumuyla gelir.

## Tuzaklar

- EtherCAT segmentinde **tek master** (AM600). İkinci master ekleme.
- TP tipi CPU için harici I/O kablosu + klemens bloğu (T024-K) zorunlu — sipariş ederken unutma.
- GR10 uzak modüller **harici 24 VDC** besleme ister.
- CANopen ve CANlink aynı CAN portunda; protokol seçimini netleştir.
- Senkronizasyon periyodu (CAM 2 ms, PTP 4 ms refresh) eksen sayısına göre planla.

## Doğrulanmamış / Boş Bırakılan

Çalışma/depolama sıcaklığı, nem, IP sınıfı, ağırlık, güç tüketimi, izolasyon ve RAM
resmi kaynaktan teyit edilmeli. ESI dosyası InoProShop kurulumundan gelir
(`download_url` boş).
