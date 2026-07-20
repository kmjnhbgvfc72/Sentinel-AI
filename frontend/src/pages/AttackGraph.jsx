import { useCallback, useEffect, useState } from 'react'
import { ChevronDown, Crosshair, Database, Network, RefreshCw, Server, ShieldAlert, UserRound } from 'lucide-react'
import { securityOperationsApi } from '../api/api'
import { EmptyState, ErrorState, LoadingState } from '../components/PageState'
import { PageHeader } from './Threats'

const stages = [{ label: 'Attacker', icon: Crosshair }, { label: 'Entry Point', icon: ShieldAlert }, { label: 'Compromised Account', icon: UserRound }, { label: 'Internal System', icon: Server }, { label: 'Sensitive Asset', icon: Database }]
export default function AttackGraph() {
  const [paths, setPaths] = useState([]); const [selected, setSelected] = useState(0); const [loading, setLoading] = useState(true); const [error, setError] = useState('')
  const load = useCallback(async () => { try { setError(''); setPaths(await securityOperationsApi.attackPaths(30)) } catch (e) { setError(e.message) } finally { setLoading(false) } }, [])
  useEffect(() => { load() }, [load]); if (loading) return <LoadingState label="Constructing attack graph…"/>; if (error) return <ErrorState message={error} onRetry={load}/>
  const path = paths[selected]
  return <div className="page"><PageHeader eyebrow="Phase 5 · Predictive defense" title="Attack Path Visualization" text="Explore likely progression from external entry point to protected assets." action={<button className="button secondary" onClick={load}><RefreshCw size={16}/>Refresh graph</button>} />{paths.length ? <><div className="attack-selector panel"><Network/><select value={selected} onChange={e => setSelected(Number(e.target.value))}>{paths.map((item, i) => <option value={i} key={item.id}>{item.source_ip} · {item.risk_level} · Path #{item.id}</option>)}</select><span className={`severity severity-${path.risk_level.toLowerCase()}`}>{path.risk_score}/100</span></div><section className="panel attack-canvas"><div className="attack-grid-bg"/><div className="attack-stage-flow">{stages.map(({label,icon:Icon}, i) => <div className="attack-stage-wrap" key={label}><div className={`attack-stage stage-${i}`}><Icon/><span>Stage {i + 1}</span><strong>{label}</strong><small>{i === 0 ? path.source_ip : ['Authentication service','User identity','Privileged network','Critical data'][i-1]}</small></div>{i < stages.length - 1 && <ChevronDown className="attack-arrow"/>}</div>)}</div><div className="attack-path-footer"><span>Prediction status: <strong>{path.status}</strong></span><span>Model path: {path.path}</span></div></section></> : <EmptyState title="No attack paths predicted" message="Suspicious authentication activity will generate an attack graph."/>}</div>
}
