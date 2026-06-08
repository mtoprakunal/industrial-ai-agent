---
KONU        : HMI Mimari — Sentez
KATEGORİ    : hmi
ALT_KATEGORI: architecture
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "knowledge/hmi/architecture/01_hmi_patterns.md"
    başlık: "HMI Mimari Kalıpları"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/architecture/02_realtime_data.md"
    başlık: "HMI'da Gerçek Zamanlı Veri Yönetimi"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/architecture/03_alarm_management.md"
    başlık: "HMI Alarm Yönetimi"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/architecture/04_user_auth.md"
    başlık: "HMI Kullanıcı Yetkilendirme ve Erişim Kontrolü"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_hmi_patterns.md"
    ilişki: detaylandırır
  - konu: "02_realtime_data.md"
    ilişki: detaylandırır
  - konu: "03_alarm_management.md"
    ilişki: detaylandırır
  - konu: "04_user_auth.md"
    ilişki: detaylandırır
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/modbus-tcp/01_protocol_basics.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Bu sentez, dört temel belgeyi okuduktan sonra okunmak üzere tasarlanmıştır."
  - "OPC UA veya Modbus TCP temel kavramları önerilir."
ÇELİŞKİLER :
  - kaynak: "ISA-101 gri renk paleti ile operatör alışkanlığı çatışması"
    konu: "Gri/nötr ekranlar ilk başta 'sıkıcı' bulunur; ancak alarm tepki süresi azalır"
    çözüm: "ISA-101 uygulanmalı, geçiş eğitimi ile operatör beklentisi yönetilmeli."
  - kaynak: "Polling her şeyi çözer algısı"
    konu: "100ms × 1000 tag = 10.000 istek/saniye; OPC UA subscription ile %70-90 trafik azalır"
    çözüm: "OPC UA subscription tercih edilmeli; Modbus için toplu okuma ve değişim filtresi uygulanmalı."
  - kaynak: "Alarm bolluğu güvenliği artırır algısı"
    konu: "ISA-18.2: <10 alarm/10 dakika sınırı; fazlası alarm körlüğüne yol açar"
    çözüm: "Her alarm operatör müdahalesi gerektirmeli; müdahale gerektirmeyenler event log'a gönderilmeli."
  - kaynak: "Frontend yetkilendirme yeterli algısı"
    konu: "UI gizleme tek başına güvenlik sağlamaz; API doğrudan çağrılabilir"
    çözüm: "Yetkilendirme her zaman backend middleware'de de uygulanmalı."
---

## Özün Ne

Bu sentez, "Modern bir endüstriyel HMI projesine başlayan biri dört temel belgeyi okuyunca ne anlamalı?" sorusuna yanıt verir. Dört belge birbirinin zorunlu katmanıdır: Mimari desenler tüm sistemin çerçevesini çizer; gerçek zamanlı veri o çerçevenin içine akan kanı sağlar; alarm yönetimi anormal durumu operatöre iletir; kullanıcı yetkilendirme ise kimin ne yapabileceğini ve ne yaptığını belirler. Bu dördü bir arada anlaşıldığında endüstriyel HMI'ın neden kurumsal web uygulamasından temelden farklı olduğu ve her mimari kararın fiziksel sonuçları olduğu netleşir.

Temel ayrım tek cümlede şudur: Bir e-ticaret sitesinde yanlış düğme tıklandığında "Geri Al" vardır; bir motor kontrol HMI'ında yanlış düğme fabrika durmasına veya yaralanmaya yol açabilir. Bu kritiklik, HMI mimarisini baştan sona etkiler.

## Nasıl Çalışır

