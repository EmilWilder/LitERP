from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ...core import get_db
from ...models.user import User
from ...models.production import ProductionSchedule, CrewAssignment, Location, ShootDay, ScheduleStatus
from ...schemas.production import (
    ProductionScheduleCreate, ProductionScheduleUpdate, ProductionScheduleResponse,
    CrewAssignmentCreate, CrewAssignmentUpdate, CrewAssignmentResponse,
    LocationCreate, LocationUpdate, LocationResponse,
    ShootDayCreate, ShootDayUpdate, ShootDayResponse
)
from .auth import get_current_active_user

router = APIRouter()


# Locations
@router.get("/locations", response_model=List[LocationResponse])
async def list_locations(
    skip: int = 0,
    limit: int = 100,
    location_type: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Location).where(Location.is_active == True)
    if location_type:
        query = query.where(Location.location_type == location_type)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/locations", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_in: LocationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    location = Location(**location_in.model_dump())
    db.add(location)
    await db.commit()
    await db.refresh(location)
    return location


@router.get("/locations/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.put("/locations/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: int,
    location_in: LocationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    for field, value in location_in.model_dump(exclude_unset=True).items():
        setattr(location, field, value)
    
    await db.commit()
    await db.refresh(location)
    return location


# Production Schedules
@router.get("/schedules", response_model=List[ProductionScheduleResponse])
async def list_schedules(
    skip: int = 0,
    limit: int = 100,
    project_id: int = None,
    status: ScheduleStatus = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(ProductionSchedule)
    if project_id:
        query = query.where(ProductionSchedule.project_id == project_id)
    if status:
        query = query.where(ProductionSchedule.status == status)
    result = await db.execute(query.order_by(ProductionSchedule.date).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/schedules", response_model=ProductionScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_in: ProductionScheduleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    schedule = ProductionSchedule(**schedule_in.model_dump())
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    return schedule


@router.get("/schedules/{schedule_id}", response_model=ProductionScheduleResponse)
async def get_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(ProductionSchedule).where(ProductionSchedule.id == schedule_id))
    schedule = result.scalar_one_or_none()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@router.put("/schedules/{schedule_id}", response_model=ProductionScheduleResponse)
async def update_schedule(
    schedule_id: int,
    schedule_in: ProductionScheduleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(ProductionSchedule).where(ProductionSchedule.id == schedule_id))
    schedule = result.scalar_one_or_none()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    for field, value in schedule_in.model_dump(exclude_unset=True).items():
        setattr(schedule, field, value)
    
    await db.commit()
    await db.refresh(schedule)
    return schedule


@router.delete("/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(ProductionSchedule).where(ProductionSchedule.id == schedule_id))
    schedule = result.scalar_one_or_none()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    await db.delete(schedule)
    await db.commit()


# Crew Assignments
@router.get("/schedules/{schedule_id}/crew", response_model=List[CrewAssignmentResponse])
async def list_crew_assignments(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(CrewAssignment).where(CrewAssignment.schedule_id == schedule_id)
    )
    return result.scalars().all()


@router.post("/crew", response_model=CrewAssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_crew_assignment(
    assignment_in: CrewAssignmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    assignment = CrewAssignment(**assignment_in.model_dump())
    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)
    return assignment


@router.put("/crew/{assignment_id}", response_model=CrewAssignmentResponse)
async def update_crew_assignment(
    assignment_id: int,
    assignment_in: CrewAssignmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(CrewAssignment).where(CrewAssignment.id == assignment_id))
    assignment = result.scalar_one_or_none()
    if not assignment:
        raise HTTPException(status_code=404, detail="Crew assignment not found")
    
    for field, value in assignment_in.model_dump(exclude_unset=True).items():
        setattr(assignment, field, value)
    
    await db.commit()
    await db.refresh(assignment)
    return assignment


@router.delete("/crew/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crew_assignment(
    assignment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(CrewAssignment).where(CrewAssignment.id == assignment_id))
    assignment = result.scalar_one_or_none()
    if not assignment:
        raise HTTPException(status_code=404, detail="Crew assignment not found")
    
    await db.delete(assignment)
    await db.commit()


# Shoot Days
@router.get("/schedules/{schedule_id}/shoot-days", response_model=List[ShootDayResponse])
async def list_shoot_days(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(ShootDay)
        .where(ShootDay.schedule_id == schedule_id)
        .order_by(ShootDay.date)
    )
    return result.scalars().all()


@router.post("/shoot-days", response_model=ShootDayResponse, status_code=status.HTTP_201_CREATED)
async def create_shoot_day(
    shoot_day_in: ShootDayCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    shoot_day = ShootDay(**shoot_day_in.model_dump())
    db.add(shoot_day)
    await db.commit()
    await db.refresh(shoot_day)
    return shoot_day


@router.put("/shoot-days/{shoot_day_id}", response_model=ShootDayResponse)
async def update_shoot_day(
    shoot_day_id: int,
    shoot_day_in: ShootDayUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(ShootDay).where(ShootDay.id == shoot_day_id))
    shoot_day = result.scalar_one_or_none()
    if not shoot_day:
        raise HTTPException(status_code=404, detail="Shoot day not found")
    
    for field, value in shoot_day_in.model_dump(exclude_unset=True).items():
        setattr(shoot_day, field, value)
    
    await db.commit()
    await db.refresh(shoot_day)
    return shoot_day
