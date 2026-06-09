---
KONU        : HMI Alarm Yönetimi
KATEGORİ    : hmi
ALT_KATEGORI: architecture
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://instrumentationtools.com/isa-18-2-alarm-management-in-process-plants/"
    başlık: "InstrumentationTools — ISA 18.2 Alarm Management"
    güvenilirlik: topluluk
  - url: "https://assets.new.siemens.com/siemens/assets/api/uuid:234f1026-298f-49dc-8961-0c5223c38588/Siemens-White-Paper-Alarm-Management.pdf"
    başlık: "Siemens — Alarm Management and ISA-18.2 White Paper"
    güvenilirlik: topluluk
  - url: "https://www.yokogawa.com/library/resources/media-publications/effective-alarm-management-planning-using-ansiisa-182/"
    başlık: "Yokogawa — Effective Alarm Management Planning Using ISA-18.2"
    güvenilirlik: topluluk
  - url: "https://www.exida.com/articles/ALARM-MANAGEMENT-AND-ISA-18-A-JOURNEY-NOT-A-DESTINATION.pdf"
    başlık: "Exida — Alarm Management and ISA-18: A Journey, Not a Destination"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_hmi_patterns.md"
    ilişki: gerektirir
  - konu: "02_realtime_data.md"
    ilişki: kullanır
  - konu: "04_user_auth.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "HMI mimari kalıpları (01_hmi_patterns.md)"
  - "PLC alarm mantığı temel kavramı"
ÇELİŞKİLER :
  - kaynak: "Çok fazla alarm, operatörü korur algısı"
    konu: "Alarm bolluğu alarm körlüğüne yol açar"
    çözüm: >
      ISA-18.2'nin temel prensibi: Her alarm bir operatör müdahalesi gerektirir.
      Eğer bir alarm hiçbir müdahaleye yol açmıyorsa alarm değildir — event'tir.
      Ortalama endüstri standardı: Operatör başına <10 alarm/10 dakika.
      Alarm bolluğu operatörü yorar ve kritik alarmları kaçırtır.
  - kaynak: "Onaylanmış alarm = çözüme kavuşmuş alarm algısı"
    konu: "Acknowledge ≠ Resolved — önemli fark"
    çözüm: >
      Acknowledge (Onaylar): Operatörün alarmı gördüğünü doğrular.
      Durum hâlâ aktif olabilir. Alarm listesinde görünmeye devam eder.
      Resolve/Clear: Alarm koşulu ortadan kalktı.
      HMI'da bu iki durum birbirinden net ayrılmalı.
---

## Özün Ne

ISA-18.2 "Management of Alarm Systems for the Process Industries" standardı, endüstriyel alarm yönetiminin tanımını netleştirir: Alarm, operatörden bir müdahale gerektiren bir durum bildirimidir. Bu tanıma göre alarm olmayan şeyleri alarm olarak kodlamak — tüm sistemin alarm kalitesini düşürür. Bir proses tesisinde 300'den fazla alarm/saatin üzerinde çalışan operatörler "alarm körlüğü" geliştirerek kritik alarmları gözden kaçırır. HMI tarafında alarm sistemi tasarımı, PLC tarafındaki alarm mantığıyla mükemmel uyum içinde olmalı ve ISA-18.2'nin yaşam döngüsü prensiplerine uymalıdır.

## Nasıl Çalışır

### Alarm Durumları

Her alarm, belirli bir durum döngüsünden geçer:

```
PLC Koşulu                           Alarm Durumu         HMI Gösterimi
──────────────────────────────────────────────────────────────────────────────
Normal. Koşul yok.                  [NORMAL]             → Alarm listesinde yok

Koşul aktif oldu.                   [UNACKNOWLEDGED]     → 🔴 Yanıp söner
(ör: Sıcaklık > 90°C)              [ACTIVE]              Kırmızı, belirgin
                                     [UNACK]

Operatör onayladı.                  [ACKNOWLEDGED]       → 🟠 Sabit (yanmıyor)
Koşul hâlâ aktif.                  [ACTIVE]              Turuncu/soluk

Koşul düzeldi.                      [RETURN-TO-NORMAL]   → Listeden kaldırılır
Alarm kapandı.                      [NORMAL]              (veya geçmişe taşınır)

Koşul aktif, Op. onaylamadı,        [SHELVED]            → 🟡 Sarı, ikon
Alarm susturuldu (shelved).                               Geçici bastırma

Bakım sırasında.                    [SUPPRESSED]         → Gri, bakım ikonu
Alarm bastırıldı.                                         Operatöre görünmez
```

