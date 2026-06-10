// ============================================================
// App.jsx — Ana HMI ekranı
// ------------------------------------------------------------
// EXAMPLE_conveyor: 3 bölgeli konveyör.
// WebSocket bağlantısı burada (singleton) bir kez kurulur.
// ============================================================

import { useOpcUa } from './hooks/useOpcUa.js';
import { ConnectionStatus } from './components/ConnectionStatus.jsx';
import { AlarmPanel } from './components/AlarmPanel.jsx';
import { ZonePanel } from './components/ZonePanel.jsx';
import { TagValue } from './components/TagValue.jsx';
import { CommandButton } from './components/CommandButton.jsx';

export default function App() {
    // Singleton WebSocket bağlantısını kur (gateway'e)
    useOpcUa();

    return (
        <div className="hmi-app">
            <header className="hmi-header">
                <h1>Konveyör Hattı — Web HMI (OPC-UA)</h1>
                <ConnectionStatus />
            </header>

            <main className="hmi-main">
                <section className="alarm-section">
                    <AlarmPanel />
                </section>

                <section className="overview-section">
                    <h2>Genel Durum</h2>
                    <div className="overview-tags">
                        {/* xEStopActive: true = E-Stop basılı (kötü). Burada bilgi amaçlı. */}
                        <TagValue tag="xEStopActive" label="E-Stop" decimals={0} />
                        <TagValue tag="xRunPermit" label="Çalışma İzni" decimals={0} />
                        <TagValue tag="xAnyAlarm" label="Genel Alarm" decimals={0} />
                    </div>
                </section>

                <section className="zones-section">
                    <h2>Bölgeler</h2>
                    <div className="zones-grid">
                        <ZonePanel zone={1} />
                        <ZonePanel zone={2} />
                        <ZonePanel zone={3} />
                    </div>
                </section>

                <section className="global-cmd-section">
                    <h2>Komutlar</h2>
                    <div className="global-cmd-row">
                        {/* xCmdReset -> HMI'dan reset; PLC tarafında PLT_RST ile OR'lanır */}
                        <CommandButton writeTag="cmdReset" label="Reset" value={true} momentary />
                    </div>
                    <p className="cmd-hint">
                        Komutlar yalnız OTO modda geçerlidir; manuel modda saha butonları önceliklidir.
                    </p>
                </section>
            </main>
        </div>
    );
}
