import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// Vite konfigürasyonu — Vue 3 SFC desteği.
export default defineConfig({
    plugins: [vue()],
    server: {
        port: 5173,
        host: true, // ağ üzerinden erişim (operatör tabletleri)
    },
});
