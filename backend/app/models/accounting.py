from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, Numeric, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class InvoiceStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PARTIAL = "partial"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class ExpenseCategory(str, enum.Enum):
    EQUIPMENT_RENTAL = "equipment_rental"
    TALENT = "talent"
    CREW = "crew"
    LOCATION = "location"
    CATERING = "catering"
    TRANSPORTATION = "transportation"
    ACCOMMODATION = "accommodation"
    POST_PRODUCTION = "post_production"
    MUSIC_LICENSING = "music_licensing"
    PROPS = "props"
    WARDROBE = "wardrobe"
    INSURANCE = "insurance"
    PERMITS = "permits"
    SOFTWARE = "software"
    MARKETING = "marketing"
    OFFICE = "office"
    UTILITIES = "utilities"
    OTHER = "other"


class ExpenseStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REIMBURSED = "reimbursed"


class PaymentMethod(str, enum.Enum):
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    CHECK = "check"
    CASH = "cash"
    PAYPAL = "paypal"
    OTHER = "other"


class BudgetCategory(str, enum.Enum):
    PRE_PRODUCTION = "pre_production"
    PRODUCTION = "production"
    POST_PRODUCTION = "post_production"
    TALENT = "talent"
    CREW = "crew"
    EQUIPMENT = "equipment"
    LOCATION = "location"
    TRAVEL = "travel"
    CONTINGENCY = "contingency"
    OTHER = "other"


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    
    # Client Info
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    # Billing Address (snapshot at invoice creation)
    billing_name = Column(String(255), nullable=True)
    billing_address = Column(Text, nullable=True)
    billing_email = Column(String(255), nullable=True)
    
    # Dates
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    
    # Status
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    
    # Amounts
    subtotal = Column(Numeric(15, 2), default=0)
    tax_rate = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(15, 2), default=0)
    discount_percentage = Column(Numeric(5, 2), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    total_amount = Column(Numeric(15, 2), default=0)
    amount_paid = Column(Numeric(15, 2), default=0)
    balance_due = Column(Numeric(15, 2), default=0)
    
    # Currency
    currency = Column(String(3), default="USD")
    
    # Notes
    notes = Column(Text, nullable=True)
    terms = Column(Text, nullable=True)
    
    # Payment Info
    payment_terms = Column(Integer, default=30)
    
    # Sent/Viewed tracking
    sent_at = Column(DateTime(timezone=True), nullable=True)
    viewed_at = Column(DateTime(timezone=True), nullable=True)
    
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    client = relationship("Client", back_populates="invoices")
    project = relationship("Project", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice")
    payments = relationship("PaymentRecord", back_populates="invoice")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    
    description = Column(String(500), nullable=False)
    quantity = Column(Numeric(10, 2), default=1)
    unit_price = Column(Numeric(15, 2), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    
    # Optional: Link to specific project phase
    project_phase = Column(String(100), nullable=True)
    
    # For hourly billing
    rate_type = Column(String(20), nullable=True)  # hourly, daily, fixed
    hours = Column(Numeric(8, 2), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    invoice = relationship("Invoice", back_populates="items")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    
    expense_number = Column(String(50), unique=True, nullable=False)
    category = Column(Enum(ExpenseCategory), nullable=False)
    description = Column(Text, nullable=False)
    
    # Amount
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), default="USD")
    
    # Date
    expense_date = Column(Date, nullable=False)
    
    # Vendor
    vendor_name = Column(String(255), nullable=True)
    vendor_invoice = Column(String(100), nullable=True)
    
    # Status
    status = Column(Enum(ExpenseStatus), default=ExpenseStatus.PENDING)
    
    # Approval
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Reimbursement
    is_reimbursable = Column(Boolean, default=False)
    reimbursed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Receipt
    receipt_path = Column(String(500), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    submitted_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="expenses")


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    category = Column(Enum(BudgetCategory), nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Amounts
    allocated_amount = Column(Numeric(15, 2), default=0)
    spent_amount = Column(Numeric(15, 2), default=0)
    remaining_amount = Column(Numeric(15, 2), default=0)
    
    # Currency
    currency = Column(String(3), default="USD")
    
    # Alert thresholds
    warning_threshold = Column(Integer, default=80)  # Percentage
    critical_threshold = Column(Integer, default=95)
    
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PaymentRecord(Base):
    __tablename__ = "payment_records"

    id = Column(Integer, primary_key=True, index=True)
    
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    
    amount = Column(Numeric(15, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    
    reference_number = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    received_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
