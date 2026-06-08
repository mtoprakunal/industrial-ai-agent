---
KONU        : TCP Socket — Sentez
KATEGORİ    : protocols
ALT_KATEGORI: tcp-socket
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-08
KAYNAKLAR   :
  - url: "knowledge/protocols/tcp-socket/01_basics.md"
    başlık: "TCP Socket Temelleri"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/tcp-socket/02_codesys_implementation.md"
    başlık: "CODESYS SysSock ile TCP Programlama"
    güvenilirlik: deneyimsel
  - url: "knowledge/protocols/tcp-socket/03_custom_protocol_design.md"
    başlık: "TCP Üzerinde Özel Protokol Tasarımı"
    güvenilirlik: deneyimsel
BAĞLANTILAR :
  - konu: "knowledge/codesys/networking/03_tcp_socket.md"
    ilişki: tamamlar
  - konu: "knowledge/protocols/modbus-tcp/01_protocol_basics.md"
    ilişki: alternatif
  - konu: "knowledge/protocols/opc-ua/01_architecture.md"
    ilişki: alternatif
  - konu: "knowledge/codesys/programming/03_function_blocks.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "OSI modeli ve TCP/IP temel kavramları"
  - "CODESYS Function Block geliştirme"
  - "Pointer ve ADR() kullanımı IEC ST'de"
ÇELİŞKİLER :
  - kaynak: "TCP = yavaş algısı"
    konu: "Fabrika LAN'ında TCP round-trip süresi"
    çözüm: >
      LAN içi TCP round-trip <1ms. Bağlantı kurulumu (SYN-SYN/ACK-ACK) tek seferlik.
      Kalıcı bağlantı (persistent connection) ile overhead minimaldir.
      "Yavaş" senaryo: Her mesaj için yeni bağlantı açılıyorsa. Çözüm: bir kez bağlan, sürekli kullan.
  - kaynak: "SysSockConnect blocking mode istisnası"
    konu: "Non-blocking socket'ta connect() davranışı"
    çözüm: >
      FIONBIO ile non-blocking moda alınan socket'ta dahi SysSockConnect BLOCKING çalışır.
      connect() çağrısını her zaman Freewheeling veya düşük öncelikli task'ta çalıştır;
      yüksek öncelikli Task_Control'de connect() tüm sistemi dondurur ve Watchdog'u tetikler.
  - kaynak: "Big-Endian vs Little-Endian seçimi"
    konu: "Özel protokolde byte sırası standardı"
    çözüm: >
      Network Byte Order = Big-Endian. IP ve TCP başlıkları big-endian kullanır.
      x86 ve çoğu CODESYS PLC little-endian işlemci. Özel protokolde big-endian seç;
      gelecekteki heterojen sistemlerde taşınabilirlik sağlar.
---

## Özün Ne

Bu sentez, "TCP socket'tan CODESYS implementasyonuna, oradan özel protokol tasarımına bütüncül bir resim nasıl çizilir?" sorusuna yanıt verir. Üç belge birbirinin önkoşuludur: TCP temelleri stream modelini ve framing ihtiyacını açıklar; CODESYS implementasyonu bu modeli SysSock API'siyle PLC bağlamına taşır; özel protokol tasarımı ise akümülatör buffer ve state machine ile uçtan uca çalışan bir iletişim katmanı kurar. Bu üçü birlikte anlaşıldığında, Modbus veya OPC UA desteklemeyen herhangi bir cihazla güvenilir, hata toleranslı bir TCP iletişimi inşa etmek mümkün olur.

## Nasıl Çalışır

### Zihin Haritası: Ham TCP'den CODESYS'e, Oradan Özel Protokole

