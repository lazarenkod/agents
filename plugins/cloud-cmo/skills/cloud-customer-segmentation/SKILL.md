---
name: cloud-customer-segmentation
description: Методология сегментации клиентов облачного провайдера по размеру, индустрии, use case и зрелости. Use when defining target segments, developing personas, or tailoring marketing strategies.
---

# Cloud Customer Segmentation

## When to Use This Skill

- Определить primary и secondary target segments для маркетинга
- Разработать buyer personas для различных сегментов
- Сегментировать существующую customer base для targeted campaigns
- Определить ideal customer profile (ICP) для sales
- Разработать segment-specific messaging и positioning
- Оценить market opportunity по сегментам (TAM/SAM/SOM)

## Core Concepts

### 1. Segmentation Dimensions

#### By Company Size (Firmographic)
```
SMB (Small-Medium Business):
├── Size: <500 employees, <$50M annual revenue
├── Cloud Spend: $500-$10K/month ($6K-120K annually)
├── Decision Maker: Technical Founder, CTO, VP Engineering
├── Decision Process: Fast (days-weeks), technical evaluation
├── Purchase: Credit card, online, self-service
├── Support Need: Documentation, community, email support
├── Priorities: Speed, cost-effectiveness, ease of use
├── Sales Motion: Product-Led Growth (PLG), inside sales for expansion
├── CAC Target: $50-500
└── LTV Target: $5K-50K

Mid-Market:
├── Size: 500-5000 employees, $50M-$1B annual revenue
├── Cloud Spend: $10K-$500K/month ($120K-$6M annually)
├── Decision Maker: VP Engineering, IT Director, CIO
├── Decision Process: Medium (weeks-months), technical + business evaluation
├── Purchase: PO, invoice, contract negotiation
├── Support Need: Phone/email support, SLAs, CSM (at higher tier)
├── Priorities: Reliability, support, cost optimization, scalability
├── Sales Motion: Inside Sales + Solution Architects
├── CAC Target: $500-5K
└── LTV Target: $50K-500K

Enterprise:
├── Size: 5000+ employees, $1B+ annual revenue
├── Cloud Spend: $500K-$50M+/month ($6M-$600M+ annually)
├── Decision Maker: CIO, CTO, SVP IT, Procurement
├── Decision Process: Long (months-year), RFP, multi-stakeholder
├── Purchase: MSA, complex contracts, legal/procurement involvement
├── Support Need: 24/7 premium, Technical Account Manager (TAM), custom SLAs
├── Priorities: Security, compliance, vendor stability, strategic partnership
├── Sales Motion: Field Sales, Executive Sponsorship, Channel Partners
├── CAC Target: $5K-100K+
└── LTV Target: $500K-$50M+
```

