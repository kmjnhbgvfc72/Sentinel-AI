import { useEffect, useState } from 'react'
import { Navigate, Route, Routes, useLocation } from 'react-router-dom'
import { authApi } from './api/api'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import Footer from './components/Footer'
import Dashboard from './pages/Dashboard'
import Threats from './pages/Threats'
import Alerts from './pages/Alerts'
import Assets from './pages/Assets'
import Reports from './pages/Reports'
import Settings from './pages/Settings'
import Login from './pages/Login'
import Logs from './pages/Logs'
import AIDetection from './pages/AIDetection'
import AttackGraph from './pages/AttackGraph'
import Incidents from './pages/Incidents'
import SystemHealth from './pages/SystemHealth'
import { LoadingState } from './components/PageState'

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [user, setUser] = useState(authApi.storedUser())
  const [checkingAuth, setCheckingAuth] = useState(authApi.hasToken())

  useEffect(() => {
    if (!authApi.hasToken()) { setCheckingAuth(false); return }
    authApi.me().then(current => { setUser(current); (localStorage.getItem('sentinel_access_token') ? localStorage : sessionStorage).setItem('sentinel_user', JSON.stringify(current)) }).catch(() => { authApi.logout(); setUser(null) }).finally(() => setCheckingAuth(false))
  }, [])

  function logout() { authApi.logout(); setUser(null) }
  if (checkingAuth) return <LoadingState label="Verifying secure session…" />

  return (
    <Routes>
      <Route path="/login" element={<Login authenticated={Boolean(user)} onLogin={session => setUser(session.user)} />} />
      <Route path="/*" element={<ProtectedRoute authenticated={Boolean(user)}><div className="app-shell">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="app-content">
        <Navbar onMenu={() => setSidebarOpen(true)} user={user} onLogout={logout} />
        <main className="page-container">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/logs" element={<Logs />} />
            <Route path="/threats" element={<Threats />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/ai-detection" element={<AIDetection />} />
            <Route path="/attack-graph" element={<AttackGraph />} />
            <Route path="/incidents" element={<Incidents />} />
            <Route path="/assets" element={<Assets />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/system-health" element={<SystemHealth />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </div></ProtectedRoute>} />
    </Routes>
  )
}

function ProtectedRoute({ authenticated, children }) {
  const location = useLocation()
  return authenticated ? children : <Navigate to="/login" state={{ from: location }} replace />
}
