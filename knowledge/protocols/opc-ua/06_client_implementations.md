---
KONU        : OPC-UA İstemci Implementasyonları
KATEGORİ    : protocols
ALT_KATEGORI: opc-ua
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://github.com/FreeOpcUa/opcua-asyncio"
    başlık: "GitHub — FreeOpcUa/opcua-asyncio (Python)"
    güvenilirlik: topluluk
  - url: "https://opcua-asyncio.readthedocs.io/en/latest/usage/get-started/minimal-client.html"
    başlık: "opcua-asyncio ReadTheDocs — Minimal Client"
    güvenilirlik: topluluk
  - url: "https://node-opcua.github.io/"
    başlık: "NodeOPCUA — OPC UA SDK for Node.js"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "01_architecture.md"
    ilişki: gerektirir
  - konu: "02_address_space.md"
    ilişki: gerektirir
  - konu: "03_security.md"
    ilişki: kullanır
  - konu: "04_subscriptions.md"
    ilişki: kullanır
ÖNKOŞUL     :
  - "OPC UA temel kavramları (01_architecture.md - 04_subscriptions.md)"
  - "Python, JavaScript veya C# programlama bilgisi"
ÇELİŞKİLER :
  - kaynak: "python-opcua (eski) vs asyncua (yeni)"
    konu: "python-opcua artık unmaintained; asyncua aktif gelişimde"
    çözüm: >
      python-opcua (opcua paketi) artık geliştirilmiyor.
      Yeni projeler için asyncua (opcua-asyncio) kullanılmalı.
      API büyük ölçüde benzer ama async/await syntax zorunlu.
      Python >= 3.10 önerilir (typing desteği için).
  - kaynak: "OPC Foundation .NET SDK vs community .NET kütüphaneleri"
    konu: "OPC Foundation resmi SDK karmaşık; community alternatifleri daha kolay"
    çözüm: >
      OPC Foundation SDK (OPCFoundation/UA-.NETStandard): Resmi, tam özellikli.
      OpcUaHelper, WorkstationOpcUaClient: Daha kolay API.
      Basit projeler için OpcUaHelper önerilir.
      Enterprise, özel güvenlik veya OPC Foundation sertifikasyonu gerekiyorsa resmi SDK.
---

## Özün Ne

OPC UA sunucusuna bağlanmak için birçok programlama dilinde açık kaynak ve ticari kütüphaneler mevcuttur. Bu belge, en yaygın üç ekosistemi ele alır: **Python** (asyncua), **JavaScript/Node.js** (node-opcua) ve **.NET/C#** (OPC Foundation SDK). Her birinde bağlantı kurma, node okuma/yazma, subscription oluşturma ve güvenli bağlantı örnekleri verilmiştir. Kütüphane seçimi rehberi belgenin sonunda yer almaktadır.

## Python — asyncua (opcua-asyncio)

### Kurulum

```bash
pip install asyncua

# TLS/güvenlik için ek paket
pip install asyncua[crypto]
# veya
pip install cryptography
```

### Temel Bağlantı ve Okuma

```python
import asyncio
from asyncua import Client, ua

async def basic_read():
    """Basit bağlantı ve değer okuma."""
    
    # Context manager — disconnect otomatik yapılır
    async with Client(url="opc.tcp://192.168.1.100:4840") as client:
        
        # Namespace index'i URI'dan al (taşınabilir!)
        ns = await client.get_namespace_index(
            "http://www.3s-software.com/schemas/Codesys-V3"
        )
        print(f"CODESYS namespace index: {ns}")
        
        # Node'u NodeID string ile al
        node = client.get_node(
            f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun"
        )
        
        # Değeri oku
        value = await node.read_value()
        print(f"Motor Run: {value}")
        
        # DataValue (değer + timestamp + status) oku
        data_value = await node.read_data_value()
        print(f"Value      : {data_value.Value.Value}")
        print(f"StatusCode : {data_value.StatusCode}")
        print(f"Timestamp  : {data_value.SourceTimestamp}")
        
        # Birden fazla node'u toplu oku (verimli)
        nodes = [
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rTemperature"),
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rPressure"),
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.xConveyor1Run")
        ]
        values = await client.read_values(nodes)
        print(f"Temp={values[0]}, Pressure={values[1]}, Conv={values[2]}")

asyncio.run(basic_read())
```

### Değer Yazma

