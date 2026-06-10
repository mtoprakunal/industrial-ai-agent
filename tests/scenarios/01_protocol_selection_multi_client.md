# Senaryo 01 — Protokol Seçimi (Çok İstemci)

## Girdi

> "Bir paketleme hattı yapıyorum. PLC'den çıkan üretim verisini aynı anda SCADA, bir
> historian veritabanı ve bulut tarafındaki bir analitik panosu okuyacak. Ayrıca SCADA'dan
> setpoint yazılabilmeli. Hangi haberleşme protokolünü kullanmalıyım?"

## Bağlam

Çok-alıcı (fan-out) + telemetri + tek noktadan setpoint yazma karışımı. Tek "doğru"
protokol yok; eksen analizi ve muhtemelen **kombinasyon** beklenir.

## Beklenen Davranış

- Önce `/knowledge/protocols/_synthesis.md`'e başvurduğunu belli eder.
- Üç ekseni (zenginlik / güvenlik / push-poll) kullanarak akıl yürütür.
- N alıcı + telemetri yayını için **MQTT** (broker push) eğilimini, setpoint/kontrol için
  **OPC-UA** (subscription + güvenli yazma) eğilimini ayırır → kombinasyon önerir.
- Kararı KARAR / GEREKÇE / TAKAS üçlüsüyle sunar.
- Alternatifi ve hangi koşulda tercih edileceğini söyler.

## Geçme Kriteri

- 🔴 KARAR/GEREKÇE/TAKAS formatı kullanıldı.
- 🔴 "Tek doğru protokol" dayatmadı; gereksinime göre akıl yürüttü (rigid eşik yok).
- N alıcı/fan-out gözlemini push-poll eksenine bağladı (MQTT eğilimi).
- Kontrol/telemetri ayrımını yaptı (raporlama ≠ kontrol).
- Tek-yazar ilkesine (setpoint'in tek yazarı) değindi.
- Güvenliği gündeme getirdi (OPC-UA PKI / MQTT TLS / Modbus internet'e açılmaz).

## Dayanak

- `agent/rules.json` → `protocol_selection` (axes, common_principles, never_use_rigid_rules)
- `agent/decision_framework.md` → §1 Protokol Seçimi
- `agent/system_prompt.md` → §3 Karar Verme Felsefen
