---
KONU        : CODESYS Domaini — Üst Sentez (Uzman)
KATEGORİ    : codesys
ALT_KATEGORI: codesys
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/codesys/fundamentals/_synthesis.md"
    başlık: "CODESYS Temeller Sentezi (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/task-structure/_synthesis.md"
    başlık: "CODESYS Task Yapısı Sentezi (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/_synthesis.md"
    başlık: "CODESYS Programlama Mimarisi Sentezi (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/networking/_synthesis.md"
    başlık: "CODESYS Networking Sentezi (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/project-generation/_synthesis.md"
    başlık: "CODESYS Otomatik Proje Üretimi Sentezi (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/debugging/_synthesis.md"
    başlık: "CODESYS Debugging Sentezi (Uzman)"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/codesys/fundamentals/_synthesis.md"
    ilişki: bileşen
  - konu: "knowledge/codesys/task-structure/_synthesis.md"
    ilişki: bileşen
  - konu: "knowledge/codesys/programming/_synthesis.md"
    ilişki: bileşen
  - konu: "knowledge/codesys/networking/_synthesis.md"
    ilişki: bileşen
  - konu: "knowledge/codesys/project-generation/_synthesis.md"
    ilişki: bileşen
  - konu: "knowledge/codesys/debugging/_synthesis.md"
    ilişki: bileşen
ÖNKOŞUL     :
  - "Altı alt sentezin Uzman bölümleri okunmuş olmalıdır; bu belge onların ortak ilkelerini birleştirir."
  - "Saha devreye alma, arıza giderme ve mimari tasarım deneyimi varsayılır."
  - "Alternatif: Bu belgeyi harita olarak oku, ardından ilgili alt senteze geç."
ÇELİŞKİLER :
  - kaynak: "project-generation/_synthesis.md — Hibrit yaklaşım"
    konu: "Tam otomatik üretim mi, hibrit şablon yaklaşımı mı?"
    çözüm: >
      En sağlam yaklaşım elle hazırlanmış template (device tree, library, task iskeleti)
      ile otomatik GVL/POU/implementasyon üretiminin kombinasyonudur. Sıfırdan tam
      otomatik üretim kırılgandır.
  - kaynak: "fundamentals/_synthesis.md — Runtime varyantları"
    konu: "Geliştirme ortamı ile üretim ortamı arasındaki zamanlama farkı"
    çözüm: >
      CODESYS Control Win SL gerçek zamanlı değildir; üretim için Control Linux SL
      (RT-preempt) veya Control RTE SL kullanılmalıdır. Geliştirmede her şeyin
      çalışması, üretim donanımında sorunsuz çalışacağının garantisi değildir.
---

## Özün Ne

CODESYS, herhangi bir donanımı IEC 61131-3 uyumlu bir PLC'ye dönüştüren SoftPLC ekosistemidir — runtime, geliştirme ortamı, protokol kütüphaneleri ve otomasyon araçlarından oluşan bütünleşik bir platform.

Bu bilgi tabanı CODESYS'i altı alana böler (Temeller, Task Yapısı, Programlama, Networking, Project Generation, Debugging). Ama **uzman seviyesinde asıl mesaj, bu altı alanın ayrı konular değil, tek bir tasarım felsefesinin katmanları olduğudur.** O felsefe **determinizm**dir: *"endüstriyel kontrolün her kararı, her döngüsü, her veri akışı öngörülebilir ve en-kötü-durum garantili olmalıdır."*

`fundamentals` bu felsefeyi kurar (JIT yok, I/O image, bellek görüntüsü koruma); diğer beş alan onu kendi katmanında uygular. Uzmanlık, bir saha belirtisini (jitter, race, kaybolan veri, watchdog, üretim hatası) doğru katmana haritalayıp determinizm zincirinin hangi halkasının koptuğunu bulabilmektir. Bu altı alan birlikte tek bir bütün oluşturur: **"IEC kodunu deterministik çalıştıran; güvenilir, bakımı kolay, dış dünyaya açık, otomatik üretilebilir ve sistematik teşhis edilebilir bir endüstriyel kontrolcü."**

---

## Birleştirici İlke: Determinizm Zinciri

Altı alanın her biri, determinizm felsefesini kendi katmanında somutlaştırır. Bunlar bağımsız kurallar değil, tek bir zincirin halkalarıdır — ve **en zayıf halka tüm sistemin determinizmini belirler** (uçtan uca özellik).

