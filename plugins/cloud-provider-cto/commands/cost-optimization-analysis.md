---
name: cost-optimization-analysis
description: Анализ затрат платформы с рекомендациями по оптимизации
---

# Cost Optimization Analysis

Проводит глубокий анализ cloud costs и формирует actionable recommendations.

## Что делает эта команда

1. Анализирует current spend patterns
2. Идентифицирует waste и inefficiency
3. Находит optimization opportunities
4. Рассчитывает potential savings
5. Приоритизирует recommendations
6. Создает implementation roadmap

## Анализ включает

### Compute Optimization
- Idle instances
- Underutilized instances (right-sizing)
- RI/Savings Plan coverage
- Spot instance opportunities
- Autoscaling configuration

### Storage Optimization
- Old snapshots
- Unattached volumes
- Lifecycle policies
- Storage class optimization
- Data compression

### Database Optimization
- Underutilized instances
- Reserved instance opportunities
- Read replica optimization
- Connection pooling
- Query performance

### Network Optimization
- Data transfer costs
- NAT Gateway usage
- Load balancer optimization
- CDN opportunities

## Результат

```markdown
# Cloud Cost Optimization Analysis

## Executive Summary

**Total Monthly Spend**: $XXX,XXX
**Identified Savings**: $XX,XXX/month (XX%)
**Implementation Effort**: X weeks

Top 3 Opportunities:
1. Right-size oversized instances - $XX,XXX/month
2. Purchase RIs для steady workloads - $XX,XXX/month
3. Delete old snapshots - $X,XXX/month

## Current Spend Breakdown

| Category | Monthly Cost | % of Total |
|----------|-------------|-----------|
| Compute | $XXX,XXX | XX% |
| Storage | $XX,XXX | XX% |
| Database | $XX,XXX | XX% |
| Network | $XX,XXX | XX% |
| Other | $X,XXX | XX% |

## Optimization Opportunities

### Quick Wins (< 1 week, Low Risk)

#### 1. Delete Old Snapshots
- **Current Cost**: $X,XXX/month
- **Savings**: $X,XXX/month
- **Effort**: 1 day
- **Risk**: Low
- **Action**: Delete snapshots > 90 days old

[More opportunities...]

### Medium-Term (1-4 weeks)

#### X. Right-size Oversized Instances
[Details...]

### Strategic (1-3 months)

#### Y. Reserved Instance Strategy
[Details...]

## Implementation Roadmap

Week 1-2: Quick wins ($XX,XXX savings)
Week 3-6: Medium-term ($XX,XXX savings)
Month 2-3: Strategic ($XX,XXX savings)

Total Projected Savings: $XX,XXX/month

## Monitoring & Tracking

- Weekly cost review meetings
- Automated alerts для anomalies
- Monthly optimization report
```

Все recommendations сохраняются в Markdown на русском языке.
