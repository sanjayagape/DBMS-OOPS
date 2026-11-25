import type { DemoState, Donation } from '../types'
export const photo = (id: string, width = 800) => `https://images.unsplash.com/${id}?auto=format&fit=crop&w=${width}&q=85`
export const photos = {
  hero: photo('photo-1547592180-85f173990554', 1600),
  vegetables: photo('photo-1540420773420-3366772f4999'),
  bread: photo('photo-1509440159596-0249088772ff'),
  meal: photo('photo-1512621776951-a57141f2eefd'),
  fruit: photo('photo-1619566636858-adf3ef46400b'),
  pantry: photo('photo-1586201375761-83865001e31c'),
}
export function seedState(): DemoState {
  const now = new Date(); const later = (hours: number) => new Date(now.getTime() + hours * 3600000).toISOString()
  const common = { preparedAt: later(-1), createdAt: now.toISOString(), claimed: false, allergens: 'Please confirm ingredients with the donor before pickup.', dietary: 'Vegetarian' }
  const donations: Donation[] = [
    { ...common, id: 'food-1', name: 'Fresh from the garden', category: 'Fresh produce', description: 'A colorful mix of fresh, seasonal vegetables. Perfect for a hearty family meal. Washed and packed with care.', quantity: 12, unit: 'kg', location: 'Green Basket, 12 Church Street', area: 'Indiranagar', distance: 1.2, deadline: later(5), image: photos.vegetables, donor: 'Green Basket Market', dietary: 'Vegan' },
    { ...common, id: 'food-2', name: 'A little loaf of happiness', category: 'Bakery', description: 'Freshly baked sourdough, whole wheat loaves, and rolls from our morning batch. Ready for a second home.', quantity: 20, unit: 'loaves', location: 'The Bread House, 8 Main Road', area: 'Koramangala', distance: 2.4, deadline: later(7), image: photos.bread, donor: 'The Bread House', allergens: 'Contains wheat and gluten. May contain dairy and nuts.' },
    { ...common, id: 'food-3', name: 'Warm meals, warmer hearts', category: 'Cooked meals', description: 'Wholesome vegetable rice bowls, cooked today and packed in individual food-safe containers. Collect promptly and consume on the same day.', quantity: 35, unit: 'meals', location: 'Community Kitchen, 24 Lake Road', area: 'HSR Layout', distance: 3.1, deadline: later(3), image: photos.meal, donor: 'The Kind Kitchen', allergens: 'Contains soy. May contain nuts.' },
    { ...common, id: 'food-4', name: 'Seasonal fruit, shared freely', category: 'Fresh produce', description: 'Ripe fruit from our daily market surplus. A naturally sweet addition to community meals.', quantity: 8, unit: 'kg', location: 'Fresh Corner, 5 Market Street', area: 'Indiranagar', distance: 1.8, deadline: later(6), image: photos.fruit, donor: 'Fresh Corner', dietary: 'Vegan' },
    { ...common, id: 'food-5', name: 'Everyday pantry essentials', category: 'Pantry', description: 'Sealed packs of rice and lentils within their best-before dates. Store in a cool, dry place.', quantity: 15, unit: 'packs', location: 'Neighborhood Store, 10 Cross Road', area: 'Whitefield', distance: 8.5, deadline: later(24), image: photos.pantry, donor: 'Neighborhood Store', dietary: 'Vegan' },
    { ...common, id: 'food-6', name: 'Lunch with a little love', category: 'Cooked meals', description: 'Fresh vegetarian lunch boxes with seasonal vegetables. Kept refrigerated until collection.', quantity: 18, unit: 'meals', location: 'Good Table Cafe, 16 Park Lane', area: 'Koramangala', distance: 2.8, deadline: later(4), image: photos.meal, donor: 'Good Table Cafe' },
  ]
  return { donations, requests: [], user: null, verified: [], reports: [{ id: 'report-1', name: 'Sample listing report', reason: 'Pickup address needs clarification', resolved: false }], distributions: [{ id: 'distribution-1', name: 'Community lunch · HSR Layout', meals: 35, completed: false }] }
}
