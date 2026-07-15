from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def create_test_data(headers):

    # Create Warehouse 1
    w1 = client.post(
        "/warehouses/",
        json={
            "warehouse_name": "Warehouse_A",
            "location": "Hyderabad",
            "manager_name": "Ramesh",
            "is_active": True
        },
        headers=headers
    )

    assert w1.status_code == 200, w1.json()

    warehouse1_id = w1.json()["id"]


    # Create Warehouse 2
    w2 = client.post(
        "/warehouses/",
        json={
            "warehouse_name": "Warehouse_B",
            "location": "Bangalore",
            "manager_name": "Suresh",
            "is_active": True
        },
        headers=headers
    )

    assert w2.status_code == 200, w2.json()

    warehouse2_id = w2.json()["id"]


    # Create Product with unique SKU
    product = client.post(
        "/products/",
        json={
            "product_name": "Monitor",
            "sku": f"MON{warehouse1_id}_TEST",
            "stock_quantity": 100,
            "unit_price": 15000,
            "warehouse_id": warehouse1_id
        },
        headers=headers
    )

    assert product.status_code == 200, product.json()

    product_id = product.json()["id"]

    return warehouse1_id, warehouse2_id, product_id



def test_create_transfer(headers):

    warehouse1_id, warehouse2_id, product_id = create_test_data(headers)

    response = client.post(
        "/transfers/",
        json={
            "product_id": product_id,
            "from_warehouse": warehouse1_id,
            "to_warehouse": warehouse2_id,
            "quantity": 10
        },
        headers=headers
    )

    assert response.status_code == 200



def test_get_transfers(headers):

    response = client.get(
        "/transfers/",
        headers=headers
    )

    assert response.status_code == 200



def test_get_transfer_by_id(headers):

    response = client.get(
        "/transfers/1",
        headers=headers
    )

    assert response.status_code in [200, 404]



def test_update_transfer(headers):

    warehouse1_id, warehouse2_id, product_id = create_test_data(headers)

    create_response = client.post(
        "/transfers/",
        json={
            "product_id": product_id,
            "from_warehouse": warehouse1_id,
            "to_warehouse": warehouse2_id,
            "quantity": 10
        },
        headers=headers
    )

    assert create_response.status_code == 200

    transfer_id = create_response.json()["id"]


    response = client.put(
        f"/transfers/{transfer_id}",
        json={
            "status": "Completed"
        },
        headers=headers
    )

    assert response.status_code == 200



def test_filter_transfers(headers):

    response = client.get(
        "/transfers/?status=Completed",
        headers=headers
    )

    assert response.status_code == 200



def test_same_warehouse_validation(headers):

    warehouse1_id, _, product_id = create_test_data(headers)

    response = client.post(
        "/transfers/",
        json={
            "product_id": product_id,
            "from_warehouse": warehouse1_id,
            "to_warehouse": warehouse1_id,
            "quantity": 10
        },
        headers=headers
    )

    assert response.status_code == 400



def test_insufficient_stock(headers):

    warehouse1_id, warehouse2_id, product_id = create_test_data(headers)

    response = client.post(
        "/transfers/",
        json={
            "product_id": product_id,
            "from_warehouse": warehouse1_id,
            "to_warehouse": warehouse2_id,
            "quantity": 1000
        },
        headers=headers
    )

    assert response.status_code == 400