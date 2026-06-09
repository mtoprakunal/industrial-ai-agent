---
KONU        : CODESYS Kütüphane Sistemi
KATEGORİ    : codesys
ALT_KATEGORI: programming
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_struct_installing_libraries.html"
    başlık: "CODESYS Online Help — Library Repository and Manager"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_library_development_information.html"
    başlık: "CODESYS Online Help — Library Developer Information"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_adding_libraries_to_project.html"
    başlık: "CODESYS Online Help — Adding a Library"
    güvenilirlik: resmi
  - url: "https://www.shaswatraj.com/post/codesys-library-management-step-by-step-guide"
    başlık: "Shaswatraj — CODESYS Library Management Step by Step"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Engineering/thread/27bffb3366/"
    başlık: "CODESYS Forge — Library Versioning tartışması"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "03_function_blocks.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/fundamentals/02_project_structure.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Function Block kavramı (03_function_blocks.md)"
  - "CODESYS Library Manager'ı proje içinde nasıl açacağını bilmek"
ÇELİŞKİLER :
  - kaynak: "Kütüphane sürüm yönetimi pratikleri"
    konu: "Use newest version' seçeneği kullanılmalı mı?"
    çözüm: >
      Geliştirme aşamasında 'Use newest version' kolaylık sağlayabilir.
      Üretim projelerinde mutlaka sabit sürüm kilitlenmelidir (ör. 3.5.17.0).
      Kütüphane güncellemesi her zaman kontrollü olmalı; gerileme testi yapılmadan
      yeni sürüm üretim projesine alınmamalıdır.
---

## Özün Ne

Kütüphaneler, tekrar kullanılabilir POU koleksiyonlarıdır. Projeye eklenmiş bir kütüphane, içindeki tüm Function Block, Function ve DUT'ları kullanılabilir hale getirir. CODESYS'in yerleşik kütüphaneleri (Standard, Util, CAA) hayatı kolaylaştıran onlarca hazır blok sağlar. Kendi kütüphanenizi oluşturmak ise `FB_Motor`, `FB_Valve` gibi tekrar kullandığınız bloklarını bir kez yazıp on farklı projede hatasız kullanmanın yoludur. Kütüphane sistemini anlamayan proje, ya her seferinde tekerleği yeniden icat eder ya da versiyonsuz kopyaların kaosuna sürüklenir.

## Nasıl Çalışır

### Kütüphane Türleri

```
Kütüphane Türü        Uzantı                    Kaynak Kod  IP Koruması
──────────────────────────────────────────────────────────────────────────
Açık kütüphane        *.library                 Görünür     Hayır
Derlenmiş kütüphane   *.compiled-library-v3     Gizli       Evet + Şifre
Container kütüphane   *.library (içeride lib)   Karma       —
External kütüphane    *.dll / *.so (C kodu)     Gizli       Evet
```

**Açık kütüphane:** Kaynak kod Library Manager'dan çift tıklanarak okunabilir. Topluluk kütüphaneleri (OSCAT), eğitim, şeffaflık amaçlı.

**Derlenmiş kütüphane:** Kaynak kod şifreli veya gizli. OEM'ler, kendi IP'lerini korumak için kullanır. CODESYS Security Key lisansı gerektirir.

**External kütüphane:** C dilinde yazılmış, platform-native performans gerektiren işlemler için (görüntü işleme, FFT, dosya şifreleme). ARM veya x64 için ayrı derleme gerekir.

---

### Yerleşik Kütüphaneler

#### Standard.library

Her CODESYS projesine otomatik eklenir. Temel blokları içerir:

```
Zamanlayıcılar:
  TON   — Açılma gecikmeli timer (On-Delay)
  TOF   — Kapanma gecikmeli timer (Off-Delay)
  TP    — Pulse timer (sabit genişlikte darbe)
  RTC   — Real-Time Clock (saat/tarih)

Sayaçlar:
  CTU   — Yukarı sayaç (Count Up)
  CTD   — Aşağı sayaç (Count Down)
  CTUD  — Yukarı/aşağı sayaç

Bistable:
  SR    — Set baskın bistable (Set dominant)
  RS    — Reset baskın bistable

Kenar Algılama:
  R_TRIG — Yükselen kenar (Rising Edge)
  F_TRIG — Düşen kenar (Falling Edge)

Veri İşleme:
  SEL   — Seçici (2 giriş, boolean seçim)
  MUX   — Çoklayıcı (N giriş, integer seçim)
  LIMIT — Sınırlama (min, max)
  MOVE  — Değer kopyalama
```

