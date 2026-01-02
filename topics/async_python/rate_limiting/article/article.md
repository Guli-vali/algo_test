
# Асинхронное лимитирование запросов в Python - мои грабли

На днях мне прилетела задачка в которой мне надо было вычерпывать данные по HTTP запросам с такими  условиями:

1) Есть ограничение по количеству запросов в минуту
2) Количество данных которые нужно выгружать исчисляется миллионами записей
3) Один запрос выполняется достаточно долго так как грузит много записей
4) Асинхронный механизм вычерпывания данных


Не включая мозг я начал накидывать решение:


## Грабли №1: async, который работает синхронно

```python 
async def fetch_all_pages():
    ...
    while True:
        response = await fetch(   # ← ошибка
            f"/resource?page={page}"
        )
        ...
        page += 1
        ...
```

Формально:

* `async` / `await`

Фактически:

* **один запрос за раз**, каждый следующий ждёт предыдущий

> **Async-код не становится параллельным автоматически.
> Если каждый запрос ждёт завершения предыдущего —
> это синхронное исполнение в async-синтаксисе.**


## Грабли №2: «давайте просто gather всё»

Окей, давайте запрашивать данные по-настоящиему асинхронно

```python 
async def fetch_all():
    tasks = [fetch(page) for page in range(1, 1000)]
    results = await asyncio.gather(*tasks) # ← ошибка
    ...
```

Ух ты работает и правда быстро, но кажется мы создали монстра.. 

 * **Coroutine storm** - Потребление RAM сразу существнно взлетело
 * ожидаемо словил 429 Too Many Requests, так же в будующем: блокировка токена, бан IP
 * gather ждёт ВСЕ задачи, и если одна зависла → зависло всё
 * невозможно стримить данные, что важно в моем кейсе

> **`asyncio.gather` без ограничений —
> это не параллелизм, а хаос.**


### Грабли №3: Давайте думать, подсказывайте!

Интегрируем семафор, он ограничит поток наших запросов и мы стабилизируем наш асинхронный вихрь, шаблонное решение из тренажеров для прохождения интревью

```python 
semaphore = Semaphore(10)

async def fetch_page(page):
    async with semaphore:
        return await fetch(f"/resource?page={page}")

async def main():
    tasks = [fetch_page(page) for page in range(1, 1000)]
    results = await asyncio.gather(*tasks)
    ...
```

Интуитивное ожидание:
> «Ну значит 10 запросов в секунду»

Реальность:

  * Latency при ответе апи скачет на дистанции из за сети и прочего, в моем случае скорость ответа скакала от 8 до 30 секунд, что чревато сильным недоиспользованием лимита и задержке выгрузки, из за latency я использовал всего 30% от позволенного лимита запросов. 
  * Преположим через время с помощью магии ответ апи ускорили и он теперь отвчает за 0.1 секунды, что произойдет в таком случае? Гарантированный DDOS шквалом запросов.

Для наглядности:
1) Ситуация 1(долгие ответы): 10 запросов / 8 секунд ≈ 75 req/min
2) Ситуация 2(деградация скорости ответов): 10 запросов / 30 секунд ≈ 20 req/min
2) Ситуация 3(Включили кеш, ускорили апи): 10 запросов / 0.5 секунды = 1200 req/min

Семафор связывает пропускную возможность системы
с самым нестабильным параметром — latency внешнего API.

> **Semaphore регулирует ширину трубы.
> Но не регулирует поток воды.**



### Грабли №4 Идем в правильном направлении

```python
async def worker(client, queue, results):
    while True:
        offset = await queue.get()  # Берет задачу из очереди
        if offset is None:
            break
        response = await client.get(API_URL, params={"offset": offset})
        await results.put(response.json()["results"])
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    results = asyncio.Queue()
    
    # Кладем задачи в очередь
    for offset in range(0, 1000, 50):
        await queue.put(offset)
    
    # Запускаем 5 воркеров
    workers = [asyncio.create_task(worker(...)) for _ in range(5)]
    
    # Обрабатываем результаты по мере поступления
    while ...:
        batch = await results.get()
        # обрабатываем
```



### Грабли кончились

```python
from aiolimiter import AsyncLimiter

limiter = AsyncLimiter(100, 60)  # 100 запросов в минуту

async def worker(client, queue, results):
    while True:
        offset = await queue.get()  # Берет задачу из очереди
        if offset is None:
            queue.task_done()
            break

        # --- rate limit: ждем разрешения на старт запроса
        await limiter.acquire()

        # --- выполняем запрос
        response = await client.get(API_URL, params={"offset": offset})

        # --- кладем результат в очередь
        await results.put(response.json()["results"])

        queue.task_done()


async def main():
    queue = asyncio.Queue()
    results = asyncio.Queue()
    
    # --- кладем задачи в очередь
    for offset in range(0, 1000, 50):
        await queue.put(offset)
    
    # --- маркеры конца для воркеров
    workers_count = 5
    for _ in range(workers_count):
        await queue.put(None)
    
    # --- создаем воркеров
    workers = [asyncio.create_task(worker(client, queue, results)) for _ in range(workers_count)]
    
    # --- обрабатываем результаты по мере поступления
    finished_workers = 0
    while finished_workers < workers_count:
        batch = await results.get()
        if batch is None:
            finished_workers += 1
            continue

        # здесь можно обработать batch
        for item in batch:
            print(item["name"])  # пример для Pokemon API
    
    await queue.join()
    await asyncio.gather(*workers)
```
