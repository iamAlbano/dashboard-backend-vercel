from src.db.conn import db
from src.models.product import Product
import json
from bson import ObjectId


class ProductRepository:
    def __init__(self):
        self.db = db
        self.collection = db.products
        self.sales = db.sales

    def create(self, product: Product):
        product_dict = product.to_dict()
        res = self.collection.insert_one(product_dict)
        product_dict['id'] = str(res.inserted_id)
        del product_dict['_id']
        return product_dict

    def find_by_id(self, product_id):
        try:
            # Tentar criar um ObjectId a partir da string
            object_id = ObjectId(product_id)
        except Exception as e:
            object_id = product_id

        # Se não houver exceção, continuar com a busca no MongoDB
        product = self.collection.find_one({'_id': object_id})

        if product:
            product['id'] = str(product['_id'])
            del product['_id']
            return product

        return None

    def find_by_column(self, column, value):
        product = self.collection.find_one({column: value})
        if product:
            product['id'] = str(product['_id'])
            del product['_id']
            return product
        return None

    def search_by_name(self, store_id, name):
        products = self.collection.find(
            {'store_id': store_id, 'name': {'$regex': name, '$options': 'i'}})

        return list(products)

    def get_products(self, store_id, page=1, page_size=10, product_name=None, categories=None, order_by=None, order_direction=None):
        if page < 1:
            page = 1

        skip = (page - 1) * page_size
        pipeline = [
            {'$match': {'store_id': store_id}}
        ]

        if product_name:
            pipeline.append(
                {'$match': {'name': {'$regex': product_name, '$options': 'i'}}})

        if categories:
            pipeline.append(
                {'$match': {'category': {'$in': categories}}})

        # if order_by and order_direction:
        #     pipeline.append(
        #         {'$sort': {[order_by]: 1 if order_direction == 'asc' else -1}})

        pipeline.append({'$skip': skip})

        pipeline.append({'$limit': page_size})

        products = self.collection.aggregate(pipeline)

        paginated_products = []
        for product in products:
            product['id'] = str(product['_id'])

            total_sold = self.sales.aggregate([
                {'$match': {'product_id': product['id']}},
                {'$group': {'_id': None, 'total': {'$sum': '$quantity'}}}
            ])

            sum_total = next(total_sold, None)

            product['total_sold'] = sum_total.get(
                'total', 0) if sum_total else 0
            del product['_id']
            paginated_products.append(product)

        return paginated_products

    def get_total_products(self, store_id, product_name=None, categories=None):
        pipeline = [
            {'$match': {'store_id': store_id}}
        ]

        if product_name:
            pipeline.append(
                {'$match': {'name': {'$regex': product_name, '$options': 'i'}}})

        if categories:
            pipeline.append({
                '$match': {'category': {'$in': categories}}})

        pipeline.append({'$count': 'total'})
        total_products = self.collection.aggregate(pipeline)

        total_products = list(total_products)

        return total_products[0]['total'] if len(total_products) > 0 else 0

    def get_total_categories(self, store_id):
        return len(self.collection.distinct('category', {'store_id': store_id}))

    def get_average_products_price(self, store_id):
        avg_price = self.collection.aggregate([
            # Filtra documentos com 'price' não vazios e do tipo double
            {'$match': {'store_id': store_id, 'price': {
                '$ne': ''}}},
            # Converte 'price' para float
            {'$project': {'price': {'$toDouble': '$price'}}},
            {'$group': {'_id': None, 'avg_price': {'$avg': '$price'}}}
        ])

        avg_price = list(avg_price)

        return avg_price[0]['avg_price'] if len(avg_price) > 0 else 0

    def get_categories(self, store_id):
        return self.collection.distinct('category', {'store_id': store_id})

    def get_total_products_by_category(self, store_id):
        pipeline = [
            {'$match': {'store_id': store_id}},
            {'$group': {'_id': '$category', 'total': {'$sum': 1}}}
        ]

        products_by_category = self.collection.aggregate(pipeline)

        return list(products_by_category)
