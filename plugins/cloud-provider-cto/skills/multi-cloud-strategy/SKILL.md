---
name: multi-cloud-strategy
description: Стратегия мультиоблачных решений для облачных провайдеров. Use when designing multi-cloud architecture, evaluating cloud vendors, planning hybrid cloud solutions, or developing inter-cloud migration strategies.
---

# Мультиоблачная стратегия

Комплексное руководство по разработке и реализации мультиоблачных стратегий на базе практик AWS, Azure, Google Cloud и Oracle Cloud.

## Обязательные правила вывода
- Всегда отвечай **на русском**.
- Сохраняй артефакты в `outputs/cloud-provider-cto/skills/multi-cloud-strategy/{timestamp}_{кратко}.md` через Write tool; обновляй один файл по итерациям.
- Формат: цель/контекст → драйверы/ограничения → варианты/архитектура → метрики/алерты → план/ритм → TODO → изменения vs прошлой версии.

## 3-итерационный контур
1) **Диагностика (1–2 ч):** драйверы (резерв/цена/регуляторика/функции), текущий стэк/данные/PII, зависимости/вендор-лок, SLA/латентность. Черновой бриф + risk log.
2) **Дизайн (2–4 ч):** варианты (primary/DR, active-active, workload split, data gravity), архитектура (network/identity/data/observability), биллинг/контракты, метрики/алерты, приоритеты (RICE/WSJF). Таблица вариантов/рисков/стоимости.
3) **Верификация (1–2 ч):** выбранный вариант, PoC/пилоты, контрольные точки/алерты, план миграций/операций, обновление логов/TODO/изменений.

## Когда использовать этот скилл

- Проектирование архитектуры для работы в нескольких облаках
- Оценка и выбор облачных провайдеров для различных workloads
- Планирование hybrid cloud решений
- Разработка стратегии миграции между облаками
- Управление vendor lock-in рисками
- Оптимизация затрат через multi-cloud распределение

## Входы (собери до старта)
- Требования SLA/латентность/PII/регуляторика, драйверы multi-cloud (резерв, цена, функции, суверенитет).
- Текущая архитектура/данные/CI/CD/observability/IAM, договоры/скидки/egress.
- Ограничения: команда/операции, инструменты, зависимости от SaaS/PaaS.

## Выходы (обязательно зафиксировать)
- Выбранный паттерн (active-active, split, primary/DR), архитектура (network/IAM/data/obs), план миграций.
- Метрики/алерты (доступность/латентность/стоимость/операции), риски/mitigation, контрольные точки.
- TODO/владельцы/сроки, decision/risk log, изменения vs прошлой версии.

## Метрики и алерты
- Доступность (SLO), латентность p50/p95, failover время, ошибка конфигов/дрейф.
- Стоимость: egress/двойное хранение/операции, дублирование CICD/obs.
- Операции: MTTR при фейловере, дрейф IAM/сетей, успех тестов DR/region.
- Алерты: рост egress, несоответствие данных, провал DR тестов, рассинхрон IAM/PKI.

## Качество ответа (checklist)
- Драйверы/ограничения чётко описаны; варианты сравнили по стоимости/риску/latency.
- Архитектура сети/IAM/данных/obs прописана; план миграций/DR есть.
- Метрики/алерты/владельцы/контрольные точки заданы; логи/TODO обновлены.

## Red Flags
- “Multi-cloud” только на слайдах; не учтены data gravity/egress/PII.
- Нет DR тестов/алертов; IAM/PKI/observability не унифицированы.
- Нет владельцев/ритма/контрольных точек; нет плана миграций/rollback.

## Шаблоны и справочники
- Assets: `multi-cloud-decision-matrix.md`, `architecture-outline.md`, `dr-failover-playbook.md`.
- References: `pattern-comparison.md`, `multi-cloud-risks.md`, `metrics-checklist.md`.

## Основные концепции

### Типы мультиоблачных архитектур

#### 1. Redundant Multi-Cloud (Высокая доступность)

**Описание**: Дублирование critical workloads в нескольких облаках для максимальной доступности.

**Архитектура**:
```
┌─────────────┐         ┌─────────────┐
│   AWS US    │◄───────►│  Azure US   │
│  Production │  Sync   │  Production │
└─────────────┘         └─────────────┘
       │                       │
       └───────┬───────────────┘
          Global DNS
        (Route53 / Azure DNS)
              │
         [Users]
```

