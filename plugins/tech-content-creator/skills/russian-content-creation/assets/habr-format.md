# Habr.com Format Guide

## Overview

Habr is Russia's largest technical community platform with 15+ million monthly readers. This guide covers Habr-specific markdown syntax, formatting conventions, and best practices for publishing technical content.

**Platform:** https://habr.com
**Audience:** Developers, IT professionals, tech enthusiasts
**Tone:** Informal, peer-to-peer (использование «ты»)
**Content:** Technical articles, tutorials, case studies

---

## Habr-Specific Markdown Extensions

### 1. Cut Tag (Preview Separator)

The `<cut />` tag separates preview content (shown on main page) from full article content (shown after click).

**Syntax:**

```markdown
Вступительный текст, который виден на главной странице Habr.

Обычно это 1-3 абзаца с кратким описанием того, о чем статья.

<cut />

Основной контент статьи, который открывается по клику "Читать далее".

Здесь размещается вся основная информация, код, примеры.
```

**Best Practices:**

- Place 150-300 words before `<cut />`
- Include hook and problem statement before cut
- Preview should make reader want to click
- Don't put critical information only in preview

**Example:**

```markdown
# Как мы ускорили API в 10 раз

Привет! В этой статье я расскажу, как мы оптимизировали наш Python API и добились десятикратного ускорения. Если ты работаешь с высоконагруженными системами, эта история будет полезна.

**Что будет в статье:**
- Профилирование и поиск узких мест
- Оптимизация работы с БД
- Внедрение кэширования
- Результаты и метрики

<cut />

## Проблема: медленный API

Все началось с того, что среднее время ответа нашего API выросло до 3.5 секунд...
```

### 2. Spoiler (Collapsible Section)

Use spoilers to hide large code blocks, detailed explanations, or optional content.

**Syntax:**

```markdown
<spoiler title="Заголовок спойлера">
Содержимое, которое будет скрыто и открывается по клику.

Может включать любой markdown: код, списки, таблицы и т.д.
</spoiler>
```

**Use Cases:**

- Large code listings
- Optional detailed explanations
- Additional examples
- Raw data or logs
- Bonus content

**Example:**

```markdown
Основной код функции выглядит так:

```python
def optimize_query(query):
    return query.select_related('user').prefetch_related('tags')
```

<spoiler title="Полная реализация с обработкой ошибок">

```python
import logging
from typing import Optional
from django.db.models import QuerySet

logger = logging.getLogger(__name__)


def optimize_query(
    query: QuerySet,
    select_related: Optional[list] = None,
    prefetch_related: Optional[list] = None
) -> QuerySet:
    """
    Оптимизирует Django QuerySet, добавляя select_related и prefetch_related.

    Args:
        query: Исходный QuerySet
        select_related: Список полей для select_related
        prefetch_related: Список полей для prefetch_related

    Returns:
        Оптимизированный QuerySet

    Raises:
        ValueError: Если query не является QuerySet
    """
    if not isinstance(query, QuerySet):
        raise ValueError("query должен быть QuerySet")

    try:
        if select_related:
            query = query.select_related(*select_related)
            logger.debug(f"Применен select_related: {select_related}")

        if prefetch_related:
            query = query.prefetch_related(*prefetch_related)
            logger.debug(f"Применен prefetch_related: {prefetch_related}")

        return query

    except Exception as e:
        logger.error(f"Ошибка оптимизации запроса: {e}")
        raise
```

</spoiler>
```

### 3. Source Code with Language Highlighting

Habr supports two ways to add code:

**Standard Markdown (Preferred):**

````markdown
```python
def hello_world():
    print("Привет, Habr!")
```
````

**Habr-Specific Tag:**

```markdown
<source lang="python">
def hello_world():
    print("Привет, Habr!")
</source>
```

**Supported Languages:**

- `python`, `javascript`, `java`, `go`, `rust`, `cpp`, `c`, `csharp`
- `php`, `ruby`, `swift`, `kotlin`, `typescript`
- `bash`, `shell`, `sql`, `html`, `css`, `xml`, `json`, `yaml`
- `dockerfile`, `nginx`, `apache`
- Many more...

