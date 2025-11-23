---
name: cloud-pricing-strategy
description: Комплексная методология разработки ценовой стратегии для облачных сервисов, включая модели ценообразования, competitive pricing, и value-based pricing. Use when developing pricing strategy, analyzing pricing models, or optimizing revenue.
---

# Cloud Pricing Strategy

## When to Use This Skill

Используйте этот скилл когда вам необходимо:
- Разработать ценовую стратегию для нового облачного сервиса
- Проанализировать и оптимизировать существующие цены
- Определить optimal pricing model (usage-based, tiered, hybrid)
- Провести competitive pricing analysis
- Разработать packaging strategy (free tier, paid tiers, enterprise)
- Рассчитать unit economics и optimize для profitability
- Ответить на competitive pricing pressure

## Core Concepts

### 1. Cloud Pricing Models

#### Usage-Based Pricing (Pay-as-you-go)
```
Definition: Клиент платит только за фактическое использование ресурсов

Characteristics:
├── No upfront commitment
├── Granular billing (per hour, per GB, per API call)
├── Variable monthly cost
├── Lower barrier to entry
└── Aligns cost with value (usage)

Typical Metrics:
├── Compute: $/hour (VM), $/second (Serverless)
├── Storage: $/GB-month (Object storage), $/IOPS (Block storage)
├── Network: $/GB (Data transfer), $/hour (Load balancer)
├── Database: $/hour (Instance) + $/GB (Storage) + $/million IOPS
├── API Services: $/1000 requests или $/million API calls
└── AI/ML: $/training hour, $/inference request

Advantages:
✅ Easy to get started (no commitment)
✅ Fair (pay for what you use)
✅ Scales up and down automatically
✅ Good for variable workloads

Disadvantages:
❌ Unpredictable costs (hard to budget)
❌ Bill shock possible (runaway usage)
❌ Complex pricing (many SKUs)
❌ Lower revenue predictability

Best For:
- Developers, startups (experimentation)
- Variable workloads (dev/test, seasonal spikes)
- New customers (low friction entry)

Examples:
- AWS EC2 On-Demand: $0.0416/hour (t3.medium)
- GCP Cloud Functions: $0.40/million invocations
- Azure Blob Storage: $0.018/GB-month
```

#### Committed Use Discounts (Reserved/Savings Plans)
```
Definition: Клиент commits к определенному уровню использования за 1-3 года в exchange за discount

Models:

1. Reserved Instances (Traditional)
   - Commit: Specific instance type, region, OS
   - Term: 1-year (30% off) или 3-year (50%+ off)
   - Payment: All upfront, partial upfront, или no upfront
   - Flexibility: Low (locked to instance type)

2. Savings Plans (Flexible)
   - Commit: Dollar amount per hour (e.g., $10/hour)
   - Term: 1-year или 3-year
   - Flexibility: High (any instance family, region)
   - Discount: Similar to reserved (30-50%)

3. Committed Use (Google Model)
   - Commit: vCPU and memory amount
   - Term: 1-year (25% off) или 3-year (52% off)
   - Flexibility: Medium (any VM using committed resources)

Advantages:
✅ Significant cost savings (30-70% discounts)
✅ Predictable costs (known commitment)
✅ Revenue predictability (for provider)
✅ Customer lock-in (reduces churn)

Disadvantages:
❌ Commitment required (risk if needs change)
❌ Complexity (which model to choose?)
❌ Underutilization risk (paying for unused)
❌ Overprovisioning (buy more than needed for safety)

Best For:
- Steady-state workloads (production apps)
- Enterprise customers (budgeting, cost optimization)
- Mature businesses (predictable usage)

Pricing Example:
├── On-Demand: $1.00/hour
├── 1-Year Reserved: $0.70/hour (30% off)
├── 3-Year Reserved: $0.50/hour (50% off)
└── Savings: $4,380/year (1-year) или $21,900/year (3-year) per instance
```

