import streamlit as st
import pandas as pd
import psycopg2

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

dau_query = """
SELECT
    DATE(event_time) as date,
    COUNT(DISTINCT user_id) as dau
FROM events
GROUP BY date
ORDER BY date;
"""

dau_df = pd.read_sql(dau_query, conn)

st.line_chart(dau_df.set_index("date"))

# =========================
# Retention (D1)
# =========================
st.header("Retention D1")

retention_query = """
WITH first_visit AS (
    SELECT user_id, MIN(DATE(event_time)) as first_date
    FROM events
    GROUP BY user_id
),
activity AS (
    SELECT
        e.user_id,
        DATE(e.event_time) as event_date,
        f.first_date
    FROM events e
    JOIN first_visit f ON e.user_id = f.user_id
),
retention AS (
    SELECT
        first_date,
        event_date,
        COUNT(DISTINCT user_id) as users
    FROM activity
    GROUP BY first_date, event_date
)
SELECT
    first_date,
    event_date,
    users
FROM retention
ORDER BY first_date, event_date;
"""

ret_df = pd.read_sql(retention_query, conn)

st.dataframe(ret_df)

# =========================
# Funnel
# =========================
st.header("Funnel")

funnel_query = """
SELECT
    event_type,
    COUNT(DISTINCT user_id) as users
FROM events
GROUP BY event_type
ORDER BY users DESC;
"""

funnel_df = pd.read_sql(funnel_query, conn)

st.bar_chart(funnel_df.set_index("event_type"))

# --- закрытие соединения ---
conn.close()