**Example with Comments:**

````markdown
```python
# Создаем подключение к Redis
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

# Устанавливаем значение с TTL
redis_client.setex(
    name='user:1000',
    time=3600,  # 1 час
    value='{"name": "Ivan", "email": "ivan@example.com"}'
)

# Получаем значение
user_data = redis_client.get('user:1000')
print(user_data)
```
````

### 4. Images

**Syntax:**

```markdown
![Alt text](https://example.com/image.png)
```

or with Habr tag:

```markdown
<img src="https://example.com/image.png" alt="Alt text"/>
```

**Best Practices:**

- Always add descriptive alt text in Russian
- Optimize images (max 1-2 MB each)
- Use PNG for screenshots, JPG for photos
- Host images on Habr CDN or reliable hosting
- Add captions below images

**Example:**

```markdown
Результирующий dashboard выглядит так:

![Dashboard с метриками производительности](https://example.com/dashboard.png)

*Рисунок 1. Dashboard Grafana с основными метриками: response time, throughput, error rate*
```

### 5. Tables

Standard markdown tables are supported:

```markdown
| Заголовок 1 | Заголовок 2 | Заголовок 3 |
|-------------|-------------|-------------|
| Ячейка 1    | Ячейка 2    | Ячейка 3    |
| Данные A    | Данные B    | Данные C    |
```

**Alignment:**

```markdown
| Left aligned | Center aligned | Right aligned |
|:-------------|:--------------:|--------------:|
| Слева        | По центру      | Справа        |
```

**Best Practices:**

- Keep tables simple and readable
- Use for comparisons and metrics
- Don't create overly wide tables
- Consider using lists for simple data

**Example:**

```markdown
### Сравнение производительности

| Подход | Время (мс) | Память (МБ) | Улучшение |
|--------|------------|-------------|-----------|
| Baseline | 1000 | 150 | - |
| С кэшированием | 100 | 200 | **10x** |
| С параллелизмом | 50 | 400 | **20x** |
```

### 6. Quotes (Blockquotes)

```markdown
> Цитата или важная мысль.
> Может занимать несколько строк.

> Отдельный блок цитаты.
```

**Use for:**

- Expert quotes
- Important takeaways
- Definitions
- Warnings or notes

**Example:**

```markdown
> **Важно:** Всегда профилируйте код перед оптимизацией. Преждевременная оптимизация — корень всех зол.

> «Простота — это высшая степень изощренности», — Леонардо да Винчи
```

### 7. Lists

**Unordered (Bulleted):**

```markdown
- Первый пункт
- Второй пункт
  - Вложенный пункт
  - Еще один вложенный
- Третий пункт
```

**Ordered (Numbered):**

```markdown
1. Первый шаг
2. Второй шаг
3. Третий шаг
```

**Task Lists (Checklists):**

```markdown
- [ ] Задача не выполнена
- [x] Задача выполнена
- [ ] Еще одна задача
```

**Example:**

```markdown
### План оптимизации

1. **Профилирование**
   - Запустить cProfile
   - Проанализировать результаты
   - Определить узкие места

2. **Оптимизация**
   - Кэширование частых запросов
   - Индексы для БД
   - Асинхронная обработка

3. **Тестирование**
   - Написать бенчмарки
   - Сравнить с baseline
   - Проверить на продакшене
```

---

## Content Structure for Habr

### Typical Article Structure

```markdown
# Заголовок: конкретный и цепляющий

Краткое вступление (1-2 абзаца):
- О чем статья
- Почему это важно
- Что читатель узнает

**Что будет в статье:**
- Основные разделы
- Ключевые темы
- Практические примеры

<cut />

## Введение

Развернутое введение с контекстом проблемы.

## Основная часть

### Раздел 1: Название

Текст с примерами кода и объяснениями.

### Раздел 2: Название

Продолжение с практическими примерами.

### Раздел 3: Название

Дополнительные детали и best practices.

## Практические рекомендации

- Actionable советы
- Best practices
- Типичные ошибки

## Заключение

Резюме и выводы.

## Полезные ссылки

- Документация
- GitHub
- Связанные статьи
```