```python
async def write_values():
    async with Client(url="opc.tcp://192.168.1.100:4840") as client:
        
        ns = await client.get_namespace_index(
            "http://www.3s-software.com/schemas/Codesys-V3"
        )
        
        # Tek değer yaz
        setpoint_node = client.get_node(
            f"ns={ns};s=|var|CODESYS Control.Application.GVL_Params.rSpeedSetpoint"
        )
        await setpoint_node.write_value(
            ua.DataValue(ua.Variant(75.0, ua.VariantType.Double))
        )
        print("Setpoint yazıldı: 75.0")
        
        # BOOL değer yaz
        start_cmd = client.get_node(
            f"ns={ns};s=|var|CODESYS Control.Application.GVL_HMI.xStartCmd"
        )
        await start_cmd.write_value(True)
        print("Start komutu gönderildi")
        
        # INT değer yaz
        recipe_node = client.get_node(
            f"ns={ns};s=|var|CODESYS Control.Application.GVL_Params.nRecipeID"
        )
        await recipe_node.write_value(
            ua.DataValue(ua.Variant(3, ua.VariantType.Int16))
        )

asyncio.run(write_values())
```

### Subscription

```python
import asyncio
import queue
from asyncua import Client

class DataHandler:
    """Thread-safe, non-blocking handler."""
    
    def __init__(self):
        self.q = queue.Queue(maxsize=10000)
    
    def datachange_notification(self, node, val, data):
        """Hızlı olmalı — block etmemeli."""
        try:
            self.q.put_nowait({
                'node': str(node.nodeid),
                'value': val,
                'timestamp': data.monitored_item.Value.SourceTimestamp
            })
        except queue.Full:
            pass

async def run_subscription():
    
    handler = DataHandler()
    
    async with Client(url="opc.tcp://192.168.1.100:4840") as client:
        ns = await client.get_namespace_index(
            "http://www.3s-software.com/schemas/Codesys-V3"
        )
        
        # Subscription kur
        subscription = await client.create_subscription(
            period=500,    # Publishing interval: 500ms
            handler=handler
        )
        
        # İzlenecek node'lar
        nodes = [
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.rTemperature"),
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun"),
            client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_Alarms.xAnyAlarm"),
        ]
        
        handles = await subscription.subscribe_data_change(nodes)
        
        print("Subscription aktif. Ctrl+C ile dur.")
        
        # Handler queue'sunu işle
        try:
            while True:
                await asyncio.sleep(0.1)
                while not handler.q.empty():
                    item = handler.q.get_nowait()
                    print(f"[{item['timestamp']}] {item['node'].split('.')[-1]} = {item['value']}")
        except asyncio.CancelledError:
            pass
        finally:
            await subscription.unsubscribe(handles)
            await subscription.delete()

asyncio.run(run_subscription())
```

### Güvenli Bağlantı (SignAndEncrypt)

```python
import asyncio
from asyncua import Client
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
from asyncua.crypto.cert_gen import generate_self_signed_app_certificate
from pathlib import Path
import os

async def create_client_cert():
    """İstemci sertifikası oluştur — bir kez yapılır."""
    cert_path = Path("client_cert.der")
    key_path = Path("client_key.pem")
    
    if not cert_path.exists():
        names = {
            "countryName": "DE",
            "stateOrProvinceName": "Bavaria",
            "localityName": "Munich",
            "organizationName": "Acme Automation",
            "commonName": "OPCUAClient"
        }
        cert, key = generate_self_signed_app_certificate(
            "MyOPCUAClientApp",
            "urn:myapp:client",
            hostnames=["localhost"],
            years_valid=10,
            subject_alternative_names=[],
            **names
        )
        cert_path.write_bytes(cert)
        key_path.write_bytes(key)
        print(f"Sertifika oluşturuldu: {cert_path}")
        print("Sunucunun trusted/certs/ klasörüne kopyala!")

async def secure_connect():
    await create_client_cert()
    
    client = Client(url="opc.tcp://192.168.1.100:4840")
    
    await client.set_security(
        SecurityPolicyBasic256Sha256,
        certificate=Path("client_cert.der").read_bytes(),
        private_key=Path("client_key.pem").read_bytes(),
        server_certificate=Path("server_cert.der").read_bytes()
    )
    
    client.set_user("opc_operator")
    client.set_password("secure_password")
    
    await client.connect()
    
    try:
        ns = await client.get_namespace_index(
            "http://www.3s-software.com/schemas/Codesys-V3"
        )
        node = client.get_node(f"ns={ns};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun")
        print(f"Motor: {await node.read_value()}")
    finally:
        await client.disconnect()

asyncio.run(secure_connect())
```

---

