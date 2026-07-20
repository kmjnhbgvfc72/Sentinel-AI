import SeverityBadge from "./SeverityBadge";
import { formatDate } from "../utils";

export default function ThreatCard({ threat, loading = false, onDetails }) {
  if (loading) return <article className="card skeleton" aria-busy="true">Loading threat…</article>;
  if (!threat) return <article className="card empty-card">No threat data available.</article>;
  return <article className="card threat-card"><div className="row between"><SeverityBadge severity={threat.severity}/><span>{threat.external_id}</span></div><h3>{threat.title}</h3><p className="muted">{threat.category}</p><dl className="compact-list"><div><dt>Confidence</dt><dd>{threat.confidence_score}%</dd></div><div><dt>Asset</dt><dd>{threat.target_asset}</dd></div><div><dt>Detected</dt><dd>{formatDate(threat.last_detected_at)}</dd></div></dl><button className="text-button" onClick={() => onDetails?.(threat)}>View details</button></article>;
}
