from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from ..models.project import ProjectStatus, ProjectType, TaskStatus, TaskPriority, TaskType


class ProjectBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    project_type: ProjectType = ProjectType.COMMERCIAL


class ProjectCreate(ProjectBase):
    client_id: Optional[int] = None
    project_manager_id: Optional[int] = None
    director_id: Optional[int] = None
    producer_id: Optional[int] = None
    start_date: Optional[date] = None
    target_end_date: Optional[date] = None
    estimated_budget: Optional[float] = 0
    video_format: Optional[str] = None
    aspect_ratio: Optional[str] = None
    duration_minutes: Optional[int] = None
    deliverables: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[ProjectType] = None
    status: Optional[ProjectStatus] = None
    client_id: Optional[int] = None
    project_manager_id: Optional[int] = None
    director_id: Optional[int] = None
    producer_id: Optional[int] = None
    start_date: Optional[date] = None
    target_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    estimated_budget: Optional[float] = None
    actual_budget: Optional[float] = None
    video_format: Optional[str] = None
    aspect_ratio: Optional[str] = None
    duration_minutes: Optional[int] = None
    deliverables: Optional[str] = None
    progress_percentage: Optional[int] = None
    is_archived: Optional[bool] = None


class ProjectResponse(ProjectBase):
    id: int
    status: ProjectStatus
    client_id: Optional[int] = None
    project_manager_id: Optional[int] = None
    director_id: Optional[int] = None
    producer_id: Optional[int] = None
    start_date: Optional[date] = None
    target_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    estimated_budget: float
    actual_budget: float
    video_format: Optional[str] = None
    aspect_ratio: Optional[str] = None
    duration_minutes: Optional[int] = None
    progress_percentage: int
    is_archived: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SprintBase(BaseModel):
    name: str
    goal: Optional[str] = None
    start_date: date
    end_date: date


class SprintCreate(SprintBase):
    project_id: int


class SprintUpdate(BaseModel):
    name: Optional[str] = None
    goal: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None
    is_completed: Optional[bool] = None


class SprintResponse(SprintBase):
    id: int
    project_id: int
    is_active: bool
    is_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: TaskType = TaskType.TASK
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskCreate(TaskBase):
    project_id: int
    sprint_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    assignee_id: Optional[int] = None
    created_by_id: int
    estimated_hours: Optional[float] = None
    due_date: Optional[date] = None
    stage: Optional[str] = None
    scene_number: Optional[str] = None
    labels: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    task_type: Optional[TaskType] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    sprint_id: Optional[int] = None
    assignee_id: Optional[int] = None
    estimated_hours: Optional[float] = None
    logged_hours: Optional[float] = None
    due_date: Optional[date] = None
    stage: Optional[str] = None
    scene_number: Optional[str] = None
    position: Optional[int] = None
    labels: Optional[str] = None


class TaskResponse(TaskBase):
    id: int
    project_id: int
    sprint_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    task_key: str
    status: TaskStatus
    assignee_id: Optional[int] = None
    created_by_id: int
    estimated_hours: Optional[float] = None
    logged_hours: float
    due_date: Optional[date] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    stage: Optional[str] = None
    scene_number: Optional[str] = None
    position: int
    labels: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    task_id: int
    author_id: int
    parent_comment_id: Optional[int] = None


class CommentResponse(CommentBase):
    id: int
    task_id: int
    author_id: int
    parent_comment_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