```iecst
(* Standard.library kullanım örnekleri *)

(* TON: 3 saniye sonra TRUE *)
tMyTimer(IN := xTrigger, PT := T#3S);
IF tMyTimer.Q THEN
    xDelayedAction := TRUE;
END_IF

(* CTU: Her yükselen kenarda say *)
cProductCount(CU := xProductSensor, RESET := xCountReset);
dwCount := DWORD(cProductCount.CV);

(* R_TRIG: Yükselen kenarı yakala *)
fbEdge(CLK := xButton);
IF fbEdge.Q THEN
    (* Butona tam bir kez basıldı *)
END_IF
```

#### Util.library

Gelişmiş veri yapıları ve yardımcı bloklar:

```
FIFO Yapıları:
  FIFO_DWORD — DWORD için kuyruk (First In First Out)
  FIFO_REAL  — REAL için kuyruk

LIFO (Stack):
  LIFO_DWORD — DWORD için yığın

Sıralama:
  SortBubble — Baloncuk sıralaması (küçük diziler)
  SortQuick  — Hızlı sıralama

String İşleme:
  CONCAT, DELETE, FIND, INSERT, LEFT, LEN, MID, REPLACE, RIGHT

Matematiksel:
  Mean, Variance, StdDev (istatistik)
```

```iecst
(* Util.library — Alarm geçmişi FIFO örneği *)
VAR
    fifoAlarms : FIFO_DWORD;
    dwAlarmCode : DWORD;
    bDataOK : BOOL;
END_VAR

(* Yeni alarm ekle *)
fifoAlarms.PutD(Put := TRUE, In := 16#00010002);  (* Alarm kodu *)

(* Son alarmı al ve işle *)
fifoAlarms.GetD(Get := TRUE, Out => dwAlarmCode, Valid => bDataOK);
IF bDataOK THEN
    (* dwAlarmCode işle *)
END_IF
```

#### CAA (CODESYS Application Architecture) Kütüphaneleri

CAA, gelişmiş işlevler için opsiyonel kütüphane ailesidir:

| Kütüphane | İçerik |
|---|---|
| CAA_File | Dosya sistemi erişimi (okuma, yazma, silme) |
| CAA_SerialCom | Seri port iletişimi (RS-232/485) |
| CAA_CAN | CAN bus mesaj gönderme/alma |
| CAA_BACNet | BACNet protokol desteği |
| CAA_MemBlockMan | Bellek blok yönetimi |

```iecst
(* CAA_File — CSV log dosyası oluşturma *)
VAR
    hFile    : CAA.HANDLE;
    xError   : BOOL;
    eError   : CAA.ERROR;
    sLine    : STRING(200);
END_VAR

hFile := FILE.Open(sPathName := '/home/codesys/log.csv',
                   eFileMode := FILE.MODE.WRITE_PLUS,
                   xError => xError, eError => eError);
IF NOT xError THEN
    sLine := CONCAT(sLine, 'Timestamp,Temperature,Pressure');
    FILE.Write(hFile := hFile, pBuffer := ADR(sLine), ...);
    FILE.Close(hFile := hFile);
END_IF
```

---

### Kendi Kütüphanenizi Oluşturma

#### Adım 1 — Library Projesi Oluşturma

```
File → New Project → Library (kütüphane şablonu)
    Name: MyMachineLib
    Company: MyCompany
    Version: 1.0.0.0
    Default namespace: MyMachineLib
```

Library projesi, standart projeden farkı: Device tree yoktur, yalnızca POU'lar, DUT'lar ve GVL'ler içerir.

#### Adım 2 — Project Information Doldurma

```
Project → Project Information:
    Title     : My Machine Library
    Version   : 1.2.3.0
    Company   : Acme Automation
    Author    : J. Smith
    Description: Motor, valve and sensor control blocks
    
(* Bu bilgiler Library Manager'da görüntülenir *)
(* Derlenmiş kütüphanede dış API dokümantasyonuna dönüşür *)
```

#### Adım 3 — POU'ları Ekle

Normal proje gibi FB, Function, DUT ekleyin. Namespace prefix her POU'nun önüne eklenir: `MyMachineLib.FB_Motor`.

