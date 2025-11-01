"""RFI (Request for Information) and Submittal model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base


class RFIStatus(str, enum.Enum):
    """RFI/Submittal status enumeration."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    CLOSED = "closed"


class RFISubmittal(Base):
    """RFI and Submittal model for Procore integration."""
    __tablename__ = "rfi_submittals"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    procore_id = Column(String, nullable=True, index=True)  # External Procore ID
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(RFIStatus), default=RFIStatus.DRAFT, nullable=False)
    documents = Column(Text, nullable=True)  # JSON array of document references
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="rfi_submittals")
