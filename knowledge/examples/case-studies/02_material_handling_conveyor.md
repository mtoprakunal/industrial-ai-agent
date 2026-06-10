---
KONU        : Vaka Çalışması — Çok Bölgeli Malzeme Taşıma / Konveyör Hattı
KATEGORİ    : examples
ALT_KATEGORI: case-studies
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.interroll.com/products/controls/zonecontrol"
    başlık: "Interroll ZoneControl — birim taşıma sistemleri için bölge kontrolü"
    güvenilirlik: resmi
  - url: "https://www.bihl-wiedemann.de/us/applications/automation-technology/material-handling-drive-control/zpa-and-as-interface-a-smart-solution-for-controlled-material-flow"
    başlık: "ZPA & AS-Interface — kontrollü malzeme akışı (OPC-UA gateway)"
    güvenilirlik: resmi
  - url: "https://www.dnc-automation.com/motorised-roller-conveyor/"
    başlık: "Motorised Roller Conveyor: MDR Zones, ZPA Accumulation (S7-1500 + OPC-UA WMS/MES)"
    güvenilirlik: topluluk
  - url: "https://www.manula.com/manuals/pulseroller/conveylinx-plc-developers-guide/1/en/topic/plc-controller-with-zpa-mode"
    başlık: "ConveyLinx PLC Developers Guide — ZPA Mode Control"
    güvenilirlik: topluluk
  - url: "knowledge/applications/conveyor/README.md"
    başlık: "Konveyör Sistemleri Otomasyonu — İç Bilgi Tabanı (FB_Conveyor, durdurma kategorileri)"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/_synthesis.md"
    başlık: "Protokol Sentezi — eksen/ilke çerçevesi"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/applications/conveyor/README.md"
    ilişki: detaylandırır
  - konu: "knowledge/protocols/modbus-tcp/_synthesis.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/opc-ua/_synthesis.md"
    ilişki: kullanır
  - konu: "knowledge/decisions/architecture/README.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "FB_Conveyor / FB_Motor durum makinesi (applications/conveyor/README.md)"
  - "Durdurma kategorileri (Cat-0/1/2) ve interlock kavramı"
  - "Protokol seçim çerçevesi (decision_framework.md §1)"
ÇELİŞKİLER :
  - kaynak: "ZPA modül üreticileri vs. merkezi PLC yaklaşımı"
    konu: "Bölge mantığı akıllı MDR kartında mı yoksa merkezi PLC'de mi olmalı?"
    çözüm: >
      İkisi de geçerli mimari. Akıllı MDR kartları (ConveyLinx, Interroll) bölge ZPA
      mantığını dağıtır; merkezi PLC tüm bölgeyi tek mantıkta toplar. Seçim, hat
      uzunluğu, esneklik ve bakım ekibinin yetkinliğine bağlıdır (bkz. Mimari karar).
---

## Özün Ne

Çok bölgeli malzeme taşıma hattı, paket/koli/tepsi gibi birimleri bir noktadan diğerine
**çarpışmadan, sıralı ve geri-basınçsız (ZPA)** taşıyan bir konveyör sistemidir. Mühendislik
özü tek bir motoru sürmek değil, **bölgeler arası el-sıkışma (handshake) ve interlock**
kurmaktır: bir birim, ileri bölge "boş" sinyali vermeden bir sonraki bölgeye geçemez. Bu
vaka, "konveyör hattı yap" gereksinimini bölge mimarisi + sıralama mantığı + üst sistem
(WMS/MES) protokol seçimine çevirir.

Neden önemli: Konveyör hatları nadiren tek başına çalışır; bir WMS/MES birime nereye
gideceğini söyler, hat da gerçek konum/durumu geri raporlar. Yani burada iki ayrı problem
var: (1) saha seviyesinde deterministik bölge kontrolü, (2) üst seviyede zengin, çift
yönlü sipariş/durum alışverişi. Bunlar farklı protokol eksenlerinde çözülür.

## Nasıl Çalışır

Bir ZPA (Zero Pressure Accumulation) hattının fonksiyonel yapısı:

