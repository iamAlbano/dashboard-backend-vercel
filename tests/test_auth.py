from app import create_app
from .conftest import create_user, login_user
import json


def test_login_successfully():
    app = create_app()
    client = app.test_client()

    user = create_user()


def test_login_with_invalid_email():
    app = create_app()
    client = app.test_client()

    user = create_user()

    login_data = {
        "email": "invalid_email@gmail.com",
        "password": "12345678"
    }

    response = client.post('/auth/login', json=login_data)

    data = json.loads(response.data)

    assert data["message"] == "Invalid email or password"
    assert response.status_code == 400
    assert "user" not in data


def test_login_with_invalid_password():
    app = create_app()
    client = app.test_client()

    user = create_user()

    login_data = {
        "email": "gui@gmail.com",
        "password": "MY_PASSWORD_123"
    }

    response = client.post('/auth/login', json=login_data)

    data = json.loads(response.data)

    assert data["message"] == "Invalid email or password"
    assert response.status_code == 400
    assert "user" not in data


def test_login_with_missing_fields():
    app = create_app()
    client = app.test_client()

    user = create_user()

    login_data = {
        "email": "gui@gmail.com",
        "password": "my_password_123"
    }

    for field in ["email", "password"]:
        invalid_data = login_data.copy()
        del invalid_data[field]

        response = client.post('/auth/login', json=invalid_data)

        data = json.loads(response.data)

        assert data["message"] == "Invalid email or password"
        assert response.status_code == 400
        assert "user" not in data


def test_if_should_not_have_access_to_protected_route_without_token():
    app = create_app()
    client = app.test_client()

    response = client.get('/')

    assert response.status_code == 401


def test_if_should_have_access_to_protected_route_with_token():
    app = create_app()
    client = app.test_client()

    user, token = login_user()

    response = client.get(
        '/', headers={"Authorization": "Bearer "+token})

    data = json.loads(response.data)

    assert data["message"] == "Hello World from a protected route!"
    assert response.status_code == 200
