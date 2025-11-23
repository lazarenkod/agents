---
name: cloud-economics
description: Экономика облачных сервисов и FinOps практики. Use when analyzing cloud costs, optimizing spend, developing pricing strategies, calculating TCO, or implementing FinOps programs.
---

# Экономика облачных сервисов (Cloud Economics)

Комплексное руководство по финансовому управлению облачной платформой на базе практик AWS, Azure, Google Cloud и Oracle Cloud.

## Когда использовать этот скилл

- Разработка pricing моделей для облачных сервисов
- Анализ и оптимизация cloud costs
- Расчет Total Cost of Ownership (TCO)
- Внедрение FinOps практик
- Margin analysis по сервисам
- Resource optimization и waste elimination

## Основные концепции

### Модели ценообразования облачных сервисов

#### 1. Compute Pricing Models

**On-Demand / Pay-As-You-Go**
```markdown
## Характеристики
- Почасовая или посекундная оплата
- Нет commitment или upfront payment
- Максимальная гибкость
- Highest unit cost

## Применение
- Непредсказуемые workloads
- Development/testing environments
- Краткосрочные проекты
- Spike handling

## Примеры
AWS EC2: $0.096/hour (m5.xlarge, on-demand)
Azure VM: $0.096/hour (D4s_v3, pay-as-you-go)
GCP: $0.095/hour (n2-standard-4, on-demand)
```

**Reserved Instances / Commitments**
```markdown
## AWS Reserved Instances
- 1-year или 3-year commitment
- Upfront payment options:
  - All Upfront: максимальная экономия (до 75% off)
  - Partial Upfront: средняя экономия (до 55% off)
  - No Upfront: минимальная экономия (до 40% off)
- Convertible RIs: можно менять instance type
- Standard RIs: фиксированный instance type

Пример экономии:
m5.xlarge On-Demand: $0.096/hour = $841/month
m5.xlarge RI 3-year All Upfront: $0.024/hour = $210/month
Savings: 75% ($631/month)

## Azure Reserved Instances
- 1-year или 3-year commitment
- Pay monthly или upfront
- Instance size flexibility в той же family
- Exchange/cancellation options

## Google Cloud Committed Use Discounts
- 1-year или 3-year commitment
- Flexible: applies to any VM в region
- Applies automatically (no manual mapping)
- До 57% discount

## Стратегия применения
1. Analyze usage patterns (CloudWatch, Cost Explorer)
2. Identify steady-state workloads (24/7 running)
3. Purchase RIs для coverage 70-80% baseline
4. Use on-demand для variable/spike capacity
5. Regular review и optimization (quarterly)
```

**Spot / Preemptible Instances**
```markdown
## AWS Spot Instances
- Unused EC2 capacity
- Bid price model (max price willing to pay)
- До 90% discount vs on-demand
- Can be interrupted (2-min warning)
- Best for fault-tolerant, flexible workloads

## Azure Spot VMs
- До 90% discount
- Eviction policies: Deallocate или Delete
- Price cap option

## Google Cloud Preemptible VMs
- До 80% discount
- Max 24-hour runtime
- No SLA
- 30-second shutdown notice

## Use Cases для Spot/Preemptible
✅ Batch processing (data analytics, rendering)
✅ CI/CD build agents
✅ Big data (EMR, Dataproc)
✅ Containerized stateless apps
✅ Testing environments

❌ Databases (stateful)
❌ Production web servers (unless with autoscaling fallback)
❌ Long-running computations without checkpointing

## Best Practices
- Implement checkpointing для long jobs
- Use Spot Fleet / Managed Instance Groups (diversification)
- Fallback to on-demand если spot unavailable
- Monitor spot price trends
- Set max price (не больше on-demand)
```

**Savings Plans (AWS/Azure)**
```markdown
## AWS Savings Plans
Два типа:

### 1. Compute Savings Plans
- Commitment: $/hour для any compute
- Flexibility: EC2, Lambda, Fargate
- Region, instance family, OS flexible
- До 66% savings

### 2. EC2 Instance Savings Plans
- Commitment: $/hour для EC2 в specific region
- Instance family specific
- Size, OS, tenancy flexible
- До 72% savings

Пример:
Commitment: $10/hour
Current usage: $15/hour (mix of EC2, Lambda, Fargate)
Savings Plan covers: $10/hour at discounted rate
Excess $5/hour: billed on-demand

## Azure Savings Plans для Compute
- Похожая модель на AWS
- 1-year или 3-year
- Hourly commitment
- До 65% savings
```

#### 2. Storage Pricing Models

