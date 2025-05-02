import boto3
from config import SENDER, RECIPIENT, REGION

def format_alert_email(alerts: list[dict]) -> str:
    lines = ["The following products are on promotion:\n"]
    for alert in alerts:
        line = (
            f"- {alert['friendly_name']}: "
            f"Now ${alert['promo_price']:.2f} "
            f"(was ${alert['regular_price']:.2f}, "
            f"{alert['discount_percent']:.1f}% off)"
        )
        lines.append(line)
    return "\n".join(lines)

def send_alert_email(alerts: list[dict]):
    if not alerts:
        print("No alerts to send.")
        return

    subject = "🛒 NewWorld Specials Alert"
    body_text = format_alert_email(alerts)

    client = boto3.client("ses", region_name=REGION)

    try:
        response = client.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [RECIPIENT]},
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Text": {"Data": body_text}
                }
            }
        )
        print(f"✅ Alert email sent! Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