- **Bölge (zone):** Her bölgede en az bir sensör (birim var/yok) ve bir tahrik (MDR
  motorlu rulo veya VFD'li bölüm) bulunur. Kaynak (Bihl+Wiedemann; Interroll) bölgeyi
  "sensör + motor rulo + taşıyıcı rulolar" olarak tanımlar.
- **Handshake mantığı:** Bir birim X bölgesinde algılanır; X, ileri bölge X+1 "boş" ise
  birimi serbest bırakır, değilse durdurur ve geri (X-1) bölgeye "dolu, gönderme" sinyali
  verir. Birikme yukarı doğru zincirleme yayılır (accumulation).
- **Sıralama (sequencing):** Birleşme (merge), ayrılma (divert/sorter), indeksleme noktaları
  birim sırasını ve önceliğini yönetir. Sorter, WMS'ten gelen hedefe göre birimi doğru kola
  yönlendirir.
- **Interlock:** Emniyet kapısı/e-stop bir bölgeyi (veya tüm hattı) durdurur; downstream
  dolu, jam (sıkışma), motor arızası gibi durumlar upstream'i durdurur.
- **Üst sistem köprüsü:** WMS/MES birime barkod/hedef atar; hat birim sayımı, bölge durumu,
  jam/arıza diagnostiğini geri raporlar (kaynak: DNC Automation — S7-1500 + OPC-UA WMS/MES).

## Pratikte Nasıl Kullanılır

**Gereksinim listesi (girdi):**
1. N bölge, her birinde sensör + tahrik; geri-basınçsız birikme.
2. Bölgeler arası handshake + jam algılama.
3. En az bir divert/merge (sıralama/yönlendirme) noktası.
4. Bölge bazlı e-stop / emniyet kapısı interlock'u.
5. WMS/MES ile sipariş (hedef) + durum/sayım alışverişi.
6. Bazı bölgelerde legacy VFD veya akıllı MDR kartı bulunabilir.

**Mimari karar (KARAR/GEREKÇE/TAKAS):**

```
KARAR:   Merkezi PLC, bölge mantığını FB_Zone örnekleriyle yürütür; tahrikler MDR
         (dijital start/stop + hız) veya VFD üzerinden sürülür.
GEREKÇE: Hat orta uzunlukta, sıralama/divert merkezi koordinasyon ister; tek noktada
         mantık bakım ve değişimi kolaylaştırır. FB_Conveyor/FB_Motor tabanı hazır.
ALT:     Dağıtık akıllı MDR (ConveyLinx/Interroll) — çok uzun, modüler, sık genişleyen
         hatta her bölge kendi ZPA'sını yürütür; PLC sadece koordine eder. Esneklik artar,
         merkezi görünürlük azalır.
TAKAS:   Merkezi PLC tek hata noktasıdır; CPU yükü ve I/O kablajı artar. Bölge sayısı
         büyürse dağıtık modele kayılır.
```

```
KARAR:   Protokol: Saha = bölge I/O için yerel/uzak dijital + (legacy tahrik) Modbus TCP;
         üst sistem (WMS/MES) = OPC-UA.
GEREKÇE: decision_framework §1: legacy VFD/sayaç → Modbus (basit register, evrensel);
         WMS sipariş + zengin durum + çift yönlü → OPC-UA (struct, keşif, güvenlik).
ALT:     Her şeyi Modbus ile yapmak; WMS tarafında hedef/lot/diagnostik verisi 16-bit
         register'a sığmaz, tipsizlik ve adres yönetimi kâbusa döner → OPC-UA seçildi.
TAKAS:   İki protokol bakımı; Modbus güvenliksiz olduğundan OT ağı segmentasyonu zorunlu
         (IEC 62443). OPC-UA kurulum yükü WMS entegrasyonunda amorti olur.
```

**Task / protokol / HMI eşlemesi:**

| Mantık | Task | Cycle | Protokol/Arayüz |
|--------|------|-------|------------------|
| E-stop / emniyet kapısı | Donanımsal emniyet + Safety task | ≤1 ms | Donanım (PLC dışı) |
| Bölge handshake, jam interlock | Task_Fast | ≤4 ms | Yerel/uzak DI/DO |
| Divert/merge sıralama | Task_Control | 10 ms | DI/DO + (sorter) |
| Legacy VFD bölge tahriki | Task_Control / Task_Comm | 10–50 ms | Modbus TCP master |
| WMS/MES sipariş + durum | Task_Comm | ≤200 ms | OPC-UA server |
| Throughput/OEE → bulut | Task_Background (Freewheeling) | best-effort | MQTT (ops.) |

## Örnekler

- **Bölge serbest bırakma (FB_Zone):** `IF urun_var AND ileri_bolge_bos THEN tahrik_calistir;
  ELSIF urun_var AND NOT ileri_bolge_bos THEN tahrik_dur; END_IF`. Tüm bölgeler aynı FB'nin
  örnekleridir; sadece komşu bölge referansları farklıdır (tek-yazar disiplini: her bölgenin
  tahrikini yalnız kendi FB'si yazar).
- **Jam (sıkışma) algılama:** Bölge sensörü beklenen sürede temizlenmezse (timeout) jam
  alarmı; o bölge ve upstream durur, downstream boşalmaya devam eder.
- **WMS divert kararı:** Birim barkodu okunur → OPC-UA ile WMS'ten hedef kol döner → divert
  bölgesi birimi ilgili kola yönlendirir; gerçek sonuç (yönlendirildi/hata) geri raporlanır.

## Sık Yapılan Hatalar

- **Bölge handshake'inde tek-yazar ihlali.** İki bölgenin aynı tahrik/bayrağı yazması yarış
  koşulu ve titreşimli start/stop üretir. Her bölgenin çıkışını yalnız kendi FB'si yazar.
- **Jam timeout'unu test etmemek.** Timeout yoksa sıkışan birim sonsuza dek motoru zorlar;
  motor/sigorta arızası. Her bölgede süre denetimi şarttır.
- **WMS verisini Modbus register'a sıkıştırmak.** Hedef/lot/öncelik gibi yapısal veri için
  Modbus yanlış eksen; adres haritası şişer, tipsizlik hataya yol açar → OPC-UA.
- **Modbus'u düz fabrika ağına koymak.** Modbus'ta kimlik doğrulama yok; OT/IT segmentasyonu
  ve VLAN olmadan açmak güvenlik açığıdır (decision_framework §1, üç ilke).
- **E-stop'u yazılım interlock'una indirgemek.** Bölge durdurma mantığı emniyet değildir;
  e-stop ve kapı donanımsal kategori-0/1 durdurma sağlamalı (bkz. conveyor/README durdurma
  kategorileri).

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Merkezi PLC + Modbus(legacy)+OPC-UA(WMS) tercih:** Orta uzunlukta, sıralama/divert içeren,
  WMS/MES'e bağlı tipik dağıtım/üretim besleme hatlarında.
- **Dağıtık akıllı MDR tercih:** Çok uzun, sık değişen/genişleyen, modüler kurulumlarda;
  her bölge kendi ZPA'sını yürütür, kablaj ve merkezi CPU yükü azalır.
- **Etmemeli:** Tek motorlu kısa bir taşıma bandı için bölge mimarisi gereksizdir; basit
  start/stop + emniyet yeterli.

## Gerçek Proje Notları

- Hattın "tıkanması" çoğu zaman en yavaş downstream noktasındaki bir darboğazdan kaynaklanır;
  birikme upstream'e doğru yayılır. Sorun bölgesini bulmak için bölge doluluk/bekleme
  sürelerini loglamak şarttır.
- Sensör seçimi sessiz başarısızlık kaynağıdır: yansıtıcı koliyle difüz sensör yanlış okur;
  birim rengi/yüzeyi değişen tesiste sensör tipi baştan test edilmeli.
- WMS entegrasyonunda en büyük gecikme protokol değil, anlam karmaşasıdır: "birim X bölgeye
  girdi" olayının tanımı iki taraf arasında netleşmezse sayımlar tutmaz. OPC-UA namespace'i
  bu olayları açık modelle tanımlamak için kullanılır.
- Legacy VFD'ler Modbus RTU adres/baud çakışmalarıyla gelir; TCP'ye geçişte gateway
  kullanılıyorsa poll periyodu kontrol task'ını bloke etmemeli (Freewheeling/Comm task).

## İlgili Konular

- `knowledge/applications/conveyor/README.md` — FB_Conveyor, durdurma kategorileri (taban)
- `knowledge/protocols/modbus-tcp/_synthesis.md` — legacy tahrik bağlantısı
- `knowledge/protocols/opc-ua/_synthesis.md` — WMS/MES köprüsü
- `knowledge/decisions/architecture/README.md` — merkezi vs. dağıtık karar
- `knowledge/examples/case-studies/01_packaging_machine.md` — komşu makineye besleme
