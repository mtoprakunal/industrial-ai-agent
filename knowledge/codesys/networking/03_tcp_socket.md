---
KONU        : CODESYS SysSock ile TCP Socket Programlama
KATEGORİ    : codesys
ALT_KATEGORI: networking
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://brightersidetech.com/tcp-socket-client-implementation-in-codesys/"
    başlık: "BrighterSideTech — TCP Socket Client in CODESYS"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Runtime/thread/1bd5690115/"
    başlık: "CODESYS Forge — TCP Socket Communication"
    güvenilirlik: topluluk
  - url: "https://forum.codesys.com/viewtopic.php?t=7935"
    başlık: "CODESYS Forum — TCP Server Code"
    güvenilirlik: topluluk
  - url: "https://www.researchgate.net/publication/264081315"
    başlık: "ResearchGate — TCP Server and Client with CODESYS SysSock"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_opcua_server.md"
    ilişki: alternatif
  - konu: "02_modbus_slave.md"
    ilişki: alternatif
  - konu: "04_mqtt_client.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "TCP/IP temel kavramları: socket, bind, listen, accept, connect, send, recv"
  - "CODESYS Function Block geliştirme (programming/03_function_blocks.md)"
  - "Pointer ve ADR() kullanımı ST'de"
ÇELİŞKİLER :
  - kaynak: "SysSockConnect — blocking mode"
    konu: "SysSockConnect her zaman blocking modda çalışır; SysSockIoctl bu fonksiyonu etkilemez"
    çözüm: >
      SysSockConnect, non-blocking ayarlanmış socket'ta dahi blocking çalışır.
      Bu, bağlantı kurulana kadar task'ın durması demektir. Freewheeling task
      veya düşük öncelikli task tercih edilmeli. Alternatif: Bağlantıyı ayrı
      bir FB içinde state machine ile yönet ve timeout mekanizması ekle.
  - kaynak: "SysSockRecv return value = 0"
    konu: "0 dönüş değeri farklı şeylere işaret edebilir"
    çözüm: >
      SysSockRecv = 0: Bağlantı karşı tarafça düzgün kapatıldı.
      SysSockRecv = -1 veya error: Gerçek iletişim hatası.
      Bu farkı kodda ayırt etmek gerekir; her ikisi de "veri gelmedi"
      olarak ele alınırsa sorun maskelenir.
---

## Özün Ne

CODESYS'in yerleşik Modbus, OPC UA ve MQTT kütüphaneleri pek çok senaryoyu karşılar. Ancak karşı taraf özel bir protokol kullanıyorsa (barcode okuyucu, kamera sistemi, eski SCADA, özel ölçüm cihazı), tek yol ham TCP socket programlamadır. `SysSock` kütüphanesi, CODESYS'e C'deki Berkeley Socket API'sine benzer bir arayüz sağlar. Düşük seviyeli bu API, dikkat gerektiren birkaç noktası olmakla birlikte PLC'ye tam ağ programlama özgürlüğü tanır.

## Nasıl Çalışır

### SysSock Kütüphanesi

```
Kütüphane adı: SysSock (veya SysSocket23 bazı versiyonlarda)
Library Manager'a ekle: "SysSock" veya "syssocket" araması
Namespace: syssocket veya SYSSOCKET
```

**Temel Fonksiyonlar:**

| Fonksiyon | Açıklama | Dönüş |
|---|---|---|
| `SysSockCreate` | Socket oluştur | RTS_IEC_HANDLE |
| `SysSockConnect` | Sunucuya bağlan (Client) | RTS_IEC_RESULT |
| `SysSockBind` | Porta bağla (Server) | RTS_IEC_RESULT |
| `SysSockListen` | Bağlantı dinle (Server) | RTS_IEC_RESULT |
| `SysSockAccept` | Bağlantı kabul et (Server) | RTS_IEC_HANDLE |
| `SysSockSend` | Veri gönder | DINT (gönderilen byte) |
| `SysSockRecv` | Veri al | DINT (alınan byte) |
| `SysSockClose` | Socket kapat | RTS_IEC_RESULT |
| `SysSockShutdown` | Bağlantıyı nazikçe kapat | RTS_IEC_RESULT |
| `SysSockIoctl` | Non-blocking moda geç | RTS_IEC_RESULT |
| `SysSockInetAddr` | IP string → UDINT | UDINT |
| `SysSockHtons` | Host byte order → Network byte order | WORD |

### TCP Client State Machine

TCP client bağlantısı bir state machine olarak modellenmeli:

```
eDisconnected → eConnecting → eConnected → eSending → eReceiving
                    │                           │
                    └── Bağlantı başarısız ──── ┘ → eDisconnected
```

