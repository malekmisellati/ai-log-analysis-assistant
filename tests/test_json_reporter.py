import os
import json

from reporter.json_reporter import generate_json_report


def test_generate_json_report(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    analysis = {
        "total_entries": 5,
        "severity_counts": {
            "ERROR": 3,
            "INFO": 2
        },
        "recurring_errors": {
            "Database timeout": 2
        },
        "high_severity_count": 3,
        "most_frequent_error": "Database timeout",
        "severity_insight": "A small number of high-severity issues detected.",
        "invalid_entries": 1
    }

    report_path = generate_json_report(analysis)

    assert os.path.normpath(report_path) == os.path.normpath(
    "reports/analysis_report.json"
)

    with open(report_path, "r", encoding="utf-8") as file:
        report = json.load(file)

    assert "generated_at" in report
    assert report["analysis"]["total_entries"] == 5
    assert report["analysis"]["high_severity_count"] == 3
    assert report["analysis"]["invalid_entries"] == 1
    assert report["analysis"]["most_frequent_error"] == "Database timeout"
