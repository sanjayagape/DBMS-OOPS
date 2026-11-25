import type { DemoState, Donation, Role, User } from '../types'

let csrf: { token: string; headerName: string } | undefined
async function securityToken() {
  const response = await fetch('/api/auth/csrf', { credentials: 'same-origin', cache: 'no-store' })
  if (!response.ok) throw new Error('Unable to establish a secure connection. Please try again.')
  csrf = await response.json()
}
async function request<T>(path: string, method = 'GET', body?: unknown): Promise<T> {
  const mutation = method !== 'GET'
  if (mutation && !csrf) await securityToken()
  const response = await fetch(`/api${path}`, {
    method, credentials: 'same-origin', cache: 'no-store',
    headers: { ...(body !== undefined ? { 'Content-Type': 'application/json' } : {}), ...(mutation && csrf ? { [csrf.headerName]: csrf.token } : {}) },
    body: body === undefined ? undefined : JSON.stringify(body),
  })
  if (!response.ok) {
    if (response.status === 403 || response.status === 401) csrf = undefined
    const error = await response.json().catch(() => ({}))
    throw new Error(error.message || `The server could not complete this request (${response.status}).`)
  }
  return response.status === 204 ? undefined as T : response.json()
}
const unsupported = async (): Promise<DemoState> => { throw new Error('This feature is not available yet in connected mode.') }
export const backendApi = {
  load: () => request<DemoState>('/state'),
  async signIn(name: string, email: string, role: Role, password?: string, register = false) {
    const state = await request<DemoState>(register ? '/auth/register' : '/auth/login', 'POST', register ? { name, email, role, password } : { email, password })
    csrf = undefined
    return state
  },
  async signOut() { await request<void>('/auth/logout', 'POST'); csrf = undefined; return request<DemoState>('/state') },
  switchRole: async (_role: Role): Promise<DemoState> => { throw new Error('Your role belongs to your account. Sign in with another account to use a different role.') },
  updateProfile: (fields: Pick<User, 'name' | 'organization' | 'area'>) => request<DemoState>('/users/me', 'PATCH', fields),
  createDonation: (input: Omit<Donation, 'id' | 'claimed' | 'createdAt' | 'ownerId' | 'donor'>) => request<DemoState>('/donations', 'POST', input),
  requestFood: (id: string) => request<DemoState>(`/donations/${encodeURIComponent(id)}/claim`, 'POST'),
  acceptAssignment: (id: string) => request<DemoState>(`/pickups/${encodeURIComponent(id)}/accept`, 'POST'),
  advancePickup: (id: string) => request<DemoState>(`/pickups/${encodeURIComponent(id)}/advance`, 'POST'),
  withdrawDonation: (id: string) => request<DemoState>(`/donations/${encodeURIComponent(id)}`, 'DELETE'),
  verify: (_id: string) => unsupported(), resolveReport: (_id: string) => unsupported(), completeDistribution: (_id: string) => unsupported(),
}
