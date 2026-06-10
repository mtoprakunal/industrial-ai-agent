---
KONU        : Örnekler ve Öğrenme Kaynakları — Üst Sentez
KATEGORİ    : examples
ALT_KATEGORI: _synthesis
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://forge.codesys.com/prj/"
    başlık: "CODESYS Forge — açık kaynak topluluk projeleri"
    güvenilirlik: resmi
  - url: "https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95"
    başlık: "ISA-95 standardı"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "open-source/01_oscat_library.md"
    ilişki: detaylandırır
  - konu: "case-studies/01_packaging_machine.md"
    ilişki: detaylandırır
  - konu: "knowledge/decisions/architecture/README.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "Temel CODESYS ve protokol bilgisi (knowledge/codesys/, knowledge/protocols/)"
ÇELİŞKİLER :
  - kaynak: "Örnek = kopyala-yapıştır beklentisi"
    konu: "Örnek projeler hazır çözüm değil, pattern ve karar kaynağıdır"
    çözüm: >
      Bu alandaki kayıtlar üçüncü taraf kodu barındırmaz; her biri resmi kaynağa
      yönlendiren, mimari/pattern/ders çıkaran özetlerdir. Kodun kendisi resmi
      kaynaktan (lisansına uyularak) alınır.
---

## Özün Ne

Bu alan (`knowledge/examples/`), agent'ın **başkalarının işinden öğrenmesi** için
kurulmuştur. Dört farklı öğrenme kaynağını kaynaklı özetlere dönüştürür:

1. **Açık kaynak** (`open-source/`) — OSCAT, CODESYS Forge/Store, GitHub IEC 61131-3
   projeleri. Yeniden kullanılabilir FB'ler, kod organizasyonu, test/CI dersleri.
2. **Vendor uygulama notları** (`vendor-app-notes/`) — CODESYS, Beckhoff TwinCAT,
   Inovance AM600 resmi örnekleri. Üreticinin "doğru yol" dediği pattern'ler.
3. **Sektör vaka çalışmaları** (`case-studies/`) — paketleme, malzeme taşıma, batch
   proses, senkron motion. Gereksinim → mimari → protokol eşlemesi (KARAR/GEREKÇE/TAKAS).
4. **Referans mimariler** (`reference-arch/`) — ISA-95, UNS/Sparkplug B, OPC-UA
   Companion Specs, NAMUR NOA. Sistem-seviyesi tasarım çerçeveleri.

Önemli ilke: **örnek = kopyalanacak kod değil, çıkarılacak karar/pattern.** Kayıtlar kod
barındırmaz; resmi kaynağa yönlendirir ve "ne öğretir, hangi tuzağı gösterir" sorusunu
yanıtlar.

## Bu Alan Mevcut Bilgi Tabanını Nasıl Besler

- **Karar çerçevesi:** Vaka çalışmaları `agent/decision_framework.md`'nin somut
  uygulamasıdır — protokol/task/HMI kararlarını gerçek makinelerde gösterir.
- **CODESYS/InoProShop:** Açık kaynak ve vendor örnekleri `knowledge/codesys/` ve
  `knowledge/inovance/` bilgisini pratik pattern'lerle pekiştirir.
- **Protokoller/standartlar:** Referans mimariler `knowledge/protocols/` ve
  `knowledge/standards/` üzerine sistem-seviyesi bağlam ekler (örn. UNS ↔ MQTT,
  NOA ↔ "raporlama ≠ kontrol").
- **Cihazlar:** Vakalar `devices/` kütüphanesindeki gerçek cihazlara (PENKO SGM820,
  Inovance AM600/SV660N) bağlanır.

## Nasıl Kullanılmalı

- Yeni bir proje tasarlarken: ilgili **vaka çalışmasını** oku → mimari iskeleti al →
  `decision_framework` ile kendi gereksinimine uyarla.
- Kod yazarken: **açık kaynak** kayıtlarındaki kütüphane/pattern'leri değerlendir
  (lisansa dikkat).
- Entegrasyon/IT-OT tasarımında: **referans mimarileri** çerçeve olarak kullan.

## Dürüstlük Notu

Tüm kayıtlar "Orta" seviyededir: kaynaklı ve pratik, ancak her teknik ayrıntı derin
gerçek-proje doğrulamasından geçmemiştir. Doğrulanamayan noktalar ilgili belgelerde
`[DOĞRULANMADI]` ile işaretlenmiştir. Üçüncü taraf kod/metin kopyalanmamış; yalnızca
olgu, pattern ve ders özetlenmiştir.

## İlgili Konular

- `_resources.md` — dış öğrenme kaynakları indeksi (linkler)
- `knowledge/decisions/`, `knowledge/applications/` — karar ve uygulama bilgisi
- `agent/decision_framework.md` — vaka çalışmalarının dayandığı metodoloji
