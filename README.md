# Congressional App Challenge - ShelterLink 🏠

**LA County shelter and resource finder - helping people find essential services**

> **Evolution**: This project started as a simple shelter finder and has evolved into a comprehensive platform with mobile app, staff portal, and advanced features.

ShelterLink is a comprehensive platform designed to help people in Los Angeles County quickly find shelters and essential resources. Built with privacy-first principles, multilingual support, and offline capabilities.

## 📁 Legacy Files

The following files are preserved from the original project:
- `hobo_view` - Original shelter view implementation
- `shelter_view` - Original shelter management view
- `web/public.html` - Original public interface
- `web/admin.html` - Original admin panel
- `server/server.js` - Original Express.js backend

## 🏗️ Architecture

- **`apps/api`** - FastAPI (Python) backend with Postgres + PostGIS
- **`apps/staff`** - Next.js 14 web portal for shelter staff
- **`apps/mobile`** - React Native (Expo) mobile app for end users
- **`packages/ui`** - Shared UI components for React Native and Next.js
- **`packages/config`** - Shared ESLint, TypeScript, and Prettier configs

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and PNPM 8+
- Python 3.11+ and Poetry
- Docker and Docker Compose
- Git

### One-Command Setup

```bash
# Clone and setup everything
git clone <repository-url>
cd shelterlink
make setup
```

This will:
1. Install all dependencies
2. Start Postgres with PostGIS
3. Run database migrations
4. Seed with sample LA data
5. Start all development servers

### Manual Setup

```bash
# 1. Install dependencies
pnpm install

# 2. Start database
pnpm db:up

# 3. Run migrations and seed data
pnpm db:migrate
pnpm db:seed

# 4. Start all apps
pnpm dev
```

## 📱 Apps

### Mobile App (`apps/mobile`)
- **React Native + Expo** with TypeScript
- **Offline-first** with React Query + AsyncStorage
- **Multilingual** (EN/ES/KO/HY/TL/ZH)
- **Accessibility** features (large targets, screen reader, TTS)
- **Location-aware** with distance sorting
- **Push notifications** for bed availability

**Start:** `pnpm --filter @shelterlink/mobile start`

### Staff Portal (`apps/staff`)
- **Next.js 14** with App Router
- **Magic link authentication**
- **Real-time shelter management**
- **Audit logging** for all changes
- **Multilingual staff interface**

**Start:** `pnpm --filter @shelterlink/staff dev`

### API (`apps/api`)
- **FastAPI** with async SQLAlchemy
- **Postgres + PostGIS** for spatial queries
- **JWT authentication** for staff
- **Rate limiting** and CORS
- **Comprehensive testing**

**Start:** `pnpm --filter @shelterlink/api dev`

## 🗄️ Database

### Schema Overview

```sql
-- Core tables
shelters(id, name, address, lat, lon, neighborhood, ...)
shelter_status(id, shelter_id, category, beds_total, beds_available, status, ...)
resources(id, name, type, address, lat, lon, neighborhood, ...)
staff(id, email, shelter_id, role, locale)
status_changes(id, shelter_id, category, prev_available, new_available, ...)
translation_strings(id, key, lang, value)

-- PostGIS spatial indexes for fast proximity searches
```

### Key Features

- **Conservatism Rule**: Status auto-downgrades to `UNKNOWN` after 12 hours
- **Spatial Queries**: Fast distance-based searches using PostGIS
- **Audit Trail**: All status changes logged with staff attribution
- **Multilingual**: Dynamic content via `translation_strings` table

## 🌍 LA-Specific Features

### Neighborhoods Covered
- Skid Row (DTLA)
- Westlake/MacArthur Park
- Koreatown
- Hollywood
- Venice
- South LA
- San Fernando Valley
- San Pedro/Harbor

### Resource Types
- **Shelters** (Men/Women/Family/Youth/Mixed)
- **Cooling & Warming Centers**
- **Safe Parking** locations
- **Food pantries & hot meals**
- **Mobile showers & hygiene**
- **Community clinics & urgent care**
- **Legal aid / benefits enrollment**

### Emergency Contacts
- **211 LA** integration
- **Crisis hotlines**
- **Shelter front desks**

## 🔧 Development

### Commands

