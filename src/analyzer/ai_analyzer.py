import os
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


def analyze_with_ai(analysis):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your_api_key_here":
        raise ValueError("OpenAI API key is missing.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are an application log analysis assistant.

    Review the following log analysis results:

    Total entries: {analysis['total_entries']}

    Severity counts: {analysis['severity_counts']}

    Recurring errors: {analysis['recurring_errors']}

    High-severity events: {analysis['high_severity_count']}

    Most frequent error: {analysis['most_frequent_error']}

    Severity insight: {analysis['severity_insight']}

    Provide:
    1. An explanation of the recurring errors.
    2. Possible causes of these errors.
    3. Recommended troubleshooting steps.
    4. An overall assessment of application health.

    Base your response only on the information provided.
    Clearly distinguish possible causes from confirmed facts.
    """

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    return response.output_text