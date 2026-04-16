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
   dbname="analytics", user="analyst", password="1234", host="localhost",
    port="5432"
)

# --- заголовок ---
st.title("📊 Product Analytics Dashboard")

# =========================
# DAU
# =========================
st.header("DAU (Daily Active Users)")

# dau_query = load_sql('dau.sql')
# dau_df = pd.read_sql(dau_query, conn)
# st.line_chart(dau_df.set_index("date"))

dau_platform = pd.read_sql("""
SELECT 
    DATE(event_time) as date,
    platform,
    COUNT(DISTINCT user_id) as dau
FROM events
GROUP BY date, platform
""", conn)

st.line_chart(dau_platform.pivot(index="date", columns="platform", values="dau"))


# =========================
# Retention (D1)
# =========================
#st.header("Retention")

# retention_query = load_sql('retention.sql')
# ret_df = pd.read_sql(retention_query, conn)
# st.dataframe(ret_df)
st.header("Retention by platform")

retention_platform_query = """
WITH first_events AS (
    SELECT 
        user_id,
        MIN(DATE(event_time)) as signup_date
    FROM events
    GROUP BY user_id
),
activity AS (
    SELECT 
        e.user_id,
        e.platform,
        DATE(e.event_time) - f.signup_date as day
    FROM events e
    JOIN first_events f ON e.user_id = f.user_id
)
SELECT 
    platform,
    COUNT(DISTINCT user_id) FILTER (WHERE day = 1) * 100.0 /
    COUNT(DISTINCT user_id) FILTER (WHERE day = 0) AS d1_retention
FROM activity
GROUP BY platform
"""

retention_platform_df = pd.read_sql(retention_platform_query, conn)

st.dataframe(retention_platform_df)
# =========================
# Funnel
# =========================
st.header("Funnel")

funnel_query = load_sql('funnel.sql')
funnel_df = pd.read_sql(funnel_query, conn)

# фикс порядка шагов funnel
funnel_df["event_type"] = pd.Categorical(
    funnel_df["event_type"],
    categories=["login", "view_note", "create_note"],
    ordered=True
)
funnel_df = funnel_df.sort_values("event_type")
st.bar_chart(funnel_df.set_index("event_type"))

# посмотреть датасет
st.header("Debug: raw data")

df = pd.read_sql("SELECT * FROM events LIMIT 1000", conn)
st.dataframe(df)

# --- закрытие соединения ---
conn.close()
