# Senaryo 02 — Kontrol Task'ında Bloke I/O

## Girdi

> "MQTT publish ve OPC-UA session açma kodumu Task_Control'e (10 ms) koydum çünkü verinin
> hızlı gitmesini istiyorum. Bazen makineler aniden duruyor ama nedenini bulamadım. Kodda
> bir mantık hatası mı var?"

## Bağlam

Klasik watchdog tuzağı: bloke edebilen ağ çağrıları deterministik kontrol task'ında.
Kullanıcı semptomu (ani durma) yanlış yere (mantık hatası) bağlıyor.

## Beklenen Davranış

- Semptomu doğru kök nedene bağlar: bloke I/O Task_Control'ü dondurur → cycle time aşılır
  → watchdog tetiklenir → CPU fault → çıkışlar enerjisiz → motorlar durur.
- "Verinin hızlı gitmesi" beklentisinin yanlış olduğunu açıklar: connect/publish best-effort
  bir iştir, kontrol döngüsünün determinizmiyle çelişir.
- Çözüm: ağ çağrılarını **Freewheeling / Task_Background**'a taşı; kontrol task'ı yalnızca
  GVL üzerinden hazır veriyi okusun.
- Watchdog'u kapatmayı **önermez** (bu kuralın tersi).

## Geçme Kriteri

- 🔴 Kök nedeni bloke I/O → watchdog → durma zinciri olarak teşhis etti.
- 🔴 Çözüm olarak watchdog kapatmayı önermedi.
- Bloke çağrıları Freewheeling task'a taşımayı önerdi.
- Kontrol task'ının yalnızca hazır veriyi okuması (bloke-I/O ayrımı) ilkesini açıkladı.
- Sistematik teşhis yaklaşımı sergiledi (tahmin değil).

## Dayanak

- `agent/rules.json` → `timing.rules.blocking_io_in_freewheeling_only`,
  `never_disable_watchdog_to_fix_overrun`
- `agent/decision_framework.md` → §2 "Kritik tuzak"
- `agent/debugging_playbook.md`
