# WPF + OPC Foundation SDK Masaüstü HMI (EXAMPLE_conveyor)

CODESYS PLC'ye **doğrudan** (gateway yok) OPC-UA ile bağlanan WPF (.NET 8) masaüstü
HMI. MVVM deseni; OPC-UA Session + Subscription + MonitoredItem ile real-time veri.
`EXAMPLE_conveyor` projesinin `GVL_HMI` değişkenlerini izler ve komut yazar.

## Özellikler

- **OPC Foundation .NET SDK** (`OPCFoundation.NetStandard.Opc.Ua.Client` 1.5.378.x).
- **MVVM** (CommunityToolkit.Mvvm): `MainViewModel` Session + Subscription'ı sürer.
- **Subscription + MonitoredItem**: real-time bildirim; callback ThreadPool thread'inde
  gelir, `Dispatcher.BeginInvoke` ile UI thread'ine taşınır.
- **SessionReconnectHandler** + `TransferSubscriptionsOnReconnect=true`: bağlantı
  kopunca abonelik aktarılır.
- **3 bölge göstergesi** (durum/hız/mod), durum şeridi, alarm `DataGrid`
  (ISA-18.2 esinli; Acknowledge ≠ Resolved), komut Button'ları (`axCmdAutoRun[i]`,
  `xCmdReset`).
- **Heartbeat watchdog**: `uHeartbeat` 3 sn değişmezse "VERİ BAYAT" + komut kilidi.

## Dosya yapısı

```
dotnet-wpf-opcua/
├── ConveyorHmi.csproj          # net8.0-windows, NuGet referansları
├── App.xaml / App.xaml.cs      # Uygulama giriş noktası
├── MainWindow.xaml / .cs        # View (DataGrid, bölge ItemsControl, butonlar)
├── HmiConfig.cs                # Endpoint, namespace URI, NodeId tanımları
├── Services/
│   └── OpcUaService.cs         # Session, Subscription, reconnect, write
├── ViewModels/
│   ├── MainViewModel.cs        # Ana VM: tag dispatch, watchdog, alarm yönetimi
│   ├── ZoneViewModel.cs        # Bölge VM
│   └── AlarmViewModel.cs       # Alarm kaydı VM
└── Converters/
    └── BoolToBrushConverter.cs # ISA-101 renk binding
```

## Kurulum

.NET 8 SDK gereklidir (WPF olduğundan **Windows**):

```powershell
dotnet restore
```

## Çalıştırma

```powershell
dotnet run
```

Pencere açılır; "Bağlan" ile PLC'ye bağlanılır. İlk çalıştırmada `./pki` altında
istemci sertifikası otomatik üretilir.

## PLC endpoint / NodeId konfigürasyonu

`HmiConfig.cs` içinde:

- `EndpointUrl` — CODESYS OPC-UA Server adresi (varsayılan port 4840).
- `CodesysNamespaceUri` — namespace URI. **Namespace index sabit yazılmaz**;
  `session.NamespaceUris.GetIndex(URI)` ile alınır. URI'yi UaExpert ile doğrulayın.
- `RuntimeName` / `ApplicationName` — NodeId yolundaki Runtime + Application adı.

CODESYS tarafı: Symbol Configuration ekleyin, "Support OPC UA features" işaretleyin,
PLC'ye indirip Runtime'ı başlatın.

### Array node'ları

CODESYS `ARRAY[1..3]` değişkenleri OPC-UA'da Array (`object[]`) değeri olarak gelir;
`MainViewModel.EnumerateArray` bunu indeksleyerek bölgelere dağıtır. Yazmada eleman
node'u (`axCmdAutoRun[1]`) kullanılır. Sunucunuz array'i farklı açıyorsa
`OpcUaService.WriteAutoRunAsync` ve `EnumerateArray` mantığını UaExpert'teki gerçek
yapıya göre uyarlayın.

## Güvenlik notu

Varsayılan `UseSecurity=false` yalnızca **geliştirme** içindir; bu modda güvenilmeyen
sunucu sertifikaları otomatik kabul edilir (`AutoAcceptUntrustedCertificates`).
Üretimde:

1. `HmiConfig.UseSecurity = true` yapın (otomatik kabul kapanır).
2. İstemci sertifikası `./pki/own` altında otomatik üretilir; sunucunun trusted
   listesine ekleyin (CODESYS: Device > Security > Trusted Clients).
3. Sunucu sertifikasını `./pki/trusted/certs/` klasörüne ekleyin.
4. `OnCertificateValidation` içinde parmak izi (thumbprint) eşleşmesiyle onaylayın.
5. Basic256Sha256 + SignAndEncrypt; CODESYS'te anonim erişimi kapatın, kullanıcı
   adı/parola (`UserName`/`Password`) tanımlayın.

`SequentialPublishing=true` ile bildirimler sıralı işlenir (sayaç/heartbeat için
önemli). Kritik komutlarda reconnect sırasındaki belirsiz durum için write sonrası
read-back doğrulaması önerilir.
