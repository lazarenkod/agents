# Internal Developer Platform (IDP) Architecture Patterns

## Overview

This reference provides detailed architecture patterns for building Internal Developer Platforms at scale, based on production implementations from AWS, Azure, Google Cloud, and leading tech companies.

## IDP Architecture Patterns

### Pattern 1: Layered IDP Architecture

**Description:** Separates concerns into distinct layers with clear boundaries.

```
┌─────────────────────────────────────────────────────────────┐
│  Developer Interface Layer                                   │
│  - Backstage Portal (UI)                                     │
│  - CLI Tools                                                 │
│  - IDE Plugins                                               │
│  - API Gateway                                               │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Platform Orchestration Layer                                │
│  - Crossplane (Infrastructure as Code)                       │
│  - ArgoCD (GitOps)                                          │
│  - Terraform (Cloud Resources)                              │
│  - Kyverno/OPA (Policy Enforcement)                         │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Platform Capabilities Layer                                 │
│  - CI/CD (Tekton, GitHub Actions)                           │
│  - Databases (CloudNativePG, RDS)                           │
│  - Secrets (Vault, External Secrets)                        │
│  - Observability (Prometheus, Loki, Tempo)                  │
│  - Security (Falco, Trivy, OPA)                             │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Infrastructure Layer                                        │
│  - Kubernetes Clusters (EKS, AKS, GKE)                      │
│  - Container Registry (ECR, ACR, GCR)                       │
│  - Networking (VPC, Service Mesh)                           │
│  - Storage (EBS, Azure Disk, Persistent Disks)              │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Integration Layer                                           │
│  - Cloud Providers (AWS, Azure, GCP)                        │
│  - Source Control (GitHub, GitLab)                          │
│  - Identity (Okta, Azure AD, Auth0)                         │
│  - Monitoring (Datadog, New Relic, Grafana Cloud)           │
└─────────────────────────────────────────────────────────────┘
```

**When to Use:**
- Large organizations with multiple teams
- Need clear separation of concerns
- Supports multiple cloud providers
- Requires different scaling characteristics per layer

**Implementation Considerations:**
- Each layer has independent scaling
- Clear API contracts between layers
- Layer-specific SLAs
- Independent upgrade cycles

### Pattern 2: Hub and Spoke Platform

**Description:** Central platform hub with spoke services for different capabilities.

```
                    ┌──────────────────┐
                    │  Platform Hub    │
                    │  (Backstage)     │
                    │  - Catalog       │
                    │  - Templates     │
                    │  - Docs          │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  CI/CD Spoke  │    │ Database Spoke│    │Security Spoke │
│  (Tekton)     │    │ (Crossplane)  │    │ (Vault)       │
│               │    │               │    │               │
│ - Pipelines   │    │ - PostgreSQL  │    │ - Secrets     │
│ - Workflows   │    │ - MongoDB     │    │ - Certs       │
│ - Artifacts   │    │ - Redis       │    │ - KMS         │
└───────────────┘    └───────────────┘    └───────────────┘
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│Observability  │    │ Networking    │    │ Cost Mgmt     │
│Spoke          │    │ Spoke         │    │ Spoke         │
│(Prometheus)   │    │(Istio/Cilium) │    │(Kubecost)     │
└───────────────┘    └───────────────┘    └───────────────┘
```

**When to Use:**
- Independent capability teams
- Each spoke can evolve independently
- Need flexibility in technology choices
- Gradual platform capability adoption

**Implementation Considerations:**
- Spokes register with hub
- Hub aggregates status from spokes
- Spoke APIs standardized
- Each spoke has its own SLA

### Pattern 3: Platform-as-Code (Score/Humanitec Pattern)

**Description:** Developers declare desired state; platform materializes it.

```
Developer Workflow:
┌─────────────────────────────────────────────────────────┐
│ 1. Developer writes score.yaml (workload spec)          │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Platform Orchestrator translates to infrastructure   │
│    - score.yaml → Kubernetes manifests                  │
│    - Resources → Cloud provider resources               │
│    - Dependencies → Service connections                 │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 3. GitOps applies configuration                         │
│    - ArgoCD/Flux deploys to cluster                     │
│    - Crossplane provisions cloud resources              │
│    - External Secrets injects credentials               │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Platform maintains desired state                     │
│    - Reconciliation loops                               │
│    - Self-healing                                       │
│    - Drift detection                                    │
└─────────────────────────────────────────────────────────┘
```

