---
KONU        : InoProShop — Üst Sentez
KATEGORİ    : inovance
ALT_KATEGORI: inoproshop
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.inovance.eu/news/details/inovance-has-worked-with-codesys-since-2015-is-now-listed-on-the-codesys-website-173"
    başlık: "Inovance — CODESYS ile 2015'ten beri (resmi)"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/products/motion-controllers-i/o-modules/am600-motion-controllers"
    başlık: "Inovance — AM400/AM600 Motion Controllers"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_inoproshop_overview.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/_synthesis.md"
    ilişki: türev
  - konu: "08_codesys_to_inoproshop.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "CODESYS V3 temel bilgisi (knowledge/codesys/)"
ÇELİŞKİLER :
  - kaynak: "Inovance ürün gamı algısı"
    konu: "Tüm Inovance PLC'leri tek ortamla programlanır sanılması"
    çözüm: >
      İki ayrı ortam vardır: InoProShop (CODESYS V3 tabanlı) AM400/AM600/AC800 için;
      AutoShop (CODESYS değil) H5U/H3U/Easy için. Doğru ortam ürünle eşlenmelidir.
---

## Özün Ne

InoProShop, **özünde CODESYS V3'tür** — Inovance'ın orta-sınıf kontrolörleri (AM400,
AM600, AC800) için markaladığı, kendi cihaz havuzu, EtherCAT yığını ve motion
kütüphaneleriyle zenginleştirilmiş bir CODESYS dağıtımıdır. Bu bilgi tabanının tek bir
cümleyle özü: **CODESYS V3 biliyorsan InoProShop'u biliyorsun; geriye sadece Inovance'a
özgü cihaz/EtherCAT/motion ayrıntıları kalır.**

Bu, alt belgelerin (`01`–`10`) ortak iskeletidir ve hepsi `knowledge/codesys/` bilgi
tabanının InoProShop'a uyarlanmış halidir.

## InoProShop ↔ CODESYS İlişkisi (net özet)

| Boyut | Durum |
|-------|-------|
| IDE / editörler | CODESYS V3 ile aynı (ST/LD/FBD/SFC/IL/CFC) |
| Proje yapısı | Device tree, Application, Library Manager, Task, GVL/DUT — aynı |
| Debug | Online izleme, breakpoint, force, trace — aynı (breakpoint motion'da riskli) |
| Motion | PLCopen MC_* / SoftMotion soyağacı; AM600 EtherCAT 32 eksen |
| Haberleşme | Modbus TCP/RTU, OPC-UA, CANopen, Socket — CODESYS mantığı |
| Fark | Marka-kilitli cihaz havuzu (Inovance ürünleri hazır), firmware-IDE sürüm eşlemesi |
| Kapsam | **Yalnız AM400/AM600/AC800.** H5U/H3U/Easy = AutoShop (ayrı, CODESYS değil) |

## Ne Zaman InoProShop Tercih Edilmeli

- **Tercih:** Donanım Inovance AM400/AM600/AC800 olduğunda; özellikle AM600 + Inovance
  EtherCAT servo (SV660N/IS620N) + GL20 I/O ile motion uygulamalarında. CODESYS bilgisi
  doğrudan transfer olur, maliyet avantajı vardır.
- **Etme:** Donanım H5U/H3U/Easy ise → **AutoShop** (InoProShop çalışmaz). Vendor-bağımsız,
  çok-marka bir mimari gerekiyorsa jenerik CODESYS + ilgili device paketleri daha esnektir.

## Doğrulanmış Olgular vs. Çıkarımlar (dürüstlük notu)

- **Sağlam olgu:** InoProShop'un CODESYS V3 tabanlı olması, hedef ürünler (AM400/600/AC800),
  AM600 motion kapasitesi (32 eksen, PLCopen), AutoShop ayrımı.
- **Çıkarım / doğrulanmalı:** Proje dosyası uzantısı, OPC-UA sunucusunun lisans/sürüm
  gereksinimi, AC800 port/cycle ayrıntıları, ESI indirme URL'leri, üreticiye özel Modbus
  parametre adresleri. Bunlar ilgili belgelerde `[DOĞRULANMADI]` / ÇELİŞKİLER ile
  işaretlendi; devreye almadan önce resmi Inovance dokümanından teyit edilmelidir.
- Bu yüzden alan olgunluğu **"Orta"** olarak işaretlendi: pratik ve kaynaklı, ancak derin
  gerçek-proje doğrulaması her ayrıntı için tamamlanmamıştır.

## Belge Haritası

1. `01_inoproshop_overview.md` — Ne olduğu, CODESYS ilişkisi, ürünler, lisanslama
2. `02_project_structure.md` — Proje/Device tree/Library Manager
3. `03_iec61131_in_inoproshop.md` — IEC dilleri + kod taşıma uyumu
4. `04_hardware_configuration.md` — AM600/AC800 donanım (+ H5U uyarısı)
5. `05_ethercat_configuration.md` — EtherCAT master/slave, ESI, servo/I/O, DC
6. `06_motion_control.md` — PLCopen MC_*, eksen, interpolasyon
7. `07_communication.md` — Modbus/OPC-UA/CANopen/Socket/HMI
8. `08_codesys_to_inoproshop.md` — Migrasyon rehberi
9. `09_debugging.md` — Debug araçları + sistematik teşhis
10. `10_best_practices.md` — Organizasyon/performans/güvenli programlama

## İlgili Konular

- `knowledge/codesys/_synthesis.md` — taban CODESYS bilgisi (bu sentezin kaynağı)
- `devices/INOVANCE_AM600/`, `devices/INOVANCE_SV660N/`, `devices/INOVANCE_GL20/`
