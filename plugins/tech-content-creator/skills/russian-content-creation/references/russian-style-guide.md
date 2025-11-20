# Russian Technical Writing Style Guide

## Overview

This comprehensive style guide covers Russian language conventions, technical terminology, grammar rules, and best practices for creating professional technical content that meets the standards of leading Russian publications.

## Table of Contents

1. [Typography and Punctuation](#typography-and-punctuation)
2. [Grammar and Syntax](#grammar-and-syntax)
3. [Technical Terminology](#technical-terminology)
4. [Tone and Voice](#tone-and-voice)
5. [Common Mistakes](#common-mistakes)
6. [Examples of Excellent Writing](#examples-of-excellent-writing)

---

## Typography and Punctuation

### Quotation Marks (Кавычки)

**Primary Quotes - French Guillemets « »**

Use for:
- Direct quotes: «Это прямая речь»
- Titles: книга «Чистый код»
- Irony or emphasis: «умный» алгоритм
- Technical terms on first mention: технология «машинного обучения»

**Nested Quotes - German Quotes „ "**

For quotes within quotes:
- «Он сказал: „Это важно"»
- «Термин „микросервисы" означает...»

**NEVER use:**
- ❌ English straight quotes: "text"
- ❌ Curly English quotes: "text"
- ❌ Apostrophes as quotes: 'text'

### Dashes and Hyphens

**Em Dash (—) - Длинное тире**

Use WITH spaces for:
- Sentence breaks: «Kubernetes — это система оркестрации»
- Before explanations: «Результат очевиден — производительность выросла»
- In dialogues: «— Как дела? — Отлично!»
- Replacing commas: «Команда — разработчики, тестировщики, DevOps — работала слаженно»

**En Dash (–) - Короткое тире**

Use WITHOUT spaces for:
- Ranges: «2020–2025», «страницы 10–15»
- Time periods: «январь–март»
- Scores: «3–2»

**Hyphen (-) - Дефис**

Use WITHOUT spaces for:
- Compound words: «full-stack-разработчик»
- Hyphenated terms: «DevOps-инженер»
- Prefixes: «веб-приложение», «микро-сервис»

**Spacing Rules:**
```
✅ Kubernetes — это система оркестрации.
❌ Kubernetes—это система оркестрации.
❌ Kubernetes -это система оркестрации.

✅ 2020–2025
❌ 2020 – 2025
❌ 2020-2025 (use en dash, not hyphen)

✅ full-stack-разработчик
❌ full stack разработчик
❌ full - stack - разработчик
```

### Special Characters

**№ (Numero Sign)**

Use for numbered items:
- «версия №5»
- «пункт №3.2»
- «сервер №12»

**Formatting:**
- ✅ «№5» or «№ 5» (no space or one space)
- ❌ «# 5» (don't use hashtag)
- ❌ «N 5» (don't use letter N)

**Percentage Sign (%)**

Use with non-breaking space:
- ✅ «30 %» (with space)
- ✅ «30%» (without space, also acceptable)
- Consistency: Choose one style per article

**Degree Symbol (°)**

For temperatures:
- ✅ «25 °C» (with space before °)
- ✅ «25°C» (without space, also acceptable)

### Ellipsis (Многоточие)

**Three Dots (…)**

- Use single character … or three dots ...
- ✅ «Мы пытались...»
- ✅ «Мы пытались…»
- ❌ «Мы пытались. . .» (not with spaces)

**With Other Punctuation:**
- Question: «Почему?..»
- Exclamation: «Невероятно!..»

### Spacing Rules

**No Space Before:**
- Comma: «текст, продолжение»
- Period: «текст. Новое предложение.»
- Colon: «результат: успех»
- Semicolon: «первое; второе»
- Question mark: «Как?»
- Exclamation: «Отлично!»

**Space After:**
- All punctuation marks
- Exception: Opening quotes « have no space after

**Non-Breaking Spaces (Неразрывный пробел)**

Use before:
- Units: «100 Кб», «5 мс», «30 ГБ»
- Percentages: «50 %»
- Short words at line end: «в 2025 году»

**HTML Entity:** `&nbsp;` or Unicode `\u00A0`

### Bullet Points and Lists

**Unordered Lists:**
```markdown
- Первый пункт
- Второй пункт
  - Вложенный пункт
  - Еще один вложенный
- Третий пункт
```

**Ordered Lists:**
```markdown
1. Первый шаг
2. Второй шаг
3. Третий шаг
```

**Punctuation in Lists:**
- Use semicolon (;) at end of each item except last
- Use period (.) at end of last item
- Or omit all punctuation for simple lists

**Example:**
```
Требования к системе:
- процессор: Intel Core i5 или выше;
- память: 8 ГБ RAM;
- диск: 256 ГБ SSD.
```

---

## Grammar and Syntax

### Formal vs. Informal Address

**Informal «ты» (you - singular, informal)**

Use in:
- Habr articles (tech community culture)
- Casual blog posts
- Tutorials for beginners
- Peer-to-peer tone

**Example:**
> «Если ты хочешь изучить Kubernetes, начни с основ. Тебе понадобится Docker и базовое понимание контейнеризации.»

**Formal «вы» (you - plural/formal)**

Use in:
- Business publications (VC.ru, RBC, Vedomosti)
- Corporate communications
- Professional contexts
- When addressing executives

**Example:**
> «Если вы хотите внедрить Kubernetes, рекомендуем начать с анализа текущей инфраструктуры. Вам понадобится провести аудит существующих систем.»

**Third Person (Avoiding Direct Address)**

Use in:
- Journalistic articles
- Research papers
- Formal reports
- Objective analysis

**Example:**
> «Для внедрения Kubernetes требуется провести аудит существующей инфраструктуры. Команде разработки необходимо оценить текущие системы.»

### Sentence Structure

**Active Voice (Preferred)**

✅ «Разработчики создали новую архитектуру.»
❌ «Новая архитектура была создана разработчиками.»

✅ «Мы оптимизировали производительность на 40%.»
❌ «Производительность была оптимизирована на 40%.»

**Exceptions for Passive Voice:**
- When actor is unknown: «Ошибка была обнаружена в логах»
- When focus is on result: «Система была успешно запущена»
- In formal reports: «Исследование было проведено в период с января по март»

### Paragraph Structure

**Opening Sentence:**
- State main idea clearly
- Hook reader's attention
- Set paragraph direction

**Supporting Sentences:**
- Develop the main idea
- Provide examples, evidence
- Maintain logical flow

**Closing Sentence:**
- Summarize or transition
- Link to next paragraph
- Provide conclusion

**Length:**
- 3-5 sentences per paragraph
- Avoid single-sentence paragraphs (except for emphasis)
- Break up long paragraphs (>7 sentences)

### Verb Tenses

**Present Tense (Настоящее время)**

For:
- General truths: «Kubernetes оркеstrирует контейнеры»
- Current situations: «Микросервисы становятся стандартом»
- Technical descriptions: «Функция возвращает результат»

**Past Tense (Прошедшее время)**

For:
- Historical events: «Docker был выпущен в 2013 году»
- Case studies: «Мы внедрили новую архитектуру»
- Results: «Производительность увеличилась на 40%»

**Future Tense (Будущее время)**

For:
- Predictions: «Технология будет развиваться»
- Plans: «Мы реализуем эту функцию в следующей версии»
- Instructions: «Далее вы установите зависимости»

### Agreement and Cases

**Subject-Verb Agreement:**

Singular:
- «Сервис работает корректно»
- «Приложение запускается»

Plural:
- «Сервисы работают корректно»
- «Приложения запускаются»

**Case Usage:**

Nominative (Именительный): «Kubernetes — это инструмент»
Genitive (Родительный): «Установка Kubernetes»
Dative (Дательный): «Благодаря Kubernetes»
Accusative (Винительный): «Мы используем Kubernetes»
Instrumental (Творительный): «Работа с Kubernetes»
Prepositional (Предложный): «О Kubernetes»

---

## Technical Terminology

### Terminology Translation Strategy

**Three-Tier Approach:**

1. **Keep English (Most Common)**
   - Widely adopted terms
   - No good Russian equivalent
   - International standards

   Examples: DevOps, API, SaaS, CI/CD, Backend, Frontend

2. **Translate to Russian**
   - Established Russian terms exist
   - Better comprehension
   - Official terminology

   Examples: база данных (database), сеть (network), безопасность (security)

3. **Hybrid (English + Russian)**
   - First mention: both languages
   - Subsequent: English term
   - Parenthetical Russian translation

   Example: «Machine Learning (машинное обучение, ML)» → then «ML»

### Technical Terms Glossary (EN → RU)

**Development & Architecture:**

| English | Russian | Usage Note |
|---------|---------|------------|
| API | API | Keep English |
| Backend | Backend или бэкенд | Both acceptable |
| Frontend | Frontend или фронтенд | Both acceptable |
| Full-stack | Full-stack | Keep English, hyphenate: full-stack-разработчик |
| Microservices | Микросервисы | Translate |
| Monolith | Монолит | Translate |
| Architecture | Архитектура | Translate |
| Design pattern | Паттерн проектирования | Translate |
| Framework | Фреймворк | Transliterate |
| Library | Библиотека | Translate |
| Database | База данных (БД) | Translate |
| Cache | Кэш | Transliterate |
| Queue | Очередь | Translate |
| Load balancer | Балансировщик нагрузки | Translate |

**DevOps & Infrastructure:**

| English | Russian | Usage Note |
|---------|---------|------------|
| DevOps | DevOps | Keep English |
| CI/CD | CI/CD | Keep English, explain on first use |
| Container | Контейнер | Translate |
| Docker | Docker | Keep English |
| Kubernetes | Kubernetes | Keep English, colloq. «k8s» |
| Deployment | Развертывание or деплой | Translate or transliterate |
| Pipeline | Пайплайн or конвейер | Both acceptable |
| Orchestration | Оркестрация | Translate |
| Infrastructure as Code | Инфраструктура как код (IaC) | Translate + acronym |
| Monitoring | Мониторинг | Transliterate |
| Logging | Логирование | Transliterate |
| Cloud | Облако or облачные вычисления | Translate |

**Programming Concepts:**

| English | Russian | Usage Note |
|---------|---------|------------|
| Variable | Переменная | Translate |
| Function | Функция | Translate |
| Class | Класс | Translate |
| Object | Объект | Translate |
| Method | Метод | Translate |
| Interface | Интерфейс | Translate |
| Loop | Цикл | Translate |
| Condition | Условие | Translate |
| Exception | Исключение | Translate |
| Error | Ошибка | Translate |
| Bug | Баг | Transliterate (colloq.) or ошибка |
| Debug | Отладка | Translate |
| Refactoring | Рефакторинг | Transliterate |
| Code review | Ревью кода or code review | Both acceptable |

**Data & ML:**

| English | Russian | Usage Note |
|---------|---------|------------|
| Machine Learning | Machine Learning (ML) or машинное обучение | Hybrid on first use |
| Deep Learning | Deep Learning or глубокое обучение | Hybrid recommended |
| Neural Network | Нейронная сеть | Translate |
| Dataset | Датасет or набор данных | Both acceptable |
| Model | Модель | Translate |
| Training | Обучение | Translate |
| Inference | Инференс or вывод | Both acceptable |
| Data Science | Data Science or наука о данных | Keep English preferred |
| Big Data | Big Data or большие данные | Keep English preferred |
| Analytics | Аналитика | Translate |

**Agile & Project Management:**

| English | Russian | Usage Note |
|---------|---------|------------|
| Agile | Agile | Keep English |
| Scrum | Scrum | Keep English |
| Sprint | Спринт | Transliterate |
| Stand-up | Стендап | Transliterate |
| Backlog | Бэклог | Transliterate |
| User Story | User Story or пользовательская история | Keep English preferred |
| Epic | Эпик | Transliterate |
| Stakeholder | Стейкхолдер or заинтересованное лицо | Both acceptable |
| Product Owner | Product Owner | Keep English |

### Abbreviations and Acronyms

**Rules:**
1. Spell out on first use with Russian translation
2. Include abbreviation in parentheses
3. Use abbreviation consistently afterward

**Examples:**

First mention:
> «Continuous Integration/Continuous Delivery (непрерывная интеграция и развертывание, CI/CD) — это практика автоматизации.»

Subsequent uses:
> «Внедрение CI/CD позволяет ускорить разработку.»

**Common Abbreviations:**

- **API** — Application Programming Interface (программный интерфейс приложения)
- **REST** — Representational State Transfer
- **CRUD** — Create, Read, Update, Delete (создание, чтение, обновление, удаление)
- **OOP** — Object-Oriented Programming (объектно-ориентированное программирование, ООП)
- **SQL** — Structured Query Language (язык структурированных запросов)
- **NoSQL** — Not Only SQL
- **HTTP/HTTPS** — HyperText Transfer Protocol (Secure)
- **SSL/TLS** — Secure Sockets Layer / Transport Layer Security
- **AWS** — Amazon Web Services
- **GCP** — Google Cloud Platform
- **VM** — Virtual Machine (виртуальная машина)

### Code-Related Terms in Text

**Variable and Function Names:**

Keep in English:
```markdown
Функция `calculateTotal()` принимает массив `items` и возвращает `number`.
```

Don't translate:
```markdown
❌ Функция `вычислитьИтого()` принимает массив `элементы`...
```

**Comments in Code:**

Use Russian for article code examples:
```python
# Вычисляем сумму всех элементов
total = sum(items)

# Проверяем наличие дубликатов
if len(items) != len(set(items)):
    raise ValueError("Обнаружены дубликаты")
```

But keep technical terms:
```python
# Инициализируем connection pool
pool = ConnectionPool(max_connections=10)

# Выполняем query к database
result = pool.execute("SELECT * FROM users")
```

---

## Tone and Voice

### Professional but Approachable

**Goal:** Sound expert without being condescending

✅ Good:
> «Kubernetes решает проблему оркестрации контейнеров. Рассмотрим, как он работает на практике.»

❌ Too casual:
> «Короче, Kubernetes — это вообще огонь для контейнеров!»

❌ Too formal:
> «Настоящим предлагается рассмотрение функционального назначения системы Kubernetes в контексте оркестрации контейнеризованных приложений.»

### Confidence Without Arrogance

**Show expertise humbly:**

✅ Good:
> «По нашему опыту, микросервисная архитектура лучше подходит для крупных проектов с независимыми командами.»

❌ Arrogant:
> «Любой, кто использует монолит в 2025 году, просто не понимает современную разработку.»

### Clear Technical Explanations

**Explain complex concepts simply:**

✅ Good:
> «Контейнер — это изолированная среда выполнения приложения. Представьте его как легковесную виртуальную машину, которая содержит только необходимое для работы приложения: код, библиотеки и зависимости.»

❌ Unclear:
> «Контейнер — это способ виртуализации на уровне операционной системы для запуска изолированных user-space инстансов.»

### Platform-Specific Tone

**Habr (Informal, peer-to-peer):**
```markdown
Привет! Сегодня разберем, как настроить мониторинг в Kubernetes. Если ты только начинаешь работать с k8s, эта статья для тебя.

Первым делом нужно установить Prometheus. Я покажу самый простой способ — через Helm chart.
```

**VC.ru (Business-focused, semi-formal):**
```markdown
Мониторинг инфраструктуры — критически важная задача для любого бизнеса. По данным исследования Gartner, 70% компаний сталкиваются с проблемами из-за недостаточного мониторинга.

Рассмотрим, как построить эффективную систему мониторинга на базе Prometheus и Grafana.
```

**RBC/Vedomosti (Formal, journalistic):**
```markdown
Российские компании активно внедряют системы мониторинга инфраструктуры. По оценкам экспертов, объем рынка решений для мониторинга вырос на 35% в 2024 году.

«Без качественного мониторинга невозможно обеспечить надежность сервисов», — комментирует технический директор крупного российского банка.
```

---

## Common Mistakes

### 1. Mixed Language Constructions

❌ **Wrong:**
```
Мы используем continuous integration для автоматизации.
Наш team работает в agile approach.
```

✅ **Correct:**
```
Мы используем Continuous Integration (непрерывную интеграцию, CI) для автоматизации.
Наша команда работает по методологии Agile.
```

### 2. Incorrect Quotation Marks

❌ **Wrong:**
```
Он сказал "это важно".
Книга "Чистый код" учит писать качественный код.
```

✅ **Correct:**
```
Он сказал «это важно».
Книга «Чистый код» учит писать качественный код.
```

### 3. Dash Spacing Errors

❌ **Wrong:**
```
Docker— это платформа для контейнеризации.
Docker —это платформа для контейнеризации.
Docker-это платформа для контейнеризации.
```

✅ **Correct:**
```
Docker — это платформа для контейнеризации.
```

### 4. Transliteration Instead of Translation

❌ **Wrong:**
```
дата сайнс, дата бэйс, нетворк, секьюрити
```

✅ **Correct:**
```
Data Science (or наука о данных), база данных, сеть, безопасность
```

### 5. Incorrect Case Usage

❌ **Wrong:**
```
Установка для Kubernetes (should be: Kubernetes)
Работа в Docker (should be: с Docker)
```

✅ **Correct:**
```
Установка Kubernetes (genitive case)
Работа с Docker (instrumental case)
```

### 6. Anglicisms in Formal Text

❌ **Wrong (for formal context):**
```
Мы засетапили сервер и задеплоили апп.
```

✅ **Correct:**
```
Мы настроили сервер и развернули приложение.
```

**Note:** Some anglicisms are acceptable in informal Habr articles but not in business publications.

### 7. Overly Long Sentences

❌ **Wrong:**
```
Kubernetes, который представляет собой платформу для оркестрации контейнеров, разработанную Google и впоследствии переданную в управление Cloud Native Computing Foundation, позволяет автоматизировать развертывание, масштабирование и управление контейнеризованными приложениями, что делает его незаменимым инструментом для современных DevOps-команд.
```

✅ **Correct:**
```
Kubernetes — это платформа для оркестрации контейнеров, разработанная Google. В 2015 году проект был передан Cloud Native Computing Foundation. Kubernetes автоматизирует развертывание, масштабирование и управление контейнеризованными приложениями. Это незаменимый инструмент для современных DevOps-команд.
```

---

## Examples of Excellent Writing

### Example 1: Technical Article Opening (Habr Style)

```markdown
# Как мы ускорили наше приложение на 300%: история оптимизации

Привет! Меня зовут Алексей, я backend-разработчик в стартапе EdTech. Недавно мы столкнулись с серьезной проблемой — наше приложение начало тормозить при 1000 одновременных пользователей. Это было критично: впереди начало учебного года, и мы ожидали десятикратный рост нагрузки.

В этой статье я расскажу, как мы провели профилирование, нашли узкие места и оптимизировали систему. Спойлер: нам удалось увеличить производительность в три раза и выдержать пиковую нагрузку в 15 000 пользователей.

**Что будет в статье:**
- Профилирование Python-приложения
- Оптимизация работы с базой данных
- Внедрение кэширования с Redis
- Асинхронная обработка задач с Celery

**Дисклеймер:** Все цифры реальные, код упрощен для наглядности.

<cut />

## Проблема: медленные ответы API

Все началось с жалоб от пользователей в поддержку. «Страница загружается по 5-10 секунд», — писали они. Мы проверили мониторинг и ужаснулись: средний response time API вырос до 3.5 секунд, а 95-й перцентиль достигал 8 секунд.

График в Grafana выглядел примерно так:

[График response time]

Стало очевидно — нужна срочная оптимизация.
```

**Why this works:**
- Engaging hook with specific metrics
- Clear problem statement
- Promise of practical value
- Friendly, conversational tone
- Structured with clear sections
- Use of habr-specific `<cut />` tag

### Example 2: Business Case Study (VC.ru Style)

```markdown
# Как мы снизили расходы на инфраструктуру на 40%: переход с монолита на микросервисы

**TL;DR:** Наша команда мигрировала legacy-монолит на микросервисную архитектуру. Результаты через 6 месяцев: экономия $15 000/месяц на инфраструктуре, ускорение релизов в 3 раза, снижение количества критических инцидентов на 60%.

---

## Контекст

Наша компания — B2B SaaS-платформа для управления проектами с 5000+ корпоративных клиентов. К 2024 году мы столкнулись с серьезными проблемами:

- **Медленная разработка:** любое изменение требовало полного релиза монолита
- **Высокие расходы:** сервера работали на 20% мощности, но нужно было держать запас
- **Частые проблемы:** падение одного модуля роняло всю систему

«Мы теряли конкурентные преимущества из-за технического долга», — комментирует наш CTO Михаил Петров.

## Решение

После аудита архитектуры мы приняли решение о поэтапной миграции на микросервисы. Процесс занял 9 месяцев и включал четыре этапа:

### 1. Анализ и декомпозиция (2 месяца)

Мы выделили шесть основных доменов...
```

**Why this works:**
- Strong business focus with ROI metrics
- Clear structure with TL;DR
- Quotes from decision-makers
- Professional, formal tone
- Emphasis on business outcomes
- Specific timeline and stages

### Example 3: Technical Tutorial (Habr Style)

```markdown
# Kubernetes для начинающих: запускаем первое приложение за 15 минут

## Для кого этот туториал

Если ты слышал о Kubernetes, но пока не пробовал его на практике — эта статья для тебя. Мы пошагово запустим простое приложение в локальном кластере. Никакого DevOps-опыта не требуется!

**Что понадобится:**
- Компьютер с 4+ ГБ RAM
- 15 минут времени
- Базовое знание командной строки

**Что установим:**
- Docker Desktop (включает Kubernetes)
- kubectl (инструмент управления кластером)

**Что создадим:**
- Простое веб-приложение на Python
- Docker-образ
- Kubernetes Deployment и Service

Поехали!

## Шаг 1: Устанавливаем Docker Desktop

Скачай Docker Desktop для своей ОС с [официального сайта](https://docker.com).

**Для macOS:**
```bash
brew install --cask docker
```

**Для Windows:**
1. Скачай установщик
2. Запусти с правами администратора
3. Перезагрузи компьютер

**Проверь установку:**
```bash
docker --version
# Ожидаемый вывод: Docker version 24.0.0, build xxx
```

**Включи Kubernetes:**
1. Открой Docker Desktop
2. Settings → Kubernetes
3. Поставь галочку «Enable Kubernetes»
4. Нажми «Apply & restart»

Подожди 2-3 минуты, пока Kubernetes запустится.

**Проверь, что все работает:**
```bash
kubectl version --short
# Ожидаемый вывод:
# Client Version: v1.28.0
# Server Version: v1.28.0
```

Если видишь обе версии — отлично, идем дальше!
```

**Why this works:**
- Clear target audience
- Prerequisites listed upfront
- Step-by-step instructions
- Expected output shown
- Encouragement and friendly tone
- Code examples with explanations
- Visual indicators (✓, →, etc.)

### Example 4: Research Article (RBC Style)

```markdown
# Российские компании увеличили инвестиции в облачные технологии на 45% в 2024 году

**МОСКВА, 20 ноября.** Объем российского рынка облачных сервисов вырос на 45% в 2024 году и достиг 180 млрд рублей. Об этом свидетельствуют данные исследования, проведенного аналитическим агентством TAdviser.

Основными драйверами роста стали переход на отечественные облачные платформы и цифровая трансформация бизнеса на фоне импортозамещения.

## Структура рынка

По данным исследования, наибольший рост показал сегмент Infrastructure as a Service (IaaS) — 52%. Доля российских провайдеров в этом сегменте достигла 78%, увеличившись с 65% годом ранее.

«Мы наблюдаем массовый переход компаний с зарубежных облачных платформ на российские аналоги», — комментирует исполнительный директор Yandex Cloud Александр Краснов.

Крупнейшие игроки рынка:
- Yandex Cloud — 28% рынка
- VK Cloud — 22%
- SberCloud — 18%
- МТС Cloud — 10%

## Отраслевой анализ

Наибольший прирост инвестиций в облачные технологии продемонстрировали:

1. **Финансовый сектор** — рост на 67%
2. **Ритейл и e-commerce** — рост на 55%
3. **Телеком** — рост на 43%

По словам аналитиков, такая динамика связана с необходимостью обеспечения отказоустойчивости и масштабируемости IT-инфраструктуры.
```

**Why this works:**
- Journalistic lead with key facts
- Objective, third-person tone
- Specific data and sources
- Expert quotes with attribution
- Clear structure
- Professional language
- No direct address to reader

---

## Checklist for Quality Russian Content

Use this checklist before finalizing any content:

### Typography
- [ ] All quotes use « » (not " ")
- [ ] Em dashes (—) have spaces on both sides
- [ ] En dashes (–) have no spaces (for ranges)
- [ ] Hyphens (-) used correctly in compound words
- [ ] № used for numbered items
- [ ] Non-breaking spaces before units (100 Кб)

### Language
- [ ] Consistent formal/informal address throughout
- [ ] Technical terms translated or explained on first use
- [ ] No mixed-language constructions
- [ ] Active voice preferred
- [ ] Clear, concise sentences

### Structure
- [ ] Engaging opening hook
- [ ] Logical flow between paragraphs
- [ ] Clear headings hierarchy
- [ ] Appropriate paragraph length (3-5 sentences)
- [ ] Strong conclusion

### Content
- [ ] Technically accurate
- [ ] Code examples working and explained
- [ ] Appropriate tone for platform
- [ ] Practical, actionable information
- [ ] Sources and references cited

### SEO
- [ ] Title includes target keyword
- [ ] Meta description compelling and <160 chars
- [ ] Headings structured (H1→H2→H3)
- [ ] Alt text for images in Russian
- [ ] Internal links included

---

## Additional Resources

- **Главред** (glvrd.ru) — tool for improving text readability
- **Орфограммка** (orfogrammka.ru) — spelling and grammar checker
- **Типограф Лебедева** — typography checker
- **Словари:** gramota.ru, dic.academic.ru

---

**Last updated:** 2025-11-20