#### Freemium Model
```
Definition: Бесплатный tier для привлечения пользователей, платные tiers для monetization

Structure:

Free Tier (Generous enough to be useful):
├── Compute: 100-200 hours/month (1-2 small instances)
├── Storage: 5-10 GB
├── Bandwidth: 10-100 GB egress
├── Databases: 1 shared instance или limited IOPS
├── API Calls: 100K-1M per month
└── Support: Community only, no SLAs

Paid Tiers (Progressive value):
├── Starter: $20-50/month (individual developers)
├── Professional: $100-500/month (small teams)
├── Business: $500-2000/month (growing companies)
└── Enterprise: $5K+/month (large organizations, custom)

Conversion Triggers:
├── Usage limits (hit free tier caps)
├── Team features (collaboration needs)
├── Support needs (SLAs, phone support)
├── Compliance (SOC 2, HIPAA for paid only)
└── Advanced features (priority queues, better performance)

Advantages:
✅ Low friction acquisition (no credit card)
✅ Product-led growth (try before buy)
✅ Viral potential (free users share)
✅ Large user base (lots of free users)

Disadvantages:
❌ Low conversion (typically 2-5% free to paid)
❌ Support costs (free users need help too)
❌ Abuse risk (free tier exploitation)
❌ Free tier optimization (hard to balance)

Best For:
- Developer tools (APIs, databases, platforms)
- High volume, low-touch products
- Viral/network effect products
- Building community and brand

Examples:
- MongoDB Atlas: Free M0 cluster (512MB RAM, 5GB storage)
- Vercel: Free tier (100GB bandwidth, unlimited sites)
- Netlify: Free tier (100GB bandwidth, 300 build minutes)
```

#### Enterprise Custom Pricing
```
Definition: Negotiated contracts для large customers с custom terms, discounts, и services

Structure:

Base Contract:
├── Minimum Annual Commitment: $100K-$100M+
├── Term: Typically 1-3 years, sometimes 5+ years
├── Discount: 30-70% off list prices (volume-based)
├── Payment Terms: Annual prepay, quarterly, или monthly
└── True-up: Reconcile actual usage vs commitment

Additional Terms:
├── Support: Dedicated TAM (Technical Account Manager)
├── SLAs: Custom uptime guarantees (99.95%, 99.99%, 99.999%)
├── Security: Private审计, dedicated environments
├── Credits: Migration assistance, training, co-marketing
├── Flexibility: Rollover credits, service swaps, multi-year pools
└── Governance: Quarterly business reviews, executive sponsorship

Pricing Models:
├── Volume Discounts: Tiered based on spend ($0-100K: 0%, $100K-1M: 20%, $1M+: 40%)
├── Committed Spend: Commit $X annually, get Y% discount across all services
├── Reserved Capacity: Reserve specific resources at deep discount
└── Custom SKUs: Bundled services at special pricing

Advantages:
✅ Massive deals (large ACV)
✅ Multi-year revenue lock-in
✅ Deep customer relationship
✅ Reference customer (logo, case study)

Disadvantages:
❌ Long sales cycles (6-12 months)
❌ Complex negotiations (legal, procurement)
❌ Custom terms (hard to scale)
❌ Lower margins (deep discounts)

Best For:
- Fortune 500 enterprises
- Mission-critical workloads
- Large-scale migrations (on-prem to cloud)
- Strategic accounts (industry leaders)

Example Deal Structure:
├── Year 1-3 Commitment: $10M annually ($30M total)
├── Discount: 45% off list prices
├── Support: Dedicated TAM + 24/7 premium support included
├── SLA: 99.95% uptime с financial penalties
├── Credits: $500K migration assistance
├── Flexibility: Quarterly true-up, service swaps allowed
└── Renewal: 60-day notice, price lock for 3 years
```

### 2. Pricing Psychology для Cloud

```
Anchoring Effect:
├── Show higher-priced tier first (Enterprise → Pro → Starter)
├── Makes middle tier seem reasonable
├── "Save 50% with annual billing" (anchor to monthly price)

Decoy Effect:
├── Add "decoy" tier to make target tier attractive
├── Example: Starter $49, Pro $99, Business $199 (Pro is sweet spot)
├── Business tier makes Pro seem like better value

Charm Pricing:
├── $99 feels significantly cheaper than $100
├── Use in self-service tiers (B2C psychology)
├── Avoid in enterprise (looks unprofessional)

Value-Based Framing:
├── "$0.10 per 1,000 API calls" vs "$100 per million calls" (same price, different perception)
├── Emphasize total savings vs competitor ($X saved annually)
├── ROI messaging (X% faster, Y% cost reduction)

Free → Paid Psychology:
├── Free tier builds habit, switching cost
├── When user hits limit, already invested (sunk cost)
├── Gentle nudge ("Upgrade to continue", not "Pay now")
├── Show value gained, not features restricted

Loss Aversion:
├── "Don't lose your data" (backup messaging)
├── "Avoid downtime" (uptime, reliability messaging)
├── Trial ending messages (fear of losing access)

Social Proof:
├── "Used by 50,000+ companies" (popularity)
├── "Trusted by [Fortune 500 logo]" (credibility)
├── "Rated 4.8/5 stars" (quality signal)
```

