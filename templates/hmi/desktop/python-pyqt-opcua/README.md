# PyQt6 + asyncua Masaüstü HMI (EXAMPLE_conveyor)

CODESYS PLC'ye **doğrudan** (gateway yok) OPC-UA ile bağlanan PyQt6 masaüstü HMI
başlangıç şablonu. `EXAMPLE_conveyor` projesinin `GVL_HMI` değişkenlerini izler ve
komut yazar.

## Özellikler

- **asyncua + qasync**: tek event loop (GUI thread), `@asyncSlot` ile async OPC-UA.
- **Subscription**: izlenen tüm node'lar tek subscription altında; veri thread-safe
  queue'ya yazılır, `QTimer` (100ms) ile coalesce edilerek UI'ye basılır.
- **3 bölge göstergesi**: durum (E_ZoneState), hız (m/min), oto/manuel mod.
- **Durum şeridi**: E-Stop, çalışma izni, genel alarm, bağlantı durumu.
- **Alarm paneli**: ISA-18.2 esinli; Acknowledge ≠ Resolved ayrımı.
- **Komut butonları**: bölge bazında `axCmdAutoRun[i]`, global `xCmdReset`.
- **Heartbeat watchdog**: `uHeartbeat` 3 sn değişmezse "VERİ BAYAT" + yazma kilidi.

## Dosya yapısı

```
python-pyqt-opcua/
├── main.py            # Uygulama + ana pencere, QTimer flush/refresh
├── opcua_client.py    # asyncua sarmalayıcı: connect, subscription, write
├── config.py          # Endpoint, namespace URI, NodeId tanımları, enum eşlemesi
├── ui/
│   ├── __init__.py
│   ├── widgets.py     # ZoneWidget, StatusBanner (ISA-101 renkleri)
│   └── alarm_panel.py # AlarmPanel (QTableWidget + onay)
├── requirements.txt
└── README.md
```

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Python 3.10+ gereklidir (asyncua v2.0).

## Çalıştırma

```bash
python main.py
```

Pencere açılır; "Bağlan" ile PLC'ye bağlanılır.

## PLC endpoint / NodeId konfigürasyonu

`config.py` içinde:

- `OPCUA_ENDPOINT` — CODESYS OPC-UA Server adresi (varsayılan port 4840).
- `CODESYS_NS_URI` — namespace URI. **Namespace index sabit yazılmaz**; bağlantıda
  `get_namespace_index(URI)` ile alınır. URI'yi UaExpert ile `NamespaceArray`'den
  doğrulayın (controller'a göre değişir).
- `RUNTIME_NAME` / `APPLICATION_NAME` — NodeId yolundaki Runtime + Application adı
  (`|var|<Runtime>.<App>.GVL_HMI.<Değişken>`). UaExpert ile doğrulayın.

CODESYS tarafı: Application'a Symbol Configuration ekleyin, "Build" yapın,
"Support OPC UA features" işaretleyin, PLC'ye indirip Runtime'ı başlatın.

### Array node'ları hakkında

CODESYS `ARRAY[1..3]` değişkenleri (aZoneState/Speed/Auto, axCmdAutoRun) Symbol
Configuration'a göre tek array node veya eleman-node olarak açılabilir. Bu şablon:
- **okumada** array'i tek değer (liste) olarak bekler,
- **yazmada** eleman-node (`axCmdAutoRun[1]`) kullanır.
Sunucunuzun davranışı farklıysa `opcua_client.write_auto_run` ve `main._as_list`
mantığını UaExpert'teki gerçek node yapısına göre uyarlayın.

## Güvenlik notu

Varsayılan `USE_SECURITY=False` yalnızca **geliştirme** içindir (anonymous,
şifresiz kanal). Üretimde:

1. `config.USE_SECURITY = True` yapın.
2. İstemci sertifikası üretin (`asyncua[crypto]`, `setup_self_signed_certificate`).
3. İstemci `.der`'ini CODESYS Runtime'ın `PKI/CA/certs/` (trusted) klasörüne ekleyin.
4. Sunucu sertifikasını indirip `config.py`'de `server_cert.der` yolunu ayarlayın.
5. Basic256Sha256 + SignAndEncrypt kullanın; CODESYS'te anonim erişimi kapatın,
   kullanıcı adı/parola tanımlayın.

Kritik komutlar (oto run / reset) için reconnect sırasında "yarı-bağlı" durum
mümkündür; sahada write sonrası read-back doğrulaması önerilir.
