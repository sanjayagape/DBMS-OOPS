# FoodBridge

A complete React + TypeScript frontend for a surplus food rescue platform. Warm cream, forest green, realistic food photography, frosted interactive controls, responsive layouts, and role-specific demo journeys.

**Two modes:** the default browser demo and an optional Spring Boot + MySQL backend. See [backend setup](backend/README.md) for connected mode. In the default demo, Authentication is simulated; passwords are neither saved nor checked. Email resets, notifications, requests, verification, and deliveries do not contact real services. Demo profiles, listings, requests, and admin actions persist in this browser’s localStorage. All platform impact statistics and testimonials are explicitly illustrative.

## Run in VS Code

1. Install Node.js 22.12+ (Node 24 recommended), which includes npm.
2. Open this folder in VS Code and open its terminal.
3. Run `npm install` (or `pnpm install` to use the included lockfile).
4. Run `npm run dev` and open the Local URL shown by Vite, normally `http://127.0.0.1:5173`.
5. Run `npm run build` for TypeScript validation and the production build. Run `npm run preview` to serve the production build, normally on port 4173.
6. Run `npm test` for reservation, expiration, filtering, and pickup lifecycle tests. This test command uses Node's TypeScript stripping; use Node 22.12+.

If PowerShell blocks npm.ps1, use `npm.cmd` instead. pnpm users can use `pnpm dev`, `pnpm build`, `pnpm preview`, and `pnpm test`.

## Explore the demo

- **Home:** photography-led landing page, three-step guide, available food, sample impact, SDG context, and illustrative testimonials.
- **Explore:** case-insensitive search, category and neighborhood filtering, distance slider, details dialog, dietary and allergen information, and request flow. Claimed and expired food is hidden from discovery.
- **Donate:** four-step validated wizard; details, sample or uploaded photo, quantity, pickup address and times, safety confirmation, and review. Uploaded images are limited to 2 MB and stored locally.
- **Authentication:** login, registration, five-role selection, reset preview, and profile setup. Any valid-looking email and password of at least eight characters can enter the demo. Do not enter a real password.
- **Dashboards:** switch roles in the demo bar at the bottom of each page. Each role has distinct navigation and actions.
  - Citizen: discover, request, track, and see local activity.
  - Donor: create and withdraw own unclaimed listings; review claims, pickups, and completed history.
  - NGO: discover and claim food, confirm receipt, and complete a sample distribution.
  - Volunteer: accept requested food pickups; track assigned and completed deliveries.
  - Administrator: sample user suspension, verification, report resolution, donation monitoring, and analytics. This is freely accessible demo UI, not real authorization.
- **Tracking:** Donation Created → Claimed → Volunteer Assigned → Picked Up → Delivered. Each change adds a timestamp; the final stage displays confirmation.
- **Impact:** six labeled sample metrics, two Recharts charts, a period selector, and separate actual local demo counts.
- **Onboarding:** three-step welcome experience, splash-style branded introduction, and skip/continue navigation.

Try a full journey: choose **Food Donor**, create a donation, switch to **Citizen** and request it, switch to **Volunteer** and accept the assignment, then open tracking and simulate pickup/delivery. The shared demo identity keeps role switching convenient; real users and permissions must be enforced by the future backend.

## Project structure

```text
public/                 App icon assets
src/
  components/           Layout, navigation, cards, dialog, photo fallback, toasts
  hooks/                Shared application state, loading, errors, mutations
  pages/                Home, Explore, Donate, Auth, Dashboard, Tracking, Impact, Onboarding
  services/             Mock API boundary, seeded data/photography, pure flow logic
  types/                TypeScript interfaces, role and status definitions
  App.tsx               Lazy-loaded routes, transitions, error boundary
  main.tsx              App bootstrap and service worker registration
  styles.css            Tailwind entry, design tokens, responsive component styles
scripts/                App icon generation helper
tests/                  Meaningful lifecycle and filter tests
vite.config.ts          React, Tailwind, and PWA configuration
```

## PWA and offline behavior

The production build generates a web manifest and Workbox service worker. App shell files are precached; previously loaded Unsplash images use a bounded runtime cache. Unavailable photos have a text fallback. All demo data is local, so there is no server synchronization.

Test PWA installation using the production preview. The worker is not enabled in normal development. Installation requires HTTPS in deployment (localhost is allowed for development) and browser support. Chromium can offer Install app; iOS Safari uses Share → Add to Home Screen. The footer’s install control uses the install prompt when supported and otherwise explains manual installation. This is a web app, not a native Android APK. Cached app routes can work offline after a successful initial visit; new uncached external photos require connectivity.

Deploy `dist/` on a static host with SPA fallback to `index.html`. Serve at the domain root or adjust Vite base, router basename, and manifest scope/start URL together. Keep the service worker at app scope.

## Spring Boot integration

The HTTP adapter in `src/services/backendApi.ts` is enabled by `VITE_API_MODE=backend`. It preserves the page state interface for accounts, donations, claims, and pickups. Return the same typed state/models, or normalize backend responses there. Put credentials and authorization enforcement on the server. Typical future resources: `/auth`, `/users/me`, `/donations`, `/requests`, `/pickups`, `/verifications`, `/reports`, and `/analytics`.

Before production, implement verified identities, role authorization, concurrent reservation handling, food safety policy, real geolocation, secure uploads, notifications, delivery permissions, and accurate analytics. Current distances and timelines are demonstrative.

## Design and accessibility

Palette: cream `#FAF6EF`, forest `#246B45`, apricot `#F2A65A`, charcoal `#26352D`, and beige. Glass effects use backdrop blur, delicate borders, inset highlights, and subtle shadows. Motion respects reduced-motion preferences. Forms expose field errors; dialogs trap focus, support Escape, and restore focus; keyboard focus rings, a skip link, live toasts, and touch-sized primary controls are included.

The provided attachment contained only the written brief, so the interface follows its palette and direction rather than an unavailable reference image. Food photos are loaded from Unsplash image URLs; replace them with your own licensed asset files before production if desired.

Clear browser localStorage key `foodbridge-demo-v1` to reset the demo. Seed pickup deadlines are relative to the first run; after they expire, reset the demo or create fresh donations.

## Backend now available

The `backend/` folder now contains the Spring Boot + MySQL implementation for account registration/login, profiles, donations, concurrent claims, volunteer assignment, and recipient-confirmed delivery. See [backend setup and API](backend/README.md).

Copy `.env.example` to `.env.local` and restart Vite to enable connected mode. Without that setting, the frontend continues to run the browser-only demo described above. Password reset, administration, distribution management, geolocation, and notifications are not yet implemented on the server.
