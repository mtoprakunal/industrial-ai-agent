---
KONU        : React ile Endüstriyel HMI Geliştirme
KATEGORİ    : hmi
ALT_KATEGORI: web-based
SEVİYE      : Uzman
SON_GÜNCELLEME: 2026-06-09
KAYNAKLAR   :
  - url: "https://oneuptime.com/blog/post/2026-01-15-websockets-react-real-time-applications/view"
    başlık: "OneUptime Blog — WebSockets in React for Real-Time Applications (2026)"
    güvenilirlik: topluluk
  - url: "https://moldstud.com/articles/p-real-time-state-management-in-react-using-websockets-boost-your-apps-performance"
    başlık: "MoldStud — Real-Time State Management in React Using WebSockets"
    güvenilirlik: topluluk
  - url: "https://dev.to/alex_bobes/react-performance-optimization-15-best-practices-for-2025-17l9"
    başlık: "DEV.to — React Performance Optimization: 15 Best Practices for 2025"
    güvenilirlik: topluluk
BAĞLANTILAR :
  - konu: "04_vue_patterns.md"
    ilişki: alternatif
  - konu: "05_realtime_websocket.md"
    ilişki: gerektirir
  - konu: "01_opcua_clients_js.md"
    ilişki: kullanır
  - konu: "knowledge/hmi/architecture/02_realtime_data.md"
    ilişki: gerektirir
ÖNKOŞUL     :
  - "React hooks (useState, useEffect, useCallback, useMemo) temel kullanımı"
  - "WebSocket temelleri (05_realtime_websocket.md)"
  - "HMI gerçek zamanlı veri yönetimi (architecture/02_realtime_data.md)"
ÇELİŞKİLER :
  - kaynak: "Her değer değişiminde tüm HMI yeniden render"
    konu: "Gerçek zamanlı veri ile React re-render yönetimi kritik"
    çözüm: >
      WebSocket'ten her saniye onlarca güncelleme gelirse ve her güncelleme
      state değiştirirse — tüm bileşen ağacı yeniden render edilir.
      Çözüm: Zustand atom'ları veya Context bölümleme ile yalnızca değişen
      bileşeni render et. useMemo ve React.memo ile hesaplama önbelleği.
      Throttle ile saniyede max N render garantisi.
---

## Özün Ne

React, bileşen tabanlı yapısı, zengin ekosistemi ve güçlü hook sistemi ile endüstriyel web HMI geliştirme için doğal bir seçimdir. Ancak endüstriyel HMI, standart web uygulamasından farklı kısıtlar getirir: Saniyede onlarca WebSocket güncellemesi, 200+ bileşenin aynı anda güncel olması, gereksiz render'lardan kaçınma ve bağlantı durumunun her bileşende tutarlı yansıtılması. Bu belge, bu kısıtlara uygun React mimarisi kalıplarını ve endüstriyel projede test edilmiş yaklaşımları ele alır.

## Nasıl Çalışır

### Mimari Genel Bakış

```
Backend (Node.js)
  OPC UA / Modbus → WebSocket Server
       │
       │ ws://
       ▼
React Frontend
  useWebSocket hook (singleton bağlantı)
       │
       ├── Zustand Store (tag değerleri, bağlantı durumu)
       │          │
       │          ├── useTagValue('motor_speed') → SpeedGauge
       │          ├── useTagValue('temperature')  → TempDisplay
       │          ├── useTagValue('motor_fault')  → AlarmBadge
       │          └── useConnectionStatus()       → StatusBar
       │
       └── API (fetch) → Yazma komutları
```

### Kurulum

```bash
npm create vite@latest hmi-frontend -- --template react-ts
cd hmi-frontend
npm install zustand
npm install @radix-ui/react-* recharts lucide-react
# İsteğe bağlı: shadcn/ui (bileşen kütüphanesi)
```

### State Yönetimi — Zustand ile

Zustand, endüstriyel HMI için Zustand Redux'tan çok daha basit ve performanslıdır:

