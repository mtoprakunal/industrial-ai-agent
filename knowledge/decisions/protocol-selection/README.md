---
KONU        : Protokol Seçim Kararları — OPC UA / Modbus TCP / MQTT / Ham TCP Socket
KATEGORİ    : decisions
ALT_KATEGORI: protocol-selection
SEVİYE      : Orta-İleri
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/protocols/_synthesis.md"
    başlık: "Endüstriyel Protokoller Karşılaştırmalı Üst Sentez"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/opc-ua/_synthesis.md"
    başlık: "OPC UA Sentezi — Mimari, Güvenlik, Subscription, CODESYS"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/modbus-tcp/_synthesis.md"
    başlık: "Modbus TCP Sentezi — Register Modeli, FC'ler, CODESYS Slave"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/mqtt/_synthesis.md"
    başlık: "MQTT Sentezi — Pub/Sub, Sparkplug B, UNS, Broker Seçimi"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/tcp-socket/_synthesis.md"
    başlık: "Ham TCP Socket Sentezi — SysSock, Framing, Özel Protokol Tasarımı"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/networking/_synthesis.md"
    başlık: "CODESYS Networking Sentezi — Dört Protokol Kurulum Rehberi"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/protocols/_synthesis.md"
    ilişki: kullanır (bu belgenin birincil kaynağı — tüm karşılaştırma tabloları)
  - konu: "knowledge/protocols/opc-ua/_synthesis.md"
    ilişki: detaylandırır (OPC UA karar gerekçeleri)
  - konu: "knowledge/protocols/modbus-tcp/_synthesis.md"
    ilişki: detaylandırır (Modbus TCP karar gerekçeleri)
  - konu: "knowledge/protocols/mqtt/_synthesis.md"
    ilişki: detaylandırır (MQTT karar gerekçeleri)
  - konu: "knowledge/protocols/tcp-socket/_synthesis.md"
    ilişki: detaylandırır (Ham TCP Socket karar gerekçeleri)
  - konu: "knowledge/decisions/architecture"
    ilişki: tamamlar (mimari kararlar bu protokol kararlarını çerçeveler)
ÖNKOŞUL     :
  - "Dört protokol sentezi okunmuş olmalı: opc-ua, modbus-tcp, mqtt, tcp-socket"
  - "Temel ağ kavramları: TCP/IP, port, LAN/WAN, pub/sub modeli"
  - "Endüstriyel otomasyon katmanları: Fieldbus → PLC → SCADA → MES → ERP → Bulut"
ÇELİŞKİLER :
  - kaynak: "MQTT vs OPC UA — Rakip protokol algısı"
    konu: "MQTT ve OPC UA rakip değil, katmanlı mimari bileşenleridir"
    çözüm: >
      OPC UA cihaz-SCADA katmanında (bidirectional, semantik, güvenli, metod çağrısı).
      MQTT veri toplama-bulut katmanında (push, çok alıcı, ölçeklenebilir).
      En olgun mimari ikisini birlikte kullanır; seçim değil katmanlama.
  - kaynak: "Modbus TCP = güvenli yeter algısı"
    konu: "Modbus TCP protokol düzeyinde hiçbir güvenlik mekanizması sunmaz"
    çözüm: >
      2024 FrostyGoop saldırısı: Port 502 internete açık → fiziksel hasar.
      Güvenlik ağ mimarisi düzeyinde sağlanır: VPN, güvenlik duvarı, VLAN segmentasyonu.
      Modbus TCP hiçbir zaman internete açılmaz.
  - kaynak: "Daha karmaşık = daha iyi algısı"
    konu: "OPC UA her senaryonun cevabı değil; Modbus TCP sık hafife alınır"
    çözüm: >
      Senaryo eğer 2-3 basit değer, tek legacy cihaz, hızlı prototiptyse Modbus TCP doğru.
      OPC UA'yı "pahalı Modbus" olarak kullanmak hem kurulum maliyetini hem bakım yükünü artırır.
      Doğru protokol en güçlü protokol değil, senaryoya en uygun protokoldür.
---

## Özün Ne

Bu belge, "Elimde bir entegrasyon problemi var — hangi protokolü seçmeliyim ve neden?" sorusunun karar kaydıdır. Teorik karşılaştırma değil, gerçek senaryolarda verilen kararların gerekçeli belgesidir. OPC UA, Modbus TCP, MQTT ve Ham TCP Socket arasındaki seçim çoğunlukla tek bir doğru yanıt içermez; ancak belirli kriterler (latency, veri karmaşıklığı, güvenlik, keşfedilebilirlik, cihaz ekosistemi, IT/bulut entegrasyonu, maliyet) sistematik bir çerçeveyle değerlendirildiğinde en az hata yapılan karar ortaya çıkar. Bu belge o çerçeveyi, somut senaryo örneklerini ve yaygın yanlış kararları bir arada sunar.

