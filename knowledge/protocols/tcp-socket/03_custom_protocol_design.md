---
KONU        : TCP Üzerinde Özel Protokol Tasarımı
KATEGORİ    : protocols
ALT_KATEGORI: tcp-socket
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-01
KAYNAKLAR   :
  - url: "https://www.codeproject.com/Articles/37496/TCP-IP-Protocol-Design-Message-Framing"
    başlık: "CodeProject — TCP/IP Protocol Design: Message Framing"
    güvenilirlik: topluluk
  - url: "https://medium.com/@harshithgowdakt/deep-dive-into-tcp-sockets-how-data-travels-under-the-hood-7c16f6b2bf95"
    başlık: "Medium — Deep Dive into TCP Sockets"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_basics.md"
    ilişki: gerektirir
  - konu: "02_codesys_implementation.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "TCP socket temelleri (01_basics.md)"
  - "CODESYS SysSock implementasyonu (02_codesys_implementation.md)"
  - "Bit ve byte işlemleri, big-endian/little-endian"
ÇELİŞKİLER :
  - kaynak: "Big-Endian vs Little-Endian seçimi"
    konu: "Ağ protokolleri tarihsel olarak big-endian kullanır"
    çözüm: >
      Network byte order = Big-Endian (MSB önce). Tüm IP, TCP başlıkları böyle.
      x86 CPU'lar Little-Endian (LSB önce). CODESYS PLC'lerin çoğu Little-Endian.
      Özel protokol tasarımında: Big-Endian'ı standart olarak seç (çoğu protokol böyle).
      Eğer iki PLC aynı mimarideyse Little-Endian de çalışır ama gelecekteki
      heterojen sistemler için Big-Endian daha taşınabilir.
  - kaynak: "Checksum vs CRC — hangisi daha iyi?"
    konu: "Basit XOR checksum vs CRC-16 seçimi"
    çözüm: >
      XOR checksum: Hesaplaması kolay ama hata tespiti zayıf.
        2 hata aynı bitlerde olursa XOR sıfırlanır → Hata kaçar.
      CRC-16: Biraz daha karmaşık ama çok daha güçlü hata tespiti.
        Endüstriyel protokollerde (Modbus CRC-16) standart.
      Fabrika LAN'ında: TCP kendi hata kontrolünü yapıyor.
        Üst katman checksum opsiyonel ama iyi pratik.
      Tavsiye: Basit XOR yeterli görüntü verirse CRC-16 kullan — bir kez yaz.
---

## Özün Ne

Ham TCP socket üzerinde iletişim kurmak "veriyi gönder, karşı taraf alsın" kadar basit değildir. TCP bir byte stream'dir: Gönderdiğin 100 byte'lık mesaj, karşı tarafta 30+70 byte olarak gelebilir. Mesaj sınırları korunmaz. Bu nedenle uygulama katmanında **framing** (çerçeveleme) zorunludur. Bu belge, endüstriyel otomasyon bağlamında sağlam, versiyonlanabilir ve hata toleranslı bir özel protokolün nasıl tasarlandığını ele alır. Teorik tasarımdan CODESYS implementasyonuna, oradan Python test istemcisine kadar uçtan uca gösterilir.

## Nasıl Çalışır

### Problem: TCP Stream ve Kısmi Alma

```
Gönderilen: [HEADER][LENGTH=100][DATA 100 byte][CHECKSUM]
Alınan:     recv() → 45 byte
            recv() → 62 byte  (ilk recv'den 17 byte + ikinci mesajdan 45 byte?)
            recv() → ...

TCP, veriyi akışlı gönderir. Buffer'a ne kadar veri sığarsa o kadar gelir.
Çözüm: Uygulama katmanında akümülatör buffer + mesaj tanıma mantığı.
```

### Protokol Tasarım İlkeleri

