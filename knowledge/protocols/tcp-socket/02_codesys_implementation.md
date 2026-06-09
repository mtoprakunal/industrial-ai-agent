---
KONU        : CODESYS SysSock ile TCP Programlama
KATEGORİ    : protocols
ALT_KATEGORI: tcp-socket
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://forge.codesys.com/forge/talk/Runtime/thread/1bd5690115/"
    başlık: "CODESYS Forge — TCP Socket Communication"
    güvenilirlik: topluluk
  - url: "https://forum.codesys.com/viewtopic.php?t=7935"
    başlık: "CODESYS Forum — TCP Server Code"
    güvenilirlik: topluluk
  - url: "https://brightersidetech.com/tcp-socket-client-implementation-in-codesys/"
    başlık: "BrighterSideTech — TCP Socket Client in CODESYS"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_basics.md"
    ilişki: gerektirir
  - konu: "03_custom_protocol_design.md"
    ilişki: tamamlar
  - konu: "knowledge/codesys/networking/03_tcp_socket.md"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "TCP socket temelleri (01_basics.md)"
  - "CODESYS Function Block geliştirme (programming/03_function_blocks.md)"
  - "Pointer ve ADR() kullanımı ST'de"
ÇELİŞKİLER :
  - kaynak: "SysSockConnect — blocking mode istisnası"
    konu: "SysSockConnect, non-blocking ayarlı socket'ta bile blocking çalışır"
    çözüm: >
      SysSockConnect'in bu istisna davranışı CODESYS belgelerinde geçer.
      SysSockIoctl ile FIONBIO komutu tüm recv/send'i non-blocking yapar.
      Ancak connect() kendisi her zaman blocking. Çözüm: connect() çağrısını
      düşük öncelikli veya Freewheeling task'ta çalıştır. Yüksek öncelikli
      task'ta (Task_Control gibi) connect çağrısı tüm sistemi dondurabilir.
---

## Özün Ne

CODESYS, TCP socket programlama için `SysSock` kütüphanesini sunar. Bu kütüphane, POSIX socket API'sine benzer bir arayüz sağlar: socket oluştur, bağlan/dinle, gönder, al, kapat. Ancak PLC ortamında socket programlama, PC ortamından önemli ölçüde farklıdır: Task döngüsünü bloke etmemek, bağlantı kopmasını algılamak, buffer yönetimi ve non-blocking mod — bunların hepsi PLC bağlamında dikkatli tasarım gerektirir. Bu belge, CODESYS'te hem TCP Client hem TCP Server implementasyonunu ele alır.

## Nasıl Çalışır

### SysSock Kütüphanesi

```
Library Manager → Add Library → "SysSock"
veya "syssocket" → Namespace: syssocket (veya SYSSOCKET)

Temel fonksiyonlar:
  SysSockCreate   → Yeni socket oluştur
  SysSockBind     → Porta bağla (Server)
  SysSockListen   → Bağlantı kabul etmeye başla (Server)
  SysSockAccept   → Gelen bağlantıyı kabul et (Server)
  SysSockConnect  → Sunucuya bağlan (Client) ← HER ZAMAN BLOCKING
  SysSockSend     → Veri gönder
  SysSockRecv     → Veri al
  SysSockClose    → Socket kapat
  SysSockShutdown → Bağlantıyı nazikçe kapat
  SysSockIoctl    → Socket seçeneklerini ayarla (non-blocking mode)
  SysSockSetOption→ Socket seçeneği (SO_REUSEADDR, SO_KEEPALIVE...)
  SysSockInetAddr → IP string → UDINT dönüşümü
  SysSockHtons    → Host byte order → Network byte order (port için)
```

### Non-Blocking Mode — Neden Kritik

```
Blocking recv() (varsayılan):
  recv() çağrısı veri gelene kadar task'ı dondurur.
  10ms task'ta blocking recv → Watchdog!

Non-blocking recv():
  recv() anında döner: veri varsa alır, yoksa -1 döner.
  Task döngüsü devam eder.

Non-blocking socket ayarlama:
  SysSockIoctl(hSocket, FIONBIO, ADR(diNonBlocking), ADR(result))
  diNonBlocking : DINT := 1;  (* 1=non-blocking, 0=blocking *)
  
  ⚠ İSTİSNA: SysSockConnect HER ZAMAN BLOCKING çalışır.
              FIONBIO bu fonksiyonu ETKİLEMEZ.
              → connect() çağrısını Freewheeling veya düşük öncelik task'ta yap.
```

### SOCKADDRESS Yapısı

```iecst
(* IP adresi ve port bilgisini tutan yapı *)
VAR
    sockAddr : syssocket.SOCKADDRESS;
END_VAR

(* Doldurma *)
sockAddr.sin_family := syssocket.SOCKET_AF_INET;  (* IPv4 *)
sockAddr.sin_port   := syssocket.SysSockHtons(9000);  (* Network byte order *)
sockAddr.sin_addr   := syssocket.SysSockInetAddr('192.168.1.200', ADR(sockAddr.sin_addr));
(* sin_addr alanı için: string → binary IP *)
```

---

## TCP Client — Tam Implementasyon

