"""Schedules routes with full CRUD operations."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date, datetime
from app.db.database import get_db
from app.models.schedule import Schedule
from app.models.project import Project
from app.models.user import User
from app.api.dependencies import get_current_user, require_project_manager
import json

router = APIRouter(prefix="/schedules", tags=["schedules"])


# Pydantic schemas
class ScheduleBase(BaseModel):
    """Base schedule schema."""
    name: str
    start_date: date
    end_date: date
    tasks_json: Optional[str] = None  # JSON string for Gantt tasks


class ScheduleCreate(ScheduleBase):
    """Schedule creation schema."""
    project_id: int


class ScheduleUpdate(BaseModel):
    """Schedule update schema."""
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    tasks_json: Optional[str] = None


class ScheduleResponse(ScheduleBase):
    """Schedule response schema."""
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ScheduleDetailResponse(ScheduleResponse):
    """Schedule detail response with parsed tasks."""
    tasks: Optional[dict] = None  # Parsed JSON tasks


@router.get("", response_model=List[ScheduleResponse])
async def list_schedules(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all schedules with pagination and optional project filter."""
    query = db.query(Schedule)
    
    if project_id:
        query = query.filter(Schedule.project_id == project_id)
    
    schedules = query.offset(skip).limit(limit).all()
    return schedules


@router.get("/{schedule_id}", response_model=ScheduleDetailResponse)
async def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific schedule by ID."""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with id {schedule_id} not found"
        )
    
    # Parse tasks_json if present
    tasks = None
    if schedule.tasks_json:
        try:
            tasks = json.loads(schedule.tasks_json)
        except json.JSONDecodeError:
            tasks = None
    
    return {
        **schedule.__dict__,
        "tasks": tasks
    }


@router.post("", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_data: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_project_manager)
):
    """Create a new schedule."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == schedule_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {schedule_data.project_id} not found"
        )
    
    # Validate dates
    if schedule_data.start_date >= schedule_data.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    # Validate tasks_json if provided
    if schedule_data.tasks_json:
        try:
            json.loads(schedule_data.tasks_json)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="tasks_json must be valid JSON"
            )
    
    schedule = Schedule(
        project_id=schedule_data.project_id,
        name=schedule_data.name,
        start_date=schedule_data.start_date,
        end_date=schedule_data.end_date,
        tasks_json=schedule_data.tasks_json
    )
    
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    
    return schedule


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_project_manager)
):
    """Update an existing schedule."""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with id {schedule_id} not found"
        )
    
    # Update fields if provided
    if schedule_data.name is not None:
        schedule.name = schedule_data.name
    if schedule_data.start_date is not None:
        schedule.start_date = schedule_data.start_date
    if schedule_data.end_date is not None:
        schedule.end_date = schedule_data.end_date
    if schedule_data.tasks_json is not None:
        # Validate JSON if provided
        try:
            json.loads(schedule_data.tasks_json)
            schedule.tasks_json = schedule_data.tasks_json
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="tasks_json must be valid JSON"
            )
    
    # Validate date range
    start_date = schedule_data.start_date or schedule.start_date
    end_date = schedule_data.end_date or schedule.end_date
    if start_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    db.commit()
    db.refresh(schedule)
    
    return schedule


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_project_manager)
):
    """Delete a schedule."""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with id {schedule_id} not found"
        )
    
    db.delete(schedule)
    db.commit()
    
    return None
