# 💼 price_watcher – Project Roadmap

This document outlines the current state, completed work, and future roadmap for the `price_watcher` project: a daily product alert tool built on AWS using product data from New World’s API.

---

## ✅ Phase 0: MVP Completed

The core functionality of the price watcher app is complete:

- [x] Daily watcher script working
- [x] API calls to New World backend using productId
- [x] Email alerts sent via AWS SES
- [x] Watchlist tracks productId and optional price/discount rules

### 🏗 Basic Architecture
- Python script (CLI + planned Lambda deployment)
- API client with bearer token (currently manual)
- Watchlist (hardcoded in Python)
- Alert trigger logic
- SES integration for email

---

## 💪 Phase 1: Codebase Stability & Config Management

### Config & Secrets
- [x] Centralize bearer token, SES emails, region into `config.py`
- [ ] Move token handling to secure source (AWS SSM, Secrets Manager)
- [x] Add `.gitignore` + `config_template.py`
- [ ] Add `.env` support or `os.getenv()` wrappers

### Requirements & Deployment Prep
- [x] Isolate virtual environment
- [x] Install `boto3`
- [x] Maintain `requirements.txt`
- [ ] Confirm minimum Lambda packaging for deployment

### Robustness
- [ ] Retry logic for network/API errors
- [ ] Exception handling for missing or malformed fields
- [ ] Basic logging

---

## 💪 Phase 2: Watchlist Expansion & Data Logging

### JSON-based Watchlist
- [ ] Convert `watchlist.py` to `watchlist.json`
- [ ] Build CRUD utilities:
  - `add_to_watchlist()`
  - `remove_from_watchlist()`
  - `update_watchlist()`
  - `get_watchlist()`

### Historical Price Logging
- [ ] Log daily price/promotions to local files or S3
- [ ] Track longest observed promotions
- [ ] Build groundwork for promotion intelligence

---

## 🥪 Phase 3: Search Interface & Workflow

### Friendly Search Workflow
- [ ] Helper function for `search_products(query)`
- [ ] Print search results nicely in terminal
- [ ] Add option to select a product and add to watchlist
- [ ] Build CLI-based watcher interface

### Documentation & Transparency
- [ ] README.md explaining:
  - Setup, dependencies
  - How to run manually
  - How to use search and add to watchlist
- [ ] Architecture diagram
- [ ] Code comments + inline docstrings

---

## 👥 Phase 4: Multi-User & Frontend Planning

### Multi-User Model
- [ ] Define user account system (Cognito, static user list, etc.)
- [ ] Separate watchlists per user (DynamoDB or user-specific JSON)

### Web UI / Admin Panel
- [ ] Frontend framework decision (React, Streamlit, etc.)
- [ ] Manual test UI (search, alerts, watchlist editing)
- [ ] Authentication layer

---

## 🔍 Suggested Future Improvements

| Feature | Benefit |
|--------|---------|
| 📊 Price history charting | Sparkline-style mini trends in emails |
| 🗕 Promotion duration tracking | Highlight "rarely on sale" items |
| ☁️ DynamoDB-based watchlist | Scalability + persistence |
| 🔐 AWS Secrets Manager or SSM | Secure token and email configs |
| 🛡 Retry logic with exponential backoff | Improve reliability |
| 📦 Package as `pricewatcher/` module | Testability + CLI interfaces |

---

This roadmap should be reviewed after any major structural changes, such as moving to a frontend or replacing the data source.




________________________________________________________________________________________________
🕰️ Phase 4: Scheduler & Email (Automation)

    Automate daily check and alert

Tasks

Create EventBridge rule to trigger Lambda daily

Set up SES (sandbox or production)

Verify email identity

    Configure email body (include scraped info, product name, price)

📝 Commit: "Automated daily scrape and email alert via EventBridge"
📦 Phase 5: Refactor, Logging & Optional Features

    Make it robust and extensible

Tasks

Add logging

Store historical prices (e.g. in S3 or log file)

Handle exceptions and HTTP errors gracefully

    Optionally scrape multiple products

📝 Commit: "Add logging and error handling for robustness"
✍️ Phase 6: Documentation & Blog Post

GitHub README

Clear install/deploy instructions

Diagram

    How to customize for another site

Blog Post Ideas


    How to use AWS Lambda & EventBridge for zero-cost automation

    Lessons learned (e.g., HTML parsing quirks)

📝 Final Commit: "Add full README and deployment instructions"


✅ Current State Summary

    ✅ MVP complete: watcher script, product-by-ID lookups, AWS SES email alerts

    ✅ Manual config and watchlist working

    ❌ Bearer token hardcoded (not sustainable)

    ❌ No structured search → watchlist pipeline

    ❌ No frontend / multi-user support yet

    ❌ Minimal documentation and no persistent storage

📋 Updated To-Do / Roadmap
🧱 Phase 1: Codebase Structure & Robustness

Bearer Token Handling

    Investigate how the frontend gets the token (e.g., guest session or auth flow)

    Implement token fetching automatically before API requests

Modular Config

    Move all secrets (token, SES addresses, region, store name) into src/config.py

    Create src/config_template.py and add src/config.py to .gitignore

Requirements Management

    Freeze requirements.txt for reproducibility

    Environment-based control

        Add .env support or use os.getenv() for deployment flexibility

📚 Phase 2: Documentation

README.md

    What the app does

    How to run it locally

    What the dependencies are

Architecture Diagram

    EventBridge → Lambda → API call → SES → User

Workflow Doc:

    How to go from "search term" → "watchlisted product"

    Comments and inline docstrings in all key modules

🧠 Phase 3: Feature Enhancements & Stability

Search Workflow

    Create CLI or Python helper function for search_products(query) to inspect search results

    Allow user to select from matched products and auto-populate watchlist entries

Watchlist Management

    Convert watchlist.py to watchlist.json

    Build CRUD functions:

        add_to_watchlist(product_id, friendly_name, target_price)

        remove_from_watchlist(product_id)

        get_watchlist()

        update_watchlist(product_id, field, value)

    Write changes to disk

    Historical Price Logging

        Save daily product snapshots to S3 or local storage (for building future logic around "good" discounts)

🌍 Phase 4: Web UI Planning & Multi-User Design

Define User Auth Model

    Will users log in via Cognito? GitHub? Email links?

Define Account Isolation

    Where does each user's config/watchlist live? S3? DynamoDB?

Frontend Stack Decision

    React/Tailwind + API Gateway backend?

    Or use something simpler like Streamlit for internal use?

    Admin Panel for Email Testing / Triggering Watcher

        Manual trigger to simulate daily run, view alerts

🧠 Suggestions You May Not Have Considered
Idea	Value
📊 Price history charting	With daily logs, you could create simple Sparkline plots for alert emails
📅 Promotion duration tracking	Track how long each product has been on promo
☁️ Use DynamoDB for persistent watchlist storage	Easier scaling + multi-user support later
🔐 Use AWS Secrets Manager or SSM Parameter Store	To store Bearer tokens or SES sender info securely
🛡 Retry logic for API calls	Especially helpful once token fetching is automated
📦 Package as a Python module (pricewatcher/)	Easier testing, importing, and future pip-style usage