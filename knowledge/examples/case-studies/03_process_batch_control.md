---
KONU        : Vaka Çalışması — Proses/Batch Kontrol (Dozajlama + Tartım Tankı)
KATEGORİ    : examples
ALT_KATEGORI: case-studies
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://www.isa.org/standards-and-publications/isa-standards/isa-88-standards"
    başlık: "ISA-88 (IEC 61512) Batch Control Series — ISA resmi"
    güvenilirlik: resmi
  - url: "https://www.plcacademy.com/isa-88-s88-batch-control-explained/"
    başlık: "ISA-88 (S88) Batch Control Explained — PLC Academy"
    güvenilirlik: topluluk
  - url: "https://sgsystemsglobal.com/glossary/isa-88-phases-equipment-modules/"
    başlık: "ISA-88 Phases & Equipment Modules — SG Systems Global"
    güvenilirlik: topluluk
  - url: "https://content.helpme-codesys.com/en/libs/Util/Current/Controller/PID.html"
    başlık: "CODESYS Util Library — PID Function Block (resmi)"
    güvenilirlik: resmi
  - url: "https://www.penko.com/globalassets/penko/documents/support-articles/how-to-use-the-pdi-protocol-to-read-or-write-the-parameter-in-the-pdi-tree-with-modbus.pdf"
    başlık: "PENKO — PDI protokolünü Modbus ile kullanma (parametre okuma/yazma)"
    güvenilirlik: resmi
  - url: "knowledge/applications/tank-level/README.md"
    başlık: "Tank Seviye Kontrolü — İç Bilgi Tabanı (PID, lead/lag, NAMUR)"
    güvenilirlik: deneyimsel
  - url: "devices/PENKO_SGM820/wiring_notes.md"
    başlık: "PENKO SGM820 — tartım transmitteri kablolama/entegrasyon notları"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/applications/tank-level/README.md"
    ilişki: detaylandırır
  - konu: "knowledge/standards/03_namur_ne107.md"
    ilişki: kullanır
  - konu: "knowledge/protocols/modbus-tcp/_synthesis.md"
    ilişki: kullanır
  - konu: "devices/PENKO_SGM820"
    ilişki: kullanır
ÖNKOŞUL     :
  - "PID ve ON-OFF/histerezis kavramı (applications/tank-level/README.md)"
  - "NAMUR NE107 sensör diagnostiği (standards/03_namur_ne107.md)"
  - "Analog 4–20 mA ve load cell mV/V temel bilgisi"
ÇELİŞKİLER :
  - kaynak: "Tartım = kontrol mü, raporlama mı?"
    konu: "Dozaj kesme kararı ağ üzerinden okunan ağırlığa mı dayanmalı?"
    çözüm: >
      Hayır. Ağ üzerinden gelen ağırlık best-effort raporlamadır. Hassas/hızlı
      dozaj kesme, cihaz-içi setpoint çıkışına (PENKO 4 programlanabilir setpoint)
      veya yerel hızlı karşılaştırmaya dayanmalı; ağ gecikmesine güvenilmez
      (bkz. PENKO_SGM820 wiring_notes — 'best-effort raporlama').
---

## Özün Ne

Proses/batch kontrol vakası, bir tankta tarifeye (recipe) göre malzeme **dozajlayan,
karıştıran, ısıtan ve boşaltan** bir sistemi kapsar. Sürekli (continuous) prosesten farkı,
işin **partiler (batch) halinde, adım adım reçeteyle** yürütülmesidir. Mühendislik özü iki
şeydir: (1) miktarı doğru ölçmek (tartım / debimetre), (2) reçete adımlarını güvenli ve
tekrarlanabilir şekilde sıralamak. ISA-88 (IEC 61512) bu sıralamayı **recipe → unit
procedure → operation → phase** hiyerarşisiyle, ekipmanı ise **equipment module →
control module** ile modeller (kaynak: ISA, PLC Academy).

Neden önemli: Dozajlamada hata doğrudan ürün kalitesi ve maliyettir. Tartım verisi nereden
okunacak, kesme kararı nerede verilecek, reçete nasıl saklanacak — bunlar yanlış kurgulanırsa
ya doğruluk ya tekrarlanabilirlik kaybolur. Bu vaka PENKO tartım dijitizer (SGM820) ile
CODESYS PID/sıralama mantığını birleştirir.

## Nasıl Çalışır

ISA-88 kavramlarının bu tanka eşlenmesi:

- **Control Module (CM):** En küçük kontrol edilebilir öğe — bir vana, bir pompa, bir
  load cell/tartım kanalı, bir karıştırıcı sürücüsü. (kaynak: Industrial Monitor Direct, SG)