### 3. Competitive Pricing Analysis

```markdown
## Pricing Comparison Matrix

### Compute (VMs) - Как пример

| Provider | Instance Type | vCPU | RAM | Price/Hour | Price/Month | Notes |
|----------|---------------|------|-----|------------|-------------|-------|
| AWS | t3.medium | 2 | 4GB | $0.0416 | ~$30 | Burstable |
| Azure | B2s | 2 | 4GB | $0.0416 | ~$30 | Burstable |
| GCP | e2-medium | 2 | 4GB | $0.0335 | ~$24 | Sustained use discount auto-applied |
| DigitalOcean | Basic Droplet | 2 | 4GB | $0.0268 | $18 | Simple pricing |
| **Us** | **Standard-2** | **2** | **4GB** | **$0.0300** | **$22** | **Competitive positioning** |

### Storage (Object Storage)

| Provider | Storage | Price/GB-month | Egress | Price/GB | Notes |
|----------|---------|----------------|--------|----------|-------|
| AWS S3 | Standard | $0.023 | First 10TB | $0.09 | Industry standard |
| Azure Blob | Hot | $0.018 | First 10TB | $0.087 | Slightly cheaper |
| GCP Cloud Storage | Standard | $0.020 | Worldwide | $0.12 | Higher egress cost |
| **Us** | **Hot** | **$0.020** | **First 10TB** | **$0.08** | **Match GCP storage, beat egress** |

### Key Insights:

Price Positioning:
├── Compute: 10-30% below AWS/Azure, similar to GCP
├── Storage: Competitive on storage cost, better egress pricing
├── Databases: Premium pricing (justify with performance, support)
├── Networking: Significantly better egress pricing (differentiation)

Competitive Strategy:
├── Lead with cost savings (vs AWS/Azure)
├── Emphasize simplicity (vs AWS complex pricing)
├── Premium on differentiated services (vs commodity compete)
└── Match GCP on data analytics (can't be much pricier)
```

### 4. Packaging Strategy

```
Packaging Framework для Cloud Services:

Good/Better/Best Model:

Starter Tier (Good):
├── Target: Individual developers, hobby projects
├── Price: $20-50/month
├── Limits: 1 project, 1 environment, community support
├── Features: Core features only
└── Goal: Acquisition, habit formation

Professional Tier (Better) - **RECOMMENDED BADGE**:
├── Target: Small teams, growing startups
├── Price: $100-500/month (sweet spot для conversion)
├── Limits: Unlimited projects, 3 environments, email support
├── Features: Core + team collaboration + basic integrations
├── Highlighted: "Most popular", "Best value"
└── Goal: Primary monetization tier

Business Tier (Best):
├── Target: Established companies, larger teams
├── Price: $500-2000/month
├── Limits: Unlimited everything, priority support
├── Features: Everything + advanced features + compliance
├── Value-adds: Dedicated CSM, training credits, SLAs
└── Goal: Expansion revenue, upsell path

Enterprise Tier (Custom):
├── Target: Fortune 500, mission-critical workloads
├── Price: Custom (typically $5K-$100K+/month)
├── Limits: Custom everything
├── Features: Everything + custom integrations + on-prem options
├── Value-adds: Dedicated TAM, custom SLAs, co-innovation
└── Goal: Strategic accounts, high ACV

Feature Allocation Guidelines:
├── Core Features: Available in all tiers (80% of value)
├── Team Features: Pro and above (collaboration, permissions)
├── Advanced Features: Business and above (integrations, automation)
├── Enterprise Features: Enterprise only (SSO, SAML, audit logs, compliance)
└── Support: Tiered (Community → Email → Phone → Dedicated)

Add-Ons (Optional purchases):
├── Additional resources (storage, bandwidth)
├── Premium support (upgrade support tier)
├── Professional services (migration, training)
├── Compliance certifications (HIPAA BAA, SOC 2 report)
└── Extended data retention (longer than standard)
```

