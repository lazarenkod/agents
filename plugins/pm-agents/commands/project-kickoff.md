---
name: project-kickoff
description: Comprehensive project kickoff workflow that creates project charter, stakeholder map, risk register, and initial project plan in Russian (markdown format).
---

# Project Kickoff

Проведение инициации проекта с созданием всех необходимых артефактов для успешного старта.

## Что делает эта команда

Автоматизирует процесс инициации проекта, создавая:
1. **Project Charter** - устав проекта с целями, scope, stakeholders
2. **Stakeholder Map** - карта стейкхолдеров с power/interest analysis
3. **Risk Register** - начальный реестр рисков
4. **RACI Matrix** - распределение ответственности
5. **Initial Project Plan** - первичный план с milestones
6. **Communication Plan** - план коммуникаций

## Использование

```bash
# Интерактивный режим
Запустите команду и ответьте на вопросы

# Все документы сохраняются в:
projects/{project-name}/
  ├── project-charter.md
  ├── stakeholder-map.md
  ├── risk-register.md
  ├── raci-matrix.md
  ├── project-plan.md
  └── communication-plan.md
```

## Процесс

### Шаг 1: Сбор базовой информации

Я задам следующие вопросы:

1. **Название проекта**: Как называется проект?
2. **Executive Sponsor**: Кто executive sponsor?
3. **Project Manager**: Кто PM?
4. **Timeline**: Примерная длительность (в месяцах)?
5. **Budget Range**: Приблизительный бюджет?
6. **Business Objective**: Основная бизнес-цель проекта?
7. **Success Criteria**: Как измерить успех?

### Шаг 2: Определение Scope

1. **In Scope**: Что входит в проект?
2. **Out of Scope**: Что точно НЕ входит?
3. **Assumptions**: Ключевые предположения
4. **Constraints**: Технические/бизнес ограничения

### Шаг 3: Stakeholder Identification

Для каждого стейкхолдера соберу:
- Имя и роль
- Отношение к проекту (Sponsor/Decision Maker/Contributor/Informed)
- Уровень влияния (High/Medium/Low)
- Уровень интереса (High/Medium/Low)
- Коммуникационные предпочтения

### Шаг 4: Initial Risk Assessment

Идентифицирую начальные риски по категориям:
- **Technical**: Технологические риски
- **Resource**: Ресурсные риски
- **Schedule**: Риски по срокам
- **Organizational**: Организационные риски
- **External**: Внешние риски

Для каждого риска:
- Описание
- Impact (1-5)
- Probability (1-5)
- Initial mitigation ideas

### Шаг 5: Team & Responsibilities

Определю:
- Core team members
- Extended team
- Key roles (RACI)
- Decision-making authority

### Шаг 6: High-Level Plan

Создам:
- Major milestones (3-5)
- Phase breakdown
- Key deliverables
- Dependencies (если известны)

## Созданные документы

### 1. Project Charter (`project-charter.md`)

```markdown
# Project Charter: [Название]

## Executive Summary
- **Project Name**: [Name]
- **Sponsor**: [Name]
- **PM**: [Name]
- **Start Date**: [Date]
- **Target Completion**: [Date]
- **Budget**: $[Amount]

## Business Case
[Почему проект важен, какую проблему решает]

## Objectives
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

## Success Criteria
- [Criterion 1]: [Metric]
- [Criterion 2]: [Metric]

## Scope
**In Scope**:
- [Item 1]
- [Item 2]

**Out of Scope**:
- [Item 1]
- [Item 2]

## Assumptions & Constraints
**Assumptions**:
- [Assumption 1]

**Constraints**:
- [Constraint 1]

## High-Level Timeline
[Timeline overview]

## Budget Overview
[Budget breakdown]

## Stakeholders
[Key stakeholders list]

## Risks
[Top 5 risks]

## Approval
- [ ] Sponsor Approval: _____________ Date: _______
- [ ] PM Acceptance: _____________ Date: _______
```

### 2. Stakeholder Map (`stakeholder-map.md`)

Power/Interest grid с детальной информацией по каждому стейкхолдеру.

### 3. Risk Register (`risk-register.md`)

Начальный список рисков с impact/probability assessment.

### 4. RACI Matrix (`raci-matrix.md`)

Матрица ответственности для ключевых deliverables и decisions.

### 5. Project Plan (`project-plan.md`)

High-level plan с phases, milestones, и deliverables.

### 6. Communication Plan (`communication-plan.md`)

План коммуникаций с stakeholders (frequency, format, audience).

## Best Practices

При использовании этой команды:

✅ **Вовлекайте Sponsor**: Проводите kickoff с executive sponsor
✅ **Будьте реалистичны**: Scope и timeline должны быть achievable
✅ **Идентифицируйте риски рано**: Лучше знать о проблемах заранее
✅ **Clear Success Criteria**: Измеримые критерии успеха
✅ **Stakeholder Buy-in**: Убедитесь в alignment ключевых stakeholders

## После Kickoff

Следующие шаги:
1. Проведите kickoff meeting с core team
2. Schedule регулярные check-ins с stakeholders
3. Начните детальное планирование первой фазы
4. Setup project tracking (Jira, Asana, etc.)
5. Initialize risk monitoring process

## Команды для следующих шагов

- `/quarterly-planning` - Детальное квартальное планирование
- `/risk-review` - Regular risk reviews
- `/status-report` - Weekly/monthly status reporting

---

**Готовы начать? Ответьте на вопросы выше, и я создам все артефакты проекта.**
