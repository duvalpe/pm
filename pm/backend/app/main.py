from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import SessionLocal, engine
from app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project Management Tool API",
    description="Cross-platform project management tool API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8081"],  # React web and React Native
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "pm-api"}

# Import routers
from app.api import auth, projects, milestones, ai

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(milestones.router, prefix="/api/milestones", tags=["milestones"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
