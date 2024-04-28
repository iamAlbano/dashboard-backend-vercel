from datetime import datetime


class Store:
    PUBLIC_FILLABLE = [
        "name",
        "users",
    ]

    def __init__(
            self,
            name: str,
            users: list
    ):
        self.name = name
        self.users = users
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "name": self.name,
            "users": self.users,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
