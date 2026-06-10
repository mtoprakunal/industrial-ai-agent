---
KONU        : Vaka Çalışması — Yatay Akış Paketleme Makinesi (Flow Wrapper)
KATEGORİ    : examples
ALT_KATEGORI: case-studies
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://timoxtoby.co.uk/case-studies/servos-revolutionise-packaging-machinery/"
    başlık: "Servos Revolutionise Packaging Machinery — film/infeed/crimp eksen senkronizasyonu"
    güvenilirlik: topluluk
  - url: "https://www.packagingdigest.com/flexible-packaging/flow-wrapping-basics-how-does-it-work-"
    başlık: "How Does a Flow Wrap Machine Work? — Packaging Digest"
    güvenilirlik: topluluk
  - url: "https://www.omac.org/packml"
    başlık: "PackML — OMAC Packaging Workgroup (durum makinesi standardı)"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/fileadmin/downloads/Brochures/EN/AM600_Br_EN_Singles_Web_V2.2.pdf"
    başlık: "Inovance AM600 Motion Controller broşürü (EtherCAT, CAM, 32 eksen)"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/fileadmin/downloads/Servo_drives_and_motors/SV660N_Advanced_User_Guide.pdf"
    başlık: "Inovance SV660N Advanced User Guide (CiA 402, ~125 µs çevrim)"
    güvenilirlik: resmi
  - url: "knowledge/applications/packaging/README.md"
    başlık: "Paketleme Makineleri Otomasyonu — İç Bilgi Tabanı (PackML/SFC/recipe)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/task-structure/_synthesis.md"
    başlık: "CODESYS Task Yapısı Sentezi — motion/control/comm ayrımı"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/applications/packaging/README.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/task-structure/_synthesis.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/_synthesis.md"
    ilişki: kullanır
  - konu: "devices/INOVANCE_AM600"
    ilişki: kullanır
  - konu: "devices/INOVANCE_SV660N"
    ilişki: kullanır
ÖNKOŞUL     :
  - "PackML durum makinesi ve recipe kavramı (applications/packaging/README.md)"
  - "EtherCAT CiA 402 eksen ve PLCopen MC_ FB temel bilgisi"
  - "Task atama mantığı (decision_framework.md §2)"
ÇELİŞKİLER :
  - kaynak: "Pazarlama metinleri ('1000 paket/dk')"
    konu: "Yüksek hız iddiaları makine/ürün/film tipine göre değişir"
    çözüm: >
      Hız hedefi her zaman ürün boyutu, film cinsi ve sızdırmazlık süresiyle
      sınırlıdır. Vakada somut sayı yerine 'gereksinim → eksen sayısı → çevrim
      süresi' zinciri kurulur; nihai hız saha kabul testinde doğrulanır [DOĞRULANMADI].
---

## Özün Ne

Yatay akış paketleme makinesi (HFFS / flow wrapper), sürekli akan bir film borusunun
içine ürünü besleyip enine sızdırmazlık (crimp/jaw) yaparak tek tek paket üreten bir
makinedir. Mühendislik açısından özü **üç eksenin tek bir sanal master'a senkron
kilitlenmesidir**: ürün besleme (infeed), film besleme (film feed) ve sızdırmazlık
çenesi (crimp/sealing jaw). Bu üçü mekanik mil yerine elektronik CAM ile senkronlanır;
film üzerindeki baskı işaretleri (print/registration mark) faz düzeltmesiyle pakete
hizalanır. Bu vaka, "paketleme makinesi yap" gereksinimini somut bir mimari + protokol
+ task eşlemesine çevirir.

Neden önemli: Paketleme, motion + makine durumu (PackML) + üretim raporlama (MES) üç
katmanı tek makinede buluşturur. Bu üç katmanın her biri farklı bir protokol ekseninde
çözülür — yanlış katmana yanlış protokol koymak en sık görülen tasarım hatasıdır.

## Nasıl Çalışır

Tipik bir servo flow wrapper'ın fonksiyonel mimarisi:

- **Sanal master (virtual axis):** Makine hızını temsil eden yazılım ekseni. Tüm gerçek
  eksenler bu master'a CAM/gear ile bağlanır. Hız değişince tüm eksenler oranını korur.
- **Infeed ekseni:** Ürünü film borusuna doğru zamanlı iter (lug/flight bar veya
  servo-konveyör). Master pozisyonuna göre CAM profili.
