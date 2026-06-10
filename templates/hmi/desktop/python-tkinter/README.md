# Tkinter + asyncua Masaüstü HMI (EXAMPLE_conveyor)

CODESYS PLC'ye **doğrudan** OPC-UA ile bağlanan, **stdlib Tkinter** tabanlı hafif
masaüstü HMI. Ek GUI bağımlılığı yoktur (yalnızca `asyncua`). `EXAMPLE_conveyor`
projesinin `GVL_HMI` değişkenlerini izler ve komut yazar.

## Özellikler

- **asyncua.sync + ayrı thread**: OPC-UA IO bir daemon thread'de `ThreadLoop` ile
  çalışır; asyncio bilgisi gerekmez (01_opcua_clients_python §9 deseni).
- **Polling**: worker thread tüm node'ları tek `read_values` ile periyodik okur.
- **Tkinter `after()`**: GUI thread snapshot'ı okuyup widget'ları yeniler; ağ IO
  asla GUI thread'inde yapılmaz.
- **3 bölge göstergesi**, durum şeridi (E-Stop / izin / alarm / bağlantı),
  alarm listesi (Treeview), komut butonları (`axCmdAutoRun[i]`, `xCmdReset`).
- **Heartbeat watchdog**: `uHeartbeat` 3 sn değişmezse "VERİ BAYAT" + komut kilidi.

## Dosya yapısı

```
python-tkinter/
├── main.py          # Tkinter pencere + after() yenileme döngüsü
├── opcua_client.py  # asyncua.sync worker thread: poll read_values + komut kuyruğu
├── config.py        # Endpoint, namespace URI, NodeId tanımları
├── requirements.txt
└── README.md
```

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Python 3.10+ gereklidir. Tkinter çoğu Python dağıtımıyla gelir; Linux'ta gerekirse
`sudo apt install python3-tk`.

## Çalıştırma

```bash
python main.py
```

Uygulama açılır açılmaz arka plan thread bağlanmayı dener; bağlantı kopunca otomatik
yeniden dener (5 sn aralıkla).

## PLC endpoint / NodeId konfigürasyonu

`config.py` içinde `OPCUA_ENDPOINT`, `CODESYS_NS_URI`, `RUNTIME_NAME`,
`APPLICATION_NAME` ayarlanır. Namespace index **sabit yazılmaz**; bağlantıda
`get_namespace_index(URI)` ile alınır. URI ve Runtime adını UaExpert ile doğrulayın.

CODESYS tarafı: Symbol Configuration ekleyin, "Support OPC UA features" işaretleyin,
PLC'ye indirip Runtime'ı başlatın.

Array node davranışı (tek array node vs eleman-node) sunucunuza göre değişebilir;
`opcua_client._drain_commands` yazma yolunu (`axCmdAutoRun[i]`) ve `main._as_list`
okuma mantığını UaExpert'teki gerçek yapıya göre uyarlayın.

## Polling vs Subscription notu

Bu şablon bilinçli olarak **polling** kullanır (Tkinter + asyncio entegrasyonu
karmaşıktır; sync API daha sade). Çok sayıda tag veya yüksek frekans gerekiyorsa
PyQt şablonundaki subscription tabanlı yaklaşımı tercih edin (trafik %70-90 azalır).

## Güvenlik notu

Varsayılan `USE_SECURITY=False` yalnızca **geliştirme** içindir. Üretimde
`config.USE_SECURITY=True` yapıp istemci/sunucu sertifikalarını üretin, CODESYS
Runtime'ın trusted klasörüne istemci sertifikasını ekleyin, Basic256Sha256 +
SignAndEncrypt ve kullanıcı adı/parola kullanın, anonim erişimi kapatın.