### Title Best Practices

**Good Titles:**

✅ «Как мы ускорили Python API в 10 раз»
✅ «Kubernetes для начинающих: исчерпывающее руководство»
✅ «5 малоизвестных фичей PostgreSQL, которые ускорят вашу БД»
✅ «Docker Compose vs Kubernetes: когда использовать каждый»

**Bad Titles:**

❌ «Оптимизация» (слишком общее)
❌ «Вы не поверите, что мы сделали с API!» (кликбейт)
❌ «Часть 1» (неинформативное)
❌ «Backend development» (на английском, неспецифичное)

**Title Formula:**

- **How-to:** «Как [достичь результата] с помощью [технологии]»
- **List:** «X способов [улучшить что-то]»
- **Comparison:** «[A] vs [B]: что выбрать»
- **Case study:** «Как мы [достигли результата]: история [проекта]»
- **Tutorial:** «[Технология] для начинающих: полное руководство»

---

## Tone and Voice

### Informal «Ты» Form

Habr culture embraces informal address:

✅ **Good:**
```markdown
Если ты работаешь с Kubernetes, тебе наверняка приходилось сталкиваться с проблемами масштабирования.

Попробуй этот подход — он помог мне решить аналогичную задачу.
```

❌ **Too formal (not Habr style):**
```markdown
Если вы работаете с Kubernetes, вам наверняка приходилось сталкиваться с проблемами масштабирования.

Попробуйте этот подход — он помог решить аналогичную задачу.
```

### Personal Experience

Share your real experience:

✅ **Good:**
```markdown
Я столкнулся с этой проблемой, когда работал над проектом для e-commerce. Наш API обрабатывал 1000 запросов в секунду, и любое изменение занимало часы.

Мы перепробовали несколько подходов. Первый — кэширование — дал прирост всего 20%. Второй — оптимизация запросов к БД — оказался гораздо эффективнее.
```

❌ **Too generic:**
```markdown
Эта проблема часто встречается в проектах. API могут обрабатывать много запросов. Оптимизация важна.
```

### Conversational Style

Write as if talking to a colleague:

✅ **Good:**
```markdown
Окей, теперь самое интересное. Помнишь, я говорил про узкое место в БД? Вот как мы это пофиксили:

Первым делом добавили индекс. Казалось бы, базовая вещь, но многие про это забывают.
```

❌ **Too academic:**
```markdown
Далее представлена методика оптимизации производительности базы данных посредством внедрения индексирования.

Индексирование является фундаментальным подходом к улучшению производительности запросов.
```

---

## Code Examples Best Practices

### 1. Always Add Comments

Write comments in Russian:

✅ **Good:**
```python
# Создаем пул соединений с БД
pool = create_pool(
    host='localhost',
    port=5432,
    database='mydb',
    min_size=10,  # Минимум 10 соединений
    max_size=100  # Максимум 100 соединений
)

# Выполняем асинхронный запрос
async with pool.acquire() as conn:
    # Используем prepared statement для безопасности
    result = await conn.fetch(
        'SELECT * FROM users WHERE created_at > $1',
        datetime.now() - timedelta(days=7)
    )
```

### 2. Show Expected Output

Always show what code produces:

````markdown
```python
>>> fibonacci(10)
55

>>> fibonacci(20)
6765
```

или:

```bash
$ python main.py
Обработано 1000 записей за 1.23 секунды
Средняя скорость: 812 записей/сек
```
````

### 3. Keep Code Concise

Don't post entire files. Show relevant parts:

✅ **Good:**
```python
# main.py
async def process_orders(orders: List[Order]) -> List[Result]:
    """Обрабатывает заказы параллельно."""
    tasks = [process_single_order(order) for order in orders]
    return await asyncio.gather(*tasks)
```

