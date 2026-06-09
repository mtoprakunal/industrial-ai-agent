---
KONU        : CODESYS Programlama Mimarisi — Uzman Sentezi
KATEGORİ    : codesys
ALT_KATEGORI: programming
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/codesys/programming/01_pou_types.md"
    başlık: "CODESYS POU Tipleri (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/02_gvl_design.md"
    başlık: "CODESYS GVL Tasarımı (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/03_function_blocks.md"
    başlık: "İyi Bir Function Block Nasıl Yazılır (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/04_libraries.md"
    başlık: "CODESYS Kütüphane Sistemi (Uzman)"
    güvenilirlik: deneyimsel
  - url: "knowledge/codesys/programming/05_error_handling.md"
    başlık: "CODESYS'te Hata Yönetimi (Uzman)"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_pou_types.md"
    ilişki: detaylandırır
  - konu: "02_gvl_design.md"
    ilişki: detaylandırır
  - konu: "03_function_blocks.md"
    ilişki: detaylandırır
  - konu: "04_libraries.md"
    ilişki: detaylandırır
  - konu: "05_error_handling.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "Beş programlama belgesinin Uzman bölümleri okunmuş olmalıdır."
  - "fundamentals/_synthesis.md (determinizm felsefesi) ve task-structure/_synthesis.md kavranmış olmalıdır."
  - "Saha kodlama, devreye alma ve bakım deneyimi varsayılır."
ÇELİŞKİLER :
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez belgesi yeni çelişki içermez; kaynak belgelere atıflar yapar."
---

## Özün Ne

Beş programlama kararı (POU tipi, GVL, FB tasarımı, kütüphane, hata yönetimi) ayrı konular gibi görünür; uzman gözüyle bunlar **üç değişmez ilkenin** uygulamalarıdır:

1. **Tek yönlü veri akışı** — Fiziksel I/O → GVL → FB → PROGRAM → GVL → I/O. Her şey bu akışı korumak içindir.
2. **Sahipli kapsülleme** — Her veri parçasının tek bir yazarı vardır (FB yalnızca output'una, her GVL'ye tek task). Bu, preemptive scheduler'da race'i ve çok-yazar kaosunu önler.
3. **Katmanlı fail-safe** — Hata "yakalanıp devam edilen" değil, "önlenip oluşursa güvenli duruma kaçılan" bir şeydir; dört dik katman (savunmacı kod, __TRY, watchdog, alarm+safety task) farklı başarısızlık ölçeklerini kapsar.

Bu üç ilke `fundamentals/_synthesis`'teki determinizm felsefesinin programlama-katmanı ifadesidir. Uzmanlık, beş kararı tek tek "doğru" yapmak değil; bir saha belirtisini (kopyalanamayan kod, race, yapışık çıkış, kaybolan retain, alarm seli) hangi ilkenin ihlal edildiğine haritalayabilmektir.

## Nasıl Çalışır

### Beş Belgenin Zihin Haritası

```
01 POU TİPLERİ ──────── Kodun yapı taşı (PROGRAM/FB/FUNCTION = bellek yaşam döngüsü)
        │ POU'lar veri için GVL'ye başvurur
        ▼
02 GVL TASARIMI ─────── Paylaşımlı durumun sahipli katmanları (IO/HMI/Params/Alarms/Config)
        │ FB GVL'yi okur; çıkışını PROGRAM aracılığıyla GVL'ye yazar
        ▼
03 FUNCTION BLOCK ───── Cihaz mantığının kapsüllenmesi (state machine + hata çıkışı)
        │ Olgun FB'ler kütüphaneye taşınır
        ▼
04 KÜTÜPHANE ────────── Tekrar kullanım altyapısı (sürüm-sabit, namespace, IP)
        │ FB'ler hata raporlar; proje alarm mimarisini besler
        ▼
05 HATA YÖNETİMİ ────── Dört katmanlı fail-safe ağı
```

### Üç İlke ↔ Beş Karar Matrisi

| İlke | 01 POU | 02 GVL | 03 FB | 04 Lib | 05 Hata |
|---|---|---|---|---|---|
| **Tek yönlü akış** | PROGRAM orkestra eder | I/O→GVL→… katmanı | FB output→PROGRAM yazar | lib global yazmaz | alarm akışı tek yön |
| **Sahipli kapsülleme** | FB instance kendi belleği | GVL'ye tek yazar | FB sadece output'una yazar | lib instance state | safety task tek sahip |
| **Katmanlı fail-safe** | ELSE→eFault | GVL_Alarms katmanı | savunmacı giriş + ELSE | sürüm kilidi | 4 dik katman |

