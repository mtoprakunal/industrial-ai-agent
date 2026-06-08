---
KONU        : HMI Domaini — Üst Sentez
KATEGORİ    : hmi
ALT_KATEGORI: hmi
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/hmi/architecture/_synthesis.md"
    başlık: "HMI Mimari — Sentez"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/web-based/_synthesis.md"
    başlık: "Web Tabanlı HMI Geliştirme — Sentez"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/hmi/architecture/_synthesis.md"
    ilişki: detaylandırır
  - konu: "knowledge/hmi/web-based/_synthesis.md"
    ilişki: detaylandırır
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/modbus-tcp/01_protocol_basics.md"
    ilişki: kullanır
  - konu: "knowledge/codesys/fundamentals/_synthesis.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "HMI Mimari alt sentezi (architecture/_synthesis.md)"
  - "Web Tabanlı HMI alt sentezi (web-based/_synthesis.md)"
  - "OPC UA ve Modbus TCP temel kavramları önerilir"
ÇELİŞKİLER :
  - kaynak: "architecture/_synthesis.md — polling her şeyi çözer algısı"
    konu: "Hem mimari katman hem web stack senkronize biçimde push modelini savunur; polling yalnızca Modbus legacy'de kaçınılmaz"
    çözüm: "OPC UA subscription + WebSocket broadcast standart seçim; polling yalnızca OPC UA sunucusu olmayan cihazlarda."
  - kaynak: "architecture/_synthesis.md — frontend yetkilendirme yeterli algısı"
    konu: "Web stack, yazma komutlarını WebSocket üzerinden gönderir; kimlik doğrulama hem frontend hook hem backend middleware'de zorunlu"
    çözüm: "usePermission() UI'da gizleme, requirePermission() + sessionToken backend'de doğrulama; ikisi birlikte uygulanmalı."
  - kaynak: "web-based/_synthesis.md — WSS olmadan üretime alma"
    konu: "ws:// açık metin komut riski; audit log gereksinimi ile birleşince hem güvenlik hem uyumluluk ihlali"
    çözüm: "Üretim ortamında wss:// (Nginx SSL termination) zorunlu; ilk günden tasarıma dahil edilmeli."
---

## Özün Ne

Bu belge, HMI domaininin tamamına ait üst haritadır. İki tamamlanmış alt sentezi — mimari katmanlar ve web tabanlı uygulama — tek bir zihinsel modelde birleştirir.

HMI domaini iki soru etrafında döner:

1. **Ne gösterilmeli, nasıl tasarlanmalı?** — ISA-101 ekran hiyerarşisi, alarm yönetimi (ISA-18.2), kullanıcı yetkilendirme (RBAC) ve bağlantı kopma davranışı: bunlar **mimari katman** sorunlarıdır.
2. **Veri PLC'den tarayıcıya nasıl akar?** — OPC UA/Modbus istemcileri, WebSocket sunucusu, React/Vue frontend ve state yönetimi: bunlar **web stack** sorunlarıdır.

İki katman birbirini önkoşul olarak gerektirir: Web stack veriyi taşır, mimari katman o veriye ne anlam yükleneceğini ve kimin ne yapabileceğini belirler. Birini diğersiz uygulamak eksik kalır.

Temel ayrım tek cümlede: Bir e-ticaret sitesinde yanlış düğme tıklandığında "Geri Al" vardır; bir motor kontrol HMI'ında yanlış komut fabrika durmasına veya yaralanmaya yol açabilir. Bu kritiklik her katmanı — tasarımdan protokol seçimine, alarm önceliğinden audit log saklama süresine — doğrudan etkiler.

## Nasıl Çalışır

### Tam Stack Zihin Haritası: PLC'den Operatöre

