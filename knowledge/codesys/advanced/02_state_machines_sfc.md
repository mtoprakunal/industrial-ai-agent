---
KONU        : Durum Makineleri — SFC Dili vs CASE Tabanlı (ST)
KATEGORİ    : codesys
ALT_KATEGORI: advanced
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://help.codesys.com/api-content/2/codesys/3.5.17.0/en/_cds_sfc_action_qualifier/"
    başlık: "CODESYS Online Help — SFC Action Qualifiers"
    güvenilirlik: resmi
  - url: "https://help.codesys.com/api-content/2/codesys/3.5.14.0/en/_cds_sfc_element_properties/"
    başlık: "CODESYS Online Help — SFC Element Properties (implicit flags: SFCInit, SFCReset, ...)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_f_obj_pou.html"
    başlık: "CODESYS Online Help — Object: POU (implementation language SFC)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "knowledge/codesys/fundamentals/03_iec61131_languages.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/programming/03_function_blocks.md"
    ilişki: gerektirir
  - konu: "01_oop_codesys.md"
    ilişki: tamamlar
  - konu: "_synthesis.md"
    ilişki: detaylandırır
ÖNKOŞUL     :
  - "ST CASE yapısı ve enum (fundamentals/03_iec61131_languages.md)"
  - "FB state machine deseni (programming/03_function_blocks.md)"
  - "Scan/task döngüsü kavramı"
ÇELİŞKİLER :
  - kaynak: "SFC dili savunucuları vs ST/CASE savunucuları"
    konu: "Karmaşık sekanslar SFC ile mi yoksa ST CASE ile mi yazılmalı?"
    çözüm: >
      İkisi de IEC 61131-3'te geçerlidir ve aynı problemi farklı güçlerle çözer.
      SFC görsel/online izlenebilirlik ve paralel dal yönetiminde üstündür;
      ST CASE versiyon kontrolü, test edilebilirlik, koşullu/iç içe mantıkta üstündür.
      Karar Ne Zaman bölümünde somutlaştırılmıştır; ikisi karışık da kullanılır.
  - kaynak: "Farklı PLC üreticileri"
    konu: "SFC implicit flag adları (SFCInit, SFCReset, SFCError...) platformlar arası birebir uyumlu değildir"
    çözüm: >
      Bu örtük değişkenler CODESYS'e özgüdür ve POU özelliklerinden açılmadıkça
      etkin olmazlar. Platform-bağımsız sekans gerekiyorsa ST CASE daha taşınabilirdir.
---

## Özün Ne

Bir otomasyon sürecinin "adımdan adıma ilerlemesi" iki yolla modellenir: **SFC dili** (Sequential Function Chart — grafik adım/geçiş yapısı) veya **ST içinde CASE tabanlı durum makinesi** (enum + CASE OF). İkisi de aynı temel fikri uygular — sistem her an tek bir durumdadır ve koşullar sağlandığında durum değiştirir — ama farklı güçlere sahiptir. SFC, "makine şu an hangi adımda?" sorusunu online modda görsel olarak yanıtlar ve paralel/alternatif dalları doğal ifade eder; ancak her adımın iç mantığı yine başka bir dilde (genellikle ST) yazılır ve versiyon kontrolü zordur. CASE state machine ise metin tabanlıdır: Git ile izlenir, birim testi yazılabilir, koşullu mantığı içerir, ama "online görünürlük" için ekstra çaba ister. Uzmanlık, hangi sürecin hangi yaklaşımı hak ettiğini ve her ikisinde de **açık (explicit) durum makinesi** disiplinini (her durum tanımlı, ELSE dalı var, durumsuz blok her scan çağrılı) korumayı bilmektir.

## Nasıl Çalışır

### Ortak Çekirdek: Açık Durum Makinesi

Her iki yaklaşım da şu üç soruya net cevap vermelidir:
1. **Hangi durumdayım?** (state değişkeni / aktif step)
2. **Bu durumda ne yapıyorum?** (action / CASE dalı gövdesi)
3. **Ne zaman geçerim?** (transition koşulu)

Bu üçü açıkça ayrılmadığında — örneğin geçiş koşulu eylem içine sızdığında — durum makinesi "örtük" hale gelir ve hata ayıklanamaz. rules.json'daki "açık state machine" ilkesi tam olarak bunu zorunlu kılar.

