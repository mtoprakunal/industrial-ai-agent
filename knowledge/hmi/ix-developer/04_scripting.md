---
KONU        : Beijer iX Developer — C# Scripting
KATEGORİ    : hmi
ALT_KATEGORI: ix-developer
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://www.beijerelectronics.com/docs/iX/3.0/User-Guide/en/scripts.html"
    başlık: "Scripts — iX Developer 3.0 User Guide (Resmi)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-Script/en/index-en.html"
    başlık: "Script Help — iX Developer Script Referans Dokümantasyonu (Resmi)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-Script/en/pitfalls.html"
    başlık: "Pitfalls — iX Developer Script Help (Resmi)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-Script/en/getting-started.html"
    başlık: "Getting Started — iX Developer Script Help (Resmi)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-Script/en/first-script.html"
    başlık: "First Script — iX Developer Script Help (Resmi)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-Script/en/referenced-assemblies.html"
    başlık: "Referenced Assemblies — iX Developer Script Help (Resmi)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-251-Reference/en/development-environment.html"
    başlık: "Development Environment — iX Developer 2.51 Reference (Resmi)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX-250-Reference/en/tags.html"
    başlık: "Tags — iX Developer 2.50 Reference (Resmi)"
    güvenilirlik: resmi
  - url: "https://www.beijerelectronics.com/docs/iX/3.0/User-Guide/en/optimize-performance.html"
    başlık: "Optimize Performance — iX Developer 3.0 User Guide (Resmi)"
    güvenilirlik: resmi
  - url: "https://timon.la/blog/tdd-for-ix/"
    başlık: "Advanced Scripting for Beijer iX Developer with TDD workflow — Timon Lapawczyk (Topluluk)"
    güvenilirlik: topluluk
  - url: "https://www.plctalk.net/forums/threads/stupid-beijer-stupid-ix-developer-stupid-c.109384/"
    başlık: "Stupid Beijer, stupid IX Developer, stupid C# — PLCtalk Forum (Topluluk)"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "knowledge/hmi/ix-developer/01_architecture.md"
    ilişki: gerektirir
  - konu: "knowledge/hmi/ix-developer/03_screen_design.md"
    ilişki: tamamlar
  - konu: "knowledge/hmi/web-based/03_react_patterns.md"
    ilişki: alternatif
ÖNKOŞUL     :
  - "Beijer iX Developer yazılımı kurulu ve temel proje yapısı anlaşılmış olmalı"
  - "C# temel programlama bilgisi (sınıf, metod, event, delegate)"
  - "HMI tag kavramı ve PLC/kontrolör bağlantısı bilinmeli"
ÇELİŞKİLER :
  - kaynak: "timon.la blog (.NET CF 3.5 kısıtlamaları)"
    konu: "Eski iX Developer sürümleri (2.40 ve öncesi) Windows CE panellerinde .NET Compact Framework 3.5 kullanır; modern C# özellikleri (expression-bodied member, get-only auto-property) çalışmaz. Ancak iX Developer 3.0 ile birlikte .NET 8'e geçildi; bu kısıtlamalar IPC hedefli projelerde kalktı."
    çözüm: "Hedef platform kritik: Windows CE panel → .NET CF 3.5 kısıtlamalarına dikkat. IPC/PC platformu ve iX 3.0+ → .NET 8 tam özellik seti. Proje hedefi kesinleşmeden kütüphane seçimi yapılmamalı."
  - kaynak: "iX Developer 2.51 resmi dokümanı (ValueOff/ValueOn kısıtlaması)"
    konu: "ValueOff ve ValueOn olayları dahili (internal) değişkenler için runtime'da tetiklenmez; yalnızca kontrolör tag'leri için çalışır. Resmi kaynak bu kısıtlamayı açıkça belirtmiştir, ancak neden'i açıklanmamıştır."
    çözüm: "Dahili değişkenler için ValueChangeOrError veya doğrudan Globals.Tags referansıyla polling yaklaşımı kullanılmalı."
  - kaynak: "Ekran navigasyon API sözdizimi (resmi kaynak bulunamadı)"
    konu: "Globals üzerinden ekran geçişi için kullanılan metodun tam adı (Globals.Navigate, ShowScreen veya başka bir isim) resmi web dokümanlarında açıkça görüntülenemedi. Yalnızca kavramsal referans bulundu."
    çözüm: "İlgili metod adı için iX Developer içindeki F1 Script Help veya IntelliSense kullanılmalı; bu belgede kavramsal düzeyde ele alınmıştır."
---

## Özün Ne

Beijer iX Developer, C# tabanlı bir scripting motoru sunarak standart eylem (action) yapılandırmalarının ötesine geçen özel davranışlar tanımlamayı sağlar. Script'ler, düğme tıklamalarından tag değer değişimlerine, ekran açılışından zamanlayıcı olaylarına kadar her türlü etkileşime bağlanabilir. Tüm script kodu C# sözdiziminde yazılır ve proje derlenmeden önce doğrulanır.

Scripting, iX Developer'ın diğer bileşenlerini (tag, ekran, nesne, alarm sunucusu) birleştiren yapıştırıcı katmandır. Hesap mantığı, dinamik görsel davranış, dosya/rapor üretimi ve özel komunikasyon gibi senaryolar için vazgeçilmezdir. Doğru kullanılmadığında ise bellek sızıntısı ve uygulama çökmesi gibi ciddi sonuçlar doğurur.

## Nasıl Çalışır

### Script Editörü ve Script View Mode

