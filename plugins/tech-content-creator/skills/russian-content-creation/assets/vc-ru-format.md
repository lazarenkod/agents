# VC.ru Format Guide

## Overview

VC.ru is Russia's leading business and technology media platform focused on startups, entrepreneurship, marketing, and investments. This guide covers VC.ru-specific formatting, style conventions, and best practices.

**Platform:** https://vc.ru
**Audience:** Entrepreneurs, founders, executives, investors, marketers
**Monthly readers:** 10+ million
**Tone:** Business-focused, semi-formal, results-oriented

---

## Core Principles

### 1. Business Value First

Every piece of content must demonstrate clear business value:

✅ **Good:**
> Мы внедрили чат-бота для поддержки и снизили нагрузку на операторов на 60%. Это позволило сократить расходы на поддержку с 500 000 до 200 000 рублей в месяц при росте NPS с 45 до 68.

❌ **Too technical (better for Habr):**
> Мы внедрили чат-бота на базе NLP-модели BERT с fine-tuning на нашем датасете из 10 000 диалогов. Использовали FastAPI для backend и React для интерфейса.

### 2. Metrics and Numbers

Quantify everything possible:

✅ **Good:**
- Рост выручки на 145%
- Сокращение CAC с $150 до $45
- Увеличение конверсии из trial в paid с 12% до 28%
- ROI маркетинговой кампании: 320%

❌ **Vague:**
- Значительный рост выручки
- Снижение стоимости привлечения
- Улучшение конверсии
- Положительный эффект от кампании

### 3. Actionable Insights

Readers should finish with clear takeaways:

✅ **Good:**
> **Что можно сделать прямо сейчас:**
> 1. Проведите A/B тест на landing page — это бесплатно и занимает 1 день
> 2. Настройте email-цепочку для trial users (увеличит конверсию на 15-20%)
> 3. Добавьте калькулятор ROI на сайт — конверсия в demo вырастет на 30%

❌ **Generic:**
> Рекомендуем проводить тесты и улучшать конверсию. Это важно для бизнеса.

---

## Content Structure

### Standard VC.ru Article Format

```markdown
# Цепляющий заголовок с конкретным результатом

**TL;DR:** Краткое резюме статьи в 2-3 предложениях. Обязательно включите ключевые метрики и выводы.

---

## Контекст

Кто вы, что за компания/проект, какая была ситуация.

**Ключевые факты:**
- Размер компании/рынка
- Начальные метрики
- Проблема или возможность

## Проблема / Вызов

Детальное описание проблемы с цифрами и контекстом.

## Решение

Что и как вы сделали. Процесс, этапы, решения.

### Этап 1: [Название]
### Этап 2: [Название]
### Этап 3: [Название]

## Результаты

Конкретные метрики до и после.

**До внедрения:**
- Метрика 1: значение
- Метрика 2: значение

**После внедрения:**
- Метрика 1: значение (+X%)
- Метрика 2: значение (+Y%)

## Инсайты / Выводы

Что узнали, что сработало, что нет.

## Рекомендации

Что можно применить прямо сейчас.

---

**[Опционально: о компании и авторе]**
```

---

## Title Formulas

### Result-Driven Titles

✅ **Excellent titles:**

- «Как мы увеличили конверсию на 300% и снизили CAC вдвое»
- «От $0 до $100k MRR за 9 месяцев: что сработало»
- «5 изменений на landing page, которые подняли конверсию с 2% до 7%»
- «Как привлечь первых 1000 платящих клиентов без бюджета на маркетинг»

✅ **Question-based titles:**

- «Почему 80% SaaS-стартапов умирают в первый год?»
- «Какой pricing убивает ваш SaaS: анализ 500 компаний»
- «Нужен ли вашему бизнесу мобильный app? Считаем ROI»

✅ **Controversial/provocative:**

- «Мы потратили $500k на маркетинг и не получили ни одного клиента»
- «Почему я закрыл прибыльный стартап с выручкой $2M»
- «Unit-экономика Zoom, Slack и Notion: что не так»

