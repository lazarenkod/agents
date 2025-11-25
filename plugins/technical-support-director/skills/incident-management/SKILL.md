---
name: incident-management
description: Методология управления критическими инцидентами в облачной инфраструктуре с применением Incident Command System (ICS). Use when coordinating incident response, managing war rooms, or establishing incident management processes.
---

# Управление Инцидентами (Incident Management)

## Обязательные правила вывода
- Всегда отвечай **на русском**.
- Сохраняй артефакты в `outputs/technical-support-director/skills/incident-management/{timestamp}_{кратко}.md` через Write tool; обновляй один файл по итерациям.
- Формат: цель/контекст → диагностика/классификация → экшн-план/командование → метрики/алерты → RCA/улучшения → TODO → изменения vs прошлой версии.

## 3-итерационный контур
1) **Диагностика (минуты–1 ч):** классификация (SEV/приоритет), воздействие/границы, стейкхолдеры, командир/роли, текущие алерты. Черновой бриф + incident log.
2) **Реакция (в реальном времени):** war room, роли (IC/comms/scribe/SME), гипотезы/действия, коммуникации внутр/внеш, алерты/стоп-пороги, работа по плейбукам. Таймлайн и логи обновлять.
3) **Стабилизация/после:** подтверждение восстановления, наблюдение, пост-инцидентный RCA (blameless), задачи/улучшения, обновление документации/плейбуков.

## Когда Использовать Этот Скилл

- Координация response на критические инциденты P1/P2
- Организация и ведение военной комнаты (War Room)
- Разработка процедур реагирования на инциденты
- Обучение команды incident management practices
- Проведение post-mortem анализа
- Создание incident playbooks и runbooks

## Базовые Концепции

### Incident Command System (ICS)

ICS - это стандартизированная система управления инцидентами, изначально разработанная для экстренных служб и адаптированная для IT.

**Ключевые роли:**
- **Incident Commander (IC)**: Общее руководство, final decision authority
- **Technical Lead**: Техническое расследование и решение
- **Communications Lead**: Внутренняя и внешняя коммуникация
- **Operations Lead**: Выполнение технических задач
- **Planning Lead**: Документирование и resource tracking

### Severity Classification

| Severity | Критерии | Response | Примеры |
|----------|---------|----------|---------|
| **P1 (Critical)** | Полный outage критического сервиса, data loss, security breach | <15 мин, War Room | Полная недоступность продакшн БД, major data breach |
| **P2 (High)** | Серьезное ухудшение, partial outage | <30 мин | Значительная деградация performance, intermittent failures |
| **P3 (Medium)** | Minor issues, workaround available | <2 ч | Non-critical feature broken, single customer affected |
| **P4 (Low)** | Косметические issues | <8 ч | UI glitches, документация неточная |

### War Room Management

**Setup Checklist:**
```markdown
## War Room Активация

### Коммуникация
- [ ] Создан Slack/Teams channel: #incident-[ID]
- [ ] Video conference bridge активен
- [ ] Backup phone bridge готов
- [ ] Status page dashboard готов

### Роли Назначены
- [ ] Incident Commander: [Имя]
- [ ] Technical Lead: [Имя]
- [ ] Communications Lead: [Имя]
- [ ] Customer Liaison: [Имя]
- [ ] Scribe (документирование): [Имя]

### Инструменты
- [ ] Live incident doc (Google Doc/Confluence)
- [ ] Monitoring dashboards открыты
- [ ] Log aggregation доступен
- [ ] Deployment tools ready

### Stakeholders Уведомлены
- [ ] Executive team
- [ ] Account managers (affected customers)
- [ ] Customer support team
```

## Incident Response Workflow

### Phase 1: Detection & Triage (0-15 min)

**Действия:**
1. **Verify the incident**: Подтверди реальность проблемы
   ```bash
   # Проверь monitoring alerts
   # Проверь metrics dashboards
   # Воспроизведи issue если возможно
   ```

2. **Assess severity**: Определи P1/P2/P3/P4
   - User impact (количество и тип пользователей)
   - Business impact (revenue, reputation)
   - Data integrity risk
   - Security implications

3. **Alert stakeholders**: Уведоми нужных людей
   - P1: Немедленно activate war room
   - P2: Notify team lead, prepare for war room
   - P3: Assign to engineer, notify team lead
   - P4: Standard ticket workflow

### Phase 2: Investigation & Diagnosis (15-60 min)

**Systematic Approach:**
```markdown
1. **Establish Timeline**
   - Когда началось?
   - Что изменилось? (deployments, config, infrastructure)

2. **Check Recent Changes**
   - git log --since="2 hours ago"
   - Deployment history
   - Configuration changes
   - Infrastructure modifications

3. **Review Monitoring Data**
   - Application metrics (error rate, latency)
   - Infrastructure metrics (CPU, memory, disk, network)
   - Logs (errors, warnings, patterns)
   - Distributed traces

4. **Form Hypotheses**
   - List potential root causes
   - Prioritize by likelihood and impact
   - Test hypotheses systematically

5. **Narrow Down Root Cause**
   - Eliminate hypotheses through testing
   - Gather additional evidence
   - Involve subject matter experts
```

### Phase 3: Mitigation & Resolution (Variable)

**Decision Framework: Fix Forward vs Rollback**