### Non-Blocking Socket

CODESYS'te socket varsayılan olarak **blocking** modda çalışır. `SysSockRecv` çağrısı veri gelene kadar task'ı dondurur. Bunu önlemek için socket non-blocking moda alınmalıdır:

```iecst
VAR
    diNonBlockingMode : DINT := 1;
    iecResult : RTS_IEC_RESULT;
END_VAR

(* Non-blocking moda al — socket oluşturulduktan hemen sonra *)
iecResult := syssocket.SysSockIoctl(
    hSocket  := iecSocketId,
    diCode   := SYSSOCKET.FIONBIO,    (* Non-blocking komut kodu *)
    pdiParam := ADR(diNonBlockingMode),
    pResult  := ADR(iecResult)
);
(* NOT: SysSockConnect bu ayardan ETKILENMEZ — connect her zaman blocking! *)
```

Non-blocking modda:
- `SysSockRecv`: Veri yoksa hemen -1 döner (WSAEWOULDBLOCK hata kodu)
- `SysSockSend`: Tampon doluysa hemen -1 döner
- `SysSockAccept`: Bağlantı yoksa hemen -1 döner
- `SysSockConnect`: **Hâlâ blocking** — özel davranış

## Pratikte Nasıl Kullanılır

### TCP Client FB — Tam Implementasyon

