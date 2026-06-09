---
KONU        : Endüstriyel Ağ — Sentez
KATEGORİ    : networking
ALT_KATEGORI: networking
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "knowledge/networking/01_topologies.md"
    başlık: "Endüstriyel Ağ Topolojileri"
    güvenilirlik: deneyimsel
  - url: "knowledge/networking/02_security.md"
    başlık: "Endüstriyel Ağ Güvenliği"
    güvenilirlik: deneyimsel
  - url: "knowledge/networking/03_performance.md"
    başlık: "Endüstriyel Ağ Gecikme ve Güvenilirlik"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/networking/01_topologies.md"
    ilişki: detaylandırır
  - konu: "knowledge/networking/02_security.md"
    ilişki: detaylandırır
  - konu: "knowledge/networking/03_performance.md"
    ilişki: detaylandırır
  - konu: "knowledge/standards/02_iec62443"
    ilişki: gerektirir
  - konu: "knowledge/protocols/profinet/"
    ilişki: kullanır
  - konu: "knowledge/protocols/ethercat/"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Bu sentez, üç temel belgeyi okuduktan sonra okunmak üzere tasarlanmıştır."
  - "OSI modeli, IP adresleme, VLAN temel kavramları"
  - "PLC, HMI, SCADA kavramları ve Purdue/ISA-95 katman numaralandırması"
ÇELİŞKİLER :
  - kaynak: "—"
    konu: "—"
    çözüm: "Bu sentez belgesi yeni çelişki içermez; kaynak belgelere atıflar yapar. Kaynak belgelerdeki çelişkiler (MRP vs RSTP, Purdue'nun geçerliliği, HSR sıfır kayıp iddiası) o belgelerde çözümlenmiştir."
---

## Özün Ne

Bu sentez, "Endüstriyel ağ tasarlamak isteyen biri topoloji, güvenlik ve performans belgelerini okuyunca ne anlamalı?" sorusuna yanıt verir. Üç belge birbirinin parçasıdır ve birlikte okunduğunda eksiksiz bir endüstriyel ağ tasarım çerçevesi ortaya çıkar.

**01_topologies.md** ağın fiziksel ve mantıksal iskeletini tanımlar: hangi topoloji, hangi yedeklilik protokolü, cihazlar Purdue'nun hangi katmanında.

**02_security.md** o iskeletin güvenlik gözlüğüyle okunmasını sağlar: IEC 62443 bölge/kanal mimarisi, iDMZ, güvenlik duvarı kuralları ve derinlemesine savunma.

**03_performance.md** ise iskelet üzerinde doğru zamanlamayı kurar: PROFINET RT/IRT, EtherCAT, TSN, QoS ve yedeklilik protokollerinin nicel parametreleri.

Tek cümlelik öz: **Topoloji ağın şeklini, güvenlik ağın sınırlarını, performans ağın zamanlamasını belirler — ve bu üçü birbirini kısıtlar.**

### Birleştirici İlke: Ağ, Determinizm ve Güvenilirliğin Omurgasıdır

Üç belge yüzeyde ayrı konulardır (topoloji, güvenlik, performans); ancak hepsini bir arada tutan **tek bir mühendislik ilkesi** vardır: *endüstriyel ağ, fiziksel sürecin determinizm ve güvenilirlik omurgasıdır.* IT ağında bir paketin gecikmesi rahatsızlık, OT ağında bir paketin geç/kayıp gelmesi ise fiziksel olaydır — durmuş bir hat, bozulmuş bir parça, tetiklenen bir güvenlik fonksiyonu. Bu yüzden her üç belge de aynı çekirdek soruyu üç farklı pencereden sorar: **"Veri, garanti edilen zamanda, garanti edilen şekilde, doğru tarafa ulaşıyor mu?"**

Bu birleştirici ilkenin üç tezahürü, üç belgeye karşılık gelir:

| Belge | Birleştirici tema | Çekirdek mekanizma | Başarısızlığın fiziksel sonucu |
|---|---|---|---|
| **01_topologies** | Güvenilir teslimat — *yol her zaman var* | Segmentasyon + halka yedekliliği (MRP/HSR/PRP) | Kopma → izole düğüm, durmuş hücre |
| **02_security** | Doğru tarafa teslimat — *yalnızca yetkili akış* | Defense-in-depth + zone/conduit izolasyonu | Yanal hareket → fidye yazılımı tüm tesisi durdurur |
| **03_performance** | Zamanında teslimat — *garanti edilen gecikme* | Deterministik iletim (IRT/EtherCAT/TSN) + QoS | Jitter → senkronizasyon kaybı, mekanik hasar |

