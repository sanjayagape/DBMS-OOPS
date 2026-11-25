# Validation

## Live backend validation — 25 November 2026

- MySQL 8.4.13: connected successfully; Flyway migration and Hibernate schema validation completed.
- Live HTTP API: registration, fixed account roles, profile storage, donation creation, competing claims with exactly one winner, donation ownership, request privacy, volunteer assignment, pickup confirmation, recipient-only delivery confirmation, and five timeline timestamps passed.
- Session security: logout, invalid-password rejection, CSRF-protected mutations, subsequent login, and retrieval of the completed delivery passed.
- Temporary integration accounts, donations, pickups, and timestamps were removed after verification.
- Local app credentials use Windows account encryption; the root password is not saved. Connected mode is enabled through `.env.local`.

## Frontend demo validation

Completed on 12 October 2026.

- Production build: passed (`pnpm build`), including strict TypeScript compilation, route chunks, web manifest, icons, and generated Workbox service worker. 23 app-shell entries are precached.
- Flow tests: 3 passed (`npm test` equivalent), covering immutable reservation, duplicate claim rejection, expired/missing listing handling, composed search/category/location/distance filters, and final delivery status.
- Browser: tested at desktop 1440 × 960 and mobile 390 × 844. No page-level horizontal overflow on discovery, dashboards, or impact. Tables and category navigation scroll within their containers.
- Search: expected bread listing found; unmatched search displays empty state and reset action.
- Request flow: Citizen claim → Volunteer assignment acceptance → Picked Up → Delivered. Timestamps and final confirmation verified.
- Donation wizard: invalid blank submission shows field errors; valid details, quantity, pickup, safety review, and submission create a listing visible in discovery and the donor dashboard.
- Admin demo: sample NGO verification and report resolution verified.
- Authentication demo: blank registration errors verified; valid demo registration leads to profile setup and saving opens the appropriate dashboard.
- Impact: Recharts renders; sample metrics remain labeled; local counts reflect demo activity.
- Browser console: no errors or warnings observed during the tested journeys.
- Photos: all desktop homepage food images loaded successfully.

PWA configuration and generated outputs were validated. A physical device installation and full offline/reconnection test were not performed. PWA installation depends on browser support and HTTPS (or localhost). Accessibility support was implemented and keyboard dialog behavior reviewed, but a full assistive-technology audit was not performed.

The desktop preview is in `docs/foodbridge-desktop.jpg`. QA created local sample activity in the preview browser; clear `foodbridge-demo-v1` in localStorage for a fresh demo. Test data is not in the source seed or backend.
