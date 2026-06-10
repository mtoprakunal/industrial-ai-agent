# Arıza Giderme Oyun Kitabı (Debugging Playbook)

Sistematik debug kılavuzu. Her arıza şu zincirle çözülür:
**Semptom → Katman → Olası sebepler → Test adımları → Kök neden → Çözüm → Doğrulama.**

Derin teknik detay `/knowledge/codesys/debugging/` (01_common_errors, 02_debugging_tools, 03_performance_analysis) altındadır. Bu playbook hızlı triage ve yönlendirme katmanıdır.

---

## Altın Kurallar

1. **Önce daralt, sonra derinleş.** Forum araması 4. adıma kadar yapılmaz.
2. **CODESYS'te her sorunun ilk durağı Log sayfasıdır** (Device → Log sekmesi). Ekrandaki mesaj *özet*, Log'daki mesaj *tanıdır*.
3. **Önce hangi katman?** — yanlış katmanda saatlerce debug yapma:
   - **Altyapı** (runtime/OS/ağ): Login, gateway, versiyon, device description
   - **Yapı/config**: RETAIN, library, I/O mapping, adres çakışması
   - **Kod/logic**: watchdog, pointer crash, NaN, yanlış I/O değeri
4. **En basit açıklamadan başla** (Occam). 3 saatlik debug çoğu zaman 30 saniyelik fiziksel kontrolle biter (kablo, port, LED).
5. **Watchdog'u kapatarak "çözme"** — watchdog bir hata değil, tanı sinyalidir. Kapatmak sorunu maskeler.
6. **Varsayma, sor/ölç.** "Garip davranış" çoğu zaman versiyon uyumsuzluğu veya bozuk bootapp'tir.

### Genel Triage Akışı
```
Hata görüldü
    ▼
Log sayfasını aç → kategori belirle
    ├── Login/bağlantı  → gateway, ağ, runtime servisi (ALTYAPI)
    ├── Download        → Log'dan Exception tipini oku (YAPI/KOD)
    ├── Build/compile   → derleme çıktısı: dosya + satır (YAPI)
    ├── Watchdog        → hangi task, exec time neden uzun (KOD)
    ├── Fieldbus        → EtherCAT/Modbus diagnostics + fiziksel (ALTYAPI)
    └── Değer yanlış    → I/O mapping + fiziksel bağlantı (YAPI/ALTYAPI)
Bulamazsan: Log'u temizle → tekrar dene → oku  /  runtime restart
```

---

## 1. CODESYS Runtime / Bağlantı Sorunları

**Semptom:** "Cannot connect to device", "Login failed", "Gateway connection failed", device tarama listesi boş.

**Katman:** Altyapı.

**Olası sebepler → Test:**
1. Gateway servisi durmuş → Windows servis / taskbar ikonu yeşil mi?
2. Runtime durmuş → `sudo systemctl status codesyscontrol` → active (running)?
3. Ağ yok → `ping <PLC-IP>`
4. Port kapalı → `telnet <PLC-IP> 1217` (gateway), 1740 da gerekli
5. Yanlış gateway ayarı → Tools → Communication Settings
6. Device description uyumsuz → runtime versiyonuyla eşleşmeli

**Çözüm:** Sebebe göre servis restart / firewall'da 1217+1740 aç / doğru IP:port / device update.
> Saha notu: Uyku modundan kalkan makinede gateway kendini başlatmayabilir → "Recovery" ayarı yap.

---

## 2. Task Watchdog Hataları

**Semptom:** Uygulama aniden durdu. Log: "Watchdog exception in Task_X". Fiziksel çıkışlar son değerinde kaldı.

**Katman:** Kod.

**Olası sebepler:**
- **Sonsuz döngü** — FOR/WHILE çıkış koşulu hiç sağlanmıyor (ör. `LEN()` off-by-one → array taşması).
- **Çok uzun exec** — task kodu cycle time'dan uzun sürüyor.
- **Bloklanma** — dosya yazma / ağ çağrısı / seri port ana task'ta, yanıt bekliyor.
- **CPU aşırı yük** — tüm task'lar toplamı %100'ü aşıyor.

