---
KONU        : Unified Namespace (UNS) ve MQTT Sparkplug B
KATEGORİ    : examples
ALT_KATEGORI: reference-arch
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://sparkplug.eclipse.org/specification/version/3.0/documents/sparkplug-specification-3.0.0.pdf"
    başlık: "Eclipse Sparkplug Specification 3.0.0 (Eclipse Foundation resmi)"
    güvenilirlik: resmi
  - url: "https://www.eclipse.org/tahu/"
    başlık: "Eclipse Tahu — Sparkplug referans implementasyonu (resmi)"
    güvenilirlik: resmi
  - url: "https://cirrus-link.com/understanding-the-unified-namespace-uns-in-industrial-iot/"
    başlık: "Understanding the Unified Namespace (UNS) in Industrial IoT — Cirrus Link"
    güvenilirlik: topluluk
  - url: "https://www.hivemq.com/blog/implementing-unified-namespace-uns-mqtt-sparkplug/"
    başlık: "Implementing Unified Namespace (UNS) With MQTT Sparkplug — HiveMQ"
    güvenilirlik: topluluk
  - url: "https://inductiveautomation.com/resources/icc/2024/demystifying-the-unified-namespace-with-ignition"
    başlık: "Demystifying the Unified Namespace with Ignition — Inductive Automation"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/protocols/mqtt/_synthesis.md"
    ilişki: detaylandırır
  - konu: "knowledge/protocols/mqtt/02_industrial_usage.md"
    ilişki: detaylandırır
  - konu: "knowledge/examples/reference-arch/01_isa95_hierarchy.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: tamamlar
  - konu: "knowledge/standards/02_iec62443.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "MQTT temelleri: broker, topic, QoS, retain, LWT (knowledge/protocols/mqtt/01_basics.md)"
  - "MQTT endüstriyel kullanım ve Sparkplug B girişi (knowledge/protocols/mqtt/02_industrial_usage.md)"
  - "ISA-95 seviye modeli (01_isa95_hierarchy.md)"
ÇELİŞKİLER :
  - kaynak: "UNS = MQTT/Sparkplug zorunlu algısı"
    konu: "UNS bir mimari KAVRAMDIR, belirli bir teknoloji değildir"
    çözüm: >
      UNS = tüm verinin tek, olay-güdümlü, broker-merkezli ve anlamlı bir
      düzlemde toplanması fikridir. MQTT en yaygın taşıyıcıdır ama UNS Kafka,
      OPC UA PubSub veya başka bir omurga üzerine de kurulabilir. Sparkplug B
      ise MQTT üzerine endüstriyel anlam + durum yönetimi ekleyen bir SPEC'tir;
      UNS için zorunlu değildir ama onu güçlü kılan en yaygın seçimdir.
  - kaynak: "Sparkplug B 'raporlama' değil kontrol de yapar algısı"
    konu: "NCMD/DCMD komut mesajları var; bu UNS'i RT kontrol katmanı yapmaz"
    çözüm: >
      Sparkplug NCMD/DCMD ile yazma/komut mümkündür ama bu deterministik RT
      kontrol DEĞİLDİR (TCP + broker kuyruğu). Raporlama ≠ kontrol ilkesi geçerli:
      kapalı çevrim ve güvenlik fonksiyonları fieldbus/PLC'de kalır; UNS gözlem,
      koordinasyon ve süpervizör seviyesi komut içindir.
---

## Özün Ne

**Unified Namespace (UNS)**, bir işletmedeki tüm operasyonel verinin (OT: PLC/SCADA/OEE;
IT: ERP/MES; mühendislik: CAD/PLM) tek, olay-güdümlü, **broker-merkezli** ve anlamlı bir
veri düzleminde toplandığı mimari kavramdır. Geleneksel "nokta-nokta spagetti"
entegrasyonun (N×M bağlantı) yerine, herkesin tek bir omurgaya yayın yaptığı / abone
olduğu hub-and-spoke (N+M) bir model koyar. Verinin **mevcut anlık durumu** omurgada
canlı tutulur; yeni bir tüketici geldiğinde geçmişe gitmeden mevcut durumu hemen alır.