```iecst
FUNCTION_BLOCK FB_TcpClient
VAR_INPUT
    xEnable        : BOOL;              (* FALSE → bağlantıyı kapat *)
    sServerIP      : STRING(15) := '192.168.1.200';
    nServerPort    : UINT := 8080;
    pTxData        : POINTER TO BYTE;  (* Gönderilecek veri pointer *)
    nTxLen         : UDINT;            (* Gönderilecek byte sayısı *)
    xSendTrigger   : BOOL;             (* Yükselen kenar → gönder *)
    tConnectTimeout: TIME := T#5S;
    tReceiveTimeout: TIME := T#2S;
END_VAR
VAR_OUTPUT
    xConnected     : BOOL;
    xDataReceived  : BOOL;
    aRxBuffer      : ARRAY[0..255] OF BYTE;  (* Alınan veri *)
    nRxLen         : UDINT;
    xFault         : BOOL;
    sFaultMsg      : STRING(80);
    eState         : E_TcpState;
END_VAR
VAR
    iecSocketId    : syssocket.RTS_IEC_HANDLE := RTS_INVALID_HANDLE;
    iecResult      : syssocket.RTS_IEC_RESULT;
    sockAddr       : syssocket.SOCKADDRESS;
    diNonBlock     : DINT := 1;
    
    nSentBytes     : DINT;
    nRecvBytes     : DINT;
    
    tConnectTimer  : TON;
    tRecvTimer     : TON;
    fbSendEdge     : R_TRIG;
    
    xSendPending   : BOOL;
END_VAR

fbSendEdge(CLK := xSendTrigger);
IF fbSendEdge.Q THEN
    xSendPending := TRUE;
END_IF

CASE eState OF

    eTcp_Disconnected:
        xConnected := FALSE;
        iecSocketId := RTS_INVALID_HANDLE;
        
        IF xEnable THEN
            (* Socket oluştur *)
            iecSocketId := syssocket.SysSockCreate(
                iAddressFamily := syssocket.SOCKET_AF_INET,
                iType          := syssocket.SOCKET_STREAM,
                iProtocol      := syssocket.SOCKET_IPPROTO_TCP,
                pResult        := ADR(iecResult)
            );
            
            IF iecSocketId = RTS_INVALID_HANDLE THEN
                xFault    := TRUE;
                sFaultMsg := 'Socket creation failed';
                eState    := eTcp_Fault;
            ELSE
                (* Non-blocking moda al (recv için) *)
                syssocket.SysSockIoctl(hSocket:=iecSocketId, diCode:=SYSSOCKET.FIONBIO,
                                       pdiParam:=ADR(diNonBlock), pResult:=ADR(iecResult));
                
                (* SOCKADDRESS yapısını doldur *)
                sockAddr.sin_family := syssocket.SOCKET_AF_INET;
                sockAddr.sin_port   := syssocket.SysSockHtons(nServerPort);
                sockAddr.sin_addr   := syssocket.SysSockInetAddr(sServerIP, ADR(sockAddr.sin_addr));
                
                tConnectTimer(IN := FALSE);
                eState := eTcp_Connecting;
            END_IF
        END_IF

    eTcp_Connecting:
        tConnectTimer(IN := TRUE, PT := tConnectTimeout);
        
        (* SysSockConnect BLOCKING — bu çağrı tamamlanana kadar task bekler! *)
        (* Freewheeling task veya düşük öncelikli task önerilir *)
        iecResult := syssocket.SysSockConnect(
            hSocket        := iecSocketId,
            pSockAddr      := ADR(sockAddr),
            diSockAddrSize := SIZEOF(sockAddr)
        );
        
        IF iecResult = RTS_S_OK THEN
            xConnected := TRUE;
            xFault     := FALSE;
            tConnectTimer(IN := FALSE);
            eState := eTcp_Connected;
        ELSIF tConnectTimer.Q THEN
            syssocket.SysSockClose(hSocket := iecSocketId, pResult := ADR(iecResult));
            iecSocketId := RTS_INVALID_HANDLE;
            xFault    := TRUE;
            sFaultMsg := CONCAT('Connect timeout to ', sServerIP);
            eState := eTcp_Fault;
        END_IF

    eTcp_Connected:
        xConnected := TRUE;
        
        IF NOT xEnable THEN
            eState := eTcp_Closing;
        ELSIF xSendPending THEN
            xSendPending := FALSE;
            eState := eTcp_Sending;
        ELSE
            (* Periyodik receive kontrolü *)
            nRecvBytes := syssocket.SysSockRecv(
                hSocket     := iecSocketId,
                pbyBuffer   := ADR(aRxBuffer),
                diBufferSize:= SIZEOF(aRxBuffer),
                diFlags     := 0,
                pResult     := ADR(iecResult)
            );
            
            IF nRecvBytes > 0 THEN
                nRxLen := DINT_TO_UDINT(nRecvBytes);
                xDataReceived := TRUE;
            ELSIF nRecvBytes = 0 THEN
                (* Bağlantı karşı tarafça kapatıldı *)
                syssocket.SysSockClose(hSocket := iecSocketId, pResult := ADR(iecResult));
                xConnected := FALSE;
                sFaultMsg  := 'Connection closed by remote';
                eState := eTcp_Disconnected;
            END_IF
            (* nRecvBytes < 0: Veri yok (non-blocking) — normal, devam et *)
        END_IF

    eTcp_Sending:
        nSentBytes := syssocket.SysSockSend(
            hSocket     := iecSocketId,
            pbyBuffer   := pTxData,
            diBufferSize:= DINT(nTxLen),
            diFlags     := 0,
            pResult     := ADR(iecResult)
        );
        
        IF nSentBytes < 0 THEN
            sFaultMsg := 'Send failed';
            xFault    := TRUE;
            eState    := eTcp_Fault;
        ELSE
            eState := eTcp_Connected;
        END_IF

    eTcp_Closing:
        syssocket.SysSockShutdown(hSocket := iecSocketId,
                                   diHow := syssocket.SOCKET_SD_BOTH,
                                   pResult := ADR(iecResult));
        syssocket.SysSockClose(hSocket := iecSocketId, pResult := ADR(iecResult));
        iecSocketId := RTS_INVALID_HANDLE;
        xConnected := FALSE;
        eState := eTcp_Disconnected;

    eTcp_Fault:
        IF iecSocketId <> RTS_INVALID_HANDLE THEN
            syssocket.SysSockClose(hSocket := iecSocketId, pResult := ADR(iecResult));
            iecSocketId := RTS_INVALID_HANDLE;
        END_IF
        xConnected := FALSE;
        IF NOT xEnable THEN
            xFault := FALSE;
            sFaultMsg := '';
            eState := eTcp_Disconnected;
        END_IF
        (* xEnable tekrar TRUE edilirse Disconnected → Connecting döngüsü başlar *)

    ELSE:
        eState := eTcp_Fault;
END_CASE

xDataReceived := (nRecvBytes > 0);
```

### TCP Server FB — Basit Implementasyon

