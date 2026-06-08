---
KONU        : OPC-UA Güvenlik Modeli
KATEGORİ    : protocols
ALT_KATEGORI: opc-ua
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/Security/_sec_using_secure_opc_ua_server.html"
    başlık: "CODESYS Online Help — Securely Using the OPC UA Server"
    güvenilirlik: resmi
  - url: "https://integrationobjects.com/blog/what-is-opc-ua/"
    başlık: "Integration Objects — OPC UA Security Section"
    güvenilirlik: topluluk
  - url: "https://www.opc-router.com/what-is-opc-ua/"
    başlık: "OPC Router — OPC UA Security Details"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_architecture.md"
    ilişki: gerektirir
  - konu: "05_codesys_server_config.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/networking/01_opcua_server.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "OPC UA mimari temelleri (01_architecture.md)"
  - "Temel PKI/sertifika kavramları (CA, X.509, şifreleme)"
ÇELİŞKİLER :
  - kaynak: "BSI OPC UA güvenlik değerlendirmesi"
    konu: "BSI raporu OPC UA'yı güvenli buldu ama implementasyon sorunlarına dikkat çekti"
    çözüm: >
      BSI (Alman Federal Bilgi Güvenliği Ofisi), OPC UA'nın protokol tasarımında
      sistematik güvenlik açığı bulmadı. Ancak yanlış yapılandırma (None security mode,
      zayıf şifre, güvenilmeyen sertifikalar) real-world saldırılara kapı açabilir.
      Protokol güvenli ama kurulum güvenliği kullanıcının sorumluluğunda.
  - kaynak: "Anonymous vs kullanıcı kimlik doğrulama"
    konu: "CODESYS SP17+ sonrası anonymous varsayılan olarak kapalı"
    çözüm: >
      SP17 ve sonrası: anonymous erişim otomatik kapalı, kullanıcı tanımlanmalı.
      Eski projelerde SP17'ye geçiş aniden tüm istemcilerin bağlantısını keser.
      Yükseltme öncesi tüm OPC UA istemcileri kimlik doğrulama desteği için kontrol edilmeli.
---

## Özün Ne

OPC UA güvenlik modeli, endüstriyel protokoller arasında en kapsamlı güvenlik altyapısına sahiptir. Üç katmanda çalışır: **Transport güvenliği** (TLS/SSL benzeri şifreleme), **Uygulama güvenliği** (sertifika tabanlı sunucu ve istemci kimlik doğrulama), ve **Kullanıcı güvenliği** (kullanıcı adı/şifre, sertifika veya Windows kimliği). Bu üç katmanın tamamının doğru yapılandırılması, OPC UA bağlantısını güvenilir kılar. Eksik veya yanlış yapılandırma, güçlü bir protokolü anlamsız kılar.

## Nasıl Çalışır

### Güvenlik Katmanları

```
┌─────────────────────────────────────────────────────────────┐
│  KATMAN 3: Kullanıcı Kimlik Doğrulama                       │
│  Kimler bağlanabilir? Ne yapabilir?                         │
│  Yöntemler: Anonymous, Username+Password, X.509 Sertifika   │
├─────────────────────────────────────────────────────────────┤
│  KATMAN 2: Uygulama Kimlik Doğrulama                        │
│  Hangi istemci güvenilir? Hangi sunucu güvenilir?           │
│  Mekanizma: X.509 sertifika değişimi + Trust List           │
├─────────────────────────────────────────────────────────────┤
│  KATMAN 1: Mesaj Güvenliği (Security Mode)                  │
│  Veriler şifreli mi? İmzalı mı?                             │
│  Modlar: None | Sign | SignAndEncrypt                       │
└─────────────────────────────────────────────────────────────┘
```

### Security Mode (Güvenlik Modu)

Üç mod tanımlıdır; her endpoint bir veya daha fazla modu destekler:

| Mod | İmzalama | Şifreleme | Kullanım |
|---|---|---|---|
| `None` | ✗ | ✗ | Yalnızca kapalı LAN test ortamı |
| `Sign` | ✓ | ✗ | Bütünlük koruması, şifresiz |
| `SignAndEncrypt` | ✓ | ✓ | Üretim ortamı — her zaman bu |