```
┌─────────────────────────────────────────────────────────────────────────────┐
│          ENDÜSTRİYEL WEB HMI — TAM STACK ZİHİN HARİTASI                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  SAHA / PLC KATMANI                                                           │
│  ┌──────────────────────────┐   ┌──────────────────────────┐                 │
│  │  CODESYS / Modern PLC    │   │  Legacy Modbus TCP Cihazı │                 │
│  │  opc.tcp://192.168.x:4840│   │  192.168.x:502            │                 │
│  └──────────────┬───────────┘   └──────────────┬────────────┘                │
│                 │ OPC UA Subscription (push)    │ Polling 500ms–1s            │
│                 ▼                               ▼                             │
│  BACKEND KATMANI — Node.js / TypeScript                                       │
│  ┌─────────────────────────────────────────────────────────┐                 │
│  │  OPCUAManager (node-opcua)   ModbusManager (jsmodbus)   │                 │
│  │  • Singleton bağlantı        • Singleton bağlantı       │                 │
│  │  • MonitoredItem / Sub       • setInterval toplu okuma  │                 │
│  │  • auto-reconnect            • auto-reconnect           │                 │
│  │              └────────────────────┘                     │                 │
│  │                 emit("tagUpdate")                        │                 │
│  │                        ▼                                │                 │
│  │           HMIWebSocketServer (ws, port 8080)            │                 │
│  │           • FULL_UPDATE (ilk bağlantıda)                │                 │
│  │           • TAG_UPDATE / BATCH_UPDATE (delta)           │                 │
│  │           • CONNECTION_STATUS                           │                 │
│  │           • WRITE_ACK (komut sonucu)                    │                 │
│  │           • Ping/Pong 30s keepalive                     │                 │
│  │                  +                                      │                 │
│  │           Yetkilendirme Middleware                       │                 │
│  │           requirePermission() + sessionToken doğrulama  │                 │
│  │           Audit log: Kim / Ne / Ne zaman / Önceki / Yeni│                 │
│  └─────────────────────────┬───────────────────────────────┘                 │
│                            │ wss:// (WebSocket Secure over TLS — üretimde)   │
│                            ▼                                                  │
│  FRONTEND KATMANI — Tarayıcı (React + Zustand  veya  Vue 3 + Pinia)          │
│  ┌─────────────────────────────────────────────────────────┐                 │
│  │  useWebSocket hook/composable → Singleton bağlantı      │                 │
│  │        ▼ onmessage                                       │                 │
│  │  State (Zustand / Pinia)                                 │                 │
│  │  tags: Record<string, TagValue>                          │                 │
│  │  connectionStatus | activeAlarms                         │                 │
│  │        ▼ granüler selector                               │                 │
│  │  Bileşenler: TagDisplay · AnalogGauge · StatusIndicator  │                 │
│  │             SetpointControl · AlarmBanner · TrendChart   │                 │
│  │                  +                                       │                 │
│  │  ISA-101 Tasarım Katmanı                                 │                 │
│  │  Ekran hiyerarşisi (4 seviye, ≤3 tıklama)               │                 │
│  │  Renk: Normal=Gri · Uyarı=Sarı · Alarm=Kırmızı(YALNIZ)  │                 │
│  │  Bağlantı kopunca: Kırmızı banner + yazma kilidi         │                 │
│  │                  +                                       │                 │
│  │  usePermission() → UI gizleme (devre dışı değil)         │                 │
│  └─────────────────────────┬───────────────────────────────┘                 │
│                            │                                                  │
│                            ▼                                                  │
│  OPERATÖR                                                                     │
│  ISA-101 uyumlu nötr/gri ekran · Alarm listesi (ISA-18.2) · RBAC rolleri     │
│  ≤3 tıklama navigasyon · Bağlantı durumu görünür · Audit iz kaydı            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Mental Model: Bir Komut Akışında Tüm Katmanlar

```
SENARYO: Operatör paketleme hattı motor setpointini değiştirip
         aşırı sıcaklık alarmını yönetir.

1. EKRAN NAVIGASYONU — Mimari Katman (ISA-101)
   Dashboard → Tıklama 1 → Hat 1 → Tıklama 2 → Motor Detay (≤3 tıklama)
   Ekranda motor simgesi nötr gri + "ÇALIŞIYOR" metni.

2. GERÇEKLİK VERİSİ — Web Stack (OPC UA → WebSocket → React/Vue)
   Motor hızı: OPC UA subscription (200ms sampling)
   → Backend OPCUAManager emit("tagUpdate")
   → HMIWebSocketServer broadcast TAG_UPDATE
   → Frontend store günceller → AnalogGauge yeniden render