```iecst
FUNCTION_BLOCK FB_TcpServer
VAR_INPUT
    xEnable    : BOOL;
    nListenPort: UINT := 9000;
    nMaxClients: INT  := 1;   (* Basit single-client server *)
END_VAR
VAR_OUTPUT
    xClientConnected : BOOL;
    aRxBuffer        : ARRAY[0..511] OF BYTE;
    nRxLen           : UDINT;
    xFault           : BOOL;
    eState           : E_TcpServerState;
END_VAR
VAR
    hListenSocket    : syssocket.RTS_IEC_HANDLE := RTS_INVALID_HANDLE;
    hClientSocket    : syssocket.RTS_IEC_HANDLE := RTS_INVALID_HANDLE;
    iecResult        : syssocket.RTS_IEC_RESULT;
    listenAddr       : syssocket.SOCKADDRESS;
    clientAddr       : syssocket.SOCKADDRESS;
    clientAddrSize   : DINT := SIZEOF(clientAddr);
    diNonBlock       : DINT := 1;
    diReuse          : DINT := 1;
    nRecvBytes       : DINT;
END_VAR

CASE eState OF

    eTcpSrv_Idle:
        IF xEnable THEN
            (* Listen socket oluştur *)
            hListenSocket := syssocket.SysSockCreate(syssocket.SOCKET_AF_INET,
                              syssocket.SOCKET_STREAM, syssocket.SOCKET_IPPROTO_TCP, ADR(iecResult));
            IF hListenSocket = RTS_INVALID_HANDLE THEN
                xFault := TRUE; eState := eTcpSrv_Fault; RETURN;
            END_IF
            
            (* Portu yeniden kullanılabilir yap (restart sonrası TIME_WAIT sorununu önler) *)
            syssocket.SysSockSetOption(hListenSocket, syssocket.SOCKET_SOL, 
                                        syssocket.SOCKET_SO_REUSEADDR,
                                        ADR(diReuse), SIZEOF(diReuse), ADR(iecResult));
            
            (* Non-blocking moda al *)
            syssocket.SysSockIoctl(hListenSocket, SYSSOCKET.FIONBIO, ADR(diNonBlock), ADR(iecResult));
            
            (* Bind: Tüm arayüzlerden kabul et *)
            listenAddr.sin_family := syssocket.SOCKET_AF_INET;
            listenAddr.sin_port   := syssocket.SysSockHtons(nListenPort);
            listenAddr.sin_addr   := 0;   (* INADDR_ANY — tüm arayüzler *)
            
            syssocket.SysSockBind(hListenSocket, ADR(listenAddr), SIZEOF(listenAddr), ADR(iecResult));
            syssocket.SysSockListen(hListenSocket, nMaxClients, ADR(iecResult));
            
            eState := eTcpSrv_Listening;
        END_IF

    eTcpSrv_Listening:
        (* Non-blocking accept — bağlantı yoksa hemen -1 döner *)
        hClientSocket := syssocket.SysSockAccept(
            hSocket       := hListenSocket,
            pSockAddr     := ADR(clientAddr),
            pdiSockAddrSize := ADR(clientAddrSize),
            pResult       := ADR(iecResult)
        );
        
        IF hClientSocket <> RTS_INVALID_HANDLE THEN
            xClientConnected := TRUE;
            eState := eTcpSrv_ClientConnected;
        END_IF
        
        IF NOT xEnable THEN eState := eTcpSrv_Closing; END_IF

    eTcpSrv_ClientConnected:
        nRecvBytes := syssocket.SysSockRecv(hClientSocket, ADR(aRxBuffer),
                                              SIZEOF(aRxBuffer), 0, ADR(iecResult));
        IF nRecvBytes > 0 THEN
            nRxLen := DINT_TO_UDINT(nRecvBytes);
        ELSIF nRecvBytes = 0 THEN
            (* Client bağlantıyı kapattı *)
            syssocket.SysSockClose(hClientSocket, ADR(iecResult));
            hClientSocket    := RTS_INVALID_HANDLE;
            xClientConnected := FALSE;
            eState := eTcpSrv_Listening;
        END_IF
        
        IF NOT xEnable THEN eState := eTcpSrv_Closing; END_IF

    eTcpSrv_Closing:
        IF hClientSocket <> RTS_INVALID_HANDLE THEN
            syssocket.SysSockClose(hClientSocket, ADR(iecResult));
        END_IF
        IF hListenSocket <> RTS_INVALID_HANDLE THEN
            syssocket.SysSockClose(hListenSocket, ADR(iecResult));
        END_IF
        hClientSocket := RTS_INVALID_HANDLE;
        hListenSocket := RTS_INVALID_HANDLE;
        xClientConnected := FALSE;
        eState := eTcpSrv_Idle;

    eTcpSrv_Fault:
        IF NOT xEnable THEN
            xFault := FALSE;
            eState := eTcpSrv_Idle;
        END_IF
END_CASE
```

### Özel Protokol Tasarımı

Ham TCP üzerinde veri gönderirken mesaj sınırlarını belirlemek için protokol çerçevesi gerekir:

```
Basit protokol çerçevesi (framing):

┌────────┬────────┬─────────────────┬──────────┐
│ SOH    │ Length │ Payload         │ Checksum │
│ 1 byte │ 2 byte │ N byte          │ 1 byte   │
└────────┴────────┴─────────────────┴──────────┘
SOH = 0x01 (Start of Header)
Length = Payload uzunluğu (Big Endian WORD)
Checksum = Payload byte'larının XOR'u
```