❌ **Too much (use spoiler instead):**
```python
# main.py - entire 300 line file with imports, configs, etc.
import sys
import os
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
# ... 200+ more lines
```

### 4. Test Your Code

All code should be:
- ✅ Tested and working
- ✅ Runnable by readers
- ✅ Free of syntax errors
- ✅ Compatible with stated versions

---

## Tags (Hubs)

Choose 2-5 relevant hubs:

### Popular Technical Hubs

**Languages:**
- Python, JavaScript, TypeScript, Go, Rust, Java, C++, C#, PHP, Ruby

**Frameworks:**
- Django, Flask, FastAPI, React, Vue, Angular, Node.js, Spring

**Technologies:**
- Docker, Kubernetes, Git, PostgreSQL, MongoDB, Redis, Nginx

**Topics:**
- Machine Learning, DevOps, Backend, Frontend, Mobile, Security
- Architecture, Microservices, API, Databases, Testing

**Concepts:**
- Performance, Scalability, High Availability, Monitoring, CI/CD

### Choosing Right Tags

✅ **Good combination:**
- Python
- FastAPI
- Docker
- Backend
- Performance

❌ **Too generic:**
- Programming
- Development
- IT

❌ **Too many:**
- Python, Django, Flask, FastAPI, Backend, API, REST, GraphQL, PostgreSQL, Redis
  (Too many, choose 5 most relevant)

---

## Formatting Tips

### Headers Hierarchy

```markdown
# H1 - Заголовок статьи (один раз)

## H2 - Основные разделы

### H3 - Подразделы

#### H4 - Редко используется
```

### Text Emphasis

```markdown
**Bold** — для важных терминов и ключевых моментов

*Italic* — для emphasis (используется реже)

`code` — для команд, переменных, функций в тексте

~~Strikethrough~~ — для зачеркнутого текста
```

### Line Breaks

```markdown
Первый абзац с важной мыслью.

Второй абзац продолжает тему. Пустая строка между параграфами обязательна.

Третий абзац с новой идеей.
```

### Horizontal Rule

```markdown
Раздел 1

---

Раздел 2
```

---

## Complete Example Article

Here's a complete example following all Habr conventions:

````markdown
# Как мы перевели монолит на микросервисы и не умерли

Привет! Я backend-разработчик в небольшом стартапе. Недавно мы завершили миграцию с монолитной архитектуры на микросервисы, и я хочу поделиться опытом.

**Спойлер:** было больно, но мы справились.

**Что будет в статье:**
- Почему мы решились на миграцию
- Как выбирали стратегию
- Проблемы, с которыми столкнулись
- Результаты и метрики
- Что бы я сделал иначе

<cut />

## Наш монолит и его проблемы

Начнем с контекста. Наш проект — B2B SaaS для управления складами. Монолит на Django, PostgreSQL, Redis. 50 000 строк кода, 15 моделей БД.

Проблемы начались при росте до 100 корпоративных клиентов:

1. **Медленный деплой** — каждый релиз занимал 2 часа
2. **Невозможность масштабать** — приходилось поднимать весь монолит
3. **Coupling между модулями** — изменение в одном модуле ломало другие

### Метрики «до»

| Метрика | Значение |
|---------|----------|
| Время деплоя | 2 часа |
| Downtime при деплое | 15 минут |
| Время сборки | 20 минут |
| Расходы на серверы | $3000/месяц |

## Выбор стратегии миграции

Мы рассмотрели три подхода:

### 1. Big Bang (все сразу)

**Плюсы:**
- Быстро закончим
- Не нужна поддержка двух систем

**Минусы:**
- Огромный риск
- Невозможность отката
- Весь бизнес под угрозой

**Вердикт:** слишком рискованно для нас.

### 2. Strangler Fig (постепенное удушение)

**Плюсы:**
- Низкий риск
- Можно откатиться на любом этапе
- Бизнес работает без простоев

**Минусы:**
- Долго (6-12 месяцев)
- Нужна поддержка двух систем
- Сложная синхронизация

**Вердикт:** выбрали этот подход.