```
┌─────────────────────────────────────────────────────────────────────────┐
│              TCP SOCKET — BÜTÜNSEL ZİHİN HARİTASI                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  01_basics.md — TCP Stream Modeli                                        │
│  ┌────────────────────────────────────────────────────────┐             │
│  │  TCP bağlantısı = Byte Stream                          │             │
│  │                                                        │             │
│  │  SYN → SYN-ACK → ACK  [Tek seferlik el sıkışma]      │             │
│  │  ════════ Kalıcı bağlantı ════════════════════════     │             │
│  │  Mesaj 1 gönder │ Mesaj 2 gönder │ Mesaj N gönder     │             │
│  │  FIN → ...      [Bağlantı kapatma]                     │             │
│  │                                                        │             │
│  │  Kritik Gerçek: send(100 byte) → recv() 30+70 byte    │             │
│  │  TCP mesaj sınırlarını korumaz → Framing zorunlu       │             │
│  └────────────────────────┬───────────────────────────────┘             │
│                           │ Framing ihtiyacını doğurur                  │
│                           ▼                                              │
│  03_custom_protocol_design.md — Protokol Katmanı                         │
│  ┌────────────────────────────────────────────────────────┐             │
│  │  [SOH 1B][VER 1B][MSG 1B][LENGTH 2B][DATA NB][CKSUM 1B]│            │
│  │                                                        │             │
│  │  Akümülatör buffer + State machine parser:             │             │
│  │  eWaitSOH → eReadHeader → eReadData → mesaj hazır      │             │
│  │                                                        │             │
│  │  Senkronizasyon kaybı → SOH arama → kurtarma           │             │
│  │  Versiyonlama → VER alanı → geriye uyumluluk           │             │
│  └────────────────────────┬───────────────────────────────┘             │
│                           │ PLC bağlamında nasıl hayata geçirilir?       │
│                           ▼                                              │
│  02_codesys_implementation.md — SysSock API                             │
│  ┌────────────────────────────────────────────────────────┐             │
│  │  SysSockCreate → SysSockIoctl(FIONBIO) → Non-blocking │             │
│  │                                                        │             │
│  │  TCP Client (FB_TcpClient):                            │             │
│  │    eDisconnected → eConnecting [BLOCKING!]             │             │
│  │    → eConnected → eSending/eReceiving → eClosing       │             │
│  │                                                        │             │
│  │  TCP Server (FB_TcpServer):                            │             │
│  │    eTcpSrv_Idle → eTcpSrv_Listening [non-blocking]    │             │
│  │    → eTcpSrv_ClientConnected → veri al / yanıtla       │             │
│  │                                                        │             │
│  │  Task mimarisi:                                        │             │
│  │    Task_Background (Prio 10-15): TCP bağlantı yönetimi │             │
│  │    Task_Control   (Prio 2):      Kontrol mantığı       │             │
│  │    GVL:  İki task arasında veri köprüsü               │             │
│  └────────────────────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────────────┘
```

### Mental Model: Üç Katman, Tek Bütün

TCP socket programlama üç bağımsız soruya yanıt arar ve her belge bir soruyu çözer:

> **"Verimi karşı tarafa nasıl güvenilir biçimde iletebilirim?"**  
> TCP'nin garantisi: Her byte eksiksiz, sıralı ulaşır. Ancak mesaj sınırları korunmaz.  
> Bu soruyu `01_basics.md` yanıtlar.

> **"Nerede başlayıp nerede biteceğini bilemediğim bir byte akışından anlamlı mesajlar nasıl çıkarırım?"**  
> SOH + LENGTH + CHECKSUM üçlüsü ve akümülatör buffer state machine'i bunu çözer.  
> Bu soruyu `03_custom_protocol_design.md` yanıtlar.

> **"Bunu bir PLC'de, scan döngüsünü bloke etmeden, bağlantı kopmasını yönetir biçimde nasıl yazarım?"**  
> SysSock API, non-blocking mode, task ayrımı ve SO_REUSEADDR bunu sağlar.  
> Bu soruyu `02_codesys_implementation.md` yanıtlar.

Bu üç soruya aynı anda hakimsen çalışan, üretim ortamına hazır bir TCP iletişim katmanı yazabilirsin.

## Hızlı Referans Tabloları

### A. CODESYS SysSock API — Fonksiyon Özeti

