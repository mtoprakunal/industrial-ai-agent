---
KONU        : CODESYS Task Yapısı — Sentez
KATEGORİ    : codesys
ALT_KATEGORI: task-structure
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "knowledge/codesys/task-structure/01_task_types.md"
    başlık: "Task Tipleri"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/task-structure/02_cycle_time.md"
    başlık: "Cycle Time Seçimi"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/task-structure/03_priority_management.md"
    başlık: "Öncelik Yönetimi"
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
  - "Bu sentez, üç task-structure belgesini okuduktan sonra okunmak üzere tasarlanmıştır."
ÇELİŞKİLER :
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez belgesi yeni çelişki içermez; kaynak belgelere atıflar yapar."
---

## Özün Ne

Bu sentez tek soruyu yanıtlar: **"Yeni bir proje geldiğinde task yapısını nasıl tasarlarım?"** Üç belge ayrı ayrı okunduğunda task tipleri, cycle time ve öncelik yönetimi kavranır. Bu sentez ise o üç boyutu birleştirerek gerçek bir proje önüne geldiğinizde hangi soruları soracağınızı ve hangi sırayla karar vereceğinizi gösterir. Sonuç: Her projede tekrar başvurulabilecek bir tasarım şablonu.

## Nasıl Çalışır

### Üç Belgenin Birbirine Bağlantısı

```
Proje Tasarım Sorusu          →  İlgili Belge
────────────────────────────────────────────────────────────────
"Kaç farklı task tipi kullanacağım?" → 01_task_types.md
"Her task ne sıklıkla çalışacak?"    → 02_cycle_time.md
"Hangisi diğerinden önce gelecek?"   → 03_priority_management.md

Bu üç karar birbirinden bağımsız değildir:
  Yanlış tip → yanlış zamanlama → öncelik de anlamsız hale gelir.
  Örnek: PID'i Freewheeling'e koymak (01) → zaman sabiti değişken (02)
         → öncelik ne olursa olsun PID doğru çalışmaz (03).
```

### Tasarım Süreci: 5 Adım

**Adım 1 — Uygulamanın Bileşenlerini Listele**

```
"Bu projede ne var?" sorusunu sor.

Tipik bileşenler:
□ Güvenlik: E-stop, kapı kilitleri, parmak koruyucu
□ Motion: Servo, frekans invertörü, step motor
□ Proses Kontrolü: PID, sıra kontrol, recipe
□ I/O: Sensörler, aktüatörler, dijital giriş/çıkış
□ İletişim: OPC UA, Modbus, Ethernet
□ HMI: Ekran güncelleme, operatör girişleri
□ Veri: Log, diagnostik, üretim sayacı
```

**Adım 2 — Her Bileşen için Zamanlama Gereksinimini Belirle**

```
Bileşen              Tepki Gereksinimi  Fieldbus?
────────────────────────────────────────────────
E-stop               < 10ms             —
EtherCAT Servo       2ms (sync)         EtherCAT 2ms
PID Sıcaklık         100ms yeterli      —
Konveyör Mantığı     20ms yeterli       —
HMI Güncelleme       200ms yeterli      —
OPC UA Write         500ms yeterli      —
USB Log              5s yeterli         —
```

**Adım 3 — Task'ları Grupla (Cycle Time'a Göre)**

```
Benzer zamanlama gereksinimi → Aynı task
Farklı zamanlama → Farklı task

Gruplama:
  2ms grubu:   EtherCAT sync, güvenlik → Task_Fast
  10-20ms:     PID, konveyör mantığı  → Task_Control
  100-200ms:   HMI güncelleme         → Task_HMI
  Arkaplan:    Log, diagnostik        → Task_Background
  Olay tabanlı: Reçete yükleme        → Task_Recipe
```

**Adım 4 — Her Task'a Tip ve Öncelik Ata**

```
Task_Fast        → Cyclic 2ms,   Prio:0  (en kritik)
Task_Control     → Cyclic 10ms,  Prio:2
Task_HMI         → Cyclic 100ms, Prio:5
Task_Background  → Freewheeling, Prio:15
Task_Recipe      → Event,        Prio:3  (nadir tetiklenir)
```

