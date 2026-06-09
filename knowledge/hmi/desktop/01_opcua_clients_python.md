---
KONU        : Masaüstü HMI için OPC UA Python İstemcileri (asyncua)
KATEGORİ    : hmi
ALT_KATEGORI: desktop
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://github.com/FreeOpcUa/opcua-asyncio"
    başlık: "GitHub — FreeOpcUa/opcua-asyncio resmi deposu (v2.0, Haziran 2026)"
    güvenilirlik: topluluk
  - url: "https://opcua-asyncio.readthedocs.io/en/latest/usage/get-started/minimal-client.html"
    başlık: "opcua-asyncio ReadTheDocs — Minimal Client"
    güvenilirlik: topluluk
  - url: "https://opcua-asyncio.readthedocs.io/en/latest/api/asyncua.client.html"
    başlık: "asyncua.client API Referansı — ReadTheDocs"
    güvenilirlik: topluluk
  - url: "https://opcua-asyncio.readthedocs.io/en/latest/usage/common/node-nodeid.html"
    başlık: "NodeId ve Nodes — opcua-asyncio ReadTheDocs"
    güvenilirlik: topluluk
  - url: "https://opcua-asyncio.readthedocs.io/en/latest/usage/sync/overview.html"
    başlık: "Synchronous Interface — opcua-asyncio ReadTheDocs"
    güvenilirlik: topluluk
  - url: "https://github.com/FreeOpcUa/opcua-asyncio/blob/master/examples/client-with-encryption.py"
    başlık: "opcua-asyncio — client-with-encryption.py resmi örnek"
    güvenilirlik: topluluk
  - url: "https://github.com/FreeOpcUa/opcua-asyncio/blob/master/examples/client-reconnect.py"
    başlık: "opcua-asyncio — client-reconnect.py resmi örnek"
    güvenilirlik: topluluk
  - url: "https://github.com/FreeOpcUa/opcua-asyncio/blob/master/examples/generate_certificates.py"
    başlık: "opcua-asyncio — generate_certificates.py resmi örnek"
    güvenilirlik: topluluk
  - url: "https://pypi.org/project/asyncua/"
    başlık: "asyncua PyPI — v2.0, Python >=3.10, LGPLv3+"
    güvenilirlik: topluluk
  - url: "https://pypi.org/project/qasync/"
    başlık: "qasync PyPI — v0.28.0, asyncio + Qt event loop köprüsü"
    güvenilirlik: topluluk
  - url: "https://github.com/CabbageDevelopment/qasync"
    başlık: "GitHub — CabbageDevelopment/qasync"
    güvenilirlik: topluluk
  - url: "https://github.com/mn-automation-academy/tutorial-codesys-opc-ua-with-python"
    başlık: "GitHub — tutorial-codesys-opc-ua-with-python (asyncua.sync + CODESYS)"
    güvenilirlik: topluluk
  - url: "https://controlbyte.tech/blog/symbol-configuration-in-codesys/"
    başlık: "ControlByte — Symbol Configuration in CODESYS"
    güvenilirlik: topluluk
  - url: "https://content.helpme-codesys.com/en/CODESYS%20Communication/_cds_symbolconfiguration.html"
    başlık: "CODESYS Yardım — Symbol Configuration (resmi)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "protocols/opc-ua/06_client_implementations"
    ilişki: tamamlar
  - konu: "hmi/desktop/03_pyqt_patterns"
    ilişki: kullanır
  - konu: "hmi/web-based/01_opcua_clients_js"
    ilişki: alternatif
  - konu: "protocols/opc-ua/03_security"
    ilişki: gerektirir
  - konu: "protocols/opc-ua/04_subscriptions"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "Python 3.10+ ve asyncio/async-await sözdizimi bilgisi"
  - "OPC UA temel kavramları: NodeID, Namespace, Subscription, MonitoredItem"
  - "CODESYS Symbol Configuration yapılandırması (değişkenlerin OPC UA ile açılması)"
ÇELİŞKİLER :
  - kaynak: "python-opcua (opcua paketi) vs asyncua (opcua-asyncio)"
    konu: "python-opcua artık unmaintained; asyncua aktif olarak geliştirilmektedir"
    çözüm: >
      python-opcua (pip install opcua) 2020'den beri geliştirilmiyor.
      Yeni tüm projeler asyncua (pip install asyncua) kullanmalı.
      API büyük ölçüde aynı, fark: async/await zorunlu.
      asyncua v2.0 yalnızca Python >= 3.10 destekler.
  - kaynak: "asyncua subscription handler: callback sınıf vs async iterator"
    konu: "asyncua v2.0'da yeni async for / match-case iterator pattern eklendi; eski callback handler da destekleniyor"
    çözüm: >
      Eski pattern (SubHandler.datachange_notification callback) hâlâ çalışır.
      Yeni v2.0 pattern: async with await client.create_subscription(...) as sub + async for event in sub.
      Yeni pattern auto_reconnect ile daha iyi entegre çalışır.
      Qt entegrasyonunda eski callback pattern tercih edilir (thread-safe queue gerekir).
  - kaynak: "setup_self_signed_certificate fonksiyon adı"
    konu: "asyncua örneklerinde setup_self_signed_certificate kullanılıyor ancak Client metodundan ayrı bir cert_gen modülü fonksiyonu olarak da geliyor"
    çözüm: >
      asyncua.crypto.cert_gen.setup_self_signed_certificate fonksiyon adı
      resmi örneklerde (client-with-encryption.py) kullanılıyor.
      Ayrıca Client sınıfı da kendi setup_self_signed_certificate metoduna sahip.
      İkisi de çalışır; örnekte cert_gen versiyonu tercih edilir.
---

## Özün Ne

**asyncua** (pip paket adı: `asyncua`, GitHub: `opcua-asyncio`), Python için en aktif OPC UA istemci ve sunucu kütüphanesidir. Haziran 2026'da v2.0 yayınlanmış olup Python 3.10+ gerektirmektedir. Tamamen asyncio tabanlıdır; bağlantı, oturum yönetimi, node okuma/yazma, subscription ve güvenlik (sertifika + kullanıcı kimlik doğrulama) için yüksek seviyeli bir API sunar. Masaüstü HMI geliştirmede asyncua; CODESYS OPC UA sunucusuna bağlanmak, anlık değerleri okumak ve değişkenler değiştiğinde otomatik bildirim almak için kullanılır. asyncio event loop'u Qt event loop'uyla birleştirmek için **qasync** (v0.28.0, PyQt5/6 + PySide2/6 desteği) veya **PySide6.QtAsyncio** kullanılır.

## Nasıl Çalışır

### asyncua Mimarisi

asyncua, OPC UA binary protokolünü (TCP üzeri) tamamen Python ile uygular. Ana bileşenler:

- **`Client`** sınıfı: Bağlantı, oturum oluşturma, kimlik doğrulama ve yüksek seviyeli servisler. `url`, `timeout` (varsayılan: 4s), `watchdog_intervall` (varsayılan: 1s) parametrelerini alır.
- **`Node`** sınıfı: Adres uzayındaki tek bir node'u temsil eder. `get_node(nodeid_str)` ile oluşturulur — **bu çağrı sunucuyla iletişim kurmaz**, yalnızca bir nesne oluşturur. Gerçek ağ işlemi `read_value()`, `write_value()` gibi metodlarda gerçekleşir.
- **`Subscription`** sınıfı: MonitoredItem yönetimi. `create_subscription(period_ms, handler)` ile oluşturulur; `subscribe_data_change(nodes)` ile node'lar izlemeye alınır.
- **`asyncua.sync`** modülü: Asenkron API'nin senkron sarmalayıcısı. PyQt QThread veya standart threading içinde kullanılabilir.

