"""
Document model for project document management.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Document(Base):
    """Document model with Procore sync support."""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    file_type = Column(String(50), nullable=True)
    file_size = Column(Integer, nullable=True)  # Size in bytes
    
    # Procore sync fields
    procore_id = Column(String(100), nullable=True, unique=True, index=True)
    procore_synced = Column(Boolean, default=False, nullable=False)
    procore_sync_date = Column(DateTime(timezone=True), nullable=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="documents")

    def __repr__(self):
        return f"<Document(id={self.id}, name={self.name}, procore_synced={self.procore_synced})>"
