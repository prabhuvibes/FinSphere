from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from app.database import get_db
from app.models.portfolio import Portfolio, Holding, Transaction
from app.models.asset import Asset, AssetPrice
from app.models.user import User
from app.core.security import verify_token
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse,
    PortfolioDetailResponse,
    HoldingWithDetails,
    TransactionCreate,
    TransactionResponse,
    TransactionWithDetails,
    PortfolioSummary
)

router = APIRouter(prefix="/api/portfolio", tags=["Portfolio & Trading"])
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


def get_latest_asset_price(asset_id, db: Session) -> Optional[Decimal]:
    """Get latest price for an asset"""
    latest_price = db.query(AssetPrice).filter(
        AssetPrice.asset_id == asset_id
    ).order_by(desc(AssetPrice.timestamp)).first()

    return latest_price.price if latest_price else None


# ==================== PORTFOLIO ENDPOINTS ====================

@router.post("/create", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    portfolio_data: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new portfolio with virtual cash"""

    new_portfolio = Portfolio(
        user_id=current_user.id,
        name=portfolio_data.name,
        initial_balance=portfolio_data.initial_balance,
        current_cash=portfolio_data.initial_balance
    )

    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)

    return new_portfolio


@router.get("/list", response_model=List[PortfolioResponse])
def get_user_portfolios(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all portfolios for current user"""
    portfolios = db.query(Portfolio).filter(
        Portfolio.user_id == current_user.id,
        Portfolio.is_active == True
    ).order_by(desc(Portfolio.created_at)).all()

    return portfolios


@router.get("/{portfolio_id}", response_model=PortfolioDetailResponse)
def get_portfolio_details(
    portfolio_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed portfolio information with holdings and P&L"""

    # Get portfolio
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id,
        Portfolio.is_active == True
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    # Get holdings with asset details
    holdings = db.query(Holding).filter(
        Holding.portfolio_id == portfolio_id
    ).all()

    holdings_with_details = []
    total_invested = Decimal('0')
    current_portfolio_value = Decimal('0')

    for holding in holdings:
        asset = db.query(Asset).filter(Asset.id == holding.asset_id).first()
        current_price = get_latest_asset_price(holding.asset_id, db)

        total_cost = holding.quantity * holding.average_buy_price
        current_value = holding.quantity * current_price if current_price else None
        profit_loss = (current_value - total_cost) if current_value else None
        profit_loss_pct = (profit_loss / total_cost * 100) if profit_loss and total_cost > 0 else None

        holdings_with_details.append({
            "id": holding.id,
            "portfolio_id": holding.portfolio_id,
            "asset_id": holding.asset_id,
            "quantity": holding.quantity,
            "average_buy_price": holding.average_buy_price,
            "updated_at": holding.updated_at,
            "asset_symbol": asset.symbol if asset else "N/A",
            "asset_name": asset.name if asset else "N/A",
            "current_price": current_price,
            "current_value": current_value,
            "total_invested": total_cost,
            "profit_loss": profit_loss,
            "profit_loss_percentage": profit_loss_pct
        })

        total_invested += total_cost
        if current_value:
            current_portfolio_value += current_value

    # Calculate summary
    total_value = portfolio.current_cash + current_portfolio_value
    total_profit_loss = total_value - portfolio.initial_balance
    total_profit_loss_pct = (total_profit_loss / portfolio.initial_balance * 100) if portfolio.initial_balance > 0 else Decimal('0')

    summary = {
        "portfolio_id": portfolio.id,
        "portfolio_name": portfolio.name,
        "initial_balance": portfolio.initial_balance,
        "current_cash": portfolio.current_cash,
        "total_invested": total_invested,
        "current_portfolio_value": current_portfolio_value,
        "total_value": total_value,
        "total_profit_loss": total_profit_loss,
        "total_profit_loss_percentage": total_profit_loss_pct,
        "holdings_count": len(holdings)
    }

    return {
        **portfolio.__dict__,
        "holdings": holdings_with_details,
        "summary": summary
    }


# ==================== TRADING ENDPOINTS ====================

@router.post("/{portfolio_id}/buy", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def buy_asset(
    portfolio_id: str,
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buy an asset (add to holdings, deduct cash)"""

    # Verify portfolio ownership
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id,
        Portfolio.is_active == True
    ).first()

    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    # Verify asset exists
    asset = db.query(Asset).filter(Asset.id == transaction.asset_id, Asset.is_active == True).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")

    # Calculate total cost
    total_cost = transaction.quantity * transaction.price_per_unit

    # Check if user has enough cash
    if portfolio.current_cash < total_cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient funds. Available: ₹{portfolio.current_cash}, Required: ₹{total_cost}"
        )

    # Create transaction record
    new_transaction = Transaction(
        portfolio_id=portfolio_id,
        asset_id=transaction.asset_id,
        transaction_type='buy',
        quantity=transaction.quantity,
        price_per_unit=transaction.price_per_unit,
        total_amount=total_cost,
        notes=transaction.notes
    )

    # Update or create holding
    existing_holding = db.query(Holding).filter(
        Holding.portfolio_id == portfolio_id,
        Holding.asset_id == transaction.asset_id
    ).first()

    if existing_holding:
        # Update average buy price and quantity
        total_quantity = existing_holding.quantity + transaction.quantity
        total_value = (existing_holding.quantity * existing_holding.average_buy_price) + total_cost
        new_avg_price = total_value / total_quantity

        existing_holding.quantity = total_quantity
        existing_holding.average_buy_price = new_avg_price
        existing_holding.updated_at = datetime.utcnow()
    else:
        # Create new holding
        new_holding = Holding(
            portfolio_id=portfolio_id,
            asset_id=transaction.asset_id,
            quantity=transaction.quantity,
            average_buy_price=transaction.price_per_unit
        )
        db.add(new_holding)

    # Deduct cash from portfolio
    portfolio.current_cash -= total_cost
    portfolio.updated_at = datetime.utcnow()

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


