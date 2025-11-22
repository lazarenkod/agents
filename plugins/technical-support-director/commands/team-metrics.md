---
name: team-metrics
description: Generate comprehensive team performance metrics report with individual and team-level analytics.
---

# Team Performance Metrics Report

Генерирует детальный отчет о производительности команды support с индивидуальными и командными метриками.

## Параметры

- **Period**: Week/Month/Quarter
- **Team/Individual**: Specific team или all teams
- **Include**: CSAT, productivity, quality, skills

## Generated Report Format

```markdown
# Team Performance Report - [Period]

## Team Summary
- **Team Size**: X engineers
- **Total Tickets**: XXX
- **Avg Tickets/Engineer/Day**: X.X
- **Team CSAT**: XX.X%
- **Team NPS**: XX

## Individual Performance

| Engineer | Tickets | CSAT | Avg Resolution | SLA Compliance | Status |
|----------|---------|------|----------------|----------------|--------|
| Alice | XX | 95% | X.Xh | 98% | ⭐ Top Performer |
| Bob | XX | 92% | X.Xh | 96% | ✅ Meeting Expectations |
| Carol | XX | 85% | X.Xh | 90% | ⚠️ Needs Support |

## Coaching Recommendations
[Specific recommendations для каждого engineer]

## Team Development
[Training needs, skill gaps, growth opportunities]
```

Сохраняется в: `./team-reports/YYYY-MM-DD-team-metrics.md`