```typescript
// store/hmiStore.ts
import { create } from 'zustand';

type ConnectionStatus = "DISCONNECTED" | "CONNECTING" | "CONNECTED" | "ERROR";
type Quality = "GOOD" | "BAD" | "UNCERTAIN";

interface TagValue {
    value: any;
    quality: Quality;
    timestamp: Date;
    age?: number;    // ms cinsinden yaş (son güncelleme)
}

interface HMIState {
    // Bağlantı
    connectionStatus: ConnectionStatus;
    setConnectionStatus: (s: ConnectionStatus) => void;

    // Tag değerleri
    tags: Record<string, TagValue>;
    updateTag: (tag: string, value: any, quality: Quality, ts: Date) => void;
    setFullUpdate: (data: Record<string, any>) => void;

    // Alarm
    activeAlarms: string[];
    addAlarm: (tag: string) => void;
    removeAlarm: (tag: string) => void;
}

export const useHMIStore = create<HMIState>((set, get) => ({
    connectionStatus: "DISCONNECTED",
    setConnectionStatus: (s) => set({ connectionStatus: s }),

    tags: {},
    updateTag: (tag, value, quality, ts) => set((state) => ({
        tags: {
            ...state.tags,
            [tag]: { value, quality, timestamp: ts, age: 0 }
        }
    })),
    setFullUpdate: (data) => {
        const now = new Date();
        const tags: Record<string, TagValue> = {};
        for (const [tag, value] of Object.entries(data)) {
            tags[tag] = { value, quality: "GOOD", timestamp: now };
        }
        set({ tags });
    },

    activeAlarms: [],
    addAlarm: (tag) => set((s) => ({
        activeAlarms: s.activeAlarms.includes(tag) ? s.activeAlarms : [...s.activeAlarms, tag]
    })),
    removeAlarm: (tag) => set((s) => ({
        activeAlarms: s.activeAlarms.filter(a => a !== tag)
    })),
}));
```

### WebSocket Hook — Singleton

```typescript
// hooks/useWebSocket.ts
import { useEffect, useRef } from 'react';
import { useHMIStore } from '../store/hmiStore';

// Singleton WebSocket — tüm bileşenler aynı bağlantıyı kullanır
let wsInstance: WebSocket | null = null;
let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

export function useWebSocket() {
    const { setConnectionStatus, updateTag, setFullUpdate } = useHMIStore();
    const mountedRef = useRef(true);

    useEffect(() => {
        mountedRef.current = true;
        initWebSocket();
        return () => { mountedRef.current = false; };
    }, []);

    function initWebSocket() {
        if (wsInstance?.readyState === WebSocket.OPEN) return;

        setConnectionStatus("CONNECTING");
        wsInstance = new WebSocket("ws://localhost:8080");

        wsInstance.onopen = () => {
            if (!mountedRef.current) return;
            setConnectionStatus("CONNECTED");
            if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = null; }
        };

        wsInstance.onmessage = (event) => {
            if (!mountedRef.current) return;
            const msg = JSON.parse(event.data);

            switch (msg.type) {
                case "TAG_UPDATE":
                    updateTag(msg.tag, msg.value, msg.quality, new Date(msg.timestamp));
                    break;
                case "FULL_UPDATE":
                    setFullUpdate(msg.data);
                    setConnectionStatus("CONNECTED");
                    break;
                case "CONNECTION_STATUS":
                    setConnectionStatus(msg.status);
                    break;
            }
        };

        wsInstance.onclose = () => {
            setConnectionStatus("DISCONNECTED");
            scheduleReconnect();
        };

        wsInstance.onerror = () => {
            setConnectionStatus("ERROR");
        };
    }

    function scheduleReconnect() {
        if (reconnectTimer) return;
        reconnectTimer = setTimeout(() => {
            reconnectTimer = null;
            initWebSocket();
        }, 3000);
    }

    // Yazma komutu gönder
    function sendCommand(type: string, payload: object) {
        if (wsInstance?.readyState === WebSocket.OPEN) {
            wsInstance.send(JSON.stringify({ type, ...payload }));
        }
    }

    return { sendCommand };
}
```

### Tag Değeri Hook'u