iX Developer'da ekranlar, nesneler, tag'ler ve fonksiyon tuşları için Script View Mode açılabilir. Bu mod, Layout ve XAML modlarından bağımsızdır. Script View'e geçmek için:

1. Bir nesne (örn. Button) seçilir.
2. Ekranın sol alt köşesindeki Script sekmesine tıklanır.
3. Nesnenin `[+]` düğmesine tıklanarak kullanılabilir olaylar (Click, ValueChanged vb.) listelenir.
4. Bir olayın üzerine çift tıklanır → metod başlığı otomatik eklenir, gövde boş bırakılır.

**IntelliSense:** `Ctrl+Spacebar` ile manuel tetiklenir; nokta (`.`) karakteri yazıldıktan sonra otomatik devreye girer. Aşırı yüklenmiş metodlarda parametre ipucu için `Ctrl+Shift+Spacebar` kullanılır.

**Build / Doğrulama:** Project ribbon sekmesinde Build komutu script kodunu derler ve hataları Error List panelinde gösterir. Hata satırına çift tıklanarak hatalı konuma atlanır.

**Harici Editör Desteği:** Visual Studio gibi harici editörler kullanılabilir. Ancak harici editörde yapılan değişiklikler iX Developer'ın cross-reference sistemine yansımaz. Geçici çözüm: Değiştirilen script dosyasını iX Developer'da açıp küçük bir değişiklik yapıp kaydetmek.

### Kapsam Modeli: Screen Script vs Global Script

iX Developer'da iki temel script kapsamı vardır:

| Kapsam | Tanım | Erişim Şekli |
|---|---|---|
| **Ekran Script'i** (Screen Script) | Belirli bir ekrana ait; o ekranın nesnelerine, tag'lerine ve olaylarına doğrudan erişebilir | Ekran sınıfının `partial class` üyesi olarak tanımlanır |
| **Global Script Modülü** (ScriptModule) | Proje genelinde yeniden kullanılabilir kod; herhangi bir ekrandan çağrılabilir | `Globals` anahtar kelimesiyle erişilir |

**Kritik kısıt:** "Scripting across different screens is not supported." Bir ekran script'i içinden başka bir ekranın nesnelerine doğrudan erişilemez. Farklı ekranlar arasında paylaşılması gereken veriler için tag'ler veya Global Script Modülleri kullanılır.

### Globals Nesnesi

`Globals` anahtar kelimesi, mevcut sınıfın dışındaki her şeye erişim noktasıdır:

| Globals Üyesi | Açıklama |
|---|---|
| `Globals.Tags.TagAdı` | Bir tag'e doğrudan referans |
| `Globals.AlarmServer` | Alarm sunucusuna erişim (olay aboneliği) |
| `Globals.Environment.Application` | Uygulama ortam bilgileri (depolama yolları, SD kart, USB) |
| `Globals.Navigate(...)` | Ekran navigasyonu (kesin sözdizimi için IntelliSense/F1 kullanılmalı) |

### .NET Framework Sürümleri ve Platform Farkları

| Platform | iX Sürümü | .NET Sürümü | Notlar |
|---|---|---|---|
| Windows CE Panel (EXTER) | 2.x ve öncesi | .NET Compact Framework 3.5 | Sınırlı API, modern C# özellikleri desteklenmez |
| IPC / PC | Tüm sürümler | Tam .NET Framework | Tam özellik seti |
| iX 3.0 (tüm hedefler) | 3.0+ | .NET 8 | NuGet desteği, tam modern C# |

**Uyarı:** Script editörü, Windows CE'de desteklenmeyen sınıf ve metodları da IntelliSense ile gösterir. Bu nedenle kod Windows CE panelde mutlaka hedef cihazda test edilmelidir.

## Pratikte Nasıl Kullanılır

### 1. Temel Button Click Script'i

En yaygın senaryo: Bir butona tıklandığında bir şey yapılması.

```csharp
public partial class Screen2
{
    void Button1_Click(System.Object sender, System.EventArgs e)
    {
        // Ekrandaki TextBox'ın metnini değiştir
        TextBox1.Text = "Sistem Çalışıyor";

        // Bir tag'e değer yaz
        Globals.Tags.MotorStart.Value = true;
    }
}
```

### 2. Tag Değeri Okuma ve Yazma

Tag'lere `Globals.Tags.TagAdı.Value` sözdizimi ile erişilir. Tip dönüşümü genellikle gereklidir:

```csharp
// Okuma — farklı veri tipleri
bool motorDurumu = (bool)Globals.Tags.Motor1_Running.Value;
int hiz          = (int)Globals.Tags.Motor1_Speed.Value;
double sicaklik  = (double)Globals.Tags.Temp_Sensor1.Value;
string mesaj     = Globals.Tags.StatusMessage.Value.ToString();

// Yazma
Globals.Tags.Motor1_Speed.Value = 1500;
Globals.Tags.AlarmAck.Value     = true;

// Hesaplanmış değer yazma (explicit cast zorunlu)
Globals.Tags.Alan.Value = (double)Globals.Tags.Uzunluk.Value 
                        * (double)Globals.Tags.Genislik.Value / 100.0;
```

**Not:** Çoklu aşırı yüklü operatörlerde explicit type cast zorunludur. Aksi hâlde build hatası alınır.

### 3. Tag ValueChanged Olayı

Bir tag'in değeri değiştiğinde tetiklenen olay:

```csharp
public partial class Screen3
{
    // Screen_Opened içinde abonelik kur
    void Screen3_Opened(System.Object sender, System.EventArgs e)
    {
        Globals.Tags.SicaklikSensoru.ValueChanged 
            += SicaklikSensoru_ValueChanged;
    }

    // ValueChanged handler
    void SicaklikSensoru_ValueChanged(System.Object sender, 
        Core.Api.DataSource.ValueChangedEventArgs e)
    {
        double deger = (double)e.Value;

        if (deger > 85.0)
        {
            LabelUyari.Text = "SICAKLIK YÜKSEK: " + deger.ToString("F1") + " °C";
            Globals.Tags.UyariAktif.Value = true;
        }
        else
        {
            LabelUyari.Text = "Normal";
            Globals.Tags.UyariAktif.Value = false;
        }
    }

    // Screen_Closed içinde abonelik iptal et — ZORUNLU (bellek sızıntısı önleme)
    void Screen3_Closed(System.Object sender, System.EventArgs e)
    {
        Globals.Tags.SicaklikSensoru.ValueChanged 
            -= SicaklikSensoru_ValueChanged;
    }
}
```

**Kısıt:** `ValueChangeOrError` olayı yalnızca kontrolör tag'leri için çalışır. `ValueOff`/`ValueOn` olayları dahili değişkenlerde runtime'da tetiklenmez.

### 4. Screen_Opened ve Screen_Closed Olayları

Ekran açılış/kapanış olayları, başlatma ve temizlik mantığı için kullanılır:

```csharp
public partial class Screen4
{
    private System.Timers.Timer _guncellemeTimer;

    void Screen4_Opened(System.Object sender, System.EventArgs e)
    {
        // Ekran açılırken bir tag'i sıfırla
        Globals.Tags.EkranAcildi.Value = true;

        // Zamanlayıcı başlat
        _guncellemeTimer = new System.Timers.Timer(1000); // 1 sn
        _guncellemeTimer.Elapsed += OnTimerElapsed;
        _guncellemeTimer.Enabled = true;
    }

    void OnTimerElapsed(System.Object sender, System.Timers.ElapsedEventArgs e)
    {
        // Her saniye çalışacak kod
        Globals.Tags.CalismaSuresi.Value = 
            (int)Globals.Tags.CalismaSuresi.Value + 1;
    }

    void Screen4_Closed(System.Object sender, System.EventArgs e)
    {
        // Zamanlayıcıyı durdur ve aboneliği iptal et — ZORUNLU
        if (_guncellemeTimer != null)
        {
            _guncellemeTimer.Enabled = false;
            _guncellemeTimer.Elapsed -= OnTimerElapsed;
            _guncellemeTimer.Dispose();
            _guncellemeTimer = null;
        }

        Globals.Tags.EkranAcildi.Value = false;
    }
}
```

### 5. Global Script Modülü (Yeniden Kullanılabilir Kod)

Global Script Modülleri, proje genelinde çağrılabilir ortak metod kütüphaneleridir. `IScriptTag` arayüzü ile parametreler belirli bir tag'e bağlı kalmadan geçirilir:

```csharp
// GlobalHesaplamalar.Script.cs — Global Script Modülü
public class GlobalHesaplamalar
{
    // IScriptTag ile reusable metod — herhangi bir tag grubuyla çalışır
    public void Topla(IScriptTag arg1, IScriptTag arg2, IScriptTag sonuc)
    {
        sonuc.Value = arg1.Value.Int + arg2.Value.Int;
    }

    public void OranHesapla(IScriptTag deger, IScriptTag maks, IScriptTag oran)
    {
        if ((double)maks.Value != 0)
            oran.Value = ((double)deger.Value / (double)maks.Value) * 100.0;
        else
            oran.Value = 0.0;
    }

    // Direkt tag referanslı metod (belirli tag'lere bağlı)
    public double HattaVerimOku()
    {
        double uretilen = (double)Globals.Tags.UretilenAdet.Value;
        double hedef    = (double)Globals.Tags.HedefAdet.Value;
        return hedef > 0 ? (uretilen / hedef) * 100.0 : 0.0;
    }
}
```

Ekran script'inden çağrım:

```csharp
void BtnHesapla_Click(System.Object sender, System.EventArgs e)
{
    // Global modül üzerinden hesap yaptır
    Globals.GlobalHesaplamalar.Topla(
        Globals.Tags.Deger1,
        Globals.Tags.Deger2,
        Globals.Tags.Toplam
    );
}
```

### 6. Alarm Sunucusu Olay Aboneliği

```csharp
public partial class Screen5
{
    void Screen5_Opened(System.Object sender, System.EventArgs e)
    {
        Globals.AlarmServer.AlarmActive += OnAlarmAktif;
    }

    void OnAlarmAktif(System.Object sender, System.EventArgs e)
    {
        // Alarm aktif olduğunda çalışacak kod
        Globals.Tags.AktifAlarmSayisi.Value = 
            (int)Globals.Tags.AktifAlarmSayisi.Value + 1;
    }

    void Screen5_Closed(System.Object sender, System.EventArgs e)
    {
        // ZORUNLU — aksi hâlde Globals.AlarmServer Screen5'e referans tutar,
        // ekran garbage collect edilemez → bellek sızıntısı
        Globals.AlarmServer.AlarmActive -= OnAlarmAktif;
    }
}
```

### 7. Dosyaya Yazma ve Rapor Üretimi

Güç kesintisi sırasında dosya bozulmasını önlemek için `FileOptions.WriteThrough` kullanılır (resmi Beijer önerisi):

