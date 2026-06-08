---
KONU        : PyQt/PySide ile Endüstriyel Masaüstü HMI Tasarım Desenleri
KATEGORİ    : hmi
ALT_KATEGORI: desktop
SEVİYE      : İleri
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://doc.qt.io/qt-6/qthread.html"
    başlık: "QThread Class — Qt Core 6 (Resmi Qt Dokümantasyonu)"
    güvenilirlik: resmi
  - url: "https://doc.qt.io/qt-6/threads-qobject.html"
    başlık: "Threads and QObjects — Qt 6 (Resmi Qt Dokümantasyonu)"
    güvenilirlik: resmi
  - url: "https://doc.qt.io/qtforpython-6/PySide6/QtCore/QThread.html"
    başlık: "PySide6.QtCore.QThread — Qt for Python (Resmi)"
    güvenilirlik: resmi
  - url: "https://doc.qt.io/qt-5/qtimer.html"
    başlık: "QTimer Class — Qt Core 5.15 (Resmi Qt Dokümantasyonu)"
    güvenilirlik: resmi
  - url: "https://doc.qt.io/qt-6/qtcharts-overview.html"
    başlık: "Qt Charts Overview — Qt 6 (Resmi Qt Dokümantasyonu)"
    güvenilirlik: resmi
  - url: "https://doc.qt.io/qtforpython-6/examples/example_opcua_opcuaviewer.html"
    başlık: "Qt OPC UA Viewer Example — Qt for Python (Resmi)"
    güvenilirlik: resmi
  - url: "https://realpython.com/python-pyqt-qthread/"
    başlık: "Use PyQt's QThread to Prevent Freezing GUIs — Real Python"
    güvenilirlik: topluluk
  - url: "https://www.pythonguis.com/tutorials/multithreading-pyqt6-applications-qthreadpool/"
    başlık: "PyQt6 Multithreading with QThreadPool — pythonguis.com"
    güvenilirlik: topluluk
  - url: "https://www.pythonguis.com/tutorials/multithreading-pyside6-applications-qthreadpool/"
    başlık: "Multithreading PySide6 applications with QThreadPool — pythonguis.com"
    güvenilirlik: topluluk
  - url: "https://www.pythonguis.com/tutorials/modelview-architecture/"
    başlık: "Using the PyQt5 ModelView Architecture — pythonguis.com"
    güvenilirlik: topluluk
  - url: "https://github.com/FreeOpcUa/opcua-asyncio"
    başlık: "opcua-asyncio — FreeOpcUa GitHub (asyncua kütüphanesi)"
    güvenilirlik: topluluk
  - url: "https://opcua-asyncio.readthedocs.io/en/latest/usage/get-started/minimal-client.html"
    başlık: "A Minimal OPC-UA Client — opcua-asyncio Dokümantasyonu"
    güvenilirlik: topluluk
  - url: "https://github.com/FreeOpcUa/opcua-client-gui"
    başlık: "OPC-UA GUI Client (asyncua + PyQt6 referans implementasyon) — GitHub"
    güvenilirlik: topluluk
  - url: "https://github.com/CabbageDevelopment/qasync"
    başlık: "qasync — asyncio PyQt/PySide entegrasyon kütüphanesi — GitHub"
    güvenilirlik: topluluk
  - url: "https://pypi.org/project/qasync/"
    başlık: "qasync 0.28.0 — PyPI"
    güvenilirlik: topluluk
  - url: "https://gist.github.com/dmfigol/3e7d5b84a16d076df02baa9f53271058"
    başlık: "asyncio event loop in a separate thread — GitHub Gist"
    güvenilirlik: topluluk
  - url: "https://www.pythonguis.com/tutorials/packaging-pyqt6-applications-windows-pyinstaller/"
    başlık: "How to Package PyQt6 Apps for Windows with PyInstaller — pythonguis.com"
    güvenilirlik: topluluk
  - url: "https://www.pythonguis.com/tutorials/pyqt6-plotting-pyqtgraph/"
    başlık: "PyQtGraph Tutorial — Create Interactive Plots in PyQt6 — pythonguis.com"
    güvenilirlik: topluluk
  - url: "https://www.electroniclinic.com/raspberry-pi-industrial-automation-hmi-gui-designing-using-pyqt5/"
    başlık: "Raspberry Pi Industrial Automation HMI/GUI designing using PYQT5"
    güvenilirlik: topluluk
  - url: "https://doc.qt.io/qt-6/stylesheet-examples.html"
    başlık: "Qt Style Sheets Examples — Qt Widgets 6 (Resmi)"
    güvenilirlik: resmi
BAĞLANTILAR :
  - konu: "hmi/desktop/01_opcua_clients_python"
    ilişki: gerektirir
  - konu: "hmi/architecture/02_realtime_data"
    ilişki: kullanır
  - konu: "hmi/architecture/03_alarm_management"
    ilişki: kullanır
ÖNKOŞUL     :
  - "Python 3.10+, PyQt6 veya PySide6 kurulu olmalı"
  - "asyncua (opcua-asyncio) kütüphanesi: pip install asyncua"
  - "OPC UA temel kavramları (node, subscription, data change): hmi/desktop/01_opcua_clients_python"
  - "HMI gerçek zamanlı veri yönetimi ilkeleri: hmi/architecture/02_realtime_data"