| Alan | Determinizmin O Katmandaki İfadesi | Kök Birleştirici İlke |
|---|---|---|
| **① Temeller** | JIT yok (her döngü aynı süre) · I/O image (giriş tutarlılığı) · Component Manager | Donanım soyutlama + bellek görüntüsü koruma + öngörülebilirlik |
| **② Task Yapısı** | tip/cycle/öncelik = tek determinizm bütçesi · jitter < %10 · %70 yük | Öngörülebilirlik bir bütçedir; üç boyut birlikte yönetilir |
| **③ Programlama** | tek-yazar (race önler) · tek yönlü akış · ELSE→eFault · katmanlı fail-safe | Paylaşımlı durumun tek sahibi; hata önlenir, oluşursa güvenli duruma |
| **④ Networking** | hiçbiri RT değil (raporlama ≠ kontrol) · GVL temeli · bloke-I/O ayrımı | Raporlama katmanı kontrol determinizmini bozmamalı |
| **⑤ Project Generation** | idempotent üretim · DUT→GVL→FB→PROGRAM · "derlendi ≠ çalışıyor" | Deterministik, tekrarlanabilir, doğrulanmış çıktı |
| **⑥ Debugging** | Max (ortalama değil) · belirti→katman→kök neden · 48h test | En-kötü-durum görünür kılınır; teşhis sistematiktir |

### Tüm Domaini Kesen Tekrarlayan Desenler

Aynı birkaç ilke her alanda farklı kılıkta tekrar eder — bunları tanımak uzmanlığın özüdür:

```
DESEN                        NEREDE TEKRAR EDER
──────────────────────────────────────────────────────────────────────────
"Tek-yazar"                  GVL→tek task yazar (③) · FB→sadece output (③) ·
                             PROGRAM tek çağrı (③) · Modbus HR tek yön (④) ·
                             preemptive race önleme (②) · üretim tek-yazar (⑤)

"Belirti→katman→kök neden"   task boyutu (②) · ilke ihlali (③) · eksen/ilke (④) ·
   (teşhis pusulası)          katman→araç (⑥) · ilke→neden (⑤)

"Uçtan uca zincir,           determinizm (①→②→⑥) · RT (kernel→IRQ→task→kod) ·
   en zayıf halka belirler"   güvenlik (④) · framing (④) · fail-safe katmanları (③⑤)

"Çalışıyor ≠ doğru"          dev≠prod (①) · Max≠ortalama (⑥) · derlendi≠çalışıyor (⑤) ·
                             sessiz cycle overrun (⑥) · semantic hata (⑤)

"Bellek layout / sıra"       retain sona ekle (①③) · PERSISTENT sıra (③) ·
                             Online Change interface (①③⑥) · word tearing (④) ·
                             üretim DUT→FB sırası (⑤)

"Bloke-I/O düşük önceliğe"   Freewheeling log (②) · TCP connect (④) · MQTT broker (④) ·
                             dosya yazma watchdog (⑥)
```

**Uzman içgörüsü:** Yeni bir sorun gördüğünde önce "hangi katman?" (teşhis pusulası), sonra "hangi tekrarlayan desen ihlal edildi?" diye sor. Çözüm neredeyse her zaman bu altı desenden biridir; alana özgü ezber değil, ilke transferi.

---

## Nasıl Çalışır