---

## Nasıl Çalışır

### Karar Kriterleri — Ne Ölçülür?

Protokol seçiminde değerlendirilen yedi ana kriter:

```
1. LATENCY (Gecikme)
   ─────────────────
   Ham TCP Socket : < 1ms (LAN içi, persistent connection)
   Modbus TCP     : < 5ms (LAN içi, basit polling)
   OPC UA         : < 10ms (session overhead var, LAN içi yeterli)
   MQTT           : < 10ms + broker gecikmesi (LAN içi broker ile ihmal edilir)
   
   → Gerçek zamanlı kontrol (< 1ms): Hiçbiri. EtherCAT / PROFINET kullan.
   → Soft real-time (1-50ms): Hepsi yeterlidir.

2. VERİ KARMAŞIKLIĞI
   ──────────────────
   16-bit integer / float setpoint    → Modbus TCP yeterli
   Semantik model, struct, enum       → OPC UA
   Metod çağrısı (StartRecipe, Reset) → OPC UA zorunlu
   JSON payload, değişken yapı        → MQTT (Sparkplug B ile şema)
   Büyük binary blob (görüntü, dalga) → Ham TCP (overhead yok)

3. KEŞFEDİLEBİLİRLİK (Discoverability)
   ────────────────────────────────────
   OPC UA : Browse servisi — NodeId, tip, hiyerarşi otomatik keşif
   Modbus : Yok — belge / register haritası zorunlu
   MQTT   : Yok — Sparkplug B NBIRTH ile kısmi (metadata otomatik)
   Ham TCP: Yok — üretici belgesi veya tersine mühendislik

4. GÜVENLİK
   ─────────
   OPC UA     : Yerleşik (PKI, TLS, rol tabanlı erişim, IEC 62443 uyumlu)
   MQTT       : TLS opsiyonel (port 8883), kullanıcı adı/şifre, ACL
   Ham TCP    : Yok protokol düzeyinde — uygulama katmanı ihtiyaç duyarsa ekle
   Modbus TCP : Sıfır — ağ mimarisi düzeyinde çöz (VPN, güvenlik duvarı)

5. IT / BULUT ENTEGRASYONU
   ──────────────────────
   MQTT   : En doğal — AWS IoT, Azure IoT Hub, Google Cloud IoT native
   OPC UA : PubSub (MQTT transport) ile buluta çıkabilir ama ağır
   Modbus : IT sistemleri anlamaz — gateway gerekir
   Ham TCP: IT sistemleri anlamaz — özel adaptör gerekir

6. CİHAZ EKOSİSTEMİ
   ─────────────────
   Modbus TCP : Dünya genelinde en geniş — VFD, enerji sayacı, akıllı röle, eski SCADA
   OPC UA     : Modern PLC'ler — Siemens, B&R, Beckhoff, CODESYS, Rockwell
   MQTT       : IoT sensörler, edge gateway'ler, Sparkplug B destekli cihazlar
   Ham TCP    : Standart protokol desteklemeyen her cihaz (barcode, özel kamera, robot)

7. MALİYET (Kurulum + Bakım)
   ──────────────────────────
   Modbus TCP : En düşük — kütüphane evrensel, kurulum dakikalar
   Ham TCP    : Orta — framing, state machine, test süreci gerekli
   MQTT       : Orta — broker altyapısı, topic tasarımı, LWT yapılandırması
   OPC UA     : Yüksek — PKI yönetimi, adres uzayı tasarımı, sertifika döngüsü
```

---

## Pratikte Nasıl Kullanılır

### Karar Ağacı — Adım Adım