### 3. Гибрид

Компромисс между первыми двумя.

<spoiler title="Детали гибридного подхода">

Гибридный подход предполагает:

1. Разбить систему на 3-4 крупных сервиса
2. Мигрировать их поэтапно (по одному в месяц)
3. Не дробить на микро-микросервисы сразу

Мы не выбрали его, потому что наши модули слишком связаны.

</spoiler>

## Реализация

Выбрали такую последовательность:

```
Монолит → Монолит + Auth Service → + Inventory Service → + Notification Service
```

### Шаг 1: Authentication Service

Первым выделили сервис аутентификации. Почему именно его?

- Относительно независимый
- Понятные границы (users, sessions, permissions)
- Небольшой объем кода

**Архитектура:**

```python
# auth_service/main.py
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def login(username: str, password: str):
    """Аутентификация пользователя."""
    user = await authenticate(username, password)
    if not user:
        raise HTTPException(status_code=401)

    # Генерируем JWT токен
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/users/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Получение текущего пользователя."""
    user_id = decode_token(token)
    user = await get_user(user_id)
    return user
```

**Интеграция с монолитом:**

```python
# monolith/utils/auth.py
import requests

def verify_token(token: str) -> Optional[User]:
    """Проверяет токен через Auth Service."""
    response = requests.get(
        'http://auth-service:8000/users/me',
        headers={'Authorization': f'Bearer {token}'}
    )

    if response.status_code == 200:
        return User(**response.json())
    return None
```

### Результаты первого этапа

После выделения Auth Service:

- ✅ Деплой auth можно делать независимо
- ✅ Масштабирование только auth при нагрузке на аутентификацию
- ❌ Добавилась latency (~20ms на проверку токена)
- ❌ Новая точка отказа

## Проблемы и решения

### Проблема 1: Distributed Transactions

**Что случилось:**

Создание заказа требует:
1. Создать запись в Orders (Inventory Service)
2. Зарезервировать товары (Inventory Service)
3. Отправить уведомление (Notification Service)

Если шаг 3 падает, у нас заказ создан, но уведомление не отправлено.

**Решение:**

Внедрили pattern Saga с компенсацией:

```python
class CreateOrderSaga:
    """Saga для создания заказа."""

    async def execute(self, order_data: dict):
        # Шаг 1: создать заказ
        order = await self.create_order(order_data)

        try:
            # Шаг 2: зарезервировать товары
            await self.reserve_items(order.id)

            try:
                # Шаг 3: отправить уведомление
                await self.send_notification(order.id)

            except Exception as e:
                # Компенсация: отменяем резервацию
                await self.unreserve_items(order.id)
                raise

        except Exception as e:
            # Компенсация: удаляем заказ
            await self.delete_order(order.id)
            raise

        return order
```

### Проблема 2: Синхронизация данных

**Что случилось:**

Auth Service и Inventory Service оба нужна информация о пользователе. Дублировать БД или делать запросы?

**Решение:**

Event-driven подход с Kafka:

```python
# auth_service/events.py
async def on_user_created(user: User):
    """Публикует событие создания пользователя."""
    await kafka_producer.send(
        'user.created',
        value={
            'user_id': user.id,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }
    )

# inventory_service/consumers.py
async def handle_user_created(event: dict):
    """Обрабатывает событие создания пользователя."""
    # Сохраняем минимальную информацию в локальную БД
    await db.users.insert_one({
        'user_id': event['user_id'],
        'email': event['email']
    })
```

## Результаты

Через 8 месяцев миграция завершена. Итоговая архитектура:

```
┌─────────────┐
│   Монолит   │ (Core Business Logic)
└──────┬──────┘
       │
   ┌───┴────┬──────────┬────────────┐
   │        │          │            │
┌──▼───┐ ┌─▼────┐ ┌───▼───┐ ┌─────▼──────┐
│ Auth │ │ Inv. │ │ Notif.│ │  Analytics │
└──────┘ └──────┘ └───────┘ └────────────┘
```

### Метрики «после»