- **Film besleme ekseni:** Filmi forming box'tan çeker. Print mark sensörü her pakette
  baskı işaretini görür; gerçek işaret ile beklenen pozisyon arasındaki fark, film
  eksenine küçük faz düzeltmesi (registration correction) olarak uygulanır.
- **Crimp/jaw ekseni:** Enine sızdırmazlık ve kesme. Master'a CAM ile kilitli; çene
  ürünle çakışmayacak fazda kapanmalıdır (no-product / no-seal mantığı).
- **Yardımcı I/O:** Sızdırmazlık ısıtıcı PID (band/jaw sıcaklığı), bıçak, ürün dedektörü,
  film bitti / film koptu sensörü, e-stop ve emniyet kapısı.

Kaynaklar (Tim Oxtoby; Packaging Digest), modern makinelerde mekanik kam yerine yazılım
CAM kullanımının ve film/infeed/crimp üçlüsünün master'a senkronizasyonunun standart
olduğunu doğrular. Print mark senkronizasyonu film–baskı hizasını korur.

## Pratikte Nasıl Kullanılır

**Gereksinim listesi (girdi):**
1. 3 senkron servo eksen (infeed, film, crimp) + 1 sanal master.
2. Baskılı film hizalama (print mark registration).
3. Çene–ürün çakışma koruması (no-product, no-seal).
4. Sızdırmazlık sıcaklık kontrolü (≥2 ısıtma bölgesi PID).
5. Operatör paneli: ürün boyutu/recipe seçimi, hız, alarm, durum.
6. Üretim raporlama: paket sayacı, OEE, batch/lot, üst MES.
7. Donanımsal e-stop ve emniyet kapısı (yazılımdan bağımsız).

**Mimari karar (KARAR/GEREKÇE/TAKAS):**

```
KARAR:   Merkezi EtherCAT motion kontrolörü (örn. Inovance AM600) + 3x EtherCAT CiA 402
         servo (örn. SV660N) + bölgesel uzak I/O. Sanal master + CAM mimarisi.
GEREKÇE: 3 eksen <1 ms jitter ile senkron kalmalı; mekanik kam esnekliği yetersiz.
         AM600 32 eksene kadar, 16 CAM destekler; SV660N CiA 402 ~125 µs çevrim.
ALT:     Bağımsız hızlı I/O'lu kompakt PLC + gear-only; ürün/film tipi az değişen,
         baskısız basit makinede yeterdi. Recipe çeşitliliği artınca CAM gerekir.
TAKAS:   EtherCAT + SoftMotion lisans/karmaşıklık maliyeti; DC (distributed clock)
         ayarı doğru yapılmazsa senkron kaybı riski (bkz. Sık Yapılan Hatalar).
```

```
KARAR:   Protokol katmanlaması: EtherCAT (eksen) + OPC-UA server (HMI+MES) + (ops.) MQTT (bulut OEE).
GEREKÇE: decision_framework §1 üç eksen: gerçek-zaman motion = fieldbus (EtherCAT),
         zengin/çift yönlü HMI+MES = OPC-UA, N-alıcılı telemetri = MQTT.
ALT:     HMI için Modbus TCP; recipe/struct verisi tipsiz register'a sığmadığı için
         OPC-UA tercih edildi (struct + metod + keşif).
TAKAS:   OPC-UA kurulum yükü (PKI, namespace); kabul edilir çünkü tek köprü çok istemciye
         hizmet eder.
```

**Task / protokol / HMI eşlemesi:**

| Mantık | Task | Cycle | Protokol/Arayüz |
|--------|------|-------|------------------|
| E-stop, emniyet kapısı | Donanımsal emniyet rölesi + Safety task | ≤1 ms | Donanım (PLC dışı) |
| Sanal master + CAM, 3 servo | Task_Motion | ≤1–2 ms | EtherCAT CiA 402 |
| Print mark faz düzeltmesi | Task_Motion (hızlı yakalama girişi) | senkron | EtherCAT touch-probe / HSC |
| No-product/no-seal interlock | Task_Fast | ≤4 ms | Yerel/uzak DI |
| Isıtıcı PID, recipe yürütme | Task_Control | 10–20 ms | Analog I/O |
| Operatör paneli, alarm | Task_Comm | ≤200 ms | OPC-UA server |
| Paket sayacı/OEE → bulut | Task_Background (Freewheeling) | best-effort | MQTT |

