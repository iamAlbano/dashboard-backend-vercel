from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.utils.functions import is_valid_email
from werkzeug.security import check_password_hash
import json


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def login(self, email, password):
        if not email or not password:
            return False, "Missing email or password"

        if not is_valid_email(email):
            return False, "Invalid email"

        users = self.user_repository.get('email', email)

        if not users:
            return False, "User not found"

        user = users[0]

        if not user:
            return False, "User not found"

        if not check_password_hash(user['password'], password):
            return False, "Invalid password"

        del user['_id']
        del user['password']

        return user, "User logged in successfully"
