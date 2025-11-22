---
name: risk-management
description: Comprehensive risk identification, assessment, mitigation, and monitoring for complex technical projects. Use when planning high-stakes projects, managing uncertainties, or developing contingency plans.
---

# Risk Management

Systematic approach to identifying, assessing, mitigating, and monitoring risks in complex technical initiatives.

## When to Use This Skill

- Planning high-stakes projects with significant uncertainty
- Executive stakeholder alignment on project risks
- Developing contingency and mitigation plans
- Monthly/quarterly risk reviews
- Crisis management and incident response
- Change management with organizational impact

## Core Concepts

### Risk Management Framework

```
Identify → Assess → Prioritize → Mitigate → Monitor → Report

Непрерывный цикл:
┌─→ Identify Risks
│   ↓
│   Assess Impact & Probability
│   ↓
│   Prioritize by Exposure
│   ↓
│   Plan Mitigation
│   ↓
│   Execute Mitigation
│   ↓
│   Monitor Progress
│   ↓
└── Update Risk Register
```

### Risk Categories

**Technical Risks:**
- Architecture scalability limitations
- Technology selection uncertainty
- Technical debt impact
- Integration complexity
- Performance bottlenecks
- Security vulnerabilities
- Data migration challenges

**Operational Risks:**
- Infrastructure failures
- Deployment issues
- Monitoring gaps
- Incident response capabilities
- Disaster recovery
- Vendor dependencies

**Resource Risks:**
- Key person dependencies
- Hiring delays
- Team turnover
- Skill gaps
- Budget overruns
- Infrastructure costs

**Schedule Risks:**
- Estimation inaccuracy
- Scope creep
- Dependency delays
- External blockers
- Regulatory approvals
- Market timing

**Organizational Risks:**
- Stakeholder misalignment
- Organizational changes
- Competing priorities
- Political challenges
- Cultural resistance
- Communication gaps

**External Risks:**
- Vendor/partner failures
- Regulatory changes
- Market shifts
- Competitive moves
- Economic conditions
- Technology obsolescence

## Risk Assessment

### Risk Matrix

```
         IMPACT
         ↑
    High │ 🟡 M │ 🔴 H │ 🔴 C │
         ├──────┼──────┼──────┤
  Medium │ 🟢 L │ 🟡 M │ 🔴 H │
         ├──────┼──────┼──────┤
     Low │ 🟢 L │ 🟢 L │ 🟡 M │
         └──────┴──────┴──────┘→
           Low   Med   High
              PROBABILITY

Legend:
🔴 Critical (C): Immediate action required
🔴 High (H): Senior leadership involvement
🟡 Medium (M): Active monitoring, mitigation planning
🟢 Low (L): Accept or monitor
```

### Impact Assessment Scale

**Critical (5):**
- Project failure / cancellation
- >$1M financial impact
- Major security breach
- Significant customer churn
- Regulatory violations

**High (4):**
- Major milestone delays (>1 month)
- $500K-$1M financial impact
- Service degradation
- Executive escalation
- Team morale crisis

**Medium (3):**
- Minor delays (1-4 weeks)
- $100K-$500K financial impact
- Reduced functionality
- Increased technical debt
- Resource reallocation needed

**Low (2):**
- Minimal delays (<1 week)
- <$100K financial impact
- Minor user impact
- Manageable with current resources

**Negligible (1):**
- No significant impact
- Easily absorbed
- Standard operational variance

### Probability Assessment

**Very High (5)**: >80% likelihood
**High (4)**: 60-80% likelihood
**Medium (3)**: 40-60% likelihood
**Low (2)**: 20-40% likelihood
**Very Low (1)**: <20% likelihood

### Risk Exposure

```
Risk Exposure = Impact × Probability

Example:
Impact: 4 (High)
Probability: 3 (Medium)
Exposure: 12 (High Priority)

Prioritization:
Critical: 20-25
High: 15-19
Medium: 8-14
Low: 1-7
```

## Risk Register Template

```markdown
# Risk Register - [Project Name]

**Last Updated**: [Date]
**Owner**: [PM Name]

## Active Risks

### RISK-001: [Risk Title]

**Category**: [Technical/Resource/Schedule/Operational/External]
**Status**: [Open/In Mitigation/Closed/Occurred]
**Owner**: [Name]
**Identified**: [Date]

**Description:**
[Подробное описание риска и potential impact]

**Impact**: ⬛⬛⬛⬛⬜ (4/5) - High
**Probability**: ⬛⬛⬛⬜⬜ (3/5) - Medium
**Exposure**: 12 (High Priority)

**Triggers/Indicators:**
- [Раннее предупреждение 1]
- [Раннее предупреждение 2]

**Mitigation Strategy:**
- [Action 1]: [Owner] - [Due Date] - [Status]
- [Action 2]: [Owner] - [Due Date] - [Status]

**Contingency Plan:**
[Что делать если риск реализуется]

**Updates:**
- [Date]: [Update description]

---

### RISK-002: Key Engineer Departure

**Category**: Resource
**Status**: In Mitigation
**Owner**: Engineering Manager
**Identified**: 2024-01-15

**Description:**
Lead backend engineer показывает признаки burnout и может уйти.
Critical знания по legacy системе concentrated с этим инженером.

**Impact**: ⬛⬛⬛⬛⬛ (5/5) - Critical
**Probability**: ⬛⬛⬜⬜⬜ (2/5) - Low
**Exposure**: 10 (Medium Priority)

**Triggers/Indicators:**
- Снижение engagement в meetings
- Increase в sick days
- Negative feedback в 1-on-1s
- Decreased code contributions

**Mitigation Strategy:**
- [✅] Провести retention conversation - EM - 2024-01-20
- [🔄] Knowledge transfer sessions запланированы - Team Lead - Ongoing
- [⏳] Документирование legacy системы - Engineer - 2024-02-15
- [⏳] Cross-training второго инженера - Team - 2024-03-01

**Contingency Plan:**
1. Offer counter-offer с retention bonus
2. Extended notice period negotiation (30-60 days)
3. Contractor backup identified
4. Reduce scope non-critical features

**Updates:**
- 2024-01-25: Had retention conversation. Engineer agreed to stay, working on workload reduction.
```

