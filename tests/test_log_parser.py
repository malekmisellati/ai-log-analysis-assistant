from parser.log_parser import parse_log_line, parse_log_file


def test_parse_valid_log_line():

    line = "2026-11-17 09:00:01 INFO Application started successfully"

    result = parse_log_line(line)

    assert result is not None
    assert result["timestamp"] == "2026-11-17 09:00:01"
    assert result["level"] == "INFO"
    assert result["message"] == "Application started successfully"


def test_parse_invalid_log_line():

    line = "INVALID LOG ENTRY"

    result = parse_log_line(line)

    assert result is None


def test_parse_invalid_timestamp():

    line = "2026-99-99 09:00:01 ERROR Invalid timestamp"

    result = parse_log_line(line)

    assert result is None


def test_parse_log_file(tmp_path):

    log_file = tmp_path / "test.log"

    log_file.write_text(
        "2026-11-17 09:00:01 INFO Application started\n"
        "INVALID LOG ENTRY\n",
        encoding="utf-8"
    )

    logs, invalid_entries = parse_log_file(log_file)

    assert len(logs) == 1
    assert invalid_entries == 1


def test_missing_log_file(tmp_path, capsys):

    missing_file = tmp_path / "missing.log"

    logs, invalid_entries = parse_log_file(missing_file)

    captured = capsys.readouterr()

    assert logs == []
    assert invalid_entries == 0
    assert "Log file not found" in captured.out