```
ADIM 1: Karşı taraf ne destekliyor?
───────────────────────────────────
    Modbus TCP destekliyor?         → Modbus TCP (zorunlu, başka seçenek yok)
    OPC UA destekliyor?             → OPC UA (modern, güvenli, semantik)
    MQTT destekliyor?               → MQTT (bulut/IoT hedef ise ideal)
    Hiçbirini desteklemiyor?        → Ham TCP Socket (özel protokol adaptasyonu)
    RS-232 / RS-485 seri port?      → SysCom (seri haberleşme, TCP değil)

ADIM 2: Yön ve kontrol tipi ne?
────────────────────────────────
    SCADA → PLC setpoint yazar + alarm onaylar (bidirectional)
        → OPC UA zorunlu (Modbus TCP da yeterli ama güvenlik yok)
    
    PLC → N alıcıya veri gönder (SCADA + historian + bulut)
        → MQTT broker (pub/sub doğal çözüm)
    
    PLC → tek SCADA (basit izleme)
        → Modbus TCP veya OPC UA (ikisi de çalışır, OPC UA tercih)

ADIM 3: Güvenlik gereksinimi var mı?
──────────────────────────────────────
    IEC 62443, NIS2, ISO 27001 uyumluluk
        → OPC UA (SignAndEncrypt + rol tabanlı erişim) zorunlu
    
    Şifreleme yeterli, sertifika zorunlu değil
        → MQTT (TLS 8883) veya OPC UA Basic256Sha256
    
    Yalnızca ağ segmentasyonu (izole LAN)
        → Modbus TCP kabul edilebilir
    
    İki cihaz, kontrollü LAN, güvenlik riski düşük
        → Ham TCP kabul edilebilir

ADIM 4: Veri zenginliği ve yapısı ne?
──────────────────────────────────────
    16-bit tam sayı / float, basit setpoint-ölçüm
        → Modbus TCP yeterli
    
    Semantik model, struct, metod çağrısı, otomatik keşif
        → OPC UA zorunlu
    
    JSON / Protobuf, değişken yapı, metadata
        → MQTT (Sparkplug B ile şema)
    
    Büyük binary payload (görüntü, dalga şekli)
        → Ham TCP (overhead yok, maksimum bant genişliği)

ADIM 5: Ölçek ve büyüme planı?
────────────────────────────────
    1 PLC + 1 SCADA, sabit topoloji
        → OPC UA veya Modbus TCP
    
    Çok PLC, değişen alıcı sayısı (yeni sistem eklenebilir)
        → MQTT (UNS — yeni alıcı = yeni subscriber, PLC kodu değişmez)
    
    50+ PLC yönetimi
        → OPC UA PubSub (MQTT transport) — iki dünyanın birleşimi
```

---

## Örnekler

### Senaryo 1 — Gıda Fabrikası: PLC → SCADA Bağlantısı

**Durum:** Yeni CODESYS tabanlı paketleme hattı, Ignition SCADA ile entegre edilecek. SCADA hem hız setpointleri yazacak hem de alarm onaylayacak. IEC 62443 uyumluluk bekleniyor.

**Karar:** OPC UA

**Gerekçe:**
- Bidirectional kontrol: Setpoint yazma + alarm onaylama → OPC UA zorunlu
- Ignition SCADA: Native OPC UA client desteği var
- IEC 62443 uyumluluk: OPC UA Basic256Sha256 + SignAndEncrypt + rol tabanlı erişim
- CODESYS Symbol Configuration: Ek lisans gerekmez, yerleşik

**Reddedilen alternatifler:**
- Modbus TCP: Güvenlik yok, IEC 62443 karşılanamaz
- MQTT: Bidirectional setpoint yazma akışı belirsiz; komut yönü güvensiz

---

### Senaryo 2 — Enerji İzleme: 20 Farklı Marka Sayaç

**Durum:** Fabrikada 20 adet farklı marka enerji sayacı var. Hepsi Modbus TCP destekliyor, başka protokol yok. Python scripti saatlik enerji tüketim raporları üretecek.

**Karar:** Modbus TCP

**Gerekçe:**
- Tüm cihazlar Modbus TCP konuşuyor; başka seçenek yok
- pymodbus ile batch okuma: Tek FC03 isteğiyle 10 register
- Basit veri: kWh, gerilim, akım — 16-bit veya float (2 HR)
- Güvenlik: İzole fabrika LAN'ı, VLAN segmentasyonu yeterli

**Dikkat edilecek noktalar:**
- Her sayaç farklı byte order kullanabilir (float için big-endian test et)
- Thread lock: pymodbus istemci nesneleri thread-safe değil
- Port 502 asla internete açılmayacak

---

### Senaryo 3 — Endüstri 4.0 Dönüşümü: 12 PLC, Bulut + Historian + SCADA

**Durum:** 12 PLC'nin verisi aynı anda InfluxDB (historian), Grafana (dashboard), AWS IoT Core (bulut analitik) ve mevcut Ignition SCADA'ya gitmeli. Gelecekte yeni alıcılar eklenebilir.

**Karar:** OPC UA (SCADA için) + MQTT (Historian + Bulut için)

**Gerekçe:**
- SCADA → PLC bidirectional kontrol: OPC UA (setpoint, alarm)
- 12 PLC × 3 hedef (InfluxDB + Grafana + AWS): Her biri ayrı bağlantı = 36 bağlantı
- MQTT UNS: 12 PLC → broker (12 bağlantı) + 3 subscriber (3 bağlantı) = 15 bağlantı
- Yeni alıcı ekleme: Sadece yeni MQTT subscriber — PLC kodu değişmez
- 50 PLC'ye büyüme: OPC UA PubSub (MQTT transport) ile geçiş kolaylaşır