```csharp
using System.IO;
using System.Text;

public void RaporYaz(string dosyaYolu, string icerik)
{
    // WriteThrough: Önbellek atlanarak doğrudan diske yazılır
    const FileOptions secenek = FileOptions.WriteThrough;

    using (FileStream akis = new FileStream(
        dosyaYolu,
        FileMode.Create,
        FileAccess.Write,
        FileShare.Write,
        4096,
        secenek))
    {
        akis.Write(Encoding.UTF8.GetBytes(icerik));
    }
}

// CSV raporu örneği
void BtnRaporUret_Click(System.Object sender, System.EventArgs e)
{
    string usbYolu = Globals.Environment.Application.FirstDetectedUsbDriveLetter 
                   + @"\rapor.csv";

    System.Text.StringBuilder sb = new System.Text.StringBuilder();
    sb.AppendLine("Zaman,Motor1_Hız,Motor1_Sıcaklık,Üretim");
    sb.AppendLine(
        System.DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss") + "," +
        Globals.Tags.Motor1_Speed.Value.ToString() + "," +
        Globals.Tags.Motor1_Temp.Value.ToString() + "," +
        Globals.Tags.UretilenAdet.Value.ToString()
    );

    RaporYaz(usbYolu, sb.ToString());
    LabelDurum.Text = "Rapor USB'ye kaydedildi.";
}
```

### 8. Dinamik Görsel Davranış

Ekran açılışında bir nesnenin görsel özelliğini dinamik olarak ayarlama:

```csharp
void Screen1_Opened(System.Object sender, System.EventArgs e)
{
    // Degrade renk dolgusu (PC/IPC platformu — Windows CE'de WPF desteklenmez)
    Rectangle1.Fill = new BrushCF(
        System.Drawing.Color.Red,
        System.Drawing.Color.Purple,
        FillDirection.Center
    );
}
```

### 9. .NET Kütüphanesi Referanslama

**iX Developer 2.x:** Project → Referenced Assemblies üzerinden `.dll` dosyaları eklenir. İç kütüphanelerle ad çakışması olursa build hatası oluşur.

**iX Developer 3.0+:** NuGet Paket Yöneticisi kullanılır. `M2Mqtt.NetCf35.dll`, `Newtonsoft.Json.Compact.dll` gibi paketler doğrudan NuGet'ten eklenir.

```csharp
// Newtonsoft.Json ile JSON serileştirme (iX 3.0 + NuGet)
using Newtonsoft.Json;

void BtnJsonYaz_Click(System.Object sender, System.EventArgs e)
{
    var veri = new {
        zaman   = System.DateTime.Now,
        motor   = (int)Globals.Tags.Motor1_Speed.Value,
        sicaklik = (double)Globals.Tags.Motor1_Temp.Value
    };
    string json = JsonConvert.SerializeObject(veri);
    Globals.Tags.JsonCikti.Value = json;
}
```

### 10. Ekran Navigasyonu Script ile

Ekran geçişleri script üzerinden tetiklenebilir (kesin API adı için IntelliSense / F1 kullanılmalı):

```csharp
void BtnDetailScreen_Click(System.Object sender, System.EventArgs e)
{
    // Hangi motor seçiliyse ilgili detay ekranına git
    int motorNo = (int)Globals.Tags.SeciliMotor.Value;
    Globals.Tags.NavigasyonParametresi.Value = motorNo;

    // Globals üzerinden ekran geçişi — kesin metod adı iX sürümüne göre değişir
    // IntelliSense ile "Globals." yazdıktan sonra navigasyon metodları listelenir
}
```

## Örnekler

### Senaryo A: Üretim Hattı Verim Hesabı

```csharp
// Her 5 saniyede bir verim hesapla ve tag'e yaz
public partial class ScreenUretim
{
    private System.Timers.Timer _verimTimer;

    void ScreenUretim_Opened(System.Object sender, System.EventArgs e)
    {
        _verimTimer = new System.Timers.Timer(5000);
        _verimTimer.Elapsed += HesaplaVerim;
        _verimTimer.Enabled = true;
    }

    void HesaplaVerim(System.Object sender, System.Timers.ElapsedEventArgs e)
    {
        double uretilen = (double)Globals.Tags.UretilenAdet.Value;
        double hedef    = (double)Globals.Tags.HedefAdet.Value;
        double fire     = (double)Globals.Tags.FireAdet.Value;

        if (hedef > 0)
        {
            double verim = ((uretilen - fire) / hedef) * 100.0;
            Globals.Tags.HatVerimi.Value = System.Math.Round(verim, 1);
        }
    }

    void ScreenUretim_Closed(System.Object sender, System.EventArgs e)
    {
        if (_verimTimer != null)
        {
            _verimTimer.Enabled = false;
            _verimTimer.Elapsed -= HesaplaVerim;
            _verimTimer.Dispose();
            _verimTimer = null;
        }
    }
}
```

### Senaryo B: Alarm Aktif Olduğunda Olay Kaydı

```csharp
public partial class ScreenAlarm
{
    void ScreenAlarm_Opened(System.Object sender, System.EventArgs e)
    {
        Globals.AlarmServer.AlarmActive     += KaydetAlarmAktif;
        Globals.AlarmServer.AlarmAcknowledge += KaydetAlarmOnay;
    }

    void KaydetAlarmAktif(System.Object sender, System.EventArgs e)
    {
        string kayit = System.DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
                     + " | ALARM AKTİF\r\n";
        Globals.Tags.AlarmLog.Value = 
            Globals.Tags.AlarmLog.Value.ToString() + kayit;
    }

    void KaydetAlarmOnay(System.Object sender, System.EventArgs e)
    {
        string kayit = System.DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
                     + " | ALARM ONAYLANDI\r\n";
        Globals.Tags.AlarmLog.Value = 
            Globals.Tags.AlarmLog.Value.ToString() + kayit;
    }

    void ScreenAlarm_Closed(System.Object sender, System.EventArgs e)
    {
        Globals.AlarmServer.AlarmActive     -= KaydetAlarmAktif;
        Globals.AlarmServer.AlarmAcknowledge -= KaydetAlarmOnay;
    }
}
```