#### By Industry Vertical
```
High-Priority Verticals (Target with specific solutions):

Financial Services & FinTech:
├── Pain Points: Compliance (PCI DSS, SOX), latency, security, audit
├── Requirements: Dedicated infrastructure, data residency, real-time processing
├── Use Cases: Payment processing, trading platforms, fraud detection, mobile banking
├── Messaging: "Enterprise-grade security and compliance for financial innovation"
├── Market Size: $35B cloud spend (22% YoY growth)
└── Competition: AWS (Capital One, Stripe), Azure (JP Morgan), specialized clouds

Healthcare & Life Sciences:
├── Pain Points: HIPAA compliance, interoperability, patient data privacy
├── Requirements: HIPAA BAA, HITRUST certification, data encryption, audit trails
├── Use Cases: EHR systems, telemedicine, medical imaging, genomics research
├── Messaging: "HIPAA-compliant cloud for healthcare innovation"
├── Market Size: $25B cloud spend (28% YoY growth)
└── Competition: AWS (Philips, Cerner), Azure (Providence), GCP (Mayo Clinic)

Retail & E-commerce:
├── Pain Points: Peak load handling, global scalability, personalization
├── Requirements: Auto-scaling, CDN, low latency, high availability
├── Use Cases: E-commerce platforms, inventory management, omnichannel retail
├── Messaging: "Infrastructure for modern retail that scales with demand"
├── Market Size: $30B cloud spend (25% YoY growth)
└── Competition: AWS (Shopify, Amazon retail itself), Azure (Target), Shopify Cloud

SaaS & Technology Companies:
├── Pain Points: Developer experience, reliability, cost at scale
├── Requirements: APIs, SDKs, high uptime, predictable pricing
├── Use Cases: SaaS application hosting, APIs, developer platforms
├── Messaging: "Cloud built for cloud-native companies"
├── Market Size: $40B cloud spend (30% YoY growth)
└── Competition: AWS, GCP, specialized PaaS providers

Manufacturing & IoT:
├── Pain Points: OT/IT convergence, edge computing, predictive maintenance
├── Requirements: IoT device management, edge-to-cloud, time-series databases
├── Use Cases: Smart factories, supply chain, predictive maintenance, digital twins
├── Messaging: "Industry 4.0 infrastructure for smart manufacturing"
├── Market Size: $20B cloud spend (30% YoY growth)
└── Competition: Azure (IoT focus), AWS (IoT Core), GE Predix

Media & Entertainment:
├── Pain Points: Media processing, content delivery, live streaming
├── Requirements: Transcoding, CDN, storage, GPUs for rendering
├── Use Cases: Video streaming, gaming, rendering, live broadcasts
├── Messaging: "Media infrastructure for content creators and platforms"
├── Market Size: $15B cloud spend (20% YoY growth)
└── Competition: AWS (Netflix, Disney+), GCP (Spotify, gaming)
```

#### By Use Case / Workload Type
```
Application Development & Hosting:
├── Description: Web/mobile applications, APIs, microservices
├── Services Needed: Compute (VMs, containers), load balancers, CDN
├── User Persona: Full-stack developers, DevOps engineers
├── Entry Point: Deploy first app (Node, Python, Go, etc.)
└── Expansion: Add databases, caching, monitoring, CI/CD

Data & Analytics:
├── Description: Data warehousing, business intelligence, data lakes
├── Services Needed: Object storage, data warehouse, ETL, visualization
├── User Persona: Data engineers, data analysts, data scientists
├── Entry Point: Migrate data warehouse (from on-prem or competitor)
└── Expansion: Add ML/AI, real-time streaming, governance tools

AI & Machine Learning:
├── Description: Model training, inference, MLOps
├── Services Needed: GPUs, managed ML platform, model serving
├── User Persona: ML engineers, data scientists, AI researchers
├── Entry Point: Train first model (TensorFlow, PyTorch, etc.)
└── Expansion: Production inference, MLOps, feature stores

DevOps & CI/CD:
├── Description: Continuous integration/deployment, automation
├── Services Needed: Container orchestration (K8s), CI/CD pipelines, registries
├── User Persona: DevOps engineers, SREs, platform engineers
├── Entry Point: Deploy K8s cluster or setup CI/CD pipeline
└── Expansion: Observability, security scanning, infrastructure-as-code

Migration & Modernization:
├── Description: Lift-and-shift from on-prem или другого cloud
├── Services Needed: VMs, storage, migration tools, professional services
├── User Persona: IT managers, infrastructure architects
├── Entry Point: Assessment, POC migration
└── Expansion: Refactor to cloud-native, containerize, serverless

IoT & Edge Computing:
├── Description: IoT device management, edge processing, data ingestion
├── Services Needed: IoT platform, edge nodes, time-series DB, streaming
├── User Persona: IoT architects, embedded engineers
├── Entry Point: Connect devices, stream data to cloud
└── Expansion: Edge ML inference, predictive analytics, digital twins
```

