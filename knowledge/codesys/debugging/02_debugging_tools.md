---
KONU        : CODESYS Dahili Debug Araçları
KATEGORİ    : codesys
ALT_KATEGORI: debugging
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_using_breakpoints.html"
    başlık: "CODESYS Online Help — Using Breakpoints"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_forcing_values.html"
    başlık: "CODESYS Online Help — Forcing and Writing of Variables"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_monitoring_running_tasks.html"
    başlık: "CODESYS Online Help — Monitoring Tasks"
    güvenilirlik: resmi
  - url: "https://www.realpars.com/blog/codesys-traces"
    başlık: "RealPars — Mastering Traces in CODESYS"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_common_errors.md"
    ilişki: tamamlar
  - konu: "03_performance_analysis.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/task-structure/02_cycle_time.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "CODESYS online bağlantısı kurulmuş (01_common_errors.md)"
  - "Temel POU ve task yapısı (fundamentals/02_project_structure.md)"
ÇELİŞKİLER :
  - kaynak: "Breakpoint ve çok task'lı sistemler"
    konu: "Breakpoint çok task'lı sistemlerde diğer task'ları da durdurur"
    çözüm: >
      Tek bir task'ta breakpoint tetiklenince tüm task'lar durur.
      Bu, üretim makinelerinde anlık durma anlamına gelir.
      Breakpoint yalnızca güvenli test ortamında veya simülasyonda kullanılmalı.
      Üretimde canlı debug için Watch Window ve Trace tercih edilmeli.
  - kaynak: "Force Values güvenlik riski"
    konu: "Force values üretim ortamında beklenmedik makine hareketi yaratabilir"
    çözüm: >
      Force values kullanmadan önce makineyi güvenli konuma getir.
      Safety interlock'ları geçersiz kılabileceğini unutma.
      Force sonrası Unforce yapmayı unutmak yaygın hatadır —
      session sonunda "Watch All Forces" ile kontrol et.
---

## Özün Ne

CODESYS, PLC programı canlı çalışırken içine bakmanı sağlayan kapsamlı bir debug araç seti sunar. Breakpoint ile programı belirli bir noktada durdurabilirsin; Watch Window ile onlarca değişkeni aynı anda izleyebilirsin; Force Values ile I/O çıkışlarını zorla test edebilirsin; Trace Recorder ile saniyeler boyunca her döngünün değerini kaydedebilirsin; Online Change ile çalışan programı durdurmadan güncelleyebilirsin. Bu araçların her birinin doğru bağlamı ve sınırları vardır — yanlış bağlamda kullanılan araç sorunu çözmek yerine yeni sorun yaratır.

## Nasıl Çalışır

### Online Mode — Debug'ın Ön Koşulu

Tüm debug araçları **Online Mode**'da çalışır. Online mode = IDE'nin çalışan runtime'a bağlı olduğu durum.

```
Online → Login (proje indirilir ve çalışmaya başlar)
Online → Start  (program çalışır)
Online → Stop   (program durur, çıkışlar son değerde)
Online → Logout (bağlantı kesilir)

Renk göstergesi:
  Yeşil  : Running — program çalışıyor
  Sarı   : Stopped — program durdu (breakpoint veya Stop)
  Kırmızı: Exception / Fault
```

---

## Araç 1: Watch Window (Değişken İzleme)

**Ne Yapar:** Seçilen değişkenleri canlı olarak gösterir. IDE polling yaparak değerleri günceller — her 200-500ms'de bir yenilenir (monitoring interval'a bağlı).

### Watch Window Açma

```
View → Watch → Watch 1 (veya Watch 2, Watch 3, Watch 4)
```

Watch Window birden fazla açılabilir: Watch 1 I/O değerleri için, Watch 2 alarm durumları için, Watch 3 timer değerleri için.

### Değişken Ekleme

```
Yöntem 1: Watch penceresine değişken ismini yaz
  → GVL_IO.xMotorRun [Enter]
  
Yöntem 2: Editörde değişkene sağ tıkla → "Add Watch"

Yöntem 3: Drag & drop — editörden Watch Window'a sürükle
```

### Düzenleme — Write Value

Watch Window'da bir değişkeni seçip değer yazabilirsin (Force değil, Write):

```
Değişken satırına çift tıkla → Yeni değer gir → Enter
Veya: Sağ tıkla → "Prepare Value" → değeri hazırla → "Write Values" (Ctrl+F7)

Fark:
  Write  : Bir döngü boyunca değişkene değer yazar → program bir sonraki
            döngüde üzerine yazabilir.
  Force  : Program üzerine yazmaz — sabitledi.
```