```iecst
(* Protokol çerçevesi oluşturma *)
FUNCTION FC_BuildFrame : UDINT
VAR_INPUT
    pPayload    : POINTER TO BYTE;
    nPayloadLen : UDINT;
    pBuffer     : POINTER TO BYTE;   (* Çıkış buffer'ı — en az nPayloadLen+4 byte *)
END_VAR
VAR
    i           : UDINT;
    nChecksum   : BYTE;
    pBuf        : POINTER TO BYTE;
END_VAR

pBuf := pBuffer;
pBuf^ := 16#01;                              (* SOH *)
(pBuf+1)^ := BYTE(SHR(nPayloadLen, 8));      (* Length High *)
(pBuf+2)^ := BYTE(nPayloadLen AND 16#FF);    (* Length Low *)

nChecksum := 0;
FOR i := 0 TO nPayloadLen - 1 DO
    (pBuf+3+i)^ := (pPayload+i)^;            (* Payload kopyala *)
    nChecksum := nChecksum XOR (pPayload+i)^;
END_FOR

(pBuf+3+nPayloadLen)^ := nChecksum;         (* Checksum *)
FC_BuildFrame := nPayloadLen + 4;            (* Toplam frame boyutu *)
```

## Örnekler

### Örnek 1: Barcode Okuyucu Entegrasyonu

```iecst
(* Barcode okuyucu TCP server'a bağlı client — gerçek proje *)
PROGRAM PRG_BarcodeReader
VAR
    fbTcpClient    : FB_TcpClient;
    sBarcode       : STRING(64);
    xNewBarcode    : BOOL;
    aRxBuf         : ARRAY[0..63] OF BYTE;
END_VAR

fbTcpClient(
    xEnable    := GVL_State.xSystemOK,
    sServerIP  := '192.168.1.150',
    nServerPort:= 4001
);

IF fbTcpClient.xDataReceived THEN
    (* Barcode null-terminated ASCII string *)
    sBarcode := '';
    (* Byte array → STRING dönüşümü *)
    MEMCPY(ADR(sBarcode), ADR(fbTcpClient.aRxBuffer), MIN(fbTcpClient.nRxLen, 63));
    xNewBarcode := TRUE;
    
    GVL_Production.sLastScannedBarcode := sBarcode;
    GVL_Production.xBarcodeReady       := TRUE;
END_IF
```

### Örnek 2: Bağlantı Kopması ve Otomatik Yeniden Bağlanma

State machine'deki `eTcp_Disconnected` → `eTcp_Connecting` döngüsü otomatik yeniden bağlanmayı sağlar:

```iecst
(* xEnable = TRUE kalırsa Disconnected durumunda hemen yeniden bağlanmaya çalışır *)
(* Aşırı hızlı retry'dan korunmak için cooldown ekle: *)

VAR
    tRetryTimer : TON;
    bRetryCooldown : BOOL;
END_VAR

IF fbTcpClient.eState = eTcp_Disconnected AND NOT bRetryCooldown THEN
    tRetryTimer(IN := TRUE, PT := T#5S);  (* 5sn bekle *)
    IF tRetryTimer.Q THEN
        tRetryTimer(IN := FALSE);
        bRetryCooldown := FALSE;
        (* fbTcpClient.xEnable zaten TRUE — state machine bağlanmaya başlar *)
    END_IF
    bRetryCooldown := NOT tRetryTimer.Q;
END_IF
```

## Sık Yapılan Hatalar

### Hata 1: SysSockConnect'in Blocking Olduğunu Unutmak

```
Semptom: Yüksek öncelikli task SysSockConnect çağrısında donuyor.
         Tüm sistem askıda gibi görünüyor.
Neden  : SysSockConnect non-blocking socket'ta bile blocking çalışır.
         Bağlantı kurulamıyorsa OS timeout'una (genellikle 20-75sn!) kadar bekler.
Çözüm  : TCP client'ı yüksek öncelikli task'ta çağırma.
          Freewheeling task veya düşük öncelikli task'a (Prio:10+) koy.
          Alternatif: connect timeout için ayrı bir mekanizma kullan.
```

### Hata 2: Socket Handle Sızdırmak (Leak)

```iecst
(* ❌ YANLIŞ — Hata durumunda socket kapatılmıyor *)
iecSocketId := syssocket.SysSockCreate(...);
IF iecResult <> RTS_S_OK THEN
    eState := eTcp_Fault;  (* Socket hâlâ açık! *)
    RETURN;
END_IF

(* ✅ DOĞRU *)
IF iecResult <> RTS_S_OK THEN
    syssocket.SysSockClose(iecSocketId, ADR(iecResult));  (* Kapat *)
    iecSocketId := RTS_INVALID_HANDLE;
    eState := eTcp_Fault;
    RETURN;
END_IF
```

