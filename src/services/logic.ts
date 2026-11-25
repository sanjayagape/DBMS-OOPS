import type { Category, Donation, DemoState, User } from '../types/index.ts'
export function filterDonations(items: Donation[], filters: { search: string; category: Category; area: string; distance: number }) {
  return items.filter(d => !d.claimed && new Date(d.deadline).getTime() > Date.now() && (filters.category === 'All food' || d.category === filters.category) && (filters.area === 'All neighborhoods' || d.area === filters.area) && d.distance <= filters.distance && `${d.name} ${d.donor} ${d.location} ${d.area}`.toLowerCase().includes(filters.search.toLowerCase()))
}
export function claimDonation(state: DemoState, donationId: string, user: User): DemoState {
  const donation = state.donations.find(d => d.id === donationId)
  if (!donation) throw new Error('This donation is no longer available.')
  if (donation.claimed) throw new Error('This food has already been claimed.')
  if (new Date(donation.deadline).getTime() <= Date.now()) throw new Error('The pickup window has closed.')
  const now = new Date().toISOString()
  return { ...state, donations: state.donations.map(d => d.id === donationId ? { ...d, claimed: true } : d), requests: [...state.requests, { id: crypto.randomUUID(), donationId, userId: user.id, recipient: user.name, stage: 1, createdAt: now, timestamps: [donation.createdAt, now] }] }
}
export function advanceRequest(state: DemoState, id: string): DemoState {
  const request = state.requests.find(r => r.id === id)
  if (!request) throw new Error('Request could not be found.')
  if (request.stage >= 4) throw new Error('This delivery is already complete.')
  return { ...state, requests: state.requests.map(r => r.id === id ? { ...r, stage: r.stage + 1, timestamps: [...r.timestamps, new Date().toISOString()] } : r) }
}
