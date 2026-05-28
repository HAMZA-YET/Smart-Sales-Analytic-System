import sqlite3
import pandas as pd
from pathlib import Path
import random
import csv
import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "sales_data.csv"
DB_PATH = BASE_DIR / "business_sales.db"

def generate_sample_data():
    DATA_DIR.mkdir(exist_ok=True)

    customers = [
        ("C001", "Ali Khan", "Seoul", "Student"),
        ("C002", "Sara Lee", "Busan", "Office Worker"),
        ("C003", "Ahmed Raza", "Incheon", "Student"),
        ("C004", "Minji Kim", "Daegu", "Office Worker"),
        ("C005", "Fatima Noor", "Daejeon", "Business Owner"),
        ("C006", "Jisoo Park", "Seoul", "Student"),
        ("C007", "Usman Malik", "Gwangju", "Office Worker"),
        ("C008", "Hana Choi", "Suwon", "Business Owner"),
    ]

    products = [
        ("P001", "Laptop Bag", "Accessories", 25000),
        ("P002", "Wireless Mouse", "Electronics", 18000),
        ("P003", "Notebook Set", "Stationery", 8000),
        ("P004", "USB-C Cable", "Electronics", 12000),
        ("P005", "Desk Lamp", "Home Office", 30000),
        ("P006", "Water Bottle", "Lifestyle", 15000),
    ]

    random.seed(7)
    start_date = datetime.date(2026, 1, 1)
    rows = []

    for i in range(1, 181):
        customer = random.choice(customers)
        product = random.choice(products)
        order_date = start_date + datetime.timedelta(days=random.randint(0, 130))
        quantity = random.randint(1, 5)
        rating = random.choice([3, 4, 4, 4, 5, 5])
        delivery_days = random.randint(1, 8)
        returned = random.choice([0, 0, 0, 0, 1])

        rows.append([
            f"O{i:04d}", order_date.isoformat(), customer[0], customer[1],
            customer[2], customer[3], product[0], product[1], product[2],
            quantity, product[3], rating, delivery_days, returned
        ])

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "order_id", "order_date", "customer_id", "customer_name", "region",
            "customer_type", "product_id", "product_name", "category", "quantity",
            "unit_price", "customer_rating", "delivery_days", "returned"
        ])
        writer.writerows(rows)

def create_database():
    if not CSV_PATH.exists():
        generate_sample_data()

    df = pd.read_csv(CSV_PATH)
    df["total_amount"] = df["quantity"] * df["unit_price"]

    conn = sqlite3.connect(DB_PATH)

    customers = df[["customer_id", "customer_name", "region", "customer_type"]].drop_duplicates()
    products = df[["product_id", "product_name", "category", "unit_price"]].drop_duplicates()
    orders = df[[
        "order_id", "order_date", "customer_id", "product_id", "quantity",
        "unit_price", "total_amount", "customer_rating", "delivery_days", "returned"
    ]]

    customers.to_sql("customers", conn, if_exists="replace", index=False)
    products.to_sql("products", conn, if_exists="replace", index=False)
    orders.to_sql("orders", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