3. SETPOINT DEĞİŞTİRME — Web Stack + Yetkilendirme
   Operatör değer girer → [Uygula]
   Frontend: usePermission('setpoint.write') → kontrol görünür
   WebSocket: WRITE_REGISTER { tag, value, sessionToken }
   Backend: validateSessionToken() → requirePermission('setpoint.write')
   → session.writeSingleNode(nodeId, yeniDeğer)
   → Audit log: { user, tag, prev, new, time }
   → WRITE_ACK → Frontend onay gösterir

4. ALARM TETİKLENME — Mimari Katman (ISA-18.2)
   Motor sıcaklığı 88°C (limit 85°C) → PLC alarm koşulu aktif
   Backend: ALARM mesajı → WebSocket broadcast
   Frontend: ACTIVE_UNACK → Alarm listesi (Yüksek öncelik, yanıp söner + siren)
   Tüm ekranlarda alarm banner görünür

5. ALARM ONAYLAMA — Mimari + Yetkilendirme
   Operatör alarm mesajını okur ("Motor 1 Sıcaklık — FR Panel kontrol et")
   [Onayla] → requirePermission('alarm.ack') → ACTIVE_UNACK → ACTIVE_ACK
   Siren durur, alarm listede turuncu/sabit kalır (koşul aktif = hâlâ listede!)

6. BAĞLANTI KOPMA — Web Stack (Stale Data + UI Kilidi)
   OPC UA bağlantısı kesildi:
   → CONNECTION_STATUS: DISCONNECTED broadcast
   → Frontend: Tüm değerler gri+italik (stale data overlay)
   → "PLC BAĞLANTISI KESİLDİ" kırmızı banner
   → Tüm yazma butonları disabled={!isConnected}
   → Backend: 3s aralıkla auto-reconnect
   Bağlantı geri gelince: FULL_UPDATE → tüm değerler yenilenir (delta yetmez)
