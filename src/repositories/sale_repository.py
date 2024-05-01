from src.db.conn import db
from src.models.product import Product
from src.models.sale import Sale
import pandas as pd
import json
from bson.son import SON
from datetime import datetime
from bson.son import SON


class SaleRepository:
    def __init__(self):
        self.db = db
        self.collection = db.sales

    def create(self, sale: Sale):
        sale_dict = sale.to_dict()
        res = self.collection.insert_one(sale_dict)
        sale_dict['id'] = str(res.inserted_id)
        return sale_dict

    def get_total_sellings(self, store_id, start_date, end_date):
        try:
            if not start_date:
                start_date = datetime.min
            else:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')

            if not end_date:
                end_date = datetime.max
            else:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

            data = self.collection.aggregate([
                {
                    "$match": {
                        "store_id": store_id,
                        "date": {
                            "$gte": start_date,
                            "$lte": end_date
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "year": {"$year": "$date"},
                            "month": {"$month": "$date"}
                        },
                        "total": {"$sum": "$quantity"},
                    }
                },
                {
                    "$sort": SON([("_id.year", 1), ("_id.month", 1)])
                },
                {
                    "$limit": 10000
                }
            ], allowDiskUse=True)
            return list(data)
        except:
            return []

    def get_top_selling_products(self, store_id, start_date, end_date, limit=5, product_ids=[]):
        try:
            if not start_date:
                start_date = datetime.min
            else:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')

            if not end_date:
                end_date = datetime.max
            else:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

            pipeline = [
                {
                    "$match": {
                        "store_id": store_id,
                        "date": {
                            "$gte": start_date,
                            "$lte": end_date
                        },
                    }
                },
                {
                    "$group": {
                        "_id": "$product_id",
                        "sales": {"$push": "$$ROOT"},
                        "total": {"$sum": "$quantity"},
                    }
                },
                {
                    "$sort": SON([("total", -1)])
                },
                {
                    "$limit": limit
                }
            ]

            if product_ids and len(product_ids) > 0:
                pipeline[0]["$match"]["product_id"] = {"$in": product_ids}

            data = self.collection.aggregate(pipeline, allowDiskUse=True)

            return list(data)
        except:
            return []

    def get_quantity_sold_in_month(self, store_id, year, month):
        start_date = datetime(year, month, 1)
        end_date = datetime(
            year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)

        data = self.collection.aggregate([
            {
                "$match": {
                    "store_id": store_id,
                    "date": {
                        "$gte": start_date,
                        "$lt": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_quantity": {"$sum": {"$ifNull": ["$quantity", 0]}}
                }
            }
        ])

        result = list(data)
        if result:
            return result[0]['total_quantity']
        else:
            return 0

    def calculate_total_sales_value(self, store_id, year, month):
        start_date = datetime(year, month, 1)
        end_date = datetime(
            year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)

        pipeline = [
            {"$match": {
                "store_id": store_id,
                "date": {
                    "$gte": start_date,
                    "$lt": end_date}
            }
            },
            {"$group": {"_id": None, "total_sales": {"$sum": "$price"}}}
        ]

        result = list(self.collection.aggregate(pipeline))

        if result:
            total_sales = result[0]["total_sales"]
            return total_sales
        else:
            return 0

    def get_total_buyers_this_month(self, store_id):
        today = datetime.now()
        start_date = datetime(today.year, today.month, 1)
        end_date = datetime(
            today.year, today.month + 1, 1) if today.month < 12 else datetime(today.year + 1, 1, 1)

        pipeline = [
            {"$match": {
                "store_id": store_id,
                "date": {
                    "$gte": start_date,
                    "$lt": end_date}
            }
            },
            {"$group": {"_id": "$customer_id"}}
        ]

        result = list(self.collection.aggregate(pipeline))
        return len(result)

    def get_all_sales(self, store_id):
        return self.collection.find({"store_id": store_id})

    def get_sales_by_states(self, store_id):
        pipeline = [
            {
                '$match': {
                    'store_id': store_id
                }
            },
            {
                '$lookup': {
                    'from': 'customers',
                    'localField': 'customer_id',
                    'foreignField': '_id',
                    'as': 'customer'
                }
            },
            {
                '$unwind': {
                    'path': '$customer'
                }
            },
            {
                '$group': {
                    '_id': '$customer.state',
                    'state': {
                        '$first': '$customer.state'
                    },
                    'total': {
                        '$sum': 1
                    }
                }
            }
        ]

        return list(self.collection.aggregate(pipeline, allowDiskUse=True))

    def get_total_sales(self, store_id):
        pipeline = [
            {"$match": {"store_id": store_id}},
            {
                "$group": {
                    "_id": {
                        "date": "$date",
                        "customer_id": "$customer_id",
                    },
                }
            },
        ]
        result = self.collection.aggregate(pipeline)

        return len(list(result))

    def get_total_sales_price(self, store_id):
        pipeline = [
            {
                '$match': {
                    'store_id': store_id,
                }
            },
            {'$project': {
                'price': {'$toDouble': '$price'},
            }},
            {
                '$group': {
                    '_id': None,
                    "total_price": {"$sum": {"$ifNull": ["$price", 0]}},
                }
            }
        ]
        data = list(self.collection.aggregate(pipeline, allowDiskUse=True))

        return data[0]['total_price'] if data else 0

    def get_month_average(self, store_id, start_date=None, end_date=None):
        try:
            if not start_date:
                start_date = datetime.min
            else:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')

            if not end_date:
                end_date = datetime.max
            else:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

            pipeline = [
                {
                    "$match": {
                        "store_id": store_id,
                        "date": {
                            "$gte": start_date,
                            "$lte": end_date
                        }
                    }
                },
                {
                    "$project": {
                        "price": {"$toDouble": "$price"},
                        "quantity": {"$toDouble": "$quantity"},
                        "month": {"$month": "$date"},
                    }
                },
                {
                    "$group": {
                        "_id": "$month",
                        "total": {
                            "$sum": {"$multiply": ["$price", "$quantity"]}
                        },
                        "quantity": {"$sum": "$quantity"},
                        "month": {"$first": "$month"}
                    }
                }
            ]

            data = self.collection.aggregate(pipeline, allowDiskUse=True)

            total = 0
            months = 0
            for item in data:
                total += item['total']
                months += 1

            if months > 0:
                return total / months

            return 0
        except:
            return 0

    def get_total_sold_this_month(self, store_id):
        today = datetime.now()
        start_date = datetime(today.year, today.month, 1)
        end_date = datetime(
            today.year, today.month + 1, 1) if today.month < 12 else datetime(today.year + 1, 1, 1)

        pipeline = [
            {"$match": {
                "store_id": store_id,
                "date": {
                    "$gte": start_date,
                    "$lt": end_date}
            }
            },
            {"$group": {"_id": None, "total_sold": {"$sum": "$quantity"}}}
        ]

        result = list(self.collection.aggregate(pipeline))

        if result:
            return result[0]["total_sold"]
        else:
            return 0

    def get_total_sales_quantity(self, store_id):
        pipeline = [
            {
                '$match': {
                    'store_id': store_id,
                }
            },
            {
                '$group': {
                    '_id': None,
                    "total_quantity": {"$sum": {"$ifNull": ["$quantity", 0]}}
                }
            }
        ]
        data = list(self.collection.aggregate(pipeline, allowDiskUse=True))

        return data[0]['total_quantity'] if data else 0

    def get_sales(self, store_id, page=1, page_size=30, start_date=None, end_date=None):
        if page < 1:
            page = 1

        if not start_date:
            start_date = datetime.min
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

        if not end_date:
            end_date = datetime.max
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        skip = (page - 1) * page_size

        pipeline = [
            {
                "$match": {
                    "store_id": store_id,
                    "date": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "date": "$date",
                        "customer_id": "$customer_id",
                        "seller_id": "$seller_id",
                        "date": "$date",
                    },
                    "sales": {"$push": "$$ROOT"},
                    "product_ids": {"$addToSet": "$product_id"},
                    "products": {"$addToSet": "$product"},
                    "customer_id": {"$first": "$customer_id"},
                    "date": {"$first": "$date"},
                    "seller_id": {"$first": "$seller_id"},
                    "status": {"$first": "$status"},
                    "quantity": {"$sum": {"$ifNull": ["$quantity", 0]}},
                    "total": {
                        "$sum": {"$multiply": [
                            {"$ifNull": [{'$toDouble': '$price'}, 1]},
                            {"$ifNull": [{'$toDouble': '$quantity'}, 1]}
                        ]
                        }
                    },
                }
            },
            {"$sort": {"total": -1}},
            {"$skip": skip},
            {"$limit": page_size}
        ]

        sales = self.collection.aggregate(pipeline)

        return list(sales)

    def get_sales_by_period(self, store_id, start_date, end_date, limit=5, product_ids=None, categories=None):
        try:
            if not start_date:
                start_date = datetime.min
            else:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')

            if not end_date:
                end_date = datetime.max
            else:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

            pipeline = [
                {
                    "$match": {
                        "store_id": store_id,
                        "date": {
                            "$gte": start_date,
                            "$lte": end_date
                        }
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "sales": {"$push": "$$ROOT"},
                        "products": {"$addToSet": "$product_id"},
                        "total": {"$sum": "$quantity"},
                    }
                },
                {
                    "$sort": SON([("total", -1)])
                },
                {
                    "$limit": limit
                }
            ]

            if product_ids and len(product_ids) > 0:
                pipeline[0]["$match"]["product_id"] = {"$in": product_ids}

            data = self.collection.aggregate(pipeline, allowDiskUse=True)

            return list(data)
        except:
            return []

    def get_top_products_sold_together(self, store_id):
        pipeline = [
            {
                "$match": {
                    "store_id": store_id
                }
            },
            {
                "$group": {
                    "_id": {
                        "customer_id": "$customer_id",
                        "date": "$date"
                    },
                    "products": {"$addToSet": "$product_id"},
                    "customer_id": {"$first": "$customer_id"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            },
            {
                "$limit": 20
            }
        ]

        result = self.collection.aggregate(pipeline, allowDiskUse=True)

        return list(result)

    def get_most_profitable_products(self, store_id, product_ids, start_date, end_date, limit=5):

        if not start_date:
            start_date = datetime.min
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

        if not end_date:
            end_date = datetime.max
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        pipeline = [
            {
                "$match": {
                    "store_id": store_id,
                    "date": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "$toObjectId": "$product_id"
                    },
                    "product_id": {"$first": "$product_id"},
                    "quantity_sold": {"$sum": {"$ifNull": [{'$toDouble': '$quantity'}, 1]}},
                    "total_sold": {"$sum": {"$multiply": [
                        {"$ifNull": [{'$toDouble': '$price'}, 1]},
                        {"$ifNull": [{'$toDouble': '$quantity'}, 1]}
                    ]}},
                }
            },
            {
                "$lookup": {
                    "from": "products",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "product"
                }
            },
            {
                "$unwind": {
                    "path": "$product"
                }
            },
            {
                "$sort": {"total_sold": -1}
            },
            {
                "$limit": limit
            },
            {
                "$project": {
                    "id": {"$toString": "$_id"},
                    "product_id": "$product_id",
                    "quantity_sold": 1,
                    "total_sold": 1,
                    "date": 1,
                    "name": "$product.name",
                    "category": "$product.category",
                    "price": {'$ifNull': ['$product.price', 0]},
                    "purchase_price": {"$ifNull": ["$product.purchase_price", 0]},
                    "stock": {'$ifNull': ['$product.stock', 0]},
                    "total_bought": {
                        "$multiply": [
                            {"$ifNull": [{'$toDouble': '$purchase_price'}, 0]},
                            {"$ifNull": ['$quantity_sold', 0]}
                        ]
                    },
                }
            },
        ]

        if product_ids and len(product_ids) > 0:
            pipeline[0]["$match"]["product_id"] = {"$in": product_ids}

        result = db.sales.aggregate(pipeline)

        return list(result)