`None` modun tehlikesi: Tüm veri düz metin. Ağda herhangi biri OPC UA trafiğini okuyabilir, hatta değiştirebilir. OPC UA'nın güvenlik avantajı tamamen devre dışı.

### Security Policy (Güvenlik Politikası)

Hangi kriptografik algoritmaların kullanılacağını belirler:

| Politika | İmzalama | Şifreleme | Durum |
|---|---|---|---|
| `Basic128Rsa15` | RSA-SHA1 | AES-128 | Eskimiş, kullanma |
| `Basic256` | RSA-SHA1 | AES-256 | Eskimiş, kullanma |
| `Basic256Sha256` | RSA-SHA256 | AES-256 | ✓ Yaygın, güvenli |
| `Aes128-Sha256-RsaOaep` | RSA-SHA256 | AES-128 | ✓ Modern, hızlı |
| `Aes256-Sha256-RsaPss` | RSA-PSS-SHA256 | AES-256 | ✓ En güçlü |

Üretim için önerilen: `Basic256Sha256` veya `Aes256-Sha256-RsaPss`.

### Sertifika Altyapısı (PKI)

OPC UA sertifika altyapısı, her iki tarafın (istemci + sunucu) X.509 sertifikası kullanmasını zorunlu kılar. Yapı:

```
Sertifika Klasör Yapısı (Sunucu tarafı):
  /pki/
  ├── trusted/         ← Güvenilir sertifikalar (buradakiler bağlanabilir)
  │   ├── certs/       ← Güvenilir CA veya istemci sertifikaları
  │   └── crl/         ← Sertifika iptal listeleri (CRL)
  ├── rejected/        ← Reddedilen sertifikalar (ilk bağlantıda buraya düşer)
  ├── own/             ← Sunucunun kendi sertifikası ve private key
  │   ├── certs/
  │   └── private/
  └── issuers/         ← Güvenilen CA sertifikaları
```

**İlk bağlantı akışı:**

```
İstemci → Sunucuya bağlanmaya çalışır
Sunucu ← İstemcinin sertifikasını alır
Sunucu → Sertifikayı rejected/ klasörüne atar
Sunucu ← İstemciyi reddeder (güvenilmiyor)

Yönetici → rejected/ klasöründeki sertifikayı trusted/certs/ klasörüne taşır
           (veya UaExpert, CODESYS Security Agent üzerinden "Trust" işareti koyar)

İstemci → Yeniden bağlanmaya çalışır
Sunucu ← İstemciyi tanır → Bağlantıya izin verir ✓
```

### Kullanıcı Kimlik Doğrulama Yöntemleri

```
1. Anonymous (Anonim):
   Kimlik doğrulama yok.
   CODESYS SP17+ sonrası varsayılan kapalı.
   Yalnızca test/geliştirme için (ve bu bile riskli).

2. Username + Password (Kullanıcı Adı + Şifre):
   En yaygın endüstriyel yaklaşım.
   Şifreler ağda şifreli gönderilir (Security Mode: Sign veya SignAndEncrypt ile).
   Kullanıcı → rol → izinler hiyerarşisi.

3. X.509 Sertifika (Kullanıcı Sertifikası):
   İstemci, kullanıcı kimliğini sertifika ile kanıtlar.
   En güçlü yöntem — şifre yönetimi gerekmez.
   OT/IT entegrasyonu projelerinde tercih edilir.

4. Kerberos / Windows NTLM:
   Bazı sunucular Windows AD kimlik doğrulamasını destekler.
   Kurumsal ortamlarda AD hesapları doğrudan kullanılabilir.
```

### Roller ve İzinler

```
Standart OPC UA rolleri:
  Anonymous    : Salt okuma (kısıtlı)
  AuthenticatedUser : Standart okuma
  Observer     : Tüm değerleri görme, değiştirme yok
  Operator     : Komut değerlerini yazma
  Engineer     : Yapılandırma değiştirme
  Supervisor   : Denetleme
  ConfigureAdmin : Kullanıcı yönetimi dahil tam yetki
  SecurityAdmin : Güvenlik politikası yönetimi

CODESYS'teki karşılık:
  Kullanıcı rolleri → Device → Access Rights sekmesi
```

