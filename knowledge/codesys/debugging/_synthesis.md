---
KONU        : CODESYS Debugging — Sentez
KATEGORİ    : codesys
ALT_KATEGORI: debugging
SEVİYE      : Orta–İleri
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "knowledge/codesys/debugging/01_common_errors.md"
    başlık: "CODESYS Sık Karşılaşılan Hatalar ve Çözümleri"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/debugging/02_debugging_tools.md"
    başlık: "CODESYS Dahili Debug Araçları"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/debugging/03_performance_analysis.md"
    başlık: "CODESYS Performans Analizi"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_common_errors.md"
    ilişki: detaylandırır
  - konu: "02_debugging_tools.md"
    ilişki: detaylandırır
  - konu: "03_performance_analysis.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "CODESYS runtime ve proje yapısı (fundamentals/01_runtime_architecture.md, 02_project_structure.md)"
  - "Bu sentez, üç debugging belgesini okuduktan sonra bütünsel bakış için tasarlanmıştır."
ÇELİŞKİLER :
  - kaynak: "CODESYS Profiler erişimi"
    konu: "Profiler yalnızca Professional Developer Edition ile gelir; standart sürümde yoktur"
    çözüm: >
      Profiler olmadığında kod içi SysTimeGetUs() ölçümü + ikili arama yöntemi
      ile sorunlu POU daraltılabilir. Bu sentez her iki yolu da kapsar.
  - kaynak: "—"
    konu: "Bu sentez belgesi başka yeni çelişki içermez; kaynak belgelere atıflar yapar."
    çözüm: "—"
---

## Özün Ne

Bu sentez, "CODESYS'te bir sorunla karşılaşan biri üç debugging belgesini okuyunca ne anlamalı?" sorusuna yanıt verir. Üç belge birbiriyle sıkı sıkıya bağlıdır: **01_common_errors.md** ne tür hatalar çıkacağını ve bunların kökenini söyler; **02_debugging_tools.md** o köklere ulaşmak için hangi araçların kullanılacağını gösterir; **03_performance_analysis.md** ise görünür hata üretmeden sistemi yıpratabilecek gizli performans sorunlarını nasıl tespit edeceğimizi açıklar. Bu üçü birlikte okunduğunda CODESYS debug'ının tek bir yetkinliğe indirgendiği görülür: **Log'u oku, aracı seç, kaynağa in.**

---

## Nasıl Çalışır

### Üç Belgenin Birbirine Bağlantısı

```
┌─────────────────────────────────────────────────────────────────────┐
│                  CODESYS DEBUG ZİHİN HARİTASI                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  01_common_errors.md                                                  │
│  ┌───────────────────────────────────────────────────┐               │
│  │             HATA KATALOĞU (10 Hata)               │               │
│  │                                                   │               │
│  │  • Login/Gateway hatası   • Watchdog              │               │
│  │  • Download hatası        • RETAIN bozulması      │               │
│  │  • I/O mapping çakışması  • EtherCAT hatası       │               │
│  │  • Library not found      • Versiyon uyumsuzluğu  │               │
│  │                                                   │               │
│  │  Her hata: Belirti → Log'u oku → Neden → Çözüm   │               │
│  └──────────────────────┬────────────────────────────┘               │
│                         │ Hata tespit edildi → Araca ihtiyaç var     │
│                         ▼                                             │
│  02_debugging_tools.md                                                │
│  ┌───────────────────────────────────────────────────┐               │
│  │           DEBUG ARAÇ KİTİ (7 Araç)                │               │
│  │                                                   │               │
│  │  Watch Window   → Anlık değer izleme              │               │
│  │  Force Values   → I/O ve alarm simülasyonu        │               │
│  │  Breakpoint     → Kod akışını dondur              │               │
│  │  Trace Recorder → Her döngü kaydı, trigger        │               │
│  │  Online Change  → Çalışırken küçük güncelleme     │               │
│  │  Log Viewer     → Runtime mesajlarının kaynağı    │               │
│  │  PLC Shell      → plcload, task list, irq-list    │               │
│  └──────────────────────┬────────────────────────────┘               │
│                         │ Hata yok ama sistem ağır/jittery?          │
│                         ▼                                             │
│  03_performance_analysis.md                                           │
│  ┌───────────────────────────────────────────────────┐               │
│  │         PERFORMANS ANALİZ KATMANI                 │               │
│  │                                                   │               │
│  │  Task Monitor   → Exec/Cycle/Jitter metrikleri    │               │
│  │  PLC Shell      → plcload, task list              │               │
│  │  Kod İçi Ölçüm → SysTimeGetUs() + ikili arama    │               │
│  │  Profiler       → POU bazlı zaman (Pro Edition)   │               │
│  │  cyclictest     → OS jitter doğrulaması           │               │
│  │  Spike Analizi  → Trace + PRG_SpikeDetector       │               │
│  └───────────────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
```

