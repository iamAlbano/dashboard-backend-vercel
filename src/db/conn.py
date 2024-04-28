import pymongo
import os
from dotenv import load_dotenv

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()

connection_string = "mongodb+srv://albano:nD1rEoU5keyG9Uep@dashboard-tcc.bazeifu.mongodb.net/"
database_name = os.getenv("DATABASE_NAME")

if os.environ.get("FLASK_ENV") == "test":
    database_name = os.getenv("TEST_DATABASE_NAME")

# Criando uma conexão com o MongoDB Atlas
client = pymongo.MongoClient(connection_string)

# Acesse um banco de dados
db = client.get_database(database_name)
