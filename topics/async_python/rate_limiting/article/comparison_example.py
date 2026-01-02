"""
Практическое сравнение Semaphore vs Worker Pool

Демонстрирует ключевые различия на примере обработки большого количества задач.
"""
import asyncio
import time
import httpx


# ========== ПОДХОД 1: SEMAPHORE ==========
async def fetch_with_semaphore(client, semaphore, offset):
    """Простой подход с Semaphore"""
    async with semaphore:
        response = await client.get(
            "https://pokeapi.co/api/v2/pokemon",
            params={"limit": 50, "offset": offset},
        )
        return response.json()["results"]


async def semaphore_approach(total_pages=100):
    """Semaphore подход: создаем все задачи сразу"""
    print("\n" + "="*60)
    print("ПОДХОД 1: SEMAPHORE")
    print("="*60)
    
    semaphore = asyncio.Semaphore(5)  # Максимум 5 одновременных запросов
    
    start_time = time.time()
    
    async with httpx.AsyncClient() as client:
        # ПРОБЛЕМА 1: Создаем ВСЕ задачи сразу (100 задач в памяти!)
        print(f"Создаю {total_pages} задач...")
        tasks = [
            fetch_with_semaphore(client, semaphore, offset)
            for offset in range(0, total_pages * 50, 50)
        ]
        print(f"✓ Все задачи созданы. Память: ~{len(tasks) * 0.001:.2f} MB (примерно)")
        
        # ПРОБЛЕМА 2: Ждем завершения ВСЕХ задач
        print("Ожидаю завершения всех запросов...")
        results = await asyncio.gather(*tasks)
        
        # ПРОБЛЕМА 3: Обрабатываем результаты только ПОСЛЕ всех запросов
        print("Начинаю обработку результатов...")
        total_pokemon = sum(len(batch) for batch in results)
    
    elapsed = time.time() - start_time
    print(f"✓ Обработано {total_pages} страниц, {total_pokemon} покемонов")
    print(f"✓ Время: {elapsed:.2f}s")
    print(f"✓ Обработка результатов началась только после всех запросов")


# ========== ПОДХОД 2: WORKER POOL ==========
async def worker(client, queue, results):
    """Воркер из пула"""
    while True:
        offset = await queue.get()
        if offset is None:
            queue.task_done()
            await results.put(None)  # Сигнал завершения
            break
        
        try:
            response = await client.get(
                "https://pokeapi.co/api/v2/pokemon",
                params={"limit": 50, "offset": offset},
            )
            data = response.json()["results"]
            await results.put(data)
        except Exception as e:
            print(f"Ошибка offset={offset}: {e}")
        finally:
            queue.task_done()


async def worker_pool_approach(total_pages=100):
    """Worker Pool подход: задачи в очереди, обработка по мере поступления"""
    print("\n" + "="*60)
    print("ПОДХОД 2: WORKER POOL")
    print("="*60)
    
    queue = asyncio.Queue()
    results = asyncio.Queue()
    workers_count = 5
    
    start_time = time.time()
    first_result_time = None
    
    async with httpx.AsyncClient() as client:
        # ПРЕИМУЩЕСТВО 1: Задачи добавляются в очередь (не все в памяти)
        print(f"Добавляю {total_pages} задач в очередь...")
        for offset in range(0, total_pages * 50, 50):
            await queue.put(offset)
        
        for _ in range(workers_count):
            await queue.put(None)
        
        print(f"✓ Задачи в очереди. Память: только очередь (~0.01 MB)")
        
        # Запускаем воркеров
        workers = [
            asyncio.create_task(worker(client, queue, results))
            for _ in range(workers_count)
        ]
        
        # ПРЕИМУЩЕСТВО 2: Обрабатываем результаты СРАЗУ, как только появляются
        print("Начинаю обработку результатов (streaming)...")
        finished_workers = 0
        total_pokemon = 0
        
        while finished_workers < workers_count:
            batch = await results.get()
            
            if batch is None:
                finished_workers += 1
                continue
            
            # ПРЕИМУЩЕСТВО 3: Первый результат обрабатывается ДО завершения всех запросов
            if first_result_time is None:
                first_result_time = time.time()
                elapsed_to_first = first_result_time - start_time
                print(f"✓ Первый результат получен через {elapsed_to_first:.2f}s")
                print(f"  (остальные запросы еще выполняются!)")
            
            total_pokemon += len(batch)
        
        await queue.join()
        await asyncio.gather(*workers)
    
    elapsed = time.time() - start_time
    print(f"✓ Обработано {total_pages} страниц, {total_pokemon} покемонов")
    print(f"✓ Время: {elapsed:.2f}s")
    print(f"✓ Обработка началась сразу при получении первого результата")