### Altı Alanı Birbirine Bağlayan ASCII Zihin Haritası

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CODESYS DOMAİNİ — BÜTÜNSEL HARİTA                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ① TEMELLER — Zemin                                                           │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  Runtime (SoftPLC) + Proje Yapısı (Device→Application→POU) + Diller  │   │
│  │  Donanımı PLC'ye dönüştürür; tüm diğer alanların inşa edildiği zemin │   │
│  └──────────────────────────────────┬────────────────────────────────────┘   │
│                                     │ Runtime üzerinde çalışacak             │
│                                     │ projenin zamanlaması tasarlanır         │
│                                     ▼                                         │
│  ② TASK YAPISI — Zamanlama                                                    │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  Cyclic / Freewheeling / Event task tipleri                           │   │
│  │  Cycle time seçimi + CPU yük dengesi + Öncelik hiyerarşisi            │   │
│  │  Güvenlik (Prio:0) → Motion (Prio:1) → Kontrol → HMI → Arkaplan      │   │
│  └──────────────────────────────────┬────────────────────────────────────┘   │
│                                     │ Task'ların içini dolduran              │
│                                     │ kod mimarisi tasarlanır                │
│                                     ▼                                         │
│  ③ PROGRAMLAMA — Kod Mimarisi                                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  POU tipleri (PROGRAM / FUNCTION_BLOCK / FUNCTION)                    │   │
│  │  GVL tasarımı (IO / HMI / Params / Alarms / Config)                   │   │
│  │  Function Block state machine + kütüphane sistemi + hata yönetimi     │   │
│  │  Fiziksel dünya → GVL_IO → FB → PROGRAM → GVL_IO → Fiziksel dünya    │   │
│  └──────────────────────────────────┬────────────────────────────────────┘   │
│                                     │ Programlanan kontrolcü                 │
│                                     │ dış sistemlerle iletişim kurar         │
│                                     ▼                                         │
│  ④ NETWORKING — Dış Dünya                                                     │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  OPC UA  → SCADA/MES, güvenli, subscription (port 4840)               │   │
│  │  Modbus  → Evrensel, hızlı entegrasyon (port 502)                     │   │
│  │  TCP     → Özel protokol, SysSock state machine                       │   │
│  │  MQTT    → IoT/Bulut, event-driven, LWT (port 1883/8883)              │   │
│  └──────────────────────────────────┬────────────────────────────────────┘   │
│                                     │ Tüm bu bilgi, programatik              │
│                                     │ proje üretimine dönüştürülür           │
│                                     ▼                                         │
│  ⑤ PROJECT GENERATION — Otomatik Üretim                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  JSON Spec → Python 3 (PLCopen XML üret)                              │   │
│  │          → Script Engine / IronPython 2.7 (CODESYS headless)          │   │
│  │          → Template .project (device tree, library, task iskeleti)    │   │
│  │          → import_xml + textual_declaration.replace + compile()       │   │
│  │  Üretim sırası: DUT → GVL → FB → PROGRAM                             │   │
│  └──────────────────────────────────┬────────────────────────────────────┘   │
│                                     │ Üretilen ve çalışan proje              │
│                                     │ sorun çıktığında teşhis edilir         │
│                                     ▼                                         │
│  ⑥ DEBUGGING — Sorun Giderme                                                  │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  Log → Watch Window → Force → Breakpoint → Trace → Online Change      │   │
│  │  Task Monitor (Max Exec/Jitter eşikleri) + PLC Shell + Profiler       │   │
│  │  48 saatlik performans izlemesi → devreye alma onayı                  │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Altı Alanın Tek Cümlelik Özeti

| Alan | Tek Cümlelik Öz |
|---|---|
| **① Temeller** | Runtime donanımı PLC'ye dönüştürür; proje yapısı ve IEC dilleri bu runtime üzerine inşa edilir. |
| **② Task Yapısı** | Hangi kodun kaç milisaniyede, hangi öncelikte çalışacağını belirleyen zamanlama mimarisi. |
| **③ Programlama** | Function Block merkezli, GVL ile veri akışının kontrol edildiği, dört katmanlı hata yönetimini içeren kod mimarisi. |
| **④ Networking** | OPC UA, Modbus, TCP Socket ve MQTT ile kontrolcünün SCADA'dan buluta farklı katmanlarda iletişim kurması. |
| **⑤ Project Generation** | JSON spesifikasyonundan PLCopen XML ve Script Engine aracılığıyla derlenebilir CODESYS projesi otomatik olarak üretme. |
| **⑥ Debugging** | Log'dan başlayıp araç seçimiyle kaynağa inen, performans eşikleriyle desteklenen sistematik sorun giderme yöntemi. |

### Bütünsel Mental Model

Altı alanın birlikte nasıl çalıştığını anlamak için şu cümle yeterlidir:

> **Runtime** (①) kodu çalıştırmak için donanımı hazırlar. **Task yapısı** (②) o kodun ne zaman ve ne kadar sıklıkla çalışacağını belirler. **Programlama mimarisi** (③) o kodun içini doğru ve bakımı kolay biçimde doldurur. **Networking** (④) kontrolcünün dış dünyaya veri gönderip almasını sağlar. **Project Generation** (⑤) bu mimariyi tekrar eden projeler için programatik olarak üretir. **Debugging** (⑥) tüm bu katmanlarda ortaya çıkabilecek sorunları sistematik biçimde çözer.

