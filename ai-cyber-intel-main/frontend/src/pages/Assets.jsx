import { useCallback, useEffect, useState } from 'react'
import { Database, Laptop, Network, Server } from 'lucide-react'
import { assetApi, unwrapList } from '../api/api'
import { EmptyState, ErrorState, LoadingState } from '../components/PageState'
import { PageHeader } from './Threats'

export default function Assets() {
  const [assets, setAssets] = useState([]); const [foundation, setFoundation] = useState(null); const [loading, setLoading] = useState(true); const [error, setError] = useState('')
  const load = useCallback(async () => { setLoading(true); const values = await Promise.allSettled([assetApi.list(), assetApi.foundationHealth()]); if (values[0].status === 'fulfilled') setAssets(unwrapList(values[0].value, ['assets'])); if (values[1].status === 'fulfilled') setFoundation(values[1].value); if (values.every(v => v.status === 'rejected')) setError(values[0].reason.message); setLoading(false) }, [])
  useEffect(() => { load() }, [load]); if (loading) return <LoadingState />; if (error) return <ErrorState message={error} onRetry={load} />
  return <div className="page"><PageHeader eyebrow="Phases 1 & 2" title="Asset Inventory" text="Protected infrastructure registered through the foundation and SOC APIs." /><div className="split-summary"><div><span>Managed assets</span><strong>{assets.length}</strong></div><div><span>Foundation API</span><strong className="text-green">{foundation ? 'Healthy' : 'Unavailable'}</strong></div><div><span>Database</span><strong>Connected</strong></div></div>{assets.length ? <section className="asset-table panel"><div className="table-head"><span>Asset</span><span>Type</span><span>Address</span><span>Risk</span><span>Status</span></div>{assets.map((asset, i) => <div className="table-row" key={asset.id || i}><span className="asset-name">{asset.type === 'server' ? <Server/> : asset.type === 'database' ? <Database/> : <Laptop/>}<strong>{asset.name || asset.hostname || `Asset ${i + 1}`}</strong></span><span>{asset.type || asset.asset_type || 'Endpoint'}</span><span>{asset.ip_address || asset.address || '—'}</span><span>{asset.risk_score ?? asset.risk_level ?? 'Low'}</span><span className="text-green">● {asset.status || 'Online'}</span></div>)}</section> : <EmptyState title="No assets returned" message="Start the Phase 2 asset service to populate this inventory." />}</div>
}
