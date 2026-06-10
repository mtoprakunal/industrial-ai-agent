// Frontend calisma zamani yapilandirmasi.
// Vite env (import.meta.env) build aninda gomulur.

// WS_URL bos ise sayfanin hostname'ini kullan (ayni makineden sunulan HMI).
export const WS_URL =
  import.meta.env.VITE_WS_URL ||
  `ws://${window.location.hostname}:8080`;

// Yazma yetki token'i (gateway WRITE_TOKEN ile eslesmeli; bos = guard kapali).
export const WRITE_TOKEN = import.meta.env.VITE_WRITE_TOKEN || "";

// Bir tag bu sureden uzun guncellenmediyse "stale" (eski) sayilir.
// Modbus'ta quality yoktur; staleness backend poll'una + WS'e gore tahmindir.
export const STALE_MS = 5000;
