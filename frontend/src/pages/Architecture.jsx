import { useCallback, useEffect, useState } from 'react'
import { Activity, CheckCircle2, RefreshCw } from 'lucide-react'
import { systemApi } from '../api/api'
import { ErrorState, LoadingState } from '../components/PageState'
import { PageHeader } from './Threats'

export default function Architecture() {
  const [health,setHealth]=useState(null); const [error,setError]=useState('')
  const load=useCallback(async()=>{try{setError('');setHealth(await systemApi.health())}catch(e){setError(e.message)}},[])
  useEffect(()=>{load();const timer=setInterval(load,30000);return()=>clearInterval(timer)},[load]); if(!health&&!error)return <LoadingState label="Mapping security fabric…"/>; if(!health)return <ErrorState message={error} onRetry={load}/>
  return <div className="page"><PageHeader eyebrow="Enterprise security fabric" title="Phase Architecture" text="Live connectivity across all nine defensive capabilities." action={<button className="button secondary" onClick={load}><RefreshCw size={16}/>Probe services</button>}/><section className="architecture-flow">{health.phases.map((phase,i)=><div className="architecture-node-wrap" key={phase.phase}><article className={`architecture-node ${phase.status}`}><span>PHASE {phase.phase}</span><div><strong>{phase.name}</strong><small>{phase.role}</small></div><i><CheckCircle2/>{phase.status==='healthy'?'CONNECTED':phase.status==='degraded'?'MONITORING':'STANDBY'}</i></article>{i<health.phases.length-1&&<div className="architecture-link"><Activity/></div>}</div>)}</section></div>
}
