-- Derived KPI views (SQLite)
DROP VIEW IF EXISTS v_dau;
CREATE VIEW v_dau AS
SELECT date(txn_ts) AS d, COUNT(DISTINCT user_id) AS dau
FROM fact_transactions
WHERE status = 'settled'
GROUP BY date(txn_ts);

DROP VIEW IF EXISTS v_gmv;
CREATE VIEW v_gmv AS
SELECT date(txn_ts) AS d, SUM(amount) AS gmv
FROM fact_transactions
WHERE status = 'settled'
GROUP BY date(txn_ts);

DROP VIEW IF EXISTS v_product_usage;
CREATE VIEW v_product_usage AS
SELECT p.product_name, COUNT(*) AS txn_cnt, SUM(CASE WHEN f.status='settled' THEN f.amount ELSE 0 END) AS gmv
FROM fact_transactions f
JOIN dim_products p ON p.product_id = f.product_id
GROUP BY p.product_name;
