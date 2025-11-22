---
name: status-report
description: Generate comprehensive project status reports with progress tracking, metrics, risks, and blockers. Creates executive-ready reports in Russian markdown format.
---

# Status Report Generator

Создание профессиональных статус-репортов для stakeholders с метриками, прогрессом, рисками и blockers.

## Типы отчетов

1. **Weekly Status** - Еженедельный отчет для команды
2. **Executive Summary** - Краткий отчет для executives (1-pager)
3. **Monthly Business Review** - Детальный месячный обзор
4. **Quarterly Report** - Квартальный отчет с OKR scores

## Процесс генерации

### Базовая информация

1. **Тип отчета**: Weekly/Executive/Monthly/Quarterly
2. **Проект/Команда**: Название
3. **Период**: Даты
4. **Аудитория**: Кто получатели

### Прогресс и метрики

1. **Overall Status**: 🟢 On Track / 🟡 At Risk / 🔴 Off Track
2. **Key Milestones**: Progress против плана
3. **Metrics**: KPIs и их значения
4. **OKR Progress** (если applicable)

### Highlights & Achievements

1. Что завершили за период?
2. Key wins
3. Team achievements

### Blockers & Risks

1. Current blockers
2. Top risks
3. Help needed

### Next Steps

1. Priorities для следующего периода
2. Upcoming milestones
3. Key decisions needed

## Templates

### Weekly Status Report

```markdown
# Weekly Status Report - [Project Name]

**Week**: [Start Date] - [End Date]
**Project Manager**: [Name]
**Status**: 🟢 On Track

---

## Executive Summary

[2-3 предложения: overall status, key progress, major concerns]

---

## Progress This Week

### Completed
- ✅ [Achievement 1]: [Brief description]
- ✅ [Achievement 2]: [Brief description]
- ✅ [Achievement 3]: [Brief description]

### In Progress
- 🔄 [Item 1]: [Status and ETA]
- 🔄 [Item 2]: [Status and ETA]

### Planned for Next Week
- 📋 [Priority 1]
- 📋 [Priority 2]
- 📋 [Priority 3]

---

## Metrics

| Metric | Target | Current | Trend | Status |
|--------|--------|---------|-------|--------|
| Sprint Velocity | 40 pts | 38 pts | → | 🟢 |
| Cycle Time | <5 days | 4.2 days | ↓ | 🟢 |
| Bug Count | <10 | 12 | ↑ | 🟡 |
| Test Coverage | >80% | 82% | ↑ | 🟢 |

---

## Milestones Tracker

| Milestone | Target Date | Status | Confidence |
|-----------|-------------|--------|-----------|
| Alpha Release | Jan 15 | On Track | 🟢 High |
| Beta Launch | Feb 1 | At Risk | 🟡 Medium |
| GA | Feb 15 | On Track | 🟢 High |

---

## Risks & Blockers

### 🚨 Blockers (Need Immediate Attention)
1. **[Blocker 1]**: [Description]
   - **Impact**: [Impact description]
   - **Help Needed**: [Specific ask]
   - **Owner**: [Name]

### ⚠️ Top Risks
| Risk | Impact | Probability | Mitigation | Owner |
|------|--------|-------------|------------|-------|
| [Risk 1] | High | Medium | [Mitigation] | [Name] |
| [Risk 2] | Medium | High | [Mitigation] | [Name] |

---

## Team Health

- **Team Size**: [N] engineers, [M] PM/Design
- **Velocity**: [Trend over last 4 weeks]
- **Morale**: 🟢 Good / 🟡 Concerns / 🔴 Issues
- **Attrition**: None / [Details if any]

---

## Decisions Needed

1. **[Decision 1]**: [Description and options]
   - **By When**: [Date]
   - **Decision Maker**: [Role]

---

## Next Week Priorities

1. **Priority 1**: [Description]
2. **Priority 2**: [Description]
3. **Priority 3**: [Description]

---

**Questions or concerns? Contact: [PM Name]**
```

### Executive One-Pager

```markdown
# Executive Status - [Project Name]

**Date**: [Date]
**PM**: [Name]
**Overall Status**: 🟢 On Track

---

## Summary

[3-4 bullet points: overall progress, key wins, major risks, next milestone]

---

## Health Dashboard

| Dimension | Status | Trend | Notes |
|-----------|--------|-------|-------|
| **Schedule** | 🟢 | → | On track for Feb 15 GA |
| **Budget** | 🟢 | → | 85% utilization, within forecast |
| **Quality** | 🟡 | ↓ | Bug count up, addressing |
| **Team** | 🟢 | → | Morale good, no attrition |
| **Stakeholders** | 🟢 | ↑ | High satisfaction scores |

---

## Key Metrics

| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| OKR Score | 0.7 | 0.6 | 🟡 |
| Deployment Freq | Daily | 2.3/day | 🟢 |
| Customer NPS | 50+ | 48 | 🟡 |
| Uptime | 99.9% | 99.95% | 🟢 |

---

## Top 3 Wins This Month

1. **[Win 1]**: [Impact]
2. **[Win 2]**: [Impact]
3. **[Win 3]**: [Impact]

---

## Top 3 Risks

1. **[Risk 1]** (High Impact, Medium Probability)
   - **Mitigation**: [Plan]

2. **[Risk 2]** (Medium Impact, High Probability)
   - **Mitigation**: [Plan]

3. **[Risk 3]** (High Impact, Low Probability)
   - **Mitigation**: [Plan]

---

## Upcoming Milestones

- **Feb 1**: Beta launch (🟡 At risk due to testing delays)
- **Feb 15**: GA (🟢 On track)
- **Feb 28**: Post-launch review (Scheduled)

---

## Ask

1. **[Ask 1]**: [Specific request from executives]
2. **[Ask 2]**: [Specific request from executives]

---

**Next Update**: [Date]
```