| Метрика | Было | Стало | Изменение |
|---------|------|-------|-----------|
| Время деплоя | 2 часа | 20 минут | **6x улучшение** |
| Downtime при деплое | 15 минут | 0 минут | **Zero downtime** |
| Время сборки | 20 минут | 5 минут | **4x улучшение** |
| Расходы на серверы | $3000 | $2400 | **20% экономия** |
| Частота деплоев | 2/неделю | 15/неделю | **7.5x рост** |

## Выводы и рекомендации

Что я узнал из этого опыта:

### 1. Не спешите с микросервисами

Если у тебя монолит на 10 000 строк и 3 разработчика — тебе не нужны микросервисы. Серьезно.

Микросервисы имеют смысл когда:
- Команда больше 15-20 человек
- Разные части системы масштабируются по-разному
- Нужны разные технологии для разных модулей

### 2. Начинайте с границ модулей

До миграции потратьте время на:
- Определение четких границ между модулями
- Минимизацию coupling'а
- Документирование зависимостей

У нас на это ушло 2 месяца, но это окупилось.

### 3. Event-driven — your friend

Использование событий вместо прямых вызовов помогло:
- Снизить coupling между сервисами
- Упростить добавление новых сервисов
- Реализовать аудит «из коробки»

### 4. Мониторинг критичен

В распределенной системе debugging в 10 раз сложнее. Инвестируйте в:
- Distributed tracing (мы используем Jaeger)
- Централизованные логи (ELK stack)
- Метрики для каждого сервиса (Prometheus + Grafana)

## Полезные ссылки

- [Martin Fowler: Microservices](https://martinfowler.com/articles/microservices.html)
- [Наш GitHub с примерами](https://github.com/example/microservices-migration)
- [Saga Pattern](https://microservices.io/patterns/data/saga.html)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)

---

Если у тебя есть вопросы или опыт миграции — делись в комментариях! Интересно послушать, как другие команды решали похожие задачи.
````

---

## Publishing Checklist

Before publishing on Habr:

### Content
- [ ] Title is specific and compelling
- [ ] Preview (before `<cut />`) is engaging (150-300 words)
- [ ] All code examples tested and working
- [ ] Code has Russian comments
- [ ] Images optimized and have alt text
- [ ] Links work and point to Russian resources when possible

### Formatting
- [ ] `<cut />` tag placed correctly
- [ ] Large code blocks in spoilers
- [ ] Proper headers hierarchy (H1 → H2 → H3)
- [ ] Tables formatted correctly
- [ ] Russian quotation marks « » used throughout
- [ ] Em dashes — with spaces

### Style
- [ ] Informal «ты» tone used
- [ ] Personal experience shared
- [ ] Conversational style
- [ ] Technical accuracy verified
- [ ] No marketing or promotional content

### Metadata
- [ ] 2-5 relevant tags selected
- [ ] Category chosen (personal blog vs company blog)
- [ ] Publication timing considered (weekday mornings best)

### Optional
- [ ] Submit for moderation (for rating boost)
- [ ] Cross-post to Telegram/social media
- [ ] Prepare to engage with comments

---

## Common Mistakes to Avoid

1. **Too much before cut**
   - ❌ Putting whole article before `<cut />`
   - ✅ Keep preview short and compelling

2. **No code examples**
   - ❌ Pure theory without practical examples
   - ✅ Show working code with output

3. **Untested code**
   - ❌ Code with syntax errors or bugs
   - ✅ Tested, runnable code

4. **Formal tone**
   - ❌ Using «вы» or third person
   - ✅ Using informal «ты»

5. **Generic titles**
   - ❌ «Микросервисы» or «Оптимизация кода»
   - ✅ «Как мы перешли на микросервисы за 8 месяцев»

6. **Wall of text**
   - ❌ Long paragraphs without breaks
   - ✅ Short paragraphs, code examples, lists, images

7. **No takeaways**
   - ❌ Story without conclusions
   - ✅ Clear recommendations and lessons learned

---

**Last updated:** 2025-11-20
