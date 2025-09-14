from pydantic import BaseModel
import pandas as pd

class Product(BaseModel):
    product_id: str
    product_name: str
    category: str
    active: bool

def load_products(csv_path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # coerce booleans
    df['active'] = df['active'].astype(str).str.lower().isin(['true', '1', 'yes'])
    df = df.drop_duplicates(subset=['product_id']).copy()
    return df
