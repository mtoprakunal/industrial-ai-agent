---
KONU        : ISA-95 Hiyerarşisi ve Otomasyon Piramidi
KATEGORİ    : examples
ALT_KATEGORI: reference-arch
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard"
    başlık: "ISA-95 Standard — Enterprise-Control System Integration (ISA resmi)"
    güvenilirlik: resmi
  - url: "https://blog.ansi.org/ansi/ansi-isa-95-00-01-2025-enterprise-control-system/"
    başlık: "ANSI/ISA-95.00.01-2025: Enterprise Control System Integration — ANSI Blog"
    güvenilirlik: resmi
  - url: "https://www.siemens.com/en-us/technology/isa-95-framework-layers/"
    başlık: "ISA-95 Framework and Layers — Siemens"
    güvenilirlik: topluluk
  - url: "https://excelpro.ca/en/news/the-automation-pyramid-isa-95"
    başlık: "The Automation Pyramid (ISA-95): Levels, Functions and Benefits — Excelpro"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/examples/reference-arch/02_uns_sparkplug_b.md"
    ilişki: alternatif
  - konu: "knowledge/examples/reference-arch/04_namur_open_architecture.md"
    ilişki: tamamlar
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/mqtt/02_industrial_usage.md"
    ilişki: tamamlar
  - konu: "knowledge/standards/02_iec62443.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "PLC / SCADA / MES / ERP terimlerine genel aşinalık"
  - "OT/IT ayrımı kavramı (knowledge/standards/_synthesis.md)"
ÇELİŞKİLER :
  - kaynak: "ISA-95 katı piramit vs UNS düz mimari söylemi"
    konu: "Bazı kaynaklar 'piramit öldü, UNS geldi' der; bu yanıltıcıdır"
    çözüm: >
      ISA-95 iki ayrı şey tanımlar: (1) fonksiyonel seviye MODELİ (L0-L4) ve
      (2) seviyeler arası veri DEĞİŞİM modeli. UNS, fonksiyonel seviyeleri
      reddetmez; yalnızca seviyeler arası katı nokta-nokta veri akışını broker
      üzerinden düzleştirir. ISA-95 hiyerarşisi UNS topic ağacında (Enterprise/
      Site/Area/Line/Cell) yaşamaya devam eder. Bkz. 02_uns_sparkplug_b.md.
---

## Özün Ne

ISA-95 (uluslararası karşılığı IEC/ISO 62264), kurumsal iş sistemleri (ERP) ile üretim
kontrol sistemleri (PLC/SCADA/MES) arasındaki entegrasyonu standartlaştıran bir model
ve terminoloji ailesidir. İki temel katkısı vardır: (1) bir fabrikayı **beş fonksiyonel
seviyeye** (L0-L4 — "otomasyon piramidi") ayıran kavramsal model ve (2) özellikle
**L3 (MES) ile L4 (ERP) arasındaki arayüzü** tanımlayan, teknolojiden bağımsız nesne/
mesaj modelleri. Standart, ANSI/ISA-95.00.01 ile başlayan çok parçalı bir seridir
(en güncel temel parça: 95.00.01-2025).

Neden önemli: Bir endüstriyel sistem tasarlarken "hangi bilgi hangi katmanda üretilir,
hangi katmana, hangi gecikme ve güvenlik gereksinimiyle akar?" sorusunun ortak dili
ISA-95'tir. Bir agent mimari kararı verirken (protokol seçimi, segmentasyon, veri
modeli) hemen her endüstriyel müşterinin kafasındaki zihinsel harita budur. Bu yüzden
ISA-95 seviyelerini doğru konumlandırmak, OPC UA / MQTT / fieldbus seçimlerini
gerekçelendirmenin temelidir.

## Nasıl Çalışır

### Beş Seviye (Otomasyon Piramidi)

```
        ┌───────────────────────────────────────────┐
  L4    │  ERP — İş Planlama & Lojistik             │  Gün/hafta/ay
        │  Sipariş, planlama, finans, tedarik        │  IT alanı
        ├───────────────────────────────────────────┤
  L3    │  MES / MOM — Üretim Operasyon Yönetimi     │  Vardiya/saat
        │  Çizelgeleme, kalite, izlenebilirlik,      │  OT↔IT köprüsü
        │  reçete, OEE, batch                        │
        ├───────────────────────────────────────────┤
  L2    │  SCADA / DCS — İzleme & Süpervizör Kontrol │  Saniye/dakika
        │  HMI, alarm, trend, setpoint yönetimi      │  OT alanı
        ├───────────────────────────────────────────┤
  L1    │  PLC / Kontrolör — Sensör/Aktüatör Kontrol │  ms
        │  Mantık, regülasyon, kapalı çevrim          │  OT alanı
        ├───────────────────────────────────────────┤
  L0    │  Fiziksel Proses — Makine, Saha, Akış      │  Sürekli/µs
        └───────────────────────────────────────────┘
   Tabandan tepeye: veri hacmi azalır, soyutlama ve zaman ufku artar.
```

