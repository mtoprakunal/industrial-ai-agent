---
KONU        : Vaka Çalışması — Senkron Motion (Winder / Flying Saw / Flying Shear)
KATEGORİ    : examples
ALT_KATEGORI: case-studies
SEVİYE      : Orta
SON_GÜNCELLEME: 2026-06-10
KAYNAKLAR   :
  - url: "https://control.com/technical-articles/an-introduction-to-synchronized-motion-control/"
    başlık: "An Introduction to Synchronized Motion Control — control.com (CAM/gear, flying shear)"
    güvenilirlik: topluluk
  - url: "https://infoneva.com/en/knowledge/impact-of-incorrect-distributed-clock-settings-on-ethercat-motion-synchronization"
    başlık: "EtherCAT Distributed Clock yanlış ayarının senkronizasyona etkisi — Infoneva"
    güvenilirlik: topluluk
  - url: "https://en.motion-con.com/news/6.html"
    başlık: "Development and application of flying shear control instructions — Motion-Con"
    güvenilirlik: topluluk
  - url: "https://www.inovance.eu/fileadmin/downloads/Brochures/EN/AM600_Br_EN_Singles_Web_V2.2.pdf"
    başlık: "Inovance AM600 — 32 eksen, 8 enterpolasyon, 16 CAM, EtherCAT master"
    güvenilirlik: resmi
  - url: "https://www.inovance.eu/fileadmin/downloads/Servo_drives_and_motors/SV660N_Advanced_User_Guide.pdf"
    başlık: "Inovance SV660N — CiA 402, CSP/CSV/CST, ~125 µs çevrim, 23-bit enkoder"
    güvenilirlik: resmi
  - url: "https://store.codesys.com/media/n98_media_assets/files/Bundle-SoftMotion/0/CODESYS%20SoftMotion%20SL_en.pdf"
    başlık: "CODESYS SoftMotion Data Sheet — MC_GearIn/MC_CamIn, sanal eksen"
    güvenilirlik: resmi
  - url: "knowledge/codesys/task-structure/_synthesis.md"
    başlık: "CODESYS Task Yapısı Sentezi — motion task önceliği/çevrimi"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/examples/case-studies/01_packaging_machine.md"
    ilişki: detaylandırır
  - konu: "knowledge/codesys/task-structure/_synthesis.md"
    ilişki: gerektirir
  - konu: "devices/INOVANCE_AM600"
    ilişki: kullanır
  - konu: "devices/INOVANCE_SV660N"
    ilişki: kullanır
  - konu: "knowledge/protocols/_synthesis.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "EtherCAT CiA 402 ekseni ve PLCopen MC_ FB kavramı"
  - "CAM (elektronik kam) ve electronic gearing temel mantığı"
  - "Task önceliği/çevrim süresi (decision_framework.md §2)"
ÇELİŞKİLER :
  - kaynak: "Pazarlama: 'sıfır following error'"
    konu: "Following error (takip hatası) sıfırlanamaz"
    çözüm: >
      Kaynak (control.com) açıkça belirtir: feedback çözünürlüğü, örnekleme jitter'ı
      ve faz gecikmesi nedeniyle her zaman bir miktar takip hatası vardır. Hedef onu
      sıfırlamak değil, sınır içinde tutmak ve eşik aşımında güvenli durdurmaktır.
---

## Özün Ne

Bu vaka, bir eksenin (slave) sürekli hareket eden bir master'a **mekanik bağlantı olmadan,
yazılımla senkron kilitlendiği** uygulamaları kapsar: winder (sarıcı, gerginlik/çap kontrolü),
flying saw / flying shear (uçan testere/makas — hareket eden malzemeyi durdurmadan kesme).
Mühendislik özü, slave ekseni master'ın **gerçek pozisyonuna** electronic gearing (sabit
oran) veya electronic CAM (pozisyona bağlı profil) ile bağlamaktır. Flying shear'da slave,
malzeme hızına eşitlenir, keser, sonra başlangıca döner (return) — hepsi malzeme akarken.

Neden önemli: Bu sınıf uygulamalar **gerçek-zaman gereksiniminin en sert olduğu** yerdir.
Senkronizasyon mikrosaniye mertebesinde tutarlı olmalı; aksi halde kesim boyu kayar, sarım
gevşer ya da takip hatası eksen arızasına dönüşür. Protokol seçiminde tartışma yoktur:
fieldbus (EtherCAT) zorunludur, raporlama protokolleri (OPC-UA/Modbus/MQTT) bu döngüye giremez.

