import { useCallback, useEffect, useState } from 'react'
import { Database, RefreshCw, Search, ShieldCheck } from 'lucide-react'
import { threatApi, unwrapList } from '../api/api'
import ThreatCard from '../components/ThreatCard'
import { EmptyState, ErrorState, LoadingState } from '../components/PageState'

export default function Threats() {
  const [threats, setThreats] = useState([]); const [feeds, setFeeds] = useState([]); const [query, setQuery] = useState(''); const [loading, setLoading] = useState(true); const [error, setError] = useState('')
  const load = useCallback(async () => { setLoading(true); setError(''); const settled = await Promise.allSettled([threatApi.list(), threatApi.logs(), threatApi.feeds()]); const threatRows = settled[0].status === 'fulfilled' ? unwrapList(settled[0].value, ['threats']) : []; const logRows = settled[1].status === 'fulfilled' ? unwrapList(settled[1].value, ['logs']) : []; setThreats(threatRows.length ? threatRows : logRows); if (settled[2].status === 'fulfilled') setFeeds(unwrapList(settled[2].value, ['feeds'])); if (settled.every(x => x.status === 'rejected')) setError(settled[0].reason.message); setLoading(false) }, [])
  useEffect(() => { load() }, [load])
  const shown = threats.filter(item => JSON.stringify(item).toLowerCase().includes(query.toLowerCase()))
  if (loading) return <LoadingState />
  if (error) return <ErrorState message={error} onRetry={load} />
  return <div className="page"><PageHeader eyebrow="Phases 3 & 7" title="Threat Intelligence" text="Correlated internal telemetry and external intelligence feeds." action={<button className="button secondary" onClick={load}><RefreshCw size={16}/>Refresh</button>} /><section className="mini-stats"><div><ShieldCheck/><span><strong>{threats.length}</strong>Threat records</span></div><div><Database/><span><strong>{feeds.length}</strong>External feeds</span></div><div><i className="pulse-dot"/><span><strong>Live</strong>Correlation status</span></div></section><div className="toolbar"><div className="filter-search"><Search size={17}/><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search indicators, sources, or descriptions" /></div><span>{shown.length} results</span></div>{shown.length ? <section className="entity-grid">{shown.map((threat, i) => <ThreatCard key={threat.id || i} threat={threat}/>)}</section> : <EmptyState title="No threats matched" message="Adjust the search or synchronize the central pipeline." />}</div>
}

export function PageHeader({ eyebrow, title, text, action }) { return <div className="page-header"><div><span className="eyebrow">{eyebrow}</span><h1>{title}</h1><p>{text}</p></div>{action}</div> }
