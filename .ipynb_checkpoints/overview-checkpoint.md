Отлично, тогда фиксируем **финальную версию** —
**чек-лист подготовки под российские продуктовые компании (Ozon, Яндекс, Авито, VK)**
**без академической воды, без FAANG-хардкора, только то, что реально спрашивают**.

Это список, с которым **можно идти на собеседование**.

---

# ✅ Python Backend Interview Checklist (Russia, Middle / Senior)

---

## 1️⃣ Алгоритмическое мышление (практика, не теория)

![Image](https://media2.dev.to/dynamic/image/width%3D800%2Cheight%3D%2Cfit%3Dscale-down%2Cgravity%3Dauto%2Cformat%3Dauto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fi%2Fm12gjqex1tbxgsunop0h.png?utm_source=chatgpt.com)

![Image](https://cdn.emre.me/2019-10-21-two-pointers.png?utm_source=chatgpt.com)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/0%2A4Horb9KM70lrBJwR.png?utm_source=chatgpt.com)

![Image](https://data-flair.training/blogs/wp-content/uploads/sites/2/2019/06/Stacks-and-queues-in-C.jpg?utm_source=chatgpt.com)

### Что уметь **делать руками**

* Один проход по массиву / строке
* Работа с `dict` / `set`
* Sliding window
* Two pointers
* Stack / Queue
* Сортировка + проход
* BFS (базово, без изысков)

### Что **уметь объяснить**

* Почему выбрал эту структуру
* Сложность по времени и памяти
* Edge cases

❌ **Не нужно**

* Реализация сортировок
* Сложная DP
* Названия алгоритмов наизусть

---

## 2️⃣ Python Core — критично важно

![Image](https://media.geeksforgeeks.org/wp-content/uploads/20201228175211/GFGTemplate-660x406.png?utm_source=chatgpt.com)

![Image](https://files.realpython.com/media/memory_management_3.52bffbf302d3.png?utm_source=chatgpt.com)

![Image](https://cdn.sanity.io/images/oaglaatp/production/e964651083d6cdb24476b57e2bfc271adf0e0969-3720x2160.png?auto=format\&h=2160\&w=3720\&utm_source=chatgpt.com)

### Обязательно:

* `list`, `dict`, `set` — сложность операций
* Mutable vs immutable
* `is` vs `==`
* Передача аргументов
* Shallow / deep copy
* Итераторы и генераторы
* `__str__` vs `__repr__`

### Часто спрашивают:

* Почему `dict` быстрый
* Когда `list` тормозит
* Как работает GC
* Что такое reference counting

---

## 3️⃣ Асинхронность и конкурентность (Ozon / Яндекс — часто)

![Image](https://codilime.com/img/03-yield-1-.svg?utm_source=chatgpt.com)

![Image](https://superfastpython.com/wp-content/uploads/2022/11/Differences-Between-asyncio-and-threading.png?utm_source=chatgpt.com)

![Image](https://files.realpython.com/media/MProc.7cf3be371bbc.png?utm_source=chatgpt.com)

### Нужно знать:

* `async` / `await`
* Event loop
* Blocking vs non-blocking
* Почему `time.sleep()` ломает async
* `asyncio.gather`

### Понимать:

* Async vs threading vs multiprocessing
* Когда async **не нужен**
* GIL (на уровне понимания, не деталей CPython)

---

## 4️⃣ Backend-инженерия (часто решает исход интервью)

![Image](https://restfulapi.net/wp-content/uploads/How-to-Design-a-REST-API.png?utm_source=chatgpt.com)

![Image](https://cdn.sanity.io/images/3jwyzebk/production/57b3d8275f0ac20cb6560b5d4d84a31a544a5213-1584x943.png?utm_source=chatgpt.com)

![Image](https://substackcdn.com/image/fetch/%24s_%21ySIW%21%2Cf_auto%2Cq_auto%3Agood%2Cfl_progressive%3Asteep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80993b71-e643-4fd7-9ea1-a968a7a5f2cf_2096x1086.png?utm_source=chatgpt.com)

### API

* REST
* Idempotency
* Версионирование
* Error handling
* Retries + timeout

### Инфраструктурные темы:

* Rate limiting
* Caching (Redis)
* Circuit breaker
* Dead letter queue (что это)

---

## 5️⃣ Базы данных (спросят 100%)

![Image](https://i.sstatic.net/UI25E.jpg?utm_source=chatgpt.com)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1086/0%2ACxpRYqlARO8JhCd8.gif?utm_source=chatgpt.com)

![Image](https://media.geeksforgeeks.org/wp-content/cdn-uploads/transactnLevel.png?utm_source=chatgpt.com)

### SQL:

* JOIN
* Индексы
* EXPLAIN (на уровне идеи)
* ACID
* Transaction isolation

### NoSQL:

* Redis — когда и зачем
* Cache invalidation (проблема)

---

## 6️⃣ ООП и дизайн (практично)

![Image](https://cdn.ttgtmedia.com/rms/onlineimages/solid_principles_of_object_oriented_design-f_mobile.png?utm_source=chatgpt.com)

![Image](https://media.geeksforgeeks.org/wp-content/uploads/20240112153449/Dependency-Injection-Design-Pattern.jpg?utm_source=chatgpt.com)

![Image](https://media.geeksforgeeks.org/wp-content/uploads/20200116152733/solution_factory-_diagram.png?utm_source=chatgpt.com)

### Обязательно:

* SOLID (без заучивания)
* Dependency Injection
* Composition > inheritance
* Где бизнес-логика

### Паттерны, которые реально встречаются:

* Factory
* Strategy
* Decorator
* Observer

❌ Не нужно:

* Заучивать все GoF паттерны

---

## 7️⃣ Тестирование (могут спросить внезапно)

![Image](https://pytest-with-eric.com/images/pytest-fixture-example-indirect-parameterization.png?utm_source=chatgpt.com)

![Image](https://static-assets.codecademy.com/Courses/testing-concepts/mocking-in-unit-tests.png?utm_source=chatgpt.com)

![Image](https://pytest-with-eric.com/images/pytest-asyncio-1.png?utm_source=chatgpt.com)

* `pytest`
* Fixtures
* `mock`
* Что тестировать
* Как тестировать async-код

---

## 8️⃣ System Design (Middle+/Senior)

![Image](https://bytebytego.com/images/courses/system-design-interview/a-framework-for-system-design-interviews/figure-3-4-4ZXFIXDU.png?utm_source=chatgpt.com)

![Image](https://docs.oracle.com/cd/E19225-01/820-5819/images/identityMgr_high_availability.gif?utm_source=chatgpt.com)

![Image](https://miro.medium.com/1%2A7Vq-CAUby3nt0UkF4GKhUg.png?utm_source=chatgpt.com)

### Типовые задачи:

* Сервис уведомлений
* Rate limiter
* Лента
* Short URL
* Очереди

### Важно:

* Trade-offs
* Где bottleneck
* Как масштабировать
* Как деградирует система

---

## 9️⃣ Live Coding — как себя вести

![Image](https://dersyb7nfifdf.cloudfront.net/blog/2021/07/Untitled-Diagram-Page-12.png?utm_source=chatgpt.com)

![Image](https://cs.unc.edu/wp-content/uploads/sites/1265/2024/09/Technical-Interview-Graphic.png?utm_source=chatgpt.com)

### Делай:

* Задавай вопросы
* Проговаривай мысли
* Обсуждай крайние случаи
* Пиши простой код

### Не делай:

* Молчать
* Усложнять
* Оптимизировать раньше времени

---

## 🔥 Итоговая формула успеха

> **Не “знаю алгоритмы” →
> а “умею решать задачи и объяснять решения”**

Если ты:

* уверенно пишешь Python
* объясняешь решения
* понимаешь backend-контекст

👉 **ты проходной кандидат для Ozon / Яндекс.**

---

## Что можем сделать дальше (максимум пользы)

* 📅 **План на 21 / 30 дней**
* 🧠 **Mock live-coding интервью**
* 🏗 **System Design — шаблон ответа**
* 🧪 **Типовые вопросы Python internals**

Скажи, **что делаем следующим шагом**?