❌ **Bad titles:**

- «Маркетинг для стартапов» (слишком общее)
- «Наша история успеха» (неконкретное)
- «Часть 2: продолжение» (неинформативное)
- «То, что должен знать каждый предприниматель» (банально)

### Title Structure

**Формула 1: Результат + Метод**
```
Как [достигли результата] с помощью [метода/инструмента]

Примеры:
- Как мы выросли до 10 000 пользователей с помощью Product Hunt
- Как увеличить LTV на 40% с помощью email-маркетинга
```

**Формула 2: Цифры + Инсайт**
```
[Конкретная цифра]: [неочевидный инсайт]

Примеры:
- 73% стартапов выбирают неправильный pricing model
- $2M выручки: почему мы решили закрыть проект
```

**Формула 3: Проблема + Решение**
```
[Проблема]: как [решили]

Примеры:
- Churn rate 15% в месяц: как мы снизили до 3%
- Конверсия в trial 1%: 7 изменений, которые помогли
```

---

## TL;DR (Too Long; Didn't Read)

**Always include TL;DR at the top** — many readers only read this.

### TL;DR Structure

1. **Что сделали** (1 предложение)
2. **Ключевые результаты** (конкретные цифры)
3. **Главный инсайт** (1 предложение)

### Examples

✅ **Excellent TL;DR:**

> **TL;DR:** Мы переделали onboarding в нашем B2B SaaS и увеличили конверсию из trial в paid с 12% до 31% за 2 месяца. Ключ к успеху — персонализация для разных сегментов и активация в первые 24 часа. ROI изменений: 850%.

✅ **Good TL;DR:**

> **TL;DR:** За 6 месяцев вырастили ARR с $50k до $300k. Основные драйверы: переход с freemium на free trial (+80% qualified leads) и внедрение customer success (+60% retention). Главное обучение: product-market fit важнее marketing.

❌ **Weak TL;DR:**

> **TL;DR:** В статье рассказываем о нашем опыте роста стартапа и делимся полезными советами.

---

## Visual Elements

### 1. Screenshots and Charts

Use visual elements generously:

- **Dashboards:** Analytics, metrics, KPIs
- **Charts:** Growth graphs, funnel analysis, cohort retention
- **Screenshots:** Product features, A/B test results
- **Comparison tables:** Before/after metrics

**Example annotation:**

```markdown
![График роста MRR](./images/mrr-growth.png)

*MRR вырос с $12k до $87k за 9 месяцев. Резкий скачок в июне связан с запуском enterprise-тарифа.*
```

### 2. Data Visualization

Present data visually when possible:

**Instead of text:**
> В январе было 100 пользователей, в феврале 150, в марте 280, в апреле 520.

**Use visual:**
```
Рост пользователей:
┌────┬────────┐
│ Ян │ ████   │ 100
│ Фв │ ██████ │ 150
│ Мр │ ██████████████ │ 280
│ Ап │ ████████████████████████████ │ 520
└────┴────────┘
```

Or a table:

| Месяц | Пользователи | Рост |
|-------|--------------|------|
| Январь | 100 | - |
| Февраль | 150 | +50% |
| Март | 280 | +87% |
| Апрель | 520 | +86% |

### 3. Quotes from Founders/Experts

Add credibility with quotes:

```markdown
> «Мы потратили первые 6 месяцев на поиск product-market fit. Без этого любой рост — это просто vanity metrics», — рассказывает Алексей Петров, CEO Startup Inc.
```

**Quote formatting:**
- Use Russian quotation marks « »
- Include full name, title, company
- Keep quotes relevant and insightful
- Don't quote yourself too much

---

## Formatting Best Practices

### Use Bold for Key Points

Make content skimmable:

```markdown
Мы протестировали 15 каналов привлечения. **Лучшие результаты показали:**

- **Content marketing:** CAC $45, LTV/CAC 4.2
- **Партнерская программа:** CAC $32, LTV/CAC 5.8
- **Cold outreach:** CAC $120, LTV/CAC 2.1

**Вывод:** партнерка приносит самых качественных клиентов при низком CAC.
```