#### By Cloud Maturity (Sophistication)
```
Cloud Beginners:
├── Characteristics: First cloud workload, on-prem background
├── Pain Points: Complexity, learning curve, migration risk
├── Needs: Simplicity, hand-holding, education, migration services
├── Entry Strategy: Managed services, professional services, training
├── Messaging: "Cloud made simple for enterprises"
└── Conversion Path: Start with VMs (lift-and-shift) → containers → serverless

Cloud Adopters:
├── Characteristics: Multiple workloads, exploring cloud-native
├── Pain Points: Cost optimization, governance, multi-account management
├── Needs: Best practices, architectural guidance, cost management tools
├── Entry Strategy: Architecture reviews, workshops, cost audits
├── Messaging: "Optimize and scale your cloud journey"
└── Conversion Path: Better pricing, governance tools, multi-cloud support

Cloud Advanced:
├── Characteristics: Cloud-first, containers, microservices
├── Pain Points: Advanced features, performance, integrations
├── Needs: Cutting-edge services, deep technical capabilities
├── Entry Strategy: Advanced features, technical differentiation
├── Messaging: "Advanced cloud for sophisticated teams"
└── Conversion Path: AI/ML, edge, serverless, platform capabilities

Cloud Native:
├── Characteristics: Serverless, multi-cloud, FinOps mature
├── Pain Points: Vendor lock-in, multi-cloud complexity, cost at scale
├── Needs: Portability, Kubernetes, open standards, best-of-breed
├── Entry Strategy: Open source, Kubernetes, multi-cloud tools
├── Messaging: "Cloud-native infrastructure for modern architectures"
└── Conversion Path: Kubernetes platform, service mesh, observability suite
```

### 2. Buyer Personas

#### Persona Template
```markdown
# [Persona Name] - [Role]

## Demographics
- **Job Title**: [Specific titles]
- **Company Size**: [SMB/Mid/Enterprise]
- **Industry**: [Verticals where common]
- **Reporting To**: [Boss's role]
- **Team Size**: [People managed/on team]
- **Experience**: [Years in role, background]

## Goals & Responsibilities
- **Primary Goal**: [What success looks like]
- **Key Responsibilities**: [Day-to-day duties]
- **Success Metrics**: [How performance measured]
- **Challenges**: [Obstacles to success]

## Pain Points (Problems We Solve)
1. **[Pain Point 1]**: [Detailed description]
2. **[Pain Point 2]**: [Detailed description]
3. **[Pain Point 3]**: [Detailed description]

## Decision Criteria (What Matters)
1. **[Criterion 1]**: [Why important, how to address]
2. **[Criterion 2]**: [Why important, how to address]
3. **[Criterion 3]**: [Why important, how to address]

## Buying Process
- **Role in Decision**: [Economic buyer / Technical evaluator / Influencer / User]
- **Evaluation Timeline**: [Typical duration]
- **Influences**: [Who influences their decision]
- **Objections**: [Common concerns, hesitations]
- **Preferred Engagement**: [How they like to buy: self-service, demo, trial, RFP]

## Information Sources
- **Content Preferences**: [Tutorials, whitepapers, videos, webinars]
- **Trusted Sources**: [Publications, analysts, influencers they follow]
- **Communities**: [Stack Overflow, Reddit, LinkedIn groups, conferences]
- **Search Behavior**: [Keywords they search, questions they ask]

## Messaging for This Persona
- **Value Proposition**: [One-sentence pitch]
- **Key Messages**: [3-5 core messages that resonate]
- **Proof Points**: [Testimonials, metrics, case studies]
- **Call-to-Action**: [What we want them to do]

## Marketing Tactics
- **Content**: [Types that work: tutorials vs ROI docs]
- **Channels**: [Where to reach: LinkedIn vs GitHub vs conferences]
- **Campaigns**: [ABM, content syndication, events]
- **Sales Enablement**: [How sales should engage]
```

