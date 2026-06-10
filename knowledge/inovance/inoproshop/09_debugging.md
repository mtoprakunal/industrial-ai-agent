---
KONU        : InoProShop Hata Ayıklama (Debug) Araçları ve Sistematik Teşhis
KATEGORİ    : inovance
ALT_KATEGORI: inoproshop
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_using_breakpoints.html"
    başlık: "CODESYS Online Help — Using Breakpoints (data breakpoint, watchdog devre dışı, çoklu-task)"
    güvenilirlik: resmi
  - url: "https://content.helpme-codesys.com/en/CODESYS%20EtherCAT/_ecat_troubleshooting.html"
    başlık: "CODESYS EtherCAT — Troubleshooting (working counter, DC sync, packet loss)"
    güvenilirlik: resmi
  - url: "https://idea-tech.in/wp-content/uploads/2020/04/INOVANCE-AM400AM600AC800-PLC-SOFTWARE-MANUAL-ENGLISH-20-4-20.pdf"
    başlık: "Inovance — AM400/AM600/AC800 (InoProShop) User Guide (online/offline emulated debug)"
    güvenilirlik: resmi
  - url: "knowledge/codesys/debugging/_synthesis.md"
    başlık: "CODESYS Debugging — Uzman Sentezi (katman→araç→kök neden)"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "01_inoproshop_overview.md"
    ilişki: gerektirir
  - konu: "08_codesys_to_inoproshop.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/debugging/_synthesis.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/debugging/01_common_errors.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "InoProShop = CODESYS V3 türevi; debug araçları CODESYS ile AYNIDIR (01_inoproshop_overview.md)"
  - "CODESYS debugging temel mantığı (knowledge/codesys/debugging/_synthesis.md)"
  - "Online izleme, breakpoint, force kavramları"
ÇELİŞKİLER :
  - kaynak: "Kullanıcı beklentisi: 'InoProShop'un kendine özgü debug aracı var'"
    konu: "InoProShop'un debug araçları CODESYS V3 ile birebir aynıdır"
    çözüm: >
      Online izleme, breakpoint, single-step, force/write, Trace, Log — hepsi CODESYS
      Development System bileşenleridir. Bu belgedeki her araç CODESYS'ten miras alınır;
      InoProShop'a özgü ek bir teşhis aracı varsayılmadı.
  - kaynak: "Breakpoint canlı makinede güvenli mi?"
    konu: "Breakpoint task'ı durdurur, watchdog devre dışı kalır, I/O güncellenmez"
    çözüm: >
      Canlı motion/EtherCAT sisteminde breakpoint ekseni düşürür ve çıkışları
      belirsiz bırakır. Canlı sistemde Trace tercih edilir; breakpoint simülasyon
      veya güvenli/durmuş sistem içindir.
---

## Özün Ne

InoProShop bir CODESYS V3 türevi olduğundan, hata ayıklama araçları CODESYS
Development System ile **birebir aynıdır**: online izleme (monitoring), breakpoint,
single-step, force/write, Trace ve Device Log. Ayrıca Inovance AM serisi **online hata
tespiti** ve **offline emülasyon (simülasyon) debug** modlarını destekler. Yani CODESYS
debug bilgisi InoProShop'a doğrudan transfer olur.

Debug'ın özü tek bir yöntemdir (CODESYS sentezinden miras): **belirtiyi katmana
haritala → o katmanda en az invazif doğru aracı seç → kök nedene in → doğrula.**
Yanlış katmanda (login hatasını kodda) veya yanlış araçla (canlı motion'a breakpoint)
çalışmak saatler kaybettirir.

## Nasıl Çalışır

### Debug Araç Kümesi (CODESYS'ten miras)

| Araç | Ne yapar | Ne zaman | İnvazivlik / Uyarı |
|---|---|---|---|
| **Device Log** | runtime/sistem olay kaydı | her hatada İLK bakış | sıfır — asla atlama |
| **Online izleme** | çevrimiçi değerleri canlı gösterir | genel davranış izleme | düşük (IDE polling, hızlı sinyal kaçar) |
| **Watch listesi** | seçili değişkenleri izler | belirli değişkenler | düşük |
| **Write / Force** | değer yazar / sabitler | I/O ve alarm testi | orta — unforce'u unutma |
| **Breakpoint** | task'ı satırda durdurur | kod akışı, simülasyon | **en yüksek** — watchdog devre dışı, I/O güncellenmez |
| **Data breakpoint** | değişken değişince durdurur | "bu değeri kim yazdı?" | yüksek — yalnız CODESYS Control Win |
| **Single-step** | satır satır ilerletir | mantık akışını izleme | yüksek — task durur |
| **Trace** | değişkenleri durdurmadan kaydeder | aralıklı arıza, canlı sistem | düşük — canlı izleme için altın standart |
| **EtherCAT diag** | slave durumu, working counter | bus hataları | sıfır (okuma) |

### Breakpoint'in Kritik Davranışı (resmi)

- Program breakpoint'e ulaşınca task **durur** ("HALT ON BP") ve **bu sırada watchdog
  devre dışı kalır**.
- Breakpoint'te duran **debug task'ın çağırdığı I/O'lar güncellenmez** (PLC'de refresh
  ayarı açık olsa bile). Yani çıkışlar son durumda donar — motion için tehlikeli.