**Сценарии использования**:
- Mission-critical приложения (финансы, healthcare)
- Требование 99.99%+ availability
- Регуляторные требования к избыточности
- Zero-downtime migrations

**Сложности**:
- Data consistency между облаками
- Стоимость (2x-3x infrastructure)
- Сложность синхронизации
- Network latency между providers

**Best Practices**:
- Active-active с global load balancing
- Asynchronous data replication с conflict resolution
- Health checks и automatic failover
- Chaos engineering для testing
- Separate CI/CD pipelines per cloud

**Пример: AWS + Azure Redundancy**
```yaml
# Terraform multi-cloud setup
# AWS Primary
module "aws_primary" {
  source = "./modules/aws"
  region = "us-east-1"
  environment = "production"

  # Application tier
  app_instances = 10
  instance_type = "m5.xlarge"

  # Database tier
  db_engine = "postgres"
  db_instance_class = "db.r5.2xlarge"
  multi_az = true
  read_replicas = 2
}

# Azure Secondary (Active)
module "azure_secondary" {
  source = "./modules/azure"
  location = "East US"
  environment = "production"

  # Application tier
  vm_count = 10
  vm_size = "Standard_D4s_v3"

  # Database tier
  database_sku = "GP_Gen5_8"
  geo_replication = true
}

# Global Traffic Manager
resource "azurerm_traffic_manager_profile" "global" {
  name = "global-tm"
  traffic_routing_method = "Performance" # or Weighted

  monitor_config {
    protocol = "HTTPS"
    port = 443
    path = "/health"
    interval_in_seconds = 30
    timeout_in_seconds = 10
    tolerated_number_of_failures = 3
  }
}
```

#### 2. Partitioned Multi-Cloud (Workload Separation)

**Описание**: Различные workloads или регионы в разных облаках по функциональным или географическим причинам.

**Архитектура**:
```
┌──────────────────────┐
│   Google Cloud US    │
│   - AI/ML Platform   │
│   - BigQuery         │
└──────────────────────┘
           │
    Data Pipeline
           │
           ▼
┌──────────────────────┐
│      AWS Global      │
│   - Core App         │
│   - APIs             │
└──────────────────────┘
           │
    Federation
           │
           ▼
┌──────────────────────┐
│    Azure Europe      │
│   - GDPR Data        │
│   - EU Customers     │
└──────────────────────┘
```

**Сценарии использования**:
- Data residency requirements (GDPR, China, Russia)
- Best-of-breed services (GCP для AI, AWS для breadth)
- M&A scenarios (acquired companies на разных clouds)
- Cost optimization (spot pricing arbitrage)

**Best Practices**:
- Clear workload boundaries
- API-based integration (REST, GraphQL, gRPC)
- Event-driven architecture для loose coupling
- Identity federation (SAML, OIDC)
- Centralized logging/monitoring
- Network interconnects (AWS Direct Connect + Azure ExpressRoute + Google Cloud Interconnect)

**Пример: Functional Partitioning**
```markdown
# Workload Distribution Strategy

## AWS (Core Platform)
- Compute: EC2, EKS для microservices
- Storage: S3 для object storage
- Database: RDS PostgreSQL
- Networking: VPC, Transit Gateway
- CDN: CloudFront

**Reasoning**: Самая широкая ecosystem, mature services

## Google Cloud (AI/ML & Analytics)
- AI Platform: Vertex AI для model training
- Data Warehouse: BigQuery
- Stream Processing: Dataflow
- ML APIs: Vision, NLP, Speech

**Reasoning**: Лучшие AI/ML capabilities, BigQuery performance

## Azure (Enterprise Integration)
- Active Directory: Azure AD для SSO
- Hybrid: Azure Arc для on-prem management
- Microsoft Stack: Integration с Office 365, Dynamics
- Europe: EU data residency

**Reasoning**: Enterprise integration, Microsoft ecosystem

## Integration Points
1. **Data Sync**: AWS S3 ↔ Google Cloud Storage (Storage Transfer Service)
2. **Identity**: Azure AD как central IdP, federated to AWS IAM & GCP IAM
3. **Networking**: VPN tunnels между VPCs
4. **Monitoring**: Centralized в Datadog/New Relic
```

#### 3. Cloud-Agnostic (Portable Architecture)

**Описание**: Архитектура максимально независимая от specific cloud provider через abstraction layers.

