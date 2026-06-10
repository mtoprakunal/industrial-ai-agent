import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./styles.css";

// StrictMode: gelistirmede effect'leri 2x calistirir -> singleton WS / cleanup
// hatalarini erken yakalar (Not 4). Singleton WS bu davranisi tolere eder.
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
