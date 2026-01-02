"""
Демонстрация работы queue.join() и queue.task_done()

Этот пример показывает:
1. Как работает механизм queue.join() / queue.task_done()
2. Что произойдет, если забыть вызвать task_done()
3. Зачем нужен queue.join() в worker pool паттерне
"""
import asyncio


async def worker_with_task_done(queue, worker_id):
    """Воркер, который ПРАВИЛЬНО вызывает task_done()"""
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()  # Важно! Помечаем маркер завершения
            break
        
        print(f"Worker {worker_id}: обрабатываю {item}")
        await asyncio.sleep(0.1)  # Имитация работы
        queue.task_done()  # Помечаем задачу как выполненную


async def worker_without_task_done(queue, worker_id):
    """Воркер, который ЗАБЫЛ вызвать task_done()"""
    while True:
        item = await queue.get()
        if item is None:
            # ЗАБЫЛИ вызвать queue.task_done()!
            break
        
        print(f"Worker {worker_id}: обрабатываю {item}")
        await asyncio.sleep(0.1)
        # ЗАБЫЛИ вызвать queue.task_done()!


async def example_with_join():
    """Пример с queue.join() - правильный подход"""
    print("\n" + "="*60)
    print("ПРИМЕР 1: С queue.join() - правильный подход")
    print("="*60)
    
    queue = asyncio.Queue()
    
    # Кладем задачи
    for i in range(5):
        await queue.put(i)
    await queue.put(None)  # Маркер завершения
    
    # Запускаем воркер
    worker = asyncio.create_task(worker_with_task_done(queue, 1))
    
    # Ждем завершения всех задач
    print("Ожидаю завершения всех задач через queue.join()...")
    await queue.join()  # Блокируется, пока все task_done() не вызваны
    print("✓ Все задачи обработаны!")
    
    await worker
    print("✓ Воркер завершен\n")


async def example_without_join():
    """Пример БЕЗ queue.join() - может быть проблема"""
    print("\n" + "="*60)
    print("ПРИМЕР 2: БЕЗ queue.join() - может быть проблема")
    print("="*60)
    
    queue = asyncio.Queue()
    
    for i in range(5):
        await queue.put(i)
    await queue.put(None)
    
    worker = asyncio.create_task(worker_with_task_done(queue, 1))
    
    # НЕ используем queue.join(), просто ждем воркер
    print("Жду завершения воркера (без queue.join())...")
    await worker
    print("✓ Воркер завершен")
    print(f"  Но queue.unfinished_tasks = {queue.unfinished_tasks}")
    print("  (должно быть 0, если все task_done() вызваны)\n")


async def example_broken_worker():
    """Пример с 'сломанным' воркером, который забыл task_done()"""
    print("\n" + "="*60)
    print("ПРИМЕР 3: Воркер забыл вызвать task_done()")
    print("="*60)
    
    queue = asyncio.Queue()
    
    for i in range(3):
        await queue.put(i)
    await queue.put(None)
    
    worker = asyncio.create_task(worker_without_task_done(queue, 1))
    
    print("Ожидаю завершения через queue.join()...")
    try:
        # Это ЗАВИСНЕТ, потому что воркер не вызвал task_done()
        # Раскомментируйте следующую строку, чтобы увидеть зависание:
        # await queue.join()  # ЗАВИСНЕТ!
        
        # Вместо этого используем timeout, чтобы показать проблему
        await asyncio.wait_for(queue.join(), timeout=1.0)
    except asyncio.TimeoutError:
        print("✗ TIMEOUT! queue.join() завис, потому что task_done() не вызван")
        print(f"  queue.unfinished_tasks = {queue.unfinished_tasks}")
        print("  Это показывает важность вызова task_done()!\n")
    
    await worker


async def main():
    await example_with_join()
    await example_without_join()
    await example_broken_worker()
    
    print("\n" + "="*60)
    print("ВЫВОД:")
    print("="*60)
    print("""
queue.join() - это механизм синхронизации, который гарантирует:
1. Все задачи из очереди были взяты (queue.get())
2. Все задачи были помечены как выполненные (queue.task_done())

БЕЗ queue.join():
- Нет гарантии, что все task_done() были вызваны
- Может быть race condition между воркерами
- Нет способа проверить, что очередь действительно пуста

С queue.join():
- Гарантируется, что все задачи обработаны
- Защита от забытых task_done()
- Правильная синхронизация в producer-consumer паттерне
    """)


if __name__ == "__main__":
    asyncio.run(main())