**State machine diyagramı:**
```
          [Normal]
           │ Koşul aktif
           ▼
     [Active+Unack] ←─── Koşul sürdü ───┐
           │ Operatör onaylar            │
           ▼                            │
     [Active+Ack] ──────────────────────┘
           │ Koşul düzeldi
           ▼
     [RTN+Unack] (Return-to-Normal, onaylanmamış)
           │ Operatör onaylar veya timeout
           ▼
         [Normal]
```

### ISA-18.2 Alarm Öncelik Seviyeleri

```
ISA-18.2, 3-4 öncelik seviyesi önerir:
  → %5'inden azı Kritik olmalı
  → Seviye sayısı artıkça operatör kafa karıştırır

Endüstriyel standart 4 seviye:

Öncelik 1 — KRİTİK (Critical):
  Renk: Kırmızı
  Tepki süresi: Saniyeler içinde (5-15 saniye)
  Sonuç: İşletme güvenliği riski, ekipman hasarı, yaralanma
  Örnekler: Acil durdurma, güvenlik limit aşımı, yangın/gaz
  ISA kısıtı: Toplam alarmların max %5'i

Öncelik 2 — YÜKSEK (High):
  Renk: Turuncu
  Tepki süresi: Dakikalar içinde (5-10 dakika)
  Sonuç: Proses bozulması, ürün kaybı riski
  Örnekler: Motor arızası, sıcaklık limit aşımı, basınç yüksek
  ISA kısıtı: Toplam alarmların max %15'i

Öncelik 3 — ORTA (Medium):
  Renk: Sarı
  Tepki süresi: Saatler içinde
  Sonuç: Etkinlik kaybı, bakım gereksinimi
  Örnekler: Filtre basınç farkı, yağ seviyesi düşük, performans sapması

Öncelik 4 — DÜŞÜK (Low):
  Renk: Mavi veya koyu sarı
  Tepki süresi: Vardiya içinde
  Sonuç: Bakım planlama, izleme
  Örnekler: Bakım bildirimi, kalibrasyon zamanı, yazılım uyarısı
```

### ISA-18.2'nin Temel Prensipleri

```
1. "Her alarm bir müdahale gerektirir":
   Operatör alarmı görünce ne yapacağını bilmeli.
   Alarm mesajı: Ne oldu? → Neden? → Ne yapmalısın?
   Kötü: "Motor Arızası"
   İyi : "Konveyör 2 Motor Arızası — Akım aşımı. Freks panelini kontrol et."

2. Alarm mı Event mi?
   Alarm: Müdahale gerektirir, operatör dikkatine alınır.
   Event: Bilgi amaçlı kayıt, müdahale gerekmez.
   Kapı açıldı → Event (log)
   Kapı 5 dakika açık kaldı → Alarm (operatör müdahalesi gerekebilir)

3. Alarm fırtınası (Alarm Flood) önleme:
   Bir olay sonrası çok sayıda alarm aynı anda aktive olabilir.
   ISA-18.2 kısıtı: <10 alarm/10 dakika operatör başına
   Çözüm: Alarm gruplama, kök neden analizi, suppression/shelving

4. "Worst Actor" analizi:
   En sık aktive olan alarm nedir? Neden?
   Gereksiz alarm → Kaldır.
   Sık tetiklenen → Limit ayarını gözden geçir.

5. Renk körü erişilebilirliği:
   Erkek nüfusun %8-12'si renk körüdür.
   Renk + şekil + konum kombinasyonu kullan.
   Yalnızca renge güvenme: Kritik = kırmızı + ünlem işareti + yanıp sönme.
```

### Alarm Ekranları

