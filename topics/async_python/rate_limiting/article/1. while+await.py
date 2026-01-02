import asyncio
import time
import httpx


async def fetch_all_pokemons():
    limit = 100
    offset = 0

    start_time = time.time()
    async with httpx.AsyncClient() as client:
        while True:
            # ОШИБКА: ждём завершения запроса перед следующим
            response = await client.get(
                "https://pokeapi.co/api/v2/pokemon",
                params={"limit": limit, "offset": offset},
            )
            await asyncio.sleep(1)

            response.raise_for_status()
            data = response.json()

            results = data["results"]
            if not results:
                break

            # обработка данных
            for pokemon in results:
                pass

            offset += limit

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

asyncio.run(fetch_all_pokemons())
