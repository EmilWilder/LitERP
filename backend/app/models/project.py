from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, Numeric, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class ProjectStatus(str, enum.Enum):
    PLANNING = "planning"
    PRE_PRODUCTION = "pre_production"
    PRODUCTION = "production"
    POST_PRODUCTION = "post_production"
    REVIEW = "review"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class ProjectType(str, enum.Enum):
    COMMERCIAL = "commercial"
    CORPORATE = "corporate"
    DOCUMENTARY = "documentary"
    MUSIC_VIDEO = "music_video"
    SHORT_FILM = "short_film"
    FEATURE_FILM = "feature_film"
    TV_SERIES = "tv_series"
    SOCIAL_MEDIA = "social_media"
    LIVE_EVENT = "live_event"
    ANIMATION = "animation"
    OTHER = "other"


class TaskStatus(str, enum.Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    BLOCKED = "blocked"
    DONE = "done"


class TaskPriority(str, enum.Enum):
    LOWEST = "lowest"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    HIGHEST = "highest"


class TaskType(str, enum.Enum):
    TASK = "task"
    BUG = "bug"
    STORY = "story"
    EPIC = "epic"
    SUBTASK = "subtask"
    MILESTONE = "milestone"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)  # e.g., PRJ-001
    description = Column(Text, nullable=True)
    project_type = Column(Enum(ProjectType), default=ProjectType.COMMERCIAL)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING)
    
    # Client relationship
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    
    # Team
    project_manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    director_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    producer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timeline
    start_date = Column(Date, nullable=True)
    target_end_date = Column(Date, nullable=True)
    actual_end_date = Column(Date, nullable=True)
    
    # Budget
    estimated_budget = Column(Numeric(15, 2), default=0)
    actual_budget = Column(Numeric(15, 2), default=0)
    
    # Video specific
    video_format = Column(String(50), nullable=True)  # 4K, 1080p, etc.
    aspect_ratio = Column(String(20), nullable=True)  # 16:9, 9:16, etc.
    duration_minutes = Column(Integer, nullable=True)
    deliverables = Column(Text, nullable=True)  # JSON string
    
    # Progress
    progress_percentage = Column(Integer, default=0)
    
    is_archived = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    client = relationship("Client", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    sprints = relationship("Sprint", back_populates="project")
    invoices = relationship("Invoice", back_populates="project")
    expenses = relationship("Expense", back_populates="project")
    schedules = relationship("ProductionSchedule", back_populates="project")


class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    goal = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="sprints")
    tasks = relationship("Task", back_populates="sprint")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    sprint_id = Column(Integer, ForeignKey("sprints.id"), nullable=True)
    parent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    
    task_key = Column(String(30), unique=True, nullable=False)  # e.g., PRJ-001-T-001
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    task_type = Column(Enum(TaskType), default=TaskType.TASK)
    status = Column(Enum(TaskStatus), default=TaskStatus.BACKLOG)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    
    # Assignment
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Time tracking
    estimated_hours = Column(Numeric(8, 2), nullable=True)
    logged_hours = Column(Numeric(8, 2), default=0)
    
    # Dates
    due_date = Column(Date, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Video production specific
    stage = Column(String(50), nullable=True)  # pre-production, production, post-production
    scene_number = Column(String(20), nullable=True)
    shot_list = Column(Text, nullable=True)
    
    # Kanban position
    position = Column(Integer, default=0)
    
    # Labels/Tags (JSON string)
    labels = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="tasks")
    sprint = relationship("Sprint", back_populates="tasks")
    assignee = relationship("User", foreign_keys=[assignee_id], back_populates="assigned_tasks")
    creator = relationship("User", foreign_keys=[created_by_id], back_populates="created_tasks")
    parent_task = relationship("Task", remote_side=[id], backref="subtasks")
    comments = relationship("Comment", back_populates="task")
    attachments = relationship("TaskAttachment", back_populates="task")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    
    # For threaded comments
    parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")
    replies = relationship("Comment", backref="parent", remote_side=[id])


class TaskAttachment(Base):
    __tablename__ = "task_attachments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    task = relationship("Task", back_populates="attachments")