### "Sorunu Görünce" İçin Özet Mental Model

CODESYS debugging'i anlamanın en kısa yolu şu üç kurala sığar:

> **Log her şeydir.** Ekranda gördüğün mesaj özettir, Log sekmesindeki mesaj tanıdır. Her sorun analizine `Device → Log sekmesi` ile başla.

> **Araç bağlamı belirler.** Breakpoint üretim makinesini durdurur; Trace durdurmadan kaydeder. Watch Window anlık fotoğrafı, Trace arıza öncesi filmi gösterir. Yanlış araç yeni sorun yaratır.

> **Ortalama yalan söyler, Max gerçeği söyler.** Task Monitor'da Average Cycle Time tatmin edici olsa da Max Cycle Time'da spike varsa sistem risk altındadır. Watchdog alarmı, Max'ın ihmal edilmesinin faturasıdır.

---

## Hızlı Referans Tabloları

### A. Hata Triage Matrisi (Belge 1)

| Belirti | İlk Kontrol | Büyük Olasılıkla Neden |
|---|---|---|
| "Cannot connect to device" | Gateway servisi çalışıyor mu? Port 1217 açık mı? | Gateway durmuş veya ağ/firewall sorunu |
| "Download failed: Unknown reason" | Log → Exception tipi ne? | GlobalInit, Retain uyumsuzluğu veya versiyon farkı |
| Uygulama aniden durdu | Log → "Watchdog exception in Task_X" | Sonsuz döngü, bloklanma veya CPU aşırı yük |
| "Library 'X' not found" | Library Manager → Sarı ikon | Kütüphane kurulu değil veya versiyon uyumsuz |
| "%Q0.0 address conflict" | Build çıktısı → Hangi dosyalar? | GVL'de aynı AT adresi iki değişkene atanmış |
| EtherCAT slave OP'a geçmiyor | EtherCAT → Diagnostics → Slave durumu | Kablo yanlış porta takılı (IN/OUT karışıklığı) |
| Power cycle sonrası parametreler sıfır | RETAIN yapısı değişti mi? | Yeni değişken eklendi → Retain sıfırlandı |
| "Device description not installed" | Device tree → Uyarı ikonu | .devdesc dosyası bu makinede kurulu değil |

### B. Debug Aracı Seçim Tablosu (Belge 2)

