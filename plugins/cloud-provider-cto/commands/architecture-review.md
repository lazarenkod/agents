---
name: architecture-review
description: Проведение архитектурного ревью сервиса или компонента платформы
---

# Architecture Review

Проводит комплексный архитектурный ревью сервиса облачной платформы.

## Что делает эта команда

1. Анализирует architecture design document
2. Оценивает по Well-Architected Framework
3. Идентифицирует risks и issues
4. Проверяет compliance с platform standards
5. Формирует рекомендации по улучшению
6. Создает Architecture Decision Record (ADR)

## Review Criteria

### Operational Excellence
- [ ] Automated deployment pipeline
- [ ] Infrastructure as Code
- [ ] Monitoring и alerting
- [ ] Runbooks для operations
- [ ] Incident response procedures

### Security
- [ ] Encryption at rest и in transit
- [ ] IAM policies (least privilege)
- [ ] Network security (VPC, security groups)
- [ ] Secrets management
- [ ] Audit logging
- [ ] Compliance requirements met

### Reliability
- [ ] Multi-AZ deployment
- [ ] Fault tolerance design
- [ ] Auto-scaling configuration
- [ ] Backup и disaster recovery
- [ ] SLA/SLO defined

### Performance Efficiency
- [ ] Right-sizing analysis
- [ ] Caching strategy
- [ ] Database optimization
- [ ] CDN usage где appropriate
- [ ] Load testing completed

### Cost Optimization
- [ ] Resource tagging
- [ ] Right-sizing opportunities
- [ ] Reserved/Spot instance usage
- [ ] Storage tiering
- [ ] Unused resource cleanup

### Sustainability
- [ ] Energy-efficient instance types
- [ ] Resource utilization targets
- [ ] Carbon footprint consideration

## Результат

```markdown
# Architecture Review: [Service Name]

## Reviewers
- [Name], [Role]
- [Name], [Role]

## Review Date
YYYY-MM-DD

## Architecture Summary
[Brief description of architecture]

## Findings

### Critical Issues (Must Fix before Launch)
1. [Issue] - [Impact] - [Recommendation]

### High Priority (Fix within 30 days)
1. [Issue] - [Impact] - [Recommendation]

### Medium Priority (Fix within 90 days)
1. [Issue] - [Impact] - [Recommendation]

### Low Priority (Nice to have)
1. [Suggestion]

## Well-Architected Pillars Assessment

| Pillar | Score | Notes |
|--------|-------|-------|
| Operational Excellence | 7/10 | Missing automated rollback |
| Security | 9/10 | Strong security posture |
| Reliability | 6/10 | Single AZ deployment |
| Performance | 8/10 | Good caching strategy |
| Cost Optimization | 7/10 | Opportunities для savings |

## Decision
- [ ] Approved - Ready для launch
- [ ] Approved with conditions
- [ ] Requires major revision

## Action Items
- [ ] [Action 1] - Owner: [Name] - Due: [Date]
- [ ] [Action 2] - Owner: [Name] - Due: [Date]

## Next Review
[Date or trigger]
```

Документ сохраняется в Markdown на русском языке.
