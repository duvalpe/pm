"""Import all models for Alembic to detect."""
from app.models.user import User, UserRole
from app.models.project import Project, ProjectStatus
from app.models.milestone import Milestone, MilestoneStatus
from app.models.schedule import Schedule
from app.models.rfi_submittal import RFISubmittal, RFIStatus
from app.models.audit_log import AuditLog

__all__ = [
    "User",
    "UserRole",
    "Project",
    "ProjectStatus",
    "Milestone",
    "MilestoneStatus",
    "Schedule",
    "RFISubmittal",
    "RFIStatus",
    "AuditLog",
]
