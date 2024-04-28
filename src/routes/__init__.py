from flask import Blueprint

# Importe as rotas relacionadas aos usuários
from .user_routes import user_routes
from .product_routes import product_routes
from .sale_routes import sale_routes
from .import_routes import import_routes
from .auth_routes import auth_routes
from .store_routes import store_routes
from .customer_routes import customer_routes

# Crie um Blueprint para agrupar as rotas
all_routes = Blueprint('all_routes', __name__)

# Adicione as rotas de usuário ao Blueprint
all_routes.register_blueprint(user_routes, url_prefix='/user')
all_routes.register_blueprint(product_routes, url_prefix='/product')
all_routes.register_blueprint(sale_routes, url_prefix='/sale')
all_routes.register_blueprint(import_routes, url_prefix='/import')
all_routes.register_blueprint(auth_routes, url_prefix='/auth')
all_routes.register_blueprint(store_routes, url_prefix='/store')
all_routes.register_blueprint(customer_routes, url_prefix='/customer')