**Adım 5 — CPU Yük Kontrolü**

```
Task_Fast       : Exec ~0.5ms / 2ms    = %25
Task_Control    : Exec ~2ms  / 10ms    = %20
Task_HMI        : Exec ~8ms  / 100ms   = %8
Task_Background : Freewheeling         = Kalan CPU
                               TOPLAM  ≈ %53 ✓
```

Toplam %70 altında → güvenli. Üstündeyse cycle time artırılır veya yük dağıtılır.

## Pratikte Nasıl Kullanılır

### Hazır Şablon: Proje Türüne Göre Başlangıç Mimarileri

---

**Şablon A — Basit Makine (Konveyör, Dolum, Basit Paketleme)**

```
Task_Safety   Cyclic  5ms  Prio:0   E-stop, güvenlik kontakları
Task_Control  Cyclic 10ms  Prio:2   Ana mantık, sensörler, aktüatörler
Task_Slow     Cyclic 100ms Prio:5   HMI, OPC UA
Task_Log      Freewheel   Prio:15   Diagnostik, log
```

4 task, yönetimi kolay, çoğu basit makine için fazlasıyla yeterli.

---

**Şablon B — Motion Dahil Makine (Servo, EtherCAT)**

```
Task_Safety   Cyclic  2ms  Prio:0   E-stop, güvenlik (EtherCAT sync döngüsüyle eşleşik)
Task_Motion   Cyclic  2ms  Prio:1   EtherCAT sync, SoftMotion
Task_Control  Cyclic 10ms  Prio:2   Koordinasyon, PID, recipe
Task_HMI      Cyclic 50ms  Prio:5   HMI, OPC UA
Task_Log      Freewheel   Prio:15   Log, diagnostik
```

5 task, motion kontrollü sistemler için standart.

---

**Şablon C — Proses Kontrol (PID Yoğun, Çoklu Döngü)**

```
Task_Safety   Cyclic  5ms  Prio:0   Güvenlik
Task_FastPID  Cyclic 10ms  Prio:1   Hızlı döngü PID'ler (basınç, akış)
Task_SlowPID  Cyclic100ms  Prio:2   Yavaş döngü PID'ler (sıcaklık, seviye)
Task_Sequence Cyclic 20ms  Prio:3   Sekans kontrolü, recipe
Task_HMI      Cyclic 200ms Prio:5   HMI
Task_Log      Freewheel   Prio:15   Log
```

6 task, proses kontrol tesisleri için uygun.

---

### Hangi Mantık Hangi Task'a Girer — Hızlı Referans

```
Mantık Türü                    Task Tipi       Neden
─────────────────────────────────────────────────────────────────
E-stop, güvenlik izleme       Cyclic (1-5ms)   En hızlı tepki şart
EtherCAT/PROFINET sync        Cyclic (fieldbus döngüsü) Sync kırılmaz
PID kontrolü                  Cyclic (10-100ms) Sabit Δt zorunlu
Konveyör, vana, piston        Cyclic (10-20ms)  Deterministik yeterli
Alarm yönetimi                Cyclic (5-20ms)   Hızlı algılama
Operatör komutları            Cyclic (10-20ms)  Gecikmesiz işlem
HMI değişken güncelleme       Cyclic (50-200ms) Görsel yeterli
OPC UA / Modbus yazma         Cyclic (50-500ms) Ağ gecikmesi hâkim
Reçete yükleme (tek seferlik) Event (kenar)    Nadir, anlık
USB / dosya yazma             Freewheeling      Bloke riski, arkaplan
Diagnostik, log               Freewheeling      Kritik değil
Büyük veri işleme             Freewheeling      Diğerlerini engellemesin
```

## Örnekler

### Örnek 1: Uçtan Uca Tasarım — Şişe Dolum Makinesi