### Dört Katmanın Birbirine Bağlantısı

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  ENDÜSTRİYEL HMI MİMARİSİ — ZİHİN HARİTASI              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  01_hmi_patterns.md — MİMARİ ÇERÇEVE                                     │
│  ┌────────────────────────────────────────────────────────────┐           │
│  │  ISA-101 Ekran Hiyerarşisi  │  Mimari Seçenekler          │           │
│  │  Seviye 1: Genel bakış      │  A) SCADA Platformu         │           │
│  │  Seviye 2: Alan             │  B) Web Tabanlı HMI         │           │
│  │  Seviye 3: Detay            │  C) CODESYS WebVisu         │           │
│  │  Seviye 4: Destek/Bakım     │                             │           │
│  │  Kural: ≤3 tıklama          │  Bileşen kütüphanesi        │           │
│  └──────────────────────────────────────────────────────────┬─┘           │
│                                                              │             │
│                         Çerçeve içine veri akar             │             │
│                                                              ▼             │
│  02_realtime_data.md — VERİ AKIŞI                                         │
│  ┌────────────────────────────────────────────────────────────┐           │
│  │  OPC UA Subscription (tercih)  │  Modbus Polling (legacy) │           │
│  │  Tag hızı: 100ms → 5s arası    │  Toplu okuma, değişim    │           │
│  │  WebSocket → Frontend push     │  filtresi zorunlu        │           │
│  │  Stale data tespiti ve overlay │  Bağlantı kopma yönetimi │           │
│  └──────────────────────────────────────────────────────────┬─┘           │
│                                                              │             │
│                    Alarm koşulları veri katmanından gelir   │             │
│                                                              ▼             │
│  03_alarm_management.md — ALARM SİSTEMİ                                  │
│  ┌────────────────────────────────────────────────────────────┐           │
│  │  ISA-18.2 öncelik: Kritik/Yüksek/Orta/Düşük              │           │
│  │  Durum döngüsü: Normal→Unack→Ack→RTN→Normal              │           │
│  │  <10 alarm/10 dakika sınırı                               │           │
│  │  Alarm vs Event ayrımı; flood bastırma (suppression)      │           │
│  └──────────────────────────────────────────────────────────┬─┘           │
│                                                              │             │
│               Alarm onaylama ve komutlar yetki kontrolüne   │             │
│               tabidir; kim ne yaptı loglanmalı              │             │
│                                                              ▼             │
│  04_user_auth.md — YETKİLENDİRME                                         │
│  ┌────────────────────────────────────────────────────────────┐           │
│  │  RBAC: Viewer→Operator→Technician→Engineer→Admin          │           │
│  │  JWT + bcrypt + backend middleware                        │           │
│  │  Oturum zaman aşımı, RFID/PIN                             │           │
│  │  Audit log: Her yazma kim/ne/ne zaman/önceki/yeni         │           │
│  └────────────────────────────────────────────────────────────┘           │
└──────────────────────────────────────────────────────────────────────────┘
```

### Mental Model: Bir HMI Mimarisi Nasıl Oluşur?

Dört belgeyi tek bir zihinsel modelde birleştiren soru şudur: "Bir operatör bir motoru durdurmak istediğinde sistemin her katmanı ne yapar?"

```
1. GÖRÜNTÜLEME (Mimari Deseni — Belge 1)
   Operatör ekrana bakar. ISA-101 uyumlu nötr/gri ekranda
   motor simgesi durumunu gösterir. ≤3 tıklamayla detay sayfasına ulaşır.

2. VERİ (Gerçek Zamanlı — Belge 2)
   Motor hızı ve durumu OPC UA subscription ile her 200ms'de
   backend'e gelir, WebSocket ile frontend'e push edilir.
   Bağlantı kopunca değerler gri + uyarı overlay görünür,
   tüm yazma butonları devre dışı kalır.

3. ALARM (Yönetim — Belge 3)
   Motor akımı yüksek limitini aştıysa PLC bir alarm koşulu üretir.
   HMI, ISA-18.2'ye göre Yüksek öncelikle alarm listesine ekler.
   Operatör alarm mesajında "ne yapmalı" bilgisini görür.
   Durdurma kararını alır.

4. YETKİ (Kullanıcı Auth — Belge 4)
   [Durdur] butonuna tıklayınca frontend usePermission('motor.stop')
   kontrolü yapar. Backend API de requirePermission('motor.stop')
   middleware'inden geçer. Komut loglanır: Kim, ne zaman, hangi motor.
   Motor durur. Log immutable olarak saklanır.
