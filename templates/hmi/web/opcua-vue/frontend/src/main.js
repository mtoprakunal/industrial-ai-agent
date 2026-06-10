// Uygulama giriş noktası — Vue 3 + Pinia kurulumu.
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import './styles.css';

createApp(App).use(createPinia()).mount('#app');