### Bullet Points and Lists

Use extensively for readability:

✅ **Good (scannable):**

```markdown
**Что сработало:**
- Внедрение free trial вместо freemium: +80% qualified leads
- Email onboarding: +45% activation
- In-app tooltips: +32% feature adoption
- Customer success звонки: +60% retention

**Что не сработало:**
- Facebook ads: CAC $280 при LTV $150
- Influencer marketing: 0 конверсий
- Content marketing: долгий ROI (6+ месяцев)
```

❌ **Bad (wall of text):**

```markdown
Мы попробовали разные подходы. Некоторые сработали хорошо, например free trial и email onboarding. Другие не принесли результатов, включая Facebook рекламу где CAC оказался выше LTV.
```

### Numbers and Metrics

**Format numbers clearly:**

✅ **Good:**
- $125,000 ARR
- 15 000 пользователей
- 2.5M impressions
- +145% рост
- CAC $45 → $23 (-51%)

❌ **Inconsistent:**
- 125000 долларов (no separators)
- 15k users (mixing languages)
- 2500000 (hard to read)

### Comparison Tables

**Before/After tables are powerful:**

| Метрика | До | После | Изменение |
|---------|-----|-------|-----------|
| MRR | $12,000 | $87,000 | **+625%** |
| CAC | $150 | $45 | **-70%** |
| Churn | 15%/мес | 3%/мес | **-80%** |
| LTV/CAC | 1.2 | 4.8 | **+300%** |
| NPS | 23 | 67 | **+191%** |

---

## Content Types

### 1. Case Study (Кейс)

**Purpose:** Share real experience with metrics and learnings

**Structure:**
1. **Контекст:** Company/project background
2. **Проблема:** Specific challenge with impact
3. **Решение:** What you did (process, tools, timeline)
4. **Результаты:** Concrete metrics (before/after)
5. **Инсайты:** What learned, what would do differently

**Length:** 1,500-3,000 words

**Example opening:**

```markdown
# Как мы снизили churn с 15% до 3% за 4 месяца

**TL;DR:** Наш SaaS терял 15% клиентов каждый месяц. Мы внедрили customer success программу, переделали onboarding и добавили in-app помощь. Churn упал до 3%, MRR вырос на 180%. Инвестиции: $15k, ROI: 450%.

---

## Контекст

Мы — B2B SaaS для автоматизации HR процессов. 200 клиентов, MRR $50k. Средний чек $250/месяц.

**Проблема:** 15% клиентов уходили каждый месяц. При таком churn unit-экономика не сходилась: LTV $2000, CAC $1500, LTV/CAC = 1.3 (нужно минимум 3).
```

### 2. Growth Story (История роста)

**Purpose:** Inspire with growth metrics and strategy

**Structure:**
1. **Старт:** Where you began (numbers)
2. **Путь:** Key milestones and decisions
3. **Рост:** Growth drivers and channels
4. **Текущее состояние:** Where you are now
5. **Планы:** Next steps and goals

**Length:** 1,500-2,500 words

**Example opening:**

```markdown
# От идеи до $500k ARR за 18 месяцев: наша история

**TL;DR:** Мы запустили B2B SaaS в июле 2023 с $0 и достигли $500k ARR к декабрю 2024. Обошлись без венчурных инвестиций, выросли на content marketing и product-led growth. Делимся цифрами, стратегией и ошибками.

---

**Основные метрики сегодня:**
- ARR: $500,000
- Клиентов: 850
- Средний чек: $49/месяц
- CAC: $85
- LTV: $588
- Churn: 4%/месяц
- Команда: 8 человек
```

### 3. Analysis/Research (Аналитика)

**Purpose:** Provide data-driven insights on market/trends

**Structure:**
1. **Исследовательский вопрос:** What you analyzed
2. **Методология:** How you collected data
3. **Данные:** Raw findings with visualizations
4. **Анализ:** What the data means
5. **Выводы:** Implications for business

**Length:** 2,000-4,000 words

