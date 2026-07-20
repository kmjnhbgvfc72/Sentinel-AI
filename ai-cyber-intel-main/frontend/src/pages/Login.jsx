import { useState } from 'react'
import { Activity, BrainCircuit, Shield, ShieldCheck } from 'lucide-react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { authApi } from '../api/api'
import AuthForm from '../components/AuthForm'

export default function Login({ authenticated, onLogin }) {
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  if (authenticated) return <Navigate to="/" replace />

  async function login(credentials) {
    setLoading(true); setError('')
    try {
      const session = await authApi.login(credentials)
      onLogin(session)
      navigate(location.state?.from?.pathname || '/', { replace: true })
    } catch (requestError) {
      setError(requestError.message || 'Login failed. Check your credentials.')
    } finally { setLoading(false) }
  }

  return <main className="login-page"><div className="login-visual"><div className="visual-grid"/><div className="network-orbit orbit-one"/><div className="network-orbit orbit-two"/><div className="login-brand"><div className="brand-mark"><Shield size={28}/></div><strong>SENTINEL<span>AI</span></strong></div><div className="visual-copy"><span className="eyebrow">AI Threat Intelligence System</span><h1>One secure view.<br/>Every threat signal.</h1><p>Authenticate to access detection, prediction, hunting, and automated response across all nine security phases.</p><div className="visual-features"><span><Activity/>Security monitoring active</span><span><BrainCircuit/>AI-powered correlation</span><span><ShieldCheck/>Protected access</span></div></div></div><section className="login-panel"><div className="login-card"><span className="eyebrow">Authorized personnel only</span><h2>Welcome back</h2><p>Sign in to the Security Operations Center.</p><AuthForm onSubmit={login} error={error} loading={loading}/><small className="security-notice"><LockKeyholeSmall/>Credentials are transmitted only to the central API.</small></div></section></main>
}

function LockKeyholeSmall() { return <span aria-hidden="true">●</span> }