| Fonksiyon | Amaç | Kritik Not |
|---|---|---|
| `SysSockCreate` | Socket oluştur | `RTS_INVALID_HANDLE` dönerse hata |
| `SysSockIoctl(FIONBIO)` | Non-blocking moda al | Hemen `Create` sonrası çağır |
| `SysSockSetOption(SO_REUSEADDR)` | Bind'dan önce ayarla | Restart sonrası TIME_WAIT sorununu önler |
| `SysSockSetOption(SO_KEEPALIVE)` | Keep-alive aç | Phantom bağlantı tespiti için |
| `SysSockConnect` | Server'a bağlan (Client) | **HER ZAMAN BLOCKING** — Freewheeling task'ta çağır |
| `SysSockBind` | Porta bağla (Server) | `INADDR_ANY` = `0` ile tüm arayüzleri dinle |
| `SysSockListen` | Bağlantı kuyruğu aç | Backlog = 1 (genellikle yeterli) |
| `SysSockAccept` | Gelen bağlantıyı kabul et | Non-blocking'de bağlantı yoksa hemen döner |
| `SysSockSend` | Veri gönder | Dönüş < 0 → Bağlantı koptu |
| `SysSockRecv` | Veri al | Dönüş 0 = EOF; < 0 = non-blocking veri yok (normal) |
| `SysSockShutdown` + `SysSockClose` | Bağlantıyı nazikçe kapat | Her çıkış yolunda her iki çağrıyı yap |
| `SysSockHtons` | Port → Network byte order | Port numarasını `sin_port`'a koymadan önce |
| `SysSockInetAddr` | IP string → UDINT | `sockAddr.sin_addr` için |

### B. Protokol Tasarım: Çerçeve Formatı

```
Bayt:  [0]      [1]     [2]      [3]    [4]    [5..4+N]   [5+N]
Alan:  SOH      VER     MSG      LEN_H  LEN_L  DATA       CKSUM
Değer: 0x01     1-255   tip      Hi     Lo     N byte     XOR
```

| Alan | Boyut | Seçim Gerekçesi |
|---|---|---|
| SOH (0x01) | 1 byte | Senkronizasyon kaybında başlangıç noktası |
| VER | 1 byte | Geriye uyumlu protokol evrimi |
| MSG Type | 1 byte | 256 mesaj tipi yeterli (0x10=Data, 0x20=Cmd, 0x30=Resp, 0x40=Err, 0x50=HB, 0x51=HB-Resp) |
| LENGTH | 2 byte big-endian | Data alanının uzunluğu; 0–65535 byte |
| DATA | N byte | Mesaj içeriği; MSG Type'a göre yorumlanır |
| CHECKSUM | 1 byte XOR | SOH'dan DATA sonuna tüm byte'ların XOR'u |

### C. Framing Yöntemleri Karşılaştırması

| Yöntem | Avantaj | Dezavantaj | Endüstriyel Öneri |
|---|---|---|---|
| Length-prefixed | Basit parse, data'da delimiter sorunu yok | Uzunluk hatalıysa parser bozulur | **Tercih et** |
| Delimiter-based (`\r\n`) | ASCII protokollerle uyumlu | Data'da delimiter gelirse escape gerekir | Yalnızca ASCII, sabit-format cihazlarda |
| Sabit uzunluk | En basit parser | Esnek değil | Yalnızca sabit payload sistemlerde |

### D. Blocking vs Non-Blocking: CODESYS'te Özet Kural

| SysSock Çağrısı | Non-blocking Moda Alınınca | Nerede Çağrılmalı |
|---|---|---|
| `SysSockConnect` | **HER ZAMAN BLOCKING** (istisna) | Freewheeling / Task_Background |
| `SysSockAccept` | Bağlantı yoksa anında döner | Task_Background |
| `SysSockRecv` | Veri yoksa -1 döner (hata değil) | Her task (non-blocking modda) |
| `SysSockSend` | Buffer doluysa -1 döner | Her task (non-blocking modda) |

