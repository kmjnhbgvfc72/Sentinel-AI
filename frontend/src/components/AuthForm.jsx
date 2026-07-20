import { useState } from 'react'
import { Eye, EyeOff, LoaderCircle, LockKeyhole, User } from 'lucide-react'

export default function AuthForm({ onSubmit, error, loading }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [remember, setRemember] = useState(false)

  function submit(event) {
    event.preventDefault()
    if (!username.trim() || !password) return
    onSubmit({ username: username.trim(), password, remember })
  }

  return <form className="auth-form" onSubmit={submit}>
    {error && <div className="auth-error" role="alert">{error}</div>}
    <label>Username<div className="auth-input"><User size={17}/><input name="username" value={username} onChange={event => setUsername(event.target.value)} autoComplete="username" autoFocus required placeholder="Enter your username" /></div></label>
    <label>Password<div className="auth-input"><LockKeyhole size={17}/><input name="password" type={showPassword ? 'text' : 'password'} value={password} onChange={event => setPassword(event.target.value)} autoComplete="current-password" required placeholder="Enter your password" /><button type="button" onClick={() => setShowPassword(value => !value)} aria-label={showPassword ? 'Hide password' : 'Show password'}>{showPassword ? <EyeOff size={16}/> : <Eye size={16}/>}</button></div></label>
    <label className="remember-session"><input type="checkbox" checked={remember} onChange={event => setRemember(event.target.checked)} /><span>Remember secure session on this device</span></label>
    <button className="button primary auth-submit" disabled={loading}>{loading ? <LoaderCircle className="spin" size={17}/> : <LockKeyhole size={17}/>} {loading ? 'Authenticating…' : 'Sign in to SOC'}</button>
  </form>
}
