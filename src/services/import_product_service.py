from src.models.product import Product


class ImportProductService:
    # transform the products from the file list into a list of Product objects
    def transform_products(self, df, store_id, name_col, description_col, category_col, price_col, purchase_price_col, stock_col):
        # Validate if the columns are valid
        valid, message = self.validate_columns(
            name_col, description_col, category_col, price_col, stock_col
        )

        if not valid:
            return False, message

        valid, message = self.validate_data_columns(
            df,
            name_col,
            description_col,
            category_col,
            price_col,
            purchase_price_col,
            stock_col
        )

        if not valid:
            return False, message

        total_valid = 0
        total_invalid = 0
        transformed_products = []

        for index, row in df.iterrows():

            # Acesse os valores da linha usando os nomes das colunas
            name = row[name_col]
            description = row[description_col] if description_col else None
            category = row[category_col] if category_col else None
            price = row[price_col] if price_col else None
            purchase_price = row[purchase_price_col] if purchase_price_col else None
            stock = row[stock_col] if stock_col else None
            legacy_id = None

            # define o valor do legacy_id que representao o id do produto no sistema legado
            if 'id' in df.columns:
                legacy_id = row['id']

            elif 'product_id' in df.columns:
                legacy_id = row['product_id']

            new_product = Product(
                store_id=store_id,
                name=name,
                description=description,
                category=category,
                price=price,
                purchase_price=purchase_price,
                stock=stock,
                legacy_id=legacy_id
            )

            if name and len(name) > 3:
                transformed_products.append(new_product)
                total_valid += 1
            else:
                total_invalid += 1

        return transformed_products, str(total_valid)

    def remove_duplicates_products(df):
        # Converter a coluna 'name' para letras minúsculas
        df['name'] = df['name'].str.lower()

        # Remover dados duplicados
        df_no_duplicates = df.drop_duplicates(subset='name', keep='first')

        return df_no_duplicates

    def validate_columns(self, name, description, category, price, stock):
        if not name or type(name) != str:
            return False, "Missing name field"

        return True, None

    def validate_data_columns(
        self,
        products: list,
        name_col: str,
        description_col: str or None,
        category_col: str or None,
        price_col: str or None,
        purchase_price_col: str or None,
        stock_col: str or None
    ):
        if name_col not in products.columns:
            return False, "Missing "+name_col+" column"

        if description_col and description_col not in products.columns:
            return False, "Missing "+description_col+" column"

        if category_col and category_col not in products.columns:
            return False, "Missing "+category_col+" column"

        if price_col and price_col not in products.columns:
            return False, "Missing "+price_col+" column"

        if purchase_price_col and purchase_price_col not in products.columns:
            return False, "Missing "+purchase_price_col+" column"

        if stock_col and stock_col not in products.columns:
            return False, "Missing "+stock_col+" column"

        return True, None
