import { useEffect, useState } from 'react'
import { CheckCircle2, Link2, ServerCog } from 'lucide-react'
import { systemApi } from '../api/api'
import { PageHeader } from './Threats'

export default function Settings() {
  const [topology, setTopology] = useState([])
  useEffect(() => { systemApi.topology().then(data => setTopology(data.phases || [])).catch(() => {}) }, [])
  return <div className="page"><PageHeader eyebrow="Platform configuration" title="Settings & Integrations" text="Read-only visibility into central API routing and phase connectivity." /><section className="settings-grid"><article className="panel settings-card"><ServerCog/><div><h2>Central API</h2><p>Frontend requests are routed through the central orchestration layer.</p><label>API base URL<input value={import.meta.env.VITE_API_BASE_URL || 'http://localhost:8100 (Vite proxy)'} readOnly /></label><span className="connected"><CheckCircle2/>Configured</span></div></article><article className="panel"><div className="panel-heading"><div><span className="eyebrow">Service registry</span><h2>Phase integrations</h2></div><Link2/></div><div className="integration-list">{topology.map(item => <div key={item.phase}><span>{item.phase}</span><div><strong>{item.name}</strong><small>{item.role}</small></div><i>Connected</i></div>)}</div></article></section></div>
}