```
1. Framing (Çerçeveleme):
   Her mesajın nerede başlayıp nerede bittiği net olmalı.
   İki yaklaşım:
   a) Length-prefixed: Başa uzunluk yaz, o kadar byte oku.
   b) Delimiter-based: Mesaj sonu belirteci (ör. \r\n, 0xFF).
   
   Endüstriyel tercih: Length-prefixed + SOH (Start of Header)
   Delimiter, data içinde de olabilir → Escape mekanizması gerekir → Karmaşık.

2. Senkronizasyon:
   Bağlantı kopup yeniden kurulursa veya veri bozulursa,
   parser doğru başlangıç noktasını bulmalı.
   SOH (Start of Header) sihirli baytı bunun için kullanılır.

3. Hata tespiti:
   Checksum veya CRC ile mesajın bütünlüğü doğrulanır.

4. Versiyonlama:
   Protokol değişirse eski istemciler graceful başarısız olmalı.
   Header'da versiyon alanı bunu sağlar.
```

### Endüstriyel TCP Protokol Şablonu

```
┌───────┬───────┬───────┬─────────────────────────┬──────────┐
│  SOH  │  VER  │  MSG  │         LENGTH          │  DATA    │  CKSUM  │
│ 1 byte│ 1 byte│ 1 byte│         2 byte          │  N byte  │  1 byte │
└───────┴───────┴───────┴─────────────────────────┴──────────┴─────────┘
   0x01   1-255   0-255   Big-Endian UINT16    0-65535 byte    XOR

Toplam minimum: 6 byte (header) + N byte (data)

SOH (Start of Header):
  0x01 — Sabit "sihirli" değer. Mesaj başlangıcı.
  Senkronizasyon kaybında bu bayt aranır.

VER (Version):
  1 = v1 protokol. İki taraf eşleşmeli.
  Uyumsuz versiyon → Bağlantıyı kes + log.

MSG (Message Type):
  0x10 = Veri mesajı (Data)
  0x20 = Komut mesajı (Command)
  0x30 = Yanıt mesajı (Response)
  0x40 = Hata mesajı (Error)
  0x50 = Heartbeat (Ping)
  0x51 = Heartbeat yanıtı (Pong)

LENGTH:
  Data alanının byte uzunluğu.
  Big-Endian 16-bit unsigned integer.
  SOH+VER+MSG+LENGTH+CHECKSUM dahil değil.

DATA:
  Mesaj içeriği. Length byte uzunluğunda.
  Message type'a göre yorumlanır.

CHECKSUM:
  SOH'dan DATA sonuna kadar tüm byte'ların XOR'u.
  Verification: CKSUM XOR hesaplandı = 0 ise geçerli.
```

### Mesaj Tipleri ve Data Formatı

```iecst
(* Mesaj tipleri *)
CONST
    MSG_DATA      : BYTE := 16#10;  (* PLC verisi: proses değerleri *)
    MSG_COMMAND   : BYTE := 16#20;  (* Komut: setpoint, start/stop *)
    MSG_RESPONSE  : BYTE := 16#30;  (* Komut yanıtı *)
    MSG_ERROR     : BYTE := 16#40;  (* Hata bildirimi *)
    MSG_HEARTBEAT : BYTE := 16#50;  (* Ping *)
    MSG_HB_RESP   : BYTE := 16#51;  (* Pong *)
END_CONST

(* MSG_DATA (0x10) Data formatı:
   [Timestamp 4 byte UINT32][Speed_x10 2 byte UINT16]
   [Temp_x10 2 byte UINT16][Status 2 byte UINT16]
   Toplam: 10 byte data
   
   Timestamp: UNIX timestamp (saniye, 1970'den beri)
   Speed_x10: Gerçek hız × 10 (ör. 453 = 45.3 m/dk)
   Temp_x10: Sıcaklık × 10 (ör. 856 = 85.6 °C)
   Status: Bit maskesi (bit0=Running, bit1=Fault, bit2=AtSP)
*)

(* MSG_COMMAND (0x20) Data formatı:
   [Command_ID 1 byte][Param_Count 1 byte][Params N×2 byte UINT16]
   
   Command_ID:
     0x01 = Start
     0x02 = Stop
     0x03 = Reset
     0x10 = SetSpeed  (Param: speed_x10)
     0x11 = SetTemp   (Param: temp_x10)
     0x20 = LoadRecipe (Param: recipe_id)
*)

(* MSG_ERROR (0x40) Data formatı:
   [Error_Code 2 byte UINT16][Error_Message N byte ASCII]
   
   Error codes:
     0x0001 = Invalid message version
     0x0002 = Unknown message type
     0x0003 = Invalid checksum
     0x0004 = Command rejected
     0x0005 = Parameter out of range
*)
```

