from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime
import uuid

from ...core import get_db
from ...models.user import User
from ...models.accounting import Invoice, InvoiceItem, Expense, Budget, PaymentRecord, InvoiceStatus, ExpenseStatus
from ...schemas.accounting import (
    InvoiceCreate, InvoiceUpdate, InvoiceResponse,
    ExpenseCreate, ExpenseUpdate, ExpenseResponse,
    BudgetCreate, BudgetUpdate, BudgetResponse,
    PaymentRecordCreate, PaymentRecordResponse
)
from .auth import get_current_active_user

router = APIRouter()


# Invoices
@router.get("/invoices", response_model=List[InvoiceResponse])
async def list_invoices(
    skip: int = 0,
    limit: int = 100,
    status: InvoiceStatus = None,
    client_id: int = None,
    project_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Invoice)
    if status:
        query = query.where(Invoice.status == status)
    if client_id:
        query = query.where(Invoice.client_id == client_id)
    if project_id:
        query = query.where(Invoice.project_id == project_id)
    result = await db.execute(query.order_by(Invoice.created_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/invoices", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice_in: InvoiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    invoice_data = invoice_in.model_dump(exclude={"items"})
    
    # Calculate totals
    subtotal = sum(item.quantity * item.unit_price for item in invoice_in.items)
    discount_amount = subtotal * invoice_data.get("discount_percentage", 0) / 100
    tax_amount = (subtotal - discount_amount) * invoice_data.get("tax_rate", 0) / 100
    total_amount = subtotal - discount_amount + tax_amount
    
    invoice = Invoice(
        **invoice_data,
        subtotal=subtotal,
        discount_amount=discount_amount,
        tax_amount=tax_amount,
        total_amount=total_amount,
        balance_due=total_amount,
        created_by_id=current_user.id
    )
    
    db.add(invoice)
    await db.flush()
    
    # Add items
    for item_data in invoice_in.items:
        item = InvoiceItem(
            invoice_id=invoice.id,
            description=item_data.description,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            amount=item_data.quantity * item_data.unit_price,
            project_phase=item_data.project_phase,
            rate_type=item_data.rate_type,
            hours=item_data.hours
        )
        db.add(item)
    
    await db.commit()
    await db.refresh(invoice)
    return invoice


@router.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.put("/invoices/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: int,
    invoice_in: InvoiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    update_data = invoice_in.model_dump(exclude_unset=True)
    
    # Track if sent
    if update_data.get("status") == InvoiceStatus.SENT and not invoice.sent_at:
        invoice.sent_at = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(invoice, field, value)
    
    await db.commit()
    await db.refresh(invoice)
    return invoice


# Payments
@router.post("/invoices/{invoice_id}/payments", response_model=PaymentRecordResponse, status_code=status.HTTP_201_CREATED)
async def record_payment(
    invoice_id: int,
    payment_in: PaymentRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    payment = PaymentRecord(
        **payment_in.model_dump(),
        received_by_id=current_user.id
    )
    db.add(payment)
    
    # Update invoice
    invoice.amount_paid += payment_in.amount
    invoice.balance_due = invoice.total_amount - invoice.amount_paid
    
    if invoice.balance_due <= 0:
        invoice.status = InvoiceStatus.PAID
    elif invoice.amount_paid > 0:
        invoice.status = InvoiceStatus.PARTIAL
    
    await db.commit()
    await db.refresh(payment)
    return payment


@router.get("/invoices/{invoice_id}/payments", response_model=List[PaymentRecordResponse])
async def list_invoice_payments(
    invoice_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(PaymentRecord).where(PaymentRecord.invoice_id == invoice_id)
    )
    return result.scalars().all()


# Expenses
@router.get("/expenses", response_model=List[ExpenseResponse])
async def list_expenses(
    skip: int = 0,
    limit: int = 100,
    status: ExpenseStatus = None,
    project_id: int = None,
    employee_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Expense)
    if status:
        query = query.where(Expense.status == status)
    if project_id:
        query = query.where(Expense.project_id == project_id)
    if employee_id:
        query = query.where(Expense.employee_id == employee_id)
    result = await db.execute(query.order_by(Expense.created_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_in: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Generate expense number
    expense_number = f"EXP-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    
    expense = Expense(
        **expense_in.model_dump(),
        expense_number=expense_number
    )
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense


@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Expense).where(Expense.id == expense_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    expense_in: ExpenseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Expense).where(Expense.id == expense_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    update_data = expense_in.model_dump(exclude_unset=True)
    
    # Track approval
    if update_data.get("status") == ExpenseStatus.APPROVED:
        expense.approved_by_id = current_user.id
        expense.approved_at = datetime.utcnow()
    elif update_data.get("status") == ExpenseStatus.REIMBURSED:
        expense.reimbursed_at = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(expense, field, value)
    
    await db.commit()
    await db.refresh(expense)
    return expense


# Budgets
@router.get("/budgets", response_model=List[BudgetResponse])
async def list_budgets(
    skip: int = 0,
    limit: int = 100,
    project_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Budget)
    if project_id:
        query = query.where(Budget.project_id == project_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/budgets", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_in: BudgetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    budget = Budget(
        **budget_in.model_dump(),
        remaining_amount=budget_in.allocated_amount
    )
    db.add(budget)
    await db.commit()
    await db.refresh(budget)
    return budget


@router.put("/budgets/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: int,
    budget_in: BudgetUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Budget).where(Budget.id == budget_id))
    budget = result.scalar_one_or_none()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    update_data = budget_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(budget, field, value)
    
    # Recalculate remaining
    budget.remaining_amount = budget.allocated_amount - budget.spent_amount
    
    await db.commit()
    await db.refresh(budget)
    return budget