```

Bu altı adım eş zamanlı çalışır. Her katmanın işlevi ayrıdır:
- **Web stack** veriyi taşır ve komutları iletir.
- **Mimari katman** o verinin nasıl gösterileceğini, alarm önceliğini, kimin ne yapabileceğini ve ne yaptığının izini belirler.

## Hızlı Referans Tabloları

### Tablo 1: HMI Teknoloji Seçimi — Web vs Masaüstü vs Panel-HMI

| Yaklaşım | Ne Zaman | Avantaj | Dezavantaj |
|---|---|---|---|
| Web HMI (React/Vue + WebSocket) | Özel proje, platform bağımsızlık, Git/CI-CD isteniyorsa | Sıfır lisans, modern UX, her tarayıcıdan erişim | Alarm/historian kendin yazarsın; WSS + güvenlik altyapısı gerekir |
| SCADA Platformu (Ignition, WinCC) | Büyük tesis (100+ ekran), historian kritik, hızlı geliştirme | Alarm/historian/reporting dahili; tag bağlama hızlı | Yüksek lisans maliyeti, vendor bağımlılığı |
| CODESYS WebVisu / TargetVisu | CODESYS PLC projesi, küçük panel | PLC ile aynı ortam, doğrudan değişken bağlama; sıfır ayrı backend | Sınırlı UI esnekliği, büyük projelerde performans sınırı |
| Panel HMI (Siemens KTP, Weintek) | Makine başında sabit dokunmatik ekran | Donanım entegrasyonu basit, dayanıklı | Kısıtlı yazılım esnekliği; web erişimi yok |

### Tablo 2: Mimari Katman Sorumlulukları

| Katman | Temel Soru | Standart / Araç | Alt Sentez |
|---|---|---|---|
| Ekran Tasarımı | Operatör neyi, nerede, kaç tıklamada görür? | ISA-101 | architecture/_synthesis.md |
| Gerçek Zamanlı Veri | Tag ne zaman, hangi protokolle, hangi hızda güncellenir? | OPC UA Sub / Modbus Polling | architecture/_synthesis.md + web-based/_synthesis.md |
| Alarm Yönetimi | Hangi koşul alarm, hangi öncelikle, hangi durum makinesinde? | ISA-18.2 | architecture/_synthesis.md |
| Kullanıcı Yetkilendirme | Kim neyi yapabilir, her eylem izlenebilir mi? | RBAC + JWT + Audit Log | architecture/_synthesis.md |
| Protokol İstemcisi | PLC verisi backend'e nasıl akar? | node-opcua / jsmodbus | web-based/_synthesis.md |
| Realtime Transport | Veri backend'den tarayıcıya nasıl iletilir? | WebSocket (ws/wss) | web-based/_synthesis.md |
| Frontend State | Tag değerleri bileşenlere nasıl dağıtılır? | Zustand / Pinia | web-based/_synthesis.md |

### Tablo 3: Realtime Veri — Protokol ve Hız Özeti

| Tag Tipi | Güncelleme Hızı | Protokol | Yöntem |
|---|---|---|---|
| Alarm / güvenlik biti | < 100ms | OPC UA | Subscription (samplingInterval: 100ms) |
| Motor çalışma durumu | 100–200ms | OPC UA | Subscription |
| Anlık ölçüm (hız, akım) | 200–500ms | OPC UA | Subscription |
| Sıcaklık, basınç | 500ms–1s | OPC UA veya Modbus | Subscription veya polling |
| Sayaç, üretim toplamı | 1–5s | OPC UA | Subscription (yavaş) |
| Enerji tüketimi | 5–60s | Modbus / MQTT | Polling veya broker |
| Vardiya raporları | Dakika/vardiya | REST API | Veritabanı sorgusu |

### Tablo 4: ISA-18.2 Alarm Öncelik Özeti

| Öncelik | Renk | Tepki Süresi | Maks Oran | Örnek |
|---|---|---|---|---|
| 1 — Kritik | Kırmızı + yanıp söner | 5–15 saniye | Toplam ≤ %5 | Acil durdurma, yangın/gaz |
| 2 — Yüksek | Turuncu | 5–10 dakika | Toplam ≤ %15 | Motor arızası, sıcaklık aşımı |
| 3 — Orta | Sarı | Saatler | — | Filtre basınç farkı |
| 4 — Düşük | Mavi | Vardiya içinde | — | Bakım bildirimi |

Kilit sınır: **< 10 alarm / 10 dakika** operatör başına (ISA-18.2).

### Tablo 5: RBAC Rol–Eylem Matrisi Özeti

| Eylem | Viewer | Operatör | Teknisyen | Mühendis | Admin |
|---|---|---|---|---|---|
| Ekran görüntüleme | ✓ | ✓ | ✓ | ✓ | ✓ |
| Setpoint yazma | ✗ | ✓ | ✓ | ✓ | ✓ |
| Motor start/stop | ✗ | ✓ | ✓ | ✓ | ✓ |
| Alarm onaylama | ✗ | ✓ | ✓ | ✓ | ✓ |
| Alarm bastırma (shelve) | ✗ | ✗ | ✓ | ✓ | ✓ |
| Alarm limiti değiştirme | ✗ | ✗ | ✗ | ✓ | ✓ |
| Kullanıcı yönetimi | ✗ | ✗ | ✗ | ✗ | ✓ |

### Tablo 6: WebSocket Mesaj Tipleri — Hızlı Başvuru

| Mesaj Tipi | Yön | Ne Zaman |
|---|---|---|
| `FULL_UPDATE` | Sunucu → Tarayıcı | Yeni bağlantı; reconnect sonrası (delta yetmez) |
| `TAG_UPDATE` | Sunucu → Tarayıcı | Tek tag değişiminde |
| `BATCH_UPDATE` | Sunucu → Tarayıcı | 100ms içindeki değişimleri toplu (50+ tag, 10+ istemci) |
| `CONNECTION_STATUS` | Sunucu → Tarayıcı | PLC bağlantı değişiminde (CONNECTED / DISCONNECTED / DEGRADED) |
| `WRITE_ACK` | Sunucu → Tarayıcı | Yazma komutu sonucu |
| `WRITE_REGISTER` | Tarayıcı → Sunucu | Operatör setpoint değiştirince (sessionToken zorunlu) |
| `WRITE_COIL` | Tarayıcı → Sunucu | Operatör boolean komut (sessionToken zorunlu) |
| `PING` / `PONG` | Her iki yön | 30s keepalive; 60s yanıt gelmezse terminate |

## Pratikte Nasıl Kullanılır

### "Sıfırdan Web HMI" Üst Düzey Kontrol Listesi

Aşağıdaki liste iki alt sentezin kontrol listelerini domain düzeyinde özetler. Her adım için ayrıntı ilgili alt sentezde bulunur.

**Mimari Kararlar — architecture/_synthesis.md**

```
□ 1. Teknoloji seç: Web HMI / SCADA Platform / Panel-HMI
     (bkz. Tablo 1: HMI Teknoloji Seçimi)

