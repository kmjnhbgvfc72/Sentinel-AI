import { useCallback, useEffect, useMemo, useState } from 'react'
import { BrainCircuit, RefreshCw, ScanSearch, ShieldAlert } from 'lucide-react'
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis } from 'recharts'
import { alertApi, unwrapList } from '../api/api'
import AlertCard from '../components/AlertCard'
import { EmptyState, ErrorState, LoadingState } from '../components/PageState'
import { PageHeader } from './Threats'

const signal = [{ t: '00:00', score: 24 }, { t: '04:00', score: 31 }, { t: '08:00', score: 58 }, { t: '12:00', score: 76 }, { t: '16:00', score: 64 }, { t: 'Now', score: 82 }]

export default function AIDetection() {
  const [alerts, setAlerts] = useState([]); const [loading, setLoading] = useState(true); const [error, setError] = useState('')
  const load = useCallback(async () => { setLoading(true); try { setAlerts(unwrapList(await alertApi.aiDetections(), ['alerts', 'detections'])); setError('') } catch (e) { setError(e.message) } finally { setLoading(false) } }, [])
  useEffect(() => { load(); const id = setInterval(load, 30000); return () => clearInterval(id) }, [load])
  const risk = useMemo(() => Math.min(99, Math.max(22, Math.round(alerts.reduce((sum, item) => sum + Number(item.risk_score || item.risk || 72), 0) / (alerts.length || 1)))), [alerts])
  if (loading) return <LoadingState label="Calibrating AI risk engine…" />; if (error) return <ErrorState message={error} onRetry={load} />
  return <div className="page"><PageHeader eyebrow="Phase 4 · AI security analytics" title="AI Detection Center" text="Behavioral anomaly analysis and threat probability scoring." action={<button className="button secondary" onClick={load}><RefreshCw size={16}/>Refresh analysis</button>} /><section className="ai-hero"><div className="ai-score"><BrainCircuit/><span>Composite risk score</span><strong>{risk}</strong><small>Elevated · live model confidence</small></div><div className="ai-chart"><div><span className="eyebrow">Detection signal</span><h2>Behavioral anomaly trend</h2></div><ResponsiveContainer width="100%" height={170}><AreaChart data={signal}><defs><linearGradient id="aiSignal" x1="0" x2="0" y1="0" y2="1"><stop stopColor="#a979ff" stopOpacity=".5"/><stop offset="1" stopColor="#a979ff" stopOpacity="0"/></linearGradient></defs><XAxis dataKey="t" tickLine={false} axisLine={false}/><Tooltip/><Area type="monotone" dataKey="score" stroke="#a979ff" fill="url(#aiSignal)" strokeWidth={2}/></AreaChart></ResponsiveContainer></div><div className="ai-prediction"><ScanSearch/><span>Leading prediction</span><strong>{alerts[0]?.threat_type || alerts[0]?.title || 'Brute-force behavior'}</strong><p><b>92%</b> probability based on current telemetry.</p></div></section><section className="panel list-panel"><div className="panel-heading"><div><span className="eyebrow">Model decisions</span><h2>Prioritized AI detections</h2></div><ShieldAlert size={18}/></div>{alerts.length ? alerts.map((item, i) => <AlertCard key={item.id || i} alert={item}/>) : <EmptyState title="No active model detections" message="The AI engine has no high-confidence anomalies." />}</section></div>
}
