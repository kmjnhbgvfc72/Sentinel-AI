import { useCallback, useEffect, useMemo, useState } from 'react'
import { Activity, Bot, CloudCog, Crosshair, RefreshCw, Route, ShieldAlert, ShieldCheck, Siren, Sparkles, Target } from 'lucide-react'
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { systemApi, unwrapList } from '../api/api'
import StatusCard from '../components/StatusCard'
import RiskScoreCard from '../components/RiskScoreCard'
import AlertCard from '../components/AlertCard'
import { ErrorState, LoadingState } from '../components/PageState'

const demoTrend = [
  { time: '00:00', threats: 14, blocked: 10 }, { time: '04:00', threats: 22, blocked: 18 },
  { time: '08:00', threats: 18, blocked: 15 }, { time: '12:00', threats: 38, blocked: 30 },
  { time: '16:00', threats: 29, blocked: 24 }, { time: '20:00', threats: 46, blocked: 39 },
  { time: 'Now', threats: 34, blocked: 31 },
]

const count = (value) => Array.isArray(value) ? value.length : Number(value?.total ?? value?.count ?? value?.total_count ?? value?.data?.length ?? 0)
const pick = (object, keys, fallback = 0) => keys.reduce((value, key) => value ?? object?.[key], null) ?? fallback

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [health, setHealth] = useState(null)
  const [error, setError] = useState('')
  const [syncing, setSyncing] = useState(false)
  const load = useCallback(async () => {
    setError('')
    try { const [overview, systemHealth] = await Promise.all([systemApi.overview(), systemApi.health()]); setData(overview); setHealth(systemHealth) }
    catch (e) { setError(e.message) }
  }, [])
  useEffect(() => { load(); const timer = setInterval(load, 30000); return () => clearInterval(timer) }, [load])

  const alerts = useMemo(() => unwrapList(data?.ai_detection, ['alerts', 'detections']), [data])
  const incidents = useMemo(() => unwrapList(data?.incidents, ['incidents']), [data])
  const paths = useMemo(() => unwrapList(data?.attack_paths, ['paths', 'attack_paths']), [data])
  const stats = data?.threat_intelligence || {}
  const dashboard = data?.dashboard || {}
  const risk = Number(pick(dashboard, ['risk_score', 'overall_risk_score'], pick(data?.ai_detection, ['average_risk_score'], 62)))
  const activeThreats = pick(stats, ['active_threats', 'total_threats', 'total'], count(stats))
  const aiCount = count(data?.ai_detection)
  const incidentCount = count(data?.incidents)

  async function synchronize() {
    setSyncing(true)
    try { await systemApi.synchronize(20); await load() } catch (e) { setError(e.message) } finally { setSyncing(false) }
  }

  if (!data && !error) return <LoadingState label="Connecting to all nine security phases…" />
  if (!data && error) return <ErrorState message={error} onRetry={load} />

  return <div className="page dashboard-page">
    <div className="page-header"><div><span className="eyebrow">Unified command center</span><h1>Security Operations Overview</h1><p>Live intelligence, detection, prediction, and response across your environment.</p></div><button className="button primary" onClick={synchronize} disabled={syncing}><RefreshCw className={syncing ? 'spin' : ''} size={17} />{syncing ? 'Synchronizing…' : 'Sync pipeline'}</button></div>
    {error && <div className="inline-warning">Live refresh failed: {error}</div>}
    <section className="status-grid">
      <StatusCard title="Active threats" value={activeThreats} subtitle="Phase 3 intelligence" icon={ShieldAlert} tone="red" trend={8.2} />
      <StatusCard title="AI detections" value={aiCount} subtitle="Phase 4 analysis" icon={Bot} tone="violet" trend={12.4} />
      <StatusCard title="Attack paths" value={paths.length} subtitle="Phase 5 predictions" icon={Route} tone="amber" trend={-3.1} />
      <StatusCard title="Open incidents" value={incidentCount} subtitle="Phase 6 SOAR" icon={Siren} tone="cyan" trend={-6.8} />
      <StatusCard title="Security events" value={count(data?.security_logs) || count(data?.threat_intelligence)} subtitle="Central event pipeline" icon={Activity} tone="cyan" trend={5.6} />
      <StatusCard title="Blocked threats" value={pick(data?.dashboard, ['blocked_threats', 'contained_threats'], paths.length)} subtitle="Automated containment" icon={ShieldCheck} tone="violet" trend={14.1} />
    </section>
    <section className="dashboard-grid">
      <article className="panel chart-panel"><div className="panel-heading"><div><span className="eyebrow">24-hour activity</span><h2>Threat detection velocity</h2></div><div className="chart-legend"><span><i className="threat-line" />Detected</span><span><i className="blocked-line" />Contained</span></div></div><div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><AreaChart data={demoTrend}><defs><linearGradient id="threatGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#ff536a" stopOpacity={.35}/><stop offset="100%" stopColor="#ff536a" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#1d2d42" vertical={false}/><XAxis dataKey="time" stroke="#718096" tickLine={false} axisLine={false}/><YAxis stroke="#718096" tickLine={false} axisLine={false}/><Tooltip contentStyle={{ background: '#0c1929', border: '1px solid #263a50', borderRadius: 10 }}/><Area type="monotone" dataKey="threats" stroke="#ff536a" fill="url(#threatGradient)" strokeWidth={2}/><Area type="monotone" dataKey="blocked" stroke="#20d6bd" fill="transparent" strokeWidth={2}/></AreaChart></ResponsiveContainer></div></article>
      <RiskScoreCard score={risk} />
    </section>
    <section className="dashboard-grid lower-grid">
      <article className="panel"><div className="panel-heading"><div><span className="eyebrow">Recent activity</span><h2>AI detections</h2></div><a href="/alerts">View all</a></div><div className="compact-list">{alerts.length ? alerts.slice(0, 4).map((alert, index) => <AlertCard key={alert.id || index} alert={alert} />) : <div className="empty-compact">No current AI detections</div>}</div></article>
      <article className="panel phase-panel"><div className="panel-heading"><div><span className="eyebrow">Platform fabric</span><h2>Phase health</h2></div><span className="health-count">{health?.available_phases || 0}/{health?.total_phases || 9} online</span></div><div className="phase-grid">{(health?.phases || []).map((phase) => <div className="phase-item" key={phase.phase}><span className={`phase-number phase-${phase.status}`}>{phase.phase}</span><div><strong>{phase.role}</strong><small>{phase.name}</small></div><i className={`status-dot ${phase.status}`} /></div>)}</div></article>
    </section>
    <section className="integration-strip"><Integration icon={Target} phase="Phase 7" label="External intelligence" value={pick(data?.external_intelligence, ['active_feeds', 'feed_count'], 'Ready')} /><Integration icon={CloudCog} phase="Phase 8" label="System monitoring" value={health?.status || 'Unknown'} /><Integration icon={Crosshair} phase="Phase 9" label="Threat hunting" value={data?.advanced_hunting ? 'Active' : 'Standby'} /><Integration icon={Sparkles} phase="AI pipeline" label="Cross-phase correlation" value="Connected" /></section>
  </div>
}

function Integration({ icon: Icon, phase, label, value }) { return <div><div className="integration-icon"><Icon size={19} /></div><span>{phase}</span><strong>{label}</strong><small><Activity size={12} />{String(value)}</small></div> }
