from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_
from typing import List, Optional
from app.database import get_db
from app.models.asset import Asset, AssetType, AssetPrice
from app.schemas.asset import (
    AssetTypeResponse,
    AssetListResponse,
    AssetDetailResponse,
    AssetWithLatestPrice,
    AssetPriceResponse
)

router = APIRouter(prefix="/api/assets", tags=["Assets"])


# ==================== ASSET TYPE ENDPOINTS ====================

@router.get("/types", response_model=List[AssetTypeResponse])
def get_asset_types(db: Session = Depends(get_db)):
    """Get all asset types (stocks, ETFs, mutual funds, etc.)"""
    asset_types = db.query(AssetType).all()
    return asset_types


# ==================== ASSET ENDPOINTS ====================

@router.get("/stocks", response_model=List[AssetWithLatestPrice])
def get_stocks(
    sector: Optional[str] = None,
    market: Optional[str] = None,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Browse stocks with optional filters
    - sector: Filter by sector (e.g., 'Information Technology', 'Banking')
    - market: Filter by market (e.g., 'NSE', 'BSE')
    - limit: Max results (default 50, max 100)
    - offset: Pagination offset
    """
    # Get stock asset type
    stock_type = db.query(AssetType).filter(AssetType.name == 'stock').first()
    if not stock_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock asset type not found"
        )

    # Build query
    query = db.query(Asset).filter(
        Asset.asset_type_id == stock_type.id,
        Asset.is_active == True
    )

    if sector:
        query = query.filter(Asset.sector == sector)

    if market:
        query = query.filter(Asset.market == market)

    # Get assets with pagination
    assets = query.offset(offset).limit(limit).all()

    # Get latest prices for these assets
    asset_ids = [asset.id for asset in assets]

    # Subquery to get latest price per asset
    latest_prices_subquery = db.query(
        AssetPrice.asset_id,
        func.max(AssetPrice.timestamp).label('max_timestamp')
    ).filter(
        AssetPrice.asset_id.in_(asset_ids)
    ).group_by(AssetPrice.asset_id).subquery()

    # Get the actual latest prices
    latest_prices = db.query(AssetPrice).join(
        latest_prices_subquery,
        (AssetPrice.asset_id == latest_prices_subquery.c.asset_id) &
        (AssetPrice.timestamp == latest_prices_subquery.c.max_timestamp)
    ).all()

    # Create price map
    price_map = {p.asset_id: p for p in latest_prices}

    # Build response with prices
    result = []
    for asset in assets:
        price_data = price_map.get(asset.id)
        asset_dict = {
            "id": asset.id,
            "symbol": asset.symbol,
            "name": asset.name,
            "asset_type_id": asset.asset_type_id,
            "description": asset.description,
            "sector": asset.sector,
            "market": asset.market,
            "is_active": asset.is_active,
            "is_demo_data": asset.is_demo_data,
            "latest_price": price_data.price if price_data else None,
            "price_timestamp": price_data.timestamp if price_data else None
        }
        result.append(asset_dict)

    return result


@router.get("/search", response_model=List[AssetListResponse])
def search_assets(
    q: str = Query(..., min_length=1, description="Search query (symbol or name)"),
    asset_type: Optional[str] = None,
    limit: int = Query(20, le=50),
    db: Session = Depends(get_db)
):
    """
    Search assets by symbol or name
    - q: Search query (required, min 1 character)
    - asset_type: Optional filter (stock, etf, mutual_fund, bond, crypto)
    - limit: Max results (default 20, max 50)
    """
    query = db.query(Asset).filter(
        Asset.is_active == True,
        or_(
            Asset.symbol.ilike(f"%{q}%"),
            Asset.name.ilike(f"%{q}%")
        )
    )

    if asset_type:
        asset_type_obj = db.query(AssetType).filter(AssetType.name == asset_type).first()
        if asset_type_obj:
            query = query.filter(Asset.asset_type_id == asset_type_obj.id)

    assets = query.limit(limit).all()
    return assets


@router.get("/{symbol}", response_model=AssetDetailResponse)
def get_asset_by_symbol(symbol: str, db: Session = Depends(get_db)):
    """Get detailed asset information by symbol"""
    asset = db.query(Asset).filter(
        Asset.symbol == symbol.upper(),
        Asset.is_active == True
    ).first()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with symbol '{symbol}' not found"
        )

    return asset


@router.get("/{symbol}/prices", response_model=List[AssetPriceResponse])
def get_asset_prices(
    symbol: str,
    limit: int = Query(30, le=365, description="Number of days (max 365)"),
    db: Session = Depends(get_db)
):
    """Get historical prices for an asset"""
    # Get asset
    asset = db.query(Asset).filter(
        Asset.symbol == symbol.upper(),
        Asset.is_active == True
    ).first()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with symbol '{symbol}' not found"
        )

    # Get prices
    prices = db.query(AssetPrice).filter(
        AssetPrice.asset_id == asset.id
    ).order_by(desc(AssetPrice.timestamp)).limit(limit).all()

    return prices


@router.get("/sectors/list")
def get_sectors(db: Session = Depends(get_db)):
    """Get list of all available sectors"""
    sectors = db.query(Asset.sector).filter(
        Asset.sector.isnot(None),
        Asset.is_active == True
    ).distinct().all()

    return {"sectors": [s[0] for s in sectors if s[0]]}
