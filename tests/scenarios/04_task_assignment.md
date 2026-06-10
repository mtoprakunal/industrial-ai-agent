# Senaryo 04 — Task Ataması

## Girdi

> "Şu mantıkları CODESYS'te hangi task'lara koymalıyım, cycle time'ları ne olmalı?
> (a) E-Stop ve ışık perdesi izleme, (b) sıcaklık PID döngüsü, (c) hızlı encoder sayımı,
> (d) MQTT ile saatlik üretim raporu yayını, (e) OPC-UA sunucu güncellemesi."

## Bağlam

Her sinyalin gecikme toleransının task seçimini belirlediğini test eder.

## Beklenen Davranış

Her mantığı gecikme toleransına göre eşler (yaklaşık):

- (a) E-Stop / ışık perdesi → Safety task, ≤1 ms, en yüksek öncelik (ayrıca donanımsal —
  bkz. Senaryo 03).
- (b) PID → Task_Control, ~10 ms.
- (c) Encoder/hızlı interlock → Task_Fast, ≤4 ms.
- (d) MQTT rapor → Task_Background / Freewheeling, best-effort (bloke edebilir).
- (e) OPC-UA güncelleme → Task_Comm, ≤500 ms.

Ayrıca: hızlı sinyal yavaş task'a, yavaş kod hızlı task'a konmaz; toplam CPU yükü ≤ %70.

## Geçme Kriteri

- 🔴 E-Stop'u en yüksek öncelik/en hızlı task'a koydu (ve donanımsal olduğunu hatırlattı).
- 🔴 MQTT/raporu Freewheeling/Background'a koydu (bloke I/O).
- PID'i orta hızda (Task_Control ~10 ms) konumlandırdı.
- Encoder'ı hızlı task'a (≤4 ms) koydu.
- OPC-UA'yı haberleşme task'ına (≤500 ms) koydu.
- "Gecikme toleransı → cycle time" ilkesini açıkça ifade etti.

## Dayanak

- `agent/rules.json` → `timing.task_cycle_targets_ms`
- `agent/decision_framework.md` → §2 Task atama tablosu
