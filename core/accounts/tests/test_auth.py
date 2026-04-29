import pytest
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_register_user(client):
    response = client.post("/api/auth/register/", {
        "email": "test@example.com",
        "username": "testuser",
        "password": "strongpassword"
    })

    assert response.status_code == 201
    assert response.data["message"] == "User Created"

@pytest.mark.django_db
def test_login_user(client):
    client.post("/api/auth/register/", {
        "email": "test@example.com",
        "username": "testuser",
        "password": "strongpassword"
    })    

    response = client.post("/api/auth/login/", {
        "email": "test@example.com",
        "password": "strongpassword"
    })

    assert response.status_code == 200
    assert "access_token" in response.cookies

@pytest.mark.django_db
def test_logout_user(client):
    client.post("/api/auth/register", {
        "email": "test@example.com",
        "username": "testuser",
        "password": "strongpassword"
    })

    login = client.post("/api/auth/login/", {
        "email": "test@example.com",
        "password": "strongpassword"
    })

    response = client.post("/api/auth/logout/")

    assert response.status_code == 200
    assert response.data["message"] == "Logged out"