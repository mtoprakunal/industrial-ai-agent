---
KONU        : CODESYS Task Yapısı — Uzman Sentezi
KATEGORİ    : codesys
ALT_KATEGORI: task-structure
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/codesys/task-structure/01_task_types.md"
    başlık: "Task Tipleri (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/task-structure/02_cycle_time.md"
    başlık: "Cycle Time Seçimi (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/task-structure/03_priority_management.md"
    başlık: "Öncelik Yönetimi (Uzman)"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_task_types.md"
    ilişki: detaylandırır
  - konu: "02_cycle_time.md"
    ilişki: detaylandırır
  - konu: "03_priority_management.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/fundamentals/_synthesis.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Üç task-structure belgesinin Uzman bölümleri okunmuş olmalıdır."
  - "fundamentals/_synthesis.md (determinizm felsefesi) kavranmış olmalıdır."
  - "Saha devreye alma ve RT tuning deneyimi varsayılır."
ÇELİŞKİLER :
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez belgesi yeni çelişki içermez; kaynak belgelere atıflar yapar."
---

## Özün Ne

Temel soru değişmedi: **"Yeni bir proje geldiğinde task yapısını nasıl tasarlarım?"** Ama uzman cevabı daha derindir. Task yapısı üç bağımsız ayar (tip, cycle time, öncelik) değil, **tek bir gerçek-zamanlılık bütçesinin** üç boyutudur. Bu bütçe `fundamentals/_synthesis.md`'deki determinizm felsefesinin doğrudan uygulanışıdır: her task öngörülebilir olmalı (tip → Cyclic), öngörülebilir kalmalı (cycle time → jitter < %10), ve öngörülebilirlik çakışmamalı (öncelik → preemption + race-free paylaşım). Uzmanlık, bir saha belirtisini (jitter, watchdog, salınım, sync kaybı) doğru boyuta haritalayıp kök nedene inebilmektir. Çünkü bu üç boyut birbirine kilitlidir: yanlış tip → cycle time'ı anlamsızlaştırır → öncelik de kurtaramaz.

## Nasıl Çalışır

### Üç Belgenin Birbirine Bağlantısı

```
Tasarım Sorusu                     →  Boyut         Hatası Diğerlerini Bozar
──────────────────────────────────────────────────────────────────────────
"Hangi tip task?" (tetikleme)       → 01 Tip        Yanlış tip → zamanlama çöker
"Ne sıklıkla?" (periyot + jitter)   → 02 Cycle      Yanlış cycle → tepki/kararlılık çöker
"Hangisi önce?" (preemption+paylaşım)→ 03 Priority  Yanlış öncelik → starvation/race

Üç boyut tek bütçe:
  PID'i Freewheeling'e koy (01) → Δt değişken (02) → öncelik ne olsa PID bozuk (03)
  Cycle çok kısa (02) → CPU dolu → düşük öncelikli aç kalır (03)
  Aynı veriyi iki task yazar (03) → preemption ortasında yarım değer (01+02)
```

### Tasarım Felsefesi: Determinizm Bütçesinin Üç Boyutu

| Boyut | Soru | Determinizm Katkısı | Kök İhlal |
|---|---|---|---|
| **Tip** (01) | Ne tetikler? | Cyclic = öngörülebilir tetik | Event/Freewheeling = asenkron/değişken |
| **Cycle Time** (02) | Ne sıklıkta + ne kadar kararlı? | Sabit Δt + düşük jitter | Jitter ≈ cycle → kaos |
| **Öncelik** (03) | Çakışınca kim? | Preemption + race-free | Starvation, race, inversion |

**Uzman içgörüsü:** "Kod doğru ama makine tuhaf davranıyor" → neredeyse her zaman bu üç boyuttan biri ihlal edilmiştir, kodun kendisi değil. Pusula: belirtiyi boyuta haritala.

### Tasarım Süreci: 5 Adım

