from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, Numeric, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class EquipmentCategory(str, enum.Enum):
    CAMERA = "camera"
    LENS = "lens"
    LIGHTING = "lighting"
    AUDIO = "audio"
    GRIP = "grip"
    SUPPORT = "support"  # Tripods, gimbals, etc.
    DRONE = "drone"
    MONITOR = "monitor"
    STORAGE = "storage"
    COMPUTER = "computer"
    SOFTWARE = "software"
    VEHICLE = "vehicle"
    OTHER = "other"


class EquipmentStatus(str, enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"
    DAMAGED = "damaged"
    RETIRED = "retired"


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CHECKED_OUT = "checked_out"
    RETURNED = "returned"
    CANCELLED = "cancelled"


class MaintenanceType(str, enum.Enum):
    ROUTINE = "routine"
    REPAIR = "repair"
    CALIBRATION = "calibration"
    CLEANING = "cleaning"
    UPGRADE = "upgrade"


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False)  # Asset tag
    category = Column(Enum(EquipmentCategory), nullable=False)
    
    # Details
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    serial_number = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    
    # Status
    status = Column(Enum(EquipmentStatus), default=EquipmentStatus.AVAILABLE)
    condition_notes = Column(Text, nullable=True)
    
    # Purchase Info
    purchase_date = Column(Date, nullable=True)
    purchase_price = Column(Numeric(15, 2), nullable=True)
    vendor = Column(String(255), nullable=True)
    warranty_expiry = Column(Date, nullable=True)
    
    # Depreciation
    current_value = Column(Numeric(15, 2), nullable=True)
    depreciation_rate = Column(Numeric(5, 2), nullable=True)  # Annual percentage
    
    # Location
    storage_location = Column(String(255), nullable=True)
    current_location = Column(String(255), nullable=True)
    
    # Rental Info (if equipment can be rented)
    is_rentable = Column(Boolean, default=True)
    daily_rate = Column(Numeric(10, 2), nullable=True)
    weekly_rate = Column(Numeric(10, 2), nullable=True)
    
    # Technical Specs (JSON string)
    specifications = Column(Text, nullable=True)
    
    # Accessories included
    accessories = Column(Text, nullable=True)
    
    # Insurance
    insurance_policy = Column(String(100), nullable=True)
    insured_value = Column(Numeric(15, 2), nullable=True)
    
    # Maintenance
    last_maintenance_date = Column(Date, nullable=True)
    next_maintenance_date = Column(Date, nullable=True)
    
    # Images
    image_url = Column(String(500), nullable=True)
    
    notes = Column(Text, nullable=True)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    bookings = relationship("EquipmentBooking", back_populates="equipment")
    maintenance_records = relationship("MaintenanceRecord", back_populates="equipment")


class EquipmentBooking(Base):
    __tablename__ = "equipment_bookings"

    id = Column(Integer, primary_key=True, index=True)
    
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    booked_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Booking Period
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # Actual Usage
    checked_out_at = Column(DateTime(timezone=True), nullable=True)
    checked_out_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    returned_at = Column(DateTime(timezone=True), nullable=True)
    returned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Status
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    
    # Condition on return
    return_condition = Column(Text, nullable=True)
    damage_reported = Column(Boolean, default=False)
    damage_notes = Column(Text, nullable=True)
    
    # Purpose
    purpose = Column(Text, nullable=True)
    
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    equipment = relationship("Equipment", back_populates="bookings")


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    
    maintenance_type = Column(Enum(MaintenanceType), nullable=False)
    description = Column(Text, nullable=False)
    
    # Date
    scheduled_date = Column(Date, nullable=True)
    completed_date = Column(Date, nullable=True)
    
    # Cost
    cost = Column(Numeric(10, 2), nullable=True)
    vendor = Column(String(255), nullable=True)
    
    # Performed by
    performed_by = Column(String(255), nullable=True)
    performed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Results
    findings = Column(Text, nullable=True)
    parts_replaced = Column(Text, nullable=True)
    
    # Next maintenance
    next_maintenance_date = Column(Date, nullable=True)
    
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_records")
