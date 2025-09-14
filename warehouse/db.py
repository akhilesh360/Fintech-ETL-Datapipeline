from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

def get_engine(db_url: str) -> Engine:
    engine = create_engine(db_url, future=True)
    return engine

DDL = [
    """CREATE TABLE IF NOT EXISTS dim_users (
        user_id TEXT PRIMARY KEY,
        signup_dt TEXT,
        segment TEXT,
        region TEXT
    );""",

    """CREATE TABLE IF NOT EXISTS dim_products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        active INTEGER
    );""",

    """CREATE TABLE IF NOT EXISTS fact_transactions (
        txn_id TEXT PRIMARY KEY,
        user_id TEXT,
        product_id TEXT,
        amount REAL,
        txn_ts TEXT,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES dim_users(user_id),
        FOREIGN KEY(product_id) REFERENCES dim_products(product_id)
    );"""
]

def create_tables(engine: Engine):
    with engine.begin() as conn:
        for stmt in DDL:
            conn.execute(text(stmt))

def upsert_df(engine: Engine, df, table: str, pk: str):
    # simple idempotent upsert using delete+insert for demo scale
    if df.empty:
        return
    keys = df[pk].tolist()
    with engine.begin() as conn:
        conn.execute(text(f"DELETE FROM {table} WHERE {pk} IN ({','.join([':k'+str(i) for i in range(len(keys))])})"),
                     {('k'+str(i)): v for i, v in enumerate(keys)})
        df.to_sql(table, conn, if_exists='append', index=False)