```
Proje: 4 nozullu şişe dolum makinesi
Bileşenler:
  - Konveyör (frekans inverter, Modbus RTU)
  - 4 solenoid vana (dijital çıkış)
  - 4 kütüphane ölçer (analog giriş, 0-10V)
  - Operatör paneli (10 buton, 5 pilot lamba)
  - Recipe: 3 farklı şişe boyutu
  - Üretim log (USB'ye günlük)

Zamanlama analizi:
  Konveyör    : 20ms yeterli (mekanik inersia)
  Solenoid    : 10ms tepki (açma/kapama hassasiyeti)
  Ölçer okuma : 50ms yeterli (analog filtre zaten var)
  Panel buton : 20ms yeterli
  Recipe      : Anlık olay, nadiren
  Log         : 5s yeterli

Karar:
  Task_Safety  Cyclic  5ms  Prio:0  E-stop, kapı kilidi
  Task_Control Cyclic 10ms  Prio:2  Konveyör, solenoid, ölçer, buton
  Task_HMI     Cyclic 50ms  Prio:5  Panel ışıkları güncelleme
  Task_Recipe  Event        Prio:3  Reçete yükleme
  Task_Log     Freewheel   Prio:15  USB log

CPU Yük (tahmini, orta sınıf ARM):
  Task_Safety  : 0.1ms/5ms   = %2
  Task_Control : 1.5ms/10ms  = %15
  Task_HMI     : 2ms/50ms    = %4
  Task_Log     : Kalan CPU   = kalan
  TOPLAM       ≈ %21 → Rahat ✓
```

### Örnek 2: Task Tasarım Kontrol Listesi

```
Her yeni proje için:
□ 1. Güvenlik task'ı var mı ve en yüksek öncelikte mi?
□ 2. PID ve ramp hesabı yapan task Cyclic mi?
□ 3. Fieldbus task cycle time, fieldbus döngüsüyle eşleşiyor mu?
□ 4. Dosya/ağ işlemleri Freewheeling task'ta mı?
□ 5. Event task'lar yüksek frekanslı sinyal için kullanılıyor mu?
   → Kullanılıyorsa R_TRIG'e taşı
□ 6. Toplam CPU yükü %70 altında mı?
□ 7. Öncelikler arasında boşluk var mı? (0, 3, 6, 10, 15)
□ 8. Paylaşılan global değişkenler için write sahibi tek task mı?
□ 9. Her task'ın watchdog'u etkin mi?
□ 10. 48 saatlik yük testi planlandı mı?
```

### Örnek 3: Hızlı Sorun Tespiti — Belirti → Neden → Çözüm

```
Belirti                          Olası Neden              İlgili Belge
─────────────────────────────────────────────────────────────────────
Watchdog alarmı                  Exec > Cycle Time         02_cycle_time
PID salınım yapıyor              Freewheeling task          01_task_types
HMI çok yavaş güncelleniyor      Starvation                 03_priority_mgmt
Drive titriyor / sync kaçıyor    Fieldbus task öncelik      03_priority_mgmt
Sayaç bazen sıfırlanıyor         Race condition             03_priority_mgmt
Event task çalışmıyor            Edge algılanmıyor          01_task_types
E-stop geç tepki veriyor         Safety task önceliği düşük 03_priority_mgmt
CPU %90+                         Cycle time çok kısa        02_cycle_time
```

## Sık Yapılan Hatalar

### Başlangıçta En Çok Yapılan 5 Hata

**1. Tek task her şeyi yapar** (Belge 1, 2, 3)  
Her şeyi tek Cyclic task'a koymak başlangıçta kolay görünür. Proje büyüyünce cycle time uzar, watchdog alarmları başlar, HMI yavaşlar. Başlangıçtan 3-5 task mimarisi kurmak bunu önler.

**2. PID'i Freewheeling'e koymak** (Belge 1, 2)  
Sık görülen hata, özellikle Siemens kökenli mühendislerde. OB1 mantığı burada geçerli değil. Freewheeling cycle time tutarsız; PID integral/türev hatalı hesaplanır.

**3. Fieldbus task cycle time yanlış** (Belge 2, 3)  
EtherCAT 2ms döngüdeyken task 10ms olarak ayarlanırsa her 5 EtherCAT döngüsünden sadece 1'i işlenir. Drive titrer, pozisyon kaybolur.