### Watch Window Örneği

```
Değişken                  | Değer    | Tip   | Hazır
──────────────────────────|──────────|───────|─────────
GVL_IO.xMotorRun          | TRUE     | BOOL  |
GVL_IO.rTemperature       | 82.5     | REAL  |
GVL_State.eSystemState    | eRunning | ENUM  |
GVL_Params.rSpeedSetpoint | 45.0     | REAL  | 60.0 ← Yeni değer hazır
fbMotor1.tTotalRunTime    | T#4H23M  | TIME  |
GVL_Alarms.xAnyAlarm      | FALSE    | BOOL  |
```

### Monitoring Interval Ayarı

```
Tools → Options → Device → Monitoring → Update Interval
Varsayılan: 200ms
Hızlı değişen sinyaller için: 100ms
Yavaş sistemler için: 500ms-1000ms
```

---

## Araç 2: Force Values (Değer Zorlama)

**Ne Yapar:** Bir değişkeni, program ne yazarsa yazsın, belirlenen değerde sabit tutar. Program kodu çalışmaya devam eder ama o değişkene yazma etkisi olmaz.

### Force Nasıl Yapılır

```
Adım 1: Watch Window'da değişkeni seç.
Adım 2: Sağ tıkla → "Force Values" → değeri gir.
Adım 3: F7 veya Debug → Force Values.
        Değişkenin önünde kilit ikonu belirir.

Klavye kısayolları:
  F7     → Force selected
  Ctrl+F7 → Write Values (Force değil, tek seferlik yaz)
  Shift+F7 → Unforce selected
```

### Force Uygulamaları

```
Test senaryosu 1 — Dijital çıkış testi:
  xMotorRun := TRUE (Force)
  Motor gerçekten çalışıyor mu? → Sahadan gözlem.
  xMotorRun := FALSE (Force) → Motor duruyor mu?
  Çıkış ve kablo testi tamamlandı.

Test senaryosu 2 — Alarm simülasyonu:
  GVL_Alarms.xTempOverRange := TRUE (Force)
  Alarm yönetim kodu doğru tepki veriyor mu? → Gözlem.
  Unforce → Normal operasyon.

Test senaryosu 3 — HMI olmadan parametreyi test etme:
  GVL_Params.rSpeedSetpoint := 75.0 (Force)
  Sistem 75'e adapte oluyor mu? → Gözlem.
```

### Force Güvenliği

```
⚠ ÜRETİM ORTAMINDA DİKKAT:

Force values, safety interlock'ları geçersiz kılabilir.
xEmergencyStop := FALSE (Force) → Acil durdurma devre dışı!

Kural 1: Force öncesi makineyi güvenli konuma al.
Kural 2: Force session sonunda mutlaka kaldırılmalı.
Kural 3: Session sonunda kontrol et:
  View → Watch → Watch All Forces
  Listede bir şey varsa → Unforce All.
```

### Watch All Forces

```
View → Watch → Watch All Forces
```

Tüm aktif force değerlerini tek yerde listeler. Session kapatılmadan önce bu pencere mutlaka kontrol edilmelidir.

---

## Araç 3: Breakpoint (Duraklatma Noktası)

**Ne Yapar:** Program belirli bir satıra ulaştığında tüm task'ları durdurur. Değişken değerlerini dondurulmuş halde incelemeye izin verir.

### Breakpoint Türleri

```
1. Satır Breakpoint (Line Breakpoint):
   Belirli bir satıra ulaşınca dur.
   Kısayol: F9 (imleç o satırdayken)
   
2. Veri Breakpoint (Data Breakpoint):
   Belirli bir değişkenin değeri değişince dur.
   Debug → New Data Breakpoint → değişken adını gir.
   NOT: Yalnızca CODESYS Control Win V3'te desteklenir.
   
3. Koşullu Breakpoint (Conditional Breakpoint):
   Koşul TRUE olduğunda tetiklenir.
   Breakpoint sağ tıkla → Condition → "xFaultActive = TRUE"
```

### Breakpoint Sonrası Navigasyon

```
Program Breakpoint'te durdu:
  F5  → Continue (devam et)
  F10 → Step Over (mevcut satırı çalıştır, içine girme)
  F11 → Step Into (fonksiyon çağrısına gir)
  Shift+F11 → Step Out (mevcut fonksiyondan çık)
  Shift+F5 → Stop debugging
```

### Data Breakpoint — Bellek Üzerine Yazma Tespiti

En güçlü debug tekniklerinden biri: Beklenmedik değer değişikliğini bul.

