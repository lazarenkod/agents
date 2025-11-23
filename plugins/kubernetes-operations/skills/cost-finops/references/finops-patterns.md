# FinOps Patterns and Best Practices

## Overview

This reference provides enterprise-grade FinOps patterns for Kubernetes cost management, covering cost allocation strategies, chargeback implementation, governance models, and organizational best practices.

## Cost Allocation Patterns

### 1. Hierarchical Allocation Model

**Multi-Level Cost Attribution:**

```
Organization ($1.2M/month)
├── Business Unit: Engineering ($800K)
│   ├── Team: Platform ($300K)
│   │   ├── Service: Monitoring ($80K)
│   │   ├── Service: CI/CD ($120K)
│   │   └── Service: API Gateway ($100K)
│   ├── Team: Backend ($350K)
│   │   ├── Service: Payments API ($180K)
│   │   ├── Service: User Service ($100K)
│   │   └── Service: Notifications ($70K)
│   └── Team: Data ($150K)
│       ├── Service: Data Pipeline ($90K)
│       └── Service: Analytics ($60K)
├── Business Unit: Product ($300K)
└── Business Unit: Marketing ($100K)
```

**Implementation:**

```yaml
# Namespace-level hierarchy
apiVersion: v1
kind: Namespace
metadata:
  name: platform-monitoring
  labels:
    # Level 1: Organization
    organization: "acme-corp"

    # Level 2: Business unit
    business-unit: "engineering"
    bu-cost-center: "CC-1000"

    # Level 3: Team
    team: "platform"
    team-cost-center: "CC-1100"
    team-lead: "alice@acme.com"

    # Level 4: Service
    service: "monitoring"
    service-owner: "bob@acme.com"

  annotations:
    # Budget allocation
    cost.kubernetes.io/budget-monthly: "80000"
    cost.kubernetes.io/budget-currency: "USD"

    # Allocation method
    cost.kubernetes.io/allocation: "direct"
    cost.kubernetes.io/shared-cost-weight: "1.0"
```

### 2. Shared Cost Allocation

**Allocation Strategies for Shared Resources:**

| Resource Type | Allocation Method | Rationale |
|--------------|-------------------|-----------|
| Cluster control plane | Equal split | Fixed cost independent of usage |
| Ingress controllers | Request-based | Proportional to traffic served |
| DNS services | Pod count | Proportional to service discovery usage |
| Monitoring infrastructure | Namespace CPU | Proportional to monitoring data volume |
| Logging infrastructure | Log volume | Direct correlation to usage |
| Security scanning | Pod count | Proportional to attack surface |

**Implementation Example:**

```yaml
# Shared cost allocation configuration
apiVersion: opencost.io/v1alpha1
kind: SharedCostAllocation
metadata:
  name: cluster-shared-costs
spec:
  resources:
    # Control plane costs
    - name: control-plane
      monthly_cost: 450.00
      allocation:
        method: equal
        targets:
          - type: namespace
            filter:
              exclude_namespaces: [kube-system, kube-public]

    # Ingress controller
    - name: ingress-nginx
      namespace: ingress-nginx
      allocation:
        method: proportional
        metric: nginx_ingress_controller_requests
        targets:
          - type: namespace

    # Monitoring stack (Prometheus + Grafana)
    - name: monitoring-stack
      namespace: monitoring
      allocation:
        method: proportional
        metric: sum(rate(container_cpu_usage_seconds_total))
        targets:
          - type: namespace

    # Centralized logging (Loki)
    - name: logging-stack
      namespace: logging
      allocation:
        method: proportional
        metric: sum(rate(loki_distributor_bytes_received_total))
        targets:
          - type: namespace

  # Idle cost allocation
  idle_costs:
    method: proportional
    allocation_base: resource_requests
```

### 3. Multi-Tenancy Cost Patterns

**Isolated Tenant Model:**

