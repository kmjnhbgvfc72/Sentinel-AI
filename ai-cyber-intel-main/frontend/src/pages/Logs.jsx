import { useCallback, useEffect, useState } from 'react'
import { Plus, Search } from 'lucide-react'
import { logApi } from '../api/api'
import LogForm from '../components/LogForm'
import LogTable from '../components/LogTable'
import { ErrorState, LoadingState } from '../components/PageState'
import { PageHeader } from './Threats'

export default function Logs() {
  const [logs, setLogs] = useState([]); const [total, setTotal] = useState(0); const [search, setSearch] = useState(''); const [severity, setSeverity] = useState(''); const [loading, setLoading] = useState(true); const [creating, setCreating] = useState(false); const [open, setOpen] = useState(false); const [error, setError] = useState(''); const [notice, setNotice] = useState('')
  const load = useCallback(async () => { setLoading(true); setError(''); try { const data = await logApi.list({ search: search || undefined, severity: severity || undefined, limit: 100 }); setLogs(data.data || []); setTotal(data.total || 0) } catch (requestError) { setError(requestError.message) } finally { setLoading(false) } }, [search, severity])
  useEffect(() => { const timer = setTimeout(load, 250); return () => clearTimeout(timer) }, [load])
  async function create(payload) { setCreating(true); setError(''); try { const result = await logApi.create(payload); const processed = Object.values(result.pipeline || {}).filter(item => ['processed', 'stored', 'available', 'observed'].includes(item.status)).length; setNotice(`Event stored and connected to ${processed} phase capabilities.`); await load(); return true } catch (requestError) { setError(requestError.message); return false } finally { setCreating(false) } }
  return <div className="page"><PageHeader eyebrow="Central security pipeline" title="Security Logs" text="Search security events and submit controlled test telemetry across Phases 1–9." action={<button className="button primary" onClick={() => setOpen(true)}><Plus size={16}/>Add test event</button>} />{notice && <div className="success-notice">{notice}<button onClick={() => setNotice('')}>×</button></div>}<div className="toolbar log-toolbar"><div className="filter-search"><Search size={17}/><input value={search} onChange={event => setSearch(event.target.value)} placeholder="Search event, username, IP, or description" /></div><select value={severity} onChange={event => setSeverity(event.target.value)}><option value="">All severities</option><option>low</option><option>medium</option><option>high</option><option>critical</option></select><span>{total} events</span></div>{loading ? <LoadingState/> : error ? <ErrorState message={error} onRetry={load}/> : <LogTable logs={logs}/>}<LogForm open={open} onClose={() => setOpen(false)} onCreate={create} loading={creating}/></div>
}