- **L0 — Fiziksel proses:** Gerçek makine, akışkan, mekanik. Otomasyonun "yönettiği şey".
- **L1 — Sensör/aktüatör ve kontrol:** Ölçüm ve manipülasyon; PLC kapalı çevrim regülasyon.
  Determinizm ve milisaniye döngü burada kritiktir (EtherCAT, PROFINET, CANopen alanı).
- **L2 — İzleme/süpervizör:** SCADA/DCS, HMI, alarm yönetimi, operatör setpoint'leri.
- **L3 — MES/MOM:** Üretim emirlerini fiili üretime çevirir; çizelgeleme, kalite,
  izlenebilirlik, batch, OEE. **OT ile IT'nin buluştuğu köprü katman.**
- **L4 — ERP:** Sipariş, malzeme planlama (MRP), finans, lojistik. Saf IT alanı.

Tabandan tepeye çıkıldıkça veri hacmi düşer, zaman ufku uzar (ms → ay), soyutlama artar.
ISA-95 piramidi bu yüzden tabanı geniş çizilir: alt seviyelerdeki devasa ham veri yukarı
çıktıkça özetlenir.

### Standardın Asıl Odağı: L3↔L4 Arayüzü

ISA-95'in *standardlaştırdığı* asıl şey piramit resmi değil — o yalnızca yaygın bir
zihinsel modeldir — **L3 ve L4 arasındaki bilgi değişimidir** [DOĞRULANMADI: piramit
çiziminin tam sürüm-resmiliği parçaya göre değişebilir, kavram ikincil kaynaklarda tutarlı].
Standart, üretim ile iş sistemleri arasında değiş tokuş edilen nesneleri (örn. üretim
çizelgesi, üretim performansı, malzeme, personel, ekipman) ve bunların öznitelik
modellerini tanımlar. Parça yapısı (özetle):

| Parça | Odak |
|-------|------|
| 95.00.01 | Modeller ve terminoloji |
| 95.00.02 | Kurumsal-kontrol entegrasyonu nesne/öznitelikleri |
| 95.00.03 | Üretim operasyon yönetimi aktivite modelleri (L3 içi) |
| 95.00.04 | MOM entegrasyonu nesne/öznitelikleri |
| 95.00.05 | İş-üretim (B2M) işlemleri |
| 95.00.06+ | Mesajlaşma servis modeli, alias servisi, bilgi değişim profilleri |

Pratikte L3↔L4 değişimi sıklıkla **B2MML** (ISA-95'in XML şeması) ile somutlaştırılır.

## Pratikte Nasıl Kullanılır

ISA-95 bir ürün değil, bir tasarım çerçevesidir. Pratik kullanım adımları:

1. **Sistemi seviyelere haritala.** Eldeki bileşenleri (sensör, PLC, SCADA, MES, ERP)
   L0-L4'e yerleştir. Bu, hangi protokolün nereye ait olduğunu netleştirir.
2. **Veri akış sınırlarını çiz.** Hangi veri yukarı (raporlama) hangi veri aşağı (komut/
   reçete) akıyor? L1↔L2 fieldbus/OPC UA; L2↔L3 OPC UA/SQL/REST; L3↔L4 B2MML/REST/mesaj kuyruğu.
3. **Topic/tag isimlendirmeyi ISA-95 hiyerarşisiyle yap.** MQTT veya historian tag ağacı
   `enterprise/site/area/line/cell/device/datapoint` şemasını izlemeli (bkz. mqtt KB).
4. **Güvenlik bölgelerini seviyelerle hizala.** IEC 62443 Zone/Conduit modeli doğal olarak
   ISA-95 seviye sınırlarına oturur (özellikle L3.5 — OT/IT arası DMZ).

## Örnekler

**Örnek 1 — Bir sıcaklık değerinin yolculuğu (raporlama yönü):**
```
L0  Reaktör sıvısı 82.5 °C
L1  Transmitter → PLC AI; PLC kapalı çevrim PID (10 ms)
L2  SCADA OPC UA ile PLC'den okur, trend/alarm (500 ms)
L3  MES batch kaydına "ortalama sıcaklık" olarak yazar (vardiya)
L4  ERP yalnızca "Lot #1234 üretildi, spesifikasyon içinde" görür (gün)
```
Aynı fiziksel olgu her seviyede farklı soyutlamada temsil edilir.

**Örnek 2 — Bir üretim emrinin yolculuğu (komut yönü):**
```
L4  ERP: "500 adet ürün X üret" (satış siparişinden)
L3  MES: emri çizelgeye böler, reçete + makine atar, malzeme rezerve eder
L2  SCADA: operatöre reçeteyi sunar, batch'i başlatır
L1  PLC: reçete parametreleriyle sekansı yürütür
L0  Makine fiziksel olarak üretir
```

## Sık Yapılan Hatalar

- **Seviyeleri atlayan doğrudan bağlantılar.** ERP'nin doğrudan PLC'ye yazması (L4→L1)
  hem güvenlik hem bakım kâbusudur; ISA-95 bu akışı L3 üzerinden disipline eder.
  Raporlama ≠ kontrol: yukarı katmandan gelen istek asla denetimsiz biçimde RT kontrole
  yazmamalı (bkz. NOA "verification of request", 04_namur_open_architecture.md).
- **L3 ile L2'yi karıştırmak.** SCADA (L2, gerçek zamanlı izleme/kontrol) ile MES (L3,
  üretim yönetimi/çizelgeleme) farklı sorumluluklardır. Tek araçta birleştirilse bile
  fonksiyon ayrımı korunmalı.
