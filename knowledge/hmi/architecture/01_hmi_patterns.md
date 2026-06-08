---
KONU        : HMI Mimari Kalıpları
KATEGORİ    : hmi
ALT_KATEGORI: architecture
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://www.isa.org/standards-and-publications/isa-standards/isa-101-standards"
    başlık: "ISA — ISA-101 Series of Standards"
    güvenilirlik: resmi
  - url: "https://www.iotindustries.sk/en/blog/isa-101/"
    başlık: "IoT Industries — ISA-101: The Standard for Modern HMI Interfaces"
    güvenilirlik: topluluk
  - url: "https://www.realpars.com/blog/high-performance-hmi"
    başlık: "RealPars — What Is High-Performance HMI?"
    güvenilirlik: topluluk
  - url: "https://plcprogramming.io/blog/hmi-design-best-practices-complete-guide"
    başlık: "PLCProgramming.io — HMI Design Best Practices 2026"
    güvenilirlik: topluluk
  - url: "https://www.code-brew.com/hmi-software-development-guide/"
    başlık: "Code-Brew — HMI Software Development Guide for 2026"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "02_realtime_data.md"
    ilişki: tamamlar
  - konu: "03_alarm_management.md"
    ilişki: tamamlar
  - konu: "04_user_auth.md"
    ilişki: tamamlar
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/modbus-tcp/01_protocol_basics.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "OPC UA veya Modbus TCP temel kavramları"
  - "Web tabanlı veya masaüstü uygulama geliştirme deneyimi"
ÇELİŞKİLER :
  - kaynak: "ISA-101 'gri ekran' tasarımı ile operatör beğenisi çatışması"
    konu: "ISA-101 gri/nötr renk paleti önerir; operatörler renkli arayüzlere alışkındır"
    çözüm: >
      ISA-101, dekoratif rengi değil anlamlı rengi savunur. Gri/nötr renk
      normal durumu temsil eder; alarm ve anormallik koşullarında renk ön plana çıkar.
      Operatörler başlangıçta "sıkıcı" bulur ama birkaç ay kullanım sonra
      alarmları çok daha hızlı fark eder. Geçişte eğitim şart.
  - kaynak: "Web HMI vs TargetVisu / WinCC — hangisi tercih edilmeli?"
    konu: "Modern web teknolojileri mi, SCADA platformunun yerleşik HMI'ı mı?"
    çözüm: >
      SCADA platformu HMI (WinCC, FactoryTalk, IgnitionPerspective): Hızlı tag bağlama,
      yerleşik alarm/historian, düşük öğrenme eğrisi; kilitli vendor ekosistemi.
      Web HMI (React, Vue, WebSocket): Platform bağımsız, modern UX, esneklik;
      protokol köprüsü gerektirir, alarm/historian kendin yazarsın.
      Büyük projeler: SCADA platform. Küçük/özel: Web teknolojileri.
---

## Özün Ne

Endüstriyel HMI (Human-Machine Interface), operatörlerin makineleri izlediği ve kontrol ettiği arayüzdür. Kurumsal bir web uygulamasından temel farkı şudur: Hata kurtarımı yoktur. Bir e-ticaret sitesinde yanlış düğmeye basıldığında "Geri Al" vardır; bir motor kontrol HMI'ında yanlış düğme fabrika durmasına veya yaralanmaya yol açabilir. Bu kritiklik, HMI mimarisini baştan sona etkiler: Veri güncelliği, alarm önceliği, yazma doğrulaması, bağlantı kopma davranışı — hepsi farklı bir titizlikle tasarlanmalıdır.

## Nasıl Çalışır

### Veri Akışı Mimarisi

HMI, üç temel operasyonu gerçekleştirir:

```
┌──────────────────────────────────────────────────────────────┐
│                    HMI Uygulama                              │
│                                                              │
│  OKUMA (Read)          GÖRÜNTÜLEME (Display)   YAZMA (Write) │
│  PLC'den değerleri ← → Ekranda göster      → PLC'ye komut  │
│  al (polling/sub)       animasyonlar           (onay sonrası)│
└──────────────────────────────────────────────────────────────┘
           │                                        │
           │ OPC UA Subscription              OPC UA Write
           │ Modbus Polling                   Modbus Write
           │ MQTT Subscribe                   (OPC UA method)
           ▼                                        ▼
    ┌──────────────────────────────────────────────────┐
    │                    PLC / SCADA                    │
    │    Gerçek veri, kontrol mantığı, alarm durumu    │
    └──────────────────────────────────────────────────┘
```

