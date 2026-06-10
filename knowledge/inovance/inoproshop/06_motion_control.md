---
KONU        : InoProShop Motion Control (PLCopen / SoftMotion, AM600 + EtherCAT servo)
KATEGORİ    : inovance
ALT_KATEGORI: inoproshop
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.inovance.eu/fileadmin/downloads/Brochures/EN/AM600_Br_EN_Singles_Web_V2.2.pdf"
    başlık: "Inovance — AM600 Motion Controller broşürü (Data code L6210221 V2.2)"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/products/motion-controllers-i/o-modules/am600-motion-controllers"
    başlık: "Inovance EU — AM400/AM600 Motion Controllers ürün sayfası"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20SoftMotion/_sm_example_single_axis_motion_control.html"
    başlık: "CODESYS SoftMotion — Single Axis Motion Control (resmi yardım)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/libs/SM3_Basic/Current/SM3_Basic/POUs/Movement/MC_MoveVelocity.html"
    başlık: "CODESYS SM3_Basic — MC_MoveVelocity (FB) referansı"
    güvenilirlik: resmi
  - url: "https://store.codesys.com/media/n98_media_assets/files/Bundle-SoftMotion/4/CODESYS%20SoftMotion%20SL_en.pdf"
    başlık: "CODESYS SoftMotion SL — Data Sheet (PLCopen MotionControl Part 1 V2.0)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "01_inoproshop_overview.md"
    ilişki: gerektirir
  - konu: "05_ethercat_servo.md"
    ilişki: gerektirir
  - konu: "knowledge/codesys/fundamentals/01_runtime_architecture.md"
    ilişki: gerektirir
  - konu: "devices/INOVANCE_SV660N/datasheet.json"
    ilişki: kullanır
ÖNKOŞUL     :
  - "InoProShop = CODESYS V3 ilişkisi (01_inoproshop_overview.md)"
  - "EtherCAT master/slave ve CiA 402 servo profili temel kavramı"
  - "IEC 61131-3 ST ve Task yapısı (POU, çevrim süresi)"
ÇELİŞKİLER :
  - kaynak: "Pulse (darbe) tabanlı eksen kontrolü beklentisi"
    konu: "AM600'de motion ağırlıkla EtherCAT CiA 402 servo eksenleri üzerinden yürür"
    çözüm: >
      AM600 CPU'sunun 4 grup 200 kHz darbe pozisyonlama çıkışı vardır (datasheet),
      ancak 32 eksenlik senkron/CAM/enterpolasyon mimarisi EtherCAT CiA 402
      eksenleri üzerine kuruludur. Bu belge PLCopen + EtherCAT eksen modelini esas
      alır; darbe-eksen sınırlı/yerel uygulamalar için kullanılır.
---

## Özün Ne

InoProShop'ta hareket kontrolü, **PLCopen Motion Control standardının** (Part 1, V2.0)
CODESYS SoftMotion gerçeklemesi üzerinden yapılır. Uygulama mühendisi, servoyu
doğrudan CiA 402 kontrol/durum kelimeleriyle (6040h/6041h) yönetmek yerine
**MC_ ile başlayan standart fonksiyon bloklarını** (FB) kullanır: `MC_Power`,
`MC_MoveAbsolute`, `MC_MoveVelocity`, `MC_Home`, `MC_Stop`, `MC_Reset` vb. Bu FB'ler
bir **eksen (axis) referansı** alır; eksenin altındaki gerçek donanım, EtherCAT
hattındaki bir SV660N/IS620N gibi CiA 402 servo sürücüsüdür.

Neden önemli: PLCopen, hareketi taşınabilir ve okunabilir kılar. `MC_MoveAbsolute`
mantığı marka/sürücü değişse de aynı kalır; yalnızca eksen konfigürasyonu (ölçek,
limit, EtherCAT eşlemesi) sürücüye özeldir. Bu sayede CODESYS SoftMotion bilen biri,
AM600 üzerinde 32 eksene kadar pozisyonlama, 8 eksen enterpolasyon ve CAM
uygulamalarını standart bir dille kurabilir (kaynak: AM600 broşürü; SoftMotion
veri sayfası).

