---
name: sla-dashboard
description: Generate SLA performance dashboard and compliance report for specified time period.
---

# Генерация SLA Performance Dashboard

Создает comprehensive SLA dashboard с метриками, trends и actionable insights.

## Входные Параметры

1. **Time Period:**
   - Weekly (default)
   - Monthly
   - Quarterly
   - Custom date range

2. **Scope:**
   - All tickets (default)
   - By priority (P1, P2, P3, P4)
   - By team/engineer
   - By customer segment

3. **Metrics:**
   - Response Time SLA
   - Resolution Time SLA
   - Availability SLA
   - All metrics (default)

## Generated Dashboard

```markdown
# SLA Performance Dashboard - [Period]

**Период**: [Start Date] - [End Date]
**Сгенерировано**: [Current Timestamp]

---

## 📊 Executive Summary

### Overall Performance
- **Response Time Compliance**: X.X% [✅/⚠️/❌]
- **Resolution Time Compliance**: X.X% [✅/⚠️/❌]
- **Availability**: XX.XX% [✅/⚠️/❌]

### Trend vs Previous Period
- Response Time: [↑ +X% | ↓ -X% | → Stable]
- Resolution Time: [↑ +X% | ↓ -X% | → Stable]
- Tickets Volume: XXX ([↑ +X% | ↓ -X% | → Stable])

### Health Status
🟢 **HEALTHY**: All SLA targets met
🟡 **AT RISK**: One or more metrics trending down
🔴 **CRITICAL**: Active SLA breaches requiring attention

---

## 📈 Response Time SLA

### Compliance by Priority

| Priority | Target | Actual Avg | Median | 95th % | Compliance | Breaches | Status |
|----------|--------|------------|--------|--------|------------|----------|--------|
| P1 | 15 min | XX min | XX min | XX min | XX.X% | X | [✅/⚠️/❌] |
| P2 | 30 min | XX min | XX min | XX min | XX.X% | X | [✅/⚠️/❌] |
| P3 | 2 hrs | XX hrs | XX hrs | XX hrs | XX.X% | X | [✅/⚠️/❌] |
| P4 | 8 hrs | XX hrs | XX hrs | XX hrs | XX.X% | X | [✅/⚠️/❌] |

### Daily Trend (Last 7/30 Days)
```
Day     | P1 Avg | P2 Avg | P3 Avg | P4 Avg | Compliance
--------|--------|--------|--------|--------|------------
Mon     | XX min | XX min | XX hrs | XX hrs | XX.X%
Tue     | XX min | XX min | XX hrs | XX hrs | XX.X%
...
```

### Breach Analysis
**Total Breaches**: X tickets

**Top Root Causes**:
1. [Category] - X breaches (XX%)
   - Example: Staffing gaps during shift change
2. [Category] - X breaches (XX%)
3. [Category] - X breaches (XX%)

---

## ⏱️ Resolution Time SLA

### Compliance by Priority

| Priority | Target | Actual Avg | Median | 95th % | Compliance | Breaches | Status |
|----------|--------|------------|--------|--------|------------|----------|--------|
| P1 | 4 hrs | XX hrs | XX hrs | XX hrs | XX.X% | X | [✅/⚠️/❌] |
| P2 | 8 hrs | XX hrs | XX hrs | XX hrs | XX.X% | X | [✅/⚠️/❌] |
| P3 | 24 hrs | XX hrs | XX hrs | XX hrs | XX.X% | X | [✅/⚠️/❌] |
| P4 | 5 days | XX days | XX days | XX days | XX.X% | X | [✅/⚠️/❌] |

### Breach Analysis
**Total Breaches**: X tickets

**Top Root Causes**:
1. [Category] - X breaches (XX%)
2. [Category] - X breaches (XX%)
3. [Category] - X breaches (XX%)

---

## 📡 Availability SLA

### Monthly Uptime

| Service | Target | Actual | Downtime | Incidents | Status |
|---------|--------|--------|----------|-----------|--------|
| Service A | 99.95% | XX.XX% | XX min | X | [✅/⚠️/❌] |
| Service B | 99.99% | XX.XX% | XX min | X | [✅/⚠️/❌] |

### Downtime Budget
- **Allocated**: XX.X minutes/month (for 99.XX% SLA)
- **Used**: XX.X minutes
- **Remaining**: XX.X minutes (XX%)

---

## 🎯 Tickets At Risk (Next 24-48 Hours)

### Critical Attention Needed

| Ticket ID | Priority | Age | SLA Remaining | Customer | Status |
|-----------|----------|-----|---------------|----------|--------|
| #XXXXX | P1 | Xh XXm | XXm remaining | [Customer] | URGENT |
| #XXXXX | P2 | Xh XXm | Xh XXm remaining | [Customer] | AT RISK |

**Action Required**: [Recommended interventions]

---

## 💰 Service Credits

### Summary
- **Total Credits**: $X,XXX
- **% of Monthly Revenue**: X.XX%
- **Customers Affected**: X

### Breakdown

| Customer | Credits | Reason | Status |
|----------|---------|--------|--------|
| [Name] | $XXX | P1 breach × 2 | Applied |
| [Name] | $XXX | Availability breach | Pending |

---

## 📊 Performance by Team/Engineer

### Top Performers (by SLA compliance)

| Engineer | Tickets | Response Time | Resolution Time | SLA Compliance |
|----------|---------|---------------|-----------------|----------------|
| Alice | XXX | XX min avg | XX hrs avg | XX.X% |
| Bob | XXX | XX min avg | XX hrs avg | XX.X% |

### Needs Support

| Engineer | Issues | Action |
|----------|--------|--------|
| [Name] | High breach rate (XX%) | Coaching scheduled |
| [Name] | Below team avg | Training plan created |

---

## ⚠️ Alerts & Recommendations

### Active Concerns
1. **[Issue]**: [Description]
   - **Impact**: [Quantified impact]
   - **Recommendation**: [Specific action]
   - **Owner**: [Assigned person]
   - **Due**: [Date]

### Process Improvements
1. [Improvement opportunity]
2. [Improvement opportunity]

### Trending Risks
- 📈 [Metric] increasing X% week-over-week
- 📉 [Metric] declining, investigate root cause

---

## 📋 Action Items

| Priority | Action | Owner | Due Date | Status |
|----------|--------|-------|----------|--------|
| P0 | [Critical action] | @person | YYYY-MM-DD | Open |
| P1 | [Important action] | @person | YYYY-MM-DD | Open |
| P2 | [Standard action] | @person | YYYY-MM-DD | Open |

---

## 📎 Appendix

### Data Sources
- Ticketing System: [System name]
- Monitoring: [System name]
- Date Range: [Start] to [End]
- Total Tickets Analyzed: XXX

### Calculation Methods
- Response Time: Time from ticket creation to first response
- Resolution Time: Time from ticket creation to resolution
- Business Hours: [Definition if applicable]
- Exclusions: [Any tickets excluded and why]

### Definitions
- **SLA Compliance**: Percentage of tickets meeting SLA target
- **Breach**: Ticket exceeding SLA target
- **At Risk**: Ticket approaching SLA deadline (>75% time elapsed)
```

## Сохранение Dashboard

Dashboard сохраняется в:
- **Path**: `./sla-reports/YYYY-MM-DD-sla-dashboard-[period].md`
- **Format**: Markdown (на русском языке)
- **Auto-refresh**: Опционально можно настроить автоматическую регенерацию

## Визуализация

Для визуализации можно экспортировать в:
1. **Grafana**: JSON конфигурация в `./grafana-dashboards/`
2. **Excel**: CSV export для графиков
3. **Presentation**: PowerPoint-ready metrics

## Автоматизация

Настройте автоматическую генерацию:
```bash
# Weekly report (every Monday)
# Monthly report (first day of month)
# Real-time dashboard (continuous update)
```

## Алерты

Dashboard автоматически генерирует alerts для:
- SLA compliance < 95%
- Trend degradation (>5% decline)
- At-risk tickets approaching deadline
- Service credit threshold exceeded