**Aktif Alarm Listesi (Ana Ekran):**
```
┌─────────────────────────────────────────────────────────────────────────┐
│  AKTİF ALARMLAR (5)              [Tümünü Onayla] [Filtre ▼] [Geçmiş]  │
├────┬────┬──────────────────────────┬──────────────┬──────────┬──────────┤
│Önc │Dur │ Açıklama                 │ Başlangıç    │ Süre     │ İşlem   │
├────┼────┼──────────────────────────┼──────────────┼──────────┼──────────┤
│ 🔴 │ !  │ Konveyör 2 Motor Arızası │ 14:23:05     │ 00:02:15 │[Onayla] │
│ 🟠 │ !  │ Hat 1 Sıcaklık Yüksek    │ 14:21:33     │ 00:03:47 │[Onayla] │
│ 🟠 │ ✓  │ Hat 2 Hız Sapması        │ 14:18:47     │ 00:06:33 │         │
│ 🟡 │ ✓  │ Yağlama Basınç Düşük     │ 14:15:22     │ 00:09:58 │         │
│ 🔵 │ !  │ Filtre Temizlik Gerekli  │ 14:10:01     │ 00:15:19 │[Onayla] │
└────┴────┴──────────────────────────┴──────────────┴──────────┴──────────┘

Öncelik: 🔴 Kritik  🟠 Yüksek  🟡 Orta  🔵 Düşük
Durum  : ! = Onaylanmamış (yanıp söner)   ✓ = Onaylandı (sabit)
```

**Alarm Geçmişi:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│  ALARM GEÇMİŞİ                                                          │
│  Dönem: [Son 24 Saat ▼]   Öncelik: [Tümü ▼]   [Excel İndir]           │
├────┬──────────────────────────┬──────────┬──────────┬──────────┬────────┤
│Önc │ Açıklama                 │ Başlangıç│ Bitiş    │ Süre     │Onaylayan│
├────┼──────────────────────────┼──────────┼──────────┼──────────┼────────┤
│ 🔴 │ Konveyör 2 Motor Arızası │ 14:23:05 │ 14:35:22 │ 00:12:17 │ Ahmet K│
│ 🟠 │ Hat 1 Sıcaklık Yüksek    │ 14:21:33 │ 14:28:45 │ 00:07:12 │ Ahmet K│
│ 🟡 │ Yağlama Basınç Düşük     │ 12:15:00 │ 12:18:30 │ 00:03:30 │ Mehmet │
└────┴──────────────────────────┴──────────┴──────────┴──────────┴────────┘
```

### HMI Alarm Veri Yapısı

```typescript
// TypeScript tip tanımlaması
interface AlarmRecord {
    id: string;                              // Benzersiz alarm ID
    name: string;                            // Alarm adı (PLC'den)
    description: string;                     // Açıklama
    priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
    state: 'ACTIVE_UNACK' | 'ACTIVE_ACK' | 'RTN_UNACK' | 'NORMAL';
    activeTime: Date;                        // Alarm aktif olduğu an
    acknowledgeTime: Date | null;           // Onaylanma zamanı
    acknowledgedBy: string | null;          // Onaylayan kullanıcı
    clearTime: Date | null;                 // Alarm kapandığı an
    value: number | boolean | null;         // Alarm tetikleyen değer
    limit: number | null;                   // Alarm limiti
    unit: string;                           // Birim
    causeNote: string;                      // Olası neden
    actionNote: string;                     // Önerilen eylem
    area: string;                           // Hat/Bölge
    equipment: string;                      // Ekipman adı
    shelved: boolean;                       // Geçici bastırılmış mı?
    suppressed: boolean;                    // Bakım bastırması var mı?
}
```

### Alarm Onaylama (Acknowledge) Mantığı

```javascript
// Alarm onaylama API
async function acknowledgeAlarm(alarmId, userId, note = '') {
    const alarm = await db.alarms.findById(alarmId);
    
    // Doğrulama: Alarm aktif ve onaylanmamış mı?
    if (alarm.state !== 'ACTIVE_UNACK' && alarm.state !== 'RTN_UNACK') {
        throw new Error('Alarm zaten onaylanmış veya normal durumda');
    }
    
    // Kullanıcı yetkisi kontrol
    const user = await auth.getUser(userId);
    if (!user.permissions.includes('alarm.acknowledge')) {
        throw new Error('Bu kullanıcının alarm onaylama yetkisi yok');
    }
    
    // Durumu güncelle
    await db.alarms.update(alarmId, {
        state: alarm.state === 'ACTIVE_UNACK' ? 'ACTIVE_ACK' : 'NORMAL',
        acknowledgeTime: new Date(),
        acknowledgedBy: userId,
        acknowledgeNote: note
    });
    
    // PLC'ye onay sinyali gönder (opsiyonel)
    await plc.writeTag(`Alarm.${alarm.plcTagName}.Acknowledge`, true);
    
    // HMI'a broadcast
    broadcastAlarmUpdate(alarmId);
    
    // Log
    logger.info(`Alarm acknowledged: ${alarm.name} by ${userId}`);
}
```

### Sesli Uyarı Yönetimi

```javascript
// Alarm ses yönetimi
class AlarmAudioManager {
    constructor() {
        this.audioContext = new AudioContext();
        this.alarmSound = new Audio('/sounds/alarm_critical.wav');
        this.warningSound = new Audio('/sounds/alarm_warning.wav');
        this.isMuted = false;
        this.activeAlarmCount = 0;
    }
    