## Pratikte Nasıl Kullanılır

### CODESYS'te Sertifika Oluşturma (Adım Adım)

```
Adım 1: Security Agent'ı Aç
  CODESYS IDE → View → Security Screen

Adım 2: Cihazı Seç
  Devices sekmesi → Kontrolcüyü seç

Adım 3: OPC UA Server Servisini Bul
  Sağ panel → CmpOPCUAServer servisini seç

Adım 4: Sertifika Oluştur
  "Create Certificate" (ikon) → Parametreler:
  
  Organization  : Acme Automation GmbH
  Common Name   : CODESYS OPC UA Server [hostname]
  Country       : DE
  City          : Munich
  State         : Bavaria
  Email         : (opsiyonel)
  Valid Days    : 3650 (10 yıl — yenileme hatırlatıcısı kur)
  Key Size      : 2048 bit (minimum), 4096 bit (önerilir)
  
  → OK → Sertifika /pki/own/ klasörüne kaydedilir

Adım 5: Runtime'ı Yeniden Başlat
  sudo systemctl restart codesyscontrol
```

### UaExpert ile İlk Güvenli Bağlantı

```
1. UaExpert → Server → Add
   Discovery URL: opc.tcp://192.168.1.100:4840
   
2. Güvenlik ayarı:
   Security Policy : Basic256Sha256
   Message Security Mode : SignAndEncrypt
   
3. OK → Endpoint listesi gelir → SignAndEncrypt'i seç → OK

4. İlk bağlantı denemesi:
   "Security Certificate" uyarısı çıkar
   → Sunucu sertifikasını gözden geçir → "Trust Server Certificate"
   
5. Kimlik doğrulama:
   Authentication Mode: Username
   Username: opc_user
   Password: ***
   
6. Connect → Bağlantı kurulur ✓
```

### Python ile Güvenli Bağlantı

```python
import asyncio
from asyncua import Client
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
from asyncua.crypto import uacrypto, security_policies
import os

async def secure_connect():
    """
    Basic256Sha256, SignAndEncrypt modunda bağlantı.
    İstemci sertifikası oluşturulmuş olmalı.
    """
    client = Client(url="opc.tcp://192.168.1.100:4840")
    
    # Güvenlik politikası ve modu ayarla
    await client.set_security(
        SecurityPolicyBasic256Sha256,
        certificate=open("client_cert.der", "rb").read(),
        private_key=open("client_key.pem", "rb").read(),
        server_certificate=open("server_cert.der", "rb").read()
    )
    
    # Kullanıcı kimlik doğrulama
    client.set_user("opc_user")
    client.set_password("securePassword123!")
    
    await client.connect()
    
    try:
        # Normal işlemler
        node = client.get_node("ns=4;s=Motor1.Speed")
        value = await node.read_value()
        print(f"Speed: {value}")
    finally:
        await client.disconnect()

asyncio.run(secure_connect())
```

### İstemci Sertifikası Oluşturma (Python)

```python
from asyncua.crypto import uacrypto

# İstemci için self-signed sertifika oluştur
cert, key = uacrypto.generate_certificate(
    common_name="MyOPCUAClient",
    organization="Acme Automation",
    country="DE",
    days=3650
)

# Dosyalara kaydet
with open("client_cert.der", "wb") as f:
    f.write(cert)
with open("client_key.pem", "wb") as f:
    f.write(key)

print("Client certificate generated.")
print("Place client_cert.der in server's pki/trusted/certs/ folder")
```

### CODESYSControl.cfg ile Güvenlik Yapılandırması

```ini
[CmpOPCUAServer]
; Security mode zorunlu kıl
; 0=None kabul edilmez, yalnızca Sign ve SignAndEncrypt
MinSecurityMode=1        ; 0=None, 1=Sign, 2=SignAndEncrypt

; Anonymous erişim
AllowAnonymous=0         ; 0=kapalı (önerilir), 1=açık

; Sertifika doğrulama
EnableCRLChecks=1        ; Sertifika iptal listesi kontrolü

; Session timeout (saniye)
SessionTimeout=3600

; Maksimum eş zamanlı session
MaxSessions=10
```

