---
name: cloud-competitive-analysis
description: Методология комплексного конкурентного анализа облачных провайдеров (AWS, Azure, GCP, Oracle). Use when analyzing competitors, preparing battlecards, conducting win/loss analysis, or developing competitive positioning.
---

# Cloud Competitive Analysis

## When to Use This Skill

Используйте этот скилл когда вам необходимо:
- Провести глубокий анализ конкурентов (AWS, Azure, GCP, Oracle)
- Подготовить competitive battlecards для sales team
- Проанализировать win/loss interviews и выявить patterns
- Разработать competitive positioning и differentiation strategy
- Ответить на competitive threat (новый feature, price drop, customer win)
- Подготовить конкурентную часть для board presentation или strategy doc

## Core Concepts

### 1. Competitive Intelligence Framework

#### Sources of Intelligence
```
Primary Sources (Публичные, Этичные):

Official Sources:
├── Earnings calls (quarterly transcripts, guidance)
├── Investor presentations (strategy reveals)
├── Blog posts (feature announcements)
├── Documentation (technical capabilities)
├── Pricing pages (current pricing)
├── Press releases (partnerships, customers)
└── Executive social media (LinkedIn, Twitter)

Third-Party Analysis:
├── Analyst reports (Gartner Magic Quadrant, Forrester Wave)
├── Market research (Synergy Research, Canalys)
├── Industry publications (The Register, InfoQ, TechCrunch)
├── Financial analysts (Bank reports on public companies)
└── Benchmark studies (performance comparisons)

Customer Intelligence:
├── Win/loss interviews (why chose us/competitor)
├── Sales feedback (objections, competitive claims)
├── Review sites (G2, TrustRadius, Gartner Peer Insights)
├── Community forums (Reddit, Hacker News sentiment)
├── Support tickets (migration inquiries, issues)
└── Conference conversations (booth visits, hallway tracks)

Technical Intelligence:
├── Hands-on testing (trial accounts, POCs)
├── Performance benchmarks (speed, latency tests)
├── Status pages (uptime, incidents)
├── API testing (capabilities, limitations)
├── Documentation analysis (feature completeness)
└── Job postings (hiring signals, tech stack)
```

#### Competitive Profile Template
```markdown
# [Competitor Name] Competitive Profile

## Company Overview
- **Founded**: [Year]
- **Headquarters**: [Location]
- **CEO**: [Name]
- **Employees**: [Count]
- **Cloud Revenue**: [Annual, если public]
- **Market Share**: [% of cloud infrastructure market]

## Strategic Positioning
- **Target Market**: [Enterprise/Mid-Market/SMB/Developer]
- **Primary Value Prop**: [Core message]
- **Differentiation**: [Key differentiators]
- **Weaknesses**: [Known gaps/issues]

## Product Portfolio

### Compute
| Service | Our Equivalent | Comparison |
|---------|---------------|------------|
| [EC2] | [VM Service] | ✅ Similar, ❌ They have spot instances |
| [Lambda] | [Functions] | ✅ Better cold start, ❌ Fewer triggers |

### Storage
[Similar breakdown]

### Databases
[Similar breakdown]

### Networking
[Similar breakdown]

### AI/ML
[Similar breakdown]

## Pricing Strategy
- **Model**: [Pay-as-you-go, Reserved, Spot]
- **Comparison**: [X% more/less expensive than us]
- **Tactics**: [Aggressive discounting, Enterprise agreements]

## Go-To-Market
- **Sales Motion**: [PLG/Sales-Led/Hybrid]
- **Partner Ecosystem**: [ISVs, SIs, Resellers]
- **Marketing Tactics**: [Content, Events, Analyst relations]
- **Developer Relations**: [Community size, GitHub activity]

## Recent Developments (Last 90 Days)
- [Date]: [Feature launch, partnership, pricing change]
- [Date]: [Customer win, market expansion]
- [Impact on us]: [Analysis of threat/opportunity]

## Competitive Response
- **When to compete head-on**: [Scenarios]
- **When to differentiate**: [Scenarios]
- **When to avoid**: [Scenarios]

## Battlecard Key Points
- **Why customers choose them**: [Top 3 reasons]
- **Why customers choose us**: [Top 3 reasons]
- **Objection handling**: [Common objections, responses]

## Sources
- [Documentation, pricing pages, analyst reports]

**Last Updated**: YYYY-MM-DD
**Next Review**: YYYY-MM-DD
```

