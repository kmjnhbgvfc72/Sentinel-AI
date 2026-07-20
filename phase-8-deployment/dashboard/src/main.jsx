import React, {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from 'recharts';
import './styles.css';

const demo = [{time:'08:00',risk:22},{time:'09:00',risk:38},{time:'10:00',risk:71},{time:'11:00',risk:57},{time:'12:00',risk:86}];
function App(){
  const [threats,setThreats]=useState([]), [alerts,setAlerts]=useState([]);
  const token=sessionStorage.getItem('soc_token');
  useEffect(()=>{ if(!token)return; Promise.all(['/api/v1/threats?limit=8','/api/v1/alerts?limit=8'].map(u=>fetch(u,{headers:{Authorization:`Bearer ${token}`}}).then(r=>r.ok?r.json():[]))).then(([t,a])=>{setThreats(t);setAlerts(a)}); },[token]);
  const critical=threats.filter(t=>t.severity==='critical').length;
  return <main>
    <header><div><span className="eyebrow">AUTONOMOUS DEFENSE GRID</span><h1>AI Security Operations Center</h1></div><div className="status"><i/>SYSTEM OPERATIONAL</div></header>
    <section className="metrics"><Metric label="Active threats" value={threats.length||12} note={`${critical||3} critical`}/><Metric label="Global risk" value="86" note="Critical" danger/><Metric label="Open alerts" value={alerts.length||27} note="5 need review"/><Metric label="AI confidence" value="94%" note="Model online"/></section>
    <section className="grid"><article className="panel wide"><div className="title"><h2>Attack timeline</h2><span>Last 24 hours</span></div><ResponsiveContainer width="100%" height={250}><AreaChart data={demo}><defs><linearGradient id="risk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#24d6d0" stopOpacity=".5"/><stop offset="1" stopColor="#24d6d0" stopOpacity="0"/></linearGradient></defs><XAxis dataKey="time" stroke="#718398"/><YAxis stroke="#718398"/><Tooltip/><Area type="monotone" dataKey="risk" stroke="#24d6d0" fill="url(#risk)" strokeWidth={3}/></AreaChart></ResponsiveContainer></article>
    <article className="panel"><div className="title"><h2>AI prediction</h2><span className="tag">NEXT 6H</span></div><div className="prediction"><strong>Credential pivot likely</strong><p>Identity anomaly may reach the production cluster through an exposed admin service.</p><b>78% confidence</b></div><button>Review attack path</button></article>
    <article className="panel wide"><div className="title"><h2>Active threats</h2><span>Live telemetry</span></div><table><thead><tr><th>Source</th><th>Category</th><th>Severity</th><th>Risk</th></tr></thead><tbody>{(threats.length?threats:[{source_ip:'185.220.101.4',category:'Command & control',severity:'critical',risk_score:94},{source_ip:'10.4.8.22',category:'Lateral movement',severity:'high',risk_score:79},{source_ip:'45.33.32.156',category:'Reconnaissance',severity:'medium',risk_score:51}]).map((t,i)=><tr key={t.id||i}><td>{t.source_ip||t.source}</td><td>{t.category}</td><td><span className={`sev ${t.severity}`}>{t.severity}</span></td><td>{t.risk_score}</td></tr>)}</tbody></table></article>
    <article className="panel"><div className="title"><h2>Recommended actions</h2></div><ol><li><b>Isolate endpoint SOC-WS-22</b><small>Contain suspected lateral movement</small></li><li><b>Rotate privileged credentials</b><small>Identity risk exceeds threshold</small></li><li><b>Block malicious infrastructure</b><small>IOC confidence 98%</small></li></ol></article></section>
  </main>}
function Metric({label,value,note,danger}) {return <article className="metric"><span>{label}</span><strong className={danger?'danger':''}>{value}</strong><small>{note}</small></article>}
createRoot(document.getElementById('root')).render(<App/>);