```iecst
FUNCTION_BLOCK FB_TcpClient
VAR_INPUT
    xEnable        : BOOL;          (* TRUE = bağlı kal *)
    sRemoteIP      : STRING(15)  := '192.168.1.200';
    nRemotePort    : UINT        := 9000;
    pTxData        : POINTER TO BYTE;  (* Gönderilecek veri *)
    nTxLen         : UDINT;
    xSendTrigger   : BOOL;         (* Yükselen kenar → gönder *)
    tConnectTimeout: TIME := T#10S;
    tRecvTimeout   : TIME := T#5S;
END_VAR
VAR_OUTPUT
    xConnected     : BOOL;
    xDataReceived  : BOOL;
    aRxBuffer      : ARRAY[0..1023] OF BYTE;
    nRxLen         : UDINT;
    xFault         : BOOL;
    sFaultMsg      : STRING(80);
    eState         : E_TcpClientState;
END_VAR
VAR
    hSocket        : syssocket.RTS_IEC_HANDLE := syssocket.RTS_INVALID_HANDLE;
    iecResult      : syssocket.RTS_IEC_RESULT;
    sockAddr       : syssocket.SOCKADDRESS;
    diNonBlock     : DINT := 1;
    diReuse        : DINT := 1;
    
    nSentBytes     : DINT;
    nRecvBytes     : DINT;
    
    fbSendEdge     : R_TRIG;
    fbConnTimer    : TON;
    fbRecvTimer    : TON;
    xSendPending   : BOOL;
    
    (* Reconnect bekleme *)
    fbRetryTimer   : TON;
    tRetryDelay    : TIME := T#5S;
END_VAR

(* TYPE E_TcpClientState :
(   eDisconnected,
    eConnecting,
    eConnected,
    eSending,
    eClosing,
    eFault
);
END_TYPE *)

fbSendEdge(CLK := xSendTrigger);
IF fbSendEdge.Q THEN xSendPending := TRUE; END_IF

CASE eState OF

    eDisconnected:
        xConnected := FALSE;
        hSocket := syssocket.RTS_INVALID_HANDLE;
        
        (* Retry bekleme *)
        fbRetryTimer(IN := NOT xEnable, PT := tRetryDelay);  (* dummy *)
        
        IF xEnable THEN
            (* Socket oluştur *)
            hSocket := syssocket.SysSockCreate(
                iAddressFamily := syssocket.SOCKET_AF_INET,
                iType          := syssocket.SOCKET_STREAM,
                iProtocol      := syssocket.SOCKET_IPPROTO_TCP,
                pResult        := ADR(iecResult)
            );
            
            IF hSocket = syssocket.RTS_INVALID_HANDLE THEN
                xFault    := TRUE;
                sFaultMsg := 'Socket create failed';
                eState    := eFault;
            ELSE
                (* Non-blocking moda al *)
                syssocket.SysSockIoctl(hSocket, SYSSOCKET.FIONBIO,
                                        ADR(diNonBlock), ADR(iecResult));
                
                (* SO_REUSEADDR: Kısa süre sonraki yeniden bağlantı için *)
                syssocket.SysSockSetOption(hSocket, syssocket.SOCKET_SOL,
                    syssocket.SOCKET_SO_REUSEADDR, ADR(diReuse),
                    SIZEOF(diReuse), ADR(iecResult));
                
                (* Hedef adres yapısını doldur *)
                sockAddr.sin_family := syssocket.SOCKET_AF_INET;
                sockAddr.sin_port   := syssocket.SysSockHtons(nRemotePort);
                sockAddr.sin_addr   := syssocket.SysSockInetAddr(
                    sRemoteIP, ADR(sockAddr.sin_addr));
                
                fbConnTimer(IN := FALSE);
                eState := eConnecting;
            END_IF
        END_IF

    eConnecting:
        (* ⚠ SysSockConnect BLOCKING — bu task döngüsünü durdurur! *)
        (* Freewheeling task veya düşük öncelikli task'ta çalıştırılmalı *)
        fbConnTimer(IN := TRUE, PT := tConnectTimeout);
        
        iecResult := syssocket.SysSockConnect(
            hSocket        := hSocket,
            pSockAddr      := ADR(sockAddr),
            diSockAddrSize := SIZEOF(sockAddr)
        );
        
        IF iecResult = RTS_S_OK THEN
            xConnected := TRUE;
            xFault     := FALSE;
            sFaultMsg  := '';
            fbConnTimer(IN := FALSE);
            eState := eConnected;
        ELSIF fbConnTimer.Q THEN
            syssocket.SysSockClose(hSocket, ADR(iecResult));
            hSocket := syssocket.RTS_INVALID_HANDLE;
            xFault    := TRUE;
            sFaultMsg := CONCAT('Timeout: ', sRemoteIP);
            eState := eFault;
        END_IF

    eConnected:
        xConnected := TRUE;
        
        IF NOT xEnable THEN
            eState := eClosing;
        ELSIF xSendPending THEN
            xSendPending := FALSE;
            eState := eSending;
        ELSE
            (* Periyodik recv kontrolü *)
            nRecvBytes := syssocket.SysSockRecv(
                hSocket      := hSocket,
                pbyBuffer    := ADR(aRxBuffer),
                diBufferSize := SIZEOF(aRxBuffer),
                diFlags      := 0,
                pResult      := ADR(iecResult)
            );
            
            IF nRecvBytes > 0 THEN
                nRxLen        := DINT_TO_UDINT(nRecvBytes);
                xDataReceived := TRUE;
            ELSIF nRecvBytes = 0 THEN
                (* EOF — karşı taraf bağlantıyı kapattı *)
                syssocket.SysSockClose(hSocket, ADR(iecResult));
                hSocket    := syssocket.RTS_INVALID_HANDLE;
                xConnected := FALSE;
                sFaultMsg  := 'Remote closed connection';
                eState     := eDisconnected;
            END_IF
            (* nRecvBytes < 0: Non-blocking → veri yok, normal durum *)
        END_IF

    eSending:
        IF pTxData <> 0 AND nTxLen > 0 THEN
            nSentBytes := syssocket.SysSockSend(
                hSocket      := hSocket,
                pbyBuffer    := pTxData,
                diBufferSize := DINT(nTxLen),
                diFlags      := 0,
                pResult      := ADR(iecResult)
            );
            
            IF nSentBytes < 0 THEN
                xFault    := TRUE;
                sFaultMsg := 'Send failed';
                eState    := eFault;
            ELSE
                eState := eConnected;
            END_IF
        ELSE
            eState := eConnected;
        END_IF

    eClosing:
        syssocket.SysSockShutdown(hSocket,
            syssocket.SOCKET_SD_BOTH, ADR(iecResult));
        syssocket.SysSockClose(hSocket, ADR(iecResult));
        hSocket    := syssocket.RTS_INVALID_HANDLE;
        xConnected := FALSE;
        eState     := eDisconnected;

    eFault:
        IF hSocket <> syssocket.RTS_INVALID_HANDLE THEN
            syssocket.SysSockClose(hSocket, ADR(iecResult));
            hSocket := syssocket.RTS_INVALID_HANDLE;
        END_IF
        xConnected := FALSE;
        
        IF NOT xEnable THEN
            xFault := FALSE;
            sFaultMsg := '';
            eState := eDisconnected;
        END_IF
        (* xEnable TRUE → Disconnect'te retry bekleyecek *)

    ELSE:
        eState := eFault;
END_CASE

xDataReceived := (nRecvBytes > 0);
```

