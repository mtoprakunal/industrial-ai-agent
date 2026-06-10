// ============================================================================
//  App.jsx — Konveyor HMI ana ekran
// ============================================================================
//  3 bolgeli konveyor (EXAMPLE_conveyor io_list mantigi):
//    DI -> discrete input (buton/sensor/secici)
//    DO -> coil (motor/lamba/korna)
//    AI -> input register (takometre hizi)
//    HR -> holding register (hiz setpoint)
// ============================================================================

import { useWebSocket } from "./hooks/useWebSocket.js";
import { ConnectionBanner } from "./components/ConnectionBanner.jsx";
import { BoolIndicator } from "./components/BoolIndicator.jsx";
import { AnalogDisplay } from "./components/AnalogDisplay.jsx";
import { CoilControl } from "./components/CoilControl.jsx";
import { SetpointControl } from "./components/SetpointControl.jsx";
import { AlarmPanel } from "./components/AlarmPanel.jsx";

const ZONES = [1, 2, 3];

export default function App() {
  // WebSocket baglantisini App seviyesinde TEK kez kur (singleton).
  useWebSocket();

  return (
    <div className="hmi-app">
      <ConnectionBanner />

      <header className="hmi-header">
        <h1>Konveyor Hatti — HMI (Modbus TCP)</h1>
      </header>

      <AlarmPanel />

      {/* Tesis geneli durum */}
      <section className="panel">
        <h2>Tesis Durumu</h2>
        <div className="grid">
          <BoolIndicator tag="estop_ok" onLabel="SAGLAM" offLabel="DEVREDE" />
          <BoolIndicator tag="permit_run" onLabel="VAR" offLabel="YOK" />
          <BoolIndicator tag="reset_pb" onLabel="BASILI" offLabel="SERBEST" />
        </div>
        <div className="grid">
          <CoilControl tag="beacon_run" />
          <CoilControl tag="beacon_fault" />
          <CoilControl tag="horn_alarm" />
        </div>
      </section>

      {/* Her bolge icin durum + hiz + kontrol */}
      {ZONES.map((z) => (
        <section className="panel" key={z}>
          <h2>Bolge {z}</h2>

          <div className="grid">
            <BoolIndicator tag={`zn${z}_sel_auto`} onLabel="OTO" offLabel="MANUEL" />
            <BoolIndicator tag={`zn${z}_pb_start`} onLabel="BASILI" offLabel="-" />
            <BoolIndicator tag={`zn${z}_pb_stop`} onLabel="BASILI" offLabel="-" />
            <BoolIndicator tag={`zn${z}_present`} onLabel="VAR" offLabel="YOK" />
            <BoolIndicator tag={`zn${z}_jam`} onLabel="SIKISMA" offLabel="NORMAL" />
          </div>

          <div className="grid">
            <AnalogDisplay
              tag={`zn${z}_speed`}
              min={0}
              max={120}
              alarmHigh={110}
              decimals={1}
            />
            <SetpointControl tag={`zn${z}_speed_sp`} />
          </div>

          <div className="grid">
            <CoilControl tag={`zn${z}_motor_run`} />
            <CoilControl tag={`zn${z}_lamp_run`} />
            <CoilControl tag={`zn${z}_lamp_fault`} />
          </div>
        </section>
      ))}
    </div>
  );
}