Üçü de aynı tasarım felsefesini paylaşır: **best-effort'u (en iyi çaba) kabul etme; çekişmeyi/belirsizliği tasarımla yok et.** Topoloji belirsizliği yedeklilikle, güvenlik belirsizliği katmanlı izolasyonla, zamanlama belirsizliği zaman-bölmeli iletimle ortadan kaldırır. Uzman seviyesinde bu üç belge ayrı ayrı değil, **tek bir "garantili omurga" tasarımının üç boyutu** olarak okunmalıdır — ve bu boyutlar birbirini kısıtlar (güvenlik DPI'ı gecikme yer, halka boyutu hem kurtarma süresini hem jitter'i etkiler, VLAN hem segmentasyon hem broadcast domain sınırıdır).

## Nasıl Çalışır

### Üç Belgenin Birbirine Bağlantısı: Topoloji → Güvenlik → Performans Üçgeni

```
┌─────────────────────────────────────────────────────────────────────────┐
│           ENDÜSTRİYEL AĞ TASARIM ZİHİN HARİTASI                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  01_topologies.md                                                         │
│  ┌────────────────────────────────────────────────────────────────┐      │
│  │                   TOPOLOJİ (Fiziksel + Mantıksal İskelet)      │      │
│  │                                                                │      │
│  │  Fiziksel:  Doğrusal │ Yıldız │ Halka │ Ağaç │ Hibrit         │      │
│  │  Yedeklilik: MRP (IEC 62439-2) │ DLR │ HSR/PRP │ RSTP         │      │
│  │  Mantıksal: Purdue/ISA-95 Katmanları (L0–L5)                  │      │
│  │  Karar: AIC önceliği — Kullanılabilirlik önce gelir            │      │
│  └──────────────────────────────┬─────────────────────────────────┘      │
│                                 │                                         │
│     "Katmanlar nerede?"         │ "Her katmana kim girebilir?"            │
│                                 ▼                                         │
│  02_security.md                                                           │
│  ┌────────────────────────────────────────────────────────────────┐      │
│  │                   GÜVENLİK (Sınırlar ve Kontroller)            │      │
│  │                                                                │      │
│  │  Bölge/Kanal: IEC 62443 Zone-Conduit mimarisi                 │      │
│  │  iDMZ (L3.5): Çift FW, "terminate-and-initiate" prensibi      │      │
│  │  VLAN: Segmentasyon kolaylaştırıcı (tek başına yetmez)        │      │
│  │  Derinlemesine Savunma: Fiziksel → Ağ → Protokol → Kimlik     │      │
│  │  SL 1–4: Risk tabanlı hedef güvenlik seviyesi                  │      │
│  └──────────────────────────────┬─────────────────────────────────┘      │
│                                 │                                         │
│     "Sınırlar çizildi."         │ "Peki gecikme bütçesi ne?"              │
│                                 ▼                                         │
│  03_performance.md                                                        │
│  ┌────────────────────────────────────────────────────────────────┐      │
│  │                   PERFORMANS (Zamanlama + Güvenilirlik)         │      │
│  │                                                                │      │
│  │  Gecikme: PROFINET RT (< 1 ms) │ IRT (< 50 µs) │ EtherCAT    │      │
│  │  Jitter:  IRT (≤ 1 µs) │ EtherCAT (< 1 µs) │ TSN (< 1 µs)   │      │
│  │  Yedeklilik: MRP (< 200 ms) │ PRP (0 ms) │ HSR (0 ms)        │      │
│  │  QoS: CoS/PCP 0–7, PROFINET RT = PCP 6, Strict Priority       │      │
│  │  Kural: T_network < %10 × T_scan                              │      │
│  └────────────────────────────────────────────────────────────────┘      │
│                                                                           │
│  ───────────────────── KIRILGAN NOKTALAR ──────────────────────         │
│  Topoloji ↔ Güvenlik : VLAN olmadan Purdue katmanları sanal kalır        │
│  Güvenlik ↔ Performans: FW derin paket denetimi gecikme ekler            │
│  Topoloji ↔ Performans: Halka büyüklüğü MRP kurtarma süresini etkiler   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Mental Model: Bir Endüstriyel Ağı Kurarken Üç Soruya Cevap Ver

> **1. "Nerede?"** — Topoloji kararı. Her cihazı Purdue katmanına yerleştir. Fiziksel topoloji: yıldız, halka, hibrit. Yedeklilik: hangi protokol, kaç düğüm, kurtarma süresi bütçesi nedir?

> **2. "Kim girebilir?"** — Güvenlik kararı. Her katman sınırına güvenlik duvarı, iDMZ'ye çift FW + "terminate-and-initiate". IEC 62443 ile her işlevsel gruba SL hedefi ata. VLAN + FW birlikte çalışır, biri tek başına yetmez.

> **3. "Ne kadar hızlı?"** — Performans kararı. Uygulama sınıfını belirle (RT A/B/C). Ağ gecikmesi T_scan'ın %10'undan az olmalı. Güvenlik duvarı DPI'ı gecikme bütçesine ekle; IRT ağında FW atlatmak için protokol aracısı kullan.

Bu üç soru yanıtlanmadan tasarım tamamlanmış sayılmaz.

## Hızlı Referans Tabloları

### A. Topoloji Seçimi (Belge 1'den)

| Topoloji | Avantaj | Dezavantaj | Ne Zaman |
|---|---|---|---|
| **Doğrusal (Line)** | Düşük kablo maliyeti, EtherCAT için ideal | Tek kopma tümünü keser | L0-L1 fieldbus, EtherCAT zincirleri, konveyör |
| **Yıldız** | Kolay bakım, bağımsız port izleme | Switch = tek arıza noktası | Küçük hücre (< 15 cihaz), kesinti toleransı yüksek |
| **Halka + MRP** | Kablo kopmasına dayanıklı, < 200 ms kurtarma | Biraz fazla kablo, 50 düğüm sınırı | Orta/büyük tesisler, PROFINET, < 1 dk tolerans |
| **Ağaç** | Ölçeklenebilir, hiyerarşik yönetim | Üst switch arızası tüm dalları keser | Geniş tesisler, omurga halka + yıldız dal hibridine alt yapı |
| **Hibrit (halka omurga + yıldız dallar)** | Yedeklilik + kolay yönetim + ölçek | Karmaşık konfigürasyon | Gerçek fabrika: çoğunlukla bu kullanılır |

### B. Purdue Katmanları ve Segmentasyon (Belge 1 + 2'den Konsolide)

| Katman | İçerik | VLAN Örneği | Hedef SL (IEC 62443) | Geçiş Noktası |
|---|---|---|---|---|
| **L5 Bulut** | ERP (dış/bulut) | VLAN 10 | SL 2 | İnternet FW |
| **L4 Kurumsal IT** | ERP, e-posta, AD | VLAN 10 | SL 2 | FW-1 |
| **L3.5 iDMZ** | Jump server, historian kopyası, yama | VLAN 20 | SL 2-3 | FW-2 |
| **L3 MES/SCADA** | Historian, SCADA sunucusu, MES | VLAN 30 | SL 3 | FW-3 |
| **L2 Denetim** | HMI, mühendislik istasyonu, DCS | VLAN 40 | SL 3 | FW |
| **L1 Temel Kontrol** | PLC, RTU, SIS/SIL | VLAN 50/51 | SL 3 | — |
| **L0 Fiziksel** | Sensör, aktüatör, motor | — | SL 2-3 | — |
| **SIS (izole)** | Güvenlik PLC'leri | VLAN 60 | SL 4 | Fiziksel izolasyon |

**Temel kural**: Komşu olmayan katmanlar arasında doğrudan iletişim yasaktır. L4 → L1 erişimi her zaman FW-1 → iDMZ → FW-2 → FW-3 üzerinden geçmelidir. (Kaynak: Belge 2 — SentinelOne/Palo Alto Purdue kılavuzları)

### C. Yedeklilik Protokolleri Karşılaştırması (Belge 1 + 3'ten Konsolide)

| Protokol | Standart | Kurtarma | Bant Yükü | Topoloji | Kullanım Yeri |
|---|---|---|---|---|---|
| **MRP** | IEC 62439-2 | < 10 ms (≤14 düğüm) / < 200 ms (≤50 düğüm) | Minimal | Halka | PROFINET ağları |
| **DLR** | ODVA | < 3 ms | Minimal | Halka | EtherNet/IP (Allen-Bradley) |
| **HSR** | IEC 62439-3 | ~0 ms (kayıpsız) | ×2 | Halka | Güç şebekeleri, bay bus (≤32 düğüm) |
| **PRP** | IEC 62439-3 | ~0 ms (kayıpsız) | ×2 | İkili paralel ağ | Kritik altyapı, sıfır kesinti |
| **RSTP** | IEEE 802.1w | 1–5 saniye | Minimal | Herhangi | Sadece IT — OT için kullanma |

**Önemli not**: HSR/PRP'de "sıfır kurtarma" = çerçeve kaybı yok; jitter'ın sıfır olduğu anlamına gelmez. Yol asimetrisi jitter artışına yol açabilir. (Kaynak: Belge 3 — ICNavigator teknik karşılaştırması)

### D. Gerçek Zamanlılık Sınıfları ve QoS Parametreleri (Belge 3'ten)

| Sınıf | Çevrim Süresi | Jitter | Protokol | PCP (CoS) |
|---|---|---|---|---|
| **RT Sınıf A** | < 100 ms | Yüksek | PROFINET NRT, SCADA polling | 0–2 |
| **RT Sınıf B** | < 10 ms | ≤ 100 µs | PROFINET RT, standart PLC I/O | 6 |
| **RT Sınıf C** | < 1 ms | ≤ 1 µs | PROFINET IRT, EtherCAT, TSN | 6 + donanım |

**Kural**: T_network ≤ %10 × T_scan. 1 ms çevrim → maksimum 100 µs ağ gecikmesi → IRT veya EtherCAT zorunlu. (Kaynak: Belge 3 — pratik kural)

**CoS kuyruğu önerisi (Maple Systems):**

```
CoS 6-7  → Kuyruk 4  (Strict Priority) — PROFINET RT/IRT siklik veri
CoS 4-5  → Kuyruk 3  (WRR ağırlık 40) — HMI, zaman-kritik kontrol
CoS 2-3  → Kuyruk 2  (WRR ağırlık 30) — SCADA sorgu/yanıt
CoS 0-1  → Kuyruk 1  (WRR ağırlık 30) — Yedek yazılım, güncelleme, IT trafiği
```

### E. Konsolide Edge-Case ve Sistem Limiti Tablosu (Üç Belgeden)

Sınır koşulları, üç belgenin en pahalı derslerini bir araya getirir. Her satır "nominalde çalışır, sınırda çöker" sınıfındandır.

| Edge-Case / Limit | Belge | Kök Neden | Sonuç | Önlem |
|---|---|---|---|---|
| MRP > 50 düğüm | 01 | Test çerçevesi tur süresi garantiyi aşar | Kurtarma süresi tanımsız | Halkayı böl, MRP-Interconnection |
| Eşzamanlı çift kopma | 01 | Halka 2 segmente bölünür | Her iki segment izole | PRP (iki bağımsız ağ) |
| RSTP + MRP aynı portta | 01 | İki protokol portu çeker | Port flapping | MRP halkada RSTP'yi kapat |
| Fiber sync domain mesafesi | 01 | Yayılım gecikmesi (~5 µs/km) | PTCP saat sapması | IRT sync domain'i kısa tut |
| VLAN/TCAM limiti | 01/02 | Switch donanım kural tablosu dolar | Segment eklenemez | Plan switch limitine göre |
| L2 broadcast/multicast | 02 | DCP/keşif L3 FW'yi atlar | Saldırgan VLAN içinde keşif | Mikro-segment + L2 ACL |
| Fail-open vs fail-closed | 02 | FW arıza davranışı belirsiz | Üretim durur / korumasız kalır | Kritik yolda HA çift |
| Eski protokol kimlik yok | 02 | Modbus/S7Comm auth'suz | IP spoof ile komut yazma | Conduit kısıt + DPI beyaz liste |
| DPI fail-closed | 02/03 | Protokol sürümü değişti | Mühendislik erişimi kesildi | DPI'ı firmware ile koordine et |
| IGMP Querier yokluğu | 03 | Snooping tablosu zaman aşımı | Multicast flood / kesinti | Statik querier ata |
| Çevrim < 250 µs + NRT | 03 | Yeşil faza çerçeve sığmaz | NRT imkansız | Frame preemption / sadece IRT segment |
| Tail latency (%99.99) | 03 | Ortalama iyi, kuyruk kötü | Tek çevrimde senkron kaybı | Maks/persentil ölç |
| Mikro-burst | 03 | Anlık tampon dolumu | RT çerçeve gecikir/düşer | Strict priority + ayrı kuyruk |
| HSR > 32 düğüm | 01/03 | Çoğaltma trafiği halkayı doldurur | Faydalı bant kalmaz | Halka boyutunu sınırla |
| Gigabit yükseltme QoS sıfırlar | 03 | Yeni ASIC varsayılana döner | Önceliklendirme kaybolur | Donanım değişiminde QoS doğrula |

### F. Uzman Optimizasyon Sıralaması (Üç Belgeyi Birleştiren)

Optimizasyon bağımsız değil, **sıralı**dır — yanlış sırada yapılan bir adım sonrakini geçersiz kılar. Uzman önceliklendirme:

```
1. ÖLÇ (03)        → Gerçek jitter/persentil/kayıp; baseline trafiği logla (02)
                     "Görmediğini optimize edemezsin / koruyamazsın"