```

Bu dört adım aynı anda çalışır ve birbirinin önkoşuludur:
- Veri katmanı olmadan mimari desen boştur.
- Alarm sistemi olmadan veri katmanı yalnızca izleme aracıdır.
- Yetkilendirme olmadan alarm onaylama ve komutlar hesap verilemez hale gelir.

## Hızlı Referans Tabloları

### A. HMI Mimari Yaklaşım Seçimi (Belge 1)

| Yaklaşım | Ne Zaman | Avantaj | Dezavantaj |
|---|---|---|---|
| SCADA Platformu (WinCC, Ignition) | Büyük tesis, hızlı geliştirme | Alarm/historian dahili, tag bağlama hızlı | Yüksek lisans, vendor bağımlılığı |
| Web HMI (React/Vue + WebSocket) | Özel proje, platform bağımsızlık | Sıfır lisans, modern UX, Git uyumlu | Alarm/historian kendin yazarsın |
| CODESYS WebVisu / TargetVisu | CODESYS PLC projesi | PLC ile aynı ortam, doğrudan değişken bağlama | Sınırlı UI, büyük projelerde performans |

### B. ISA-101 Renk ve Tasarım Kuralları (Belge 1)

| Durum | Renk | Kural |
|---|---|---|
| Normal çalışma | Gri / Nötr | Ekran sakin, göz yorulmuyor |
| Uyarı | Sarı / Turuncu | "Dikkat, izle" |
| Alarm (Kritik) | Kırmızı | YALNIZCA alarm için — başka hiçbir şey için kullanma |
| Bilgi / Seçim | Mavi | Seçili durum, bilgilendirme |
| Onay / OK | Yeşil | Yalnızca teyit mesajları için |
| Renk körü uyumu | Renk + Şekil | ▲ kritik, ▲▲ yüksek — yalnızca renge güvenme |

### C. Gerçek Zamanlı Veri Stratejileri (Belge 2)

| Tag Tipi | Güncelleme Sıklığı | Yöntem |
|---|---|---|
| Alarm / güvenlik biti | <100ms | OPC UA Sub — hızlı (100ms publish interval) |
| Motor çalışma durumu | 100–200ms | OPC UA Sub — normal |
| Anlık ölçüm (hız, akım) | 200–500ms | OPC UA Sub — normal |
| Sıcaklık, basınç | 500ms–1s | OPC UA Sub / Polling |
| Sayaç, üretim toplamı | 1–5s | OPC UA Sub — yavaş |
| Enerji tüketimi | 5–60s | Yavaş polling / MQTT |
| Vardiya raporları | Dakika/vardiya | REST API, veritabanı |

### D. ISA-18.2 Alarm Öncelik Standartları (Belge 3)

| Öncelik | Renk | Tepki Süresi | Maksimum Oran | Örnekler |
|---|---|---|---|---|
| 1 — Kritik | Kırmızı + yanıp söner | 5–15 saniye | Toplam alarmların ≤%5 | Acil durdurma, güvenlik limiti, yangın/gaz |
| 2 — Yüksek | Turuncu | 5–10 dakika | Toplam alarmların ≤%15 | Motor arızası, sıcaklık aşımı, basınç yüksek |
| 3 — Orta | Sarı | Saatler | — | Filtre basınç farkı, yağ seviyesi düşük |
| 4 — Düşük | Mavi | Vardiya içinde | — | Bakım bildirimi, kalibrasyon zamanı |

Kilit sayısal sınır: **<10 alarm / 10 dakika** operatör başına (ISA-18.2).

### E. Alarm Durum Makinesi (Belge 3)

| Durum | HMI Gösterimi | Anlam |
|---|---|---|
| ACTIVE_UNACK | Kırmızı, yanıp söner + siren | Koşul aktif, operatör görmedi |
| ACTIVE_ACK | Turuncu, sabit + siren durur | Koşul aktif, operatör onayladı |
| RTN_UNACK | Sarı, sabit | Koşul düzeldi ama onaylanmadı |
| NORMAL | Listeden kaldırılır | Her şey normal |
| SHELVED | Sarı, ikon | Operatör geçici bastırdı |
| SUPPRESSED | Gri, bakım ikonu | Bakım sırasında bastırıldı |

**Kritik ayrım**: Acknowledge ≠ Resolved. Onaylamak "gördüm" demektir; koşul aktif kalmaya devam edebilir.

### F. RBAC Rol İzin Matrisi (Belge 4)

| Eylem | Viewer | Operatör | Teknisyen | Mühendis | Admin |
|---|---|---|---|---|---|
| Ekran görüntüleme | ✓ | ✓ | ✓ | ✓ | ✓ |
| Setpoint yazma | ✗ | ✓ | ✓ | ✓ | ✓ |
| Motor start/stop | ✗ | ✓ | ✓ | ✓ | ✓ |
| Alarm onaylama | ✗ | ✓ | ✓ | ✓ | ✓ |
| Bakım modu | ✗ | ✗ | ✓ | ✓ | ✓ |
| Alarm bastırma (shelve) | ✗ | ✗ | ✓ | ✓ | ✓ |
| Alarm limiti değiştirme | ✗ | ✗ | ✗ | ✓ | ✓ |
| Reçete düzenleme | ✗ | ✗ | ✗ | ✓ | ✓ |
| Kullanıcı yönetimi | ✗ | ✗ | ✗ | ✗ | ✓ |

### G. Bağlantı Kopma Davranış Tablosu (Belge 2)

| Durum | Gösterim | Yazma Butonları | Yeniden Bağlanma |
|---|---|---|---|
| CONNECTED | Normal | Aktif | — |
| DISCONNECTED | Kırmızı banner + değerler gri/italik | Devre dışı | Arka planda otomatik (3s aralık) |
| CONNECTING | Sarı banner | Devre dışı | Devam ediyor |
| DEGRADED | Sarı banner | Kısıtlı | Kısmi bağlantı |

Reconnect sonrası: Her zaman FULL_UPDATE gönder — delta yetmez.

## Pratikte Nasıl Kullanılır

### "İlk HMI Projesi" Kontrol Listesi

Aşağıdaki adımları sırayla tamamlayan biri, temel bir çalışan endüstriyel HMI kurabilir:

**Mimari Kararlar (Belge 1)**

```
□ 1. Proje ölçeğine göre mimari seç:
      Küçük/özel    → Web HMI (React + WebSocket + Backend)
      Büyük/hızlı   → SCADA Platform (Ignition, WinCC)
      CODESYS PLC   → WebVisu başlangıç, büyüyünce Web HMI

