---
KONU        : CODESYS Debugging — Uzman Sentezi
KATEGORİ    : codesys
ALT_KATEGORI: debugging
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/codesys/debugging/01_common_errors.md"
    başlık: "CODESYS Sık Karşılaşılan Hatalar (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/debugging/02_debugging_tools.md"
    başlık: "CODESYS Dahili Debug Araçları (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/debugging/03_performance_analysis.md"
    başlık: "CODESYS Performans Analizi (Uzman)"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_common_errors.md"
    ilişki: detaylandırır
  - konu: "02_debugging_tools.md"
    ilişki: detaylandırır
  - konu: "03_performance_analysis.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/fundamentals/_synthesis.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Üç debugging belgesinin Uzman bölümleri okunmuş olmalıdır."
  - "fundamentals/_synthesis (determinizm), task-structure/_synthesis (jitter/watchdog), programming/_synthesis (tek-yazar/retain), networking/_synthesis kavranmış olmalıdır."
  - "Saha devreye alma ve arıza giderme deneyimi varsayılır."
ÇELİŞKİLER :
  - kaynak: "CODESYS Profiler erişimi"
    konu: "Profiler yalnızca Professional Developer Edition ile gelir"
    çözüm: "Profiler yoksa kod-içi SysTimeGetUs + ikili arama aynı işi yapar; sentez her ikisini kapsar."
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez yeni çelişki içermez; kaynak belgelere atıflar yapar."
---

## Özün Ne

Debugging üç ayrı beceri gibi görünür (hata kataloğu, araç kullanımı, performans ölçümü); uzman gözüyle hepsi **tek bir yöntemin** uygulamasıdır: **belirtiyi katmana haritala → o katmanda doğru aracı seç → kök nedene in → doğrula.** Bu, dört önceki sentezdeki "belirti→katman/ilke→kök neden" yaklaşımının teşhise dönüşmüş halidir.

Üç temel kural her şeyi özetler:
1. **Log tanıdır, ekran özettir** — ama bazı sorunlar log'a hiç yazılmaz (sessiz hatalar); o zaman katmana göre araç seçilir.
2. **Araç bağlamı belirler** — Breakpoint motion sistemini düşürür, Trace düşürmez; yanlış araç yeni sorun yaratır.
3. **Max gerçeği söyler, ortalama yalan söyler** — determinizm en-kötü-durum garantisidir; spike'lar ortalamada gizlenir.

Uzmanlık, hangi katmanda olduğunu hızla teşhis edip (altyapı/yapı/kod/performans) en az invazif doğru aracı seçmektir.

## Nasıl Çalışır

### Üç Belgenin Birbirine Bağlantısı

```
01 HATALAR ──────── ne tür sorun + hangi katman (triage)
        │ sorun tespit → kaynağa ulaşmak için araç gerek
        ▼
02 ARAÇLAR ───────── Watch/Force/Breakpoint/Trace/Online Change/Log/PLC Shell
        │ hata yok ama sistem ağır/jittery?
        ▼
03 PERFORMANS ────── Task Monitor/Profiler/cyclictest/spike analizi (gizli birikim)
```

### Teşhisin Çekirdeği: Belirtiyi Katmana Haritala

```
KATMAN              BELİRTİ ÖRNEKLERİ              BİRİNCİL ARAÇ
──────────────────────────────────────────────────────────────────
Altyapı (runtime/OS/ağ)  Login, gateway, versiyon  Log + PLC Shell + ping/telnet
Yapı (config)            RETAIN, library, I/O map   Log + Library Manager + I/O Mapping
Kod (logic)              watchdog, crash, NaN, değer Watch/Data BP/Trace
Performans (gizli)       jitter, spike, şişen exec   Task Monitor/Profiler/cyclictest
```

**Uzman içgörüsü:** Yanlış katmanda debug = boşa saatler. Login hatası kodda aranmaz (altyapı); watchdog gateway'de aranmaz (kod→performans). İlk soru her zaman "hangi katman?"dır.

### "Sorunu Görünce" Mental Modeli

> **Log her şeydir — ama her şey log'da değildir.** Önce `Device → Log`. Log boşsa veya yanıltıyorsa (bozuk bootapp, dangling pointer, sessiz cycle overrun, NaN) → katmana göre araç seç (01 edge cases).

