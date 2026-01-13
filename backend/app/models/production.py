from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, Numeric, Date, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class ScheduleStatus(str, enum.Enum):
    TENTATIVE = "tentative"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"


class ShootType(str, enum.Enum):
    STUDIO = "studio"
    ON_LOCATION = "on_location"
    GREEN_SCREEN = "green_screen"
    INTERVIEW = "interview"
    B_ROLL = "b_roll"
    AERIAL = "aerial"
    UNDERWATER = "underwater"
    LIVE_EVENT = "live_event"
    OTHER = "other"


class CrewRole(str, enum.Enum):
    DIRECTOR = "director"
    PRODUCER = "producer"
    CINEMATOGRAPHER = "cinematographer"
    CAMERA_OPERATOR = "camera_operator"
    SOUND_MIXER = "sound_mixer"
    BOOM_OPERATOR = "boom_operator"
    GAFFER = "gaffer"
    GRIP = "grip"
    PRODUCTION_ASSISTANT = "production_assistant"
    MAKEUP_ARTIST = "makeup_artist"
    WARDROBE = "wardrobe"
    EDITOR = "editor"
    COLORIST = "colorist"
    VFX_ARTIST = "vfx_artist"
    MOTION_GRAPHICS = "motion_graphics"
    DRONE_OPERATOR = "drone_operator"
    SCRIPT_SUPERVISOR = "script_supervisor"
    ART_DIRECTOR = "art_director"
    SET_DESIGNER = "set_designer"
    RUNNER = "runner"
    OTHER = "other"


class LocationType(str, enum.Enum):
    STUDIO = "studio"
    OFFICE = "office"
    OUTDOOR = "outdoor"
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    NATURAL = "natural"
    VEHICLE = "vehicle"
    OTHER = "other"


class ProductionSchedule(Base):
    __tablename__ = "production_schedules"

    id = Column(Integer, primary_key=True, index=True)
    
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    shoot_type = Column(Enum(ShootType), default=ShootType.ON_LOCATION)
    status = Column(Enum(ScheduleStatus), default=ScheduleStatus.TENTATIVE)
    
    # Location
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    location_notes = Column(Text, nullable=True)
    
    # Timing
    date = Column(Date, nullable=False)
    call_time = Column(Time, nullable=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    wrap_time = Column(Time, nullable=True)
    
    # Weather backup (for outdoor shoots)
    weather_backup_date = Column(Date, nullable=True)
    
    # Scene/Shot info
    scenes = Column(Text, nullable=True)  # JSON string of scene numbers
    shot_count = Column(Integer, nullable=True)
    
    # Call sheet info
    general_notes = Column(Text, nullable=True)
    parking_info = Column(Text, nullable=True)
    catering_info = Column(Text, nullable=True)
    nearest_hospital = Column(String(255), nullable=True)
    
    # Contact
    production_manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="schedules")
    crew_assignments = relationship("CrewAssignment", back_populates="schedule")
    location = relationship("Location", back_populates="schedules")
    shoot_days = relationship("ShootDay", back_populates="schedule")


class CrewAssignment(Base):
    __tablename__ = "crew_assignments"

    id = Column(Integer, primary_key=True, index=True)
    
    schedule_id = Column(Integer, ForeignKey("production_schedules.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    
    # If external crew (freelancer)
    external_name = Column(String(255), nullable=True)
    external_email = Column(String(255), nullable=True)
    external_phone = Column(String(50), nullable=True)
    
    role = Column(Enum(CrewRole), nullable=False)
    
    # Call time specific to this crew member
    call_time = Column(Time, nullable=True)
    
    # Rate
    day_rate = Column(Numeric(10, 2), nullable=True)
    
    # Status
    is_confirmed = Column(Boolean, default=False)
    confirmation_sent = Column(Boolean, default=False)
    
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    schedule = relationship("ProductionSchedule", back_populates="crew_assignments")
    employee = relationship("Employee", back_populates="crew_assignments")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(255), nullable=False)
    location_type = Column(Enum(LocationType), default=LocationType.OTHER)
    
    # Address
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Coordinates
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    
    # Contact
    contact_name = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    contact_email = Column(String(255), nullable=True)
    
    # Facilities
    has_power = Column(Boolean, default=True)
    has_parking = Column(Boolean, default=False)
    has_bathroom = Column(Boolean, default=True)
    has_wifi = Column(Boolean, default=False)
    
    # Capacity
    max_crew_size = Column(Integer, nullable=True)
    
    # Rental Info
    rental_rate = Column(Numeric(10, 2), nullable=True)
    rental_terms = Column(Text, nullable=True)
    
    # Requirements
    permit_required = Column(Boolean, default=False)
    permit_notes = Column(Text, nullable=True)
    insurance_required = Column(Boolean, default=False)
    
    # Restrictions
    noise_restrictions = Column(Text, nullable=True)
    time_restrictions = Column(Text, nullable=True)
    
    # Media
    photos = Column(Text, nullable=True)  # JSON array of URLs
    
    notes = Column(Text, nullable=True)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    schedules = relationship("ProductionSchedule", back_populates="location")


class ShootDay(Base):
    __tablename__ = "shoot_days"

    id = Column(Integer, primary_key=True, index=True)
    
    schedule_id = Column(Integer, ForeignKey("production_schedules.id"), nullable=False)
    
    # Day summary
    day_number = Column(Integer, nullable=True)  # Day 1, Day 2, etc.
    date = Column(Date, nullable=False)
    
    # Actual times
    actual_start = Column(DateTime(timezone=True), nullable=True)
    actual_end = Column(DateTime(timezone=True), nullable=True)
    
    # Progress
    scenes_completed = Column(Text, nullable=True)  # JSON array
    shots_completed = Column(Integer, default=0)
    total_shots = Column(Integer, nullable=True)
    
    # Issues
    delays = Column(Text, nullable=True)
    issues = Column(Text, nullable=True)
    
    # Daily report
    director_notes = Column(Text, nullable=True)
    producer_notes = Column(Text, nullable=True)
    
    # Weather (for outdoor shoots)
    weather_conditions = Column(String(100), nullable=True)
    
    # Footage
    footage_shot = Column(String(50), nullable=True)  # e.g., "2h 30m"
    data_captured = Column(String(50), nullable=True)  # e.g., "500GB"
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    schedule = relationship("ProductionSchedule", back_populates="shoot_days")
