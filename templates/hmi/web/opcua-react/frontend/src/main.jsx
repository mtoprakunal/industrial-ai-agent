import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles.css';

// React 18 StrictMode: geliştirmede effect'leri 2x çalıştırır.
// useOpcUa singleton WebSocket kullandığı için çift bağlantı oluşmaz.
createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