    // Alarm durumuna göre ses çal
    updateAlarmState(alarms) {
        const unacknowledgedCritical = alarms.filter(
            a => a.priority === 'CRITICAL' && a.state === 'ACTIVE_UNACK'
        );
        const unacknowledgedHigh = alarms.filter(
            a => a.priority === 'HIGH' && a.state === 'ACTIVE_UNACK'
        );
        
        if (this.isMuted) return;
        
        if (unacknowledgedCritical.length > 0) {
            // Kritik: Sürekli alarm sesi
            this.playLoop(this.alarmSound);
        } else if (unacknowledgedHigh.length > 0) {
            // Yüksek: Aralıklı uyarı sesi
            this.playInterval(this.warningSound, 5000);  // 5 saniyede bir
        } else {
            this.stopAll();
        }
    }
    
    // Tümünü onayla veya sessiz
    muteTemporary(durationMs = 60000) {
        this.isMuted = true;
        this.stopAll();
        setTimeout(() => {
            this.isMuted = false;
        }, durationMs);
    }
    
    // ...
}
```

## Örnekler

### Örnek 1: Alarm Mesajı Formatı — İyi vs Kötü

```
Kötü alarm mesajı (çoğu yerleşik SCADA'nın varsayılanı):
  "ALARM: TAG_CONV2_MOTOR_TEMP"
  → Operatör: Ne yapacağım? Nereye bakacağım?

İyi alarm mesajı (ISA-18.2 uyumlu):
  Öncelik: YÜKSEK
  Açıklama: "Konveyör 2 Motor Sıcaklığı Yüksek"
  Değer: 88°C (Limit: 85°C)
  Neden: Motor aşırı yüklenmiş veya soğutma sistemi arızalı olabilir.
  Eylem: Motor yükünü azaltın veya Bakım'ı çağırın.
         FR Panel'i kontrol edin (Bina B, Hat 2 elektrik panosu).
```

### Örnek 2: Alarm Flood Senaryosu ve Çözümü

```
Olay: Konveyör ana motor durdu.
Sonuç: 45 alarm 30 saniye içinde aktive oldu (bağımlı alarmlar).

Kök neden: 1 arıza → 45 bağımlı alarm.
Operatör bakışından: "Hangi alarm birincil? Nereden başlayayım?"

ISA-18.2 çözümü: Alarm bastırma (Suppression) ile kök neden önce gösterilir.

Kural tanımla:
  IF Konveyör_Motor_Arızalı THEN
    Suppress: Konveyör_Sensör_*, Konveyör_Hız_*, Hat_Üretim_*
  END_IF
  
Sonuç: 1 kritik alarm + 44 bastırılmış bildirim.
Operatör: Tek bir kritik alarmla yönlendiriliyor.
```

### Örnek 3: Renk Körü Erişilebilirliği

```
Yalnızca renkle alarm gösterimi (KÖTÜ):
  🔴 = Kritik    🟠 = Yüksek    🟡 = Orta
  → Kırmızı-yeşil renk körü için farksız.

Renk + Şekil + Pozisyon + Yanıp Sönme (İYİ):
  ▲▲▲ + Kırmızı arka plan + Yanıp söner = KRİTİK
  ▲▲  + Turuncu arka plan + Sabit      = YÜKSEK  
  ▲   + Sarı arka plan   + Sabit      = ORTA
  ●   + Mavi arka plan   + Sabit      = DÜŞÜK
```

## Sık Yapılan Hatalar

### Hata 1: Her Şeyi Alarm Yapmak

```
Mühendis: "Her şeyi alarm yapalım, güvenli olsun."
Sonuç: Operatör başına 500+ alarm/gün.
        Kritik alarmlar gürültüde kaybolur.
        Alarm körlüğü → Gerçek alarm gözden kaçar.

ISA-18.2: "Event" alanını kullan. Müdahale gerektirmeyen
           her bildirim Event log'una gider, Alarm listesine değil.
```

### Hata 2: Acknowledge = Çözüldü Sanmak

```
Operatör alarmı onayladı → Alarm listesinden silindi.
Sorun: Koşul hâlâ aktif! Motor hâlâ aşırı yüklenmiş.
       "Onaylandı" = "Gördüm", "Normal duruma döndü" değil.

HMI tasarımı: Onaylandı + Hâlâ Aktif → Listede kalır (farklı renk/ikon).
               Yalnızca koşul gerçekten düzelince kaybolur.
```

### Hata 3: Alarm Geçmişi Olmamak

```
"Gerçi bu alarm dün de olmuştu, ama kim onayladı?"
Takip yok, hesap sorulabilirlik yok, kök neden analizi imkânsız.

Zorunlu bilgiler alarm log'unda:
  timestamp_aktif, timestamp_onayli, timestamp_kapandi,
  onaylayan_kullanici, alarm_suresi, onay_notu
```

### Hata 4: Alarm Sesi Yönetimi Olmadan Deploy

```
Kritik alarm geldi → Siren çalıyor.
Operatör alarmı onayla → Siren hâlâ çalıyor (koşul aktif).
Operatör: "Neden hâlâ çalıyor? Onayladım ya!"

ISA-18.2 önerisi:
  Siren: Onaylanmamış alarm için çalar.
  Alarm onaylanınca: Siren durur.
  Koşul aktif kalsa da: Siren durmuş, alarm listesinde görünüyor.
  → Siren "onaylanmamış" için, alarm listesi "aktif" için.
```

## Gerçek Proje Notları

**Not 1 — "Worst Actor" Analizi ile Alarm Sayısı Yarıya İndi**  
Bir fabrikada 1200 aktif alarm tanımlanmıştı. ISA-18.2 "worst actor" analizi yapıldı: En sık tetiklenen 20 alarm, tüm alarm vakalarının %60'ını oluşturuyordu. Bu 20 alarmın 14'ü aslında gereksizdi (event olmalıydı) veya limitleri yanlış ayarlanmıştı. 3 ay içinde alarm sayısı 1200'den 580'e indi, operatör memnuniyeti arttı.

**Not 2 — Alarm Körlüğünün Fiziksel Sonucu**  
Bir tesiste günde 800+ alarm aktive oluyordu. Operatörler "bunları görmezden geliyoruz" dedi. Kritik bir kompresör alarmı bu kalabalıkta kayboldu, 4 saat fark edilmedi. Kompresör hasarlı oldu. Alarm yeniden tasarımı: 600 alarm → 180'e düşürüldü, kritikler net ayrıldı.

**Not 3 — Alarm Onaylama Sonrası Kapanma Beklentisi**  
Bir operatör "Onayladım ama alarm hâlâ listede. Bu normal mi?" diye sordu. Onayla = gördüm; koşul aktif kalabilir. Bu fark HMI eğitimde işlenmemişti. Alarm listesinde görsel ayrım iyileştirildi: Onaylanmış+Aktif = turuncu (sabit), Onaylanmamış+Aktif = kırmızı (yanıp söner).

**Not 4 — Chattering Alarm: Bir Sensör, Bir Günde 4000 Olay**  
Bir basınç switch'i tam alarm eşiğinin (4.0 bar) sınırında salınıyordu: 4.01 → alarm aktif, 4.00 → alarm normal, saniyede birkaç kez. Tek bir tag bir günde 4000+ alarm-aktif/normal olayı üretti, alarm geçmişi log'unu doldurdu ve gerçek alarmları gömdü. Bu klasik **chattering** (gevezelik). Çözüm iki katmanlı: (1) PLC tarafında **hysteresis (deadband)** — alarm 4.0'da aktif olur ama yalnızca 3.8'in altına düşünce normale döner; (2) **on-delay / off-delay debounce** — koşul en az 2 saniye sürmeden alarm tetiklenmez. Olay sayısı 4000 → 12'ye indi. Ders: chattering'in çözümü HMI'da filtreleme değil, alarm koşulunun kaynağında hysteresis + zaman gecikmesidir.

**Not 5 — Shelving Süresinin Olmaması: Unutulan Alarm**  
Bir teknisyen bakım sırasında gürültü yapan bir alarmı "shelve" etti (geçici sustur). Ama HMI'da shelving'in zaman aşımı yoktu — alarm süresiz bastırılmış kaldı. 3 hafta sonra aynı ekipmanda gerçek bir arıza oluştu; alarm hâlâ shelved olduğu için operatöre hiç görünmedi. ISA-18.2 shelving'in **maksimum süreli** ve **otomatik geri-dönüşlü** olmasını şart koşar. Çözüm: Her shelve işlemine zorunlu süre (max 8 saat = vardiya) + süre dolunca otomatik un-shelve + "shelved alarmlar" özel ekranı (kaç tane, kim, ne zamana kadar). Ders: shelving güçlü ama denetimsiz bırakılırsa alarmı kalıcı olarak kör eder; süre limiti ve görünürlük zorunlu.

**Not 6 — Alarm Önceliğinin "Risk" Yerine "Mühendisin Hissi" ile Atanması**  
Bir projede önceliklendirme rasyonalizasyon (alarm rationalization) yapılmadan, mühendislerin sezgisiyle atanmıştı. Sonuç: alarmların %40'ı "Kritik" işaretliydi (ISA-18.2 tavanı %5). Her şey kırmızı olunca hiçbir şey kritik değildi. ISA-18.2 önceliği **sonuç şiddeti × müdahaleye kalan süre** matrisiyle (risk-tabanlı) belirler. Rasyonalizasyon çalıştayı yapıldı: her alarm için "müdahale edilmezse ne olur, ne kadar sürede olur" soruldu. Kritik oran %40 → %4'e indi. Ders: öncelik subjektif atanamaz; risk matrisi ile rasyonalize edilmeli, aksi halde öncelik anlamını yitirir.

## Edge Case'ler ve Sistem Limitleri

Alarm sistemi en çok "anormal anın anormal anı"nda — yani aynı anda çok şey ters gittiğinde — sınanır. Aşağıdaki tablo bu sınır koşulları toplar.

| Edge Case | Tetikleyen Koşul | Belirti | Doğru Davranış |
|---|---|---|---|
| Chattering | Değer alarm eşiğinde salınıyor | Tek tag binlerce olay/gün, log şişer | Hysteresis (deadband) + on/off-delay (kaynakta) |
| Alarm flood | Tek kök arıza → onlarca bağımlı alarm | Operatör birincili bulamaz | Kök-neden suppression / first-out mantığı |
| Süresiz shelving | Shelve'e zaman limiti yok | Gerçek alarm kalıcı bastırılır | Max süre + otomatik un-shelve + shelved ekranı |
| Stale alarm state | OPC UA kopuk, alarm durumu donmuş | "Aktif" alarm aslında belirsiz | Bağlantı kopunca alarm durumu "BELİRSİZ" işaretle |
| Öncelik enflasyonu | Risk-tabanlı rasyonalizasyon yok | Kritik oranı %5'i aşar, anlam kaybı | Risk matrisi ile rasyonalizasyon çalıştayı |
| Ack yarış durumu | İki operatör aynı alarmı aynı anda onaylar | Çift kayıt / tutarsız ackBy | Sunucu-tarafı atomik durum geçişi (idempotent) |
| Siren mantık hatası | Siren koşula bağlı, ack'e değil | Ack sonrası siren susmaz | Siren = onaylanmamış alarm var; ack → sus |
| Zaman damgası kaynağı | HMI ack zamanını kendi saatiyle yazar | SoE sırası bozulur | PLC/server timestamp'i kaynak al (SoE) |

**Sayısal limitler ve ISA-18.2 metrikleri:**
```
Hedef alarm oranı (kararlı)  : ~1 alarm / 10 dakika / operatör (çok iyi)
Kabul edilebilir tavan       : <10 alarm / 10 dakika / operatör
Flood eşiği (ISA-18.2)       : >10 alarm / 10 dakika = "alarm flood" durumu
Kritik öncelik oranı         : Toplam alarmların ≤%5
Yüksek öncelik oranı         : Toplam alarmların ≤%15
Öncelik seviye sayısı        : 3-4 (fazlası operatörü zorlar)
Shelving max süre            : Tipik 1 vardiya (≤8 saat), sonra oto un-shelve
Hysteresis (deadband)        : Ölçüm aralığının ~%1-5'i (sürece bağlı)
Debounce (on-delay)          : Gürültülü ayrık sinyal için 1-5 saniye
```

## Optimizasyon

Alarm sisteminde "optimizasyon" performanstan önce **bilişsel optimizasyondur**: amaç operatörün doğru anda doğru alarmı görmesidir. Teknik optimizasyon (log, render) ikincildir.

**Optimizasyon önceliği (operatör bilişinden teknik katmana):**
```
1. RASYONALİZASYON — Alarm sayısını ve önceliğini doğru belirle (en yüksek etki)
   → "Worst actor" analizi: en sık tetikleyen 20 alarm tüm vakaların ~%60'ı
   → Gereksiz alarmları event'e çevir; limitleri düzelt
   → Risk-tabanlı önceliklendirme: kritik ≤%5

2. KAYNAKTA FİLTRELEME — Gürültüyü alarm olmadan önce kes
   → Hysteresis (deadband) + on/off-delay → chattering biter
   → İlişkili alarmları gruplama (group alarm)

3. FLOOD YÖNETİMİ — Çok-alarm anını sadeleştir
   → Kök-neden suppression: birincil arıza → bağımlıları bastır
   → "First-out" : ilk tetikleneni vurgula
   → Dinamik alarm bastırma (proses durumuna göre — ör. "ünite durmuşken
     o üniteye ait alarmları gösterme")

4. SUNUM — Operatörün taramasını hızlandır
   → Önceliğe göre sıralama + renk + şekil + konum
   → Alarm banner her ekranda (modal üstü)

5. TEKNİK — Log/render verimliliği (en son)
   → Alarm geçmişini indeksli/zaman-serili DB'de tut, sayfalama
   → Aktif liste için delta güncelleme; tüm listeyi her olayda yeniden çizme
```

**Dinamik (state-based) suppression — neden statik kuraldan üstün:**
```
Statik suppression: "Konveyör motoru arızalıysa sensör alarmlarını bastır"
  → Sabit kural, her durumda aynı.

Dinamik suppression: Proses moduna göre alarm seti değişir.
  Ünite "Bakımda"      → o ünitenin tüm proses alarmları beklenir, bastır
  Ünite "Başlatılıyor" → düşük-sıcaklık alarmı normal, bastır
  Ünite "Çalışıyor"    → tüm alarmlar aktif
  → ISA-18.2 "state-based alarming". Flood'u kaynağında %70+ azaltabilir.
```

## Derin Teknik Detay

**Alarm durum makinesinin iç ayrışımı — neden iki bağımsız boyut:**
Bir alarmın HMI durumu tek bir değişken değil, **iki ortogonal boyutun** çarpımıdır:
```
Boyut 1 — Koşul durumu (process condition):  ACTIVE | NORMAL  (PLC'den gelir)
Boyut 2 — Onay durumu (acknowledgement):     UNACK  | ACK     (operatörden gelir)

Çarpım → 4 anlamlı durum:
  ACTIVE + UNACK  : koşul var, görülmedi   → kırmızı, yanıp söner, siren
  ACTIVE + ACK    : koşul var, görüldü     → turuncu sabit, siren susar
  NORMAL + UNACK  : koşul gitti, görülmedi → sarı sabit (RTN-unack), kayda değer
  NORMAL + ACK    : koşul gitti, görüldü   → listeden çıkar (NORMAL)
```
Bu ortogonallik neden kritik? Çünkü iki boyut **iki farklı aktör** tarafından, **bağımsızca** değiştirilir: koşulu PLC değiştirir (fiziksel gerçeklik), onayı operatör değiştirir (insan eylemi). Tek değişkene indirgemek (ör. "onaylandı = silindi") Hata 2'nin tam kaynağıdır: operatör onayı koşulu *değiştirmez*, sadece "gördüm" der. Siren mantığı da bu ayrımdan türer: siren Boyut 2'ye (UNACK var mı) bağlıdır, Boyut 1'e (ACTIVE) değil — bu yüzden ack siren'i susturur ama alarmı listeden silmez. RTN-unack durumu özellikle önemlidir: koşul geçici belirip kaybolduysa (transient) operatör bunu *kaçırmamalı* — bu yüzden kaybolmuş ama onaylanmamış alarm yine de listede tutulur.

**Hysteresis ve debounce'un matematiksel gerekçesi:**
```
Tek eşik (sadece limit):           Hysteresis (iki eşik):
  alarm = (x > 4.0)                  IF x > 4.0 THEN alarm := TRUE
  x = 4.0 ± gürültü → titrer         IF x < 3.8 THEN alarm := FALSE
                                     (3.8-4.0 ölü banttır, durum korunur)

Debounce (zaman boyutu):
  alarm yalnızca koşul T süre KESİNTİSİZ sürerse tetiklenir.
  Ayrık (digital) gürültülü sinyallerde hysteresis anlamsız (0/1) → debounce şart.
```
Hysteresis genliği gürültü genliğinden büyük olmalıdır; aksi halde işe yaramaz. Pratikte hysteresis (analog değerler için) ve debounce (ayrık sinyaller için) birlikte kullanılır. Bu mantık **PLC'de** olmalıdır, HMI'da değil: HMI sadece alarm *durumunu* görselleştirir, alarm *koşulunu* üretmez. HMI'da filtreleme yapmak demek, başka bir HMI istemcisinin filtrelenmemiş alarmı görmesi ve tutarsızlık demektir.

**Sequence of Events (SoE) ve timestamp kaynağı — flood'da first-out neden HMI saatiyle yapılamaz:**
Alarm flood'da "hangi alarm önce tetiklendi" (first-out) sorusu kök-neden analizinin temelidir. Ama 45 alarm 30 saniyede gelirse ve sıralama HMI'ın *alarmı aldığı* zamana göre yapılırsa, ağ gecikmesi/işleme sırası gerçek sırayı bozar. Bu yüzden ciddi sistemlerde alarm timestamp'i **olayın kaynakta (PLC'de) oluştuğu an** ile damgalanır (OPC UA Alarms & Conditions'da `Time` alanı, PLC'de SoE buffer). HMI bu kaynak-timestamp'e göre sıralar. Milisaniye-doğruluğunda first-out gereken yerlerde (elektrik şalt, koruma rölesi) PTP/IEEE-1588 saat senkronu ve PLC SoE modülleri kullanılır — HMI yalnızca sunucudur.

**Ack işleminin idempotent ve atomik olması:**
İki operatör (iki istasyon) aynı alarmı aynı anda onaylarsa, ikisi de aynı `ACTIVE_UNACK → ACTIVE_ACK` geçişini tetikler. `acknowledgeAlarm` fonksiyonu (bkz. örnek kod) bu yüzden sunucu tarafında **atomik durum kontrolü** yapmalıdır: "zaten ACK ise tekrar ACK yazma, ilk onaylayanı koru". Aksi halde `acknowledgedBy` ikinci operatöre overwrite olur, audit trail yanlış kişiyi gösterir. Doğru desen: durum geçişini koşullu güncelleme (compare-and-set) ile yap; ikinci istek "zaten onaylanmış" yanıtı alsın, sessizce başarılı olsun (idempotent).

## İlgili Konular

```
knowledge/hmi/architecture/
├── 01_hmi_patterns.md           → Alarm ekranlarının yeri
├── 02_realtime_data.md          → Alarm güncellemelerinin hızı
└── 04_user_auth.md              → Alarm onaylama yetkisi

ISA Standartları:
  ISA-18.2 (ANSI/ISA-18.2-2016) → Alarm yönetimi yaşam döngüsü
  ISA-TR18.2.4                   → Gelişmiş alarm yöntemleri
  ISA-TR18.2.6                   → Kesintili ve ayrık prosesler için
  ISA-101.01                     → HMI tasarım standardı (alarm sunum)
```