```bash
# Development
pnpm dev              # Start all apps
pnpm build           # Build all apps
pnpm test            # Run all tests
pnpm lint            # Lint all code
pnpm format          # Format all code

# Database
pnpm db:up           # Start database
pnpm db:down         # Stop database
pnpm db:migrate      # Run migrations
pnpm db:seed         # Seed data
pnpm db:reset        # Reset database

# Individual apps
pnpm --filter @shelterlink/api dev
pnpm --filter @shelterlink/staff dev
pnpm --filter @shelterlink/mobile start
```

### Environment Variables

Copy the example files and configure:

```bash
# API
cp apps/api/env.example apps/api/.env

# Staff Portal
cp apps/staff/env.example apps/staff/.env

# Mobile App
cp apps/mobile/env.example apps/mobile/.env
```

### Testing

```bash
# Backend tests
cd apps/api && poetry run pytest

# Frontend tests (when implemented)
pnpm --filter @shelterlink/staff test
pnpm --filter @shelterlink/mobile test
```

## 🎯 Demo Script (90 seconds)

1. **Problem**: "LA has thousands of people needing shelter and resources"
2. **Open Mobile App**: Show home screen with location permission
3. **Filter**: Tap "Women" + "Pet Friendly" chips
4. **Results**: Show distance-sorted shelters with status pills
5. **Detail**: Tap shelter → show requirements, languages, "Call" button
6. **Directions**: Tap "Go" → opens Google/Apple Maps
7. **Staff Update**: Open staff portal → update bed count
8. **Real-time**: Refresh mobile → shows updated availability
9. **Privacy**: "No login required, location stays on device"
10. **Multilingual**: Switch to Spanish → entire UI changes
11. **Offline**: Turn off internet → cached data still works
12. **Weather**: Show heat advisory banner → links to cooling centers

## 🔒 Privacy & Security

### Privacy-First Design
- **No end-user accounts** - completely anonymous
- **Location stays on device** - never sent to server
- **No PII collection** - no tracking or analytics
- **Offline-first** - works without internet

### Staff Security
- **Magic link authentication** - no passwords
- **JWT tokens** with short expiration
- **Rate limiting** on all endpoints
- **Audit logging** for all changes
- **Role-based access** (ADMIN/STAFF)

## 🌐 Internationalization

### Supported Languages
- **English** (en) - Primary
- **Spanish** (es) - Español
- **Korean** (ko) - 한국어
- **Armenian** (hy) - Հայերեն
- **Tagalog** (tl) - Tagalog
- **Mandarin** (zh) - 中文

### Implementation
- **Static content**: Bundled in app
- **Dynamic content**: Database-driven via `translation_strings`
- **Auto-detection**: Device locale detection
- **Manual toggle**: Settings screen language picker

## 📊 Data Management

### Seed Data
- **5 shelters** across LA neighborhoods
- **5 resources** (food, showers, health, cooling, safe parking)
- **2 staff accounts** (admin + shelter staff)
- **24 translation strings** in 3 languages

### Real Data Integration
- **ETL scripts** for importing from LA County data
- **ArcGIS integration** for shelter data
- **211 LA API** for resource updates
- **Weather API** for extreme weather alerts

## 🚀 Deployment

### Production Setup

```bash
# 1. Environment
cp apps/api/env.example apps/api/.env
# Configure DATABASE_URL, JWT_SECRET, EMAIL_PROVIDER, etc.

# 2. Database
docker compose -f docker-compose.prod.yml up -d

# 3. Migrations
cd apps/api && poetry run alembic upgrade head

# 4. Build & Deploy
pnpm build
# Deploy to your platform (Vercel, Railway, etc.)
```

### Docker Production

```bash
# Build images
docker build -f apps/api/Dockerfile -t shelterlink-api .
docker build -f apps/staff/Dockerfile -t shelterlink-staff .

# Run with docker-compose.prod.yml
docker compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

### Development Guidelines
- **TypeScript** for all JavaScript/TypeScript code
- **Black** for Python formatting
- **ESLint** for JavaScript linting
- **Pre-commit hooks** for code quality
- **Comprehensive tests** for all features

## 📄 License

This project is created for the **Congressional App Challenge**.

## 🆘 Support

- **Documentation**: Check this README and code comments
- **Issues**: Create GitHub issues for bugs/features
- **Community**: Join our development discussions

---

**Built with ❤️ for LA County - Helping people find shelter and resources when they need it most.**