```typescript
// hooks/useTagValue.ts
import { useHMIStore } from '../store/hmiStore';

export function useTagValue<T = any>(tag: string): {
    value: T | null;
    quality: "GOOD" | "BAD" | "UNCERTAIN";
    isStale: boolean;
    timestamp: Date | null;
} {
    // Zustand'dan yalnızca bu tag'i seç → Diğer tag güncellenince render olmaz
    const tagData = useHMIStore((state) => state.tags[tag]);
    const connectionStatus = useHMIStore((state) => state.connectionStatus);

    if (!tagData || connectionStatus === "DISCONNECTED") {
        return { value: null, quality: "BAD", isStale: true, timestamp: null };
    }

    const isStale = (Date.now() - tagData.timestamp.getTime()) > 5000;  // 5s
    return {
        value: tagData.value as T,
        quality: tagData.quality,
        isStale,
        timestamp: tagData.timestamp
    };
}
```

### Temel HMI Bileşenleri

```tsx
// components/TagDisplay.tsx
import React from 'react';
import { useTagValue } from '../hooks/useTagValue';

interface TagDisplayProps {
    tag: string;
    label: string;
    unit?: string;
    decimals?: number;
    maxAge?: number;     // ms, varsayılan 5000
}

export const TagDisplay = React.memo(({ tag, label, unit = "", decimals = 1, maxAge = 5000 }: TagDisplayProps) => {
    const { value, quality, isStale } = useTagValue<number>(tag);

    const formattedValue = value !== null ? value.toFixed(decimals) : "--.-";

    return (
        <div className={`tag-display ${isStale ? "stale" : ""} quality-${quality.toLowerCase()}`}>
            <span className="label">{label}</span>
            <span className="value">
                {formattedValue}
                <span className="unit">{unit}</span>
            </span>
            {isStale && <span className="stale-badge" title="Eski veri">⚠</span>}
        </div>
    );
});
// React.memo: Tag değeri değişmedikçe yeniden render olmaz
```

```tsx
// components/StatusIndicator.tsx — Motor durumu göstergesi (ISA-101 uyumlu)
interface StatusIndicatorProps {
    tag: string;    // Boolean tag
    label: string;
    onLabel?: string;
    offLabel?: string;
}

export const StatusIndicator = React.memo(({ tag, label, onLabel = "ÇALIŞIYOR", offLabel = "DURMUŞ" }: StatusIndicatorProps) => {
    const { value, quality, isStale } = useTagValue<boolean>(tag);

    // ISA-101: Normal = gri, Alarm/Değişim = renkli
    const state = isStale || quality === "BAD" ? "unknown"
                : value ? "running"
                : "stopped";

    return (
        <div className={`status-indicator state-${state}`}>
            <div className="status-dot" />
            <div className="status-info">
                <span className="status-label">{label}</span>
                <span className="status-text">
                    {state === "unknown" ? "?" : value ? onLabel : offLabel}
                </span>
            </div>
        </div>
    );
});
```

```tsx
// components/AnalogGauge.tsx — Analog değer göstergesi + alarm seviyeleri
interface AnalogGaugeProps {
    tag: string;
    label: string;
    unit: string;
    min: number;
    max: number;
    alarmHigh?: number;
    alarmLow?: number;
    decimals?: number;
}

export const AnalogGauge = React.memo(({
    tag, label, unit, min, max, alarmHigh, alarmLow, decimals = 1
}: AnalogGaugeProps) => {
    const { value, quality, isStale } = useTagValue<number>(tag);

    const pct = value !== null ? Math.max(0, Math.min(100, ((value - min) / (max - min)) * 100)) : 0;
    const isHighAlarm = alarmHigh !== undefined && value !== null && value >= alarmHigh;
    const isLowAlarm  = alarmLow  !== undefined && value !== null && value <= alarmLow;
    const hasAlarm = isHighAlarm || isLowAlarm;

    return (
        <div className={`analog-gauge ${hasAlarm ? "alarm" : ""} ${isStale ? "stale" : ""}`}>
            <div className="gauge-label">{label}</div>
            <div className="gauge-value">
                {value !== null ? value.toFixed(decimals) : "--.-"}
                <span className="unit">{unit}</span>
            </div>
            <div className="gauge-bar">
                <div
                    className={`gauge-fill ${isHighAlarm ? "alarm-high" : isLowAlarm ? "alarm-low" : ""}`}
                    style={{ width: `${pct}%` }}
                />
                {alarmHigh && <div className="alarm-line high" style={{ left: `${((alarmHigh - min) / (max - min)) * 100}%` }} />}
                {alarmLow  && <div className="alarm-line low"  style={{ left: `${((alarmLow  - min) / (max - min)) * 100}%` }} />}
            </div>
            <div className="gauge-range">
                <span>{min}</span><span>{max} {unit}</span>
            </div>
        </div>
    );
});
```

