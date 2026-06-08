---
KONU        : CODESYS Domaini — Üst Sentez
KATEGORİ    : codesys
ALT_KATEGORI: codesys
SEVİYE      : Temel
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/codesys/fundamentals/_synthesis.md"
    başlık: "CODESYS Temeller Sentezi"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/task-structure/_synthesis.md"
    başlık: "CODESYS Task Yapısı Sentezi"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/_synthesis.md"
    başlık: "CODESYS Programlama Mimarisi Sentezi"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/networking/_synthesis.md"
    başlık: "CODESYS Networking Sentezi"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/project-generation/_synthesis.md"
    başlık: "CODESYS Otomatik Proje Üretimi Sentezi"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/debugging/_synthesis.md"
    başlık: "CODESYS Debugging Sentezi"
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
  - "Bu belge, 6 alt sentezin tamamını okuduktan sonra bütünsel bakış için kullanılmak üzere tasarlanmıştır."
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

CODESYS, herhangi bir donanımı IEC 61131-3 uyumlu bir PLC'ye dönüştüren SoftPLC ekosistemidir. Tek bir ürün değil; runtime katmanı, geliştirme ortamı, protokol kütüphaneleri ve otomasyon araçlarından oluşan bütünleşik bir platformdur.

Bu bilgi tabanı, CODESYS'i altı birbirine bağlı alan üzerinden haritalıyor: **Temeller** platformun ne olduğunu, **Task Yapısı** zamanlamanın nasıl kurulduğunu, **Programlama** kod mimarisinin nasıl tasarlandığını, **Networking** dış dünyayla nasıl iletişim kurulduğunu, **Project Generation** projenin nasıl programatik olarak üretildiğini, **Debugging** ise sorunların nasıl teşhis ve giderildiğini açıklar.

Bu altı alan bir araya geldiğinde oluşan bütün şudur: **"IEC kodunu çalıştıran güvenilir, bakımı kolay, dış dünyaya açık, otomatik üretilebilir ve sorunları çözülebilir bir endüstriyel kontrolcü."**

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

---

## Öğrenme Yol Haritası

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
