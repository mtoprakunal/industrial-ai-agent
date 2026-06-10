using System.Collections.ObjectModel;
using System.Windows;
using System.Windows.Threading;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using ConveyorHmi.Services;

namespace ConveyorHmi.ViewModels;

/// <summary>
/// Ana görünüm modeli — OPC-UA servisini sürer, tag değişimlerini
/// WPF Dispatcher ile UI thread'ine taşır ve heartbeat watchdog yürütür.
///
/// OpcUaService.TagChanged event'i ThreadPool thread'inde gelir; bu yüzden
/// tüm property güncellemeleri Dispatcher.BeginInvoke ile sarmalanır
/// (knowledge/hmi/desktop/02_opcua_clients_dotnet.md Hata 2).
/// </summary>
public partial class MainViewModel : ObservableObject, IAsyncDisposable
{
    private readonly OpcUaService _service = new();
    private readonly Dispatcher _dispatcher = Application.Current.Dispatcher;
    private readonly DispatcherTimer _watchdogTimer;

    private uint _lastHeartbeat;
    private DateTime _lastHeartbeatUtc = DateTime.MinValue;

    public ObservableCollection<ZoneViewModel> Zones { get; } = new();
    public ObservableCollection<AlarmViewModel> Alarms { get; } = new();

    [ObservableProperty]
    private string _connectionState = "BAĞLI DEĞİL";

    [ObservableProperty]
    private bool _eStopActive;

    [ObservableProperty]
    private bool _runPermit;