```tsx
// components/SetpointControl.tsx — Setpoint giriş kontrolü
import { useState } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';
import { useTagValue } from '../hooks/useTagValue';
import { useHMIStore } from '../store/hmiStore';

interface SetpointControlProps {
    tag: string;
    writeTag: string;    // Backend'e gönderilecek tag ismi
    label: string;
    unit: string;
    min: number;
    max: number;
    step?: number;
    requiredPermission?: string;
}

export const SetpointControl = ({ tag, writeTag, label, unit, min, max, step = 1, requiredPermission }: SetpointControlProps) => {
    const { value: currentValue } = useTagValue<number>(tag);
    const [inputValue, setInputValue] = useState<string>("");
    const [pending, setPending] = useState(false);
    const connectionStatus = useHMIStore((s) => s.connectionStatus);
    const { sendCommand } = useWebSocket();

    const isConnected = connectionStatus === "CONNECTED";
    const displayValue = inputValue !== "" ? parseFloat(inputValue) : (currentValue ?? 0);

    const handleApply = async () => {
        const newValue = parseFloat(inputValue);
        if (isNaN(newValue) || newValue < min || newValue > max) {
            alert(`Değer ${min}-${max} aralığında olmalı`);
            return;
        }

        setPending(true);
        sendCommand("WRITE_REGISTER", { tag: writeTag, value: newValue });
        setInputValue("");
        setTimeout(() => setPending(false), 1000);
    };

    return (
        <div className="setpoint-control">
            <label className="sp-label">{label}</label>
            <div className="sp-current">Mevcut: {currentValue?.toFixed(1)} {unit}</div>
            <div className="sp-input-row">
                <input
                    type="number"
                    min={min} max={max} step={step}
                    value={inputValue}
                    onChange={e => setInputValue(e.target.value)}
                    placeholder={String(currentValue?.toFixed(1) ?? "--")}
                    disabled={!isConnected || pending}
                    className="sp-input"
                />
                <span className="sp-unit">{unit}</span>
                <button
                    onClick={handleApply}
                    disabled={!isConnected || pending || inputValue === ""}
                    className="sp-apply-btn"
                >
                    {pending ? "..." : "Uygula"}
                </button>
            </div>
        </div>
    );
};
```

### Alarm Paneli

```tsx
// components/AlarmPanel.tsx
import { useHMIStore } from '../store/hmiStore';

const ALARM_LABELS: Record<string, { label: string; priority: "CRITICAL" | "HIGH" | "MEDIUM" }> = {
    motor_fault:      { label: "Motor Arızası", priority: "CRITICAL" },
    temp_high_alarm:  { label: "Sıcaklık Yüksek", priority: "HIGH" },
    pressure_low:     { label: "Basınç Düşük", priority: "MEDIUM" },
};

export const AlarmPanel = () => {
    const activeAlarms = useHMIStore((s) => s.activeAlarms);

    if (activeAlarms.length === 0) {
        return <div className="alarm-panel no-alarms">✓ Aktif Alarm Yok</div>;
    }

    return (
        <div className="alarm-panel">
            <h3>Aktif Alarmlar ({activeAlarms.length})</h3>
            <ul className="alarm-list">
                {activeAlarms.map(tag => {
                    const info = ALARM_LABELS[tag] ?? { label: tag, priority: "MEDIUM" };
                    return (
                        <li key={tag} className={`alarm-item priority-${info.priority.toLowerCase()}`}>
                            <span className="alarm-icon">
                                {info.priority === "CRITICAL" ? "🔴" : info.priority === "HIGH" ? "🟠" : "🟡"}
                            </span>
                            <span className="alarm-label">{info.label}</span>
                        </li>
                    );
                })}
            </ul>
        </div>
    );
};
```