### E. recv() Dönüş Değeri Anlamları

| Değer | Anlam | Yapılacak |
|---|---|---|
| `> 0` | N byte veri alındı | İşle, buffer'a ekle |
| `= 0` | EOF: Karşı taraf bağlantıyı kapattı | `eState := eDisconnected` |
| `< 0` (non-blocking) | Veri yok, döngüye devam et | Hiçbir şey yapma, bekle |
| `< 0` (blocking) | Gerçek hata | `eState := eFault` |

## Pratikte Nasıl Kullanılır

### Yeni Bir TCP Cihazı Entegrasyon Kontrol Listesi

**Adım 1 — Cihazı Tanı (Başlamadan Önce)**

```
□ 1. Cihaz dökümanını oku: TCP Server mi, Client mi?
□ 2. Port numarası?
□ 3. Protokol: ASCII mi, Binary mi?
□ 4. Bağlantı: Kalıcı mı, mesaj başına mı?
□ 5. Bilmiyorsan: nc (netcat) ile bağlan, mesaj izle
         nc <cihaz_ip> <port>
         Cihaz bir şey yapınca terminale ne geliyor? → Protokol bu.
```

**Adım 2 — Protokol Çerçevesine Karar Ver**

```
ASCII + satır sonu (\r\n):
  → Delimiter-based framing: \r\n bulana kadar buffer'la
  → Örnek: Barcode okuyucu "DATA\r\n"

Binary + bilinen uzunluk:
  → Sabit-uzunluk framing: her recv N byte bekle
  → Örnek: Sensör her 50ms 8 byte gönderir

Binary + değişken uzunluk:
  → Length-prefixed framing + SOH (03_custom_protocol_design.md şablonu)
  → PLC↔PLC veya kendi yazdığın server
```

**Adım 3 — CODESYS'te Uygula**

```
□ 6. Library Manager → SysSock ekle
□ 7. FB_TcpClient veya FB_TcpServer oluştur (02_codesys_implementation.md şablonu)
□ 8. Task_Background oluştur (Prio 10-15, Freewheeling veya 100ms Cyclic)
□ 9. connect() çağrısını Task_Background'da yap — Task_Control'e koyma
□ 10. GVL_TCP oluştur: xConnected, aRxBuffer, xSendTrigger, nTxLen, pTxData
□ 11. FB_ProtocolDecoder (akümülatör + state machine) ekle
□ 12. Task_Control → GVL_TCP üzerinden veriyi kullan
□ 13. Python test istemcisiyle (03_custom_protocol_design.md) uçtan uca doğrula
□ 14. Heartbeat + timeout mekanizması ekle
```

**Adım 4 — Üretime Geçmeden Önce**

```
□ 15. SO_REUSEADDR ayarlı mı? (Restart sonrası bind hatası önler)
□ 16. SO_KEEPALIVE açık mı? (Phantom bağlantı tespiti)
□ 17. Bağlantı kopunca otomatik yeniden bağlanma var mı?
□ 18. Buffer overflow koruması var mı?
□ 19. Checksum hatası → Senkronizasyon kurtarma mı?
□ 20. Wireshark ile canlı trafik doğrulandı mı?
```

### Tipik Mimari Şema (PLC Client + Cihaz Server)