---

## TCP Server — Tam Implementasyon

```iecst
FUNCTION_BLOCK FB_TcpServer
VAR_INPUT
    xEnable      : BOOL;
    nListenPort  : UINT := 9000;
END_VAR
VAR_OUTPUT
    xClientConnected : BOOL;
    aRxBuffer        : ARRAY[0..1023] OF BYTE;
    nRxLen           : UDINT;
    xFault           : BOOL;
    sFaultMsg        : STRING(80);
    eState           : E_TcpServerState;
END_VAR
VAR
    hListenSocket : syssocket.RTS_IEC_HANDLE := syssocket.RTS_INVALID_HANDLE;
    hClientSocket : syssocket.RTS_IEC_HANDLE := syssocket.RTS_INVALID_HANDLE;
    iecResult     : syssocket.RTS_IEC_RESULT;
    listenAddr    : syssocket.SOCKADDRESS;
    clientAddr    : syssocket.SOCKADDRESS;
    clientAddrLen : DINT := SIZEOF(clientAddr);
    diNonBlock    : DINT := 1;
    diReuse       : DINT := 1;
    nRecvBytes    : DINT;
END_VAR

CASE eState OF

    eTcpSrv_Idle:
        IF xEnable THEN
            (* Listen socket oluştur *)
            hListenSocket := syssocket.SysSockCreate(
                syssocket.SOCKET_AF_INET, syssocket.SOCKET_STREAM,
                syssocket.SOCKET_IPPROTO_TCP, ADR(iecResult));
            
            IF hListenSocket = syssocket.RTS_INVALID_HANDLE THEN
                xFault    := TRUE;
                sFaultMsg := 'Listen socket create failed';
                eState    := eTcpSrv_Fault;
            ELSE
                (* SO_REUSEADDR: Restart sonrası TIME_WAIT sorununu önler *)
                syssocket.SysSockSetOption(hListenSocket, syssocket.SOCKET_SOL,
                    syssocket.SOCKET_SO_REUSEADDR, ADR(diReuse),
                    SIZEOF(diReuse), ADR(iecResult));
                
                (* Non-blocking moda al (accept için) *)
                syssocket.SysSockIoctl(hListenSocket, SYSSOCKET.FIONBIO,
                                        ADR(diNonBlock), ADR(iecResult));
                
                (* Bind: Tüm arayüzlerden dinle *)
                listenAddr.sin_family := syssocket.SOCKET_AF_INET;
                listenAddr.sin_port   := syssocket.SysSockHtons(nListenPort);
                listenAddr.sin_addr   := 0;  (* INADDR_ANY *)
                
                iecResult := syssocket.SysSockBind(
                    hListenSocket, ADR(listenAddr), SIZEOF(listenAddr));
                
                IF iecResult = RTS_S_OK THEN
                    iecResult := syssocket.SysSockListen(hListenSocket, 1);
                    IF iecResult = RTS_S_OK THEN
                        eState := eTcpSrv_Listening;
                    ELSE
                        syssocket.SysSockClose(hListenSocket, ADR(iecResult));
                        xFault    := TRUE;
                        sFaultMsg := 'Listen failed';
                        eState    := eTcpSrv_Fault;
                    END_IF
                ELSE
                    syssocket.SysSockClose(hListenSocket, ADR(iecResult));
                    xFault    := TRUE;
                    sFaultMsg := CONCAT('Bind failed port:', UINT_TO_STRING(nListenPort));
                    eState    := eTcpSrv_Fault;
                END_IF
            END_IF
        END_IF

    eTcpSrv_Listening:
        (* Non-blocking accept — bağlantı yoksa hemen döner *)
        hClientSocket := syssocket.SysSockAccept(
            hSocket         := hListenSocket,
            pSockAddr       := ADR(clientAddr),
            pdiSockAddrSize := ADR(clientAddrLen),
            pResult         := ADR(iecResult)
        );
        
        IF hClientSocket <> syssocket.RTS_INVALID_HANDLE THEN
            (* Client bağlandı *)
            xClientConnected := TRUE;
            (* Client socket'ı da non-blocking yap *)
            syssocket.SysSockIoctl(hClientSocket, SYSSOCKET.FIONBIO,
                                    ADR(diNonBlock), ADR(iecResult));
            eState := eTcpSrv_ClientConnected;
        END_IF
        
        IF NOT xEnable THEN
            eState := eTcpSrv_Closing;
        END_IF

    eTcpSrv_ClientConnected:
        nRecvBytes := syssocket.SysSockRecv(
            hSocket      := hClientSocket,
            pbyBuffer    := ADR(aRxBuffer),
            diBufferSize := SIZEOF(aRxBuffer),
            diFlags      := 0,
            pResult      := ADR(iecResult)
        );
        
        IF nRecvBytes > 0 THEN
            nRxLen := DINT_TO_UDINT(nRecvBytes);
            (* Veriyi işle — özel protokol: 03_custom_protocol_design.md *)
        ELSIF nRecvBytes = 0 THEN
            (* Client bağlantıyı kapattı *)
            syssocket.SysSockClose(hClientSocket, ADR(iecResult));
            hClientSocket    := syssocket.RTS_INVALID_HANDLE;
            xClientConnected := FALSE;
            eState := eTcpSrv_Listening;  (* Yeni client bekle *)
        END_IF
        (* nRecvBytes < 0: Non-blocking → veri yok, normal *)
        
        IF NOT xEnable THEN
            eState := eTcpSrv_Closing;
        END_IF

    eTcpSrv_Closing:
        IF hClientSocket <> syssocket.RTS_INVALID_HANDLE THEN
            syssocket.SysSockClose(hClientSocket, ADR(iecResult));
            hClientSocket    := syssocket.RTS_INVALID_HANDLE;
        END_IF
        IF hListenSocket <> syssocket.RTS_INVALID_HANDLE THEN
            syssocket.SysSockClose(hListenSocket, ADR(iecResult));
            hListenSocket := syssocket.RTS_INVALID_HANDLE;
        END_IF
        xClientConnected := FALSE;
        eState := eTcpSrv_Idle;

    eTcpSrv_Fault:
        IF NOT xEnable THEN
            xFault := FALSE;
            sFaultMsg := '';
            eState := eTcpSrv_Idle;
        END_IF
END_CASE
```

