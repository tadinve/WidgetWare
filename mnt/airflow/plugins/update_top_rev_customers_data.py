import pandas as pd
from sqlalchemy import create_engine

account_identifier = '<account_identifier>'
user = '<user_login_name>'
password = '<password>'
database_name = '<database_name>'
schema_name = '<schema_name>'
postgres_link = 'postgresql://postgres:postgres@database-1.c3tdzmqqtx8o.us-east-2.rds.amazonaws.com/widgetware'

def extract_customers():
    query = """
    SELECT * from pg_customers;
    """

    postgres_engine = create_engine(postgres_link)
    df_pg_customers = pd.read_sql(query, con=postgres_engine)

    df_pg_customers.to_sql('customers_raw', con=postgres_engine, if_exists='replace', index=False)


def extract_order_details():

    query = """
    SELECT * from pg_order_details;
    """

    postgres_engine = create_engine(postgres_link)
    df_pg_order_details = pd.read_sql(query, con=postgres_engine)


    df_pg_order_details.to_sql('order_details_raw', con=postgres_engine, if_exists='replace', index=False)


def merge_customers_orders():
    query = """
        SELECT *
        FROM pg_customers
        INNER JOIN pg_orders as orders
        ON pg_customers."CustomerID" = orders."CustomerID"
        INNER JOIN pg_order_details as ord_det
        ON orders."OrderID" = ord_det."OrderID"
    """
    postgres_engine = create_engine(postgres_link)
    customers_orders = pd.read_sql(query, postgres_engine)
    customers_orders.to_sql('customers_orders', con=postgres_engine, if_exists='replace', index=False)


def aggregate_top_revenue_customers():
    query = """
    SELECT *
    FROM customers_orders
    """
    postgres_engine = create_engine(postgres_link)
    df = pd.read_sql(query, postgres_engine)
    df['Revenue'] = df['UnitPrice'] * df['Quantity']
    df = df[['CustomerID', 'CompanyName', 'ContactName',
             'ProductID', 'UnitPrice', 'Quantity', 'Revenue']]
    df = df.T.drop_duplicates().T
    top_revenue_customers = df.groupby('CustomerID')[['Revenue']].sum().\
        merge(df[['CustomerID', 'CompanyName', 'ContactName']],
              on='CustomerID').drop_duplicates().\
        sort_values('Revenue', ascending=False).reset_index(drop=True)
    top_revenue_customers.to_sql('top_revenue_customers', con=postgres_engine,
                                 if_exists='replace', index=False)


def send_to_superset_dashboard(table):
    query = f"""
        SELECT *
        FROM {table}
        """
    postgres_engine = create_engine(postgres_link)
    df = pd.read_sql(query, postgres_engine)


def extract_products():
    query = """
            SELECT *
            FROM pg_products
            """
    postgres_engine = create_engine(postgres_link)
    pg_products = pd.read_sql(query, postgres_engine)
    pg_products.to_sql('products_raw', postgres_engine, if_exists='replace', index=False)

def merge_product_orders():
    query = """
    SELECT *
    FROM products_raw
    INNER JOIN order_details_raw
    ON products_raw."ProductID" = order_details_raw."ProductID"
    """
    postgres_engine = create_engine(postgres_link)
    products_orders = pd.read_sql(query, postgres_engine).T.drop_duplicates().T
    products_orders.to_sql('products_orders', postgres_engine, if_exists='replace', index=False)


def aggregate_top_revenue_products():
    query = """
        SELECT *
        FROM products_orders
    """
    postgres_engine = create_engine(postgres_link)
    
    df = pd.read_sql(query, postgres_engine).T.drop_duplicates().T
    print(df.columns)
    #df['UnitPrice_avg'] = df['UnitPrice'].mean(axis=1)
    df['Revenue'] = df['UnitPrice'] * df['Quantity']
    top_revenue_products = df[['ProductID', 'Revenue']].groupby('ProductID').\
        sum().reset_index().merge(
        df[['ProductID', 'ProductName', 'UnitPrice']],
        on='ProductID').drop_duplicates('ProductID').reset_index(
        drop=True).sort_values('Revenue', ascending=False).reset_index(drop=True)
    top_revenue_products.to_sql('top_revenue_products', postgres_engine, if_exists='replace', index=False)








