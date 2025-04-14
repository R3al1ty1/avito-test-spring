from fastapi.testclient import TestClient

import pytest
from src.core.db_helper import get_db_connection
from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
async def cleanup_db():
    """Очистка тестовых данных перед каждым тестом"""
    conn = await get_db_connection()
    try:
        await conn.execute("DELETE FROM users WHERE email LIKE 'test-%'")
    finally:
        await conn.close()


def test_wrong_role_register():
    response = client.post(
        "/register",
        json={
            "email": "test-user@example.com",
            "role": "test",
            "password": "test-password"
        }
    )
 
    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Invalid role, must be 'employee' or 'moderator'"


def test_wrong_email_register():
    response = client.post(
        "/register",
        json={
            "email": "test-user",
            "role": "moderator",
            "password": "test-password"
        }
    )
 
    assert response.status_code == 422


def test_register_moderator():
    response = client.post(
        "/register",
        json={
            "email": "test-mod@example.com",
            "role": "moderator",
            "password": "test-password"
        }
    )
 
    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test-mod@example.com"
    assert data["role"] == "moderator"


def test_register_employee():
    response = client.post(
        "/register",
        json={
            "email": "test-emp@example.com",
            "role": "employee",
            "password": "test-password"
        }
    )
 
    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test-emp@example.com"
    assert data["role"] == "employee"


def test_login_employee():
    response = client.post(
        "/login",
        json={
            "email": "test-emp@example.com",
            "password": "test-password"
        }
    )
 
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["access_token"], str)