### Monthly Business Review

```markdown
# Monthly Business Review - [Month Year]

**Team**: [Name]
**Prepared by**: [PM Name]
**Date**: [Date]

---

## Executive Summary

### Overall Health: 🟢 On Track

[Paragraph summarizing month: achievements, challenges, outlook]

### Key Highlights
- [Highlight 1]
- [Highlight 2]
- [Highlight 3]

### Key Challenges
- [Challenge 1]
- [Challenge 2]

---

## OKR Progress

### Objective 1: [Objective Name]

| KR | Target | Progress | Score | Status |
|----|--------|----------|-------|--------|
| KR 1.1 | [Target] | [Current] | 0.6 | 🟡 |
| KR 1.2 | [Target] | [Current] | 0.8 | 🟢 |
| KR 1.3 | [Target] | [Current] | 0.4 | 🔴 |

**Objective Score**: 0.6 (On Track for 0.7)

**Deep Dive on At-Risk KRs**:
- **KR 1.3**: [Analysis and recovery plan]

### Objective 2: [Objective Name]
[Repeat structure]

---

## Key Metrics Trends

### Business Metrics

| Metric | Month -2 | Month -1 | Current | Target | Trend |
|--------|----------|----------|---------|--------|-------|
| Revenue | $X | $Y | $Z | $T | ↑ |
| Users | N | M | K | Goal | ↑ |
| NPS | X | Y | Z | 50+ | → |

### Delivery Metrics

| Metric | Month -2 | Month -1 | Current | Target | Trend |
|--------|----------|----------|---------|--------|-------|
| Velocity | X pts | Y pts | Z pts | W pts | ↑ |
| Cycle Time | X days | Y days | Z days | <5 days | ↓ |
| Deployment Freq | X/day | Y/day | Z/day | Daily | ↑ |
| Change Fail Rate | X% | Y% | Z% | <5% | ↓ |

---

## Accomplishments

### Major Deliverables
1. **[Deliverable 1]**: [Description and impact]
2. **[Deliverable 2]**: [Description and impact]
3. **[Deliverable 3]**: [Description and impact]

### Team Achievements
- [Achievement 1]
- [Achievement 2]

---

## Challenges & Learnings

### Challenges
1. **[Challenge 1]**: [Description]
   - **Impact**: [Impact description]
   - **Resolution**: [How addressed or plan]

2. **[Challenge 2]**: [Description]
   - **Impact**: [Impact description]
   - **Resolution**: [How addressed or plan]

### Key Learnings
- [Learning 1]
- [Learning 2]

---

## Risk Dashboard

| Risk | Previous | Current | Trend | Mitigation Status |
|------|----------|---------|-------|------------------|
| [Risk 1] | High | Medium | ↓ | Mitigated |
| [Risk 2] | Medium | High | ↑ | In Progress |
| [Risk 3] | - | Medium | New | Planning |

**New Risks This Month**:
- [Risk 3]: [Description and plan]

---

## Resource & Budget

### Headcount
- **Current**: [N] FTE
- **Plan**: [M] FTE
- **Variance**: [+/- X] FTE
- **Open Roles**: [N] ([List])

### Budget
- **Allocated**: $[X]
- **Spent**: $[Y] ([Z]%)
- **Forecast**: On track / [Variance]
- **Main Costs**: [Breakdown]

---

## Next Month Priorities

1. **Priority 1**: [Description and expected outcome]
2. **Priority 2**: [Description and expected outcome]
3. **Priority 3**: [Description and expected outcome]

**Key Milestones**:
- [Date]: [Milestone 1]
- [Date]: [Milestone 2]

---

## Decisions Needed

1. **[Decision 1]**: [Context and options]
   - **Deadline**: [Date]
   - **Owner**: [Role]

---

## Appendix

### Detailed Metrics
[Additional charts, graphs, detailed breakdowns]

### Team Feedback
[Summary of team retrospective or feedback]
```

## Использование

```bash
# Generate weekly report
/status-report
> Type: Weekly
> Answer questions...

# Generate executive summary
/status-report
> Type: Executive
> Answer questions...

# Outputs saved to:
reports/
  ├── weekly/
  │   └── status-[date].md
  ├── executive/
  │   └── executive-summary-[date].md
  └── monthly/
      └── mbr-[month]-[year].md
```

## Best Practices

✅ **Consistent Format**: Use same template each time
✅ **Data-Driven**: Include actual metrics, not opinions
✅ **Action-Oriented**: Focus on what's next, не just what happened
✅ **Highlight Risks**: Be transparent about problems
✅ **Visual**: Use tables, emojis for quick scanning
✅ **Timely**: Send on consistent schedule

## Tips

- **Weekly**: Focus on tactical progress, blockers
- **Executive**: High-level, business impact focus
- **Monthly**: Comprehensive, trends, learnings
- **Keep it brief**: Respect reader's time

---

**Готовы создать статус репорт? Выберите тип и ответьте на вопросы.**
