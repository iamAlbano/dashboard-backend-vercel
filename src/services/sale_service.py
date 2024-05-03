from src.repositories.sale_repository import SaleRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.customer_repository import CustomerRepository
from src.models.sale import Sale
import pandas as pd


class SaleService:
    def __init__(self):
        self.sale_repository = SaleRepository()
        self.product_repository = ProductRepository()
        self.customer_repository = CustomerRepository()

    def create(
        self,
        store_id: str,
        product_id: str,
        product: dict or None,
        quantity: str or int or float or None,
        price: str or float or None,
        seller_id: str or None,
        customer_id: str or None,
        status: str or None,
        date: str or None
    ):
        valid, message = self.valid_sale(
            store_id,
            product_id,
            quantity,
            price,
            seller_id,
            customer_id,
            status,
            date
        )

        if not valid:
            return False, message

        sale = Sale(
            store_id,
            product_id,
            product,
            quantity,
            price,
            seller_id,
            customer_id,
            status,
            date
        )
        return self.sale_repository.create(sale), "Sale created successfully"

    def valid_sale(
        self,
        store_id: str,
        product_id: str,
        quantity: str or int or float or None,
        price: str or float or None,
        seller_id: str or None,
        customer_id: str or None,
        status: str or None,
        date: str or None
    ):
        if not store_id or type(store_id) != str:
            return False, "Missing store_id field"

        if not product_id:
            return False, "Missing product_id field"

        return True, "Sale is valid"

    def get_total_sellings(self, store_id, start_date, end_date):
        return self.sale_repository.get_total_sellings(
            store_id, start_date, end_date)

    def get_top_selling_products(self, store_id, start_date, end_date, limit=5, product_ids=[]):
        return self.sale_repository.get_top_selling_products(
            store_id, start_date, end_date, limit, product_ids)

    def get_top_selling_categories(self, store_id, start_date, end_date, limit=5):
        return self.sale_repository.get_top_selling_categories(
            store_id, start_date, end_date, limit)

    def get_quantity_sold_in_month(self, store_id, year, month):
        return self.sale_repository.get_quantity_sold_in_month(
            store_id, year, month)

    def get_total_buyers_this_month(self, store_id):
        return self.sale_repository.get_total_buyers_this_month(store_id)

    def get_average_customer_spent(self, store_id):
        sales = self.sale_repository.get_all_sales(store_id)

        # Criar um DataFrame do Pandas com os dados
        df = pd.DataFrame(list(sales))

        # Converter colunas 'quantity' e 'price' para números
        df['quantity'] = pd.to_numeric(
            df['quantity']) if 'quantity' in df else 0
        df['price'] = pd.to_numeric(df['price']) if 'price' in df else 0

        # Calcular o valor total (quantity * price) para cada registro
        df['total_value'] = df['quantity'] * df['price']

        # Calcular a média do valor total
        average = df['total_value'].mean()

        return average

    def get_sales_by_states(self, store_id):
        return self.sale_repository.get_sales_by_states(store_id)

    def get_total_sales(self, store_id):
        return self.sale_repository.get_total_sales(store_id)

    def get_sales_resume(self, store_id, start_date, end_date):
        quantity = self.sale_repository.get_total_sales_quantity(store_id)
        price = self.sale_repository.get_total_sales_price(store_id)
        month_average = self.sale_repository.get_month_average(store_id)
        sold_this_month = self.sale_repository.get_total_sold_this_month(
            store_id)

        return {
            "total_quantity": quantity,
            "total_price": price,
            "month_average": month_average,
            "sold_this_month": sold_this_month
        }

    def get_sales(self, store_id, page, page_size, start_date, end_date):
        return self.sale_repository.get_sales(
            store_id, page, page_size, start_date, end_date)

    def get_sales_by_period(self, store_id, start_date, end_date, period_group='month', limit=5, product_ids=None, categories=None):
        sales = self.sale_repository.get_sales_by_period(
            store_id, start_date, end_date, limit, product_ids, categories)

        data = []

        for product in sales:

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

            data.append(sellingData.to_dict('records'))

        return data[0] if data else []

    def get_top_products_sold_together(self, store_id):
        sales = self.sale_repository.get_top_products_sold_together(store_id)

        products = []
        customers = []

        sold_products = []

        for sale in sales:
            if not sale['customer_id']:
                continue

            client = None

            for customer in customers:
                if not customer:
                    continue

                if customer['id'] == sale['customer_id']:
                    client = customer
                    break

            if not client:
                client = self.customer_repository.find_by_id(
                    sale['customer_id'])

                customers.append(client)

            sale_products = []

            for sale_product_id in sale['products']:

                sold_product = None

                for product in products:
                    if product['id'] == sale_product_id:
                        sold_product = product
                        break

                if not sold_product:
                    sold_product = self.product_repository.find_by_id(
                        sale_product_id)

                    products.append(sold_product)

                sale_products.append(sold_product)

            sold_products.append({
                'customer': client,
                'products': sale_products,
                'count': sale['count']
            })

        return sold_products

    def get_most_profitable_products(
        self,
        store_id,
        product_ids,
        start_date,
        end_date,
        limit=5
    ):
        return self.sale_repository.get_most_profitable_products(
            store_id, product_ids, start_date, end_date, limit)
