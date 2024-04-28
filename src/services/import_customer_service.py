from src.models.customer import Customer


class ImportCustomerService:
  # transform the customers from a file list into a list of Customer objects
    def transform_customers(
        self,
        df,
        store_id,
        name_col,
        email_col,
        phone_col,
        birthday_col,
        address_col,
        city_col,
        state_col,
        country_col,
        zipcode_col
    ):
        if not store_id:
            return False, "Missing store_id field"

        valid, message = self.validate_data_columns(
            df,
            name_col,
            email_col,
            phone_col,
            birthday_col,
            address_col,
            city_col,
            state_col,
            country_col,
            zipcode_col
        )

        if not valid:
            return False, message

        total_valid = 0
        total_invalid = 0
        transformed_customers = []

        for index, row in df.iterrows():
            # Acesse os valores da linha usando os nomes das colunas
            name = row[name_col] if name_col else None
            email = row[email_col] if email_col else None
            phone = row[phone_col] if phone_col else None
            birthday = row[birthday_col] if birthday_col else None
            address = row[address_col] if address_col else None
            city = row[city_col] if city_col else None
            state = row[state_col] if state_col else None
            country = row[country_col] if country_col else None
            zipcode = row[zipcode_col] if zipcode_col else None
            legacy_id = None

            # define o valor do legacy_id que representao o id do produto no sistema legado
            if 'id' in df.columns:
                legacy_id = row['id']
            elif 'customer_unique_id' in df.columns:
                legacy_id = row['customer_unique_id']
            elif 'customer_id' in df.columns:
                legacy_id = row['customer_id']

            if not name and not email and not phone and not birthday and not address and not city and not state and not country and not zipcode:
                total_invalid += 1
                continue

            new_customer = Customer(
                store_id, name, email, phone, birthday, address, city, state, country, zipcode, legacy_id)

            transformed_customers.append(new_customer)
            total_valid += 1

        return transformed_customers, str(total_valid)

  # Validate if the columns are valid

    def validate_data_columns(
        self,
        customers: list,
        name_col,
        email_col,
        phone_col,
        birthday_col,
        address_col,
        city_col,
        state_col,
        country_col,
        zipcode_col
    ):
        if name_col and name_col not in customers.columns:
            return False, "Missing "+description_col+" column"

        if email_col and email_col not in customers.columns:
            return False, "Missing "+description_col+" column"

        if phone_col and phone_col not in customers.columns:
            return False, "Missing "+category_col+" column"

        if birthday_col and birthday_col not in customers.columns:
            return False, "Missing "+price_col+" column"

        if address_col and address_col not in customers.columns:
            return False, "Missing "+stock_col+" column"

        if city_col and city_col not in customers.columns:
            return False, "Missing "+stock_col+" column"

        if state_col and state_col not in customers.columns:
            return False, "Missing "+stock_col+" column"

        if country_col and country_col not in customers.columns:
            return False, "Missing "+stock_col+" column"

        if zipcode_col and zipcode_col not in customers.columns:
            return False, "Missing "+stock_col+" column"

        return True, "Valid columns"