### SFC — Grafik Adım/Geçiş Modeli

SFC iki temel elemandan oluşur:
- **Step (Adım):** Sistemin bir fazı. Aktif olduğunda kendisine bağlı **Action**'lar çalışır. Bir başlangıç adımı (Init step) vardır.
- **Transition (Geçiş):** İki adım arası boolean koşul. TRUE olunca üst adım pasifleşir, alt adım aktifleşir.

Adımlara bağlanan eylemler **action qualifier** ile zamanlanır:

| Qualifier | Anlamı |
|---|---|
| N | Adım aktifken sürekli çalışır (Non-stored) |
| R | İlgili eylemi reset eder |
| S | Set — bir kez set edilir, adım pasifleşse de kalır (R ile silinene dek) |
| P | Pulse — adım aktifleşince bir kez çalışır |
| L | Limited — belirtilen süre boyunca aktif |
| D | Delayed — belirtilen gecikmeden sonra aktif |
| SD | Stored + Delayed — gecikmeli set, kalıcı |
| DS | Delayed + Stored — gecikme sonra set, adım aktif kalırsa |
| SL | Stored + time Limited — set edilir, süre dolunca kalkar |

> [DOĞRULANMADI — qualifier ayrıntılı zamanlama semantiği sürüm dokümanına göre teyit edilmeli; yukarıdaki özet IEC 61131-3 standart davranışına dayanır.]

**Örtük (implicit) bayraklar:** CODESYS, SFC POU'su için `SFCInit`, `SFCReset`, `SFCError`, `SFCPause`, `SFCEnableLimit` gibi örtük değişkenler sunar. Bunlar **POU özelliklerinden etkinleştirilmedikçe** çalışmaz. Adım/eylem zaman aşımı için adım özelliklerinde süre tanımlanabilir; aşıldığında `SFCError` tetiklenir.

### CASE Tabanlı Durum Makinesi (ST)

Aynı model metinsel olarak: bir enum durum değişkeni + `CASE OF`. Her dal bir durumdur; dal içinde hem eylem hem geçiş koşulu yer alır.

```iecst
TYPE E_FillStep : (eIdle := 0, eFilling := 1, eDraining := 2, eFault := 99); END_TYPE
```

```iecst
CASE eStep OF
    eIdle:
        (* eylem *)            xFillValve := FALSE;
        (* geçiş *)            IF xStart THEN eStep := eFilling; END_IF
    eFilling:
        xFillValve := TRUE;
        IF rLevel >= rTarget THEN xFillValve := FALSE; eStep := eDraining; END_IF
    eDraining:
        xDrainValve := TRUE;
        IF rLevel <= rMin THEN xDrainValve := FALSE; eStep := eIdle; END_IF
    ELSE:                       (* tanımsız durum → güvenli *)
        xFillValve := FALSE; xDrainValve := FALSE; eStep := eFault;
END_CASE
```

### İki Modelin Eşleşmesi

| SFC kavramı | CASE karşılığı |
|---|---|
| Step | enum durum değeri |
| Step action (N) | CASE dalı gövdesi |
| Transition | dal içindeki `IF ... THEN eStep := ...` |
| Init step | enum'un 0/ilk değeri + init ataması |
| Paralel dal | iki ayrı durum değişkeni (alt-makine) |
| SFCError (timeout) | dal içinde TON + fault geçişi |

İkisi semantik olarak aynı şeye derlenir (fundamentals/03 "diller temsildir, semantik ortaktır"). Fark **ifade biçimi** ve **araç desteğindedir**.

## Pratikte Nasıl Kullanılır

### SFC Seçildiğinde

```
Add Object → POU → Implementation language: Sequential Function Chart (SFC)
```
- Init step otomatik gelir; adımları ekleyip Action atayın (Action içeriği ST yazın).
- Transition'ları **yalnızca boolean koşul** olarak yazın — yan etki/atama koymayın (fundamentals/03 Hata 5).
- Timeout/diagnostik gerekiyorsa adım özelliklerinden süre + `SFCError`'u açın.

### CASE Seçildiğinde