---

## Buffer Yönetimi

TCP stream tabanlıdır. Gönderilen mesaj sınırları recv() tarafında korunmaz. Uygulama katmanında akümülatör buffer gerekir:

```iecst
(* Kısmi veri akümülatörü *)
FUNCTION_BLOCK FB_ReceiveBuffer
VAR_INPUT
    pNewData     : POINTER TO BYTE;
    nNewDataLen  : UDINT;
    xClear       : BOOL;
END_VAR
VAR_OUTPUT
    xMessageReady : BOOL;
    pMessage      : POINTER TO BYTE;
    nMessageLen   : UDINT;
END_VAR
VAR
    aBuffer    : ARRAY[0..4095] OF BYTE;
    nFilled    : UDINT := 0;
    (* Protokol: ilk 4 byte = uzunluk (uint32 big-endian) *)
    nExpectedLen : UDINT := 0;
END_VAR

IF xClear THEN
    nFilled := 0;
    nExpectedLen := 0;
    xMessageReady := FALSE;
END_IF

(* Gelen veriyi buffer'a ekle *)
IF nNewDataLen > 0 AND pNewData <> 0 THEN
    IF (nFilled + nNewDataLen) <= SIZEOF(aBuffer) THEN
        MEMCPY(ADR(aBuffer) + nFilled, pNewData, nNewDataLen);
        nFilled := nFilled + nNewDataLen;
    ELSE
        (* Buffer taşması — protokol hatası *)
        nFilled := 0;
        nExpectedLen := 0;
    END_IF
END_IF

(* Tam mesaj var mı kontrol et *)
xMessageReady := FALSE;

IF nFilled >= 4 THEN
    (* İlk 4 byte'dan mesaj uzunluğunu oku *)
    IF nExpectedLen = 0 THEN
        nExpectedLen :=
            (UDINT(aBuffer[0]) SHL 24) OR
            (UDINT(aBuffer[1]) SHL 16) OR
            (UDINT(aBuffer[2]) SHL 8)  OR
            UDINT(aBuffer[3]);
    END_IF
    
    IF nFilled >= (4 + nExpectedLen) THEN
        (* Tam mesaj geldi *)
        xMessageReady := TRUE;
        pMessage      := ADR(aBuffer) + 4;  (* Header sonrası data *)
        nMessageLen   := nExpectedLen;
    END_IF
END_IF
```

---

## Bağlantı Kopmasını Algılama

CODESYS'te bağlantı kopması tespiti:

