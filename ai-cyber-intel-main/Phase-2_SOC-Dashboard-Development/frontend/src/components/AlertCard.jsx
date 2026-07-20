import SeverityBadge from "./SeverityBadge";
import { formatDate, titleCase } from "../utils";

export default function AlertCard({ alert, loading = false, onDetails, onStatusChange }) {
  if (loading) return <article className="card skeleton" aria-busy="true">Loading alert…</article>;
  if (!alert) return <article className="card empty-card">No alert data available.</article>;
  return <article className="alert-card"><div><SeverityBadge severity={alert.severity}/><h3>{alert.title}</h3><p>{alert.source} · {alert.asset}</p><time>{formatDate(alert.created_at)}</time></div><div className="alert-actions"><span className={`status status-${alert.status}`}>{titleCase(alert.status)}</span><button className="text-button" onClick={() => onDetails?.(alert)}>Details</button>{alert.status === "new" && <button className="button secondary small" onClick={() => onStatusChange?.(alert, "acknowledged")}>Acknowledge</button>}{alert.status !== "resolved" && <button className="button small" onClick={() => onStatusChange?.(alert, "resolved")}>Resolve</button>}</div></article>;
}