### NodeID ve Namespace

OPC UA'da her node bir `NodeID` ile tanımlanır. NodeID iki bileşenden oluşur:
1. **Namespace Index** (`ns=`): Sunucunun namespace dizisindeki sıra numarası. **Sunucuya göre değişir** — asla hard-code edilmemeli.
2. **Tanımlayıcı**: Sayısal (`i=`), string (`s=`), GUID (`g=`) veya opaque (`b=`).

CODESYS OPC UA sunucusunda değişkenler string NodeID ile erişilir:
```
ns=<INDEX>;s=|var|CODESYS Control.Application.GVL_IO.xMotorRun
```

Namespace index'ini URI üzerinden dinamik olarak almak zorunludur:
```python
ns = await client.get_namespace_index("http://www.3s-software.com/schemas/Codesys-V3")
```

### asyncio + Qt Event Loop Sorunu

asyncio ve Qt birbirinden bağımsız event loop'lar kullanır. İkisini aynı thread'de çalıştırmak için köprü gerekir:

- **qasync** (önerilen — PyQt5, PyQt6, PySide2, PySide6): Qt event loop'unu asyncio loop olarak kullanır. `@asyncSlot()` dekoratörü Qt signal'larında async fonksiyon çağırmayı sağlar.
- **PySide6.QtAsyncio**: Qt 6.5+ ile gelen resmi çözüm, yalnızca PySide6.
- **Ayrı thread** (basit ama daha kaba): asyncio loop'u `threading.Thread` içinde çalıştırıp Qt signal'ları ile iletişim kurmak.

## Pratikte Nasıl Kullanılır

### 1. Kurulum

```bash
# Temel kurulum
pip install asyncua

# Güvenlik (sertifika, şifreleme) için kriptografi kütüphanesi
pip install "asyncua[crypto]"
# veya ayrıca:
pip install cryptography

# Qt entegrasyonu için
pip install qasync          # PyQt5, PyQt6, PySide2, PySide6 desteği
# veya
pip install PyQt6 qasync
pip install PySide6         # PySide6.QtAsyncio built-in gelir
```

asyncua v2.0 Python 3.10, 3.11, 3.12 ve 3.13'ü destekler. LGPLv3+ lisansı ile dağıtılır.

### 2. CODESYS Sunucu Yapılandırması

Python istemcisi bağlanmadan önce CODESYS tarafında şu adımlar tamamlanmalıdır:

1. **Symbol Configuration ekleme**: CODESYS IDE'de Application'a sağ tıkla → Add Object → Symbol Configuration.
2. **Derleme**: Symbol Configuration penceresinde "Build" butonuna bas — GVL değişkenleri listelenir.
3. **OPC UA desteği**: "Support OPC UA features" kutusunu işaretle.
4. **Proje indir ve çalıştır**: PLC'ye yükle, Runtime'ı başlat.
5. **Güvenlik (geliştirme ortamı için)**: Device → Communication Settings → "Allow anonymous login" aktif et.

CODESYS OPC UA sunucu varsayılan endpoint: `opc.tcp://<PLC_IP>:4840`

### 3. Temel Bağlantı ve Okuma