## Pratikte Nasıl Kullanılır

### Protokol Encoder/Decoder — CODESYS (IEC 61131-3)

```iecst
(* === PROTOKOL ENCODER === *)
FUNCTION FC_BuildMessage : UDINT
(* Mesaj oluştur ve buffer'a yaz *)
(* Dönüş: Toplam frame boyutu *)
VAR_INPUT
    nMsgType  : BYTE;
    pData     : POINTER TO BYTE;
    nDataLen  : UINT;
    pOutBuf   : POINTER TO BYTE;  (* Çıkış buffer'ı, en az nDataLen+6 byte *)
END_VAR
VAR
    i         : UDINT;
    nChecksum : BYTE := 0;
    nOffset   : UDINT := 0;
    pBuf      : POINTER TO BYTE;
END_VAR

pBuf := pOutBuf;

(* SOH *)
(pBuf + 0)^ := 16#01;

(* VER *)
(pBuf + 1)^ := 1;

(* MSG Type *)
(pBuf + 2)^ := nMsgType;

(* LENGTH — Big-Endian UINT16 *)
(pBuf + 3)^ := BYTE(SHR(nDataLen, 8));   (* High byte *)
(pBuf + 4)^ := BYTE(nDataLen AND 16#FF); (* Low byte *)

(* DATA — kopyala *)
FOR i := 0 TO nDataLen - 1 DO
    (pBuf + 5 + i)^ := (pData + i)^;
END_FOR

(* CHECKSUM — SOH'dan DATA sonuna XOR *)
nChecksum := 0;
FOR i := 0 TO UDINT(nDataLen) + 4 DO
    nChecksum := nChecksum XOR (pBuf + i)^;
END_FOR
(pBuf + 5 + nDataLen)^ := nChecksum;

FC_BuildMessage := nDataLen + 6;  (* Header(5) + Data + Checksum(1) *)
```