```yaml
# Dedicated namespace per tenant
---
apiVersion: v1
kind: Namespace
metadata:
  name: tenant-acme
  labels:
    tenant-id: "acme-corp"
    tenant-tier: "enterprise"
    billing-account: "BA-12345"
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-acme-quota
  namespace: tenant-acme
spec:
  hard:
    requests.cpu: "100"
    requests.memory: "200Gi"
    requests.storage: "1Ti"
    persistentvolumeclaims: "50"
  scopeSelector:
    matchExpressions:
    - operator: Exists
      scopeName: NotTerminating
---
# Cost tracking ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: tenant-billing-config
  namespace: tenant-acme
data:
  billing_account: "BA-12345"
  cost_center: "CC-ACME-001"
  pricing_tier: "enterprise"
  # Custom pricing multiplier (1.0 = standard rate)
  pricing_multiplier: "0.85"  # 15% enterprise discount
  invoice_frequency: "monthly"
  payment_terms: "net-30"
```

**Shared Cluster Multi-Tenancy:**

```yaml
# Multi-tenant with namespace isolation
tenants:
  - name: tenant-a
    namespaces: [tenant-a-prod, tenant-a-staging]
    allocation:
      method: direct
      overhead_charge: 5%  # Management fee

  - name: tenant-b
    namespaces: [tenant-b-prod, tenant-b-staging, tenant-b-dev]
    allocation:
      method: direct
      overhead_charge: 5%

  - name: internal
    namespaces: [platform-*]
    allocation:
      method: internal-cost-center
      chargeback: false
```

## Chargeback Implementation

### 1. Pricing Model Design

**Consumption-Based Pricing:**

```yaml
# Pricing tiers
pricing:
  # Compute pricing
  compute:
    cpu:
      unit: "core-hour"
      tiers:
        - name: on-demand
          rate_usd: 0.031
          description: "Standard on-demand pricing"

        - name: reserved-1yr
          rate_usd: 0.020
          discount: 35%
          commitment: "1-year"

        - name: reserved-3yr
          rate_usd: 0.015
          discount: 52%
          commitment: "3-year"

        - name: spot
          rate_usd: 0.009
          discount: 71%
          availability: "best-effort"

    memory:
      unit: "GB-hour"
      tiers:
        - name: on-demand
          rate_usd: 0.004
        - name: reserved-1yr
          rate_usd: 0.0026
          discount: 35%

  # Storage pricing
  storage:
    persistent_volumes:
      standard_hdd:
        unit: "GB-month"
        rate_usd: 0.05
      standard_ssd:
        unit: "GB-month"
        rate_usd: 0.17
      premium_ssd:
        unit: "GB-month"
        rate_usd: 0.35

    snapshots:
      unit: "GB-month"
      rate_usd: 0.026

  # Network pricing
  network:
    ingress:
      rate_usd: 0.00  # Free
    egress_internal:
      rate_usd: 0.01  # Per GB, same region
    egress_internet:
      rate_usd: 0.09  # Per GB, to internet

  # Load balancer pricing
  load_balancers:
    network_lb:
      hourly_rate: 0.025
      data_processed_gb: 0.008
    application_lb:
      hourly_rate: 0.040
      data_processed_gb: 0.008
```

**Cost Calculation Formula:**

```python
def calculate_monthly_cost(namespace_metrics):
    """
    Calculate monthly cost for a namespace.

    Cost = Base Resources + Storage + Network + Shared Costs + Overhead
    """
    # Base compute costs
    cpu_cost = (
        namespace_metrics['cpu_core_hours'] *
        pricing['compute']['cpu']['on-demand']['rate_usd']
    )

    memory_cost = (
        namespace_metrics['memory_gb_hours'] *
        pricing['compute']['memory']['on-demand']['rate_usd']
    )

    # Storage costs
    pv_cost = sum([
        volume['size_gb'] * pricing['storage']['persistent_volumes'][volume['class']]['rate_usd']
        for volume in namespace_metrics['persistent_volumes']
    ])

    # Network costs
    network_cost = (
        namespace_metrics['egress_internet_gb'] *
        pricing['network']['egress_internet']['rate_usd']
    )

    # Shared cost allocation (proportional)
    total_cluster_cpu = get_cluster_total_cpu_hours()
    shared_cost_allocation = (
        (namespace_metrics['cpu_core_hours'] / total_cluster_cpu) *
        get_monthly_shared_costs()
    )

    # Management overhead (5%)
    overhead = (cpu_cost + memory_cost + pv_cost + network_cost) * 0.05

    total_cost = (
        cpu_cost +
        memory_cost +
        pv_cost +
        network_cost +
        shared_cost_allocation +
        overhead
    )

    return {
        'compute': cpu_cost + memory_cost,
        'storage': pv_cost,
        'network': network_cost,
        'shared': shared_cost_allocation,
        'overhead': overhead,
        'total': total_cost
    }
```