## JavaScript / Node.js — node-opcua

### Kurulum

```bash
npm install node-opcua
# veya
yarn add node-opcua
```

### Bağlantı, Okuma ve Yazma

```javascript
const { OPCUAClient, AttributeIds, DataType, resolveNodeId } = require("node-opcua");

async function basicOpcUaClient() {
    const client = OPCUAClient.create({
        applicationName: "MyNodeJSClient",
        connectionStrategy: {
            initialDelay: 1000,
            maxRetry: 5             // Bağlantı kesilirse 5 kez dene
        },
        securityMode: "None",       // Test için
        securityPolicy: "None",
        endpoint_must_exist: false
    });

    const endpointUrl = "opc.tcp://192.168.1.100:4840";

    await client.connect(endpointUrl);
    console.log("Connected.");

    const session = await client.createSession({
        userName: "opc_user",
        password: "password123"
    });
    console.log("Session created.");

    try {
        // Namespace index al
        const nsUri = "http://www.3s-software.com/schemas/Codesys-V3";
        const nsIndex = await session.getNamespaceIndex(nsUri);
        console.log(`Namespace index: ${nsIndex}`);

        const motorNodeId = `ns=${nsIndex};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun`;
        const tempNodeId   = `ns=${nsIndex};s=|var|CODESYS Control.Application.GVL_IO.rTemperature`;

        // Tek değer oku
        const motorResult = await session.readVariableValue(motorNodeId);
        console.log("Motor Run:", motorResult.value.value);
        console.log("StatusCode:", motorResult.statusCode.toString());

        // Toplu okuma (verimli)
        const readResults = await session.read([
            { nodeId: motorNodeId, attributeId: AttributeIds.Value },
            { nodeId: tempNodeId,  attributeId: AttributeIds.Value }
        ]);
        console.log("Motor:", readResults[0].value.value);
        console.log("Temp:", readResults[1].value.value);

        // Değer yaz
        const setpointNodeId = `ns=${nsIndex};s=|var|CODESYS Control.Application.GVL_Params.rSpeedSetpoint`;
        const writeStatus = await session.writeSingleNode(
            setpointNodeId,
            { dataType: DataType.Double, value: 65.0 }
        );
        console.log("Write status:", writeStatus.toString());

    } finally {
        await session.close();
        await client.disconnect();
    }
}

basicOpcUaClient().catch(console.error);
```

### Subscription (Node.js)

```javascript
const { OPCUAClient, ClientSubscription, ClientMonitoredItem,
        TimestampsToReturn, MonitoringParametersOptions, AttributeIds } = require("node-opcua");

async function subscriptionExample() {
    const client = OPCUAClient.create({ endpointMustExist: false });
    await client.connect("opc.tcp://192.168.1.100:4840");
    
    const session = await client.createSession();
    const nsIndex = await session.getNamespaceIndex(
        "http://www.3s-software.com/schemas/Codesys-V3"
    );

    // Subscription oluştur
    const subscription = await ClientSubscription.create(session, {
        requestedPublishingInterval: 500,      // 500ms publishing
        requestedMaxKeepAliveCount: 10,
        requestedLifetimeCount: 120,
        maxNotificationsPerPublish: 1000,
        publishingEnabled: true,
        priority: 128
    });

    subscription.on("started", () => {
        console.log(`Subscription started (ID: ${subscription.subscriptionId})`);
    });
    subscription.on("terminated", () => {
        console.log("Subscription terminated");
    });

    // MonitoredItem ekle
    const itemsToMonitor = [
        `ns=${nsIndex};s=|var|CODESYS Control.Application.GVL_IO.xMotorRun`,
        `ns=${nsIndex};s=|var|CODESYS Control.Application.GVL_IO.rTemperature`,
        `ns=${nsIndex};s=|var|CODESYS Control.Application.GVL_Alarms.xAnyAlarm`
    ];

    for (const nodeIdStr of itemsToMonitor) {
        const monitoredItem = await ClientMonitoredItem.create(
            subscription,
            { nodeId: nodeIdStr, attributeId: AttributeIds.Value },
            {
                samplingInterval: 100,    // 100ms örnekleme
                discardOldest: true,
                queueSize: 10
            },
            TimestampsToReturn.Source
        );

        monitoredItem.on("changed", (dataValue) => {
            const varName = nodeIdStr.split(".").pop();
            console.log(`[${new Date(dataValue.sourceTimestamp).toISOString()}] ${varName} = ${dataValue.value.value}`);
        });
    }

    // 60 saniye çalış
    await new Promise(resolve => setTimeout(resolve, 60000));

    await subscription.terminate();
    await session.close();
    await client.disconnect();
}

subscriptionExample().catch(console.error);
```

