from src.db.conn import db
from src.models.user import User
import json


class UserRepository:
    def __init__(self):
        self.db = db
        self.collection = db.users

    def create(self, user: User):
        user_dict = user.to_dict()
        res = self.collection.insert_one(user_dict)
        user_dict['id'] = str(res.inserted_id)
        del user_dict['_id']
        del user_dict['password']
        return user_dict

    def find(self, id: str) -> User:
        user = self.collection.find_one({'_id': id})
        user['id'] = str(user['_id'])
        user['created_at'] = str(user['created_at'])
        del user['_id']
        del user['password']
        return user

    def get(self, column: str, value: str) -> list:
        results = self.collection.find({column: value})
        found_users = []
        for result in results:
            result['id'] = str(result['_id'])
            result['created_at'] = str(result['created_at'])
            found_users.append(result)
        return found_users

    def update(self, id: str, user: str) -> User:
        user_dict = user.to_dict()
        user = self.collection.update_one({'_id': id}, {'$set': user_dict})
        return user

    def delete(self, id: str):
        return self.collection.delete_one({'_id': id})