### 2. Billing Cycle Implementation

**Monthly Billing Process:**

```yaml
# Billing automation workflow
billing_workflow:
  schedule: "0 2 1 * *"  # 2 AM on first day of month

  steps:
    1_data_collection:
      - query_prometheus_metrics:
          range: "last_month"
          metrics:
            - container_cpu_usage_seconds_total
            - container_memory_working_set_bytes
            - kube_persistentvolumeclaim_resource_requests_storage_bytes
            - network_egress_bytes_total

      - export_opencost_data:
          format: json
          aggregation: namespace

    2_cost_calculation:
      - apply_pricing_model:
          source: pricing_config.yaml
          adjustments:
            - reserved_capacity_discounts
            - volume_discounts
            - promotional_credits

      - allocate_shared_costs:
          method: proportional
          resources:
            - control_plane
            - monitoring
            - ingress
            - dns

    3_invoice_generation:
      - generate_invoice:
          format: pdf
          language: [en, ru]
          include:
            - cost_breakdown
            - usage_trends
            - optimization_recommendations

      - store_invoice:
          location: s3://billing-invoices/
          retention: 7_years

    4_notification:
      - send_invoice:
          recipients: billing_contacts
          cc: namespace_owners
          method: email

      - publish_to_dashboard:
          url: https://finops.company.com

    5_reconciliation:
      - compare_to_cloud_bill:
          tolerance: 5%
          alert_on_mismatch: true

      - update_ledger:
          system: erp
          cost_center_mapping: billing_config
```

### 3. Chargeback Report Template

**Monthly Invoice Structure:**

```markdown
# Monthly Kubernetes Cost Invoice

**Invoice Period:** October 2024
**Namespace:** platform-monitoring
**Cost Center:** CC-1100
**Business Unit:** Engineering - Platform Team

---

## Summary

| Category | Cost (USD) |
|----------|-----------|
| Compute | $3,245.67 |
| Storage | $856.32 |
| Network | $234.12 |
| Shared Services | $445.89 |
| Management Overhead (5%) | $239.10 |
| **Total** | **$5,021.10** |

---

## Compute Costs

### CPU Usage
- **Total Core-Hours:** 104,700
- **Average Cores:** 142.5
- **Rate:** $0.031 per core-hour
- **Cost:** $3,245.70

**Top 5 Deployments by CPU Cost:**
1. prometheus-server: $1,234.56 (38%)
2. grafana: $567.89 (18%)
3. alertmanager: $345.67 (11%)
4. kube-state-metrics: $234.56 (7%)
5. node-exporter: $178.90 (6%)

### Memory Usage
- **Total GB-Hours:** 214,080
- **Average GB:** 291.5
- **Rate:** $0.004 per GB-hour
- **Cost:** $856.32

---

## Storage Costs

| Volume Name | Type | Size (GB) | Cost |
|------------|------|-----------|------|
| prometheus-data-0 | premium-ssd | 500 | $175.00 |
| prometheus-data-1 | premium-ssd | 500 | $175.00 |
| grafana-data | standard-ssd | 100 | $17.00 |
| alertmanager-data | standard-ssd | 50 | $8.50 |
| **Total** | | **1,150** | **$375.50** |

**Snapshots:** 12 snapshots × 480 GB × $0.026 = $149.76

---

## Network Costs

- **Ingress:** 2.4 TB (Free)
- **Egress (internal):** 1.8 TB × $0.01 = $18.00
- **Egress (internet):** 0.3 TB × $0.09 = $27.00
- **Load Balancers:** 2 × 730 hours × $0.025 = $36.50
- **Total Network:** $81.50

---

## Shared Services Allocation

Your namespace consumed **6.8%** of cluster resources.

| Service | Total Cost | Your Share | Allocation Method |
|---------|-----------|------------|-------------------|
| Control Plane | $2,500 | $170.00 | Equal split (34 namespaces) |
| Ingress Controller | $1,200 | $81.60 | Request count (6.8%) |
| DNS Services | $800 | $54.40 | Pod count (6.8%) |
| Logging Infrastructure | $3,000 | $204.00 | Log volume (6.8%) |
| **Total Shared** | **$7,500** | **$510.00** | |

---

## Month-over-Month Comparison

| Month | Total Cost | Change |
|-------|-----------|--------|
| August 2024 | $4,567.89 | - |
| September 2024 | $4,789.23 | +4.8% |
| **October 2024** | **$5,021.10** | **+4.8%** |

**Trend:** Costs have increased 10% over the last quarter due to:
- Additional Prometheus retention (30d → 45d)
- New Grafana dashboards increasing query load
- Expanded monitoring coverage (+15 new services)

---

## Cost Optimization Recommendations

1. **Right-size prometheus-server** (Potential savings: $450/month)
   - Current: 4 cores, 8GB memory
   - Recommended: 2.5 cores, 5GB memory
   - Reason: P95 usage is 2.2 cores, 4.5GB

2. **Migrate snapshots to cheaper storage** (Potential savings: $85/month)
   - Current: Premium SSD snapshots
   - Recommended: Standard HDD snapshots
   - Reason: Snapshots accessed rarely

3. **Enable compression for metrics** (Potential savings: $120/month)
   - Reduce storage requirements by ~30%
   - Minimal CPU overhead

**Total potential savings: $655/month (13% reduction)**

---

## Payment Information

**Payment Due:** November 15, 2024
**Payment Method:** Internal cost center transfer
**Questions:** finops-team@company.com
```

