import json
import os
from datetime import datetime


def generate_json_report(analysis):

    os.makedirs("reports", exist_ok=True)

    report = {
        "generated_at": datetime.now().isoformat(),
        "analysis": analysis
    }

    report_path = os.path.join(
        "reports",
        "analysis_report.json"
    )

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4
        )

    return report_path