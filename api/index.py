from flask import Flask, jsonify
from flask_cors import CORS
from src.routes import all_routes
from flask_jwt_extended import JWTManager, jwt_required
from datetime import timedelta
import os

app = Flask(__name__)

# Configuração da chave secreta para assinatura do token
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Configuração do tempo de expiração do token
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Inicializa o CORS
CORS(app)

# Registrar todas as rotas
app.register_blueprint(all_routes)

jwt = JWTManager(app)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/jwt')
@jwt_required()
def protected():
    return jsonify(message='Hello World from a protected route!')