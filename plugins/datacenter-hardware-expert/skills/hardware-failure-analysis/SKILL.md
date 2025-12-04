---
name: hardware-failure-analysis
description: Методология анализа отказов серверного оборудования. Использовать когда требуется RCA анализ, диагностика причин отказа или разработка превентивных мер.
---

# Анализ отказов серверного оборудования

## Когда использовать этот навык

- Расследование инцидентов с аппаратными отказами
- Root Cause Analysis (RCA) для критических сбоев
- Разработка превентивных мероприятий
- Анализ трендов отказов для планирования замен
- Экспертиза по warranty claims и vendor escalation

## Базовые концепции

### Типы отказов

**Catastrophic Failure (Катастрофический отказ)**
```
Характеристики:
- Внезапный, полный отказ компонента
- Без предварительных предупреждений
- Немедленная потеря функциональности

Примеры:
- CPU die crack
- DIMM модуль полностью failed
- Disk head crash
- PSU полный отказ

Причины:
- Manufacturing defect
- Electrical overstress (EOS)
- Mechanical shock
- Lightning/surge
```

**Degradation Failure (Деградационный отказ)**
```
Характеристики:
- Постепенное ухудшение характеристик
- Предварительные warning signs
- Predictable pattern

Примеры:
- SSD wear (увеличение UBER - Uncorrectable Bit Error Rate)
- HDD increasing reallocated sectors
- Thermal paste drying (температура растет)
- Capacitor aging (voltage ripple увеличивается)

Причины:
- Normal wear and tear
- Thermal cycling
- Write endurance exhaustion
- Environmental factors
```

**Intermittent Failure (Прерывистый отказ)**
```
Характеристики:
- Проблема появляется и исчезает
- Сложно воспроизвести
- Environment-dependent (температура, влажность, вибрация)

Примеры:
- Cold boot problems (исчезают после прогрева)
- Thermal-induced errors (только при высокой нагрузке)
- Connector intermittent (oxidation, loose connection)
- Memory errors под определенной нагрузкой

Причины:
- Thermal expansion/contraction
- Marginal component (near failure threshold)
- Environmental sensitivity
- Poor connections
```

### Bathtub Curve (Кривая ванны)

```
Частота отказов
     ^
     |  Ранние  |  Нормальная  |  Износ
     |  отказы  |  эксплуатация| (Wear-out)
     |          |              |
High |●●●       |              |       ●●●
     |  ●●●     |              |     ●●
     |    ●●●   |              |   ●●
     |      ●●● |              | ●●
Low  |         ●●●●●●●●●●●●●●●●●
     |________________________________> Время
        0-1 год   1-5 лет    5+ лет

Infant Mortality (0-1 год):
- Manufacturing defects
- Component screening failures
- Installation errors
- Burn-in testing catches большинство

Normal Life (1-5 лет):
- Random failures
- Константная низкая частота
- External factors (power events, environmental)
- Правильная эксплуатация минимизирует

Wear-out Period (5+ лет):
- End of design life
- Material fatigue
- Electrolytic capacitor degradation
- Mechanical wear
- Proactive replacement необходима
```

### MTBF и AFR

**MTBF (Mean Time Between Failures)**
```
Определение:
- Среднее время между отказами
- Используется для non-repairable или repairable systems
- Measured в часах

Расчет:
MTBF = Total Operating Hours / Number of Failures

Пример:
- 100 серверов × 8760 часов/год = 876,000 часов
- 5 failures за год
- MTBF = 876,000 / 5 = 175,200 часов (~20 лет)

Важно:
- MTBF не означает "продлится X часов"
- Это статистическое среднее для популяции
- Не предсказывает индивидуальный отказ
```

**AFR (Annualized Failure Rate)**
```
Определение:
- Процент устройств, которые откажут за год
- Более интуитивная метрика чем MTBF

Расчет:
AFR = (8760 / MTBF) × 100%

Примеры:
MTBF          AFR
1,000,000 ч → 0.88%  (1 из 114 дисков/год)
500,000 ч   → 1.75%  (1 из 57)
200,000 ч   → 4.38%  (1 из 23)

Реальность:
- Vendor specs: AFR 0.5-1%
- Реальные данные (Google, Backblaze): AFR 2-8%
- Зависит от workload, environment, model
```

