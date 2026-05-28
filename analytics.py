import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "business_sales.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def load_sales_data():
    query = """
    SELECT 
        o.order_id,
        o.order_date,
        c.customer_id,
        c.customer_name,
        c.region,
        c.customer_type,
        p.product_id,
        p.product_name,
        p.category,
        o.quantity,
        o.unit_price,
        o.total_amount,
        o.customer_rating,
        o.delivery_days,
        o.returned
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products p ON o.product_id = p.product_id
    """

    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    return df

def calculate_kpis(df):
    total_orders = len(df)
    unique_customers = df["customer_id"].nunique()

    repeat_customers = df.groupby("customer_id")["order_id"].count()
    repeat_customer_count = (repeat_customers > 1).sum()

    average_order_value = df["total_amount"].mean()
    customer_retention_rate = (repeat_customer_count / unique_customers) * 100
    return_rate = (df["returned"].sum() / total_orders) * 100
    average_delivery_time = df["delivery_days"].mean()
    satisfaction_score = df["customer_rating"].mean()

    return {
        "Average Order Value": round(average_order_value, 2),
        "Customer Retention Rate (%)": round(customer_retention_rate, 2),
        "Return Rate (%)": round(return_rate, 2),
        "Average Delivery Time (Days)": round(average_delivery_time, 2),
        "Customer Satisfaction Score": round(satisfaction_score, 2)
    }

def run_sql_insights():
    queries = {
        "Top Products": """
            SELECT p.product_name, SUM(o.quantity) AS total_quantity
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            GROUP BY p.product_name
            ORDER BY total_quantity DESC
        """,

        "Sales by Region": """
            SELECT c.region, SUM(o.total_amount) AS total_sales
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.region
            ORDER BY total_sales DESC
        """
    }

    results = {}

    with get_connection() as conn:
        for title, query in queries.items():
            results[title] = pd.read_sql_query(query, conn)

    return results
