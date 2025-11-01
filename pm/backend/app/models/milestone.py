"""
Milestone model for Gantt chart and schedule tracking.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Milestone(Base):
    """Milestone model with Gantt chart data."""
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Schedule data
    planned_start = Column(DateTime(timezone=True), nullable=False)
    planned_end = Column(DateTime(timezone=True), nullable=False)
    actual_start = Column(DateTime(timezone=True), nullable=True)
    actual_end = Column(DateTime(timezone=True), nullable=True)
    
    # Status and progress
    status = Column(String(50), default="planned", nullable=False)  # planned, in_progress, completed, delayed
    progress_percentage = Column(Float, default=0.0, nullable=False)  # 0-100%
    
    # Color coding for Gantt chart
    color_code = Column(String(7), default="#4CAF50", nullable=False)  # Hex color
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="milestones")
    tasks = relationship("Task", back_populates="milestone", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Milestone(id={self.id}, name={self.name}, status={self.status})>"
