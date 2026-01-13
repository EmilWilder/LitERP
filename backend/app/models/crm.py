from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, Numeric, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class ClientType(str, enum.Enum):
    AGENCY = "agency"
    BRAND = "brand"
    PRODUCTION_COMPANY = "production_company"
    BROADCASTER = "broadcaster"
    STREAMING_PLATFORM = "streaming_platform"
    INDIVIDUAL = "individual"
    NON_PROFIT = "non_profit"
    GOVERNMENT = "government"
    OTHER = "other"


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class LeadSource(str, enum.Enum):
    WEBSITE = "website"
    REFERRAL = "referral"
    SOCIAL_MEDIA = "social_media"
    COLD_CALL = "cold_call"
    EMAIL_CAMPAIGN = "email_campaign"
    TRADE_SHOW = "trade_show"
    PARTNERSHIP = "partnership"
    REPEAT_CLIENT = "repeat_client"
    OTHER = "other"


class DealStage(str, enum.Enum):
    DISCOVERY = "discovery"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CONTRACT = "contract"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class InteractionType(str, enum.Enum):
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    PRESENTATION = "presentation"
    DEMO = "demo"
    NOTE = "note"


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    client_type = Column(Enum(ClientType), default=ClientType.BRAND)
    
    # Contact Info
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Address
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Business Info
    industry = Column(String(100), nullable=True)
    company_size = Column(String(50), nullable=True)
    annual_revenue = Column(Numeric(15, 2), nullable=True)
    
    # Account Management
    account_manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Billing
    billing_email = Column(String(255), nullable=True)
    payment_terms = Column(Integer, default=30)  # Days
    tax_id = Column(String(50), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    contacts = relationship("Contact", back_populates="client")
    projects = relationship("Project", back_populates="client")
    deals = relationship("Deal", back_populates="client")
    invoices = relationship("Invoice", back_populates="client")
    interactions = relationship("Interaction", back_populates="client")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    mobile = Column(String(50), nullable=True)
    
    job_title = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    
    # Social Media
    linkedin = Column(String(255), nullable=True)
    twitter = Column(String(255), nullable=True)
    
    is_primary = Column(Boolean, default=False)
    is_decision_maker = Column(Boolean, default=False)
    
    notes = Column(Text, nullable=True)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    client = relationship("Client", back_populates="contacts")
    leads = relationship("Lead", back_populates="contact")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    
    # Lead Info
    title = Column(String(255), nullable=False)  # e.g., "Corporate Video Project"
    description = Column(Text, nullable=True)
    
    # Contact Info (if not linked to existing contact)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    contact_name = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    company_name = Column(String(255), nullable=True)
    
    # Lead Details
    source = Column(Enum(LeadSource), default=LeadSource.WEBSITE)
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    
    # Value
    estimated_value = Column(Numeric(15, 2), nullable=True)
    probability = Column(Integer, default=0)  # Percentage
    
    # Assignment
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Project Type Interest
    project_type_interest = Column(String(100), nullable=True)
    
    # Follow-up
    next_follow_up = Column(DateTime(timezone=True), nullable=True)
    
    # Conversion
    converted_to_deal_id = Column(Integer, ForeignKey("deals.id"), nullable=True)
    converted_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    contact = relationship("Contact", back_populates="leads")


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    
    stage = Column(Enum(DealStage), default=DealStage.DISCOVERY)
    
    # Value
    amount = Column(Numeric(15, 2), default=0)
    probability = Column(Integer, default=0)
    expected_revenue = Column(Numeric(15, 2), default=0)
    
    # Dates
    expected_close_date = Column(Date, nullable=True)
    actual_close_date = Column(Date, nullable=True)
    
    # Assignment
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Related Project
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    # Win/Loss Info
    win_reason = Column(Text, nullable=True)
    loss_reason = Column(Text, nullable=True)
    competitor = Column(String(255), nullable=True)
    
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    client = relationship("Client", back_populates="deals")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    
    interaction_type = Column(Enum(InteractionType), nullable=False)
    subject = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    
    # Meeting/Call details
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    outcome = Column(Text, nullable=True)
    
    # Follow-up
    follow_up_date = Column(DateTime(timezone=True), nullable=True)
    follow_up_notes = Column(Text, nullable=True)
    
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    client = relationship("Client", back_populates="interactions")
