namespace ConveyorHmi;

/// <summary>
/// OPC-UA bağlantı ve NodeId konfigürasyonu.
/// EXAMPLE_conveyor CODESYS PLC'sine doğrudan (gateway yok) bağlanır.
///
/// ÖNEMLI: Namespace index (ns=) sabit yazılmaz; bağlantı sonrası
/// session.NamespaceUris.GetIndex(URI) ile alınır (bkz. OpcUaService).
/// Buradaki tanımlar ns'siz NodeId "identifier" (string) kısımlarıdır.
/// </summary>
public static class HmiConfig
{
    // --- Sunucu / endpoint ---
    public const string EndpointUrl = "opc.tcp://192.168.1.100:4840";

    // CODESYS namespace URI — UaExpert ile NamespaceArray'den doğrulayın.
    public const string CodesysNamespaceUri = "http://www.3s-software.com/schemas/Codesys-V3";

    // NodeId yolundaki Runtime + Application + GVL adı.
    public const string RuntimeName = "CODESYS Control Win V3";
    public const string ApplicationName = "Application";
    public const string GvlHmi = "GVL_HMI";

    // --- Güvenlik ---
    // Geliştirme: false (anonymous, güvenliksiz kanal). Üretim: true + sertifika.
    public const bool UseSecurity = false;
    public const string? UserName = null;   // örn. "opc_operator"
    public const string? Password = null;

    // --- Subscription / watchdog ---
    public const int PublishingIntervalMs = 500;
    public const int SamplingIntervalMs = 200;
    public const int HeartbeatTimeoutMs = 3000;

    public const int ZoneCount = 3;

    /// <summary>GVL_HMI değişkeni için ns'siz NodeId identifier üretir.</summary>
    public static string Node(string varName) =>
        $"|var|{RuntimeName}.{ApplicationName}.{GvlHmi}.{varName}";

    // E_ZoneState enum eşlemesi (PLC enum sırasına göre doğrulayın).
    public static readonly Dictionary<int, string> ZoneStateNames = new()
    {
        [0] = "IDLE",
        [1] = "STARTING",
        [2] = "RUNNING",
        [3] = "STOPPING",
        [4] = "JAM",
        [5] = "FAULT",
    };
}
