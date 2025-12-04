---
name: root-cause-analysis
description: Проведение Root Cause Analysis (RCA) для аппаратных инцидентов с использованием структурированной методологии.
---

# Root Cause Analysis (RCA) аппаратных инцидентов

Эта команда проводит систематический RCA анализ аппаратного инцидента используя проверенные методологии (5 Whys, Fishbone Diagram, Timeline Analysis).

## Использование

```bash
/root-cause-analysis [incident-id или описание проблемы]
```

## Процесс RCA

### Шаг 1: Сбор информации об инциденте

Соберу следующую информацию:

**Обязательные данные:**
1. **Описание проблемы**
   - Что произошло? (симптомы)
   - Когда произошло? (timestamp, продолжительность)
   - Где произошло? (affected systems)
   - Кто обнаружил? (alerting или user report)
   - Impact? (users affected, services down)

2. **Timeline событий**
   - Первое обнаружение
   - Ключевые события
   - Действия response team
   - Восстановление service

3. **System context**
   - Конфигурация affected systems
   - Recent changes (последние 7 дней)
   - Workload characteristics
   - Environmental conditions

4. **Logs и метрики**
   - System event logs (BMC SEL, OS logs)
   - Performance metrics before/during/after
   - Alerting history
   - Related incidents

### Шаг 2: Timeline Analysis

Построю детальный timeline:

```markdown
## Timeline инцидента

| Время | Событие | Источник | Категория |
|-------|---------|----------|-----------|
| T-2h | Correctable memory errors начали расти (DIMM A1) | EDAC logs | Warning |
| T-30m | Memory error rate превысил 10/час | Monitoring alert | Warning |
| T-5m | Uncorrectable memory error | BMC SEL | Critical |
| T-0 | Kernel panic, server crash | Console logs | Outage |
| T+2m | Automatic reboot попытка (failed) | BMC | Recovery |
| T+5m | Manual power cycle by ops team | Ticketing system | Recovery |
| T+7m | Server boot успешен, DIMM A1 disabled by BIOS | POST logs | Recovery |
| T+10m | Services restored, operating на reduced memory | Monitoring | Recovered |
```

**Correlation:** CE errors были leading indicator за 2 hours до critical failure.

### Шаг 3: 5 Whys Analysis

Применю метод 5 Whys:

```markdown
## 5 Whys Analysis

**Проблема:** Production сервер неожиданно crashed с kernel panic

1. Почему сервер crashed?
   → Kernel panic вызван uncorrectable memory error (UE)

2. Почему возник uncorrectable memory error?
   → DIMM модуль в слоте A1 failed (multi-bit error не исправлен ECC)

3. Почему DIMM failed?
   → Модуль достиг end of life, показывал растущие correctable errors 2 недели

4. Почему модуль не был заменен проактивно?
   → Мониторинг ECC errors не был настроен, warnings пропущены

5. Почему мониторинг не был настроен?
   → Отсутствовала standard operating procedure для setup мониторинга при commissioning новых servers

**ROOT CAUSE:** Отсутствие SOP для настройки hardware health monitoring при вводе серверов в эксплуатацию
```

### Шаг 4: Fishbone Diagram

Построю Fishbone (Ishikawa) diagram:

```markdown
## Fishbone Analysis

                        [Server Crash / Outage]
                                 ◆
                                 │
      ┌──────────────────────────┼──────────────────────────┐
      │                          │                          │
   Equipment                 Process                    People
      │                          │                          │
  ├─ DIMM failure          ├─ No ECC monitoring      ├─ Ops не знали
  │   - 2 years old        │   setup в SOP           │   о risks
  │   - High utilization   │                         │
  │   - Thermal stress?    ├─ No proactive          ├─ Limited training
  │                        │   maintenance           │   на hardware health
  ├─ No spare inventory    │   schedule              │
  │   (delayed replacement)│                         ├─ Reactive только
      │                    ├─ No trending analysis   │   approach
      │                    │   (missed pattern)      │
      └────────────────────┴──────────────────────────┘

**Contributing Factors:**
1. Equipment: Aging hardware past typical refresh (contributing)
2. Process: Lack of monitoring setup procedure (root cause)
3. Process: No preventive maintenance (contributing)
4. People: Training gaps (contributing)
```

### Шаг 5: Fault Tree Analysis

Создам логическое дерево:

```markdown
## Fault Tree

                    [Production Outage]
                            │
                     ┌──────┴──────┐
                     │     AND     │
                     │             │
              [Hardware Failure] [No Redundancy]
                     │                   │
              ┌──────┴──────┐           │
              │     OR      │      [Single Server]
              │             │      [Critical Service]
         [DIMM Fail]   [Other HW]
              │
         ┌────┴────┐
         │   AND   │
         │         │
    [DIMM EOL] [No Detection]
         │             │
     [Age 2y+]    [No Monitoring]
     [High Load]       │
                  [No SOP]

**Analysis:**
- Hardware failure (DIMM) был inevitable (age + load)
- BUT: Outage был preventable если:
  1. Monitoring обнаружил degradation рано → Proactive replacement
  2. OR: Redundancy (clustered service) → No single point failure

**Primary Failure:** Lack of monitoring (preventable)
**Secondary Failure:** Architecture single point failure (design issue)
```