## Методология RCA (Root Cause Analysis)

### 5 Whys Method

**Процесс**
```
1. Определите проблему
2. Спросите "Почему это произошло?"
3. Определите причину
4. Спросите "Почему эта причина возникла?"
5. Повторите 5 раз (или до root cause)

Критерии root cause:
- Устранение причины предотвратит повторение
- Находится в зоне нашего контроля
- Actionable (можно принять меры)
```

**Пример: Сервер перезагрузился**
```
Проблема: Production сервер неожиданно перезагрузился

1. Почему сервер перезагрузился?
   → Kernel panic из-за uncorrectable memory error

2. Почему возникла uncorrectable memory error?
   → DIMM модуль в слоте A1 выдал multi-bit error

3. Почему DIMM выдал multi-bit error?
   → Модуль достиг конца срока службы (MTBF), показывает
     растущее количество correctable errors за последние 3 месяца

4. Почему модуль не был заменен проактивно?
   → Система мониторинга ECC errors не была настроена

5. Почему мониторинг не был настроен?
   → Отсутствовала процедура при commissioning новых серверов

ROOT CAUSE: Отсутствие стандартной процедуры настройки
мониторинга при вводе серверов в эксплуатацию

Corrective Actions:
- Immediate: Замена DIMM в A1
- Short-term: Audit всех серверов на ECC error monitoring
- Long-term: Процедура commissioning с чек-листом,
  включающим setup мониторинга всех hardware health metrics
```

### Fishbone Diagram (Ishikawa)

**Структура**
```
                          Problem
                             ◆
                             │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    Categories         Categories         Categories

Основные категории (6M):
- Man (People): Человеческий фактор
- Machine (Equipment): Оборудование
- Method (Process): Процессы
- Material: Материалы/Компоненты
- Measurement: Мониторинг/Метрики
- Mother Nature (Environment): Окружающая среда
```

**Пример: High disk failure rate**
```
                    High Disk Failure Rate
                            ◆
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
   Equipment            Environment          Process
       │                    │                    │
   ├─ Old drives       ├─ High temp         ├─ No burn-in
   │   (5+ years)      │   (>30°C)          │   testing
   │                   │                    │
   ├─ Single vendor    ├─ Vibration        ├─ No predictive
   │   (model defect)  │   from adjacent    │   monitoring
   │                   │   equipment        │
   ├─ Firmware bugs    │                    ├─ Reactive only
       (known issue)   ├─ Humidity          │   replacement
                       │   fluctuation      │
                       │                    └─ No spare pool
                       └─ Poor airflow
                           management

Analysis:
Primary contributors:
1. Environment: Temperature >30°C (должно быть <25°C)
2. Equipment: Drives 6+ лет (past design life)
3. Process: No predictive monitoring (SMART alerts)

Root Cause: Lack of proactive thermal management +
aging equipment beyond refresh cycle
```

### Fault Tree Analysis

**Принцип**
```
Top Event (проблема)
  └─ OR/AND gates
      └─ Contributing events
          └─ Basic events (leaf nodes)

Логические операторы:
- OR gate: Любое событие вызывает проблему
- AND gate: Все события должны произойти одновременно
```

**Пример: Server Unresponsive**
```
           [Server Unresponsive]
                    │
           ┌────────┴────────┐
           │      OR         │
           │                 │
    [Hardware Failure]  [Software Hang]
           │
    ┌──────┴──────┐
    │     OR      │
    │             │
[CPU Fail]   [Memory Fail]
    │             │
    │        ┌────┴────┐
    │        │   AND   │
    │        │         │
    │   [UE Error] [No Spare DIMM]
    │
┌───┴───┐
│  OR   │
│       │
[MCE] [Thermal]

Probability Analysis:
- P(MCE) = 0.001 (0.1%)
- P(Thermal) = 0.002 (0.2%)
- P(CPU Fail) = P(MCE) + P(Thermal) = 0.003

- P(UE) = 0.01 (1%)
- P(No Spare) = 0.5 (50% память без sparing enabled)
- P(Memory Fail) = P(UE) × P(No Spare) = 0.005

- P(Hardware Failure) = P(CPU) + P(Memory) = 0.008 (0.8%)
```

