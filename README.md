# Stock Insight SaaS – Starter Kit (MVP)

This repository contains a *no‑code‑friendly* starter kit that powers a lightweight stock‑market insight platform aimed at retail traders.

**Components**

| Folder | Description |
|--------|-------------|
| `backend/` | FastAPI micro‑service that aggregates data from Finnhub & AlphaVantage, applies user filters, and returns JSON. |
| `frontend/` | Single‑page HTML app built with plain JS – consumes the backend API and renders tables/alerts. |
| `supabase/` | SQL schema for user auth, watchlists, saved scans. |
| `workflows/` | `n8n` JSON workflow files for Daily Close Recap & Intraday Alerts. |

---

## Quick Start (local)

```bash
# 1. clone
git clone <this‑repo>
cd stock-saas

# 2. backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your API keys
uvicorn main:app --reload

# 3. frontend
# open frontend/index.html in your browser
```

---

## Deploy Cheap / Free

| Part | Service | Plan | Notes |
|------|---------|------|-------|
| Backend | Render.com | Free web service | connect GitHub repo, set env vars |
| DB/Auth | Supabase | Free tier | run schema.sql |
| Cron/Flows | n8n Cloud (community) or self‑host on Fly.io | Free | import JSON |
| Frontend | Netlify | Free | drag‑and‑drop build |

Detailed instructions are in each folder’s `README.md`.

---

### Disclaimer

> All information provided by this application is for educational and informational purposes only and **does not constitute financial advice**. Investors should conduct their own research or consult a qualified advisor before making investment decisions.

---