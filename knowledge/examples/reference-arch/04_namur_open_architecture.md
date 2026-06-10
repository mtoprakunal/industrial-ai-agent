---
KONU        : NAMUR Open Architecture (NOA)
KATEGORİ    : examples
ALT_KATEGORI: reference-arch
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.namur.net/en/work-areas-and-project-groups/focus-topics/namur-open-architecture.html"
    başlık: "NAMUR Open Architecture (NOA) — namur.net (resmi)"
    güvenilirlik: resmi
  - url: "https://www.namur.net/en/publications/news-archive/ne-175-is-newly-published.html"
    başlık: "NE 175 is newly published (NOA Concept) — namur.net (resmi)"
    güvenilirlik: resmi
  - url: "https://www.beckhoff.com/en-en/industries/process-industry/namur-open-architecture-noa/"
    başlık: "NAMUR Open Architecture (NOA) — Beckhoff"
    güvenilirlik: topluluk
  - url: "https://www.yokogawa.com/eu/blog/chemical-pharma/en/breaking-with-tradition-the-classic-automation-pyramid/"
    başlık: "Breaking with tradition: the classic automation pyramid — Yokogawa"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/examples/reference-arch/01_isa95_hierarchy.md"
    ilişki: tamamlar
  - konu: "knowledge/standards/03_namur_ne107.md"
    ilişki: tamamlar
  - konu: "knowledge/standards/02_iec62443.md"
    ilişki: gerektirir
  - konu: "knowledge/examples/reference-arch/03_opcua_companion_specs.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/opc-ua/03_security.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "ISA-95 otomasyon piramidi ve L0-L4 seviyeleri (01_isa95_hierarchy.md)"
  - "OT/IT segmentasyon ve IEC 62443 Zone/Conduit (knowledge/standards/02_iec62443.md)"
  - "NAMUR NE107 cihaz sağlık diagnostiği (knowledge/standards/03_namur_ne107.md)"
ÇELİŞKİLER :
  - kaynak: "NOA = piramidi yıkar / DCS'i değiştirir algısı"
    konu: "NOA çekirdek kontrol sistemine DOKUNMAZ; yanına ikinci kanal ekler"
    çözüm: >
      NOA'nın çekirdek ilkesi, geleneksel proses kontrol (Core Process Control)
      sistemini DEĞİŞTİRMEDEN, izleme ve optimizasyon (M+O) için ayrı, açık ve
      güvenli bir İKİNCİ KANAL açmaktır. Mevcut DCS/PLC, alarm ve güvenlik
      mantığı olduğu gibi kalır; NOA yalnızca veriyi yan kapıdan dışarı (ve
      kontrollü biçimde geri) akıtır.
  - kaynak: "M+O kanalından kontrole serbest yazma algısı"
    konu: "IT'den çekirdek kontrole geri akış denetimsiz olamaz"
    çözüm: >
      NOA, IT/M+O alanından çekirdek kontrole geri akışı "Verification of
      Request" (NE 178) ile zorunlu kılar: her geri istek doğrulanmadan kontrol
      sistemine etki edemez. Bu, "raporlama ≠ kontrol" ilkesinin NOA'daki resmi
      karşılığıdır; tek yönlü gözlem serbest, kontrole geri yazma denetlidir.
---

## Özün Ne

**NAMUR Open Architecture (NOA)**, proses endüstrisi kullanıcı derneği NAMUR'un
geliştirdiği bir referans mimari kavramıdır. Temel fikri tek cümleyle: **çekirdek proses
kontrol sistemine (DCS/PLC, alarm, emniyet) hiç dokunmadan, sahadaki zengin veriyi
izleme ve optimizasyon (Monitoring + Optimization, "M+O") amacıyla ayrı, açık ve güvenli
bir ikinci kanaldan üst sistemlere/buluta açmak.** NOA, klasik otomasyon piramidinin
verinin yukarı akışını boğan katı yapısını, piramidi bozmadan aşmayı hedefler.

NOA bir dizi NAMUR Tavsiyesiyle (NE) somutlaşır: **NE 175** (NOA Konsepti), **NE 176**
(NOA Bilgi Modeli), **NE 177** (NOA Güvenlik Bölgeleri ve Güvenlik Ağ Geçidi); geliştirme
aşamasında **NE 178** (Verification of Request bileşeni) ve **NE 179** (Aggregating Server
konsepti).

Neden önemli: Proses endüstrisinde tesisler on yıllarca çalışır; çekirdek kontrolü
değiştirmek hem riskli hem pahalıdır. NOA, "mevcut sistemi riske atmadan dijitalleşme/
analitik/tahminsel bakım nasıl yapılır?" sorusunun standart cevabıdır. Agent, brownfield
proses tesislerinde veri açma sorularında NOA'yı doğru çerçeve olarak önermelidir.

## Nasıl Çalışır

### İki Alan + İkinci Kanal

