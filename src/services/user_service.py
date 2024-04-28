from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.utils.functions import is_valid_email
from werkzeug.security import generate_password_hash


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create(self, name, surname, email, password):

        valid, message = self.valid_user(name, surname, email, password)
        if not valid:
            return False, message

        find_by_email = self.user_repository.get('email', email)
        if find_by_email:
            return False, "Email already registered"

        user = User(name, surname, email, generate_password_hash(password))
        return self.user_repository.create(user), "User created successfully"

    def find(self, id):
        user = self.user_repository.find(id)
        if not user:
            return False, "User not found"
        return user, "User found successfully"

    def get(self, column, value):
        users = self.user_repository.get(column, value)
        return users, "Users found successfully"

    def update(self, id, user):
        valid, message = self.valid_user(name, surname, email, password)
        if not valid:
            return False, message

        users = self.user_repository.get('email', email)

        return self.user_repository.update(id, user)

    def delete(self, id):
        return self.user_repository.delete(id)

    def valid_user(self, name, surname, email, password):

        fields = {'name': name, 'surname': surname,
                  'email': email, 'password': password}

        for field in fields:
            if not fields[field]:
                return False, "Missing "+field+" field"

        for field in fields:
            if type(fields[field]) != str:
                return False, field+" must be a string"

        if len(name) < 3:
            return False, "Name must be at least 3 characters long"

        if len(surname) < 3:
            return False, "Surname must be at least 3 characters long"

        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if len(email) < 5:
            return False, "Email must be at least 5 characters long"

        if not is_valid_email(email):
            return False, "Invalid email"
        return True, "Valid"
