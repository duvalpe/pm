"""Mission Alignment API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.models.project import Project
from app.models.user import User
from app.api.dependencies import get_current_user
from app.services.alignment_service import calculate_mission_alignment

router = APIRouter(prefix="/alignment", tags=["mission-alignment"])


class AlignmentResponse(BaseModel):
    """Mission alignment response schema."""
    project_id: int
    alignment_score: float  # 0-100%
    message: str


class AlignmentDetailResponse(BaseModel):
    """Detailed alignment response with breakdown."""
    project_id: int
    alignment_score: float
    milestones_total: int
    milestones_completed: int
    milestones_on_time: int
    schedules_total: int
    schedules_on_track: int


@router.get("/project/{project_id}", response_model=AlignmentResponse)
async def get_project_alignment(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get mission alignment score for a project."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    
    try:
        alignment_score = calculate_mission_alignment(db, project_id)
        
        # Update project's alignment_score
        project.alignment_score = alignment_score
        db.commit()
        
        # Generate message based on score
        if alignment_score >= 80:
            message = "Excellent alignment with mission objectives"
        elif alignment_score >= 60:
            message = "Good alignment with minor areas for improvement"
        elif alignment_score >= 40:
            message = "Moderate alignment - review milestones and schedules"
        else:
            message = "Low alignment - significant attention needed"
        
        return AlignmentResponse(
            project_id=project_id,
            alignment_score=alignment_score,
            message=message
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/project/{project_id}/recalculate", response_model=AlignmentResponse)
async def recalculate_alignment(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Recalculate and update mission alignment score for a project."""
    return await get_project_alignment(project_id, db, current_user)
