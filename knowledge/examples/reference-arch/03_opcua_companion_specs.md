---
KONU        : OPC UA Companion Specifications (Birlikte Çalışabilirlik Modelleri)
KATEGORİ    : examples
ALT_KATEGORI: reference-arch
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://opcfoundation.org/about/opc-technologies/opc-ua/ua-companion-specifications/"
    başlık: "UA Companion Specifications — OPC Foundation (resmi)"
    güvenilirlik: resmi
  - url: "https://opcfoundation.org/markets-collaboration/pa-dim/"
    başlık: "PA-DIM (Process Automation Device Information Model) — OPC Foundation (resmi)"
    güvenilirlik: resmi
  - url: "https://www.euromap.org/i40/OPCUA"
    başlık: "EUROMAP — Overview OPC UA Specifications (EUROMAP resmi)"
    güvenilirlik: resmi
  - url: "https://reference.opcfoundation.org/"
    başlık: "OPC UA Online Reference (OPC Foundation resmi)"
    güvenilirlik: resmi
  - url: "https://www.opcconnect.com/opc-ua-companion-specifications.php"
    başlık: "OPC UA Companion Specifications — OPCconnect.com"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/protocols/opc-ua/02_address_space.md"
    ilişki: detaylandırır
  - konu: "knowledge/protocols/opc-ua/_synthesis.md"
    ilişki: detaylandırır
  - konu: "knowledge/standards/03_namur_ne107.md"
    ilişki: tamamlar
  - konu: "knowledge/examples/reference-arch/04_namur_open_architecture.md"
    ilişki: kullanır
  - konu: "knowledge/examples/reference-arch/01_isa95_hierarchy.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "OPC UA mimari ve adres uzayı: Object/Variable/Method/ObjectType, NodeId, namespace (knowledge/protocols/opc-ua/01_architecture.md, 02_address_space.md)"
  - "Bilgi modeli (information model) kavramı"
ÇELİŞKİLER :
  - kaynak: "Companion spec = ayrı/yeni protokol algısı"
    konu: "Companion spec yeni bir protokol değildir; OPC UA üzerine bir bilgi modeli katmanıdır"
    çözüm: >
      Companion Specification, OPC UA'nın taşıma/güvenlik/servis altyapısını
      DEĞİŞTİRMEZ. Yalnızca belirli bir alan için standart ObjectType, Variable
      ve Method tanımları (ns=... ayrı namespace) ekler. Aynı opc.tcp bağlantısı,
      aynı Read/Write/Subscribe servisleri kullanılır; değişen tek şey adres
      uzayındaki tiplerin önceden tanımlı ve üreticiler arası ortak olmasıdır.
  - kaynak: "Companion spec uyumu RT kontrol sağlar algısı"
    konu: "Companion spec semantik birlikte çalışabilirliktir, gerçek zamanlılık değil"
    çözüm: >
      Bir cihaz PackML veya PA-DIM uyumlu olması onu deterministik RT kontrol
      arayüzü yapmaz. OPC UA hâlâ raporlama/süpervizör komut katmanıdır
      (raporlama ≠ kontrol). Companion spec yalnızca "veri NE anlama geliyor"
      sorusunu standartlaştırır; "ne kadar hızlı/deterministik" sorusu fieldbus'ın işidir.
---

## Özün Ne

**OPC UA Companion Specification (Companion Spec / UA-CS)**, belirli bir endüstri, cihaz
sınıfı veya kullanım senaryosu için **standart bir OPC UA bilgi modeli** tanımlayan
spesifikasyondur. OPC Foundation, çekirdek OPC UA standardının (IEC 62541) üzerine —
çoğu zaman ilgili sektör birliğiyle (EUROMAP, FieldComm, VDMA, vb.) ortak çalışma
gruplarında — bu modelleri yayımlar. Bugün **60'tan fazla** companion spec mevcuttur.

Özü: OPC UA *taşıma + güvenlik + servis* altyapısını verir ama "bir ambalaj makinesinin
durumu hangi node'da, hangi adla, hangi tiple temsil edilir?" sorusuna cevap vermez.
Companion spec tam olarak bunu yapar — alan için ortak ObjectType/Variable/Method
tanımlarını sabitler. Böylece **aynı spec'i destekleyen farklı üreticilerin cihazları,
özel mühendislik olmadan birbirine ve üst sistemlere bağlanabilir** (semantik düzeyde
birlikte çalışabilirlik / interoperability).

Neden önemli: Endüstride en pahalı kalemlerden biri "tag eşleme" işidir — her cihazın
verisini elle anlamlandırmak. Companion spec bu işi standartlaştırarak entegrasyon
süresini ve maliyetini dramatik düşürür. Agent, bir entegrasyon/satınalma sorusunda
"bu cihaz hangi companion spec'i destekliyor?" diye sormayı bilmelidir.

