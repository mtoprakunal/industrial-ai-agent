---
KONU        : Masaüstü HMI için OPC UA .NET/C# İstemcileri
KATEGORİ    : hmi
ALT_KATEGORI: desktop
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://github.com/OPCFoundation/UA-.NETStandard"
    başlık: "GitHub — OPCFoundation/UA-.NETStandard (Resmi OPC Foundation .NET Stack)"
    güvenilirlik: resmi
  - url: "https://www.nuget.org/packages/OPCFoundation.NetStandard.Opc.Ua/"
    başlık: "NuGet — OPCFoundation.NetStandard.Opc.Ua v1.5.378.145"
    güvenilirlik: resmi
  - url: "https://www.nuget.org/packages/OPCFoundation.NetStandard.Opc.Ua.Client"
    başlık: "NuGet — OPCFoundation.NetStandard.Opc.Ua.Client v1.5.378.145"
    güvenilirlik: resmi
  - url: "https://github.com/OPCFoundation/UA-.NETStandard/blob/master/Applications/ConsoleReferenceClient/UAClient.cs"
    başlık: "GitHub — ConsoleReferenceClient/UAClient.cs (Resmi referans implementasyon)"
    güvenilirlik: resmi
  - url: "https://github.com/OPCFoundation/UA-.NETStandard/blob/master/Applications/ConsoleReferenceClient/ClientSamples.cs"
    başlık: "GitHub — ConsoleReferenceClient/ClientSamples.cs (Browse/Read/Write/Subscribe örnekleri)"
    güvenilirlik: resmi
  - url: "https://github.com/OPCFoundation/UA-.NETStandard/blob/master/Docs/Certificates.md"
    başlık: "GitHub — Certificates.md (PKI yapısı ve sertifika yönetimi)"
    güvenilirlik: resmi
  - url: "https://github.com/OPCFoundation/UA-.NETStandard/releases"
    başlık: "GitHub — UA-.NETStandard Release Notes (1.5.378.x serisi)"
    güvenilirlik: resmi
  - url: "https://github.com/dathlin/OpcUaHelper"
    başlık: "GitHub — dathlin/OpcUaHelper (Topluluk wrapper kütüphanesi)"
    güvenilirlik: topluluk
  - url: "https://github.com/convertersystems/opc-ua-client"
    başlık: "GitHub — convertersystems/Workstation.UaClient (WPF MVVM kütüphanesi)"
    güvenilirlik: topluluk
  - url: "https://deepwiki.com/OPCFoundation/UA-.NETStandard/4.2-client-subscription-model"
    başlık: "DeepWiki — Client Subscription Model (Subscription/MonitoredItem detayları)"
    güvenilirlik: topluluk
  - url: "https://forge.codesys.com/forge/talk/Engineering/thread/e13e290e29/"
    başlık: "CODESYS Forge — C# OPC UA Client connecting to CODESYS server"
    güvenilirlik: topluluk
  - url: "https://docs.factoryio.com/tutorials/codesys/setting-up/codesys-opc-ua-sp18/"
    başlık: "FACTORY I/O — CODESYS OPC UA SP18 kurulum (port ve endpoint bilgileri)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "protocols/opc-ua/06_client_implementations"
    ilişki: detaylandırır
  - konu: "hmi/desktop/01_opcua_clients_python"
    ilişki: alternatif
  - konu: "protocols/opc-ua/03_security"
    ilişki: kullanır
  - konu: "protocols/opc-ua/04_subscriptions"
    ilişki: kullanır
  - konu: "protocols/opc-ua/02_address_space"
    ilişki: gerektirir
  - konu: "protocols/opc-ua/05_codesys_server_config"
    ilişki: tamamlar
ÖNKOŞUL     :
  - "OPC UA temel kavramları: Session, Subscription, MonitoredItem, NodeId, Namespace (01–04_*.md)"
  - "C# ve .NET 6/8/9 programlama bilgisi"
  - "NuGet paket yönetimi"
  - "CODESYS OPC UA Server yapılandırması (05_codesys_server_config.md)"
ÇELİŞKİLER :
  - kaynak: "OPC Foundation SDK vs OpcUaHelper vs Workstation.UaClient"
    konu: >
      Resmi OPC Foundation SDK tam özellikli fakat API'si karmaşık ve verbose.
      OpcUaHelper (dathlin) daha sade bir wrapper sunar; üretim projelerinde kullanılıyor.
      Workstation.UaClient WPF/MVVM için attribute-tabanlı subscription sunar.
    çözüm: >
      OPC Foundation SDK: Enterprise, OPC Foundation sertifikasyonu, tam kontrol gerektiğinde.
      OpcUaHelper: Sade API, küçük-orta ölçekli endüstriyel uygulamalar.
      Workstation.UaClient: WPF/MVVM uygulamaları için en hızlı entegrasyon.
      Bu belge resmi SDK üzerine yoğunlaşır; OpcUaHelper pattern'larını da gösterir.
  - kaynak: "Session.Create (eski API) vs DefaultSessionFactory.CreateAsync (yeni API)"
    konu: >
      SDK v1.5.374+ ile DefaultSessionFactory.CreateAsync kullanımı önerilir.
      Eski Session.Create hâlâ çalışır fakat bazı async senaryolarda sorun çıkarabilir.
    çözüm: >
      Yeni projeler için DefaultSessionFactory.CreateAsync veya UAClient wrapper pattern kullanılmalı.
      Eski projeler için Session.Create geçerli olmaya devam ediyor.
  - kaynak: "AutoAcceptUntrustedCertificates"
    konu: >
      AutoAcceptUntrustedCertificates=true geliştirme sürecini kolaylaştırır,
      fakat üretime taşınan kodda güvenlik açığı oluşturur.
    çözüm: >
      Geliştirmede true, üretimde false kullanılmalı. Üretimde sunucu sertifikası
      pki/trusted/certs/ klasörüne elle eklenmeli veya CertificateValidationEvent ile
      yönetilmeli.
---

## Özün Ne

OPC UA .NET/C# istemcisi, masaüstü HMI uygulamalarının (WPF, WinForms) endüstriyel PLC sunucularına — özellikle CODESYS tabanlı kontrolörlere — bağlanmasını sağlayan temel teknolojidir. OPC Foundation'ın açık kaynak resmi kütüphanesi **OPCFoundation.NetStandard.Opc.Ua** (GitHub: OPCFoundation/UA-.NETStandard), MIT lisansı ile dağıtılır ve .NET 4.8, .NET 6/8/9, .NET Standard 2.1'i destekler. En güncel sürüm v1.5.378.145'tir (Mayıs 2026). Kütüphane; Session kurma, Browse/Read/Write, Subscription+MonitoredItem ve X.509 tabanlı güvenlik için eksiksiz bir API sunar. WPF entegrasyonu için resmi SDK doğrudan kullanılabileceği gibi, community kütüphaneleri (OpcUaHelper, Workstation.UaClient) geliştirme sürecini büyük ölçüde hızlandırır.

