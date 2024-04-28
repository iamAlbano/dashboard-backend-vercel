from flask import request, jsonify
from src.services.auth_service import AuthService
from flask_jwt_extended import create_access_token
from src.models.user import User
import json


class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def validate_request(self, request):
        try:
            data = request.get_json()

            for field in ['email', 'password']:
                if field not in data:
                    return False, "Missing "+field+" field"

            email = data['email']
            password = data['password']

            return True, "Valid request"
        except:
            return False, "Missing data"

    def login(self):
        data = request.get_json()

        valid, message = self.validate_request(request)
        if not valid:
            return jsonify({"message": "Invalid email or password"}), 400

        email = data['email']
        password = data['password']

        user, message = self.auth_service.login(
            email, password
        )

        if not user:
            return jsonify({"message": "Invalid email or password"}), 400

        user = json.loads(json.dumps(user, default=str))

        return jsonify({
            "user": user,
            "token": create_access_token(identity=user['id']),
            "message": message
        }), 200
