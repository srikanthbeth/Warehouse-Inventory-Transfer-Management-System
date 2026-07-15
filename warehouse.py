from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import get_db
from dependencies import admin_only

router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)


# ==========================================
# Create Warehouse
# ==========================================
@router.post("/", response_model=schemas.WarehouseResponse)
def create_warehouse(
    warehouse: schemas.WarehouseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return crud.create_warehouse(db, warehouse)


# ==========================================
# Get All Warehouses
# ==========================================
@router.get("/", response_model=List[schemas.WarehouseResponse])
def get_warehouses(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    skip = (page - 1) * limit

    return crud.get_warehouses(
        db=db,
        skip=skip,
        limit=limit
    )


# ==========================================
# Get Warehouse By ID
# ==========================================
@router.get("/{warehouse_id}", response_model=schemas.WarehouseResponse)
def get_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return crud.get_warehouse(
        db,
        warehouse_id
    )


# ==========================================
# Update Warehouse
# ==========================================
@router.put("/{warehouse_id}", response_model=schemas.WarehouseResponse)
def update_warehouse(
    warehouse_id: int,
    warehouse: schemas.WarehouseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return crud.update_warehouse(
        db,
        warehouse_id,
        warehouse
    )


# ==========================================
# Delete Warehouse
# ==========================================
@router.delete("/{warehouse_id}")
def delete_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return crud.delete_warehouse(
        db,
        warehouse_id
    )