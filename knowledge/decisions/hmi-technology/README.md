---
KONU        : HMI Teknoloji Seçimleri — Karar Kaydı
KATEGORİ    : decisions
ALT_KATEGORI: hmi-technology
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/hmi/_synthesis.md"
    başlık: "HMI Domaini — Üst Sentez (ANA KAYNAK)"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/architecture/_synthesis.md"
    başlık: "HMI Mimari — Sentez"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/web-based/_synthesis.md"
    başlık: "Web Tabanlı HMI Geliştirme — Sentez"
    güvenilirlik: deneyimsel
  - url: "knowledge/hmi/desktop/01_opcua_clients_python.md"
    başlık: "Masaüstü HMI için OPC UA Python İstemcileri (asyncua)"
    güvenilirlik: topluluk
  - url: "knowledge/hmi/ix-developer/01_architecture.md"
    başlık: "Beijer iX Developer Mimarisi"
    güvenilirlik: resmi
  - url: "https://www.inductiveautomation.com/ignition"
    başlık: "Ignition SCADA Platformu — Inductive Automation"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/en/Products/software/ix-hmi-software"
    başlık: "Beijer iX2 HMI Software Resmi Ürün Sayfası"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "knowledge/hmi/_synthesis.md"
    ilişki: gerektirir
  - konu: "knowledge/hmi/web-based/_synthesis.md"
    ilişki: kullanır
  - konu: "knowledge/hmi/ix-developer/01_architecture.md"
    ilişki: kullanır
  - konu: "knowledge/decisions/architecture"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "knowledge/hmi/architecture/_synthesis.md — HMI mimari katmanlar"
  - "knowledge/hmi/_synthesis.md — Teknoloji seçim tabloları ve 'Ne Zaman' bölümleri"
  - "ISA-101 ve ISA-18.2 standartları hakkında temel bilgi"
ÇELİŞKİLER :
  - kaynak: "hmi/_synthesis.md — CODESYS WebVisu her zaman başlangıç tercihi olarak sunulabilir algısı"
    konu: "WebVisu CODESYS PLC projelerinde hızlı başlatır ancak büyümez; proje ilk günden çok ekran ve alarm yönetimi gerektiriyorsa doğrudan Web HMI veya SCADA tercih edilmeli"
    çözüm: "WebVisu/TargetVisu yalnızca < 10 ekran ve tek site senaryosunda ön koşulsuz tercih; büyüme beklentisi varsa başlangıçta Web HMI stack kurulmalı."
  - kaynak: "hmi/ix-developer/01_architecture.md — iX Developer her panel HMI senaryosu için uygun görünebilir"
    konu: "iX Developer X2/X3 serisi panellere kilitlidir; hedef donanım Siemens TP veya Weintek ise geçersiz seçimdir"
    çözüm: "Panel HMI kararında önce donanım markası sabitleniyor, sonra yazılım seçiliyor. iX Developer yalnızca Beijer X2/X3 için."
  - kaynak: "Masaüstü HMI (PyQt+asyncua) evrensel çözüm gibi görünebilir"
    konu: "PyQt+asyncua güçlüdür ancak çok site veya mobil erişim gerektirdiğinde yetersiz kalır; her kullanıcıya ayrı kurulum zorunluluğu bakım yükü oluşturur"
    çözüm: "Masaüstü HMI; offline, tek istasyon, mühendis analiz araçları veya test jig senaryoları için doğru seçim. Operatör arayüzü için Web HMI veya panel tercih edilmeli."
---

## Özün Ne

Bu belge HMI teknoloji seçiminde **ne seçilmeli, neden, hangi senaryoda** sorularına yanıt veren bir karar kaydıdır. Dört ana kategori arasında — **web tabanlı HMI** (React/Vue + OPC UA + WebSocket), **masaüstü HMI** (PyQt/.NET + asyncua), **panel-HMI** (Beijer iX Developer, Weintek, Siemens TP) ve **SCADA platformu** (Ignition, WinCC) — her birinin güçlü olduğu ve zayıf kaldığı bağlam nettir; sorun bu bağlamı hızla tanımlayarak doğru seçimi yapabilmektir.

Temel ilke şudur: HMI teknoloji seçimi yazılım tercihi değil, **operatörün kim olduğu, nerede durduğu ve neye ihtiyaç duyduğu** sorusuna verilen yanıttır. Makine başında tek bir operatör varsa panel-HMI; binada dolaşan 30 operatör varsa web HMI; tarihsel veriye ve raporlamaya ihtiyaç varsa SCADA; mühendis analiz araçlarına ihtiyaç varsa masaüstü HMI doğru yolda başlar.

---

## Nasıl Çalışır — Dört Yaklaşımın Mimarisi

