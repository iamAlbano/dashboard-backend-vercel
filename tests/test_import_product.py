from app import create_app
from .conftest import create_user, login_user, create_store, create_temp_csv_file, create_temp_xlsx_file, create_temp_ods_file
from werkzeug.datastructures import FileStorage
import json
import os


def test_if_cant_import_without_login():
    app = create_app()
    client = app.test_client()

    response = client.post('/import/products')

    assert response.status_code == 401


def test_if_returns_error_when_no_store_id():
    app = create_app()
    client = app.test_client()

    user, token = login_user()

    # Create a temporary CSV file with some example content
    temp_file_path = create_temp_csv_file(
        columns="name,description,category,price,stock",
        content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200"
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
            '/import/products',
            headers={"Authorization": "Bearer " + token},
            content_type='multipart/form-data',
            data={
                'file': file_storage,
                'name_column': 'name',
                'description_column': 'description',
                'category_column': 'category',
                'price_column': 'price',
                'stock_column': 'stock',
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
        '/import/products', headers={"Authorization": "Bearer "+token},
        content_type='multipart/form-data',
        data={
            'store_id': user['id'],
            'name_column': 'name',
            'description_column': 'description',
            'category_column': 'category',
            'price_column': 'price',
            'stock_column': 'stock',
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
        columns="name,description,category,price,stock",
        content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200"
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
            '/import/products',
            headers={"Authorization": "Bearer " + token},
            content_type='multipart/form-data',
            data={
                'file': file_storage,
                'store_id': store['id'],
                'name_column': 'name',
                'description_column': 'description',
                'category_column': 'category',
                'price_column': 'price',
                'stock_column': 'stock',
            },
        )

    os.remove(temp_file_path)  # Remove the temporary file

    data = json.loads(response.data)

    assert response.status_code == 200
    assert "message" in json.loads(response.data)
    assert "imported" in json.loads(response.data)
    assert "failed" in json.loads(response.data)
    assert data["message"] == "2 products imported successfully"
    assert data["imported"] == 2
    assert data["failed"] == 0


def test_upload_xlsx_file():
    app = create_app()
    client = app.test_client()

    user, token = login_user()
    store = create_store(token, users=[user['id']])

    # Create a temporary CSV file with some example content
    temp_file_path = create_temp_xlsx_file(
        columns="name,description,category,price,stock",
        content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200"
    )

    file_storage = FileStorage(
        stream=open(temp_file_path, 'rb'),
        filename='example.xlsx',
        name='file',
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Send the CSV file to the endpoint
    with open(temp_file_path, 'rb') as file:
        response = client.post(
            '/import/products',
            headers={"Authorization": "Bearer " + token},
            content_type='multipart/form-data',
            data={
                'store_id': store['id'],
                'file': file_storage,
                'name_column': 'name',
                'description_column': 'description',
                'category_column': 'category',
                'price_column': 'price',
                'stock_column': 'stock',
            },
        )

    os.remove(temp_file_path)  # Remove the temporary file

    data = json.loads(response.data)

    assert response.status_code == 200
    assert "message" in json.loads(response.data)
    assert "imported" in json.loads(response.data)
    assert "failed" in json.loads(response.data)
    assert data["message"] == "2 products imported successfully"
    assert data["imported"] == 2
    assert data["failed"] == 0


def test_upload_ods_file():
    app = create_app()
    client = app.test_client()

    user, token = login_user()
    store = create_store(token, users=[user['id']])

    # Create a temporary ODS file with some example content
    temp_file_path = create_temp_ods_file(
        columns="name,description,category,price,stock",
        content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200"
    )

    file_storage = FileStorage(
        stream=open(temp_file_path, 'rb'),
        filename='example.ods',
        name='file',
        content_type='application/vnd.oasis.opendocument.spreadsheet'
    )

    # Send the ODS file to the endpoint
    with open(temp_file_path, 'rb') as file:
        response = client.post(
            '/import/products',
            headers={"Authorization": "Bearer " + token},
            content_type='multipart/form-data',
            data={
                'store_id': store['id'],
                'file': file_storage,
                'name_column': 'name',
                'description_column': 'description',
                'category_column': 'category',
                'price_column': 'price',
                'stock_column': 'stock',
            },
        )

    os.remove(temp_file_path)  # Remove the temporary file

    data = json.loads(response.data)

    assert response.status_code == 200
    assert "message" in json.loads(response.data)
    assert "imported" in json.loads(response.data)
    assert "failed" in json.loads(response.data)
    assert data["message"] == "2 products imported successfully"
    assert data["imported"] == 2
    assert data["failed"] == 0


def test_upload_fails_without_column_name():
    app = create_app()
    client = app.test_client()

    user, token = login_user()
    store = create_store(token, users=[user['id']])

    # Create a temporary CSV file with some example content
    temp_file_path = create_temp_xlsx_file(
        columns="name,description,category,price,stock",
        content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200"
    )

    file_storage = FileStorage(
        stream=open(temp_file_path, 'rb'),
        filename='example.xlsx',
        name='file',
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Send the CSV file to the endpoint
    with open(temp_file_path, 'rb') as file:
        response = client.post(
            '/import/products',
            headers={"Authorization": "Bearer " + token},
            content_type='multipart/form-data',
            data={
                'store_id': store['id'],
                'file': file_storage,
                'name_column': '',
                'description_column': 'description',
                'category_column': 'category',
                'price_column': 'price',
                'stock_column': 'stock',
            },
        )

    os.remove(temp_file_path)  # Remove the temporary file

    data = json.loads(response.data)

    assert response.status_code == 400
    assert "message" in json.loads(response.data)
    assert data["message"] == "Missing name_column field"


def test_upload_only_with_column_name():
    app = create_app()
    client = app.test_client()

    user, token = login_user()
    store = create_store(token, users=[user['id']])

    # Create a temporary CSV file with some example content
    temp_file_path = create_temp_xlsx_file(
        columns="name,description,category,price,stock",
        content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200"
    )

    file_storage = FileStorage(
        stream=open(temp_file_path, 'rb'),
        filename='example.xlsx',
        name='file',
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Send the CSV file to the endpoint
    with open(temp_file_path, 'rb') as file:
        response = client.post(
            '/import/products',
            headers={"Authorization": "Bearer " + token},
            content_type='multipart/form-data',
            data={
                'store_id': store['id'],
                'file': file_storage,
                'name_column': 'name',
            },
        )

    os.remove(temp_file_path)  # Remove the temporary file

    data = json.loads(response.data)

    assert response.status_code == 200
    assert "message" in json.loads(response.data)
    assert "imported" in json.loads(response.data)
    assert "failed" in json.loads(response.data)
    assert data["message"] == "2 products imported successfully"
    assert data["imported"] == 2
    assert data["failed"] == 0
