import type { DemoState, Donation, Role, User } from '../types'
import { seedState } from './seed'
import { advanceRequest, claimDonation } from './logic'
import { backendApi } from './backendApi'
export const backendEnabled = import.meta.env.VITE_API_MODE === 'backend'
const KEY = 'foodbridge-demo-v1'
const delay = () => new Promise(resolve => setTimeout(resolve, 250))
function read(): DemoState {
  try { const saved = localStorage.getItem(KEY); if (saved) { const state = JSON.parse(saved); if (Array.isArray(state.donations) && Array.isArray(state.requests) && Array.isArray(state.verified) && Array.isArray(state.reports) && Array.isArray(state.distributions)) return state } } catch { /* Recover from corrupt demo storage. */ }
  return seedState()
}
function save(state: DemoState) { try { localStorage.setItem(KEY, JSON.stringify(state)) } catch { throw new Error('Your browser could not save this demo. Free some storage and try again.') }; return state }
// Replace these methods with fetch calls to Spring Boot. No real authentication or network writes occur.
const demoApi = {
  async load() { await delay(); return read() },
  async signIn(name: string, email: string, role: Role, _password?: string, _register?: boolean) { await delay(); const state = read(); const user: User = { id: `demo-${email.toLowerCase()}`, name, email, role, organization: '', area: 'Indiranagar' }; return save({ ...state, user }) },
  async switchRole(role: Role) { await delay(); const state = read(); const user = state.user ?? { id: 'demo-community', name: 'Alex Morgan', email: 'alex@example.com', organization: '', area: 'Indiranagar' }; return save({ ...state, user: { ...user, role } }) },
  async signOut() { await delay(); return save({ ...read(), user: null }) },
  async updateProfile(fields: Pick<User, 'name' | 'organization' | 'area'>) { await delay(); const state = read(); if (!state.user) throw new Error('Choose a demo role or sign in first.'); return save({ ...state, user: { ...state.user, ...fields } }) },
  async createDonation(input: Omit<Donation, 'id' | 'claimed' | 'createdAt' | 'ownerId' | 'donor'>) { await delay(); const state = read(); if (!state.user) throw new Error('Please enter the demo before sharing food.'); return save({ ...state, donations: [{ ...input, id: crypto.randomUUID(), claimed: false, ownerId: state.user.id, donor: state.user.organization || state.user.name, createdAt: new Date().toISOString() }, ...state.donations] }) },
  async requestFood(id: string) { await delay(); const state = read(); if (!state.user) throw new Error('Please sign in to the demo before requesting food.'); return save(claimDonation(state, id, state.user)) },
  async advancePickup(id: string) { await delay(); return save(advanceRequest(read(), id)) },
  async acceptAssignment(id: string) { await delay(); const state = read(); const request = state.requests.find(r => r.id === id); if (!state.user || state.user.role !== 'Volunteer') throw new Error('Choose the Volunteer role to accept a pickup.'); if (!request || request.stage !== 1) throw new Error('This pickup is no longer available.'); return save({ ...state, requests: state.requests.map(r => r.id === id ? { ...r, stage: 2, volunteerId: state.user!.id, timestamps: [...r.timestamps, new Date().toISOString()] } : r) }) },
  async withdrawDonation(id: string) { await delay(); const state = read(); const donation = state.donations.find(d => d.id === id); if (!donation || donation.ownerId !== state.user?.id) throw new Error('Only your own listings can be withdrawn.'); if (donation.claimed) throw new Error('Claimed donations cannot be withdrawn.'); return save({ ...state, donations: state.donations.filter(d => d.id !== id) }) },
  async verify(id: string) { await delay(); const state = read(); return save({ ...state, verified: [...new Set([...state.verified, id])] }) },
  async resolveReport(id: string) { await delay(); const state = read(); return save({ ...state, reports: state.reports.map(r => r.id === id ? { ...r, resolved: true } : r) }) },
  async completeDistribution(id: string) { await delay(); const state = read(); return save({ ...state, distributions: state.distributions.map(d => d.id === id ? { ...d, completed: true } : d) }) },
}
export const api = backendEnabled ? backendApi : demoApi
