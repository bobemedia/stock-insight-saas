import os, datetime, requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

FINNHUB_KEY = os.getenv("FINNHUB_API_KEY")
ALPHAV_KEY  = os.getenv("ALPHAVANTAGE_API_KEY")
BASE_TICKERS = [ "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "TSLA" ]  # replace with fuller universe

app = FastAPI(title="Stock Insight SaaS – API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_quote(symbol:str):
    """Return latest quote using Finnhub"""
    r = requests.get(
        "https://finnhub.io/api/v1/quote",
        params={"symbol": symbol, "token": FINNHUB_KEY},
        timeout=8,
    )
    r.raise_for_status()
    return r.json()

def get_summary(symbol:str):
    """Return basic fundamentals using Alpha Vantage"""
    r = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function":"OVERVIEW",
            "symbol":symbol,
            "apikey":ALPHAV_KEY
        },
        timeout=8,
    )
    r.raise_for_status()
    return r.json()

@app.get("/scan")
def scan(
    min_price: float = 0,
    max_price: float = 1_000,
    min_yoy: float = -100,
    max_yoy: float = 1_000,
):
    """Very simple scan across BASE_TICKERS (MVP placeholder)"""
    matches = []
    for sym in BASE_TICKERS:
        q = get_quote(sym)
        price = q.get("c")  # current price
        if price is None:
            continue
        if price < min_price or price > max_price:
            continue

        try:
            pct_yoy = ((price - q["pc"]) / q["pc"]) * 100  # previous close as rough proxy
        except ZeroDivisionError:
            pct_yoy = 0
        if pct_yoy < min_yoy or pct_yoy > max_yoy:
            continue

        matches.append(
            {
                "symbol": sym,
                "price": price,
                "pct_change_yoy": pct_yoy,
            }
        )
    return {"results": matches, "server_time": datetime.datetime.utcnow().isoformat()}