#### Adım 4 — Kütüphaneyi Yükle

```
File → Save as Library
    Format seç:
    ○ *.library         (açık — kaynak kod görünür)
    ○ *.compiled-library-v3 (gizli — CODESYS Security Key gerekir)

Tools → Library Repository → Add Library → kütüphane dosyasını seç
```

#### Adım 5 — Projeye Ekle

```
Library Manager → Add Library → MyMachineLib araması yap → Seç → OK

Kullanım:
    VAR
        fbMotor1 : MyMachineLib.FB_Motor;
    END_VAR
    
    (* Veya namespace prefix kaldırılırsa: *)
    VAR
        fbMotor1 : FB_Motor;  (* Namespace transparent ise *)
    END_VAR
```

---

### Versiyon Yönetimi

```
Kütüphane versiyonu: MAJOR.MINOR.PATCH.BUILD
Örnek: 1.2.3.0

MAJOR: Geriye dönük uyumlu olmayan değişiklikler (API kırılması)
MINOR: Geriye dönük uyumlu yeni özellikler
PATCH: Hata düzeltmeleri
BUILD: Derleme numarası (otomatik)
```

**Proje içinde kütüphane referansı:**

```
Library Manager'da her kütüphane için:
  ✓ Sabit versiyon: Standard, 3.5.17.0
  ✗ Newest versiyon: Standard, * (üretimde tehlikeli)
```

**Kütüphane güncellemesi nasıl yapılır:**

```
1. Yeni versiyonu library repository'ye yükle
2. Test projesinde gerileme testi yap
3. Onaylandıktan sonra üretim projesinde:
   Project → Project Environment → Libraries → 
   MyMachineLib 1.0 → Update → 1.1
4. Değişiklikleri gözden geçir, test et
5. Commit (Git/SVN)
```

---

### Kütüphane Bağımlılık Yönetimi

```
Proje
├── Standard, 3.5.17.0          (hiçbir şeye bağlı değil)
├── Util, 3.5.17.0              (Standard'a bağlı)
├── CAA_File, 3.5.17.0         (Standard'a bağlı)
└── MyMachineLib, 1.2.0.0      (Standard ve Util'e bağlı)
    └── Otomatik çözümlenir: Util, Standard da eklenir
```

CODESYS kütüphane bağımlılıklarını otomatik çözer. Ancak çakışan bağımlılık versiyonları (farklı iki kütüphane, aynı alt kütüphanenin farklı versiyonunu gerektiriyorsa) derleme hatası verebilir.

**Projectarchive ile taşıma:**

```
File → Save as Project Archive (*.projectarchive)
    ☑ Include all referenced libraries
    
→ Tek dosya tüm kütüphaneleri içeriyor. Başka makineye taşımak için ideal.
```

## Pratikte Nasıl Kullanılır

### Library Manager Detay

```
Application → Library Manager (çift tık)

Görünüm:
  Library Name        | Version    | Namespace  | Placeholde
  Standard            | 3.5.17.0   | *          | -
  Util                | 3.5.17.0   | Util        | -
  MyMachineLib        | 1.2.0.0   | MyMachine   | -
  └── Standard (dep)  | 3.5.17.0   | -           | -
  └── Util (dep)      | 3.5.17.0   | -           | -

İkonlar:
  📁 = Kütüphane — açılabilir
  🔒 = Compiled — kaynak gizli
  ⚠ = Version uyuşmazlığı
  ✱ = Placeholder (yüklü değil)
```

**Placeholder nedir?** Kütüphane yüklü değil ama proje referans ediyor. Compile hatası vermeden açılabilir — kütüphane bulununca placeholder kalkar.

### Kütüphane Namespace Yönetimi

```iecst
(* Namespace ile kullanım — açık, çakışma yok *)
VAR
    fbMotor1 : MyMachineLib.FB_Motor;
    fbMotor2 : ThirdPartyLib.FB_Motor;  (* Farklı kütüphaneden, aynı isim — OK *)
END_VAR

(* qualified_only kaldırılmış kütüphane — prefix gerekmez *)
(* Ama iki kütüphanede aynı isim varsa derleme hatası! *)
VAR
    fbMotor1 : FB_Motor;   (* Hangisi? Belirsiz — derleme hatası *)
END_VAR
```