ÇELİŞKİLER :
  - kaynak: "QThread alt sınıflandırma (subclassing) yaygın eski kullanım"
    konu: "QThread doğrudan alt sınıflandırılması; run() içinde iş yapılır"
    çözüm: "Qt resmi dokümantasyonu (qt-6/qthread.html) worker-object + moveToThread() desenini öneriyor: 'A developer who wishes to invoke slots in the new thread must use the worker-object approach; new slots should not be implemented directly into a subclassed QThread.' QThread'i alt sınıflandırmak slot'ların eski thread'de çalışmasına neden olur."
  - kaynak: "qasync (tek event loop) ile QThread+asyncio (ayrı thread) yaklaşımı"
    konu: "asyncua'yı GUI'ye bağlamak için qasync (ana thread'de asyncio) vs QThread içinde ayrı asyncio loop"
    çözüm: "qasync ana thread'i temiz tutar, asyncio ve Qt event loop'u birleştirir; karmaşık polling senaryolarında QThread + asyncio.run_coroutine_threadsafe() daha fazla kontrol sağlar. İkisi birbirini dışlamaz; tercih uygulama karmaşıklığına göre değişir."
  - kaynak: "QtCharts vs PyQtGraph performans tartışması"
    konu: "Gerçek zamanlı yüksek frekanslı trend gösterimi"
    çözüm: "PyQtGraph resmi Qt dokümantasyonunun bir parçası değildir fakat Qt'nin QGraphicsScene üzerine inşa edilmiştir ve yüksek frekanslı (>10 Hz) gerçek zamanlı veri için QtCharts'tan daha performanslıdır (pythonguis.com). QtCharts daha az veri noktası olan trend ve raporlama grafikleri için yeterlidir. Resmi kaynak: ikisi için resmi karşılaştırma benchmarkı bulunamamıştır."
---

## Özün Ne

PyQt6/PySide6, endüstriyel masaüstü HMI geliştirmek için Python'da kullanılan en olgun Qt binding'leridir. Endüstriyel uygulamalarda temel zorluk şudur: PLC veya OPC UA sunucusundan sürekli veri okunurken GUI'nin donmaması ve thread-safe güncelleme yapılması gerekir. Qt'nin sinyal-slot mekanizması thread sınırlarını aşan güvenli iletişim sağlar; QThread ve asyncio entegrasyonu ise arka plan veri okumayı yönetir. Bu belge, endüstriyel gerçek zamanlı HMI için gerekli beş temel deseni kapsar: arka plan veri okuma (QThread + moveToThread), Model-View mimarisi, QTimer tabanlı polling, alarm/durum gösterimi, QtCharts/PyQtGraph ile trend görselleştirmesi ve PyInstaller ile dağıtım.

_synthesis.md'deki HMI mimari ilkeleriyle bağlantı: Bu desenler "veri katmanı" ve "donma önleme" konularının masaüstü Python implementasyonudur. OPC UA subscription tercihi (_synthesis.md: "100ms × 1000 tag polling yerine OPC UA subscription ile %70-90 trafik azalır"), ISA-101 renk kuralları ve bağlantı kopma overlay'i bu belgedeki kod örneklerine doğrudan yansımıştır.

## Nasıl Çalışır

### QThread: Worker-Object + moveToThread Deseni

Qt resmi dokümantasyonu (doc.qt.io/qt-6/qthread.html), QThread'i doğrudan alt sınıflandırmak yerine **worker-object + moveToThread()** desenini zorunlu kılmaktadır. Temel neden: QThread nesnesi kendisini **oluşturan** thread'de yaşar, yeni thread'de değil. Bu nedenle QThread alt sınıfında tanımlanan slot'lar eski thread'de çalışmaya devam eder.

```
GUI Thread (Ana Thread)          Worker Thread
───────────────────────          ─────────────────────
QThread                 →        worker.run() çalışır
worker.moveToThread()            worker'ın slot'ları burada çalışır
sinyaller bağlanır      ←←←←    worker.data_ready.emit(value)
                                 (Queued Connection ile iletilir)
```

Kaynak: Qt dokümantasyonu (qt-6/threads-qobject.html): _"It is safe to connect signals and slots across different threads, thanks to a mechanism called queued connections."_

### Bağlantı Türleri (Cross-Thread)

Kaynak: qt-6/threads-qobject.html — Qt beş bağlantı türü tanımlar:

| Bağlantı Türü | Ne Zaman Kullanılır | Davranış |
|---|---|---|
| Auto (varsayılan) | Her zaman | Aynı thread ise Direct; farklı thread ise Queued |
| Queued | Cross-thread GUI güncelleme | Slot, alıcı thread'in event loop'unda çalışır (thread-safe) |
| Direct | Aynı thread içinde | Slot anında çalışır |
| Blocking Queued | Cross-thread, sonuç beklenir | Deadlock riski — dikkatli kullanılmalı |

Endüstriyel HMI'da neredeyse her zaman **Auto** veya açık **Queued** bağlantı kullanılır.

### asyncio + QThread Entegrasyon Seçenekleri

asyncua (opcua-asyncio) tamamen async tabanlıdır. Python 3.10+ gerektirir. GUI ile entegrasyon için iki strateji vardır:

**Strateji A — qasync (Ana thread'de asyncio + Qt birleşik event loop):**
qasync, asyncio event loop'unu Qt'nin event loop'uyla birleştirir. `@asyncSlot()` decorator'ı Qt sinyallerini async fonksiyonlara bağlar. PyPI'de 0.28.0 sürümü mevcuttur (Ağustos 2025).

**Strateji B — QThread içinde ayrı asyncio loop (asyncio.run_coroutine_threadsafe):**
asyncio event loop'u daemon thread'de `loop.run_forever()` ile çalıştırılır. Coroutine'ler `asyncio.run_coroutine_threadsafe()` ile gönderilir. Sonuçlar Qt sinyalleriyle GUI thread'e iletilir.

Kaynak: GitHub Gist (dmfigol): asyncio loop daemon thread'de çalıştırılır, `run_coroutine_threadsafe` ile coroutine submit edilir.

## Pratikte Nasıl Kullanılır

### 1. Temel QThread + moveToThread Deseni (PLC Polling)

```python
# worker.py — PySide6 / PyQt6 uyumlu
from PySide6.QtCore import QObject, QThread, Signal, Slot
import time

class PlcWorker(QObject):
    """PLC'den veri okuyan arka plan worker'ı."""
    data_ready = Signal(dict)      # GUI'ye veri iletir
    connection_lost = Signal()     # Bağlantı koptu
    finished = Signal()

    def __init__(self, poll_interval_ms: int = 200):
        super().__init__()
        self._poll_interval = poll_interval_ms / 1000.0
        self._running = False

    @Slot()
    def run(self):
        """QThread.started sinyaline bağlanacak slot."""
        self._running = True
        while self._running:
            try:
                # Gerçek uygulamada: pymodbus veya diğer sync kütüphane
                data = self._read_plc()
                self.data_ready.emit(data)
            except ConnectionError:
                self.connection_lost.emit()
                break
            time.sleep(self._poll_interval)
        self.finished.emit()

    def _read_plc(self) -> dict:
        # Örnek: Modbus TCP okuma (pymodbus ile değiştirilebilir)
        return {"motor_speed": 1450.0, "temperature": 72.3, "running": True}

    @Slot()
    def stop(self):
        self._running = False


# main_window.py — Ana GUI penceresi
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._start_worker()

    def _setup_ui(self):
        self.lbl_speed = QLabel("Hız: — rpm")
        self.lbl_temp = QLabel("Sıcaklık: — °C")
        self.lbl_conn = QLabel("Bağlantı: BAĞLANIYOR")
        layout = QVBoxLayout()
        for w in [self.lbl_speed, self.lbl_temp, self.lbl_conn]:
            layout.addWidget(w)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _start_worker(self):
        self.thread = QThread()
        self.worker = PlcWorker(poll_interval_ms=200)
        # Worker'ı thread'e taşı
        self.worker.moveToThread(self.thread)
        # Sinyalleri bağla
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.data_ready.connect(self._on_data)
        self.worker.connection_lost.connect(self._on_disconnected)
        self.thread.start()

    def _on_data(self, data: dict):
        """Queued connection ile GUI thread'de çalışır — thread-safe."""
        self.lbl_speed.setText(f"Hız: {data['motor_speed']:.1f} rpm")
        self.lbl_temp.setText(f"Sıcaklık: {data['temperature']:.1f} °C")
        self.lbl_conn.setText("Bağlantı: BAĞLI")
        self.lbl_conn.setStyleSheet("color: green;")

    def _on_disconnected(self):
        self.lbl_conn.setText("Bağlantı: KESİLDİ")
        self.lbl_conn.setStyleSheet("color: red;")

    def closeEvent(self, event):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        event.accept()
```

### 2. asyncua (OPC UA) + QThread Entegrasyonu

asyncua tamamen async'tir; senkron PyQt event loop ile doğrudan çalışmaz. Aşağıdaki desen, asyncio loop'unu ayrı bir thread'de çalıştırır ve Qt sinyalleriyle GUI'ye veri iletir.

```python
import asyncio
import threading
from asyncua import Client
from PySide6.QtCore import QObject, Signal


class OpcUaWorker(QObject):
    """asyncua subscription'ı ayrı asyncio loop'ta çalıştırır."""
    tag_updated = Signal(str, object)   # (tag_path, yeni_değer)
    conn_state = Signal(str)            # "CONNECTED" | "DISCONNECTED"

    OPC_URL = "opc.tcp://192.168.1.100:4840"
    TAG_NODES = [
        "ns=2;s=Motor1.Speed",
        "ns=2;s=Motor1.Temperature",
    ]

    def __init__(self):
        super().__init__()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None

    def start(self):
        """GUI thread'den çağrılır — arka plan loop'unu başlatır."""
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run_loop, daemon=True
        )
        self._thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._opcua_task())

    async def _opcua_task(self):
        """OPC UA subscription döngüsü."""
        client = Client(url=self.OPC_URL)
        try:
            await client.connect(auto_reconnect=True, reconnect_max_delay=3.0)
            self.conn_state.emit("CONNECTED")

            # DataChange handler — asyncua callback'i
            # Kaynak: opcua-asyncio GitHub examples/client-subscription.py
            from asyncua import ua
            from asyncua.common.subscription import DataChangeEvent

            subscription = await client.create_subscription(200, None)

            # Node listesini subscribe et
            nodes = [client.get_node(t) for t in self.TAG_NODES]
            handle = await subscription.subscribe_data_change(nodes)

            # Event döngüsü
            async for event in subscription:
                if isinstance(event, DataChangeEvent):
                    tag = str(event.node)
                    value = event.value.Value.Value if event.value else None
                    # Qt sinyali ile GUI thread'e ilet (thread-safe Queued conn.)
                    self.tag_updated.emit(tag, value)
        except Exception:
            self.conn_state.emit("DISCONNECTED")
        finally:
            await client.disconnect()

    def stop(self):
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)


# GUI'de kullanım:
# worker = OpcUaWorker()
# worker.tag_updated.connect(self._on_tag_update)
# worker.conn_state.connect(self._on_conn_state)
# worker.start()
```

**Not**: asyncua'nın `client-subscription.py` örneği `async for event in subscription` desenini kullanır (opcua-asyncio GitHub, examples/client-subscription.py). Bu desen Python 3.10+ gerektirir. Subscription 500ms interval ile oluşturulur; `subscribe_data_change()` ile node listesi izlenir.

### 3. qasync ile Alternatif Entegrasyon

qasync (v0.28.0, PyPI), asyncio event loop'unu Qt'nin event loop'uyla birleştirir. `asyncio.run_coroutine_threadsafe` gerekmez; `@asyncSlot()` decorator'ı sinyalleri async fonksiyonlara bağlar.

```python
# pip install qasync asyncua
import asyncio
import sys
from qasync import QApplication, QEventLoop, asyncSlot
from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel
from asyncua import Client

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.btn = QPushButton("OPC UA Oku")
        self.lbl = QLabel("Değer: —")
        self.btn.clicked.connect(self.read_opcua)
        # ... layout setup ...

    @asyncSlot()
    async def read_opcua(self):
        """Buton tıklandığında async OPC UA okuma — GUI donmaz."""
        async with Client("opc.tcp://localhost:4840") as client:
            node = client.get_node("ns=2;s=Motor1.Speed")
            value = await node.read_value()
            self.lbl.setText(f"Hız: {value:.1f} rpm")


# Uygulama başlatma (Python 3.11+):
# asyncio.run(main(app), loop_factory=QEventLoop)
```

### 4. Model-View Mimarisi ile Gerçek Zamanlı Tag Tablosu

`QAbstractTableModel` alt sınıflandırarak veriyi GUI'den bağımsız tutar. `dataChanged` sinyali yalnızca değişen hücreyi yeniden çizer — tüm tabloyu değil. Bu özellik, çok sayıda tag'in izlendiği SCADA tablolarında kritik performans avantajı sağlar.

```python
from PySide6.QtCore import (
    QAbstractTableModel, Qt, QModelIndex, Signal
)
from PySide6.QtWidgets import QTableView
from typing import Any

HEADERS = ["Tag", "Değer", "Birim", "Durum"]

class TagTableModel(QAbstractTableModel):
    """
    OPC UA / PLC tag verilerini tutup QTableView'a sunan model.
    Kaynak: pythonguis.com modelview-architecture + doc.qt.io/qt-6/qthread.html
    """

    def __init__(self, tags: list[dict]):
        super().__init__()
        # tags: [{"name": "Motor1.Speed", "value": 0.0, "unit": "rpm", "status": "OK"}]
        self._tags = tags

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._tags)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(HEADERS)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return HEADERS[section]
        return None

    def data(self, index: QModelIndex, role=Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        tag = self._tags[row]
        if role == Qt.DisplayRole:
            return [tag["name"], f"{tag['value']:.2f}",
                    tag["unit"], tag["status"]][col]
        if role == Qt.BackgroundRole and col == 3:
            from PySide6.QtGui import QColor
            return QColor("red") if tag["status"] == "ALARM" else QColor("white")
        return None

    def update_tag(self, tag_name: str, new_value: float, status: str = "OK"):
        """Worker'ın data_ready sinyaline bağlanan slot."""
        for row, tag in enumerate(self._tags):
            if tag["name"] == tag_name:
                tag["value"] = new_value
                tag["status"] = status
                # Yalnızca değişen satırı yeniden çiz
                top_left = self.index(row, 1)
                bottom_right = self.index(row, 3)
                self.dataChanged.emit(top_left, bottom_right, [Qt.DisplayRole])
                return


# Kullanım:
# tags = [{"name": "Motor1.Speed", "value": 0.0, "unit": "rpm", "status": "OK"}]
# model = TagTableModel(tags)
# view = QTableView()
# view.setModel(model)
# worker.data_ready.connect(lambda d: model.update_tag("Motor1.Speed", d["motor_speed"]))
```

### 5. QTimer ile Periyodik Polling

QTimer, Qt event loop'u içinde periyodik görev zamanlamak için kullanılır. Kaynak: doc.qt.io/qt-5/qtimer.html — `start(msec)`, `stop()`, `timeout` sinyali.

**Önemli kural**: QTimer'ın `timeout` sinyali GUI thread'de çalışır. Bu sinyale bağlanan slot'lar ağır iş (IO, PLC okuma) yapmamalıdır — aksi takdirde GUI donar. Hafif UI güncelleme için (görsel yenileme, stale data kontrolü) doğrudan kullanılabilir. Ağır iş için QThread tercih edilmelidir.

```python
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow

class DashboardWindow(QMainWindow):
    STALE_TIMEOUT_MS = 5000   # 5 saniye veri gelmezse "bayat" say

    def __init__(self):
        super().__init__()
        self._last_update_ms = 0
        # Stale data kontrolü — hafif, GUI thread'de çalışabilir
        self._stale_timer = QTimer(self)
        self._stale_timer.setInterval(1000)    # Her 1 saniyede kontrol et
        self._stale_timer.timeout.connect(self._check_stale)
        self._stale_timer.start()

        # UI animasyon/görsel yenileme timer'ı (ör: alarm yanıp sönme)
        self._blink_timer = QTimer(self)
        self._blink_timer.setInterval(500)     # 500ms
        self._blink_timer.timeout.connect(self._toggle_alarm_blink)
        self._alarm_blink_state = False

    def _check_stale(self):
        """Son veri gelişinden bu yana geçen süreyi kontrol et."""
        from PySide6.QtCore import QDateTime
        now = QDateTime.currentMSecsSinceEpoch()
        if (now - self._last_update_ms) > self.STALE_TIMEOUT_MS:
            self._show_stale_overlay(True)
        else:
            self._show_stale_overlay(False)

    def _show_stale_overlay(self, stale: bool):
        # _synthesis.md bağlantı kopma ilkesi: veri bayatsa gri/italik gösterim
        style = "color: gray; font-style: italic;" if stale else ""
        # tüm değer label'larına uygula
        pass

    def _toggle_alarm_blink(self):
        self._alarm_blink_state = not self._alarm_blink_state
        # Aktif onaylanmamış alarm varsa yanıp sönsün
        pass

    def on_data_received(self, data: dict):
        """Worker sinyaline bağlı — veri gelince timestamp güncelle."""
        from PySide6.QtCore import QDateTime
        self._last_update_ms = QDateTime.currentMSecsSinceEpoch()
        # Değerleri güncelle...
```

### 6. Alarm / Durum Gösterimi

ISA-101 renk kuralları (_synthesis.md Tablo B) QSS ile uygulanır. Kaynak: doc.qt.io/qt-6/stylesheet-examples.html — `setStyleSheet()` dinamik olarak çağrılabilir.

```python
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from enum import Enum

class AlarmPriority(Enum):
    NORMAL   = "NORMAL"
    LOW      = "LOW"        # Mavi
    MEDIUM   = "MEDIUM"     # Sarı
    HIGH     = "HIGH"       # Turuncu
    CRITICAL = "CRITICAL"   # Kırmızı

# ISA-101 renk haritası (_synthesis.md Tablo B'ye uygun)
ALARM_STYLES = {
    AlarmPriority.NORMAL:   "background-color: #d0d0d0; color: #000;",          # Gri
    AlarmPriority.LOW:      "background-color: #1565C0; color: #fff;",           # Mavi
    AlarmPriority.MEDIUM:   "background-color: #F9A825; color: #000;",           # Sarı
    AlarmPriority.HIGH:     "background-color: #E65100; color: #fff;",           # Turuncu
    AlarmPriority.CRITICAL: "background-color: #B71C1C; color: #fff; font-weight: bold;",  # Kırmızı
}

class AlarmBanner(QWidget):
    """
    ISA-18.2 uyumlu alarm banner widget'ı.
    Onaylanmamış kritik alarmlar için yanıp söner.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._label = QLabel("Sistem Normal")
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setMinimumHeight(40)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._label)
        self._blink_state = False
        self._current_priority = AlarmPriority.NORMAL

    def set_alarm(self, message: str, priority: AlarmPriority):
        """Alarm durumunu güncelle."""
        self._current_priority = priority
        self._label.setText(message)
        self._label.setStyleSheet(ALARM_STYLES[priority])

    def clear(self):
        self._current_priority = AlarmPriority.NORMAL
        self._label.setText("Sistem Normal")
        self._label.setStyleSheet(ALARM_STYLES[AlarmPriority.NORMAL])

    def blink_tick(self):
        """QTimer.timeout sinyaline bağlanarak yanıp sönen görünüm sağlar."""
        if self._current_priority == AlarmPriority.CRITICAL:
            self._blink_state = not self._blink_state
            if self._blink_state:
                self._label.setStyleSheet(ALARM_STYLES[AlarmPriority.CRITICAL])
            else:
                self._label.setStyleSheet("background-color: #fff; color: #B71C1C; font-weight: bold;")


class MotorStatusWidget(QWidget):
    """
    Tek motor için durum göstergesi — ISA-101 renk kuralları.
    Normal: gri; Çalışıyor: yeşil; Arıza: kırmızı.
    Kaynak: stylesheets + HMI architecture/_synthesis.md
    """
    STATUS_STYLES = {
        "STOPPED":     "background-color: #9E9E9E; color: #fff; border-radius: 4px; padding: 4px;",
        "RUNNING":     "background-color: #388E3C; color: #fff; border-radius: 4px; padding: 4px;",
        "FAULT":       "background-color: #B71C1C; color: #fff; border-radius: 4px; padding: 4px; font-weight: bold;",
        "MAINTENANCE": "background-color: #F57F17; color: #fff; border-radius: 4px; padding: 4px;",
        "STALE":       "background-color: #9E9E9E; color: #fff; border-radius: 4px; padding: 4px; font-style: italic;",
    }

    def __init__(self, motor_name: str, parent=None):
        super().__init__(parent)
        self._label = QLabel(f"{motor_name}: STOPPED")
        self._label.setAlignment(Qt.AlignCenter)
        layout = QHBoxLayout(self)
        layout.addWidget(self._label)
        self.set_status("STOPPED")

    def set_status(self, status: str, speed: float | None = None):
        text = self._label.text().split(":")[0]  # motor adını koru
        display = f"{text}: {status}"
        if speed is not None and status == "RUNNING":
            display += f" ({speed:.0f} rpm)"
        self._label.setText(display)
        self._label.setStyleSheet(self.STATUS_STYLES.get(status, ""))
```

### 7. QtCharts ile Gerçek Zamanlı Trend Grafiği

QtCharts modülü PySide6 ile birlikte gelir (lisans: GPL/LGPL). `QLineSeries`, `QChart`, `QChartView`, `QValueAxis` temel sınıflardır. Kaynak: doc.qt.io/qt-6/qtcharts-overview.html.

**Önemli**: Gerçek zamanlı yüksek frekanslı veri (>5 Hz) için **PyQtGraph** daha performanslıdır (pythonguis.com). QtCharts; düşük frekanslı trend, raporlama ve geçmiş veri görüntüleme için uygundur.

```python
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from collections import deque
import time

MAX_POINTS = 300    # Ekranda tutulacak maksimum nokta (kayan pencere)


class TrendWidget(QWidget):
    """
    Gerçek zamanlı sliding-window trend grafiği.
    Kaynak: doc.qt.io/qt-6/qtcharts-overview.html + Medium PyQt5 oscilloscope article
    """

    def __init__(self, title: str = "Trend", y_min=0.0, y_max=100.0,
                 y_label="Değer", parent=None):
        super().__init__(parent)
        self._series = QLineSeries()
        self._chart = QChart()
        self._chart.addSeries(self._series)
        self._chart.setTitle(title)
        self._chart.legend().hide()

        # X ekseni: zaman (saniye cinsinden göreceli)
        self._axis_x = QValueAxis()
        self._axis_x.setRange(0, MAX_POINTS / 5)  # Başlangıç aralığı
        self._axis_x.setTitleText("Zaman (s)")

        # Y ekseni
        self._axis_y = QValueAxis()
        self._axis_y.setRange(y_min, y_max)
        self._axis_y.setTitleText(y_label)

        self._chart.addAxis(self._axis_x, Qt.AlignBottom)
        self._chart.addAxis(self._axis_y, Qt.AlignLeft)
        self._series.attachAxis(self._axis_x)
        self._series.attachAxis(self._axis_y)

        self._view = QChartView(self._chart)
        layout = QVBoxLayout(self)
        layout.addWidget(self._view)

        # Kayan pencere için veri buffer'ı
        self._buffer: deque[tuple[float, float]] = deque(maxlen=MAX_POINTS)
        self._start_time = time.monotonic()

    def append(self, value: float):
        """Yeni veri noktası ekle — worker'ın data_ready sinyaline bağlanabilir."""
        t = time.monotonic() - self._start_time
        self._buffer.append((t, value))
        self._refresh()

    def _refresh(self):
        """Seriyi tamamen yeniden çiz (kayan pencere)."""
        self._series.clear()
        for t, v in self._buffer:
            self._series.append(t, v)
        # X eksenini kayar pencereye göre ayarla
        if self._buffer:
            t_max = self._buffer[-1][0]
            window = MAX_POINTS / 5  # 5 Hz varsayımı
            self._axis_x.setRange(max(0.0, t_max - window), t_max)


# PyQtGraph alternatifi — yüksek frekans için (>5 Hz):
# pip install pyqtgraph
# import pyqtgraph as pg
# plot_widget = pg.PlotWidget()
# line = plot_widget.plot([], [], pen='y')
# # Güncelleme (QTimer veya signal bağlantısı):
# line.setData(time_array, value_array)
```

### 8. PyInstaller ile Dağıtım

Kaynak: pythonguis.com/tutorials/packaging-pyqt6-applications-windows-pyinstaller

```bash
# 1. Gerekli paketler
pip install pyinstaller
pip install --upgrade PyInstaller pyinstaller-hooks-contrib

# 2. Tek klasör çıktısı (tavsiye edilen — plugin sorunlarını azaltır)
pyinstaller --windowed --name "IndustrialHMI" main.py

# 3. Uygulamaya özel ikon ekle
pyinstaller --windowed --icon=hmi.ico --name "IndustrialHMI" main.py

# 4. Tek dosya (--onefile) — başlatma daha yavaş, plugin sorunları yaygın
pyinstaller --onefile --windowed main.py

# 5. Veri dosyaları ekle (QSS, ikonlar, config)
pyinstaller --windowed --add-data "resources;resources" --name "IndustrialHMI" main.py

# 6. Spec dosyası oluşturulduktan sonra yeniden derleme
pyinstaller app.spec
```

**Spec dosyasında asyncua için hidden imports:**

```python
# app.spec — Analysis bloğu içinde
a = Analysis(
    ['main.py'],
    hiddenimports=[
        'asyncua',
        'asyncua.common',
        'asyncua.client',
        'asyncua.crypto',
        'cryptography',
    ],
    datas=[('resources', 'resources')],
)
```

**Windows görev çubuğu entegrasyonu (endüstriyel uygulama kimliği):**

```python
# main.py başına ekle
try:
    from ctypes import windll
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        'com.sirket.industrial-hmi.1.0'
    )
except ImportError:
    pass
```

**Önemli uyarı**: PyInstaller çıktısı her zaman hedef işletim sisteminde derlenmelidir. "You always need to compile your app on your target system." (pythonguis.com)

## Örnekler

### Tam OPC UA → QThread → Model-View Entegrasyon Akışı

```
┌─────────────────────────────────────────────────────────────┐
│                   ENDÜSTRİYEL MASAÜSTÜ HMI                  │
│                                                              │
│  OPC UA Sunucu          Worker Thread           GUI Thread   │
│  (PLC/CODESYS)                                              │
│                                                              │
│  asyncua Client  ──►  asyncio loop          ┌──────────────┐│
│  subscription         daemon thread         │  MainWindow  ││
│  500ms interval  ──►  tag_updated.emit() ──►│  TagTable    ││
│                                             │  TrendWidget ││
│                       conn_state.emit()  ──►│  AlarmBanner ││
│                                             │  StatusWidget││
│  (auto_reconnect=True                       └──────────────┘│
│   reconnect_max_delay=3.0)                                  │
└─────────────────────────────────────────────────────────────┘
```

### Bağlantı Kopma Senaryosu (ISA-101 + _synthesis.md uyumu)

```python
class ConnectionManager(QObject):
    """
    _synthesis.md Tablo G: Bağlantı durumu gösterim kuralları.
    CONNECTED → DISCONNECTED → CONNECTING döngüsü.
    """

    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window

    def on_connected(self):
        self.mw.status_bar.showMessage("PLC: BAĞLI", 0)
        self.mw.status_bar.setStyleSheet("background-color: #388E3C; color: #fff;")
        # Yazma butonlarını aktif et
        for btn in self.mw.write_buttons:
            btn.setEnabled(True)

    def on_disconnected(self):
        # _synthesis.md: "Bağlantı kopunca değerler gri + uyarı overlay,
        # tüm yazma butonları devre dışı"
        self.mw.status_bar.showMessage("PLC BAĞLANTISI KESİLDİ — Yeniden bağlanılıyor...", 0)
        self.mw.status_bar.setStyleSheet("background-color: #B71C1C; color: #fff;")
        # Tüm değer label'larını gri yap
        for lbl in self.mw.value_labels:
            lbl.setStyleSheet("color: gray; font-style: italic;")
        # Yazma butonlarını devre dışı bırak
        for btn in self.mw.write_buttons:
            btn.setEnabled(False)
```

## Sık Yapılan Hatalar

### 1. GUI Thread'de IO Yapmak (En Kritik Hata)

```python
# YANLIŞ — GUI donar
def on_read_button_clicked(self):
    value = plc.read_register(100)   # Ağ IO → GUI thread bloke
    self.label.setText(str(value))

# DOĞRU — Worker'a komut gönder
def on_read_button_clicked(self):
    self.read_requested.emit(100)    # Sinyal ile worker'a ilet
```

Kaynak: realpython.com/python-pyqt-qthread/: _"If you launch a long-running task in the GUI thread, then your GUI will freeze until the task terminates."_

### 2. QThread'i Alt Sınıflandırıp run() İçinde Slot Tanımlamak

```python
# YANLIŞ — Slot'lar eski thread'de çalışır
class MyThread(QThread):
    def run(self):
        self._do_work()

    def update_config(self, v):     # Bu slot eski thread'de çalışır!
        self._config = v

# DOĞRU — Worker object + moveToThread
class MyWorker(QObject):
    def run(self):       # slot olarak bağlanır
        self._do_work()

    def update_config(self, v):     # Bu slot worker thread'de çalışır
        self._config = v
```

Kaynak: doc.qt.io/qt-6/qthread.html: _"A developer who wishes to invoke slots in the new thread must use the worker-object approach."_

### 3. Worker Thread'den Doğrudan GUI Widget Güncellemesi

```python
# YANLIŞ — Thread-unsafe, crash riski
class Worker(QObject):
    def run(self):
        self.main_window.label.setText("yeni değer")  # YASAK

# DOĞRU — Sinyal ile ilet
class Worker(QObject):
    value_changed = Signal(str)

    def run(self):
        self.value_changed.emit("yeni değer")   # GUI thread alır
```

Kaynak: qt-6/threads-qobject.html: QObject thread-safe değildir; farklı thread'den erişim mutex veya sinyal gerektirir.

### 4. asyncio Coroutine'i GUI Thread'de Çalıştırmak

```python
# YANLIŞ — Event loop yok veya Qt loop'unu engeller
async def read():
    async with Client("opc.tcp://...") as c:
        return await c.get_node("ns=2;s=Tag").read_value()

asyncio.run(read())   # Qt uygulaması içinde çalışmaz veya bloke eder

# DOĞRU — Seçenek A: asyncio.run_coroutine_threadsafe
asyncio.run_coroutine_threadsafe(read(), self._background_loop)

# DOĞRU — Seçenek B: qasync @asyncSlot()
@asyncSlot()
async def on_button():
    value = await read()
```

### 5. PyInstaller'da asyncua/cryptography Hidden Import Eksikliği

asyncua, `cryptography` ve alt modüllerini dinamik olarak import eder. PyInstaller bunu tespit edemez. Spec dosyasına açıkça `hiddenimports` eklenmelidir (bkz. Dağıtım bölümü).

### 6. QTimer'ı Worker Thread'de Oluşturmak

```python
# YANLIŞ — QTimer sahibi thread'in event loop'una ihtiyaç duyar
class Worker(QObject):
    def run(self):
        self.timer = QTimer()   # Hata: thread event loop'u yok (run_forever çağrılmadı)
        self.timer.start(100)

# DOĞRU — QTimer GUI thread'de oluşturulur veya worker thread'e moveToThread ile taşınır
# Genellikle QTimer GUI thread'de tutulur ve data_ready sinyali ile stale kontrolü yapılır
```

Kaynak: qt-6/threads-qobject.html: _"Event-driven objects (timers, sockets) can only be used in a single thread."_

### 7. Stale Data Göstermemek

_synthesis.md Sentez Notu 3'ten: Gerçek proje vakası — bağlantı 20 dakika önce kesilmiş, ekran 68°C gösteriyordu, motor 92°C'ye ulaşmıştı. Stale data overlay **ilk günden** tasarlanmalı. QTimer ile son veri zamanı kontrol edilip değerler gri/italik yapılmalıdır (bkz. QTimer örneği, `_check_stale` metodu).

## Ne Zaman Tercih Edilmeli / Edilmemeli

### PyQt6/PySide6 Masaüstü HMI — Ne Zaman Uygun?

**Tercih et:**
- Operatör paneli, kurulum istasyonu, makine başı terminal
- ISA-101 uyumlu özelleşmiş widget gereksinimleri
- Offline çalışma zorunluluğu (web bağlantısı yok)
- Var olan Python PLC kütüphaneleriyle (pymodbus, asyncua) doğrudan entegrasyon
- Linux/Windows gömülü panel bilgisayarlar (Raspberry Pi, x86 IPC)
- Sıfır lisans maliyeti gerekliliği

**Tercih etme:**
- 50+ eş zamanlı kullanıcı, uzak izleme — Web HMI (React + WebSocket) daha uygun
- Büyük ölçekli tesis, hızlı geliştirme — SCADA platform (Ignition, WinCC) historian/alarm'ı hazır sunar
- Mobil/tablet erişimi öncelikli — web tabanlı veya native mobil uygulama

### asyncua (async) vs Senkron OPC UA Kütüphane

| | asyncua (opcua-asyncio) | opcua (eski, sync) |
|---|---|---|
| Python sürümü | ≥ 3.10 | 2.7–3.x |
| API | async/await | Senkron |
| PyQt entegrasyon | qasync veya QThread+asyncio | Doğrudan QThread |
| Bakım | Aktif (2025) | Pasif |
| Tavsiye | Yeni projeler | Eski projeler |

### QtCharts vs PyQtGraph

| Kriter | QtCharts | PyQtGraph |
|---|---|---|
| PySide6 ile uyum | Dahili, resmi | Üçüncü parti (Qt native) |
| Lisans | GPL/LGPL (resmi Qt) | MIT |
| Yüksek frekans (>5 Hz) | Performans sorunları olabilir | Üstün (QGraphicsScene native) |
| Düşük frekans trend/rapor | Yeterli, şık görünüm | Kullanılabilir |
| 3D grafik | Hayır | Evet (pyqtgraph.opengl) |

## Gerçek Proje Notları

**Not 1 — moveToThread Unutulunca:**
Bir projede `QThread`'i doğrudan alt sınıflandırıp slot eklenmiş, config güncelleme sinyali bağlanmıştı. Config'in değişmediği fark edildiğinde `moveToThread()` eksikliği anlaşıldı — slot eski thread'de çalışıyordu. Qt dokümantasyonu bu konuda nettir (qt-6/qthread.html).

**Not 2 — asyncua reconnect otomatik değil (eski versiyonlar):**
asyncua'nın eski sürümlerinde `auto_reconnect` parametresi yoktu. Yeni sürümlerde (0.9.x+) `Client(url=..., auto_reconnect=True, reconnect_max_delay=3.0)` ile otomatik yeniden bağlanma desteklenir (kaynak: opcua-asyncio GitHub examples/client-subscription.py).

**Not 3 — QLineSeries.clear() + yeniden append performansı:**
Çok noktalı (>1000) gerçek zamanlı güncelleme için `clear()` + `append()` döngüsü yavaş kalabilir. `replace()` ile tüm seriyi tek seferde değiştirmek veya PyQtGraph'a geçmek daha iyi sonuç verir.

**Not 4 — PySide6 vs PyQt6 seçimi:**
Her ikisi de aynı Qt API'sini sarıyor. PySide6 LGPL lisanslı (ticari proje için ücretsiz); PyQt6 GPL/Ticari lisanslı. Kapalı kaynak ticari proje için **PySide6 tercih edilmeli**. Kaynak: riverbankcomputing.com (PyQt lisans) ve doc.qt.io/qtforpython-6 (PySide6).

**Not 5 — PyInstaller tek dosya (--onefile) endüstriyel uygulamalarda sorunlu:**
`--onefile` her başlatmada geçici dizine extract eder; yavaş başlatma + antivirüs false positive riski. Endüstriyel panel bilgisayarlarda `--onedir` (varsayılan) tercih edilmeli, SMB/USB'den çalıştırılmamalı.

**Not 6 — QTimer minimum çözünürlüğü:**
Windows'ta QTimer minimum interval ~15ms'dir (platform timer çözünürlüğü). 1ms'den kısa interval istenmemeli. Kritik zamanlama için QThread içinde `time.sleep()` veya platform-spesifik timer kullanılmalı.

## İlgili Konular

```
knowledge/hmi/desktop/
├── 01_opcua_clients_python.md    → asyncua client kurulum, node okuma, subscription temelleri
├── 02_opcua_clients_dotnet.md    → .NET OPC UA alternatifleri
└── 03_pyqt_patterns.md           ← Bu belge

knowledge/hmi/architecture/
├── 02_realtime_data.md           → OPC UA subscription stratejileri, stale data, bağlantı yönetimi
├── 03_alarm_management.md        → ISA-18.2 alarm durum makinesi, flood önleme
└── _synthesis.md                 → Tüm HMI katmanlarını birleştiren sentez

Dış kaynaklar:
  doc.qt.io/qt-6/qthread.html              → QThread resmi API
  doc.qt.io/qtforpython-6/                 → PySide6 resmi dokümantasyon
  opcua-asyncio.readthedocs.io             → asyncua kütüphane dokümantasyonu
  pypi.org/project/qasync/                 → qasync 0.28.0
  pyqtgraph.org                            → Yüksek performanslı Qt plot kütüphanesi
  pyinstaller.org                          → PyInstaller resmi dokümantasyon
```