### Veri Kaynakları

HMI'ın PLC'den veri alacağı protokol ilk mimari kararıdır:

```
OPC UA (Önerilir — Modern sistemler):
  ✓ Subscription: Değer değişince otomatik bildirim
  ✓ Zengin metadata (birim, veri tipi, timestamp, kalite)
  ✓ Güvenli şifreli bağlantı
  ✓ Browse: Tag listesi otomatik keşif
  → Gecikme: <1ms (LAN), 5-50ms (WAN)
  → Kaynak: Node tarafı (CODESYS Symbol Config)

Modbus TCP (Yaygın — Legacy sistemler):
  ✓ Evrensel uyumluluk
  ✓ Basit polling döngüsü
  ✗ Güvenlik yok
  ✗ Metadata yok (register belgeden öğrenilir)
  → Gecikme: 1-10ms (LAN)

MQTT (Bulut/analitik bileşen):
  ✓ Event-driven, düşük overhead
  ✓ Çok alıcıya aynı anda
  ✗ İki yönlü kontrol için ek mekanizma gerekir
  → HMI read için MQTT, write için OPC UA/Modbus kombinasyon

WebSocket + Backend API (Web HMI'ı için):
  → Backend: OPC UA/Modbus istemcisi
  → Frontend: WebSocket ile gerçek zamanlı push
  → Ayrı belge: 02_realtime_data.md
```

### ISA-101 — HMI Tasarım Standardı

ANSI/ISA-101.01-2015 "Human Machine Interfaces for Process Automation Systems" standardı, HMI tasarımı için kapsamlı bir çerçeve sunar. Temel ilkeleri:

**1. Ekran Hiyerarşisi (Display Hierarchy):**
```
Seviye 1 — Genel Bakış (Overview):
  Tüm tesisin / hattın özet görünümü.
  KPI'lar, genel durum, aktif alarmlar özeti.
  En az detay, en fazla bağlam.

Seviye 2 — Alan (Area):
  Belirli bir üretim alanı veya hat.
  Ekipmanlar görünür, kritik değerler.

Seviye 3 — Detay (Detail):
  Tekil makine veya proses birimi.
  Tüm ölçümler, setpointler, komutlar.

Seviye 4 — Destek/Diagnostik (Support):
  Bakım bilgileri, kalibrasyon, trend grafikleri.
  Operatörden çok teknisyen/mühendis için.

Navigasyon kuralı: Operatör herhangi bir noktaya
≤3 tıklamayla ulaşabilmeli.
```

**2. Renk Kullanımı:**
```
Normal durum   : Gri / Nötr tonlar
  → Ekran sakin, göz yorulmuyor
  → Motor çalışıyor: Açık gri
  → Motor durmuş: Koyu gri

Uyarı          : Sarı / Turuncu
  → "Dikkat, izle"

Alarm (Kritik) : Kırmızı (YALNIZCA alarm için!)
  → Kırmızı başka hiçbir amaçla kullanılmaz
  → "Hemen müdahale gerekiyor"

Bilgi          : Mavi
  → Seçili durum, bilgi mesajları

Başarı / OK    : Yeşil (sadece onay için)
  → Kırmızı/yeşil renk körü için: Şekil + renk birlikte kullan

Kural: Eğer ekranınız normalde çok renkli ve
       bir alarm gelince fark edilmiyorsa → ISA-101 uygulayın.
```

**3. Yazı ve Görsel Hiyerarşi:**
```
Başlık        : 14-16pt, bold, koyu renk
Değer (sayı)  : 12-14pt, mono font (Courier/Consolas)
                → Sayıların sütun hizası bozulmasın
Birim         : 10-12pt, değerin yanında
Etiket        : 10-12pt, değerin üstünde veya solunda
Durum metni   : 10pt, uppercase (RUNNING, STOPPED, FAULT)
```