```iecst
(* === PROTOKOL DECODER (State Machine) === *)
FUNCTION_BLOCK FB_ProtocolDecoder
VAR_INPUT
    pNewData    : POINTER TO BYTE;
    nNewDataLen : UDINT;
END_VAR
VAR_OUTPUT
    xMsgReady   : BOOL;
    nMsgType    : BYTE;
    aPayload    : ARRAY[0..511] OF BYTE;
    nPayloadLen : UINT;
    xChecksumOK : BOOL;
    xVersionErr : BOOL;
    xFrameError : BOOL;
END_VAR
VAR
    aAccum      : ARRAY[0..1023] OF BYTE;  (* Akümülatör buffer *)
    nAccumFilled: UDINT := 0;
    eParseState : (eWaitSOH, eReadHeader, eReadData, eReadChecksum);
    nExpectedDataLen : UINT := 0;
    nBytesRead  : UDINT := 0;
    nChecksum   : BYTE;
    i           : UDINT;
END_VAR

xMsgReady := FALSE;

(* Gelen veriyi akümülatöre ekle *)
IF nNewDataLen > 0 AND pNewData <> 0 THEN
    FOR i := 0 TO nNewDataLen - 1 DO
        IF nAccumFilled < SIZEOF(aAccum) THEN
            aAccum[nAccumFilled] := (pNewData + i)^;
            nAccumFilled := nAccumFilled + 1;
        END_IF
    END_FOR
END_IF

(* State machine ile mesaj ayrıştır *)
CASE eParseState OF

    eWaitSOH:
        (* SOH baytını ara *)
        WHILE nAccumFilled > 0 DO
            IF aAccum[0] = 16#01 THEN  (* SOH bulundu *)
                eParseState := eReadHeader;
                EXIT;
            ELSE
                (* SOH değil → atla *)
                xFrameError := TRUE;
                MEMCPY(ADR(aAccum[0]), ADR(aAccum[1]), nAccumFilled - 1);
                nAccumFilled := nAccumFilled - 1;
            END_IF
        END_WHILE

    eReadHeader:
        (* Header: SOH(1)+VER(1)+MSG(1)+LEN(2) = 5 byte *)
        IF nAccumFilled >= 5 THEN
            (* Versiyon kontrol *)
            IF aAccum[1] <> 1 THEN
                xVersionErr := TRUE;
                (* SOH atla, yeniden senkronize et *)
                MEMCPY(ADR(aAccum[0]), ADR(aAccum[1]), nAccumFilled - 1);
                nAccumFilled := nAccumFilled - 1;
                eParseState := eWaitSOH;
            ELSE
                nMsgType := aAccum[2];
                (* LENGTH — Big-Endian → UINT *)
                nExpectedDataLen :=
                    (UINT(aAccum[3]) SHL 8) OR UINT(aAccum[4]);
                eParseState := eReadData;
            END_IF
        END_IF

    eReadData:
        (* Data + Checksum = nExpectedDataLen + 1 byte *)
        IF nAccumFilled >= UDINT(5 + nExpectedDataLen + 1) THEN
            
            (* Checksum doğrula *)
            nChecksum := 0;
            FOR i := 0 TO UDINT(nExpectedDataLen) + 4 DO
                nChecksum := nChecksum XOR aAccum[i];
            END_FOR
            
            IF nChecksum = aAccum[5 + nExpectedDataLen] THEN
                (* Checksum geçerli — payload'ı kopyala *)
                nPayloadLen := nExpectedDataLen;
                MEMCPY(ADR(aPayload[0]), ADR(aAccum[5]), nExpectedDataLen);
                xChecksumOK := TRUE;
                xMsgReady := TRUE;
            ELSE
                (* Checksum hatası — senkronizasyonu kaybet *)
                xChecksumOK := FALSE;
                xFrameError := TRUE;
            END_IF
            
            (* Kullanılan frame'i buffer'dan çıkar *)
            VAR_TEMP
                nFrameSize : UDINT;
            END_VAR
            nFrameSize := UDINT(5 + nExpectedDataLen + 1);
            
            IF nAccumFilled > nFrameSize THEN
                MEMCPY(ADR(aAccum[0]), ADR(aAccum[nFrameSize]),
                       nAccumFilled - nFrameSize);
            END_IF
            nAccumFilled := nAccumFilled - nFrameSize;
            
            (* Sonraki mesaj için hazır *)
            eParseState := eWaitSOH;
            nExpectedDataLen := 0;
        END_IF
END_CASE
```

### Mesaj Oluşturma — Pratik Örnekler

