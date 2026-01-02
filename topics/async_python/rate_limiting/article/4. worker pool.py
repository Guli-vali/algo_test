import asyncio
import httpx

API_URL = "https://pokeapi.co/api/v2/pokemon"


async def worker(client: httpx.AsyncClient, queue: asyncio.Queue[int | None], results: asyncio.Queue[list]):
    while True:
        offset = await queue.get()
        if offset is None:
            # возвращаем None в очередь для других воркеров
            queue.task_done()
            # сигнализируем о завершении воркера
            await results.put(None)
            break

        try:
            response = await client.get(
                API_URL,
                params={"limit": 50, "offset": offset},
            )
            response.raise_for_status()
            data = response.json()["results"]
            # кладём результаты в очередь
            await results.put(data)
        except httpx.HTTPError as e:
            print(f"Ошибка запроса offset={offset}: {e}")
        finally:
            queue.task_done()


async def main():
    queue = asyncio.Queue()
    results = asyncio.Queue()
    workers_count = 5
    total_pages = 20  # для примера, реально можно определить по API

    async with httpx.AsyncClient() as client:
        # --- producer
        for offset in range(0, total_pages * 50, 50):
            await queue.put(offset)

        # --- ставим маркеры конца для каждого воркера
        for _ in range(workers_count):
            await queue.put(None)

        # --- запускаем воркеров
        workers = [
            asyncio.create_task(worker(client, queue, results))
            for _ in range(workers_count)
        ]

        # --- потребляем результаты
        finished_workers = 0
        while finished_workers < workers_count:
            batch = await results.get()
            if batch is None:
                finished_workers += 1
                continue
            for pokemon in batch:
                pass

        await queue.join()
        await asyncio.gather(*workers)


asyncio.run(main())