```iecst
(* Örnek: iNumber değişkeni beklenmedik şekilde değişiyor *)
PROGRAM PLC_PRG
VAR
    Idx : INT;
    Ary : ARRAY[0..3] OF BYTE;
    iNumber : INT := 55;
END_VAR

(* Hatalı kod: Array sınırını aşıyor *)
FOR Idx := 0 TO 6 DO   (* 0-3 arasında olmalı, 0-6 yazıyor! *)
    Ary[Idx] := 0;
END_FOR
```

```
Debug → New Data Breakpoint → "PLC_PRG.iNumber"
Program çalıştır → Breakpoint tetiklenir →
  "Memory of PLC_PRG.iNumber was modified at: Idx = 7"
Sorun: Array[7] = iNumber'ın bellek adresi.
```

### Breakpoint Kullanım Kısıtları

```
⚠ Dikkat:
  - Breakpoint tüm task'ları dondurur (güvenlik riski)
  - I/O çıkışlar son değerlerinde kalır
  - Fieldbus sync kaçırılır (EtherCAT hata verebilir)
  - Timer ve TON blokları donmuş sayar devam edemez
  
Uygun kullanım: Simülasyon, geliştirme ortamı, PC'de test
Uygun değil: Canlı üretim makinesi, EtherCAT motion control
```

---

## Araç 4: Trace Recorder (Sinyal Kaydedici)

**Ne Yapar:** PLC içinde çalışan bir ring buffer. Her döngüde seçilen değişkenlerin değerini kaydeder. Runtime'a bağlı olsanız da olmasanız da kayıt devam eder. IDE'ye bağlandığınızda kaydı upload ederek geçmişe bakabilirsiniz.

### Trace Nasıl Oluşturulur

```
Adım 1: Application → Add Object → Trace
        İsim: Trace_SpeedAnalysis

Adım 2: Trace editöründe değişken ekle:
  Variables sekmesi → Add variable → GVL_IO.rMotorSpeed
  Variables sekmesi → Add variable → GVL_IO.rMotorCurrent
  Variables sekmesi → Add variable → GVL_Alarms.xMotorFault

Adım 3: Trace ayarları:
  Task      : Task_Control (hangi task döngüsünde kayıt)
  Buffer size: 1000 (kayıt edilen döngü sayısı)
  Records   : Every cycle (her döngüde kayıt)
  
Adım 4: Trigger ayarı (opsiyonel):
  Trigger variable: GVL_Alarms.xMotorFault
  Trigger edge    : Rising Edge (yükselen kenarda tetikle)
  Pre-trigger     : 100 (tetikten 100 döngü önce de kaydet)
  Post-trigger    : 200 (tetikten sonra 200 döngü kaydet)

Adım 5: Online → Login → Trace otomatik başlar.
```

### Trace Analizi

```
Online modda:
  Trace editörü → Grafik görünüm → Canlı sinyal
  
Offline analiz:
  Trace → Upload → Kaydedilmiş veriyi al
  Zaman ekseninde değerleri incele
  Zoom in/out → Detay inceleme
  Cursor ile iki nokta arası Δt ölç
```

### Trace Trigger Senaryosu — Arıza Öncesi Ne Oldu?

```
Senaryo: Motor arızası oluşuyor ama nedeni bilinmiyor.

Trace konfigürasyonu:
  Variables: rMotorSpeed, rMotorCurrent, rTemperature, xMotorFault
  Trigger: xMotorFault rising edge
  Pre-trigger: 500 döngü (10ms task → 5 saniye öncesi)
  Post-trigger: 100 döngü
  
Arıza tetiklenince trace durur.
Upload et → Grafiği incele:
  "Arızadan 2 saniye önce akım %30 arttı, sıcaklık yükseldi"
  → Termik aşırı yük — motor aşırı yükleniyor.
```

### Trace vs Watch Window Karşılaştırması

```
Watch Window:
  ✓ Kurulumu kolay, anlık değer
  ✗ Geçmiş yok (200ms polling — hızlı geçişler kaçar)
  
Trace:
  ✓ Her döngü kaydedilir — hiçbir değer kaçmaz
  ✓ Trigger ile olayı yakalama
  ✓ Runtime'a bağlı olmak zorunda değilsin
  ✗ Kurulumu biraz daha uzun

Kullanım:
  Watch Window: Hızlı durum kontrolü, genel izleme
  Trace: Intermittent arıza, olayı kaçırmama, arıza öncesi analiz
```

---

## Araç 5: Online Change (Çalışırken Güncelleme)