### Ana Uygulama

```tsx
// App.tsx
import { useEffect } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import { useHMIStore } from './store/hmiStore';
import { TagDisplay } from './components/TagDisplay';
import { StatusIndicator } from './components/StatusIndicator';
import { AnalogGauge } from './components/AnalogGauge';
import { SetpointControl } from './components/SetpointControl';
import { AlarmPanel } from './components/AlarmPanel';

function ConnectionBanner() {
    const status = useHMIStore((s) => s.connectionStatus);
    if (status === "CONNECTED") return null;
    return (
        <div className={`connection-banner status-${status.toLowerCase()}`}>
            {status === "DISCONNECTED" && "⚠ PLC bağlantısı kesildi — yeniden bağlanıyor..."}
            {status === "CONNECTING"   && "⏳ PLC'ye bağlanılıyor..."}
            {status === "ERROR"        && "❌ Bağlantı hatası"}
        </div>
    );
}

export default function App() {
    // WebSocket bağlantısını kur (singleton)
    useWebSocket();

    return (
        <div className="hmi-app">
            <ConnectionBanner />
            
            <header className="hmi-header">
                <h1>Hat 1 — Paketleme Makinesi</h1>
                <AlarmPanel />
            </header>

            <main className="hmi-main">
                {/* Durum */}
                <section className="status-section">
                    <StatusIndicator tag="motor_running" label="Ana Motor" />
                    <StatusIndicator tag="motor_fault" label="Motor Arıza" onLabel="ARIZALI" offLabel="NORMAL" />
                </section>

                {/* Ölçümler */}
                <section className="measurements-section">
                    <AnalogGauge
                        tag="actual_speed" label="Gerçek Hız" unit="m/dk"
                        min={0} max={100} alarmHigh={90} decimals={1}
                    />
                    <AnalogGauge
                        tag="actual_temp" label="Sıcaklık" unit="°C"
                        min={0} max={150} alarmHigh={90} alarmLow={10} decimals={1}
                    />
                    <TagDisplay tag="production_count" label="Üretim Sayacı" decimals={0} />
                </section>

                {/* Kontroller */}
                <section className="controls-section">
                    <SetpointControl
                        tag="actual_speed" writeTag="speed_setpoint"
                        label="Hız Setpoint" unit="m/dk"
                        min={0} max={100} step={0.5}
                    />
                </section>
            </main>
        </div>
    );
}
```

### Performans Optimizasyonu

```typescript
// Kural 1: React.memo ile gereksiz render önle
export const TagDisplay = React.memo(TagDisplayComponent);

// Kural 2: Zustand selector ile granüler state seçimi
const speed = useHMIStore((s) => s.tags["actual_speed"]?.value);
// YERİNE: const { tags } = useHMIStore(); → tags değişince HER bileşen render olur!

// Kural 3: useCallback ile callback stabilitesi
const handleApply = useCallback(() => {
    sendCommand("WRITE_REGISTER", { tag: writeTag, value });
}, [sendCommand, writeTag, value]);

// Kural 4: Çok hızlı güncellemeyi throttle et
import { useMemo } from 'react';
import throttle from 'lodash/throttle';

function useThrottledTagValue(tag: string, ms = 200) {
    const updateTag = useHMIStore((s) => s.updateTag);
    const throttledUpdate = useMemo(
        () => throttle(updateTag, ms),
        [updateTag, ms]
    );
    return throttledUpdate;
}
```

## Sık Yapılan Hatalar

### Hata 1: Tüm Store'u Tek Selectorla Almak

```typescript
// ❌ YANLIŞ — Herhangi bir tag güncellenince TÜM bileşenler render olur
const { tags } = useHMIStore();
const speed = tags["actual_speed"]?.value;

// ✅ DOĞRU — Yalnızca bu tag değişince render olur
const speed = useHMIStore((s) => s.tags["actual_speed"]?.value);
```

### Hata 2: WebSocket'i Her Bileşende Ayrı Açmak