**Uzman içgörüsü:** "Kod doğru ama bakım/saha sorunu var" → ihlal edilen ilkeyi bul. Kopyalanan kod → kapsülleme (PROGRAM yerine FB). Race/yapışık çıkış → tek-yazar ihlali. Kaybolan değer → kalıcılık+layout. Alarm seli → fail-safe katmanı eksik/histerezissiz.

### Bütünsel Akış: Bir CODESYS Projesi Nasıl Nefes Alır

> Fiziksel dünya → **GVL_IO** (mapping) → **FB** (okur, durum işler) → **PROGRAM** (FB çağırır, çıkışı GVL'ye yazar) → **GVL_IO** → fiziksel dünya. Her adımda hata → **GVL_Alarms** + **Task_Safety**. Olgun FB → **Kütüphane**.

Karışıklık hep bu akışın dışına çıkınca başlar: FB'nin global'e yazması, PROGRAM'ın çok yerden çağrılması, GVL_IO'ya iş-mantığı değişkeni, kütüphanenin global tutması — her biri tek-yönlü akışı kırar.

## Hızlı Referans

### A. POU Türü (Belge 1)

| Soru | Türü | Neden (bellek yaşam döngüsü) |
|---|---|---|
| Çoklu kopya? | **FB** | instance-başına statik bellek |
| Task'tan tek kopya? | **PROGRAM** | tekil global singleton |
| Saf hesap, durumsuz? | **FUNCTION** | stack — reentrant, çağrıda doğar/ölür |
| Timer/sayaç/OOP? | **FB** | kalıcı instance state + method/THIS^ |

### B. GVL Katmanı (Belge 2)

| GVL | İçerik | Tek Yazar | Kalıcılık |
|---|---|---|---|
| GVL_IO | AT% fiziksel sinyal (tercihen mapping) | Task_Control | Standart |
| GVL_HMI | operatör komutu | Task_HMI | Standart |
| GVL_Params | proses parametresi | Task_HMI (doğrulamalı) | Std/RETAIN |
| GVL_Alarms | alarm bayrağı | Task_Control/Safety | Standart |
| GVL_Config | kalibrasyon, kimlik | mühendis | **PERSISTENT** |

### C. FB Arayüz Standardı (Belge 3)

```
VAR_OUTPUT minimumu: xFault, eFaultCode:DWORD, sFaultMsg:STRING, eState
Kural: her scan koşulsuz çağır · önce çağır sonra oku · CASE'de ELSE→eFault
       output salt-okunur · büyük veri VAR_IN_OUT · durumlu blok FB body'de
```

### D. Kütüphane (Belge 4)

```
Sürüm: ASLA "newest"/* → sabit (3.5.17.0) · MAJOR=kırma, MINOR/PATCH=uyumlu
Namespace: her lib'e benzersiz · global durum lib'de YASAK
Dağıtım: .projectarchive (bağımlılık paketler) · compiled=IP+compiler kilidi
Kütüphaneleştir: 3+ projede aynı FB
```

### E. Hata Katmanları (Belge 5)

| Katman | Ölçek | Platform | Zorunlu |
|---|---|---|---|
| Savunmacı kod | mantık (kötü giriş) | tüm | her FB |
| __TRY/__CATCH | bellek (null deref) | yalnız 32-bit | pointer işlemde |
| Watchdog | zaman (takılma) | tüm | her task |
| Alarm + Safety task | sistem (bildirim+güvenli durum) | tüm | her üretim |

### F. İsimlendirme

```
x=BOOL n=INT w=WORD dw=DWORD r=REAL s=STRING t=TIME dt=DT a=ARRAY st=STRUCT e=ENUM
GVL prefix (qualified_only): GVL_IO.x / GVL_HMI.x / GVL_Params.r / GVL_Alarms.x
Postfix: ...Cmd(yaz) ...Feedback(oku) ...Setpoint  ..._C/_Bar/_Pct
```

### Uzman Edge Case Konsolidasyonu

```
İLKE/ALAN   EDGE CASE                        BELİRTİ                  KORUMA
──────────────────────────────────────────────────────────────────────────────
POU(01)     VAR_STAT Function'da POU-tekil    Paylaşılan tek sayaç     Per-instance→FB
POU(01)     Function'da recursion             Stack overflow crash     İteratif çöz
POU(01)     output'a dışarıdan yazma          FB bir sonraki scan ezer Salt-okunur muamele
GVL(02)     RETAIN/PERSIST sıra değişti        Sessiz değer bozulması   Yalnızca sona ekle
GVL(02)     PERSISTENT FB içinde              Kaydedilmez (sessiz)     PersistentVars listesi
GVL(02)     çok-word paylaşım (LREAL/STRUCT)  Frankenstein değer       double-buffer/mutex
GVL(02)     AT% topoloji kayması              Yanlış çıkış aktif        Sembolik mapping
FB(03)      koşullu FB çağrısı                Timer donar              bEnabled ile çağır
FB(03)      çıkışı çağrıdan önce oku          1 scan gecikme           Önce çağır sonra oku
FB(03)      ELSE yok + bozuk eState           Tanımsız çıkış           ELSE→eFault
FB(03)      REFERENCE TO atanmamış             Deref crash              __ISVALIDREF kontrol
Lib(04)     iki lib farklı alt-sürüm ister    Çözülemez derleme hatası placeholder/container
Lib(04)     compiled + farklı compiler        "incompatible version"   sözleşmede sürüm
Hata(05)    REAL /0 → NaN                      Sessiz yayılır, < hep F  __FINITE/açık kontrol
Hata(05)    alarm chattering                  Log seli, gerçek kaybolur histerezis+debounce
Hata(05)    __TRY 64-bit                       Derlenir, çalışmaz       savunmacı programlama
Hata(05)    watchdog→çıkış                     Otomatik 0 DEĞİL          fieldbus fail-safe+test
```

## Pratikte Nasıl Kullanılır

### Yeni Makine Projesi — Mimari Kontrol Listesi (Uzman)

```
BAŞLANGIÇ
□ Cihaz türü başına bir FB (kopyalama yok)
□ GVL katmanla: IO/HMI/Params/Alarms/Config/Comm — her birine tek yazar
□ Task başına bir PROGRAM (orkestra)
□ RETAIN=üretim sayacı/aktif reçete · PERSISTENT=kalibrasyon/kimlik
□ RETAIN/PERSIST listesi: yalnızca sona ekleme kuralı belgelendi
□ qualified_only her GVL'de açık · her lib'e namespace
□ Symbol Configuration daraltıldı (sadece dışa açılan GVL)

KODLAMA
□ DUT: E_State enum + ST_Diag/ST_AlarmRecord struct
□ FB'ler: state machine + ELSE→eFault + xFault/eFaultCode/sFaultMsg çıkışları
□ FB'ler output-only yazar; büyük veri VAR_IN_OUT
□ Durumlu bloklar FB body'de (method yerel VAR'da değil)
□ PRG_Control: FB çağır → çıkış GVL_IO'ya → alarm GVL_Alarms'a
□ PRG_Safety (Prio:0): xAnyCriticalAlarm → kritik çıkışları kapat
□ Analog alarmlara histerezis + debounce

HATA / FAIL-SAFE
□ Her task watchdog açık (cycle×3-5, sensitivity 2-3)
□ 64-bit ise __TRY yok → null/index savunmacı kontrol
□ Çıkış fail-safe fieldbus slave'de yapılandırıldı + FİZİKSEL test
□ Exception handler minimum/non-blocking
□ Hata kodu DWORD bit-mask (string HMI/SCADA'da çözülür)

KÜTÜPHANELEŞTİRME
□ 3+ projede FB → library, sürüm-sabit, .projectarchive dağıtım
```

### Belirti → İlke/Belge → Kök Neden

```
Belirti                              İlke/Belge   Kök Neden / Çözüm
─────────────────────────────────────────────────────────────────────
4 motor için 4 kopya kod             Kapsülleme/01 PROGRAM→FB + array of FB
Sayaç bazen sıfırlanıyor             Tek-yazar/02  iki task yazıyor → tek yazar
Kalibrasyon download'da gitti        Kalıcılık/02  RETAIN→PERSISTENT
Persistent değerler "kaymış"         Layout/02     liste sırası değişti→sona ekle
Çıkış 5 instance'ta yapışık          Tek-yazar/03  FB global'e yazıyor→output-only
Timer bazen donuyor                  Çağrı/03      koşullu çağrı→bEnabled
Bozuk durumda makine kaçtı           Fail-safe/03  ELSE yok→ELSE→eFault
Lib güncellemesi her şeyi kırdı      Sürüm/04      newest→sabit sürüm
3. taraf lib aynı isim çakıştı       Namespace/02,04 qualified_only+namespace
8 saat süren arıza araması           Bildirim/05   kötü alarm mesajı→ne/nerede/ne yap
Watchdog sonrası motor durmadı       Fail-safe/05  fieldbus fail-safe + safety task
Alarm log 10 dk'da doldu             Histerezis/05 deadband + debounce
PID çıkışı NaN, limit yakalamadı     Sayısal/05    __FINITE kontrol + /0 önleme
```

### Performans Optimizasyon Sıralaması (Beş Belgeden)

```
1. Büyük veri VAR_IN_OUT (kopya elimine)        02,03 — ölçülebilir CPU
2. Array of FB + FOR (tekrar→döngü)             01,03 — kod+bakım
3. STRUCT/GVL alan sıralama (padding↓)          02 — bellek, retain bütçesi
4. Hata kodu bit-mask (string CONCAT yok)       05 — sıcak task CPU
5. Alarm değerlendirme orta task'ta (1ms değil) 05 — sıcak task yükü
6. Function inline (sıcak döngüde çağrı yükü)   01 — çağrı overhead
7. Symbol set daralt (bootapp/sembolik erişim)  02 — boyut+hız
8. Kullanılmayan lib çıkar (bootapp)            04 — bellek
```

## Örnekler

### Uçtan Uca: 2 Motor + 1 Isıtıcı + Sıcaklık Sensörü (Uzman)

```
POU (01): FB_Motor×2, FB_TemperatureCtrl×1, FB_AnalogSensor×1, FC_Scale,
          PRG_ProcessControl (Task_Control), PRG_Safety (Task_Safety Prio:0)

GVL (02): GVL_IO (mapping, AT% değil) · GVL_Params · GVL_Alarms ·
          GVL_Config PERSISTENT (rTemp_CalOffset)

FB (03):  FB_Motor: input(Start/Stop/Reset/tDelay) output(xRunOutput/xFault/eState/sMsg)
          CASE eIdle→eStarting→eRunning→eStopping/eFault · ELSE→eFault

Lib (04): Standard(TON,R_TRIG,CTU) + MyMachineLib 1.2.0.0 (sabit sürüm)

Hata(05): Task_Control wd 30ms×3 · Task_Safety wd 1ms×5
          Sıcaklık alarmı: histerezis (set 90°C, reset 87°C) + 2s debounce

PRG_ProcessControl:
    fbMotor1(xStartCmd:=GVL_HMI.xConv1_Start, bEnabled:=xEnable1);  (* koşulsuz *)
    GVL_IO.xConv1_Out             := fbMotor1.xRunOutput;          (* output-only *)
    GVL_Alarms.xAlarm_Conv1_Fault := fbMotor1.xFault;
    GVL_Alarms.xAnyCriticalAlarm  := GVL_Alarms.xAlarm_Conv1_Fault OR GVL_Alarms.xAlarm_Temp_High;

PRG_Safety:  (* bağımsız watchdog, fieldbus fail-safe ile birlikte *)
    IF GVL_Alarms.xAnyCriticalAlarm THEN
        GVL_IO.xConv1_Out := FALSE; GVL_IO.xConv2_Out := FALSE; GVL_IO.xHeater_Out := FALSE;
    END_IF
```

## Sık Yapılan Hatalar

### Başlangıç Hataları (5)

1. **Her şeyi PROGRAM'a** (01) — kopyalama; FB kullan.
2. **Tek büyük GVL** (02) — kategorisiz; katmanla.
3. **Function'a timer** (01) — sıfırlanır; FB kullan.
4. **Watchdog kapalı** (05) — donma; her task'ta aç.
5. **RETAIN'de kalibrasyon** (02) — download'da gider; PERSISTENT.

### Uzman Hataları (5)

1. **FB global'e yazar / çok-yazar** (02,03) — race, yapışık çıkış; output-only + tek yazar.
2. **RETAIN/PERSIST sıra değiştirme** (02) — sessiz veri bozulması; yalnızca sona ekle.
3. **"newest" lib + compiler kilidi körlüğü** (04) — sürpriz davranış / uyumsuzluk; sabit sürüm + sözleşme.
4. **64-bit'te __TRY + NaN/histerezissiz alarm** (05) — çalışmayan koruma, alarm seli; savunmacı kod + histerezis.
5. **"Watchdog/STOP = güvenli" varsaymak** (05) — çıkış fail-safe otomatik değil; fieldbus fail-safe + safety task + fiziksel test.

## Ne Zaman Tercih Edilmeli / Edilmemeli

```
FB yerine PROGRAM?     → tek kopya, task orkestratörü, kopyalanmayacak
PROGRAM yerine FB?     → çoklu kopya VEYA cihaz yaşam döngüsü VEYA OOP
FUNCTION?              → durumsuz saf hesap (timer/sayaç YOKsa)
Kütüphane oluştur?     → 3+ projede aynı FB / dağıtım / IP
__TRY/__CATCH?         → yalnız 32-bit, pointer/external lib
PERSISTENT?            → güç+download'a dayanmalı (kalibrasyon/kimlik)
RETAIN?                → yalnız güç kesilmesine (sayaç/aktif reçete)
Ayrı Task_Safety?      → kritik çıkış başka task'ın wd'sinden etkilenmemeli
```

Yetersiz kalınca: OOP derinliği → advanced/oop_codesys · birim test → advanced/unit_testing · compiled lib → advanced/compiled_library_guide · SIL → standards/safety_plc · profiling → debugging.

## Gerçek Proje Notları

**Sentez Notu 1 — Üç İlke, Beş Karar**  
Uzmanlığın eşiği: POU/GVL/FB/lib/hata kararlarını ayrı ayrı ezberlemek değil, üçünü tek yönlü akış + sahipli kapsülleme + katmanlı fail-safe ilkelerinden türetebilmek. Her saha tuhaflığı bu üçten birinin ihlalidir; ilke pusula, edge case harita.

**Sentez Notu 2 — Beş Kararın Birikimli Değeri**  
PROGRAM→FB ayrımı kopyalamayı, GVL katmanlama race'i, FB tasarımı test edilemezliği, kütüphane sıfırdan-başlamayı, hata yönetimi 8 saatlik debug'ı ortadan kaldırır. Beşi bir zincir; en zayıf halka projeyi belirler — biri eksikse diğer dördü telafi edemez.

**Sentez Notu 3 — Tek-Yazar Kuralı Her Katmanda Tekrar Eder**  
"FB sadece output'una yazar" (03), "her GVL'ye tek task yazar" (02), "PROGRAM tek noktadan çağrılır" (01), "kütüphane global tutmaz" (04) — hepsi aynı kuralın farklı katmanlardaki ifadesi: paylaşımlı durumun tek sahibi olmalı. Bu, preemptive scheduler'da (task-structure/03) race condition'ı önlemenin programlama-katmanı stratejisidir.

**Sentez Notu 4 — Fail-Safe "Yakala-Devam Et" Değil, "Önle-Güvenli Duruma Kaç"tır**  
CODESYS'te genel try/catch'in olmaması (ve 64-bit'te __TRY yokluğu) bir eksiklik değil, felsefe: determinizm ve sertifikasyon, exception unwinding'in öngörülemez sürelerini kabul etmez. Bu yüzden hata stratejisi savunmacı önleme + katmanlı fail-safe'tir. Dört katman dik (orthogonal) olduğu için biri eksik olunca o ölçekteki başarısızlık tamamen korumasız kalır.

**Sentez Notu 5 — Mimari Başta 2 Saat, Sonra Aylar**  
GVL katmanlama 2 saat, sonradan bölmek 3 gün + %60 bakım yükü (sahada görülmüş). FB mimarisi başta kurulursa bir bug fix tek noktadan yayılır; kurulmazsa yıllar içinde 20 farklı "FB_Motor" versiyonu doğar. PERSISTENT 5 dakikalık karar, eksikliği bir üretim partisine mal olur. Programlama mimarisinde "önce çalıştır sonra düzelt" işlemez — çünkü kötü mimari aylarca "çalışıyor" görünür, en kötü anda çöker.

## İlgili Konular

```
knowledge/codesys/programming/      ← Şu an buradasınız (Uzman seviye)
├── 01_pou_types.md          (Uzman)
├── 02_gvl_design.md         (Uzman)
├── 03_function_blocks.md    (Uzman)
├── 04_libraries.md          (Uzman)
├── 05_error_handling.md     (Uzman)
└── _synthesis.md (bu belge)

Önkoşul:
knowledge/codesys/fundamentals/   → determinizm felsefesi, runtime/proje/diller
knowledge/codesys/task-structure/ → tek-yazar/race, watchdog, öncelik

Sonraki adım — İleri/Uzman:
knowledge/codesys/advanced/   → oop_codesys, unit_testing, compiled_library, application_events
knowledge/codesys/debugging/  → profiling, hata ayıklama, performans analizi
knowledge/protocols/ (opc-ua, modbus) · knowledge/networking/ (ethercat)
knowledge/standards/safety_plc.md → SIL, güvenlik mimarisi
```