### Güvenli Bağlantı (Node.js)

```javascript
const { OPCUAClient, MessageSecurityMode, SecurityPolicy, OPCUACertificateManager } = require("node-opcua");
const path = require("path");

async function secureConnect() {
    // Sertifika yöneticisi
    const certificateManager = new OPCUACertificateManager({
        automaticallyAcceptUnknownCertificate: false,
        rootFolder: path.join(__dirname, "pki")  // PKI klasörü
    });
    await certificateManager.initialize();

    const client = OPCUAClient.create({
        applicationName: "SecureNodeJSClient",
        applicationUri: "urn:mynodejsclient",
        securityMode: MessageSecurityMode.SignAndEncrypt,
        securityPolicy: SecurityPolicy.Basic256Sha256,
        certificateFile: path.join(__dirname, "pki", "own", "certs", "client.pem"),
        privateKeyFile: path.join(__dirname, "pki", "own", "private", "private_key.pem"),
        certificateManager: certificateManager
    });

    await client.connect("opc.tcp://192.168.1.100:4840");
    
    const session = await client.createSession({
        userName: "opc_scada",
        password: "scada_password"
    });
    
    try {
        const ns = await session.getNamespaceIndex(
            "http://www.3s-software.com/schemas/Codesys-V3"
        );
        const result = await session.readVariableValue(
            `ns=${ns};s=|var|CODESYS Control.Application.GVL_IO.rTemperature`
        );
        console.log("Temperature:", result.value.value);
    } finally {
        await session.close();
        await client.disconnect();
    }
}

secureConnect().catch(console.error);
```

---

## .NET / C# — OPC Foundation SDK

### Kurulum

```bash
# NuGet
dotnet add package OPCFoundation.NetStandard.Opc.Ua
dotnet add package OPCFoundation.NetStandard.Opc.Ua.Client

# veya Package Manager Console
Install-Package OPCFoundation.NetStandard.Opc.Ua
```

### Bağlantı ve Okuma

