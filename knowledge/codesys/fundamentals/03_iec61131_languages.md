---
KONU        : CODESYS'te IEC 61131-3 Programlama Dilleri
KATEGORİ    : codesys
ALT_KATEGORI: fundamentals
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_f_obj_pou.html"
    başlık: "CODESYS Online Help — Object: POU (implementation language seçimi)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_adding_objects.html"
    başlık: "CODESYS Online Help — Adding Objects"
    güvenilirlik: resmi
  - url: "https://feelautom.fr/en/blog/in-depth-comparison-of-iec-61131-3-programming-languages-ladder-st-fbd-sfc"
    başlık: "In-Depth Comparison of IEC 61131-3 Languages — FeelAutom"
    güvenilirlik: topluluk
  - url: "https://industrialmonitordirect.com/blogs/knowledgebase/iec-61131-3-language-comparison-ladder-vs-st-vs-fbd-vs-sfc"
    başlık: "IEC 61131-3 Language Comparison — Industrial Monitor Direct"
    güvenilirlik: topluluk
  - url: "https://www.controleng.com/which-iec-61131-3-programming-language-is-best-part-2/"
    başlık: "Which IEC 61131-3 Language Is Best? Part 2 — Control Engineering"
    güvenilirlik: topluluk
  - url: "https://plcprogramming.io/pillar/iec-61131-3-standards"
    başlık: "IEC 61131-3 Standard Complete Guide (2025) — PLCProgramming.io"
    güvenilirlik: topluluk
  - url: "https://www.iqytechnicalcollege.com/Programmable%20Logic%20Controllers%20%20IEC%2061131-3%20using%20CoDeSys.pdf"
    başlık: "Programmable Logic Controllers: IEC 61131-3 using CODESYS — Dag H. Hanssen"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_runtime_architecture.md"
    ilişki: gerektirir
  - konu: "02_project_structure.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/advanced/state_machines_sfc.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/advanced/oop_codesys.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "Temel mantık kapıları ve Boole cebri"
  - "POU kavramı (02_project_structure.md)"
  - "Herhangi bir programlama diline giriş düzeyinde aşinalık"
