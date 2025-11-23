---
name: platform-engineering
description: Master platform engineering practices including IDP design, Backstage.io, golden paths, self-service platforms, and developer portals. Use when building internal developer platforms, implementing Backstage, creating golden paths, designing self-service capabilities, or establishing platform teams.
---

# Platform Engineering

## When to Use This Skill

- Building or designing an Internal Developer Platform (IDP)
- Implementing Backstage.io for developer portals
- Creating golden paths and paved roads for developers
- Designing self-service platform capabilities
- Establishing platform engineering teams
- Migrating from traditional operations to platform models
- Creating software catalogs and service templates
- Measuring and improving developer experience
- Implementing Team Topologies platform team patterns

## Core Concepts

### What is Platform Engineering?

Platform engineering is the discipline of designing and building toolchains and workflows that enable self-service capabilities for software engineering organizations in the cloud-native era. The platform team creates an Internal Developer Platform (IDP) that abstracts complexity and provides golden paths for developers.

**Key Principles:**

1. **Developer Self-Service**: Reduce cognitive load by providing curated, opinionated paths
2. **Product Thinking**: Treat the platform as a product with internal customers
3. **Thin Abstraction Layer**: Hide complexity without limiting flexibility
4. **Golden Paths**: Paved roads that make the right thing the easy thing
5. **Measured Experience**: Quantify developer experience and platform adoption

### The Platform Engineering Manifesto

- **Platform as a Product** — not just infrastructure automation
- **Self-Service Over Ticket Queues** — empower developers to move fast
- **Golden Paths Over Freedom** — opinionated but escapable patterns
- **Measured Experience** — metrics drive platform improvements
- **Team Topologies** — platform teams enable stream-aligned teams

### Platform Engineering vs DevOps vs SRE

| Aspect | DevOps | SRE | Platform Engineering |
|--------|--------|-----|---------------------|
| Focus | Culture & practices | Reliability & operations | Developer experience & productivity |
| Delivery | CI/CD pipelines | SLOs & error budgets | Self-service platform |
| Team Model | Cross-functional | Ops with dev skills | Platform team serving dev teams |
| Success Metric | Deployment frequency | Service uptime | Developer satisfaction & velocity |
| Tooling | Tool diversity | Custom reliability tools | Unified IDP with golden paths |

## Internal Developer Platform (IDP) Architecture

### IDP Components

An IDP consists of five layers:

```
┌─────────────────────────────────────────────────────┐
│  Developer Portal (Backstage, Port, etc)            │  ← Interface Layer
├─────────────────────────────────────────────────────┤
│  Platform Orchestrator (Crossplane, Terraform, etc) │  ← Orchestration Layer
├─────────────────────────────────────────────────────┤
│  Platform Capabilities (CI/CD, DBs, Secrets, etc)   │  ← Capability Layer
├─────────────────────────────────────────────────────┤
│  Infrastructure (K8s, Cloud, Networking)            │  ← Infrastructure Layer
├─────────────────────────────────────────────────────┤
│  Integrations (Git, Monitoring, Security)           │  ← Integration Layer
└─────────────────────────────────────────────────────┘
```

**Layer Details:**

1. **Interface Layer** (Developer Portal)
   - Software catalog (all services, APIs, teams)
   - Service templates (scaffolding new services)
   - Documentation and runbooks
   - Dashboards and metrics
   - Search and discovery

2. **Orchestration Layer** (Platform Engine)
   - Resource provisioning (Crossplane, Terraform)
   - GitOps workflows (ArgoCD, Flux)
   - Policy enforcement (OPA, Kyverno)
   - Score, Humanitec, or custom orchestrators

3. **Capability Layer** (Platform Services)
   - CI/CD pipelines (ephemeral preview envs)
   - Database provisioning (PostgreSQL, MongoDB)
   - Secrets management (Vault, External Secrets)
   - Observability (metrics, logs, traces)
   - Security scanning (SAST, DAST, SCA)

4. **Infrastructure Layer** (Foundation)
   - Kubernetes clusters (multi-region, multi-cloud)
   - Container registries
   - Networking (service mesh, ingress)
   - Storage (persistent volumes, object storage)

5. **Integration Layer** (Connections)
   - Source control (GitHub, GitLab)
   - Identity providers (SSO, RBAC)
   - Cloud providers (AWS, Azure, GCP)
   - Third-party services (PagerDuty, Slack)