## Nasıl Çalışır

- **Master ekseni:** Gerçek bir hat ekseni (çekme rulosu) ya da sanal (virtual) eksen.
  Master pozisyonu/hızı tüm senkron eksenlerin referansıdır.
- **Electronic gearing (MC_GearIn):** Slave = master × oran. Winder'da rulo çapı arttıkça
  oran değiştirilir (sabit çizgisel hız ya da sabit gerginlik için).
- **Electronic CAM (MC_CamIn):** Slave pozisyonu, master pozisyonunun bir tablo
  fonksiyonudur. Flying shear profili: sync (malzeme hızına eşitle) → cut (kesme penceresi) →
  return (hızla geri) → bekle. (kaynak: control.com; Motion-Con flying shear).
- **Touch-probe / yakalama:** Kesme tetiği (uzunluk sayacı veya işaret sensörü) ile fazlanır;
  hassas uzunluk için master encoder + touch-probe kullanılır.
- **Following error (takip hatası):** Komut pozisyon ile gerçek pozisyon farkı. Kaynak
  (control.com) der ki bu her zaman vardır (çözünürlük, jitter, faz gecikmesi). Sürücü
  eşiği aşınca hata/STO ile güvenli durur.
- **Distributed Clock (DC):** EtherCAT'te tüm senkron eksenlerin aynı anda güncellenmesini
  sağlar. Yanlış DC → jitter ve birikimli sapma (kaynak: Infoneva).

## Pratikte Nasıl Kullanılır

**Gereksinim listesi (flying shear örneği):**
1. Hareket eden malzemeyi durdurmadan, sabit uzunlukta kesmek.
2. Kesme ekseni malzeme hızına ±küçük takip hatasıyla eşitlenmeli.
3. Uzunluk doğruluğu: enkoder/işaret tetiği ile faz.
4. Takip hatası eşiği aşılırsa güvenli durdurma (+ STO).
5. HMI: kesim uzunluğu, hız, sayaç, takip hatası/alarm.
6. (Winder) çap/gerginlik geri beslemesiyle oran/tork kontrolü.

**Mimari karar (KARAR/GEREKÇE/TAKAS):**

```
KARAR:   EtherCAT master kontrolör (Inovance AM600) + CiA 402 servo (SV660N) CSP modunda;
         sanal master + MC_CamIn ile flying shear profili. Senkron en hızlı motion task'ta.
GEREKÇE: Senkronizasyon <1 ms jitter ve DC eşlemesi ister. SV660N CSP/CSV/CST, ~125 µs
         çevrim, 23-bit enkoder; AM600 16 CAM/8 enterpolasyon EtherCAT master.
ALT:     Step + basit gear; sadece düşük hız/düşük doğruluk + sabit oranda yeter. Değişken
         hız ve hassas uzunlukta CAM + servo gerekir.
TAKAS:   SoftMotion/EtherCAT lisans + DC kurulum karmaşıklığı; yanlış kurulumda senkron
         kaybı. Bu yüzden devreye almada following error ve DC ölçümü zorunlu.
```

```
KARAR:   Protokol katmanlaması: EtherCAT (eksen, ZORUNLU) + OPC-UA/Modbus (yalnız HMI/raporlama).
GEREKÇE: decision_framework §1, ilke 3: dört raporlama protokolünün hiçbiri <1 ms motion
         için değildir. Kesme/sarım kontrolü EtherCAT'te; uzunluk/sayaç/alarm raporlama
         katmanında.
ALT:     Yok — raporlama protokolünü kontrol döngüsüne sokmak tasarım hatasıdır.
TAKAS:   İki katman; ama bu ayrım pazarlık konusu değil. HMI çağrısı motion task'ını asla
         bloke etmemeli (ayrı Task_Comm).
```

**Task / protokol / HMI eşlemesi:**

| Mantık | Task | Cycle | Protokol/Arayüz |
|--------|------|-------|------------------|
| STO / e-stop | Donanımsal emniyet (STO girişi) | ≤1 ms | Donanım (SV660N CN6 STO) |
| Sanal master + CAM/gear, servo | Task_Motion | ≤1 ms (DC senkron) | EtherCAT CiA 402 (CSP) |
| Kesme tetiği / touch-probe | Task_Motion | senkron | EtherCAT touch-probe / HSC |
| Takip hatası izleme + güvenli dur | Task_Motion | senkron | EtherCAT (Statusword 6041h) |
| Çap/gerginlik (winder) hesap | Task_Fast/Control | 4–10 ms | Analog/enkoder |
| HMI: uzunluk, hız, sayaç, alarm | Task_Comm | ≤200 ms | OPC-UA |
| Üretim/OEE log | Task_Background | best-effort | MQTT/OPC-UA |

