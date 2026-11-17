
import re
from datetime import datetime


# Expected log format:
# 2026-11-17 09:00:01 INFO Application started successfully

LOG_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(INFO|WARNING|ERROR|CRITICAL) "
    r"(.+)$"
)


def parse_log_line(line):

    match = LOG_PATTERN.match(line.strip())

    if not match:
        return None

    timestamp, level, message = match.groups()

    try:
        parsed_timestamp = datetime.strptime(
            timestamp,
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:
        return None

    return {
        "timestamp": parsed_timestamp.isoformat(sep=" "),
        "level": level,
        "message": message
    }


def parse_log_file(file_path):

    parsed_logs = []
    invalid_entries = 0

    try:
        with open(file_path, "r", encoding="utf-8") as file:

            for line in file:

                parsed_entry = parse_log_line(line)

                if parsed_entry is not None:
                    parsed_logs.append(parsed_entry)
                else:
                    invalid_entries += 1

    except FileNotFoundError:
        print(f"Error: Log file not found: {file_path}")

    return parsed_logs, invalid_entries