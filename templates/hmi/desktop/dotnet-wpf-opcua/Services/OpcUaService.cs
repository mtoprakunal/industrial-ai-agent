using Opc.Ua;
using Opc.Ua.Client;
using Opc.Ua.Configuration;

namespace ConveyorHmi.Services;

/// <summary>
/// OPC-UA istemci servisi — OPC Foundation .NET SDK üzerine.
///
/// Mimari (knowledge/hmi/desktop/02_opcua_clients_dotnet.md):
/// - DefaultSessionFactory.CreateAsync ile Session (modern API, v1.5.374+).
/// - SessionReconnectHandler + TransferSubscriptionsOnReconnect=true ile
///   bağlantı kopunca abonelik aktarılır (veri kaybı minimum).
/// - Subscription + MonitoredItem ile real-time bildirim. Notification
///   callback'i ThreadPool thread'inde gelir; UI güncellemesi için
///   ViewModel WPF Dispatcher kullanır (bu servis ham değeri event ile yayar).
/// - Namespace index sabit yazılmaz; session.NamespaceUris.GetIndex ile alınır.
/// </summary>
public sealed class OpcUaService : IAsyncDisposable
{
    private ApplicationConfiguration? _config;
    private ISession? _session;
    private SessionReconnectHandler? _reconnectHandler;
    private Subscription? _subscription;
    private ushort _ns;

    // MonitoredItem.DisplayName -> mantıksal isim (örn. "aZoneSpeed").
    private readonly Dictionary<string, string> _itemNames = new();

    /// <summary>Bir tag değeri değiştiğinde (isim, değer). ThreadPool thread'inde tetiklenir.</summary>
    public event Action<string, object?>? TagChanged;

    /// <summary>Bağlantı durumu değişiminde: "CONNECTED" | "RECONNECTING" | "DISCONNECTED".</summary>
    public event Action<string>? ConnectionStateChanged;

    public bool IsConnected => _session is { Connected: true };

    // --- Konfigürasyon ---

    private static async Task<ApplicationConfiguration> BuildConfigurationAsync()
    {
        var config = new ApplicationConfiguration
        {
            ApplicationName = "ConveyorHmi",
            ApplicationUri = Utils.Format("urn:{0}:ConveyorHmi", System.Net.Dns.GetHostName()),
            ApplicationType = ApplicationType.Client,
            SecurityConfiguration = new SecurityConfiguration
            {
                ApplicationCertificate = new CertificateIdentifier
                {
                    StoreType = CertificateStoreType.Directory,
                    StorePath = "./pki/own",
                    SubjectName = "CN=ConveyorHmi, O=Industrial HMI",
                },
                TrustedIssuerCertificates = new CertificateTrustList
                {
                    StoreType = CertificateStoreType.Directory, StorePath = "./pki/issuers",
                },
                TrustedPeerCertificates = new CertificateTrustList
                {
                    StoreType = CertificateStoreType.Directory, StorePath = "./pki/trusted",
                },
                RejectedCertificateStore = new CertificateTrustList
                {
                    StoreType = CertificateStoreType.Directory, StorePath = "./pki/rejected",
                },
                // Geliştirme kolaylığı; ÜRETIMDE false yapın (bkz. README güvenlik notu).
                AutoAcceptUntrustedCertificates = !HmiConfig.UseSecurity,
                RejectSHA1SignedCertificates = true,
                MinimumCertificateKeySize = 2048,
            },
            TransportQuotas = new TransportQuotas { OperationTimeout = 15_000 },
            ClientConfiguration = new ClientConfiguration { DefaultSessionTimeout = 60_000 },
        };

        await config.Validate(ApplicationType.Client);

        // İstemci sertifikası yoksa otomatik üret.
        var appInstance = new ApplicationInstance(config);
        await appInstance.CheckApplicationInstanceCertificates(silent: true);

        return config;
    }

    // --- Bağlanma ---

    public async Task ConnectAsync(CancellationToken ct = default)
    {
        _config ??= await BuildConfigurationAsync();

        _config.CertificateValidator.CertificateValidation += OnCertificateValidation;

        var endpoint = await CoreClientUtils.SelectEndpointAsync(
            _config, HmiConfig.EndpointUrl, HmiConfig.UseSecurity, ct);

        var configuredEndpoint = new ConfiguredEndpoint(
            null, endpoint, EndpointConfiguration.Create(_config));

        IUserIdentity identity = HmiConfig.UserName is { } user
            ? new UserIdentity(user, HmiConfig.Password ?? "")
            : new UserIdentity();   // Anonymous

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

        _session.KeepAlive += OnKeepAlive;
        _session.DeleteSubscriptionsOnClose = false;
        _session.TransferSubscriptionsOnReconnect = true;

        // Namespace index — URI'den dinamik al, ASLA sabit yazma.
        int idx = _session.NamespaceUris.GetIndex(HmiConfig.CodesysNamespaceUri);
        if (idx < 0)
            throw new InvalidOperationException(
                $"Namespace bulunamadı: {HmiConfig.CodesysNamespaceUri}. " +
                "UaExpert ile NamespaceArray'i kontrol edin.");
        _ns = (ushort)idx;

        CreateSubscription();
        ConnectionStateChanged?.Invoke("CONNECTED");
    }

    private NodeId FullNodeId(string identifier) => new(identifier, _ns);

    // --- Subscription ---

