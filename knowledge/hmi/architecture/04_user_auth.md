---
KONU        : HMI Kullanıcı Yetkilendirme ve Erişim Kontrolü
KATEGORİ    : hmi
ALT_KATEGORI: architecture
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://plcprogramming.io/blog/hmi-design-best-practices-complete-guide"
    başlık: "PLCProgramming.io — HMI Design Best Practices 2026"
    güvenilirlik: topluluk
  - url: "https://docs.tatsoft.com/display/FX/ISA-101+HMI+Compliance+How-to+Guide"
    başlık: "Tatsoft — ISA-101 HMI Compliance Guide"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_hmi_patterns.md"
    ilişki: gerektirir
  - konu: "02_realtime_data.md"
    ilişki: tamamlar
  - konu: "03_alarm_management.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "HMI mimari kalıpları (01_hmi_patterns.md)"
  - "Temel güvenlik kavramları (kimlik doğrulama, yetkilendirme)"
ÇELİŞKİLER :
  - kaynak: "Basit şifre yeterli algısı"
    konu: "Fabrika zemininde HMI'a 'herkes' erişiyorsa tek şifre anlamsız"
    çözüm: >
      Fabrika zemininde HMI'ı fiziksel olarak kullanan herkes tek şifreyi biliyorsa,
      yetkilendirme sistemin değil kağıdın üzerinde kalır.
      Çözüm: Kişisel kullanıcı adı/şifre + oturum zaman aşımı.
      İdeal: RFID kart ile hızlı oturum açma (fabrika zemininde pratik).
  - kaynak: "Role-based vs Attribute-based erişim kontrolü"
    konu: "RBAC basit ama bazı senaryolar için yetersiz"
    çözüm: >
      RBAC (Role-Based Access Control): Kullanıcı bir role sahip,
      rol belirli izinlere sahip. Sade ve yönetilebilir.
      ABAC (Attribute-Based): Vardiya, lokasyon, ekipman durumu gibi
      koşullara bağlı erişim. Çok güçlü ama karmaşık.
      Endüstriyel HMI için RBAC genellikle yeterli.
---

## Özün Ne

HMI yetkilendirme, "kim ne yapabilir" sorusunun yanıtıdır. Yetkilendirme olmayan bir fabrika HMI'ı, herkesin her şeyi — parametre değiştirme, makineyi durdurma, alarm bastırma — yapabileceği anlamına gelir. Sahada bu durum hem üretim kayıplarına hem güvenlik risklerine hem de hesap sorulabilirlik eksikliğine yol açar. "Motor 2 kim durdurdu?" sorusunun yanıtı logda olmalıdır. Bu belge, rol tabanlı erişim kontrolü tasarımını, uygulama yöntemlerini ve gerçek projelerde öğrenilen dersleri ele alır.

## Nasıl Çalışır

### Rol Tabanlı Erişim Kontrolü (RBAC)

Temel ilke: Kullanıcıya doğrudan izin verilmez; kullanıcı bir role atanır, role izin verilir.

```
Kullanıcı → Rol → İzinler

Ali (Operatör)     → OPERATOR rolü → [okuma, alarm onaylama, temel komutlar]
Fatma (Teknisyen)  → TECHNICIAN rolü → [okuma, yazma, test modu, kalibrasyon]
Hasan (Mühendis)   → ENGINEER rolü → [tüm Technician + parametre değiştirme]
Büyük Yönetici     → ADMIN rolü → [tüm izinler + kullanıcı yönetimi]
Ziyaretçi          → VIEWER rolü → [yalnızca okuma, hiç yazma yok]
```

### Standart Rol Hiyerarşisi