**Tiered Storage Pricing**
```markdown
## AWS S3 Storage Classes

| Storage Class | Use Case | Cost ($/GB-month) | Retrieval Cost |
|---------------|----------|-------------------|----------------|
| S3 Standard | Frequent access | $0.023 | Free |
| S3 Intelligent-Tiering | Unknown patterns | $0.023 (frequent) | Free |
| S3 Standard-IA | Infrequent access | $0.0125 | $0.01/GB |
| S3 One Zone-IA | Non-critical, infrequent | $0.01 | $0.01/GB |
| S3 Glacier Instant | Archive, instant access | $0.004 | $0.03/GB |
| S3 Glacier Flexible | Archive, mins-hours | $0.0036 | $0.02/GB + requests |
| S3 Glacier Deep | Long-term, 12-hour retrieval | $0.00099 | $0.02/GB + requests |

## Cost Optimization Strategy
1. Lifecycle Policies:
   - 30 days → Standard-IA
   - 90 days → Glacier
   - 365 days → Glacier Deep Archive

2. S3 Intelligent-Tiering:
   - Auto-moves между access tiers
   - Monitoring fee: $0.0025/1000 objects
   - Worth it для > 128KB objects

3. CloudFront для hot data (reduce S3 GET requests)

Пример экономии:
10 TB данных, 90% не accessed > 30 дней
Standard: 10,000 GB × $0.023 = $230/month
IA (after 30 days): 9,000 GB × $0.0125 + 1,000 GB × $0.023 = $135.5/month
Savings: $94.5/month = 41%
```

#### 3. Database Pricing Models

**Provisioned vs Serverless**
```markdown
## AWS RDS Pricing
### Provisioned
- Instance cost: $0.17/hour (db.r5.xlarge)
- Storage: $0.115/GB-month (gp3)
- IOPS: $0.02/IOPS-month (если > 3000)
- Backup: $0.095/GB-month (exceeding DB size)
- Data transfer: $0.01-0.09/GB (out)

### Aurora Serverless v2
- ACU-based pricing
- 1 ACU = 2 GB RAM
- Auto-scaling (0.5 - 128 ACUs)
- $0.12/ACU-hour
- Ideal for: variable/unpredictable workloads

Пример сравнения:
Workload: variable, avg 4 ACUs, peak 20 ACUs (10% time)

Provisioned (db.r5.large = 8 ACUs):
$0.17/hour × 730 hours = $124/month

Serverless (avg 4.6 ACUs):
4.6 ACUs × $0.12 × 730 = $403/month

Winner: Provisioned (constant workload)

For spiky workload (2 ACUs avg, 20 peak 5% time):
Serverless: (2 × 0.95 + 20 × 0.05) × $0.12 × 730 = $241/month
Winner: Serverless
```

#### 4. Network Pricing (Data Transfer)

**Принципы pricing**
```markdown
## Data Transfer Costs (AWS example)

### Inbound
- Internet → AWS: FREE
- AWS region → AWS region: $0.01-0.02/GB
- Availability Zone → AZ (same region): $0.01/GB

### Outbound
- AWS → Internet:
  - First 100 GB/month: FREE (AWS Free Tier)
  - Next 10 TB: $0.09/GB
  - Next 40 TB: $0.085/GB
  - Next 100 TB: $0.07/GB
  - > 150 TB: $0.05/GB

### CloudFront (CDN)
- Origin → CloudFront: FREE
- CloudFront → Internet: $0.085/GB (US/Europe)
- Cheaper than direct S3/EC2 egress
- Reduces origin load

## Cost Optimization
1. **Use CloudFront**: даже для dynamic content (cheaper egress)
2. **VPC Endpoints**: S3/DynamoDB в той же region (FREE transfer)
3. **Direct Connect**: для high-volume transfers ($0.02/GB vs $0.09)
4. **Compress data**: reduce transfer volume
5. **Regional architecture**: minimize cross-region transfers

Пример экономии:
100 TB/month data transfer

Direct S3 → Internet:
100,000 GB × $0.05 (average tiered) = $5,000/month

Via CloudFront:
Origin → CloudFront: FREE
CloudFront → Internet: 100,000 × $0.085 = $8,500/month
Wait, that's worse!

Ah, but CloudFront caching reduces origin requests by 80%:
Origin traffic: 20 TB
CloudFront: 20,000 GB × $0.085 = $1,700/month
Savings: $3,300/month + reduced S3 requests
```

### FinOps Framework

#### FinOps Operating Model