```
┌──────────────────────────────────────────────────────────────────┐
│  CODESYS PLC                                                     │
│                                                                  │
│  Task_Control (10ms, Prio:2)                                     │
│  ┌────────────────────────────┐                                  │
│  │ Kontrol mantığı            │                                  │
│  │ GVL_TCP.aRxBuffer → işle  │                                  │
│  │ GVL_TCP.xSendTrigger := 1 │                                  │
│  └────────────────────────────┘                                  │
│              │ GVL_TCP (paylaşılan değişkenler)                  │
│              ▼                                                   │
│  Task_Background (Freewheeling, Prio:10)                         │
│  ┌────────────────────────────┐                                  │
│  │ FB_TcpClient               │                                  │
│  │  ├─ eDisconnected          │                                  │
│  │  ├─ eConnecting [BLOCKING] │──── connect() ──►┐               │
│  │  ├─ eConnected             │                  │               │
│  │  ├─ eSending ─────────────►│──── send() ─────►│  TCP/IP LAN  │
│  │  └─ eReceiving ◄───────────│◄─── recv() ──────│              │
│  │                            │                  │               │
│  │ FB_ProtocolDecoder         │                  │               │
│  │  ├─ eWaitSOH               │       ┌──────────┘               │
│  │  ├─ eReadHeader            │       │ Cihaz (TCP Server)       │
│  │  └─ eReadData → xMsgReady │       │  Port: 10000-20000        │
│  └────────────────────────────┘       └──────────────────────────┘
└──────────────────────────────────────────────────────────────────┘
```

## Sık Yapılan Hatalar

### Hata 1: connect() Task_Control'de — Watchdog Tetikleyicisi

```
Semptom: Hedef cihaz erişilemez veya geç yanıt veriyor
         → Task_Control 10-20 saniye donuyor → Watchdog → Tüm motorlar duruyor.

Neden: SysSockConnect her zaman blocking — non-blocking moda alınan
       socket'ta bile bu istisna geçerli.

Çözüm: FB_TcpClient'ı Task_Background (Prio:10, Freewheeling) içinde çalıştır.
       Task_Control yalnızca GVL üzerinden xConnected ve aRxBuffer'ı okur.
```

### Hata 2: recv() = 0 ile recv() < 0 Karıştırmak

```iecst
(* ❌ Yanlış: Her iki durumu hata sayar *)
IF SysSockRecv(...) <= 0 THEN
    eState := eDisconnected;
END_IF

(* ✅ Doğru: Üç durum ayrı ayrı ele alınır *)
nRcv := SysSockRecv(...);
IF nRcv > 0 THEN
    (* Veri alındı, işle *)
ELSIF nRcv = 0 THEN
    (* EOF: Karşı taraf kapattı → yeniden bağlan *)
    eState := eDisconnected;
END_IF
(* nRcv < 0: Non-blocking, veri yok → normal, devam et *)
```

### Hata 3: SO_REUSEADDR Eksikliği — 4 Dakika Bekleme

```
Semptom: PLC veya server restart sonrası SysSockBind hata veriyor.
         ~4 dakika sonra kendiliğinden düzelir.

Neden: TCP TIME_WAIT — OS eski bağlantıyı 2-4 dakika tutar.

Çözüm: SysSockSetOption → SO_REUSEADDR → 1
        Bind'DAN ÖNCE ayarlanmalı. SysSockCreate'in hemen ardından.
```

### Hata 4: Her Mesaj İçin Yeni TCP Bağlantısı

```
Semptom: 100ms polling döngüsünde cihaz bağlantı kuyruğu doluyor.
         Cihaz yavaş yanıt vermeye başlıyor veya bağlantıyı reddediyor.

Neden: Her döngüde SYN-SYN/ACK-ACK-FIN-FIN/ACK: 6 paket overhead.

Çözüm: Bir kez bağlan, sürekli kullan (persistent connection).
        FB_TcpClient eConnected durumunda kalır, xEnable = TRUE sürece bağlantıyı korur.
```

### Hata 5: Akümülatör Buffer Olmadan Direkt recv() Kullanmak

```
Semptom: Bazen mesaj eksik geliyor, bazen iki mesaj birleşiyor gibi görünüyor.

Neden: TCP stream davranışı — send(100 byte) → recv() 30+70 byte gelebilir.

Çözüm: FB_ReceiveBuffer veya FB_ProtocolDecoder ile akümülatör buffer kullan.
        Tam mesaj gelene kadar buffer'a ekle, SOH+LENGTH+CKSUM ile doğrula, sonra işle.
```

### Hata 6: Socket Handle Sızdırma

