from datetime import datetime


class Product:
    PUBLIC_FILLABLE = [
        "store_id",
        "name",
        "category",
        "description",
        "price",
        "stock",
        "legacy_id",
    ]

    def __init__(
        self,
        store_id: str,
        name: str,
        description: str or None,
        category: str or None,
        price: str or float or None,
        purchase_price: str or float or None,
        stock: str or int or None,
        legacy_id: str or None = None,
    ):
        self.store_id = store_id
        self.name = name
        self.description = description
        self.category = category
        self.price = str(price)
        self.purchase_price = str(purchase_price)
        self.stock = str(stock)
        self.legacy_id = legacy_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "legacy_id": self.legacy_id,
            "store_id": self.store_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "purchase_price": self.purchase_price,
            "stock": self.stock,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