### Platform Capability Model

Every platform capability should follow this structure:

```yaml
capability:
  name: postgresql-database
  type: data-store
  self_service: true

  interface:
    portal: backstage-template
    api: kubernetes-crd
    cli: platform-cli

  golden_path:
    default_config: production-ready
    escape_hatches: advanced-config-available

  lifecycle:
    provision_time: "< 5 minutes"
    automation_level: "100% automated"

  governance:
    policies: [backup-daily, encryption-at-rest]
    compliance: [pci-dss, soc2]

  observability:
    metrics: [connections, query-latency, storage-usage]
    alerts: [high-connections, replication-lag]
    dashboards: grafana-postgresql
```

## Backstage.io Implementation

### Why Backstage?

Backstage is the leading open-source developer portal platform created by Spotify. It provides:

- **Software Catalog**: Single pane of glass for all software
- **Software Templates**: Scaffolding for new services
- **TechDocs**: Documentation alongside code
- **Plugins**: Extensible ecosystem (K8s, CI/CD, cloud)
- **Search**: Unified search across all platform resources

### Backstage Architecture

```
┌──────────────────────────────────────────────────┐
│           Backstage Frontend (React)              │
├──────────────────────────────────────────────────┤
│  Catalog │ Templates │ TechDocs │ Search │ K8s   │  ← Core Plugins
├──────────────────────────────────────────────────┤
│          Backstage Backend (Node.js)              │
│  - Catalog API                                    │
│  - Scaffolder Service                             │
│  - TechDocs Generator                             │
│  - Search Indexer                                 │
├──────────────────────────────────────────────────┤
│  PostgreSQL │ GitHub │ K8s │ ArgoCD │ Jenkins    │  ← Integrations
└──────────────────────────────────────────────────┘
```

### Software Catalog Design

The catalog is defined using `catalog-info.yaml` files:

**Entity Types:**
- **Component**: Services, libraries, websites
- **API**: REST, GraphQL, gRPC interfaces
- **Resource**: Databases, queues, storage buckets
- **System**: Collection of components
- **Domain**: Business capability area
- **Group**: Teams and organizational units
- **User**: Individual engineers
- **Template**: Service scaffolding templates

**Catalog Organization Patterns:**

1. **Monorepo Pattern**: Single `catalog-info.yaml` at root
2. **Polyrepo Pattern**: `catalog-info.yaml` in each repo
3. **Centralized Pattern**: Central catalog repo with all definitions
4. **Hybrid Pattern**: Repos own components, platform owns resources

### Software Templates (Scaffolder)

Templates enable developers to create new services following golden paths:

**Template Structure:**
```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: nodejs-microservice
  title: Node.js Microservice
spec:
  owner: platform-team
  type: service

  parameters:
    - title: Service Information
      properties:
        name: { type: string }
        description: { type: string }
        owner: { type: string, ui:field: OwnerPicker }

  steps:
    - id: fetch-base
      name: Fetch Template
      action: fetch:template

    - id: create-repo
      name: Create GitHub Repository
      action: publish:github

    - id: register-catalog
      name: Register in Catalog
      action: catalog:register
```

**Golden Template Categories:**

1. **Service Templates**
   - Microservice (Node.js, Python, Go, Java)
   - API Gateway
   - Background worker
   - Serverless function

2. **Data Templates**
   - PostgreSQL database
   - MongoDB cluster
   - Redis cache
   - S3 bucket

3. **Infrastructure Templates**
   - Kubernetes namespace
   - CI/CD pipeline
   - Monitoring dashboard
   - Load balancer

### Backstage Plugins Ecosystem

**Essential Plugins:**

1. **Kubernetes Plugin**
   - View pods, deployments, services
   - Real-time logs and metrics
   - Resource health status

2. **ArgoCD Plugin**
   - Deployment status
   - Sync health
   - Application history

3. **GitHub Plugin**
   - Pull requests
   - Actions workflows
   - Repository insights

4. **PagerDuty Plugin**
   - On-call schedules
   - Recent incidents
   - Service dependencies

5. **Cost Insights Plugin**
   - Cloud spend by service
   - Cost trending
   - Budget alerts

**Custom Plugin Development:**