**MQTT Sparkplug B**, UNS'i MQTT üzerine kurarken ham MQTT'nin endüstriyel
eksiklerini kapatan, **Eclipse Foundation** tarafından standartlaştırılan bir
spesifikasyondur (güncel: Sparkplug 3.0; referans implementasyon: **Eclipse Tahu**).
Standart topic ad uzayı (`spBv1.0/...`), Protobuf payload, birth/death sertifikaları ve
durum yönetimi getirir. Böylece "broker'a ne yayınlandığı" tüm üreticiler için tahmin
edilebilir ve kendini-tanımlayan hale gelir.

Neden önemli: UNS, modern IIoT mimarisinin baskın tasarım deseni haline geldi; agent bir
"PLC'leri buluta/MES'e/analitiğe bağla" sorusunu doğru yanıtlamak için UNS'in ne zaman
doğru, ne zaman aşırı olduğunu bilmelidir. Bu belge mevcut MQTT bilgi tabanını (bkz.
ÖNKOŞUL) referans mimari seviyesine bağlar.

## Nasıl Çalışır

### Spagettiden Hub-and-Spoke'a

```
GELENEKSEL (nokta-nokta)              UNS (broker-merkezli)
                                      
PLC1 ─┬─ SCADA                        PLC1 ─┐
PLC1 ─┼─ Historian                    PLC2 ─┤        ┌─ SCADA
PLC1 ─┼─ Cloud                        PLC3 ─┼──► UNS ┼─ Historian
PLC2 ─┼─ SCADA                        MES  ─┤  Broker┼─ Cloud
PLC2 ─┼─ Historian        →           ERP  ─┘   (UNS) ┼─ Analitik
...   N×M bağlantı                              └─ Yeni tüketici
12 PLC × 3 hedef = 36 bağlantı        12 + 3 = 15; yeni tüketici = +1 abone
```

Asıl kazanç **gevşek bağlantı**tır (decoupling): yayıncı tüketiciyi bilmez. Yeni bir
analitik/dashboard eklemek PLC kodunu değiştirmez — yalnızca yeni bir abone eklenir.

### UNS'in Dört Niteliği

UNS yalnızca "MQTT broker" demek değildir; iyi bir UNS şu dördünü taşır:
1. **Tek kaynak (single source of truth):** Tüm sistemler aynı omurgadan okur/yazar.
2. **Olay-güdümlü (event-driven):** Veri değiştikçe iter (report-by-exception), sorgu döngüsü yok.
3. **Mevcut durum canlı (edge-of-state):** Omurga her topic'in son değerini tutar (MQTT retain / Sparkplug birth).
4. **Anlamlı/hiyerarşik (semantic):** Topic ağacı ISA-95'i izler: `enterprise/site/area/line/cell/device/datapoint`.

ISA-95 hiyerarşisi burada **organizasyonel** olarak (topic isimlendirmede) yaşar; veri
**akışı** ise düzdür (herkes broker'a). "Piramidin düzleştirilmesi" denen şey budur:
seviyeler kavram olarak durur, katı nokta-nokta veri bağımlılığı kalkar (bkz.
01_isa95_hierarchy.md ÇELİŞKİLER).

### Sparkplug B'nin Eklediği Anlam ve Durum Yönetimi

Ham MQTT topic/payload'ı serbest bırakır; Sparkplug B bunu disipline eder:

```
spBv1.0/{group_id}/{message_type}/{edge_node_id}/{device_id}

NBIRTH/DBIRTH  → Doğum sertifikası: tüm metric'ler + metadata (birim, tip, alias) bir kez
NDATA/DDATA    → Yalnızca değişen metric'ler (alias ile; isim tekrar edilmez) — RbE
NDEATH/DDEATH  → Ölüm sertifikası: LWT ile bağlantı kopuşu otomatik ilan edilir
NCMD/DCMD      → Komut (host → edge node/device)
STATE          → Primary Host Application'ın çevrimiçi/çevrimdışı durumu (QoS 1)
```

Kritik kavramlar:
- **Edge Node / Device:** Veriyi broker'a getiren mantıksal düğüm ve onun altındaki cihazlar.
- **Birth/Death sertifikası:** Bir düğüm bağlanınca tüm tag yapısını + metadata'yı bir kez
  yayınlar (NBIRTH); araçlar bunu okuyup tag ağacını otomatik kurar. Kopunca NDEATH (LWT).
- **Alias:** Birth'te her metric'e bir sayısal alias atanır; sonraki NDATA'da yalnızca alias
  taşınır → bant genişliği ciddi düşer.
- **Primary Host Application + STATE:** Edge node, kendisine atanmış birincil host
  uygulamasının (örn. SCADA) çevrimiçi olmasını bekleyebilir; host STATE ile durumunu
  güvenilir (QoS 1) yayınlar. Bu, "kimse dinlemiyorken boşa yayın" ve durum tutarsızlığı
  sorunlarını çözer.

Sonuç: ham MQTT'de 2-3 gün süren bir entegrasyon (topic analiz, payload decode, birim
belgeleme), Sparkplug B'de 2-3 saate iner çünkü NBIRTH her şeyi kendi anlatır (bkz.
mqtt/_synthesis.md, tablo C).

