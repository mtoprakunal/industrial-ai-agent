# Inovance GL20 (GL20-RTU-ECT) — Kablolama ve Entegrasyon Notları

> Mühendislik özeti. Bağlayıcı değerler için resmi Inovance GL20 broşürü ve modül
> etiketlerine bak. Boş değerler `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

GL20, Inovance'ın **yeni nesil ince/kompakt dağıtık I/O sistemidir** (iF Design Award
2022). Bir **bus coupler** (EtherCAT: GL20-RTU-ECT, sipariş kodu 1440286 / PROFINET:
GL20-RTU-PN) arkasına **16 modüle kadar** DI/DO/AI/AO/sıcaklık modülü takılır. GL10'a
göre %66 kabin alanı tasarrufu (modüller 12 mm kalınlığa kadar). Programlanmaz —
saf I/O slave'idir.

## Coupler Spesifikasyonu (GL20-RTU-ECT)

| Özellik | Değer |
|---------|-------|
| Fieldbus rolü | EtherCAT **SLAVE** |
| EtherCAT port | 2x RJ45 (IN/OUT), 100 Mbit/s tam dupleks, 100 m |
| Min. çevrim | 125 µs |
| Process data | 1024 girdi + 1024 çıktı bayta kadar |
| Mailbox | 256 + 256 bayt (CoE: PDO/SDO) |
| Maks. modül | 16 genişletme modülü |
| Besleme | +24 VDC (A&B 2 kanal terminal) |
| Firmware | USB-C portu |
| Boyut | 24 x 100 x 83 mm |
| Koruma | Aşırı akım / ters bağlantı; IP20; -20~55 °C; <%95 yoğuşmasız |

## Modül Çeşitleri (özet)

- **DI:** GL20-0800END (8), GL20-1600END (16), GL20-3200END-M (32) — PNP/NPN, filtre 0.25–32 ms.
- **DO:** GL20-0008/0016/0032 ETN(NPN)/ETP(PNP) transistör, yanıt 100 µs; GL20-0008ER röle (15 ms).
- **DI/DO kombo:** GL20-0808ETN, GL20-3232ETN-M.
- **AI:** GL20-4AD (4 kanal, 16 bit, 250 µs). **AO:** GL20-4DA (4 kanal, 16 bit, 250 µs).
- **Sıcaklık:** GL20-4PT (RTD), GL20-4TC (termokupl).
- 32 kanal modüller (3200END/0032ETN-M/3232ETN) FCN kablosu + T024-K klemens bloğu ister.

## Fieldbus Rolü

- **SLAVE.** Bir EtherCAT (veya PROFINET) master'a bağlanır; kendisi master değildir.
- DI/DO donanım yanıtı ~100 µs; AI/AO örnekleme 250 µs — senkron, hızlı I/O.

## CODESYS Entegrasyonu (DOLAYLI — slave olarak)

GL20-RTU-ECT, **EtherCAT slave** olduğu için herhangi bir EtherCAT master'a eklenir:

1. Master tarafında (Inovance AM600/H5U/Easy ya da **üçüncü taraf CODESYS master**)
   EtherCAT yapılandırmasına GL20-RTU-ECT'yi **ESI dosyası** ile ekle.
2. Coupler arkasındaki modülleri tara/ekle; **PDO eşlemesiyle** I/O verisini oku/yaz.
3. EtherCAT **alias** master üzerinden 1–65535 aralığında ayarlanır.

> CODESYS tabanlı bir master ile sorunsuz çalışır (dolaylı uyum): GL20 bir I/O cihazı,
> mantık master'da yazılır. ESI dosyasını Inovance destek/master kurulumundan temin et.

## Tuzaklar

- **Coupler arkasındaki modüller alias erişimini desteklemez** — yalnız coupler alias alır.
- Bus coupler başına en fazla **16 modül**; daha fazlası için ek coupler ekle.
- 24 VDC besleme A&B iki kanal; akım bütçesini modül sayısına göre hesapla.
- 32 kanal modüller daha büyük gövde + FCN kablo/klemens ister (siparişte unutma).
- DIN ray montajı ürün merkez çizgisinin 5 mm altında; mandalı gevşetmek için üstte
  en az 10 mm boşluk bırak.

## Doğrulanmamış / Boş Bırakılan

Ağırlık, güç tüketimi (modül başına akım), depolama sıcaklığı ve modül-bazlı detaylı
elektriksel değerler resmi kaynaktan teyit edilmeli. ESI dosyası master kurulumundan
gelir (`download_url` boş).