## Örnekler

- **Flying shear profili (CAM):** Master 0–360° için slave profili: 0–120° sync (hız eşit,
  pozisyon kilitli), 120–180° cut (bıçak indir/kaldır), 180–360° return (hızlı geri). Master
  uzunluk sayacı hedefe ulaşınca CAM bir çevrim tetiklenir.
- **Winder oran güncelleme:** Çap = ∫(hat hızı)/(rpm) ile tahmin edilir; MC_GearIn oranı her
  çevrimde güncellenir (sabit çizgisel hız). Gerginlik için tork limiti (CST) veya dancer
  geri beslemesi.
- **Takip hatası koruması:** `IF ABS(komut_poz − gercek_poz) > esik THEN MC_Stop + STO talep`.
  Eşik malzeme/hıza göre ayarlanır; aşım genelde mekanik sıkışma/aşırı hız işaretidir.

## Sık Yapılan Hatalar

- **Senkron mantığı yavaş task'a koymak.** CAM/gear Task_Control'e (10 ms) konursa jitter
  uzunluğu kaydırır. Senkron eksenler en hızlı, en yüksek öncelikli task'ta, DC ile.
- **Distributed Clock'u yanlış/kapalı bırakmak.** Eksenler aynı anda güncellenmez; sapma
  birikir, kesim boyu sürekli kayar (kaynak: Infoneva). Tüm senkron slave'de DC eşlenmeli.
- **Following error'ı 'sıfır' beklemek.** Fiziksel olarak imkânsız (control.com); doğru
  yaklaşım eşik koymak ve aşımda güvenli durmaktır.
- **Return fazını malzeme hızına yetiştirememek.** Return çok yavaşsa eksen bir sonraki
  kesime hazır olamaz; profil/ivme tekrar boyutlandırılır (makine hız limiti buradan çıkar).
- **STO'yu yazılımla taklit etmek.** Takip hatası durdurması emniyet DEĞİLDİR; STO donanımsal
  güvenlik fonksiyonudur (SV660N -FS, çift kanal). E-stop/STO yazılımdan bağımsız kalmalı.

## Ne Zaman Tercih Edilmeli / Edilmemeli

- **EtherCAT + CAM/gear servo tercih:** Değişken hatta hassas uzunluk kesimi (flying shear/saw),
  gerginlik/çap kontrollü sarım, çok eksenli senkron baskı/tekstil.
- **Etmemeli:** Malzeme durdurulup kesilebiliyorsa (stop-and-cut), flying shear karmaşıklığı
  gereksizdir; durdur–kes daha basit ve ucuzdur. Sabit oranlı düşük doğruluk işinde basit
  gear/step yeter.

## Gerçek Proje Notları

- Devreye almada ilk bakılan şey following error trendidir: kararsız/artıyorsa ya kazançlar
  (gain) ya DC ya da mekanik (kayış gerginliği/atalet) sorunludur. CAM profilini suçlamadan
  önce bunlar elenir.
- "Kesim boyu yavaşça kayıyor" = neredeyse her zaman DC/senkronizasyon ya da enkoder kayması;
  "rastgele sıçrıyor" = tetik/touch-probe gürültüsü. Belirti kök nedeni daraltır.
- Winder'da çap tahmini hatası gerginliği bozar; doğrudan dancer/load-cell gerginlik geri
  beslemesi tahmine her zaman üstündür ama daha pahalıdır — gereksinime göre seçilir.
- AM600 + SV660N'de CSP modu + DC en yaygın senkron kurulumdur; ESI/firmware sürüm uyumu ve
  SoftMotion eksen yapılandırması devreye almada en sık takılınan adımdır (bkz. inoproshop).

## İlgili Konular

- `knowledge/examples/case-studies/01_packaging_machine.md` — CAM senkronizasyonun makine içi kullanımı
- `knowledge/codesys/task-structure/_synthesis.md` — motion task önceliği/çevrimi
- `devices/INOVANCE_AM600`, `devices/INOVANCE_SV660N` — EtherCAT master + CiA 402 servo
- `knowledge/protocols/_synthesis.md` — neden raporlama protokolü motion'a girmez
