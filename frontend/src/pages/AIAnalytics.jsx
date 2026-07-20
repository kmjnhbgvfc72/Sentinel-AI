import { useCallback, useEffect, useMemo, useState } from 'react'
import { BrainCircuit, RefreshCw, ScanSearch, Sparkles } from 'lucide-react'
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { riskApi, securityOperationsApi } from '../api/api'
import RiskScoreCard from '../components/RiskScoreCard'
import { EmptyState, ErrorState, LoadingState } from '../components/PageState'
import { PageHeader } from './Threats'

export default function AIAnalytics() {
  const [detections, setDetections] = useState([]); const [risk, setRisk] = useState(null); const [loading, setLoading] = useState(true); const [error, setError] = useState('')
  const load = useCallback(async () => { setLoading(true); setError(''); try { const [rows, current] = await Promise.all([securityOperationsApi.detections(50), riskApi.current()]); setDetections(rows); setRisk(current) } catch (e) { setError(e.message) } finally { setLoading(false) } }, [])
  useEffect(() => { load(); const timer = setInterval(load, 15000); return () => clearInterval(timer) }, [load])
  const chart = useMemo(() => detections.slice(0, 12).reverse().map((item, i) => ({ event: `E${i + 1}`, risk: item.risk_score })), [detections])
  if (loading && !risk) return <LoadingState label="Initializing AI risk engine…" />
  if (error && !risk) return <ErrorState message={error} onRetry={load} />
  const top = detections[0]
  return <div className="page"><PageHeader eyebrow="Phase 4 · Behavioral intelligence" title="AI Security Analytics" text="Authentication anomaly scoring, behavior analysis, and predictive threat classification." action={<button className="button secondary" onClick={load}><RefreshCw size={16}/>Refresh model feed</button>} /><section className="ai-analytics-grid"><RiskScoreCard score={risk?.risk_score || 10}/><article className="panel ai-confidence"><div className="ai-core"><BrainCircuit/><span>AI confidence</span><strong>{Math.min(99, (top?.risk_score || 10) + 7)}%</strong></div><div className="confidence-meter"><i style={{ width: `${Math.min(99, (top?.risk_score || 10) + 7)}%` }}/></div><p>{top?.behavior_summary || 'Baseline behavior established. No anomalous authentication patterns detected.'}</p><div className="ai-flags"><span><ScanSearch/>Anomaly {top?.threat_level === 'HIGH' ? 'detected' : 'monitoring'}</span><span><Sparkles/>Model online</span></div></article></section><article className="panel ai-chart-panel"><div className="panel-heading"><div><span className="eyebrow">Live inference stream</span><h2>Detection Risk Graph</h2></div><span className={`severity severity-${(risk?.risk_level || 'LOW').toLowerCase()}`}>{risk?.risk_level || 'LOW'}</span></div>{chart.length ? <div className="ai-chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={chart}><CartesianGrid stroke="#1b3043" vertical={false}/><XAxis dataKey="event" stroke="#60758a"/><YAxis domain={[0,100]} stroke="#60758a"/><Tooltip contentStyle={{background:'#091725',border:'1px solid #1c3044'}}/><Bar dataKey="risk" fill="#20d6bd" radius={[4,4,0,0]}/></BarChart></ResponsiveContainer></div> : <EmptyState title="No model results" message="Authentication activity will appear after the next login event."/>}</article></div>
}
