---
name: dora-metrics
description: DORA (DevOps Research and Assessment) metrics framework for measuring and improving software delivery performance. Use when establishing delivery metrics, benchmarking team performance, or optimizing CI/CD processes.
---

# DORA Metrics Framework

Comprehensive guide to implementing and improving DORA metrics for elite software delivery performance.

## When to Use This Skill

- Establishing baseline delivery performance metrics
- Benchmarking against industry standards
- Identifying bottlenecks in delivery pipeline
- Measuring impact of process improvements
- Executive reporting on delivery velocity
- Team performance optimization

## Core Concepts

### The Four Key Metrics

**1. Deployment Frequency (DF)**
- **Определение**: Как часто происходят deployments в production
- **Elite**: On-demand (multiple deploys per day)
- **High**: Between once per day and once per week
- **Medium**: Between once per week and once per month
- **Low**: Between once per month and once per six months

**2. Lead Time for Changes (LT)**
- **Определение**: Время от commit до running в production
- **Elite**: Less than one hour
- **High**: Between one day and one week
- **Medium**: Between one week and one month
- **Low**: Between one month and six months

**3. Time to Restore Service (MTTR)**
- **Определение**: Время восстановления после incident
- **Elite**: Less than one hour
- **High**: Less than one day
- **Medium**: Between one day and one week
- **Low**: More than one week

**4. Change Failure Rate (CFR)**
- **Определение**: % deployments causing production issues
- **Elite**: 0-15%
- **High**: 16-30%
- **Medium**: 31-45%
- **Low**: 46-60%

## Implementation Guide

### Измерение Deployment Frequency

**Источники данных:**
- CI/CD pipeline logs (Jenkins, GitLab CI, GitHub Actions)
- APM tools (Datadog, New Relic)
- Git tags для releases
- Deployment tracking systems

**Расчет:**
```
DF = Total Production Deployments / Time Period

Пример:
- 120 deployments за 30 days
- DF = 4 deployments per day (Elite)
```

**SQL Query Example (для CI/CD базы):**
```sql
SELECT
    DATE(deployed_at) as deploy_date,
    COUNT(*) as deployments_per_day
FROM deployments
WHERE environment = 'production'
    AND deployed_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(deployed_at)
ORDER BY deploy_date DESC;
```

### Измерение Lead Time

**Компоненты Lead Time:**
```
Lead Time = Code Commit → Production
  ├── Coding Time (Commit → PR)
  ├── Review Time (PR Open → Approved)
  ├── Build Time (Merge → Build Complete)
  ├── Test Time (Build → Tests Pass)
  ├── Deployment Time (Deploy Start → Live)
  └── Validation Time (Live → Verified)
```

**Tracking Method:**
```python
# Расчет lead time через Git + CI/CD
lead_time = production_deploy_timestamp - first_commit_timestamp

# Детальная разбивка:
components = {
    'code_time': pr_created - first_commit,
    'review_time': pr_merged - pr_created,
    'ci_time': build_complete - pr_merged,
    'deploy_time': prod_live - build_complete
}
```

### Измерение MTTR

**Процесс измерения:**
```
MTTR = Time Incident Resolved - Time Incident Detected

Этапы:
1. Detection: Когда обнаружена проблема (monitoring alert)
2. Response: Когда команда начала работу
3. Diagnosis: Когда причина определена
4. Resolution: Когда проблема исправлена
5. Verification: Когда решение подтверждено
```

**Incident Tracking:**
| Incident ID | Detected | Resolved | Duration | Severity | Root Cause |
|-------------|----------|----------|----------|----------|------------|
| INC-001 | 10:15 | 10:42 | 27 min | P1 | Cache failure |
| INC-002 | 14:30 | 16:15 | 1h 45m | P0 | DB connection pool |

### Измерение Change Failure Rate

**Формула:**
```
CFR = (Failed Deployments / Total Deployments) × 100%

Failed Deployment определяется как:
- Rollback в течение 24 часов
- Hotfix deployment сразу после
- P0/P1 incident caused by deployment
- Degraded performance requiring intervention
```

**Tracking Table:**
| Deploy ID | Date | Status | Rollback | Incident | Notes |
|-----------|------|--------|----------|----------|-------|
| D-1001 | 2024-01-15 | Success | No | - | Clean deploy |
| D-1002 | 2024-01-15 | Failed | Yes | INC-003 | API errors |
| D-1003 | 2024-01-16 | Success | No | - | |

## Metrics Dashboard Template

### Executive Dashboard (Monthly)

```markdown
# DORA Metrics Report - [Месяц Год]

## Summary

| Metric | Current | Previous | Target | Status |
|--------|---------|----------|--------|--------|
| Deployment Frequency | 3.2/day | 2.8/day | 4/day | 🟡 |
| Lead Time | 6.5 hours | 8.2 hours | <4 hours | 🟡 |
| MTTR | 42 minutes | 65 minutes | <30 min | 🟡 |
| Change Failure Rate | 8% | 12% | <5% | 🟢 |

**Performance Level**: High (trending Elite)

## Trends

[Графики showing 3-month trend lines]

## Key Insights

**Improvements:**
- ✅ CFR снизился на 33% благодаря improved testing
- ✅ MTTR improvement через better runbooks
- ✅ Lead time reduction from pipeline optimization

**Areas for Focus:**
- 🎯 Increase deployment frequency to 4+/day
- 🎯 Reduce lead time below 4 hours
- 🎯 Achieve <30min MTTR consistently

## Action Items

1. [Action 1]: [Owner] - [Due date]
2. [Action 2]: [Owner] - [Due date]
```