```iecst
(* Üç yöntem *)

(* Yöntem 1: recv() = 0 → EOF = Karşı taraf kapattı *)
nRecvBytes := syssocket.SysSockRecv(hSocket, ADR(buf), SIZEOF(buf), 0, ADR(result));
IF nRecvBytes = 0 THEN
    (* Bağlantı koptu — yeniden bağlan *)
    eState := eDisconnected;
END_IF

(* Yöntem 2: send() hatası → Bağlantı koptu *)
nSent := syssocket.SysSockSend(hSocket, ADR(buf), nLen, 0, ADR(result));
IF nSent < 0 THEN
    (* Send başarısız → Bağlantı koptu *)
    eState := eDisconnected;
END_IF

(* Yöntem 3: Uygulama katmanı heartbeat *)
(* Her N saniyede bir "ping" mesajı gönder *)
(* Yanıt N+timeout saniyede gelmezse → Bağlantı koptu *)
fbHeartbeatTimer(IN := xConnected, PT := T#30S);
IF fbHeartbeatTimer.Q THEN
    fbHeartbeatTimer(IN := FALSE);
    (* Ping mesajı gönder *)
    xSendHeartbeat := TRUE;
    (* Yanıt beklemeye başla... *)
END_IF
```

---

## Task Seçimi

```
TCP Client (connect çağrısı var):
  → Freewheeling Task veya Task_Background (Prio: 10-15)
  → connect() blocking olduğu için yüksek öncelikli task'ta OLMAMALÏ

TCP Server (listen + accept):
  → Task_Background (Prio: 5-15)
  → Non-blocking accept ile task döngüsünü bloke etmez

Veri gönderme/alma (send/recv):
  → Her task'ta olabilir (non-blocking modda)
  → Kritik kontrol task'ında veri işleme dikkatli yapılmalı
  
İdeal mimari:
  Task_Control (10ms, Prio:2): Kontrol mantığı, veri kullanımı
  Task_Background (Prio:10): TCP bağlantı yönetimi, veri al/gönder
  → Veriler GVL üzerinden paylaşılır
```

## Örnekler

### Örnek 1: Barcode Okuyucu Client

```iecst
(* PRG_BarcodeClient — Task_Background içinde *)
PROGRAM PRG_BarcodeClient
VAR
    fbClient       : FB_TcpClient;
    sBarcode       : STRING(64);
    xNewBarcode    : BOOL;
    sTempBuf       : STRING(64);
    i              : INT;
    nNullTerm      : DINT;
END_VAR

fbClient(
    xEnable      := GVL_State.xSystemOK,
    sRemoteIP    := '192.168.1.150',
    nRemotePort  := 4001
);

IF fbClient.xDataReceived AND fbClient.nRxLen > 0 THEN
    (* ASCII barcode — null-terminated string *)
    (* RxBuffer → STRING dönüşümü *)
    (* \r\n terminate bul *)
    
    (* Basit yaklaşım: Buffer'ı STRING olarak kopyala *)
    MEMSET(ADR(sTempBuf), 0, SIZEOF(sTempBuf));
    MEMCPY(ADR(sTempBuf), ADR(fbClient.aRxBuffer),
           MIN(fbClient.nRxLen, SIZEOF(sTempBuf) - 1));
    
    (* \r veya \n'yi sıfırla *)
    FOR i := 0 TO LEN(sTempBuf) - 1 DO
        IF sTempBuf[i] = '$R' OR sTempBuf[i] = '$N' THEN
            sTempBuf[i] := ' ';  (* CR/LF'yi boşlukla değiştir *)
        END_IF
    END_FOR
    
    sBarcode := sTempBuf;
    xNewBarcode := TRUE;
    
    GVL_Production.sLastBarcode := sBarcode;
    GVL_Production.xBarcodeReady := TRUE;
END_IF
```

### Örnek 2: Watchdog Heartbeat Sistemi

```iecst
(* Uygulama katmanı heartbeat — bağlantı sağlığı *)
PROGRAM PRG_TcpHeartbeat
VAR
    fbHBTimer      : TON;
    fbHBTimeout    : TON;
    xWaitingHB     : BOOL;
    nHeartbeatMsg  : WORD := 16#BEEF;  (* Magic number: 0xBEEF *)
    nHeartbeatResp : WORD := 16#CAFE;  (* Beklenen yanıt: 0xCAFE *)
END_VAR

(* Her 30 saniyede heartbeat gönder *)
fbHBTimer(IN := GVL_TCP.xConnected, PT := T#30S);
IF fbHBTimer.Q THEN
    fbHBTimer(IN := FALSE);
    
    (* Heartbeat mesajı gönder *)
    GVL_TCP.aOutBuffer[0] := BYTE(SHR(nHeartbeatMsg, 8));
    GVL_TCP.aOutBuffer[1] := BYTE(nHeartbeatMsg AND 16#FF);
    GVL_TCP.nOutLen := 2;
    GVL_TCP.xSendTrigger := TRUE;
    
    xWaitingHB := TRUE;
    fbHBTimeout(IN := FALSE);
END_IF

(* Heartbeat yanıt timeout: 5 saniye *)
fbHBTimeout(IN := xWaitingHB, PT := T#5S);
IF fbHBTimeout.Q THEN
    (* Yanıt gelmedi → Bağlantı koptu *)
    GVL_TCP.xConnected := FALSE;
    GVL_Alarms.xTcpHeartbeatTimeout := TRUE;
    xWaitingHB := FALSE;
END_IF

(* Gelen veri heartbeat yanıtı mı? *)
IF GVL_TCP.xDataReceived AND GVL_TCP.nRxLen >= 2 AND xWaitingHB THEN
    VAR_TEMP
        nReceived : WORD;
    END_VAR
    nReceived := WORD(SHL(WORD(GVL_TCP.aRxBuffer[0]), 8)) OR WORD(GVL_TCP.aRxBuffer[1]);
    
    IF nReceived = nHeartbeatResp THEN
        xWaitingHB := FALSE;
        fbHBTimeout(IN := FALSE);
        GVL_Alarms.xTcpHeartbeatTimeout := FALSE;
    END_IF
END_IF
```