**Score Specification Example:**
```yaml
# score.yaml
apiVersion: score.dev/v1b1
metadata:
  name: user-service

service:
  ports:
    web:
      port: 8080
      protocol: TCP

containers:
  web:
    image: user-service:latest
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 500m
        memory: 512Mi

resources:
  database:
    type: postgres
    properties:
      version: "15"

  cache:
    type: redis

  queue:
    type: sqs
```

**Platform Translates to:**
```yaml
# Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: web
        image: user-service:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: user-service-db
              key: url
---
# Crossplane Composite Resource
apiVersion: database.platform.company.com/v1alpha1
kind: PostgreSQLInstance
metadata:
  name: user-service-db
spec:
  parameters:
    version: "15"
    storageGB: 100
    instanceType: db.t3.medium
---
# External Secret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: user-service-db
spec:
  secretStoreRef:
    name: vault-backend
  target:
    name: user-service-db
  data:
  - secretKey: url
    remoteRef:
      key: database/user-service/url
```

**When to Use:**
- Want to abstract cloud complexity
- Developers shouldn't know Kubernetes
- Need portable workload definitions
- Multi-cloud or hybrid cloud

**Implementation Considerations:**
- Define resource abstractions upfront
- Create translation logic (score → K8s)
- Handle edge cases and overrides
- Version abstraction API carefully

### Pattern 4: Golden Path Templates (Backstage-Centric)

**Description:** Pre-built templates for common use cases.

```
Developer Experience:
┌────────────────────────────────────────────────┐
│ 1. Browse Template Catalog                     │
│    - Node.js Microservice                      │
│    - Python Data Service                       │
│    - Go API Gateway                            │
│    - React Frontend                            │
└────────────────┬───────────────────────────────┘
                 ▼
┌────────────────────────────────────────────────┐
│ 2. Fill Template Form                          │
│    Service Name: user-service                  │
│    Owner: team-backend                         │
│    Database: PostgreSQL                        │
│    Cache: Redis                                │
└────────────────┬───────────────────────────────┘
                 ▼
┌────────────────────────────────────────────────┐
│ 3. Platform Scaffolds (15-30 seconds)          │
│    ✓ GitHub repo created                       │
│    ✓ Code scaffolded (app + tests)             │
│    ✓ CI/CD pipeline configured                 │
│    ✓ Kubernetes manifests generated            │
│    ✓ Monitoring dashboards created             │
│    ✓ Database provisioned                      │
│    ✓ Secrets injected                          │
│    ✓ Service registered in catalog             │
└────────────────┬───────────────────────────────┘
                 ▼
┌────────────────────────────────────────────────┐
│ 4. Developer Ready to Code                     │
│    $ git clone repo && npm start               │
│    Service running locally in 2 minutes        │
└────────────────────────────────────────────────┘
```

**Template Architecture:**
```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: nodejs-microservice
spec:
  owner: platform-team
  type: service

  parameters:
    - title: Service Information
      required: [name, owner]
      properties:
        name:
          type: string
          ui:autofocus: true
        owner:
          type: string
          ui:field: OwnerPicker
        database:
          type: string
          enum: [postgres, mysql, mongodb, none]
          default: postgres

  steps:
    # Step 1: Fetch template from GitHub
    - id: fetch-base
      name: Fetch Base Template
      action: fetch:template
      input:
        url: ./templates/nodejs-microservice
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}

    # Step 2: Create GitHub repository
    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        repoUrl: github.com?owner=company&repo=${{ parameters.name }}

    # Step 3: Provision database (if needed)
    - id: create-database
      if: ${{ parameters.database !== 'none' }}
      name: Provision Database
      action: http:backstage:request
      input:
        method: POST
        path: /api/v1/databases
        body:
          type: ${{ parameters.database }}
          name: ${{ parameters.name }}-db

    # Step 4: Configure CI/CD
    - id: setup-cicd
      name: Setup CI/CD Pipeline
      action: github:actions:dispatch
      input:
        repoUrl: github.com?owner=company&repo=${{ parameters.name }}
        workflowId: setup-pipeline.yml

    # Step 5: Register in catalog
    - id: register
      name: Register Component
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml

  output:
    links:
      - title: Repository
        url: ${{ steps.publish.output.remoteUrl }}
      - title: Pipeline
        url: ${{ steps.publish.output.remoteUrl }}/actions
      - title: Catalog Entry
        url: /catalog/default/component/${{ parameters.name }}
```

**When to Use:**
- Want consistent service structure
- Need fast onboarding for new developers
- Standardize best practices
- Reduce copy-paste errors

### Pattern 5: Multi-Cloud Abstraction