```iecst
(* Veri mesajı gönderme *)
PROGRAM PRG_SendData
VAR
    aDataMsg  : ARRAY[0..9] OF BYTE;   (* 10 byte data *)
    aFrame    : ARRAY[0..15] OF BYTE;  (* 10 + 6 = 16 byte frame *)
    nFrameLen : UDINT;
    dwTimestamp : UDINT;
    wSpeed     : UINT;
    wTemp      : UINT;
    wStatus    : UINT;
END_VAR

(* Data payload oluştur *)
dwTimestamp := SysTimeRtcGet();  (* UNIX timestamp *)
wSpeed := REAL_TO_UINT(GVL_Diagnostics.rActualSpeed * 10.0);
wTemp  := REAL_TO_UINT(GVL_Diagnostics.rActualTemp  * 10.0);

(* Status bit maskesi *)
wStatus := 0;
IF GVL_State.xRunning    THEN wStatus := wStatus OR 16#0001; END_IF
IF GVL_Alarms.xAnyActive THEN wStatus := wStatus OR 16#0002; END_IF
IF GVL_State.xAtSetpoint THEN wStatus := wStatus OR 16#0004; END_IF

(* Big-Endian yerleştirme *)
aDataMsg[0] := BYTE(SHR(dwTimestamp, 24));
aDataMsg[1] := BYTE(SHR(dwTimestamp, 16) AND 16#FF);
aDataMsg[2] := BYTE(SHR(dwTimestamp,  8) AND 16#FF);
aDataMsg[3] := BYTE(dwTimestamp AND 16#FF);
aDataMsg[4] := BYTE(SHR(wSpeed, 8));
aDataMsg[5] := BYTE(wSpeed AND 16#FF);
aDataMsg[6] := BYTE(SHR(wTemp, 8));
aDataMsg[7] := BYTE(wTemp AND 16#FF);
aDataMsg[8] := BYTE(SHR(wStatus, 8));
aDataMsg[9] := BYTE(wStatus AND 16#FF);

(* Frame oluştur *)
nFrameLen := FC_BuildMessage(
    nMsgType := MSG_DATA,
    pData    := ADR(aDataMsg[0]),
    nDataLen := 10,
    pOutBuf  := ADR(aFrame[0])
);

(* FB_TcpClient'a gönder *)
GVL_TCP.pTxData      := ADR(aFrame[0]);
GVL_TCP.nTxLen       := nFrameLen;
GVL_TCP.xSendTrigger := TRUE;
```

### Python Test İstemcisi