```typescript
// plugins/platform-metrics/src/plugin.ts
export const platformMetricsPlugin = createPlugin({
  id: 'platform-metrics',
  apis: [
    createApiFactory({
      api: platformMetricsApiRef,
      deps: { discoveryApi: discoveryApiRef },
      factory: ({ discoveryApi }) => new PlatformMetricsClient(discoveryApi),
    }),
  ],
  routes: {
    root: rootRouteRef,
  },
});
```

## Golden Paths and Paved Roads

### What are Golden Paths?

Golden paths are the opinionated, well-lit, production-ready paths that make the right thing the easy thing. They're not mandatory, but they're so good that developers choose them.

**Golden Path Characteristics:**

- **Opinionated**: Pre-configured with best practices
- **Complete**: From local dev to production
- **Documented**: Clear, always-updated docs
- **Tested**: Battle-tested in production
- **Escapable**: Advanced users can deviate

### Golden Path Categories

#### 1. Service Creation Golden Path

```
Developer Action → Platform Response → Outcome
───────────────────────────────────────────────
Fill template → Scaffold repo → Repo created
                ↓
Commit code → Trigger CI → Tests pass
                ↓
Merge PR → Deploy staging → Auto-deployed
                ↓
Approve → Deploy prod → Live in production
                ↓
Monitor → Auto-dashboards → Observability ready
```

**Included by Default:**
- Project structure
- Dependency management
- Testing framework
- CI/CD pipeline
- Dockerfile (multi-stage, optimized)
- Kubernetes manifests
- Monitoring instrumentation
- Security scanning
- Documentation template

#### 2. Database Provisioning Golden Path

```
Request DB → Select template → Backstage template filled
             ↓
Platform → Provision (Crossplane) → RDS instance created
           ↓
Platform → Configure → Backups, encryption enabled
           ↓
Platform → Inject secrets → App can connect
           ↓
Platform → Monitor → Dashboards auto-created
```

**Included:**
- Production-ready configuration
- Automated backups
- Encryption at rest
- Connection pooling
- Monitoring and alerting
- Cost tagging

#### 3. Environment Management Golden Path

```
Service exists → Define environments → YAML config
                 ↓
Platform → Create namespaces → Dev, staging, prod
           ↓
Platform → Configure networking → Ingress, service mesh
           ↓
Platform → Set policies → RBAC, network policies
           ↓
Platform → Enable preview envs → PR-based ephemeral envs
```

**Environments:**
- **Development**: Developer-owned, relaxed policies
- **Staging**: Production-like, testing ground
- **Production**: High-availability, strict policies
- **Preview**: Ephemeral, PR-triggered

### Escape Hatches

Golden paths must have escape hatches for advanced use cases:

**Escape Hatch Levels:**

1. **Configuration Overrides** (Easy)
   - Override default values
   - Add custom environment variables
   - Adjust resource limits

2. **Custom Resources** (Moderate)
   - Add additional K8s resources
   - Custom init containers
   - Sidecar containers

3. **Full Control** (Advanced)
   - Bring your own manifests
   - Custom Helm charts
   - Direct infrastructure access

**Implementation:**

```yaml
# score.yaml - Platform abstraction
apiVersion: score.dev/v1b1
metadata:
  name: my-service

containers:
  web:
    image: my-app:latest

resources:
  database:
    type: postgres  # Platform provides

# Escape hatch: Advanced configuration
advanced:
  database:
    custom_config: |
      max_connections: 500
      shared_buffers: 2GB
```

## Platform Capabilities Design

### Core Platform Capabilities

#### 1. CI/CD Capability

**Requirements:**
- Trigger on git push
- Run tests automatically
- Build container images
- Deploy to environments
- Rollback on failure

**Implementation Stack:**
- GitHub Actions / GitLab CI
- Tekton for K8s-native pipelines
- ArgoCD for GitOps deployments
- Kaniko for container builds

**Developer Experience:**
```bash
# Developer workflow
git commit -m "Add feature"
git push

# Platform automatically:
# 1. Runs tests
# 2. Builds image
# 3. Deploys to dev
# 4. Creates preview env (if PR)
```

#### 2. Database Provisioning Capability

**Requirements:**
- Self-service database creation
- Multiple database types (PostgreSQL, MySQL, MongoDB)
- Production-ready configuration
- Automated backups
- Secret injection

