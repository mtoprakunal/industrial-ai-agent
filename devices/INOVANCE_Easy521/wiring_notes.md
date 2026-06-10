# Inovance Easy521-0808TN — Kablolama ve Entegrasyon Notları

> Mühendislik özeti. Bağlayıcı değerler için resmi Inovance Easy Series broşürü /
> Easy521 User Manual ve cihaz etiketine bak. Boş değerler `datasheet.json`'da boş bırakıldı.

## Cihaz Ne İşe Yarar

Easy521, Inovance **Easy500 hareket-kontrol alt serisinin 8 eksenli** üyesidir
(Easy522=16 eksen, Easy523=32 eksen). Kompakt **EtherCAT master** PLC; 8 DI / 8 DO
yerleşiktir, EtherCAT + darbe ile 8 eksene kadar kontrol yapar, CAM ve enterpolasyon
destekler. Inovance **AutoShop** ile programlanır (CODESYS DEĞİL).

Model kodu çözümü: **08**=8 giriş, **08**=8 çıkış, **5**=EtherCAT'li, **2**=çift Ethernet,
**TN**=sink transistör. Sipariş kodu **01440385**.

## Portlar ve Yerleşik I/O

| Arayüz | İşlev |
|--------|-------|
| 2x Ethernet (RJ45) | Modbus TCP (master/client + slave/server), EtherNet/IP scanner/adapter, ağ geçişi |
| EtherCAT (RJ45) | Master; Easy500 alt serisi 72 slave'e kadar (senkron eksenler dahil) |
| RS485 | Modbus RTU/ASCII, serbest protokol |
| USB Type-C | Programlama, yükleme/indirme, debug |
| GE20 yuvaları (A/B) | RS232/485, CAN/485, analog (2AD1DA), dijital (4DI/4DO), RTC, TF kart |

- **8 DI**: seçilebilir sink/source.
- **8 DO**: TN = sink (NPN) transistör.
- 4 kanal enkoder ekseni (8 yüksek hızlı giriş, 200 kHz'e kadar).
- Güç: **DC 24V** (etiket: INPUT DC24V 1A, OUTPUT DC24V 0.5A res. load).
- I/O genişletme: yerel/uzak **GL20** modülleri (yaylı klemens, takım gerektirmez).

## Fieldbus Rolü

- **EtherCAT: MASTER.** SV630N/SV660N servoları, MD520/MD800 sürücüleri ve GL20-RTU-ECT
  uzak I/O coupler'larını slave olarak sürer.
- Modbus TCP hem master/client (32 slave'e kadar) hem slave/server (16 master'a kadar).
- CANopen/CANlink GE20 genişletme kartı gerektirir.

## CODESYS Entegrasyonu (DOLAYLI — Easy serisi CODESYS değildir)

Easy serisi (H5U gibi) **AutoShop** ile programlanır — CODESYS DEĞİL. Doğrudan CODESYS
runtime'ı yoktur.

**Yol A — Modbus TCP/RTU:** Easy521'i Modbus TCP server / RTU slave yap; CODESYS
master register'ları okusun/yazsın. Paylaşılacak değişkenleri register alanına eşle.

**Yol B — Ağ seviyesi:** Easy521 kendi EtherCAT slave ağını master olarak sürer; bu
segment ayrı tutulur (tek master kuralı). Üst seviye köprü Ethernet/Modbus TCP olur.

## Tuzaklar

- **GE20 kartları Easy301'e uygulanmaz** — Easy521'de slot A/B mevcuttur; kart-slot
  uyumunu (bazı kartlar yalnız A veya yalnız B) tabloyla teyit et.
- EtherCAT segmentinde **tek master**. CODESYS master'la aynı hatta koyma.
- 8 eksen sınırı: EtherCAT eksenleri + maks. 5 darbe ekseni dahil kombinasyon.
- CAN/CANopen için ayrı GE20-CAN-485 kartı gerekir (yerleşik CAN yok).
- DI sink/source ortak ucunu (NPN/PNP) doğru kabloyla bağla.

## Doğrulanmamış / Boş Bırakılan

CPU çalışma/depolama sıcaklığı (broşür CPU tablosunda yok; tahmin edilmedi), nem, güç
tüketimi ve izolasyon resmi kaynaktan teyit edilmeli. EtherCAT ESI dosyası AutoShop
kurulumundan gelir (`download_url` boş). Program/veri kapasitesi Easy500 alt serisi
genel değeridir; Easy521 birim teyidi için User Manual'a bak.
