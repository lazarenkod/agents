---
name: root-cause-analysis
description: Методы и техники Root Cause Analysis (RCA) для глубокого анализа инцидентов и предотвращения повторений. Включает 5 Whys, Fishbone Diagram, Fault Tree Analysis. Use when conducting post-mortems, analyzing recurring issues, or improving system reliability.
---

# Анализ Первопричин (Root Cause Analysis)

## Обязательные правила вывода
- Всегда отвечай **на русском**.
- Сохраняй артефакты в `outputs/technical-support-director/skills/root-cause-analysis/{timestamp}_{кратко}.md` через Write tool; обновляй один файл по итерациям.
- Формат: контекст → факты/данные → причинные цепочки → выводы/корни → действия/алерты → TODO → изменения vs прошлой версии.

## 3-итерационный контур
1) **Сбор фактов (0.5–1 ч):** таймлайн, данные/логи/метрики, свидетели, без гипотез; класс проблем (процесс/люди/система/среда). Черновой бриф + risk/decision log.
2) **Анализ (1–2 ч):** 5 Whys/Fishbone/FMEA, подтверждение фактами, различие “корень vs симптом”, оценка рисков/повтора, список исправлений. Таблица причин/доказательств.
3) **Решения (0.5–1 ч):** план действий (prevention/mitigation/детекция), владельцы/сроки, алерты/пороги, обновление документации/плейбуков, контрольные точки.
## Когда Использовать

- Post-mortem анализ после инцидентов
- Расследование повторяющихся проблем
- Систематические failures
- Process improvement инициативы
- Preventive action planning

## Методологии RCA

### 1. 5 Whys Analysis

Простой но мощный метод итеративных вопросов "Почему?".

**Пример:**
```markdown
**Проблема**: Customers не могут логиниться

**Why #1**: Почему customers не могут логиниться?
→ Authentication service возвращает 500 errors

**Why #2**: Почему auth service возвращает 500 errors?
→ Database queries timing out

**Why #3**: Почему database queries timing out?
→ Database connection pool exhausted (100/100 connections used)

**Why #4**: Почему connection pool exhausted?
→ Traffic spike 3x normal load

**Why #5**: Почему 3x traffic вызвал exhaustion?
→ Connection pool не масштабируется автоматически при load spike

**Root Cause**: Отсутствие auto-scaling для database connection pool

**Preventive Actions**:
1. Implement auto-scaling connection pool (P0, 1 week)
2. Add connection pool utilization monitoring (P0, 3 days)
3. Load test 5x normal traffic scenarios (P1, 2 weeks)
4. Review all resource pools для similar issues (P1, 1 month)
```

### 2. Fishbone Diagram (Ishikawa)

Визуальный метод для категоризации potential causes.

```markdown
# Fishbone Analysis: Database Outage

## Effect: Production Database Unavailable

### People
- On-call engineer unfamiliar with DB systems
- No DBA on call during incident
- Insufficient training on failover procedures

### Process
- Manual failover process (not automated)
- No automated health checks
- Backup restore procedure not tested

### Technology
- Primary DB instance failed (hardware issue)
- Replica lag too high for failover
- Monitoring didn't detect degradation early

### Environment
- High traffic period (Black Friday)
- Recent schema migration increased load
- No load testing after migration

## True Root Causes (из анализа):
1. **Immediate**: Hardware failure (unavoidable)
2. **Contributing**: Manual failover process (slow recovery)
3. **Systemic**: Lack of automated failover и testing

## Actions:
- Implement automated failover (eliminates manual delay)
- Regular disaster recovery drills (every quarter)
- Enhanced monitoring для early detection
```

### 3. Fault Tree Analysis

Top-down deductive analysis для complex systems.

```markdown
# Fault Tree: API Complete Outage

## Top Event: API Completely Unavailable

### AND Gate: Requires ALL of:
├─ Load Balancer Failed
└─ All API Servers Down

### OR Gate: Load Balancer Fails IF ANY:
├─ Configuration Error (✓ This happened)
├─ Hardware Failure
└─ Network Issue

### OR Gate: All Servers Down IF:
├─ Deployment Killed All Instances (✓ This happened)
└─ Cascading Failure

## Chain of Events:
1. Deployment started: Rolling update initiated
2. Config error: New config had syntax error
3. Health checks failed: All new instances failing
4. Orchestrator response: Killed all old instances (before new ones healthy)
5. Result: Zero healthy instances → Complete outage

## Root Cause:
Deployment process doesn't verify minimum healthy instances before killing old ones

## Fix:
Implement blue-green deployment с health verification gate
```