@router.post("/{portfolio_id}/sell", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def sell_asset(
    portfolio_id: str,
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Sell an asset (reduce holdings, add cash)"""

    # Verify portfolio ownership
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id,
        Portfolio.is_active == True
    ).first()

    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    # Check if holding exists
    holding = db.query(Holding).filter(
        Holding.portfolio_id == portfolio_id,
        Holding.asset_id == transaction.asset_id
    ).first()

    if not holding:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't own this asset"
        )

    # Check if user has enough quantity
    if holding.quantity < transaction.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient quantity. You own: {holding.quantity}, Trying to sell: {transaction.quantity}"
        )

    # Calculate total proceeds
    total_proceeds = transaction.quantity * transaction.price_per_unit

    # Create transaction record
    new_transaction = Transaction(
        portfolio_id=portfolio_id,
        asset_id=transaction.asset_id,
        transaction_type='sell',
        quantity=transaction.quantity,
        price_per_unit=transaction.price_per_unit,
        total_amount=total_proceeds,
        notes=transaction.notes
    )

    # Update holding
    holding.quantity -= transaction.quantity
    holding.updated_at = datetime.utcnow()

    # If quantity becomes 0, delete holding
    if holding.quantity == 0:
        db.delete(holding)

    # Add cash to portfolio
    portfolio.current_cash += total_proceeds
    portfolio.updated_at = datetime.utcnow()

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


@router.get("/{portfolio_id}/transactions", response_model=List[TransactionWithDetails])
def get_transaction_history(
    portfolio_id: str,
    limit: int = Query(50, le=200),
    offset: int = 0,
    transaction_type: Optional[str] = Query(None, pattern="^(buy|sell)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get transaction history for a portfolio"""

    # Verify portfolio ownership
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    # Build query
    query = db.query(Transaction).filter(Transaction.portfolio_id == portfolio_id)

    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)

    transactions = query.order_by(desc(Transaction.timestamp)).offset(offset).limit(limit).all()

    # Add asset details
    result = []
    for txn in transactions:
        asset = db.query(Asset).filter(Asset.id == txn.asset_id).first()
        result.append({
            **txn.__dict__,
            "asset_symbol": asset.symbol if asset else "N/A",
            "asset_name": asset.name if asset else "N/A"
        })

    return result


@router.get("/{portfolio_id}/holdings", response_model=List[HoldingWithDetails])
def get_portfolio_holdings(
    portfolio_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all holdings for a portfolio"""

    # Verify portfolio ownership
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    holdings = db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()

    result = []
    for holding in holdings:
        asset = db.query(Asset).filter(Asset.id == holding.asset_id).first()
        current_price = get_latest_asset_price(holding.asset_id, db)

        total_cost = holding.quantity * holding.average_buy_price
        current_value = holding.quantity * current_price if current_price else None
        profit_loss = (current_value - total_cost) if current_value else None
        profit_loss_pct = (profit_loss / total_cost * 100) if profit_loss and total_cost > 0 else None

        result.append({
            "id": holding.id,
            "portfolio_id": holding.portfolio_id,
            "asset_id": holding.asset_id,
            "quantity": holding.quantity,
            "average_buy_price": holding.average_buy_price,
            "updated_at": holding.updated_at,
            "asset_symbol": asset.symbol if asset else "N/A",
            "asset_name": asset.name if asset else "N/A",
            "current_price": current_price,
            "current_value": current_value,
            "total_invested": total_cost,
            "profit_loss": profit_loss,
            "profit_loss_percentage": profit_loss_pct
        })

    return result
