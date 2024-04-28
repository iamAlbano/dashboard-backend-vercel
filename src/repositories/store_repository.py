from src.db.conn import db
from src.models.store import Store
import json


class StoreRepository:
    def __init__(self):
        self.db = db
        self.collection = db.stores

    def create(self, store: Store):
        store_dict = store.to_dict()
        res = self.collection.insert_one(store_dict)
        store_dict['id'] = str(res.inserted_id)
        del store_dict['_id']
        return store_dict

    def get_user_stores(self, user_id: str) -> list:
        results = self.collection.find({'users': user_id})
        found_stores = []
        for store in results:
            found_stores.append({
                'id': str(store['_id']),
                'name': store['name'],
            })
        return found_stores

    def find(self, id: str) -> Store:
        store = self.collection.find_one({'_id': id})
        store['id'] = str(store['_id'])
        del store['_id']
        return store

    def update(self, id: str, store: str) -> Store:
        store_dict = store.to_dict()
        store = self.collection.update_one({'_id': id}, {'$set': store_dict})
        return store

    def delete(self, id: str):
        return self.collection.delete_one({'_id': id})

    def add_user(self, store_id: str, user_id: str):
        store = self.find(store_id)
        store['users'].append(user_id)
        return self.update(store_id, store)