## Örnekler

### Örnek 1: Standard.library Temel Bloklarının Kullanımı

```iecst
(* Üretim hattı başlatma sekansı — Standard.library ile *)
PROGRAM PRG_StartupSequence
VAR
    tValve1_Delay  : TON;
    tMotor1_Delay  : TON;
    cStartAttempts : CTU;
    fbEStop_Edge   : R_TRIG;
    srRunlatch     : SR;
END_VAR

(* E-stop yükselen kenar — acil durumu kaydet *)
fbEStop_Edge(CLK := GVL_IO.xEmergencyStop);
IF fbEStop_Edge.Q THEN
    cStartAttempts(RESET := TRUE);  (* Sayacı sıfırla *)
END_IF

(* Start denemelerini say *)
cStartAttempts(CU := GVL_HMI.xStartBtn, RESET := FALSE);
IF cStartAttempts.CV >= 3 THEN
    GVL_Alarms.xTooManyStartAttempts := TRUE;
END_IF

(* Set-dominant bistable: E-stop SET'ler, normal koşul RESET'ler *)
srRunlatch(SET1 := GVL_IO.xRunPermission,
           RESET := GVL_IO.xEmergencyStop OR GVL_Alarms.xAnyActiveAlarm);
GVL_State.xRunEnabled := srRunlatch.Q1;

(* Sıralı gecikme: Vana aç → 3sn bekle → Motor çalıştır *)
tValve1_Delay(IN := GVL_State.xRunEnabled, PT := T#3S);
GVL_IO.xValve1_Out := GVL_State.xRunEnabled;
tMotor1_Delay(IN := tValve1_Delay.Q, PT := T#1S);
GVL_IO.xMotor1_Out := tMotor1_Delay.Q;
```

### Örnek 2: Kendi Kütüphanenin Minimum Yapısı

```
MyMachineLib (Library Project)
│
├── POUs
│   ├── FB_Motor          (Temel motor kontrol)
│   ├── FB_Valve          (Vana kontrol)
│   ├── FB_AnalogSensor   (Analog ölçeklendirme + filtre + alarm)
│   ├── FC_ScaleLinear    (Lineer ölçeklendirme fonksiyon)
│   └── FC_IsInRange      (Sınır kontrol fonksiyonu)
│
├── DUTs
│   ├── ST_MotorDiag      (Motor diagnostik struct)
│   ├── ST_AlarmRecord    (Alarm kayıt struct)
│   ├── E_MotorState      (Motor durum enum)
│   └── E_ValveState      (Vana durum enum)
│
└── GVLs
    └── GVL_Version       (Kütüphane versiyon sabiti — VAR_GLOBAL CONSTANT)
        VERSION_STRING : STRING := '1.2.0';
```

### Örnek 3: Kütüphane Versiyonu Kırıldığında Ne Olur?

```
Senaryo: MyMachineLib 1.0 → 1.1 güncellendi.
FB_Motor'da tStartDelay parametresi kaldırıldı, tStartupTime ile değiştirildi.

Güncelleme sonrası derleme:
  ERROR: FB_Motor: Unknown input 'tStartDelay' in instance 'fbMotor1'
  ERROR: FB_Motor: Unknown input 'tStartDelay' in instance 'fbMotor2'
  ... (12 hata)

Doğru yönetim:
  1. Versiyon 1.1 changelog'unda kırılan değişiklik belgelenmiş: "BREAKING: tStartDelay → tStartupTime"
  2. Proje güncelleme kontrollistesi: Her FB örneğinde parametre güncellemesi
  3. Alternatif: tStartDelay korunur (deprecated), tStartupTime eklenir — geçiş kolaylaşır
```

## Sık Yapılan Hatalar

### Hata 1: "Use Newest Version" ile Üretim Projesi

```
❌ YANLIŞ: Kütüphane referansı → Version: *
  Kütüphane V1.2'de düzgün çalışıyor.
  Kütüphane V1.3 yüklendi → Proje otomatik güncellendi → Değişen davranış.

✅ DOĞRU: Kütüphane referansı → Version: 1.2.0.0
  Güncelleme bilinçli ve test edilerek yapılır.
```

### Hata 2: Kütüphane Olmadan Projeyi Paylaşmak

