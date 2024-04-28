from flask import request, jsonify
from src.models.product import Product
from src.models.customer import Customer
from src.services.product_service import ProductService
from src.services.import_product_service import ImportProductService
from src.services.import_sale_service import ImportSaleService
from src.services.import_customer_service import ImportCustomerService
from src.services.customer_service import CustomerService
import pandas as pd
import json
from dateutil import parser


class ImportController:
    def __init__(self):
        self.product_service = ProductService()
        self.import_product_service = ImportProductService()
        self.import_sale_service = ImportSaleService()
        self.import_customer_service = ImportCustomerService()
        self.customer_service = CustomerService()

    def import_sales(self):
        valid_request, message = self.is_valid_file(
            request, filename='sales_file')

        if not valid_request:
            return jsonify({"message": message}), 400

        if 'products_file' in request.files:
            valid_request, message = self.is_valid_file(
                request, filename='products_file')

            if not valid_request:
                return jsonify({"message": message}), 400

        if 'customers_file' in request.files:
            valid_request, message = self.is_valid_file(
                request, filename='customers_file')

            if not valid_request:
                return jsonify({"message": message}), 400

        if 'product_column' not in request.form or not request.form['product_column']:
            return jsonify({"message": "Missing product_column field"}), 400

        if 'store_id' not in request.form or not request.form['store_id']:
            return jsonify({"message": "Missing store_id field"}), 400

        # transform sales file to dataframe
        sales_file = request.files['sales_file']
        df_sales, message = self.read_file(sales_file)

        if df_sales.empty:
            return jsonify({"message": message}), 400

        # transform products file to dataframe if exists
        products_file = request.files['products_file'] if 'products_file' in request.files else None
        df_products, message = self.read_file(products_file)

        # transform customers file to dataframe if exists
        customers_file = request.files['customers_file'] if 'customers_file' in request.files else None
        df_customers, message = self.read_file(customers_file)

        data, message = self.import_sale_service.import_sales(
            df_sales,
            df_products if not df_products.empty else None,
            df_customers if not df_customers.empty else None,
            request.form['store_id'],
            request.form['product_column'],
            'quantity_column' in request.form and request.form['quantity_column'],
            'price_column' in request.form and request.form['price_column'],
            'seller_column' in request.form and request.form['seller_column'],
            'customer_column' in request.form and request.form['customer_column'],
            'status_column' in request.form and request.form['status_column'],
            'date_column' in request.form and request.form['date_column']
        )

        return jsonify({
            "message": message,
            "data": data
        }), 200

    def import_products(self):
        valid_request, message = self.is_valid_file(request)
        if not valid_request:
            return jsonify({"message": message}), 400

        store_id = 'store_id' in request.form and request.form['store_id'] or None

        if not store_id:
            return jsonify({"message": "Missing store_id field"}), 400

        if 'name_column' not in request.form or not request.form['name_column']:
            return jsonify({"message": "Missing name_column field"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"message": "No file selected"}), 400

        df, message = self.read_file(file)

        if df.empty:
            return jsonify({"message": message}), 400

        product_list, message = self.import_product_service.transform_products(
            df,
            store_id,
            request.form['name_column'],
            'description_column' in request.form and request.form['description_column'],
            'category_column' in request.form and request.form['category_column'],
            'price_column' in request.form and request.form['price_column'],
            'purchase_price_column' in request.form and request.form['purchase_price_column'],
            'stock_column' in request.form and request.form['stock_column']
        )

        if not product_list:
            return jsonify({"message": message}), 400

        imported_products = 0
        failed_imports = 0
        for product in product_list:
            new_product = Product(
                store_id=store_id,
                name=product.name,
                description=product.description,
                category=product.category,
                price=product.price,
                purchase_price=product.purchase_price,
                stock=product.stock if product.stock.isnumeric() else 0,
                legacy_id=product.legacy_id
            )
            created_product = self.product_service.create(new_product)

            if created_product:
                imported_products += 1
            else:
                failed_imports += 1

        return jsonify({
            "message": str(imported_products) + " products imported successfully",
            "imported": imported_products,
            "failed": failed_imports
        }), 200

    def import_customers(self):
        valid_request, message = self.is_valid_file(request)
        if not valid_request:
            return jsonify({"message": message}), 400

        store_id = 'store_id' in request.form and request.form['store_id'] or None

        if not store_id:
            return jsonify({"message": "Missing store_id field"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"message": "No file selected"}), 400

        df, message = self.read_file(file)

        if df.empty:
            return jsonify({"message": message}), 400

        customer_list, message = self.import_customer_service.transform_customers(
            df,
            store_id,
            'name_column' in request.form and request.form['name_column'],
            'email_column' in request.form and request.form['email_column'],
            'phone_column' in request.form and request.form['phone_column'],
            'birthday_column' in request.form and request.form['birthday_column'],
            'address_column' in request.form and request.form['address_column'],
            'city_column' in request.form and request.form['city_column'],
            'state_column' in request.form and request.form['state_column'],
            'country_column' in request.form and request.form['country_column'],
            'zipcode_column' in request.form and request.form['zipcode_column']
        )

        if not customer_list:
            return jsonify({"message": message}), 400

        imported_customers = 0
        failed_imports = 0
        for customer in customer_list:

            new_customer = Customer(
                store_id=store_id,
                name=customer.name,
                email=customer.email,
                phone=customer.phone,
                birthday=customer.birthday,
                address=customer.address,
                city=customer.city,
                state=customer.state,
                country=customer.country,
                zipcode=customer.zipcode,
                legacy_id=customer.legacy_id
            )

            created_customer, message = self.customer_service.create(
                new_customer)

            if created_customer:
                imported_customers += 1
            else:
                failed_imports += 1

        return jsonify({
            "message": str(imported_customers) + " customers imported successfully",
            "imported": imported_customers,
            "failed": failed_imports
        }), 200

    ###############################################################
    #                        Auxiliary methods                    #
    ###############################################################

    def is_valid_file(self, request, filename='file'):
        if filename not in request.files:
            return False, "No file part in the request"

        file = request.files[filename]

        if file.filename == '':
            return False, "No file selected"

        return True, None

    def read_file(self, file):
        if file:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.filename.endswith('.xlsx'):
                df = pd.read_excel(file)

            elif file.filename.endswith('.ods'):
                df = pd.read_excel(file, engine='odf')
            else:
                return pd.DataFrame(), "File extension not supported"

            return df.fillna(''), None

        return pd.DataFrame(), "No file selected"
