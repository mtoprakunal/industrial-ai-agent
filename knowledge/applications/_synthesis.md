---
KONU        : Uygulamalar — Sentez
KATEGORİ    : applications
ALT_KATEGORI: _synthesis
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: ""
    başlık: "İç sentez — applications/ belgeleri ve agent/decision_framework.md"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "conveyor/README.md"
    ilişki: detaylandırır
  - konu: "knowledge/examples/case-studies/01_packaging_machine.md"
    ilişki: tamamlar
  - konu: "knowledge/decisions/_synthesis.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "Temel CODESYS, protokol ve task yapısı bilgisi"
ÇELİŞKİLER :
  - kaynak: "Uygulama şablonu = hazır çözüm beklentisi"
    konu: "Uygulama bilgisi reçete değil, ortak pattern kaynağıdır"
    çözüm: >
      Her gerçek makine kendi gereksinimini dayatır; bu belgeler ortak iskeleti
      verir, agent/decision_framework.md ile somut projeye uyarlanır.
---

## Özün Ne

Bu alan, sık karşılaşılan uygulama tiplerinin (konveyör, tank seviye, motor kontrol,
paketleme) ortak mühendislik kalıplarını toplar. Amaç: yeni bir projede sıfırdan
başlamamak — benzer makinenin kanıtlanmış iskeletini almak ve gereksinime uyarlamak.

## Ortak Kalıplar (uygulamalar arası)

- **Durum makinesi merkezlidir.** Konveyör bölgesi, dolum sekansı, motor çalıştırma —
  hepsi açık CASE/SFC durum makineleriyle modellenir (bkz. `codesys/advanced/02_state_machines_sfc.md`).
- **Tek-yazar disiplini.** Her çıkış/register tek bir POU tarafından yazılır.
- **Emniyet donanımsaldır.** E-stop, ışık perdesi, taşma koruması yazılım mantığına
  bırakılmaz (bkz. `knowledge/safety/`).
- **Raporlama ≠ kontrol.** Hızlı interlock PLC'de; HMI/MES'e veri OPC-UA/Modbus ile çıkar.
- **Ölçekleme ve NAMUR.** Analog girişler 4-20mA ölçeklenir, kablo kopması (NE107) izlenir.

## Uygulama → Tipik Mimari Eşlemesi

| Uygulama | Kritik eksen | Tipik protokol | Task vurgusu |
|----------|--------------|----------------|--------------|
| Konveyör | Bölge interlock, sıralama | OPC-UA / Modbus | Fast + Control |
| Tank seviye | Analog PID, tartım | OPC-UA + cihaz-içi hızlı kesme | Control |
| Motor kontrol | VFD/servo komutu | Modbus RTU / EtherCAT | Fast / Motion |
| Paketleme | Senkron motion | EtherCAT (motion) + OPC-UA (HMI) | Motion + Control |

## Nasıl Kullanılmalı

İlgili uygulama belgesini oku → ortak kalıbı al → `agent/decision_framework.md` ile
protokol/task/HMI kararını kendi gereksinimine göre ver → `examples/case-studies/`
ile gerçek vaka derinliğine in.

## İlgili Konular

- `conveyor/`, `tank-level/`, `motor-control/`, `packaging/`
- `knowledge/examples/case-studies/` — gerçek vaka çalışmaları
- `agent/decision_framework.md` — karar metodolojisi
