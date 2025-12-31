import httpx

import asyncio


URL = 'https://pokeapi.co/api/v2/pokemon'

async def request_to_service(client, semaphore, offset: int, limit: int = 1):
    async with semaphore:
        resp = await client.get(
            URL,
            params={
                'limit': limit,
                'offset': offset,
            }
        )
        print(f'Reqest done: offset: {offset}')
        await asyncio.sleep(3)
        return resp.json()


async def main():
    semaphore = asyncio.Semaphore(2)
    async with httpx.AsyncClient() as client:
        tasks = [
            asyncio.create_task(
                request_to_service(client, semaphore, offset)) 
                for offset in range(1, 11)
        ]
        res = await asyncio.gather(*tasks)

    response = []
    for i in res:
        response.append(i)
    return response


asyncio.run(main())


# Async limiter period example
import httpx
import asyncio
from aiolimiter import AsyncLimiter

URL = 'https://pokeapi.co/api/v2/pokemon'

async def request_to_service(client, limiter, offset: int, limit: int = 1):
    async with limiter:  # Ожидание доступного токена
        resp = await client.get(
            URL,
            params={
                'limit': limit,
                'offset': offset,
            }
        )
        print(f'Request done: offset: {offset}')
        return resp.json()


async def main():
    # 100 запросов за 60 секунд = rate = 100/60 ≈ 1.67 запросов/сек
    # max_rate - максимальная скорость, time_period - период в секундах
    limiter = AsyncLimiter(max_rate=100, time_period=60)
    
    async with httpx.AsyncClient() as client:
        tasks = [
            asyncio.create_task(
                request_to_service(client, limiter, offset)) 
                for offset in range(1, 11)
        ]
        res = await asyncio.gather(*tasks)

    response = []
    for i in res:
        response.append(i)
    return response


asyncio.run(main())