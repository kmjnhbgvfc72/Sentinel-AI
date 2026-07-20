import { useState } from 'react'
import { Activity, BrainCircuit, Shield } from 'lucide-react'
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
      navigate(location.state?.from?.pathname || '/', { replace: true, state: { authenticationMessage: 'Authentication successful' } })
    } catch (requestError) {
      setError(requestError.status === 401 ? 'Invalid credentials' : requestError.message || 'Login failed. Check your credentials.')
    } finally { setLoading(false) }
  }

  return <main className="login-page"><div className="login-visual"><div className="visual-grid"/><div className="network-orbit orbit-one"/><div className="network-orbit orbit-two"/><div className="login-brand"><div className="brand-mark"><Shield size={28}/></div><div><strong>SENTINEL<span>AI</span></strong><small>AI Threat Intelligence System</small></div></div><div className="visual-copy"><span className="eyebrow"><i className="pulse-dot"/> Security monitoring active</span><h1>One secure view.<br/>Every threat signal.</h1><p>Authenticate to access real-time detection, attack prediction, advanced hunting, and automated response across all nine security phases.</p><div className="visual-features"><span><Activity/>Live security telemetry</span><span><BrainCircuit/>AI-powered correlation</span></div></div></div><section className="login-panel"><div className={`login-card ${loading ? 'authenticating' : ''}`}><div className="login-card-glow"/><span className="eyebrow">Authorized personnel only</span><h2>Secure SOC Access</h2><p>Sign in to the enterprise command center.</p><AuthForm onSubmit={login} error={error} loading={loading}/><small className="security-notice"><LockKeyholeSmall/>Zero-trust session · Security monitoring active</small></div></section></main>
}

function LockKeyholeSmall() { return <span aria-hidden="true">●</span> }
