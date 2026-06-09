---
KONU        : CODESYS Cycle Time Seçimi
KATEGORİ    : codesys
ALT_KATEGORI: task-structure
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://docs.codesys-p2cds622.com/en/latest/Additional%20Topics/jitter.html"
    başlık: "CODESYS P2CDS622 — Jitter, Latency, Cycle Time Tanımları"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Control/_rtsl_performance_optimization_linux.html"
    başlık: "CODESYS Control — Performance Optimization on Linux"
    güvenilirlik: resmi
  - url: "https://cdrdv2-public.intel.com/832560/improving-real-time-performance-of-codesys-control-applications-with-intel-s-real-time-technologies-1723443578.pdf"
    başlık: "Intel White Paper — Improving RT Performance of CODESYS (2022)"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Engineering/thread/d9ca4f6f53/"
    başlık: "CODESYS Forge — Cycle Time ve Jitter Analizi"
    güvenilirlik: topluluk
  - url: "https://www.plctalk.net/forums/threads/maximum-jitter-on-cpu-of-motion-controller.138404/"
    başlık: "PLCtalk — Motion Control için Maksimum Jitter"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_task_types.md"
    ilişki: gerektirir
  - konu: "03_priority_management.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Task tipleri (01_task_types.md)"
  - "Scan cycle ve I/O image kavramı (fundamentals/01_runtime_architecture.md)"
ÇELİŞKİLER :
  - kaynak: "Çeşitli platform denemeleri"
    konu: "Raspberry Pi için minimum cycle time: forum tartışmalarında farklı değerler"
    çözüm: >
      Standart Linux: ~10ms güvenli minimum.
      RT-preempt çekirdek + CPU izolasyonu ile 1ms'ye kadar inilebilir.
      İzole çekirdek olmadan 1ms altı önerilmez: tutarsız jitter yaşanır.
  - kaynak: "Intel White Paper (2022)"
    konu: "Maksimum CPU yük eşiği: %70 mü %80 mi?"
    çözüm: >
      Güvenli üst sınır için %70 önerilir. Intel testleri %80'de kararlı
      sonuçlar gösterse de gerçek projeler için %70 tampon payı tutulmalıdır;
      sürpriz yük artışlarına (ör. fieldbus yeniden başlatma) karşı koruma sağlar.
---

## Özün Ne

Cycle time, bir Cyclic task'ın ne sıklıkla çalışacağını belirler. Çok kısa seçilirse task sürekli watchdog ihlali yaşar, CPU dolup diğer task'lar çalışamaz. Çok uzun seçilirse sinyaller kaçırılır, geç tepki verilir, PID kararsız çalışır. Doğru cycle time seçimi, uygulamanın dinamik gereksinimlerini (en hızlı değişen sinyal, tepki süresi beklentisi, kullanılan fieldbus) ile donanımın işlem kapasitesini dengeleme sanatıdır. Bu dengeyi kuramayan projeler ya watchdog alarmlarıyla ya da "neden geç tepki veriyor?" sorusuyla boğuşur.

## Nasıl Çalışır

### Temel Kavramlar: Cycle Time, Jitter, Latency

```
Ideal (Konfigüre Edilen) Döngü: T₀ = 10ms
──────────────────────────────────────────────────────────
                T₀=10ms     T₀=10ms    T₀=10ms
Beklenen: │←──────────→│←──────────→│←──────────→│
          0ms          10ms         20ms         30ms

Gerçek:   │←───────────→│←─────────→│←───────────→│
          0ms           11ms        20ms          31ms
                  ↑ Jitter=1ms       ↑ Jitter=1ms

Latency: Task'ın başlaması gereken an ile gerçekte başladığı an arası gecikme.
Jitter:  Ardışık iki döngü başlangıç anı arasındaki sapma.
```

**Exec Time (Yürütme Süresi):** Task kodunun tamamlanması için geçen süre. Cycle time ile karıştırılmamalıdır.