2. HATA ALANI (01) → Fault domain'i küçült: halkaları böl, çift uplink
                     En yüksek getiri burada; sonraki adımlar bunun üzerine kurulur
3. GÖRÜNÜRLÜK (02) → Pasif varlık keşfi; ne var bilinmeden segmentlenemez
4. SEGMENT (01+02) → Risk sırasıyla: iDMZ → SIS → kritik hücre → yardımcı
5. ZAMANLAMA (03)  → Cut-through + hop azalt + QoS (CoS güven → SP → WRR)
6. SIKILAŞTIR (02) → "İzin+logla" baseline → açık kural → varsayılan engelle
7. YEDEKLİLİK (01) → MRP/PRP/HSR'i watchdog ve bant bütçesine sığdır
8. DOĞRULA        → Kabloyu kes (kurtarma), yük bin (jitter), kural test et
```

**Sıralama mantığı**: Ölçmeden optimize etmek körlemedir (1). Hata alanını küçültmek diğer her şeyi kolaylaştırır (2). Segmentasyon görünürlük olmadan eksik kalır (3→4). QoS, segmentasyon kararından sonra anlamlıdır (5). Kural sıkılaştırma ölçülen baseline'a dayanmalıdır (6). Yedeklilik son katmandır çünkü performans ve güvenlik bütçesini tüketir (7). Hiçbir adım doğrulamadan tamamlanmış sayılmaz (8).

## Pratikte Nasıl Kullanılır

### "Yeni Tesis Tasarımı" Kontrol Listesi

Aşağıdaki adımları sırayla tamamlayan biri, endüstriyel bir ağın temel tasarım kararlarını verebilir:

**Adım 1 — Envanter ve Sınıflandırma (Belge 1 + 2)**

```
□ 1. Tüm cihazları listele: PLC, HMI, sensör ağ geçidi, switch, mühendislik istasyonu
□ 2. Her cihaza Purdue katmanı ata (L0–L5)
□ 3. Kritiklik puanı ata: "Bu cihaz dursa ne olur?" (güvenlik / üretim / çevre)
□ 4. İşlevsel grupları belirle: makine A hücresi, makine B hücresi, SCADA odası
```

**Adım 2 — Fiziksel Topoloji Kararı (Belge 1)**

```
□ 5. Kablo mesafelerini ölç: 100 m üzeri veya yüksek EMI → fiber
□ 6. Kesinti toleransını belirle: > 1 dk → yıldız; < 1 dk → halka+MRP; sıfır → PRP/HSR
□ 7. Düğüm sayısını say: MRP halkası ≤ 50 düğüm; fazlası → birden fazla halka
□ 8. Her konuma MANAGED switch planla — unmanaged switch kabul edilemez
□ 9. IRT uygulaması varsa: Conformance Class C onaylı, cut-through switch zorunlu
```

**Adım 3 — Güvenlik Mimarisi (Belge 2)**

```
□ 10. IT ve OT ağları arasında iDMZ (L3.5) planla: FW-1 + iDMZ sunucuları + FW-2
□ 11. Her işlevsel grup için VLAN tanımla (VLAN tek başına yetmez; FW kuralıyla birlikte)
□ 12. IEC 62443 SL hedeflerini ata: üretim PLC'leri için başlangıç SL 2-3
□ 13. Uzak erişim mimarisi: VPN+MFA → Jump Server (iDMZ) → OT (en az ayrıcalık)
□ 14. Kural seti: varsayılan tümünü engelle, isteneni açık (deny-all, permit-by-exception)
```

**Adım 4 — Performans ve QoS Yapılandırması (Belge 3)**

```
□ 15. Uygulama sınıfını belirle: standart I/O → RT; servo/hareket → IRT veya EtherCAT
□ 16. Çevrim süresi hesapla: T_scan + T_network + T_fieldbus + T_actuator → toplam bütçe
□ 17. Switch'lerde CoS güven modunu etkinleştir: PROFINET portlarında PCP = 6 etiketleme
□ 18. Storm control her porta aktif et: broadcast %2-5 eşik, IGMP snooping aktif
□ 19. MRP/PRP/HSR yapılandır, test et: kablo keserek kurtarma süresini ölç
```

**Adım 5 — Doğrulama ve Belgeleme**

```
□ 20. Topoloji diyagramı çiz ve kablolama ile birlikte belgele (güncel tut!)
□ 21. Güvenlik duvarı kural setini test ortamında test et, üretimde geçerli kıl
□ 22. Watchdog tetiklemeden MRP kurtarma süresini doğrula
□ 23. Karma trafik altında QoS etkinliğini ölç (yük testi ile jitter ölçümü)
```

### Üç Belgeyi Bağlayan Pratik Senaryo: 20 Eksenli Baskı Makinesi Ağı

Bu senaryo, üç belgenin kesişim noktasıdır.

```
TOPOLOJİ KARARI (Belge 1):
  - 20 servo sürücü + PLC + 2 HMI + historian
  - Omurga: 2 core switch, fiber, MRP (< 200 ms kurtarma)
  - Makine hücresi: yıldız, managed switch, bakır 100 Mbps
  - Servo zincirleri: PROFINET IRT (≤ 1 µs jitter)

