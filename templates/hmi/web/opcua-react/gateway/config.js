// ============================================================
// config.js — Gateway konfigürasyonu ve TAG eşlemesi
// ------------------------------------------------------------
// Buradaki tag listesi EXAMPLE_conveyor projesinin GVL_HMI
// değişkenlerine göre örneklenmiştir. Kendi projende:
//   1) symbolPath değerlerini kendi GVL yoluna göre değiştir
//   2) İzlenmeyecek tag'leri sil, yenilerini ekle
//   3) Yazılabilir tag'lerin writable=true ve dataType'ını doğru ver
//      (REAL -> "Float", LREAL -> "Double", BOOL -> "Boolean" — TypeMismatch'e dikkat!)
// ============================================================

import 'dotenv/config';

export const config = {
    // OPC-UA (PLC) bağlantısı
    opcua: {
        endpoint: process.env.OPCUA_ENDPOINT || 'opc.tcp://192.168.1.100:4840',
        namespaceUri:
            process.env.OPCUA_NAMESPACE_URI ||
            'http://www.3s-software.com/schemas/Codesys-V3',
        user: process.env.OPCUA_USER || '',
        pass: process.env.OPCUA_PASS || '',
        securityMode: process.env.OPCUA_SECURITY_MODE || 'None',
        securityPolicy: process.env.OPCUA_SECURITY_POLICY || 'None',
    },

    // WebSocket sunucusu
    wsPort: Number(process.env.WS_PORT || 8080),

    // Yazma yetkisi (boş = doğrulama kapalı, yalnız geliştirme)
    writeAuthToken: process.env.WRITE_AUTH_TOKEN || '',

    // Davranış
    batchIntervalMs: Number(process.env.BATCH_INTERVAL_MS || 100),
    reconnectDelayMs: Number(process.env.RECONNECT_DELAY_MS || 5000),
    heartbeatTimeoutMs: Number(process.env.HEARTBEAT_TIMEOUT_MS || 3000),
};

// ------------------------------------------------------------
// CODESYS symbol yolu öneki.
// CODESYS OPC-UA sunucusunda node yolu tipik olarak:
//   |var|<RuntimeName>.Application.<GVL>.<Değişken>
// RuntimeName projeden projeye değişebilir ("CODESYS Control Win V3" vb.).
// Kendi PLC'nde UaExpert ile gerçek yolu doğrula.
// ------------------------------------------------------------
const SYMBOL_PREFIX = '|var|CODESYS Control.Application.GVL_HMI';

// nsIdx (namespace index) runtime'da getNamespaceIndex ile dinamik gelir;
// burada sadece sembolik yolu tutarız. server.js nodeId'yi `ns=${nsIdx};s=...`
// olarak birleştirir.
function sym(name) {
    return `${SYMBOL_PREFIX}.${name}`;
}

// ------------------------------------------------------------
// İzlenecek (PLC -> HMI) tag'ler — subscription monitored item olur.
// sampling: samplingInterval (ms). Alarm/güvenlik hızlı, sayaç yavaş.
//   tag        : frontend'in kullandığı kısa anahtar
//   symbolPath : CODESYS sembol yolu (nsIdx hariç)
//   sampling   : OPC-UA samplingInterval (ms)
// ------------------------------------------------------------
export const MONITORED_TAGS = [
    // --- Güvenlik / alarm (hızlı: 100ms) ---
    { tag: 'xEStopActive', symbolPath: sym('xEStopActive'), sampling: 100 },
    { tag: 'xAnyAlarm', symbolPath: sym('xAnyAlarm'), sampling: 100 },
    { tag: 'xRunPermit', symbolPath: sym('xRunPermit'), sampling: 100 },
    { tag: 'xZone2Itlk', symbolPath: sym('xZone2Itlk'), sampling: 100 },

    // --- Bölge durumları (normal: 250ms) ---
    // aZoneState[1..3] -> E_ZoneState enum (0..5). Frontend enum'u metne çevirir.
    { tag: 'aZoneState_1', symbolPath: sym('aZoneState[1]'), sampling: 250 },
    { tag: 'aZoneState_2', symbolPath: sym('aZoneState[2]'), sampling: 250 },
    { tag: 'aZoneState_3', symbolPath: sym('aZoneState[3]'), sampling: 250 },

    { tag: 'aZoneRunning_1', symbolPath: sym('aZoneRunning[1]'), sampling: 250 },
    { tag: 'aZoneRunning_2', symbolPath: sym('aZoneRunning[2]'), sampling: 250 },
    { tag: 'aZoneRunning_3', symbolPath: sym('aZoneRunning[3]'), sampling: 250 },

    { tag: 'aZoneJam_1', symbolPath: sym('aZoneJam[1]'), sampling: 100 },
    { tag: 'aZoneJam_2', symbolPath: sym('aZoneJam[2]'), sampling: 100 },
    { tag: 'aZoneJam_3', symbolPath: sym('aZoneJam[3]'), sampling: 100 },

    { tag: 'aZoneSpdFlt_1', symbolPath: sym('aZoneSpdFlt[1]'), sampling: 100 },
    { tag: 'aZoneSpdFlt_2', symbolPath: sym('aZoneSpdFlt[2]'), sampling: 100 },
    { tag: 'aZoneSpdFlt_3', symbolPath: sym('aZoneSpdFlt[3]'), sampling: 100 },

    // --- Analog ölçümler (normal: 500ms) ---
    // aZoneSpeed[1..3] -> REAL (m/min). Gürültülü ise server.js'de deadband uygulanır.
    { tag: 'aZoneSpeed_1', symbolPath: sym('aZoneSpeed[1]'), sampling: 500, deadband: 0.5 },
    { tag: 'aZoneSpeed_2', symbolPath: sym('aZoneSpeed[2]'), sampling: 500, deadband: 0.5 },
    { tag: 'aZoneSpeed_3', symbolPath: sym('aZoneSpeed[3]'), sampling: 500, deadband: 0.5 },

    // --- Heartbeat (1s: 500ms sampling yeterli) ---
    // uHeartbeat -> UDINT, PLC her saniye toggle/artırır. Bağlantı canlılığı için.
    { tag: 'uHeartbeat', symbolPath: sym('uHeartbeat'), sampling: 500 },
];

// ------------------------------------------------------------
// Yazılabilir (HMI -> PLC) komut tag'leri.
// Frontend WRITE_TAG mesajında writeTag anahtarını gönderir; gateway burada
// nodeId'ye ve OPC-UA dataType'ına çevirir.
//   dataType: node-opcua değer tipi. CODESYS BOOL -> "Boolean".
// NOT: aZoneState ENUM (DINT tabanlı) yazma örneği vermedik; komutlar BOOL.
// ------------------------------------------------------------
export const WRITABLE_TAGS = {
    // axCmdAutoRun[1..3] — oto modda bölge çalıştırma isteği (BOOL)
    cmdAutoRun_1: { symbolPath: sym('axCmdAutoRun[1]'), dataType: 'Boolean' },
    cmdAutoRun_2: { symbolPath: sym('axCmdAutoRun[2]'), dataType: 'Boolean' },
    cmdAutoRun_3: { symbolPath: sym('axCmdAutoRun[3]'), dataType: 'Boolean' },

    // xCmdReset — HMI'dan reset (BOOL). PLC tarafında PLT_RST ile OR'lanır.
    cmdReset: { symbolPath: sym('xCmdReset'), dataType: 'Boolean' },
};
