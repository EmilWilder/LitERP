from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from ..models.equipment import EquipmentCategory, EquipmentStatus, BookingStatus, MaintenanceType


class EquipmentBase(BaseModel):
    name: str
    code: str
    category: EquipmentCategory


class EquipmentCreate(EquipmentBase):
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    description: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = None
    vendor: Optional[str] = None
    warranty_expiry: Optional[date] = None
    current_value: Optional[float] = None
    depreciation_rate: Optional[float] = None
    storage_location: Optional[str] = None
    is_rentable: bool = True
    daily_rate: Optional[float] = None
    weekly_rate: Optional[float] = None
    specifications: Optional[str] = None
    accessories: Optional[str] = None
    insurance_policy: Optional[str] = None
    insured_value: Optional[float] = None
    image_url: Optional[str] = None
    notes: Optional[str] = None


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[EquipmentCategory] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    description: Optional[str] = None
    status: Optional[EquipmentStatus] = None
    condition_notes: Optional[str] = None
    current_value: Optional[float] = None
    storage_location: Optional[str] = None
    current_location: Optional[str] = None
    is_rentable: Optional[bool] = None
    daily_rate: Optional[float] = None
    weekly_rate: Optional[float] = None
    specifications: Optional[str] = None
    accessories: Optional[str] = None
    image_url: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class EquipmentResponse(EquipmentBase):
    id: int
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    description: Optional[str] = None
    status: EquipmentStatus
    condition_notes: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    storage_location: Optional[str] = None
    current_location: Optional[str] = None
    is_rentable: bool
    daily_rate: Optional[float] = None
    weekly_rate: Optional[float] = None
    last_maintenance_date: Optional[date] = None
    next_maintenance_date: Optional[date] = None
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class EquipmentBookingBase(BaseModel):
    start_date: datetime
    end_date: datetime
    purpose: Optional[str] = None


class EquipmentBookingCreate(EquipmentBookingBase):
    equipment_id: int
    project_id: Optional[int] = None
    booked_by_id: int
    notes: Optional[str] = None


class EquipmentBookingUpdate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[BookingStatus] = None
    purpose: Optional[str] = None
    return_condition: Optional[str] = None
    damage_reported: Optional[bool] = None
    damage_notes: Optional[str] = None
    notes: Optional[str] = None


class EquipmentBookingResponse(EquipmentBookingBase):
    id: int
    equipment_id: int
    project_id: Optional[int] = None
    booked_by_id: int
    status: BookingStatus
    checked_out_at: Optional[datetime] = None
    returned_at: Optional[datetime] = None
    return_condition: Optional[str] = None
    damage_reported: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MaintenanceRecordBase(BaseModel):
    maintenance_type: MaintenanceType
    description: str


class MaintenanceRecordCreate(MaintenanceRecordBase):
    equipment_id: int
    scheduled_date: Optional[date] = None
    cost: Optional[float] = None
    vendor: Optional[str] = None
    performed_by: Optional[str] = None
    performed_by_id: Optional[int] = None
    findings: Optional[str] = None
    parts_replaced: Optional[str] = None
    next_maintenance_date: Optional[date] = None
    notes: Optional[str] = None


class MaintenanceRecordUpdate(BaseModel):
    maintenance_type: Optional[MaintenanceType] = None
    description: Optional[str] = None
    scheduled_date: Optional[date] = None
    completed_date: Optional[date] = None
    cost: Optional[float] = None
    vendor: Optional[str] = None
    performed_by: Optional[str] = None
    findings: Optional[str] = None
    parts_replaced: Optional[str] = None
    next_maintenance_date: Optional[date] = None
    notes: Optional[str] = None


class MaintenanceRecordResponse(MaintenanceRecordBase):
    id: int
    equipment_id: int
    scheduled_date: Optional[date] = None
    completed_date: Optional[date] = None
    cost: Optional[float] = None
    vendor: Optional[str] = None
    performed_by: Optional[str] = None
    performed_by_id: Optional[int] = None
    findings: Optional[str] = None
    parts_replaced: Optional[str] = None
    next_maintenance_date: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True