```
VIEWER (İzleyici):
  ✓ Tüm ekranları görüntüle
  ✓ Trend grafiklerini izle
  ✗ Hiçbir kontrol eylemi yok
  Tipik kullanıcı: Misafir, yönetici tur, kalite denetçisi

OPERATOR (Operatör):
  ✓ Tüm VIEWER izinleri
  ✓ Üretim parametreleri değiştirme (setpointler)
  ✓ Standart start/stop komutları
  ✓ Alarm onaylama
  ✓ Reçete seçimi ve yükleme
  ✗ Limit değerleri değiştirme
  ✗ Güvenlik parametreleri
  ✗ Bakım modu
  Tipik kullanıcı: Vardiya operatörü

TECHNICIAN (Teknisyen):
  ✓ Tüm OPERATOR izinleri
  ✓ Bakım modu aktivasyonu
  ✓ Manuel test komutları
  ✓ Kalibrasyon parametreleri
  ✓ Alarm bastırma (geçici, shelving)
  ✗ Güvenlik parametreleri
  ✗ Kullanıcı yönetimi
  Tipik kullanıcı: Bakım teknisyeni, devreye alma mühendisi

ENGINEER (Mühendis):
  ✓ Tüm TECHNICIAN izinleri
  ✓ Limit ve alarm sınır değerleri değiştirme
  ✓ PID parametre ayarı
  ✓ Reçete oluşturma/düzenleme
  ✓ Güvenlik parametrelerine sınırlı erişim
  ✗ Kullanıcı yönetimi
  Tipik kullanıcı: Proses mühendisi, otomasyon mühendisi

ADMIN (Yönetici):
  ✓ Tüm ENGINEER izinleri
  ✓ Kullanıcı ekleme/silme/rol atama
  ✓ Sistem yapılandırması
  ✓ Alarm sistemi yapılandırması
  ✓ Güvenlik ayarları
  Tipik kullanıcı: OT güvenlik sorumlusu, sistem yöneticisi

SAFETY (Güvenlik — Ayrı Kontrol):
  ✓ Güvenlik sistemi override
  ✓ Emergency stop bypass (prosedüre bağlı)
  → Bu rol çok kısıtlı ve belgelenmiş prosedüre bağlı olmalı
```

### İzin Matrisi

```
Eylem                          VİEWER  OPERATÖR  TEKNİSYEN  MÜHENDİS  ADMIN
──────────────────────────────────────────────────────────────────────────────
Ekranları görüntüle              ✓       ✓          ✓          ✓         ✓
Trend grafiklerini izle          ✓       ✓          ✓          ✓         ✓
Setpoint değiştirme              ✗       ✓          ✓          ✓         ✓
Motor start/stop                 ✗       ✓          ✓          ✓         ✓
Alarm onaylama                   ✗       ✓          ✓          ✓         ✓
Reçete seçimi                    ✗       ✓          ✓          ✓         ✓
Reçete düzenleme                 ✗       ✗          ✗          ✓         ✓
Alarm sınır değiştirme          ✗       ✗          ✗          ✓         ✓
Bakım modu aktive               ✗       ✗          ✓          ✓         ✓
Alarm bastırma (shelve)          ✗       ✗          ✓          ✓         ✓
Güvenlik parametresi             ✗       ✗          ✗          🔑        ✓
Kullanıcı yönetimi               ✗       ✗          ✗          ✗         ✓
Sistem yapılandırması            ✗       ✗          ✗          ✗         ✓

🔑 = Kısıtlı erişim, belgeleme gerektirir
```

## Pratikte Nasıl Kullanılır

### Backend: JWT Tabanlı Kimlik Doğrulama

