from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from decimal import Decimal
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.portfolio import Portfolio, Holding, Transaction
from app.models.learning import Course, Lesson, LearningProgress
from app.models.asset import Asset, AssetPrice
from app.core.security import verify_token
from app.schemas.dashboard import (
    DashboardResponse,
    DashboardStats,
    DashboardPortfolioSummary,
    RecentTransactionSummary,
    RecentLearningActivity
)

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])
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


@router.get("/summary", response_model=DashboardResponse)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get complete dashboard summary for user:
    - Portfolio overview with P&L
    - Learning progress
    - Recent transactions
    - Recent learning activity
    - Overall statistics
    """

    # ==================== PORTFOLIO DATA ====================

    portfolios = db.query(Portfolio).filter(
        Portfolio.user_id == current_user.id,
        Portfolio.is_active == True
    ).all()

    portfolio_summaries = []
    total_cash = Decimal('0')
    total_portfolio_value = Decimal('0')
    total_initial_balance = Decimal('0')

    for portfolio in portfolios:
        # Get holdings for this portfolio
        holdings = db.query(Holding).filter(Holding.portfolio_id == portfolio.id).all()

        holdings_value = Decimal('0')
        for holding in holdings:
            current_price = get_latest_asset_price(holding.asset_id, db)
            if current_price:
                holdings_value += holding.quantity * current_price

        portfolio_total = portfolio.current_cash + holdings_value
        profit_loss = portfolio_total - portfolio.initial_balance
        profit_loss_pct = (profit_loss / portfolio.initial_balance * 100) if portfolio.initial_balance > 0 else Decimal('0')

        portfolio_summaries.append({
            "portfolio_id": portfolio.id,
            "portfolio_name": portfolio.name,
            "initial_balance": portfolio.initial_balance,
            "current_cash": portfolio.current_cash,
            "total_value": portfolio_total,
            "total_profit_loss": profit_loss,
            "profit_loss_percentage": profit_loss_pct,
            "holdings_count": len(holdings)
        })

        total_cash += portfolio.current_cash
        total_portfolio_value += portfolio_total
        total_initial_balance += portfolio.initial_balance

    # ==================== LEARNING DATA ====================

    total_lessons = db.query(func.count(Lesson.id)).filter(
        Lesson.is_published == True
    ).scalar() or 0

    completed_lessons = db.query(func.count(LearningProgress.id)).filter(
        LearningProgress.user_id == current_user.id
    ).scalar() or 0

    learning_completion = (completed_lessons / total_lessons * 100) if total_lessons > 0 else Decimal('0')

    # Recent learning activity
    recent_learning_records = db.query(LearningProgress).filter(
        LearningProgress.user_id == current_user.id
    ).order_by(desc(LearningProgress.completed_at)).limit(5).all()

    recent_learning = []
    for progress in recent_learning_records:
        lesson = db.query(Lesson).filter(Lesson.id == progress.lesson_id).first()
        if lesson:
            course = db.query(Course).filter(Course.id == lesson.course_id).first()
            recent_learning.append({
                "lesson_id": lesson.id,
                "lesson_title": lesson.title,
                "course_title": course.title if course else "N/A",
                "completed_at": progress.completed_at
            })

    # ==================== TRANSACTION DATA ====================

    total_transactions = db.query(func.count(Transaction.id)).join(
        Portfolio, Transaction.portfolio_id == Portfolio.id
    ).filter(Portfolio.user_id == current_user.id).scalar() or 0

    last_transaction = db.query(Transaction).join(
        Portfolio, Transaction.portfolio_id == Portfolio.id
    ).filter(Portfolio.user_id == current_user.id).order_by(
        desc(Transaction.timestamp)
    ).first()

    last_transaction_date = last_transaction.timestamp if last_transaction else None

    # Recent transactions
    recent_txn_records = db.query(Transaction).join(
        Portfolio, Transaction.portfolio_id == Portfolio.id
    ).filter(Portfolio.user_id == current_user.id).order_by(
        desc(Transaction.timestamp)
    ).limit(10).all()

    recent_transactions = []
    for txn in recent_txn_records:
        portfolio = db.query(Portfolio).filter(Portfolio.id == txn.portfolio_id).first()
        asset = db.query(Asset).filter(Asset.id == txn.asset_id).first()

        recent_transactions.append({
            "id": txn.id,
            "portfolio_name": portfolio.name if portfolio else "N/A",
            "asset_symbol": asset.symbol if asset else "N/A",
            "asset_name": asset.name if asset else "N/A",
            "transaction_type": txn.transaction_type,
            "quantity": txn.quantity,
            "price_per_unit": txn.price_per_unit,
            "total_amount": txn.total_amount,
            "timestamp": txn.timestamp
        })

    # ==================== OVERALL STATS ====================

    total_invested = total_initial_balance - total_cash
    overall_profit_loss = total_portfolio_value - total_initial_balance
    overall_profit_loss_pct = (overall_profit_loss / total_initial_balance * 100) if total_initial_balance > 0 else Decimal('0')

    stats = {
        "total_portfolios": len(portfolios),
        "total_cash_available": total_cash,
        "total_invested": total_invested,
        "total_portfolio_value": total_portfolio_value,
        "overall_profit_loss": overall_profit_loss,
        "overall_profit_loss_percentage": overall_profit_loss_pct,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "learning_completion_percentage": round(learning_completion, 2),
        "total_transactions": total_transactions,
        "last_transaction_date": last_transaction_date
    }

    # ==================== BUILD RESPONSE ====================

    return {
        "stats": stats,
        "portfolios": portfolio_summaries,
        "recent_transactions": recent_transactions,
        "recent_learning": recent_learning
    }
