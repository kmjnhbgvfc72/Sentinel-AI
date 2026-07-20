import { useCallback, useEffect, useState } from 'react'
import { CircleDot, RefreshCw, Route, ShieldAlert } from 'lucide-react'
import { attackPathApi, unwrapList } from '../api/api'
import { EmptyState, ErrorState, LoadingState } from '../components/PageState'
import { PageHeader } from './Threats'

const stages = ['External attacker', 'Entry point', 'Compromised account', 'Internal system', 'Sensitive asset']
export default function AttackGraph() {
  const [paths, setPaths] = useState([]); const [loading, setLoading] = useState(true); const [error, setError] = useState('')
  const load = useCallback(async () => { setLoading(true); try { setPaths(unwrapList(await attackPathApi.list(), ['paths', 'attack_paths'])); setError('') } catch (e) { setError(e.message) } finally { setLoading(false) } }, [])
  useEffect(() => { load() }, [load]); if (loading) return <LoadingState label="Mapping predicted attack paths…" />; if (error) return <ErrorState message={error} onRetry={load} />
  return <div className="page"><PageHeader eyebrow="Phase 5 · Predictive defense" title="Attack Path Graph" text="Potential lateral-movement routes derived from asset risk and AI detections." action={<button className="button secondary" onClick={load}><RefreshCw size={16}/>Refresh graph</button>} /><section className="attack-canvas panel"><div className="attack-flow">{stages.map((stage, index) => <div className="attack-stage" key={stage}><div className={index === stages.length - 1 ? 'stage-node critical' : 'stage-node'}><CircleDot size={18}/><span>Stage {index + 1}</span><strong>{stage}</strong></div>{index < stages.length - 1 && <div className="attack-arrow">→</div>}</div>)}</div><div className="attack-key"><span><i className="danger"/>High-risk route</span><span><i className="warning"/>Predicted pivot</span><span><i className="safe"/>Protected control</span></div></section><section className="path-grid">{paths.length ? paths.map((path, i) => <article className="panel path-card" key={path.id || i}><Route/><span className="severity severity-high">{path.risk_level || 'High'} risk</span><h2>{path.title || path.name || `Predicted path ${i + 1}`}</h2><p>{path.description || 'Potential path connecting an exposed entry point to a protected asset.'}</p><div><ShieldAlert size={14}/>{path.target_asset || path.affected_asset || 'Sensitive asset'}</div></article>) : <EmptyState title="No attack paths available" message="Run the Phase 5 analysis pipeline to generate predictive routes." />}</section></div>
}