**4. Hareket ve Animasyon:**
```
Endüstriyel HMI'da animasyonu minimize et:
  ❌ Dönen dişliler, akan sıvı animasyonları, yanıp sönen renkler
  → Operatör dikkatini dağıtır, kafa karıştırır

  ✅ Alarm durumunda yanıp sönen çerçeve (yanıp sönen renk değil)
  ✅ Alarm onaylandıktan sonra sabit renk
  ✅ Seviye göstergesi gerçek zamanlı güncelleme (animasyon değil, sayı)
```

### Ekran Tasarım Kalıpları

**Kalıp 1 — Ana Sayfa (Dashboard)**
```
┌────────────────────────────────────────────────────────────────┐
│  [Logo]  Hat 1 | Hat 2 | Hat 3 | Alarmlar | Raporlar | Çıkış │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐ │
│  │ Hat 1    │  │ Hat 2    │  │ Enerji   │  │ AKTİF ALARMLAR│ │
│  │ ████████ │  │ ████████ │  │ 245 kW   │  │ 3 Kritik      │ │
│  │ ÇALIŞIYOR│  │ DURMUŞ   │  │          │  │ 7 Yüksek      │ │
│  │ 450 adet │  │ 0 adet   │  │ 82% OEE  │  │ 2 Orta        │ │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

**Kalıp 2 — Detay Sayfası**
```
┌────────────────────────────────────────────────────────────────┐
│ [◄ Genel] Hat 1 / Motor 1 Detay                    [Alarmlar] │
├────────────────────────────────────────────────────────────────┤
│  Durum: ████ ÇALIŞIYOR                                         │
│                                                                 │
│  Hız Setpoint  : [45.0 m/dk ▼] [Uygula]                      │
│  Gerçek Hız    : 44.8 m/dk                                     │
│  Motor Akımı   : 12.3 A                                        │
│  Motor Sıcaklığı: 68°C  ████████░░ (max: 85°C)                │
│                                                                 │
│  Toplam Çalışma: 1234.5 saat                                   │
│  Başlatma Sayısı: 342                                          │
│                                                                 │
│  [Başlat] [Durdur] [Reset]        Son alarm: Motor Sıcaklık   │
└────────────────────────────────────────────────────────────────┘
```

**Kalıp 3 — Alarm Listesi (Bant)**
```
┌────────────────────────────────────────────────────────────────┐
│ Alarm Listesi                          Filtre: [Tümü ▼]       │
├──────┬───────────────────┬──────────────┬──────────┬──────────┤
│ Önce │ Açıklama          │ Zaman        │ Durum    │ İşlem    │
├──────┼───────────────────┼──────────────┼──────────┼──────────┤
│  🔴  │ Motor 1 Sıcaklık  │ 14:23:05     │ AKTİF    │ [Onaylar]│
│  🟠  │ Hız Tolerans Aşım │ 14:21:33     │ AKTİF    │ [Onaylar]│
│  🟡  │ Yağ Basınç Düşük  │ 14:18:47     │ ONAYLANDI│          │
└──────┴───────────────────┴──────────────┴──────────┴──────────┘
```

### Endüstriyel HMI vs Kurumsal Web Uygulaması

```
Özellik              Endüstriyel HMI         Kurumsal Web Uygulaması
──────────────────────────────────────────────────────────────────────
Veri güncelliği      <1s kritik              Birkaç saniye tolere edilir
Hata kurtarma        Yok (fiziksel sonuç)    "Geri Al" mekanizması var
Kullanıcı sayısı     Az (1-10 operatör)      Çok (yüzler-binler)
Bağlantı kopması     Kırmızı uyarı gerekli   "Lütfen yenileyin" yeterli
Yetkilendirme        Fiziksel güvenlik ek    Yalnızca yazılımsal
Kullanım ortamı      Fabrika zemini, eldiven Ofis masası, fare + klavye
Ekran boyutu         Sabit (21"-32" panel)   Çeşitli (mobil dahil)
Sesli uyarı          Alarm buzzer            Yok
Uluslararası norm    ISA-101, ISA-18.2       WCAG, Material Design
```

### Mimari Yaklaşımlar

**Seçenek A: SCADA Platformu HMI**
```
Wonderware InTouch / Siemens WinCC / Ignition / FactoryTalk

Yapı:
  SCADA platform → Tag database → Display scripts → Screen
  
Avantajlar:
  Hızlı geliştirme (sürükle-bırak)
  Yerleşik OPC UA/Modbus bağlantısı
  Alarm/historian dahili
  Vendor destek ve eğitim
  
