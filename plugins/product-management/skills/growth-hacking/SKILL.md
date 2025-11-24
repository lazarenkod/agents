---
name: growth-hacking
description: World-class growth skill covering AARRR, North Star, RICE/ICE/WSJF, RARRA, growth accounting, PLG/viral loops. Always produces Russian markdown artifacts for each iteration of experiments.
---

# Growth Hacking

Мирового уровня ростовая практика с упором на циклы экспериментов, метрики, виральность и устойчивую экономику.

## Обязательные правила вывода
- Всегда отвечай **на русском**.
- Каждый результат сохраняй в `outputs/product-management/skills/growth-hacking/{timestamp}_{кратко_о_задаче}.md` через Write tool (обновляй файл по итерациям).
- Структура: цель → гипотезы → метрики → дизайн эксперимента → вывод → следующие шаги.

## Когда использовать
- Рост DAU/WAU/MAU, конверсии AARRR/RARRA
- Проектирование вирусных/реферальных механик и PLG
- Оптимизация активации/онбординга и payback
- Экспериментальные программы (A/B/n, holdout)
- Модели монетизации и ценообразования

## 3-итерационный цикл роста
1) **Диагностика:** карта воронки AARRR/RARRA, NSM + инпут-метрики, ростовой P&L (LTV/CAC/payback), сегментация. Фиксируй проблемы и приоритет (RICE/WSJF).
2) **Дизайн экспериментов:** 3–5 гипотез, план A/B с критерием успеха, power analysis, контрольные метрики/guardrails (churn, качество трафика), каналы и сообщения. Сохраняй таблицу гипотез.
3) **Верификация:** анализ результатов, статистическая значимость, перенос в прод (ship/iterate/kill), влияние на NSM/LTV/CAC. Обнови roadmap и backlog экспериментов.

## Ключевые фреймворки
- **AARRR/RARRA + North Star:** связывает воронку и основную метрику ценности.
- **Growth Accounting (Facebook):** New + Resurrected – Churn; Quick Ratio.
- **RICE/ICE/WSJF:** приоритизация гипотез и каналов.
- **Hooked/Habit Loop, Viral Loops (K-factor), PLG motions:** self-serve, приглашения, коллаборация.
- **Unit Economics:** LTV/CAC, payback, маржинальность по каналам.
- **HEART/Activation Benchmarks:** измерение UX и прогрессии в онбординге.

## Шаблон сохранения артефакта
```markdown
# {Эксперимент/инициатива}
**Дата:** {timestamp} | **Этап:** Диагностика/Дизайн/Верификация
**NSM:** {north_star} | **Цель:** {что улучшаем}

## Текущая воронка (AARRR/RARRA)
- Acquisition: {метрики, источники}
- Activation: {магическое число, шаги онбординга}
- Retention: {D1/D7/D30, churn}
- Revenue: {ARPU, LTV, payback}
- Revenue: {ARPU, LTV, payback}
- Referral: {k-factor, приглашения}

## Гипотезы (RICE/WSJF)
| # | Идея | Целевой шаг | RICE/WSJF | Риск/гарнды |

## Дизайн эксперимента
- Тип теста, длительность, размер выборки, сегменты
- Основные метрики и guardrails
- Сообщения/креативы/каналы

## Результаты и решение
- Итоговые метрики, значимость, эффект на NSM
- Ship / Iterate / Kill + причины

## Следующие шаги
- {3–5 действий с владельцами и сроками}
```

## Assets и References
- `/assets/` — шаблоны цикла экспериментов, карты воронки, калькулятор RICE/WSJF, дизайн реферальных/PLG механик.
- `/references/` — конспекты AARRR/RARRA, growth accounting, viral/freemium/monetization playbooks, метрики активации и payback.
