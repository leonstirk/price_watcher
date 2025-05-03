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
- [x] Convert `watchlist.py` to `watchlist.json`
- [x] Build CRUD utilities:
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



Regroup 2025/05/03

🧱 1. System Architecture Overview

[User/CLI] ───▶ [Search module] ───▶ [Watchlist (JSON store)]
                                      ▲         │
                                      │         ▼
                          [Scheduled Lambda (Dockerized)]
                                      │
                                      ▼
                              [New World API]
                                      │
                              [Alert Triggers]
                                      ▼
                                [AWS SES Email]

🧩 2. Key Functional Modules
Module	Responsibility
token_extractor	Get bearer token using Playwright (with cache fallback)
token_cache	Handle save/load of token and expiry info
api_client	Encapsulate New World API access (search, lookup by ID, etc.)
watchlist_manager	CRUD ops on a persistent watchlist.json
watcher.py	Periodically check watched items for trigger conditions
emailer.py	Format and send aggregated alerts via AWS SES
lambda_function.py	Entry point for Lambda to run run_daily_check()
watchlist_cli.py	UX path to add/search/remove items via CLI (for manual testing/dev)
🔄 3. Current Concerns to Revisit
Concern	Next Design Step
❗ Store name/ID mismatch	Decide if store name should ever be stored — or only the ID
❗ Too many emails	Refactor watcher.py to aggregate alerts and send one email per run
❗ Docker context issues	Ensure relative imports work from /app/src inside container
❗ Watchlist format	Standardize the structure: include product_id, friendly_name, store_id, etc.
❗ Config security	All secrets and tokens should be out of versioned code and into .env or AWS Param Store
❗ Testing vs Deployment behavior	Decide how to cleanly switch between CLI and Lambda execution (e.g. a main.py dev script?)
🔭 4. Future Features to Plan For
Feature	Notes
✅ Auto bearer token refresh	Done via token_cache.py
🛠️ Historical price storage	Store snapshots for pricing trends and smarter alerting
👤 Multi-user support	Watchlist becomes user-scoped, emails go to user emails
🌐 Web frontend	Would call backend or manipulate watchlist.json via API
🧪 Unit/integration tests	Test CLI commands, token lifecycle, parsing logic
⏱️ Resilient scheduling	Lambda + EventBridge or CloudWatch rules
🧰 Admin tools (flush cache, dump alerts, rebuild watchlist)	Helpful for maintenance
🧭 What to do next

Would you like to:

    Diagram the final app structure with folders/modules?

    Refactor some logic now (e.g. watcher/email bundling)?

    Draft a README or architecture doc?

    Split dev/prod execution paths?

    Or just start with some specific design questions?

Let’s make the moving parts manageable again. What's your preferred next step?




🧭 High-Level System Goals

You're describing an app that supports:

    🧑 Multiple users

    📦 Watchlists linked to user accounts

    🏪 Geographically relevant store scoping

    💌 Alerting when user-tracked products go on special

    🖥 Frontend UI for searching, adding/removing products, managing stores

    💰 Optional billing tier support (e.g., free up to X products)

Let’s walk through the core parts.
🧱 System Architecture: Scalable Design

Here’s what a future-proof system might look like:

          [User Browser]
               │
       ┌───────▼────────┐
       │    Web Frontend (React/Vue/11ty+JS)    │
       └───────┬────────┘
               │  (REST/API)
          ┌────▼────────────┐
          │     Backend (API Gateway + Lambda)  │
          └────┬────────────┘
               │
       ┌───────▼──────────────┐
       │     AWS DynamoDB or RDS (User, Product, Watchlist DBs)
       └───────┬──────────────┘
               │
      ┌────────▼──────────────┐
      │ S3 (Static files + dynamic watchlist json, tokens etc.)
      └────────┬──────────────┘
               │
   Scheduled ──▼── Lambda (Docker) ──▶ [New World API]
               │
               └────▶ SES Alerts to Users

🧩 Key Design Building Blocks
1. User System

    Sign up / log in (AWS Cognito for low-lift auth)

    Email address is verified (good for SES deliverability)

    Each user has:

        user_id (UUID)

        store preferences (by ID or lat/lon radius)

        watchlist (linked by product ID)

2. Product Catalog DB

    Maintains:

        product_id, name, brand, unit, categories

        price history (aggregated by scraper logic)

        frequency/pattern of specials (could calculate avg. discount, time since last special)

    These are not user-specific, so they live in a shared DB.

3. Watchlist Table

    Each record links:

        user_id

        product_id

        target_price, min_discount, etc.

So when the watcher Lambda runs, it does:

    Fetch all user watchlist entries

    For each product, pull latest price from API

    Check if any entry triggers an alert

    Bundle alerts per user

    Send SES email

🧰 Deployment & Data Interaction

You're absolutely right — you should not rebuild Docker images every time the data changes.
✅ Instead:

    Your Lambda image stays constant, and

    It reads dynamic inputs (like watchlist JSONs or DB rows) from:

        S3 (for simple setups)

        DynamoDB or RDS (for relational or large setups)

    This means the watchlist, user configs, store lists, etc., live in the cloud and are read live at runtime.

You could even use a "one file per user" model to simplify dynamic loading (e.g., watchlists/user_1234.json in S3).
🛒 Re: Which Products Are Worth Watching

This is an analytics problem.

You'll want a crawler/scraper running separately from the alerting logic that:

    Collects all product data across all stores on a daily/weekly basis

    Saves to a historical dataset (S3 or DB)

    Computes:

        Discount frequency

        Average discount depth

        Seasonality/patterns

You can then surface this in your frontend:

    “This product is usually on special every 3 weeks with an average 25% discount.”

🧩 Design Choices to Decide Next

Here are some key decision forks you’ll want to pick a path for:
Feature	Recommendation
Auth	Use AWS Cognito or Clerk/Supabase Auth
Watchlist DB	Start with JSON in S3; move to DynamoDB if scaling
Deployment	Containerized Lambda (EventBridge for scheduling)
Frontend	Start with static site + JS hitting API Gateway
Product DB	One product cache file per day or per store in S3
✅ Suggested Next Steps

    Move watchlist JSONs to S3: One per user

    Modify watcher.py to read all user watchlists from S3

    Write a products/ data structure in S3 for analytics

    Map out database schema if you go RDS/Dynamo later

    Design how the frontend will interface with the backend:

        Search products

        Add to watchlist

        View/edit alerts

    Add an admin CLI for dumping data, rebuilding product cache, etc.

Would you like help:

    Sketching a concrete folder + S3 layout for step 1?

    Writing code to load multiple watchlists from S3?

    Planning for a frontend API layer?

    Or drawing a full deployment diagram?

Let’s tackle this iteratively.