from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from ..models.accounting import InvoiceStatus, ExpenseCategory, ExpenseStatus, PaymentMethod, BudgetCategory


class InvoiceItemBase(BaseModel):
    description: str
    quantity: float = 1
    unit_price: float


class InvoiceItemCreate(InvoiceItemBase):
    project_phase: Optional[str] = None
    rate_type: Optional[str] = None
    hours: Optional[float] = None


class InvoiceItemResponse(InvoiceItemBase):
    id: int
    invoice_id: int
    amount: float
    project_phase: Optional[str] = None
    rate_type: Optional[str] = None
    hours: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InvoiceBase(BaseModel):
    invoice_number: str
    issue_date: date
    due_date: date


class InvoiceCreate(InvoiceBase):
    client_id: int
    project_id: Optional[int] = None
    billing_name: Optional[str] = None
    billing_address: Optional[str] = None
    billing_email: Optional[str] = None
    tax_rate: float = 0
    discount_percentage: float = 0
    currency: str = "USD"
    notes: Optional[str] = None
    terms: Optional[str] = None
    payment_terms: int = 30
    items: List[InvoiceItemCreate] = []


class InvoiceUpdate(BaseModel):
    status: Optional[InvoiceStatus] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    billing_name: Optional[str] = None
    billing_address: Optional[str] = None
    billing_email: Optional[str] = None
    tax_rate: Optional[float] = None
    discount_percentage: Optional[float] = None
    notes: Optional[str] = None
    terms: Optional[str] = None
    payment_terms: Optional[int] = None


class InvoiceResponse(InvoiceBase):
    id: int
    client_id: int
    project_id: Optional[int] = None
    status: InvoiceStatus
    subtotal: float
    tax_rate: float
    tax_amount: float
    discount_percentage: float
    discount_amount: float
    total_amount: float
    amount_paid: float
    balance_due: float
    currency: str
    notes: Optional[str] = None
    terms: Optional[str] = None
    payment_terms: int
    sent_at: Optional[datetime] = None
    viewed_at: Optional[datetime] = None
    created_at: datetime
    items: List[InvoiceItemResponse] = []

    class Config:
        from_attributes = True


class ExpenseBase(BaseModel):
    category: ExpenseCategory
    description: str
    amount: float
    expense_date: date


class ExpenseCreate(ExpenseBase):
    project_id: Optional[int] = None
    employee_id: Optional[int] = None
    currency: str = "USD"
    vendor_name: Optional[str] = None
    vendor_invoice: Optional[str] = None
    is_reimbursable: bool = False
    receipt_path: Optional[str] = None
    notes: Optional[str] = None
    submitted_by_id: Optional[int] = None


class ExpenseUpdate(BaseModel):
    category: Optional[ExpenseCategory] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    expense_date: Optional[date] = None
    status: Optional[ExpenseStatus] = None
    vendor_name: Optional[str] = None
    vendor_invoice: Optional[str] = None
    is_reimbursable: Optional[bool] = None
    notes: Optional[str] = None
    rejection_reason: Optional[str] = None


class ExpenseResponse(ExpenseBase):
    id: int
    expense_number: str
    project_id: Optional[int] = None
    employee_id: Optional[int] = None
    currency: str
    vendor_name: Optional[str] = None
    status: ExpenseStatus
    is_reimbursable: bool
    approved_by_id: Optional[int] = None
    approved_at: Optional[datetime] = None
    reimbursed_at: Optional[datetime] = None
    submitted_by_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BudgetBase(BaseModel):
    category: BudgetCategory
    name: str
    allocated_amount: float


class BudgetCreate(BudgetBase):
    project_id: int
    description: Optional[str] = None
    currency: str = "USD"
    warning_threshold: int = 80
    critical_threshold: int = 95
    notes: Optional[str] = None


class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    allocated_amount: Optional[float] = None
    spent_amount: Optional[float] = None
    warning_threshold: Optional[int] = None
    critical_threshold: Optional[int] = None
    notes: Optional[str] = None


class BudgetResponse(BudgetBase):
    id: int
    project_id: int
    description: Optional[str] = None
    spent_amount: float
    remaining_amount: float
    currency: str
    warning_threshold: int
    critical_threshold: int
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentRecordBase(BaseModel):
    amount: float
    payment_date: date
    payment_method: PaymentMethod


class PaymentRecordCreate(PaymentRecordBase):
    invoice_id: int
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    received_by_id: Optional[int] = None


class PaymentRecordResponse(PaymentRecordBase):
    id: int
    invoice_id: int
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    received_by_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
