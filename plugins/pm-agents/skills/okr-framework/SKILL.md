---
name: okr-framework
description: OKR (Objectives and Key Results) framework for setting goals, measuring progress, and aligning teams. Use when defining quarterly/annual goals, cascading company strategy, or implementing goal-setting practices.
---

# OKR Framework

Objectives and Key Results methodology для ambitious goal-setting, alignment, and measurable outcomes.

## When to Use This Skill

- Quarterly/annual planning cycles
- Cascading company strategy to teams
- Aligning cross-functional initiatives
- Measuring business impact of projects
- Setting ambitious yet achievable goals
- Executive strategy communication

## Core Concepts

### OKR Structure

```
Objective (O): Qualitative, aspirational goal
  ├── Key Result 1 (KR): Measurable outcome
  ├── Key Result 2 (KR): Measurable outcome
  └── Key Result 3 (KR): Measurable outcome

Objective: ЧТО мы хотим достичь (inspiring, qualitative)
Key Results: КАК мы измерим успех (specific, measurable, time-bound)
```

### Good vs Bad OKRs

**Good Objective:**
✅ "Стать лидирующей AI-платформой для enterprise"
✅ "Создать лучший developer experience в индустрии"
✅ "Достичь product-market fit для нового продукта"

**Bad Objective:**
❌ "Увеличить revenue на 20%" (это KR, не objective)
❌ "Сделать 10 features" (output, не outcome)
❌ "Поддерживать существующие системы" (BAU, не aspirational)

**Good Key Result:**
✅ "Увеличить enterprise ARR с $5M до $10M"
✅ "Достичь NPS 50+ (с текущих 35)"
✅ "Снизить deployment time с 4 часов до 30 минут"
✅ "Onboard 100 enterprise customers (с текущих 40)"

**Bad Key Result:**
❌ "Улучшить performance" (не measurable)
❌ "Запустить новый feature" (output, не outcome)
❌ "Работать над AI integration" (activity, не result)

## OKR Types

### Company OKRs
- 3-5 Objectives
- 3-4 Key Results каждый
- Annual + Quarterly
- CEO ownership
- Board alignment

### Team OKRs
- 2-3 Objectives
- 2-3 Key Results каждый
- Quarterly
- Team Lead ownership
- Alignment с Company OKRs

### Individual OKRs
- 1-2 Objectives
- 2-3 Key Results каждый
- Quarterly
- Individual ownership
- 50% aligned, 50% aspirational

## OKR Template

```markdown
## Q[N] [YEAR] OKRs - [Team/Company]

### Objective 1: [Inspiring qualitative goal]

**Alignment**: [Company OKR или Strategic Theme]
**Owner**: [Name/Team]
**Priority**: P0/P1/P2

**Why it Matters**:
[1-2 предложения о бизнес-impact]

**Key Results**:

- **KR 1.1**: [Metric] from [baseline] to [target]
  - **Baseline**: [Current value]
  - **Target**: [Goal value]
  - **Q1 Progress**: [Update]
  - **Confidence**: 🟢 High / 🟡 Medium / 🔴 Low
  - **Owner**: [Name]

- **KR 1.2**: [Metric] from [baseline] to [target]
  - **Baseline**: [Current value]
  - **Target**: [Goal value]
  - **Q1 Progress**: [Update]
  - **Confidence**: 🟢 High / 🟡 Medium / 🔴 Low
  - **Owner**: [Name]

- **KR 1.3**: [Metric] from [baseline] to [target]
  - **Baseline**: [Current value]
  - **Target**: [Goal value]
  - **Q1 Progress**: [Update]
  - **Confidence**: 🟢 High / 🟡 Medium / 🔴 Low
  - **Owner**: [Name]

**Grade**: [Final score 0.0-1.0]
**Status**: ⚪ Not Started / 🔵 On Track / 🟡 At Risk / 🔴 Off Track / ✅ Achieved

---

### Objective 2: [Another inspiring goal]

[Repeat structure]

---

## Cross-Functional Dependencies

| Our KR | Depends On | Team | Status |
|--------|------------|------|--------|
| KR 1.2 | API endpoint delivery | Platform Team | 🟢 On Track |
| KR 2.1 | Design system update | Design Team | 🟡 Delayed |

---

## Initiatives Supporting OKRs

| Initiative | Supporting OKR | Status | Timeline |
|-----------|---------------|--------|----------|
| [Project A] | O1: KR1.1, KR1.2 | On Track | Q1-Q2 |
| [Project B] | O2: KR2.1 | At Risk | Q1 |
```