**Архитектура**:
```
┌─────────────────────────────────────┐
│     Application Layer               │
│  (Cloud-agnostic via abstractions)  │
└─────────────────────────────────────┘
              │
┌─────────────┴─────────────┐
│   Abstraction Layer       │
│  - Kubernetes (compute)   │
│  - Terraform (IaC)        │
│  - OpenTelemetry (obs)    │
└─────────────┬─────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼───┐ ┌──▼────┐
│  AWS  │ │ Azure│ │  GCP  │
└───────┘ └──────┘ └───────┘
```

**Ключевые технологии**:
- **Compute**: Kubernetes (EKS, AKS, GKE)
- **IaC**: Terraform, Pulumi, Crossplane
- **Service Mesh**: Istio, Linkerd
- **Observability**: OpenTelemetry, Prometheus, Grafana
- **CI/CD**: ArgoCD, Flux (GitOps)
- **Storage**: MinIO (S3-compatible), Rook-Ceph
- **Database**: CockroachDB (distributed SQL), Cassandra

**Преимущества**:
- Минимальный vendor lock-in
- Легкая миграция между providers
- Negotiation leverage с vendors
- Multi-cloud deployment из одного codebase

**Недостатки**:
- Не используются managed services
- Выше operational overhead
- Сложность в поддержке
- Может быть дороже

**Пример: Kubernetes-based Abstraction**
```yaml
# Kubernetes deployment (работает на EKS, AKS, GKE)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: app
        image: myregistry.io/app:v1.2.3
        ports:
        - containerPort: 8080
        env:
        # Environment-specific config via ConfigMaps
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        # Cloud-agnostic storage via CSI driver
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: app-storage
---
# Terraform для provisioning (multi-cloud)
module "kubernetes_cluster" {
  source = "./modules/kubernetes"

  # Variables switch based on provider
  provider = var.cloud_provider # "aws" | "azure" | "gcp"
  region = var.region
  node_count = 5
  node_instance_type = var.instance_type
}

# Provider-specific но with consistent interface
# ./modules/kubernetes/aws.tf
# ./modules/kubernetes/azure.tf
# ./modules/kubernetes/gcp.tf
```

### Стратегия выбора облачных провайдеров

#### Критерии оценки

**1. Функциональные возможности**

| Критерий | AWS | Azure | Google Cloud | Oracle Cloud |
|----------|-----|-------|--------------|--------------|
| **Breadth of Services** | ⭐⭐⭐⭐⭐ (200+) | ⭐⭐⭐⭐ (100+) | ⭐⭐⭐⭐ (100+) | ⭐⭐⭐ (80+) |
| **Compute Options** | EC2, Lambda, Fargate, Batch, Lightsail | VMs, Functions, Container Instances, Batch | Compute Engine, Cloud Functions, Cloud Run, GKE | Compute, Functions, Container Instances |
| **Managed Kubernetes** | EKS ⭐⭐⭐⭐ | AKS ⭐⭐⭐⭐⭐ | GKE ⭐⭐⭐⭐⭐ | OKE ⭐⭐⭐ |
| **AI/ML Platform** | SageMaker ⭐⭐⭐⭐ | Azure ML ⭐⭐⭐⭐ | Vertex AI ⭐⭐⭐⭐⭐ | OCI Data Science ⭐⭐⭐ |
| **Database Variety** | RDS, Aurora, DynamoDB, DocumentDB, Neptune | SQL DB, Cosmos DB, PostgreSQL, MySQL | Cloud SQL, Spanner, Firestore, Bigtable | Autonomous DB, MySQL, NoSQL |
| **Analytics** | Redshift, Athena, EMR ⭐⭐⭐⭐ | Synapse, Databricks ⭐⭐⭐⭐ | BigQuery ⭐⭐⭐⭐⭐ | Autonomous DW ⭐⭐⭐ |

**2. Geographic Coverage**

- **AWS**: 33 regions, 105 availability zones, 600+ edge locations (лидер)
- **Azure**: 60+ regions (включая China, Government), hybrid edge
- **Google Cloud**: 40+ regions, 121 zones, global fiber network
- **Oracle Cloud**: 44 regions (rapid expansion), Government clouds

**Выбор по региону**:
- **China**: Azure (через 21Vianet), AWS (через Sinnet/NWCD), Alibaba Cloud (local leader)
- **Europe (GDPR)**: Все major providers, но Azure сильнее in Enterprise
- **Government (US)**: AWS GovCloud, Azure Government, Google Cloud для DoD
- **Emerging Markets**: AWS шире coverage

