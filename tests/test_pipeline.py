from pathlib import Path
import sqlite3
import subprocess, sys

def test_pipeline_builds_db():
    root = Path(__file__).resolve().parents[1]
    # run ETL
    subprocess.check_call([sys.executable, '-m', 'etl.run_pipeline'], cwd=root.as_posix())
    db = root / 'warehouse' / 'fintech.db'
    assert db.exists(), 'DB file should exist'
    con = sqlite3.connect(db)
    cur = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {r[0] for r in cur.fetchall()}
    assert {'dim_users', 'dim_products', 'fact_transactions'} <= tables