## Showback vs. Chargeback Decision Framework

### When to Use Showback

**Best for:**
- Early-stage FinOps maturity (Crawl phase)
- Organizations building cost awareness
- Teams without established budgets
- Environments where accurate allocation is still being refined
- Internal platform teams

**Benefits:**
- Low friction, high transparency
- Builds cost culture without financial pressure
- Easier to implement and iterate
- Encourages voluntary optimization

**Implementation:**
```yaml
showback:
  enabled: true
  reporting:
    frequency: weekly
    recipients:
      type: namespace_owners
      cc: management
    format:
      - email_summary
      - dashboard_link
      - csv_export

  content:
    - total_cost
    - cost_by_workload
    - cost_trends
    - peer_comparison  # Anonymous benchmarking
    - optimization_opportunities

  gamification:
    enabled: true
    leaderboard: cost_efficiency
    rewards: quarterly_recognition
```

### When to Use Chargeback

**Best for:**
- Mature FinOps organizations (Walk/Run phase)
- Cost centers with defined budgets
- Multi-tenant platforms
- SaaS platforms with external customers
- Business units with P&L accountability

**Prerequisites:**
- Accurate cost allocation (95%+ accuracy)
- Established pricing model
- Buy-in from finance and leadership
- Clear escalation processes
- Budget management tools

**Implementation:**
```yaml
chargeback:
  enabled: true
  billing_period: monthly
  currency: USD

  pricing_model:
    source: pricing_config.yaml
    update_frequency: quarterly
    approval_required: true

  invoice_generation:
    automatic: true
    approval_workflow:
      - namespace_owner_review
      - cost_center_approval
      - finance_validation

  payment:
    method: internal_transfer
    due_date: 15  # Days after invoice
    late_fee: 2%

  dispute_resolution:
    window: 10_days
    escalation:
      - namespace_owner
      - finance_team
      - vp_engineering
```

## FinOps Governance Models

### 1. Centralized Governance

**Structure:**
- Central FinOps team owns all cost decisions
- Teams submit requests for resource increases
- Top-down budget allocation

**Best for:** Small organizations, strict cost control needed