```javascript
// Backend: Node.js + JWT

const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

const JWT_SECRET = process.env.JWT_SECRET;  // Güçlü, rastgele secret
const SESSION_TIMEOUT = 8 * 60 * 60;        // 8 saat (vardiya süresi)

// Giriş endpoint'i
app.post('/api/auth/login', async (req, res) => {
    const { username, password } = req.body;
    
    // Kullanıcıyı veritabanından bul
    const user = await db.users.findOne({ username, active: true });
    if (!user) {
        // Güvenlik: "Kullanıcı bulunamadı" değil, genel hata
        return res.status(401).json({ error: 'Geçersiz kimlik bilgileri' });
    }
    
    // Şifre kontrolü (bcrypt)
    const valid = await bcrypt.compare(password, user.passwordHash);
    if (!valid) {
        // Başarısız giriş logla (brute force tespiti için)
        await logFailedLogin(username, req.ip);
        return res.status(401).json({ error: 'Geçersiz kimlik bilgileri' });
    }
    
    // Çok fazla başarısız giriş → Hesabı kilitle
    if (user.failedLoginCount >= 5) {
        return res.status(423).json({ error: 'Hesap kilitlendi. Yönetici ile iletişime geçin.' });
    }
    
    // JWT token üret
    const token = jwt.sign(
        {
            userId: user.id,
            username: user.username,
            role: user.role,
            area: user.area    // Yalnızca belirli hat/alana erişim (opsiyonel)
        },
        JWT_SECRET,
        { expiresIn: SESSION_TIMEOUT }
    );
    
    // Başarılı giriş logla
    await logSuccessfulLogin(username, req.ip);
    await db.users.update(user.id, { failedLoginCount: 0, lastLogin: new Date() });
    
    res.json({
        token,
        user: { username: user.username, role: user.role, fullName: user.fullName }
    });
});

// Yetkilendirme middleware
function requirePermission(permission) {
    return (req, res, next) => {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) return res.status(401).json({ error: 'Oturum açılmamış' });
        
        try {
            const decoded = jwt.verify(token, JWT_SECRET);
            req.user = decoded;
            
            if (!userHasPermission(decoded.role, permission)) {
                // Yetkisiz erişim girişimini logla
                logUnauthorizedAccess(decoded.username, permission);
                return res.status(403).json({ error: 'Bu işlem için yetkiniz yok' });
            }
            
            next();
        } catch (err) {
            return res.status(401).json({ error: 'Oturum süresi dolmuş' });
        }
    };
}

// İzin kontrol matrisi
const ROLE_PERMISSIONS = {
    VIEWER:     ['read', 'trend.view'],
    OPERATOR:   ['read', 'trend.view', 'setpoint.write', 'motor.start', 'motor.stop', 'alarm.ack', 'recipe.select'],
    TECHNICIAN: ['read', 'trend.view', 'setpoint.write', 'motor.start', 'motor.stop', 'alarm.ack', 'recipe.select', 'maintenance.mode', 'alarm.shelve', 'calibration.write'],
    ENGINEER:   ['read', 'trend.view', 'setpoint.write', 'motor.start', 'motor.stop', 'alarm.ack', 'recipe.select', 'maintenance.mode', 'alarm.shelve', 'calibration.write', 'limit.write', 'recipe.edit', 'pid.tune'],
    ADMIN:      ['*']  // Tüm izinler
};

function userHasPermission(role, permission) {
    const perms = ROLE_PERMISSIONS[role] || [];
    return perms.includes('*') || perms.includes(permission);
}

// Korumalı endpoint örnekleri
app.post('/api/setpoint/:tagName', requirePermission('setpoint.write'), async (req, res) => {
    const { value } = req.body;
    const tagName = req.params.tagName;
    
    // Yazma log'u (kimin, neyi, ne zaman, önceki değer, yeni değer)
    await logWrite({
        userId: req.user.userId,
        username: req.user.username,
        tag: tagName,
        newValue: value,
        timestamp: new Date()
    });
    
    await plc.writeTag(tagName, value);
    res.json({ success: true });
});
```

### Frontend: Rol Bazlı UI

```jsx
// React: İzin kontrolüne göre UI elementi göster/gizle
function usePermission(permission) {
    const { user } = useAuth();
    if (!user) return false;
    return userHasPermission(user.role, permission);
}

function MotorControlPanel({ motorId }) {
    const canStart = usePermission('motor.start');
    const canStop = usePermission('motor.stop');
    const canSetSetpoint = usePermission('setpoint.write');
    const canAckAlarm = usePermission('alarm.ack');
    
    return (
        <div className="motor-panel">
            <div className="motor-status">
                {/* Herkes görebilir */}
                <MotorStatusDisplay motorId={motorId} />
            </div>
            
            <div className="motor-controls">
                {/* Yalnızca izni olan görür */}
                {canStart && (
                    <button
                        onClick={() => sendCommand(motorId, 'START')}
                        className="btn-start"
                    >
                        Başlat
                    </button>
                )}
                {canStop && (
                    <button
                        onClick={() => sendCommand(motorId, 'STOP')}
                        className="btn-stop"
                    >
                        Durdur
                    </button>
                )}
            </div>
            
            {canSetSetpoint && (
                <SetpointControl
                    tagName={`motor.${motorId}.speed_setpoint`}
                    min={0} max={100}
                    unit="m/dk"
                />
            )}
        </div>
    );
}

// Gizleme vs Devre Dışı Bırakma:
// Gizleme: Yetersiz izin → Element hiç görünmez (tercih edilir: Basit, temiz UX)
// Devre dışı: Element görünür ama tıklanamaz → "Neden çalışmıyor?" kafa karışıklığı
// ISA-101 önerisi: Yetki yoksa gizle. Operatör hayal kırıklığını önler.
```