## Blameless Post-Mortems

### Философия

- **Focus**: Process и system failures, NOT personal failures
- **Culture**: Learning, NOT punishment
- **Outcome**: Prevention, NOT blame

**Плохо:**
> "John deployed without testing, causing the outage."

**Хорошо:**
> "Deployment lacked automated pre-production testing gate, allowing untested code to reach production."

### Post-Mortem Template

```markdown
# Blameless Post-Mortem: [Title]

## Summary
[Neutral description of what happened]

## Impact
- Users affected: [Number]
- Duration: [Time]
- Revenue impact: [$Amount]
- Service credits: [$Amount]

## Timeline (UTC)
[Objective chronology of events]

## Root Cause
[System/process failure, not person]

## Contributing Factors
- Factor 1: [Why это contributed]
- Factor 2: [Context]

## What Went Well ✅
[Positive aspects to reinforce]

## What Could Be Better ❌
[Improvement opportunities]

## Action Items
[System improvements, not "Person should do X better"]

## Lessons Learned
[General insights applicable to other scenarios]
```

## Анализ Recurring Issues

### Pattern Detection

```python
def analyze_recurring_issues(incidents_last_90_days):
    """
    Identify patterns в incident data
    """
    patterns = {
        "by_service": group_by(incidents, "affected_service"),
        "by_time": group_by(incidents, "hour_of_day"),
        "by_root_cause": group_by(incidents, "root_cause_category"),
        "correlation": find_correlations(incidents)
    }

    insights = []

    # Service hotspots
    for service, count in patterns["by_service"]:
        if count > threshold:
            insights.append({
                "type": "hotspot",
                "service": service,
                "incident_count": count,
                "recommendation": f"Deep dive review of {service} architecture"
            })

    # Time patterns
    for hour, count in patterns["by_time"]:
        if count > threshold:
            insights.append({
                "type": "time_pattern",
                "hour": hour,
                "recommendation": f"Review batch jobs/scheduled tasks at {hour}:00"
            })

    # Root cause patterns
    for cause, count in patterns["by_root_cause"]:
        if count > 3:  # Repeated same root cause
            insights.append({
                "type": "systemic_issue",
                "root_cause": cause,
                "priority": "HIGH",
                "recommendation": "Systemic fix needed, not point solutions"
            })

    return insights
```

### Example Analysis Result

```markdown
# Recurring Issues Analysis - Q1 2024

## Patterns Detected

### Service Hotspot: Database Service
- **Incidents**: 12 in last 90 days
- **Pattern**: Connection pool exhaustion (8 incidents)
- **Root Cause**: No auto-scaling
- **Priority**: P0
- **Action**: Implement auto-scaling connection pool

### Time Pattern: Every Friday 2-3 AM UTC
- **Incidents**: 8 incidents
- **Pattern**: Database backup job causes performance degradation
- **Root Cause**: Backup during high-replica-lag period
- **Action**: Reschedule backup window, optimize backup process

### Systemic Issue: Manual Configuration Changes
- **Incidents**: 7 incidents
- **Pattern**: Configuration errors during manual changes
- **Root Cause**: No validation before applying config
- **Action**: Implement configuration-as-code с automated validation
```

## Preventive Action Framework

### Immediate (0-1 week)
- Fixes для specific issue
- Hotfixes
- Temporary mitigations

### Short-term (1-4 weeks)
- Process improvements
- Additional monitoring
- Automation quick wins

### Long-term (1-6 months)
- Architectural changes
- Systemic improvements
- Culture/training initiatives

## Metrics для RCA Effectiveness

```python
RCA_METRICS = {
    "incident_recurrence_rate": {
        "calculation": "Same root cause incidents / Total incidents",
        "target": "<5%",
        "indicates": "Effectiveness of preventive actions"
    },
    "action_item_completion": {
        "calculation": "Completed action items / Total action items",
        "target": ">90%",
        "indicates": "Follow-through on improvements"
    },
    "time_to_action": {
        "calculation": "Days from post-mortem to action item start",
        "target": "<7 days",
        "indicates": "Urgency of improvement"
    }
}
```

## References
- `examples/5-whys-examples.md` - Примеры 5 Whys analysis
- `examples/fishbone-diagrams.md` - Fishbone templates
- `templates/post-mortem-template.md` - Comprehensive template
