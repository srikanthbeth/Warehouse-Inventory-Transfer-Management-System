# Warehouse Inventory Transfer Management System

## Project Overview

The Warehouse Inventory Transfer Management System is a backend application developed using **FastAPI**. It provides secure warehouse, product, and inventory transfer management with **JWT Authentication**, **Role-Based Authorization**, inventory reports, and search functionality.

This project demonstrates REST API development, authentication, business logic implementation, SQLAlchemy ORM, and SQLite database integration.

---

# Features

## Authentication

- User Registration
- User Login
- JWT Token Authentication
- Password Hashing using bcrypt
- Role-Based Authorization

### Roles

- Admin
- Warehouse Manager

---

# Warehouse Management

Manage warehouses with the following information:

- Warehouse Name
- Location
- Manager Name
- Active Status

### APIs

| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | /warehouses | Create Warehouse |
| GET | /warehouses | Get All Warehouses |
| GET | /warehouses/{id} | Get Warehouse by ID |
| PUT | /warehouses/{id} | Update Warehouse |
| DELETE | /warehouses/{id} | Delete Warehouse |

---

# Product Management

Manage products stored in warehouses.

### Product Fields

- Product Name
- SKU (Unique)
- Stock Quantity
- Unit Price
- Warehouse ID

### APIs

| Method | Endpoint |
|---------|-----------|
| POST | /products |
| GET | /products |
| GET | /products/{id} |
| PUT | /products/{id} |
| GET | /products/search |

---

# Stock Transfer

Transfer inventory between warehouses.

### Transfer Fields

- Source Warehouse
- Destination Warehouse
- Product
- Quantity
- Transfer Date
- Status

### Status

- Pending
- Approved
- Completed
- Cancelled

### APIs

| Method | Endpoint |
|---------|-----------|
| POST | /transfers |
| GET | /transfers |
| GET | /transfers/{id} |
| PUT | /transfers/{id} |

---

# Reports

### Warehouse Inventory Report

Displays warehouse-wise inventory.

Endpoint

```
GET /reports/inventory
```

### Product Search

Search products using

- Product Name
- SKU

Endpoint

```
GET /reports/products/search
```

### Transfer Report

Filter transfers by status.

Endpoint

```
GET /reports/transfers
```

---

# Business Rules

- JWT Authentication required
- SKU must be unique
- Stock quantity must be greater than zero
- Source and destination warehouses cannot be the same
- Stock cannot be transferred if insufficient quantity exists
- Completed transfers update inventory
- Cancelled transfers do not affect inventory
- Admin can access all modules
- Warehouse Manager can manage products and transfers

---

# Technologies Used

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Passlib (bcrypt)
- Uvicorn
- Pytest

---

# Project Structure

```
warehouse_inventory_transfer_management_system/
│
├── routers/
│   ├── auth.py
│   ├── warehouse.py
│   ├── product.py
│   ├── transfer.py
│   ├── reports.py
│   └── __init__.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_warehouse.py
│   ├── test_product.py
│   ├── test_transfer.py
│   └── test_reports.py
│
├── auth.py
├── crud.py
├── database.py
├── dependencies.py
├── main.py
├── models.py
├── schemas.py
├── inventory.db
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
```

```bash
cd warehouse_inventory_transfer_management_system
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
uvicorn main:app --reload
```

Server

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Authentication Flow

## Register

```
POST /auth/register
```

Example

```json
{
  "username": "Admin",
  "email": "admin@example.com",
  "password": "admin123",
  "role": "Admin"
}
```

---

## Login

```
POST /auth/login
```

Use

```
username = admin@example.com
password = admin123
```

Copy the generated JWT token.

Click **Authorize** in Swagger and enter:

```
Bearer <your_token>
```

---

# Running Tests

Run all tests

```bash
pytest -v
```

Run a specific test

```bash
pytest tests/test_auth.py -v
```

---

# Validation

- Unique SKU validation
- Positive stock quantity validation
- Positive unit price validation
- Warehouse existence validation
- Product existence validation
- Inventory validation
- JWT Authentication
- Role-Based Authorization

---

# Future Enhancements

- PostgreSQL Support
- Docker Deployment
- Email Notifications
- Inventory Dashboard
- Audit Logs
- Export Reports to Excel/PDF

---

# Author

**Srikanth Bethamcharla**

Backend Developer

---

# License

This project is developed for educational and assignment purposes.