## Mitigation Strategies

### Strategy Types

**1. Avoid**
- Eliminate риск полностью
- Change approach или scope
- Example: Риск vendor lock-in → Use open-source alternative

**2. Mitigate**
- Reduce вероятность или impact
- Proactive actions
- Example: Hiring риск → Start recruiting early

**3. Transfer**
- Shift риск to third party
- Insurance, vendors, partners
- Example: Infrastructure риск → Use managed cloud services

**4. Accept**
- Acknowledge and monitor
- Have contingency plan
- Example: Minor UX риск → Accept, gather user feedback post-launch

### Mitigation Plan Template

```markdown
## Mitigation Plan: [Risk ID]

**Objective**: [What we want to achieve]

**Strategy**: [Avoid/Mitigate/Transfer/Accept]

**Actions**:

| # | Action | Owner | Due Date | Status | Dependencies |
|---|--------|-------|----------|--------|--------------|
| 1 | [Action description] | [Name] | [Date] | 🟢 Done | None |
| 2 | [Action description] | [Name] | [Date] | 🟡 In Progress | Action 1 |
| 3 | [Action description] | [Name] | [Date] | ⚪ Not Started | Action 2 |

**Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Metrics:**
- [Метрика showing risk reduction]

**Budget**: $[Amount] (if applicable)

**Timeline**: [Duration]

**Review Date**: [When to reassess]
```

## Risk Monitoring

### Early Warning Indicators

**Technical Risks:**
- Test coverage trending down
- Build times increasing
- Incident rate increasing
- Technical debt metrics rising
- Performance degradation

**Resource Risks:**
- Team velocity declining
- Unplanned attrition
- Hiring pipeline empty
- Budget burn rate high
- Overtime trending up

**Schedule Risks:**
- Velocity < planned
- Scope creep ratio >10%
- Dependencies slipping
- Quality metrics degrading
- Testing phase compressed

### Risk Dashboard

```markdown
# Risk Dashboard - [Month Year]

## Risk Summary

| Risk Level | Count | % Total | Trend |
|-----------|-------|---------|-------|
| 🔴 Critical | 2 | 10% | ↓ -1 |
| 🔴 High | 5 | 25% | → |
| 🟡 Medium | 8 | 40% | ↑ +2 |
| 🟢 Low | 5 | 25% | ↓ -1 |
| **Total** | **20** | **100%** | → |

## Top 5 Risks

| ID | Risk | Exposure | Trend | Owner | Status |
|----|------|----------|-------|-------|--------|
| R-003 | Infrastructure scaling | 20 | ↓ | DevOps Lead | Mitigating |
| R-007 | Dependency на Team B | 16 | → | PM | Open |
| R-012 | Security audit deadline | 15 | ↑ | Security Lead | Escalated |
| R-001 | Key person risk | 12 | ↓ | EM | In Progress |
| R-005 | Budget overrun | 12 | → | Finance | Monitoring |

## Risks Closed This Month

- R-004: Performance bottleneck - Resolved through caching layer
- R-009: Vendor dependency - Alternative vendor onboarded

## New Risks This Month

- R-015: Regulatory change - New compliance requirements
- R-016: Market competition - Competitor launched similar feature
```

## Best Practices

✅ **Regular Reviews**: Weekly for high-risk projects, monthly for stable
✅ **Blameless Culture**: Focus on системные факторы, не люди
✅ **Quantify When Possible**: Use data over gut feel
✅ **Document Assumptions**: Risk assessment основан на assumptions
✅ **Escalate Appropriately**: Don't hide critical risks
✅ **Learn from Incidents**: Convert incidents to risk mitigation
✅ **Cross-Functional Input**: Involve eng, product, security, ops

## Common Pitfalls

❌ **Ignoring Low-Probability/High-Impact**: "It won't happen to us"
✅ Plan for black swan events

❌ **Static Risk Register**: Written once, never updated
✅ Living document с regular updates

❌ **No Ownership**: Risks без assigned owners
✅ Clear ownership и accountability

❌ **Insufficient Mitigation**: "We're monitoring it"
✅ Proactive mitigation actions

❌ **Over-Optimism**: Underestimating probability
✅ Realistic, data-driven assessment

## Templates

См. `assets/` для:
- `risk-register-template.md` - Полный риск регистр
- `risk-assessment-matrix.xlsx` - Scoring matrix
- `mitigation-plan-template.md` - План митигации
- `risk-review-template.md` - Monthly risk review

## Success Criteria

- **Early Identification**: Risks identified before impact
- **Ownership**: 100% risks have assigned owners
- **Mitigation Progress**: >70% high risks have active mitigation
- **No Surprises**: Major issues were on risk register
- **Learning**: Post-mortems feed back into risk register
