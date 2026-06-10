# Güvenlik Mühendisliği İlkeleri

Endüstriyel otomasyonda yazılım, fiziksel dünyayı hareket ettirir. Bir hata; makine kırılması, üretim kaybı veya insan yaralanması demektir. Bu ilkeler tartışmaya kapalıdır — `rules.json` içindeki `codesys.safety` bölümünün gerekçeli açılımıdır.

> Temel ilke: **Emniyet, yazılım mantığına bağımlı olmamalıdır.** Yazılım emniyeti destekler, garanti etmez. Garanti donanımsal emniyet zincirinden gelir.

---

## 1. Emniyet ≠ Standart Kontrol
- Emniyet I/O **asla** standart modüllere bağlanmaz (`safety_io_on_standard_modules_forbidden`).
- Acil durdurma (E-Stop), ışık perdesi, kapı kilidi → sertifikalı emniyet donanımı (Safety PLC / emniyet rölesi).
- Standart PLC bu sinyalleri **okuyabilir** (durum göstermek için) ama emniyet fonksiyonunu **üstlenemez**.

## 2. Arıza Durumunda Güvenli Hâl (Fail-Safe)
- CPU arızası, watchdog tetiği veya güç kaybında **tüm çıkışlar enerjisiz** olmalı (`all_outputs_deenergize_on_cpu_fault`).
- Varsayılan hâl her zaman "durdur / güvenli" olmalı, "çalışmaya devam et" değil.
- Aktüatörleri öyle tasarla ki sinyal kaybı = güvenli yön (ör. yay-geri valf).

## 3. Watchdog
- Watchdog devre dışı bırakmak **gerekçe gerektirir** (`watchdog_disable_requires_justification`).
- Gerekçe `project_report.md` içinde açıkça yazılır. Sessizce devre dışı bırakma yok.

## 4. Interlock Mantığı
- Birbirini etkileyen hareketler (ör. konveyör bölge geçişleri) açık interlock ile korunur.
- Interlock koşulu kod içinde dağıtık değil, tek ve okunabilir yerde toplanır.
- Her interlock'un neden var olduğu yorumda açıklanır.

## 5. Acil Durdurma Zinciri
- E-Stop donanımsaldır; yazılım sadece durumu yansıtır ve kontrollü duruşu yönetir.
- Belirtilen süre içinde durma garantisi (ör. spec'teki "500 ms içinde dur") test edilebilir olmalı.

## 6. Sınır ve Aralık Kontrolü
- Tüm analog girişler aralık dışı (out-of-range / sensör kopması) için kontrol edilir → NAMUR NE107 (`/knowledge/standards/03_namur_ne107`).
- Hesaplamalarda taşma (overflow) ve sıfıra bölme açıkça ele alınır.

## 7. Siber Güvenlik (IEC 62443)
- Ağ erişimi en az ayrıcalık ilkesiyle tasarlanır (`/knowledge/standards/02_iec62443`).
- OPC-UA için: anonim erişim yerine kimlik doğrulama + şifreleme tercih edilir.
- Kontrol ağı ile IT/ofis ağı segmente edilir (bkz. `/knowledge/networking/02_security`).

---

## Teslim Öncesi Emniyet Sorusu
Her projede kendine sor: *"Bu sistemde tek bir yazılım hatası birini yaralayabilir mi?"*
Cevap "evet" ise, o fonksiyon donanımsal emniyet zincirine taşınmalı ve raporda işaretlenmelidir.
