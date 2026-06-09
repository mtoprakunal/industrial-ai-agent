---
KONU        : HMI Mimari Kalıpları
KATEGORİ    : hmi
ALT_KATEGORI: architecture
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
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

**Not 4 — Panel PC'de Tarayıcı Tabanlı HMI'ın Bellek Sızıntısı**  
Web HMI 24/7 çalışan bir endüstriyel Panel PC'de (4 GB RAM, Chromium kiosk modu) deploy edildi. İlk gün sorun yok. Üçüncü günün sonunda tarayıcı 2.8 GB RAM kullanıyordu, ekran kasıyordu. Sebep: Her saniye eklenen DOM trend noktaları hiç temizlenmiyordu (`<svg>` içinde 250.000 `<path>` segmenti birikmişti). React DevTools profiler ile bulundu. Çözüm: Trend için canvas-tabanlı render (uPlot) + sabit pencere (ör. son 3600 nokta, FIFO). Bellek 2.8 GB → 320 MB sabitlendi. Ders: Endüstriyel HMI ofis uygulaması değildir; "günde bir kez yeniden başlat" lüksü yoktur, leak'ler haftalar boyunca birikir.

**Not 5 — WinCC ScreenItem Limiti ve "Sayfa Açılmıyor" Sorunu**  
Siemens WinCC (TIA Portal) ile yapılan bir detay sayfasında ~450 ScreenItem (gösterge, metin, I/O field) vardı. Sayfa runtime'da açılırken 6-8 saniye donuyordu. Operatör "HMI bozuldu" diye düşünüp paneli resetliyordu. Sebep: WinCC tek bir ekranda çok sayıda dinamik nesneyi tek tek tag bağlama ile günceller; her tag ayrı bir okuma döngüsüne giriyordu. Çözüm: Faceplate (tip örneği) kullanımı + tag'leri tek bir struct UDT'de gruplayıp area pointer ile okuma. Açılış süresi 1 saniyenin altına indi. Ders: Platform yerleşik HMI'larda ekran başına nesne/tag sayısı somut bir performans limitidir, web HMI'da olduğu gibi "render edilince bedava" değildir.

