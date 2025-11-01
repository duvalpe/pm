# Cross-Platform Project Management Tool MVP

A cross-platform project management tool integrating Procore and Microsoft Project, featuring real-time dashboards, AI assistant (Ollama), and on-premises PostgreSQL storage.

## Technology Stack

- **Backend**: FastAPI (Python 3.11+), SQLAlchemy, PostgreSQL 15+
- **Frontend Web**: React 18+ (to be implemented)
- **Mobile**: React Native (to be implemented)
- **AI**: Ollama (local LLM inference)
- **Integrations**: Procore API, MPXJ (Java library via JNI or Python wrapper)
- **Deployment**: Docker, Docker Compose

## Project Structure

```
BrNTG/
??? backend/           # FastAPI backend
?   ??? app/
?   ?   ??? api/       # API routes and dependencies
?   ?   ??? models/    # SQLAlchemy models
?   ?   ??? services/  # Business logic services
?   ?   ??? db/        # Database configuration
?   ?   ??? config.py  # Application settings
?   ??? alembic/       # Database migrations
?   ??? tests/         # Test files
?   ??? Dockerfile
?   ??? requirements.txt
??? frontend/          # Frontend applications (to be implemented)
??? docker-compose.yml
??? .env.example
??? README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Setup

1. **Clone the repository** (if applicable)

2. **Copy environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Update `.env`** with your configuration (especially `SECRET_KEY`)

4. **Start services with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

5. **Run database migrations**:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

6. **Access the API**:
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Local Development (without Docker)

1. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start PostgreSQL** (or use Docker):
   ```bash
   docker-compose up -d postgres
   ```

3. **Set environment variables**:
   ```bash
   export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/pm_db"
   export SECRET_KEY="your-secret-key"
   ```

4. **Run migrations**:
   ```bash
   cd backend
   alembic upgrade head
   ```

5. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Database Migrations

Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/register` - Register new user
- `GET /api/auth/me` - Get current user info

### Projects (Phase 2 - Placeholder)
- `GET /api/projects` - List projects
- More endpoints to be implemented

### Milestones (Phase 2 - Placeholder)
- `GET /api/milestones` - List milestones
- More endpoints to be implemented

### Schedules (Phase 2 - Placeholder)
- `GET /api/schedules` - List schedules
- More endpoints to be implemented

## Testing

Run tests:
```bash
cd backend
pytest
```

## Development Status

### Phase 1: Foundation & Infrastructure ?
- [x] FastAPI project structure
- [x] PostgreSQL schema (SQLAlchemy models)
- [x] Alembic migrations setup
- [x] JWT authentication
- [x] Role-based access control (RBAC)
- [x] Docker Compose setup
- [x] Environment configuration

### Phase 2: Core Backend APIs (In Progress)
- [ ] Projects API (CRUD)
- [ ] Milestones API
- [ ] Schedules API
- [ ] Mission Alignment API
- [ ] User Management API

### Future Phases
See `cross-platform-pm-tool-mvp.plan.md` for full development plan.

## License

Proprietary - Internal use only
