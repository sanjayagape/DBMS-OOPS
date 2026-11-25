import test from 'node:test'
import assert from 'node:assert/strict'
import { seedState } from '../src/services/seed.ts'
import { advanceRequest, claimDonation, filterDonations } from '../src/services/logic.ts'
import type { User } from '../src/types/index.ts'
const user: User = { id:'test-user',name:'Test Neighbor',email:'test@example.com',role:'Citizen',organization:'',area:'Indiranagar' }
test('request reserves a donation, survives transitions, and completes once', () => {
  const seed = seedState(); const claimed = claimDonation(seed,'food-1',user)
  assert.equal(seed.requests.length,0); assert.equal(seed.donations[0].claimed,false)
  assert.equal(claimed.donations[0].claimed,true); assert.equal(claimed.requests[0].stage,1)
  assert.equal(claimed.requests[0].userId,user.id)
  assert.throws(() => claimDonation(claimed,'food-1',user),/already been claimed/)
  let state = claimed
  for (let stage = 2; stage <= 4; stage++) { state = advanceRequest(state,state.requests[0].id); assert.equal(state.requests[0].stage,stage); assert.equal(state.requests[0].timestamps.length,stage+1) }
  assert.throws(() => advanceRequest(state,state.requests[0].id),/already complete/)
})
test('expired and missing donations cannot be requested', () => {
  const state = seedState(); state.donations[0].deadline = '2000-01-01T00:00:00Z'
  assert.throws(() => claimDonation(state,'food-1',user),/window has closed/)
  assert.throws(() => claimDonation(state,'missing',user),/no longer available/)
  assert.throws(() => advanceRequest(state,'missing'),/could not be found/)
})
test('search, category, neighborhood, and distance compose without showing claimed or expired listings', () => {
  const state = seedState(); const filters = { search:'',category:'All food' as const,area:'All neighborhoods',distance:25 }
  assert.equal(filterDonations(state.donations,filters).length,6)
  assert.equal(filterDonations(state.donations,{ ...filters,search:'BREAD' })[0].id,'food-2')
  assert.equal(filterDonations(state.donations,{ ...filters,category:'Fresh produce',area:'Indiranagar',distance:1.5 }).length,1)
  assert.equal(filterDonations(state.donations,{ ...filters,search:'nowhere' }).length,0)
  state.donations[0].claimed = true; state.donations[1].deadline = '2000-01-01T00:00:00Z'
  assert.equal(filterDonations(state.donations,filters).length,4)
})