□ 2. ISA-101 ekran tasarımı:
     Normal = gri · Uyarı = sarı · Alarm = kırmızı (YALNIZCA)
     4 seviye hiyerarşi · ≤ 3 tıklama kuralı

□ 3. ISA-18.2 alarm sistemi:
     Alarm vs Event ayrımı · 4 öncelik seviyesi
     State machine: ACTIVE_UNACK → ACTIVE_ACK → RTN → NORMAL
     < 10 alarm / 10 dakika sınırı

□ 4. RBAC rol hiyerarşisi:
     VIEWER → OPERATOR → TECHNICIAN → ENGINEER → ADMIN
     Audit log: Her yazma kim/ne/ne zaman/önceki/yeni değer
```

**Web Stack — web-based/_synthesis.md**

```
□ 5. Backend: Node.js + TypeScript
     OPCUAManager (node-opcua) veya ModbusManager (jsmodbus)
     → Singleton bağlantı · auto-reconnect · emit("tagUpdate")

□ 6. WebSocket sunucusu (ws paketi, port 8080):
     FULL_UPDATE (ilk bağlantı) · TAG_UPDATE (delta) · WRITE_ACK
     Ping/Pong 30s · Ölü bağlantı cleanup

□ 7. Frontend state (Zustand veya Pinia):
     tags: Record<string, TagValue>
     connectionStatus · activeAlarms

□ 8. Frontend bileşenler:
     TagDisplay · AnalogGauge · StatusIndicator
     SetpointControl · ConnectionBanner · AlarmBanner

□ 9. Bağlantı kopma:
     Kırmızı banner · Stale data overlay (gri+italik)
     Tüm yazma butonları: disabled={!isConnected}

□ 10. Yetkilendirme (iki katmanlı):
      Frontend: usePermission() → UI gizleme
      Backend: requirePermission() + sessionToken → her endpoint

□ 11. Üretim:
      wss:// (Nginx SSL termination) · HTTPS · Oturum zaman aşımı 15 dk