**Mimari:**
```
CODESYS PLC (×12)
    ├── OPC UA Server (port 4840)
    │   └── Ignition SCADA ← bidirectional kontrol
    └── MQTT Publisher (Task_Background, 500ms)
        └── EMQX Broker
            ├── InfluxDB (subscriber)
            ├── Grafana (subscriber, native MQTT)
            └── AWS IoT Core (subscriber, TLS 8883)
```

---

### Senaryo 4 — Barkod Okuyucu Entegrasyonu

**Durum:** Üretim hattında barkod okuyucu. Üretici belgesine göre "TCP server, port 4001, ASCII string + \r\n". Modbus, OPC UA veya MQTT desteği yok.

**Karar:** Ham TCP Socket

**Gerekçe:**
- Standart protokol desteği yok; başka seçenek yok
- Protokol tanımlı: ASCII + delimiter (\r\n) → framing basit
- CODESYS SysSock ile 30 dakikada entegrasyon (gerçek proje deneyimi)

**Uygulama:**
```
1. nc <cihaz_ip> 4001 → protokolü tanı
2. CODESYS: FB_TcpClient → Task_Background (connect() blocking!)
3. recv() loop: \r\n bulana kadar akümülatör buffer'a ekle
4. GVL_Barcode.sLastScan := barcode_string
5. Task_Control: GVL üzerinden barcode değerini kullan
```

---

### Senaryo 5 — İki PLC Arası Özel Veri Köprüsü

**Durum:** İki CODESYS PLC arasında 100ms periyotta 50 değişkenin senkronize edilmesi gerekiyor. Her iki PLC de kontrol edilebilir (protokol tasarımı serbest).

**Karar:** Ham TCP Socket (veya OPC UA — tradeoff var)

**Gerekçe (Ham TCP tercih edilirse):**
- Her iki taraf da kontrol edilebilir → özel protokol tasarlanabilir
- 50 değişken × 4 byte = 200 byte; tek frame, minimum overhead
- OPC UA'ya göre daha az kurulum karmaşıklığı (PKI, sertifika yönetimi yok)
- Latency: < 1ms (LAN, persistent connection)

**OPC UA tercih edilirse:**
- Eğer gelecekte üçüncü taraf SCADA da bu veriye erişecekse OPC UA'ya geç
- Eğer değişken listesi büyüyecek ve belgeleme kritikse OPC UA daha iyi
- Ham TCP: 2 PLC arasında sabit senaryo, değişken liste küçük, ekip küçük → yeterli

---

### Senaryo 6 — Uzak Pompa İstasyonu: 4G/LTE Bağlantısı

**Durum:** Şehir dışında pompa istasyonu, yalnızca 4G/LTE bağlantısı. Merkez SCADA operasyonel verileri ve alarmları izleyecek. Zaman zaman setpoint güncellemesi gerekebilir.

**Karar:** MQTT (telemetri + alarmlar) + OPC UA veya MQTT komut kanalı (setpoint)

**Gerekçe:**
- 4G/LTE kısıtlı bant: MQTT minimum overhead (2-byte sabit header)
- Bağlantısız çalışma: MQTT QoS 1 + session → broker bağlantı kesilse bile mesaj biriktir
- LWT: PLC kopunca merkez SCADA otomatik "Offline" görür
- Modbus TCP: 4G üzerinden polling → her istek round-trip gecikme + bağlantı kararsızlığı
- OPC UA: Session yönetimi 4G'de ağır; bağlantı kopunca session süresi dolana kadar belirsiz

**Topic tasarımı:**
```
pompa_istanbul_001/telemetry/flow_rate     QoS 0, retain=False
pompa_istanbul_001/telemetry/pressure      QoS 0, retain=False
pompa_istanbul_001/alarm/#                 QoS 1, retain=False
pompa_istanbul_001/status/online           QoS 1, retain=True (LWT="false")
pompa_istanbul_001/command/setpoint_flow   QoS 1, retain=False (SCADA → PLC)
```

---

### Senaryo 7 — İlaç Fabrikası: FDA 21 CFR Part 11 Uyumluluk

**Durum:** İlaç üretim hattı. FDA 21 CFR Part 11 uyumluluk zorunlu (audit trail, elektronik imza, erişim kontrolü). Üretici değişkenleri izleniyor, reçete yükleme metodu çağrılıyor.

**Karar:** OPC UA (Companion Specification PA-DIM / ISA-88 ile)

