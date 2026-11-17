
import sqlite3
import os


DATABASE_PATH = os.path.join(
    "data",
    "logs.db"
)


def get_connection():

    os.makedirs("data", exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_logs
            ON logs (timestamp, level, message)
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_entries INTEGER NOT NULL,
                severity_counts TEXT NOT NULL,
                recurring_errors TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    finally:
        connection.close()

def save_logs(logs):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.executemany(
            """
            INSERT OR IGNORE INTO logs (timestamp, level, message)
            VALUES (?, ?, ?)
            """,
            [
                (
                    log["timestamp"],
                    log["level"],
                    log["message"]
                )
                for log in logs
            ]
        )

        connection.commit()

    finally:
        connection.close()


def save_analysis(analysis):

    import json

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO analysis_results (
                total_entries,
                severity_counts,
                recurring_errors
            )
            VALUES (?, ?, ?)
            """,
            (
                analysis["total_entries"],
                json.dumps(analysis["severity_counts"]),
                json.dumps(analysis["recurring_errors"])
            )
        )

        connection.commit()

    finally:
        connection.close()

def get_logs():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT timestamp, level, message
            FROM logs
            ORDER BY timestamp
        """)

        rows = cursor.fetchall()

        return [
            {
                "timestamp": row[0],
                "level": row[1],
                "message": row[2]
            }
            for row in rows
        ]

    finally:
        connection.close()

def get_analysis_results():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT total_entries, severity_counts, recurring_errors, created_at
            FROM analysis_results
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        return rows

    finally:
        connection.close()