## Nasıl Çalışır

### Mimari Katmanlar

```
WPF / WinForms Uygulaması
        │
        ▼
  OPC UA İstemci Katmanı (Session, Subscription)
        │  Opc.Ua.Client.dll
        ▼
  OPC UA Stack (Opc.Ua.Core.dll)
        │  UA Binary / HTTPS transport
        ▼
  TCP (opc.tcp://host:4840)
        │
        ▼
  CODESYS Runtime / PLC OPC UA Server
```

### Temel Kavramlar

**ApplicationConfiguration** — İstemci uygulamasını tanımlayan merkezi yapılandırma nesnesi. ApplicationUri, sertifika store yolları, transport quota'ları ve güvenlik politikasını içerir. XML dosyasından veya programatik olarak oluşturulabilir.

**Session** — Sunucuyla kurulan logical bağlantı. Tek TCP bağlantısı üzerinden çalışır. Kimlik doğrulama (anonymous, username/password, X.509), namespace tablosu ve oturum zaman aşımını yönetir. v1.5.374+ API'de `ISession` arayüzü kullanılır.

**Subscription** — Sunucunun istemciye periyodik bildirim göndermesini sağlar. `PublishingInterval` (ms) ile bildirim sıklığı ayarlanır. Tek session üzerinde birden fazla Subscription olabilir.

**MonitoredItem** — Subscription'a eklenen izleme birimi. Her MonitoredItem belirli bir NodeId'yi, `SamplingInterval` ile örnekleme hızını ve `QueueSize` ile tampon kapasitesini tanımlar.

**SessionReconnectHandler** — Bağlantı koptuğunda otomatik yeniden bağlantıyı yönetir. `TransferSubscriptionsOnReconnect = true` ile abonelikler aktarılır, veri kaybı minimuma iner.

### CODESYS OPC UA NodeId Formatı

CODESYS OPC UA Server, değişkenleri belirli bir yol formatında yayınlar:

```
Namespace URI : uygulamaya ve platforma göre değişir (UaExpert ile keşfedilmeli)
NodeId string : ns=<index>;s=|var|<RuntimeAdı>.Application.<GVLAdı>.<DeğişkenAdı>
```

Örnek:
```
ns=4;s=|var|CODESYS Control Win V3.Application.GVL_IO.rTemperature
ns=4;s=|var|CODESYS Control Win V3.Application.PLC_PRG.xMotorRun
```

> **Önemli:** Namespace index (`ns=4`) doğrudan kodda sabit yazılmamalıdır. Namespace URI her sunucuda farklı index alabilir. Namespace URI, session bağlandıktan sonra `session.NamespaceUris.GetIndex(uri)` ile sorgulanmalıdır. CODESYS namespace URI'si UaExpert veya benzer araçlarla keşfedilmelidir; tipik değerler `"urn:<device-name>:CODESYS3-2"` veya `"http://www.3s-software.com/schemas/Codesys-V3"` şeklinde görülmüştür (Kaynak: CODESYS Forge topluluk tartışmaları), fakat değerlerin controller modeline göre değiştiği bilinmektedir.

## Pratikte Nasıl Kullanılır

### 1. NuGet Paket Kurulumu

```bash
# Tek paket — tüm bağımlılıkları (Core, Client, Configuration, Security.Certificates...) içerir
dotnet add package OPCFoundation.NetStandard.Opc.Ua

# Veya sadece istemci için (daha hafif)
dotnet add package OPCFoundation.NetStandard.Opc.Ua.Core
dotnet add package OPCFoundation.NetStandard.Opc.Ua.Client

# Package Manager Console (Visual Studio)
NuGet\Install-Package OPCFoundation.NetStandard.Opc.Ua -Version 1.5.378.145
```

**Mevcut paketler (v1.5.378.145, Mayıs 2026):**
- `OPCFoundation.NetStandard.Opc.Ua` — meta-paket (tüm bileşenler)
- `OPCFoundation.NetStandard.Opc.Ua.Core` — temel tipler ve stack
- `OPCFoundation.NetStandard.Opc.Ua.Client` — Session, Subscription, MonitoredItem
- `OPCFoundation.NetStandard.Opc.Ua.Configuration` — ApplicationInstance, sertifika yönetimi
- `OPCFoundation.NetStandard.Opc.Ua.Security.Certificates` — X.509 yardımcıları
- `OPCFoundation.NetStandard.Opc.Ua.Bindings.Https` — HTTPS transport (isteğe bağlı)

