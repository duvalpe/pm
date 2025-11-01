<!-- efe078e2-835a-4551-b6c0-eed9bb0374be 6c9ec42f-a69b-455b-aba1-06447cf03d42 -->
# Cross-Platform Project Management Tool MVP Development Plan

## Agent Assignment Strategy (4 Agents)

### Agent Responsibilities

**Agent 1: Backend Core & Database**
- Database models and migrations
- Core CRUD APIs
- Session authentication
- Database connection and encryption setup
- Alembic migration management

**Agent 2: Backend Integrations & Services**
- Procore API integration
- MS Project (MPXJ) integration
- Background sync services
- External API error handling and retry logic

**Agent 3: Frontend Web**
- React + TypeScript setup
- ImGui.js integration
- Dashboard components
- Web UI implementation

**Agent 4: Mobile & Deployment**
- React Native setup
- Mobile screens and components
- Docker Compose configuration
- Deployment scripts
- Documentation

### Parallel Work Opportunities

- **Phase 1-2**: Agents 1 & 2 can work in parallel on backend core vs integrations
- **Phase 4-5**: Agents 3 & 4 can work in parallel on web vs mobile frontends
- **Phase 3**: Agent 2 can handle AI integration (Ollama)
- **Phase 6**: Agent 4 handles testing and deployment

## Architecture Overview

**Tech Stack:**

- Backend: FastAPI (Python) with SQLAlchemy ORM
- Database: PostgreSQL (on-premises, encrypted)
- Frontend Web: React + TypeScript with ImGui.js libraries (react-immediate-mode-gui or imgui-js)
- Mobile: React Native + TypeScript
- AI: Ollama (local inference)
- Integrations: Procore API, MPXJ for MS Project (.mpp files)

**Project Structure:**

```
pm/
??? backend/              # FastAPI application
?   ??? app/
?   ?   ??? api/         # API routes
?   ?   ??? models/      # SQLAlchemy models
?   ?   ??? services/    # Business logic
?   ?   ??? integrations/ # Procore, MS Project
?   ?   ??? ai/          # Ollama client
?   ??? migrations/      # Alembic migrations
?   ??? requirements.txt
??? frontend-web/         # React web app
?   ??? src/
?   ?   ??? components/  # ImGui-style components
?   ?   ??? pages/       # Dashboard, milestones, etc.
?   ?   ??? services/    # API clients
?   ??? package.json
??? mobile/              # React Native app
?   ??? src/
?   ?   ??? screens/
?   ?   ??? components/
?   ?   ??? services/
?   ??? package.json
??? docker/              # Docker configs
??? scripts/             # Deployment scripts
??? docs/                # API docs, setup guides
```

## Development Phases with Agent Assignments

### Phase 1: Foundation & Backend Core (Days 1-4)

**Agent 1: Backend Core & Database**

- Set up FastAPI project structure with PostgreSQL
- Database models: Projects, Milestones, Tasks, Documents, RFIs, Users, Roles
- Session-based authentication (no financial tables)
- Core CRUD APIs for projects, milestones, schedules
- Database migrations with Alembic
- Health check endpoints
- On-premises deployment configuration

**Key Files:**

- `backend/app/models/project.py` - Project model with relationships
- `backend/app/models/milestone.py` - Milestone with Gantt data
- `backend/app/api/auth.py` - Session auth endpoints
- `backend/app/db/session.py` - PostgreSQL connection with encryption

### Phase 2: Integrations (Days 5-7)

**Agent 2: Backend Integrations & Services**

- Procore API integration:
  - OAuth2 setup and token management
  - Documents/RFIs sync endpoints (bi-directional)
  - Rate limiting for API calls
  - Error handling and retry logic
- MS Project integration:
  - MPXJ library for .mpp file parsing
  - Import/export endpoints
  - CSV fallback support
  - Scheduled batch processing (15min intervals)

**Key Files:**

- `backend/app/integrations/procore.py` - Procore API client
- `backend/app/integrations/mpxj_importer.py` - MS Project file handler
- `backend/app/services/sync_service.py` - Background sync jobs