## Nasıl Çalışır

### Katmanlı Bilgi Modeli

```
┌──────────────────────────────────────────────────────────────┐
│  Companion Specification (alan namespace, örn. ns=PackML)     │
│  Standart ObjectType: MachineType, PackTags, UnitState...    │
│  → "Bu domain'de veri NE anlama gelir" (üreticiler arası ortak)│
├──────────────────────────────────────────────────────────────┤
│  OPC UA Çekirdek Bilgi Modeli (ns=0)                          │
│  BaseObjectType, BaseDataVariableType, HasComponent...        │
├──────────────────────────────────────────────────────────────┤
│  OPC UA Altyapısı: Discovery · Transport (opc.tcp) ·          │
│  Servisler (Read/Write/Browse/Subscribe/Call) · Güvenlik (PKI)│
└──────────────────────────────────────────────────────────────┘
```

Companion spec, çekirdek modelden tip türetir (inheritance). Bir cihaz "PackML uyumlu"
ise adres uzayında PackML namespace'inden gelen standart tipleri sunar; bir istemci bu
tipleri *önceden* bildiği için keşif + eşleme neredeyse otomatiktir. Çekirdek OPC UA
servisleri (Read/Write/Subscribe/Call Method) hiç değişmez — bu yüzden companion spec
"yeni protokol" değil, "ortak sözlük"tür (bkz. ÇELİŞKİLER).

### Temsili Companion Spec'ler (alanlara göre)

| Alan | Companion Spec (örnek) | Ne tanımlar |
|------|------------------------|-------------|
| Ambalaj | **PackML** | Ambalaj makinesi durum makinesi (state model) + tag isimlendirme |
| Plastik/enjeksiyon | **EUROMAP** (77, 83 vb.) | Plastik & kauçuk makineleri; 83 temel tipler, 77 enjeksiyon→MES |
| Proses cihazları | **PA-DIM** | Proses otomasyon cihazı bilgi modeli; üreticiden bağımsız ölçüm + NE107 sağlık |
| Robotik | **Robotics (OPC 40010)** | Robot sistemleri entegrasyonu |
| Takım tezgahı/CNC | **MachineTool / CNC** | Takım tezgahı ve CNC operasyonları |
| Cihaz entegrasyonu | **DI (Device Integration)** | Jenerik cihaz bağlanırlığı temel modeli (çok spec bunun üstüne kurulur) |
| Analizör | **ADI (Analyser Devices)** | Analitik cihazlar |
| Otomatik tanıma | **AutoID** | RFID/barkod/otomatik kimlik |
| PLC | **IEC 61131-3** | PLC programlama yapılarını OPC UA'da temsil |
| Kurumsal entegrasyon | **ISA-95** | ISA-95 nesnelerini OPC UA bilgi modeli olarak sunar |
| Makine görü | **Machine Vision** | Endüstriyel görüntüleme |

[DOĞRULANMADI: tam spec numaraları ve sürümleri — örn. EUROMAP 77/83, OPC 40010 —
proje öncesi opcfoundation.org/reference.opcfoundation.org'tan teyit edilmeli; isim ve
alan eşlemesi resmi genel-bakış belgesinde tutarlıdır.]

### PA-DIM — Üç Standardın Kesişimi

PA-DIM (Process Automation Device Information Model, FieldComm Group + OPC Foundation),
proses cihazının ölçümlerini ve sağlık durumunu **üreticiden ve fieldbus'tan bağımsız**
bir OPC UA modeline taşır. Önemli: PA-DIM, **NAMUR NE107** sağlık kategorilerini (F/C/S/M)
standart OPC UA node'ları olarak sunar. Böylece PA-DIM, OPC UA companion spec'i + NE107
diagnostiği + (NOA bağlamında) ikinci kanal veri akışının buluştuğu noktadır (bkz.
standards/03_namur_ne107.md ve 04_namur_open_architecture.md).

## Pratikte Nasıl Kullanılır

1. **Satınalma şartnamesine koy.** "Cihaz OPC UA sunmalı" yetmez; "X companion spec'ine
   uyumlu OPC UA sunmalı" yaz. Asıl entegrasyon kolaylığı buradan gelir.
2. **İstemci tarafında spec'i tanı.** İstemci (SCADA/MES) aynı companion spec'i
   destekliyorsa, standart node'lar elle eşleme olmadan kullanılır.
3. **Namespace'i dinamik çöz.** Companion spec kendi namespace URI'sini taşır; NodeId'leri
   `get_namespace_index(spec_URI)` ile dinamik al, hardcode etme (bkz. opc-ua/_synthesis.md İlke 3).
