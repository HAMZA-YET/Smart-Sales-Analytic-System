import streamlit as st
import plotly.express as px
import requests
from pathlib import Path

from analytics import load_sales_data, calculate_kpis, run_sql_insights
from automation import generate_report
from database_setup import create_database

st.set_page_config(page_title="Smart Sales Analytics System", layout="wide")

st.title("Smart Sales Analytics & Automation System")
st.write("Business dashboard using Python, SQLite, Streamlit, SQL, automation, and API integration.")

if not Path("business_sales.db").exists():
    create_database()

try:
    df = load_sales_data()
except Exception as error:
    st.error(str(error))
    st.stop()

regions = sorted(df["region"].unique())
categories = sorted(df["category"].unique())

selected_regions = st.sidebar.multiselect("Select Region", regions, default=regions)
selected_categories = st.sidebar.multiselect("Select Category", categories, default=categories)

filtered_df = df[
    (df["region"].isin(selected_regions)) &
    (df["category"].isin(selected_categories))
]

kpis = calculate_kpis(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Avg Order Value", f"₩{kpis['Average Order Value']:,.0f}")
col2.metric("Retention Rate", f"{kpis['Customer Retention Rate (%)']}%")
col3.metric("Return Rate", f"{kpis['Return Rate (%)']}%")
col4.metric("Avg Delivery", f"{kpis['Average Delivery Time (Days)']} days")
col5.metric("Satisfaction", f"{kpis['Customer Satisfaction Score']}/5")

monthly = filtered_df.groupby("month", as_index=False)["total_amount"].sum()
fig = px.line(monthly, x="month", y="total_amount", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Sales by Category")
category_sales = filtered_df.groupby("category", as_index=False)["total_amount"].sum()
fig2 = px.bar(category_sales, x="category", y="total_amount")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("SQL Insights")
results = run_sql_insights()
for title, result in results.items():
    st.write(title)
    st.dataframe(result)

st.subheader("API Integration")
try:
    response = requests.get("https://api.exchangerate.host/latest?base=KRW&symbols=USD,PKR", timeout=10)
    st.json(response.json())
except Exception as error:
    st.error(error)

if st.button("Generate Automated Report"):
    report_path = generate_report()
    st.success(f"Report Generated: {report_path.name}")
