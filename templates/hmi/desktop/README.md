# Masaüstü HMI Şablonları

Python ve .NET tabanlı, çalışan masaüstü HMI başlangıç şablonları. Üçü de
`EXAMPLE_conveyor` CODESYS PLC'sine **doğrudan** (gateway yok) OPC-UA ile bağlanır
ve aynı `GVL_HMI` tag setini kullanır: `aZoneState[1..3]`, `aZoneSpeed[1..3]`,
`aZoneAuto`, `xEStopActive`, `xRunPermit`, `xZone2Itlk`, `xAnyAlarm`, alarm
bayrakları (`aZoneJam`/`aZoneSpdFlt`/`aZoneTacBrk`), komutlar `axCmdAutoRun[1..3]`
ve `xCmdReset`, watchdog `uHeartbeat`.

| Şablon | Stack | Veri yöntemi | Notlar |
|---|---|---|---|
| [`python-pyqt-opcua/`](python-pyqt-opcua/) | PyQt6 + asyncua + qasync | Subscription (tek event loop) | Zengin UI, real-time; üretim odaklı |
| [`python-tkinter/`](python-tkinter/) | Tkinter (stdlib) + asyncua.sync | Polling (ayrı thread + after()) | Hafif, minimum bağımlılık |
| [`dotnet-wpf-opcua/`](dotnet-wpf-opcua/) | WPF (.NET 8) + OPC Foundation SDK | Subscription + MonitoredItem (MVVM) | Kurumsal Windows, OPC Foundation stack |

Ortak tasarım ilkeleri (knowledge/hmi):

- **Namespace index sabit yazılmaz** — bağlantıda namespace URI'den alınır.
- **GUI thread'inde ağ IO yapılmaz** — async/await (PyQt, WPF) veya ayrı worker
  thread (Tkinter) + thread-safe veri aktarımı.
- **ISA-101 renk kuralları** (durağan=gri, çalışıyor=yeşil, arıza=kırmızı).
- **ISA-18.2 alarm mantığı** — Acknowledge ≠ Resolved.
- **Heartbeat watchdog** — `uHeartbeat` durunca "VERİ BAYAT" + yazma kilidi.
- **Güvenlik** — şablonlar geliştirme için anonymous/güvenliksiz başlar; her
  README'de üretim için sertifika + SignAndEncrypt adımları açıklanır.

Her şablonun kurulum, çalıştırma, PLC konfigürasyonu ve güvenlik detayı kendi
`README.md` dosyasındadır.