## Örnekler

### Örnek 1: Rol Bazlı Erişim Senaryosu

```
Kullanıcılar ve roller (CODESYS Access Rights):
  opc_viewer  : Observer   → Tüm değerleri okur, yazamaz
  opc_operator: Operator   → İşletmeci komutları yazar (Start/Stop/Setpoint)
  opc_scada   : Engineer   → Tüm yazma işlemleri, parametre değiştirme
  opc_maint   : Supervisor → Diagnostik veriye tam erişim

Node bazlı kısıtlama:
  Motor1.StartCmd (ReadWrite):
    → opc_viewer: Yalnızca Read
    → opc_operator: ReadWrite
    → opc_scada: ReadWrite
    
  SafetyInterlocks (ReadWrite):
    → opc_viewer: Yalnızca Read
    → opc_operator: Yalnızca Read   ← Operatör de yazamaz
    → opc_scada: ReadWrite
```

### Örnek 2: Sertifika Güven Listesini Yönetme (Linux)

```bash
# OPC UA server sertifika klasörü
cd /var/opt/codesys/pki/

# Reddedilen sertifikaları görüntüle
ls -la rejected/certs/

# UaExpert istemcisinin sertifikasını güven listesine ekle
cp rejected/certs/UaExpert_[fingerprint].der trusted/certs/

# Değişiklik otomatik uygulanır (restart gerekmez)
# Yeni bağlantı denemesinde istemci kabul edilir

# Güvenilen sertifikaları listele
ls -la trusted/certs/
```

### Örnek 3: Sertifika Yenileme Hatırlatma Sistemi

```iecst
(* PLC programında sertifika son kullanma kontrolü *)
(* CmpCert kütüphanesi gerekebilir — platforma bağlı *)
PROGRAM PRG_CertMonitor
VAR
    dtCertExpiry     : DATE_AND_TIME;   (* Sertifika son kullanma tarihi *)
    tDaysRemaining   : DINT;
    xCertExpirySoon  : BOOL;
END_VAR

(* Sertifika bitiş tarihini hardcode veya yapılandırma dosyasından oku *)
dtCertExpiry := DT#2036-06-01-00:00:00;

(* Kalan günü hesapla *)
tDaysRemaining := DATE_AND_TIME_TO_DINT(dtCertExpiry) - DATE_AND_TIME_TO_DINT(NOW());
tDaysRemaining := tDaysRemaining / 86400;  (* Saniyeyi güne çevir *)

(* 30 günden az kaldıysa uyar *)
xCertExpirySoon := tDaysRemaining < 30;

IF xCertExpirySoon THEN
    GVL_Alarms.xOPCUACertExpiringSoon := TRUE;
    (* Operatör panelinde uyarı göster *)
END_IF
```

## Sık Yapılan Hatalar

### Hata 1: Üretimde None Security Mode Bırakmak

```
Test için None mode yapılandırıldı → Hızlı test kolaylaştı.
Proje üretime geçti, None mode kaldırılmadı.
Sonuç: Tüm OPC UA trafiği şifresiz, ağdaki herkes okuyabilir.

Kontrol: Periyodik endpoint taramasıyla security mode doğrula.
Önlem : Üretim dağıtım kontrol listesinde "Security Mode = SignAndEncrypt" şartı.
```

### Hata 2: Sertifika Süresini Takip Etmemek

```
Self-signed sertifika 1 yıl için oluşturuldu.
1 yıl sonra sertifika expired → Tüm OPC UA bağlantıları kesildi.
Üretim makineleri izleme kaybetti.

Çözüm: 
  a) Sertifikaları minimum 5-10 yıl için oluştur.
  b) Sertifika bitiş tarihini takvime ekle (30 gün önceden uyarı).
  c) Otomasyon: Sertifika son kullanma tarihi PLC log'una yazılsın.
```

