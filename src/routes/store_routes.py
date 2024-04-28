from flask import Blueprint, request, jsonify
from src.controllers.store_controller import StoreController
from flask_jwt_extended import jwt_required

store_routes = Blueprint('store_routes', __name__)
store_controller = StoreController()

# All routes automatically have the prefix /store


@store_routes.route('/create', methods=['POST'])
@jwt_required()
def create_store():
    return store_controller.create()


@store_routes.route('/get', methods=['GET'])
@jwt_required()
def get_user_stores():
    return store_controller.get_user_stores()