**Description:** Single platform interface for multiple cloud providers.

```
┌──────────────────────────────────────────────┐
│         Platform Abstraction Layer            │
│   (Unified API for all cloud resources)      │
└────────────┬──────────────┬──────────────────┘
             │              │
     ┌───────▼─────┐  ┌────▼────────┐  ┌───────▼──────┐
     │  AWS Impl   │  │ Azure Impl  │  │  GCP Impl    │
     └─────────────┘  └─────────────┘  └──────────────┘
```

**Abstraction Example (Crossplane):**
```yaml
# Abstract database definition
apiVersion: database.platform.company.com/v1alpha1
kind: Database
metadata:
  name: user-db
spec:
  type: postgresql
  size: medium
  region: us-east
  backup:
    enabled: true
    retention: 30

---
# Composition maps to cloud provider
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: database-aws
spec:
  compositeTypeRef:
    apiVersion: database.platform.company.com/v1alpha1
    kind: Database
  resources:
    - name: rds-instance
      base:
        apiVersion: rds.aws.crossplane.io/v1alpha1
        kind: DBInstance
        spec:
          forProvider:
            engine: postgres
            instanceClass: db.t3.medium  # medium = t3.medium
            allocatedStorage: 100
            backupRetentionPeriod: 30

---
# Alternative composition for Azure
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: database-azure
spec:
  compositeTypeRef:
    apiVersion: database.platform.company.com/v1alpha1
    kind: Database
  resources:
    - name: azure-postgres
      base:
        apiVersion: dbforpostgresql.azure.crossplane.io/v1alpha1
        kind: Server
        spec:
          forProvider:
            sku:
              tier: GeneralPurpose
              capacity: 2  # medium = 2 vCores
            storageProfile:
              storageMB: 102400
              backupRetentionDays: 30
```

**When to Use:**
- Multi-cloud strategy
- Want to avoid cloud lock-in
- Need to migrate between clouds
- Compliance requires data residency

**Implementation Considerations:**
- Define cloud-agnostic abstractions
- Handle cloud-specific features carefully
- Test on all target clouds
- Document cloud-specific limitations

## Capability Mapping

### Core Capabilities Matrix

| Capability | Developer Facing | Implementation | Maturity Target |
|------------|------------------|----------------|-----------------|
| **Service Creation** | Backstage template | GitHub + Scaffolder | Self-Service |
| **CI/CD** | Auto-configured on git push | GitHub Actions / Tekton | Invisible |
| **Kubernetes Deploy** | GitOps (declarative) | ArgoCD / Flux | Invisible |
| **Database** | Request via template | Crossplane + CloudNativePG | Self-Service |
| **Secrets** | Declare reference | External Secrets + Vault | Invisible |
| **Observability** | Auto-dashboards | Prometheus + Grafana | Invisible |
| **Logs** | Search UI | Loki + Grafana | Self-Service |
| **Traces** | Auto-instrumentation | OpenTelemetry + Tempo | Invisible |
| **Networking** | Service + Ingress | Istio / Cilium | Self-Service |
| **TLS/Certificates** | Auto-provisioned | cert-manager | Invisible |
| **Preview Envs** | Auto on PR | Namespace + ArgoCD | Invisible |
| **Cost Visibility** | Dashboard per service | Kubecost / OpenCost | Self-Service |
| **Security Scanning** | Auto in CI | Trivy + Snyk | Invisible |
| **Policy Enforcement** | Transparent checks | Kyverno / OPA | Invisible |

### Capability Maturity Model

**Level 0: None**
- Capability doesn't exist
- Manual, tribal knowledge

**Level 1: Manual**
- Submit ticket to ops team
- Human performs task
- Inconsistent results

**Level 2: Automated**
- Scripts exist
- Developer must run them
- Requires technical knowledge

**Level 3: Self-Service**
- Portal or CLI
- Automated provisioning
- Consistent, tested results

**Level 4: Invisible**
- Declared in code
- Platform auto-provisions
- Developer doesn't think about it

### Capability Design Template

For each platform capability, define:

