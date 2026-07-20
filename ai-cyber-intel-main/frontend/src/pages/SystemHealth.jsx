import { useCallback, useEffect, useState } from 'react'
import { Activity, RefreshCw, ServerCog } from 'lucide-react'
import { systemApi } from '../api/api'
import { ErrorState, LoadingState } from '../components/PageState'
import { PageHeader } from './Threats'

export default function SystemHealth() {
  const [health, setHealth] = useState(null); const [error, setError] = useState('')
  const load = useCallback(async () => { try { setHealth(await systemApi.health()); setError('') } catch (e) { setError(e.message) } }, [])
  useEffect(() => { load(); const id = setInterval(load, 30000); return () => clearInterval(id) }, [load]); if (!health && !error) return <LoadingState label="Checking the nine-phase platform fabric…" />; if (!health && error) return <ErrorState message={error} onRetry={load} />
  return <div className="page"><PageHeader eyebrow="Platform operations · Phases 1–9" title="System Health" text="Live connectivity and runtime status across the security platform." action={<button className="button secondary" onClick={load}><RefreshCw size={16}/>Check now</button>} /><section className="health-hero panel"><ServerCog/><div><span>Platform availability</span><strong>{health.available_phases || 0}/{health.total_phases || 9} phases online</strong><p>Central orchestration is actively monitoring dependent SOC capabilities.</p></div><Activity className="health-pulse"/></section><section className="health-board">{(health.phases || []).map(phase => <article className="panel health-service" key={phase.phase}><span className={`phase-number phase-${phase.status}`}>P{phase.phase}</span><div><small>{phase.role}</small><h2>{phase.name}</h2><p>{phase.url || 'Managed service'}</p></div><b className={phase.status}>{phase.status || 'unknown'}</b></article>)}</section></div>
}
