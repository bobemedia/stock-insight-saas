import os, requests, asyncpg, asyncio

FINNHUB = os.getenv("FINNHUB_API_KEY")
DB_URL  = os.getenv("DATABASE_URL")

async def main():
    conn = await asyncpg.connect(dsn=DB_URL)
    for exch in ("US", "TO"):
        r = requests.get("https://finnhub.io/api/v1/stock/symbol",
                         params={"exchange": exch, "token": FINNHUB}, timeout=30)
        r.raise_for_status()
        for item in r.json():
            symbol = item["symbol"]
            name   = item["description"]
            await conn.execute("""
                insert into tickers(symbol, name, exchange)
                values($1,$2,$3)
                on conflict(symbol) do update set name=$2, exchange=$3
            """, symbol, name, exch)
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