# ========== ПОДХОД 3: ДИНАМИЧЕСКИЕ ЗАДАЧИ (только Worker Pool) ==========
async def dynamic_producer(queue, total_pages):
    """Producer, который добавляет задачи динамически"""
    # Имитация: задачи приходят из внешнего источника (БД, файл, API)
    for i in range(total_pages):
        offset = i * 50
        await queue.put(offset)
        await asyncio.sleep(0.01)  # Имитация задержки получения задачи
    
    # Сигнализируем воркерам о завершении
    for _ in range(5):
        await queue.put(None)


async def worker_pool_dynamic_approach(total_pages=50):
    """Worker Pool с динамическим producer"""
    print("\n" + "="*60)
    print("ПОДХОД 3: WORKER POOL + ДИНАМИЧЕСКИЙ PRODUCER")
    print("="*60)
    print("(Это невозможно с Semaphore!)")
    
    queue = asyncio.Queue()
    results = asyncio.Queue()
    workers_count = 5
    
    async with httpx.AsyncClient() as client:
        # Producer работает параллельно с воркерами
        producer = asyncio.create_task(dynamic_producer(queue, total_pages))
        
        workers = [
            asyncio.create_task(worker(client, queue, results))
            for _ in range(workers_count)
        ]
        
        print("Producer и Workers работают параллельно...")
        print("Задачи добавляются в очередь по мере необходимости")
        
        finished_workers = 0
        total_pokemon = 0
        
        while finished_workers < workers_count:
            batch = await results.get()
            if batch is None:
                finished_workers += 1
                continue
            total_pokemon += len(batch)
        
        await producer
        await queue.join()
        await asyncio.gather(*workers)
    
    print(f"✓ Обработано {total_pages} страниц, {total_pokemon} покемонов")
    print("✓ Producer добавлял задачи динамически во время выполнения")


async def main():
    """Сравнение подходов"""
    print("\n" + "="*60)
    print("СРАВНЕНИЕ: SEMAPHORE vs WORKER POOL")
    print("="*60)
    
    # Используем меньше страниц для демонстрации
    pages = 20
    
    # Подход 1: Semaphore
    await semaphore_approach(pages)
    
    await asyncio.sleep(1)
    
    # Подход 2: Worker Pool
    await worker_pool_approach(pages)
    
    await asyncio.sleep(1)
    
    # Подход 3: Динамический producer (только Worker Pool)
    await worker_pool_dynamic_approach(pages)
    
    print("\n" + "="*60)
    print("ВЫВОДЫ:")
    print("="*60)
    print("""
1. SEMAPHORE:
   - Простой код
   - Все задачи создаются сразу (память)
   - Обработка результатов только после всех запросов
   - Нельзя добавлять задачи динамически

2. WORKER POOL:
   - Более сложный код
   - Задачи в очереди (эффективная память)
   - Streaming обработка результатов
   - Можно добавлять задачи динамически
   - Гибкость и контроль

Выбирайте подход в зависимости от задачи!
    """)


if __name__ == "__main__":
    asyncio.run(main())

