// ============================================================
// config.js — Gateway konfigürasyonu ve TAG HARİTASI
// ------------------------------------------------------------
// .env değerlerini okur ve EXAMPLE_conveyor projesinin
// OPC-UA değişkenlerini somut tag tanımlarına çevirir.
//
// node-opcua API notları (knowledge/hmi/web-based/01_opcua_clients_js.md):
//  - NodeId formatı CODESYS için: ns=<idx>;s=|var|<RuntimeAdı>.Application.<GVL>.<Değişken>
//  - namespace index ÇALIŞMA ZAMANINDA getNamespaceIndex(URI) ile alınır (Hata 2).
//    Bu yüzden buradaki nodeId'lerde ns yerine `{ns}` yer tutucusu kullanılır;
//    server.js bağlantı kurulunca gerçek index ile doldurur.
// ============================================================

import 'dotenv/config';

// --- Çevre değişkenleri (varsayılanlarla) ---
export const config = {
    opcua: {
        endpoint: process.env.OPCUA_ENDPOINT || 'opc.tcp://192.168.1.100:4840',
        namespaceUri: process.env.OPCUA_NAMESPACE_URI || 'http://www.3s-software.com/schemas/Codesys-V3',
        user: process.env.OPCUA_USER || '',
        pass: process.env.OPCUA_PASS || '',
        securityMode: process.env.OPCUA_SECURITY_MODE || 'None',
        securityPolicy: process.env.OPCUA_SECURITY_POLICY || 'None',
    },
    ws: {
        port: parseInt(process.env.WS_PORT || '8080', 10),
        writeAuthToken: process.env.WRITE_AUTH_TOKEN || '',
    },
    batchIntervalMs: parseInt(process.env.BATCH_INTERVAL_MS || '100', 10),
    reconnectDelayMs: 5000,
};

// CODESYS runtime'da Application altındaki tam yol öneki.
// PLC projenizdeki gerçek runtime/uygulama adına göre düzenleyin.
const APP = 'CODESYS Control.Application';

// ------------------------------------------------------------
// TAG HARİTASI — EXAMPLE_conveyor / GVL_HMI değişkenleri
// ------------------------------------------------------------
// path : `{ns}` yer tutuculu NodeId (server.js doldurur)
// dir  : 'r' (PLC->HMI salt okunur) | 'rw' (HMI->PLC yazılabilir komut)
// dataType: yalnız yazılabilir tag'ler için zorunlu — yazma sırasında
//           Bad_TypeMismatch'i önler (01_opcua_clients_js.md Not 6).
//           CODESYS BOOL->Boolean, REAL->Float, LREAL->Double, UDINT->UInt32.
// sampling: OPC-UA monitoredItem samplingInterval (ms). Alarmlar hızlı,
//           analoglar orta, sayaçlar yavaş (katmanlı sampling).
// ------------------------------------------------------------
function n(variable) {
    return `ns={ns};s=|var|${APP}.GVL_HMI.${variable}`;
}

export const TAGS = {
    // --- Bölge durumları (E_ZoneState enum: 0..5) — salt okunur ---
    zone1_state: { path: n('aZoneState[1]'), dir: 'r', sampling: 250 },
    zone2_state: { path: n('aZoneState[2]'), dir: 'r', sampling: 250 },
    zone3_state: { path: n('aZoneState[3]'), dir: 'r', sampling: 250 },

    // --- Bölge hızları (REAL, m/min) — salt okunur, analog ---
    zone1_speed: { path: n('aZoneSpeed[1]'), dir: 'r', sampling: 500 },
    zone2_speed: { path: n('aZoneSpeed[2]'), dir: 'r', sampling: 500 },
    zone3_speed: { path: n('aZoneSpeed[3]'), dir: 'r', sampling: 500 },

    // --- Bölge çalışma bayrakları (BOOL) — salt okunur ---
    zone1_running: { path: n('aZoneRunning[1]'), dir: 'r', sampling: 250 },
    zone2_running: { path: n('aZoneRunning[2]'), dir: 'r', sampling: 250 },
    zone3_running: { path: n('aZoneRunning[3]'), dir: 'r', sampling: 250 },

    // --- Sıkışma alarmları (BOOL) — hızlı sampling, alarm ---
    zone1_jam: { path: n('aZoneJam[1]'), dir: 'r', sampling: 100 },
    zone2_jam: { path: n('aZoneJam[2]'), dir: 'r', sampling: 100 },
    zone3_jam: { path: n('aZoneJam[3]'), dir: 'r', sampling: 100 },

    // --- Güvenlik / interlock / genel alarm (BOOL) — kritik, hızlı ---
    estop_active: { path: n('xEStopActive'), dir: 'r', sampling: 100 },
    run_permit:   { path: n('xRunPermit'),   dir: 'r', sampling: 250 },
    zone2_itlk:   { path: n('xZone2Itlk'),   dir: 'r', sampling: 100 },
    any_alarm:    { path: n('xAnyAlarm'),     dir: 'r', sampling: 100 },

    // --- Komutlar (HMI -> PLC, yazılabilir) ---
    cmd_auto_run_z1: { path: n('axCmdAutoRun[1]'), dir: 'rw', dataType: 'Boolean', sampling: 500 },
    cmd_auto_run_z2: { path: n('axCmdAutoRun[2]'), dir: 'rw', dataType: 'Boolean', sampling: 500 },
    cmd_auto_run_z3: { path: n('axCmdAutoRun[3]'), dir: 'rw', dataType: 'Boolean', sampling: 500 },
    cmd_reset:       { path: n('xCmdReset'),        dir: 'rw', dataType: 'Boolean', sampling: 500 },

    // --- Heartbeat (UDINT, her saniye toggle) — bağlantı canlılığı ---
    heartbeat: { path: n('uHeartbeat'), dir: 'r', sampling: 500 },
};

// Alarm sınıflandırması (architecture/03_alarm_management.md, ISA-18.2 öncelikleri).
// Frontend bu meta-veriyi kullanmaz; gateway BOOL alarm tag'lerini bu listeden
// türeterek ALARM mesajı üretir. Mesaj: ne oldu + öncelik.
export const ALARM_DEFS = {
    estop_active: { priority: 'CRITICAL', text: 'Acil Durdurma (E-Stop) Aktif' },
    zone2_itlk:   { priority: 'HIGH',     text: 'Bölge 2 Interlock Blokajı (A060)' },
    zone1_jam:    { priority: 'HIGH',     text: 'Bölge 1 Sıkışma' },
    zone2_jam:    { priority: 'HIGH',     text: 'Bölge 2 Sıkışma' },
    zone3_jam:    { priority: 'HIGH',     text: 'Bölge 3 Sıkışma' },
};