#### Example Developer Persona
```markdown
# Alex the Application Developer

## Demographics
- **Job Titles**: Software Engineer, Full-Stack Developer, Backend Engineer
- **Company Size**: Startups to Mid-Market (mostly <1000 employees)
- **Industry**: SaaS, FinTech, E-commerce, Any tech company
- **Reports To**: Engineering Manager, CTO (in small companies)
- **Team Size**: Individual contributor или small team (2-5 engineers)
- **Experience**: 2-8 years coding, comfortable with cloud basics

## Goals
- **Primary**: Ship features fast, minimal infrastructure headaches
- **Responsibilities**: Build APIs, deploy applications, fix bugs, code reviews
- **Success Metrics**: Velocity (features shipped), uptime, code quality
- **Challenges**: Limited time, pressure to deliver, not a DevOps expert

## Pain Points
1. **Complex Infrastructure**: AWS overwhelming (too many services, cryptic docs)
2. **DevOps Burden**: Wants to code, not manage servers and infrastructure
3. **Cost Surprises**: Bill shock from unexpected usage, hard to predict costs
4. **Slow Deployments**: Waiting on DevOps team, complicated CI/CD

## Decision Criteria
1. **Developer Experience**: Intuitive, well-documented, fast to get started
2. **Speed**: Can I deploy in 10 minutes? Quick iteration loops?
3. **Pricing**: Transparent, predictable, not going to drain startup budget
4. **Community**: Good docs, helpful community, Stack Overflow activity

## Buying Process
- **Role**: Technical evaluator (trial, POC) + user
- **Timeline**: Fast (days to weeks for personal decision)
- **Influences**: Peers, Twitter, Hacker News, dev influencers
- **Objections**: "Never heard of it", "Will my team know it?", "Is it reliable?"
- **Preferred**: Self-service trial → love it → push for team adoption

## Information Sources
- **Content**: Tutorials, code samples, getting started guides, comparison articles
- **Trusted Sources**: Dev.to, Hacker News, Twitter, tech YouTube, blogs
- **Communities**: Stack Overflow, GitHub, Reddit (r/webdev, r/node), Discord
- **Search**: "How to deploy [framework]", "[service] vs [competitor]", "[tech] tutorial"

## Messaging
- **Value Prop**: "Deploy your app in 10 minutes with great docs and predictable pricing"
- **Key Messages**:
  1. Simple, not simplistic (handles production workloads)
  2. Developer-friendly (CLI, API-first, good docs)
  3. Transparent pricing (no surprises, easy to estimate)
  4. Fast deployment (git push to deploy)
- **Proof**: "Developers rate our docs 4.8/5", "Deploy in <10 min", "Used by 50K+ developers"
- **CTA**: "Start free trial" (no credit card), "Follow tutorial"

## Tactics
- **Content**: Lots of tutorials, YouTube coding videos, Twitter tips
- **Channels**: Dev.to, Hashnode, GitHub, Stack Overflow, Reddit, Hacker News
- **Events**: Meetups, hackathons, developer conferences (JSConf, PyCon)
- **Sales**: No sales needed (PLG), inside sales only when team scales
```

## Resources и Templates

См. `references/` для:
- Persona Development Template
- ICP Definition Framework
- Segment Opportunity Analysis
- Persona Interview Questions

См. `assets/` для:
- Segment Comparison Matrix
- Persona at-a-glance Cards (printable)
- Buyer Journey Maps (по persona)

## Сохранение результатов

```markdown
# Customer Segmentation Analysis

## Метаданные
- **Дата**: YYYY-MM-DD
- **Автор**: [Name]
- **Статус**: [Draft/Approved]

## Target Segments
[Priority segments, characteristics, opportunity size]

## Buyer Personas
[Detailed personas для каждого key role]

## Segment Strategy
[How to address each segment: GTM, messaging, channels]

## ICP Definition
[Ideal Customer Profile для sales targeting]
```

Сохраняйте в: `~/cmo-output/segmentation/customer-segmentation-YYYY-MM-DD.md`