### Senaryo C: AdaptedObject ile Platform'a Özel Görsel Efekt (PC hedef)

```csharp
void Screen1_Opened(System.Object sender, System.EventArgs e)
{
    // PC/WPF hedefi — Windows CE'de çalışmaz
    System.Windows.Controls.Button wpfButton = 
        Button1.AdaptedObject as System.Windows.Controls.Button;

    if (wpfButton != null)
    {
        var effect = new System.Windows.Media.Effects.DropShadowEffect();
        effect.Color      = System.Windows.Media.Colors.Blue;
        effect.BlurRadius = 10;
        wpfButton.Effect  = effect;
    }
}
```

**Uyarı:** `AdaptedObject` kullanımı platform hedefini kilitler; IPC → Windows CE geçişinde build hatası oluşur.

## Sık Yapılan Hatalar

### 1. Olay Aboneliğini İptal Etmemek (Bellek Sızıntısı)

**Sorun:** `Globals.AlarmServer.AlarmActive += handler` ya da timer `Elapsed += handler` gibi abonelikler Screen_Closed içinde iptal edilmezse, nesne garbage collector tarafından toplanamaz. Bu durum birikimli bellek sızıntısına ve sonunda uygulama çökmesine yol açar.

**Çözüm:** Her `+=` için ilgili `Closed` olayında mutlaka `-=` bulunmalıdır.

```csharp
// YANLIŞ — abonelik iptal edilmemiş
void Screen_Opened(...) { SomeEvent += MyHandler; }
// Screen_Closed içinde hiçbir şey yok → sızıntı

// DOĞRU
void Screen_Opened(...) { SomeEvent += MyHandler; }
void Screen_Closed(...) { SomeEvent -= MyHandler; }
```

### 2. Zamanlayıcıyı Kapatmamak

**Sorun:** Screen_Closed çağrıldıktan sonra timer hâlâ çalışmaya devam eder. Ekran bellekten temizlenemez.

**Çözüm:**
```csharp
void Screen_Closed(...)
{
    timer.Enabled = false;
    timer.Elapsed -= Handler;
    timer.Dispose();
    timer = null;
}
```

### 3. Static State Kullanmak

**Sorun:** Script sınıfında `static` alanlara veri yazılması global durum kirliliğine ve bellek sızıntısına yol açar.

**Çözüm:** Statik alanlardan kaçınılmalı; veri paylaşımı için tag'ler veya Global Script Modülleri kullanılmalıdır.

### 4. Blocking Script Yazmak

**Sorun:** `Thread.Sleep()`, `Console.ReadLine()`, `MessageBox.Show()` gibi çağrılar UI thread'ini bloklar ve uygulama donabilir.

**Çözüm:** Resmi doküman açıkça belirtir: "Creating scripts that block execution, waiting for other resources or user input, is not supported." Uzun işlemler için timer veya arka plan thread kullanılmalı, UI thread serbest bırakılmalıdır.

### 5. Action ve Script'i Birlikte Kullanmak

**Sorun:** Bir nesneye hem Action hem de Script tanımlandığında Action öncelik alır. Script beklendiği gibi çalışmayabilir.

**Çözüm:** "When actions are defined for an object, this will have precedence over script code." — bir nesne için ya Action ya Script, ikisi birden değil.

### 6. Nesne/Ekran Adını Layout Modda Değiştirmek

**Sorun:** Script view'de referanslanan bir nesnenin adı Layout modda değiştirilirse script kodu eski adı referans etmeye devam eder ve build hatası oluşur.

**Çözüm:** İsim değişikliğinden sonra ilgili tüm script referansları manuel olarak güncellenmeli.

### 7. .NET Compact Framework Uyumsuzluğu

**Sorun:** IntelliSense, Windows CE'de desteklenmeyen metodları da listeler. Kod geliştirme makinasında derlense bile panelde çalışmayabilir.

**Çözüm:** Windows CE panel hedefli projelerde her yeni kütüphane / metod mutlaka hedef cihazda test edilmeli. iX Developer 3.0 + IPC hedefi kullanılıyorsa bu sorun ortadan kalkar.

### 8. Tag'in Script'te Aktif Olmaması

**Sorun:** Bazı tag'ler script içinde `Globals.Tags.TagAdı` sözdizimi ile kullanılsa bile cross-reference tarafından tanınmayabilir ve "Remove Unused Tags" ile yanlışlıkla silinebilir.

**Çözüm:** `Globals.Tags.TagAdı` sözdizimi kullanılmalı (direkt referans); harici editörde değişiklik yapıldıysa iX Developer'da açıp küçük bir düzenleme yapıp kaydedilmelidir.

## Ne Zaman Tercih Edilmeli / Edilmemeli

### Script Kullanılmalı:

- Standart eylem/bağlama (binding) yetmeyen karmaşık hesap mantığı gerektiğinde
- Birden fazla tag ve UI nesnesini ilişkilendiren özel iş kuralları yazılırken
- Dosyaya yazma, rapor üretimi, CSV export gibi I/O işlemleri için
- Zamanlayıcı tabanlı periyodik görevler (üretim sayacı, verim hesabı)
- Alarm olaylarına özel tepki mantığı eklenirken
- Üçüncü parti .NET kütüphaneleri entegre edilirken (MQTT, JSON, serial port)
- Yeniden kullanılabilir hesaplama mantığı modüler yapıda tutulmak istendiğinde

