import os, asyncpg, aiohttp, asyncio, datetime

FINNHUB = os.getenv("FINNHUB_API_KEY")
DB_URL  = os.getenv("DATABASE_URL")

async def fetch_quote(session, sym):
    url = "https://finnhub.io/api/v1/quote"
    params = {"symbol": sym, "token": FINNHUB}
    async with session.get(url, params=params, timeout=10) as r:
        return sym, await r.json()

async def main():
    conn = await asyncpg.connect(dsn=DB_URL)
    rows = await conn.fetch("select symbol from tickers")
    symbols = [r["symbol"] for r in rows]

    # 50 calls/min keeps us under Finnhub's free 60-calls/min limit
    chunks = [symbols[i:i+50] for i in range(0, len(symbols), 50)]

    async with aiohttp.ClientSession() as session:
        for chunk in chunks:
            tasks = [fetch_quote(session, s) for s in chunk]
            for sym, q in await asyncio.gather(*tasks):
                price = q.get("c") or 0        # current price
                prev  = q.get("pc") or 0       # previous close
                pct   = (price - prev)/prev*100 if prev else None
                await conn.execute("""
                    update tickers
                    set last_price=$1, pct_yoy=$2, updated_at=now()
                    where symbol=$3
                """, price, pct, sym)
            await asyncio.sleep(65)  # pause 65 s before next batch

    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
