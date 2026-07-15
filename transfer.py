from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db
from dependencies import admin_or_manager

router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"]
)


# ==========================================
# Create Transfer
# ==========================================
@router.post("/", response_model=schemas.TransferResponse)
def create_transfer(
    transfer: schemas.TransferCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_manager)
):

    return crud.create_transfer(db, transfer)


# ==========================================
# Get All Transfers
# ==========================================
@router.get("/", response_model=List[schemas.TransferResponse])
def get_transfers(
    page: int = 1,
    limit: int = 10,
    status: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_manager)
):

    skip = (page - 1) * limit

    if status:
        return crud.filter_transfers(
            db=db,
            status=status,
            skip=skip,
            limit=limit
        )

    return crud.get_transfers(
        db=db,
        skip=skip,
        limit=limit
    )


# ==========================================
# Get Transfer By ID
# ==========================================
@router.get("/{transfer_id}", response_model=schemas.TransferResponse)
def get_transfer(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_manager)
):

    return crud.get_transfer(
        db,
        transfer_id
    )


# ==========================================
# Update Transfer Status
# ==========================================
@router.put("/{transfer_id}", response_model=schemas.TransferResponse)
def update_transfer(
    transfer_id: int,
    transfer: schemas.TransferUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_manager)
):

    return crud.update_transfer(
        db,
        transfer_id,
        transfer
    )