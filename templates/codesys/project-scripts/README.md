# CODESYS Script Engine Şablonları

Bu klasör, CODESYS Script Engine (IronPython) ile
projeyi otomatik dolduran Python scriptlerini içerir.

Tüm scriptler **IronPython 2.7** uyumludur (`from __future__ import print_function`,
`.format()`, `codecs` ile utf-8 I/O). Python 3'e özgü f-string / walrus / type-hint
kullanılmaz.

## Nasıl Kullanılır
1. CODESYS'te yeni boş proje aç (PLC cihazı + Application hazır olmalı)
2. Tools > Scripting > Execute Script File
3. İlgili scripti seç
4. Script projeyi otomatik yapılandırır

Tüm scriptler **idempotent**'tir: var olan nesneyi bulup günceller, yoksa oluşturur;
kısmi hata sonrası yeniden çalıştırılabilir. Her script sonunda `proj.compile()` ile
doğrulama yapar (script "tamamlandı" demesi yeterli değil — derleme sonucu esastır).

## Mevcut Scriptler

### `create_basic_structure.py`
Boş projede temel iskeleti kurar:
- Task konfigürasyonu: `Task_Fast` (2ms, Prio 1), `Task_Control` (10ms, Prio 5),
  `Task_Slow` (100ms, Prio 10)
- `GVL_IO` (I/O iskeleti), `GVL_Const` (VAR_GLOBAL CONSTANT)
- `MAIN` (PROGRAM PRG, kontrol döngüsü iskeleti), Task_Control'e bağlanır

Task API'si sürüme göre değişir; `create_task` / `set_interval` yoksa kullanıcıya
manuel adım önerilir.

### `add_opcua_server.py`
Yerleşik OPC UA sunucusu için yayını kurar:
- Application altında **Symbol Configuration** nesnesi (yoksa oluşturur)
- Seçili GVL'leri yayına alır (varsayılan: `GVL_HMI` readwrite, `GVL_Diagnostics`
  read) — GVL deklarasyonuna `{attribute 'symbol := 'readwrite''}` pragması enjekte
  ederek. Tüm değişkenler değil, yalnız seçili GVL'ler açılır (saldırı yüzeyi + bootapp).

NodeId formatı: `ns=4;s=|var|<RuntimeName>.Application.GVL_HMI.<Tag>`.
SP17+ runtime'da anonymous kapalı; client'ta kullanıcı/şifre veya
`AllowAnonymous=1` gerekir (runtime tarafı, scriptlenmez).

### `add_modbus_slave.py`
Modbus TCP Slave ekler + register haritalar (io_list mantığı):
- Ethernet arayüzü altına **ModbusTCP Slave Device** (DeviceID sürüme/repo'ya bağlı —
  guard'lı; başarısız olursa GVL yine üretilir)
- io_list `Yon` → Modbus alanı eşlemesi:
  `DO→Coil`, `DI→Discrete Input`, `AO→Holding Register`, `AI→Input Register`
- `GVL_Modbus` üretir + offset'leri içeren register haritası dökümanı yazar

CSV→register/GVL üretim mantığı saf fonksiyondadır; standalone test:
```bash
python add_modbus_slave.py ../../../projects/EXAMPLE_conveyor/io_list.csv
```

### `generate_gvl_from_io.py`
Bir `io_list.csv` (`Tag,Adres,Tip,Yon,Task,Aciklama,Olcek_Not`) okur ve hizalanmış,
DI/DO/AI/AO kategorilerine ayrılmış `GVL_IO` ST içeriği üretir. **İki modlu**:
- **Standalone** (CPython/IronPython, CODESYS gerekmez) — CSV→ST mantığı
  `build_gvl_declaration()` saf fonksiyonundadır, test edilebilir:
  ```bash
  python generate_gvl_from_io.py io_list.csv [cikti.st]
  ```
- **CODESYS içinde** — açık projede `GVL_IO` bulur/oluşturur, içeriği yazar.

CSV→ST üretim mantığı saf fonksiyonda olduğundan `add_modbus_slave.py` de aynı CSV
ayrıştırıcıyı yeniden kullanır.
