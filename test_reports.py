from tests.conftest import client


def get_admin_headers():

    # Register Admin
    client.post(
        "/auth/register",
        json={
            "username": "ReportAdmin",
            "email": "reportadmin@test.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": "reportadmin@test.com",
            "password": "admin123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


headers = get_admin_headers()


# ==========================================
# Warehouse Inventory Report
# ==========================================

def test_inventory_report():

    response = client.get(
        "/reports/inventory",
        headers=headers
    )

    assert response.status_code == 200


# ==========================================
# Product Search Report
# ==========================================

def test_search_products_report():

    response = client.get(
        "/reports/products/search?keyword=LAP",
        headers=headers
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)


# ==========================================
# Transfer Report
# ==========================================

def test_transfer_report():

    response = client.get(
        "/reports/transfers",
        headers=headers
    )

    assert response.status_code == 200


# ==========================================
# Transfer Report Filter
# ==========================================

def test_transfer_report_filter():

    response = client.get(
        "/reports/transfers?status=Completed",
        headers=headers
    )

    assert response.status_code == 200


# ==========================================
# Pagination
# ==========================================

def test_pagination():

    response = client.get(
        "/reports/transfers?page=1&limit=5",
        headers=headers
    )

    assert response.status_code == 200