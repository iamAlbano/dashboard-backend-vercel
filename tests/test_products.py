from app import create_app
from .conftest import create_user, create_store, login_user, create_temp_csv_file, create_temp_xlsx_file, create_temp_ods_file
from werkzeug.datastructures import FileStorage
import json
import os


def test_get_most_sold_products():
    app = create_app()
    client = app.test_client()

    user, token = login_user()
    store = create_store(token, users=[user['id']])

    # Create a temporary CSV file with some example products content
    products_temp_file = create_temp_csv_file(
        columns="name,description,category,price,stock",
        content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200\nProduct3,Description3,Category3,30.0,300\nProduct4,Description4,Category4,40.0,400\nProduct5,Description5,Category5,50.0,500\nProduct6,Description6,Category6,60.0,600\nProduct7,Description7,Category7,70.0,700\nProduct8,Description8,Category8,80.0,800\nProduct9,Description9,Category9,90.0,900\nProduct10,Description10,Category10,100.0,1000"
    )

    products_file = FileStorage(
        stream=open(products_temp_file, 'rb'),
        filename='products.csv',
        name='file',
        content_type='text/csv'
    )

    # Create a temporary CSV file with some example sales content
    sales_temp_file = create_temp_csv_file(
        columns="product_name,quantity,total,date",
        content="Product1,9,10.0,02/02/2020\nProduct1,2,10.0,01/01/2020\nProduct2,12,10.0,01/01/2020"
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
                'quantity_column': 'quantity',
                'total_column': 'total',
                'date_column': 'date',
            },
        )

    os.remove(products_temp_file)  # Remove the temporary file
    os.remove(sales_temp_file)  # Remove the temporary file

    response = client.get('/product/most_sold', headers={
        "Authorization": "Bearer "+token
    }, query_string={
        "store_id": store['id'],
        "start_date": "2020-01-01",
        "end_date": "2020-03-03",
        "limit": 5
    })

    data = json.loads(response.data)

    assert response.status_code == 200

    assert len(data["products"]) == 2

    assert data["products"][0]["product"]["name"] == "Product2"
    assert data["products"][0]["sales"][0]['month'] == 1
    assert data["products"][0]["sales"][0]['quantity'] == 12


def test_get_most_sold_categories():
    app = create_app()
    client = app.test_client()

    user, token = login_user()
    store = create_store(token, users=[user['id']])

    # Create a temporary CSV file with some example products content
    products_temp_file = create_temp_csv_file(
        columns="name,description,category,price,stock",
        content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200\nProduct3,Description2,Category1,30.0,300\nProduct4,Description4,Category1,40.0,400\nProduct5,Description5,Category1,50.0,500\nProduct6,Description6,Category2,60.0,600\nProduct7,Description7,Category7,70.0,700\nProduct8,Description8,Category8,80.0,800\nProduct9,Description9,Category9,90.0,900\nProduct10,Description10,Category10,100.0,1000"
    )

    products_file = FileStorage(
        stream=open(products_temp_file, 'rb'),
        filename='products.csv',
        name='file',
        content_type='text/csv'
    )

    # Create a temporary CSV file with some example sales content
    sales_temp_file = create_temp_csv_file(
        columns="product_name,quantity,total,date",
        content="Product1,9,10.0,02/02/2020\nProduct1,2,10.0,01/01/2020\nProduct2,12,10.0,01/01/2020"
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
                'quantity_column': 'quantity',
                'total_column': 'total',
                'date_column': 'date',
            },
        )

    os.remove(products_temp_file)  # Remove the temporary file
    os.remove(sales_temp_file)  # Remove the temporary file

    response = client.get('/product/most_sold_categories', headers={
        "Authorization": "Bearer "+token
    }, query_string={
        "store_id": store['id'],
        "start_date": "2020-01-01",
        "end_date": "2020-03-03",
        "limit": 5
    })

    data = json.loads(response.data)

    assert response.status_code == 200

    assert len(data["categories"]) == 2

    assert data["categories"][0]["category"] == "Category2"

    assert data["categories"][0]["sales"][0]['month'] == 1
    assert data["categories"][0]["sales"][0]['quantity'] == 12

    assert data["categories"][1]["category"] == "Category1"

    assert data["categories"][1]["sales"][0]['month'] == 1
    assert data["categories"][1]["sales"][0]['quantity'] == 2

    assert data["categories"][1]["sales"][1]['month'] == 2
    assert data["categories"][1]["sales"][1]['quantity'] == 9
