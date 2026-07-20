import { AlertTriangle, LoaderCircle, RefreshCw } from 'lucide-react'

export function LoadingState({ label = 'Loading security telemetry…' }) { return <div className="page-state"><LoaderCircle className="spin" /><p>{label}</p></div> }
export function ErrorState({ message, onRetry }) { return <div className="page-state error-state"><AlertTriangle /><h3>Unable to load live data</h3><p>{message}</p>{onRetry && <button className="button secondary" onClick={onRetry}><RefreshCw size={16} /> Try again</button>}</div> }
export function EmptyState({ title = 'No records found', message = 'There is no security data to display yet.' }) { return <div className="page-state"><h3>{title}</h3><p>{message}</p></div> }