### 2. AWS Competitive Analysis

```markdown
# AWS (Amazon Web Services) - Market Leader

## Strategic Position
- **Market Share**: 32-34% (абсолютный лидер)
- **Strengths**: First-mover, widest portfolio, enterprise trust, innovation velocity
- **Weaknesses**: Complex pricing, support quality, legacy baggage, learning curve

## Key Services to Monitor
├── Compute: EC2, Lambda, ECS, EKS, Fargate, Batch
├── Storage: S3, EBS, EFS, Glacier, Storage Gateway
├── Databases: RDS, Aurora, DynamoDB, Redshift, Neptune, DocumentDB
├── Analytics: Athena, EMR, Kinesis, QuickSight, Lake Formation
├── AI/ML: SageMaker, Rekognition, Comprehend, Lex, Polly
├── Networking: VPC, CloudFront, Route 53, Direct Connect, Transit Gateway
└── Security: IAM, KMS, Secrets Manager, WAF, Shield, GuardDuty

## Pricing Strategy
- Base: Most expensive на list price (premium brand)
- Discounts: Reserved Instances (1-year: 30%, 3-year: 50%+)
- Savings Plans: Flexible committed use (similar discounts)
- Spot Instances: 70-90% discount (interruptible workloads)
- Egress: High data transfer fees ($0.09/GB)

## When We Win vs AWS
├── Price sensitivity (40% cost savings message resonates)
├── Simplicity needed (developers overwhelmed by AWS complexity)
├── Support quality concerns (premium support expensive, inconsistent)
├── Multi-cloud strategy (avoid AWS lock-in)
└── Startups (AWS credits running out, need better economics)

## When We Lose vs AWS
├── Enterprise safety (CIO says "nobody gets fired for choosing AWS")
├── Service breadth (need niche service only AWS has)
├── Ecosystem (ISV только поддерживает AWS)
├── Existing footprint (already heavily invested in AWS)
└── Talent availability (more engineers know AWS)

## Response Playbook
- **On AWS price drop**: Emphasize total cost of ownership (support, egress, hidden fees)
- **On new AWS feature**: Evaluate demand, roadmap match, alternative approach messaging
- **On AWS customer win**: Analyze why (was it competitive deal?), learn, adjust
- **On AWS outage**: Don't gloat, subtle messaging на reliability и multi-cloud
```

### 3. Azure Competitive Analysis

```markdown
# Microsoft Azure - Strong #2

## Strategic Position
- **Market Share**: 21-23% (сильный второй)
- **Strengths**: Microsoft relationship, hybrid (Azure Stack/Arc), enterprise sales, Office 365 integration
- **Weaknesses**: Reliability issues, Linux/OSS perception, complex licensing

## Enterprise Bundling Strategy
- **Microsoft 365 + Azure**: Attractive bundles для enterprise
- **Enterprise Agreements (EA)**: Volume discounts, committed spend
- **Azure Hybrid Benefit**: Use on-prem Windows licenses in cloud
- **Dev/Test Pricing**: Lower rates for non-production

## When We Win vs Azure
├── Reliability concerns (history of outages)
├── Non-Microsoft shops (Linux-first, open-source culture)
├── Licensing complexity (customers frustrated with EA negotiations)
├── Better technical depth (perceived as more mature on specific services)
└── Pricing transparency (simpler than Azure complex SKU matrix)

## When We Lose vs Azure
├── Microsoft footprint (Office 365, Windows Server installed base)
├── Hybrid requirements (Azure Stack/Arc unique capabilities)
├── Enterprise agreements (bundled pricing impossible to match)
├── Salesforce size (Microsoft has largest enterprise sales team)
└── Vertical industry clouds (Healthcare, Financial Services specific)

## Response Playbook
- **On Azure bundling**: Emphasize total solution cost, avoid lock-in messaging
- **On hybrid cloud**: Position multi-cloud approach, Kubernetes портability
- **On industry clouds**: Highlight flexibility, best-of-breed approach
```

### 4. GCP Competitive Analysis

