# Proje Tasarım Raporu — `[PROJE_ADI]`

> Bu rapor, üretilen her CODESYS projesi için tasarım kararlarını ve gerekçelerini
> belgeler. Her `[doldurulacak]` alani proje verisi ile degistirin; rehber notlar
> (`> ...` satirlari) teslim oncesi silinebilir.

| Alan | Deger |
|------|-------|
| Proje adi | `[doldurulacak]` |
| Olusturulma tarihi | `[doldurulacak]` |
| Platform | CODESYS `[surum]` |
| Hedef donanim | `[doldurulacak]` |
| Rapor surumu | `[doldurulacak]` |
| Hazirlayan | `[doldurulacak]` |

---

## 1. Proje Ozeti

`[doldurulacak]`

> 2-4 cumle: sistem ne yapar, kac bolge/eksen/istasyon, ana fonksiyon nedir.
> Ornek: "3 bolgeli konveyor hatti; hiz kontrolu, sikisma algilama ve acil durdurma."

## 2. Gereksinim Analizi

### 2.1 Fonksiyonel Gereksinimler
- `[doldurulacak]`

> `project_spec.json` icindeki `fonksiyonel_gereksinimler` listesini buraya cikar.
> Her gereksinime izlenebilirlik icin FR-01, FR-02 gibi numara ver.

### 2.2 Fonksiyonel Olmayan Gereksinimler
- Cevrim suresi / determinizm: `[doldurulacak]`
- Erisilebilirlik / yedeklilik: `[doldurulacak]`
- Standart uyumu (IEC 61131-3, IEC 62443, performans seviyesi): `[doldurulacak]`

## 3. Mimari Karar — Protokol Secimi

| Konu | Karar | Gerekce |
|------|-------|---------|
| Haberlesme protokolu | `[doldurulacak]` | `[doldurulacak]` |
| HMI tipi | `[doldurulacak]` | `[doldurulacak]` |

> Protokol secim gerekcesini acikca yaz. Ornek: birden fazla HMI istemcisi ve
> yapilandirilmis veri gerektiginden OPC-UA secildi; basit register erisimi
> yeterli olsaydi Modbus TCP tercih edilirdi. Reddedilen alternatifleri de belirt.

## 4. Donanim / IO Mimarisi

- IO sayilari: DI `[..]`, DO `[..]`, AI `[..]`, AO `[..]`
- IO modul yapilandirmasi: `[doldurulacak]`
- Detayli sinyal listesi: bkz. `io_list.csv`

> Adresleme semasini (%IX, %QX, %IW) ve olcekleme notlarini (orn. 4-20mA = 0-120
> m/min) ozetle. Tam liste io_list.csv'de tutulur, burada tekrar etme.

## 5. Task Yapisi ve Cevrim Sureleri

| Task | Tip | Cevrim | Oncelik | Atanan POU'lar |
|------|-----|--------|---------|----------------|
| Fast | Cyclic | `[..] ms` | `[..]` | `[doldurulacak]` |
| Control | Cyclic | `[..] ms` | `[..]` | `[doldurulacak]` |
| Slow | Cyclic | `[..] ms` | `[..]` | `[doldurulacak]` |

> Guvenlik kritik (E-Stop, calistirma izni) sinyaller en hizli task'a atanmalidir.
> io_list.csv'deki `Task` sutunu ile tutarli olmalidir.

## 6. Yazilim Mimarisi (POU / FB)

| POU / FB | Tip | Sorumluluk |
|----------|-----|------------|
| `[doldurulacak]` | PRG/FB/FUN | `[doldurulacak]` |

> Her bolge/istasyon icin yeniden kullanilabilir FB tasarimini belirt.
> Durum makinesi (State Machine) varsa durumlari listele
> (orn. IDLE -> RUNNING -> JAMMED -> FAULT).

## 7. Haberlesme Tasarimi

- Protokol / port: `[doldurulacak]`
- Adres alani / namespace / register haritasi: `[doldurulacak]`
- Yayinlanan / abone olunan etiketler: `[doldurulacak]`
- Ag topolojisi: bkz. `network_diagram.md`

## 8. HMI Tasarimi

- HMI tipi / teknoloji: `[doldurulacak]`
- Ekranlar: `[doldurulacak]`
- Operator / Bakim / Yonetici yetki seviyeleri: `[doldurulacak]`

> Ana ekran, bolge detay, alarm ekrani, trend gibi temel sayfalari listele.

## 9. Alarm Stratejisi

- Seviyeler: Kritik / Yuksek / Orta / Dusuk
- Alarm listesi: bkz. `alarm_list.csv`
- Onaylama (acknowledge) ve reset mantigi: `[doldurulacak]`
- NAMUR NE107 / kablo kopmasi tespiti: `[doldurulacak]`

## 10. Guvenlik (E-Stop / Interlock)

- E-Stop zinciri: `[doldurulacak]`

> NC mantik, donanimsal kesme, en gec durma suresi (orn. 500 ms) belirt.

- Interlock mantigi: `[doldurulacak]`
- Calistirma izni (permit) kosullari: `[doldurulacak]`
- Reset / hata kabul akisi: `[doldurulacak]`

## 11. Test Senaryolari

| # | Senaryo | On Kosul | Beklenen Sonuc | Durum |
|---|---------|----------|----------------|-------|
| T-01 | `[doldurulacak]` | `[..]` | `[..]` | [ ] |
| T-02 | E-Stop basildiginda tum motorlar `[..] ms` icinde durur | Sistem calisiyor | Tum DO motor cikislari 0 | [ ] |
| T-03 | `[doldurulacak]` | `[..]` | `[..]` | [ ] |

> En az: normal calisma, E-Stop, sikisma, haberlesme kopmasi ve interlock
> senaryolarini ekle.

## 12. Bilinen Sinirlamalar

- `[doldurulacak]`

> Kapsam disi birakilanlar, varsayimlar, gelecekteki gelistirmeler.

## 13. Referanslar

- `project_spec.json` — proje gereksinim girdisi
- `io_list.csv` — sinyal listesi
- `alarm_list.csv` — alarm listesi
- `network_diagram.md` — ag topolojisi
- Standartlar: IEC 61131-3, IEC 62443, NAMUR NE107
- `[doldurulacak]` — ek referanslar