Bu altı halka, bir CODESYS projesinin başından devreye almasına — ve sonrasına — kadar izlenen öğrenme ve uygulama yolculuğunu tanımlar.

---

## Hızlı Referans Tabloları

### A. "Ne Zaman Buraya Bak" — Navigasyon Tablosu

| Durum / Görev | Birincil Alan | Alt Sentez |
|---|---|---|
| CODESYS nedir, nasıl kurulur, hangi runtime? | Temeller | `fundamentals/_synthesis.md` |
| IEC dili seçimi: ST mi, LD mi, SFC mi? | Temeller | `fundamentals/_synthesis.md` |
| Task sayısı ve cycle time tasarımı | Task Yapısı | `task-structure/_synthesis.md` |
| EtherCAT için task mimarisi | Task Yapısı | `task-structure/_synthesis.md` |
| FB, PROGRAM, FUNCTION hangisini yazmalıyım? | Programlama | `programming/_synthesis.md` |
| GVL nasıl bölümlenmeli? RETAIN mi, PERSISTENT mi? | Programlama | `programming/_synthesis.md` |
| State machine ve hata çıkışı tasarımı | Programlama | `programming/_synthesis.md` |
| SCADA veya MES'e veri açma | Networking | `networking/_synthesis.md` |
| Modbus register haritası tasarımı | Networking | `networking/_synthesis.md` |
| Bulut veya IoT entegrasyonu | Networking | `networking/_synthesis.md` |
| JSON'dan CODESYS projesi üretme | Project Generation | `project-generation/_synthesis.md` |
| Script Engine API ve headless modu | Project Generation | `project-generation/_synthesis.md` |
| PLCopen XML ile POU üretimi | Project Generation | `project-generation/_synthesis.md` |
| Download hatası, watchdog alarmı, login sorunu | Debugging | `debugging/_synthesis.md` |
| Aralıklı arıza, Trace kurulumu | Debugging | `debugging/_synthesis.md` |
| Devreye alma performans testi (48 saat) | Debugging | `debugging/_synthesis.md` |

### B. Her Alandan 1-2 Kritik Kural