```csharp
using Opc.Ua;
using Opc.Ua.Client;
using Opc.Ua.Configuration;

class OpcUaClientExample
{
    private Session _session;

    public async Task ConnectAsync(string endpointUrl)
    {
        // Uygulama konfigürasyonu
        var config = new ApplicationConfiguration
        {
            ApplicationName = "MyCSharpOpcUaClient",
            ApplicationType = ApplicationType.Client,
            SecurityConfiguration = new SecurityConfiguration
            {
                ApplicationCertificate = new CertificateIdentifier
                {
                    StoreType = "Directory",
                    StorePath = "./pki/own",
                    SubjectName = "CN=MyCSharpOpcUaClient, O=Acme Automation"
                },
                TrustedIssuerCertificates = new CertificateTrustList
                {
                    StoreType = "Directory",
                    StorePath = "./pki/issuers"
                },
                TrustedPeerCertificates = new CertificateTrustList
                {
                    StoreType = "Directory",
                    StorePath = "./pki/trusted"
                },
                AutoAcceptUntrustedCertificates = false,    // Üretime güvenli
                RejectSHA1SignedCertificates = true
            },
            TransportQuotas = new TransportQuotas { OperationTimeout = 15000 },
            ClientConfiguration = new ClientConfiguration { DefaultSessionTimeout = 60000 }
        };

        await config.Validate(ApplicationType.Client);

        // Sertifika otomatik oluştur (yoksa)
        if (!config.SecurityConfiguration.ApplicationCertificate.Certificate.HasPrivateKey)
        {
            await CertificateFactory.CreateCertificate(
                config.SecurityConfiguration.ApplicationCertificate.StoreType,
                config.SecurityConfiguration.ApplicationCertificate.StorePath,
                null, config.ApplicationUri, config.ApplicationName,
                config.SecurityConfiguration.ApplicationCertificate.SubjectName,
                null, CertificateFactory.DefaultKeySize, DateTime.UtcNow - TimeSpan.FromDays(1),
                CertificateFactory.DefaultLifeTime, CertificateFactory.DefaultHashSize,
                isCA: false);
        }

        // Endpoint bul ve session kur
        var endpoint = CoreClientUtils.SelectEndpoint(
            config, endpointUrl,
            useSecurity: true    // Security endpoint tercih et
        );
        
        var configuredEndpoint = new ConfiguredEndpoint(
            null, endpoint, EndpointConfiguration.Create(config)
        );

        _session = await Session.Create(
            config, configuredEndpoint,
            updateBeforeConnect: false,
            checkDomain: false,
            sessionName: "MySession",
            sessionTimeout: 60000,
            identity: new UserNameIdentityToken
            {
                UserName = "opc_user",
                DecryptedPassword = "password"
            },
            preferredLocales: null
        );

        Console.WriteLine($"Connected. Session ID: {_session.SessionId}");
    }

    public async Task ReadWriteAsync()
    {
        // Namespace index al
        var ns = _session.NamespaceUris.GetIndex(
            "http://www.3s-software.com/schemas/Codesys-V3"
        );

        // Değer oku
        var motorNodeId = new NodeId(
            $"|var|CODESYS Control.Application.GVL_IO.xMotorRun", (ushort)ns
        );
        
        DataValue motorValue = _session.ReadValue(motorNodeId);
        Console.WriteLine($"Motor: {motorValue.Value}");
        Console.WriteLine($"Status: {motorValue.StatusCode}");
        Console.WriteLine($"Timestamp: {motorValue.SourceTimestamp}");

        // Toplu okuma (verimli)
        var nodesToRead = new ReadValueIdCollection
        {
            new ReadValueId { NodeId = motorNodeId, AttributeId = Attributes.Value },
            new ReadValueId
            {
                NodeId = new NodeId("|var|CODESYS Control.Application.GVL_IO.rTemperature", (ushort)ns),
                AttributeId = Attributes.Value
            }
        };

        _session.Read(null, 0, TimestampsToReturn.Source,
            nodesToRead, out DataValueCollection results, out _);

        Console.WriteLine($"Motor: {results[0].Value}, Temp: {results[1].Value}");

        // Değer yaz
        var setpointNodeId = new NodeId(
            "|var|CODESYS Control.Application.GVL_Params.rSpeedSetpoint", (ushort)ns
        );
        _session.WriteValue(setpointNodeId, new DataValue(new Variant(75.0)));
    }

    public async Task CreateSubscriptionAsync()
    {
        var ns = _session.NamespaceUris.GetIndex(
            "http://www.3s-software.com/schemas/Codesys-V3"
        );

        // Subscription oluştur
        var subscription = new Subscription(_session.DefaultSubscription)
        {
            PublishingInterval = 500,       // 500ms
            LifetimeCount = 100,
            MaxNotificationsPerPublish = 1000,
            PublishingEnabled = true,
            Priority = 128
        };

        subscription.AddItem(new MonitoredItem(subscription.DefaultItem)
        {
            DisplayName = "Motor Run",
            StartNodeId = new NodeId(
                "|var|CODESYS Control.Application.GVL_IO.xMotorRun", (ushort)ns
            ),
            AttributeId = Attributes.Value,
            MonitoringMode = MonitoringMode.Reporting,
            SamplingInterval = 100,
            QueueSize = 1,
            DiscardOldest = true
        });

        subscription.ApplyChanges();
        
        subscription.FastDataChangeCallback = (_, notifications, _) =>
        {
            foreach (var item in notifications.MonitoredItems)
            {
                Console.WriteLine($"[{DateTime.Now}] {item.DisplayName} = {item.Value.Value}");
            }
        };

        _session.AddSubscription(subscription);
        subscription.Create();

        Console.WriteLine("Subscription created. Monitoring...");
        await Task.Delay(60000);

        subscription.Delete(true);
    }

    public async Task DisconnectAsync()
    {
        if (_session != null && _session.Connected)
        {
            _session.Close();
            _session.Dispose();
        }
    }
}
```

---

## Kütüphane Seçim Rehberi