```yaml
governance:
  model: centralized
  finops_team:
    responsibilities:
      - budget_planning
      - cost_allocation
      - optimization_decisions
      - policy_enforcement

  approval_workflows:
    resource_increase:
      - team_request
      - finops_review
      - finance_approval
      - implementation

    new_workload:
      - cost_estimate_required
      - finops_approval
      - budget_allocation
      - deployment
```

### 2. Federated Governance

**Structure:**
- Teams have budget autonomy
- FinOps team provides tools and guidance
- Teams responsible for staying within budget

**Best for:** Large organizations, mature teams

```yaml
governance:
  model: federated
  finops_team:
    responsibilities:
      - provide_cost_visibility_tools
      - define_best_practices
      - offer_optimization_guidance
      - manage_shared_resources

  team_autonomy:
    budget_authority: true
    optimization_decisions: team_owned
    policy_compliance: required

  guardrails:
    - resource_quotas
    - budget_alerts
    - automated_shutdowns  # Dev/test after hours
    - cost_approval_thresholds:
        under_1000: team_approved
        1000_to_5000: manager_approved
        over_5000: director_approved
```

### 3. Hybrid Governance

**Structure:**
- Central control for shared resources
- Team autonomy for dedicated resources
- Collaborative optimization

**Best for:** Most enterprise organizations

```yaml
governance:
  model: hybrid

  centralized:
    resources:
      - cluster_control_plane
      - ingress_controllers
      - monitoring_infrastructure
      - security_scanning
    decision_authority: finops_team

  federated:
    resources:
      - application_workloads
      - team_namespaces
      - development_environments
    decision_authority: product_teams
    constraints:
      - must_comply_with_policies
      - must_stay_within_budget
      - must_use_approved_tools

  collaboration:
    monthly_reviews: true
    optimization_workshops: quarterly
    shared_kpis:
      - cluster_utilization
      - cost_per_request
      - waste_percentage
```

## KPI Framework

### Technical Efficiency KPIs

```yaml
technical_kpis:
  - name: cluster_cpu_utilization
    formula: |
      avg(
        sum(rate(container_cpu_usage_seconds_total[5m]))
        /
        sum(kube_node_status_allocatable{resource="cpu"})
      )
    target: ">60%"
    alert_threshold: "<40%"

  - name: cluster_memory_utilization
    formula: |
      avg(
        sum(container_memory_working_set_bytes)
        /
        sum(kube_node_status_allocatable{resource="memory"})
      )
    target: ">65%"
    alert_threshold: "<45%"

  - name: resource_request_accuracy
    formula: |
      avg(
        container_cpu_usage_seconds_total
        /
        kube_pod_container_resource_requests{resource="cpu"}
      )
    target: "60-80%"
    description: "Sweet spot: not over-provisioned, not throttled"

  - name: waste_percentage
    formula: |
      (
        sum(kube_pod_container_resource_requests)
        -
        sum(container_resource_usage)
      ) / sum(kube_pod_container_resource_requests) * 100
    target: "<20%"
    alert_threshold: ">30%"
```

### Financial KPIs

```yaml
financial_kpis:
  - name: cost_per_namespace
    unit: USD/month
    tracking: monthly_trend
    benchmarking: peer_comparison

  - name: cost_per_request
    formula: |
      monthly_infrastructure_cost
      /
      sum(http_requests_total)
    unit: USD/million_requests
    benchmark: industry_average

  - name: cost_per_customer
    formula: |
      total_platform_cost
      /
      active_customers
    unit: USD/customer/month
    target: continuous_reduction

  - name: infrastructure_cost_as_percentage_of_revenue
    formula: |
      (infrastructure_cost / revenue) * 100
    target: "<15%"
    industry_benchmark: "10-20%"
```

### Optimization KPIs

```yaml
optimization_kpis:
  - name: spot_instance_coverage
    formula: |
      spot_instance_hours
      /
      total_instance_hours * 100
    target: ">40%"
    workload_filter: fault_tolerant

  - name: reserved_capacity_utilization
    formula: |
      reserved_instance_hours_used
      /
      reserved_instance_hours_purchased * 100
    target: ">85%"
    alert_threshold: "<70%"

  - name: monthly_savings_from_recommendations
    unit: USD/month
    tracking: cumulative
    breakdown:
      - rightsizing
      - spot_migration
      - storage_optimization
      - unused_resource_cleanup

  - name: recommendation_implementation_rate
    formula: |
      recommendations_implemented
      /
      recommendations_generated * 100
    target: ">60%"
```

