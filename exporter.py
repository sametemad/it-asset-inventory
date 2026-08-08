import csv
import json
import os
from datetime import datetime

from system_info import get_system_info
from health_check import evaluate_health


REPORTS_DIR = "reports"


def ensure_reports_folder():
    os.makedirs(REPORTS_DIR, exist_ok=True)


def build_report():
    system_data = get_system_info()
    health_data = evaluate_health(system_data)

    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system": system_data,
        "health": health_data,
    }

    return report


def export_json():
    ensure_reports_folder()

    report = build_report()

    filename = os.path.join(
        REPORTS_DIR,
        f"asset_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return filename


def export_csv():
    ensure_reports_folder()

    report = build_report()

    filename = os.path.join(
        REPORTS_DIR,
        f"asset_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    system_data = report["system"]
    health_data = report["health"]

    row = {
        "generated_at": report["generated_at"],
        **system_data,
        "health_status": health_data["status"],
        "health_alerts": " | ".join(health_data["alerts"]),
    }

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)

    return filename


if __name__ == "__main__":
    json_file = export_json()
    csv_file = export_csv()

    print("\n=== EXPORT COMPLETE ===")
    print(f"JSON: {json_file}")
    print(f"CSV : {csv_file}")