    [ObservableProperty]
    private bool _anyAlarm;

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(ResetCommand))]
    private bool _commandsEnabled;

    public MainViewModel()
    {
        for (int z = 1; z <= HmiConfig.ZoneCount; z++)
            Zones.Add(new ZoneViewModel(z));

        _service.TagChanged += OnTagChanged;
        _service.ConnectionStateChanged += OnConnectionStateChanged;

        // Heartbeat watchdog — UI thread'inde, hafif kontrol.
        _watchdogTimer = new DispatcherTimer { Interval = TimeSpan.FromMilliseconds(500) };
        _watchdogTimer.Tick += (_, _) => CheckWatchdog();
        _watchdogTimer.Start();
    }

    // --- Komutlar ---

    [RelayCommand]
    private async Task ConnectAsync()
    {
        try
        {
            await _service.ConnectAsync();
        }
        catch (Exception ex)
        {
            ConnectionState = $"Hata: {ex.Message}";
        }
    }

    [RelayCommand]
    private async Task DisconnectAsync()
    {
        await _service.DisconnectAsync();
        CommandsEnabled = false;
    }

    [RelayCommand(CanExecute = nameof(CommandsEnabled))]
    private async Task ResetAsync()
    {
        try { await _service.WriteResetAsync(); }
        catch (Exception ex) { ConnectionState = $"Reset hatası: {ex.Message}"; }
    }

    /// <summary>Bölge oto-run komutu (View'dan zone no + değer ile çağrılır).</summary>
    public async Task SetAutoRunAsync(int zoneNo, bool value)
    {
        try { await _service.WriteAutoRunAsync(zoneNo, value); }
        catch (Exception ex) { ConnectionState = $"AutoRun hatası: {ex.Message}"; }
    }

    // --- OPC-UA event'leri (ThreadPool -> Dispatcher) ---

    private void OnConnectionStateChanged(string state)
    {
        _dispatcher.BeginInvoke(() =>
        {
            ConnectionState = state switch
            {
                "CONNECTED" => "BAĞLI",
                "RECONNECTING" => "YENİDEN BAĞLANIYOR",
                _ => "BAĞLI DEĞİL",
            };
            CommandsEnabled = state == "CONNECTED";
        });
    }

    private void OnTagChanged(string name, object? value)
    {
        _dispatcher.BeginInvoke(() => ApplyTag(name, value));
    }

    private void ApplyTag(string name, object? value)
    {
        switch (name)
        {
            case "aZoneState":
                foreach (var (v, i) in EnumerateArray(value))
                    if (i < Zones.Count)
                        Zones[i].State = HmiConfig.ZoneStateNames.GetValueOrDefault(
                            Convert.ToInt32(v), "?");
                break;
            case "aZoneSpeed":
                foreach (var (v, i) in EnumerateArray(value))
                    if (i < Zones.Count) Zones[i].Speed = Convert.ToDouble(v);
                break;
            case "aZoneAuto":
                foreach (var (v, i) in EnumerateArray(value))
                    if (i < Zones.Count) Zones[i].IsAuto = Convert.ToBoolean(v);
                break;
            case "xEStopActive":
                EStopActive = Convert.ToBoolean(value);
                UpdateAlarm("A001", "Acil Stop aktif", EStopActive);
                break;
            case "xRunPermit":
                RunPermit = Convert.ToBoolean(value);
                break;
            case "xZone2Itlk":
                UpdateAlarm("A060", "Bölge 2 interlock", Convert.ToBoolean(value));
                break;
            case "xAnyAlarm":
                AnyAlarm = Convert.ToBoolean(value);
                break;
            case "aZoneJam":
                UpdateZoneAlarms("JAM", "Sıkışma", value);
                break;
            case "aZoneSpdFlt":
                UpdateZoneAlarms("SPD", "Hız arızası", value);
                break;
            case "aZoneTacBrk":
                UpdateZoneAlarms("TAC", "Takometre kablo kopması", value);
                break;
            case "uHeartbeat":
                _lastHeartbeat = Convert.ToUInt32(value);
                _lastHeartbeatUtc = DateTime.UtcNow;
                break;
        }
    }

    // --- Alarm yönetimi ---

    private void UpdateZoneAlarms(string code, string text, object? arrayValue)
    {
        foreach (var (v, i) in EnumerateArray(arrayValue))
            UpdateAlarm($"{code}-Z{i + 1}", $"Bölge {i + 1} {text}", Convert.ToBoolean(v));
    }

    private void UpdateAlarm(string code, string message, bool active)
    {
        var existing = Alarms.FirstOrDefault(a => a.Code == code);
        if (active)
        {
            if (existing is null)
                Alarms.Add(new AlarmViewModel(code, message, DateTime.Now) { Active = true });
            else
                existing.Active = true;
        }
        else if (existing is not null)
        {
            existing.Active = false;
            if (existing.Acknowledged)
                Alarms.Remove(existing);
        }
    }

    [RelayCommand]
    private void AcknowledgeAll()
    {
        foreach (var alarm in Alarms.ToList())
        {
            alarm.Acknowledged = true;
            if (!alarm.Active) Alarms.Remove(alarm);
        }
    }

    // --- Watchdog ---

    private void CheckWatchdog()
    {
        if (!_service.IsConnected) return;
        var ageMs = (DateTime.UtcNow - _lastHeartbeatUtc).TotalMilliseconds;
        bool stale = _lastHeartbeatUtc == DateTime.MinValue || ageMs > HmiConfig.HeartbeatTimeoutMs;
        if (stale)
        {
            ConnectionState = "VERİ BAYAT";
            CommandsEnabled = false;
            foreach (var z in Zones) z.IsStale = true;
        }
        else
        {
            foreach (var z in Zones) z.IsStale = false;
        }
    }

    // --- Yardımcı ---

    private static IEnumerable<(object value, int index)> EnumerateArray(object? value)
    {
        if (value is null) yield break;
        // CODESYS ARRAY[1..3] OPC-UA'da Array (object[]) olarak gelir.
        if (value is System.Collections.IEnumerable en and not string)
        {
            int i = 0;
            foreach (var item in en)
                yield return (item, i++);
        }
        else
        {
            yield return (value, 0);
        }
    }

    public async ValueTask DisposeAsync()
    {
        _watchdogTimer.Stop();
        await _service.DisposeAsync();
    }
}
