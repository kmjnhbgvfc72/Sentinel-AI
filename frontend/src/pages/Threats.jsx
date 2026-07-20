import { useCallback, useEffect, useState } from 'react'
import { Database, RefreshCw, Search, ShieldCheck } from 'lucide-react'
import { threatApi, unwrapList } from '../api/api'
import ThreatCard from '../components/ThreatCard'
import { EmptyState, ErrorState, LoadingState } from '../components/PageState'

export default function Threats() {
  const [threats, setThreats] = useState([]); const [feeds, setFeeds] = useState([]); const [query, setQuery] = useState(''); const [loading, setLoading] = useState(true); const [error, setError] = useState('')
  const load = useCallback(async () => { setLoading(true); setError(''); const settled = await Promise.allSettled([threatApi.security({limit:100}), threatApi.list(), threatApi.logs(), threatApi.feeds()]); const central = settled[0].status === 'fulfilled' ? unwrapList(settled[0].value) : []; const threatRows = settled[1].status === 'fulfilled' ? unwrapList(settled[1].value, ['threats']) : []; const logRows = settled[2].status === 'fulfilled' ? unwrapList(settled[2].value, ['logs']) : []; setThreats(central.length ? central : threatRows.length ? threatRows : logRows); if (settled[3].status === 'fulfilled') setFeeds(unwrapList(settled[3].value, ['feeds'])); if (settled.every(x => x.status === 'rejected')) setError(settled[0].reason.message); setLoading(false) }, [])
  useEffect(() => { load() }, [load])
  const shown = threats.filter(item => JSON.stringify(item).toLowerCase().includes(query.toLowerCase()))
  if (loading) return <LoadingState />
  if (error) return <ErrorState message={error} onRetry={load} />
  return <div className="page"><PageHeader eyebrow="Phases 3 & 7" title="Threat Intelligence Center" text="Correlated internal telemetry, suspicious sources, and external intelligence feeds." action={<button className="button secondary" onClick={load}><RefreshCw size={16}/>Refresh</button>} /><section className="mini-stats"><div><ShieldCheck/><span><strong>{threats.length}</strong>Threat records</span></div><div><Database/><span><strong>{feeds.length}</strong>External feeds</span></div><div><i className="pulse-dot"/><span><strong>Live</strong>Correlation status</span></div></section><article className="panel threat-map"><div className="panel-heading"><div><span className="eyebrow">Global source telemetry</span><h2>Threat Map</h2></div><span className="health-count">{new Set(threats.map(x=>x.source_ip).filter(Boolean)).size} suspicious IPs</span></div><div className="map-canvas"><div className="world-silhouette">GLOBAL THREAT SURFACE</div>{threats.slice(0,12).map((threat,i)=><span className={`map-ping ping-${i%6}`} key={threat.id||i} title={threat.source_ip||'Unknown source'}><i/></span>)}</div></article><div className="toolbar"><div className="filter-search"><Search size={17}/><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search indicators, sources, or descriptions" /></div><span>{shown.length} results</span></div>{shown.length ? <section className="entity-grid">{shown.map((threat, i) => <ThreatCard key={threat.id || i} threat={threat}/>)}</section> : <EmptyState title="No threats matched" message="Adjust the search or synchronize the central pipeline." />}</div>
}

export function PageHeader({ eyebrow, title, text, action }) { return <div className="page-header"><div><span className="eyebrow">{eyebrow}</span><h1>{title}</h1><p>{text}</p></div>{action}</div> }
