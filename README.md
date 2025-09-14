# Fintech ETL & BI

## Project Overview

This repository demonstrates a production-style ETL and BI pipeline for fintech data, including synthetic transactions, users, and product information. The project showcases best practices in data engineering, analytics, and dashboarding, designed for consultants, analysts, and engineers seeking robust, modular, and reproducible workflows.


## Key Features

- **End-to-end ETL pipeline:** Ingest, clean, and transform raw data from multiple sources
- **Modular architecture:** Separate scripts for products, transactions, and users
- **Data warehouse integration:** SQLite and Snowflake DDLs for analytics-ready storage
- **Interactive dashboard:** Visualize KPIs and trends with a simple web app
- **Reproducible environment:** Requirements and config files for easy setup

```
fintech_etl_bi/
├── etl/            # ETL scripts and pipeline orchestration
├── data/           # Raw and reference datasets
├── models/         # Database schemas (Snowflake, SQLite)
├── warehouse/      # DB connection and query logic
├── dashboard/      # Streamlit or Flask dashboard app
├── tests/          # Unit tests for pipeline and logic
├── requirements.txt
├── README.md
```

## About the Dataset

- **Transactions:** Synthetic financial transactions with realistic attributes
- **Users:** Demographic and account info in JSON format
- **Products:** Reference product catalog
- **KPIs:** Calculated metrics for BI reporting

## Technologies Used

- **Python 3.11+**
- **pandas, numpy:** Data manipulation
- **SQLAlchemy:** Database interaction
- **SQLite, Snowflake:** Data warehousing
- **Streamlit/Flask:** Dashboarding
- **pytest:** Testing

## Example Outputs

- **Dashboard:** Interactive charts and tables for KPIs
- **ETL Logs:** Stepwise reporting of data ingestion and transformation
- **Warehouse Tables:** Analytics-ready schemas for reporting

## How to Contribute

1. Fork the repo and create a feature branch
2. Follow modular code structure and comment clearly
3. Submit a pull request with a description of your changes

## Acknowledgements

Inspired by best practices in fintech analytics and open-source data engineering.

---

## Step-by-Step Usage

### 1. Clone the Repository

```bash
git clone <repo-url>
cd fintech_etl_bi
```

### 2. Set Up the Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the ETL Pipeline

```bash
python etl/run_pipeline.py
```

### 4. Launch the Dashboard

```bash
python dashboard/app.py
```

### 5. Run Tests

```bash
pytest tests/
```

---
# Scalable ETL Pipelines & BI Adoption — Fintech Startup

A portfolio-ready, end-to-end, showing how to:
- **Ingest** multiple fintech data sources (transactions CSV, users JSON, products CSV).
- **Transform & model** data into a **star schema** (SQLite by default, Snowflake-ready SQL included).
- **Serve BI** via a **Streamlit** dashboard (KPIs, trends, product usage).
- **Collaborate on KPIs** with a crisp lineage from raw → models → dashboard.

> Quick start (local, SQLite): run the ETL, then launch the dashboard.

---

##  Architecture
```
data/
  raw/                 # source-like files (CSV/JSON) for sample data
  reference/           # reference/master data
etl/
  config.py            # config (DB URL, file paths, fee rates, etc.)
  run_pipeline.py      # orchestrates ingestion → cleaning → load
  ingest_transactions.py
  ingest_users.py
  ingest_products.py
warehouse/
  db.py                # DB helpers & table creation
models/
  sqlite/              # SQLite-compatible DDL/DML
  snowflake/           # Snowflake-compatible DDL/DML (for portability)
dashboard/
  app.py               # Streamlit BI app
requirements.txt
```

---

##  Quick Start

### 1) Install
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run ETL (builds `warehouse/fintech.db`)
```bash
python -m etl.run_pipeline
```

### 3) Launch Dashboard
```bash
streamlit run dashboard/app.py
```

---

##  Included KPIs (examples)
- **DAU (Daily Active Users)** — distinct users with ≥1 transaction.
- **GMV (Gross Merchandise Volume)** — sum of transaction amounts.
- **AOV (Average Order Value)** — GMV / # transactions.
- **Revenue (fees)** — `GMV * fee_rate` (configurable in `etl/config.py`).
- **Product usage** — txn count/GMV by product.

---

##  Snowflake Notes
This project ships with **Snowflake DDL/DML** in `models/snowflake/` so you can:
1. Point the ETL to Snowflake (optional; not required for local run).
2. Create equivalent tables/roles/indexing strategies in Snowflake.
3. Use your Looker (or other BI) on top of Snowflake.

For portability, local runs default to **SQLite**. The SQL in `models/snowflake/` mirrors the star schema.

---

##  Tests
A minimal test ensures the pipeline builds tables and loads rows. Run:
```bash
pytest -q
```

---

##  Tech Stack
- **Python** (pandas, SQLAlchemy, pydantic)
- **SQLite** (default) / **Snowflake-ready SQL** (optional)
- **Streamlit** (BI/dashboard)

---

##  Portfolio Talking Points
- Built **modular ETL** with source-specific ingestion, schema validation, and idempotent loads.
- Modeled a **star schema** with `fact_transactions`, `dim_users`, `dim_products`.
- Delivered **BI dashboards** surfacing DAU, GMV, AOV, product usage, & revenue trends.
- Clear **KPI lineage** from raw → modeled → dashboard; easy to swap SQLite → Snowflake.
