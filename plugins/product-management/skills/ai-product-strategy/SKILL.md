---
name: ai-product-strategy
description: World-class AI PM skill covering LLM product strategy, responsible AI, model evaluation, and top product frameworks (PRFAQ, RICE, WSJF, JTBD, Kano, HEART, AARRR). Always saves Russian markdown artifacts for every iteration of the work.
---

# AI Product Strategy

Мирового уровня подход к созданию и развитию AI/LLM продуктов: стратегия, безопасность, метрики, опыт пользователей и скорость экспериментов.

## Обязательные правила вывода
- Всегда отвечай **на русском** независимо от языка запроса.
- Сохраняй каждый артефакт через Write tool в `outputs/product-management/skills/ai-product-strategy/{timestamp}_{кратко_о_задаче}.md`.
- В файл включай: контекст, гипотезы, метрики (модельные + продуктовые), риски/гарнды, решения, следующие шаги. Обновляй тот же файл по мере итераций.

## Когда применять
- Планирование и запуск AI/LLM функций и продуктов
- Проработка ответственности и безопасного масштабирования
- Выбор и оценка моделей (latency/quality/cost)
- Проектирование промтов, RAG, fine-tuning, multi-agent
- Построение AI-метрик и экспериментов (offline/online)

## 3-итерационный цикл (глубокая проработка)
1) **Диагностика** — сформулируй задачу, целевые метрики (North Star + HEART), ограничения, RICE/WSJF приоритет, риски и допущения. Зафиксируй черновой бриф в markdown.
2) **Дизайн & эксперименты** — 2–3 варианта решения (baseline vs улучшенный), план оффлайн eval (accuracy/hallucination/toxicity/latency/cost) и онлайн экспериментов, схема guardrails (модерация, safety filters, red teaming), чек-лист приватности/ответственности. Обнови markdown таблицами вариантов.
3) **Верификация & rollout** — выбери вариант, пропиши staged rollout (canary → % трафика), мониторинг и алерты, действия при деградации, план улучшений. Зафиксируй финальный план и TODO.

## Когда применять
- Стратегия/дизайн AI/LLM фич, выбор модели/инфраструктуры.
- Настройка guardrails/ответственного AI, оценка стоимости/latency/качества.
- Планирование экспериментов (offline/online), запуск RAG/agent/copilot.
- Подготовка к Board/ExCo/команде по AI инициативе.

## Ключевые фреймворки (поддерживать явным образом)
- **PRFAQ (Working Backwards)** для визии и PRD, **JTBD + Kano + HEART** для UX-качества, **AARRR/North Star** для продуктовых метрик.
- **RICE/ICE/WSJF** для приоритизации AI инициатив с учётом стоимости инференса.
- **Constitutional AI, RLHF, Model Cards, Safety Checklists** для ответственности и прозрачности.
- **Offline/Online Eval Stack**: golden datasets, автотесты, LLM-as-judge, regression suite.
- **Responsible AI Ops**: аттестация данных, PII-контроль, bias/fairness проверки, долговременный мониторинг.

## Подробные плейбуки (3 итерации)
### Итерация 1 — Диагностика (1–2 часа)
- Цель/NSM + модельные метрики (точность/latency/cost/safety), ограничения/данные.
- Риск-карта (safety/bias/PII/регуляторика), требования к guardrails.
- Артефакт: черновой бриф + risk/decision log.
### Итерация 2 — Дизайн (2–4 часа)
- Варианты: baseline/upgrade (модель/контекст/RAG/fine-tune/агентность).
- Eval: offline (datasets, LLM-judge), online план (A/B/canary), пороги и guardrails.
- Стоимость/latency/качество: таблицы trade-offs, RICE/WSJF приоритет.
- Артефакт: таблица вариантов, план экспериментов, safety/PII чек-лист.
### Итерация 3 — Верификация/rollout (1–2 часа)
- Решение, staged rollout, алерты/стоп-пороги, rollback/fallback.
- Мониторинг: метрики + guardrails, частота обзоров.
- Обнови decision/risk logs, TODO с владельцами и датами.