```

### İki Alt Sentezi Birbirinden Ayıran Pratik Kural

- **Tasarım sorusu** (ISA-101 renk, alarm sayısı, rol izinleri, audit log) → `architecture/_synthesis.md`
- **Uygulama sorusu** (node-opcua parametre, Zustand selector, WebSocket mesaj tipi, Nginx WSS yapılandırması) → `web-based/_synthesis.md`
- **Seçim sorusu** (web vs SCADA, OPC UA vs Modbus, React vs Vue) → Bu belge (Tablo 1 ve "Ne Zaman Hangi HMI Yaklaşımı" bölümü)

## Sık Yapılan Hatalar

Bu bölüm iki alt sentezdeki hataları domain düzeyinde özetler; ayrıntılar ilgili alt sentezde açıklanmaktadır.

### Mimari Katman Hataları

**1. ISA-101 ihlali — Renk bolluğu**
Normal durumda yeşil/kırmızı kullanılınca alarm geldiğinde "hangi kırmızı alarm?" sorusu ortaya çıkar. Normal durum her zaman nötr/gri; renk yalnızca anomali için.

**2. Alarm bolluğu**
ISA-18.2 sınırı: < 10 alarm / 10 dakika. Müdahale gerektirmeyen bildirimler Event log'a gönderilmeli; alarm listesine eklenmemeli. Aksi hâlde alarm körlüğü → kritik alarm kaçırılır → fiziksel hasar.

**3. Acknowledge = Çözüldü sanmak**
Alarm onaylandıktan sonra listeden silmek büyük hatadır. ACTIVE_ACK durumu "gördüm" demektir; koşul aktifse listede kalmaya devam eder.

**4. Yetkilendirme yalnızca frontend'de**
`usePermission()` UI gizleme sağlar ama API doğrudan çağrılabilir. `requirePermission()` + `sessionToken` doğrulaması backend middleware'de her endpoint için zorunludur.

**5. Paylaşılan hesap kullanmak**
"Herkes operator/1234 kullanıyor" → audit log anlamsız → hesap verilebilirlik sıfır. Her kullanıcının kendi hesabı olmalı.

### Web Stack Hataları

**6. Singleton bağlantı yerine bileşen başına WebSocket/OPC UA**
50 widget × kendi bağlantısı → backend CPU %80+. Hem OPC UA manager hem WebSocket hook singleton olmalı.

**7. Bağlantı kopmasını sessizce geçiştirmek**
Gerçek vaka: 20 dakika önce bağlantı kesilmiş, ekran 68°C gösteriyordu, gerçekte 92°C'ye ulaşmıştı → motor hasar gördü. Bağlantı kopunca görünür overlay + yazma kilidi ilk günden tasarlanmalı.

**8. Reconnect sonrası yalnızca delta göndermek**
Bağlantı kopuk süresinde değişen değerler kaybolur. Reconnect'te her zaman FULL_UPDATE.

**9. wss:// olmadan üretime almak**
ws:// açık metin → IT güvenlik denetiminde acil düzeltme gerektirir. Nginx SSL termination + wss:// baştan planlanmalı.

**10. OPC UA namespace index hardcode**
`ns=4` farklı runtime versiyonunda `ns=3` veya `ns=5` gelebilir. Her session başlangıcında `session.getNamespaceIndex(uri)` ile dinamik alınmalı.

## Ne Zaman Hangi HMI Yaklaşımı

### Ne Zaman Web HMI?

```
Web HMI seç:
  ✓ Platform bağımsızlık kritik (tarayıcıdan her cihazdan erişim)
  ✓ Git ile versiyon kontrolü ve CI/CD pipeline isteniyor
  ✓ Özel UX gereksinimleri (standart SCADA widget'ları yetmiyor)
  ✓ Sıfır lisans maliyeti tercih ediliyor
  ✓ Küçük-orta ölçek, hem PLC hem frontend bilen mühendis var
  ✓ node-opcua veya jsmodbus ile PLC bağlantısı kurulabilir

Dezavantajı kabul et:
  ✗ Alarm yönetimi, historian ve raporlama sıfırdan yazılır
  ✗ wss:// + güvenlik altyapısı ek iş yükü gerektirir
```

### Ne Zaman SCADA Platformu (Ignition, WinCC)?

```
SCADA Platform seç:
  ✓ 100+ ekran, hızlı geliştirme gereksinimi
  ✓ Historian (geçmiş veri) ve raporlama kritik
  ✓ Ekip OT geliştirme biliyor, frontend bilmiyor
  ✓ ISA-18.2 alarm yönetimi dahili kullanılacak
  ✓ Vendor destek sözleşmesi (SLA) gerekli
```

### Ne Zaman OPC UA, Ne Zaman Modbus?

```
OPC UA seç (standart tercih):
  ✓ CODESYS, Siemens TIA, Beckhoff gibi modern PLC
  ✓ Subscription (push) modeli — polling yok
  ✓ Veri kalitesi (GOOD/BAD/UNCERTAIN) önemli
  ✓ Sertifika tabanlı güvenli bağlantı gerekiyor
  ✓ Struct, array veya method call gibi karmaşık veri modeli

Modbus seç (kaçınılmaz ise):
  ✓ OPC UA sunucusu olmayan legacy PLC veya I/O cihazı
  ✓ Register haritası belgelenmiş ve sabit
  ✓ Basit int/float veri, struct gerekmez
  Zorunlu: Toplu okuma (max 125 register/istek) + değişim filtresi
```

### Ne Zaman React, Ne Zaman Vue?

```
React seç:
  ✓ Büyük/karmaşık uygulama (100K+ satır, 20+ geliştirici)
  ✓ Ekip React biliyor; TypeScript entegrasyonu çok kritik
  ✓ Mobil (React Native) de planlanıyor
  Dikkat: React.memo / useMemo / granüler selector optimizasyonu zorunlu

Vue 3 seç:
  ✓ Orta ölçek, hızlı prototipleme (daha az boilerplate)
  ✓ Ekip JS biliyor ama framework'e yeni
  ✓ Pinia Proxy tabanlı reaktivite ekstra optimizasyon gerektirmiyor
  ✓ 200 tag, 50 güncelleme/s → Vue CPU %18 (React memo'suz %60+)
```

### Ne Zaman Batch Update Ekle?

```
Ekle:
  ✓ 50'den fazla tag aynı 500ms dilimde değişiyor
  ✓ 10'dan fazla eş zamanlı WebSocket istemcisi
  Etki: 80 tag × 20 istemci = 1600 mesaj/s → BATCH ile 20 mesaj/s

Ekleme:
  ✗ Az tag, az istemci → karmaşıklık değmez
  ✗ Gecikme toleranssız kritik alarmlar → o tag'ler için anlık TAG_UPDATE
```

## İlgili Konular

```
knowledge/hmi/                        ← Şu an buradasınız (üst sentez)
├── _synthesis.md                     → Bu belge
│
├── architecture/                     ← TAMAMLANDI
│   ├── 01_hmi_patterns.md            → ISA-101 mimari çerçeve, ekran hiyerarşisi
│   ├── 02_realtime_data.md           → OPC UA sub, Modbus polling, stale data
│   ├── 03_alarm_management.md        → ISA-18.2, alarm state machine, flood önleme
│   ├── 04_user_auth.md               → RBAC, JWT, audit log, oturum yönetimi
│   └── _synthesis.md                 → Dört mimari katmanın sentezi
│
├── web-based/                        ← TAMAMLANDI
│   ├── 01_opcua_clients_js.md        → node-opcua backend detayları
│   ├── 02_modbus_clients_js.md       → jsmodbus backend detayları
│   ├── 03_react_patterns.md          → React + Zustand HMI desenleri
│   ├── 04_vue_patterns.md            → Vue 3 + Pinia HMI desenleri
│   ├── 05_realtime_websocket.md      → WebSocket sunucu/istemci tam implementasyon
│   └── _synthesis.md                 → Web stack beş belgesinin sentezi
│
├── desktop/                          ← HENÜZ DOLDURULMADI (gelecekte eklenecek)
│   └── (stub)                        → Masaüstü HMI uygulamaları, WPF/Qt, yerel kurulum
│
└── ix-developer/                     ← HENÜZ DOLDURULMADI (gelecekte eklenecek)
    └── (stub)                        → ABB IX Developer, panel HMI programlama

Protokol katmanı:
knowledge/protocols/
├── opc-ua/
│   ├── 01_architecture.md            → OPC UA sunucu mimarisi
│   └── 04_subscriptions.md           → MonitoredItem parametre teorisi
└── modbus-tcp/
    ├── 01_protocol_basics.md         → Modbus TCP temelleri
    └── 02_register_model.md          → Register adresleme ve ölçekleme

PLC tarafı:
knowledge/codesys/
└── fundamentals/_synthesis.md        → CODESYS Runtime + Proje + Diller sentezi

Standartlar:
  ISA-101.01-2015    → HMI tasarım standardı (ekran, renk, navigasyon)
  ISA-18.2-2016      → Alarm yönetimi yaşam döngüsü
  IEC 62443          → OT siber güvenlik
  FDA 21 CFR Part 11 → Elektronik kayıt ve imza (ilaç sektörü, audit log saklama)

Araçlar:
  node-opcua / asyncua    → OPC UA istemci/sunucu kütüphaneleri
  jsmodbus / modbus-serial→ Modbus TCP/RTU JavaScript istemcileri
  Zustand                 → React state yönetimi (HMI için önerilir)
  Pinia                   → Vue 3 state yönetimi (resmi, önerilir)
  ws (npm)                → Node.js WebSocket sunucusu
  wscat                   → WebSocket CLI test: wscat -c ws://localhost:8080
  Ignition (Ind. Automation) → Büyük ölçek SCADA/HMI platform
  InfluxDB + Grafana      → Monitoring/analytics (salt okuma dashboard)
```