**Gerekçe:**
- FDA 21 CFR Part 11: Denetim izi, erişim kontrolü → OPC UA SecurityMode SignAndEncrypt
- Rol tabanlı kullanıcı yönetimi: Operatör (okuma), Mühendis (yazma), Yönetici (reçete)
- Metod çağrısı: `StartBatch(recipeId)`, `AbortBatch()` → OPC UA Method node zorunlu
- Companion Specification: PA-DIM (Process Automation) veya ISA-88 (batch) ile uyumluluk
- Semantik model: Cihaz ağacı, ürün parametreleri, batch geçmişi → adres uzayı hiyerarşisi

**Reddedilen alternatifler:**
- Modbus TCP: Güvenlik yok, audit trail yok, metod çağrısı yok
- MQTT: Erişim kontrolü broker ACL ile sınırlı, audit trail entegre değil
- Ham TCP: FDA uyumluluğu için belgelenmiş standart protokol zorunlu

---

### Senaryo 8 — SCADA Modernizasyonu: Eski Sistem Korunacak

**Durum:** Mevcut SCADA sadece Modbus TCP biliyor ve değiştirilemez (5 yıl daha kullanılacak). Yeni CODESYS PLC devreye alınacak. Paralelde bulut analitik de başlatılacak.

**Karar:** Modbus TCP (eski SCADA için) + MQTT (yeni bulut analitik için) — ikisi aynı anda

**Gerekçe:**
- Eski SCADA değiştirilemez → Modbus TCP zorunlu
- Yeni bulut analitik → MQTT ideal
- CODESYS: Aynı PLC'de hem Modbus Slave (port 502) hem MQTT Client çalışabilir
- İki protokol çakışmaz; farklı GVL'ler, farklı task'lar

**Uygulama:**
```
CODESYS PLC
    ├── ModbusTCP_Slave (port 502)
    │   GVL_Modbus: HR→setpoint, IR→ölçüm
    │   PRG_ModbusUpdate: Task_Slow (100ms)
    │   → Eski SCADA (Modbus TCP Master)
    │
    └── MQTT Client (Task_Background)
        PRG_MQTTPublish: Task_Slow (500ms)
        Topic: factory/line1/+/telemetry
        → EMQX Broker → InfluxDB → Grafana → AWS IoT
```

---

## Sık Yapılan Hatalar

### Yanlış Karar 1: MQTT ile SCADA Setpoint Yazımı

```
Senaryo : SCADA PLC'ye setpoint yazmak için MQTT kullanılıyor.
Sorun   : Pub/sub modelde komut yönü belirsiz. Broker ACL zayıfsa
          herhangi bir publisher setpoint değiştirebilir.
          Metod çağrısı yok; "yaz + onay" zinciri kurulamaz.
          Komut başarısız olursa PLC'nin geri bildirimi yok.
Çözüm   : SCADA ↔ PLC bidirectional kontrol için OPC UA.
          MQTT sadece PLC → dışarıya veri akışı için (publisher = PLC).
Kural   : MQTT pub/sub ve OPC UA client-server farklı güç alanlarıdır.
          Setpoint/alarm kanalı OPC UA; izleme/analitik kanalı MQTT.
```

### Yanlış Karar 2: Modbus TCP'yi "Basit ve Hızlı" Diye İnternete Açmak

```
Senaryo : Port 502 NAT arkasında açık bırakıldı (uzaktan erişim kolaylığı için).
Referans: 2024 FrostyGoop saldırısı — Ukrayna ısıtma sistemi, fiziksel hasar.
Etki    : Saldırgan Modbus komutları göndererek sistemde kalıcı hasar oluşturdu.
Kural   : Modbus TCP protokol düzeyinde sıfır güvenlik.
          Port 502 hiçbir zaman internete açılmaz.
          Uzak erişim için: VPN tüneli + MQTT/OPC UA üzerinde şifreli bağlantı.
```

### Yanlış Karar 3: OPC UA'yı "Pahalı Modbus" Olarak Kurmak

```
Senaryo : OPC UA kuruldu ama Address Space düz liste — 300 değişken aynı seviyede.
          NodeId'ler hardcode, ns=4. Subscription yok; her şey polling döngüsü.
          Güvenlik None mode. Sadece 1 istemci var.
Etki    : OPC UA'nın tüm avantajları (keşfedilebilirlik, semantik, push, güvenlik)
          kullanılmıyor. Modbus TCP'ye göre çok daha karmaşık ama daha zayıf.
Çözüm   : Bu senaryoda Modbus TCP daha doğru seçimdi.
          OPC UA seçilmişse: Hiyerarşik adres uzayı, Subscription, güvenlik kullan.
Kural   : OPC UA seçilmişse doğru kullan; yoksa Modbus TCP tercih et.
```

