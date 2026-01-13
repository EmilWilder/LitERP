from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from ...core import get_db
from ...models.user import User
from ...models.equipment import Equipment, EquipmentBooking, MaintenanceRecord, EquipmentStatus, BookingStatus
from ...schemas.equipment import (
    EquipmentCreate, EquipmentUpdate, EquipmentResponse,
    EquipmentBookingCreate, EquipmentBookingUpdate, EquipmentBookingResponse,
    MaintenanceRecordCreate, MaintenanceRecordUpdate, MaintenanceRecordResponse
)
from .auth import get_current_active_user

router = APIRouter()


# Equipment
@router.get("/", response_model=List[EquipmentResponse])
async def list_equipment(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    status: EquipmentStatus = None,
    is_available: bool = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Equipment).where(Equipment.is_active == True)
    if category:
        query = query.where(Equipment.category == category)
    if status:
        query = query.where(Equipment.status == status)
    if is_available is True:
        query = query.where(Equipment.status == EquipmentStatus.AVAILABLE)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_equipment(
    equipment_in: EquipmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    equipment = Equipment(**equipment_in.model_dump())
    db.add(equipment)
    await db.commit()
    await db.refresh(equipment)
    return equipment


@router.get("/{equipment_id}", response_model=EquipmentResponse)
async def get_equipment(
    equipment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Equipment).where(Equipment.id == equipment_id))
    equipment = result.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.put("/{equipment_id}", response_model=EquipmentResponse)
async def update_equipment(
    equipment_id: int,
    equipment_in: EquipmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Equipment).where(Equipment.id == equipment_id))
    equipment = result.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    for field, value in equipment_in.model_dump(exclude_unset=True).items():
        setattr(equipment, field, value)
    
    await db.commit()
    await db.refresh(equipment)
    return equipment


@router.delete("/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipment(
    equipment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Equipment).where(Equipment.id == equipment_id))
    equipment = result.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    equipment.is_active = False
    await db.commit()


# Bookings
@router.get("/bookings/all", response_model=List[EquipmentBookingResponse])
async def list_all_bookings(
    skip: int = 0,
    limit: int = 100,
    status: BookingStatus = None,
    equipment_id: int = None,
    project_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(EquipmentBooking)
    if status:
        query = query.where(EquipmentBooking.status == status)
    if equipment_id:
        query = query.where(EquipmentBooking.equipment_id == equipment_id)
    if project_id:
        query = query.where(EquipmentBooking.project_id == project_id)
    result = await db.execute(query.order_by(EquipmentBooking.start_date).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{equipment_id}/bookings", response_model=List[EquipmentBookingResponse])
async def list_equipment_bookings(
    equipment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(EquipmentBooking)
        .where(EquipmentBooking.equipment_id == equipment_id)
        .order_by(EquipmentBooking.start_date)
    )
    return result.scalars().all()


@router.post("/bookings", response_model=EquipmentBookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_in: EquipmentBookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check equipment exists and is available
    result = await db.execute(select(Equipment).where(Equipment.id == booking_in.equipment_id))
    equipment = result.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # Check for overlapping bookings
    overlap_result = await db.execute(
        select(EquipmentBooking).where(
            EquipmentBooking.equipment_id == booking_in.equipment_id,
            EquipmentBooking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED, BookingStatus.CHECKED_OUT]),
            EquipmentBooking.start_date < booking_in.end_date,
            EquipmentBooking.end_date > booking_in.start_date
        )
    )
    if overlap_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Equipment is already booked for this period")
    
    booking = EquipmentBooking(**booking_in.model_dump())
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking


@router.put("/bookings/{booking_id}", response_model=EquipmentBookingResponse)
async def update_booking(
    booking_id: int,
    booking_in: EquipmentBookingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(EquipmentBooking).where(EquipmentBooking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    update_data = booking_in.model_dump(exclude_unset=True)
    
    # Handle status changes
    if update_data.get("status") == BookingStatus.CHECKED_OUT:
        booking.checked_out_at = datetime.utcnow()
        booking.checked_out_by_id = current_user.id
        # Update equipment status
        eq_result = await db.execute(select(Equipment).where(Equipment.id == booking.equipment_id))
        equipment = eq_result.scalar_one()
        equipment.status = EquipmentStatus.IN_USE
    elif update_data.get("status") == BookingStatus.RETURNED:
        booking.returned_at = datetime.utcnow()
        booking.returned_to_id = current_user.id
        # Update equipment status
        eq_result = await db.execute(select(Equipment).where(Equipment.id == booking.equipment_id))
        equipment = eq_result.scalar_one()
        equipment.status = EquipmentStatus.AVAILABLE
    
    for field, value in update_data.items():
        setattr(booking, field, value)
    
    await db.commit()
    await db.refresh(booking)
    return booking


# Maintenance
@router.get("/{equipment_id}/maintenance", response_model=List[MaintenanceRecordResponse])
async def list_maintenance_records(
    equipment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(MaintenanceRecord)
        .where(MaintenanceRecord.equipment_id == equipment_id)
        .order_by(MaintenanceRecord.created_at.desc())
    )
    return result.scalars().all()


@router.post("/maintenance", response_model=MaintenanceRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_maintenance_record(
    maintenance_in: MaintenanceRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    maintenance = MaintenanceRecord(**maintenance_in.model_dump())
    db.add(maintenance)
    
    # Update equipment maintenance dates
    eq_result = await db.execute(select(Equipment).where(Equipment.id == maintenance_in.equipment_id))
    equipment = eq_result.scalar_one_or_none()
    if equipment and maintenance_in.next_maintenance_date:
        equipment.next_maintenance_date = maintenance_in.next_maintenance_date
    
    await db.commit()
    await db.refresh(maintenance)
    return maintenance


@router.put("/maintenance/{maintenance_id}", response_model=MaintenanceRecordResponse)
async def update_maintenance_record(
    maintenance_id: int,
    maintenance_in: MaintenanceRecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(MaintenanceRecord).where(MaintenanceRecord.id == maintenance_id))
    maintenance = result.scalar_one_or_none()
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    
    update_data = maintenance_in.model_dump(exclude_unset=True)
    
    # If completing maintenance, update equipment
    if update_data.get("completed_date"):
        eq_result = await db.execute(select(Equipment).where(Equipment.id == maintenance.equipment_id))
        equipment = eq_result.scalar_one()
        equipment.last_maintenance_date = update_data["completed_date"]
        if update_data.get("next_maintenance_date"):
            equipment.next_maintenance_date = update_data["next_maintenance_date"]
    
    for field, value in update_data.items():
        setattr(maintenance, field, value)
    
    await db.commit()
    await db.refresh(maintenance)
    return maintenance
