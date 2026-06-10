# Proje Üretim Oyun Kitabı (Playbook)

Bir `project_spec.json` veya proje talebi geldiğinde bu 8 adımı sırayla izle. **Önce tasarla, sonra kodla.** Her adım: *oku → karar ver → üret → doğrula.* Hiçbir adımı atlama; eksik bilgi varsa o adımda dur ve sor (`interaction_guide.md`).

---

## ADIM 1 — Gereksinim Analizi

**Amaç:** Üretime başlamadan önce belirsizliği sıfırla. Yanlış varsayımla üretilen kusursuz proje yine yanlıştır.

### Zorunlu bilgiler (yoksa SOR)
- Uygulama tipi ve fonksiyonel gereksinimler (ne yapacak?)
- Platform (CODESYS / hedef donanım)
- I/O sayıları (DI / DO / AI / AO)
- İletişim protokolü ihtiyacı (kaç istemci, hangi yön, güvenlik)
- HMI tipi ve teknoloji tercihi
- Emniyet gereksinimleri — **burada asla varsayım yapma**

### Opsiyonel bilgiler (yoksa makul varsay + işaretle)
- Cycle time tercihleri (yoksa `rules.json` timing'den türet)
- İsimlendirme alan kodları (yoksa standart uygula)
- Üretim formatı (yoksa varsayılan: ST kaynak)

### Eksik bilgiyle ilerleme
- Kararı değiştiren eksik → SOR (tek seferde, grupla).
- Kararı değiştirmeyen eksik → makul varsay, **"X varsaydım, farklıysa söyle"** diye işaretle.

### Çıktı
Fonksiyonel gereksinim listesi (madde madde), her maddenin hangi I/O + task + alarm'a haritalandığı zihinsel harita. Uygulama tipini `/knowledge/applications/{tip}/` ile eşle ve oku.

---

## ADIM 2 — Mimari Karar

**Amaç:** Tüm üretimi yönlendiren üst-seviye kararları gerekçeleriyle ver.

1. **Platform** — hedef donanım, CODESYS runtime tipi.
2. **Protokol** — `decision_framework.md` §1. `/knowledge/protocols/_synthesis.md` oku. Ekseni belirle, ilkeyi planla.
3. **HMI teknolojisi** — `decision_framework.md` §3.
4. **Mimari** — tek/dağıtık PLC, veri akış yönleri, segmentasyon (`decision_framework.md` §4).

### Çıktı
Her karar KARAR / GEREKÇE / ALT / TAKAS formatında. Bu blok `project_report.md`'nin çekirdeğidir.

---

## ADIM 3 — Donanım Konfigürasyonu

**Amaç:** Fiziksel dünya ile yazılımın buluştuğu katmanı netleştir — kod yazmadan önce.

1. **I/O listesi çıkar** — her sinyal: tag, tip (BOOL/INT/REAL), yön (DI/DO/AI/AO), açıklama, ölçek (analog için 4-20mA → eng. unit).
2. **Adres haritası oluştur** — %I/%Q/%M atamaları; çakışma yok.
3. **Cihaz konfigürasyonu** — fieldbus (EtherCAT/Modbus) slave'leri, offset'ler.
4. İsimlendirme `rules.json`: `{Area}_{DeviceType}_{Number}_{Signal}`, ≤24 karakter.

### Çıktı
`io_list.csv` taslağı (GVL ile senkron tutulacak), `hardware_config/`.

---

## ADIM 4 — Task Yapısı

**Amaç:** Hangi mantığın hangi task'ta, hangi hızda çalışacağını belirle.

1. **Mantık → task ataması** — `decision_framework.md` §2 tablosu.
2. **Cycle time hesabı** — gecikme toleransına göre; exec time < cycle time olmalı.
3. **Öncelik sıralaması** — emniyet en yüksek, telemetri en düşük; EtherCAT bus task prio ≤5.
4. **Bloke-I/O ayrımı** — connect/MQTT/dosya → Freewheeling task.

### Doğrulama
- Toplam CPU yükü hedefi ≤ %70.
- Hiçbir bloke çağrı kontrol task'ında değil.

### Çıktı
Task tablosu: tip, cycle, öncelik, **neden** (her satır gerekçeli).

---

## ADIM 5 — Yazılım Mimarisi

**Amaç:** Kod yazmadan önce yapıyı kur. Referans: `/knowledge/codesys/programming/`.

1. **GVL yapısı** — global değişkenler, I/O listesiyle birebir. Tek-yazar disiplini.
2. **FB hiyerarşisi** — her FB tek sorumluluk. Cihazın tüm yaşam döngüsü (init/run/fault/stop) bir FB'de; alt işlevler (ölçekleme, PID) ayrı küçük FB/Function'larda.
3. **Kütüphane seçimi** — standart kütüphaneler + versiyon notu (devir sorunlarını önlemek için).
4. **Durum makineleri** — CASE tabanlı, açık.

### Çıktı
GVL şeması, FB ağacı, kütüphane listesi (versiyonlu).

---

## ADIM 6 — Kod Üretimi

**Amaç:** Tasarımı koda dök. Referans: `/knowledge/codesys/`, `/knowledge/hmi/`.

1. **PLC kodu** — ST. Sihirli sayı yok (sabit kullan). Her FB açıklamalı. Hata yönetimi açık. Pointer'ları her scan yeniden hesapla. REAL bölmede NaN/sıfır kontrolü.
2. **Ağ konfigürasyonu** — OPC-UA server (Symbol Config + güvenlik modu) / Modbus slave (register haritası) / MQTT (topic + LWT). Adres haritası `io_list.csv` ile birebir.
3. **HMI kodu** — seçilen teknolojide. Köprü protokol. Tüm kritik sinyaller + bağlantı kopması senaryosu + alarm onayı.

### Üretim formatı (kullanıcı tercihi)
- **Script Engine** — `templates/codesys/project-scripts/`
- **PLCopen XML** — `templates/codesys/plcopen-xml/`
- **ST kaynak** — `templates/codesys/st-snippets/` (varsayılan, en taşınabilir)

---

## ADIM 7 — Doğrulama

**Amaç:** Teslimden önce her şeyi makineye kurmadan yakala.

- **Adres çakışması** — aynı %Q/%I iki yerde mi? GVL'de ara.
- **Timing** — her task exec < cycle; toplam yük ≤ %70; bloke çağrı kontrol task'ında değil.
- **Safety** — emniyet I/O standart modülde değil; fail-safe = stop; watchdog açık; `safety_principles.md` sorusu.
- **İsimlendirme** — format + ≤24 karakter + GVL/io_list/HMI/ağ tutarlılığı.
- **Tek-yazar** — her register/node/topic tek yazar.

`quality_checklist.md` üzerinden tam liste.

---

## ADIM 8 — Dokümantasyon

**Amaç:** Projeyi devredilebilir ve bakılabilir kıl.

1. **`io_list.csv`** — tüm I/O, adres, tag, tip, açıklama.
2. **`alarm_list.csv`** — alarm, seviye, sebep, çözüm.
3. **`project_report.md`** — tasarım özeti, kararlar (KARAR/GEREKÇE/TAKAS), kullanılan bilgi tabanı belgeleri.
4. **Risk değerlendirmesi** — bilinen riskler, varsayımlar (işaretli), öneriler.

### Teslim
`quality_checklist.md`'yi tamamla. Eksik kalan maddeyi gizleme — **söyle.** Riskleri ve önerileri açıkça sun. Üretilen yeni bilgi varsa bilgi tabanına eklemeyi öner.
