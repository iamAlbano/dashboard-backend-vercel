from flask import request, jsonify
from src.services.user_service import UserService
from src.models.user import User
import json


class UserController:
    def __init__(self):
        self.user_service = UserService()

    def validate_request(self, request):
        try:
            data = request.get_json()

            for field in User.PUBLIC_FILLABLE:
                if field not in data:
                    return False, "Missing "+field+" field"

            name = data['name']
            surname = data['surname']
            email = data['email']
            password = data['password']

            return self.user_service.valid_user(name, surname, email, password)
        except:
            return False, "Missing data"

    def create(self):
        data = request.get_json()

        valid, message = self.validate_request(request)
        if not valid:
            return jsonify({"message": message}), 400

        name = data['name']
        surname = data['surname']
        email = data['email']
        password = data['password']

        user, message = self.user_service.create(
            name, surname, email, password
        )

        if not user:
            return jsonify({"message": message}), 400

        user = json.loads(json.dumps(user, default=str))

        return jsonify({
            "user": user,
            "message": message
        }), 201