```
                         Python        Node.js       .NET/C#
                         asyncua       node-opcua    OPC Foundation SDK
─────────────────────────────────────────────────────────────────────────
Lisans          │ MIT          │ MIT          │ MIT
Aktif Gelişim   │ ✓ Evet       │ ✓ Evet       │ ✓ Evet
API Kolaylığı   │ ✓✓ Kolay     │ ✓ Orta       │ ✗ Karmaşık
Async Desteği   │ ✓ Tam (async)│ ✓ Tam (async)│ ✓ Var
Güvenlik (TLS)  │ ✓ Var        │ ✓ Var        │ ✓ Tam
OPC Foundation  │ Hayır        │ Hayır        │ Evet (sertifika)
Performans      │ Orta         │ Yüksek       │ En Yüksek
Kullanım Alanı  │ Script, IoT  │ Web, Node-RED│ Enterprise, WinForms
─────────────────────────────────────────────────────────────────────────

asyncua seç:
  ✓ Python ekosistemi (pandas, numpy, scikit-learn entegrasyonu)
  ✓ Hızlı prototip, data analysis script
  ✓ Linux/Raspberry Pi, gömülü sistemler
  ✓ MQTT, InfluxDB gibi açık araçlarla entegrasyon

node-opcua seç:
  ✓ Web dashboard, Node-RED akışları
  ✓ JavaScript tabanlı full-stack uygulama
  ✓ Real-time web HMI (WebSocket entegrasyon)
  ✓ Microservice mimarisi

OPC Foundation .NET SDK seç:
  ✓ Enterprise .NET uygulaması
  ✓ OPC Foundation uyumluluk sertifikasyonu gerekiyor
  ✓ Windows Forms / WPF / ASP.NET HMI
  ✓ En yüksek performans ve özellik seti
```

## Sık Yapılan Hatalar

### Hata 1: Session'ı Kapatmadan Çıkmak

```python
# ❌ Yanlış
client = Client("opc.tcp://...")
await client.connect()
# ... program bitiyor, session kapatılmadı
# Sunucuda hayalet session kalıyor → MaxSessions dolabilir

# ✅ Doğru
async with Client("opc.tcp://...") as client:
    # ... otomatik disconnect
```

### Hata 2: Reconnect Mekanizması Olmadan Production

```python
# ❌ Yanlış — Bağlantı kopunca uygulama çöker
async with Client("opc.tcp://...") as client:
    while True:
        value = await node.read_value()

# ✅ Doğru — Retry mekanizması ile
import asyncio

async def robust_read():
    while True:
        try:
            async with Client("opc.tcp://192.168.1.100:4840") as client:
                print("Connected.")
                while True:
                    try:
                        value = await node.read_value()
                        # işle...
                        await asyncio.sleep(1)
                    except ConnectionError as e:
                        print(f"Read error: {e}")
                        break  # Dış döngü yeniden bağlanır
        except Exception as e:
            print(f"Connection failed: {e}. Retry in 5s...")
            await asyncio.sleep(5)
```

### Hata 3: Namespace Index Cache Etmemek

```python
# ❌ Yanlış — Her döngüde namespace sorgula (gereksiz overhead)
while True:
    ns = await client.get_namespace_index("http://...")  # Her döngü!
    node = client.get_node(f"ns={ns};s=...")
    value = await node.read_value()

# ✅ Doğru — Bir kez al, cache'le
ns = await client.get_namespace_index("http://...")
node = client.get_node(f"ns={ns};s=...")  # Node objesi de cache'le
while True:
    value = await node.read_value()
```

## Gerçek Proje Notları

**Not 1 — asyncua ile Production Dashboard**  
Python asyncua ile 200 MonitoredItem, 500ms publishing interval, InfluxDB yazma. Handler'da queue kullandık, ayrı asyncio task InfluxDB'ye yazıyor. CPU: %2. Veri kaybı: sıfır (queue doldu mesajı hiç görülmedi). 6 aydır kesintisiz çalışıyor.

**Not 2 — node-opcua ile Node-RED Entegrasyonu**  
node-red-contrib-opcua paketi node-opcua üzerine kurulu. Node-RED akışında OPC UA subscription → InfluxDB → Grafana dashboard 30 dakikada kuruldu. Klasik SCADA yerine açık araç ekosistemi, bakım maliyetini sıfıra indirdi.

**Not 3 — .NET SDK'nın Belgeleme Zorluğu**  
OPC Foundation .NET SDK, güçlü ama belgesi karmaşık. API'yi anlamak için Unified Automation örnek projeleri çok daha faydalı. Enterprise projesinde SDK kullanmak zorundaydık (müşteri OPC Foundation sertifikasyonu istiyordu) — API'yi sarmak için kendi abstraction katmanını yazdık.

**Not 4 — asyncio Event Loop'unun Sync Kodla Kilitlenmesi**  
asyncua ile yazılmış bir köprü, FastAPI içinde çalışırken zaman zaman tüm OPC UA bağlantılarını dondurdu. Sebep: bir geliştirici handler içinden senkron `requests.post()` çağırmıştı; bu, tek event loop'u bloklayıp tüm subscription'ları durdurdu. asyncua tek thread'li asyncio üzerinde çalışır — handler'da senkron blocking çağrı, *tüm* istemciyi durdurur. Çözüm: blocking I/O için `run_in_executor` veya tamamen async kütüphane. Ders: async kütüphanede "bir yeri bloklamak hepsini bloklamaktır".

