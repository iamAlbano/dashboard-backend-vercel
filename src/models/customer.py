from datetime import datetime


class Customer:
    PUBLIC_FILLABLE = [
        "store_id",
        "name",
        "email",
        "phone",
        "birthday",
        "address",
        "city",
        "state",
        "zipcode",
        "country",
        "legacy_id",
    ]

    def __init__(
        self,
        store_id: str,
        name: str or None,
        email: str or None,
        phone: str or None,
        birthday: str or None,
        address: str or None,
        city: str or None,
        state: str or None,
        zipcode: str or None,
        country: str or None,
        legacy_id: str or None = None,
    ):
        self.store_id = store_id
        self.name = name
        self.email = email
        self.phone = phone
        self.birthday = birthday
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.country = country
        self.legacy_id = legacy_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "legacy_id": self.legacy_id,
            "store_id": self.store_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "country": self.country,
            "birthday": self.birthday,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