### Hata 3: SysSockRecv = 0 ve -1 Farkını Gözetmemek

```iecst
(* ❌ YANLIŞ — İkisini aynı ele almak *)
IF syssocket.SysSockRecv(...) <= 0 THEN
    eState := eTcp_Disconnected;  (* -1 = Veri yok (non-blocking normal durum!) *)
END_IF

(* ✅ DOĞRU *)
nRet := syssocket.SysSockRecv(...);
IF nRet > 0 THEN
    (* Veri alındı — işle *)
ELSIF nRet = 0 THEN
    (* Bağlantı karşı tarafça kapatıldı *)
    eState := eTcp_Disconnected;
ELSIF nRet = -1 THEN
    (* Non-blocking: Veri yok — normal, devam et *)
    (* Veya gerçek hata — iecResult kontrol et *)
END_IF
```

### Hata 4: Büyük Buffer'ı Stack'te Tanımlamak

```iecst
(* ❌ YANLIŞ — Büyük lokal array stack taşmasına neden olabilir *)
PROGRAM PRG_TcpTest
VAR
    aLocalBuffer : ARRAY[0..65535] OF BYTE;  (* 64KB stack'te! *)
END_VAR

(* ✅ DOĞRU — Global veya FB VAR bölümünde tanımla *)
(* PROGRAM veya FB VAR bölümünde → statik bellek *)
FUNCTION_BLOCK FB_TcpServer
VAR
    aRxBuffer : ARRAY[0..4095] OF BYTE;   (* Statik bellek — OK *)
END_VAR
```

### Hata 5: SO_REUSEADDR Eksikliği