PackML durum makinesi (Idle→Starting→Execute→Stopping…) makine durumunu HMI ve MES'e
tek ortak dille sunar; recipe parametreleri (paket boyu, hız, sıcaklık, CAM profili)
CODESYS recipe yönetimi ile saklanır (bkz. applications/packaging/README.md).

## Örnekler

- **Recipe değişimi:** Operatör HMI'de "150 mm bisküvi" recipe'sini seçer → OPC-UA ile
  recipe ID PLC'ye yazılır → PLC ilgili CAM profilini ve sıcaklık setpoint'lerini yükler →
  PackML Idle→Ready. Eksen mantığı değişmez, sadece CAM tablosu/parametre değişir.
- **Print mark düzeltme döngüsü:** Her pakette print mark sensörü tetiklenir; ölçülen faz
  hatası bir sonraki paket için film eksenine küçük offset olarak verilir. Düzeltme oranı
  sınırlandırılır (ani büyük düzeltme filmi yırtar).
- **No-seal:** Ürün dedektörü ürün yoksa der → crimp ekseni o çevrimde sızdırmazlık fazına
  girmez (boş paket/ürün ezme önlenir).

## Sık Yapılan Hatalar

- **Motion'u yavaş task'a koymak.** CAM/servo mantığını Task_Control'e (10 ms) koymak
  jitter ve senkron kaybı yaratır. Senkron eksenler en hızlı, en yüksek öncelikli task'ta.
- **EtherCAT distributed clock (DC) yanlış ayarı.** DC kapalı/yanlışken eksenler aynı anda
  güncellenmez; sapma birikir, paket boyu kayar. Tüm senkron slave'lerde DC eşlenmeli
  (kaynak: Infoneva DC analizi; control.com synchronized motion).
- **Print mark düzeltmesini sınırsız uygulamak.** Tek seferde büyük faz düzeltmesi film
  gerginliğini bozar/yırtar. Düzeltme rampalanır ve doyurulur.
- **OPC-UA/HMI çağrısını kontrol task'ında bloke etmek.** Session/okuma kontrol döngüsünü
  dondurursa watchdog motorları durdurur. İletişim ayrı task'ta (decision_framework §2).
- **E-stop'u yazılım state machine'ine bağlamak.** PackML "Aborting" durumu emniyeti
  YERİNE GEÇMEZ; e-stop donanımsal kategori-0/1 durdurma sağlamalı.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Merkezi EtherCAT + CAM mimarisi tercih:** Çok eksenli senkron, baskılı film, sık
  recipe değişimi, yüksek hız hedefi olan makinelerde.
- **Etmemeli:** Tek motorlu, baskısız, sabit boy basit bir torba/etiket makinesinde; orada
  kompakt PLC + VFD/step + basit gear yeterli ve daha ucuzdur. Gereğinden ağır motion
  mimarisi maliyet ve bakım yükü getirir.

## Gerçek Proje Notları

- "Makine durmadan paket boyu kayıyor" şikâyetinin tipik kök nedeni print mark düzeltme
  parametreleri veya DC senkronizasyonudur, mekanik değil. Önce motion log'unda following
  error ve düzeltme miktarına bakılır.
- Recipe sayısı arttıkça mantık değil veri büyür: CAM tabloları ve parametreler recipe'de
  tutulur, kod sabit kalır. Bu disiplin makineyi sürdürülebilir kılar.
- Isıtıcı PID'i devreye almadan üretime geçmek tipik bir acelecilik hatasıdır; soğuk
  çeneyle yapılan sızdırmazlık ilk vardiyada fire üretir.
- AM600 + SV660N ekosisteminde ESI dosyası ve InoProShop/firmware sürüm uyumu en sık
  sürtünme noktasıdır (bkz. inovance/inoproshop overview).

## İlgili Konular

- `knowledge/applications/packaging/README.md` — PackML, recipe, SFC tabanı (üzerine inşa)
- `knowledge/examples/case-studies/04_motion_winder_flying_saw.md` — senkron motion derinliği
- `knowledge/protocols/opc-ua/_synthesis.md` — HMI/MES köprüsü
- `knowledge/codesys/task-structure/_synthesis.md` — task atama
- `devices/INOVANCE_AM600`, `devices/INOVANCE_SV660N` — kullanılan donanım