**Example opening:**

```markdown
# Мы проанализировали 500 SaaS-стартапов: вот что отличает успешные

**TL;DR:** Изучили 500 SaaS компаний основанных в 2020-2023. Из них 127 достигли $1M ARR. Ключевые паттерны успеха: time to value <1 час (73% успешных vs 12% неуспешных), customer success с первого дня (81% vs 23%), pricing выше среднего по рынку (медиана $79 vs $29).

---

## Методология

**Выборка:** 500 B2B SaaS компаний из США и Европы, основанных между январем 2020 и декабрем 2023.

**Источники данных:**
- Crunchbase (funding, founding dates)
- Публичные отчеты и блоги компаний
- Интервью с 45 основателями
- SaaS metrics от Baremetrics, ChartMogul

**Критерии успеха:** ARR >$1M к концу 2024 года
```

### 4. How-To Guide (Практический гайд)

**Purpose:** Teach specific skill/process

**Structure:**
1. **Для кого:** Target audience
2. **Что получите:** Clear outcome
3. **Что понадобится:** Prerequisites/tools
4. **Шаги:** Step-by-step process
5. **Результат:** What success looks like

**Length:** 1,500-3,000 words

**Example opening:**

```markdown
# Как запустить email-onboarding, который увеличит retention на 40%

**TL;DR:** Email onboarding — один из самых недооцененных инструментов. Мы внедрили его за 2 недели и подняли retention с 45% до 63%. В статье — пошаговый план, готовые шаблоны и метрики.

---

## Для кого этот гайд

✅ Подходит если у вас:
- B2B или B2C SaaS
- База пользователей 100+
- Email marketing платформа (Mailchimp, SendPulse, etc.)
- 2-4 часа на настройку

**Что получите:**
- Готовую email-последовательность (7 писем)
- Шаблоны с высокой конверсией
- Метрики для отслеживания
- Прогноз: +20-40% retention
```

### 5. Opinion/Commentary (Мнение)

**Purpose:** Share perspective on industry trend/issue

**Structure:**
1. **Тезис:** Your main argument
2. **Контекст:** Why this matters now
3. **Аргументы:** Supporting points with data
4. **Контр-аргументы:** Address opposing views
5. **Вывод:** Implications and predictions

**Length:** 1,000-2,000 words

**Example opening:**

```markdown
# Почему freemium модель убивает большинство SaaS-стартапов

**TL;DR:** 78% ранних стартапов выбирают freemium, но только 3% из них достигают $1M ARR. Free trial на 14-30 дней работает в 5 раз лучше. Делюсь данными и объясняю почему.

---

## Тезис

Freemium кажется очевидным выбором: дать продукт бесплатно, пусть пользователи пробуют и платят за premium. Но **для раннего стартапа это почти всегда ошибка**.

Вот почему:

**1. Вы привлекаете не тех пользователей**

Freemium привлекает массу пользователей, которые никогда не заплатят...
```

---

## Writing Style

### Business-Focused Language

Use business terminology your audience knows:

✅ **Good:**
- Unit-экономика
- CAC, LTV, MRR, ARR, churn
- Product-market fit
- Growth hacking
- Customer success
- North Star Metric

❌ **Too technical:**
- REST API endpoints
- Асимптотическая сложность
- Docker контейнеры
- Kubernetes pods

### Numbers Tell Stories

Lead with data:

✅ **Good:**
> Мы выросли с 50 до 500 клиентов за квартал. MRR увеличился с $12k до $87k (+625%). CAC снизился с $180 до $65 благодаря органическому трафику. LTV/CAC вырос с 1.5 до 4.2.

❌ **Vague:**
> Мы активно растем. Количество клиентов значительно увеличилось. Стоимость привлечения стала ниже, а экономика улучшилась.

### Honest and Transparent

Share failures and learnings:

✅ **Good:**
> **Что не сработало:**
> - Facebook ads: потратили $15k, CAC $280 при LTV $150. Убыток $8k.
> - Influencer marketing: 3 кампании, 0 конверсий в платящих клиентов
> - Affiliate program: паузим, ROI отрицательный
>
> **Вывод:** для B2B SaaS перфоманс-маркетинг редко работает. Лучше content + outreach.