**3. Pricing Models**

```markdown
## Сравнение pricing подходов

### AWS
- **On-Demand**: pay-as-you-go (highest cost)
- **Reserved Instances**: 1-year или 3-year commitment (до 75% discount)
- **Savings Plans**: flexible commitments (compute, EC2, SageMaker)
- **Spot Instances**: unused capacity (до 90% discount, но evictable)

### Azure
- **Pay-As-You-Go**: standard rates
- **Reserved Instances**: 1-year или 3-year (до 72% discount)
- **Spot VMs**: unused capacity (до 90% discount)
- **Hybrid Benefit**: use existing Windows/SQL licenses (до 55% savings)
- **Dev/Test Pricing**: discounted rates для non-production

### Google Cloud
- **On-Demand**: standard pricing
- **Committed Use Discounts**: 1-year или 3-year (до 57% discount)
- **Sustained Use Discounts**: автоматически для long-running (до 30%)
- **Preemptible VMs**: short-lived instances (до 80% discount)
- **Free Tier**: generous always-free tier

### Oracle Cloud
- **Pay-As-You-Go**: standard rates
- **Universal Credits**: flexible spend commitment
- **Always Free**: limited always-free resources
- **Bring Your Own License (BYOL)**: migrate existing licenses
- **Oracle Cloud Lift**: free migration services
```

**Cost Optimization Strategy**:
1. **Dev/Test**: GCP (sustained use discounts, preemptible VMs)
2. **Production steady-state**: Reserved/Committed instances
3. **Batch workloads**: Spot/Preemptible instances
4. **Microsoft workloads**: Azure (Hybrid Benefit)
5. **Oracle databases**: Oracle Cloud (BYOL, Autonomous DB)

**4. Enterprise Integration**

| Use Case | Recommended Provider |
|----------|---------------------|
| **Microsoft Ecosystem** (Office 365, AD, Dynamics) | Azure (tight integration) |
| **SAP Workloads** | Azure, AWS, GCP (certified) |
| **Oracle Databases** | Oracle Cloud (best performance, BYOL), AWS RDS Oracle |
| **VMware** | Azure (AVS), AWS (VMware Cloud on AWS), GCP (GCVE) |
| **Hybrid Cloud** | Azure (Arc, Stack), AWS (Outposts), GCP (Anthos) |

### Data Residency & Compliance

**Стратегия по регионам**:

```markdown
# Data Residency Strategy

## Europe (GDPR)
**Primary**: Azure Europe или AWS EU regions
**Requirements**:
- Data stored только в EU
- Data transfers require SCCs
- DPO appointment
- GDPR-compliant DPA

**Implementation**:
- Region restriction policies (AWS Organizations, Azure Policy)
- Encryption с customer-managed keys (в EU HSM)
- Access controls (EU personnel only)
- Audit logging в EU storage

## China
**Primary**: AWS China (через Sinnet) или Azure China (через 21Vianet)
**Requirements**:
- ICP license
- Local partner (no direct operation by foreign company)
- Data localization (cannot transfer abroad)
- Government access requirements

**Implementation**:
- Separate China region deployment
- Local account structure
- Restricted data sync to global
- Compliance с Cybersecurity Law

## Russia
**Primary**: Local providers (Yandex Cloud, VK Cloud) или on-prem
**Requirements**:
- Personal data localization law
- Data stored на Russian territory
- Registered in Russian database

## Middle East
**AWS**: Bahrain region
**Azure**: UAE regions (Dubai, Abu Dhabi)
**Google Cloud**: Planning

## Government (US)
- **AWS GovCloud**: FedRAMP High, ITAR, DoD SRG
- **Azure Government**: FedRAMP High, DoD IL5
- **Google Cloud**: FedRAMP High Authorized
- **Oracle Cloud**: Government regions available
```

### Multi-Cloud Networking

#### Interconnection Options

**1. VPN Tunnels**
```
AWS VPC ←──VPN──→ Azure VNet ←──VPN──→ GCP VPC

Pros:
- Low cost ($0.05/GB transfer)
- Easy setup
- Encrypted by default

Cons:
- Internet routing (variable latency)
- Limited bandwidth (1-2 Gbps)
- Best effort delivery
```

