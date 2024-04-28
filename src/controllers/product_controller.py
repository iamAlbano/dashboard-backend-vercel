from flask import request, jsonify
from src.services.product_service import ProductService
from src.services.sale_service import SaleService
from src.models.product import Product
from dateutil import parser
from bson import json_util
import json


class ProductController:
    def __init__(self):
        self.product_service = ProductService()
        self.sale_service = SaleService()

    def get_products(self):
        store_id = request.args.get('store_id', default=None, type=str)
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)
        product_name = request.args.get('search', default=None, type=str)
        categories = request.args.getlist('categories[]')
        order_by = request.args.get('order_by', default=None, type=str)
        order_direction = request.args.get(
            'order_direction', default=None, type=str)

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        products = self.product_service.get_products(
            store_id, page, page_size, product_name, categories, order_by)

        total_products = self.product_service.get_total_products(
            store_id, product_name, categories)

        total_pages = (total_products // page_size) + 1

        return jsonify({
            "products": products,
            "total_pages": total_pages,
            "total_products": total_products,
            "message": "Products retrieved successfully"
        }), 200

    def get_products_resume(self):
        store_id = request.args.get('store_id', default=None, type=str)

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        stats = self.product_service.get_products_resume(store_id)

        return jsonify({
            "stats": stats,
            "message": "Stats retrieved successfully"
        }), 200

    def get_most_sold_products_by_period(self):
        store_id = request.args.get('store_id', default=None, type=str)
        start_date = request.args.get(
            'start_date', default=None, type=str)
        end_date = request.args.get('end_date', default=None, type=str)
        limit = request.args.get('limit', default=3, type=int)
        period_group = request.args.get(
            'period_group', default='month', type=str)

        product_ids = request.args.getlist('product_ids[]')
        categories = request.args.getlist('categories[]')

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        start_date = parser.parse(
            start_date
        ).strftime("%Y-%m-%d") if start_date else None

        end_date = parser.parse(
            end_date
        ).strftime("%Y-%m-%d") if end_date else None

        products = self.product_service.get_most_sold_products_by_period(
            store_id,
            start_date,
            end_date,
            period_group,
            limit,
            product_ids,
            categories
        )

        total_sellings = self.sale_service.get_total_sellings(
            store_id,
            start_date,
            end_date,
        )

        return jsonify({
            "products": products,
            "total_sellings": total_sellings,
            "message": "Products retrieved successfully"
        }), 200

    def get_top_selling_categories(self):
        store_id = request.args.get('store_id', default=None, type=str)
        start_date = request.args.get(
            'start_date', default=None, type=str)
        end_date = request.args.get('end_date', default=None, type=str)
        limit = request.args.get('limit', default=5, type=int)
        period_group = request.args.get(
            'period_group', default='month', type=str)
        categories = request.args.getlist('categories[]')

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        start_date = parser.parse(
            start_date
        ).strftime("%Y-%m-%d") if start_date else None

        end_date = parser.parse(
            end_date
        ).strftime("%Y-%m-%d") if end_date else None

        categories = self.product_service.get_top_selling_categories(
            store_id,
            categories,
            start_date,
            end_date,
            period_group,
            limit
        )

        total_sellings = self.sale_service.get_total_sellings(
            store_id,
            start_date,
            end_date,
        )

        return jsonify({
            "categories": categories,
            "total_sellings": total_sellings,
            "message": "Categories retrieved successfully"
        }), 200

    def search_by_name(self):
        store_id = request.args.get('store_id', default=None, type=str)
        name = request.args.get('name', default=None, type=str)

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        if not name:
            return jsonify({
                "message": "Missing name field"
            }), 400

        products = self.product_service.search_by_name(store_id, name)

        return jsonify({
            "products": products,
            "message": "Products retrieved successfully"
        }), 200

    def get_most_profitable_products(self):
        store_id = request.args.get('store_id', default=None, type=str)
        productIds = request.args.getlist('product_ids[]')

        start_date = request.args.get(
            'start_date', default=None, type=str)
        end_date = request.args.get('end_date', default=None, type=str)
        limit = request.args.get('limit', default=5, type=int)

        limit = request.args.get('limit', default=5, type=int)

        start_date = parser.parse(
            start_date
        ).strftime("%Y-%m-%d") if start_date else None

        end_date = parser.parse(
            end_date
        ).strftime("%Y-%m-%d") if end_date else None

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        res = self.sale_service.get_most_profitable_products(
            store_id,
            productIds,
            start_date,
            end_date,
            limit
        )

        return jsonify({
            "products": json.loads(json_util.dumps(res)),
            "message": "Products retrieved successfully"
        }), 200

    def get_categories(self):
        store_id = request.args.get('store_id', default=None, type=str)

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        categories = self.product_service.get_categories(store_id)

        return jsonify({
            "categories": categories,
            "message": "Categories retrieved successfully"
        }), 200

    def get_total_products_by_category(self):
        store_id = request.args.get('store_id', default=None, type=str)

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        categories = self.product_service.get_total_products_by_category(
            store_id)

        return jsonify({
            "categories": categories,
            "message": "Categories retrieved successfully"
        }), 200