```markdown
# FinOps Maturity Model

## Phase 1: Inform (Visibility)
### Цель: Understand where money is being spent

**Инструменты**:
- AWS Cost Explorer, Azure Cost Management, GCP Cost Management
- Tagging strategy (обязательная!)
- Showback reports (who's spending what)
- Anomaly detection alerts

**Метрики**:
- Total cloud spend
- Spend by service
- Spend by team/project
- Month-over-month growth

**Действия**:
- [ ] Implement comprehensive tagging
- [ ] Setup cost allocation reports
- [ ] Create baseline cost dashboards
- [ ] Enable budget alerts

## Phase 2: Optimize (Efficiency)
### Цель: Eliminate waste, improve efficiency

**Waste Categories**:
1. **Idle Resources**
   - Stopped EC2 instances (still paying for EBS)
   - Unused Elastic IPs ($0.005/hour = $3.60/month each)
   - Unattached EBS volumes
   - Old snapshots

2. **Overprovisioned Resources**
   - Right-sizing opportunities (CloudWatch metrics)
   - CPU utilization < 10% consistently
   - Memory underutilized

3. **Unused Reservations**
   - RIs для terminated instances
   - Unconverted standard RIs

**Tools**:
- AWS Compute Optimizer (ML-based recommendations)
- Azure Advisor
- GCP Recommender
- Third-party: CloudHealth, Cloudability, Apptio

**Quick Wins**:
```yaml
# Common optimizations with impact

1. Shutdown non-prod environments after hours
   Savings: 50-70% on dev/test costs
   Example: 100 instances × $0.10/hour × 16 hours/day × 22 days = $3,520/month

2. Right-size oversized instances
   Savings: 20-40% на affected instances
   Example: m5.2xlarge → m5.xlarge (50% reduction if underutilized)

3. Purchase RIs/Savings Plans для steady-state
   Savings: 40-75% на covered usage
   Example: $10,000/month on-demand → $3,000 with 3-year RI

4. Lifecycle policies для S3
   Savings: 50-90% на old/archived data
   Example: 100 TB old data, Standard → Glacier Deep = $2,300 → $99/month

5. Delete old snapshots/backups
   Savings: variable, often $100s-$1000s
   Automation: lambda function для cleanup
```

**Phase 2 Checklist**:
- [ ] Identify и delete idle resources (weekly scan)
- [ ] Right-size analysis (monthly)
- [ ] RI/Savings Plan coverage optimization (quarterly)
- [ ] Storage lifecycle policies (implement once, monitor)
- [ ] Compress/dedupe data где possible

## Phase 3: Operate (Continuous Improvement)
### Цель: Embed FinOps into culture

**Governance**:
- **FinOps Team**: centralized or distributed?
- **Budget ownership**: engineering teams own their budgets
- **KPIs**: cost per customer, cost per transaction, unit economics
- **Policies**: approval workflows для large spends

**Processes**:
```markdown
### Monthly FinOps Review
Attendees: Engineering leads, Finance, FinOps
Agenda:
1. Review spend trends (vs budget)
2. Top 3 cost drivers this month
3. Optimization initiatives (status, savings realized)
4. New services/projects (budget impact)
5. Action items для next month

### Quarterly Business Review
Attendees: Executives, FinOps lead
Topics:
1. Cloud spend vs revenue (unit economics)
2. Forecast для next quarter
3. Major optimization programs
4. RI/Commitment strategy review
5. Cloud strategy alignment (multi-cloud, new regions)
```

**Cultural Practices**:
- **Cost-aware development**: engineers see costs in dashboards
- **Shift-left**: cost considerations в design phase
- **Gamification**: team cost optimization leaderboards
- **Training**: FinOps certification (FinOps Foundation)

## FinOps Metrics & KPIs

```markdown
# Key Metrics Hierarchy

## Business Metrics
- **Unit Economics**: cost per user, transaction, API call
  Example: $0.05 per active user per month
- **Gross Margin**: (Revenue - COGS including cloud) / Revenue
  Target: > 70% для SaaS
- **Customer Acquisition Cost (CAC) Payback**: including infrastructure
- **Revenue per $ spent на cloud**: $10 revenue per $1 cloud cost (10x)

## Operational Metrics
- **RI/Savings Plan Coverage**: % of eligible usage covered
  Target: 70-80% (balance commitment vs flexibility)
- **RI/Savings Plan Utilization**: % of purchased commitment used
  Target: > 95%
- **Spot Usage**: % of compute на spot instances
  Target: 20-40% для fault-tolerant workloads
- **On-Demand Waste**: idle resources cost / total cost
  Target: < 5%

