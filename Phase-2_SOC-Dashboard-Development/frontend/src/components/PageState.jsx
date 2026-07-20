import { AlertTriangle, Inbox, LoaderCircle } from "lucide-react";

export function LoadingState({ label = "Loading security data" }) { return <div className="page-state" role="status"><LoaderCircle className="spin"/><p>{label}…</p></div>; }
export function ErrorState({ error, retry }) { return <div className="page-state error" role="alert"><AlertTriangle/><h3>Data unavailable</h3><p>{error?.message}</p><button className="button secondary" onClick={retry}>Retry</button></div>; }
export function EmptyState({ message = "No records match the current filters." }) { return <div className="page-state"><Inbox/><h3>No results</h3><p>{message}</p></div>; }
