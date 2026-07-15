from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException

import models
import schemas
from auth import hash_password, verify_password


# =====================================================
# USER CRUD
# =====================================================

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email
    ).first()


def create_user(db: Session, user: schemas.UserRegister):

    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(db: Session, email: str, password: str):

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user

# =====================================================
# WAREHOUSE CRUD
# =====================================================

def create_warehouse(db: Session, warehouse: schemas.WarehouseCreate):

    db_warehouse = models.Warehouse(
        warehouse_name=warehouse.warehouse_name,
        location=warehouse.location,
        manager_name=warehouse.manager_name,
        is_active=warehouse.is_active
    )

    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)

    return db_warehouse


def get_warehouses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Warehouse).offset(skip).limit(limit).all()


def get_warehouse(db: Session, warehouse_id: int):

    warehouse = db.query(models.Warehouse).filter(
        models.Warehouse.id == warehouse_id
    ).first()

    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found."
        )

    return warehouse


def update_warehouse(
    db: Session,
    warehouse_id: int,
    warehouse: schemas.WarehouseUpdate
):

    db_warehouse = get_warehouse(db, warehouse_id)

    for key, value in warehouse.model_dump(exclude_unset=True).items():
        setattr(db_warehouse, key, value)

    db.commit()
    db.refresh(db_warehouse)

    return db_warehouse


def delete_warehouse(db: Session, warehouse_id: int):

    warehouse = get_warehouse(db, warehouse_id)

    db.delete(warehouse)
    db.commit()

    return {"message": "Warehouse deleted successfully."}

# =====================================================
# PRODUCT CRUD
# =====================================================

def get_product_by_sku(db: Session, sku: str):
    return db.query(models.Product).filter(
        models.Product.sku == sku
    ).first()


def create_product(db: Session, product: schemas.ProductCreate):

    # Check if warehouse exists
    warehouse = db.query(models.Warehouse).filter(
        models.Warehouse.id == product.warehouse_id
    ).first()

    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found."
        )

    # SKU must be unique
    existing_product = get_product_by_sku(db, product.sku)

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="SKU already exists."
        )

    db_product = models.Product(
        product_name=product.product_name,
        sku=product.sku,
        stock_quantity=product.stock_quantity,
        unit_price=product.unit_price,
        warehouse_id=product.warehouse_id
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return product


def update_product(
    db: Session,
    product_id: int,
    product: schemas.ProductUpdate
):

    db_product = get_product(db, product_id)

    update_data = product.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    return db_product


def search_products(
    db: Session,
    search: str,
    skip: int = 0,
    limit: int = 10
):

    return db.query(models.Product).filter(
        or_(
            models.Product.product_name.ilike(f"%{search}%"),
            models.Product.sku.ilike(f"%{search}%")
        )
    ).offset(skip).limit(limit).all()

# =====================================================
# TRANSFER CRUD
# =====================================================

def create_transfer(db: Session, transfer: schemas.TransferCreate):

    # Source and destination cannot be same
    if transfer.from_warehouse == transfer.to_warehouse:
        raise HTTPException(
            status_code=400,
            detail="Source and destination warehouses cannot be the same."
        )

    # Check source warehouse
    source = db.query(models.Warehouse).filter(
        models.Warehouse.id == transfer.from_warehouse
    ).first()

    if not source:
        raise HTTPException(
            status_code=404,
            detail="Source warehouse not found."
        )

    # Check destination warehouse
    destination = db.query(models.Warehouse).filter(
        models.Warehouse.id == transfer.to_warehouse
    ).first()

    if not destination:
        raise HTTPException(
            status_code=404,
            detail="Destination warehouse not found."
        )

    # Check product
    product = db.query(models.Product).filter(
        models.Product.id == transfer.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    # Product must belong to source warehouse
    if product.warehouse_id != transfer.from_warehouse:
        raise HTTPException(
            status_code=400,
            detail="Product does not belong to source warehouse."
        )

    # Stock validation
    if product.stock_quantity < transfer.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock."
        )

    db_transfer = models.Transfer(
        from_warehouse=transfer.from_warehouse,
        to_warehouse=transfer.to_warehouse,
        product_id=transfer.product_id,
        quantity=transfer.quantity,
        status="Pending"
    )

    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)

    return db_transfer


def get_transfers(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.Transfer).offset(skip).limit(limit).all()


def get_transfer(db: Session, transfer_id: int):

    transfer = db.query(models.Transfer).filter(
        models.Transfer.id == transfer_id
    ).first()

    if not transfer:
        raise HTTPException(
            status_code=404,
            detail="Transfer not found."
        )

    return transfer
def update_transfer(
    db: Session,
    transfer_id: int,
    transfer: schemas.TransferUpdate
):

    db_transfer = get_transfer(db, transfer_id)

    # Already completed
    if db_transfer.status == "Completed":
        raise HTTPException(
            status_code=400,
            detail="Transfer already completed."
        )

    # Cancelled
    if transfer.status == "Cancelled":

        db_transfer.status = "Cancelled"

        db.commit()
        db.refresh(db_transfer)

        return db_transfer

    # Approved
    if transfer.status == "Approved":

        db_transfer.status = "Approved"

        db.commit()
        db.refresh(db_transfer)

        return db_transfer

    # Completed
    if transfer.status == "Completed":

        product = get_product(db, db_transfer.product_id)

        if product.stock_quantity < db_transfer.quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock."
            )

        # Reduce stock
        product.stock_quantity -= db_transfer.quantity

        # Product moved to destination warehouse
        product.warehouse_id = db_transfer.to_warehouse

        db_transfer.status = "Completed"

        db.commit()

        db.refresh(product)
        db.refresh(db_transfer)

        return db_transfer

    raise HTTPException(
        status_code=400,
        detail="Invalid transfer status."
    )

def filter_transfers(
    db: Session,
    status: str,
    skip: int = 0,
    limit: int = 10
):

    return (
        db.query(models.Transfer)
        .filter(models.Transfer.status == status)
        .offset(skip)
        .limit(limit)
        .all()
    )

# =====================================================
# REPORTS CRUD
# =====================================================

from sqlalchemy.orm import joinedload


def warehouse_inventory_report(db: Session):
    """
    Returns all warehouses with their products.
    """

    warehouses = (
        db.query(models.Warehouse)
        .options(joinedload(models.Warehouse.products))
        .all()
    )

    report = []

    for warehouse in warehouses:

        products = []

        for product in warehouse.products:
            products.append({
                "product_id": product.id,
                "product_name": product.product_name,
                "sku": product.sku,
                "stock_quantity": product.stock_quantity,
                "unit_price": product.unit_price
            })

        report.append({
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.warehouse_name,
            "location": warehouse.location,
            "products": products
        })

    return report


def search_product(
    db: Session,
    keyword: str,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(models.Product)
        .filter(
            or_(
                models.Product.product_name.ilike(f"%{keyword}%"),
                models.Product.sku.ilike(f"%{keyword}%")
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def transfer_report(
    db: Session,
    status: str = None,
    skip: int = 0,
    limit: int = 10
):

    query = db.query(models.Transfer)

    if status:
        query = query.filter(
            models.Transfer.status == status
        )

    return query.offset(skip).limit(limit).all()