- Çoklu-task: aynı anda birden çok task debug edilemez; siz bir task'ta dururken diğer
  task'ların breakpoint'leri yok sayılır, o task'lar çalışmaya devam eder.
- **Sonuç:** Canlı EtherCAT/motion sisteminde breakpoint **kullanılmaz** — eksen
  düşer/çıkış donar. Canlı sistemde **Trace** kullan; breakpoint'i offline emülasyon
  veya güvenli/durmuş sistem için sakla.

### Offline Emülasyon (Simülasyon)

InoProShop, gerçek donanım olmadan mantığı PC üzerinde **emüle ederek** test etmeyi
destekler (CODESYS Simulation mode). Breakpoint/single-step burada güvenle kullanılır,
çünkü gerçek bir eksen/çıkış yoktur. Mantık doğrulaması için ideal; ancak gerçek timing,
EtherCAT senkronu ve I/O fiziği emüle edilmez — onlar yalnız donanımda doğrulanır.

## Pratikte Nasıl Kullanılır

### "Sorun Çıktı" Akışı (katman → araç → kök neden → doğrula)

```
Sorun gözlemlendi
   │
   ▼ 1. Device Log oku — ekran özetine güvenme
   │
   ├── ALTYAPI (login/gateway/sürüm)  → ağ/gateway/port + firmware-IDE sürüm uyumu
   ├── YAPI (lib/I/O/retain)          → Library Manager + I/O eşleme + retain
   ├── KOD (yanlış değer/crash)       → Online izleme → Trace/Data BP (kim/ne zaman)
   ├── BUS (EtherCAT)                 → EtherCAT diag (working counter, DC, kablo)
   └── PERFORMANS (watchdog/jitter)   → Task Monitor Max → bloke I/O / yük / döngü
```

### Yaygın Hatalar ve Çözümleri

**1) Login / bağlanamıyor**
- Belirti: "Cannot connect" / gateway bulunamıyor.
- Kontrol: PLC IP ve ağ erişimi (ping), gateway servisi, kontrolör açık mı.
- Kök neden çoğunlukla altyapı (ağ/gateway), kod değil.

**2) Sürüm uyumsuzluğu (IDE ↔ firmware)**
- Belirti: indirme/derleme hatası, "version mismatch", beklenmedik davranış.
- Kontrol: InoProShop sürümü ile kontrolör firmware sürümünün uyumu; kütüphanelerin
  sabit sürümleri.
- Çözüm: uyumlu sürüm eşlemesi (kesin tablo InoProShop kurulumundan teyit edilir
  `[DOĞRULANMADI]`); kütüphaneleri fix version'a çek.

**3) EtherCAT bus hatası**
- Belirti: slave OP durumuna geçmiyor; "Working counter for sync unit group wrong,
  group set to nonoperational"; "packets lost, check cables".
- Kontrol (resmi sıra):
  1. **Fiziksel önce:** kablo, link LED'leri, slave güç beslemesi.
  2. Device tree'de kırmızı üçgenli (hatalı) cihazı bul; slave durum sayfası.
  3. "Distributed clock always same value" → ilk DC-etkin slave'in IN/OUT konektörlerini
     değiştir (fiziksel port sırası).
  4. EtherCAT Master FB'sinin **LastError** özelliğini IEC kodundan oku.
- Kök neden çoğunlukla fizikseldir (kablo/port/topoloji), config değil.

