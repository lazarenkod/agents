---
name: sla-engineering
description: Проектирование SLA, SLO и SLI для облачных сервисов. Use when defining service level agreements, calculating error budgets, designing reliability targets, or establishing SRE practices.
---

# SLA Engineering

Руководство по проектированию Service Level Agreements, Objectives и Indicators для облачных провайдеров.

## Когда использовать этот скилл

- Определение SLA для новых сервисов
- Расчет error budgets
- Проектирование SLO иSLI
- Разработка compensation policies
- SRE practices implementation
- Reliability target setting

## Основные концепции

### SLI (Service Level Indicators)

```markdown
# SLI = Измеримая метрика качества сервиса

## Типы SLI

### 1. Availability SLI
**Definition**: Процент успешных запросов

Formula:
Availability = (Successful Requests / Total Requests) × 100%

**Measurement**:
```python
# Prometheus query
sum(rate(http_requests_total{status!~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

**Thresholds (industry standard)**:
- 99.9% ("three nines") = 43.8 min downtime/month
- 99.95% = 21.9 min downtime/month
- 99.99% ("four nines") = 4.38 min downtime/month
- 99.999% ("five nines") = 26.3 sec downtime/month

**Применение по tier**:
- Tier 1 (critical): 99.95-99.99%
- Tier 2 (important): 99.9%
- Tier 3 (standard): 99.5%

### 2. Latency SLI
**Definition**: Response time percentiles

**Measurement points**:
- p50 (median): 50% requests faster than X
- p95: 95% requests faster than X
- p99: 99% requests faster than X
- p99.9: 99.9% requests faster than X

**Why percentiles?**
- Average hides outliers
- p99 catches tail latency
- User experience focused

**Example targets**:
```yaml
API Service:
  p50: < 100ms
  p95: < 200ms
  p99: < 500ms
  p99.9: < 1000ms

Database:
  p50: < 10ms
  p95: < 50ms
  p99: < 100ms
```

**AWS Service Examples**:
- DynamoDB: p99 < 10ms (single-digit millisecond)
- S3: p99 < 100ms для GET requests
- Lambda: cold start p99 < 1000ms

### 3. Throughput SLI
**Definition**: Requests per second capacity

```python
# Prometheus
rate(http_requests_total[1m])
```

**Targets**:
- Sustained: 10,000 RPS
- Burst (1 minute): 50,000 RPS
- Peak (Black Friday): 100,000 RPS

### 4. Durability SLI (Storage)
**Definition**: Probability of data loss

**AWS S3 Example**:
- Durability: 99.999999999% (11 nines)
- Meaning: Losing 1 object per 10 billion per year
- Implementation: erasure coding across multiple AZs

**Calculation**:
```
11 nines = 1 - (1 / 10^11)
If you store 10 million objects:
Expected loss = 10,000,000 / 10,000,000,000 = 0.001 objects/year
```

### 5. Error Rate SLI
**Definition**: Percentage of failed requests

```python
# Target: < 0.1% error rate
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
< 0.001
```

**Classification**:
- **5xx errors**: service fault (counts against SLA)
- **4xx errors**: client fault (excluded from SLA usually)
- **Timeout**: counts as error
- **Throttling**: may or may not count (policy decision)
```

### SLO (Service Level Objectives)

```markdown
# SLO = Internal target для SLI (stricter than SLA)

## SLO Design Principles

1. **User-Centric**: Based on user experience, not technical metrics
2. **Achievable**: Must be realistic given architecture
3. **Measurable**: Clear measurement methodology
4. **Aspirational**: Stretch goals для improvement

## SLO vs SLA Relationship

```
        Tighter ←                    → Looser
Internal Target          Customer Contract

99.99% SLO  →  99.95% SLA
(Engineering goal) (Legal commitment)

Gap = Error budget для innovation
```

**Example Stack**:
| Layer | SLO Target | Reason |
|-------|-----------|--------|
| Load Balancer | 99.99% | Most reliable layer |
| API Gateway | 99.98% | Aggregates risk |
| Microservice | 99.95% | Business logic complexity |
| Database | 99.99% | Managed service, redundant |
| **Aggregate SLO** | **99.92%** | Multiplied: 0.9999×0.9998×0.9995×0.9999 |

## SLO Templates by Service Type

### Compute Service (EC2-like)
```yaml
Service: Virtual Machines
SLOs:
  - metric: Instance Availability
    target: 99.95%
    measurement_window: monthly
    calculation: (Total minutes - Downtime) / Total minutes

  - metric: API Availability
    target: 99.99%
    scope: Control plane operations (Start, Stop, Terminate)

  - metric: API Latency
    target: p99 < 1000ms
    scope: Instance launch time

Exclusions:
  - Customer-initiated shutdowns
  - Scheduled maintenance (with 2-week notice)
  - Force majeure events
```

### Storage Service (S3-like)
```yaml
Service: Object Storage
SLOs:
  - metric: Durability
    target: 99.999999999% (11 nines)
    measurement: Annual

  - metric: Availability
    target: 99.9%
    measurement: Monthly
    scope: GET, PUT, LIST operations

  - metric: Latency (GET)
    target: p99 < 100ms
    condition: Objects < 5GB

  - metric: Throughput
    target: 3,500 PUT/s, 5,500 GET/s per prefix

Data_Consistency: Read-after-write для PUTs, eventual для DELETEs
```

### Database Service (RDS-like)
```yaml
Service: Managed PostgreSQL
SLOs:
  - metric: Availability (Multi-AZ)
    target: 99.95%
    measurement: Monthly

  - metric: Availability (Single-AZ)
    target: 99.5%

  - metric: Query Latency
    target: p95 < 50ms
    condition: Simple SELECT queries

  - metric: Backup Success Rate
    target: 100%

  - metric: RPO (Recovery Point Objective)
    target: 5 minutes
    implementation: Continuous backup to S3

  - metric: RTO (Recovery Time Objective)
    target: 30 minutes
    scope: Failover to standby
```

### CDN Service (CloudFront-like)
```yaml
Service: Content Delivery Network
SLOs:
  - metric: Edge Availability
    target: 99.9% per edge location

  - metric: Cache Hit Ratio
    target: > 80%

  - metric: Latency (cached content)
    target: p95 < 50ms

  - metric: Origin Shield Hit Rate
    target: > 90%
    measurement: Reduces origin load
```

## Error Budget Calculation

```markdown
# Error Budget = (1 - SLO) × Time Period

## Example: 99.95% SLO

Monthly error budget:
= (1 - 0.9995) × 30 days × 24 hours × 60 minutes
= 0.0005 × 43,200 minutes
= 21.6 minutes/month

Weekly error budget:
= 21.6 / 4.3 = 5 minutes/week

Daily error budget:
= 21.6 / 30 = 0.72 minutes/day = 43 seconds/day

## Error Budget Policy

```yaml
Error_Budget_Status:
  Healthy (> 50% remaining):
    - Normal release cadence (daily)
    - Feature development prioritized
    - Low-risk changes allowed

  Warning (10-50% remaining):
    - Slower release cadence (weekly)
    - Increased testing/review
    - Focus on stability

  Exhausted (< 10% remaining):
    - Release freeze (except fixes)
    - All-hands reliability efforts
    - Postmortem required
    - Resume only when budget replenished > 25%

Measurement_Window:
  Rolling 30-day window (not calendar month)
  Reason: Avoids gaming the system at month boundaries
```

## Burn Rate Alerting

```markdown
# Burn Rate = Speed of error budget consumption

## Multi-Window Alerting (Google SRE)

### Critical Alert (Page immediately)
Condition:
  - 2% of budget burned in 1 hour (14.4× burn rate)
  - AND confirmed over 5 minutes

Calculation:
Monthly budget: 21.6 min
2% = 0.43 minutes = 26 seconds
If we burn 26 sec in 1 hour → exhausted in 50 hours

Action: Wake up on-call engineer

### Warning Alert (Ticket)
Condition:
  - 5% of budget burned in 6 hours (3.3× burn rate)

Calculation:
5% of 21.6 min = 1.08 minutes
If we burn 1.08 min in 6 hours → exhausted in 5 days

Action: Investigate during business hours

### Implementation (Prometheus)
```yaml
groups:
- name: slo_alerts
  rules:
  - alert: ErrorBudgetBurnRateCritical
    expr: |
      (
        sum(rate(http_requests_total{status=~"5.."}[1h]))
        /
        sum(rate(http_requests_total[1h]))
      ) > (14.4 * 0.0005)  # 14.4× burn × SLO threshold
    for: 5m
    annotations:
      summary: "Critical: Error budget exhausted in 50 hours at current rate"

  - alert: ErrorBudgetBurnRateWarning
    expr: |
      (
        sum(rate(http_requests_total{status=~"5.."}[6h]))
        /
        sum(rate(http_requests_total[6h]))
      ) > (3.3 * 0.0005)
    for: 30m
```
```

### SLA (Service Level Agreements)

```markdown
# SLA = Contractual commitment to customers

## SLA Components

### 1. Service Credit Policy

**AWS EC2 Example**:
| Monthly Uptime % | Service Credit |
|------------------|----------------|
| < 99.99% but ≥ 99.0% | 10% |
| < 99.0% | 30% |

**Azure VMs Example (Single Instance)**:
| Monthly Uptime % | Service Credit |
|------------------|----------------|
| < 99.9% | 10% |
| < 99.0% | 25% |
| < 95.0% | 100% |

**Calculation**:
```python
# Customer bill: $10,000
# Actual uptime: 99.5% (target: 99.9%)
# Credit tier: 10%

Service credit = $10,000 × 10% = $1,000
Applied to next month's bill
```

### 2. Claim Process

```markdown
## SLA Credit Request Process

1. **Detection Period**:
   - Customer must file claim within 30 days of incident

2. **Required Information**:
   - Account ID
   - Impacted resource IDs
   - Timestamp of unavailability
   - Error logs/screenshots

3. **Provider Verification**:
   - Check monitoring data
   - Validate customer claim
   - Calculate downtime

4. **Credit Issuance**:
   - Applied to next month's invoice
   - Maximum: 100% of monthly fee для affected service
   - Not refundable cash

5. **Timeline**:
   - Response within 10 business days
   - Credit applied within 1 billing cycle
```

### 3. SLA Exclusions (Standard)

```yaml
Excluded_from_SLA:
  - Customer Actions:
      - Misconfiguration by customer
      - Customer-initiated shutdowns
      - Quota/limit exceeded
      - Payment failures

  - External Factors:
      - Internet/DNS issues outside our control
      - DDoS attacks (unless we offer DDoS protection)
      - Force majeure (natural disasters, war, etc.)

  - Scheduled Maintenance:
      - Announced 2+ weeks in advance
      - During maintenance window (e.g., Tue 2-6 AM)
      - Limited to 4 hours/month

  - Beta/Preview Services:
      - Clearly marked as preview
      - No SLA until General Availability (GA)

  - Free Tier Usage:
      - Best-effort only, no SLA
```

## SLA Design Patterns

### Pattern 1: Tiered SLA (by Service Tier)

```markdown
## Premium Tier (99.99%)
- Multi-AZ deployment mandatory
- Priority support (15-minute response)
- Dedicated capacity reserved
- 30% service credit if breached
Price: 2× Standard

## Standard Tier (99.9%)
- Single or Multi-AZ available
- Standard support (4-hour response)
- Shared capacity
- 10% service credit
Price: 1× baseline

## Basic Tier (99.5%)
- Single-AZ only
- Community support
- Best-effort capacity
- No service credits
Price: 0.5× Standard
```

### Pattern 2: Regional SLA

```markdown
## AWS Global Service Example

### Regional Scope:
- SLA applies per region
- Multi-region replication customer responsibility
- Failure in US-East-1 doesn't credit US-West-2

### Multi-Region SLA (optional):
- Customer can purchase cross-region failover SLA
- Higher SLA: 99.99% (any region available)
- Premium pricing: +50%
```

### Pattern 3: Dependency-Based SLA

```markdown
## Composite Service SLA

Service: Managed Kubernetes (like GKE/EKS)

Component SLAs:
- Control Plane: 99.95%
- Worker Nodes (customer managed): 99.5%
- Networking (VPC): 99.99%
- Load Balancer: 99.99%

Aggregate SLA Calculation:
= 0.9995 × 0.995 × 0.9999 × 0.9999
= 0.9943 = 99.43%

Published SLA: 99.5% (conservative)
Reason: Includes buffer для customer config issues
```

## SLA Monitoring & Reporting

```markdown
# Automated SLA Compliance Tracking

## Real-Time Dashboard

```python
# Pseudocode для SLA dashboard

class SLAMonitor:
    def __init__(self, slo_target=0.999):
        self.slo = slo_target
        self.window = 30  # days

    def current_availability(self):
        """Calculate current availability"""
        total_requests = query_metrics("sum(http_requests_total[30d])")
        failed_requests = query_metrics("sum(http_requests_total{status=~'5..'}[30d])")
        return (total_requests - failed_requests) / total_requests

    def error_budget_remaining(self):
        """Calculate remaining error budget"""
        actual_availability = self.current_availability()
        error_budget_used = (1 - actual_availability)
        error_budget_total = (1 - self.slo)
        return (error_budget_total - error_budget_used) / error_budget_total

    def projected_SLA_breach(self):
        """Predict if SLA will be breached"""
        burn_rate = self.calculate_burn_rate()
        budget_remaining = self.error_budget_remaining()
        days_until_breach = (budget_remaining / burn_rate) * 30
        return days_until_breach < 7  # Alert if < 1 week
```

## Monthly SLA Report Template

```markdown
# SLA Compliance Report - [Month] [Year]

## Executive Summary
- **Overall SLA Status**: ✅ Met / ⚠️ At Risk / ❌ Breached
- **Availability Achieved**: 99.97%
- **SLA Target**: 99.95%
- **Incidents**: 2 (1 SEV2, 1 SEV3)
- **Service Credits Issued**: $12,450

## Detailed Metrics

### Availability by Service
| Service | SLA Target | Achieved | Status | Incidents |
|---------|-----------|----------|--------|-----------|
| Compute | 99.95% | 99.98% | ✅ Met | 0 |
| Storage | 99.9% | 99.87% | ❌ Missed | 2 |
| Database | 99.95% | 99.96% | ✅ Met | 0 |
| Networking | 99.99% | 99.99% | ✅ Met | 0 |

### Incidents Detail

#### INC-2024-001 (SEV2)
- **Service**: Object Storage
- **Date**: Jan 15, 2024 14:30-15:45 UTC
- **Duration**: 75 minutes
- **Impact**: 2.3% of GET requests failed
- **Root Cause**: Storage node cascade failure
- **Customers Affected**: 145
- **Service Credits**: $8,200

#### INC-2024-002 (SEV3)
- **Service**: Storage API
- **Date**: Jan 22, 2024 03:20-04:10 UTC
- **Duration**: 50 minutes
- **Impact**: Elevated latency, no failures
- **Root Cause**: Database connection pool exhaustion
- **Customers Affected**: 23
- **Service Credits**: $4,250

## Error Budget Status
- **Budget Allocated**: 21.6 minutes (99.95% SLO)
- **Budget Consumed**: 18.2 minutes (84%)
- **Budget Remaining**: 3.4 minutes (16%)
- **Status**: ⚠️ Warning - Low budget

## Recommendations
1. Implement connection pool auto-scaling (prevent INC-2024-002 recurrence)
2. Add redundancy to storage nodes (increase resilience)
3. Slow release velocity для Feb (replenish error budget)
```

---

**Все SLA документы, расчеты и отчеты сохраняются в Markdown на русском языке.**
