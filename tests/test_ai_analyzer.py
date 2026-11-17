
from unittest.mock import patch

import pytest

from analyzer.ai_analyzer import analyze_with_ai


def sample_analysis():

    return {
        "total_entries": 12,
        "severity_counts": {
            "INFO": 5,
            "WARNING": 2,
            "ERROR": 4,
            "CRITICAL": 1
        },
        "recurring_errors": {
            "Failed to connect to payment service": 2,
            "Database query timeout": 2
        },
        "high_severity_count": 5,
        "most_frequent_error": "Failed to connect to payment service",
        "severity_insight": (
            "High number of severe issues detected. "
            "Investigation recommended."
        ),
        "invalid_entries": 0
    }


def test_missing_api_key(monkeypatch):

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="OpenAI API key is missing"):
        analyze_with_ai(sample_analysis())


def test_placeholder_api_key(monkeypatch):

    monkeypatch.setenv("OPENAI_API_KEY", "your_api_key_here")

    with pytest.raises(ValueError, match="OpenAI API key is missing"):
        analyze_with_ai(sample_analysis())


def test_successful_ai_analysis(monkeypatch):

    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

    with patch("analyzer.ai_analyzer.OpenAI") as mock_openai:

        mock_openai.return_value.responses.create.return_value.output_text = (
            "The application has recurring database and payment errors."
        )

        result = analyze_with_ai(sample_analysis())

        assert result == (
            "The application has recurring database and payment errors."
        )

        mock_openai.assert_called_once_with(api_key="test-api-key")

        mock_openai.return_value.responses.create.assert_called_once()