```
Semptom: PLC restart sonrası server socket port'a bind olamıyor.
         "Address already in use" hatası.
Neden  : TCP TIME_WAIT durumu — eski bağlantı henüz OS tarafından kapanmadı.
Çözüm  : Socket oluşturulduktan hemen sonra SO_REUSEADDR option'ını set et:
         SysSockSetOption(..., SOCKET_SO_REUSEADDR, 1)
         Bu seçenek, aynı port'u TIME_WAIT bitmeden yeniden kullanmaya izin verir.
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**TCP Socket Tercih Et:**
- Karşı taraf yalnızca özel protokol konuşuyor (barcode, kamera, ölçüm)
- Var olan legacy sisteme bağlanılması gerekiyor
- Standart protokol (Modbus, OPC UA) seçeneği yok
- Tam kontrol, özel framing ve hata yönetimi gerekiyor

**TCP Socket Tercih Etme:**
- Modbus, OPC UA veya MQTT yeterli → Bu kütüphaneler çok daha güvenilir ve bakımlı
- Hızlı entegrasyon gerekiyor → Ham socket geliştirmesi uzun sürer
- Gerçek zamanlılık kritik → TCP kendisi garantisiz gecikme sunar

## Gerçek Proje Notları

**Not 1 — SysSockConnect Donması**  
Yüksek öncelikli Task_Control (10ms, Prio:2) içinde SysSockConnect çağrıldı. Hedef IP erişilemez durumdaydı. OS timeout 75 saniye sürdü — bu süre boyunca tüm Task_Control çalışmadı, motorlar watchdog ile durdu. TCP client tüm mantığı Freewheeling task'a taşındıktan sonra sorun kalktı.

**Not 2 — Barcode Okuyucu Newline Karakteri**  
Barcode okuyucu her okumadan sonra `\r\n` gönderiyordu. Uygulama her recv'de tüm buffer'ı string olarak aldı. `\r\n` karakterlerini siferlediğimizde barcode doğru okundu. Ders: Özel protokollerde terminatör karakterlerine dikkat.

**Not 3 — SO_REUSEADDR Olmadan Restart Sorunu**  
Her PLC restart'ında server socket 2 dakika bind olamıyordu (TIME_WAIT). Production ortamında watchdog sonrası yeniden başlama sorunuydu. SO_REUSEADDR eklendikten sonra restart'tan 1-2 saniye içinde port hazır hale geldi.

**Not 4 — Multi-Client Server Karmaşıklığı**  
Birden fazla SCADA bağlantısı için multi-client TCP server yazılmaya çalışıldı. `fd_set` / `SysSockSelect` ile seçici bekleme implementasyonu çok karmaşık oldu ve hatalı davrandı. Alternatif çözüm: OPC UA'ya geçildi — built-in multi-client desteği ile sorun ortadan kalktı. Ders: Multi-client TCP server CODESYS'te gerçekten zor; standart protokol kullan.

**Not 5 — TCP "Mesaj" Değil "Akış" — Yarım Paket Tuzağı**  
Bir cihaz 100 byte'lık mesajlar gönderiyordu; geliştirici her `SysSockRecv`'in tam bir mesaj döndüreceğini varsaydı. Çoğu zaman çalıştı, ama yoğun anlarda recv bazen 60, bazen 140 byte döndürdü (iki mesajın parçası). Neden: TCP bir **byte akışıdır**, mesaj sınırı korumaz — gönderenin "bir send"i alıcıda birden fazla recv'e bölünebilir veya iki send tek recv'de birleşebilir (Nagle + TCP segmentasyon). Ders: Uygulama katmanında **framing** (uzunluk öneki veya terminatör) ile mesaj sınırını kendin belirle ve bir **birikim buffer'ı** (accumulator) tut; recv'leri buffer'a ekle, tam frame oluşunca işle. "1 recv = 1 mesaj" varsayımı en sinsi TCP hatasıdır.

**Not 6 — Nagle Algoritması ve Küçük Mesaj Gecikmesi**  
Küçük komut paketleri (birkaç byte) gönderilirken ~40ms gecikme gözlendi. Neden: TCP Nagle algoritması küçük paketleri biriktirip birleştirir (bant verimi için), bu da düşük-latency için gecikme yaratır. Çözüm: `TCP_NODELAY` socket option (`SysSockSetOption`) ile Nagle kapatıldı — küçük paketler anında gitti. Ders: İnteraktif/düşük-latency protokollerde TCP_NODELAY; yüksek-verim toplu transferde Nagle açık kalsın.

**Not 7 — Yarı-Açık Bağlantı (Half-Open) Tespiti**  
Karşı cihazın güç kablosu çekildiğinde PLC'nin socket'i "bağlı" kaldı — `recv` veri vermedi ama hata da dönmedi (FIN/RST gelmedi, kablo koptu). PLC saatlerce ölü bir bağlantıyı canlı sandı. Ders: TCP kendisi yarı-açık bağlantıyı hemen tespit etmez. Uygulama katmanında **heartbeat/keepalive** (periyodik ping + yanıt timeout) veya `SO_KEEPALIVE` socket option ekleyin; veri-yokluğu timeout'u ile ölü bağlantıyı proaktif kapatın.

## Edge Case'ler ve Sistem Limitleri

### TCP Akış Semantiği Edge Case'leri

```
Edge Case                          Davranış                  Koruma
─────────────────────────────────────────────────────────────────────
recv yarım mesaj döndürür          TCP akış, mesaj değil     framing + accumulator
iki mesaj tek recv'de birleşir     TCP segmentasyon          framing ile ayır
recv = 0                           karşı taraf düzgün kapattı bağlantıyı kapat
recv = -1 (non-blocking)           veri yok — NORMAL         devam et (hata değil)
recv = -1 + gerçek hata            iecResult kontrol et      bağlantıyı kapat
kablo koptu (FIN/RST yok)          yarı-açık, recv sessiz    heartbeat/keepalive
connect erişilemez IP'ye           OS timeout 20-75sn BLOCK  düşük öncelik task + timeout
```

### SysSock Handle ve Kaynak Sınırları

```
- Socket handle sızıntısı: her açılan socket kapatılmazsa OS fd limiti dolar →
  yeni socket açılamaz (genelde ~1024 fd). Her hata dalında SysSockClose şart.
- TIME_WAIT: kapatılan server socket portu ~2dk meşgul kalır → SO_REUSEADDR ile aş.
- Büyük buffer stack'te: 64KB+ lokal array stack overflow → FB/global VAR'da tut.
- Blocking connect: non-blocking socket'ta bile connect blocking (SP/platform farkı olabilir).
```

### Endian ve Hizalama

Ham byte buffer'dan struct'a `MEMCPY` ile veri çekerken: gönderen sistemin endian'ı ve struct padding'i (bkz. fundamentals/02 pack_mode) eşleşmeli. Network protokolleri genelde big-endian (network byte order); `SysSockHtons`/`Ntohs` ile dönüştür. `pack_mode 1` ile hizasız struct kullanırken bazı ARM platformlarında hizasız erişim exception'ı riski vardır.

## Optimizasyon

### Framing ve Buffer Yönetimi

```
- Birikim buffer'ı (accumulator): recv'leri ekle, tam frame oluşunca parse et,
  kalan kısmı buffer'da bırak. "1 recv = 1 mesaj" varsayma (Not 5).