□ 2. ISA-101 renk paletini uygula:
      Normal: Gri  |  Uyarı: Sarı  |  Alarm: Kırmızı (YALNIZCA)

□ 3. Ekran hiyerarşisini tasarla (4 seviye, ≤3 tıklama kuralı)

□ 4. Bileşen kütüphanesi oluştur:
      Motor_Status_Widget, Analog_Gauge, Alarm_Banner, Trend_Chart
```

**Veri Katmanı (Belge 2)**

```
□ 5. Tag listesi ve güncelleme hızlarını belirle:
      Alarm bitleri → 100ms OPC UA Sub
      Ölçümler      → 200-500ms OPC UA Sub
      Sayaçlar      → 1-5s OPC UA Sub
      Enerji         → 60s veya MQTT

□ 6. Backend singleton bağlantı oluştur:
      Tek OPC UA Client → paylaşımlı subscription → WebSocket broadcast
      (Her widget kendi bağlantısı açmamalı!)

□ 7. Stale data yönetimi uygula:
      maxAgeMs = 5000 → Gri/italik gösterim

□ 8. Bağlantı kopma overlay ve yeniden bağlanma döngüsü ekle
```

**Alarm Sistemi (Belge 3)**

```
□ 9. Alarm vs Event ayrımını yap:
      Müdahale gerektiriyor → Alarm
      Yalnızca kayıt        → Event log

