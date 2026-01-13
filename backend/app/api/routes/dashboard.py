from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any
from datetime import datetime, timedelta

from ...core import get_db
from ...models.user import User
from ...models.project import Project, Task, ProjectStatus, TaskStatus
from ...models.crm import Client, Lead, Deal, LeadStatus, DealStage
from ...models.accounting import Invoice, Expense, InvoiceStatus
from ...models.equipment import Equipment, EquipmentStatus
from ...models.hr import Employee, LeaveRequest, LeaveStatus
from ...models.production import ProductionSchedule, ScheduleStatus
from .auth import get_current_active_user

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get comprehensive dashboard statistics"""
    
    # Project stats
    active_projects = await db.execute(
        select(func.count(Project.id)).where(
            Project.is_archived == False,
            Project.status.notin_([ProjectStatus.COMPLETED, ProjectStatus.CANCELLED])
        )
    )
    completed_projects = await db.execute(
        select(func.count(Project.id)).where(Project.status == ProjectStatus.COMPLETED)
    )
    
    # Task stats
    total_tasks = await db.execute(select(func.count(Task.id)))
    tasks_in_progress = await db.execute(
        select(func.count(Task.id)).where(Task.status == TaskStatus.IN_PROGRESS)
    )
    tasks_completed = await db.execute(
        select(func.count(Task.id)).where(Task.status == TaskStatus.DONE)
    )
    
    # CRM stats
    active_clients = await db.execute(
        select(func.count(Client.id)).where(Client.is_active == True)
    )
    new_leads = await db.execute(
        select(func.count(Lead.id)).where(Lead.status == LeadStatus.NEW)
    )
    open_deals = await db.execute(
        select(func.count(Deal.id)).where(
            Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST])
        )
    )
    deal_value = await db.execute(
        select(func.sum(Deal.amount)).where(
            Deal.stage.notin_([DealStage.CLOSED_WON, DealStage.CLOSED_LOST])
        )
    )
    
    # Financial stats
    pending_invoices = await db.execute(
        select(func.count(Invoice.id)).where(
            Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.VIEWED, InvoiceStatus.PARTIAL])
        )
    )
    pending_invoice_amount = await db.execute(
        select(func.sum(Invoice.balance_due)).where(
            Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.VIEWED, InvoiceStatus.PARTIAL])
        )
    )
    overdue_invoices = await db.execute(
        select(func.count(Invoice.id)).where(Invoice.status == InvoiceStatus.OVERDUE)
    )
    
    # Equipment stats
    available_equipment = await db.execute(
        select(func.count(Equipment.id)).where(
            Equipment.is_active == True,
            Equipment.status == EquipmentStatus.AVAILABLE
        )
    )
    equipment_in_use = await db.execute(
        select(func.count(Equipment.id)).where(
            Equipment.is_active == True,
            Equipment.status == EquipmentStatus.IN_USE
        )
    )
    
    # HR stats
    total_employees = await db.execute(
        select(func.count(Employee.id)).where(Employee.is_active == True)
    )
    pending_leave = await db.execute(
        select(func.count(LeaveRequest.id)).where(LeaveRequest.status == LeaveStatus.PENDING)
    )
    
    # Production stats - upcoming shoots
    today = datetime.utcnow().date()
    upcoming_shoots = await db.execute(
        select(func.count(ProductionSchedule.id)).where(
            ProductionSchedule.date >= today,
            ProductionSchedule.status.in_([ScheduleStatus.TENTATIVE, ScheduleStatus.CONFIRMED])
        )
    )
    
    return {
        "projects": {
            "active": active_projects.scalar() or 0,
            "completed": completed_projects.scalar() or 0
        },
        "tasks": {
            "total": total_tasks.scalar() or 0,
            "in_progress": tasks_in_progress.scalar() or 0,
            "completed": tasks_completed.scalar() or 0
        },
        "crm": {
            "active_clients": active_clients.scalar() or 0,
            "new_leads": new_leads.scalar() or 0,
            "open_deals": open_deals.scalar() or 0,
            "pipeline_value": float(deal_value.scalar() or 0)
        },
        "finance": {
            "pending_invoices": pending_invoices.scalar() or 0,
            "pending_amount": float(pending_invoice_amount.scalar() or 0),
            "overdue_invoices": overdue_invoices.scalar() or 0
        },
        "equipment": {
            "available": available_equipment.scalar() or 0,
            "in_use": equipment_in_use.scalar() or 0
        },
        "hr": {
            "total_employees": total_employees.scalar() or 0,
            "pending_leave_requests": pending_leave.scalar() or 0
        },
        "production": {
            "upcoming_shoots": upcoming_shoots.scalar() or 0
        }
    }


@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get recent activity across all modules"""
    
    # Recent projects
    recent_projects_result = await db.execute(
        select(Project)
        .order_by(Project.updated_at.desc().nullsfirst(), Project.created_at.desc())
        .limit(5)
    )
    recent_projects = recent_projects_result.scalars().all()
    
    # Recent tasks
    recent_tasks_result = await db.execute(
        select(Task)
        .order_by(Task.updated_at.desc().nullsfirst(), Task.created_at.desc())
        .limit(5)
    )
    recent_tasks = recent_tasks_result.scalars().all()
    
    # Recent leads
    recent_leads_result = await db.execute(
        select(Lead)
        .order_by(Lead.created_at.desc())
        .limit(5)
    )
    recent_leads = recent_leads_result.scalars().all()
    
    return {
        "recent_projects": [
            {"id": p.id, "name": p.name, "code": p.code, "status": p.status.value}
            for p in recent_projects
        ],
        "recent_tasks": [
            {"id": t.id, "title": t.title, "task_key": t.task_key, "status": t.status.value}
            for t in recent_tasks
        ],
        "recent_leads": [
            {"id": l.id, "title": l.title, "status": l.status.value}
            for l in recent_leads
        ]
    }


@router.get("/my-tasks")
async def get_my_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get tasks assigned to current user"""
    result = await db.execute(
        select(Task)
        .where(
            Task.assignee_id == current_user.id,
            Task.status != TaskStatus.DONE
        )
        .order_by(Task.due_date.asc().nullslast(), Task.priority.desc())
        .limit(10)
    )
    tasks = result.scalars().all()
    
    return [
        {
            "id": t.id,
            "title": t.title,
            "task_key": t.task_key,
            "status": t.status.value,
            "priority": t.priority.value,
            "due_date": t.due_date.isoformat() if t.due_date else None
        }
        for t in tasks
    ]