```python
import socket
import struct
import time
import threading

PROTOCOL_VERSION = 1
SOH = 0x01

# Message Types
MSG_DATA      = 0x10
MSG_COMMAND   = 0x20
MSG_RESPONSE  = 0x30
MSG_ERROR     = 0x40
MSG_HEARTBEAT = 0x50
MSG_HB_RESP   = 0x51

def build_frame(msg_type: int, data: bytes) -> bytes:
    """Protokol frame'i oluştur."""
    length = len(data)
    header = bytes([SOH, PROTOCOL_VERSION, msg_type,
                   (length >> 8) & 0xFF, length & 0xFF])
    payload = header + data
    
    checksum = 0
    for b in payload:
        checksum ^= b
    
    return payload + bytes([checksum])

def parse_frame(buf: bytearray) -> tuple:
    """
    Buffer'dan mesaj ayrıştır.
    Dönüş: (msg_type, payload, bytes_consumed) veya (None, None, 0)
    """
    # SOH ara
    soh_idx = None
    for i, b in enumerate(buf):
        if b == SOH:
            soh_idx = i
            break
    
    if soh_idx is None:
        return None, None, len(buf)  # Tüm buffer'ı tüket
    
    # Eski byte'ları atla
    if soh_idx > 0:
        return None, None, soh_idx
    
    # Header tam mı?
    if len(buf) < 5:
        return None, None, 0
    
    # Versiyon kontrol
    if buf[1] != PROTOCOL_VERSION:
        return None, None, 1  # SOH'u atla
    
    msg_type = buf[2]
    data_len = (buf[3] << 8) | buf[4]
    
    # Frame tamamlandı mı?
    total_len = 5 + data_len + 1
    if len(buf) < total_len:
        return None, None, 0
    
    # Checksum doğrula
    expected_cs = 0
    for b in buf[:5 + data_len]:
        expected_cs ^= b
    
    if expected_cs != buf[5 + data_len]:
        print(f"Checksum hatası! Beklenen: {expected_cs:02X}, Alınan: {buf[5+data_len]:02X}")
        return None, None, 1  # SOH'u atla
    
    payload = bytes(buf[5:5 + data_len])
    return msg_type, payload, total_len

def parse_data_message(payload: bytes) -> dict:
    """MSG_DATA payload'ını çözümle."""
    if len(payload) < 10:
        return None
    ts, speed_x10, temp_x10, status = struct.unpack('>IHHH', payload[:10])
    return {
        'timestamp':   ts,
        'speed':       speed_x10 / 10.0,
        'temperature': temp_x10 / 10.0,
        'running':     bool(status & 0x0001),
        'fault':       bool(status & 0x0002),
        'at_setpoint': bool(status & 0x0004)
    }

class IndustrialProtocolClient:
    """Test istemcisi — CODESYS PLC'ye bağlanır."""
    
    def __init__(self, host: str, port: int = 9000):
        self.host = host
        self.port = port
        self._sock = None
        self._buf = bytearray()
        self._running = False
    
    def connect(self) -> bool:
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(5)
            self._sock.connect((self.host, self.port))
            self._sock.settimeout(None)  # Non-blocking recv için
            self._sock.setblocking(False)
            print(f"Bağlandı: {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
            return False
    
    def send_heartbeat(self):
        frame = build_frame(MSG_HEARTBEAT, b'')
        self._sock.sendall(frame)
        print("Heartbeat gönderildi.")
    
    def send_command(self, cmd_id: int, params: list = None):
        """Komut gönder."""
        if params is None:
            params = []
        data = bytes([cmd_id, len(params)])
        for p in params:
            data += struct.pack('>H', p)
        frame = build_frame(MSG_COMMAND, data)
        self._sock.sendall(frame)
        print(f"Komut gönderildi: 0x{cmd_id:02X}")
    
    def receive_messages(self, timeout: float = 0.1):
        """Buffer'ı oku ve mesajları ayrıştır."""
        try:
            chunk = self._sock.recv(4096)
            if not chunk:
                print("Bağlantı kapandı.")
                return False
            self._buf.extend(chunk)
        except BlockingIOError:
            pass  # Veri yok, normal
        except Exception as e:
            print(f"Recv hatası: {e}")
            return False
        
        # Buffer'dan mesajları çıkar
        while self._buf:
            msg_type, payload, consumed = parse_frame(self._buf)
            
            if consumed > 0:
                del self._buf[:consumed]
            
            if msg_type is not None:
                self._handle_message(msg_type, payload)
            
            if consumed == 0:
                break  # Daha fazla veri bekleniyor
        
        return True
    
    def _handle_message(self, msg_type: int, payload: bytes):
        if msg_type == MSG_DATA:
            data = parse_data_message(payload)
            if data:
                print(f"Veri: Hız={data['speed']:.1f}m/dk, "
                      f"Sıcaklık={data['temperature']:.1f}°C, "
                      f"Çalışıyor={data['running']}")
        
        elif msg_type == MSG_HB_RESP:
            print("Heartbeat yanıtı alındı.")
        
        elif msg_type == MSG_ERROR:
            if len(payload) >= 2:
                err_code = struct.unpack('>H', payload[:2])[0]
                err_msg = payload[2:].decode('ascii', errors='replace')
                print(f"Hata: 0x{err_code:04X} — {err_msg}")
    
    def run(self):
        """Ana döngü."""
        self._running = True
        last_heartbeat = time.time()
        
        while self._running:
            if not self.receive_messages():
                break
            
            # Her 30 saniyede heartbeat
            if time.time() - last_heartbeat > 30:
                self.send_heartbeat()
                last_heartbeat = time.time()
            
            time.sleep(0.1)
    
    def disconnect(self):
        self._running = False
        if self._sock:
            self._sock.close()

# Test çalıştırma
if __name__ == '__main__':
    client = IndustrialProtocolClient('192.168.1.100', 9000)
    
    if client.connect():
        # Start komutu gönder
        client.send_command(cmd_id=0x01)  # Start
        time.sleep(0.5)
        
        # Hız setpoint ayarla (45.0 m/dk → 450)
        client.send_command(cmd_id=0x10, params=[450])  # SetSpeed
        
        # 30 saniye veri izle
        import threading
        t = threading.Thread(target=client.run, daemon=True)
        t.start()
        time.sleep(30)
        
        client.disconnect()
```

