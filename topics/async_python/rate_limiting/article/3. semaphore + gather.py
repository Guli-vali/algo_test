import asyncio
import time
import httpx


semaphore = asyncio.Semaphore(10)
API_URL = "https://pokeapi.co/api/v2/pokemon"


async def fetch_page(client: httpx.AsyncClient, offset: int):
    async with semaphore:
        start = time.perf_counter()

        response = await client.get(
            API_URL,
            params={"limit": 50, "offset": offset},
        )
        response.raise_for_status()

        elapsed = time.perf_counter() - start
        print(f"offset={offset:4d} | request_time={elapsed:.2f}s")

        return response.json()["results"]


async def main():
    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_page(client, offset)
            for offset in range(0, 1000, 50)
        ]

        await asyncio.gather(*tasks)


asyncio.run(main())