□ 10. ISA-18.2 öncelik seviyelerini ata (4 seviye)
       Kontrol: Kritik ≤%5, Yüksek ≤%15

□ 11. Alarm state machine uygula:
       ACTIVE_UNACK → ACTIVE_ACK → RTN → NORMAL

□ 12. Alarm log şemasını oluştur:
       id, priority, state, activeTime, ackTime, ackBy, clearTime, causeNote, actionNote

□ 13. Sesli uyarı yönetimi:
       Onaylanmamış kritik → siren | Onaylanınca → siren durur
```

**Yetkilendirme (Belge 4)**

```
□ 14. Rol hiyerarşisini tanımla: VIEWER → OPERATOR → TECHNICIAN → ENGINEER → ADMIN

□ 15. Backend middleware: requirePermission() her API endpoint'inde

□ 16. Frontend: usePermission() ile UI gizleme (devre dışı değil, gizle)

□ 17. Oturum zaman aşımı: 15 dakika inaktivite, 2 dakika önceden uyarı

□ 18. Audit log: Her yazma kim/ne/ne zaman/önceki değer/yeni değer

□ 19. Fabrika zemini için RFID + PIN kombinasyonu değerlendir
```

### Dört Belgeyi Bağlayan Pratik Senaryo

**Görev**: Hat 1 motorunun hız setpointini değiştir ve aşırı sıcaklık alarmını yönet.

```
ADIM 1 — Ekran Navigasyonu (Belge 1 — ISA-101)
  Dashboard → Tıklama 1 → Hat 1 → Tıklama 2 → Motor Detay sayfası
  Ekranda motor simgesi: Açık gri + "ÇALIŞIYOR" metni

ADIM 2 — Veri Görüntüleme (Belge 2 — Gerçek Zamanlı)
  Motor hızı: OPC UA sub (200ms) → Backend → WebSocket → Frontend
  Sıcaklık:   OPC UA sub (500ms) → Backend → WebSocket → Frontend
  Değerler taze, bağlantı yeşil → Normal gösterim

ADIM 3 — Setpoint Değiştirme (Belge 4 — Yetkilendirme)
  Operatör [45.0 m/dk] setpoint kontrolünü görüyor
  (usePermission('setpoint.write') = true → Kontrol görünür)
  Yeni değer girer → [Uygula] tıklar
  Backend: requirePermission('setpoint.write') ✓
  Audit log: { user: "ali", tag: "motor1.speedSP", prev: 45.0, new: 50.0, time: "..." }
  PLC'ye OPC UA Write gönderilir

ADIM 4 — Alarm Tetiklenir (Belge 3 — ISA-18.2)
  Motor sıcaklığı 88°C'yi aşıyor (limit: 85°C)
  PLC alarm koşulunu aktif ediyor
  HMI: ACTIVE_UNACK → Alarm listesine eklenir (🟠 Yüksek öncelik, yanıp söner)
  Alarm banner tüm ekranlarda görünür

ADIM 5 — Alarm Onaylama (Belge 3 + 4)
  Operatör alarm mesajını okur:
    "Motor 1 Sıcaklık Yüksek — Akım aşımı. FR Panel'i kontrol et."
  [Onayla] tıklar → requirePermission('alarm.ack') ✓
  Durum: ACTIVE_UNACK → ACTIVE_ACK
  Siren durur, alarm listesinde turuncu/sabit kalır
  Operatör motor yükünü azaltır (setpoint düşürür)
  Sıcaklık düşünce → RTN → NORMAL → Alarm listesinden kalkar

ADIM 6 — Bağlantı Koparsa (Belge 2)
  OPC UA bağlantısı kesildi:
  → Tüm değerler gri + italik (stale data overlay)
  → "PLC BAĞLANTISI KESİLDİ" kırmızı banner
  → [Uygula] ve tüm yazma butonları devre dışı
  → Arka planda 3s aralıkla yeniden bağlanma deneniyor
  Bağlantı geri gelince: FULL_UPDATE ile tüm değerler yenilenir