```python
def should_rollback():
    """
    Решение о rollback vs fix forward
    """
    # Rollback if:
    if incident.caused_by_recent_deployment:
        if incident.severity == "P1":
            return True  # Always rollback P1 from bad deployment

    if estimated_fix_time > estimated_rollback_time * 2:
        return True  # Rollback быстрее

    if data_integrity_at_risk:
        return True  # Безопасность данных критична

    # Fix forward if:
    if rollback_will_cause_data_loss:
        return False  # Нельзя откатывать

    if root_cause_well_understood and fix_simple:
        return False  # Быстрый fix предпочтительнее

    # Default: Prefer rollback for safety
    return True
```

**Staged Rollout Pattern:**
```markdown
1. **Canary** (1-5% traffic): Verify fix works
2. **Small** (10% traffic): Monitor for 10-15 min
3. **Medium** (25% traffic): Monitor for 10 min
4. **Large** (50% traffic): Monitor for 10 min
5. **Full** (100% traffic): Complete rollout
```

### Phase 4: Communication (Continuous)

**Update Frequency:**
- **P1**: Every 15-30 minutes
- **P2**: Every 30-60 minutes
- **P3**: Every 2-4 hours
- **P4**: Daily or as significant progress made

**Communication Template:**
```markdown
## Incident Update #[N] - [HH:MM UTC]

**Status**: [INVESTIGATING | IDENTIFIED | MITIGATING | RESOLVED | MONITORING]

**Summary**: [One-line summary of current state]

**Since Last Update**:
- [Action 1 completed]
- [Discovery made]
- [Next step initiated]

**Current Understanding**:
- **Root Cause**: [Known | Suspected | Under investigation]
- **Impact**: [Scope of affected users/services]
- **ETA**: [If determinable]

**Next Steps**:
1. [Specific action with owner]
2. [Expected completion time]

**Next Update**: [Specific time]
```

### Phase 5: Verification & Monitoring (30-120 min)

**Verification Checklist:**
```markdown
- [ ] Error rate returned to baseline
- [ ] Latency metrics normal
- [ ] User reports stopped
- [ ] Synthetic monitors passing
- [ ] No error logs
- [ ] Customer verification (if applicable)
- [ ] 30+ minutes stable operation
```

## Post-Incident Activities

### Post-Mortem Structure

```markdown
# Post-Mortem: [Incident Title]

**Дата**: YYYY-MM-DD
**Длительность**: [Start] - [End] ([X hours Y minutes])
**Severity**: P1/P2/P3
**Участники**: [Names]

## Executive Summary
[2-3 предложения: что случилось, impact, resolution]

## Impact
- **Users Affected**: [Number/percentage]
- **Services Affected**: [List]
- **Revenue Impact**: [$Amount or N/A]
- **Downtime**: [Duration]

## Timeline (UTC)
| Time | Event |
|------|-------|
| 14:35 | 🔴 Incident started |
| 14:38 | 🔔 Alert triggered |
| 14:40 | 👥 War room assembled |
| 14:50 | 🔍 Root cause identified |
| 15:05 | 🔧 Fix deployed |
| 15:20 | ✅ Resolution verified |

## Root Cause
[Детальное объяснение технической причины]

## Resolution
[Что было сделано для решения]

## What Went Well ✅
- [Item 1]
- [Item 2]

## What Could Be Improved ❌
- [Item 1]
- [Item 2]

## Action Items
| Action | Owner | Due Date | Priority | Status |
|--------|-------|----------|----------|--------|
| [Preventive action] | [@person] | YYYY-MM-DD | P0 | Open |

## Lessons Learned
[Key takeaways для будущего]
```

### 5 Whys Analysis

```markdown
**Проблема**: Production database unavailable

**Why #1**: Почему database unavailable?
→ Connection pool exhausted

**Why #2**: Почему connection pool exhausted?
→ Внезапный spike в traffic (3x normal)

**Why #3**: Почему spike вызвал exhaustion?
→ Connection pool не масштабировался автоматически

**Why #4**: Почему нет автоматического масштабирования?
→ Не было implemented в initial design

**Why #5**: Почему не было в design?
→ Load testing не покрывал 3x traffic scenarios

**Root Cause**: Insufficient capacity planning и load testing

**Prevention**:
- Implement auto-scaling connection pool
- Expand load testing scenarios
- Add connection pool monitoring с alerts
```

## Incident Playbooks

### Database Outage Playbook

```markdown
# Playbook: Database Outage

## Initial Response (0-5 min)
1. Verify outage: Check monitoring, attempt connection
2. Check database server status (cloud console)
3. Review recent changes (last 2 hours)
4. Declare P1, activate war room

## Diagnosis (5-15 min)
```bash
# Check database health
aws rds describe-db-instances --db-instance-identifier prod-db

# Check metrics
# - CPU utilization
# - Free storage space
# - Database connections
# - Read/write IOPS

# Check logs
aws logs tail /aws/rds/instance/prod-db/postgresql --follow

# Common issues:
# - Storage full
# - Connection limit reached
# - Instance stopped/terminated
# - Network/security group blocking
```

## Mitigation
- **If storage full**: Extend storage, purge old logs
- **If connections exhausted**: Kill idle connections, restart app servers
- **If stopped**: Start instance
- **If security group**: Fix security group rules

## Escalation
- If unresolvable in 15 min → Escalate to vendor (AWS/Azure)
```

## References

См. дополнительные материалы в директории `references/`:
- `incident-playbook-templates.md` - Шаблоны playbooks
- `war-room-best-practices.md` - Best practices для War Room
- `post-mortem-examples.md` - Примеры качественных post-mortems