```markdown
# Google Cloud Platform - Fast-Growing #3

## Strategic Position
- **Market Share**: 10-11% (третье место, быстрый рост)
- **Strengths**: Data/AI/ML, Kubernetes (created), network performance, open-source leadership
- **Weaknesses**: Smaller ecosystem, enterprise sales execution, trust issues (product sunset reputation)

## Technical Differentiation
- **BigQuery**: Industry-leading data warehouse (serverless, fast, cost-effective)
- **Kubernetes**: Created K8s, GKE most mature managed K8s
- **Network**: Google's global backbone (lower latency)
- **TPUs**: Custom AI chips (TensorFlow acceleration)
- **Pricing**: Simpler, sustained use discounts automatic

## When We Win vs GCP
├── Enterprise sales (GCP weak in complex sales cycles)
├── Service breadth (GCP has fewer services than AWS/Azure/us)
├── Trust concerns ("Will Google sunset this?")
├── Support maturity (less enterprise support experience)
└── Regional coverage (fewer regions than competitors)

## When We Lose vs GCP
├── Data/Analytics workloads (BigQuery unmatched)
├── AI/ML focus (TensorFlow, Vertex AI, TPUs)
├── Kubernetes expertise (developers trust Google for K8s)
├── Pricing simplicity (easier to estimate costs)
└── Open source alignment (CNCF, OSS community perception)

## Response Playbook
- **On BigQuery wins**: Position our data warehouse + best-of-breed integrations
- **On K8s claims**: Emphasize our K8s expertise, contributions, managed service
- **On pricing**: Match transparency, highlight areas where we're more cost-effective
```

### 5. Competitive Battlecard Structure

```markdown
# [Service Name] Battlecard

## Elevator Pitch (30 seconds)
[Concise value prop vs competition]

## Competitive Landscape
| Provider | Product | Strengths | Weaknesses |
|----------|---------|-----------|------------|
| AWS | [Service] | [Strength] | [Weakness] |
| Azure | [Service] | [Strength] | [Weakness] |
| GCP | [Service] | [Strength] | [Weakness] |
| Us | [Service] | [Strength] | [Weakness] |

## Key Differentiators
1. **[Differentiator #1]**
   - What: [Specific feature/capability]
   - Why it matters: [Customer benefit]
   - Proof: [Benchmark, testimonial, metric]

2-3. [Additional differentiators]

## Pricing Comparison
| Provider | Pricing | Example Monthly Cost |
|----------|---------|---------------------|
| Us | $X | $XXX |
| AWS | $Y | $YYY (+20%) |
| Azure | $Z | $ZZZ (+15%) |
| GCP | $A | $AAA (+10%) |

## Objection Handling

**"AWS is the safer choice"**
Response: "While AWS is the market leader, consider total cost and complexity. Our customers report 40% cost savings and 50% faster developer productivity. For [customer segment], innovation and agility matter more than playing it safe. [Customer name] chose us for precisely this reason."

**"You don't have [specific AWS feature]"**
Response: "We solve [problem] differently. Instead of [AWS approach], we provide [our approach], which gives you [benefit]. This is actually better for [use case] because [reason]. If [feature] is critical, we're adding it in Q[X], but let's explore if our approach meets your needs first."

[Additional objections...]

## Competitive Win Stories
- **[Company name]**: Migrated from AWS, saved $2M annually, 3x faster deploys
- **[Company name]**: Chose us over Azure, cited simplicity and support quality
- **[Company name]**: Multi-cloud with us+AWS, using us for [workload], AWS for [other workload]

## Discovery Questions
- "What cloud providers are you currently evaluating?"
- "What's most important: cost, performance, simplicity, or support?"
- "Have you experienced any frustrations with [current provider]?"
- "What workloads are you looking to migrate/deploy?"

## Demo Key Messages
1. **Speed**: Show fast deployment (compare to AWS 15 steps)
2. **Simplicity**: Highlight intuitive UI vs AWS console complexity
3. **Performance**: Live benchmark comparison
4. **Cost**: Show transparent pricing vs AWS estimator confusion
5. **Support**: Mention included 24/7 support vs AWS premium support cost

## Resources
- Demo video: [URL]
- Case studies: [URLs]
- Pricing calculator: [URL]
- Technical comparison: [URL]
- Sales contact: [PMM name/email]

**Last Updated**: YYYY-MM-DD
```