## Pratikte Nasıl Kullanılır

1. **Topic ağacını ISA-95 ile baştan tasarla.** `enterprise/site/area/line/cell/device/...`.
   Bu, UNS'in en kalıcı kararıdır; sonradan değiştirmek pahalıdır.
2. **Omurga broker'ı seç ve HA kur.** Tek-node Mosquitto bir SPOF'tur; üretim-kritik UNS'te
   HiveMQ/EMQX cluster (bkz. mqtt/_synthesis.md tablo D). UNS broker'ı tüm işletmenin kalbidir.
3. **Sparkplug B mı, ham MQTT mi?** Çok üreticili, otomatik tag keşfi ve durum yönetimi
   gerekiyorsa Sparkplug B. Basit/pilot ya da tüm tüketiciler özel yazılımsa ham MQTT yeterli.
4. **Edge node'ları kur.** PLC verisini omurgaya getiren edge yazılımı (Ignition + Cirrus
   Link MQTT modülleri, HiveMQ Edge, Node-RED vb.) Sparkplug edge node olarak yapılandır.
5. **Güvenliği baştan ekle.** TLS (8883), kimlik doğrulama, ACL. UNS broker'ı tüm verinin
   tek noktası olduğu için IEC 62443 açısından yüksek değerli bir varlıktır; uygun Zone'a
   yerleştir (bkz. standards/02_iec62443.md).
6. **OPC UA ile katmanla.** UNS, OPC UA'yı dışlamaz: SCADA↔PLC iki yönlü/semantik kontrol
   OPC UA'da kalır; UNS veri toplama ve dağıtım katmanıdır. OPC UA PubSub, MQTT'yi transport
   olarak kullanarak ikisini birleştirebilir.

## Örnekler

**Örnek topic ağacı (Sparkplug + UNS):**
```
spBv1.0/Istanbul_Plant/NBIRTH/Line1_EdgeNode          (doğumda tüm tag + metadata)
spBv1.0/Istanbul_Plant/NDATA/Line1_EdgeNode/Conveyor  (yalnızca değişen hız/akım)
spBv1.0/Istanbul_Plant/NDEATH/Line1_EdgeNode          (kopuş — LWT)

# UNS okunabilir gölge ağaç (JSON, dashboard/IT için, opsiyonel):
enterprise/istanbul/imalat/line1/conveyor/speed   = {"value":1452.3,"unit":"rpm"}
enterprise/istanbul/imalat/line1/status/online    = "true" (retain)
```

**Senaryo — yeni analitik eklemek:** Bir tahminsel bakım servisi devreye alındı. UNS'te
yapılması gereken tek şey: servisi broker'a `enterprise/+/+/+/+/vibration`'a abone etmek.
Hiçbir PLC, SCADA veya MES kodu değişmez. Gevşek bağlantının somut getirisi budur.

## Sık Yapılan Hatalar