**4. Event task yüksek frekanslı sinyal için** (Belge 1)  
Encoder veya hızlı dijital sinyal Event task'a bağlanırsa runtime HALT'a geçer. Hızlı sinyaller için R_TRIG + Cyclic tercih edilir.

**5. CPU yük hesabı yapmamak** (Belge 2, 3)  
"Çalışıyor" demek "doğru çalışıyor" değildir. CPU %85'te çalışan sistemde fieldbus restart, OS güncelleme gibi ani yük artışları watchdog tetikler. Tasarım aşamasında %70 hedefi belirlenmeli.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Bu Sentezin Kapsamı

Bu 3 belge + sentez şu durumlar için yeterlidir:
- Standart makine otomasyonu (konveyör, paketleme, dolum, montaj)
- Motion kontrolü olan sistemler (EtherCAT + SoftMotion dahil)
- Çoklu PID döngülü proses kontrol

Bu durumlar için daha ileri kaynaklara bakılmalıdır:
- **SIL güvenlik gereksinimleri** → CODESYS Safety (ayrı ürün)
- **100+ task barındıran büyük sistemler** → Multicore + task affinity
- **Sub-µs zamanlama gereksinimleri** → FPGA/ASIC donanım, CODESYS yeterli olmayabilir
- **Birden fazla runtime arasında koordinasyon** → Distributed systems belgesi

## Gerçek Proje Notları

**Sentez Notu 1 — "5 Task Şablonu" Ne Zaman Yetmez?**  
5 task mimarisi neredeyse her standart makine için yeterlidir. Yetmediği durum: Çok sayıda bağımsız makine ekseninin farklı hızlarda kontrol edilmesi gerektiğinde (ör. 10 farklı PID döngüsü farklı zaman sabitleriyle). Bu durumda her döngü grubu için ayrı Cyclic task açmak yerine, task sayısını 3-4'te tutarak kodun içinde manüel örnekleme (her N döngüde bir çalış) yapılabilir.

**Sentez Notu 2 — Tasarım Başında 10 Dakika, Devreye Almada 2 Gün**  
Task mimarisini proje başında kâğıt üzerinde tasarlamak 10 dakika alır. Devreye alma sırasında task yapısını değiştirmek (POU'ları taşımak, watchdog ayarlamak, öncelikleri yeniden sıralamak) en az 2 gün ve müşteri tesisinde beklenmedik saatler demektir. "Önce çalıştır, sonra düzelt" yaklaşımı task mimarisinde işe yaramaz.

**Sentez Notu 3 — Fieldbus Geldiğinde Task Mimarisi Değişir**  
Pek çok projede ilk aşama Modbus TCP ile başlar, sonra müşteri EtherCAT servo ekler. EtherCAT gelince task mimarisi değişmek zorundadır: Yeni bir Cyclic 2ms task eklenir, güvenlik task'ı bu döngüye alınır, öncelikler yeniden sıralanır. Bu dönüşüm planlanmamışsa 1-2 günlük iş. Başlangıçtan "fieldbus eklenirse ne olur?" sorusu sorulmalı.

**Sentez Notu 4 — Task Monitor Her Devreye Almada Açık Olmalı**  
Task Monitor, task yapısının doğruluğunu kanıtlayan tek araçtır. Devreye alma sürecinde Task Monitor her zaman açık tutulmalı ve Max Cycle Time değerlerinin Interval'ın %70'ini geçmediği doğrulanmalıdır. "Çalışıyor" yeterli değil; "Max Cycle Time kontrol edildi, %70 altında" standardı hedeflenmelidir.

## İlgili Konular

```
knowledge/codesys/task-structure/    ← Şu an buradasınız
├── 01_task_types.md
├── 02_cycle_time.md
├── 03_priority_management.md
└── _synthesis.md (bu belge)

Önceki temel:
knowledge/codesys/fundamentals/
└── _synthesis.md → Runtime, proje yapısı, diller sentezi

Sonraki adım — EtherCAT entegrasyonu:
knowledge/networking/ethercat/
├── 01_ethercat_basics.md
└── 02_task_sync_ethercat.md

Sonraki adım — Gelişmiş mimari:
knowledge/codesys/advanced/
├── multicore_tasks.md
└── shared_memory_patterns.md
```
