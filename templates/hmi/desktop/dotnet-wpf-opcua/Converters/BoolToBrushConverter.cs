using System.Globalization;
using System.Windows.Data;
using System.Windows.Media;

namespace ConveyorHmi.Converters;

/// <summary>
/// Boolean -> Brush dönüştürücü. ConverterParameter "true|false" renklerini
/// "TrueHex;FalseHex" formatında alır (örn. "#388E3C;#B71C1C").
/// ISA-101 renk kuralları için XAML'da kullanılır.
/// </summary>
public sealed class BoolToBrushConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object? parameter, CultureInfo culture)
    {
        bool b = value is true;
        var (onColor, offColor) = ParseParameter(parameter as string);
        return new SolidColorBrush(b ? onColor : offColor);
    }

    public object ConvertBack(object value, Type targetType, object? parameter, CultureInfo culture)
        => throw new NotSupportedException();

    private static (Color on, Color off) ParseParameter(string? param)
    {
        // Varsayılan: yeşil / kırmızı
        if (string.IsNullOrWhiteSpace(param))
            return ((Color)ColorConverter.ConvertFromString("#388E3C"),
                    (Color)ColorConverter.ConvertFromString("#B71C1C"));

        var parts = param.Split(';');
        var on = (Color)ColorConverter.ConvertFromString(parts[0]);
        var off = (Color)ColorConverter.ConvertFromString(parts.Length > 1 ? parts[1] : "#9E9E9E");
        return (on, off);
    }
}
