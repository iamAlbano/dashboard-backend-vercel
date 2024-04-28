from flask import Blueprint, request, jsonify
from src.controllers.customer_controller import CustomerController

customer_routes = Blueprint('customer_routes', __name__)
customer_controller = CustomerController()


# All routes automatically have the prefix /customer

@customer_routes.route('/get', methods=['GET'])
def get_customers():
    return customer_controller.get_customers()


@customer_routes.route('/states', methods=['GET'])
def get_customers_states():
    return customer_controller.get_customers_states()


@customer_routes.route('/resume', methods=['GET'])
def get_customers_resume():
    return customer_controller.get_customers_resume()