Kaynak: [NuGet Gallery — OPCFoundation.NetStandard.Opc.Ua](https://www.nuget.org/packages/OPCFoundation.NetStandard.Opc.Ua/)

### 2. ApplicationConfiguration — Programatik Kurulum

```csharp
using Opc.Ua;
using Opc.Ua.Client;
using Opc.Ua.Configuration;

/// <summary>
/// ApplicationConfiguration'ı programatik olarak oluşturur.
/// XML dosyasına gerek yok.
/// Kaynak: github.com/OPCFoundation/UA-.NETStandard — UAClient.cs pattern
/// </summary>
public static async Task<ApplicationConfiguration> BuildConfigurationAsync(
    string appName = "DesktopHmiClient",
    string pkiRootPath = "./pki")
{
    var config = new ApplicationConfiguration
    {
        ApplicationName = appName,
        ApplicationUri  = Utils.Format(
            "urn:{0}:{1}", System.Net.Dns.GetHostName(), appName),
        ApplicationType = ApplicationType.Client,

        SecurityConfiguration = new SecurityConfiguration
        {
            // İstemcinin kendi sertifikası (otomatik oluşturulur)
            ApplicationCertificate = new CertificateIdentifier
            {
                StoreType   = CertificateStoreType.Directory,
                StorePath   = $"{pkiRootPath}/own",
                SubjectName = $"CN={appName}, O=Industrial HMI"
            },
            // Güvenilen CA sertifikaları
            TrustedIssuerCertificates = new CertificateTrustList
            {
                StoreType = CertificateStoreType.Directory,
                StorePath = $"{pkiRootPath}/issuers"
            },
            // Güvenilen peer sertifikaları (sunucu sertifikaları buraya eklenir)
            TrustedPeerCertificates = new CertificateTrustList
            {
                StoreType = CertificateStoreType.Directory,
                StorePath = $"{pkiRootPath}/trusted"
            },
            // Reddedilen sertifikalar (yönetici incelemesi için)
            RejectedCertificateStore = new CertificateTrustList
            {
                StoreType = CertificateStoreType.Directory,
                StorePath = $"{pkiRootPath}/rejected"
            },
            AutoAcceptUntrustedCertificates = false, // Üretimde false!
            RejectSHA1SignedCertificates     = true,
            MinimumCertificateKeySize        = 2048
        },

        TransportQuotas = new TransportQuotas
        {
            OperationTimeout   = 15_000,  // 15 saniye
            MaxStringLength    = 1_048_576,
            MaxByteStringLength = 4_194_304,
            MaxArrayLength     = 65_535,
            MaxMessageSize     = 4_194_304
        },

        ClientConfiguration = new ClientConfiguration
        {
            DefaultSessionTimeout = 60_000  // 60 saniye
        }
    };

    // Konfigürasyonu doğrula (eksik alan varsa exception fırlatır)
    await config.Validate(ApplicationType.Client);

    // Sertifika yoksa otomatik oluştur
    var appCert = config.SecurityConfiguration.ApplicationCertificate;
    if (!appCert.Certificate?.HasPrivateKey ?? true)
    {
        var certResult = await CertificateFactory.CreateCertificate(
            appCert.StoreType,
            appCert.StorePath,
            null,
            config.ApplicationUri,
            config.ApplicationName,
            appCert.SubjectName,
            null,
            CertificateFactory.DefaultKeySize,
            DateTime.UtcNow - TimeSpan.FromDays(1),
            CertificateFactory.DefaultLifeTime,
            CertificateFactory.DefaultHashSize,
            isCA: false);

        appCert.Certificate = certResult;
        Console.WriteLine($"Sertifika oluşturuldu: {appCert.StorePath}");
        Console.WriteLine("CODESYS sunucusunun trusted/certs/ klasörüne bu sertifikayı ekle!");
    }

    return config;
}
```

Kaynak: [UA-.NETStandard Certificates.md](https://github.com/OPCFoundation/UA-.NETStandard/blob/master/Docs/Certificates.md), [ConsoleReferenceClient Program.cs](https://github.com/OPCFoundation/UA-.NETStandard/blob/master/Applications/ConsoleReferenceClient/Program.cs)

### 3. Session Oluşturma ve Bağlanma

```csharp
using Opc.Ua;
using Opc.Ua.Client;

public class OpcUaHmiClient : IDisposable
{
    private ISession?             _session;
    private SessionReconnectHandler? _reconnectHandler;
    private readonly ApplicationConfiguration _config;

    // Yeniden bağlantı periyodu (ms)
    public int ReconnectPeriodMs { get; set; } = 5_000;
    public int ReconnectBackoffMs { get; set; } = 30_000;

    public OpcUaHmiClient(ApplicationConfiguration config)
    {
        _config = config;
    }

    /// <summary>
    /// CODESYS OPC UA sunucusuna bağlan.
    /// Endpoint güvenlik politikasını otomatik seçer.
    /// Kaynak: github.com/OPCFoundation/UA-.NETStandard — UAClient.cs
    /// </summary>
    public async Task ConnectAsync(
        string endpointUrl,
        bool   useSecurity  = true,
        string? userName    = null,
        string? password    = null,
        CancellationToken ct = default)
    {
        // Sertifika doğrulama olayına bağlan
        _config.CertificateValidator.CertificateValidation +=
            OnCertificateValidation;

        // Endpoint keşfi ve seçimi
        var endpointDescription = await CoreClientUtils.SelectEndpointAsync(
            _config,
            endpointUrl,
            useSecurity,
            cancellationToken: ct);

        var configuredEndpoint = new ConfiguredEndpoint(
            null,
            endpointDescription,
            EndpointConfiguration.Create(_config));

        // Kullanıcı kimliği
        IUserIdentity identity = (userName != null)
            ? new UserNameIdentityToken { UserName = userName,
                                          DecryptedPassword = password ?? "" }
            : new AnonymousIdentityToken();

        // Session oluştur (modern API: DefaultSessionFactory)
        var factory = new DefaultSessionFactory();
        _session = await factory.CreateAsync(
            _config,
            configuredEndpoint,
            updateBeforeConnect: false,
            checkDomain: false,
            sessionName: $"HMI-{System.Net.Dns.GetHostName()}",
            sessionTimeout: (uint)_config.ClientConfiguration.DefaultSessionTimeout,
            identity: identity,
            preferredLocales: null,
            ct: ct);

        // KeepAlive: bağlantı koptuğunda yeniden bağlan
        _session.KeepAlive += OnSessionKeepAlive;

        // Abonelikler yeniden bağlanmada aktarılsın
        _session.DeleteSubscriptionsOnClose    = false;
        _session.TransferSubscriptionsOnReconnect = true;

        Console.WriteLine($"Bağlandı: {endpointUrl}");
        Console.WriteLine($"Session ID: {_session.SessionId}");
    }

    private void OnSessionKeepAlive(ISession session, KeepAliveEventArgs e)
    {
        if (!ReferenceEquals(session, _session)) return;

        if (ServiceResult.IsBad(e.Status))
        {
            Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] KeepAlive hatası: {e.Status}. Yeniden bağlanıyor...");

            if (_reconnectHandler == null)
            {
                _reconnectHandler = new SessionReconnectHandler(
                    reconnectAbort: false);
                _reconnectHandler.BeginReconnect(
                    _session,
                    ReconnectPeriodMs,
                    OnReconnectComplete);
            }
        }
    }

    private void OnReconnectComplete(object? sender, EventArgs e)
    {
        if (!ReferenceEquals(sender, _reconnectHandler)) return;

        if (_reconnectHandler?.Session != null)
        {
            if (!ReferenceEquals(_session, _reconnectHandler.Session))
            {
                _session?.Dispose();
                _session = _reconnectHandler.Session;
                _session.KeepAlive += OnSessionKeepAlive;
            }
        }

        _reconnectHandler?.Dispose();
        _reconnectHandler = null;
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Yeniden bağlandı.");
    }

    private void OnCertificateValidation(
        CertificateValidator sender,
        CertificateValidationEventArgs e)
    {
        // Üretimde: sadece bilinen hataları geç, diğerlerini reddet
        if (e.Error.StatusCode == StatusCodes.BadCertificateUntrusted)
        {
            // GELİŞTİRME İÇİN — üretimde sertifikayı pki/trusted/ klasörüne ekle
            Console.WriteLine($"Uyarı: Güvenilmeyen sertifika kabul edildi: {e.Certificate.Subject}");
            e.Accept = true;
        }
    }

    public async Task DisconnectAsync()
    {
        _reconnectHandler?.Dispose();
        _reconnectHandler = null;

        if (_session != null)
        {
            _session.KeepAlive -= OnSessionKeepAlive;
            await _session.CloseAsync();
            _session.Dispose();
            _session = null;
        }
    }

    public void Dispose() => DisconnectAsync().GetAwaiter().GetResult();
}
```

Kaynak: [UAClient.cs — OPCFoundation/UA-.NETStandard](https://github.com/OPCFoundation/UA-.NETStandard/blob/master/Applications/ConsoleReferenceClient/UAClient.cs)

### 4. Address Space Browse (Adres Alanı Keşfi)

```csharp
/// <summary>
/// CODESYS sunucusundaki değişkenleri keşfetmek için Browse kullan.
/// NodeId'leri öğrenmeden önce UaExpert ile manuel keşif daha pratiktir.
/// Kaynak: github.com/OPCFoundation/UA-.NETStandard — ClientSamples.cs
/// </summary>
public async Task<List<ReferenceDescription>> BrowseNodeAsync(
    NodeId startNodeId,
    CancellationToken ct = default)
{
    var browser = new Browser(_session)
    {
        BrowseDirection = BrowseDirection.Forward,
        NodeClassMask   = (int)(NodeClass.Object | NodeClass.Variable),
        ReferenceTypeId = ReferenceTypeIds.HierarchicalReferences,
        IncludeSubtypes = true
    };

    ReferenceDescriptionCollection refs = await browser.BrowseAsync(startNodeId, ct);

    foreach (var r in refs)
    {
        Console.WriteLine($"  [{r.NodeClass}] {r.BrowseName} — {r.NodeId}");
    }

    return refs.ToList();
}

// Kullanım: Objects klasöründen başla
// await client.BrowseNodeAsync(ObjectIds.ObjectsFolder);
```

### 5. Read — Değer Okuma

```csharp
using Opc.Ua;
using Opc.Ua.Client;

/// <summary>
/// CODESYS değişkeni okuma.
/// Namespace index'i namespace URI'den dinamik olarak al.
/// Kaynak: github.com/OPCFoundation/UA-.NETStandard — ClientSamples.cs
/// </summary>

// Namespace index'i session bağlandıktan sonra al (bir kez yap, cache'le)
// NOT: CODESYS namespace URI'si platforma göre değişir — UaExpert ile kontrol et
private ushort GetNamespaceIndex(string namespaceUri)
{
    int idx = _session!.NamespaceUris.GetIndex(namespaceUri);
    if (idx < 0)
        throw new InvalidOperationException(
            $"Namespace bulunamadı: {namespaceUri}. " +
            "UaExpert ile sunucunun namespace tablosunu kontrol edin.");
    return (ushort)idx;
}

// --- Tekil değer okuma ---
public DataValue ReadValue(string nodeIdString)
{
    var nodeId = NodeId.Parse(nodeIdString);

    // Senkron API
    DataValue dv = _session!.ReadValue(nodeId);
    Console.WriteLine($"Değer   : {dv.Value}");
    Console.WriteLine($"Status  : {dv.StatusCode}");
    Console.WriteLine($"Zaman   : {dv.SourceTimestamp:HH:mm:ss.fff}");
    return dv;
}

// --- Toplu değer okuma (verimli — tek servis çağrısı) ---
public async Task<DataValueCollection> ReadMultipleAsync(
    string[] nodeIdStrings,
    CancellationToken ct = default)
{
    var nodesToRead = new ReadValueIdCollection(
        nodeIdStrings.Select(s => new ReadValueId
        {
            NodeId      = NodeId.Parse(s),
            AttributeId = Attributes.Value
        })
    );

    ReadResponse response = await _session!.ReadAsync(
        requestHeader:    null,
        maxAge:           0,
        timestampsToReturn: TimestampsToReturn.Source,
        nodesToRead:      nodesToRead,
        ct:               ct);

    ClientBase.ValidateResponse(response.Results, nodesToRead);

    for (int i = 0; i < response.Results.Count; i++)
    {
        Console.WriteLine($"{nodeIdStrings[i].Split('.').Last()} = " +
                          $"{response.Results[i].Value} " +
                          $"[{response.Results[i].StatusCode}]");
    }

    return response.Results;
}

// --- CODESYS'e özgü kullanım örneği ---
/*
    ushort ns = GetNamespaceIndex("urn:MyController:CODESYS3-2");

    // Tek okuma
    DataValue tempValue = ReadValue($"ns={ns};s=|var|CODESYS Control Win V3.Application.GVL_IO.rTemperature");

    // Toplu okuma
    string[] tags = {
        $"ns={ns};s=|var|CODESYS Control Win V3.Application.GVL_IO.rTemperature",
        $"ns={ns};s=|var|CODESYS Control Win V3.Application.GVL_IO.rPressure",
        $"ns={ns};s=|var|CODESYS Control Win V3.Application.GVL_IO.xMotorRun",
        $"ns={ns};s=|var|CODESYS Control Win V3.Application.GVL_IO.nConveyorSpeed"
    };
    var values = await ReadMultipleAsync(tags);
*/
```

Kaynak: [ClientSamples.cs — OPCFoundation/UA-.NETStandard](https://github.com/OPCFoundation/UA-.NETStandard/blob/master/Applications/ConsoleReferenceClient/ClientSamples.cs)

### 6. Write — Değer Yazma

```csharp
/// <summary>
/// Tek değer yazma.
/// Kaynak: github.com/OPCFoundation/UA-.NETStandard — ClientSamples.cs (WriteAsync pattern)
/// </summary>
public async Task<bool> WriteValueAsync<T>(
    string nodeIdString,
    T      value,
    CancellationToken ct = default)
{
    var nodeToWrite = new WriteValue
    {
        NodeId      = NodeId.Parse(nodeIdString),
        AttributeId = Attributes.Value,
        Value       = new DataValue(new Variant(value))
        {
            StatusCode      = StatusCodes.Good,
            ServerTimestamp = DateTime.MinValue,
            SourceTimestamp = DateTime.MinValue
        }
    };

    WriteResponse response = await _session!.WriteAsync(
        requestHeader: null,
        nodesToWrite:  new WriteValueCollection { nodeToWrite },
        ct:            ct);

    ClientBase.ValidateResponse(response.Results, new WriteValueCollection { nodeToWrite });

    bool success = StatusCode.IsGood(response.Results[0]);
    if (!success)
        Console.WriteLine($"Yazma hatası: {response.Results[0]}");

    return success;
}

// --- Toplu yazma ---
public async Task WriteBatchAsync(
    Dictionary<string, object> tagValues,
    CancellationToken ct = default)
{
    var nodesToWrite = new WriteValueCollection(
        tagValues.Select(kv => new WriteValue
        {
            NodeId      = NodeId.Parse(kv.Key),
            AttributeId = Attributes.Value,
            Value       = new DataValue(new Variant(kv.Value))
        })
    );

    WriteResponse response = await _session!.WriteAsync(
        null, nodesToWrite, ct);

    for (int i = 0; i < response.Results.Count; i++)
    {
        string tag = tagValues.Keys.ElementAt(i);
        Console.WriteLine($"{tag.Split('.').Last()}: " +
                          $"{(StatusCode.IsGood(response.Results[i]) ? "OK" : response.Results[i].ToString())}");
    }
}

/*  Kullanım:
    ushort ns = GetNamespaceIndex("urn:MyController:CODESYS3-2");

    // Bool yaz (motor start komutu)
    await WriteValueAsync($"ns={ns};s=|var|...Application.GVL_HMI.xStartCmd", true);

    // Float yaz (setpoint)
    await WriteValueAsync($"ns={ns};s=|var|...Application.GVL_Params.rSpeedSetpoint", 75.5f);

    // Int yaz (reçete no)
    await WriteValueAsync($"ns={ns};s=|var|...Application.GVL_Params.nRecipeID", (short)3);
*/
```

Kaynak: [ClientSamples.cs — OPCFoundation/UA-.NETStandard](https://github.com/OPCFoundation/UA-.NETStandard/blob/master/Applications/ConsoleReferenceClient/ClientSamples.cs)

### 7. Subscription ve MonitoredItem

```csharp
/// <summary>
/// OPC UA Subscription oluştur ve değişkenleri izle.
/// Bildirimler arka plan thread'inde gelir — WPF Dispatcher gerekir.
/// Kaynak: github.com/OPCFoundation/UA-.NETStandard — ClientSamples.cs + DeepWiki subscription model
/// </summary>
public async Task<Subscription> CreateSubscriptionAsync(
    string[] nodeIdStrings,
    int publishingIntervalMs = 500,
    int samplingIntervalMs   = 100,
    CancellationToken ct     = default)
{
    var subscription = new Subscription(_session!.DefaultSubscription)
    {
        DisplayName                 = "HMI-Subscription",
        PublishingEnabled           = true,
        PublishingInterval          = publishingIntervalMs,
        LifetimeCount               = 100,
        MaxNotificationsPerPublish  = 1_000,
        KeepAliveCount              = 10,
        Priority                    = 100,
        // Sıralı işleme garantisi (yüksek frekanslı veri için önemli)
        SequentialPublishing        = true
    };

    foreach (string nodeIdStr in nodeIdStrings)
    {
        var item = new MonitoredItem(subscription.DefaultItem)
        {
            StartNodeId     = NodeId.Parse(nodeIdStr),
            AttributeId     = Attributes.Value,
            DisplayName     = nodeIdStr.Split('.').Last(),
            SamplingInterval = samplingIntervalMs,
            QueueSize        = 10,
            DiscardOldest    = true,
            MonitoringMode   = MonitoringMode.Reporting
        };

        // Per-item bildirim olayı
        item.Notification += OnMonitoredItemNotification;
        subscription.AddItem(item);
    }

    _session!.AddSubscription(subscription);
    await subscription.CreateAsync(ct);

    Console.WriteLine($"Subscription oluşturuldu. " +
                      $"PublishingInterval: {subscription.CurrentPublishingInterval}ms, " +
                      $"ID: {subscription.Id}");

    return subscription;
}

private void OnMonitoredItemNotification(
    MonitoredItem item,
    MonitoredItemNotificationEventArgs e)
{
    // Bu metot arka plan (OPC UA client publish) thread'inde çalışır!
    // WPF UI güncellemesi için Dispatcher gerekir — aşağıdaki WPF bölümüne bakın.

    foreach (var value in item.DequeueValues())
    {
        if (StatusCode.IsGood(value.StatusCode))
        {
            Console.WriteLine($"[{value.SourceTimestamp:HH:mm:ss.fff}] " +
                              $"{item.DisplayName} = {value.Value}");
        }
        else
        {
            Console.WriteLine($"[{item.DisplayName}] Hatalı değer: {value.StatusCode}");
        }
    }
}
```

Kaynak: [DeepWiki — Client Subscription Model](https://deepwiki.com/OPCFoundation/UA-.NETStandard/4.2-client-subscription-model), [ClientSamples.cs](https://github.com/OPCFoundation/UA-.NETStandard/blob/master/Applications/ConsoleReferenceClient/ClientSamples.cs)

## Örnekler

### Örnek 1 — Tam WPF MVVM Entegrasyonu

```csharp
// ViewModel — INotifyPropertyChanged ile OPC UA subscription
// Bildirimler arka plan thread'inden WPF Dispatcher aracılığıyla UI thread'ine aktarılır

using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows;
using Opc.Ua;
using Opc.Ua.Client;

public class MachineStatusViewModel : INotifyPropertyChanged, IDisposable
{
    public event PropertyChangedEventHandler? PropertyChanged;

    private double  _temperature;
    private double  _pressure;
    private bool    _motorRunning;
    private int     _alarmCount;
    private string  _connectionStatus = "Bağlı Değil";

    public double Temperature
    {
        get => _temperature;
        set { _temperature = value; OnPropertyChanged(); }
    }

    public double Pressure
    {
        get => _pressure;
        set { _pressure = value; OnPropertyChanged(); }
    }

    public bool MotorRunning
    {
        get => _motorRunning;
        set { _motorRunning = value; OnPropertyChanged(); }
    }

    public int AlarmCount
    {
        get => _alarmCount;
        set { _alarmCount = value; OnPropertyChanged(); }
    }

    public string ConnectionStatus
    {
        get => _connectionStatus;
        set { _connectionStatus = value; OnPropertyChanged(); }
    }

    private OpcUaHmiClient?  _client;
    private Subscription?    _subscription;
    private readonly Dictionary<string, Action<object?>> _tagMap;
    private ushort _ns;

    public MachineStatusViewModel()
    {
        // NodeId son parçası → property mapping
        _tagMap = new Dictionary<string, Action<object?>>
        {
            ["rTemperature"] = v => Temperature  = Convert.ToDouble(v),
            ["rPressure"]    = v => Pressure     = Convert.ToDouble(v),
            ["xMotorRun"]    = v => MotorRunning = Convert.ToBoolean(v),
            ["nAlarmCount"]  = v => AlarmCount   = Convert.ToInt32(v)
        };
    }

    public async Task InitializeAsync(string serverUrl = "opc.tcp://192.168.1.100:4840")
    {
        try
        {
            var config = await OpcUaHmiClient.BuildConfigurationAsync("WpfHmiClient");
            _client = new OpcUaHmiClient(config);

            // Geliştirme: anonymous; üretim: username/password veya X.509
            await _client.ConnectAsync(serverUrl, useSecurity: false);

            ConnectionStatus = "Bağlandı";

            // Namespace index — UaExpert ile URI'yi öğren, burada kullan
            // Örnek URI (platforma göre değişir, sabit kullanma!):
            // _ns = _client.GetNamespaceIndex("urn:CODESYS-Device:CODESYS3-2");
            // Bu örnekte ns=4 varsayımıyla devam ediyoruz (gerçekte dinamik al):
            _ns = 4; // GERÇEK PROJEDE: session.NamespaceUris.GetIndex(uri)

            string[] tags = {
                $"ns={_ns};s=|var|CODESYS Control Win V3.Application.GVL_IO.rTemperature",
                $"ns={_ns};s=|var|CODESYS Control Win V3.Application.GVL_IO.rPressure",
                $"ns={_ns};s=|var|CODESYS Control Win V3.Application.GVL_IO.xMotorRun",
                $"ns={_ns};s=|var|CODESYS Control Win V3.Application.GVL_Alarms.nAlarmCount"
            };

            _subscription = await _client.CreateSubscriptionAsync(
                tags, publishingIntervalMs: 500, samplingIntervalMs: 100);

            // Bildirim callback'ini özelleştir
            foreach (var item in _subscription.MonitoredItems)
            {
                item.Notification += OnTagNotification;
            }
        }
        catch (Exception ex)
        {
            ConnectionStatus = $"Hata: {ex.Message}";
        }
    }

    private void OnTagNotification(MonitoredItem item, MonitoredItemNotificationEventArgs e)
    {
        foreach (var value in item.DequeueValues())
        {
            if (!StatusCode.IsGood(value.StatusCode)) continue;

            // WPF UI thread'ine geçiş — zorunlu!
            Application.Current.Dispatcher.BeginInvoke(() =>
            {
                string tagName = item.DisplayName; // rTemperature, xMotorRun vb.
                if (_tagMap.TryGetValue(tagName, out var setter))
                    setter(value.Value);
            });
        }
    }

    public async Task SendStartCommandAsync()
    {
        if (_client == null || _ns == 0) return;
        await _client.WriteValueAsync(
            $"ns={_ns};s=|var|CODESYS Control Win V3.Application.GVL_HMI.xStartCmd",
            true);
    }

    public async Task SetSpeedSetpointAsync(double rpm)
    {
        if (_client == null || _ns == 0) return;
        await _client.WriteValueAsync(
            $"ns={_ns};s=|var|CODESYS Control Win V3.Application.GVL_Params.rSpeedSetpoint",
            (float)rpm);
    }

    protected void OnPropertyChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));

    public void Dispose()
    {
        _subscription?.Delete(true);
        _client?.Dispose();
    }
}
```

```xml
<!-- MainWindow.xaml — WPF DataBinding -->
<Window x:Class="DesktopHmi.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Grid>
        <StackPanel Margin="20">
            <TextBlock Text="{Binding ConnectionStatus}"
                       FontWeight="Bold" Margin="0,0,0,10"/>

            <TextBlock Text="{Binding Temperature, StringFormat='Sıcaklık: {0:F1} °C'}"/>
            <TextBlock Text="{Binding Pressure,    StringFormat='Basınç: {0:F2} bar'}"/>
            <TextBlock Text="{Binding AlarmCount,  StringFormat='Alarm: {0}'}"/>

            <!-- Motor durumu — renk binding -->
            <Ellipse Width="20" Height="20" Margin="0,5">
                <Ellipse.Fill>
                    <Binding Path="MotorRunning">
                        <Binding.Converter>
                            <!-- BoolToColorConverter: true=Yeşil, false=Kırmızı -->
                            <local:BoolToColorConverter/>
                        </Binding.Converter>
                    </Binding>
                </Ellipse.Fill>
            </Ellipse>

            <Button Content="Motor Başlat"
                    Command="{Binding StartCommand}"/>
            <Slider Minimum="0" Maximum="3000"
                    Value="{Binding SpeedSetpoint, Mode=TwoWay}"/>
        </StackPanel>
    </Grid>
</Window>
```

### Örnek 2 — OpcUaHelper ile Daha Sade API (Topluluk Kütüphanesi)

```bash
dotnet add package OpcUaHelper
```

```csharp
// OpcUaHelper — dathlin/OpcUaHelper wrapper kütüphanesi
// Daha az kod, karmaşık güvenlik senaryoları için yetersiz
// Kaynak: github.com/dathlin/OpcUaHelper — OpcUaClient.cs

using OpcUaHelper;

var client = new OpcUaClient();

// Bağlan (güvenlik sertifikası otomatik: CurrentUser\My store kullanır)
await client.ConnectServer("opc.tcp://192.168.1.100:4840");
Console.WriteLine($"Bağlandı: {client.Connected}");

// KeepAlive ve reconnect event'leri
client.KeepAliveComplete += (s, e) => Console.WriteLine("KeepAlive OK");
client.ReconnectComplete += (s, e) => Console.WriteLine("Yeniden bağlandı");

// Değer oku (generic, type-safe)
// NOT: NodeId string'i doğrudan ns=X;s=... formatında ver
float temp = client.ReadNode<float>("ns=4;s=|var|CODESYS Control Win V3.Application.GVL_IO.rTemperature");
bool  motorRun = client.ReadNode<bool>("ns=4;s=|var|CODESYS Control Win V3.Application.GVL_IO.xMotorRun");
Console.WriteLine($"Sıcaklık: {temp}, Motor: {motorRun}");

// Toplu okuma
string[] tags = {
    "ns=4;s=|var|CODESYS Control Win V3.Application.GVL_IO.rTemperature",
    "ns=4;s=|var|CODESYS Control Win V3.Application.GVL_IO.rPressure"
};
List<float> vals = client.ReadNodes<float>(tags);

// Değer yaz
client.WriteNode("ns=4;s=|var|CODESYS Control Win V3.Application.GVL_Params.rSpeedSetpoint", 75.0f);
client.WriteNode("ns=4;s=|var|CODESYS Control Win V3.Application.GVL_HMI.xStartCmd", true);

// Subscription
client.AddSubscription(
    "motor_group",
    new[] {
        "ns=4;s=|var|CODESYS Control Win V3.Application.GVL_IO.xMotorRun",
        "ns=4;s=|var|CODESYS Control Win V3.Application.GVL_IO.rTemperature"
    },
    (key, monItem, args) =>
    {
        // WPF'de Dispatcher.BeginInvoke ile sarmalayın!
        var notification = args.NotificationValue as MonitoredItemNotification;
        Console.WriteLine($"[{key}] {monItem.DisplayName} = {notification?.Value.Value}");
    },
    sub => { sub.PublishingInterval = 500; }  // Ek subscription ayarları
);

// Bağlantıyı kes
client.Disconnect();
```

Kaynak: [github.com/dathlin/OpcUaHelper](https://github.com/dathlin/OpcUaHelper)

### Örnek 3 — Workstation.UaClient ile WPF Attribute-Tabanlı Subscription

```bash
dotnet add package Workstation.UaClient
```

```csharp
// Workstation.UaClient — convertersystems/opc-ua-client
// WPF için en hızlı entegrasyon: attribute-tabanlı subscription
// Kaynak: github.com/convertersystems/opc-ua-client

using Workstation.ServiceModel.Ua;
using Workstation.ServiceModel.Ua.Channels;

// App.xaml.cs / startup'ta UaApplication başlat
var ua = new UaApplicationBuilder()
    .SetApplicationUri("urn:MyDesktopHmi")
    .SetDirectoryStore("./pki")
    .SetIdentityProvider(new AnonymousIdentityProvider())
    .AddMappedEndpoint("codesys-plc", "opc.tcp://192.168.1.100:4840")
    .Build();

await ua.StartAsync();

// ViewModel — SubscriptionBase miras alır
[Subscription(endpointName: "codesys-plc", publishingInterval: 500)]
public class PlcViewModel : SubscriptionBase
{
    // Attribute ile NodeId binding — subscription otomatik oluşur
    [MonitoredItem(nodeId: "ns=4;s=|var|CODESYS Control Win V3.Application.GVL_IO.rTemperature")]
    public float Temperature
    {
        get => _temperature;
        set => SetProperty(ref _temperature, value);
    }
    private float _temperature;

    [MonitoredItem(nodeId: "ns=4;s=|var|CODESYS Control Win V3.Application.GVL_IO.xMotorRun")]
    public bool MotorRunning
    {
        get => _motorRunning;
        set => SetProperty(ref _motorRunning, value);
    }
    private bool _motorRunning;
}
// XAML'da doğrudan {Binding Temperature} çalışır — Dispatcher yok, minimal kod
```

Kaynak: [github.com/convertersystems/opc-ua-client](https://github.com/convertersystems/opc-ua-client)

### Örnek 4 — Güvenli Bağlantı (SignAndEncrypt, X.509 Sertifika)

```csharp
// Güvenli bağlantı — CODESYS OPC UA Server güvenlik modunu destekliyorsa
// Kaynak: github.com/OPCFoundation/UA-.NETStandard — Certificates.md + UAClient.cs

// 1. Adım: config'te AutoAcceptUntrustedCertificates = false
// 2. Adım: İstemci sertifikasını oluştur (ilk çalıştırmada otomatik)
// 3. Adım: İstemci sertifikasını sunucunun pki/trusted/certs/ klasörüne kopyala
//           CODESYS IDE > Device > Security > Trusted Clients
// 4. Adım: Sunucu sertifikasını istemcinin pki/trusted/ klasörüne kopyala

// ApplicationConfiguration içinde (BuildConfigurationAsync'te):
config.SecurityConfiguration.AutoAcceptUntrustedCertificates = false;

// Bağlanırken useSecurity = true:
await _client.ConnectAsync(
    "opc.tcp://192.168.1.100:4840",
    useSecurity: true,  // Basic256Sha256 otomatik seçilir
    userName: "opc_operator",
    password: "G$tr0ng!Pass");

// CertificateValidationEvent — üretimde elle onay
void OnCertificateValidation(CertificateValidator v, CertificateValidationEventArgs e)
{
    // Sadece belirli sunucu sertifikasını kabul et (parmak izi ile)
    const string allowedThumbprint = "AA:BB:CC:DD:..."; // sunucu sertifikası parmak izi
    if (e.Certificate.Thumbprint == allowedThumbprint)
        e.Accept = true;
    else
        throw new Exception($"Bilinmeyen sunucu sertifikası: {e.Certificate.Thumbprint}");
}
```

### Örnek 5 — PKI Klasör Yapısı

```
./pki/
├── own/
│   ├── certs/           ← İstemci sertifikası (.der)
│   └── private/         ← İstemci özel anahtarı
├── trusted/
│   ├── certs/           ← Güvenilen sunucu sertifikaları (.der)
│   └── crl/             ← Sertifika iptal listeleri
├── issuers/
│   ├── certs/           ← CA sertifikaları
│   └── crl/
└── rejected/
    └── certs/           ← Reddedilen sertifikalar (inceleme için)
```

CODESYS sunucu sertifikasını almak için:
1. `pki/rejected/certs/` klasörüne atılan sertifikayı kopyala
2. `pki/trusted/certs/` klasörüne yapıştır
3. Uygulamayı yeniden başlat

Kaynak: [UA-.NETStandard Certificates.md](https://github.com/OPCFoundation/UA-.NETStandard/blob/master/Docs/Certificates.md)

## Sık Yapılan Hatalar

### Hata 1 — Namespace Index'i Sabit Yazmak

```csharp
// ❌ Yanlış — ns=4 her controller'da geçerli değil
var nodeId = new NodeId("|var|...Application.GVL_IO.rTemperature", 4);

// ✅ Doğru — Namespace URI'den dinamik al
int idx = _session.NamespaceUris.GetIndex("urn:MyController:CODESYS3-2");
if (idx < 0) throw new Exception("Namespace bulunamadı!");
var nodeId = new NodeId("|var|...Application.GVL_IO.rTemperature", (ushort)idx);
```

### Hata 2 — WPF'de UI Thread İhlali

```csharp
// ❌ Yanlış — OPC UA callback arka plan thread'inde çalışır
item.Notification += (item, e) =>
{
    TemperatureLabel.Content = item.DequeueValues().First().Value; // InvalidOperationException!
};

// ✅ Doğru — Dispatcher ile UI thread'ine geç
item.Notification += (item, e) =>
{
    var value = item.DequeueValues().FirstOrDefault();
    if (value == null) return;

    Application.Current.Dispatcher.BeginInvoke(() =>
    {
        TemperatureLabel.Content = value.Value;
    });
    // Veya: Dispatcher.InvokeAsync (async versiyon)
};
```

### Hata 3 — Session Kapatmadan Çıkmak

```csharp
// ❌ Yanlış — Session açık kalır, sunucuda MaxSessions dolabilir
var session = await factory.CreateAsync(...);
// ... uygulama kapanıyor, session.Close() çağrılmadı

// ✅ Doğru — using pattern ile otomatik kapat
// ISession IDisposable değil; manuel kapat:
try
{
    // ... işlemler
}
finally
{
    if (session.Connected)
        await session.CloseAsync();
    session.Dispose();
}
```

### Hata 4 — Session Sağlığını Kontrol Etmeden Okuma

```csharp
// ❌ Yanlış
DataValue val = _session.ReadValue(nodeId); // session null veya bağlı değil!

// ✅ Doğru
if (_session == null || !_session.Connected)
{
    Console.WriteLine("Session bağlı değil.");
    return;
}
DataValue val = _session.ReadValue(nodeId);
```

### Hata 5 — Reconnect Sırasında Subscription'ı Silip Yeniden Oluşturmak

```csharp
// ❌ Yanlış — Veri kaybı + gereksiz overhead
_session.KeepAlive += (s, e) =>
{
    if (ServiceResult.IsBad(e.Status))
    {
        _subscription.Delete(true); // Kötü!
        // yeniden bağlan → yeni subscription oluştur
    }
};

// ✅ Doğru — TransferSubscriptionsOnReconnect=true ile otomatik aktarım
_session.DeleteSubscriptionsOnClose    = false;
_session.TransferSubscriptionsOnReconnect = true;
// SessionReconnectHandler otomatik halleder
```

Kaynak: [UAClient.cs reconnect pattern](https://github.com/OPCFoundation/UA-.NETStandard/blob/master/Applications/ConsoleReferenceClient/UAClient.cs)

### Hata 6 — AutoAcceptUntrustedCertificates=true Üretimde Bırakmak

```csharp
// ❌ Üretim güvenlik açığı
SecurityConfiguration = new SecurityConfiguration
{
    AutoAcceptUntrustedCertificates = true  // Ortadaki adam saldırısına açık!
}

// ✅ Üretim için
AutoAcceptUntrustedCertificates = false;
// Sunucu sertifikasını pki/trusted/certs/ klasörüne elle ekle
// veya CertificateValidationEvent'te parmak izi kontrolü yap
```

## Ne Zaman Tercih Edilmeli / Edilmemeli

### OPC Foundation .NET SDK Tercih Et

- Enterprise .NET masaüstü uygulaması (WPF, WinForms, .NET MAUI)
- OPC Foundation uyumluluk sertifikasyonu gerektiğinde
- Tam güvenlik kontrolü (X.509, SignAndEncrypt, kullanıcı yönetimi)
- ECC güvenlik profilleri veya PubSub gerektiğinde (.NET 9/10 ile)
- Yüksek performans, çok sayıda MonitoredItem (1000+)
- CODESYS, Siemens S7, Beckhoff TwinCAT gibi çoklu PLC markalarına bağlanma

### OPCFoundation SDK Yerine Düşün

- **Sadece basit okuma/yazma + Python ekibi varsa:** asyncua daha kolay ve hızlı
- **Web HMI veya Node-RED:** node-opcua uygun
- **Çok küçük proje, sertifika yönetimi istemiyorsan:** OpcUaHelper veya Workstation.UaClient
- **Protype/demo:** OpcUaHelper sade API sağlar, daha az kod gerektirir

### Kütüphane Seçim Tablosu

```
                     OPC Foundation SDK    OpcUaHelper    Workstation.UaClient
──────────────────────────────────────────────────────────────────────────────
Lisans              │ MIT                │ MIT            │ MIT
Aktif Gelişim       │ ✓ Evet (v1.5.378+) │ ✓ Orta         │ ✓ Var
API Kolaylığı       │ ✗ Verbose          │ ✓ Kolay        │ ✓✓ Attribute-tabanlı
WPF MVVM Desteği    │ Manuel Dispatcher  │ Manuel         │ ✓ Yerleşik
Güvenlik (TLS/X509) │ ✓ Tam              │ Sınırlı        │ Sınırlı
OPC Foundation Srt. │ ✓ Evet             │ Hayır          │ Hayır
.NET 8/9 Desteği    │ ✓ Evet             │ Evet           │ Kontrol et
Reconnect Handler   │ ✓ SessionReconnect │ ✓ Var          │ Otomatik
Performans          │ En Yüksek          │ Yüksek         │ Yüksek
──────────────────────────────────────────────────────────────────────────────
```

## Gerçek Proje Notları

**Not 1 — CODESYS Namespace URI Keşfi Zorunlu**
CODESYS OPC UA namespace URI'si her controller markasında ve yazılım sürümünde farklıdır. `"urn:CODESYS-PC:CODESYS3-2"`, `"http://www.3s-software.com/schemas/Codesys-V3"`, `"urn:BrickPi3:CODESYS3-2"` gibi formatlar görülmüştür (CODESYS Forge topluluk tartışmaları). Kod içine URI'yi sabit yazmak yerine, uygulama başlangıcında sunucuya bağlanıp `session.NamespaceUris` listesini loglayın ve doğru URI'yi yapılandırma dosyasından (appsettings.json) okuyun. Bu sayede aynı uygulama farklı controller modellerinde çalışabilir.

**Not 2 — SessionReconnectHandler Üretim Gerekliliği**
24/7 çalışan HMI uygulamalarında ağ kesintisi kaçınılmazdır. `SessionReconnectHandler` ile `TransferSubscriptionsOnReconnect = true` kombinasyonu, yeniden bağlanmada subscription'ları aktarır — veri kaybı sıfıra yaklaşır. `DeleteSubscriptionsOnClose = false` unutulursa subscription aktarımı başarısız olur. Reconnect period exponential backoff ile ayarlanmalıdır (1s → 10s → 30s).

**Not 3 — WPF Dispatcher Her Callback'te Gerekli**
OPC UA publish thread'i WPF UI thread'inden farklıdır. `MonitoredItem.Notification` event handler içinde her UI güncellemesi `Application.Current.Dispatcher.BeginInvoke()` veya `InvokeAsync()` ile sarmalanmalıdır; aksi halde `InvalidOperationException` fırlatılır. Workstation.UaClient bu sorunu otomatik çözer.

**Not 4 — PublishingInterval vs SamplingInterval Farkı**
`SamplingInterval`: Sunucunun değeri kontrol etme sıklığı (ör. 100ms). `PublishingInterval`: Sunucunun istemciye bildirim gönderme sıklığı (ör. 500ms). 500ms publishing + 100ms sampling: değer 100ms'de bir örneklenir, 500ms'de bir istemciye gönderilir. HMI için 250-1000ms publishing genellikle yeterlidir. CODESYS 10ms'nin altında sampling desteklemeyebilir — sunucu revise eder.

**Not 5 — OPC Foundation SDK v1.5.378+ Kırıcı Değişiklikler**
v1.5.374 ile `ISession` arayüzü eklendi, `DefaultSessionFactory.CreateAsync` önerildi. Eski `Session.Create()` (senkron) hâlâ çalışır fakat bazı async reconnect senaryolarında sorun çıkarabilir. v1.5.378.145 (Mayıs 2026): Task.Delay sonsuz döngü hatası düzeltildi, aşırı task spawn sorunu giderildi — üretim kritik güncelleme. Kaynak: [GitHub Releases](https://github.com/OPCFoundation/UA-.NETStandard/releases).

**Not 6 — CODESYS Güvenlik Modları**
CODESYS OPC UA Server varsayılan olarak anonim erişime izin verir; ancak güvenlik politikası "None" olarak ayarlanmışsa TLS şifrelemesi yapılamaz. Üretimde en az "SignAndEncrypt + Basic256Sha256" kullanın. CODESYS IDE'de: `Device > Runtime Security` → `Allow anonymous login` checkbox'ı kaldırın. Ayrıca `CODESYS OPC UA Server SL` lisansı gerekebilir. Kaynak: CODESYS Forge topluluk deneyimleri.

## İlgili Konular

```
knowledge/protocols/opc-ua/
├── 01_architecture.md           → Session, endpoint, transport kavramları
├── 02_address_space.md          → NodeId, namespace, address space yapısı
├── 03_security.md               → X.509 sertifika, PKI, güvenlik politikaları
├── 04_subscriptions.md          → Subscription ve MonitoredItem parametreleri
├── 05_codesys_server_config.md  → CODESYS OPC UA Server kurulumu ve yapılandırması
└── 06_client_implementations.md → Python, Node.js ve .NET kütüphane karşılaştırması

knowledge/hmi/desktop/
├── 01_opcua_clients_python.md   → Python asyncua ile alternatif yaklaşım
└── 03_pyqt_patterns.md          → PyQt ile masaüstü HMI pattern'ları

Resmi kaynaklar:
  OPC Foundation SDK    → https://github.com/OPCFoundation/UA-.NETStandard
  NuGet paketi          → https://www.nuget.org/packages/OPCFoundation.NetStandard.Opc.Ua
  Referans istemci      → UA-.NETStandard/Applications/ConsoleReferenceClient/
  OpcUaHelper wrapper   → https://github.com/dathlin/OpcUaHelper
  Workstation.UaClient  → https://github.com/convertersystems/opc-ua-client

Test araçları:
  UaExpert (Unified Automation) → NodeId ve namespace keşfi için zorunlu
  CODESYS IDE symbol browser   → CODESYS değişken yollarını doğrulamak için
```
