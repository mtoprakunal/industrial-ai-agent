# PLCopen XML Şablonları

IEC 61131-10 standardına uygun PLCopen XML şablonları.
CODESYS'e doğrudan import edilebilir.

Şema sürümü: PLCopen XML v2.01 (`xmlns="http://www.plcopen.org/xml/tc6_0201"`).
ST gövdeleri `<body><ST><xhtml><![CDATA[...]]></xhtml></ST></body>` içinde taşınır.

## İçe Aktarma
File > Import > PLCopen XML > ilgili `.xml` dosyasını seç > hedef: Application.

İçe aktarma sonrası kontrol:
- `FB_MotorControl` standart `RS` blokunu, `FB_AlarmHandler` standart `R_TRIG` blokunu kullanır.
  Bunlar Standard kütüphanesinden gelir; eksikse Library Manager'dan ekle.
- AT %I/%Q adresleri ve I/O mapping taşınmaz; cihaz ağacında yeniden eşle.

## Mevcut Şablonlar
- `basic_program.xml`      — Temel PRG (pouType=program). Yerel değişkenler (xRun:BOOL,
  iCounter:INT, rValue:REAL) ve sayaç + ölçekleme örneği içeren ST gövdesi.
- `motor_control_fb.xml`   — `FB_MotorControl`. VAR_INPUT: xStart, xStop, xInterlock;
  VAR_OUTPUT: xRun, xFault; VAR: RS mandalı. Stop ve interlock kaybı önceliklidir.
- `analog_scaling_fb.xml`  — `FB_AnalogScale`. 4-20mA lineer ölçekleme, under-range
  (kablo kopması / NAMUR NE107) ve over-range tespiti, sıfıra bölme koruması + clamp.
- `alarm_handler_fb.xml`   — `FB_AlarmHandler`. Yükselen kenarda alarm latch + seviye saklama,
  acknowledge ile temizleme (yalnız koşul düştüyse), aktif/mandallı/kabul-bekliyor çıkışları.

## Doğrulama
Tüm dosyalar well-formed XML olarak doğrulandı:
```
python3 -c "import xml.dom.minidom; xml.dom.minidom.parse('DOSYA.xml')"
```