```
Cycle Time = 10ms   (task ne sıklıkla çalışır)
Exec Time  = 2.3ms  (bir çalışmada ne kadar sürer)
Boşta Kalma: 10 - 2.3 = 7.7ms  (CPU bu task için bekliyor)
```

Exec Time, Cycle Time'ı geçemez — geçerse watchdog tetiklenir.

### Cycle Time ile Sinyal Örnekleme İlişkisi

Nyquist-Shannon örnekleme teoreminden pratik çıkarım:

```
Sinyal frekansını yakalamak için cycle time ≤ 1/(2 × f_sinyal) olmalı.
Güvenli kural: cycle time ≤ 1/(5 × f_sinyal)  (5x örnekleme payı)

Örnek:
  20Hz değişen sıcaklık sinyali → cycle time ≤ 1/100 = 10ms ✓
  Acil stop butonu (tepki < 50ms) → cycle time ≤ 10ms ✓
  1kHz encoder sinyali → donanım sayaç gerekir, yazılım cycle time ile yakalanmaz
```

### CPU Yük Hesabı

```
Tek task CPU yükü (yaklaşık):
  CPU Yük ≈ (Exec Time / Cycle Time) × 100%

Örnek: Exec Time = 3ms, Cycle Time = 10ms
  CPU Yük = (3/10) × 100 = %30

Birden fazla task varsa tüm yükler toplanır:
  Task_Safety  : 0.2ms / 1ms   = %20
  Task_Motion  : 0.5ms / 2ms   = %25
  Task_Control : 2ms  / 10ms   = %20
  Task_HMI     : 5ms  / 50ms   = %10
                           TOPLAM ≈ %75  ← Dikkatli olunmalı
```

Güvenli üst sınır: **%70**. Bu sınırın üstünde fieldbus yeniden başlatma, büyük veri transferi gibi ani yük artışları watchdog ihlaline neden olabilir.

### Fieldbus Cycle Time Kısıtlamaları

Fieldbus kullandığınızda task cycle time, fieldbus döngüsüyle eşleşmek zorundadır:

| Fieldbus | Tipik Döngü | Task Cycle Time |
|---|---|---|
| EtherCAT 1ms | 1ms | 1ms (tam eşleşme) |
| EtherCAT 2ms | 2ms | 2ms |
| PROFINET RT  | 4ms, 8ms | 4ms veya 8ms |
| CANopen 10ms | 10ms | 10ms |
| Modbus TCP   | 20-100ms | 20ms+ (gereksinime göre) |

EtherCAT ve PROFINET'te task cycle time, fieldbus döngüsünün tam katı olmalıdır; aksi halde sync kaybolur.

### Sinyal Türüne Göre Cycle Time Rehberi

| Sinyal / Uygulama | Önerilen Cycle Time | Açıklama |
|---|---|---|
| E-stop, güvenlik interlockları | 1–5ms | İnsan müdahalesi olmadan hızlı tepki |
| EtherCAT motion (servo) | 1–2ms | Fieldbus sync gereksinimi |
| PID sıcaklık kontrolü | 10–100ms | Termal sistemler yavaş değişir |
| PID basınç/akış kontrolü | 10–50ms | Sistem dinamiğine göre |
| Konveyör hız kontrolü | 10–20ms | Orta dinamik |
| Dijital I/O okuma (genel) | 10–20ms | Tipik makine mantığı |
| HMI değişken güncelleme | 50–200ms | Görsel yeterli |
| OPC UA / Modbus kommunikasyon | 50–500ms | Ağ gecikmesi hâkim |
| Log, diagnostik | 500ms–5s | Gerçek zamanlılık gerekmez |
| Alarm kontrolü | 5–20ms | Hızlı algılama, gecikme riski |

### Çok Kısa Cycle Time'ın Zararları

