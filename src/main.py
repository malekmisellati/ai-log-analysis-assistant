
import logging
import os

from parser.log_parser import parse_log_file
from analyzer.log_analyzer import analyze_logs
from analyzer.ai_analyzer import analyze_with_ai

from database.database import (
    initialize_database,
    save_logs,
    save_analysis,
    get_logs,
    get_analysis_results
)

from reporter.json_reporter import generate_json_report


# Ensure the reports directory exists
os.makedirs("reports", exist_ok=True)


# Configure application logging
logging.basicConfig(
    filename="reports/application.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    try:
        # Initialize the database
        initialize_database()

        logging.info("Database initialized successfully.")

        # Read and parse the log file
        logs, invalid_entries = parse_log_file(
            "sample_logs/application.log"
        )

        logging.info(
            "Log parsing completed. Valid entries: %s, Invalid entries: %s",
            len(logs),
            invalid_entries
        )

        if invalid_entries > 0:
            logging.warning(
                "%s invalid log entries were skipped.",
                invalid_entries
            )

        # Stop if the log file could not be found
        if not logs and invalid_entries == 0:
            logging.error("No valid log file was found.")
            print("Application stopped: No valid log file was found.")
            return

        # Analyze the parsed entries
        analysis = analyze_logs(logs, invalid_entries)

        # Save logs and analysis to SQLite
        save_logs(logs)
        save_analysis(analysis)

        logging.info("Analysis results saved to database.")

        # Generate JSON analysis report
        report_path = generate_json_report(analysis)

        logging.info("JSON report generated: %s", report_path)

        # Display the analysis report
        print("\n--- Log Analysis Report ---\n")

        print(f"Total entries: {analysis['total_entries']}")
        print(f"Invalid log entries: {invalid_entries}")
        print(f"High-severity events: {analysis['high_severity_count']}")
        print(f"Severity Insight: {analysis['severity_insight']}")

        print("\nSeverity Breakdown:")

        for level, count in analysis["severity_counts"].items():
            print(f"{level}: {count}")

        print("\nRecurring Errors:")

        for message, count in analysis["recurring_errors"].items():
            print(f"{message}: {count} occurrences")

        print(f"\nMost frequent error: {analysis['most_frequent_error']}")

        print(f"\nJSON report saved to: {report_path}")

        # Retrieve stored records from SQLite
        stored_logs = get_logs()
        stored_analysis = get_analysis_results()

        print(f"\nRetrieved log records: {len(stored_logs)}")
        print(f"Retrieved analysis records: {len(stored_analysis)}")

        # Generate optional AI analysis
        try:
            ai_insights = analyze_with_ai(analysis)

            # Save AI insights to a text report
            ai_report_path = os.path.join(
                "reports",
                "ai_analysis.txt"
            )

            with open(
                ai_report_path,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(ai_insights)

            logging.info("AI analysis completed successfully.")

            print("\n--- AI Analysis ---\n")
            print(ai_insights)

            print(f"\nAI report saved to: {ai_report_path}")

        except ValueError as error:
            logging.warning("AI analysis skipped: %s", error)
            print(f"\nAI analysis skipped: {error}")

        except Exception:
            logging.exception("AI analysis failed.")
            print("\nAI analysis unavailable. Standard analysis completed.")

        print("\nLog analysis completed successfully.")

    except Exception:
        logging.exception("Application encountered an unexpected error.")
        print("\nApplication encountered an unexpected error.")


if __name__ == "__main__":
    main()