### Script Kullanılmamalı / Dikkat Edilmeli:

- Standart bağlama (tag → UI nesne) yeterliyse — Actions/Bindings daha güvenli ve bakımı kolay
- Windows CE panel hedefli projelerde modern .NET özelliklerine ihtiyaç varsa — platform kısıtlamaları geçerli
- UI thread'i bloklayacak işlemler için — asla blocking script yazılmamalı
- Cross-screen mantık için — ekranlar arası scripting desteklenmez, tag'ler üzerinden iletişim kurulmalı
- Her görsel davranış için script yerine Expression/Binding tercih edilmeli — script aşırı kullanımı bakım yükü yaratır

## Gerçek Proje Notları

**Not 1 — Bellek Sızıntısı En Büyük Tehlike**
Endüstriyel uygulamalarda paneller haftalarca, aylarca yeniden başlatılmadan çalışır. Tek bir eksik `-=` abonelik iptali, zamanla uygulama çökmesine yol açabilir. Kural: Her `Screen_Opened` içinde yapılan kaynak edinimi (timer başlatma, event aboneliği) için `Screen_Closed` içinde karşılıklı temizlik kodu zorunludur.

**Not 2 — .NET Sürüm Kararı Erkenden Verilmeli**
Windows CE panel mi, IPC mi sorusu projenin başında netleştirilmelidir. Windows CE seçilirse modern NuGet paketleri, LINQ sorguları, async/await ve expression-bodied üyeler kullanılamaz. Bu karar sonradan değiştirilmek istenirse kod tabanı ciddi ölçüde yeniden yazılmak zorunda kalır.

**Not 3 — IScriptTag ile Modülerlik**
`Globals.Tags.BelirliTagAdi.Value` şeklinde sabit referanslar, kodu belirli bir tag yapısına bağlar. Farklı hat veya makine konfigürasyonlarına aynı hesap mantığını uygulamak için `IScriptTag` parametreli ScriptModule metodları çok daha esnek ve yeniden kullanılabilirdir. Ölçeklenen projeler için bu ayrımı erken yapmak büyük zaman kazandırır.

**Not 4 — FileOptions.WriteThrough Endüstriyel Zorunluluk**
Standart `File.WriteAllText()` işletim sistemi önbelleğine yazar; güç kesintisinde dosya bozulabilir. Endüstriyel ortamlarda güç kesintisi her an mümkündür. Beijer'in resmi önerisi olan `FileOptions.WriteThrough` + `FileStream` kullanımı bu riski minimize eder.

**Not 5 — Harici Editör Kullanımı: Fayda ve Risk**
Visual Studio'da geliştirme, otomatik tamamlama, refactoring ve unit test desteği sağlar. Timon Lapawczyk'ın TDD yaklaşımı (timon.la blog) bu iş akışını belgeler: Script dosyaları VS projesiyle link'lenir, `VariableReference<T>` ile tag bağımlılıkları mock'lanır. Ancak iX Developer'ın cross-reference ve "Remove Unused Tags" sistemleri harici editörü görmez; bu nedenle iX Developer'da ara ara küçük kaydetme yapılmalıdır.

**Not 6 — Actions Önceliği Tuzağı**
Aynı nesneye hem Action hem Script tanımlandığında Action önce çalışır. Bu, script'in hiç çalışmadığı izlenimi yaratabilir ve tespit edilmesi zaman alan bir hatadır. Bir nesne için tek mekanizma seçilmeli; önce varolan Action tanımları kontrol edilmelidir.

