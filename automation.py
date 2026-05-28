from pathlib import Path
from datetime import datetime
from analytics import load_sales_data, calculate_kpis

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

def generate_report():
    df = load_sales_data()
    kpis = calculate_kpis(df)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"business_report_{timestamp}.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("SMART SALES ANALYTICS REPORT\n")
        file.write("=" * 50 + "\n\n")

        for name, value in kpis.items():
            file.write(f"{name}: {value}\n")

        file.write("\nRecommendations:\n")
        file.write("- Focus marketing on high-performing regions.\n")
        file.write("- Improve delivery efficiency.\n")
        file.write("- Reward repeat customers.\n")

    return report_path
