using CommunityToolkit.Mvvm.ComponentModel;

namespace ConveyorHmi.ViewModels;

/// <summary>
/// Tek bir alarm kaydı (ISA-18.2 esinli).
/// Acknowledge != Resolved: koşul kapansa da onaylanmadıysa listede kalır.
/// </summary>
public partial class AlarmViewModel : ObservableObject
{
    public string Code { get; }
    public string Message { get; }
    public DateTime RaisedAt { get; }

    [ObservableProperty]
    private bool _active;

    [ObservableProperty]
    private bool _acknowledged;

    public AlarmViewModel(string code, string message, DateTime raisedAt)
    {
        Code = code;
        Message = message;
        RaisedAt = raisedAt;
    }

    public string TimeText => RaisedAt.ToString("HH:mm:ss");
    public string StatusText => Active ? "AKTİF" : "KAPANDI";
    public string AckText => Acknowledged ? "EVET" : "—";

    partial void OnActiveChanged(bool value)
    {
        OnPropertyChanged(nameof(StatusText));
    }

    partial void OnAcknowledgedChanged(bool value)
    {
        OnPropertyChanged(nameof(AckText));
    }
}
