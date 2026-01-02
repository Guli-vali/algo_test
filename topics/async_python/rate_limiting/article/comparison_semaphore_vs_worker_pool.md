# Сравнение: Semaphore vs Worker Pool

## Подход 1: Semaphore (простой)

```python
semaphore = asyncio.Semaphore(5)

async def fetch_page(client, offset):
    async with semaphore:  # Ограничение: максимум 5 одновременных запросов
        response = await client.get(API_URL, params={"offset": offset})
        return response.json()["results"]

async def main():
    async with httpx.AsyncClient() as client:
        # Создаем ВСЕ задачи сразу (1000 задач!)
        tasks = [
            fetch_page(client, offset)
            for offset in range(0, 1000, 50)  # 20 задач
        ]
        # Semaphore ограничивает одновременное выполнение до 5
        results = await asyncio.gather(*tasks)
```

## Подход 2: Worker Pool (с очередями)

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

---

## Преимущества Worker Pool подхода:

### 1. **Память: задачи создаются динамически, а не все сразу**

**Semaphore:**
```python
# Создаем 10,000 задач сразу - все в памяти!
tasks = [fetch_page(...) for _ in range(10_000)]
# Каждая задача = объект корутины в памяти
```

**Worker Pool:**
```python
# Создаем только 5 воркеров
workers = [worker(...) for _ in range(5)]
# Задачи добавляются в очередь по мере необходимости
# Можно добавлять задачи динамически, даже из другого источника
```

**Когда важно:** При обработке миллионов задач или потоков данных.

---

### 2. **Гибкость: можно добавлять задачи динамически**

**Semaphore:**
```python
# Все задачи должны быть известны ЗАРАНЕЕ
tasks = [fetch_page(...) for offset in known_offsets]
# Нельзя добавить новые задачи во время выполнения
```

**Worker Pool:**
```python
# Producer может добавлять задачи в любой момент
async def producer(queue):
    while has_more_data:
        new_task = await get_next_task()  # Из БД, файла, API и т.д.
        await queue.put(new_task)
    
    # Сигнализируем воркерам о завершении
    for _ in range(workers_count):
        await queue.put(None)

# Producer и Workers работают параллельно!
```

**Когда важно:** 
- Обработка данных из файла/БД по частям
- Потоковая обработка (streaming)
- Задачи генерируются динамически

---

### 3. **Обработка результатов по мере поступления (streaming)**

**Semaphore:**
```python
# Ждем завершения ВСЕХ задач
results = await asyncio.gather(*tasks)  # Блокируется до конца

# Только потом обрабатываем результаты
for result in results:
    process(result)  # Начинаем обработку только после всех запросов
```

**Worker Pool:**
```python
# Обрабатываем результаты СРАЗУ, как только они появляются
while finished_workers < workers_count:
    batch = await results.get()  # Получаем результат сразу
    process(batch)  # Обрабатываем немедленно
    
    # Пока обрабатываем этот батч, воркеры уже делают следующие запросы!
```

**Когда важно:**
- Нужно начать обработку до завершения всех запросов
- Результаты большие и нужно обрабатывать по частям
- Real-time обработка данных

---

### 4. **Лучший контроль над жизненным циклом воркеров**

**Semaphore:**
```python
# Каждая задача = новая корутина
# Нет переиспользования контекста между задачами
```

**Worker Pool:**
```python
async def worker(client, queue, results):
    # Воркер может инициализировать ресурсы один раз
    db_connection = await connect_to_db()
    cache = {}
    
    while True:
        task = await queue.get()
        # Используем переиспользованные ресурсы
        result = await process_with_cache(task, cache)
        await results.put(result)
    
    # Закрываем ресурсы один раз при завершении
    await db_connection.close()
```

**Когда важно:**
- Дорогая инициализация (БД соединения, кэш, модели ML)
- Нужно переиспользовать состояние между задачами

---

### 5. **Обработка ошибок и retry логика**

**Semaphore:**
```python
# Если одна задача упала, gather() может упасть
# Нужно обрабатывать ошибки для каждой задачи отдельно
```

**Worker Pool:**
```python
async def worker(client, queue, results):
    while True:
        task = await queue.get()
        for attempt in range(3):  # Retry логика
            try:
                result = await process(task)
                await results.put(result)
                break
            except Exception as e:
                if attempt == 2:
                    await error_queue.put((task, e))
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        queue.task_done()
```

**Когда важно:** Нужна сложная логика обработки ошибок, retry, dead letter queue.

---

### 6. **Приоритизация задач**

**Semaphore:**
```python
# Все задачи равноправны, нет приоритетов
tasks = [fetch_page(...) for offset in offsets]
```

**Worker Pool:**
```python
# Можно использовать PriorityQueue
from asyncio import PriorityQueue

queue = PriorityQueue()

# Высокий приоритет = меньше число
await queue.put((1, high_priority_task))  # Выполнится первым
await queue.put((10, low_priority_task))  # Выполнится позже
```

---

### 7. **Backpressure (контроль перегрузки)**

**Worker Pool:**
```python
# Очередь результатов может быть ограничена
results = asyncio.Queue(maxsize=100)s

# Если consumer медленный, очередь заполнится
# Воркеры автоматически замедлятся (await results.put() будет ждать)
# Это защищает от перегрузки памяти
```

**Semaphore:**
```python
# Нет встроенного механизма backpressure
# Если обработка результатов медленная, все результаты накапливаются в памяти
```

---

## Когда использовать Semaphore:

✅ **Простая задача:** ограничить количество одновременных запросов  
✅ **Все задачи известны заранее**  
✅ **Небольшое количество задач** (< 1000)  
✅ **Не нужна streaming обработка**  
✅ **Простота кода важнее гибкости**

## Когда использовать Worker Pool:

✅ **Большое количество задач** (> 1000) или бесконечный поток  
✅ **Задачи генерируются динамически**  
✅ **Нужна streaming обработка результатов**  
✅ **Нужно переиспользовать ресурсы между задачами**  
✅ **Сложная логика обработки ошибок/retry**  
✅ **Нужна приоритизация задач**  
✅ **Важен контроль памяти (backpressure)**

---

## Пример: обработка большого файла

**Semaphore (плохо):**
```python
# Читаем ВЕСЬ файл в память
all_lines = file.readlines()  # 1GB файл = 1GB в памяти!
tasks = [process(line) for line in all_lines]  # Еще больше памяти!
await asyncio.gather(*tasks)
```

**Worker Pool (хорошо):**
```python
async def producer(queue, file):
    for line in file:  # Читаем построчно
        await queue.put(line)  # Только одна строка в памяти

async def worker(queue, results):
    while True:
        line = await queue.get()
        result = process(line)
        await results.put(result)
        queue.task_done()

# Память: только несколько строк, а не весь файл!
```

---

## Итоговая таблица сравнения:

| Характеристика | Semaphore | Worker Pool |
|---------------|-----------|-------------|
| **Простота кода** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Использование памяти** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Гибкость** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Streaming обработка** | ❌ | ✅ |
| **Динамические задачи** | ❌ | ✅ |
| **Переиспользование ресурсов** | ❌ | ✅ |
| **Приоритизация** | ❌ | ✅ |
| **Backpressure** | ❌ | ✅ |
| **Производительность (малые задачи)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Производительность (большие задачи)** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