4. **Eksik tarafı tamamla.** Cihaz spec'i destekliyor ama üst sistem desteklemiyorsa, bir
   eşleme katmanı (gateway/aggregating server) yine gerekebilir; o zaman bile spec, eşlemeyi
   standart kıldığı için işi kolaylaştırır.

## Örnekler

**Senaryo — robot OEM entegrasyonu (gerçek getiri):** Bir robot OEM'i Robotics companion
spec uyumlu OPC UA server sundu, SCADA istemcisi aynı spec'i destekliyordu. Özel tag
eşlemesi yazmak yerine standartta tanımlı node'lar doğrudan kullanıldı; entegrasyon
2 günden ~4 saate indi. Bu deneyimden sonra companion spec uyumluluğu satınalma
şartnamesinde standart madde oldu (bkz. opc-ua/_synthesis.md, Gerçek Proje Notları Not 6).

**Senaryo — PA-DIM + NE107:** Farklı üreticilerin transmitterları PA-DIM uyumlu olunca,
SCADA tek bir standart "Device Health" node'undan tüm cihazların F/C/S/M durumunu okudu;
üretici-özel diagnostik byte'larını çözmek gerekmedi.

## Sık Yapılan Hatalar

- **"OPC UA destekliyor" ile "companion spec destekliyor"u karıştırmak.** Ham OPC UA
  yalnızca taşımayı verir; semantik birlikte çalışabilirlik companion spec ile gelir.
- **Namespace index hardcode etmek.** Companion spec namespace index'i kuruluma göre
  değişir; daima URI'dan dinamik çöz.
- **Companion spec'i RT kontrol arayüzü sanmak.** Semantik standarttır, determinizm değil;
  kapalı çevrim fieldbus'ta kalır (raporlama ≠ kontrol).
- **Spec sürüm uyumsuzluğu.** Server ve client farklı companion spec sürümlerindeyse bazı
  node'lar eşleşmez; sürümü şartnamede sabitle.
- **Her şeyi flat yayınlayıp companion spec'i atlamak.** Standart tip varken özel düz model
  kurmak OPC UA'yı "pahalı Modbus"a düşürür (bkz. opc-ua/_synthesis.md İlke 5).

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih:** Çok üreticili ortam; ilgili sektörde olgun bir spec varsa (ambalaj→PackML,
  plastik→EUROMAP, proses cihazı→PA-DIM); entegrasyon maliyetini düşürmek; gelecekte cihaz
  değişimine açık kalmak; NE107 sağlık verisini standart taşımak (PA-DIM).
- **Etme / gereksiz:** Tek üretici, kapalı ekosistem, küçük ve değişmeyecek sistem; ilgili
  alanda olgun bir spec henüz yoksa (zorlamak yerine net bir özel model + iyi dokümantasyon).
- **Tek başına yetmez:** Companion spec semantiği standartlaştırır; güvenlik (PKI), gerçek
  zamanlılık (fieldbus) ve ağ segmentasyonu (IEC 62443) ayrı kararlar olarak durur.

## Gerçek Proje Notları

- **Companion spec'in asıl getirisi "değişim direnci"dir.** Spec uyumlu bir cihazı, aynı
  spec'i destekleyen başka bir üreticininkiyle değiştirmek üst sistemde minimum değişiklik
  gerektirir — vendor lock-in'i azaltır.
- **Olgunluk alana göre çok değişir.** EUROMAP (plastik) ve PackML (ambalaj) çok olgun ve
  yaygın; bazı yeni alanlarda spec taslak/az yaygın olabilir. Şartnameye koymadan önce
  hedef sektörde gerçek pazar yaygınlığını doğrula.
- **PA-DIM, agent için stratejik düğümdür.** OPC UA companion spec + NE107 + NOA ikinci
  kanal aynı noktada buluşur; proses endüstrisi sorularında PA-DIM'i tanımak üç konuyu
  birden bağlar.
- **[DOĞRULANMADI]** Spec sayısı "60+" mertebesindedir ve sürekli artar; kesin güncel
  liste ve sürümler için reference.opcfoundation.org tek güvenilir kaynaktır.

## İlgili Konular

- `knowledge/protocols/opc-ua/02_address_space.md` — ObjectType/Variable/Method, NodeId, namespace (companion spec'in dayandığı temel)
- `knowledge/protocols/opc-ua/_synthesis.md` — Information model = asıl değer; namespace dinamik çözme ilkesi
- `knowledge/standards/03_namur_ne107.md` — PA-DIM'in taşıdığı F/C/S/M diagnostik kategorileri
- `04_namur_open_architecture.md` — NOA ikinci kanalda OPC UA + PA-DIM kullanımı
- `01_isa95_hierarchy.md` — ISA-95'in de bir companion spec'i vardır (kurumsal entegrasyon modeli)
