# Smart Sales Analytics & Automation System

## Project Title
Smart Sales Analytics & Automation System using Python, SQLite, Streamlit, and API Integration

## What this system does
This mini business system analyzes sales data, stores it in an SQLite database, calculates business KPIs, displays a dashboard, runs SQL insights, integrates an external API, and generates automated reports.

## How to run

### 1. Install requirements
```bash
pip install -r requirements.txt
```

### 2. Create database
```bash
python database_setup.py
```

### 3. Run dashboard
```bash
streamlit run app.py
```

## Important project parts
- `data/sales_data.csv` = sample business dataset
- `database_setup.py` = creates SQLite database
- `analytics.py` = KPI and analysis functions
- `automation.py` = report generator
- `app.py` = Streamlit dashboard
- `business_sales.db` = generated database after setup
- `reports/` = generated reports

## KPIs used
The assignment says not to use revenue, cost, or profit as the 4 main KPIs. This project uses:
1. Average Order Value
2. Customer Retention Rate
3. Return Rate
4. Average Delivery Time
5. Customer Satisfaction Score

Revenue is shown only as supporting business information, not as one of the main four required KPIs.
