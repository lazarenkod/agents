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

## Ключевые фреймворки (поддерживать явным образом)
- **PRFAQ (Working Backwards)** для визии и PRD, **JTBD + Kano + HEART** для UX-качества, **AARRR/North Star** для продуктовых метрик.
- **RICE/ICE/WSJF** для приоритизации AI инициатив с учётом стоимости инференса.
- **Constitutional AI, RLHF, Model Cards, Safety Checklists** для ответственности и прозрачности.
- **Offline/Online Eval Stack**: golden datasets, автотесты, LLM-as-judge, regression suite.
- **Responsible AI Ops**: аттестация данных, PII-контроль, bias/fairness проверки, долговременный мониторинг.

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