```
Adım 1 — Bileşenleri listele (güvenlik, motion, PID, I/O, komm, HMI, veri)
Adım 2 — Her bileşene tepki gereksinimi + fieldbus periyodu ata
Adım 3 — Benzer zamanlamaları grupla (cycle time'a göre task'lar)
Adım 4 — Her task'a tip + öncelik ata (boşluklu: 0,3,6,10,15)
Adım 5 — CPU yük kontrolü: Σ(exec/cycle) < %70 (ortalama) + spike payı
```

### Hızlı Referans (Konsolide)

**A. Task Tipi Seçimi (Belge 1)**

| Tip | Tetik | Kullan | Kullanma |
|---|---|---|---|
| Cyclic | Sabit zaman | Kontrol, PID, motion, fieldbus, güvenlik | — |
| Freewheeling | Bittiğinde + bekleme | Log, diagnostik (en düşük öncelik!) | PID, fieldbus, kritik |
| Event | Bit kenarı (yazılım polling) | Nadir komut (reçete) | Hızlı/kısa puls (coalescing) |
| Status | Bit seviyesi | Nadiren doğru seçim | Uzun-TRUE koşullar (CPU yer) |
| External Event | Donanım IRQ | µs encoder, "kısa kap-çık" | Ağır işlem |

**B. Cycle Time Aralıkları (Belge 2)**

| Aralık | Kullanım | Not |
|---|---|---|
| ≤1ms | EtherCAT sync, güvenlik | RT-preempt + izole CPU şart |
| 2-5ms | Motion, hızlı PID | RT kernel gerekebilir |
| 10-20ms | Genel makine mantığı | Projelerin %80'i |
| 50-200ms | HMI, yavaş proses | Kesinlikle yeterli |
| Freewheeling | Arka plan | Kontrol asla |

**C. Öncelik Bandı (Belge 3)**

| IEC Prio | Linux | Kullanım |
|---|---|---|
| 0 | RT 79 | Yalnızca e-stop/güvenlik |
| 1-3 | RT 76-78 | Motion, fieldbus sync |
| 4-6 | RT 73-75 | Ana kontrol, PID |
| 7-12 | RT 67-72 | İzleme, log altyapısı |
| ≥13 | SCHED_OTHER | RT garantisi YOK |

**D. Kritik Eşikler**

| Konu | Değer | Kaynak |
|---|---|---|
| CPU yük tavanı | < %70 (ortalama + spike payı) | 02, 03 |
| Jitter sınırı | < cycle × %10 | 02 |
| Event tetik limiti | ~6/ms üstü → HALT | 01 |
| Fieldbus task önceliği | ağ IRQ'dan yüksek (Prio ≤5) | 03 |
| RT garanti sınırı | IEC Prio ≤12 | 03 |
| Atomik atama | ≤ word boyutu (platforma bağlı) | 03 |
| Watchdog Time | ~2-5× Max Exec, Sensitivity 2-3 | 02 |

### Uzman Edge Case Konsolidasyonu

```
BOYUT     EDGE CASE                       BELİRTİ                  KORUMA
──────────────────────────────────────────────────────────────────────────────
Tip       Event coalescing (hızlı puls)   Tetik kaybolur           Latch + Cyclic
Tip       Aşırı Event tetik               Runtime HALT             R_TRIG + Cyclic
Tip       External Event'te ağır kod      Kesme birikir, kilit     Kısa kap-çık
Tip       Aynı FB iki task'ta             Tanımsız .ET             Tek task / instance
Cycle     Jitter ≈ cycle (RT yok)         Determinizm yok          RT-preempt + izole
Cycle     Termal throttling               Gündüz Max Cycle artar   En kötü termalde test
Cycle     I/O image gizli maliyeti        "Optimize ettim, hızlanmadı" Az kanal/uzun cycle
Cycle     Büyüyen array O(n)              Exec yavaşça şişer       Trend izle, indeksli erişim
Öncelik   LREAL 32-bit'te bölünür         Frankenstein değer       Double-buffer/mutex
Öncelik   Multicore paralel race          Klasik race patlar       Atomik/mutex (öncelik korumaz)
Öncelik   RT throttling (%95 sınırı)      Prio:0 yine de gecikir   İzole çekirdek
Öncelik   Harici lock'ta inversion        Süresiz bloke            Yüksek task'tan OS çağrısı yok
Öncelik   Starvation → omitted watchdog   Sağlıklı sistem durur    Geniş watchdog / yük düşür
```

