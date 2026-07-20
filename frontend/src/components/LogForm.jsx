import { useState } from 'react'
import { LoaderCircle, Plus, X } from 'lucide-react'

const initial = { event_type: 'failed_login', username: '', source_ip: '192.0.2.10', severity: 'medium', description: '' }

export default function LogForm({ open, onClose, onCreate, loading }) {
  const [form, setForm] = useState(initial)
  if (!open) return null
  const update = event => setForm(value => ({ ...value, [event.target.name]: event.target.value }))
  async function submit(event) {
    event.preventDefault()
    const success = await onCreate({ ...form, username: form.username || undefined })
    if (success) { setForm(initial); onClose() }
  }
  return <div className="modal-backdrop"><form className="log-form panel" onSubmit={submit}><div className="panel-heading"><div><span className="eyebrow">Pipeline test event</span><h2>Add security log</h2></div><button type="button" className="icon-button" onClick={onClose}><X size={18}/></button></div><div className="form-grid"><label>Event type<input name="event_type" value={form.event_type} onChange={update} required /></label><label>Username<input name="username" value={form.username} onChange={update} placeholder="Defaults to signed-in user" /></label><label>Source IP<input name="source_ip" value={form.source_ip} onChange={update} required /></label><label>Severity<select name="severity" value={form.severity} onChange={update}><option>low</option><option>medium</option><option>high</option><option>critical</option></select></label><label className="full-field">Description<textarea name="description" value={form.description} onChange={update} rows="4" maxLength="4000" placeholder="Describe the observed security event…" /></label></div><div className="form-actions"><button type="button" className="button secondary" onClick={onClose}>Cancel</button><button className="button primary" disabled={loading}>{loading ? <LoaderCircle className="spin" size={16}/> : <Plus size={16}/>}Create and analyze</button></div></form></div>
}
