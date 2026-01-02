import time
import asyncio
import httpx


async def fetch_page(client: httpx.AsyncClient, offset: int, limit: int):
    await asyncio.sleep(1)
    return await client.get(
        "https://pokeapi.co/api/v2/pokemon",
        params={"limit": limit, "offset": offset},
    )


async def fetch_all_pokemons():
    limit = 50
    total_pages = 100  # ❌ "примерно знаем", берём с запасом
    start_time = time.time()

    async with httpx.AsyncClient() as client:
        tasks = []

        # ❌ ОШИБКА №1: создаём сотни задач сразу
        for page in range(total_pages):
            offset = page * limit
            tasks.append(
                fetch_page(client, offset, limit)
            )

        #  ОШИБКА №2: gather без ограничений
        responses = await asyncio.gather(*tasks)

        for response in responses:
            response.raise_for_status()
            data = response.json()
            for pokemon in data["results"]:
                pass

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

asyncio.run(fetch_all_pokemons())