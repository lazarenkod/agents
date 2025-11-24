---
name: platform-strategy
description: World-class platform product strategy covering ecosystem design, API/SDK quality, marketplace flywheels, pricing/packaging, and developer experience. Produces Russian markdown artifacts for every iteration.
---

# Platform Strategy

Мирового уровня платформа-стратегия: flywheels, API/SDK качество, экосистема, маркетплейсы, монетизация.

## Обязательные правила вывода
- Всегда отвечай **на русском**.
- Сохраняй каждый шаг работы в `outputs/product-management/skills/platform-strategy/{timestamp}_{кратко_о_задаче}.md`.
- Структура: цель → контекст/акторы → фреймворки/анализ → решения → метрики → следующие шаги. Обновляй файл по мере итераций.

## Когда использовать
- Проектирование платформы, API/SDK, маркетплейса или двухсторонней сети
- Планирование flywheel и стратегии экосистемы/партнёров
- Улучшение Developer Experience и качества API
- Ценообразование и упаковка (tiers, usage-based, rev-share)
- Масштабирование governance и безопасности платформы

## 3-итерационный цикл
1) **Диагностика:** карта стейкхолдеров (продюсеры/консьюмеры/партнёры), текущее состояние flywheel, API scorecard, метрики (NSM, DX, GMV/Take Rate). Выяви бутылочные горлышки.
2) **Дизайн:** варианты платформенной модели (marketplace, usage API, extensibility), стратегии ревеню/рев-шера, DX улучшения (time-to-first-call <5 мин), governance (версионирование, лимиты, безопасность). Применяй RICE/WSJF для приоритета.
3) **Верификация:** пилоты с партнёрами, метрики DX (TTV, % успешных интеграций), рост экосистемы (# активных девов/приложений), финансовые метрики (take rate, attach, churn). Зафиксируй rollout и алерты.

## Ключевые фреймворки
- **Flywheel (AWS/Shopify):** предложение → разработчики → больше приложений/интеграций → ценность → спрос → предложение (цикл).
- **API/SDK Scorecard:** время до первого запроса, стабильность, документация, версионирование, ошибки, observability.
- **Platform Models:** marketplace (двусторонний), usage-based API, extensibility/плагины, data network effects.
- **Economics:** take rate, attach rate, contribution margin, рев-шеры, subsidies, incentivation.
- **Governance & Safety:** валидация приложений, безопасные скоупы, rate limits, политика данных/PII.
- **DX Framework:** onboarding <5 минут, примеры/SDK, sandbox, линтеры/CLI, changelog/депрекейшн политика.

## Шаблон сохранения артефакта
```markdown
# {Задача платформы}
**Дата:** {timestamp} | **Этап:** Диагностика/Дизайн/Верификация

## Контекст
- Акторы: {producers/consumers/partners}
- Ценности: {для каждой стороны}
- NSM и метрики: GMV/Take Rate/DX (TTV, success rate), безопасность

## Анализ
- Flywheel: текущее состояние, тормозящие звенья
- API scorecard: время до первого запроса, ошибки, версия, доки
- Экономика: pricing/packaging, рев-share, payback партнёров

## Варианты решения (RICE/WSJF)
| Вариант | Фокус | RICE/WSJF | Риски | Гарнды |

## План и rollout
- Пилоты/беты, партнёры, KPI
- Governance и безопасность (rate limits, scopes, ревью)
- Timeline и алерты

## Следующие шаги
- {3–5 действий с владельцами и сроками}
```

## Assets и References
- `/assets/` — API scorecard, platform brief, шаблон flywheel, дизайн рев-шера, DX checklist.
- `/references/` — платформенные фреймворки, метрики экосистемы, лучшие практики версионирования и безопасности.
