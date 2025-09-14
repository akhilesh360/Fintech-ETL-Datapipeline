import pandas as pd
from .config import DB_URL, TRANSACTIONS_CSV, USERS_JSON, PRODUCTS_CSV, FEE_RATE
from .ingest_transactions import load_transactions
from .ingest_users import load_users
from .ingest_products import load_products
from ..warehouse.db import get_engine, create_tables, upsert_df

def transform_join(transactions, users, products):
    # filter bad statuses for revenue KPIs; keep raw status in fact
    clean_txn = transactions[transactions['status'].isin(['settled', 'refunded', 'chargeback'])].copy()
    # demo: no ref data needed here; joins are for dims existence
    return clean_txn, users, products

def load(engine, fact_df, dim_users, dim_products):
    create_tables(engine)
    upsert_df(engine, dim_users, 'dim_users', 'user_id')
    upsert_df(engine, dim_products, 'dim_products', 'product_id')
    upsert_df(engine, fact_df, 'fact_transactions', 'txn_id')

def main():
    print('Loading sources...')
    tx = load_transactions(TRANSACTIONS_CSV)
    users = load_users(USERS_JSON)
    products = load_products(PRODUCTS_CSV)

    print('Transforming...')
    fact_df, dim_users, dim_products = transform_join(tx, users, products)

    print('Loading warehouse...')
    engine = get_engine(DB_URL)
    load(engine, fact_df, dim_users, dim_products)

    print('Done. Warehouse at:', DB_URL)

if __name__ == '__main__':
    main()