**Ne Yapar:** Çalışan programı durdurmadan küçük kod değişikliklerini yükler. Kritik üretim süreçlerinde makineyi durdurmadan hata düzeltmek için kullanılır.

### Online Change Nasıl Yapılır

```
Adım 1: Online Login (zaten bağlısın ve program çalışıyor).
Adım 2: Kodu düzenle (POU'yu aç, değişikliği yap).
Adım 3: Build → Compile (değişiklikler derlenir).
Adım 4: Online → Login tekrar → "Online Change" sorusu çıkar.
         "Yes" → Değişiklik yüklenir, program devam eder.
```

### Online Change Neyi Değiştirebilir, Neyi Değiştiremez

```
Online Change İLE yapılabilir:
  ✓ POU implementasyonunu değiştirme (kodun içi)
  ✓ Sabit değerleri güncelleme
  ✓ IF koşullarını düzenleme
  ✓ Yorum ekleme/silme
  
Online Change İLE YAPILAMAMAZ:
  ✗ Yeni değişken ekleme/silme (interface değişikliği)
  ✗ Yeni POU oluşturma
  ✗ GVL'ye değişken ekleme
  ✗ Task yapılandırması değiştirme
  ✗ Library ekleme/silme
  ✗ I/O Mapping değiştirme
  → Bu durumlarda tam download gerekir (makine durur)
```

### Online Change Riskleri

```
Risk 1 — Değişken durumları:
  Online change sırasında çalışan POU'nun yerel değişkenleri
  sıfırlanabilir. Timer, sayaç gibi durum tutan değişkenler etkilenir.
  
Risk 2 — SFC adım durumu:
  SFC (Sequential Function Chart) içeren POU'da online change
  mevcut adımı sıfırlayabilir → Makine beklenmedik konuma gidebilir.
  
Risk 3 — Boyutu aşan değişiklik:
  Çok fazla değişiklik online change limitini aşabilir → Tam download gerekir.

Kural:
  Küçük, izole düzeltmeler → Online Change
  Büyük yeniden yapılanma → Planlı makine durdurma + tam download
```

---

## Araç 6: Log Viewer (Log Görüntüleyici)

**Ne Yapar:** Runtime'ın ürettiği tüm mesajları — hatalar, uyarılar, bilgiler — zaman damgalı olarak görüntüler.

### Log Viewer Erişimi

```
Device (çift tık) → Log sekmesi
Veya: View → Log
```

### Log Seviyeleri

```
🔴 Exception : Kritik hata (uygulama durdu, watchdog vb.)
🟠 Error     : Hata (download başarısız, I/O hata)
🟡 Warning   : Uyarı (versiyon uyumsuzluğu, eksik bileşen)
🔵 Info      : Bilgi (uygulama başladı, bağlantı kuruldu)
⚪ Debug     : Ayrıntılı geliştirici mesajları (genellikle gizli)
```

### Log'u Okuma Stratejisi

```
İyi bir log okuma sırası:
  1. Son hata mesajını bul (En üstteki/son zaman damgalı Exception)
  2. O mesajdan 2-3 satır üste çık → Neyin önce olduğuna bak
  3. "Component" alanını oku → CmpApp (uygulama), CmpSched (zamanlayıcı)
  
Örnek log:
  [09:15:32] INFO  | CmpApp    | Application 'Application' started
  [09:15:35] INFO  | CmpApp    | Download started
  [09:15:36] ERROR | CmpApp    | EXCEPTION [GlobalInit]: AccessViolation
  [09:15:36] ERROR | CmpApp    | Download failed
  
  Okuma: GlobalInit sırasında AccessViolation → Pointer veya array sınır sorunu.
```

### Programdan Log'a Yazma

```iecst
(* IEC kodundan log mesajı gönderme — Util kütüphanesi gerekir *)
VAR
    fbLogMsg : CmpLog.FB_LogMessage;
END_VAR

fbLogMsg(
    sMessage  := CONCAT('Motor fault: ', sFaultMsg),
    iClass    := CmpLog.LOG_WARNING,
    sComponent:= 'FB_Motor'
);

(* Log'da görünür:
   [10:22:15] WARNING | FB_Motor | Motor fault: Feedback timeout *)
```

---

## Araç 7: PLC Shell — Komut Satırı

**Ne Yapar:** Runtime'a doğrudan komut gönderme arayüzü. Yük bilgisi, versiyon, IRQ durumu gibi düşük seviye bilgilere erişim.

### PLC Shell Erişimi

```
Online Login → Device → PLC Shell sekmesi
```

