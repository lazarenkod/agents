---
name: crisis-communication
description: Стратегии и тактики кризисной коммуникации при major incidents, outages и customer escalations. Охватывает internal и external communication, stakeholder management, и reputation protection. Use when managing crisis communication, coordinating messaging during incidents, or handling PR situations.
---

# Кризисная Коммуникация (Crisis Communication)

## Обязательные правила вывода
- Всегда отвечай **на русском**.
- Сохраняй артефакты в `outputs/technical-support-director/skills/crisis-communication/{timestamp}_{кратко}.md` через Write tool; обновляй один файл по итерациям.
- Формат: цель/контекст → аудитории/каналы → сообщение/частота → алерты/стоп-пороги → TODO → изменения vs прошлой версии.

## 3-итерационный контур
1) **Диагностика (минуты–1 ч):** кто затронут, что известно/неизвестно, риски, регуляторика, говорящие лица. Черновой бриф + риск/decision log.
2) **Дизайн (1–2 ч):** сообщения по аудиториям, каналы/частота, Q&A/FAQ, escalations, алерты/пороги, approval (легал/PR). Шаблоны сообщений.
3) **Верификация (в процессе):** своевременные апдейты, корректировки контента, журнал коммуникаций, пост-комм анализ, TODO/изменения.
## Когда Использовать

- Major outages или security breaches
- Executive escalations
- Public relations issues
- Multi-customer impact situations
- Regulatory или legal implications
- Media attention на инцидент

## Принципы Кризисной Коммуникации

### Ключевые Принципы

1. **Speed**: Быстрая initial response (within 1 hour)
2. **Accuracy**: Только проверенные facts
3. **Transparency**: Честность о проблеме и progress
4. **Empathy**: Признание impact на customers
5. **Accountability**: Ownership проблемы
6. **Consistency**: Единое сообщение через все каналы

### Коммуникационная Иерархия

```markdown
## Приоритет Коммуникации

1. **Safety/Security** (если применимо)
   - Immediate notification о security risks
   - Actions customers должны предпринять

2. **Business Impact**
   - Scope affected users/services
   - Current status
   - Workarounds если available

3. **Resolution Progress**
   - What we're doing
   - ETA если determinable
   - Next update time

4. **Prevention**
   - Root cause
   - Future preventive measures
```

## Internal Communication

### Incident Command Communication

**War Room Updates (Every 15-30 min для P1)**:
```markdown
## Internal Status Update #[N]

**Time**: [HH:MM UTC]
**Status**: [INVESTIGATING | IDENTIFIED | MITIGATING | RESOLVED]

**Technical Progress**:
- [Specific action completed]
- [Current hypothesis/findings]
- [Next technical step]

**Customer Impact**:
- Affected: [X users / Y% of base]
- Services: [List]
- Current workaround: [If available]

**Communication Status**:
- Status page: [Updated at HH:MM]
- Customer emails: [Sent to X customers]
- Executive brief: [Sent/Scheduled]

**Blockers**: [Any issues preventing progress]

**Next Update**: [HH:MM UTC]
```

### Executive Briefings

**Executive Summary Template**:
```markdown
# Executive Brief: [Incident Title]

**For**: [CEO/CTO/Board]
**Severity**: P1 - Critical
**Time**: [Current timestamp]
**Status**: [One-word status]

## The Bottom Line
[1-2 sentences: что случилось и current impact]

## Business Impact
- **Customers Affected**: [Number & % of base]
- **Revenue Impact**: [$X/hour or $Y total]
- **Reputation Risk**: [High/Medium/Low]
- **SLA Implications**: [Service credits estimate]

## What We're Doing
[3-5 bullet points of key actions]

## ETA Resolution
[Realistic estimate or "TBD - next update in X hours"]

## Your Action Needed
[Specific asks or "None - we have this handled"]

## Media/PR Status
[Any public attention, prepared statements]
```

## External Communication

### Customer Communication Templates

**Initial Notification (within 30 min)**:
```markdown
Subject: [URGENT] Service Issue Notification

We are currently investigating reports of [brief description].

**What We Know**:
- Issue started: [Time]
- Services affected: [List]
- Impact: [User-facing impact]

**What We're Doing**:
- Assembled technical team
- Actively investigating
- [Any immediate action taken]

**What You Should Do**:
- [Any customer action needed or "No action required"]
- [Workaround if available]

**Next Update**: [Specific time] or sooner if status changes

We apologize for the inconvenience and are working urgently to resolve this.

[Support Contact Info]
```