## Efficiency Metrics
- **Cost Per Environment**:
  - Production: $X
  - Staging: $Y (should be < 20% prod)
  - Dev: $Z (should be < 10% prod)
- **Infrastructure Cost as % of Revenue**:
  Target: < 30% (varies by industry)
- **Month-over-Month Spend Growth vs Usage Growth**:
  Ideal: usage growth > spend growth (efficiency improving)

## Team/Project Metrics
- **Spend Attribution**: 100% of costs tagged и allocated
- **Budget Variance**: actual vs forecast
  Target: within ±10%
- **Cost Avoidance**: savings from optimization (track annually)

# Dashboard Example (Grafana/Tableau)

```markdown
## Executive Dashboard

### Overview
┌─────────────────────────────────────┐
│ Total Cloud Spend (MTD)             │
│ $1,234,567  ▲12% MoM  ⚠️ 5% over    │
└─────────────────────────────────────┘

### Breakdown
┌──────────────┬──────────────┬────────┐
│ Service      │ Spend        │ % Total│
├──────────────┼──────────────┼────────┤
│ Compute      │ $500K        │  40%   │
│ Database     │ $300K        │  24%   │
│ Storage      │ $200K        │  16%   │
│ Network      │ $150K        │  12%   │
│ Other        │ $84K         │   8%   │
└──────────────┴──────────────┴────────┘

### Top 5 Cost Drivers (Projects)
1. ML Training Platform: $250K (20%)
2. Production API: $200K (16%)
3. Data Pipeline: $150K (12%)
4. Analytics Platform: $120K (10%)
5. Customer Portal: $100K (8%)

### Optimization Tracker
- Active Initiatives: 12
- MTD Savings: $45K
- Projected Annual: $540K
```

### TCO Analysis Framework

```markdown
# Total Cost of Ownership: Cloud vs On-Premises

## On-Premises TCO Components

### Capital Expenses (CapEx)
1. **Hardware**
   - Servers: $5,000-10,000 per server × quantity
   - Storage: $100-500 per TB (SAN/NAS)
   - Networking: switches, routers, firewalls
   - Lifespan: 3-5 years (depreciation)

2. **Data Center**
   - Construction/lease: $1,000-3,000 per kW capacity
   - Power distribution (UPS, PDU)
   - Cooling systems (HVAC)
   - Physical security

3. **Software Licenses**
   - Hypervisor (VMware, RHEL)
   - Operating systems
   - Database licenses (Oracle, SQL Server)
   - Monitoring tools

### Operating Expenses (OpEx)
1. **Personnel**
   - System admins: $80K-120K/year each
   - Network engineers: $90K-130K/year
   - Security team: $100K-150K/year
   - 24/7 coverage multiplier: 4-5 FTEs per role

2. **Facilities**
   - Power: $0.10-0.15 per kWh × consumption
   - Cooling: 1.5-2x power consumption (PUE)
   - Space: $100-300 per sq ft per year
   - Internet bandwidth: $10-50 per Mbps

3. **Maintenance & Support**
   - Hardware maintenance: 15-20% of hardware cost/year
   - Software support: 20-25% of license cost/year
   - Spare parts inventory

4. **Refresh Cycle**
   - Every 3-5 years: replace hardware
   - Migration costs (planning, execution)

## Cloud TCO Components

### Direct Costs
1. **Compute**: instances, containers, serverless
2. **Storage**: object, block, file storage
3. **Network**: data transfer, load balancers
4. **Database**: managed database services
5. **Services**: AI/ML, analytics, etc.

### Indirect Costs
1. **Personnel** (reduced vs on-prem)
   - Cloud architects: $120K-180K/year
   - DevOps engineers: $110K-160K/year
   - Fewer ops staff needed (managed services)

2. **Tools & Training**
   - Cost management tools: $5K-50K/year
   - Training & certifications: $2K-5K per person
   - Third-party monitoring (Datadog, New Relic)

3. **Data Transfer**
   - Egress costs (often forgotten!)
   - Cross-region transfers

## TCO Comparison Example

### Scenario: 100 VMs, 500 TB storage, 3-year period

#### On-Premises
```
CapEx:
- Servers (100 × $8K): $800K
- Storage (500 TB × $300): $150K
- Networking: $100K
- Data center (allocated): $200K
Total CapEx: $1,250K

OpEx (annual):
- Personnel (10 FTEs × $100K): $1,000K
- Power (200 kW × $0.12 × 8760 hrs): $210K
- Cooling (200 kW × 1.5 × $0.12 × 8760): $315K
- Maintenance (15% of hardware): $157K
- Software licenses: $100K
Annual OpEx: $1,782K
3-year OpEx: $5,346K