## Диагностические паттерны

### Pattern 1: Sudden множественные отказы

**Признаки**
```
- Несколько серверов/компонентов отказали одновременно
- Одинаковая временная метка (в пределах минут)
- Географически близкое расположение (одна стойка, PDU, зона)
```

**Вероятные причины**
```
1. Power event:
   - Utility power outage/brownout
   - UPS failure или bypass
   - PDU overload trip
   - Generator switchover issue

2. Environmental:
   - CRAC/CRAH failure → thermal shutdown
   - Water leak → equipment damage
   - Fire suppression accidental discharge

3. Network event:
   - Switch failure → lost management connectivity
   - Network broadcast storm → CPU saturation

Диагностика:
- IPMI/BMC SEL logs: Корреляция timestamps
- UPS/PDU logs: Power anomalies
- Thermal sensors: Temperature spikes
- Network logs: Link down events, broadcast counters
```

**Пример расследования**
```
Incident: 15 серверов в одной стойке rebooted в 14:23-14:24

Timeline:
14:22:45 - PDU power spike event logged
14:23:00 - Servers begin rebooting (BMC logs)
14:23:15 - All servers down
14:25:00 - Servers come back online

Investigation:
1. Check PDU logs:
   → Spike to 95% capacity at 14:22:45
   → No trip, но voltage sag logged

2. Check UPS:
   → Transfer to battery at 14:22:45 for 200ms
   → Utility voltage dip: 208V → 180V → 208V

3. Check utility:
   → Maintenance notification: Switchgear work at 14:20
   → Не было coordination с datacenter team

Root Cause: Utility maintenance caused voltage sag,
UPS transferred briefly, insufficient for dirty shutdown,
servers experienced power glitch and rebooted

Corrective Actions:
- Immediate: Coordinate с utility на future maintenance
- Short-term: Review UPS transfer threshold settings
- Long-term: Implement holdup time testing для servers,
  ensure >20ms to avoid brief power anomaly reboots
```

### Pattern 2: Cascading failures

**Признаки**
```
- Отказы происходят последовательно
- Каждый отказ увеличивает нагрузку на оставшиеся компоненты
- Accelerating failure rate (сначала 1, потом 2, потом 4...)
```

**Вероятные причины**
```
1. Capacity exhaustion:
   - Single component fails → load redistributes →
     → remaining overload → more failures

2. Thermal cascade:
   - Cooling unit fails → temperature rises →
     → server throttles/shuts down → less heat load →
     → temperature stabilizes BUT reduced capacity →
     → work moves to другим servers → они overload

3. Power cascade:
   - PSU fails в multi-PSU system →
     → remaining PSU takes full load →
     → operates at higher temp/stress →
     → higher failure probability

Диагностика:
- Timeline analysis: Интервалы между failures
- Load correlation: Нагрузка на компоненты перед failure
- Thermal correlation: Temperature trends
- Redundancy state: Was system already degraded (N+1 → N)?
```

**Пример расследования**
```
Incident: 6 PSU failures за 48 часов в одном cluster

Timeline:
Day 1, 10:00 - PSU #1 fails (server A)
Day 1, 18:00 - PSU #2 fails (server C)
Day 2, 02:00 - PSU #3 fails (server E)
Day 2, 08:00 - PSU #4 fails (server G)
Day 2, 12:00 - PSU #5 fails (server B)
Day 2, 14:00 - PSU #6 fails (server D)

Observation: Accelerating failures, все dual-PSU servers

Investigation:
1. PSU analysis:
   - All failed PSUs: 5+ лет старые, same vendor/model
   - Capacitor bulging observed (electrolytic aging)

2. Environmental:
   - Inlet temperature: 28°C (высоковато, норма <25°C)
   - CRAC unit #2 was offline для maintenance (N+1 → N)

3. Load analysis:
   - Cluster workload increased 40% (migration from другого DC)
   - Servers running higher average CPU → higher power draw

4. Cascade mechanism:
   - PSU #1 fails → Server A loses redundancy
   - Higher ambient temp + higher load →
     → remaining aging PSUs operating near thermal limits
   - Each failure increases stress на оставшиеся
     (workload rebalancing)

Root Cause:
- Primary: Aging PSUs past design life (5+ years)
- Contributing: Elevated temperature (CRAC maintenance)
- Contributing: Increased load (workload migration)
- Trigger: PSU #1 failure started cascade

Corrective Actions:
- Emergency: Replace all PSUs в affected cluster (>5 years)
- Immediate: Restore CRAC N+1 redundancy
- Short-term: Thermal audit и temperature setpoint review
- Long-term: Proactive PSU replacement program (4-year cycle)
- Long-term: Capacity planning с headroom для migrations
```