```iecst
(* ❌ Hata yolunda socket kapatılmıyor — handle sızıyor *)
hSocket := SysSockCreate(...);
IF SysSockBind(...) <> RTS_S_OK THEN
    eState := eFault;  (* hSocket açık kalıyor! *)
END_IF

(* ✅ Her hata yolunda kapat *)
IF SysSockBind(...) <> RTS_S_OK THEN
    SysSockClose(hSocket, ADR(iecResult));
    hSocket := RTS_INVALID_HANDLE;
    eState := eFault;
END_IF
```

### Hata 7: Checksum'ı Yalnızca DATA Üzerinden Hesaplamak

```
Yanlış: XOR yalnızca DATA byte'larına uygulanıyor.
Doğru:  XOR hesabı SOH + VER + MSG + LENGTH + DATA tamamına uygulanmalı.

Verification kontrolü:
  Tüm frame byte'larının XOR'u (CHECKSUM dahil) = 0 olmalı.
  Bu sıfır sonucu frame bütünlüğünü doğrular.
```

## Ne Zaman Ham TCP Socket Kullanılır

### Kullan

```
✓ Karşı taraf Modbus TCP, OPC UA, MQTT'yi desteklemiyor
✓ Legacy cihaz: Barcode okuyucu, eski SCADA, özel ölçüm cihazı, robot kontrolcü
✓ Üretici özel binary protokolü tanımlıyor
✓ Büyük binary veri (görüntü, dalga şekli) — standart protokol overhead'ı istenmiyor
✓ İki PLC arasında özel, düşük gecikmeli köprü
✓ Mevcut legacy sistemin protokolüne adapte olmak zorundasın
```

### Kullanma

```
✗ Karşı taraf Modbus TCP destekliyorsa → Modbus TCP kullan
✗ Karşı taraf OPC UA destekliyorsa → OPC UA kullan
✗ Cihaz RS-232/RS-485 seri port kullanıyorsa → SysCom (seri haberleşme) kullan
✗ Güvenlik (SIL) gereksinimleri varsa → Ham TCP yetmez, TLS + authenticated protokol
✗ Ekip içinde belgelenmiş standart protokol varsa → Oraya yatırım yap
```

### Karar Ağacı

```
Entegre edilecek cihaz →
    Modbus TCP destekliyor?         → Evet → Modbus TCP
    OPC UA destekliyor?             → Evet → OPC UA
    MQTT destekliyor?               → Evet → MQTT
    RS-232/RS-485 kulllanıyor?      → Evet → SysCom (seri)
    Özel TCP protokolü konuşuyor?   → Evet → Ham TCP Socket (bu klasör)
    Protokolü bilinmiyor?           → Netcat ile bağlan, izle, tersine mühendislik uygula
```

## Gerçek Proje Notları

**Not 1 — Netcat ile Protokol Keşfi**  
Yeni bir barkod okuyucu entegre edilecekti. Üretici belgesi "TCP server, port 4001" diyordu; protokol detayı yoktu. `nc <IP> 4001` ile bağlanıldı. Okuyucu bir şey taradığında terminale geldi: `<barcode_value>\r\n`. Protokol bu kadardı. CODESYS kodu: Connect → recv loop → `\r\n` bulana kadar buffer → barcode string. Wireshark ve protocol dökümantasyonu olmadan bile 30 dakikada entegrasyon bitti.

**Not 2 — Phantom Bağlantı ve Keep-Alive**  
Gece mesai olmayan bir fabrikada sabah SCADA PLC'ye bağlanamıyordu. Araştırma: PLC tarafında bağlantı "xConnected = TRUE" görünüyordu ama NAT gateway gece 30 dakika sessizlik sonrası session'ı kapatmıştı. recv() = -1 (non-blocking, normal), send() = -1 (gerçek hata). Ayırt etmek güçtü. Çözüm: SO_KEEPALIVE + 60 saniyede probe + uygulama katmanı heartbeat (30 saniyede 2-byte ping). Sabah bağlantı sorunu tamamen ortadan kalktı.