**Implementation Stack:**
- Crossplane for cloud database provisioning
- CloudNativePG for in-cluster PostgreSQL
- External Secrets for credential management

**Developer Experience:**
```yaml
# In Backstage template or score.yaml
resources:
  user_db:
    type: postgresql
    params:
      size: small  # small, medium, large
      backup: daily
```

#### 3. Secrets Management Capability

**Requirements:**
- Secure secret storage
- Automatic rotation
- Injection into workloads
- Audit logging
- Multi-environment support

**Implementation Stack:**
- HashiCorp Vault (storage)
- External Secrets Operator (K8s integration)
- Cert-manager (certificate management)

**Developer Experience:**
```yaml
# Declarative secret reference
env:
  - name: DB_PASSWORD
    valueFrom:
      secretRef:
        name: user-db-credentials
        key: password
# Platform handles creation, rotation, injection
```

#### 4. Observability Capability

**Requirements:**
- Metrics collection (RED/USE)
- Log aggregation
- Distributed tracing
- Auto-generated dashboards
- Smart alerting

**Implementation Stack:**
- Prometheus (metrics)
- Loki (logs)
- Tempo (traces)
- Grafana (visualization)
- OpenTelemetry (instrumentation)

**Developer Experience:**
```
# Platform provides automatically:
- Service dashboard (requests, errors, latency)
- Log search interface
- Trace visualization
- Default alerts (error rate, latency)
```

#### 5. Preview Environments Capability

**Requirements:**
- Ephemeral environments per PR
- Identical to production
- Automatic cleanup
- Shareable URLs
- Cost-effective

**Implementation Stack:**
- Namespace-per-PR pattern
- ArgoCD ApplicationSet
- Ingress with dynamic routing
- TTL-based cleanup

**Developer Experience:**
```bash
# Create PR
gh pr create

# Platform automatically:
# - Creates namespace
# - Deploys branch
# - Generates URL: pr-123.preview.company.com
# - Comments URL on PR
# - Deletes after 7 days or PR merge
```

### Platform Capability Maturity Model

**Level 1: Manual** (Ticket-based)
- Submit ticket to ops team
- Wait for provisioning
- Manual configuration
- No self-service

**Level 2: Automated** (Script-based)
- Run scripts to provision
- Some automation
- Still requires knowledge
- Error-prone

**Level 3: Self-Service** (Portal-based)
- Fill form in portal
- Automated provisioning
- Pre-configured best practices
- Consistent results

**Level 4: Invisible** (Platform-as-Code)
- Declare in code
- Platform auto-provisions
- Zero manual steps
- Developer doesn't think about it

**Goal:** Move all capabilities to Level 3 (Self-Service) or Level 4 (Invisible)

## Platform Metrics and Feedback Loops

### DORA Metrics

Track platform impact using DORA (DevOps Research and Assessment) metrics:

1. **Deployment Frequency**: How often deploys to production
   - Target: Multiple times per day
   - Platform lever: Automated pipelines, preview environments

2. **Lead Time for Changes**: Code commit to production
   - Target: < 1 hour
   - Platform lever: Fast CI/CD, automated testing

3. **Time to Restore Service**: Incident to recovery
   - Target: < 1 hour
   - Platform lever: Auto-rollback, canary deployments

4. **Change Failure Rate**: % of deployments causing incidents
   - Target: < 5%
   - Platform lever: Testing, progressive delivery

### Platform-Specific Metrics

**Adoption Metrics:**
- % of services using platform
- % of deployments via platform
- Golden path usage rate

**Experience Metrics:**
- Time to first deployment (new service)
- Time to provision resource (database, etc)
- Support ticket volume (lower is better)

**Satisfaction Metrics:**
- Developer NPS (Net Promoter Score)
- Platform satisfaction surveys
- Feature request volume

**Operational Metrics:**
- Platform uptime (99.9%+)
- API response times
- Resource provisioning success rate

### Feedback Loops

**1. Quantitative Feedback:**
```yaml
# Instrument platform APIs
POST /api/v1/provision/database
  - metric: provision_duration_seconds
  - metric: provision_success_total
  - metric: provision_failures_total

# Dashboard per capability
Grafana dashboard:
  - Average provision time
  - Success rate
  - Error breakdown
```

