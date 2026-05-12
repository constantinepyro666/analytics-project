import os
import streamlit as st
import pandas as pd
import psycopg2
import altair as alt

# --- Настройка страницы ---
st.set_page_config(page_title="Product Analytics Dashboard", layout="wide")

# --- Функция для загрузки SQL из файлов ---
def load_sql(filename):
    # Путь относительно текущего файла app.py: ./sql/filename
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, 'sql', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# --- Подключение к базе данных ---
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"), 
        port="5432"
    )

conn = get_connection()

# --- Заголовок ---
st.title("📊 Product Analytics Dashboard")

# =========================
# Блок 1: DAU
# =========================
st.header("DAU (Daily Active Users)")

dau_query = load_sql('dau.sql')
dau_platform = pd.read_sql(dau_query, conn)

# Превращаем в сводную таблицу для графика
dau_pivot = dau_platform.pivot(index="date", columns="platform", values="dau")
st.line_chart(dau_pivot)


# =========================
# Блок 2: Retention
# =========================
st.header("Retention by Platform (Daily)")

retention_query = load_sql('retention.sql')
retention_df = pd.read_sql(retention_query, conn)

# Превращаем в сводную таблицу (строки — дни жизни, колонки — платформы)
retention_pivot = retention_df.pivot(index="day", columns="platform", values="retention")
st.line_chart(retention_pivot)


# =========================
# Блок 3: Funnel
# =========================
st.header("Funnel")

funnel_query = load_sql('funnel.sql')
fp_df = pd.read_sql(funnel_query, conn)

# Расчет конверсий
fp_df["conversion_to_view"] = (fp_df["view_note"] / fp_df["login"] * 100).round(2)
fp_df["conversion_to_create"] = (fp_df["create_note"] / fp_df["login"] * 100).round(2)
fp_df["view_to_create"] = (fp_df["create_note"] / fp_df["view_note"] * 100).round(2)

st.subheader("Funnel Table")
st.dataframe(fp_df, use_container_width=True)

st.subheader("Visual Funnel by Platform")

# Подготовка данных для Altair (long format)
plot_long = fp_df.melt(
    id_vars="platform", 
    value_vars=["login", "view_note", "create_note"],
    var_name="step", 
    value_name="users"
)

# Красивые названия и порядок шагов
step_map = {
    "login": "1. Login",
    "view_note": "2. View Note",
    "create_note": "3. Create Note"
}
plot_long["step"] = plot_long["step"].map(step_map)
step_order = ["1. Login", "2. View Note", "3. Create Note"]

# Отрисовка столбчатой диаграммы
chart = alt.Chart(plot_long).mark_bar().encode(
    x=alt.X("step:N", sort=step_order, title="Step"),
    y=alt.Y("users:Q", title="Unique Users"),
    color=alt.Color("platform:N", title="Platform"),
    column="platform:N" # Разделение на колонки для сравнения платформ
).properties(width=200, height=400)

st.altair_chart(chart)


# =========================
# Блок 4: Сырые данные
# =========================
with st.expander("Show Raw Data Sample"):
    raw_data = pd.read_sql("SELECT * FROM user_events LIMIT 100", conn)
    st.dataframe(raw_data, use_container_width=True)

# Закрытие соединения при остановке приложения (опционально для Streamlit)
# conn.close()
