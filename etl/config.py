from pathlib import Path

# Database (SQLite by default for portability; swap to Snowflake via SQLAlchemy if needed)
DB_URL = f"sqlite:///{Path(__file__).resolve().parent.parent / 'warehouse' / 'fintech.db'}"

# Files
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
RAW_DIR = DATA_DIR / 'raw'
REF_DIR = DATA_DIR / 'reference'

TRANSACTIONS_CSV = RAW_DIR / 'transactions.csv'
USERS_JSON = RAW_DIR / 'users.json'
PRODUCTS_CSV = REF_DIR / 'products.csv'

# KPI / Business Config
FEE_RATE = 0.0125  # 1.25% fee on GMV
