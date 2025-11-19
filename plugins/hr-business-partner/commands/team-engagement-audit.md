---
name: team-engagement-audit
description: Audit team engagement and motivation, identify issues, generate action plan. Creates comprehensive engagement analysis in Russian markdown with data-driven recommendations.
---

# Team Engagement Audit Command

Проведите комплексный audit engagement и мотивации команды с actionable recommendations.

## Использование

```
/team-engagement-audit [team-name]
```

## Что делает эта команда

1. **Анализирует engagement signals**: eNPS, attrition, survey data, 1-on-1 insights
2. **Диагностирует root causes**: Autonomy, mastery, purpose, recognition, workload
3. **Определяет risk factors**: Burnout, disengagement, flight risk employees
4. **Генерирует action plan**: Prioritized interventions с timeline
5. **Сохраняет результат**: Comprehensive audit report на русском

## Процесс

### Шаг 1: Сбор данных

Команда запросит:
- Название команды и размер
- eNPS score (если есть)
- Voluntary attrition rate
- Результаты engagement surveys
- Feedback из 1-on-1s и skip-levels
- Recent org changes (layoffs, reorgs, leadership changes)

### Шаг 2: Диагностика

Анализирует по 6 dimensions:
- **Autonomy**: Есть ли ownership и decision authority?
- **Mastery**: Есть ли рост и development opportunities?
- **Purpose**: Понимают ли impact своей работы?
- **Recognition**: Чувствуют ли себя ценными?
- **Workload**: Sustainable ли работа?
- **Psychological Safety**: Безопасно ли высказываться?

### Шаг 3: Risk Assessment

Определяет:
- **High Risk**: Top performers на грани ухода
- **Medium Risk**: Disengaged но удерживаемые
- **Low Risk**: Engaged и мотивированные

### Шаг 4: Action Plan

Генерирует prioritized recommendations:
- **Quick Wins** (0-30 days): Immediate impact
- **Medium-term** (1-3 months): Systemic improvements
- **Long-term** (3-6 months): Culture transformation

### Шаг 5: Документ

Создается audit report:
```markdown
# Team Engagement Audit: {Команда}
**Дата**: {Дата}
**Размер команды**: {N человек}
**Проведен**: hr-business-partner agent

## Executive Summary
{Краткое резюме: общий health score, top issues, critical actions}

## Engagement Metrics
{eNPS, attrition, survey scores, benchmarks}

## Diagnostic Analysis
### Autonomy: {Score}/5
{Оценка, evidence, issues}

### Mastery: {Score}/5
{Оценка, evidence, issues}

### Purpose: {Score}/5
{Оценка, evidence, issues}

### Recognition: {Score}/5
{Оценка, evidence, issues}

### Workload: {Score}/5
{Оценка, evidence, issues}

### Psychological Safety: {Score}/5
{Оценка, evidence, issues}

## Risk Assessment
{High/medium/low risk employees, specific concerns}

## Root Cause Analysis
{Top 3 systemic issues impacting engagement}

## Action Plan
### Quick Wins (0-30 days)
{Immediate actions}

### Medium-term (1-3 months)
{Systemic improvements}

### Long-term (3-6 months)
{Culture transformation}

## Success Metrics
{How we'll track improvement}

## Next Steps
{Timeline, owners, checkpoints}
```

## Примеры использования

**Пример 1: Low eNPS**
```
User: /team-engagement-audit Platform Engineering

Agent: Проведу engagement audit для Platform Engineering team.

Текущие данные:
- Размер команды: 15 engineers
- eNPS: 10 (low)
- Attrition: 20% (high)

Пожалуйста, поделитесь insights:
1. Что говорят в 1-on-1s? [...]
2. Были ли недавние changes? [...]

[Анализирует данные]

Agent: Диагностика выявила:
- **Workload** (2/5): Unsustainable, burnout risk
- **Recognition** (2/5): Invisible work, no appreciation
- **Purpose** (3/5): Unclear impact

Top 3 root causes:
1. On-call burden (24/7, no backup)
2. Lack of manager feedback and recognition
3. Disconnect from product outcomes

Action Plan generated...

Документ: outputs/hr-business-partner/2024-12-18_engagement-audit-platform-eng.md
```

**Пример 2: High Attrition**
```
User: /team-engagement-audit Sales-Ops

Agent: 3 resignations в последний месяц. Проведу urgent audit.

[Deep dive анализ]

Agent: Critical findings:
- **Compensation** (1/5): 30% below market (Confirmed via Pave data)
- **Leadership** (2/5): New manager, poor relationship
- **Career Growth** (2/5): No clear path

Immediate actions:
1. Compensation review для всей команды (urgent)
2. Skip-level meetings с оставшимися
3. Manager coaching on relationship building

Документ сохранен с URGENT priority...
```

## Лучшие практики

1. **Честность**: Поощряйте честную обратную связь (anonymity помогает)
2. **Data-driven**: Используйте metrics, не только anecdotes
3. **Timely**: Не ждите annual surveys - audit регулярно
4. **Action-oriented**: Audit без action plan бесполезен
5. **Follow-through**: Commit к action plan и отслеживайте

## Follow-up

После audit:
- Презентуйте findings leadership
- Коммуницируйте team (transparency)
- Execute action plan
- Re-audit через 3-6 months

## См. также

- `team-motivation-excellence` skill - deep dive на motivation theory
- `performance-review-mastery` skill - для individual performance issues