**Not 6 — Dokunmatik Hedef Boyutu ve Eldivenli Yanlış Dokunma**  
Bir saha projesinde web HMI butonları 32×32 px tasarlanmıştı (masaüstü mockup'ta güzel görünüyordu). Fabrika zemininde eldivenli operatörler sürekli komşu butona basıyordu; bir keresinde "Durdur" yerine yandaki "Reset" tetiklendi. ISA-101 ve dokunmatik kılavuzlar minimum 15-20 mm (yaklaşık 60-75 px @ tipik panel DPI) dokunma hedefi ve 8 mm aralık önerir. Tüm kritik butonlar büyütüldü, kritik/yıkıcı butonlar (acil durdur) fiziksel olarak ayrı bölgeye taşındı. Eldivenli yanlış dokunma vakaları sıfıra indi.

## Edge Case'ler ve Sistem Limitleri

Mimari kararların pratikte çarptığı sınırlar genellikle "kağıt üzerinde çalışan" tasarımı bozar. Aşağıdaki tablo sahada en sık çarpılan limitleri ve davranışları özetler.

| Edge Case | Tetikleyen Koşul | Tipik Belirti | Doğru Davranış |
|---|---|---|---|
| Ekran nesne patlaması | Detay ekranında 300+ dinamik nesne | Sayfa açılışı saniyelerce donar (WinCC/FactoryTalk) | Faceplate + UDT gruplama; bilgi yoğunluğunu ISA-101 seviyesine indir |
| Çözünürlük varyasyonu | Aynı HMI 1280×800 panel + 1920×1080 mühendis istasyonu | Taşma, kırpılma, sabit-piksel layout bozulması | Grid/relatif layout; "design resolution" + ölçekleme; kritik öğeler asla taşmaz |
| Çok dilli metin genişlemesi | Almanca/Türkçe çeviri İngilizceden %30-40 uzun | Buton metni taşar, durum etiketi kesilir | Esnek genişlik, metin kısaltma yerine ikon+tooltip, uzun metinde wrap |
| Renk körü + monokrom panel | %8-12 erkek renk körü; bazı eski mono paneller | Kritik/normal ayırt edilemez | Renk + şekil + konum + metin; asla yalnızca renk |
| 3 tıklama kuralı ihlali | 5+ seviyeli navigasyon hiyerarşisi | Operatör kritik ekrana ulaşamaz, kestirme arar | Hiyerarşi yeniden tasarımı + "favoriler"; geçici çözümle yetinme |
| Yıkıcı eylem yanlış tetikleme | Küçük/bitişik dokunma hedefi, eldiven | Yanlış "Durdur/Reset/E-Stop" | Min 15-20 mm hedef, yıkıcı butonu ayır, onay dialogu |
| Modal dialog kilitlenmesi | Onay modalı açıkken yeni kritik alarm gelir | Alarm modal arkasında görünmez | Alarm banner her zaman en üstte (modal üstü z-index) |
| Faceplate instance senkronu | Aynı UDT'den 50 instance, biri stale | Bir motor güncel, biri donmuş | Instance bazlı kalite/timestamp; toplu "bağlantı sağlığı" göstergesi |

**Sert sistemsel limitler (deneyimsel eşikler):**
```
Tek ekranda dinamik nesne   : Platform HMI'da pratik tavan ~200-300 (üstü = açılış gecikmesi)
Bilgi yoğunluğu (Level 3)   : İnsan kısa-süreli belleği ~7±2 öğe — bir bakışta izlenecek
                              kritik değer sayısı 10'u geçmemeli
Navigasyon derinliği        : ≤3 tıklama (kritik ekran), ≤4 (diagnostik)
Animasyon kare hızı         : Endüstriyel panelde GPU sınırlı; >30 fps animasyon CPU yer
Trend görünür nokta         : Canvas ile ~10.000, DOM/SVG ile ~1.000 (üstü leak/lag)
```

## Optimizasyon

HMI mimarisinde optimizasyon önce **doğru mimari karar**, sonra **render verimliliği**, en son **mikro-iyileştirme** sırasıyla yapılır. Yanlış sırada başlamak (önce mikro-optimize etmek) en yaygın zaman kaybıdır.

**Optimizasyon önceliği (etki sırasına göre):**
```
1. MİMARİ — Bilgi mimarisi ve ekran hiyerarşisi (en yüksek etki)
   → Doğru ekran sayısı, doğru bilgi dağılımı. Bir Level-1 overview
     ekranı, operatörün 10 detay ekranını gezmesini önler.
   → ISA-101 seviye ayrımı: Her veri en uygun seviyede gösterilir.

2. RENDER — Çizim/güncelleme maliyetini düşür
   → Yalnızca DEĞİŞEN nesneyi güncelle (dirty-checking / reactive binding).
   → Görünmeyen ekran/sekme güncellemesini durdur (visibility-aware).
   → Trend/grafik canvas-tabanlı; DOM/SVG'de binlerce nokta tutma.

3. BİLEŞEN — Yeniden kullanılabilir faceplate/widget
   → Tek widget tanımı, N instance. Hem hız hem tutarlılık.
   → Web'de React.memo / Vue v-once ile gereksiz re-render önleme.

4. MİKRO — Font/asset/CSS optimizasyonu (en düşük etki, en son)
   → Mono font sayı hizası, asset preload, GPU-accelerated transform.
```

**Somut teknikler:**
```
Reaktif binding > polling-render:
  Her tag değişiminde tüm ekranı yeniden çizmek yerine, yalnızca o tag'e
  bağlı nesneyi güncelle. WinCC'de "trigger on change", web'de fine-grained
  reactivity (signals / observable). 1000 tag'lik ekranda CPU %70 → %8.

Görünürlük-farkında güncelleme:
  Arka plandaki sekme/ekrana ait widget'ların subscription'ı askıya alınır
  (Page Visibility API / IntersectionObserver). Çok sekmeli HMI'da kritik.

Layout sabitleme:
  "Design resolution" belirle (ör. 1920×1080), her şeyi relatif/grid yerleştir,
  CSS transform: scale() veya viewport birimi ile ölçekle. Mutlak piksel ASLA.

Sayfa ön-yükleme (preload):
  Sık geçilen Level-2/3 ekranları arka planda hazırla; geçiş 0 gecikme hissi.
  Platform HMI'da "background screen caching" seçeneği.
```

## Derin Teknik Detay

**Sunum (presentation) ile kontrol durumunun (control state) ayrılması — neden?**
HMI mimarisinin en temel iç prensibi, *ekranda gördüğün şey kontrol gerçeğinin bir kopyasıdır, kendisi değildir*. PLC kontrol mantığını yürütür; HMI yalnızca o durumun bir görselleştirmesidir. Bu ayrım MVVM (Model-View-ViewModel) deseninde formelleşir:
```
Model      : PLC/OPC UA tag değerleri (tek doğruluk kaynağı — source of truth)
ViewModel  : Tag'leri ekran semantiğine çeviren ara katman
             (ör. rTemp=88 + limit=85 → durum="ALARM", renk="kırmızı")
View       : Salt görsel — kendi başına karar vermez, ViewModel'i yansıtır
```
Neden bu ayrım kritik? Çünkü View'da iş mantığı (örn. "sıcaklık 85'i geçerse motoru durdur") tutulursa, iki tehlikeli sonuç doğar: (1) HMI çökerse veya bağlantı koparsa o mantık çalışmaz — güvenlik mantığı asla HMI'da olmamalı, PLC'de olmalı; (2) iki farklı HMI istemcisi aynı tag'i farklı yorumlarsa tutarsızlık doğar. ViewModel katmanı ayrıca test edilebilirlik sağlar: Görsel olmadan "bu tag kombinasyonu hangi durumu üretir" birim testi yazılabilir.

**Neden ISA-101 gri/nötr palet — algısal temel:**
Bu estetik bir tercih değil, insan görsel sisteminin çalışma biçiminden türer. İnsan periferik (çevresel) görüşü harekete ve yüksek kontrasta duyarlıdır, renge değil. Normal durum düşük-kontrastlı/nötr olduğunda, ani bir yüksek-kontrastlı kırmızı (alarm) periferik görüşte anında "pop-out" yapar — operatör doğrudan bakmıyor olsa bile fark eder. Ekran zaten renk doluysa, yeni renk ortalama kontrastı artırmaz, pop-out etkisi kaybolur (görsel arama "konjonktif arama"ya döner: yavaş ve sıralı). Yani "sıkıcı gri ekran" aslında *bilinçli olarak sinyal-gürültü oranını maksimize eden* bir tasarım kararıdır.

**SCADA platform HMI vs Web HMI — iç mimari farkı:**
```
SCADA platform (WinCC, FactoryTalk, Ignition Vision):
  Tag motoru ekran nesnelerine sıkı bağlıdır (tightly coupled).
  Her nesne bir tag'e doğrudan abone; runtime motoru güncelleme döngüsünü yönetir.
  → Hızlı geliştirme, ama ekran-tag bağı esnek değil; nesne sayısı = yük.

Web HMI (React/Vue + WebSocket):
  Veri katmanı (store) ile görünüm katmanı tamamen ayrı.
  Tek WebSocket → merkezi store → bileşenler store'dan türetir (selector).
  → Esnek, test edilebilir, ama alarm/historian/tag-binding kendin yazarsın.

Ignition Perspective (hibrit):
  Web teknolojisi (HTML render) + SCADA tag motoru. İki dünyanın ortası.
```
Temel mühendislik tercihi şudur: SCADA platformu **bağ-zamanı (binding-time) verimliliği** sunar (hızlı kur, çalış), web HMI **çalışma-zamanı (runtime) esnekliği** sunar (her render kararını sen verirsin). Büyük, standart proseslerde birincisi; özel/çok istemcili/mobil senaryolarda ikincisi kazanır.

**Yazma yolu (write path) neden okuma yolundan farklı tasarlanır:**
Okuma yüksek-frekanslı, idempotent ve geri-alınabilir bir akıştır; bir okuma kaçsa bir sonraki günceller. Yazma ise düşük-frekanslı, *yan etkili* ve çoğu zaman geri-alınamazdır. Bu yüzden yazma yolu tasarımı her zaman: (1) yetki kontrolü (bkz. 04), (2) bağlantı sağlığı kontrolü — kopuksa yazma kilitli (bkz. 02), (3) kritikse onay/çift-onay, (4) audit log, (5) PLC tarafında değer aralığı doğrulaması (HMI doğrulaması atlanabilir, PLC clamp her zaman çalışır) içerir. HMI'da "tek bir buton" gibi görünen şey, arkada bu beş aşamalı bir boru hattıdır.

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
