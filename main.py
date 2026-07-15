from fastapi import FastAPI

from database import Base, engine

from routers import auth
from routers import warehouse
from routers import product
from routers import transfer
from routers import reports

# =====================================
# Create Database Tables
# =====================================
Base.metadata.create_all(bind=engine)

# =====================================
# FastAPI App
# =====================================
app = FastAPI(
    title="Warehouse Inventory Transfer Management System",
    version="1.0.0"
)

# =====================================
# Include Routers
# =====================================
app.include_router(auth.router)
app.include_router(warehouse.router)
app.include_router(product.router)
app.include_router(transfer.router)
app.include_router(reports.router)

# =====================================
# Root Endpoint
# =====================================
@app.get("/")
def root():
    return {
        "message": "Welcome to Warehouse Inventory Transfer Management System"
    }