**Test adımları:**
1. Log → hangi task?
2. O task'ın son döngüde ne çalıştırdığını bul.
3. Task Monitor → Max Cycle Time ölç.
4. Data breakpoint ile şüpheli döngü değişkenini izle.

**Çözüm:** Sonsuz döngü → çıkış koşulu. Uzun exec / bloklanma → Freewheeling task'a taşı, cycle artır. CPU yük → kodu dağıt.
> Watchdog süresini artırmak çözüm değil, sadece araştırma için zaman kazanır.

---

## 3. OPC-UA Bağlantı Sorunları

**Semptom:** İstemci bağlanamıyor / node bulunamıyor / "BadCertificateUntrusted" / değerler kademeli güncelleniyor.

**Katman:** Çoğunlukla config/altyapı.

**Olası sebepler → Test:**
1. **Sertifika güvenilmiyor** → istemci/sunucu trust listesini kontrol et; sertifika expire / PLC saati yanlış (NTP)?
2. **Güvenlik modu uyumsuz** → sunucu SignAndEncrypt, istemci None mı?
3. **NodeId değişti** → değişken adı değişince tag kaybı (NodeId'leri "frozen" say).
4. **Sampling < task cycle** → değerler kademeli; sampling interval ≥ task cycle olmalı.
5. **Sembol patlaması** → çok node, bootapp şişti → sembol setini daralt.
6. **Anonim erişim üretimde açık** → güvenlik açığı (kapatılmalı).

**Çözüm:** Trust + NTP + güvenlik modu eşitle; sampling ≥ cycle; symbol config daralt. Referans: `/knowledge/protocols/opc-ua/`, `/knowledge/codesys/networking/01_opcua_server.md`.

---

## 4. Modbus İletişim Hataları

**Semptom:** "Illegal Data Address" (0x02) / veri hiç gelmiyor / setpoint kayboluyor / DWORD değeri saçma ("Frankenstein").

**Katman:** Config/kod.

**Olası sebepler → Test:**
1. **0 vs 1 tabanlı adres** → belge "40001" diyor, protokol 0-tabanlı: `address = belge_no - 40001`. Test değeriyle doğrula.
2. **Word tearing** → DWORD/REAL iki register, ayrı isteklerde okununca yarısı eski. Tek FC isteğinde oku.
3. **HR'ı PLC eziyor** → master setpoint yazıyor ama PLC her döngü üzerine yazıyor → HR→GVL tek yön kuralı.
4. **125-register limiti** → tek istekte >125 register → reddedilir. Blok böl.
5. **Byte/word order** → float 2 register, sıralama yanlış.

**Çözüm:** Adres tabanını doğrula, tek-yazar disiplini, blok limiti, byte order. Referans: `/knowledge/protocols/modbus-tcp/`.
> Modbus internete asla açılmaz (FrostyGoop 2024). Port 502 NAT arkasında bile değil.

---

## 5. HMI Veri Güncellenmeme Sorunları

**Semptom:** HMI'da değer donmuş / eski / hiç gelmiyor; bağlantı kopması fark edilmiyor.

**Katman:** Köprü protokolü + HMI.

**Olası sebepler → Test:**
1. **Protokol bağlantısı koptu** → OPC-UA session / Modbus master canlı mı? Wireshark ile trafik var mı?
2. **Sampling/poll periyodu** → "geç görüyor" çoğu zaman sampling, ağ değil.
3. **Bağlantı-kopması ele alınmamış** → HMI son değeri "canlı" sanıyor. Heartbeat/connection flag eksik.
4. **MQTT LWT yok** → broker'dan kopunca dashboard "online" gösterir → LWT retained "false" zorunlu.
5. **Tek-yazar ihlali** → iki kaynak aynı değeri yazıyor, biri eziyor.

**Çözüm:** Connection flag/heartbeat ekle; sampling ayarla; LWT kur. HMI her zaman bağlantı durumunu göstermeli.

---

## 6. Performans Sorunları

**Semptom:** Jitter, ara ara watchdog'a yaklaşma, CPU yüksek, tepki yavaş.

**Katman:** Kod/yapı.

**Test adımları:**
1. Task Monitor → her task Average + **Max** cycle time (Max kritik — sessiz jitter burada).
2. Toplam CPU yükü ölç (hedef ≤ %70).
3. En ağır task'ı bul; içinde döngü/string/ağ işlemi var mı?

**Çözüm:**
- Ağır hesabı yavaş task'a veya Freewheeling'e taşı.
- String/dizi işlemlerini optimize et.
- Bloke I/O'yu kontrol task'ından çıkar.
- Gereksiz polling'i subscription/event ile değiştir.

Referans: `/knowledge/codesys/debugging/03_performance_analysis.md`, `/knowledge/codesys/task-structure/02_cycle_time.md`.

---

## 7. Log'un Yanılttığı / Sessiz Hatalar

Bazı sorunlar Log'a yazılmaz ya da yanıltıcı yazar — bunları bilmek uzmanlıktır:

| Durum | Log davranışı | Gerçek tanı yolu |
|-------|---------------|------------------|
| Bozuk bootapp (eski kod yüklü) | Hata YOK | power-cycle + versiyon karşılaştır; Create Boot Application unutulmuş |
| Dangling pointer crash | AccessViolation, yeri değişken | pointer şüphesi, data breakpoint |
| Cycle overrun < watchdog | Hata YOK (sessiz jitter) | Task Monitor Max Cycle |
| RTC pili bitik → 1970 | Yanlış zaman damgalı log | NTP + RTC kontrol |
| `__TRY/__CATCH` 64-bit'te | Derlendi ama çalışmaz | savunmacı null/index kontrolü |
| NaN yayılması (REAL /0) | Hata YOK | `__FINITE` kontrol, watch |
| Multicore race | Sporadik, izsiz | atomiklik analizi |

**Hata mesajının "yalan söylediği" klasikler:**
- "Download failed: Unknown reason" → gerçek neden Log'un **altındaki** Exception satırında.
- "Communication error" → çoğu zaman gateway/ağ, runtime değil.
- "Compile required" (derlenmişken) → device/runtime versiyon uyumsuzluğu.
- AccessViolation farklı yerlerde → sabit değil → pointer/bellek.
- "Slave not operational" → çoğu zaman fiziksel (kablo IN/OUT portu), config değil.

---

## 8. Tekrarlayan Hata Kontrol Listesi

Sahada aynı 10-15 hata döner. Devreye alma öncesi:
```
□ Devreye alma: Create Boot Application + power-cycle test
□ RETAIN değişikliği: değerleri yedekle, değişkeni SONA ekle
□ Yeni donanım: device description kur + EtherCAT kablo IN/OUT kontrol
□ Yeni kurulum: gateway servisi + port 1217/1740 + kütüphane sürümü
□ Platform değişimi (32→64-bit): __TRY çalışmaz → savunmacı kod
□ OPC-UA: sertifika + NTP + güvenlik modu + sampling ≥ cycle
□ Modbus: adres tabanı (0 vs 1) test değeriyle doğrula
□ MQTT: LWT retained "false" + benzersiz Client ID
```

---

## Debug Süresini Kısaltma — Disiplin

```
1. Log oku (ekran özeti değil, Log sekmesi) → kategori
2. Kategoriye göre TEK alt-sistemde daralt (ağ/kod/fieldbus/retain/versiyon)
3. O alt-sistemde doğru aracı seç (Watch / Trace / Data BP / PLC Shell)
4. Kök nedene in → düzelt → doğrula (Online Change veya download + boot app)
```

Kritik hataları (watchdog, exception, fieldbus) OPC-UA/MQTT ile SCADA'ya raporlamak, "ne oldu" sorusunu post-mortem'den anlık tespite indirir.