| Araç | Ne Zaman Kullan | Ne Zaman Kullanma | Kritik Kısayol |
|---|---|---|---|
| **Watch Window** | Anlık değer kontrolü, genel durum izleme | Hızlı değişen sinyallerde (200ms polling kaçırır) | Drag & drop veya sağ tık → Add Watch |
| **Force Values** | I/O testi, alarm simülasyonu, HMI olmadan test | Safety interlock aktifken, unforce risksizse | F7 force, Shift+F7 unforce |
| **Breakpoint** | Kod akışı debug, veri üzerine yazma tespiti | Canlı üretim makinesi, EtherCAT motion | F9 koy, F5 devam, F10 step |
| **Data Breakpoint** | Beklenmedik değişken değişimi kimin yaptığı | (Yalnızca Control Win V3'te çalışır) | Debug → New Data Breakpoint |
| **Trace Recorder** | Intermittent arıza, arıza öncesi analiz, her döngü | Basit anlık durum kontrolü | Trigger: rising edge + pre-trigger |
| **Online Change** | Küçük hata düzeltme (interface değişmeden) | Yeni değişken/POU/GVL değişimi, büyük refactor | Online → Login → "Yes" |
| **PLC Shell** | CPU yük, IRQ, versiyon, sistem bilgisi | Kod debug (bu araç değil) | `plcload`, `task list`, `irq-set-prio` |
| **Log Viewer** | **Her hata için — ilk bakış, hiç atla** | — | View → Log veya Device → Log sekmesi |

### C. Performans Eşik Değerleri (Belge 3)

| Metrik | Güvenli | İzle | Tehlike |
|---|---|---|---|
| Max Exec Time / Cycle Time | < %70 | %70–%85 | ≥ %100 (Watchdog) |
| Max Jitter / Cycle Time | < %10 | %10–%20 | > %20 (RT sorunu) |
| Toplam CPU Yükü (tüm task'lar) | < %70 | %70–%85 | > %85 |
| cyclictest Max Latency (RT kernel) | < 100µs | 100–500µs | > 500µs (motion için yetersiz) |
| EtherCAT Send/Recv Time (x64) | < 10µs | 10–50µs | > 50µs |
| EtherCAT Send/Recv Time (ARM) | < 50µs | 50–200µs | > 200µs |

### D. PLC Shell Kritik Komutları (Belge 2 + 3)

```bash
version           # Runtime versiyonu
plcload           # Anlık CPU yükü (%)
task list         # Tüm task'ların exec/cycle/jitter değerleri
app info Application  # Uygulama durumu
irq-list          # IRQ numaraları ve öncelikleri
irq-set-prio 32 85    # IRQ 32'nin önceliğini 85'e çek
rt-get kernelinfo # RT kernel kullanılıyor mu?
log clear         # Log'u temizle
```

### E. Online Change: Ne Olur / Ne Olmaz (Belge 2)

```
Yapılabilir:             Yapılamaz:
✓ POU kodunun içi        ✗ Yeni değişken ekleme/silme
✓ Sabit değerleri güncelle  ✗ Yeni POU/GVL
✓ IF koşullarını düzenle    ✗ Task yapılandırması
✓ Yorum ekleme/silme        ✗ Library ekleme/silme
                            ✗ I/O Mapping değiştirme
```

### F. Trace Buffer Boyutu Hesaplama (Belge 2)

```
Gerekli Buffer = Yakalanmak istenen süre (ms) / Cycle Time (ms)
Örnek: 5 saniye, 10ms task → 5000 / 10 = 500 döngü buffer
       3 saniye, 1ms task  → 3000 / 1  = 3000 döngü buffer
Pre-trigger genellikle buffer'ın %50–80'i olarak ayarlanır.
```

---

## Pratikte Nasıl Kullanılır

### "Sorun Çıktı" Kontrol Akışı

Her hata ve beklenmedik davranış için tek bir başlangıç noktası vardır:

```
Sorun gözlemlendi
       │
       ▼
1. Log sayfasını aç (Device → Log sekmesi)
       │
       ├── Hata mesajı net mi? → 01_common_errors.md'deki hata kataloğuna bak
       │
       ├── Hata mesajı yok, davranış yanlış?
       │     → Watch Window: şüpheli değişkenleri izle
       │     → Sorun izole edildi ama neden olduğu bilinmiyor?
       │           → Data Breakpoint veya Trace kur
       │
       ├── Watchdog alarmı?
       │     → Hangi task → Task Monitor → Max Exec Time bak
       │     → Dosya/ağ kodu mu → Freewheeling'e taşı
       │     → Sonsuz döngü mü → FOR/WHILE kontrolü
       │
       └── Hata yok ama sistem hissettiriyor ki ağır?
             → Task Monitor → 03_performance_analysis.md akışına geç
```

### "Devreye Alma Günü" Performans Kontrol Listesi (Belge 3'ten)

```
□ Task Monitor'u 48 saat izle (gece vardiyasını kapsasın)
□ Max Cycle Time < Cycle Time × 0.70 mı?
□ Tüm task'ların toplam yükü < %70 mı?
□ Max Jitter < Cycle Time × 0.10 mı?
□ EtherCAT sync zamanlaması (varsa) eşik altında mı?
□ Freewheeling task Max değeri anormal yüksek değil mi?
□ 48 saatte kaç spike? (PRG_SpikeDetector sayacı)
```

### Üç Belgeyi Birleştiren Pratik Senaryo

**Görev**: Çalışan bir sistemde motor akımı zaman zaman yüksek alarm veriyor, ama nedeni bilinmiyor.

```
ADIM 1 — Hata neyle başladı? (Belge 1)
  Log: "Alarm triggered: xMotorCurrentHigh"
  Download hatası veya watchdog yok → Sistem çalışıyor, belirti anlık.

ADIM 2 — Aracı seç (Belge 2)
  Watch Window ile anlık değerlere bak:
    GVL_IO.rMotorCurrent | GVL_Alarms.xMotorCurrentHigh | fbMotor.eState
  Sorun aralıklı ve izleme sırasında olmuyor → Watch Window kaçırıyor.
  
  Trace kur:
    Variables: rMotorCurrent, rMotorSpeed, xMotorCurrentHigh, rLoadSetpoint
    Trigger: xMotorCurrentHigh rising edge
    Pre-trigger: 300 döngü (10ms task → 3 saniye öncesi)
    Post-trigger: 100 döngü

ADIM 3 — Veriyi incele (Belge 2 + Belge 3)
  Alarm tetiklenince trace upload et.
  Grafik: Alarmdan 1.8 saniye önce rLoadSetpoint aniden arttı → akım yükseldi.
  rLoadSetpoint'i kimin yazdığını bul → Data Breakpoint kur.
  Kaynak: PRG_HMIUpdate beklenmedik değer yazıyor.

ADIM 4 — Performans etkisi var mı? (Belge 3)
  Task Monitor: Bu task'ın Max Exec Time güvenli aralıkta mı?
  PLC Shell > task list: Yük %55 → Normal.

ADIM 5 — Düzelt ve uygula (Belge 2)
  Küçük mantık düzeltmesi → Online Change ile canlı uygula.
  Watch Window ile rLoadSetpoint izle → Doğrula.
```

---

## Sık Yapılan Hatalar

### Belgeler Arası Ortak Tuzaklar

**1. Log'u atlamak, ekrandaki özet mesajla çözüm aramak** (Belge 1 + 2)  
"Download failed" ekranda görünce forum araması yerine önce `Device → Log sekmesi` açılmalıdır. Log 9/10 vakada doğrudan nedeni yazar (GlobalInit, Retain, Checksum).

**2. Watchdog'u kapatmayı "çözüm" saymak** (Belge 1)  
Watchdog süresini artırmak kök sorunu maskeleyerek zamanla daha büyük arıza biriktirir. Gerçek çözüm: hangi task, neden uzun sürdüğünü bulmak.

**3. Force'u Unforce etmeyi unutmak** (Belge 2)  
Session sonunda `View → Watch → Watch All Forces` kontrolü yapılmadan çıkılmamalıdır. Production'da aktif force kalan bir çıkış, HMI stop komutunu devre dışı bırakabilir.

**4. Breakpoint'i üretim makinesinde bırakmak** (Belge 2)  
Breakpoint tetiklenince tüm task'lar durur. Session sonunda rutin: `Debug → Delete All Breakpoints`.

**5. Average Cycle Time'a güvenmek, Max'ı görmezden gelmek** (Belge 3)  
Average: 10.1ms — sorun yok görünür. Max: 45.7ms — kimse bakmamış. Watchdog alarmının büyük çoğunluğu ihmal edilen Max değerlerinin birikiminden kaynaklanır.

**6. Trace buffer'ını küçük tutmak** (Belge 2 + 3)  
50 döngülük buffer arıza anından 0.5 saniye önceye bakabilir. Sorun 3 saniye önce başlıyorsa kayıp. Buffer = yakalanması gereken süre / cycle time formülüyle hesaplanmalı.

**7. 48 saatlik test olmadan üretime geçmek** (Belge 3)  
Gündüz devreye alma testleri gece ağ trafiğini, vardiya değişimlerini ve OS interrupt yükünü kapsamaz. İlk hafta uyku vakasının gateway'i, EtherCAT broadcast storm'un IRQ'yu boğduğu arızalar gece vardiyasında ortaya çıkmıştır.

**8. RETAIN değişken yapısını değiştirmeden önce yedek almamak** (Belge 1)  
RETAIN yapısına (arasına) yeni değişken eklemek download sırasında tüm retain değerlerini sıfırlar. Değişiklik öncesi değerleri kayıt al; sona ekle, araya ekleme.

---

## Ne Zaman ...

### Ne Zaman hangi belgeye dönülür?

```
Durum                                     Birincil Belge
──────────────────────────────────────────────────────────────
Login veya download sorunu                01_common_errors.md
Watchdog alarmı — hangi task, neden?      01_common_errors.md → 03_performance_analysis.md
Hata var ama nereden geldiği bilinmiyor   02_debugging_tools.md (Data Breakpoint/Trace)
Motor çıkışı gitmiyor, değer yanlış       02_debugging_tools.md (Watch Window → I/O Mapping)
Aralıklı arıza, yakalanması zor           02_debugging_tools.md (Trace + Trigger)
Sistem çalışıyor ama hissettiriyor ağır   03_performance_analysis.md (Task Monitor)
Spike var, hangi POU yavaş?               03_performance_analysis.md (ikili arama / Profiler)
Linux'ta jitter problemi, servo sallanıyor 03_performance_analysis.md (cyclictest, isolcpus)
EtherCAT slave OP'a geçmiyor              01_common_errors.md (Hata 8)
```

### Breakpoint mi Trace mi?

```
Breakpoint seç:
  → Kod akışını adım adım izlemek istiyorsun
  → Belirli bir değişkene kimin, ne zaman yazdığını bulmak istiyorsun (Data BP)
  → Geliştirme/simülasyon ortamındasın — makine üretimde değil

Trace seç:
  → Arıza aralıklı ve gerçek zamanlı yakalamak istiyorsun
  → Canlı makinede çalışmayı durdurmak istemiyorsun
  → Arızadan önceki 2-5 saniyeye bakmak istiyorsun
  → Watch Window değişimi kaçırıyor (hızlı sinyal)
```

### Online Change mi Tam Download mi?

```
Online Change:
  → POU içindeki mantık değişti, interface (değişken listesi) değişmedi
  → Üretimi durdurmak maliyetli
  → Küçük, izole bir düzeltme

Tam Download (makine durur):
  → Yeni değişken, yeni POU, GVL değişikliği
  → Task yapılandırması, library, I/O mapping değişti
  → SFC adım yapısı değişti
```

---

## Gerçek Proje Notları

**Sentez Notu 1 — Üç Belgenin Tamamlayıcılığı**  
Bu üç belge birer ayrı araç kutusu değil, katmanlar halinde çalışır: Hata triage (Belge 1) sizi doğru soruya götürür; debug araçları (Belge 2) o sorunun kaynağını bulmanızı sağlar; performans analizi (Belge 3) sorunun görünür hata üretmeden önce birikmesini engeller. Yalnızca Belge 1'i okumak "yangını söndürmek"; üçünü birlikte uygulamak ise "yangın alarm sistemi kurmak" gibidir.

**Sentez Notu 2 — "Garip Davranış" Her Zaman Bir Hata Kodu Üretmez**  
Sahada en zorlu vakalar hata mesajı üretmeyen vakalardır. Motor zaman zaman geç tepki veriyor; setpoint bazen yanlış değer alıyor; sistem bazen yavaşlıyor. Bu vakaların tamamında başlangıç noktası Trace ve Task Monitor'dur. Hata kodu olmadan da sistematik debug mümkündür; üç belge bu yolu birlikte çizer.

**Sentez Notu 3 — Performans Analizi Debug'dan Farklı Bir Disiplindir**  
Çoğu mühendis hata çıkınca debug yapar, çıkmazsa bakmaz. Oysa Belge 3'ün anlattığı performans analizi, hata üretmeyen gizli birikimi — yükselen Max Exec Time, büyüyen jitter, düzensiz spike'lar — görmek için gerçekleştirilir. 48 saatlik Task Monitor izlemesi ve cyclictest, devreye almadan önce "sessiz riskler"i ortadan kaldırır.

**Sentez Notu 4 — Sahadan En Çok Öğreten Vakalar**  
Belgelerdeki gerçek proje notları birer ders kitabı gibidir: Trace ile 3 günlük aralıklı arıza 1.2 saniyede basınç spike'ıyla çözüldü (Belge 2). Data Breakpoint ile 4 saatlik debug 20 dakikaya indi (Belge 2). RETAIN değişkeni eklenmesi operatörün 6 saatlik reçete verisini sildi (Belge 1). 48 saatlik test yapılmadan gece vardiyasında EtherCAT çöktü (Belge 3). Bu dört vakayı ezberlemek, yıllar içinde aynı hataları tekrarlamamak için yeterlidir.

**Sentez Notu 5 — Bu Bilgi Tabanının Kullanım Önerisi**  
Bu üç belge + sentez, bir CODESYS mühendisinin "ilk proje devreye alma" sürecinde nelerle karşılaşacağını ve nasıl yönetiyor olacağını kapsar. Önerilen akış:
1. Bu sentezi oku → Genel debug haritası anlaşıldı
2. `01_common_errors.md` → Olası hatalar ve triage akışı öğrenildi
3. `02_debugging_tools.md` → Araçlar denendi (Watch, Trace, Force)
4. `03_performance_analysis.md` → Task Monitor kuruldu, eşikler belirlendi
5. İlk projeyi 48 saatlik izlemeyle onayladın → Üretime güvenle geçildi

---

## İlgili Konular

```
knowledge/codesys/debugging/       ← Şu an buradasınız
├── 01_common_errors.md
├── 02_debugging_tools.md
├── 03_performance_analysis.md
└── _synthesis.md (bu belge)

Önkoşul — Temel:
knowledge/codesys/fundamentals/
├── 01_runtime_architecture.md    → Watchdog, scan cycle, runtime servisi
├── 02_project_structure.md       → POU, GVL, Task yapısı
└── 03_iec61131_languages.md      → ST/SFC kod yapısı debug bağlamı

Bağlantılı — Orta/İleri:
knowledge/codesys/task-structure/
├── 02_cycle_time.md              → Exec/Cycle time teorisi
└── 03_priority_management.md     → Linux IRQ öncelik tablosu

knowledge/codesys/programming/
└── 05_error_handling.md          → Programdan log'a mesaj yazma

Araçlar (harici):
  cyclictest    → Linux RT jitter ölçümü (apt install rt-tests)
  CODESYS Profiler → Professional Developer Edition (ücretli)
  PLC Shell     → Dahili komut satırı (Online Login → Device → PLC Shell)
```
