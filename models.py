from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


# -----------------------------
# User Model
# -----------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)


# -----------------------------
# Warehouse Model
# -----------------------------
class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    manager_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # One Warehouse -> Many Products
    products = relationship("Product", back_populates="warehouse")


# -----------------------------
# Product Model
# -----------------------------
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False, index=True)
    stock_quantity = Column(Integer, default=0)
    unit_price = Column(Float, nullable=False)

    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))

    # Many Products -> One Warehouse
    warehouse = relationship("Warehouse", back_populates="products")


# -----------------------------
# Transfer Model
# -----------------------------
class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)

    from_warehouse = Column(Integer, ForeignKey("warehouses.id"))
    to_warehouse = Column(Integer, ForeignKey("warehouses.id"))

    product_id = Column(Integer, ForeignKey("products.id"))

    quantity = Column(Integer, nullable=False)

    transfer_date = Column(DateTime, default=datetime.utcnow)

    status = Column(String, default="Pending")

    