    private void CreateSubscription()
    {
        _subscription = new Subscription(_session!.DefaultSubscription)
        {
            DisplayName = "ConveyorHmi-Subscription",
            PublishingEnabled = true,
            PublishingInterval = HmiConfig.PublishingIntervalMs,
            KeepAliveCount = 10,
            LifetimeCount = 100,               // KeepAliveCount'un >= 3 katı
            MaxNotificationsPerPublish = 1000,
            Priority = 100,
            SequentialPublishing = true,
        };

        // İzlenecek değişkenler (PLC -> HMI).
        string[] vars =
        {
            "aZoneState", "aZoneSpeed", "aZoneRunning", "aZoneJam",
            "aZoneSpdFlt", "aZoneTacBrk", "aZoneAuto",
            "xEStopActive", "xRunPermit", "xZone2Itlk", "xAnyAlarm", "uHeartbeat",
        };

        foreach (var v in vars)
        {
            var item = new MonitoredItem(_subscription.DefaultItem)
            {
                StartNodeId = FullNodeId(HmiConfig.Node(v)),
                AttributeId = Attributes.Value,
                DisplayName = v,
                SamplingInterval = HmiConfig.SamplingIntervalMs,
                QueueSize = 10,
                DiscardOldest = true,
                MonitoringMode = MonitoringMode.Reporting,
            };
            _itemNames[v] = v;
            item.Notification += OnItemNotification;
            _subscription.AddItem(item);
        }

        _session.AddSubscription(_subscription);
        _subscription.Create();
    }

    private void OnItemNotification(MonitoredItem item, MonitoredItemNotificationEventArgs e)
    {
        // ThreadPool thread'inde çalışır — UI'ye DOKUNMAZ; ham değeri yayar.
        foreach (var value in item.DequeueValues())
        {
            if (!StatusCode.IsGood(value.StatusCode))
                continue;
            TagChanged?.Invoke(item.DisplayName, value.Value);
        }
    }

    // --- Yazma (komut) ---

    public async Task WriteAutoRunAsync(int zoneNo, bool value, CancellationToken ct = default)
    {
        if (_session is not { Connected: true }) return;
        // CODESYS array elemanı: ...axCmdAutoRun[1]
        var nodeId = FullNodeId($"{HmiConfig.Node("axCmdAutoRun")}[{zoneNo}]");
        await WriteValueAsync(nodeId, value, ct);
    }

    public async Task WriteResetAsync(CancellationToken ct = default)
    {
        if (_session is not { Connected: true }) return;
        await WriteValueAsync(FullNodeId(HmiConfig.Node("xCmdReset")), true, ct);
    }

    private async Task WriteValueAsync(NodeId nodeId, object value, CancellationToken ct)
    {
        var nodeToWrite = new WriteValue
        {
            NodeId = nodeId,
            AttributeId = Attributes.Value,
            Value = new DataValue(new Variant(value))
            {
                ServerTimestamp = DateTime.MinValue,
                SourceTimestamp = DateTime.MinValue,
            },
        };
        var nodes = new WriteValueCollection { nodeToWrite };
        var response = await _session!.WriteAsync(null, nodes, ct);
        ClientBase.ValidateResponse(response.Results, nodes);
        if (!StatusCode.IsGood(response.Results[0]))
            throw new ServiceResultException(response.Results[0].Code);
    }

    // --- Reconnect ---

    private void OnKeepAlive(ISession session, KeepAliveEventArgs e)
    {
        if (!ReferenceEquals(session, _session)) return;
        if (!ServiceResult.IsBad(e.Status)) return;

        ConnectionStateChanged?.Invoke("RECONNECTING");
        if (_reconnectHandler is null)
        {
            _reconnectHandler = new SessionReconnectHandler(reconnectAbort: false);
            _reconnectHandler.BeginReconnect(_session, 5_000, OnReconnectComplete);
        }
    }

    private void OnReconnectComplete(object? sender, EventArgs e)
    {
        if (!ReferenceEquals(sender, _reconnectHandler)) return;

        if (_reconnectHandler?.Session is { } newSession &&
            !ReferenceEquals(_session, newSession))
        {
            _session!.KeepAlive -= OnKeepAlive;
            _session.Dispose();
            _session = newSession;
            _session.KeepAlive += OnKeepAlive;
        }

        _reconnectHandler?.Dispose();
        _reconnectHandler = null;
        ConnectionStateChanged?.Invoke("CONNECTED");
    }

    private static void OnCertificateValidation(
        CertificateValidator sender, CertificateValidationEventArgs e)
    {
        // GELİŞTİRME: güvenilmeyen sunucu sertifikasını kabul et.
        // ÜRETIM: sertifikayı pki/trusted/certs/ klasörüne ekleyin ve burada
        //         yalnızca parmak izi eşleşmesini kabul edin.
        if (!HmiConfig.UseSecurity &&
            e.Error.StatusCode == StatusCodes.BadCertificateUntrusted)
        {
            e.Accept = true;
        }
    }

    public async Task DisconnectAsync()
    {
        _reconnectHandler?.Dispose();
        _reconnectHandler = null;

        if (_subscription is not null)
        {
            try { _subscription.Delete(true); } catch { /* yok say */ }
            _subscription = null;
        }

        if (_session is not null)
        {
            _session.KeepAlive -= OnKeepAlive;
            if (_session.Connected)
                await _session.CloseAsync();
            _session.Dispose();
            _session = null;
        }
        ConnectionStateChanged?.Invoke("DISCONNECTED");
    }

    public async ValueTask DisposeAsync() => await DisconnectAsync();
}