**Not 3 — connect() Watchdog Felaketi**  
İlk CODESYS TCP uygulamasında FB_TcpClient Task_Control (10ms, Prio:2) içindeydi. Hedef cihaz ağda yoktu. SysSockConnect 20 saniye blocking çalıştı; Task_Control dondu; tüm motorlar watchdog ile durdu. Gerçek üretim ortamında. Derhal Freewheeling task'a taşındı. Artık bağlantı kurulamazsa Task_Control etkilenmiyor.

**Not 4 — SO_REUSEADDR Olmadan 4 Dakika Beklemek**  
Test aşamasında server PLC sık sık restart ediliyordu. Her restart'tan sonra SysSockBind hata verdi; yaklaşık 4 dakika sonra tekrar çalıştı. TCP TIME_WAIT mekanizması. SO_REUSEADDR eklendikten sonra anında bind oluyor. Bu seçenek şimdi tüm TCP server şablonlarının standart parçası.

**Not 5 — İlk Protokolde SOH Yoktu**  
İlk özel protokolde SOH yoktu; doğrudan VER+MSG+LENGTH ile başlıyordu. Bağlantı kesintisi sonrası buffer'daki yarım veri yüzünden parser bozuldu; anlamsız mesajlar işlendi, hatalı komutlar çalıştı. SOH (0x01) eklendi ve senkronizasyon kurtarma state machine'i yazıldı. Artık bağlantı kopunca buffer temizleniyor, SOH aranıyor, geçerli header bulunamayan N byte sonrası yeniden bağlanma tetikleniyor.

**Not 6 — Protokol Versiyonlama Değerini Kanıtladı**  
V1 MSG_DATA 8 byte'tı; V2'de 12 byte'a çıktı. Eski V1 istemciler hâlâ bağlıydı. VER alanı sayesinde: V2 sunucu, VER=1 gelen istemcilere 8-byte yanıt, VER=2'ye 12-byte yanıt verdi. 6 ay boyunca iki versiyon aynı anda sorunsuz çalıştı. Versiyonsuz bir protokolde bu geçiş sistemi durdurmadan yapılamazdı.

**Not 7 — CRC-16 Geçişinin Değeri**  
Başlangıçta tek byte XOR checksum yeterliydi. EMI'dan etkilenen bir kablo hatalı veri gönderdi; XOR yakalamadı, hatalı komut işlendi. CRC-16'ya geçildi. Fabrika ortamında: Güçlü elektromanyetik gürültü kaynakları (motor sürücüler, kaynak makineleri) varsa CRC-16 tercih et.

## İlgili Konular

```
knowledge/protocols/tcp-socket/     ← Şu an buradasınız
├── 01_basics.md                    → TCP stream modeli, kalıcı bağlantı, keep-alive
├── 02_codesys_implementation.md    → SysSock API, FB_TcpClient, FB_TcpServer, task seçimi
├── 03_custom_protocol_design.md    → Framing, encoder/decoder, Python test istemcisi
└── _synthesis.md                   → Bu belge

Bir üst bağlam:
knowledge/protocols/
├── modbus-tcp/                     → TCP üzerine kurulu standart saha bus protokolü
└── opc-ua/                         → TCP üzerine kurulu zengin veri modeli + güvenlik

CODESYS tarafı:
knowledge/codesys/networking/
└── 03_tcp_socket.md                → SysSock özet implementasyon, hızlı başlangıç

knowledge/codesys/programming/
├── 03_function_blocks.md           → FB state machine tasarımı
└── 05_error_handling.md            → Hata yönetimi prensipleri

Araçlar:
  netcat (nc)   → nc -l 9000 (server) veya nc <IP> 9000 (client) — Hızlı test
  Wireshark     → TCP stream analizi, hex view ile byte inceleme
  socat         → Gelişmiş socket köprüsü
  Python socket → Test server/client, protokol doğrulama (03_custom_protocol_design.md şablonu)
  pytest        → Protokol encoder/decoder unit testleri
```
