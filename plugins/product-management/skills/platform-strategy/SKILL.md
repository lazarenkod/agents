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

## Подробные плейбуки (3 итерации)
### Итерация 1 — Диагностика (1–2 часа)
- Акторы (producers/consumers/partners), ценность, текущее состояние flywheel и узкие места.
- API/SDK scorecard: time-to-first-call, стабильность, доки, версии, ошибки, DX/NPS.
- Экономика: GMV/TPV, attach/take rate, partner margin, churn, cost-to-serve; риски/PII/регуляторика.
- Артефакт: черновой platform brief + risk/decision log.
### Итерация 2 — Дизайн (2–4 часа)
- Модель: marketplace vs usage API vs extensibility; стимулы/субсидии, pricing/packaging, рев-шеры.
- Flywheel план: предложение → разработчики → приложения → ценность → спрос; тормоза и гарнды.
- Governance: версионирование/депрекейшн, лимиты, безопасность/PII, партнёрский онбординг/ревью.
- DX: TTF call <5 мин, SDK/CLI, примеры, sandbox, changelog; observability/алерты.
- Артефакт: platform brief, scorecard, DX checklist, план рев-шеров и governance.
### Итерация 3 — Верификация/rollout (1–2 часа)
- Пилоты/партнёры/маркетплейс лоты: KPI/пороги, алерты/стоп-условия, миграции/версии.
- Ритм: WBR/MBR/QBR, обзор метрик/инцидентов, эскалации, roadmap изменений.
- Обнови decision/risk logs, TODO с владельцами/датами, изменения vs прошлой версии.

## Метрики и алерты
- **Экосистема:** активные девы/приложения/интеграции, GMV/TPV, attach/take rate, churn партнёров.
- **DX:** time-to-first-call, success rate интеграций, dev NPS/CSAT, тикеты/SLA.
- **Надёжность/безопасность:** 4xx/5xx, latency p50/p95/p99, версии/миграции, инциденты/PII.
- **Экономика:** partner margin, payback партнёров, рев-шеры/субсидии, cost-to-serve.
- Алерты: деградация DX/ошибок/latency, срыв миграций, рост инцидентов/PII, падение attach/take rate.

## Входы (собери до старта)
- Текущее состояние API/SDK, метрики DX/ошибок, партнёрский портфель/маркетплейс, экономические показатели.
- Ограничения: безопасность/PII, комплаенс/регуляторика, ресурсы, зависимость от версий/инфры.
- Источники: dev опросы/NPS, логи ошибок, marketplace данные, конкурентные платформы.

## Выходы (обязательно зафиксировать)
- Platform brief с моделью/ценностью/акторами; scorecard и flywheel план.
- Pricing/packaging/rev-share, governance/версии/лимиты, DX checklist.
- План пилотов/партнёров/маркетплейса, KPI/алерты/ритм, TODO с владельцами/датами, обновлённые логи.

## Источники данных и инструменты
- Логи API/SDK, observability, dev NPS/support, marketplace аналитика, WebSearch/WebFetch (конкуренты/прайсинг).
- Фреймворки: Flywheel, Two-sided networks, API lifecycle, DX scorecard, governance & safety.
- Claude Agent SDK: Task (параллельный анализ), Write (артефакты), Bash (подсчёт метрик/ошибок).

## Качество ответа (checklist)
- Описаны акторы/ценность/модель, scorecard и flywheel с тормозами/гарндами.
- DX/версии/безопасность/PII/лимиты учтены; pricing/рев-шеры/стимулы прописаны.
- KPI/алерты/ритм и владельцы заданы; план пилотов/миграций есть.
- Decision/risk logs обновлены; TODO и изменения зафиксированы.

## Red Flags (осторожно)
- Нет DX/scorecard или не измеряется time-to-first-call/ошибки.
- Governance/версии/безопасность не определены; нет лимитов/эскалаций.
- Модель/рев-шеры/стимулы не просчитаны; нет flywheel тормозов/гарнды.
- Нет KPI/алертов/ритма; нет владельцев и плана пилотов/миграций.
