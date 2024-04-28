from src.repositories.store_repository import StoreRepository
from src.models.store import Store


class StoreService:
    def __init__(self):
        self.store_repository = StoreRepository()

    def create(self, name, users):
        valid, message = self.valid_store(
            name)
        if not valid:
            return False, message

        store = Store(name, users)
        return self.store_repository.create(store), "Store created successfully"

    def get_user_stores(self, user_id: str) -> list:
        return self.store_repository.get_user_stores(user_id)

    def find(self, id: str) -> Store:
        return self.store_repository.find(id)

    def update(self, id: str, store: str) -> Store:
        return self.store_repository.update(id, store)

    def delete(self, id: str):
        return self.store_repository.delete(id)

    def add_user(self, store_id: str, user_id: str):
        return self.store_repository.add_user(store_id, user_id)

    def valid_store(self, name):
        if not name:
            return False, "name is required"
        return True, None
