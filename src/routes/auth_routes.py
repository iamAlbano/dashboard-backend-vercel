from flask import Blueprint, request, jsonify
from src.controllers.auth_controller import AuthController

auth_routes = Blueprint('auth_routes', __name__)
auth_controller = AuthController()
# All routes automatically have the prefix /auth


@auth_routes.route('/login', methods=['POST'])
def login_user():
    return auth_controller.login()
