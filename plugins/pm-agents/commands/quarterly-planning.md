---
name: quarterly-planning
description: Quarterly planning workflow for OKR setting, roadmap creation, resource allocation, and team alignment. Creates comprehensive quarterly plan in Russian markdown format.
---

# Quarterly Planning

Комплексное квартальное планирование с OKRs, roadmap, ресурсным планированием и alignment.

## Что создает команда

1. **Quarterly OKRs** - Цели и ключевые результаты на квартал
2. **Quarterly Roadmap** - Дорожная карта инициатив
3. **Resource Plan** - План распределения ресурсов
4. **Dependency Map** - Карта зависимостей между командами
5. **Risk Assessment** - Оценка квартальных рисков
6. **Success Metrics** - Метрики для отслеживания прогресса

## Процесс планирования

### Фаза 1: Review & Retrospective (Неделя 1)

**Вопросы:**
1. Какой квартал планируем? (Q1/Q2/Q3/Q4 [Год])
2. Какая команда/департамент?
3. Предыдущий квартал: что достигли? (OKR scores)
4. Что сработало хорошо?
5. Что нужно улучшить?
6. Carry-over items из прошлого квартала?

### Фаза 2: Strategic Alignment (Неделя 2)

**Alignment с Company OKRs:**
1. Какие Company OKRs на этот квартал?
2. Как наша команда contributes к Company OKRs?
3. Strategic priorities для команды?

### Фаза 3: OKR Definition (Неделя 3)

Для каждого Objective (2-3 max):

**Objective [N]:**
- Название (aspirational goal)
- Why it matters
- Alignment (какой Company OKR поддерживает)

**Key Results (2-3 per objective):**
- KR описание
- Baseline (текущее значение)
- Target (целевое значение)
- Measurement method
- Owner

### Фаза 4: Initiative Planning (Неделя 4)

Для каждой инициативы:
- Название и описание
- Supporting OKR/KR
- Scope и deliverables
- Timeline (weeks)
- Team размер (FTE)
- Dependencies
- Risks

### Фаза 5: Resource Allocation (Неделя 5)

**Capacity Analysis:**
1. Available team capacity (FTE)
2. Committed vs. discretionary work
3. Allocation по инициативам
4. Buffer для unexpected work
5. Hiring needs

### Фаза 6: Risk & Dependencies (Неделя 6)

**Dependencies:**
- Cross-team dependencies
- External dependencies (vendors, partners)
- Technical dependencies

**Risks:**
- Top quarterly risks
- Mitigation plans
- Contingencies

## Output структура

```
planning/Q[N]-[YEAR]/
  ├── okrs-q[n]-[year].md
  ├── roadmap-q[n]-[year].md
  ├── resource-plan-q[n]-[year].md
  ├── dependencies-q[n]-[year].md
  ├── risks-q[n]-[year].md
  └── metrics-dashboard-q[n]-[year].md
```

## Quarterly OKR Template

```markdown
# Q[N] [YEAR] OKRs - [Team Name]

**Owner**: [Team Lead]
**Period**: [Start Date] - [End Date]
**Status**: Planning / Active / Complete

---

## Objective 1: [Inspiring Goal]

**Why it Matters**: [1-2 sentences on business impact]
**Alignment**: [Company OKR X.Y]
**Priority**: P0

### Key Results

**KR 1.1**: [Metric] from [baseline] to [target]
- **Owner**: [Name]
- **Measurement**: [How measured]
- **Baseline**: [Current value]
- **Target**: [Goal value]
- **Confidence**: 🟢 High

**KR 1.2**: [Metric] from [baseline] to [target]
- **Owner**: [Name]
- **Measurement**: [How measured]
- **Baseline**: [Current value]
- **Target**: [Goal value]
- **Confidence**: 🟡 Medium

---

## Objective 2: [Another Goal]

[Repeat structure]

---

## Initiatives Supporting OKRs

| Initiative | OKR | Timeline | Team Size | Status |
|-----------|-----|----------|-----------|--------|
| [Project A] | O1: KR1.1, KR1.2 | Week 1-8 | 3 FTE | Planned |
| [Project B] | O2: KR2.1 | Week 4-12 | 2 FTE | Planned |

---

## Dependencies

| Dependency | Type | Owner Team | ETA | Risk |
|-----------|------|------------|-----|------|
| [API endpoint] | Blocker | Platform | Week 4 | 🟡 Medium |
| [Design system] | Input | Design | Week 2 | 🟢 Low |

---

## Top Quarterly Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | High | Medium | [Mitigation plan] |
| [Risk 2] | Medium | High | [Mitigation plan] |
```

