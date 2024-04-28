from src.repositories.customer_repository import CustomerRepository
from src.services.sale_service import SaleService
from src.models.customer import Customer
import pandas as pd
import json
from bson.son import SON
from datetime import datetime


class CustomerService:
    def __init__(self):
        self.customer_repository = CustomerRepository()
        self.sale_service = SaleService()

    def create(
        self,
        customer: Customer,
    ):
        return self.customer_repository.create(customer), "Customer created successfully"

    def update(
        self,
        customer_id,
        name: str or None,
        email: str or None,
        phone: str or None,
        address: str or None,
        city: str or None,
        state: str or None,
        country: str or None,
        zipcode: str or None
    ):

        customer = Customer(
            name,
            email,
            phone,
            address,
            city,
            state,
            country,
            zipcode
        )
        return self.customer_repository.update(customer_id, customer), "Customer updated successfully"

    def delete(self, customer_id):
        return self.customer_repository.delete(customer_id)

    def get_total_customers(self, store_id, search):
        return self.customer_repository.get_total_customers(store_id, search)

    def get_customers(self, store_id, query, page, page_size):
        return self.customer_repository.get_customers(store_id, query, page, page_size)

    def find_by_id(self, customer_id):
        return self.customer_repository.find_by_id(customer_id)

    def find_by_column(self, column, value):
        return self.customer_repository.find_by_column(column, value)

    def get_customers_states(self, store_id):
        return self.customer_repository.get_customers_states(store_id)

        return idade_media

    def get_customers_resume(self, store_id):
        total_customers = self.customer_repository.get_total_customers(
            store_id)
        total_buyers_this_month = self.sale_service.get_total_buyers_this_month(
            store_id)
        average_spent = self.sale_service.get_average_customer_spent(store_id)

        sales = self.sale_service.get_sales_by_states(store_id)

        return {
            "total_customers": total_customers,
            "total_buyers_this_month": total_buyers_this_month,
            "average_spent": average_spent,
        }