```
        ┌──────────────────────────────────────────────────────────┐
   IT / │   M+O ALANI (Monitoring + Optimization)                  │
  Bulut │   Tahminsel bakım, fleet yönetimi, analitik, optimizasyon │
        │   Aggregating Server (NE 179), NOA Bilgi Modeli (NE 176)  │
        └───────────────▲───────────────────────┬──────────────────┘
                        │ tek yön: gözlem        │ geri akış: DENETLİ
                        │ (serbest, salt-okuma)  │ "Verification of Request"
            ┌───────────┴───────────────────────▼──────────────┐
            │   NOA GÜVENLİK AĞ GEÇİDİ / GÜVENLİK BÖLGELERİ      │  NE 177
            │   (data diode benzeri tek-yön + denetli geri yol)  │
            └───────────▲───────────────────────────────────────┘
                        │  İKİNCİ KANAL (saha verisi kopyası)
   ┌────────────────────┴──────────────────────────────────────┐
   │   ÇEKİRDEK PROSES KONTROL (Core Process Control)           │
   │   DCS / PLC / SIS — DEĞİŞMEZ, dokunulmaz                   │
   │   Klasik otomasyon piramidi (L1-L2) olduğu gibi çalışır     │
   └───────────────────────────────────────────────────────────┘
```

- **Core Process Control (çekirdek kontrol):** Mevcut DCS/PLC/SIS. NOA buna dokunmaz;
  kapalı çevrim, alarm, emniyet işlevleri aynen kalır. Güvenlik ve sertifikasyon riski yok.
- **İkinci kanal:** Saha verisinin bir *kopyasını* çekirdek kontrolün dışına, M+O alanına
  taşır. Genellikle salt-okuma; çekirdek kontrolü etkilemez.
- **M+O alanı:** İzleme + optimizasyon uygulamaları (tahminsel bakım, varlık yönetimi,
  enerji/proses optimizasyonu, analitik, bulut).
- **NOA Güvenlik Ağ Geçidi (NE 177) + Güvenlik Bölgeleri:** İkinci kanalı güvenli kılan
  sınır; tek-yön (data-diode benzeri) gözlemi serbest bırakır, geri akışı kısıtlar.
- **Verification of Request (NE 178):** IT/M+O alanından çekirdek kontrole *geri* gelen
  her istek, çekirdek sisteme etki etmeden önce doğrulanır. Denetimsiz geri yazma yasaktır.
- **Aggregating Server (NE 179):** Birçok kaynağın verisini toplayıp M+O için tek bir
  birleşik bilgi modeli (NE 176) olarak sunar; pratikte OPC UA tabanlıdır.

### Piramitle İlişkisi

NOA piramidi *yıkmaz*, *aşar*: çekirdek kontrol klasik piramit olarak (L1-L2) çalışmaya
devam ederken, veri yan kapıdan M+O alanına akar. Bu, ISA-95'teki "veri yukarı çıktıkça
boğulur" sorununa, seviyeleri bozmadan getirilen pratik bir çözümdür. UNS ile akrabadır:
ikisi de katı dikey akışı gevşetir; NOA özellikle **çekirdek kontrol bütünlüğünü ve
güvenliğini koruma** ekseninde, proses endüstrisine özgü ve güvenlik-merkezlidir.

## Pratikte Nasıl Kullanılır

1. **Çekirdeği dokunulmaz ilan et.** İlk ilke: DCS/PLC/SIS konfigürasyonu, mantığı ve
   sertifikasyonu değişmeyecek. Tüm M+O işi yan kanaldan yapılacak.
2. **İkinci kanalı kur.** Saha verisinin kopyasını M+O'ya taşıyacak yolu tasarla: OPC UA
   (sıklıkla PA-DIM bilgi modeliyle), edge gateway, APL (Ethernet-APL) gibi teknolojiler.
3. **Güvenlik ağ geçidini ve bölgeleri tanımla (NE 177 + IEC 62443).** İkinci kanal tek-yön
   gözleme açık; geri akış varsa Verification of Request (NE 178) ile denetlenir. Bu, IEC
   62443 Zone/Conduit modeline doğrudan oturur (bkz. standards/02_iec62443.md).
4. **Aggregating Server (NE 179) ile birleştir.** Çok kaynağı tek OPC UA bilgi modelinde
   (NE 176) topla; M+O uygulamaları tek noktadan tüketsin.
5. **NE107 sağlığını taşı.** Cihaz F/C/S/M durumunu PA-DIM üzerinden M+O'ya getir; tahminsel
   bakımın temel girdisi budur (bkz. standards/03_namur_ne107.md, 03_opcua_companion_specs.md).

## Örnekler

**Senaryo — brownfield tahminsel bakım:** 15 yıllık bir DCS'li proses tesisi. Üretici
DCS'e dokunulmasına izin vermiyor (sertifikasyon/garanti). NOA ile saha cihazlarından
NE107 sağlık + ek diagnostik veri, ikinci kanaldan (OPC UA/PA-DIM + güvenlik ağ geçidi)
bir bulut tahminsel-bakım platformuna akıtılır. Çekirdek kontrol hiç değişmez; titreşim/
sıcaklık trendiyle pompa arızaları önceden yakalanır.

