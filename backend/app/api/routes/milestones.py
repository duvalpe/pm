"""Milestones routes with full CRUD operations."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date, datetime
from app.db.database import get_db
from app.models.milestone import Milestone, MilestoneStatus
from app.models.project import Project
from app.models.user import User
from app.api.dependencies import get_current_user, require_project_manager

router = APIRouter(prefix="/milestones", tags=["milestones"])


# Pydantic schemas
class MilestoneBase(BaseModel):
    """Base milestone schema."""
    name: str
    description: Optional[str] = None
    target_date: date
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED


class MilestoneCreate(MilestoneBase):
    """Milestone creation schema."""
    project_id: int


class MilestoneUpdate(BaseModel):
    """Milestone update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[date] = None
    completion_date: Optional[date] = None
    status: Optional[MilestoneStatus] = None


class MilestoneResponse(MilestoneBase):
    """Milestone response schema."""
    id: int
    project_id: int
    completion_date: Optional[date] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


@router.get("", response_model=List[MilestoneResponse])
async def list_milestones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_id: Optional[int] = None,
    status: Optional[MilestoneStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all milestones with pagination and optional filters."""
    query = db.query(Milestone)
    
    if project_id:
        query = query.filter(Milestone.project_id == project_id)
    if status:
        query = query.filter(Milestone.status == status)
    
    milestones = query.offset(skip).limit(limit).all()
    return milestones


@router.get("/{milestone_id}", response_model=MilestoneResponse)
async def get_milestone(
    milestone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific milestone by ID."""
    milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Milestone with id {milestone_id} not found"
        )
    
    return milestone


@router.post("", response_model=MilestoneResponse, status_code=status.HTTP_201_CREATED)
async def create_milestone(
    milestone_data: MilestoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_project_manager)
):
    """Create a new milestone."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == milestone_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {milestone_data.project_id} not found"
        )
    
    milestone = Milestone(
        project_id=milestone_data.project_id,
        name=milestone_data.name,
        description=milestone_data.description,
        target_date=milestone_data.target_date,
        status=milestone_data.status
    )
    
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    
    return milestone


@router.put("/{milestone_id}", response_model=MilestoneResponse)
async def update_milestone(
    milestone_id: int,
    milestone_data: MilestoneUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_project_manager)
):
    """Update an existing milestone."""
    milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Milestone with id {milestone_id} not found"
        )
    
    # Update fields if provided
    if milestone_data.name is not None:
        milestone.name = milestone_data.name
    if milestone_data.description is not None:
        milestone.description = milestone_data.description
    if milestone_data.target_date is not None:
        milestone.target_date = milestone_data.target_date
    if milestone_data.completion_date is not None:
        milestone.completion_date = milestone_data.completion_date
    if milestone_data.status is not None:
        milestone.status = milestone_data.status
        # Auto-set completion_date if status is completed
        if milestone_data.status == MilestoneStatus.COMPLETED and not milestone.completion_date:
            milestone.completion_date = date.today()
        # Clear completion_date if status is not completed
        elif milestone_data.status != MilestoneStatus.COMPLETED:
            milestone.completion_date = None
    
    db.commit()
    db.refresh(milestone)
    
    return milestone


@router.delete("/{milestone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_milestone(
    milestone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_project_manager)
):
    """Delete a milestone."""
    milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Milestone with id {milestone_id} not found"
        )
    
    db.delete(milestone)
    db.commit()
    
    return None
