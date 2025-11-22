---
name: strategic-planning
description: Senior-level strategic planning for technical projects including vision development, multi-year roadmaps, portfolio prioritization, and business case creation. Use when developing project strategy, quarterly/annual planning, or aligning technical initiatives with business objectives.
---

# Strategic Planning

Comprehensive strategic planning framework for senior project managers to transform business vision into executable technical roadmaps with measurable outcomes.

## When to Use This Skill

- Developing quarterly or annual project roadmaps
- Creating 6-18 month technical strategy
- Prioritizing portfolio of 5-20+ concurrent initiatives
- Aligning technical projects with business OKRs
- Building business cases for major investments
- Strategic planning sessions with executives

## Core Concepts

### 1. Vision to Strategy Framework

**От видения к стратегии:**

```
Видение (Vision)
  ↓
Стратегические цели (Strategic Goals)
  ↓
Ключевые результаты (Key Results)
  ↓
Инициативы (Initiatives)
  ↓
Дорожная карта (Roadmap)
  ↓
Спринты/Релизы (Sprints/Releases)
```

**Ключевые элементы:**
- **Видение**: Куда мы движемся (3-5 лет)
- **Миссия**: Почему это важно
- **Стратегические темы**: Фокусные области (4-6 тем)
- **Цели**: Измеримые результаты (квартал/год)
- **Инициативы**: Проекты для достижения целей

### 2. Стратегические темы для Tech компаний

**Cloud Infrastructure & Platform:**
- Миграция в облако (AWS/Azure/GCP)
- Модернизация платформы
- Масштабируемость и надежность
- Cost optimization

**AI/ML & Data:**
- Внедрение AI/ML capabilities
- Data platform modernization
- Real-time analytics
- Personalization & recommendations

**Developer Experience:**
- Internal tooling & platforms
- CI/CD optimization
- Developer productivity
- Technical debt reduction

**Product Innovation:**
- New product development
- Feature expansion
- User experience improvement
- Market differentiation

**Security & Compliance:**
- Zero-trust architecture
- Compliance certifications (SOC2, ISO)
- Data privacy & governance
- Security automation

**Operational Excellence:**
- SRE & observability
- Incident management
- Performance optimization
- Automation & efficiency

### 3. Модель приоритизации портфеля

**RICE Framework:**

```
Score = (Reach × Impact × Confidence) / Effort

Reach: Количество пользователей/команд (за период)
Impact: Масштаб влияния (3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal)
Confidence: Уверенность в оценках (100%=high, 80%=medium, 50%=low)
Effort: Человеко-месяцы команды
```

**Weighted Shortest Job First (WSJF):**

```
WSJF = Cost of Delay / Job Duration

Cost of Delay = User/Business Value + Time Criticality + Risk Reduction
Job Duration = Размер работы в story points
```

**Value vs. Effort Matrix:**

```
    Высокая ценность
    ┌─────────┬─────────┐
    │ Quick   │ Major   │
Low │ Wins    │ Projects│ High
    ├─────────┼─────────┤ Effort
    │ Fill-ins│ Money   │
    │         │ Pits    │
    └─────────┴─────────┘
    Низкая ценность
```

### 4. Структура стратегического плана

**Executive Summary (1 страница):**
- Ключевые цели на период
- Топ-5 инициатив
- Необходимые ресурсы
- Ожидаемые результаты
- Основные риски

**Strategic Context:**
- Бизнес-цели компании
- Рыночная ситуация
- Конкурентная позиция
- Технические ограничения
- Организационные факторы

**Goals & Key Results:**
- 3-5 стратегических целей
- 2-4 ключевых результата на цель
- Метрики и целевые значения
- Baseline (текущее состояние)

**Initiative Portfolio:**
- Список инициатив с приоритетами
- Alignment с целями
- Владельцы и команды
- Временные рамки
- Зависимости

**Resource Plan:**
- Headcount по командам
- Budget breakdown
- Infrastructure costs
- Third-party services
- Contingency reserves

**Risks & Assumptions:**
- Топ-10 рисков
- Mitigation strategies
- Ключевые assumptions
- Validation criteria

**Roadmap:**
- Quarterly milestones
- Release schedule
- Dependencies timeline
- Key decision points

### 5. Roadmap Development Process

**Фаза 1: Discovery (2-3 недели)**
- Сбор input от stakeholders
- Анализ данных и метрик
- Оценка текущего состояния
- Идентификация constraints

