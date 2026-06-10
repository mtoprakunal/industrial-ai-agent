using CommunityToolkit.Mvvm.ComponentModel;

namespace ConveyorHmi.ViewModels;

/// <summary>Tek konveyör bölgesinin görünüm modeli (durum, hız, mod).</summary>
public partial class ZoneViewModel : ObservableObject
{
    public int ZoneNo { get; }

    [ObservableProperty]
    private string _state = "—";

    [ObservableProperty]
    private double _speed;

    [ObservableProperty]
    private bool _isAuto;

    [ObservableProperty]
    private bool _isStale;

    public ZoneViewModel(int zoneNo) => ZoneNo = zoneNo;

    public string Header => $"Bölge {ZoneNo}";
}
