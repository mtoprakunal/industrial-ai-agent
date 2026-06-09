---
KONU        : CODESYS Otomatik Proje Üretimi — Uzman Sentezi
KATEGORİ    : codesys
ALT_KATEGORI: project-generation
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/codesys/project-generation/01_project_file_structure.md"
    başlık: "CODESYS Proje Dosyası İç Yapısı (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/project-generation/02_script_engine.md"
    başlık: "CODESYS Script Engine (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/project-generation/03_plcopen_xml.md"
    başlık: "PLCopen XML (IEC 61131-10) Formatı (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/project-generation/04_generation_templates.md"
    başlık: "CODESYS Otomatik Proje Üretimi — Şablon Sistemi (Uzman)"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_project_file_structure.md"
    ilişki: detaylandırır
  - konu: "02_script_engine.md"
    ilişki: detaylandırır
  - konu: "03_plcopen_xml.md"
    ilişki: detaylandırır
  - konu: "04_generation_templates.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/programming/_synthesis.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Dört project-generation belgesinin Uzman bölümleri okunmuş olmalıdır."
  - "fundamentals (proje yapısı/GUID, ST), programming (FB/GVL/tek-yazar), task-structure (task yapısı) kavranmış olmalıdır."
  - "Python (IronPython 2.7 vs CPython 3 farkı) ve XML temelleri varsayılır."
ÇELİŞKİLER :
  - kaynak: "04 — Hibrit yaklaşım"
    konu: "Tam otomatik mi, hibrit şablon mu?"
    çözüm: "Sıfırdan tam otomatik (device tree dahil) kırılgandır. Hibrit: elle template (device tree/library/task) + otomatik GVL/POU/impl. Bu sentez hibridi temel alır."
  - kaynak: "01 — File-Based Storage"
    konu: "Klasik tek-XML mi, file-based mi?"
    çözüm: "File-based (2026 beta) Git-dostu ama tam desteklenmiyor. Üretim klasik .project'i hedeflemeli."
---

## Özün Ne

Bu klasör tek soruya yanıt verir: **Bir agent, JSON spesifikasyonundan nasıl geçerli, derlenebilir CODESYS projesi üretir?** Dört belge ayrı araç gibi görünür; uzman gözüyle iki ilke her şeyi yönetir:

1. **Üç-format üçgeni + Script Engine köprüsü** — Native `.project` (IDE-tam, taşınamaz, elle yazılamaz) / PLCopen XML (taşınabilir, lossy, dışarıda üretilir) / Script Engine (native'i obje-API ile yazan köprü). Üretim üçünü birleştirir: içeriği PLCopen ile dışarıda üret, native projeye Script Engine ile yerleştir.
2. **Üretilebilirlik = bilginin kaynağı** — Spec'ten türetilebilen (motor→FB) otomatik üretilir; platforma bağlı (typeGuid, device tree) template'te elle; mühendislik kararı (PID tuning, SIL) insan yazar. Hibrit yaklaşım bu üçü ayırır.

Bunlara iki disiplin eşlik eder: **bağımlılık sırası** (DUT→GVL→FB→PROGRAM) ve **katmanlı doğrulama** (spec→compile→semantic→simülasyon — çünkü "derlendi ≠ doğru çalışıyor").

Bu klasör agent için kritiktir: bu bilgi olmadan agent "bir motor FB'si oluştur" komutunu karşılayacak araçlara sahip değildir.

## Nasıl Çalışır

### Dört Belgenin Bağlantısı

```
01 DOSYA YAPISI ──── .project XML anatomisi (GUID grafiği); okuma için parse, yazma için DEĞİL
        │ Script Engine bu XML'i obje-API ile yazar
        ▼
02 SCRIPT ENGINE ─── IronPython 2.7; create_pou/gvl/dut, replace, import_xml, compile
        │ Script Engine PLCopen XML'i import eder
        ▼
03 PLCopen XML ───── taşınabilir IEC içeriği (POU/DUT/GVL); dışarıda Python 3 ile üretilir; lossy
        │ şablon sistemi üçünü bir araya getirir
        ▼
04 ŞABLONLAR ─────── JSON spec → üret → headless import+compile → .project; karar ağacı + hibrit
```

### Üç-Format Üçgeni (Birleştirici Çerçeve)

| Format | Ne | Taşınabilir? | Yazılır mı? | Üretimdeki Rolü |
|---|---|---|---|---|
| Native `.project` (01) | IDE tam durum, GUID grafiği | hayır | Script Engine ile (elle DEĞİL) | hedef artefakt |
| PLCopen XML (03) | IEC içeriği (lossy) | evet | Python 3 ile dışarıda | içerik üretimi |
| Script Engine (02) | obje-API köprüsü | — | native'i tutarlı yazar | yerleştirme + config |

**Akış:** PLCopen ile içeriği **dışarıda** üret (Script Engine'siz, çapraz-platform) → Script Engine ile native'e **tutarlı** yerleştir (import_xml + library + task) → compile ile doğrula.

### Üretilebilirlik Sınırı (Hibrit'in Kökü)

```
Spec'ten türetilebilen      → OTOMATİK üret (script)
  motor→FB, I/O listesi→GVL, alarm→özet, task atama
Platforma/repository'ye bağlı → TEMPLATE'te elle (Script Engine ile manuel)
  typeGuid, device tree, EtherCAT ESI/PDO
Mühendislik kararı           → İNSAN yazar (üretilemez)
  PID tuning, motion path, SIL mantığı
```

**Uzman içgörüsü:** "Ne kadar otomatik?" = "spec'ten deterministik türetilebilen kadar". Bu sınır project-generation'ın temel kararıdır; aşmaya çalışmak (device tree'yi script'le üretmek) kırılganlık getirir.

### "Agent İçin" Mental Model

> **Dosya Yapısı (01):** `.project` UTF-8 XML, ama semantik bir GUID grafiğidir — okuma için parse et, yazma için ASLA elle dokunma (GUID/referans bozulur), Script Engine kullan.

> **Script Engine (02):** IronPython 2.7 (f-string yok, `.format()` + `u"..."`). Dört temel API: create_pou/gvl/dut, textual_*.replace, import_xml, compile. Headless lisans ister. Idempotent yaz.

> **PLCopen XML (03):** İçeriği dışarıda Python 3 ile üret, import_xml ile ver. ST kayıpsız (CDATA), device tree/I/O mapping/library taşınmaz (lossy). Taşınabilirlik için ST kullan.

> **Şablon (04):** Template device tree'yi taşır (elle, sürüm-kilitli). Script GVL/FB/orkestrasyon üretir. Sıra: DUT→GVL→FB→PROGRAM. Doğrulama compile'da bitmez (semantic+sim).

## Hızlı Referans

### A. Script Engine Temel API (Belge 2)

| İşlem | API | Not |
|---|---|---|
| Proje aç | `projects.open(path)` | headless zorunlu (primary=None) |
| Bul | `proj.find("ad", recursive=True)` | liste; `[0]` öncesi kontrol |
| FB/PRG/FC | `app.create_pou("ad", PouType.X)` | varsayılan FunctionBlock |
| GVL/DUT | `app.create_gvl()` / `create_dut(.., DutType.X)` | — |
| Kod yaz | `pou.textual_declaration/implementation.replace(metin)` | sözdizimi doğrulamaz |
| PLCopen import | `app.import_xml(path)` | merge semantiği, DUT önce |
| Library | `lib_mgr.add_library(ad, sürüm, firma)` | — |
| Derle/Kaydet | `proj.compile()` (True/False) / `projects.save()` | compile=doğruluk ölçütü |

### B. PLCopen XML Yapı Taşları (Belge 3)

| Nesne | Element | Konum |
|---|---|---|
| FB/PRG/FC | `<pou pouType="...">` | `<pous>` |
| STRUCT/ENUM | `<dataType><structured>/<enumerated>` | `<types><dataTypes>` |
| GVL | `<globalVars>` | `<instances>...<resource>` |
| ST kodu | `<body><ST><xhtml><![CDATA[...]]>` | `<pou>` içinde (CDATA!) |
| Tip | `<BOOL/>`, `<string length="80"/>`, `<derived name="E_X"/>` | `<type>` içinde |

### C. Kritik Kurallar (Tüm Belgeler)

| Kural | Değer | Kaynak |
|---|---|---|
| Script Python | IronPython 2.7: f-string yok, `.format()`, `u"..."` | 02 |
| Headless | `--noUI --runscript=.. --scriptargs=..`; primary=None; lisans gerekir | 02 |
| BOM | `encoding='utf-8-sig'` (.project + PLCopen) | 01,03 |
| typeGuid | platform/sürüm-bağlı, hardcode etme; repository'den al | 01 |
| Üretim sırası | DUT → GVL → FB → PROGRAM | 04 |
| ST gövde | CDATA içinde (`<,>,&` için) | 03 |
| Device tree | template'te elle (script'le üretme) | 01,04 |
| Doğrulama | compile sözdizimi · semantic+sim mantık | 04 |
| Idempotency | temiz template kopyası VEYA get-or-create | 02,04 |
| PLCopen lossy | device tree/I/O map/library/OPC UA taşınmaz | 03 |

### D. Uzman Edge Case Konsolidasyonu

```
ALAN        EDGE CASE                       BELİRTİ/YANILGI          KORUMA
──────────────────────────────────────────────────────────────────────────────
Yapı(01)    elle XML düzenleme              proje açılmaz            Script Engine
Yapı(01)    GUID kopya-yapıştır             hayalet referans         export/import
Yapı(01)    Git merge .project              dosya bozulur            object-export/CODESYS Git
Yapı(01)    BOM                             parser patlar            utf-8-sig
Script(02)  Python 3 sözdizimi              SyntaxError              .format(), future
Script(02)  primary=None (headless)         AttributeError           projects.open()
Script(02)  replace sessiz başarısız        12 FB hatalı             compile() zorunlu
Script(02)  exception → yarım proje         "obje zaten var"          idempotent / temiz kopya
Script(02)  IronPython unicode              mojibake (ç,ş,ğ)         u"..." + codecs
PLCopen(03) CDATA'sız < >                   dosya bozulur            CDATA / XML lib
PLCopen(03) export-import lossy             config kaybolur          .projectarchive (tam)
PLCopen(03) şema sürümü                     sessiz alan atlama       xmllint + hizala
Şablon(04)  DUT sonra import                "tip bulunamadı" 40 hata DUT→GVL→FB→PROGRAM
Şablon(04)  derlendi ≠ çalışıyor            eksik FB bağlantısı      semantic check + sim
Şablon(04)  template drift                  4 farklı BaseProject      sürüm-kilitli template
Şablon(04)  idempotent değil                kirli çıktı birikir       temiz template kopyası
```

### E. PLCopen — Taşınanlar / Taşınmayanlar (Belge 3)

```
TAŞINIR:   POU içeriği (ST kayıpsız), değişken+init, DUT, GVL, Task config
TAŞINMAZ:  device tree, I/O mapping (AT %), library ref, OPC UA/MQTT, Symbol Config, viz
```

## Pratikte Nasıl Kullanılır

### Üretim Akışı (Üç Aşama)

```
HAZIRLIK (IDE, elle, bir kez — sürüm-kilitli template)
  device tree (hedef platform) · Standard+Util library · task iskeleti
  boş GVL'ler (GVL_IO/Params/Alarms) · boş PLC_PRG

HARİCİ ÜRETİM (Python 3, her proje)
  spec.json → validate (I/O çakışma, task ref) → generate_gvl_*/fb_* metinleri
  → PLCopen XML yaz (DUT+FB, CDATA, XML lib) → prg orkestrasyon → spec_final.json

SCRIPT ENGINE (IronPython 2.7, headless)
  template kopyala (temiz) → open → GVL replace → import_xml (DUT önce!)
  → PRG güncelle → library ekle → save → compile (False=dur) → close
```

### Devreye Alma / Üretim Kontrol Listesi (Uzman)

```
HAZIRLIK
□ Template sürüm-kilitli, tek kaynaktan (drift yok)
□ Device tree + library + task iskeleti template'te hazır
□ Üretim aracı klasik .project hedefliyor (file-based beta değil)

HARİCİ ÜRETİM
□ spec validate: I/O çakışma, task referansı, zorunlu alan
□ XML lib ile üret (string concat yok), ST gövde CDATA'da
□ encoding='utf-8-sig' her okuma, u"..." her metin

SCRIPT ENGINE
□ projects.open() (primary=None varsay), find sonrası [0] kontrol
□ idempotent: temiz template kopyası VEYA get-or-create
□ üretim sırası DUT→GVL→FB→PROGRAM
□ IronPython 2.7: .format(), future, codecs
□ compile() False → projeyi sakla-ma, hata raporla, iterasyona dön

DOĞRULAMA (compile yetmez)
□ semantic: her FB girişi bağlı mı, her PROGRAM task'ta mı, alarm özeti dolu mu
□ simülasyon: temel I/O akışı çalışıyor mu
□ spec.json'ı .project ile version control'e al
```

### Agent Üretim Karar Ağacı (Belge 4)

```
Motor>0?   → E_MotorState ENUM + FB_<ad> + GVL_IO(RunCmd/RunFB/FaultFB) + GVL_Params + GVL_Alarms
Analog>0?  → FB_AnalogSensor + GVL_IO(w<ad>_Raw)
Recipe?    → GVL_Recipes(RETAIN) + FB_RecipeManager
Modbus?    → GVL_Modbus + PRG_ModbusUpdate → Task_Background
OPC UA?    → Symbol Configuration (kısmen manuel)

Task: Safety→Task_Safety(P0,5ms) · Motor/kontrol→Task_Control(P2,10ms)
      HMI/OPCUA→Task_HMI(P5,100ms) · Modbus/log→Task_Background(Freewheel)
```

### Belirti → İlke → Kök Neden

```
Belirti                          İlke/Belge        Kök Neden / Çözüm
─────────────────────────────────────────────────────────────────────
Proje açılmıyor                  Yapı/01           elle XML düzenleme → Script Engine
"40 hata: tip bulunamadı"        Sıra/04           DUT sonra import → DUT önce
Script "başarılı" ama FB hatalı  Doğrulama/02      replace sessiz → compile() zorunlu
Derlendi ama sahada çalışmıyor   Doğrulama/04      semantic eksik → bağlantı kontrolü + sim
Yeniden çalıştırma kirli         Idempotency/02,04 yarım durum → temiz template kopyası
Config export-import'ta kayıp    Lossy/03          PLCopen lossy → .projectarchive
typeGuid çalışmıyor              Platform/01       sürüm-bağlı → repository'den dinamik
Türkçe karakter bozuk            IronPython/02     str/unicode → u"..." + codecs
4 farklı template                Drift/04          → tek kaynak, sürüm-kilit
```

## Sık Yapılan Hatalar

### Başlangıç Hataları (4)

1. **IronPython 2.7'de Python 3 sözdizimi** (02) — f-string/walrus; `.format()`, future.
2. **primary None kontrolü yok** (02) — headless çöker; `projects.open()`.
3. **DUT'u FB'den sonra import** (04) — "tip bulunamadı"; sıra DUT→GVL→FB→PROGRAM.
4. **Template'de device tree yok** (04) — Application bulunamaz; template hazır olmalı.

### Uzman Hataları (5)

1. **"Derlendi = doğru"** (04) — eksik FB bağlantısı derlenir; semantic check + simülasyon.
2. **replace sessiz başarısızı** (02) — her tur compile() ile doğrula; script çıktısı yetmez.
3. **Idempotent olmayan üretim** (02,04) — yarım/kirli durum birikir; temiz template kopyası.
4. **PLCopen'ı tam yedek sanmak** (03) — lossy, config kaybolur; .projectarchive tam yedek.
5. **Template drift** (04) — çok kopya, hangisi doğru bilinmez; sürüm-kilitli tek kaynak.

## Ne Zaman ...

```
Otomatik üretim değerli:  5+ benzer parametreli proje (OEM) · sık değişen I/O · CI/CD
Manuel daha iyi:          tek proje/nadir değişiklik · PID/motion (şablona girmez) · SIL

Hangi araç:
  POU/GVL/DUT oluştur/güncelle    → Script Engine
  device tree config              → template (elle)
  içeriği CODESYS dışında üret    → PLCopen XML + Python 3
  projeyi analiz/raporla          → .project XML parse (lisanssız)
  çapraz-marka POU (ABB→CODESYS)  → PLCopen import
  Git'te içerik takibi            → PLCopen export
  tekrarlayan CI                  → headless (--noUI, lisans)

Hibrit (otomatik / manuel):
  otomatik: GVL içerik, standart FB, I/O atama, PRG orkestrasyon, alarm özeti, library listesi
  manuel:   device tree, task yapısı, PID tuning, motion path, güvenlik mantığı, müşteri-özel iş
```

## Gerçek Proje Notları

**Sentez Notu 1 — Üç Format Rakip Değil, Ortak**  
En sık soru: "PLCopen XML mi, Script Engine mi?" Yanlış soru — ikisi üçgenin iki köşesi (native üçüncü). PLCopen içeriği dışarıda üretir (taşınabilir, lisanssız, çapraz-platform), Script Engine native'e tutarlı yerleştirir (import + library + config). En güçlü üretim her zaman üçünün kombinasyonudur (04 hibrit).

**Sentez Notu 2 — Üretilebilirlik Bilginin Kaynağına Bağlıdır**  
"Ne kadar otomatik?" sorusu aslında "bu bilgi nereden geliyor?" sorusudur. Spec'ten türetilebilen otomatik üretilir; platforma bağlı (typeGuid/device tree) template'te elle; mühendislik kararı (PID/SIL) insan yazar. Bu sınırı zorlamak (device tree'yi script'le üretmek) kırılganlık getirir. Hibrit yaklaşım üç kaynağı doğru katmana yerleştirir.

**Sentez Notu 3 — "Derlendi" En Pahalı Yanılgı**  
Derleme sözdizimini doğrular, mantığı değil. Eksik FB bağlantısı, yanlış I/O adresi, eksik alarm özeti, task'a atanmamış PROGRAM — hepsi derlenir ama sahada çöker (Not 5). Üretim doğrulaması dört katmandır: spec → compile → semantic check → simülasyon. "Derlendi = teslim edilebilir" sanmak, sahada motor geri bildirimi işlenmeyen projeler doğurur.

**Sentez Notu 4 — Bağımlılık Sırası ve Idempotency: Üretimin İki Disiplini**  
"40 hata" dersi tek bir kuralı öğretti: DUT→GVL→FB→PROGRAM, çünkü her obje bir öncekine bağımlıdır (FB, E_MotorState'i kullanır). Idempotency ise güvenilirliğin temelidir: her üretim temiz template kopyasından başlamalı (yarım-durum birikimini imkânsız kılar). İkisi birlikte, üretimi deterministik ve tekrarlanabilir yapar — model-driven development'in PLC karşılığının çekirdeği.

**Sentez Notu 5 — Agent'ın Bu Klasörü Kullanma Şekli**  
Agent "3 motorlu konveyör hattı üret" komutunu aldığında: (1) spec JSON üret (motor/I/O/task), (2) DUT XML'leri (E_MotorState, ST_MotorDiag) PLCopen'da yaz, (3) her motor için FB XML, (4) GVL içerik metinleri, (5) PRG orkestrasyon, (6) Script Engine'e pas et (DUT önce!), (7) compile başarısızsa hata oku → ilgili bölümü yeniden üret → tekrar dene (ort. 2-3 iterasyon). Bu döngü, üretim kalitesini kademeli artırır. Bu klasörün bilgisi olmadan agent bu akışı kuramaz.

## İlgili Konular

```
knowledge/codesys/project-generation/   ← Şu an buradasınız (Uzman seviye)
├── 01_project_file_structure.md  (Uzman) → .project XML anatomisi, parse, GUID grafiği
├── 02_script_engine.md           (Uzman) → IronPython API, headless, idempotency
├── 03_plcopen_xml.md             (Uzman) → POU/DUT/GVL XML, lossy transfer, CDATA
├── 04_generation_templates.md    (Uzman) → üretim akışı, hibrit, doğrulama katmanları
└── _synthesis.md (bu belge)

Önkoşul / üretilen içeriğin detayı:
knowledge/codesys/fundamentals/   → proje yapısı/GUID, ST'nin üretilebilirliği, determinizm
knowledge/codesys/programming/    → üretilecek FB/GVL/DUT tasarımı, tek-yazar, hata yönetimi
knowledge/codesys/task-structure/ → üretilen task yapısı, öncelik, cycle time
knowledge/codesys/networking/     → üretilen Modbus/OPC UA config (GVL_Modbus, Symbol Cfg)

Araçlar:
  Python xml.etree.ElementTree / lxml · xmllint/xmlstarlet · openpyxl (Excel→spec)
  CODESYS Forge Scripting · GitHub tkucic/codesys_workflow_automation
```
