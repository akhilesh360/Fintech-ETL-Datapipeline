import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

DB_PATH = Path(__file__).resolve().parents[1] / 'warehouse' / 'fintech.db'

st.set_page_config(page_title='Fintech ETL & BI Demo', layout='wide')

st.title('📊 Fintech ETL & BI Demo')
st.caption('End-to-end: ETL → Star Schema → KPIs → Dashboard')

if not DB_PATH.exists():
    st.warning('Database not found. Please run the ETL first: `python -m etl.run_pipeline`')
    st.stop()

conn = sqlite3.connect(DB_PATH)

# Create KPI views if not created
with open(Path(__file__).resolve().parents[1] / 'models' / 'sqlite' / 'kpis.sql') as f:
    conn.executescript(f.read())

dau = pd.read_sql_query('SELECT * FROM v_dau ORDER BY d;', conn, parse_dates=['d'])
gmv = pd.read_sql_query('SELECT * FROM v_gmv ORDER BY d;', conn, parse_dates=['d'])
prod = pd.read_sql_query('SELECT * FROM v_product_usage ORDER BY gmv DESC;', conn)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Days Covered', len(dau))
with col2:
    st.metric('Total GMV', f"${gmv['gmv'].sum():,.2f}")
with col3:
    st.metric('Peak DAU', int(dau['dau'].max()) if len(dau)>0 else 0)

st.subheader('GMV Over Time')
fig1, ax1 = plt.subplots()
ax1.plot(gmv['d'], gmv['gmv'])
ax1.set_xlabel('Date'); ax1.set_ylabel('GMV')
st.pyplot(fig1)

st.subheader('Daily Active Users')
fig2, ax2 = plt.subplots()
ax2.bar(dau['d'], dau['dau'])
ax2.set_xlabel('Date'); ax2.set_ylabel('DAU')
st.pyplot(fig2)

st.subheader('Product Usage (Transactions & GMV)')
st.dataframe(prod)

st.markdown('---')
st.caption('Tip: Swap SQLite for Snowflake in production; See `models/snowflake/ddl.sql`.')