### Sık Kullanılan Komutlar

```bash
# Runtime versiyonu
> version
CODESYS Control for Linux ARM64 SL V4.10.0.0

# CPU yükü
> plcload
PLC Load: 47%

# Uygulama bilgisi
> app info Application

# Ağ arayüzleri
> ifconfig

# IRQ listesi ve öncelikleri (Linux)
> irq-list

# IRQ önceliğini değiştir
> irq-set-prio 2 80

# RT kernel kullanılıyor mu?
> rt-get kernelinfo

# Tüm task'ların durumu
> task list

# Log temizle
> log clear
```

---

## Debug Senaryoları — Uçtan Uca

### Senaryo 1: Değişken Beklenmedik Şekilde Değişiyor

```
Problem: Motor hız setpoint'i zaman zaman 0'a düşüyor.
         Kim yazıyor, ne zaman?

Çözüm Adımları:
1. Watch Window: GVL_Params.rSpeedSetpoint ekle → Değeri izle.
2. Data Breakpoint: "GVL_Params.rSpeedSetpoint" için kur.
   (Debug → New Data Breakpoint)
3. Program çalıştır → Breakpoint tetiklenir → Call Stack'e bak.
   Call Stack: PRG_HMIUpdate → rSpeedSetpoint := 0
4. PRG_HMIUpdate'e git → "0 ataması" neden yapılıyor?
5. Hatalı koşul bulundu → Düzelt → Online Change.
```

### Senaryo 2: Intermittent Alarm — Ne Tetikliyor?

```
Problem: Sıcaklık alarmı bazen günde bir kez çalıyor.
         Nedeni bilinemiyor.

Çözüm Adımları:
1. Trace kur:
   Variables: rTemperature, rTemperatureFiltered, xTempAlarm
   Trigger: xTempAlarm rising edge
   Pre-trigger: 500 döngü (10ms task → 5 saniye)
   
2. Alarm bir sonraki tetiklendiğinde trace durur.
3. Upload → Grafiği incele.
4. Sonuç: rTemperature'ün filtrelenmemiş değeri anlık 95°C'ye çıkıyor
           (sensör spike), rTemperatureFiltered normal.
5. Alarm filtreli değere bağlandı → Sorun giderildi.
```

### Senaryo 3: Motor Komutu Gitmiyor

```
Problem: HMI'dan start komutu veriliyor ama motor çalışmıyor.
         Motor kontaktörü enerjilemiyor.

Çözüm Adımları:
1. Watch Window: GVL_IO.xMotorRun ekle → FALSE mı?
2. Watch Window: GVL_HMI.xStartCmd ekle → TRUE geldi mi?
3. Watch Window: fbMotor1.eState → Hangi durumda?
4. Watch Window: fbMotor1.xFault → Arıza var mı?
5. Watch Window: fbMotor1.xRunOutput → FB çıkışı TRUE mu?

Tıkandığı yer: GVL_IO.xMotorRun FALSE ama fbMotor1.xRunOutput TRUE.
→ I/O Mapping kontrol et: xMotorRun doğru çıkışa bağlı mı?
→ I/O Mapping'de çift tıkla → Offset ve değişken bağlantısı yanlış.
Düzelt → Test.
```

## Sık Yapılan Hata Ayıklama Hataları

### Hata 1: Force'u Unforce Etmeyi Unutmak

```
Senaryo: Test için xConveyorRun := TRUE force edildi.
         Test bitti, force kaldırılmadı.
         Operatör makineyi durdurdu → HMI stop komutu gönderdi →
         ama konveyör durmadı! Force hâlâ aktif.
         
Çözüm: Her debug session sonunda View → Watch → Watch All Forces kontrol.
```

### Hata 2: Breakpoint'i Üretim Makinesinde Bırakmak

```
Senaryo: Sahada test yapılırken breakpoint konuldu.
         Test bitti, breakpoint kaldırılmadı.
         Ertesi gün program belirli koşulda durdu.
         Operatör panikle aradı.
         
Çözüm: Debug → Delete All Breakpoints. Session sonunda rutin.
```

### Hata 3: Trace Buffer'ını Küçük Tutmak

```
Senaryo: Trace 50 döngü buffer ile kuruldu.
         Arıza tetiklendiğinde trace 0.5 saniye önceye bakabiliyor.
         Sorun 3 saniye önceden başlıyordu → Kayıp.
         
Çözüm: Buffer size = gerekli süre / cycle time
         5 saniye, 10ms task → 500 döngü buffer gerekir.
```

### Hata 4: Watch Window'u Monitoring Interval'ı Anlamadan Kullanmak