```typescript
// ❌ YANLIŞ — Her bileşen kendi WS açar
function SpeedWidget() {
    const [speed, setSpeed] = useState(0);
    useEffect(() => {
        const ws = new WebSocket("ws://...");  // Her widget için yeni bağlantı!
        ws.onmessage = (e) => setSpeed(JSON.parse(e.data).speed);
    }, []);
}

// ✅ DOĞRU — Singleton WS hook + Store
function SpeedWidget() {
    const speed = useHMIStore((s) => s.tags["actual_speed"]?.value);
    // WS bağlantısı App.tsx seviyesinde tek kez kurulur
}
```

### Hata 3: Bağlantı Kopunca Butonları Aktif Bırakmak

```typescript
// ❌ YANLIŞ
<button onClick={handleStart}>Başlat</button>

// ✅ DOĞRU
const isConnected = useHMIStore((s) => s.connectionStatus === "CONNECTED");
<button onClick={handleStart} disabled={!isConnected}>Başlat</button>
```

## Gerçek Proje Notları

**Not 1 — 200 Bileşen, Her Saniye 50 Güncelleme**  
İlk implementasyonda her WebSocket mesajı tüm `tags` objesini güncelledi → Zustand state değişti → 200 bileşen hepsi render oldu. Saniyede 50 güncelleme × 200 render = aşırı CPU yükü. Granüler selector (her bileşen yalnızca kendi tag'ini seçiyor) eklendikten sonra render sayısı %95 azaldı.

**Not 2 — React.memo'nun Tuzağı**  
`React.memo` kullanıldı ama nesne prop geçildi: `<AnalogGauge config={{ min: 0, max: 100 }} />`. Her render'da yeni nesne → `React.memo` eşleşme bulamadı → Her render tetiklendi. Çözüm: Konfigürasyonu sabit tanımla veya `useMemo` ile sar.

**Not 3 — Zustand DevTools ile Debug**  
```
npm install zustand-devtools
store'u: devtools()(create(...)) şeklinde sar.
Redux DevTools Extension ile state geçmişini izle.
Hangi bileşen ne zaman ne değiştirdi? Net görünür.
```

**Not 4 — useEffect Cleanup Unutulunca Zombi WebSocket Listener**  
`useEffect` içinde `ws.onmessage` atandı ama cleanup'ta kaldırılmadı. Hot-reload (Vite HMR) ve React 18 StrictMode'da bileşen iki kez mount oldu → iki listener birikti → her mesaj iki kez işlendi, alarm sayacı iki katına çıktı. Çözüm: singleton WS + listener'ları cleanup'ta sökme. StrictMode'un çift-mount davranışı geliştirme aşamasında bu sınıf hataları erken ortaya çıkarır — kapatma değil, düzeltme doğru yaklaşımdır.

**Not 5 — React 18 Otomatik Batching Beklenmedik Davranış**  
React 18'de `setState` çağrıları event handler dışında da (Promise, setTimeout, WebSocket onmessage) otomatik batch'lenir. Tek WS mesajında 10 tag güncellense bile tek render olur — bu iyi. Ancak `flushSync` kullanan bir trend grafiği ara değerleri kaçırdı çünkü batching ile sadece son state'i gördü. Yüksek frekanslı veride render'ı senkron zorlamak (`flushSync`) performansı yok eder; batching'e güven, ara değer gerekiyorsa store'da history array tut.

**Not 6 — Zustand Selector Referans Eşitliği Tuzağı**  
`useHMIStore((s) => ({ value: s.tags[tag]?.value, q: s.tags[tag]?.quality }))` her render'da **yeni nesne** döndürdü → Zustand `Object.is` ile eşitlik göremedi → bileşen her store değişiminde (başka tag dahil) render oldu. Çözüm: ya iki ayrı atomik selector, ya `useShallow` (Zustand v4.4+) ile sığ karşılaştırma. Nesne/dizi döndüren selector'lar gizli re-render kaynağıdır.

**Not 7 — Tarih Nesnesinin JSON Serileştirme Kaybı**  
Backend `timestamp` Date olarak gönderdi ama JSON.stringify → string'e çevirdi; frontend `new Date(msg.timestamp)` yapmayı unutunca `isStale` hesabındaki `.getTime()` patladı (`timestamp.getTime is not a function`). WebSocket üzerinden Date asla taşınmaz — number (epoch ms) gönder, frontend'de `new Date()` ile geri kur. Tip katmanında bunu zorlamak (timestamp: number) hatayı derleme zamanına çeker.

## Edge Case'ler ve Sistem Limitleri

React, "ne değişti" yönetimini geliştiriciye bırakır; endüstriyel HMI'ın yüksek frekanslı veri akışında limitler **render maliyeti** ve **reconciliation** etrafında toplanır.

| Edge Case | Tetikleyen | Belirti | Çözüm |
|---|---|---|---|
| StrictMode çift mount | Geliştirmede effect 2× çalışır | Çift listener, çift abonelik | Cleanup fonksiyonu + singleton (Not 4) |
| Selector yeni nesne | Nesne döndüren selector (Not 6) | Gereksiz render | Atomik selector veya `useShallow` |
| Stale closure | `useEffect` deps eksik | Eski değerle çalışan callback | Doğru deps veya `useRef` |
| Yüksek frekans render | >30 güncelleme/s aynı bileşene | Frame drop, UI takılır | Throttle/RAF coalescing |
| Çok node DOM | 500+ tag aynı ekranda | Reconciliation yavaş | Sanallaştırma (react-window), sayfalama |
| Date serileştirme | WS üzerinden Date (Not 7) | `getTime is not a function` | Epoch number gönder |
| Kontrolsüz input + WS | Setpoint input'a WS değeri yazar | Operatör yazarken değer zıplar | Yerel state, WS'i input'a bağlama |
| Memory leak | Listener/timer temizlenmez | Sekme zamanla yavaşlar | Cleanup'ta `clearInterval`/`removeEventListener` |
| Tab arka planda | `setInterval` throttle olur | Geri dönünce veri "donmuş" görünür | `visibilitychange` ile FULL_UPDATE iste |

**Pratik render bütçesi:** 60 FPS için kare başına ~16ms vardır. 200 bileşenli bir HMI'da granüler selector ile yalnızca değişen 5-10 bileşen render olur (~2-4ms) — sorunsuz. Tüm ağacı render etmek (kötü selector) 30-50ms alır → gözle görülür takılma. Kritik eşik: saniyede toplam render süresi × güncelleme frekansı < %50 CPU.

## Optimizasyon

React'ta optimizasyonun özü tek cümledir: **state değişiminden etkilenen bileşen sayısını minimize et.**

1. **Granüler selector (en yüksek etki).** Her bileşen yalnızca kendi tag'ini seçsin: `useHMIStore((s) => s.tags[tag]?.value)`. Tüm `tags` objesini almak tek bir tag değişiminde tüm ağacı render eder (Not 1, %95 fark).

2. **Selector primitif döndürsün.** Nesne/dizi döndüren selector referans eşitliğini bozar (Not 6). Primitif (number/string/boolean) döndür ya da `useShallow` kullan.

3. **React.memo + stabil proplar.** `React.memo`'yu kullan ama nesne/fonksiyon proplarını `useMemo`/`useCallback` ile stabilize et — yoksa memo işe yaramaz (mevcut Not 2).

4. **Yüksek frekanslı tag'leri RAF ile coalesce et.** Saniyede 50 değişen bir tag için her değişimde render gereksiz (insan gözü ~10-15 FPS üstünü ayırt edemez). `requestAnimationFrame` ile son değeri kareye sabitle:

   ```typescript
   function useRafTagValue(tag: string) {
       const raw = useHMIStore((s) => s.tags[tag]?.value);
       const [display, setDisplay] = useState(raw);
       const frame = useRef<number>();
       useEffect(() => {
           cancelAnimationFrame(frame.current!);
           frame.current = requestAnimationFrame(() => setDisplay(raw));
           return () => cancelAnimationFrame(frame.current!);
       }, [raw]);
       return display;
   }
   ```

5. **Store seviyesinde throttle/batch.** Backend zaten batch yapmıyorsa, `updateTag`'i store'da 100ms throttle'la (mevcut `useThrottledTagValue`). Render kaynağını azaltmak, render'ı optimize etmekten önce gelir.

6. **Büyük listeleri sanallaştır.** Alarm geçmişi, 500 satır tag tablosu → `react-window`/`react-virtual`. Yalnızca görünen satırlar DOM'da olur.

7. **State şeklini düzleştir.** İç içe nesne yerine `tags: Record<string, TagValue>` düz yapı; tek tag güncellemesi yalnızca o anahtarı değiştirir, derin spread maliyeti olmaz.

**Optimizasyon sırası (önce yüksek etki):** granüler selector → primitif selector → render kaynağını azalt (throttle/RAF) → React.memo → sanallaştırma. Genelde ilk iki madde sorunların %90'ını çözer; profiler olmadan `useMemo` serpiştirmek erken optimizasyondur.

## Derin Teknik Detay

**Zustand neden Redux'tan hızlı ve neden HMI'a uygun?** Zustand, React Context kullanmaz; harici bir store (closure içinde tutulan mutable referans) + `useSyncExternalStore` (React 18 API) üzerine kuruludur. Context'in temel sorunu: Context value değişince **tüm tüketiciler** yeniden render olur, selector ile daraltma yapılamaz. Zustand'da her `useHMIStore(selector)` çağrısı kendi selector'ını store'a abone eder; store değişince Zustand tüm abonelerin selector'ını çalıştırır, sonucu `Object.is` ile eski sonuçla karşılaştırır, **yalnızca değişen** selector'ın bileşenini render'a sokar. Bu, 200 tag'li HMI'da neden granüler selector'ın kritik olduğunu açıklar — abonelik granülaritesi selector granülaritesidir.

**`useSyncExternalStore` ve tearing.** React 18'in concurrent rendering'i, bir render sırasında harici store değişirse "tearing" (ekranın bir kısmı eski, bir kısmı yeni değer gösterir) yaratabilir. `useSyncExternalStore` bu sorunu çözmek için tasarlandı: render sırasında store snapshot'ının tutarlılığını garanti eder. Zustand bunu kullandığı için yüksek frekanslı WebSocket güncellemelerinde concurrent mode'da bile tutarlı görüntü verir — manuel state (useState + WS) bu garantiyi sunmaz.

**React'ın reconciliation maliyeti neden HMI'da kritik?** React her render'da yeni Virtual DOM ağacı üretir ve eskisiyle diff'ler (reconciliation). Bu O(n) ama n = render edilen bileşen sayısıdır. Tüm ağacı her WS mesajında render etmek (kötü selector) reconciliation'ı her saniye onlarca kez O(200) çalıştırır. Granüler selector ile n=5-10'a iner. React.memo, diff'i bileşen seviyesinde "kes" der: proplar referans-eşitse alt ağaç diff'lenmez. Ama memo'nun karşılaştırması da maliyetlidir — yüzlerce memo bileşeninde shallow compare bile birikir; bu yüzden render'ı *tetiklememek* (selector), tetikleyip *kesmekten* (memo) daha verimlidir.

**vs alternatifler:** Redux Toolkit + `useSelector` benzer granülarite sunar ama boilerplate ağırdır; HMI'ın basit "tag → değer" modeline overkill. Jotai/Recoil "atom" modeli (her tag bir atom) teorik olarak en granüler çözümdür ve 1000+ bağımsız tag senaryosunda Zustand'dan üstün olabilir, ama ekosistem ve öğrenme maliyeti yüksektir. Saf Context + useReducer endüstriyel HMI için yetersizdir (tearing + tüm-tüketici render). Web HMI'ın "çok sayıda bağımsız, sık güncellenen skaler değer" profili için Zustand pratikte en iyi denge: minimal boilerplate + selector-bazlı granülarite + `useSyncExternalStore` güvencesi.

## İlgili Konular

```
knowledge/hmi/web-based/
├── 04_vue_patterns.md           → Vue.js alternatifi
└── 05_realtime_websocket.md     → WebSocket backend entegrasyonu

knowledge/hmi/architecture/
├── 01_hmi_patterns.md           → ISA-101 tasarım prensipleri
├── 02_realtime_data.md          → Stale data ve bağlantı yönetimi
└── 03_alarm_management.md       → Alarm sistemi tasarımı
```