GÜVENLİK KARARI (Belge 2):
  - PLC hücresi: VLAN 50, SL 3
  - HMI / Mühendislik: VLAN 40, SL 3
  - SCADA: VLAN 30, SL 3
  - iDMZ: VLAN 20 — historian kopyası + yama sunucusu
  - FW-2 kuralı: SCADA → PLC yalnızca OPC UA port 4840, okuma

PERFORMANS KARARI (Belge 3):
  - Servo senkronizasyonu: PROFINET IRT, 500 µs çevrim, ≤ 1 µs jitter
  - Switch: Conformance Class C, cut-through mod
  - PTCP senkronizasyon sapması: ≤ 1 µs
  - CoS: servo portlarında PCP = 6 → Kuyruk 4 (Strict Priority)
  - Storm control: her porta %2 broadcast eşiği

KIRILGAN NOKTALAR:
  - FW-2 DPI gecikmesi: OPC UA trafiği için < 200 µs bütçelendi
  - MRP kurtarma süresi: 32 düğüm, < 150 ms hedef, watchdog = 500 ms
  - IRT switch firmware: üretici doğrulaması kurulumdan önce yapıldı
```

## Sık Yapılan Hatalar

### En Kritik 7 Hata (Üç Belgeden Konsolide)

**1. Unmanaged switch kullanmak** *(Belge 1)*

```
❌ Maliyet için unmanaged switch → MRP yok, VLAN yok, QoS yok, SNMP yok
✅ Her konumda managed switch; IRT için Conformance Class C onaylı
```

**2. RSTP'yi MRP yerine kullanmak** *(Belge 1)*

```
❌ Halka topolojide RSTP aktif → kablo koptuğunda 1-5 sn kesinti → watchdog tetiklenir
✅ PROFINET: MRP; EtherNet/IP: DLR; kritik altyapı: HSR/PRP
```

**3. iDMZ olmadan IT/OT bağlantısı** *(Belge 2)*

```
❌ ERP → doğrudan → PLC → fidye yazılımı fabrikayı kapatır (bkz. NotPetya)
✅ ERP → FW-1 → iDMZ → FW-2 → SCADA → PLC
```

**4. VLAN'ı tek başına güvenlik katmanı saymak** *(Belge 1 + 2)*

```
❌ "VLAN var, güvendeyiz" → FW yoksa VLAN hopping ile atlatılır
✅ Her VLAN sınırında Layer-3 güvenlik duvarı; varsayılan kural = engelle
```

**5. IRT ağında store-and-forward switch kullanmak** *(Belge 3)*

```
❌ IRT ağında IT tipi switch → gecikme IRT jitter bütçesini (1 µs) çok aşar
✅ Conformance Class C onaylı, cut-through modlu switch; firmware doğrulaması zorunlu
```

**6. Çevrim süresini ağ gecikmesini hesaplamadan belirlemek** *(Belge 3)*

```
❌ "PLC görevim 500 µs, yeter" → T_network + T_fieldbus hesaplanmadı → kararsızlık
✅ T_scan + T_network ≤ toplam bütçe; T_network ≤ %10 × T_scan
```

**7. PRP'de "bağımsız" ağların aslında paylaşımlı olması** *(Belge 3)*

```
❌ LAN A ve LAN B aynı UPS → UPS arızasında PRP garantisi anlamsızlaşır
✅ Fiziksel yol, güç kaynağı ve rack konumu LAN A ve LAN B için tamamen bağımsız olmalı
```

## Ne Zaman ...

### Ne Zaman Halka + MRP, Ne Zaman PRP/HSR?

| Senaryo | Tercih |
|---|---|
| Kesinti toleransı > 1 dakika | Yıldız topoloji, MRP yok |
| Kesinti toleransı < 1 dakika, üretim hattı | Halka + MRP (< 200 ms) |
| Watchdog < 100 ms, hareket kontrol | MRP < 30 ms yapılandırması veya DLR |
| Sıfır çerçeve kaybı, güç şebekesi, SIS | PRP (iki bağımsız LAN) veya HSR (halka) |
| Büyük halka (> 32 düğüm) | HSR yerine birden fazla MRP halkası + RedBox |

### Ne Zaman PROFINET RT, Ne Zaman IRT veya EtherCAT?

| Senaryo | Tercih |
|---|---|
| Standart I/O: sıcaklık, basınç, 250 µs–10 ms çevrim | PROFINET RT |
| Servo senkronizasyonu, çok eksen, < 500 µs, ≤ 1 µs jitter | PROFINET IRT |
| En yüksek performans, < 100 µs, robotik, koordineli hareket | EtherCAT |
| IT+OT aynı ağda, yeni tesis, OPC UA PubSub determinizm | TSN |

### Ne Zaman Veri Diyotu, Ne Zaman Güvenlik Duvarı?

| Senaryo | Tercih |
|---|---|
| Yalnızca OT→IT veri akışı (historian), kritik altyapı (SL 4) | Veri diyotu |
| İki yönlü iletişim gerekiyor (mühendislik erişimi, yama) | Güvenlik duvarı |
| Bütçe kısıtlı, orta ölçek tesis, SL 2-3 | Güvenlik duvarı + sıkı kural seti |

### Ne Zaman Bu Üç Belge Yetmez?

```
Yetersiz Kaldığı Durum                  Bakılacak Sonraki Kaynak
─────────────────────────────────────────────────────────────────
OPC UA güvenliği (şifreleme, RBAC)     → knowledge/protocols/opc-ua/03_security
PROFINET IO mimarisi, GSD, tanılama    → knowledge/protocols/profinet/
EtherCAT protokol katmanları (CoE, FoE)→ knowledge/protocols/ethercat/
IEC 62443 tam standart detayları       → knowledge/standards/02_iec62443
Historian replikasyonu ve iDMZ akışı   → knowledge/applications/historian/
Real-time OS, CPU interrupt latency    → knowledge/hardware/industrial-pc/03_performance_tuning
PLC görev yapısı, watchdog, scan time  → knowledge/codesys/task-structure/02_cycle_time
```

## Gerçek Proje Notları

**Not 1 — Topoloji Kararı Güvenliği Doğrudan Etkiler**
Bir tesiste fiziksel topoloji basit yıldız iken Purdue katmanları VLAN ile sanal olarak uygulandı. Ancak VLAN'lar arası yönlendirme için Layer-3 switch yerine unmanaged switch kullanılmıştı. VLAN'lar var gibi görünüyordu; VLAN hopping ile hepsi atlatılabiliyordu. Topoloji kararı (unmanaged switch) güvenlik mimarisini görünmez biçimde geçersiz kıldı. **Ders: Topoloji ve güvenlik kararları ayrı alınamaz; switch seçimi her ikisini birden etkiler.** (Belge 1 — Proje Notu 3; Belge 2 — Hata 3)

**Not 2 — MRP Kurtarma Süresi, Watchdog ve Switch Firmware Üçlüsü**
Bir otomobil fabrikasında 32 düğümlü MRP halkasında watchdog zaman aşımları yaşandı. Belgede < 200 ms garantisi vardı; ancak karışık üretici switch ortamında kurtarma süresi 350 ms'e çıkıyordu. Aynı anda PLC watchdog süresi 300 ms ayarlıydı. Çözüm: tüm halka switch'leri aynı üreticinin onaylı cihazlarına döndürüldü, watchdog 500 ms'e ayarlandı, ortalama kurtarma 143 ms'e indi. **Ders: MRP kurtarma süresi, watchdog süresi ve switch firmware uyumluluğu birlikte planlanmalıdır.** (Belge 1 + 3 kesişimi)

**Not 3 — Güvenlik Duvarı DPI Gecikmesi IRT Bütçesini Yer**
Bir PROFINET IRT ağında, iDMZ güvenlik duvarının OT tarafında DPI etkinleştirilmişti. FW'nin S7Comm derin paket denetimi, IRT çevrim süresi bütçesinin (500 µs) %40'ını tüketiyordu. Servo eksenlerinde 5–8 µs jitter hedefi 25 µs'e çıktı. Çözüm: IRT trafiği FW bypass listesine alındı; OPC UA SCADA trafiği DPI kapsamında tutuldu; IRT segmenti ayrı VLAN'a alındı. **Ders: Güvenlik duvarı DPI gecikmesi performans bütçesine dahil edilmelidir.** (Belge 2 + 3 kesişimi)

**Not 4 — Storm Control Olmadan Üretim Durması**
Bir otomotiv montaj hattında tüm PROFINET cihazları periyodik olarak 1-2 dakika çevrimdışı kalıyordu. Wireshark analizi, arızalı bir IO-Link gateway'in 50.000 paket/saniye broadcast gönderdiğini ortaya koydu. Storm control hiç yapılandırılmamıştı. **Ders: Storm control, "normal çalışmada görünmez; ancak arıza anında ağı kurtarır" kategorisindedir. Her porta %2-5 eşik ile yapılandırılmalıdır.** (Belge 3 — Proje Notu 3)

**Not 5 — iDMZ Olmayan Bir Tesiste Fidye Yazılımı Yayılımı**
Bir üretim tesisinde IT ağından OT'ye doğrudan erişim vardı. Muhasebe bilgisayarından yayılan fidye yazılımı, SCADA sunucusuna, oradan PLC'lere ulaştı. Tesis 18 saat durdu. Sonradan kurulan iDMZ tüm IT→OT trafiğini kesti. **Ders: iDMZ, "geleceğe yönelik güzel eklenti" değil, minimum temel gerekliliktir. İki FW'nin maliyeti, bir saatlik üretim kaybının çok altındadır.** (Belge 2 — Proje Notu 1)

**Not 6 — TSN GCL Planlaması ve Beklenmedik Trafik**
Bir pilot TSN projesinde GCL (Gate Control List) yapılandırması sırasında bir HMI video akışı gözden kaçırıldı. Video akışı IRT zaman penceresine denk gelince servo eksenlerinde 5 ms gecikme oluştu. 802.1Qcc ile otomatik akış planlamasına geçilince sorun ortadan kalktı. **Ders: TSN'de GCL planlaması, ağdaki her veri akışının önceden karakterize edilmesini gerektirir.** (Belge 3 — Proje Notu 5)

**Not 7 — Aynı Birleştirici İlke, Üç Farklı Pencere: Tek Kök Neden Üç Belgeyi Birden Vurur**
Bir tesiste yönetim VLAN'ı üretim VLAN'ıyla aynı subnet'teydi (Belge 2 — Not 8: güvenlik açığı). Aynı yanlış yapılandırma, switch yönetim trafiği ile RT trafiğini aynı broadcast domain'de tutuyordu; bir keşif fırtınası RT jitter'ini bozuyordu (Belge 3: performans). Ve bu yapılandırma, topoloji diyagramında "ayrı yönetim ağı" olarak gösteriliyordu (Belge 1: belgeleme tutarsızlığı). Tek bir kök neden, üç belgenin de uyardığı üç ayrı belirti üretti. **Ders: Topoloji/güvenlik/performans ayrı denetlenmez — bir yapılandırma hatası üç boyutta birden tezahür eder. Birleştirici ilke (garantili omurga) ihlal edildiğinde semptomlar her üç pencerede görünür.** (Belge 1+2+3 kesişimi)

**Not 8 — "Daha İyi Donanım" Tuzağı: Yükseltme Determinizmi Bozdu**
Bir omurga 100 Mbps'ten 1 Gbps'e yükseltildi (Belge 3 — Not 6). Daha geniş bant beklenirken RT jitter kötüleşti çünkü yeni ASIC QoS'u varsayılana sıfırlamıştı. Aynı yükseltme sırasında yeni switch fabrika varsayılanı MRM ile geldi ve halkada çift-MRM çakışması riski doğdu (Belge 1 — Not 5). **Ders: Donanım yükseltmesi, "garantili omurga"nın üç boyutunu (topoloji rolü, QoS, yedeklilik yapılandırması) sıfırlayabilir. Her donanım değişiminden sonra MRP rolü, QoS/CoS haritalaması ve segmentasyon ayrı ayrı yeniden doğrulanmalıdır. "Daha hızlı link" ≠ "daha iyi ağ".** (Belge 1+3 kesişimi)

## İlgili Konular

```
knowledge/networking/                  ← Şu an buradasınız
├── 01_topologies.md                   → Fiziksel topoloji, MRP mimarisi, Purdue modeli
│                                        (Uzman: MRP iç mekanizması, edge-case'ler, optimizasyon)
├── 02_security.md                     → IEC 62443 zone/conduit, iDMZ, DPI, defense-in-depth
│                                        (Uzman: terminate-and-initiate, veri diyotu fiziği, DiD matematiği)
├── 03_performance.md                  → RT/IRT/EtherCAT/TSN, QoS, PRP/HSR nicel değerler
│                                        (Uzman: IRT zaman-bölme, cut-through determinizmi, tail latency)
└── _synthesis.md (bu belge)           → Birleştirici ilke, konsolide edge-case tablosu, optimizasyon sırası

knowledge/standards/
└── 02_iec62443                        → IEC 62443 standart serisi tüm detaylar (02_security.md özet)

knowledge/protocols/
├── profinet/                          → PROFINET IO mimarisi, GSD dosyaları, MRP, PTCP
├── ethercat/                          → EoE, CoE, FoE, SoE; dağıtık saat detayları
└── opc-ua/03_security                 → OPC UA güvenliği: şifreleme, RBAC, iDMZ geçişi

knowledge/hardware/
└── industrial-pc/03_performance_tuning → Real-time OS, PREEMPT_RT, CPU interrupt latency

knowledge/codesys/
└── task-structure/02_cycle_time       → PLC scan time, watchdog, görev yapısı

knowledge/applications/
└── historian/                         → Historian replikasyonu iDMZ üzerinden; güvenli veri akışı
```