**2. Qualitative Feedback:**
```yaml
# Regular developer surveys (quarterly)
questions:
  - "How satisfied are you with the platform?"
  - "What capability would help you most?"
  - "What's your biggest pain point?"

# Office hours (weekly)
format: Drop-in sessions
goal: Face-to-face feedback
outcome: Feature ideas, pain points

# Feedback slack channel
channel: #platform-feedback
monitored: Daily
response_sla: 24 hours
```

**3. Usage Analytics:**
```yaml
# Track template usage
templates:
  nodejs-service: 45 uses/month
  python-service: 23 uses/month
  database: 67 uses/month

# Identify unused capabilities
capabilities:
  redis: 2 uses/month → consider deprecating?
  kafka: 45 uses/month → keep and improve
```

## Team Topologies and Platform Teams

### Team Topologies Model

Based on the book "Team Topologies" by Matthew Skelton and Manuel Pais:

**Four Team Types:**

1. **Stream-Aligned Teams** (Product teams)
   - Build and run services
   - Aligned to business capabilities
   - Primary customers of platform

2. **Platform Teams** (Your team)
   - Build and run the IDP
   - Enable stream-aligned teams
   - Reduce cognitive load

3. **Enabling Teams**
   - Coaching and mentoring
   - Help teams adopt new technologies
   - Temporary assistance

4. **Complicated-Subsystem Teams**
   - Specialized subsystems (ML, search)
   - Deep expertise required
   - Long-lived teams

### Platform Team Structure

**Recommended Structure:**

```
Platform Team (8-12 people)
├── Platform Product Manager (1)
│   └── Roadmap, prioritization, user research
├── Platform Engineering Squad (4-6)
│   ├── Backend engineers (orchestration, APIs)
│   ├── Frontend engineer (Backstage portal)
│   └── SRE/Infrastructure (K8s, cloud)
├── Developer Experience Engineer (1-2)
│   └── Documentation, templates, onboarding
└── Platform SRE (1-2)
    └── Platform reliability, monitoring
```

**Responsibilities:**

- **Product Manager**: Treat platform as a product
- **Engineers**: Build and maintain capabilities
- **DX Engineer**: Focus on developer experience
- **SRE**: Keep platform reliable and performant

### Interaction Modes

**1. Self-Service (Preferred)**
- Developer uses portal, no interaction needed
- Fully automated golden paths
- Documentation and discoverability

**2. Enabling**
- Platform team helps with onboarding
- Workshops and training sessions
- Office hours and pairing

**3. Collaboration (Limited)**
- Complex migrations
- New capability development
- Platform team works alongside product teams

### Team Metrics

**Team Health Metrics:**

1. **Cognitive Load Score**: Survey stream-aligned teams
   - "Do you feel overwhelmed by tooling complexity?"
   - Target: < 3/10 complexity score

2. **Time to Value**: Measure platform impact
   - Time from idea to production (before vs after)
   - Target: 80% reduction

3. **Support Burden**: Track platform team time
   - % time on support vs building
   - Target: < 20% on support

## Platform Engineering Best Practices

### Design Principles

**1. Developer-Centric Design**
```yaml
principle: Start with developer needs
anti_pattern: Build what you think they need
approach:
  - User research with developers
  - Observe their workflows
  - Measure pain points
  - Co-design solutions
```

**2. Progressive Disclosure**
```yaml
principle: Simple by default, powerful when needed
anti_pattern: Expose all options upfront
approach:
  - Level 1: Use defaults (95% use case)
  - Level 2: Configure via UI
  - Level 3: YAML configuration
  - Level 4: Full infrastructure access
```

**3. Paved Paths, Not Paved Prisons**
```yaml
principle: Golden paths, but not mandatory
anti_pattern: Force everyone to use platform
approach:
  - Make golden paths so good they're chosen
  - Allow escape hatches
  - Support "bring your own"
  - Measure adoption, don't mandate
```

**4. Platform as a Product**
```yaml
principle: Treat internal platform like external product
practices:
  - Product roadmap
  - User research
  - Feature prioritization
  - Marketing and onboarding
  - Deprecation policies
  - SLAs and support
```

**5. Everything as Code**
```yaml
principle: All platform configuration in Git
benefits:
  - Version control
  - Code review
  - Audit trail
  - Disaster recovery
  - Reproducibility
```