**Not 7 — Timer Thread'i UI Thread'i Değil — Cross-Thread Erişim Tuzağı**
`System.Timers.Timer` Elapsed olayı UI thread'inde değil, bir thread pool thread'inde çalışır. Bir projede Elapsed handler'ı içinden doğrudan bir ekran nesnesinin `.Text`'i değiştirildiğinde PC hedefinde sporadik çökme yaşandı (WPF nesnelerine yalnızca sahip oldukları thread'den erişilebilir). Tag yazma (`Globals.Tags.X.Value`) thread-safe'tir ve sorun çıkarmaz; ancak doğrudan UI nesne erişimi gerektiğinde değer bir tag'e yazılıp nesne o tag'e bind edilmeli. Kural: timer içinden tag yaz, nesneye dokunma.

**Not 8 — Globals.Tags Cross-Reference'a Görünür, String İndeksleme Görünmez**
`Globals.Tags.MotorHiz` doğrudan referansı iX'in cross-reference sistemine görünür ve "Remove Unused Tags" bunu korur. Ancak bazı kodlarda tag'e dinamik/string tabanlı erişim denenince (yansıma benzeri) cross-reference tag'i "kullanılmıyor" sayıp silebildi; sonraki derlemede runtime hatası çıktı. Her zaman güçlü-tipli `Globals.Tags.X` sözdizimi kullanılmalı; dinamik tag adı gerekiyorsa IScriptTag parametresiyle geçirilmeli.

**Not 9 — Build Hatası "Eski İsim" — Layout'ta Yeniden Adlandırma Sonrası**
Script'te referanslanan bir nesne Layout modda yeniden adlandırıldığında iX referansları otomatik güncellemez; build "CS0103: 'Button1' does not exist" verir. Büyük bir ekranı yeniden düzenleyen bir ekipte bu, derlemeyi saatlerce bloke etti çünkü hatanın script'te değil rename'de olduğu fark edilmedi. Nesne yeniden adlandırma öncesi script referansları aranmalı; mümkünse adlandırma baştan kesinleştirilmeli.

**Not 10 — Async/await ve LINQ Sadece iX3/.NET 8 ve IPC'de Güvenli**
Bir geliştirme PC'sinde (tam .NET Framework) sorunsuz derlenen LINQ ve async/await içeren kod, Windows CE panel hedefinde (.NET CF 3.5) derleme veya runtime hatası verdi — IntelliSense bu metodları gösterdiği için yanıltıcıydı. Modern dil/kütüphane özellikleri yalnızca iX3 (.NET 8) veya IPC tam framework hedefinde güvenle kullanılabilir. Hedef platform kütüphane seçiminden önce kesinleştirilmelidir.

## Edge Case'ler ve Sistem Limitleri

Scripting katmanında sınırlar çoğunlukla çalışma zamanı modeli (tek UI thread, derlenmiş kod, platform .NET sürümü) ile ilgilidir.

| Alan | Sınır / Davranış | Sonuç |
|---|---|---|
| Cross-screen erişim | Desteklenmez | Başka ekranın nesnesine erişim derlenmez; tag ile köprü kurulur |
| Blocking çağrı | Desteklenmez | Thread.Sleep / MessageBox / ReadLine → UI donar |
| ValueOn / ValueOff | Yalnızca controller tag | Internal tag'de runtime'da hiç tetiklenmez (sessiz) |
| Static alan | Önerilmez | Global durum kirliliği + sızıntı |
| Timer Elapsed | Thread pool thread | UI nesne erişimi cross-thread hatası |
| AdaptedObject | Platform kilitler | IPC→CE geçişinde build hatası |
| .NET sürümü | CE: CF 3.5 / IPC: full / iX3: .NET 8 | Hedefe göre özellik seti değişir |

**Olay aboneliği yaşam döngüsü:** `+=` ile kurulan her abonelik (timer, AlarmServer, ValueChanged) ekran kapanışında `-=` ile sökülmezse, AlarmServer/timer ekran nesnesine referans tutmaya devam eder; ekran garbage collect edilemez ve haftalarca çalışan panelde birikimli bellek sızıntısı uygulamayı çökertir. Bu, scriptingdeki en kritik edge case'tir — `Opened`'daki her `+=` için `Closed`'da karşılık gelen `-=` zorunludur.

**Action vs Script önceliği:** Aynı nesneye hem Action hem Script atanırsa Action öncelik alır ve script hiç çalışmamış gibi görünür — hata mesajı yoktur. Tek mekanizma kuralı geçerlidir.

**Explicit cast zorunluluğu:** `Globals.Tags.X.Value` aşırı yüklü tip dönüşümleri içerdiğinden, aritmetik veya atamada explicit cast (`(double)`, `(int)`) olmadan build hatası verir. Bu, runtime sürprizi yerine derleme zamanı yakalanan bir kısıttır.

**Internal tag persistency:** Script'ten internal tag'e yazılan değer, tag non-volatile değilse panel yeniden başladığında kaybolur; non-volatile olsa bile ani güç kesintisinde son değişim flash'a yazılmamış olabilir (bkz. 01 belgesi). Kritik sayaçlar PLC retain değişkende tutulmalı.

## Optimizasyon

**1. Script yerine binding/expression tercih et**
Her görsel davranış için script yazmak hem bakım yükü hem performans maliyetidir. Basit tag→nesne ilişkileri Dynamics/Expression ile çözülmeli; script yalnızca standart mekanizmanın yetmediği karmaşık mantık için kullanılmalıdır. Aşırı script kullanımı render ve bakım maliyetini artırır.

**2. ValueChanged'i polling timer'a tercih et**
Bir değerin değişimine tepki vermek için her saniye çalışan bir timer ile tag okumak yerine, `ValueChanged` olayına abone olmak hem CPU hem iletişim açısından verimlidir — kod yalnızca gerçekten değişiklik olduğunda çalışır. Timer yalnızca gerçekten periyodik (zamana bağlı) görevler için kullanılmalı.

**3. IScriptTag ile yeniden kullanılabilir modüller**
Sabit `Globals.Tags.BelirliAd` referansları kodu tek bir tag yapısına bağlar. `IScriptTag` parametreli Global Script Modülleri, aynı hesabı farklı hat/makine tag setlerine uygulamayı sağlar — kod tekrarını ve bakım yükünü azaltır.

**4. Timer'da hafif işlem, ağır işi tag'e devret**
Timer Elapsed handler'ı kısa tutulmalı; uzun hesaplar UI tepkiselliğini değil ama thread havuzunu meşgul eder ve abonelik temizliğini zorlaştırır. Mümkünse hesap PLC tarafına alınmalı, HMI yalnızca sonucu göstermeli.

**5. Dosya I/O'yu seyrek ve WriteThrough ile yap**
Her tag değişiminde dosyaya yazmak disk I/O baskısı yaratır. Rapor/CSV yazımı periyodik (vardiya sonu, buton tetikli) yapılmalı ve `FileOptions.WriteThrough` ile güç kesintisine dayanıklı hale getirilmeli — sürekli yazma hem performans hem flash ömrü açısından zararlıdır.

**6. Gereksiz abonelikten kaçın**
Yalnızca aktif ekranda gereken olaylara abone olunmalı; tüm AlarmServer olaylarına global abonelik, her alarm değişiminde script tetikler ve gereksiz yük üretir. Olay aboneliği ekran yaşam döngüsüyle (Opened/Closed) sınırlandırılmalıdır.

## Derin Teknik Detay

**Script neden yorumlanmaz, derlenir?**
iX, C# script'leri runtime'da yorumlamaz; Build aşamasında bunları ekran sınıflarının `partial class` üyeleri olarak gerçek .NET assembly'lerine derler. Bunun nedeni performans ve tip güvenliğidir: yorumlanan bir motor, her olay tetiklenişinde ayrıştırma ve tip çözümleme maliyeti doğururdu — gömülü panelin sınırlı CPU'sunda bu kabul edilemez. Derlenmiş model, scriptin native .NET hızında çalışmasını ve hataların derleme zamanı yakalanmasını sağlar. Bedeli, canlı düzenleme olmaması ve her değişikliğin yeniden derleme + transfer gerektirmesidir. Bu yüzden iX scripting, tarayıcıda anında çalışan web HMI script'lerinden temelde farklı bir yaşam döngüsüne sahiptir.

**Neden cross-screen scripting yasak?**
Her ekran kendi `partial class`'ı olarak derlenir ve nesneleri o sınıfın private üyeleridir. Bir ekranın nesneleri yalnızca o ekran runtime'da yüklüyken bellekte var olur — kapalı bir ekranın nesneleri instantiate edilmemiştir. Başka ekranın nesnesine doğrudan erişim, var olmayan bir nesneye referans anlamına gelirdi. iX bu durumu derleme zamanı kuralıyla (cross-screen desteklenmez) engeller; ekranlar arası veri paylaşımı, ekran yaşam döngüsünden bağımsız var olan tag'ler veya Global Script Modülleri (proje boyu tek instance) üzerinden yapılır. Bu, "ekran = geçici görünüm, tag = kalıcı durum" mimari ayrımının doğrudan sonucudur.

**Globals nesnesi ve singleton model**
`Globals`, runtime'ın tag motoru, alarm sunucusu ve ortam servislerine tek erişim noktasıdır — etkin bir service locator / singleton'dır. Ekran script'lerinin doğrudan instance alanları yerine `Globals` üzerinden erişmesinin nedeni, bu servislerin uygulama boyu tek bir örnek olarak yaşamasıdır: tag motoru tüm ekranlar için aynıdır. Bu yüzden bir ekranda `Globals.AlarmServer.AlarmActive += handler` yapmak, ekran kapansa bile AlarmServer'ın handler'a (ve dolayısıyla ekrana) referans tutmasına yol açar — singleton uzun ömürlüdür, ekran kısa ömürlü. Bellek sızıntısı tuzağının kök nedeni bu ömür uyumsuzluğudur.

**.NET CF 3.5 vs .NET 8 — neden platform kütüphane setini belirler?**
Windows CE panellerde çalışan iX2 runtime'ı .NET Compact Framework 3.5 üzerine kuruludur; CF, tam .NET Framework'ün gömülü cihazlar için budanmış bir alt kümesidir (LINQ kısıtlı, async/await yok, birçok BCL sınıfı eksik). iX Developer'ın editörü geliştirme PC'sinin tam framework'ünün IntelliSense'ini gösterdiği için, CE'de var olmayan API'leri de önerir — bu "derlenir ama panelde çalışmaz" tuzağının nedenidir. iX3, .NET 8'e (cross-platform, modern runtime) geçerek bu ikiliği ortadan kaldırır ve NuGet ekosistemini açar. Hedef platformun .NET sürümü, kullanılabilecek dil ve kütüphane özelliklerini doğrudan belirler; bu yüzden platform kararı kod yazmadan önce verilmelidir.

**WriteThrough neden endüstriyel zorunluluk?**
Standart `File.WriteAllText` veya tamponlu `FileStream`, veriyi önce işletim sistemi yazma önbelleğine koyar; fiziksel diske/flash'a yazım gecikmeli ve toplu yapılır. Bir endüstriyel panelde güç kesintisi her an mümkündür ve önbellekteki yazılmamış veri kaybolur — dahası, dosya yarım yazılmış (corrupt) kalabilir. `FileOptions.WriteThrough`, OS önbelleğini atlayıp her yazımı doğrudan kalıcı depolamaya zorlar; bu, performanstan ödün vererek tutarlılık/dayanıklılık kazanır. Beijer'in bunu resmi olarak önermesinin nedeni, HMI'ın denetimsiz güç ortamında çalışmasıdır — bu, masaüstü yazılımından farklı bir güvenilirlik gereksinimidir.

## İlgili Konular

```
knowledge/hmi/ix-developer/
├── 01_architecture.md        → iX Developer genel mimarisi, proje yapısı
├── 02_codesys_connection.md  → CODESYS PLC bağlantısı, tag eşleme
├── 03_screen_design.md       → Ekran tasarımı, nesneler, layout
└── 04_scripting.md           ← Şu an buradasınız

knowledge/hmi/architecture/
├── 01_hmi_patterns.md        → ISA-101 mimari çerçeve
└── 03_alarm_management.md    → ISA-18.2 alarm yönetimi

knowledge/hmi/web-based/
└── 03_react_patterns.md      → Web tabanlı HMI alternatifi (React)

Standartlar ve referanslar:
  Beijer iX Script Help (iX Developer içinden F1)
  Microsoft .NET Compact Framework belgeleri (CE panel hedefi için)
  Beijer iX Talk forumu: https://connected.beijerelectronics.com/
```