## Nasıl Çalışır

### PLCopen ↔ SoftMotion ↔ InoProShop ilişkisi

- **InoProShop = CODESYS V3** olduğundan motion altyapısı CODESYS SoftMotion'dur
  (bkz. 01_inoproshop_overview.md). MC_ FB'leri `SM3_Basic` SoftMotion kütüphanesinden
  gelir; Library Manager altında görünür.
- **PLCopen** sadece arayüzü (FB adları, giriş/çıkış semantiği, durum makinesi)
  standartlaştırır. Gerçek hareketi üreten, runtime içindeki SoftMotion çekirdeğidir;
  o da EtherCAT master üzerinden her çevrimde sürücüye hedef üretir.
- **Eksen objesi (axis):** Device tree'de EtherCAT slave (servo) altına eklenen
  `SoftMotion CiA 402 Axis` düğümüdür. FB'lerin `Axis` girişi bu objenin
  `AXIS_REF_SM3` tipindeki global değişkenine bağlanır.

### PLCopen eksen durum makinesi (state machine)

PLCopen motion mantığının kalbi eksen durum makinesidir. Her eksen tek bir durumda olur
ve geçişler FB'lerle tetiklenir. Temel durumlar (PLCopen Part 1 tanımı):

- **Disabled** — eksen enerjisiz; güç (regülatör) kapalı. Başlangıç durumu.
- **Standstill** — eksen enerjili (regülatör açık), durur; hareket komutu kabul eder.
- **Discrete Motion** — sonlu hedefli hareket (örn. `MC_MoveAbsolute`).
- **Continuous Motion** — sonsuz hareket (örn. `MC_MoveVelocity`).
- **Homing** — referanslama (`MC_Home`) sürüyor.
- **Stopping** — `MC_Stop` ile yavaşlatılıyor; bitince Standstill'e döner.
- **ErrorStop** — hata (takip hatası, sürücü arızası, limit) oluştu; tüm hareket
  durur. Bu durumdan **yalnızca `MC_Reset`** ile (hata giderildikten sonra) çıkılır,
  ardından Disabled veya Standstill'e geçilir.

Kritik kural: ErrorStop **her durumdan** girilebilir ve önceliklidir. Bir hata
oluştuğunda hareket FB'leri `CommandAborted` veya `Error` verir; mantığınız bunu
ele almazsa makine sessizce durur.

### Temel fonksiyon blokları

- **MC_Power** — eksene gücü (regülatör/sürücü enable) verir. `Enable`, `bRegulatorOn`,
  `bDriveStart` girişleri TRUE iken `Status` çıkışı TRUE olur ve eksen Standstill'e
  geçer. Diğer hareket FB'lerinin ön koşuludur: MC_Power olmadan eksen Disabled'da kalır
  (kaynak: SoftMotion single-axis örneği).
- **MC_MoveAbsolute** — ekseni mutlak `Position` değerine, verilen `Velocity`,
  `Acceleration`, `Deceleration`, `Jerk` ile götürür. `Execute` yükselen kenarda
  başlar; hedefe varınca `Done` TRUE olur. Discrete Motion durumunda çalışır.
- **MC_MoveVelocity** — sonlu hedef yok; ekseni verilen `Velocity`'de **sürekli**
  döndürür. `Velocity/Acceleration/Deceleration` daima pozitif büyüklüktür; yön
  `Direction` (current/positive/negative) ile verilir. Komut hıza ulaşınca `InVelocity`
  TRUE olur; durdurmak için başka bir FB (örn. `MC_Stop`) gerekir (kaynak: MC_MoveVelocity
  referansı).
- **MC_Home** — referanslama (homing). Mutlak (absolute, multi-turn) enkoderli SV660N/
  IS620N'de çoğu zaman bir kez kalibrasyon yeter; artımlı sistemlerde her güç açılışında
  gerekir.
- **MC_Stop** — kontrollü duruş; eksen Stopping durumuna geçer ve `Execute` TRUE kaldıkça
  yeni hareketi engeller. E-stop yerine geçmez (bkz. emniyet notu).