## Pratikte Nasıl Kullanılır

### Hazır Şablonlar (Başlangıç Mimarileri)

**Şablon A — Basit Makine**
```
Task_Safety   Cyclic  5ms  Prio:0   E-stop, güvenlik kontakları
Task_Control  Cyclic 10ms  Prio:2   Ana mantık, sensör, aktüatör
Task_Slow     Cyclic 100ms Prio:5   HMI, OPC UA
Task_Log      Freewheel   Prio:15   Diagnostik, log
```

**Şablon B — Motion (EtherCAT)**
```
Task_Safety   Cyclic  2ms  Prio:0   E-stop (EtherCAT döngüsüyle eşleşik)
Task_Motion   Cyclic  2ms  Prio:1   EtherCAT bus cycle task, SoftMotion
Task_Control  Cyclic 10ms  Prio:2   Koordinasyon, PID, recipe
Task_HMI      Cyclic 50ms  Prio:5   HMI, OPC UA
Task_Log      Freewheel   Prio:15   Log
```

**Şablon C — Proses (PID Yoğun)**
```
Task_Safety   Cyclic  5ms  Prio:0
Task_FastPID  Cyclic 10ms  Prio:1   Basınç, akış
Task_SlowPID  Cyclic100ms  Prio:2   Sıcaklık, seviye
Task_Sequence Cyclic 20ms  Prio:3   Sekans, recipe
Task_HMI      Cyclic 200ms Prio:5
Task_Log      Freewheel   Prio:15
```

### Production-Grade Devreye Alma Kontrol Listesi (Uzman)

```
TASARIM
□ Güvenlik task'ı Prio:0 ve en hızlı cycle'da
□ PID/ramp içeren her şey Cyclic (Freewheeling değil)
□ Fieldbus task cycle = fieldbus periyodu (DC ise bus cycle task olarak atanmış)
□ Öncelikler boşluklu (0,3,6,10,15) — ileride ara ekleme için
□ Bloke eden I/O (dosya/ağ) Freewheeling + en düşük öncelik
□ Event task tetik sinyali scheduler interval'inden yavaş değişiyor

PAYLAŞIM (RACE GÜVENLİĞİ)
□ Her paylaşılan değişkenin tek yazarı var
□ Çok-word veri (LREAL/STRUCT/STRING) için double-buffer veya mutex
□ Multicore'da paralel task'lar arası atomik/mutex (öncelik korumaz)
□ Yüksek öncelikli task'tan OS/dosya/ağ çağrısı YOK (inversion riski)
□ Mutex altındaki kritik bölge minimum (sadece pointer/index swap)

RT ALTYAPI (fundamentals/01 ile)
□ RT-preempt kernel + isolcpus + IRQ affinity
□ Kritik motion task'ı izole çekirdekte (Core ataması)
□ Ağ IRQ önceliği < fieldbus task önceliği
□ RT throttling izole çekirdekte yönetildi

DOĞRULAMA
□ Task Monitor açık: Max Cycle < Interval × %70
□ Jitter < cycle × %10
□ 48 saat yük testi (stress-ng + en kötü termal koşul)
□ Online Change spike'ı watchdog sensitivity ile tolere ediliyor
□ Exec time TRENDİ izleniyor (haftalar içinde şişme var mı)
```

### Belirti → Boyut → Kök Neden (Genişletilmiş Teşhis)