## Protokol Versiyonlama

```
Protokol geliştikçe yeni alanlar nasıl eklenir?

Kural 1 — Geriye uyumluluk:
  V1 istemci → V2 sunucu: Çalışmalı (V2, V1 mesajlarını anlıyor).
  V2 istemci → V1 sunucu: Graceful başarısızlık.

Kural 2 — Versiyon alanı:
  VER=1: Orijinal protokol
  VER=2: Extension alanı eklendi (optional fields)
  VER=3: Şifreleme eklendi

Kural 3 — Uyumsuz versiyon:
  Sunucu VER=2'yi anlayamıyorsa:
  → MSG_ERROR (0x40) + Error Code 0x0001 gönder
  → Bağlantıyı kapat

Kural 4 — Yeni mesaj tipleri:
  MSG Type bilinmiyorsa:
  → MSG_ERROR (0x0002 = Unknown message type)
  → Bağlantıyı KAPATMA — hata bildir, devam et

Kural 5 — Data padding:
  V1: MSG_DATA = 10 byte
  V2: MSG_DATA = 12 byte (2 byte ek)
  V1 istemci: LENGTH=12 görünce fazla byte'ı yok sayar.
  → LENGTH alanı sayesinde eski istemci yeni mesajı okuyabilir.
```

## Senkronizasyon Kaybı ve Kurtarma

```
Durum: Bağlantı kesintisi sonrası bağlantı yeniden kuruldu.
       Buffer'da eski yarım mesaj kalıp kalmadığı bilinmiyor.

Kurtarma algoritması:

1. Bağlantı yeniden kurulunca: Buffer'ı temizle.
2. SOH (0x01) baytını ara.
3. SOH bulununca header okumaya çalış.
4. Header geçersizse (versiyon yanlış, length saçma): SOH'u atla, tekrar ara.
5. Header geçerliyse, length kadar data oku.
6. Checksum hatalıysa: SOH'u atla, tekrar ara.
7. Başarılıysa: Mesajı işle, sonraki mesaj için başa dön.

Sonsuz döngü önlemi:
  Eğer N byte arandı ve hiç SOH bulunamazsa: Buffer'ı temizle.
  Bağlantıyı kapat, yeniden bağlan (veri bütünlüğü yoktur).
```

```iecst
(* CODESYS'te desync kurtarma *)
(* FB_ProtocolDecoder state machine'de eWaitSOH'da *)
(* Her geçersiz byte için xFrameError := TRUE *)
(* N byte'dan fazla hata gelirse: *)

IF nFrameErrorCount > 100 THEN
    (* Desync — bağlantıyı kapat, yeniden başla *)
    nFrameErrorCount := 0;
    nAccumFilled := 0;
    eParseState := eWaitSOH;
    GVL_TCP.xForceReconnect := TRUE;  (* TCP katmanına sinyal *)
END_IF
```

## Sık Yapılan Hatalar

### Hata 1: SOH Değerini Data'da Da Kullanmak

```
SOH = 0x01 seçildi. Data alanında da 0x01 byte olabilir.
Çözüm: SOH yalnızca framing için kullanılır; data yorumlanmaz.
       Parser "SOH + geçerli header" kombinasyonunu arar,
       yalnızca 0x01'i aramaz.
       Ek güvence: Length + Checksum ikili doğrulama.
```

### Hata 2: Big-Endian'ı Tutarsız Uygulamak