## Roadmap Template

```markdown
# Q[N] [YEAR] Roadmap - [Team]

## Timeline View

### Month 1 (Weeks 1-4)
**Theme**: [Focus theme]

**Week 1-2**:
- [Milestone 1]
- [Deliverable 1]

**Week 3-4**:
- [Milestone 2]
- [Deliverable 2]

### Month 2 (Weeks 5-8)
[Repeat structure]

### Month 3 (Weeks 9-13)
[Repeat structure]

---

## By Initiative

### Initiative 1: [Name]
**OKR**: O1: KR1.1, KR1.2
**Timeline**: Week 1-8
**Team**: 3 engineers, 1 PM

**Phases**:
- Discovery (Week 1-2): [Activities]
- Implementation (Week 3-6): [Activities]
- Testing & Launch (Week 7-8): [Activities]

**Milestones**:
- Week 2: Design complete
- Week 6: Implementation complete
- Week 8: Launch

**Dependencies**:
- [Dependency 1]
```

## Resource Plan Template

```markdown
# Resource Plan Q[N] [YEAR]

## Team Capacity

**Total Available**: [N] FTE
**Committed Work**: [N] FTE ([%])
**Buffer**: [N] FTE ([%])

## Allocation by Initiative

| Initiative | FTE | % Capacity | Timeline |
|-----------|-----|------------|----------|
| Initiative 1 | 3.0 | 30% | Week 1-8 |
| Initiative 2 | 2.0 | 20% | Week 4-12 |
| Tech Debt | 1.5 | 15% | Ongoing |
| Maintenance | 2.0 | 20% | Ongoing |
| Buffer | 1.5 | 15% | - |
| **Total** | **10.0** | **100%** | |

## Allocation by Role

| Role | Headcount | Initiatives | Utilization |
|------|-----------|-------------|-------------|
| Senior Engineer | 3 | Init 1, 2 | 90% |
| Engineer | 5 | Init 1, 2, Maint | 85% |
| PM | 1 | All | 100% |
| Designer | 1 | Init 1 | 60% |

## Hiring Plan

- [Q1]: [N] engineers (Senior Backend)
- [Q2]: [N] engineers (Frontend)
```

## Best Practices

✅ **Bottom-up + Top-down**: Combine team input с company strategy
✅ **Ambitious but Realistic**: OKRs should stretch (70% = good)
✅ **Limited Focus**: 2-3 objectives max
✅ **Clear Ownership**: Every KR has owner
✅ **Buffer Capacity**: Plan 70-80% capacity, leave buffer
✅ **Dependency Awareness**: Map all cross-team dependencies
✅ **Risk-Adjusted**: Plan for known risks

## After Planning

**Communication:**
1. Team all-hands для OKR presentation
2. Cross-functional dependency sync
3. Executive readout
4. Documentation sharing (Confluence, Notion)

**Execution:**
1. Weekly OKR check-ins
2. Monthly business reviews
3. Dependency tracking
4. Risk monitoring

## Related Commands

- `/status-report` - Weekly/monthly progress tracking
- `/risk-review` - Quarterly risk reviews
- `/retrospective` - End-of-quarter retrospectives

---

**Готовы начать квартальное планирование? Ответьте на вопросы выше.**