### Шаг 6: Corrective Actions

Разработаю action plan:

## Формат RCA Report

```markdown
# Root Cause Analysis Report

**Incident ID:** [INC-2024-1234]
**Date:** [2024-12-04]
**Analyst:** datacenter-hardware-architect
**Reviewed by:** [Team Lead]

## Executive Summary

**Incident:** Production database server (db-prod-01) crashed вызвав 45-minute outage critical service.

**Impact:**
- Downtime: 45 minutes
- Users affected: ~5,000
- Revenue impact: Estimated $50,000
- Data loss: None (last transaction committed 2 min before crash)

**Root Cause:** Memory module failure (DIMM A1) не обнаружен проактивно из-за отсутствия ECC error monitoring.

**Status:** Resolved, server operating normally на reduced memory (480GB вместо 512GB).

## Incident Timeline

[Detailed timeline таблица из Шага 2]

## Problem Statement

**What happened:**
Production database server db-prod-01 crashed unexpectedly at 14:23 UTC 2024-12-01, resulting в kernel panic и automatic reboot failure. Service восстановлен в 15:08 UTC после manual intervention.

**Expected behavior:**
- ECC memory должна correcting single-bit errors
- Monitoring должен alerting на degrading components
- Proactive replacement должен occur before failure

**Actual behavior:**
- Uncorrectable multi-bit error → kernel panic
- No prior alerting (monitoring не настроен)
- Reactive response (45 min downtime)

## Analysis

### Root Cause Analysis (5 Whys)
[Из Шага 3]

### Contributing Factors (Fishbone)
[Diagram и analysis из Шага 4]

### Fault Tree Analysis
[Логическое дерево из Шага 5]

## Root Cause

**Primary Root Cause:**
Отсутствие standard operating procedure для настройки hardware health monitoring (specifically ECC error monitoring) при commissioning новых servers.

**Why this is root cause:**
- Directly led to: Missed early warning signs (CE errors 2 weeks prior)
- Under our control: We can implement SOP
- Actionable: Clear procedure can be defined и enforced
- Prevents recurrence: With monitoring, future DIMM degradation будет detected early

**Contributing Factors:**
1. Aging hardware (2 years, approaching refresh cycle)
2. No preventive maintenance schedule для memory health checks
3. Lack of spare parts inventory (delayed replacement)
4. Single server architecture для critical service (no redundancy)
5. Team training gap (hardware failure patterns не хорошо understood)

## Immediate Actions Taken

1. **[T+5m] Server power cycled**
   - Action: Manual power cycle после failed auto-reboot
   - Result: Successful boot, BIOS automatically disabled failed DIMM

2. **[T+10m] Services restored**
   - Действие: Database started, connections restored
   - Result: Service operational на 480GB memory (vs 512GB)

3. **[T+2h] DIMM заказан**
   - Действие: Replacement DIMM ordered (32GB DDR4 RDIMM)
   - ETA: 2 business days

4. **[T+4h] Monitoring enabled**
   - Действие: Настроен EDAC monitoring на all production servers
   - Result: ECC errors теперь alerting via Zabbix

5. **[T+24h] Inventory check**
   - Действие: Audit hardware spares inventory
   - Result: Insufficient memory spares (now ordering safety stock)

## Corrective Actions

### Immediate (0-7 days) - PREVENT RECURRENCE

**Action 1: Deploy ECC Monitoring (ALL servers)**
- **Owner:** Infrastructure Team
- **Priority:** Critical
- **Deadline:** 2024-12-06 (2 days)
- **Steps:**
  1. Deploy edac-util monitoring на all Linux servers
  2. Configure Windows servers (WMI queries для memory errors)
  3. Setup alerting thresholds:
     - Warning: >1 CE/hour per DIMM
     - Critical: >10 CE/hour или ANY UE
  4. Create dashboard (Grafana) для ECC error trending
- **Success Criteria:** All production servers reporting ECC metrics

**Action 2: Immediate Hardware Audit**
- **Owner:** Hardware Team
- **Priority:** High
- **Deadline:** 2024-12-07 (3 days)
- **Steps:**
  1. Check BMC SEL logs на all servers (last 30 days)
  2. Identify any servers с CE errors
  3. Proactive replacement if CE trend detected
  4. Generate report of findings
- **Success Criteria:** No production servers с degrading memory

**Action 3: Spares Inventory**
- **Owner:** Procurement
- **Priority:** High
- **Deadline:** 2024-12-11 (1 week)
- **Steps:**
  1. Define minimum spare levels:
     - Memory: 10% of total DIMM count
     - Disks: 15% of total disk count
     - PSUs: 5% of total PSU count
  2. Order to reach minimum levels
  3. Implement reorder process (auto-order при usage)
- **Success Criteria:** Spare inventory встречает minimums

### Short-term (1-4 weeks) - PROCESS IMPROVEMENTS

**Action 4: Server Commissioning SOP**
- **Owner:** Architecture Team
- **Priority:** High
- **Deadline:** 2024-12-18 (2 weeks)
- **Steps:**
  1. Document standard monitoring setup:
     - Hardware health (temps, fans, PSUs)
     - ECC memory errors
     - SMART disk monitoring
     - Network interface errors
  2. Create commissioning checklist
  3. Train ops team на new SOP
  4. Require sign-off before production deployment
- **Success Criteria:** SOP published, team trained, enforced на new servers

**Action 5: Preventive Maintenance Schedule**
- **Owner:** Operations Team
- **Priority:** Medium
- **Deadline:** 2024-12-25 (3 weeks)
- **Steps:**
  1. Define PM tasks:
     - Weekly: ECC error review (automated)
     - Monthly: SMART data review, firmware check
     - Quarterly: Thermal audit, spare parts inventory
  2. Create automated reports
  3. Assign ownership (team rotation)
- **Success Criteria:** PM schedule активно running 1 month

### Long-term (1-6 months) - SYSTEMIC IMPROVEMENTS

**Action 6: Hardware Refresh Program**
- **Owner:** Architecture + Finance
- **Priority:** Medium
- **Deadline:** 2024-03-01 (3 months - planning)
- **Steps:**
  1. Audit all production hardware ages
  2. Identify servers >3 years old
  3. Budget allocation для refresh
  4. Prioritize: Critical services first
  5. Refresh schedule (rolling, minimize impact)
- **Success Criteria:** Refresh plan approved, budget allocated

**Action 7: Architectural Resilience**
- **Owner:** Architecture Team
- **Priority:** Medium
- **Deadline:** 2025-03-01 (6 months)
- **Steps:**
  1. Identify single points of failure (SPOFs)
  2. Prioritize by business impact
  3. Design redundancy solutions:
     - Database: Cluster или replication
     - Applications: Load balancing
     - Storage: RAID, replication
  4. Implementation roadmap
- **Success Criteria:** Top 10 critical services have redundancy

**Action 8: Training Program**
- **Owner:** Operations Manager
- **Priority:** Low
- **Deadline:** 2025-02-01 (2 months)
- **Steps:**
  1. Develop training materials:
     - Hardware failure patterns
     - Proactive monitoring
     - Troubleshooting methodologies (RCA)
  2. Quarterly training sessions
  3. Knowledge base (wiki) creation
- **Success Criteria:** All ops team members trained

## Lessons Learned

### What Went Well
1. ✓ Automatic BIOS disablement of failed DIMM (prevented boot loops)
2. ✓ Team response time good (5 minutes to manual intervention)
3. ✓ No data loss (database checkpointing working correctly)
4. ✓ Communication effective (stakeholders notified promptly)

### What Didn't Go Well
1. ✗ No early warning (monitoring gap)
2. ✗ 45-minute downtime (too long для critical service)
3. ✗ No spare parts (delayed permanent fix)
4. ✗ Reactive approach (should be proactive)

### Key Takeaways
1. **Monitoring is critical:** Hardware failures часто have precursors (CE errors, SMART warnings). Proactive monitoring saves downtime.

2. **Process over heroics:** Response team handled well, BUT better process (monitoring, spares) would have prevented outage entirely.

3. **Redundancy matters:** Single server для critical service = business risk. Architecture должна tolerate component failures.

4. **Documentation is key:** SOP ensures consistency, reduces human error, enables scaling team.

5. **Preventive maintenance pays off:** Small regular investments (monitoring, PM) prevent large costly outages.

## Verification

**Follow-up Actions:**
- **1 week:** Verify ECC monitoring deployed и functional
- **2 weeks:** Review SOP compliance (new servers)
- **1 month:** Check PM schedule execution
- **3 months:** Review hardware refresh planning progress
- **6 months:** Assess architectural resilience improvements

**Success Metrics:**
- Zero memory-related outages (next 6 months)
- Mean Time To Detect (MTTD) hardware degradation: <1 hour
- Mean Time To Repair (MTTR): <15 minutes (with spares)
- Compliance: 100% servers with monitoring

## Approval

**Prepared by:** datacenter-hardware-architect, [Date]
**Reviewed by:** Operations Manager, [Date]
**Approved by:** IT Director, [Date]

---

**Next Review:** [6 months from incident date]
**Distribution:** Operations Team, Management, IT Leadership
```

## Deliverables

После завершения RCA, будут созданы:

1. **RCA Report** (Markdown) - Полный отчет как выше
2. **Action Items** (CSV/Spreadsheet) - Tracking всех corrective actions
3. **Executive Summary** (1-page PDF) - Для leadership
4. **Knowledge Base Article** - Для future reference
5. **Training Material** (если applicable) - Lessons learned для team

## Требования

Для effective RCA необходимо:
- Доступ к logs (BMC SEL, OS logs, application logs)
- Historical metrics (performance data до/во время/после incident)
- Incident documentation (tickets, communication logs)
- System configuration information
- Change management records (recent changes)