### 6. Win/Loss Analysis Framework

```markdown
# Win/Loss Analysis Program

## Interview Structure

### Win Interview (30-45 minutes)

**Opening (5 min)**
- Explain purpose: Learning, not celebration
- Assure confidentiality
- Request candor

**Decision Process (10 min)**
- What triggered evaluation?
- Who was involved? (developer, architect, CTO, CFO, procurement)
- What were evaluation criteria? (price, features, support, brand)
- Which providers were finalists? (us vs AWS vs Azure vs GCP)
- How long was sales cycle? (weeks, months)

**Competitive Evaluation (15 min)**
- How did we compare to [AWS/Azure/GCP]?
- What were our strengths?
- What were our weaknesses?
- What almost made you choose competitor?
- How did pricing compare? (specific numbers)
- How did sales experience compare?

**Decision Factors (10 min)**
- What was #1 reason you chose us? (single biggest factor)
- What were other key factors? (rank top 5)
- Any concerns you had to overcome?
- What would have made decision easier/faster?

**Closing (5 min)**
- Any advice for us?
- Anything we missed?

### Loss Interview (Similar structure)

Focus on:
- Why did you choose [competitor]?
- What did they do better?
- What could we have done differently?
- Would you reconsider in future? Under what circumstances?

## Analysis Framework

### Quantitative Analysis

Win Reasons (Aggregate):
1. Price/TCO: 35% of wins
2. Technical capabilities: 28%
3. Support quality: 15%
4. Ease of use: 12%
5. Sales experience: 10%

Loss Reasons (Aggregate):
1. Price too high: 40% of losses
2. Missing feature: 25%
3. Brand/trust concerns: 15%
4. Competitor relationship: 12%
5. Sales execution: 8%

Competitor Breakdown:
- Lost to AWS: 45% (reasons: breadth, brand, ecosystem)
- Lost to Azure: 30% (Microsoft relationship, bundling)
- Lost to GCP: 15% (price, data/AI capabilities)
- Lost to others: 10%

### Qualitative Insights

Themes (Quarterly Trends):
├── ↑ Pricing sensitivity (economic uncertainty)
├── ↑ AI/ML capabilities importance (market trend)
├── ↓ Multi-cloud interest (consolidation)
├── → Security/compliance (table stakes)
└── ↑ Support responsiveness (critical differentiator)

### Action Items

Product:
- Develop [missing feature] (25% of losses)
- Improve [service] performance
- Add [integration] requested

Pricing:
- Competitive response for [segment]
- TCO calculator improvements
- Migration credit program

Marketing:
- Update competitive comparison page
- Create case studies in [industry]
- Improve brand awareness via [channel]

Sales:
- Train on [competitor] objection handling
- Improve demo of [differentiating feature]
- Accelerate POC process (2 weeks → 1 week)
```

## Resources и Templates

См. директорию `references/` для:
- Competitive Profile Template (детальный шаблон анализа)
- Battlecard Template (стандартный формат)
- Win/Loss Interview Script (вопросы для интервью)
- Competitive Response Playbook (reaction framework)

См. директорию `assets/` для:
- Feature Comparison Matrix (Excel с feature comparison)
- Pricing Comparison Calculator (динамический калькулятор)
- Market Share Dashboard (визуализация доли рынка)

## Сохранение результатов

Сохраняйте все конкурентные анализы в **Markdown на русском**:

```markdown
# Конкурентный Анализ: [Competitor Name]

## Метаданные
- **Дата**: YYYY-MM-DD
- **Аналитик**: [Your name]
- **Период**: Q[X] YYYY
- **Конфиденциальность**: Internal Only

## Исполнительное резюме
[Ключевые выводы и recommendations]

## Детальный Анализ
[Company overview, product portfolio, strategy]

## Конкурентная Позиция
[Strengths, weaknesses, market position]

## Рекомендации
### Краткосрочные (0-3 месяца)
[Immediate tactical responses]

### Долгосрочные (3-12 месяцев)
[Strategic positioning adjustments]

## Приложения
[Data sources, detailed comparisons]
```

Сохраняйте в: `~/cmo-output/competitive-intel/[competitor]-analysis-YYYY-MM-DD.md`