```

## Sık Yapılan Hatalar

### Belge 1 — Mimari Deseni Hataları

**1. Her Şeyin Renkli Olması (ISA-101 İhlali)**
Normal durumda yeşil/kırmızı renk bolluğu kullanılınca alarm geldiğinde operatör "hangi kırmızı alarm?" sorusunu sorar. Çözüm: Normal durum nötr/gri, renk yalnızca anomali için.

**2. Üç Tıklama Kuralını İhlal Etmek**
Beş seviyeli menü hiyerarşisi sık kullanılan ekranlara ulaşımı zorlaştırır. Navigasyon hiyerarşisi baştan tasarlanmalı; kritik ekranlar ≤3 tıklama olmalı.

**3. Her Eylem İçin Onay Dialogu**
Onay dialogunu her şeye koymak operatörü yavaşlatır, yorar. Yalnızca geri alınamaz kritik eylemler (motor durdurma, sistem reset) için dialog; setpoint güncellemesi gibi geri alınabilir işlemler için doğrudan uygula.

### Belge 2 — Gerçek Zamanlı Veri Hataları

**4. Her Widget Kendi OPC UA Bağlantısını Açmak**
50 widget × 100ms = 5000 istek/saniye; backend CPU %80+. Çözüm: Tek singleton DataService, paylaşımlı subscription, WebSocket broadcast.

**5. Bağlantı Kopmasını Sessizce Geçiştirmek**
Ekran eski değerleri gösterirken operatör canlı veri sandı. Gerçek hayat vakası: Motor sıcaklığı 20 dakika önce gösterilen 68°C'ydi, gerçekte 92°C'ye ulaşmıştı, motor hasar gördü. Bağlantı kopunca mutlaka görünür overlay + yazma devre dışı.

**6. Reconnect Sonrası Yalnızca Delta Göndermek**
Bağlantı kopuk süresinde değişip geri dönen değerler kaybolur. Reconnect'te her zaman FULL_UPDATE.

### Belge 3 — Alarm Sistemi Hataları

**7. Her Şeyi Alarm Yapmak**
1000+ alarm/gün → Alarm körlüğü → Kritik alarm kaybolur → Fiziksel hasar. Müdahale gerektirmeyen her bildirim Event log'a gitmeli.

**8. Acknowledge = Çözüldü Sanmak**
Alarm onaylandıktan sonra listeden silmek büyük hatadır. Onaylandı = "Gördüm". Koşul aktifse ACTIVE_ACK durumunda listede kalmalı; yalnızca koşul düzelince listeden kalkmalı.

**9. Alarm Sesi Yanlış Bağlamak**
Sirenin yalnızca onaylanmamış alarm için çalması gerekir. Alarm onaylanınca siren durmalı (koşul aktif olsa bile). Çoğu yanlış implementasyonda siren koşul düzelene kadar çalıyor — bu operatörü acil durumu onayla yerine koşulu düzeltmeye değil, sadece "sesi kesmek için" onaylamaya iter.

### Belge 4 — Yetkilendirme Hataları

**10. Paylaşılan Hesap Kullanmak**
"Herkes operator/1234 kullanıyor" → Kim ne yaptı bilinmiyor → Hesap sorulabilirlik sıfır. Her kullanıcı kendi hesabı olmalı; personel değişince hesap silinmeli.

**11. Yalnızca Frontend Yetkilendirme**
UI gizleme yeterli değil; kullanıcı F12 açıp API'yi direkt çağırabilir. Backend middleware her endpoint'te zorunlu.

**12. Audit Log Eksikliği**
"Parametre yanlış — kim değiştirdi?" sorusu log olmadan yanıtsız kalır. Her yazma: kim, ne, ne zaman, önceki değer, yeni değer. Saklama süresi: en az 1 yıl (FDA 21 CFR Part 11: 3 yıl).

## Ne Zaman ...

### Ne Zaman Web HMI Yerine SCADA Platformu Seçilir?

```
SCADA Platform seç:
  → 100+ ekran, hızlı geliştirme gereksinimi
  → Historian (geçmiş veri) ve raporlama kritik
  → Ekip OT geliştirme biliyor, frontend bilmiyor
  → Vendor destek sözleşmesi gerekli (SLA)
  → ISA-18.2 alarm yönetimi dahili kullanılabilir