## Improvement Strategies

### Improving Deployment Frequency

**Tactics:**
1. **Automate Everything**: Remove manual approval steps
2. **Small Batch Size**: Deploy smaller, incremental changes
3. **Feature Flags**: Decouple deploy from release
4. **Continuous Deployment**: Auto-deploy on green builds
5. **Remove Bottlenecks**: Eliminate deployment windows

**Anti-patterns:**
- ❌ Weekly release trains
- ❌ Manual approval gates
- ❌ Large batch releases
- ❌ Change advisory boards for every change

### Improving Lead Time

**Tactics:**
1. **Trunk-Based Development**: Reduce branch lifetime
2. **Fast CI Pipelines**: Optimize build/test time
3. **Parallel Testing**: Run tests concurrently
4. **Automated Code Review**: Static analysis pre-PR
5. **Reduce WIP**: Focus on completing work

**Bottleneck Analysis:**
```
Value Stream Map:
Commit → [2h] → PR Review → [4h] → CI Build → [30m] → Deploy → [15m] → Live
         ^^^^                ^^^^
    Optimization targets
```

### Improving MTTR

**Tactics:**
1. **Comprehensive Monitoring**: Detect issues faster
2. **Automated Rollback**: One-click revert capability
3. **Runbooks**: Document common issues
4. **Incident Response Process**: Clear escalation paths
5. **Practice Chaos Engineering**: Build muscle memory

**Incident Response Checklist:**
```markdown
- [ ] Incident detected and logged
- [ ] On-call engineer paged
- [ ] Initial assessment (5 min)
- [ ] War room established if needed
- [ ] Mitigation in progress
- [ ] Service restored
- [ ] Root cause identified
- [ ] Post-mortem scheduled
```

### Improving Change Failure Rate

**Tactics:**
1. **Comprehensive Testing**: Unit, integration, E2E, performance
2. **Canary Deployments**: Gradual rollout with monitoring
3. **Feature Flags**: Kill switch for problematic features
4. **Pre-Production Testing**: Staging environment parity
5. **Post-Deployment Monitoring**: Automated health checks

**Quality Gates:**
```yaml
pipeline:
  - unit_tests: >80% coverage
  - integration_tests: all pass
  - security_scan: no critical vulnerabilities
  - performance_test: <500ms p95 latency
  - canary_deploy: 5% traffic for 30min
  - full_deploy: monitor error rates
  - auto_rollback: if error rate >2%
```

## Benchmarking

### Industry Performance Levels

| Level | DF | Lead Time | MTTR | CFR |
|-------|----|-----------| -----|-----|
| **Elite** | On-demand (multiple/day) | <1 hour | <1 hour | 0-15% |
| **High** | Daily to weekly | 1 day - 1 week | <1 day | 16-30% |
| **Medium** | Weekly to monthly | 1 week - 1 month | 1 day - 1 week | 31-45% |
| **Low** | Monthly to 6 months | 1-6 months | >1 week | 46-60% |

### Company Size Context

**Startups (<50 people):**
- Target: High to Elite
- Focus: Speed, experimentation
- Common challenges: Quality processes

**Scale-ups (50-500):**
- Target: High
- Focus: Scaling practices, maintaining velocity
- Common challenges: Coordination overhead

**Enterprises (500+):**
- Target: Medium to High
- Focus: Consistency, compliance, coordination
- Common challenges: Organizational complexity

## Tools & Integration

### Recommended Tools

**CI/CD Analytics:**
- GitHub Actions insights
- GitLab CI/CD analytics
- CircleCI Insights
- Jenkins Blue Ocean

**APM & Monitoring:**
- Datadog DORA dashboard
- New Relic deployment tracking
- Honeycomb observability
- Grafana dashboards

**Incident Management:**
- PagerDuty analytics
- Opsgenie reporting
- Incident.io metrics

**All-in-One:**
- Sleuth.io (DORA-focused)
- LinearB
- Code Climate Velocity
- Swarmia

## Templates

См. `assets/` для:
- `dora-dashboard-template.md` - Шаблон дашборда
- `metrics-tracking-sheet.xlsx` - Таблица отслеживания
- `improvement-plan-template.md` - План улучшений
- `executive-report-template.md` - Executive отчет

## Common Pitfalls

❌ **Focusing on One Metric**: Оптимизация одной метрики за счет других
✅ Балансировать все 4 метрики

❌ **Vanity Metrics**: Tracking без action plans
✅ Metrics → Insights → Actions → Improvement

❌ **Blame Culture**: Использовать metrics для наказания
✅ Blameless culture, focus на системных улучшениях

❌ **Inconsistent Measurement**: Changing definitions часто
✅ Stable definitions, consistent tracking

## Success Criteria

- **Baseline Established**: 3 months consistent data
- **Trend Analysis**: Month-over-month improvement visibility
- **Team Awareness**: Everyone understands metrics
- **Actionable Insights**: Metrics drive specific improvements
- **Elite Performance**: Achieving elite in 2-3 metrics