```
Senaryo: 10ms yeterli olan task için 1ms kullanmak.

Sorun 1 — CPU İsrafı:
  Task her 1ms'de çalışıyor, ama yapacak işi yok.
  1ms Cyclic → %100 frekans, %30 exec → %30 CPU boşa gidiyor

Sorun 2 — Diğer Task'ların Açlığı:
  Yüksek öncelikli 1ms task CPU'yu yoğun tüketirse
  düşük öncelikli task'lara yeterli CPU kalmaz.

Sorun 3 — Watchdog Riski:
  Exec time beklenmedik yük artışında (fieldbus restart, log flush)
  cycle time'ı geçer → gereksiz watchdog alarmı.

Kural: En kısa cycle time gerçek gereksinimden 2-3x daha kısa olmamalı.
```

### Çok Uzun Cycle Time'ın Riskleri

```
Senaryo: 10ms yeterli olan task için 100ms kullanmak.

Sorun 1 — Sinyal Kaçırma:
  50ms'de değişen bir sensör sinyali 100ms cycle time ile
  her seferinde yakalanacağı garanti edilemez.

Sorun 2 — PID Kararsızlığı:
  Uzun Δt ile çalışan PID integral/türev terimleri
  sistemin gerçek dinamiğini temsil edemez.

Sorun 3 — Geç Tepki:
  E-stop 100ms'de işlenirse makinenin 10cm daha hareket etmesi anlamına gelir.
  Güvenlik açısından kabul edilemez.
```

## Pratikte Nasıl Kullanılır

### Adım 1: Uygulamanın En Hızlı Bileşenini Belirle

```
Soru listesi:
□ En hızlı değişen sinyal hangisi? (ör. encoder, basınç, sıcaklık)
□ Fieldbus kullanılıyor mu? Hangi döngüde?
□ En kısa tepki süresi gereksinimi nedir? (ör. E-stop < 10ms)
□ PID loop varsa sistemin zaman sabiti nedir?
□ CPU kapasitesi nedir?
```

### Adım 2: Task Hiyerarşisini Tasarla

```
Her task için başlangıç cycle time değerleri:

Safety/Fast:  1–5ms  (güvenlik, hızlı acil durum)
Motion:       1–2ms  (servo, EtherCAT)
Control:     10–20ms (PID, ana makine mantığı)
Slow:        50–100ms(HMI, ağ)
Background: Freewheel(log, diagnostik)
```

### Adım 3: Online Monitörde Doğrula

Task yapılandırması tamamlandıktan sonra online bağlantıda:

```
Task Configuration → [Online görünüm] → Monitor sekmesi

İzleme metrikleri:
  Last Cycle Time  : Son döngü süresi
  Max Cycle Time   : En uzun döngü (spike izleme için kritik)
  Avg Cycle Time   : Ortalama döngü süresi
  Max Jitter       : Maksimum zamanlama sapması
  Min Jitter       : Minimum zamanlama sapması
```

**Kabul kriterleri:**
```
Max Cycle Time < Interval × 0.70   → ✓ Güvenli
Max Cycle Time < Interval × 0.85   → ⚠ İzle, yakın
Max Cycle Time ≥ Interval           → ✗ Watchdog riski — cycle time artır veya kodu böl
Max Jitter > Interval × 0.10        → ⚠ RT kernel gerekebilir
```

### Adım 4: Yük Testi

Üretim öncesi en az 48 saat boyunca yük testi yapılmalıdır. CODESYS Monitor tab'ındaki `Max Cycle Time` değeri bu süre boyunca izlenmeli, spike olup olmadığı kontrol edilmelidir.

```bash
# Linux'ta sistem yük simülasyonu (CODESYS dışarıdan stres test)
stress-ng --cpu 2 --cpu-load 50 --vm 2 --vm-bytes 256M --timeout 3600s

# Paralelde CODESYS Monitor'u izle — Max Cycle Time değişiyor mu?
```

## Örnekler

### Örnek 1: Cycle Time Hesabı — Sıcaklık Kontrol Sistemi

