from datetime import datetime


class Sale:
    PUBLIC_FILLABLE = [
        "store_id",
        "product_id",
        "quantity",
        "price",
        "seller_id",
        "customer_id",
        "status",
        "date",
        "legacy_id"
    ]

    def __init__(
            self,
            store_id: str,
            product_id: str,
            quantity: str or int or float or None,
            price: str or float or None,
            seller_id: str or None,
            customer_id: str or None,
            status: str or None,
            date: str or None,
            legacy_id: str or None = None,

    ):
        self.legacy_id = legacy_id
        self.store_id = store_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = str(price)
        self.seller_id = seller_id
        self.customer_id = customer_id
        self.status = status
        self.date = date
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "legacy_id": self.legacy_id,
            "store_id": self.store_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": self.price,
            "seller_id": self.seller_id,
            "customer_id": self.customer_id,
            "status": self.status,
            "date": self.date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