```
❌ YANLIŞ: Yalnızca *.project dosyasını göndermek.
  Alıcı yüklü kütüphane olmadan açmaya çalışır → Placeholder uyarısı → Derleme hatası.

✅ DOĞRU: File → Save as Project Archive (*.projectarchive)
  Tüm kütüphaneler içeri gömülü — tek dosya her şeyi içeriyor.
```

### Hata 3: Kütüphane Projesini Test Etmeden Serbest Bırakmak

```
Kütüphane projesinde runtime çalıştırılamaz.
Test için iki yaklaşım:
  1. İki CODESYS IDE aç: biri kütüphane projesi (geliştirme), biri test projesi (runtime)
  2. Kütüphaneyi test projesine ekle, tüm FB'leri test programıyla doğrula
  3. Sonra compile → repository'ye yükle
```

### Hata 4: Namespace Çakışması

```
Projede MyMachineLib.FB_Motor ve VendorLib.FB_Motor ikisi de ekli.
qualified_only olmadan: Derleme hatası — hangisi?

✅ Çözüm: Her kütüphane için ayrı, benzersiz namespace.
  MyMachineLib  → namespace: MyMachine
  VendorLib     → namespace: Vendor
  Kullanım: MyMachine.FB_Motor vs Vendor.FB_Motor — net ayrım.
```

### Hata 5: Kütüphane İçinde Global Değişken Kullanmak

