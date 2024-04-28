from app import create_app
from .conftest import create_user, create_store, login_user, create_temp_csv_file, create_temp_xlsx_file, create_temp_ods_file
from werkzeug.datastructures import FileStorage
import json
import os


def test_if_cant_import_without_login():
    app = create_app()
    client = app.test_client()

    response = client.post('/import/sales')

    assert response.status_code == 401


def test_if_returns_error_when_no_file():
    app = create_app()
    client = app.test_client()

    user, token = login_user()

    body = {"file": ""}

    response = client.post(
        '/import/sales', headers={"Authorization": "Bearer "+token}, json=body)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["message"] == "No file part in the request"


def test_if_throws_missing_product_column_error():
    app = create_app()
    client = app.test_client()

    user, token = login_user()

    # Create a temporary CSV file with some example content
    temp_file_path = create_temp_csv_file(
        columns="name,description,category,price,stock",
        content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200"
    )

    products_file = FileStorage(
        stream=open(temp_file_path, 'rb'),
        filename='example.csv',
        name='file',
        content_type='text/csv'
    )

    # Send the CSV file to the endpoint
    with open(temp_file_path, 'rb') as file:
        response = client.post(
            '/import/sales',
            headers={"Authorization": "Bearer " + token},
            content_type='multipart/form-data',
            data={
                'sales_file': products_file,
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
    assert "message" in json.loads(response.data)
    assert data["message"] == "Missing product_column field"


def test_import():
    app = create_app()
    client = app.test_client()

    user, token = login_user()
    store = create_store(token, users=[user['id']])

    # Create a temporary CSV file with some example products content
    products_temp_file = create_temp_csv_file(
        columns="name,description,category,price,stock",
        content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200"
    )

    products_file = FileStorage(
        stream=open(products_temp_file, 'rb'),
        filename='products.csv',
        name='file',
        content_type='text/csv'
    )

    # Create a temporary CSV file with some example sales content
    sales_temp_file = create_temp_csv_file(
        columns="product_name",
        content="Product1\nProduct2"
    )

    sales_file = FileStorage(
        stream=open(sales_temp_file, 'rb'),
        filename='products.csv',
        name='file',
        content_type='text/csv'
    )

    # Send the CSV file to the endpoint
    with open(products_temp_file, 'rb') as products_file, open(sales_temp_file, 'rb') as sales_file:
        response = client.post(
            '/import/sales',
            headers={"Authorization": "Bearer " + token},
            content_type='multipart/form-data',
            data={
                'store_id': store['id'],
                'sales_file': sales_file,
                'products_file': products_file,
                'product_column': 'product_name',
            },
        )

    os.remove(products_temp_file)  # Remove the temporary file
    os.remove(sales_temp_file)  # Remove the temporary file

    data = json.loads(response.data)

    assert response.status_code == 200
    assert "message" in json.loads(response.data)
    assert data["message"] == "2 sales imported successfully, 0 failed imports"
    assert "data" in json.loads(response.data)