**2. Direct Interconnects**
```
┌─────────┐  Direct Connect  ┌──────────────┐
│   AWS   │←────(10 Gbps)───→│   Equinix    │
└─────────┘                   │   Colocation │
                              │              │
┌─────────┐  ExpressRoute    │              │
│  Azure  │←────(10 Gbps)───→│              │
└─────────┘                   └──────────────┘

Pros:
- Predictable latency (1-5ms)
- Higher bandwidth (up to 100 Gbps)
- Reduced data transfer costs
- Private connectivity

Cons:
- Setup complexity
- Monthly port fees ($500-5000)
- Requires colocation или carrier
```

**3. Cloud Interconnect Platforms**
- **Megaport**: On-demand connectivity marketplace
- **Equinix Fabric**: Software-defined interconnection
- **PacketFabric**: Automated cloud connectivity
- **Console Connect**: Marketplace for cloud connections

**Пример: Megaport для Multi-Cloud**
```markdown
# Megaport Multi-Cloud Connectivity

## Architecture
                 ┌──────────────┐
                 │   Megaport   │
                 │   Virtual    │
                 │    Router    │
                 └──────┬───────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
   │   AWS   │    │  Azure  │    │   GCP   │
   │  VPC    │    │  VNet   │    │  VPC    │
   └─────────┘    └─────────┘    └─────────┘

## Benefits
- Single interface для управления all connections
- On-demand provisioning (минуты, не months)
- Pay-as-you-grow bandwidth
- Centralized billing

## Cost Example (10 Gbps cross-cloud)
- Megaport Port: $500/month
- AWS VXC: $200/month
- Azure VXC: $200/month
- GCP VXC: $200/month
- Data transfer: $0.02-0.05/GB
Total: ~$1100/month + data transfer
```

### Identity & Access Management (IAM) Federation

**Стратегия centralized identity**:

```markdown
# Federated Identity Architecture

## Central Identity Provider (IdP)
**Options**:
1. **Azure AD** (best for enterprise)
2. **Okta** (best for multi-cloud)
3. **Auth0** (developer-friendly)
4. **Ping Identity**

## Federation Flow
                  ┌─────────────┐
                  │   Azure AD  │
                  │  (Central)  │
                  └──────┬──────┘
                         │ SAML/OIDC
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐      ┌───▼────┐      ┌───▼────┐
   │   AWS   │      │ Google │      │ Oracle │
   │   IAM   │      │  Cloud │      │  Cloud │
   │  (SAML) │      │  (OIDC)│      │  (SAML)│
   └─────────┘      └────────┘      └────────┘

## Implementation

### Azure AD → AWS
# AWS IAM SAML Provider
aws iam create-saml-provider \
  --name AzureAD \
  --saml-metadata-document file://azure-metadata.xml

# IAM Role for federated users
{
  "Role": "AzureAD-Admins",
  "AssumeRolePolicyDocument": {
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT:saml-provider/AzureAD"
      },
      "Action": "sts:AssumeRoleWithSAML",
      "Condition": {
        "StringEquals": {
          "SAML:aud": "https://signin.aws.amazon.com/saml"
        }
      }
    }]
  }
}

### Azure AD → Google Cloud
# Google Workspace SAML App
gcloud iam workload-identity-pools create azure-pool \
  --location="global" \
  --display-name="Azure AD Federation"

### Centralized MFA
- Enforce MFA в Azure AD
- Propagates to all federated clouds
- Single MFA enrollment для users
```

### Multi-Cloud Monitoring & Observability

**Centralized Observability Stack**:

```markdown
# Multi-Cloud Observability Architecture

## Strategy: Unified observability platform

### Option 1: Datadog (SaaS)
**Pros**:
- Native integrations: AWS, Azure, GCP, Oracle
- Single pane of glass
- APM, Infrastructure, Logs, Synthetics
- Out-of-box dashboards

**Cons**:
- Cost (host-based pricing)
- Vendor lock-in

### Option 2: Self-Hosted (Open Source)
**Stack**:
- **Metrics**: Prometheus + Thanos (long-term storage)
- **Logs**: Loki или Elasticsearch
- **Traces**: Jaeger или Tempo
- **Visualization**: Grafana
- **Alerting**: Alertmanager

**Pros**:
- Lower cost at scale
- Data ownership
- Customizable

**Cons**:
- Operational overhead
- Maintenance burden

### Option 3: Hybrid
- **Centralized SaaS**: New Relic, Datadog для core metrics
- **Self-hosted**: ELK stack для log archival
- **Cloud-native**: CloudWatch, Azure Monitor для cloud-specific

## Implementation Example: Prometheus Federation

```yaml
# Prometheus в каждом cloud
# AWS Prometheus
scrape_configs:
  - job_name: 'aws-ec2'
    ec2_sd_configs:
      - region: us-east-1

