from analyzer.log_analyzer import analyze_logs


def sample_logs():

    return [
        {
            "timestamp": "2026-11-17 09:00:01",
            "level": "ERROR",
            "message": "Payment service unavailable"
        },
        {
            "timestamp": "2026-11-17 09:01:01",
            "level": "ERROR",
            "message": "Payment service unavailable"
        },
        {
            "timestamp": "2026-11-17 09:02:01",
            "level": "ERROR",
            "message": "Database timeout"
        },
        {
            "timestamp": "2026-11-17 09:03:01",
            "level": "ERROR",
            "message": "Database timeout"
        },
        {
            "timestamp": "2026-11-17 09:04:01",
            "level": "CRITICAL",
            "message": "Memory limit reached"
        },
        {
            "timestamp": "2026-11-17 09:05:01",
            "level": "INFO",
            "message": "Application started"
        }
    ]


def test_total_entries():

    result = analyze_logs(sample_logs())

    assert result["total_entries"] == 6


def test_severity_counts():

    result = analyze_logs(sample_logs())

    assert result["severity_counts"]["ERROR"] == 4
    assert result["severity_counts"]["CRITICAL"] == 1
    assert result["severity_counts"]["INFO"] == 1


def test_high_severity_count():

    result = analyze_logs(sample_logs())

    assert result["high_severity_count"] == 5


def test_recurring_errors():

    result = analyze_logs(sample_logs())

    assert result["recurring_errors"] == {
        "Payment service unavailable": 2,
        "Database timeout": 2
    }


def test_most_frequent_error():

    result = analyze_logs(sample_logs())

    assert result["most_frequent_error"] == "Payment service unavailable"


def test_severity_insight():

    result = analyze_logs(sample_logs())

    assert result["severity_insight"] == (
        "High number of severe issues detected. "
        "Investigation recommended."
    )


def test_invalid_entry_count():

    result = analyze_logs(sample_logs(), invalid_entries=3)

    assert result["invalid_entries"] == 3


def test_no_high_severity_events():

    logs = [
        {
            "timestamp": "2026-11-17 09:00:01",
            "level": "INFO",
            "message": "Application started"
        }
    ]

    result = analyze_logs(logs)

    assert result["high_severity_count"] == 0
    assert result["severity_insight"] == "No high-severity issues detected."


def test_small_number_of_high_severity_events():

    logs = [
        {
            "timestamp": "2026-11-17 09:00:01",
            "level": "ERROR",
            "message": "Connection failed"
        }
    ]

    result = analyze_logs(logs)

    assert result["severity_insight"] == (
        "A small number of high-severity issues detected."
    )
