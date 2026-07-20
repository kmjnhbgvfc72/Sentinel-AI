import { ArrowDownRight, ArrowUpRight } from 'lucide-react'

export default function StatusCard({ title, value, subtitle, icon: Icon, tone = 'cyan', trend }) {
  return <article className={`status-card tone-${tone}`}>
    <div className="status-card-top"><div className="card-icon"><Icon size={21} /></div>{trend != null && <span className={trend >= 0 ? 'trend-up' : 'trend-down'}>{trend >= 0 ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}{Math.abs(trend)}%</span>}</div>
    <strong className="metric-value">{value}</strong><span className="metric-title">{title}</span><small>{subtitle}</small>
  </article>
}