### Oturum Zaman Aşımı

```javascript
// Frontend: Otomatik çıkış (Inactivity timeout)
class SessionManager {
    constructor(timeoutMs = 15 * 60 * 1000) {  // 15 dakika
        this.timeoutMs = timeoutMs;
        this.timer = null;
        this.warningTimer = null;
        this.onExpire = null;
        
        this.resetOnActivity();
    }
    
    resetOnActivity() {
        ['mousemove', 'mousedown', 'keydown', 'touchstart', 'scroll'].forEach(event => {
            document.addEventListener(event, () => this.resetTimer(), { passive: true });
        });
        this.resetTimer();
    }
    
    resetTimer() {
        clearTimeout(this.timer);
        clearTimeout(this.warningTimer);
        
        // 2 dakika kala uyarı
        this.warningTimer = setTimeout(() => {
            this.showSessionWarning();
        }, this.timeoutMs - 2 * 60 * 1000);
        
        // Süre bitince oturumu kapat
        this.timer = setTimeout(() => {
            this.expireSession();
        }, this.timeoutMs);
    }
    
    showSessionWarning() {
        // Modal: "Oturumunuz 2 dakika içinde kapanacak. Devam etmek ister misiniz?"
        showModal({
            message: 'Oturumunuz 2 dakika içinde kapanacak.',
            actions: [
                { label: 'Devam Et', onClick: () => this.resetTimer() },
                { label: 'Çıkış Yap', onClick: () => this.expireSession() }
            ]
        });
    }
    
    expireSession() {
        clearTimeout(this.timer);
        clearTimeout(this.warningTimer);
        logout();  // Token temizle, giriş sayfasına yönlendir
    }
}
```

### Şifre Politikası

```javascript
// Şifre validasyon
function validatePassword(password) {
    const rules = [
        { test: p => p.length >= 8, msg: 'En az 8 karakter' },
        { test: p => /[A-Z]/.test(p), msg: 'En az bir büyük harf' },
        { test: p => /[a-z]/.test(p), msg: 'En az bir küçük harf' },
        { test: p => /[0-9]/.test(p), msg: 'En az bir rakam' },
        { test: p => /[!@#$%^&*]/.test(p), msg: 'En az bir özel karakter' }
    ];
    
    const failures = rules.filter(r => !r.test(password)).map(r => r.msg);
    return { valid: failures.length === 0, errors: failures };
}

// Fabrika zemini için pratik şifre politikası:
// Minimum 8 karakter, büyük+küçük harf + rakam
// 90 günde bir değişim hatırlatması (zorla değil — operatör çok değiştirirse
//   sarı kağıda yazar ve monitöre yapıştırır → daha tehlikeli!)
```

### Yazma Log'u (Audit Trail)

```javascript
// Her yazma işlemi loglanmalı
async function logWriteOperation(data) {
    await db.auditLog.create({
        timestamp: new Date(),
        userId: data.userId,
        username: data.username,
        userRole: data.role,
        action: data.action,           // 'SETPOINT_WRITE', 'MOTOR_START' vb.
        targetTag: data.tag,           // 'motor.1.speed_setpoint'
        previousValue: data.prevValue, // 44.0
        newValue: data.newValue,       // 50.0
        unit: data.unit,               // 'm/dk'
        clientIp: data.ip,
        sessionId: data.sessionId
    });
}

// Kimin ne yaptığı sorgulanabilir olmalı:
// "Motor 2 kim durdurdu?"
// "Setpoint 08:30'da kim değiştirdi?"
// "Bu hafta kaç kez alarm onaylandı?"
```

