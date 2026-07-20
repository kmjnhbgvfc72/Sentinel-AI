import { Clock3, MapPin, MonitorSmartphone, UserRound } from 'lucide-react'
import { formatDate } from './ThreatCard'
import { EmptyState } from './PageState'

export default function LogTable({ logs }) {
  if (!logs.length) return <EmptyState title="No security logs found" message="Add a test event or change the active filters." />
  return <div className="log-table panel"><div className="log-table-head"><span>Event</span><span>User / IP</span><span>Device</span><span>Location</span><span>Risk</span><span>Time</span></div>{logs.map(log => { const state=(log.status || log.severity || 'unknown').toLowerCase(); return <div className={`log-table-row event-${state}`} key={log.id}><span><strong><i className={`event-state state-${state}`}/>{log.event_type} {log.status || ''}</strong><small>{log.failure_reason || log.description || 'Security event collected'}</small></span><span><UserRound size={13}/><span>{log.username}<small className="mono">{log.ip_address || log.source_ip}</small></span></span><span title={log.device_information || log.user_agent || ''}><MonitorSmartphone size={13}/>{shortDevice(log.device_information || log.user_agent)}</span><span><MapPin size={13}/>{log.location_information || 'Not enriched'}</span><span><i className={`severity severity-${log.severity}`}>{log.severity}</i></span><span><Clock3 size={13}/>{formatDate(log.created_at || log.timestamp)}</span></div>})}</div>
}

function shortDevice(value) { if (!value) return 'Unknown device'; if (/mobile|android|iphone/i.test(value)) return 'Mobile device'; if (/windows/i.test(value)) return 'Windows workstation'; if (/linux/i.test(value)) return 'Linux workstation'; if (/macintosh|mac os/i.test(value)) return 'Apple workstation'; return 'Web client' }
