from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, time
from ..models.production import ScheduleStatus, ShootType, CrewRole, LocationType


class LocationBase(BaseModel):
    name: str
    location_type: LocationType = LocationType.OTHER


class LocationCreate(LocationBase):
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    has_power: bool = True
    has_parking: bool = False
    has_bathroom: bool = True
    has_wifi: bool = False
    max_crew_size: Optional[int] = None
    rental_rate: Optional[float] = None
    rental_terms: Optional[str] = None
    permit_required: bool = False
    permit_notes: Optional[str] = None
    insurance_required: bool = False
    noise_restrictions: Optional[str] = None
    time_restrictions: Optional[str] = None
    photos: Optional[str] = None
    notes: Optional[str] = None


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    location_type: Optional[LocationType] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    has_power: Optional[bool] = None
    has_parking: Optional[bool] = None
    has_bathroom: Optional[bool] = None
    has_wifi: Optional[bool] = None
    max_crew_size: Optional[int] = None
    rental_rate: Optional[float] = None
    rental_terms: Optional[str] = None
    permit_required: Optional[bool] = None
    permit_notes: Optional[str] = None
    insurance_required: Optional[bool] = None
    noise_restrictions: Optional[str] = None
    time_restrictions: Optional[str] = None
    photos: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class LocationResponse(LocationBase):
    id: int
    address_line1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    has_power: bool
    has_parking: bool
    has_bathroom: bool
    has_wifi: bool
    max_crew_size: Optional[int] = None
    rental_rate: Optional[float] = None
    permit_required: bool
    insurance_required: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CrewAssignmentBase(BaseModel):
    role: CrewRole


class CrewAssignmentCreate(CrewAssignmentBase):
    schedule_id: int
    employee_id: Optional[int] = None
    external_name: Optional[str] = None
    external_email: Optional[str] = None
    external_phone: Optional[str] = None
    call_time: Optional[time] = None
    day_rate: Optional[float] = None
    notes: Optional[str] = None


class CrewAssignmentUpdate(BaseModel):
    role: Optional[CrewRole] = None
    employee_id: Optional[int] = None
    external_name: Optional[str] = None
    external_email: Optional[str] = None
    external_phone: Optional[str] = None
    call_time: Optional[time] = None
    day_rate: Optional[float] = None
    is_confirmed: Optional[bool] = None
    confirmation_sent: Optional[bool] = None
    notes: Optional[str] = None


class CrewAssignmentResponse(CrewAssignmentBase):
    id: int
    schedule_id: int
    employee_id: Optional[int] = None
    external_name: Optional[str] = None
    external_email: Optional[str] = None
    external_phone: Optional[str] = None
    call_time: Optional[time] = None
    day_rate: Optional[float] = None
    is_confirmed: bool
    confirmation_sent: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ProductionScheduleBase(BaseModel):
    title: str
    date: date
    shoot_type: ShootType = ShootType.ON_LOCATION


class ProductionScheduleCreate(ProductionScheduleBase):
    project_id: int
    description: Optional[str] = None
    location_id: Optional[int] = None
    location_notes: Optional[str] = None
    call_time: Optional[time] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    wrap_time: Optional[time] = None
    weather_backup_date: Optional[date] = None
    scenes: Optional[str] = None
    shot_count: Optional[int] = None
    general_notes: Optional[str] = None
    parking_info: Optional[str] = None
    catering_info: Optional[str] = None
    nearest_hospital: Optional[str] = None
    production_manager_id: Optional[int] = None


class ProductionScheduleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    shoot_type: Optional[ShootType] = None
    status: Optional[ScheduleStatus] = None
    location_id: Optional[int] = None
    location_notes: Optional[str] = None
    date: Optional[date] = None
    call_time: Optional[time] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    wrap_time: Optional[time] = None
    weather_backup_date: Optional[date] = None
    scenes: Optional[str] = None
    shot_count: Optional[int] = None
    general_notes: Optional[str] = None
    parking_info: Optional[str] = None
    catering_info: Optional[str] = None
    nearest_hospital: Optional[str] = None
    production_manager_id: Optional[int] = None


class ProductionScheduleResponse(ProductionScheduleBase):
    id: int
    project_id: int
    description: Optional[str] = None
    status: ScheduleStatus
    location_id: Optional[int] = None
    location_notes: Optional[str] = None
    call_time: Optional[time] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    wrap_time: Optional[time] = None
    weather_backup_date: Optional[date] = None
    scenes: Optional[str] = None
    shot_count: Optional[int] = None
    general_notes: Optional[str] = None
    production_manager_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ShootDayBase(BaseModel):
    date: date


class ShootDayCreate(ShootDayBase):
    schedule_id: int
    day_number: Optional[int] = None
    total_shots: Optional[int] = None


class ShootDayUpdate(BaseModel):
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    scenes_completed: Optional[str] = None
    shots_completed: Optional[int] = None
    delays: Optional[str] = None
    issues: Optional[str] = None
    director_notes: Optional[str] = None
    producer_notes: Optional[str] = None
    weather_conditions: Optional[str] = None
    footage_shot: Optional[str] = None
    data_captured: Optional[str] = None


class ShootDayResponse(ShootDayBase):
    id: int
    schedule_id: int
    day_number: Optional[int] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    scenes_completed: Optional[str] = None
    shots_completed: int
    total_shots: Optional[int] = None
    delays: Optional[str] = None
    issues: Optional[str] = None
    director_notes: Optional[str] = None
    producer_notes: Optional[str] = None
    weather_conditions: Optional[str] = None
    footage_shot: Optional[str] = None
    data_captured: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
