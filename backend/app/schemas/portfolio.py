from pydantic import BaseModel, UUID4, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ==================== PORTFOLIO SCHEMAS ====================

class PortfolioCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    initial_balance: Decimal = Field(..., gt=0, description="Initial virtual cash (e.g., 1000000 for ₹10L)")


class PortfolioResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    name: str
    initial_balance: Decimal
    current_cash: Decimal
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# ==================== HOLDING SCHEMAS ====================

class HoldingResponse(BaseModel):
    id: UUID4
    portfolio_id: UUID4
    asset_id: UUID4
    quantity: Decimal
    average_buy_price: Decimal
    updated_at: datetime

    class Config:
        from_attributes = True


class HoldingWithDetails(HoldingResponse):
    asset_symbol: str
    asset_name: str
    current_price: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    total_invested: Decimal
    profit_loss: Optional[Decimal] = None
    profit_loss_percentage: Optional[Decimal] = None


# ==================== TRANSACTION SCHEMAS ====================

class TransactionCreate(BaseModel):
    asset_id: UUID4
    transaction_type: str = Field(..., pattern="^(buy|sell)$")
    quantity: Decimal = Field(..., gt=0)
    price_per_unit: Decimal = Field(..., gt=0)
    notes: Optional[str] = None


class TransactionResponse(BaseModel):
    id: UUID4
    portfolio_id: UUID4
    asset_id: UUID4
    transaction_type: str
    quantity: Decimal
    price_per_unit: Decimal
    total_amount: Decimal
    timestamp: datetime
    notes: Optional[str]

    class Config:
        from_attributes = True


class TransactionWithDetails(TransactionResponse):
    asset_symbol: str
    asset_name: str


# ==================== PORTFOLIO SUMMARY SCHEMAS ====================

class PortfolioSummary(BaseModel):
    portfolio_id: UUID4
    portfolio_name: str
    initial_balance: Decimal
    current_cash: Decimal
    total_invested: Decimal
    current_portfolio_value: Decimal
    total_value: Decimal  # cash + holdings value
    total_profit_loss: Decimal
    total_profit_loss_percentage: Decimal
    holdings_count: int


class PortfolioDetailResponse(PortfolioResponse):
    holdings: List[HoldingWithDetails] = []
    summary: Optional[PortfolioSummary] = None