- **Equipment Module (EM):** CM kümesini bir yetenek için koordine eder — "Dozaj EM"
  (besleme vanası + tartım + kesme), "Isıtma EM" (ısıtıcı + sıcaklık PID).
- **Phase:** Tanımlı başı/sonu olan adım — `Dose(ingredient, target_kg)`, `HeatTo(°C)`,
  `Hold(t)`, `Agitate`, `Transfer`, `CIP`. Phase'ler EM'leri çağırır.
- **Recipe / Unit Procedure:** Phase'lerin sıralı/şartlı dizisi (kaynak: PLC Academy).
- **Tartım katmanı (PENKO SGM820):** Load cell mV/V sinyalini dijitalleştirir (8 load cell,
  1600/s'e kadar örnekleme), ağırlığı Modbus TCP / Ethernet-IP ile sunar; **4 programlanabilir
  setpoint çıkışı** ile cihaz-içi hızlı kesme yapabilir (kaynak: PENKO datasheet/wiring_notes).
- **Dozaj mantığı:** Kaba/ince dozaj (coarse/fine) — hedefe kadar kaba akış, eşiğe yaklaşınca
  ince akış, "in-flight" (kapatma anından sonra düşen malzeme) telafisiyle kesme.

## Pratikte Nasıl Kullanılır

**Gereksinim listesi (girdi):**
1. Reçeteye göre 2–4 bileşen dozajlama, hedef ±tolerans (kg).
2. Tartım: load cell tank veya akış toplamı; in-flight telafili kesme.
3. Sıcaklık kontrolü (PID, ≥1 bölge) ve karıştırma.
4. Reçete saklama/seçme; batch raporu (lot, miktar, sapma, zaman).
5. Sensör diagnostiği (NAMUR NE107) ve güvenli durum (vana kapalı).
6. Üst sistem (MES/SCADA) ile reçete indirme + batch raporu yükleme.

**Mimari karar (KARAR/GEREKÇE/TAKAS):**

```
KARAR:   Reçete sıralaması ve PID PLC'de (CODESYS SFC + Util.PID); tartım PENKO SGM820'de,
         hızlı dozaj kesme cihaz-içi setpoint çıkışıyla.
GEREKÇE: Kesme kararı ağ gecikmesine duyarlı olmamalı (decision_framework §1, ilke 3:
         raporlama ≠ kontrol). SGM820'nin yüksek örnekleme + 4 setpoint çıkışı bunu
         yerelde çözer; PLC reçete/koordinasyonu yürütür.
ALT:     Ağırlığı PLC'de okuyup PLC'de kesmek; ağ jitter'ı in-flight telafisini bozar,
         hassas dozajda fire artar → cihaz-içi kesme tercih edildi.
TAKAS:   Setpoint parametreleri iki yerde (cihaz + PLC reçete) tutuluyor; senkron tutma
         disiplini gerekir. Kabul edilir çünkü doğruluk kritik.
```

```
KARAR:   Protokol: Tartım = Modbus TCP (SGM820 slave); MES/SCADA reçete+rapor = OPC-UA;
         analog enstrümanlar = 4–20 mA (NAMUR NE43 arıza eşikleriyle).
GEREKÇE: decision_framework §1: basit register/ağırlık → Modbus; zengin reçete+batch
         raporu (struct, zaman damgası, lot) → OPC-UA. PENKO parametre erişimi PDI-over-Modbus.
ALT:     Tartımı Ethernet/IP ile almak (SGM820 destekler); tesis Modbus standardındaysa
         Modbus daha taşınabilir. Tercih tesis altyapısına göre.
TAKAS:   Modbus'ta güvenlik yok → OT segmentasyonu zorunlu. PENKO register/PDI adresleri
         resmi dokümandan alınmalı [DOĞRULANMADI — burada adres uydurulmadı].
```

**Task / protokol / HMI eşlemesi:**

| Mantık | Task | Cycle | Protokol/Arayüz |
|--------|------|-------|------------------|
| E-stop, taşma/yüksek-seviye emniyeti | Donanımsal emniyet + Safety task | ≤1 ms | Donanım + bağımsız seviye şalteri |
| Hızlı dozaj kesme | PENKO cihaz-içi setpoint | cihaz hızı | DO (cihaz) |
| Reçete SFC, PID, in-flight telafi | Task_Control | 10–20 ms | Analog I/O + Modbus okuma |
| Tartım okuma (raporlama) | Task_Comm | ≤200 ms | Modbus TCP master |
| Sensör NE107 diagnostiği | Task_Control | 20 ms | 4–20 mA / NAMUR |
| MES reçete indir / batch rapor | Task_Comm | ≤500 ms | OPC-UA |
| Batch log → historian/bulut | Task_Background (Freewheeling) | best-effort | OPC-UA / MQTT |

## Örnekler

- **Kaba/ince dozaj (phase Dose):** SFC adımları: `Aç_kaba → (ağırlık ≥ hedef−ince_eşik)
  → Aç_ince → (cihaz setpoint kesme) → Bekle_durulma → Oku_son_ağırlık → Sapma_kaydet`.
  Kesmeyi cihaz yapar; PLC sadece sırayı ve telafiyi yönetir.
- **In-flight telafi:** Kapatma komutundan sonra havada/borudaki malzeme tankı doldurmaya
  devam eder. Setpoint = hedef − öğrenilen in-flight. Sistem her batch'te gerçek-hedef
  farkından in-flight'ı günceller (adaptif).
- **NE107 güvenli durum:** Load cell/transmitter "arıza" durumu (NE107 Failure) verirse dozaj
  phase'i durur, besleme vanası kapanır, alarm; tahmini ağırlıkla devam EDİLMEZ.

## Sık Yapılan Hatalar

- **Dozaj kesmeyi ağ üzerinden okunan ağırlığa bağlamak.** Ağ jitter'ı + poll periyodu
  in-flight'ı belirsizleştirir, doz şişer. Kesme cihaz-içi/yerel olmalı (PENKO setpoint).
- **In-flight telafisini ihmal etmek.** Komut anında değil, malzeme durunca tartılır;
  telafi yoksa her doz hedefi aşar.
- **Tartım filtre/yenileme hızını yanlış ayarlamak.** Çok hızlı = gürültülü okuma (yanlış
  erken kesme); çok yavaş = geç kesme. Karıştırıcı titreşimi de okumayı bozar — dozaj
  sırasında karıştırıcı durdurma sık çözümdür.
- **Reçeteyi koda gömmek.** Yeni ürün = kod değişikliği olursa sistem sürdürülemez. Reçete
  veri olarak (CODESYS recipe / MES) tutulur; SFC sabit kalır (ISA-88 ruhu).
- **Taşma korumasını PID'e/PLC'ye bırakmak.** Yüksek-yüksek seviye, PLC'den bağımsız bir
  emniyet şalteri + donanımsal kesme olmalı; yazılım tek hat olamaz (decision_framework §4).

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **PENKO + cihaz-içi kesme + PLC SFC tercih:** Hassas gravimetrik dozaj, sertifikalı/yasal
  tartım, çok bileşenli reçete, MES'e batch raporu gereken tesislerde.
- **Etmemeli:** Hassasiyet kritik olmayan, debimetreyle hacimsel basit dolumda load cell
  + cihaz-içi kesme aşırı olabilir; basit totalizer + vana yeterlidir.
- **ISA-88 tam yapısı:** Çok ürünlü, denetlenen (gıda/ilaç) tesiste değer üretir; tek
  ürünlü basit makinede tam S88 modeli gereksiz ağırlık olabilir — kavramları ölçekle uygula.

## Gerçek Proje Notları

- "Doz hep aşıyor" şikâyetinin %1 numaralı nedeni in-flight telafisinin eksik/yanlış
  öğrenilmesidir, tartım donanımı değil. Önce kesme→durulma penceresi loglanır.
- Karıştırıcı/pompa titreşimi tartımı bozar; hassas okuma anında karıştırıcıyı durdurmak
  veya dijital filtre + sakinleşme (stability) bekleme şarttır.
- PENKO PDI-over-Modbus ile parametre okuma güçlüdür ama register/PDI indeksi resmi
  dokümandan gelir; tahmini adresle entegrasyon sessizce yanlış değer okutur [DOĞRULANMADI].
- Batch izlenebilirliği (lot, miktar, sapma, zaman, operatör) raporlama katmanındadır;
  bunu kontrol döngüsüne karıştırmak (her batch'te dosya yazma vb.) kontrol task'ını
  bloke edebilir → Freewheeling/Comm task (decision_framework §2).

## İlgili Konular

- `knowledge/applications/tank-level/README.md` — PID, lead/lag, seviye sensörleri (taban)
- `knowledge/standards/03_namur_ne107.md` — sensör diagnostiği ve güvenli durum
- `devices/PENKO_SGM820/wiring_notes.md` — tartım transmitteri entegrasyonu
- `knowledge/protocols/modbus-tcp/_synthesis.md` — tartım okuma protokolü
- `knowledge/examples/case-studies/01_packaging_machine.md` — recipe yönetimi paralelliği
