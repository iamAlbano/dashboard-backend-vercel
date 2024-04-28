from app import create_app
from .conftest import create_user
import json


def test_create_user():
    app = create_app()
    client = app.test_client()

    create_user()


def test_create_user_without_required_field():
    app = create_app()
    client = app.test_client()

    user_data = {
        "name": "Guilherme",
        "surname": "Albano",
        "email": "gui@gmail.com",
        "password": "12345678"
    }

    for key in user_data.keys():
        data = user_data.copy()
        data.pop(key)

        response = client.post('/user/create', json=data)

        data = json.loads(response.data)

        assert data["message"] == "Missing "+key+" field"
        assert response.status_code == 400


def test_create_user_with_invalid_email():
    app = create_app()
    client = app.test_client()

    user_data = {
        "name": "Guilherme",
        "surname": "Albano",
        "email": "invalid_email",
        "password": "12345678"
    }

    response = client.post('/user/create', json=user_data)

    data = json.loads(response.data)

    assert data["message"] == "Invalid email"
    assert response.status_code == 400


def test_create_user_with_existing_email():
    app = create_app()
    client = app.test_client()

    user_data = {
        "name": "Guilherme",
        "surname": "Albano",
        "email": "gui@gmail.com",
        "password": "12345678"
    }

    response = client.post('/user/create', json=user_data)

    data = json.loads(response.data)

    assert data["message"] == "User created successfully"

    response = client.post('/user/create', json=user_data)

    data = json.loads(response.data)

    assert data["message"] == "Email already registered"

    assert response.status_code == 400


def test_create_with_blank_field():
    app = create_app()
    client = app.test_client()

    user_data = {
        "name": "Guilherme",
        "surname": "Albano",
        "email": "gui@gmail.com",
        "password": "12345678"
    }

    minimun_length = {
        "name": 3,
        "surname": 3,
        "password": 8,
        "email": 5
    }

    for key in user_data.keys():
        data = user_data.copy()
        data[key] = "a"

        response = client.post('/user/create', json=data)

        data = json.loads(response.data)

        assert data["message"] == key.capitalize()+" must be at least "+str(
            minimun_length[key])+" characters long"

        assert response.status_code == 400
