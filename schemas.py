from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# =====================================
# User Schemas
# =====================================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# =====================================
# Warehouse Schemas
# =====================================

class WarehouseCreate(BaseModel):
    warehouse_name: str
    location: str
    manager_name: str
    is_active: bool = True


class WarehouseUpdate(BaseModel):
    warehouse_name: Optional[str] = None
    location: Optional[str] = None
    manager_name: Optional[str] = None
    is_active: Optional[bool] = None


class WarehouseResponse(BaseModel):
    id: int
    warehouse_name: str
    location: str
    manager_name: str
    is_active: bool

    class Config:
        from_attributes = True


# =====================================
# Product Schemas
# =====================================

class ProductCreate(BaseModel):
    product_name: str
    sku: str
    stock_quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    warehouse_id: int


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[float] = Field(None, gt=0)


class ProductResponse(BaseModel):
    id: int
    product_name: str
    sku: str
    stock_quantity: int
    unit_price: float
    warehouse_id: int

    class Config:
        from_attributes = True


# =====================================
# Transfer Schemas
# =====================================

class TransferCreate(BaseModel):
    from_warehouse: int
    to_warehouse: int
    product_id: int
    quantity: int = Field(..., gt=0)


class TransferUpdate(BaseModel):
    status: str


class TransferResponse(BaseModel):
    id: int
    from_warehouse: int
    to_warehouse: int
    product_id: int
    quantity: int
    transfer_date: datetime
    status: str

    class Config:
        from_attributes = True