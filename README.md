# Construction AI Suite

Enterprise AI Construction Intelligence Platform with native Monday.com integration.

## Architecture Overview

Monorepo structure:
- **Backend**: Flask REST API (App Factory), service layer, PostgreSQL, Redis
- **Frontend**: React, Vite, Tailwind CSS, mobile-first responsive design
- **Infrastructure**: Multi-container Docker, Nginx

## Demo Mode

The platform runs in demo mode with simulated Monday.com data. Boards, items, status columns, and dependencies mimic Monday.com structure. Connect real Monday.com via OAuth in Phase 2.

## Quick Start

### Option A: Docker (recommended)
```bash
cd construction-ai-suite
docker-compose up -d
```

### Option B: Local (no Docker)
Uses SQLite by default. No PostgreSQL required for demo.

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
set FLASK_APP=app
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Access:**
- This machine: http://localhost:3000
- Ubuntu laptop (same network): http://YOUR_WINDOWS_IP:3000
- Backend API: http://localhost:8000
- Health: http://localhost:8000/health

## API Endpoints (Demo)

| Endpoint | Description |
|----------|-------------|
| GET /api/v1/health | Health check |
| GET /api/v1/dashboard/kpis | Executive KPIs |
| GET /api/v1/projects | Monday.com boards (demo) |
| GET /api/v1/projects/{id}/items | Board items |
| GET /api/v1/risk/scores?scope=items\|boards | Risk scores |
| GET /api/v1/dependencies/graph | Dependency graph |

## Development

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Unix: source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/construction_ai
flask db upgrade
flask run
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Database
Requires PostgreSQL. With Docker:
```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=construction_ai postgres:16-alpine
```

## Branching Strategy

- `main`: Production-ready code
- Feature branches: `feature/<name>` per capability
- PR required for merge, CI must pass

## License

Proprietary - All rights reserved.
