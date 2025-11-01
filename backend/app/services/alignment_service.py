"""Mission Alignment calculation service."""
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.models.project import Project
from app.models.milestone import Milestone, MilestoneStatus
from app.models.schedule import Schedule


def calculate_mission_alignment(
    db: Session,
    project_id: int
) -> float:
    """
    Calculate mission alignment score (0-100%) for a project.
    
    Factors considered:
    - Milestone completion rate (weight: 40%)
    - Milestone on-time performance (weight: 30%)
    - Schedule adherence (weight: 30%)
    
    Returns:
        float: Alignment score between 0.0 and 100.0
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ValueError(f"Project with id {project_id} not found")
    
    milestones = db.query(Milestone).filter(Milestone.project_id == project_id).all()
    schedules = db.query(Schedule).filter(Schedule.project_id == project_id).all()
    
    # If no milestones or schedules, return 0
    if not milestones and not schedules:
        return 0.0
    
    scores = []
    weights = []
    
    # Factor 1: Milestone completion rate (40% weight)
    if milestones:
        completed_count = sum(1 for m in milestones if m.status == MilestoneStatus.COMPLETED)
        completion_rate = (completed_count / len(milestones)) * 100
        scores.append(completion_rate)
        weights.append(0.4)
    
    # Factor 2: Milestone on-time performance (30% weight)
    if milestones:
        today = date.today()
        on_time_count = 0
        total_past_due = 0
        
        for milestone in milestones:
            if milestone.status == MilestoneStatus.COMPLETED:
                if milestone.completion_date and milestone.completion_date <= milestone.target_date:
                    on_time_count += 1
            elif milestone.target_date < today:
                # Past due and not completed
                total_past_due += 1
        
        # Calculate on-time score (penalize past due milestones)
        if len(milestones) > 0:
            on_time_rate = ((on_time_count / len(milestones)) * 100) - (total_past_due / len(milestones) * 50)
            on_time_rate = max(0, min(100, on_time_rate))  # Clamp between 0 and 100
        else:
            on_time_rate = 0
        
        scores.append(on_time_rate)
        weights.append(0.3)
    
    # Factor 3: Schedule adherence (30% weight)
    if schedules:
        # Check if current date is within schedule date range
        today = date.today()
        schedule_scores = []
        
        for schedule in schedules:
            if schedule.start_date <= today <= schedule.end_date:
                # On schedule
                schedule_scores.append(100.0)
            elif today < schedule.start_date:
                # Before schedule starts
                schedule_scores.append(100.0)  # Not started yet is considered good
            elif today > schedule.end_date:
                # Past schedule end date
                schedule_scores.append(0.0)  # Overdue schedule
            else:
                schedule_scores.append(50.0)
        
        avg_schedule_score = sum(schedule_scores) / len(schedule_scores) if schedule_scores else 0
        scores.append(avg_schedule_score)
        weights.append(0.3)
    
    # Calculate weighted average
    if not scores:
        return 0.0
    
    # Normalize weights if they don't sum to 1.0
    total_weight = sum(weights)
    if total_weight > 0:
        weights = [w / total_weight for w in weights]
    
    alignment_score = sum(score * weight for score, weight in zip(scores, weights))
    return round(alignment_score, 2)
