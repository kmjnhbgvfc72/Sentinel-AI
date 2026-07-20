import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 12000,
  headers: { Accept: 'application/json' },
})

const TOKEN_KEY = 'sentinel_access_token'
const USER_KEY = 'sentinel_user'
const tokenStorage = () => localStorage.getItem(TOKEN_KEY) ? localStorage : sessionStorage

client.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem(TOKEN_KEY)
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

client.interceptors.response.use(
  (response) => response,
  (error) => Promise.reject({
    message: error.response?.data?.detail || error.message || 'The service is unavailable',
    status: error.response?.status,
  }),
)

const get = async (url, config) => (await client.get(url, config)).data
const post = async (url, data, config) => (await client.post(url, data, config)).data
const phase = (number, path) => `/api/v1/phase/${number}/${path.replace(/^\//, '')}`

export const authApi = {
  login: async (credentials) => {
    const { remember, ...payload } = credentials
    const session = await post('/api/auth/login', payload)
    const storage = remember ? localStorage : sessionStorage
    localStorage.removeItem(TOKEN_KEY); localStorage.removeItem(USER_KEY)
    sessionStorage.removeItem(TOKEN_KEY); sessionStorage.removeItem(USER_KEY)
    storage.setItem(TOKEN_KEY, session.access_token)
    storage.setItem(USER_KEY, JSON.stringify(session.user))
    return session
  },
  me: () => get('/api/auth/me'),
  logout: async () => {
    try { await post('/api/auth/logout') } finally {
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USER_KEY)
      sessionStorage.removeItem(TOKEN_KEY)
      sessionStorage.removeItem(USER_KEY)
    }
  },
  clearSession: () => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    sessionStorage.removeItem(TOKEN_KEY)
    sessionStorage.removeItem(USER_KEY)
  },
  hasToken: () => Boolean(localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem(TOKEN_KEY)),
  storedUser: () => {
    try { return JSON.parse(tokenStorage().getItem(USER_KEY)) } catch { return null }
  },
  storeUser: (user) => tokenStorage().setItem(USER_KEY, JSON.stringify(user)),
}

export const logApi = {
  list: (params) => get('/api/logs', { params }),
  create: (event) => post('/api/logs', event),
}

export const systemApi = {
  health: () => get('/api/v1/system/health'),
  overview: () => get('/api/v1/system/overview'),
  topology: () => get('/api/v1/system/topology'),
  synchronize: (limit = 20) => post(`/api/v1/pipeline/synchronize?limit=${limit}`),
}

export const threatApi = {
  security: (params = { limit: 8 }) => get('/api/threats', { params }),
  list: (params = { page_size: 50 }) => get(phase(3, '/api/threats'), { params }),
  statistics: () => get(phase(3, '/api/threat-statistics')),
  logs: (params = { page_size: 50 }) => get(phase(3, '/api/logs'), { params }),
  externalSummary: () => get(phase(7, '/api/intelligence/summary')),
  feeds: () => get(phase(7, '/api/feeds')),
  indicators: (params) => get(phase(7, '/api/ioc'), { params }),
}

export const riskApi = {
  current: () => get('/api/risk'),
}

export const securityOperationsApi = {
  detections: (limit = 8) => get('/api/detections', { params: { limit } }),
  attackPaths: (limit = 8) => get('/api/attack-paths', { params: { limit } }),
  incidents: (params = { limit: 8 }) => get('/api/incidents', { params }),
}

export const alertApi = {
  security: (params = { status: 'ACTIVE', limit: 50 }) => get('/api/alerts', { params }),
  list: (params = { limit: 50 }) => get(phase(2, '/api/alerts'), { params }),
  aiDetections: (params = { limit: 50 }) => get(phase(4, '/api/ai/alerts'), { params }),
  analyze: (event) => post(phase(4, '/api/ai/analyze'), event),
}

export const assetApi = {
  list: (params) => get(phase(2, '/api/assets'), { params }),
  foundationHealth: () => get(phase(1, '/api/v1/health')),
}

export const attackPathApi = {
  list: (params = { limit: 50 }) => get(phase(5, '/api/attack/paths'), { params }),
  analyze: (event) => post(phase(5, '/api/attack/analyze'), event),
}

export const soarApi = {
  incidents: (params) => get(phase(6, '/api/incidents'), { params }),
  playbooks: () => get(phase(6, '/api/playbooks')),
  notifications: () => get(phase(6, '/api/notifications')),
}

export const operationsApi = {
  readiness: () => get(phase(8, '/health/ready')),
  health: () => get(phase(8, '/health')),
}

export const huntingApi = {
  dashboard: () => get(phase(9, '/api/v1/analytics/dashboard')),
  hunts: (params) => get(phase(9, '/api/v1/hunts'), { params }),
}

export const reportsApi = {
  list: () => get(phase(2, '/api/reports')),
}

export const unwrapList = (payload, keys = []) => {
  if (Array.isArray(payload)) return payload
  for (const key of [...keys, 'data', 'items', 'results']) {
    const value = payload?.[key]
    if (Array.isArray(value)) return value
    if (Array.isArray(value?.data)) return value.data
  }
  return []
}

export default client
