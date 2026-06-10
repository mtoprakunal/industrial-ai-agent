# Karar Verme Çerçevesi

Bu belge agent'ın mühendislik kararlarını *nasıl* verdiğini tanımlar. Katı eşik kuralları değil, gerekçeli akıl yürütme sunar. Somut teknik temel `/knowledge/` altındadır — bu belge o bilgiyi karar anında nasıl kullanacağını anlatır.

> **Temel ilke:** Her karar gözlemlenebilir bir gereksinimden doğmalı ve tek cümlede gerekçelendirilebilmeli. Gerekçesini söyleyemediğin kararı verme.

Her önemli karar şu üçlüyle sunulur:
```
KARAR:   <ne seçildi>
GEREKÇE: <hangi gereksinimden doğdu>
TAKAS:   <neyi feda ettin / risk>
```

---

## 1. Protokol Seçimi

Referans: `/knowledge/protocols/_synthesis.md` (karşılaştırmalı üst sentez — her zaman önce oku).

### Önce ekseni belirle, sonra ilkeyi kur
Protokol seçimi **üç eksende** yapılır, sağlam kurulum **üç ortak ilkeyle** korunur. Yanlış eksen = baştan yanlış protokol. İhlal edilen ilke = doğru protokol kötü kurulum.

**Üç eksen (hangisini?):**
1. **Zenginlik ↔ Basitlik** — OPC-UA (zengin model) ↔ Modbus (16-bit register) ↔ ham TCP (byte)
2. **Güvenlik** — OPC-UA (yerleşik PKI) ↔ MQTT (TLS ops.) ↔ Modbus/TCP (sıfır → ağ koruması zorunlu)
3. **Push ↔ Poll** — MQTT (broker push) ↔ OPC-UA (subscription) ↔ Modbus (poll)

**Üç ortak ilke (nasıl sağlam?):**
1. **Tek-yazar** — her register/node/topic'in tek yazarı olmalı.
2. **Bloke-I/O ayrımı** — ağ çağrıları (connect, session, broker) Freewheeling task'ta; kontrol döngüsünü dondurmamalı.
3. **Raporlama ≠ kontrol** — dördü de raporlama katmanı; <1ms motion için EtherCAT/PROFINET.

### Her protokol seçiminde sorulacak sorular
1. **Karşı taraf ne destekliyor?** Legacy VFD/sayaç → Modbus. Modern PLC → OPC-UA. IoT/bulut → MQTT. Hiçbiri → ham TCP.
2. **Kaç alıcı, hangi yön?** Tek alıcı + setpoint yaz → OPC-UA/Modbus. N alıcı (SCADA+historian+bulut) → MQTT.
3. **Güvenlik kritik mi?** IEC 62443/NIS2 → OPC-UA SignAndEncrypt. Sadece şifreleme → MQTT TLS. Sadece segmentasyon → Modbus.
4. **Veri ne kadar zengin?** 16-bit setpoint → Modbus. Struct/metod/keşif → OPC-UA. Büyük binary → ham TCP.
5. **Gerçek zaman mı?** <1ms motion → bu 4'ten hiçbiri; fieldbus.

### Tipik sonuçlar (eğilim, kural değil)
| Protokol | Ne zaman | Bedeli |
|----------|----------|--------|
| **OPC-UA** | Karmaşık veri, çok istemci, güvenlik, uzun ömür, bidirectional kontrol | Ağır kurulum (PKI, namespace, session) |
| **Modbus TCP** | Basit register, legacy/evrensel uyumluluk | Tipsiz, güvenliksiz, push yok |
| **TCP Socket** | Özel protokol, niş cihaz, tam kontrol | Framing/state machine'i sen yazarsın |
| **MQTT** | Telemetri, bulut, N alıcı, kesintili bağlantı | SCADA kontrol döngüsü için değil |

> Endüstride **kombinasyon hakimdir**: OPC-UA + Modbus (legacy), OPC-UA + MQTT (kontrol + bulut). "Tek doğru protokol" arama; her veri akışına ekseninde en uygun olanı ata.

---

## 2. Task Yapısı Tasarımı

Referans: `/knowledge/codesys/task-structure/`.

### Temel kural
**Her sinyalin gecikme toleransı, atandığı task'ın cycle time'ını belirler.** Hızlı sinyal yavaş task'a, yavaş kod hızlı task'a konmaz.

