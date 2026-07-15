import uuid

from conftest import client


# Create product
def test_create_product(headers):

    response = client.post(
        "/products/",
        json={
            "product_name": "Laptop",
            "sku": f"LAP{uuid.uuid4().hex[:6]}",
            "stock_quantity": 100,
            "unit_price": 50000,
            "warehouse_id": 1
        },
        headers=headers
    )

    assert response.status_code == 200


# Get all products
def test_get_products(headers):

    response = client.get(
        "/products/",
        headers=headers
    )

    assert response.status_code == 200


# Get product by id
def test_get_product_by_id(headers):

    response = client.get(
        "/products/1",
        headers=headers
    )

    assert response.status_code in [200, 404]


# Update product
def test_update_product(headers):

    response = client.put(
        "/products/1",
        json={
            "unit_price": 60000
        },
        headers=headers
    )

    assert response.status_code in [200, 404]


# Search product
def test_search_product(headers):

    response = client.get(
        "/products/search/?keyword=LAP",
        headers=headers
    )

    assert response.status_code == 200


# Duplicate SKU validation
def test_duplicate_sku(headers):

    sku = f"DUP{uuid.uuid4().hex[:6]}"

    # Create first product
    first_response = client.post(
        "/products/",
        json={
            "product_name": "Laptop Duplicate Test",
            "sku": sku,
            "stock_quantity": 50,
            "unit_price": 55000,
            "warehouse_id": 1
        },
        headers=headers
    )

    assert first_response.status_code == 200


    # Create duplicate product
    response = client.post(
        "/products/",
        json={
            "product_name": "Laptop Duplicate",
            "sku": sku,
            "stock_quantity": 20,
            "unit_price": 60000,
            "warehouse_id": 1
        },
        headers=headers
    )

    assert response.status_code == 400