❌ **Only success:**
> Мы попробовали разные каналы и нашли оптимальный. Все идет отлично.

### Actionable Advice

Always end with clear next steps:

✅ **Good:**
```markdown
## Что делать прямо сейчас

**Если у вас <100 клиентов:**
1. Позвоните каждому клиенту на этой неделе
2. Спросите: что заставило их выбрать вас?
3. Найдите паттерны в ответах — это ваша UVP

**Если у вас 100-1000 клиентов:**
1. Сегментируйте по поведению (активные/неактивные)
2. NPS опрос для выявления promoters и detractors
3. Customer success звонки для топ-20% по revenue

**Если у вас 1000+ клиентов:**
1. Cohort analysis для определения retention patterns
2. Automated email campaigns для re-engagement
3. Customer success только для enterprise (>$1k/месяц)
```

❌ **Vague:**
> Рекомендую работать с клиентами и улучшать продукт. Это важно для роста.

---

## SEO and Discoverability

### Keywords

Include relevant keywords naturally:

**Primary keywords:**
- SaaS, стартап, маркетинг, рост, метрики
- Конкретные термины: CAC, LTV, churn, MRR, ARR
- Ниши: B2B SaaS, EdTech, FinTech, MarTech

**Use in:**
- Title (primary keyword)
- First paragraph
- Headings (H2, H3)
- Throughout body naturally

### Internal Links

Link to related content:

```markdown
Читайте также:
- [Как считать unit-экономику SaaS](./unit-economics)
- [Product-market fit: как понять что нашли](./pmf-guide)
- [CAC Payback Period и его влияние на рост](./cac-payback)
```

### Meta Description

Craft compelling meta descriptions (150-160 chars):

✅ **Good:**
> Как мы вырастили MRR с $12k до $87k за 9 месяцев. Стратегия, каналы, метрики. Обошлись без инвестиций. Делимся опытом и цифрами.

❌ **Generic:**
> Статья о росте стартапа. Полезные советы для предпринимателей.

---

## Publishing Checklist

### Before Publishing

**Content:**
- [ ] TL;DR at the top with key metrics
- [ ] Concrete numbers throughout
- [ ] Before/after comparison
- [ ] Visual elements (charts, screenshots)
- [ ] Actionable takeaways
- [ ] Links to related content

**Style:**
- [ ] Business-focused (not too technical)
- [ ] Key points in **bold**
- [ ] Bullet points for scannability
- [ ] Tables for comparisons
- [ ] Short paragraphs (3-4 sentences)

**Formatting:**
- [ ] Compelling title with numbers
- [ ] Proper headers hierarchy
- [ ] Russian quotation marks « »
- [ ] Em dashes — with spaces
- [ ] Images optimized and captioned

**Metadata:**
- [ ] Relevant category selected
- [ ] 3-5 tags added
- [ ] Meta description written
- [ ] Cover image added

**Quality:**
- [ ] All metrics verified
- [ ] No typos or grammar errors
- [ ] Links working
- [ ] Mobile-friendly

### After Publishing

- [ ] Share on social media (Telegram, Twitter)
- [ ] Notify relevant communities
- [ ] Monitor and respond to comments
- [ ] Track metrics (views, engagement, referrals)
- [ ] Consider cross-posting to Medium, Habr

---

## Example Complete Article