```
Uygulama: Fırın sıcaklık kontrolü (PID)
Sensör  : PT100 → 4-20mA → 0.1Hz değişim hızı (termal sistem yavaş)
Tepki   : Operatör setpoint değişikliğine 500ms içinde tepki yeterli
Fieldbus: Modbus RTU (polled, 100ms periyot)
CPU     : i7-8550U endüstriyel PC

Hesap:
  Sinyal frekansı  : 0.1Hz → 1/(5×0.1) = 2000ms → çok rahat
  Tepki gereksinimi: 500ms → en az 5 örnekle → 100ms yeterli
  Fieldbus döngüsü : 100ms → eşleşme
  
Karar: Task_TempControl → Cyclic, t#100ms, Prio:3
Onay  : %10 exec/cycle yük → CPU bolca var
```

### Örnek 2: Cycle Time Hesabı — Motion Kontrol

```
Uygulama: EtherCAT servo kontrol (5 eksen)
Fieldbus: EtherCAT, 2ms döngü
Tepki   : E-stop < 5ms
CPU     : Atom E3845 (4 çekirdek), Linux RT-preempt

Hesap:
  EtherCAT döngüsü : 2ms → task 2ms olmalı
  E-stop           : Task 2ms'de çalışıyorsa 2ms tepki → ✓
  Exec time beklenti: 0.5ms (5 axis calc) → %25 yük
  
Karar:
  Task_EtherCAT → Cyclic, t#2ms,  Prio:0 (EtherCAT sync)
  Task_Safety   → Cyclic, t#2ms,  Prio:1 (güvenlik, e-stop)
  Task_Control  → Cyclic, t#10ms, Prio:2 (koordinasyon)
  
CPU Yük: %25 + %5 + %20 = %50 → ✓ Güvenli
```

### Örnek 3: Monitörde Ne Görülmeli

```
Task_Control (Cyclic, 10ms):

Sağlıklı durum:
  Last: 10.0ms | Avg: 10.0ms | Max: 11.2ms | Jitter: ±0.3ms
  Exec: Avg 2.1ms | Max: 3.8ms

Sorunlu durum (müdahale gerekir):
  Last: 10.0ms | Avg: 10.0ms | Max: 28.4ms ← spike!
  Exec: Avg 2.1ms | Max: 17.6ms ← uzun exec
  
Teşhis: Kod içinde bloklanma var (dosya erişimi, uzun döngü?).
Çözüm : Uzun süren kodu daha düşük öncelikli / Freewheeling task'a taşı.
```

### Örnek 4: PLC Shell ile Yük İzleme

CODESYS IDE → Device → PLC Shell:

```bash
> plcload
PLC Load: 54%
Application: MainApplication
  Task_Safety  [1ms  Prio:0]: Exec avg 0.18ms  Max 0.31ms  Jitter ±0.05ms
  Task_Motion  [2ms  Prio:1]: Exec avg 0.52ms  Max 0.89ms  Jitter ±0.12ms
  Task_Control [10ms Prio:2]: Exec avg 2.20ms  Max 3.60ms  Jitter ±0.30ms
  Task_HMI     [50ms Prio:5]: Exec avg 4.10ms  Max 8.90ms  Jitter ±1.20ms
  Task_Log   [Freewheel p:15]: Exec avg 12.0ms Max 620ms  ← Dikkat!
```

`Task_Log`'un Max 620ms'si alarm vermez (Freewheeling) ama kodun neden bloklandığı araştırılmalıdır (USB yazma sorunlu).

## Sık Yapılan Hatalar

### Hata 1: Tüm Task'ları Aynı Cycle Time ile Yapılandırmak

```
❌ Yanlış:
  Task_Safety:  10ms
  Task_Motion:  10ms
  Task_Control: 10ms
  Task_HMI:     10ms

  Sorun: Tüm task'lar aynı anda çalışmaya çalışır → çakışma, öncelik
  belirsizliği, gereksiz CPU tüketimi.

✅ Doğru: Her task kendi gerçek gereksinimini karşılayan cycle time'a sahip.
```

### Hata 2: Cycle Time'ı Daraltarak "Daha İyi" Kontrol Sağlamaya Çalışmak

