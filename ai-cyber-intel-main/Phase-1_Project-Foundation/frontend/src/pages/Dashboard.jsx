import { useEffect, useState } from "react";
import { getHealth } from "../services/api";
import { formatTimestamp, statusLabel } from "../utils/helpers";

const capabilities = [
  { label: "Threat feeds", value: "Ready", detail: "Integration foundation" },
  { label: "Detection engine", value: "Phase 4", detail: "AI pipeline planned" },
  { label: "Risk analysis", value: "Phase 3", detail: "Scoring model planned" },
];

export default function Dashboard() {
  const [health, setHealth] = useState({ state: "loading", data: null });

  useEffect(() => {
    const controller = new AbortController();
    getHealth(controller.signal)
      .then((data) => setHealth({ state: "success", data }))
      .catch((error) => {
        if (error.name !== "AbortError") setHealth({ state: "error", data: null });
      });
    return () => controller.abort();
  }, []);

  const isHealthy = health.state === "success" && health.data?.status === "healthy";

  return (
    <section>
      <div className="dashboard-heading">
        <div>
          <p className="eyebrow">Security Operations Center</p>
          <h2>System Overview</h2>
          <p className="muted">Real-time foundation status for the threat intelligence platform.</p>
        </div>
        <span className="classification">TLP:CLEAR</span>
      </div>

      <div className="metrics-grid">
        {capabilities.map((item) => (
          <article className="metric-card" key={item.label}>
            <p>{item.label}</p>
            <strong>{item.value}</strong>
            <span>{item.detail}</span>
          </article>
        ))}
      </div>

      <article className="health-panel">
        <div className="panel-title">
          <div>
            <p className="eyebrow">Platform telemetry</p>
            <h3>Backend Health</h3>
          </div>
          <span className={`status-badge ${isHealthy ? "healthy" : health.state}`}>
            {health.state === "loading" ? "Checking" : statusLabel(health.data?.status)}
          </span>
        </div>
        <div className="health-details">
          <div><span>Service</span><strong>{health.data?.service ?? "FastAPI backend"}</strong></div>
          <div><span>Version</span><strong>{health.data?.version ?? "—"}</strong></div>
          <div><span>Last check</span><strong>{formatTimestamp(health.data?.timestamp)}</strong></div>
        </div>
        {health.state === "error" && (
          <p className="error-message">The API is unreachable. Start the backend and confirm VITE_API_BASE_URL.</p>
        )}
      </article>
    </section>
  );
}