## Cost Anomaly Patterns

### Common Anomaly Types

1. **Gradual Resource Leak**
   - **Pattern:** Slow, steady cost increase
   - **Cause:** Memory leaks, unclosed connections
   - **Detection:** Week-over-week trend analysis
   - **Resolution:** Restart deployments, fix leaks

2. **Sudden Spike**
   - **Pattern:** Sharp cost increase (>50% in 1 hour)
   - **Cause:** Traffic surge, DDoS, autoscaling runaway
   - **Detection:** Real-time alerting
   - **Resolution:** Investigate traffic patterns, check HPA

3. **Zombie Resources**
   - **Pattern:** Flat cost for unused resources
   - **Cause:** Forgotten test environments, old PVCs
   - **Detection:** Utilization <5% for >7 days
   - **Resolution:** Automated cleanup policies

4. **Storage Bloat**
   - **Pattern:** Exponential storage growth
   - **Cause:** No log rotation, missing TTL
   - **Detection:** Storage growth rate analysis
   - **Resolution:** Implement retention policies

**Anomaly Detection Query:**

```promql
# Detect namespace cost anomalies
(
  sum by (namespace) (
    rate(container_cpu_usage_seconds_total[1h]) * 0.031 +
    avg_over_time(container_memory_working_set_bytes[1h]) / 1e9 * 0.004
  )
  /
  avg_over_time(
    sum by (namespace) (
      rate(container_cpu_usage_seconds_total[1h]) * 0.031 +
      avg_over_time(container_memory_working_set_bytes[1h]) / 1e9 * 0.004
    )[7d:1h]
  )
) > 1.5
```

## Best Practices Summary

1. **Tag Everything**
   - Consistent labeling from day one
   - Automated tag enforcement
   - Regular tag audits

2. **Allocate Shared Costs Fairly**
   - Use proportional allocation
   - Document allocation methods
   - Review quarterly

3. **Start Simple, Iterate**
   - Begin with showback
   - Refine allocation accuracy
   - Graduate to chargeback

4. **Automate Recommendations**
   - Daily right-sizing analysis
   - Automated idle resource cleanup
   - Proactive alerts

5. **Build a Cost Culture**
   - Make costs visible
   - Incentivize optimization
   - Celebrate efficiency wins

6. **Measure and Improve**
   - Track KPIs monthly
   - Benchmark against peers
   - Set annual improvement targets

7. **Governance with Flexibility**
   - Set guardrails, not gates
   - Enable self-service
   - Support experimentation

## Tools and Integrations

### Recommended Stack

- **Cost Monitoring:** OpenCost or KubeCost
- **Metrics:** Prometheus + Thanos (multi-cluster)
- **Visualization:** Grafana
- **Alerting:** Alertmanager
- **Reporting:** Custom scripts + BI tools (Looker, Tableau)
- **Automation:** Argo Workflows, Tekton
- **Cloud Integration:** Cloud provider cost APIs

### Integration Points

```yaml
integrations:
  # Cloud provider billing
  aws:
    api: cost_explorer
    features:
      - reserved_instance_recommendations
      - savings_plans
      - budgets_alerts

  azure:
    api: cost_management
    features:
      - advisor_recommendations
      - budgets
      - reservations

  gcp:
    api: billing_api
    features:
      - committed_use_discounts
      - budget_alerts
      - recommender

  # Financial systems
  erp:
    type: sap
    integration: cost_center_sync
    frequency: monthly

  # Communication
  slack:
    channels:
      - finops-alerts
      - cost-optimization
    notifications:
      - daily_summaries
      - anomaly_alerts
      - monthly_reports
```

---

**Related References:**
- optimization-guide.md — Detailed right-sizing and resource optimization
- cloud-cost-management.md — Cloud provider-specific cost optimization