- **MC_Reset** — ErrorStop'tan çıkış; biriken hatayı temizler. Hata fiziksel olarak
  giderilmeden Reset kalıcı sonuç vermez.

### BufferMode

Hareket FB'leri `BufferMode` ile zincirlenir: `Aborting` (mevcut hareketi kesip yenisine
geç — varsayılan), `Buffered` (mevcut bitince başla), `BlendingLow/High/Previous/Next`
(hız harmanlama). Bir eksen Busy iken yeni FB'yi Aborting dışı modda tetiklemek
genellikle reddedilir (kaynak: MC_MoveVelocity referansı — Busy iken yalnızca Aborting).

## Pratikte Nasıl Kullanılır

### 1. EtherCAT ekseni tanımlama (CiA 402 Axis)

1. Device tree'de **EtherCAT Master** ekle (AM600 EtherCAT portu).
2. Servonun **ESI/XML** dosyasını Device Repository'ye ekle (SV660N/IS620N ESI;
   Inovance destek portalından — datasheet'lere göre `download_url` boş, üreticiden
   temin edilir). Master altına slave olarak ekle.
3. Slave altına **SoftMotion CiA 402 Axis** ekle. InoProShop bu eksen için bir
   `AXIS_REF_SM3` global değişkeni üretir; FB'lerin `Axis` girişine bunu bağla.
4. Çalışma modu: pozisyon eksenleri için **CSP (8)** önerilir (her çevrimde hedef
   pozisyon). Mode of operation 6060h SoftMotion tarafından yönetilir.

### 2. Ölçek / birim (scaling)

- **Birim/devir (units per revolution)** ve **dişli oranı (gear ratio)** eksen
  konfigürasyon sayfasında ayarlanır. Amaç: PLCopen "technical units" (örn. mm, derece)
  ↔ enkoder artımı (increment) dönüşümü.
- SV660N/IS620N **23-bit enkoder** kullanır → tek tur 2^23 = 8.388.608 increment
  (datasheet). Ölçek bu çözünürlük + mekanik (vida hatvesi, redüktör) üzerinden kurulur.
- Yanlış ölçek = yanlış mesafe/hız. İlk devreye almada eksenin "1 birim git" komutuyla
  gerçekte ne kadar gittiğini ölçerek doğrula.

### 3. Limitler

- **Yazılım limitleri (software limits):** eksen konfigürasyonunda min/max pozisyon.
  PLCopen hareketi bu aralıkta tutar.
- **Hız/ivme/jerk dinamik limitleri:** maksimum izinli değerler eksen ayarında
  tanımlanır; FB girişleri bunları aşamaz.
- **Donanım limit anahtarları + e-stop:** yazılım limitinin üstünde, **donanımsal**
  emniyet katmanıdır (bkz. emniyet notu).

### 4. Tipik kullanım sırası (ST)

1. `MC_Power(Enable, bRegulatorOn, bDriveStart)` → `Status` bekle.
2. Gerekiyorsa `MC_Home` → `Done` bekle.
3. `MC_MoveAbsolute` / `MC_MoveVelocity` → hareket.
4. Hata olursa `MC_Reset` → ardından tekrar `MC_Power`.

### 5. Task ataması (AM600, 32 eksen)

- Motion mantığı **hızlı, deterministik bir task**ta koşmalıdır. SoftMotion çevrimi
  EtherCAT senkron çevrimiyle hizalanır.
- AM600 broşür değerleri: 32 eksene kadar PTP (broşür notu: ~4 ms tazeleme),
  16 eksene kadar CAM (broşür notu: ~2 ms senkron periyot), 8 eksene kadar
  enterpolasyon. **[DOĞRULANMAMIŞ — proje bazlı]** kesin çevrim süreleri eksen sayısı,
  CPU yükü ve EtherCAT topolojisine göre değişir; gerçek değerleri InoProShop task
  monitor ile ölçün.
- Mantık (logic) task'ını motion task'ından ayırın: yavaş HMI/Modbus işlerini motion
  çevrimine sokmayın; jitter/aşım (overrun) hareketi bozar.