```
Belirti                          Boyut      Kök Neden / Çözüm
─────────────────────────────────────────────────────────────────────
Watchdog alarmı                  02         Exec > Cycle → kodu böl/cycle artır
PID salınım yapıyor              01+02      Freewheeling → Cyclic; sabit Δt
HMI çok yavaş                    03         Starvation → üst task exec düşür
Drive titriyor / sync kaçıyor    02+03      Fieldbus cycle/öncelik; IRQ önceliği
Sayaç bazen sıfırlanıyor         03         Race → tek yazar / double-buffer
Frankenstein REAL değeri         03         LREAL 32-bit bölünme → mutex/buffer
Event task çalışmıyor            01         Coalescing → latch+Cyclic
E-stop geç/tutarsız tepki        02+03      Safety cycle çok uzun / öncelik düşük
CPU %90+                         02         Cycle çok kısa → gerçek gereksinime çek
Prio:0 task yine de gecikiyor    03         RT throttling → izole çekirdek
Gündüz yavaşlama                 02         Termal throttling → soğutma/test
Exec haftalar içinde şişiyor     02         Büyüyen veri yapısı → algoritma
Multicore'da beklenmedik race    03         Paralel çalışma → atomik/mutex
```

## Örnekler

### Örnek — Uçtan Uca: Şişe Dolum Makinesi (Race-Safe)

```
Bileşenler: konveyör (Modbus RTU), 4 solenoid, 4 ölçer (analog),
            panel, recipe (3 boyut), USB log

Task mimarisi:
  Task_Safety  Cyclic  5ms  Prio:0   E-stop, kapı kilidi
  Task_Control Cyclic 10ms  Prio:2   Konveyör, solenoid, ölçer, buton
  Task_HMI     Cyclic 50ms  Prio:5   Panel ışıkları
  Task_Recipe  Event        Prio:3   Reçete yükleme (yavaş tetik → güvenli)
  Task_Log     Freewheel   Prio:15   USB log (bloke riski izole)

Race güvenliği:
  - Üretim sayacı (DWORD): yalnızca Task_Control yazar, Task_HMI okur → atomik OK
  - PID çıkışı (REAL): Task_Control yazar tek satır → atomik OK
  - Recipe struct (çok-word): Task_Recipe yazar, Task_Control okur
    → double-buffer + index swap (preemption ortasında yarım okuma yok)

CPU Yük (orta ARM): %2 + %15 + %4 + Freewheel ≈ %21 ✓
  + spike payı: periyotların buluştuğu anda bile < %70 ✓
```

## Sık Yapılan Hatalar

### Başlangıç Hataları (5)

1. **Tek task her şeyi yapar** — büyüyünce watchdog/starvation.
2. **PID'i Freewheeling'e koymak** — değişken Δt, salınım.
3. **Fieldbus cycle yanlış** — sync kaçar, drive titrer.
4. **Event'i hızlı sinyale bağlamak** — HALT; R_TRIG+Cyclic kullan.
5. **CPU yük hesabı yapmamak** — %85'te ani yük watchdog tetikler.

### Uzman Hataları (5) — Sahada Pahalıya Patlayan

1. **Multicore'da "öncelik race'i korur" varsaymak** — paralel çalışma, atomik/mutex şart.
2. **Çok-word veride atomiklik varsaymak** — LREAL/STRUCT bölünür, double-buffer.
3. **Yüksek öncelikli task'tan OS/dosya çağrısı** — sınırsız priority inversion.
4. **Jitter'ı RT altyapısı olmadan kovalamak** — sub-ms cycle, RT-preempt+izolasyon olmadan anlamsız.
5. **Termal/trend körlüğü** — oda sıcaklığı + anlık ölçüme güvenmek; en kötü koşul + trend izle.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Bu Sentezin Kapsamı ve Sınırı

Bu 3 belge + sentez şunlar için yeterlidir: standart makine otomasyonu, motion (EtherCAT+SoftMotion), çoklu PID proses kontrol.