```markdown
# Как мы выросли с $0 до $100k MRR за 9 месяцев без инвестиций

**TL;DR:** Запустили B2B SaaS для команд маркетинга в марте 2024 с нулевым бюджетом. К декабрю достигли $100k MRR, 850 платящих клиентов, CAC $42, churn 3.5%. Основные драйверы: content marketing (60% лидов), product-led growth и customer success с первого дня. Делимся всеми цифрами и стратегией.

---

## Контекст: с чего начинали

**Март 2024:**
- Команда: 2 фаундера
- Бюджет: $0
- Продукт: MVP после 3 месяцев разработки
- Клиентов: 0

**Наш SaaS:** Инструмент для автоматизации email и социальных сетей. Целевая аудитория — маркетинговые команды в B2B компаниях 10-50 человек.

## Проблема: как расти без бюджета на маркетинг

Мы потратили последние деньги на разработку MVP. **Бюджет на маркетинг: $0.**

Классические каналы требуют денег:
- Google Ads: минимум $3-5k/месяц
- Facebook Ads: от $2k/месяц
- Конференции: $5-10k за участие
- PR-агентство: от $3k/месяц

**Вопрос:** Как привлекать клиентов бесплатно?

## Решение: Content + Product-Led Growth

### Month 1-2: Поиск каналов (март-апрель)

Протестировали 8 бесплатных каналов:

| Канал | Лиды | Конверсия | CAC |
|-------|------|-----------|-----|
| Content marketing | 23 | 17% | $0 |
| Cold email | 45 | 4% | $0 |
| Product Hunt | 120 | 2% | $0 |
| Reddit | 8 | 12% | $0 |
| LinkedIn organic | 15 | 13% | $0 |
| Hacker News | 3 | 33% | $0 |
| Twitter | 12 | 8% | $0 |
| Referrals | 0 | 0% | $0 |

**Вывод:** Фокусируемся на content marketing + cold email + Product Hunt.

### Month 3-5: Content Machine (май-июль)

**Стратегия:**
1. Публиковать 3-4 статьи в неделю
2. Фокус на SEO + распространение в комьюнити
3. Каждая статья = lead magnet

**Результаты за 3 месяца:**

- 52 статьи опубликовано
- 45,000 уникальных посетителей
- 1,200 email подписчиков
- 180 trial регистраций
- 24 платящих клиента

**Ключевые статьи (топ-3 по трафику):**

1. «15 инструментов email-маркетинга: сравнение» — 8,500 визитов
2. «Как автоматизировать LinkedIn posting: гайд» — 6,200 визитов
3. «Email sequences для SaaS: 7 шаблонов» — 5,800 визитов

**CAC через контент:** $0 на трафик + ~20 часов в неделю

### Month 6-9: Масштабирование (август-декабрь)

**Что добавили:**

1. **Customer Success с первого дня**
   - Onboarding call для каждого trial
   - Weekly check-ins первый месяц
   - Результат: trial→paid конверсия выросла с 8% до 23%

2. **Реферальная программа**
   - 20% discount на 3 месяца за каждого приведенного клиента
   - Результат: 15% новых клиентов из referrals

3. **PLG механика**
   - Free plan с лимитом (vs free trial)
   - Viral loops (invite team members)
   - Результат: +40% signups, +60% team accounts

## Результаты: декабрь 2024

**Основные метрики:**

| Метрика | Значение |
|---------|----------|
| MRR | $100,400 |
| ARR | ~$1.2M |
| Клиентов (платящих) | 852 |
| Trial users | 1,240 |
| Trial→Paid | 23% |
| Средний чек | $118/месяц |
| CAC | $42 |
| LTV | $1,512 |
| LTV/CAC | 36 |
| Churn | 3.5%/месяц |
| NPS | 58 |

**Распределение клиентов по тарифам:**

- Starter ($49/мес): 540 клиентов (63%)
- Professional ($149/мес): 280 клиентов (33%)
- Enterprise ($399/мес): 32 клиента (4%)

**Каналы привлечения:**

- Content marketing: 60% лидов
- Referrals: 15%
- Product Hunt/органика: 12%
- Cold outreach: 8%
- Другое: 5%

## Что сработало

### 1. Content-First подход

**Вложили:** 15-20 часов в неделю
**Получили:** 60% всех лидов бесплатно

**Ключ к успеху:**
- SEO-оптимизация под коммерческие запросы
- Практический контент (гайды, templates, checklists)
- Распространение в релевантных комьюнити

### 2. Customer Success как конкурентное преимущество

Trial→Paid конверсия: 8% → 23% (+188%)

**Что делали:**
- Personal onboarding call (30 мин)
- Помощь с настройкой
- Weekly check-ins первый месяц
- Быстрая поддержка (ответ <2 часов)

**ROI:** Customer success обходится в ~$15/клиент, но повышает LTV на $400.

### 3. Product-Led Growth механики

Free plan + viral loops дали 40% прирост signups.

**Что внедрили:**
- Free tier с лимитами
- Easy upgrade path
- Invite team members → больше активации
- In-app prompts для upgrade

## Что не сработало

**1. Twitter organic**
- Вложили: 50+ часов
- Получили: 12 лидов, 1 клиент
- Вывод: ROI слишком низкий для раннего стартапа

**2. Reddit marketing**
- Попытки: 15+ постов
- Результат: в основном минусы, мало лидов
- Вывод: сложно для B2B продуктов

**3. Партнерская программа (первая попытка)**
- Запустили в мае
- За 2 месяца: 0 партнеров
- Причина: слишком рано, недостаточно credibility

## Инсайты и обучения

### 1. Content работает, но нужно терпение

Первые 3 месяца: почти нет трафика.
Месяцы 4-6: начался рост.
Месяцы 7-9: exponential growth.

**Вывод:** контент — это long game. Нужно минимум 50-100 статей для critical mass.

### 2. Не все метрики важны на старте

Мы тратили время на:
- Оптимизацию churn (когда было 10 клиентов)
- A/B тесты UI (на 50 юзерах — статистически незначимо)
- Детальную аналитику продукта

**Вывод:** до 100 клиентов важно только одно — привлечение и базовый product-market fit.

### 3. Цена влияет на качество клиентов

Первый pricing: $19/месяц.
Клиенты: много, но high churn (12%), низкий engagement.

Подняли до $49/месяц.
Клиенты: меньше, но churn 4%, high engagement.

**Вывод:** не бойтесь поднимать цены. Платящие больше клиенты — более committed.

## Рекомендации: что делать

### Если вы на старте ($0-10k MRR):

1. **Выберите 1-2 канала и удвойте усилия**
   - Не распыляйтесь на 10 каналов
   - Content или cold outreach — выберите что ближе

2. **Говорите с каждым клиентом**
   - Call или встреча с каждым
   - Спрашивайте: почему выбрали вас?
   - Ищите паттерны

3. **Не тратьте на платный маркетинг**
   - CAC будет огромный без product-market fit
   - Лучше вложить в продукт или контент

### Если вы в фазе роста ($10k-100k MRR):

1. **Внедрите Customer Success ASAP**
   - ROI будет 5-10x в виде retention
   - Начните с топ-20% клиентов

2. **Автоматизируйте то, что работает**
   - Email sequences
   - Onboarding flows
   - Analytics и reporting

3. **Начинайте думать о брендинге**
   - До этого момента — только performance
   - Теперь можно вкладывать в awareness

## Что дальше

**Цели на 2025:**

- $500k MRR к концу года
- Нанять команду (customer success, sales, marketing)
- Запустить enterprise-тариф
- Открыть европейский рынок

**Ключевой фокус:** удержание на уровне продукта + масштабирование того, что работает.

---

## Полезные ресурсы

- [Notion doc со всеми метриками](https://notion.so/metrics)
- [Шаблоны email sequences](https://templates.example.com)
- [Content calendar](https://airtable.com/content)

**Вопросы?** Пишите в комментариях, с удовольствием отвечу!

---

**О проекте:** [Название] — инструмент для автоматизации маркетинга. [Website]

**Об авторе:** Иван Петров, co-founder & CEO. [Twitter] | [LinkedIn]
```

---

## Final Tips

1. **Lead with numbers** — readers come for data
2. **Be honest** — share failures, not just success
3. **Make it scannable** — bold, bullets, tables
4. **End with action** — clear next steps
5. **Engage in comments** — build community
6. **Cross-promote** — link to your best content
7. **Track metrics** — see what resonates

---

**Last updated:** 2025-11-20