- Uzunluk-önekli framing (length-prefixed), terminatör-tabanlıdan (newline) daha
  sağlam ve hızlıdır — payload'da terminatör çakışması olmaz.
- MEMCPY ile blok kopyala, byte-byte döngüden kat kat hızlı.
```

### Latency vs Verim: TCP_NODELAY

```
Küçük, sık, interaktif paketler   → TCP_NODELAY açık (Nagle kapalı) → düşük latency
Büyük, toplu veri transferi        → Nagle açık (varsayılan) → yüksek verim
```

### Task Yerleşimi (Blocking Yönetimi)

`SysSockConnect` blocking olduğu için (OS timeout'una kadar task'ı dondurur), TCP istemci/sunucu mantığı **Freewheeling veya en düşük öncelikli task**'ta olmalı (Not 1, task-structure/01 bloke-I/O kuralı). Ana kontrol task'ında asla socket çağrısı yapılmamalı — watchdog tetikler.

## Derin Teknik Detay

### TCP Akış Modeli: Neden Mesaj Sınırı Yok?

TCP, OSI taşıma katmanında **güvenilir, sıralı bir byte akışı** sunar — mesaj/datagram değil. Gönderenin `send(100 byte)` çağrısı, TCP tarafından segmentlere bölünebilir, ağda birleşebilir, alıcıda farklı boyutlarda `recv` ile teslim edilir. TCP yalnızca "byte'lar sırayla ve eksiksiz gelir" garantisi verir, "send sınırları korunur" garantisi vermez. Bu yüzden her TCP uygulaması kendi **mesaj çerçeveleme (framing)** katmanını kurmak zorundadır — uzunluk öneki, terminatör veya sabit boyut. Bu, Modbus/OPC UA gibi protokollerin neden kendi framing'lerini taşıdığının ve ham socket kullanırken neden bunu sıfırdan yazmak gerektiğinin (belgedeki SOH+Length+Payload+Checksum örneği) köküdür. UDP datagram (mesaj sınırlı) sunar ama güvenilirlik vermez; TCP tersini yapar.

### Blocking vs Non-Blocking: İşletim Sistemi Çağrı Modeli

`SysSock*` fonksiyonları OS'in Berkeley socket API'sine ince bir sarmalayıcıdır. Blocking modda `recv`, kernel'de veri gelene kadar thread'i uyutur (sleep) — PLC bağlamında bu, IEC task'ının (bir pthread, task-structure/01) o süre boyunca CPU bırakması demektir. `SysSockConnect`'in non-blocking ayara rağmen blocking kalması, CODESYS sarmalayıcısının bu özel çağrıyı senkron tutmasındandır — bu yüzden connect'in OS timeout'u (TCP SYN retry, 20-75sn) task'ı bloke eder. Non-blocking mod (`FIONBIO`), recv/send/accept'in "veri yoksa hemen -1 dön" davranışını açar; bu, PLC'nin scan-cycle modeline (her scan kısa sürmeli) uymak için zorunludur. Bloke eden socket çağrısı = scan cycle'ı kıran şey = watchdog tetikleyici.

### State Machine Zorunluluğu: Asenkron I/O'yu Senkron Scan'e Sığdırmak

TCP bağlantısı doğası gereği asenkron ve çok-adımlıdır (connect → send → recv → close), her adım zaman alabilir. PLC scan cycle ise her döngüde kısa ve deterministik olmalı (fundamentals/01). Bu gerilimi çözmenin tek yolu, bağlantıyı bir **state machine**'e bölmektir: her scan bir adım ilerlet, bloke etme. `eDisconnected→eConnecting→eConnected→...` her durumda non-blocking bir işlem yapıp hemen döner. Bu, programming/03'teki "her scan koşulsuz çağır + durum makinesi" deseninin networking'e uygulanmış halidir — asenkron dünyayı senkron scan modeline sığdırmanın CODESYS yolu. Bu yüzden ham TCP, Modbus/OPC UA'dan çok daha zordur: framing + state machine + handle yönetimi + endian'ı elle yazarsın.

## İlgili Konular

```
knowledge/codesys/networking/
├── 01_opcua_server.md        → Standart, güvenli, çok daha kolay
├── 02_modbus_slave.md        → Basit veri paylaşımı için
└── 04_mqtt_client.md         → Event-driven IoT iletişimi

knowledge/codesys/programming/
├── 03_function_blocks.md     → FB içinde state machine tasarımı
└── 05_error_handling.md      → Bağlantı hata yönetimi

Araçlar:
  Wireshark → TCP paket analizi, protokol doğrulama
  Netcat    → Hızlı test sunucu/istemci: nc -l -p 9000
  Python    → socket modülü ile test client/server
```
