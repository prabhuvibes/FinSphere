from pydantic import BaseModel, UUID4, EmailStr, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


# ==================== USER PROFILE SCHEMAS ====================

class UserProfileResponse(BaseModel):
    id: UUID4
    email: EmailStr
    full_name: str
    knowledge_level: Optional[str]
    created_at: datetime
    last_login: Optional[datetime]
    is_active: bool

    # Additional stats
    total_portfolios: int
    total_lessons_completed: int
    total_transactions: int
    member_since_days: int

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    knowledge_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")


class UserStatsResponse(BaseModel):
    # Learning stats
    total_courses_available: int
    total_lessons_available: int
    lessons_completed: int
    learning_completion_percentage: Decimal

    # Portfolio stats
    total_portfolios: int
    active_portfolios: int
    total_initial_investment: Decimal
    current_total_value: Decimal
    overall_profit_loss: Decimal
    overall_profit_loss_percentage: Decimal

    # Trading stats
    total_transactions: int
    total_buy_transactions: int
    total_sell_transactions: int
    total_holdings: int

    # Account stats
    account_age_days: int
    last_transaction_date: Optional[datetime]
    last_learning_activity: Optional[datetime]