### Hata 3: SP17 Yükseltmesi Sonrası Bağlantı Kesilmesi

```
Runtime SP17'ye yükseltildi.
Anonymous erişim otomatik kapandı.
Mevcut tüm OPC UA istemcileri (SCADA dahil) bağlanamıyor.

Acil çözüm: AllowAnonymous=1 (geçici)
Kalıcı çözüm: Tüm istemcilerde kullanıcı adı/şifre yapılandır.
```

### Hata 4: Tek Kullanıcı ile Tüm Erişim

```
Tüm istemciler aynı "admin" hesabı kullanıyor.
Bir istemci kötü amaçlı komut gönderirse kimin gönderdiği bilinemez.
Admin şifresi ele geçirilirse tüm sistem risk altında.

Çözüm: Her istemci/uygulama için ayrı kullanıcı + minimum gerekli izinler.
       Principle of Least Privilege — endüstriyel otomasyon için de geçerli.
```

### Hata 5: Şifreleme Olmadan Şifre Göndermek

```
Security Mode: None → Şifreleme yok.
Kullanıcı kimliği: Username + Password.

Sonuç: Şifre ağda açık metin gönderiliyor.
       Güvenlik katmanları birbirini desteklemez.

Kural: Kullanıcı kimliği Username/Password ise
       Security Mode en az Sign olmalı (tercihen SignAndEncrypt).
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**SignAndEncrypt + Kullanıcı kimlik kullan:**
- OT/IT sınırını geçen her bağlantı (PLC → SCADA, MES, ERP)
- Farklı organizasyonlar arası veri paylaşımı
- Internet veya WAN üzerinden erişim
- Endüstriyel ağda dahi (ISO 27001 veya NIS2 uyumluluk)

**None mode yalnızca:**
- Kapalı, izole geliştirme ağında kısa süreli test
- Başka hiçbir durumda kabul edilemez

## Gerçek Proje Notları

**Not 1 — Sertifika Sorunuyla Geçen 4 Saat**  
İlk OPC UA projesinde sertifika güven listesi kurulmamıştı. İstemci bağlanamıyordu; hata mesajı "BadSecurityChecksFailed" — anlamsız. Sorunun kaynağı: Sunucunun rejected/ klasöründe biriken sertifikalar. trusted/certs/'e taşınınca anında bağlandı. Şimdi kurulum sırasında Trust yapılandırması ilk adım.

**Not 2 — SP17 Güncelleme Felaketi**  
Üretime yakın bir gün runtime güncellemesi yapıldı. SP17 ile anonymous erişim kapandı. SCADA sistemi bağlantısı kesildi. Sahada acil: AllowAnonymous=1 geçici düzeltmesi. 2 hafta içinde tüm SCADA bağlantıları kullanıcı kimliğine geçirildi. Bu deneyim sonrası tüm runtime güncellemeleri önce release notes okunarak yapılıyor.

**Not 3 — Rol Tabanlı Erişimin Güvenlik Denetimini Geçmesi**  
Fabrika, NIS2 direktifi kapsamında güvenlik denetiminden geçti. OPC UA rol tabanlı erişim (her kullanıcının kendi hesabı + minimum izin) denetçilere sistem güvenliği konusunda güven verdi. Modbus tabanlı sistemler "kimlik doğrulama yok" gerekçesiyle daha ayrıntılı incelendi.

## İlgili Konular

```
knowledge/protocols/opc-ua/
├── 01_architecture.md           → Güvenlik katmanlarının genel bağlamı
├── 05_codesys_server_config.md  → CODESYS güvenlik yapılandırma detayı
└── 06_client_implementations.md → Python/JS'de güvenli bağlantı örnekleri

knowledge/codesys/networking/
└── 01_opcua_server.md           → CODESYS OPC UA server güvenlik kurulumu

Araçlar:
  OpenSSL     → Sertifika oluşturma ve doğrulama
  UaExpert    → Endpoint discovery + güvenlik policy kontrolü
  Wireshark   → OPC UA trafik analizi (şifreli trafiği çözmek için private key gerekir)
```