### Security and Governance

**1. Secure by Default**
```yaml
template: nodejs-microservice
includes:
  - Container image scanning
  - Dependency vulnerability checks
  - Secret scanning in code
  - Network policies (deny by default)
  - Pod security policies
  - HTTPS/TLS by default
```

**2. Policy as Code**
```yaml
# OPA/Kyverno policies
policies:
  - require-labels: [owner, cost-center, environment]
  - require-resource-limits: all containers
  - block-privileged-containers: true
  - require-readonly-root-filesystem: true
  - enforce-image-sources: [company-registry]
```

**3. Audit and Compliance**
```yaml
audit_trail:
  - Who provisioned what resource
  - When was it created
  - What configuration was used
  - Who has access

compliance_reports:
  - SOC 2 evidence
  - PCI-DSS controls
  - GDPR data inventory
```

### Migration Strategies

**Migrating Existing Services to Platform:**

**Phase 1: Catalog (Month 1-2)**
- Import existing services into Backstage
- Create catalog entries
- Build ownership graph

**Phase 2: Visibility (Month 2-3)**
- Integrate monitoring dashboards
- Connect CI/CD status
- Link documentation

**Phase 3: Onboarding (Month 3-6)**
- Migrate 1-2 pilot services to golden paths
- Gather feedback, iterate
- Create migration runbooks

**Phase 4: Adoption (Month 6-12)**
- Migrate 10-20% of services
- Offer migration assistance
- Track metrics and celebrate wins

**Phase 5: Scale (Month 12+)**
- Majority of new services use platform
- Gradual migration of legacy services
- Platform becomes default choice

### Common Pitfalls

**1. Building for Yourself, Not Users**
```yaml
mistake: Platform team builds what they think is cool
fix: Regular user research, feedback loops
indicator: Low adoption despite great tech
```

**2. Too Much Abstraction**
```yaml
mistake: Hide everything, no escape hatches
fix: Progressive disclosure, allow overrides
indicator: Developers bypass platform for flexibility
```

**3. Ignoring Change Management**
```yaml
mistake: Build platform, assume adoption
fix: Marketing, onboarding, enablement
indicator: "Build it and they will come" didn't work
```

**4. Measuring Outputs, Not Outcomes**
```yaml
mistake: Count features shipped
fix: Measure developer satisfaction, time to production
indicator: Platform growing but not delivering value
```

**5. No Product Thinking**
```yaml
mistake: Treat platform as infrastructure project
fix: Dedicated PM, roadmap, user feedback
indicator: Platform feels like internal IT
```

## Bilingual Support / Двуязычная поддержка

### Russian Language Support / Русская языковая поддержка

**Платформенная инженерия — это дисциплина проектирования и создания инструментов и рабочих процессов, обеспечивающих самообслуживание для разработчиков в облачной среде.**

**Ключевые концепции:**

- **IDP (Internal Developer Platform)** — Внутренняя платформа разработчика
- **Golden Path** — Золотой путь (рекомендуемый подход)
- **Self-Service** — Самообслуживание
- **Developer Portal** — Портал разработчика
- **Platform Capabilities** — Возможности платформы

**Пример использования Backstage:**

```yaml
# catalog-info.yaml - описание сервиса
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: user-service
  title: Сервис пользователей
  description: Микросервис управления пользователями
  annotations:
    backstage.io/kubernetes-label-selector: 'app=user-service'
spec:
  type: service
  owner: team-backend
  lifecycle: production
```

## Troubleshooting and Common Issues

### Issue 1: Low Platform Adoption

**Symptoms:**
- Developers still submit tickets
- Platform usage metrics low
- Continued shadow IT

**Diagnosis:**
- Survey developers on blockers
- Analyze where they bypass platform
- Compare platform vs manual effort

**Solutions:**
1. Improve documentation and discoverability
2. Run onboarding workshops
3. Add missing capabilities
4. Reduce friction in existing flows
5. Marketing and communication

### Issue 2: Backstage Performance Issues

**Symptoms:**
- Slow catalog loading
- Template scaffolding timeouts
- Search unresponsive

**Diagnosis:**
```bash
# Check backend logs
kubectl logs -n backstage backstage-backend

# Check database performance
# Catalog has too many entities?

# Check integration timeouts
# GitHub API rate limits?
```

