# FoodBridge backend

Spring Boot 3.5.16, Java 21, Spring Security, JPA, Flyway, and MySQL. The API stores real accounts, donations, and pickup timelines. No demo records are inserted into the database.

## Start locally

The local MySQL setup is complete on this computer. To start the backend again from the project root in PowerShell 7:

```powershell
./scripts/start-backend.ps1
```

This uses the downloaded Java/Maven tools and the app password encrypted for your Windows account in `.tools/db-password.local`. Keep the terminal open while using the app. The root password is not stored. For a fresh local setup, `./scripts/setup-local-database.ps1` prompts privately for the root password, creates the database and app user, enables connected frontend mode, and starts the backend. Re-running setup without a saved credential resets only the local `foodbridge` app user's password.

The manual setup steps below are an alternative for another computer.

1. Install JDK 21, Maven 3.9+, and MySQL 8.4 (or use the project-local Java/Maven toolchain under `.tools` prepared during development).
2. As a MySQL administrator, create an empty database and a dedicated local user. Replace the password below with your own password:

```sql
CREATE DATABASE foodbridge CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'foodbridge'@'localhost' IDENTIFIED BY 'your-local-password';
GRANT ALL PRIVILEGES ON foodbridge.* TO 'foodbridge'@'localhost';
```

3. In a PowerShell terminal from the project root:

```powershell
$env:DB_PASSWORD = 'your-local-password'
# Optional: DB_URL and DB_USER override the defaults in application.yml.
mvn -f backend/pom.xml spring-boot:run
```

With the downloaded project-local tools:

```powershell
$env:JAVA_HOME = (Get-ChildItem .tools -Directory -Filter 'jdk-*' | Select-Object -First 1).FullName
$env:DB_PASSWORD = 'your-local-password'
& '.tools/apache-maven-3.9.11/bin/mvn.cmd' -f backend/pom.xml '-Dmaven.repo.local=E:/Projects/DBMS OOPS/.tools/m2' spring-boot:run
```

Flyway creates the tables on startup, and Hibernate validates the schema. The API listens on `http://127.0.0.1:8080`.

4. Enable connected frontend mode in another terminal:

```powershell
Copy-Item .env.example .env.local
npm.cmd run dev
```

Vite forwards `/api` to Spring Boot. Restart Vite after changing the mode. Without `VITE_API_MODE=backend`, the existing local frontend demo is used. Demo data is never imported into the backend.

## Try a complete journey

Use different browser profiles (or sign out between accounts):

1. Register a **Food Donor**, then create a donation with a future pickup deadline.
2. Register a **Citizen** or **NGO**, then claim the donation from Explore.
3. Register a **Volunteer**, accept the open assignment in the dashboard, and confirm pickup in tracking.
4. Sign back in as the recipient and confirm delivery in tracking.

Each account has a fixed role. Public registration cannot create Administrator accounts. The server checks ownership and roles even when requests bypass the UI. A database write lock and a unique pickup constraint prevent two recipients from claiming the same donation. Volunteers can accept open requests, and each request is only returned to its recipient, donor, assigned volunteer, administrators, or volunteers browsing unassigned requests.

## API

All mutation endpoints require a CSRF token. First GET `/api/auth/csrf`, keep the session cookie, and send the returned token in the returned header name (normally `X-CSRF-TOKEN`). Refresh the token after login, registration, or logout. Browser authentication uses an HttpOnly session cookie; passwords are hashed with BCrypt and never returned.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Application liveness |
| GET | `/api/auth/csrf` | Session security token |
| GET | `/api/state` | Frontend-compatible state scoped to the current user |
| POST | `/api/auth/register` | `{name,email,password,role}` and sign in |
| POST | `/api/auth/login` | `{email,password}` and sign in |
| POST | `/api/auth/logout` | Invalidate session |
| PATCH | `/api/users/me` | `{name,organization,area}` |
| POST | `/api/donations` | Create donation using the frontend donation input |
| DELETE | `/api/donations/{id}` | Withdraw an owned, unclaimed donation |
| POST | `/api/donations/{id}/claim` | Claim unexpired food as Citizen or NGO |
| POST | `/api/pickups/{id}/accept` | Assign current Volunteer |
| POST | `/api/pickups/{id}/advance` | Assigned volunteer confirms pickup; recipient confirms delivery |

Successful mutations return the same state shape as `/api/state`, except logout returns 204. Errors return a `message`, with field `errors` for validation failures. Statuses: 400 invalid input, 401 authentication needed, 403 forbidden action, 404 missing resource, 409 state conflict.

## Validation

```powershell
mvn -f backend/pom.xml test
npm.cmd run build
npm.cmd test
```

Backend integration tests use an in-memory H2 database in MySQL compatibility mode and run the actual Flyway migration and schema validation. They cover real password checks, denied public admin registration, CSRF, logout, role tampering, ownership, request visibility, pickup confirmations, expiration, and concurrent reservation. On 25 November 2026, the live API was also verified against MySQL 8.4.13 for registration, profile storage, donations, competing claims, ownership, privacy, volunteer assignment, recipient-confirmed delivery, timestamps, logout, invalid-password rejection, and subsequent login. Temporary integration records were removed afterward.

## Current scope and deployment

Email resets, email verification, administrator user management, reports, distributions, notifications, geolocation, and production upload storage remain future work. Connected mode returns empty report, verification, and distribution collections and does not perform sample admin writes. Distances are still entered/display data rather than calculated geolocation. The current state endpoint returns all relevant listings; pagination is needed for larger datasets.

For deployment, serve the frontend and `/api` behind the same HTTPS origin, set `COOKIE_SECURE=true`, use secrets for database credentials, and keep `/api` outside SPA/service-worker fallback. Sessions currently live in server memory, so restart signs users out; use a shared session store before scaling across servers. Add rate limiting, identity verification, file validation/storage, operational monitoring, and a reviewed food safety policy before a public launch.
