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
st.header("Retention by platform (daily)")

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
),
cohort_size AS (
    SELECT 
        platform,
        COUNT(DISTINCT user_id) as users
    FROM activity
    WHERE day = 0
    GROUP BY platform
)
SELECT 
    a.platform,
    a.day,
    COUNT(DISTINCT a.user_id) * 100.0 / c.users as retention
FROM activity a
JOIN cohort_size c ON a.platform = c.platform
WHERE a.day <= 7
GROUP BY a.platform, a.day, c.users
ORDER BY a.platform, a.day
"""

retention_platform_df = pd.read_sql(retention_platform_query, conn)

pivot_df = retention_platform_df.pivot(
    index="day",
    columns="platform",
    values="retention"
)

st.line_chart(pivot_df)

# =========================
# Funnel
# =========================
st.header("Funnel")

# --- SQL ---
funnel_platform_query = """
SELECT 
    platform,
    COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'login') as login,
    COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'view_note') as view_note,
    COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'create_note') as create_note
FROM events
GROUP BY platform;
"""

fp_df = pd.read_sql(funnel_platform_query, conn)

# --- конверсия в целевое действие ---
fp_df["conversion_to_create"] = fp_df["create_note"] / fp_df["login"] * 100

# --- показываем таблицу ---
st.subheader("Funnel table")
st.dataframe(fp_df)

# --- готовим данные для графика (события по X, платформы — цвета) ---
plot_df = fp_df.set_index("platform")[["login", "view_note", "create_note"]].T

# фикс порядка шагов
plot_df = plot_df.loc[["login", "view_note", "create_note"]]

# --- график ---
st.subheader("Funnel by platform")
st.bar_chart(plot_df)

# посмотреть датасет
st.header("Data")

df = pd.read_sql("SELECT * FROM events LIMIT 1000", conn)
st.dataframe(df)

# --- закрытие соединения ---
conn.close()