```
Yanılgı: "Cycle time'ı 10ms'den 1ms'ye indirirsem PID daha iyi çalışır."

Gerçek : PID kalitesi cycle time/sistem dinamiği oranına bağlıdır.
         Sistemin zaman sabiti 10 saniye ise 1ms yerine 100ms de yeterlidir.
         1ms ile 100ms fark edilmez; ama CPU yükü 100x artar.
```

### Hata 3: Max Cycle Time Spike'larını Görmezden Gelmek

```
Gözlem: Avg Cycle Time normal, ama Max Cycle Time zaman zaman Interval'ı aşıyor.
Tepki : "Bazen oluyor, sorun yok."

Gerçek: Spike, kodda beklenmedik gecikme var demektir.
        Uzun vadede Watchdog alarmına, veri tutarsızlığına dönüşür.
        Spike'ın kaynağı bulunmalı ve çözülmelidir.
```

### Hata 4: Fieldbus Cycle Time'ını Göz Ardı Etmek

```
❌ Yanlış: EtherCAT 2ms döngü, Task_EtherCAT = Cyclic 10ms
  Sonuç: Her EtherCAT döngüsü işlenmez, 5 döngüde 1 işlenir.
         Drive'lar geç komut alır, titreme, pozisyon hatası.

✅ Doğru: Task_EtherCAT = Cyclic 2ms (fieldbus döngüsüyle tam eşleşme)
```

### Hata 5: Dinamik Veri Transferini Kontrol Task'ına Koymak

