import os
import streamlit as st
import pandas as pd
import psycopg2

# функция для загрузки SQL из файлов
def load_sql(filename):
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, '..', 'sql', filename)
    with open(path, 'r') as f:
        return f.read()

# --- подключение к базе ---
conn = psycopg2.connect(
    dbname="analytics",
    user="analyst",
    password="1234",
    host="localhost",
    port="5432"
)

# --- заголовок ---
st.title("📊 Product Analytics Dashboard")

# =========================
# DAU
# =========================
st.header("DAU (Daily Active Users)")

dau_query = load_sql('dau.sql')
dau_df = pd.read_sql(dau_query, conn)
st.line_chart(dau_df.set_index("date"))

# =========================
# Retention (D1)
# =========================
st.header("Retention D1")

retention_query = load_sql('retention.sql')
ret_df = pd.read_sql(retention_query, conn)
st.dataframe(ret_df)

# =========================
# Funnel
# =========================
st.header("Funnel")

funnel_query = load_sql('funnel.sql')
funnel_df = pd.read_sql(funnel_query, conn)
st.bar_chart(funnel_df.set_index("event_type"))
st.write(funnel_df)
st.write(funnel_df.columns)
# --- закрытие соединения ---
conn.close()