Total 3-year TCO: $6,596K
Average annual: $2,199K

#### Cloud (AWS)
```
Monthly costs:
- Compute (100 × m5.2xlarge RIs): $24K
- Storage (500 TB S3 + EBS): $15K
- Network: $5K
- Managed services: $6K
Total monthly: $50K

Annual: $600K
3-year total: $1,800K
Average annual: $600K

Savings vs on-prem: $4,796K (73% reduction!)
```

**Why cloud wins**:
- No upfront CapEx (cash flow)
- Reduced staffing (managed services)
- No data center costs
- Pay only для actual usage
- Faster time to market (agility value)

**When on-prem might win**:
- Massive scale (100,000+ servers) with consistent load
- Special hardware requirements (GPU farms для years)
- Regulatory constraints (air-gapped environments)
- Already own data center with sunk costs
```

### Advanced Cost Optimization Techniques

```markdown
# Enterprise Cost Optimization Playbook

## 1. Autoscaling Strategies

### Horizontal Pod Autoscaling (Kubernetes)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scale down
      policies:
      - type: Percent
        value: 50  # Max 50% scale down at once
        periodSeconds: 60
```

**Impact**: Handle 10x traffic spikes без overprovisioning
**Savings**: 40-60% на non-peak hours

## 2. Spot Instance Strategies

### Diversification Pattern
```python
# AWS Spot Fleet Request
spot_fleet_config = {
    'AllocationStrategy': 'lowestPrice',  # or 'diversified'
    'IamFleetRole': 'arn:aws:iam::123:role/spot-fleet',
    'LaunchSpecifications': [
        # Multiple instance types для availability
        {'InstanceType': 'm5.large', 'SpotPrice': '0.05'},
        {'InstanceType': 'm5a.large', 'SpotPrice': '0.05'},
        {'InstanceType': 'm5n.large', 'SpotPrice': '0.05'},
        {'InstanceType': 'm4.large', 'SpotPrice': '0.05'},
    ],
    'TargetCapacity': 100,
    'SpotPrice': '0.05',  # Max price (on-demand price)
}

# Fallback to On-Demand if spot unavailable
'OnDemandTargetCapacity': 10,  # Minimum guaranteed capacity
```

## 3. Reserved Instance Optimization

### RI Portfolio Management
```markdown
Strategy: Tiered RI commitments

1. **Baseline (3-year All Upfront)**: 50% of minimum usage
   - Deepest discounts
   - Lock in for stable workloads

2. **Buffer (1-year Partial Upfront)**: 30% of average usage
   - Moderate discounts
   - More flexibility

3. **Flex (Savings Plan)**: 10% of average usage
   - Covers growth
   - Instance family flexible

4. **On-Demand**: 10% for spikes
   - Highest cost but necessary

Example:
1000 instance-hours/month average usage
- 500 hrs: 3-year RIs (75% discount) = $12.50/hr → $6,250
- 300 hrs: 1-year RIs (40% discount) = $30/hr → $9,000
- 100 hrs: Savings Plan (50% discount) = $25/hr → $2,500
- 100 hrs: On-Demand (0% discount) = $50/hr → $5,000
Total: $22,750/month

vs All On-Demand: $50,000/month
Savings: 54% ($27,250/month)
```

## 4. Storage Optimization

### S3 Lifecycle + Intelligent-Tiering
```json
{
  "Rules": [
    {
      "Id": "Move to IA after 30 days",
      "Filter": {"Prefix": "logs/"},
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        },
        {
          "Days": 365,
          "StorageClass": "DEEP_ARCHIVE"
        }
      ],
      "Expiration": {
        "Days": 730  # Delete after 2 years
      }
    },
    {
      "Id": "Intelligent-Tiering for unknown patterns",
      "Filter": {"Prefix": "data/"},
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 0,
          "StorageClass": "INTELLIGENT_TIERING"
        }
      ]
    }
  ]
}
```

**Impact**: 70-90% reduction на archival data

## 5. Commitment Laddering

### Avoiding Over-Commitment
```markdown
Problem: 3-year RI, business pivots after 1 year → stuck with unused commitment

Solution: Ladder RIs across time periods

Year 1: Buy 3-year RI для 33% of usage
Year 2: Buy another 3-year RI для 33%
Year 3: Buy another 3-year RI для 33%

Result: Every year, only 33% of RIs expire (vs 100%), more flexibility
```

---

**Все экономические модели, калькуляторы и отчеты сохраняются в Markdown на русском языке.**
