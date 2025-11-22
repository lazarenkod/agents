# Technical Support Director Plugin

Комплексный плагин для роли Technical Support Director облачного провайдера с экспертизой уровня AWS, Azure, Google Cloud, Oracle Cloud.

## Обзор

Этот плагин предоставляет полный набор агентов, навыков и команд для управления технической поддержкой enterprise-уровня в облачных провайдерах. Разработан на основе best practices ведущих облачных провайдеров.

## Компоненты

### Агенты (6)

1. **support-director** - Главный директор технической поддержки
   - Стратегическое управление поддержкой
   - Управление SLA, командой, процессами
   - Координация кросс-функциональных инициатив

2. **incident-commander** - Командир критических инцидентов
   - Управление P1/P2 инцидентами
   - War room coordination
   - Post-mortem analysis

3. **sla-compliance-manager** - Менеджер по соблюдению SLA
   - Мониторинг SLA compliance
   - Расчет service credits
   - Breach analysis и reporting

4. **team-performance-analyst** - Аналитик производительности команды
   - KPI tracking (CSAT, NPS, FCR)
   - Capacity planning
   - Quality assurance

5. **knowledge-base-curator** - Куратор базы знаний
   - Content management
   - Search optimization
   - Deflection rate improvement

6. **escalation-coordinator** - Координатор эскалаций
   - Technical и executive escalations
   - Vendor coordination (AWS, Azure, GCP, Oracle)
   - Customer relationship recovery

### Скиллы (10)

1. **incident-management** - Управление инцидентами (ICS, War Room, Post-Mortems)
2. **sla-management** - Управление SLA (Compliance, Credits, Reporting)
3. **crisis-communication** - Кризисная коммуникация (Internal/External)
4. **root-cause-analysis** - Анализ первопричин (5 Whys, Fishbone, Fault Tree)
5. **vendor-escalation** - Эскалация к вендорам (AWS, Azure, GCP, Oracle)
6. **customer-success** - Успех клиентов (CSAT/NPS, Health Scoring, QBRs)
7. **capacity-planning** - Планирование мощностей (Staffing, Forecasting)
8. **knowledge-base-optimization** - Оптимизация базы знаний (Deflection, SEO)
9. **team-coaching** - Коучинг команды (1-on-1s, Development Plans)
10. **executive-communication** - Коммуникация с руководством (Briefs, Dashboards)

### Команды (4)

1. **incident-report** - Генерация post-mortem reports
2. **sla-dashboard** - Создание SLA performance dashboards
3. **team-metrics** - Отчеты по производительности команды
4. **escalation-workflow** - Workflow управления эскалациями

## Особенности

### Многоязычная Поддержка
Все агенты и скиллы поддерживают русский и английский языки. Автоматическое определение языка запроса.

### Экспертиза Уровня Enterprise
- AWS Enterprise Support best practices
- Azure Premier/Unified Support patterns
- Google Cloud Premium Support workflows
- Oracle Cloud Premier Support procedures

### Все Результаты на Русском
Все генерируемые документы, отчеты и дашборды создаются на русском языке:
- Post-mortem reports
- SLA dashboards
- Team metrics
- Escalation tracking

### Production-Ready Templates
- Incident playbooks
- Communication templates
- Escalation procedures
- Metrics dashboards

## Использование

### Установка
```bash
# Установка плагина через Claude Code
claude plugin install technical-support-director
```

### Примеры Использования

**Создание Post-Mortem Report:**
```
Используй команду /incident-report для создания post-mortem отчета по инциденту P1 с database outage
```

**Генерация SLA Dashboard:**
```
Создай SLA dashboard за январь 2024 с breakdown по priorities и breach analysis
```

**Анализ Производительности Команды:**
```
Сгенерируй team performance report с индивидуальными метриками и coaching recommendations
```

**Vendor Escalation:**
```
Помоги создать escalation к AWS TAM для критического RDS инцидента
```

## Структура Плагина

```
technical-support-director/
├── agents/                    # 6 специализированных агентов
│   ├── support-director.md
│   ├── incident-commander.md
│   ├── sla-compliance-manager.md
│   ├── team-performance-analyst.md
│   ├── knowledge-base-curator.md
│   └── escalation-coordinator.md
├── skills/                    # 10 навыков с references
│   ├── incident-management/
│   ├── sla-management/
│   ├── crisis-communication/
│   ├── root-cause-analysis/
│   ├── vendor-escalation/
│   ├── customer-success/
│   ├── capacity-planning/
│   ├── knowledge-base-optimization/
│   ├── team-coaching/
│   └── executive-communication/
└── commands/                  # 4 команды для automation
    ├── incident-report.md
    ├── sla-dashboard.md
    ├── team-metrics.md
    └── escalation-workflow.md
```

## Best Practices

### Управление Инцидентами
- Используйте Incident Command System (ICS) для структурированного управления
- War Room protocols для критических P1/P2
- Blameless post-mortems с фокусом на системные улучшения

### SLA Management
- Проактивный мониторинг at-risk tickets
- Автоматизация расчета service credits
- Root cause analysis для всех breaches

### Team Management
- Data-driven decisions через KPI и analytics
- Regular 1-on-1s и development planning
- Quality assurance через systematic ticket reviews

### Vendor Relations
- Enterprise support plans для критических сервисов
- Established escalation paths к TAM/DSE/CE
- Documented procedures для всех major vendors

## Требования

- Claude Code (latest version)
- Claude Agent SDK support
- Рекомендуется: опыт в enterprise technical support

## Версия

**1.0.0** - Initial release
- 6 agents
- 10 skills
- 4 commands
- Полная поддержка русского языка
- Production-ready templates

## Лицензия

MIT

## Автор

Dmitry Lazarenko
- GitHub: [@lazarenkod](https://github.com/lazarenkod)
- Email: lazarenkod@gmail.com

## Вклад

Contributions welcome! См. CONTRIBUTING.md для деталей.
