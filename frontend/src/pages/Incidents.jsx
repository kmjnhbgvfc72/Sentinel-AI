import { useCallback, useEffect, useState } from 'react'
import { CheckCircle2, CircleDot, RefreshCw, SearchCheck, ShieldCheck, Siren } from 'lucide-react'
import { securityOperationsApi } from '../api/api'
import { EmptyState, ErrorState, LoadingState } from '../components/PageState'
import { PageHeader } from './Threats'

const workflow = [{label:'Detection',icon:Siren},{label:'Investigation',icon:SearchCheck},{label:'Response',icon:ShieldCheck},{label:'Resolution',icon:CheckCircle2}]
export default function Incidents() {
  const [items, setItems] = useState([]); const [loading, setLoading] = useState(true); const [error, setError] = useState('')
  const load = useCallback(async () => { try { setError(''); setItems(await securityOperationsApi.incidents({limit:50})) } catch(e) { setError(e.message) } finally { setLoading(false) } }, [])
  useEffect(() => { load(); const timer=setInterval(load,15000); return()=>clearInterval(timer) }, [load]); if(loading) return <LoadingState label="Loading response workflows…"/>; if(error) return <ErrorState message={error} onRetry={load}/>
  return <div className="page"><PageHeader eyebrow="Phase 6 · Automated defense" title="Incidents & SOAR Automation" text="High-risk detections promoted into traceable defensive response workflows." action={<button className="button secondary" onClick={load}><RefreshCw size={16}/>Refresh incidents</button>}/><div className="incident-summary"><div><Siren/><span>Active incidents</span><strong>{items.filter(x=>x.status!=='RESOLVED').length}</strong></div><div><ShieldCheck/><span>Automation state</span><strong>ARMED</strong></div><div><CircleDot/><span>Response SLA</span><strong>&lt; 1 min</strong></div></div>{items.length ? <section className="incident-grid">{items.map(item=><article className="panel incident-card" key={item.id}><div className="incident-heading"><div><span>INC-{String(item.id).padStart(5,'0')}</span><h2>{item.incident_type.replaceAll('_',' ')}</h2></div><span className={`severity severity-${item.severity.toLowerCase()}`}>{item.severity}</span></div><p>{item.response_action}</p><div className="workflow-track">{workflow.map(({label,icon:Icon},i)=><div className={i===0 || item.status!=='OPEN' ? 'complete' : i===1 ? 'current' : ''} key={label}><Icon/><span>{label}</span></div>)}</div><footer><span>Status: {item.status}</span><time>{new Date(item.created_at).toLocaleString()}</time></footer></article>)}</section> : <EmptyState title="No active incidents" message="SOAR is armed and monitoring high-risk security detections."/>}</div>
}
