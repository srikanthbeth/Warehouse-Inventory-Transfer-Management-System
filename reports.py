from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from database import get_db
from dependencies import admin_or_manager

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# =====================================================
# Warehouse Inventory Report
# =====================================================

@router.get("/inventory")
def warehouse_inventory(
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_manager)
):

    return crud.warehouse_inventory_report(db)


# =====================================================
# Search Products
# =====================================================

@router.get("/products/search")
def search_products(
    keyword: str,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_manager)
):

    skip = (page - 1) * limit

    return crud.search_product(
        db=db,
        keyword=keyword,
        skip=skip,
        limit=limit
    )


# =====================================================
# Transfer Report
# =====================================================

@router.get("/transfers")
def transfer_report(
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_manager)
):

    skip = (page - 1) * limit

    return crud.transfer_report(
        db=db,
        status=status,
        skip=skip,
        limit=limit
    )