**Solutions:**
1. Optimize catalog ingestion (batch updates)
2. Add caching layer (Redis)
3. Scale backend horizontally
4. Tune PostgreSQL (connection pool, indexes)
5. Use catalog refresh scheduling

### Issue 3: Template Scaffolding Failures

**Symptoms:**
- Templates fail to create repos
- Missing files in scaffolded projects
- Errors during scaffolding

**Diagnosis:**
```bash
# Check scaffolder logs
kubectl logs -n backstage backstage-backend | grep scaffolder

# Validate template syntax
backstage-cli repo schema openapi verify

# Test template actions manually
```

**Solutions:**
1. Validate template YAML syntax
2. Check GitHub token permissions
3. Verify template path references
4. Test actions in isolation
5. Add error handling in custom actions

### Issue 4: Platform Team Overloaded

**Symptoms:**
- Platform team spending 80% time on support
- Backlog not moving
- Developer satisfaction dropping

**Diagnosis:**
- Analyze support ticket categories
- Identify repetitive requests
- Find missing capabilities

**Solutions:**
1. Automate common requests (more self-service)
2. Improve documentation (reduce "how to" questions)
3. Add FAQ and troubleshooting guides
4. Office hours instead of ad-hoc support
5. Hire enabling team member

## Advanced Topics

### Multi-Tenancy Patterns

**Namespace-per-Team:**
```yaml
# Platform creates isolated namespaces
apiVersion: v1
kind: Namespace
metadata:
  name: team-backend
  labels:
    team: backend
    platform-managed: "true"
---
# Network policies for isolation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: team-backend
spec:
  podSelector: {}
  policyTypes:
    - Ingress
```

**Resource Quotas per Team:**
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-backend-quota
  namespace: team-backend
spec:
  hard:
    pods: "100"
    requests.cpu: "40"
    requests.memory: "100Gi"
    persistentvolumeclaims: "20"
```

### Cost Management

**Chargeback Model:**
```yaml
# Tag all resources with cost center
metadata:
  labels:
    cost-center: engineering
    team: backend
    environment: production

# Generate monthly reports
# Show cost per team, per environment
# Enable informed decisions
```

**Cost Optimization Golden Paths:**
- Right-sized resource requests
- Horizontal pod autoscaling by default
- Spot instances for non-production
- Automatic cleanup of unused resources

### Compliance Automation

**Automated Compliance Checks:**
```yaml
# Platform validates before provisioning
pre_provision_checks:
  - data_residency: Ensure data in correct region
  - encryption: Verify encryption enabled
  - backup: Confirm backup configured
  - access_control: Check RBAC policies

# Continuous compliance scanning
compliance_scans:
  - frequency: daily
  - report: to security team
  - remediation: automated where possible
```

## References and Resources

See the following reference materials for detailed patterns and examples:

- **[IDP Patterns](./references/idp-patterns.md)** - Internal Developer Platform architecture patterns and capability mapping
- **[Backstage Guide](./references/backstage-guide.md)** - Comprehensive Backstage setup, software catalog design, and template creation
- **[Golden Paths](./references/golden-paths.md)** - Golden path templates, scaffolding patterns, and self-service workflows

See the assets directory for ready-to-use examples:

- **[Backstage Catalog Examples](./assets/backstage-catalog.yaml)** - Software catalog entity definitions
- **[Backstage Template Examples](./assets/backstage-template.yaml)** - Service scaffolding templates
- **[Platform Capabilities](./assets/platform-capabilities.yaml)** - Platform capability definitions and configurations

## External Resources

**Books:**
- "Team Topologies" by Matthew Skelton and Manuel Pais
- "Platform Engineering" by Kaspar von Grünberg
- "The DevOps Handbook" by Gene Kim et al.

**Frameworks:**
- Backstage.io - https://backstage.io
- Crossplane - https://crossplane.io
- Score - https://score.dev
- Humanitec - https://humanitec.com

**Communities:**
- Platform Engineering Community - https://platformengineering.org
- CNCF Platforms Working Group
- Backstage Discord Community

**Podcasts and Talks:**
- PlatformCon (annual conference)
- "What is Platform Engineering?" by Kaspar von Grünberg
- Backstage Community Sessions
