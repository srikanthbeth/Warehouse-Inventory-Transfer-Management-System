from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import get_db
from dependencies import admin_or_manager

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# ==========================================
# Create Product
# ==========================================
@router.post("/", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_manager)
):

    return crud.create_product(db, product)


# ==========================================
# Get All Products
# ==========================================
@router.get("/", response_model=List[schemas.ProductResponse])
def get_products(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_manager)
):

    skip = (page - 1) * limit

    return crud.get_products(
        db=db,
        skip=skip,
        limit=limit
    )


# ==========================================
# Get Product By ID
# ==========================================
@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_manager)
):

    return crud.get_product(
        db,
        product_id
    )


# ==========================================
# Update Product
# ==========================================
@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_manager)
):

    return crud.update_product(
        db,
        product_id,
        product
    )


# ==========================================
# Search Product
# ==========================================
@router.get("/search/", response_model=List[schemas.ProductResponse])
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