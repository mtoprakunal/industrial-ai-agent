import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite yapilandirmasi.
// WebSocket adresi runtime'da env'den okunur (src/config.js); burada proxy
// gerekmez cunku gateway ayri bir portta (8080) dogrudan WS sunar.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true, // LAN'dan erisim (operator istasyonlari)
  },
});
