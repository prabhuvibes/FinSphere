from sqlalchemy import Column, String, Boolean, DateTime, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    initial_balance = Column(Numeric(20, 2), nullable=False)
    current_cash = Column(Numeric(20, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        CheckConstraint('initial_balance > 0', name='initial_balance_positive'),
        CheckConstraint('current_cash >= 0', name='current_cash_non_negative'),
    )

    # Relationships
    holdings = relationship("Holding", back_populates="portfolio")
    transactions = relationship("Transaction", back_populates="portfolio")


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolios.id"), nullable=False)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    quantity = Column(Numeric(20, 8), nullable=False)
    average_buy_price = Column(Numeric(20, 4), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('quantity > 0', name='quantity_positive'),
        CheckConstraint('average_buy_price > 0', name='average_buy_price_positive'),
    )

    # Relationships
    portfolio = relationship("Portfolio", back_populates="holdings")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolios.id"), nullable=False)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    transaction_type = Column(String(10), nullable=False)  # 'buy' or 'sell'
    quantity = Column(Numeric(20, 8), nullable=False)
    price_per_unit = Column(Numeric(20, 4), nullable=False)
    total_amount = Column(Numeric(20, 2), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    notes = Column(String)

    __table_args__ = (
        CheckConstraint("transaction_type IN ('buy', 'sell')", name='valid_transaction_type'),
        CheckConstraint('quantity > 0', name='quantity_positive'),
        CheckConstraint('price_per_unit > 0', name='price_positive'),
        CheckConstraint('total_amount > 0', name='total_amount_positive'),
    )

    # Relationships
    portfolio = relationship("Portfolio", back_populates="transactions")
