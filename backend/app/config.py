"""Application configuration management."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/pm_db"
    
    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Procore API (optional)
    PROCORE_CLIENT_ID: Optional[str] = None
    PROCORE_CLIENT_SECRET: Optional[str] = None
    PROCORE_REDIRECT_URI: Optional[str] = None
    
    # Ollama API (optional)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
