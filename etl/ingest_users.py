from pydantic import BaseModel
import pandas as pd
import json

class User(BaseModel):
    user_id: str
    signup_dt: str
    segment: str
    region: str

def load_users(json_path) -> pd.DataFrame:
    data = json.loads(open(json_path).read())
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=['user_id']).copy()
    df['signup_dt'] = pd.to_datetime(df['signup_dt'], errors='coerce')
    df = df[df['signup_dt'].notna()]
    return df
