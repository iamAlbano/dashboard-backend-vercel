from flask import request, jsonify
from src.services.store_service import StoreService
from src.models.store import Store
import json


class StoreController:
    def __init__(self):
        self.store_service = StoreService()

    def create(self):
        try:
            data = request.get_json()

            store, message = self.store_service.create(
                data['name'],
                data['users']
            )

            return jsonify({
                "store": store,
                "message": message
            }), 201

        except:
            return jsonify({"message": "Missing data"}), 400

    def get_user_stores(self):

        user_id = request.args.get('user_id')

        stores = self.store_service.get_user_stores(user_id)

        return jsonify({
            "stores": stores,
            "message": "Stores retrieved successfully"
        }), 200

    def update(self):
        try:
            data = request.get_json()

            return self.store_service.update(
                data['id'],
                data['store']
            )

        except:
            return jsonify({"message": "Missing data"}), 400

    def delete(self):
        try:
            data = request.get_json()

            return self.store_service.delete(data['id'])

        except:
            return jsonify({"message": "Missing data"}), 400

    def add_user(self):
        try:
            data = request.get_json()

            return self.store_service.add_user(
                data['store_id'],
                data['user_id']
            )

        except:
            return jsonify({"message": "Missing data"}), 400
