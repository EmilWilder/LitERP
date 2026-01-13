from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date
from ..models.crm import ClientType, LeadStatus, LeadSource, DealStage, InteractionType


class ClientBase(BaseModel):
    name: str
    code: str
    client_type: ClientType = ClientType.BRAND


class ClientCreate(ClientBase):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    account_manager_id: Optional[int] = None
    billing_email: Optional[EmailStr] = None
    payment_terms: int = 30
    tax_id: Optional[str] = None
    notes: Optional[str] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    client_type: Optional[ClientType] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    account_manager_id: Optional[int] = None
    billing_email: Optional[EmailStr] = None
    payment_terms: Optional[int] = None
    tax_id: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class ClientResponse(ClientBase):
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    account_manager_id: Optional[int] = None
    payment_terms: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class ContactCreate(ContactBase):
    client_id: Optional[int] = None
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    is_primary: bool = False
    is_decision_maker: bool = False
    notes: Optional[str] = None


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    is_primary: Optional[bool] = None
    is_decision_maker: Optional[bool] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class ContactResponse(ContactBase):
    id: int
    client_id: Optional[int] = None
    job_title: Optional[str] = None
    is_primary: bool
    is_decision_maker: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LeadBase(BaseModel):
    title: str
    description: Optional[str] = None
    source: LeadSource = LeadSource.WEBSITE


class LeadCreate(LeadBase):
    contact_id: Optional[int] = None
    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    company_name: Optional[str] = None
    estimated_value: Optional[float] = None
    probability: int = 0
    assigned_to_id: Optional[int] = None
    project_type_interest: Optional[str] = None
    next_follow_up: Optional[datetime] = None


class LeadUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    source: Optional[LeadSource] = None
    status: Optional[LeadStatus] = None
    estimated_value: Optional[float] = None
    probability: Optional[int] = None
    assigned_to_id: Optional[int] = None
    project_type_interest: Optional[str] = None
    next_follow_up: Optional[datetime] = None


class LeadResponse(LeadBase):
    id: int
    status: LeadStatus
    contact_id: Optional[int] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    company_name: Optional[str] = None
    estimated_value: Optional[float] = None
    probability: int
    assigned_to_id: Optional[int] = None
    project_type_interest: Optional[str] = None
    next_follow_up: Optional[datetime] = None
    converted_to_deal_id: Optional[int] = None
    converted_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DealBase(BaseModel):
    name: str
    description: Optional[str] = None


class DealCreate(DealBase):
    client_id: int
    contact_id: Optional[int] = None
    amount: float = 0
    probability: int = 0
    expected_close_date: Optional[date] = None
    owner_id: Optional[int] = None
    notes: Optional[str] = None


class DealUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[DealStage] = None
    amount: Optional[float] = None
    probability: Optional[int] = None
    expected_close_date: Optional[date] = None
    actual_close_date: Optional[date] = None
    owner_id: Optional[int] = None
    project_id: Optional[int] = None
    win_reason: Optional[str] = None
    loss_reason: Optional[str] = None
    competitor: Optional[str] = None
    notes: Optional[str] = None


class DealResponse(DealBase):
    id: int
    client_id: int
    contact_id: Optional[int] = None
    stage: DealStage
    amount: float
    probability: int
    expected_revenue: float
    expected_close_date: Optional[date] = None
    actual_close_date: Optional[date] = None
    owner_id: Optional[int] = None
    project_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InteractionBase(BaseModel):
    interaction_type: InteractionType
    subject: str
    content: Optional[str] = None


class InteractionCreate(InteractionBase):
    client_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None
    lead_id: Optional[int] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    follow_up_notes: Optional[str] = None
    created_by_id: int


class InteractionResponse(InteractionBase):
    id: int
    client_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None
    lead_id: Optional[int] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True
