"""
RFI (Request for Information) model for construction project RFIs.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class RFI(Base):
    """RFI model with Procore sync support."""
    __tablename__ = "rfis"

    id = Column(Integer, primary_key=True, index=True)
    rfi_number = Column(String(50), unique=True, nullable=False, index=True)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="open", nullable=False)  # open, answered, closed
    
    # Procore sync fields
    procore_id = Column(String(100), nullable=True, unique=True, index=True)
    procore_synced = Column(Boolean, default=False, nullable=False)
    procore_sync_date = Column(DateTime(timezone=True), nullable=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    answered_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    project = relationship("Project", back_populates="rfis")

    def __repr__(self):
        return f"<RFI(id={self.id}, rfi_number={self.rfi_number}, status={self.status})>"
