# Structured Text Kod Parçacıkları

Kopyala-yapıştır hazır, IEC 61131-3 Structured Text kod parçacıkları.
Ev stili: Türkçe ama ASCII yorumlar, sihirli sayı yok (sabitler `VAR_INPUT`/`VAR CONSTANT`),
güvenli varsayılanlar, sıfıra bölme koruması, her FB tek sorumluluk.

Referans örnek: `projects/EXAMPLE_conveyor/program/03_FB_AnalogScale.st`

## Dosyalar

- **`01_motor_start_stop.st`** — `FB_MotorStartStop`: start (NO) / stop (NC tel-emniyetli) butonları, interlock, çalışma geri beslemesi denetimi, kilitli arıza + reset; durdurma/arıza reset-dominant (güvenli taraf).
- **`02_analog_scaling.st`** — `FB_EngToRaw` (tersine ölçekleme rEng→iRaw, 4-20mA çıkış) + `FB_EMAFilter` (üstel hareketli ortalama gürültü filtresi) + `FB_AnalogScale` kullanım örneği.
- **`03_pid_loop.st`** — `FB_SimplePID`: anti-windup (integral clamp), manuel/oto bumpless geçiş, çıkış kelepçeleme; ayrıca CODESYS standart `FB_PID` kullanım örneği.
- **`04_timer_patterns.st`** — TON/TOF/TP kalıpları: `FB_Debounce` (sıkışma 200ms), `FB_OnDelay`, `FB_Pulse`, `FB_Blink` (lamba), `FB_RetentiveTimer` (akümülatif süre).
- **`05_opcua_symbol_publish.st`** — OPC-UA sembol yayınlama: `{attribute 'OPC.UA.DA'}` pragma'ları, salt-okunur izleme vs yazılabilir komut ayrımı, `PRG_Heartbeat` (HMI bağlantı kopması tespiti).
- **`06_alarm_handling.st`** — `FB_Alarm` (gelme/gitme/kabul latch, seviye, zaman damgası), `FB_AnalogAlarm` (histerezis + debounce), `PRG_AlarmManager` (aktif alarm sayacı + seviye özetleri).
- **`07_error_watchdog.st`** — `FB_CommWatchdog` (heartbeat timeout), `FB_TryReadStatus` (TRY benzeri durum-kodu/retry), `PRG_SafeState` (fail-safe), task watchdog yapılandırma notları.

> Not: Enum tipleri (`E_AlarmLevel` vb.) ve bazı GVL'ler (`GVL_IO`, `GVL_HMI_Cmd` ...) dosya
> başlarındaki yorumlarda gösterilmiştir; derleme öncesi kendi projenizdeki tanımlarla eşleyin.