## Sık Yapılan Hatalar

### Hata 1: connect() Yüksek Öncelikli Task'ta

```
Semptom: Hedef IP erişilemez → Task_Control dondu → Watchdog.
Çözüm : FB_TcpClient'ı Task_Background'da çalıştır.
         Task_Control yalnızca GVL üzerinden veriyi kullanır.
```

### Hata 2: Socket Handle Sızdırmak

```iecst
(* ❌ Hata durumunda socket kapatılmıyor *)
hSocket := syssocket.SysSockCreate(...);
IF iecResult <> RTS_S_OK THEN
    eState := eFault;   (* hSocket hâlâ açık! *)
    RETURN;
END_IF

(* ✅ Her çıkış noktasında kapat *)
IF iecResult <> RTS_S_OK THEN
    syssocket.SysSockClose(hSocket, ADR(iecResult));
    hSocket := syssocket.RTS_INVALID_HANDLE;
    eState  := eFault;
    RETURN;
END_IF
```

### Hata 3: recv() = -1 ile recv() = 0 Karıştırmak

```iecst
(* ❌ Yanlış *)
IF syssocket.SysSockRecv(...) <= 0 THEN
    eState := eDisconnected;  (* -1 = normal non-blocking, 0 = gerçek bağlantı kopması *)
END_IF

(* ✅ Doğru *)
nRcv := syssocket.SysSockRecv(...);
IF nRcv > 0 THEN
    (* Veri alındı *)
ELSIF nRcv = 0 THEN
    (* EOF: Bağlantı kapatıldı *)
    eState := eDisconnected;
END_IF
(* nRcv < 0: Non-blocking, veri yok — devam et *)
```

### Hata 4: SO_REUSEADDR Olmadan Restart

```
Semptom: PLC restart sonrası Server socket port'a bind olamıyor.
         "Address already in use" benzeri hata.
Neden  : TCP TIME_WAIT — eski bağlantı OS'ta 2-4 dakika bekler.
Çözüm  : SysSockSetOption → SO_REUSEADDR → 1
         Bind'den ÖNCE ayarlanmalı.
```

## Gerçek Proje Notları

**Not 1 — Freewheeling Task ve connect()**  
İlk CODESYS TCP uygulamasında connect() Task_Control (10ms, Prio:2) içindeydi. Hedef cihaz ağda yoktu. connect() 20 saniye dondu, tüm motorlar watchdog ile durdu. Derhal Freewheeling task'a taşındı. Artık connect() Freewheeling'de çalışıyor; Task_Control etkilenmiyor.

**Not 2 — SO_REUSEADDR Olmadan 4 Dakika Beklemek**  
Server uygulaması test aşamasında sık sık restart ediliyordu. Her restart'tan sonra bind() hata verdi — yaklaşık 4 dakika sonra tekrar çalıştı. TIME_WAIT süresi. SO_REUSEADDR eklenince anında bind oluyor.

**Not 3 — Heartbeat ile Phantom Bağlantı Tespiti**  
SCADA bağlantısı sabahları "connected" görünüyor ama veri gelmiyor ve gönderilemiyor. Nedeni: Gece boyunca NAT gateway session'ı kapsamış; TCP phantom bağlantı. recv() = -1 (non-blocking, veri yok) ve send() = -1 (gerçek hata) arasındaki fark net değildi. Heartbeat eklendi: 30 saniyede bir 2-byte ping, 5 saniyede yanıt gelmezse disconnect. Sabah bağlantı sorunu tamamen çözüldü.

**Not 4 — FIONBIO'nun connect()'i Etkilememesi Sürprizi**  
Yeni bir geliştirici, "socket'ı non-blocking yaptım, artık connect de non-blocking olur" varsayımıyla connect()'i Task_Control'e koydu. SysSockCreate hemen ardından FIONBIO=1 ayarlanmıştı. Yine de connect, erişilemeyen IP'de tüm task'ı dondurdu. CODESYS SysSock'ta SysSockConnect, FIONBIO'dan bağımsız olarak senkron tamamlanmaya çalışır — bu POSIX'teki "EINPROGRESS dönüp select ile bekle" davranışından farklıdır. Çözüm: connect mutlaka düşük öncelikli/Freewheeling task'ta. Bu davranış runtime/platforma göre değişebildiği için "non-blocking connect" varsayımına asla güvenme.

