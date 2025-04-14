from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app

client = TestClient(app)


def test_create_product_electr():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": "электроника",
            "pvz_id": "65f9855a-ecc9-4c9c-97fb-51937878e064"
        }
    )
 
    assert response.status_code == 201

    product_resp = response.json()

    assert product_resp["type"] == "электроника"
    assert isinstance(product_resp["reception_id"], str)


def test_create_wrong_product():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": "test",
            "pvz_id": "65f9855a-ecc9-4c9c-97fb-51937878e064"
        }
    )
 
    assert response.status_code == 400

    product_resp = response.json()
    assert product_resp["detail"] == "Invalid product type, must be 'электроника', 'одежда', or 'обувь'"



def test_create_product_wrong_pvz():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": "электроника",
            "pvz_id": "65f9855a-ecc9-4c9c-97fb-51937aa8e064"
        }
    )
 
    assert response.status_code == 404

    product_resp = response.json()
    assert product_resp["detail"] == "PVZ not found"