**4) Watchdog / cycle overrun**
- Belirti: task aniden durdu, watchdog exception (Log'da).
- Kontrol: hangi task düştü (Log) → Task Monitor **Max Exec / Max Cycle** (ortalamaya
  değil, Max'a bak).
- Kök neden adayları: kontrol task'ında **bloke I/O** (Modbus/socket/dosya), sonsuz
  döngü (FOR/WHILE çıkış koşulu), aşırı yük (>%70 CPU).
- Çözüm: bloke I/O'yu Freewheeling task'a taşı; döngü sınırla; yükü böl.
- **Watchdog'u uzatarak/kapatarak "düzeltme" YASAK** (rules.json: watchdog daima açık;
  overrun'ı maskelemek kök sorunu gizler).

**5) Force unutulması (zombi durum)**
- Belirti: stop komutu işe yaramıyor, çıkış beklenmedik kalıyor.
- Kök neden: önceki oturumdan kalan force.
- Çözüm: oturum sonunda tüm force'ları kaldır (Watch All Forces / unforce);
  breakpoint'leri sil.

### Devreye Alma Debug Kontrol Listesi

```
□ Device Log temiz (download/watchdog/exception yok)
□ EtherCAT tüm slave'ler OP, working counter doğru, DC sync tamam
□ Task Monitor: Max Cycle < cycle × 0.70, toplam CPU < %70
□ Tüm force kaldırıldı, tüm breakpoint silindi
□ Create Boot Application + power-cycle testi yapıldı
□ Watchdog açık (kapalı değil)
```

## Örnekler

**Senaryo: Servo zaman zaman "following error", neden belirsiz**

```
1. Katman? (Log) download/watchdog yok, alarm aralıklı → KOD/MOTION, aralıklı
2. Araç: Online izleme aralıklıyı kaçırır → Trace kur
   (komut hız + gerçek hız + following error + alarm), trigger = alarm rising,
   pre-trigger %50-80
3. İncele: alarmdan ~1 sn önce komut hızında sıçrama → following error büyümüş
   → komutu kim yazdı? Data breakpoint (yalnız emülasyon/Win) → şüpheli POU
4. Bus etkisi? EtherCAT diag: working counter doğru, DC sync tamam → bus değil, mantık
5. Düzelt → emülasyonda doğrula → donanımda Trace ile teyit
```

## Sık Yapılan Hatalar

- **Log'u atlamak.** Önce Device Log; ekran özetiyle foruma koşmak zaman kaybı.
- **Canlı motion'a breakpoint koymak.** Watchdog devre dışı kalır, I/O donar, eksen
  düşer. Canlı sistemde Trace kullan.
- **Ortalama cycle'a bakmak.** Spike'lar ortalamada gizlenir; tek anlamlı metrik **Max**.
- **EtherCAT'i config'te aramak.** Hata çoğunlukla fiziksel (kablo/port/güç); önce onu kontrol et.
- **Watchdog'u susturmak.** Tanı sinyalini silmek demektir; kök nedeni bul.
- **Force/breakpoint bırakmak.** Üretime force'lu/breakpoint'li çıkmak gizli arıza üretir.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Breakpoint / single-step:** offline emülasyon veya güvenli/durmuş sistem — EVET.
  Canlı motion/EtherCAT — HAYIR (Trace kullan).
- **Trace:** aralıklı arıza, arıza-öncesi yakalama, canlı sistem — birincil seçim.
- **Force:** I/O ve alarm testi — kontrollü ortamda; safety aktifken dikkat, unforce'u unutma.
- **Online izleme:** genel davranış; ama hızlı sinyalleri kaçırır (Trace'e geç).

## Gerçek Proje Notları

- InoProShop debug'ında CODESYS deneyimi doğrudan işe yarar; yeni öğrenilecek tek şey
  Inovance cihaz/ESI'lerinin diagnostik sayfalarının yeri olur — mantık aynıdır.
- EtherCAT arızalarının büyük çoğunluğu sahada fizikseldir (gevşek konektör, yanlış
  IN/OUT portu, beslemesi düşen slave). "Working counter wrong" görünce ilk refleks
  kablo/port olmalı, saatlerce config kurcalamak değil.
- En sinsi tuzak: emülasyonda kusursuz çalışan mantığın donanımda timing/EtherCAT-senkron
  yüzünden farklı davranması. Emülasyon mantığı doğrular, **timing'i ve I/O fiziğini
  doğrulamaz** — onlar daima donanımda Trace + Task Monitor ile teyit edilir.
- "Orta" olgunluk: araç davranışları CODESYS resmi kaynaklı; sürüm-uyum tablosu ve
  InoProShop'a özgü menü etiketleri kurulu sürümden teyit edilmeli (`[DOĞRULANMADI]`).

## İlgili Konular

- `01_inoproshop_overview.md` — InoProShop = CODESYS V3 (taban)
- `08_codesys_to_inoproshop.md` — taşıma sonrası debug/doğrulama
- `10_best_practices.md` — watchdog/timing/performans ilkeleri
- `knowledge/codesys/debugging/_synthesis.md` — katman→araç→kök neden yöntemi
- `knowledge/codesys/debugging/01_common_errors.md` — login/download/watchdog/library hataları