### Sorulacak sorular
1. Bu mantık ne kadar hızlı tepki vermeli? (gecikme toleransı)
2. Bloke edebilir mi? (ağ, dosya, seri → evetse Freewheeling)
3. Diğer task'larla veri paylaşıyor mu? (tek-yazar disiplini)
4. CPU yükü ne? (toplam hedef ≤ %70)

### Task atama tablosu (`rules.json` timing ile senkron)
| Mantık | Task | Cycle | Öncelik |
|--------|------|-------|---------|
| E-Stop, ışık perdesi | Safety | ≤1 ms | En yüksek |
| Servo/VFD, EtherCAT senkron | Task_Motion | ≤2 ms | 1–5 |
| Hızlı interlock, encoder | Task_Fast | ≤4 ms | düşük sayı |
| PID, analog, sıralama | Task_Control | 10–20 ms | orta |
| OPC-UA/Modbus/HMI | Task_Comm | ≤500 ms | düşük |
| MQTT, log, dosya, **connect()** | Task_Background (Freewheeling) | best-effort | en düşük |

> **Kritik tuzak:** `SysSockConnect`, MQTT broker bağlantısı, dosya yazma → asla Task_Control'de. Bloke ederse watchdog tetiklenir, motorlar durur (gerçek saha vakası — bkz. `/knowledge/protocols/_synthesis.md` Hata 6).

---

## 3. HMI Teknolojisi Seçimi

Referans: `/knowledge/hmi/`, `/knowledge/decisions/hmi-technology/`.

| Senaryo | Eğilim |
|---------|--------|
| Çok kullanıcı, uzaktan tarayıcı erişimi | Web (React / Vue) |
| Sahada panel PC, dokunmatik | iX Developer veya web kiosk |
| Mühendislik istasyonu, zengin masaüstü | PyQt / .NET |
| Hızlı prototip, mevcut Python ekibi | Python + OPC-UA istemci |
| Sertifikalı endüstriyel HMI gereksinimi | iX Developer |

**Sorulacak sorular:** Kim kullanacak? Nereden erişecek (saha/uzak)? Ekip hangi teknolojide rahat? Sertifikasyon gerekli mi? Köprü protokolü ne?

Kullanıcının açık tercihi varsa ona uy; yalnızca tercih bir gereksinimle çelişiyorsa belirt.

---

## 4. Mimari Kararı

Referans: `/knowledge/decisions/architecture/`, `/knowledge/networking/`.

1. **Tek PLC mi, dağıtık mı?** — I/O coğrafi dağınıksa veya bölgeler bağımsız çalışabilmeliyse dağıtık.
2. **Kontrol nerede?** — Gerçek-zaman ve emniyet PLC'de; yorumlama/loglama/ağır hesap üst katmanda.
3. **HMI köprüsü protokoldür** — HMI asla PLC mantığına gömülmez.
4. **Veri akış yönü** — Kontrol döngüsü (deterministik) ≠ telemetri akışı (best-effort). Ayır.
5. **Tek hata noktası** — Emniyet zinciri yazılıma bağımlı olamaz (bkz. `safety_principles.md`).
6. **Ağ segmentasyonu** — OT ağı ile IT/ofis ağı ayrılır (IEC 62443).

---

## 5. Gerekçe Şablonları

Her karar tipi için doldurulacak iskelet:

**Protokol:**
```
KARAR:   {protokol} seçildi.
GEREKÇE: {kaç alıcı / yön / güvenlik / veri zenginliği} gereksinimi bunu gerektiriyor.
         Eksen analizi: {zenginlik/güvenlik/push-poll konumu}.
ALT:     {alternatif protokol} da mümkündü; {hangi koşulda} daha iyi olurdu.
TAKAS:   {feda edilen} — {nasıl yönetilecek}.
RİSK:    {tek-yazar / bloke-I/O / güvenlik} ilkesi şöyle korunacak: ...
```

**Task:**
```
KARAR:   {mantık} → {task}, cycle {ms}, öncelik {n}.
GEREKÇE: Gecikme toleransı {ms}; {bloke edip etmediği}.
TAKAS:   {CPU yükü / jitter} — toplam yük %{n}, hedef ≤%70.
```

**HMI:**
```
KARAR:   {teknoloji} seçildi.
GEREKÇE: {kullanıcı/erişim/ekip} gereksinimi.
ALT:     {alternatif}; {koşulda} tercih edilirdi.
TAKAS:   {feda edilen}.
```

Bu şablonlar `project_report.md` "Kararlar" bölümünün temelidir.
