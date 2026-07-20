import { Clock3, MapPin } from 'lucide-react'

export const severityOf = (item = {}) => String(item.severity || item.risk_level || item.risk || item.priority || 'medium').toLowerCase()

export default function ThreatCard({ threat }) {
  const severity = severityOf(threat)
  return <article className="entity-card">
    <div className="entity-heading"><span className={`severity severity-${severity}`}>{severity}</span><span className="entity-id">#{threat.id ?? threat.threat_id ?? '—'}</span></div>
    <h3>{threat.title || threat.name || threat.threat_type || threat.event_type || 'Security threat detected'}</h3>
    <p>{threat.description || threat.details?.summary || threat.source || 'Threat intelligence event requiring analyst review.'}</p>
    <div className="entity-meta"><span><MapPin size={14} />{threat.source_ip || threat.ip_address || threat.origin || 'Unknown source'}</span><span><Clock3 size={14} />{formatDate(threat.created_at || threat.detected_at || threat.timestamp)}</span></div>
  </article>
}

export function formatDate(value) {
  if (!value) return 'Recently'
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' })
}