- **Broker'ı SPOF bırakmak.** UNS omurgası çökerse tüm görünürlük gider. HA cluster zorunlu.
- **Topic ağacını düz/anlamsız tasarlamak.** `sensor1`, `temp2` gibi isimler wildcard ve
  ISA-95 hizalamasını imkânsızlaştırır; ölçek büyüyünce her tüketici yeniden eşlenir.
- **Sparkplug seq/Rebirth disiplinini ihmal etmek.** Reconnect'te `seq` sıfırlanmazsa
  "Rebirth fırtınası" trafiği patlatır (bkz. mqtt/_synthesis.md tablo F).
- **UNS'i RT kontrol katmanı sanmak.** NCMD/DCMD ile komut göndermek deterministik değildir;
  kapalı çevrim ve güvenlik fonksiyonları PLC/fieldbus'ta kalır (raporlama ≠ kontrol).
- **OPC UA ile UNS'i "ya o ya bu" sanmak.** İkisi rakip değil, katmanlıdır: OPC UA
  cihaz-SCADA kontrol; UNS/MQTT veri toplama-dağıtım.
- **Güvenliği sonraya bırakmak.** En değerli tek varlık (tüm işletme verisi tek broker'da)
  en iyi korunması gerekendir; port 1883 + anonymous üretimde kabul edilemez.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih (UNS):** Çok kaynak → çok tüketici dağıtımı; bulut/analitik entegrasyonu; çoklu
  tesis; sık değişen/eklenen tüketiciler; "spagetti" entegrasyonu temizleme.
- **Tercih (Sparkplug B üstüne):** Çok üreticili ortam, otomatik tag keşfi, durum yönetimi,
  Ignition/Cirrus Link/HiveMQ Sparkplug ekosistemi, bant genişliği kısıtı (4G/uydu).
- **Etme / aşırı:** İki cihazın doğrudan konuşması (Modbus TCP yeter); deterministik RT
  kontrol (fieldbus); SCADA↔PLC iki yönlü semantik kontrol (OPC UA); küçük pilot (ham MQTT
  veya doğrudan bağlantı, Sparkplug ek karmaşıklık getirir).

## Gerçek Proje Notları

- **UNS'in değeri değişim anında görünür.** OPC UA + MQTT katmanlı bir projede SCADA
  değişti ama MQTT pipeline etkilenmedi; sonra analitik platformu değişti ama OPC UA SCADA
  etkilenmedi. Gevşek bağlantının getirisi ancak bir bileşen değişince anlaşılır (bkz.
  mqtt/_synthesis.md Not 5).
- **Topic ağacı = API kontratı.** OPC UA'da NodeId ne ise UNS'te topic ağacı odur:
  yayımlandıktan sonra değiştirmek tüm tüketicileri kırar. ISA-95 tabanlı şemayı baştan,
  bir daha değişmeyecek şekilde kur.
- **Walker Reynolds / 4.0 Solutions** UNS terimini popülerleştirdi; **Cirrus Link**
  (Ignition MQTT modülleri), **HiveMQ**, **Litmus**, **HighByte** ekosistemin tipik
  bileşenleridir. Agent bir UNS sorusunda bu araç manzarasını tanımalı.
- **[DOĞRULANMADI]** Sparkplug'ın belirli sürüm-özellik eşlemesi (örn. hangi STATE
  davranışı 2.2 vs 3.0'a ait) proje öncesi resmi spec'ten teyit edilmeli; bu belge kavramsal
  düzeyde tutulmuştur.

## İlgili Konular

- `knowledge/protocols/mqtt/_synthesis.md` — MQTT bütünsel sentez; Sparkplug B, UNS, broker seçimi tabloları
- `knowledge/protocols/mqtt/02_industrial_usage.md` — Sparkplug B mesaj tipleri, ISA-95 topic tasarımı
- `01_isa95_hierarchy.md` — UNS topic ağacının dayandığı seviye modeli; "piramidin düzleştirilmesi"
- `03_opcua_companion_specs.md` — Semantik birlikte çalışabilirliğin OPC UA tarafındaki karşılığı
- `knowledge/protocols/opc-ua/01_architecture.md` — OPC UA PubSub + MQTT transport; katmanlı mimari
- `knowledge/standards/02_iec62443.md` — UNS broker'ının Zone/Conduit içinde korunması