```
Senaryo: 1ms'de değişen bir sinyal Watch Window'da "stabil" görünüyor.
         Watch Window 200ms'de bir güncellendiği için anlık değişikliği kaçırıyor.
         
Çözüm: Hızlı değişen sinyaller için Trace kullan — her döngü kaydeder.
        Watch Window günlük izleme ve genel durum için idealdir.
```

## Ne Zaman Hangi Aracı Kullan

```
Araç            | Ne Zaman Kullan                          | Ne Zaman Kullanma
────────────────|──────────────────────────────────────────|──────────────────────
Watch Window    | Anlık değer kontrolü, genel izleme       | Hızlı sinyal geçişleri
Force Values    | I/O testi, alarm simülasyonu             | Safety kritik üretimde
Breakpoint      | Kod akışı debug, veri üzerine yazma tespiti | Canlı üretim makinesi
Trace           | Intermittent arıza, arıza öncesi analiz  | Basit durum kontrolü
Online Change   | Küçük hata düzeltme, interface değişmeden | Büyük refactoring
PLC Shell       | CPU yük, IRQ, versiyon, sistem bilgisi   | Kod debug (bu araç değil)
Log Viewer      | Her hata için — ilk bakış                | Hiçbir zaman atla
```

## Gerçek Proje Notları

**Not 1 — Trace ile 3 Günlük Arıza Çözüldü**  
Bir dolum makinesi haftada 2-3 kez beklenmedik dururdu. Nedeni bulunamıyordu; tamamen rastgele görünüyordu. Trace kuruldu: 8 değişken, 1000 döngü buffer, xEmergencyStop rising edge trigger. Bir sonraki durmada trace upload edildi. Grafik netleşti: Durumdan 1.2 saniye önce rPressure değeri 2 bar sınırını aşıyordu — sensör dalga yapıyor. Sensör kalibrasyonu bozuktu. Sensor değiştirildi, sorun bitti.

**Not 2 — Data Breakpoint ile 4 Saatlik Debug'ı 20 Dakikaya İndirme**  
Bir proje değişken değişkeninin nasıl bozulduğunu anlayamıyordu. `wProductionCount` zaman zaman 0'a dönüyordu. Beş farklı POU aynı değişkeni yazan şüpheliydı. Data Breakpoint: `GVL_Diagnostics.wProductionCount`. 3. çalışmada tetiklendi. Call Stack: `PRG_ModbusUpdate → wProductionCount := 0`. Modbus holding register write kodu üzerine yazıyordu. Düzeltme: 10 dakika. Toplam debug: 20 dakika.

**Not 3 — Online Change'in Kurtardığı Devreye Alma**  
Müşteri tesisinde devreye alma günü PLC programında küçük ama kritik bir mantık hatası bulundu. Makineyi durdurmak 2 saatlik üretim kaybı demekti. Hata yalnızca bir IF koşulundaydı — interface değişmiyordu. Online Change uygulandı, program 3 saniye durmadan güncellendi. Üretim devam etti.

**Not 4 — Force Sonrası Makine Hareketi**  
Bir servo motor testi sırasında `xServoEnable := TRUE` force edildi. Ama bir önceki test sırasında position referans değeri sıfırlanmamıştı. Motor enable olunca 50mm hızlı hareket yaptı. Beklenmedik hareket çevre ekipmanına çarptı. Ders: Force öncesi güvenli durumu doğrula; hareket sistemlerinde force öncesi tüm pozisyon/referans değerlerini kontrol et.

**Not 5 — Breakpoint EtherCAT'i Düşürdü**  
Canlı bir motion sisteminde "sadece bir bakayım" diye breakpoint kondu. Program durunca tüm task'lar dondu, EtherCAT bus cycle task çalışmadı → master sync sinyali kesildi → tüm slave'ler SafeOp'a düştü → servo'lar serbest kaldı, eksen yer çekimiyle düştü. Ders: Breakpoint tüm task'ları durdurur ve fieldbus sync'i öldürür; motion/EtherCAT canlı sistemde ASLA breakpoint — Trace kullan (durdurmaz). Geliştirme/simülasyon için saklı tut.

**Not 6 — Watch Window'un Yanılttığı Hızlı Sinyal**  
Bir mühendis 1ms'de değişen bir bayrağı Watch Window'da izledi, "hiç TRUE olmuyor" sonucuna vardı ve mantığı yanlış değiştirdi. Gerçekte bayrak her 1ms TRUE oluyordu ama Watch Window 200ms polling yapıyordu — 200 değişimde 1'ini gösteriyordu. Ders: Watch Window monitoring interval'inden (200ms) hızlı değişen sinyalleri güvenilir gösteremez; bu sinyaller Trace ile (her döngü kayıt) izlenmeli. Watch Window "anlık fotoğraf", Trace "film".