| Alan | Kritik Kural 1 | Kritik Kural 2 |
|---|---|---|
| **Temeller** | Task exec time / cycle time oranı **< %70** olmalı | Windows SoftPLC ile üretimde RT garantisi yoktur — Linux RT gerekir |
| **Task Yapısı** | PID ve ramp hesabı mutlaka **Cyclic** task'ta olmalı (Freewheeling'de değil) | Fieldbus (EtherCAT) cycle time ile task cycle time eşleşmelidir |
| **Programlama** | Her cihaz için ayrı **Function Block** — tüm mantığı PROGRAM'a yazmak anti-pattern | Kalibrasyon → **PERSISTENT**; üretim sayacı → **RETAIN** (karıştırma) |
| **Networking** | OPC UA'ya açılan değişken adları **"frozen"** sayılmalı — isim değişikliği SCADA bağlantısını kırar | TCP Socket client mutlaka **Freewheeling** task'a alınmalı (blocking connect task'ı dondurur) |
| **Project Generation** | POU üretim sırası zorunludur: **DUT → GVL → FB → PROGRAM** | Script Engine **IronPython 2.7** çalışır — f-string yok, `.format()` kullan |
| **Debugging** | Her sorun analizine **Log sekmesinden** başla (ekran özet, log tanı) | Task Monitor'da **Max Exec Time** izle — Average aldatıcıdır |

### C. Domain-Üstü Master Teşhis Tablosu

Saha belirtileri çoğu zaman tek alana sığmaz; aşağıdaki tablo belirtiyi doğru alana ve kök nedene haritalar (her alt sentezin teşhis tablolarının konsolidasyonu).

| Belirti | Birincil Katman | Kök Neden / İlke | Çözüm Yönü |
|---|---|---|---|
| Kod doğru ama jitter var | ① Temeller / ② Task | RT zinciri zayıf halka | BIOS C-state → isolcpus → RT-preempt |
| PID salınıyor | ② Task | Freewheeling değişken Δt | Cyclic'e al, sabit Δt |
| HMI yavaş / OPC UA kopuyor | ② Task | starvation | üst task exec düşür |
| Sayaç/setpoint kayboluyor | ③ Programlama | tek-yazar ihlali / race | tek yazar + double-buffer |
| Kalibrasyon download'da gitti | ① ③ | RETAIN vs PERSISTENT | kalibrasyon = PERSISTENT |
| Bozuk durumda makine kaçtı | ③ | ELSE yok | ELSE→eFault |
| 4 motor için 4 kopya kod | ③ | kapsülleme yok | FB + array of FB |
| SCADA değeri geç görüyor | ② ④ | sampling < cycle / bus cycle | sampling ≥ task cycle |
| Connect/publish sistemi dondurdu | ② ④ | bloke-I/O ana task'ta | Freewheeling task |
| Ağdaki herkes PLC'ye erişti | ④ | güvenlik yok/None | OPC UA AES / ağ izolasyonu |
| Gerçek-zaman bekledim, olmadı | ① ④ | raporlama ≠ kontrol | fieldbus (EtherCAT) |
| "40 hata: tip bulunamadı" | ⑤ | bağımlılık sırası | DUT→GVL→FB→PROGRAM |
| Derlendi ama sahada çalışmıyor | ⑤ ⑥ | "derlendi ≠ çalışıyor" | semantic check + simülasyon |
| Sporadik crash, farklı yer | ① ⑥ | dangling pointer (Online Change) | pointer her scan, saklama |
| Power-cycle eski davranış | ① ⑥ | bootapp | Create Boot App + power-cycle test |
| Aralıklı arıza, yakalanamıyor | ⑥ | araç yanlış (Watch kaçırır) | Trace + trigger + pre-trigger |
| Watchdog alarmı | ② ⑥ | exec > cycle / bloke / yük | Max Exec → kök neden |

### D. Uçtan Uca Uzman Senaryosu — Altı Alan Birlikte

**Görev**: OEM, 3 konveyörlü paketleme hattı projesini üretip devreye alacak; SCADA + bulut entegrasyonu istiyor.

```
① TEMELLER:   Hedef = Control Linux SL (RT-preempt) — Win SL üretim için değil.
              Determinizm zincirinin tabanı: RT kernel + isolcpus + BIOS C-state kapalı.

② TASK:       Task_Safety(P0,5ms) · Task_Control(P2,10ms) · Task_HMI(P5,100ms) ·
              Task_Background(Freewheel) — bloke-I/O (bulut) buraya. CPU < %70.

③ PROGRAMLAMA: FB_Conveyor ×3 (state machine + ELSE→eFault + xFault çıkışı).
              GVL katmanlı (IO/HMI/Params/Alarms), her birine tek yazar.
              PERSISTENT kalibrasyon, RETAIN üretim sayacı.

④ NETWORKING:  OPC UA (SCADA, fabrika-içi, AES+auth, sembol seti daraltılmış) +
              MQTT (bulut, Freewheel task, QoS1+idempotency, LWT). İkisi çakışmaz.

⑤ GENERATION:  spec.json → PLCopen XML (DUT+FB, CDATA) → Script Engine headless
              (temiz template kopyası → import DUT önce → GVL replace → library → compile).
              50 müşteri için aynı script, farklı spec.

⑥ DEBUGGING:   Devreye alma: Task Monitor 48h (gece+termal), Max Cycle < %70,
              cyclictest Max < 100µs. Aralıklı arıza → Trace. Create Boot App + power-cycle.
              Semantic check: her FB girişi bağlı mı (⑤ "derlendi≠çalışıyor").
```

Bu senaryo determinizm zincirinin uçtan uca kurulmasıdır: her alan bir öncekinin garantisini korur, en zayıf halka (RT yok / tek-yazar ihlali / güvenlik açık / sıra hatası / Max ihmali) tüm sistemi bozar.

---

## Öğrenme Yol Haritası

Aşağıdaki harita Temel→İleri ilerlemeyi gösterir. **Her belge ayrıca Uzman bölümleri içerir** (Edge Case'ler, Optimizasyon, Derin Teknik Detay) — bunlar saha deneyimiyle, ilerideki bir UZMAN aşamasında okunmalıdır: tasarım kararlarının "neden"i, sessiz hatalar, RT tuning, gözlemci etkisi, bellek layout. Aşağıdaki sıralama "ne öğrenilir"i; Uzman bölümleri "neden böyle ve nerede patlar"ı verir.

```
BAŞLANGIÇ (0–2 hafta) — Zemin Kurma
─────────────────────────────────────────────────────────────────
Alan: Temeller
  → Runtime nedir, SoftPLC nedir (01_runtime_architecture.md)
  → Device Tree ve proje iskeletini tanı (02_project_structure.md)
  → ST, LD, SFC dillerini dene (03_iec61131_languages.md)
  Pratik: Control Win kurulu, motor FB yaz, PLC_PRG'den çağır

Alan: Programlama (temel)
  → POU tipleri: PROGRAM / FUNCTION_BLOCK / FUNCTION (01_pou_types.md)
  → GVL neden ayrılır? GVL_IO, GVL_Alarms, GVL_Params (02_gvl_design.md)
  Pratik: FB_Motor state machine (Idle→Starting→Running→Fault)

─────────────────────────────────────────────────────────────────
TEMEL (2–4 hafta) — Mimari Anlayış
─────────────────────────────────────────────────────────────────
Alan: Task Yapısı
  → Cyclic, Freewheeling, Event task tipleri (01_task_types.md)
  → Cycle time seçimi: PID için 10–100ms, HMI için 50–200ms (02_cycle_time.md)
  → Öncelik yönetimi: Güvenlik Prio:0, motion Prio:1 (03_priority_management.md)
  Pratik: 3–5 task mimarisini bir proje için tasarla

Alan: Programlama (tam)
  → İyi Function Block: state machine, savunmacı giriş doğrulama (03_function_blocks.md)
  → Kütüphane sistemi: Standard.lib, sabit versiyon kuralı (04_libraries.md)
  → Dört katmanlı hata yönetimi: Watchdog, __TRY, FB doğrulama, alarm (05_error_handling.md)

─────────────────────────────────────────────────────────────────
ORTA (1–3 ay) — Dış Dünya ve Sorun Giderme
─────────────────────────────────────────────────────────────────
Alan: Networking
  → OPC UA sunucu: Symbol Configuration, SP17+ kullanıcı yönetimi (01_opcua_server.md)
  → Modbus TCP slave: Register haritası tasarımı, I/O mapping (02_modbus_slave.md)
  → TCP Socket: SysSock API, non-blocking state machine (03_tcp_socket.md)
  → MQTT client: Kütüphane seçimi, topic şeması, LWT (04_mqtt_client.md)
  Pratik: OPC UA + MQTT birlikte çalışan bir proje

Alan: Debugging
  → Hata kataloğu: 10 sık hata ve triage akışı (01_common_errors.md)
  → Debug araçları: Watch, Force, Breakpoint, Trace, Online Change (02_debugging_tools.md)
  → Performans analizi: Task Monitor eşikleri, cyclictest, 48h test (03_performance_analysis.md)
  Pratik: Trace ile aralıklı bir arıza yaka

─────────────────────────────────────────────────────────────────
İLERİ (3–6 ay) — Otomasyon ve Üretim Kalitesi
─────────────────────────────────────────────────────────────────
Alan: Project Generation
  → .project XML anatomisi (01_project_file_structure.md)
  → Script Engine API, headless modu (02_script_engine.md)
  → PLCopen XML formatı: POU, DUT, GVL üretimi (03_plcopen_xml.md)
  → Şablon sistemi ve üretim akışı (04_generation_templates.md)
  Pratik: JSON spesifikasyonundan tam derlenebilir proje üret

─────────────────────────────────────────────────────────────────
UZMAN (6 ay+) — Felsefe ve Kök Neden (her belgenin Uzman bölümleri)
─────────────────────────────────────────────────────────────────
  → Determinizm zincirini her katmanda görme: belirti→katman→kök neden
  → Tekrarlayan desenleri tanıma: tek-yazar, uçtan-uca zincir, çalışıyor≠doğru
  → Edge Case'ler: sessiz hatalar (bootapp, dangling pointer, cycle overrun, NaN, word tearing)
  → Optimizasyon: RT tuning (isolcpus/IRQ/C-state), bellek layout, gözlemci etkisi
  → Derin Teknik Detay: neden JIT yok, neden preemptive, neden lossy PLCopen, neden Max
  Pratik: bir saha tuhaflığını ilkeye indirgeyip kök nedeni dakikalarda bul

İleri Konular (bu bilgi tabanı kapsamı dışında):
  → OOP: Interface, Inheritance, Polymorphism (ST)
  → EtherCAT SoftMotion entegrasyonu
  → Güvenlik (SIL) gereksinimleri — CODESYS Safety ayrı ürün
  → Multicore task affinity
  → CI/CD pipeline ile otomatik test ve dağıtım
```

---

## Sık Yapılan Hatalar

Aşağıdaki hatalar tek bir alana özgü değildir; tüm domain genelinde tekrar eden kök nedenlerden kaynaklanır.

**1. Temeli atlamak — "Çalışıyor" yeterli saymak**
Runtime, task yapısı ve programlama mimarisini öğrenmeden yazan mühendisler, başlangıçta çalışan bir sistem kurar. Ama ölçek büyüyünce — yeni motor eklendi, ikinci müşteri geldi, EtherCAT istendi — temelsiz yapı çöker. Temeli sağlamlaştırmak için harcanan 2 hafta, ilerleyen aylarda haftalarca debug ve yeniden yazma sürecini önler.

**2. Tek task, tek GVL, tek büyük POU anti-pattern'i**
Tüm mantığı PLC_PRG'ye yazmak, tüm değişkenleri tek GVL'ye yığmak ve tek bir 10ms task kullanmak — başlangıçta kolay görünür. Proje büyüyünce bakımı imkânsız hale gelir. Her cihaz için FB, her sorumluluk için GVL, her zamanlama gereksinimi için ayrı task: bu üç kural baştan uygulanmalıdır.

**3. Geliştirme ortamı = üretim ortamı yanılgısı**
Control Win SL üzerinde her şey mükemmel çalışır. Gerçek donanımda (ARM, Linux RT) zamanlama, IRQ öncelikleri ve jitter farklı davranır. Üretim hedef platformunda erken ve uzun test yapılmazsa devreye alma günü sürprizler kaçınılmazdır.

**4. Networking'i güvenlikten bağımsız düşünmek**
OPC UA'yı "None" güvenlik politikasıyla açık bırakmak, MQTT'yi şifresiz internet üzerinden bağlamak, Modbus slave'i güvenlik duvarı arkasına almamak — bunlar test aşamasında kolaylık sağlar, üretimde güvenlik açığı yaratır. Protokol seçilirken güvenlik politikası da birlikte belirlenmeli; sonradan eklemek çok daha maliyetlidir.

**5. Otomatik üretimde bağımlılık sırasını gözetmemek**
Project Generation domain'ine girerken en sık karşılaşılan hata: FB'den önce DUT'ları import etmemek. "E_MotorState tipi bulunamadı" hatasıyla 40 derleme hatası çıkabilir. Zorunlu sıra unutulmamalıdır: **DUT → GVL → FB → PROGRAM**.

**6. Debugging'i yalnızca hata çıktığında yapmak**
Performans analizi (Task Monitor, Max Exec Time, jitter) yalnızca hata sonrası değil, her devreye almada proaktif olarak yapılmalıdır. "Çalışıyor" ile "sağlıklı çalışıyor" arasındaki fark, 48 saatlik izlemede Max değerlerinin eşik altında olmasıdır. Bu yapılmadan yapılan her devreye alma, gelecekte beklenmedik bir watchdog alarmı riski taşır.

**7. Kalıcılık stratejisini karıştırmak**
RETAIN ve PERSISTENT arasındaki farkı bilmemek somut üretim kaybına yol açar: Kalibrasyon RETAIN'de saklanırsa yeni firmware yüklendiğinde kaybolur; üretim partisi iptal edilmek zorunda kalınabilir. Kural nettir — kalibrasyon: PERSISTENT, üretim sayacı: RETAIN.

---

## Sentez Notları (Uzman)

**Sentez Notu 1 — Altı Alan, Tek Felsefe**
Uzmanlığın eşiği, altı alanı ayrı ayrı bilmek değil; hepsinin tek bir determinizm felsefesinin katmanları olduğunu görmektir. `fundamentals` felsefeyi kurar (JIT yok, I/O image, bellek görüntüsü); task-structure onu bütçeler, programming kapsüller, networking sınırını çizer (raporlama ≠ kontrol), generation tekrarlanabilir kılar, debugging görünür kılar. Bir saha tuhaflığını çözmek = bu zincirin hangi halkasının koptuğunu bulmak. Felsefe pusula, altı alan harita.

**Sentez Notu 2 — Tekrarlayan Desenler İlke Transferidir**
"Tek-yazar" GVL'de de (③), Modbus HR'da da (④), üretimde de (⑤) aynı kuraldır. "Belirti→katman→kök neden" her alt sentezin teşhis pusulasıdır. "Uçtan uca zincir" determinizmde, RT'de, güvenlikte tekrar eder. Uzman, yeni bir alanda bu desenleri tanır ve önceki alandan ilkeyi transfer eder — her alanı sıfırdan ezberlemez. Altı alandaki yüzlerce edge-case, aslında ~6 ilkenin farklı kılıklarıdır.

**Sentez Notu 3 — "Çalışıyor ≠ Doğru" Tüm Domaini Keser**
Dev ortamında çalışır ≠ üretimde çalışır (①). Ortalama iyi ≠ Max güvenli (⑥). Derlendi ≠ doğru çalışıyor (⑤). Sessiz cycle overrun, hata üretmeyen jitter, eksik FB bağlantısı — hepsi "çalışıyor görünüp" en kötü anda çöken sınıftır. Uzman, "çalışıyor"a güvenmez; en-kötü-durumu (Max, 48h test, semantic check, fiziksel fail-safe testi) doğrular. Bu, determinizm felsefesinin saha disiplinine dönüşmesidir.

**Sentez Notu 4 — Determinizm Uçtan Uca, Tek Katman Kurtarmaz**
Mükemmel ST kodu + RT-preempt kernel, ama BIOS C-state açıksa → jitter. Mükemmel FB, ama global'e yazıyorsa → race. Mükemmel OPC UA, ama task'ı bloke ediyorsa → watchdog. Mükemmel üretim, ama DUT sırası yanlışsa → 40 hata. Her katman bir öncekinin garantisini korumalı; bir katmanın ihmali tüm zinciri bozar. Bu yüzden uzman tek alana değil, zincirin bütününe bakar.

**Sentez Notu 5 — Bu Bilgi Tabanının Agent İçin Değeri**
Bu altı Uzman sentez + üst sentez, bir agent'ın CODESYS projesi üretip, devreye alıp, sorununu çözebilmesi için gereken bütünsel modeli verir. Agent "3 motorlu hat üret" dediğinde D-bölümündeki uçtan-uca senaryoyu izler: doğru runtime (①), doğru task (②), kapsüllü kod (③), güvenli iletişim (④), idempotent üretim (⑤), 48h doğrulama (⑥). Tek bir alanı atlayan agent, "çalışıyor görünen ama sahada çöken" proje üretir — bu sentezin önlemeye çalıştığı tam da budur.

---

## İlgili Konular

```
knowledge/codesys/                     ← Şu an buradasınız (domain üst sentezi)
│
├── fundamentals/_synthesis.md         → Runtime, proje yapısı, IEC dilleri
│   ├── 01_runtime_architecture.md
│   ├── 02_project_structure.md
│   └── 03_iec61131_languages.md
│
├── task-structure/_synthesis.md       → Task tipleri, cycle time, öncelik
│   ├── 01_task_types.md
│   ├── 02_cycle_time.md
│   └── 03_priority_management.md
│
├── programming/_synthesis.md          → POU, GVL, FB, kütüphane, hata yönetimi
│   ├── 01_pou_types.md
│   ├── 02_gvl_design.md
│   ├── 03_function_blocks.md
│   ├── 04_libraries.md
│   └── 05_error_handling.md
│
├── networking/_synthesis.md           → OPC UA, Modbus, TCP Socket, MQTT
│   ├── 01_opcua_server.md
│   ├── 02_modbus_slave.md
│   ├── 03_tcp_socket.md
│   └── 04_mqtt_client.md
│
├── project-generation/_synthesis.md   → Dosya yapısı, Script Engine, PLCopen XML, şablon
│   ├── 01_project_file_structure.md
│   ├── 02_script_engine.md
│   ├── 03_plcopen_xml.md
│   └── 04_generation_templates.md
│
└── debugging/_synthesis.md            → Hata kataloğu, debug araçları, performans analizi
    ├── 01_common_errors.md
    ├── 02_debugging_tools.md
    └── 03_performance_analysis.md

Bu domain dışı, bağlantılı konular:
  knowledge/standards/
  ├── safety_plc.md                    → SIL gereksinimleri — CODESYS Safety ayrı ürün
  └── opcua_overview.md                → OPC UA Information Model, NodeId detayı

  knowledge/networking/
  └── ethercat/                        → EtherCAT slave konfigürasyonu, SoftMotion

  knowledge/protocols/
  ├── opc-ua/                          → OPC UA client tarafı ve bilgi modeli
  └── modbus/                          → Modbus master ve diğer varyantlar
```
