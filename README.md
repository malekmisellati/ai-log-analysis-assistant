
# AI Log Analysis Assistant

## Overview

A Python-based application that analyzes application log files, identifies recurring errors, tracks severity levels, and generates structured reports.

The application uses rule-based analysis by default and supports optional OpenAI integration to provide AI-generated explanations, possible causes, and troubleshooting recommendations.

## Features

- Parse application log files.
- Validate log entries and identify invalid records.
- Categorize logs by severity: INFO, WARNING, ERROR, and CRITICAL.
- Identify recurring errors and the most frequent error.
- Generate severity insights.
- Store log records and analysis results in SQLite.
- Prevent duplicate log records.
- Generate structured JSON reports.
- Record application events using Python logging.
- Optional OpenAI integration for AI-powered error explanations and troubleshooting recommendations.
- Automated testing with pytest.

## Technologies

- Python
- OpenAI API
- SQLite
- JSON
- Regular Expressions
- Python Logging
- python-dotenv
- pytest
- Git and GitHub

## Project Structure

```text
ai-log-analysis-assistant/
├── src/
│   ├── analyzer/
│   │   ├── ai_analyzer.py
│   │   └── log_analyzer.py
│   ├── database/
│   │   └── database.py
│   ├── parser/
│   │   └── log_parser.py
│   ├── reporter/
│   │   └── json_reporter.py
│   └── main.py
├── tests/
├── sample_logs/
│   └── application.log
├── reports/
├── .env.example
├── .gitignore
├── pytest.ini
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-log-analysis-assistant
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment.

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application from the project root:

```bash
python src/main.py
```

The application reads:

```text
sample_logs/application.log
```

It then parses and analyzes the entries, saves records to SQLite, and generates a JSON report.

Generated files include:

- `data/logs.db` — SQLite database.
- `reports/analysis_report.json` — Structured analysis results.
- `reports/application.log` — Application execution logs.

## Optional AI Integration

The application supports optional OpenAI integration.

Without an API key, the application performs its standard rule-based analysis.

To enable AI functionality:

1. Create an OpenAI API key.
2. Copy `.env.example` to a new file named `.env`.
3. Replace the placeholder with your API key:

```text
OPENAI_API_KEY=your_actual_api_key
```

4. Run the application:

```bash
python src/main.py
```

When configured correctly, the application can additionally generate:

- Explanations of recurring errors.
- Possible causes of detected issues.
- Recommended troubleshooting steps.
- An overall assessment of application health.

AI-generated insights are saved to:

```text
reports/ai_analysis.txt
```

An OpenAI API account and applicable API billing are required for this optional functionality.

Never commit your `.env` file or expose your API key.

## Running Tests

Run the complete test suite:

```bash
pytest -v
```

The project includes automated tests for:

- Log parsing and validation.
- Severity analysis and recurring error detection.
- Database initialization, storage, retrieval, and duplicate prevention.
- JSON report generation.
- AI analyzer behavior using mocked API responses.

## Current Test Results

22 automated tests passing.

## License

This project is available for educational and portfolio purposes.
