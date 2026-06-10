using System.Windows;
using System.Windows.Controls;
using ConveyorHmi.ViewModels;

namespace ConveyorHmi;

/// <summary>
/// MainWindow code-behind — MVVM'de minimum tutulur.
/// Yalnızca bölge CheckBox'ının (Tag=ZoneNo) komutunu ViewModel'e iletir
/// ve pencere kapanışında OPC-UA session'ını temiz kapatır.
/// </summary>
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        Closed += OnClosed;
    }

    private async void OnAutoRunChanged(object sender, RoutedEventArgs e)
    {
        if (sender is CheckBox { Tag: int zoneNo } cb &&
            DataContext is MainViewModel vm)
        {
            await vm.SetAutoRunAsync(zoneNo, cb.IsChecked == true);
        }
    }

    private async void OnClosed(object? sender, EventArgs e)
    {
        if (DataContext is MainViewModel vm)
            await vm.DisposeAsync();
    }
}
