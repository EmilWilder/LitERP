from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from ..models.hr import EmploymentType, LeaveType, LeaveStatus


class DepartmentBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    budget: Optional[float] = 0


class DepartmentCreate(DepartmentBase):
    manager_id: Optional[int] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None
    budget: Optional[float] = None
    is_active: Optional[bool] = None


class DepartmentResponse(DepartmentBase):
    id: int
    manager_id: Optional[int] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    employee_code: str
    job_title: str
    employment_type: EmploymentType = EmploymentType.FULL_TIME
    hire_date: date


class EmployeeCreate(EmployeeBase):
    user_id: int
    department_id: Optional[int] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    salary: Optional[float] = 0
    hourly_rate: Optional[float] = None
    skills: Optional[str] = None
    certifications: Optional[str] = None
    equipment_proficiency: Optional[str] = None


class EmployeeUpdate(BaseModel):
    department_id: Optional[int] = None
    job_title: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    salary: Optional[float] = None
    hourly_rate: Optional[float] = None
    skills: Optional[str] = None
    certifications: Optional[str] = None
    equipment_proficiency: Optional[str] = None
    annual_leave_balance: Optional[int] = None
    sick_leave_balance: Optional[int] = None
    is_active: Optional[bool] = None


class EmployeeResponse(EmployeeBase):
    id: int
    user_id: int
    department_id: Optional[int] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    salary: Optional[float] = None
    skills: Optional[str] = None
    annual_leave_balance: int
    sick_leave_balance: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LeaveRequestBase(BaseModel):
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: Optional[str] = None


class LeaveRequestCreate(LeaveRequestBase):
    employee_id: int


class LeaveRequestUpdate(BaseModel):
    status: Optional[LeaveStatus] = None
    rejection_reason: Optional[str] = None


class LeaveRequestResponse(LeaveRequestBase):
    id: int
    employee_id: int
    total_days: int
    status: LeaveStatus
    approved_by_id: Optional[int] = None
    approved_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AttendanceBase(BaseModel):
    date: date
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    notes: Optional[str] = None
    location: Optional[str] = None
    project_id: Optional[int] = None


class AttendanceCreate(AttendanceBase):
    employee_id: int


class AttendanceResponse(AttendanceBase):
    id: int
    employee_id: int
    total_hours: Optional[float] = None
    overtime_hours: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True
