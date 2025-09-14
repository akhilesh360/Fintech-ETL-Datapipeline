from pydantic import BaseModel, Field
from typing import Optional
import pandas as pd

class Transaction(BaseModel):
    txn_id: str
    user_id: str
    product_id: str
    amount: float = Field(ge=0)
    txn_ts: str
    status: str

def load_transactions(csv_path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # Basic cleaning
    df = df.drop_duplicates(subset=['txn_id']).copy()
    df['txn_ts'] = pd.to_datetime(df['txn_ts'], errors='coerce')
    df = df[df['txn_ts'].notna()]
    df['status'] = df['status'].str.lower().str.strip()

    # Validate a few rows with pydantic for demo
    for _, row in df.head(5).iterrows():
        Transaction(**row.to_dict())

    return df