**Not 5 — node-opcua Otomatik Reconnect ile Hayalet MonitoredItem'lar**  
node-opcua'nın otomatik reconnect'i bağlantı kopunca subscription'ları yeniden kurar; ama uygulama kodu da kendi reconnect mantığını ekleyince her kopmada MonitoredItem'lar iki kez oluşturuldu. Sunucu tarafında `MaxMonitoredItems` birkaç saat içinde doldu. Çözüm: SDK'nın yerleşik reconnect'ine güvenmek ve uygulama seviyesinde çift mantık koymamak. SDK reconnect davranışını anlamadan üstüne reconnect yazmak limit tüketir.

**Not 6 — .NET ReadValue Sync API'sinin Thread Havuzunu Tüketmesi**  
.NET SDK'da senkron `Session.ReadValue()` yüzlerce eş zamanlı çağrıda thread pool'u tüketti (her çağrı bir thread bloklar). ASP.NET servisi yanıt veremez hale geldi. Çözüm: async overload'lar (`ReadValueAsync` / `ReadAsync`) ve toplu Read kullanımı. Ders: yüksek eşzamanlılıkta sync OPC UA API'leri ölçeklenmez; async + batch zorunlu.

## Edge Case'ler ve Sistem Limitleri

İstemci tarafı sorunlarının çoğu protokol değil, *eşzamanlılık modeli* ve *reconnect/cleanup yaşam döngüsü* kaynaklıdır:

| Edge Case | Kütüphane | Belirti | Önlem |
|---|---|---|---|
| Handler'da blocking çağrı | asyncua (tek loop) | Tüm istemci donar | `run_in_executor` / queue |
| Sync API + yüksek eşzamanlılık | .NET SDK | Thread pool tükenir | Async overload + batch |
| Çift reconnect mantığı | node-opcua | Hayalet MonitoredItem | SDK reconnect'ine güven |
| Session kapatılmadan çıkış | Hepsi | Sunucuda hayalet session | Context manager / using |
| Namespace index her döngü sorgu | Hepsi | Gereksiz round-trip | Bir kez al, cache |
| Reconnect sonrası NodeId yeniden çözmeme | Hepsi | `BadNodeIdUnknown` | Reconnect'te tekrar resolve |
| Subscription republish atlama | Düşük seviye | Kopma sonrası boşluk | sequenceNumber takibi |
| SecureChannel timeout (idle) | Hepsi | Uzun idle'da kopma | Keepalive/periyodik read |
| python-opcua (eski) kullanımı | Python | Bakım yok, async yok | asyncua'ya geç |

Kritik sınır gerçekleri:
- **asyncua tek event loop'tur — bir blocking çağrı her şeyi durdurur.** Bu en sık görülen production hatasıdır; handler ve callback'ler asla senkron I/O yapmamalı.
- **Reconnect sonrası durum yeniden kurulmalı.** Çoğu SDK SecureChannel/Session'ı kurtarır ama uygulama, çözülmüş NodeId cache'ini ve subscription handle'larını doğrulamalı; kör reconnect `Bad` döngüsüne girebilir.
- **Cleanup yaşam döngüsünün parçasıdır.** Session ve subscription temizlenmezse sunucu kotaları (MaxSessions/MaxSubscriptions/MaxMonitoredItems) sessizce dolar; istemci hatası sunucuyu kilitler.

## Optimizasyon

İstemci optimizasyonu = round-trip minimizasyonu + doğru eşzamanlılık modeli. Öncelik:

1. **Toplu Read/Write kullan.** Tek `read_values([...])` / batch Read, 100 ayrı çağrının round-trip maliyetini 1'e indirir. En büyük tek kazanç.
2. **Polling yerine subscription.** İzleme her zaman subscription; istemci sürekli sormaz, sunucu değişimde iter. Read yalnızca anlık tek-okuma için.
3. **Namespace index ve Node nesnesini cache'le.** Her döngüde `get_namespace_index` / `get_node` çağırmak gereksiz overhead'tir; bir kez çöz, sakla.
4. **Handler'ı non-blocking yap (queue + worker).** Handler değeri queue'ya atıp döner; ağır iş (DB/InfluxDB/ağ) ayrı task/thread. Hem performans hem kararlılık.
5. **Async API + concurrency.** .NET'te async overload, Python/Node'da zaten async. Sync API yüksek eşzamanlılıkta thread tüketir.
6. **Tek kalıcı bağlantı.** Her işlem için connect/disconnect yapmak SecureChannel asimetrik kripto maliyetini tekrarlatır; tek kalıcı Session + reconnect mantığı.
7. **UA Binary (varsayılan) bırak.** İstemci tarafında JSON/XML kodlamaya zorlamak gereksiz boyut ve CPU yaratır; cihaz iletişiminde Binary kal.