## Метрики и алерты
- **Продуктовые:** NSM, AARRR, adoption, retention, satisfaction (NPS/CSAT).
- **Модельные:** точность, hallucination, toxicity/violations, latency p50/p95/p99, $/req.
- **Бизнес:** LTV/CAC, payback, маржа/COGS инференса.
- **Риск:** rate policy violations, PII leakage, drift, complaints; алерты на деградацию качества/latency/стоимости.

## Входы (собери до старта)
- Цель/NSM и бизнес-контекст, доступные данные/источники, ограничения (PII/регуляторика/инфра/бюджет).
- Базовая метрика качества/latency/стоимости, текущие guardrails/политики, риски и зависимости.

## Выходы (обязательно зафиксировать)
- Стратегический бриф + выбранный вариант с trade-offs.
- Eval/эксперимент-план с порогами go/stop, guardrails, мониторинг.
- Планы rollout/rollback, алерты, TODO с владельцами и датами.
- Decision/Risk logs, изменения vs прошлой версии.

## Источники и инструменты
- WebSearch/WebFetch (исследование рынка/практик), внутренние данные/логи, eval датасеты.
- Claude Agent SDK: Task (делегировать анализ/оценку), Write (сохранение артефактов), Bash (скрипты eval/calc).
- Шаблоны из assets: PRFAQ, Responsible AI чек-лист, план экспериментов.

## Качество ответа (checklist)
- Есть ≥2 варианта с метриками качества/стоимости/latency/safety и RICE/WSJF.
- Eval и guardrails прописаны с порогами; есть алерты/rollback.
- Учтены PII/регуляторика, bias/safety; decision/risk logs обновлены.
- TODO с владельцами/датами; изменения vs прошлой версии зафиксированы.

## Red Flags (осторожно)
- Нет оффлайн eval или порогов, нет guardrails/PII контроля.
- Выбор модели без учёта стоимости/latency или бюджета.
- Единственный сценарий без альтернатив и критериев go/stop.
- Мониторинг/алерты не определены; нет владельцев и rollback.

## Паттерны использования
- **Copilot/Agent**: контекст (RAG), инструменты, memory, ограничения; измеряй success rate, latency, $/вызов.
- **Content & Moderation**: модерация до/после генерации, self-critique по конституции, explainability блок.
- **Decision Support**: прозрачные цепочки рассуждений, уровни уверенности, fallback к правилам.
- **Experiment Factory**: быстрые AB/nudges, feature flags, обратимые изменения, автоматический отчёт.

## Шаблон сохранения артефакта
```markdown
# {Название задачи}
**Дата:** {timestamp} | **Этап:** Диагностика/Дизайн/Верификация | **Ответственный:** AI PM

## Контекст и цель
- Продукт/персона/рынок
- Целевые метрики: NSM + HEART + модельные (точность, токсичность, latency, стоимость)
- Ограничения/риски: безопасность, данные, регуляторика, технические лимиты

## Варианты решений (RICE/WSJF)
| Вариант | Описание | RICE/WSJF | Ключевые риски | Меры защиты |

## Эксперименты и оценки
- Offline eval: датасет, метрики, пороги, автоматизация
- Online: дизайн теста, длительность, критерии ship/kill, guardrails

## Решение и rollout
- Выбранный вариант и обоснование
- План релиза: этапы, %, условия стопа
- Мониторинг: метрики, алерты, каналы

## Следующие шаги
- {3–5 действий с владельцами и сроками}
```

## Assets и References
- `/assets/` — шаблоны PRFAQ, чек-лист Responsible AI, план эксперимента и шаблон отчёта.
- `/references/` — сводка фреймворков (PRFAQ, JTBD, Kano, HEART, RICE, WSJF), карта рисков и метрик для AI продуктов, примеры eval стеков.