```
Yetersiz Kaldığı Durum              Bakılacak Sonraki Konu
─────────────────────────────────────────────────────────
SIL güvenlik gereksinimleri         → CODESYS Safety (ayrı ürün)
100+ task / büyük dağıtık sistem     → multicore + task affinity derinliği
Sub-µs zamanlama                     → FPGA/ASIC (CODESYS sınırı)
EtherCAT DC faz kilitleme detayı     → knowledge/networking/ethercat/
Profiling / trace ile exec analizi   → knowledge/codesys/advanced/profiling/
Lock-free / atomik desen derinliği   → knowledge/codesys/advanced/shared_memory_patterns/
```

## Gerçek Proje Notları

**Sentez Notu 1 — Üç Boyut Tek Bütçedir**  
Uzmanlığın eşiği: tip, cycle time ve önceliği ayrı ayrı "doğru" yapmak yetmez; üçünün **etkileşimini** görmek gerekir. Doğru tip + doğru cycle + yanlış öncelik = starvation. Doğru öncelik + yanlış tip = bozuk PID. Üçü birlikte tek bir determinizm bütçesini oluşturur; biri ihlal edilirse diğer ikisi telafi edemez.

**Sentez Notu 2 — Belirtiyi Boyuta Haritala, Kodu Okuma**  
Saha sorunlarının çoğu IEC kodunda değil, task yapısındadır. "Drive titriyor" → kodu saatlerce okumak yerine "bu cycle time mı, öncelik mi, sync mi?" diye sor. Belirti→boyut tablosu (yukarıda), uzman teşhisin pusulasıdır.

**Sentez Notu 3 — Preemption Hem Güç Hem Sorumluluk**  
V3'ün preemptive modeli "kritik her zaman önce" garantisini verir (güç), ama race condition yüzeyini açar (sorumluluk). V2'den taşınan kodda gizli race'ler patlar. Her preemptive sistemde paylaşılan veri, atomiklik ve double-buffer disiplini, öncelik tasarımının ayrılmaz parçasıdır — öncelik tek başına veriyi korumaz.

**Sentez Notu 4 — RT Garantisi Uçtan Uca Bir Zincirdir**  
Mükemmel task tasarımı, alttaki kernel RT-preempt değilse, ağ IRQ önceliği yanlışsa, BIOS C-state açıksa veya CPU termal throttle ediyorsa boşa gider. Öncelik (03) ↔ cycle time/jitter (02) ↔ runtime/OS (fundamentals/01) tek bir RT zinciridir; en zayıf halka determinizmi belirler.

**Sentez Notu 5 — Tasarım Başında 10 Dakika, Sahada 2 Gün**  
Task mimarisini kâğıtta tasarlamak 10 dakika; devreye almada değiştirmek (POU taşı, watchdog ayarla, öncelik sırala, race düzelt) 2 gün ve müşteri tesisinde gece mesaisidir. "Önce çalıştır sonra düzelt" task mimarisinde işe yaramaz — çünkü çalışan bir sistem, gizli race veya marjinal yük ile aylarca "çalışıyor" görünür, sonra en kötü anda durur.

## İlgili Konular

```
knowledge/codesys/task-structure/    ← Şu an buradasınız (Uzman seviye)
├── 01_task_types.md           (Uzman)
├── 02_cycle_time.md           (Uzman)
├── 03_priority_management.md  (Uzman)
└── _synthesis.md (bu belge)

Önceki temel:
knowledge/codesys/fundamentals/
└── _synthesis.md → Runtime/proje/diller (determinizm felsefesi)

Sonraki adım — Gelişmiş:
knowledge/codesys/advanced/
├── multicore_tasks.md        → Çok çekirdek, task affinity
└── shared_memory_patterns.md → Lock-free, atomik, double-buffer

knowledge/networking/ethercat/ → EtherCAT DC sync ve task eşleşmesi
knowledge/codesys/debugging/   → Profiling, jitter/exec analizi
```
