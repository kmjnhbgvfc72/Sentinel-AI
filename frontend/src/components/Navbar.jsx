import { useEffect, useState } from 'react'
import { Bell, LogOut, Menu, Search, ShieldCheck } from 'lucide-react'
import { alertApi, logApi } from '../api/api'

export default function Navbar({ onMenu, user, onLogout }) {
  const [counts,setCounts]=useState({threats:0,critical:0})
  useEffect(()=>{let active=true;async function load(){const values=await Promise.allSettled([logApi.list({limit:1}),alertApi.security({status:'ACTIVE',limit:50})]);if(!active)return;const logs=values[0].status==='fulfilled'?values[0].value.total||0:0;const alerts=values[1].status==='fulfilled'?values[1].value.data||[]:[];setCounts({threats:logs,critical:alerts.filter(x=>['HIGH','CRITICAL'].includes(x.severity)).length})}load();const timer=setInterval(load,15000);return()=>{active=false;clearInterval(timer)}},[])
  return (
    <header className="navbar">
      <button className="icon-button mobile-menu" onClick={onMenu} aria-label="Open navigation"><Menu size={21} /></button>
      <div className="search-box">
        <Search size={18} />
        <input aria-label="Search security data" placeholder="Search threats, IPs, assets…" />
        <kbd>⌘ K</kbd>
      </div>
      <div className="navbar-actions">
        <span className="top-counter"><small>Threat events</small><strong>{counts.threats}</strong></span>
        <span className="top-counter critical"><small>Critical</small><strong>{counts.critical}</strong></span>
        <span className="live-indicator"><i /> Live monitoring</span>
        <button className="icon-button notification-button" aria-label={`${counts.critical} critical notifications`} title={`${counts.critical} critical alerts`}><Bell size={19} />{counts.critical>0&&<span />}</button>
        <div className="analyst-profile">
          <div className="avatar"><ShieldCheck size={19} /></div>
          <div><strong>{user?.username || 'SOC Analyst'}</strong><small>{user?.role || 'Analyst'}</small></div>
        </div>
        <button className="icon-button" onClick={onLogout} aria-label="Sign out" title="Sign out"><LogOut size={17}/></button>
      </div>
    </header>
  )
}
