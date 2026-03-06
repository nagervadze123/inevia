'use client'

import { useEffect, useMemo, useState } from 'react'
import { useParams } from 'next/navigation'

import { api } from '@/lib/api'

type Tab = 'opps' | 'strategy' | 'assets' | 'listings' | 'distribution' | 'runs'

export default function ProjectPage() {
  const { id } = useParams<{ id: string }>()
  const [tab, setTab] = useState<Tab>('opps')
  const [data, setData] = useState<any>({ opps: [], strategy: null, assets: [], listings: [], cals: [], runs: [], project: null })
  const [loading, setLoading] = useState(true)
  const [buildLoading, setBuildLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = async () => {
    setLoading(true)
    setError(null)
    try {
      const [project, opps, strategy, assets, listings, cals, runs] = await Promise.all([
        api(`/api/projects/${id}`).catch(() => null),
        api(`/api/projects/${id}/opportunities`).catch(() => []),
        api(`/api/projects/${id}/strategy`).catch(() => null),
        api(`/api/projects/${id}/assets`).catch(() => []),
        api(`/api/projects/${id}/listings`).catch(() => []),
        api(`/api/projects/${id}/content-calendars`).catch(() => []),
        api(`/api/projects/${id}/runs`).catch(() => []),
      ])
      setData({ project, opps, strategy, assets, listings, cals, runs })
    } catch (err: any) {
      setError(err.message || 'Failed to load project data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [id])

  useEffect(() => {
    const timer = setInterval(() => {
      load()
    }, 3000)
    return () => clearInterval(timer)
  }, [id])

  const runBuildAll = async () => {
    setBuildLoading(true)
    setError(null)
    try {
      await api(`/api/projects/${id}/run`, {
        method: 'POST',
        body: JSON.stringify({ run_type: 'build_all', opportunity_ids: [] }),
      })
      await load()
    } catch (err: any) {
      setError(err.message || 'Build failed')
    } finally {
      setBuildLoading(false)
    }
  }

  const latestRun = useMemo(() => (data.runs?.length ? data.runs[0] : null), [data.runs])

  return (
    <div className='space-y-4'>
      <div className='flex items-center justify-between'>
        <h1 className='text-xl font-semibold'>{data.project?.name || `Project ${id}`}</h1>
        <button className='border px-3 py-2 rounded disabled:opacity-50' onClick={runBuildAll} disabled={buildLoading}>
          {buildLoading ? 'Starting Build...' : 'Build All'}
        </button>
      </div>

      {latestRun?.status === 'running' && <p className='text-amber-300'>Workflow running... refreshing tabs automatically.</p>}
      {error && <p className='text-red-400 whitespace-pre-wrap'>{error}</p>}

      <div className='flex gap-2'>
        {(['opps', 'strategy', 'assets', 'listings', 'distribution', 'runs'] as Tab[]).map((t) => (
          <button key={t} className={`border px-2 py-1 rounded ${tab === t ? 'bg-slate-800' : ''}`} onClick={() => setTab(t)}>
            {t}
          </button>
        ))}
      </div>

      {loading ? <p>Loading...</p> : null}

      {tab === 'opps' && (
        <div className='grid md:grid-cols-2 gap-3'>
          {(data.opps || []).map((o: any) => {
            const d = o.differentiation_json || {}
            return (
              <div key={o.id} className='border rounded p-3 space-y-1'>
                <h3 className='font-semibold'>{o.title}</h3>
                <p className='text-sm text-slate-300'>{d.description || 'No description available yet.'}</p>
                <p className='text-sm'>Demand: {o.demand_score} | Competition: {o.competition_score} | Profit: {o.profit_score}</p>
                <p className='text-sm'>Format: {d.suggested_format || d.suggested_formats?.[0] || 'TBD'} | Price: {d.price_range || d.suggested_price_range || 'TBD'}</p>
              </div>
            )
          })}
          {data.opps?.length === 0 && <p>No opportunities yet. Click Build All.</p>}
        </div>
      )}

      {tab === 'strategy' && (
        <div className='space-y-2'>
          <pre className='whitespace-pre-wrap'>{JSON.stringify(data.strategy?.strategy_json || {}, null, 2)}</pre>
        </div>
      )}

      {tab === 'assets' && (
        <div className='space-y-2'>
          {(data.assets || []).map((a: any) => (
            <div key={a.id} className='border rounded p-3'>
              <p className='font-medium'>{a.asset_type}</p>
              <pre className='text-xs whitespace-pre-wrap'>{JSON.stringify(a.meta_json, null, 2)}</pre>
              <a className='underline' href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/assets/${a.id}/download`}>
                Download
              </a>
            </div>
          ))}
          {data.assets?.length === 0 && <p>No assets yet. Click Build All.</p>}
        </div>
      )}

      {tab === 'listings' && (
        <div className='space-y-3'>
          {(data.listings || []).map((l: any) => (
            <div key={l.id} className='border rounded p-3'>
              <h3 className='font-semibold'>{l.platform.toUpperCase()}</h3>
              <pre className='text-xs whitespace-pre-wrap'>{JSON.stringify(l.listing_json, null, 2)}</pre>
            </div>
          ))}
          {data.listings?.length === 0 && <p>No listings yet. Click Build All.</p>}
        </div>
      )}

      {tab === 'distribution' && (
        <div className='space-y-3'>
          {(data.cals || []).map((c: any) => (
            <div key={c.id} className='border rounded p-3'>
              <h3 className='font-semibold'>{c.platform} · {c.month}</h3>
              <pre className='text-xs whitespace-pre-wrap'>{JSON.stringify(c.calendar_json, null, 2)}</pre>
            </div>
          ))}
          {data.cals?.length === 0 && <p>No calendars yet. Click Build All.</p>}
        </div>
      )}

      {tab === 'runs' && (
        <div className='space-y-2'>
          {(data.runs || []).map((r: any) => (
            <div key={r.id} className='border rounded p-3'>
              <p>run_type: {r.run_type}</p>
              <p>status: {r.status}</p>
              <p>started_at: {r.started_at || 'N/A'}</p>
              <p>finished_at: {r.finished_at || 'N/A'}</p>
              <pre className='text-xs whitespace-pre-wrap'>error_json: {JSON.stringify(r.error_json, null, 2)}</pre>
            </div>
          ))}
          {data.runs?.length === 0 && <p>No runs yet.</p>}
        </div>
      )}
    </div>
  )
}