```yaml
capability_name: database-provisioning

# 1. Interface
interface:
  primary: backstage-template
  secondary: kubectl-crd
  api: platform-api-v1

# 2. Developer Experience
developer_experience:
  request_method: Fill template form
  provision_time: "< 5 minutes"
  approval_required: false
  self_service: true

# 3. Implementation
implementation:
  orchestrator: crossplane
  providers:
    - aws-rds
    - azure-postgresql
    - cloudnative-pg
  configuration: gitops
  secrets: external-secrets-operator

# 4. Governance
governance:
  policies:
    - enforce-backups
    - require-encryption
    - limit-instance-sizes
  compliance:
    - pci-dss
    - soc2
  cost_controls:
    - budget-alerts
    - auto-shutdown-dev

# 5. Operations
operations:
  monitoring:
    - connection-count
    - query-latency
    - storage-usage
  alerting:
    - high-connections
    - replication-lag
    - backup-failures
  backup:
    frequency: daily
    retention: 30-days
  disaster_recovery:
    rto: 4-hours
    rpo: 24-hours

# 6. Documentation
documentation:
  getting_started: docs/database/quickstart.md
  advanced: docs/database/advanced.md
  troubleshooting: docs/database/troubleshooting.md
  examples: templates/database-examples/

# 7. Support
support:
  sla: 4-hour response
  escalation: platform-team-oncall
  feedback: #platform-database-feedback
```

## Reference Architectures

### Small Company (< 50 Engineers)

**Recommended Stack:**
```yaml
interface: Backstage (simplified)
orchestration: ArgoCD + Terraform
capabilities:
  - cicd: GitHub Actions
  - database: AWS RDS (managed)
  - secrets: AWS Secrets Manager
  - monitoring: Grafana Cloud

team_size: 2-3 platform engineers
focus: Reduce toil, standard templates
```

### Medium Company (50-200 Engineers)

**Recommended Stack:**
```yaml
interface: Backstage (full featured)
orchestration: ArgoCD + Crossplane
capabilities:
  - cicd: Tekton
  - database: Crossplane (RDS + CloudNativePG)
  - secrets: External Secrets + Vault
  - monitoring: Self-hosted Prometheus/Grafana
  - service_mesh: Istio

team_size: 6-8 platform engineers
focus: Self-service, golden paths
```

### Large Company (200+ Engineers)

**Recommended Stack:**
```yaml
interface: Backstage (custom plugins)
orchestration:
  - Crossplane (infrastructure)
  - ArgoCD (applications)
  - Custom orchestrator
capabilities:
  - cicd: Tekton + GitHub Actions
  - database: Multi-cloud abstraction
  - secrets: Vault (HA cluster)
  - monitoring: Observability platform
  - service_mesh: Istio + Cilium
  - cost: Kubecost enterprise
  - security: Custom security platform

team_size: 12-15 platform engineers
structure:
  - platform-core: 4-5 engineers
  - platform-security: 2-3 engineers
  - platform-dx: 2-3 engineers
  - platform-sre: 3-4 engineers
focus: Product platform, multi-tenancy
```

## Decision Framework

### Build vs Buy vs Adopt

**Evaluation Criteria:**

| Criteria | Build | Buy | Adopt OSS |
|----------|-------|-----|-----------|
| Time to Value | Months | Weeks | Weeks-Months |
| Customization | Full control | Limited | Moderate |
| Maintenance | High burden | Vendor managed | Community + internal |
| Cost | Engineer time | License fees | Engineer time |
| Expertise Required | High | Low | Moderate |
| Lock-in Risk | None | High | Low |

**Decision Matrix:**

```
Generic Capability → Adopt OSS (Backstage, Crossplane)
Standard Cloud Service → Buy (RDS, managed services)
Unique Business Logic → Build (custom workflows)
```

**Examples:**

- **Developer Portal**: Adopt Backstage ✓
- **Database**: Buy managed cloud service ✓
- **Orchestration**: Adopt Crossplane ✓
- **Custom Approval Flow**: Build ✓
- **Monitoring**: Adopt Prometheus + Grafana ✓
- **Compliance Reporting**: Build ✓

### Technology Selection Guide

**Criteria for Platform Technologies:**

1. **Adoption**: Large community, proven in production
2. **Extensibility**: Plugin system, APIs
3. **Observability**: Metrics, logs, health checks
4. **Declarative**: GitOps-compatible
5. **Cloud-Agnostic**: Not locked to single cloud
6. **Open Source**: Avoids vendor lock-in
7. **Enterprise Support**: Available if needed

**Recommended Technologies:**

- **Portal**: Backstage, Port, Cortex
- **GitOps**: ArgoCD, Flux
- **Infrastructure**: Crossplane, Terraform
- **CI/CD**: Tekton, GitHub Actions, GitLab CI
- **Secrets**: External Secrets + Vault
- **Service Mesh**: Istio, Linkerd, Cilium
- **Monitoring**: Prometheus, Grafana, Loki, Tempo
- **Policy**: Kyverno, OPA

