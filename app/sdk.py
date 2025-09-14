from datetime import datetime

from core.config import WEBHOOK_URL
from schema.fraud_check_schema import FraudCheckRequest


def send_slack_teams_message(fraud_event: FraudCheckRequest) -> None:
    import requests
    import json

    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": ":rotating_light: FRAUD LOGIN DETECTED!"}
            },
            {"type": "divider"},
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*User ID:*\n{fraud_event.user_id}"},
                    {"type": "mrkdwn", "text": f"*Login Time:*\n{fraud_event.login_at}"},
                    {"type": "mrkdwn", "text": f"*IP Country:*\n{fraud_event.ip_country}"},
                    {"type": "mrkdwn", "text": f"*Timezone:*\n{fraud_event.ip_timezone}"}
                ]
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Immediate investigation recommended! :mag: \n<http://localhost:5173/ Fraud Login Dashboard>"
                }
            },
            {"type": "context",
             "elements": [
                 {"type": "mrkdwn",
                  "text": f"Event triggered by Fraud Detection System at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
             ]}
        ]
    }

    # Send POST request
    response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