## Örnekler

### Örnek 1: RFID ile Hızlı Giriş

```
Fabrika zemini sorunu: Operatörler eldiven giyiyor,
şifre yazmak zor ve yavaş.

Çözüm: RFID kart okuyucu + PIN kombinasyonu.
  1. RFID kartı okutunca kullanıcı tespit edilir.
  2. 4 haneli PIN gir (dokunmatik ekran, büyük buton).
  3. Giriş tamamlandı — 5 saniye.

Geleneksel kullanıcı adı + şifre:
  Kullanıcı adını yaz + şifreyi yaz = 30 saniye (eldivensiz).
  Eldivensiz: Daha uzun.

RFID kart + PIN:
  Kartı okut + 4 tuş = 5-8 saniye.
  
Ek güvenlik: Kart kaybolursa admin devre dışı bırakır.
              PIN bilinmeden kart tek başına yetersiz.
```

### Örnek 2: Mühendis Onaylı Yazma

```
Bazı kritik parametreler çift onay gerektirir.
Operatör değişiklik yapamaz; Mühendis onaylamalı.

Akış:
  1. Operatör: Sıcaklık üst limitini 95°C'den 100°C'ye değiştirmek istiyor.
  2. Sistem: "Bu parametre Mühendis onayı gerektiriyor."
  3. Mühendis kendi bilgileriyle giriş yapar (ayrı modal).
  4. Mühendis değişikliği onaylar + onay notu ekler.
  5. Değişiklik uygulanır, hem operatör hem mühendis log'da.

Bu mekanizma:
  → Kritik parametrelerin yanlışlıkla değiştirilmesini önler.
  → FDA 21 CFR Part 11 gibi regüle ortamlarda zorunlu.
```

### Örnek 3: Zaman Bazlı Erişim (Vardiya Kısıtlaması)

```javascript
// Bazı izinler yalnızca belirli vardiyada geçerli
function checkTimeBasedPermission(user, permission, requestTime) {
    // Gece vardiyası (22:00-06:00) için kısıtlı izinler
    const hour = requestTime.getHours();
    const isNightShift = hour >= 22 || hour < 6;
    
    if (isNightShift && permission === 'recipe.edit') {
        // Gece vardiyasında reçete düzenleme yok
        return {
            allowed: false,
            reason: 'Reçete düzenleme yalnızca gündüz vardiyasında (06:00-22:00)'
        };
    }
    
    return { allowed: true };
}
```

## Sık Yapılan Hatalar

### Hata 1: Paylaşılan Hesap Kullanmak

```
"Herkes 'operator/1234' ile giriş yapıyor."

Sonuç:
  - Kim ne yaptı bilinmiyor → Hesap verilebilirlik yok
  - Şifre değiştirilince herkese söylenmeli → Güvensiz
  - Birisi kötü eylem yaparsa izlenemez

Çözüm: Her kullanıcı kendi hesabı. İnsan kaynağı değişince hesap silinir.
```

### Hata 2: Frontend'de Yetkilendirmeyi Sonlandırmak

```javascript
// ❌ YANLIŞ — Yalnızca UI gizleme, backend'de kontrol yok
// Kullanıcı F12 açar, API direkt çağırır → Yazma başarılı!
if (user.role === 'VIEWER') {
    hideButton('stopMotor');  // Buton gizlendi ama API hâlâ açık
}

// ✅ DOĞRU — Backend'de her API isteğinde yetki kontrolü
app.post('/api/motor/stop', requirePermission('motor.stop'), (req, res) => {
    // Buton görünse de görünmese de, API istek gelirse kontrol edilir
});
```

### Hata 3: Şifreyi Post-it'e Yazdırmak

```
Karmaşık şifre politikası → Operatör hatırlamıyor → Monitöre yapıştırıyor.
Bu gerçek güvenlik riskidir.

Endüstriyel HMI için makul politika:
  8 karakter, büyük+küçük+rakam, 90 günde hatırlatma (zorla değil)
  + RFID/PIN kombinasyonu (fabrika zemini için)
  > Karmaşık şifre politikası

Güvenlik politikası insan davranışını hesaba katmalıdır.
```

