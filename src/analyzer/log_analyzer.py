
from collections import Counter


def analyze_logs(logs, invalid_entries=0):

    # Count entries by severity level
    severity_counts = Counter(
        log["level"] for log in logs
    )

    # Count occurrences of each log message
    message_counts = Counter(
        log["message"] for log in logs
    )

    # Identify messages that appear more than once
    recurring_errors = {
        message: count
        for message, count in message_counts.items()
        if count > 1
        and any(
            log["message"] == message
            and log["level"] in ("ERROR", "CRITICAL")
            for log in logs
        )
    }

    # Identify the most frequent recurring error
    most_frequent_error = None

    if recurring_errors:
        most_frequent_error = max(
            recurring_errors,
            key=recurring_errors.get
        )

    # Count high-severity events
    high_severity_count = sum(
        1
        for log in logs
        if log["level"] in ("ERROR", "CRITICAL")
    )
        # Generate a severity insight
    if high_severity_count == 0:
        severity_insight = "No high-severity issues detected."

    elif high_severity_count <= 3:
        severity_insight = "A small number of high-severity issues detected."

    else:
        severity_insight = (
            "High number of severe issues detected. "
            "Investigation recommended."
        )

    return {
        "total_entries": len(logs),
        "severity_counts": dict(severity_counts),
        "recurring_errors": recurring_errors,
        "high_severity_count": high_severity_count,
        "most_frequent_error": most_frequent_error,
        "severity_insight": severity_insight,
        "invalid_entries": invalid_entries
    }


    return {
        "total_entries": len(logs),
        "severity_counts": dict(severity_counts),
        "recurring_errors": recurring_errors,
        "high_severity_count": high_severity_count,

    }