**Progress Update**:
```markdown
Subject: Update #[N] - [Incident]

**Current Time**: [Timestamp]
**Status**: [Making progress / Identified cause / Implementing fix]

**Since Last Update**:
✅ [Progress point 1]
✅ [Progress point 2]
🔄 [In progress action]

**Current Impact**: [Any improvement or change]

**Expected Resolution**: [ETA if possible]

**Next Update**: [Specific time]
```

**Resolution Notification**:
```markdown
Subject: RESOLVED - [Incident]

We have resolved the issue affecting [services].

**Resolution Summary**:
- Started: [Time]
- Resolved: [Time]
- Duration: [X hours Y minutes]
- Root Cause: [Brief explanation]

**Impact Analysis**:
- Users affected: [Number/percentage]
- Services: [List]

**What We Fixed**:
[1-2 sentence explanation]

**Prevention**:
To prevent recurrence, we are:
- [Immediate action]
- [Long-term improvement]

**Service Credit** (if applicable):
[Automatic application details]

**Follow-Up**:
We will share a detailed post-mortem within [timeframe].

We sincerely apologize for the disruption and appreciate your patience.
```

### Status Page Management

**Status Page Update Structure**:
```markdown
## [Incident Title]

**Posted**: [Date Time UTC]
**Status**: [Investigating | Identified | Monitoring | Resolved]
**Severity**: [Minor | Major | Critical]

### Latest Update ([Time UTC])
[Current status description]

**Affected Services**:
- Service A: [Performance Degraded | Partial Outage | Major Outage]
- Service B: [Operational | Performance Degraded]

**Timeline**:
- [HH:MM UTC] - Issue detected
- [HH:MM UTC] - Root cause identified
- [HH:MM UTC] - Fix deployed

**Next Update**: [Specific time or "Updates as available"]

---
[Previous updates in reverse chronological order]
```

## Stakeholder-Specific Communication

### VIP/Enterprise Customer Communication

**Должно быть**:
- Персонализированное (не массовое)
- Более детальное technical information
- Прямой контакт (phone/video, не только email)
- Executive-to-executive для major issues
- Proactive follow-up post-resolution

**Template**:
```markdown
Dear [Customer Executive],

I'm reaching out personally regarding [incident] affecting your environment.

**Your Specific Impact**:
- [Customized impact assessment]
- [Affected resources/users in their account]

**Dedicated Support**:
- Your contact: [Name, Direct Phone, Email]
- My direct line: [Your contact] (24/7 for this issue)

**Resolution Plan**:
[Specific plan relevant to their environment]

I will provide you updates every [X hours] or sooner.

[Your Name]
[Title]
```

### Media/PR Communication

**Key Principles**:
- **Single spokesperson**: Designated person только
- **Prepared statements**: Pre-approved messaging
- **Fact-based**: Avoid speculation
- **Empathy**: Acknowledge customer impact
- **Solutions-focused**: Emphasize resolution efforts

**Holding Statement**:
```markdown
We are aware of and currently investigating [issue]. Our teams are
working urgently to resolve this. We will provide updates as more
information becomes available. Customer safety and service reliability
are our top priorities.
```

## Post-Crisis Communication

### Post-Mortem Sharing

**Public Post-Mortem (для transparency)**:
```markdown
# Post-Mortem: [Incident Title]

**Date**: [Date]
**Duration**: [X hours]
**Impact**: [Y users affected]

## What Happened
[Accessible explanation for non-technical audience]

## Why It Happened
[Root cause in understandable terms]

## How We Fixed It
[Resolution approach]

## How We're Preventing It
[Specific preventive measures with timeline]

## What We Learned
[Key insights]

We apologize to all customers impacted and remain committed to earning
your trust through continuous improvement.
```

### Reputation Recovery

**Actions Post-Crisis**:
1. **Immediate** (0-24 hrs):
   - Personal outreach to affected VIP customers
   - Public acknowledgment и apology
   - Transparent post-mortem

2. **Short-term** (1-2 weeks):
   - Service credit processing
   - Customer success check-ins
   - Team retrospective и improvements

3. **Medium-term** (1-3 months):
   - Implement preventive measures
   - Enhanced monitoring
   - Customer advisory board feedback
   - Public sharing of improvements

## Communication Channels

### Channel Selection Matrix

| Audience | Channel | Timing | Purpose |
|----------|---------|--------|---------|
| All Customers | Status Page | Every 30-60 min | Broad updates |
| Enterprise | Direct Email | Hourly for P1 | Detailed info |
| VIP/Strategic | Phone/Video | As needed | Relationship |
| Internal Team | Slack/War Room | Real-time | Coordination |
| Executives | Email Brief | Every 2-4 hrs | Decision support |
| Public/Media | PR Statement | As needed | Reputation |

## References
- `templates/` - Коммуникационные шаблоны
- `scripts/` - Automation для status updates
- `examples/` - Примеры качественной crisis communication
