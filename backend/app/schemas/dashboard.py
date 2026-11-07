from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


# ==================== DASHBOARD SCHEMAS ====================

class DashboardPortfolioSummary(BaseModel):
    portfolio_id: UUID4
    portfolio_name: str
    initial_balance: Decimal
    current_cash: Decimal
    total_value: Decimal
    total_profit_loss: Decimal
    profit_loss_percentage: Decimal
    holdings_count: int


class RecentTransactionSummary(BaseModel):
    id: UUID4
    portfolio_name: str
    asset_symbol: str
    asset_name: str
    transaction_type: str
    quantity: Decimal
    price_per_unit: Decimal
    total_amount: Decimal
    timestamp: datetime


class RecentLearningActivity(BaseModel):
    lesson_id: UUID4
    lesson_title: str
    course_title: str
    completed_at: datetime


class DashboardStats(BaseModel):
    total_portfolios: int
    total_cash_available: Decimal
    total_invested: Decimal
    total_portfolio_value: Decimal
    overall_profit_loss: Decimal
    overall_profit_loss_percentage: Decimal

    total_lessons: int
    completed_lessons: int
    learning_completion_percentage: Decimal

    total_transactions: int
    last_transaction_date: Optional[datetime]


class DashboardResponse(BaseModel):
    stats: DashboardStats
    portfolios: List[DashboardPortfolioSummary]
    recent_transactions: List[RecentTransactionSummary]
    recent_learning: List[RecentLearningActivity]