**Фаза 2: Prioritization (1-2 недели)**
- Scoring инициатив (RICE/WSJF)
- Capacity modeling
- Dependency analysis
- Trade-off discussions

**Фаза 3: Planning (2-3 недели)**
- Detailed planning топ инициатив
- Resource allocation
- Timeline development
- Risk assessment

**Фаза 4: Alignment (1-2 недели)**
- Stakeholder reviews
- Executive approval
- Team communication
- Commitment получение

**Фаза 5: Execution & Refinement (квартал)**
- Monthly check-ins
- Quarterly reviews
- Adaptive planning
- Learning capture

### 6. Roadmap Patterns

**Theme-based Roadmap:**
- Группировка по стратегическим темам
- Flexibility в выборе конкретных features
- Фокус на outcomes

**Feature-based Roadmap:**
- Конкретные features с датами
- Commitment на execution
- Waterfall-oriented

**Now-Next-Later:**
- Now: Текущий квартал (committed)
- Next: Следующий квартал (planned)
- Later: В разработке (exploratory)

**Outcome-driven Roadmap:**
- Цели вместо features
- OKR alignment
- Measurable impact

### 7. Stakeholder Alignment Techniques

**Stakeholder Mapping:**
```
    Высокая власть
    ┌─────────┬─────────┐
    │ Keep    │ Manage  │
    │Satisfied│ Closely │
Low ├─────────┼─────────┤ High
    │ Monitor │ Keep    │ Interest
    │         │Informed │
    └─────────┴─────────┘
    Низкая власть
```

**Communication Matrix:**
- Executive Sponsors: Monthly 1-pagers, quarterly reviews
- Product Leads: Weekly syncs, roadmap updates
- Engineering Leads: Bi-weekly technical reviews
- Cross-functional: Quarterly all-hands

**Alignment Mechanisms:**
- Strategic planning sessions
- Quarterly business reviews (QBR)
- Architecture review boards
- Portfolio steering committees
- Town halls & AMAs

## Шаблоны и Инструменты

### Strategic Plan Template

См. `assets/strategic-plan-template.md` для полного шаблона на русском языке.

### Roadmap Template

См. `assets/roadmap-template.md` для визуальной дорожной карты.

### RICE Scoring Calculator

См. `assets/rice-calculator.md` для таблицы расчета приоритетов.

### Stakeholder Map Template

См. `assets/stakeholder-map.md` для mapping stakeholders.

## Best Practices

**1. Balance Horizons:**
- 70% текущий квартал (execution)
- 20% следующий квартал (planning)
- 10% exploration (innovation)

**2. Build in Flexibility:**
- Reserve 20-30% capacity для unpredictable work
- Quarterly re-planning cycles
- Ability to pivot based on learnings

**3. Measure Progress:**
- Leading indicators (velocity, quality)
- Lagging indicators (business metrics)
- Monthly metric reviews

**4. Communicate Transparently:**
- Share roadmap broadly
- Explain prioritization decisions
- Update on changes promptly

**5. Iterate and Learn:**
- Quarterly retrospectives на strategy
- What worked / what didn't
- Adjust planning process

## Common Pitfalls

❌ **Overcommitment**: Planning 100% capacity без buffer
✅ Plan для 70-80% known capacity

❌ **Feature Factory**: Roadmap как список features
✅ Focus на outcomes и impact

❌ **Top-Down Only**: Strategy без team input
✅ Bottom-up + top-down alignment

❌ **Set and Forget**: Roadmap не обновляется
✅ Living document с regular updates

❌ **No Trade-offs**: Trying to do everything
✅ Clear prioritization и conscious choices

## Success Metrics

- **Stakeholder Alignment**: >90% executive agreement на roadmap
- **Delivery Predictability**: 80%+ roadmap items delivered on time
- **Business Impact**: Measurable progress на OKRs/KPIs
- **Team Clarity**: >85% team understanding of priorities
- **Flexibility**: Ability to pivot без major disruption

## References

- [Product Roadmap Guide](references/roadmap-guide.md) - Детальное руководство по roadmapping
- [Prioritization Frameworks](references/prioritization-frameworks.md) - Сравнение методов приоритизации
- [Strategic Planning Examples](references/strategy-examples.md) - Примеры из AWS, Google, Microsoft