### Yanlış Karar 4: Ham TCP'yi Standart Protokol Yerine Kullanmak

```
Senaryo : Geliştirici "daha fazla kontrol" için Ham TCP seçti; karşı taraf OPC UA destekliyordu.
Etki    : Framing state machine, senkronizasyon kurtarma, versiyonlama, checksum,
          heartbeat — hepsini sıfırdan yazmak gerekti. 3 haftalık geliştirme.
          OPC UA ile 2 gün sürecek entegrasyon 3 haftaya uzadı.
          Yeni geliştirici projeye katılınca özel protokol anlaşılmaz geldi.
Kural   : Ham TCP YALNIZCA karşı taraf standart protokol desteklemiyorsa kullanılır.
          Standart protokol seçeneği varsa her zaman standart protokol tercih edilir.
```

### Yanlış Karar 5: MQTT Topic'ini Başta Düz Tasarlamak

```
Senaryo : Pilot projede topic'ler: "temp1", "speed_motor2", "alarm3".
Etki    : Fabrika genişleyince wildcard kullanılamadı. Tüm subscriber'lar güncellendi.
          InfluxDB eski yapıda veri kaldı; Grafana bozuldu. 2 günlük migrasyon.
Kural   : ISA-95 tabanlı hiyerarşiyi başta kur:
          enterprise/site/area/line/cell/device/datapoint
          Bu yapı bir daha değiştirilmez.
```

### Yanlış Karar 6: Her Şeye OPC UA Kurmak (Boyut Uyumsuzluğu)

```
Senaryo : Küçük ölçekli proje: 1 CODESYS PLC, 3 basit float değer, 1 Python monitoring
          script. Enerji ölçümü izleme uygulaması.
          "Kurumsal standard" için OPC UA kuruldu: PKI, sertifika yönetimi,
          güvenlik yapılandırması, namespace tasarımı.
Etki    : 3 saatte biten Modbus TCP entegrasyonu 3 günde bitti.
          Script geliştiricisi asyncua, sertifika döngüsü, namespace URI ile boğuştu.
Kural   : Senaryo küçükse, güvenlik zorunlu değilse, karşı taraf Modbus destekliyorsa →
          Modbus TCP seç. Protokol karmaşıklığı boyuta uygun olmalı.
```

### Yanlış Karar 7: MQTT'de LWT Olmadan Konuşlandırma

```
Senaryo : PLC beklenmedik kesildi. Dashboard 2 saat "Online" gösterdi.
Etki    : Operatör sorunu fark etmedi. 2 saat üretim kaybı.
Kural   : Her MQTT bağlantısında LWT zorunlu:
          LWT Topic:   factory/.../status/online
          LWT Payload: "false"    QoS: 1    Retain: True
          Bağlanınca:  "true" yayınla (QoS 1, retain=True)
          LWT olmayan MQTT sistemi eksik sistemdir.
```

---

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Karar Matrisi 1 — Senaryo → Protokol (Özet)

| Senaryo | Önerilen | Gerekçe |
|---|---|---|
| PLC → SCADA veri aktarımı (standart) | **OPC UA** | Semantik, güvenli, çok istemci |
| SCADA → PLC setpoint yaz + alarm onayla | **OPC UA** | Bidirectional kontrol zorunlu |
| PLC → SCADA + MES + ERP zinciri | **OPC UA** | Companion Spec, metod çağrısı |
| Legacy VFD / enerji sayacı entegrasyonu | **Modbus TCP** | Cihaz sadece Modbus konuşuyor |
| Eski SCADA yalnızca Modbus biliyor | **Modbus TCP** | Başka seçenek yok |
| Basit 2-3 değer, hızlı prototip | **Modbus TCP** | Gereksiz karmaşıklıktan kaçın |
| PLC → InfluxDB + Grafana + AWS aynı anda | **MQTT** | Pub/sub, N alıcı, broker fanout |
| Unified Namespace (UNS) mimarisi | **MQTT** | Merkezi veri havuzu |
| Bulut platform entegrasyonu (AWS/Azure) | **MQTT** | Cloud-native protokol |
| 4G/LTE uzak bağlantı | **MQTT** | Düşük overhead, QoS, bağlantısız çalışma |
| IEC 62443 / NIS2 / FDA uyumluluk | **OPC UA** | SignAndEncrypt + PKI + rol yönetimi |
| Barkod okuyucu / özel cihaz | **Ham TCP** | Standart protokol desteği yok |
| İki PLC arası özel köprü | **Ham TCP** | Overhead yok, protocol özgürlüğü |
| Büyük binary payload (görüntü, dalga) | **Ham TCP** | Standart protokol overhead'ı ağır |
| Gerçek zamanlı motion control (< 1ms) | **EtherCAT / PROFINET** | Bu 4 protokolden hiçbiri |
| OPC UA + çok alıcı ölçeklenebilir | **OPC UA PubSub (MQTT transport)** | İki dünyanın birleşimi |

