import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Vite konfigürasyonu — React + dev server.
// WebSocket gateway adresi .env (VITE_WS_URL) ile geçilir; bkz. useOpcUa.js
export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
        host: true, // LAN'dan erişim (fabrika zemini cihazları)
    },
});