- **Piramidi protokol reçetesi sanmak.** ISA-95 hangi protokolü kullanacağını söylemez;
  yalnızca nereye hangi tip bilgi aktığını çerçeveler. Protokol seçimi ayrı bir karardır.
- **"Piramit öldü" söylemini yanlış anlamak.** UNS, fonksiyonel seviyeleri kaldırmaz;
  yalnızca seviyeler arası katı nokta-nokta bağımlılığı broker'la gevşetir (bkz. ÇELİŞKİLER).

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih:** Her endüstriyel entegrasyon konuşmasının ortak dili olarak. ERP/MES
  entegrasyonu, izlenebilirlik, çoklu-tesis raporlaması tasarlanırken. Güvenlik
  bölgelemesini (IEC 62443) seviyelere oturtmak için.
- **Tek başına yetersiz:** ISA-95 *nasıl* iletileceğini (protokol, payload, gerçek zamanlılık)
  söylemez. Onu OPC UA (L1-L3 semantik veri), MQTT/UNS (L2-L4 veri dağıtımı), fieldbus
  (L0-L1 RT) ve IEC 62443 (güvenlik) ile birlikte kullan.
- **Katı piramidi dogma yapmak:** Modern mimarilerde (UNS, NOA) seviyeler korunur ama
  veri akışı düz/broker-merkezli olabilir. ISA-95'i model olarak tut, katı tek-yön
  veri yolunu zorunluluk sanma.

## Gerçek Proje Notları

- **L3.5 (OT/IT DMZ) çoğu projede en kritik ve en ihmal edilen sınırdır.** ISA-95
  seviyeleri ile IEC 62443 Zone'larını çakıştırınca, MES ile SCADA arasına bir
  güvenlik DMZ'i (data diode / broker / OPC UA aggregating server) koymak doğal hale gelir.
- **Agent için pratik kural:** Bir müşteri "PLC verisini ERP'ye bağla" derse, doğru yanıt
  doğrudan bağlantı değil — L3 (MES/historian/broker) üzerinden katmanlı bir yol önermektir.
  Bu hem ISA-95 hem IEC 62443 ile uyumludur.
- **Topic/tag isimlendirme borcunun maliyeti yüksektir.** ISA-95 tabanlı isimlendirme baştan
  kurulmazsa, ölçek büyüdüğünde tüm historian/dashboard yeniden eşlenir (bkz. mqtt KB,
  Gerçek Proje Notları "topic değişikliğinin 2 günlük maliyeti").

## İlgili Konular

- `02_uns_sparkplug_b.md` — ISA-95 hiyerarşisinin UNS topic ağacında yaşaması; piramidin "düzleştirilmesi"
- `04_namur_open_architecture.md` — Piramidi bozmadan ikinci kanalla veri açma (M+O)
- `03_opcua_companion_specs.md` — Bir ISA-95 companion spec'i de vardır (kurumsal entegrasyon modeli)
- `knowledge/standards/02_iec62443.md` — Zone/Conduit'in ISA-95 seviyelerine oturması
- `knowledge/protocols/mqtt/02_industrial_usage.md` — ISA-95 tabanlı topic tasarımı
- `knowledge/protocols/opc-ua/01_architecture.md` — OPC UA'nın endüstriyel katman rolü
