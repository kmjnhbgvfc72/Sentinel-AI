import { Bell, CheckCheck, LogOut, Menu, Search, ShieldAlert, ShieldCheck } from 'lucide-react'
import { useCallback, useEffect, useRef, useState } from 'react'
import { notificationApi } from '../api/api'

export default function Navbar({ onMenu, user, onLogout }) {
  const [open, setOpen] = useState(false); const [items, setItems] = useState([]); const [unread, setUnread] = useState(0); const menuRef = useRef(null)
  const load = useCallback(async () => { try { const result = await notificationApi.list(); setItems(result.data || []); setUnread(result.unread_count || 0) } catch {} }, [])
  useEffect(() => { load(); const timer = setInterval(load, 30000); return () => clearInterval(timer) }, [load])
  useEffect(() => { const close = event => { if (!menuRef.current?.contains(event.target)) setOpen(false) }; document.addEventListener('mousedown', close); return () => document.removeEventListener('mousedown', close) }, [])
  async function read(item) { if (!item.is_read) { try { await notificationApi.markRead(item.id); await load() } catch {} } }
  return (
    <header className="navbar">
      <button className="icon-button mobile-menu" onClick={onMenu} aria-label="Open navigation"><Menu size={21} /></button>
      <div className="search-box">
        <Search size={18} />
        <input aria-label="Search security data" placeholder="Search threats, IPs, assets…" />
        <kbd>⌘ K</kbd>
      </div>
      <div className="navbar-actions">
        <span className="live-indicator"><i /> Live telemetry</span>
        <div className="notification-menu" ref={menuRef}><button className="icon-button notification-button" aria-label="Notifications" onClick={() => { setOpen(value => !value); if (!open) load() }}><Bell size={19} />{unread > 0 && <span>{unread > 9 ? '9+' : unread}</span>}</button>{open && <div className="notification-dropdown"><div className="notification-heading"><div><span className="eyebrow">Live security events</span><strong>Notifications</strong></div><span>{unread} unread</span></div><div className="notification-list">{items.length ? items.slice(0, 7).map(item => <button className={`notification-item ${item.is_read ? 'read' : ''}`} key={item.id} onClick={() => read(item)}><ShieldAlert/><div><strong>{item.title}</strong><p>{item.message}</p><small><b className={`severity severity-${item.severity}`}>{item.severity}</b>{item.related_user || 'SOC system'} · {new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</small></div>{!item.is_read && <i/>}</button>) : <div className="notification-empty"><CheckCheck/>No new security notifications</div>}</div></div>}</div>
        <div className="analyst-profile">
          <div className="avatar"><ShieldCheck size={19} /></div>
          <div><strong>{user?.username || 'SOC Analyst'}</strong><small>{user?.role || 'Analyst'}</small></div>
        </div>
        <button className="icon-button" onClick={onLogout} aria-label="Sign out" title="Sign out"><LogOut size={17}/></button>
      </div>
    </header>
  )
}