### Pattern 3: Periodic failures

**Признаки**
```
- Отказы происходят с регулярностью (ежедневно, еженедельно)
- Specific time of day или условия
- Predictable pattern
```

**Вероятные причины**
```
1. Scheduled events:
   - Backup windows → load spike → thermal/power stress
   - Batch jobs → memory pressure → OOM kills
   - Maintenance windows → human error

2. Environmental cycles:
   - Diurnal temperature swing → thermal stress cycles
   - Business hours load → higher utilization periods
   - HVAC scheduling → temperature variations

3. Software issues:
   - Memory leak → накопление до OOM (периодический restart)
   - Log file growth → disk full (ежедневно)
   - Certificate expiration → weekly monitoring miss

Диагностика:
- Temporal analysis: Точное время failures, correlation
- Scheduled tasks: Cron jobs, scheduled maintenance
- Environmental data: Temperature, power load cycles
- Application metrics: Memory usage trends, disk I/O patterns
```

**Пример расследования**
```
Incident: Storage array failover каждый вторник в 02:00-03:00

Timeline:
Week 1, Tuesday 02:23 - Controller failover, 15min outage
Week 2, Tuesday 02:45 - Controller failover, 12min outage
Week 3, Tuesday 02:18 - Controller failover, 18min outage
Week 4, Tuesday 02:31 - Controller failover, 14min outage

Investigation:
1. Storage logs:
   - Controller panic due to "watchdog timeout"
   - Active I/O at time: >100,000 IOPS (normal: 20,000)

2. Scheduled tasks:
   - Full database backup starts: Tuesday 02:00
   - Backup method: Storage snapshot + copy

3. Snapshot analysis:
   - Snapshot creation time: 2-3 minutes
   - During snapshot: Array под heavy metadata I/O
   - Observed: Latency spike 50ms → 500ms

4. Controller behavior:
   - Watchdog timer: 30 seconds for heartbeat
   - Under load: Controller CPU 98%, watchdog miss
   - Failover triggered for "unresponsive controller"

Root Cause:
- Backup snapshot operation creates heavy metadata workload
- Coincides с production OLTP load tail (batch jobs finishing)
- Combined load overwhelms controller CPU
- Watchdog timeout triggers unnecessary failover

Corrective Actions:
- Immediate: Change backup schedule to 04:00 (lower load)
- Short-term: Optimize snapshot settings (smaller chunks)
- Long-term: Storage capacity planning (add controller/cache)
- Long-term: Workload analysis и scheduling optimization
```

## Превентивные стратегии

### Predictive Monitoring

**SMART Monitoring (Storage)**
```
Критические атрибуты:
ID  Attribute Name             Threshold  Action
5   Reallocated_Sector_Ct      >10        Replace soon
187 Reported_Uncorrect         >0         Monitor closely
188 Command_Timeout            >100       Cable/controller check
197 Current_Pending_Sector     >5         Replace soon
198 Offline_Uncorrectable      >0         Replace immediately
199 UDMA_CRC_Error_Count       >50        Cable replacement

Monitoring strategy:
- Daily SMART checks (automated)
- Trend analysis (increasing errors over 30 days)
- Threshold alerts (immediate notification)
- Quarterly reports (для планирования replacements)
```

**ECC Memory Monitoring**
```
Correctable Error thresholds:
Rate                 Action
>1 per hour         Warning - monitor daily
>10 per hour        Critical - replace within 7 days
>100 per hour       Emergency - replace immediately

Uncorrectable Errors:
ANY UE              Replace DIMM immediately
                    RCA для determining if more widespread issue

Monitoring tools:
- edac-util (Linux)
- IPMI SEL monitoring
- Vendor tools (iDRAC, iLO)
- Centralized logging (Splunk, ELK)
```

