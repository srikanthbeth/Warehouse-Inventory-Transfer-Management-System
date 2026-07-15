from tests.conftest import client


def get_admin_token():
    # Register Admin (ignore if already exists)
    client.post(
        "/auth/register",
        json={
            "username": "WarehouseAdmin",
            "email": "warehouseadmin@test.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": "warehouseadmin@test.com",
            "password": "admin123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


headers = get_admin_token()


def test_create_warehouse():

    response = client.post(
        "/warehouses/",
        json={
            "warehouse_name": "Hyderabad Warehouse",
            "location": "Hyderabad",
            "manager_name": "Ramesh",
            "is_active": True
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["warehouse_name"] == "Hyderabad Warehouse"


def test_get_all_warehouses():

    response = client.get(
        "/warehouses/",
        headers=headers
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_get_warehouse_by_id():

    response = client.get(
        "/warehouses/1",
        headers=headers
    )

    assert response.status_code == 200

    assert response.json()["id"] == 1


def test_update_warehouse():

    response = client.put(
        "/warehouses/1",
        json={
            "location": "Bangalore"
        },
        headers=headers
    )

    assert response.status_code == 200

    assert response.json()["location"] == "Bangalore"


def test_delete_warehouse():

    # Create a warehouse to delete
    create = client.post(
        "/warehouses/",
        json={
            "warehouse_name": "Delete Warehouse",
            "location": "Chennai",
            "manager_name": "Suresh",
            "is_active": True
        },
        headers=headers
    )

    warehouse_id = create.json()["id"]

    response = client.delete(
        f"/warehouses/{warehouse_id}",
        headers=headers
    )

    assert response.status_code == 200