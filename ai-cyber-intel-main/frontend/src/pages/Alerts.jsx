import { useCallback, useEffect, useState } from 'react'
import { RefreshCw } from 'lucide-react'
import { alertApi, soarApi, unwrapList } from '../api/api'
import AlertCard from '../components/AlertCard'
import { EmptyState, ErrorState, LoadingState } from '../components/PageState'
import { PageHeader } from './Threats'

export default function Alerts() {
  const [alerts, setAlerts] = useState([]); const [incidents, setIncidents] = useState([]); const [loading, setLoading] = useState(true); const [error, setError] = useState('')
  const load = useCallback(async () => { setLoading(true); setError(''); const values = await Promise.allSettled([alertApi.aiDetections(), alertApi.list(), soarApi.incidents()]); const ai = values[0].status === 'fulfilled' ? unwrapList(values[0].value, ['alerts', 'detections']) : []; const soc = values[1].status === 'fulfilled' ? unwrapList(values[1].value, ['alerts']) : []; setAlerts(ai.length ? ai : soc); if (values[2].status === 'fulfilled') setIncidents(unwrapList(values[2].value, ['incidents'])); if (values.every(x => x.status === 'rejected')) setError(values[0].reason.message); setLoading(false) }, [])
  useEffect(() => { load() }, [load]); if (loading) return <LoadingState />; if (error) return <ErrorState message={error} onRetry={load} />
  return <div className="page"><PageHeader eyebrow="Phases 2, 4 & 6" title="Alerts & AI Detections" text="Detection decisions linked to automated incident response." action={<button className="button secondary" onClick={load}><RefreshCw size={16}/>Refresh</button>} /><div className="split-summary"><div><span>AI alerts</span><strong>{alerts.length}</strong></div><div><span>SOAR incidents</span><strong>{incidents.length}</strong></div><div><span>Automation</span><strong className="text-green">Enabled</strong></div></div><section className="panel list-panel"><div className="panel-heading"><div><span className="eyebrow">Detection queue</span><h2>Prioritized alerts</h2></div></div>{alerts.length ? alerts.map((alert, i) => <AlertCard key={alert.id || i} alert={alert}/>) : <EmptyState title="No active alerts" message="The AI detection queue is clear." />}</section></div>
}