Dezavantajlar:
  Lisans maliyeti (yüksek)
  Vendor bağımlılığı
  Eski görünüm/his (bazı platformlar)
  Kısıtlı özelleştirme
```

**Seçenek B: Web Tabanlı HMI**
```
React / Vue / Svelte + WebSocket + Backend (Node.js/Python)

Yapı:
  Browser ← WebSocket → Backend API → OPC UA/Modbus → PLC
  
Avantajlar:
  Platform bağımsız (herhangi bir tarayıcı)
  Modern UX imkânı
  Açık kaynak, sıfır lisans
  Git ile versiyon kontrolü
  Mobil uyumlu
  
Dezavantajlar:
  Alarm/historian kendin yazarsın
  OPC UA köprüsü gerekli (node-opcua, opcua-asyncio)
  Gerçek zamanlılık için dikkatli WebSocket tasarımı
  Ekip frontend geliştirme bilmeli
  
Kütüphaneler:
  node-red-dashboard → Hızlı prototip
  ICONICS WebHMI     → Endüstriyel web platformu
  InfluxDB + Grafana → Monitoring dashboard (salt okuma)
```

**Seçenek C: CODESYS WebVisu / TargetVisu**
```
CODESYS dahili visualization motor

Avantajlar:
  PLC ile aynı ortamda
  Doğrudan değişken bağlama
  Lisans dahil (CODESYS SL'ye bağlı)
  
Dezavantajlar:
  Sınırlı modern UI özelliği
  Büyük projelerde performans sorunu
  Çok sayfalı navigasyon kısıtlı
  Web versiyonu (WebVisu): HTTP, HTTPS seçeneği
```

### Bileşen Tabanlı Tasarım

Yeniden kullanılabilir bileşenler HMI geliştirmeyi dramatik hızlandırır:

```
Standart Bileşen Kütüphanesi:

Motor_Status_Widget (xRunning, xFault, sName)
  → Her motor için aynı widget, farklı parametreler

Analog_Gauge (rValue, rMin, rMax, sUnit, rAlarmHigh, rAlarmLow)
  → Sıcaklık, basınç, hız için ortak gösterge

Alarm_Banner ()
  → Her sayfada aynı alarm özeti şeridi

Trend_Chart (sTagName, nMinutes)
  → Son N dakika trendi

SetpointControl (rCurrentValue, rSetpoint, sUnit, rMin, rMax)
  → Doğrulama, yetki kontrolü dahil
```

## Örnekler

### Örnek 1: ISA-101 Renk Dönüşümü

```
Öncesi (kötü pratik):
  Motor çalışıyor → Parlak yeşil doldurma
  Motor durmuş   → Kırmızı doldurma
  Alarm          → Yanıp sönen kırmızı

Sonrası (ISA-101):
  Motor çalışıyor → Açık gri, beyaz metin "RUNNING"
  Motor durmuş    → Koyu gri, beyaz metin "STOPPED"
  Motor alarm     → Gri arka plan, kırmızı çerçeve/ikon, "FAULT"
  (Kırmızı YALNIZCA alarm için kullanılır)

Sonuç: Operatör gürültülü ortamda alarm durumunu
       daha hızlı fark etti (%40 daha hızlı tepki — gerçek vaka).
```

### Örnek 2: Üç Tıklama Kuralı

```
Operatör Motor 7'yi durdurmak istiyor:
  Tıklama 1: Dashboard → Hat 2
  Tıklama 2: Hat 2 → Motor 7 Detay
  Tıklama 3: Motor 7 Detay → [Durdur] butonu
  
Üç tıklama. ✓

Eğer Motor 7 dört menü derinliğindeyse:
  Dashboard → Hat → Bölüm → Motor → Durdur = 4 tıklama ✗
  → Navigasyon hiyerarşisi yeniden tasarlanmalı
```

### Örnek 3: Yazma Doğrulaması (Confirmation)

```
Kritik eylemler için iki adımlı onay:

[Durdur] butonuna basınca:
  Modal dialog: "Motor 1'i durdurmak istediğinizden emin misiniz?"
  [İptal]  [Evet, Durdur]

Kritik:
  "Tüm hattı acil durdur" → Modal + şifre girişi

NOT: Her eylem için onay dialogu istemek operatörü yavaşlatır.
     Yalnızca geri alınamaz ve kritik eylemler için dialog göster.
     Setpoint güncellemesi → Doğrudan uygula (geri alınabilir).
     Motor durdurma → Onay dialog (etkisi büyük).
     Sistem reset → Onay + yetki kontrolü.
```

## Sık Yapılan Hatalar

### Hata 1: Her Şey Kırmızı veya Yeşil

```
Tüm ekipman durumu kırmızı/yeşil renk kodlaması.
Alarm gelince operator "hangi kırmızı gerçek alarm?" göremez.

ISA-101 çözümü: Normal durum nötr/gri.
Alarm rengi (kırmızı) yalnızca alarm için ayrılmış.
```

### Hata 2: Çok Fazla Bilgi Tek Ekranda

```
Seviye 3 detay ekranında 100+ ölçüm, 30 buton, 15 trend.
Operator cognitive overload.

ISA-101 çözümü: Seviyeye uygun bilgi yoğunluğu.
Level 3 → Seçili kritik parametreler.
Level 4 → Detaylı diagnostik, bakım için ayrılmış.
```

### Hata 3: Yazma Doğrulaması Olmadan Kritik Buton

```
[Tüm Hattı Durdur] butonu doğrudan etkili.
Eldiven giymiş operatör yanlış tıkladı.
Üretim durdu.

Çözüm: Kritik eylemler → Onay dialog zorunlu.
        Fiziksel donanım (hardware interlock) ile yazılımsal kopyalanma.
```

### Hata 4: Bağlantı Kopunca Hiç Değişmeyen Ekran

```
OPC UA bağlantısı kesildi.
Ekranda son değerler görünüyor — sanki hâlâ canlı.
Operatör eski veriyle karar aldı.

Çözüm: 02_realtime_data.md konusu.
Bağlantı kopunca: Değerler gri + "Bağlantı Kesildi" overlay.
```

## Gerçek Proje Notları

**Not 1 — ISA-101 Geçişinde Operatör Direnci**  
Bir fabrikada ISA-101 uyumlu gri/nötr ekranlara geçildi. Operatörler ilk hafta "ekranlar çirkin, eski renkli HMI çok daha iyiydi" dedi. Altı ay sonra aynı operatörler alarm tepki sürelerinin %35 azaldığını kabul etti. "Artık alarm gelince hemen fark ediyorum."

**Not 2 — Üç Tıklama Kuralının İhlali**  
Bir web HMI projesinde navigasyon hiyerarşisi 5 seviyeydi. Operatörler sık kullandıkları ekrana ulaşmak için 6-7 tıklama yapıyordu. "Sık Kullanılanlar" kısayol menüsü eklendi. Problem geçici çözüldü ama asıl sorun hiyerarşi tasarımındaydı. Sonraki revizyon: Yeniden düzenlenen hiyerarşi ile tüm kritik ekranlar ≤3 tıklamaya indirildi.

**Not 3 — Bileşen Kütüphanesinin Getirdiği Hız**  
İlk HMI projemizde her motor için sıfırdan widget tasarladık. 12 motor = 12 kez aynı iş. İkinci projede Motor_Status_Widget oluşturduk. Aynı 12 motor: Parametre geçirerek 12 instance. Geliştirme süresi %70 azaldı; tutarsızlık sıfıra indi.

## İlgili Konular

```
knowledge/hmi/architecture/
├── 02_realtime_data.md          → Veri güncelliği ve bağlantı kopma yönetimi
├── 03_alarm_management.md       → ISA-18.2 alarm tasarımı
└── 04_user_auth.md              → Rol tabanlı erişim kontrolü

knowledge/protocols/
├── opc-ua/01_architecture.md    → HMI'ın tercih ettiği veri kaynağı
└── modbus-tcp/01_protocol_basics.md → Legacy HMI veri kaynağı

Araçlar ve kaynaklar:
  ISA-101 Standard   → https://www.isa.org/isa-101-standards
  ISA-18.2 Standard  → Alarm yönetimi standardı
  Ignition           → Yaygın SCADA/HMI platformu
  Node-RED Dashboard → Hızlı web HMI prototipleme
  InfluxDB + Grafana → Monitoring/analytics dashboard
```