- Durumları **enum** ile adlandırın (sihirli sayı yok — rules.json).
- Her CASE dalında: önce eylem, sonra geçiş koşulu.
- **ELSE dalı zorunlu** → bilinmeyen durumda güvenli duruma kaç (programming/03 ELSE felsefesi).
- Timer/sayaç/R_TRIG her scan **koşulsuz** çağrılmalı; CASE dalının içinde koşullu çağrı timer'ı dondurur (fundamentals/03 Not 7).

### İkisinin Karışımı (En Yaygın Üretim Deseni)

SFC ana iskelet, ST aksiyon detayı (fundamentals/03 Not 5): SFC "makine ne yapıyor" sorusunu yöneticilere/proses ekibine görsel verir; her step action'ı ST ile "nasıl"ı detaylandırır. Alternatif: üst düzey faz yönetimi SFC, cihaz-seviyesi state machine'ler klasik FB CASE içinde.

## Örnekler

### Örnek 1: Aynı Sekans — SFC ve CASE Yan Yana

**Görev:** Boş → Doldur → Karıştır → Boşalt → Boş döngüsü.

**SFC (metin temsili):**
```
   ═══════  Init: eEmpty   (N: tüm vanalar kapalı)
      │
   [T1: xStartButton AND NOT xFault]
      │
   ═══════  STEP_Fill       (N: FillValve aç; timeout 30s → SFCError)
      │
   [T2: rLevel >= rTarget]
      │
   ═══════  STEP_Mix         (L T#20S: Mixer çalışır)
      │
   [T3: tMixDone]
      │
   ═══════  STEP_Drain       (N: DrainValve aç)
      │
   [T4: rLevel <= rMin]
      │
   (Init'e döner)
```

**CASE (ST) eşdeğeri:**
```iecst
FUNCTION_BLOCK FB_BatchTank
VAR_INPUT
    xStart   : BOOL;
    xFault   : BOOL;
    rLevel   : REAL;
    rTarget  : REAL := 80.0;
    rMin     : REAL := 5.0;
END_VAR
VAR_OUTPUT
    xFillValve  : BOOL;
    xDrainValve : BOOL;
    xMixer      : BOOL;
    eStep       : E_BatchStep;
END_VAR
VAR
    tFillTimeout : TON;
    tMix         : TON;
END_VAR

(* Durumlu bloklar her scan koşulsuz çağrılır *)
tFillTimeout(IN := (eStep = eBatch_Fill), PT := T#30S);
tMix(IN := (eStep = eBatch_Mix), PT := T#20S);

CASE eStep OF
    eBatch_Empty:
        xFillValve := FALSE; xDrainValve := FALSE; xMixer := FALSE;
        IF xStart AND NOT xFault THEN
            eStep := eBatch_Fill;
        END_IF

    eBatch_Fill:
        xFillValve := TRUE;
        IF rLevel >= rTarget THEN
            xFillValve := FALSE;
            eStep := eBatch_Mix;
        ELSIF tFillTimeout.Q THEN          (* timeout → fault *)
            eStep := eBatch_Fault;
        END_IF

    eBatch_Mix:
        xMixer := TRUE;
        IF tMix.Q THEN
            xMixer := FALSE;
            eStep := eBatch_Drain;
        END_IF

    eBatch_Drain:
        xDrainValve := TRUE;
        IF rLevel <= rMin THEN
            xDrainValve := FALSE;
            eStep := eBatch_Empty;
        END_IF

    eBatch_Fault:
        xFillValve := FALSE; xDrainValve := FALSE; xMixer := FALSE;
        (* reset harici yönetilir *)

    ELSE:
        xFillValve := FALSE; xDrainValve := FALSE; xMixer := FALSE;
        eStep := eBatch_Fault;
END_CASE
```

### Örnek 2: Paralel Dallar — SFC'nin Doğal Üstünlüğü

SFC'de iki kol aynı anda çalışıp birleşir:
```
        [T: xStart]
   ─────────┼──────────
   │                  │
 STEP_HeatA        STEP_PressureB     (eşzamanlı)
   │                  │
   ─────────┼──────────              (birleşme: HER İKİSİ de bitince)
        [T: TRUE]
```

