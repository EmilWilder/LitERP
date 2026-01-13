from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from ...core import get_db
from ...models.user import User
from ...models.hr import Department, Employee, LeaveRequest, Attendance, LeaveStatus
from ...schemas.hr import (
    DepartmentCreate, DepartmentUpdate, DepartmentResponse,
    EmployeeCreate, EmployeeUpdate, EmployeeResponse,
    LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestResponse,
    AttendanceCreate, AttendanceResponse
)
from .auth import get_current_active_user

router = APIRouter()


# Departments
@router.get("/departments", response_model=List[DepartmentResponse])
async def list_departments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Department).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    dept_in: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    dept = Department(**dept_in.model_dump())
    db.add(dept)
    await db.commit()
    await db.refresh(dept)
    return dept


@router.get("/departments/{dept_id}", response_model=DepartmentResponse)
async def get_department(
    dept_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept


@router.put("/departments/{dept_id}", response_model=DepartmentResponse)
async def update_department(
    dept_id: int,
    dept_in: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    for field, value in dept_in.model_dump(exclude_unset=True).items():
        setattr(dept, field, value)
    
    await db.commit()
    await db.refresh(dept)
    return dept


# Employees
@router.get("/employees", response_model=List[EmployeeResponse])
async def list_employees(
    skip: int = 0,
    limit: int = 100,
    department_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Employee)
    if department_id:
        query = query.where(Employee.department_id == department_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    emp_in: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    emp = Employee(**emp_in.model_dump())
    db.add(emp)
    await db.commit()
    await db.refresh(emp)
    return emp


@router.get("/employees/{emp_id}", response_model=EmployeeResponse)
async def get_employee(
    emp_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Employee).where(Employee.id == emp_id))
    emp = result.scalar_one_or_none()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.put("/employees/{emp_id}", response_model=EmployeeResponse)
async def update_employee(
    emp_id: int,
    emp_in: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Employee).where(Employee.id == emp_id))
    emp = result.scalar_one_or_none()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for field, value in emp_in.model_dump(exclude_unset=True).items():
        setattr(emp, field, value)
    
    await db.commit()
    await db.refresh(emp)
    return emp


# Leave Requests
@router.get("/leave-requests", response_model=List[LeaveRequestResponse])
async def list_leave_requests(
    skip: int = 0,
    limit: int = 100,
    status: LeaveStatus = None,
    employee_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(LeaveRequest)
    if status:
        query = query.where(LeaveRequest.status == status)
    if employee_id:
        query = query.where(LeaveRequest.employee_id == employee_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/leave-requests", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_leave_request(
    leave_in: LeaveRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Calculate total days
    total_days = (leave_in.end_date - leave_in.start_date).days + 1
    
    leave = LeaveRequest(
        **leave_in.model_dump(),
        total_days=total_days
    )
    db.add(leave)
    await db.commit()
    await db.refresh(leave)
    return leave


@router.put("/leave-requests/{leave_id}", response_model=LeaveRequestResponse)
async def update_leave_request(
    leave_id: int,
    leave_in: LeaveRequestUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(LeaveRequest).where(LeaveRequest.id == leave_id))
    leave = result.scalar_one_or_none()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    update_data = leave_in.model_dump(exclude_unset=True)
    
    # Set approved_by and approved_at if status is changing to approved
    if update_data.get("status") == LeaveStatus.APPROVED:
        update_data["approved_by_id"] = current_user.id
        update_data["approved_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(leave, field, value)
    
    await db.commit()
    await db.refresh(leave)
    return leave


# Attendance
@router.get("/attendance", response_model=List[AttendanceResponse])
async def list_attendance(
    skip: int = 0,
    limit: int = 100,
    employee_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Attendance)
    if employee_id:
        query = query.where(Attendance.employee_id == employee_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/attendance", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def create_attendance(
    att_in: AttendanceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    att = Attendance(**att_in.model_dump())
    
    # Calculate total hours if both check_in and check_out provided
    if att.check_in and att.check_out:
        delta = att.check_out - att.check_in
        att.total_hours = round(delta.total_seconds() / 3600, 2)
    
    db.add(att)
    await db.commit()
    await db.refresh(att)
    return att
