from src.repositories.product_repository import ProductRepository
from src.services.sale_service import SaleService
from src.models.product import Product
import pandas as pd
from datetime import datetime


class ProductService:

    def __init__(self):
        self.product_repository = ProductRepository()
        self.sale_service = SaleService()

    def create(self, product: Product):
        valid, message = self.valid_product(product)
        if not valid:
            return False, message

        return self.product_repository.create(product), "Product created successfully"

    def find_by_id(self, product_id):
        return self.product_repository.find_by_id(product_id)

    def find_by_column(self, column, value):
        return self.product_repository.find_by_column(column, value)

    def get_products(self, store_id, page=1, page_size=10, product_name=None, categories=None, order_by=None, order_direction=None):
        return self.product_repository.get_products(store_id, page, page_size, product_name, categories, order_by, order_direction)

    def valid_product(self, product: Product):
        if not product.store_id or type(product.store_id) != str:
            return False, "Missing store_id field"

        if not product.name or type(product.name) != str:
            return False, "Missing name field"

        return True, "Product is valid"

    def search_by_name(self, store_id, name):
        products = self.product_repository.search_by_name(store_id, name)

        products = list(map(lambda product: {
            "id": str(product['_id']),
            "name": product['name'],
            "price": product['price'],
            "category": product['category']
        }, products))

        return products

    def get_products_resume(self, store_id):
        avg_price = self.product_repository.get_average_products_price(
            store_id)
        total_products = self.product_repository.get_total_products(store_id)
        total_categories = self.product_repository.get_total_categories(
            store_id)

        current_date = datetime.utcnow()
        current_year = current_date.year
        current_month = current_date.month

        total_sold = self.sale_service.get_quantity_sold_in_month(
            store_id, current_year, current_month)

        return {
            "total_products": total_products,
            "total_categories": total_categories,
            "avg_price": avg_price,
            "total_sold": total_sold
        }

    def get_total_products(self, store_id, product_name=None, categories=None):
        return self.product_repository.get_total_products(store_id, product_name, categories)

    def get_most_sold_products_by_period(self, store_id, start_date, end_date, period_group='month', limit=5, product_ids=[], categories=[]):
        top_products = self.sale_service.get_top_selling_products(
            store_id, start_date, end_date, limit, product_ids)

        data = []
        for product in top_products:
            product['product'] = self.product_repository.find_by_id(
                product['_id'])

            if categories and categories != []:
                if product['product']['category'] not in categories:
                    continue

            sellingData = []
            df = pd.DataFrame(product['sales'])
            df['date'] = pd.to_datetime(df['date'])

            if period_group == 'month':
                df['month'] = df['date'].dt.month

                sellingData = df.groupby('month').agg(
                    {'quantity': 'sum'}).reset_index()

            elif period_group == 'day':
                df['day'] = df['date'].dt.day

                sellingData = df.groupby('day').agg(
                    {'quantity': 'sum'}).reset_index()

            elif period_group == 'year':
                df['year'] = df['date'].dt.year

                sellingData = df.groupby('year').agg(
                    {'quantity': 'sum'}).reset_index()

            data.append({
                "sales": sellingData.to_dict('records'),
                "product": product['product'],
                "total": product['total']
            })

        return data

    def get_top_selling_categories(self, store_id, categories=[], start_date=None, end_date=None, period_group='month', limit=5):

        if not start_date:
            start_date = datetime(2023, 1, 1)

        if not end_date:
            end_date = datetime(2023, 12, 31)

        top_products = self.get_most_sold_products_by_period(
            store_id=store_id,
            start_date=start_date,
            end_date=end_date,
            period_group='month',
            limit=9999,
            product_ids=[],
            categories=categories
        )

        if not top_products:
            return []

        # Criar um DataFrame a partir dos dados
        df = pd.DataFrame(top_products)

        # Adicionar colunas 'category' e 'month' com base na categoria e mês do produto
        df['category'] = df['product'].apply(lambda x: x['category'])
        df['month'] = df['sales'].apply(lambda x: x[0]['month'])

        # Agrupar e somar os dados
        result = df.groupby(['category']).agg(
            {'sales': 'sum',
             'total': 'sum'}).reset_index()

        result = result.sort_values(by='total', ascending=False).head(
            limit).to_dict('records')

        return result

    def get_most_profitable_products(self):
        data = self.sale_service.get_most_profitable_products()

        return []

    def get_categories(self, store_id):
        return self.product_repository.get_categories(store_id)

    def get_total_products_by_category(self, store_id):
        return self.product_repository.get_total_products_by_category(store_id)