```
Bazı alanlar Big-Endian, bazıları Little-Endian → Hata.
Kural: Tüm multi-byte alanlar aynı byte order kullanmalı.
Standart seçim: Big-Endian (Network Byte Order).

IEC ST'de Big-Endian UINT16 yerleştirme:
  buf[0] := BYTE(SHR(value, 8));     (* High byte önce *)
  buf[1] := BYTE(value AND 16#FF);   (* Low byte sonra *)

IEC ST'de Big-Endian UINT16 okuma:
  value := (UINT(buf[0]) SHL 8) OR UINT(buf[1]);
```

### Hata 3: Buffer Overflow Kontrolü Yapmamak

```
Akümülatör buffer büyüklüğü: 4096 byte.
Bağlantı kopmadan önce cihaz 5000 byte gönderdiyse:
  Buffer doldu → Taşma → Veri kaybı veya bellek bozulması.

Kontrol:
  IF (nFilled + nNewData) > SIZEOF(aBuffer) THEN
      (* Buffer taşacak → Desync varsay → Sıfırla *)
      nFilled := 0;
  END_IF
```

### Hata 4: Checksum'ı Yanlış Hesaplamak

```
XOR checksum, tüm frame üzerinden hesaplanmalı (SOH dahil).
Yanlış: Yalnızca DATA üzerinden XOR.
Doğru: SOH + VER + MSG + LENGTH + DATA hepsinin XOR'u.

Verification:
  Frame [SOH, VER, MSG, LEN_H, LEN_L, D0, D1, ..., CKSUM]
  Tüm byte XOR → 0 olmalı (CKSUM dahil).
```

## Gerçek Proje Notları

**Not 1 — İlk Protokolde SOH Olmadan**  
İlk protokol tasarımında SOH yoktu; doğrudan VER+MSG+LENGTH ile başladı. Bağlantı kesintisi sonrası buffer'daki yarım veri yüzünden parser bozuldu; anlamsız mesajlar işlendi. SOH eklendi ve senkronizasyon kurtarma algoritması yazıldı. Artık bağlantı kopunca buffer temizleniyor.

**Not 2 — Length Alanı Olmadan İlk Deneme**  
İlk versiyonda delimiter-based framing kullanıldı: `\r\n` mesaj sonu. Data içinde `\r\n` gelince parser bozuldu. Length-prefixed framing'e geçildi. Escape mekanizması yerine sabit-uzunluklu header — çok daha basit ve güvenilir.

**Not 3 — Checksum Büyüklüğü vs Güvenilirlik**  
Tek byte XOR checksum başlangıçta yeterliydi. Bir noktada EMI'dan etkilenen bir kablo hatalı veri gönderdi, XOR checksum bunu yakalamadı. CRC-16'ya geçildi. Karmaşıklık arttı ama hata tespiti dramatik şekilde iyileşti. Fabrika ortamında: CRC-16 tercih et.

**Not 4 — Versiyon Geçişi**  
V1'de MSG_DATA 8 byte'tı. V2'ye geçince 12 byte eklendi. Eski V1 istemciler hâlâ bağlıydı. Çözüm: VER alanı. V2 sunucu, VER=1 gelen istemcilere 8 byte yanıt verdi, VER=2 gelen istemcilere 12 byte. 6 ay boyunca iki versiyon aynı anda çalıştı, sorunsuz geçiş.

## İlgili Konular

```
knowledge/protocols/tcp-socket/
├── 01_basics.md                 → TCP stream ve framing ihtiyacı
└── 02_codesys_implementation.md → CODESYS SysSock implementasyonu

knowledge/codesys/networking/
└── 03_tcp_socket.md             → Temel SysSock kullanımı

Araçlar:
  Python socket  → Hızlı protokol test istemcisi/sunucusu
  Wireshark      → Frame analizi (Hex view ile byte'ları incele)
  Hex editör     → Test mesajı oluşturma
  pytest         → Protokol unit testleri
```