```iecst
(* ❌ YANLIŞ — Kütüphane kendi GVL'sine proje değişkeni yazıyor *)
(* MyMachineLib içindeki GVL_LibStatus: *)
VAR_GLOBAL
    xAnyMotorFault : BOOL;  (* Kütüphane içinden yazılıyor *)
END_VAR
(* Sorun: Kütüphaneyi kullanan her proje bu global'i paylaşır *)
(* İki proje aynı kütüphaneyi kullanırsa ne olur? *)

(* ✅ DOĞRU — Kütüphane sadece VAR_OUTPUT ile iletişir *)
(* Çağıran proje global'lere kendi GVL'sinden yazar *)
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**Kütüphane oluştur:**
- 3+ projede aynı FB kullanılıyorsa
- Ekipten bağımsız olarak dağıtılacaksa
- IP koruması gerekiyorsa
- Standartlaşma ve tutarlılık isteniyor

**Kütüphane oluşturma, proje içinde bırak:**
- Tek projeye özgü, kopyalanmayacak
- Küçük proje, fayda/maliyet oranı düşük
- Hızlı prototip aşaması

## Gerçek Proje Notları

**Not 1 — "Newest Version" Tuzağına Düşme**  
Bir firmanın tüm projeleri `Util, *` (newest) ile çalışıyordu. Util kütüphanesinin bir güncellemesinde FIFO implementasyonu değişti. 5 aktif proje bir gece sonra beklenmedik davranış sergiledi. Tüm projeleri sabit versiyona kilitlemek 2 günlük iş oldu.

**Not 2 — Compiled Library'nin Müşteri İlişkisi Üzerindeki Etkisi**  
Bir OEM müşteriye compiled kütüphane olarak FB_Motor teslim etti. Müşteri kodu göremedi, bakımı OEM'e bağlıydı. Müşteri anlaşma koşullarına itiraz etti. Sonraki projelerde kütüphane açık verildi ancak bakım kontratı imzalandı. IP koruması = compiled, bakım bağımlılığı = sözleşme.

**Not 3 — Library Bağımlılık Çakışması**  
Bir projede iki farklı OEM kütüphanesi aynı anda kullanılıyordu. Her ikisi de `Standard, 3.5.15.0` gerektiriyordu — sorun yok. Sonra OEM_A kütüphanesinin yeni versiyonu `Standard, 3.5.20.0` istedi. OEM_B hâlâ `3.5.15.0` gerektiriyordu. Bağımlılık çakışması: CODESYS ikisini aynı anda çözemedi. Çözüm: OEM_B için placeholder ile doğrudan kopyala-yapıştır yöntemi benimsendi — kütüphane sistemi dışına çıkıldı.

**Not 4 — Kütüphane Geliştirmede İki IDE Yaklaşımı**  
FB_Motor'u kütüphane projesinde geliştirirken test için ayrı bir CODESYS IDE açıldı. Kütüphane projesinde değişiklik → kaydedildi → test projesine reload → test edildi. Bu iki pencereli yaklaşım, geliştirme döngüsünü hızlandırdı.

**Not 5 — Compiled Library'nin Platform/Sürüm Kilidi**  
Bir OEM, `compiled-library` olarak teslim ettiği kütüphanenin yalnızca derlendiği compiler sürümüyle uyumlu olduğunu sahada öğrendi. Müşteri CODESYS'i güncelleyince compiled kütüphane "incompatible compiler version" hatası verdi; kaynak olmadığı için müşteri hiçbir şey yapamadı, OEM'in yeniden derlemesini beklemek zorunda kaldı. Ders: compiled-library, açık kütüphaneden farklı olarak compiler sürümüne sıkı bağlıdır; OEM, desteklenen CODESYS sürümlerini sözleşmede netleştirmeli ve her sürüm için yeniden derleme süreci kurmalı. IP koruması, bakım esnekliğini feda eder.

**Not 6 — Placeholder ve Device-Specific Library Çözümü**  
Bir kütüphane farklı cihazlarda farklı sürümler gerektiriyordu (ARM vs x86 native). Sabit sürüm referansı taşınabilirliği kırdı. Çözüm: **Library Placeholder** kullanıldı — proje soyut bir placeholder'a referans verir, gerçek sürüm device/target tarafından çözülür. Ders: Birden fazla hedef platforma dağıtılan projelerde placeholder, sabit sürümden daha taşınabilirdir; ama "hangi sürüm yüklendi" belirsizliğini de getirir — device-specific çözümleme dikkatle test edilmeli.

**Not 7 — Container Library ile Bağımlılık Paketleme**  
İç içe bağımlılıkları olan bir kütüphane ailesi (MyMachineLib → MyBaseLib → Util) her müşteride eksik bağımlılık hatası veriyordu. Çözüm: bağımlılıkları **container library** içine gömerek tek bir dağıtılabilir paket oluşturuldu. Ders: Karmaşık bağımlılık ağaçları için container library veya `.projectarchive` ile "include all referenced libraries", saha kurulum hatalarını ortadan kaldırır.

## Edge Case'ler ve Sistem Limitleri

### Bağımlılık Çözümleme Edge Case'leri

```
Senaryo                                    Sonuç
─────────────────────────────────────────────────────────────────
İki lib aynı alt-lib'in FARKLI sürümünü ister  Çözülemez → derleme hatası (Not 3)
Lib namespace'i proje GVL ile çakışır          Belirsiz erişim
Compiled lib + farklı compiler sürümü          "incompatible compiler version"
Placeholder çözülemez (target eşleşmez)        Derleme reddedilir veya yanlış sürüm
Açık lib içinde kütüphaneye özel GVL           Tüm projeler global'i paylaşır (Not 5)
Lib MAJOR güncellemesi (API kırılması)         Tüm instance'larda hata (changelog şart)
```

### Versiyon Numaralandırma Tuzakları

```
1.2.3.0 vs 1.2.10.0  → string karşılaştırma yapılırsa 1.2.10 < 1.2.3 sanılabilir
"Use newest" + pre-release → kararsız geliştirme sürümü üretime sızabilir
BUILD numarası farkı → aynı kod sanılır ama derleme farklı olabilir
```

### Kütüphane İçi Global Durum Yasağı

Bir kütüphane kendi `VAR_GLOBAL`'ını yazarsa, o kütüphaneyi kullanan **tüm uygulamalar aynı global'i paylaşır** — iki bağımsız makine kontrolü aynı kütüphaneyi kullanınca durumları çakışır. Kütüphane FB'leri yalnızca kendi instance state'i + VAR_OUTPUT ile iletişmeli; global durum çağırana bırakılmalı.

## Optimizasyon

### Bootapp Boyutu ve Yüklenmeyen Kütüphane

Projeye eklenen ama kullanılmayan kütüphaneler, ölü kod olarak bootapp'ı şişirebilir. CODESYS çoğunlukla kullanılmayan POU'ları eler (tree-shaking), ama büyük CAA aileleri ve initialization kodu yine de yer kaplar. Yalnızca gerçekten kullanılan kütüphaneleri ekleyin; "lazım olur" diye eklenen kütüphaneler kısıtlı cihazlarda (32MB RAM) sorun olur.

### Compiled vs Açık Library: Derleme Süresi

Açık kütüphane (`.library`) her proje derlemesinde kaynak kodu yeniden derlenir; compiled-library önceden derlenmiştir, proje derleme süresini kısaltır. Büyük, kararlı, sık değişmeyen kütüphaneler için compiled-library hem IP korur hem build hızlandırır — ama compiler sürüm kilidi bedeliyle (Not 5).

### Namespace ile Erişim Netliği ve Çakışma Önleme

Her kütüphaneye benzersiz namespace vermek (Library Manager → Properties → Namespace) hem çakışmayı baştan engeller hem de kodda `MyLib.FB_Motor` ile nereden geldiğini netleştirir — büyük projede okunabilirlik ve refactoring güvenliği kazandırır.

## Derin Teknik Detay

### Kütüphane Referansı Neden Kütüphaneyi İçermez?

`.project` dosyası kütüphaneyi değil, ona bir **referansı** (isim, sürüm, namespace) saklar (bkz. fundamentals/02). Bu kasıtlı bir tasarım:
- Aynı kütüphane onlarca projede paylaşılır; her projeye gömmek devasa tekrar olurdu.
- Library Repository merkezi bir önbellektir; referans çözümleme oradan yapılır.
- Bedeli: proje taşınınca kütüphane eksik olabilir → bu yüzden `.projectarchive` (bağımlılıkları paketler) dağıtım için doğru formattır.

Bu, yazılım dünyasındaki "package manifest + dependency cache" (npm/Maven) modeliyle aynı felsefedir: kod değil, çözümlenebilir bir bildirim saklanır.

### Semantik Versiyonlama ve API Sözleşmesi

MAJOR.MINOR.PATCH şeması bir **API sözleşmesidir**: MINOR/PATCH geriye uyumlu olmalı, yalnızca MAJOR kırabilir. CODESYS bunu zorlamaz (otomatik kontrol yok); disiplin geliştiricidedir. Bir FB'nin VAR_INPUT'unu kaldırmak veya yeniden adlandırmak MAJOR değişikliktir — tüm çağıran instance'lar kırılır (Örnek 3). Geçiş kolaylığı için eski parametreyi `deprecated` işaretleyip korumak, yenisini eklemek (genişletme, kırma değil) profesyonel kütüphane bakımının özüdür. Bu, fundamentals/02 ve task-structure'daki "sabit sürüm kilitle" kuralının neden var olduğunun kökü: çünkü sözleşme makine tarafından zorlanmaz.

### Compiled Library ve Compiler Bağımlılığı

Compiled-library, kaynak yerine hedef-bağımsız derlenmiş ara temsil saklar; ama bu ara temsil compiler sürümüne bağlıdır (fundamentals/01'deki "V3 native kod üretir" ile ilişkili). Compiler değişince ara temsil uyumsuz olabilir — açık kütüphane yeniden derlenebildiği için bu sorunu yaşamaz. IP koruması (kaynağı gizleme) ile bakım esnekliği (her sürümde yeniden derlenebilme) arasındaki ödünleşim, compiled-library kararının özüdür.

### Kütüphane Mimarisinin Yeniden Kullanım Ekonomisi

Bir FB'yi kütüphaneye taşımak, fundamentals/02'deki "kütüphane-merkezli mimari" optimizasyonunun somut uygulamasıdır. Ekonomi şudur: tek noktada bug fix → tüm projelere yayılır; tek noktada test → her projede güven; IP koruması → ticari değer. Maliyet: sürüm yönetimi disiplini, dağıtım karmaşıklığı, compiler kilidi. Kütüphaneleştirme kararı (3+ proje kuralı), bu ekonominin maliyet/fayda eşiğidir — eşiğin altında proje-içi FB daha pratiktir.

## İlgili Konular

```
knowledge/codesys/programming/
├── 03_function_blocks.md    → Kütüphaneye girecek FB'lerin tasarımı
└── 01_pou_types.md          → Kütüphanede kullanılan POU tipleri

knowledge/codesys/fundamentals/
└── 02_project_structure.md  → Library Manager nesnesi

knowledge/codesys/advanced/
└── compiled_library_guide.md → Compiled library oluşturma detayları

Kullanışlı kütüphaneler (CODESYS Store):
  Standard.library — Her projede
  Util.library     — FIFO, string, istatistik
  CAA_File         — Dosya sistemi
  OSCAT Basic      — Açık kaynak endüstriyel kontrol bloları
```
