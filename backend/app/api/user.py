from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timezone
from decimal import Decimal

from app.database import get_db
from app.models.user import User
from app.models.portfolio import Portfolio, Holding, Transaction
from app.models.learning import Course, Lesson, LearningProgress
from app.models.asset import AssetPrice
from app.core.security import verify_token
from app.schemas.user_profile import (
    UserProfileResponse,
    UserProfileUpdate,
    UserStatsResponse
)

router = APIRouter(prefix="/api/user", tags=["User Profile"])
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    token = credentials.credentials
    email = verify_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_latest_asset_price(asset_id, db: Session):
    """Get latest price for an asset"""
    latest_price = db.query(AssetPrice).filter(
        AssetPrice.asset_id == asset_id
    ).order_by(desc(AssetPrice.timestamp)).first()
    return latest_price.price if latest_price else None


def get_utc_now():
    """Get timezone-aware UTC datetime"""
    return datetime.now(timezone.utc)


def safe_datetime_diff_days(end_dt, start_dt):
    """Safely calculate days difference between datetimes"""
    # Make both timezone-aware if needed
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=timezone.utc)
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=timezone.utc)
    return (end_dt - start_dt).days


@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user profile with basic statistics"""

    # Calculate member since days
    member_since = safe_datetime_diff_days(datetime.utcnow(), current_user.created_at)

    # Get counts
    total_portfolios = db.query(func.count(Portfolio.id)).filter(
        Portfolio.user_id == current_user.id
    ).scalar() or 0

    total_lessons_completed = db.query(func.count(LearningProgress.id)).filter(
        LearningProgress.user_id == current_user.id
    ).scalar() or 0

    total_transactions = db.query(func.count(Transaction.id)).join(
        Portfolio, Transaction.portfolio_id == Portfolio.id
    ).filter(Portfolio.user_id == current_user.id).scalar() or 0

    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "knowledge_level": current_user.knowledge_level,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login,
        "is_active": current_user.is_active,
        "total_portfolios": total_portfolios,
        "total_lessons_completed": total_lessons_completed,
        "total_transactions": total_transactions,
        "member_since_days": member_since
    }


@router.put("/profile", response_model=UserProfileResponse)
def update_user_profile(
    profile_update: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile information"""

    if profile_update.full_name is not None:
        current_user.full_name = profile_update.full_name

    if profile_update.knowledge_level is not None:
        current_user.knowledge_level = profile_update.knowledge_level

    current_user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(current_user)

    # Return updated profile with stats
    return get_user_profile(db, current_user)


@router.get("/stats", response_model=UserStatsResponse)
def get_user_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed user statistics"""

    # Learning stats
    total_courses = db.query(func.count(Course.id)).filter(
        Course.is_published == True
    ).scalar() or 0

    total_lessons = db.query(func.count(Lesson.id)).filter(
        Lesson.is_published == True
    ).scalar() or 0

    completed_lessons = db.query(func.count(LearningProgress.id)).filter(
        LearningProgress.user_id == current_user.id
    ).scalar() or 0

    learning_completion = (completed_lessons / total_lessons * 100) if total_lessons > 0 else Decimal('0')

    # Portfolio stats
    portfolios = db.query(Portfolio).filter(
        Portfolio.user_id == current_user.id
    ).all()

    total_portfolios = len(portfolios)
    active_portfolios = sum(1 for p in portfolios if p.is_active)

    total_initial = Decimal('0')
    total_current = Decimal('0')

    for portfolio in portfolios:
        total_initial += portfolio.initial_balance

        # Calculate current value
        holdings = db.query(Holding).filter(Holding.portfolio_id == portfolio.id).all()
        holdings_value = Decimal('0')

        for holding in holdings:
            current_price = get_latest_asset_price(holding.asset_id, db)
            if current_price:
                holdings_value += holding.quantity * current_price

        total_current += portfolio.current_cash + holdings_value

    overall_profit_loss = total_current - total_initial
    overall_pl_pct = (overall_profit_loss / total_initial * 100) if total_initial > 0 else Decimal('0')

    # Trading stats
    total_transactions = db.query(func.count(Transaction.id)).join(
        Portfolio, Transaction.portfolio_id == Portfolio.id
    ).filter(Portfolio.user_id == current_user.id).scalar() or 0

    total_buy = db.query(func.count(Transaction.id)).join(
        Portfolio, Transaction.portfolio_id == Portfolio.id
    ).filter(
        Portfolio.user_id == current_user.id,
        Transaction.transaction_type == 'buy'
    ).scalar() or 0

    total_sell = db.query(func.count(Transaction.id)).join(
        Portfolio, Transaction.portfolio_id == Portfolio.id
    ).filter(
        Portfolio.user_id == current_user.id,
        Transaction.transaction_type == 'sell'
    ).scalar() or 0

    total_holdings = db.query(func.count(Holding.id)).join(
        Portfolio, Holding.portfolio_id == Portfolio.id
    ).filter(Portfolio.user_id == current_user.id).scalar() or 0

    # Last activity dates
    last_transaction = db.query(Transaction).join(
        Portfolio, Transaction.portfolio_id == Portfolio.id
    ).filter(Portfolio.user_id == current_user.id).order_by(
        desc(Transaction.timestamp)
    ).first()

    last_learning = db.query(LearningProgress).filter(
        LearningProgress.user_id == current_user.id
    ).order_by(desc(LearningProgress.completed_at)).first()

    # Account age
    account_age = safe_datetime_diff_days(datetime.utcnow(), current_user.created_at)

    return {
        "total_courses_available": total_courses,
        "total_lessons_available": total_lessons,
        "lessons_completed": completed_lessons,
        "learning_completion_percentage": round(learning_completion, 2),
        "total_portfolios": total_portfolios,
        "active_portfolios": active_portfolios,
        "total_initial_investment": total_initial,
        "current_total_value": total_current,
        "overall_profit_loss": overall_profit_loss,
        "overall_profit_loss_percentage": round(overall_pl_pct, 2),
        "total_transactions": total_transactions,
        "total_buy_transactions": total_buy,
        "total_sell_transactions": total_sell,
        "total_holdings": total_holdings,
        "account_age_days": account_age,
        "last_transaction_date": last_transaction.timestamp if last_transaction else None,
        "last_learning_activity": last_learning.completed_at if last_learning else None
    }
