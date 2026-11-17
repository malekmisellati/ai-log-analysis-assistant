import database.database as db


def test_database_initialization(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(db, "DATABASE_PATH", str(tmp_path / "test.db"))

    db.initialize_database()

    logs = db.get_logs()
    analysis = db.get_analysis_results()

    assert logs == []
    assert analysis == []


def test_save_and_retrieve_logs(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(db, "DATABASE_PATH", str(tmp_path / "test.db"))

    db.initialize_database()

    logs = [
        {
            "timestamp": "2026-11-17 09:00:01",
            "level": "ERROR",
            "message": "Database connection failed"
        }
    ]

    db.save_logs(logs)

    stored_logs = db.get_logs()

    assert len(stored_logs) == 1
    assert stored_logs[0]["level"] == "ERROR"
    assert stored_logs[0]["message"] == "Database connection failed"


def test_duplicate_log_prevention(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(db, "DATABASE_PATH", str(tmp_path / "test.db"))

    db.initialize_database()

    logs = [
        {
            "timestamp": "2026-11-17 09:00:01",
            "level": "ERROR",
            "message": "Database connection failed"
        }
    ]

    db.save_logs(logs)
    db.save_logs(logs)

    stored_logs = db.get_logs()

    assert len(stored_logs) == 1


def test_save_and_retrieve_analysis(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(db, "DATABASE_PATH", str(tmp_path / "test.db"))

    db.initialize_database()

    analysis = {
        "total_entries": 5,
        "severity_counts": {
            "ERROR": 3,
            "INFO": 2
        },
        "recurring_errors": {
            "Database timeout": 2
        }
    }

    db.save_analysis(analysis)

    results = db.get_analysis_results()

    assert len(results) == 1
    assert results[0][0] == 5
    assert '"ERROR": 3' in results[0][1]
    assert "Database timeout" in results[0][2]