### 5. Unit Economics

```
Cloud Unit Economics Framework:

Revenue Side:
├── ARPU (Average Revenue Per User)
│   ├── SMB: $50-200/month
│   ├── Mid-Market: $500-$5K/month
│   └── Enterprise: $10K-$100K+/month
├── LTV (Lifetime Value)
│   └── LTV = ARPU × Gross Margin × (1 / Monthly Churn Rate)
│   └── Example: $200 ARPU × 70% margin × (1 / 3% churn) = $4,667 LTV
└── Expansion Revenue
    └── Net Revenue Retention: 110-140% (healthy SaaS)

Cost Side:
├── COGS (Cost of Goods Sold)
│   ├── Infrastructure: AWS/GCP costs (50-70% of COGS)
│   ├── Bandwidth: Data transfer costs
│   ├── Support: Customer support team (allocated)
│   └── Target COGS: 20-30% of revenue (healthy margin)
├── CAC (Customer Acquisition Cost)
│   ├── Marketing spend: Ads, content, events
│   ├── Sales cost: Sales team, commissions
│   ├── By channel: PLG ($50-200), Sales-led ($200-2K), Enterprise ($5K-50K)
│   └── Target: CAC payback < 12 months
└── Operational Costs
    ├── R&D: Engineering, product teams
    ├── G&A: General & administrative overhead
    └── Target: 40-50% of revenue (scale with growth)

Key Metrics:
├── Gross Margin: (Revenue - COGS) / Revenue
│   └── Target: 70-80% (healthy SaaS)
├── LTV/CAC Ratio: Lifetime Value / Customer Acquisition Cost
│   └── Target: 3:1 или выше (sustainable growth)
├── CAC Payback: Months to recover acquisition cost
│   └── Target: <12 months (capital efficient)
├── Rule of 40: (Revenue Growth % + Profit Margin %)
│   └── Target: >40% (good SaaS company)
└── Magic Number: (Quarterly Revenue Growth × 4) / Prior Quarter S&M Spend
    └── Target: >0.75 (efficient growth)

Pricing Optimization for Unit Economics:
├── Raise prices: Increase revenue without increasing COGS (but may decrease conversion)
├── Reduce COGS: Optimize infrastructure efficiency (reserved instances, autoscaling)
├── Improve conversion: Better onboarding, features → increase paid users from same traffic
├── Reduce churn: Better support, reliability → increase LTV
└── Expand ACV: Upsells, cross-sells → increase ARPU from existing customers
```

## Resources и Templates

См. директорию `references/` для:
- Pricing Strategy Template (comprehensive pricing strategy doc)
- Unit Economics Calculator (Excel модель для расчета LTV, CAC, margins)
- Competitive Pricing Analysis Template (framework для анализа)
- Pricing Experiment Framework (A/B testing pricing)

См. директорию `assets/` для:
- Pricing Comparison Matrix (визуальное сравнение с конкурентами)
- Packaging Model Template (Good/Better/Best структура)
- Price Sensitivity Analysis (willingness to pay research)

## Сохранение результатов

Сохраняйте все pricing стратегии в **Markdown на русском**:

```markdown
# Ценовая Стратегия: [Service Name]

## Метаданные
- **Сервис**: [Name]
- **Дата**: YYYY-MM-DD
- **Владелец**: [Product Marketing]
- **Статус**: [Draft/Review/Approved]
- **Эффективная дата**: [Launch date]

## Исполнительное резюме
[Pricing model, rationale, competitive positioning]

## 1. Pricing Model
[Usage-based, tiered, freemium, enterprise]

## 2. Price Points
[Specific prices для each tier/unit]

## 3. Competitive Analysis
[Comparison vs AWS, Azure, GCP]

## 4. Packaging
[Tiers, features, limits]

## 5. Unit Economics
[COGS, CAC, LTV, margins, targets]

## 6. Go-To-Market
[How to sell it, messaging, positioning]

## 7. Success Metrics
[Conversion, ARPU, churn, NRR targets]

## 8. Risks & Mitigation
[Price sensitivity, competitive response, etc.]

## Приложения
[Detailed calculations, models, research]
```

Сохраняйте в: `~/cmo-output/pricing/[service-name]-pricing-strategy-YYYY-MM-DD.md`