# Azure Prometheus
scrape_configs:
  - job_name: 'azure-vms'
    azure_sd_configs:
      - subscription_id: xxx

# GCP Prometheus
scrape_configs:
  - job_name: 'gcp-instances'
    gce_sd_configs:
      - project: my-project

# Central Thanos Query (aggregates all)
stores:
  - aws-prometheus:10901
  - azure-prometheus:10901
  - gcp-prometheus:10901
```

### Disaster Recovery Multi-Cloud

**RPO/RTO Strategy**:

```markdown
# Multi-Cloud DR Strategy

## Tier 1: Mission Critical (RPO: 0, RTO: < 5 min)
**Architecture**: Active-Active Multi-Cloud
- AWS US-East + Azure US-East
- Synchronous replication
- Global load balancer (Cloudflare, Akamai)
- Auto-failover

**Services**:
- Payment processing
- Trading systems
- Emergency services

**Cost**: 2-3x production cost

## Tier 2: Business Critical (RPO: 15 min, RTO: 1 hour)
**Architecture**: Active-Passive Multi-Cloud
- AWS US-East (Primary)
- GCP US-Central (DR)
- Asynchronous replication (15 min lag)
- Manual failover (runbook)

**Services**:
- E-commerce platform
- CRM systems
- Customer portals

**Cost**: 1.5x production cost

## Tier 3: Important (RPO: 4 hours, RTO: 8 hours)
**Architecture**: Backup to Different Cloud
- Azure Europe (Primary)
- AWS Europe (DR - cold standby)
- Daily backups replicated
- Infrastructure as Code (быстрое восстановление)

**Services**:
- Internal tools
- Reporting systems
- Data warehouses

**Cost**: 1.1x production cost

## Implementation: Active-Passive

### Primary (AWS)
- Full production environment
- Real-time transaction processing
- Continuous backup to S3

### DR (Azure)
- Minimal infrastructure (stopped VMs)
- Standby database (replicated from AWS)
- Pre-configured ARM templates

### Failover Process
1. Detect failure (monitoring alerts)
2. Promote Azure DB to primary
3. Scale up Azure infrastructure (IaC)
4. Update DNS (TTL: 60s)
5. Redirect traffic
Total time: ~30-60 minutes
```

## Референсные материалы

### Сравнительные таблицы сервисов

См. файл `references/service-comparison.md` с детальным сравнением 100+ сервисов AWS vs Azure vs GCP vs Oracle.

### Архитектурные диаграммы

См. директорию `assets/` с reference architectures для типовых multi-cloud сценариев.

### Case Studies

См. `references/case-studies.md` с реальными примерами мультиоблачных внедрений от Netflix, Spotify, Capital One.

## Чек-лист мультиоблачной стратегии

```markdown
# Multi-Cloud Strategy Checklist

## Strategic Planning
- [ ] Определены бизнес-драйверы для multi-cloud
- [ ] Выбран тип multi-cloud architecture (redundant/partitioned/agnostic)
- [ ] Проведена оценка cloud providers по критериям
- [ ] Разработана workload distribution strategy
- [ ] Определены data residency requirements

## Architecture & Design
- [ ] Спроектирована network connectivity (VPN/Direct Connect)
- [ ] Разработана federated identity strategy
- [ ] Определена data replication approach
- [ ] Спроектирована observability architecture
- [ ] Планирование disaster recovery

## Governance & Operations
- [ ] Созданы multi-cloud policies и standards
- [ ] Настроены cost allocation и chargeback
- [ ] Определены SLAs для cross-cloud services
- [ ] Разработаны runbooks для multi-cloud operations
- [ ] Проведены chaos engineering tests

## Security & Compliance
- [ ] Реализована unified security posture
- [ ] Настроен centralized logging и SIEM
- [ ] Проведена compliance mapping по регионам
- [ ] Реализована encryption strategy
- [ ] Планирование incident response across clouds

## Cost Management
- [ ] Настроены cost monitoring dashboards
- [ ] Реализованы budget alerts
- [ ] Проведен pricing comparison analysis
- [ ] Определена commitment strategy (reserved/committed)
- [ ] Планирование cost optimization initiatives
```

---

**Все материалы сохраняются в Markdown на русском языке для использования CTO и архитектурными командами.**
