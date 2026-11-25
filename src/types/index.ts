export type Role = 'Citizen' | 'Food Donor' | 'NGO' | 'Volunteer' | 'Administrator'
export const roles: Role[] = ['Citizen', 'Food Donor', 'NGO', 'Volunteer', 'Administrator']
export const stages = ['Donation Created', 'Claimed', 'Volunteer Assigned', 'Picked Up', 'Delivered'] as const
export type Category = 'All food' | 'Cooked meals' | 'Fresh produce' | 'Bakery' | 'Pantry'
export interface Donation {
  id: string; name: string; category: Exclude<Category, 'All food'>; description: string;
  quantity: number; unit: string; location: string; area: string; distance: number;
  preparedAt: string; deadline: string; image: string; donor: string; dietary: string;
  allergens: string; ownerId?: string; claimed: boolean; createdAt: string;
}
export interface FoodRequest { id: string; donationId: string; userId: string; recipient: string; stage: number; createdAt: string; timestamps: string[]; volunteerId?: string }
export interface User { id: string; name: string; email: string; role: Role; organization: string; area: string }
export interface DemoState { donations: Donation[]; requests: FoodRequest[]; user: User | null; verified: string[]; reports: { id: string; name: string; reason: string; resolved: boolean }[]; distributions: { id: string; name: string; meals: number; completed: boolean }[] }