**Temperature Monitoring**
```
Component     Normal    Warning   Critical  Action
CPU           <75°C     75-85°C   >85°C     Throttling/shutdown
Memory        <75°C     75-85°C   >85°C     Errors increase
HDD           <40°C     40-50°C   >50°C     Wear acceleration
SSD           <60°C     60-70°C   >70°C     Throttling/wear
Ambient       <25°C     25-30°C   >30°C     Cooling issue

Proactive measures:
- Continuous monitoring с 5-minute granularity
- Trend analysis (30-day averages)
- Thermal mapping (quarterly)
- Hot spot identification и remediation
```

### Refresh Cycles

**Lifecycle Planning**
```
Component       Design Life    Proactive Refresh
Servers         5 years        4 years
Switches        7 years        5 years
Storage         5 years        4 years (disks earlier)
UPS Batteries   5 years        3-4 years
PSU             5-7 years      Not replaced (server refresh)
Fans            5+ years       On failure (rapid replacement)

Factors для adjustment:
- Workload intensity (accelerate для high utilization)
- Environment (harsh conditions → shorter cycle)
- Vendor reliability data
- TCO analysis (repair costs vs refresh costs)
```

**Burn-in Testing**
```
Process:
1. New equipment arrival
2. Burn-in period: 48-72 hours под full load
3. Comprehensive testing:
   - CPU: stress-ng, Prime95
   - Memory: memtest86+ (full pass)
   - Disk: fio (random write test)
   - Network: iperf3 (bandwidth saturation)
4. Monitoring: Zero errors required для pass
5. Failed units: RMA immediately

Benefits:
- Catches infant mortality defects
- Validates vendor QA
- Reduces production failures
- Documents baseline performance
```

## Vendor Engagement

### Warranty Claims

**Documentation Requirements**
```
Essential Data:
1. System Information:
   - Model, serial number
   - Configuration (CPU, RAM, storage)
   - Firmware/BIOS versions

2. Failure Evidence:
   - Error logs (IPMI SEL, system logs)
   - SMART data (для disk failures)
   - Photos (physical damage)
   - Timeline (when first observed)

3. Troubleshooting Performed:
   - Steps taken
   - Results observed
   - Isolation testing (swapped components)

4. Business Impact:
   - Severity (production down vs degraded)
   - Users affected
   - Financial impact (если applicable)
```

**Escalation Process**
```
Level 1 → Level 2 → Level 3 → Engineering
(Support) (Senior)  (Expert)  (Development)

When to escalate:
- L1 не может resolve за 2 hours (Severity 1)
- Требуется firmware/software bug fix
- Hardware replacement не resolved issue
- Widespread problem (multiple systems affected)
- Known issue требует workaround или patch

Effective escalation:
- Clear problem statement
- All diagnostic data attached
- Business impact quantified
- Requested action specific
```

### Known Issues Tracking

**Process**
```
1. Discovery:
   - Vendor bulletin/advisory
   - Community reports (forums, social media)
   - Internal multiple occurrences

2. Assessment:
   - Impact severity
   - Affected population (# systems в fleet)
   - Mitigation availability
   - Vendor ETA для fix

3. Action:
   - Apply patch/workaround (если available)
   - Proactive monitoring (если no fix yet)
   - Communication план (stakeholders)
   - Track to resolution

4. Knowledge Base:
   - Document issue, symptoms, resolution
   - Runbook для rapid response (если recurs)
   - Lessons learned
```

## Референсы

Подробные материалы доступны в директории `references/`:
- `rca-templates.md` - Шаблоны отчетов RCA
- `failure-mode-catalog.md` - Каталог типовых отказов по категориям оборудования
- `monitoring-thresholds.md` - Рекомендуемые пороги мониторинга
- `vendor-escalation-guide.md` - Процедуры эскалации для major vendors

Примеры и чек-листы в директории `assets/`:
- `rca-checklist.md` - Контрольный список для проведения RCA
- `failure-analysis-report-example.md` - Пример полного отчета
- `preventive-maintenance-schedule.md` - Шаблон графика ТО
