from flask import Blueprint, request, jsonify
from src.controllers.user_controller import UserController

user_routes = Blueprint('user_routes', __name__)
user_controller = UserController()

# All routes automatically have the prefix /user


@user_routes.route('/create', methods=['POST'])
def create_user():
    return user_controller.create()
