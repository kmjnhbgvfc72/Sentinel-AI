import { Clock3, UserRound } from 'lucide-react'
import { formatDate } from './ThreatCard'
import { EmptyState } from './PageState'

export default function LogTable({ logs }) {
  if (!logs.length) return <EmptyState title="No security logs found" message="Add a test event or change the active filters." />
  return <div className="log-table panel"><div className="log-table-head"><span>Event type</span><span>Username</span><span>Source IP</span><span>Severity</span><span>Timestamp</span></div>{logs.map(log => <div className="log-table-row" key={log.id}><span><strong>{log.event_type}</strong><small>{log.description || 'No additional description'}</small></span><span><UserRound size={13}/>{log.username}</span><span className="mono">{log.source_ip}</span><span><i className={`severity severity-${log.severity}`}>{log.severity}</i></span><span><Clock3 size={13}/>{formatDate(log.timestamp)}</span></div>)}</div>
}