### Hata 4: Çıkış Yapmayı Zorlaştırmak

```
Operatör çıkış yapmak için menüye giriyor → alt menü → "çıkış" buluyor.
Sonuç: Operatör çıkış yapmıyor, ekranı açık bırakıyor.

Çözüm:
  - Her ekranda görünür [Çıkış] butonu.
  - Veya otomatik zaman aşımı (inactivity timeout: 15 dakika).
  - Zaman aşımı uyarısı 2 dakika önce.
```

### Hata 5: Audit Log'u Olmamak

```
"Parametre yanlış ayarlanmış — kim değiştirdi?"
Log yok → Kim, ne zaman, ne değiştirdi bilinmiyor.
Sorumlu belirlenemiyor, aynı hata tekrar.

Her yazma işlemi loglanmalı:
  Kim, ne, ne zaman, önceki değer, yeni değer.
  Log: Değiştirilemez (immutable log).
  Saklama: En az 1 yıl (FDA 21 CFR Part 11: 3 yıl).
```

## Gerçek Proje Notları

**Not 1 — Paylaşılan Hesabın Sonucu**  
Bir fabrikada tüm operatörler "operator/123456" kullanıyordu. Reçete parametreleri yanlış girildi — 200'den fazla ürün hatalı üretildi. "Kim değiştirdi?" sorusu yanıtsız kaldı. Log'da yalnızca "operator" kullanıcısı görünüyordu. 12 saatlik vardiya boyunca 6 kişi o hesabı kullanmıştı. Kişisel hesap sistemine geçildi; bir sonraki benzer olayda 4 dakika içinde kimin ne yaptığı bulundu.

**Not 2 — Frontend-Only Yetkilendirmenin Kırılması**  
Bir web HMI'ında yetkilendirme yalnızca UI katmanındaydı. Bir teknisyen F12 açtı, Network sekmesini gözlemleyerek API endpoint'lerini buldu ve Postman'de doğrudan motor durdurma API'si çağırdı — yetkilendirme kontrol edilmedi, motor durdu. Backend'e `requirePermission()` middleware eklendi.

**Not 3 — Zaman Aşımı ile Üretim Kesintisi**  
Bir tesiste session timeout 5 dakikaydı. Operatör rapor oluştururken oturum kapandı, girdiği parametreler kayboldu. Operatör sinirli, zaman aşımını tamamen kapattı (admin şifresiyle). Çözüm: Activity-based timeout (mouse hareketi, tuş basışı sıfırlar). 15 dakika inaktivite = oturum kapatılır. Rapor düzenlemedeki keyboard aktivitesi timer'ı sıfırladı.

**Not 4 — Mühendis Onayı Mekanizmasının FDA Denetimini Geçmesi**  
Bir ilaç üretim tesisinde FDA 21 CFR Part 11 denetimi yapıldı. "Kritik parametreler kim tarafından değiştiriliyor?" sorusuna mühendis onaylı yazma mekanizması + immutable audit log ile yanıt verildi. Denetçi: "Bu çok iyi uygulanmış." Mekanizma, FDA denetimini geçmenin kritik bir unsuru oldu.

## İlgili Konular

```
knowledge/hmi/architecture/
├── 01_hmi_patterns.md           → HMI genel mimarisi
├── 02_realtime_data.md          → Bağlantı kopunca yazma devre dışı
└── 03_alarm_management.md       → Alarm onaylama yetkisi

Güvenlik standartları:
  IEC 62443                      → OT güvenlik standartlar ailesi
  FDA 21 CFR Part 11             → İlaç sektörü elektronik kayıt/imza
  ISA-101.01                     → HMI tasarım standardı (erişim kontrol bölümü)
  
Araçlar:
  JSON Web Token (JWT)           → Token tabanlı kimlik doğrulama
  bcrypt                         → Şifre hash'leme
  LDAP/Active Directory          → Kurumsal kullanıcı yönetimi entegrasyonu
```