CASE'de paralel kollar iki ayrı durum değişkeniyle modellenir:
```iecst
(* iki bağımsız alt-makine, ana makine ikisinin de bitmesini bekler *)
fbHeatSub(xRun := xPhaseActive);          (* kendi CASE state machine'i *)
fbPressSub(xRun := xPhaseActive);

IF fbHeatSub.xDone AND fbPressSub.xDone THEN
    eMainStep := eMain_Next;              (* birleşme *)
END_IF
```

### Örnek 3: Diagnostik İçin Durum Geçmişi (CASE'in Esnekliği)

```iecst
(* CASE'de durum geçişini loglamak trivial — SFC'de ekstra çaba ister *)
IF eStep <> eStepPrev THEN
    GVL_Diag.aStepHistory[GVL_Diag.nHistIdx] := eStep;
    GVL_Diag.nHistIdx := (GVL_Diag.nHistIdx + 1) MOD UINT#16;
    eStepPrev := eStep;
END_IF
```

## Sık Yapılan Hatalar

### Hata 1: Transition İçinde Yan Etki

```iecst
(* ❌ SFC transition'ı yalnızca boolean döndürmeli — atama OLMAZ *)
T1: xValve := TRUE; xStart AND xReady;
(* ✅ atamayı step action'a taşı, transition saf koşul *)
T1: xStart AND xReady;
```

### Hata 2: CASE'de ELSE Yok

ELSE'siz CASE, tanımsız durumda hiçbir dal çalıştırmaz → çıkışlar son değerinde donar → makine belirsiz hareket eder (programming/03 Not 4). Her CASE'de `ELSE → güvenli durum`.

### Hata 3: Durumlu Bloğu CASE Dalı İçinde Koşullu Çağırmak

```iecst
(* ❌ TON yalnızca bir dalda çağrılırsa diğer dallarda .ET donar *)
eBatch_Fill:
    tTimer(IN := TRUE, PT := T#30S);   (* yalnızca burada *)

(* ✅ timer'ı CASE dışında, koşulsuz çağır; IN ile kontrol et *)
tTimer(IN := (eStep = eBatch_Fill), PT := T#30S);
```

### Hata 4: REAL Eşitliğiyle Geçiş

```iecst
(* ❌ float eşitliği — sensör asla tam 100.0 olmaz, adımda takılır *)
IF rLevel = 100.0 THEN ...
(* ✅ eşik/karşılaştırma kullan (fundamentals/03 Not 6) *)
IF rLevel >= 100.0 THEN ...
```

### Hata 5: SFC Paralel Dalda Deadlock

Paralel kolların **hepsi** son adımına ulaşmadan birleşme geçişi tetiklenmez. Bir kol takılırsa tüm birleşme kilitlenir (sessiz deadlock). Her paralel kola **timeout** ekleyin.

### Hata 6: SFC Implicit Flag'lerin Kapalı Olması

`SFCReset`/`SFCInit` POU özelliklerinden açılmadıysa beklenen reset davranışı oluşmaz. Reset stratejisi tasarlanıyorsa bu bayrakları önce etkinleştirin.

### Hata 7: 2 Adımlık İş İçin SFC

2-3 adımlı basit döngü için SFC fazla ağırdır ve ölçülebilir ek yük getirir (fundamentals/03 Optimizasyon). Basit sekans → CASE.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### SFC Tercih Edin

- **5+ adımlı sıralı süreçler** (batch, makine döngüsü, CIP/temizleme).
- **Paralel / alternatif dallar** doğal ifade gerektiriyorsa.
- **Online görünürlük kritik**: saha ekibi "hangi adım aktif" renkle görsün (fundamentals/03 Not 2).
- **ISA S88 batch** uyumu, reçete sekansları.
- Proses mühendisleri/operatörler kodu okuyacaksa.

### CASE (ST) Tercih Edin