**Senaryo — denetimli optimizasyon geri akışı:** M+O alanındaki bir optimizasyon motoru
yeni bir setpoint önerir. NOA bunu çekirdek kontrole doğrudan *yazmaz*; öneri Verification
of Request (NE 178) üzerinden doğrulanır, ancak onaylanırsa kontrol alanına etki eder.
Böylece optimizasyon kazanımı, emniyet ve raporlama≠kontrol ilkesi korunarak elde edilir.

## Sık Yapılan Hatalar

- **NOA'yı DCS değişimi sanmak.** NOA çekirdeğe dokunmaz; bu yanlış anlama tüm güvenlik
  argümanını çökertir. NOA = yanına ikinci kanal, üstüne değil yerine değil.
- **İkinci kanalı güvensiz açmak.** "Salt veri okuyoruz" diye güvenlik ağ geçidini atlamak.
  İkinci kanal yine bir saldırı yüzeyidir; NE 177 + IEC 62443 zorunlu.
- **Geri akışı denetimsiz bırakmak.** M+O'dan çekirdeğe doğrudan yazmaya izin vermek NOA'nın
  ihlalidir; Verification of Request (NE 178) atlanamaz (raporlama ≠ kontrol).
- **NOA'yı UNS/MQTT ile karıştırmak.** Akraba ama aynı değil: NOA proses endüstrisine özgü,
  çekirdek-koruma ve güvenlik-merkezli bir mimari kavram; UNS daha genel bir veri-omurga
  desenidir. İkinci kanal omurgası MQTT/UNS olabilir ama NOA'nın özü güvenli ayrımdır.
- **NE107/PA-DIM bağlantısını kaçırmak.** NOA'nın en somut M+O getirisi cihaz sağlığıdır;
  PA-DIM + NE107 olmadan ikinci kanal "ham veri çöplüğüne" döner.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **Tercih:** Brownfield proses tesisleri (kimya, ilaç, petrokimya, su); çekirdek kontrole
  dokunmadan dijitalleşme/analitik/tahminsel bakım; DCS değişiminin riskli/pahalı olduğu
  durumlar; NE107 cihaz sağlığını üst sistemlere taşıma; güvenliğin birinci öncelik olduğu
  veri-açma senaryoları.
- **Etme / gereksiz:** Greenfield tesiste baştan açık bir mimari (UNS/OPC UA) kurmak daha
  doğrudan olabilir; çok küçük sistemlerde ikinci kanal aşırı; gerçek zamanlı kontrol
  ihtiyacı (NOA kontrol katmanı değildir, M+O katmanıdır).
- **Tek başına yetmez:** NOA çerçeveyi verir; somut taşıma (OPC UA/PA-DIM), güvenlik
  (IEC 62443) ve diagnostik içerik (NE107) ayrı yapı taşlarıdır.

## Gerçek Proje Notları

- **NOA'nın asıl satış argümanı "risksiz dijitalleşme"dir.** Proses müşterileri "buluta
  bağlanalım" der ama DCS'e dokunulmasını istemez; NOA tam bu gerilimi çözer — agent bu
  çerçeveyi sunabildiğinde teknik güveni hızla kazanır.
- **Verification of Request, raporlama≠kontrol ilkesinin proses-endüstrisi resmiyetidir.**
  Bu belge tabanında tekrarlanan "yukarıdan gelen istek denetimsiz kontrole yazmaz" ilkesi,
  NOA'da NE 178 olarak standartlaşmıştır; OPC UA/UNS bölümleriyle aynı ilkenin farklı yüzü.
- **NOA, Ethernet-APL ve MTP ile birlikte konumlanır.** Modern saha verisi (APL ile uzun
  mesafe güçlü Ethernet) ve modüler tesis (MTP) yaklaşımları NOA ikinci kanalını besler;
  proses endüstrisi sorularında bu üçlü sıkça birlikte geçer.
- **[DOĞRULANMADI]** NE 175/176/177'nin yayımlandığı, NE 178/179'un geliştirme aşamasında
  olduğu resmi kaynaklarda belirtilir; her NE'nin tam güncel sürüm/durumu proje öncesi
  namur.net'ten teyit edilmeli. NE belgeleri ücretlidir; bu özet resmi duyurular ve otoriter
  ikincil kaynaklara dayanır.

## İlgili Konular

- `01_isa95_hierarchy.md` — NOA'nın "aştığı" otomasyon piramidi; seviyeler ve veri akışı
- `knowledge/standards/03_namur_ne107.md` — İkinci kanalın taşıdığı F/C/S/M cihaz sağlığı
- `knowledge/standards/02_iec62443.md` — NOA güvenlik bölgeleri/ağ geçidinin Zone/Conduit karşılığı
- `03_opcua_companion_specs.md` — PA-DIM: ikinci kanalın tipik OPC UA bilgi modeli
- `knowledge/protocols/opc-ua/03_security.md` — İkinci kanal OPC UA güvenliği (SignAndEncrypt, PKI)
- `02_uns_sparkplug_b.md` — Akraba veri-omurga deseni (UNS); farkları ve kesişimi