## Örnekler

Özgün ST örneği — tek eksen: güç ver, referansla, ileri-geri pozisyonla. (Telifli örnek
kod kopyalanmamıştır; bu kendi yazımımdır.)

```iecst
// GVL'de: axDrive : AXIS_REF_SM3;  (CiA 402 Axis objesine bağlı)
PROGRAM PRG_Eksen
VAR
    fbPower    : MC_Power;
    fbHome     : MC_Home;
    fbMoveAbs  : MC_MoveAbsolute;
    fbStop     : MC_Stop;
    fbReset    : MC_Reset;
    eStep      : (S_GUC, S_HOME, S_HAREKET, S_HATA) := S_GUC;
    rHedef     : LREAL := 250.0;   // teknik birim (örn. mm)
    xHataVar   : BOOL;
END_VAR

// Güç bloğu her çevrimde çağrılır (PLCopen FB'leri böyle kullanılır)
fbPower(Axis := axDrive, Enable := TRUE, bRegulatorOn := TRUE, bDriveStart := TRUE);

// Eksen hatası -> hata durumuna kaç (ErrorStop yakalama)
IF axDrive.bError AND eStep <> S_HATA THEN
    eStep := S_HATA;
END_IF

CASE eStep OF
    S_GUC:
        IF fbPower.Status THEN          // eksen Standstill
            fbHome(Axis := axDrive, Execute := TRUE);
            eStep := S_HOME;
        END_IF

    S_HOME:
        fbHome(Axis := axDrive, Execute := TRUE);
        IF fbHome.Done THEN
            fbHome(Axis := axDrive, Execute := FALSE);
            eStep := S_HAREKET;
        END_IF

    S_HAREKET:
        fbMoveAbs(Axis := axDrive, Execute := TRUE,
                  Position := rHedef, Velocity := 100.0,
                  Acceleration := 500.0, Deceleration := 500.0, Jerk := 1000.0);
        IF fbMoveAbs.Done THEN
            fbMoveAbs(Axis := axDrive, Execute := FALSE);
            // hedefi değiştir, döngüle...
        END_IF

    S_HATA:
        // Önce kontrollü dur, fiziksel sebep giderilince resetle
        fbStop(Axis := axDrive, Execute := TRUE, Deceleration := 1000.0);
        fbReset(Axis := axDrive, Execute := NOT xHataVar);
        IF fbReset.Done THEN
            fbReset(Axis := axDrive, Execute := FALSE);
            fbStop(Axis := axDrive, Execute := FALSE);
            eStep := S_GUC;             // güçten yeniden başla
        END_IF
END_CASE
```

Sürekli hareket örneği (`MC_MoveVelocity`): konveyör gibi sonsuz dönüşte ekseni sabit
hızda çevirip yalnızca `MC_Stop` ile durdurursunuz; `MC_MoveVelocity.InVelocity`
hıza ulaşıldığını bildirir.

## Sık Yapılan Hatalar

- **MC_Power'ı tek seferlik çağırmak.** PLCopen FB'leri her çevrim çağrılmalı; aksi
  halde `Status` ve durum geçişleri güncellenmez.
- **`Execute`'i FALSE'a çekmeyi unutmak.** `Done` görüldükten sonra `Execute := FALSE`
  yapılmazsa bir sonraki yükselen kenar oluşmaz; hareket tekrarlanmaz.
- **Ölçek doğrulamasını atlamak.** 23-bit enkoder + dişli oranı yanlış girilirse eksen
  "100 mm" yerine bambaşka mesafe gider. İlk işte fiziksel ölçümle teyit et.
- **Motion'ı yavaş task'a koymak.** HMI/Modbus ile aynı yavaş task'ta jitter hareketi
  bozar; ayrı hızlı/senkron motion task kullan.
- **ErrorStop'u ele almamak.** Eksen sessizce durur ve "neden hareket etmiyor"
  yaşanır. `axis.bError`/FB `Error` çıkışını izle, `MC_Reset` akışı kur.
