from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base


class AssetType(Base):
    __tablename__ = "asset_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    assets = relationship("Asset", back_populates="asset_type")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    asset_type_id = Column(UUID(as_uuid=True), ForeignKey("asset_types.id"), nullable=False)
    description = Column(Text)
    sector = Column(String(100))
    market = Column(String(50))
    is_active = Column(Boolean, default=True)
    data_source = Column(String(100))
    is_demo_data = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    asset_type = relationship("AssetType", back_populates="assets")
    prices = relationship("AssetPrice", back_populates="asset")


class AssetPrice(Base):
    __tablename__ = "asset_prices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    price = Column(Numeric(20, 4), nullable=False)
    volume = Column(Numeric(20, 0))
    market_cap = Column(Numeric(20, 2))
    timestamp = Column(DateTime, nullable=False)
    data_source = Column(String(100))
    is_demo_data = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    asset = relationship("Asset", back_populates="prices")