**Not 5 — RTS_INVALID_HANDLE ile 0 Karıştırma ve Sızıntı**  
Bir FB, hata yolunda `hSocket := 0` yapıyordu, `RTS_INVALID_HANDLE` değil. Bazı CODESYS runtime'larında geçerli bir handle değeri 0 olabilir; bu yüzden "0 ise kapatma" kontrolü gerçek bir açık socket'ı atladı → handle sızıntısı. Birkaç gün çalıştıktan sonra "SysSockCreate failed" ile tüm haberleşme durdu, restart geçici çözdü. Ders: handle kontrolünü her zaman `<> RTS_INVALID_HANDLE` ile yap, sihirli 0 ile değil; ve kapatınca tekrar `RTS_INVALID_HANDLE` ata (çifte close'u önler).

**Not 6 — SysSockSelect ile Scan Verimliliği**  
İlk tasarımda her client socket için ayrı non-blocking recv() çağrılıyordu; 8 bağlantıda scan süresi şişti çünkü her recv bir runtime/kernel geçişi. SysSockSelect ile tek çağrıda "hangi socket'larda veri var" sorgulanıp yalnızca hazır olanlarda recv yapıldı. Çok-bağlantılı server'da scan yükü belirgin düştü. Tek bağlantıda fark yok; çok-istemcili PLC server'da Select neredeyse zorunlu.

## Edge Case'ler ve Sistem Limitleri

PLC bağlamı, PC socket programlamasından iki kritik noktada ayrılır: (1) blocking bir çağrı tüm scan'i ve dolayısıyla kontrol mantığını dondurur (watchdog riski), (2) runtime'ın handle/buffer havuzu PC'ye göre çok daha kısıtlıdır. SysSock'un edge case'leri bu iki gerçeğin etrafında döner.

### SysSock Çağrı Davranışları — Sınır Durumları

| Durum | recv/connect/send davranışı | Doğru Tepki |
|---|---|---|
| `SysSockConnect`, erişilemez IP | Senkron bloke (saniyelerce) | Yalnızca Freewheeling/düşük-prio task |
| `SysSockRecv` = 0 | Karşı taraf FIN gönderdi (EOF) | Socket kapat, `eDisconnected` |
| `SysSockRecv` < 0 (non-blocking) | Veri yok | Normal — hiçbir şey yapma, devam et |
| `SysSockRecv` < 0 (blocking) | Gerçek hata / timeout | `eFault`, socket kapat |
| `SysSockSend` < istenen | TX buffer doldu (kısmi yazım) | Kalan byte için send-loop / tekrar dene |
| `SysSockSend` < 0 | Bağlantı koptu (RST/FIN) | `eDisconnected` |
| `SysSockAccept` = INVALID (non-blocking) | Bekleyen bağlantı yok | Normal — listening'de kal |
| `SysSockBind` hata (restart) | TIME_WAIT, port meşgul | `SO_REUSEADDR` (Create sonrası, Bind öncesi) |
| `SysSockCreate` = INVALID | Handle havuzu doldu (sızıntı!) | Sızıntıyı ara; her yolda Close çağrıldığını doğrula |

### Gömülü Runtime Limitleri

```
Eşzamanlı socket:    Genellikle onlarla sınırlı (16-64 tipik). PC değil bu.
                     Her açık handle havuzdan düşer; sızıntı = kademeli ölüm.
Socket buffer:       PC'ye göre küçük (8-32 KB olabilir). Büyük blok = kısmi send.
Scan etkileşimi:     Her SysSock çağrısı runtime geçişi; scan başına çok sayıda
                     çağrı scan süresini şişirir → jitter, watchdog riski.
String/Pointer:      ADR() ile geçilen buffer FB ömrü boyunca geçerli olmalı;
                     VAR_TEMP buffer'ın adresini send/recv'e geçirmek = bellek hatası.
```

### Tehlikeli PLC-Özel Senaryolar

```
1. connect() yüksek-prio task'ta → watchdog → motorlar durur (en sık felaket).
2. recv() <= 0 ile birleştirme → her boş non-blocking recv'de yanlışlıkla reconnect.
3. Online change sonrası socket handle'ları persistent değil → "connected" sanılan
   ölü handle; online change/reset sonrası bağlantıyı yeniden kurmaya zorla.
4. İki task aynı socket'a erişiyor → yarış durumu, bozuk buffer. Socket sahibi tek task olmalı.
```

## Optimizasyon

CODESYS'te TCP optimizasyonu öncelikle **scan'i temiz tutmak** ve **runtime kaynaklarını korumak** üzerinedir; ham throughput ikincildir. Etki sırasına göre:

```
ÖNCELİK 1 — Blocking connect'i scan'den ayır:
  connect()'i Freewheeling/Task_Background'a al. Tek başına en kritik karar:
  hem watchdog'u önler hem scan jitter'ını sıfırlar.

ÖNCELİK 2 — Task ayrımı (GVL köprüsü):
  TCP yönetimi Task_Background'da, kontrol Task_Control'de.
  Veri GVL üzerinden paylaşılır → kontrol mantığı socket gecikmesinden izole.

ÖNCELİK 3 — SysSockSelect ile çoklu socket:
  Birden çok bağlantıda her socket'a ayrı recv yerine tek Select çağrısı.
  Scan başına runtime geçiş sayısını düşürür.

ÖNCELİK 4 — Buffer'ı bir kerede oku:
  recv()'e büyük buffer (1-4 KB) ver; scan başına tek recv ile mümkün
  olduğunca çok byte al. Çok sayıda küçük recv = çok sayıda runtime geçişi.

ÖNCELİK 5 — TCP_NODELAY (komut-yanıt) / SO_SNDBUF (toplu transfer):
  SysSockSetOption ile. Küçük komutlarda Nagle kapat; büyük binary'de buffer büyüt.

ÖNCELİK 6 — Akümülatörü verimli yönet:
  Tüketilen frame'i MEMCPY ile başa kaydırmak yerine, mümkünse ring buffer /
  okuma-indeksi kullan; büyük buffer'da sürekli MEMCPY scan yükü yaratır.
```

| Hedef | Birincil Ayar | Task Yerleşimi |
|---|---|---|
| Watchdog'u önle | connect ayrı task | Freewheeling / Background |
| Düşük komut gecikmesi | TCP_NODELAY | Background (recv/send), Control (kullanım) |
| Yüksek throughput | SO_SNDBUF/RCVBUF büyük | Background, büyük recv buffer |
| Çok istemci | SysSockSelect | Background, tek select döngüsü |

## Derin Teknik Detay

### SysSock Neden POSIX'e Benzer Ama Aynı Değil?

SysSock, CODESYS runtime'ının altındaki işletim sisteminin (Linux, VxWorks, Windows CE, özel RTOS) socket API'sini soyutlayan ince bir sarmalayıcıdır. Amaç **platform bağımsızlığı**: aynı IEC kodu farklı PLC donanımlarında çalışsın. Bu soyutlama POSIX'e benzer isimler (`SysSockCreate`, `Bind`, `Recv`) kullanır ama bire bir değildir — örneğin handle tipi `RTS_IEC_HANDLE`'dır (ham int değil) ve hata kodları `RTS_IEC_RESULT` üzerinden taşınır. Bu yüzden POSIX/Python alışkanlıklarını (`select` ile non-blocking connect, errno yorumu) doğrudan taşımak hatalıdır.

```
Uygulama (IEC ST)
      │  SysSockCreate / Connect / Recv ...
      ▼
SysSocket bileşeni  (platform-bağımsız IEC arayüzü)
      │  runtime sistem çağrısı
      ▼
OS socket API  (Linux: socket()/connect()/recv(); VxWorks: kendi yığını)
      │
      ▼
TCP/IP yığını + NIC sürücüsü
```

connect()'in blocking kalması, bu sarmalayıcının altındaki bazı RTOS'larda non-blocking connect'in (EINPROGRESS + select) güvenilir/taşınabilir olmamasından kaynaklanır; CODESYS güvenli ortak payda olarak senkron connect sunar. Bu yüzden "connect ayrı task" kuralı bir tavsiye değil, mimari zorunluluktur.

### Neden State Machine — Doğrusal Kod Değil?

PLC scan modeli **kooperatif** çalışır: her FB, scan başına bir kez çağrılır ve hızla geri dönmek zorundadır; içeride bekleyemez (`WHILE recv...` yasak). Bir TCP bağlantısı ise doğası gereği **uzun ömürlü ve asenkron** bir süreçtir (bağlan → veri al/gönder → kopunca yeniden bağlan). Bu iki modeli uzlaştırmanın tek yolu, asenkron süreci bir durum makinesine bölmektir: her scan'de mevcut durumda yapılabilecek küçük adımı at, durumu kaydet, geri dön.

```
Scan N   : eConnecting → connect denendi, henüz dönmedi (Freewheeling'de bekliyor)
Scan N+1 : eConnecting → connect OK → eConnected
Scan N+2 : eConnected  → recv: -1 (veri yok) → durumda kal
Scan N+3 : eConnected  → recv: 37 byte → akümülatöre ekle
...
```

Bu, "asenkron I/O'yu senkron scan'e sıkıştırma" probleminin kanonik çözümüdür. Aynı desen Modbus/OPC UA client FB'lerinde de görülür. Doğrusal/blocking yazım PC'de çalışır ama PLC'de watchdog'a yol açar — bu nedenle endüstriyel socket kodu her zaman explicit state machine'dir.

### Handle Yönetimi — Neden Bu Kadar Disiplin Gerekir?

Her `SysSockCreate` runtime'ın sınırlı handle havuzundan bir slot ayırır. PC'de binlerce socket açılabildiği için bir sızıntı fark edilmeyebilir; gömülü PLC'de havuz onlarla sınırlı olduğundan **sızıntı kesin ölümdür** — sadece zaman meselesidir. Bu yüzden her çıkış yolu (hata, timeout, EOF, disable) socket'ı kapatmalı ve handle'ı `RTS_INVALID_HANDLE`'a sıfırlamalıdır. State machine'in `eFault` ve `eClosing` durumlarının kapanışı garanti etmesi tesadüf değil, tasarım gereğidir: tek bir kaçış yolu bile saatler/günler içinde sistemi durdurur.

## İlgili Konular

```
knowledge/protocols/tcp-socket/
├── 01_basics.md                 → TCP temelleri
└── 03_custom_protocol_design.md → Buffer'da işlenecek protokol tasarımı

knowledge/codesys/networking/
└── 03_tcp_socket.md             → SysSock özet implementasyon

knowledge/codesys/programming/
├── 03_function_blocks.md        → FB state machine tasarımı
└── 05_error_handling.md         → Hata yönetimi

Araçlar:
  Netcat (nc)    → TCP test: nc -l 9000 (server) veya nc IP 9000 (client)
  Wireshark      → TCP stream ve paket analizi
  Python socket  → Hızlı test server/client
```
