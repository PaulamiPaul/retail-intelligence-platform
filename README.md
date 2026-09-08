# Retail Intelligence Platform

An AI-powered retail analytics platform built on the Olist Brazilian E-commerce dataset — combining data cleaning, a cloud PostgreSQL database, a natural-language AI agent, and a live interactive dashboard.

**Live app:** https://retail-intelligence-platform-xt9bv9idmgsh9qp9zjqrlg.streamlit.app

## Project Overview
End-to-end retail analytics platform covering data exploration, a cleaned data pipeline loaded into a cloud database, an AI agent that answers plain-English business questions via generated SQL, and a public interactive dashboard.

## Dataset
Olist Brazilian E-commerce Public Dataset — 99,441 orders across 8 relational tables.
Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## Tech Stack
- **Language/Libraries:** Python, pandas, SQLAlchemy, Plotly
- **Database:** Neon (serverless PostgreSQL)
- **AI Agent:** Groq API (`openai/gpt-oss-120b`) for natural-language-to-SQL
- **Dashboard:** Streamlit, deployed on Streamlit Cloud
- **Version control:** Git + GitHub

## Phases
- **Phase 1 ✅ Data Exploration** — Cleaned and explored 8 raw CSVs; identified key trends (top revenue categories, delivery timelines, review patterns)
- **Phase 2 ✅ Data Pipeline** — Cleaned and merged all 8 tables into a 114,092-row master dataset; loaded into Neon PostgreSQL
- **Phase 3 ✅ AI Agent** — Built a natural-language-to-SQL agent using the Groq API; takes a plain English business question, generates SQL, runs it against the database, and returns results
- **Phase 4 ✅ Dashboard** — Interactive Streamlit dashboard with KPI cards, revenue/category/review visualizations, and an embedded AI query tool; deployed publicly on Streamlit Cloud

## Key Features
- 4 live KPI cards: Total Orders, Total Revenue, Avg Review Score, Late Delivery Rate
- Top 10 Categories by Revenue (bar chart)
- Monthly Order Volume trend (line chart)
- Average Review Score by Category (bar chart)
- **AI Agent:** ask any business question in plain English (e.g. *"Which sellers have the most 5-star reviews?"*) and get an instant SQL-backed answer

## Project Structure
```
retail-intelligence-platform/
├── data/raw/          ← Olist CSVs (gitignored)
├── data/exports/      ← saved charts from exploration
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_cleaning.ipynb      ← cleans data, loads into Neon
│   └── 03_ai_agent.ipynb      ← AI agent prototyping
├── dashboard/
│   ├── app.py                 ← Streamlit app
│   └── .streamlit/
│       └── secrets.toml       ← DB + API credentials (gitignored)
├── requirements.txt
└── .gitignore
```

## Running Locally
1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create `dashboard/.streamlit/secrets.toml` with:
   ```toml
   GROQ_API_KEY = "your-groq-key"
   DATABASE_URL = "your-neon-connection-string"
   ```
3. Run the dashboard:
   ```bash
   cd dashboard
   streamlit run app.py
   ```
