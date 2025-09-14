-- Snowflake DDL/DML equivalent (run manually in Snowflake)
CREATE OR REPLACE TABLE dim_users (
  user_id STRING PRIMARY KEY,
  signup_dt DATE,
  segment STRING,
  region STRING
);

CREATE OR REPLACE TABLE dim_products (
  product_id STRING PRIMARY KEY,
  product_name STRING,
  category STRING,
  active BOOLEAN
);

CREATE OR REPLACE TABLE fact_transactions (
  txn_id STRING PRIMARY KEY,
  user_id STRING REFERENCES dim_users(user_id),
  product_id STRING REFERENCES dim_products(product_id),
  amount NUMBER(12,2),
  txn_ts TIMESTAMP_NTZ,
  status STRING
);

-- Example KPI views
CREATE OR REPLACE VIEW v_dau AS
SELECT TO_DATE(txn_ts) AS d, COUNT(DISTINCT user_id) AS dau
FROM fact_transactions
WHERE status = 'SETTLED'
GROUP BY TO_DATE(txn_ts);

CREATE OR REPLACE VIEW v_gmv AS
SELECT TO_DATE(txn_ts) AS d, SUM(amount) AS gmv
FROM fact_transactions
WHERE status = 'SETTLED'
GROUP BY TO_DATE(txn_ts);

CREATE OR REPLACE VIEW v_product_usage AS
SELECT p.product_name, COUNT(*) AS txn_cnt, SUM(IFF(f.status='SETTLED', f.amount, 0)) AS gmv
FROM fact_transactions f
JOIN dim_products p ON p.product_id = f.product_id
GROUP BY p.product_name;