- **MC_Stop'u e-stop sanmak.** MC_Stop yazılımsal, kontrollü duruştur; güvenlik
  fonksiyonu değildir (aşağıya bakın).

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih (PLCopen + EtherCAT eksen):** Çok eksenli senkron hareket, pozisyonlama,
  enterpolasyon, CAM/elektronik dişli; SV660N/IS620N gibi CiA 402 servolarla. AM600'ün
  asıl güçlü olduğu alan.
- **Etme / sınırla:** Tek, basit, açık çevrim bir step/darbe ekseni gerekiyorsa AM600'ün
  200 kHz darbe çıkışı yeterli olabilir; tam SoftMotion eksen mimarisi gereksiz yük
  olur. EtherCAT olmayan, çok düşük maliyetli mikro uygulamalar için orta-sınıf motion
  kontrolör aşırı çözüm olabilir.

## Gerçek Proje Notları

- **Emniyet — e-stop donanımsaldır (kritik):** Acil durdurma, PLCopen `MC_Stop` veya
  yazılım limitleriyle **sağlanmaz**. E-stop, sürücünün **STO (Safe Torque Off)** girişi
  ve emniyet rölesi/güvenlik kontrolörü ile **donanımsal** kurulmalıdır. SV660N'de STO,
  CN6 üzerinde çift kanallı izole giriştir (-FS modeli; datasheet). Yazılım yalnızca
  STO sonrası temiz toparlanma (eksen ErrorStop → MC_Reset → MC_Power) sağlar.
  Bu ilke knowledge tabanındaki emniyet yaklaşımıyla uyumludur: güvenlik fonksiyonu
  standart PLC mantığına emanet edilmez.
- **Takip hatası (following error):** Yetersiz tuning, fazla ivme/hız veya mekanik
  takılmada sürücü "excessive position deviation" verir → eksen ErrorStop. Çözüm:
  ivme/hız profilini gerçekçi tut, sürücü kazançlarını (InoDriverShop/InoServoShop ile)
  ayarla, jerk vererek geçişleri yumuşat.
- **Jerk/ivme ayarı:** Sıfır jerk = trapez profil = sert geçiş, mekanik şok ve titreşim.
  Sonlu jerk (S-curve) parça/yük üzerindeki şoku azaltır ama hareketi uzatır. Hassas
  veya kırılgan yüklerde jerk sınırla; çevrim süresi kritikse jerk'i gevşet.
- **Referanslama (homing):** SV660N/IS620N **mutlak multi-turn enkoderlidir**; pil
  yedeği ile pozisyon güç kesilse de korunur → çoğu uygulamada bir kez homing yeter.
  Pil/enkoder verisi kaybolursa yeniden referanslama gerekir; üretimde "ilk açılışta
  homing zorunlu mu" kararını bu davranışa göre ver.
- **E-stop ↔ motion ilişkisi:** STO devreye girince eksen torksuz kalır → eksen
  ErrorStop'a düşer. Operatör reset sırasında ekseni güvenli pozisyona almak gerekebilir;
  dikey/yer çekimi yükü olan eksenlerde STO sırasında düşmeyi önlemek için
  **mekanik fren** (servo motor freni) şarttır — yazılım bunu telafi edemez.
- **Eksen sayısı/çevrim teyidi:** Broşürdeki 32/16/8 eksen ve çevrim süreleri tavan
  değerlerdir. Gerçek projede InoProShop task monitor ile EtherCAT çevrim aşımı (cycle
  overrun) ve CPU yükünü ölçün; aşım varsa eksen yükünü/çevrimi yeniden boyutlandırın.

## İlgili Konular

- `01_inoproshop_overview.md` — InoProShop = CODESYS V3 tabanı
- `05_ethercat_servo.md` — EtherCAT master, CiA 402 servo eşleme, ESI yönetimi
- `devices/INOVANCE_SV660N/datasheet.json` — SV660N servo (STO, CiA 402 objeleri)
- `devices/INOVANCE_IS620N/datasheet.json` — IS620N servo
- `devices/INOVANCE_AM600/datasheet.json` — AM600 motion kontrolör sınırları
- `knowledge/codesys/fundamentals/` — task yapısı, runtime (motion task için taban)
