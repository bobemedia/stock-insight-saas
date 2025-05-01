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
async def scan(
    min_price: float = 0,
    max_price: float = 1_000,
    min_yoy: float = -1_000,
    max_yoy: float = 1_000,
    exchange: str | None = None,
    limit: int = 100,
):
    query = """
        select symbol, last_price as price, pct_yoy
        from tickers
        where last_price between $1 and $2
          and pct_yoy between $3 and $4
    """
    params = [min_price, max_price, min_yoy, max_yoy]
    if exchange:
        query += " and exchange = $5"
        params.append(exchange.upper())
    query += " order by pct_yoy desc limit $6"
    params.append(limit)

    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    rows = await conn.fetch(query, *params)
    await conn.close()
    return {"results": [dict(r) for r in rows],
            "server_time": datetime.datetime.utcnow().isoformat()}
