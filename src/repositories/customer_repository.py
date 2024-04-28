from src.db.conn import db
from src.models.customer import Customer
import json


class CustomerRepository:
    def __init__(self):
        self.db = db
        self.collection = db.customers

    def create(self, customer: Customer):
        customer_dict = customer.to_dict()
        res = self.collection.insert_one(customer_dict)
        customer_dict['id'] = str(res.inserted_id)
        del customer_dict['_id']
        return customer_dict

    def get_all_customers(self, store_id):
        customers = self.collection.find({'store_id': store_id})
        customers_list = []
        for customer in customers:
            customer['id'] = str(customer['_id'])
            del customer['_id']
            customers_list.append(customer)
        return customers_list

    def find_by_id(self, customer_id):
        try:
            # Tentar criar um ObjectId a partir da string
            object_id = ObjectId(customer_id)
        except Exception as e:
            object_id = customer_id

        customer = self.collection.find_one({'_id': object_id})

        if customer:
            customer['id'] = str(customer['_id'])
            del customer['_id']
            return customer
        return None

    def find_by_column(self, column, value):
        customer = self.collection.find_one({column: value})
        if customer:
            customer['id'] = str(customer['_id'])
            del customer['_id']
            return customer
        return None

    def update(self, customer_id, customer: Customer):
        customer_dict = customer.to_dict()
        res = self.collection.update_one(
            {'_id': ObjectId(customer_id)}, {'$set': customer_dict})
        if res.modified_count > 0:
            customer_dict['id'] = customer_id
            return customer_dict
        return None

    def delete(self, customer_id):
        res = self.collection.delete_one({'_id': ObjectId(customer_id)})
        return res.deleted_count > 0

    def get_total_customers(self, store_id, search=None):
        try:
            pipeline = [
                {'$match': {'store_id': store_id}},
                {'$count': 'total'}
            ]

            if search:
                pipeline[0]['$match']['$or'] = [
                    {'name': {'$regex': search, '$options': 'i'}},
                    {'email': {'$regex': search, '$options': 'i'}}
                ]

            res = list(self.collection.aggregate(pipeline))

            if res:
                return res[0]['total']

            return 0
        except Exception as e:
            return 0

    def get_customers(self, store_id, search, page, page_size):
        if page < 1:
            page = 1

        skip = (page - 1) * page_size
        pipeline = [
            {'$match': {'store_id': store_id}},
            {
                '$project': {
                    '_id': 0,
                    'id': {'$toString': '$_id'},
                    'name': 1,
                    'email': 1,
                    'phone': 1,
                    'address': 1,
                    'city': 1,
                    'state': 1,
                    'country': 1,
                    'zipcode': 1,

                }
            }
        ]

        if search:
            pipeline.append(
                {'$match': {'$or': [
                    {'name': {'$regex': search, '$options': 'i'}},
                    {'email': {'$regex': search, '$options': 'i'}},
                ]}}
            )

        pipeline.append({'$skip': skip})

        pipeline.append({'$limit': page_size})

        return list(self.collection.aggregate(pipeline))

    def get_customers_states(self, store_id):
        pipeline = [
            {
                '$match': {
                    'store_id': store_id
                }
            },
            {
                '$group': {
                    '_id': '$state',
                    'state': {
                        '$first': '$state'
                    },
                    'total': {
                        '$sum': 1
                    }
                }
            }
        ]

        return list(self.collection.aggregate(pipeline))
