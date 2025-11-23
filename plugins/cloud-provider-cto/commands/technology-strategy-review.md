---
name: technology-strategy-review
description: Проведение комплексного анализа технологической стратегии облачной платформы с рекомендациями
---

# Technology Strategy Review

Проводит глубокий анализ текущей технологической стратегии облачного провайдера и формирует рекомендации по развитию.

## Что делает эта команда

1. Анализирует текущий портфель сервисов
2. Оценивает конкурентную позицию vs AWS/Azure/GCP/Oracle
3. Идентифицирует gaps и opportunities
4. Формирует technology roadmap
5. Рассчитывает required investments
6. Создает executive summary с рекомендациями

## Процесс выполнения

### Шаг 1: Сбор данных

```markdown
# Исходные данные

## Текущее состояние
- Список всех облачных сервисов
- Usage metrics по сервисам
- Revenue breakdown
- Customer feedback
- Technical debt inventory

## Рыночный контекст
- Competitor analysis (AWS, Azure, GCP, Oracle)
- Industry trends
- Customer requests
- Technology radar
```

### Шаг 2: Анализ портфеля

Анализирует каждый сервис по критериям:
- Strategic fit
- Market demand
- Revenue contribution
- Competitive position
- Technical health
- Innovation potential

### Шаг 3: Gap Analysis

Идентифицирует:
- Missing critical services
- Underperforming services
- Technology debt
- Capability gaps
- Market opportunities

### Шаг 4: Roadmap формирование

Создает 3-летний roadmap:
- Year 1: Quick wins и critical gaps
- Year 2: Strategic initiatives
- Year 3: Transformational bets

### Шаг 5: Investment planning

Рассчитывает:
- Required budget по initiative
- Expected ROI
- Resource requirements (headcount, infrastructure)
- Risk assessment

## Результат

Создает comprehensive strategy document в Markdown на русском языке:

```markdown
# Технологическая стратегия облачной платформы 2025-2027

## Executive Summary

[2-3 параграфа ключевых рекомендаций]

## Текущее состояние

### Портфель сервисов
[Оценка текущих сервисов]

### Конкурентная позиция
[Сравнение с AWS/Azure/GCP]

## Стратегические рекомендации

### Приоритет 1: Critical Gaps
- [Инициатива 1]
- [Инициатива 2]

### Приоритет 2: Strategic Growth
- [Инициатива 3]

### Приоритет 3: Innovation Bets
- [Инициатива 4]

## Technology Roadmap

### 2025 (Year 1)
Q1:
- [Milestone 1]
- [Milestone 2]

Q2-Q4:
- [...]

### 2026-2027
[High-level initiatives]

## Investment Requirements

Total: $XXM over 3 years

Breakdown:
- H1 (Core): $XXM (70%)
- H2 (Strategic): $XXM (20%)
- H3 (Innovation): $XXM (10%)

## Risks & Mitigations

[Key risks и mitigation plans]

## Success Metrics

[KPIs для tracking progress]
```

## Использование

```bash
# Запуск команды
/technology-strategy-review

# С параметрами
/technology-strategy-review --focus=ai-ml --timeframe=5-years
```

Команда запрашивает у пользователя необходимые данные и создает полный стратегический документ.