### Phase 3: AI Assistant (Days 8-9)

**Agent 2: Backend Integrations & Services (Ollama Integration)**

- Ollama client integration
- Query processing for non-financial data
- Response caching for <2s latency
- Query examples: milestone status, schedule adherence, project health

**Key Files:**

- `backend/app/ai/ollama_client.py` - Ollama API wrapper
- `backend/app/ai/query_processor.py` - Natural language to SQL/API queries
- `backend/app/api/ai.py` - AI chat endpoint

### Phase 4: Frontend Web Dashboard (Days 10-13)

**Agent 3: Frontend Web**

- React + TypeScript setup with ImGui.js library
- Dashboard components:
  - Mission alignment radial gauge (0-100%)
  - Gantt chart for milestones (color-coded)
  - Schedule timeline slider
  - Health heatmap
- Real-time data refresh (<5s)
- Session auth UI
- Responsive layout (minimalist, RemedyBG-inspired)

**Key Files:**

- `frontend-web/src/components/MissionAlignmentGauge.tsx`
- `frontend-web/src/components/MilestoneGantt.tsx`
- `frontend-web/src/pages/Dashboard.tsx`
- `frontend-web/src/services/api.ts` - API client

### Phase 5: Mobile App (Days 14-16)

**Agent 4: Mobile & Deployment (Mobile Focus)**

- React Native setup with TypeScript
- Core screens: Dashboard, Milestones, Schedule
- API integration matching web
- Mobile-optimized UI (similar minimalist style)
- Navigation structure

**Key Files:**

- `mobile/src/screens/DashboardScreen.tsx`
- `mobile/src/components/MissionGauge.tsx`
- `mobile/src/navigation/AppNavigator.tsx`

### Phase 6: Testing & Deployment (Days 17-18)

**Agent 4: Mobile & Deployment (Testing & Deployment Focus)**
- Unit tests for backend services (Agent 1 may assist)
- Integration tests for APIs (Agent 1 may assist)
- Docker Compose setup (PostgreSQL + Backend)
- MacBook Air deployment scripts
- Environment configuration management
- Basic documentation

**Agent 1: Backend Core (Testing Assistance)**
- Unit tests for backend services
- Integration tests for APIs

**Key Files:**

- `docker/docker-compose.yml` - Local dev environment
- `scripts/deploy-macos.sh` - MacBook deployment
- `backend/tests/` - Test suite
- `README.md` - Setup instructions

## Detailed Agent Work Breakdown

### Agent 1: Backend Core & Database
**Phase 1 Tasks:**
1. Create FastAPI app structure (`app/main.py`, `app/db/session.py`)
2. Create SQLAlchemy models:
   - `models/user.py` - User with roles
   - `models/project.py` - Project model
   - `models/milestone.py` - Milestone with Gantt data
   - `models/task.py` - Task model
   - `models/document.py` - Document model
   - `models/rfi.py` - RFI model
3. Set up Alembic migrations
4. Create session authentication (`api/auth.py`)
5. Create core CRUD APIs:
   - `api/projects.py` - Project endpoints
   - `api/milestones.py` - Milestone endpoints
   - `api/tasks.py` - Task endpoints (if needed)
6. Database connection pooling and encryption setup

**Phase 6 Tasks:**
1. Write unit tests for models
2. Write integration tests for API endpoints

### Agent 2: Backend Integrations & Services
**Phase 2 Tasks:**
1. Procore API client:
   - OAuth2 authentication flow
   - Token refresh mechanism
   - Document sync endpoint
   - RFI sync endpoint
   - Error handling and retry logic
   - Mock mode for development
2. MS Project integration:
   - MPXJ wrapper or python-mpxj setup
   - `.mpp` file parser
   - Import endpoint
   - Export endpoint
   - CSV fallback implementation
3. Background sync service:
   - Scheduled tasks (15min intervals)
   - Queue management
   - Error logging

**Phase 3 Tasks:**
1. Ollama client setup
2. Query processor (natural language ? SQL/API)
3. Response caching mechanism
4. AI chat endpoint
5. Query validation (exclude financial data)

