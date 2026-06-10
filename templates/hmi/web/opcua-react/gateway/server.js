// ============================================================
// server.js — Gateway giriş noktası
// ------------------------------------------------------------
// PLC (OPC-UA) <-> Gateway <-> Tarayıcı (WebSocket) köprüsünü başlatır.
//
//   PLC  ──opc.tcp──►  OpcuaManager  ──tagUpdate──►  HmiWsServer  ──ws──►  Tarayıcı
//   PLC  ◄─writeNode─  OpcuaManager  ◄─WRITE_TAG───  HmiWsServer  ◄─ws───  Tarayıcı
//
// Çalıştırma:  npm start   (veya geliştirmede: npm run dev)
// ============================================================

import { config } from './config.js';
import { OpcuaManager } from './opcuaManager.js';
import { HmiWsServer } from './wsServer.js';

console.log('============================================');
console.log(' OPC-UA -> WebSocket Gateway (React HMI)');
console.log('============================================');
console.log(` PLC endpoint : ${config.opcua.endpoint}`);
console.log(` WS port      : ${config.wsPort}`);
console.log(` Write auth   : ${config.writeAuthToken ? 'ENABLED' : 'DISABLED (dev only!)'}`);
console.log('--------------------------------------------');

const opcua = new OpcuaManager();
const wsServer = new HmiWsServer(opcua);

// PLC'ye bağlan (başarısız olursa OpcuaManager kendi içinde yeniden dener)
opcua.connect();

// Temiz kapanış — subscription + session + client + WS hepsini kapat
async function shutdown(signal) {
    console.log(`\n[main] ${signal} received, shutting down...`);
    wsServer.stop();
    await opcua.disconnect();
    process.exit(0);
}

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));

// Yakalanmamış hataları logla (gateway çökmesin)
process.on('unhandledRejection', (reason) => {
    console.error('[main] unhandledRejection:', reason);
});
