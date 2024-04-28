from app import create_app
from .conftest import create_user, login_user, create_store, create_temp_csv_file, create_temp_xlsx_file, create_temp_ods_file
from werkzeug.datastructures import FileStorage
import json
import os


def test_if_cant_import_without_login():
    app = create_app()
    client = app.test_client()

    response = client.post('/import/customers')

    assert response.status_code == 401


def test_if_returns_error_when_no_store_id():
    app = create_app()
    client = app.test_client()

    user, token = login_user()

    # Create a temporary CSV file with some example content
    temp_file_path = create_temp_csv_file(
        columns="name,email,phone,birthday,address,city,state,country,zipcode",
        content="John Doe,johndoe@gmail.com,123456789,1990-01-01,Street 1,New York,New York,USA,12345678"
    )

    file_storage = FileStorage(
        stream=open(temp_file_path, 'rb'),
        filename='example.csv',
        name='file',
        content_type='text/csv'
    )

    # Send the CSV file to the endpoint
    with open(temp_file_path, 'rb') as file:
        response = client.post(
            '/import/customers',
            headers={"Authorization": "Bearer " + token},
            content_type='multipart/form-data',
            data={
                'file': file_storage,
                'name_column': 'name',
                'email_column': 'email',
                'phone_column': 'phone',
                'birthday_column': 'birthday',
                'address_column': 'address',
                'city_column': 'city',
                'state_column': 'state',
                'country_column': 'country',
                'zipcode_column': 'zipcode'
            },
        )

    os.remove(temp_file_path)  # Remove the temporary file

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["message"] == "Missing store_id field"


def test_if_returns_error_when_no_file():
    app = create_app()
    client = app.test_client()

    user, token = login_user()

    response = client.post(
        '/import/customers', headers={"Authorization": "Bearer "+token},
        content_type='multipart/form-data',
        data={
            'store_id': user['id'],
            'name_column': 'name',
            'email_column': 'email',
            'phone_column': 'phone',
            'birthday_column': 'birthday',
            'address_column': 'address',
            'city_column': 'city',
            'state_column': 'state',
            'country_column': 'country',
            'zipcode_column': 'zipcode'
        },
    )

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["message"] == "No file part in the request"


def test_upload_csv_file():
    app = create_app()
    client = app.test_client()

    user, token = login_user()
    store = create_store(token, users=[user['id']])

    # Create a temporary CSV file with some example content
    temp_file_path = create_temp_csv_file(
        columns="name,email,phone,birthday,address,city,state,country,zipcode",
        content="John Doe,johndoe@gmail.com,123456789,1990-01-01,Street 1,New York,New York,USA,12345678\nMary Doe,marydoe@gmail.com,987654321,1990-01-01,Street 2,New York,New York,USA,12345678\nJim Doe,jimdoe@gmail.com,987654321,1990-01-01,Street 2,New York,New York,USA,12345678"
    )

    file_storage = FileStorage(
        stream=open(temp_file_path, 'rb'),
        filename='example.csv',
        name='file',
        content_type='text/csv'
    )

    # Send the CSV file to the endpoint
    with open(temp_file_path, 'rb') as file:
        response = client.post(
            '/import/customers',
            headers={"Authorization": "Bearer " + token},
            content_type='multipart/form-data',
            data={
                'file': file_storage,
                'store_id': store['id'],
                'name_column': 'name',
                'email_column': 'email',
                'phone_column': 'phone',
                'birthday_column': 'birthday',
                'address_column': 'address',
                'city_column': 'city',
                'state_column': 'state',
                'country_column': 'country',
                'zipcode_column': 'zipcode'
            },
        )

    os.remove(temp_file_path)  # Remove the temporary file

    data = json.loads(response.data)

    assert response.status_code == 200
    assert "message" in json.loads(response.data)
    assert "imported" in json.loads(response.data)
    assert "failed" in json.loads(response.data)
    assert data["failed"] == 0
    assert data["imported"] == 3
    assert data["message"] == "3 customers imported successfully"