### Agent 3: Frontend Web
**Phase 4 Tasks:**
1. Initialize React + TypeScript project
2. Install and configure ImGui.js library
3. Set up API client service
4. Create dashboard page layout
5. Build components:
   - MissionAlignmentGauge (radial gauge 0-100%)
   - MilestoneGantt (color-coded Gantt chart)
   - TimelineSlider (schedule navigation)
   - HealthHeatmap (project health visualization)
6. Implement real-time data refresh (<5s polling)
7. Create authentication UI
8. Implement responsive layout (RemedyBG-inspired minimalist style)

### Agent 4: Mobile & Deployment
**Phase 5 Tasks:**
1. Initialize React Native + TypeScript project
2. Set up navigation (React Navigation)
3. Create API client (matching web)
4. Build mobile screens:
   - DashboardScreen (mission gauge, summary)
   - MilestonesScreen (list view)
   - ScheduleScreen (timeline view)
5. Create mobile-optimized components
6. Implement authentication flow

**Phase 6 Tasks:**
1. Create Docker Compose configuration:
   - PostgreSQL service
   - Backend service
   - Environment variables
   - Volume mounts
2. Create deployment scripts:
   - `scripts/deploy-macos.sh` - MacBook Air setup
   - Environment configuration
   - Service startup scripts
3. Write README.md with:
   - Setup instructions
   - API documentation
   - Deployment guide
   - Environment variables reference
4. Coordinate testing with Agent 1 (if needed)

## Key Metrics Targets

- Dashboard refresh: <5s
- AI query response: <2s
- Page load time: <3s
- Support up to 50 projects, 1,000 items/project
- 100 queries/hour/user capacity

## Out of Scope (MVP)

- Financial data/tracking
- QuickBooks integration
- Predictive analytics
- Full offline mobile mode
- IoT integrations

## Dependencies

**Backend:**
- fastapi, uvicorn, sqlalchemy, alembic, psycopg2
- requests, python-jose (auth)
- mpxj (Java bridge or python-mpxj alternative)
- ollama Python client

**Frontend Web:**
- react, react-dom, typescript
- react-immediate-mode-gui or imgui-js
- axios, react-query (for real-time updates)
- recharts or d3 for visualizations

**Mobile:**
- react-native, react-navigation
- react-native-charts-wrapper or victory-native
- axios

## Risk Mitigation

- Procore API: Include mock/stub mode for development without credentials
- MPXJ: Test with sample .mpp files; provide CSV fallback
- Ollama: Ensure local installation instructions; fallback to mock responses
- Performance: Implement pagination, caching, connection pooling early

### To-dos

- [ ] Create project directory structure with backend, frontend-web, mobile, docker, and scripts folders
- [ ] Set up FastAPI app with PostgreSQL connection, SQLAlchemy models (Projects, Milestones, Tasks, Documents, RFIs, Users), and Alembic migrations
- [ ] Implement session-based authentication with role-based access control endpoints
- [ ] Create CRUD APIs for projects, milestones, schedules with real-time data refresh support
- [ ] Build Procore API client with OAuth2, document/RFI sync endpoints (bi-directional), and error handling. Include mock mode for development without credentials
- [ ] Implement MPXJ-based MS Project .mpp import/export with CSV fallback and scheduled batch processing (15min intervals)
- [ ] Integrate Ollama client for AI queries on non-financial data with response caching for <2s latency
- [ ] Set up React + TypeScript project with ImGui.js library (react-immediate-mode-gui) and API client service
- [ ] Build dashboard components: Mission alignment radial gauge (0-100%), Gantt chart, timeline slider, health heatmap with real-time refresh
- [ ] Set up React Native + TypeScript project with navigation and API client matching web implementation
- [ ] Create mobile screens: Dashboard, Milestones, Schedule with mobile-optimized UI components
- [ ] Create Docker Compose setup for PostgreSQL + Backend with environment configuration
- [ ] Create MacBook Air deployment scripts with environment setup and startup instructions
- [ ] Write unit tests for backend services and integration tests for API endpoints
- [ ] Create README with setup instructions, API documentation, and deployment guide
