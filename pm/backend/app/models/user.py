"""
User and Role models for authentication and authorization.
"""
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class Role(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    VIEWER = "viewer"
    CONTRACTOR = "contractor"


class User(Base):
    """User model for session-based authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(Enum(Role), nullable=False, default=Role.VIEWER)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    projects = relationship("Project", back_populates="created_by_user", foreign_keys="Project.created_by")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
