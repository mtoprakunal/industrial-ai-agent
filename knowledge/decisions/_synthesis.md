---
KONU        : Kararlar — Sentez
KATEGORİ    : decisions
ALT_KATEGORI: _synthesis
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: ""
    başlık: "İç sentez — decisions/ belgeleri ve agent/decision_framework.md"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "protocol-selection/README.md"
    ilişki: detaylandırır
  - konu: "knowledge/applications/_synthesis.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "agent/decision_framework.md metodolojisi"
ÇELİŞKİLER :
  - kaynak: "Katı eşik kuralı beklentisi"
    konu: "Kararlar eşikle değil gerekçeli akıl yürütmeyle verilir"
    çözüm: >
      'Tag > 100 ise OPC-UA' gibi kural yoktur; her karar gözlemlenebilir bir
      gereksinimden doğar ve KARAR/GEREKÇE/TAKAS ile gerekçelendirilir.
---

## Özün Ne

Bu alan, gerçek mühendislik kararlarının *nasıl* verildiğini örneklerle gösterir:
protokol seçimi, mimari ve HMI teknolojisi. Çekirdek ilke `agent/decision_framework.md`'de;
bu belgeler o metodolojinin somut uygulamasıdır.

## Ortak Karar Disiplini

Her önemli karar üç parçayla sunulur:

```
KARAR:   <ne seçildi>
GEREKÇE: <hangi gözlemlenebilir gereksinimden doğdu>
TAKAS:   <neyi feda ettin / risk>
```

- **Gerekçesiz karar verme.** Tek cümleyle gerekçelendiremiyorsan karar olgunlaşmamıştır.
- **Alternatifi söyle.** "X seçtim; Y de mümkündü, şu koşulda Y daha iyi olurdu."
- **Riski önceden işaretle.** Sorun çıkmadan uyar.

## Karar Eksenleri (özet)

| Karar | Eksenler |
|-------|----------|
| Protokol | Zenginlik↔basitlik / güvenlik / push↔poll; kaç alıcı, hangi yön |
| Mimari | Tek/dağıtık PLC, kontrol nerede, veri akış yönü, segmentasyon |
| HMI | Kim/nereden erişecek, ekip teknolojisi, sertifikasyon, köprü protokol |

## Nasıl Kullanılmalı

İlgili karar belgesini oku → eksenleri kendi gereksinimine uygula → KARAR/GEREKÇE/TAKAS
ile kaydet → `project_report.md`'nin "Kararlar" bölümüne taşı.

## İlgili Konular

- `protocol-selection/`, `architecture/`, `hmi-technology/`
- `agent/decision_framework.md` — metodoloji
- `knowledge/examples/case-studies/` — kararların gerçek makinelerdeki uygulaması
