from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app

client = TestClient(app)


def test_get_pvz_list():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.get(
        "/pvz",
        headers={"Authorization": f"Bearer {token}"}
    )
 
    assert response.status_code == 200

    pvz_list = response.json()

    assert isinstance(pvz_list, list)

    assert pvz_list[0]["city"] == "Казань"
    assert pvz_list[0]["id"] == "65f9855a-ecc9-4c9c-97fb-51937878e064"
    assert datetime.fromisoformat(pvz_list[0]["registration_date"].replace("Z", "+00:00"))

    assert isinstance(pvz_list[0]["receptions"], list)
    assert len(pvz_list[0]["receptions"]) == 1

    reception = pvz_list[0]["receptions"][0]
    assert reception["id"] == "9f53ae04-1ff7-415e-9a6d-8d9d2872e55f"
    assert reception["status"] == "in_progress"
    assert datetime.fromisoformat(reception["date_time"].replace("Z", "+00:00"))

    assert pvz_list[1]["city"] == "Москва"
    assert pvz_list[1]["id"] == "dfe664a4-0c81-4368-a8c6-9a6f0449de55"
    assert datetime.fromisoformat(pvz_list[1]["registration_date"].replace("Z", "+00:00"))

    assert len(pvz_list[1]["receptions"]) == 2

    reception1 = pvz_list[1]["receptions"][0]
    assert reception1["status"] == "in_progress"
    assert len(reception1["products"]) == 5

    expected_types = ["обувь", "электроника", "одежда"]
    assert set(p["type"] for p in reception1["products"]) == set(expected_types)

    reception2 = pvz_list[1]["receptions"][1]
    assert reception2["status"] == "close"
    assert len(reception2["products"]) == 2
    assert set(p["type"] for p in reception2["products"]) == {"электроника", "обувь"}


def test_create_pvz_wrong_city():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy-mod@example.com",
            "role": "moderator"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.post(
        "/pvz",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "city": "Краснодар"
        }
    )
 
    assert response.status_code == 400

    pvz_resp = response.json()

    assert pvz_resp["detail"] == "PVZ can only be created in Moscow, Saint Petersburg, or Kazan"


def test_create_pvz_wrong_role():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.post(
        "/pvz",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "city": "Москва"
        }
    )
 
    assert response.status_code == 403

    pvz_resp = response.json()

    assert pvz_resp["detail"] == "Operation requires moderator privileges"


def test_create_pvz_wrong_no_role():

    response = client.post(
        "/pvz",
        json={
            "city": "Москва"
        }
    )
 
    assert response.status_code == 403

    pvz_resp = response.json()

    assert pvz_resp["detail"] == "Not authenticated"


def test_create_pvz():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy-mod@example.com",
            "role": "moderator"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.post(
        "/pvz",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "city": "Москва"
        }
    )
 
    assert response.status_code == 201

    pvz_resp = response.json()

    assert pvz_resp["city"] == "Москва"


def test_close_last_reception():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.get(
        "/pvz",
        headers={"Authorization": f"Bearer {token}"},
    )
 
    assert response.status_code == 200

    pvz_list = response.json()

    pvz_id = pvz_list[2]["id"]

    client.post(
        "/receptions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": pvz_id
        }
    )

    close_resp = client.post(
        f"/pvz/{pvz_id}/close_last_reception",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": pvz_id
        }
    )
    assert close_resp.status_code == 200
    
    resp_data = close_resp.json()
    assert resp_data["status"] == "close"
    assert resp_data["pvz_id"] == pvz_id
    

def test_close_last_reception_no_open():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.get(
        "/pvz",
        headers={"Authorization": f"Bearer {token}"},
    )
 
    assert response.status_code == 200

    pvz_list = response.json()

    pvz_id = pvz_list[2]["id"]

    client.post(
        "/receptions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": pvz_id
        }
    )

    client.post(
        f"/pvz/{pvz_id}/close_last_reception",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": pvz_id
        }
    )

    close_resp = client.post(
        f"/pvz/{pvz_id}/close_last_reception",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": pvz_id
        }
    )
    resp_data = close_resp.json()
    
    assert close_resp.status_code == 400
    assert resp_data["detail"] == "No open reception found for this PVZ"


def test_delete_last_product():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.get(
        "/pvz",
        headers={"Authorization": f"Bearer {token}"},
    )
 
    assert response.status_code == 200

    pvz_list = response.json()

    pvz_id = pvz_list[2]["id"]

    client.post(
        "/receptions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": pvz_id
        }
    )

    client.post(
        f"/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": "электроника",
            "pvz_id": pvz_id
        }
    )

    delete_resp = client.post(
        f"/pvz/{pvz_id}/delete_last_product",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": pvz_id
        }
    )
    
    resp_data = delete_resp.json()
    assert delete_resp.status_code == 200
    assert resp_data["message"] == "Product successfully deleted"
    

def test_delete_last_product_no_products():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.get(
        "/pvz",
        headers={"Authorization": f"Bearer {token}"},
    )
 
    assert response.status_code == 200

    pvz_list = response.json()

    pvz_id = pvz_list[2]["id"]

    delete_resp = client.post(
        f"/pvz/{pvz_id}/delete_last_product",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": pvz_id
        }
    )
    
    resp_data = delete_resp.json()
    assert delete_resp.status_code == 400
    assert resp_data["detail"] == "No products to delete in this reception"
