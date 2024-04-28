from flask import request, jsonify
from src.services.customer_service import CustomerService
from src.models.customer import Customer
from dateutil import parser
import json


class CustomerController:
    def __init__(self):
        self.customer_service = CustomerService()

    def get_customers(self):
        store_id = request.args.get('store_id', default=None, type=str)
        query = request.args.get('search', default=None, type=str)
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        customers = self.customer_service.get_customers(
            store_id, query, page, page_size)

        total_customers = self.customer_service.get_total_customers(
            store_id, query)

        total_pages = (total_customers // page_size) + 1

        return jsonify({
            "customers": customers,
            "total_pages": total_pages,
            "total_customers": total_customers,
            "message": "Customers retrieved successfully"
        }), 200

    def get_customers_states(self):
        store_id = request.args.get('store_id', default=None, type=str)

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        customers_states = self.customer_service.get_customers_states(store_id)

        return jsonify({
            "states": customers_states,
            "message": "Customers states retrieved successfully"
        }), 200

    def get_customers_resume(self):
        store_id = request.args.get('store_id', default=None, type=str)

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        customers_resume = self.customer_service.get_customers_resume(store_id)

        return jsonify({
            "stats": customers_resume,
            "message": "Customers resume retrieved successfully"
        }), 200