## OKR Scoring

### Grading Scale

**1.0 = 100%**: Fully achieved or exceeded
**0.7 = 70%**: Substantial progress, good outcome
**0.3 = 30%**: Some progress, fell short
**0.0 = 0%**: No progress

### Interpretation

**0.7-1.0**: 🟢 Success
- Ambitious goal largely achieved
- Stretch targets с reasonable completion

**0.4-0.6**: 🟡 Partial Success
- Made progress, но fell short
- Learn and adjust

**0.0-0.3**: 🔴 Miss
- Significant gap
- Retrospective needed
- Re-assess feasibility

### Scoring Example

```markdown
### Objective: Achieve Product-Market Fit for AI Assistant

**KR 1**: Increase daily active users from 1K to 10K
- **Actual**: 6K DAU
- **Score**: 0.5 (50% of stretch goal)

**KR 2**: Achieve NPS of 50+ (from 30)
- **Actual**: NPS 48
- **Score**: 0.9 (90% achieved)

**KR 3**: Reduce churn from 8% to 3%
- **Actual**: Churn at 4%
- **Score**: 0.8 (80% improvement)

**Overall Objective Score**: (0.5 + 0.9 + 0.8) / 3 = 0.73 (Success!)
```

## OKR Cascading

### Top-Down Alignment

```
Company OKR
  ├── Engineering Department OKR (supports Company KR 1)
  │   ├── Platform Team OKR (supports Eng KR 1, 2)
  │   ├── Product Team OKR (supports Eng KR 2, 3)
  │   └── Infrastructure Team OKR (supports Eng KR 1)
  │
  ├── Product Department OKR (supports Company KR 2)
  │   ├── PM Team OKR
  │   └── Design Team OKR
  │
  └── Sales Department OKR (supports Company KR 3)
```

### Example Cascade

**Company O**: Become the #1 AI platform for developers

**Company KR**: Grow developer user base from 100K to 500K

↓ Cascades to:

**Engineering O**: Deliver world-class developer experience

**Eng KR 1**: Reduce API latency p95 from 500ms to 100ms
**Eng KR 2**: Achieve 99.99% uptime (from 99.5%)

↓ Cascades to:

**Platform Team O**: Build scalable, reliable infrastructure

**Platform KR 1**: Deploy autoscaling reducing latency spikes by 60%
**Platform KR 2**: Implement multi-region failover (zero downtime)

## OKR Planning Process

### Timeline

**Week 1-2: Input Gathering**
- Company strategy review
- Customer feedback analysis
- Market research
- Team retrospectives
- Bottom-up proposals

**Week 3-4: Draft Creation**
- Leadership drafts company OKRs
- Teams propose alignment
- Cross-functional review
- Dependencies identified

**Week 5-6: Refinement**
- Stakeholder feedback
- Feasibility validation
- Resource alignment
- Final adjustments

**Week 7: Finalization**
- Executive approval
- Company-wide communication
- Team cascading
- Kickoff meetings

### Stakeholder Involvement

| Role | Responsibility |
|------|----------------|
| **CEO** | Set company vision, approve company OKRs |
| **Executives** | Propose department OKRs, align cross-functionally |
| **Directors** | Cascade to team OKRs, ensure feasibility |
| **Team Leads** | Define team OKRs, identify initiatives |
| **ICs** | Contribute to team OKRs, set individual goals |

