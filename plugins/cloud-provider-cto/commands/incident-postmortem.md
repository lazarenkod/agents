---
name: incident-postmortem
description: Создание blameless postmortem после инцидента
---

# Incident Postmortem

Создает comprehensive postmortem analysis после production incident.

## Что делает эта команда

1. Собирает incident data (timeline, impact, actions)
2. Анализирует root cause
3. Идентифицирует contributing factors
4. Определяет action items
5. Извлекает lessons learned
6. Создает blameless postmortem document

## Процесс

1. Сбор данных от участников incident response
2. Построение временной шкалы событий
3. Root cause analysis (5 Whys, Fishbone)
4. Impact assessment (customers, revenue, SLA)
5. Определение preventive measures
6. Формирование action items с owners

## Результат

```markdown
# Incident Postmortem: [Краткое описание]

## Metadata
- **Incident ID**: INC-2024-XXX
- **Date**: YYYY-MM-DD HH:MM UTC
- **Severity**: SEV1 / SEV2 / SEV3
- **Duration**: X hours Y minutes
- **Incident Commander**: [Name]
- **Participants**: [Names]

## Executive Summary

[2-3 предложения: что произошло, impact, resolution]

## Impact

- **Customers Affected**: X,XXX (XX%)
- **Services Affected**: [List]
- **Failed Requests**: X,XXX,XXX
- **Revenue Impact**: $XX,XXX (estimated)
- **SLA Breach**: Yes/No
  - Error Budget Consumed: XX%

## Timeline (all times UTC)

| Time | Event |
|------|-------|
| 14:00 | Normal operations |
| 14:15 | First alerts fired |
| 14:17 | On-call engineer acknowledged |
| 14:20 | Incident declared SEV2 |
| 14:25 | Root cause identified |
| 14:40 | Mitigation deployed |
| 15:00 | Service restored |
| 15:30 | Incident closed |

## Root Cause Analysis

### What Happened
[Detailed technical description]

### Why It Happened
[5 Whys analysis]

1. Why did service fail?
   - Database connection pool exhausted

2. Why was pool exhausted?
   - Traffic spike от new marketing campaign

3. Why didn't autoscaling handle it?
   - Max connection limit hit before autoscaling triggered

4. Why was limit insufficient?
   - Capacity planning didn't account for campaign

5. Why wasn't campaign communicated?
   - No process для cross-team coordination

### Contributing Factors
- Lack of traffic forecasting
- Insufficient monitoring на connection pool
- No alerting before exhaustion

## What Went Well

- ✅ Quick detection (2 minutes)
- ✅ Proper escalation
- ✅ Effective communication to customers
- ✅ Fast mitigation (25 minutes to resolution)

## What Went Poorly

- ❌ Preventable issue (capacity planning)
- ❌ Alert threshold too late
- ❌ No runbook для this scenario
- ❌ Marketing campaign not communicated

## Action Items

### Prevent Recurrence
- [ ] **Action**: Implement auto-scaling для connection pool
  - **Owner**: Database Team
  - **Due**: 2024-XX-XX
  - **Priority**: P0

- [ ] **Action**: Add pre-exhaustion alerts (80% threshold)
  - **Owner**: Monitoring Team
  - **Due**: 2024-XX-XX
  - **Priority**: P0

### Improve Detection
- [ ] **Action**: Enhanced monitoring dashboard
  - **Owner**: SRE Team
  - **Due**: 2024-XX-XX
  - **Priority**: P1

### Improve Response
- [ ] **Action**: Create runbook для connection pool issues
  - **Owner**: On-call Team
  - **Due**: 2024-XX-XX
  - **Priority**: P1

### Process Improvements
- [ ] **Action**: Marketing campaign notification process
  - **Owner**: Product Team
  - **Due**: 2024-XX-XX
  - **Priority**: P1

## Lessons Learned

1. **Technical**: Connection pool limits need monitoring
2. **Process**: Cross-team communication critical
3. **Cultural**: Blameless focus on systems

## Follow-up

- Next review: [Date]
- Tracking: [Link to issue tracker]

---

*This postmortem is blameless. Focus is on improving systems and processes, not blaming individuals.*
```

Все postmortems сохраняются в Markdown на русском языке.
