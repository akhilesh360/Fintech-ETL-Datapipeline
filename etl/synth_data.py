from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timedelta
import json, csv, random, math
import numpy as np

@dataclass
class SynthConfig:
    n_users: int = 50_000
    n_products: int = 25
    n_txns: int = 200_000
    start_date: str = "2025-07-01"
    days: int = 45
    out_dir_raw: Path = Path(__file__).resolve().parents[1] / "data" / "raw"
    out_dir_ref: Path = Path(__file__).resolve().parents[1] / "data" / "reference"
    seed: int = 42

SEGMENTS = ["retail", "business", "vip"]
REGIONS = ["CA","NY","TX","FL","WA","IL","MA","NJ","PA","GA","OH","MI","NC","VA","AZ","CO","WA","OR","MN","WI"]
CATEGORIES = ["card","credit","deposit","invest","insure"]
PRODUCT_NAMES = {
    "card": ["Debit Card","Travel Card","Cashback Card","Platinum Card","Student Card"],
    "credit": ["Personal Loan","Auto Loan","Credit Line","Micro Loan","BNPL"],
    "deposit": ["Savings Account","Checking Account","CD Account","Money Market","High-Yield Savings"],
    "invest": ["Brokerage","Robo Advisor","ETF Basket","Retirement IRA","Crypto Wallet"],
    "insure": ["Term Insurance","Health Cover","Accident Cover","Home Insurance","Device Protection"]
}

def make_products(n_products: int, rng: random.Random):
    # sample evenly from categories, cycle names
    products = []
    cat_list = list(CATEGORIES)
    pid = 1
    while len(products) < n_products:
        cat = cat_list[(pid-1) % len(cat_list)]
        name_list = PRODUCT_NAMES[cat]
        name = name_list[(pid-1) % len(name_list)]
        products.append({
            "product_id": f"P{pid:03d}",
            "product_name": name,
            "category": cat,
            "active": rng.random() > 0.05
        })
        pid += 1
    return products

def make_users(n_users: int, start_date: str, days: int, rng: random.Random):
    start = datetime.fromisoformat(start_date)
    users = []
    for i in range(1, n_users+1):
        signup_offset = rng.randint(0, days)
        signup_dt = (start + timedelta(days=signup_offset)).date().isoformat()
        users.append({
            "user_id": f"U{i:06d}",
            "signup_dt": signup_dt,
            "segment": rng.choice(SEGMENTS),
            "region": rng.choice(REGIONS)
        })
    return users

def sample_amount(rng: random.Random):
    # log-normal-ish distribution for transaction amounts
    m = rng.lognormvariate(3.2, 0.6)  # skewed right; median around ~24
    return round(min(max(m, 1.0), 5000.0), 2)

def status_from_risk(r: float, rng: random.Random):
    # small chance of refund/chargeback, grows with r
    if rng.random() < 0.02 + 0.05*r:
        return "chargeback"
    if rng.random() < 0.03 + 0.03*r:
        return "refunded"
    return "settled"

def make_txns(n_txns: int, start_date: str, days: int, n_users: int, n_products: int, rng: random.Random):
    start = datetime.fromisoformat(start_date)
    txns = []
    # Seasonality: day-of-week, and gradual growth
    for i in range(1, n_txns+1):
        day_offset = rng.randint(0, days-1)
        base_dt = start + timedelta(days=day_offset)
        # Hourly peaks: 9–11, 17–21
        hour = rng.choices(
            population=list(range(24)),
            weights=[1,1,1,1,1, 1,1,2,5,7,6,3, 2,2,2,2,2, 6,8,7,3,2,1,1],
            k=1
        )[0]
        minute = rng.randint(0,59); second = rng.randint(0,59)
        ts = base_dt.replace(hour=hour, minute=minute, second=second)

        user_idx = rng.randint(1, n_users)
        prod_idx = rng.randint(1, n_products)

        amount = sample_amount(rng)
        # risk increases with amount
        r = min(max((amount-50)/5000, 0.0), 1.0)
        st = status_from_risk(r, rng)

        txns.append({
            "txn_id": f"T{i:07d}",
            "user_id": f"U{user_idx:06d}",
            "product_id": f"P{prod_idx:03d}",
            "amount": f"{amount:.2f}",
            "txn_ts": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "status": st
        })
    return txns

def write_csv(path: Path, rows, header):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def write_json(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(rows, f, indent=2)

def generate(cfg: SynthConfig):
    rng = random.Random(cfg.seed)
    products = make_products(cfg.n_products, rng)
    users = make_users(cfg.n_users, cfg.start_date, cfg.days, rng)
    txns = make_txns(cfg.n_txns, cfg.start_date, cfg.days, cfg.n_users, cfg.n_products, rng)

    # write
    write_json(cfg.out_dir_raw / "users.json", users)
    write_csv(cfg.out_dir_ref / "products.csv", products, ["product_id","product_name","category","active"])
    write_csv(cfg.out_dir_raw / "transactions.csv", txns, ["txn_id","user_id","product_id","amount","txn_ts","status"])

if __name__ == "__main__":
    cfg = SynthConfig()
    generate(cfg)
    print("Generated synthetic dataset:")
    print(f"Users: {cfg.n_users}, Products: {cfg.n_products}, Transactions: {cfg.n_txns}")
