from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_integration():
    mod_token = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy-mod@example.com",
            "role": "moderator"
        }
    )
    mod_token = mod_token.json()["access_token"]

    pvz_info = client.post(
        "/pvz",
        headers={"Authorization": f"Bearer {mod_token}"},
        json={
            "city": "Москва"
        }
    )

    pvz_id = pvz_info.json()["id"]

    emp_token = client.post(
        "/dummyLogin",
        json={
            "username": "test-user-dummy@example.com",
            "role": "employee"
        }
    )

    emp_token = emp_token.json()["access_token"]

    
    client.post(
        "/receptions",
        headers={"Authorization": f"Bearer {emp_token}"},
        json={
            "pvz_id": pvz_id
        }
    )

    for _ in range(50):
        client.post(
            "/prdoucts",
            headers={"Authorization": f"Bearer {emp_token}"},
            json={
                "type": "электроника",
                "pvz_id": pvz_id
            }
        )

    close_resp = client.post(
        f"/pvz/{pvz_id}/close_last_reception",
        headers={"Authorization": f"Bearer {emp_token}"},
        json={
            "pvz_id": pvz_id
        }
    )
    assert close_resp.status_code == 200
    
    resp_data = close_resp.json()
    assert resp_data["status"] == "close"
    assert resp_data["pvz_id"] == pvz_id
    