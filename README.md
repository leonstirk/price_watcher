# 🛒 Price Watcher

A lightweight AWS-based scraper that checks a grocery website daily for price changes and emails an alert if a product goes on special.

## 🧱 Architecture

- **EventBridge**: Triggers the Lambda function daily
- **Lambda**: Scrapes website and checks product price
- **SES**: Sends alert email if price condition is met

## 🚀 Features

- No API access needed
- Zero ongoing compute cost (fully within AWS free tier)
- Easy to adapt to other products or websites

## 📁 Project Structure

price_watcher/
|-- src/                 # Lambda function logic
|     `-- lambda_function.py
|-- infra/               # Infrastructure as code (e.g., SAM or Terraform files)
|-- requirements.txt     # Python dependencies
|-- README.md            # Project documentation
`-- .gitignore           # Files and folders to exclude from Git

## 🔜 Upcoming

- [ ] Scraping logic
- [ ] Lambda setup
- [ ] Daily scheduling via EventBridge
- [ ] SES alerts
- [ ] Historical price tracking