> **Araç = bağlam.** Watch anlık fotoğraf (hızlı sinyal kaçar), Trace film (durdurmadan kaydeder), Breakpoint dondurma (motion'da eksen düşürür), Data BP "kim yazdı" (yalnız Win V3). En az invaziften başla: Log → PLC Shell → Trace → Watch → Force → Breakpoint.

> **Max gerçek, ortalama yalan.** Average Cycle iyi görünse de Max'ta spike varsa risk vardır; üstelik bazı sorunlar spike değil yavaş şişmedir (trend izle). Determinizm = en-kötü-durum.

## Hızlı Referans

### A. Hata Triage Matrisi (Belge 1)

| Belirti | Katman | İlk Kontrol | Olası Neden |
|---|---|---|---|
| "Cannot connect" | Altyapı | gateway + port 1217 + ping | gateway durmuş / ağ |
| "Download failed" | Yapı/Kod | Log → Exception tipi | GlobalInit / retain / versiyon |
| Aniden durdu | Kod→Perf | Log → watchdog task | sonsuz döngü / bloke / yük |
| "Library not found" | Yapı | Library Manager sarı ikon | kurulu değil / sürüm |
| "%Q address conflict" | Yapı | Build çıktısı | AT adres çakışması |
| Slave OP'a geçmiyor | Altyapı | EtherCAT diag + **kablo** | IN/OUT port (fiziksel) |
| Power-cycle eski davranış | Yapı | bootapp | Create Boot App unutuldu |
| Sporadik crash, farklı yer | Kod | — | dangling pointer (Online Change) |
| Çalışıyor ama ağır | Perf | Task Monitor Max | spike / şişen exec / jitter |

### B. Araç Seçim Tablosu (Belge 2)

| Araç | Kullan | Kullanma | İnvazivlik |
|---|---|---|---|
| **Log** | her hata, ilk bakış | — (asla atla) | sıfır |
| **PLC Shell** | yük/IRQ/versiyon/sistem | kod debug | sıfır |
| **Trace** | aralıklı arıza, arıza-öncesi, hızlı sinyal | basit anlık | düşük (runtime-yerel) |
| **Watch** | anlık değer, genel izleme | hızlı sinyal (200ms kaçar) | düşük (IDE polling) |
| **Force** | I/O/alarm testi | safety aktifken; unforce unutma | orta |
| **Data BP** | "kim bu değişkeni yazdı" | gerçek donanım (yalnız Win V3) | yüksek (durdurur) |
| **Breakpoint** | kod akışı, simülasyon | canlı motion/EtherCAT (düşürür) | en yüksek |
| **Online Change** | küçük mantık (interface aynı) | SFC/retain/interface/yapısal | değişir |

### C. Performans Eşikleri (Belge 3)

| Metrik | Güvenli | İzle | Tehlike |
|---|---|---|---|
| Max Exec / Cycle | < %70 | %70-85 | ≥ %100 (watchdog) |
| Max Jitter / Cycle | < %10 | %10-20 | > %20 (RT sorunu) |
| Toplam CPU | < %70 | %70-85 | > %85 |
| cyclictest Max (RT) | < 100µs | 100-500µs | > 500µs (motion yetersiz) |
| EtherCAT Send/Recv x64 | < 10µs | 10-50µs | > 50µs |

### D. PLC Shell Komutları

```
version · plcload · task list · app info Application
irq-list · irq-set-prio <n> <prio> · rt-get kernelinfo · log clear
```

### E. Uzman Edge Case Konsolidasyonu

```
ALAN       EDGE CASE                       YANILGI/BELİRTİ          KORUMA
──────────────────────────────────────────────────────────────────────────────
Hata(01)   bozuk bootapp                   "download başarılı" ama eski Create Boot App + power-cycle test
Hata(01)   dangling pointer crash          farklı yerde AccessViolation pointer her scan, saklama
Hata(01)   __TRY 64-bit                    derlendi ama çalışmıyor   savunmacı null/index kontrol
Hata(01)   sessiz cycle overrun            log'da hata yok           Task Monitor Max Cycle
Araç(02)   breakpoint motion'da            EtherCAT/eksen düşer       Trace kullan
Araç(02)   Watch hızlı sinyal              "hiç değişmiyor" sanılır   Trace (her döngü)
Araç(02)   force unforce unutuldu          stop çalışmaz (zombi)      Watch All Forces
Araç(02)   Online Change SFC               adım sıfırlanır            planlı duruş
Perf(03)   ortalamaya bakmak               "sağlıklı" ama spike var   Max Cycle Time
Perf(03)   yavaş şişen exec                tek ölçüm normal           trend izle (haftalık)
Perf(03)   profiler overhead'i             "o POU yavaş" yanılgısı    geniş→dar profil
Perf(03)   termal throttle                 yazın watchdog             en kötü termalde test
```

### F. Trace Buffer & Online Change

```
Buffer = yakalanacak süre / task cycle · pre-trigger = %50-80
Online Change YAPILABİLİR: POU içi mantık, sabit, IF, yorum
Online Change YAPILAMAZ: yeni değişken/POU/GVL, task config, library, I/O map, SFC yapısı
```

## Pratikte Nasıl Kullanılır

### "Sorun Çıktı" Kontrol Akışı (Uzman)

```
Sorun gözlemlendi
   │
   ▼ 1. Log oku (Device → Log) — ekran özetine güvenme
   │
   ├── Log net hata veriyor → katmanı belirle (01 triage matrisi)
   │      Altyapı → gateway/ağ/versiyon · Yapı → retain/lib/mapping
   │      Kod → araç seç (02) · Perf → Task Monitor (03)
   │
   ├── Log boş/yanıltıyor (sessiz hata)
   │      → bozuk bootapp? (power-cycle test) · dangling pointer? (data BP)
   │      → cycle overrun? (Task Monitor) · NaN? (__FINITE/watch)
   │
   ├── Hata yok, davranış yanlış
   │      → Watch (şüpheli değişken) → izole → Data BP/Trace (kim/ne zaman)
   │
   ├── Watchdog → hangi task (Log) → Task Monitor Max Exec → kök neden
   │      bloke I/O → Freewheeling · sonsuz döngü → FOR/WHILE · yük → böl
   │
   └── Çalışıyor ama ağır → 03 akışı: Task Monitor → spike/trend → optimizasyon hiyerarşisi
```

### Devreye Alma Performans Kontrol Listesi

```
□ Task Monitor 48 saat (gece vardiyası + en kötü termal dahil)
□ Max Cycle < Cycle × 0.70 · Toplam CPU < %70 · Max Jitter < Cycle × 0.10
□ EtherCAT sync eşik altında · Freewheeling Max anormal değil
□ cyclictest (RT kernel): Max < 100µs (motion için)
□ Spike sayacı ~0 · Max Exec trend kaydı başlatıldı (şişme izleme)
□ Create Boot Application + power-cycle test yapıldı
□ Tüm force kaldırıldı · tüm breakpoint silindi
```

### Üç Belgeyi Birleştiren Senaryo

```
Görev: motor akımı zaman zaman yüksek alarm, neden bilinmiyor

1. Katman? (01) Log: "alarm triggered", download/watchdog yok → Kod/sensör, aralıklı
2. Araç (02): Watch kaçırıyor (aralıklı) → Trace kur (akım+hız+setpoint+alarm),
   trigger=alarm rising, pre-trigger=300 döngü
3. İncele (02+03): alarmdan 1.8sn önce setpoint sıçramış → akım yükselmiş
   → setpoint'i kim yazdı? Data BP → PRG_HMIUpdate beklenmedik değer
4. Perf etkisi? (03): Task Monitor Max güvenli, plcload %55 → performans değil mantık
5. Düzelt (02): küçük mantık fix → Online Change → Watch ile doğrula
```

## Sık Yapılan Hatalar

### Belgeler Arası Ortak Tuzaklar

1. **Log'u atlamak** (01+02) — ekran özetiyle forum araması; önce Log sekmesi.
2. **Watchdog'u susturmak** (01) — süreyi artırmak kök sorunu maskeler; tanı sinyalidir.
3. **Force'u unforce etmemek** (02) — Watch All Forces ile session sonu kontrol.
4. **Breakpoint'i üretimde bırakmak** (02) — Delete All Breakpoints rutini.
5. **Ortalamaya güvenmek** (03) — Max Cycle Time tek anlamlı metrik.
6. **Trace buffer küçük** (02+03) — buffer = süre/cycle formülü.
7. **48 saat test yok** (03) — gece/termal/vardiya kapsanmaz.
8. **RETAIN değişikliği yedeksiz** (01) — sona ekle, değer yedekle.

### Uzman Tuzakları (5)

1. **Yanlış katmanda debug** — login'i kodda, watchdog'u gateway'de aramak; önce katman.
2. **Yanlış araç** — hızlı sinyale Watch, aralıklıya breakpoint, motion'a breakpoint (eksen düşer).
3. **Sessiz hatayı görmemek** — log'da iz yok (bootapp/pointer/overrun/NaN); katmana göre araç.
4. **Trend körlüğü** — yavaş şişen exec'i tek ölçümle kaçırmak; haftalık trend.
5. **Gözlemci etkisi** — profiler/trace'in kendi yükünü ölçtüğü şeyle karıştırmak.

## Ne Zaman ...

```
Hangi belge?           Login/download → 01 · araç gerek → 02 · ağır/jitter → 03
Breakpoint mi Trace?   adım-adım/simülasyon → BP · aralıklı/canlı/arıza-öncesi → Trace
                       motion/EtherCAT canlı → ASLA breakpoint → Trace
Online Change mi DL?   POU içi mantık → OC · yeni değişken/SFC/task/retain → tam download
Profiler mi kod-ölçüm? Pro Edition var + dar çevrim → Profiler · yoksa → SysTimeGetUs+ikili arama
Max mı ortalama mı?    HER ZAMAN Max (determinizm en-kötü-durum)
```

## Gerçek Proje Notları

**Sentez Notu 1 — Tek Yöntem: Belirtiyi Katmana Haritala**  
Üç belge ayrı beceri değil, tek teşhis yönteminin parçaları: katman belirle (01 triage) → araç seç (02) → kök nedene in → doğrula. Yanlış katmanda (login'i kodda) saatler kaybedilir. Uzman ilk soruyu "hangi katman?" diye sorar, sonra o katmanın aracını seçer. Bu, dört önceki sentezdeki "belirti→ilke→kök neden" pusulasının teşhise dönüşmesidir.

**Sentez Notu 2 — Log Tanıdır, Ama Her Şey Log'da Değildir**  
"Log her şeydir" doğru başlangıçtır ama eksiktir: bozuk bootapp, dangling pointer, sessiz cycle overrun, NaN yayılması log'a yazılmaz. Sessiz hatalarda Log boş/yanıltıcıdır; o zaman katmana göre araç (power-cycle test, data BP, Task Monitor, __FINITE) devreye girer. Uzman, log'un sustuğu yerde nereye bakacağını bilir.

**Sentez Notu 3 — Araç Bağlamı: En Az İnvazifle Başla**  
Her aracın görünmez bir bedeli var: Watch hızlı sinyali kaçırır, Breakpoint motion eksenini düşürür, Profiler ölçtüğünü yavaşlatır (gözlemci etkisi). Canlı sistemde sıralama: Log → PLC Shell → Trace → Watch → Force → Breakpoint. Trace'in runtime-yerel ring buffer mimarisi, onu canlı/intermittent vakalarda altın standart yapar — durdurmadan her döngüyü kaydeder.

**Sentez Notu 4 — Performans Debug'dan Ayrı Bir Disiplin**  
Çoğu mühendis hata çıkınca bakar; performans analizi (03) hata üretmeyen gizli birikimi görmek içindir: yükselen Max Exec, büyüyen jitter, yavaş şişen exec (algoritmik sızıntı), termal throttle. Max'a bakmak (ortalamaya değil), trend izlemek (tek ölçüme değil), 48 saat test (gece+termal) — bunlar "sessiz riskleri" devreye almadan önce ortadan kaldırır. Watchdog alarmı, atlanan performans analizinin faturasıdır.

**Sentez Notu 5 — En Çok Öğreten Vakalar**  
Belgelerdeki gerçek notlar ders kitabıdır: Trace ile 3 günlük aralıklı arıza 1.2sn basınç spike'ıyla çözüldü; Data BP ile 4 saatlik debug 20 dakikaya indi; RETAIN değişikliği 6 saatlik reçeteyi sildi; breakpoint motion eksenini düşürdü; 48 saat test yokluğu gece EtherCAT'i çökertti; termal throttle yazın watchdog verdi. Bu vakaları içselleştirmek, yıllar içinde aynı hataları tekrarlamamaktır — ve hepsi tek yönteme indirgenir: katman → araç → kök neden → doğrula.

## İlgili Konular

```
knowledge/codesys/debugging/       ← Şu an buradasınız (Uzman seviye)
├── 01_common_errors.md       (Uzman)
├── 02_debugging_tools.md     (Uzman)
├── 03_performance_analysis.md (Uzman)
└── _synthesis.md (bu belge)

Önkoşul / bağlı:
knowledge/codesys/fundamentals/   → determinizm, watchdog, I/O image, runtime servisi
knowledge/codesys/task-structure/ → jitter zinciri, %70 yük, RT tuning, omitted-cycle wd
knowledge/codesys/programming/    → tek-yazar, retain layout, pointer, __TRY/64-bit, NaN
knowledge/codesys/networking/     → fieldbus diag, blocking I/O, protokol analizi

Araçlar:
  cyclictest (Linux RT jitter) · CODESYS Profiler (Pro Edition) · PLC Shell · Wireshark · Trace
```
