from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from ...core import get_db
from ...models.user import User
from ...models.crm import Client, Contact, Lead, Deal, Interaction
from ...schemas.crm import (
    ClientCreate, ClientUpdate, ClientResponse,
    ContactCreate, ContactUpdate, ContactResponse,
    LeadCreate, LeadUpdate, LeadResponse,
    DealCreate, DealUpdate, DealResponse,
    InteractionCreate, InteractionResponse
)
from .auth import get_current_active_user

router = APIRouter()


# Clients
@router.get("/clients", response_model=List[ClientResponse])
async def list_clients(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Client).where(Client.is_active == is_active)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/clients", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_in: ClientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    client = Client(**client_in.model_dump())
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client


@router.get("/clients/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/clients/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_in: ClientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    for field, value in client_in.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    
    await db.commit()
    await db.refresh(client)
    return client


# Contacts
@router.get("/contacts", response_model=List[ContactResponse])
async def list_contacts(
    skip: int = 0,
    limit: int = 100,
    client_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Contact).where(Contact.is_active == True)
    if client_id:
        query = query.where(Contact.client_id == client_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/contacts", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_in: ContactCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    contact = Contact(**contact_in.model_dump())
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_in: ContactUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    for field, value in contact_in.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    
    await db.commit()
    await db.refresh(contact)
    return contact


# Leads
@router.get("/leads", response_model=List[LeadResponse])
async def list_leads(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    assigned_to_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Lead)
    if status:
        query = query.where(Lead.status == status)
    if assigned_to_id:
        query = query.where(Lead.assigned_to_id == assigned_to_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/leads", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead_in: LeadCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    lead = Lead(**lead_in.model_dump())
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead


@router.get("/leads/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.put("/leads/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    lead_in: LeadUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    for field, value in lead_in.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    
    await db.commit()
    await db.refresh(lead)
    return lead


# Deals
@router.get("/deals", response_model=List[DealResponse])
async def list_deals(
    skip: int = 0,
    limit: int = 100,
    stage: str = None,
    client_id: int = None,
    owner_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Deal)
    if stage:
        query = query.where(Deal.stage == stage)
    if client_id:
        query = query.where(Deal.client_id == client_id)
    if owner_id:
        query = query.where(Deal.owner_id == owner_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/deals", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
async def create_deal(
    deal_in: DealCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    deal_data = deal_in.model_dump()
    deal_data["expected_revenue"] = deal_data["amount"] * deal_data["probability"] / 100
    deal = Deal(**deal_data)
    db.add(deal)
    await db.commit()
    await db.refresh(deal)
    return deal


@router.get("/deals/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.put("/deals/{deal_id}", response_model=DealResponse)
async def update_deal(
    deal_id: int,
    deal_in: DealUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    update_data = deal_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(deal, field, value)
    
    # Recalculate expected revenue
    deal.expected_revenue = deal.amount * deal.probability / 100
    
    await db.commit()
    await db.refresh(deal)
    return deal


# Interactions
@router.get("/interactions", response_model=List[InteractionResponse])
async def list_interactions(
    skip: int = 0,
    limit: int = 100,
    client_id: int = None,
    deal_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Interaction)
    if client_id:
        query = query.where(Interaction.client_id == client_id)
    if deal_id:
        query = query.where(Interaction.deal_id == deal_id)
    result = await db.execute(query.order_by(Interaction.created_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/interactions", response_model=InteractionResponse, status_code=status.HTTP_201_CREATED)
async def create_interaction(
    interaction_in: InteractionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    interaction = Interaction(**interaction_in.model_dump())
    db.add(interaction)
    await db.commit()
    await db.refresh(interaction)
    return interaction