```
❌ Yanlış: USB'ye büyük veri yazma, veritabanı sorgusu, HTTP isteği
           → Task_Control (Cyclic 10ms) içinde

  Sorun: Dosya/ağ işlemleri bloke olabilir → Max Exec Time 600ms → Watchdog

✅ Doğru: Tüm I/O yoğun, bloklanma riski olan işlemler → Freewheeling task
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Cycle Time Aralıklarının Kullanım Kılavuzu

**1ms veya altı:** Sadece EtherCAT/PROFINET RT sync task ve güvenlik acil durum task'ları. Zorunlu değilse kullanma; CPU yükü yüksek, jitter toleransı sıfır.

**2–5ms:** Motion control, hızlı PID döngüleri, encoder bazlı konum kontrol. Gerçek RT kernel gerekebilir.

**10–20ms:** Genel makine kontrol mantığı, konveyör, valves, orta hız PID. CODESYS projelerinin %80'i buraya girer.

**50–100ms:** HMI değişken güncellemesi, yavaş proses (sıcaklık, seviye). Kesinlikle yeterli; daha kısa yapmaya gerek yok.

**100ms–1s:** Alarm yönetimi, yavaş haberleşme, log zamanlayıcıları.

**Freewheeling:** Arka plan log, diagnostik, CPU boşaltma amaçlı görevler. Kontrol mantığı asla buraya girmemeli.

## Gerçek Proje Notları

**Not 1 — "1ms Yeterli Değil mi?" Sorusunun Cevabı**  
Endüstriyel PC'ler için 1ms cycle time mümkün ama Raspberry Pi veya zayıf ARM işlemcilerde RT-preempt çekirdek olmadan 1ms'de güvenilir çalışma sağlanamaz. Bir projede Pi üzerinde 1ms Cyclic task denenmiş, standart Raspbian'da max jitter 300ms'ye çıkmış. RT-preempt çekirdek kurulduktan sonra max jitter 1ms altına indi.

**Not 2 — 48 Saat Testi Zorunlu**  
Bir paketleme hattında devreye alma günü her şey mükemmeldi. 3 gün sonra gece vardiyasında watchdog alarmı. Araştırma: Gece güncelleme kontrolü (arka planda çalışan OS servisi) CPU'yu anlık %30 artırıyordu; bu da Task_Control'ün Max Exec Time'ını interval'ı aşmasına neden oluyordu. Linux'ta güncelleme servisleri devre dışı bırakıldı. Ders: 48 saat yük testi, kısa testlerde görünmeyen spike'ları ortaya çıkarır.

**Not 3 — Yanlış Cycle Time Seçiminin Ekonomik Maliyeti**  
Bir boya hattında Task_Control 1ms olarak yapılandırılmış (gerek yoktu, 20ms yeterliydi). CPU %85 yükte çalışıyordu. HMI güncellemesi yavaşlamıştı, OPC UA bağlantısı zaman zaman kopuyordu. Cycle time 20ms'ye alındı; CPU %25'e indi, tüm sorunlar ortadan kalktı. Toplam değişiklik süresi: 10 dakika. "Daha sık = daha iyi" yanılgısının bedeli.

**Not 4 — Max Cycle Time İzlemenin Değeri**  
Log yazma task'ının zaman zaman 620ms sürdüğü görüldü. Araştırma: CAA File kütüphanesi ile USB'ye yazma, USB meşgulken bloke oluyordu. Çözüm: Log data önce RAM'deki buffer'a yazıldı, Freewheeling task arkaplanda buffer'ı USB'ye boşalttı. Max Exec Time 15ms'ye indi, ana task etkilenmez oldu.

**Not 5 — Termal Throttling Nedeniyle Gece Yavaşlayan Sistem**  
Bir fansız endüstriyel PC, gündüz sıcağında Max Cycle Time'ı %40 artırıyordu. Neden: CPU sıcaklığı eşiği geçince termal throttling devreye girip frekansı düşürüyordu — exec time uzuyordu. Test ortamı klimalıydı, saha kabini değildi. Ders: Cycle time bütçesini **en kötü termal koşulda** (kapalı kabin, yaz, tam yük) doğrulayın; oda sıcaklığındaki ölçüm yanıltıcıdır. Kabin sıcaklığı + CPU frekansını telemetriye ekleyin.

**Not 6 — Online Change Sırasındaki Anlık Spike**  
Devreye almada her Online Change anında Max Cycle Time bir kez tavan yapıyordu (örn. 10ms task'ta 45ms). Bu normaldir: Online Change, kodu değiştirirken kısa bir senkronizasyon noktası yaratır. Tehlike: Watchdog sensitivity 1 ise bu tek spike watchdog'u tetikleyebilir. Ders: Üretimde Online Change yapılacaksa watchdog sensitivity'yi spike'ı tolere edecek şekilde (≥2-3) ayarlayın veya kritik anlarda Online Change'den kaçının.

**Not 7 — Garbage/Fragmentasyon Olmayan Ama "Yavaşça Şişen" Exec Time**  
Bir sistemde exec time haftalar içinde yavaşça arttı. Neden: Bir diagnostik buffer (array) her döngü doluyor, içinde lineer arama yapan kod büyüdükçe yavaşlıyordu (`O(n)` arama, n zamanla büyüyor). Cycle time sabit kaldı ama exec time/cycle oranı tehlikeli bölgeye girdi. Ders: Exec time'ın **trendini** izleyin, tek anlık değeri değil; veri yapısı büyüdükçe algoritmik karmaşıklık exec time'a sızar.

## Edge Case'ler ve Sistem Limitleri

### Cycle Time'ın Scheduler Interval'i ile İlişkisi

Bir Cyclic task'ın interval'i, scheduler interval'inin **tam katı** olmalıdır:

```
SchedulerInterval = 1ms (varsayılan)
  ✓ Task interval: 1, 2, 5, 10, 20, 100ms (1ms'in katları)
  ✗ Task interval: 1.5ms, 0.7ms → en yakın kata yuvarlanır/uyarı

SchedulerInterval = 250µs ise → 250µs altı task imkânsız
```

İstenen 1.5ms gibi bir değer, scheduler 1ms ise ya 1ms'ye ya 2ms'ye oturur — "yaklaşık" çalışır ama gerçek frekans beklenenden farklıdır. Sub-millisecond task için önce `SchedulerInterval`'i düşürmek gerekir, bu da tüm sistemin overhead'ini artırır.

### Jitter'ın Cycle Time'ı Geçtiği Kritik Eşik

```
Jitter < Cycle Time × 0.10   → İhmal edilebilir
Jitter ≈ Cycle Time          → Determinizm tamamen kaybolur
Jitter > Cycle Time          → Task sırası belirsiz, fieldbus sync imkânsız
```

1ms hedef cycle'da 300µs jitter (standart Linux), efektif olarak 0.7ms–1.3ms arası rastgele bir periyot demektir — motion kontrol için kabul edilemez. Bu yüzden sub-ms cycle, RT-preempt + izole CPU olmadan anlamsızdır (jitter cycle'ı yer).

### En Kısa Uygulanabilir Cycle Time (Platforma Göre)

| Platform | RT'siz Güvenli Min | RT-preempt + izolasyon |
|---|---|---|
| Endüstriyel x86 IPC | ~5-10ms | 250µs–1ms |
| Atom / düşük güç x86 | ~10ms | 1ms |
| Raspberry Pi 4 | ~10ms | 1ms (dikkatli tuning) |
| Zayıf ARM (Cortex-A7) | ~20ms | 2-5ms |
| Raspberry Pi (standart Raspbian) | ~10ms | — (jitter 300ms'e çıkabilir) |

### Watchdog ile Cycle Time İlişkisinde İnce Ayar

```
Watchdog Time çok dar (≈ cycle time):   sahte (false) tetik riski
Watchdog Time çok geniş (10× cycle):    gerçek takılmayı geç yakalar
Pratik kural: Watchdog Time ≈ 2-5 × beklenen Max Exec Time
              Sensitivity ≈ 2-3 (tek spike'ı tolere et, kalıcı sorunu yakala)
```

## Optimizasyon

### Exec Time'ı Düşürme Teknikleri (Cycle Time'a Dokunmadan)

Cycle time'ı uzatmak yerine, çoğu zaman exec time'ı düşürmek daha doğrudur:

```
1. Ağır işi alt-örnekle: her döngü değil, her N döngüde bir çalıştır
   (bkz. 01_task_types Optimizasyon → sub-sampling)
2. Bloke eden I/O'yu (dosya/ağ) ayrı Freewheeling task'a taşı
3. Döngü-değişmezi hesapları döngü dışına çıkar (loop-invariant hoisting)
4. Lineer arama yerine indeksli/hash erişim; büyüyen array'lerde O(n)'den kaç
5. String işlemlerini sıcak task'tan çıkar
6. Büyük struct/array'leri VAR_IN_OUT (referans) ile geçir, kopyalama
```

### CPU Yük Dengeleme: Tek Büyük Task yerine Katmanlama

```
❌ Tek task: 10ms cycle, exec 8ms → %80 yük, watchdog'a 2ms pay
✅ Bölünmüş:
   Task_Fast    10ms, exec 2ms (kritik) → %20
   Task_Slow   100ms, exec 6ms (yavaş)  → %6
   Toplam %26, her ikisi de bol watchdog payına sahip
```

Yavaş işi yavaş task'a taşımak, kritik döngünün exec time'ını ve dolayısıyla jitter'ını düşürür.

### Cycle Time'ı Fieldbus'a Hizalama (Sync Optimizasyonu)

EtherCAT Distributed Clocks (DC) modunda task, fieldbus döngüsüyle **faz kilitli** olmalıdır — sadece aynı periyot değil, aynı an. CODESYS'te bu "Sync with EtherCAT" / "I/O bus cycle task" seçeneğiyle yapılır. Task'ı bağımsız 2ms Cyclic yapmak periyodu eşler ama fazı eşlemez; DC için task doğrudan fieldbus'a bağlanmalıdır. Yanlış: serbest 2ms task. Doğru: EtherCAT master'ın bus cycle task'ı olarak atanmış task.

## Derin Teknik Detay

### Cycle Time Neden "Garanti" Değil de "Hedef"?

CODESYS'te `Interval`, task'ın çalışmaya **başlamayı hedeflediği** periyottur — başlama anının kesinliği değil. Gerçek başlangıç, o anda daha yüksek öncelikli bir task çalışıyorsa gecikir (jitter). Yani:

```
Interval     = sözleşme (her 10ms'de bir çalışmaya çalış)
Latency      = sözleşmenin ne kadar geç başladığı
Jitter       = latency'nin döngüden döngüye değişimi
Exec Time    = çalışınca ne kadar sürdüğü
```

Bu dört kavram bağımsızdır. Mükemmel kod (düşük exec) bile, üst öncelikli bir task veya OS gürültüsü yüzünden yüksek jitter yaşayabilir. Cycle time tasarımı, dördünü birlikte yönetmektir — yalnızca interval seçmek değil.

### I/O Image ile Cycle Time'ın Gizli Maliyeti

Her Cyclic task döngüsü, kod çalışmadan **önce** input image'i tazeler, **sonra** output image'i yazar (`fundamentals/01`). Bu I/O kopyalama, exec time'a dahildir ve task ne kadar çok I/O kanalına bağlıysa o kadar büyür. 1000 kanallı bir EtherCAT topolojisinde, "kod" 0.1ms sürse bile I/O image güncellemesi 0.3ms ekleyebilir. Çok kısa cycle time + çok I/O kombinasyonunda, exec time'ın çoğu kodda değil, I/O image transferinde geçer — bu, "kodu optimize ettim ama hızlanmadı" şaşkınlığının kaynağıdır.

### Nyquist'in PLC'ye Uyarlanması — Neden 5× Pay?

Nyquist teoremi, bir sinyali yeniden inşa etmek için ≥2× örnekleme der. Ama PLC kontrolünde amaç yeniden inşa değil **tepki**tir; ayrıca aliasing ve faz gecikmesi kontrol kararlılığını bozar. Pratik 5× kuralı şu nedenlerden gelir:

- **Faz gecikmesi:** 2× örneklemede en kötü durumda yarı periyot gecikme oluşur; kapalı çevrim kontrolde bu, faz marjını yer ve salınıma yol açar.
- **Jitter payı:** Gerçek örnekleme anı jitter ile kayar; 5× pay bu kaymayı yutar.
- **Türev gürültüsü:** PID türev terimi, az örneklemede gürültüyü büyütür.

Yani 5× kuralı, teorik Nyquist sınırının üstüne kontrol kararlılığı ve gerçek-dünya jitter'ı için eklenmiş mühendislik payıdır.

### CPU Yük Formülünün Sınırı: Neden %70?

`Σ(exec/cycle) < %70` formülü ortalama yükü verir ama **anlık (instantaneous) yükü** gizler. Kritik an: tüm task'lar aynı scheduler tick'inde hizalandığında (ör. 1ms, 2ms, 10ms task'ların hepsi t=0, 10, 20...'de buluşur). O anda CPU bir mikro-saniye penceresinde %100'e fırlar; ortalama %53 olsa bile. %70 hedefi, bu hizalanma spike'ları + fieldbus restart/OS gürültüsü gibi ani yükler için tampondur. Matematiksel ortalama yanıltıcıdır; gerçek tehlike, periyotların en küçük ortak katında buluşan yük zirvesidir.

## İlgili Konular

```
knowledge/codesys/task-structure/
├── 01_task_types.md          → Cyclic vs Freewheeling seçimi
├── 03_priority_management.md → Cycle time ve öncelik etkileşimi
└── _synthesis.md             → Task mimarisi tasarım kılavuzu

knowledge/codesys/fundamentals/
└── 01_runtime_architecture.md → Scheduler interval, jitter temelleri

knowledge/codesys/advanced/
└── profiling_codesys.md      → CODESYS Profiler ile exec time analizi

knowledge/networking/
├── ethercat/cycle_time.md    → EtherCAT sync ve task eşleşmesi
└── profinet/cycle_time.md    → PROFINET RT döngü yapılandırması
```
