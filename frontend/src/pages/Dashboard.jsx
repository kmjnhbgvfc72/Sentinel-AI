import { useCallback, useEffect, useMemo, useState } from 'react'
import { Activity, Bot, CloudCog, Crosshair, RefreshCw, Route, ShieldAlert, Siren, Sparkles, Target } from 'lucide-react'
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { useLocation } from 'react-router-dom'
import { alertApi, logApi, riskApi, securityOperationsApi, systemApi, threatApi, unwrapList } from '../api/api'
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
const SECURITY_REFRESH_INTERVAL_MS = 15_000

export default function Dashboard() {
  const location = useLocation()
  const [data, setData] = useState(null)
  const [health, setHealth] = useState(null)
  const [securityActivity, setSecurityActivity] = useState([])
  const [securityTotal, setSecurityTotal] = useState(0)
  const [securityAlerts, setSecurityAlerts] = useState([])
  const [authThreats, setAuthThreats] = useState([])
  const [authRisk, setAuthRisk] = useState({ risk_level: 'LOW', risk_score: 10, distribution: { LOW: 1, MEDIUM: 0, HIGH: 0 } })
  const [centralDetections, setCentralDetections] = useState([])
  const [centralPaths, setCentralPaths] = useState([])
  const [centralIncidents, setCentralIncidents] = useState([])
  const [error, setError] = useState('')
  const [syncing, setSyncing] = useState(false)
  const loadSecurity = useCallback(async () => {
    const [loginLogs, activeAlerts, threats, risk, detections, attackPaths, incidents] = await Promise.all([
      logApi.list({ event_type: 'LOGIN', limit: 8 }), alertApi.security({ status: 'ACTIVE', limit: 8 }),
      threatApi.security({ limit: 8 }), riskApi.current(),
      securityOperationsApi.detections(8), securityOperationsApi.attackPaths(8), securityOperationsApi.incidents({ limit: 8 }),
    ])
    setSecurityActivity(loginLogs.data || []); setSecurityAlerts(activeAlerts.data || [])
    setSecurityTotal(loginLogs.total || 0)
    setAuthThreats(threats.data || []); setAuthRisk(risk)
    setCentralDetections(detections || []); setCentralPaths(attackPaths || []); setCentralIncidents(incidents || [])
  }, [])
  const load = useCallback(async () => {
    setError('')
    try {
      const [overview, systemHealth] = await Promise.all([
        systemApi.overview(), systemApi.health(), loadSecurity(),
      ])
      setData(overview); setHealth(systemHealth)
    }
    catch (e) { setError(e.message) }
  }, [loadSecurity])
  useEffect(() => { load() }, [load])
  useEffect(() => {
    const interval = window.setInterval(() => { loadSecurity().catch(() => {}) }, SECURITY_REFRESH_INTERVAL_MS)
    return () => window.clearInterval(interval)
  }, [loadSecurity])

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
    {location.state?.authenticationMessage && <div className="success-notice">{location.state.authenticationMessage}</div>}
    <div className="page-header"><div><span className="eyebrow">Unified command center</span><h1>Security Operations Overview</h1><p>Live intelligence, detection, prediction, and response across your environment.</p></div><button className="button primary" onClick={synchronize} disabled={syncing}><RefreshCw className={syncing ? 'spin' : ''} size={17} />{syncing ? 'Synchronizing…' : 'Sync pipeline'}</button></div>
    {error && <div className="inline-warning">Live refresh failed: {error}</div>}
    <section className="status-grid">
      <StatusCard title="Total Security Events" value={securityTotal} subtitle="Central telemetry" icon={Activity} tone="cyan" trend={12.4} />
      <StatusCard title="Active Threats" value={authThreats.length || activeThreats} subtitle="Threat intelligence" icon={ShieldAlert} tone="red" trend={8.2} />
      <StatusCard title="Critical Alerts" value={securityAlerts.filter(item => ['HIGH','CRITICAL'].includes(item.severity)).length} subtitle="Requires attention" icon={Siren} tone="red" trend={4.1} />
      <StatusCard title="Risk Score" value={`${authRisk.risk_score}/100`} subtitle={authRisk.risk_level} icon={Bot} tone="violet" trend={-3.1} />
      <StatusCard title="Detected Attacks" value={centralPaths.length || paths.length} subtitle="Predicted paths" icon={Route} tone="amber" trend={6.7} />
      <StatusCard title="Blocked Threats" value={centralIncidents.length || incidentCount} subtitle="SOAR workflows" icon={Crosshair} tone="cyan" trend={-6.8} />
    </section>
    <section className="dashboard-grid">
      <article className="panel chart-panel"><div className="panel-heading"><div><span className="eyebrow">24-hour activity</span><h2>Threat detection velocity</h2></div><div className="chart-legend"><span><i className="threat-line" />Detected</span><span><i className="blocked-line" />Contained</span></div></div><div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><AreaChart data={demoTrend}><defs><linearGradient id="threatGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#ff536a" stopOpacity={.35}/><stop offset="100%" stopColor="#ff536a" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#1d2d42" vertical={false}/><XAxis dataKey="time" stroke="#718096" tickLine={false} axisLine={false}/><YAxis stroke="#718096" tickLine={false} axisLine={false}/><Tooltip contentStyle={{ background: '#0c1929', border: '1px solid #263a50', borderRadius: 10 }}/><Area type="monotone" dataKey="threats" stroke="#ff536a" fill="url(#threatGradient)" strokeWidth={2}/><Area type="monotone" dataKey="blocked" stroke="#20d6bd" fill="transparent" strokeWidth={2}/></AreaChart></ResponsiveContainer></div></article>
      <RiskScoreCard score={risk} />
    </section>
    <section className="dashboard-grid lower-grid">
      <article className="panel"><div className="panel-heading"><div><span className="eyebrow">Recent activity</span><h2>AI detections</h2></div><a href="/alerts">View all</a></div><div className="compact-list">{alerts.length ? alerts.slice(0, 4).map((alert, index) => <AlertCard key={alert.id || index} alert={alert} />) : <div className="empty-compact">No current AI detections</div>}</div></article>
      <article className="panel phase-panel"><div className="panel-heading"><div><span className="eyebrow">Platform fabric</span><h2>Phase health</h2></div><span className="health-count">{health?.available_phases || 0}/{health?.total_phases || 9} online</span></div><div className="phase-grid">{(health?.phases || []).map((phase) => <div className="phase-item" key={phase.phase}><span className={`phase-number phase-${phase.status}`}>{phase.phase}</span><div><strong>{phase.role}</strong><small>{phase.name}</small></div><i className={`status-dot ${phase.status}`} /></div>)}</div></article>
    </section>
    <section className="dashboard-grid soc-activity-grid">
      <article className="panel"><div className="panel-heading"><div><span className="eyebrow">Authentication telemetry</span><h2>Recent Security Activity</h2></div><a href="/logs">View all</a></div><div className="security-activity-list">{securityActivity.length ? securityActivity.map((item) => <div className="security-activity-row" key={item.id}><div><strong>{item.username}</strong><small>{item.ip_address || item.source_ip}</small></div><span className={`login-status status-${(item.status || 'unknown').toLowerCase()}`}>{item.status || 'UNKNOWN'}</span><time>{formatSecurityTime(item.created_at || item.timestamp)}</time></div>) : <div className="empty-compact">No login activity recorded yet</div>}</div></article>
      <article className="panel"><div className="panel-heading"><div><span className="eyebrow">Detection queue</span><h2>Security Alerts</h2></div><a href="/alerts">View all</a></div><div className="security-alert-list">{securityAlerts.length ? securityAlerts.map((alert) => <div className="security-alert-item" key={alert.id}><div><strong>{alert.alert_type.replaceAll('_', ' ')}</strong><span className={`severity severity-${alert.severity.toLowerCase()}`}>{alert.severity}</span></div><p>{alert.description}</p><small>User: {alert.username} · IP: {alert.ip_address}</small><time>{formatSecurityTime(alert.created_at)}</time></div>) : <div className="empty-compact">No active security alerts</div>}</div></article>
    </section>
    <section className="dashboard-grid intelligence-risk-grid">
      <article className="panel"><div className="panel-heading"><div><span className="eyebrow">Authentication intelligence</span><h2>Threat Intelligence</h2></div><span className="health-count">{authThreats.length} recent</span></div><div className="threat-intel-list">{authThreats.length ? authThreats.map((threat) => <div className="threat-intel-row" key={threat.id}><div><strong>{threat.threat_type.replaceAll('_', ' ')}</strong><small>Suspicious IP: {threat.source_ip}</small></div><span className={`severity severity-${threat.risk_level.toLowerCase()}`}>{threat.risk_level}</span><time>{formatSecurityTime(threat.created_at)}</time></div>) : <div className="empty-compact">No suspicious authentication intelligence</div>}</div></article>
      <article className="panel"><div className="panel-heading"><div><span className="eyebrow">Five-minute authentication window</span><h2>Risk Monitoring</h2></div><span className={`severity severity-${authRisk.risk_level.toLowerCase()}`}>{authRisk.risk_score}/100</span></div><div className="risk-level-grid">{['LOW', 'MEDIUM', 'HIGH'].map((level) => <div className={`risk-level-item risk-${level.toLowerCase()} ${authRisk.risk_level === level ? 'active' : ''}`} key={level}><span>{level}</span><strong>{authRisk.distribution?.[level] || 0}</strong><small>risk events</small></div>)}</div></article>
    </section>
    <section className="security-pipeline-grid">
      <article className="panel"><div className="panel-heading"><div><span className="eyebrow">Phase 4 central fallback</span><h2>AI Detection</h2></div></div><div className="pipeline-compact-list">{centralDetections.length ? centralDetections.slice(0, 4).map((item) => <div className="pipeline-item" key={item.id}><strong>{item.threat_level} · Risk {item.risk_score}</strong><p>{item.behavior_summary}</p><time>{formatSecurityTime(item.created_at)}</time></div>) : <div className="empty-compact">No AI authentication detections</div>}</div></article>
      <article className="panel"><div className="panel-heading"><div><span className="eyebrow">Phase 5 prediction</span><h2>Attack Prediction</h2></div></div><div className="pipeline-compact-list">{centralPaths.length ? centralPaths.slice(0, 3).map((item) => <div className="pipeline-item" key={item.id}><strong>{item.risk_level} · {item.status}</strong><p>{item.path}</p><time>{formatSecurityTime(item.created_at)}</time></div>) : <div className="empty-compact">No predicted authentication paths</div>}</div></article>
      <article className="panel"><div className="panel-heading"><div><span className="eyebrow">Phase 6 response</span><h2>SOAR Response</h2></div></div><div className="pipeline-compact-list">{centralIncidents.length ? centralIncidents.slice(0, 4).map((item) => <div className="pipeline-item" key={item.id}><strong>{item.incident_type.replaceAll('_', ' ')} · {item.status}</strong><p>{item.response_action}</p><time>{formatSecurityTime(item.created_at)}</time></div>) : <div className="empty-compact">No active authentication incidents</div>}</div></article>
    </section>
    <section className="integration-strip"><Integration icon={Target} phase="Phase 7" label="External intelligence" value={pick(data?.external_intelligence, ['active_feeds', 'feed_count'], 'Ready')} /><Integration icon={CloudCog} phase="Phase 8" label="System monitoring" value={health?.status || 'Unknown'} /><Integration icon={Crosshair} phase="Phase 9" label="Threat hunting" value={data?.advanced_hunting ? 'Active' : 'Standby'} /><Integration icon={Sparkles} phase="AI pipeline" label="Cross-phase correlation" value="Connected" /></section>
  </div>
}

function formatSecurityTime(value) { return value ? new Date(value).toLocaleString() : 'Unknown time' }

function Integration({ icon: Icon, phase, label, value }) { return <div><div className="integration-icon"><Icon size={19} /></div><span>{phase}</span><strong>{label}</strong><small><Activity size={12} />{String(value)}</small></div> }