## Migration Patterns

### Pattern: Brownfield Platform Adoption

**Challenge:** Existing services, legacy infrastructure

**Approach:**
```
Phase 1: Catalog (No disruption)
  └─ Import existing services into Backstage
  └─ Build ownership graph
  └─ Integrate monitoring, CI/CD status

Phase 2: Observe (Read-only)
  └─ Developers see their services
  └─ No changes required
  └─ Gather feedback

Phase 3: Pilot (1-2 services)
  └─ Migrate pilot services to golden paths
  └─ Document migration process
  └─ Measure before/after metrics

Phase 4: Enable (10-20% of services)
  └─ Offer migration assistance
  └─ Run workshops
  └─ Create migration runbooks

Phase 5: Scale (Majority)
  └─ New services default to platform
  └─ Legacy services gradually migrate
  └─ Platform becomes default
```

### Pattern: Greenfield Platform

**Challenge:** Building from scratch

**Approach:**
```
Month 1-2: Foundation
  └─ Kubernetes clusters
  └─ GitOps (ArgoCD)
  └─ Basic CI/CD

Month 3-4: Portal
  └─ Backstage setup
  └─ First templates (1-2)
  └─ Software catalog

Month 5-6: Capabilities
  └─ Database provisioning
  └─ Secrets management
  └─ Observability

Month 7-8: Refinement
  └─ More templates
  └─ Documentation
  └─ Developer onboarding

Month 9-12: Adoption
  └─ Marketing
  └─ Support and enablement
  └─ Metrics and iteration
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Building Without Users

**Problem:** Platform team builds in isolation

**Symptom:** Low adoption despite great technology

**Solution:**
- Conduct user research before building
- Co-design with developers
- Start with pilot teams
- Iterate based on feedback

### Anti-Pattern 2: Too Much Abstraction

**Problem:** Hide everything, no escape hatches

**Symptom:** Developers bypass platform for flexibility

**Solution:**
- Progressive disclosure
- Provide escape hatches
- Allow "bring your own"
- Document advanced usage

### Anti-Pattern 3: "Build It and They Will Come"

**Problem:** No change management or marketing

**Symptom:** Platform exists but nobody uses it

**Solution:**
- Active onboarding program
- Regular workshops
- Champion program
- Success stories and marketing

### Anti-Pattern 4: Optimizing for Platform Team

**Problem:** Prioritize platform team convenience over developers

**Symptom:** Complex interfaces, technical jargon

**Solution:**
- Developer-first design
- Usability testing
- Measure developer satisfaction
- Hide complexity

### Anti-Pattern 5: Boil the Ocean

**Problem:** Try to build everything at once

**Symptom:** Nothing ships, burnout, scope creep

**Solution:**
- Start with 1-2 core capabilities
- Ship iteratively
- Prioritize based on pain points
- Celebrate small wins

## Case Studies

### Case Study 1: E-Commerce Platform (500+ Engineers)

**Challenge:**
- 200+ microservices
- Inconsistent deployment practices
- Developer velocity declining
- 5-day time to first deployment

**Solution:**
- Implemented Backstage for catalog
- Created Node.js, Python, Go templates
- ArgoCD for GitOps
- Crossplane for database provisioning
- Preview environments per PR

**Results:**
- Time to first deployment: 5 days → 2 hours
- Deployment frequency: Weekly → Daily
- Developer satisfaction: +40%
- Ops tickets: -70%

### Case Study 2: FinTech Startup (50 Engineers)

**Challenge:**
- Rapid growth, need to scale
- Compliance requirements (SOC2, PCI)
- Manual infrastructure provisioning
- No standardization

**Solution:**
- Lightweight Backstage setup
- Terraform + GitHub Actions
- Vault for secrets
- Policy-as-code with OPA
- Automated compliance reporting

**Results:**
- SOC2 audit time: -60%
- Infrastructure provisioning: 2 days → 10 minutes
- Security incidents: -85%
- Passed PCI audit first time

### Case Study 3: SaaS Company (100 Engineers)

**Challenge:**
- Multi-tenant architecture
- Need isolated environments per customer
- Complex deployment dependencies
- Poor observability

**Solution:**
- Namespace-per-tenant model
- Backstage for service catalog
- ArgoCD ApplicationSets
- Observability platform (Prometheus + Grafana)
- Cost allocation per tenant

**Results:**
- Onboard new customer: 1 week → 1 hour
- Cost visibility: 0% → 100%
- MTTR: 4 hours → 30 minutes
- Customer isolation incidents: -100%
