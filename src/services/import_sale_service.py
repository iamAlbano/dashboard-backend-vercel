from src.models.sale import Sale
import pandas as pd
from src.models.product import Product
from src.models.customer import Customer
from src.services.product_service import ProductService
from src.services.sale_service import SaleService
from src.services.customer_service import CustomerService
from dateutil import parser
from datetime import datetime


class ImportSaleService:
    def __init__(self):
        self.sale_service = SaleService()
        self.product_service = ProductService()
        self.customer_service = CustomerService()

    def validate_columns(
        self,
        product_column,
        quantity_column,
        price_column,
        seller_column,
        customer_column,
        status_column,
        date_column
    ):

        if not product_column or type(product_column) != str:
            return False, "Missing product_column field"

        return True, None

    def import_sales(
        self,
        df_sales,
        df_products: pd.DataFrame or None,
        df_customers: pd.DataFrame or None,
        store_id: str,
        product_column: str,
        quantity_column: str or None,
        price_column: str or None,
        seller_column: str or None,
        customer_column: str or None,
        status_column: str or None,
        date_column: str or None
    ):
        valid, message = self.validate_columns(
            product_column,
            quantity_column,
            price_column,
            seller_column,
            customer_column,
            status_column,
            date_column
        )

        if not valid:
            return False, message

        successful_imports = 0
        failed_imports = 0

        # loop through sales
        for index, sale in df_sales.iterrows():

            product = None
            customer = None

            # search the product in the products file if exists
            if df_products is not None:
                # loop through columns to find the product in the products file
                for column in ['id', 'legacy_id', 'name', product_column]:
                    # search the product in the products file
                    if column not in df_products.columns:
                        continue

                    found_product = df_products.loc[
                        df_products[column.lower(
                        )] == sale[product_column.lower()]
                    ]

                    # if the product is found, search if already exists in the database
                    if not found_product.empty:
                        product = self.product_service.find_by_column(
                            column, found_product.iloc[0][column.lower()]
                        )

                        if product:
                            break

                # if the product is not found, create it
                if product is None and 'name' in df_products.columns:

                    new_product = Product(
                        store_id=store_id,
                        name=found_product.iloc[0]['name'],
                        description=found_product.iloc[0]['description'] if 'description' in df_products.columns else None,
                        category=found_product.iloc[0]['category'] if 'category' in df_products.columns else None,
                        price=found_product.iloc[0]['price'] if 'price' in df_products.columns else 0,
                        purchase_price=found_product.iloc[0][
                            'purchase_price'] if 'purchase_price' in df_products.columns else 0,
                        stock=found_product.iloc[0]['stock'] if 'stock' in df_products.columns else 0,
                        legacy_id=found_product.iloc[0]['id'] if 'id' in df_products.columns else None,
                    )
                    product, message = self.product_service.create(new_product)

            # if the product is not found in the products file, search in the database
            if product is None and product_column in sale:
                # if there's no products file, search the product in the database by legacy_id
                product = self.product_service.find_by_column(
                    'legacy_id', sale[product_column].strip()
                )

                # if the product still not found by name, search for name
                if product is None:
                    product = self.product_service.find_by_column(
                        'name', sale[product_column])

                # if the product still not found by name, search for id
                if product is None:
                    product = self.product_service.find_by_id(
                        sale[product_column])

                # if the product is not found, try create it
                if product is None:

                    total_price = sale[price_column] if price_column in sale else 0

                    quantity = sale[quantity_column] if quantity_column in sale else 1

                    price = total_price / quantity

                    new_product = Product(
                        store_id=store_id,
                        name=sale[product_column],
                        description=None,
                        category=None,
                        price=price,
                        purchase_price=None,
                        stock=None,
                        legacy_id=None,
                    )
                    product, message = self.product_service.create(
                        new_product)

            # if the product is not found, skip the import
            if product is None:
                failed_imports += 1
                continue

            # search the customer in the customers file if exists
            if df_customers is not None and customer_column in sale:
                # loop through columns to find the customer in the customers file
                for column in ['id', 'legacy_id', 'name', customer_column]:
                    # search the customer in the customers file
                    if column not in df_customers.columns:
                        continue

                    found_customer = df_customers.loc[
                        df_customers[column.lower(
                        )] == sale[customer_column.lower()]
                    ]

                    # if the customer is found, search if already exists in the database
                    if not found_customer.empty:
                        customer = self.customer_service.find_by_column(
                            column, found_customer.iloc[0][column.lower()]
                        )

                        if customer:
                            break

                # if the customer is not found, create it
                if customer is None and 'name' in df_customers.columns:
                    new_customer = Customer(
                        store_id=store_id,
                        name=found_customer.iloc[0]['name'],
                        email=found_customer.iloc[0]['email'] if 'email' in df_customers.columns else None,
                        phone=found_customer.iloc[0]['phone'] if 'phone' in df_customers.columns else None,
                        birthday=found_customer.iloc[0]['birthday'] if 'birthday' in df_customers.columns else None,
                        address=found_customer.iloc[0]['address'] if 'address' in df_customers.columns else None,
                        city=found_customer.iloc[0]['city'] if 'city' in df_customers.columns else None,
                        state=found_customer.iloc[0]['state'] if 'state' in df_customers.columns else None,
                        country=found_customer.iloc[0]['country'] if 'country' in df_customers.columns else None,
                        zipcode=found_customer.iloc[0]['zipcode'] if 'zipcode' in df_customers.columns else None,
                        legacy_id=found_customer.iloc[0]['id'] if 'id' in df_customers.columns else None,
                    )
                    customer, message = self.customer_service.create(
                        new_customer)

            # if the customer is not found in the customers file, search in the database
            if customer_column in sale and customer is None:
                # if there's no customers file, search the customer in the database by legacy_id
                customer = self.customer_service.find_by_column(
                    'legacy_id', sale[customer_column]
                )

                # if the customer still not found by name, search for name
                customer = self.customer_service.find_by_column(
                    'name', sale[customer_column]
                )

                # if the customer still not found by name, search for id
                if customer is None:
                    customer = self.customer_service.find_by_id(
                        sale[customer_column])

            # create the sale
            quantity = sale[quantity_column] if quantity_column else 1
            price = sale[price_column] if price_column else 0

            formated_date = date_column and parser.parse(
                sale[date_column]
            ).strftime("%Y-%m-%d") or None

            formated_date = formated_date and datetime.strptime(
                formated_date, "%Y-%m-%d") or None

            try:
                # Tentar criar um ObjectId a partir da string
                product_id = ObjectId(product['id'])
            except Exception as e:
                product_id = product['id']

            try:
                customer_id = ObjectId(customer['id'])
            except Exception as e:
                customer_id = sale[customer_column] if customer_column else None

            sale, message = self.sale_service.create(
                store_id=store_id,
                product_id=product_id,
                quantity=quantity,
                price=sale[price_column] if price_column else price*quantity,
                seller_id=sale[seller_column] if seller_column else None,
                customer_id=customer_id,
                status=sale[status_column] if status_column else None,
                date=formated_date
            )

            if sale:
                successful_imports += 1
            else:
                failed_imports += 1

        return True, f"{successful_imports} sales imported successfully, {failed_imports} failed imports"