Kaynak: [opcua-asyncio ReadTheDocs — Minimal Client](https://opcua-asyncio.readthedocs.io/en/latest/usage/get-started/minimal-client.html)

```python
import asyncio
from asyncua import Client, ua

CODESYS_URL = "opc.tcp://192.168.1.100:4840"
CODESYS_NS_URI = "http://www.3s-software.com/schemas/Codesys-V3"

async def basic_read():
    # async with — disconnect otomatik yapılır
    async with Client(url=CODESYS_URL) as client:

        # Namespace index'i URI üzerinden al — ASLA sabit sayı yazma!
        ns = await client.get_namespace_index(CODESYS_NS_URI)
        print(f"CODESYS namespace index: {ns}")

        # Node'u string NodeID ile al
        # get_node() sunucuyla iletişim KURMAZ; sadece nesne oluşturur
        motor_node = client.get_node(
            f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun"
        )

        # Değeri oku (Python tipine otomatik dönüşüm)
        value = await motor_node.read_value()
        print(f"Motor Run: {value}")  # True veya False

        # DataValue oku: değer + timestamp + StatusCode
        data_value = await motor_node.read_data_value()
        print(f"Değer       : {data_value.Value.Value}")
        print(f"StatusCode  : {data_value.StatusCode}")
        print(f"Zaman damgası: {data_value.SourceTimestamp}")

        # Toplu okuma — tek UA çağrısıyla birden fazla node (verimli)
        nodes = [
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rTemperature"),
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rPressure"),
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.xConveyor1Run"),
        ]
        values = await client.read_values(nodes)
        print(f"Temp={values[0]:.1f}°C  Pressure={values[1]:.2f}bar  Konv={values[2]}")

asyncio.run(basic_read())
```

### 4. Değer Yazma

```python
import asyncio
from asyncua import Client, ua

async def write_values():
    async with Client(url="opc.tcp://192.168.1.100:4840") as client:
        ns = await client.get_namespace_index(
            "http://www.3s-software.com/schemas/Codesys-V3"
        )

        # Basit yazma — Python tipi otomatik çevrilir
        start_cmd = client.get_node(
            f"ns={ns};s=|var|CODESYS Control.Application.GVL_HMI.xStartCmd"
        )
        await start_cmd.write_value(True)
        print("Start komutu gönderildi")

        # Tip belirterek yazma (sunucu tipiyle uyumsuzluk hatalarını önler)
        setpoint_node = client.get_node(
            f"ns={ns};s=|var|CODESYS Control.Application.GVL_Params.rSpeedSetpoint"
        )
        await setpoint_node.write_value(
            ua.DataValue(ua.Variant(75.0, ua.VariantType.Double))
        )
        print("Hız setpointi yazıldı: 75.0")

        # INT16 yazma
        recipe_node = client.get_node(
            f"ns={ns};s=|var|CODESYS Control.Application.GVL_Params.nRecipeID"
        )
        await recipe_node.write_value(
            ua.DataValue(ua.Variant(3, ua.VariantType.Int16))
        )
        print("Reçete ID yazıldı: 3")

        # Toplu yazma — tek UA çağrısıyla birden fazla node
        nodes_to_write = [
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rSetTemp"),
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rSetPress"),
        ]
        await client.set_values(nodes_to_write, [120.0, 2.5])
        print("Toplu yazma tamamlandı")

asyncio.run(write_values())
```

### 5. Subscription ve MonitoredItem

asyncua v2.0'da iki yöntem desteklenmektedir:

**Yöntem A — Eski Callback Sınıfı (Qt entegrasyonu için önerilir):**

```python
import asyncio
import queue
from asyncua import Client, ua

class OpcuaDataHandler:
    """Thread-safe, non-blocking subscription handler.
    
    datachange_notification asyncio event loop thread'inde çağrılır.
    Qt GUI thread'ine güvenli iletim için queue kullanılır.
    """

    def __init__(self):
        self.data_queue: queue.Queue = queue.Queue(maxsize=10_000)

    def datachange_notification(self, node, val, data):
        """HIZLI OLMALI — hiçbir zaman block etmemeli."""
        try:
            self.data_queue.put_nowait({
                "node_id": str(node.nodeid),
                "value": val,
                "source_ts": data.monitored_item.Value.SourceTimestamp,
            })
        except queue.Full:
            pass  # Kuyruk doluysa veri at, GUI'yi engelleme

    def status_change_notification(self, status):
        print(f"Subscription durumu değişti: {status}")

    def event_notification(self, event):
        print(f"OPC UA eventi: {event}")


async def run_subscription():
    handler = OpcuaDataHandler()

    async with Client(url="opc.tcp://192.168.1.100:4840") as client:
        ns = await client.get_namespace_index(
            "http://www.3s-software.com/schemas/Codesys-V3"
        )

        # Subscription oluştur (publishing interval: 500ms)
        subscription = await client.create_subscription(
            period=500,       # ms
            handler=handler,
            publishing=True,
        )

        # İzlenecek node'lar
        nodes = [
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rTemperature"),
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun"),
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_Alarms.xAnyAlarm"),
        ]

        # subscribe_data_change → MonitoredItem handle listesi döner
        handles = await subscription.subscribe_data_change(nodes)
        print(f"Subscription aktif. {len(handles)} node izleniyor.")

        try:
            while True:
                await asyncio.sleep(0.05)  # 50ms GUI güncelleme döngüsü
                while not handler.data_queue.empty():
                    item = handler.data_queue.get_nowait()
                    var_name = item["node_id"].split(".")[-1]
                    print(f"[{item['source_ts']}] {var_name} = {item['value']}")
        except asyncio.CancelledError:
            pass
        finally:
            await subscription.unsubscribe(handles)
            await subscription.delete()
            print("Subscription temizlendi.")

asyncio.run(run_subscription())
```

**Yöntem B — Yeni async iterator pattern (v2.0, auto_reconnect ile uyumlu):**

```python
import asyncio
from asyncua import Client, ua
from asyncua.common.subscription import DataChangeEvent, StatusChangeEvent

async def run_subscription_v2():
    client = Client(url="opc.tcp://192.168.1.100:4840")

    # auto_reconnect=True: Bağlantı kopunca otomatik yeniden bağlan
    await client.connect(auto_reconnect=True, reconnect_max_delay=2.0)

    try:
        ns = await client.get_namespace_index(
            "http://www.3s-software.com/schemas/Codesys-V3"
        )

        # Context manager → subscription otomatik temizlenir
        async with await client.create_subscription(500) as sub:
            nodes = [
                client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rTemperature"),
                client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun"),
            ]
            await sub.subscribe_data_change(nodes)

            # async for ile event akışı — Python 3.10+ match-case
            async for event in sub:
                match event:
                    case DataChangeEvent(node=node, value=value):
                        print(f"Değer değişti: {node} = {value}")
                    case StatusChangeEvent(notification=notif):
                        print(f"Durum: {notif.Status}")
                        if notif.Status.is_bad():
                            print("Bağlantı sorunu — döngü sonlandırılıyor")
                            break
    finally:
        await client.disconnect()

asyncio.run(run_subscription_v2())
```

### 6. Yeniden Bağlanma (Reconnect) — Production Pattern

Kaynak: [client-reconnect.py resmi örnek](https://github.com/FreeOpcUa/opcua-asyncio/blob/master/examples/client-reconnect.py)

```python
import asyncio
import logging
from asyncua import Client, ua
from asyncua.common.subscription import DataChangeEvent, StatusChangeEvent

_logger = logging.getLogger(__name__)

async def opcua_client_with_reconnect(url: str, ns_uri: str):
    """Production-ready: bağlantı kopunca yeniden bağlan, subscription'ı yeniden kur."""

    while True:
        try:
            client = Client(url=url, timeout=10)
            # auto_reconnect: transport düştüğünde session'ı yeniden aktive eder
            await client.connect(auto_reconnect=True, reconnect_max_delay=2.0)
            _logger.info("Bağlantı kuruldu: %s", url)

            try:
                ns = await client.get_namespace_index(ns_uri)
                node = client.get_node(
                    f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rTemperature"
                )

                async with await client.create_subscription(500) as sub:
                    await sub.subscribe_data_change([node])

                    async for event in sub:
                        match event:
                            case DataChangeEvent(node=n, value=v):
                                _logger.info("Sıcaklık: %.1f°C", v)
                            case StatusChangeEvent(notification=notif):
                                _logger.warning("Subscription durumu: %s", notif.Status)
                                if notif.Status.is_bad():
                                    break  # Dış döngü yeniden bağlanacak

            finally:
                await client.disconnect()

        except Exception as exc:
            _logger.error("Bağlantı hatası: %s. 5 saniye sonra yeniden deneniyor...", exc)
            await asyncio.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(opcua_client_with_reconnect(
        url="opc.tcp://192.168.1.100:4840",
        ns_uri="http://www.3s-software.com/schemas/Codesys-V3",
    ))
```

### 7. Güvenlik — Sertifika ve Kullanıcı Kimlik Doğrulama

Kaynak: [client-with-encryption.py resmi örnek](https://github.com/FreeOpcUa/opcua-asyncio/blob/master/examples/client-with-encryption.py) ve [generate_certificates.py](https://github.com/FreeOpcUa/opcua-asyncio/blob/master/examples/generate_certificates.py)

```bash
# Önce kriptografi paketi kurulmalı
pip install "asyncua[crypto]"
```

**Adım 1: İstemci sertifikası oluşturma (bir kez yapılır)**

```python
import asyncio
import socket
from pathlib import Path
from cryptography.x509.oid import ExtendedKeyUsageOID
from asyncua.crypto.cert_gen import (
    setup_self_signed_certificate,
    generate_private_key,
    dump_private_key_as_pem,
)

async def generate_client_certificate():
    """Masaüstü HMI istemcisi için self-signed sertifika oluştur."""

    host_name = socket.gethostname()
    client_app_uri = f"urn:{host_name}:mycompany:hmi_client"

    cert_path = Path("client_cert.der")
    key_path  = Path("client_key.pem")

    # setup_self_signed_certificate: anahtar + sertifika birlikte oluşturur
    await setup_self_signed_certificate(
        key_path,
        cert_path,
        client_app_uri,
        host_name,
        [ExtendedKeyUsageOID.CLIENT_AUTH],
        {
            "countryName": "DE",
            "stateOrProvinceName": "Bavaria",
            "localityName": "Munich",
            "organizationName": "My Company GmbH",
        },
    )

    print(f"Sertifika oluşturuldu: {cert_path}")
    print("ÖNEMLI: Bu .der dosyasını CODESYS Runtime'ın")
    print("trusted/certs/ klasörüne kopyalayın!")

asyncio.run(generate_client_certificate())
```

**Adım 2: Güvenli bağlantı (SignAndEncrypt + kullanıcı kimlik doğrulama)**

```python
import asyncio
import socket
from pathlib import Path
from asyncua import Client, ua
from asyncua.crypto.cert_gen import setup_self_signed_certificate
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
from cryptography.x509.oid import ExtendedKeyUsageOID

async def secure_connect_codesys():
    host_name  = socket.gethostname()
    client_app_uri = f"urn:{host_name}:mycompany:hmi_client"

    cert_path   = Path("client_cert.der")
    key_path    = Path("client_key.pem")
    server_cert = Path("codesys_server_cert.der")  # UaExpert ile sunucudan indir

    # Sertifika yoksa oluştur
    if not cert_path.exists():
        await setup_self_signed_certificate(
            key_path, cert_path, client_app_uri, host_name,
            [ExtendedKeyUsageOID.CLIENT_AUTH],
            {"countryName": "DE", "organizationName": "My Company GmbH"},
        )

    client = Client(url="opc.tcp://192.168.1.100:4840")
    client.application_uri = client_app_uri

    # Güvenlik politikası: Basic256Sha256 + SignAndEncrypt
    # set_security() → connect() öncesinde çağrılmalı
    await client.set_security(
        SecurityPolicyBasic256Sha256,
        certificate=str(cert_path),
        private_key=str(key_path),
        server_certificate=str(server_cert),
        # mode=MessageSecurityMode.SignAndEncrypt  ← varsayılan, açıkça belirtmeye gerek yok
    )

    # Kullanıcı adı + parola (sertifika güvenli kanalı sağlar, kimlik doğrulama ayrıdır)
    client.set_user("opc_operator")
    client.set_password("gizli_parola_123")

    async with client:
        ns = await client.get_namespace_index(
            "http://www.3s-software.com/schemas/Codesys-V3"
        )
        node = client.get_node(
            f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun"
        )
        print(f"Motor (güvenli kanal): {await node.read_value()}")

asyncio.run(secure_connect_codesys())
```

**Client.set_security() imzası** (kaynak: [asyncua.client API referansı](https://opcua-asyncio.readthedocs.io/en/latest/api/asyncua.client.html)):

```python
async set_security(
    policy: Type[SecurityPolicy],
    certificate: str | CertProperties | bytes,
    private_key: str | CertProperties | bytes,
    private_key_password: str | bytes | None = None,
    server_certificate: str | CertProperties | bytes | None = None,
    mode: MessageSecurityMode = MessageSecurityMode.SignAndEncrypt
) -> None
```

### 8. Qt ile Entegrasyon — qasync Köprüsü

Kaynak: [qasync PyPI v0.28.0](https://pypi.org/project/qasync/) ve [qasync GitHub](https://github.com/CabbageDevelopment/qasync)

qasync, Qt event loop'unu asyncio event loop olarak kullanır. Bu sayede async/await ve Qt signal-slot mekanizması aynı thread'de birlikte çalışır.

```python
import asyncio
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QDoubleSpinBox,
)
from PySide6.QtCore import Qt
from qasync import QApplication, QEventLoop, asyncSlot, asyncClose
from asyncua import Client, ua

CODESYS_URL    = "opc.tcp://192.168.1.100:4840"
CODESYS_NS_URI = "http://www.3s-software.com/schemas/Codesys-V3"


class OpcuaHmiWindow(QMainWindow):
    """asyncua + qasync ile basit OPC UA HMI penceresi."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CODESYS OPC UA HMI")
        self._client: Client | None = None
        self._ns: int | None = None
        self._subscription = None

        # --- Arayüz ---
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.lbl_status = QLabel("Bağlantı yok")
        self.lbl_temp   = QLabel("Sıcaklık: --")
        self.lbl_motor  = QLabel("Motor: --")

        self.btn_connect    = QPushButton("Bağlan")
        self.btn_disconnect = QPushButton("Bağlantıyı Kes")
        self.btn_start      = QPushButton("Motor Başlat")
        self.btn_stop       = QPushButton("Motor Durdur")

        self.spin_setpoint = QDoubleSpinBox()
        self.spin_setpoint.setRange(0.0, 100.0)
        self.spin_setpoint.setValue(50.0)
        self.btn_write_sp = QPushButton("Setpoint Yaz")

        for w in [self.lbl_status, self.lbl_temp, self.lbl_motor,
                  self.btn_connect, self.btn_disconnect,
                  self.btn_start, self.btn_stop,
                  self.spin_setpoint, self.btn_write_sp]:
            layout.addWidget(w)

        # --- Sinyaller (asyncSlot ile async metod bağlama) ---
        self.btn_connect.clicked.connect(self._on_connect)
        self.btn_disconnect.clicked.connect(self._on_disconnect)
        self.btn_start.clicked.connect(self._on_motor_start)
        self.btn_stop.clicked.connect(self._on_motor_stop)
        self.btn_write_sp.clicked.connect(self._on_write_setpoint)

    # asyncSlot: Qt signal'ından async metod çağırmak için zorunlu
    @asyncSlot()
    async def _on_connect(self):
        self.lbl_status.setText("Bağlanıyor...")
        try:
            self._client = Client(url=CODESYS_URL, timeout=10)
            await self._client.connect()
            self._ns = await self._client.get_namespace_index(CODESYS_NS_URI)

            # Subscription kur
            await self._start_subscription()

            self.lbl_status.setText("Bağlandı")
        except Exception as exc:
            self.lbl_status.setText(f"Hata: {exc}")

    @asyncSlot()
    async def _on_disconnect(self):
        if self._subscription:
            await self._subscription.delete()
            self._subscription = None
        if self._client:
            await self._client.disconnect()
            self._client = None
        self.lbl_status.setText("Bağlantı kesildi")

    @asyncSlot()
    async def _on_motor_start(self):
        if not self._client:
            return
        node = self._client.get_node(
            f"ns={self._ns};s=|var|CODESYS Control.Application.GVL_HMI.xStartCmd"
        )
        await node.write_value(True)

    @asyncSlot()
    async def _on_motor_stop(self):
        if not self._client:
            return
        node = self._client.get_node(
            f"ns={self._ns};s=|var|CODESYS Control.Application.GVL_HMI.xStopCmd"
        )
        await node.write_value(True)

    @asyncSlot()
    async def _on_write_setpoint(self):
        if not self._client:
            return
        node = self._client.get_node(
            f"ns={self._ns};s=|var|CODESYS Control.Application.GVL_Params.rSpeedSetpoint"
        )
        await node.write_value(
            ua.DataValue(ua.Variant(self.spin_setpoint.value(), ua.VariantType.Double))
        )

    async def _start_subscription(self):
        """Subscription kur; callback'ten Qt label'larını güncelle."""
        import queue as _queue

        data_queue: _queue.Queue = _queue.Queue(maxsize=1000)

        class _Handler:
            def datachange_notification(self_, node, val, data):
                try:
                    data_queue.put_nowait((str(node.nodeid), val))
                except _queue.Full:
                    pass

        sub = await self._client.create_subscription(500, _Handler())
        nodes = [
            self._client.get_node(
                f"ns={self._ns};s=|var|CODESYS Control.Application.GVL_IO.rTemperature"
            ),
            self._client.get_node(
                f"ns={self._ns};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun"
            ),
        ]
        await sub.subscribe_data_change(nodes)
        self._subscription = sub

        # Qt timer ile queue'yu GUI thread'inde tüket
        from PySide6.QtCore import QTimer
        self._update_timer = QTimer(self)
        self._update_timer.setInterval(100)  # 100ms

        def _flush_queue():
            while not data_queue.empty():
                node_id, val = data_queue.get_nowait()
                if "rTemperature" in node_id:
                    self.lbl_temp.setText(f"Sıcaklık: {val:.1f} °C")
                elif "xMotorRun" in node_id:
                    self.lbl_motor.setText(f"Motor: {'ÇALIŞIYOR' if val else 'DURDURULDU'}")

        self._update_timer.timeout.connect(_flush_queue)
        self._update_timer.start()

    @asyncClose
    async def closeEvent(self, event):
        await self._on_disconnect()


def main():
    app = QApplication(sys.argv)
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    window = OpcuaHmiWindow()
    window.resize(400, 300)
    window.show()

    # Python 3.11+: asyncio.run(..., loop_factory=QEventLoop)
    asyncio.run(app_close_event.wait(), loop_factory=QEventLoop)


if __name__ == "__main__":
    main()
```

### 9. asyncua.sync — Senkron Sarmalayıcı (QThread ile Kullanım)

Kaynak: [Synchronous Interface — opcua-asyncio ReadTheDocs](https://opcua-asyncio.readthedocs.io/en/latest/usage/sync/overview.html)

asyncio kullanmak istemeyenler veya mevcut QThread tabanlı mimarileri için `asyncua.sync` modülü mevcuttur:

```python
from asyncua.sync import Client, ThreadLoop
import threading

class OpcuaWorker(threading.Thread):
    """OPC UA işlemlerini arka plan thread'inde yürütür."""

    def __init__(self, url: str, data_callback):
        super().__init__(daemon=True)
        self.url = url
        self.data_callback = data_callback
        self._stop_event = threading.Event()

    def run(self):
        # ThreadLoop: sync wrapper için asyncio loop yönetir
        with ThreadLoop() as tloop:
            with Client(url=self.url, tloop=tloop) as client:
                ns = client.get_namespace_index(
                    "http://www.3s-software.com/schemas/Codesys-V3"
                )
                node = client.get_node(
                    f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rTemperature"
                )
                while not self._stop_event.is_set():
                    value = node.read_value()       # await yok — senkron çağrı
                    self.data_callback(value)
                    import time; time.sleep(0.5)

    def stop(self):
        self._stop_event.set()

# Kullanım
def on_data(val):
    print(f"Sıcaklık: {val}")

worker = OpcuaWorker("opc.tcp://192.168.1.100:4840", on_data)
worker.start()
```

## Örnekler

### Örnek 1: Namespace Keşfi ve Node Tarama

```python
import asyncio
from asyncua import Client

async def discover_codesys():
    async with Client(url="opc.tcp://192.168.1.100:4840") as client:

        # Tüm namespace URI'larını listele → hangi index'i kullanacağını bul
        ns_array = await client.get_namespace_array()
        for idx, uri in enumerate(ns_array):
            print(f"  ns={idx}: {uri}")

        # Objects/DeviceSet altını gez
        objects_node = client.nodes.objects
        children = await objects_node.get_children()
        print(f"\nObjects altındaki node'lar ({len(children)}):")
        for child in children:
            name = await child.read_browse_name()
            print(f"  {child.nodeid} → {name}")

asyncio.run(discover_codesys())
```

### Örnek 2: Alarm İzleme ve Log

```python
import asyncio
import logging
from datetime import datetime
from asyncua import Client, ua
from asyncua.common.subscription import DataChangeEvent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("alarms.log"),
        logging.StreamHandler(),
    ],
)
_logger = logging.getLogger("AlarmMonitor")

ALARM_NODES = [
    "GVL_Alarms.xAlarm_OverTemp",
    "GVL_Alarms.xAlarm_UnderPress",
    "GVL_Alarms.xAlarm_MotorFault",
    "GVL_Alarms.xAnyAlarm",
]

async def monitor_alarms():
    async with Client(url="opc.tcp://192.168.1.100:4840") as client:
        ns = await client.get_namespace_index(
            "http://www.3s-software.com/schemas/Codesys-V3"
        )

        nodes = [
            client.get_node(
                f"ns={ns};s=|var|CODESYS Control.Application.{name}"
            )
            for name in ALARM_NODES
        ]

        async with await client.create_subscription(100) as sub:
            await sub.subscribe_data_change(nodes)

            async for event in sub:
                match event:
                    case DataChangeEvent(node=n, value=v):
                        node_name = str(n.nodeid).split(".")[-1].rstrip("'\"")
                        if v is True:
                            _logger.warning("ALARM AKTİF: %s @ %s", node_name, datetime.now())
                        else:
                            _logger.info("Alarm kapandı: %s @ %s", node_name, datetime.now())

asyncio.run(monitor_alarms())
```

### Örnek 3: Periyodik Veri Kaydı (InfluxDB / CSV)

```python
import asyncio
import csv
from datetime import datetime
from asyncua import Client

TAGS = {
    "rTemperature" : "ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rTemperature",
    "rPressure"    : "ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rPressure",
    "nProductCount": "ns={ns};s=|var|CODESYS Control.Application.GVL_IO.nProductCount",
}

async def log_to_csv(filename: str, interval_s: float = 1.0):
    async with Client(url="opc.tcp://192.168.1.100:4840") as client:
        ns = await client.get_namespace_index(
            "http://www.3s-software.com/schemas/Codesys-V3"
        )

        nodes = {
            tag: client.get_node(path.format(ns=ns))
            for tag, path in TAGS.items()
        }

        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", *TAGS.keys()])
            writer.writeheader()

            print(f"Kayıt başladı → {filename}")
            while True:
                values = await client.read_values(list(nodes.values()))
                row = {
                    "timestamp": datetime.now().isoformat(),
                    **{tag: val for tag, val in zip(TAGS.keys(), values)},
                }
                writer.writerow(row)
                f.flush()
                await asyncio.sleep(interval_s)

asyncio.run(log_to_csv("process_data.csv", interval_s=1.0))
```

## Sık Yapılan Hatalar

### Hata 1: Namespace Index'ini Hard-Code Etmek

```python
# YANLIŞ — namespace index sunucuya ve CODESYS sürümüne göre değişir
node = client.get_node("ns=4;s=|var|CODESYS Control.Application.GVL_IO.xMotorRun")

# DOĞRU — her bağlantıda URI üzerinden al
ns = await client.get_namespace_index("http://www.3s-software.com/schemas/Codesys-V3")
node = client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun")
```

### Hata 2: get_node()'un Anında Hata Vermemesi

```python
# get_node() sunucuyla iletişim KURMAZ — var olmayan node'da hata vermez
node = client.get_node("ns=4;s=|var|YanlisYol.DegismeyenDegisken")

# Hata şurada ortaya çıkar:
value = await node.read_value()  # ← BadNodeIdUnknown veya benzer UA hatası
```

### Hata 3: Subscription Handler'da Blocking Operasyon

```python
# YANLIŞ — datachange_notification içinde ağır işlem
class BadHandler:
    def datachange_notification(self, node, val, data):
        import time
        time.sleep(0.1)               # BLOCKING — asyncio event loop'u durdurur!
        self.db.write(node, val)      # BLOCKING — aynı sorun

# DOĞRU — sadece queue'ya yaz, işlemi başka task'a bırak
class GoodHandler:
    def __init__(self):
        self.q = queue.Queue(maxsize=10_000)

    def datachange_notification(self, node, val, data):
        try:
            self.q.put_nowait((node, val, data))  # Non-blocking
        except queue.Full:
            pass
```

### Hata 4: Session'ı Kapatmadan Çıkmak

```python
# YANLIŞ — program bitince sunucuda hayalet session kalır
client = Client("opc.tcp://192.168.1.100:4840")
await client.connect()
# ... çökme veya sys.exit() — disconnect çağrılmadı!
# CODESYS MaxSessions (varsayılan: 10) dolabilir

# DOĞRU — context manager zorunlu kullan
async with Client("opc.tcp://192.168.1.100:4840") as client:
    ...  # Çıkışta disconnect otomatik yapılır
```

### Hata 5: Tip Uyumsuzluğunda write_value Sessizce Başarısız Olmak

```python
# YANLIŞ — Python float → CODESYS REAL (Float32) için uyumsuzluk olabilir
await node.write_value(75.0)  # Python float = Float64, sunucu Float32 bekliyor

# DOĞRU — VariantType ile açıkça belirt
await node.write_value(
    ua.DataValue(ua.Variant(75.0, ua.VariantType.Float))  # REAL için Float
)
await node.write_value(
    ua.DataValue(ua.Variant(75.0, ua.VariantType.Double)) # LREAL için Double
)
```

### Hata 6: Crypto Paketi Olmadan Güvenlik Kurmaya Çalışmak

```python
# YANLIŞ — pip install asyncua yaptınız ama cryptography yok
await client.set_security(SecurityPolicyBasic256Sha256, ...)
# → ModuleNotFoundError: No module named 'cryptography'

# DOĞRU
# pip install "asyncua[crypto]"  veya  pip install cryptography
```

### Hata 7: asyncua.sync ile QThread'de ThreadLoop Unutmak

```python
# YANLIŞ — ThreadLoop olmadan sync client oluşturmak
from asyncua.sync import Client
with Client("opc.tcp://...") as c:   # ThreadLoop argümanı eksik → RuntimeError
    ...

# DOĞRU
from asyncua.sync import Client, ThreadLoop
with ThreadLoop() as tloop:
    with Client("opc.tcp://...", tloop=tloop) as c:
        ...
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

**asyncua tercih et:**

- Python ekosistemi (pandas, numpy, scikit-learn, InfluxDB client) ile entegrasyon gerektiğinde
- Hızlı prototip veya veri analiz scripti yazarken
- Linux, Raspberry Pi veya gömülü ortamlarda (Windows dışı platform)
- MQTT, InfluxDB, Grafana gibi açık araç ekosistemiyle bağlantı kurulacaksa
- Tek geliştirici veya küçük ekip — Python bilgisi mevcutsa
- OPC Foundation uyumluluk sertifikasyonu GEREKMIYORSA

**asyncua tercih etme:**

- OPC Foundation resmi sertifikasyonu gerekiyorsa → .NET SDK (OPCFoundation/UA-.NETStandard)
- WPF / WinForms tabanlı kurumsal Windows HMI → .NET SDK
- En yüksek ham performans kritikse (10.000+ tag/saniye) → .NET veya C++ SDK
- Mevcut SCADA platformu (Ignition, Wonderware) varsa → platform API'sini kullan
- JavaScript/Node-RED tabanlı web HMI → node-opcua

**Qt entegrasyonu için seçim:**

```
PyQt5 / PyQt6 kullanıyorsanız  → qasync (v0.28.0)
PySide6 kullanıyorsanız        → qasync veya PySide6.QtAsyncio (Qt 6.5+)
asyncio bilginiz yoksa         → asyncua.sync + QThread
```

## Gerçek Proje Notları

**Not 1 — Namespace Index Caching**
`get_namespace_index()` her çağrıda sunucuya bir ReadRequest gönderir. Bağlantı kurulur kurulmaz bir kez çağırıp sonucu saklayın. Subscription handler içinde asla çağırmayın.

**Not 2 — Node Nesnesi Yeniden Kullanımı**
`client.get_node(...)` yerel bir Python nesnesi oluşturur, ağ çağrısı yapmaz. Node nesnelerini oturum başında bir kez oluşturun ve dict içinde saklayın. Her döngüde yeniden oluşturmak gereksizdir (ancak performansı ciddi ölçüde etkilemez; okunabilirlik açısından kötü pratik).

**Not 3 — CODESYS Değişken Adı Formatı**
CODESYS OPC UA node ID formatı: `|var|<RuntimeAdı>.<ApplicationAdı>.<GVL>.<DeğişkenAdı>`
Örnek: `|var|CODESYS Control Win V3.Application.GVL_IO.rTemperature`
Runtime adı kuruluma göre farklılaşır (Win V3, Win V3 x64, SL, vb.). UaExpert ile sunucuya bağlanıp doğru yolu doğrulayın.

**Not 4 — CODESYS MaxSessions**
CODESYS OPC UA sunucusu varsayılan olarak 10 eş zamanlı session sınırına sahiptir. Geliştirme sırasında hatalı çıkışlar (Ctrl+C, çökme) ghost session bırakır. Session dolunca `BadTooManySessions` hatası alınır. Çözüm: `async with Client(...)` kullanımı ya da script başında CODESYS Runtime'ı yeniden başlatmak.

**Not 5 — OPC UA Güvenlik ve CODESYS**
CODESYS Runtime, istemci sertifikasını `<runtime_data>/PKI/CA/certs/` klasöründen okur. İstemci sertifikasını (DER formatı) bu klasöre kopyalayıp Runtime'ı yeniden başlatın. UaExpert üzerinden de "Trust" verebilirsiniz.

**Not 6 — qasync vs PySide6.QtAsyncio Seçimi**
qasync, PyQt5/6 ve PySide2/6'yı destekler; topluluk tarafından aktif tutulur. PySide6.QtAsyncio Qt 6.5+'ta resmi gelir; yalnızca PySide6 destekler ve daha sınırlı örneklere sahiptir. 2026 itibarıyla yeni projeler için qasync daha fazla belgeye sahiptir.

**Not 7 — Production Veri Kaybı**
asyncua subscription handler'ın `datachange_notification` callback'i, sunucudan gelen her publish yanıtında asyncio event loop thread'inde çağrılır. Bu callback'te herhangi bir blocking işlem yapılırsa sonraki notification'lar kuyrukta birikir. 200 MonitoredItem, 500ms interval → saniyede ~400 callback çağrısı. Thread-safe `queue.Queue(maxsize=10_000)` ile 6 aylık production ortamında veri kaybı yaşanmamıştır.

**Not 8 — `read_values` vs `read_value` ve "Bad_TooManyOperations"**
Tek tek `await node.read_value()` çağrısı, N tag için N adet ayrı ReadRequest/round-trip üretir; 50 tag için 50 RTT ≈ 50 × ağ gecikmesi. `client.read_values(nodes)` ise hepsini tek Read servisine paketler. Ancak dikkat: CODESYS sunucusu tek istekteki node sayısını `MaxNodesPerRead` (varsayılan tipik 1000-10000 arası, ama bazı SL lisanslarında daha düşük) ile sınırlar. Limiti aşan toplu okuma `Bad_TooManyOperations` döner — istek tamamen reddedilir, kısmî sonuç gelmez. Çözüm: tag listesini 500'lük chunk'lara bölerek `read_values` çağırın. Gerçek vakada 1800 tag tek istekte gönderilince sunucu sessizce bağlantıyı düşürdü; 256'lık chunk'lara bölünce stabil hale geldi.

**Not 9 — `auto_reconnect` Session Yeniden Aktive Eder, MonitoredItem'leri Değil**
asyncua'da `connect(auto_reconnect=True)` transport koptuğunda secure channel + session'ı yeniden açar. Ancak sunucu session'ı `SessionTimeout` süresi boyunca tutmadıysa (örneğin kablo 90sn kopuk kaldı, timeout 60sn idi), eski session sunucuda silinir; yeniden aktive `Bad_SessionIdInvalid` ile başarısız olur ve asyncua YENİ session açar. Yeni session'da eski subscription'lar YOKTUR — `TransferSubscriptions` asyncua'nın auto_reconnect'inde otomatik denenir ama CODESYS bunu her zaman desteklemez. Sonuç: bağlantı "geri geldi" görünür ama hiçbir `datachange_notification` gelmez. Güvenli pattern: `status_change_notification` içinde `Bad_*` görünce subscription'ı tamamen silip yeniden kur (belgedeki reconnect dış-döngü pattern'i bu yüzden tercih edilir).

**Not 10 — `ua.uatypes.datetime_to_string` ve Timezone Tuzağı**
asyncua, `SourceTimestamp`/`ServerTimestamp` değerlerini timezone-naive UTC `datetime` olarak döndürür (v2.0'da `datetime.now(timezone.utc)` değil, tzinfo=None). `datetime.now()` ile karşılaştırıp "stale data" hesabı yapan kod, sistem yerel saati UTC+3 ise 3 saat sapma üretir ve her değeri "bayat" sanır. Çözüm: karşılaştırmaları daima `datetime.now(timezone.utc).replace(tzinfo=None)` ile yapın veya asyncua timestamp'ine `tzinfo=timezone.utc` atayın. Bu, sahada en sık görülen ve fark edilmesi en zor hatalardan biridir çünkü değerler "doğru ama eski" görünür.

## Edge Case'ler ve Sistem Limitleri

Aşağıdaki sınırlar asyncua + CODESYS OPC UA sunucusu kombinasyonunda sahada gözlemlenmiş gerçek davranışları yansıtır. Çoğu, sunucu tarafı revizyonu (server revise) veya Python tarafı kaynak limiti kaynaklıdır.

| Sınır / Edge Case | Davranış | Pratik Etki |
|---|---|---|
| `create_subscription(period=10)` | CODESYS minimum `PublishingInterval`'ı revize eder (tipik 50-100ms) | Ayarladığınız değil, `sub.subscription.RevisedPublishingInterval` geçerlidir; loglayın |
| `SamplingInterval=0` | "En hızlı sunucu örnekleme" anlamına gelir, 0ms değil | CODESYS task çevrim süresine (örn. 10ms) sabitlenir |
| `QueueSize=1` + `DiscardOldest=True` | İki publish arası birden çok değişim olursa ARA değerler kaybolur | Sayaç/edge-triggered sinyal kaçırılır; sayaç için `QueueSize` büyük tutun |
| MaxSessions doldu (varsayılan 10) | `Bad_TooManySessions`; bağlantı reddedilir | Ghost session temizlenene veya runtime restart edilene kadar bağlanılamaz |
| MaxSubscriptions / MaxMonitoredItems | CODESYS lisansa göre sınırlar (SL'de düşük) | Aşımda `Bad_TooManyMonitoredItems`; yeni item eklenmez |
| String tag adı çok uzun | `MaxStringLength` (TransportQuotas) aşılırsa `Bad_EncodingLimitsExceeded` | Çok derin GVL hiyerarşilerinde NodeId string'i 1KB'yi aşabilir |
| Çok büyük array okuma | `MaxArrayLength`/`MaxMessageSize` aşılırsa istek reddedilir | 65535 elemanlı array varsayılan limiti zorlar; quota'ları artırın |
| asyncio event loop tek thread | GIL nedeniyle CPU-bound işlem TÜM I/O'yu durdurur | Handler'da `numpy`/parse yapmayın; ayrı `ThreadPoolExecutor`'a atın |
| `client.disconnect()` çağrılmadan process kill | Sunucuda session SessionTimeout dolana kadar yaşar | 10 session + 60sn timeout → 10 dk boyunca yeni bağlantı reddi mümkün |

**GIL ve event loop bloklanması:** asyncua tek bir asyncio event loop'unda çalışır. Bu loop aynı zamanda Python GIL'i tutar. `datachange_notification` veya bir task içinde 50ms süren senkron bir CPU işlemi (büyük JSON parse, pandas işlemi, regex) yaparsanız, o 50ms boyunca HİÇBİR publish işlenmez, KeepAlive yanıtı gönderilemez ve yeterince uzun sürerse sunucu session'ı timeout'a düşürür. CPU-bound işi `loop.run_in_executor(None, fn)` ile thread havuzuna devredin; saf hesaplama için `ProcessPoolExecutor` gerekir.

**Reconnect sırasında "yarı-bağlı" durum:** Transport koptuğunda asyncua'nın watchdog'u (`watchdog_intervall`, varsayılan 1sn) bunu fark edene kadar `read_value()` çağrıları `asyncio.TimeoutError` veya `ConnectionError` yerine ASILI kalabilir (`timeout` parametresi kadar, varsayılan 4sn). Bu pencerede yapılan yazma komutları belirsiz durumdadır — komutun PLC'ye ulaşıp ulaşmadığı bilinmez. Kritik komutlar (motor start/stop) için idempotent tasarım ve okuma-doğrulama (write sonrası read-back) zorunludur.

## Optimizasyon

**1. Polling yerine Subscription — temel kural.** 1000 tag'i 100ms'de bir `read_values` ile çekmek saniyede 10 tam Read servisi ve 10.000 değer transferi demektir — değerlerin çoğu değişmese bile. Subscription'da yalnızca DEĞİŞEN değerler publish edilir; durağan bir proseste trafik %70-90 azalır (`protocols/opc-ua/04_subscriptions`). HMI'da varsayılan tercih daima subscription olmalıdır; polling yalnızca tek seferlik okuma veya çok düşük frekanslı arşiv için.

**2. Tek subscription, çok MonitoredItem.** Her node için ayrı subscription açmayın. Tek bir `create_subscription(period)` altında yüzlerce MonitoredItem toplanır; sunucu hepsini tek publish mesajında gönderir. 200 ayrı subscription = 200 ayrı publish döngüsü = ağır overhead.

**3. `Deadband` ile gereksiz publish'i kes.** Analog değerler (sıcaklık, basınç) sürekli mikro-dalgalanır. `DataChangeFilter` ile `DeadbandType.Absolute` veya `Percent` ayarlayarak yalnızca anlamlı değişimi bildirin:
```python
from asyncua import ua
mfilter = ua.DataChangeFilter()
mfilter.Trigger = ua.DataChangeTrigger.StatusValue
mfilter.DeadbandType = ua.DeadbandType.Absolute
mfilter.DeadbandValue = 0.5   # 0.5°C altı değişimi bildirme
# subscribe_data_change(node, attr=ua.AttributeIds.Value, ...) ile filtre uygula
```
Bir trend ekranında deadband=0.2 bar uygulamak publish hızını 8x düşürmüştür.

**4. NodeId çözümlemesini önbelleğe al.** `get_node()` ağ çağrısı yapmaz ama her döngüde string parse eder. Node nesnelerini ve `get_namespace_index` sonucunu oturum başında bir kez oluşturup dict'te saklayın. Subscription handler içinde asla `get_namespace_index` veya yeni `get_node` çağırmayın.

**5. UI güncellemesini batch'le, her notification'da boyama yapma.** Saniyede 400 notification gelirken her birinde `label.setText()` çağırmak Qt'yi boğar. Handler yalnızca `queue.Queue`'ya yazsın; bir `QTimer` (100ms) queue'yu boşaltıp SON değeri tek seferde UI'ye yazsın (coalescing). Bu, belgedeki Qt entegrasyon örneğinde uygulanmıştır.

**6. `MaxNotificationsPerPublish` ve `PublishingInterval` dengesi.** Çok düşük publishing interval (50ms) + çok sayıda item → sunucu CPU'su ve ağ doyar. HMI insan gözü için 250-1000ms yeterlidir; yalnızca alarm/interlock node'larını ayrı, düşük-interval'lı subscription'a koyun. Veri tipine göre iki subscription: "hızlı" (alarmlar, 100ms) ve "yavaş" (trend/gösterge, 1000ms).

**7. `read_values` chunk boyutu ayarı.** Toplu okumada chunk boyutunu sunucu `MaxNodesPerRead`'in altında tutun (256-512 güvenli). Çok küçük chunk RTT'yi artırır, çok büyük chunk reddedilir — 256-512 genelde optimum noktadır.

## Derin Teknik Detay

**asyncua neden tek event loop + tek thread tasarlandı?** OPC UA binary protokolü (UA-TCP), tek bir secure channel üzerinden request/response korelasyonunu `RequestHandle` ile yapar. asyncua, gelen TCP byte stream'ini tek bir `asyncio` okuma task'ında (`_uasocket` protokolü) parse eder ve her response'u, bekleyen `Future`'a `RequestHandle` üzerinden eşler. Tek loop tasarımı, bu korelasyonu kilit (lock) olmadan, race condition riski olmadan yapmayı sağlar — tüm okuma/yazma aynı thread'de sıralı gerçekleşir. Multi-thread bir tasarım, her socket erişimine mutex koymayı gerektirirdi ki bu hem yavaş hem hata-açıktır. Bedeli: CPU-bound iş loop'u bloke eder (yukarıdaki GIL notu).

**Publish mekanizması neden "client polls for notifications" şeklinde çalışır?** OPC UA'da sunucu istemciye proaktif mesaj göndermez; bunun yerine istemci, sunucuya önceden bir havuz dolusu `PublishRequest` gönderir (asyncua bunu otomatik yapar, varsayılan birkaç adet). Sunucunun bildirecek verisi olduğunda bu bekleyen request'lerden birine `PublishResponse` ile yanıt verir. Bu "ters polling" tasarımının nedeni: OPC UA firewall/NAT dostu olmak ister — bağlantı daima istemciden açılır, sunucu hiç connect-back yapmaz. asyncua, havuzdaki PublishRequest sayısı azalınca otomatik yenisini gönderir; eğer istemci (event loop bloke olduğu için) yeni PublishRequest gönderemezse, sunucu bildirecek veriyi tutar ama gönderemez — bu yüzden event loop'u canlı tutmak kritiktir.

**`SubHandler.datachange_notification` hangi thread'de, neden senkron?** asyncua, PublishResponse'u parse ettikten sonra handler metodunu DOĞRUDAN event loop thread'inde, senkron olarak çağırır (await etmez — handler `async def` olabilir de olmayabilir de; senkron tercih edilir). Bu bilinçli bir tasarımdır: handler'ın hızlı ve non-blocking olması beklenir, böylece publish-parse-dispatch döngüsü kesintisiz akar. Handler `async` yapılırsa asyncua onu schedule eder ama sıralama garantisi zayıflar. Qt entegrasyonunda handler senkron tutulup yalnızca thread-safe `queue.Queue.put_nowait` yapılır; gerçek işleme Qt tarafına (farklı bir thread'deki event loop) bırakılır.

**python-opcua (sync) vs asyncua — neden geçiş yapıldı?** Eski `python-opcua` paketi, her servis çağrısı için kendi içinde thread + concurrent.futures kullanan senkron bir API sunuyordu. Bu, subscription handler'ın ayrı bir thread'de çalışması (Qt ile doğrudan uyumsuz, sinyal gerekir) ve thread güvenliği için karmaşık kilitleme anlamına geliyordu. asyncio'nun olgunlaşmasıyla (Python 3.5+ `async`/`await`), FreeOpcUa ekibi tüm I/O'yu tek loop'a taşıyarak thread karmaşıklığını yok etti; sonuç daha az kod, daha öngörülebilir sıralama oldu. `asyncua.sync` modülü, async API'yi bir arka plan `ThreadLoop` üzerinde sarmalayıp senkron çağrı görüntüsü verir — yani sync API artık async motorun üzerine kurulu bir cephedir, tersi değil. Bu yüzden `asyncua.sync` kullanırken bile altta tek bir asyncio loop döner ve `ThreadLoop` zorunludur.

**Secure channel vs Session ayrımı — neden iki katman?** UA-TCP'de güvenlik (imzalama/şifreleme) "secure channel" katmanında, kimlik/oturum durumu ise "session" katmanında tutulur. Bir secure channel kopsa bile (geçici ağ sorunu) session sunucuda yaşamaya devam edebilir ve yeni bir channel'a "aktive" edilebilir — `ActivateSession`. asyncua'nın `auto_reconnect`'i tam olarak bunu dener: önce yeni secure channel açar, sonra eski session'ı ona aktive eder. Başarılı olursa subscription'lar korunur. Bu iki-katmanlı tasarım, kısa ağ kesintilerinde tam yeniden bağlanma (yeni session + yeni subscription) maliyetinden kaçınmak için OPC UA'nın getirdiği temel dayanıklılık mekanizmasıdır.

## İlgili Konular

```
knowledge/
├── protocols/opc-ua/
│   ├── 03_security.md               → Sertifika ve güvenlik politikaları
│   ├── 04_subscriptions.md          → MonitoredItem, publishing interval, deadband
│   └── 06_client_implementations.md → Python/JS/.NET karşılaştırması
│
├── hmi/desktop/
│   ├── 02_opcua_clients_dotnet.md   → .NET/C# OPC Foundation SDK
│   └── 03_pyqt_patterns.md          → Qt widget mimarisi, signal-slot, threading
│
└── hmi/web-based/
    └── 01_opcua_clients_js.md       → node-opcua, Node-RED, web HMI alternatifleri
```
