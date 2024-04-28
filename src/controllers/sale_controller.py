from flask import request, jsonify
from src.services.sale_service import SaleService
from src.models.sale import Sale
from dateutil import parser
import json


class SaleController:
    def __init__(self):
        self.sale_service = SaleService()

    def get_sales_resume(self):
        store_id = request.args.get('store_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not store_id:
            return jsonify([store_id])

        resume = self.sale_service.get_sales_resume(
            store_id, start_date, end_date)

        return jsonify({
            "resume": resume,
            "message": "Resume retrieved successfully"
        }), 200

    def get_sales(self):
        store_id = request.args.get('store_id')
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)
        start_date = request.args.get(
            'start_date', default=None, type=str)
        end_date = request.args.get('end_date', default=None, type=str)

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        sales = self.sale_service.get_sales(
            store_id, page, page_size, start_date, end_date)

        total_sales = self.sale_service.get_total_sales(store_id)

        total_pages = (total_sales // page_size) + 1

        return jsonify({
            "sales": sales,
            "total_pages": total_pages,
            "total_sales": total_sales,
            "message": "Sales retrieved successfully"
        }), 200

    def get_sales_by_period(self):
        store_id = request.args.get('store_id', default=None, type=str)
        start_date = request.args.get(
            'start_date', default=None, type=str)
        end_date = request.args.get('end_date', default=None, type=str)
        limit = request.args.get('limit', default=5, type=int)
        period_group = request.args.get(
            'period_group', default='month', type=str)

        productIds = request.args.getlist('product_ids[]')
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

        sales = self.sale_service.get_sales_by_period(
            store_id,
            start_date,
            end_date,
            period_group,
            limit,
            productIds,
            categories
        )

        return jsonify({
            "sales": sales,
            "total_sellings": [],
            "message": "Sales retrieved successfully"
        }), 200

    def get_top_products_sold_together(self):
        store_id = request.args.get('store_id', default=None, type=str)

        if not store_id:
            return jsonify({
                "message": "Missing store_id field"
            }), 400

        sales = self.sale_service.get_top_products_sold_together(store_id)

        return jsonify({
            "sales": sales,
            "message": "Products retrieved successfully"
        }), 200