ÇELİŞKİLER :
  - kaynak: "IEC 61131-3 2. Baskı vs 3. Baskı"
    konu: "IL (Instruction List) dili 3. baskıda deprecated (kullanımdan kaldırılmış) olarak işaretlendi"
    çözüm: >
      IL, CODESYS V3.5'te hâlâ desteklenmektedir ancak yeni projeler için ST tercih edilmelidir.
      Eski IL kodunu ST'ye çeviren otomatik araçlar mevcuttur.
      CODESYS IDE → IL editörü → Edit → Convert to ST
  - kaynak: "Farklı PLC üreticileri"
    konu: "CFC (Continuous Function Chart) IEC standardında yoktur, CODESYS'e özgüdür"
    çözüm: >
      CODESYS'te FBD'nin yanı sıra CFC de kullanılabilir. CFC daha esnektir
      (serbest bağlantı, geri besleme loop'ları). Diğer platformlara taşınabilirlik
      gerektiren projeler için CFC yerine FBD tercih edilmelidir.
---

## Özün Ne

IEC 61131-3, PLC programlama için 5 resmi dil tanımlar: ST (Structured Text), LD (Ladder Diagram), FBD (Function Block Diagram), SFC (Sequential Function Chart) ve IL (Instruction List). CODESYS bu dillerin tümünü destekler ve bir proje içinde bunları serbestçe karıştırmanıza izin verir; her POU farklı bir dille yazılabilir. Her dilin farklı bir düşünce biçimini yansıttığını anlamak kritiktir: LD elektrikçi mantığıyla düşünür, FBD sinyal akışıyla, ST yazılımcı mantığıyla, SFC süreç mühendisi mantığıyla. Doğru dili doğru bağlamda kullanmak, kodun hem yazılmasını hem de bakımını kolaylaştırır.

## Nasıl Çalışır

### Dil Karşılaştırma Matrisi

| Özellik | ST | LD | FBD | SFC | IL |
|---|---|---|---|---|---|
| Paradigma | Metinsel / Prosedürel | Grafik / Kontaklar | Grafik / Blok | Grafik / Durum | Metinsel / Assembly |
| Hedef kitle | Yazılımcı | Elektrikçi / Teknisyen | Proses mühendisi | Süreç tasarımcısı | Düşük seviye uzman |
| Karmaşık mantık | ✅ Mükemmel | ⚠️ Zor | ⚠️ Zor | ❌ Uygun değil | ⚠️ Ağır |
| Görsel netlik | ⚠️ Orta | ✅ Yüksek | ✅ Yüksek | ✅ En yüksek | ❌ Düşük |
| Matematiksel işlem | ✅ Mükemmel | ❌ Zor | ⚠️ Orta | ❌ Uygun değil | ⚠️ Ağır |
| Sıralı kontrol | ⚠️ Mümkün (CASE) | ❌ Karmaşık | ❌ Karmaşık | ✅ Mükemmel | ❌ Uygun değil |
| Yeniden kullanım | ✅ Yüksek (FB) | ⚠️ Orta | ✅ Yüksek (FB) | ⚠️ Orta | ❌ Düşük |
| IEC 3. baskı durumu | ✅ Aktif | ✅ Aktif | ✅ Aktif | ✅ Aktif | ⚠️ Deprecated |

---

## ST — Structured Text (Yapısal Metin)

### Tanım

ST, Pascal'a benzeyen yüksek seviyeli metin tabanlı bir dildir. Modern yazılım geliştirme pratiklerine en yakın IEC dilidir. IF-THEN-ELSE, CASE, FOR, WHILE, REPEAT yapılarını destekler.

### Avantajları

- Karmaşık algoritmalara, matematiksel hesaplamalara, string işlemine en uygun dil.
- Versiyon kontrolü (Git/SVN) için ideal: diff ve merge metin tabanlı çalışır.
- OOP (Object Oriented Programming) CODESYS'te yalnızca ST üzerinden mümkündür.
- En kısa yazım, en yoğun bilgi ifadesi.

### Dezavantajları

- Elektrikçiler ve saha teknisyenleri için okunması zor.
- Görsel takip mümkün değil; bir sinyalin nereden gelip nereye gittiği okunarak anlaşılır.

### Örnek Kod

```iecst
(* Motorun sıcaklık korumalı çalıştırılması *)
PROGRAM PRG_MotorControl
VAR
    fbMotor     : FB_Motor;
    fbPID       : FB_PID;
    rTempScaled : REAL;
    xOverTemp   : BOOL;
    tFaultDelay : TON;
END_VAR

(* Analog sensör ölçeklendirme: 0-10V → 0-100°C *)
rTempScaled := (GVL_IO.rTempRaw / 10.0) * 100.0;

(* Aşırı sıcaklık algılama *)
xOverTemp := rTempScaled > GVL_Params.rMaxTemperature;

(* Gecikme ile hata: anlık spike'ları filtrele *)
tFaultDelay(IN := xOverTemp, PT := T#5S);

(* Motor FB çağrısı *)
fbMotor(
    xStartCommand := GVL_IO.xStartButton AND NOT tFaultDelay.Q,
    xStopCommand  := GVL_IO.xStopButton OR GVL_IO.xEmergencyStop,
    xFaultReset   := GVL_IO.xFaultResetButton
);

GVL_IO.xMotorOutput := fbMotor.xRunOutput;

(* PID ile hız kontrolü *)
IF fbMotor.eState = eRunning THEN
    fbPID(
        fActualValue  := rTempScaled,
        fSetpointValue:= GVL_Params.rTargetTemperature,
        fManSyncValue := 50.0,
        bManualMode   := FALSE
    );
    GVL_IO.rSpeedSetpoint := fbPID.fOut;
END_IF
```

---

## LD — Ladder Diagram (Merdiven Diyagramı)

### Tanım

LD, röle ve kontaktörlü elektrik devrelerini simüle eden grafik bir dildir. Sol ray güç kaynağını, sağ ray nötrü temsil eder. Aralarındaki "rung"lar (merdiven basamakları) mantığı tanımlar.

### Avantajları

- Elektrikçiler ve donanım teknisyenleri için sezgisel: Devre şemasıyla aynı mantık.
- Online debug sırasında "enerji akışı" görsel olarak izlenebilir (aktif kontaklar vurgulanır).
- Basit boolean mantığı ve interlock devreler için son derece net.
- Saha ekipleri, yazılım bilmeden sorun giderebilir.

### Dezavantajları

- Matematiksel hesaplamalar "kutu" içinde gösterilir, okunması güçleşir.
- Koşul ağaçları (nested IF) merdiven çok karmaşık ve geniş hale gelir.
- Git üzerinde takip yapmak pratik değil (binary/XML format).

### LD Elemanları

```
[Normalde Açık Kontakt]   —|  |—     xInput TRUE iken geçirir
[Normalde Kapalı Kontakt] —|/|—     xInput FALSE iken geçirir
[Poz Kenar Kontakt]       —|P|—     xInput'un yükselen kenarında tek pulse
[Neg Kenar Kontakt]       —|N|—     xInput'un düşen kenarında tek pulse
[Çıkış Bobini]            —( )—     Koşul sağlanırsa TRUE
[Set Bobini]              —(S)—     Koşul sağlanınca SET, düşürülmez
[Reset Bobini]            —(R)—     Koşul sağlanınca RESET
[Function Block Kutusu]   [TON]     Timer, Counter gibi bloklar kutu olarak
```

### Örnek (Basit Çalıştır-Durdur Devresi)

```
Rung 1: Çalıştırma komutu
|----[xStart]----[/xEmgStop]----[/xFault]-----(xRunCmd)-----|
           NOT                 NOT

Rung 2: Kendini tutma (Latch)
|----[xRunCmd]----[/xStopBtn]----(xRunCmd)----|
   (paralelde START veya mevcut RUN komutu)

Rung 3: TON ile motor gecikmeli start
|----[xRunCmd]----[TON_Start: PT=T#2S]----( Motor_ON )----|
```

### Ne Zaman Kullanılmalı

- Acil durum devresi, kilit (interlock) mantığı
- Saha personelinin okuyup anlayabileceği basit giriş/çıkış kontrol devresi
- Kapı sensörü, basınç anahtarı gibi boolean field cihaz entegrasyonları
- Müşteri, programı kendiniz okumak istiyor ve elektrik bilgisi var

---

## FBD — Function Block Diagram (Fonksiyon Blok Diyagramı)

### Tanım

FBD, mantığı bloklar ve bunları birbirine bağlayan sinyal hatları olarak gösterir. DCS (Distributed Control System) ortamlarından gelir; sürekli sinyal akışını görselleştirir.

### Avantajları

- PID, analog filtre, alarm yönetimi gibi süreç kontrol uygulamalarında son derece açık.
- Sinyallerin nereden gelip nereye gittiği grafiksel olarak takip edilir.
- FB'ler arasındaki bağlantılar görsel olarak doğrulanabilir.
- Kontrol mühendisleri (ISA S88 altyapılı) için doğal bir dil.

### Dezavantajları

- Koşullu mantık (IF/CASE) çok sayıda MUX/SEL bloğu gerektirir; görsel karmaşa yaratır.
- Büyük diyagramlar yatay olarak yayılır; ekranda gezinmek zorlaşır.
- Git ile versiyon takibi verimli değil.

### Örnek (PID Döngüsü — FBD Şematik Anlatım)

```
                  ┌───────────────┐
rActualTemp ──────│ in1           │
                  │   FC_Scale    │── rScaledTemp ──┐
0..100 range ─────│ in2           │                 │
                  └───────────────┘                 │
                                                    ▼
rSetpoint ─────────────────────────────────► [FB_PID]───► rOutput ──► rHeaterPower
                                              │  Kp=1.2
                                              │  Ki=0.5
                                              │  Kd=0.1
                                              │
                                        [Alarm Block]──► xOverTempAlarm
```

### CFC Notu (CODESYS Özel)

CODESYS ayrıca **CFC (Continuous Function Chart)** sunar. FBD'den farkı:
- Bloklar serbest konumlandırılabilir (grid'e bağlı değil)
- Geri besleme döngüleri (feedback loop) doğrudan oluşturulabilir
- Daha esnek ama IEC standardı dışında

Beckhoff TwinCAT, WAGO e!COCKPIT gibi CODESYS tabanlı platformlara özgüdür. Diğer platformlara taşınabilirlik için FBD tercih edilmelidir.

---

## SFC — Sequential Function Chart (Sıralı Fonksiyon Diyagramı)

### Tanım

SFC, Petri nets ve Grafcet'ten esinlenmiş grafik bir dildir. **Adımlar (Steps)** ve **Geçişler (Transitions)** olmak üzere iki temel eleman içerir. Bir otomasyon sürecinin fazlarını, sırasını ve koşullarını net biçimde görselleştirir.

### Avantajları

- Karmaşık sıralı süreçler (batch, makine döngüleri) için biçilmiş kaftan.
- Sistemin hangi adımda olduğu online modda anlık görülür.
- Süreç akışı, teknik bilmeyen kişilerin bile anlayabileceği netlikte.
- ISA S88 batch standardıyla birebir örtüşür.

### Dezavantajları

- Her adımın içindeki mantık başka bir dilde (ST, LD, FBD) yazılır; katmanlı yapı.
- Paralel sekanslar ve alternatif dallar görsel karmaşıklık yaratabilir.
- Küçük boolean kontrol devreleri için fazla ağır.

### SFC Temel Yapısı

```
         ══════════
          INIT Step
         ══════════
              │
         [Transition 1: xStartSignal = TRUE]
              │
         ═══════════
          STEP_01     ← Action: Motor1 çalıştır
         ═══════════   (Entry, During, Exit aksiyonları tanımlanabilir)
              │
         [Transition 2: xMotor1Running AND T#3S]
              │
         ═══════════
          STEP_02     ← Action: Sıcaklığı kontrol et
         ═══════════
              │
         [Transition 3: rTemp > 80.0 OR xStopCommand]
              │
    ──────────┼───────────     ← Paralel dal (OR)
    │                   │
════════════   ══════════════
  STEP_03A     STEP_03B        ← Aynı anda çalışır
════════════   ══════════════
    │                   │
    ──────────┼───────────     ← Paralel birleşme
              │
         [Transition 4: TRUE]
              │
         ══════════
          INIT Step  (döngü)
         ══════════
```

### Aksiyon Tipleri

| Qualifier | Açıklama |
|---|---|
| N (Non-stored) | Adım aktifken sürekli TRUE |
| S (Set) | Adım başladığında set, silinmez |
| R (Reset) | Adımda reset edilir |
| P (Pulse) | Adım başlangıcında tek pulse |
| L (Limited) | Belirtilen süre kadar TRUE |
| D (Delayed) | Belirtilen süreden sonra TRUE |

### Örnek (Dolum Makinesi Döngüsü)

```iecst
(* SFC içindeki bir Step'in Action kodu — ST ile yazılır *)
(* STEP_FillProduct aksiyonu *)
ACTION FillProduct_During:
    (* Dolum vanasını aç *)
    GVL_IO.xFillValve := TRUE;
    
    (* Dolum miktarını say *)
    IF GVL_IO.xFlowPulse THEN
        GVL_State.dwCurrentFill := GVL_State.dwCurrentFill + 1;
    END_IF
    
    (* Hedef miktara ulaştı mı? *)
    GVL_State.xFillComplete := 
        GVL_State.dwCurrentFill >= GVL_Params.dwTargetFill;
END_ACTION
```

---

## IL — Instruction List (Komut Listesi)

### Tanım

IL, assembly diline benzeyen düşük seviyeli bir metin dilidir. Her satır tek bir işlem içerir. IEC 61131-3'ün 3. baskısında **deprecated** (kullanımdan kaldırılmış) olarak işaretlenmiştir.

### Durumu

- CODESYS V3.5'te hâlâ destekleniyor ancak aktif olarak geliştirilmiyor.
- Yeni projeler için **kesinlikle kullanılmamalıdır**.
- Eski IL kodu ST'ye dönüştürülebilir (CODESYS IDE otomatik dönüştürme sunar).
- Siemens STL (Statement List) ile karıştırılmamalıdır; benzer görünse de farklıdır.

### Örnek (Tarihsel Referans İçin)

```
(* IL — Basit AND/OR mantığı *)
LD    xInput1       (* xInput1'i accumulator'a yükle *)
AND   xInput2       (* AND işlemi *)
OR    xInput3       (* OR işlemi *)
ST    xOutput       (* Sonucu xOutput'a kaydet *)
```

Aynı mantık ST'de:
```iecst
xOutput := (xInput1 AND xInput2) OR xInput3;
```

---

## Diller Arası Karşılaştırma ve Gerçek Tercih Rehberi

### Hangi Dil, Hangi Durum?

```
Senaryo                          → Önerilen Dil     Neden
─────────────────────────────────────────────────────────────
Makine güvenlik interlockları    → LD veya ST        Saha okunabilirliği
PID kontrolü, analog işlem       → ST veya FBD       Matematiksel güç / sinyal akışı
Sıralı makine döngüsü           → SFC + ST          Adım görünürlüğü + aksiyon mantığı
Reçete yönetimi, batch          → SFC + ST          ISA S88 uyumu
Kommunikasyon, protokol decode  → ST                String, array, döngü gücü
Kütüphane Function Block        → ST                OOP desteği, test edilebilirlik
Acil durum devresi               → LD                Saha teknisyeni bakımı
Analog ölçeklendirme fonksiyon  → ST                Saf hesaplama, test edilebilir
Proses sinyal akışı görselliği  → FBD               DCS mühendisi iletişimi
Assembly benzeri optimizasyon   → (gerekmiyor)       ST yeterli, IL önerilmez
```

### Dil Karıştırma Stratejisi (Best Practice)

Gerçek projelerde diller karıştırılır:

```
Proje Mimarisi Örneği:
├── PRG_Safety           → LD    (saha teknisyeni okuyabilir)
├── PRG_MainSequence     → SFC   (ana makine döngüsü)
│   └── Her SFC aksiyonu → ST    (aksiyon mantığı)
├── FB_TemperatureCtrl   → ST    (PID, math)
├── FB_Communication     → ST    (protokol, string, array)
├── FB_AnalogScaling     → ST (Function) (birim dönüşümü)
└── Visualization        → (Grafik editör, dil değil)
```

## Pratikte Nasıl Kullanılır

### Bir POU'nun Dilini Seçmek

CODESYS'te dil, POU oluşturulurken belirlenir. Resmi iş akışı:

```
Application (sağ tık) → Add Object → POU...
    ├── Name: FB_Motor
    ├── Type: ○ Program  ● Function Block  ○ Function
    └── Implementation language: ▼
            ├── Structured Text (ST)
            ├── Ladder Logic Diagram (LD)
            ├── Function Block Diagram (FBD)
            ├── Sequential Function Chart (SFC)
            ├── Instruction List (IL)
            └── Continuous Function Chart (CFC)   ← CODESYS'e özel
```

Aynı komuta `Project → Add Object → POU` menüsünden veya **POUs** görünümünde sağ tıkla da ulaşılır. POU oluşturulduktan sonra çift tıklanınca seçtiğiniz dile uygun editör açılır: ST için metin editörü, LD/FBD/SFC/CFC için grafik editör.

> **Önemli kısıt:** Bir POU **Function** türündeyse, implementasyon dili olarak **SFC seçilemez** (SFC adım/geçiş yapısı durumsuz fonksiyona uygun değildir).

### Oluşturulduktan Sonra Dil Değiştirme

CODESYS, bir POU'nun implementasyon dilini oluşturulduktan sonra menüden doğrudan değiştirmeye izin vermez (resmi dokümantasyon bu konuda yöntem belirtmez). Pratikte izlenen yol:

```
1. Hedef dilde YENİ bir POU oluştur (ör. FB_Motor_ST)
2. VAR bildirimlerini (arayüz + yerel) kopyala
3. Mantığı yeni dilde yeniden yaz (IL → ST için IDE otomatik dönüştürücü var:
   IL editörü → Edit → 'ST'ye dönüştür')
4. Eski POU'yu sil, çağrıları güncelle
```

Bu nedenle **dil seçimi başta doğru yapılmalıdır**; sonradan değişim manuel yeniden yazım demektir.

### Bir Projede Dilleri Karıştırmak

CODESYS bir proje içinde her POU'nun farklı dilde olmasına izin verir; bu bir kısıt değil, **önerilen** yaklaşımdır. Tipik dağılım:

```
PRG_Safety            → LD     (saha teknisyeni okuyabilsin)
PRG_MainSequence      → SFC    (makine döngüsü görünür olsun)
  └── Step Action'ları → ST    (adım mantığı)
FB_TemperatureCtrl    → ST     (PID, matematik)
FC_ScaleAnalog        → ST     (saf hesap — Function, SFC olamaz)
```

### Pratik İlk Tercih Kuralı

Kararsızsanız **ST ile başlayın**: tüm IEC yapı taşlarını destekler, OOP için tek seçenektir, metin tabanlı olduğu için Git diff/merge ile çalışır ve birim testine en uygun dildir. LD, FBD ve SFC'yi yalnızca güçlü oldukları bağlamda (interlock, sinyal akışı, sıralı döngü) seçici biçimde kullanın.

## Örnekler

### Örnek 1: Aynı Mantık 3 Dilde

**Görev**: Konveyör 5 saniye boyunca çalıştıktan sonra otomatik durduruluyor.

**ST (Structured Text):**
```iecst
PROGRAM PRG_ConveyorTimer
VAR
    tRunTimer : TON;
END_VAR

tRunTimer(IN := GVL_IO.xConveyorStart, PT := T#5S);
GVL_IO.xConveyorOutput := GVL_IO.xConveyorStart AND NOT tRunTimer.Q;
```

**LD (Ladder Diagram — metin temsili):**
```
Rung 1: Timer çalıştır
|----[xConveyorStart]----[TON: PT=T#5S]----|
                          tRunTimer

Rung 2: Çıkış (start var AMA timer bitmedi)
|----[xConveyorStart]----[/tRunTimer.Q]----(xConveyorOutput)----|
```

**FBD (metin temsili):**
```
xConveyorStart ──► [TON: PT=T#5S] ──► .Q ──► [NOT] ──┐
xConveyorStart ──────────────────────────────────────► [AND] ──► xConveyorOutput
```

---

### Örnek 2: SFC ile Dolum Sekansı

```
(* SFC Transition ST kodları *)

(* Transition: READY → FILLING *)
T_ReadyToFilling: GVL_IO.xStartButton AND NOT GVL_State.xFault;

(* Transition: FILLING → DRAINING *)
T_FillingToDraining: GVL_State.dwFillLevel >= GVL_Params.dwMaxFillLevel;

(* Transition: DRAINING → READY *)
T_DrainingToReady: GVL_State.dwFillLevel <= GVL_Params.dwMinFillLevel;
```

---

### Örnek 3: Gelişmiş ST — CASE ile Durum Makinesi

```iecst
FUNCTION_BLOCK FB_PackagingMachine
VAR_INPUT
    xStartCmd   : BOOL;
    xStopCmd    : BOOL;
    xItemDetect : BOOL;
END_VAR
VAR_OUTPUT
    xSealerOn    : BOOL;
    xEjectorOn   : BOOL;
    eCurrentStep : E_PackStep;
END_VAR
VAR
    tSealTimer   : TON;
    tEjectTimer  : TON;
    dwPackCount  : DWORD;
END_VAR

CASE eCurrentStep OF

    ePack_Idle:
        xSealerOn  := FALSE;
        xEjectorOn := FALSE;
        IF xStartCmd AND xItemDetect THEN
            eCurrentStep := ePack_Sealing;
        END_IF

    ePack_Sealing:
        xSealerOn := TRUE;
        tSealTimer(IN := TRUE, PT := T#800MS);
        IF tSealTimer.Q THEN
            tSealTimer(IN := FALSE);
            xSealerOn := FALSE;
            eCurrentStep := ePack_Ejecting;
        END_IF
        IF xStopCmd THEN
            tSealTimer(IN := FALSE);
            eCurrentStep := ePack_Idle;
        END_IF

    ePack_Ejecting:
        xEjectorOn := TRUE;
        tEjectTimer(IN := TRUE, PT := T#300MS);
        IF tEjectTimer.Q THEN
            tEjectTimer(IN := FALSE);
            xEjectorOn  := FALSE;
            dwPackCount := dwPackCount + 1;
            eCurrentStep := ePack_Idle;
        END_IF

    ELSE:
        (* Bilinmeyen durum — güvenli duruma geç *)
        xSealerOn    := FALSE;
        xEjectorOn   := FALSE;
        eCurrentStep := ePack_Idle;
END_CASE
```

---

## Sık Yapılan Hatalar

### Hata 1: Her Şeyi LD ile Yazmak

```
Senaryo: Sıcaklık kontrol algoritması LD'de yazılıyor.
Sonuç  : Onlarca rung, içlerinde matematik kutuları, okunması imkansız.
Çözüm  : Math işlemleri için ST, LD sadece discrete I/O için.
```

### Hata 2: SFC'yi Basit Durum Makinesi İçin Kullanmak

2-3 adımlı basit durum makineleri için SFC gerekmez; ST içinde `CASE` yeterlidir. SFC gerçek değerini 5+ adımlı, paralel dallar içeren karmaşık sekansda gösterir.

```
❌ Yanlış: 2 adımlı basit açık/kapa döngüsü için SFC
✅ Doğru : ST içinde CASE ile eIdle → eOpen → eClose
```

### Hata 3: FBD'de Feedback Loop Oluşturmaya Çalışmak

Standart FBD'de geri besleme döngüsü yapılamaz (blok çıkışını aynı döngü içinde kendi girişine bağlayamazsınız). Bu ihtiyaç varsa:
- CFC kullanın (CODESYS'e özgü)
- Veya ST ile yazın, bir sonraki scan cycle'da değeri okuyun

### Hata 4: IL Kodu Yeni Projeye Kopyalamak

IL, deprecated'dir. Eski bir projeden IL kodu kopyalanırsa:
1. CODESYS IDE'nin otomatik ST dönüştürücüsünü kullanın
2. Dönüştürülen kodu gözden geçirin ve test edin
3. IL bloğunu silin

### Hata 5: SFC Transition'ını Doğru Yazmamak

```iecst
(* ❌ Yanlış: Transition içinde yan etki yaratmak *)
T_Transition1: 
    xOutput := TRUE;  (* Transition'da assignment OLMAZ *)
    xInput AND xReady;

(* ✅ Doğru: Transition sadece boolean koşul döndürür *)
T_Transition1: xInput AND xReady;
(* xOutput ataması step aksiyon koduna taşınır *)
```

### Hata 6: LD'de Coil'i Birden Fazla Rung'da Kullanmak

```
Rung 1: |---[A]----(xOutput)---|
Rung 2: |---[B]----(xOutput)---|   ← ❌ HATALI: Multiple output coil

Son rung kazanır, Rung 1'in etkisi ezilir.
CODESYS'te bu statik analizde uyarı verir.

✅ Doğru:
Rung 1: |---[A]---[OR]---(xOutput)---|
Rung 2: |---[B]---┘
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### ST Tercih Edin

- Kütüphane geliştiriyorsanız (Function Block, Function)
- Algoritma, matematiksel hesaplama, string işleme yapıyorsanız
- OOP (Interfaces, Inheritance) kullanacaksanız
- Git ile versiyon kontrolü kritikse
- Test edilebilir, unit test yazılabilir kod istiyorsanız

### LD Tercih Edin

- Saha personelinin (elektrikçi, teknisyen) okuyup anlayacağı kod
- Basit interlock devreleri
- Güvenlik devrelerinde (SIL için LD daha kolay revize edilir)
- Müşterinin kendi ekibi bakım yapacaksa

### FBD Tercih Edin

- Proses kontrol mühendisleri ekibinizde varsa
- Sinyal akışının görsel takibi önemliyse
- DCS'ten gelip CODESYS'e geçiş yapan ekipler için adaptasyon
- Analog sinyal zincirleri görselleştirmek için

### SFC Tercih Edin

- 5+ adımlı sıralı makine döngüleri
- Batch üretim, reçete yönetimi (ISA S88)
- Paralel veya alternatif sekanslar
- Süreç adımlarının online izlenmesi kritikse

### IL Hiç Tercih Etmeyin

- Yeni projeler için kullanmayın
- Mevcut IL kodunu ST'ye dönüştürün
- Tek istisna: eski cihazlarla doğrulama gerektiren legacy projeler

## Gerçek Proje Notları

**Not 1 — Dil Seçiminin Bakım Maliyetine Etkisi**  
Bir boya hattı projesinde tüm mantık FBD ile yazılmıştı. 2 yıl sonra bakım ekibi yeni bir sıcaklık zonu ekledi; ancak ekibin ST deneyimi vardı, FBD bilmiyordu. FBD diyagramları yorumlamak 3 gün sürdü. Sonraki yeni moduller ST ile yeniden yazıldı. Ders: Ekibin bildiği dili kullanın veya ekibi eğitin.

**Not 2 — SFC'nin Online Görünürlüğünün Değeri**  
Bir dolum hattında intermittent arıza vardı; makine bazen yanlış adımda takılıp kalıyordu. SFC'nin online görünümü (hangi step'in aktif olduğu renkle vurgulanır) sayesinde arıza, saha ekibi tarafından 20 dakikada tespit edildi. Aynı mantık ST CASE içinde olsaydı debug için programcının devreye girmesi gerekirdi.

**Not 3 — ST ile Birim Test Yapılabilir Kod**  
FB_PID, FB_Motor gibi function block'ların tamamı ST ile yazıldı. Her FB için ayrı test programı (PRG_Test_FB_Motor) oluşturuldu; gerçek donanım olmadan simülasyonda test edildi. Bu yaklaşım, saha devreye almasını yarı yarıya kısalttı.

**Not 4 — LD'de Matematiksel İşlem Tuzağı**  
Bir proje özellikle "herkes okuyabilsin" gerekçesiyle tamamen LD ile yazılmıştı. Analog ölçeklendirme, PID output hesabı, alarm yönetimi hepsi LD'deydi. Rung başına bir matematik bloğu, 200+ rung, 40 sayfalık diyagram. Bakım ekibi, saha yerine dizüstünü açıp CODESYS'e bağlanmak zorunda kalıyordu. Paradoks: "herkes okuyabilsin" hedefi tersine döndü.

**Not 5 — SFC + ST Kombinasyonunun Gücü**  
En başarılı yaklaşım: SFC ana iskelet, ST aksiyon detayı. SFC yöneticilere ve proses mühendislerine "makine ne yapıyor" sorusunun cevabını verir. ST, yazılım ekibine "nasıl yapıyor"un detayını sunar. İkisi birlikte hem okunabilir hem güçlü bir kod tabanı oluşturur.

**Not 6 — REAL Karşılaştırması Yüzünden Takılan SFC Transition**  
Bir dolum hattında SFC transition'ı `rFillLevel = 100.0` yazılmıştı; makine bazen o adımda sonsuza dek takılıyordu. Neden: Kayan nokta (floating point) eşitliği. Sensör değeri `99.9997` ya da `100.0001` oluyor, asla tam `100.0` olmuyordu. Ders: `REAL`/`LREAL` için **asla `=` kullanma**; `>=`, `<=` ya da tolerans bandı (`ABS(a-b) < 0.001`) kullan. Bu, sahada en çok zaman kaybettiren sessiz hatalardan biridir.

**Not 7 — Timer'ı CASE İçinde Koşullu Çağırmanın Tuzağı**  
Bir geliştirici TON bloğunu yalnızca belirli bir CASE dalında çağırdı; diğer dallarda `tTimer()` hiç çalışmadı. TON, **her scan çağrılmazsa** iç zamanını güncellemez ve `.ET` donar. Diğer dala geçildiğinde timer kaldığı yerden devam etti, beklenmedik gecikmeler oluştu. Ders: FB instance'larını (özellikle timer/counter) her scan **koşulsuz** çağırın; davranışı `IN` girişiyle kontrol edin, çağrının kendisiyle değil.

**Not 8 — LD'de `JMP` ve Çoklu Network Kötüye Kullanımı**  
Eski bir projede LD içinde `JMP`/`LABEL` ile spagetti kontrol akışı kurulmuştu; kod LD görünüyordu ama mantığı IL kadar okunaksızdı. Ders: LD'de atlama (jump) kullanımı, dilin "görsel okunabilirlik" avantajını yok eder. Karmaşık akış gerekiyorsa o POU zaten ST'de olmalıydı — dil seçimi en baştan yanlıştı.

**Not 9 — CFC Yürütme Sırası Görünmezliği**  
CFC'de bloklar serbest konumlandırılır; bir mühendis sol-üstteki bloğun önce çalıştığını varsaydı, ama CFC kendi data-flow sırasını hesaplar ve bunu blok köşesindeki küçük numara ile gösterir. Yanlış varsayım, bir scan gecikmesi yarattı (bir blok diğerinin eski çıkışını okudu). Ders: CFC'de **execution order numaralarını** daima kontrol edin; gerekirse `Order → Set Execution Order` ile elle düzenleyin. FBD grid'e bağlı olduğu için bu sorun FBD'de daha nadirdir.

## Edge Case'ler ve Dil Sınırları

### ST'nin Sessiz Davranışları

- **Tamsayı taşması sessizdir:** `INT` (-32768..32767) taşınca sarmalanır (wrap), exception fırlatmaz. `nCount := nCount + 1` bir döngüde 32767'den sonra -32768 olur. Sayaçlar için `UDINT`/`DINT` kullanın ve sınır kontrolü ekleyin.
- **Tamsayı bölmede kalan atılır:** `7 / 2 = 3` (REAL değil). `REAL` sonucu için en az bir operand REAL olmalı: `7.0 / 2`.
- **Tip dönüşümü daraltması (narrowing):** `INT_TO_BYTE(300)` üst bitleri atar, `44` döner — uyarı vermeyebilir. Açık `_TO_` dönüşümlerinde aralık taşmasına dikkat.
- **`EXIT` ve `RETURN` SFC içinde farklı davranır:** ST aksiyonu içinde `RETURN`, yalnızca o aksiyondan çıkar, SFC adımından değil.

### Operatör ve Değerlendirme Sırası

- **Kısa devre (short-circuit) GARANTİ DEĞİLDİR:** Birçok dilde `A AND B`, A false ise B'yi atlar. IEC ST'de standart bunu **garanti etmez**; CODESYS bazı bağlamlarda her iki tarafı da değerlendirebilir. `IF (pPtr <> 0) AND (pPtr^.value > 0)` güvenli görünür ama pPtr null ise yine de dereference edilebilir → crash. Güvenli yol: iç içe `IF` kullanın.
- **Bit operatörü vs mantıksal operatör:** `AND`, `OR` hem boolean hem bit-bazlı çalışır (operand tipine göre). `WORD AND WORD` bit işlemidir; istemeden `BOOL` beklenen yerde `WORD` kullanmak sessiz mantık hatası verir.

### SFC Özel Edge Case'leri

- **Action qualifier `P` (Pulse) ve scan etkileşimi:** `P` aksiyonu adım aktifleştiğinde **bir kez** çalışır; ama adıma bir sonraki dönüşte yine bir kez çalışır. "Bir kere ömür boyu" değil, "her giriş başına bir kez"dir.
- **Eşzamanlı (parallel) dallarda transition:** Paralel kolların **hepsi** kendi son adımına ulaşmadan birleşme (convergence) geçişi tetiklenmez. Bir kol takılırsa tüm birleşme kilitlenir — sessiz deadlock.
- **SFC flag'leri:** `SFCInit`, `SFCReset`, `SFCError` gibi örtük (implicit) değişkenler etkinleştirilmemişse beklenen reset davranışı olmaz; bunları POU özelliklerinden açmak gerekir.

### LD/FBD Limitleri

- **Yürütme sırası soldan sağa, yukarıdan aşağıya** sabittir (CFC hariç); ama bir network içindeki bir FB çıkışı, aynı network'te kendisinden önce gelen başka bir bloğa beslenirse **bir scan gecikme** oluşur.
- **Multiple coil (Not'taki Hata 6)** statik analizde uyarı verir ama derlemeyi durdurmaz; son atama kazanır.

## Optimizasyon

### Dil Seçiminin Performans Boyutu

Dil seçimi yalnızca okunabilirlik değil, **üretilen kodun verimliliği**ni de etkiler — ama beklenenden az:

- ST, LD, FBD aynı ara temsile (IR) derlenir; basit mantıkta üçü de benzer makine kodu üretir. "ST daha hızlı" miti çoğunlukla yanlıştır.
- **Gerçek fark algoritmadadır:** Bir LD merdiveninde 50 rung'luk arama mantığı, ST'de bir `FOR` döngüsü + `ARRAY` ile hem daha hızlı hem daha az kod olur. Fark dilden değil, dilin teşvik ettiği veri yapısından gelir.
- **SFC overhead:** SFC, adım/geçiş yönetimi için ek durum makinesi kodu üretir. Çok basit (2-3 adım) mantıkta SFC, eşdeğer ST CASE'den ölçülebilir biçimde daha ağırdır. Sık çağrılan, basit mantıkta ST CASE tercih edin.

### ST Performans Best Practice'leri

```iecst
(* ❌ Yavaş: döngü içinde tekrarlanan FB çağrısı / hesap *)
FOR i := 0 TO 999 DO
    aResult[i] := aData[i] * fScale * SQRT(2.0);  (* SQRT her iterasyonda *)
END_FOR

(* ✅ Hızlı: değişmezi döngü dışına çıkar (loop invariant hoisting) *)
fFactor := fScale * SQRT(2.0);
FOR i := 0 TO 999 DO
    aResult[i] := aData[i] * fFactor;
END_FOR
```

- **`MEMCPY`/`MemMove`** büyük array kopyaları için eleman-eleman döngüden kat kat hızlıdır.
- **`CASE` vs uzun `IF-ELSIF` zinciri:** Yoğun (dense) tamsayı değerlerinde `CASE`, derleyici tarafından jump table'a çevrilebilir; uzun `ELSIF` zinciri sıralı karşılaştırmadır. Durum makineleri için `CASE` hem okunur hem hızlı.
- **String işlemleri pahalıdır:** `CONCAT`, `FIND` her çağrıda string'i tarar. Sıcak döngüde string kaçının; gerekiyorsa düşük öncelikli task'a taşıyın.

### Karma Dil Mimarisinde Performans Katmanlaması

```
Hızlı task (1ms)   → ST (kompakt, deterministik, minimum FB)
Orta task (10ms)   → ST + FBD (proses kontrol, PID)
Yavaş task (100ms) → SFC (sekans), string/iletişim ST'de
```

Pahalı, görsel-ağır mantığı (SFC, string) **asla** en hızlı task'a koymayın.

## Derin Teknik Detay

### Beş Dilin Tek Bir Derleyiciye İndirgenmesi

IEC 61131-3'ün beş dili **sözdizimsel cephe (front-end)** farklılıklarıdır; CODESYS derleyicisi hepsini ortak bir **soyut sözdizim ağacına (AST)** indirger, oradan platform native koduna derler. Bu yüzden:

- Bir ST POU, bir LD POU'yu çağırabilir; ikisi de aynı çağrı kuralına (calling convention) derlenir.
- LD'deki bir kontak ile ST'deki `IF` aynı boolean test makine koduna iner.
- Bu birleşik model, IEC 61131-3'ün en zarif tasarım kararıdır: diller **temsil**dir, **semantik** ortaktır. Petri-net kökenli SFC bile, altta bir durum değişkeni + transition kontrol akışına derlenir.

### Neden IL Deprecated Edildi?

IL (Instruction List), tek-akümülatörlü (single-accumulator) bir sanal makine modelini varsayar — 1990'ların düşük bellekli PLC'lerine uygundu. Deprecated edilme nedenleri:

- **Modern donanımda anlamsız:** IL'in "elle optimizasyon" avantajı, optimize eden derleyiciler karşısında kayboldu. ST kodu, IL'den en az aynı kadar verimli native kod üretir.
- **Akümülatör modeli kompozisyona direnir:** Karmaşık ifadeler, parantezli alt-ifadeler (IL'de `(` `)` operatörleri) IL'de çirkin ve hataya açıktır.
- **OOP ile uyumsuz:** Metot çağrısı, interface, polymorphism gibi V3 kavramları akümülatör modeline oturmaz. IEC komitesi geleceği ST'de gördü.

Siemens STL ile karıştırılır ama farklıdır: STL, S7 donanımına özgü zengin bir komut setine sahiptir; IEC IL ise minimal ve jeneriktir.

### CFC: IEC Dışı Ama Neden Var?

CFC (Continuous Function Chart) IEC standardında yoktur; 3S'in (CODESYS üreticisi) eklentisidir. Varlık nedeni: **DCS dünyasından gelen** kontrol mühendisleri, sürekli proses kontrolünü (geri besleme döngüleri, serbest yerleşim) FBD'nin grid kısıtı olmadan çizmek ister. CFC bunu sağlar:

- **Data-flow yürütme modeli:** CFC, blokları topolojik sıraya göre değil, **veri bağımlılığına** göre sıralar (execution order). Geri besleme döngüsünde bir bloğun çıkışı kendi girişine dönerse, CFC bunu "önceki scan değeri" olarak çözer — bu, FBD'nin yapamadığı şeydir.
- **Bedeli taşınabilirlik:** CFC POU'ları PLCopenXML ile bile diğer platformlara temiz taşınmaz. Platform-bağımsızlık gerektiren kütüphaneler asla CFC içermemelidir.

### ST'nin OOP Tekel Konumu

CODESYS'te OOP (METHOD, PROPERTY, INTERFACE, EXTENDS, IMPLEMENTS) yalnızca metin tabanlı bağlamlarda tanımlanır — pratikte ST. Neden grafik diller OOP'u tam desteklemez?

- Bir metot çağrısı `fb.Method(args)` doğal olarak metinseldir; bir kontak veya blokla "metot çağırma" semantiği zorlama olur.
- Inheritance ve polymorphism, derleme-zamanı tip çözümleme gerektirir; grafik editör bunu görsel olarak temsil edemez.
- Bu yüzden modern, test edilebilir, yeniden kullanılabilir CODESYS kod tabanları **ST + OOP** üzerine kuruludur; grafik diller arayüz/sahaya bakan ince katmanda kalır. Bu, dil seçiminin neden giderek ST'ye kaydığının yapısal sebebidir.

## İlgili Konular

```
knowledge/codesys/fundamentals/
├── 01_runtime_architecture.md   → Bu dillerin çalıştığı runtime
├── 02_project_structure.md      → Dillerin yazıldığı POU yapısı
└── _synthesis.md                → Üç belgenin özet sentezi

knowledge/codesys/advanced/
├── state_machines_sfc.md        → SFC detaylı rehberi
├── oop_codesys.md               → ST ile Interface, Inheritance, Polymorphism
└── unit_testing_codesys.md      → ST ile test edilebilir kod yazma

knowledge/standards/
├── iec61131_pou_types.md        → IEC standardı POU tanımları
└── isa88_batch.md               → SFC ile batch programlama

knowledge/codesys/libraries/
├── standard_library.md          → TON, TOF, CTU, RS, SR, MOVE
└── util_library.md              → FIFO, LIFO, sort algoritmaları
```
