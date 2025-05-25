# notify.py
import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def notify_new_shows(message):
    payload = {
        "text": message
    }
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            print(f"Slack notify failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Slack notify error: {e}")

notify_new_shows("Hello, this is a test message from my scraper!")