---

### Karar Matrisi 2 — Protokol × Karar Kriteri

| Kriter | OPC UA | Modbus TCP | Ham TCP Socket | MQTT |
|---|---|---|---|---|
| **Latency (LAN)** | < 10ms | < 5ms | < 1ms | < 10ms + broker |
| **Güvenlik (yerleşik)** | Tam (PKI, TLS, rol) | Yok | Yok | TLS opsiyonel |
| **Keşfedilebilirlik** | Tam (Browse) | Yok | Yok | Kısmi (Sparkplug B) |
| **Bidirectional kontrol** | Tam | Sınırlı (polling) | Tasarıma bağlı | Zayıf (topic tabanlı) |
| **Push bildirimi** | Evet (Subscription) | Hayır (polling) | Tasarıma bağlı | Evet (doğal) |
| **N alıcıya dağıtım** | Orta (multi-session) | Zor (polling) | Zor | Doğal (broker) |
| **Bulut entegrasyonu** | Dolaylı (PubSub) | Hayır (gateway) | Hayır | Doğal |
| **Veri tipi zenginliği** | Çok zengin | 16-bit (zayıf) | Tasarıma bağlı | JSON/Protobuf |
| **Cihaz ekosistemi** | Modern PLC'ler | Evrensel (en geniş) | Özel cihazlar | IoT / edge |
| **Kurulum maliyeti** | Yüksek | Düşük | Orta-Yüksek | Orta |
| **Bağlantısız çalışma** | Hayır | Hayır | Hayır | Evet (QoS + session) |
| **CODESYS kurulum zorluğu** | Orta (Symbol Config) | Kolay (Device Tree) | Zor (SysSock + FB) | Orta (kütüphane + config) |

---

### Karar Matrisi 3 — İki Protokol Kombinasyonları

| Kombinasyon | Ne Zaman Kullanılır | Gerçek Örnek |
|---|---|---|
| OPC UA + Modbus TCP | Yeni OPC UA sistemi + legacy Modbus cihazlar | CODESYS PLC: OPC UA server (SCADA için) + Modbus slave (eski HMI için) |
| OPC UA + MQTT | SCADA kontrolü + bulut analitik | PLC: OPC UA → Ignition, MQTT → InfluxDB + AWS |
| Modbus TCP + MQTT | Eski SCADA değiştirilemez + bulut yeni ekleniyor | PLC: Modbus slave (eski SCADA) + MQTT publisher (yeni bulut) |
| OPC UA PubSub + MQTT | 50+ PLC yönetimi | 50 PLC → MQTT broker, SCADA tek noktadan abone |
| Ham TCP + OPC UA | Özel cihaz + SCADA | Barkod okuyucu (Ham TCP) + SCADA (OPC UA) aynı PLC'de |

---

## Gerçek Proje Notları

**Not 1 — "OPC UA mı Modbus mu?" Sorusunun Gerçek Cevabı**

Sahada en sık sorulan soru bu. Pratik cevap: "Karşı SCADA / HMI sistemi ne destekliyor?" Eski SCADA Modbus konuşuyorsa OPC UA kurmak için haftalarca plan yapmanın anlamı yok — Modbus TCP saatler içinde devreye girer, iş görür. OPC UA zamanı ise müşteri veya standart gerektirdiğinde, güvenlik şartnamesinde madde olarak geçtiğinde veya semantik model gerçekten değer kattığında gelir (robot entegrasyonunda Companion Spec sayesinde 2 günlük entegrasyon 4 saate indi — Not 2).

**Not 2 — Companion Specification ile Entegrasyon Süresinin %70 Kısalması**

Robot OEM'i OPC 40010 (Robotics Companion Spec) uyumlu server sundu. SCADA istemcisi aynı spec'i destekliyordu. Custom tag eşlemesi yazmak yerine standartta tanımlı node'lar direkt kullanıldı. Entegrasyon 2 günden 4 saate indi. Bu deneyimden sonra kural: OPC UA seçildiyse Companion Specification uyumluluğu satın alma şartnamesinin standart maddesi.

**Not 3 — Yanlış Protokol Seçiminin Gerçek Maliyeti (Ham TCP Yanılgısı)**