### Yaklaşım 1: Web Tabanlı HMI (React/Vue + OPC UA/WebSocket)

```
[CODESYS/PLC] ──OPC UA subscription──► [Node.js Backend]
                                              │
                                        WebSocket (wss://)
                                              │
                               ┌──────────────▼──────────────┐
                               │  Tarayıcı (React/Vue)        │
                               │  Zustand/Pinia state          │
                               │  ISA-101 uyumlu bileşenler   │
                               └─────────────────────────────┘
                               Herhangi bir cihaz — sıfır kurulum
```

- **Veri akışı:** OPC UA subscription (push) → Backend event emitter → WebSocket broadcast → Frontend state → Bileşen render
- **Güvenlik:** wss:// (Nginx SSL termination), sessionToken doğrulama, RBAC
- **Kurulum:** Node.js + npm; tarayıcı tarafında sıfır kurulum
- **Detay:** `knowledge/hmi/web-based/_synthesis.md`

### Yaklaşım 2: Masaüstü HMI (PyQt/PySide6 + asyncua)

```
[CODESYS/PLC] ──OPC UA subscription──► [asyncua — Python]
                                              │
                                    queue.Queue (thread-safe)
                                              │
                               ┌──────────────▼──────────────┐
                               │  PyQt/PySide6 GUI            │
                               │  QTimer + queue flush        │
                               │  Widget (QLabel, QSpinBox)   │
                               └─────────────────────────────┘
                               Yalnızca kurulumu olan PC'de
```

- **Veri akışı:** asyncua subscription callback → queue → QTimer (100ms) → GUI güncelleme
- **Event loop köprüsü:** qasync (v0.28.0) veya PySide6.QtAsyncio
- **Avantaj:** Python ekosistemi entegrasyonu (pandas, numpy, InfluxDB client)
- **Detay:** `knowledge/hmi/desktop/01_opcua_clients_python.md`

### Yaklaşım 3: Panel-HMI (Beijer iX Developer)

```
[PLC (herhangi marka)] ──Sürücü/OPC UA──► [iX Runtime — X2/X3 Panel]
                                                    │
                                          Dahili Alarm Motoru
                                          Dahili Trend/Data Logger
                                          Dahili Reçete Motoru
                                          Dahili Audit Trail
                                                    │
                               ┌────────────────────▼────────────────┐
                               │  Dokunmatik ekran (panel yüzeyinde) │
                               │  + Web Server (port 7001, HTTPS)    │
                               │  + OPC UA Server (maks 20 oturum)   │
                               └─────────────────────────────────────┘
```

- **Geliştirme:** iX Developer (Windows 10/11) → Build → Panel'e transfer
- **Scripting:** C# (.NET/WPF tabanlı), NuGet desteği (iX3)
- **Tag modeli:** Controller tag (PLC), Internal tag, System tag, Array tag
- **Detay:** `knowledge/hmi/ix-developer/01_architecture.md`

### Yaklaşım 4: SCADA Platformu (Ignition, WinCC)

```
[Çok sayıda PLC/Cihaz] ──OPC UA / Protokol──► [SCADA Server]
                                                     │
                                           Dahili Historian (veri ambarı)
                                           Dahili Alarm & Event
                                           Dahili Raporlama
                                           Tag database (100K+ tag)
                                                     │
                               ┌─────────────────────▼──────────────┐
                               │  Web Client / Thin Client / Designer│
                               │  100+ ekran, çoklu site            │
                               └────────────────────────────────────┘
```

- **Lisans:** Yüksek; yıllık bakım maliyeti dahil
- **Hız:** Konfigürasyon tabanlı geliştirme, tag bağlama hızlı
- **Avantaj:** Historian, raporlama, ISA-18.2 alarm yönetimi dahili

---

## Karar Kriterleri ve Ağırlıkları

Aşağıdaki kriterler teknoloji seçiminde sıralanmalıdır. Her proje için her kriterin ağırlığı farklıdır:

| Kriter | Açıklama | Kritik Eşik |
|---|---|---|
| **Erişim / Cihaz** | Operatörler nerede, hangi cihazla? | Panel başı = panel-HMI; her yerden = web |
| **Operatör sayısı** | Aynı anda kaç kişi? | 1–2 kişi = panel/masaüstü; 10+ = web/SCADA |
| **Uzaktan erişim** | Ofisten/evden izleme var mı? | Evet → web HMI veya SCADA zorunlu |
| **Ekip yetkinliği** | OT mi, IT mi, ikisi de mi? | OT → iX/SCADA; IT/fullstack → web HMI |
| **Ekran sayısı** | Kaç farklı ekran gerekecek? | < 10 → WebVisu/panel; 10–50 → web; > 50 → SCADA |
| **Historian / Raporlama** | Geçmiş veri ve rapor kritik mi? | Evet → SCADA ya da InfluxDB+Grafana |
| **Geliştirme süresi** | Prototip ne zaman çalışmalı? | Hızlı → iX/SCADA; tam kontrol → web |
| **Lisans bütçesi** | Yazılım lisansı kabul edilebilir mi? | Sıfır bütçe → web HMI veya CODESYS WebVisu |
| **Offline çalışma** | Ağ kesilince HMI çalışmalı mı? | Evet → panel-HMI veya masaüstü HMI |
| **Çoklu site** | Birden fazla fabrika/lokasyon? | Evet → SCADA veya web HMI (wss://) |
| **Bakım kolaylığı** | Güncellemeleri kim yapacak? | Uzaktan güncelleme → web HMI CI/CD; yerel → panel |
| **Regülasyon uyumu** | FDA 21 CFR Part 11, ISO vb.? | FDA → iX Developer FDA modu veya SCADA |

---

## Karar Matrisi

### Ana Teknoloji Karşılaştırması

| Kriter | Web HMI (React/Vue) | Masaüstü (PyQt) | Panel-HMI (iX Dev) | SCADA (Ignition) | WebVisu / TargetVisu |
|---|---|---|---|---|---|
| **Lisans maliyeti** | Sıfır | Sıfır (LGPLv3) | Panel lisanssız, PC lisanslı | Yüksek | CODESYS Runtime lisansına dahil |
| **Uzaktan erişim** | Mükemmel (wss://) | Zayıf (tek PC) | Orta (Web Server dahili) | Mükemmel | Sınırlı |
| **Operatör erişimi** | Her cihaz / tarayıcı | Kurulumlu PC | Sadece panel + Web Server | Her cihaz | Tarayıcı (kısıtlı UI) |
| **Ekran sayısı sınırı** | Sınırsız | Orta (~20–50) | Orta (RAM/flash sınırı) | Sınırsız | Düşük (< 20 önerilir) |
| **Alarm yönetimi** | Manuel (kendin yaz) | Manuel | Dahili | Dahili (ISA-18.2 uyumlu) | Temel (dahili) |
| **Historian** | Manuel (InfluxDB vb.) | Manuel | Dahili (Data Logger) | Dahili (enterprise) | Yok |
| **Offline çalışma** | Kısmi (cache ile) | Tam | Tam | Kısmi (server gerekli) | Tam (PLC üzerinde) |
| **Git / CI-CD uyumu** | Mükemmel | İyi | Zayıf (binary proje) | Zayıf (tescilli format) | Zayıf |
| **Geliştirme hızı** | Orta (full stack) | Orta | Hızlı (konfigürasyon) | Çok hızlı | Çok hızlı |
| **UX esnekliği** | Maksimum | Yüksek | Orta (WPF ile artırılabilir) | Orta (template tabanlı) | Düşük |
| **Ekip yetkinliği** | Frontend + Node.js | Python + Qt | OT / endüstriyel | OT geliştirici | CODESYS mühendis |
| **Çoklu site** | Mükemmel | Uygunsuz | Orta (her panel ayrı) | Mükemmel | Uygunsuz |
| **OPC UA bağlantısı** | node-opcua (Node.js) | asyncua (Python) | Dahili OPC UA client | Dahili (çoklu protokol) | Dahili (CODESYS OPC UA) |
| **Regülasyon uyumu** | Özel geliştirme | Özel geliştirme | FDA modu dahili | Güçlü (enterprise) | Temel |

### Frontend Framework Karşılaştırması (Web HMI için)

| Kriter | React + Zustand | Vue 3 + Pinia |
|---|---|---|
| **Render optimizasyonu** | Manuel (React.memo, useMemo, granüler selector) | Otomatik (Proxy tabanlı reaktivite) |
| **CPU (200 tag, 50 güncelleme/s)** | Optimizasyonsuz %60+; optimize edilmiş düşük | %18 (ekstra optimizasyon gerektirmez) |
| **Öğrenme eğrisi** | Dik | Daha kolay |
| **Büyük proje esnekliği** | Çok yüksek | Yüksek |
| **TypeScript entegrasyonu** | Çok güçlü | Güçlü |
| **Ekip boyutu tercihi** | 10+ geliştirici, kurumsal proje | 1–10 geliştirici, hızlı geliştirme |
| **HMI tercihi** | Büyük/karmaşık, React Native da planlanıyorsa | Orta ölçek, fabrika HMI, hızlı prototip |

### Backend Protokol Karşılaştırması

| Kriter | OPC UA (node-opcua / asyncua) | Modbus TCP (jsmodbus / pymodbus) |
|---|---|---|
| **Veri modeli** | Karmaşık (struct, array, method) | Düz register haritası |
| **Güncelleme mekanizması** | Subscription (push) — PLC haberdar eder | Polling (istemci sorgular) |
| **Trafik verimliliği** | Çok yüksek (yalnızca değişim gönderilir) | Düşük (her cycle tüm register okunur) |
| **PLC desteği** | Modern PLC (CODESYS, Siemens, Beckhoff) | Legacy PLC + her Modbus cihazı |
| **Güvenlik** | Sertifika + SignAndEncrypt (opsiyonel) | Yok (şifresiz) |
| **Veri kalitesi** | GOOD/BAD/UNCERTAIN | Yok |
| **Namespace index** | Her session başında dinamik alınmalı | Yok |
| **Seçim kuralı** | OPC UA sunucusu varsa her zaman tercih | Yalnızca OPC UA yoksa zorunlu |

---

## Pratikte Nasıl Kullanılır — Senaryo Bazlı Karar Süreci

### Adım 1: Ortamı Tanımla (3 Soru)

```
Soru 1: Operatör nerede duruyor?
  a) Makine başında, sabit → Panel-HMI veya masaüstü HMI
  b) Tüm fabrikada dolaşıyor → Web HMI (mobil tarayıcı)
  c) Kontrol odasında, birden fazla istasyon → Web HMI veya SCADA
  d) Uzak lokasyonda (ofis, ev) → Web HMI (wss://) veya SCADA

Soru 2: Kaç ekrana ihtiyaç var?
  a) < 5 ekran → WebVisu, panel-HMI veya masaüstü
  b) 5–30 ekran → Web HMI veya panel-HMI
  c) 30–100 ekran → Web HMI (büyük) veya SCADA
  d) 100+ ekran → SCADA

Soru 3: Historian ve raporlama kritik mi?
  a) Hayır / sadece trend → Web HMI + InfluxDB+Grafana veya panel-HMI Data Logger
  b) Evet, vardiya/günlük rapor → SCADA ya da InfluxDB+Grafana+Loki
  c) Evet, FDA 21 CFR Part 11 uyumu → iX Developer FDA modu veya SCADA
```

### Adım 2: Ekip Yetkinliğini Eşleştir

```
Ekip OT (CODESYS, ladder, PLC programlama biliyor, frontend bilmiyor):
  → iX Developer (konfigürasyon tabanlı) veya SCADA platformu

Ekip IT / fullstack (Node.js, React/Vue, TypeScript biliyor):
  → Web HMI stack (node-opcua + React/Vue + WebSocket)

Ekip Python biliyor, GUI deneyimi var:
  → PyQt + asyncua (masaüstü, mühendis araçları için)

Karma ekip (1 PLC mühendis + 1 yazılım):
  → Web HMI veya iX Developer (orta yol)
```

### Adım 3: Kısıt Kontrolü

```
□ Lisans bütçesi sıfır?  → SCADA ve iX Developer (PC) düş
□ Linux ortamı?          → iX Developer düş (yalnızca Windows)
□ Offline çalışma zorunlu? → Web HMI için cache stratejisi veya panel-HMI
□ Çoklu site, merkezi izleme? → SCADA veya web HMI + VPN
□ Marka bağımsız PLC?   → iX Developer (onlarca sürücü) veya SCADA
```

---

## Örnekler — Somut Senaryo → Karar (Gerekçeli)

### Senaryo 1: Küçük Paketleme Makinesi, Tek Operatör

**Durum:** Tek üretim hattı, 1 operatör makine başında, 3 ekran gerekiyor (dashboard, motor detay, alarm listesi), CODESYS PLC, bütçe kısıtlı.

**Karar: CODESYS WebVisu veya Beijer iX Developer (X2 panel)**

**Gerekçe:**
- 3 ekran = WebVisu veya panel-HMI için ideal ölçek
- Tek operatör, makine başı = web erişimine ihtiyaç yok
- CODESYS PLC = WebVisu doğrudan entegrasyon (ayrı backend yok)
- Bütçe kısıtlı = iX Developer panel için lisans yok; WebVisu CODESYS lisansına dahil
- Operatör üretim hattını terk etmiyor = uzaktan erişim gereksiz

**Uyarı:** Proje ilerlemesi bekleniyor, uzaktan erişim gündeme gelebilir → Web HMI'a geçiş planını baştan belgele.

---

### Senaryo 2: Orta Ölçek Fabrika, 20 Operatör, 5 Hat

**Durum:** 5 üretim hattı, 20 operatör (bazıları gezici), kontrol odası + sahada tablet kullanımı, 25 ekran, OPC UA destekleyen PLC'ler, uzaktan mühendis izlemesi isteniyor.

**Karar: Web HMI — Vue 3 + Pinia + Node.js (node-opcua) + WebSocket**

**Gerekçe:**
- 20 operatör, tablet + PC = web tarayıcısından erişim zorunlu
- 25 ekran = web HMI ölçeğine uygun (SCADA'ya gerek yok)
- OPC UA PLC = node-opcua subscription, polling yok
- Uzaktan erişim = wss:// (Nginx SSL) + VPN
- Sıfır lisans = bütçe avantajı
- Gezici operatörler = mobil tarayıcı (React Native gerekmez)
- Vue 3 seçimi: Ekip 2–5 kişi, orta ölçek → Pinia reaktivite avantajı

**Dikkat:** Alarm yönetimi ve historian sıfırdan yazılacak. ISA-18.2 alarm state machine ve InfluxDB+Grafana bütçeye dahil edilmeli.

---

### Senaryo 3: Büyük Tesis, 100+ Ekran, Historian Kritik

**Durum:** 3 fabrika binası, 150 ekran, 50+ PLC (farklı markalar: Siemens, AB, CODESYS), vardiya raporları ERP'ye gidiyor, 5 mühendis sürekli izliyor, SLA gerektiren proje.

**Karar: SCADA Platformu — Ignition (Inductive Automation)**

**Gerekçe:**
- 150 ekran = web HMI ile yapılabilir ama bakım yükü ağır; konfigürasyon tabanlı SCADA daha hızlı
- Farklı PLC markaları = SCADA dahili protokol sürücüleri (OPC UA, Modbus, Allen-Bradley EtherNet/IP vb.)
- Historian kritik = SCADA dahili historian + ERP entegrasyonu
- SLA + vendor destek = Ignition resmi destek sözleşmesi
- Vardiya raporu = dahili raporlama modülü
- Lisans maliyeti kabul edilebilir = büyük ölçekte ROI pozitif

**Alternatif:** Siemens WinCC (Siemens ağırlıklı tesis için); AVEVA System Platform.

---

### Senaryo 4: Mühendis Analiz İstasyonu, Tek PC

**Durum:** Üretim mühendisi offline analiz yapıyor, CODESYS OPC UA sunucusundan veri çekip pandas ile analiz, InfluxDB'ye yazıyor, zaman zaman setpoint gönderme gerekiyor. Tarayıcı HMI'a gerek yok.

**Karar: Masaüstü HMI — Python + asyncua + (isteğe bağlı PyQt/PySide6)**

**Gerekçe:**
- Tek PC, tek mühendis = web stack kurmak overkill
- Python ekosistemi (pandas, numpy, InfluxDB client) = asyncua doğal entegrasyon
- OPC UA subscription + veri analizi = asyncua async iterator pattern
- Setpoint yazma = asyncua write_value (sessionToken gerekmez; lokal bağlantı)
- Deployment = pip install; PyQt GUI isteğe bağlı

**Önemli not:** Bu istasyonu 10 mühendisle paylaşmak zorunda kalınırsa web HMI'a geçilmeli (asyncua singleton bir bağlantı, 10 bağlantı CODESYS MaxSessions'ı (10) tüketir).

---

### Senaryo 5: Makine Üreticisi (OEM), Ürünle Giden Panel

**Durum:** Makine üreticisi, müşteriye teslim edilen her makineye bir HMI dahil ediyor. Siemens, Allen-Bradley ve CODESYS PLC'lerle çalışıyor. Müşteri farklı ülkelerde, uzaktan destek kritik.

**Karar: Beijer iX Developer + X2 serisi panel (müşteride) + dahili Web Server (uzak erişim için)**

**Gerekçe:**
- OEM standardizasyon = tek geliştirme ortamı + onlarca PLC sürücüsü
- Panel makineyle gider = lisans maliyeti panel fiyatına dahil
- Alarm, trend, reçete, audit trail = dahili (ek yazılım yok)
- Uzak erişim = iX Developer dahili Web Server (port 7001, HTTPS)
- C# scripting = makineye özgü hesaplama mantığı
- FDA 21 CFR Part 11 uyumu = müşteri ilaç/gıda sektöründeyse FDA modu aktif

**Uyarı:** Hedef panel Siemens TP veya Weintek ise iX Developer geçersiz; o markanın yazılımına geçilmeli.

---

### Senaryo 6: Start-up, Hızlı MVP, Küçük Ekip

**Durum:** 2 kişilik ekip (1 PLC mühendis + 1 fullstack geliştirici), 10 ekranl web HMI prototipi, CODESYS PLC, 2 ay içinde demo hazır olmalı, bütçe sıfır.

**Karar: Web HMI — Vue 3 + Pinia + Node.js (node-opcua) + ws**

**Gerekçe:**
- Vue 3: 1 fullstack geliştirici + hızlı prototip + az boilerplate = Vue avantajı
- node-opcua: CODESYS OPC UA subscription, Modbus polling gerekmez
- Sıfır lisans = bütçeye uygun
- Git + CI/CD = her güncelleme anında deploy
- 10 ekran = web HMI ölçeğine uygun

**MVP sonrası dikkat:** Alarm yönetimi (ISA-18.2), wss:// (Nginx), RBAC+audit log ilk sürümde minimum uygulanmalı. "Sonra ekleriz" diyerek bırakılırsa audit log eksikliği geçmişi siler.

---

## Sık Yapılan Hatalar (Yaygın Yanlış Kararlar)

### Yanlış Karar 1: "En tanıdık teknoloji en doğru seçimdir"

Ekip React biliyor diye tüm projeler için React seçmek — 5 ekran, 2 tag, tek operatör için React + Zustand + Node.js kurmak overengineering'dir. Bu ölçekte CODESYS WebVisu 1 günde çalışır, web stack 2 haftada.

**Düzeltme:** Ölçeği önce belirle, sonra teknoloji seç.

---

### Yanlış Karar 2: "SCADA her şeyi çözer"

Küçük projede SCADA satın alıp lisans maliyetini yazılım geliştirme süresinden tasarruf gibi göstermek. 3 ekran, 20 tag için yıllık Ignition lisansı gereksiz harcamadır.

**Düzeltme:** SCADA için eşik: 30+ ekran VEYA historian kritik VEYA 10+ PLC VEYA SLA zorunlu. Bunlardan hiçbiri yoksa web HMI veya panel-HMI yeterli.

---

### Yanlış Karar 3: "WebVisu yeter, büyürsek geçeriz"

WebVisu ile başlayıp 2 yıl içinde 40 ekrana çıkmak ve geçişi ertelemeye devam etmek — performans sorunu üretimde ortaya çıkana kadar fark edilmez.

**Düzeltme:** Başlangıçta > 15 ekran öngörülüyorsa WebVisu yerine doğrudan web HMI stack kur. Mimari borç pahalıdır.

---

### Yanlış Karar 4: "Alarm yönetimini sonra ekleriz"

Web HMI projelerinde alarm yönetimi ve audit log "MVP sonrasına" bırakılır. Üretime giren sistemde hiçbir yazma kim tarafından yapıldı bilinmez; kritik alarm sessizce kaybolabilir.

**Düzeltme:** ISA-18.2 alarm state machine ve audit log projenin 0. günü mimariye dahil edilmeli. Sonradan eklemek hem daha zordur hem geçmiş verileri kaybettirir (Gerçek Proje Notu — architecture/_synthesis.md, Sentez Notu 1).

---

### Yanlış Karar 5: "ws:// ile başlarız, production'da geçeriz"

Geliştirmede ws:// (açık metin) kurar, üretime alırken "IT onay verince geçeceğiz" denir. IT güvenlik denetiminde "tüm PLC komutları açık metin" bulgusu ile acil düzeltme gerekir.

**Düzeltme:** Nginx SSL termination + wss:// planı baştan yapılır. Konfigürasyon ek iş değil, 2 saatlik ön yatırımdır (Gerçek Proje Notu — web-based/_synthesis.md, Not 8).

---

### Yanlış Karar 6: "Panel HMI'ı her makineye koy"

Çok kullanıcılı, gezici operatörlü bir tesiste her makineye ayrı panel koymak — hem maliyet hem bakım yükü. 20 panel × firmware güncellemesi × 20 makineye gidip gelmek.

**Düzeltme:** Gezici operatörler + çok sayıda makine = merkezi web HMI + operatör tabletleri daha ekonomik ve bakım kolaylığı sağlar.

---

### Yanlış Karar 7: "Masaüstü HMI 10 mühendisle paylaşılabilir"

PyQt + asyncua masaüstü HMI CODESYS'e tek bir OPC UA bağlantısı açar. 10 mühendis 10 ayrı instance çalıştırınca CODESYS MaxSessions (varsayılan: 10) dolar → `BadTooManySessions` → sistem çöker.

**Düzeltme:** Masaüstü HMI tek kullanıcı veya küçük ekip içindir. Çok kullanıcılı senaryo → web HMI (tek backend bağlantısı, 50 WebSocket istemcisi broadcast).

---

### Yanlış Karar 8: "Namespace index sabit 4'tür"

CODESYS runtime versiyonu değiştiğinde `ns=4` hardcode olan tüm node ID'leri `ns=3` veya `ns=5` gelince sessizce başarısız olur. Veri kesilir; operatör fark etmeyebilir.

**Düzeltme:** Her session başlangıcında `session.getNamespaceIndex(uri)` (node-opcua) veya `client.get_namespace_index(uri)` (asyncua) ile dinamik al. Bu kural hem web HMI hem masaüstü HMI için geçerlidir.

---

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Web HMI (React/Vue + Node.js + WebSocket)

```
Tercih et:
  ✓ 5–100 ekran arası proje
  ✓ Çok operatör, gezici, farklı cihazlar
  ✓ Uzaktan erişim zorunlu
  ✓ Git/CI-CD ile sürekli güncelleme
  ✓ Sıfır lisans bütçesi
  ✓ Ekip fullstack geliştirici
  ✓ Custom UX gereksinimleri (standart widget yetmez)
  ✓ OPC UA destekleyen modern PLC

Tercih etme:
  ✗ Alarm historian kritik ve sıfırdan yazmak istemiyorsan → SCADA
  ✗ Ekip yalnızca OT biliyorsa → iX Developer veya SCADA daha hızlı
  ✗ Offline çalışma kesinlikle zorunluysa → panel-HMI (web cache yeterli olmayabilir)
  ✗ < 5 ekran, tek operatör → overengineering
```

### Masaüstü HMI (PyQt + asyncua)

```
Tercih et:
  ✓ Tek mühendis / küçük ekip
  ✓ Python ekosistemi entegrasyonu (pandas, numpy)
  ✓ Veri analiz scripti + InfluxDB/CSV log
  ✓ Linux/Raspberry Pi ortamı
  ✓ Hızlı prototip veya test jig
  ✓ Offline, yerel bağlantı

Tercih etme:
  ✗ Çok kullanıcılı senaryo (CODESYS MaxSessions sorunu)
  ✗ Uzaktan erişim gereksinimi
  ✗ Kurulum yapılamayan ortamlar
  ✗ OPC Foundation resmi sertifikasyonu gerekiyorsa → .NET SDK
```

### Panel-HMI (Beijer iX Developer)

```
Tercih et:
  ✓ Hedef Beijer X2 veya X3 serisi panel
  ✓ Makine başında sabit operatör
  ✓ Marka bağımsız PLC entegrasyonu (onlarca sürücü)
  ✓ Alarm, trend, reçete, audit trail dahili isteniyor
  ✓ OEM (ürünle giden panel)
  ✓ FDA 21 CFR Part 11 uyumu gerekliyse (FDA modu)
  ✓ C# scripting ile özel hesaplama

Tercih etme:
  ✗ Hedef donanım Beijer dışı (Siemens TP, Weintek vb.)
  ✗ Büyük ölçekli SCADA (100+ ekran, historian kritik)
  ✗ Web tabanlı geliştirme tercih ediliyorsa
  ✗ Linux/macOS geliştirme ortamı (yalnızca Windows 10/11)
  ✗ Açık kaynak / sıfır lisans zorunluysa (PC runtime lisanslı)
```

### SCADA Platformu (Ignition, WinCC)

```
Tercih et:
  ✓ 50+ ekran, büyük tesis
  ✓ Historian kritik (geçmiş veri, vardiya raporu)
  ✓ Çok sayıda farklı marka PLC
  ✓ Vendor destek sözleşmesi (SLA) gerekli
  ✓ Hızlı geliştirme, konfigürasyon tabanlı
  ✓ ISA-18.2 alarm yönetimi dahili kullanmak

Tercih etme:
  ✗ < 30 ekran → maliyet fazla
  ✗ Sıfır lisans bütçesi → web HMI
  ✗ Özel UX / tam kontrol isteniyor → web HMI
  ✗ Küçük proje, hızlı prototip → overengineering
```

---

## Gerçek Proje Notları

**Karar Notu 1 — "Önce çalışsın sonra güvenlik" tuzağı**

Web HMI projelerinde en sık karşılaşılan hata: audit log ve yetkilendirme sonraya bırakılır. Üretime giren sistemde kim ne yazdı bilinmez. Sonradan eklenen audit log yalnızca eklendikten sonrasını kaydeder; geçmiş tüm yazma işlemleri anonim kalır. Bu durum, regülasyon denetiminde "geçmiş kayıt yok" bulgusuna yol açar. **Yetkilendirme ve audit log projenin 0. günü mimariye dahil edilmeli.** (Kaynak: architecture/_synthesis.md — Sentez Notu 1)

**Karar Notu 2 — Bağlantı kopma senaryosu geliştirmede test edilmeli**

Teknoloji ne olursa olsun (web, panel, masaüstü) bağlantı kopma davranışı geliştirme aşamasında simüle edilmelidir. Web HMI'da 20 dakika önce bağlantı kesilmiş, ekran 68°C gösteriyordu, gerçekte 92°C'ye ulaşmıştı, motor hasar gördü vakası yaşandı. Panel-HMI'da connection timeout parametresi yanlış ayarlanmışsa benzer risk var. **Bağlantı kopma testi deployment checklist'in zorunlu adımıdır.** (Kaynak: architecture/_synthesis.md — Sentez Notu 3)

**Karar Notu 3 — OPC UA vs Modbus kararı ertelenmemeli**

Proje başında "Modbus ile başlarız, OPC UA'ya geçeriz" kararı verilir, geçiş ertelenir. Modbus polling + web HMI kombinasyonunda toplu okuma ve değişim filtresi zorunluyken eklenmemişse 100 tag × 500ms × 10 istemci = 200 istek/saniye PLC CPU'sunu zorlar. **Protokol kararı baştan verilmeli; OPC UA sunucusu mevcutsa Modbus seçmek için geçerli neden olmalıdır.** (Kaynak: hmi/_synthesis.md — "Ne Zaman OPC UA, Ne Zaman Modbus?")

**Karar Notu 4 — iX Developer sürüm uyumluluğu ilk kontrol**

iX Developer projesinde hedef panel modeli proje oluşturulurken seçilir ve geri dönüşü zordur. iX2 ile X2 serisi, iX3 ile X3 serisi uyumludur; karıştırılamaz. OEM projesinde 50 müşteriye teslim edilen paneller eski X2 serisinden yenisine geçiş planlanmadan yapılırsa iX3 ile geliştirilen proje X2 panellere aktarılamaz. **Hedef panel serisi kesinleşmeden proje başlatılmamalıdır.** (Kaynak: ix-developer/01_architecture.md — Sık Yapılan Hatalar 6)

**Karar Notu 5 — Çoklu site kararında VPN vs SCADA**

Birden fazla fabrika lokasyonu olan projede "her fabrikaya ayrı web HMI mı, yoksa merkezi SCADA mı?" sorusu erken sorulmalıdır. Web HMI + VPN teknik olarak mümkündür; ancak her sitenin kendi Node.js backend'i, kendi deployment süreçleri ve kendi güvenlik yapılandırması gerektirir. 5+ site → SCADA'nın merkezi yönetim ve historian avantajı belirginleşir.

**Karar Notu 6 — Vue CPU avantajı gerçek, ama React ile de çözülebilir**

Aynı uygulamayı Vue 3 + Pinia ile %18 CPU, React.memo/useMemo olmadan %60+ CPU olarak ölçüldü. Bu Vue'yu her zaman daha iyi yapmaz; granüler selector + React.memo uygulanan React projesi de düşük CPU'ya ulaşır. **Fark geliştirme çabasıdır:** Vue'da performans "ücretsiz" gelir; React'ta ek iş ister. Ekip yetkinliği bu kararı belirler. (Kaynak: web-based/_synthesis.md — Not 4)

---

## İlgili Konular

```
Karar tabanı:
knowledge/decisions/
├── hmi-technology/README.md   ← Şu an buradasınız
├── architecture/              → Mimari düzey kararlar (PLC, ağ, SCADA vs Edge)
└── protocol-selection/        → OPC UA / Modbus / MQTT / EtherCAT seçim kararları

HMI domain bilgi tabanı:
knowledge/hmi/
├── _synthesis.md              → Üst sentez (HMI teknoloji seçim tabloları — ANA KAYNAK)
├── architecture/_synthesis.md → ISA-101, ISA-18.2, RBAC, alarm state machine
├── web-based/_synthesis.md    → node-opcua, jsmodbus, React, Vue, WebSocket
├── desktop/01_opcua_clients_python.md → asyncua, qasync, PyQt entegrasyonu
└── ix-developer/01_architecture.md   → Beijer iX Developer mimari ve tag modeli

Protokol katmanı:
knowledge/protocols/
├── opc-ua/01_architecture.md  → OPC UA sunucu mimarisi
├── opc-ua/04_subscriptions.md → MonitoredItem parametreleri
└── modbus-tcp/01_protocol_basics.md → Modbus TCP polling temelleri

PLC tarafı:
knowledge/codesys/
└── fundamentals/_synthesis.md → CODESYS Runtime + Proje + Diller sentezi

Standartlar:
  ISA-101.01-2015    → HMI ekran tasarım standardı
  ISA-18.2-2016      → Alarm yönetimi yaşam döngüsü
  FDA 21 CFR Part 11 → Elektronik kayıt ve imza (ilaç/gıda sektörü)
  IEC 62443          → OT siber güvenlik
```
