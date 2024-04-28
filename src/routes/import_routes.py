from flask import Blueprint, request, jsonify
from src.controllers.import_controller import ImportController
from flask_jwt_extended import jwt_required
import_routes = Blueprint('import_routes', __name__)

import_controller = ImportController()

# All the routes automatically have the prefix /import


@import_routes.route('/products', methods=['POST'])
@jwt_required()
def import_products():
    return import_controller.import_products()


@import_routes.route('/sales', methods=['POST'])
@jwt_required()
def import_sales():
    return import_controller.import_sales()


@import_routes.route('/customers', methods=['POST'])
@jwt_required()
def import_customers():
    return import_controller.import_customers()