## Monitoring & Review

### Weekly Check-ins

```markdown
# OKR Check-in - Week [N]

**Team**: [Name]
**Date**: [Date]

## Progress Update

### O1: [Objective]

**KR 1.1**: [Metric]
- **Target**: [Goal]
- **Current**: [Value]
- **Progress**: [%] (🟢/🟡/🔴)
- **Blockers**: [If any]
- **This week**: [Planned actions]

**KR 1.2**: [Metric]
[Repeat]

## Highlights
- ✅ [Achievement 1]
- ✅ [Achievement 2]

## Blockers
- 🚨 [Blocker 1]: [Description and ask]

## Help Needed
- [Request 1]
```

### Monthly Business Reviews

```markdown
# Monthly OKR Review - [Month]

## Overall Health

| Objective | Score | Confidence | Trend |
|-----------|-------|----------|--------|
| O1 | 0.6 | 🟡 Medium | ↑ Improving |
| O2 | 0.4 | 🔴 Low | → Flat |
| O3 | 0.8 | 🟢 High | ↑ Improving |

## Deep Dive: At-Risk OKRs

### O2: [Objective] (🔴 At Risk)

**Current State**: [Summary]

**Root Causes**:
- [Cause 1]
- [Cause 2]

**Recovery Plan**:
- [Action 1]: [Owner] - [Date]
- [Action 2]: [Owner] - [Date]

**Revised Forecast**: [New expected score]

## Lessons Learned
- [Learning 1]
- [Learning 2]
```

## Best Practices

### Writing Effective OKRs

✅ **Aspirational not Incremental**: Stretch goals (70% success = good)
✅ **Outcome not Output**: Measure impact, не activities
✅ **Specific and Measurable**: Clear metrics, no ambiguity
✅ **Time-Bound**: Quarterly cadence
✅ **Limited in Number**: 3-5 objectives, 2-4 KRs each
✅ **Aligned**: Support higher-level OKRs
✅ **Transparent**: Visible to entire organization

### Common Anti-Patterns

❌ **Sandbagging**: Setting easy targets
✅ 70% achievement = success shows ambition

❌ **Too Many OKRs**: >5 objectives = no focus
✅ 3-5 max, prioritize ruthlessly

❌ **Activity-Based**: "Ship 10 features"
✅ Outcome-based: "Increase engagement by 30%"

❌ **Set and Forget**: No progress tracking
✅ Weekly check-ins, monthly reviews

❌ **100% Completion Expectation**: Treating as commitments
✅ 60-70% = success for stretch goals

❌ **Individual Performance Evaluation**: Using for comp/promotion
✅ Separate OKRs from performance reviews

## OKR vs Other Frameworks

| Framework | Focus | Cadence | Style |
|-----------|-------|---------|-------|
| **OKRs** | Aspirational outcomes | Quarterly | Stretch goals (70% success) |
| **KPIs** | Business health | Ongoing | Metrics to maintain |
| **MBOs** | Individual commitments | Annual | Performance-linked |
| **SMART Goals** | Tactical tasks | Varies | 100% achievable |

**When to use OKRs**: Strategic alignment, ambitious goals
**When to use KPIs**: Operational health, ongoing monitoring
**Combination**: OKRs для strategy, KPIs для BAU metrics

## Templates

См. `assets/` для:
- `okr-template.md` - Quarterly OKR template
- `okr-planning-worksheet.md` - Planning guide
- `okr-review-template.md` - Monthly review
- `okr-cascade-example.md` - Cascading examples

## Success Criteria

- **Alignment**: 100% team OKRs link to company OKRs
- **Transparency**: All OKRs visible company-wide
- **Regular Reviews**: Weekly check-ins, monthly deep dives
- **Scoring**: 60-70% average achievement (shows ambition)
- **Learning**: Retrospectives feed next quarter planning