Bir projede geliştirici "daha fazla kontrol" için karşı taraf OPC UA desteklediği halde Ham TCP seçti. Framing, state machine, heartbeat, versiyonlama, checksum — her şeyi sıfırdan yazdı. OPC UA ile 2 günde biten entegrasyon 3 haftaya uzadı. 6 ay sonra yeni geliştirici projeye katıldı; özel protokolü anlamak 4 gün sürdü. Standart protokol seçeneği varken Ham TCP = sonraki herkes için teknik borç.

**Not 4 — UNS Mimarisinde "Bağlantı Patlamasından" Kurtulmak**

12 PLC, 3 hedef (SCADA + InfluxDB + AWS): Her PLC her hedefle konuşsaydı 36 bağlantı, 36 farklı erişim izni, 36 farklı hata senaryosu. MQTT UNS ile: 12 PLC broker'a bağlandı (12 bağlantı), 3 sistem subscriber oldu (3 bağlantı). Dördüncü sistem eklendi: 1 yeni subscriber, 0 PLC kodu değişikliği. Bakım yükü dramatik düştü. 50 PLC'ye büyüyünce fark daha da belirgin.

**Not 5 — 4G/LTE Ortamında Modbus TCP ile OPC UA Deneyimi**

Uzak pompa istasyonu projesinde başlangıçta OPC UA denendi. 4G bağlantısı kararsız olduğunda OPC UA session yönetimi sorunlu davrandı: Bağlantı kesilince session süresi dolana kadar (varsayılan 30 saniye) belirsizlik. Her yeniden bağlantıda PKI el sıkışması gerekti. MQTT'ye geçildi: QoS 1 + session store ile bağlantı kesilince broker mesajları biriktirdi, PLC yeniden bağlanınca teslim etti. LWT ile kopuş 30 saniyede tespit edildi. Kısıtlı bant ortamı için MQTT açık ara kazanan.

**Not 6 — Güvenlik "Sonra Eklerim" Tuzağı**

OPC UA ile kurulan sistemde başlangıçta SecurityMode None ile test yapıldı. Test bitti, "güvenliği sonra ekleriz" dendi. Üretim devreye alınmasına iki hafta kala güvenlik modu değiştirilmek istendi. SCADA istemcisinin sertifika yönetimi yoktu; istemci kodu yeniden yazılmalıydı. Ek iki haftalık gecikme. Kural: Güvenlik modu projenin başında seçilir, test ortamında da aktif tutulur.

**Not 7 — "Hangisi Daha Hızlı?" Sorusu Nadiren Doğru Soru**

LAN içi 10-50ms aralığında dört protokolün tamamı yeterlidir. Gerçek fark performansta değil, operasyonel özelliklerde: Modbus TCP polling gerektirir (push yok), OPC UA subscription push sağlar, MQTT zaten push. 100ms periyotta sürekli polling ile subscription karşılaştırıldığında ağ trafiği ve CPU farkı önemsizdir. "En hızlı protokol" sorusu yerine "Bu senaryo için gerçekten hangi özellikler gerekiyor?" sorusu sorulmalı.

---

## İlgili Konular

```
Bu belgenin birincil kaynakları (okuma sırası önerilir):
knowledge/protocols/
├── _synthesis.md                    → Karşılaştırmalı üst sentez (bu belgenin temeli)
├── opc-ua/_synthesis.md             → OPC UA uçtan uca sentez
├── modbus-tcp/_synthesis.md         → Modbus TCP uçtan uca sentez
├── mqtt/_synthesis.md               → MQTT uçtan uca sentez
└── tcp-socket/_synthesis.md         → Ham TCP Socket uçtan uca sentez

CODESYS implementasyon rehberleri:
knowledge/codesys/networking/
├── _synthesis.md                    → Dört protokolün CODESYS'teki uygulaması
├── 01_opcua_server.md               → OPC UA server adım adım kurulum
├── 02_modbus_slave.md               → Modbus TCP slave yapılandırması
├── 03_tcp_socket.md                 → SysSock implementasyon özeti
└── 04_mqtt_client.md                → MQTT client kurulumu

Mimari kararlar:
knowledge/decisions/
└── architecture/                    → Sistemin bütünü için mimari karar kayıtları

Temel önkoşullar:
knowledge/codesys/fundamentals/
└── _synthesis.md                    → Device Tree, GVL, Task yapısı

Araçlar:
  UaExpert         → OPC UA browser, NodeId keşif, subscription test
  Modbus Poll      → GUI Modbus master test
  MQTT Explorer    → GUI MQTT browser ve yayın testi
  netcat (nc)      → Ham TCP protokol keşfi: nc <IP> <port>
  Wireshark        → Tüm protokol trafik analizi
  pymodbus         → pip install pymodbus
  asyncua          → pip install asyncua[crypto]
  paho-mqtt        → pip install paho-mqtt
  Python socket    → Ham TCP test (stdlib)
```