**Not 7 — Online Change SFC Adımını Sıfırladı**  
Çalışan bir dolum sekansında (SFC) küçük bir aksiyon kodu Online Change ile düzeltildi. Değişiklik sonrası SFC mevcut adımı kaybetti, başa döndü — makine dolum ortasındayken valfi kapatıp baştan başladı, ürün taştı. Ders: SFC içeren POU'da Online Change mevcut adım durumunu sıfırlayabilir; sekans-kritik makinelerde SFC değişikliği için planlı duruş + güvenli durumdan başlatma tercih edilmeli (programming/03 + bu belge Online Change riskleri).

## Edge Case'ler ve Araç Sınırları

### Her Aracın Görünmez Sınırı

```
Araç           Gizli Sınır                          Sonuç
─────────────────────────────────────────────────────────────────────
Watch Window   200ms polling                        hızlı sinyal kaçar (Not 6)
Force          unforce unutulur                      zombi force (stop çalışmaz)
Breakpoint     TÜM task'ları durdurur               EtherCAT düşer (Not 5)
Data Breakpoint yalnız Control Win V3                gerçek donanımda yok
Trace          buffer sonlu                          küçük buffer → olay kaçar
Online Change  interface/SFC/retain değişimini reddeder tam download gerekir
PLC Shell      komut platforma göre değişir          ARM'de bazı komut yok
Log            bazı sorunlar log'a yazılmaz          sessiz hata (01 edge cases)
```

### Force vs Write: Sık Karıştırılan Ayrım

```
Write (Ctrl+F7): değişkene BİR döngü değer yazar → program bir sonraki scan EZER
Force (F7):      değişkeni KİLİTLER → program yazsa da değer sabit kalır
```

Edge case: bir output'u Write ile test edip "değişmedi" sanmak — program zaten bir sonraki scan'de üzerine yazmıştır. Kalıcı test için Force gerekir. Ama Force unutulursa zombi (Not / Hata 1). İkisinin farkını bilmemek en yaygın araç hatasıdır.

### Trace'in Yakalayamadıkları

```
- Buffer'dan eski olaylar: ring buffer dolunca en eski üzerine yazılır
- Trigger'dan önce çok geride olan kök neden: pre-trigger yetmezse görünmez
- Task cycle'ından hızlı değişim: Trace task cycle'da örnekler, ara değişimi görmez
- Trace'in kendi yükü: çok değişken + her-döngü kayıt → ölçülebilir CPU (gözlemci etkisi)
```

## Optimizasyon

### Doğru Aracı Doğru Soruya Eşleme

```
Soru                                  Araç                 Neden
──────────────────────────────────────────────────────────────────────
"Şu an değeri ne?"                     Watch Window         anlık, kurulumu sıfır
"Kim/ne zaman bu değeri yazdı?"        Data Breakpoint      call stack gösterir
"Aralıklı arıza, öncesinde ne oldu?"   Trace + trigger      her döngü + pre-trigger
"Hangi POU yavaş?"                     Profiler / kod-ölçüm POU bazlı zaman
"I/O fiziksel çalışıyor mu?"           Force                çıkışı sabitle, gözlemle
"Sistem yükü ne?"                      PLC Shell plcload    runtime metriği
"Neden durdu/çöktü?"                   Log Viewer           kök neden satırı
```

Yanlış araç = boşa zaman: hızlı sinyale Watch Window (kaçırır), aralıklı arızaya breakpoint (yakalayamaz), motion'a breakpoint (sistemi düşürür).

### Gözlemci Etkisini (Observer Effect) Azaltma

Debug araçlarının kendisi sistemi etkiler:
- **Monitoring/Watch:** IDE polling ek ağ+CPU yükü; çok değişken izleme task'ı yavaşlatabilir.
- **Trace:** çok değişken + her-döngü kayıt CPU yer; kritik ölçümde değişkeni sınırla.
- **Breakpoint:** sistemi tamamen durdurur — en invazif.

Sıralama (en az → en çok invazif): Log → PLC Shell → Trace → Watch → Force → Breakpoint. Canlı sistemde mümkün olan en az invazif araçla başla.

### Trace Buffer Boyutlandırma

