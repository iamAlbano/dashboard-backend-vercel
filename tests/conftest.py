from app import create_app
from pymongo import MongoClient
from src.db.conn import client, db
from dotenv import load_dotenv
import tempfile
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from pyexcel_ods import save_data
import pandas as pd
import pytest
import os
import json

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()

env_type = os.environ.get("FLASK_ENV")

# Verifica se o ambiente é de testes


@pytest.fixture(scope="function", autouse=True)
def setup():

    if env_type != "test":
        raise Exception(
            "You can't run this function in an environment different from test")

    yield


# Executa limpeza no banco de dados depois de cada teste
@pytest.fixture(scope="function", autouse=True)
def teardown():

    yield

    if env_type != "test":
        raise Exception(
            "You can't run this function in an environment different from test")

    # Limpa o banco de dados depois de cada teste

    # Apague todas as coleções (tabelas) no banco de dados
    for collection_name in db.list_collection_names():
        db[collection_name].drop()


# create and return an user for tests that requires one
def create_user():
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
    assert response.status_code == 201
    assert "user" in data
    user = data["user"]

    assert "id" in user
    assert "name" in user
    assert "surname" in user
    assert "email" in user
    assert "created_at" in user
    assert "updated_at" in user
    assert "password" not in data["user"]

    return user


# create an user and login for tests that requires authentication
def login_user():
    app = create_app()
    client = app.test_client()

    user = create_user()

    login_data = {
        "email": "gui@gmail.com",
        "password": "12345678"
    }

    response = client.post('/auth/login', json=login_data)

    data = json.loads(response.data)

    assert data["message"] == "User logged in successfully"
    assert response.status_code == 200

    assert "user" in data

    user = data["user"]

    assert "id" in user
    assert "name" in user
    assert "surname" in user
    assert "email" in user
    assert "password" not in data["user"]
    assert "token" in data

    return user, data["token"]


def create_store(token: str, users: list = []):
    app = create_app()
    client = app.test_client()

    store_data = {
        "name": "Store1",
        "users": users,
    }

    response = client.post('/store/create', json=store_data, headers={
        "Authorization": "Bearer "+token
    })

    data = json.loads(response.data)

    assert data["message"] == "Store created successfully"
    assert response.status_code == 201
    assert "store" in data

    store = data["store"]

    assert "id" in store
    assert "name" in store
    assert "users" in store

    return store


def create_temp_csv_file(
    columns="name,description,category,price,stock",
    content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200"
):
    # Crie um arquivo CSV temporário com algum conteúdo de exemplo
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
        csv_content = columns+"\n"+content
        temp_file.write(csv_content.encode())
        temp_file_path = temp_file.name
    return temp_file_path


def create_temp_xlsx_file(
    columns="name,description,category,price,stock",
    content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200"
):
    # Criar um DataFrame a partir do conteúdo
    data = [row.split(',') for row in content.split('\n')]
    df = pd.DataFrame(data, columns=columns.split(','))

    # Criar um arquivo XLSX temporário
    temp_xlsx_path = tempfile.mktemp(suffix=".xlsx")

    # Inicializar o Workbook do openpyxl
    workbook = Workbook()
    worksheet = workbook.active

    # Adicionar cabeçalho
    header = columns.split(',')
    worksheet.append(header)

    # Adicionar linhas de dados do DataFrame
    for row in dataframe_to_rows(df, index=False, header=False):
        worksheet.append(row)

    # Salvar o arquivo XLSX
    workbook.save(temp_xlsx_path)

    return temp_xlsx_path


def create_temp_ods_file(
    columns="name,description,category,price,stock",
    content="Product1,Description1,Category1,10.0,100\nProduct2,Description2,Category2,20.0,200"
):
    # Criar um DataFrame a partir do conteúdo
    data = [row.split(',') for row in content.split('\n')]
    df = pd.DataFrame(data, columns=columns.split(','))

    # Criar um arquivo ODS temporário
    temp_ods_path = tempfile.mktemp(suffix=".ods")

    # Converter o DataFrame em um dicionário de dados
    data_dict = {"Sheet1": [df.columns.tolist()] + df.values.tolist()}

    # Salvar os dados no arquivo ODS
    save_data(temp_ods_path, data_dict)

    return temp_ods_path