- **Versiyon kontrolü kritik** (Git diff/merge — SFC binary/XML zor izlenir).
- **Birim testi** yazılacak (FB CASE simülasyonda test edilir — programming/03 Not 3).
- **Koşullu/iç içe mantık** ağırlıkta (SFC'de iç içe koşul çirkinleşir).
- **Yeniden kullanılabilir FB / kütüphane** geliştiriyorsanız (OOP yalnızca metinsel — 01_oop_codesys.md).
- **Sıcak döngü / basit sekans** (SFC overhead'i istenmiyor).
- **Diagnostik/log/state geçmişi** programatik gerekiyorsa.

### Karar Kuralı

> Süreç "doğrusal bir akış, görsel takip değerli, 5+ adım, belki paralel" ise SFC. Süreç "test edilebilir/yeniden kullanılabilir FB, koşullu mantık, Git, az adım" ise CASE. Kararsızsanız **CASE ile başlayın**: her zaman SFC iskeletine sarmalayabilirsiniz; tersi (SFC'den temiz CASE'e) daha zordur.

## Gerçek Proje Notları

**Not 1 — SFC Online Görünürlüğünün Arıza Çözdüğü An**
Bir dolum hattında makine ara ara yanlış adımda takılıyordu. SFC online görünümünde aktif step renkle vurgulandığı için saha ekibi arızayı 20 dakikada buldu (fundamentals/03 Not 2). Aynı mantık ST CASE'de olsaydı, programcının bağlanıp `eStep` değerini izlemesi gerekirdi. Ders: operatör/saha bakımı önceliğindeyse SFC'nin görünürlüğü somut zaman kazandırır.

**Not 2 — CASE'in Test Avantajı**
Bir paketleme FB'si tamamen CASE state machine'di. Devreye almadan önce `PRG_TestPackaging` ile her durum geçişi simülasyonda doğrulandı; sahada makineye dokunmadan mantık onaylandı (programming/03 Not 3). SFC ile bu kadar temiz bir offline test kurmak daha zordu. Ders: test edilebilirlik önceliğindeyse CASE kazanır.

**Not 3 — Paralel Dal Deadlock'u (SFC)**
Bir CIP (temizleme) sekansında iki paralel kol vardı: biri sıcaklık, biri debi. Debi sensörü arızalandı, o kol son adıma ulaşamadı; birleşme tetiklenmedi, tüm sekans sonsuza kilitlendi — ama hiçbir alarm yoktu (sessiz deadlock). Çözüm: her paralel kola adım timeout + `SFCError` eklendi. Ders: SFC paralel dallarda timeout olmadan deadlock kaçınılmazdır.

**Not 4 — Karışık Yaklaşımın Gücü**
En başarılı büyük projede üst seviye faz yönetimi SFC (Hazırlık → Üretim → Temizlik → Bekleme), her fazın içindeki cihaz mantığı klasik FB CASE'di. Yöneticiler SFC'den süreci, mühendisler FB'lerden detayı okudu. İki katman birbirini boğmadı. Ders: SFC ve CASE rakip değil, farklı soyutlama katmanlarıdır.

**Not 5 — SFC'nin Git ile Çatışması**
SFC ağırlıklı bir proje iki şubede paralel geliştirildi. Merge zamanı SFC'nin XML temsili çakıştı; CODESYS'in görsel diff'i sınırlıydı, değişiklikleri elle ayıklamak yarım gün sürdü. Aynı projedeki ST CASE FB'leri sorunsuz merge oldu. Ders: çok kişili paralel geliştirmede ST CASE versiyon kontrolüyle çok daha barışıktır.

**Not 6 — Init Değeri Atanmamış Enum**
Bir CASE makinesinde `eStep` enum'unun ilk değeri 0 değildi (`eIdle := 10` gibi başlamıştı) ama init ataması yoktu; instance 0'dan başladı, hiçbir dala düşmedi, yalnızca ELSE çalıştı. Ders: enum durumlarında 0 ya geçerli bir durum olsun ya da `eStep`'e açık init değeri verin (programming/01 edge case).

## İlgili Konular

```
knowledge/codesys/advanced/
├── _synthesis.md               → Durum makinesi tasarımı + OOP ne zaman sentezi
└── 01_oop_codesys.md           → State machine'i metoda taşıma (OOP), polimorfik durum

knowledge/codesys/fundamentals/
└── 03_iec61131_languages.md    → SFC dili tanıtımı, qualifier'lar, dil seçimi

knowledge/codesys/programming/
├── 03_function_blocks.md       → FB içinde CASE state machine, ELSE felsefesi
└── 01_pou_types.md             → State machine'in yaşadığı FB instance modeli

knowledge/standards/
└── (ISA S88 batch — SFC ile reçete/batch sekansları)
```
