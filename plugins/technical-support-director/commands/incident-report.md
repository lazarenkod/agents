---
name: incident-report
description: Generate comprehensive incident post-mortem report with timeline, root cause analysis, and action items.
---

# Генерация Incident Post-Mortem Report

Эта команда помогает создать comprehensive post-mortem report после разрешения критического инцидента.

## Входные Данные

Предоставьте следующую информацию об инциденте:

1. **Базовая информация:**
   - Incident ID
   - Название инцидента
   - Severity (P1/P2/P3)
   - Дата и время начала (UTC)
   - Дата и время разрешения (UTC)

2. **Impact данные:**
   - Количество затронутых пользователей
   - Затронутые сервисы
   - Estimated revenue impact (если применимо)
   - Регионы/зоны доступности

3. **Timeline events:**
   - Хронология ключевых событий с timestamps
   - Actions taken
   - Key decisions made

4. **Technical details:**
   - Root cause
   - Contributing factors
   - Resolution steps

## Процесс Генерации

Команда сгенерирует structured post-mortem в следующем формате:

```markdown
# Post-Mortem: [Incident Title]

**Дата**: YYYY-MM-DD
**Длительность**: X hours Y minutes
**Severity**: P1/P2/P3
**Автор**: [Your Name]

## Исполнительное Резюме

[2-3 предложения краткого описания: что случилось, impact, resolution]

## Impact

- **Пользователи затронуты**: [Number/percentage]
- **Сервисы затронуты**: [List]
- **Revenue Impact**: [$Amount или N/A]
- **Downtime**: [Duration]
- **Регионы**: [Geographic areas]

## Timeline (UTC)

| Время | Событие |
|-------|---------|
| HH:MM | 🔴 Incident started - [Initial symptom] |
| HH:MM | 🔔 Alert triggered - [Monitoring system] |
| HH:MM | 👥 War room assembled |
| HH:MM | 🔍 Root cause identified - [Brief description] |
| HH:MM | 🔧 Fix deployed - [Action taken] |
| HH:MM | 📊 Metrics returning to normal |
| HH:MM | ✅ Resolution verified |
| HH:MM | 📢 Customer communication sent |

## Root Cause

### Technical Root Cause
[Детальное объяснение технической причины инцидента]

### Contributing Factors
1. **Factor 1**: [Explanation]
2. **Factor 2**: [Explanation]
3. **Factor 3**: [Explanation]

### 5 Whys Analysis
**Problem**: [Initial problem statement]

**Why #1**: Почему [problem]?
→ [Answer]

**Why #2**: Почему [answer from Why #1]?
→ [Answer]

**Why #3**: Почему [answer from Why #2]?
→ [Answer]

**Why #4**: Почему [answer from Why #3]?
→ [Answer]

**Why #5**: Почему [answer from Why #4]?
→ [Root cause]

## Resolution

### Immediate Actions Taken
1. [Action 1]
2. [Action 2]
3. [Action 3]

### Verification Process
- [How resolution was verified]
- [Metrics checked]
- [Customer validation]

## What Went Well ✅

- [Positive aspect 1]
- [Positive aspect 2]
- [Positive aspect 3]

## What Could Be Improved ❌

- [Improvement area 1]
- [Improvement area 2]
- [Improvement area 3]

## Action Items

| Action | Owner | Due Date | Priority | Status |
|--------|-------|----------|----------|--------|
| [Preventive action] | @person | YYYY-MM-DD | P0 | Open |
| [Process improvement] | @person | YYYY-MM-DD | P1 | Open |
| [Monitoring enhancement] | @person | YYYY-MM-DD | P1 | Open |
| [Documentation update] | @person | YYYY-MM-DD | P2 | Open |

## Lessons Learned

1. **Lesson 1**: [Key takeaway]
2. **Lesson 2**: [Key takeaway]
3. **Lesson 3**: [Key takeaway]

## Prevention

### Immediate (0-1 week)
- [Short-term fix or mitigation]

### Short-term (1-4 weeks)
- [Process improvements]
- [Additional monitoring]

### Long-term (1-6 months)
- [Architectural changes]
- [Systemic improvements]

## Appendix

### Relevant Links
- Incident ticket: [Link]
- Monitoring dashboard: [Link]
- Communication thread: [Link]
- Customer communication: [Link]

### Logs/Screenshots
[Attach or link to relevant technical evidence]
```

## Сохранение Report

Report будет сохранен в файл:
- Путь: `./incident-reports/YYYY-MM-DD-incident-[id]-postmortem.md`
- Формат: Markdown (на русском языке)
- Автоматически создается директория если не существует

## Следующие Шаги

После генерации report:

1. **Review**: Проверьте accuracy и completeness
2. **Share**: Распространите среди stakeholders
3. **Schedule**: Организуйте post-mortem meeting если needed
4. **Track**: Добавьте action items в project tracking system
5. **Follow-up**: Регулярно проверяйте progress по action items
6. **Archive**: Сохраните в knowledge base для future reference

## Примечания

- Report создается на русском языке
- Используйте emoji для visual clarity в timeline
- Фокусируйтесь на системных проблемах, а не на blame individuals
- Будьте конкретны в action items (owner, deadline, success criteria)
