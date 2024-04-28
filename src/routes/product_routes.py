from flask import Blueprint, request, jsonify
from src.controllers.product_controller import ProductController

product_routes = Blueprint('product_routes', __name__)
product_controller = ProductController()

# All routes automatically have the prefix /product


@product_routes.route('/get', methods=['GET'])
def get_products():
    return product_controller.get_products()


@product_routes.route('/resume', methods=['GET'])
def get_product_stats():
    return product_controller.get_products_resume()


@product_routes.route('/most_sold', methods=['GET'])
def get_most_sold_products_by_period():
    return product_controller.get_most_sold_products_by_period()


@product_routes.route('/most_sold_categories', methods=['GET'])
def get_top_selling_categories():
    return product_controller.get_top_selling_categories()


@product_routes.route('/most_profitable', methods=['GET'])
def get_most_profitable_products():
    return product_controller.get_most_profitable_products()


@product_routes.route('/search', methods=['GET'])
def search_by_name():
    return product_controller.search_by_name()


@product_routes.route('/categories', methods=['GET'])
def get_categories():
    return product_controller.get_categories()


@product_routes.route('/total-by-categories', methods=['GET'])
def get_total_categories():
    return product_controller.get_total_products_by_category()