## Derin Teknik Detay

**Neden async modelin OPC UA istemcileri için doğal eşleşme?** OPC UA istemci-sunucu iletişimi tek SecureChannel üzerinde RequestId ile çoğullanmış (multiplexed) istek-yanıtlardan oluşur; yanıtlar sırasız dönebilir. Bu, doğal olarak asenkron bir modeldir — istemci bir Read'i beklerken paralel bir Browse gönderebilir ve event loop yanıtları RequestId ile eşleştirir. Bu yüzden asyncua (Python asyncio) ve node-opcua (Node.js event loop) modeli protokole birebir oturur. Bedeli: tek event loop'u bloklamak (senkron I/O) tüm çoğullamayı durdurur (Not 4). .NET SDK senkron API de sunar ama altta yine async I/O vardır; senkron sarmalama her çağrıyı bir thread'e bağlayarak ölçeklenmeyi bozar (Not 6). Eşzamanlılık modeli kütüphane seçiminden daha kritiktir.

**Subscription republish: kayıpsız teslimin altyapısı.** Her bildirim bir `sequenceNumber` taşır. İstemci, aldığı son sequence'ı sunucuya bildirir (acknowledge); sunucu onaylanmamış bildirimleri retransmission queue'da tutar. Bağlantı kopup yeni SecureChannel ile aynı Session'a dönüldüğünde istemci, eksik sequence'ları `Republish` servisiyle yeniden ister. Bu, "geçici ağ kesintisinde veri kaybetme" garantisinin mekanizmasıdır ve düşük seviyeli SDK kullananların elle yönetmesi gerekir; yüksek seviyeli SDK'lar (asyncua, node-opcua) bunu otomatikleştirir. Kütüphane seçerken "republish'i kim yönetiyor?" kritik sorudur.

**Reconnect: SecureChannel/Session/Subscription katmanlarının ayrı kurtarılması.** Sağlam bir reconnect üç katmanı sırayla ele alır: (1) yeni SecureChannel aç (asimetrik handshake), (2) `ActivateSession` ile eski Session'a dön — başarılıysa subscription'lar yaşıyordur; (3) Session da öldüyse (SessionTimeout aşıldı) her şeyi sıfırdan kur ve NodeId cache'ini yeniden doğrula. İyi SDK'lar bu kademeyi otomatik dener; kötü uygulama doğrudan (3)'e atlayıp her kopmada yeni session+subscription üreterek sunucu kotalarını tüketir (Not 5). Reconnect'i "her şeyi sil-baştan kur" sanmak, OPC UA'nın katmanlı dayanıklılığını boşa harcar.

**Kütüphane seçiminin gerçek ekseni: ekosistem + eşzamanlılık + sertifikasyon.** asyncua Python veri/IoT ekosistemine (pandas, InfluxDB, ML) doğal bağlanır ve async'tir; node-opcua web/Node-RED ve WebSocket köprüleri için idealdir; OPC Foundation .NET SDK ise tek "OPC Foundation uyumluluk sertifikalı" seçenektir — müşteri sertifikasyon şartı koyuyorsa zorunludur, aksi halde karmaşıklığı çoğu projede gereksizdir. Performans farkları (Node/.NET daha yüksek throughput) çoğu endüstriyel yükte belirleyici değildir; belirleyici olan, çevreleyen ekosistem ve eşzamanlılık modelidir.

## İlgili Konular

```
knowledge/protocols/opc-ua/
├── 01_architecture.md           → Session, endpoint kavramları
├── 02_address_space.md          → NodeID ve namespace
├── 03_security.md               → Güvenli bağlantı kurma
├── 04_subscriptions.md          → Subscription parametreleri
└── 05_codesys_server_config.md  → Sunucu tarafı yapılandırma

Kütüphane kaynakları:
  asyncua      → https://github.com/FreeOpcUa/opcua-asyncio
  node-opcua   → https://node-opcua.github.io/
  OPC Fnd SDK  → https://github.com/OPCFoundation/UA-.NETStandard
  
Test araçları:
  UaExpert     → Manuel test ve NodeID keşfi
  Prosys OPC   → Gelişmiş test istemcisi
```
