from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime
from decimal import Decimal


# ==================== ASSET TYPE SCHEMAS ====================

class AssetTypeResponse(BaseModel):
    id: UUID4
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


# ==================== ASSET SCHEMAS ====================

class AssetBase(BaseModel):
    symbol: str
    name: str
    description: Optional[str]
    sector: Optional[str]
    market: Optional[str]


class AssetListResponse(AssetBase):
    id: UUID4
    asset_type_id: UUID4
    is_active: bool
    is_demo_data: bool

    class Config:
        from_attributes = True


class AssetDetailResponse(AssetListResponse):
    data_source: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== ASSET PRICE SCHEMAS ====================

class AssetPriceResponse(BaseModel):
    id: UUID4
    asset_id: UUID4
    price: Decimal
    volume: Optional[Decimal]
    market_cap: Optional[Decimal]
    timestamp: datetime
    data_source: Optional[str]
    is_demo_data: bool

    class Config:
        from_attributes = True


class AssetWithLatestPrice(AssetListResponse):
    latest_price: Optional[Decimal] = None
    price_timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
