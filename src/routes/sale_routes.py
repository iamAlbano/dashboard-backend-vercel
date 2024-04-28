from flask import Blueprint, request, jsonify
from src.controllers.sale_controller import SaleController

sale_routes = Blueprint('sale_routes', __name__)
sale_controller = SaleController()

# All routes automatically have the prefix /sale


@sale_routes.route('/resume', methods=['GET'])
def get_sales_resume():
    return sale_controller.get_sales_resume()


@sale_routes.route('get', methods=['GET'])
def get_sales():
    return sale_controller.get_sales()


@sale_routes.route('get_by_period', methods=['GET'])
def get_sales_by_period():
    return sale_controller.get_sales_by_period()


@sale_routes.route('get_top_products_sold_together', methods=['GET'])
def get_top_products_sold_together():
    return sale_controller.get_top_products_sold_together()
