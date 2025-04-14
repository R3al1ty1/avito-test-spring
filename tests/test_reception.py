from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app

client = TestClient(app)


def test_create_reception_not_closed():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.post(
        "/receptions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": "65f9855a-ecc9-4c9c-97fb-51937878e064"
        }
    )
 
    assert response.status_code == 400

    reception_resp = response.json()

    assert reception_resp["detail"] == "There is already an open reception for this PVZ"


def test_create_reception_wrong_pvz():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    response = client.post(
        "/receptions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": "65f9855a-ecc9-4c9c-97fb-51937818e064"
        }
    )
 
    assert response.status_code == 404

    reception_resp = response.json()

    assert reception_resp["detail"] == "PVZ not found"


def test_create_new_reception():
    token_resp = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )
    token = token_resp.json()["access_token"]

    pvz_id = "65f9855a-ecc9-4c9c-97fb-51937878e064"

    response = client.post(
        f"/pvz/{pvz_id}/close_last_reception",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": pvz_id
        }
    )
    response = client.post(
        "/receptions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pvz_id": pvz_id
        }
    )
 
    assert response.status_code == 201

    reception_resp = response.json()

    assert reception_resp["pvz_id"] == pvz_id
    assert reception_resp["status"] == "in_progress"
    assert isinstance(reception_resp["id"], str)