```
Buffer = (yakalanacak süre) / (task cycle)
5sn olay, 10ms task → 500 döngü · pre-trigger = buffer'ın %50-80'i
Kök neden olaydan çok önceyse → buffer'ı büyüt veya sürekli kayıt + sonradan upload
```

## Derin Teknik Detay

### Breakpoint Neden Tüm Task'ları Durdurur?

Breakpoint, runtime'ın execution engine'ini (fundamentals/01) bir noktada askıya alır — ama IEC task'ları tek bir runtime altında çalıştığı için, biri durunca scheduler tüm IEC yürütmesini dondurur (tutarlı bir "durmuş durum" snapshot'ı için). Bu kasıtlıdır: bir task dururken diğeri çalışsaydı, incelediğiniz değişkenler altınızda değişir, snapshot anlamsızlaşırdı. Bedeli: bus cycle task da durur → EtherCAT/PROFINET sync kaybolur → slave'ler SafeOp'a düşer (Not 5). Bu yüzden breakpoint, "tutarlı snapshot" ile "canlı sistem sürekliliği" arasında temel bir takastır; motion'da snapshot'ın bedeli eksenin düşmesidir. Trace bu takası çözer: durdurmadan, her döngü kaydederek snapshot'ı zaman içinde toplar.

### Trace: Runtime İçi Ring Buffer Mimarisi

Trace, IDE'de değil **runtime içinde** çalışan bir ring buffer'dır (fundamentals/01 bileşen mimarisi). Her seçili task cycle'ında değişken değerlerini buffer'a yazar; IDE bağlı olmasa bile kayıt sürer. Bu, Watch Window'dan temel farkıdır: Watch IDE-polling'dir (IDE ↔ runtime ağ trafiği, 200ms), Trace runtime-yereldir (her döngü, ağ yok). Bu yüzden Trace hiçbir döngüyü kaçırmaz ve gözlemci etkisi minimaldir (yalnızca buffer yazma maliyeti). Trigger + pre-trigger mekanizması, "olaydan önceki ana" bakmayı sağlar — buffer sürekli döndüğü için tetik anında geçmiş zaten kayıtlıdır. Bu mimari, intermittent arızaları (Not 1: 3 günlük arıza) yakalamanın tek güvenilir yoludur.

### Online Change'in Reddetme Mantığı (Debug Perspektifi)

Online Change'in neyi kabul/reddettiği (programming/02 derin detay), çalışan **bellek görüntüsünü koruma** ilkesine dayanır. Debug açısından kritik: Online Change "interface değişmedi" derken, FB'nin bellek layout'unun (VAR offset'leri) aynı kaldığını kontrol eder. Layout aynıysa çalışan instance'ların verisi korunur; değiştiyse (yeni değişken, sıra değişimi) veri taşınamaz → reddedilir veya sıfırlanır. SFC adım sıfırlanması (Not 7) bunun özel bir halidir: SFC'nin iç adım-durumu değişkeni, kod değişikliğiyle yeniden konumlanırsa adım kaybolur. Bu yüzden Online Change "küçük mantık düzeltmesi" için güvenli, "yapısal değişiklik" için tehlikelidir — debug sırasında hızlı düzeltme cazip olsa da, SFC/retain/interface içeren kodda planlı duruş daha güvenlidir.

### Data Breakpoint: Donanım Watchpoint'in PLC Karşılığı

Data Breakpoint (belirli bir değişken değişince dur), CPU'nun donanım watchpoint (debug register) yeteneğine dayanır — bu yüzden yalnızca CODESYS Control Win V3'te (x86, OS debug API erişimi) çalışır, gömülü/ARM runtime'larda yoktur. Mekanizma: değişkenin bellek adresine bir donanım izleme kaydı kurulur; o adrese her yazma CPU'yu durdurur ve call stack'i yakalar. Bu, "kim bu değişkeni bozuyor?" sorusunu (Not 2: 4 saat → 20 dakika) doğrudan yanıtlar — değeri değiştiren kod yolunu call stack'te gösterir. Gerçek donanımda olmadığı için, oradaki aynı sorun için alternatif: değişkene yazan tüm yerleri grep'le + her birine geçici log ekle, veya tek-yazar disiplinini (programming/02) baştan uygula.

## İlgili Konular

```
knowledge/codesys/debugging/
├── 01_common_errors.md          → Debug araçlarıyla çözülecek hatalar
└── 03_performance_analysis.md   → Task Monitor ve Profiler araçları

knowledge/codesys/task-structure/
└── 01_task_types.md             → Breakpoint'in task'ları durdurması

knowledge/codesys/programming/
└── 05_error_handling.md         → Log'a programdan mesaj yazma
```