Web HMI seç:
  → Platform bağımsızlık kritik (SCADA lisansı olmayan makineler)
  → Git ile versiyon kontrolü, CI/CD pipeline isteniyorsa
  → Özel UX gereksinimleri (standart SCADA widget'ları yetmiyorsa)
  → Küçük ekip, hem PLC hem frontend yazılım bilen mühendis
```

### Ne Zaman OPC UA Subscription Yerine Polling Kullanılır?

```
OPC UA Subscription kullan (standart tercih):
  → Değer değişim bazlı bildirim yeterli
  → Çok sayıda tag (100+) izleniyorsa
  → OPC UA server mevcut (CODESYS, modern PLC)

Polling zorunlu:
  → Modbus TCP legacy PLC (subscription alternatifi yok)
  → OPC UA server kurulamayan gömülü cihazlar

Polling kullanıyorsan mutlaka:
  → Toplu okuma (tek FC03 isteği, çok register)
  → Değişim filtresi (sadece değişen değerleri WebSocket'e ilet)
```

### Ne Zaman RFID + PIN Kombinasyonu Kullanılır?

```
RFID + PIN seç:
  → Fabrika zemini, operatörler eldiven giyiyor
  → Giriş hızı kritik (vardiya değişiminde 10+ kişi)
  → Kart kaybolunca admin anında devre dışı bırakabilmeli

Standart kullanıcı adı + şifre yeterli:
  → Ofis / mühendis istasyonu (klavye rahat kullanılıyor)
  → Az kullanıcı, sık giriş gerekmiyorsa
```

### Ne Zaman Bu Dört Belge Yetmez?

```
Yetersiz Kaldığı Durum                  Bakılacak Sonraki Konu
──────────────────────────────────────────────────────────────────────
Historian (geçmiş veri saklama)         → knowledge/hmi/historian/
Mobile HMI (tablet, saha cihazı)        → knowledge/hmi/mobile/
Fonksiyonel güvenlik (SIL) + HMI       → knowledge/standards/safety_plc/
OPC UA sunucu yapılandırması (CODESYS) → knowledge/codesys/visualization/
ISA S88 Batch reçete yönetimi           → knowledge/standards/isa-s88/
IEC 62443 OT siber güvenlik            → knowledge/security/iec-62443/
EtherCAT motion control görselleştirme → knowledge/networking/ethercat/
```

## Gerçek Proje Notları

**Sentez Notu 1 — Dört Katmanın Hiyerarşisi Neden Önemli?**
Deneyimde en sık karşılaşılan hata şudur: Yetkilendirme sonraya bırakılır ("önce çalışsın, sonra güvenlik ekleriz"). Ancak audit log olmadan eklenmesi demek, geçmiş tüm yazma işlemlerinin anonim kalması demektir. Yetkilendirme ve audit log projenin ilk günden mimariye dahil edilmelidir — sonradan eklemek hem daha zordur hem ilk verileri kaybettirir.

**Sentez Notu 2 — ISA-101 ile ISA-18.2'nin Kesişimi**
İki standart birbirini tamamlar: ISA-101 alarm rengini belirler (kırmızı = yalnızca alarm), ISA-18.2 alarm sayısını belirler (<10/10 dakika). Bu iki kural birlikte uygulandığında operatör alarm bastığında hem ekranda hemen fark eder (ISA-101) hem de alarm kalabalığına boğulmaz (ISA-18.2). Birini uygulamak, diğerini atlamak sistemin yalnızca yarısını optimize etmek demektir.

**Sentez Notu 3 — Bağlantı Kopma: En Çok Gözden Kaçan Konu**
Yeni başlayan ekipler bağlantı kopma senaryosunu geliştirme sırasında test etmez. "Normal şartlarda çalışıyor" denir. Prodüksiyonda ilk ağ kesintisinde operatör eski veriyle karar alır. Gerçek hayat vakası: 20 dakika önce bağlantı kesilmiş, ekran 68°C gösteriyordu, gerçekte 92°C'ye ulaşmıştı, motor aşırı ısındı. Bu nedenle: Bağlantı kopma senaryosu geliştirme aşamasında mutlaka test edilmeli; overlay, stale data işareti, yazma kilidi ilk günden tasarlanmalı.

**Sentez Notu 4 — Alarm Tasarımı Bir Kez Yapılmaz**
ISA-18.2'nin "worst actor" analizi sürekli yapılması gereken bir pratiktir. Bir tesiste başlangıçta 1200 alarm vardı; 3 ay sonra analiz yapıldı, en sık tetiklenen 20 alarm tespit edildi, bunların 14'ü gereksizdi veya limitleri yanlış ayarlanmıştı. Sonuç: 1200 → 580 alarm. Alarm tasarımı prodüksiyona giriş sonrası da izlenmeli; "bu ay en çok hangi alarm tetiklendi, neden?" sorusu düzenli sorulmalı.

**Sentez Notu 5 — Güvenlik Politikası İnsan Davranışını Hesaba Katmalı**
Çok karmaşık şifre politikası → Operatör hatırlamıyor → Post-it monitöre yapıştırıyor → Daha tehlikeli. Endüstriyel HMI için en iyi yaklaşım: RFID kart + 4 haneli PIN (fabrika zemini), makul şifre karmaşıklığı, 15 dakika inaktivite zaman aşımı. Güvenlik politikası, onu kullanan insanın gerçek koşullarına uyarlanmalıdır.

**Sentez Notu 6 — Bu Bilgi Tabanının Önerilen Okuma Sırası**
1. Sentezi oku (bu belge) → Genel harita anlaşıldı
2. `01_hmi_patterns.md` → ISA-101 ve mimari seçenekler kavrandı
3. `02_realtime_data.md` → OPC UA subscription ve bağlantı yönetimi öğrenildi
4. `03_alarm_management.md` → ISA-18.2 alarm durum makinesi anlaşıldı
5. `04_user_auth.md` → RBAC ve audit log kuruldu
6. Senaryoyu uygula (bu belgede) → Motor setpoint + alarm + auth akışı çalıştırıldı

## İlgili Konular

```
knowledge/hmi/architecture/      ← Şu an buradasınız
├── 01_hmi_patterns.md           → ISA-101 mimari çerçeve, ekran hiyerarşisi
├── 02_realtime_data.md          → OPC UA sub, Modbus polling, stale data
├── 03_alarm_management.md       → ISA-18.2, alarm state machine, flood önleme
├── 04_user_auth.md              → RBAC, JWT, audit log, oturum yönetimi
└── _synthesis.md (bu belge)

Protokol katmanı:
knowledge/protocols/
├── opc-ua/
│   ├── 01_architecture.md       → OPC UA sunucu mimarisi
│   └── 04_subscriptions.md      → Subscription detayları
└── modbus-tcp/
    └── 01_protocol_basics.md    → Modbus TCP polling temelleri

Standartlar:
  ISA-101.01-2015    → HMI tasarım standardı (ekran, renk, navigasyon)
  ISA-18.2-2016      → Alarm yönetimi yaşam döngüsü
  IEC 62443          → OT siber güvenlik standartlar ailesi
  FDA 21 CFR Part 11 → İlaç sektörü elektronik kayıt ve imza

Araçlar:
  Ignition (Inductive Automation)  → Yaygın SCADA/HMI platformu
  Node-RED Dashboard               → Hızlı web HMI prototipleme
  InfluxDB + Grafana               → Monitoring/analytics dashboard (salt okuma)
  node-opcua / asyncua             → OPC UA istemci kütüphaneleri
  pymodbus                         → Python Modbus TCP istemcisi
  JSON Web Token (JWT) + bcrypt    → Web HMI kimlik doğrulama
```
