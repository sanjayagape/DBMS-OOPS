import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from 'react'
import type { DemoState } from '../types'
import { api } from '../services/api'
type Toast = { id: number; message: string; error: boolean }
interface AppContextValue { state: DemoState | null; loading: boolean; error: string; busy: boolean; toasts: Toast[]; notify: (message: string, error?: boolean) => void; run: (action: () => Promise<DemoState>, message?: string) => Promise<DemoState | null>; reload: () => void }
const AppContext = createContext<AppContextValue | null>(null)
export function AppProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<DemoState | null>(null)
  const [loading, setLoading] = useState(true); const [error, setError] = useState(''); const [busy, setBusy] = useState(false); const [toasts, setToasts] = useState<Toast[]>([])
  const notify = useCallback((message: string, error = false) => { const id = Date.now() + Math.random(); setToasts(t => [...t, { id, message, error }]); window.setTimeout(() => setToasts(t => t.filter(x => x.id !== id)), 5500) }, [])
  const reload = useCallback(() => { setLoading(true); setError(''); api.load().then(setState).catch(e => setError(e instanceof Error ? e.message : 'FoodBridge could not load. Please try again.')).finally(() => setLoading(false)) }, [])
  useEffect(reload, [reload])
  async function run(action: () => Promise<DemoState>, message?: string) { setBusy(true); try { const next = await action(); setState(next); if (message) notify(message); return next } catch (e) { notify(e instanceof Error ? e.message : 'Something went wrong. Please try again.', true); return null } finally { setBusy(false) } }
  return <AppContext.Provider value={{ state, loading, error, busy, toasts, notify, run, reload }}>{children}</AppContext.Provider>
}
export function useApp() { const value = useContext(AppContext); if (!value) throw new Error('AppProvider is required'); return value }
